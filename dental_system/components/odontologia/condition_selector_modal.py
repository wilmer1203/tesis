# 🦷 COMPONENTE: MODAL SELECTOR DE CONDICIONES DENTALES
# dental_system/components/odontologia/condition_selector_modal.py

import reflex as rx
from typing import Dict, List, Optional
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.interactive_tooth import (
    CONDITION_COLORS, CONDITION_NAMES, CONDITION_CATEGORIES,
    get_condition_color, get_condition_name
)
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS DEL MODAL
# ==========================================

MODAL_OVERLAY_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "width": "100vw",
    "height": "100vh",
    "background": "rgba(0, 0, 0, 0.7)",
    "backdrop_filter": "blur(8px)",
    "z_index": "1000",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center"
}

MODAL_CONTAINER_STYLE = {
    "background": DARK_THEME["colors"]["surface_elevated"],
    "border": f"2px solid {COLORS['primary']['500']}",
    "border_radius": RADIUS["2xl"],
    "box_shadow": "0 25px 60px rgba(0, 0, 0, 0.5)",
    "width": "90%",
    "max_width": "800px",
    "max_height": "80vh",
    "overflow": "hidden"
}

MODAL_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['600']} 0%, {COLORS['primary']['500']} 100%)",
    "padding": f"{SPACING['4']} {SPACING['6']}",
    "color": "white"
}

MODAL_BODY_STYLE = {
    "padding": SPACING["6"],
    "max_height": "50vh",
    "overflow_y": "auto"
}

MODAL_FOOTER_STYLE = {
    "background": DARK_THEME["colors"]["surface_secondary"],
    "padding": f"{SPACING['4']} {SPACING['6']}",
    "border_top": f"1px solid {DARK_THEME['colors']['primary']}"
}

# ==========================================
# 🎯 COMPONENTE: BOTÓN DE CONDICIÓN
# ==========================================

def condition_button(
    condition_key: str,
    is_selected: bool = False,
    is_current: bool = False
) -> rx.Component:
    """
    🎯 Botón individual para seleccionar una condición dental
    
    Args:
        condition_key: Clave de la condición (ej: "caries", "sano")
        is_selected: Si está seleccionado para aplicar
        is_current: Si es la condición actual de la superficie
    """
    
    condition_name = get_condition_name(condition_key)
    condition_color = get_condition_color(condition_key)
    
    # Estilos base
    base_style = {
        "width": "120px",
        "height": "80px",
        "border_radius": RADIUS["lg"],
        "cursor": "pointer",
        "transition": "all 0.2s ease",
        "display": "flex",
        "flex_direction": "column",
        "align_items": "center",
        "justify_content": "center",
        "gap": SPACING["2"],
        "position": "relative"
    }
    
    # Estilos condicionales usando rx.cond
    button_style = rx.cond(
        is_selected,
        {
            **base_style,
            "border": f"3px solid {COLORS['primary']['400']}",
            "box_shadow": f"0 8px 25px {COLORS['primary']['400']}40",
            "transform": "scale(1.05)"
        },
        rx.cond(
            is_current,
            {
                **base_style,
                "border": f"2px solid {COLORS['success']['400']}",
                "box_shadow": f"0 4px 15px {COLORS['success']['400']}30"
            },
            {
                **base_style,
                "border": f"2px solid {DARK_THEME['colors']['primary']}"
            }
        )
    )
    
    return rx.box(
        # Muestra de color de la condición
        rx.box(
            style={
                "width": "40px",
                "height": "25px",
                "background": condition_color,
                "border_radius": RADIUS["md"],
                "border": f"1px solid {DARK_THEME['colors']['border']}"
            }
        ),
        
        # Nombre de la condición
        rx.text(
            condition_name,
            size="2",
            weight="medium",
            color=DARK_THEME["colors"]["text_primary"],
            text_align="center"
        ),
        
        # Indicador de condición actual
        rx.cond(
            is_current,
            rx.box(
                rx.icon(tag="check", size=12, color="white"),
                style={
                    "position": "absolute",
                    "top": "5px",
                    "right": "5px",
                    "background": COLORS["success"]["500"],
                    "border_radius": "50%",
                    "width": "20px",
                    "height": "20px",
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center"
                }
            )
        ),
        
        # Indicador de selección para aplicar
        rx.cond(
            is_selected,
            rx.box(
                rx.icon(tag="arrow-right", size=12, color="white"),
                style={
                    "position": "absolute",
                    "top": "5px",
                    "left": "5px",
                    "background": COLORS["primary"]["500"],
                    "border_radius": "50%",
                    "width": "20px", 
                    "height": "20px",
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center"
                }
            )
        ),
        
        style=button_style,
        on_click=lambda: AppState.select_condition_to_apply(condition_key),
        _hover={
            "transform": "scale(1.02)",
            "box_shadow": f"0 6px 20px {condition_color}30"
        }
    )

