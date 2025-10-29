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
# REFACTOR FASE 4: estado_odontograma_avanzado eliminado - funcionalidad en EstadoOdontologia

# ✅ MODELOS TIPADOS PARA COMPUTED VARS
from dental_system.models import ( PersonalModel, ConsultaModel)

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
                    self.cargar_servicios_basico(),
                    self.cargar_lista_consultas(),
                    self.cargar_pacientes_asignados(),
                    self.cargar_consultas_disponibles_otros(),
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

    # ==========================================
    # 🔗 NAVEGACIÓN ENTRE MÓDULOS
    # ==========================================
    
    # @rx.event
    # async def navegar_a_odontologia_consulta(self, consulta_id: str, paciente_id: Optional[str] = None):
    #     """
    #     🦷 NAVEGAR A MÓDULO DE ODONTOLOGÍA CON CONSULTA ESPECÍFICA

    #     Delega al método especializado seleccionar_paciente_consulta() que:
    #     1. Busca y carga paciente + consulta
    #     2. Cambia estado de consulta a "en_atencion"
    #     3. Carga odontograma última versión
    #     4. Carga intervenciones previas
    #     5. Navega a página de intervención

    #     Args:
    #         consulta_id: ID de la consulta a atender
    #     """
    #     try:
    #         logger.info(f"🦷 Iniciando navegación a odontología con consulta: {consulta_id}")

    #         # Buscar la consulta en ambas listas
    #         consulta_encontrada = None

    #         # Buscar en lista_consultas (EstadoConsultas)
    #         for consulta in self.lista_consultas:
    #             if consulta.id == consulta_id:
    #                 consulta_encontrada = consulta
    #                 break

    #         # Buscar en consultas_asignadas (EstadoOdontologia)
    #         if not consulta_encontrada:
    #             for consulta in self.consultas_asignadas:
    #                 if consulta.id == consulta_id:
    #                     consulta_encontrada = consulta
    #                     break

    #         if not consulta_encontrada:
    #             logger.warning(f"❌ Consulta no encontrada: {consulta_id}")
    #             return

    #         # Obtener paciente_id de la consulta
    #         paciente_id = consulta_encontrada.paciente_id

    #         if not paciente_id:
    #             logger.error(f"❌ Consulta sin paciente_id: {consulta_id}")
    #             return

    #         # Usar el método especializado que maneja todo el flujo
    #         await self.seleccionar_paciente_consulta(paciente_id, consulta_id)

    #         logger.info(f"✅ Navegación completada exitosamente")

    #     except Exception as e:
    #         logger.error(f"❌ Error navegando a odontología: {str(e)}")
    #         import traceback
    #         traceback.print_exc()
    

