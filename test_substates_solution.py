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

# Clase auxiliar para estadísticas
class SimpleStatValue:
    def __init__(self, value: int = 0):
        self.value = value
    
    def to_string(self) -> str:
        return str(self.value)
    
    def __int__(self) -> int:
        return self.value
    
    def __gt__(self, other) -> bool:
        if isinstance(other, SimpleStatValue):
            return self.value > other.value
        return self.value > other
    
    def __lt__(self, other) -> bool:
        if isinstance(other, SimpleStatValue):
            return self.value < other.value
        return self.value < other
    
    def __eq__(self, other) -> bool:
        if isinstance(other, SimpleStatValue):
            return self.value == other.value
        return self.value == other

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
    CategoriaServicioModel, ConceptoPagoModel,
    
    # Modelos de formularios  
    PacienteFormModel, ConsultaFormModel, PersonalFormModel,
    ServicioFormModel, PagoFormModel, IntervencionFormModel
)

logger = logging.getLogger(__name__)

class AppState(EstadoAuth, EstadoPersonal,rx.State):
    """
    🎯 APPSTATE DEFINITIVO - ARQUITECTURA FINAL COMPLETA
    
    CARACTERÍSTICAS:
    ✅ Event handlers async con get_state() (patrón oficial Reflex)
    ✅ Computed vars sin async para UI (performance)
    ✅ Substates existentes preservados (modularidad)
    ✅ Una sola herencia rx.State (sin MRO conflicts)
    ✅ TODOS los módulos con modelos tipados
    ✅ Variables y funciones en español
    ✅ Escalable y mantenible
    
    PATRÓN:
    UI → Computed vars (sync) → Variables directas
    UI → Event handlers (async) → get_state() → Coordinación
    """
    
    # ==========================================
    # 🔧 MÉTODOS HELPER PARA ACCESO RÁPIDO (PRIVADOS)
    # ==========================================
    
    # def _auth(self) -> EstadoAuth:
    #     """🔐 Acceso rápido a autenticación (solo para computed vars)"""
    #     return self.get_state(EstadoAuth)
    
    # def _ui(self) -> EstadoUI:
    #     """🎨 Acceso rápido a UI (solo para computed vars)"""
    #     return self.get_state(EstadoUI)
    
    # def _pacientes(self) -> EstadoPacientes:
    #     """👥 Acceso rápido a pacientes (solo para computed vars)"""
    #     return self.get_state(EstadoPacientes)
    
    # def _consultas(self) -> EstadoConsultas:
    #     """📅 Acceso rápido a consultas (solo para computed vars)"""
    #     return self.get_state(EstadoConsultas)
    
    # def _personal(self) -> EstadoPersonal:
    #     """👨‍⚕️ Acceso rápido a personal (solo para computed vars)"""
    #     return self.get_state(EstadoPersonal)
    
    # def _odontologia(self) -> EstadoOdontologia:
    #     """🦷 Acceso rápido a odontología (solo para computed vars)"""
    #     return self.get_state(EstadoOdontologia)
    
    # def _servicios(self) -> EstadoServicios:
    #     """🏥 Acceso rápido a servicios (solo para computed vars)"""
    #     return self.get_state(EstadoServicios)
    
    # # ==========================================
    # # 🔐 COMPUTED VARS: AUTENTICACIÓN (SIN ASYNC)
    # # ==========================================
    

    
    # @rx.var(cache=True)
    # def id_usuario(self) -> str:
    #     """👤 ID del usuario - ACCESO DIRECTO UI"""
    #     return self._auth().id_usuario
    
    # @rx.var(cache=True)
    # def rol_usuario(self) -> str:
    #     """👔 Rol del usuario - ACCESO DIRECTO UI"""
    #     return self._auth().rol_usuario
    
    # @rx.var(cache=True)
    # def email_usuario(self) -> str:
    #     """📧 Email del usuario - ACCESO DIRECTO UI"""
    #     return self._auth().email_usuario
    
    # @rx.var(cache=True)
    # def id_personal(self) -> str:
    #     """🆔 ID personal - ACCESO DIRECTO UI"""
    #     return self._auth().id_personal
    
    # @rx.var(cache=True)
    # def nombre_usuario_display(self) -> str:
    #     """👤 Nombre para mostrar - ACCESO DIRECTO UI"""
    #     return self._auth().nombre_usuario_display
    
    # @rx.var(cache=True)
    # def rol_usuario_display(self) -> str:
    #     """👔 Rol formateado - ACCESO DIRECTO UI"""
    #     return self._auth().rol_usuario_display
    
    # @rx.var(cache=True)
    # def sesion_valida(self) -> bool:
    #     """✅ Sesión válida - ACCESO DIRECTO UI"""
    #     return self._auth().sesion_valida
    
    # @rx.var(cache=True)
    # def error_login(self) -> str:
    #     """❌ Error de login - ACCESO DIRECTO UI"""
    #     return self._auth().error_login
    
    # # ==========================================
    # # 🔗 ALIASES PARA COMPATIBILIDAD BACKWARD
    # # ==========================================
    
    # @rx.var(cache=True)
    # def is_authenticated(self) -> bool:
    #     """✅ Alias para esta_autenticado - COMPATIBILIDAD"""
    #     return self._auth().esta_autenticado
    
    # @rx.var(cache=True)
    # def user_role(self) -> str:
    #     """👔 Alias para rol_usuario - COMPATIBILIDAD"""
    #     return self._auth().rol_usuario
    
    # @rx.var(cache=True)
    # def is_loading_auth(self) -> bool:
    #     """⏳ Alias para esta_cargando_auth - COMPATIBILIDAD"""
    #     return self._auth().esta_cargando_auth
    
    # @rx.var(cache=True)
    # def login_error(self) -> str:
    #     """❌ Alias para error_login - COMPATIBILIDAD"""
    #     return self._auth().error_login
    
    # @rx.var(cache=True)
    # def dashboard_stats(self) -> Dict[str, Any]:
    #     """📊 Estadísticas del dashboard - TEMPORAL"""
    #     # TODO: Implementar estadísticas reales desde servicios
    #     return {
    #         "total_pacientes": SimpleStatValue(0),
    #         "total_consultas": SimpleStatValue(0),
    #         "consultas_hoy": SimpleStatValue(0),
    #         "personal_activo": SimpleStatValue(0),
    #         "total_servicios": SimpleStatValue(0)
    #     }
    
    # @rx.var(cache=True)
    # def area_toggle(self) -> bool:
    #     """📈 Toggle para área de gráficas - TEMPORAL"""
    #     return True
    
    # @rx.var(cache=True)
    # def personal_stats(self) -> Dict[str, Any]:
    #     """📊 Estadísticas completas de personal - DESDE SERVICIO"""
    #     return self._personal().estadisticas_personal
    
    # @rx.var(cache=True)
    # def success_message(self) -> str:
    #     """✅ Mensaje de éxito - ALIAS PARA COMPATIBILIDAD"""
    #     return self._ui().mensaje_modal_confirmacion
    
    # @rx.var(cache=True)
    # def error_message(self) -> str:
    #     """❌ Mensaje de error - ALIAS PARA COMPATIBILIDAD"""
    #     return self._ui().mensaje_modal_alerta
    
    # @rx.var(cache=True)  
    # def staff_form_step(self) -> int:
    #     """📝 Paso actual del formulario de personal - ALIAS PARA COMPATIBILIDAD"""
    #     return self._ui().paso_formulario_personal
    
    # @rx.var(cache=True)
    # def esta_cargando_auth(self) -> bool:
    #     """⏳ Cargando auth - ACCESO DIRECTO UI"""
    #     return self._auth().esta_cargando_auth
    
    # # ✅ PERMISOS POR MÓDULO
    # @rx.var(cache=True)
    # def tiene_permiso_pacientes(self) -> bool:
    #     """👥 Puede acceder a pacientes - ACCESO DIRECTO UI"""
    #     return self._auth().tiene_permiso_pacientes
    
    # @rx.var(cache=True)
    # def tiene_permiso_consultas(self) -> bool:
    #     """📅 Puede acceder a consultas - ACCESO DIRECTO UI"""
    #     return self._auth().tiene_permiso_consultas
    
    # @rx.var(cache=True)
    # def tiene_permiso_personal(self) -> bool:
    #     """👨‍⚕️ Puede acceder a personal - ACCESO DIRECTO UI"""
    #     return self._auth().tiene_permiso_personal
    
    # @rx.var(cache=True)
    # def tiene_permiso_servicios(self) -> bool:
    #     """🏥 Puede acceder a servicios - ACCESO DIRECTO UI"""
    #     return self._auth().tiene_permiso_servicios
    
    # @rx.var(cache=True)
    # def tiene_permiso_pagos(self) -> bool:
    #     """💳 Puede acceder a pagos - ACCESO DIRECTO UI"""
    #     return self._auth().tiene_permiso_pagos
    
    # @rx.var(cache=True)
    # def tiene_permiso_odontologia(self) -> bool:
    #     """🦷 Puede acceder a odontología - ACCESO DIRECTO UI"""
    #     return self._auth().tiene_permiso_odontologia
    
    # @rx.var(cache=True)
    # def es_gerente(self) -> bool:
    #     """👑 Es gerente - ACCESO DIRECTO UI"""
    #     return self._auth().es_gerente
    
    # @rx.var(cache=True)
    # def es_administrador(self) -> bool:
    #     """👤 Es administrador - ACCESO DIRECTO UI"""
    #     return self._auth().es_administrador
    
    # @rx.var(cache=True)
    # def es_odontologo(self) -> bool:
    #     """🦷 Es odontólogo - ACCESO DIRECTO UI"""
    #     return self._auth().es_odontologo
    
    # @rx.var(cache=True)
    # def es_asistente(self) -> bool:
    #     """👩‍⚕️ Es asistente - ACCESO DIRECTO UI"""
    #     return self._auth().es_asistente
    
    # # ==========================================
    # # 👥 COMPUTED VARS: PACIENTES (SIN ASYNC)
    # # ==========================================
    
    # @rx.var(cache=True)
    # def lista_pacientes(self) -> List[PacienteModel]:
    #     """📋 Lista completa de pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().lista_pacientes
    
    # @rx.var(cache=True)
    # def pacientes_filtrados(self) -> List[PacienteModel]:
    #     """🔍 Pacientes filtrados - ACCESO DIRECTO UI"""
    #     return self._pacientes().pacientes_filtrados_display
    
    # @rx.var(cache=True)
    # def total_pacientes(self) -> int:
    #     """📊 Total de pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().total_pacientes
    
    # @rx.var(cache=True)
    # def total_pacientes_activos(self) -> int:
    #     """👥 Pacientes activos - ACCESO DIRECTO UI"""
    #     return self._pacientes().total_pacientes_activos
    
    # @rx.var(cache=True)
    # def pacientes_registrados_hoy(self) -> int:
    #     """📅 Pacientes registrados hoy - ACCESO DIRECTO UI"""
    #     return self._pacientes().pacientes_registrados_hoy
    
    # @rx.var(cache=True)
    # def paciente_seleccionado(self) -> Optional[PacienteModel]:
    #     """🎯 Paciente seleccionado - ACCESO DIRECTO UI"""
    #     return self._pacientes().paciente_seleccionado if self._pacientes().paciente_seleccionado_valido else None
    
    # @rx.var(cache=True)
    # def termino_busqueda_pacientes(self) -> str:
    #     """🔍 Término de búsqueda pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().termino_busqueda_pacientes
    
    # @rx.var(cache=True)
    # def cargando_lista_pacientes(self) -> bool:
    #     """⏳ Cargando pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().cargando_lista_pacientes
    
    # @rx.var(cache=True)
    # def errores_validacion_paciente(self) -> Dict[str, str]:
    #     """❌ Errores validación pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().errores_validacion_paciente
    
    # @rx.var(cache=True)
    # def filtro_genero_pacientes(self) -> str:
    #     """⚧ Filtro género pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().filtro_genero
    
    # @rx.var(cache=True)
    # def filtro_estado_pacientes(self) -> str:
    #     """🔄 Filtro estado pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().filtro_estado
    
    # @rx.var(cache=True)
    # def mostrar_solo_activos_pacientes(self) -> bool:
    #     """✅ Mostrar solo activos - ACCESO DIRECTO UI"""
    #     return self._pacientes().mostrar_solo_activos_pacientes
    
    # @rx.var(cache=True)
    # def formulario_paciente_data(self) -> PacienteFormModel:
    #     """📝 Datos formulario paciente - ACCESO DIRECTO UI"""
    #     return self._pacientes().formulario_paciente_data
    
    # @rx.var(cache=True)
    # def paciente_para_eliminar(self) -> Optional[PacienteModel]:
    #     """🗑️ Paciente a eliminar - ACCESO DIRECTO UI"""
    #     return self._pacientes().paciente_para_eliminar
    
    # @rx.var(cache=True)
    # def estadisticas_pacientes(self) -> PacientesStatsModel:
    #     """📊 Estadísticas pacientes - ACCESO DIRECTO UI"""
    #     return self._pacientes().estadisticas_pacientes
    
    # # ==========================================
    # # 👨‍⚕️ COMPUTED VARS: PERSONAL (SIN ASYNC)
    # # ==========================================
    
    # @rx.var(cache=True)
    # def lista_personal(self) -> List[PersonalModel]:
    #     """📋 Lista completa de personal - ACCESO DIRECTO UI"""
    #     return self._personal().lista_personal
    
    # @rx.var(cache=True)
    # def personal_filtrado(self) -> List[PersonalModel]:
    #     """🔍 Personal filtrado - ACCESO DIRECTO UI"""
    #     return self._personal().lista_personal  # Usar lista principal por ahora
    
    # @rx.var(cache=True)
    # def total_personal(self) -> int:
    #     """📊 Total de personal - ACCESO DIRECTO UI"""
    #     return self._personal().total_personal
    
    # @rx.var(cache=True)
    # def total_personal_activo(self) -> int:
    #     """👨‍⚕️ Personal activo - ACCESO DIRECTO UI"""
    #     return self._personal().total_personal_activo
    
    # @rx.var(cache=True)
    # def personal_seleccionado(self) -> Optional[PersonalModel]:
    #     """🎯 Personal seleccionado - ACCESO DIRECTO UI"""
    #     return self._personal().empleado_seleccionado if hasattr(self._personal().empleado_seleccionado, 'id') and self._personal().empleado_seleccionado.id else None
    
    # @rx.var(cache=True)
    # def termino_busqueda_personal(self) -> str:
    #     """🔍 Término búsqueda personal - ACCESO DIRECTO UI"""
    #     return self._personal().termino_busqueda_personal
    
    # @rx.var(cache=True)
    # def cargando_lista_personal(self) -> bool:
    #     """⏳ Cargando personal - ACCESO DIRECTO UI"""
    #     return self._personal().cargando_lista_personal
    
    # @rx.var(cache=True)
    # def errores_validacion_personal(self) -> Dict[str, str]:
    #     """❌ Errores validación personal - ACCESO DIRECTO UI"""
    #     return self._personal().errores_validacion_empleado
    
    # @rx.var(cache=True)
    # def filtro_rol_personal(self) -> str:
    #     """👔 Filtro rol personal - ACCESO DIRECTO UI"""
    #     return self._personal().filtro_rol
    
    # @rx.var(cache=True)
    # def filtro_especialidad_personal(self) -> str:
    #     """🦷 Filtro especialidad personal - ACCESO DIRECTO UI"""
    #     return self._personal().filtro_especialidad
    
    # @rx.var(cache=True)
    # def mostrar_solo_activos_personal(self) -> bool:
    #     """✅ Mostrar solo activos personal - ACCESO DIRECTO UI"""
    #     return self._personal().mostrar_solo_activos_personal
    
    # @rx.var(cache=True)
    # def formulario_personal_data(self) -> PersonalFormModel:
    #     """📝 Datos formulario personal - ACCESO DIRECTO UI"""
    #     return self._personal().formulario_empleado or PersonalFormModel()
    
    # @rx.var(cache=True)
    # def personal_para_eliminar(self) -> Optional[PersonalModel]:
    #     """🗑️ Personal a eliminar - ACCESO DIRECTO UI"""
    #     return self._personal().empleado_seleccionado if hasattr(self._personal(), 'empleado_para_eliminar') else self._personal().empleado_seleccionado
    
    # @rx.var(cache=True)
    # def lista_odontologos_disponibles(self) -> List[PersonalModel]:
    #     """🦷 Odontólogos disponibles - ACCESO DIRECTO UI"""
    #     return self._personal().lista_odontologos_disponibles
    
    # @rx.var(cache=True)
    # def estadisticas_personal(self) -> PersonalStatsModel:
    #     """📊 Estadísticas personal - ACCESO DIRECTO UI"""
    #     return self._personal().estadisticas_personal
    
    # # ==========================================
    # # 📅 COMPUTED VARS: CONSULTAS (SIN ASYNC)
    # # ==========================================
    
    # @rx.var(cache=True)
    # def lista_consultas(self) -> List[ConsultaModel]:
    #     """📋 Lista completa de consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().lista_consultas
    
    # @rx.var(cache=True)
    # def consultas_filtradas(self) -> List[ConsultaModel]:
    #     """🔍 Consultas filtradas - ACCESO DIRECTO UI"""
    #     return self._consultas().consultas_filtradas_display
    
    # @rx.var(cache=True)
    # def total_consultas(self) -> int:
    #     """📊 Total de consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().total_consultas
    
    # @rx.var(cache=True)
    # def consultas_hoy(self) -> List[ConsultaModel]:
    #     """📅 Consultas de hoy - ACCESO DIRECTO UI"""
    #     return self._consultas().consultas_hoy
    
    # @rx.var(cache=True)
    # def consultas_pendientes(self) -> List[ConsultaModel]:
    #     """⏳ Consultas pendientes - ACCESO DIRECTO UI"""
    #     return self._consultas().consultas_pendientes
    
    # @rx.var(cache=True)
    # def consultas_en_progreso(self) -> List[ConsultaModel]:
    #     """🔄 Consultas en progreso - ACCESO DIRECTO UI"""
    #     return self._consultas().consultas_en_progreso
    
    # @rx.var(cache=True)
    # def consultas_completadas_hoy(self) -> List[ConsultaModel]:
    #     """✅ Consultas completadas hoy - ACCESO DIRECTO UI"""
    #     return self._consultas().consultas_completadas_hoy
    
    # @rx.var(cache=True)
    # def consulta_seleccionada(self) -> Optional[ConsultaModel]:
    #     """🎯 Consulta seleccionada - ACCESO DIRECTO UI"""
    #     return self._consultas().consulta_seleccionada if hasattr(self._consultas().consulta_seleccionada, 'id') and self._consultas().consulta_seleccionada.id else None
    
    # @rx.var(cache=True)
    # def termino_busqueda_consultas(self) -> str:
    #     """🔍 Término búsqueda consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().termino_busqueda_consultas
    
    # @rx.var(cache=True)
    # def cargando_lista_consultas(self) -> bool:
    #     """⏳ Cargando consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().cargando_lista_consultas
    
    # @rx.var(cache=True)
    # def errores_validacion_consulta(self) -> Dict[str, str]:
    #     """❌ Errores validación consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().errores_validacion_consulta
    
    # @rx.var(cache=True)
    # def filtro_estado_consultas(self) -> str:
    #     """🔄 Filtro estado consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().filtro_estado_consultas
    
    # @rx.var(cache=True)
    # def filtro_odontologo_consultas(self) -> str:
    #     """🦷 Filtro odontólogo consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().filtro_odontologo_consultas
    
    # @rx.var(cache=True)
    # def filtro_fecha_consultas(self) -> str:
    #     """📅 Filtro fecha consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().filtro_fecha_consultas
    
    # @rx.var(cache=True)
    # def formulario_consulta_data(self) -> ConsultaFormModel:
    #     """📝 Datos formulario consulta - ACCESO DIRECTO UI"""
    #     return self._consultas().formulario_consulta_data
    
    # @rx.var(cache=True)
    # def consulta_para_eliminar(self) -> Optional[ConsultaModel]:
    #     """🗑️ Consulta a eliminar - ACCESO DIRECTO UI"""
    #     return self._consultas().consulta_para_eliminar
    
    # @rx.var(cache=True)
    # def lista_turnos_hoy(self) -> List[TurnoModel]:
    #     """🔄 Lista de turnos hoy - ACCESO DIRECTO UI"""
    #     return self._consultas().lista_turnos_hoy
    
    # @rx.var(cache=True)
    # def proximo_numero_turno(self) -> int:
    #     """🔢 Próximo número de turno - ACCESO DIRECTO UI"""
    #     return self._consultas().proximo_numero_turno
    
    # @rx.var(cache=True)
    # def estadisticas_consultas(self) -> ConsultasStatsModel:
    #     """📊 Estadísticas consultas - ACCESO DIRECTO UI"""
    #     return self._consultas().estadisticas_consultas
    
    # # ==========================================
    # # 🏥 COMPUTED VARS: SERVICIOS (SIN ASYNC)
    # # ==========================================
    
    # @rx.var(cache=True)
    # def lista_servicios(self) -> List[ServicioModel]:
    #     """📋 Lista completa de servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().lista_servicios
    
    # @rx.var(cache=True)
    # def servicios_filtrados(self) -> List[ServicioModel]:
    #     """🔍 Servicios filtrados - ACCESO DIRECTO UI"""
    #     return self._servicios().servicios_filtrados_display
    
    # @rx.var(cache=True)
    # def total_servicios(self) -> int:
    #     """📊 Total de servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().total_servicios
    
    # @rx.var(cache=True)
    # def servicios_activos(self) -> List[ServicioModel]:
    #     """✅ Servicios activos - ACCESO DIRECTO UI"""
    #     return self._servicios().servicios_activos
    
    # @rx.var(cache=True)
    # def servicio_seleccionado(self) -> Optional[ServicioModel]:
    #     """🎯 Servicio seleccionado - ACCESO DIRECTO UI"""
    #     return self._servicios().servicio_seleccionado if self._servicios().servicio_seleccionado_valido else None
    
    # @rx.var(cache=True)
    # def termino_busqueda_servicios(self) -> str:
    #     """🔍 Término búsqueda servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().termino_busqueda_servicios
    
    # @rx.var(cache=True)
    # def cargando_lista_servicios(self) -> bool:
    #     """⏳ Cargando servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().cargando_lista_servicios
    
    # @rx.var(cache=True)
    # def errores_validacion_servicio(self) -> Dict[str, str]:
    #     """❌ Errores validación servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().errores_validacion_servicio
    
    # @rx.var(cache=True)
    # def filtro_categoria_servicios(self) -> str:
    #     """🏷️ Filtro categoría servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().filtro_categoria
    
    # @rx.var(cache=True)
    # def filtro_rango_precio_servicios(self) -> Dict[str, float]:
    #     """💰 Filtro rango precio servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().filtro_rango_precio_servicios
    
    # @rx.var(cache=True)
    # def mostrar_solo_activos_servicios(self) -> bool:
    #     """✅ Mostrar solo activos servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().mostrar_solo_activos_servicios
    
    # @rx.var(cache=True)
    # def formulario_servicio_data(self) -> ServicioFormModel:
    #     """📝 Datos formulario servicio - ACCESO DIRECTO UI"""
    #     # Convertir Dict a modelo si es necesario
    #     form_data = self._servicios().formulario_servicio
    #     if isinstance(form_data, dict):
    #         return ServicioFormModel.from_dict(form_data)
    #     return form_data or ServicioFormModel()
    
    # @rx.var(cache=True)
    # def servicio_para_eliminar(self) -> Optional[ServicioModel]:
    #     """🗑️ Servicio a eliminar - ACCESO DIRECTO UI"""
    #     return self._servicios().servicio_para_eliminar
    
    # @rx.var(cache=True)
    # def lista_categorias_servicios(self) -> List[CategoriaServicioModel]:
    #     """🏷️ Lista categorías servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().lista_categorias_servicios
    
    # @rx.var(cache=True)
    # def servicios_mas_populares(self) -> List[ServicioModel]:
    #     """⭐ Servicios más populares - ACCESO DIRECTO UI"""
    #     return self._servicios().servicios_mas_populares
    
    # @rx.var(cache=True)
    # def estadisticas_servicios(self) -> ServicioStatsModel:
    #     """📊 Estadísticas servicios - ACCESO DIRECTO UI"""
    #     return self._servicios().estadisticas_servicios
    
    # # ==========================================
    # # 🦷 COMPUTED VARS: ODONTOLOGÍA (SIN ASYNC)
    # # ==========================================
    
    # @rx.var(cache=True)
    # def lista_pacientes_asignados(self) -> List[PacienteModel]:
    #     """👥 Pacientes asignados al odontólogo - ACCESO DIRECTO UI"""
    #     return self._odontologia().lista_pacientes_asignados
    
    # @rx.var(cache=True)
    # def consultas_pendientes_odontologo(self) -> List[ConsultaModel]:
    #     """📅 Consultas pendientes odontólogo - ACCESO DIRECTO UI"""
    #     return self._odontologia().consultas_pendientes_odontologo
    
    # @rx.var(cache=True)
    # def paciente_odontologia_seleccionado(self) -> Optional[PacienteModel]:
    #     """🎯 Paciente seleccionado odontología - ACCESO DIRECTO UI"""
    #     return self._odontologia().paciente_odontologia_seleccionado
    
    # @rx.var(cache=True)
    # def consulta_actual_odontologia(self) -> Optional[ConsultaModel]:
    #     """📋 Consulta actual odontología - ACCESO DIRECTO UI"""
    #     return self._odontologia().consulta_actual_odontologia
    
    # @rx.var(cache=True)
    # def odontograma_actual(self) -> Optional[OdontogramaModel]:
    #     """🦷 Odontograma actual - ACCESO DIRECTO UI"""
    #     return self._odontologia().odontograma_actual
    
    # @rx.var(cache=True)
    # def lista_dientes_catalogo(self) -> List[DienteModel]:
    #     """🦷 Catálogo de dientes - ACCESO DIRECTO UI"""
    #     return self._odontologia().lista_dientes_catalogo
    
    # @rx.var(cache=True)
    # def condiciones_dientes_actuales(self) -> List[CondicionDienteModel]:
    #     """🔍 Condiciones actuales de dientes - ACCESO DIRECTO UI"""
    #     return self._odontologia().condiciones_dientes_actuales
    
    # @rx.var(cache=True)
    # def diente_seleccionado_odontograma(self) -> Optional[DienteModel]:
    #     """🎯 Diente seleccionado en odontograma - ACCESO DIRECTO UI"""
    #     return self._odontologia().diente_seleccionado_odontograma
    
    # @rx.var(cache=True)
    # def historial_clinico_actual(self) -> Optional[HistorialClinicoModel]:
    #     """📋 Historial clínico actual - ACCESO DIRECTO UI"""
    #     return self._odontologia().historial_clinico_actual
    
    # @rx.var(cache=True)
    # def lista_intervenciones_realizadas(self) -> List[IntervencionModel]:
    #     """🔧 Intervenciones realizadas - ACCESO DIRECTO UI"""
    #     return self._odontologia().lista_intervenciones_realizadas
    
    # @rx.var(cache=True)
    # def formulario_intervencion_data(self) -> IntervencionFormModel:
    #     """📝 Datos formulario intervención - ACCESO DIRECTO UI"""
    #     return self._odontologia().formulario_intervencion_data
    
    # @rx.var(cache=True)
    # def cargando_datos_odontologia(self) -> bool:
    #     """⏳ Cargando datos odontología - ACCESO DIRECTO UI"""
    #     return self._odontologia().cargando_datos_odontologia
    
    # @rx.var(cache=True)
    # def errores_validacion_intervencion(self) -> Dict[str, str]:
    #     """❌ Errores validación intervención - ACCESO DIRECTO UI"""
    #     return self._odontologia().errores_validacion_intervencion
    
    # # ==========================================
    # # 🎨 COMPUTED VARS: UI (SIN ASYNC)
    # # ==========================================
    
    # @rx.var(cache=True)
    # def modal_actual(self) -> str:
    #     """📱 Modal actual - ACCESO DIRECTO UI"""
    #     return self._ui().modal_actual
    
    # @rx.var(cache=True)
    # def mensaje_toast(self) -> str:
    #     """🎨 Mensaje toast - ACCESO DIRECTO UI"""
    #     return self._ui().mensaje_toast
    
    # @rx.var(cache=True)
    # def tipo_toast(self) -> str:
    #     """🎨 Tipo toast - ACCESO DIRECTO UI"""
    #     return self._ui().tipo_toast
    
    # @rx.var(cache=True)
    # def toast_visible(self) -> bool:
    #     """🎨 Toast visible - ACCESO DIRECTO UI"""
    #     return self._ui().toast_visible
    
    # @rx.var(cache=True)
    # def sidebar_collapsed(self) -> bool:
    #     """📱 Sidebar colapsado - ACCESO DIRECTO UI"""
    #     return self._ui().sidebar_collapsed
    
    # @rx.var(cache=True)
    # def current_page(self) -> str:
    #     """📄 Página actual - ACCESO DIRECTO UI"""
    #     return self._ui().current_page
    
    # @rx.var(cache=True)
    # def tema_oscuro_activo(self) -> bool:
    #     """🌙 Tema oscuro activo - ACCESO DIRECTO UI"""
    #     return self._ui().tema_oscuro_activo
    
    # @rx.var(cache=True)
    # def cargando_global(self) -> bool:
    #     """⏳ Cargando global - ACCESO DIRECTO UI"""
    #     return self._ui().cargando_global
    
    # # ==========================================
    # # 🎬 EVENT HANDLERS: PATRÓN OFICIAL REFLEX (ASYNC)
    # # ==========================================
    
    # # ✅ AUTENTICACIÓN - SIGUIENDO PATRÓN OFICIAL
    # @rx.event
    # async def iniciar_sesion(self, form_data: Dict[str, str]):
    #     """🔐 LOGIN - PATRÓN OFICIAL REFLEX"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     result = await auth_state.iniciar_sesion(form_data)
        
    #     # Coordinar después del login
    #     if auth_state.esta_autenticado:
    #         await self.cargar_datos_iniciales()
        
    #     return result
    
    # @rx.event
    # async def cerrar_sesion(self):
    #     """🚪 LOGOUT - PATRÓN OFICIAL REFLEX"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     # Coordinar limpieza de todos los estados
    #     await auth_state.cerrar_sesion()
    #     ui_state.limpiar_ui()
        
    #     # Limpiar datos de otros estados
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     personal_state = await self.get_state(EstadoPersonal)
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     servicios_state = await self.get_state(EstadoServicios)
    #     odontologia_state = await self.get_state(EstadoOdontologia)
        
    #     pacientes_state.limpiar_datos()
    #     personal_state.limpiar_datos()
    #     consultas_state.limpiar_datos()
    #     servicios_state.limpiar_datos()
    #     odontologia_state.limpiar_datos()
        
    #     return rx.redirect("/login")
    
    # # ==========================================
    # # 🔗 ALIASES EVENT HANDLERS PARA COMPATIBILIDAD
    # # ==========================================
    
    # @rx.event
    # async def login(self, form_data: Dict[str, str]):
    #     """🔐 Alias para iniciar_sesion - COMPATIBILIDAD"""
    #     return await self.iniciar_sesion(form_data)
    
    # @rx.event 
    # async def logout(self):
    #     """🚪 Alias para cerrar_sesion - COMPATIBILIDAD"""
    #     return await self.cerrar_sesion()
    
    # @rx.event
    # async def navigate_to(self, page: str, title: str = "", subtitle: str = ""):
    #     """🧭 Navegación entre páginas"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.navigate_to(page, title, subtitle)
    
    # # ✅ PACIENTES - PATRÓN OFICIAL REFLEX
    # @rx.event
    # async def cargar_lista_pacientes(self, force_refresh: bool = False):
    #     """👥 CARGAR PACIENTES - PATRÓN OFICIAL REFLEX"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     if not auth_state.tiene_permiso_pacientes:
    #         return
        
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     await pacientes_state.cargar_lista_pacientes(force_refresh)
    
    # @rx.event
    # async def crear_paciente(self, form_data: Dict[str, Any]):
    #     """➕ CREAR PACIENTE - COORDINACIÓN ENTRE ESTADOS"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         # Crear paciente
    #         resultado = await pacientes_state.crear_paciente(form_data)
            
    #         if resultado:
    #             # Coordinar UI
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Paciente creado exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def actualizar_paciente(self, form_data: Dict[str, Any]):
    #     """✏️ ACTUALIZAR PACIENTE - PATRÓN OFICIAL REFLEX"""
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await pacientes_state.actualizar_paciente(form_data)
            
    #         if resultado:
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Paciente actualizado exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def eliminar_paciente(self):
    #     """🗑️ ELIMINAR PACIENTE - COORDINACIÓN COMPLEJA"""
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         if hasattr(pacientes_state.paciente_seleccionado, 'id') and pacientes_state.paciente_seleccionado.id:
    #             resultado = await pacientes_state.eliminar_paciente()
                
    #             if resultado:
    #                 ui_state.cerrar_modal()
    #                 ui_state.mostrar_toast("Paciente eliminado exitosamente", "success")
    #             else:
    #                 ui_state.mostrar_toast("Error al eliminar paciente", "error")
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def buscar_pacientes(self, query: str):
    #     """🔍 BUSCAR PACIENTES - PATRÓN OFICIAL REFLEX"""
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     await pacientes_state.buscar_pacientes(query)
    
    # @rx.event
    # async def seleccionar_paciente(self, patient_id: str):
    #     """🎯 SELECCIONAR PACIENTE - PATRÓN OFICIAL REFLEX"""
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     await pacientes_state.seleccionar_paciente(patient_id)
    
    # @rx.event
    # async def aplicar_filtros_pacientes(self, filtros: Dict[str, Any]):
    #     """🔍 APLICAR FILTROS PACIENTES - PATRÓN OFICIAL REFLEX"""
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     await pacientes_state.aplicar_filtros_pacientes(filtros)
    
    # # ✅ PERSONAL - PATRÓN OFICIAL REFLEX
    # @rx.event
    # async def cargar_lista_personal(self):
    #     """👨‍⚕️ CARGAR PERSONAL - PATRÓN OFICIAL REFLEX"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     if not auth_state.tiene_permiso_personal:
    #         return
        
    #     personal_state = await self.get_state(EstadoPersonal)
    #     await personal_state.cargar_lista_personal()
    
    # @rx.event
    # async def crear_personal(self, form_data: Dict[str, Any]):
    #     """➕ CREAR PERSONAL - COORDINACIÓN ENTRE ESTADOS"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     personal_state = await self.get_state(EstadoPersonal)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await personal_state.crear_personal(form_data)
            
    #         if resultado:
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Personal creado exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def actualizar_personal(self, form_data: Dict[str, Any]):
    #     """✏️ ACTUALIZAR PERSONAL - PATRÓN OFICIAL REFLEX"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await personal_state.actualizar_personal(form_data)
            
    #         if resultado:
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Personal actualizado exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def eliminar_personal(self):
    #     """🗑️ ELIMINAR PERSONAL - COORDINACIÓN COMPLEJA"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         if hasattr(personal_state.empleado_seleccionado, 'id') and personal_state.empleado_seleccionado.id:
    #             resultado = await personal_state.eliminar_personal()
                
    #             if resultado:
    #                 ui_state.cerrar_modal()
    #                 ui_state.mostrar_toast("Personal eliminado exitosamente", "success")
    #             else:
    #                 ui_state.mostrar_toast("Error al eliminar personal", "error")
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def buscar_personal(self, query: str):
    #     """🔍 BUSCAR PERSONAL - PATRÓN OFICIAL REFLEX"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     await personal_state.buscar_personal(query)
    
    # @rx.event
    # async def seleccionar_personal(self, staff_id: str):
    #     """🎯 SELECCIONAR PERSONAL - PATRÓN OFICIAL REFLEX"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     await personal_state.seleccionar_personal(staff_id)
    
    # @rx.event
    # async def aplicar_filtros_personal(self, filtros: Dict[str, Any]):
    #     """🔍 APLICAR FILTROS PERSONAL - PATRÓN OFICIAL REFLEX"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     await personal_state.aplicar_filtros_personal(filtros)
    
    # # ✅ CONSULTAS - PATRÓN OFICIAL REFLEX
    # @rx.event
    # async def cargar_lista_consultas(self):
    #     """📅 CARGAR CONSULTAS - PATRÓN OFICIAL REFLEX"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     if not auth_state.tiene_permiso_consultas:
    #         return
        
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     await consultas_state.cargar_lista_consultas()
    
    # @rx.event
    # async def crear_consulta(self, form_data: Dict[str, Any]):
    #     """➕ CREAR CONSULTA - COORDINACIÓN COMPLEJA"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     pacientes_state = await self.get_state(EstadoPacientes)
    #     personal_state = await self.get_state(EstadoPersonal)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         # Coordinación compleja entre múltiples estados
    #         resultado = await consultas_state.crear_consulta(form_data)
            
    #         if resultado:
    #             # Actualizar paciente si es necesario
    #             if form_data.get("paciente_id"):
    #                 await pacientes_state.actualizar_ultimo_acceso(form_data["paciente_id"])
                
    #             # Actualizar estadísticas del personal
    #             if form_data.get("odontologo_id"):
    #                 await personal_state.actualizar_estadisticas_doctor(form_data["odontologo_id"])
                
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Consulta creada exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def actualizar_consulta(self, form_data: Dict[str, Any]):
    #     """✏️ ACTUALIZAR CONSULTA - PATRÓN OFICIAL REFLEX"""
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await consultas_state.actualizar_consulta(form_data)
            
    #         if resultado:
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Consulta actualizada exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def cambiar_estado_consulta(self, consulta_id: str, nuevo_estado: str):
    #     """🔄 CAMBIAR ESTADO CONSULTA - PATRÓN OFICIAL REFLEX"""
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await consultas_state.cambiar_estado_consulta(consulta_id, nuevo_estado)
            
    #         if resultado:
    #             ui_state.mostrar_toast(f"Estado cambiado a {nuevo_estado}", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def buscar_consultas(self, query: str):
    #     """🔍 BUSCAR CONSULTAS - PATRÓN OFICIAL REFLEX"""
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     await consultas_state.buscar_consultas(query)
    
    # @rx.event
    # async def seleccionar_consulta(self, consultation_id: str):
    #     """🎯 SELECCIONAR CONSULTA - PATRÓN OFICIAL REFLEX"""
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     await consultas_state.seleccionar_consulta(consultation_id)
    
    # @rx.event
    # async def aplicar_filtros_consultas(self, filtros: Dict[str, Any]):
    #     """🔍 APLICAR FILTROS CONSULTAS - PATRÓN OFICIAL REFLEX"""
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     await consultas_state.aplicar_filtros_consultas(filtros)
    
    # # ✅ SERVICIOS - PATRÓN OFICIAL REFLEX
    # @rx.event
    # async def cargar_lista_servicios(self):
    #     """🏥 CARGAR SERVICIOS - PATRÓN OFICIAL REFLEX"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     if not auth_state.tiene_permiso_servicios:
    #         return
        
    #     servicios_state = await self.get_state(EstadoServicios)
    #     await servicios_state.cargar_lista_servicios()
    
    # @rx.event
    # async def crear_servicio(self, form_data: Dict[str, Any]):
    #     """➕ CREAR SERVICIO - COORDINACIÓN ENTRE ESTADOS"""
    #     servicios_state = await self.get_state(EstadoServicios)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await servicios_state.crear_servicio(form_data)
            
    #         if resultado:
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Servicio creado exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def actualizar_servicio(self, form_data: Dict[str, Any]):
    #     """✏️ ACTUALIZAR SERVICIO - PATRÓN OFICIAL REFLEX"""
    #     servicios_state = await self.get_state(EstadoServicios)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await servicios_state.actualizar_servicio(form_data)
            
    #         if resultado:
    #             ui_state.cerrar_modal()
    #             ui_state.mostrar_toast("Servicio actualizado exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def eliminar_servicio(self):
    #     """🗑️ ELIMINAR SERVICIO - COORDINACIÓN COMPLEJA"""
    #     servicios_state = await self.get_state(EstadoServicios)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         if hasattr(servicios_state, 'servicio_seleccionado') and hasattr(servicios_state.servicio_seleccionado, 'id') and servicios_state.servicio_seleccionado.id:
    #             resultado = await servicios_state.eliminar_servicio()
                
    #             if resultado:
    #                 ui_state.cerrar_modal()
    #                 ui_state.mostrar_toast("Servicio eliminado exitosamente", "success")
    #             else:
    #                 ui_state.mostrar_toast("Error al eliminar servicio", "error")
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def buscar_servicios(self, query: str):
    #     """🔍 BUSCAR SERVICIOS - PATRÓN OFICIAL REFLEX"""
    #     servicios_state = await self.get_state(EstadoServicios)
    #     await servicios_state.buscar_servicios(query)
    
    # @rx.event
    # async def seleccionar_servicio(self, service_id: str):
    #     """🎯 SELECCIONAR SERVICIO - PATRÓN OFICIAL REFLEX"""
    #     servicios_state = await self.get_state(EstadoServicios)
    #     await servicios_state.seleccionar_servicio(service_id)
    
    # @rx.event
    # async def aplicar_filtros_servicios(self, filtros: Dict[str, Any]):
    #     """🔍 APLICAR FILTROS SERVICIOS - PATRÓN OFICIAL REFLEX"""
    #     servicios_state = await self.get_state(EstadoServicios)
    #     await servicios_state.aplicar_filtros_servicios(filtros)
    
    # # ✅ ODONTOLOGÍA - PATRÓN OFICIAL REFLEX
    # @rx.event
    # async def cargar_pacientes_asignados(self):
    #     """🦷 CARGAR PACIENTES ASIGNADOS - PATRÓN OFICIAL REFLEX"""
    #     auth_state = await self.get_state(EstadoAuth)
    #     if not auth_state.tiene_permiso_odontologia:
    #         return
        
    #     odontologia_state = await self.get_state(EstadoOdontologia)
    #     await odontologia_state.cargar_pacientes_asignados()
    
    # @rx.event
    # async def seleccionar_paciente_odontologia(self, patient_id: str):
    #     """🎯 SELECCIONAR PACIENTE ODONTOLOGÍA - COORDINACIÓN COMPLEJA"""
    #     odontologia_state = await self.get_state(EstadoOdontologia)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await odontologia_state.seleccionar_paciente_odontologia(patient_id)
            
    #         if resultado:
    #             # Cargar datos relacionados
    #             await odontologia_state.cargar_odontograma_paciente(patient_id)
    #             await odontologia_state.cargar_historial_clinico(patient_id)
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def crear_intervencion(self, form_data: Dict[str, Any]):
    #     """🔧 CREAR INTERVENCIÓN - COORDINACIÓN COMPLEJA"""
    #     odontologia_state = await self.get_state(EstadoOdontologia)
    #     consultas_state = await self.get_state(EstadoConsultas)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         # Coordinación entre odontología y consultas
    #         resultado = await odontologia_state.crear_intervencion(form_data)
            
    #         if resultado:
    #             # Actualizar estado de consulta si es necesario
    #             if form_data.get("consulta_id"):
    #                 await consultas_state.actualizar_estado_consulta_intervencion(
    #                     form_data["consulta_id"], "en_progreso"
    #                 )
                
    #             ui_state.mostrar_toast("Intervención creada exitosamente", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def actualizar_condicion_diente(self, diente_data: Dict[str, Any]):
    #     """🦷 ACTUALIZAR CONDICIÓN DIENTE - PATRÓN OFICIAL REFLEX"""
    #     odontologia_state = await self.get_state(EstadoOdontologia)
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         resultado = await odontologia_state.actualizar_condicion_diente(diente_data)
            
    #         if resultado:
    #             ui_state.mostrar_toast("Condición de diente actualizada", "success")
            
    #         return resultado
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error: {str(e)}", "error")
    
    # @rx.event
    # async def seleccionar_diente_odontograma(self, diente_id: str):
    #     """🎯 SELECCIONAR DIENTE ODONTOGRAMA - PATRÓN OFICIAL REFLEX"""
    #     odontologia_state = await self.get_state(EstadoOdontologia)
    #     await odontologia_state.seleccionar_diente_odontograma(diente_id)
    
    # # ✅ UI - PATRÓN OFICIAL REFLEX
    # @rx.event
    # async def abrir_modal(self, modal_id: str):
    #     """📱 ABRIR MODAL - PATRÓN OFICIAL REFLEX"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.abrir_modal(modal_id)
    
    # @rx.event
    # async def cerrar_modal(self):
    #     """📱 CERRAR MODAL - PATRÓN OFICIAL REFLEX"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.cerrar_modal()
    
    # @rx.event
    # async def mostrar_toast(self, message: str, toast_type: str = "info"):
    #     """🎨 MOSTRAR TOAST - PATRÓN OFICIAL REFLEX"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.mostrar_toast(message, toast_type)
    
    # @rx.event
    # async def ocultar_toast(self):
    #     """🎨 OCULTAR TOAST - PATRÓN OFICIAL REFLEX"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.ocultar_toast()
    
    # @rx.event
    # async def toggle_sidebar(self):
    #     """📱 TOGGLE SIDEBAR - PATRÓN OFICIAL REFLEX"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.toggle_sidebar()
    
    # @rx.event
    # async def cambiar_pagina(self, nueva_pagina: str):
    #     """📄 CAMBIAR PÁGINA - PATRÓN OFICIAL REFLEX"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.cambiar_pagina(nueva_pagina)
    
    # @rx.event
    # async def toggle_tema_oscuro(self):
    #     """🌙 TOGGLE TEMA OSCURO - PATRÓN OFICIAL REFLEX"""
    #     ui_state = await self.get_state(EstadoUI)
    #     ui_state.toggle_tema_oscuro()
    
    # # ==========================================
    # # 🚀 COORDINACIÓN COMPLEJA ENTRE ESTADOS
    # # ==========================================
    
    # @rx.event
    # async def cargar_datos_iniciales(self):
    #     """🚀 CARGAR DATOS INICIALES - COORDINACIÓN MASIVA"""
    #     auth_state = await self.get_state(EstadoAuth)
        
    #     if not auth_state.sesion_valida:
    #         return
        
    #     # Cargar según permisos del usuario
    #     tasks = []
        
    #     if auth_state.tiene_permiso_pacientes:
    #         tasks.append(self.cargar_lista_pacientes())
        
    #     if auth_state.tiene_permiso_consultas:
    #         tasks.append(self.cargar_lista_consultas())
        
    #     if auth_state.tiene_permiso_personal:
    #         tasks.append(self.cargar_lista_personal())
        
    #     if auth_state.tiene_permiso_servicios:
    #         tasks.append(self.cargar_lista_servicios())
        
    #     if auth_state.tiene_permiso_odontologia:
    #         tasks.append(self.cargar_pacientes_asignados())
        
    #     # Ejecutar en paralelo
    #     if tasks:
    #         await asyncio.gather(*tasks, return_exceptions=True)
        
    #     print("✅ Datos iniciales cargados usando patrón oficial Reflex")
    
    # @rx.event
    # async def coordinar_operacion_compleja(self, operacion_data: Dict[str, Any]):
    #     """🔄 COORDINACIÓN COMPLEJA - EJEMPLO PATRÓN OFICIAL"""
    #     # ✅ ESTE ES EL PATRÓN QUE RECOMIENDA REFLEX
    #     auth_state = await self.get_state(EstadoAuth)
    #     consultas_state = await self.get_state(EstadoConsultas)  
    #     pacientes_state = await self.get_state(EstadoPacientes)  
    #     personal_state = await self.get_state(EstadoPersonal)
    #     ui_state = await self.get_state(EstadoUI)
          
    #     try:
    #         # Coordinar operaciones entre estados  
    #         resultado_consulta = await consultas_state.crear_consulta(operacion_data.get("consulta_data"))
    #         resultado_paciente = await pacientes_state.actualizar_paciente(operacion_data.get("paciente_data"))
    #         resultado_personal = await personal_state.actualizar_estadisticas(operacion_data.get("doctor_id"))
            
    #         # Mostrar resultado
    #         if all([resultado_consulta, resultado_paciente, resultado_personal]):
    #             ui_state.mostrar_toast("Operación compleja completada exitosamente", "success")
    #         else:
    #             ui_state.mostrar_toast("Error en operación compleja", "error")
                
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error en coordinación: {str(e)}", "error")
    
    # @rx.event
    # async def sincronizar_datos_completos(self):
    #     """🔄 SINCRONIZACIÓN COMPLETA - COORDINACIÓN MASIVA"""
    #     ui_state = await self.get_state(EstadoUI)
        
    #     try:
    #         ui_state.mostrar_cargando_global(True)
            
    #         # Recargar todos los datos
    #         await self.cargar_datos_iniciales()
            
    #         # Actualizar estadísticas
    #         # await self.actualizar_estadisticas_dashboard()
            
    #         ui_state.mostrar_toast("Datos sincronizados exitosamente", "success")
            
    #     except Exception as e:
    #         ui_state.mostrar_toast(f"Error en sincronización: {str(e)}", "error")
    #     finally:
    #         ui_state.mostrar_cargando_global(False)
    
    # # ==========================================
    # # 🔧 MÉTODOS HELPER (NO ASYNC)
    # # ==========================================
    
    # def obtener_contexto_usuario(self) -> Dict[str, Any]:
    #     """📋 Contexto del usuario (sin async)"""
    #     return self._auth().obtener_contexto_usuario()
    
    # def validar_permiso_para_operacion(self, module: str, operation: str) -> bool:
    #     """🔒 Validar permiso (sin async)"""
    #     return self._auth().validar_permiso_para_operacion(module, operation)
    
    # def obtener_resumen_estado_actual(self) -> Dict[str, Any]:
    #     """📊 Resumen del estado actual (sin async)"""
    #     return {
    #         "autenticado": self.esta_autenticado,
    #         "usuario": self.nombre_usuario_display,
    #         "rol": self.rol_usuario_display,
    #         "total_pacientes": self.total_pacientes,
    #         "total_personal": self.total_personal,
    #         "total_consultas": self.total_consultas,
    #         "total_servicios": self.total_servicios,
    #         "modal_actual": self.modal_actual,
    #         "cargando": self.cargando_global
    #     }
    
    # # ==========================================
    # # 🔗 MÉTODOS PÚBLICOS DE ACCESO A SUBSTATES
    # # ==========================================
    
    # def get_estado_pacientes(self) -> EstadoPacientes:
    #     """👥 Acceso público al substate de pacientes"""
    #     return self.get_state(EstadoPacientes)
    
    # def get_estado_consultas(self) -> EstadoConsultas:
    #     """📅 Acceso público al substate de consultas"""
    #     return self.get_state(EstadoConsultas)
    
    # def get_estado_servicios(self) -> EstadoServicios:
    #     """🏥 Acceso público al substate de servicios"""
    #     return self.get_state(EstadoServicios)
    
    # def get_estado_pagos(self):
    #     """💳 Acceso público al substate de pagos"""
    #     from .estado_pagos import EstadoPagos
    #     return self.get_state(EstadoPagos)
    
    # def get_estado_odontologia(self) -> EstadoOdontologia:
    #     """🦷 Acceso público al substate de odontología"""
    #     return self.get_state(EstadoOdontologia)
    
    # def get_estado_personal(self) -> EstadoPersonal:
    #     """👨‍⚕️ Acceso público al substate de personal"""
    #     return self.get_state(EstadoPersonal)
    
    # def get_estado_auth(self) -> EstadoAuth:
    #     """🔐 Acceso público al substate de autenticación"""
    #     return self.get_state(EstadoAuth)
    
    # def get_estado_ui(self) -> EstadoUI:
    #     """🎨 Acceso público al substate de UI"""
    #     return self.get_state(EstadoUI)
    
    # # ==========================================
    # # 📊 EVENT HANDLERS DASHBOARD
    # # ==========================================
    
    # @rx.event
    # async def load_dashboard_stats(self):
    #     """📊 Cargar estadísticas del dashboard"""
    #     # Por ahora solo un placeholder para evitar errores
    #     # TODO: Implementar carga de estadísticas reales
    #     print("📊 Cargando estadísticas del dashboard...")
    #     return True
    
    # @rx.event
    # async def toggle_areachart(self):
    #     """📈 Toggle para alternar gráficas de área"""
    #     # TODO: Implementar toggle real
    #     print("📈 Toggle areachart...")
    #     return True
    
    # @rx.event
    # async def set_selected_tab(self, tab: str):
    #     """📊 Cambiar tab seleccionado en dashboard"""
    #     print(f"📊 Tab seleccionado: {tab}")
    #     return True
    
    # # ==========================================
    # # 👨‍⚕️ EVENT HANDLERS PERSONAL - SIMPLES
    # # ==========================================
    
    # @rx.event
    # async def abrir_modal_personal(self, personal_id: str = ""):
    #     """👨‍⚕️ Abrir modal personal - Crear (si ID vacío) o Editar (si tiene ID)"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     await personal_state.abrir_modal_personal(personal_id)
    
    # @rx.event
    # async def seleccionar_personal_para_eliminar(self, personal_id: str):
    #     """🗑️ Seleccionar personal para eliminar"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     await personal_state.seleccionar_personal_para_eliminar(personal_id)
    
    # @rx.event
    # async def reactivar_personal(self, personal_id: str):
    #     """🔄 Reactivar personal"""
    #     personal_state = await self.get_state(EstadoPersonal)
    #     await personal_state.reactivar_empleado(personal_id)