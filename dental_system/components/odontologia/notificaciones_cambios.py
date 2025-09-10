"""
🔔 COMPONENTE: SISTEMA DE NOTIFICACIONES DE CAMBIOS
===================================================

Sistema inteligente de notificaciones para cambios en odontograma con:
- Notificaciones en tiempo real
- Centro de notificaciones centralizado
- Alertas automáticas por cambios críticos
- Sistema de escalamiento
- Configuración personalizable por usuario

CARACTERÍSTICAS:
- Notificaciones toast en tiempo real
- Centro de notificaciones con histórico
- Filtros por prioridad y tipo
- Configuraciones de usuario personalizables
- Integración con alertas médicas
- Sistema de recordatorios automáticos
"""

import reflex as rx
from typing import Dict, List, Optional
from datetime import datetime, date, timedelta
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS DE NOTIFICACIONES
# ==========================================

NOTIFICACIONES_PANEL_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["md"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "max_height": "500px",
    "min_width": "350px",
    "overflow": "hidden"
}

TOAST_NOTIFICATION_STYLE = {
    "position": "fixed",
    "top": "20px",
    "right": "20px",
    "z_index": "1000",
    "min_width": "300px",
    "max_width": "400px",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["lg"],
    "border_left": "4px solid"
}

NOTIFICATION_ITEM_STYLE = {
    "padding": SPACING["3"],
    "border_bottom": f"1px solid {COLORS['gray']['100']}",
    "transition": "all 0.2s ease",
    "_hover": {
        "background": COLORS['gray']['50']
    }
}

# ==========================================
# 📢 NOTIFICACIONES TOAST EN TIEMPO REAL
# ==========================================

def toast_notification() -> rx.Component:
    """🍞 Notificación toast en tiempo real"""
    return rx.cond(
        AppState.notificacion_toast_visible,
        rx.box(
            rx.card(
                rx.vstack(
                    # Header de la notificación
                    rx.hstack(
                        rx.icon(
                            AppState.notificacion_toast_icono,
                            size=20,
                            color=f"{AppState.notificacion_toast_color}.500"
                        ),
                        rx.vstack(
                            rx.text(
                                AppState.notificacion_toast_titulo,
                                weight="bold",
                                size="3",
                                color=f"{AppState.notificacion_toast_color}.700"
                            ),
                            rx.text(
                                AppState.notificacion_toast_timestamp,
                                size="1",
                                color="gray.500"
                            ),
                            align_items="start",
                            spacing="0"
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=16),
                            size="1",
                            variant="ghost",
                            on_click=AppState.cerrar_toast_notification
                        ),
                        spacing="3",
                        align_items="start",
                        width="100%"
                    ),
                    
                    # Contenido de la notificación
                    rx.text(
                        AppState.notificacion_toast_mensaje,
                        size="2",
                        color="gray.700"
                    ),
                    
                    # Botones de acción (condicional)
                    rx.cond(
                        AppState.notificacion_toast_tiene_acciones,
                        rx.hstack(
                            rx.button(
                                "Ver Detalles",
                                size="2",
                                variant="outline",
                                on_click=AppState.ver_detalles_notificacion
                            ),
                            rx.button(
                                "Marcar como Leída",
                                size="2",
                                color_scheme=AppState.notificacion_toast_color,
                                on_click=AppState.marcar_notificacion_leida
                            ),
                            spacing="2"
                        ),
                        rx.box()
                    ),
                    
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                style={
                    **TOAST_NOTIFICATION_STYLE,
                    "border_left_color": f"{COLORS["blue"]['500']}"
                }
            ),
            # Auto-hide después de 5 segundos
            id="toast-notification"
        ),
        rx.box()
    )

# ==========================================
# 🔔 CENTRO DE NOTIFICACIONES
# ==========================================

