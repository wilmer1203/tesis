# 🦷 PÁGINA DE INTERVENCIÓN - VERSIÓN SIMPLE Y ELEGANTE
import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
from dental_system.components.odontologia.intervention_tabs_v2 import intervention_tabs_integrated
from dental_system.styles.themes import COLORS, RADIUS, SPACING

# ========================================
# ESTILOS SIMPLES Y LIMPIOS
# ========================================

PAGE_STYLE = {
    "min_height": "100vh",
    "background": f"linear-gradient(135deg, {COLORS['primary']['50']} 0%, white 100%)",
    "padding": SPACING["4"]
}

HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "color": "white",
    "padding": SPACING["4"],
    "border_radius": RADIUS["lg"],
    "margin_bottom": SPACING["4"],
    "box_shadow": "0 4px 12px rgba(0,0,0,0.15)"
}

CONTENT_STYLE = {
    "display": "grid",
    "grid_template_columns": "300px 1fr",
    "gap": SPACING["4"],
    "height": "calc(100vh - 200px)"
}

PANEL_STYLE = {
    "background": "white",
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["lg"],
    "box_shadow": "0 2px 8px rgba(0,0,0,0.1)",
    "overflow": "hidden"
}

# ========================================
# COMPONENTES SIMPLES
# ========================================

def header_simple():
    return rx.box(
        rx.hstack(
            rx.button(
                "← Volver",
                on_click=lambda: AppState.navigate_to("odontologia"),
                variant="ghost",
                color="white"
            ),
            rx.heading("🦷 Intervención Odontológica", size="6", color="white"),
            rx.spacer(),
            rx.text("Sesión Activa", color="white", opacity="0.9"),
            justify="between",
            align="center",
            width="100%"
        ),
        style=HEADER_STYLE
    )

def botones_accion_simple():
    return rx.hstack(
        rx.button("Guardar", color_scheme="blue"),
        rx.button("Cancelar", color_scheme="red", variant="outline"),
        rx.button("Finalizar", color_scheme="green"),
        spacing="2",
        style={
            "position": "fixed",
            "top": SPACING["4"],
            "right": SPACING["4"],
            "z_index": "999"
        }
    )

def intervencion_page_simple():
    """Página de intervención simple y funcional"""
    return rx.box(
        header_simple(),
        botones_accion_simple(),
        
        rx.box(
            # Panel del paciente
            rx.box(
                panel_informacion_paciente(),
                style=PANEL_STYLE
            ),
            
            # Panel central
            rx.box(
                intervention_tabs_integrated(),
                style=PANEL_STYLE
            ),
            
            style=CONTENT_STYLE
        ),
        
        style=PAGE_STYLE,
        on_mount=[
            AppState.cargar_servicios_disponibles,
            AppState.cargar_estadisticas_dia
        ]
    )