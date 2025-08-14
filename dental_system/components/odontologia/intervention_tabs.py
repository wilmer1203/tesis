# 🦷 COMPONENTE: NAVEGACIÓN POR TABS PROFESIONAL PARA INTERVENCIÓN
# dental_system/components/odontologia/intervention_tabs.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS, ROLE_THEMES, dark_crystal_card

# ==========================================
# 🎨 ESTILOS ESPECÍFICOS PARA TABS ODONTOLÓGICOS
# ==========================================

# Colores específicos para odontólogos con tema cristalino
ODONTOLOGO_COLORS = {
    "primary": COLORS["success"]["500"],        # Verde profesional
    "secondary": COLORS["primary"]["500"],      # Turquesa dental  
    "accent": COLORS["primary"]["400"],         # Acento turquesa claro
    "surface": "rgba(255, 255, 255, 0.08)",   # Glassmorphism
    "border": "rgba(255, 255, 255, 0.2)"      # Bordes cristal
}

# Configuración de tabs
TAB_CONFIG = {
    "paciente": {
        "title": "📋 Información Paciente",
        "icon": "user-check", 
        "color": COLORS["info"]["500"],
        "description": "Datos médicos y alertas"
    },
    "odontograma": {
        "title": "🦷 Odontograma",
        "icon": "clipboard-list",
        "color": ODONTOLOGO_COLORS["primary"], 
        "description": "32 dientes FDI + condiciones"
    },
    "intervencion": {
        "title": "⚕️ Intervención", 
        "icon": "activity",
        "color": COLORS["warning"]["500"],
        "description": "Servicios y procedimientos"
    },
    "finalizar": {
        "title": "💾 Finalizar",
        "icon": "check-circle",
        "color": ODONTOLOGO_COLORS["accent"],
        "description": "Revisar y completar"
    }
}

# Estilos para tab navigation
TAB_HEADER_STYLE = {
    "background": "rgba(255, 255, 255, 0.06)",
    "backdrop_filter": "blur(25px) saturate(150%)",
    "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
    "border_radius": RADIUS["2xl"], 
    "box_shadow": SHADOWS["crystal_md"],
    "padding": SPACING["2"],
    "margin_bottom": SPACING["6"],
    "position": "relative",
    "overflow": "hidden"
}

TAB_BUTTON_BASE_STYLE = {
    "padding": f"{SPACING['3']} {SPACING['6']}",
    "border_radius": RADIUS["xl"],
    "transition": "all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
    "cursor": "pointer",
    "position": "relative",
    "border": "1px solid transparent",
    "backdrop_filter": "blur(10px)",
    "display": "flex",
    "align_items": "center",
    "gap": SPACING["3"],
    "min_width": "200px",
    "justify_content": "flex-start"
}

TAB_CONTENT_STYLE = {
    "background": "rgba(255, 255, 255, 0.05)", 
    "backdrop_filter": "blur(20px) saturate(180%)",
    "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
    "border_radius": RADIUS["3xl"],
    "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
    "padding": SPACING["8"],
    "min_height": "600px",
    "position": "relative",
    "overflow": "hidden"
}

PROGRESS_BAR_STYLE = {
    "height": "4px",
    "background": "rgba(255, 255, 255, 0.1)",
    "border_radius": RADIUS["full"],
    "overflow": "hidden",
    "margin_bottom": SPACING["4"]
}

# ==========================================
# 🎯 COMPONENTES DE TAB INDIVIDUAL
# ==========================================

def tab_button(tab_id: str, tab_config: dict, is_active: bool = False) -> rx.Component:
    """🎯 Botón individual de tab con efectos cristalinos"""
    
    # Estilos dinámicos según estado
    if is_active:
        button_style = {
            **TAB_BUTTON_BASE_STYLE,
            "background": f"linear-gradient(135deg, {tab_config['color']}40 0%, {tab_config['color']}20 100%)",
            "border": f"1px solid {tab_config['color']}60",
            "color": "white",
            "box_shadow": f"0 4px 12px {tab_config['color']}30, inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "transform": "translateY(-2px)",
            "_before": {
                "content": "''",
                "position": "absolute",
                "bottom": "0",
                "left": "0",
                "right": "0", 
                "height": "3px",
                "background": f"linear-gradient(90deg, transparent 0%, {tab_config['color']} 50%, transparent 100%)",
                "box_shadow": f"0 0 10px {tab_config['color']}80"
            }
        }
    else:
        button_style = {
            **TAB_BUTTON_BASE_STYLE,
            "background": "rgba(255, 255, 255, 0.03)",
            "color": DARK_THEME["colors"]["text_secondary"],
            "_hover": {
                "background": "rgba(255, 255, 255, 0.08)",
                "border": f"1px solid {tab_config['color']}30",
                "color": DARK_THEME["colors"]["text_primary"],
                "transform": "translateY(-1px)",
                "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.2)"
            }
        }
    
    return rx.box(
        # Contenido del botón
        rx.hstack(
            # Icono
            rx.icon(
                tag=tab_config["icon"],
                size=20,
                color=rx.cond(is_active, tab_config["color"], DARK_THEME["colors"]["text_secondary"])
            ),
            
            # Textos
            rx.vstack(
                rx.text(
                    tab_config["title"],
                    size="3",
                    weight="semibold"
                ),
                rx.text(
                    tab_config["description"],
                    size="1",
                    opacity="0.8"
                ),
                spacing="1",
                align_items="start"
            ),
            
            spacing="3",
            align_items="center",
            width="100%"
        ),
        
        style=button_style,
        on_click=AppState.set_active_intervention_tab(tab_id)
    )

