# 🦷 COMPONENTE: MODAL SELECTOR DE CONDICIONES DENTALES V2.0
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
# 🎨 ESTILOS DEL MODAL V2.0 - MODERNOS
# ==========================================

def get_color_tone(color_name: str, tone: str) -> str:
    """
    Obtiene un tono de color de forma segura, con fallback a tonos disponibles.

    Args:
        color_name: Nombre del color (primary, blue, etc)
        tone: Tono deseado (400, 500, 600)

    Returns:
        Código hexadecimal del color
    """
    # Colores especiales con solo 500
    if color_name in ['secondary', 'info']:
        return COLORS[color_name]['500']

    # Intentar obtener el tono solicitado
    if tone in COLORS[color_name]:
        return COLORS[color_name][tone]

    # Fallbacks por tono
    if tone == '400':
        # Si no hay 400, usar 500 o 300
        return COLORS[color_name].get('500', COLORS[color_name].get('300', COLORS[color_name]['500']))
    elif tone == '600':
        # Si no hay 600, usar 700 o 500
        return COLORS[color_name].get('700', COLORS[color_name].get('500', COLORS[color_name]['500']))
    else:
        # Tono 500 siempre debe existir
        return COLORS[color_name]['500']


def map_to_radix_color_scheme(color_name: str) -> str:
    """
    Mapea nuestros colores personalizados a los color_scheme válidos de Radix UI.

    Radix UI acepta: gray, red, orange, yellow, green, blue, purple, pink,
                     crimson, indigo, cyan, teal, mint, lime, amber, bronze, gold, sky, violet

    Args:
        color_name: Nuestro color personalizado (primary, secondary, success, etc)

    Returns:
        Color scheme válido de Radix UI
    """
    color_scheme_map = {
        "primary": "cyan",      # Turquesa → cyan
        "secondary": "amber",   # Dorado → amber
        "blue": "blue",         # Azul → blue
        "gray": "gray",         # Gris → gray
        "success": "green",     # Verde → green
        "error": "red",         # Rojo → red
        "warning": "orange",    # Amarillo/naranja → orange
        "info": "sky"           # Info → sky (azul claro)
    }

    return color_scheme_map.get(color_name, "gray")  # Default: gray

MODAL_OVERLAY_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "width": "100vw",
    "height": "100vh",
    "background": "linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(20, 20, 20, 0.9) 100%)",
    "backdrop_filter": "blur(12px)",
    "z_index": "1000",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "animation": "fadeIn 0.3s ease-out"
}

MODAL_CONTAINER_STYLE = {
    "background": f"linear-gradient(145deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_elevated']} 100%)",
    "border": f"1px solid {COLORS['primary']['400']}40",
    "border_radius": "24px",
    "box_shadow": f"0 32px 64px rgba(0, 0, 0, 0.6), 0 0 0 1px {COLORS['primary']['400']}20, inset 0 1px 0 rgba(255, 255, 255, 0.1)",
    "width": "95%",
    "max_width": "900px",
    "max_height": "85vh",
    "overflow": "hidden",
    "transform": "scale(1)",
    "animation": "modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)"
}

MODAL_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['600']} 0%, {COLORS['primary']['500']} 50%, {COLORS['blue']['600']} 100%)",
    "padding": "24px 32px",
    "color": "white",
    "position": "relative",
    "overflow": "hidden"
}

MODAL_BODY_STYLE = {
    "padding": "32px",
    "max_height": "55vh",
    "overflow_y": "auto",
    "background": f"linear-gradient(180deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)"
}

