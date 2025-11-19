"""
📋 TABLA DE SERVICIOS DE CONSULTA ACTUAL
==========================================

Muestra todos los servicios/intervenciones agregados en la consulta actual.
100% declarativo - Usa datos procesados desde computed vars del Estado.

Características:
- Lista editable de servicios agregados HOY
- Columnas: Diente | Servicio | Superficies | Costo | Acciones
- Total acumulado de la consulta
- Botón para agregar nuevo servicio
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import (
    COLORS, DARK_THEME, SPACING, RADIUS, SHADOWS,
    dark_crystal_card, glassmorphism_card
)

# ==========================================
# 📊 COMPONENTE TABLA DE SERVICIOS
# ==========================================

def current_consultation_services_table() -> rx.Component:
    """
    📋 Tabla de servicios de la consulta actual

    Usa AppState.get_consultation_services_rows que retorna lista procesada:
    [
        {
            "id": "uuid",
            "diente": "16",
            "servicio": "Obturación",
            "superficies": "Oclusal, Mesial",
            "costo_bs": "250,000",
            "costo_usd": "6.85"
        },
        ...
    ]

    Returns:
        Tabla completa con servicios y acciones
    """

    return rx.box(
        # Header con título y botón agregar
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.icon("clipboard-list", size=20, color=COLORS["primary"]["400"]),
                    rx.text(
                        "Intervenciones de Esta Consulta",
                        font_weight="700",
                        font_size="16px",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    spacing="2",
                ),
                rx.text(
                    "Servicios realizados en esta atención",
                    font_size="13px",
                    color=DARK_THEME["colors"]["text_secondary"],
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=16),
                        rx.text("Agregar Servicio", font_size="14px"),
                        spacing="2",
                    ),
                    on_click=AppState.open_add_intervention_modal,
                    variant="soft",
                    color_scheme="cyan",
                    size="2",
                    disabled=~AppState.selected_tooth,
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("edit-3", size=16),
                        rx.text("Cambiar Condición", font_size="14px"),
                        spacing="2",
                    ),
                    on_click=AppState.toggle_change_condition_modal,
                    variant="soft",
                    color_scheme="blue",
                    size="2",
                    disabled=~AppState.selected_tooth,
                ),
                spacing="2",
            ),
            width="100%",
            align="center",
            margin_bottom="16px",
        ),

        # Tabla de servicios o mensaje vacío
        rx.cond(
            AppState.servicios_en_intervencion,
            # Hay servicios - mostrar tabla
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Diente", width="15%"),
                            rx.table.column_header_cell("Servicio", width="35%"),
                            rx.table.column_header_cell("Superficies", width="20%"),
                            rx.table.column_header_cell("Costo", width="20%"),
                            rx.table.column_header_cell("Acciones", width="10%"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            AppState.get_consultation_services_rows,
                            lambda service: rx.table.row(
                                # Diente
                                rx.table.cell(
                                    rx.badge(
                                        rx.cond(
                                            service['diente'] == "Boca completa",
                                            service['diente'],
                                            f"Diente {service['diente']}"
                                        ),
                                        color_scheme="cyan",
                                        variant="soft",
                                    ),
                                ),
                                # Servicio
                                rx.table.cell(
                                    rx.text(
                                        service["servicio"],
                                        font_size="13px",
                                        color=DARK_THEME["colors"]["text_primary"],
                                        font_weight="500",
                                    ),
                                ),
                                # Superficies
                                rx.table.cell(
                                    rx.text(
                                        service["superficies"],
                                        font_size="12px",
                                        color=DARK_THEME["colors"]["text_secondary"],
                                    ),
                                ),
                                # Costo
                                rx.table.cell(
                                    rx.vstack(
                                        rx.text(
                                            service["costo_bs"],
                                            font_size="13px",
                                            color=DARK_THEME["colors"]["text_primary"],
                                            font_weight="600",
                                        ),
                                        rx.text(
                                            service["costo_usd"],
                                            font_size="11px",
                                            color=DARK_THEME["colors"]["text_secondary"],
                                        ),
                                        spacing="0",
                                        align="end",
                                    ),
                                ),
                                # Acciones
                                rx.table.cell(
                                    rx.hstack(
                                        rx.icon_button(
                                            rx.icon("pencil", size=14),
                                            on_click=lambda sid=service["id"]: AppState.edit_consultation_service(sid),
                                            variant="ghost",
                                            size="1",
                                            color_scheme="blue",
                                        ),
                                        rx.icon_button(
                                            rx.icon("trash-2", size=14),
                                            on_click=lambda sid=service["id"]: AppState.delete_consultation_service(sid),
                                            variant="ghost",
                                            size="1",
                                            color_scheme="red",
                                        ),
                                        spacing="1",
                                    ),
                                ),
                            ),
                        ),
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                ),

                # Total
                rx.hstack(
                    rx.spacer(),
                    rx.vstack(
                        rx.text(
                            "TOTAL CONSULTA:",
                            font_size="12px",
                            font_weight="600",
                            color=DARK_THEME["colors"]["text_secondary"],
                            text_align="right",
                        ),
                        rx.hstack(
                            rx.text(
                                f"{AppState.total_intervencion_bs:,.0f} Bs",
                                font_size="18px",
                                font_weight="700",
                                color=COLORS["success"]["500"],
                            ),
                            rx.text(
                                f"/ ${AppState.total_intervencion_usd:.2f}",
                                font_size="14px",
                                font_weight="600",
                                color=DARK_THEME["colors"]["text_secondary"],
                            ),
                            spacing="2",
                        ),
                        spacing="0",
                        align="end",
                    ),
                    width="100%",
                    padding_top="12px",
                    padding_right="12px",
                ),
            ),
            # Sin servicios - mensaje vacío
            rx.box(
                rx.vstack(
                    rx.icon(
                        "inbox",
                        size=48,
                        color=DARK_THEME["colors"]["text_muted"],
                    ),
                    rx.text(
                        "No hay servicios agregados",
                        font_size="15px",
                        font_weight="600",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    rx.text(
                        "Haz clic en 'Agregar Servicio' para registrar una intervención",
                        font_size="13px",
                        color=DARK_THEME["colors"]["text_secondary"],
                        text_align="center",
                    ),
                    spacing="3",
                    align="center",
                    padding_y="48px",
                ),
                border=f"2px dashed {DARK_THEME['colors']['border']}",
                border_radius=RADIUS["lg"],
                style={
                    "background": f"rgba({DARK_THEME['colors']['surface']}, 0.3)",
                    "backdrop_filter": "blur(10px)"
                }
            ),
        ),

        # Estilos del contenedor
        style={
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="0px"),
            "padding": SPACING["6"]
        },
        width="100%",
        margin_y="4",
    )
