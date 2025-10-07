"""
🏥 MODAL MÉDICO PROFESIONAL: SELECTOR DE CONDICIONES DENTALES
===========================================================

Modal profesional y limpio para seleccionar condiciones dentales.
Diseñado según estándares médicos sin efectos distractores.

Características:
- Diseño limpio sin glassmorphism excesivo
- Animaciones sutiles (200ms ease-out)
- Grid compacto 80x80px
- Vista lista alternativa disponible
- Preview minimal sin información redundante
- Footer simple con 2 botones
- Paleta médica profesional

Versión: 3.0 Professional Medical
Fecha: Enero 2025
"""

import reflex as rx
from typing import List, Dict
from dental_system.state.app_state import AppState
from dental_system.styles.medical_design_system import (
    MEDICAL_COLORS,
    MEDICAL_SPACING,
    MEDICAL_TYPOGRAPHY,
    MEDICAL_SHADOWS,
    MEDICAL_RADIUS,
    MEDICAL_TRANSITIONS,
    medical_modal_overlay_style,
    medical_modal_container_style,
    medical_button_style,
    get_dental_condition_color
)

# ==========================================
# 📋 CONDICIONES MÉDICAS DISPONIBLES
# ==========================================

MEDICAL_CONDITIONS = [
    # Condiciones básicas
    {"key": "sano", "name": "Sano", "category": "basica", "icon": "circle-check"},
    {"key": "caries", "name": "Caries", "category": "basica", "icon": "circle-alert", "urgent": True},
    {"key": "fractura", "name": "Fractura", "category": "basica", "icon": "triangle-alert", "urgent": True},

    # Restauraciones
    {"key": "obturado", "name": "Obturado", "category": "restaurativa", "icon": "shield"},
    {"key": "composite", "name": "Composite", "category": "restaurativa", "icon": "layers"},
    {"key": "amalgama", "name": "Amalgama", "category": "restaurativa", "icon": "box"},
    {"key": "resina", "name": "Resina", "category": "restaurativa", "icon": "droplet"},

    # Prótesis
    {"key": "corona", "name": "Corona", "category": "protesica", "icon": "crown"},
    {"key": "puente", "name": "Puente", "category": "protesica", "icon": "link"},
    {"key": "implante", "name": "Implante", "category": "protesica", "icon": "anchor"},
    {"key": "protesis", "name": "Prótesis", "category": "protesica", "icon": "smile"},

    # Tratamientos especiales
    {"key": "endodoncia", "name": "Endodoncia", "category": "endodontica", "icon": "activity"},
    {"key": "ausente", "name": "Ausente", "category": "quirurgica", "icon": "x-circle"},
    {"key": "extraccion", "name": "Extracción", "category": "quirurgica", "icon": "minus-circle"},

    # Estados
    {"key": "planificado", "name": "Planificado", "category": "estado", "icon": "calendar"},
    {"key": "en_tratamiento", "name": "En Tratamiento", "category": "estado", "icon": "clock"}
]

# ==========================================
# 🎨 BOTÓN DE CONDICIÓN MÉDICA
# ==========================================

