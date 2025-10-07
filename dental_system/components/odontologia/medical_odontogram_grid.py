"""
🦷 GRID MÉDICO PROFESIONAL: ODONTOGRAMA FDI COMPLETO
==================================================

Grid optimizado del odontograma con espaciado estandarizado y diseño profesional.
Organizado según sistema FDI estándar (4 cuadrantes, 32 dientes).

Características:
- Barra de estado compacta (48px)
- Separadores sutiles (1px, opacity 0.2)
- Cuadrantes optimizados (padding 12px, gap 8px)
- Leyenda fija en sidebar derecho
- Sistema de espaciado consistente (8/16/24/32px)
- Colores médicos profesionales

Versión: 3.0 Professional Medical
Fecha: Enero 2025
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.professional_tooth import (
    professional_tooth_with_tooltip,
    medical_conditions_legend
)
from dental_system.components.odontologia.medical_condition_modal import medical_condition_modal
from dental_system.styles.medical_design_system import (
    MEDICAL_COLORS,
    MEDICAL_SPACING,
    MEDICAL_TYPOGRAPHY,
    MEDICAL_SHADOWS,
    MEDICAL_RADIUS,
    medical_card_style
)

# ==========================================
# 🚦 BARRA DE ESTADO COMPACTA (48px)
# ==========================================

def medical_status_bar() -> rx.Component:
    """
    🚦 Barra de estado compacta y profesional del odontograma

    Altura: 48px
    Contenido: Paciente + Estado + Última modificación

    Returns:
        Barra de estado médica compacta
    """

    return rx.box(
        rx.hstack(
            # Información del paciente
            rx.hstack(
                rx.icon(
                    tag="user",
                    size=18,
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                ),
                rx.text(
                    f"{AppState.paciente_actual.primer_nombre} {AppState.paciente_actual.primer_apellido}",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                    font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["medium"],
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                ),
                spacing="2",
                align="center"
            ),

            rx.spacer(),

            # Estado del odontograma
            rx.cond(
                AppState.odontograma_cargando,
                rx.hstack(
                    rx.spinner(size="2", color=MEDICAL_COLORS["medical_ui"]["accent_primary"]),
                    rx.text(
                        "Cargando...",
                        font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.cond(
                    AppState.odontograma_guardando,
                    rx.hstack(
                        rx.spinner(size="2", color=MEDICAL_COLORS["medical_ui"]["accent_success"]),
                        rx.text(
                            "Guardando...",
                            font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                            color=MEDICAL_COLORS["medical_ui"]["accent_success"]
                        ),
                        spacing="2",
                        align="center"
                    ),
                    rx.cond(
                        AppState.cambios_sin_guardar,
                        rx.hstack(
                            rx.icon(tag="clock", size=16, color=MEDICAL_COLORS["medical_ui"]["accent_warning"]),
                            rx.text(
                                "Cambios sin guardar",
                                font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                                color=MEDICAL_COLORS["medical_ui"]["accent_warning"]
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.hstack(
                            rx.icon(tag="check-circle-2", size=16, color=MEDICAL_COLORS["medical_ui"]["accent_success"]),
                            rx.text(
                                "Sincronizado",
                                font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                                color=MEDICAL_COLORS["medical_ui"]["accent_success"]
                            ),
                            spacing="2",
                            align="center"
                        )
                    )
                )
            ),

            spacing="4",
            align="center",
            width="100%"
        ),

        # Estilos de la barra
        height="48px",
        padding=f"0 {MEDICAL_SPACING['lg']}",
        background=MEDICAL_COLORS["medical_ui"]["surface"],
        border_bottom=f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
        width="100%"
    )


# ==========================================
# 🎛️ CONTROLES CONTEXTUALES MÉDICOS
# ==========================================

def medical_controls_panel() -> rx.Component:
    """
    🎛️ Panel de controles contextuales médicos

    Incluye: Nueva Intervención, Historial, Exportar PDF

    Returns:
        Panel de controles médicos profesional
    """

    return rx.hstack(
        # Controles principales
        rx.button(
            rx.hstack(
                rx.icon(tag="plus-circle", size=18),
                rx.text("Nueva Intervención", font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"]),
                spacing="2"
            ),
            size="2",
            variant="solid",
            color_scheme="blue",
            on_click=AppState.nueva_intervencion
        ),

        rx.button(
            rx.hstack(
                rx.icon(tag="history", size=18),
                rx.text("Historial", font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"]),
                spacing="2"
            ),
            size="2",
            variant="outline",
            color_scheme="gray",
            on_click=AppState.mostrar_historial_odontograma
        ),

        rx.button(
            rx.hstack(
                rx.icon(tag="download", size=18),
                rx.text("Exportar PDF", font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"]),
                spacing="2"
            ),
            size="2",
            variant="ghost",
            color_scheme="gray",
            on_click=AppState.exportar_odontograma_pdf
        ),

        spacing="3",
        align="center",
        width="100%",
        padding=MEDICAL_SPACING["md"]
    )


# ==========================================
# 📐 CUADRANTE DE DIENTES
# ==========================================

def medical_quadrant_section(
    title: str,
    quadrant_key: str,
    color_scheme: str = "blue"
) -> rx.Component:
    """
    📐 Sección de cuadrante médica optimizada

    Args:
        title: Título del cuadrante
        quadrant_key: Clave del cuadrante en el estado
        color_scheme: Esquema de color (blue/orange)

    Returns:
        Componente de cuadrante médico profesional
    """

    return rx.box(
        # Título del cuadrante
        rx.text(
            title,
            font_size=MEDICAL_TYPOGRAPHY["font_size"]["xs"],
            font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["semibold"],
            color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
            text_align="center",
            margin_bottom="2"
        ),

        # Grid de dientes del cuadrante
        rx.grid(
            rx.foreach(
                AppState.dientes_por_cuadrante[quadrant_key],
                lambda tooth_num: professional_tooth_with_tooltip(tooth_num)
            ),
            columns="4",  # 4 columnas anatómicas
            gap=MEDICAL_SPACING["sm"],  # 8px gap estandarizado
            width="100%",
            justify_content="center"
        ),

        # Estilos del contenedor
        style={
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "border": f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
            "border_radius": MEDICAL_RADIUS["md"],
            "padding": MEDICAL_SPACING["md"],  # 16px padding
            "box_shadow": MEDICAL_SHADOWS["xs"]
        },
        width="100%",
        max_width="300px"
    )


# ==========================================
# 🦷 GRID PRINCIPAL DEL ODONTOGRAMA
# ==========================================

def medical_odontogram_grid() -> rx.Component:
    """
    🦷 Grid principal del odontograma médico profesional

    Layout FDI estándar:
    - Cuadrante 1 (Superior Derecho): 18-11
    - Cuadrante 2 (Superior Izquierdo): 21-28
    - Cuadrante 3 (Inferior Izquierdo): 31-38
    - Cuadrante 4 (Inferior Derecho): 41-48

    Returns:
        Grid completo del odontograma profesional
    """

    return rx.vstack(
        # ===================================
        # ARCADA SUPERIOR
        # ===================================
        rx.vstack(
            # Label arcada superior
            rx.badge(
                "ARCADA SUPERIOR",
                size="2",
                variant="soft",
                color_scheme="blue"
            ),

            # Cuadrantes superiores
            rx.hstack(
                # Cuadrante 1 (Superior Derecho)
                medical_quadrant_section(
                    "Cuadrante 1 (Sup. Der.)",
                    "cuadrante_1",
                    "blue"
                ),

                # Separador vertical sutil
                rx.divider(
                    orientation="vertical",
                    height="280px",
                    border_color=MEDICAL_COLORS["medical_ui"]["border_light"],
                    opacity="0.3"
                ),

                # Cuadrante 2 (Superior Izquierdo)
                medical_quadrant_section(
                    "Cuadrante 2 (Sup. Izq.)",
                    "cuadrante_2",
                    "blue"
                ),

                spacing="4",  # Reflex scale: 4 = 16px
                justify="center",
                align="center"
            ),

            spacing="3",
            align="center"
        ),

        # ===================================
        # SEPARADOR HORIZONTAL SUTIL
        # ===================================
        rx.divider(
            width="60%",
            border_color=MEDICAL_COLORS["medical_ui"]["border_light"],
            opacity="0.3",
            margin_y=MEDICAL_SPACING["lg"]  # 24px
        ),

        # ===================================
        # ARCADA INFERIOR
        # ===================================
        rx.vstack(
            # Label arcada inferior
            rx.badge(
                "ARCADA INFERIOR",
                size="2",
                variant="soft",
                color_scheme="orange"
            ),

            # Cuadrantes inferiores
            rx.hstack(
                # Cuadrante 4 (Inferior Derecho)
                medical_quadrant_section(
                    "Cuadrante 4 (Inf. Der.)",
                    "cuadrante_4",
                    "orange"
                ),

                # Separador vertical sutil
                rx.divider(
                    orientation="vertical",
                    height="280px",
                    border_color=MEDICAL_COLORS["medical_ui"]["border_light"],
                    opacity="0.3"
                ),

                # Cuadrante 3 (Inferior Izquierdo)
                medical_quadrant_section(
                    "Cuadrante 3 (Inf. Izq.)",
                    "cuadrante_3",
                    "orange"
                ),

                spacing="4",  # Reflex scale: 4 = 16px
                justify="center",
                align="center"
            ),

            spacing="3",
            align="center"
        ),

        spacing="6",  # Reflex scale: 6 = 24px entre secciones
        align="center",
        width="100%"
    )


# ==========================================
# 📊 PÁGINA PRINCIPAL CON LAYOUT COMPLETO
# ==========================================

def medical_odontogram_page() -> rx.Component:
    """
    📊 Página principal del odontograma médico profesional

    Layout:
    - Barra de estado compacta (top)
    - Controles contextuales
    - Grid principal (centro)
    - Leyenda fija (sidebar derecho)
    - Modal de condiciones (overlay)

    Returns:
        Página completa del odontograma médico
    """

    return rx.box(
        # Barra de estado compacta
        medical_status_bar(),

        # Contenido principal con sidebar
        rx.hstack(
            # Contenido principal
            rx.vstack(
                # Controles contextuales
                medical_controls_panel(),

                # Grid del odontograma
                rx.box(
                    medical_odontogram_grid(),
                    style={
                        **medical_card_style(elevated=True),
                        "padding": MEDICAL_SPACING["xl"]  # 32px
                    }
                ),

                spacing="6",  # Reflex scale: 6 = 24px
                align="center",
                flex="1",
                padding=MEDICAL_SPACING["lg"]
            ),

            # Sidebar derecho con leyenda
            rx.box(
                medical_conditions_legend(),
                width="280px",
                padding=MEDICAL_SPACING["lg"],
                border_left=f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}"
            ),

            spacing="0",
            width="100%",
            height="calc(100vh - 48px)",
            overflow="hidden"
        ),

        # Modal de condiciones (overlay)
        medical_condition_modal(),

        # Estilos del contenedor principal
        width="100%",
        height="100vh",
        background=MEDICAL_COLORS["medical_ui"]["background"],
        overflow="hidden"
    )


# ==========================================
# 🎯 EXPORTS
# ==========================================

__all__ = [
    "medical_odontogram_grid",
    "medical_odontogram_page",
    "medical_status_bar",
    "medical_controls_panel",
    "medical_quadrant_section"
]