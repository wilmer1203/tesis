"""
➕ MODAL AGREGAR INTERVENCIÓN COMPLETA - VERSIÓN ENTERPRISE
========================================

Modal para registrar una nueva intervención con:
- Selección de servicio
- Superficies tratadas
- Observaciones
- Cambio automático de condición
- Cálculo de costo

✨ Diseño consistente con el sistema enterprise del proyecto
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import modal_wrapper, primary_button, secondary_button
from dental_system.components.forms import enhanced_form_field, form_section_header
from dental_system.styles.themes import (
    COLORS, SHADOWS, RADIUS, SPACING, ANIMATIONS,
    GRADIENTS, GLASS_EFFECTS, DARK_THEME
)

# ==========================================
# ➕ MODAL AGREGAR INTERVENCIÓN
# ==========================================

def modal_add_intervention() -> rx.Component:
    """
    ➕ Modal para agregar nueva intervención completa

    Campos:
    - Servicio (dropdown)
    - Superficies tratadas (checkboxes)
    - Observaciones (textarea)
    - Cambiar condición automáticamente (checkbox + selector)
    - Costo calculado automáticamente

    Returns:
        Modal completo con formulario enterprise-level
    """

    return modal_wrapper(
        title=rx.cond(
            AppState.selected_tooth,
            f"Nueva Intervención - Diente {AppState.selected_tooth}",
            "Nueva Intervención"
        ),
        subtitle="Registra un servicio odontológico realizado en esta consulta",
        icon="plus-circle",
        color=COLORS["primary"]["500"],
        is_open=AppState.show_add_intervention_modal,
        on_open_change=AppState.toggle_add_intervention_modal,
        children=rx.vstack(
            rx.vstack(
                # Label
                rx.hstack(
                    rx.icon("stethoscope", size=18, color=COLORS["primary"]["500"]),
                    rx.text(
                        "Servicio / Procedimiento",
                        style={
                            "font_size": "1.3em",
                            "font_weight": "600",
                            "color": DARK_THEME["colors"]["text_primary"]
                        }
                    ),
                    rx.text(
                        "*",
                        style={
                            "color": COLORS["error"]["500"],
                            "font_weight": "700",
                            "margin_left": "2px"
                        }
                    ),
                    spacing="2",
                    align="center"
                ),

                # Select de servicio
                rx.select(
                    AppState.get_available_services_names,
                    value=AppState.selected_service_name,
                    on_change=AppState.set_selected_service_name,
                    placeholder="Seleccionar servicio...",
                    size="3",
                    width="100%",
                    style={
                        "background": DARK_THEME["colors"]["surface_secondary"],
                        "border": f"2px solid {DARK_THEME['colors']['border']}",
                        "border_radius": RADIUS["lg"],
                        "color": DARK_THEME["colors"]["text_primary"],
                        "transition": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)",
                        "_focus": {
                            "outline": "none",
                            "border_color": COLORS["primary"]["400"],
                            "box_shadow": f"0 0 0 3px {COLORS['primary']['200']}"
                        }
                    }
                ),

                # 🎯 Alcance del servicio (info dinámica)
                rx.cond(
                    AppState.selected_service_name != "",
                    rx.box(
                        rx.hstack(
                            rx.icon("info", size=14, color=COLORS["primary"]["400"]),
                            rx.text(
                                AppState.selected_service_alcance_display,
                                style={
                                    "font_size": "0.875rem",
                                    "color": DARK_THEME["colors"]["text_secondary"],
                                    "font_style": "italic"
                                }
                            ),
                            spacing="2",
                            align="center"
                        ),
                        style={
                            "padding": SPACING["3"],
                            "background": f"{COLORS['blue']['900']}35",
                            "border": f"1px solid {COLORS['primary']['400']}30",
                            "border_radius": RADIUS["lg"],
                            "margin_top": SPACING["2"]
                        }
                    ),
                    rx.box()
                ),

                spacing="2",
                width="100%"
            ),

            # 🦷 SUPERFICIES TRATADAS (solo si alcance es "superficie_especifica")
            rx.cond(
                AppState.selected_service_requiere_superficies,
                rx.vstack(
                    form_section_header(
                        "Superficies Tratadas",
                        "Selecciona las caras del diente afectadas",
                        "layers",
                        COLORS["blue"]["500"]
                    ),

                    rx.vstack(
                        # Fila 1: Oclusal, Mesial, Distal
                        rx.hstack(
                            _checkbox_superficie(
                                "Oclusal",
                                AppState.superficie_oclusal_selected,
                                AppState.toggle_superficie_oclusal,
                                "circle"
                            ),
                            _checkbox_superficie(
                                "Mesial",
                                AppState.superficie_mesial_selected,
                                AppState.toggle_superficie_mesial,
                                "arrow-left"
                            ),
                            _checkbox_superficie(
                                "Distal",
                                AppState.superficie_distal_selected,
                                AppState.toggle_superficie_distal,
                                "arrow-right"
                            ),
                            spacing="3",
                            width="100%",
                            wrap="wrap"
                        ),

                        # Fila 2: Vestibular, Lingual
                        rx.hstack(
                            _checkbox_superficie(
                                "Vestibular",
                                AppState.superficie_vestibular_selected,
                                AppState.toggle_superficie_vestibular,
                                "smile"
                            ),
                            _checkbox_superficie(
                                "Lingual",
                                AppState.superficie_lingual_selected,
                                AppState.toggle_superficie_lingual,
                                "chevrons-down"
                            ),
                            spacing="3",
                            width="100%",
                            wrap="wrap"
                        ),

                        spacing="3",
                        width="100%"
                    ),

                    spacing="4",
                    width="100%"
                ),
                rx.box()
            ),

            enhanced_form_field(
                label="Observaciones",
                field_name="intervention_observations",
                value=AppState.intervention_observations,
                on_change=lambda field, value: AppState.set_intervention_observations(value),
                field_type="textarea",
                placeholder="Detalles del procedimiento, hallazgos, recomendaciones...",
                required=False,
                icon="edit",
                help_text="Información adicional sobre el tratamiento realizado"
            ),

            # BOTONES DE ACCIÓN
            rx.hstack(
                rx.dialog.close(
                    secondary_button(
                        "Cancelar",
                        icon="x",
                        on_click=AppState.toggle_add_intervention_modal
                    )
                ),
                primary_button(
                    "Guardar Intervención",
                    icon="check",
                    on_click=AppState.save_intervention_to_consultation,
                    loading=False
                ),
                spacing="3",
                width="100%",
                justify="end",
                margin_top=SPACING["6"]
            ),

            spacing="6",
            width="100%"
        )
    )


def _checkbox_superficie(label: str, checked: bool, on_change: callable, icon: str) -> rx.Component:
    """✅ Checkbox estilizado para superficies dentales"""
    return rx.box(
        rx.checkbox(
            rx.hstack(
                rx.icon(icon, size=14, color=COLORS["primary"]["400"]),
                rx.text(
                    label,
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "500",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="2",
                align="center"
            ),
            checked=checked,
            on_change=on_change,
            size="2"
        ),
        style={
            "padding": f"{SPACING['2']} {SPACING['3']}",
            "background": rx.cond(
                checked,
                f"{COLORS['primary']['500']}15",
                DARK_THEME["colors"]["surface_secondary"]
            ),
            "border": f"1px solid {rx.cond(checked, COLORS['primary']['400'], DARK_THEME['colors']['border'])}",
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
