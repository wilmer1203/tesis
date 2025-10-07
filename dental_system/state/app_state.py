"""
🏥 APPSTATE DEFINITIVO - ARQUITECTURA FINAL COMPLETA
====================================================

✅ ARQUITECTURA PERFECTA QUE COMBINA:
- Event handlers async con get_state() (como recomienda Reflex)
- Computed vars sin async para acceso directo desde UI
- Substates existentes preservados (modularidad)
- Zero MRO conflicts
- Máxima performance
- TODOS los módulos con modelos tipados
- Variables y funciones en ESPAÑOL

PATRÓN OFICIAL: Event handlers → async get_state() → coordinación
PATRÓN HÍBRIDO: Computed vars → acceso directo → sin async
"""

import reflex as rx
from datetime import date, datetime
from typing import List, Dict, Any, Optional, Union
import logging
import asyncio

# ✅ IMPORTAR LOS SUBSTATES EXISTENTES
from .estado_auth import EstadoAuth, auth
from .estado_ui import EstadoUI
from .estado_pacientes import EstadoPacientes
from .estado_consultas import EstadoConsultas
from .estado_personal import EstadoPersonal
from .estado_odontologia import EstadoOdontologia
from .estado_servicios import EstadoServicios
from .estado_pagos import EstadoPagos
from .estado_intervencion_servicios import EstadoIntervencionServicios
from .estado_odontograma_avanzado import EstadoOdontogramaAvanzado

# ✅ MODELOS TIPADOS PARA COMPUTED VARS
from dental_system.models import (
    # Modelos principales
    PacienteModel, PersonalModel, ConsultaModel, ServicioModel,
    PagoModel, OdontogramaModel, DienteModel, CondicionDienteModel,
    
    # Modelos de estadísticas
    DashboardStatsModel, AdminStatsModel, GerenteStatsModel,
    OdontologoStatsModel, AsistenteStatsModel, PacientesStatsModel,
    ConsultasStatsModel, PersonalStatsModel, ServicioStatsModel,
    PagosStatsModel,
    
    # Modelos auxiliares
    TurnoModel, IntervencionModel, HistorialClinicoModel,
    CategoriaServicioModel, ConceptoPagoModel, ConsultaConOrdenModel,
    
    # Modelos de formularios  
    PacienteFormModel, ConsultaFormModel, PersonalFormModel,
    ServicioFormModel, PagoFormModel, IntervencionFormModel
)

logger = logging.getLogger(__name__)