def centro_notificaciones() -> rx.Component:
    """📱 Panel central de todas las notificaciones"""
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("bell", size=18),
                    rx.cond(
                        AppState.total_notificaciones_no_leidas > 0,
                        rx.badge(
                            AppState.total_notificaciones_no_leidas,
                            color_scheme="red",
                            size="1",
                            variant="solid"
                        ),
                        rx.box()
                    ),
                    spacing="1",
                    align_items="center"
                ),
                variant="ghost",
                size="2"
            )
        ),
        rx.popover.content(
            rx.vstack(
                # Header del centro
                rx.hstack(
                    rx.text("🔔 Notificaciones", weight="bold", size="4"),
                    rx.spacer(),
                    rx.hstack(
                        rx.button(
                            "Marcar todas",
                            size="1",
                            variant="ghost",
                            on_click=AppState.marcar_todas_notificaciones_leidas
                        ),
                        rx.button(
                            rx.icon("settings", size=14),
                            size="1",
                            variant="ghost",
                            on_click=AppState.abrir_configuracion_notificaciones
                        ),
                        spacing="1"
                    ),
                    width="100%",
                    align_items="center",
                    padding_bottom="2",
                    border_bottom=f"1px solid {COLORS['gray']['200']}"
                ),
                
                # Filtros rápidos
                rx.hstack(
                    filtro_notificacion("Todas", "todas"),
                    filtro_notificacion("Críticas", "criticas"),
                    filtro_notificacion("Recordatorios", "recordatorios"),
                    filtro_notificacion("Cambios", "cambios"),
                    spacing="1",
                    width="100%",
                    padding_y="2"
                ),
                
                # Lista de notificaciones
                rx.box(
                    rx.cond(
                        AppState.notificaciones_filtradas_count > 0,
                        rx.vstack(
                            # Notificaciones no leídas
                            rx.cond(
                                AppState.hay_notificaciones_no_leidas,
                                rx.vstack(
                                    rx.text("🔴 No Leídas", weight="medium", size="2", color="red.600"),
                                    item_notificacion(
                                        "Cambio Crítico Detectado",
                                        "Diente 16: Estado cambió de Sano a Caries Profunda",
                                        "hace 5 min",
                                        "circle_alert",
                                        "red",
                                        False,
                                        {"diente": "16", "tipo": "cambio_critico"}
                                    ),
                                    item_notificacion(
                                        "Recordatorio Vencido",
                                        "Control post-operatorio del diente 21 está vencido",
                                        "hace 2 horas",
                                        "clock",
                                        "orange",
                                        False,
                                        {"diente": "21", "tipo": "recordatorio_vencido"}
                                    ),
                                    spacing="0",
                                    width="100%"
                                ),
                                rx.box()
                            ),
                            
                            # Notificaciones leídas recientes
                            rx.vstack(
                                rx.text("📋 Recientes", weight="medium", size="2", color="gray.600"),
                                item_notificacion(
                                    "Nueva Versión Creada",
                                    "Odontograma actualizado a v2.1 por Dr. García",
                                    "hace 1 hora",
                                    "git_branch",
                                    "blue",
                                    True,
                                    {"version": "2.1", "tipo": "nueva_version"}
                                ),
                                item_notificacion(
                                    "Intervención Completada",
                                    "Obturación exitosa en diente 16",
                                    "hace 3 horas",
                                    "circle_check",
                                    "green",
                                    True,
                                    {"diente": "16", "tipo": "intervencion_completada"}
                                ),
                                spacing="0",
                                width="100%"
                            ),
                            
                            spacing="3",
                            width="100%"
                        ),
                        # Estado vacío
                        rx.vstack(
                            rx.icon("bell_off", size=32, color="gray.400"),
                            rx.text("No hay notificaciones", color="gray.500"),
                            align_items="center",
                            padding="4",
                            spacing="2"
                        )
                    ),
                    width="100%",
                    max_height="300px",
                    overflow_y="auto"
                ),
                
                # Footer con acciones
                rx.hstack(
                    rx.button(
                        "Ver Todas",
                        size="2",
                        variant="outline",
                        width="100%",
                        on_click=AppState.abrir_panel_completo_notificaciones
                    ),
                    width="100%",
                    padding_top="2",
                    border_top=f"1px solid {COLORS['gray']['200']}"
                ),
                
                spacing="2",
                width="100%"
            ),
            style=NOTIFICACIONES_PANEL_STYLE,
            side="bottom",
            align="end"
        )
    )

