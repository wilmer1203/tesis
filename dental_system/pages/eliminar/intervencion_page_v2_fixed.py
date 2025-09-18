"""
🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA V2 - ESTILO PROFESIONAL
============================================================

Inspirada en consultas_page_v41.py con tema oscuro médico profesional.
- Layout limpio y funcional
- Colores consistentes con el sistema
- Sin efectos complejos que causen errores
- Focus en funcionalidad médica
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, primary_button, secondary_button
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
from dental_system.components.odontologia.intervention_tabs_v2 import intervention_tabs_integrated
from dental_system.styles.themes import COLORS, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 TEMA MÉDICO PROFESIONAL (BASADO EN CONSULTAS)
# ==========================================

MEDICAL_COLORS = {
    "background": COLORS["gray"]["50"],      # Fondo claro profesional
    "surface": "white",                     # Surface de cards
    "surface_hover": COLORS["gray"]["25"],   # Surface al hover
    "border": COLORS["gray"]["200"],         # Bordes sutiles
    "text_primary": COLORS["gray"]["900"],   # Texto principal
    "text_secondary": COLORS["gray"]["600"], # Texto secundario
    "accent_primary": COLORS["primary"]["500"], # Turquesa principal
    "accent_success": COLORS["success"]["500"], # Verde éxito
}

# ==========================================
# 📱 ESTILOS DEL LAYOUT PRINCIPAL
# ==========================================

PAGE_LAYOUT_STYLE = {
    "min_height": "100vh",
    "background": MEDICAL_COLORS["background"],
    "padding": SPACING["4"]
}

HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "color": "white",
    "padding": SPACING["4"],
    "border_radius": RADIUS["lg"],
    "margin_bottom": SPACING["4"],
    "box_shadow": SHADOWS["lg"]
}

CONTENT_GRID_STYLE = {
    "display": "grid",
    "grid_template_columns": "320px 1fr",
    "gap": SPACING["4"],
    "height": "calc(100vh - 180px)",
    "@media (max-width: 1024px)": {
        "grid_template_columns": "1fr",
        "height": "auto"
    }
}

PANEL_BASE_STYLE = {
    "background": MEDICAL_COLORS["surface"],
    "border": f"1px solid {MEDICAL_COLORS['border']}",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["md"],
    "overflow": "hidden"
}

# ==========================================
# 🧩 COMPONENTES SIMPLES
# ==========================================

def header_intervencion() -> rx.Component:
    """Header simple y profesional"""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.button(
                    "← Volver",
                    on_click=lambda: AppState.navigate_to("odontologia"),
                    variant="ghost",
                    color="white"
                ),
                rx.heading("🦷 Intervención Odontológica", size="6", color="white"),
                spacing="4",
                align="center"
            ),
            rx.spacer(),
            rx.text("Sesión Activa", color="white", opacity="0.9"),
            justify="between",
            align="center",
            width="100%"
        ),
        style=HEADER_STYLE
    )

def botones_accion() -> rx.Component:
    """Botones de acción flotantes"""
    return rx.hstack(
        rx.button("💾 Guardar", color_scheme="blue", variant="outline"),
        rx.button("❌ Cancelar", color_scheme="red", variant="outline"),
        rx.button("✅ Finalizar", color_scheme="green"),
        spacing="2",
        style={
            "position": "fixed",
            "top": SPACING["4"],
            "right": SPACING["4"],
            "z_index": "999",
            "padding": SPACING["2"],
            "background": "white",
            "border_radius": RADIUS["lg"],
            "box_shadow": SHADOWS["lg"]
        }
    )

def panel_paciente_wrapper() -> rx.Component:
    """Panel del paciente con estilo consistente"""
    return rx.box(
        panel_informacion_paciente(),
        style=PANEL_BASE_STYLE
    )

def panel_central_wrapper() -> rx.Component:
    """Panel central con tabs de intervención"""
    return rx.box(
        intervention_tabs_integrated(),
        style=PANEL_BASE_STYLE
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL
# ==========================================

def intervencion_page_v2() -> rx.Component:
    """
    🦷 Página de intervención odontológica - Versión profesional limpia
    
    Características:
    - Layout grid responsive
    - Tema médico consistente
    - Colores del sistema (COLORS)
    - Sin efectos complejos
    - Funcionalidad completa preservada
    """
    return rx.box(
        # Header principal
        header_intervencion(),
        
        # Botones de acción flotantes
        botones_accion(),
        
        # Contenido principal en grid
        rx.box(
            panel_paciente_wrapper(),
            panel_central_wrapper(),
            style=CONTENT_GRID_STYLE
        ),
        
        style=PAGE_LAYOUT_STYLE,
        
        # Eventos de inicialización
        on_mount=[
            AppState.cargar_servicios_disponibles,
            AppState.cargar_historial_paciente(AppState.paciente_actual.id),
            AppState.cargar_estadisticas_dia
        ]
    )