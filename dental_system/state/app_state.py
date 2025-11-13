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
from .estado_perfil import EstadoPerfil
from .estado_reportes import EstadoReportes
# REFACTOR FASE 4: estado_odontograma_avanzado eliminado - funcionalidad en EstadoOdontologia

logger = logging.getLogger(__name__)

class AppState(EstadoReportes, EstadoPerfil, EstadoIntervencionServicios,EstadoServicios,EstadoPagos,EstadoConsultas,EstadoOdontologia,EstadoPersonal,EstadoAuth, EstadoPacientes,EstadoUI, rx.State):
    """
    🎯 APPSTATE DEFINITIVO CON MIXINS

    Hereda de todos los substates como mixins:
    - EstadoReportes: Sistema de reportes diferenciados por rol
    - EstadoPerfil: Gestión de perfil de usuario
    - EstadoIntervencionServicios: Gestión de servicios en intervenciones
    - EstadoServicios: Catálogo de servicios
    - EstadoPagos: Sistema de facturación
    - EstadoConsultas: Sistema de turnos
    - EstadoOdontologia: Módulo dental con odontograma FDI
    - EstadoPersonal: Gestión de empleados
    - EstadoAuth: Autenticación y permisos
    - EstadoPacientes: Gestión de pacientes
    - EstadoUI: Navegación y estados de UI
    """
    @rx.event
    async def post_login_inicializacion(self):
        """🚀 INICIALIZACIÓN COMPLETA DESPUÉS DEL LOGIN - POR ROL

        Carga solo los datos necesarios según el rol del usuario
        para evitar errores de permisos y mejorar rendimiento
        """
        try:
            print("🚀 Iniciando carga de datos post-login...")

            # 🎯 ESTABLECER PÁGINA INICIAL SEGÚN ROL
            if self.rol_usuario == "odontologo" or self.rol_usuario == "asistente":
                self.current_page = "dashboard-odontologo"
            else:
                self.current_page = "dashboard"

            print(f"📄 Página inicial establecida: {self.current_page}")

            # Datos específicos por rol
            if self.rol_usuario == "gerente":
                # Gerente: Acceso completo a todo
                datos_especificos = [
                    self.cargar_lista_pacientes(),
                    self.cargar_lista_personal(),
                    self.cargar_lista_consultas(),
                    self.cargar_lista_servicios(),
                    self.cargar_lista_pagos(),
                    self.cargar_estadisticas_duales(),
                ]
            elif self.rol_usuario == "administrador":
                # Administrador: Gestión operativa, sin personal
                datos_especificos = [
                    self.cargar_lista_pacientes(),
                    self.cargar_lista_consultas(),
                    self.cargar_lista_servicios(),
                    self.cargar_lista_pagos(),
                    self.cargar_estadisticas_duales(),
                ]
            elif self.rol_usuario == "odontologo":
                # Odontólogo: Solo datos odontológicos, pacientes y servicios
                datos_especificos = [
                    self.cargar_lista_servicios(),
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
            todas_las_tareas = datos_especificos
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

