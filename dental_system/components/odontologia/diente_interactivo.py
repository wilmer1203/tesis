"""
Componente Diente Interactivo SVG V2.0
Diente completamente clickeable por superficies con efectos visuales avanzados
"""
import reflex as rx
from typing import Dict, Any

# Imports del sistema
from dental_system.models.odontograma_avanzado_models import DienteInteractivoModel, CaraDiente
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME


def diente_interactivo(diente: rx.Var[DienteInteractivoModel]) -> rx.Component:
    """
    Componente diente individual completamente interactivo

    Características:
    - SVG nativo con 5 caras clickeables independientes
    - Colores dinámicos según condición de cada cara
    - Hover effects y transiciones suaves
    - Integración completa con estado centralizado
    - Número FDI visible en el centro
    - Indicadores de selección y estado

    Args:
        diente: Modelo del diente interactivo

    Returns:
        Componente SVG interactivo
    """
    return rx.box(
        # SVG del diente con caras clickeables
        rx.el.svg(
            # =============================================
            # CARA OCLUSAL (Centro - Superficie de masticación)
            # =============================================
            rx.el.polygon(
                points="50,25 75,40 50,55 25,40",
                fill=diente.cara_oclusal.color_hex,
                stroke=DARK_THEME["colors"]["border"],
                stroke_width=2,
                cursor="pointer",
                on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.OCLUSAL),
                class_name="cara-oclusal transition-all duration-200 hover:scale-110 hover:stroke-4",
                id=f"oclusal-{diente.numero_fdi}"
            ),

            # =============================================
            # CARA MESIAL (Izquierda - Hacia el centro)
            # =============================================
            rx.el.polygon(
                points="15,35 35,25 35,55 15,45",
                fill=diente.cara_mesial.color_hex,
                stroke=DARK_THEME["colors"]["border"],
                stroke_width=2,
                cursor="pointer",
                on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.MESIAL),
                class_name="cara-mesial transition-all duration-200 hover:scale-110 hover:stroke-4",
                id=f"mesial-{diente.numero_fdi}"
            ),

            # =============================================
            # CARA DISTAL (Derecha - Hacia afuera)
            # =============================================
            rx.el.polygon(
                points="65,25 85,35 85,45 65,55",
                fill=diente.cara_distal.color_hex,
                stroke=DARK_THEME["colors"]["border"],
                stroke_width=2,
                cursor="pointer",
                on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.DISTAL),
                class_name="cara-distal transition-all duration-200 hover:scale-110 hover:stroke-4",
                id=f"distal-{diente.numero_fdi}"
            ),

            # =============================================
            # CARA VESTIBULAR (Arriba - Hacia labios/mejillas)
            # =============================================
            rx.el.polygon(
                points="25,10 75,10 85,25 15,25",
                fill=diente.cara_vestibular.color_hex,
                stroke=DARK_THEME["colors"]["border"],
                stroke_width=2,
                cursor="pointer",
                on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.VESTIBULAR),
                class_name="cara-vestibular transition-all duration-200 hover:scale-110 hover:stroke-4",
                id=f"vestibular-{diente.numero_fdi}"
            ),

            # =============================================
            # CARA LINGUAL (Abajo - Hacia la lengua)
            # =============================================
            rx.el.polygon(
                points="15,55 85,55 75,70 25,70",
                fill=diente.cara_lingual.color_hex,
                stroke=DARK_THEME["colors"]["border"],
                stroke_width=2,
                cursor="pointer",
                on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.LINGUAL),
                class_name="cara-lingual transition-all duration-200 hover:scale-110 hover:stroke-4",
                id=f"lingual-{diente.numero_fdi}"
            ),

            # =============================================
            # NÚMERO FDI EN EL CENTRO
            # =============================================
            rx.el.text(
                str(diente.numero_fdi),
                x=50,
                y=45,
                text_anchor="middle",
                dominant_baseline="middle",
                fill="white",
                font_weight="bold",
                font_size="14px",
                pointer_events="none",
                class_name="select-none",
                style={
                    "text_shadow": "1px 1px 2px rgba(0,0,0,0.8)"
                }
            ),

            # =============================================
            # INDICADORES DE ESTADO
            # =============================================

            # Indicador de selección (anillo dorado pulsante)
            rx.cond(
                diente.is_selected,
                rx.el.circle(
                    cx=50,
                    cy=40,
                    r=42,
                    fill="none",
                    stroke="#FFD700",
                    stroke_width=3,
                    stroke_dasharray="8,4",
                    class_name="animate-pulse",
                    pointer_events="none"
                )
            ),

            # Indicador de condiciones críticas (borde rojo)
            rx.cond(
                diente.condiciones_criticas.length() > 0,
                rx.el.circle(
                    cx=50,
                    cy=40,
                    r=45,
                    fill="none",
                    stroke="#FF6B6B",
                    stroke_width=2,
                    stroke_dasharray="4,2",
                    class_name="animate-pulse",
                    pointer_events="none"
                )
            ),

            # Badge de número de condiciones activas
            rx.cond(
                diente.numero_condiciones_activas > 0,
                rx.el.g(
                    rx.el.circle(
                        cx=85,
                        cy=15,
                        r=8,
                        fill=rx.cond(
                            diente.condiciones_criticas.length() > 0,
                            "#FF6B6B",
                            "#FFEAA7"
                        ),
                        stroke="white",
                        stroke_width=2
                    ),
                    rx.el.text(
                        str(diente.numero_condiciones_activas),
                        x=85,
                        y=15,
                        text_anchor="middle",
                        dominant_baseline="middle",
                        fill="white",
                        font_size="10px",
                        font_weight="bold",
                        pointer_events="none"
                    ),
                    pointer_events="none"
                )
            ),

            # =============================================
            # CONFIGURACIÓN DEL SVG
            # =============================================
            width=100,
            height=80,
            view_box="0 0 100 80",
            cursor="pointer",
            on_click=lambda: AppState.seleccionar_diente(diente.numero_fdi),
            class_name=f"diente-{diente.numero_fdi} transition-all duration-300 hover:scale-105",
            id=f"diente-svg-{diente.numero_fdi}"
        ),

        # =============================================
        # INFORMACIÓN ADICIONAL DEL DIENTE
        # =============================================

        # Nombre del diente (tooltip)
        rx.tooltip(
            rx.vstack(
                rx.text(
                    diente.nombre_diente,
                    size="2",
                    weight="medium",
                    color=COLORS["gray"]["100"]
                ),
                rx.text(
                    diente.estado_display,
                    size="1",
                    color=COLORS["gray"]["400"]
                ),
                rx.cond(
                    diente.costo_total_estimado > 0,
                    rx.text(
                        f"Costo estimado: ${diente.costo_total_estimado:.0f}",
                        size="1",
                        color=COLORS["warning"]["400"]
                    )
                ),
                spacing="1",
                align="start"
            )
        ),

        # =============================================
        # ESTILOS DEL CONTENEDOR
        # =============================================
        position="relative",
        padding="8px",
        border_radius="12px",
        background=rx.cond(
            diente.is_selected,
            f"linear-gradient(135deg, {DARK_THEME['colors']['surface']}80 0%, {DARK_THEME['colors']['surface_secondary']}80 100%)",
            "transparent"
        ),
        border=rx.cond(
            diente.is_selected,
            f"2px solid #FFD700",
            "2px solid transparent"
        ),
        transition="all 0.3s ease",
        _hover={
            "background": f"{DARK_THEME['colors']['surface']}40",
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.3)"
        }
    )


