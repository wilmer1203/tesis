
import reflex as rx
from typing import Dict, Any, List, Optional, Tuple
import logging
from dental_system.services.odontologia_service import odontologia_service
from dental_system.models import (
    PacienteModel,
    ConsultaModel,
    IntervencionModel,
    ServicioModel,
    OdontogramaModel,
    IntervencionFormModel,
    HistorialServicioModel
)
# ✅ V2.0: Importar modelo unificado
from dental_system.state.estado_intervencion_servicios import ServicioIntervencionCompleto

logger = logging.getLogger(__name__)

class EstadoOdontologia(rx.State, mixin=True):
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

    # ==========================================
    # 📊 ESTADÍSTICAS DEL DASHBOARD
    # ==========================================

    # 🦷 VARIABLES DASHBOARD ODONTÓLOGO (NUEVO 2025-10-30)
    dashboard_stats_odontologo: Dict[str, Any] = {}  # Stats para 5 cards
    consultas_data_odontologo: List[Dict[str, Any]] = []  # Gráfico consultas 30 días
    ingresos_data_odontologo: List[Dict[str, Any]] = []  # Gráfico ingresos 30 días
    top_servicios_odontologo: List[Dict[str, Any]] = []  # Top servicios aplicados hoy
    cargando_dashboard_odontologo: bool = False  # Loading state
    
    # ==========================================
    # 📋 HISTORIAL CLÍNICO DEL PACIENTE ACTUAL
    # ==========================================

    # para mantener consistencia con el tipo de datos esperado
    intervenciones_anteriores: List[IntervencionModel] = []
    ultima_consulta_info: Optional[ConsultaModel] = None
    tiene_historial_cargado: bool = False
    
    # ==========================================
    # 🦷 SERVICIOS ODONTOLÓGICOS
    # ==========================================

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

    # ==========================================
    # 🆕 HISTORIAL DE SERVICIOS DEL PACIENTE (2025-10-16)
    # ==========================================

    # Lista de servicios históricos del paciente (una card por servicio)
    historial_intervenciones: List[HistorialServicioModel] = []

    # Estados de carga
    historial_loading: bool = False

    # Filtrado por diente
    historial_filtrado_por_diente: Optional[int] = None

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

    # # Configuración de condiciones disponibles
    # condiciones_disponibles: Dict[str, Dict[str, str]] = {
    #     "sano": {"color": "#90EE90", "descripcion": "Diente sano", "simbolo": "✓"},
    #     "caries": {"color": "#FF0000", "descripcion": "Caries dental", "simbolo": "C"},
    #     "obturado": {"color": "#C0C0C0", "descripcion": "Obturación/empaste", "simbolo": "O"},
    #     "endodoncia": {"color": "#FFD700", "descripcion": "Tratamiento de conducto", "simbolo": "E"},
    #     "corona": {"color": "#4169E1", "descripcion": "Corona dental", "simbolo": "R"},
    #     "puente": {"color": "#800080", "descripcion": "Puente dental", "simbolo": "P"},
    #     "extraccion": {"color": "#8B0000", "descripcion": "Para extraer", "simbolo": "X"},
    #     "ausente": {"color": "#FFFFFF", "descripcion": "Diente ausente", "simbolo": "-"},
    #     "fractura": {"color": "#FF6347", "descripcion": "Fractura dental", "simbolo": "F"},
    #     "implante": {"color": "#32CD32", "descripcion": "Implante dental", "simbolo": "I"},
    #     "protesis": {"color": "#DA70D6", "descripcion": "Prótesis removible", "simbolo": "PT"},
    #     "giroversion": {"color": "#FF8C00", "descripcion": "Diente rotado", "simbolo": "G"}
    # }

    # Control de carga lazy de historial
    historial_cargado_por_diente: Dict[int, bool] = {}

    # Variables para la selección de condiciones
    selected_condition_to_apply: Optional[str] = None  # Condición seleccionada para aplicar
    # NOTA: current_surface_condition es un computed var, no variable de estado
    is_applying_condition: bool = False  # Indica si se está aplicando una condición
    
    # # Cuadrantes FDI
    # cuadrante_1: List[int] = [11, 12, 13, 14, 15, 16, 17, 18]  # Superior derecho
    # cuadrante_2: List[int] = [21, 22, 23, 24, 25, 26, 27, 28]  # Superior izquierdo
    # cuadrante_3: List[int] = [31, 32, 33, 34, 35, 36, 37, 38]  # Inferior izquierdo
    # cuadrante_4: List[int] = [41, 42, 43, 44, 45, 46, 47, 48]  # Inferior derecho
    
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
    

    @rx.var(cache=True)
    def consultas_por_estado(self) -> Dict[str, List[ConsultaModel]]:
        """Agrupar consultas por estado - ESQUEMA v4.1"""
        try:
            agrupadas = {
                "en_espera": [],  # Mantener para backward compatibility
                "en_atencion": [],  # Mantener para backward compatibility
                "completada": [],
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
                if estado == "en_espera":
                    agrupadas["en_espera"].append(consulta)
                elif estado == "en_atencion":
                    agrupadas["en_atencion"].append(consulta)
                elif estado == "completada":
                    agrupadas["completada"].append(consulta)

            return agrupadas

        except Exception:
            return {"completada": [], "en_espera": [], "en_atencion": [], "entre_odontologos": [], "cancelada": []}

    @rx.var(cache=True)
    def consultas_activas(self) -> List[ConsultaModel]:
        """
        🔄 Consultas ACTIVAS (no completadas ni canceladas)

        ✅ NUEVO (2025-01-13): Computed var para filtrar consultas que aún necesitan atención
        Usado en UI para mostrar cola de pacientes pendientes
        """
        try:
            return [
                c for c in self.consultas_asignadas
                if c.estado not in ["completada", "cancelada"]
            ]
        except Exception:
            return []

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

            # ✅ CORRECCIÓN (2025-01-13): Cargar TODAS las consultas del día (incluyendo completadas)
            # Esto permite que las estadísticas cuenten correctamente las consultas finalizadas
            self.consultas_asignadas = consultas_asignadas
            
            # BACKWARD COMPATIBILITY: Mantener pacientes_asignados para otros componentes
            # Crear PacienteModel básico desde información de consulta
            self.pacientes_asignados = []
            for c in self.consultas_asignadas:
                if c.paciente_id and c.paciente_nombre:
                    from dental_system.services.pacientes_service import pacientes_service
                    pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
                    paciente_basico = await pacientes_service.get_patient_by_id(c.paciente_id)
                    self.pacientes_asignados.append(paciente_basico)
            
            logger.info(f"✅ Consultas asignadas cargadas: {len(self.consultas_asignadas)}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando consultas asignadas: {e}")
            self.handle_error("Error al cargar consultas asignadas", e)
            
        finally:
            self.cargando_pacientes_asignados = False

    async def cargar_consultas_disponibles_otros(self):
        """
        🔄 Cargar consultas disponibles de otros odontólogos

        Estas son consultas donde el paciente ya fue atendido por otro odontólogo
        pero puede necesitar una segunda intervención (derivación).
        Estado: "entre_odontologos"
        """

        try:
            # Establecer contexto en el servicio
            odontologia_service.set_user_context(user_id=self.id_usuario, user_profile=self.perfil_usuario)

            # ✅ CORRECCIÓN: Obtener CONSULTAS disponibles (no pacientes)
            consultas_disponibles = await odontologia_service.get_consultas_disponibles(self.id_personal)

            # ✅ CORRECCIÓN: Actualizar consultas_disponibles_otros (no pacientes_disponibles_otros)
            self.consultas_disponibles_otros = [
                ConsultaModel.from_dict(c) for c in consultas_disponibles
            ]

            logger.info(f"✅ Consultas disponibles cargadas: {len(self.consultas_disponibles_otros)}")

        except Exception as e:
            logger.error(f"❌ Error cargando consultas disponibles: {e}")
            import traceback
            traceback.print_exc()
    
   
    # ==========================================
    # 🦷 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================
    
 
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
            if not paciente_encontrado:
                logger.warning(f"❌ Paciente no encontrados: {paciente_id}")
                return
            
            # 2. Buscar consulta en la lista
            consulta_encontrada = next(
                (c for c in self.consultas_asignadas if c.id == consulta_id),
                None
            )

            if  not consulta_encontrada:
                logger.warning(f"❌ consulta no encontrados:{consulta_id}")
                return

            # 3. Establecer como contexto actual
            self.paciente_actual = paciente_encontrado
            self.consulta_actual = consulta_encontrada

            logger.info(f"✅ Paciente seleccionado: {paciente_encontrado.nombre_completo}")

            # 4. Cambiar estado de consulta a "en_atencion" si está "en_espera"
            if consulta_encontrada.estado in ["en_espera", "programada"]:
                # Con mixin=True, acceso directo a métodos de EstadoConsultas
                await self.iniciar_atencion_consulta(
                    consulta_id,
                    estado_objetivo="en_atencion"
                )
                logger.info(f"🏥 Consulta cambiada a 'en_atencion'")

            # 5. Cargar odontograma del paciente (última versión)
            await self.cargar_odontograma_paciente_actual()

            # 7. Cargar historial del paciente
            await self.cargar_historial_paciente(paciente_id)

            # 8. Establecer flag de formulario activo
            self.en_formulario_intervencion = True
            self.modo_formulario = "crear"

            # 9. Navegar a página de intervención
            # Con mixin=True, navigate_to está disponible directamente
            self.navigate_to(
                "intervencion",
                f"Atención Odontológica - {paciente_encontrado.nombre_completo}",
                f"Consulta #{consulta_encontrada.numero_consulta or 'N/A'}"
            )

            logger.info(f"🦷 Navegación a intervención completada")

        except Exception as e:
            logger.error(f"❌ Error en seleccionar_paciente_consulta: {str(e)}")
            self.self.mostrar_toast("Error al seleccionar paciente")
    
    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.pacientes_asignados = []
        self.consultas_asignadas = []  
        self.consulta_actual = ConsultaModel()
        self.paciente_actual = PacienteModel()
        self.intervencion_actual = IntervencionModel()
        
        self.servicio_seleccionado = ServicioModel()
        self.id_servicio_seleccionado = ""
        
        
        # Limpiar odontograma
        self.dientes_fdi = []
        self.odontograma_actual = OdontogramaModel()
        self.diente_seleccionado = None
        self.modo_odontograma = "visualizacion"
        
        # Limpiar formulario y estadísticas
        self.formulario_intervencion = IntervencionFormModel()
 
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
    
    @rx.var
    def consultas_disponibles_filtradas(self) -> List[ConsultaModel]:
        """
        🔄 Lista filtrada de consultas disponibles de otros odontólogos

        ✅ CORRECCIÓN (2025-01-13): Ahora filtra CONSULTAS (no pacientes)
        """
        if not self.consultas_disponibles_otros:
            return []

        try:
            resultado = self.consultas_disponibles_otros.copy()

            # Filtro por búsqueda si está activo (buscar en nombre o documento del paciente)
            if self.termino_busqueda_pacientes and len(self.termino_busqueda_pacientes) >= 2:
                termino_lower = self.termino_busqueda_pacientes.lower()
                resultado = [
                    c for c in resultado
                    if (termino_lower in c.paciente_nombre.lower() or
                        termino_lower in c.paciente_documento.lower() or
                        termino_lower in c.paciente_historia.lower())
                ]

            # Ordenar por fecha de llegada (más antiguo primero = orden de llegada)
            return resultado

        except Exception as e:
            logger.error(f"Error en consultas_disponibles_filtradas: {e}")
            return []
    
    @rx.var(cache=True)
    def estadisticas_odontologo_tiempo_real(self) -> Dict[str, int]:
        """
        📊 Estadísticas en tiempo real del odontólogo - PATRÓN CONSULTAS PAGE

        ✅ CORRECCIÓN (2025-01-13): Usa consultas_disponibles_otros (no pacientes_disponibles_otros)
        """
        try:
            # Contar directamente desde self.consultas_asignadas (como en página consultas)
            consultas_del_odontologo = self.consultas_asignadas

            return {
                "pacientes_asignados": len(consultas_del_odontologo),
                "consultas_en_espera": len([c for c in consultas_del_odontologo if c.estado =="en_espera"]),
                "consultas_en_atencion": len([c for c in consultas_del_odontologo if c.estado == "en_atencion"]),
                "consultas_completadas": len([c for c in consultas_del_odontologo if c.estado == "completada"]),
                "pacientes_disponibles": len(self.consultas_disponibles_otros)  # ✅ Consultas, no pacientes
            }

        except Exception as e:
            logger.error(f"Error en estadisticas_odontologo_tiempo_real: {e}")
            return {
                "pacientes_asignados": 0,
                "pacientes_disponibles": 0,
                "consultas_en_espera": 0,
                "consultas_en_atencion": 0,
                "consultas_completadas": 0
            }
    
    # @rx.var(cache=True)
    # def proxima_consulta_info(self) -> Dict[str, str]:
    #     """📅 Información de la próxima consulta en orden"""
    #     try:
    #         consultas_programadas = self.consultas_por_estado.get("en_espera", [])
            
    #         if not consultas_programadas:
    #             return {
    #                 "tiene_proxima": "false",
    #                 "paciente": "No hay consultas programadas",
    #                 "tiempo_estimado": "N/A"
    #             }
            
    #         # Obtener la primera consulta (orden de llegada)
    #         proxima_consulta = consultas_programadas[0]
    #         paciente = next(
    #             (p for p in self.pacientes_asignados if p.id == proxima_consulta.paciente_id),
    #             None
    #         )
            
    #         return {
    #             "tiene_proxima": "true",
    #             "paciente": paciente.nombre_completo if paciente else "Paciente no encontrado",
    #             "tiempo_estimado": "15-30 min",
    #             "prioridad": getattr(proxima_consulta, 'prioridad', 'normal')
    #         }
            
    #     except Exception as e:
    #         logger.error(f"Error en proxima_consulta_info: {e}")
    #         return {
    #             "tiene_proxima": "false",
    #             "paciente": "Error",
    #             "tiempo_estimado": "N/A"
    #         }
    
    # @rx.var(cache=True)
    # def resumen_actividad_dia(self) -> str:
    #     """📋 Resumen textual de la actividad del día"""
    #     try:
    #         total_consultas = len(self.consultas_asignadas)
    #         completadas = len(self.consultas_por_estado.get("completada", []))
    #         en_atencion = len(self.consultas_por_estado.get("en_atencion", []))
    #         en_espera = len(self.consultas_por_estado.get("en_espera", []))
            
    #         if total_consultas == 0:
    #             return "Sin consultas asignadas hoy"
            
    #         if completadas == total_consultas:
    #             return f"Día completado: {completadas} consultas finalizadas"
            
    #         resumen_parts = []
    #         if en_espera > 0:
    #             resumen_parts.append(f"{en_espera} en espera")
    #         if en_atencion > 0:
    #             resumen_parts.append(f"{en_atencion} en atención")
    #         if completadas > 0:
    #             resumen_parts.append(f"{completadas} completadas")
                
    #         return f"Actividad: {', '.join(resumen_parts)}"
            
    #     except Exception as e:
    #         logger.error(f"Error en resumen_actividad_dia: {e}")
    #         return "Error calculando actividad"
    
    # @rx.var(cache=True)
    # def alerta_pacientes_urgentes(self) -> Dict[str, Any]:
    #     """🚨 Verificar si hay pacientes urgentes que requieren atención inmediata"""
    #     try:
    #         urgentes_asignados = [
    #             p for p in self.pacientes_asignados 
    #             if hasattr(p, 'prioridad') and p.prioridad in ['urgente', 'alta']
    #         ]
            
    #         urgentes_disponibles = [
    #             p for p in self.pacientes_disponibles_otros
    #             if hasattr(p, 'prioridad') and p.prioridad in ['urgente', 'alta']
    #         ]
            
    #         total_urgentes = len(urgentes_asignados) + len(urgentes_disponibles)
            
    #         return {
    #             "tiene_urgentes": total_urgentes > 0,
    #             "cantidad": total_urgentes,
    #             "mensaje": f"{total_urgentes} paciente{'s' if total_urgentes != 1 else ''} urgente{'s' if total_urgentes != 1 else ''}" if total_urgentes > 0 else "No hay pacientes urgentes"
    #         }
            
    #     except Exception as e:
    #         logger.error(f"Error en alerta_pacientes_urgentes: {e}")
    #         return {
    #             "tiene_urgentes": False,
    #             "cantidad": 0,
    #             "mensaje": "Error verificando urgencias"
    #         }
    


    # ==========================================
    # 🎨 MÉTODOS PARA PANEL PACIENTE MEJORADO
    # ==========================================
    
    def toggle_panel_paciente(self):
        """🔄 Alternar expansión del panel de paciente"""
        self.panel_paciente_expandido = not self.panel_paciente_expandido
    

    # ==========================================
    # 🚀 MÉTODOS V2.0 - ODONTOGRAMA INTERACTIVO
    # ==========================================

    @rx.event
    async def cargar_odontograma_paciente_actual(self):
        """📋 Cargar odontograma actual del paciente seleccionado"""
        try:
            if not self.paciente_actual or not self.paciente_actual.id:
                print("⚠️ No hay paciente actual seleccionado")
                return

            self.odontograma_cargando = True
            
            # SIMPLIFICADO: Solo un método
            result = await odontologia_service.get_patient_odontogram(self.paciente_actual.id)

            # Asignar condiciones
            self.condiciones_por_diente = result["conditions"]

            self.odontograma_cargando = False
            logger.info(f"✅ Odontograma cargado: {result['total_condiciones']} condiciones")

        except Exception as e:
            logger.error(f"❌ Error cargando odontograma: {e}")
            self.odontograma_cargando = False


    @rx.event
    async def guardar_cambios_odontograma(self):
        """💾 Guardar cambios del odontograma"""
        try:
            if not self.cambios_sin_guardar:
                return

            self.odontograma_guardando = True

            # Obtener intervención actual
            intervencion_id = self.intervencion_actual_id if hasattr(self, 'intervencion_actual_id') else None

            # SIMPLIFICADO: Actualizar cada cambio
            for diente_num, superficies in self.condiciones_por_diente.items():
                for superficie, condicion_data in superficies.items():
                    # Extraer condición (puede ser str o dict)
                    if isinstance(condicion_data, str):
                        condicion_str = condicion_data
                        material = None
                    elif isinstance(condicion_data, dict):
                        condicion_str = condicion_data.get("condicion", "sano")
                        material = condicion_data.get("material")
                    else:
                        condicion_str = "sano"
                        material = None

                    await odontologia_service.actualizar_condicion_diente(
                        paciente_id=self.paciente_actual.id,
                        diente_numero=diente_num,
                        superficie=superficie,
                        nueva_condicion=condicion_str,
                        intervencion_id=intervencion_id,
                        material=material
                    )

            self.cambios_sin_guardar = False
            self.odontograma_guardando = False
            self.mostrar_toast("Odontograma guardado correctamente", "success")

        except Exception as e:
            logger.error(f"❌ Error guardando odontograma: {e}")
            self.odontograma_guardando = False
            self.mostrar_toast(f"Error: {str(e)}", "error")
  
    # ==========================================
    # 🌟 EVENTOS V4.0 - NUEVO DISEÑO PROFESIONAL
    # ==========================================

    @rx.event
    def select_tooth(self, tooth_number: int):
        """
        🦷 Seleccionar un diente del odontograma

        Args:
            tooth_number: Número FDI del diente (11-48)

        🆕 MODIFICADO (2025-10-16): Ahora también filtra el historial automáticamente
        """
        self.selected_tooth = tooth_number
        self.active_sidebar_tab = "historial"  # Resetear a tab historial

        # 🆕 Auto-filtrar historial cuando se selecciona diente
        self.filtrar_historial_por_diente(tooth_number)

        logger.info(f"✅ Diente {tooth_number} seleccionado + historial filtrado")



    # ============================================================================
    # 📊 COMPUTED VARS V4.0 - DATOS PARA COMPONENTES PROFESIONALES
    # ============================================================================

    @rx.var
    def get_teeth_data(self) -> Dict[int, Dict[str, Any]]:
        """
        🦷 Obtener data de todos los dientes para el grid profesional

        Determina el STATUS GENERAL del diente analizando las condiciones de sus 5 superficies.
        El status se asigna por PRIORIDAD (de más crítico a menos crítico).
        """

        if not self.condiciones_por_diente:
            return {}

        teeth_data = {}
        for diente_num in range(11, 49):  # FDI: 11-18, 21-28, 31-38, 41-48
            # Saltar números inválidos (19, 20, 29, 30, etc.)
            if diente_num % 10 == 9 or diente_num % 10 == 0:
                continue

            # Obtener condiciones del diente actual (puede ser int o str)
            condiciones = self.condiciones_por_diente.get(diente_num, {})
            if not condiciones:
                condiciones = self.condiciones_por_diente.get(str(diente_num), {})

            # Extraer lista de condiciones para análisis
            condiciones_no_sanas = [c for c in condiciones.values() if c != "sano"]

            # ✅ LÓGICA CORREGIDA: Asignar status por PRIORIDAD
            # Orden: ausente > fractura > caries > endodoncia > obturado > corona > implante > sano

            if any(cond == "ausente" for cond in condiciones.values()):
                status = "ausente"  # ⚫ Gris - Diente extraído
            elif any(cond == "fractura" for cond in condiciones.values()):
                status = "fractura"  # 🔴 Rojo - Fractura (urgente)
            elif any(cond == "caries" for cond in condiciones.values()):
                status = "caries"  # 🔴 Rojo - Caries (necesita tratamiento)
            elif any(cond == "endodoncia" for cond in condiciones.values()):
                status = "endodoncia"  # 🟠 Naranja - Tratamiento de conducto
            elif any(cond == "obturacion" for cond in condiciones.values()):
                status = "obturado"  # 🔵 Azul - Tiene obturación/empaste
            elif any(cond == "corona" for cond in condiciones.values()):
                status = "corona"  # 🟡 Amarillo - Corona dental
            elif any(cond == "implante" for cond in condiciones.values()):
                status = "implante"  # 🟣 Púrpura - Implante dental
            else:
                status = "sano"  # 🟢 Verde - Diente saludable

            teeth_data[diente_num] = {
                "number": diente_num,
                "status": status,
                "has_conditions": len(condiciones_no_sanas) > 0,  # Badge rojo si tiene condiciones
                "conditions": list(condiciones.values())
            }

        return teeth_data


    @rx.var()
    def selected_service_id(self) -> str:
        """🆔 ID del servicio seleccionado del catálogo"""
        if not self.selected_service_name:
            logger.warning("⚠️ No hay servicio seleccionado")
            return ""
        for service in self.lista_servicios:
            logger.debug(f"  Comparando: '{service.nombre}' vs '{self.selected_service_name}'")
            if service.nombre == self.selected_service_name:
                logger.info(f"✅ Servicio encontrado! ID: {service.id}")
                return service.id if service.id else ""

        logger.error(f"❌ Servicio '{self.selected_service_name}' NO encontrado en catálogo")
        return ""

    # ==========================================
    # 🆕 COMPUTED VARS NUEVA ESTRUCTURA
    # ==========================================

    @rx.var(cache=True)
    def get_consultation_services_rows(self) -> List[Dict[str, Any]]:
        """
        📋 V2.0: Formatear servicios de intervención para tabla

        Compatible con ambos modelos durante migración:
        - ServicioIntervencionCompleto (V2.0)
        - ServicioIntervencionTemporal (deprecated)
        """
        rows = []
        for service in self.servicios_en_intervencion:
            # ✅ DETECTAR TIPO DE MODELO
            if isinstance(service, ServicioIntervencionCompleto):
                # ✅ MODELO NUEVO V2.0
                # Formatear diente según alcance
                if service.alcance == "boca_completa":
                    diente_display = "Boca completa"
                elif service.diente_numero:
                    diente_display = str(service.diente_numero)
                else:
                    diente_display = "—"

                # Formatear superficies (lista → string)
                if service.superficies:
                    superficies_display = ", ".join([s.capitalize() for s in service.superficies])
                else:
                    superficies_display = "—"

                rows.append({
                    "id": service.servicio_id,
                    "diente": diente_display,
                    "servicio": service.nombre_servicio,
                    "superficies": superficies_display,
                    "costo_bs": f"{service.costo_bs:,.0f} Bs",
                    "costo_usd": f"${service.costo_usd:.2f}",
                })
            else:
                # ⚠️ MODELO ANTIGUO (deprecated)
                rows.append({
                    "id": service.id_servicio,
                    "diente": service.dientes_texto,
                    "servicio": service.nombre_servicio,
                    "superficies": service.superficie if service.superficie else "—",
                    "costo_bs": f"{service.total_bs:,.0f} Bs",
                    "costo_usd": f"${service.total_usd:.2f}",
                })

        return rows

  
    @rx.var(cache=True)
    def get_available_services_names(self) -> List[str]:
        """📋 Lista de nombres de servicios para select"""
        if self.lista_servicios:
            return [s.nombre for s in self.lista_servicios if s.nombre]
        return []

    @rx.var(cache=True)
    def selected_service_cost_bs(self) -> float:
        """💵 Costo BS del servicio seleccionado"""
        if not self.selected_service_name:
            return 0.0

        for service in self.lista_servicios:
            if service.nombre == self.selected_service_name:
                return float(service.precio_base_usd) if service.precio_base_usd else 0.0
        return 0.0

    @rx.var(cache=True)
    def selected_service_cost_usd(self) -> float:
        """💵 Costo USD del servicio seleccionado"""
        if not self.selected_service_name:
            return 0.0

        for service in self.lista_servicios:
            if service.nombre == self.selected_service_name:
                return float(service.precio_base_usd) if service.precio_base_usd else 0.0
        return 0.0

    @rx.var(cache=True)
    def selected_service_alcance(self) -> str:
        """🎯 Alcance del servicio seleccionado (superficie_especifica | diente_completo | boca_completa)"""
        if not self.selected_service_name:
            return "boca_completa"  # Default

        for service in self.lista_servicios:
            if service.nombre == self.selected_service_name:
                return service.alcance_servicio
        return "superficie_especifica"

    @rx.var(cache=True)
    def selected_service_requiere_superficies(self) -> bool:
        """🦷 Indica si el servicio seleccionado requiere selección de superficies"""
        return self.selected_service_alcance == "superficie_especifica"

    @rx.var(cache=True)
    def selected_service_requiere_diente(self) -> bool:
        """🦷 Indica si el servicio seleccionado requiere selección de diente"""
        return self.selected_service_alcance in ["superficie_especifica", "diente_completo"]

    @rx.var(cache=True)
    def selected_service_aplica_toda_boca(self) -> bool:
        """👄 Indica si el servicio seleccionado se aplica a toda la boca"""
        return self.selected_service_alcance == "boca_completa"

    @rx.var(cache=True)
    def selected_service_alcance_display(self) -> str:
        """📝 Alcance del servicio seleccionado formateado para display"""
        alcances_map = {
            "superficie_especifica": "Se aplica a superficies específicas del diente",
            "diente_completo": "Se aplica al diente completo",
            "boca_completa": "Se aplica a toda la boca"
        }
        return alcances_map.get(self.selected_service_alcance, "")

    # ==========================================
    # 🆕 MÉTODOS NUEVA ESTRUCTURA
    # ==========================================

    def toggle_add_intervention_modal(self):
        """Toggle modal agregar intervención"""
        self.show_add_intervention_modal = not self.show_add_intervention_modal

    async def open_add_intervention_modal(self):
        """Abrir modal agregar intervención"""
        self.show_add_intervention_modal = True
         # Cargar servicios si la lista está vacía
        if not self.lista_servicios:
            await self.cargar_lista_servicios()  # ← Agregar esto
            
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

    @rx.event
    async def save_intervention_to_consultation(self):
        """
        💾 Agregar servicio a lista temporal de consulta actual

        Maneja 3 casos según alcance del servicio:
        1. superficie_especifica: Requiere diente + superficies
        2. diente_completo: Requiere solo diente (sin superficies)
        3. boca_completa: No requiere diente ni superficies
        """
        try:
            # Validación 1: Servicio seleccionado
            if not self.selected_service_name:
                self.mostrar_toast("Selecciona un servicio", "warning")
                return

            # Obtener alcance del servicio
            alcance = self.selected_service_alcance
            logger.info(f"📊 Guardando servicio con alcance: {alcance}")

            import uuid
            servicio = {
                "id": str(uuid.uuid4()),
                "servicio": self.selected_service_name,
                "servicio_id": self.selected_service_id,  # ✅ ID real del servicio
                "costo_bs": self.selected_service_cost_bs,
                "costo_usd": self.selected_service_cost_usd,
                "observaciones": self.intervention_observations,
                "alcance": alcance,  # 🆕 Guardar alcance
            }

            # CASO 1: Superficie específica (requiere diente + superficies)
            if alcance == "superficie_especifica":
                if not self.selected_tooth:
                    self.mostrar_toast("Selecciona un diente", "warning")
                    return

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

                servicio["diente"] = self.selected_tooth
                servicio["superficies"] = superficies
                logger.info(f"✅ Servicio superficie específica: diente {self.selected_tooth}, superficies {superficies}")

            # CASO 2: Diente completo (requiere solo diente)
            elif alcance == "diente_completo":
                if not self.selected_tooth:
                    self.mostrar_toast("Selecciona un diente", "warning")
                    return

                servicio["diente"] = self.selected_tooth
                servicio["superficies"] = ["Completo"]  # Indicador de diente completo
                logger.info(f"✅ Servicio diente completo: diente {self.selected_tooth}")

            # CASO 3: Boca completa (no requiere diente ni superficies)
            elif alcance == "boca_completa":
                servicio["diente"] = None  # No aplica diente específico
                servicio["superficies"] = []  # Sin superficies específicas
                logger.info(f"✅ Servicio boca completa")

            # ✅ V2.0: AGREGAR SERVICIO DIRECTAMENTE sin variables temporales
            # Buscar el servicio completo en el catálogo
            servicio_completo = None
            for s in self.lista_servicios:
                if s.nombre == self.selected_service_name:
                    servicio_completo = s
                    break

            if not servicio_completo:
                logger.error(f"❌ Servicio '{self.selected_service_name}' no encontrado")
                self.mostrar_toast("Error: Servicio no encontrado", "error")
                return

            # ✅ NUEVO MÉTODO V2.0: agregar_servicio_directo()
            # Obtener superficies en el formato correcto (minúsculas)
            superficies_list = []
            for sup in servicio.get("superficies", []):
                superficies_list.append(sup.lower())

            # ✅ CORRECCIÓN: Determinar condición a aplicar
            # Prioridad 1: Manual override si usuario marcó checkbox
            # Prioridad 2: Condición desde BD (servicio.condicion_resultante)
            if self.auto_change_condition and self.new_condition_value:
                condicion_a_aplicar = self.new_condition_value  # Override manual
                logger.info(f"🔧 Usando condición MANUAL: {condicion_a_aplicar}")
            else:
                condicion_a_aplicar = servicio_completo.condicion_resultante  # De BD
                logger.info(f"💾 Usando condición desde BD: {condicion_a_aplicar}")

            # Llamar al nuevo método unificado
            self.agregar_servicio_directo(
                servicio=servicio_completo,
                alcance=alcance,
                diente_numero=servicio.get("diente"),
                superficies=superficies_list,
                nueva_condicion=condicion_a_aplicar,
                observaciones=self.intervention_observations
            )

            self.tiene_servicios_seleccionados = True
            self.show_add_intervention_modal = False

            # Mensaje personalizado según alcance
            mensaje_map = {
                "superficie_especifica": f"✅ Servicio agregado al diente {servicio.get('diente')}",
                "diente_completo": f"✅ Servicio agregado al diente {servicio.get('diente')} (completo)",
                "boca_completa": "✅ Servicio agregado (toda la boca)"
            }
            self.mostrar_toast(mensaje_map.get(alcance, "✅ Servicio agregado"), "success")

        except Exception as e:
            logger.error(f"❌ Error agregando servicio: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostrar_toast(f"Error: {str(e)}", "error")

    @rx.event
    async def apply_quick_condition_change(self):
        """
        🔄 Cambiar condición del diente (solo diagnóstico, sin servicio)

        Actualiza el odontograma con la nueva condición del diente.
        Se vincula a la intervención actual para trazabilidad.
        """
        try:
            # Validaciones
            if not self.selected_tooth:
                self.mostrar_toast("Selecciona un diente", "warning")
                return

            if not self.quick_surface_selected:
                self.mostrar_toast("Selecciona una superficie", "warning")
                return

            if not self.quick_condition_value:
                self.mostrar_toast("Selecciona una condición", "warning")
                return

            if not self.paciente_actual or not self.paciente_actual.id:
                self.mostrar_toast("No hay paciente seleccionado", "error")
                return

            logger.info(f"🔄 Cambiando condición: Diente {self.selected_tooth} ({self.quick_surface_selected}) → {self.quick_condition_value}")

            # Obtener ID de intervención actual (si existe)
            intervencion_id = None
            if hasattr(self, 'intervencion_actual') and self.intervencion_actual.id:
                intervencion_id = self.intervencion_actual.id

            # Actualizar condición en BD (vinculado a intervención actual)
            await odontologia_service.actualizar_condicion_diente(
                paciente_id=self.paciente_actual.id,
                diente_numero=self.selected_tooth,
                superficie=self.quick_surface_selected,
                nueva_condicion=self.quick_condition_value,
                intervencion_id=intervencion_id,
                material=None,
                descripcion="Actualización de diagnóstico"
            )

            # Actualizar en memoria para reflejar en UI inmediatamente
            if self.selected_tooth not in self.condiciones_por_diente:
                self.condiciones_por_diente[self.selected_tooth] = {}

            self.condiciones_por_diente[self.selected_tooth][self.quick_surface_selected] = self.quick_condition_value

            # Cerrar modal y limpiar
            self.show_change_condition_modal = False
            self.quick_surface_selected = ""
            self.quick_condition_value = ""

            self.mostrar_toast("Condición actualizada correctamente", "success")
            logger.info(f"✅ Condición actualizada: Diente {self.selected_tooth}")

        except Exception as e:
            logger.error(f"❌ Error cambiando condición: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostrar_toast(f"Error: {str(e)}", "error")

    @rx.event
    async def edit_consultation_service(self, service_id: str):
        """✏️ Editar servicio de la consulta actual"""
        self.mostrar_toast("Edición próximamente", "info")

    @rx.event
    async def delete_consultation_service(self, service_id: str):
        """
        🗑️ Eliminar servicio de la intervención

        Busca el servicio por ID y lo remueve de la lista usando
        el método unificado remover_servicio_de_intervencion()

        Args:
            service_id: ID del servicio a eliminar
        """
        try:
            # Buscar el índice del servicio por id
            index_to_remove = -1
            for idx, servicio in enumerate(self.servicios_en_intervencion):
                if servicio.id_servicio == service_id:
                    index_to_remove = idx
                    break

            # Llamar al método unificado del estado_intervencion_servicios
            if index_to_remove >= 0:
                exito = self.remover_servicio_de_intervencion(index_to_remove)
                if exito:
                    self.mostrar_toast("Servicio eliminado exitosamente", "success")
                    logger.info(f"✅ Servicio {service_id} eliminado del índice {index_to_remove}")
                else:
                    self.mostrar_toast("Error al eliminar servicio", "error")
            else:
                logger.warning(f"⚠️ Servicio {service_id} no encontrado en la lista")
                self.mostrar_toast("Servicio no encontrado", "warning")

        except Exception as e:
            logger.error(f"❌ Error eliminando servicio: {e}")
            self.mostrar_toast("Error al eliminar servicio", "error")

    @rx.event
    async def cargar_historial_paciente(self, paciente_id: str = None):
        """Cargar historial de servicios del paciente actual"""
        try:
            self.historial_loading = True

            pid = paciente_id or self.paciente_actual.id
            if not pid:
                logger.warning("⚠️ No hay paciente actual para cargar historial")
                return

            logger.info(f"📋 Cargando historial para paciente {pid}")

            historial_raw = await odontologia_service.get_historial_servicios_paciente(pid)

            self.historial_intervenciones = [
                HistorialServicioModel.from_dict(item) for item in historial_raw
            ]

            logger.info(f"✅ Historial cargado: {len(self.historial_intervenciones)} servicios")

        except Exception as e:
            logger.error(f"❌ Error cargando historial: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.historial_loading = False

    def filtrar_historial_por_diente(self, numero_diente: int):
        """Filtrar historial por diente seleccionado"""
        self.historial_filtrado_por_diente = numero_diente
        logger.info(f"🔍 Filtrando historial por diente {numero_diente}")

    def limpiar_filtro_historial(self):
        """Limpiar filtro de diente"""
        self.historial_filtrado_por_diente = None
        logger.info("🔄 Filtro de historial limpiado")

    @rx.var
    def historial_filtrado(self) -> List[HistorialServicioModel]:
        """Historial filtrado según diente seleccionado o todos los servicios"""
        if not self.historial_filtrado_por_diente:
            return self.historial_intervenciones

        return [
            servicio for servicio in self.historial_intervenciones
            if servicio.diente_numero == self.historial_filtrado_por_diente
            or servicio.alcance == "boca_completa"
        ]

    @rx.var
    def tiene_filtro_activo(self) -> bool:
        """Indica si hay filtro de diente activo"""
        return self.historial_filtrado_por_diente is not None

    @rx.var
    def nombre_diente_filtrado(self) -> str:
        """Nombre legible del diente filtrado"""
        if not self.historial_filtrado_por_diente:
            return ""

        nombres_dientes = {
            # Cuadrante 1 (Superior Derecho)
            18: "Tercer Molar Superior Derecho",
            17: "Segundo Molar Superior Derecho",
            16: "Primer Molar Superior Derecho",
            15: "Segundo Premolar Superior Derecho",
            14: "Primer Premolar Superior Derecho",
            13: "Canino Superior Derecho",
            12: "Incisivo Lateral Superior Derecho",
            11: "Incisivo Central Superior Derecho",
            # Cuadrante 2 (Superior Izquierdo)
            21: "Incisivo Central Superior Izquierdo",
            22: "Incisivo Lateral Superior Izquierdo",
            23: "Canino Superior Izquierdo",
            24: "Primer Premolar Superior Izquierdo",
            25: "Segundo Premolar Superior Izquierdo",
            26: "Primer Molar Superior Izquierdo",
            27: "Segundo Molar Superior Izquierdo",
            28: "Tercer Molar Superior Izquierdo",
            # Cuadrante 3 (Inferior Izquierdo)
            38: "Tercer Molar Inferior Izquierdo",
            37: "Segundo Molar Inferior Izquierdo",
            36: "Primer Molar Inferior Izquierdo",
            35: "Segundo Premolar Inferior Izquierdo",
            34: "Primer Premolar Inferior Izquierdo",
            33: "Canino Inferior Izquierdo",
            32: "Incisivo Lateral Inferior Izquierdo",
            31: "Incisivo Central Inferior Izquierdo",
            # Cuadrante 4 (Inferior Derecho)
            41: "Incisivo Central Inferior Derecho",
            42: "Incisivo Lateral Inferior Derecho",
            43: "Canino Inferior Derecho",
            44: "Primer Premolar Inferior Derecho",
            45: "Segundo Premolar Inferior Derecho",
            46: "Primer Molar Inferior Derecho",
            47: "Segundo Molar Inferior Derecho",
            48: "Tercer Molar Inferior Derecho",
        }

        return nombres_dientes.get(
            self.historial_filtrado_por_diente,
            f"Diente {self.historial_filtrado_por_diente}"
        )

    # ==========================================
    # 📊 MÉTODO PARA DASHBOARD ODONTÓLOGO (NUEVO 2025-10-30)
    # ==========================================

    @rx.event
    async def cargar_dashboard_odontologo_completo(self):
        """
        🦷 CARGAR DASHBOARD COMPLETO DEL ODONTÓLOGO

        Carga todas las estadísticas y datos para el dashboard:
        - Stats para los 5 cards
        - Datos de gráficos (últimos 30 días)
        - Top servicios aplicados hoy
        """
        
        try:
                self.cargando_dashboard_odontologo = True
                print(f"🦷 Cargando dashboard para odontólogo: {self.id_personal}")

                # Importar el servicio de dashboard
                from dental_system.services.dashboard_service import dashboard_service

                # Validar que tengamos el id_personal
                if not self.id_personal:
                    logger.warning("⚠️ No hay id_personal disponible para cargar dashboard")
                    self.mostrar_toast("Error: No se pudo identificar al odontólogo", "error")
                    return

                # 1. Cargar estadísticas para los 5 cards
                stats = await dashboard_service.get_odontologo_stats_simple(self.id_personal)
                self.dashboard_stats_odontologo = stats
                print(f"✅ Stats cargadas: {len(stats)} métricas")

                # 2. Cargar datos para gráficos (últimos 30 días)
                chart_data = await dashboard_service.get_odontologo_chart_data(self.id_personal)
                self.consultas_data_odontologo = chart_data.get("consultas_data", [])
                self.ingresos_data_odontologo = chart_data.get("ingresos_data", [])
                print(f"✅ Datos de gráficos cargados: {len(self.consultas_data_odontologo)} puntos")

                # 3. Cargar top servicios aplicados hoy
                top_servicios = await dashboard_service.get_odontologo_top_servicios(self.id_personal, limit=5)
                self.top_servicios_odontologo = top_servicios
                print(f"✅ Top servicios cargados: {len(top_servicios)} servicios")

                print("✅ Dashboard del odontólogo cargado exitosamente")

        except Exception as e:
                logger.error(f"❌ Error cargando dashboard del odontólogo: {e}")
                import traceback
                traceback.print_exc()
                self.mostrar_toast(f"Error cargando dashboard: {str(e)}", "error")

        finally:
                self.cargando_dashboard_odontologo = False
