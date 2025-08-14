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
    CategoriaServicioModel, ConceptoPagoModel,
    
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
                # self.cargar_lista_consultas(),
                # self.cargar_lista_servicios(), 
                # self.cargar_lista_pagos(),
                
                return_exceptions=True  # No fallar si uno falla
            )
            
            print("✅ Inicialización post-login completada")
            print("🎯 Datos disponibles: Pacientes, Personal, Dashboard")
            
        except Exception as e:
            print(f"⚠️ Error en inicialización post-login: {e}")
            # No lanzar excepción para no bloquear el login