from ..state.app_state import AppState
import reflex as rx
from dental_system.styles.themes import (COLORS, SHADOWS, dark_crystal_card,DARK_THEME)
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
    📊 COMPONENTE PRINCIPAL DE GRÁFICOS - DATOS REALES

    CARACTERÍSTICAS:
    - Datos reales desde dashboard_service (últimos 30 días)
    - Toggle entre área y barras
    - Selector de métricas (Pacientes/Ingresos/Consultas)
    - Adaptación por rol de usuario
    """
    return rx.box(
        rx.hstack(
            chart_toggle(),
            rx.spacer(),
            custom_segmented_control(),
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
        width="100%"
    )


# ==========================================
# 📈 GRÁFICOS DE REPORTES - REUTILIZA COMPONENTES
# ==========================================

def graficas_reportes() -> rx.Component:
    """
    📊 GRÁFICOS DE EVOLUCIÓN TEMPORAL PARA REPORTES

    REUTILIZA:
    - Componentes de render_chart (área/barras)
    - Tooltips y gradientes personalizados
    - Toggle de área/barras

    USA DATOS DE:
    - AppState.datos_evolucion_activa (computed var de reportes)
    - AppState.tab_grafico_activo (estado de reportes)
    - AppState.cambiar_tab_grafico (método de reportes)
    """
    return rx.box(
        rx.hstack(
            chart_toggle(),  # Reutilizar toggle
            rx.spacer(),
            # Segmented control específico para reportes
            rx.segmented_control.root(
                rx.segmented_control.item("Pacientes Nuevos", value="pacientes_nuevos"),
                rx.segmented_control.item("Consultas", value="consultas"),
                rx.segmented_control.item("Ingresos", value="ingresos"),
                default_value="pacientes_nuevos",
                on_change=AppState.cambiar_tab_grafico,  # Método de reportes
                margin_bottom="1.5em",
                radius="full"
            ),
            align="center",
            width="100%",
            margin_bottom="1em"
        ),
        rx.match(
            AppState.tab_grafico_activo,
            (
                "pacientes_nuevos",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_pacientes,
                    key="valor",
                    color="blue",
                    gradient_id="gradient-reportes-blue"
                )
            ),
            (
                "consultas",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_consultas,
                    key="valor",
                    color="orange",
                    gradient_id="gradient-reportes-orange"
                )
            ),
            (
                "ingresos",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_ingresos,
                    key="valor",
                    color="green",
                    gradient_id="gradient-reportes-green"
                )
            ),
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )


def _render_chart_reportes(data: list, key: str, color: str, gradient_id: str) -> rx.Component:
    """
    Renderiza gráfico para reportes (reutiliza lógica de render_chart)
    Formato de datos: [{"fecha": "2025-01-01", "valor": 5}, ...]
    """
    return rx.box(
        rx.cond(
            AppState.area_toggle,
            rx.recharts.area_chart(
                rx.recharts.area(
                    data_key=key,
                    fill=f"url(#{gradient_id})",
                    stroke=color,
                    type_="natural"
                ),
                rx.recharts.x_axis(data_key="fecha", axis_line=False, tick_line=False),
                create_gradient(color, gradient_id),
                custom_tooltip(color),
                data=data,  # Datos de reportes
                height=300,
                width="100%"
            ),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    data_key=key,
                    fill=color,
                    radius=[4, 4, 0, 0]
                ),
                rx.recharts.x_axis(data_key="fecha", axis_line=False, tick_line=False),
                custom_tooltip(color),
                data=data,  # Datos de reportes
                height=300,
                width="100%"
            )
        ),
        width="100%"
    )


# ==========================================
# 📈 GRÁFICOS DE REPORTES ODONTÓLOGO - REUTILIZA COMPONENTES
# ==========================================

def graficas_reportes_odontologo() -> rx.Component:
    """
    📊 GRÁFICOS DE EVOLUCIÓN TEMPORAL PARA REPORTES ODONTÓLOGO

    REUTILIZA:
    - Componentes de render_chart (área/barras)
    - Tooltips y gradientes personalizados
    - Toggle de área/barras

    USA DATOS DE:
    - AppState.evolucion_temporal_ingresos_odontologo
    - AppState.evolucion_temporal_intervenciones_odontologo
    - AppState.tab_grafico_odontologo (estado de reportes)
    - AppState.cambiar_tab_grafico_odontologo (método de reportes)
    """
    return rx.box(
        rx.hstack(
            chart_toggle(),  # Reutilizar toggle
            rx.spacer(),
            # Segmented control específico para reportes odontólogo
            rx.segmented_control.root(
                rx.segmented_control.item("Ingresos", value="ingresos"),
                rx.segmented_control.item("Intervenciones", value="intervenciones"),
                default_value="ingresos",
                on_change=AppState.cambiar_tab_grafico_odontologo,  # Método de reportes
                margin_bottom="1.5em",
                radius="full"
            ),
            align="center",
            width="100%",
            margin_bottom="1em"
        ),
        rx.match(
            AppState.tab_grafico_odontologo,
            (
                "ingresos",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_ingresos_odontologo,
                    key="valor",
                    color="green",
                    gradient_id="gradient-reportes-odontologo-green"
                )
            ),
            (
                "intervenciones",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_intervenciones_odontologo,
                    key="valor",
                    color="blue",
                    gradient_id="gradient-reportes-odontologo-blue"
                )
            ),
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )


# ==========================================
# 📈 GRÁFICOS DE REPORTES ADMINISTRADOR - REUTILIZA COMPONENTES
# ==========================================

def graficas_reportes_admin() -> rx.Component:
    """
    📊 GRÁFICOS DE EVOLUCIÓN TEMPORAL PARA REPORTES ADMINISTRADOR

    REUTILIZA:
    - Componentes de render_chart (área/barras)
    - Tooltips y gradientes personalizados
    - Toggle de área/barras

    USA DATOS DE:
    - AppState.evolucion_temporal_consultas_admin
    - AppState.evolucion_temporal_ingresos_admin
    - AppState.evolucion_temporal_pacientes_admin
    - AppState.tab_grafico_admin (estado de reportes)
    - AppState.cambiar_tab_grafico_admin (método de reportes)
    """
    return rx.box(
        rx.hstack(
            chart_toggle(),  # Reutilizar toggle
            rx.spacer(),
            # Segmented control específico para reportes administrador
            rx.segmented_control.root(
                rx.segmented_control.item("Consultas", value="consultas"),
                rx.segmented_control.item("Ingresos", value="ingresos"),
                rx.segmented_control.item("Pacientes Nuevos", value="pacientes_nuevos"),
                default_value="consultas",
                on_change=AppState.cambiar_tab_grafico_admin,  # Método de reportes
                margin_bottom="1.5em",
                radius="full"
            ),
            align="center",
            width="100%",
            margin_bottom="1em"
        ),
        rx.match(
            AppState.tab_grafico_admin,
            (
                "consultas",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_consultas_admin,
                    key="valor",
                    color="blue",
                    gradient_id="gradient-reportes-admin-blue"
                )
            ),
            (
                "ingresos",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_ingresos_admin,
                    key="valor",
                    color="green",
                    gradient_id="gradient-reportes-admin-green"
                )
            ),
            (
                "pacientes_nuevos",
                _render_chart_reportes(
                    data=AppState.evolucion_temporal_pacientes_admin,
                    key="valor",
                    color="orange",
                    gradient_id="gradient-reportes-admin-orange"
                )
            ),
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )


# ==========================================
# 🥧 PIE CHART CARD - NUEVO COMPONENTE
# ==========================================

def pie_chart_card(
    title: str,
    data: list,  # [{"name": "USD", "value": 4357.75}, ...]
    subtitle: str = "",
    height: int = 320
) -> rx.Component:
    """
    📊 Card con gráfico de torta redondo (pie chart)

    USADO EN:
    - Distribución de pagos USD vs BS (Gerente)
    - Distribución de ingresos odontólogo (Odontólogo)
    - Tipos de consulta (Administrador)

    Args:
        title: Título del card
        data: Lista de dicts con name, value y fill (color)
        subtitle: Subtítulo opcional
        height: Altura del gráfico en px

    Returns:
        Card con pie chart estilizado
    """
    return rx.box(
        rx.vstack(
            # Header
            rx.vstack(
                rx.heading(
                    title,
                    size="5",
                    weight="bold",
                    style={
                        "color": DARK_THEME["colors"]["text_primary"],
                        "margin_bottom": "4px"
                    }
                ),
                rx.cond(
                    subtitle != "",
                    rx.text(
                        subtitle,
                        size="2",
                        style={
                            "color": DARK_THEME["colors"]["text_secondary"]
                        }
                    )
                ),
                spacing="1",
                align="start",
                width="100%",
                margin_bottom="4"
            ),

            # Pie Chart
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    inner_radius=0,
                    outer_radius=80,
                    label=True,
                    label_line=True
                ),
                rx.recharts.legend(
                    icon_type="circle",
                    layout="horizontal",
                    vertical_align="bottom"
                ),
                width="100%",
                height=height
            ),

            # Stats summary (abajo del gráfico)
            rx.hstack(
                rx.foreach(
                    data,
                    lambda item: rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            background=item["fill"],
                            border_radius="2px"
                        ),
                        rx.text(
                            f"{item['name']}: ${item['value']:,.2f}",
                            size="2",
                            weight="medium",
                            style={
                                "color": DARK_THEME["colors"]["text_primary"]
                            }
                        ),
                        spacing="2",
                        align="center"
                    )
                ),
                spacing="4",
                wrap="wrap",
                width="100%",
                justify="center"
            ),

            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )