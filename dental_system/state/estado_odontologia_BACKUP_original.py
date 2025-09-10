"""
🦷 ESTADO DE ODONTOLOGÍA - SUBSTATE SEPARADO
=============================================

PROPÓSITO: Manejo centralizado y especializado del módulo odontológico
- Pacientes asignados por orden de llegada
- Formulario completo de intervenciones
- Odontograma FDI visual (32 dientes)
- Historia clínica básica
- Integración con servicios odontológicos

USADO POR: AppState como coordinador principal  
PATRÓN: Substate con get_estado_odontologia() en AppState
"""

import reflex as rx
from datetime import date, datetime
from typing import Dict, Any, List, Optional, Union, Tuple
import logging

# Servicios y modelos
from dental_system.services.odontologia_service import odontologia_service
from dental_system.services.servicios_service import servicios_service
from dental_system.models import (
    PacienteModel,
    ConsultaModel, 
    IntervencionModel,
    ServicioModel,
    OdontogramaModel,
    DienteModel,
    IntervencionFormModel,
    OdontologoStatsModel,
    CondicionDienteModel
)

logger = logging.getLogger(__name__)

class EstadoOdontologia(rx.State,mixin=True):
    """
    🦷 ESTADO ESPECIALIZADO EN MÓDULO ODONTOLÓGICO
    
    RESPONSABILIDADES:
    - Gestión de pacientes asignados por orden de llegada
    - Formulario completo de intervenciones con servicios
    - Odontograma FDI visual de 32 dientes
    - Historia clínica básica del paciente
    - Integración con servicios odontológicos disponibles
    - Gestión de estado de consultas (programada → en_progreso → completada)
    """
    
    # ==========================================
    # 🦷 VARIABLES PRINCIPALES ODONTOLÓGICAS
    # ==========================================
    
    # Pacientes asignados al odontólogo por orden de llegada
    pacientes_asignados: List[PacienteModel] = []
    consultas_asignadas: List[ConsultaModel] = []
    total_pacientes_asignados: int = 0
    
    # Consulta e intervención actual
    consulta_actual: ConsultaModel = ConsultaModel()
    paciente_actual: PacienteModel = PacienteModel()
    intervencion_actual: IntervencionModel = IntervencionModel()
    
    # ==========================================
    # 🔄 PACIENTES DISPONIBLES (DE OTROS ODONTÓLOGOS)
    # ==========================================
    
    # Pacientes que pueden ser atendidos (ya fueron vistos por otro odontólogo)
    pacientes_disponibles_otros: List[PacienteModel] = []
    consultas_disponibles_otros: List[ConsultaModel] = []
    total_pacientes_disponibles: int = 0
    
    # ==========================================
    # 📊 ESTADÍSTICAS DEL DASHBOARD
    # ==========================================
    
    # Estadísticas del día para el odontólogo (modelo tipado)
    estadisticas_dia: OdontologoStatsModel = OdontologoStatsModel()
    
    # ==========================================
    # 📋 HISTORIAL CLÍNICO DEL PACIENTE ACTUAL
    # ==========================================
    
    # Historial médico completo del paciente seleccionado (modelo tipado)
    historial_paciente_actual: List[CondicionDienteModel] = []
    intervenciones_anteriores: List[IntervencionModel] = []
    ultima_consulta_info: Optional[ConsultaModel] = None
    tiene_historial_cargado: bool = False
    
    # ==========================================
    # 🦷 SERVICIOS ODONTOLÓGICOS
    # ==========================================
    
    # Catálogo de servicios disponibles
    servicios_disponibles: List[ServicioModel] = []
    servicios_por_categoria: Dict[str, List[ServicioModel]] = {}
    
    # Servicio seleccionado en intervención
    servicio_seleccionado: ServicioModel = ServicioModel()
    id_servicio_seleccionado: str = ""
    
    # ==========================================
    # 🦷 FORMULARIO DE INTERVENCIÓN
    # ==========================================
    
    # Formulario de intervención (modelo tipado)
    formulario_intervencion: IntervencionFormModel = IntervencionFormModel()
    
    # Validaciones del formulario
    errores_validacion_intervencion: Dict[str, str] = {}
    
    # Variables auxiliares para el formulario
    precio_servicio_base: float = 0.0  # Precio base del servicio seleccionado
    
    # ==========================================
    # 📊 COMPUTED VARS PARA ODONTOGRAMA
    # ==========================================
    
    @rx.var
    def odontogram_stats_summary(self) -> List[Tuple[str, int]]:
        """📊 Estadísticas del odontograma como lista de tuplas (nombre, cantidad)"""
        try:
            total_dientes = 32
            dientes_con_condiciones = len(self.condiciones_odontograma) + len(self.cambios_pendientes_odontograma)
            dientes_sanos = total_dientes - dientes_con_condiciones
            
            # Contar por tipo de condición (simplificado)
            condiciones_caries = 0
            condiciones_obturaciones = 0
            condiciones_otros = dientes_con_condiciones
            
            return [
                ("Sanos", dientes_sanos),
                ("Caries", condiciones_caries), 
                ("Obturaciones", condiciones_obturaciones),
                ("Otros", condiciones_otros)
            ]
        except Exception:
            return [("Sanos", 32), ("Caries", 0), ("Obturaciones", 0), ("Otros", 0)]
    
    # ==========================================
    # 📊 HISTORIAL CLÍNICO
    # ==========================================
    
    # Intervenciones anteriores del paciente
    intervenciones_anteriores: List[IntervencionModel] = []
    
    # Historial de consultas del paciente actual
    historial_paciente_actual: List[ConsultaModel] = []
    
    # ==========================================
    # 🦷 ODONTOGRAMA FDI (32 DIENTES)
    # ==========================================
    
    # Estructura FDI de dientes
    dientes_fdi: List[DienteModel] = []
    odontograma_actual: OdontogramaModel = OdontogramaModel()
    
    # Estado visual del odontograma
    diente_seleccionado: Optional[int] = None
    superficie_seleccionada: str = "oclusal"  # oclusal, mesial, distal, vestibular, lingual
    condiciones_odontograma: Dict[int, Dict[str, str]] = {}  # {diente: {superficie: condicion}}
    cambios_pendientes_odontograma: Dict[int, Dict[str, str]] = {}  # Cambios no guardados
    modo_odontograma: str = "visualizacion"  # visualizacion, edicion
    modal_condicion_abierto: bool = False  # Estado del modal selector de condición
    termino_busqueda_condicion: str = ""  # Búsqueda en modal de condiciones
    categoria_condicion_seleccionada: str = "todas"  # Filtro de categoría de condiciones
    
    # Variables para la selección de condiciones
    selected_condition_to_apply: Optional[str] = None  # Condición seleccionada para aplicar
    current_surface_condition: Optional[str] = None  # Condición actual de la superficie seleccionada
    is_applying_condition: bool = False  # Indica si se está aplicando una condición
    
    # Cuadrantes FDI
    cuadrante_1: List[int] = [11, 12, 13, 14, 15, 16, 17, 18]  # Superior derecho
    cuadrante_2: List[int] = [21, 22, 23, 24, 25, 26, 27, 28]  # Superior izquierdo
    cuadrante_3: List[int] = [31, 32, 33, 34, 35, 36, 37, 38]  # Inferior izquierdo
    cuadrante_4: List[int] = [41, 42, 43, 44, 45, 46, 47, 48]  # Inferior derecho
    
    # ==========================================
    # 🦷 FILTROS Y BÚSQUEDAS
    # ==========================================
    
    # Filtros de pacientes asignados
    filtro_estado_consulta: str = "programada"  # programada, en_progreso, completada
    filtro_fecha_consulta: str = ""  # Fecha específica o hoy
    mostrar_solo_urgencias: bool = False
    
    # Búsqueda de pacientes
    termino_busqueda_pacientes: str = ""
    
    # ==========================================
    # 🦷 ESTADOS DE CARGA Y UI
    # ==========================================
    
    # Estados de carga
    cargando_pacientes_asignados: bool = False
    cargando_servicios: bool = False
    cargando_intervencion: bool = False
    creando_intervencion: bool = False
    
    # Estados de navegación
    en_formulario_intervencion: bool = False
    modo_formulario: str = "crear"  # crear, editar, ver
    
    # ==========================================
    # 💡 COMPUTED VARS OPTIMIZADAS CON CACHE
    # ==========================================
    
    @rx.var(cache=True)
    def pacientes_filtrados(self) -> List[PacienteModel]:
        """
        Lista de pacientes filtrada según criterios actuales
        """
        if not self.pacientes_asignados:
            return []
        
        try:
            resultado = self.pacientes_asignados.copy()
            
            # Filtro por búsqueda
            if self.termino_busqueda_pacientes and len(self.termino_busqueda_pacientes) >= 2:
                termino_lower = self.termino_busqueda_pacientes.lower()
                resultado = [
                    p for p in resultado
                    if (termino_lower in p.nombre_completo.lower() or
                        termino_lower in p.numero_documento.lower() or
                        termino_lower in p.numero_historia.lower())
                ]
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en pacientes_filtrados: {e}")
            return []
    
    @rx.var(cache=True)
    def consultas_por_estado(self) -> Dict[str, List[ConsultaModel]]:
        """Agrupar consultas por estado"""
        try:
            agrupadas = {
                "programada": [],
                "en_progreso": [],
                "completada": []
            }
            
            for consulta in self.consultas_asignadas:
                if consulta.estado in agrupadas:
                    agrupadas[consulta.estado].append(consulta)
            
            return agrupadas
            
        except Exception:
            return {"programada": [], "en_progreso": [], "completada": []}
    
    @rx.var(cache=True)
    def servicios_por_categoria_computed(self) -> Dict[str, List[ServicioModel]]:
        """Servicios agrupados por categoría"""
        try:
            agrupados = {}
            
            for servicio in self.servicios_disponibles:
                categoria = servicio.categoria or "General"
                if categoria not in agrupados:
                    agrupados[categoria] = []
                agrupados[categoria].append(servicio)
            
            return agrupados
            
        except Exception:
            return {}
    
    @rx.var(cache=True)
    def precio_servicio_seleccionado(self) -> str:
        """Precio del servicio seleccionado para mostrar en formulario"""
        try:
            if self.servicio_seleccionado and self.servicio_seleccionado.precio_base:
                return f"${self.servicio_seleccionado.precio_base:,.0f}"
            return "$0"
        except Exception:
            return "$0"
    
    @rx.var(cache=True)
    def turno_actual_paciente(self) -> str:
        """Número de turno del paciente actual"""
        try:
            if self.consulta_actual and self.consulta_actual.orden_llegada:
                return f"Turno #{self.consulta_actual.orden_llegada}"
            return "Sin turno"
        except Exception:
            return "Sin turno"
    
    @rx.var(cache=True)
    def estadisticas_del_dia_computed(self) -> OdontologoStatsModel:
        """Estadísticas computadas del día para el odontólogo"""
        try:
            # Combinar estadísticas del servicio con cálculos locales
            stats_data = {
                "consultas_hoy": len(self.consultas_asignadas),
                "pacientes_asignados": len(self.pacientes_asignados),
                "consultas_pendientes_hoy": len(self.consultas_por_estado.get("programada", [])),
                "intervenciones_mes": len(self.consultas_por_estado.get("completada", [])),
                "tratamientos_pendientes": len(self.consultas_por_estado.get("en_progreso", [])),
            }
            # Usar estadísticas base del servicio si están disponibles
            if hasattr(self.estadisticas_dia, 'ingresos_generados_mes'):
                stats_data.update({
                    "ingresos_generados_mes": self.estadisticas_dia.ingresos_generados_mes,
                    "promedio_tiempo_consulta": self.estadisticas_dia.promedio_tiempo_consulta,
                    "consultas_semana": self.estadisticas_dia.consultas_semana,
                    "consultas_mes": self.estadisticas_dia.consultas_mes
                })
            
            return OdontologoStatsModel.from_dict(stats_data)
        except Exception:
            return OdontologoStatsModel()
    
    @rx.var(cache=True)
    def dientes_afectados_texto(self) -> str:
        """Texto descriptivo de dientes afectados en intervención"""
        try:
            # Obtener dientes desde el formulario tipado
            if isinstance(self.formulario_intervencion.dientes_afectados, str):
                if self.formulario_intervencion.dientes_afectados.strip():
                    dientes = [int(x.strip()) for x in self.formulario_intervencion.dientes_afectados.split(",") if x.strip().isdigit()]
                else:
                    dientes = []
            else:
                dientes = self.formulario_intervencion.dientes_afectados or []
            
            if not dientes:
                return "Ningún diente seleccionado"
            
            if len(dientes) == 1:
                return f"Diente {dientes[0]}"
            elif len(dientes) <= 3:
                return f"Dientes {', '.join(map(str, dientes))}"
            else:
                return f"{len(dientes)} dientes seleccionados"
                
        except Exception:
            return "Error en selección"
    
    # ==========================================
    # 🔄 MÉTODOS DE CARGA DE DATOS
    # ==========================================
    
    async def cargar_pacientes_asignados(self):
        """
        Cargar consultas asignadas al odontólogo por orden de llegada
        """
        # Verificar autenticación
        if not self.esta_autenticado or self.rol_usuario != "odontologo":
            logger.warning(f"Usuario no autorizado para ver pacientes asignados")
            return
        
        self.cargando_pacientes_asignados = True
        
        try:
            # Usar servicio de consultas para obtener consultas completas con modelos
            from dental_system.services.consultas_service import consultas_service
            
            # Establecer contexto
            consultas_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Obtener consultas del día para este odontólogo
            consultas_asignadas = await consultas_service.get_today_consultations(self.id_personal)
            
            # Filtrar solo las que están en espera o en progreso (no completadas)
            self.consultas_asignadas = [
                c for c in consultas_asignadas 
                if c.estado in ["en_espera", "programada", "en_progreso", "en_atencion"]
            ]
            
            # BACKWARD COMPATIBILITY: Mantener pacientes_asignados para otros componentes
            # Extraer solo los pacientes de las consultas
            self.pacientes_asignados = [c.paciente for c in self.consultas_asignadas if c.paciente]
            
            self.total_pacientes_asignados = len(self.consultas_asignadas)
            
            logger.info(f"✅ Consultas asignadas cargadas: {len(self.consultas_asignadas)}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando consultas asignadas: {e}")
            self.handle_error("Error al cargar consultas asignadas", e)
            
        finally:
            self.cargando_pacientes_asignados = False
    
    async def cargar_servicios_disponibles(self):
        """Cargar catálogo de servicios odontológicos"""
        self.cargando_servicios = True
        
        try:
            # Usar servicios_service para obtener catálogo
            servicios_data = await servicios_service.get_filtered_services(activos_only=True)
            self.servicios_disponibles = servicios_data
            
            # Agrupar por categoría
            self.servicios_por_categoria = self.servicios_por_categoria_computed
            
            logger.info(f"✅ Servicios disponibles cargados: {len(servicios_data)}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando servicios: {e}")
            
        finally:
            self.cargando_servicios = False
    
    async def cargar_odontograma_paciente(self, paciente_id: str):
        """Cargar odontograma del paciente actual"""
        try:
            odontograma_data = await odontologia_service.get_odontograma_paciente(paciente_id)
            if odontograma_data:
                self.odontograma_actual = odontograma_data
            else:
                # Crear odontograma vacío si no existe
                self.odontograma_actual = await odontologia_service.create_odontograma_base(paciente_id)
            
            # Cargar estructura FDI
            self.dientes_fdi = await odontologia_service.get_dientes_fdi()
            
            logger.info(f"✅ Odontograma cargado para paciente {paciente_id}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando odontograma: {e}")
    
    async def cargar_consultas_disponibles_otros(self):
        """
        🔄 Cargar consultas disponibles de otros odontólogos
        
        Estas son consultas donde el paciente ya fue atendido por otro odontólogo
        pero puede necesitar una segunda intervención (derivación).
        """
        # Auth variables available via mixin pattern
    
        
        if not self.esta_autenticado or self.rol_usuario != "odontologo":
            logger.warning("Usuario no autorizado para ver consultas disponibles")
            return
        
        try:
            # Establecer contexto en el servicio
            odontologia_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            
            # Obtener consultas disponibles para tomar
            pacientes_disponibles = await odontologia_service.get_pacientes_disponibles(self.id_personal)
            
            self.pacientes_disponibles_otros = pacientes_disponibles
            self.total_pacientes_disponibles = len(pacientes_disponibles)
            
            logger.info(f"✅ Consultas disponibles cargadas: {len(pacientes_disponibles)}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando consultas disponibles: {e}")
    
    async def cargar_estadisticas_dia(self):
        """
        📊 Cargar estadísticas del día para el dashboard del odontólogo
        """
        if not self.esta_autenticado or self.rol_usuario != "odontologo":
            return
        
        try:
            # Obtener estadísticas del servicio
            stats_data = await odontologia_service.get_estadisticas_odontologo(self.id_personal)
            
            # Crear modelo tipado desde los datos
            if stats_data:
                self.estadisticas_dia = OdontologoStatsModel.from_dict(stats_data)
            else:
                self.estadisticas_dia = OdontologoStatsModel()
            
            logger.info(f"✅ Estadísticas del día actualizadas")
            
        except Exception as e:
            logger.error(f"❌ Error cargando estadísticas: {e}")
            # Mantener valores por defecto en caso de error
    
    async def cargar_historial_paciente(self, paciente_id: str):
        """
        📋 Cargar historial clínico completo del paciente actual
        
        Args:
            paciente_id: ID del paciente del cual cargar historial
        """
        if not paciente_id:
            logger.warning("ID de paciente no proporcionado para cargar historial")
            return
        
        self.tiene_historial_cargado = False
        
        try:
            # Obtener historial médico
            historial_data = await odontologia_service.get_historial_paciente_completo(paciente_id)
            
            # Obtener intervenciones anteriores
            intervenciones_data = await odontologia_service.get_intervenciones_anteriores_paciente(paciente_id)
            
            # Obtener información de última consulta
            ultima_consulta_data = await odontologia_service.get_ultima_consulta_paciente(paciente_id)
            
            # Convertir a modelos tipados
            self.historial_paciente_actual = [
                CondicionDienteModel.from_dict(item) for item in (historial_data or [])
                if isinstance(item, dict)
            ]
            self.intervenciones_anteriores = intervenciones_data or []
            self.ultima_consulta_info = ConsultaModel.from_dict(ultima_consulta_data) if ultima_consulta_data else None
            self.tiene_historial_cargado = True
            
            logger.info(f"✅ Historial cargado para paciente {paciente_id}: {len(historial_data)} entradas")
            
        except Exception as e:
            logger.error(f"❌ Error cargando historial del paciente {paciente_id}: {e}")
            self.historial_paciente_actual = []
            self.intervenciones_anteriores = []
            self.ultima_consulta_info = None
    
    async def tomar_paciente_disponible(self, paciente: PacienteModel, consulta_id: str):
        """
        🔄 Tomar un paciente disponible de otro odontólogo para nueva intervención
        
        Args:
            paciente: Modelo del paciente a tomar
            consulta_id: ID de la consulta asociada
        """
        # Auth variables available via mixin pattern
        from dental_system.state.estado_ui import EstadoUI
        ui_state = self.get_state(EstadoUI)
        
        try:
            # Cambiar el estado de la consulta para derivación
            resultado = await odontologia_service.derivar_paciente_a_odontologo(
                consulta_id=consulta_id,
                nuevo_odontologo_id=self.id_personal,
                motivo_derivacion="Requiere intervención adicional"
            )
            
            if resultado:
                # Mover paciente de disponibles a asignados
                self.pacientes_disponibles_otros = [
                    p for p in self.pacientes_disponibles_otros if p.id != paciente.id
                ]
                self.pacientes_asignados.append(paciente)
                
                # Actualizar contadores
                self.total_pacientes_disponibles = len(self.pacientes_disponibles_otros)
                self.total_pacientes_asignados = len(self.pacientes_asignados)
                
                ui_state.mostrar_toast_exito(f"Paciente {paciente.nombre_completo} asignado exitosamente")
                logger.info(f"✅ Paciente {paciente.nombre_completo} tomado de otro odontólogo")
                
                # Recargar datos para mantener sincronización
                await self.cargar_pacientes_asignados()
                await self.cargar_consultas_disponibles_otros()
            
        except Exception as e:
            logger.error(f"❌ Error tomando paciente disponible: {e}")
            ui_state.mostrar_toast_error("Error al tomar paciente")
    
    # ==========================================
    # 🦷 GESTIÓN DE CONSULTAS E INTERVENCIONES
    # ==========================================
    
    async def iniciar_consulta(self, consulta_id: str):
        """
        Iniciar consulta (programada → en_progreso)
        """
        from dental_system.state.estado_ui import EstadoUI
        ui_state = self.get_state(EstadoUI)
        
        try:
            # Cambiar estado de consulta
            consulta_actualizada = await odontologia_service.iniciar_consulta(consulta_id)
            
            # Actualizar en la lista
            for i, consulta in enumerate(self.consultas_asignadas):
                if consulta.id == consulta_id:
                    self.consultas_asignadas[i] = consulta_actualizada
                    break
            
            # Establecer como consulta actual
            self.consulta_actual = consulta_actualizada
            
            ui_state.mostrar_toast_exito("Consulta iniciada")
            logger.info(f"✅ Consulta iniciada: {consulta_id}")
            
        except Exception as e:
            logger.error(f"❌ Error iniciando consulta: {e}")
            ui_state.mostrar_toast_error("Error al iniciar consulta")
    
    async def completar_consulta(self, consulta_id: str):
        """
        Completar consulta (en_progreso → completada)
        """
        from dental_system.state.estado_ui import EstadoUI
        ui_state = self.get_state(EstadoUI)
        
        try:
            consulta_actualizada = await odontologia_service.completar_consulta(consulta_id)
            
            # Actualizar en la lista
            for i, consulta in enumerate(self.consultas_asignadas):
                if consulta.id == consulta_id:
                    self.consultas_asignadas[i] = consulta_actualizada
                    break
            
            ui_state.mostrar_toast_exito("Consulta completada")
            logger.info(f"✅ Consulta completada: {consulta_id}")
            
        except Exception as e:
            logger.error(f"❌ Error completando consulta: {e}")
            ui_state.mostrar_toast_error("Error al completar consulta")
    
    def navegar_a_intervencion(self, paciente: PacienteModel, consulta: ConsultaModel):
        """
        Navegar al formulario de intervención
        """
        from dental_system.state.estado_ui import EstadoUI
        ui_state = self.get_state(EstadoUI)
        
        # Establecer paciente y consulta actual
        self.paciente_actual = paciente
        self.consulta_actual = consulta
        
        # Limpiar formulario
        self.limpiar_formulario_intervencion()
        
        # Cambiar estado UI
        self.en_formulario_intervencion = True
        self.modo_formulario = "crear"
        
        # Cargar odontograma del paciente
        self.cargar_odontograma_paciente(paciente.id)
        
        # Navegar a página de intervención
        ui_state.navegar_a("intervencion")
        
        logger.info(f"✅ Navegando a intervención para paciente: {paciente.nombre_completo}")
    
    # ==========================================
    # 📝 GESTIÓN DEL FORMULARIO DE INTERVENCIÓN
    # ==========================================
    
    async def crear_intervencion(self):
        """
        Crear nueva intervención odontológica
        """
        if not self.validar_formulario_intervencion():
            return
        
        # Auth variables available via mixin pattern
        from dental_system.state.estado_ui import EstadoUI

        ui_state = self.get_state(EstadoUI)
        
        self.creando_intervencion = True
        
        try:
            # Preparar datos para crear intervención usando modelo tipado
            datos_intervencion = self.formulario_intervencion.to_dict()
            datos_intervencion.update({
                "consulta_id": self.consulta_actual.id,
                "paciente_id": self.paciente_actual.id,
                "odontologo_id": self.id_personal
            })
            
            # Crear intervención
            nueva_intervencion = await odontologia_service.create_intervencion(
                form_data=datos_intervencion,
                user_id=self.perfil_usuario.get("id") if self.perfil_usuario else ""
            )
            
            # Limpiar formulario
            self.limpiar_formulario_intervencion()
            
            # Navegar de vuelta
            self.en_formulario_intervencion = False
            ui_state.navegar_a("odontologia")
            
            # Mostrar éxito
            ui_state.mostrar_toast_exito("Intervención creada exitosamente")
            
            # Recargar consultas
            await self.cargar_pacientes_asignados()
            
            logger.info(f"✅ Intervención creada: {nueva_intervencion.id}")
            
        except Exception as e:
            logger.error(f"❌ Error creando intervención: {e}")
            ui_state.mostrar_toast_error("Error al crear intervención")
            
        finally:
            self.creando_intervencion = False
    
    def seleccionar_servicio(self, servicio_id: str):
        """Seleccionar servicio para la intervención"""
        try:
            # Encontrar servicio en la lista
            servicio = next(
                (s for s in self.servicios_disponibles if s.id == servicio_id),
                None
            )
            
            if servicio:
                self.servicio_seleccionado = servicio
                self.id_servicio_seleccionado = servicio_id
                
                # Actualizar formulario tipado
                self.formulario_intervencion.servicio_id = servicio_id
                self.formulario_intervencion.precio_final = str(servicio.precio_base or 0)
                
                logger.info(f"✅ Servicio seleccionado: {servicio.nombre}")
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando servicio: {e}")
    
    def actualizar_campo_intervencion(self, campo: str, valor: Any):
        """Actualizar campo del formulario de intervención"""
        # Usar setattr para modelos tipados en lugar de dict access
        if hasattr(self.formulario_intervencion, campo):
            setattr(self.formulario_intervencion, campo, valor)
        
        # Limpiar error del campo si existe
        if campo in self.errores_validacion_intervencion:
            del self.errores_validacion_intervencion[campo]
    
    def agregar_diente_afectado(self, numero_diente: int):
        """Agregar diente a la lista de afectados"""
        # Convertir string a lista si es necesario
        if isinstance(self.formulario_intervencion.dientes_afectados, str):
            if self.formulario_intervencion.dientes_afectados.strip():
                dientes_actuales = [int(x.strip()) for x in self.formulario_intervencion.dientes_afectados.split(",") if x.strip().isdigit()]
            else:
                dientes_actuales = []
        else:
            dientes_actuales = list(self.formulario_intervencion.dientes_afectados) if self.formulario_intervencion.dientes_afectados else []
        
        if numero_diente not in dientes_actuales:
            dientes_actuales.append(numero_diente)
            self.formulario_intervencion.dientes_afectados = ",".join(map(str, dientes_actuales))
    
    def quitar_diente_afectado(self, numero_diente: int):
        """Quitar diente de la lista de afectados"""
        # Convertir string a lista si es necesario
        if isinstance(self.formulario_intervencion.dientes_afectados, str):
            if self.formulario_intervencion.dientes_afectados.strip():
                dientes_actuales = [int(x.strip()) for x in self.formulario_intervencion.dientes_afectados.split(",") if x.strip().isdigit()]
            else:
                dientes_actuales = []
        else:
            dientes_actuales = list(self.formulario_intervencion.dientes_afectados) if self.formulario_intervencion.dientes_afectados else []
        
        if numero_diente in dientes_actuales:
            dientes_actuales.remove(numero_diente)
            self.formulario_intervencion.dientes_afectados = ",".join(map(str, dientes_actuales))
    
    def limpiar_formulario_intervencion(self):
        """Limpiar todos los datos del formulario"""
        # Usar modelo tipado en lugar de diccionario
        self.formulario_intervencion = IntervencionFormModel(
            anestesia_utilizada="ninguna",
            descuento="0",
            requiere_control=False
        )
        
        self.errores_validacion_intervencion = {}
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
    
    def validar_formulario_intervencion(self) -> bool:
        """Validar formulario de intervención"""
        # Usar el método validate_form del modelo tipado
        errores = self.formulario_intervencion.validate_form()
        
        # Validaciones adicionales
        if self.formulario_intervencion.precio_final:
            try:
                precio = float(self.formulario_intervencion.precio_final)
                if precio <= 0:
                    errores.setdefault("precio_final", []).append("El precio debe ser mayor a 0")
            except ValueError:
                errores.setdefault("precio_final", []).append("Precio inválido")
        
        if self.formulario_intervencion.descuento:
            try:
                descuento = float(self.formulario_intervencion.descuento)
                if descuento < 0 or descuento > 100:
                    errores.setdefault("descuento", []).append("Descuento debe estar entre 0 y 100")
            except ValueError:
                errores.setdefault("descuento", []).append("Descuento inválido")
        
        # Convertir errores a formato plano para compatibilidad
        self.errores_validacion_intervencion = {
            campo: "; ".join(lista_errores) for campo, lista_errores in errores.items()
        }
        
        return len(errores) == 0
    
    # ==========================================
    # 🦷 GESTIÓN DEL ODONTOGRAMA
    # ==========================================
    
    def seleccionar_diente(self, numero_diente: int):
        """Seleccionar diente en el odontograma"""
        self.diente_seleccionado = numero_diente
        
        # Si estamos en modo edición, agregar a dientes afectados
        if self.modo_odontograma == "edicion":
            self.agregar_diente_afectado(numero_diente)
    
    def alternar_modo_odontograma(self):
        """Alternar entre modo visualización y edición"""
        if self.modo_odontograma == "visualizacion":
            self.modo_odontograma = "edicion"
        else:
            self.modo_odontograma = "visualizacion"
            self.diente_seleccionado = None
    
    def obtener_color_diente(self, numero_diente: int) -> str:
        """Obtener color del diente según su estado"""
        try:
            # Obtener dientes afectados desde formulario tipado
            dientes_afectados = []
            if isinstance(self.formulario_intervencion.dientes_afectados, str):
                if self.formulario_intervencion.dientes_afectados.strip():
                    dientes_afectados = [int(x.strip()) for x in self.formulario_intervencion.dientes_afectados.split(",") if x.strip().isdigit()]
            
            # Si está en dientes afectados, resaltar
            if numero_diente in dientes_afectados:
                return "#ff6b6b"  # Rojo para seleccionados
            
            # Color por defecto (sano)
            return "#ffffff"  # Blanco para sanos
            
        except Exception:
            return "#ffffff"
    
    # ==========================================
    # 🔍 MÉTODOS DE FILTROS Y BÚSQUEDA
    # ==========================================
    
    @rx.event
    async def buscar_pacientes_asignados(self, termino: str):
        """Buscar pacientes asignados con throttling"""
        self.termino_busqueda_pacientes = termino.strip()
        # Los resultados se actualizarán automáticamente vía computed var
    
    async def filtrar_por_estado_consulta(self, estado: str):
        """Filtrar consultas por estado"""
        self.filtro_estado_consulta = estado
        await self.cargar_pacientes_asignados()
    
    def alternar_mostrar_urgencias(self):
        """Alternar filtro de urgencias"""
        self.mostrar_solo_urgencias = not self.mostrar_solo_urgencias
    
    # ==========================================
    # 🔧 MÉTODOS DE UTILIDAD
    # ==========================================
    
    def handle_error(self, contexto: str, error: Exception):
        """Manejar errores de manera centralizada"""
        logger.error(f"{contexto}: {str(error)}")
        
        try:
            from dental_system.state.estado_ui import EstadoUI
            ui_state = self.get_state(EstadoUI)
            ui_state.mostrar_toast_error(f"Error: {contexto}")
        except Exception:
            pass
    
    async def refrescar_datos_odontologia(self):
        """Refrescar todos los datos del módulo"""
        await self.cargar_pacientes_asignados()
        await self.cargar_servicios_disponibles()
        logger.info("🔄 Datos de odontología refrescados")
    
    def limpiar_estado_navegacion(self):
        """Limpiar estado de navegación al salir del módulo"""
        self.en_formulario_intervencion = False
        self.paciente_actual = PacienteModel()
        self.consulta_actual = ConsultaModel()
        self.limpiar_formulario_intervencion()
        self.diente_seleccionado = None
        self.modo_odontograma = "visualizacion"
    
    # ==========================================
    # 🦷 COMPUTED VARS ADICIONALES PARA APPSTATE
    # ==========================================
    
    @rx.var(cache=True)
    def pacientes_filtrados_display(self) -> List[PacienteModel]:
        """🔍 Pacientes filtrados según criterios actuales (alias para AppState)"""
        return self.pacientes_filtrados
    
    @rx.var(cache=True)
    def paciente_seleccionado_valido(self) -> bool:
        """✅ Validar si hay paciente actual válido"""
        return (
            hasattr(self.paciente_actual, 'id') and 
            bool(self.paciente_actual.id)
        )
    
    @rx.var(cache=True)
    def consulta_seleccionada_valida(self) -> bool:
        """✅ Validar si hay consulta actual válida"""
        return (
            hasattr(self.consulta_actual, 'id') and 
            bool(self.consulta_actual.id)
        )
    
    @rx.var(cache=True)
    def puede_crear_intervencion(self) -> bool:
        """⚙️ Verificar si se puede crear intervención"""
        return (
            self.paciente_seleccionado_valido and
            self.consulta_seleccionada_valida and
            self.consulta_actual.estado in ["programada", "en_progreso"]
        )
    
    @rx.var(cache=True)
    def formulario_intervencion_valido(self) -> bool:
        """📝 Verificar si formulario de intervención es válido"""
        # Usar validación del modelo tipado
        errores = self.formulario_intervencion.validate_form()
        return len(errores) == 0
    
    @rx.var(cache=True)
    def texto_estado_consulta_actual(self) -> str:
        """📋 Texto descriptivo del estado de la consulta actual"""
        if not self.consulta_actual.estado:
            return "Sin consulta"
        
        estados_texto = {
            "programada": "⏳ En espera",
            "en_progreso": "🔄 En atención", 
            "completada": "✅ Completada"
        }
        return estados_texto.get(self.consulta_actual.estado, "❓ Estado desconocido")
    
    @rx.var(cache=True)
    def resumen_dientes_seleccionados(self) -> str:
        """🦷 Resumen de dientes seleccionados en odontograma"""
        try:
            # Obtener dientes desde el formulario tipado
            if isinstance(self.formulario_intervencion.dientes_afectados, str):
                if self.formulario_intervencion.dientes_afectados.strip():
                    dientes = [int(x.strip()) for x in self.formulario_intervencion.dientes_afectados.split(",") if x.strip().isdigit()]
                else:
                    dientes = []
            else:
                dientes = self.formulario_intervencion.dientes_afectados or []
            
            if not dientes:
                return "Ningún diente seleccionado"
            
            # Ordenar dientes
            dientes_ordenados = sorted(dientes)
            
            if len(dientes_ordenados) == 1:
                return f"Diente {dientes_ordenados[0]}"
            elif len(dientes_ordenados) <= 5:
                return f"Dientes: {', '.join(map(str, dientes_ordenados))}"
            else:
                return f"{len(dientes_ordenados)} dientes seleccionados"
                
        except Exception:
            return "Error en selección"
    
    # ==========================================
    # 🦷 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================
    
    @rx.event
    async def aplicar_filtros_odontologia(self, filtros: Dict[str, Any]):
        """🔍 APLICAR FILTROS DE ODONTOLOGÍA - COORDINACIÓN CON APPSTATE"""
        try:
            # Aplicar filtros individuales
            if "estado_consulta" in filtros:
                self.filtro_estado_consulta = filtros["estado_consulta"]
            
            if "fecha_consulta" in filtros:
                self.filtro_fecha_consulta = filtros["fecha_consulta"]
            
            if "mostrar_solo_urgencias" in filtros:
                self.mostrar_solo_urgencias = filtros["mostrar_solo_urgencias"]
            
            logger.info(f"✅ Filtros de odontología aplicados: {filtros}")
            
            # Recargar datos con nuevos filtros
            await self.cargar_pacientes_asignados()
            
        except Exception as e:
            logger.error(f"❌ Error aplicando filtros odontología: {str(e)}")
    
    @rx.event
    async def seleccionar_paciente_consulta(self, paciente_id: str, consulta_id: str):
        """🎯 SELECCIONAR PACIENTE Y CONSULTA ESPECÍFICA"""
        try:
            # Buscar paciente en la lista
            paciente_encontrado = next(
                (p for p in self.pacientes_asignados if p.id == paciente_id),
                None
            )
            
            # Buscar consulta en la lista
            consulta_encontrada = next(
                (c for c in self.consultas_asignadas if c.id == consulta_id),
                None
            )
            
            if paciente_encontrado and consulta_encontrada:
                self.paciente_actual = paciente_encontrado
                self.consulta_actual = consulta_encontrada
                
                # Cargar odontograma del paciente
                await self.cargar_odontograma_paciente(paciente_id)
                
                logger.info(f"✅ Paciente y consulta seleccionados: {paciente_encontrado.nombre_completo}")
            else:
                logger.warning(f"❌ Paciente o consulta no encontrados: {paciente_id}, {consulta_id}")
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando paciente/consulta: {str(e)}")
    
    @rx.event
    async def actualizar_progreso_intervencion(self, progreso: str):
        """📊 ACTUALIZAR PROGRESO DE INTERVENCIÓN"""
        try:
            # Esto podría actualizarse en una base de datos real
            # Por ahora solo logging
            logger.info(f"📊 Progreso intervención: {progreso}")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando progreso: {str(e)}")
    
    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.pacientes_asignados = []
        self.consultas_asignadas = []
        self.total_pacientes_asignados = 0
        
        self.consulta_actual = ConsultaModel()
        self.paciente_actual = PacienteModel()
        self.intervencion_actual = IntervencionModel()
        
        self.servicios_disponibles = []
        self.servicios_por_categoria = {}
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
        
        self.limpiar_formulario_intervencion()
        
        # Limpiar odontograma
        self.dientes_fdi = []
        self.odontograma_actual = OdontogramaModel()
        self.diente_seleccionado = None
        self.modo_odontograma = "visualizacion"
        
        # Limpiar formulario y estadísticas
        self.formulario_intervencion = IntervencionFormModel()
        self.estadisticas_dia = OdontologoStatsModel()
        
        # Limpiar filtros
        self.filtro_estado_consulta = "programada"
        self.filtro_fecha_consulta = ""
        self.mostrar_solo_urgencias = False
        self.termino_busqueda_pacientes = ""
        
        # Estados de carga
        self.cargando_pacientes_asignados = False
        self.cargando_servicios = False
        self.cargando_intervencion = False
        self.creando_intervencion = False
        
        # Estados de navegación
        self.en_formulario_intervencion = False
        self.modo_formulario = "crear"
        
        logger.info("🧹 Datos de odontología limpiados")
    
    # ==========================================
    # 💡 COMPUTED VARIABLES ADICIONALES OPTIMIZADAS
    # ==========================================
    
    @rx.var(cache=True)
    def pacientes_disponibles_filtrados(self) -> List[PacienteModel]:
        """🔄 Lista filtrada de pacientes disponibles de otros odontólogos"""
        if not self.pacientes_disponibles_otros:
            return []
        
        try:
            resultado = self.pacientes_disponibles_otros.copy()
            
            # Filtro por búsqueda si está activo
            if self.termino_busqueda_pacientes and len(self.termino_busqueda_pacientes) >= 2:
                termino_lower = self.termino_busqueda_pacientes.lower()
                resultado = [
                    p for p in resultado
                    if (termino_lower in p.nombre_completo.lower() or
                        termino_lower in p.numero_documento.lower() or
                        termino_lower in p.numero_historia.lower())
                ]
            
            # Ordenar por prioridad y fecha
            return sorted(resultado, key=lambda p: (
                -1 if hasattr(p, 'prioridad') and p.prioridad == 'urgente' else 0,
                p.nombre_completo
            ))
            
        except Exception as e:
            logger.error(f"Error en pacientes_disponibles_filtrados: {e}")
            return []
    
    @rx.var(cache=True)
    def estadisticas_dashboard_optimizadas(self) -> Dict[str, Any]:
        """📊 Estadísticas optimizadas para dashboard del odontólogo"""
        try:
            base_stats = {
                "pacientes_asignados": len(self.pacientes_asignados),
                "pacientes_disponibles": len(self.pacientes_disponibles_otros),
                "consultas_programadas": len(self.consultas_por_estado.get("programada", [])),
                "consultas_en_progreso": len(self.consultas_por_estado.get("en_progreso", [])),
                "consultas_completadas": len(self.consultas_por_estado.get("completada", [])),
            }
            
            # Combinar con estadísticas del servicio si están disponibles
            base_stats.update(self.estadisticas_dia)
            
            return base_stats
            
        except Exception as e:
            logger.error(f"Error en estadisticas_dashboard_optimizadas: {e}")
            return {
                "pacientes_asignados": 0,
                "pacientes_disponibles": 0,
                "consultas_programadas": 0,
                "consultas_en_progreso": 0,
                "consultas_completadas": 0,
            }
    
    @rx.var(cache=True)
    def tiene_pacientes_para_atender(self) -> bool:
        """⚡ Verificar si hay pacientes listos para atención"""
        return (
            len(self.pacientes_asignados) > 0 or 
            len(self.pacientes_disponibles_otros) > 0
        )
    
    @rx.var(cache=True)
    def proxima_consulta_info(self) -> Dict[str, str]:
        """📅 Información de la próxima consulta en orden"""
        try:
            consultas_programadas = self.consultas_por_estado.get("programada", [])
            
            if not consultas_programadas:
                return {
                    "tiene_proxima": "false",
                    "paciente": "No hay consultas programadas",
                    "tiempo_estimado": "N/A"
                }
            
            # Obtener la primera consulta (orden de llegada)
            proxima_consulta = consultas_programadas[0]
            paciente = next(
                (p for p in self.pacientes_asignados if p.id == proxima_consulta.paciente_id),
                None
            )
            
            return {
                "tiene_proxima": "true",
                "paciente": paciente.nombre_completo if paciente else "Paciente no encontrado",
                "tiempo_estimado": "15-30 min",
                "prioridad": getattr(proxima_consulta, 'prioridad', 'normal')
            }
            
        except Exception as e:
            logger.error(f"Error en proxima_consulta_info: {e}")
            return {
                "tiene_proxima": "false",
                "paciente": "Error",
                "tiempo_estimado": "N/A"
            }
    
    @rx.var(cache=True)
    def resumen_actividad_dia(self) -> str:
        """📋 Resumen textual de la actividad del día"""
        try:
            total_consultas = len(self.consultas_asignadas)
            completadas = len(self.consultas_por_estado.get("completada", []))
            en_progreso = len(self.consultas_por_estado.get("en_progreso", []))
            programadas = len(self.consultas_por_estado.get("programada", []))
            
            if total_consultas == 0:
                return "Sin consultas asignadas hoy"
            
            if completadas == total_consultas:
                return f"Día completado: {completadas} consultas finalizadas"
            
            resumen_parts = []
            if programadas > 0:
                resumen_parts.append(f"{programadas} en espera")
            if en_progreso > 0:
                resumen_parts.append(f"{en_progreso} en atención")
            if completadas > 0:
                resumen_parts.append(f"{completadas} completadas")
                
            return f"Actividad: {', '.join(resumen_parts)}"
            
        except Exception as e:
            logger.error(f"Error en resumen_actividad_dia: {e}")
            return "Error calculando actividad"
    
    @rx.var(cache=True)
    def alerta_pacientes_urgentes(self) -> Dict[str, Any]:
        """🚨 Verificar si hay pacientes urgentes que requieren atención inmediata"""
        try:
            urgentes_asignados = [
                p for p in self.pacientes_asignados 
                if hasattr(p, 'prioridad') and p.prioridad in ['urgente', 'alta']
            ]
            
            urgentes_disponibles = [
                p for p in self.pacientes_disponibles_otros
                if hasattr(p, 'prioridad') and p.prioridad in ['urgente', 'alta']
            ]
            
            total_urgentes = len(urgentes_asignados) + len(urgentes_disponibles)
            
            return {
                "tiene_urgentes": total_urgentes > 0,
                "cantidad": total_urgentes,
                "mensaje": f"{total_urgentes} paciente{'s' if total_urgentes != 1 else ''} urgente{'s' if total_urgentes != 1 else ''}" if total_urgentes > 0 else "No hay pacientes urgentes"
            }
            
        except Exception as e:
            logger.error(f"Error en alerta_pacientes_urgentes: {e}")
            return {
                "tiene_urgentes": False,
                "cantidad": 0,
                "mensaje": "Error verificando urgencias"
            }
    
    @rx.var(cache=True)
    def puede_tomar_mas_pacientes(self) -> bool:
        """⚡ Verificar si el odontólogo puede tomar más pacientes"""
        return (
            len(self.consultas_por_estado.get("en_progreso", [])) < 3 and  # Máximo 3 en progreso
            len(self.pacientes_disponibles_otros) > 0
        )
    
    @rx.var(cache=True)
    def historial_paciente_resumen(self) -> Dict[str, Any]:
        """📋 Resumen del historial del paciente actual"""
        try:
            if not self.tiene_historial_cargado or not self.historial_paciente_actual:
                return {
                    "tiene_historial": False,
                    "total_entradas": 0,
                    "ultima_consulta": "Sin historial",
                    "intervenciones_previas": 0
                }
            
            return {
                "tiene_historial": True,
                "total_entradas": len(self.historial_paciente_actual),
                "ultima_consulta": self.ultima_consulta_info.fecha_programada if self.ultima_consulta_info else "Sin consultas previas",
                "intervenciones_previas": len(self.intervenciones_anteriores),
                "ultima_intervencion": self.intervenciones_anteriores[0].procedimiento_realizado if self.intervenciones_anteriores else "Sin intervenciones previas"
            }
            
        except Exception as e:
            logger.error(f"Error en historial_paciente_resumen: {e}")
            return {
                "tiene_historial": False,
                "total_entradas": 0,
                "ultima_consulta": "Error",
                "intervenciones_previas": 0
            }

    # ==========================================
    # 🦷 MÉTODOS DE ODONTOGRAMA
    # ==========================================

    async def seleccionar_diente_superficie(self, numero_diente: int, nombre_superficie: str):
        """
        🦷 Seleccionar un diente y su superficie en el odontograma
        
        Args:
            numero_diente: Número FDI del diente (11-48)
            nombre_superficie: Nombre de la superficie (oclusal, mesial, distal, vestibular, lingual)
        """
        try:
            # Validar número de diente FDI
            if numero_diente not in (self.cuadrante_1 + self.cuadrante_2 + self.cuadrante_3 + self.cuadrante_4):
                logger.warning(f"Número de diente inválido: {numero_diente}")
                return
                
            # Validar superficie
            superficies_validas = ["oclusal", "mesial", "distal", "vestibular", "lingual"]
            if nombre_superficie not in superficies_validas:
                logger.warning(f"Superficie inválida: {nombre_superficie}")
                return
                
            # Actualizar selección
            self.diente_seleccionado = numero_diente
            self.superficie_seleccionada = nombre_superficie
            
            logger.info(f"✅ Seleccionado diente {numero_diente}, superficie {nombre_superficie}")
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando diente/superficie: {e}")

    async def seleccionar_diente(self, numero_diente: int):
        """
        🦷 Seleccionar solo un diente en el odontograma (sin superficie específica)
        
        Args:
            numero_diente: Número FDI del diente (11-48)
        """
        try:
            # Validar número de diente FDI
            if numero_diente not in (self.cuadrante_1 + self.cuadrante_2 + self.cuadrante_3 + self.cuadrante_4):
                logger.warning(f"Número de diente inválido: {numero_diente}")
                return
                
            # Actualizar selección (mantener superficie actual)
            self.diente_seleccionado = numero_diente
            
            logger.info(f"✅ Seleccionado diente {numero_diente}")
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando diente: {e}")

    async def abrir_modal_condicion(self):
        """🔧 Abrir modal selector de condición dental"""
        self.modal_condicion_abierto = True

    async def cerrar_modal_condicion(self):
        """🔧 Cerrar modal selector de condición dental"""
        self.modal_condicion_abierto = False

    async def establecer_condicion_diente(self, numero_diente: int, superficie: str, condicion: str):
        """🦷 Establecer condición de una superficie del diente"""
        try:
            if numero_diente not in self.cambios_pendientes_odontograma:
                self.cambios_pendientes_odontograma[numero_diente] = {}
            
            self.cambios_pendientes_odontograma[numero_diente][superficie] = condicion
            logger.info(f"✅ Condición establecida: Diente {numero_diente}, {superficie} = {condicion}")
            
        except Exception as e:
            logger.error(f"❌ Error estableciendo condición: {e}")

    async def actualizar_busqueda_condicion(self, termino: str):
        """🔍 Actualizar término de búsqueda de condiciones"""
        self.termino_busqueda_condicion = termino

    async def cambiar_categoria_condicion(self, categoria: str):
        """📂 Cambiar filtro de categoría de condiciones"""
        self.categoria_condicion_seleccionada = categoria

    async def seleccionar_condicion_aplicar(self, condicion: str):
        """🦷 Seleccionar condición que se va a aplicar"""
        self.selected_condition_to_apply = condicion
        
    async def actualizar_condicion_superficie_actual(self):
        """🔄 Actualizar condición actual de la superficie seleccionada"""
        if self.diente_seleccionado and self.superficie_seleccionada:
            # Obtener condición de cambios pendientes o actual
            if self.diente_seleccionado in self.cambios_pendientes_odontograma:
                condicion_pendiente = self.cambios_pendientes_odontograma[self.diente_seleccionado].get(self.superficie_seleccionada)
                if condicion_pendiente:
                    self.current_surface_condition = condicion_pendiente
                    return
            
            # Si no hay cambios pendientes, obtener de condiciones actuales
            if self.diente_seleccionado in self.condiciones_odontograma:
                condicion_actual = self.condiciones_odontograma[self.diente_seleccionado].get(self.superficie_seleccionada)
                self.current_surface_condition = condicion_actual if condicion_actual else "sano"
            else:
                self.current_surface_condition = "sano"
        else:
            self.current_surface_condition = None

    async def apply_selected_condition(self):
        """🦷 Aplicar la condición seleccionada al diente y superficie actual"""
        try:
            if not (self.selected_condition_to_apply and self.diente_seleccionado and self.superficie_seleccionada):
                return
                
            self.is_applying_condition = True
            
            # Aplicar la condición a los cambios pendientes
            await self.establecer_condicion_diente(
                self.diente_seleccionado, 
                self.superficie_seleccionada, 
                self.selected_condition_to_apply
            )
            
            # Actualizar la condición actual
            await self.actualizar_condicion_superficie_actual()
            
            # Limpiar selección
            self.selected_condition_to_apply = None
            self.modal_condicion_abierto = False
            
            logger.info(f"✅ Condición aplicada exitosamente: {self.selected_condition_to_apply}")
            
        except Exception as e:
            logger.error(f"❌ Error aplicando condición: {e}")
        finally:
            self.is_applying_condition = False

    async def restaurar_precio_base(self):
        """💰 Restaurar precio base del servicio al formulario"""
        try:
            if self.servicio_seleccionado and self.servicio_seleccionado.precio_base:
                precio_base = self.servicio_seleccionado.precio_base
                self.formulario_intervencion.precio_final = str(precio_base)
                logger.info(f"✅ Precio restaurado a base: ${precio_base}")
        except Exception as e:
            logger.error(f"❌ Error restaurando precio base: {e}")

