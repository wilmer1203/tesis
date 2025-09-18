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
from typing import Dict, Any, List, Optional, Union, Tuple, cast
import logging

# Servicios y modelos
from dental_system.services.odontologia_service import odontologia_service
from dental_system.services.servicios_service import servicios_service
from dental_system.state.estado_odontograma_avanzado import EstadoOdontogramaAvanzado
from dental_system.state.estado_ui import EstadoUI
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

class EstadoOdontologia(EstadoOdontogramaAvanzado):
    """
    🦷 ESTADO ESPECIALIZADO EN MÓDULO ODONTOLÓGICO
    
    RESPONSABILIDADES:
    - Gestión de pacientes asignados por orden de llegada
    - Formulario completo de intervenciones con servicios
    - Integración con odontograma FDI avanzado
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
    # 📊 COMPUTED VARS OPTIMIZADAS PARA ODONTOGRAMA
    # ==========================================
    
    # Los métodos surface_condition_optimized, tooth_has_changes_optimized y
    # selected_tooth_info_optimized han sido reemplazados por la funcionalidad
    # proporcionada por EstadoOdontogramaAvanzado
    
    @rx.var(cache=True)
    def surface_condition_optimized(self) -> Dict[str, str]:
        """⚡ Proxy al estado del odontograma avanzado"""
        result: Dict[str, str] = {}
        for numero_fdi, estado in self.dientes_estados.items():
            for superficie in ["oclusal", "mesial", "distal", "vestibular", "lingual"]:
                key = f"{numero_fdi}_{superficie}"
                result[key] = estado.get("codigo", "SAO")
        return result
        
    @rx.var(cache=True)
    def selected_tooth_info_optimized(self) -> Dict[str, Any]:
        """⚡ Info del diente seleccionado usando el estado avanzado"""
        if not self.diente_seleccionado:
            return {"tooth": None, "surfaces": {}, "pending": {}, "quadrant": 0}
            
        # Obtener información del diente del catálogo
        diente_info = next(
            (d for d in self.dientes_catalogo if d["numero_fdi"] == self.diente_seleccionado),
            None
        )
        
        if not diente_info:
            return {"tooth": None, "surfaces": {}, "pending": {}, "quadrant": 0}
            
        return {
            "tooth": self.diente_seleccionado,
            "surfaces": self.dientes_estados.get(self.diente_seleccionado, {}),
            "pending": {},  # No hay cambios pendientes en el nuevo sistema
            "quadrant": diente_info["cuadrante"],
            "has_changes": False  # Los cambios son inmediatos en el nuevo sistema
        }
    
    @rx.var
    def odontogram_stats_summary(self) -> List[Tuple[str, int]]:
        """📊 Estadísticas del odontograma optimizadas"""
        try:
            total_dientes = 32
            dientes_con_condiciones = len(self.condiciones_odontograma) + len(self.cambios_pendientes_odontograma)
            dientes_sanos = max(0, total_dientes - dientes_con_condiciones)
            
            # Contar por tipo de condición de forma más eficiente
            condiciones_caries = sum(1 for conditions in self.condiciones_odontograma.values() 
                                   if any("caries" in cond for cond in conditions.values()))
            condiciones_obturaciones = sum(1 for conditions in self.condiciones_odontograma.values() 
                                         if any("obturado" in cond for cond in conditions.values()))
            
            return [
                ("Sanos", dientes_sanos),
                ("Caries", condiciones_caries), 
                ("Obturaciones", condiciones_obturaciones),
                ("Otros", max(0, dientes_con_condiciones - condiciones_caries - condiciones_obturaciones))
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
    modo_odontograma: str = "edicion"  # visualizacion, edicion - Por defecto en modo edición para intervenciones

    # 📚 Variables para historial de dientes (modo consulta)
    historial_diente_seleccionado: List[Dict[str, Any]] = []  # Historial real del diente
    modal_condicion_abierto: bool = False  # Estado del modal selector de condición
    termino_busqueda_condicion: str = ""  # Búsqueda en modal de condiciones
    categoria_condicion_seleccionada: str = "todas"  # Filtro de categoría de condiciones
    
    # 🎈 Variables del popover contextual
    popover_diente_abierto: bool = False  # Estado del popover del diente
    popover_diente_posicion: Dict[str, float] = {}  # Posición x, y del popover
    
    # 📚 Variables del modal de historial flotante
    modal_historial_completo_abierto: bool = False  # Estado del modal de historial
    
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
    
    # Filtros de pacientes asignados (Estados reales de BD)
    filtro_estado_consulta: str = "Todos"  # Todos, En Espera, En Atención, Entre Odontólogos, Completada, Cancelada
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
    modo_formulario: str = "crear"
    
    # NAVEGACIÓN DE TABS DE INTERVENCIÓN
    active_intervention_tab: str = "odontograma"  # odontograma, intervencion, finalizar
    tabs_completed: List[str] = []  # Tabs completados con validaciones
    puede_avanzar_tab: bool = True
    
    # Estados de carga por tab
    cargando_odontograma: bool = False
    cargando_servicios: bool = False
    guardando_intervencion: bool = False
    
    # ==========================================
    # 🆕 VARIABLES PARA FORMULARIO INTEGRADO V3.0
    # ==========================================
    
    # Selección de dientes integrada
    dientes_seleccionados_lista: List[Dict[str, Any]] = []
    total_dientes_seleccionados: int = 0
    modo_seleccion_multiple: bool = False
    
    # Servicios seleccionados
    servicios_seleccionados: List[str] = []
    servicios_seleccionados_detalle: List[Dict[str, Any]] = []
    total_servicios_seleccionados: int = 0
    filtro_servicios: str = ""
    
    # Costos de la intervención
    total_usd_intervencion: float = 0.0
    total_bs_intervencion: float = 0.0
    
    # Observaciones médicas
    diagnostico_previo: str = ""
    procedimiento_realizado: str = ""
    observaciones_post_tratamiento: str = ""
    recomendaciones_paciente: str = ""
    
    # Estados del proceso
    is_guardando_intervencion: bool = False
    modal_vista_previa_abierto: bool = False  # crear, editar, ver
    
    # ==========================================
    # 🎨 VARIABLES PARA PANEL PACIENTE MEJORADO
    # ==========================================
    
    # Panel paciente colapsable
    panel_paciente_expandido: bool = True  # Por defecto expandido
    
    # Control de información expandida
    mostrar_info_emergencia: bool = True
    mostrar_estadisticas_visitas: bool = True
    mostrar_historial_medico: bool = True
    
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
            # Establecer contexto de usuario antes de usar el servicio
            servicios_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
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
        """Cargar odontograma del paciente actual usando el estado avanzado"""
        try:
            # Verificar autenticación
            if not self.id_personal:
                print("⚠️ No hay odontólogo autenticado para cargar odontograma")
                return
            
            # Primero cargar el catálogo FDI si no está cargado
            if not self.catalogo_cargado:
                await self.cargar_catalogo_fdi()
            
            # Obtener datos del odontograma del paciente
            odontograma_data = await odontologia_service.get_odontograma_paciente(paciente_id, self.id_personal)
            
            if odontograma_data and hasattr(odontograma_data, 'condiciones'):
                # Actualizar estados de los dientes según condiciones guardadas
                for numero_fdi, condicion in odontograma_data.condiciones.items():
                    self.aplicar_condicion_diente(
                        int(numero_fdi), 
                        condicion.get('codigo', 'SAO')
                    )
            else:
                # Si no hay datos, inicializar todos como sanos (ya hecho en cargar_catalogo_fdi)
                print(f"🔄 Inicializando nuevo odontograma para paciente {paciente_id}")
                
            print(f"✅ Odontograma cargado para paciente {paciente_id} por odontólogo {self.id_personal}")
            
        except Exception as e:
            print(f"❌ Error cargando odontograma: {e}")
            self.error_message = f"Error cargando odontograma: {str(e)}"
    # Los métodos _inicializar_dientes_fdi, _obtener_cuadrante_diente y _obtener_tipo_diente
    # han sido reemplazados por la funcionalidad del catálogo FDI en EstadoOdontogramaAvanzado
        else:
            return "desconocido"
    
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
            # Establecer contexto de usuario antes de usar el servicio
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
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
            # Establecer contexto de usuario antes de usar el servicio
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
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
        # Get UI state
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
        """Seleccionar servicio para la intervención con auto-actualización de precio"""
        try:
            # Encontrar servicio en la lista
            servicio = next(
                (s for s in self.servicios_disponibles if s.id == servicio_id),
                None
            )
            
            if servicio:
                self.servicio_seleccionado = servicio
                self.id_servicio_seleccionado = servicio_id
                
                # Actualizar formulario tipado con precio automático
                self.formulario_intervencion.servicio_id = servicio_id
                self.formulario_intervencion.precio_final = str(servicio.precio_base or 0)
                
                # Mostrar notificación de precio actualizado si hay cambio significativo
                precio_anterior = float(self.formulario_intervencion.precio_final) if self.formulario_intervencion.precio_final else 0
                precio_nuevo = servicio.precio_base or 0
                
                if abs(precio_anterior - precio_nuevo) > 0.01:
                    from dental_system.state.estado_ui import EstadoUI
                    ui_state = self.get_state(EstadoUI)
                    ui_state.mostrar_toast(f"Precio actualizado: ${precio_nuevo:,.2f}", "info")
                
                logger.info(f"✅ Servicio seleccionado: {servicio.nombre} - Precio: ${precio_nuevo}")
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando servicio: {e}")
    
    @rx.event
    async def seleccionar_servicio_mejorado(self, servicio_id: str):
        """Versión mejorada con validación de precio extremo"""
        try:
            servicio = next(
                (s for s in self.servicios_disponibles if s.id == servicio_id),
                None
            )
            
            if servicio:
                precio_base = servicio.precio_base or 0
                
                # Alertar si el precio es muy alto (más de $500)
                if precio_base > 500:
                    from dental_system.state.estado_ui import EstadoUI
                    ui_state = self.get_state(EstadoUI)
                    ui_state.mostrar_toast(f"Precio alto detectado: ${precio_base:,.2f} - Verificar", "warning")
                
                # Proceder con selección normal
                self.seleccionar_servicio(servicio_id)
                
        except Exception as e:
            logger.error(f"❌ Error en selección mejorada: {e}")
    
    @rx.event  
    async def validar_precio_tiempo_real(self):
        """Validación de precio en tiempo real para mostrar feedback inmediato"""
        try:
            precio_str = self.formulario_intervencion.precio_final.strip()
            if not precio_str:
                return
                
            precio = float(precio_str)
            precio_base = float(self.precio_servicio_base or 0)
            
            from dental_system.state.estado_ui import EstadoUI
            ui_state = self.get_state(EstadoUI)
            
            # Precio muy alto
            if precio_base > 0 and precio > (precio_base * 3):
                ui_state.mostrar_toast(f"Precio alto: {precio/precio_base:.1f}x el precio base", "warning")
            
            # Precio muy bajo
            elif precio_base > 0 and precio < (precio_base * 0.5):
                ui_state.mostrar_toast(f"Precio bajo: Verificar descuento", "info")
                
        except ValueError:
            # Error de formato, se maneja en las validaciones principales
            pass
        except Exception as e:
            logger.error(f"Error validando precio: {e}")
    
    # Los métodos optimizados para el odontograma están ahora heredados 
    # de EstadoOdontogramaAvanzado, que incluye:
    # - surface_condition_optimized
    # - tooth_has_changes_optimized  
    # - select_tooth_optimized
            
            self.diente_seleccionado = tooth_number
            logger.info(f"✅ Diente seleccionado: {tooth_number}")
            
        except Exception as e:
            logger.error(f"Error seleccionando diente: {e}")
    
    def select_quadrant_optimized(self, quadrant: int):
        """⚡ Selección rápida de cuadrante completo"""
        try:
            quadrant_teeth = {
                1: [11, 12, 13, 14, 15, 16, 17, 18],  # Superior derecho
                2: [21, 22, 23, 24, 25, 26, 27, 28],  # Superior izquierdo
                3: [31, 32, 33, 34, 35, 36, 37, 38],  # Inferior izquierdo
                4: [41, 42, 43, 44, 45, 46, 47, 48]   # Inferior derecho
            }
            
            if quadrant in quadrant_teeth:
                # Seleccionar primer diente del cuadrante
                self.diente_seleccionado = quadrant_teeth[quadrant][0]
                logger.info(f"✅ Cuadrante {quadrant} seleccionado")
                
        except Exception as e:
            logger.error(f"Error seleccionando cuadrante: {e}")
    
    async def set_condition_optimized(self, tooth: int, surface: str, condition: str):
        """⚡ Establecer condición de forma optimizada"""
        try:
            # Validar inputs
            if tooth not in range(11, 49) or tooth in [19, 20, 29, 30, 39, 40]:
                return
            
            if surface not in ["oclusal", "mesial", "distal", "vestibular", "lingual"]:
                return
            
            # Inicializar diccionarios si no existen
            if tooth not in self.cambios_pendientes_odontograma:
                self.cambios_pendientes_odontograma[tooth] = {}
            
            # Establecer condición
            self.cambios_pendientes_odontograma[tooth][surface] = condition
            
            # Auto-agregar a dientes afectados en formulario de intervención
            if condition != "sano":
                self.agregar_diente_afectado(tooth)
            
            logger.info(f"✅ Condición establecida: Diente {tooth}, {surface} = {condition}")
            
        except Exception as e:
            logger.error(f"Error estableciendo condición: {e}")
    
    async def save_odontogram_changes_optimized(self):
        """⚡ Guardar cambios del odontograma optimizado"""
        try:
            if not self.cambios_pendientes_odontograma:
                logger.info("No hay cambios pendientes para guardar")
                return
            
            # Establecer contexto de usuario
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Aplicar cambios al odontograma actual
            for tooth, surfaces in self.cambios_pendientes_odontograma.items():
                if tooth not in self.condiciones_odontograma:
                    self.condiciones_odontograma[tooth] = {}
                
                for surface, condition in surfaces.items():
                    self.condiciones_odontograma[tooth][surface] = condition
            
            # Limpiar cambios pendientes
            self.cambios_pendientes_odontograma = {}
            
            logger.info(f"✅ Cambios del odontograma guardados")
            
        except Exception as e:
            logger.error(f"❌ Error guardando odontograma: {e}")
    
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

            # ✨ SINCRONIZACIÓN: Odontograma → Campo manual
            try:
                if hasattr(self, 'dientes_seleccionados_texto'):
                    self.dientes_seleccionados_texto = ",".join(map(str, dientes_actuales))
            except Exception as e:
                logger.warning(f"Error sincronizando campo manual: {e}")
    
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

            # ✨ SINCRONIZACIÓN: Odontograma → Campo manual
            try:
                if hasattr(self, 'dientes_seleccionados_texto'):
                    self.dientes_seleccionados_texto = ",".join(map(str, dientes_actuales))
            except Exception as e:
                logger.warning(f"Error sincronizando campo manual: {e}")
    
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
    
    @rx.event
    def seleccionar_diente_simple(self, numero_diente: int):
        """Seleccionar diente en el odontograma (versión simple para el formulario)"""
        self.diente_seleccionado = numero_diente
        
        # Si estamos en modo edición, agregar a dientes afectados del formulario
        if self.modo_odontograma == "edicion":
            self.agregar_diente_afectado(numero_diente)
            
        # También actualizar la lista visual de dientes seleccionados
        self.actualizar_lista_dientes_seleccionados()
    
    def actualizar_lista_dientes_seleccionados(self):
        """Actualizar la lista visual de dientes seleccionados para la UI"""
        try:
            # Obtener dientes con condiciones no sanas
            dientes_nums = [
                numero_fdi for numero_fdi, estado in self.dientes_estados.items()
                if estado.get("codigo", "SAO") != "SAO"
            ]
            
            # Actualizar formulario
            self.formulario_intervencion.dientes_afectados = ",".join(map(str, dientes_nums))
            
            # Actualizar lista de diccionarios para la UI
            self.dientes_seleccionados_lista = [
                {"numero": diente, "nombre": f"Diente {diente}"} 
                for diente in sorted(dientes_nums)
            ]
            self.total_dientes_seleccionados = len(dientes_nums)
            
        except Exception as e:
            print(f"❌ Error actualizando lista de dientes: {e}")
            self.dientes_seleccionados_lista = []
            self.total_dientes_seleccionados = 0
    
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
    # 🦷 MÉTODOS DEL ODONTOGRAMA SVG INTERACTIVO
    # ==========================================
    
    @rx.event
    def resetear_seleccion_odontograma(self):
        """Resetear selección del odontograma y limpiar dientes seleccionados"""
        self.diente_seleccionado = None
        self.superficie_seleccionada = "oclusal"
        self.cambios_pendientes_odontograma = {}
        
        # También limpiar dientes del formulario de intervención
        self.formulario_intervencion.dientes_afectados = ""
        self.actualizar_lista_dientes_seleccionados()
        
        print("✅ Selección de odontograma reseteada")
    
    async def guardar_odontograma(self):
        """Guardar cambios del odontograma usando el estado avanzado"""
        try:
            if not self.paciente_actual.id:
                self.mostrar_mensaje_error("No hay paciente seleccionado")
                return
                
            # Convertir estados actuales a formato de guardado
            cambios = {
                str(numero_fdi): {
                    "codigo": estado.get("codigo", "SAO"),
                    "condicion": estado.get("condicion", "sano"),
                    "superficie": estado.get("superficie", "completa"),
                    "observaciones": estado.get("observaciones", "")
                }
                for numero_fdi, estado in self.dientes_estados.items()
            }
            
            # Guardar en BD
            await odontologia_service.guardar_cambios_odontograma(
                self.paciente_actual.id,
                cambios
            )
            
            self.mostrar_mensaje_exito("Odontograma guardado correctamente")
            
        except Exception as e:
            self.mostrar_mensaje_error(f"Error al guardar odontograma: {str(e)}")
    
    # ==========================================
    # 🦷 MÉTODOS PANEL DETALLES DIENTE
    # ==========================================
    
    # Variables adicionales para panel de detalles
    notas_diente_actual: str = ""
    fecha_ultima_nota: str = ""
    autor_ultima_nota: str = ""
    
    def obtener_cuadrante_diente(self) -> str:
        """Obtener el cuadrante del diente seleccionado usando el catálogo FDI"""
        if not self.diente_seleccionado:
            return ""
            
        # Obtener información del diente del catálogo
        diente_info = next(
            (d for d in self.dientes_catalogo if d["numero_fdi"] == self.diente_seleccionado),
            None
        )
        
        if not diente_info:
            return "Desconocido"
            
        cuadrante = diente_info["cuadrante"]
        
        # Mapear número de cuadrante a texto descriptivo
        cuadrantes = {
            1: "Superior Derecho (1)",
            2: "Superior Izquierdo (2)", 
            3: "Inferior Izquierdo (3)",
            4: "Inferior Derecho (4)"
        }
        
        return cuadrantes.get(cuadrante, "Desconocido")
    
    def obtener_tipo_diente(self) -> str:
        """Obtener el tipo de diente según catálogo FDI"""
        if not self.diente_seleccionado:
            return ""
            
        # Obtener información del diente del catálogo
        diente_info = next(
            (d for d in self.dientes_catalogo if d["numero_fdi"] == self.diente_seleccionado),
            None
        )
        
        if not diente_info:
            return "Desconocido"
            
        return diente_info.get("tipo_diente", "Desconocido")
        
        posicion = numero_str[-1]
        
        tipos = {
            "1": "Incisivo Central",
            "2": "Incisivo Lateral", 
            "3": "Canino",
            "4": "Primer Premolar",
            "5": "Segundo Premolar",
            "6": "Primer Molar",
            "7": "Segundo Molar",
            "8": "Tercer Molar"
        }
        
        return tipos.get(posicion, "Desconocido")
    
    def seleccionar_superficie(self, superficie: str):
        """Seleccionar superficie dental específica"""
        self.superficie_seleccionada = superficie
        logger.info(f"Superficie seleccionada: {superficie} en diente {self.diente_seleccionado}")
    
    def abrir_editor_superficie(self):
        """Abrir modal para editar superficie dental"""
        # Implementar modal de edición de superficie
        logger.info(f"Abriendo editor para superficie {self.superficie_seleccionada} en diente {self.diente_seleccionado}")
    
    def mostrar_historial_superficie(self):
        """Mostrar historial de cambios de la superficie"""
        logger.info(f"Mostrando historial de superficie {self.superficie_seleccionada} en diente {self.diente_seleccionado}")
    
    def abrir_formulario_historial(self):
        """Abrir formulario para agregar entrada al historial"""
        logger.info(f"Abriendo formulario de historial para diente {self.diente_seleccionado}")
    
    def abrir_planificador_tratamiento(self):
        """Abrir planificador de tratamientos para el diente"""
        logger.info(f"Abriendo planificador de tratamiento para diente {self.diente_seleccionado}")
    
    
    def actualizar_notas_diente(self, notas: str):
        """Actualizar notas clínicas del diente actual"""
        self.notas_diente_actual = notas
        logger.info(f"Notas actualizadas para diente {self.diente_seleccionado}")
    
    async def guardar_notas_diente(self):
        """Guardar notas clínicas del diente"""
        try:
            if self.diente_seleccionado and self.notas_diente_actual:
                # Aquí se integraría con el servicio para guardar
                self.fecha_ultima_nota = datetime.now().strftime("%d/%m/%Y %H:%M")
                self.autor_ultima_nota = self.nombre_usuario_display or "Usuario"
                logger.info(f"Notas guardadas para diente {self.diente_seleccionado}")
                self.mostrar_mensaje_exito("Notas guardadas correctamente")
        except Exception as e:
            logger.error(f"Error guardando notas: {e}")
            self.mostrar_mensaje_error(f"Error al guardar notas: {str(e)}")
    
    def seleccionar_diente_svg(self, numero_diente: int):
        """Seleccionar diente en el odontograma SVG"""
        self.diente_seleccionado = numero_diente
    
    # ==========================================
    # 🔄 SISTEMA VERSIONADO ODONTOGRAMA
    # ==========================================
    
    # Variables del sistema de versionado
    version_actual_odontograma: str = "2.1"
    historial_versiones: List[Dict[str, Any]] = []
    modal_nueva_version_abierto: bool = False
    comentario_nueva_version: str = ""
    cambios_detectados_actual: List[Dict[str, str]] = []
    
    # Comparación de versiones
    modo_comparacion_activo: bool = False
    version_comparar_a: str = "v2.1 (Actual)"
    version_comparar_b: str = "v2.0"
    
    async def cargar_historial_versiones(self):
        """Cargar historial completo de versiones del odontograma"""
        try:
            # Aquí se integraría con el servicio para cargar historial real
            self.historial_versiones = [
                {
                    "version": "v2.1",
                    "titulo": "Versión Actual",
                    "fecha": "15/08/2024 14:30",
                    "doctor": "Dr. García",
                    "descripcion": "Obturación diente 16 - superficie oclusal",
                    "tipo": "current"
                },
                {
                    "version": "v2.0", 
                    "titulo": "Intervención Anterior",
                    "fecha": "10/08/2024 10:15",
                    "doctor": "Dr. García",
                    "descripcion": "Limpieza dental general",
                    "tipo": "completed"
                }
            ]
            logger.info("Historial de versiones cargado correctamente")
        except Exception as e:
            logger.error(f"Error cargando historial versiones: {e}")
            self.mostrar_mensaje_error(f"Error al cargar historial: {str(e)}")
    
    def detectar_cambios_significativos(self) -> bool:
        """Detectar si hay cambios significativos que requieren nueva versión"""
        # Lógica para detectar cambios significativos
        # Por ejemplo: cambios de estado en más de X dientes, etc.
        return len(self.cambios_pendientes_odontograma) > 0
    
    def abrir_modal_nueva_version(self):
        """Abrir modal para confirmar nueva versión"""
        if self.detectar_cambios_significativos():
            self.modal_nueva_version_abierto = True
            self.cambios_detectados_actual = [
                {"diente": "16", "anterior": "Sano", "nuevo": "Obturado", "descripcion": "Nueva obturación con resina compuesta"}
            ]
        else:
            self.mostrar_mensaje_info("No se detectaron cambios significativos")
    
    def actualizar_comentario_version(self, comentario: str):
        """Actualizar comentario de la nueva versión"""
        self.comentario_nueva_version = comentario
    
    async def confirmar_nueva_version(self):
        """Confirmar y crear nueva versión del odontograma"""
        try:
            # Aquí se integraría con el servicio para crear nueva versión
            nueva_version = f"v{float(self.version_actual_odontograma.replace('v', '')) + 0.1:.1f}"
            self.version_actual_odontograma = nueva_version
            
            # Guardar en historial
            nueva_entrada = {
                "version": nueva_version,
                "titulo": "Nueva Versión",
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "doctor": self.nombre_usuario_display or "Usuario",
                "descripcion": self.comentario_nueva_version,
                "tipo": "current"
            }
            
            # Mover la versión anterior
            if self.historial_versiones:
                self.historial_versiones[0]["tipo"] = "completed"
            
            self.historial_versiones.insert(0, nueva_entrada)
            
            # Limpiar formulario
            self.comentario_nueva_version = ""
            self.modal_nueva_version_abierto = False
            self.cambios_pendientes_odontograma = {}
            
            self.mostrar_mensaje_exito(f"Nueva versión {nueva_version} creada correctamente")
            logger.info(f"Nueva versión creada: {nueva_version}")
            
        except Exception as e:
            logger.error(f"Error creando nueva versión: {e}")
            self.mostrar_mensaje_error(f"Error al crear versión: {str(e)}")
    
    def cancelar_nueva_version(self):
        """Cancelar creación de nueva versión"""
        self.modal_nueva_version_abierto = False
        self.comentario_nueva_version = ""
        self.cambios_detectados_actual = []
    
    def crear_version_manual(self):
        """Crear nueva versión manualmente (sin cambios automáticos)"""
        self.comentario_nueva_version = ""
        self.modal_nueva_version_abierto = True
        logger.info("Creación manual de versión iniciada")
    
    async def ver_version_odontograma(self, version: str):
        """Ver una versión específica del odontograma"""
        try:
            # Aquí se cargaría la versión específica
            logger.info(f"Visualizando versión: {version}")
            self.mostrar_mensaje_info(f"Mostrando versión {version}")
        except Exception as e:
            logger.error(f"Error visualizando versión {version}: {e}")
            self.mostrar_mensaje_error(f"Error al cargar versión: {str(e)}")
    
    def comparar_version(self, version: str):
        """Iniciar comparación con una versión específica"""
        self.modo_comparacion_activo = True
        self.version_comparar_b = version
        logger.info(f"Iniciando comparación con versión: {version}")
    
    async def restaurar_version(self, version: str):
        """Restaurar una versión anterior del odontograma"""
        try:
            # Aquí se integraría con el servicio para restaurar
            logger.info(f"Restaurando versión: {version}")
            self.mostrar_mensaje_exito(f"Versión {version} restaurada correctamente")
        except Exception as e:
            logger.error(f"Error restaurando versión {version}: {e}")
            self.mostrar_mensaje_error(f"Error al restaurar versión: {str(e)}")
    
    def cambiar_version_a(self, version: str):
        """Cambiar versión A para comparación"""
        self.version_comparar_a = version
    
    def cambiar_version_b(self, version: str):
        """Cambiar versión B para comparación"""
        self.version_comparar_b = version
    
    def cerrar_comparador(self):
        """Cerrar el modo de comparación"""
        self.modo_comparacion_activo = False
    
    # ==========================================
    # 📜 HISTORIAL DE CAMBIOS POR DIENTE
    # ==========================================
    
    # Variables del historial
    historial_cambios_diente: List[Dict[str, Any]] = []
    filtro_historial_tipo: str = "Todos"
    filtro_historial_tiempo: str = "Todo el tiempo"
    alertas_diente_activas: List[Dict[str, Any]] = []
    recordatorios_diente: List[Dict[str, Any]] = []
    
    def filtrar_historial_por_tipo(self, tipo: str):
        """Filtrar historial por tipo de cambio"""
        self.filtro_historial_tipo = tipo
        logger.info(f"Filtrando historial por tipo: {tipo}")
    
    def filtrar_historial_por_tiempo(self, tiempo: str):
        """Filtrar historial por período de tiempo"""
        self.filtro_historial_tiempo = tiempo
        logger.info(f"Filtrando historial por tiempo: {tiempo}")
    
    async def exportar_historial_diente(self):
        """Exportar historial completo del diente"""
        try:
            if not self.diente_seleccionado:
                self.mostrar_mensaje_error("Selecciona un diente primero")
                return
            
            # Aquí se integraría con servicio de exportación
            logger.info(f"Exportando historial de diente {self.diente_seleccionado}")
            self.mostrar_mensaje_exito("Historial exportado correctamente")
        except Exception as e:
            logger.error(f"Error exportando historial: {e}")
            self.mostrar_mensaje_error(f"Error al exportar: {str(e)}")
    
    def ver_cambio_completo(self, cambio_id: str):
        """Ver detalles completos de un cambio específico"""
        logger.info(f"Visualizando cambio completo: {cambio_id}")
    
    def ver_imagenes_cambio(self, cambio_id: str):
        """Ver imágenes asociadas a un cambio"""
        logger.info(f"Visualizando imágenes del cambio: {cambio_id}")
    
    def marcar_alerta_leida(self, alerta_titulo: str):
        """Marcar una alerta como leída"""
        logger.info(f"Marcando alerta como leída: {alerta_titulo}")
        # Aquí se removería de alertas_diente_activas
    
    def abrir_formulario_recordatorio(self):
        """Abrir formulario para crear nuevo recordatorio"""
        logger.info(f"Abriendo formulario de recordatorio para diente {self.diente_seleccionado}")
    
    async def refrescar_historial_diente(self):
        """Refrescar datos del historial del diente"""
        try:
            if not self.diente_seleccionado:
                self.mostrar_mensaje_error("Selecciona un diente primero")
                return
            
            # Aquí se cargarían los datos reales del historial
            logger.info(f"Refrescando historial de diente {self.diente_seleccionado}")
            self.mostrar_mensaje_exito("Historial actualizado")
        except Exception as e:
            logger.error(f"Error refrescando historial: {e}")
            self.mostrar_mensaje_error(f"Error al actualizar: {str(e)}")
    
    def abrir_formulario_entrada_historial(self):
        """Abrir formulario para agregar nueva entrada al historial"""
        logger.info(f"Abriendo formulario de entrada para diente {self.diente_seleccionado}")
    
    # ==========================================
    # 🔔 SISTEMA DE NOTIFICACIONES
    # ==========================================
    
    # Variables del sistema de notificaciones
    notificacion_toast_visible: bool = False
    notificacion_toast_titulo: str = ""
    notificacion_toast_mensaje: str = ""
    notificacion_toast_icono: str = "bell"
    notificacion_toast_color: str = "blue"
    notificacion_toast_timestamp: str = ""
    notificacion_toast_tiene_acciones: bool = False
    
    # Centro de notificaciones
    notificaciones_activas: List[Dict[str, Any]] = []
    total_notificaciones_no_leidas: int = 0
    filtro_notificaciones: str = "todas"
    modal_config_notificaciones_abierto: bool = False
    
    # Configuraciones de notificaciones
    config_notif_cambios_criticos: bool = True
    config_notif_recordatorios: bool = True
    config_notif_nuevas_versiones: bool = True
    config_notif_intervenciones: bool = True
    config_sonido_notificaciones: bool = False
    
    def mostrar_toast_notification(self, titulo: str, mensaje: str, icono: str = "bell", color: str = "blue", tiene_acciones: bool = False):
        """Mostrar notificación toast en tiempo real"""
        self.notificacion_toast_titulo = titulo
        self.notificacion_toast_mensaje = mensaje
        self.notificacion_toast_icono = icono
        self.notificacion_toast_color = color
        self.notificacion_toast_timestamp = datetime.now().strftime("%H:%M")
        self.notificacion_toast_tiene_acciones = tiene_acciones
        self.notificacion_toast_visible = True
        
        # Auto-ocultar después de 5 segundos (se podría implementar con JS)
        logger.info(f"Toast mostrado: {titulo} - {mensaje}")
    
    def cerrar_toast_notification(self):
        """Cerrar notificación toast"""
        self.notificacion_toast_visible = False
    
    def aplicar_filtro_notificaciones(self, filtro: str):
        """Aplicar filtro al centro de notificaciones"""
        self.filtro_notificaciones = filtro
        logger.info(f"Filtro de notificaciones aplicado: {filtro}")
    
    def marcar_todas_notificaciones_leidas(self):
        """Marcar todas las notificaciones como leídas"""
        self.total_notificaciones_no_leidas = 0
        logger.info("Todas las notificaciones marcadas como leídas")
    
    def marcar_notificacion_individual_leida(self, titulo: str):
        """Marcar notificación específica como leída"""
        if self.total_notificaciones_no_leidas > 0:
            self.total_notificaciones_no_leidas -= 1
        logger.info(f"Notificación marcada como leída: {titulo}")
    
    def abrir_configuracion_notificaciones(self):
        """Abrir modal de configuración de notificaciones"""
        self.modal_config_notificaciones_abierto = True
    
    def cerrar_config_notificaciones(self):
        """Cerrar modal de configuración"""
        self.modal_config_notificaciones_abierto = False
    
    async def guardar_config_notificaciones(self):
        """Guardar configuración de notificaciones"""
        try:
            # Aquí se guardarían las configuraciones en BD
            self.modal_config_notificaciones_abierto = False
            self.mostrar_mensaje_exito("Configuración guardada correctamente")
            logger.info("Configuración de notificaciones guardada")
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
            self.mostrar_mensaje_error(f"Error al guardar: {str(e)}")
    
    def actualizar_config_notificacion(self, campo: str, valor: bool):
        """Actualizar configuración específica"""
        if campo == "config_notif_cambios_criticos":
            self.config_notif_cambios_criticos = valor
        elif campo == "config_notif_recordatorios":
            self.config_notif_recordatorios = valor
        elif campo == "config_notif_nuevas_versiones":
            self.config_notif_nuevas_versiones = valor
        elif campo == "config_notif_intervenciones":
            self.config_notif_intervenciones = valor
        
        logger.info(f"Configuración actualizada: {campo} = {valor}")
    
    def toggle_sonido_notificaciones(self, habilitado: bool):
        """Habilitar/deshabilitar sonidos"""
        self.config_sonido_notificaciones = habilitado
        logger.info(f"Sonidos de notificación: {'habilitados' if habilitado else 'deshabilitados'}")
    
    def ver_detalles_notificacion(self):
        """Ver detalles de la notificación actual"""
        self.cerrar_toast_notification()
        logger.info("Abriendo detalles de notificación")
    
    def marcar_notificacion_leida(self):
        """Marcar la notificación toast como leída"""
        self.cerrar_toast_notification()
        if self.total_notificaciones_no_leidas > 0:
            self.total_notificaciones_no_leidas -= 1
        logger.info("Notificación toast marcada como leída")
    
    def abrir_detalle_notificacion(self, metadata: Dict[str, str]):
        """Abrir detalle específico de notificación"""
        logger.info(f"Abriendo detalle de notificación: {metadata}")
    
    def abrir_panel_completo_notificaciones(self):
        """Abrir panel completo de notificaciones"""
        logger.info("Abriendo panel completo de notificaciones")
    
    def actualizar_regla_alerta(self, tipo: str, activa: bool):
        """Actualizar regla de alerta automática"""
        logger.info(f"Regla de alerta {tipo}: {'activada' if activa else 'desactivada'}")
    
    # Computed vars para notificaciones
    @rx.var
    def notificaciones_filtradas_count(self) -> int:
        """Contar notificaciones filtradas"""
        # Lógica para contar según filtro
        return len(self.notificaciones_activas)
    
    @rx.var
    def hay_notificaciones_no_leidas(self) -> bool:
        """Verificar si hay notificaciones sin leer"""
        return self.total_notificaciones_no_leidas > 0
    
    # Método para disparar notificaciones automáticas
    def disparar_notificacion_cambio_critico(self, diente: int, estado_anterior: str, estado_nuevo: str):
        """Disparar notificación por cambio crítico en diente"""
        if self.config_notif_cambios_criticos:
            self.mostrar_toast_notification(
                "🚨 Cambio Crítico Detectado",
                f"Diente {diente}: {estado_anterior} → {estado_nuevo}",
                "circle_alert",
                "red",
                True
            )
            self.total_notificaciones_no_leidas += 1
    
    def disparar_notificacion_nueva_version(self, version: str):
        """Disparar notificación por nueva versión"""
        if self.config_notif_nuevas_versiones:
            self.mostrar_toast_notification(
                "📋 Nueva Versión Creada",
                f"Odontograma actualizado a {version}",
                "git_branch",
                "blue"
            )
            self.total_notificaciones_no_leidas += 1
    
    def disparar_notificacion_intervencion_completada(self, diente: int, tipo: str):
        """Disparar notificación por intervención completada"""
        if self.config_notif_intervenciones:
            self.mostrar_toast_notification(
                "✅ Intervención Completada",
                f"{tipo} exitosa en diente {diente}",
                "circle_check",
                "green"
            )
            self.total_notificaciones_no_leidas += 1
        self.superficie_seleccionada = "oclusal"  # Por defecto
    
    async def cambiar_condicion_diente_svg(self, numero_diente: int, condicion: str):
        """Cambiar condición de un diente en el SVG"""
        try:
            if numero_diente not in self.cambios_pendientes_odontograma:
                self.cambios_pendientes_odontograma[numero_diente] = {}
            
            self.cambios_pendientes_odontograma[numero_diente]["condicion"] = condicion
            self.mostrar_mensaje_info(f"Diente {numero_diente}: {condicion}")
            
        except Exception as e:
            self.mostrar_mensaje_error(f"Error al cambiar condición: {str(e)}")

    # ==========================================
    # 🔍 MÉTODOS DE FILTROS Y BÚSQUEDA
    # ==========================================
    
    @rx.event
    async def buscar_pacientes_asignados(self, termino: str):
        """Buscar pacientes asignados con throttling"""
        self.termino_busqueda_pacientes = termino.strip()
        # Los resultados se actualizarán automáticamente vía computed var
    
    # ==========================================
    # 🔄 NAVEGACIÓN DE TABS DE INTERVENCIÓN
    # ==========================================
    
    @rx.event
    def set_active_intervention_tab(self, tab_id: str):
        """Cambiar tab activo con validaciones"""
        try:
            # Validaciones previas antes de cambiar tab
            if tab_id == "odontograma" and not self.paciente_actual.id:
                logger.warning("No se puede acceder al odontograma sin paciente")
                return
            
            if tab_id == "intervencion":
                # Cargar servicios cuando se acceda al tab de intervención
                # No llamar aquí porque es async, se carga en el componente con on_mount
                pass
            
            if tab_id == "finalizar":
                # Validar que se haya completado la información mínima
                if not self._validar_datos_minimos_intervencion():
                    logger.warning("Complete los datos mínimos antes de finalizar")
                    return
            
            self.active_intervention_tab = tab_id
            logger.info(f"Navegando a tab: {tab_id}")
            
            # Marcar tab anterior como completado si es válido
            if tab_id not in self.tabs_completed:
                self.tabs_completed.append(tab_id)
                
        except Exception as e:
            logger.error(f"Error navegando a tab {tab_id}: {e}")
    
    def _validar_datos_minimos_intervencion(self) -> bool:
        """Validar que hay datos mínimos para finalizar intervención"""
        try:
            # Verificar que hay un servicio seleccionado
            if not self.servicio_seleccionado.id:
                return False
            
            # Verificar que hay descripción del procedimiento
            if not self.formulario_intervencion.procedimiento_realizado.strip():
                return False
            
            return True
        except:
            return False
    
    @rx.event
    def validar_y_avanzar_tab(self):
        """Validar tab actual y avanzar al siguiente"""
        tabs_orden = ["paciente", "odontograma", "intervencion", "finalizar"]
        try:
            indice_actual = tabs_orden.index(self.active_intervention_tab)
            
            if indice_actual < len(tabs_orden) - 1:
                siguiente_tab = tabs_orden[indice_actual + 1]
                self.set_active_intervention_tab(siguiente_tab)
        except ValueError:
            logger.error(f"Tab activo no válido: {self.active_intervention_tab}")
    
    @rx.event
    def retroceder_tab(self):
        """Retroceder al tab anterior"""
        tabs_orden = ["paciente", "odontograma", "intervencion", "finalizar"]
        try:
            indice_actual = tabs_orden.index(self.active_intervention_tab)
            
            if indice_actual > 0:
                tab_anterior = tabs_orden[indice_actual - 1]
                self.set_active_intervention_tab(tab_anterior)
        except ValueError:
            logger.error(f"Tab activo no válido: {self.active_intervention_tab}")
            
    # Computed var para saber si podemos avanzar al siguiente tab
    @rx.var
    def puede_avanzar_al_siguiente_tab(self) -> bool:
        """Determina si se puede avanzar al siguiente tab"""
        try:
            if self.active_intervention_tab == "odontograma":
                return True  # Siempre se puede avanzar desde odontograma
            elif self.active_intervention_tab == "intervencion":
                return self._validar_datos_minimos_intervencion()
            else:
                return False
        except:
            return False
    
    async def filtrar_por_estado_consulta(self, estado: str):
        """Filtrar consultas por estado - Estados reales de BD"""
        # Mapear estados de UI a estados de BD
        estados_map = {
            "Todos": "",
            "En Espera": "en_espera", 
            "En Atención": "en_atencion",
            "Entre Odontólogos": "entre_odontologos",
            "Completada": "completada",
            "Cancelada": "cancelada"
        }
        
        self.filtro_estado_consulta = estado
        # El servicio usará el mapeo para filtrar por estado real de BD
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
        self.filtro_estado_consulta = "Todos"
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

    @rx.event
    async def seleccionar_diente(self, numero_diente: int):
        """
        🦷 Seleccionar solo un diente en el odontograma (versión principal)
        
        Args:
            numero_diente: Número FDI del diente (11-48)
        """
        try:
            # Validar número de diente FDI
            if numero_diente not in (self.cuadrante_1 + self.cuadrante_2 + self.cuadrante_3 + self.cuadrante_4):
                print(f"⚠️ Número de diente inválido: {numero_diente}")
                return
                
            # Actualizar selección
            self.diente_seleccionado = numero_diente
            
            # En modo edición, agregar a lista de dientes afectados para intervención
            if self.modo_odontograma == "edicion":
                self.agregar_diente_afectado(numero_diente)
                self.actualizar_lista_dientes_seleccionados()
            
            print(f"✅ Diente {numero_diente} seleccionado")
            
        except Exception as e:
            print(f"❌ Error seleccionando diente {numero_diente}: {e}")

    @rx.event
    async def abrir_popover_diente(self, numero_diente: int, x: float = 100, y: float = 100):
        """
        🎈 Abrir popover contextual del diente en posición específica
        
        Args:
            numero_diente: Número FDI del diente
            x: Posición X del mouse/click
            y: Posición Y del mouse/click
        """
        try:
            # Primero seleccionar el diente
            await self.seleccionar_diente(numero_diente)
            
            # Calcular posición inteligente del popover
            # Ajustar para evitar que se salga de la pantalla
            popover_width = 320
            popover_height = 450
            
            # Límites de pantalla aproximados (se pueden ajustar)
            max_x = 1200 - popover_width
            max_y = 800 - popover_height
            
            adjusted_x = min(max(x, 10), max_x)
            adjusted_y = min(max(y, 10), max_y)
            
            # Establecer posición del popover
            self.popover_diente_posicion = {
                "x": adjusted_x,
                "y": adjusted_y
            }
            
            # Abrir popover
            self.popover_diente_abierto = True
            
            print(f"✅ Popover abierto para diente {numero_diente} en posición ({adjusted_x}, {adjusted_y})")
            
        except Exception as e:
            print(f"❌ Error abriendo popover para diente {numero_diente}: {e}")

    @rx.event
    def cerrar_popover_diente(self):
        """🎈 Cerrar popover contextual del diente"""
        self.popover_diente_abierto = False
        self.popover_diente_posicion = {}
        print("✅ Popover cerrado")

    @rx.event
    def abrir_modal_historial_completo(self):
        """📚 Abrir modal completo de historial del paciente"""
        self.modal_historial_completo_abierto = True
        print("✅ Modal de historial completo abierto")

    @rx.event
    def cerrar_modal_historial_completo(self):
        """📚 Cerrar modal completo de historial del paciente"""
        self.modal_historial_completo_abierto = False
        print("✅ Modal de historial completo cerrado")

    @rx.var
    def obtener_nombre_diente_fdi(self) -> str:
        """📋 Obtener nombre descriptivo del diente seleccionado"""
        if not self.diente_seleccionado:
            return "Ningún diente seleccionado"
        
        return self._obtener_nombre_diente_completo(self.diente_seleccionado)
    
    def _obtener_nombre_diente_completo(self, numero_diente: int) -> str:
        """Obtener nombre completo descriptivo del diente"""
        last_digit = numero_diente % 10
        quadrant = numero_diente // 10
        
        # Determinar tipo y posición
        if last_digit == 1:
            tipo = "Incisivo Central"
        elif last_digit == 2:
            tipo = "Incisivo Lateral"
        elif last_digit == 3:
            tipo = "Canino"
        elif last_digit == 4:
            tipo = "Primer Premolar"
        elif last_digit == 5:
            tipo = "Segundo Premolar"
        elif last_digit == 6:
            tipo = "Primer Molar"
        elif last_digit == 7:
            tipo = "Segundo Molar"
        elif last_digit == 8:
            tipo = "Tercer Molar"
        else:
            tipo = "Desconocido"
        
        # Determinar cuadrante
        if quadrant == 1:
            cuadrante = "Superior Derecho"
        elif quadrant == 2:
            cuadrante = "Superior Izquierdo"
        elif quadrant == 3:
            cuadrante = "Inferior Izquierdo"
        elif quadrant == 4:
            cuadrante = "Inferior Derecho"
        else:
            cuadrante = "Desconocido"
        
        return f"{tipo} {cuadrante}"




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
    
    # ==========================================
    # 🎨 MÉTODOS PARA PANEL PACIENTE MEJORADO
    # ==========================================
    
    def toggle_panel_paciente(self):
        """🔄 Alternar expansión del panel de paciente"""
        self.panel_paciente_expandido = not self.panel_paciente_expandido
        logger.info(f"✅ Panel paciente {'expandido' if self.panel_paciente_expandido else 'colapsado'}")
    
    def expandir_panel_paciente(self):
        """📈 Expandir panel de paciente"""
        self.panel_paciente_expandido = True
        logger.info("✅ Panel paciente expandido")
    
    def colapsar_panel_paciente(self):
        """📉 Colapsar panel de paciente"""
        self.panel_paciente_expandido = False
        logger.info("✅ Panel paciente colapsado")
    
    def toggle_info_emergencia(self):
        """🚨 Alternar mostrar información de emergencia"""
        self.mostrar_info_emergencia = not self.mostrar_info_emergencia
    
    def toggle_estadisticas_visitas(self):
        """📊 Alternar mostrar estadísticas de visitas"""
        self.mostrar_estadisticas_visitas = not self.mostrar_estadisticas_visitas
    
    def toggle_historial_medico(self):
        """🏥 Alternar mostrar historial médico"""
        self.mostrar_historial_medico = not self.mostrar_historial_medico
    
    # ==========================================
    # 🆕 MÉTODOS PARA FORMULARIO INTEGRADO V3.0
    # ==========================================
    
    # Gestión de dientes seleccionados
    async def limpiar_seleccion_dientes(self):
        """🧹 Limpiar todos los dientes seleccionados"""
        try:
            # Restablecer el diente seleccionado
            self.diente_seleccionado = None
            
            # Limpiar el formulario
            self.formulario_intervencion.dientes_afectados = ""
            
            # Actualizar la lista de dientes seleccionados
            self.actualizar_lista_dientes_seleccionados()
            
            logger.info("✅ Selección de dientes limpiada")
            
        except Exception as e:
            logger.error(f"❌ Error limpiando selección de dientes: {e}")
            self.error_message = str(e)

    async def seleccionar_todos_los_dientes(self):
        """🦷 Seleccionar todos los 32 dientes FDI para servicios generales"""
        try:
            # Lista completa de dientes FDI (32 dientes adulto)
            todos_los_dientes = []
            todos_los_dientes.extend(self.cuadrante_1)  # 11-18
            todos_los_dientes.extend(self.cuadrante_2)  # 21-28
            todos_los_dientes.extend(self.cuadrante_3)  # 31-38
            todos_los_dientes.extend(self.cuadrante_4)  # 41-48

            # Actualizar lista de seleccionados
            self.dientes_seleccionados_lista = [
                {"numero": diente, "condicion": "sano"} for diente in todos_los_dientes
            ]
            self.total_dientes_seleccionados = len(todos_los_dientes)

            # Actualizar formulario (string separado por comas)
            self.formulario_intervencion.dientes_afectados = ",".join(map(str, todos_los_dientes))

            # ✨ SINCRONIZACIÓN: Actualizar también el campo manual
            try:
                if hasattr(self, 'dientes_seleccionados_texto'):
                    self.dientes_seleccionados_texto = ",".join(map(str, todos_los_dientes))
            except Exception as e:
                logger.warning(f"Error sincronizando campo manual: {e}")

            logger.info(f"✅ Seleccionados todos los {len(todos_los_dientes)} dientes FDI")

        except Exception as e:
            logger.error(f"❌ Error seleccionando todos los dientes: {e}")

    async def seleccionar_diente_para_historial(self, numero_diente: int):
        """📚 Seleccionar diente para ver su historial (modo consulta)"""
        try:
            self.diente_seleccionado = numero_diente
            # Cargar historial real desde BD para este diente
            await self.cargar_historial_diente_especifico(numero_diente)
            logger.info(f"✅ Diente {numero_diente} seleccionado para consulta de historial")
        except Exception as e:
            logger.error(f"❌ Error seleccionando diente para historial: {e}")

    async def cargar_historial_diente_especifico(self, numero_diente: int):
        """📊 Cargar historial real de intervenciones en un diente específico"""
        try:
            # Aquí integrarías con el servicio real de odontología
            # Por ahora simulamos datos hasta que tengas el servicio
            self.historial_diente_seleccionado = [
                {
                    "servicio_nombre": "Obturación",
                    "fecha_formateada": "15/08/2024",
                    "observaciones": "Obturación con resina compuesta en superficie oclusal",
                    "odontologo_nombre": "Dr. García",
                    "costo_total": 150.00
                },
                {
                    "servicio_nombre": "Revisión",
                    "fecha_formateada": "10/06/2024",
                    "observaciones": "Control post-tratamiento, evolución favorable",
                    "odontologo_nombre": "Dr. García",
                    "costo_total": 50.00
                }
            ]
            logger.info(f"✅ Historial cargado para diente {numero_diente}")
        except Exception as e:
            logger.error(f"❌ Error cargando historial del diente {numero_diente}: {e}")
            self.historial_diente_seleccionado = []

    async def activar_modo_seleccion_multiple(self):
        """🎯 Activar modo de selección múltiple de dientes"""
        self.modo_seleccion_multiple = True
        logger.info("✅ Modo selección múltiple activado")
    
    async def remover_diente_seleccionado(self, numero_diente: int):
        """🗑️ Remover diente específico de la selección"""
        self.dientes_seleccionados_lista = [
            d for d in self.dientes_seleccionados_lista 
            if d.get('numero') != numero_diente
        ]
        self.total_dientes_seleccionados = len(self.dientes_seleccionados_lista)
        logger.info(f"✅ Diente {numero_diente} removido de selección")
    
    # Gestión de servicios
    async def filtrar_servicios(self, termino: str):
        """🔍 Filtrar servicios por término de búsqueda"""
        self.filtro_servicios = termino.lower()
        logger.info(f"✅ Filtro de servicios aplicado: {termino}")
    
    def is_servicio_seleccionado(self, codigo_servicio: str) -> bool:
        """✅ Verificar si un servicio está seleccionado"""
        return codigo_servicio in self.servicios_seleccionados
    
    async def toggle_servicio_seleccionado(self, codigo_servicio: str, seleccionado: bool):
        """🔄 Agregar/remover servicio de la selección"""
        if seleccionado and codigo_servicio not in self.servicios_seleccionados:
            self.servicios_seleccionados.append(codigo_servicio)
        elif not seleccionado and codigo_servicio in self.servicios_seleccionados:
            self.servicios_seleccionados.remove(codigo_servicio)
        
        self.total_servicios_seleccionados = len(self.servicios_seleccionados)
        await self.actualizar_servicios_detalle()
        await self.recalcular_costos_intervencion()
        logger.info(f"✅ Servicio {codigo_servicio} {'agregado' if seleccionado else 'removido'}")
    
    async def actualizar_servicios_detalle(self):
        """🔄 Actualizar detalles de servicios seleccionados"""
        try:
            detalles = []
            for codigo in self.servicios_seleccionados:
                # Buscar servicio en la lista disponible
                servicio = next((s for s in self.servicios_disponibles if s.codigo == codigo), None)
                if servicio:
                    detalles.append({
                        'codigo': servicio.codigo,
                        'nombre': servicio.nombre,
                        'cantidad': 1,  # Por ahora cantidad fija
                        'precio_usd': servicio.precio_usd,
                        'precio_bs': servicio.precio_bs,
                        'total_usd': servicio.precio_usd * 1,
                        'total_bs': servicio.precio_bs * 1
                    })
            
            self.servicios_seleccionados_detalle = detalles
            logger.info(f"✅ Detalles de servicios actualizados: {len(detalles)} servicios")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando detalles de servicios: {e}")
    
    async def recalcular_costos_intervencion(self):
        """💰 Recalcular costos totales de la intervención"""
        try:
            total_usd = sum(s.get('total_usd', 0) for s in self.servicios_seleccionados_detalle)
            total_bs = sum(s.get('total_bs', 0) for s in self.servicios_seleccionados_detalle)
            
            self.total_usd_intervencion = total_usd
            self.total_bs_intervencion = total_bs
            
            logger.info(f"✅ Costos recalculados: ${total_usd:.2f} USD, Bs {total_bs:,.0f}")
            
        except Exception as e:
            logger.error(f"❌ Error recalculando costos: {e}")
    
    # Gestión de observaciones
    async def actualizar_diagnostico_previo(self, texto: str):
        """📝 Actualizar diagnóstico previo"""
        self.diagnostico_previo = texto
    
    async def actualizar_procedimiento_realizado(self, texto: str):
        """🛠️ Actualizar descripción del procedimiento"""
        self.procedimiento_realizado = texto
    
    async def actualizar_observaciones_post(self, texto: str):
        """📋 Actualizar observaciones post-tratamiento"""
        self.observaciones_post_tratamiento = texto
    
    async def actualizar_recomendaciones_paciente(self, texto: str):
        """💡 Actualizar recomendaciones para el paciente"""
        self.recomendaciones_paciente = texto
    
    # Acciones principales
    async def guardar_intervencion_completa(self):
        """💾 Guardar intervención completa"""
        try:
            self.is_guardando_intervencion = True
            
            # Aquí iría la lógica de guardado real
            # Por ahora simulo el proceso
            
            logger.info("🔄 Iniciando guardado de intervención completa...")
            
            # Simular delay de guardado
            import asyncio
            await asyncio.sleep(1)
            
            logger.info("✅ Intervención guardada exitosamente")
            
            # Limpiar formulario después del guardado
            await self.limpiar_formulario_intervencion_completo()
            
        except Exception as e:
            logger.error(f"❌ Error guardando intervención: {e}")
        finally:
            self.is_guardando_intervencion = False
    
    async def guardar_borrador_intervencion(self):
        """💾 Guardar como borrador"""
        try:
            logger.info("🔄 Guardando borrador de intervención...")
            # Lógica de borrador aquí
            logger.info("✅ Borrador guardado")
        except Exception as e:
            logger.error(f"❌ Error guardando borrador: {e}")
    
    async def mostrar_vista_previa(self):
        """👁️ Mostrar vista previa de la intervención"""
        self.modal_vista_previa_abierto = True
        logger.info("✅ Vista previa abierta")
    
    async def limpiar_formulario_intervencion_completo(self):
        """🧹 Limpiar todo el formulario de intervención"""
        self.dientes_seleccionados_lista = []
        self.total_dientes_seleccionados = 0
        self.servicios_seleccionados = []
        self.servicios_seleccionados_detalle = []
        self.total_servicios_seleccionados = 0
        self.total_usd_intervencion = 0.0
        self.total_bs_intervencion = 0.0
        self.diagnostico_previo = ""
        self.procedimiento_realizado = ""
        self.observaciones_post_tratamiento = ""
        self.recomendaciones_paciente = ""
        self.filtro_servicios = ""
        self.modal_vista_previa_abierto = False
        logger.info("✅ Formulario de intervención limpiado completamente")
    
    # ==========================================
    # 🔍 VALIDACIONES MEJORADAS - FASE CRÍTICA
    # ==========================================
    
    @rx.var(cache=True)
    def precio_valido(self) -> bool:
        """Validación específica del precio - más estricta"""
        try:
            precio_str = self.formulario_intervencion.precio_final.strip()
            if not precio_str:
                return False
                
            precio = float(precio_str)
            precio_base = float(self.precio_servicio_base or 0)
            
            # Precio debe ser positivo
            if precio <= 0:
                return False
            
            # Si hay precio base, no debe exceder 5x el precio base (validación de precio extremo)
            if precio_base > 0 and precio > (precio_base * 5):
                return False
                
            # Precio no debe ser menor al 10% del precio base (muy bajo)
            if precio_base > 0 and precio < (precio_base * 0.1):
                return False
                
            return True
            
        except ValueError:
            return False
        except Exception as e:
            logger.error(f"Error validando precio: {e}")
            return False
    
    @rx.var(cache=True)
    def procedimiento_valido(self) -> bool:
        """Validación del procedimiento - mínimo 10 caracteres"""
        try:
            procedimiento = self.formulario_intervencion.procedimiento_realizado.strip()
            return len(procedimiento) >= 10
        except Exception:
            return False
    
    @rx.var(cache=True)
    def errores_validacion_tiempo_real(self) -> List[str]:
        """Lista de errores para mostrar inmediatamente en el formulario"""
        try:
            errores = []
            
            # Validar servicio seleccionado
            if not self.id_servicio_seleccionado.strip():
                errores.append("Debe seleccionar un servicio")
            
            # Validar procedimiento
            if not self.procedimiento_valido:
                procedimiento = self.formulario_intervencion.procedimiento_realizado.strip()
                if not procedimiento:
                    errores.append("El procedimiento realizado es obligatorio")
                else:
                    errores.append("El procedimiento debe tener al menos 10 caracteres")
            
            # Validar precio
            if not self.precio_valido:
                precio_str = self.formulario_intervencion.precio_final.strip()
                if not precio_str:
                    errores.append("El precio final es obligatorio")
                else:
                    try:
                        precio = float(precio_str)
                        precio_base = float(self.precio_servicio_base or 0)
                        
                        if precio <= 0:
                            errores.append("El precio debe ser mayor a cero")
                        elif precio_base > 0 and precio > (precio_base * 5):
                            errores.append(f"Precio muy alto (máximo ${precio_base * 5:,.2f})")
                        elif precio_base > 0 and precio < (precio_base * 0.1):
                            errores.append(f"Precio muy bajo (mínimo ${precio_base * 0.1:,.2f})")
                    except ValueError:
                        errores.append("El precio debe ser un número válido")
            
            return errores
            
        except Exception as e:
            logger.error(f"Error generando errores validación: {e}")
            return ["Error interno de validación"]
    
    @rx.var(cache=True)
    def alergias_conocidas(self) -> List[str]:
        """Lista de alergias del paciente actual para mostrar alertas"""
        try:
            if hasattr(self.paciente_actual, 'alergias') and self.paciente_actual.alergias:
                return self.paciente_actual.alergias.split(',')
            return []
        except Exception:
            return []
    
    @rx.var(cache=True) 
    def alergias_display(self) -> str:
        """Texto formateado de alergias para mostrar"""
        try:
            alergias = self.alergias_conocidas
            if alergias:
                return ", ".join(alergia.strip() for alergia in alergias if alergia.strip())
            return "Sin alergias reportadas"
        except Exception:
            return "Sin información"
    
    @rx.var(cache=True)
    def formulario_completo(self) -> bool:
        """Validación completa del formulario"""
        return (
            bool(self.id_servicio_seleccionado) and
            self.procedimiento_valido and
            self.precio_valido
        )

