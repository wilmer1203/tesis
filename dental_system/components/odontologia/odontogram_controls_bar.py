"""
🎛️ BARRA DE CONTROLES DEL ODONTOGRAMA - VERSIÓN SIMPLIFICADA
=============================================================

DISEÑO: Barra superior minimalista con info del paciente y acción principal
COMPONENTES:
- Info del paciente actual (nombre + HC)
- Botón único: "Finalizar Intervención"
"""

import reflex as rx
from dental_system.styles.themes import COLORS, RADIUS, SPACING, dark_crystal_card


def odontogram_controls_bar(
    patient_name: str = "",
    patient_hc: str = "",
    show_timeline: bool = False,
    has_odontogram_changes: bool = False,
    has_selected_services: bool = False,
    is_saving: bool = False,
    on_save_intervention = None,
    on_export = None,
    on_print = None,
) -> rx.Component:
    """
    🎛️ BARRA DE CONTROLES SUPERIOR DEL ODONTOGRAMA V5.0 - SIMPLIFICADA

    Args:
        patient_name: Nombre completo del paciente
        patient_hc: Número de historia clínica
        has_selected_services: Si hay servicios seleccionados
        is_saving: Si está guardando actualmente
        on_save_intervention: Callback para finalizar intervención completa

    Returns:
        Barra de controles simplificada
    """

    return rx.box(
        rx.hstack(
            # Info del paciente (izquierda)
            rx.hstack(
                rx.icon("user", size=20, color=COLORS["primary"]["400"]),
                rx.vstack(
                    rx.text(
                        patient_name,
                        font_weight="700",
                        color=COLORS["gray"]["100"],
                        size="4",
                    ),
                    rx.cond(
                        patient_hc != "",
                        rx.text(
                            f"HC: {patient_hc}",
                            size="2",
                            color=COLORS["gray"]["400"],
                        ),
                        rx.text(
                            "Seleccione un paciente",
                            size="2",
                            color=COLORS["gray"]["500"],
                        ),
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),

            rx.spacer(),

            # Botón único: Finalizar Intervención (derecha)
            rx.cond(
                has_selected_services,
                rx.button(
                    rx.hstack(
                        rx.cond(
                            is_saving,
                            rx.spinner(size="2", color="white"),
                            rx.icon("circle-check", size=18, color="white"),
                        ),
                        rx.text(
                            rx.cond(
                                is_saving,
                                "Finalizando...",
                                "Finalizar Intervención"
                            ),
                            size="3",
                            weight="bold",
                            color="white"
                        ),
                        spacing="2",
                        align="center"
                    ),
                    on_click=on_save_intervention,
                    disabled=is_saving,
                    style={
                        "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['success']['600']} 100%)",
                        "border": "none",
                        "border_radius": RADIUS["xl"],
                        "padding": f"{SPACING['3']} {SPACING['5']}",
                        "cursor": "pointer",
                        "transition": "all 0.3s ease",
                        "_hover": {
                            "transform": "translateY(-2px)",
                            "box_shadow": f"0 8px 20px {COLORS['success']['500']}40"
                        },
                        "_active": {
                            "transform": "translateY(0)"
                        }
                    }
                ),
                # Mensaje cuando no hay servicios seleccionados
                rx.text(
                    "Seleccione servicios para finalizar",
                    size="2",
                    color=COLORS["gray"]["500"],
                    style={"font_style": "italic"}
                )
            ),

            # Estilos del contenedor
            width="100%",
            align="center",
        ),

        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="2px", padding=f"{SPACING['4']} {SPACING['5']}"),
        # padding=f"{SPACING['4']} {SPACING['5']}",
        margin_bottom=SPACING["5"],
        width="100%"
    )