MODAL_FOOTER_STYLE = {
    "background": f"linear-gradient(90deg, {DARK_THEME['colors']['surface_secondary']} 0%, {DARK_THEME['colors']['surface']} 100%)",
    "padding": "24px 32px",
    "border_top": f"1px solid {COLORS['primary']['400']}30"
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
    🎯 Botón individual para seleccionar una condición dental V2.0
    Diseño moderno con glassmorphism y animaciones suaves
    """

    condition_name = get_condition_name(condition_key)
    condition_color = get_condition_color(condition_key)

    return rx.box(
        # Contenedor principal con glassmorphism
        rx.box(
            # Muestra de color grande y prominente
            rx.box(
                style={
                    "width": "60px",
                    "height": "60px",
                    "background": f"linear-gradient(135deg, {condition_color} 0%, {condition_color}80 100%)",
                    "border_radius": "16px",
                    "border": "2px solid rgba(255, 255, 255, 0.2)",
                    "box_shadow": f"0 8px 24px {condition_color}40, inset 0 1px 0 rgba(255, 255, 255, 0.2)",
                    "margin_bottom": "12px",
                    "position": "relative",
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center"
                }
            ),

            # Nombre de la condición
            rx.text(
                condition_name,
                size="3",
                weight="bold",
                color="white",
                text_align="center",
                style={
                    "text_shadow": "0 2px 8px rgba(0, 0, 0, 0.6)",
                    "margin_bottom": "4px"
                }
            ),

            # Badge de estado (actual/seleccionado)
            rx.cond(
                is_current,
                rx.badge(
                    rx.hstack(
                        rx.icon(tag="check", size=12),
                        rx.text("Actual", size="1"),
                        spacing="1",
                        align="center"
                    ),
                    color_scheme="green",
                    variant="solid",
                    size="1"
                ),
                rx.cond(
                    is_selected,
                    rx.badge(
                        rx.hstack(
                            rx.icon(tag="arrow-right", size=12),
                            rx.text("Nuevo", size="1"),
                            spacing="1",
                            align="center"
                        ),
                        color_scheme="blue",
                        variant="solid",
                        size="1"
                    ),
                    rx.box(height="24px")  # Spacer para mantener altura consistente
                )
            ),

            # Estilos del contenedor
            style={
                "width": "140px",
                "height": "140px",
                "padding": "16px",
                "border_radius": "20px",
                "background": rx.cond(
                    is_selected,
                    f"linear-gradient(135deg, {COLORS['primary']['600']}40 0%, {COLORS['primary']['500']}30 100%)",
                    rx.cond(
                        is_current,
                        f"linear-gradient(135deg, {COLORS['success']['600']}40 0%, {COLORS['success']['500']}30 100%)",
                        f"linear-gradient(135deg, {DARK_THEME['colors']['surface_elevated']} 0%, {DARK_THEME['colors']['surface']} 100%)"
                    )
                ),
                "border": rx.cond(
                    is_selected,
                    f"2px solid {COLORS['primary']['400']}",
                    rx.cond(
                        is_current,
                        f"2px solid {COLORS['success']['400']}",
                        f"1px solid {DARK_THEME['colors']['border']}"
                    )
                ),
                "box_shadow": rx.cond(
                    is_selected,
                    f"0 12px 32px {COLORS['primary']['400']}30, 0 0 0 1px {COLORS['primary']['400']}20",
                    rx.cond(
                        is_current,
                        f"0 8px 24px {COLORS['success']['400']}25, 0 0 0 1px {COLORS['success']['400']}20",
                        f"0 4px 16px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)"
                    )
                ),
                "cursor": "pointer",
                "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                "transform": rx.cond(is_selected, "scale(1.05)", "scale(1)"),
                "display": "flex",
                "flex_direction": "column",
                "align_items": "center",
                "justify_content": "center",
                "position": "relative",
                "backdrop_filter": "blur(10px)",
                "overflow": "hidden"
            },

            # Efectos hover y click
            _hover={
                "transform": "scale(1.08) translateY(-2px)",
                "box_shadow": f"0 16px 40px {condition_color}40, 0 0 0 1px {condition_color}30",
                "border_color": condition_color
            },
            _active={
                "transform": "scale(1.02)",
                "transition": "all 0.1s ease"
            }
        ),

        on_click=lambda: AppState.seleccionar_condicion_temporal(condition_key)
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
    🗂️ Sección de condiciones agrupadas por categoría V2.0
    Diseño moderno con glassmorphism y mejor organización visual
    """

    # Nombres de categorías para mostrar con iconos mejorados
    # Colores disponibles: primary, secondary, blue, gray, success, error, warning, info
    category_info = {
        "basicas": {"name": "Condiciones Básicas", "icon": "activity", "color": "blue"},
        "restaurativas": {"name": "Restauraciones", "icon": "wrench", "color": "primary"},
        "protesicas": {"name": "Prótesis", "icon": "crown", "color": "secondary"},
        "preventivas": {"name": "Preventivas", "icon": "shield", "color": "success"},
        "quirurgicas": {"name": "Quirúrgicas", "icon": "scissors", "color": "error"},
        "endodonticas": {"name": "Endodoncia", "icon": "zap", "color": "warning"},
        "materiales": {"name": "Materiales", "icon": "box", "color": "gray"},
        "estados": {"name": "Estados", "icon": "clipboard", "color": "info"}
    }

    category_data = category_info.get(category_key, {"name": category_key.title(), "icon": "circle", "color": "gray"})

    return rx.box(
        # Header mejorado de la categoría
        rx.hstack(
            rx.box(
                rx.icon(tag=category_data["icon"], size=20, color="white"),
                style={
                    "background": f"linear-gradient(135deg, {get_color_tone(category_data['color'], '500')} 0%, {get_color_tone(category_data['color'], '600')} 100%)",
                    "border_radius": "12px",
                    "padding": "8px",
                    "box_shadow": f"0 4px 16px {get_color_tone(category_data['color'], '400')}40"
                }
            ),
            rx.text(
                category_data["name"],
                size="5",
                weight="bold",
                color=get_color_tone(category_data["color"], "400"),
                style={"text_shadow": "0 1px 3px rgba(0, 0, 0, 0.3)"}
            ),
            rx.badge(
                f"{len(conditions_list)} opciones",
                color=category_data["color"],
                variant="soft",
                size="1"
            ),
            spacing="3",
            align="center",
            margin_bottom="4"
        ),

        # Grid mejorado de condiciones
        rx.box(
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
                gap="16px",
                justify="start",
                align="start"
            ),
            style={
                "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
                "border_radius": "16px",
                "padding": "20px",
                "border": f"1px solid {get_color_tone(category_data['color'], '500')}20",
                "box_shadow": f"inset 0 1px 0 rgba(255, 255, 255, 0.1), 0 2px 8px rgba(0, 0, 0, 0.1)"
            }
        ),

        width="100%",
        margin_bottom="6"
    )

