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

class EstadoOdontologia(EstadoOdontogramaAvanzado, mixin=True):
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
    # 🌟 VARIABLES V4.0 - NUEVO DISEÑO PROFESIONAL
    # ==========================================

    # Control del odontograma profesional
    selected_tooth: Optional[int] = None  # Diente seleccionado en el grid
    active_sidebar_tab: str = "historial"  # Tab activo del sidebar (historial|info)
    show_timeline: bool = False  # Mostrar/ocultar timeline de intervenciones

    # Filtros del timeline
    timeline_filter_dentist: str = "all"  # Filtro por dentista
    timeline_filter_procedure: str = "all"  # Filtro por procedimiento
    timeline_filter_period: str = "all"  # Filtro por período (all|7|30|90)

    # ==========================================
    # 💉 VARIABLES PARA INTERVENCIONES COMPLETAS
    # ==========================================

    # Lista de servicios aplicados con sus dientes específicos
    servicios_intervencion: List[Dict[str, Any]] = []
    # Estructura: {
    #   "servicio_id": "uuid",
    #   "nombre_servicio": "Obturación",
    #   "codigo": "OB001",
    #   "dientes": [11, 12],
    #   "cantidad": 1,
    #   "precio_unitario_bs": 50.00,
    #   "precio_unitario_usd": 10.00,
    #   "precio_total_bs": 50.00,
    #   "precio_total_usd": 10.00,
    #   "observaciones": ""
    # }

    # Totales calculados automáticamente
    total_bs_intervencion: float = 0.0
    total_usd_intervencion: float = 0.0

    # Versión de odontograma actual (para vincular con intervención)
    odontograma_version_actual_id: Optional[str] = None

    # Flags de estado para validaciones
    tiene_cambios_odontograma: bool = False
    tiene_servicios_seleccionados: bool = False

    # ==========================================
    # 📋 VARIABLES PARA TIMELINE V4.0
    # ==========================================

    # Datos de intervenciones del paciente actual
    intervenciones_paciente: List[Dict[str, Any]] = []
    # Lista de dentistas que han atendido al paciente
    dentistas_paciente: List[str] = []
    # Lista de procedimientos realizados al paciente
    procedimientos_paciente: List[str] = []

    # ==========================================
    # 🆕 VARIABLES NUEVA ESTRUCTURA (SIN TABS)
    # ==========================================

    # Modales
    show_add_intervention_modal: bool = False
    show_change_condition_modal: bool = False

    # Formulario intervención completa
    selected_service_name: str = ""
    superficie_oclusal_selected: bool = False
    superficie_mesial_selected: bool = False
    superficie_distal_selected: bool = False
    superficie_vestibular_selected: bool = False
    superficie_lingual_selected: bool = False
    auto_change_condition: bool = False
    new_condition_value: str = ""
    intervention_observations: str = ""

    # Formulario cambio condición rápido
    quick_surface_selected: str = ""
    quick_condition_value: str = ""

    # Servicios de consulta actual (temporal, antes de guardar en BD)
    servicios_consulta_actual: List[Dict[str, Any]] = []

    # ==========================================
    # 📊 COMPUTED VARS PARA ODONTOGRAMA
    # ==========================================
    
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
    historial_diente_seleccionado: List[Dict[str, Any]] = []  # Necesario para rx.foreach
    modal_condicion_abierto: bool = False  # Estado del modal selector de condición
    termino_busqueda_condicion: str = ""  # Búsqueda en modal de condiciones
    categoria_condicion_seleccionada: str = "todas"  # Filtro de categoría de condiciones
    
    # 🎈 Variables del popover contextual
    popover_diente_abierto: bool = False  # Estado del popover del diente
    popover_diente_posicion: Dict[str, float] = {}  # Posición x, y del popover

    # ✨ NUEVAS VARIABLES V2.0 - ODONTOGRAMA INTERACTIVO
    # ================================================

    # Estado de carga y guardado
    odontograma_cargando: bool = False
    odontograma_guardando: bool = False
    odontograma_error: str = ""

    # Condiciones por diente organizadas (para interactividad)
    condiciones_por_diente: Dict[int, Dict[str, str]] = {}  # {diente_num: {superficie: condicion}}

    # Modal de selección de condiciones
    modal_condiciones_abierto: bool = False
    condicion_seleccionada_temp: str = "sano"  # Condición temporal para aplicar

    # Feedback visual
    diente_hover: Optional[int] = None
    superficie_hover: Optional[str] = None
    cambios_sin_guardar: bool = False

    # Configuración de condiciones disponibles
    condiciones_disponibles: Dict[str, Dict[str, str]] = {
        "sano": {"color": "#90EE90", "descripcion": "Diente sano", "simbolo": "✓"},
        "caries": {"color": "#FF0000", "descripcion": "Caries dental", "simbolo": "C"},
        "obturado": {"color": "#C0C0C0", "descripcion": "Obturación/empaste", "simbolo": "O"},
        "endodoncia": {"color": "#FFD700", "descripcion": "Tratamiento de conducto", "simbolo": "E"},
        "corona": {"color": "#4169E1", "descripcion": "Corona dental", "simbolo": "R"},
        "puente": {"color": "#800080", "descripcion": "Puente dental", "simbolo": "P"},
        "extraccion": {"color": "#8B0000", "descripcion": "Para extraer", "simbolo": "X"},
        "ausente": {"color": "#FFFFFF", "descripcion": "Diente ausente", "simbolo": "-"},
        "fractura": {"color": "#FF6347", "descripcion": "Fractura dental", "simbolo": "F"},
        "implante": {"color": "#32CD32", "descripcion": "Implante dental", "simbolo": "I"},
        "protesis": {"color": "#DA70D6", "descripcion": "Prótesis removible", "simbolo": "PT"},
        "giroversion": {"color": "#FF8C00", "descripcion": "Diente rotado", "simbolo": "G"}
    }

    # ==========================================
    # 🚀 VARIABLES V3.0 - FASE 1: CACHE INTELIGENTE
    # ==========================================

    # Cache de odontogramas por paciente_id
    odontograma_cache: Dict[str, Dict[int, Dict[str, str]]] = {}
    odontograma_cache_timestamp: Dict[str, float] = {}
    odontograma_cache_ttl: int = 300  # 5 minutos TTL

    # Control de carga lazy de historial
    historial_cargado_por_diente: Dict[int, bool] = {}

    # ==========================================
    # 📦 VARIABLES V3.0 - FASE 2: BATCH UPDATES
    # ==========================================

    # Buffer de cambios pendientes para batch save
    cambios_pendientes_buffer: Dict[int, Dict[str, str]] = {}
    ultimo_guardado_timestamp: float = 0.0
    intervalo_auto_guardado: int = 30  # 30 segundos

    # Control de auto-guardado
    auto_guardado_activo: bool = False
    contador_cambios_pendientes: int = 0

    # ==========================================
    # 📜 VARIABLES V3.0 - FASE 4: HISTORIAL TIMELINE
    # ==========================================

    # Historial completo de versiones del odontograma
    historial_versiones_odontograma: List[Dict[str, Any]] = []  # Necesario para rx.foreach
    total_versiones_historial: int = 0
    historial_versiones_cargando: bool = False

    # Control de modal de historial completo
    modal_historial_completo_abierto: bool = False

    # Filtros de historial
    filtro_odontologo_historial: str = ""
    filtro_tipo_version: str = "Todas"  # Todas, Solo críticas, Con cambios

    # ==========================================
    # 🛡️ VARIABLES V3.0 - FASE 5: VALIDACIONES
    # ==========================================

    # Resultados de validación
    validacion_errores: List[Dict[str, Any]] = []  # Necesario para rx.foreach
    validacion_warnings: List[Dict[str, Any]] = []  # Necesario para rx.foreach
    modal_validacion_abierto: bool = False

    # Variables para la selección de condiciones
    selected_condition_to_apply: Optional[str] = None  # Condición seleccionada para aplicar
    # NOTA: current_surface_condition es un computed var, no variable de estado
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

    # ==========================================
    # 🆕 VARIABLES V2.0 ODONTOGRAMA INTERACTIVO
    # ==========================================
    modo_edicion_ui: bool = False  # Modo visualización vs edición
    mostrar_solo_condiciones: bool = False  # Filtro: solo dientes con condiciones
    mostrar_solo_criticos: bool = False  # Filtro: solo dientes críticos
    
    # Búsqueda de pacientes
    termino_busqueda_pacientes: str = ""
    
    # ==========================================
    # 🦷 ESTADOS DE CARGA Y UI
    # ==========================================
    
    # Estados de carga
    cargando_pacientes_asignados: bool = False
    cargando_servicios: bool = False
    cargando_odontograma_historial: bool = False
    cargando_intervencion: bool = False
    creando_intervencion: bool = False
    
    # Estados de navegación
    en_formulario_intervencion: bool = False
    modo_formulario: str = "crear"
    
    # NAVEGACIÓN DE TABS DE INTERVENCIÓN
    active_intervention_tab: str = "intervencion"  # intervencion, historial
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
    dientes_seleccionados_lista: List[Dict[str, Any]] = []  # Necesario para rx.foreach
    total_dientes_seleccionados: int = 0
    modo_seleccion_multiple: bool = False
    
    # Servicios seleccionados
    servicios_seleccionados: List[str] = []
    servicios_seleccionados_detalle: List[Dict[str, Any]] = []  # Necesario para rx.foreach
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
        """Agrupar consultas por estado - ESQUEMA v4.1"""
        try:
            agrupadas = {
                "programada": [],  # Mantener para backward compatibility
                "en_progreso": [],  # Mantener para backward compatibility
                "completada": [],
                "en_espera": [],
                "en_atencion": [],
                "entre_odontologos": [],
                "cancelada": []
            }

            for consulta in self.consultas_asignadas:
                # Mapear estados nuevos a compatibility keys + agregar estados reales
                estado = consulta.estado

                # Agregar a estado real
                if estado in agrupadas:
                    agrupadas[estado].append(consulta)

                # Mapeo para backward compatibility
                if estado in ["en_espera", "programada"]:
                    agrupadas["programada"].append(consulta)
                elif estado in ["en_atencion", "en_progreso"]:
                    agrupadas["en_progreso"].append(consulta)
                elif estado == "completada":
                    agrupadas["completada"].append(consulta)

            return agrupadas

        except Exception:
            return {"programada": [], "en_progreso": [], "completada": [], "en_espera": [], "en_atencion": [], "entre_odontologos": [], "cancelada": []}
    
    @rx.var(cache=True)
    def total_intervenciones_previas_bs(self) -> float:
        """💰 Total acumulado en BS de intervenciones previas de la consulta"""
        try:
            return sum(
                float(i.costo_total_bs) if i.costo_total_bs else 0.0
                for i in self.intervenciones_anteriores
            )
        except Exception:
            return 0.0

    @rx.var(cache=True)
    def total_intervenciones_previas_usd(self) -> float:
        """💵 Total acumulado en USD de intervenciones previas de la consulta"""
        try:
            return sum(
                float(i.costo_total_usd) if i.costo_total_usd else 0.0
                for i in self.intervenciones_anteriores
            )
        except Exception:
            return 0.0

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
            # Crear PacienteModel básico desde información de consulta
            self.pacientes_asignados = []
            for c in self.consultas_asignadas:
                if c.paciente_id and c.paciente_nombre:
                    from dental_system.models import PacienteModel
                    paciente_basico = PacienteModel(
                        id=c.paciente_id,
                        primer_nombre=c.paciente_nombre.split(' ')[0] if c.paciente_nombre else "",
                        primer_apellido=' '.join(c.paciente_nombre.split(' ')[1:]) if len(c.paciente_nombre.split(' ')) > 1 else "",
                        numero_documento=c.paciente_documento,
                        celular_1=c.paciente_telefono
                    )
                    self.pacientes_asignados.append(paciente_basico)
            
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

            # DEBUG: Mostrar primeros 3 servicios para verificar que tienen ID
            if servicios_data:
                for i, servicio in enumerate(servicios_data[:3]):
                    logger.debug(f"  Servicio {i+1}: {servicio.nombre} (ID: {servicio.id})")

        except Exception as e:
            logger.error(f"❌ Error cargando servicios: {e}")

        finally:
            self.cargando_servicios = False
    
    async def cargar_intervenciones_consulta_actual(self):
        """
        📋 CARGAR INTERVENCIONES PREVIAS DE LA CONSULTA ACTUAL

        Carga todas las intervenciones registradas para la consulta actual,
        útil para ver qué otros odontólogos ya atendieron al paciente.
        """
        if not self.consulta_actual or not self.consulta_actual.id:
            logger.warning("No hay consulta actual para cargar intervenciones")
            return

        try:
            from dental_system.services.odontologia_service import odontologia_service

            # Establecer contexto de usuario
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # TODO: Cargar intervenciones de esta consulta
            # NOTA: Método get_intervenciones_by_consulta no implementado aún
            # intervenciones_data = await odontologia_service.get_intervenciones_by_consulta(
            #     self.consulta_actual.id
            # )

            # Actualizar lista de intervenciones anteriores (vacía por ahora)
            self.intervenciones_anteriores = []

            logger.info(f"✅ Intervenciones previas: función pendiente de implementar")

        except Exception as e:
            logger.error(f"❌ Error cargando intervenciones de consulta: {e}")
            self.intervenciones_anteriores = []

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

            # DEBUG: Mostrar estado de cuadrantes
            print(f"DEBUG - Estado cuadrantes después de cargar catálogo:")
            print(f"  catalogo_cargado: {self.catalogo_cargado}")
            print(f"  cuadrante_1: {self.cuadrante_1}")
            print(f"  cuadrante_2: {self.cuadrante_2}")
            print(f"  cuadrante_3: {self.cuadrante_3}")
            print(f"  cuadrante_4: {self.cuadrante_4}")
            
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
                
            print(f"OK Odontograma cargado para paciente {paciente_id} por odontologo {self.id_personal}")
            
        except Exception as e:
            print(f"ERROR cargando odontograma: {e}")
            self.error_message = f"Error cargando odontograma: {str(e)}"

    @rx.event
    async def test_forzar_actualizacion_cuadrantes(self):
        """Método de test para forzar actualización de cuadrantes"""
        print("\nTEST: Forzando actualización de cuadrantes...")

        # Cargar catálogo si no está cargado
        if not self.catalogo_cargado:
            await self.cargar_catalogo_fdi()

        # Forzar cambio de cuadrantes para activar reactivity
        self.cuadrante_1 = [11, 12, 13, 14, 15, 16, 17, 18]
        self.cuadrante_2 = [21, 22, 23, 24, 25, 26, 27, 28]
        self.cuadrante_3 = [31, 32, 33, 34, 35, 36, 37, 38]
        self.cuadrante_4 = [41, 42, 43, 44, 45, 46, 47, 48]

        print(f"TEST: Cuadrantes actualizados manualmente")
        print(f"  Cuadrante 1: {self.cuadrante_1}")
        print(f"  Cuadrante 2: {self.cuadrante_2}")
        print(f"  Cuadrante 3: {self.cuadrante_3}")
        print(f"  Cuadrante 4: {self.cuadrante_4}")

        # Obtener estado UI para mostrar mensaje
        self.mostrar_toast("Cuadrantes actualizados manualmente", "success")

    # Los métodos _inicializar_dientes_fdi, _obtener_cuadrante_diente y _obtener_tipo_diente
    # han sido reemplazados por la funcionalidad del catálogo FDI en EstadoOdontogramaAvanzado
    
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
            
            # ⚠️ TEMP FIX: Métodos no implementados - comentar para evitar errores
            # intervenciones_data = await odontologia_service.get_intervenciones_anteriores_paciente(paciente_id)
            # ultima_consulta_data = await odontologia_service.get_ultima_consulta_paciente(paciente_id)
            intervenciones_data = []  # Datos vacíos temporalmente
            ultima_consulta_data = {}
            
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

    # ==========================================
    # 🚀 MÉTODOS V3.0 - FASE 1: CACHE INTELIGENTE
    # ==========================================

    def _es_cache_valido(self, paciente_id: str) -> bool:
        """
        ✅ Verificar si el cache del odontograma está vigente

        Args:
            paciente_id: ID del paciente

        Returns:
            True si el cache es válido y puede usarse
        """
        import time

        if paciente_id not in self.odontograma_cache:
            return False

        timestamp = self.odontograma_cache_timestamp.get(paciente_id, 0)
        tiempo_transcurrido = time.time() - timestamp

        es_valido = tiempo_transcurrido < self.odontograma_cache_ttl

        if es_valido:
            logger.info(f"✅ Cache válido para paciente {paciente_id} ({tiempo_transcurrido:.1f}s)")
        else:
            logger.info(f"⏰ Cache expirado para paciente {paciente_id} ({tiempo_transcurrido:.1f}s > {self.odontograma_cache_ttl}s)")

        return es_valido

    async def cargar_odontograma_paciente_optimizado(self):
        """
        🚀 FASE 1.1: Carga optimizada con cache inteligente

        Flujo:
        1. Verifica cache válido → usa cache
        2. Cache inválido → carga desde BD y actualiza cache
        3. Muestra feedback visual durante carga
        """
        import time

        # Validar que hay paciente actual con ID
        if not hasattr(self, 'paciente_actual') or not self.paciente_actual:
            logger.warning("⚠️ No hay paciente actual para cargar odontograma")
            return

        paciente_id = getattr(self.paciente_actual, 'id', None)
        if not paciente_id:
            logger.warning("⚠️ Paciente actual sin ID")
            return

        # Verificar cache
        if self._es_cache_valido(paciente_id):
            logger.info(f"✅ Usando cache para paciente {paciente_id}")
            self.condiciones_por_diente = self.odontograma_cache[paciente_id].copy()
            self.cambios_sin_guardar = False
            return

        # Cargar desde BD con indicador visual
        self.odontograma_cargando = True
        self.odontograma_error = ""

        try:
            # Establecer contexto
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Obtener o crear odontograma del paciente
            resultado = await odontologia_service.get_or_create_patient_odontogram(
                paciente_id,
                self.id_personal
            )

            if resultado:
                # Actualizar estado con condiciones cargadas
                condiciones = resultado.get("conditions", {})
                self.condiciones_por_diente = condiciones.copy()

                # Actualizar cache
                self.odontograma_cache[paciente_id] = condiciones.copy()
                self.odontograma_cache_timestamp[paciente_id] = time.time()

                self.cambios_sin_guardar = False

                logger.info(f"✅ Odontograma cargado desde BD y cacheado: {len(condiciones)} dientes con condiciones")
            else:
                logger.warning(f"⚠️ No se pudo obtener odontograma para paciente {paciente_id}")
                self.odontograma_error = "No se pudo cargar el odontograma"

        except Exception as e:
            logger.error(f"❌ Error cargando odontograma: {e}")
            self.odontograma_error = f"Error: {str(e)}"

        finally:
            self.odontograma_cargando = False

    def invalidar_cache_odontograma(self, paciente_id: Optional[str] = None):
        """
        🗑️ Invalidar cache del odontograma

        Args:
            paciente_id: ID específico del paciente. Si es None, invalida todo el cache.
        """
        if paciente_id:
            self.odontograma_cache.pop(paciente_id, None)
            self.odontograma_cache_timestamp.pop(paciente_id, None)
            logger.info(f"🗑️ Cache invalidado para paciente {paciente_id}")
        else:
            self.odontograma_cache.clear()
            self.odontograma_cache_timestamp.clear()
            logger.info("🗑️ Cache completo de odontogramas invalidado")

    async def cargar_historial_diente_lazy(self, tooth_number: int):
        """
        🚀 FASE 1.2: Carga lazy del historial de un diente específico

        Solo carga el historial cuando el usuario hace click en el tab "Historial"

        Args:
            tooth_number: Número FDI del diente
        """
        # Verificar si ya está cargado
        if self.historial_cargado_por_diente.get(tooth_number, False):
            logger.info(f"✅ Historial de diente {tooth_number} ya está en cache")
            return

        self.cargando_odontograma_historial = True

        try:
            # Establecer contexto
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Cargar historial del diente
            historial = await odontologia_service.get_tooth_condition_history(
                self.paciente_actual.id,
                tooth_number
            )

            # Actualizar estado
            self.historial_diente_seleccionado = historial or []
            self.historial_cargado_por_diente[tooth_number] = True

            logger.info(f"✅ Historial de diente {tooth_number} cargado: {len(historial)} entradas")

        except Exception as e:
            logger.error(f"❌ Error cargando historial de diente {tooth_number}: {e}")
            self.historial_diente_seleccionado = []

        finally:
            self.cargando_odontograma_historial = False

    # ==========================================
    # 📦 MÉTODOS V3.0 - FASE 2: BATCH UPDATES
    # ==========================================

    def registrar_cambio_diente(self, tooth_number: int, surface: str, condition: str):
        """
        📦 FASE 2.1: Registrar cambio en buffer sin guardar inmediatamente

        Los cambios se acumulan en buffer y se guardan en batch cuando:
        - Usuario hace click en "Guardar cambios"
        - Pasan 30 segundos (auto-guardado)
        - Usuario finaliza la intervención

        Args:
            tooth_number: Número FDI del diente
            surface: Superficie del diente (oclusal, mesial, etc.)
            condition: Nueva condición (sano, caries, etc.)
        """
        # Inicializar buffer para este diente si no existe
        if tooth_number not in self.cambios_pendientes_buffer:
            self.cambios_pendientes_buffer[tooth_number] = {}

        # Registrar cambio en buffer
        self.cambios_pendientes_buffer[tooth_number][surface] = condition

        # Actualizar visual inmediatamente (optimistic update)
        if tooth_number not in self.condiciones_por_diente:
            self.condiciones_por_diente[tooth_number] = {}
        self.condiciones_por_diente[tooth_number][surface] = condition

        # Marcar como cambios sin guardar
        self.cambios_sin_guardar = True
        self.contador_cambios_pendientes = sum(
            len(surfaces) for surfaces in self.cambios_pendientes_buffer.values()
        )

        logger.info(f"📝 Cambio registrado en buffer: Diente {tooth_number} {surface} → {condition} ({self.contador_cambios_pendientes} cambios pendientes)")

    # TODO V3.0: Este método necesita refactoring completo para usar @rx.event(background=True)
    # Por ahora mantenerlo sin decorador para no romper funcionalidad V2.0
    async def guardar_cambios_batch(self):
        """
        💾 FASE 2.1 + FASE 3.3: Guardar con versionado automático

        Proceso completo:
        1. Detectar si requiere nueva versión
        2. Crear nueva versión si es necesario
        3. Guardar cambios en batch
        4. Limpiar buffer y actualizar UI

        Ventajas:
        - Reduce queries a BD de N a 1
        - Versionado automático sin intervención
        - Mejora rendimiento
        """
        import time

        if not self.cambios_pendientes_buffer:
            logger.info("ℹ️ No hay cambios pendientes para guardar")
            return

        self.odontograma_guardando = True

        try:
            # Establecer contexto
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Obtener ID del odontograma actual
            if not self.odontograma_actual or not self.odontograma_actual.id:
                # Si no existe, obtener o crear
                resultado = await odontologia_service.get_or_create_patient_odontogram(
                    self.paciente_actual.id,
                    self.id_personal
                )
                odontogram_id = resultado.get("id")
            else:
                odontogram_id = self.odontograma_actual.id

            # 🛡️ FASE 5.2: Validar cambios ANTES de guardar
            condiciones_anteriores = self.condiciones_por_diente.copy()

            es_valido, errores_validacion, warnings_validacion = odontologia_service.validar_cambios_odontograma(
                condiciones_anteriores,
                self.cambios_pendientes_buffer
            )

            # Si hay errores críticos, bloquear guardado
            if not es_valido:
                logger.error(f"❌ Validación falló: {len(errores_validacion)} errores")
                self.odontograma_error = f"Errores de validación: {len(errores_validacion)}"

                # Guardar errores y warnings para mostrar en modal
                self.validacion_errores = errores_validacion
                self.validacion_warnings = warnings_validacion
                self.modal_validacion_abierto = True

                return  # BLOQUEAR guardado

            # Si hay warnings pero es válido, mostrar pero permitir continuar
            if len(warnings_validacion) > 0:
                logger.warning(f"⚠️ {len(warnings_validacion)} advertencias detectadas")
                self.validacion_warnings = warnings_validacion
                self.modal_validacion_abierto = True
                # Continuar con guardado después de mostrar warnings

            # 🚀 FASE 3.3: Detectar si requiere nueva versión
            requiere_version, cambios_criticos, motivo = await odontologia_service.detectar_cambios_significativos(
                condiciones_anteriores,
                self.cambios_pendientes_buffer
            )

            # 🚀 Si requiere nueva versión, crear antes de guardar
            if requiere_version:
                logger.info(f"📚 Creando nueva versión: {motivo}")

                nueva_version = await odontologia_service.crear_nueva_version_odontograma(
                    odontograma_actual_id=odontogram_id,
                    paciente_id=self.paciente_actual.id,
                    odontologo_id=self.id_personal,
                    intervencion_id=self.intervencion_actual.id if self.intervencion_actual else None,
                    cambios_criticos=cambios_criticos,
                    motivo=motivo
                )

                # Actualizar referencia al odontograma actual
                odontogram_id = nueva_version["id"]
                if self.odontograma_actual:
                    self.odontograma_actual.id = nueva_version["id"]
                    self.odontograma_actual.version = nueva_version["version"]

                self.mostrar_toast_info(
                    f"📚 Nueva versión creada: v{nueva_version['version']} - {motivo}"
                )

            # Guardar todos los cambios en un solo batch
            contador_antes = self.contador_cambios_pendientes
            logger.info(f"💾 Guardando {contador_antes} cambios en batch...")

            success = await odontologia_service.save_odontogram_conditions(
                odontogram_id,
                self.cambios_pendientes_buffer
            )

            if success:
                # Limpiar buffer
                self.cambios_pendientes_buffer = {}
                self.cambios_sin_guardar = False
                self.contador_cambios_pendientes = 0
                self.ultimo_guardado_timestamp = time.time()

                # Invalidar cache para forzar recarga en próxima visita
                self.invalidar_cache_odontograma(self.paciente_actual.id)

                logger.info("✅ Cambios guardados exitosamente en batch con versionado")

                self.mostrar_toast_exito(f"✅ {contador_antes} cambios guardados")
            else:
                logger.error("❌ Error guardando cambios en batch")
                self.odontograma_error = "Error al guardar cambios"

        except Exception as e:
            logger.error(f"❌ Error en guardar_cambios_batch: {e}")
            self.odontograma_error = f"Error: {str(e)}"

        finally:
            self.odontograma_guardando = False

    @rx.event(background=True)
    async def iniciar_auto_guardado(self):
        """
        ⏰ FASE 2.2: Auto-guardado inteligente cada 30 segundos

        Ejecuta en background y guarda automáticamente si:
        - Hay cambios pendientes
        - Han pasado al menos 30 segundos desde el último guardado
        """
        import asyncio
        import time

        # IMPORTANTE: Modificar estado dentro de context manager en background tasks
        async with self:
            self.auto_guardado_activo = True
        logger.info("⏰ Auto-guardado activado (cada 30 segundos)")

        while self.auto_guardado_activo:
            await asyncio.sleep(self.intervalo_auto_guardado)

            # Verificar si hay cambios pendientes
            if self.cambios_sin_guardar and self.contador_cambios_pendientes > 0:
                tiempo_desde_ultimo = time.time() - self.ultimo_guardado_timestamp

                if tiempo_desde_ultimo >= self.intervalo_auto_guardado:
                    logger.info(f"🔄 Auto-guardado activado ({self.contador_cambios_pendientes} cambios pendientes)")

                    async with self:
                        await self.guardar_cambios_batch()

    def detener_auto_guardado(self):
        """
        🛑 Detener el auto-guardado en background

        Debe llamarse al salir de la página de intervención
        """
        self.auto_guardado_activo = False
        logger.info("🛑 Auto-guardado detenido")

    async def descartar_cambios_pendientes(self):
        """
        ❌ Descartar cambios pendientes sin guardar

        Recarga el odontograma desde la base de datos, descartando los cambios pendientes.
        """
        # Recargar odontograma desde BD para restaurar estado original
        await self.cargar_odontograma_paciente_optimizado()

        logger.info("❌ Cambios pendientes descartados - odontograma recargado desde BD")

        # Mostrar toast
        self.mostrar_toast_warning("Cambios descartados")

    # ==========================================
    # 📜 MÉTODOS V3.0 - FASE 4: HISTORIAL TIMELINE
    # ==========================================
    @rx.event(background=True)
    async def cargar_historial_versiones(self):
        """
        📜 FASE 4.3: Cargar historial completo de versiones del odontograma

        Carga todas las versiones del odontograma del paciente actual con:
        - Información de cada versión
        - Cambios detectados vs versión anterior
        - Odontólogo responsable
        - Fecha y motivo de cada versión
        """
        async with self:
            self.historial_versiones_cargando = True
            self.historial_versiones_odontograma = []
            self.total_versiones_historial = 0

        try:
            # Validar que hay paciente actual con ID
            if not hasattr(self, 'paciente_actual') or not self.paciente_actual:
                logger.warning("⚠️ No hay paciente actual para cargar historial")
                return

            paciente_id = getattr(self.paciente_actual, 'id', None)
            if not paciente_id:
                logger.warning("⚠️ Paciente actual sin ID para cargar historial")
                return

            # Cargar historial completo desde el service
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)
            historial = await odontologia_service.get_odontogram_full_history(paciente_id)

            async with self:
                if historial:
                    self.historial_versiones_odontograma = historial
                    self.total_versiones_historial = len(historial)
                    logger.info(f"✅ Historial cargado: {self.total_versiones_historial} versiones")
                else:
                    logger.info("ℹ️ No hay historial de versiones para este paciente")

        except Exception as e:
            logger.error(f"❌ Error cargando historial de versiones: {e}")
            async with self:
                self.odontograma_error = f"Error al cargar historial: {str(e)}"

        finally:
            async with self:
                self.historial_versiones_cargando = False

    def abrir_modal_historial(self):
        """
        🗂️ FASE 4.4: Abrir modal de historial completo

        Abre el modal flotante y carga el historial de versiones
        """
        self.modal_historial_completo_abierto = True
        # Cargar historial si no está cargado o está desactualizado
        if self.total_versiones_historial == 0:
            yield EstadoOdontologia.cargar_historial_versiones

    def cerrar_modal_historial(self):
        """
        ❌ Cerrar modal de historial completo
        """
        self.modal_historial_completo_abierto = False

    async def ver_detalles_version(self, version_id: str):
        """
        👁️ FASE 4.5: Ver detalles de una versión específica

        Carga los detalles completos de una versión seleccionada
        Args:
            version_id: ID de la versión a visualizar
        """
        logger.info(f"👁️ Viendo detalles de versión: {version_id}")
        # TODO: Implementar vista detallada de versión específica
        # Por ahora, solo registrar la acción

    async def comparar_con_anterior(self, version_id: str):
        """
        🔄 FASE 4.6: Comparar versión con la anterior

        Muestra una comparación lado a lado de dos versiones
        Args:
            version_id: ID de la versión a comparar
        """
        logger.info(f"🔄 Comparando versión: {version_id} con anterior")
        # TODO: Implementar vista comparativa de versiones
        # Por ahora, solo registrar la acción

    # ==========================================
    # 🛡️ MÉTODOS V3.0 - FASE 5: VALIDACIONES
    # ==========================================

    def cerrar_modal_validacion(self):
        """❌ Cerrar modal de validación"""
        self.modal_validacion_abierto = False
        self.validacion_errores = []
        self.validacion_warnings = []

    def forzar_guardado_con_warnings(self):
        """
        ⚠️ FASE 5.3: Forzar guardado a pesar de warnings

        Permite al usuario continuar guardando después de revisar warnings.
        Solo funciona si NO hay errores críticos.
        """
        # Solo cerrar modal si no hay errores críticos
        # (el guardado continúa automáticamente desde guardar_cambios_batch)

    # ==========================================
    # 🔧 SETTERS MANUALES PARA FILTROS - FASE 4
    # ==========================================
    # NOTA: En Reflex, event handlers ya reciben 'self' implícitamente
    # Solo necesitamos el parámetro del valor que envía el componente

    def set_filtro_odontologo_historial(self, valor: str):
        """
        🔍 Setter para filtro de odontólogo en historial

        Args:
            valor: Texto de búsqueda para filtrar por odontólogo

        Event: Llamado desde rx.input.on_change (envía 1 arg: el texto)
        """
        self.filtro_odontologo_historial = valor
        logger.info(f"🔍 Filtro odontólogo historial actualizado: '{valor}'")

    def set_filtro_tipo_version(self, valor: str):
        """
        🔍 Setter para filtro de tipo de versión

        Args:
            valor: Tipo de versión ("Todas", "Solo críticas", "Con cambios")

        Event: Llamado desde rx.select.on_change (envía 1 arg: el valor seleccionado)
        """
        self.filtro_tipo_version = valor
        logger.info(f"🔍 Filtro tipo versión actualizado: '{valor}'")

    async def tomar_paciente_disponible(self, paciente: PacienteModel, consulta_id: str):
        """
        🔄 TOMAR PACIENTE DISPONIBLE (EN ESTADO "entre_odontologos")

        Flujo para segundo/tercer odontólogo:
        1. Cambia estado de consulta: "entre_odontologos" → "en_atencion"
        2. Registra segundo odontólogo en la consulta
        3. Carga odontograma con última versión
        4. Carga intervenciones previas de otros odontólogos
        5. Navega a página de intervención

        Args:
            paciente: Modelo del paciente a tomar
            consulta_id: ID de la consulta asociada
        """


        try:
            logger.info(f"🔄 Tomando paciente {paciente.nombre_completo} de otro odontólogo")

            # Validar que la consulta esté en estado "entre_odontologos"
            consulta_encontrada = next(
                (c for c in self.consultas_disponibles_otros if c.id == consulta_id),
                None
            )

            if not consulta_encontrada:
                logger.warning(f"❌ Consulta no encontrada: {consulta_id}")
                self.mostrar_toast_error("Consulta no encontrada")
                return

            if consulta_encontrada.estado != "entre_odontologos":
                logger.warning(f"⚠️ Consulta no está en estado 'entre_odontologos': {consulta_encontrada.estado}")
                # Continuar de todas formas, puede estar en otro estado válido

            # Usar servicio para derivar/asignar paciente
            from dental_system.services.odontologia_service import odontologia_service
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

            resultado = await self.derivar_paciente_a_odontologo(
                consulta_id=consulta_id,
                nuevo_odontologo_id=self.id_personal,
                motivo_derivacion="Intervención adicional requerida"
            )

            if resultado:
                logger.info(f"✅ Paciente {paciente.nombre_completo} asignado exitosamente")

                # Mover paciente de disponibles a asignados (UI local)
                self.pacientes_disponibles_otros = [
                    p for p in self.pacientes_disponibles_otros if p.id != paciente.id
                ]
                self.pacientes_asignados.append(paciente)

                # Actualizar contadores
                self.total_pacientes_disponibles = len(self.pacientes_disponibles_otros)
                self.total_pacientes_asignados = len(self.pacientes_asignados)

                # Establecer contexto actual
                self.paciente_actual = paciente
                self.consulta_actual = consulta_encontrada

                # Cambiar estado a "en_atencion" para este odontólogo
                await self.iniciar_atencion_consulta(
                    consulta_id,
                    estado_objetivo="en_atencion"
                )

                # Cargar odontograma (última versión con cambios previos)
                await self.cargar_odontograma_paciente_actual()

                # Cargar intervenciones previas de otros odontólogos
                await self.cargar_intervenciones_consulta_actual()

                # Establecer flag de formulario activo
                self.en_formulario_intervencion = True
                self.modo_formulario = "crear"

                # Mostrar toast de éxito
                self.mostrar_toast_exito(f"Paciente {paciente.nombre_completo} asignado - Ver intervenciones previas")

                # Navegar a página de intervención
                self.navigate_to(
                    "intervencion",
                    f"Intervención Adicional - {paciente.nombre_completo}",
                    f"Consulta #{consulta_encontrada.numero_consulta or 'N/A'}"
                )

                logger.info(f"🦷 Navegación a intervención completada")

        except Exception as e:
            logger.error(f"❌ Error tomando paciente disponible: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_toast_error("Error al tomar paciente")
    
    # ==========================================
    # 🦷 GESTIÓN DE CONSULTAS E INTERVENCIONES
    # ==========================================
    
    async def iniciar_consulta(self, consulta_id: str):
        """
        Iniciar consulta (programada → en_progreso)
        """
        
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
            
            self.mostrar_toast_exito("Consulta iniciada")
            logger.info(f"✅ Consulta iniciada: {consulta_id}")
            
        except Exception as e:
            logger.error(f"❌ Error iniciando consulta: {e}")
            self.mostrar_toast_error("Error al iniciar consulta")
    
    async def completar_consulta(self, consulta_id: str):
        """
        Completar consulta (en_progreso → completada)
        """

        try:
            consulta_actualizada = await odontologia_service.completar_consulta(consulta_id)
            
            # Actualizar en la lista
            for i, consulta in enumerate(self.consultas_asignadas):
                if consulta.id == consulta_id:
                    self.consultas_asignadas[i] = consulta_actualizada
                    break
            
            self.mostrar_toast_exito("Consulta completada")
            logger.info(f"✅ Consulta completada: {consulta_id}")
            
        except Exception as e:
            logger.error(f"❌ Error completando consulta: {e}")
            self.mostrar_toast_error("Error al completar consulta")
    
    def navegar_a_intervencion(self, paciente: PacienteModel, consulta: ConsultaModel):
        """
        Navegar al formulario de intervención
        """

        # Establecer paciente y consulta actual
        self.paciente_actual = paciente
        self.consulta_actual = consulta
        
        # Limpiar formulario
        self.limpiar_formulario_intervencion()
        
        # Cambiar estado UI
        self.en_formulario_intervencion = True
        self.modo_formulario = "crear"
        
        # Cargar odontograma del paciente
        
        # self.cargar_odontograma_paciente(paciente.id)
        
        # Navegar a página de intervención
        self.navegar_a("intervencion")
        
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

            logger.info(f"✅ Cambios del odontograma guardados en memoria local")

        except PermissionError as e:
            logger.error(f"❌ Error de permisos: {e}")
            yield rx.toast.error(
                "⚠️ Sin Permisos",
                description=str(e),
                duration=5000
            )
        except Exception as e:
            logger.error(f"❌ Error guardando odontograma: {e}")
            yield rx.toast.error(
                "Error al guardar",
                description=str(e),
                duration=3000
            )
    
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
    async def seleccionar_diente_unificado(
        self,
        numero_diente: int,
        modo: str = "simple",
        superficie: str = "",
        cargar_historial: bool = False,
        cargar_estadisticas: bool = False
    ):
        """
        🦷 FUNCIÓN UNIFICADA PARA SELECCIÓN DE DIENTES

        Esta función reemplaza a todas las funciones de selección individuales:
        - seleccionar_diente_simple() -> modo="simple"
        - seleccionar_diente_svg() -> modo="svg"
        - seleccionar_diente() -> modo="principal"
        - seleccionar_diente_superficie() -> modo="superficie" + superficie
        - seleccionar_diente_para_historial() -> modo="historial" + cargar_historial=True
        - seleccionar_diente_profesional() -> modo="profesional" + cargar_historial=True + cargar_estadisticas=True

        Args:
            numero_diente: Número FDI del diente (11-48)
            modo: Tipo de selección ("simple", "svg", "principal", "superficie", "historial", "profesional")
            superficie: Nombre de la superficie (solo para modo="superficie")
            cargar_historial: Si cargar historial del diente desde BD
            cargar_estadisticas: Si cargar estadísticas del paciente
        """
        try:
            # Validar número de diente FDI
            todos_los_dientes = self.cuadrante_1 + self.cuadrante_2 + self.cuadrante_3 + self.cuadrante_4
            if numero_diente not in todos_los_dientes:
                logger.warning(f"⚠️ Número de diente inválido: {numero_diente}")
                return

            # Selección básica común a todos los modos
            self.diente_seleccionado = numero_diente

            # Lógica específica por modo
            if modo == "simple":
                # Si estamos en modo edición, agregar a dientes afectados del formulario
                if self.modo_odontograma == "edicion":
                    self.agregar_diente_afectado(numero_diente)
                # También actualizar la lista visual de dientes seleccionados
                self.actualizar_lista_dientes_seleccionados()

            elif modo == "svg":
                # Solo selección básica (ya hecha arriba)
                pass

            elif modo == "principal":
                # En modo edición, agregar a lista de dientes afectados para intervención
                if self.modo_odontograma == "edicion":
                    self.agregar_diente_afectado(numero_diente)
                    self.actualizar_lista_dientes_seleccionados()
                logger.info(f"🦷 Diente {numero_diente} seleccionado (modo principal)")

            elif modo == "superficie":
                # Validar superficie si se proporciona
                superficies_validas = ["oclusal", "mesial", "distal", "vestibular", "lingual", "palatino"]
                if superficie and superficie not in superficies_validas:
                    logger.warning(f"⚠️ Superficie inválida: {superficie}")
                    return
                # Establecer superficie seleccionada
                if superficie:
                    self.superficie_seleccionada = superficie
                logger.info(f"🦷 Diente {numero_diente} superficie {superficie} seleccionada")

            elif modo == "historial":
                cargar_historial = True

            elif modo == "profesional":
                cargar_historial = True
                cargar_estadisticas = True

            # Cargar historial si se solicita
            if cargar_historial:
                await self.cargar_historial_diente_especifico(numero_diente)

            # Cargar estadísticas si se solicita
            if cargar_estadisticas:
                if not hasattr(self, 'estadisticas_paciente_bd') or not self.estadisticas_paciente_bd:
                    await self.obtener_estadisticas_paciente_bd_async()

            logger.info(f"✅ Diente {numero_diente} seleccionado exitosamente (modo: {modo})")

        except Exception as e:
            logger.error(f"❌ Error seleccionando diente {numero_diente}: {e}")

    # ==========================================
    # 🔄 FUNCIONES DE RETROCOMPATIBILIDAD
    # ==========================================
    # Estas funciones mantienen la compatibilidad con el código existente
    # y redirigen a la función unificada

    @rx.event
    def seleccionar_diente_simple(self, numero_diente: int):
        """🔄 FUNCIÓN DE RETROCOMPATIBILIDAD - Usar seleccionar_diente_unificado()"""
        return self.seleccionar_diente_unificado(numero_diente, modo="simple")
    
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
        """Obtener color del diente según su estado real desde BD"""
        try:
            # Primera verificación: dientes afectados en formulario actual
            dientes_afectados_formulario = []
            if isinstance(self.formulario_intervencion.dientes_afectados, str):
                if self.formulario_intervencion.dientes_afectados.strip():
                    dientes_afectados_formulario = [int(x.strip()) for x in self.formulario_intervencion.dientes_afectados.split(",") if x.strip().isdigit()]

            if numero_diente in dientes_afectados_formulario:
                return "blue"  # Azul para seleccionados en formulario

            # Segunda verificación: estado real desde BD usando condiciones_odontograma
            estado_real = self.obtener_estado_diente_bd_sync(numero_diente)

            # Mapeo de estados a esquemas de colores de Reflex
            color_mapping = {
                "sano": "green",         # Verde para sanos
                "caries": "red",         # Rojo para caries
                "obturado": "gray",      # Gris para obturaciones
                "corona": "purple",      # Púrpura para coronas
                "endodoncia": "yellow",  # Amarillo para endodoncias
                "extraccion": "blackAlpha", # Negro para extracciones
                "ausente": "gray",       # Gris claro para ausentes
                "implante": "cyan",      # Cyan para implantes
                "fractura": "orange",    # Naranja para fracturas
                "tratado": "teal"        # Verde azulado para tratados
            }

            return color_mapping.get(estado_real, "gray")  # Por defecto gris

        except Exception as e:
            logger.warning(f"Error obteniendo color diente {numero_diente}: {e}")
            return "gray"  # Color por defecto en caso de error
    
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
    
    # ==========================================
    # 📝 FORMULARIO MANUAL LEGACY - ELIMINADO
    # ==========================================
    # REFACTOR: Funciones eliminadas (editor_superficie, historial_superficie, planificador_tratamiento, notas_diente)
    # Ahora se usa tooth_detail_sidebar con tabs especializados
    
    @rx.event
    def seleccionar_diente_svg(self, numero_diente: int):
        """🔄 FUNCIÓN DE RETROCOMPATIBILIDAD - Usar seleccionar_diente_unificado()"""
        return self.seleccionar_diente_unificado(numero_diente, modo="svg")
    
    # ==========================================
    # 🔄 SISTEMA VERSIONADO ODONTOGRAMA - OBSOLETO
    # ==========================================
    # NOTA: Esta sección contiene código OBSOLETO del sistema de versionado antiguo.
    # La funcionalidad de versionado ahora está implementada en V3.0:
    # - FASE 3: Versionado automático (línea ~1033-1091)
    # - FASE 4: Historial timeline (línea ~1200-1285)
    #
    # Este código se mantiene comentado solo como referencia histórica.
    # NO USAR - Puede causar conflictos con V3.0
    # ==========================================

    # # Variables del sistema de versionado (OBSOLETAS - V3.0 usa otras)
    # version_actual_odontograma: str = "2.1"
    # historial_versiones: List[Dict[str, Any]] = []  # V3.0 usa: historial_versiones_odontograma
    # modal_nueva_version_abierto: bool = False
    # comentario_nueva_version: str = ""
    # cambios_detectados_actual: List[Dict[str, str]] = []
    # modo_comparacion_activo: bool = False
    # version_comparar_a: str = "v2.1 (Actual)"
    # version_comparar_b: str = "v2.0"

    # MÉTODOS OBSOLETOS REMOVIDOS:
    # - cargar_historial_versiones() → Ahora en FASE 4.3 (línea ~1202)
    # - detectar_cambios_significativos() → Ahora en service (odontologia_service.py)
    # - abrir_modal_nueva_version() → Versionado es automático en V3.0
    # - confirmar_nueva_version() → Ahora es crear_nueva_version_odontograma() en service
    # - cancelar_nueva_version() → No necesario, versionado automático
    # - crear_version_manual() → No necesario, versionado automático
    # - ver_version_odontograma() → Ahora es ver_detalles_version() (línea ~1262)
    # - comparar_version() → Ahora es comparar_con_anterior() (línea ~1275)
    # - restaurar_version() → Pendiente implementar en V4.0
    # - cambiar_version_a/b() → Pendiente implementar en V4.0
    # - cerrar_comparador() → Pendiente implementar en V4.0
    
    # ==========================================
    # 📜 HISTORIAL MANUAL Y ALERTAS - ELIMINADO
    # ==========================================
    # REFACTOR: Historial manual eliminado (filtros, exportar, ver cambios, alertas, recordatorios)
    # Ahora usa intervention_timeline automático desde BD
    
    # ==========================================
    # 🔔 SISTEMA DE NOTIFICACIONES - ELIMINADO
    # ==========================================
    # REFACTOR: Sistema de notificaciones toast eliminado por no uso en páginas principales
    # Si se necesita en futuro, implementar con sistema de mensajes global simplificado

    
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
    # 🔄 NAVEGACIÓN DE TABS - ELIMINADO (Sistema sin tabs V4)
    # ==========================================
    # REFACTOR: Sistema de tabs eliminado - intervencion_page.py ahora usa diseño sin tabs
    # active_intervention_tab sigue existiendo como variable legacy (usada en stats)

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
        """
        🎯 SELECCIONAR PACIENTE Y CONSULTA + PREPARAR PARA INTERVENCIÓN

        Flujo completo de atención:
        1. Buscar y cargar paciente + consulta
        2. Cambiar estado de consulta a "en_atencion"
        3. Cargar odontograma última versión del paciente
        4. Cargar intervenciones previas de la consulta
        5. Navegar automáticamente a página de intervención

        Args:
            paciente_id: ID del paciente
            consulta_id: ID de la consulta
        """
        try:
            # 1. Buscar paciente en la lista
            paciente_encontrado = next(
                (p for p in self.pacientes_asignados if p.id == paciente_id),
                None
            )

            # 2. Buscar consulta en la lista
            consulta_encontrada = next(
                (c for c in self.consultas_asignadas if c.id == consulta_id),
                None
            )

            if not paciente_encontrado or not consulta_encontrada:
                logger.warning(f"❌ Paciente o consulta no encontrados: {paciente_id}, {consulta_id}")
                return

            # 3. Establecer como contexto actual
            self.paciente_actual = paciente_encontrado
            self.consulta_actual = consulta_encontrada

            logger.info(f"✅ Paciente seleccionado: {paciente_encontrado.nombre_completo}")

            # 4. Cambiar estado de consulta a "en_atencion" si está "en_espera"
            if consulta_encontrada.estado in ["en_espera", "programada"]:
                from dental_system.state.estado_consultas import EstadoConsultas
                estado_consultas = self.get_state(EstadoConsultas)
                await self.iniciar_atencion_consulta(
                    consulta_id,
                    estado_objetivo="en_atencion"
                )
                logger.info(f"🏥 Consulta cambiada a 'en_atencion'")

            # 5. Cargar odontograma del paciente (última versión)
            await self.cargar_odontograma_paciente_actual()

            # 6. Cargar intervenciones previas de esta consulta
            await self.cargar_intervenciones_consulta_actual()

            # 7. Cargar historial del paciente
            await self.cargar_historial_paciente(paciente_id)

            # 8. Establecer flag de formulario activo
            self.en_formulario_intervencion = True
            self.modo_formulario = "crear"

            # 9. Navegar a página de intervención
            from dental_system.state.estado_ui import EstadoUI
            ui_state = self.get_state(EstadoUI)
            self.navigate_to(
                "intervencion",
                f"Atención Odontológica - {paciente_encontrado.nombre_completo}",
                f"Consulta #{consulta_encontrada.numero_consulta or 'N/A'}"
            )

            logger.info(f"🦷 Navegación a intervención completada")

        except Exception as e:
            logger.error(f"❌ Error en seleccionar_paciente_consulta: {str(e)}")
            from dental_system.state.estado_ui import EstadoUI
            ui_state = self.get_state(EstadoUI)
           
            self.mostrar_toast_error("Error al seleccionar paciente")
    
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
    def estadisticas_odontologo_tiempo_real(self) -> Dict[str, int]:
        """📊 Estadísticas en tiempo real del odontólogo - PATRÓN CONSULTAS PAGE"""
        try:
            # Contar directamente desde self.consultas_asignadas (como en página consultas)
            consultas_del_odontologo = self.consultas_asignadas

            return {
                "pacientes_asignados": len(consultas_del_odontologo),
                "consultas_programadas": len([c for c in consultas_del_odontologo if c.estado in ["programada", "en_espera"]]),
                "consultas_en_progreso": len([c for c in consultas_del_odontologo if c.estado in ["en_progreso", "en_atencion"]]),
                "consultas_completadas": len([c for c in consultas_del_odontologo if c.estado == "completada"]),
                "pacientes_disponibles": len(self.pacientes_disponibles_otros),
                "pacientes_urgentes": len([c for c in consultas_del_odontologo if c.prioridad == "urgente" and c.estado in ["programada", "en_espera", "en_progreso", "en_atencion"]])
            }

        except Exception as e:
            logger.error(f"Error en estadisticas_odontologo_tiempo_real: {e}")
            return {
                "pacientes_asignados": 0,
                "pacientes_disponibles": 0,
                "consultas_programadas": 0,
                "consultas_en_progreso": 0,
                "consultas_completadas": 0,
                "pacientes_urgentes": 0
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
                "ultima_consulta": self.ultima_consulta_info.fecha_llegada if self.ultima_consulta_info else "Sin consultas previas",
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

    # async def seleccionar_diente_superficie(self, numero_diente: int, nombre_superficie: str):
    #     """🔄 FUNCIÓN DE RETROCOMPATIBILIDAD - Usar seleccionar_diente_unificado()"""
    #     await self.seleccionar_diente_unificado(numero_diente, modo="superficie", superficie=nombre_superficie)

    @rx.event
    async def seleccionar_diente(self, numero_diente: int):
        """🔄 FUNCIÓN DE RETROCOMPATIBILIDAD - Usar seleccionar_diente_unificado()"""
        await self.seleccionar_diente_unificado(numero_diente, modo="principal")

    @rx.event
    # ==========================================
    # 🎈 POPOVER ANTIGUO - ELIMINADO (Reemplazado por Sidebar V4)
    # ==========================================
    # REFACTOR: Sistema de popover contextual eliminado - ahora usa tooth_detail_sidebar

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
        
    # MÉTODO REMOVIDO: actualizar_condicion_superficie_actual
    # current_surface_condition es ahora un computed var que se calcula automáticamente

    async def limpiar_odontograma_test(self):
        """🧹 Limpiar odontograma para pruebas"""
        try:
            self.condiciones_por_diente = {}
            self.cambios_pendientes_odontograma = {}
            self.diente_seleccionado = None
            self.superficie_seleccionada = "oclusal"
            print("🧹 Odontograma limpiado para pruebas")
        except Exception as e:
            print(f"❌ Error limpiando odontograma: {e}")

    async def cargar_odontograma_ejemplo(self):
        """📋 Cargar datos de ejemplo para pruebas"""
        try:
            # Datos de ejemplo con algunas condiciones
            ejemplo = {
                11: {"oclusal": "caries", "mesial": "sano", "distal": "sano", "vestibular": "sano", "lingual": "sano"},
                12: {"oclusal": "obturado", "mesial": "sano", "distal": "sano", "vestibular": "sano", "lingual": "sano"},
                21: {"oclusal": "corona", "mesial": "sano", "distal": "sano", "vestibular": "sano", "lingual": "sano"},
                31: {"oclusal": "caries", "mesial": "caries", "distal": "sano", "vestibular": "sano", "lingual": "sano"},
                46: {"oclusal": "endodoncia", "mesial": "sano", "distal": "sano", "vestibular": "sano", "lingual": "sano"}
            }

            self.condiciones_por_diente = ejemplo
            print("📋 Odontograma de ejemplo cargado")
        except Exception as e:
            print(f"❌ Error cargando ejemplo: {e}")

    # ==========================================
    # 🆕 MÉTODOS V2.0 ODONTOGRAMA INTERACTIVO
    # ==========================================

    def toggle_modo_edicion(self):
        """🔄 Alternar entre modo visualización y edición"""
        self.modo_edicion_ui = not self.modo_edicion_ui
        print(f"🔄 Modo cambiado a: {'Edición' if self.modo_edicion_ui else 'Visualización'}")

    def aplicar_filtro_visualizacion(self, tipo: str):
        """🔍 Aplicar filtros específicos de visualización del odontograma"""
        try:
            if tipo == "solo_condiciones":
                self.mostrar_solo_condiciones = not self.mostrar_solo_condiciones
                print(f"🔍 Filtro 'Solo Condiciones': {'ON' if self.mostrar_solo_condiciones else 'OFF'}")

            elif tipo == "solo_criticos":
                self.mostrar_solo_criticos = not self.mostrar_solo_criticos
                print(f"🔍 Filtro 'Solo Críticos': {'ON' if self.mostrar_solo_criticos else 'OFF'}")

            else:
                print(f"⚠️ Tipo de filtro no reconocido: {tipo}")

        except Exception as e:
            print(f"❌ Error aplicando filtro {tipo}: {e}")

    def mostrar_comparador_versiones(self):
        """📊 Mostrar modal comparador de versiones del odontograma"""
        # Por ahora es un placeholder - funcionalidad completa se implementará después
        print("📊 Comparador de versiones - Funcionalidad en desarrollo")
        # self.modal_comparador_versiones_abierto = True  # Se agregará cuando se implemente

    def simular_condiciones_test(self):
        """🎲 Simular condiciones aleatorias para testing"""
        try:
            # Simular algunas condiciones aleatorias para prueba rápida
            import random

            # Dientes de prueba con condiciones variadas
            dientes_prueba = [11, 12, 21, 22, 16, 26, 36, 46]
            condiciones_test = ["caries", "obturado", "corona", "endodoncia", "fractura"]

            for diente in dientes_prueba:
                if random.choice([True, False]):  # 50% probabilidad
                    condicion = random.choice(condiciones_test)
                    superficie = random.choice(["oclusal", "mesial", "distal", "vestibular", "lingual"])

                    # Inicializar diente si no existe
                    if diente not in self.condiciones_por_diente:
                        self.condiciones_por_diente[diente] = {
                            "oclusal": "sano", "mesial": "sano", "distal": "sano",
                            "vestibular": "sano", "lingual": "sano"
                        }

                    self.condiciones_por_diente[diente][superficie] = condicion

            print("🎲 Condiciones de prueba simuladas aleatoriamente")

        except Exception as e:
            print(f"❌ Error simulando condiciones: {e}")

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
            
            # NOTA: current_surface_condition se actualiza automáticamente (computed var)
            
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
        """🔄 FUNCIÓN DE RETROCOMPATIBILIDAD - Usar seleccionar_diente_unificado()"""
        await self.seleccionar_diente_unificado(numero_diente, modo="historial", cargar_historial=True)

    async def cargar_historial_diente_especifico(self, numero_diente: int):
        """📊 Cargar historial real de intervenciones en un diente específico"""
        try:
            if not self.paciente_actual or not self.paciente_actual.id:
                logger.warning("No hay paciente actual seleccionado")
                self.historial_diente_seleccionado = []
                return

            # 🔗 INTEGRACIÓN REAL con BD - Consultar tabla `intervenciones`
            from dental_system.services.odontologia_service import OdontologiaService
            odontologia_service = OdontologiaService()

            # Establecer contexto de usuario
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Obtener historial real del diente específico
            historial_bd = await odontologia_service.get_tooth_specific_history(
                paciente_id=self.paciente_actual.id,
                numero_diente=numero_diente
            )

            if historial_bd:
                # Formatear datos reales para UI
                self.historial_diente_seleccionado = [
                    {
                        "servicio_nombre": item.get("servicio_nombre", "Servicio no especificado"),
                        "fecha_formateada": item.get("fecha_intervencion", "").strftime("%d/%m/%Y") if item.get("fecha_intervencion") else "Sin fecha",
                        "observaciones": item.get("observaciones") or item.get("procedimiento_realizado", "Sin observaciones"),
                        "odontologo_nombre": f"Dr. {item.get('odontologo_nombre', 'Sistema')}",
                        "costo_total": float(item.get('precio_final', 0) or 0),
                        "estado_tratamiento": item.get("estado", "completado"),
                        "materiales_utilizados": item.get("materiales_utilizados", []),
                        "intervencion_id": item.get("id"),
                        "requiere_control": item.get("requiere_control", False)
                    }
                    for item in historial_bd
                ]
                logger.info(f"✅ Historial BD real cargado: {len(self.historial_diente_seleccionado)} intervenciones para diente {numero_diente}")
            else:
                # Sin historial real encontrado
                self.historial_diente_seleccionado = []
                logger.info(f"ℹ️ Sin historial encontrado para diente {numero_diente} del paciente {self.paciente_actual.numero_historia}")

        except Exception as e:
            logger.error(f"❌ Error cargando historial BD del diente {numero_diente}: {e}")
            # Fallback a datos simulados solo en caso de error
            self.historial_diente_seleccionado = [
                {
                    "servicio_nombre": "Error - Datos simulados",
                    "fecha_formateada": "Hoy",
                    "observaciones": f"Error cargando historial real: {str(e)}",
                    "odontologo_nombre": "Dr. Sistema",
                    "costo_total": 0.00,
                    "estado_tratamiento": "error"
                }
            ]

    # ==========================================
    # 🔬 MÉTODOS BD REALES PARA TAB HISTORIAL PROFESIONAL
    # ==========================================

    def obtener_estado_diente_bd_sync(self, numero_diente: int) -> str:
        """🔬 Obtener estado real del diente desde BD (síncrono)"""
        try:
            if not self.paciente_actual or not self.paciente_actual.id:
                return "sano"

            # Consultar última condición del diente desde condiciones_odontograma
            if hasattr(self, 'condiciones_odontograma') and self.condiciones_odontograma:
                condicion_diente = self.condiciones_odontograma.get(numero_diente, {})
                if condicion_diente:
                    # Obtener la condición más reciente (cualquier superficie)
                    for superficie, estado in condicion_diente.items():
                        if estado and estado != "sano":
                            return estado  # Retornar primer estado no sano encontrado
                    return "sano"  # Todas las superficies sanas

            # Fallback: consultar historial disponible
            if hasattr(self, 'historial_diente_seleccionado') and self.diente_seleccionado == numero_diente:
                if self.historial_diente_seleccionado:
                    # Inferir estado desde última intervención
                    ultima_intervencion = self.historial_diente_seleccionado[0]  # Lista ordenada por fecha desc
                    servicio = ultima_intervencion.get("servicio_nombre", "").lower()

                    if "obturacion" in servicio or "restauracion" in servicio:
                        return "obturado"
                    elif "endodoncia" in servicio or "conducto" in servicio:
                        return "endodoncia"
                    elif "corona" in servicio:
                        return "corona"
                    elif "extraccion" in servicio:
                        return "extraccion"
                    elif "implante" in servicio:
                        return "implante"
                    else:
                        return "tratado"  # Genérico para otros tratamientos

            return "sano"  # Por defecto

        except Exception as e:
            logger.warning(f"Error obteniendo estado BD diente {numero_diente}: {e}")
            return "sano"

    @rx.event
    async def obtener_estadisticas_paciente_bd_async(self):
        """📊 Obtener estadísticas reales del paciente desde BD"""
        try:
            if not self.paciente_actual or not self.paciente_actual.id:
                logger.warning("No hay paciente actual para estadísticas")
                return

            from dental_system.services.odontologia_service import OdontologiaService
            odontologia_service = OdontologiaService()
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Obtener estadísticas reales del paciente
            stats_bd = await odontologia_service.get_patient_dental_stats(self.paciente_actual.id)

            if stats_bd:
                # Actualizar variables de estadísticas
                self.estadisticas_paciente_bd = {
                    "dientes_sanos": stats_bd.get("dientes_sanos", 32),
                    "dientes_tratados": stats_bd.get("dientes_tratados", 0),
                    "dientes_criticos": stats_bd.get("dientes_criticos", 0),
                    "total_intervenciones": stats_bd.get("total_intervenciones", 0),
                    "ultima_visita": stats_bd.get("ultima_visita", "Sin visitas"),
                    "proxima_cita": stats_bd.get("proxima_cita", "No programada"),
                    "costo_total_tratamientos": float(stats_bd.get("costo_total", 0))
                }
                logger.info(f"✅ Estadísticas BD cargadas para paciente {self.paciente_actual.numero_historia}")
            else:
                # Estadísticas por defecto si no hay datos
                self.estadisticas_paciente_bd = {
                    "dientes_sanos": 32,
                    "dientes_tratados": 0,
                    "dientes_criticos": 0,
                    "total_intervenciones": 0,
                    "ultima_visita": "Primera visita",
                    "proxima_cita": "No programada",
                    "costo_total_tratamientos": 0.0
                }

        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas BD: {e}")
            # Estadísticas fallback en caso de error
            self.estadisticas_paciente_bd = {
                "dientes_sanos": 30,
                "dientes_tratados": 2,
                "dientes_criticos": 0,
                "total_intervenciones": 0,
                "ultima_visita": "Error cargando datos",
                "proxima_cita": "Consulte con su odontólogo",
                "costo_total_tratamientos": 0.0
            }

    @rx.event
    async def seleccionar_diente_profesional(self, numero_diente: int):
        """🔄 FUNCIÓN DE RETROCOMPATIBILIDAD - Usar seleccionar_diente_unificado()"""
        await self.seleccionar_diente_unificado(numero_diente, modo="profesional", cargar_historial=True, cargar_estadisticas=True)

    # Variable para almacenar estadísticas de BD
    estadisticas_paciente_bd: dict = {}  # Cambió de Dict[str, Any]

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
                        'precio_usd': servicio.precio_base_usd,
                        'precio_bs': servicio.precio_base_bs,
                        'total_usd': servicio.precio_base_usd * 1,
                        'total_bs': servicio.precio_base_bs * 1
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

    # ==========================================
    # 🦷 COMPUTED VARS PARA HISTORIAL CON COLORES REALES
    # ==========================================

    # Diccionario de colores por condición de diente
    COLORES_CONDICIONES_HISTORIAL = {
        "sano": "#22C55E",        # Verde brillante
        "caries": "#EF4444",      # Rojo
        "obturacion": "#3B82F6",  # Azul
        "corona": "#F59E0B",      # Naranja/Dorado
        "puente": "#A855F7",      # Púrpura
        "implante": "#10B981",    # Verde esmeralda
        "ausente": "#6B7280",     # Gris
        "extraccion_indicada": "#F87171",  # Rojo claro
        "endodoncia": "#8B5CF6",  # Púrpura claro
        "protesis": "#EC4899",    # Rosa
        "fractura": "#DC2626",    # Rojo oscuro
        "mancha": "#FBBF24",      # Amarillo
        "desgaste": "#F97316",    # Naranja
        "sensibilidad": "#06B6D4", # Cian
        "movilidad": "#EF4444"     # Rojo
    }

    def color_diente_historial(self, numero_diente: int) -> str:
        """🦷 Color del diente basado en la condición real de la BD"""
        try:
            # Obtener condición actual del diente desde el odontograma cargado
            if hasattr(self, 'condiciones_odontograma') and self.condiciones_odontograma:
                condicion = self.condiciones_odontograma.get(str(numero_diente), {}).get("tipo_condicion", "sano")
                return self.COLORES_CONDICIONES_HISTORIAL.get(condicion, self.COLORES_CONDICIONES_HISTORIAL["sano"])

            # Si no hay condiciones cargadas, usar color por defecto
            return self.COLORES_CONDICIONES_HISTORIAL["sano"]

        except Exception as e:
            logger.error(f"Error obteniendo color diente {numero_diente}: {str(e)}")
            return self.COLORES_CONDICIONES_HISTORIAL["sano"]

    async def cargar_condiciones_historial_paciente(self, paciente_id: str):
        """🦷 Cargar condiciones reales del odontograma para historial"""
        try:
            from dental_system.supabase.tablas.condiciones_diente import condiciones_diente_table
            from dental_system.supabase.tablas.odontograma import odontograms_table

            # Obtener odontograma actual del paciente
            if not paciente_id or paciente_id.strip() == "":
                logger.warning("ID de paciente no válido para cargar condiciones del historial")
                self.condiciones_odontograma = {}
                return

            odontograma_actual = await odontograms_table.get_active_odontogram(paciente_id)

            if not odontograma_actual:
                logger.warning(f"No se encontró odontograma para paciente {paciente_id}")
                self.condiciones_odontograma = {}
                return

            # Obtener todas las condiciones actuales
            condiciones = await condiciones_diente_table.get_by_odontograma(odontograma_actual["id"])

            # Convertir a diccionario indexado por número de diente
            condiciones_dict = {}
            for condicion in condiciones:
                numero_diente = condicion.get("diente", {}).get("numero_diente")
                if numero_diente:
                    condiciones_dict[str(numero_diente)] = {
                        "tipo_condicion": condicion.get("tipo_condicion", "sano"),
                        "descripcion": condicion.get("descripcion", ""),
                        "material_utilizado": condicion.get("material_utilizado", ""),
                        "fecha_tratamiento": condicion.get("fecha_tratamiento"),
                        "observaciones": condicion.get("observaciones", "")
                    }

            self.condiciones_odontograma = condiciones_dict
            logger.info(f"✅ Condiciones del historial cargadas: {len(condiciones_dict)} dientes")

        except Exception as e:
            logger.error(f"Error cargando condiciones del historial: {str(e)}")
            self.condiciones_odontograma = {}



    @rx.event
    async def inicializar_historial_paciente(self):
        """🦷 Inicializar historial cargando condiciones del paciente actual"""
        try:
            if self.paciente_actual.id:
                await self.cargar_condiciones_historial_paciente(self.paciente_actual.id)
                logger.info(f"Historial inicializado para paciente {self.paciente_actual.numero_historia}")
        except Exception as e:
            logger.error(f"Error inicializando historial: {str(e)}")

    # 🦷 COMPUTED VARS PROFESIONALES - BD REAL
    # ==========================================

    @rx.var(cache=True)
    def historial_diente_disponible(self) -> bool:
        """✅ Verificar si hay historial disponible para el diente seleccionado"""
        return (
            self.diente_seleccionado is not None and
            bool(self.historial_diente_seleccionado) and
            not self.cargando_odontograma_historial
        )

    @rx.var(cache=True)
    def estadisticas_paciente_resumen(self) -> Dict[str, Any]:
        """📊 Resumen estadísticas del paciente actual con datos BD"""
        if not (hasattr(self.paciente_actual, 'id') and self.paciente_actual.id):
            return {
                "total_intervenciones": 0,
                "ultima_visita": "N/A",
                "dientes_afectados": 0,
                "total_gastado": "$0"
            }

        # Usar datos reales de BD si están disponibles
        if self.estadisticas_paciente_bd:
            return {
                "total_intervenciones": self.estadisticas_paciente_bd.get("total_intervenciones", 0),
                "ultima_visita": self.estadisticas_paciente_bd.get("ultima_visita", "N/A"),
                "dientes_afectados": self.estadisticas_paciente_bd.get("dientes_tratados", 0),
                "total_gastado": f"${self.estadisticas_paciente_bd.get('total_gastado', 0):,.2f}"
            }

        return {
            "total_intervenciones": 0,
            "ultima_visita": "Cargando...",
            "dientes_afectados": 0,
            "total_gastado": "$0"
        }

    @rx.var(cache=True)
    def odontograma_tiene_cambios(self) -> bool:
        """🔄 Verificar si el odontograma tiene cambios pendientes"""
        return bool(self.cambios_pendientes_odontograma)

    @rx.var(cache=True)
    def diente_seleccionado_nombre(self) -> str:
        """📋 Nombre descriptivo del diente seleccionado (sistema FDI)"""
        if not self.diente_seleccionado:
            return "Ningún diente seleccionado"

        nombres_dientes = {
            # Cuadrante 1 (Superior Derecho)
            11: "Incisivo Central Superior Derecho", 12: "Incisivo Lateral Superior Derecho",
            13: "Canino Superior Derecho", 14: "Primer Premolar Superior Derecho",
            15: "Segundo Premolar Superior Derecho", 16: "Primer Molar Superior Derecho",
            17: "Segundo Molar Superior Derecho", 18: "Tercer Molar Superior Derecho",

            # Cuadrante 2 (Superior Izquierdo)
            21: "Incisivo Central Superior Izquierdo", 22: "Incisivo Lateral Superior Izquierdo",
            23: "Canino Superior Izquierdo", 24: "Primer Premolar Superior Izquierdo",
            25: "Segundo Premolar Superior Izquierdo", 26: "Primer Molar Superior Izquierdo",
            27: "Segundo Molar Superior Izquierdo", 28: "Tercer Molar Superior Izquierdo",

            # Cuadrante 3 (Inferior Izquierdo)
            31: "Incisivo Central Inferior Izquierdo", 32: "Incisivo Lateral Inferior Izquierdo",
            33: "Canino Inferior Izquierdo", 34: "Primer Premolar Inferior Izquierdo",
            35: "Segundo Premolar Inferior Izquierdo", 36: "Primer Molar Inferior Izquierdo",
            37: "Segundo Molar Inferior Izquierdo", 38: "Tercer Molar Inferior Izquierdo",

            # Cuadrante 4 (Inferior Derecho)
            41: "Incisivo Central Inferior Derecho", 42: "Incisivo Lateral Inferior Derecho",
            43: "Canino Inferior Derecho", 44: "Primer Premolar Inferior Derecho",
            45: "Segundo Premolar Inferior Derecho", 46: "Primer Molar Inferior Derecho",
            47: "Segundo Molar Inferior Derecho", 48: "Tercer Molar Inferior Derecho"
        }

        return nombres_dientes.get(self.diente_seleccionado, f"Diente #{self.diente_seleccionado}")

    @rx.var(cache=True)
    def cuadrante_diente_seleccionado(self) -> int:
        """📍 Cuadrante del diente seleccionado (1-4)"""
        if not self.diente_seleccionado:
            return 0

        if self.diente_seleccionado in self.cuadrante_1:
            return 1
        elif self.diente_seleccionado in self.cuadrante_2:
            return 2
        elif self.diente_seleccionado in self.cuadrante_3:
            return 3
        elif self.diente_seleccionado in self.cuadrante_4:
            return 4
        else:
            return 0

    @rx.var(cache=True)
    def puede_mostrar_historial(self) -> bool:
        """🔍 Verificar si se puede mostrar el tab de historial"""
        return (
            (hasattr(self.paciente_actual, 'id') and bool(self.paciente_actual.id)) and
            self.diente_seleccionado is not None and
            not self.cargando_odontograma_historial
        )

    @rx.var(cache=True)
    def color_diente_actual(self) -> str:
        """🎨 Color del diente seleccionado según su estado"""
        if not self.diente_seleccionado:
            return "#ffffff"  # Blanco por defecto

        return self.obtener_color_diente(self.diente_seleccionado)

    @rx.var(cache=True)
    def resumen_historial_diente(self) -> str:
        """📄 Resumen del historial del diente seleccionado"""
        if not self.historial_diente_seleccionado:
            return "Sin historial registrado"

        total_intervenciones = len(self.historial_diente_seleccionado)
        if total_intervenciones == 0:
            return "Sin intervenciones registradas"
        elif total_intervenciones == 1:
            return "1 intervención registrada"
        else:
            return f"{total_intervenciones} intervenciones registradas"

    # ==========================================
    # 🚀 MÉTODOS V2.0 - ODONTOGRAMA INTERACTIVO
    # ==========================================

    @rx.event
    async def cargar_odontograma_paciente_actual(self):
        """🔄 Cargar odontograma del paciente actual con datos reales"""
        if not self.paciente_actual.id:
            logger.warning("No hay paciente actual seleccionado")
            return

        try:
            self.odontograma_cargando = True
            self.odontograma_error = ""

            logger.info(f"🔄 Cargando odontograma para paciente: {self.paciente_actual.id}")

            # Usar id_personal del odontólogo (accesible directamente vía mixin=True)
            # Preferir id_personal (tabla personal) sobre id_usuario
            personal_id = self.id_personal if self.id_personal else self.id_usuario

            # Llamar al servicio para obtener/crear odontograma
            odontograma_data = await odontologia_service.get_or_create_patient_odontogram(
                self.paciente_actual.id,
                personal_id
            )

            if odontograma_data:
                # Actualizar datos del odontograma
                self.odontograma_actual = OdontogramaModel.from_dict(odontograma_data)

                # Cargar condiciones organizadas por diente y superficie
                self.condiciones_por_diente = odontograma_data.get("conditions", {})

                # Resetear cambios pendientes
                self.cambios_pendientes_odontograma = {}
                self.cambios_sin_guardar = False

                logger.info(f"✅ Odontograma cargado - Versión: {odontograma_data.get('version', 1)}")

                # NUEVO V4.0: Cargar datos para timeline
                self.intervenciones_paciente = await odontologia_service.get_patient_interventions(
                    self.paciente_actual.id
                )
                self.dentistas_paciente = await odontologia_service.get_patient_dentists(
                    self.paciente_actual.id
                )
                self.procedimientos_paciente = await odontologia_service.get_patient_procedures(
                    self.paciente_actual.id
                )

                logger.info(f"✅ Timeline cargado: {len(self.intervenciones_paciente)} intervenciones")

            else:
                logger.warning("No se pudo cargar/crear odontograma")
                self.odontograma_error = "Error cargando odontograma"

            # ✅ ACTIVAR TIMELINE AUTOMÁTICAMENTE cuando hay datos
            if self.intervenciones_paciente:
                self.show_timeline = True
                logger.info(f"✅ Timeline activado automáticamente - {len(self.intervenciones_paciente)} intervenciones")

        except Exception as e:
            logger.error(f"❌ Error cargando odontograma: {str(e)}")
            self.odontograma_error = f"Error: {str(e)}"
        finally:
            self.odontograma_cargando = False

    @rx.event
    def seleccionar_diente_superficie(self, tooth_number: int, surface: str):
        """👆 Seleccionar diente y superficie específica para edición"""

        # NOTA: No validamos permisos aquí porque ya se validaron a nivel de ruta
        # Si el usuario llegó a la página de intervención, ya tiene permisos de odontólogo
        # Validación redundante eliminada para mejorar UX

        self.diente_seleccionado = tooth_number
        self.superficie_seleccionada = surface

        # Abrir modal de condiciones
        self.modal_condiciones_abierto = True

        logger.info(f"👆 Seleccionado: Diente {tooth_number}, Superficie {surface}")

    @rx.event
    def cerrar_modal_condiciones(self):
        """❌ Cerrar modal de selección de condiciones"""
        self.modal_condiciones_abierto = False
        self.condicion_seleccionada_temp = "sano"

    @rx.event
    def seleccionar_condicion_temporal(self, condicion: str):
        """🎯 Seleccionar condición temporal para aplicar"""
        self.condicion_seleccionada_temp = condicion

    @rx.event
    async def aplicar_condicion_seleccionada(self):
        """💾 Aplicar condición seleccionada al diente/superficie"""
        if not (self.diente_seleccionado and self.superficie_seleccionada and self.condicion_seleccionada_temp):
            logger.warning("Datos incompletos para aplicar condición")
            return

        try:
            # Actualizar en estado local
            if self.diente_seleccionado not in self.condiciones_por_diente:
                self.condiciones_por_diente[self.diente_seleccionado] = {}

            self.condiciones_por_diente[self.diente_seleccionado][self.superficie_seleccionada] = self.condicion_seleccionada_temp

            # Marcar como cambio pendiente
            if self.diente_seleccionado not in self.cambios_pendientes_odontograma:
                self.cambios_pendientes_odontograma[self.diente_seleccionado] = {}

            self.cambios_pendientes_odontograma[self.diente_seleccionado][self.superficie_seleccionada] = self.condicion_seleccionada_temp
            self.cambios_sin_guardar = True

            # Cerrar modal
            self.modal_condiciones_abierto = False

            logger.info(f"✅ Condición '{self.condicion_seleccionada_temp}' aplicada a diente {self.diente_seleccionado} - {self.superficie_seleccionada}")

            # Auto-guardar (opcional - puede quitarse para guardar manual)
            await self.guardar_cambios_odontograma()

        except Exception as e:
            logger.error(f"❌ Error aplicando condición: {str(e)}")
            self.odontograma_error = f"Error aplicando condición: {str(e)}"

    async def guardar_cambios_odontograma(self):
        """💾 Guardar cambios pendientes del odontograma en BD (método helper sin @rx.event)"""
        if not self.cambios_pendientes_odontograma:
            logger.info("No hay cambios pendientes para guardar")
            return

        try:
            self.odontograma_guardando = True
            self.odontograma_error = ""

            # Guardar cambios usando el servicio
            success = await odontologia_service.save_odontogram_conditions(
                self.odontograma_actual.id,
                self.cambios_pendientes_odontograma
            )

            if success:
                # Limpiar cambios pendientes
                self.cambios_pendientes_odontograma = {}
                self.cambios_sin_guardar = False

                logger.info("✅ Cambios del odontograma guardados exitosamente")
            else:
                raise ValueError("Error guardando en base de datos")

        except PermissionError as e:
            # Error de permisos - mensaje específico
            error_msg = str(e)
            logger.error(f"❌ {error_msg}")
            self.odontograma_error = error_msg
            self.mostrar_toast(f"⚠️ Sin Permisos: {error_msg}", "error")
        except Exception as e:
            # Otros errores
            logger.error(f"❌ Error guardando odontograma: {str(e)}")
            self.odontograma_error = f"Error guardando cambios: {str(e)}"
            self.mostrar_toast(f"Error al guardar: {str(e)}", "error")
        finally:
            self.odontograma_guardando = False

    # ==========================================
    # 🆕 MÉTODOS NUEVA ESTRUCTURA
    # ==========================================

    # ─────────────────────────────────────────
    # MODALES
    # ─────────────────────────────────────────

    def toggle_add_intervention_modal(self):
        """Toggle modal agregar intervención"""
        self.show_add_intervention_modal = not self.show_add_intervention_modal

    def open_add_intervention_modal(self):
        """Abrir modal agregar intervención"""
        self.show_add_intervention_modal = True
        # Resetear formulario
        self.selected_service_name = ""
        self.superficie_oclusal_selected = False
        self.superficie_mesial_selected = False
        self.superficie_distal_selected = False
        self.superficie_vestibular_selected = False
        self.superficie_lingual_selected = False
        self.auto_change_condition = False
        self.new_condition_value = ""
        self.intervention_observations = ""

    def toggle_change_condition_modal(self):
        """Toggle modal cambiar condición"""
        self.show_change_condition_modal = not self.show_change_condition_modal

    # ─────────────────────────────────────────
    # SUPERFICIES (CHECKBOXES)
    # ─────────────────────────────────────────

    def toggle_superficie_oclusal(self, checked: bool):
        """Toggle superficie oclusal"""
        self.superficie_oclusal_selected = checked

    def toggle_superficie_mesial(self, checked: bool):
        """Toggle superficie mesial"""
        self.superficie_mesial_selected = checked

    def toggle_superficie_distal(self, checked: bool):
        """Toggle superficie distal"""
        self.superficie_distal_selected = checked

    def toggle_superficie_vestibular(self, checked: bool):
        """Toggle superficie vestibular"""
        self.superficie_vestibular_selected = checked

    def toggle_superficie_lingual(self, checked: bool):
        """Toggle superficie lingual"""
        self.superficie_lingual_selected = checked

    # ─────────────────────────────────────────
    # OTROS SETTERS
    # ─────────────────────────────────────────

    def toggle_auto_change_condition(self, checked: bool):
        """Toggle cambio automático de condición"""
        self.auto_change_condition = checked

    def set_new_condition_value(self, value: str):
        """Setear nueva condición"""
        self.new_condition_value = value

    def set_intervention_observations(self, value: str):
        """Setear observaciones"""
        self.intervention_observations = value

    def set_selected_service_name(self, value: str):
        """Setear servicio seleccionado"""
        self.selected_service_name = value

    def set_quick_surface_selected(self, value: str):
        """Setear superficie seleccionada (cambio rápido)"""
        self.quick_surface_selected = value

    def set_quick_condition(self, condition: str):
        """Setear condición (cambio rápido)"""
        self.quick_condition_value = condition

    # ─────────────────────────────────────────
    # GUARDAR SERVICIOS
    # ─────────────────────────────────────────

    @rx.event
    async def save_intervention_to_consultation(self):
        """
        💾 Agregar servicio a lista temporal de consulta actual

        NO guarda en BD aún, solo agrega a self.servicios_consulta_actual
        Se guardará cuando se complete la consulta
        """
        try:
            # Validar datos
            if not self.selected_service_name:
                self.mostrar_toast("Selecciona un servicio", "warning")
                return

            if not self.selected_tooth:
                self.mostrar_toast("Selecciona un diente", "warning")
                return

            # Recopilar superficies seleccionadas
            superficies = []
            if self.superficie_oclusal_selected:
                superficies.append("Oclusal")
            if self.superficie_mesial_selected:
                superficies.append("Mesial")
            if self.superficie_distal_selected:
                superficies.append("Distal")
            if self.superficie_vestibular_selected:
                superficies.append("Vestibular")
            if self.superficie_lingual_selected:
                superficies.append("Lingual")

            if not superficies:
                self.mostrar_toast("Selecciona al menos una superficie", "warning")
                return

            # Crear dict del servicio
            import uuid

            # Obtener ID del servicio del catálogo
            servicio_id = self.selected_service_id
            logger.info(f"📝 Creando servicio: '{self.selected_service_name}' con ID: {servicio_id}")

            if not servicio_id:
                self.mostrar_toast("⚠️ Error: No se encontró el servicio en el catálogo", "error")
                logger.error(f"❌ Servicio '{self.selected_service_name}' sin ID. Servicios disponibles: {len(self.servicios_disponibles)}")
                return

            servicio = {
                "id": str(uuid.uuid4()),  # ID temporal para la UI
                "servicio_id": servicio_id,  # ID real del catálogo
                "diente": self.selected_tooth,
                "servicio": self.selected_service_name,
                "superficies": superficies,
                "costo_bs": self.selected_service_cost_bs,
                "costo_usd": self.selected_service_cost_usd,
                "observaciones": self.intervention_observations,
            }

            # Agregar a lista
            self.servicios_consulta_actual.append(servicio)
            logger.info(f"✅ Servicio agregado a lista: {servicio}")

            # Actualizar flag de servicios seleccionados
            self.tiene_servicios_seleccionados = len(self.servicios_consulta_actual) > 0

            # Si auto_change_condition, actualizar condiciones
            if self.auto_change_condition and self.new_condition_value:
                if self.selected_tooth not in self.condiciones_por_diente:
                    self.condiciones_por_diente[self.selected_tooth] = {}

                for superficie in superficies:
                    self.condiciones_por_diente[self.selected_tooth][superficie.lower()] = self.new_condition_value

                # Guardar en BD
                await self.guardar_cambios_odontograma()

            # Cerrar modal
            self.show_add_intervention_modal = False
            self.mostrar_toast("Servicio agregado exitosamente", "success")

        except Exception as e:
            logger.error(f"❌ Error agregando servicio: {str(e)}")
            self.mostrar_toast(f"Error: {str(e)}", "error")

    @rx.event
    async def apply_quick_condition_change(self):
        """
        🔄 Cambiar condición del diente (cambio rápido)

        Guarda directamente en BD
        """
        try:
            # Validar
            if not self.selected_tooth:
                self.mostrar_toast("Selecciona un diente", "warning")
                return

            if not self.quick_surface_selected:
                self.mostrar_toast("Selecciona una superficie", "warning")
                return

            if not self.quick_condition_value:
                self.mostrar_toast("Selecciona una condición", "warning")
                return

            # Actualizar en memoria
            if self.selected_tooth not in self.condiciones_por_diente:
                self.condiciones_por_diente[self.selected_tooth] = {}

            self.condiciones_por_diente[self.selected_tooth][self.quick_surface_selected] = self.quick_condition_value

            # Guardar en BD
            await self.guardar_cambios_odontograma()

            # Cerrar modal
            self.show_change_condition_modal = False
            self.mostrar_toast("Condición actualizada", "success")

        except Exception as e:
            logger.error(f"❌ Error cambiando condición: {str(e)}")
            self.mostrar_toast(f"Error: {str(e)}", "error")

    @rx.event
    async def edit_consultation_service(self, service_id: str):
        """✏️ Editar servicio de la consulta actual"""
        # TODO: Implementar edición
        self.mostrar_toast("Edición próximamente", "info")

    @rx.event
    async def delete_consultation_service(self, service_id: str):
        """🗑️ Eliminar servicio de la consulta actual"""
        self.servicios_consulta_actual = [
            s for s in self.servicios_consulta_actual
            if s.get("id") != service_id
        ]
        # Actualizar flag
        self.tiene_servicios_seleccionados = len(self.servicios_consulta_actual) > 0
        self.mostrar_toast("Servicio eliminado", "success")

    @rx.event
    def set_hover_diente(self, tooth_number: Optional[int]):
        """🖱️ Establecer diente en hover para efectos visuales"""
        self.diente_hover = tooth_number

    @rx.event
    def set_hover_superficie(self, surface: Optional[str]):
        """🖱️ Establecer superficie en hover para efectos visuales"""
        self.superficie_hover = surface

    # ==========================================
    # 🎨 COMPUTED VARS V2.0 - COLORES Y VISUAL
    # ==========================================

   
    def get_surface_color(self, tooth_number: int, surface: str) -> str:
        """🎨 Obtener color de superficie específica según condición"""
        # Verificar cambios pendientes primero
        if tooth_number in self.cambios_pendientes_odontograma:
            pending_condition = self.cambios_pendientes_odontograma[tooth_number].get(surface)
            if pending_condition:
                return self.condiciones_disponibles.get(pending_condition, {}).get("color", "#90EE90")

        # Verificar condiciones guardadas
        if tooth_number in self.condiciones_por_diente:
            current_condition = self.condiciones_por_diente[tooth_number].get(surface, "sano")
            return self.condiciones_disponibles.get(current_condition, {}).get("color", "#90EE90")

        # Por defecto: sano
        return "#90EE90"

    @rx.var
    def odontograma_status_message(self) -> str:
        """📊 Mensaje de estado del odontograma"""
        if self.odontograma_cargando:
            return "🔄 Cargando odontograma..."
        elif self.odontograma_guardando:
            return "💾 Guardando cambios..."
        elif self.odontograma_error:
            return f"❌ {self.odontograma_error}"
        elif self.cambios_sin_guardar:
            return f"⚠️ {len(self.cambios_pendientes_odontograma)} cambios sin guardar"
        else:
            return "✅ Odontograma sincronizado"

    @rx.var
    def condiciones_disponibles_lista(self) -> List[Dict[str, str]]:
        """📋 Lista de condiciones disponibles para el selector"""
        return [
            {
                "key": key,
                "color": value["color"],
                "descripcion": value["descripcion"],
                "simbolo": value["simbolo"]
            }
            for key, value in self.condiciones_disponibles.items()
        ]

    @rx.var
    def condiciones_disponibles_ui(self) -> List[Dict[str, str]]:
        """🎨 Lista de condiciones formateada específicamente para UI V2.0"""
        return [
            {
                "nombre": value["descripcion"],
                "color": value["color"],
                "codigo": key
            }
            for key, value in self.condiciones_disponibles.items()
        ]

    @rx.var
    def current_surface_condition(self) -> str:
        """🦷 Condición actual de la superficie seleccionada"""
        if not (self.diente_seleccionado and self.superficie_seleccionada):
            return "sano"

        # Verificar condiciones guardadas
        if self.diente_seleccionado in self.condiciones_por_diente:
            return self.condiciones_por_diente[self.diente_seleccionado].get(self.superficie_seleccionada, "sano")

        return "sano"

    @rx.var
    def dientes_por_cuadrante(self) -> Dict[str, List[int]]:
        """🦷 Diccionario de dientes organizados por cuadrante FDI"""
        return {
            "cuadrante_1": self.cuadrante_1,
            "cuadrante_2": self.cuadrante_2,
            "cuadrante_3": self.cuadrante_3,
            "cuadrante_4": self.cuadrante_4
        }

    @rx.var
    def estadisticas_resumen(self) -> Dict[str, int]:
        """📊 Estadísticas resumidas del odontograma actual"""
        if not self.condiciones_por_diente:
            return {
                "dientes_sanos": 32,
                "dientes_afectados": 0,
                "condiciones_criticas": 0
            }

        dientes_con_condiciones = set()
        condiciones_criticas = 0
        condiciones_criticas_tipos = {"caries", "fractura", "ausente"}

        for diente, superficies in self.condiciones_por_diente.items():
            for superficie, condicion in superficies.items():
                if condicion != "sano":
                    dientes_con_condiciones.add(diente)
                    if condicion in condiciones_criticas_tipos:
                        condiciones_criticas += 1

        dientes_afectados = len(dientes_con_condiciones)
        dientes_sanos = 32 - dientes_afectados

        return {
            "dientes_sanos": dientes_sanos,
            "dientes_afectados": dientes_afectados,
            "condiciones_criticas": condiciones_criticas
        }

    @rx.var
    def ultima_intervencion_fecha(self) -> str:
        """📅 Fecha de la última intervención (simplificada)"""
        # Por ahora retorna "today" o "Ver historial"
        # En el futuro se puede conectar con el servicio para obtener fecha real
        return "today" if self.cambios_sin_guardar else "Ver historial"

    # ==========================================
    # 🎛️ MÉTODOS DE CONTROL PROFESIONAL
    # ==========================================

    @rx.event
    def nueva_intervencion(self):
        """➕ Iniciar nueva intervención odontológica"""
        # TODO: Implementar navegación a página de intervención
        yield rx.toast.info(
            "Nueva Intervención",
            description="Funcionalidad en desarrollo",
            duration=3000
        )

    @rx.event
    def mostrar_historial_odontograma(self):
        """📜 Mostrar historial completo del odontograma"""
        # TODO: Implementar modal o página de historial
        yield rx.toast.info(
            "Historial",
            description="Funcionalidad en desarrollo",
            duration=3000
        )

    @rx.event
    def exportar_odontograma_pdf(self):
        """📄 Exportar odontograma a PDF"""
        # TODO: Implementar generación de PDF
        yield rx.toast.info(
            "Exportar PDF",
            description="Funcionalidad en desarrollo",
            duration=3000
        )

    # ==========================================
    # 🌟 EVENTOS V4.0 - NUEVO DISEÑO PROFESIONAL
    # ==========================================

    @rx.event
    def select_tooth(self, tooth_number: int):
        """
        🦷 Seleccionar un diente del odontograma

        Args:
            tooth_number: Número FDI del diente (11-48)
        """
        self.selected_tooth = tooth_number
        self.active_sidebar_tab = "historial"  # Resetear a tab historial
        logger.info(f"✅ Diente {tooth_number} seleccionado")

    @rx.event
    def close_sidebar(self):
        """📭 Cerrar panel lateral de detalles"""
        self.selected_tooth = None
        logger.info("✅ Sidebar cerrado")

    @rx.event
    def change_sidebar_tab(self, tab_name: str):
        """
        🔄 Cambiar tab del sidebar

        Args:
            tab_name: Nombre del tab ("historial" | "info")
        """
        self.active_sidebar_tab = tab_name
        logger.info(f"✅ Tab cambiado a: {tab_name}")

    @rx.event
    def toggle_timeline(self):
        """⏱️ Mostrar/ocultar timeline de intervenciones"""
        self.show_timeline = not self.show_timeline
        logger.info(f"✅ Timeline {'mostrado' if self.show_timeline else 'ocultado'}")

    @rx.event
    def update_timeline_filter(self, filter_type: str, value: str):
        """
        🔍 Actualizar filtros del timeline

        Args:
            filter_type: Tipo de filtro ("dentist" | "procedure" | "period")
            value: Valor del filtro
        """
        if filter_type == "dentist":
            self.timeline_filter_dentist = value
        elif filter_type == "procedure":
            self.timeline_filter_procedure = value
        elif filter_type == "period":
            self.timeline_filter_period = value

        logger.info(f"✅ Filtro {filter_type} actualizado a: {value}")

    # ============================================================================
    # 🛠️ MÉTODOS DE GESTIÓN DE SERVICIOS PARA INTERVENCIONES (V4.0)
    # ============================================================================

    @rx.event
    def agregar_servicio_a_intervencion(self, servicio_id: str, nombre_servicio: str,
                                       precio_bs: float, precio_usd: float, dientes: List[int]):
        """➕ Agregar servicio con dientes específicos a la intervención actual"""
        try:
            nuevo_servicio = {
                "id_servicio": servicio_id,
                "nombre": nombre_servicio,
                "precio_bs": precio_bs,
                "precio_usd": precio_usd,
                "dientes": dientes,
                "cantidad": len(dientes) if dientes else 1,
            }

            self.servicios_intervencion.append(nuevo_servicio)
            self.recalcular_totales()
            self.tiene_servicios_seleccionados = True

            logger.info(f"✅ Servicio '{nombre_servicio}' agregado a intervención para dientes: {dientes}")

        except Exception as e:
            logger.error(f"❌ Error agregando servicio a intervención: {str(e)}")

    @rx.event
    def quitar_servicio_de_intervencion(self, index: int):
        """➖ Quitar servicio de la lista de intervención"""
        try:
            if 0 <= index < len(self.servicios_intervencion):
                servicio_removido = self.servicios_intervencion.pop(index)
                self.recalcular_totales()

                # Actualizar flag de servicios
                self.tiene_servicios_seleccionados = len(self.servicios_intervencion) > 0

                logger.info(f"✅ Servicio '{servicio_removido.get('nombre')}' removido de intervención")
            else:
                logger.warning(f"⚠️ Índice inválido para quitar servicio: {index}")

        except Exception as e:
            logger.error(f"❌ Error quitando servicio de intervención: {str(e)}")

    @rx.event
    def recalcular_totales(self):
        """🧮 Recalcular totales de la intervención según servicios agregados"""
        try:
            total_bs = 0.0
            total_usd = 0.0

            for servicio in self.servicios_intervencion:
                cantidad = servicio.get("cantidad", 1)
                total_bs += servicio.get("precio_bs", 0.0) * cantidad
                total_usd += servicio.get("precio_usd", 0.0) * cantidad

            self.total_bs_intervencion = round(total_bs, 2)
            self.total_usd_intervencion = round(total_usd, 2)

            logger.info(f"✅ Totales recalculados: BS {self.total_bs_intervencion} | USD {self.total_usd_intervencion}")

        except Exception as e:
            logger.error(f"❌ Error recalculando totales: {str(e)}")
            self.total_bs_intervencion = 0.0
            self.total_usd_intervencion = 0.0

    @rx.event
    def marcar_cambio_odontograma(self, diente: int, condicion: str):
        """🦷 Marcar cambio en odontograma y activar flag para guardado"""
        try:
            # Actualizar condición del diente (simplificado para V4.0 - 1 diente = 1 condición)
            self.condiciones_por_diente[str(diente)] = {
                "general": condicion
            }

            # Activar flags de cambios
            self.tiene_cambios_odontograma = True

            logger.info(f"✅ Cambio marcado en diente {diente}: {condicion}")

        except Exception as e:
            logger.error(f"❌ Error marcando cambio en odontograma: {str(e)}")

    @rx.event
    def limpiar_intervencion_actual(self):
        """🧹 Limpiar datos de intervención actual (reset para nueva intervención)"""
        try:
            # Limpiar servicios antiguos
            self.servicios_intervencion = []
            self.total_bs_intervencion = 0.0
            self.total_usd_intervencion = 0.0

            # Limpiar servicios nuevos (V4.0)
            self.servicios_consulta_actual = []

            # Limpiar flags y estado
            self.tiene_cambios_odontograma = False
            self.tiene_servicios_seleccionados = False
            self.selected_tooth = None
            self.selected_service_name = ""

            logger.info("✅ Datos de intervención limpiados (incluye servicios_consulta_actual)")

        except Exception as e:
            logger.error(f"❌ Error limpiando intervención: {str(e)}")

    # ============================================================================
    # 💾 MÉTODOS DE GUARDADO - DUAL WORKFLOW (V4.0)
    # ============================================================================

    @rx.event(background=True)
    async def guardar_solo_diagnostico_odontograma(self):
        """💾 WORKFLOW A: Guardar solo cambios en odontograma SIN crear intervención"""
        async with self:
            if not self.tiene_cambios_odontograma:
                logger.warning("⚠️ No hay cambios en odontograma para guardar")
                return

            if not self.paciente_actual.id:
                logger.error("❌ No hay paciente actual seleccionado")
                return

            try:
                self.odontograma_guardando = True
                logger.info("💾 Guardando solo diagnóstico (sin intervención)...")

                # Obtener odontograma actual o crear uno nuevo
                odontograma_id = self.odontograma_actual.id if self.odontograma_actual else None

                if not odontograma_id:
                    # Crear nuevo odontograma para el paciente
                    personal_id = self.id_personal if self.id_personal else self.id_usuario
                    odontograma_data = await odontologia_service.get_or_create_patient_odontogram(
                        self.paciente_actual.id,
                        personal_id
                    )
                    odontograma_id = odontograma_data.get("id") if odontograma_data else None

                if not odontograma_id:
                    logger.error("❌ No se pudo obtener/crear odontograma")
                    return

                # Guardar condiciones de dientes modificados
                for diente_num, condiciones in self.condiciones_por_diente.items():
                    for superficie, condicion in condiciones.items():
                        await odontologia_service.save_tooth_condition(
                            odontograma_id=odontograma_id,
                            tooth_number=int(diente_num),
                            surface=superficie,
                            condition=condicion
                        )

                # Resetear flags
                self.tiene_cambios_odontograma = False
                logger.info("✅ Diagnóstico guardado exitosamente (sin intervención)")

            except Exception as e:
                logger.error(f"❌ Error guardando diagnóstico: {str(e)}")
            finally:
                self.odontograma_guardando = False

    @rx.event(background=True)
    async def guardar_intervencion_completa(self):
        """
        💾 FINALIZAR INTERVENCIÓN DEL ODONTÓLOGO ACTUAL

        FLUJO COMPLETO:
        1. Guardar intervención con servicios en BD
        2. Actualizar odontograma con nueva versión
        3. Cambiar estado consulta a "entre_odontologos" o "completada"
        4. Navegar de vuelta a lista de pacientes
        """
        async with self:
            # Validaciones
            if not self.servicios_consulta_actual:
                self.mostrar_toast("⚠️ No hay servicios para guardar", "warning")
                logger.warning("⚠️ No hay servicios en consulta actual")
                return

            if not self.consulta_actual or not self.consulta_actual.id:
                self.mostrar_toast("❌ No hay consulta activa", "error")
                logger.error("❌ No hay consulta actual activa")
                return

            try:
                self.odontograma_guardando = True
                logger.info(f"💾 Finalizando intervención con {len(self.servicios_consulta_actual)} servicios...")

                # Calcular totales
                total_bs = sum(float(s.get("costo_bs", 0)) for s in self.servicios_consulta_actual)
                total_usd = sum(float(s.get("costo_usd", 0)) for s in self.servicios_consulta_actual)

                # 1. Crear nueva versión del odontograma si hay cambios
                odontograma_version_id = None
                if self.condiciones_por_diente:
                    personal_id = self.id_personal if self.id_personal else self.id_usuario
                    # Guardar condiciones actuales
                    for diente_num, condiciones in self.condiciones_por_diente.items():
                        for superficie, condicion in condiciones.items():
                            await odontologia_service.save_tooth_condition(
                                odontograma_id=self.odontograma_actual.id if self.odontograma_actual else None,
                                tooth_number=int(diente_num),
                                surface=superficie,
                                condition=condicion
                            )
                    logger.info("✅ Odontograma actualizado")

                # 2. Crear intervención en BD
                personal_id = self.id_personal if self.id_personal else self.id_usuario
                datos_intervencion = {
                    "consulta_id": self.consulta_actual.id,
                    "odontologo_id": personal_id,
                    "servicios": [
                        {
                            "diente": s["diente"],
                            "servicio_nombre": s["servicio"],
                            "superficies": s["superficies"],
                            "costo_bs": float(s["costo_bs"]),
                            "costo_usd": float(s["costo_usd"]),
                            "observaciones": s.get("observaciones", "")
                        }
                        for s in self.servicios_consulta_actual
                    ],
                    "total_bs": total_bs,
                    "total_usd": total_usd,
                    "observaciones_generales": f"Intervención completada con {len(self.servicios_consulta_actual)} servicios"
                }

                # Configurar contexto del servicio (usar perfil completo con permisos)
                from dental_system.services.odontologia_service import odontologia_service
                odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)

                # Preparar servicios para backend (formato antiguo)
                servicios_backend = []
                for s in self.servicios_consulta_actual:
                    servicio_data = {
                        "servicio_id": s.get("servicio_id"),  # ID real del catálogo
                        "cantidad": 1,
                        "precio_unitario_bs": float(s.get("costo_bs", 0)),
                        "precio_unitario_usd": float(s.get("costo_usd", 0)),
                        "dientes_texto": str(s.get("diente", "")),
                        "material_utilizado": "",
                        "superficie_dental": ", ".join(s.get("superficies", [])),
                        "observaciones": s.get("observaciones", s.get("servicio", ""))
                    }
                    servicios_backend.append(servicio_data)

                datos_intervencion_backend = {
                    "consulta_id": self.consulta_actual.id,
                    "odontologo_id": personal_id,
                    "servicios": servicios_backend,
                    "observaciones_generales": f"Intervención completada con {len(self.servicios_consulta_actual)} servicios",
                    "requiere_control": False
                }

                # Crear intervención con servicios (método antiguo que funciona)
                resultado = await odontologia_service.crear_intervencion_con_servicios(datos_intervencion_backend)

                if not resultado.get("success"):
                    async with self:
                        self.mostrar_toast(f"❌ Error: {resultado.get('message', 'Error desconocido')}", "error")
                    logger.error(f"Error guardando intervención: {resultado}")
                    return

                intervencion_id = resultado.get("intervencion_id")
                logger.info(f"✅ Intervención guardada: {intervencion_id}")
                print(f"\n{'='*80}")
                print(f"🔍 DEBUG - CAMBIO DE ESTADO DE CONSULTA")
                print(f"{'='*80}")

                # 3. CAMBIAR ESTADO CONSULTA (solo si no está en estado final)
                estado_actual = self.consulta_actual.estado if hasattr(self.consulta_actual, 'estado') else None
                print(f"📋 Estado actual de la consulta: '{estado_actual}'")
                print(f"🆔 ID de consulta: {self.consulta_actual.id}")
                print(f"📊 Servicios guardados: {len(self.servicios_consulta_actual)}")
                print(f"🎯 Nuevo estado deseado: 'entre_odontologos'")
                print(f"✅ ¿Puede cambiar? {estado_actual not in ['completada', 'cancelada']}")
                print(f"{'='*80}\n")

                if estado_actual and estado_actual not in ["completada", "cancelada"]:
                    from dental_system.services.consultas_service import consultas_service
                    consultas_service.set_user_context(self.id_usuario, self.perfil_usuario)

                    print(f"🔄 Intentando cambiar estado de '{estado_actual}' → 'entre_odontologos'...")

                    # Cambiar a "entre_odontologos" para que otro odontólogo pueda atender
                    await consultas_service.change_consultation_status(
                        consultation_id=self.consulta_actual.id,
                        nuevo_estado="entre_odontologos",
                        notas=f"Intervención completada por odontólogo con {len(self.servicios_consulta_actual)} servicios"
                    )
                    print(f"✅ Consulta cambiada exitosamente a 'entre_odontologos'")
                    logger.info("✅ Consulta cambiada a 'entre_odontologos'")
                else:
                    print(f"⚠️ SKIPPED: Consulta ya está en estado final '{estado_actual}' - No se cambia")
                    logger.info(f"⚠️ Consulta ya está en estado final '{estado_actual}' - No se cambia el estado")

                # 4. CREAR PAGO PENDIENTE (TODO: Implementar método crear_pago_pendiente)
                # El pago se creará manualmente desde el módulo de pagos por ahora
                logger.info(f"💳 Pago pendiente por crear manualmente: ${resultado.get('total_usd', 0.0)} USD / Bs {resultado.get('total_bs', 0.0)}")

                # 5. LIMPIAR ESTADO LOCAL
                self.servicios_consulta_actual = []
                self.condiciones_por_diente = {}
                self.selected_tooth = None
                self.show_add_intervention_modal = False
                self.tiene_servicios_seleccionados = False

                # 6. MOSTRAR ÉXITO Y NAVEGAR
                self.mostrar_toast("✅ Intervención completada exitosamente", "success")

                # Navegar de vuelta después de 2 segundos
                import asyncio
                await asyncio.sleep(2)

                self.navigate_to("odontologia", "Lista de Pacientes", "")

                logger.info("✅ Intervención finalizada con flujo completo")

            except Exception as e:
                logger.error(f"❌ Error finalizando intervención: {str(e)}")
                import traceback
                traceback.print_exc()
                self.mostrar_toast(f"❌ Error: {str(e)}", "error")
            finally:
                self.odontograma_guardando = False

    # ============================================================================
    # 📊 COMPUTED VARS V4.0 - DATOS PARA COMPONENTES PROFESIONALES
    # ============================================================================

    @rx.var(cache=True)
    def get_teeth_data(self) -> Dict[int, Dict[str, Any]]:
        """🦷 Obtener data de todos los dientes para el grid profesional"""
        if not self.odontograma_actual:
            return {}

        teeth_data = {}
        for diente_num in range(11, 49):  # FDI: 11-18, 21-28, 31-38, 41-48
            # Saltar números inválidos (19, 20, 29, 30, etc.)
            if diente_num % 10 == 9 or diente_num % 10 == 0:
                continue

            # Obtener condiciones del diente actual
            condiciones = self.condiciones_por_diente.get(str(diente_num), {})

            # Determinar estado general del diente
            if any(cond in ["caries", "fractura", "ausente"] for cond in condiciones.values()):
                status = "patologico"
            elif any(cond in ["restauracion", "corona", "implante"] for cond in condiciones.values()):
                status = "tratado"
            elif any(cond in ["obturacion_temporal", "en_tratamiento"] for cond in condiciones.values()):
                status = "en_tratamiento"
            else:
                status = "sano"

            teeth_data[diente_num] = {
                "number": diente_num,
                "status": status,
                "has_conditions": len(condiciones) > 0,
                "conditions": list(condiciones.values())
            }

        return teeth_data

    @rx.var(cache=True)
    def get_tooth_name(self) -> str:
        """📝 Obtener nombre del diente seleccionado"""
        if not self.selected_tooth:
            return ""

        from dental_system.components.odontologia.simple_tooth import TOOTH_NAMES
        return TOOTH_NAMES.get(self.selected_tooth, f"Diente {self.selected_tooth}")

    @rx.var(cache=True)
    def get_tooth_status(self) -> str:
        """📊 Obtener estado del diente seleccionado"""
        if not self.selected_tooth:
            return "sano"

        teeth_data = self.get_teeth_data
        tooth_data = teeth_data.get(self.selected_tooth, {})
        return tooth_data.get("status", "sano")

    @rx.var(cache=True)
    def get_tooth_interventions(self) -> List[Dict[str, Any]]:
        """📋 Obtener intervenciones del diente seleccionado"""
        if not self.selected_tooth:
            return []

        # Filtrar intervenciones por diente seleccionado
        return [
            intervention for intervention in self.intervenciones_paciente
            if self.selected_tooth in intervention.get("tooth_numbers", [])
        ]

    @rx.var(cache=True)
    def get_tooth_conditions(self) -> List[str]:
        """🔍 Obtener condiciones activas del diente seleccionado"""
        if not self.selected_tooth:
            return []

        condiciones = self.condiciones_por_diente.get(str(self.selected_tooth), {})
        return [cond for cond in condiciones.values() if cond]

    @rx.var(cache=True)
    def get_filtered_interventions(self) -> List[Dict[str, Any]]:
        """🔍 Obtener intervenciones filtradas para el timeline V4.0"""
        if not self.intervenciones_paciente:
            return []

        interventions = self.intervenciones_paciente

        # Filtro por dentista
        if self.timeline_filter_dentist and self.timeline_filter_dentist != "all" and self.timeline_filter_dentist != "Todos":
            interventions = [
                i for i in interventions
                if i.get("dentist") == self.timeline_filter_dentist
            ]

        # Filtro por procedimiento
        if self.timeline_filter_procedure and self.timeline_filter_procedure != "all" and self.timeline_filter_procedure != "Todos":
            interventions = [
                i for i in interventions
                if self.timeline_filter_procedure in i.get("procedure", "")
            ]

        # Filtro por período
        if self.timeline_filter_period and self.timeline_filter_period != "all" and self.timeline_filter_period != "Todo el historial":
            from datetime import datetime, timedelta
            today = datetime.now().date()

            if self.timeline_filter_period == "Últimos 7 días":
                cutoff_date = today - timedelta(days=7)
            elif self.timeline_filter_period == "Últimos 30 días":
                cutoff_date = today - timedelta(days=30)
            elif self.timeline_filter_period == "Últimos 90 días":
                cutoff_date = today - timedelta(days=90)
            else:
                cutoff_date = None

            if cutoff_date:
                interventions = [
                    i for i in interventions
                    if datetime.strptime(i.get("date", ""), "%Y-%m-%d").date() >= cutoff_date
                ]

        return interventions

    @rx.var(cache=True)
    def get_patient_display_name(self) -> str:
        """👤 Obtener nombre completo del paciente para el control bar"""
        if not self.consulta_actual or not hasattr(self, 'paciente_info'):
            return "Sin paciente seleccionado"

        paciente = self.paciente_info
        if paciente:
            nombres = paciente.get('nombres', '')
            apellidos = paciente.get('apellidos', '')
            return f"{nombres} {apellidos}".strip()

        return "Sin paciente"

    @rx.var(cache=True)
    def get_patient_id_display(self) -> str:
        """🔢 Obtener HC del paciente para el control bar"""
        if not self.consulta_actual or not hasattr(self, 'paciente_info'):
            return ""

        paciente = self.paciente_info
        return paciente.get('numero_historia', '') if paciente else ""

    @rx.var(cache=True)
    def get_available_dentists(self) -> List[str]:
        """👨‍⚕️ Lista de dentistas para filtros del timeline (con 'Todos' incluido)"""
        return ["Todos"] + self.dentistas_paciente

    @rx.var(cache=True)
    def get_available_procedures(self) -> List[str]:
        """🦷 Lista de procedimientos para filtros del timeline (con 'Todos' incluido)"""
        return ["Todos"] + self.procedimientos_paciente

    @rx.var(cache=True)
    def get_interventions_count(self) -> int:
        """🔢 Contador total de intervenciones"""
        return len(self.intervenciones_paciente)

    @rx.var(cache=True)
    def get_filtered_count(self) -> int:
        """🔢 Contador de intervenciones filtradas"""
        return len(self.get_filtered_interventions)

    # ==========================================
    # 🆕 COMPUTED VARS NUEVA ESTRUCTURA
    # ==========================================

    @rx.var(cache=True)
    def get_tooth_conditions_rows(self) -> List[Dict[str, str]]:
        """📊 Formatear condiciones del diente seleccionado para tabla"""
        if not self.selected_tooth:
            return []

        condition_map = {
            "sano": {"icon": "circle-check", "color": "#48BB78"},
            "caries": {"icon": "circle-alert", "color": "#E53E3E"},
            "obturado": {"icon": "shield", "color": "#4299E1"},
            "corona": {"icon": "crown", "color": "#9F7AEA"},
            "endodoncia": {"icon": "zap", "color": "#ED8936"},
            "ausente": {"icon": "x-circle", "color": "#A0AEC0"},
            "por_extraer": {"icon": "scissors", "color": "#F59E0B"},
            "fracturado": {"icon": "triangle-alert", "color": "#EF4444"},
        }

        surfaces = [
            ("oclusal", "Oclusal"),
            ("mesial", "Mesial"),
            ("distal", "Distal"),
            ("vestibular", "Vestibular"),
            ("lingual", "Lingual"),
        ]

        rows = []
        condiciones_diente = self.condiciones_por_diente.get(self.selected_tooth, {})

        for surface_key, surface_name in surfaces:
            condicion = condiciones_diente.get(surface_key, "sano")
            map_data = condition_map.get(condicion, {"icon": "circle", "color": "#A0AEC0"})

            rows.append({
                "superficie": surface_name,
                "estado": condicion.replace("_", " ").title(),
                "icon": map_data["icon"],
                "color": map_data["color"]
            })

        return rows

    @rx.var(cache=True)
    def get_consultation_services_rows(self) -> List[Dict[str, Any]]:
        """📋 Formatear servicios de consulta actual para tabla"""
        rows = []
        for service in self.servicios_consulta_actual:
            superficies = service.get("superficies", [])
            superficies_str = ", ".join(superficies) if superficies else "—"

            rows.append({
                "id": service.get("id", ""),
                "diente": str(service.get("diente", "")),
                "servicio": service.get("servicio", ""),
                "superficies": superficies_str,
                "costo_bs": f"{service.get('costo_bs', 0):,.0f} Bs",
                "costo_usd": f"${service.get('costo_usd', 0):.2f}",
            })

        return rows

    @rx.var(cache=True)
    def get_consultation_total_bs(self) -> float:
        """💰 Total en bolívares de servicios actuales"""
        return sum(s.get("costo_bs", 0) for s in self.servicios_consulta_actual)

    @rx.var(cache=True)
    def get_consultation_total_usd(self) -> float:
        """💰 Total en dólares de servicios actuales"""
        return sum(s.get("costo_usd", 0) for s in self.servicios_consulta_actual)

    @rx.var(cache=True)
    def get_consultation_total_bs_formatted(self) -> str:
        """💰 Total BS formateado"""
        return f"{self.get_consultation_total_bs:,.0f} Bs"

    @rx.var(cache=True)
    def get_consultation_total_usd_formatted(self) -> str:
        """💰 Total USD formateado"""
        return f"/ ${self.get_consultation_total_usd:.2f}"

    @rx.var(cache=True)
    def get_available_services_names(self) -> List[str]:
        """📋 Lista de nombres de servicios para select"""
        if self.servicios_disponibles:
            return [s.nombre for s in self.servicios_disponibles if s.nombre]
        return []

    @rx.var(cache=True)
    def selected_service_cost_bs(self) -> float:
        """💵 Costo BS del servicio seleccionado"""
        if not self.selected_service_name:
            return 0.0

        for service in self.servicios_disponibles:
            if service.nombre == self.selected_service_name:
                return float(service.precio_base_bs) if service.precio_base_bs else 0.0
        return 0.0

    @rx.var(cache=True)
    def selected_service_cost_usd(self) -> float:
        """💵 Costo USD del servicio seleccionado"""
        if not self.selected_service_name:
            return 0.0

        for service in self.servicios_disponibles:
            if service.nombre == self.selected_service_name:
                return float(service.precio_base_usd) if service.precio_base_usd else 0.0
        return 0.0

    @rx.var(cache=True)
    def selected_service_id(self) -> str:
        """🆔 ID del servicio seleccionado del catálogo"""
        if not self.selected_service_name:
            logger.warning("⚠️ No hay servicio seleccionado")
            return ""

        logger.debug(f"🔍 Buscando ID para servicio: '{self.selected_service_name}'")
        logger.debug(f"📋 Servicios disponibles: {len(self.servicios_disponibles)}")

        for service in self.servicios_disponibles:
            logger.debug(f"  Comparando: '{service.nombre}' vs '{self.selected_service_name}'")
            if service.nombre == self.selected_service_name:
                logger.info(f"✅ Servicio encontrado! ID: {service.id}")
                return service.id if service.id else ""

        logger.error(f"❌ Servicio '{self.selected_service_name}' NO encontrado en catálogo")
        return ""