def medical_condition_button(condition: Dict) -> rx.Component:
    """
    🎨 Botón de condición médica profesional - Diseño compacto y limpio

    Args:
        condition: Diccionario con información de la condición

    Returns:
        Componente de botón médico profesional
    """

    condition_key = condition["key"]
    condition_name = condition["name"]
    is_selected = AppState.condicion_seleccionada_temp == condition_key
    is_current = AppState.current_surface_condition == condition_key
    is_urgent = condition.get("urgent", False)

    # Obtener color médico
    color_base = get_dental_condition_color(condition_key, "base")
    color_light = get_dental_condition_color(condition_key, "light")

    return rx.box(
        # Muestra de color grande
        rx.box(
            style={
                "width": "40px",
                "height": "40px",
                "background": color_light,
                "border": f"2px solid {color_base}",
                "border_radius": MEDICAL_RADIUS["base"],
                "margin_bottom": "8px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center"
            }
        ),

        # Nombre de condición
        rx.text(
            condition_name,
            font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
            font_weight=rx.cond(
                is_selected | is_current,
                MEDICAL_TYPOGRAPHY["font_weight"]["semibold"],
                MEDICAL_TYPOGRAPHY["font_weight"]["normal"]
            ),
            color=rx.cond(
                is_selected | is_current,
                MEDICAL_COLORS["medical_ui"]["text_primary"],
                MEDICAL_COLORS["medical_ui"]["text_secondary"]
            ),
            text_align="center",
            line_height=MEDICAL_TYPOGRAPHY["line_height"]["tight"]
        ),

        # Badge de estado
        rx.cond(
            is_current,
            rx.badge(
                "Actual",
                size="1",
                color_scheme="gray",
                variant="soft"
            ),
            rx.cond(
                is_selected,
                rx.badge(
                    "Seleccionado",
                    size="1",
                    color_scheme="blue",
                    variant="soft"
                ),
                rx.box(height="20px")  # Spacer para mantener altura
            )
        ),

        # Indicador de urgencia (si aplica)
        rx.cond(
            is_urgent,
            rx.box(
                "!",
                style={
                    "position": "absolute",
                    "top": "2px",
                    "right": "2px",
                    "width": "16px",
                    "height": "16px",
                    "background": MEDICAL_COLORS["medical_ui"]["accent_error"],
                    "color": "white",
                    "border_radius": MEDICAL_RADIUS["full"],
                    "font_size": MEDICAL_TYPOGRAPHY["font_size"]["xs"],
                    "font_weight": MEDICAL_TYPOGRAPHY["font_weight"]["bold"],
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center",
                    "box_shadow": MEDICAL_SHADOWS["sm"]
                }
            )
        ),

        # Estilos del contenedor
        style={
            "width": "80px",
            "height": "90px",
            "padding": "8px",
            "border_radius": MEDICAL_RADIUS["md"],
            "background": rx.cond(
                is_selected,
                MEDICAL_COLORS["medical_ui"]["selected_overlay"],
                rx.cond(
                    is_current,
                    MEDICAL_COLORS["medical_ui"]["surface"],
                    MEDICAL_COLORS["medical_ui"]["surface"]
                )
            ),
            "border": f"1px solid",
            "border_color": rx.cond(
                is_selected,
                MEDICAL_COLORS["medical_ui"]["border_focus"],
                rx.cond(
                    is_current,
                    MEDICAL_COLORS["medical_ui"]["border_medium"],
                    MEDICAL_COLORS["medical_ui"]["border_light"]
                )
            ),
            "box_shadow": rx.cond(
                is_selected,
                MEDICAL_SHADOWS["md"],
                MEDICAL_SHADOWS["xs"]
            ),
            "cursor": "pointer",
            "transition": MEDICAL_TRANSITIONS["base"],
            "display": "flex",
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center",
            "position": "relative",

            # Hover profesional
            "_hover": {
                "border_color": MEDICAL_COLORS["medical_ui"]["border_focus"],
                "box_shadow": MEDICAL_SHADOWS["md"],
                "background": MEDICAL_COLORS["medical_ui"]["hover_overlay"]
            }
        },

        # Evento de selección
        on_click=lambda: AppState.seleccionar_condicion_temporal(condition_key)
    )


# ==========================================
# 📊 GRID DE CONDICIONES POR CATEGORÍA
# ==========================================

def medical_conditions_grid(category: str = "todas") -> rx.Component:
    """
    📊 Grid de condiciones médicas organizado por categoría

    Args:
        category: Categoría a mostrar (todas, basica, restaurativa, etc)

    Returns:
        Grid con condiciones médicas profesionales
    """

    # Filtrar condiciones por categoría
    if category == "todas":
        conditions_to_show = MEDICAL_CONDITIONS
    else:
        conditions_to_show = [c for c in MEDICAL_CONDITIONS if c.get("category") == category]

    return rx.box(
        rx.grid(
            *[
                medical_condition_button(condition)
                for condition in conditions_to_show
            ],
            columns="4",  # 4 columnas para diseño compacto
            gap=MEDICAL_SPACING["md"],
            width="100%"
        ),
        style={
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "border_radius": MEDICAL_RADIUS["md"],
            "padding": MEDICAL_SPACING["md"],
            "border": f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}"
        }
    )


# ==========================================
# 🔍 FILTROS DE CATEGORÍA
# ==========================================

def medical_category_filters() -> rx.Component:
    """
    🔍 Filtros de categoría médica profesionales

    Returns:
        Selector de categoría simple
    """

    categories = [
        {"key": "todas", "name": "Todas"},
        {"key": "basica", "name": "Básicas"},
        {"key": "restaurativa", "name": "Restauraciones"},
        {"key": "protesica", "name": "Prótesis"},
        {"key": "endodontica", "name": "Endodoncia"},
        {"key": "quirurgica", "name": "Quirúrgicas"},
        {"key": "estado", "name": "Estados"}
    ]

    return rx.hstack(
        rx.text(
            "Categoría:",
            font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
            font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["medium"],
            color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
        ),
        rx.select(
            [cat["name"] for cat in categories],
            placeholder="Todas las condiciones",
            value=AppState.categoria_condicion_seleccionada,
            on_change=AppState.cambiar_categoria_condicion,
            size="2"
        ),
        spacing="3",
        align="center",
        width="100%"
    )


# ==========================================
# 📋 PREVIEW MINIMAL DEL CAMBIO
# ==========================================