def diente_interactivo_grande(diente: rx.Var[DienteInteractivoModel]) -> rx.Component:
    """
    Versión grande del diente interactivo para modal de detalles

    Características:
    - Tamaño más grande para mejor interacción
    - Labels visibles en cada cara
    - Información detallada en hover
    - Animaciones más pronunciadas

    Args:
        diente: Modelo del diente interactivo

    Returns:
        Componente SVG grande e interactivo
    """
    return rx.center(
        rx.vstack(
            # Título del diente
            rx.heading(
                f"Diente {diente.numero_fdi} - {diente.nombre_diente}",
                size="5",
                color=COLORS["gray"]["100"],
                text_align="center"
            ),

            # SVG grande del diente
            rx.el.svg(
                # =============================================
                # CARA OCLUSAL (Centro)
                # =============================================
                rx.el.g(
                    rx.el.polygon(
                        points="150,75 225,120 150,165 75,120",
                        fill=diente.cara_oclusal.color_hex,
                        stroke=DARK_THEME["colors"]["border"],
                        stroke_width=3,
                        cursor="pointer",
                        on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.OCLUSAL),
                        class_name="cara-oclusal-grande transition-all duration-300 hover:scale-105 hover:stroke-6"
                    ),
                    rx.el.text(
                        "Oclusal",
                        x=150,
                        y=125,
                        text_anchor="middle",
                        dominant_baseline="middle",
                        fill="white",
                        font_weight="bold",
                        font_size="14px",
                        pointer_events="none",
                        style={"text_shadow": "2px 2px 4px rgba(0,0,0,0.8)"}
                    ),
                    id="oclusal-grande"
                ),

                # =============================================
                # CARA MESIAL (Izquierda)
                # =============================================
                rx.el.g(
                    rx.el.polygon(
                        points="30,90 90,75 90,165 30,150",
                        fill=diente.cara_mesial.color_hex,
                        stroke=DARK_THEME["colors"]["border"],
                        stroke_width=3,
                        cursor="pointer",
                        on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.MESIAL),
                        class_name="cara-mesial-grande transition-all duration-300 hover:scale-105 hover:stroke-6"
                    ),
                    rx.el.text(
                        "Mesial",
                        x=60,
                        y=120,
                        text_anchor="middle",
                        dominant_baseline="middle",
                        fill="white",
                        font_weight="bold",
                        font_size="12px",
                        pointer_events="none",
                        style={"text_shadow": "2px 2px 4px rgba(0,0,0,0.8)"}
                    ),
                    id="mesial-grande"
                ),

                # =============================================
                # CARA DISTAL (Derecha)
                # =============================================
                rx.el.g(
                    rx.el.polygon(
                        points="210,75 270,90 270,150 210,165",
                        fill=diente.cara_distal.color_hex,
                        stroke=DARK_THEME["colors"]["border"],
                        stroke_width=3,
                        cursor="pointer",
                        on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.DISTAL),
                        class_name="cara-distal-grande transition-all duration-300 hover:scale-105 hover:stroke-6"
                    ),
                    rx.el.text(
                        "Distal",
                        x=240,
                        y=120,
                        text_anchor="middle",
                        dominant_baseline="middle",
                        fill="white",
                        font_weight="bold",
                        font_size="12px",
                        pointer_events="none",
                        style={"text_shadow": "2px 2px 4px rgba(0,0,0,0.8)"}
                    ),
                    id="distal-grande"
                ),

                # =============================================
                # CARA VESTIBULAR (Arriba)
                # =============================================
                rx.el.g(
                    rx.el.polygon(
                        points="75,30 225,30 270,75 30,75",
                        fill=diente.cara_vestibular.color_hex,
                        stroke=DARK_THEME["colors"]["border"],
                        stroke_width=3,
                        cursor="pointer",
                        on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.VESTIBULAR),
                        class_name="cara-vestibular-grande transition-all duration-300 hover:scale-105 hover:stroke-6"
                    ),
                    rx.el.text(
                        "Vestibular",
                        x=150,
                        y=55,
                        text_anchor="middle",
                        dominant_baseline="middle",
                        fill="white",
                        font_weight="bold",
                        font_size="14px",
                        pointer_events="none",
                        style={"text_shadow": "2px 2px 4px rgba(0,0,0,0.8)"}
                    ),
                    id="vestibular-grande"
                ),

                # =============================================
                # CARA LINGUAL (Abajo)
                # =============================================
                rx.el.g(
                    rx.el.polygon(
                        points="30,165 270,165 225,210 75,210",
                        fill=diente.cara_lingual.color_hex,
                        stroke=DARK_THEME["colors"]["border"],
                        stroke_width=3,
                        cursor="pointer",
                        on_click=lambda: AppState.seleccionar_cara_diente(CaraDiente.LINGUAL),
                        class_name="cara-lingual-grande transition-all duration-300 hover:scale-105 hover:stroke-6"
                    ),
                    rx.el.text(
                        "Lingual",
                        x=150,
                        y=190,
                        text_anchor="middle",
                        dominant_baseline="middle",
                        fill="white",
                        font_weight="bold",
                        font_size="14px",
                        pointer_events="none",
                        style={"text_shadow": "2px 2px 4px rgba(0,0,0,0.8)"}
                    ),
                    id="lingual-grande"
                ),

                # =============================================
                # NÚMERO FDI CENTRAL
                # =============================================
                rx.el.text(
                    str(diente.numero_fdi),
                    x=150,
                    y=125,
                    text_anchor="middle",
                    dominant_baseline="middle",
                    fill="white",
                    font_weight="bold",
                    font_size="24px",
                    pointer_events="none",
                    style={
                        "text_shadow": "3px 3px 6px rgba(0,0,0,0.9)",
                        "font_family": "monospace"
                    }
                ),

                # =============================================
                # CONFIGURACIÓN SVG GRANDE
                # =============================================
                width=300,
                height=240,
                view_box="0 0 300 240",
                class_name="diente-grande transition-all duration-500"
            ),

            # Información detallada
            rx.hstack(
                rx.badge(
                    diente.estado_display,
                    color_scheme="cyan" if not diente.tiene_condiciones else "orange",
                    size="2"
                ),
                rx.cond(
                    diente.costo_total_estimado > 0,
                    rx.badge(
                        f"${diente.costo_total_estimado:.0f}",
                        color_scheme="yellow",
                        size="2"
                    )
                ),
                spacing="3",
                justify="center",
                margin_top="4"
            ),

            spacing="4",
            align="center"
        ),
        padding="20px"
    )


