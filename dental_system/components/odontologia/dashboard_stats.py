"""
🦷 COMPONENTE: ESTADÍSTICAS DEL DASHBOARD ODONTOLÓGICO
=====================================================

Componente especializado para mostrar estadísticas y métricas del día
para el dashboard principal del odontólogo.

Funcionalidades:
- Tarjetas de estadísticas con iconos
- Información de próxima consulta
- Alertas de pacientes urgentes
- Resumen de actividad del día
"""

import reflex as rx
from typing import Dict, Any
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS PARA ESTADÍSTICAS
# ==========================================

STAT_CARD_BASE_STYLE = {
    "padding": SPACING["4"],
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["sm"],
    "border": "1px solid",
    "min_height": "120px",
    "display": "flex",
    "flex_direction": "column",
    "justify_content": "center",
    "align_items": "center",
    "text_align": "center",
    "transition": "all 0.3s ease",
    "_hover": {
        "box_shadow": SHADOWS["lg"],
        "transform": "translateY(-2px)"
    }
}

STAT_CARD_PRIMARY_STYLE = {
    **STAT_CARD_BASE_STYLE,
    "background": COLORS["primary"]["50"],
    "border_color": COLORS["primary"]["200"],
    "color": COLORS["primary"]["800"],
}

STAT_CARD_SUCCESS_STYLE = {
    **STAT_CARD_BASE_STYLE,
    "background": COLORS["success"]["50"],
    "border_color": COLORS["success"]["200"], 
    "color": COLORS["success"]["800"],
}

STAT_CARD_WARNING_STYLE = {
    **STAT_CARD_BASE_STYLE,
    "background": COLORS["warning"]["50"],
    "border_color": COLORS["warning"]["200"],
    "color": COLORS["warning"]["800"],
}

STAT_CARD_INFO_STYLE = {
    **STAT_CARD_BASE_STYLE,
    "background": COLORS["blue"]["50"],
    "border_color": COLORS["blue"]["200"],
    "color": COLORS["blue"]["800"],
}

URGENT_ALERT_STYLE = {
    "background": COLORS["error"]["50"],
    "border": f"1px solid {COLORS['error']['200']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["4"],
}

# ==========================================
# 📊 COMPONENTES DE ESTADÍSTICAS
# ==========================================

def stat_card(titulo: str, valor: rx.Var, icono: str, estilo: Dict[str, Any]) -> rx.Component:
    """
    📊 Tarjeta individual de estadística con icono
    
    Args:
        titulo: Título de la estadística
        valor: Valor a mostrar (computed variable)
        icono: Icono emoji o nombre
        estilo: Estilo CSS de la tarjeta
    """
    return rx.box(
        rx.vstack(
            # Icono
            rx.text(
                icono,
                font_size="32px",
                margin_bottom="8px",
            ),
            
            # Valor principal
            rx.text(
                valor,
                font_size="32px",
                font_weight="bold",
                line_height="1",
            ),
            
            # Título
            rx.text(
                titulo,
                font_size="14px",
                font_weight="medium",
                opacity="0.8",
            ),
            
            spacing="2",
            align_items="center"
        ),
        style=estilo
    )

def dashboard_stats_grid() -> rx.Component:
    """📊 Grid principal de estadísticas del dashboard odontológico"""
    return rx.grid(
        # Pacientes Asignados
        stat_card(
            titulo="Pacientes Asignados",
            valor=AppState.estadisticas_odontologo_tiempo_real["pacientes_asignados"],
            icono="👥",
            estilo=STAT_CARD_PRIMARY_STYLE
        ),
        
        # Pacientes Disponibles
        stat_card(
            titulo="Disponibles",
            valor=AppState.estadisticas_odontologo_tiempo_real["pacientes_disponibles"],
            icono="🔄",
            estilo=STAT_CARD_SUCCESS_STYLE
        ),
        
        # Consultas En Progreso
        stat_card(
            titulo="En Atención",
            valor=AppState.estadisticas_odontologo_tiempo_real["consultas_en_progreso"],
            icono="🏥",
            estilo=STAT_CARD_WARNING_STYLE
        ),
        
        # Consultas Completadas
        stat_card(
            titulo="Completadas Hoy",
            valor=AppState.estadisticas_odontologo_tiempo_real["consultas_completadas"],
            icono="✅",
            estilo=STAT_CARD_SUCCESS_STYLE
        ),
        
        # Tiempo promedio
        stat_card(
            titulo="Tiempo Promedio",
            valor=f"{AppState.estadisticas_odontologo_tiempo_real.get('tiempo_promedio_minutos', 25)} min",
            icono="⏱️",
            estilo=STAT_CARD_INFO_STYLE
        ),
        
        # Próxima Consulta Info
        stat_card(
            titulo="En Cola",
            valor=AppState.estadisticas_odontologo_tiempo_real["consultas_programadas"],
            icono="⏳",
            estilo=STAT_CARD_PRIMARY_STYLE
        ),
        
        columns="3",
        gap="4",
        width="100%"
    )