def progress_indicator() -> rx.Component:
    """📊 Indicador de progreso entre tabs"""
    return rx.vstack(
        rx.text(
            f"Paso {AppState.tab_progress} de 4",
            size="2",
            color=DARK_THEME["colors"]["text_muted"],
            text_align="center"
        ),
        
        rx.box(
            rx.box(
                style={
                    "height": "100%",
                    "background": f"linear-gradient(90deg, {ODONTOLOGO_COLORS['primary']} 0%, {ODONTOLOGO_COLORS['accent']} 100%)",
                    "border_radius": RADIUS["full"],
                    "width": f"{AppState.tab_progress * 25}%",
                    "transition": "width 0.5s ease-in-out",
                    "box_shadow": f"0 0 10px {ODONTOLOGO_COLORS['primary']}40"
                }
            ),
            style=PROGRESS_BAR_STYLE
        ),
        
        spacing="2",
        width="100%"
    )

# ==========================================
# 🧭 NAVEGACIÓN PRINCIPAL DE TABS
# ==========================================

def tab_navigation_header() -> rx.Component:
    """🧭 Header de navegación con tabs horizontales"""
    return rx.box(
        rx.vstack(
            # Título principal
            rx.hstack(
                rx.icon(tag="activity", size=24, color=ODONTOLOGO_COLORS["primary"]),
                rx.text(
                    "Intervención Odontológica",
                    size="6",
                    weight="bold",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                spacing="3",
                align_items="center",
                justify_content="center",
                width="100%",
                margin_bottom="4"
            ),
            
            # Indicador de progreso
            progress_indicator(),
            
            # Tabs navegación
            rx.hstack(
                *[
                    tab_button(
                        tab_id=tab_id,
                        tab_config=tab_data,
                        is_active=AppState.active_intervention_tab == tab_id
                    )
                    for tab_id, tab_data in TAB_CONFIG.items()
                ],
                spacing="2",
                width="100%",
                justify_content="center",
                flex_wrap="wrap"  # Responsive para tablets
            ),
            
            spacing="4",
            width="100%"
        ),
        
        style=TAB_HEADER_STYLE
    )

def tab_navigation_footer() -> rx.Component:
    """🔄 Footer con botones de navegación rápida"""
    return rx.hstack(
        # Botón anterior
        rx.cond(
            AppState.tab_progress > 1,
            rx.button(
                rx.hstack(
                    rx.icon(tag="chevron-left", size=16),
                    rx.text("Anterior"),
                    spacing="2"
                ),
                on_click=AppState.previous_tab,
                style={
                    "background": "rgba(255, 255, 255, 0.1)",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
                    "border_radius": RADIUS["xl"],
                    "padding": f"{SPACING['2']} {SPACING['4']}",
                    "_hover": {
                        "background": "rgba(255, 255, 255, 0.15)"
                    }
                }
            ),
            rx.box()  # Spacer cuando no hay botón anterior
        ),
        
        rx.spacer(),
        
        # Estado actual
        rx.badge(
            f"Tab: {AppState.active_intervention_tab.title()}",
            color_scheme="blue",
            variant="soft",
            size="2"
        ),
        
        rx.spacer(),
        
        # Botón siguiente  
        rx.cond(
            AppState.tab_progress < 4,
            rx.button(
                rx.hstack(
                    rx.text("Siguiente"),
                    rx.icon(tag="chevron-right", size=16),
                    spacing="2"
                ),
                on_click=AppState.next_tab,
                style={
                    "background": f"linear-gradient(135deg, {ODONTOLOGO_COLORS['primary']} 0%, {ODONTOLOGO_COLORS['accent']} 100%)",
                    "color": "white", 
                    "border": "none",
                    "border_radius": RADIUS["xl"],
                    "padding": f"{SPACING['2']} {SPACING['4']}",
                    "box_shadow": f"0 4px 12px {ODONTOLOGO_COLORS['primary']}30",
                    "_hover": {
                        "transform": "translateY(-1px)",
                        "box_shadow": f"0 6px 16px {ODONTOLOGO_COLORS['primary']}40"
                    }
                }
            ),
            rx.box()  # Spacer cuando no hay botón siguiente
        ),
        
        spacing="4",
        width="100%",
        align_items="center",
        padding=f"{SPACING['4']} {SPACING['6']}",
        style={
            "background": "rgba(255, 255, 255, 0.03)",
            "backdrop_filter": "blur(20px)",
            "border_top": f"1px solid {ODONTOLOGO_COLORS['border']}",
            "border_radius": f"{RADIUS['none']} {RADIUS['none']} {RADIUS['3xl']} {RADIUS['3xl']}"
        }
    )

# ==========================================
# 📦 CONTENEDOR PRINCIPAL DE TABS
# ==========================================

def intervention_tabs_container() -> rx.Component:
    """🦷 Contenedor principal con sistema de tabs profesional"""
    return rx.vstack(
        # Header con navegación  
        tab_navigation_header(),
        
        # Contenido dinámico según tab activo
        rx.box(
            # El contenido se definirá externamente desde intervencion_page_v2.py
            # para mantener la separación de responsabilidades
            rx.box(
                id="tab-content-placeholder",
                # Este contenido será reemplazado por la página principal
                style={
                    "min_height": "400px",
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center"
                }
            ),
            
            style=TAB_CONTENT_STYLE
        ),
        
        # Footer con navegación
        tab_navigation_footer(),
        
        spacing="0",
        width="100%",
        max_width="1400px"
    )