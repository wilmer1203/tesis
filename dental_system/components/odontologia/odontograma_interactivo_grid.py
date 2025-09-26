"""
Grid Completo de Odontograma Interactivo V2.0
Layout FDI estándar con 32 dientes organizados en 4 cuadrantes
"""
import reflex as rx

# Imports del sistema
from dental_system.models.odontograma_avanzado_models import DienteInteractivoModel
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.diente_interactivo import (
    diente_interactivo,
    selector_condiciones_cara
)
from dental_system.styles.themes import COLORS, DARK_THEME, SHADOWS


def odontograma_interactivo_grid() -> rx.Component:
    """
    Grid completo de odontograma con 32 dientes interactivos

    Layout FDI estándar:
    - Cuadrante 1 (Superior Derecho): 18-11
    - Cuadrante 2 (Superior Izquierdo): 21-28
    - Cuadrante 3 (Inferior Izquierdo): 31-38
    - Cuadrante 4 (Inferior Derecho): 41-48

    Returns:
        Grid completo interactivo del odontograma
    """
    return rx.vstack(
        # =============================================
        # HEADER CON CONTROLES Y ESTADÍSTICAS
        # =============================================
        header_odontograma(),

        # =============================================
        # FILTROS Y CONTROLES
        # =============================================
        controles_odontograma(),

        # =============================================
        # GRID PRINCIPAL DE DIENTES
        # =============================================
        rx.box(
            rx.vstack(
                # ===============================
                # ARCADA SUPERIOR
                # ===============================
                rx.vstack(
                    # Label arcada superior
                    rx.center(
                        rx.badge(
                            "ARCADA SUPERIOR",
                            color_scheme="blue",
                            size="2",
                            variant="outline"
                        ),
                        margin_bottom="3"
                    ),

                    # Cuadrantes superiores
                    rx.hstack(
                        # Cuadrante 1 (Superior Derecho): 18-11
                        cuadrante_dientes(
                            titulo="Cuadrante 1 (Sup. Der.)",
                            cuadrante_key="cuadrante_1",
                            orden_reverso=True
                        ),

                        # Separador central
                        rx.divider(
                            orientation="vertical",
                            height="200px",
                            border_color=DARK_THEME["colors"]["border"],
                            border_width="2px"
                        ),

                        # Cuadrante 2 (Superior Izquierdo): 21-28
                        cuadrante_dientes(
                            titulo="Cuadrante 2 (Sup. Izq.)",
                            cuadrante_key="cuadrante_2",
                            orden_reverso=False
                        ),

                        spacing="6",
                        justify="center",
                        align="start"
                    ),

                    spacing="4"
                ),

                # ===============================
                # SEPARADOR HORIZONTAL
                # ===============================
                rx.center(
                    rx.divider(
                        width="90%",
                        border_color=DARK_THEME["colors"]["border"],
                        border_width="2px",
                        margin_y="6"
                    )
                ),

                # ===============================
                # ARCADA INFERIOR
                # ===============================
                rx.vstack(
                    # Label arcada inferior
                    rx.center(
                        rx.badge(
                            "ARCADA INFERIOR",
                            color_scheme="orange",
                            size="2",
                            variant="outline"
                        ),
                        margin_bottom="3"
                    ),

                    # Cuadrantes inferiores
                    rx.hstack(
                        # Cuadrante 4 (Inferior Derecho): 48-41
                        cuadrante_dientes(
                            titulo="Cuadrante 4 (Inf. Der.)",
                            cuadrante_key="cuadrante_4",
                            orden_reverso=True
                        ),

                        # Separador central
                        rx.divider(
                            orientation="vertical",
                            height="200px",
                            border_color=DARK_THEME["colors"]["border"],
                            border_width="2px"
                        ),

                        # Cuadrante 3 (Inferior Izquierdo): 31-38
                        cuadrante_dientes(
                            titulo="Cuadrante 3 (Inf. Izq.)",
                            cuadrante_key="cuadrante_3",
                            orden_reverso=False
                        ),

                        spacing="6",
                        justify="center",
                        align="start"
                    ),

                    spacing="4"
                ),

                spacing="6",
                align="center"
            ),

            # Estilo del contenedor principal
            padding="8",
            background=f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
            border_radius="20px",
            border=f"1px solid {DARK_THEME['colors']['border']}",
            box_shadow=SHADOWS["2xl"],
            width="100%",
            max_width="1200px"
        ),

        # =============================================
        # SELECTOR DE CONDICIONES (FLOTANTE)
        # =============================================
        rx.box(
            selector_condiciones_cara(),
            position="fixed",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            z_index="1000",
            display=rx.cond(
                AppState.show_selector_condiciones,
                "block",
                "none"
            )
        ),

        # =============================================
        # LEYENDA Y AYUDA
        # =============================================
        leyenda_odontograma(),

        spacing="6",
        align="center",
        width="100%"
    )