def alerta_pacientes_urgentes() -> rx.Component:
    """🚨 Alerta para pacientes urgentes"""
    return rx.cond(
        AppState.alerta_pacientes_urgentes["tiene_urgentes"],
        rx.box(
            rx.hstack(
                rx.text(
                    "🚨",
                    font_size="24px",
                    color=COLORS["error"]["500"]
                ),
                rx.vstack(
                    rx.text(
                        "Atención: Pacientes Urgentes",
                        font_weight="bold",
                        font_size="16px",
                        color=COLORS["error"]["700"]
                    ),
                    rx.text(
                        AppState.alerta_pacientes_urgentes["mensaje"],
                        font_size="14px",
                        color=COLORS["error"]["600"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                rx.spacer(),
                rx.button(
                    "Ver Urgentes",
                    size="2",
                    variant="outline",
                    color_scheme="red",
                    # on_click=AppState.filtrar_solo_urgentes
                ),
                spacing="3",
                align_items="center",
                width="100%"
            ),
            style=URGENT_ALERT_STYLE
        )
    )

def proxima_consulta_info() -> rx.Component:
    """📅 Información de la próxima consulta"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "📅",
                    font_size="20px"
                ),
                rx.text(
                    "Próxima Consulta",
                    font_weight="bold",
                    font_size="16px",
                    color=COLORS["gray"]["700"]
                ),
                spacing="2",
                align_items="center"
            ),
            
            rx.cond(
                AppState.proxima_consulta_info["tiene_proxima"] == "true",
                rx.vstack(
                    rx.text(
                        AppState.proxima_consulta_info["paciente"],
                        font_weight="medium",
                        font_size="15px",
                        color=COLORS["gray"]["800"]
                    ),
                    rx.hstack(
                        rx.text(
                            f"⏱️ {AppState.proxima_consulta_info['tiempo_estimado']}",
                            font_size="14px",
                            color=COLORS["gray"]["600"]
                        ),
                        rx.cond(
                            AppState.proxima_consulta_info["prioridad"] == "urgente",
                            rx.badge(
                                "URGENTE",
                                color_scheme="red",
                                size="2"
                            )
                        ),
                        spacing="3",
                        align_items="center"
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                rx.text(
                    AppState.proxima_consulta_info["paciente"],
                    font_style="italic",
                    color=COLORS["gray"]["500"],
                    font_size="14px"
                )
            ),
            
            spacing="3",
            align_items="start",
            width="100%"
        ),
        background=COLORS["gray"]["50"],
        border=f"1px solid {COLORS['gray']['200']}",
        border_radius=RADIUS["lg"],
        padding=SPACING["4"],
        margin_top=SPACING["4"]
    )

def resumen_actividad() -> rx.Component:
    """📋 Resumen de actividad del día"""
    return rx.box(
        rx.hstack(
            rx.text(
                "📋",
                font_size="20px"
            ),
            rx.vstack(
                rx.text(
                    "Resumen del Día",
                    font_weight="bold",
                    font_size="16px",
                    color=COLORS["gray"]["700"]
                ),
                rx.text(
                    AppState.resumen_actividad_dia,
                    font_size="14px",
                    color=COLORS["gray"]["600"]
                ),
                spacing="1",
                align_items="start"
            ),
            spacing="3",
            align_items="center",
            width="100%"
        ),
        background="white",
        border=f"1px solid {COLORS['gray']['200']}",
        border_radius=RADIUS["lg"],
        padding=SPACING["3"],
        margin_top=SPACING["3"]
    )

def acciones_rapidas() -> rx.Component:
    """⚡ Botones de acciones rápidas"""
    return rx.hstack(
        rx.button(
            "🔄 Actualizar Datos",
            size="2",
            variant="outline",
            on_click=[
                AppState.cargar_pacientes_asignados,
                AppState.cargar_consultas_disponibles_otros,
                AppState.cargar_estadisticas_dia
            ]
        ),
        
        rx.cond(
            AppState.puede_tomar_mas_pacientes,
            rx.button(
                "➕ Ver Disponibles",
                size="2",
                color_scheme="green",
                # on_click=AppState.enfocar_pacientes_disponibles
            )
        ),
        
        rx.cond(
            AppState.tiene_pacientes_para_atender,
            rx.button(
                "🏥 Ir a Atención",
                size="2",
                color_scheme="blue",
                # on_click=AppState.ir_a_primera_consulta_programada
            )
        ),
        
        spacing="3",
        justify_content="center",
        width="100%",
        margin_top=SPACING["4"]
    )
