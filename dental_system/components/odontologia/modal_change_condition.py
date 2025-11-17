"""
MODAL CAMBIAR CONDICIÓN - VERSIÓN CON MODAL_WRAPPER
====================================================

Modal compacto para actualizar diagnóstico del diente sin agregar servicio.

Características:
- Usa modal_wrapper() para consistencia visual
- Tema oscuro del proyecto
- Checkboxes múltiples para superficies
- Grid 2 columnas para condiciones (ahorro de espacio)
- Diseño médico profesional
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, SPACING, RADIUS
from dental_system.components.common import modal_wrapper, primary_button, secondary_button
from dental_system.components.forms import form_section_header

# ==========================================
# CONDICIONES DENTALES (CORREGIDAS)
# ==========================================

CONDICIONES_DENTALES = {
    "sano": {
        "icon": "check-circle",
        "color": COLORS["success"]["500"],
        "label": "Sano"
    },
    "caries": {
        "icon": "alert-circle",
        "color": COLORS["error"]["500"],
        "label": "Caries"
    },
    "obturado": {
        "icon": "shield-check",
        "color": COLORS["info"]["500"],
        "label": "Obturado"
    },
    "corona": {
        "icon": "gem",
        "color": COLORS["warning"]["500"],
        "label": "Corona"
    },
    "endodoncia": {
        "icon": "zap",
        "color": COLORS["warning"]["500"],
        "label": "Endodoncia"
    },
    "ausente": {
        "icon": "x-circle",
        "color": COLORS["gray"]["500"],
        "label": "Ausente"
    },
    "fracturado": {
        "icon": "alert-triangle",
        "color": COLORS["error"]["600"],
        "label": "Fracturado"
    },
}


# ==========================================
# COMPONENTES AUXILIARES
# ==========================================

def _checkbox_superficie(label: str, surface_key: str, icon: str) -> rx.Component:
    """✅ Checkbox estilizado para superficies dentales"""
    is_checked = AppState.quick_surfaces_selected.contains(surface_key)

    return rx.box(
        rx.checkbox(
            rx.hstack(
                rx.icon(icon, size=14, color=COLORS["primary"]["400"]),
                rx.text(
                    label,
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "500",
                        "color": COLORS["gray"]["100"]
                    }
                ),
                spacing="2",
                align="center"
            ),
            checked=is_checked,
            on_change=lambda checked: AppState.toggle_quick_surface(surface_key),
            size="2"
        ),
        style={
            "padding": f"{SPACING['2']} {SPACING['3']}",
            "background": rx.cond(
                is_checked,
                f"{COLORS['primary']['500']}15",
                COLORS["gray"]["900"]
            ),
            "border": f"1px solid {rx.cond(is_checked, COLORS['primary']['400'], COLORS['gray']['700'])}",
            "border_radius": RADIUS["lg"],
            "transition": "all 200ms ease",
            "cursor": "pointer",
            "_hover": {
                "background": f"{COLORS['primary']['500']}10",
                "border_color": COLORS["primary"]["300"]
            }
        },
        flex="1"
    )


def condition_option(
    condition_key: str,
    icon: str,
    label: str,
    color: str,
) -> rx.Component:
    """Botón de selección de condición dental mejorado"""
    is_selected = AppState.quick_condition_value == condition_key

    return rx.button(
        rx.hstack(
            rx.icon(
                icon,
                size=16,
                color=rx.cond(is_selected, "white", color),
            ),
            rx.text(
                label,
                size="2",
                weight="bold",
                color=rx.cond(is_selected, "white", COLORS["gray"]["100"]),
            ),
            spacing="2",
            align="center",
        ),
        on_click=lambda: AppState.set_quick_condition(condition_key),
        style={
            "width": "100%",
            "padding": f"{SPACING['2']} {SPACING['3']}",
            "background": rx.cond(
                is_selected,
                f"linear-gradient(135deg, {color} 0%, {color}DD 100%)",
                "transparent"
            ),
            "border": rx.cond(
                is_selected,
                f"2px solid {color}",
                f"1px solid {COLORS['gray']['700']}"
            ),
            "border_radius": RADIUS["lg"],
            "cursor": "pointer",
            "transition": "all 0.3s ease",
            "_hover": {
                "border_color": color,
                "background": rx.cond(
                    is_selected,
                    f"linear-gradient(135deg, {color} 0%, {color}DD 100%)",
                    f"{color}10"
                ),
                "transform": "translateX(4px)"
            }
        }
    )


def modal_change_condition() -> rx.Component:
    """
    Modal compacto para cambiar condición del diente

    Actualiza solo el diagnóstico visual sin agregar servicios.
    Se vincula a la intervención actual para trazabilidad.

    Returns:
        Modal con selector de superficie y condición
    """

    # Contenido del modal
    modal_content = rx.vstack(
        # ========== SUPERFICIES MÚLTIPLES ==========
        rx.vstack(
            form_section_header(
                "Superficies Afectadas",
                "Selecciona una o más caras del diente",
                "layers",
                COLORS["blue"]["500"]
            ),

            # Botón: TODO EL DIENTE
            rx.button(
                rx.hstack(
                    rx.icon("circle-dot", size=18, color=COLORS["primary"]["400"]),
                    rx.text(
                        "TODO EL DIENTE",
                        size="3",
                        weight="bold",
                        color=COLORS["gray"]["100"]
                    ),
                    spacing="2"
                ),
                on_click=AppState.select_all_quick_surfaces,
                style={
                    "width": "100%",
                    "padding": f"{SPACING['3']} {SPACING['4']}",
                    "background": f"{COLORS['primary']['500']}20",
                    "border": f"2px dashed {COLORS['primary']['400']}",
                    "border_radius": RADIUS["lg"],
                    "cursor": "pointer",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "background": f"{COLORS['primary']['500']}30",
                        "transform": "scale(1.02)"
                    }
                }
            ),

            # Checkboxes individuales
            rx.vstack(
                # Fila 1: Oclusal, Mesial, Distal
                rx.hstack(
                    _checkbox_superficie("Oclusal", "oclusal", "circle"),
                    _checkbox_superficie("Mesial", "mesial", "arrow-left"),
                    _checkbox_superficie("Distal", "distal", "arrow-right"),
                    spacing="2",
                    width="100%"
                ),
                # Fila 2: Vestibular, Lingual
                rx.hstack(
                    _checkbox_superficie("Vestibular", "vestibular", "smile"),
                    _checkbox_superficie("Lingual", "lingual", "chevrons-down"),
                    spacing="2",
                    width="100%"
                ),
                spacing="2",
                width="100%"
            ),

            spacing="3",
            width="100%"
        ),

        # Separador
        rx.box(
            width="100%",
            height="1px",
            background=f"linear-gradient(90deg, transparent 0%, {COLORS['gray']['700']}80 50%, transparent 100%)",
            margin_y=SPACING["4"]
        ),

        # ========== CONDICIONES EN 2 COLUMNAS ==========
        rx.vstack(
            form_section_header(
                "Nueva Condición Dental",
                "Selecciona el diagnóstico del diente",
                "clipboard-list",
                COLORS["primary"]["500"]
            ),

            # SANO destacado (full-width arriba)
            condition_option(
                "sano",
                CONDICIONES_DENTALES["sano"]["icon"],
                CONDICIONES_DENTALES["sano"]["label"],
                CONDICIONES_DENTALES["sano"]["color"]
            ),

            # Grid 2 columnas para el resto
            rx.grid(
                # Columna 1
                rx.vstack(
                    condition_option("caries", CONDICIONES_DENTALES["caries"]["icon"],
                                   CONDICIONES_DENTALES["caries"]["label"],
                                   CONDICIONES_DENTALES["caries"]["color"]),
                    condition_option("obturado", CONDICIONES_DENTALES["obturado"]["icon"],
                                   CONDICIONES_DENTALES["obturado"]["label"],
                                   CONDICIONES_DENTALES["obturado"]["color"]),
                    condition_option("corona", CONDICIONES_DENTALES["corona"]["icon"],
                                   CONDICIONES_DENTALES["corona"]["label"],
                                   CONDICIONES_DENTALES["corona"]["color"]),
                    spacing="2",
                    width="100%"
                ),

                # Columna 2
                rx.vstack(
                    condition_option("endodoncia", CONDICIONES_DENTALES["endodoncia"]["icon"],
                                   CONDICIONES_DENTALES["endodoncia"]["label"],
                                   CONDICIONES_DENTALES["endodoncia"]["color"]),
                    condition_option("ausente", CONDICIONES_DENTALES["ausente"]["icon"],
                                   CONDICIONES_DENTALES["ausente"]["label"],
                                   CONDICIONES_DENTALES["ausente"]["color"]),
                    condition_option("fracturado", CONDICIONES_DENTALES["fracturado"]["icon"],
                                   CONDICIONES_DENTALES["fracturado"]["label"],
                                   CONDICIONES_DENTALES["fracturado"]["color"]),
                    spacing="2",
                    width="100%"
                ),

                columns="2",
                spacing="3",
                width="100%"
            ),

            spacing="3",
            width="100%"
        ),

        # Separador
        rx.box(
            width="100%",
            height="1px",
            background=f"linear-gradient(90deg, transparent 0%, {COLORS['gray']['700']}80 50%, transparent 100%)",
            margin_y=SPACING["4"]
        ),

        # Botones de acción
        rx.hstack(
            rx.dialog.close(
                secondary_button("Cancelar", icon="x")
            ),
            primary_button(
                "Guardar Cambio",
                icon="save",
                on_click=AppState.apply_quick_condition_change,
                disabled=~(AppState.quick_surfaces_selected.length() > 0) | ~AppState.quick_condition_value
            ),
            spacing="3",
            justify="end",
            width="100%"
        ),

        spacing="0",
        width="100%"
    )

    # Modal usando modal_wrapper
    return modal_wrapper(
        title=rx.cond(
            AppState.selected_tooth,
            f"Diente {AppState.selected_tooth}",
            "Actualizar Diagnóstico"
        ),
        subtitle="Cambiar condición dental sin agregar tratamiento",
        icon="stethoscope",
        color=COLORS["primary"]["500"],
        children=modal_content,
        is_open=AppState.show_change_condition_modal,
        on_open_change=AppState.toggle_change_condition_modal,
        max_width="520px",
        padding=SPACING["6"]
    )