# ==========================================
# 🔍 COMPONENTE: FILTROS DE BÚSQUEDA
# ==========================================

def condition_search_filters() -> rx.Component:
    """🔍 Filtros de búsqueda y categorización V2.0 - Modernos"""

    return rx.box(
        rx.vstack(
            # Header de filtros
            rx.hstack(
                rx.icon(tag="filter", size=20, color=COLORS["primary"]["400"]),
                rx.text(
                    "Filtros de Búsqueda",
                    size="4",
                    weight="bold",
                    color=COLORS["primary"]["400"]
                ),
                spacing="2",
                align="center",
                margin_bottom="3"
            ),

            # Búsqueda por texto mejorada
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.icon(tag="search", size=18, color=COLORS["primary"]["400"]),
                        style={
                            "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['blue']['500']} 100%)",
                            "border_radius": "10px",
                            "padding": "8px",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center"
                        }
                    ),
                    rx.input(
                        placeholder="Buscar condición dental...",
                        value=AppState.termino_busqueda_condicion,
                        on_change=AppState.actualizar_busqueda_condicion,
                        style={
                            "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface_elevated']} 0%, {DARK_THEME['colors']['surface']} 100%)",
                            "border": f"2px solid {COLORS['primary']['500']}30",
                            "border_radius": "12px",
                            "padding": "12px 16px",
                            "font_size": "14px",
                            "color": "white",
                            "flex": "1",
                            "_focus": {
                                "border_color": COLORS["primary"]["400"],
                                "box_shadow": f"0 0 0 3px {COLORS['primary']['400']}20"
                            },
                            "_placeholder": {
                                "color": DARK_THEME["colors"]["text_muted"]
                            }
                        }
                    ),
                    spacing="3",
                    width="100%"
                ),
                margin_bottom="3"
            ),

            # Filtros por categoría mejorados
            rx.hstack(
                rx.box(
                    rx.icon(tag="folder", size=18, color=COLORS["primary"]["400"]),
                    style={
                        "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['blue']['500']} 100%)",
                        "border_radius": "10px",
                        "padding": "8px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                rx.text(
                    "Categoría:",
                    size="3",
                    weight="medium",
                    color=COLORS["primary"]["400"],
                    min_width="80px"
                ),
                rx.select(
                    ["todas", "basicas", "restaurativas", "protesicas", "preventivas",
                     "quirurgicas", "endodonticas", "materiales", "estados"],
                    value=AppState.categoria_condicion_seleccionada,
                    on_change=AppState.cambiar_categoria_condicion,
                    placeholder="Todas las categorías",
                    style={
                        "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface_elevated']} 0%, {DARK_THEME['colors']['surface']} 100%)",
                        "border": f"2px solid {COLORS['primary']['500']}30",
                        "border_radius": "12px",
                        "padding": "8px 12px",
                        "color": "white",
                        "flex": "1",
                        "_focus": {
                            "border_color": COLORS["primary"]["400"],
                            "box_shadow": f"0 0 0 3px {COLORS['primary']['400']}20"
                        }
                    }
                ),
                spacing="3",
                width="100%",
                align="center"
            ),

            spacing="4",
            width="100%"
        ),

        style={
            "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface_elevated']}80 0%, {DARK_THEME['colors']['surface']}60 100%)",
            "border": f"1px solid {COLORS['primary']['500']}30",
            "border_radius": "16px",
            "padding": "20px",
            "backdrop_filter": "blur(10px)",
            "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)"
        },
        margin_bottom="4"
    )