# ==========================================
# 🗂️ COMPONENTE: CATEGORÍA DE CONDICIONES
# ==========================================

def condition_category_section(
    category_key: str,
    conditions_list: List[str],
    current_condition: Optional[str] = None,
    selected_condition: Optional[str] = None
) -> rx.Component:
    """
    🗂️ Sección de condiciones agrupadas por categoría
    
    Args:
        category_key: Clave de la categoría
        conditions_list: Lista de condiciones en la categoría
        current_condition: Condición actual de la superficie
        selected_condition: Condición seleccionada para aplicar
    """
    
    # Nombres de categorías para mostrar
    category_names = {
        "basicas": "🦷 Condiciones Básicas",
        "restaurativas": "🔧 Restauraciones", 
        "protesicas": "👑 Prótesis",
        "preventivas": "🛡️ Preventivas",
        "quirurgicas": "⚔️ Quirúrgicas",
        "endodonticas": "🧬 Endodoncia",
        "materiales": "🧱 Materiales",
        "estados": "📋 Estados de Tratamiento"
    }
    
    category_name = category_names.get(category_key, category_key.title())
    
    return rx.vstack(
        # Header de la categoría
        rx.text(
            category_name,
            size="4",
            weight="bold",
            color=COLORS["primary"]["400"],
            margin_bottom="3"
        ),
        
        # Grid de condiciones
        rx.flex(
            *[
                condition_button(
                    condition_key=condition,
                    is_selected=(selected_condition == condition),
                    is_current=(current_condition == condition)
                )
                for condition in conditions_list
            ],
            direction="row",
            wrap="wrap",
            gap=SPACING["3"],
            justify="start"
        ),
        
        spacing="2",
        align_items="start",
        width="100%"
    )

# ==========================================
# 🔍 COMPONENTE: FILTROS DE BÚSQUEDA
# ==========================================

def condition_search_filters() -> rx.Component:
    """🔍 Filtros de búsqueda y categorización"""
    
    return rx.vstack(
        # Búsqueda por texto
        rx.hstack(
            rx.icon(tag="search", size=16, color=DARK_THEME["colors"]["text_secondary"]),
            rx.input(
                placeholder="Buscar condición...",
                value=AppState.condition_search_term,
                on_change=AppState.set_condition_search_term,
                style={
                    "background": DARK_THEME["colors"]["surface_secondary"],
                    "border": f"1px solid {DARK_THEME['colors']['primary']}",
                    "flex": "1"
                }
            ),
            spacing="2",
            width="100%"
        ),
        
        # Filtros por categoría
        rx.hstack(
            rx.text("Categoría:", size="2", color=DARK_THEME["colors"]["text_secondary"]),
            rx.select(
                ["todas", "basicas", "restaurativas", "protesicas", "preventivas", 
                 "quirurgicas", "endodonticas", "materiales", "estados"],
                value=AppState.condition_category_filter,
                on_change=AppState.set_condition_category_filter,
                placeholder="Todas las categorías",
                style={
                    "background": DARK_THEME["colors"]["surface_secondary"],
                    "border": f"1px solid {DARK_THEME['colors']['primary']}"
                }
            ),
            spacing="2",
            align_items="center"
        ),
        
        spacing="3",
        width="100%"
    )

# ==========================================
# 📋 COMPONENTE: PREVIEW DEL CAMBIO
# ==========================================

