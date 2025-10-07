"""
Grid Completo de Odontograma Interactivo V2.0
Layout FDI estándar con 32 dientes organizados en 4 cuadrantes
"""
import reflex as rx

# Imports del sistema
from dental_system.models.odontograma_avanzado_models import DienteInteractivoModel
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.interactive_tooth import (
    interactive_tooth
)
from dental_system.components.odontologia.condition_selector_modal import (
    condition_selector_modal
)
from dental_system.styles.themes import COLORS, DARK_THEME, SHADOWS


def odontograma_status_bar() -> rx.Component:
    """
    🚦 Barra de estado del odontograma V2.0 con feedback visual

    Muestra estado de carga, guardado, errores y cambios pendientes
    """
    return rx.box(
        rx.hstack(
            # Información del paciente
            rx.hstack(
                rx.icon(tag="user", size=20, color=COLORS["primary"]["400"]),
                rx.text(
                    f"Paciente: {AppState.paciente_actual.primer_nombre} {AppState.paciente_actual.primer_apellido}",
                    weight="medium",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                spacing="2",
                align="center"
            ),

            rx.spacer(),

            # Estado del odontograma con animaciones
            rx.cond(
                AppState.odontograma_cargando,
                rx.hstack(
                    rx.spinner(size="2", color=COLORS["primary"]["400"]),
                    rx.text(
                        "Cargando odontograma...",
                        color=COLORS["primary"]["400"],
                        weight="medium"
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.cond(
                    AppState.odontograma_guardando,
                    rx.hstack(
                        rx.spinner(size="2", color=COLORS["success"]["400"]),
                        rx.text(
                            "Guardando cambios...",
                            color=COLORS["success"]["400"],
                            weight="medium"
                        ),
                        spacing="2",
                        align="center"
                    ),
                    rx.cond(
                        AppState.odontograma_error != "",
                        rx.hstack(
                            rx.icon(tag="circle-alert", size=16, color=COLORS["error"]["400"]),
                            rx.text(
                                AppState.odontograma_error,
                                color=COLORS["error"]["400"],
                                weight="medium"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.cond(
                            AppState.cambios_sin_guardar,
                            rx.hstack(
                                rx.icon(tag="clock", size=16, color=COLORS["warning"]["400"]),
                                rx.text(
                                    "Cambios sin guardar",
                                    color=COLORS["warning"]["400"],
                                    weight="medium"
                                ),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.icon(tag="circle-check", size=16, color=COLORS["success"]["400"]),
                                rx.text(
                                    "Sincronizado",
                                    color=COLORS["success"]["400"],
                                    weight="medium"
                                ),
                                spacing="2",
                                align="center"
                            )
                        )
                    )
                )
            ),

            spacing="4",
            align="center",
            width="100%"
        ),

        # Estilo de la barra
        padding="3",
        background=f"linear-gradient(90deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
        border_radius="12px",
        border=f"1px solid {DARK_THEME['colors']['border']}",
        margin_bottom="4",
        width="100%"
    )


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
        # BARRA DE ESTADO DEL ODONTOGRAMA V2.0
        # =============================================
        odontograma_status_bar(),

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

                    # Cuadrantes superiores mejorados
                    rx.hstack(
                        # Cuadrante 1 (Superior Derecho): 18-11
                        cuadrante_dientes(
                            titulo="Cuadrante 1 (Sup. Der.)",
                            cuadrante_key="cuadrante_1",
                            orden_reverso=True
                        ),

                        # Separador central mejorado
                        rx.box(
                            rx.divider(
                                orientation="vertical",
                                height="280px",
                                border_color=f"{COLORS['primary']['400']}60",
                                border_width="3px"
                            ),
                            style={
                                "display": "flex",
                                "align_items": "center",
                                "justify_content": "center",
                                "padding": "0 20px",
                                "position": "relative"
                            }
                        ),

                        # Cuadrante 2 (Superior Izquierdo): 21-28
                        cuadrante_dientes(
                            titulo="Cuadrante 2 (Sup. Izq.)",
                            cuadrante_key="cuadrante_2",
                            orden_reverso=False
                        ),

                        spacing="4",
                        justify="center",
                        align="center",
                        width="100%"
                    ),

                    spacing="4"
                ),

                # ===============================
                # SEPARADOR HORIZONTAL MEJORADO
                # ===============================
                rx.center(
                    rx.box(
                        rx.divider(
                            width="60%",
                            border_color=f"{COLORS['primary']['400']}60",
                            border_width="3px",
                            margin_y="8"
                        ),
                        # Línea cruzada central
                        rx.box(
                            style={
                                "position": "absolute",
                                "top": "50%",
                                "left": "50%",
                                "transform": "translate(-50%, -50%)",
                                "width": "3px",
                                "height": "40px",
                                "background": f"{COLORS['primary']['400']}60",
                                "border_radius": "2px"
                            }
                        ),
                        style={"position": "relative", "width": "100%"}
                    ),
                    margin_y="8"
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

                    # Cuadrantes inferiores mejorados
                    rx.hstack(
                        # Cuadrante 4 (Inferior Derecho): 48-41
                        cuadrante_dientes(
                            titulo="Cuadrante 4 (Inf. Der.)",
                            cuadrante_key="cuadrante_4",
                            orden_reverso=True
                        ),

                        # Separador central mejorado
                        rx.box(
                            rx.divider(
                                orientation="vertical",
                                height="280px",
                                border_color=f"{COLORS['primary']['400']}60",
                                border_width="3px"
                            ),
                            style={
                                "display": "flex",
                                "align_items": "center",
                                "justify_content": "center",
                                "padding": "0 20px",
                                "position": "relative"
                            }
                        ),

                        # Cuadrante 3 (Inferior Izquierdo): 31-38
                        cuadrante_dientes(
                            titulo="Cuadrante 3 (Inf. Izq.)",
                            cuadrante_key="cuadrante_3",
                            orden_reverso=False
                        ),

                        spacing="4",
                        justify="center",
                        align="center",
                        width="100%"
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
        # MODAL SELECTOR DE CONDICIONES V2.0
        # =============================================
        condition_selector_modal(),

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
    Cuadrante individual con 8 dientes V2.0 - Alineación mejorada

    Args:
        titulo: Título del cuadrante
        cuadrante_key: Clave del cuadrante en dientes_por_cuadrante
        orden_reverso: Si mostrar en orden reverso

    Returns:
        Componente del cuadrante con mejor alineación
    """
    return rx.box(
        # Título del cuadrante mejorado
        rx.center(
            rx.badge(
                titulo,
                size="2",
                variant="soft",
                color_scheme="blue" if "Sup" in titulo else "orange",
                style={
                    "font_weight": "semibold",
                    "padding": "8px 16px",
                    "border_radius": "12px"
                }
            ),
            margin_bottom="4"
        ),

        # Grid mejorado de dientes del cuadrante
        rx.box(
            rx.grid(
                rx.foreach(
                    AppState.dientes_por_cuadrante[cuadrante_key],
                    lambda tooth_num: interactive_tooth(tooth_num)
                ),
                columns="4",  # 4 columnas para mejor distribución
                gap="12px",   # Espaciado uniforme entre dientes
                width="100%",
                justify_content="center",
                align_items="center"
            ),
            style={
                "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
                "border_radius": "16px",
                "padding": "20px",
                "border": f"1px solid {DARK_THEME['colors']['border']}",
                "box_shadow": "inset 0 1px 0 rgba(255, 255, 255, 0.1), 0 2px 8px rgba(0, 0, 0, 0.1)"
            }
        ),

        width="100%",
        max_width="400px",  # Ancho máximo para mantener proporciones
        style={
            "display": "flex",
            "flex_direction": "column",
            "align_items": "center"
        }
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
            AppState.error_message != "",
            odontograma_error_state( AppState.error_message),

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