def medical_change_preview() -> rx.Component:
    """
    📋 Preview minimal del cambio - Sin información redundante

    Returns:
        Preview simple y profesional
    """

    return rx.cond(
        AppState.condicion_seleccionada_temp,
        rx.hstack(
            # Condición actual
            rx.vstack(
                rx.text(
                    "Actual",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["xs"],
                    color=MEDICAL_COLORS["medical_ui"]["text_muted"]
                ),
                rx.box(
                    style={
                        "width": "32px",
                        "height": "32px",
                        "background": get_dental_condition_color(
                            rx.cond(AppState.current_surface_condition, AppState.current_surface_condition, "sano"),
                            "light"
                        ),
                        "border": f"2px solid {get_dental_condition_color(rx.cond(AppState.current_surface_condition, AppState.current_surface_condition, 'sano'), 'base')}",
                        "border_radius": MEDICAL_RADIUS["sm"]
                    }
                ),
                spacing="1",
                align="center"
            ),

            # Flecha simple
            rx.icon(
                tag="arrow-right",
                size=20,
                color=MEDICAL_COLORS["medical_ui"]["text_muted"]
            ),

            # Nueva condición
            rx.vstack(
                rx.text(
                    "Nueva",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["xs"],
                    color=MEDICAL_COLORS["medical_ui"]["text_muted"]
                ),
                rx.box(
                    style={
                        "width": "32px",
                        "height": "32px",
                        "background": get_dental_condition_color(
                            AppState.condicion_seleccionada_temp,
                            "light"
                        ),
                        "border": f"2px solid {get_dental_condition_color(AppState.condicion_seleccionada_temp, 'base')}",
                        "border_radius": MEDICAL_RADIUS["sm"]
                    }
                ),
                spacing="1",
                align="center"
            ),

            spacing="4",
            align="center",
            justify="center",
            padding=MEDICAL_SPACING["md"],
            background=MEDICAL_COLORS["medical_ui"]["surface"],
            border_radius=MEDICAL_RADIUS["md"],
            border=f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}"
        ),
        rx.box()  # Vacío cuando no hay selección
    )


# ==========================================
# 🏥 MODAL PRINCIPAL MÉDICO PROFESIONAL
# ==========================================

def medical_condition_modal() -> rx.Component:
    """
    🏥 Modal principal médico profesional para seleccionar condiciones

    Características:
    - Diseño limpio sin glassmorphism excesivo
    - Animaciones sutiles 200ms ease-out
    - Grid compacto 80x80px
    - Preview minimal
    - Footer simple con 2 botones

    Returns:
        Modal médico profesional completo
    """

    return rx.cond(
        AppState.modal_condiciones_abierto,
        rx.box(
            # Overlay simple
            rx.box(
                # Container del modal
                rx.box(
                    # ===================================
                    # HEADER MÉDICO PROFESIONAL
                    # ===================================
                    rx.box(
                        rx.hstack(
                            # Título principal
                            rx.vstack(
                                rx.text(
                                    "Seleccionar Condición Dental",
                                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["xl"],
                                    font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["semibold"],
                                    color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                                ),
                                rx.text(
                                    f"Diente {AppState.diente_seleccionado} - Superficie {AppState.superficie_seleccionada}",
                                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                                ),
                                spacing="1",
                                align="start"
                            ),

                            rx.spacer(),

                            # Botón cerrar simple
                            rx.button(
                                rx.icon(tag="x", size=20),
                                size="2",
                                variant="ghost",
                                color_scheme="gray",
                                on_click=AppState.cerrar_modal_condiciones
                            ),

                            spacing="4",
                            align="center",
                            width="100%"
                        ),
                        padding=MEDICAL_SPACING["lg"],
                        border_bottom=f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}"
                    ),

                    # ===================================
                    # BODY DEL MODAL
                    # ===================================
                    rx.box(
                        rx.vstack(
                            # Filtros de categoría
                            medical_category_filters(),

                            # Preview del cambio
                            medical_change_preview(),

                            # Grid de condiciones
                            medical_conditions_grid("todas"),

                            spacing="4",
                            width="100%"
                        ),
                        padding=MEDICAL_SPACING["lg"],
                        max_height="60vh",
                        overflow_y="auto"
                    ),

                    # ===================================
                    # FOOTER SIMPLE
                    # ===================================
                    rx.box(
                        rx.hstack(
                            # Botón cancelar
                            rx.button(
                                "Cancelar",
                                size="3",
                                variant="outline",
                                color_scheme="gray",
                                on_click=AppState.cerrar_modal_condiciones
                            ),

                            rx.spacer(),

                            # Botón aplicar
                            rx.button(
                                rx.cond(
                                    AppState.odontograma_guardando,
                                    rx.hstack(
                                        rx.spinner(size="3"),
                                        rx.text("Aplicando..."),
                                        spacing="2"
                                    ),
                                    rx.text("Aplicar Cambio")
                                ),
                                size="3",
                                color_scheme="blue",
                                on_click=AppState.aplicar_condicion_seleccionada,
                                disabled=rx.cond(AppState.condicion_seleccionada_temp, False, True)
                            ),

                            spacing="3",
                            align="center",
                            width="100%"
                        ),
                        padding=MEDICAL_SPACING["lg"],
                        border_top=f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}"
                    ),

                    # Estilos del container
                    **medical_modal_container_style(),
                    width="700px",  # Ancho fijo profesional
                ),

                # Estilos del overlay
                **medical_modal_overlay_style()
            )
        )
    )


# ==========================================
# 🎯 EXPORTS
# ==========================================

__all__ = [
    "medical_condition_modal",
    "medical_condition_button",
    "medical_conditions_grid",
    "medical_category_filters",
    "medical_change_preview"
]