def condition_change_preview() -> rx.Component:
    """📋 Preview visual del cambio que se va a aplicar"""
    
    return rx.cond(
        AppState.selected_condition_to_apply,
        rx.box(
            rx.hstack(
                rx.text("Vista previa del cambio:", size="3", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                rx.spacer(),
                
                # Cambio: de -> a
                rx.hstack(
                    # Condición actual
                    rx.vstack(
                        rx.box(
                            style={
                                "width": "30px",
                                "height": "20px",
                                "background": get_condition_color(rx.cond(AppState.current_surface_condition, AppState.current_surface_condition, "sano")),
                                "border_radius": RADIUS["sm"],
                                "border": f"1px solid {DARK_THEME['colors']['border']}"
                            }
                        ),
                        rx.text("Actual", size="1", color=DARK_THEME["colors"]["text_muted"]),
                        spacing="1", align_items="center"
                    ),
                    
                    rx.icon(tag="arrow-right", size=16, color=COLORS["primary"]["400"]),
                    
                    # Nueva condición
                    rx.vstack(
                        rx.box(
                            style={
                                "width": "30px",
                                "height": "20px", 
                                "background": get_condition_color(AppState.selected_condition_to_apply),
                                "border_radius": RADIUS["sm"],
                                "border": f"1px solid {DARK_THEME['colors']['border']}"
                            }
                        ),
                        rx.text("Nuevo", size="1", color=DARK_THEME["colors"]["text_muted"]),
                        spacing="1", align_items="center"
                    ),
                    
                    spacing="3", align_items="center"
                ),
                
                spacing="4", align_items="center", width="100%"
            ),
            style={
                "background": f"linear-gradient(135deg, {COLORS['primary']['900']}40 0%, {COLORS['primary']['800']}20 100%)",
                "border": f"1px solid {COLORS['primary']['600']}40",
                "border_radius": RADIUS["lg"],
                "padding": SPACING["3"]
            }
        )
    )

# ==========================================
# 🔧 COMPONENTE: MODAL PRINCIPAL
# ==========================================

def condition_selector_modal() -> rx.Component:
    """
    🔧 Modal principal para seleccionar condiciones dentales
    Se muestra cuando el usuario hace click en una superficie del diente
    """
    
    return rx.cond(
        AppState.condition_modal_open,
        rx.box(
            # Modal container
            rx.box(
                # Header del modal
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                f"Seleccionar Condición",
                                size="5",
                                weight="bold",
                                color="white"
                            ),
                            rx.text(
                                f"Diente: {AppState.selected_tooth} | Superficie: {AppState.selected_surface}",
                                size="3",
                                color="rgba(255, 255, 255, 0.8)"
                            ),
                            spacing="1", align_items="start"
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="x", size=20),
                            size="2",
                            variant="ghost",
                            color_scheme="gray",
                            on_click=AppState.close_condition_modal
                        ),
                        spacing="4", align_items="start", width="100%"
                    ),
                    style=MODAL_HEADER_STYLE
                ),
                
                # Body del modal
                rx.box(
                    rx.vstack(
                        # Filtros de búsqueda
                        condition_search_filters(),
                        
                        rx.divider(color=DARK_THEME["colors"]["border"]),
                        
                        # Preview del cambio
                        condition_change_preview(),
                        
                        # Secciones de condiciones por categoría
                        rx.vstack(
                            # Mostrar todas las categorías si el filtro es "todas"
                            rx.cond(
                                AppState.condition_category_filter == "todas",
                                rx.vstack(
                                    condition_category_section("basicas", CONDITION_CATEGORIES["basicas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    condition_category_section("restaurativas", CONDITION_CATEGORIES["restaurativas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    condition_category_section("protesicas", CONDITION_CATEGORIES["protesicas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    condition_category_section("preventivas", CONDITION_CATEGORIES["preventivas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    condition_category_section("quirurgicas", CONDITION_CATEGORIES["quirurgicas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    condition_category_section("endodonticas", CONDITION_CATEGORIES["endodonticas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    condition_category_section("materiales", CONDITION_CATEGORIES["materiales"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    condition_category_section("estados", CONDITION_CATEGORIES["estados"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    spacing="6", width="100%"
                                ),
                                # Mostrar solo la categoría seleccionada
                                rx.cond(
                                    AppState.condition_category_filter == "basicas",
                                    condition_category_section("basicas", CONDITION_CATEGORIES["basicas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                    rx.cond(
                                        AppState.condition_category_filter == "restaurativas",
                                        condition_category_section("restaurativas", CONDITION_CATEGORIES["restaurativas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                        rx.cond(
                                            AppState.condition_category_filter == "protesicas",
                                            condition_category_section("protesicas", CONDITION_CATEGORIES["protesicas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                            rx.cond(
                                                AppState.condition_category_filter == "preventivas",
                                                condition_category_section("preventivas", CONDITION_CATEGORIES["preventivas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                                rx.cond(
                                                    AppState.condition_category_filter == "quirurgicas",
                                                    condition_category_section("quirurgicas", CONDITION_CATEGORIES["quirurgicas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                                    rx.cond(
                                                        AppState.condition_category_filter == "endodonticas",
                                                        condition_category_section("endodonticas", CONDITION_CATEGORIES["endodonticas"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                                        rx.cond(
                                                            AppState.condition_category_filter == "materiales",
                                                            condition_category_section("materiales", CONDITION_CATEGORIES["materiales"], AppState.current_surface_condition, AppState.selected_condition_to_apply),
                                                            condition_category_section("estados", CONDITION_CATEGORIES["estados"], AppState.current_surface_condition, AppState.selected_condition_to_apply)
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            ),
                            spacing="6", width="100%"
                        ),
                        
                        spacing="4", width="100%"
                    ),
                    style=MODAL_BODY_STYLE
                ),
                
                # Footer del modal
                rx.box(
                    rx.hstack(
                        # Información adicional
                        rx.text(
                            "Selecciona una condición y haz click en Aplicar",
                            size="2",
                            color=DARK_THEME["colors"]["text_muted"]
                        ),
                        
                        rx.spacer(),
                        
                        # Botones de acción
                        rx.hstack(
                            rx.button(
                                "Cancelar",
                                size="3",
                                variant="outline",
                                color_scheme="gray",
                                on_click=AppState.close_condition_modal
                            ),
                            rx.button(
                                rx.cond(
                                    AppState.is_applying_condition,
                                    rx.spinner(size="3"),
                                    rx.text("Aplicar Cambio")
                                ),
                                size="3",
                                color_scheme="green",
                                on_click=AppState.apply_selected_condition,
                                disabled=rx.cond(AppState.selected_condition_to_apply, False, True)
                            ),
                            spacing="3"
                        ),
                        
                        spacing="4", align_items="center", width="100%"
                    ),
                    style=MODAL_FOOTER_STYLE
                ),
                
                style=MODAL_CONTAINER_STYLE
            ),
            
            style=MODAL_OVERLAY_STYLE
        )
    )

# ==========================================
# 🎨 COMPONENTE: LEYENDA DE CONDICIONES
# ==========================================

def odontogram_legend() -> rx.Component:
    """🎨 Leyenda visual con todas las condiciones disponibles"""
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="palette", size=20, color=COLORS["primary"]["500"]),
                rx.text("Leyenda de Condiciones", size="4", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
                spacing="2", align_items="center"
            ),
            
            # Grid compacto de condiciones
            rx.flex(
                *[
                    rx.hstack(
                        rx.box(
                            style={
                                "width": "16px",
                                "height": "16px",
                                "background": get_condition_color(condition),
                                "border_radius": RADIUS["sm"],
                                "border": f"1px solid {DARK_THEME['colors']['border']}"
                            }
                        ),
                        rx.text(
                            get_condition_name(condition),
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="2", align_items="center"
                    )
                    for condition in ["sano", "caries", "obturado", "corona", "implante", 
                                     "ausente", "fractura", "endodoncia", "protesis"]
                ],
                direction="column",
                spacing="1"
            ),
            
            spacing="3", align_items="start", width="100%"
        ),
        style={
            "background": DARK_THEME["colors"]["surface_secondary"],
            "border": f"1px solid {DARK_THEME['colors']['primary']}",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "max_width": "300px"
        }
    )