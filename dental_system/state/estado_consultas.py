"""
📅 ESTADO DE CONSULTAS - SUBSTATE SEPARADO
==========================================

PROPÓSITO: Manejo centralizado y especializado del sistema de consultas
- Gestión de consultas por orden de llegada (NO citas programadas)
- CRUD completo de consultas con validaciones
- Sistema de turnos por odontólogo
- Estados de consulta y transiciones
- Integración con pacientes y personal
- Estadísticas de consultas y productividad

USADO POR: AppState como coordinador principal
PATRÓN: Substate con get_estado_consultas() en AppState
"""

import reflex as rx
from datetime import date, datetime
from typing import Dict, Any, List, Optional
import logging

# Servicios y modelos
from dental_system.services.consultas_service import consultas_service
from dental_system.models import (
    ConsultaModel,
    TurnoModel, 
    PacienteModel,
    ConsultaFormModel,
)

logger = logging.getLogger(__name__)

class EstadoConsultas(rx.State,mixin=True):
    """
    📅 ESTADO ESPECIALIZADO EN GESTIÓN DE CONSULTAS
    
    RESPONSABILIDADES:
    - Sistema de consultas por orden de llegada (NO citas programadas)
    - CRUD completo con validaciones de negocio
    - Gestión de turnos y cola de espera por odontólogo
    - Estados de consulta y transiciones automáticas
    - Integración con pacientes y personal
    - Estadísticas de productividad y métricas
    """
    
    # ==========================================
    # 📅 VARIABLES PRINCIPALES DE CONSULTAS
    # ==========================================
    
    # Lista principal de consultas (modelos tipados)
    lista_consultas: List[ConsultaModel] = []
    consultas_hoy: List[ConsultaModel] = []
    total_consultas: int = 0
    
    # Consulta seleccionada para operaciones
    consulta_seleccionada: Optional[ConsultaModel] = None
    id_consulta_seleccionada: str = ""
    
    # ==========================================
    # 📝 FORMULARIO UNIFICADO INTELIGENTE
    # ==========================================

    # Formulario principal consolidado (mantiene compatibilidad)
    formulario_consulta_data: ConsultaFormModel = ConsultaFormModel()
    errores_validacion_consulta: Dict[str, List[str]] = {}

    # Variables auxiliares
    cargando_lista_consultas: bool = False
    termino_busqueda_pacientes_modal: str = ""

    # Formulario consolidado (nuevas variables)
    formulario_unificado: ConsultaFormModel = ConsultaFormModel()
    errores_formulario: Dict[str, List[str]] = {}
    modo_formulario: str = "crear"
    formulario_activo: bool = False

    # Variables del modal (consolidadas)
    consulta_form_busqueda_paciente: str = ""
    consulta_form_paciente_seleccionado: PacienteModel = PacienteModel()
    consulta_form_prioridad: str = "normal"
    cargando_crear_consulta: bool = False
    
    # ==========================================
    # 📅 SISTEMA DE TURNOS POR ORDEN DE LLEGADA
    # ==========================================
    
    # Cola de espera por odontólogo
    turnos_por_odontologo: Dict[str, List[TurnoModel]] = {}
    odontologo_seleccionado: str = ""
    
    # Estados de atención
    consulta_en_curso: Optional[ConsultaModel] = None
    id_consulta_en_curso: str = ""

    # 🛡️ Protección anti-doble-clic para finalizar consulta
    finalizando_consulta: bool = False
    consulta_siendo_finalizada: str = ""  # ID de la consulta que se está finalizando

    # Métricas de turnos
    siguiente_numero_turno: int = 1
    total_turnos_dia: int = 0
    turnos_completados_dia: int = 0
    tiempo_promedio_atencion: float = 0.0
    
    # ==========================================
    # 📅 FILTROS Y BÚSQUEDAS ESPECIALIZADAS
    # ==========================================
    
    # Filtros de fecha
    filtro_fecha_consultas: str = date.today().isoformat()
    rango_fecha_inicio: str = ""
    rango_fecha_fin: str = ""
    
    # Filtros de estado
    filtro_estado_consultas: str = "todas"  # todas, programada, en_curso, completada, cancelada
    filtro_tipo_consulta: str = "todas"    # todas, primera_vez, control, emergencia, tratamiento

    # Búsqueda avanzada
    termino_busqueda_consultas: str = ""
    buscar_por_paciente: str = ""
    buscar_por_diagnostico: str = ""
   
    # Variables de mensajes
    success_message: str = ""
    error_message: str = ""

    @rx.event
    def set_doctor_seleccionado(self, doctor_id: str):
        """👨‍⚕️ Seleccionar odontólogo activo"""
        self.odontologo_seleccionado = doctor_id
    
    # ==========================================
    # 📅 ESTADÍSTICAS Y MÉTRICAS CACHE
    # ==========================================
    
    ultima_actualizacion_stats_consultas: str = ""
    
    # Métricas de productividad
    total_completadas_hoy: int = 0
    ingresos_estimados_hoy: float = 0.0
    
    # ==========================================
    # 🧠 SISTEMA DE CACHE INTELIGENTE UNIFICADO
    # ==========================================

    # Cache unificado con timestamps independientes
    cache_datos: Dict[str, Dict[str, Any]] = {
        "consultas": {"data": [], "timestamp": "", "validez_minutos": 5},
        "estadisticas": {"data": {}, "timestamp": "", "validez_minutos": 10},
        "turnos": {"data": {}, "timestamp": "", "validez_minutos": 3},
        "por_odontologo": {"data": {}, "timestamp": "", "validez_minutos": 5}
    }

    # Cache especializado para consultas por odontólogo
    cache_consultas_odontologo: Dict[str, List[ConsultaModel]] = {}

    # Estados de carga
    cargando_consultas: bool = False
    cargando_turnos: bool = False
    cargando_estadisticas_consultas: bool = False
    actualizando_estado_consulta: bool = False
    
 
    # ==========================================
    # 📊 COMPUTED VARS ESPECÍFICAS PARA UI (TIPADAS)
    # ==========================================

    @rx.var(cache=True)
    def total_consultas_dashboard(self) -> int:
        """📊 Total de consultas para dashboard"""
        return len(self.lista_consultas)

    @rx.var(cache=True)
    def total_en_espera_dashboard(self) -> int:
        """⏳ Total en espera para dashboard"""
        return len([c for c in self.lista_consultas if c.estado == "en_espera"])

    @rx.var(cache=True)
    def total_en_atencion_dashboard(self) -> int:
        """🔄 Total en atención para dashboard"""
        return len([c for c in self.lista_consultas if c.estado == "en_atencion"])

    @rx.var(cache=True)
    def total_canceladas_dashboard(self) -> int:
        """🚨 Total canceladas para dashboard"""
        return len([c for c in self.lista_consultas if c.prioridad == "canceladas"])

    @rx.var(cache=True)
    def total_completadas_dashboard(self) -> int:
        """✅ Total completadas para dashboard"""
        return len([c for c in self.lista_consultas if c.estado == "completada"])

    @rx.var(cache=True)
    def consultas_completadas_hoy(self) -> List[ConsultaModel]:
        """✅ Lista de consultas completadas hoy"""
        return [c for c in self.consultas_hoy if c.estado == "completada"]

    @rx.var(cache=True)
    def total_odontologos_activos_dashboard(self) -> int:
        """👨‍⚕️ Total odontólogos activos para dashboard"""
        return len(set(c.primer_odontologo_id for c in self.lista_consultas if c.primer_odontologo_id))

    @rx.var(cache=True)
    def consultas_por_odontologo_dict(self) -> Dict[str, List[ConsultaModel]]:
        """📊 Diccionario con consultas agrupadas por odontólogo ORDENADAS por orden_cola_odontologo"""
        resultado = {}
        # ✅ Usar consultas_hoy (todas las del día) en vez de lista_consultas (filtrada)
        for consulta in self.consultas_hoy:
            # ✅ CORREGIDO: Incluir "entre_odontologos" para que Gerente/Admin puedan finalizar
            if consulta.primer_odontologo_id and consulta.estado in ["en_espera", "en_atencion", "entre_odontologos"]:
                doctor_id = consulta.primer_odontologo_id
                if doctor_id not in resultado:
                    resultado[doctor_id] = []
                resultado[doctor_id].append(consulta)

        # ✅ ORDENAR cada lista por orden_cola_odontologo (CRÍTICO para UI)
        for doctor_id in resultado:
            resultado[doctor_id] = sorted(
                resultado[doctor_id],
                key=lambda c: c.orden_cola_odontologo if c.orden_cola_odontologo else 9999
            )

        return resultado

    @rx.var(cache=True)
    def totales_por_odontologo_dict(self) -> Dict[str, int]:
        """📊 Total de consultas por odontólogo"""
        resultado = {}
        for doctor_id, consultas_list in self.consultas_por_odontologo_dict.items():
            resultado[doctor_id] = len(consultas_list)
        return resultado

    @rx.var(cache=True)
    def urgentes_por_odontologo_dict(self) -> Dict[str, int]:
        """🚨 Urgentes por odontólogo"""
        resultado = {}
        for doctor_id, consultas_list in self.consultas_por_odontologo_dict.items():
            urgentes = len([c for c in consultas_list if c.prioridad == "urgente"])
            resultado[doctor_id] = urgentes
        return resultado

    # ==========================================
    # 🛠️ MÉTODOS HELPER RESTAURADOS
    # ==========================================

    @rx.event
    def abrir_modal_nueva_consulta(self):
        """➕ Abrir modal para nueva consulta"""
        logger.info("➕ Abriendo modal nueva consulta")
        # Limpiar formulario
        self.formulario_consulta_data = ConsultaFormModel()
        # Activar modal directamente
        self.modal_crear_consulta_abierto = True
        self.modal_editar_consulta_abierto = False
        logger.info("✅ Modal nueva consulta activado")

    # ==========================================
    # 🚀 MÉTODO PRINCIPAL UNIFICADO - VERSIÓN REFACTORIZADA
    # ==========================================

    @rx.event
    async def operacion_consulta_master(self, accion: str, consulta_id: str = "", datos: Dict[str, Any] = None, opciones: Dict[str, Any] = None):
        """
        🚀 OPERACIÓN MASTER UNIFICADA - Maneja TODAS las operaciones de consultas de forma eficiente

        Reemplaza: crear_consulta, actualizar_consulta, cancelar_consulta, cambiar_estado_consulta, etc.

        Args:
            accion: 'crear', 'actualizar', 'cancelar', 'cambiar_estado', 'transferir'
            consulta_id: ID de consulta (requerido excepto para crear)
            datos: Datos de la operación
            opciones: {forzar_refresco: bool, mostrar_toast: bool, invalidar_cache: bool}
        """
        try:
            opciones = opciones or {}

            # Validar autenticación
            if not self.esta_autenticado:
                raise ValueError("Sesión no válida")

            # Configurar servicio
            consultas_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Variable de resultado
            resultado = None
            mensaje_exito = ""

            # Ejecutar acción específica
            if accion == "crear":
                if not datos:
                    # Validar formulario actual
                    errores = self.formulario_consulta_data.validate_form()
                    if errores:
                        if hasattr(self, 'mostrar_toast'):
                            self.mostrar_toast(f"Errores: {list(errores.keys())}", "error")
                        return {"exito": False, "errores": errores}
                    datos = self.formulario_consulta_data.to_dict()

                resultado = await consultas_service.create_consultation(datos)
                mensaje_exito = "Consulta creada exitosamente"

            elif accion == "cancelar":
                # Método correcto existe: cancel_consultation
                motivo = datos.get("motivo", "Consulta cancelada") if datos else "Cancelada"
                resultado = await consultas_service.cancel_consultation(consulta_id, motivo)
                mensaje_exito = "Consulta cancelada"

            elif accion == "cambiar_estado":
                # CORREGIDO: usar change_consultation_status (no update_consultation_status)
                nuevo_estado = datos["estado"]
                motivo = datos.get("motivo", f"Estado cambiado a {nuevo_estado}")
                exito = await consultas_service.change_consultation_status(consulta_id, nuevo_estado, motivo)
                if exito:
                    resultado = await consultas_service.get_consultation_by_id(consulta_id)
                else:
                    resultado = None
                mensaje_exito = f"Estado actualizado: {nuevo_estado}"

            # Procesar resultado
            if resultado:
                # Invalidar cache y recargar
                self.cache_inteligente("invalidar", "consultas")
                await self.cargar_consultas_hoy(forzar_refresco=True)

                # Limpiar formularios para crear/actualizar
                if accion in ["crear", "actualizar"]:
                    self.formulario_consulta_data = ConsultaFormModel()
                    self.consulta_seleccionada = None
                    self.id_consulta_seleccionada = ""
                    if hasattr(self, 'cerrar_todos_los_modales'):
                        self.cerrar_todos_los_modales()

                # Mostrar mensaje de éxito
                if opciones.get("mostrar_toast", True) and hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast(mensaje_exito, "success")

                logger.info(f"✅ {mensaje_exito} - ID: {consulta_id}")

            else:
                error_msg = f"Error ejecutando {accion}"
                if hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast(error_msg, "error")
                logger.error(f"❌ {error_msg}")      

        except Exception as e:
            error_msg = f"Error en {accion}: {str(e)}"
            logger.error(f"❌ {error_msg}")
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast(error_msg, "error")


    # ==========================================
    # 📅 MÉTODOS CRUD ORIGINALES (LEGACY)
    # ==========================================
    
    @rx.event
    async def cargar_consultas_hoy(self, odontologo_id: str = None, forzar_refresco: bool = False):
        """
        📋 CARGAR CONSULTAS DEL DÍA CON CACHE
        
        Args:
            odontologo_id: Filtrar por odontólogo específico
            forzar_refresco: Forzar recarga desde BD
        """
        print("📅 Cargando consultas del día...")
        
        # Verificar cache inteligente
        clave_cache = f"consultas_{odontologo_id or 'todas'}"
        resultado_cache = self.cache_inteligente("get", "consultas")

        # if not forzar_refresco and resultado_cache["valido"]:
        #     self.lista_consultas = resultado_cache["datos"]
        #     print(f"✅ Usando cache de consultas válido (hace {resultado_cache.get('timestamp', 'N/A')})")
        #     return
        
        self.cargando_consultas = True
        
        try:
            # Obtener datos desde el servicio
            consultas_data = await consultas_service.get_today_consultations(
                odontologo_id=odontologo_id
            )
            
            # Actualizar listas
            if odontologo_id:
                # Filtrar para odontólogo específico
                self.lista_consultas = consultas_data
                self.cache_consultas_odontologo[odontologo_id] = consultas_data
            else:
                # Todas las consultas del día
                self.consultas_hoy = consultas_data
                self.lista_consultas = consultas_data
            
            self.total_consultas = len(consultas_data)
            
            # Actualizar métricas del día
            self._actualizar_metricas_dia()
            
            # Actualizar sistema de turnos
            self._actualizar_turnos_por_odontologo()
            
            # Actualizar cache inteligente
            self.cache_inteligente("set", "consultas", consultas_data)
            
            print(f"✅ {self.total_consultas} consultas cargadas correctamente")
            
        except Exception as e:
            error_msg = f"Error cargando consultas: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
            # Usar datos del cache en caso de error
            if odontologo_id and odontologo_id in self.cache_consultas_odontologo:
                self.lista_consultas = self.cache_consultas_odontologo[odontologo_id]
                print("🔄 Usando datos del cache por error de conexión")
        
        finally:
            self.cargando_consultas = False
    
    @rx.event
    async def crear_consulta(self, datos_formulario: Optional[ConsultaFormModel] = None):
        """📅 LEGACY: Usar operacion_consulta_master('crear') en su lugar"""
        datos = datos_formulario.to_dict() if datos_formulario else None
        return await self.operacion_consulta_master("crear", datos=datos)

    
    @rx.event
    async def iniciar_atencion_consulta(self, id_consulta: str, estado_objetivo: str = "en_curso"):
        """
        🏥 INICIAR ATENCIÓN DE CONSULTA (CAMBIAR A EN_CURSO)
        
        Args:
            id_consulta: ID de la consulta a iniciar
        """
        print(f"🏥 Iniciando atención de consulta {id_consulta}...")
        
        self.actualizando_estado_consulta = True
        
        try:
            # Validar que no hay otra consulta en curso para el mismo odontólogo
            consulta = self._buscar_consulta_por_id(id_consulta)
            if not consulta:
                raise ValueError("Consulta no encontrada")
            
            # Verificar si el odontólogo ya tiene una consulta en curso
            odontologo_id = consulta.primer_odontologo_id
            if self._odontologo_tiene_consulta_en_curso(odontologo_id):
                raise ValueError("El odontólogo ya tiene una consulta en curso")

            # Establecer contexto de usuario en el servicio
            consultas_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )

            # Usar change_consultation_status que SOLO cambia el estado (sin validar campos completos)
            success = await consultas_service.change_consultation_status(
                id_consulta,
                "en_atencion",
                f"Iniciada atención por odontólogo {self.id_personal}"
            )

            if not success:
                raise Exception("No se pudo iniciar la atención de la consulta")

            # Recargar la consulta actualizada desde BD
            consulta_actualizada = await consultas_service.get_consultation_by_id(id_consulta)
            
            # Actualizar listas locales
            self._actualizar_consulta_en_listas(id_consulta, consulta_actualizada)
            await self.cargar_consultas_hoy(forzar_refresco=True)
            # Establecer como consulta en curso
            self.consulta_en_curso = consulta_actualizada
            self.id_consulta_en_curso = id_consulta
            
            # Actualizar métricas
            self._actualizar_metricas_dia()
            
            print(f"✅ Consulta {id_consulta} iniciada correctamente")
            
        except Exception as e:
            error_msg = f"Error iniciando consulta: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.actualizando_estado_consulta = False
    
   
    
    # ==========================================
    # 📅 SISTEMA DE TURNOS Y COLA DE ESPERA
    # ==========================================
    
    @rx.event
    def seleccionar_odontologo(self, odontologo_id: str):
        """
        👨‍⚕️ SELECCIONAR ODONTÓLOGO PARA VER SUS TURNOS
        
        Args:
            odontologo_id: ID del odontólogo a seleccionar
        """
        self.odontologo_seleccionado = odontologo_id 
        # Cargar consultas específicas del odontólogo
        self.cargar_consultas_hoy(odontologo_id=odontologo_id)
    
    def _obtener_siguiente_numero_turno(self, odontologo_id: str) -> int:
        """🔢 Obtener siguiente número de turno para odontólogo"""
        turnos_odontologo = self.turnos_por_odontologo.get(odontologo_id, [])
        
        if not turnos_odontologo:
            return 1
        
        # Encontrar el número más alto y sumar 1
        numero_max = max(turno.numero_turno for turno in turnos_odontologo)
        return numero_max + 1
    
    def _actualizar_turnos_por_odontologo(self):
        """🔄 Actualizar sistema de turnos por odontólogo"""
        self.turnos_por_odontologo = {}
        
        for consulta in self.consultas_hoy:
            # ESQUEMA v4.1: usar primer_odontologo_id
            odontologo_id = consulta.primer_odontologo_id
            
            if odontologo_id not in self.turnos_por_odontologo:
                self.turnos_por_odontologo[odontologo_id] = []
            
            # Crear objeto turno con campos actualizados
            turno = TurnoModel(
                numero_turno=consulta.orden_cola_odontologo or consulta.orden_llegada_general or 0,
                consulta_id=consulta.id,
                paciente_nombre=consulta.paciente_nombre,
                estado_turno=consulta.estado,
                hora_llegada=consulta.fecha_llegada,
                tiempo_espera_minutos=self._calcular_tiempo_espera_consulta(consulta)
            )
            
            self.turnos_por_odontologo[odontologo_id].append(turno)
        
        # Ordenar turnos por número
        for odontologo_id in self.turnos_por_odontologo:
            self.turnos_por_odontologo[odontologo_id].sort(
                key=lambda t: t.numero_turno
            )
    
    def _calcular_tiempo_espera_consulta(self, consulta: ConsultaModel) -> float:
        """⏱️ Calcular tiempo de espera en minutos para consulta - ESQUEMA v4.1"""
        if not consulta.fecha_llegada or consulta.estado != "en_espera":
            return 0.0
        
        try:
            # Intentar parsear fecha completa o solo hora
            if 'T' in consulta.fecha_llegada:
                fecha_llegada = datetime.fromisoformat(consulta.fecha_llegada.replace('Z', '+00:00'))
                hora_llegada = fecha_llegada.time()
            else:
                hora_llegada = datetime.strptime(consulta.fecha_llegada, "%H:%M:%S").time()
            
            ahora = datetime.now().time()
            
            # Convertir a minutos desde medianoche
            minutos_llegada = hora_llegada.hour * 60 + hora_llegada.minute
            minutos_ahora = ahora.hour * 60 + ahora.minute
            
            return max(0, minutos_ahora - minutos_llegada)
        except:
            return 0.0
    
    def _odontologo_tiene_consulta_en_curso(self, odontologo_id: str) -> bool:
        """🔍 Verificar si odontólogo tiene consulta en curso - ESQUEMA v4.1"""
        for consulta in self.consultas_hoy:
            if (consulta.primer_odontologo_id == odontologo_id and 
                consulta.estado == "en_atencion"):
                return True
        return False
    
    
    # ==========================================
    # 📊 COMPUTED VARS PARA DASHBOARD AVANZADO
    # ==========================================
    
    # NOTA: estadisticas_globales_tiempo_real duplicada - usar estadisticas_completas["globales"]
    @rx.var(cache=True)
    def estadisticas_globales_tiempo_real(self) -> Dict[str, Any]:
        """📊 Estadísticas globales DUPLICADA - usar estadisticas_completas["globales"]"""
        try:
            urgentes = len([c for c in self.consultas_hoy if c.prioridad == "urgente"])
            en_espera = len([c for c in self.consultas_hoy if c.estado == "en_espera"])
            en_atencion = len([c for c in self.consultas_hoy if c.estado == "en_atencion"])
            
            return {
                "total_pacientes": len(self.consultas_hoy),
                "urgentes": urgentes,
                "en_espera": en_espera,
                "en_atencion": en_atencion,
                "completadas": len([c for c in self.consultas_hoy if c.estado == "completada"]),
                "dentistas_activos": len(self.odontologos_activos_hoy),
                "tiempo_promedio": round(self.promedio_tiempo_espera, 1),
                "capacidad_usada": min((len(self.consultas_hoy) / 50) * 100, 100)
            }
        except Exception:
            return {
                "total_pacientes": 0, "urgentes": 0, "en_espera": 0, "en_atencion": 0,
                "completadas": 0, "dentistas_activos": 0, "tiempo_promedio": 0.0, "capacidad_usada": 0.0
            }
    
    
    # ==========================================
    # 🔍 COMPUTED VARS PARA BÚSQUEDA DE PACIENTES
    # ==========================================
    
    @rx.var(cache=False)
    def pacientes_filtrados_modal(self) -> List[PacienteModel]:
        """🔍 Lista de pacientes filtrados para modal de nueva consulta"""
  
        
        # Si no hay término de búsqueda, no mostrar nada
        if not self.consulta_form_busqueda_paciente.strip():
            return []
        
        # Si el término es muy corto, esperar más caracteres
        termino = self.consulta_form_busqueda_paciente.strip()
        if len(termino) < 2:
            return []
        
        try:
            # Obtener lista de pacientes desde AppStateapp_state = get_state("dental_system.state.app_state.AppState")
            if not self.lista_pacientes:
                return []
            
            busqueda = termino.lower()
            pacientes_filtrados = []
            
            # Buscar en la lista de pacientes
            for paciente in self.lista_pacientes:
                # Buscar en nombre completo
                primer_nombre = (paciente.primer_nombre or "").lower()
                segundo_nombre = (paciente.segundo_nombre or "").lower() 
                primer_apellido = (paciente.primer_apellido or "").lower()
                segundo_apellido = (paciente.segundo_apellido or "").lower()
                
                # Buscar en número de documento
                numero_doc = (paciente.numero_documento or "").lower()
                
                # Buscar en cualquier parte de los nombres o documento
                match = (busqueda in primer_nombre or 
                        busqueda in segundo_nombre or
                        busqueda in primer_apellido or
                        busqueda in segundo_apellido or
                        busqueda in numero_doc or
                        busqueda in f"{primer_nombre} {primer_apellido}" or
                        busqueda in f"{primer_nombre} {segundo_nombre}" or
                        busqueda in f"{primer_nombre} {segundo_nombre} {primer_apellido}")
                
                if match:
                    pacientes_filtrados.append(paciente)
                    
                    # Limitar resultados para performance
                    if len(pacientes_filtrados) >= 8:
                        break
            
            return pacientes_filtrados
            
        except Exception as e:
            print(f"🚨 Error en pacientes_filtrados_modal: {e}")
            return []
    
    @rx.var
    def pacientes_filtrados_modal_count(self) -> int:
        """🔢 Contador de pacientes filtrados para el modal"""
        return len(self.pacientes_filtrados_modal)
    
    # ==========================================
    # 📅 UTILIDADES Y MÉTODOS INTERNOS
    # ==========================================
    
    def _validar_formulario_consulta_legacy(self, datos: Dict[str, Any]) -> str:
        """✅ Validar datos del formulario de consulta legacy"""
        if not datos.get("paciente_id"):
            return "Paciente es requerido"
        
        if not datos.get("primer_odontologo_id") and not datos.get("odontologo_id"):
            return "Odontólogo es requerido"
        
        if not datos.get("motivo_consulta", "").strip():
            return "Motivo de consulta es requerido"
        
        return ""
    
    def _buscar_consulta_por_id(self, id_consulta: str) -> Optional[ConsultaModel]:
        """🔍 Buscar consulta por ID en TODAS las listas disponibles

        Con mixin=True, busca en:
        - lista_consultas: Todas las consultas del día
        - consultas_asignadas: Consultas asignadas al odontólogo actual
        """
        # Buscar en lista_consultas
        for consulta in self.lista_consultas:
            if consulta.id == id_consulta:
                return consulta

        # Con mixin=True, también buscar en consultas_asignadas
        for consulta in self.consultas_asignadas:
            if consulta.id == id_consulta:
                return consulta

        return None
    
    def _actualizar_consulta_en_listas(self, id_consulta: str, consulta_actualizada: ConsultaModel):
        """🔄 Actualizar consulta en todas las listas locales"""
        # Actualizar en lista principal
        for i, consulta in enumerate(self.lista_consultas):
            if consulta.id == id_consulta:
                self.lista_consultas[i] = consulta_actualizada
                break
        
        # Actualizar en consultas del día
        for i, consulta in enumerate(self.consultas_hoy):
            if consulta.id == id_consulta:
                self.consultas_hoy[i] = consulta_actualizada
                break
    
    def _actualizar_metricas_dia(self):
        """📊 Actualizar métricas del día"""
        self.total_completadas_hoy = len(self.consultas_completadas_hoy)
        self.total_turnos_dia = len(self.consultas_hoy)
        self.turnos_completados_dia = self.total_completadas_hoy

        # Calcular ingresos estimados (simplificado) - ESQUEMA v4.1
        self.ingresos_estimados_hoy = sum(
            float(c.costo_total_bs or 0) + float(c.costo_total_usd or 0) * 36.5  # Conversión aproximada
            for c in self.consultas_completadas_hoy
        )
    
    def cache_inteligente(self, operacion: str, clave: str = "consultas", datos: Any = None, forzar_invalidacion: bool = False) -> Dict[str, Any]:
        """🧠 CACHE INTELIGENTE UNIFICADO - Maneja todo el sistema de cache

        Args:
            operacion: 'get', 'set', 'invalidar', 'validar'
            clave: Tipo de cache ('consultas', 'estadisticas', 'turnos', 'por_odontologo')
            datos: Datos a almacenar (solo para 'set')
            forzar_invalidacion: Fuerza invalidación completa

        Returns:
            Dict con 'valido', 'datos', 'timestamp', etc.
        """
        try:
            if forzar_invalidacion:
                # Limpiar todo el cache
                for cache_key in self.cache_datos:
                    self.cache_datos[cache_key]["timestamp"] = ""
                    self.cache_datos[cache_key]["data"] = {} if cache_key in ["estadisticas", "turnos", "por_odontologo"] else []
                return {"operacion": "invalidacion_completa", "exito": True}

            if clave not in self.cache_datos:
                return {"valido": False, "error": f"Clave de cache '{clave}' no existe"}

            cache_item = self.cache_datos[clave]
            validez_minutos = cache_item.get("validez_minutos", 5)

            if operacion == "validar":
                if not cache_item["timestamp"]:
                    return {"valido": False, "motivo": "Sin timestamp"}

                timestamp_cache = datetime.fromisoformat(cache_item["timestamp"])
                tiempo_transcurrido = datetime.now() - timestamp_cache
                valido = tiempo_transcurrido.total_seconds() < (validez_minutos * 60)

                return {
                    "valido": valido,
                    "timestamp": cache_item["timestamp"],
                    "minutos_transcurridos": tiempo_transcurrido.total_seconds() / 60,
                    "validez_minutos": validez_minutos
                }

            elif operacion == "get":
                validacion = self.cache_inteligente("validar", clave)
                if validacion["valido"]:
                    return {
                        "valido": True,
                        "datos": cache_item["data"],
                        "desde_cache": True,
                        "timestamp": cache_item["timestamp"]
                    }
                else:
                    return {
                        "valido": False,
                        "datos": None,
                        "motivo": validacion.get("motivo", "Cache expirado")
                    }

            elif operacion == "set":
                if datos is not None:
                    cache_item["data"] = datos
                    cache_item["timestamp"] = datetime.now().isoformat()
                    return {
                        "operacion": "set",
                        "exito": True,
                        "timestamp": cache_item["timestamp"],
                        "clave": clave
                    }
                else:
                    return {"operacion": "set", "exito": False, "error": "Datos requeridos para set"}

            elif operacion == "invalidar":
                cache_item["timestamp"] = ""
                cache_item["data"] = {} if clave in ["estadisticas", "turnos", "por_odontologo"] else []
                return {"operacion": "invalidar", "exito": True, "clave": clave}

            else:
                return {"error": f"Operación '{operacion}' no reconocida"}

        except Exception as e:
            logger.error(f"❌ Error en cache_inteligente: {e}")
            return {"error": str(e), "exito": False}
    
  
    # ==========================================
    # 📅 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================
    
    @rx.event
    async def cargar_lista_consultas(self):
        """📋 CARGAR LISTA COMPLETA DE CONSULTAS - COORDINACIÓN CON APPSTATE"""
        try:
            self.cargando_lista_consultas = True

            # Establecer contexto de usuario para el servicio
            consultas_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Cargar consultas según el rol del usuario
            odontologo_id = None
            if self.rol_usuario == "odontologo" and self.id_personal:
                odontologo_id = self.id_personal
                print(f"🦷 Cargando consultas para odontólogo: {odontologo_id}")
            else:
                print(f"👥 Cargando todas las consultas (rol: {self.rol_usuario})")

            # Cargar consultas de hoy desde el servicio
            consultas_data = await consultas_service.get_today_consultations(odontologo_id=odontologo_id)
            
            # Convertir a modelos tipados con validación
            self.lista_consultas = []
            for consulta_data in consultas_data:
                try:
                    # Convertir objeto a diccionario si es necesario
                    if hasattr(consulta_data, '__dict__'):
                        # Es un objeto, convertir a diccionario
                        data_dict = {key: getattr(consulta_data, key) for key in dir(consulta_data) if not key.startswith('_')}
                    elif hasattr(consulta_data, 'dict'):
                        # Es un modelo Pydantic, usar .dict()
                        data_dict = consulta_data.dict()
                    else:
                        # Ya es un diccionario
                        data_dict = consulta_data
                    
                    consulta_model = ConsultaModel.from_dict(data_dict)
                    self.lista_consultas.append(consulta_model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo consulta a modelo: {e}, Data: {consulta_data}")
                    continue
            self.total_consultas = len(self.lista_consultas)
            
            # Actualizar consultas de hoy con validación robusta
            hoy = date.today()
            self.consultas_hoy = []
            for consulta in self.lista_consultas:
                try:
                    if (consulta.fecha_llegada and 
                        consulta.fecha_llegada.strip() and 
                        datetime.fromisoformat(consulta.fecha_llegada.replace('Z', '+00:00')).date() == hoy):
                        self.consultas_hoy.append(consulta)
                except Exception as e:
                    logger.warning(f"Error procesando fecha de consulta {consulta.id}: {e}")
                    continue
            
            logger.info(f"✅ {len(self.lista_consultas)} consultas cargadas")
            
        except Exception as e:
            logger.error(f"❌ Error cargando consultas: {str(e)}")
        finally:
            self.cargando_lista_consultas = False
    

    
    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.lista_consultas = []
        self.consultas_hoy = []
        self.total_consultas = 0
        self.consulta_seleccionada = ConsultaModel()
        self.id_consulta_seleccionada = ""
        self.formulario_consulta_data = ConsultaFormModel()
        self.errores_validacion_consulta = {}
        self.cargando_lista_consultas = False
        
        # Limpiar turnos
        self.turnos_por_odontologo = {}
        self.odontologo_seleccionado = ""
        self.consulta_en_curso = None
        self.siguiente_numero_turno = 1
        
        # Limpiar filtros
        self.filtro_estado_consultas = "todas"
        self.filtro_fecha_consultas = date.today().isoformat()
        self.termino_busqueda_consultas = ""
        self.buscar_por_paciente = ""
        self.buscar_por_diagnostico = ""
        
        # Limpiar cache
        self.cache_consultas_odontologo = {}
        self.cache_inteligente("invalidar", "consultas")
        
        logger.info("🧹 Datos de consultas limpiados")
    
 
    # ==========================================
    # 📅 MÉTODOS DE EDICIÓN SIGUIENDO PATRÓN PERSONAL
    # ==========================================
    
    
    @rx.event
    def set_formulario_consulta_field(self, field: str, value: str):
        """📝 LEGACY: Actualizar campo específico del formulario de consulta"""
        # Mantener compatibilidad con código existente
        if hasattr(self.formulario_consulta_data, field):
            setattr(self.formulario_consulta_data, field, value)
        # Actualizar también el formulario unificado
        if hasattr(self.formulario_unificado, field):
            setattr(self.formulario_unificado, field, value)

    @rx.event
    def gestionar_formulario_unificado(self, accion: str, campo: str = "", valor: Any = None, datos: Dict[str, Any] = None):
        """📝 GESTOR UNIFICADO DE FORMULARIOS - Maneja crear, editar, limpiar, validar

        Args:
            accion: 'set_campo', 'cargar_datos', 'limpiar', 'validar', 'cambiar_modo'
            campo: Nombre del campo a actualizar
            valor: Valor para el campo
            datos: Diccionario completo de datos (para cargar_datos)
        """
        try:
            if accion == "set_campo" and campo and valor is not None:
                if hasattr(self.formulario_unificado, campo):
                    setattr(self.formulario_unificado, campo, valor)
                    # Limpiar errores del campo actualizado
                    if campo in self.errores_formulario:
                        del self.errores_formulario[campo]

            elif accion == "cargar_datos" and datos:
                for campo, valor in datos.items():
                    if hasattr(self.formulario_unificado, campo):
                        setattr(self.formulario_unificado, campo, valor)

            elif accion == "limpiar":
                self.formulario_unificado = ConsultaFormModel()
                self.errores_formulario = {}
                self.consulta_form_paciente_seleccionado = PacienteModel()
                self.modo_formulario = "crear"
                self.formulario_activo = False

            elif accion == "validar":
                self.errores_formulario = self.formulario_unificado.validate_form()
                return len(self.errores_formulario) == 0

            elif accion == "cambiar_modo" and valor:
                self.modo_formulario = str(valor)
                if valor == "crear":
                    self.gestionar_formulario_unificado("limpiar")
                self.formulario_activo = True

            elif accion == "to_dict":
                return self.formulario_unificado.to_dict()

        except Exception as e:
            logger.error(f"❌ Error en gestionar_formulario_unificado ({accion}): {e}")
            
    @rx.event
    def actualizar_campo_paciente_consulta(self, value: str):
        """🔍 Actualizar campo de paciente dependiendo del modo del modal"""
        if self.modal_editar_consulta_abierto:
            self.set_formulario_consulta_field("paciente_nombre", value)
        else:
            self.set_consulta_form_busqueda_paciente(value)
    
    @rx.event  
    async def actualizar_consulta(self):
        """✏️ Actualizar consulta existente"""
        try:
            if not self.consulta_seleccionada or not self.id_consulta_seleccionada:
                logger.warning("⚠️ No hay consulta seleccionada para actualizar")
                return
            
            # Validar formulario
            if not self.formulario_consulta_data.paciente_id:
                self.mostrar_toast("Debe seleccionar un paciente", "error")
                return
            
            if not self.formulario_consulta_data.primer_odontologo_id:
                self.mostrar_toast("Debe seleccionar un odontólogo", "error") 
                return
            
            # Establecer contexto de usuario en el servicio
            consultas_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            
            # Actualizar usando el servicio
            consulta_actualizada = await consultas_service.update_consultation(
                self.id_consulta_seleccionada,
                self.formulario_consulta_data
            )
            
            if consulta_actualizada:
                # Actualizar en la lista local
                for i, consulta in enumerate(self.lista_consultas):
                    if consulta.id == self.id_consulta_seleccionada:
                        self.lista_consultas[i] = consulta_actualizada
                        break
                
                # Actualizar todas las listas de consultas
                await self.cargar_consultas_hoy(forzar_refresco=True)
                
                # Si hay un odontólogo seleccionado en la página, recargar también sus consultas
                if hasattr(self, 'odontologo_seleccionado_id') and self.odontologo_seleccionado_id:
                    await self.cargar_consultas_odontologo(self.odontologo_seleccionado_id)
                    
                # Forzar actualización de computed vars del dashboard si existen
                if hasattr(self, 'recargar_estadisticas'):
                    await self.recargar_estadisticas()
                    
                # Invalidar cache de variables computadas relacionadas con consultas
                if hasattr(self, '_invalidate_computed_vars'):
                    self._invalidate_computed_vars(['consultas_hoy', 'consultas_por_odontologo', 'total_consultas_hoy'])
                
                # Limpiar formulario y cerrar modal
                self.formulario_consulta_data = ConsultaFormModel()
                self.consulta_seleccionada = None
                self.id_consulta_seleccionada = ""
                
                if hasattr(self, 'cerrar_todos_los_modales'):
                    self.cerrar_todos_los_modales()
                
                if hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast("Consulta actualizada exitosamente", "success")
                
                logger.info(f"✅ Consulta {self.id_consulta_seleccionada} actualizada")
                
            
        except Exception as e:
            logger.error(f"❌ Error actualizando consulta: {e}")
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast(f"Error actualizando consulta: {str(e)}", "error")
    
    @rx.event
    async def guardar_consulta_modal(self):
        """💾 Guardar consulta desde formulario modal usando formulario tipado"""
        try:
            # Validar campos obligatorios usando formulario tipado
            if not self.formulario_consulta_data.paciente_id:
                self.mostrar_toast("Complete los campos obligatorios: Paciente requerido", "error")
                return

            if not self.formulario_consulta_data.primer_odontologo_id:
                self.mostrar_toast("Complete los campos obligatorios: Odontólogo requerido", "error")
                return
            
            # Establecer contexto de usuario en el servicio
            consultas_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            
            if self.consulta_seleccionada and self.id_consulta_seleccionada:
                # Modo editar
                await self.actualizar_consulta()
            else:
                # Modo crear usando el formulario tipado
                await self.crear_consulta()

                # Cerrar modal si existe
                if hasattr(self, 'set_modal_crear_consulta_abierto'):
                    self.set_modal_crear_consulta_abierto(False)
                
        except Exception as e:
            logger.error(f"❌ Error guardando consulta: {e}")
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast(f"Error guardando consulta: {str(e)}", "error")
    

    # ==========================================
    # 🎨 GESTIÓN UNIFICADA DE MODALES Y OPERACIONES para tranferir 
    # ==========================================

    # Variables unificadas para modales
    modal_transferir_paciente_abierto: bool = False
    consulta_para_transferir: Optional[ConsultaModel] = None
    odontologo_destino_seleccionado: str = ""
    motivo_transferencia: str = ""

    @rx.event
    def gestionar_modal_operacion(self, accion: str, consulta_id: str = "", datos: Dict[str, Any] = None):
        """🎨 GESTOR UNIFICADO DE MODALES - Maneja transferencia, cancelación, cambios"""
        try:
            consulta_encontrada = None
            if consulta_id:
                consulta_encontrada = next((c for c in self.lista_consultas if c.id == consulta_id), None)

            if accion == "abrir_transferencia":
                if consulta_encontrada:
                    self.consulta_para_transferir = consulta_encontrada
                    self.odontologo_destino_seleccionado = ""
                    self.motivo_transferencia = ""
                    self.modal_transferir_paciente_abierto = True
                    logger.info(f"🔄 Modal transferencia abierto: {consulta_id}")

            elif accion == "cerrar_transferencia":
                self.modal_transferir_paciente_abierto = False
                self.consulta_para_transferir = None
                self.odontologo_destino_seleccionado = ""
                self.motivo_transferencia = ""

            elif accion == "set_odontologo_destino":
                self.odontologo_destino_seleccionado = datos.get("odontologo_id", "") if datos else ""

            elif accion == "set_motivo_transferencia":
                self.motivo_transferencia = datos.get("motivo", "") if datos else ""

            elif accion == "seleccionar_paciente_modal":
                paciente_id = datos.get("paciente_id", "") if datos else ""
                paciente = next((p for p in self.pacientes_filtrados_modal if p.id == paciente_id), None)
                if paciente:
                    self.consulta_form_paciente_seleccionado = paciente
                    self.consulta_form_busqueda_paciente = ""
                    self.set_formulario_consulta_field("paciente_id", paciente.id)
                    self.set_formulario_consulta_field("paciente_nombre", paciente.nombre_completo)

        except Exception as e:
            logger.error(f"❌ Error en gestionar_modal_operacion ({accion}): {e}")
    
    @rx.event
    async def ejecutar_transferencia_paciente(self):
        """🚀 EJECUTAR TRANSFERENCIA DE PACIENTE"""
        try:
            if not self.consulta_para_transferir:
                logger.warning("⚠️ No hay consulta seleccionada para transferir")
                return
            
            if not self.odontologo_destino_seleccionado:
                if hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast("Debe seleccionar un odontólogo destino", "error")
                return
            
            if not self.motivo_transferencia.strip():
                if hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast("Debe proporcionar un motivo para la transferencia", "error")
                return
            
            # Verificar que no sea el mismo odontólogo
            if self.consulta_para_transferir.primer_odontologo_id == self.odontologo_destino_seleccionado:
                if hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast("No puede transferir a la misma cola", "error")
                return
            
            # Usar el método ya existente de cambio de odontólogo
            await self.cambiar_odontologo_consulta(
                self.consulta_para_transferir.id,
                self.odontologo_destino_seleccionado,
                f"Transferencia: {self.motivo_transferencia.strip()}"
            )
            
            # Cerrar modal tras éxito
            self.gestionar_modal_operacion("cerrar_transferencia")
            
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast("Paciente transferido exitosamente", "success")
            
            logger.info(f"✅ Paciente transferido exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error ejecutando transferencia: {e}")
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast(f"Error en transferencia: {str(e)}", "error")

    # ==========================================
    # 🔄 CAMBIO DE ODONTÓLOGO
    # ==========================================
    
    @rx.event
    async def cambiar_odontologo_consulta(self, consulta_id: str, nuevo_odontologo_id: str, motivo: str):
        """🔄 Cambiar odontólogo de una consulta"""
        try:
            if not consulta_id or not nuevo_odontologo_id:
                logger.warning("⚠️ Faltan datos para cambio de odontólogo")
                return
            
            if not motivo or len(motivo.strip()) < 10:
                logger.warning("⚠️ Motivo del cambio debe tener al menos 10 caracteres")
                return
            
            # Establecer contexto de usuario en el servicio
            consultas_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            
            # Usar el método directo de transferencia simplificado
            transferencia_exitosa = await consultas_service.transferir_consulta(
                consulta_id, nuevo_odontologo_id, motivo.strip()
            )
            
            if transferencia_exitosa:
                # Invalidar cache completamente
                self.cache_inteligente("invalidar", "consultas")

                # Limpiar todas las listas para forzar recálculo
                self.consultas_hoy = []
                self.lista_consultas = []
                self.cache_consultas_odontologo = {}

                # Recargar desde cero para forzar la actualización
                await self.cargar_consultas_hoy(forzar_refresco=True)
                
                # Limpiar variables auxiliares
                self.consulta_seleccionada = None
                self.id_consulta_seleccionada = ""
                
                logger.info(f"✅ Consulta {consulta_id} cambiada a odontólogo {nuevo_odontologo_id}")
                
                if hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast("Odontólogo cambiado exitosamente", "success")
            else:
                logger.warning("❌ No se pudo cambiar el odontólogo")
                if hasattr(self, 'mostrar_toast'):
                    self.mostrar_toast("Error cambiando odontólogo", "error")
            
        except Exception as e:
            logger.error(f"❌ Error cambiando odontólogo: {e}")
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast(f"Error: {str(e)}", "error")


    # ==========================================
    # 🔄 MÉTODOS DE REORDENAMIENTO EN COLA
    # ==========================================
    
    @rx.event
    async def subir_en_cola(self, consulta_id: str):
        """⬆️ Subir paciente una posición en la cola de su odontólogo"""
        try:
            logger.info(f"⬆️ Subiendo en cola: {consulta_id}")

            # Buscar la consulta actual
            consulta_actual = next((c for c in self.consultas_hoy if c.id == consulta_id), None)

            if not consulta_actual:
                logger.error("❌ Consulta no encontrada")
                self.mostrar_toast("❌ Consulta no encontrada", "error")
                return

            odontologo_id = consulta_actual.primer_odontologo_id
            orden_actual = consulta_actual.orden_cola_odontologo

            logger.info(f"📍 Orden actual: {orden_actual}, Odontólogo: {odontologo_id}")

            if orden_actual <= 1:
                self.mostrar_toast("⚠️ Ya está en la primera posición", "warning")
                return

            # Usar el servicio para intercambiar posiciones
            from dental_system.services.consultas_service import ConsultasService
            service = ConsultasService()
            service.set_user_context(self.id_usuario, self.perfil_usuario)

            logger.info(f"🔄 Intercambiando posición {orden_actual} → {orden_actual - 1}")

            resultado = await service.intercambiar_orden_cola(
                consulta_id,
                odontologo_id,
                orden_actual,
                orden_actual - 1
            )

            logger.info(f"📊 Resultado del servicio: {resultado}")

            if resultado.get("success"):
                # ✅ INVALIDAR CACHE Y RECARGAR TODAS LAS CONSULTAS (igual que al crear/transferir)
                self.cache_inteligente("invalidar", "consultas")
                await self.cargar_consultas_hoy(forzar_refresco=True)

                self.mostrar_toast("✅ Paciente movido hacia arriba", "success")
                logger.info(f"✅ Intercambio exitoso y lista recargada")
            else:
                error_msg = resultado.get("message", "Error desconocido")
                self.mostrar_toast(f"❌ {error_msg}", "error")
                logger.error(f"❌ Error en intercambio: {error_msg}")

        except Exception as e:
            logger.error(f"❌ Error subiendo en cola: {e}")
            self.mostrar_toast("❌ Error al mover paciente", "error")
    
    @rx.event
    async def bajar_en_cola(self, consulta_id: str):
        """⬇️ Bajar paciente una posición en la cola de su odontólogo"""
        try:
            logger.info(f"⬇️ Bajando en cola: {consulta_id}")

            # Buscar la consulta actual
            consulta_actual = next((c for c in self.consultas_hoy if c.id == consulta_id), None)

            if not consulta_actual:
                logger.error("❌ Consulta no encontrada")
                self.mostrar_toast("❌ Consulta no encontrada", "error")
                return

            odontologo_id = consulta_actual.primer_odontologo_id
            orden_actual = consulta_actual.orden_cola_odontologo

            # Contar total de consultas en esa cola (usar estados correctos)
            total_en_cola = len([c for c in self.consultas_hoy
                               if c.primer_odontologo_id == odontologo_id and c.estado in ["programada", "en_espera"]])

            logger.info(f"📍 Orden actual: {orden_actual}/{total_en_cola}, Odontólogo: {odontologo_id}")

            if orden_actual >= total_en_cola:
                self.mostrar_toast("⚠️ Ya está en la última posición", "warning")
                return

            # Usar el servicio para intercambiar posiciones
            from dental_system.services.consultas_service import ConsultasService
            service = ConsultasService()
            service.set_user_context(self.id_usuario, self.perfil_usuario)

            logger.info(f"🔄 Intercambiando posición {orden_actual} → {orden_actual + 1}")

            resultado = await service.intercambiar_orden_cola(
                consulta_id,
                odontologo_id,
                orden_actual,
                orden_actual + 1
            )

            logger.info(f"📊 Resultado del servicio: {resultado}")

            if resultado.get("success"):
                # ✅ INVALIDAR CACHE Y RECARGAR TODAS LAS CONSULTAS (igual que al crear/transferir)
                self.cache_inteligente("invalidar", "consultas")
                await self.cargar_consultas_hoy(forzar_refresco=True)

                self.mostrar_toast("✅ Paciente movido hacia abajo", "success")
                logger.info(f"✅ Intercambio exitoso y lista recargada")
            else:
                error_msg = resultado.get("message", "Error desconocido")
                self.mostrar_toast(f"❌ {error_msg}", "error")
                logger.error(f"❌ Error en intercambio: {error_msg}")

        except Exception as e:
            logger.error(f"❌ Error bajando en cola: {e}")
            self.mostrar_toast("❌ Error al mover paciente", "error")
            
    @rx.event
    async def completar_consulta_completa(self, consulta_id: str):
        """
        🏥 COMPLETAR CONSULTA + CREAR PAGO (LLAMADA DESDE FRONTEND)
        """
        # 🛡️ PROTECCIÓN 1: Prevenir doble ejecución
        if self.finalizando_consulta and self.consulta_siendo_finalizada == consulta_id:
            logger.warning(f"⚠️ Ya se está finalizando la consulta {consulta_id} - ignorando doble clic")
            return

        try:
            # 🛡️ Marcar como "en proceso de finalización"
            self.finalizando_consulta = True
            self.consulta_siendo_finalizada = consulta_id
            self.cargando_consultas = True

            # Llamar servicio completo
            
            consultas_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            resultado = await consultas_service.complete_consultation_with_payment(
                consulta_id,
                self.id_usuario
            )

            if resultado.get("success"):
                # Mostrar toast de éxito (diferente mensaje si ya existía)
                mensaje = resultado.get("mensaje", "")
                if "ya existía" in mensaje:
                    self.mostrar_toast(
                        f"ℹ️ Pago {resultado.get('numero_recibo')} ya existía - consulta completada",
                        "info"
                    )
                else:
                    self.mostrar_toast(
                        f"✅ Consulta finalizada - Pago {resultado.get('numero_recibo')} creado",
                        "success"
                    )

                # 🔄 FORZAR INVALIDACIÓN DE CACHE DE COMPUTED VARS
                # Limpiar listas base para forzar recálculo
                self.lista_consultas = []
                self.consultas_hoy = []

                # ✅ Recargar datos forzando refresh (sin cache)
                await self.cargar_consultas_hoy(forzar_refresco=True)

                # 🔄 REFRESCAR TAMBIÉN ODONTÓLOGOS (afecta contadores)
                await self.cargar_odontologos_disponibles()

        except ValueError as ve:
            logger.error(f"Error completando consulta: {ve}")
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast(f"❌ {str(ve)}", "error")
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            if hasattr(self, 'mostrar_toast'):
                self.mostrar_toast("Error completando consulta", "error")
        finally:
            # 🛡️ Limpiar flags de protección
            self.finalizando_consulta = False
            self.consulta_siendo_finalizada = ""
            self.cargando_consultas = False