def header_odontograma() -> rx.Component:
    """Header con título y estadísticas principales"""
    return rx.hstack(
        # Título principal
        rx.vstack(
            rx.heading(
                "Odontograma Interactivo FDI",
                size="7",
                color=COLORS["gray"]["100"]
            ),
            rx.text(
                f"HC: {AppState.numero_historia_actual}",
                size="3",
                color=COLORS["gray"]["400"]
            ),
            spacing="1",
            align="start"
        ),

        rx.spacer(),

        # Estadísticas en tiempo real
        rx.hstack(
            # Dientes sanos
            stat_card(
                "Dientes Sanos",
                AppState.estadisticas_resumen["dientes_sanos"],
                "✅",
                "success"
            ),

            # Dientes afectados
            stat_card(
                "Con Condiciones",
                AppState.estadisticas_resumen["dientes_afectados"],
                "📋",
                "warning"
            ),

            # Condiciones críticas
            stat_card(
                "Críticos",
                AppState.estadisticas_resumen["condiciones_criticas"],
                "⚠️",
                "error"
            ),

            # Porcentaje de salud
            stat_card(
                "% Salud",
                f"{AppState.estadisticas_resumen['porcentaje_salud']}%",
                "💚",
                "primary"
            ),

            spacing="4"
        ),

        justify="between",
        align="center",
        width="100%",
        padding="4"
    )


def controles_odontograma() -> rx.Component:
    """Controles y filtros del odontograma"""
    return rx.hstack(
        # Controles de vista
        rx.hstack(
            rx.button(
                "Modo Edición",
                left_icon=rx.cond(AppState.modo_edicion_ui, "eye", "edit"),
                variant=rx.cond(AppState.modo_edicion_ui, "solid", "outline"),
                color_scheme="blue",
                on_click=AppState.toggle_modo_edicion
            ),

            rx.button(
                "Comparar Versiones",
                left_icon="git_compare",
                variant="outline",
                color_scheme="purple",
                on_click=AppState.mostrar_comparador_versiones
            ),

            rx.button(
                "Simular Test",
                left_icon="play",
                variant="ghost",
                color_scheme="gray",
                on_click=AppState.simular_condiciones_test
            ),

            spacing="3"
        ),

        rx.spacer(),

        # Filtros
        rx.hstack(
            rx.switch(
                checked=AppState.mostrar_solo_condiciones,
                on_change=lambda v: AppState.aplicar_filtro_visualizacion("solo_condiciones")
            ),
            rx.text("Solo con condiciones", size="2", color=COLORS["gray"]["300"]),

            rx.switch(
                checked=AppState.mostrar_solo_criticos,
                on_change=lambda v: AppState.aplicar_filtro_visualizacion("solo_criticos")
            ),
            rx.text("Solo críticos", size="2", color=COLORS["gray"]["300"]),

            spacing="4",
            align="center"
        ),

        justify="between",
        align="center",
        width="100%",
        padding="4",
        background=f"{DARK_THEME['colors']['surface']}80",
        border_radius="12px",
        border=f"1px solid {DARK_THEME['colors']['border']}"
    )