class AppState(EstadoIntervencionServicios,EstadoServicios,EstadoPagos,EstadoConsultas,EstadoOdontologia,EstadoPersonal,EstadoAuth, EstadoPacientes,EstadoUI, rx.State):
    """Incluye AdvancedFDIState como mixin - se integra automáticamente"""
    """
    🎯 APPSTATE DEFINITIVO CON MIXINS

    Hereda de todos los substates como mixins:
    - AdvancedFDIState: Odontograma FDI interactivo avanzado
    - EstadoAuth: Autenticación y permisos
    - EstadoUI: Navegación y estados de UI
    - EstadoPacientes: Gestión de pacientes
    - EstadoPersonal: Gestión de empleados
    - EstadoConsultas: Sistema de turnos
    - EstadoServicios: Catálogo de servicios
    - EstadoOdontologia: Módulo dental
    """

    # ==========================================
    # 🦷 VARIABLES ESPECÍFICAS DEL APPSTATE
    # ==========================================

    # Tab activo en página de intervención odontológica
    active_intervention_tab: str = "intervencion"

    # ==========================================
    # 📊 EVENT HANDLERS BÁSICOS PARA COMPATIBILIDAD
    # ==========================================
    
    # ==========================================
    # 🔗 MÉTODOS YA DISPONIBLES VIA MIXINS
    # ==========================================
    
    # ✅ Ya disponible via EstadoUI:
    # - navigate_to(pagina, titulo, subtitulo)
    # - current_page (variable)
    # - abrir_modal(modal_id)
    # - cerrar_modal()
    # - mostrar_toast(mensaje, tipo)
    
    # ✅ Ya disponible via EstadoAuth:
    # - iniciar_sesion(form_data)
    # - cerrar_sesion()
    # - rol_usuario (variable)
    # - esta_autenticado (variable)
    
    # ✅ Ya disponible via otros substates:
    # - cargar_lista_pacientes() (EstadoPacientes)
    # - cargar_lista_personal() (EstadoPersonal)
    # - cargar_estadisticas_consultas() (EstadoConsultas)
 
    # ==========================================
    # 📊 MÉTODOS ADICIONALES PARA DASHBOARD
    # ==========================================
    
    @rx.event
    async def cargar_estadisticas_dashboard(self):
        """📊 Cargar estadísticas del dashboard usando servicio"""
        try:
            from ..services.dashboard_service import DashboardService
            dashboard_service = DashboardService()
            
            # Usar rol actual del usuario autenticado
            rol_usuario = self.rol_usuario
            
            # Cargar estadísticas del servicio
            stats = await dashboard_service.get_dashboard_stats(rol_usuario)
            print(f"📊 Estadísticas cargadas para rol: {rol_usuario}")
            return stats
            
        except Exception as e:
            print(f"❌ Error cargando estadísticas: {str(e)}")
            return {}
    
    @rx.event
    async def post_login_inicializacion(self):
        """🚀 INICIALIZACIÓN COMPLETA DESPUÉS DEL LOGIN - POR ROL

        Carga solo los datos necesarios según el rol del usuario
        para evitar errores de permisos y mejorar rendimiento
        """
        try:
            print("🚀 Iniciando carga de datos post-login...")

            # Datos básicos que TODOS los roles necesitan
            datos_basicos = [
                self.cargar_estadisticas_dashboard(),
            ]

            # Datos específicos por rol
            if self.rol_usuario == "gerente":
                # Gerente: Acceso completo a todo
                datos_especificos = [
                    self.cargar_lista_pacientes(),
                    self.cargar_lista_personal(),
                    self.cargar_estadisticas_personal(),
                    self.cargar_lista_consultas(),
                    self.cargar_servicios_basico(),
                    self.cargar_consultas_pendientes_pago(),
                    self.cargar_estadisticas_duales(),
                ]
            elif self.rol_usuario == "administrador":
                # Administrador: Gestión operativa, sin personal
                datos_especificos = [
                    self.cargar_lista_pacientes(),
                    self.cargar_lista_consultas(),
                    self.cargar_servicios_basico(),
                    self.cargar_consultas_pendientes_pago(),
                    self.cargar_estadisticas_duales(),
                ]
            elif self.rol_usuario == "odontologo":
                # Odontólogo: Solo datos odontológicos, pacientes y servicios
                datos_especificos = [
                    self.cargar_pacientes_asignados(),
                    self.cargar_consultas_disponibles_otros(),
                    self.cargar_servicios_disponibles(),
                    self.cargar_estadisticas_dia(),
                ]
            elif self.rol_usuario == "asistente":
                # Asistente: Solo datos básicos
                datos_especificos = [
                    self.cargar_lista_consultas(),
                ]
            else:
                # Rol desconocido: solo datos básicos
                datos_especificos = []

            # Cargar datos en paralelo para máxima velocidad
            todas_las_tareas = datos_basicos + datos_especificos
            await asyncio.gather(*todas_las_tareas, return_exceptions=True)

            print("✅ Inicialización post-login completada")
            print(f"🎯 Datos cargados para rol: {self.rol_usuario}")

        except Exception as e:
            print(f"⚠️ Error en inicialización post-login: {e}")
            # No lanzar excepción para no bloquear el login
    
    # ==========================================
    # 📅 EVENT HANDLERS MÍNIMOS PARA CONSULTAS
    # ==========================================
    
    @rx.event
    def enfocar_busqueda_consultas(self):
        """🔍 Enfocar campo de búsqueda de consultas"""
        print("🔍 Enfocando búsqueda de consultas")
    
    @rx.event
    async def refrescar_consultas(self):
        """🔄 Refrescar lista de consultas"""
        await self.cargar_lista_consultas()
    
    
    @rx.event
    def ver_historial_paciente(self, paciente_id: str):
        """📋 Ver historial de un paciente"""
        print(f"📋 Viendo historial del paciente: {paciente_id}")
        # TODO: Implementar navegación a historial
    
    @rx.event
    def llamar_paciente(self, telefono: str):
        """📞 Acción para llamar a un paciente"""
        print(f"📞 Llamando a paciente: {telefono}")
        # TODO: Integrar con sistema de llamadas
    
    @rx.event
    def agregar_nota_consulta(self, consulta_id: str):
        """📝 Agregar nota a una consulta"""
        print(f"📝 Agregando nota a consulta: {consulta_id}")
        # TODO: Abrir modal de notas
    
    @rx.event
    def ver_recibo_consulta(self, consulta_id: str):
        """📄 Ver recibo de una consulta"""
        print(f"📄 Viendo recibo de consulta: {consulta_id}")
        # TODO: Navegación a módulo de pagos
    
    @rx.event
    def ver_historial_completo(self, consulta_id: str):
        """📋 Ver historial completo de una consulta"""
        print(f"📋 Viendo historial completo: {consulta_id}")
        # TODO: Modal con historial detallado

    # ==========================================
    # 🦷 ODONTOGRAMA V2.0 - MÉTODOS DE INTEGRACIÓN
    # ==========================================

    @rx.event
    async def cargar_odontograma_paciente(self, paciente_id: str):
        """🦷 Cargar odontograma interactivo del paciente actual"""
        if not paciente_id:
            print("⚠️ No se puede cargar odontograma sin ID de paciente")
            return

        try:
            print(f"🦷 Cargando odontograma para paciente: {paciente_id}")

            # Obtener estado odontología
            estado_odontologia = self.get_estado_odontologia()

            # Establecer paciente actual si no está establecido
            if not estado_odontologia.paciente_actual.id:
                # Buscar paciente en la lista cargada
                paciente = next(
                    (p for p in estado_odontologia.pacientes_asignados if p.id == paciente_id),
                    None
                )
                if paciente:
                    estado_odontologia.paciente_actual = paciente

            # Cargar odontograma con datos reales
            await estado_odontologia.cargar_odontograma_paciente_actual()

            print(f"✅ Odontograma cargado para paciente {paciente_id}")

        except Exception as e:
            print(f"❌ Error cargando odontograma: {str(e)}")

    @rx.event
    def set_active_intervention_tab(self, tab_name: str):
        """🔄 Establecer tab activo en página de intervención"""
        self.active_intervention_tab = tab_name
        print(f"🔄 Tab de intervención activo: {tab_name}")

    # ==========================================
    # 📜 ODONTOGRAMA V3.0 - HELPERS FASE 4 Y 5
    # ==========================================

    def abrir_modal_historial(self):
        """🗂️ FASE 4: Abrir modal de historial de odontograma"""
        odonto_state = self.get_state(EstadoOdontologia)
        return odonto_state.abrir_modal_historial()

    def cerrar_modal_historial(self):
        """❌ FASE 4: Cerrar modal de historial de odontograma"""
        odonto_state = self.get_state(EstadoOdontologia)
        odonto_state.cerrar_modal_historial()

    def cerrar_modal_validacion(self):
        """❌ FASE 5: Cerrar modal de validación médica"""
        odonto_state = self.get_state(EstadoOdontologia)
        odonto_state.cerrar_modal_validacion()

    async def forzar_guardado_con_warnings(self):
        """⚠️ FASE 5: Forzar guardado aceptando warnings"""
        odonto_state = self.get_state(EstadoOdontologia)
        # Cerrar modal de validación
        odonto_state.cerrar_modal_validacion()
        # Guardar cambios ignorando warnings
        await odonto_state.guardar_cambios_batch(forzar=True)

    # Computed vars para acceso directo a variables de validación
    # IMPORTANTE: No usar get_state() en computed vars (no puede ser async)
    # Con mixin=True, las variables están directamente disponibles en self
    # Ya no son necesarios estos computed vars porque están en el state directamente
    # Se acceden como: AppState.validacion_errores directamente desde componentes

    # ==========================================
    # 📝 VARIABLES PARA MODAL NUEVA CONSULTA FASE 1
    # ==========================================
    
    
    @rx.var
    def odontologos_list(self) -> List[PersonalModel]:
        """👨‍⚕️ Lista de odontólogos para modal consulta - DATOS REALES"""
        # Usar los datos reales del estado personal
        return self.odontologos_disponibles
    
    
    
    # ==========================================
    # 🔗 COMPUTED VARS PARA FASE 2 - FUNCIONALIDAD DINÁMICA
    # ==========================================
    
    @rx.var
    def consultas_por_doctor_dict(self) -> Dict[str, List[ConsultaModel]]:
        """📋 Consultas pendientes agrupadas por doctor - v4.1"""
        consultas_dict = {}
        for doctor in self.get_lista_odontologos_activos:
            consultas_dict[doctor.id] = [
                c for c in self.consultas_hoy 
                if c.primer_odontologo_id == doctor.id and c.estado in ["en_espera", "en_atencion"]
            ]
        return consultas_dict
    
    @rx.var
    def conteos_consultas_por_doctor(self) -> Dict[str, int]:
        """🔢 Conteos de consultas por doctor"""
        conteos = {}
        for doctor_id, consultas in self.consultas_por_doctor_dict.items():
            conteos[doctor_id] = len(consultas)
        return conteos

    @rx.var
    def get_urgentes_por_doctor(self) -> Dict[str, int]:
        """🚨 Contador de urgentes por odontólogo"""
        urgentes = {}
        for doctor_id, consultas in self.consultas_por_doctor_dict.items():
            urgentes_count = len([c for c in consultas if c.prioridad == "urgente"])
            urgentes[doctor_id] = urgentes_count
        return urgentes

    @rx.var
    def get_tiempo_promedio_espera(self) -> Dict[str, str]:
        """⏱️ Tiempo promedio de espera por odontólogo"""
        tiempos = {}
        for doctor in self.odontologos_disponibles:
            # TODO: Calcular tiempo real basado en consultas
            consultas_doctor = self.consultas_por_doctor_dict.get(doctor.id, [])
            if len(consultas_doctor) == 0:
                tiempos[doctor.id] = "0m"
            elif len(consultas_doctor) <= 2:
                tiempos[doctor.id] = "15m"
            elif len(consultas_doctor) <= 5:
                tiempos[doctor.id] = "30m"
            else:
                tiempos[doctor.id] = "45m+"
        return tiempos
    
    @rx.var
    def consultas_con_orden_por_doctor(self) -> Dict[str, List[ConsultaConOrdenModel]]:
        """📋 Consultas con número de orden real por doctor - MODELO TIPADO"""
        resultado = {}
        for doctor_id, consultas in self.consultas_por_doctor_dict.items():
            consultas_con_orden = []
            for index, consulta in enumerate(consultas, 1):
                consulta_con_orden = ConsultaConOrdenModel.from_consulta(
                    consulta=consulta,
                    orden=index,
                    tiempo_espera=self._calcular_tiempo_espera(index, consulta.estado),
                    es_siguiente=(index == 1 and consulta.estado == "en_espera")
                )
                consultas_con_orden.append(consulta_con_orden)
            resultado[doctor_id] = consultas_con_orden
        return resultado
    
    def _calcular_tiempo_espera(self, posicion: int, estado: str) -> str:
        """⏱️ Calcular tiempo de espera estimado"""
        if estado == "en_atencion":
            return "En atención"
        elif posicion == 1:
            return "0"
        else:
            # Estimar 30 minutos por consulta
            minutos_estimados = (posicion - 1) * 30
            if minutos_estimados < 60:
                return f"~{minutos_estimados} min"
            else:
                horas = minutos_estimados // 60
                minutos_restantes = minutos_estimados % 60
                if minutos_restantes == 0:
                    return f"~{horas}h"
                else:
                    return f"~{horas}h {minutos_restantes}min"
    
    @rx.var  
    def metricas_avanzadas_por_doctor(self) -> Dict[str, Dict[str, Any]]:
        """📊 Métricas avanzadas por doctor"""
        metricas = {}
        for doctor in self.odontologos_disponibles:
            doctor_id = doctor.id
            consultas_doctor = self.consultas_por_doctor_dict.get(doctor_id, [])
            
            # Calcular métricas
            en_espera = len([c for c in consultas_doctor if c.estado == "programada"])
            en_curso = len([c for c in consultas_doctor if c.estado == "en_curso"])
            
            # Tiempo promedio (estimado)
            tiempo_promedio = "30 min"  # TODO: Calcular desde datos reales
            
            metricas[doctor_id] = {
                "nombre_doctor": doctor.nombre_completo,
                "especialidad": doctor.especialidad,
                "en_espera": en_espera,
                "en_curso": en_curso,
                "tiempo_promedio": tiempo_promedio,
                "carga_trabajo": "Alta" if en_espera > 3 else "Media" if en_espera > 1 else "Baja",
                "disponible": en_curso == 0
            }
        return metricas
    
    @rx.var
    def consultas_con_orden_por_doctor_con_prioridad(self) -> Dict[str, List[ConsultaModel]]:
        """📊 CONSULTAS AGRUPADAS POR DOCTOR CON ORDEN DE PRIORIDAD - IMPLEMENTACIÓN DIRECTA"""
        consultas_por_doctor: Dict[str, List[ConsultaModel]] = {}
        
        # Definir orden de prioridades
        orden_prioridad = {"urgente": 0, "alta": 1, "normal": 2, "baja": 3}
        
        for doctor in self.get_lista_odontologos_activos:
            doctor_id = doctor.id
            consultas_doctor = []
            
            # Obtener consultas del doctor que están en espera o en atención
            for consulta in self.consultas_hoy:
                if (consulta.primer_odontologo_id == doctor_id and 
                    consulta.estado in ["en_espera", "en_atencion"]):
                    consultas_doctor.append(consulta)
            
            # Ordenar por prioridad y luego por orden de llegada
            if consultas_doctor:
                consultas_doctor = sorted(
                    consultas_doctor,
                    key=lambda c: (
                        orden_prioridad.get(c.prioridad or "normal", 2),
                        c.orden_cola_odontologo or c.orden_llegada_general or 999
                    )
                )
            
            consultas_por_doctor[doctor_id] = consultas_doctor
        
        return consultas_por_doctor
    
    # ==========================================
    # 🔧 MÉTODOS HELPER PARA CONSULTAS v4.1
    # ==========================================
    

    @rx.var
    def get_consultas_pendientes(self) -> List[ConsultaModel]:
        """⏳ Consultas pendientes (en espera)"""
        return [c for c in self.consultas_hoy if c.estado == "en_espera"]
    
    def get_consultas_pendientes_doctor(self, doctor_id: str) -> List[ConsultaModel]:
        """⏳ Consultas pendientes de un doctor específico - v4.1"""
        return [
            c for c in self.consultas_hoy 
            if c.primer_odontologo_id == doctor_id and c.estado in ["en_espera", "en_atencion"]
        ]
    
    
    
    @rx.var
    def get_opciones_pacientes(self) -> List[str]:
        """👥 Opciones de pacientes para selectores"""
        try:
            if not self.lista_pacientes:
                return []
            return [f"{p.numero_historia} - {p.nombre_completo}" for p in self.lista_pacientes[:20]]  # Limitar a 20
        except Exception:
            return []
    
    @rx.var
    def get_lista_odontologos_activos(self) -> List[PersonalModel]:
        """👨‍⚕️ Lista de odontólogos activos para colas"""
        try:
            # Verificar que la lista existe y no está vacía
            if not self.lista_personal:
                return []
            
            # Filtrar odontólogos activos con manejo seguro de atributos
            odontologos = []
            for p in self.lista_personal:
                try:
                    if (hasattr(p, 'rol_nombre') and p.rol_nombre == "odontologo" and 
                        hasattr(p, 'estado_laboral') and p.estado_laboral == "activo"):
                        odontologos.append(p)
                except Exception:
                    continue
            return odontologos
        except Exception:
            return []
    
    @rx.var
    def get_opciones_odontologos(self) -> List[str]:
        """👨‍⚕️ Opciones de odontólogos para selectores"""
        try:
            # Usar directamente odontologos_disponibles del estado personal
            odontologos = self.odontologos_disponibles
            if not odontologos:
                return []
            return [f"{p.id} - Dr. {p.nombre_completo} ({p.especialidad})" for p in odontologos]
        except Exception:
            return []
    
    @rx.var
    def get_opciones_pacientes_filtradas(self) -> List[str]:
        """👥 Opciones de pacientes filtradas para modal de consulta"""
        try:
            # Acceso directo via mixin (no necesita get_estado_consultas)
            if not estado_consultas:
                return self.get_opciones_pacientes  # Fallback a todas las opciones
            
            # Si hay término de búsqueda, usar pacientes filtrados
            if estado_consultas.termino_busqueda_pacientes_modal:
                if not estado_consultas.pacientes_filtrados_modal:
                    return []
                return [
                    f"{p.numero_historia} - {p.nombre_completo}" 
                    for p in estado_consultas.pacientes_filtrados_modal 
                    if hasattr(p, 'numero_historia') and hasattr(p, 'nombre_completo')
                ]
            else:
                # Si no hay búsqueda, mostrar todas las opciones
                return self.get_opciones_pacientes
                
        except Exception:
            return []
    
    @rx.var
    def termino_busqueda_pacientes_modal(self) -> str:
        """🔍 Término de búsqueda de pacientes en modal"""
        try:
            # Acceso directo via mixin (no necesita get_estado_consultas)
            return estado_consultas.termino_busqueda_pacientes_modal if estado_consultas else ""
        except Exception:
            return ""
    
    @rx.event
    def buscar_pacientes_modal(self, termino: str):
        """🔍 Delegado para búsqueda de pacientes en modal - DESHABILITADO TEMPORALMENTE"""
        # Método deshabilitado temporalmente para evitar errores de compilación
        # TODO: Restaurar funcionalidad cuando se resuelvan los problemas de estado
        print(f"🔧 Búsqueda deshabilitada temporalmente. Término: {termino}")
        return
    
    def get_consultas_por_odontologo(self, odontologo_id: str) -> List[ConsultaModel]:
        """📅 Obtener consultas de hoy por odontólogo específico"""
        try:
            # Acceso directo via mixin (no necesita get_estado_consultas)
            if not estado_consultas or not estado_consultas.consultas_hoy:
                return []
            
            # Filtrar consultas del odontólogo en estados relevantes
            consultas_odontologo = []
            for consulta in estado_consultas.consultas_hoy:
                if (hasattr(consulta, 'primer_odontologo_id') and 
                    consulta.primer_odontologo_id == odontologo_id and
                    consulta.estado in ['en_espera', 'en_atencion', 'entre_odontologos']):
                    consultas_odontologo.append(consulta)
            
            # Ordenar por orden de llegada
            consultas_odontologo.sort(key=lambda c: c.orden_llegada_general or 0)
            return consultas_odontologo
            
        except Exception as e:
            print(f"Error obteniendo consultas por odontólogo: {e}")
            return []
    
    def get_total_consultas_por_odontologo(self, odontologo_id: str) -> int:
        """📊 Total de consultas por odontólogo específico"""
        try:
            consultas = self.get_consultas_por_odontologo(odontologo_id)
            return len(consultas)
        except Exception:
            return 0
    
    @rx.var
    def get_total_consultas_hoy(self) -> int:
        """📊 Total de consultas de hoy"""
        try:
            # Acceso directo via mixin (no necesita get_estado_consultas)
            return len(estado_consultas.consultas_hoy) if estado_consultas else 0
        except Exception:
            return 0
    
    # ==========================================
    # 📊 COMPUTED VARS PARA PANEL DE PACIENTE
    # ==========================================
    
    @rx.var
    def total_visitas_paciente_actual(self) -> int:
        """📊 Total de visitas del paciente actual"""
        try:
            if not self.paciente_actual or not self.paciente_actual.numero_historia:
                return 0
            # Contar todas las consultas históricas del paciente
            return len([
                c for c in self.lista_consultas 
                if c.numero_historia == self.paciente_actual.numero_historia
            ])
        except Exception:
            return 0
    
    @rx.var 
    def ultima_visita_paciente_actual(self) -> str:
        """📅 Fecha de última visita formateada del paciente actual"""
        try:
            if not self.paciente_actual or not self.paciente_actual.numero_historia:
                return "Sin visitas"
            
            # Buscar la consulta más reciente del paciente
            consultas_paciente = [
                c for c in self.lista_consultas 
                if c.numero_historia == self.paciente_actual.numero_historia
                and c.estado == "completada"
            ]
            
            if not consultas_paciente:
                return "Sin visitas"
            
            # Ordenar por fecha descendente y tomar la primera
            consulta_reciente = max(consultas_paciente, key=lambda c: c.fecha_consulta or "")
            return consulta_reciente.fecha_display if hasattr(consulta_reciente, 'fecha_display') else "Fecha no disponible"
            
        except Exception:
            return "Sin visitas"
    
    @rx.var
    def consultas_pendientes_paciente(self) -> int:
        """📋 Número de consultas pendientes del paciente actual"""
        try:
            if not self.paciente_actual or not self.paciente_actual.numero_historia:
                return 0
            
            # Contar consultas en estados pendientes
            return len([
                c for c in self.consultas_hoy 
                if (c.numero_historia == self.paciente_actual.numero_historia and 
                    c.estado in ["en_espera", "en_atencion"])
            ])
        except Exception:
            return 0
    
    @rx.var
    def get_consultas_en_espera_hoy(self) -> int:
        """📊 Total de consultas en espera hoy"""
        try:
            # Acceso directo via mixin (no necesita get_estado_consultas)
            if not estado_consultas or not estado_consultas.consultas_hoy:
                return 0
            return len([c for c in estado_consultas.consultas_hoy if c.estado == 'en_espera'])
        except Exception:
            return 0
    
    @rx.var
    def get_consultas_en_atencion_hoy(self) -> int:
        """📊 Total de consultas en atención hoy"""
        try:
            # Acceso directo via mixin (no necesita get_estado_consultas)
            if not estado_consultas or not estado_consultas.consultas_hoy:
                return 0
            return len([c for c in estado_consultas.consultas_hoy if c.estado == 'en_atencion'])
        except Exception:
            return 0
    
    @rx.var
    def get_consultas_completadas_hoy(self) -> int:
        """📊 Total de consultas completadas hoy"""
        try:
            # Acceso directo via mixin (no necesita get_estado_consultas)
            if not estado_consultas or not estado_consultas.consultas_hoy:
                return 0
            return len([c for c in estado_consultas.consultas_hoy if c.estado == 'completada'])
        except Exception:
            return 0
    
    
    
    # ==========================================
    # 🔗 NAVEGACIÓN ENTRE MÓDULOS
    # ==========================================
    
    @rx.event
    async def navegar_a_odontologia_consulta(self, consulta_id: str):
        """
        🦷 NAVEGAR A MÓDULO DE ODONTOLOGÍA CON CONSULTA ESPECÍFICA

        Delega al método especializado seleccionar_paciente_consulta() que:
        1. Busca y carga paciente + consulta
        2. Cambia estado de consulta a "en_atencion"
        3. Carga odontograma última versión
        4. Carga intervenciones previas
        5. Navega a página de intervención

        Args:
            consulta_id: ID de la consulta a atender
        """
        try:
            logger.info(f"🦷 Iniciando navegación a odontología con consulta: {consulta_id}")

            if not consulta_id:
                self.mostrar_toast("ID de consulta requerido", "error")
                return

            # Buscar la consulta en ambas listas
            consulta_encontrada = None

            # Buscar en lista_consultas (EstadoConsultas)
            for consulta in self.lista_consultas:
                if consulta.id == consulta_id:
                    consulta_encontrada = consulta
                    break

            # Buscar en consultas_asignadas (EstadoOdontologia)
            if not consulta_encontrada:
                for consulta in self.consultas_asignadas:
                    if consulta.id == consulta_id:
                        consulta_encontrada = consulta
                        break

            if not consulta_encontrada:
                logger.warning(f"❌ Consulta no encontrada: {consulta_id}")
                self.mostrar_toast("Consulta no encontrada", "error")
                return

            # Obtener paciente_id de la consulta
            paciente_id = consulta_encontrada.paciente_id

            if not paciente_id:
                logger.error(f"❌ Consulta sin paciente_id: {consulta_id}")
                self.mostrar_toast("Consulta sin paciente asociado", "error")
                return

            # Usar el método especializado que maneja todo el flujo
            await self.seleccionar_paciente_consulta(paciente_id, consulta_id)

            logger.info(f"✅ Navegación completada exitosamente")

        except Exception as e:
            logger.error(f"❌ Error navegando a odontología: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostrar_toast(f"Error navegando a odontología: {str(e)}", "error")
    
    @rx.event
    def navegar_a_pagos_consulta(self, consulta_id: str):
        """💳 Navegar al módulo de pagos con consulta específica"""
        try:
            if not consulta_id:
                self.mostrar_toast("ID de consulta requerido", "error")
                return
            
            # Obtener información de la consulta
            # Acceso directo via mixin (no necesita get_estado_consultas)
            if True:  # Siempre disponible via mixin
                # Buscar la consulta en la lista
                consulta_encontrada = None
                for consulta in self.lista_consultas:
                    if consulta.id == consulta_id:
                        consulta_encontrada = consulta
                        break
                
                if consulta_encontrada:
                    # Establecer contexto para pagos
                    self.establecer_contexto_pagos(consulta_encontrada)
                    
                    # Cambiar página
                    self.current_page = "pagos"
                    self.titulo_pagina = "Gestión de Pagos"
                    self.subtitulo_pagina = f"Consulta: {consulta_encontrada.numero_consulta}"
                    
                    self.mostrar_toast("Navegando a módulo de pagos", "info")
                else:
                    self.mostrar_toast("Consulta no encontrada", "error")
            else:
                self.mostrar_toast("Error accediendo a datos de consulta", "error")
                
        except Exception as e:
            self.mostrar_toast(f"Error navegando a pagos: {str(e)}", "error")
    
    async def establecer_contexto_odontologia(self, consulta: ConsultaModel):
        """🦷 Establecer contexto para módulo de odontología"""
        try:
            print(f"🔍 DEBUG - Estableciendo contexto para consulta ID: {consulta.id}")
            print(f"🔍 DEBUG - Paciente ID en consulta: {consulta.paciente_id}")
            print(f"🔍 DEBUG - Total pacientes en lista: {len(self.lista_pacientes)}")
            
            # Establecer contexto usando acceso directo via mixins
            # EstadoOdontologia está incluido como mixin, usar nombres correctos
            self.consulta_actual = consulta
            
            # Debug: mostrar algunos pacientes disponibles
            if len(self.lista_pacientes) > 0:
                print(f"🔍 DEBUG - Primeros 3 pacientes:")
                for i, p in enumerate(self.lista_pacientes[:3]):
                    print(f"   [{i}] ID: {p.id}, HC: {p.numero_historia}, Nombre: {p.nombre_completo}")
            
            # Buscar el paciente completo por ID (no por numero_historia)
            paciente_encontrado = None
            for i, paciente in enumerate(self.lista_pacientes):
                print(f"🔍 DEBUG - Comparando paciente ID '{paciente.id}' con consulta paciente_id '{consulta.paciente_id}'")
                if paciente.id == consulta.paciente_id:
                    paciente_encontrado = paciente
                    print(f"✅ MATCH encontrado en índice {i}")
                    break
            
            if paciente_encontrado:
                self.paciente_actual = paciente_encontrado
                print(f"✅ Contexto odontología establecido - Consulta: {consulta.id}")
                print(f"✅ Paciente actual: {paciente_encontrado.nombre_completo} (ID: {paciente_encontrado.id}, HC: {paciente_encontrado.numero_historia})")
                print(f"✅ Edad: {paciente_encontrado.edad}, Genero: {paciente_encontrado.genero}")
                print(f"✅ Alergias: {len(paciente_encontrado.alergias)} items")
            else:
                print(f"❌ PACIENTE NO ENCONTRADO para consulta paciente_id: {consulta.paciente_id}")
                print(f"❌ Verificar si los IDs coinciden exactamente")
                
                # Intentar cargar el paciente directamente desde la base de datos
                print(f"🔍 Intentando cargar paciente directamente desde BD usando servicio...")
                try:
                    from dental_system.services.pacientes_service import pacientes_service
                    
                    # Establecer contexto de usuario para permisos
                    pacientes_service.set_user_context(self.id_usuario, self.perfil_usuario)
                    
                    # Usar método sincrónico del servicio
                    paciente_desde_bd = pacientes_service.get_patient_by_id_sync(consulta.paciente_id)
                    if paciente_desde_bd:
                        self.paciente_actual = paciente_desde_bd
                        print(f"✅ PACIENTE CARGADO DESDE BD VIA SERVICIO: {paciente_desde_bd.nombre_completo}")
                        # También agregar a la lista para futuras búsquedas
                        self.lista_pacientes.append(paciente_desde_bd)
                    else:
                        print(f"❌ PACIENTE NO EXISTE EN BD con ID: {consulta.paciente_id}")
                        
                        # Como último recurso, búsqueda por nombre en lista actual
                        print(f"🔍 Última opción: búsqueda backup por nombre del paciente...")
                        if hasattr(consulta, 'paciente_nombre') and consulta.paciente_nombre:
                            for i, paciente in enumerate(self.lista_pacientes):
                                if consulta.paciente_nombre.strip().lower() in paciente.nombre_completo.strip().lower():
                                    print(f"🔍 POSIBLE MATCH por nombre: '{paciente.nombre_completo}' vs '{consulta.paciente_nombre}'")
                                    self.paciente_actual = paciente
                                    print(f"⚠️ USANDO MATCH POR NOMBRE como último recurso")
                                    break
                except Exception as e:
                    print(f"❌ Error cargando paciente desde BD: {e}")
                    # Backup por nombre si falla la carga desde BD
                    if hasattr(consulta, 'paciente_nombre') and consulta.paciente_nombre:
                        for i, paciente in enumerate(self.lista_pacientes):
                            if consulta.paciente_nombre.strip().lower() in paciente.nombre_completo.strip().lower():
                                print(f"🔍 FALLBACK - MATCH por nombre: '{paciente.nombre_completo}' vs '{consulta.paciente_nombre}'")
                                self.paciente_actual = paciente
                                print(f"⚠️ USANDO FALLBACK POR NOMBRE")
                                break

            # ✅ CAMBIO CRÍTICO: Cambiar estado de consulta de "en_espera" a "en_atencion"
            if consulta.estado in ["en_espera", "programada"]:
                try:
                    print(f"🔄 Cambiando estado de consulta: {consulta.estado} → en_atencion")
                    # Usar el método existente para cambiar estado (sin segundo parámetro)
                    await self.iniciar_atencion_consulta(consulta.id)
                    print(f"✅ Estado cambiado exitosamente: {consulta.estado} → en_atencion")
                except Exception as estado_error:
                    print(f"❌ Error cambiando estado de consulta: {estado_error}")
                    # Continuar aunque falle el cambio de estado - el contexto ya está establecido
            else:
                print(f"ℹ️ Consulta ya en estado: {consulta.estado}, no se cambia estado")

        except Exception as e:
            print(f"❌ Error estableciendo contexto odontología: {e}")
            import traceback
            traceback.print_exc()
    
    def establecer_contexto_pagos(self, consulta: ConsultaModel):
        """💳 Establecer contexto para módulo de pagos"""
        try:
            # Aquí se establecería el contexto necesario para pagos
            # Por ejemplo, consulta para facturar, paciente, etc.
            # Acceso directo via mixin EstadoPagos (si existiera)
            if estado_pagos:
                # Establecer consulta para facturar
                estado_pagos.consulta_para_facturar = consulta
                estado_pagos.paciente_seleccionado = consulta.paciente_id
                
        except Exception as e:
            print(f"Error estableciendo contexto pagos: {e}")
    
    def get_estado_odontologia(self):
        """🦷 Obtener estado de odontología si existe"""
        try:
            return getattr(self, '_estado_odontologia', None)
        except Exception:
            return None
    
    def get_estado_pagos(self):
        """💳 Obtener estado de pagos (disponible como mixin)"""
        return self  # EstadoPagos está disponible como mixin

    # ==========================================
    # 💰 HELPERS SISTEMA DUAL USD/BS
    # ==========================================

    @rx.event
    async def crear_pago_coordinado(self, form_data: Dict[str, Any]):
        """💰 COORDINADOR: Crear pago con sistema dual"""
        try:
            # Usar el método del substate EstadoPagos
            resultado = await self.crear_pago_dual()

            if resultado:
                # Actualizar estadísticas globales
                await self.actualizar_estadisticas_dashboard()
                logger.info("✅ Pago dual creado y estadísticas actualizadas")
                return True

            return False

        except Exception as e:
            logger.error(f"❌ Error coordinando pago dual: {str(e)}")
            return False

    @rx.event
    async def actualizar_tasa_coordinada(self, nueva_tasa: float):
        """💱 COORDINADOR: Actualizar tasa de cambio"""
        try:
            # Usar el método del substate EstadoPagos
            resultado = await self.actualizar_tasa_del_dia(nueva_tasa)

            if resultado:
                # Notificar cambio de tasa globalmente
                await self.mostrar_toast(f"Tasa actualizada: {nueva_tasa} BS/USD", "success")
                logger.info(f"✅ Tasa coordinada actualizada: {nueva_tasa}")
                return True

            return False

        except Exception as e:
            logger.error(f"❌ Error coordinando tasa: {str(e)}")
            return False

    # ==========================================
    # 💰 COMPUTED VARS COORDINADAS PARA PAGOS
    # ==========================================

    @rx.var(cache=True)
    def estadisticas_pagos_dashboard(self) -> Dict[str, Any]:
        """📊 Estadísticas de pagos para dashboard principal"""
        try:
            # Obtener estadísticas duales
            dual_stats = self.total_recaudado_dual_hoy
            pendientes_stats = self.pendientes_dual_totales

            return {
                "recaudacion_usd_hoy": dual_stats.get("usd", 0.0),
                "recaudacion_bs_hoy": dual_stats.get("bs", 0.0),
                "tasa_promedio_dia": dual_stats.get("tasa_promedio", self.tasa_del_dia),
                "pendiente_usd": pendientes_stats.get("usd", 0.0),
                "pendiente_bs": pendientes_stats.get("bs", 0.0),
                "total_facturas_pendientes": pendientes_stats.get("total_facturas", 0),
                "tasa_actual": self.tasa_del_dia,
                "vista_dual_activa": self.vista_dual_activa,
                "moneda_preferida": self.preferencia_moneda_del_dia
            }
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas pagos dashboard: {str(e)}")
            return {
                "recaudacion_usd_hoy": 0.0,
                "recaudacion_bs_hoy": 0.0,
                "tasa_promedio_dia": 36.50,
                "pendiente_usd": 0.0,
                "pendiente_bs": 0.0,
                "total_facturas_pendientes": 0,
                "tasa_actual": 36.50,
                "vista_dual_activa": True,
                "moneda_preferida": "USD"
            }

    @rx.var(cache=True)
    def resumen_pagos_del_dia(self) -> str:
        """💰 Resumen textual de pagos del día"""
        try:
            stats = self.estadisticas_pagos_dashboard
            usd = stats["recaudacion_usd_hoy"]
            bs = stats["recaudacion_bs_hoy"]
            pendientes = stats["total_facturas_pendientes"]

            if usd > 0 and bs > 0:
                return f"Recaudado: ${usd:.2f} USD + {bs:,.2f} BS | Pendientes: {pendientes}"
            elif usd > 0:
                return f"Recaudado: ${usd:.2f} USD | Pendientes: {pendientes}"
            elif bs > 0:
                return f"Recaudado: {bs:,.2f} BS | Pendientes: {pendientes}"
            else:
                return f"Sin recaudación hoy | Pendientes: {pendientes}"

        except Exception:
            return "Error calculando resumen de pagos"
    
