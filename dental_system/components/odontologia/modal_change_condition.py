"""
🔄 MODAL CAMBIAR CONDICIÓN SIMPLE
==================================

Modal simplificado para cambiar solo la condición visual del diente
sin registrar intervención médica completa.

Características:
- Selección de superficie
- Selección de condición
- Guardado rápido
- Diseño médico minimalista
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.medical_design_system import DARK_COLORS,MEDICAL_COLORS

# Condiciones médicas disponibles
MEDICAL_CONDITIONS = {
    "sano": {"icon": "circle-check", "color": "#48BB78", "label": "Sano"},
    "caries": {"icon": "circle-alert", "color": "#E53E3E", "label": "Caries"},
    "obturado": {"icon": "shield", "color": "#4299E1", "label": "Obturado"},
    "corona": {"icon": "crown", "color": "#9F7AEA", "label": "Corona"},
    "endodoncia": {"icon": "zap", "color": "#ED8936", "label": "Endodoncia"},
    "ausente": {"icon": "x-circle", "color": "#A0AEC0", "label": "Ausente"},
    "por_extraer": {"icon": "scissors", "color": "#F59E0B", "label": "Por Extraer"},
    "fracturado": {"icon": "triangle-alert", "color": "#EF4444", "label": "Fracturado"},
}

# ==========================================
# 🔄 MODAL CAMBIAR CONDICIÓN
# ==========================================

def condition_button(
    icon: str,
    label: str,
    condition_key: str,
    color: str,
) -> rx.Component:
    """Botón de condición médica"""
    is_selected = AppState.quick_condition_value == condition_key

    return rx.button(
        rx.vstack(
            rx.icon(icon, size=24, color=color),
            rx.text(
                label,
                font_size="12px",
                font_weight="600",
                color=rx.cond(
                    is_selected,
                    "white",
                    MEDICAL_COLORS["medical_ui"]["text_primary"]
                ),
            ),
            spacing="1",
            align="center",
        ),
        on_click=lambda: AppState.set_quick_condition(condition_key),
        variant="soft",
        size="3",
        width="120px",
        height="80px",
        background=rx.cond(
            is_selected,
            color,
            f"{color}15"
        ),
        style={
            "border": f"2px solid {color}",
        },
    )


def modal_change_condition() -> rx.Component:
    """
    🔄 Modal para cambiar condición simple del diente

    Flujo:
    1. Seleccionar superficie (si no está seleccionada)
    2. Seleccionar condición
    3. Guardar cambio

    Returns:
        Modal compacto con selector de condición
    """

    return rx.dialog.root(
        rx.dialog.content(
            # Header
            rx.dialog.title(
                rx.hstack(
                    rx.icon("refresh-cw", size=22, color=MEDICAL_COLORS["medical_ui"]["accent_primary"]),
                    rx.cond(
                        AppState.selected_tooth,
                        rx.text(
                            f"Cambiar Condición - Diente {AppState.selected_tooth}",
                            font_weight="700",
                            font_size="17px",
                        ),
                        rx.text(
                            "Cambiar Condición",
                            font_weight="700",
                            font_size="17px",
                        ),
                    ),
                    spacing="2",
                ),
            ),

            rx.dialog.description(
                "Actualiza el estado visual del diente sin registrar intervención",
                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                margin_bottom="16px",
                font_size="13px",
            ),

            # Formulario
            rx.vstack(
                # 🦷 Superficie
                rx.vstack(
                    rx.text(
                        "🦷 Superficie:",
                        font_weight="600",
                        font_size="14px",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    ),
                    rx.select(
                        ["oclusal", "mesial", "distal", "vestibular", "lingual"],
                        value=AppState.quick_surface_selected,
                        on_change=AppState.set_quick_surface_selected,
                        placeholder="Seleccionar superficie...",
                        size="3",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),

                # 🎨 Condiciones disponibles
                rx.vstack(
                    rx.text(
                        "🎨 Nueva Condición:",
                        font_weight="600",
                        font_size="14px",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    ),
                    # Fila 1
                    rx.hstack(
                        condition_button(
                            "circle-check",
                            "Sano",
                            "sano",
                            MEDICAL_CONDITIONS["sano"]["color"],
                        ),
                        condition_button(
                            "circle-alert",
                            "Caries",
                            "caries",
                            MEDICAL_CONDITIONS["caries"]["color"],
                        ),
                        condition_button(
                            "shield",
                            "Obturado",
                            "obturado",
                            MEDICAL_CONDITIONS["obturado"]["color"],
                        ),
                        spacing="3",
                        width="100%",
                        justify="center",
                    ),
                    # Fila 2
                    rx.hstack(
                        condition_button(
                            "crown",
                            "Corona",
                            "corona",
                            MEDICAL_CONDITIONS["corona"]["color"],
                        ),
                        condition_button(
                            "zap",
                            "Endodoncia",
                            "endodoncia",
                            MEDICAL_CONDITIONS["endodoncia"]["color"],
                        ),
                        condition_button(
                            "x-circle",
                            "Ausente",
                            "ausente",
                            MEDICAL_CONDITIONS["ausente"]["color"],
                        ),
                        spacing="3",
                        width="100%",
                        justify="center",
                    ),
                    # Fila 3
                    rx.hstack(
                        condition_button(
                            "scissors",
                            "Por Extraer",
                            "por_extraer",
                            "#F59E0B",  # Amber
                        ),
                        condition_button(
                            "triangle-alert",
                            "Fracturado",
                            "fracturado",
                            "#EF4444",  # Red
                        ),
                        spacing="3",
                        width="100%",
                        justify="center",
                    ),
                    spacing="3",
                    width="100%",
                ),

                spacing="5",
                width="100%",
            ),

            # Botones de acción
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        size="3",
                    ),
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("check", size=16),
                        rx.text("Aplicar Cambio"),
                        spacing="2",
                    ),
                    on_click=AppState.apply_quick_condition_change,
                    variant="solid",
                    color_scheme="cyan",
                    size="3",
                    disabled=~(AppState.quick_surface_selected & AppState.quick_condition_value),
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="20px",
            ),

            max_width="500px",
            padding="24px",
        ),
        open=AppState.show_change_condition_modal,
        on_open_change=AppState.toggle_change_condition_modal,
    )