def cuadrante_dientes(titulo: str, cuadrante_key: str, orden_reverso: bool = False) -> rx.Component:
    """
    Cuadrante individual con 8 dientes

    Args:
        titulo: Título del cuadrante
        cuadrante_key: Clave del cuadrante en dientes_por_cuadrante
        orden_reverso: Si mostrar en orden reverso

    Returns:
        Componente del cuadrante
    """
    return rx.vstack(
        # Título del cuadrante
        rx.center(
            rx.text(
                titulo,
                size="2",
                weight="medium",
                color=COLORS["gray"]["300"]
            ),
            margin_bottom="2"
        ),

        # Grid de dientes del cuadrante usando computed var
        rx.hstack(
            rx.foreach(
                AppState.dientes_por_cuadrante[cuadrante_key],
                lambda diente: diente_interactivo(diente)
            ),
            spacing="2",
            justify="center",
            wrap="wrap"
        ),

        spacing="2",
        align="center",
        min_width="600px"
    )


def stat_card(titulo: str, valor: rx.Var, icono: str, color: str) -> rx.Component:
    """
    Card de estadística individual

    Args:
        titulo: Título de la estadística
        valor: Valor a mostrar
        icono: Emoji del icono
        color: Color del tema

    Returns:
        Card de estadística
    """
    return rx.card(
        rx.vstack(
            rx.text(icono, font_size="24px"),
            rx.text(
                valor,
                size="5",
                weight="bold",
                color=COLORS["primary"]["400"]
            ),
            rx.text(
                titulo,
                size="1",
                color=COLORS["gray"]["400"],
                text_align="center"
            ),
            spacing="1",
            align="center"
        ),
        padding="3",
        min_width="80px",
        background=f"{DARK_THEME['colors']['surface']}80",
        border=f"1px solid {COLORS[color]['500']}40"
    )


def leyenda_odontograma() -> rx.Component:
    """Leyenda de colores y condiciones"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.hstack(
                rx.text("Leyenda de Condiciones", size="3", weight="medium"),
                rx.icon("chevron_down", size=18),
                spacing="2",
                align="center"
            ),
            padding="3",
            cursor="pointer"
        ),

        rx.dialog.content(
            rx.grid(
                rx.foreach(
                    AppState.condiciones_disponibles_ui,
                    lambda condicion: rx.hstack(
                        rx.box(
                            width="20px",
                            height="20px",
                            background=condicion["color"],
                            border_radius="4px",
                            border="1px solid rgba(255,255,255,0.2)"
                        ),
                        rx.text(
                            condicion["nombre"],
                            size="2",
                            color=COLORS["gray"]["300"]
                        ),
                        spacing="2",
                        align="center"
                    )
                ),
                columns="4",
                spacing="3",
                padding="4"
            )
        ),

        width="100%",
        max_width="800px"
    )


def odontograma_loading_state() -> rx.Component:
    """Estado de carga del odontograma"""
    return rx.center(
        rx.vstack(
            rx.spinner(size="3", color=COLORS["primary"]["500"]),
            rx.text(
                "Cargando odontograma...",
                size="3",
                color=COLORS["gray"]["400"]
            ),
            spacing="3",
            align="center"
        ),
        min_height="400px"
    )


def odontograma_error_state(mensaje: str) -> rx.Component:
    """Estado de error del odontograma"""
    return rx.center(
        rx.vstack(
            rx.icon("alert_triangle", size=48, color=COLORS["error"]["500"]),
            rx.heading("Error cargando odontograma", size="5", color=COLORS["error"]["400"]),
            rx.text(mensaje, size="3", color=COLORS["gray"]["400"], text_align="center"),
            rx.text("Intente recargando la página", size="2", color=COLORS["gray"]["500"]),
            spacing="4",
            align="center"
        ),
        min_height="400px"
    )


def odontograma_principal_con_estados() -> rx.Component:
    """
    Componente principal del odontograma con manejo de estados

    Incluye estados de carga, error y contenido principal
    """
    return rx.cond(
        AppState.cargando_odontograma,
        odontograma_loading_state(),

        rx.cond(
            AppState.error_mensaje != "",
            odontograma_error_state(AppState.error_mensaje),

            # ✅ CONTENIDO PRINCIPAL: Odontograma completo del paciente
            odontograma_interactivo_grid()
        )
    )


# ===========================================
# EXPORTS
# ===========================================

__all__ = [
    "odontograma_interactivo_grid",
    "odontograma_principal_con_estados",
    "header_odontograma",
    "controles_odontograma",
    "cuadrante_dientes",
    "leyenda_odontograma"
]