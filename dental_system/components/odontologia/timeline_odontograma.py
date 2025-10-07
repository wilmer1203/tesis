"""
📜 TIMELINE ODONTOGRAMA V3.0 - FASE 4
======================================

Componente visual que muestra el historial completo de versiones
del odontograma con timeline interactiva y comparación.

Features:
- Timeline vertical con indicadores de versión
- Cards por versión con información detallada
- Lista de cambios con badges de colores
- Botones para comparar versiones
- Filtros por fecha/odontólogo
"""

import reflex as rx
from typing import List, Dict, Any
from dental_system.state.estado_odontologia import EstadoOdontologia
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME


def cambio_badge_color(tipo_cambio: str) -> str:
    """
    🎨 Color según tipo de cambio

    Args:
        tipo_cambio: deterioro, mejora, modificacion, sin_cambio

    Returns:
        Color scheme para badge
    """
    colores = {
        "deterioro": "red",
        "mejora": "green",
        "modificacion": "blue",
        "sin_cambio": "gray"
    }
    return colores.get(tipo_cambio, "gray")


def version_badge(version_num: int, es_actual: bool) -> rx.Component:
    """
    🏷️ Badge de versión con estilo

    Args:
        version_num: Número de versión
        es_actual: Si es la versión actual

    Returns:
        Badge component
    """
    return rx.badge(
        f"v{version_num}",
        color_scheme="blue" if es_actual else "gray",
        size="2",
        variant="solid" if es_actual else "soft",
        style={
            "font_weight": "bold",
            "padding": "4px 12px"
        }
    )


def cambio_item(cambio: Dict[str, Any]) -> rx.Component:
    """
    📝 Item individual de cambio

    Args:
        cambio: Diccionario con información del cambio

    Returns:
        Component mostrando el cambio
    """
    return rx.hstack(
        rx.icon(
            "arrow-right",
            size=14,
            color=COLORS[cambio_badge_color(cambio["tipo_cambio"])]["500"]
        ),
        rx.text(
            f"Diente {cambio['diente']} {cambio['superficie']}:",
            size="2",
            weight="medium"
        ),
        rx.text(
            cambio["antes"],
            size="2",
            color="gray"
        ),
        rx.icon("arrow-right", size=12, color="gray"),
        rx.text(
            cambio["despues"],
            size="2",
            weight="medium",
            color=COLORS[cambio_badge_color(cambio["tipo_cambio"])]["500"]
        ),
        rx.badge(
            cambio["tipo_cambio"],
            color=cambio_badge_color(cambio["tipo_cambio"]),
            size="1"
        ),
        spacing="2",
        align="center"
    )


