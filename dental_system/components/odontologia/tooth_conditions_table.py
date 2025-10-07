"""
📊 TABLA DE CONDICIONES DEL DIENTE
====================================

Muestra las condiciones actuales de cada superficie del diente seleccionado.
100% declarativo - Usa datos desde computed vars del Estado.

Características:
- Tabla compacta con 5 superficies
- Iconos de estado con colores
- Diseño médico profesional
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.medical_design_system import MEDICAL_COLORS

# ==========================================
# 📊 COMPONENTE TABLA DE CONDICIONES
# ==========================================

def tooth_conditions_table() -> rx.Component:
    """
    📊 Tabla de condiciones actuales del diente seleccionado

    Usa AppState.get_tooth_conditions_rows que retorna lista de dicts procesados:
    [
        {"superficie": "Oclusal", "estado": "Caries", "icon": "circle-alert", "color": "#E53E3E"},
        ...
    ]

    Returns:
        Tabla compacta con condiciones
    """

    return rx.box(
        # Header
        rx.hstack(
            rx.icon("clipboard-list", size=18, color=MEDICAL_COLORS["accent"]),
            rx.text(
                "Condiciones Actuales",
                font_weight="700",
                font_size="15px",
                color=MEDICAL_COLORS["text"]["primary"],
            ),
            spacing="2",
            margin_bottom="12px",
        ),

        # Tabla
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell(
                        "Superficie",
                        color=MEDICAL_COLORS["text"]["secondary"],
                        font_size="12px",
                        font_weight="600",
                    ),
                    rx.table.column_header_cell(
                        "Estado",
                        color=MEDICAL_COLORS["text"]["secondary"],
                        font_size="12px",
                        font_weight="600",
                    ),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    AppState.get_tooth_conditions_rows,
                    lambda row: rx.table.row(
                        # Superficie
                        rx.table.cell(
                            rx.text(
                                row["superficie"],
                                font_size="13px",
                                color=MEDICAL_COLORS["text"]["primary"],
                            ),
                        ),
                        # Estado con icono
                        rx.table.cell(
                            rx.hstack(
                                rx.icon(
                                    tag=row["icon"],
                                    size=14,
                                    color=row["color"],
                                ),
                                rx.text(
                                    row["estado"],
                                    font_size="13px",
                                    color=MEDICAL_COLORS["text"]["primary"],
                                ),
                                spacing="2",
                                align="center",
                            ),
                        ),
                    ),
                ),
            ),
            variant="surface",
            size="1",
            width="100%",
        ),

        # Estilos del contenedor
        padding="16px",
        background=MEDICAL_COLORS["surface"],
        border=f"1px solid {MEDICAL_COLORS['border']}",
        border_radius="8px",
        width="100%",
    )