def selector_condiciones_cara() -> rx.Component:
    """
    Selector de condiciones para aplicar a la cara seleccionada

    Returns:
        Grid de condiciones disponibles
    """
    return rx.cond(
        AppState.show_selector_condiciones,
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    f"Superficie {AppState.cara_seleccionada}",
                    size="4",
                    color=COLORS["gray"]["100"]
                ),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x", size=18),
                    variant="ghost",
                    on_click=lambda: AppState.set_show_selector_condiciones(False),
                    color_scheme="gray"
                ),
                justify="between",
                width="100%",
                margin_bottom="4"
            ),

            # Grid de condiciones
            rx.grid(
                rx.foreach(
                    AppState.condiciones_disponibles_ui,
                    lambda condicion: rx.card(
                        rx.vstack(
                            rx.box(
                                width="40px",
                                height="40px",
                                background=condicion["color"],
                                border_radius="8px",
                                border="2px solid rgba(255,255,255,0.2)"
                            ),
                            rx.text(
                                condicion["nombre"],
                                size="2",
                                weight="medium",
                                color=COLORS["gray"]["100"],
                                text_align="center"
                            ),
                            align="center",
                            spacing="2"
                        ),
                        cursor="pointer",
                        on_click=lambda c=condicion: AppState.aplicar_condicion_cara(
                            c["tipo"],
                            "leve",
                            f"Condición aplicada: {c['nombre']}"
                        ),
                        padding="3",
                        transition="all 0.2s ease",
                        _hover={
                            "transform": "scale(1.05)",
                            "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.4)"
                        }
                    )
                ),
                columns="4",
                spacing="3",
                width="100%"
            ),

            # Botones de acción
            rx.hstack(
                rx.button(
                    "Resetear a Sano",
                    left_icon="refresh_cw",
                    variant="outline",
                    color_scheme="green",
                    on_click=AppState.resetear_cara_diente
                ),
                rx.button(
                    "Cancelar",
                    variant="ghost",
                    on_click=lambda: AppState.set_show_selector_condiciones(False)
                ),
                spacing="3",
                justify="center",
                margin_top="4"
            ),

            spacing="4",
            padding="6",
            background=f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
            border_radius="16px",
            border=f"1px solid {DARK_THEME['colors']['border']}",
            box_shadow="0 20px 40px rgba(0, 0, 0, 0.4)",
            max_width="400px"
        )
    )


# ===========================================
# FUNCIONES DE UTILIDAD
# ===========================================

def _hover_cara(numero_fdi: int, cara: str):
    """Manejar hover sobre cara específica"""
    # En implementación real podríamos mostrar tooltip o highlights
    pass


def _unhover_cara():
    """Manejar salida de hover"""
    # En implementación real limpiaríamos highlights
    pass


# ===========================================
# EXPORTS
# ===========================================

__all__ = [
    "diente_interactivo",
    "diente_interactivo_grande",
    "selector_condiciones_cara"
]