# ==========================================
# 📋 COMPONENTE: PREVIEW DEL CAMBIO
# ==========================================

def condition_change_preview() -> rx.Component:
    """📋 Preview visual del cambio que se va a aplicar V2.0"""

    return rx.cond(
        AppState.condicion_seleccionada_temp,
        rx.box(
            rx.vstack(
                # Header del preview
                rx.hstack(
                    rx.box(
                        rx.icon(tag="eye", size=18, color="white"),
                        style={
                            "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['success']['600']} 100%)",
                            "border_radius": "10px",
                            "padding": "8px",
                            "box_shadow": f"0 4px 16px {COLORS['success']['400']}40"
                        }
                    ),
                    rx.text(
                        "Vista Previa del Cambio",
                        size="4",
                        weight="bold",
                        color=COLORS["success"]["400"],
                        style={"text_shadow": "0 1px 3px rgba(0, 0, 0, 0.3)"}
                    ),
                    spacing="3",
                    align="center"
                ),

                # Visualización del cambio con animación
                rx.center(
                    rx.hstack(
                        # Condición actual
                        rx.vstack(
                            rx.box(
                                rx.box(
                                    style={
                                        "width": "50px",
                                        "height": "50px",
                                        "background": f"linear-gradient(135deg, {get_condition_color(rx.cond(AppState.current_surface_condition, AppState.current_surface_condition, 'sano'))} 0%, {get_condition_color(rx.cond(AppState.current_surface_condition, AppState.current_surface_condition, 'sano'))}80 100%)",
                                        "border_radius": "12px",
                                        "border": "2px solid rgba(255, 255, 255, 0.2)",
                                        "box_shadow": f"0 6px 20px {get_condition_color(rx.cond(AppState.current_surface_condition, AppState.current_surface_condition, 'sano'))}40, inset 0 1px 0 rgba(255, 255, 255, 0.2)"
                                    }
                                ),
                                style={
                                    "padding": "8px",
                                    "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface_elevated']} 0%, {DARK_THEME['colors']['surface']} 100%)",
                                    "border_radius": "16px",
                                    "border": f"1px solid {COLORS['gray']['600']}40"
                                }
                            ),
                            rx.badge(
                                rx.hstack(
                                    rx.icon(tag="clock", size=12),
                                    rx.text("Actual", size="1"),
                                    spacing="1",
                                    align="center"
                                ),
                                color_scheme="gray",
                                variant="soft",
                                size="1"
                            ),
                            spacing="2",
                            align="center"
                        ),

                        # Flecha animada
                        rx.box(
                            rx.icon(tag="arrow-right", size=24, color=COLORS["primary"]["400"]),
                            style={
                                "background": f"linear-gradient(135deg, {COLORS['primary']['600']} 0%, {COLORS['primary']['500']} 100%)",
                                "border_radius": "50%",
                                "padding": "12px",
                                "animation": "pulse 2s infinite",
                                "box_shadow": f"0 4px 20px {COLORS['primary']['400']}50"
                            }
                        ),

                        # Nueva condición
                        rx.vstack(
                            rx.box(
                                rx.box(
                                    style={
                                        "width": "50px",
                                        "height": "50px",
                                        "background": f"linear-gradient(135deg, {get_condition_color(AppState.condicion_seleccionada_temp)} 0%, {get_condition_color(AppState.condicion_seleccionada_temp)}80 100%)",
                                        "border_radius": "12px",
                                        "border": "2px solid rgba(255, 255, 255, 0.2)",
                                        "box_shadow": f"0 6px 20px {get_condition_color(AppState.condicion_seleccionada_temp)}40, inset 0 1px 0 rgba(255, 255, 255, 0.2)"
                                    }
                                ),
                                style={
                                    "padding": "8px",
                                    "background": f"linear-gradient(135deg, {COLORS['success']['600']}30 0%, {COLORS['success']['500']}20 100%)",
                                    "border_radius": "16px",
                                    "border": f"2px solid {COLORS['success']['400']}60",
                                    "box_shadow": f"0 8px 24px {COLORS['success']['400']}30"
                                }
                            ),
                            rx.badge(
                                rx.hstack(
                                    rx.icon(tag="sparkles", size=12),
                                    rx.text("Nuevo", size="1"),
                                    spacing="1",
                                    align="center"
                                ),
                                color_scheme="green",
                                variant="solid",
                                size="1"
                            ),
                            spacing="2",
                            align="center"
                        ),

                        spacing="6",
                        align="center",
                        justify="center"
                    )
                ),

                spacing="4",
                align="center",
                width="100%"
            ),

            style={
                "background": f"linear-gradient(135deg, {COLORS['success']['800']}40 0%, {COLORS['success']['700']}30 100%)",
                "border": f"2px solid {COLORS['success']['500']}60",
                "border_radius": "20px",
                "padding": "24px",
                "backdrop_filter": "blur(10px)",
                "box_shadow": f"0 16px 40px {COLORS['success']['400']}20, inset 0 1px 0 rgba(255, 255, 255, 0.1)"
            }
        ),
        # Estado cuando no hay condición seleccionada
        rx.box(
            rx.center(
                rx.vstack(
                    rx.icon(tag="info", size=32, color=COLORS["gray"]["500"]),
                    rx.text(
                        "Selecciona una condición para ver el preview",
                        size="3",
                        color=COLORS["gray"]["400"],
                        text_align="center"
                    ),
                    spacing="3",
                    align="center"
                )
            ),
            style={
                "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
                "border": f"1px dashed {COLORS['gray']['600']}",
                "border_radius": "16px",
                "padding": "20px",
                "min_height": "120px"
            }
        )
    )

