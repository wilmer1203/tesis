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

class AppState(EstadoServicios,EstadoConsultas,EstadoOdontologia,EstadoPersonal,EstadoAuth, EstadoPacientes,EstadoUI,rx.State):
    """
    🎯 APPSTATE DEFINITIVO CON MIXINS
    
    Hereda de todos los substates como mixins:
    - EstadoAuth: Autenticación y permisos
    - EstadoUI: Navegación y estados de UI
    - EstadoPacientes: Gestión de pacientes
    - EstadoPersonal: Gestión de empleados
    - EstadoConsultas: Sistema de turnos
    - EstadoServicios: Catálogo de servicios
    - EstadoOdontologia: Módulo dental
    """
    
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
        """🚀 INICIALIZACIÓN COMPLETA DESPUÉS DEL LOGIN
        
        Carga todos los datos esenciales una sola vez para que 
        la navegación sea instantánea
        """
        try:
            print("🚀 Iniciando carga de datos post-login...")
            
            # Cargar datos en paralelo para máxima velocidad
            await asyncio.gather(
                # Datos esenciales para todas las páginas
                self.cargar_lista_pacientes(),
                self.cargar_lista_personal(),
                self.cargar_estadisticas_personal(),
                self.cargar_estadisticas_dashboard(),
                
                # Agregar aquí otros módulos cuando estén listos:
                self.cargar_lista_consultas(),
                # self.cargar_lista_servicios(), 
                # self.cargar_lista_pagos(),
                
                return_exceptions=True  # No fallar si uno falla
            )
            
            print("✅ Inicialización post-login completada")
            print("🎯 Datos disponibles: Pacientes, Personal, Dashboard")
            
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
    async def cambiar_estado_consulta(self, consulta_id: str, nuevo_estado: str):
        """🔄 Cambiar estado de una consulta - FUNCIONAL"""
        try:
            print(f"🔄 Cambiando estado de consulta {consulta_id} a {nuevo_estado}")
            
            # Usar el service de consultas existente
            consultas_state = await self.get_state(EstadoConsultas)
            success = await consultas_state.cambiar_estado_consulta(consulta_id, nuevo_estado)
            
            if success:
                self.success_message = f"Consulta {nuevo_estado} exitosamente"
                # Recargar consultas para actualizar UI
                await self.cargar_lista_consultas()
            else:
                self.error_message = "Error cambiando estado de la consulta"
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"❌ Error cambiando estado: {e}")
    
    @rx.event
    async def cancelar_consulta(self, consulta_id: str):
        """❌ Cancelar una consulta - FUNCIONAL"""
        try:
            print(f"❌ Cancelando consulta: {consulta_id}")
            
            # Usar el service de consultas existente
            consultas_state = await self.get_state(EstadoConsultas)
            success = await consultas_state.cancelar_consulta(consulta_id)
            
            if success:
                self.success_message = "Consulta cancelada exitosamente"
                await self.cargar_lista_consultas()
            else:
                self.error_message = "Error cancelando la consulta"
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"❌ Error cancelando consulta: {e}")
    
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
    # 📝 VARIABLES PARA MODAL NUEVA CONSULTA FASE 1
    # ==========================================
    
    # Variables del formulario simplificado
    consulta_form_odontologo_id: str = ""
    consulta_form_busqueda_paciente: str = ""
    consulta_form_paciente_seleccionado: PacienteModel = PacienteModel()
    consulta_form_tipo_consulta: str = "general"
    consulta_form_prioridad: str = "normal"
    consulta_form_motivo: str = ""
    cargando_crear_consulta: bool = False
    
    # ==========================================
    # 📝 MÉTODOS PARA MODAL NUEVA CONSULTA FASE 1
    # ==========================================
    
    @rx.event
    def set_consulta_form_odontologo_id(self, value: str):
        """👨‍⚕️ Seleccionar odontólogo"""
        self.consulta_form_odontologo_id = value
    
    @rx.event
    def set_consulta_form_busqueda_paciente(self, value: str):
        """🔍 Actualizar búsqueda de paciente"""
        self.consulta_form_busqueda_paciente = value
    
    @rx.event  
    def set_consulta_form_tipo_consulta(self, value: str):
        """📋 Seleccionar tipo de consulta"""
        self.consulta_form_tipo_consulta = value
    
    @rx.event
    def set_consulta_form_prioridad(self, value: str):
        """🚨 Seleccionar prioridad"""
        self.consulta_form_prioridad = value
    
    @rx.event
    def set_consulta_form_motivo(self, value: str):
        """📝 Actualizar motivo"""
        self.consulta_form_motivo = value
    
    @rx.event
    def seleccionar_paciente_modal(self, paciente_id: str):
        """👤 Seleccionar paciente desde resultados de búsqueda"""
        # Buscar el paciente en la lista filtrada
        for paciente in self.pacientes_filtrados_modal:
            if paciente.id == paciente_id:
                self.consulta_form_paciente_seleccionado = paciente
                self.consulta_form_busqueda_paciente = ""
                break
        print(f"👤 Paciente seleccionado: {self.consulta_form_paciente_seleccionado.nombre_completo}")
    
    @rx.event
    def limpiar_paciente_seleccionado(self):
        """🗑️ Limpiar paciente seleccionado"""
        self.consulta_form_paciente_seleccionado = PacienteModel()
        self.consulta_form_busqueda_paciente = ""
    
    @rx.event
    def abrir_modal_crear_consulta(self):
        """📝 Abrir modal de crear consulta"""
        self.modal_crear_consulta_abierto = True
        # Limpiar formulario
        self.consulta_form_odontologo_id = ""
        self.consulta_form_busqueda_paciente = ""
        self.consulta_form_paciente_seleccionado = PacienteModel()
        self.consulta_form_tipo_consulta = "general"
        self.consulta_form_prioridad = "normal"
        self.consulta_form_motivo = ""
    
    @rx.event
    async def crear_nueva_consulta(self):
        """✅ Crear nueva consulta"""
        try:
            self.cargando_crear_consulta = True
            
            # Validar que tenga odontólogo y paciente
            if not self.consulta_form_odontologo_id:
                self.error_message = "Debe seleccionar un odontólogo"
                return
                
            if not self.consulta_form_paciente_seleccionado.id:
                self.error_message = "Debe seleccionar un paciente"
                return
            
            # Crear usando el service existente
            consultas_state = await self.get_state(EstadoConsultas)
            
            # Preparar datos del formulario
            form_consulta = {
                'paciente_id': self.consulta_form_paciente_seleccionado.id,
                'odontologo_id': self.consulta_form_odontologo_id,
                'tipo_consulta': self.consulta_form_tipo_consulta,
                'prioridad': self.consulta_form_prioridad,
                'motivo_consulta': self.consulta_form_motivo if self.consulta_form_motivo else None
            }
            
            # Crear la consulta
            await consultas_state.crear_consulta(form_consulta)
            
            # Cerrar modal y limpiar formulario
            self.modal_crear_consulta_abierto = False
            self.success_message = "Consulta creada exitosamente"
            
            # Recargar consultas
            await self.cargar_lista_consultas()
            
        except Exception as e:
            self.error_message = f"Error creando consulta: {str(e)}"
            print(f"❌ Error creando consulta: {e}")
        finally:
            self.cargando_crear_consulta = False
    
    @rx.var
    def pacientes_filtrados_modal(self) -> List[PacienteModel]:
        """🔍 Pacientes filtrados para el modal (máximo 5 resultados)"""
        if not self.consulta_form_busqueda_paciente or len(self.consulta_form_busqueda_paciente) < 2:
            return []
        
        search_lower = self.consulta_form_busqueda_paciente.lower()
        filtered = []
        
        for paciente in self.lista_pacientes:
            # Buscar en nombre completo o documento
            nombre_completo = f"{paciente.primer_nombre} {paciente.primer_apellido}".lower()
            documento = paciente.numero_documento.lower() if paciente.numero_documento else ""
            
            if search_lower in nombre_completo or search_lower in documento:
                filtered.append(paciente)
                
            # Limitar a 5 resultados para no sobrecargar UI
            if len(filtered) >= 5:
                break
                
        return filtered
    
    # ==========================================
    # 🔗 COMPUTED VARS PARA FASE 2 - FUNCIONALIDAD DINÁMICA
    # ==========================================
    
    @rx.var
    def consultas_por_doctor_dict(self) -> Dict[str, List[ConsultaModel]]:
        """📋 Diccionario con consultas agrupadas por doctor"""
        consultas_dict = {}
        for consulta in self.lista_consultas:
            if consulta.estado in ["programada", "en_curso"]:
                if consulta.odontologo_id not in consultas_dict:
                    consultas_dict[consulta.odontologo_id] = []
                consultas_dict[consulta.odontologo_id].append(consulta)
        
        # Ordenar cada lista por fecha/hora
        for doctor_id in consultas_dict:
            consultas_dict[doctor_id] = sorted(
                consultas_dict[doctor_id], 
                key=lambda c: c.fecha_programada or ""
            )
        
        return consultas_dict
    
    @rx.var
    def conteos_consultas_por_doctor(self) -> Dict[str, int]:
        """🔢 Conteos de consultas por doctor"""
        conteos = {}
        for doctor_id, consultas in self.consultas_por_doctor_dict.items():
            conteos[doctor_id] = len(consultas)
        return conteos
    
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
                    es_siguiente=(index == 1 and consulta.estado == "programada")
                )
                consultas_con_orden.append(consulta_con_orden)
            resultado[doctor_id] = consultas_con_orden
        return resultado
    
    def _calcular_tiempo_espera(self, posicion: int, estado: str) -> str:
        """⏱️ Calcular tiempo de espera estimado"""
        if estado == "en_curso":
            return "En atención ahora"
        elif posicion == 1:
            return "Siguiente en cola"
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
    
