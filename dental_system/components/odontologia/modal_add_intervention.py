"""
➕ MODAL AGREGAR INTERVENCIÓN COMPLETA
========================================

Modal para registrar una nueva intervención con:
- Selección de servicio
- Superficies tratadas
- Observaciones
- Cambio automático de condición
- Cálculo de costo

Diseño médico profesional
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.medical_design_system import MEDICAL_COLORS

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
        Modal completo con formulario
    """

    return rx.dialog.root(
        rx.dialog.content(
            # Header
            rx.dialog.title(
                rx.hstack(
                    rx.icon("plus-circle", size=24, color=MEDICAL_COLORS["medical_ui"]["accent_primary"]),
                    rx.cond(
                        AppState.selected_tooth,
                        rx.text(
                            f"Nueva Intervención - Diente {AppState.selected_tooth}",
                            font_weight="700",
                            font_size="18px",
                        ),
                        rx.text(
                            "Nueva Intervención",
                            font_weight="700",
                            font_size="18px",
                        ),
                    ),
                    spacing="3",
                ),
            ),

            rx.dialog.description(
                "Registra un servicio odontológico realizado en esta consulta",
                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                margin_bottom="16px",
            ),

            # Formulario
            rx.vstack(
                # 📋 Servicio
                rx.vstack(
                    rx.text(
                        "📋 Servicio / Procedimiento",
                        font_weight="600",
                        font_size="14px",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    ),
                    rx.select(
                        AppState.get_available_services_names,
                        value=AppState.selected_service_name,
                        on_change=AppState.set_selected_service_name,
                        placeholder="Seleccionar servicio...",
                        size="3",
                        width="100%",
                    ),
                    # 🎯 Alcance del servicio (info dinámica)
                    rx.cond(
                        AppState.selected_service_name != "",
                        rx.box(
                            rx.text(
                                AppState.selected_service_alcance_display,
                                font_size="12px",
                                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                                font_style="italic",
                            ),
                            padding="8px",
                            background=f"{MEDICAL_COLORS['medical_ui']['accent_primary']}10",
                            border_radius="4px",
                            margin_top="4px",
                        ),
                    ),
                    spacing="2",
                    width="100%",
                ),

                # 🦷 Superficies tratadas (CONDICIONAL: solo si requiere superficies)
                rx.cond(
                    AppState.selected_service_requiere_superficies,
                    rx.vstack(
                    rx.text(
                        "🦷 Superficies tratadas",
                        font_weight="600",
                        font_size="14px",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    ),
                    rx.hstack(
                        rx.checkbox(
                            "Oclusal",
                            checked=AppState.superficie_oclusal_selected,
                            on_change=AppState.toggle_superficie_oclusal,
                        ),
                        rx.checkbox(
                            "Mesial",
                            checked=AppState.superficie_mesial_selected,
                            on_change=AppState.toggle_superficie_mesial,
                        ),
                        rx.checkbox(
                            "Distal",
                            checked=AppState.superficie_distal_selected,
                            on_change=AppState.toggle_superficie_distal,
                        ),
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.checkbox(
                            "Vestibular",
                            checked=AppState.superficie_vestibular_selected,
                            on_change=AppState.toggle_superficie_vestibular,
                        ),
                        rx.checkbox(
                            "Lingual",
                            checked=AppState.superficie_lingual_selected,
                            on_change=AppState.toggle_superficie_lingual,
                        ),
                        spacing="4",
                    ),
                        spacing="2",
                        width="100%",
                    ),
                ),  # Cierre del rx.cond para superficies

                # 🎨 Cambiar condición automáticamente (CONDICIONAL: solo si requiere diente)
                rx.cond(
                    AppState.selected_service_requiere_diente,
                    rx.vstack(
                    rx.checkbox(
                        "Cambiar condición del diente automáticamente",
                        checked=AppState.auto_change_condition,
                        on_change=AppState.toggle_auto_change_condition,
                        font_weight="600",
                        font_size="14px",
                    ),
                    rx.cond(
                        AppState.auto_change_condition,
                        rx.select(
                            [
                                "sano",
                                "caries",
                                "obturado",
                                "corona",
                                "endodoncia",
                                "ausente",
                                "por_extraer",
                                "fracturado",
                            ],
                            value=AppState.new_condition_value,
                            on_change=AppState.set_new_condition_value,
                            placeholder="Nueva condición...",
                            size="2",
                            width="100%",
                        ),
                    ),
                        spacing="2",
                        width="100%",
                    ),
                ),  # Cierre del rx.cond para cambiar condición

                # 💬 Observaciones
                rx.vstack(
                    rx.text(
                        "💬 Observaciones",
                        font_weight="600",
                        font_size="14px",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    ),
                    rx.text_area(
                        value=AppState.intervention_observations,
                        on_change=AppState.set_intervention_observations,
                        placeholder="Detalles del procedimiento, hallazgos, recomendaciones...",
                        rows="4",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),

                # 💰 Costo estimado
                rx.cond(
                    AppState.selected_service_cost_bs > 0,
                    rx.box(
                        rx.hstack(
                            rx.icon("dollar-sign", size=18, color=MEDICAL_COLORS["medical_ui"]["accent_primary"]),
                            rx.text(
                                "Costo estimado:",
                                font_weight="600",
                                font_size="14px",
                                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                            ),
                            rx.spacer(),
                            rx.vstack(
                                rx.text(
                                    f"{AppState.selected_service_cost_bs:,.0f} Bs",
                                    font_weight="700",
                                    font_size="16px",
                                    color=MEDICAL_COLORS["medical_ui"]["accent_primary"],
                                ),
                                rx.text(
                                    f"${AppState.selected_service_cost_usd:.2f}",
                                    font_size="13px",
                                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                                ),
                                spacing="0",
                                align="end",
                            ),
                            width="100%",
                            align="center",
                        ),
                        padding="12px",
                        background=f"{MEDICAL_COLORS["medical_ui"]['surface_overlay']}15",
                        border=f"1px solid {MEDICAL_COLORS["medical_ui"]['border_focus']}40",
                        border_radius="8px",
                    ),
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
                        rx.text("Guardar Intervención"),
                        spacing="2",
                    ),
                    on_click=AppState.save_intervention_to_consultation,
                    variant="solid",
                    color_scheme="cyan",
                    size="3",
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="20px",
            ),

            max_width="600px",
            padding="24px",
        ),
        open=AppState.show_add_intervention_modal,
        on_open_change=AppState.toggle_add_intervention_modal,
    )
