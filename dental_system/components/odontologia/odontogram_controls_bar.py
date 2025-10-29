"""
🎛️ BARRA DE CONTROLES DEL ODONTOGRAMA
======================================

DISEÑO: Barra superior con info del paciente y acciones
COMPONENTES:
- Info del paciente actual
- Botones de acción (Exportar, Imprimir)
- Toggle para mostrar/ocultar timeline
"""

import reflex as rx
from dental_system.styles.medical_design_system import DARK_COLORS


def odontogram_controls_bar(
    patient_name: str = "",
    patient_hc: str = "",
    show_timeline: bool = False,
    has_odontogram_changes: bool = False,
    has_selected_services: bool = False,
    is_saving: bool = False,
    on_save_diagnosis = None,
    on_save_intervention = None,
    on_export = None,
    on_print = None,
    on_toggle_timeline = None,
) -> rx.Component:
    """
    🎛️ BARRA DE CONTROLES SUPERIOR DEL ODONTOGRAMA V4.0

    Args:
        patient_name: Nombre completo del paciente
        patient_id: Número de historia clínica
        show_timeline: Si el timeline está visible
        has_odontogram_changes: Si hay cambios pendientes en odontograma
        has_selected_services: Si hay servicios seleccionados
        is_saving: Si está guardando actualmente
        on_save_diagnosis: Callback para guardar solo diagnóstico
        on_save_intervention: Callback para guardar intervención completa
        on_export: Callback para exportar PDF
        on_print: Callback para imprimir
        on_toggle_timeline: Callback para mostrar/ocultar timeline

    Returns:
        Barra de controles completa
    """

    return rx.hstack(
        # Info del paciente
        rx.hstack(
            rx.icon(tag="user", size=20, color=DARK_COLORS["accent_blue"]),
            rx.vstack(
                rx.text(
                    patient_name,  # Computed var ya retorna fallback
                    font_weight="600",
                    color=DARK_COLORS["foreground"],
                    font_size="15px",
                ),
                rx.cond(
                    patient_hc != "",
                    rx.text(
                        f"HC: {patient_hc}",
                        font_size="12px",
                        color=DARK_COLORS["text_secondary"],
                    ),
                    rx.text(
                        "Seleccione un paciente",
                        font_size="12px",
                        color=DARK_COLORS["text_secondary"],
                    ),
                ),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
        ),

        rx.spacer(),

        # Botones de acción
        rx.hstack(
            # NUEVO: Guardar solo diagnóstico
            rx.cond(
                has_odontogram_changes,
                rx.button(
                    rx.cond(
                        is_saving,
                        rx.spinner(size="1"),
                        rx.icon(tag="clipboard-check", size=16),
                    ),
                    "Guardar Diagnóstico",
                    variant="solid",
                    color_scheme="blue",
                    disabled=is_saving,
                    on_click=on_save_diagnosis,
                ),
            ),

            # NUEVO: Finalizar intervención completa
            rx.cond(
                has_selected_services,
                rx.button(
                    rx.cond(
                        is_saving,
                        rx.spinner(size="1"),
                        rx.icon(tag="circle-check", size=16),
                    ),
                    "Finalizar Intervención",
                    variant="solid",
                    color_scheme="green",
                    disabled=is_saving,
                    on_click=on_save_intervention,
                ),
            ),

            # Toggle timeline
            rx.button(
                rx.icon(tag="clock", size=16),
                rx.cond(
                    show_timeline,
                    "Ocultar Timeline",
                    "Timeline"
                ),
                variant=rx.cond(show_timeline, "solid", "outline"),
                color_scheme="cyan",
                on_click=on_toggle_timeline,
            ),

            # Exportar
            rx.button(
                rx.icon(tag="download", size=16),
                "Exportar",
                variant="outline",
                on_click=on_export,
            ),

            # Imprimir
            rx.button(
                rx.icon(tag="printer", size=16),
                "Imprimir",
                variant="outline",
                on_click=on_print,
            ),

            spacing="2",
        ),

        # Estilos del contenedor
        width="100%",
        padding="16px 20px",
        background=DARK_COLORS["card"],
        border=f"1px solid {DARK_COLORS['border']}",
        border_radius="12px",
        margin_bottom="20px",
        align="center",
    )
