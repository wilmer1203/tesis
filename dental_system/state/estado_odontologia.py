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
from typing import Dict, Any, List, Optional, Union
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
    DienteModel
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
    
    # Datos del formulario de intervención
    formulario_intervencion: Dict[str, Any] = {
        "servicio_id": "",
        "procedimiento_realizado": "",
        "materiales_utilizados": "",
        "anestesia_utilizada": "ninguna",  # ninguna, local, regional, general
        "duracion_minutos": "",
        "precio_final": "",
        "descuento": "0",
        "instrucciones_paciente": "",
        "requiere_control": "false",
        "fecha_control_sugerida": "",
        "dientes_afectados": [],  # Array de números de dientes
        "complicaciones": "",
        "observaciones": ""
    }
    
    # Validaciones del formulario
    errores_validacion_intervencion: Dict[str, str] = {}
    
    # ==========================================
    # 🦷 ODONTOGRAMA FDI (32 DIENTES)
    # ==========================================
    
    # Estructura FDI de dientes
    dientes_fdi: List[DienteModel] = []
    odontograma_actual: OdontogramaModel = OdontogramaModel()
    
    # Estado visual del odontograma
    diente_seleccionado: Optional[int] = None
    modo_odontograma: str = "visualizacion"  # visualizacion, edicion
    
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
    def estadisticas_del_dia(self) -> Dict[str, int]:
        """Estadísticas del día para el odontólogo"""
        try:
            return {
                "total_consultas": len(self.consultas_asignadas),
                "programadas": len(self.consultas_por_estado.get("programada", [])),
                "en_progreso": len(self.consultas_por_estado.get("en_progreso", [])),
                "completadas": len(self.consultas_por_estado.get("completada", []))
            }
        except Exception:
            return {"total_consultas": 0, "programadas": 0, "en_progreso": 0, "completadas": 0}
    
    @rx.var(cache=True)
    def dientes_afectados_texto(self) -> str:
        """Texto descriptivo de dientes afectados en intervención"""
        try:
            dientes = self.formulario_intervencion.get("dientes_afectados", [])
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
        Cargar pacientes asignados al odontólogo por orden de llegada
        """
        from dental_system.state.estado_auth import EstadoAuth
        
        auth_state = self.get_state(EstadoAuth)
        
        if not auth_state.is_authenticated or auth_state.user_role != "odontologo":
            logger.warning("Usuario no autorizado para ver pacientes asignados")
            return
        
        self.cargando_pacientes_asignados = True
        
        try:
            # Establecer contexto en el servicio
            odontologia_service.set_user_context(
                user_id=auth_state.user_profile.get("id"),
                role=auth_state.user_role,
                personal_id=auth_state.personal_id
            )
            
            # Obtener pacientes asignados por orden de llegada
            pacientes_data = await odontologia_service.get_pacientes_asignados_por_orden()
            consultas_data = await odontologia_service.get_consultas_asignadas()
            
            self.pacientes_asignados = pacientes_data
            self.consultas_asignadas = consultas_data
            self.total_pacientes_asignados = len(pacientes_data)
            
            logger.info(f"✅ Pacientes asignados cargados: {len(pacientes_data)}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando pacientes asignados: {e}")
            self.handle_error("Error al cargar pacientes asignados", e)
            
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
        
        from dental_system.state.estado_auth import EstadoAuth
        from dental_system.state.estado_ui import EstadoUI
        
        auth_state = self.get_state(EstadoAuth)
        ui_state = self.get_state(EstadoUI)
        
        self.creando_intervencion = True
        
        try:
            # Preparar datos para crear intervención
            datos_intervencion = {
                **self.formulario_intervencion,
                "consulta_id": self.consulta_actual.id,
                "paciente_id": self.paciente_actual.id,
                "odontologo_id": auth_state.personal_id
            }
            
            # Crear intervención
            nueva_intervencion = await odontologia_service.create_intervencion(
                form_data=datos_intervencion,
                user_id=auth_state.user_profile.get("id")
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
                
                # Actualizar formulario
                self.formulario_intervencion["servicio_id"] = servicio_id
                self.formulario_intervencion["precio_final"] = str(servicio.precio_base or 0)
                
                logger.info(f"✅ Servicio seleccionado: {servicio.nombre}")
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando servicio: {e}")
    
    def actualizar_campo_intervencion(self, campo: str, valor: Any):
        """Actualizar campo del formulario de intervención"""
        self.formulario_intervencion[campo] = valor
        
        # Limpiar error del campo si existe
        if campo in self.errores_validacion_intervencion:
            del self.errores_validacion_intervencion[campo]
    
    def agregar_diente_afectado(self, numero_diente: int):
        """Agregar diente a la lista de afectados"""
        dientes_actuales = self.formulario_intervencion.get("dientes_afectados", [])
        if numero_diente not in dientes_actuales:
            dientes_actuales.append(numero_diente)
            self.formulario_intervencion["dientes_afectados"] = dientes_actuales
    
    def quitar_diente_afectado(self, numero_diente: int):
        """Quitar diente de la lista de afectados"""
        dientes_actuales = self.formulario_intervencion.get("dientes_afectados", [])
        if numero_diente in dientes_actuales:
            dientes_actuales.remove(numero_diente)
            self.formulario_intervencion["dientes_afectados"] = dientes_actuales
    
    def limpiar_formulario_intervencion(self):
        """Limpiar todos los datos del formulario"""
        self.formulario_intervencion = {
            "servicio_id": "",
            "procedimiento_realizado": "",
            "materiales_utilizados": "",
            "anestesia_utilizada": "ninguna",
            "duracion_minutos": "",
            "precio_final": "",
            "descuento": "0",
            "instrucciones_paciente": "",
            "requiere_control": "false",
            "fecha_control_sugerida": "",
            "dientes_afectados": [],
            "complicaciones": "",
            "observaciones": ""
        }
        
        self.errores_validacion_intervencion = {}
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
    
    def validar_formulario_intervencion(self) -> bool:
        """Validar formulario de intervención"""
        self.errores_validacion_intervencion = {}
        
        # Campos requeridos
        campos_requeridos = [
            "servicio_id", "procedimiento_realizado", "precio_final"
        ]
        
        for campo in campos_requeridos:
            valor = self.formulario_intervencion.get(campo, "")
            if not str(valor).strip():
                self.errores_validacion_intervencion[campo] = "Este campo es requerido"
        
        # Validar precio
        try:
            precio = float(self.formulario_intervencion.get("precio_final", "0"))
            if precio <= 0:
                self.errores_validacion_intervencion["precio_final"] = "El precio debe ser mayor a 0"
        except ValueError:
            self.errores_validacion_intervencion["precio_final"] = "Precio inválido"
        
        # Validar descuento
        try:
            descuento = float(self.formulario_intervencion.get("descuento", "0"))
            if descuento < 0 or descuento > 100:
                self.errores_validacion_intervencion["descuento"] = "Descuento debe estar entre 0 y 100"
        except ValueError:
            self.errores_validacion_intervencion["descuento"] = "Descuento inválido"
        
        return len(self.errores_validacion_intervencion) == 0
    
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
            # Si está en dientes afectados, resaltar
            if numero_diente in self.formulario_intervencion.get("dientes_afectados", []):
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
        campos_requeridos = ["servicio_id", "procedimiento_realizado", "precio_final"]
        for campo in campos_requeridos:
            if not str(self.formulario_intervencion.get(campo, "")).strip():
                return False
        return True
    
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
            dientes = self.formulario_intervencion.get("dientes_afectados", [])
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

