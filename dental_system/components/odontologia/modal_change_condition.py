"""
MODAL CAMBIAR CONDICIÓN SIMPLE
===============================

Modal compacto para actualizar diagnóstico del diente sin agregar servicio.

Características:
- Selección rápida de superficie
- Condiciones médicas estándar
- Diseño médico minimalista
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, SPACING, RADIUS

# Condiciones médicas disponibles
CONDICIONES_DENTALES = {
    "sano": {"icon": "circle-check", "color": COLORS["success"]["500"], "label": "Sano"},
    "caries": {"icon": "alert-circle", "color": COLORS["error"]["700"], "label": "Caries"},
    "obturado": {"icon": "shield", "color": COLORS["info"]["500"], "label": "Obturado"},
    "corona": {"icon": "crown", "color": COLORS["secondary"]["500"], "label": "Corona"},
    "endodoncia": {"icon": "zap", "color": COLORS["warning"]["500"], "label": "Endodoncia"},
    "ausente": {"icon": "x-circle", "color": DARK_THEME["colors"]["text_muted"], "label": "Ausente"},
    "fracturado": {"icon": "alert-triangle", "color": "#EF4444", "label": "Fracturado"},
}

# ==========================================
# COMPONENTES DEL MODAL
# ==========================================

def condition_option(
    condition_key: str,
    icon: str,
    label: str,
    color: str,
) -> rx.Component:
    """Botón de selección de condición dental"""
    is_selected = AppState.quick_condition_value == condition_key

    return rx.button(
        rx.hstack(
            rx.icon(
                icon,
                size=18,
                color=rx.cond(is_selected, "white", color),
            ),
            rx.text(
                label,
                font_size="13px",
                font_weight="600",
                color=rx.cond(is_selected, "white", DARK_THEME["colors"]["text_primary"]),
            ),
            spacing="2",
            align="center",
        ),
        on_click=lambda: AppState.set_quick_condition(condition_key),
        variant=rx.cond(is_selected, "solid", "soft"),
        color_scheme=rx.cond(is_selected, "cyan", "gray"),
        size="2",
        width="100%",
        style={
            "cursor": "pointer",
            "border": rx.cond(
                is_selected,
                f"2px solid {COLORS['primary']['500']}",
                f"1px solid {DARK_THEME['colors']['border']}"
            ),
        },
    )


def modal_change_condition() -> rx.Component:
    """
    Modal compacto para cambiar condición del diente

    Actualiza solo el diagnóstico visual sin agregar servicios.
    Se vincula a la intervención actual para trazabilidad.

    Returns:
        Modal con selector de superficie y condición
    """

    return rx.dialog.root(
        rx.dialog.content(
            # Header
            rx.dialog.title(
                rx.hstack(
                    rx.icon("stethoscope", size=20, color=COLORS["primary"]["400"]),
                    rx.text(
                        rx.cond(
                            AppState.selected_tooth,
                            f"Actualizar Diagnóstico - Diente {AppState.selected_tooth}",
                            "Actualizar Diagnóstico"
                        ),
                        font_weight="700",
                        font_size="16px",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    spacing="2",
                ),
            ),

            rx.dialog.description(
                "Cambia el estado del diente sin agregar tratamiento",
                color=DARK_THEME["colors"]["text_secondary"],
                margin_bottom="20px",
                font_size="13px",
            ),

            # Formulario compacto
            rx.vstack(
                # Superficie
                rx.vstack(
                    rx.text(
                        "Superficie:",
                        font_weight="600",
                        font_size="13px",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    rx.select(
                        ["oclusal", "mesial", "distal", "vestibular", "lingual"],
                        value=AppState.quick_surface_selected,
                        on_change=AppState.set_quick_surface_selected,
                        placeholder="Seleccionar...",
                        size="2",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Condiciones
                rx.vstack(
                    rx.text(
                        "Nueva Condición:",
                        font_weight="600",
                        font_size="13px",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    rx.vstack(
                        condition_option("sano", CONDICIONES_DENTALES["sano"]["icon"],
                                       CONDICIONES_DENTALES["sano"]["label"],
                                       CONDICIONES_DENTALES["sano"]["color"]),
                        condition_option("caries", CONDICIONES_DENTALES["caries"]["icon"],
                                       CONDICIONES_DENTALES["caries"]["label"],
                                       CONDICIONES_DENTALES["caries"]["color"]),
                        condition_option("obturado", CONDICIONES_DENTALES["obturado"]["icon"],
                                       CONDICIONES_DENTALES["obturado"]["label"],
                                       CONDICIONES_DENTALES["obturado"]["color"]),
                        condition_option("corona", CONDICIONES_DENTALES["corona"]["icon"],
                                       CONDICIONES_DENTALES["corona"]["label"],
                                       CONDICIONES_DENTALES["corona"]["color"]),
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
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                spacing="4",
                width="100%",
            ),

            # Botones de acción
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        size="2",
                    ),
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("save", size=16),
                        rx.text("Guardar"),
                        spacing="2",
                    ),
                    on_click=AppState.apply_quick_condition_change,
                    variant="solid",
                    color_scheme="cyan",
                    size="2",
                    disabled=~(AppState.quick_surface_selected & AppState.quick_condition_value),
                ),
                spacing="2",
                justify="end",
                width="100%",
                margin_top="16px",
            ),

            max_width="420px",
            padding="20px",
        ),
        open=AppState.show_change_condition_modal,
        on_open_change=AppState.toggle_change_condition_modal,
    )
