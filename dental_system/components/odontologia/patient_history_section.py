"""
📚 SECCIÓN DE HISTORIAL DEL PACIENTE
=====================================

Muestra el historial completo de servicios/intervenciones del paciente.
100% declarativo - Usa datos procesados desde estado.

Características:
- Lista de servicios históricos (uno por card)
- Filtrado automático por diente seleccionado
- Chip indicador de filtro activo
- Botón para limpiar filtro
- Estado de carga y mensaje vacío
- Scroll automático si hay muchos registros
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.history_service_card import history_service_card
from dental_system.styles.themes import (
    COLORS, DARK_THEME, SPACING, RADIUS, SHADOWS,
    dark_crystal_card, glassmorphism_card
)

# ==========================================
# 📚 COMPONENTE SECCIÓN DE HISTORIAL
# ==========================================

def patient_history_section() -> rx.Component:
    """
    📚 Sección completa de historial del paciente

    Muestra:
    - Header con título y filtro activo
    - Lista de cards de servicios históricos
    - Indicador de filtro por diente
    - Estado de carga
    - Mensaje vacío si no hay registros

    Returns:
        Sección completa con historial
    """

    return rx.box(
        # ==========================================
        # 📋 HEADER: Título + Filtro Activo
        # ==========================================
        rx.hstack(
            # Título + Descripción
            rx.vstack(
                rx.hstack(
                    rx.icon("history", size=20, color=COLORS["primary"]["400"]),
                    rx.text(
                        "Historial de Intervenciones",
                        font_weight="700",
                        font_size="16px",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    spacing="2",
                ),
                rx.text(
                    "Servicios previos realizados al paciente",
                    font_size="13px",
                    color=DARK_THEME["colors"]["text_secondary"],
                ),
                spacing="1",
                align="start",
            ),

            rx.spacer(),

            # Filtro activo (si hay)
            rx.cond(
                AppState.historial_filtrado_por_diente,
                rx.hstack(
                    rx.badge(
                        rx.hstack(
                            rx.icon("filter", size=14),
                            rx.text(
                                f"Diente {AppState.historial_filtrado_por_diente}",
                                font_size="12px",
                            ),
                            rx.text(
                                f"({AppState.nombre_diente_filtrado})",
                                font_size="11px",
                            ),
                            spacing="1",
                        ),
                        color_scheme="cyan",
                        variant="soft",
                        size="2",
                    ),
                    rx.button(
                        rx.icon("x", size=14),
                        on_click=AppState.limpiar_filtro_historial,
                        variant="ghost",
                        color_scheme="red",
                        size="1",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.box(),  # Placeholder vacío
            ),

            width="100%",
            align="center",
            margin_bottom="16px",
        ),

        # ==========================================
        # 📋 CONTENIDO: Cards de Historial
        # ==========================================
        rx.cond(
            AppState.historial_loading,
            # ⏳ ESTADO DE CARGA
            rx.box(
                rx.vstack(
                    rx.spinner(
                        size="3",
                        color=COLORS["primary"]["400"],
                    ),
                    rx.text(
                        "Cargando historial...",
                        font_size="13px",
                        color=DARK_THEME["colors"]["text_secondary"],
                    ),
                    spacing="3",
                    align="center",
                    padding_y="48px",
                ),
            ),
            # ✅ CONTENIDO CARGADO
            rx.cond(
                AppState.historial_filtrado,
                # HAY SERVICIOS - Mostrar lista
                rx.box(
                    # Estadísticas rápidas
                    rx.hstack(
                        rx.badge(
                            rx.hstack(
                                rx.icon("clipboard-list", size=14),
                                rx.text(
                                    f"{AppState.historial_filtrado.length()} servicios encontrados",
                                    font_size="12px",
                                ),
                                spacing="1",
                            ),
                            color_scheme="blue",
                            variant="soft",
                            size="1",
                        ),
                        rx.cond(
                            AppState.historial_filtrado_por_diente,
                            rx.text(
                                f"(Filtrados para diente {AppState.historial_filtrado_por_diente})",
                                font_size="11px",
                                color=DARK_THEME["colors"]["text_secondary"],
                            ),
                            rx.text(
                                "(Mostrando todos los servicios del paciente)",
                                font_size="11px",
                                color=DARK_THEME["colors"]["text_secondary"],
                            ),
                        ),
                        spacing="2",
                        align="center",
                        margin_bottom="12px",
                    ),

                    # Lista de cards con scroll
                    rx.box(
                        rx.foreach(
                            AppState.historial_filtrado,
                            history_service_card,
                        ),
                        max_height="600px",
                        overflow_y="auto",
                        overflow_x="hidden",
                        padding_right="8px",
                        # Custom scrollbar
                        style={
                            "&::-webkit-scrollbar": {
                                "width": "8px",
                            },
                            "&::-webkit-scrollbar-track": {
                                "background": DARK_THEME["colors"]["surface_secondary"],
                                "border_radius": "4px",
                            },
                            "&::-webkit-scrollbar-thumb": {
                                "background": f"{COLORS['primary']['500']}60",
                                "border_radius": "4px",
                            },
                            "&::-webkit-scrollbar-thumb:hover": {
                                "background": COLORS["primary"]["400"],
                            },
                        },
                    ),
                ),
                # NO HAY SERVICIOS - Mensaje vacío
                rx.box(
                    rx.vstack(
                        rx.icon(
                            "inbox",
                            size=48,
                            color=DARK_THEME["colors"]["text_muted"],
                        ),
                        rx.text(
                            rx.cond(
                                AppState.historial_filtrado_por_diente,
                                f"No hay servicios para el diente {AppState.historial_filtrado_por_diente}",
                                "No hay servicios en el historial",
                            ),
                            font_size="15px",
                            font_weight="600",
                            color=DARK_THEME["colors"]["text_secondary"],
                            text_align="center",
                        ),
                        rx.text(
                            rx.cond(
                                AppState.historial_filtrado_por_diente,
                                "Este diente no tiene intervenciones previas registradas",
                                "El paciente no tiene intervenciones previas registradas",
                            ),
                            font_size="13px",
                            color=DARK_THEME["colors"]["text_muted"],
                            text_align="center",
                        ),
                        rx.cond(
                            AppState.historial_filtrado_por_diente,
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", size=14),
                                    rx.text("Ver todo el historial", font_size="13px"),
                                    spacing="2",
                                ),
                                on_click=AppState.limpiar_filtro_historial,
                                variant="soft",
                                color_scheme="blue",
                                size="2",
                                margin_top="12px",
                            ),
                            rx.box(),  # Placeholder vacío
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
        ),

        # Estilos del contenedor
        style={
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="0px"),
            "padding": SPACING["6"]
        },
        width="100%",
        margin_y="4",
    )
