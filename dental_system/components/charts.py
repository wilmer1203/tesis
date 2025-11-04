from ..state.app_state import AppState
import reflex as rx
from dental_system.styles.themes import (COLORS, SHADOWS, dark_crystal_card)
# =============================================
# Componentes Reutilizables
# =============================================



def chart_toggle() -> rx.Component:
    """Botón para alternar entre gráficos de área/barras."""
    return rx.icon_button(
        rx.cond(
            AppState.area_toggle,
            rx.icon("area-chart"),  # Ícono de gráfico de área
            rx.icon("bar-chart-3")  # Ícono de gráfico de barras
        ),
        on_click=AppState.toggle_areachart(),  # Alterna el estado
        variant="soft",
        color_scheme="blue"
    )
 
    
def custom_segmented_control() -> rx.Component:
    return rx.segmented_control.root(
            rx.segmented_control.item("Pacientes", value="Pacientes"),
            rx.segmented_control.item("Ingresos", value="Ingresos"),
            rx.segmented_control.item("Consultas", value="Consultas"),
            default_value="Pacientes",
            on_change=AppState.set_selected_tab,
            margin_bottom="1.5em",
            radius="full"
        )
      

def create_gradient(color: str, id: str) -> rx.Component:
    """Crea un gradiente SVG reutilizable."""
    return rx.el.svg.defs(
        rx.el.svg.linear_gradient(
            rx.el.svg.stop(offset="5%", stop_color=rx.color(color, 7), stop_opacity=0.8),
            rx.el.svg.stop(offset="95%", stop_color=rx.color(color, 7), stop_opacity=0),
            id=id,
            x1="0",
            x2="0",
            y1="0",
            y2="1",
        )
    )


def custom_tooltip(color: str, ) -> rx.Component:
    """Tooltip personalizado con sombra y borde."""
    return rx.recharts.graphing_tooltip(
        
        content_style={
            "backgroundColor": rx.color("gray", 1),
            "borderRadius": "var(--radius-2)",
            "borderWidth": "1px",
            "borderColor": rx.color(color, 7),
            "padding": "0.5rem",
            "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        },
        #separator=" : ",  # Separador entre el nombre y el valor

    )


def render_chart(key: str, color: str, gradient_id: str) -> rx.Component:
    return rx.box(  # Contenedor genérico para ajustar el tamaño
        rx.cond(
            AppState.area_toggle,
            rx.recharts.area_chart(  # AreaChart directamente
                rx.recharts.area(
                    data_key=key,
                    fill=f"url(#{gradient_id})",
                    stroke=color,
                    type_="natural"
                ),
                rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                #rx.recharts.y_axis(axis_line=False, tick_line=False, width=80),
                create_gradient(color, gradient_id),
                custom_tooltip(color),
                data=AppState.get_current_data,  # <-- Datos aquí
                height=300,
                width="100%"
            ),
            rx.recharts.bar_chart(  # BarChart directamente
                rx.recharts.bar(
                    data_key=key,
                    fill=color,
                    radius=[4, 4, 0, 0]
                ),
                rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                #rx.recharts.y_axis(axis_line=False, tick_line=False, width=80),
                custom_tooltip(color),
                data=AppState.get_current_data,  # <-- Datos aquí
                height=300,
                width="100%"
            )
            
        ),
        width="100%"
    )
    

    
def graficas_resume() -> rx.Component:
    """
    📊 COMPONENTE PRINCIPAL DE GRÁFICOS - CON TOGGLE REAL/RANDOM

    MEJORAS V2.0:
    - Datos reales desde dashboard_service
    - Toggle temporal para testing (icono pequeño)
    - Adaptación por rol de usuario
    - Mejor manejo de errores
    """
    return rx.box(
        rx.hstack(
            chart_toggle(),
            rx.spacer(),
            custom_segmented_control(),
            rx.spacer(),
            # 🧪 TOGGLE TEMPORAL PARA TESTING (eliminar después)
            rx.tooltip(
                rx.icon_button(
                    rx.cond(
                        AppState.usar_datos_reales_dashboard,
                        rx.icon("database", size=16),  # Icono base de datos (datos reales)
                        rx.icon("test-tube", size=16)  # Icono laboratorio (datos de prueba)
                    ),
                    on_click=AppState.toggle_datos_dashboard,
                    variant="ghost",
                    size="2",
                    color_scheme=rx.cond(
                        AppState.usar_datos_reales_dashboard,
                        "green",  # Verde para datos reales
                        "orange"  # Naranja para datos random
                    )
                ),
                content=rx.cond(
                    AppState.usar_datos_reales_dashboard,
                    "Datos Reales (click para random)",
                    "Datos Random (click para reales)"
                ),
            ),
            align="center",
            width="100%",
            margin_bottom="1em"
        ),
        rx.match(
            AppState.selected_tab,
            (
                "Pacientes",
                render_chart(
                    key="Pacientes",
                    color="blue",
                    gradient_id="gradient-blue"
                )
            ),
            (
                "Ingresos",
                render_chart(
                    key="Ingresos",
                    color="green",
                    gradient_id="gradient-green"
                )
            ),
            (
                "Consultas",
                render_chart(
                    key="Consultas",
                    color="orange",
                    gradient_id="gradient-orange"
                )
            ),
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        padding="24px",
        width="100%"
    )