def filtro_notificacion(label: str, valor: str) -> rx.Component:
    """🏷️ Filtro rápido de notificaciones"""
    return rx.button(
        label,
        size="1",
        variant=rx.cond(
            AppState.filtro_notificaciones == valor,
            "solid",
            "outline"
        ),
        color_scheme=rx.cond(
            AppState.filtro_notificaciones == valor,
            "blue",
            "gray"
        ),
        on_click=lambda: AppState.aplicar_filtro_notificaciones(valor)
    )

def item_notificacion(
    titulo: str,
    mensaje: str,
    tiempo: str,
    icono: str,
    color: str,
    leida: bool,
    metadata: Dict[str, str]
) -> rx.Component:
    """📬 Item individual de notificación"""
    return rx.box(
        rx.hstack(
            # Indicador de no leída
            rx.cond(
                not leida,
                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="50%",
                    background=f"{color}.500"
                ),
                rx.box(width="8px")
            ),
            
            # Icono de la notificación
            rx.icon(icono, size=16, color=f"{color}.500"),
            
            # Contenido
            rx.vstack(
                rx.text(titulo, weight="bold" if not leida else "medium", size="2"),
                rx.text(mensaje, size="1", color="gray.600"),
                rx.text(tiempo, size="1", color="gray.400"),
                align_items="start",
                spacing="0",
                width="100%"
            ),
            
            # Botón de acción
            rx.button(
                rx.icon("chevron_right", size=14),
                size="1",
                variant="ghost",
                on_click=lambda: AppState.abrir_detalle_notificacion(metadata)
            ),
            
            spacing="2",
            align_items="start",
            width="100%"
        ),
        style={
            **NOTIFICATION_ITEM_STYLE,
            "background": COLORS['blue']['25'] if not leida else "transparent"
        },
        on_click=lambda: AppState.marcar_notificacion_individual_leida(titulo)
    )

# ==========================================
# ⚙️ CONFIGURACIÓN DE NOTIFICACIONES
# ==========================================

def modal_configuracion_notificaciones() -> rx.Component:
    """⚙️ Modal para configurar preferencias de notificaciones"""
    return rx.dialog.root(
        rx.dialog.trigger(rx.box()),  # Trigger invisible
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("settings", size=24, color="blue.500"),
                    rx.text("Configuración de Notificaciones", weight="bold", size="5"),
                    spacing="3",
                    align_items="center",
                    width="100%",
                    margin_bottom="4"
                ),
                
                # Configuraciones por categoría
                rx.vstack(
                    # Notificaciones de cambios críticos
                    config_categoria(
                        "🚨 Cambios Críticos",
                        "Notificar cambios importantes en el estado dental",
                        AppState.config_notif_cambios_criticos,
                        "config_notif_cambios_criticos"
                    ),
                    
                    # Recordatorios
                    config_categoria(
                        "⏰ Recordatorios",
                        "Alertas de seguimiento y citas programadas",
                        AppState.config_notif_recordatorios,
                        "config_notif_recordatorios"
                    ),
                    
                    # Nuevas versiones
                    config_categoria(
                        "📋 Nuevas Versiones",
                        "Notificar cuando se crea una nueva versión del odontograma",
                        AppState.config_notif_nuevas_versiones,
                        "config_notif_nuevas_versiones"
                    ),
                    
                    # Intervenciones completadas
                    config_categoria(
                        "✅ Intervenciones",
                        "Confirmación de procedimientos completados",
                        AppState.config_notif_intervenciones,
                        "config_notif_intervenciones"
                    ),
                    
                    spacing="3",
                    width="100%"
                ),
                
                # Configuración de sonido
                rx.divider(),
                rx.vstack(
                    rx.text("🔊 Configuración de Sonido", weight="bold", size="3"),
                    rx.hstack(
                        rx.switch(
                            checked=AppState.config_sonido_notificaciones,
                            on_change=AppState.toggle_sonido_notificaciones
                        ),
                        rx.text("Habilitar sonidos de notificación", size="2"),
                        spacing="2",
                        align_items="center"
                    ),
                    align_items="start",
                    width="100%"
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="outline",
                        on_click=AppState.cerrar_config_notificaciones
                    ),
                    rx.button(
                        "Guardar",
                        color_scheme="blue",
                        on_click=AppState.guardar_config_notificaciones
                    ),
                    spacing="2",
                    justify="end",
                    width="100%",
                    margin_top="4"
                ),
                
                spacing="3",
                width="100%"
            ),
            max_width="500px",
            width="90vw"
        ),
        open=AppState.modal_config_notificaciones_abierto
    )

