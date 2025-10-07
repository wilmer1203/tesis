"""
📋 PANEL LATERAL DE DETALLES DEL DIENTE
========================================

DISEÑO: Inspirado en ToothDetailPanel.jsx de plantilla React
TABS: Solo 2 tabs → Historial | Info (SIN planificación, SIN costos)

FUNCIONALIDAD:
- Click en diente → Se abre este panel
- Tab Historial: Lista de intervenciones pasadas
- Tab Info: Condiciones actuales del diente
"""

import reflex as rx
from typing import List, Dict, Any
from dental_system.styles.medical_design_system import DARK_COLORS


def tab_button(label: str, icon: str, is_active: bool, badge_count: int = 0, on_click = None) -> rx.Component:
    """
    Botón de tab personalizado con badge opcional
    """
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon, size=16),
            rx.text(label, font_size="14px", font_weight="500"),
            rx.cond(
                badge_count > 0,
                rx.badge(
                    str(badge_count),
                    color_scheme=rx.cond(icon == "triangle-alert", "red", "blue"),
                    variant="solid",
                ),
            ),
            spacing="2",
            align="center",
        ),
        variant=rx.cond(is_active, "solid", "ghost"),
        color_scheme=rx.cond(is_active, "cyan", "gray"),
        width="100%",
        justify="start",
        on_click=on_click,
    )


