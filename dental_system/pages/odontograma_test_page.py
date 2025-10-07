"""
🦷 PÁGINA DE PRUEBA - ODONTOGRAMA V2.0 INTERACTIVO
==================================================

Página dedicada para probar el odontograma V2.0 interactivo de forma independiente.
Accesible en: /odontograma-test

Funcionalidades:
- Odontograma FDI completo (32 dientes)
- Interactividad por superficie (5 superficies por diente)
- Modal de selección de condiciones
- Guardado en tiempo real
- Visualización de estado y feedback
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.odontograma_interactivo_grid import (
    odontograma_principal_con_estados
)
from dental_system.styles.themes import (
    COLORS, DARK_THEME, SHADOWS, GRADIENTS,
    dark_page_background, dark_crystal_card
)

# ==========================================
# 🎨 ESTILOS ESPECÍFICOS PARA PÁGINA DE PRUEBA
# ==========================================

def page_header() -> rx.Component:
    """📋 Header de la página de prueba"""
    return rx.box(
        rx.vstack(
            # Título principal
            rx.heading(
                "🦷 Odontograma V2.0 Interactivo",
                size="8",
                color=COLORS["primary"]["400"],
                text_align="center",
                style={
                    "background": f"linear-gradient(135deg, {COLORS['primary']['400']} 0%, {COLORS['blue']['500']} 100%)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent",
                    "background-clip": "text"
                }
            ),

            # Subtítulo
            rx.text(
                "Sistema FDI Completo • 32 Dientes • 5 Superficies por Diente • Tiempo Real",
                size="4",
                color=DARK_THEME["colors"]["text_secondary"],
                text_align="center",
                font_weight="500"
            ),

            # Estado del paciente de prueba
            rx.hstack(
                rx.badge(
                    "Paciente de Prueba",
                    color_scheme="blue",
                    size="2"
                ),
                rx.badge(
                    "Modo Desarrollo",
                    color_scheme="gray",
                    size="2"
                ),
                rx.badge(
                    "V2.0 Interactivo",
                    color_scheme="green",
                    size="2"
                ),
                spacing="3",
                justify="center"
            ),

            spacing="4",
            align="center",
            width="100%"
        ),
        style=dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        padding="6",
        margin_bottom="6"
    )

def info_panel() -> rx.Component:
    """📋 Panel de información y instrucciones"""
    return rx.box(
        rx.vstack(
            rx.heading("📋 Instrucciones de Uso", size="5", color=COLORS["primary"]["400"]),

            rx.vstack(
                rx.hstack(
                    rx.icon("mouse-pointer-click", size=20, color=COLORS["success"]["400"]),
                    rx.text(
                        "Haz clic en cualquier superficie de un diente para seleccionarla",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    spacing="3",
                    align="center"
                ),

                rx.hstack(
                    rx.icon("palette", size=20, color=COLORS["warning"]["400"]),
                    rx.text(
                        "Se abrirá el modal de condiciones para elegir el estado de la superficie",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    spacing="3",
                    align="center"
                ),

                rx.hstack(
                    rx.icon("save", size=20, color=COLORS["blue"]["500"]),
                    rx.text(
                        "Los cambios se guardan automáticamente en tiempo real",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    spacing="3",
                    align="center"
                ),

                rx.hstack(
                    rx.icon("eye", size=20, color=COLORS["primary"]["400"]),
                    rx.text(
                        "Observa el feedback visual y las animaciones de estado",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    spacing="3",
                    align="center"
                ),

                spacing="3",
                align="start"
            ),

            spacing="4",
            width="100%"
        ),
        style=dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        padding="4",
        margin_bottom="4"
    )

def test_controls() -> rx.Component:
    """🎛️ Controles de prueba"""
    return rx.box(
        rx.hstack(
            # Botón para limpiar odontograma
            rx.button(
                rx.hstack(
                    rx.icon("trash-2", size=16),
                    rx.text("Limpiar Odontograma", size="2"),
                    spacing="2"
                ),
                variant="outline",
                color_scheme="red",
                on_click=AppState.limpiar_odontograma_test,
                size="2"
            ),

            # Botón para cargar datos de ejemplo
            rx.button(
                rx.hstack(
                    rx.icon("download", size=16),
                    rx.text("Cargar Ejemplo", size="2"),
                    spacing="2"
                ),
                variant="outline",
                color_scheme="blue",
                on_click=AppState.cargar_odontograma_ejemplo,
                size="2"
            ),

            # Botón volver al dashboard
            rx.button(
                rx.hstack(
                    rx.icon("arrow-left", size=16),
                    rx.text("Volver al Dashboard", size="2"),
                    spacing="2"
                ),
                variant="solid",
                color_scheme="gray",
                on_click=lambda: rx.redirect("/dashboard"),
                size="2"
            ),

            spacing="3",
            justify="center",
            width="100%"
        ),
        style=dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        padding="4",
        margin_bottom="4"
    )

def odontograma_test_page() -> rx.Component:
    """🦷 Página completa de prueba del odontograma V2.0"""
    return rx.container(
        rx.vstack(
            # Header de la página
            page_header(),

            # Panel de información
            info_panel(),

            # Controles de prueba
            test_controls(),

            # 🆕 ODONTOGRAMA V2.0 INTERACTIVO PRINCIPAL
            odontograma_principal_con_estados(),

            spacing="6",
            width="100%",
            align="center"
        ),

        # Estilo de página
         style=dark_page_background(),
        size="4",
        padding="4"
    )

# ==========================================
# 🚀 EXPORTAR PÁGINA
# ==========================================

__all__ = ["odontograma_test_page"]