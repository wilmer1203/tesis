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
from datetime import date, datetime, time
from typing import Dict, Any, List, Optional, Union
import logging

# Servicios y modelos
from dental_system.services.consultas_service import consultas_service
from dental_system.models import (
    ConsultaModel,
    TurnoModel, 
    ConsultasStatsModel,
    MotivosConsultaModel,
    PacienteModel,
    PersonalModel,
    ConsultaFormModel
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
    consulta_seleccionada: ConsultaModel = ConsultaModel()
    id_consulta_seleccionada: str = ""
    
    # Formulario de consulta (datos temporales)
    formulario_consulta: Dict[str, Any] = {}
    formulario_consulta_data: ConsultaFormModel = ConsultaFormModel()
    errores_validacion_consulta: Dict[str, str] = {}
    
    # Variables auxiliares para operaciones
    consulta_para_eliminar: Optional[ConsultaModel] = None
    cargando_lista_consultas: bool = False
    
    # ==========================================
    # 📅 SISTEMA DE TURNOS POR ORDEN DE LLEGADA
    # ==========================================
    
    # Cola de espera por odontólogo
    turnos_por_odontologo: Dict[str, List[TurnoModel]] = {}
    odontologo_seleccionado: str = ""
    
    # Estados de atención
    consulta_en_curso: Optional[ConsultaModel] = None
    id_consulta_en_curso: str = ""
    
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
    
    # Filtros por personal
    filtro_odontologo_consultas: str = ""
    solo_mis_consultas: bool = False  # Para odontólogos
    
    # Búsqueda avanzada
    termino_busqueda_consultas: str = ""
    buscar_por_paciente: str = ""
    buscar_por_diagnostico: str = ""
    
    # Variables adicionales para UI
    pacientes_search_modal: str = ""
    consulta_form: Dict[str, Any] = {
        "paciente_id": "",
        "odontologo_id": "",
        "motivo_consulta": "",
        "tipo_consulta": "",
        "prioridad": "rutina",
        "observaciones": ""
    }
    
    # Variables de mensajes
    success_message: str = ""
    error_message: str = ""
    
    # ==========================================
    # 📅 ESTADÍSTICAS Y MÉTRICAS CACHE
    # ==========================================
    
    # Estadísticas principales
    estadisticas_consultas: ConsultasStatsModel = ConsultasStatsModel()
    ultima_actualizacion_stats_consultas: str = ""
    
    # Métricas de productividad
    total_completadas_hoy: int = 0
    ingresos_estimados_hoy: float = 0.0
    tiempo_total_atencion_hoy: float = 0.0
    
    # Cache de consultas por odontólogo
    cache_consultas_odontologo: Dict[str, List[ConsultaModel]] = {}
    cache_timestamp_consultas: str = ""
    
    # Estados de carga
    cargando_consultas: bool = False
    cargando_turnos: bool = False
    cargando_estadisticas_consultas: bool = False
    actualizando_estado_consulta: bool = False
    
    # ==========================================
    # 📅 COMPUTED VARS PARA UI (SIN ASYNC)
    # ==========================================
    
    @rx.var(cache=True)
    def consultas_filtradas(self) -> List[ConsultaModel]:
        """🔍 Consultas filtradas según criterios actuales"""
        consultas = self.lista_consultas
        
        # Filtrar por búsqueda
        if self.termino_busqueda_consultas:
            consultas = [
                c for c in consultas 
                if (self.termino_busqueda_consultas.lower() in c.motivo_consulta.lower() or
                    self.termino_busqueda_consultas.lower() in c.diagnostico_preliminar.lower())
            ]
        
        # Filtrar por estado
        if self.filtro_estado_consultas != "todas":
            consultas = [c for c in consultas if c.estado == self.filtro_estado_consultas]
        
        # Filtrar por odontólogo
        if self.filtro_odontologo_consultas:
            consultas = [c for c in consultas if c.odontologo_id == self.filtro_odontologo_consultas]
        
        return consultas
    
    @rx.var(cache=True)
    def consultas_pendientes(self) -> List[ConsultaModel]:
        """⏳ Consultas pendientes por atender"""
        return [c for c in self.lista_consultas if c.estado == "programada"]
    
    @rx.var(cache=True)
    def consultas_en_progreso(self) -> List[ConsultaModel]:
        """🔄 Consultas actualmente en progreso"""
        return [c for c in self.lista_consultas if c.estado == "en_progreso"]
    
    @rx.var(cache=True)
    def consultas_completadas_hoy(self) -> List[ConsultaModel]:
        """✅ Consultas completadas hoy"""
        hoy = date.today()
        return [
            c for c in self.lista_consultas 
            if c.estado == "completada" and c.fecha_consulta.date() == hoy
        ]
    
    @rx.var(cache=True)
    def lista_turnos_hoy(self) -> List[TurnoModel]:
        """🔄 Lista de turnos del día"""
        # Extraer turnos de todos los odontólogos para hoy
        turnos_hoy = []
        for turnos_odontologo in self.turnos_por_odontologo.values():
            turnos_hoy.extend(turnos_odontologo)
        return sorted(turnos_hoy, key=lambda t: t.orden_llegada)
    
    @rx.var(cache=True)
    def proximo_numero_turno(self) -> int:
        """🔢 Próximo número de turno disponible"""
        return self.siguiente_numero_turno
    
    @rx.var(cache=True)
    def consulta_seleccionada_valida(self) -> bool:
        """✅ Validar si hay consulta seleccionada"""
        return (
            hasattr(self.consulta_seleccionada, 'id') and 
            bool(self.consulta_seleccionada.id)
        )
    
    # ==========================================
    # 📅 MÉTODOS PRINCIPALES DE CRUD
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
        
        # Verificar cache válido
        if not forzar_refresco and self._cache_consultas_valido(odontologo_id or "todos"):
            print("✅ Usando cache de consultas válido")
            return
        
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
            
            # Actualizar cache timestamp
            self.cache_timestamp_consultas = datetime.now().isoformat()
            
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
    async def crear_consulta(self, datos_formulario: Dict[str, Any]):
        """
        ➕ CREAR NUEVA CONSULTA (REGISTRO POR ORDEN DE LLEGADA)
        
        Args:
            datos_formulario: Datos del formulario de nueva consulta
        """
        print("➕ Creando nueva consulta por orden de llegada...")
        
        self.cargando_turnos = True
        self.errores_validacion_consulta = {}
        
        try:
            # Obtener contexto de usuario
            estado_auth = self.get_state("EstadoAuth")
            if not estado_auth.sesion_valida:
                raise ValueError("Sesión no válida para crear consulta")
            
            # Validar datos requeridos
            errores = self._validar_formulario_consulta(datos_formulario)
            if errores:
                self.errores_validacion_consulta = errores
                return
            
            # Asignar número de turno automáticamente
            numero_turno = self._obtener_siguiente_numero_turno(
                datos_formulario.get("odontologo_id", "")
            )
            datos_formulario["orden_llegada"] = numero_turno
            datos_formulario["estado"] = "programada"  # Esperando por orden de llegada
            
            # Crear consulta usando el servicio
            consulta_nueva = await consultas_service.create_consultation(
                datos_formulario,
                estado_auth.id_usuario
            )
            
            # Actualizar listas locales
            self.lista_consultas.append(consulta_nueva)
            self.consultas_hoy.append(consulta_nueva)
            self.total_consultas += 1
            
            # Actualizar sistema de turnos
            self._actualizar_turnos_por_odontologo()
            
            # Invalidar cache
            self._invalidar_cache_consultas()
            
            # Mostrar feedback de éxito
            estado_ui = self.get_state("EstadoUI")
            if hasattr(estado_ui, 'mostrar_toast'):
                estado_ui.mostrar_toast(
                    f"Consulta creada - Turno #{numero_turno}",
                    "success"
                )
            
            print(f"✅ Consulta creada con turno #{numero_turno}")
            return consulta_nueva
            
        except Exception as e:
            error_msg = f"Error creando consulta: {str(e)}"
            self.errores_validacion_consulta["general"] = error_msg
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.cargando_turnos = False
    
    @rx.event
    async def iniciar_atencion_consulta(self, id_consulta: str):
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
            odontologo_id = consulta.odontologo_id
            if self._odontologo_tiene_consulta_en_curso(odontologo_id):
                raise ValueError("El odontólogo ya tiene una consulta en curso")
            
            # Actualizar estado a en_curso
            datos_actualizacion = {
                "estado": "en_curso",
                "hora_inicio": datetime.now().time().isoformat(),
                "fecha_consulta": date.today().isoformat()
            }
            
            consulta_actualizada = await consultas_service.update_consultation(
                id_consulta,
                datos_actualizacion
            )
            
            # Actualizar listas locales
            self._actualizar_consulta_en_listas(id_consulta, consulta_actualizada)
            
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
    
    @rx.event
    async def completar_consulta(self, id_consulta: str, datos_finalizacion: Dict[str, Any]):
        """
        ✅ COMPLETAR CONSULTA Y REGISTRAR RESULTADOS
        
        Args:
            id_consulta: ID de la consulta a completar
            datos_finalizacion: Datos del diagnóstico, tratamiento, etc.
        """
        print(f"✅ Completando consulta {id_consulta}...")
        
        self.actualizando_estado_consulta = True
        
        try:
            # Preparar datos de finalización
            datos_actualizacion = {
                **datos_finalizacion,
                "estado": "completada",
                "hora_fin": datetime.now().time().isoformat(),
                "fecha_consulta": date.today().isoformat()
            }
            
            # Actualizar consulta usando el servicio
            consulta_completada = await consultas_service.update_consultation(
                id_consulta,
                datos_actualizacion
            )
            
            # Actualizar listas locales
            self._actualizar_consulta_en_listas(id_consulta, consulta_completada)
            
            # Limpiar consulta en curso si era esta
            if self.id_consulta_en_curso == id_consulta:
                self.consulta_en_curso = None
                self.id_consulta_en_curso = ""
            
            # Actualizar métricas
            self.total_completadas_hoy += 1
            self._actualizar_metricas_dia()
            
            # Actualizar sistema de turnos
            self._actualizar_turnos_por_odontologo()
            
            print(f"✅ Consulta {id_consulta} completada correctamente")
            
        except Exception as e:
            error_msg = f"Error completando consulta: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.actualizando_estado_consulta = False
    
    @rx.event
    async def cancelar_consulta(self, id_consulta: str, motivo_cancelacion: str):
        """
        ❌ CANCELAR CONSULTA CON MOTIVO
        
        Args:
            id_consulta: ID de la consulta a cancelar
            motivo_cancelacion: Motivo de la cancelación
        """
        print(f"❌ Cancelando consulta {id_consulta}...")
        
        self.actualizando_estado_consulta = True
        
        try:
            datos_cancelacion = {
                "estado": "cancelada",
                "observaciones": f"Cancelada: {motivo_cancelacion}",
                "fecha_consulta": date.today().isoformat()
            }
            
            consulta_cancelada = await consultas_service.update_consultation(
                id_consulta,
                datos_cancelacion
            )
            
            # Actualizar listas locales
            self._actualizar_consulta_en_listas(id_consulta, consulta_cancelada)
            
            # Limpiar consulta en curso si era esta
            if self.id_consulta_en_curso == id_consulta:
                self.consulta_en_curso = None
                self.id_consulta_en_curso = ""
            
            # Actualizar sistema de turnos
            self._actualizar_turnos_por_odontologo()
            
            print(f"✅ Consulta {id_consulta} cancelada: {motivo_cancelacion}")
            
        except Exception as e:
            error_msg = f"Error cancelando consulta: {str(e)}"
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
        print(f"👨‍⚕️ Odontólogo seleccionado: {odontologo_id}")
        
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
            odontologo_id = consulta.odontologo_id
            
            if odontologo_id not in self.turnos_por_odontologo:
                self.turnos_por_odontologo[odontologo_id] = []
            
            # Crear objeto turno
            turno = TurnoModel(
                numero_turno=consulta.orden_llegada or 0,
                consulta_id=consulta.id,
                paciente_nombre=f"{consulta.paciente_nombre or ''} {consulta.paciente_apellido or ''}".strip(),
                estado=consulta.estado,
                hora_llegada=consulta.hora_inicio or datetime.now().time().isoformat(),
                tiempo_espera=self._calcular_tiempo_espera(consulta)
            )
            
            self.turnos_por_odontologo[odontologo_id].append(turno)
        
        # Ordenar turnos por número
        for odontologo_id in self.turnos_por_odontologo:
            self.turnos_por_odontologo[odontologo_id].sort(
                key=lambda t: t.numero_turno
            )
    
    def _calcular_tiempo_espera(self, consulta: ConsultaModel) -> float:
        """⏱️ Calcular tiempo de espera en minutos"""
        if not consulta.hora_inicio or consulta.estado != "programada":
            return 0.0
        
        try:
            hora_llegada = datetime.strptime(consulta.hora_inicio, "%H:%M:%S").time()
            ahora = datetime.now().time()
            
            # Convertir a minutos desde medianoche
            minutos_llegada = hora_llegada.hour * 60 + hora_llegada.minute
            minutos_ahora = ahora.hour * 60 + ahora.minute
            
            return max(0, minutos_ahora - minutos_llegada)
        except:
            return 0.0
    
    def _odontologo_tiene_consulta_en_curso(self, odontologo_id: str) -> bool:
        """🔍 Verificar si odontólogo tiene consulta en curso"""
        for consulta in self.consultas_hoy:
            if (consulta.odontologo_id == odontologo_id and 
                consulta.estado == "en_curso"):
                return True
        return False
    
    # ==========================================
    # 📅 BÚSQUEDAS Y FILTROS
    # ==========================================
    
    @rx.event
    async def buscar_consultas(self, termino: str):
        """
        🔍 BÚSQUEDA PRINCIPAL DE CONSULTAS
        
        Args:
            termino: Término de búsqueda
        """
        self.termino_busqueda_consultas = termino.strip()
        print(f"🔍 Búsqueda de consultas: '{self.termino_busqueda_consultas}'")
        
        # Aplicar filtros con búsqueda
        await self._aplicar_filtros_internos()
    
    @rx.event
    async def aplicar_filtros_consultas(self, filtros: Dict[str, Any]):
        """
        🎛️ APLICAR FILTROS AVANZADOS DE CONSULTAS
        
        Args:
            filtros: Diccionario con filtros a aplicar
        """
        self.filtro_estado_consulta = filtros.get("estado", "todas")
        self.filtro_tipo_consulta = filtros.get("tipo", "todas")
        self.filtro_odontologo_id = filtros.get("odontologo_id", "")
        self.fecha_consulta_filtro = filtros.get("fecha", date.today().isoformat())
        
        print(f"🎛️ Filtros de consultas aplicados: {filtros}")
        
        await self._aplicar_filtros_internos()
    
    async def _aplicar_filtros_internos(self):
        """🔄 Aplicar filtros internamente"""
        # Recargar consultas con filtros aplicados
        await self.cargar_consultas_hoy(
            odontologo_id=self.filtro_odontologo_id if self.filtro_odontologo_id else None,
            forzar_refresco=True
        )
    
    @rx.event
    def limpiar_filtros_consultas(self):
        """🧹 LIMPIAR TODOS LOS FILTROS DE CONSULTAS"""
        self.termino_busqueda_consultas = ""
        self.filtro_estado_consulta = "todas"
        self.filtro_tipo_consulta = "todas"
        self.filtro_odontologo_id = ""
        self.fecha_consulta_filtro = date.today().isoformat()
        self.buscar_por_paciente = ""
        self.buscar_por_diagnostico = ""
        
        print("🧹 Filtros de consultas limpiados")
    
    # ==========================================
    # 📅 COMPUTED VARS CON CACHE
    # ==========================================
    
    @rx.var(cache=True)
    def consultas_pendientes_hoy(self) -> List[ConsultaModel]:
        """⏳ Consultas pendientes (programadas) del día"""
        return [c for c in self.consultas_hoy if c.estado == "programada"]
    
    @rx.var(cache=True)
    def consultas_en_curso_hoy(self) -> List[ConsultaModel]:
        """🏥 Consultas en curso del día"""
        return [c for c in self.consultas_hoy if c.estado == "en_curso"]
    
    @rx.var(cache=True)
    def consultas_completadas_hoy_lista(self) -> List[ConsultaModel]:
        """✅ Consultas completadas del día"""
        return [c for c in self.consultas_hoy if c.estado == "completada"]
    
    @rx.var(cache=True)
    def consultas_completadas_list(self) -> List[ConsultaModel]:
        """✅ Alias para consultas completadas (compatibilidad UI)"""
        return self.consultas_completadas_hoy_lista
    
    @rx.var(cache=True)
    def consultas_canceladas_list(self) -> List[ConsultaModel]:
        """❌ Lista de consultas canceladas hoy"""
        return [c for c in self.consultas_hoy if c.estado == "cancelada"]
    
    @rx.var(cache=True)
    def show_consulta_modal(self) -> bool:
        """🪟 Estado del modal de consulta (delegado a EstadoUI)"""
        return self.modal_crear_consulta_abierto  # Acceso directo por mixin

    @rx.var(cache=True)
    def consultas_canceladas(self) -> int:
        """❌ Número de consultas canceladas hoy"""
        return len(self.consultas_canceladas_list)
    
    @rx.var(cache=True)
    def total_turnos_pendientes(self) -> int:
        """📊 Total de turnos pendientes"""
        return len(self.consultas_pendientes_hoy)
    
    @rx.var(cache=True)
    def promedio_tiempo_espera(self) -> float:
        """⏱️ Promedio de tiempo de espera en minutos"""
        if not self.consultas_pendientes_hoy:
            return 0.0
        
        tiempos = [self._calcular_tiempo_espera(c) for c in self.consultas_pendientes_hoy]
        return sum(tiempos) / len(tiempos) if tiempos else 0.0
    
    @rx.var(cache=True)
    def turnos_odontologo_seleccionado(self) -> List[TurnoModel]:
        """👨‍⚕️ Turnos del odontólogo seleccionado"""
        if not self.odontologo_seleccionado:
            return []
        
        return self.turnos_por_odontologo.get(self.odontologo_seleccionado, [])
    
    @rx.var(cache=True)
    def siguiente_turno_odontologo(self) -> Optional[TurnoModel]:
        """⏭️ Siguiente turno para odontólogo seleccionado"""
        turnos = self.turnos_odontologo_seleccionado
        turnos_pendientes = [t for t in turnos if t.estado == "programada"]
        
        if turnos_pendientes:
            return min(turnos_pendientes, key=lambda t: t.numero_turno)
        
        return None
    
    @rx.var(cache=True)
    def resumen_dia_actual(self) -> Dict[str, Any]:
        """📊 Resumen completo del día actual"""
        return {
            "total_consultas": len(self.consultas_hoy),
            "pendientes": len(self.consultas_pendientes_hoy),
            "en_curso": len(self.consultas_en_curso_hoy),
            "completadas": len(self.consultas_completadas_hoy_lista),
            "canceladas": len([c for c in self.consultas_hoy if c.estado == "cancelada"]),
            "tiempo_promedio_espera": self.promedio_tiempo_espera,
            "ingresos_estimados": self.ingresos_estimados_hoy
        }
    
    # ==========================================
    # 📅 UTILIDADES Y MÉTODOS INTERNOS
    # ==========================================
    
    def _validar_formulario_consulta(self, datos: Dict[str, Any]) -> Dict[str, str]:
        """✅ Validar datos del formulario de consulta"""
        errores = {}
        
        if not datos.get("paciente_id"):
            errores["paciente_id"] = "Paciente es requerido"
        
        if not datos.get("odontologo_id"):
            errores["odontologo_id"] = "Odontólogo es requerido"
        
        if not datos.get("motivo_consulta", "").strip():
            errores["motivo_consulta"] = "Motivo de consulta es requerido"
        
        return errores
    
    def _buscar_consulta_por_id(self, id_consulta: str) -> Optional[ConsultaModel]:
        """🔍 Buscar consulta por ID en listas locales"""
        for consulta in self.lista_consultas:
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
        self.total_completadas_hoy = len(self.consultas_completadas_hoy_lista)
        self.total_turnos_dia = len(self.consultas_hoy)
        self.turnos_completados_dia = self.total_completadas_hoy
        
        # Calcular ingresos estimados (simplificado)
        self.ingresos_estimados_hoy = sum(
            float(c.costo_consulta or 0) 
            for c in self.consultas_completadas_hoy_lista
        )
    
    def _cache_consultas_valido(self, clave_cache: str) -> bool:
        """⏰ Verificar si el cache de consultas es válido"""
        if not self.cache_timestamp_consultas:
            return False
        
        try:
            timestamp_cache = datetime.fromisoformat(self.cache_timestamp_consultas)
            tiempo_transcurrido = datetime.now() - timestamp_cache
            return tiempo_transcurrido.total_seconds() < 300  # 5 minutos
        except:
            return False
    
    def _invalidar_cache_consultas(self):
        """🗑️ Invalidar cache de consultas"""
        self.cache_timestamp_consultas = ""
        self.cache_consultas_odontologo = {}
        print("🗑️ Cache de consultas invalidado")
    
    # ==========================================
    # 📅 MÉTODOS DE ESTADÍSTICAS
    # ==========================================
    
    @rx.event
    async def cargar_estadisticas_consultas(self, forzar_refresco: bool = False):
        """
        📊 CARGAR ESTADÍSTICAS DE CONSULTAS
        
        Args:
            forzar_refresco: Forzar recálculo de estadísticas
        """
        self.cargando_estadisticas_consultas = True
        
        try:
            # Obtener estadísticas desde el servicio
            stats = await consultas_service.get_consultations_stats()
            
            self.estadisticas_consultas = stats
            self.ultima_actualizacion_stats_consultas = datetime.now().isoformat()
            
            print("✅ Estadísticas de consultas actualizadas")
            
        except Exception as e:
            error_msg = f"Error cargando estadísticas: {str(e)}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            
        finally:
            self.cargando_estadisticas_consultas = False
    
    # ==========================================
    # 📅 MÉTODOS AUXILIARES PARA APPSTATE
    # ==========================================
    
    @rx.event
    async def cargar_lista_consultas(self):
        """📋 CARGAR LISTA COMPLETA DE CONSULTAS - COORDINACIÓN CON APPSTATE"""
        try:
            self.cargando_lista_consultas = True
            
            # Cargar desde el servicio
            consultas_data = await consultas_service.get_all_consultations()
            
            # Convertir a modelos tipados
            self.lista_consultas = [
                ConsultaModel.from_dict(consulta) 
                for consulta in consultas_data
            ]
            self.total_consultas = len(self.lista_consultas)
            
            # Actualizar consultas de hoy
            hoy = date.today()
            self.consultas_hoy = [
                c for c in self.lista_consultas 
                if c.fecha_consulta.date() == hoy
            ]
            
            logger.info(f"✅ {len(self.lista_consultas)} consultas cargadas")
            
        except Exception as e:
            logger.error(f"❌ Error cargando consultas: {str(e)}")
        finally:
            self.cargando_lista_consultas = False
    
    @rx.event
    async def actualizar_estado_consulta_intervencion(self, consulta_id: str, nuevo_estado: str):
        """🔧 ACTUALIZAR ESTADO CONSULTA DESDE INTERVENCIÓN"""
        try:
            # Actualizar en la lista local
            for i, consulta in enumerate(self.lista_consultas):
                if consulta.id == consulta_id:
                    consulta_actualizada = ConsultaModel.from_dict({
                        **consulta.__dict__,
                        "estado": nuevo_estado
                    })
                    self.lista_consultas[i] = consulta_actualizada
                    
                    # Si es la seleccionada, actualizarla también
                    if self.consulta_seleccionada.id == consulta_id:
                        self.consulta_seleccionada = consulta_actualizada
                    break
            
            # Actualizar en el servicio
            await consultas_service.update_consultation_status(consulta_id, nuevo_estado)
            
            logger.info(f"✅ Estado de consulta {consulta_id} actualizado a {nuevo_estado}")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando estado consulta: {str(e)}")
    
    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.lista_consultas = []
        self.consultas_hoy = []
        self.total_consultas = 0
        self.consulta_seleccionada = ConsultaModel()
        self.id_consulta_seleccionada = ""
        self.formulario_consulta = {}
        self.formulario_consulta_data = ConsultaFormModel()
        self.errores_validacion_consulta = {}
        self.consulta_para_eliminar = None
        self.cargando_lista_consultas = False
        
        # Limpiar turnos
        self.turnos_por_odontologo = {}
        self.odontologo_seleccionado = ""
        self.consulta_en_curso = None
        self.siguiente_numero_turno = 1
        
        # Limpiar filtros
        self.filtro_estado_consultas = "todas"
        self.filtro_odontologo_consultas = ""
        self.filtro_fecha_consultas = date.today().isoformat()
        self.termino_busqueda_consultas = ""
        self.buscar_por_paciente = ""
        self.buscar_por_diagnostico = ""
        
        # Limpiar cache
        self.cache_consultas_odontologo = {}
        self.cache_timestamp_consultas = ""
        
        logger.info("🧹 Datos de consultas limpiados")
    
    # ==========================================
    # 📅 FUNCIONES ADICIONALES FALTANTES PARA UI
    # ==========================================
    
    @rx.event
    def buscar_pacientes_modal(self, termino: str):
        """🔍 Buscar pacientes en modal"""
        self.pacientes_search_modal = termino
        print(f"🔍 Buscando pacientes en modal: {termino}")
    
    @rx.event
    def update_consulta_form(self, campo: str, valor: str):
        """📝 Actualizar campo del formulario de consulta"""
        self.consulta_form[campo] = valor
        print(f"📝 Formulario consulta actualizado: {campo} = {valor}")
    
    @rx.event
    async def guardar_consulta(self):
        """💾 Guardar nueva consulta"""
        print("💾 Guardando nueva consulta...")
        try:
            await self.crear_consulta(self.consulta_form)
            # Limpiar formulario después de guardar
            self.consulta_form = {
                "paciente_id": "",
                "odontologo_id": "",
                "motivo_consulta": "",
                "tipo_consulta": "",
                "prioridad": "rutina",
                "observaciones": ""
            }
            self.success_message = "Consulta creada exitosamente"
            self.error_message = ""
            print("✅ Consulta guardada exitosamente")
        except Exception as e:
            self.error_message = f"Error guardando consulta: {str(e)}"
            self.success_message = ""
            print(f"❌ Error guardando consulta: {str(e)}")
    
    @rx.event
    def set_show_consulta_modal(self, mostrar: bool):
        """🪟 Controlar visibilidad del modal (manejado por EstadoUI)"""
        print(f"🪟 Modal consulta: {mostrar}")
        # Esta función es un alias para compatibilidad
        # El modal real es manejado por EstadoUI.abrir_modal_consulta()
    
    @rx.event
    def debug_boton_click(self):
        """🔥 Debug: Verificar si el botón funciona"""
        print("🔥 DEBUG: Botón clickeado correctamente")
        print("🔥 DEBUG: Llamando seleccionar_y_abrir_modal_consulta...")
        return self.seleccionar_y_abrir_modal_consulta("")
    
    @rx.event
    async def seleccionar_y_abrir_modal_consulta(self, consulta_id: str = ""):
        """📅 Seleccionar consulta y abrir modal usando EstadoUI correctamente"""
        print("🔥 FUNCIÓN LLAMADA - seleccionar_y_abrir_modal_consulta")
        print(f"🔥 consulta_id recibido: '{consulta_id}'")
        
        try:
            if consulta_id:
                # Modo editar: seleccionar la consulta primero
                consulta = self._buscar_consulta_por_id(consulta_id)
                if consulta:
                    self.consulta_seleccionada = consulta
                    self.id_consulta_seleccionada = consulta_id
                    # Cargar datos en el formulario
                    self.consulta_form = {
                        "paciente_id": consulta.paciente_id,
                        "odontologo_id": consulta.odontologo_id,
                        "motivo_consulta": consulta.motivo_consulta,
                        "tipo_consulta": consulta.tipo_consulta or "",
                        "prioridad": consulta.prioridad or "rutina",
                        "observaciones": consulta.observaciones or ""
                    }
                print("🔥 Llamando abrir_modal_consulta('editar')")
                self.abrir_modal_consulta("editar")
            else:
                # Modo crear: limpiar selección
                self.consulta_seleccionada = ConsultaModel()
                self.id_consulta_seleccionada = ""
                self.consulta_form = {
                    "paciente_id": "",
                    "odontologo_id": "",
                    "motivo_consulta": "",
                    "tipo_consulta": "",
                    "prioridad": "rutina",
                    "observaciones": ""
                }
                print("🔥 Llamando abrir_modal_consulta('crear')")
                self.abrir_modal_consulta("crear")
                print("🔥 Regresó de abrir_modal_consulta('crear')")
                
            print(f"🔥 Modal debería estar abierto: {self.modal_crear_consulta_abierto}")
            print("🔥 FUNCIÓN COMPLETADA EXITOSAMENTE")
            
        except Exception as e:
            print(f"🔥 ERROR: {str(e)}")
            print(f"🔥 Tipo de error: {type(e)}")
            import traceback
            traceback.print_exc()