def intervention_card(intervention: Dict[str, Any]) -> rx.Component:
    """
    📄 Tarjeta de intervención (SIN mostrar costos)

    Muestra:
    - Fecha y procedimiento
    - Dentista que la realizó
    - Notas clínicas
    """
    return rx.box(
        # Header de la intervención
        rx.hstack(
            rx.vstack(
                rx.text(
                    intervention.get("procedure", "Procedimiento"),
                    font_weight="600",
                    color=DARK_COLORS["foreground"],
                    font_size="15px",
                ),
                rx.text(
                    f"{intervention.get('date', '')} • {intervention.get('dentist', '')}",
                    font_size="13px",
                    color=DARK_COLORS["text_secondary"],
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            width="100%",
        ),

        # Notas clínicas
        rx.cond(
            intervention.get("notes", "") != "",
            rx.text(
                intervention.get("notes", ""),
                font_size="13px",
                color=DARK_COLORS["text_secondary"],
                margin_top="8px",
            ),
        ),

        # Estilos de la tarjeta
        padding="12px",
        background=DARK_COLORS["surface"],
        border=f"1px solid {DARK_COLORS['border']}",
        border_radius="8px",
        width="100%",
    )


def condition_badge(condition: str) -> rx.Component:
    """
    🚨 Badge de condición activa
    """
    return rx.hstack(
        rx.icon(tag="triangle-alert", size=18, color=DARK_COLORS["priority_urgent"]),
        rx.vstack(
            rx.text(
                condition,
                font_weight="600",
                color=DARK_COLORS["foreground"],
                font_size="14px",
            ),
            rx.text(
                "Fecha de detección",  # TODO V4.1: Agregar fecha real desde intervención
                font_size="12px",
                color=DARK_COLORS["text_secondary"],
            ),
            spacing="0",
            align="start",
        ),
        spacing="3",
        padding="12px",
        background=f"{DARK_COLORS['priority_urgent']}15",
        border_radius="8px",
        width="100%",
    )


def tooth_detail_sidebar(
    tooth_number: int = None,
    tooth_name: str = "",
    status: str = "Sano",
    active_tab: str = "historial",
    interventions: List[Dict[str, Any]] = None,
    conditions: List[str] = None,
    on_close = None,
    on_tab_change = None,
) -> rx.Component:
    """
    📋 PANEL LATERAL COMPLETO DE DETALLES DEL DIENTE

    Args:
        tooth_number: Número FDI del diente (11-48)
        tooth_name: Nombre completo en español
        status: Estado actual ("Sano", "Caries", etc.)
        active_tab: Tab activo ("historial" | "info")
        interventions: Lista de intervenciones pasadas
        conditions: Lista de condiciones activas
        on_close: Callback para cerrar el panel
        on_tab_change: Callback(tab_name) al cambiar de tab

    Returns:
        Panel lateral completo con tabs
    """

    # Defaults
    if interventions is None:
        interventions = []
    if conditions is None:
        conditions = []

    return rx.box(
        # Header del panel
        rx.hstack(
            rx.vstack(
                rx.heading(
                    f"Diente {tooth_number}",
                    size="5",
                    color=DARK_COLORS["foreground"],
                ),
                rx.text(
                    tooth_name,
                    font_size="13px",
                    color=DARK_COLORS["text_secondary"],
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                # Color del badge de estado (usando rx.cond anidado)
                rx.cond(
                    status == "Sano",
                    rx.badge(status, color_scheme="green", variant="solid"),
                    rx.cond(
                        status == "Caries",
                        rx.badge(status, color_scheme="red", variant="solid"),
                        rx.badge(status, color_scheme="blue", variant="solid"),
                    ),
                ),
                rx.icon_button(
                    rx.icon(tag="x", size=18),
                    size="2",
                    variant="ghost",
                    on_click=on_close,
                ),
                spacing="2",
            ),
            width="100%",
            padding_bottom="16px",
            border_bottom=f"1px solid {DARK_COLORS['border']}",
        ),

        # Tabs navigation
        rx.vstack(
            tab_button(
                label="Historial",
                icon="history",
                is_active=(active_tab == "historial"),
                on_click=on_tab_change("historial") if on_tab_change else lambda: None,
            ),
            tab_button(
                label="Información",
                icon="info",
                is_active=(active_tab == "info"),
                badge_count=conditions.length() if hasattr(conditions, 'length') else len(conditions),
                on_click=on_tab_change("info") if on_tab_change else lambda: None,
            ),
            spacing="2",
            width="100%",
            margin_top="16px",
            margin_bottom="16px",
        ),

        # Contenido según tab activo
        rx.box(
            # TAB: HISTORIAL
            rx.cond(
                active_tab == "historial",
                rx.vstack(
                    rx.cond(
                        interventions,  # Vars son truthy si no están vacías
                        rx.vstack(
                            # ✅ CORRECCIÓN: rx.foreach en lugar de list comprehension con *args
                            rx.foreach(interventions, intervention_card),
                            rx.button(
                                rx.icon(tag="plus", size=16),
                                "Agregar Intervención",
                                variant="outline",
                                width="100%",
                                margin_top="12px",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        # Sin intervenciones
                        rx.vstack(
                            rx.icon(tag="file-text", size=48, color=DARK_COLORS["text_secondary"]),
                            rx.text(
                                "No hay intervenciones registradas",
                                color=DARK_COLORS["text_secondary"],
                                font_size="14px",
                            ),
                            rx.button(
                                rx.icon(tag="plus", size=16),
                                "Agregar Primera Intervención",
                                variant="outline",
                                width="100%",
                                margin_top="12px",
                            ),
                            spacing="4",
                            align="center",
                            padding_y="32px",
                        ),
                    ),
                    width="100%",
                ),
            ),

            # TAB: INFO (Condiciones)
            rx.cond(
                active_tab == "info",
                rx.vstack(
                    rx.cond(
                        conditions,  # Vars son truthy si no están vacías
                        rx.vstack(
                            # ✅ CORRECCIÓN: rx.foreach en lugar de list comprehension con *args
                            rx.foreach(conditions, condition_badge),
                            spacing="3",
                            width="100%",
                        ),
                        # Sin condiciones
                        rx.vstack(
                            rx.icon(tag="circle-check", size=48, color=DARK_COLORS["accent_green"]),
                            rx.text(
                                "Sin condiciones detectadas",
                                color=DARK_COLORS["accent_green"],
                                font_weight="600",
                                font_size="15px",
                            ),
                            rx.text(
                                "Este diente está en buen estado",
                                color=DARK_COLORS["text_secondary"],
                                font_size="13px",
                            ),
                            spacing="3",
                            align="center",
                            padding_y="32px",
                        ),
                    ),
                    width="100%",
                ),
            ),

            width="100%",
            max_height="400px",
            overflow_y="auto",
        ),

        # Estilos del contenedor principal
        padding="20px",
        background=DARK_COLORS["card"],
        border=f"1px solid {DARK_COLORS['border']}",
        border_radius="12px",
        width="100%",
        max_width="350px",
    )


def empty_sidebar_placeholder() -> rx.Component:
    """
    📭 Placeholder cuando no hay diente seleccionado
    """
    return rx.box(
        rx.vstack(
            rx.icon(tag="mouse-pointer", size=48, color=DARK_COLORS["text_secondary"]),
            rx.heading(
                "Selecciona un Diente",
                size="5",
                color=DARK_COLORS["foreground"],
            ),
            rx.text(
                "Haz clic en cualquier diente del odontograma para ver su historial detallado",
                text_align="center",
                color=DARK_COLORS["text_secondary"],
                font_size="14px",
                max_width="250px",
            ),

            # Estadísticas rápidas
            rx.vstack(
                rx.box(
                    rx.text("Dientes Sanos", font_size="12px", color=DARK_COLORS["text_secondary"]),
                    rx.text("24", font_size="24px", font_weight="bold", color=DARK_COLORS["accent_green"]),
                    padding="12px",
                    background=DARK_COLORS["surface"],
                    border_radius="8px",
                    text_align="center",
                ),
                rx.box(
                    rx.text("Requieren Atención", font_size="12px", color=DARK_COLORS["text_secondary"]),
                    rx.text("6", font_size="24px", font_weight="bold", color=DARK_COLORS["accent_yellow"]),
                    padding="12px",
                    background=DARK_COLORS["surface"],
                    border_radius="8px",
                    text_align="center",
                ),
                rx.box(
                    rx.text("Urgentes", font_size="12px", color=DARK_COLORS["text_secondary"]),
                    rx.text("2", font_size="24px", font_weight="bold", color=DARK_COLORS["priority_urgent"]),
                    padding="12px",
                    background=DARK_COLORS["surface"],
                    border_radius="8px",
                    text_align="center",
                ),
                spacing="3",
                width="100%",
                margin_top="24px",
            ),

            spacing="5",
            align="center",
            padding_y="32px",
        ),
        padding="20px",
        background=DARK_COLORS["card"],
        border=f"1px solid {DARK_COLORS['border']}",
        border_radius="12px",
        width="100%",
        max_width="350px",
        text_align="center",
    )
