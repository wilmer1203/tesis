"""
Estado Centralizado para Odontograma Interactivo V2.0
Gestión completa del estado para dientes clickeables y superficies interactivas
"""
import reflex as rx
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# Imports del sistema
from dental_system.models.odontograma_avanzado_models import (
    DienteInteractivoModel,
    CondicionCaraModel,
    OdontogramaInteractivoModel,
    TipoCondicion,
    SeveridadCondicion,
    CaraDiente,
    CONDICIONES_DISPONIBLES,
    CARAS_DIENTE
)
from dental_system.utils.logger import dental_logger


class EstadoOdontogramaInteractivo(rx.State, mixin=True):
    """
    Estado centralizado para odontograma completamente interactivo

    Funcionalidades:
    - Gestión de dientes y caras seleccionadas
    - Aplicación de condiciones en tiempo real
    - Versionado automático de cambios
    - Estados de UI (modales, selecciones)
    - Guardado automático con debounce
    - Comparación entre versiones
    """

    # ===========================================
    # DATOS PRINCIPALES DEL ODONTOGRAMA
    # ===========================================

    # Odontograma actual
    odontograma_actual: OdontogramaInteractivoModel = OdontogramaInteractivoModel.crear_odontograma_adulto("")
    numero_historia_actual: str = ""

    # Estados de selección
    diente_seleccionado: Optional[DienteInteractivoModel] = None
    numero_diente_seleccionado: int = 0
    cara_seleccionada: str = ""

    # Historial y versionado
    versiones_disponibles: List[OdontogramaInteractivoModel] = []
    version_comparacion: Optional[OdontogramaInteractivoModel] = None
    cambios_pendientes: List[Dict[str, Any]] = []

    # ===========================================
    # ESTADOS DE UI
    # ===========================================

    # Modales y ventanas
    show_modal_diente: bool = False
    show_selector_condiciones: bool = False
    show_comparador_versiones: bool = False
    show_historial_cambios: bool = False

    # Estados de edición
    modo_edicion_ui: bool = False
    guardando_cambios: bool = False
    hay_cambios_sin_guardar: bool = False

    # Tab activo en modal de diente
    tab_activo_diente: str = "superficies"  # superficies, historial, tratamientos, notas

    # Estados de carga
    cargando_odontograma: bool = False
    cargando_historial: bool = False
    error_mensaje: str = ""

    # ===========================================
    # CONFIGURACIÓN Y FILTROS
    # ===========================================

    # Filtros de visualización
    mostrar_solo_condiciones: bool = False
    mostrar_solo_criticos: bool = False
    filtro_tipo_condicion: str = "todos"

    # Configuración de guardado
    auto_guardar_habilitado: bool = True
    intervalo_auto_guardado: int = 30  # segundos

    # Estadísticas en tiempo real
    total_dientes_afectados: int = 0
    total_condiciones_criticas: int = 0
    costo_total_estimado: float = 0.0

    # ===========================================
    # MÉTODOS DE INICIALIZACIÓN
    # ===========================================

    async def cargar_odontograma_paciente(self, paciente_id: str):
        """
        Cargar odontograma de un paciente específico

        Args:
            paciente_id: ID del paciente (UUID)
        """
        self.cargando_odontograma = True
        self.error_mensaje = ""

        try:
            dental_logger.info(f"Cargando odontograma para paciente ID: {paciente_id}")

            # ✅ FIX: Obtener información del paciente por ID para tener HC
            from dental_system.supabase.tablas.pacientes import pacientes_table
            paciente_data = pacientes_table.get_by_id(paciente_id)

            if paciente_data:
                numero_historia = paciente_data.get("numero_historia", "")
                self.numero_historia_actual = numero_historia
                dental_logger.info(f"✅ Paciente encontrado: HC {numero_historia}")
            else:
                self.error_mensaje = f"Paciente con ID {paciente_id} no encontrado"
                return

            # ✅ INTEGRACIÓN REAL: Usar odontologia_service para obtener datos reales
            from dental_system.services.odontologia_service import odontologia_service

            # Establecer contexto de usuario
            from dental_system.state.app_state import AppState
            user_context = AppState.obtener_contexto_usuario()
            if user_context:
                odontologia_service.set_user_context(
                    user_context.get("id_usuario", ""),
                    user_context
                )

            # Obtener odontograma real de la base de datos
            odontograma_real = odontologia_service.get_patient_odontogram(paciente_id)

            if odontograma_real:
                dental_logger.info(f"✅ Odontograma cargado desde BD para paciente {paciente_id}")
                # Aquí podríamos convertir el odontograma real al modelo interactivo
                # Por ahora mantenemos la simulación
                if not self.odontograma_actual.numero_historia:
                    self.odontograma_actual = OdontogramaInteractivoModel.crear_odontograma_adulto(
                        numero_historia
                    )
            else:
                # Crear odontograma nuevo si no existe
                self.odontograma_actual = OdontogramaInteractivoModel.crear_odontograma_adulto(
                    numero_historia
                )
                dental_logger.info(f"🆕 Creado nuevo odontograma para paciente {paciente_id}")

            # Cargar versiones históricas
            await self._cargar_versiones_historicas(numero_historia)

            # Actualizar estadísticas
            self._actualizar_estadisticas()

            dental_logger.info(f"Odontograma cargado exitosamente: {self.odontograma_actual.resumen_estado}")

        except Exception as e:
            self.error_mensaje = f"Error cargando odontograma: {str(e)}"
            dental_logger.error("Error cargando odontograma", error=e)

        finally:
            self.cargando_odontograma = False

    async def _cargar_versiones_historicas(self, numero_historia: str):
        """Cargar historial de versiones del odontograma"""
        # En implementación real consultaríamos la BD
        # Por ahora simulamos versiones históricas
        self.versiones_disponibles = [self.odontograma_actual]

    # ===========================================
    # MÉTODOS DE SELECCIÓN
    # ===========================================

    def seleccionar_diente(self, numero_fdi: int):
        """
        Seleccionar diente para edición

        Args:
            numero_fdi: Número FDI del diente (11-18, 21-28, etc.)
        """
        dental_logger.info(f"Seleccionando diente FDI: {numero_fdi}")

        # Deseleccionar todos los dientes
        for diente in self._obtener_dientes_seguros():
            diente.is_selected = False

        # Seleccionar el diente target
        diente_target = self.odontograma_actual.get_diente_por_fdi(numero_fdi)

        if diente_target:
            diente_target.is_selected = True
            self.diente_seleccionado = diente_target
            self.numero_diente_seleccionado = numero_fdi
            self.show_modal_diente = True
            self.tab_activo_diente = "superficies"

            dental_logger.info(f"Diente {numero_fdi} seleccionado: {diente_target.estado_display}")
        else:
            self.error_mensaje = f"Diente FDI {numero_fdi} no encontrado"

    def seleccionar_cara_diente(self, cara: str):
        """
        Seleccionar cara específica del diente

        Args:
            cara: Nombre de la cara (oclusal, mesial, distal, vestibular, lingual)
        """
        if self.diente_seleccionado:
            self.cara_seleccionada = cara
            self.show_selector_condiciones = True

            cara_obj = self.diente_seleccionado.get_cara_por_nombre(cara)
            if cara_obj:
                dental_logger.info(
                    f"Cara {cara} seleccionada en diente {self.numero_diente_seleccionado}: "
                    f"{cara_obj.descripcion_condicion}"
                )

    def deseleccionar_todo(self):
        """Deseleccionar diente y cara"""
        for diente in self._obtener_dientes_seguros():
            diente.is_selected = False

        self.diente_seleccionado = None
        self.numero_diente_seleccionado = 0
        self.cara_seleccionada = ""
        self.show_modal_diente = False
        self.show_selector_condiciones = False

    # ===========================================
    # MÉTODOS DE EDICIÓN
    # ===========================================

    async def aplicar_condicion_cara(self,
                                   tipo_condicion: str,
                                   severidad: str = SeveridadCondicion.LEVE,
                                   notas: str = ""):
        """
        Aplicar condición a la cara seleccionada

        Args:
            tipo_condicion: Tipo de condición a aplicar
            severidad: Severidad de la condición
            notas: Notas adicionales
        """
        if not self.diente_seleccionado or not self.cara_seleccionada:
            self.error_mensaje = "Debe seleccionar un diente y una cara"
            return

        try:
            # Aplicar la condición
            success = self.diente_seleccionado.actualizar_cara(
                self.cara_seleccionada,
                tipo_condicion,
                severidad,
                notas
            )

            if success:
                # Registrar cambio para guardado
                cambio = {
                    "timestamp": datetime.now().isoformat(),
                    "diente_fdi": self.numero_diente_seleccionado,
                    "cara": self.cara_seleccionada,
                    "tipo_condicion": tipo_condicion,
                    "severidad": severidad,
                    "notas": notas
                }
                self.cambios_pendientes.append(cambio)
                self.hay_cambios_sin_guardar = True

                # Actualizar estadísticas
                self._actualizar_estadisticas()

                # Auto-guardar si está habilitado
                if self.auto_guardar_habilitado:
                    await self.guardar_cambios_automatico()

                dental_logger.info(
                    f"Condición aplicada: Diente {self.numero_diente_seleccionado}, "
                    f"cara {self.cara_seleccionada}, condición {tipo_condicion}"
                )

                # Cerrar selector de condiciones
                self.show_selector_condiciones = False

            else:
                self.error_mensaje = "Error aplicando condición"

        except Exception as e:
            self.error_mensaje = f"Error aplicando condición: {str(e)}"
            dental_logger.error("Error aplicando condición", error=e)

    async def resetear_cara_diente(self):
        """Resetear cara seleccionada a estado sano"""
        await self.aplicar_condicion_cara(
            TipoCondicion.SANO,
            SeveridadCondicion.LEVE,
            "Superficie reseteda a estado sano"
        )

    async def resetear_diente_completo(self):
        """Resetear todas las caras del diente seleccionado"""
        if not self.diente_seleccionado:
            return

        caras = [CaraDiente.OCLUSAL, CaraDiente.MESIAL, CaraDiente.DISTAL,
                CaraDiente.VESTIBULAR, CaraDiente.LINGUAL]

        for cara in caras:
            self.cara_seleccionada = cara
            await self.aplicar_condicion_cara(TipoCondicion.SANO)

        dental_logger.info(f"Diente {self.numero_diente_seleccionado} reseteado completamente")

    # ===========================================
    # MÉTODOS DE GUARDADO Y VERSIONADO
    # ===========================================

    @rx.event
    async def guardar_cambios_automatico(self):
        """Guardar cambios automáticamente con nueva versión"""
        async with self:
            if not self.hay_cambios_sin_guardar:
                return

            self.guardando_cambios = True

            try:
                # Crear nueva versión del odontograma
                nueva_version = await self._crear_nueva_version_odontograma()

                if nueva_version:
                    # Actualizar versión actual
                    self.odontograma_actual.version = nueva_version["version"]
                    self.odontograma_actual.id = nueva_version["id"]
                    self.odontograma_actual.fecha_ultima_modificacion = datetime.now().isoformat()

                    # Limpiar cambios pendientes
                    self.cambios_pendientes = []
                    self.hay_cambios_sin_guardar = False

                    # Actualizar historial
                    await self._cargar_versiones_historicas(self.numero_historia_actual)

                    dental_logger.info(f"Odontograma guardado - versión {nueva_version['version']}")

                    # Mostrar notificación temporal
                    await self._mostrar_notificacion("Cambios guardados automáticamente", "success")

            except Exception as e:
                self.error_mensaje = f"Error guardando cambios: {str(e)}"
                dental_logger.error("Error guardando odontograma", error=e)

            finally:
                self.guardando_cambios = False

    async def _crear_nueva_version_odontograma(self) -> Dict[str, Any]:
        """Crear nueva versión en base de datos (simulado)"""
        # En implementación real usaríamos el servicio de odontograma
        nueva_version = {
            "id": f"odonto_{datetime.now().timestamp()}",
            "version": self.odontograma_actual.version + 1,
            "motivo": f"Actualización automática - {len(self.cambios_pendientes)} cambios"
        }

        # Simular guardado en BD
        await rx.sleep(0.5)  # Simular latencia

        return nueva_version

    # ===========================================
    # MÉTODOS DE COMPARACIÓN Y HISTORIAL
    # ===========================================

    def mostrar_comparador_versiones(self):
        """Abrir modal de comparación de versiones"""
        self.show_comparador_versiones = True

    def seleccionar_version_comparacion(self, version_id: str):
        """Seleccionar versión para comparar"""
        for version in self.versiones_disponibles:
            if version.id == version_id:
                self.version_comparacion = version
                break

    def obtener_cambios_entre_versiones(self) -> List[Dict[str, Any]]:
        """Obtener lista de cambios entre versión actual y comparación"""
        if not self.version_comparacion:
            return []

        cambios = []

        # Comparar cada diente
        for diente_actual in self._obtener_dientes_seguros():
            diente_anterior = self.version_comparacion.get_diente_por_fdi(diente_actual.numero_fdi)

            if diente_anterior:
                # Comparar cada cara
                caras = [
                    ("oclusal", diente_actual.cara_oclusal, diente_anterior.cara_oclusal),
                    ("mesial", diente_actual.cara_mesial, diente_anterior.cara_mesial),
                    ("distal", diente_actual.cara_distal, diente_anterior.cara_distal),
                    ("vestibular", diente_actual.cara_vestibular, diente_anterior.cara_vestibular),
                    ("lingual", diente_actual.cara_lingual, diente_anterior.cara_lingual)
                ]

                for nombre_cara, cara_actual, cara_anterior in caras:
                    if cara_actual.tipo_condicion != cara_anterior.tipo_condicion:
                        cambios.append({
                            "numero_diente": diente_actual.numero_fdi,
                            "cara": nombre_cara,
                            "tipo_cambio": "condicion_modificada",
                            "condicion_anterior": cara_anterior.descripcion_condicion,
                            "condicion_actual": cara_actual.descripcion_condicion,
                            "fecha_cambio": cara_actual.fecha_ultima_modificacion
                        })

        return cambios

    # ===========================================
    # MÉTODOS DE UI Y UTILIDADES
    # ===========================================

    def cambiar_tab_modal(self, tab: str):
        """Cambiar tab activo en modal de diente"""
        tabs_validos = ["superficies", "historial", "tratamientos", "notas"]
        if tab in tabs_validos:
            self.tab_activo_diente = tab

    def cerrar_modal_diente(self):
        """Cerrar modal de diente"""
        self.show_modal_diente = False
        self.show_selector_condiciones = False
        self.tab_activo_diente = "superficies"
        
    @rx.event
    def toggle_modo_edicion(self):
        """Alternar modo de edición"""
        # Reflex requiere asignaciones directas, no operaciones con Vars
        self.modo_edicion_ui =  not self.modo_edicion_ui


    def aplicar_filtro_visualizacion(self, filtro: str):
        """Aplicar filtro de visualización"""
        if filtro == "solo_condiciones":
            self.mostrar_solo_condiciones = not self.mostrar_solo_condiciones
        elif filtro == "solo_criticos":
            self.mostrar_solo_criticos = not self.mostrar_solo_criticos
        else:
            self.filtro_tipo_condicion = filtro

    def _actualizar_estadisticas(self):
        """Actualizar estadísticas en tiempo real"""
        self.total_dientes_afectados = self.odontograma_actual.numero_dientes_afectados
        if hasattr(self.odontograma_actual, 'dientes_criticos'):
            self.total_condiciones_criticas = len(self.odontograma_actual.dientes_criticos)
        else:
            self.total_condiciones_criticas = 0
        self.costo_total_estimado = self.odontograma_actual.costo_total_estimado

    async def _mostrar_notificacion(self, mensaje: str, tipo: str = "info"):
        """Mostrar notificación temporal"""
        # En implementación real usaríamos un sistema de toast/notificaciones
        dental_logger.info(f"Notificación {tipo}: {mensaje}")

    # ===========================================
    # MÉTODOS AUXILIARES DE SEGURIDAD
    # ===========================================

    def _obtener_dientes_seguros(self) -> List[DienteInteractivoModel]:
        """Obtener dientes del odontograma de forma segura"""
        if not hasattr(self.odontograma_actual, 'dientes'):
            return []
        return self.odontograma_actual.dientes or []

    # ===========================================
    # MÉTODOS COMPUTADOS PARA UI
    # ===========================================

    @rx.var
    def dientes_filtrados(self) -> List[DienteInteractivoModel]:
        """Obtener dientes según filtros activos"""
        dientes = self._obtener_dientes_seguros()
        if not dientes:
            return []

        if self.mostrar_solo_condiciones:
            dientes = [d for d in dientes if d.tiene_condiciones]

        if self.mostrar_solo_criticos:
            dientes = [d for d in dientes if len(d.condiciones_criticas) > 0]

        if self.filtro_tipo_condicion != "todos":
            # Filtrar por tipo de condición específico
            dientes_con_condicion = []
            for diente in dientes:
                for cara in [diente.cara_oclusal, diente.cara_mesial, diente.cara_distal,
                           diente.cara_vestibular, diente.cara_lingual]:
                    if cara.tipo_condicion == self.filtro_tipo_condicion:
                        dientes_con_condicion.append(diente)
                        break
            dientes = dientes_con_condicion

        return dientes

    @rx.var
    def estadisticas_resumen(self) -> Dict[str, Any]:
        """Estadísticas resumen para dashboard"""
        return {
            "total_dientes": len(self._obtener_dientes_seguros()),
            "dientes_sanos": len(self._obtener_dientes_seguros()) - self.total_dientes_afectados,
            "dientes_afectados": self.total_dientes_afectados,
            "condiciones_criticas": self.total_condiciones_criticas,
            "costo_estimado": self.costo_total_estimado,
            "porcentaje_salud": round(
                ((len(self._obtener_dientes_seguros()) - self.total_dientes_afectados) /
                 len(self._obtener_dientes_seguros())) * 100, 1
            ) if self._obtener_dientes_seguros() else 100
        }

    @rx.var
    def condiciones_disponibles_ui(self) -> List[Dict[str, Any]]:
        """Lista de condiciones disponibles para selector"""
        return CONDICIONES_DISPONIBLES

    @rx.var
    def caras_diente_ui(self) -> List[Dict[str, str]]:
        """Lista de caras del diente para UI"""
        return CARAS_DIENTE

    # ===========================================
    # COMPUTED VARS PARA UI
    # ===========================================

    @rx.var
    def dientes_por_cuadrante(self) -> Dict[str, List[DienteInteractivoModel]]:
        """Organizar dientes filtrados por cuadrante FDI"""
        dientes = self.dientes_filtrados

        cuadrantes = {
            "cuadrante_1": [18, 17, 16, 15, 14, 13, 12, 11],  # Superior Derecho
            "cuadrante_2": [21, 22, 23, 24, 25, 26, 27, 28],  # Superior Izquierdo
            "cuadrante_3": [31, 32, 33, 34, 35, 36, 37, 38],  # Inferior Izquierdo
            "cuadrante_4": [48, 47, 46, 45, 44, 43, 42, 41],  # Inferior Derecho
        }

        resultado = {}
        for cuadrante_name, numeros_fdi in cuadrantes.items():
            resultado[cuadrante_name] = [
                diente for diente in dientes
                if diente.numero_fdi in numeros_fdi
            ]

        return resultado

    # ===========================================
    # MÉTODOS DE DEBUGGING Y DESARROLLO
    # ===========================================

    def debug_estado_actual(self) -> Dict[str, Any]:
        """Obtener estado actual para debugging"""
        return {
            "numero_historia": self.numero_historia_actual,
            "diente_seleccionado": self.numero_diente_seleccionado,
            "cara_seleccionada": self.cara_seleccionada,
            "modo_edicion_ui": self.modo_edicion_ui,
            "cambios_pendientes": len(self.cambios_pendientes),
            "total_dientes": len(self._obtener_dientes_seguros()),
            "estadisticas": self.estadisticas_resumen
        }

    def simular_condiciones_test(self):
        """Simular algunas condiciones para testing de UI"""
        if not self._obtener_dientes_seguros():
            return

        # Simular caries en diente 11
        diente_11 = self.odontograma_actual.get_diente_por_fdi(11)
        if diente_11:
            diente_11.actualizar_cara(CaraDiente.OCLUSAL, TipoCondicion.CARIES, SeveridadCondicion.MODERADA)

        # Simular restauración en diente 16
        diente_16 = self.odontograma_actual.get_diente_por_fdi(16)
        if diente_16:
            diente_16.actualizar_cara(CaraDiente.OCLUSAL, TipoCondicion.RESTAURACION, SeveridadCondicion.LEVE)

        # Actualizar estadísticas
        self._actualizar_estadisticas()

        dental_logger.info("Condiciones de test simuladas")