def config_categoria(
    titulo: str,
    descripcion: str,
    valor_actual: bool,
    campo_config: str
) -> rx.Component:
    """⚙️ Configuración por categoría de notificación"""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(titulo, weight="bold", size="3"),
                rx.text(descripcion, size="2", color="gray.600"),
                align_items="start",
                spacing="1"
            ),
            rx.spacer(),
            rx.switch(
                checked=valor_actual,
                on_change=lambda checked: AppState.actualizar_config_notificacion(campo_config, checked)
            ),
            spacing="3",
            align_items="start",
            width="100%"
        ),
        size="2",
        width="100%"
    )

# ==========================================
# 🚨 ALERTAS AUTOMÁTICAS POR CAMBIOS
# ==========================================

def sistema_alertas_automaticas() -> rx.Component:
    """🚨 Sistema de alertas automáticas basado en reglas"""
    return rx.vstack(
        rx.text("🚨 Sistema de Alertas Automáticas", weight="bold", size="4"),
        
        # Reglas de alertas activas
        rx.vstack(
            regla_alerta(
                "Cambio de Estado Crítico",
                "Alerta cuando un diente cambia de 'Sano' a cualquier condición problemática",
                True,
                "critica"
            ),
            regla_alerta(
                "Recordatorios Vencidos",
                "Notificar cuando un recordatorio de seguimiento se vence",
                True,
                "recordatorio"
            ),
            regla_alerta(
                "Múltiples Cambios por Día",
                "Alerta si se hacen más de 5 cambios en un día en el mismo diente",
                False,
                "frecuencia"
            ),
            regla_alerta(
                "Intervención Compleja",
                "Notificar cuando se planifica una intervención de alta complejidad",
                True,
                "complejidad"
            ),
            spacing="2",
            width="100%"
        ),
        
        spacing="3",
        width="100%"
    )

def regla_alerta(titulo: str, descripcion: str, activa: bool, tipo: str) -> rx.Component:
    """📋 Configuración de regla de alerta"""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(titulo, weight="bold", size="2"),
                rx.text(descripcion, size="1", color="gray.600"),
                align_items="start",
                spacing="1"
            ),
            rx.spacer(),
            rx.switch(
                checked=activa,
                on_change=lambda checked: AppState.actualizar_regla_alerta(tipo, checked)
            ),
            spacing="3",
            align_items="center",
            width="100%"
        ),
        size="1",
        width="100%"
    )

# ==========================================
# 🔔 COMPONENTE PRINCIPAL NOTIFICACIONES
# ==========================================

def sistema_notificaciones_cambios() -> rx.Component:
    """
    🔔 Sistema completo de notificaciones de cambios
    
    FUNCIONALIDADES:
    - Notificaciones toast en tiempo real
    - Centro de notificaciones centralizado
    - Configuración personalizable
    - Alertas automáticas por reglas
    - Filtros y organización inteligente
    """
    
    return rx.fragment(
        # Notificación toast flotante
        toast_notification(),
        
        # Centro de notificaciones (en navbar)
        centro_notificaciones(),
        
        # Modal de configuración
        modal_configuracion_notificaciones(),
        
        # Sistema de alertas (para configuración avanzada)
        # sistema_alertas_automaticas()  # Comentado para no mostrar siempre
    )