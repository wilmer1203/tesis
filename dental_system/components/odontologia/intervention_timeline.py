"""
⏱️ TIMELINE DE INTERVENCIONES PROFESIONAL
==========================================

DISEÑO: Inspirado en InterventionTimeline.jsx
CARACTERÍSTICAS:
- Timeline visual con cards de intervenciones
- Filtros por: diente, dentista, procedimiento, período
- SIN mostrar costos (solo información clínica)
- Estadísticas resumidas al final
"""

import reflex as rx
from typing import List, Dict, Any
from dental_system.styles.medical_design_system import DARK_COLORS


def filter_select(
    label: str,
    value: str,
    options: List[str],  # Solo strings, no tuplas
    on_change = None,
) -> rx.Component:
    """
    Selector de filtro personalizado
    """
    return rx.vstack(
        rx.text(
            label,
            font_size="12px",
            font_weight="500",
            color=DARK_COLORS["text_secondary"],
            margin_bottom="4px",
        ),
        rx.select(
            options,
            value=value,
            on_change=on_change,
            size="2",
            variant="soft",
        ),
        spacing="1",
        align="start",
        width="100%",
    )


def get_procedure_icon(procedure: str) -> str:
    """
    Obtener icono según tipo de procedimiento
    """
    procedure_lower = procedure.lower()
    if "limpieza" in procedure_lower:
        return "sparkles"
    elif "obturación" in procedure_lower or "resina" in procedure_lower:
        return "wrench"
    elif "corona" in procedure_lower:
        return "crown"
    elif "extracción" in procedure_lower:
        return "scissors"
    elif "endodoncia" in procedure_lower:
        return "zap"
    elif "diagnóstico" in procedure_lower:
        return "search"
    else:
        return "activity"


def intervention_timeline_card(intervention: Dict[str, Any], show_tooth_badge: bool = True) -> rx.Component:
    """
    📄 Card de intervención en timeline (SIN costos)

    Muestra:
    - Ícono de estado y procedimiento
    - Fecha, hora, dentista
    - Notas clínicas
    - Badge del diente (si show_tooth_badge=True)
    - Cambios realizados
    """
    return rx.box(
        # Timeline connector (línea vertical)
        rx.box(
            width="2px",
            height="100%",
            background=DARK_COLORS["border"],
            position="absolute",
            left="24px",
            top="48px",
        ),

        # Card content
        rx.hstack(
            # Ícono de estado
            rx.box(
                rx.icon(
                    tag="circle-check",
                    size=20,
                    color=DARK_COLORS["accent_green"],
                ),
                width="48px",
                height="48px",
                display="flex",
                align_items="center",
                justify_content="center",
                background=DARK_COLORS["background"],
                border=f"2px solid {DARK_COLORS['border']}",
                border_radius="50%",
                flex_shrink="0",
            ),

            # Contenido principal
            rx.vstack(
                # Header con procedimiento
                rx.hstack(
                    rx.icon(
                        tag="activity",  # Icono genérico para todos los procedimientos
                        size=16,
                        color=DARK_COLORS["accent_blue"],
                    ),
                    rx.text(
                        intervention.get("procedure", "Procedimiento"),
                        font_weight="600",
                        color=DARK_COLORS["foreground"],
                        font_size="15px",
                    ),
                    rx.cond(
                        show_tooth_badge,
                        rx.badge(
                            f"Diente {intervention.get('tooth', '')}",
                            color_scheme="cyan",
                            variant="soft",
                        ),
                    ),
                    spacing="2",
                    align="center",
                ),

                # Fecha y dentista
                rx.text(
                    f"{intervention.get('date', '')} • {intervention.get('time', '')} • {intervention.get('dentist', '')}",
                    font_size="13px",
                    color=DARK_COLORS["text_secondary"],
                ),

                # Notas clínicas
                rx.cond(
                    intervention.get("notes", "") != "",
                    rx.text(
                        intervention.get("notes", ""),
                        font_size="13px",
                        color=DARK_COLORS["foreground"],
                        margin_top="4px",
                    ),
                ),

                # TODO V4.1: Cambios realizados - requiere estructura de datos diferente
                # rx.foreach no puede iterar sobre intervention.get("changes", [])
                # Solución: Pasar 'changes' como campo directo del dict, no con .get()

                spacing="2",
                align="start",
                width="100%",
            ),

            spacing="4",
            width="100%",
            padding="12px",
            background=DARK_COLORS["surface"],
            border_radius="8px",
            cursor="pointer",
            _hover={"background": DARK_COLORS["surface_hover"]},
        ),

        position="relative",
        margin_bottom="16px",
    )


