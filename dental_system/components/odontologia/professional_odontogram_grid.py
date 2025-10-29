"""
🦷 GRID PROFESIONAL DE ODONTOGRAMA - 32 DIENTES FDI
===================================================

DISEÑO: Inspirado en plantilla React professional-odontogram-viewer
LAYOUT: 4 cuadrantes estándar FDI + Leyenda lateral

ESTRUCTURA:
┌─────────────────────────────────────┐
│  18 17 16 15 14 13 12 11 │ 21 22 23 24 25 26 27 28  │
│  ─────────────────────────┼─────────────────────────  │
│  48 47 46 45 44 43 42 41 │ 31 32 33 34 35 36 37 38  │
└─────────────────────────────────────┘
"""

import reflex as rx
from typing import List, Dict, Any
from dental_system.components.odontologia.simple_tooth import (
    tooth_with_tooltip,
    TOOTH_NAMES,
    get_tooth_color,
)
from dental_system.styles.medical_design_system import DARK_COLORS


# Organización de dientes por cuadrantes FDI
ADULT_TEETH_FDI = {
    "upper_right": [18, 17, 16, 15, 14, 13, 12, 11],
    "upper_left": [21, 22, 23, 24, 25, 26, 27, 28],
    "lower_left": [31, 32, 33, 34, 35, 36, 37, 38],
    "lower_right": [48, 47, 46, 45, 44, 43, 42, 41],
}


def odontogram_legend() -> rx.Component:
    """
    📋 Leyenda de colores del odontograma

    Muestra todos los estados posibles con sus colores
    """
    legend_items = [
        ("sano", "Sano"),
        ("caries", "Caries"),
        ("obturado", "Obturado"),
        ("corona", "Corona"),
        ("endodoncia", "Endodoncia"),
        ("ausente", "Ausente"),
        ("fractura", "Fractura"),
        ("implante", "Implante"),
    ]

    return rx.box(
        rx.heading(
            "Leyenda",
            size="4",
            color=DARK_COLORS["foreground"],
            margin_bottom="12px",
        ),
        rx.vstack(
            *[
                rx.hstack(
                    rx.box(
                        width="20px",
                        height="20px",
                        background=get_tooth_color(status),
                        border_radius="4px",
                        border=f"2px solid {DARK_COLORS['border']}",
                    ),
                    rx.text(
                        label,
                        font_size="13px",
                        color=DARK_COLORS["text_secondary"],
                    ),
                    spacing="2",
                    align="center",
                )
                for status, label in legend_items
            ],
            spacing="3",
            align="start",
        ),
        padding="16px",
        background=DARK_COLORS["surface"],
        border=f"1px solid {DARK_COLORS['border']}",
        border_radius="8px",
    )


def professional_odontogram_grid(
    selected_tooth: int = None,
    teeth_data: Dict[int, Dict[str, Any]] = {},
    on_tooth_click = None,
) -> rx.Component:
    """
    🦷 GRID COMPLETO DE ODONTOGRAMA PROFESIONAL

    Args:
        selected_tooth: Número del diente seleccionado (resaltado)
        teeth_data: Diccionario con data de cada diente
            Ejemplo: {
                12: {"status": "caries", "has_conditions": True},
                16: {"status": "endodoncia", "has_conditions": False},
            }
        on_tooth_click: Callback(tooth_number) al hacer click en un diente

    Returns:
        Grid completo con 32 dientes + leyenda lateral
    """


    def render_quadrant(tooth_numbers: List[int], reverse: bool = False) -> rx.Component:
        """Renderizar un cuadrante de 8 dientes"""
        # Aplicar reverse antes de iterar
        teeth_list = tooth_numbers[::-1] if reverse else tooth_numbers

        
        return rx.hstack(
            *[
                tooth_with_tooltip(
                    tooth_number=tooth_num,
                    tooth_name=TOOTH_NAMES.get(tooth_num, f"Diente {tooth_num}"),
                    status=teeth_data.get(tooth_num, {}).get("status", "sano"),
                    has_conditions=teeth_data.get(tooth_num, {}).get("has_conditions", False),
                    is_selected=(tooth_num == selected_tooth),
                    on_click=(lambda t=tooth_num: lambda: on_tooth_click(t))() if on_tooth_click else lambda: None,
                )
                for tooth_num in teeth_list
            ],
            spacing="2",
            justify="center",
        )

    return rx.box(
        # Header del odontograma
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Odontograma Digital",
                    size="6",
                    color=DARK_COLORS["foreground"],
                ),
                rx.text(
                    "Sistema FDI - 32 Dientes Permanentes",
                    font_size="14px",
                    color=DARK_COLORS["text_secondary"],
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.badge(
                "Actualizado",
                color_scheme="green",
            ),
            width="100%",
            margin_bottom="24px",
            align="center",
        ),

        # Grid principal: Odontograma (70%) + Leyenda (30%)
        rx.hstack(
            # Odontograma central
            rx.vstack(
                # Maxilar superior (cuadrantes 1 y 2)
                rx.hstack(
                    render_quadrant(ADULT_TEETH_FDI["upper_right"], reverse=True),
                    rx.box(width="2px", height="48px", background=DARK_COLORS["border"]),
                    render_quadrant(ADULT_TEETH_FDI["upper_left"]),
                    spacing="4",
                    justify="center",
                ),

                # Separador horizontal
                rx.box(
                    height="2px",
                    width="100%",
                    background=DARK_COLORS["border"],
                    margin_y="12px",
                ),

                # Maxilar inferior (cuadrantes 3 y 4)
                rx.hstack(
                    render_quadrant(ADULT_TEETH_FDI["lower_right"], reverse=True),
                    rx.box(width="2px", height="48px", background=DARK_COLORS["border"]),
                    render_quadrant(ADULT_TEETH_FDI["lower_left"]),
                    spacing="4",
                    justify="center",
                ),

                spacing="4",
                align="center",
                padding="24px",
                background=DARK_COLORS["background"],
                border=f"1px solid {DARK_COLORS['border']}",
                border_radius="12px",
                width="70%",
            ),

            # Leyenda lateral
            odontogram_legend(),

            spacing="6",
            align="start",
            width="100%",
        ),

        # Instrucciones
        rx.box(
            rx.hstack(
                rx.icon(tag="info", size=16, color=DARK_COLORS["accent_blue"]),
                rx.text(
                    "Haz clic en cualquier diente para ver su historial y detalles completos",
                    font_size="13px",
                    color=DARK_COLORS["text_secondary"],
                ),
                spacing="2",
                align="center",
            ),
            margin_top="16px",
            padding="12px",
            background=f"{DARK_COLORS['accent_blue']}15",
            border_radius="8px",
        ),

        # Estilos del contenedor principal
        padding="20px",
        width="100%",
    )
