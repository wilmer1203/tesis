"""
📋 PANEL DE INTERVENCIONES PREVIAS - MÚLTIPLES ODONTÓLOGOS
===========================================================

Componente para mostrar el historial de intervenciones realizadas
por otros odontólogos en la misma consulta.

Funcionalidades:
- Lista de intervenciones previas con odontólogo
- Servicios realizados por cada uno
- Costos por intervención
- Fechas y horas de atención
- Estado de cada intervención
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.models import IntervencionModel
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,
    dark_crystal_card
)

# ==========================================
# 🎨 ESTILOS PARA EL PANEL
# ==========================================

PANEL_STYLE = {
    "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
    "border": f"1px solid {DARK_THEME['colors']['border']}",
    "border_radius": RADIUS["xl"],
    "padding": SPACING["6"],
    "backdrop_filter": "blur(10px)",
    "box_shadow": SHADOWS["lg"]
}

INTERVENCION_CARD_STYLE = {
    "background": DARK_THEME["colors"]["surface"],
    "border": f"1px solid {DARK_THEME['colors']['border']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "margin_bottom": SPACING["3"],
    "transition": "all 0.3s ease",
    "_hover": {
        "transform": "translateY(-2px)",
        "box_shadow": f"0 4px 12px {COLORS['primary']['500']}20",
        "border_color": f"{COLORS['primary']['500']}40"
    }
}

# ==========================================
# 📋 COMPONENTES DEL PANEL
# ==========================================

def intervencion_previa_card(intervencion: rx.Var[IntervencionModel]) -> rx.Component:
    """
    🦷 Card individual de intervención previa

    Muestra:
    - Nombre del odontólogo
    - Fecha y hora de atención
    - Servicios realizados
    - Costos (BS/USD)
    - Estado de la intervención
    """
    return rx.box(
        rx.vstack(
            # Header con odontólogo y fecha
            rx.hstack(
                # Info del odontólogo
                rx.vstack(
                    rx.hstack(
                        rx.icon("user-round", size=16, color=COLORS["primary"]["400"]),
                        rx.text(
                            intervencion.odontologo_nombre,
                            font_weight="700",
                            font_size="1rem",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),
                        spacing="2",
                        align="center"
                    ),
                    # Especialidad con rx.cond (NO usar 'or')
                    rx.text(
                        rx.cond(
                            intervencion.odontologo_especialidad != "",
                            f"Especialidad: {intervencion.odontologo_especialidad}",
                            "Especialidad: Odontología General"
                        ),
                        font_size="0.85rem",
                        color=DARK_THEME["colors"]["text_secondary"]
                    ),
                    spacing="1",
                    align_items="start"
                ),

                rx.spacer(),

                # Fecha y hora
                rx.vstack(
                    rx.text(
                        intervencion.fecha_display,
                        font_weight="600",
                        font_size="0.85rem",
                        color=COLORS["blue"]["500"]
                    ),
                    rx.text(
                        intervencion.hora_display,
                        font_size="0.75rem",
                        color=DARK_THEME["colors"]["text_muted"]
                    ),
                    spacing="1",
                    align_items="end"
                ),

                width="100%",
                align="center"
            ),

            # Divider
            rx.divider(
                border_color=DARK_THEME["colors"]["border"],
                margin=f"{SPACING['3']} 0"
            ),

            # Servicios realizados
            rx.vstack(
                rx.text(
                    "📋 Servicios Realizados:",
                    font_weight="600",
                    font_size="0.9rem",
                    color=DARK_THEME["colors"]["text_primary"],
                    margin_bottom=SPACING["2"]
                ),

                # Mostrar resumen de servicios (NO usar length() > 0 con estado)
                rx.cond(
                    intervencion.servicios_resumen != "",
                    rx.text(
                        intervencion.servicios_resumen,
                        font_size="0.85rem",
                        color=DARK_THEME["colors"]["text_secondary"],
                        white_space="pre-line"
                    ),
                    rx.text(
                        "Sin servicios registrados",
                        font_size="0.85rem",
                        color=DARK_THEME["colors"]["text_muted"],
                        font_style="italic"
                    )
                ),

                spacing="2",
                width="100%",
                align_items="start"
            ),

            # Footer con costos y estado
            rx.hstack(
                # Costos - NO usar f-strings con :,.2f en vars
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "BS",
                                font_size="0.65rem",
                                color=DARK_THEME["colors"]["text_muted"]
                            ),
                            rx.text(
                                "Bs. " + intervencion.costo_total_bs.to(str),
                                font_weight="700",
                                font_size="0.9rem",
                                color=COLORS["success"]["400"]
                            ),
                            spacing="0",
                            align="center"
                        ),
                        padding=SPACING["2"],
                        background=f"{COLORS['success']['500']}10",
                        border_radius=RADIUS["md"]
                    ),

                    rx.box(
                        rx.vstack(
                            rx.text(
                                "USD",
                                font_size="0.65rem",
                                color=DARK_THEME["colors"]["text_muted"]
                            ),
                            rx.text(
                                "$ " + intervencion.costo_total_usd.to(str),
                                font_weight="700",
                                font_size="0.9rem",
                                color=COLORS["blue"]["500"]
                            ),
                            spacing="0",
                            align="center"
                        ),
                        padding=SPACING["2"],
                        background=f"{COLORS['blue']['500']}10",
                        border_radius=RADIUS["md"]
                    ),

                    spacing="3"
                ),

                rx.spacer(),

                # Badge de estado
                rx.badge(
                    intervencion.estado_display,
                    color_scheme=rx.cond(
                        intervencion.estado == "completada",
                        "green",
                        rx.cond(
                            intervencion.estado == "en_progreso",
                            "yellow",
                            "gray"
                        )
                    ),
                    size="2"
                ),

                width="100%",
                align="center"
            ),

            spacing="4",
            width="100%",
            align_items="start"
        ),
        style=INTERVENCION_CARD_STYLE
    )


def panel_intervenciones_previas() -> rx.Component:
    """
    📋 PANEL PRINCIPAL DE INTERVENCIONES PREVIAS

    Muestra todas las intervenciones registradas en la consulta actual
    por otros odontólogos.
    """
    return rx.cond(
        AppState.intervenciones_anteriores.length() > 0,
        rx.box(
            rx.vstack(
                # Header del panel
                rx.hstack(
                    rx.icon("history", size=20, color=COLORS["primary"]["400"]),
                    rx.text(
                        "Intervenciones Previas en esta Consulta",
                        font_size="1.25rem",
                        font_weight="700",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    spacing="2",
                    align="center"
                ),

                # Subtítulo informativo - NO usar f-string con length()
                rx.text(
                    AppState.intervenciones_anteriores.length().to(str) + " intervención(es) realizada(s) por otros odontólogos",
                    font_size="0.9rem",
                    color=DARK_THEME["colors"]["text_secondary"],
                    margin_bottom=SPACING["2"]
                ),

                rx.divider(
                    border_color=DARK_THEME["colors"]["border"],
                    margin=f"{SPACING['3']} 0"
                ),

                # Lista de intervenciones
                rx.vstack(
                    rx.foreach(
                        AppState.intervenciones_anteriores,
                        intervencion_previa_card
                    ),
                    spacing="3",
                    width="100%"
                ),

                # Footer con totales acumulados - NO usar f-strings con :,.2f
                rx.box(
                    rx.hstack(
                        rx.text(
                            "Total Acumulado:",
                            font_weight="600",
                            font_size="0.95rem",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),

                        rx.spacer(),

                        rx.hstack(
                            rx.text(
                                "Bs. " + AppState.total_intervenciones_previas_bs.to(str),
                                font_weight="700",
                                font_size="1rem",
                                color=COLORS["success"]["400"]
                            ),
                            rx.text(
                                "|",
                                color=DARK_THEME["colors"]["border"]
                            ),
                            rx.text(
                                "$ " + AppState.total_intervenciones_previas_usd.to(str),
                                font_weight="700",
                                font_size="1rem",
                                color=COLORS["blue"]["500"]
                            ),
                            spacing="2"
                        ),

                        width="100%",
                        align="center"
                    ),
                    padding=SPACING["4"],
                    background=f"{DARK_THEME['colors']['surface']}80",
                    border_radius=RADIUS["md"],
                    border=f"1px solid {DARK_THEME['colors']['border']}",
                    margin_top=SPACING["3"]
                ),

                spacing="4",
                width="100%"
            ),
            style=PANEL_STYLE
        ),
        # Estado vacío (no hay intervenciones previas - primer odontólogo)
        rx.box(
            rx.vstack(
                rx.icon("circle-check", size=32, color=COLORS["success"]["400"]),
                rx.text(
                    "Primera Intervención",
                    font_size="1.1rem",
                    font_weight="600",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                rx.text(
                    "Eres el primer odontólogo en atender esta consulta",
                    font_size="0.9rem",
                    color=DARK_THEME["colors"]["text_secondary"],
                    text_align="center"
                ),
                spacing="2",
                align="center"
            ),
            style={
                **PANEL_STYLE,
                "padding": SPACING["8"],
                "text_align": "center",
                "border": f"2px dashed {DARK_THEME['colors']['border']}"
            }
        )
    )


# ==========================================
# EXPORTS
# ==========================================
__all__ = [
    "panel_intervenciones_previas",
    "intervencion_previa_card"
]