# ==========================================
# 🔧 COMPONENTE: MODAL PRINCIPAL
# ==========================================

def condition_selector_modal() -> rx.Component:
    """
    🔧 Modal principal para seleccionar condiciones dentales V2.0
    Diseño moderno con glassmorphism, animaciones y mejor UX
    """

    return rx.cond(
        AppState.modal_condiciones_abierto,
        rx.box(
            # Modal container
            rx.box(
                # Header modernizado del modal
                rx.box(
                    rx.vstack(
                        # Título principal con gradiente
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="tooth", size=28, color="white"),
                                style={
                                    "background": "rgba(255, 255, 255, 0.2)",
                                    "border_radius": "12px",
                                    "padding": "8px",
                                    "backdrop_filter": "blur(10px)"
                                }
                            ),
                            rx.vstack(
                                rx.text(
                                    "Selector de Condiciones Dentales",
                                    size="6",
                                    weight="bold",
                                    color="white",
                                    style={"text_shadow": "0 2px 8px rgba(0, 0, 0, 0.3)"}
                                ),
                                rx.text(
                                    "Selecciona la nueva condición para aplicar",
                                    size="3",
                                    color="rgba(255, 255, 255, 0.9)",
                                    style={"text_shadow": "0 1px 4px rgba(0, 0, 0, 0.3)"}
                                ),
                                spacing="1",
                                align="start"
                            ),
                            rx.spacer(),
                            rx.button(
                                rx.icon(tag="x", size=24),
                                size="3",
                                variant="ghost",
                                color_scheme="gray",
                                on_click=AppState.cerrar_modal_condiciones,
                                style={
                                    "border_radius": "12px",
                                    "_hover": {
                                        "background": "rgba(255, 255, 255, 0.2)",
                                        "backdrop_filter": "blur(10px)"
                                    }
                                }
                            ),
                            spacing="4",
                            align="start",
                            width="100%"
                        ),

                        # Información del diente/superficie
                        rx.box(
                            rx.hstack(
                                rx.badge(
                                    rx.hstack(
                                        rx.icon(tag="map-pin", size=14),
                                        rx.text(f"Diente {AppState.diente_seleccionado}", size="2"),
                                        spacing="1",
                                        align="center"
                                    ),
                                    color_scheme="gray",
                                    variant="solid",
                                    size="2"
                                ),
                                rx.badge(
                                    rx.hstack(
                                        rx.icon(tag="target", size=14),
                                        rx.text(f"Superficie {AppState.superficie_seleccionada}", size="2"),
                                        spacing="1",
                                        align="center"
                                    ),
                                    color_scheme="gray",
                                    variant="solid",
                                    size="2"
                                ),
                                spacing="2",
                                justify="center"
                            ),
                            style={
                                "background": "rgba(255, 255, 255, 0.1)",
                                "border_radius": "12px",
                                "padding": "12px",
                                "backdrop_filter": "blur(10px)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)"
                            }
                        ),

                        spacing="4",
                        width="100%"
                    ),
                    style=MODAL_HEADER_STYLE
                ),

                # Body modernizado del modal
                rx.box(
                    rx.vstack(
                        # Filtros de búsqueda
                        condition_search_filters(),

                        # Preview del cambio
                        condition_change_preview(),

                        # Secciones de condiciones mejoradas
                        rx.box(
                            # Mostrar todas las categorías si el filtro es "todas"
                            rx.cond(
                                AppState.categoria_condicion_seleccionada == "todas",
                                rx.vstack(
                                    condition_category_section("basicas", CONDITION_CATEGORIES["basicas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp),
                                    condition_category_section("restaurativas", CONDITION_CATEGORIES["restaurativas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp),
                                    condition_category_section("protesicas", CONDITION_CATEGORIES["protesicas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp),
                                    condition_category_section("preventivas", CONDITION_CATEGORIES["preventivas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp),
                                    spacing="4",
                                    width="100%"
                                ),
                                # Categoría específica seleccionada
                                rx.match(
                                    AppState.categoria_condicion_seleccionada,
                                    ("basicas", condition_category_section("basicas", CONDITION_CATEGORIES["basicas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    ("restaurativas", condition_category_section("restaurativas", CONDITION_CATEGORIES["restaurativas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    ("protesicas", condition_category_section("protesicas", CONDITION_CATEGORIES["protesicas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    ("preventivas", condition_category_section("preventivas", CONDITION_CATEGORIES["preventivas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    ("quirurgicas", condition_category_section("quirurgicas", CONDITION_CATEGORIES["quirurgicas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    ("endodonticas", condition_category_section("endodonticas", CONDITION_CATEGORIES["endodonticas"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    ("materiales", condition_category_section("materiales", CONDITION_CATEGORIES["materiales"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    ("estados", condition_category_section("estados", CONDITION_CATEGORIES["estados"], AppState.current_surface_condition, AppState.condicion_seleccionada_temp)),
                                    rx.text("Categoría no encontrada")
                                )
                            ),
                            width="100%"
                        ),

                        spacing="6",
                        width="100%"
                    ),
                    style=MODAL_BODY_STYLE
                ),

                # Footer modernizado del modal
                rx.box(
                    rx.hstack(
                        # Información y ayuda
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="lightbulb", size=16, color=COLORS["warning"]["400"]),
                                rx.text(
                                    "Tip: Utiliza los filtros para encontrar condiciones específicas",
                                    size="2",
                                    color=DARK_THEME["colors"]["text_muted"]
                                ),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.icon(tag="info", size=16, color=COLORS["blue"]["500"]),
                                rx.text(
                                    "Los cambios se guardan automáticamente al aplicar",
                                    size="2",
                                    color=DARK_THEME["colors"]["text_muted"]
                                ),
                                spacing="2",
                                align="center"
                            ),
                            spacing="1",
                            align="start"
                        ),

                        rx.spacer(),

                        # Botones modernizados de acción
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.icon(tag="x", size=16),
                                    rx.text("Cancelar", size="3"),
                                    spacing="2",
                                    align="center"
                                ),
                                size="3",
                                variant="outline",
                                color_scheme="gray",
                                on_click=AppState.cerrar_modal_condiciones,
                                style={
                                    "border_radius": "12px",
                                    "padding": "12px 20px"
                                }
                            ),
                            rx.button(
                                rx.cond(
                                    AppState.odontograma_guardando,
                                    rx.hstack(
                                        rx.spinner(size="3"),
                                        rx.text("Aplicando...", size="3"),
                                        spacing="2",
                                        align="center"
                                    ),
                                    rx.hstack(
                                        rx.icon(tag="check", size=16),
                                        rx.text("Aplicar Cambio", size="3"),
                                        spacing="2",
                                        align="center"
                                    )
                                ),
                                size="3",
                                color_scheme="green",
                                on_click=AppState.aplicar_condicion_seleccionada,
                                disabled=rx.cond(AppState.condicion_seleccionada_temp, False, True),
                                style={
                                    "border_radius": "12px",
                                    "padding": "12px 24px",
                                    "box_shadow": f"0 4px 16px {COLORS['success']['400']}30"
                                }
                            ),
                            spacing="3"
                        ),

                        spacing="4",
                        align="center",
                        width="100%"
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