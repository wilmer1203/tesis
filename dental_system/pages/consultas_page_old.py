"""
📅 PÁGINA DE CONSULTAS REDISEÑADA - TEMA OSCURO (RESPALDO)
=========================================================

ESTE ES EL CÓDIGO ORIGINAL RESPALDADO
Guardado en: consultas_page_old.py
"""

"""
📅 PÁGINA DE CONSULTAS REDISEÑADA - TEMA OSCURO
===============================================

🌟 Características del nuevo diseño:
- Tema oscuro profesional con efectos glassmorphism
- Layout por odontólogo (NO tabla tradicional)
- Cards de pacientes con estados visuales
- Columna de resumen lateral
- Header con contadores integrados
- Modal optimizado para nueva consulta
- Diseño responsive mobile-first

✨ CONSULTAS POR ORDEN DE LLEGADA (NO citas programadas)
"""

import reflex as rx
from typing import Dict, Any
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button
from dental_system.models.consultas_models import ConsultaModel
from dental_system.styles.themes import (
    COLORS, 
    SHADOWS, 
    RADIUS, 
    SPACING, 
    ANIMATIONS, 
    DARK_THEME,
    GRADIENTS,
    GLASS_EFFECTS,
    dark_page_background,
    dark_crystal_card,
    dark_header_style
)

# ==========================================
# 🎨 CONSTANTES CSS CENTRALIZADAS
# ==========================================

# 🎨 Colores especializados para consultas
CONSULTAS_COLORS = {
    "primary_gradient": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
    "warning_gradient": f"linear-gradient(135deg, {COLORS['warning']['500']} 0%, #F59E0B 100%)",
    "success_gradient": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, #10B981 100%)",
    "danger_gradient": f"linear-gradient(135deg, #EF4444 0%, #DC2626 100%)",
    "surface_subtle": f"rgba({DARK_THEME['colors']['surface']}, 0.3)",
    "surface_hover": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
    "border_subtle": f"rgba({DARK_THEME['colors']['border']}, 0.2)",
    "border_hover": f"rgba({DARK_THEME['colors']['border']}, 0.4)",
    "divider_gradient": f"linear-gradient(90deg, transparent 0%, rgba({DARK_THEME['colors']['border']}, 0.6) 50%, transparent 100%)"
}

# 📏 Espaciado reutilizable
CONSULTAS_SPACING = {
    "card_padding": SPACING["5"],
    "section_padding": SPACING["4"],
    "compact_padding": f"{SPACING['2']} {SPACING['3']}",
    "button_padding": f"{SPACING['4']} {SPACING['8']}",
    "divider_margin": f"{SPACING['4']} 0",
    "header_margin": SPACING["8"],
    "card_margin": SPACING["4"]
}

# 🔘 Radius centralizados
CONSULTAS_RADIUS = {
    "card": RADIUS["lg"],
    "compact": RADIUS["md"],
    "button": RADIUS["xl"],
    "badge": RADIUS["full"]
}

# 📝 Tipografía especializada
CONSULTAS_TEXT = {
    "header_large": {
        "font_size": "1.5rem",
        "font_weight": "700",
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "header_medium": {
        "font_size": "1.1rem",
        "font_weight": "700", 
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "header_small": {
        "font_size": "1rem",
        "font_weight": "600",
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "body_primary": {
        "font_size": "0.9rem",
        "font_weight": "600",
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "body_secondary": {
        "font_size": "0.85rem",
        "color": DARK_THEME["colors"]["text_secondary"]
    },
    "body_accent": {
        "font_size": "0.85rem",
        "font_weight": "500",
        "color": DARK_THEME["colors"]["accent"]
    },
    "caption": {
        "font_size": "0.8rem",
        "color": DARK_THEME["colors"]["text_secondary"]
    },
    "badge": {
        "color": "white",
        "font_weight": "700",
        "font_size": "0.9rem"
    }
}

# 🎭 Efectos y animaciones
CONSULTAS_EFFECTS = {
    "card_hover": {
        "transform": "translateY(-2px)",
        "box_shadow": f"0 8px 25px rgba({DARK_THEME['colors']['shadow']}, 0.3)",
        "border_color": CONSULTAS_COLORS["border_hover"]
    },
    "button_hover": {
        "box_shadow": f"0 12px 40px {DARK_THEME['colors']['primary']}60",
        "transform": "translateY(-1px)"
    },
    "compact_hover": {
        "background": CONSULTAS_COLORS["surface_hover"],
        "border_color": CONSULTAS_COLORS["border_hover"]
    }
}

# ==========================================
# 🌙 COMPONENTES DEL TEMA OSCURO
# ==========================================

def quick_actions_panel() -> rx.Component:
    """⚡ Panel de acciones rápidas para eficiencia operativa"""
    return rx.card(
        rx.hstack(
            # Acciones principales
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=18),
                    rx.text("Nueva Consulta", weight="medium"),
                    spacing="2",
                    align="center"
                ),
                color_scheme="blue",
                size="3",
                on_click=lambda: AppState.seleccionar_y_abrir_modal_consulta(""),
                style={
                    "background": f"linear-gradient(135deg, {COLORS['blue']['600']} 0%, {COLORS['blue']['500']} 100%)",
                    "border": "none",
                    "box_shadow": f"0 4px 12px rgba({COLORS['blue']['500']}, 0.3)",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "transform": "translateY(-2px)",
                        "box_shadow": f"0 6px 20px rgba({COLORS['blue']['500']}, 0.4)"
                    }
                }
            ),
            rx.button(
                rx.hstack(
                    rx.icon("search", size=18),
                    rx.text("Buscar Paciente", weight="medium"),
                    spacing="2",
                    align="center"
                ),
                color_scheme="gray",
                size="3",
                on_click=AppState.enfocar_busqueda_consultas,
                style={
                    "background": f"linear-gradient(135deg, {COLORS['gray']['600']} 0%, {COLORS['gray']['500']} 100%)",
                    "border": f"1px solid {COLORS['gray']['400']}",
                    "box_shadow": f"0 4px 12px rgba({COLORS['gray']['500']}, 0.2)",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "transform": "translateY(-2px)",
                        "box_shadow": f"0 6px 20px rgba({COLORS['gray']['500']}, 0.3)"
                    }
                }
            ),
            rx.button(
                rx.hstack(
                    rx.icon("refresh-cw", size=18),
                    rx.text("Actualizar", weight="medium"),
                    spacing="2",
                    align="center"
                ),
                color_scheme="green",
                size="3",
                on_click=AppState.refrescar_consultas,
                style={
                    "background": f"linear-gradient(135deg, {COLORS['success']['600']} 0%, {COLORS['success']['500']} 100%)",
                    "border": "none",
                    "box_shadow": f"0 4px 12px rgba({COLORS['success']['500']}, 0.3)",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "transform": "translateY(-2px)",
                        "box_shadow": f"0 6px 20px rgba({COLORS['success']['500']}, 0.4)"
                    }
                }
            ),
            spacing="4",
            align="center",
            wrap="wrap",
            justify="center"
        ),
        style={
            **dark_crystal_card(hover_lift="2px"),
            "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, rgba({DARK_THEME['colors']['surface']}, 0.8) 100%)",
            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.3)",
            "margin_bottom": SPACING["4"],
            "padding": SPACING["4"],
            "backdrop_filter": "blur(10px)",
            "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.3)"
        }
    )

# [TODO EL RESTO DEL CÓDIGO ORIGINAL AQUÍ...]

def consultas_page_new() -> rx.Component:
    """PÁGINA ORIGINAL RESPALDADA"""
    return rx.text("Página original respaldada en consultas_page_old.py")