def intervention_timeline(
    selected_tooth: int = None,
    interventions: List[Dict[str, Any]] = None,
    dentists: List[str] = None,
    procedures: List[str] = None,
    total_count: int = 0,
    filter_dentist: str = "all",
    filter_procedure: str = "all",
    filter_period: str = "all",
    on_filter_change = None,
    on_intervention_click = None,
) -> rx.Component:
    """
    ⏱️ TIMELINE COMPLETA DE INTERVENCIONES V4.0

    Args:
        selected_tooth: Si se especifica, muestra solo intervenciones de ese diente
        interventions: Lista de intervenciones (ya filtradas)
        dentists: Lista de dentistas disponibles para filtros
        procedures: Lista de procedimientos disponibles para filtros
        total_count: Contador total de intervenciones
        filter_dentist: Filtro activo de dentista
        filter_procedure: Filtro activo de procedimiento
        filter_period: Filtro activo de período
        on_filter_change: Callback(filter_type, value) al cambiar filtros
        on_intervention_click: Callback(intervention) al hacer click en una intervención

    Returns:
        Panel completo de timeline con filtros y estadísticas
    """

    # Nota: Los valores None se manejan automáticamente por Reflex como listas vacías
    # No podemos usar if/else con Vars, así que eliminamos estas validaciones

    return rx.box(
        # Header con título y contador
        rx.hstack(
            rx.heading(
                rx.cond(
                    selected_tooth,
                    f"Historial - Diente {selected_tooth}",
                    "Línea de Tiempo de Intervenciones"
                ),
                size="5",
                color=DARK_COLORS["foreground"],
            ),
            rx.spacer(),
            # Contador de intervenciones
            rx.cond(
                total_count > 0,
                rx.text(
                    f"{total_count} intervenciones registradas",
                    font_size="14px",
                    color=DARK_COLORS["text_secondary"],
                ),
                rx.text(
                    "Sin intervenciones",
                    font_size="14px",
                    color=DARK_COLORS["text_secondary"],
                ),
            ),
            width="100%",
            margin_bottom="16px",
        ),

        # Filtros
        rx.hstack(
            filter_select(
                label="Dentista",
                value=filter_dentist,
                options=dentists,  # Ya incluye "Todos" desde computed var
                on_change=lambda val: on_filter_change("dentist", val),
            ),
            filter_select(
                label="Procedimiento",
                value=filter_procedure,
                options=procedures,  # Ya incluye "Todos" desde computed var
                on_change=lambda val: on_filter_change("procedure", val),
            ),
            filter_select(
                label="Período",
                value=filter_period,
                options=[
                    "Todo el historial",
                    "Últimos 7 días",
                    "Últimos 30 días",
                    "Últimos 90 días",
                ],
                on_change=lambda val: on_filter_change("period", val),
            ),
            spacing="4",
            width="100%",
            margin_bottom="24px",
        ),

        # Lista de intervenciones
        rx.box(
            rx.cond(
                interventions,  # Truthy check para Vars
                rx.foreach(
                    interventions,
                    lambda intervention: intervention_timeline_card(
                        intervention,
                        show_tooth_badge=(selected_tooth is None)
                    )
                ),
                # Sin intervenciones
                rx.vstack(
                    rx.icon(tag="clock", size=48, color=DARK_COLORS["text_secondary"]),
                    rx.heading(
                        "No hay intervenciones",
                        size="5",
                        color=DARK_COLORS["foreground"],
                    ),
                    # Mensaje dinámico usando rx.cond
                    rx.cond(
                        selected_tooth,
                        rx.text(
                            f"No se encontraron intervenciones para el diente {selected_tooth}",
                            text_align="center",
                            color=DARK_COLORS["text_secondary"],
                            font_size="14px",
                        ),
                        rx.text(
                            "No se encontraron intervenciones con los filtros aplicados",
                            text_align="center",
                            color=DARK_COLORS["text_secondary"],
                            font_size="14px",
                        ),
                    ),
                    rx.button(
                        "Limpiar Filtros",
                        variant="outline",
                        margin_top="16px",
                    ),
                    spacing="4",
                    align="center",
                    padding_y="48px",
                ),
            ),
            max_height="400px",
            overflow_y="auto",
            padding="4px",
        ),

        # Estadísticas resumidas (SIN costos)
        # NOTA: Las estadísticas con len() y list comprehensions sobre Vars
        # deben calcularse como computed vars en el Estado, no aquí en el componente
        rx.cond(
            interventions,  # Truthy check
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            total_count,  # Usar total_count en vez de interventions.length()
                            font_size="24px",
                            font_weight="bold",
                            color=DARK_COLORS["foreground"],
                        ),
                        rx.text(
                            "Intervenciones",
                            font_size="12px",
                            color=DARK_COLORS["text_secondary"],
                        ),
                        spacing="0",
                        align="center",
                    ),
                    rx.vstack(
                        rx.text(
                            # TODO V4.1: Crear computed var `unique_dentists_count` en Estado
                            "N/A",  # Placeholder hasta computed var
                            font_size="24px",
                            font_weight="bold",
                            color=DARK_COLORS["foreground"],
                        ),
                        rx.text(
                            "Dentistas",
                            font_size="12px",
                            color=DARK_COLORS["text_secondary"],
                        ),
                        spacing="0",
                        align="center",
                    ),
                    rx.vstack(
                        rx.text(
                            # TODO V4.1: Crear computed var `unique_teeth_count` en Estado
                            "N/A",  # Placeholder hasta computed var
                            font_size="24px",
                            font_weight="bold",
                            color=DARK_COLORS["foreground"],
                        ),
                        rx.text(
                            "Dientes Tratados",
                            font_size="12px",
                            color=DARK_COLORS["text_secondary"],
                        ),
                        spacing="0",
                        align="center",
                    ),
                    spacing="8",
                    justify="center",
                    width="100%",
                ),
                padding="16px",
                background=f"{DARK_COLORS['surface']}80",
                border_top=f"1px solid {DARK_COLORS['border']}",
                margin_top="24px",
            ),
        ),

        # Estilos del contenedor
        padding="20px",
        background=DARK_COLORS["card"],
        border=f"1px solid {DARK_COLORS['border']}",
        border_radius="12px",
        width="100%",
    )