def version_card(version: Dict[str, Any], index: int) -> rx.Component:
    """
    📇 Card de versión individual en la timeline

    Args:
        version: Datos de la versión
        index: Índice en la lista

    Returns:
        Card component
    """
    return rx.box(
        rx.hstack(
            # Indicador de timeline
            rx.vstack(
                rx.box(
                    width="16px",
                    height="16px",
                    border_radius="50%",
                    background=COLORS["primary"]["500"] if version["es_version_actual"] else COLORS["gray"]["400"],
                    border=f"3px solid {DARK_THEME['colors']['background']}"
                ),
                rx.cond(
                    index < EstadoOdontologia.total_versiones_historial - 1,
                    rx.box(
                        width="2px",
                        height="100%",
                        background=COLORS["gray"]["400"],
                        min_height="80px"
                    ),
                    rx.fragment()
                ),
                align="center",
                spacing="0",
                width="16px"
            ),

            # Contenido del card
            rx.vstack(
                # Header
                rx.hstack(
                    version_badge(version["version"], version["es_version_actual"]),

                    rx.text(
                        f"· {version.get('odontologo_nombre', 'Desconocido')}",
                        size="2",
                        color=DARK_THEME["colors"]["text_secondary"]
                    ),

                    rx.spacer(),

                    rx.text(
                        version["fecha"][:10] if version.get("fecha") else "",
                        size="2",
                        color=DARK_THEME["colors"]["text_secondary"]
                    ),

                    align="center",
                    width="100%"
                ),

                # Motivo
                rx.text(
                    version.get("motivo", "Sin motivo especificado"),
                    size="3",
                    weight="medium",
                    color=DARK_THEME["colors"]["text_primary"]
                ),

                # Estadísticas
                rx.hstack(
                    rx.badge(
                        rx.icon("activity", size=12),
                        f"{version.get('total_dientes_afectados', 0)} dientes",
                        color_scheme="blue",
                        variant="soft",
                        size="1"
                    ),

                    rx.cond(
                        len(version.get("cambios_vs_anterior", [])) > 0,
                        rx.badge(
                            rx.icon("edit", size=12),
                            f"{len(version.get('cambios_vs_anterior', []))} cambios",
                            color_scheme="orange",
                            variant="soft",
                            size="1"
                        ),
                        rx.fragment()
                    ),

                    spacing="2"
                ),

                # Lista de cambios (si existen)
                rx.cond(
                    len(version.get("cambios_vs_anterior", [])) > 0,
                    rx.vstack(
                        rx.text(
                            "Cambios detectados:",
                            size="2",
                            weight="medium",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        rx.vstack(
                            rx.foreach(
                                version["cambios_vs_anterior"],
                                cambio_item
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        spacing="2",
                        padding="12px",
                        background=DARK_THEME["colors"]["surface"],
                        border_radius="6px",
                        width="100%"
                    ),
                    rx.fragment()
                ),

                # Botones de acción
                rx.hstack(
                    rx.button(
                        rx.icon("eye", size=14),
                        "Ver detalles",
                        on_click=lambda: EstadoOdontologia.ver_detalles_version(version["id"]),
                        size="2",
                        variant="soft"
                    ),

                    rx.cond(
                        len(version.get("cambios_vs_anterior", [])) > 0,
                        rx.button(
                            rx.icon("git-compare", size=14),
                            "Comparar",
                            on_click=lambda: EstadoOdontologia.comparar_con_anterior(version["id"]),
                            size="2",
                            variant="ghost"
                        ),
                        rx.fragment()
                    ),

                    spacing="2"
                ),

                spacing="3",
                align="start",
                width="100%"
            ),

            align="start",
            spacing="4",
            width="100%"
        ),

        padding="16px",
        border_radius="8px",
        background=DARK_THEME["colors"]["surface_elevated"],
        border=f"1px solid {DARK_THEME['colors']['border']}",
        width="100%",
        _hover={
            "border_color": COLORS["primary"]["500"]
        }
    )


def timeline_odontograma_versiones() -> rx.Component:
    """
    📜 FASE 4.2: Timeline visual completa de versiones del odontograma

    Features:
    - Timeline vertical con indicadores
    - Cards por versión con información detallada
    - Lista de cambios con colores
    - Botones de comparación
    - Scroll infinito optimizado

    Returns:
        Timeline component completo
    """
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading(
                "📚 Historial de Versiones",
                size="6",
                style={
                    # FIX: secondary['400'] no existe en themes.py, usar primary['500'] para gradiente
                    "background": f"linear-gradient(135deg, {COLORS['primary']['400']}, {COLORS['primary']['500']})",
                    "background_clip": "text",
                    "color": "transparent"
                }
            ),

            rx.spacer(),

            rx.badge(
                f"{EstadoOdontologia.total_versiones_historial} versiones",
                color_scheme="blue",
                size="2"
            ),

            align="center",
            width="100%"
        ),

        # TODO V3.0: Filtros temporalmente deshabilitados
        # Motivo: Reflex no permite setters personalizados en on_change desde substates
        # Alternativa: Usar lambda o acceder vía AppState
        # rx.hstack(
        #     rx.input(
        #         placeholder="Buscar por odontólogo...",
        #         on_change=lambda v: EstadoOdontologia.set_filtro_odontologo_historial(v),
        #         size="2",
        #         width="300px"
        #     ),
        #     rx.select(
        #         ["Todas", "Solo críticas", "Con cambios"],
        #         default_value="Todas",
        #         on_change=lambda v: EstadoOdontologia.set_filtro_tipo_version(v),
        #         size="2"
        #     ),
        #     spacing="3"
        # ),

        # Timeline con versiones
        rx.cond(
            EstadoOdontologia.historial_versiones_cargando,
            rx.center(
                rx.spinner(size="3"),
                padding="40px"
            ),
            rx.cond(
                EstadoOdontologia.total_versiones_historial > 0,
                rx.vstack(
                    rx.foreach(
                        EstadoOdontologia.historial_versiones_odontograma,
                        lambda version, index: version_card(version, index)
                    ),
                    spacing="0",
                    width="100%"
                ),
                rx.callout(
                    rx.icon("info"),
                    rx.text("No hay historial de versiones para este paciente"),
                    color_scheme="gray",
                    size="2"
                )
            )
        ),

        spacing="4",
        width="100%",
        padding="20px"
    )


def modal_historial_odontograma() -> rx.Component:
    """
    🗂️ Modal flotante con historial completo

    Returns:
        Modal dialog component
    """
    return rx.dialog.root(
        rx.dialog.content(
            timeline_odontograma_versiones(),

            style={
                "max_width": "900px",
                "max_height": "80vh",
                "overflow_y": "auto"
            }
        ),

        open=EstadoOdontologia.modal_historial_completo_abierto,
        on_open_change=EstadoOdontologia.set_modal_historial_completo_abierto
    )


def boton_ver_historial() -> rx.Component:
    """
    🔘 Botón flotante para abrir historial

    Returns:
        Button component
    """
    return rx.button(
        rx.icon("history", size=18),
        "Ver historial",
        on_click=AppState.abrir_modal_historial,
        size="3",
        variant="soft",
        color_scheme="blue"
    )
