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
            if self.rol_usuario == "odontologo":
                self.current_page = "dashboard-odontologo"
            elif self.rol_usuario == "asistente":
                self.current_page = "dashboard-asistente"
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
            consulta_reciente = max(consultas_paciente, key=lambda c: c.fecha_llegada or "")
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
    # 🔔 COMPUTED VARS PARA ACTIVIDAD RECIENTE
    # ==========================================

    @rx.var(cache=False)
    def actividades_recientes(self) -> list[dict]:
        """🔔 Últimas 10 actividades del sistema (pacientes + consultas + pagos)"""
        from dental_system.models.dashboard_models import ActividadReciente

        actividades = []

        try:
            # 🆕 Últimos 5 pacientes registrados
            pacientes_recientes = sorted(
                [p for p in self.lista_pacientes if p.fecha_registro],
                key=lambda p: p.fecha_registro,
                reverse=True
            )[:5]

            for pac in pacientes_recientes:
                actividades.append(ActividadReciente(
                    tipo="paciente",
                    titulo=f"Nuevo paciente: {pac.nombre_completo}",
                    descripcion=f"HC: {pac.numero_historia}",
                    tiempo_relativo=self._calcular_tiempo_relativo(pac.fecha_registro),
                    icono="user-plus",
                    color="#00D4FF"  # cyan
                ))

            # ✅ Últimas 5 consultas completadas
            consultas_completadas = sorted(
                [c for c in self.lista_consultas if c.estado == "completada" and c.fecha_llegada],
                key=lambda c: c.fecha_llegada,
                reverse=True
            )[:5]

            for cons in consultas_completadas:
                actividades.append(ActividadReciente(
                    tipo="consulta",
                    titulo="Consulta finalizada",
                    descripcion=f"Paciente: {cons.paciente_nombre if cons.paciente_nombre else 'N/A'}",
                    tiempo_relativo=self._calcular_tiempo_relativo(cons.fecha_llegada),
                    icono="check-circle",
                    color="#00FF9D"  # green
                ))

            # 💰 Últimos 5 pagos procesados
            if hasattr(self, 'lista_pagos') and self.lista_pagos:
                pagos_recientes = sorted(
                    [p for p in self.lista_pagos if getattr(p, 'estado', '') == "completado" and getattr(p, 'fecha_pago', '')],
                    key=lambda p: getattr(p, 'fecha_pago', ''),
                    reverse=True
                )[:5]

                for pago in pagos_recientes:
                    monto = getattr(pago, 'monto_total', 0) or getattr(pago, 'total_usd', 0)
                    actividades.append(ActividadReciente(
                        tipo="pago",
                        titulo="Pago procesado",
                        descripcion=f"Monto: ${monto:.2f}" if monto else "Monto: N/A",
                        tiempo_relativo=self._calcular_tiempo_relativo(getattr(pago, 'fecha_pago', '')),
                        icono="dollar-sign",
                        color="#FFD700"  # gold
                    ))

            # Convertir a diccionarios simples para compatibilidad con Reflex
            return [
                {
                    "tipo": a.tipo,
                    "titulo": a.titulo,
                    "descripcion": a.descripcion,
                    "tiempo_relativo": a.tiempo_relativo,
                    "icono": a.icono,
                    "color": a.color
                }
                for a in actividades[:10]
            ]

        except Exception as e:
            logger.error(f"Error al obtener actividades recientes: {e}")
            return []

    def _calcular_tiempo_relativo(self, fecha_str: str) -> str:
        """🕐 Calcula tiempo relativo desde una fecha (ej: 'hace 2h', 'hace 30m')"""
        try:
            if not fecha_str:
                return "Fecha desconocida"

            from datetime import datetime, timezone

            # Parsear la fecha (asumiendo formato ISO con o sin Z)
            if 'T' in fecha_str:
                # Formato ISO con hora
                fecha_limpia = fecha_str.replace('Z', '+00:00')
                try:
                    fecha = datetime.fromisoformat(fecha_limpia)
                except:
                    # Si falla, intentar sin timezone
                    fecha = datetime.fromisoformat(fecha_str.split('+')[0].split('Z')[0])
                    if fecha.tzinfo is None:
                        fecha = fecha.replace(tzinfo=timezone.utc)
            else:
                # Solo fecha YYYY-MM-DD
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                fecha = fecha.replace(tzinfo=timezone.utc)

            # Comparar con ahora
            ahora = datetime.now(timezone.utc)
            if fecha.tzinfo is None:
                ahora = datetime.now()

            diferencia = ahora - fecha

            segundos = diferencia.total_seconds()
            minutos = segundos / 60
            horas = minutos / 60
            dias = horas / 24

            if segundos < 60:
                return "Ahora"
            elif minutos < 60:
                return f"Hace {int(minutos)}m"
            elif horas < 24:
                return f"Hace {int(horas)}h"
            elif dias < 7:
                return f"Hace {int(dias)}d"
            else:
                # Formatear fecha corta
                return fecha.strftime("%d/%m/%Y")

        except Exception as e:
            logger.error(f"Error calculando tiempo relativo: {e}")
            return "Fecha inválida"

