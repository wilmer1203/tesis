"""
🦷 DASHBOARD ODONTÓLOGO - MÉTRICAS Y PRODUCTIVIDAD PERSONAL
============================================================

Dashboard especializado para odontólogos mostrando:
- 5 métricas clave (ingresos, consultas, servicios, tiempo)
- Gráficos de tendencia (últimos 30 días)
- Top servicios aplicados hoy
- Lista de consultas en cola

Diseñado específicamente para rol 'odontologo'
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout, page_header, stat_card, refresh_button
from dental_system.components.charts import chart_toggle
from dental_system.styles.themes import COLORS, SHADOWS, dark_crystal_card

# ==========================================
# COMPONENTES DEL DASHBOARD ODONTÓLOGO
# ==========================================

def odontologist_stats_grid() -> rx.Component:
    """Grid de estadísticas del odontólogo - 5 métricas principales"""
    return rx.grid(
        # Card 1: Ingresos del Mes (USD)
        stat_card(
            title="Ingresos del Mes",
            value=rx.cond(
                AppState.dashboard_stats_odontologo,
                f"${AppState.dashboard_stats_odontologo.get('ingresos_mes', 0):,.0f}",
                "$0"
            ),
            icon="dollar-sign",
            color=COLORS["success"]["500"],
        ),

        # Card 2: Ingresos Hoy (USD)
        stat_card(
            title="Ingresos Hoy",
            value=rx.cond(
                AppState.dashboard_stats_odontologo,
                f"${AppState.dashboard_stats_odontologo.get('ingresos_hoy', 0):,.0f}",
                "$0"
            ),
            icon="trending-up",
            color=COLORS["secondary"]["500"],
        ),

        # Card 3: Consultas Hoy (Intervenciones realizadas)
        stat_card(
            title="Consultas Hoy",
            value=rx.cond(
                AppState.dashboard_stats_odontologo,
                f"{AppState.dashboard_stats_odontologo.get('consultas_hoy', 0)}",
                "0"
            ),
            icon="activity",
            color=COLORS["primary"]["500"],
        ),

        # Card 4: Servicios Aplicados
        stat_card(
            title="Servicios Aplicados",
            value=rx.cond(
                AppState.dashboard_stats_odontologo,
                f"{AppState.dashboard_stats_odontologo.get('servicios_aplicados', 0)}",
                "0"
            ),
            icon="check-circle",
            color=COLORS["blue"]["500"],
        ),

        # Card 5: Tiempo Promedio
        stat_card(
            title="Tiempo Promedio",
            value=rx.cond(
                AppState.dashboard_stats_odontologo,
                f"{AppState.dashboard_stats_odontologo.get('tiempo_promedio_minutos', 0):.0f} min",
                "0 min"
            ),
            icon="clock",
            color=COLORS["warning"]["500"],
        ),

        grid_template_columns=[
            "1fr",                  # Móvil: 1 columna
            "repeat(1, 1fr)",       # Móvil grande: 1 columna
            "repeat(2, 1fr)",       # Tablet: 2 columnas
            "repeat(3, 1fr)",       # Desktop pequeño: 3 columnas
            "repeat(5, 1fr)",       # Desktop: 5 columnas
        ],
        spacing="6",
        width="100%"
    )


def odontologist_charts() -> rx.Component:
    """Gráficos del odontólogo (Consultas e Ingresos)"""
    return rx.box(
        # Control superior: Tab selector + Toggle de gráfico
        rx.hstack(
            rx.segmented_control.root(
                rx.segmented_control.item("Consultas", value="Consultas"),
                rx.segmented_control.item("Ingresos", value="Ingresos"),
                default_value="Consultas",
                on_change=AppState.set_selected_tab,
                radius="full"
            ),
            chart_toggle(),  # ✅ Toggle para cambiar entre área/barra
            justify="between",
            align="center",
            width="100%",
            margin_bottom="1em"
        ),

        # Gráfico dinámico según tab seleccionado
        rx.match(
            AppState.selected_tab,
            (
                "Consultas",
                rx.cond(
                    AppState.area_toggle,
                    # Gráfico de área
                    rx.recharts.area_chart(
                        rx.recharts.area(
                            data_key="Consultas",
                            fill="url(#gradient-blue)",
                            stroke=rx.color("blue", 7),
                            type_="natural"
                        ),
                        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                        rx.recharts.graphing_tooltip(
                            content_style={
                                "backgroundColor": rx.color("gray", 1),
                                "borderRadius": "var(--radius-2)",
                                "borderWidth": "1px",
                                "borderColor": rx.color("blue", 7),
                                "padding": "0.5rem",
                                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                            },
                        ),
                        rx.el.svg.defs(
                            rx.el.svg.linear_gradient(
                                rx.el.svg.stop(offset="5%", stop_color=rx.color("blue", 7), stop_opacity=0.8),
                                rx.el.svg.stop(offset="95%", stop_color=rx.color("blue", 7), stop_opacity=0),
                                id="gradient-blue",
                                x1="0",
                                x2="0",
                                y1="0",
                                y2="1",
                            )
                        ),
                        data=AppState.consultas_data_odontologo,
                        height=300,
                        width="100%"
                    ),
                    # Gráfico de barras
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key="Consultas",
                            fill=rx.color("blue", 7),
                            radius=[4, 4, 0, 0]
                        ),
                        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                        rx.recharts.graphing_tooltip(
                            content_style={
                                "backgroundColor": rx.color("gray", 1),
                                "borderRadius": "var(--radius-2)",
                                "borderWidth": "1px",
                                "borderColor": rx.color("blue", 7),
                                "padding": "0.5rem",
                                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                            },
                        ),
                        data=AppState.consultas_data_odontologo,
                        height=300,
                        width="100%"
                    )
                )
            ),
            (
                "Ingresos",
                rx.cond(
                    AppState.area_toggle,
                    # Gráfico de área
                    rx.recharts.area_chart(
                        rx.recharts.area(
                            data_key="Ingresos",
                            fill="url(#gradient-green)",
                            stroke=rx.color("green", 7),
                            type_="natural"
                        ),
                        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                        rx.recharts.graphing_tooltip(
                            content_style={
                                "backgroundColor": rx.color("gray", 1),
                                "borderRadius": "var(--radius-2)",
                                "borderWidth": "1px",
                                "borderColor": rx.color("green", 7),
                                "padding": "0.5rem",
                                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                            },
                        ),
                        rx.el.svg.defs(
                            rx.el.svg.linear_gradient(
                                rx.el.svg.stop(offset="5%", stop_color=rx.color("green", 7), stop_opacity=0.8),
                                rx.el.svg.stop(offset="95%", stop_color=rx.color("green", 7), stop_opacity=0),
                                id="gradient-green",
                                x1="0",
                                x2="0",
                                y1="0",
                                y2="1",
                            )
                        ),
                        data=AppState.ingresos_data_odontologo,
                        height=300,
                        width="100%"
                    ),
                    # Gráfico de barras
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key="Ingresos",
                            fill=rx.color("green", 7),
                            radius=[4, 4, 0, 0]
                        ),
                        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                        rx.recharts.graphing_tooltip(
                            content_style={
                                "backgroundColor": rx.color("gray", 1),
                                "borderRadius": "var(--radius-2)",
                                "borderWidth": "1px",
                                "borderColor": rx.color("green", 7),
                                "padding": "0.5rem",
                                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                            },
                        ),
                        data=AppState.ingresos_data_odontologo,
                        height=300,
                        width="100%"
                    )
                )
            ),
        ),

        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        padding="24px",
        width="100%"
    )


def top_services_chart() -> rx.Component:
    """Gráfico de barras con top servicios aplicados hoy"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text("Servicios Más Aplicados Hoy", size="4", weight="bold", color=COLORS["gray"]["800"]),
                rx.spacer(),
                rx.badge(
                    f"{AppState.top_servicios_odontologo.length()}",
                    color_scheme="blue",
                    variant="soft"
                ),
                align="center",
                width="100%",
                margin_bottom="4"
            ),

            # Gráfico de barras horizontal
            rx.cond(
                AppState.top_servicios_odontologo,
                rx.recharts.bar_chart(
                    rx.recharts.bar(
                        data_key="count",
                        fill=COLORS["primary"]["500"],
                        radius=[0, 4, 4, 0]
                    ),
                    rx.recharts.y_axis(
                        data_key="servicio_nombre",
                        type_="category",
                        width=150,
                        axis_line=False,
                        tick_line=False
                    ),
                    rx.recharts.x_axis(type_="number", axis_line=False, tick_line=False),
                    rx.recharts.graphing_tooltip(
                        content_style={
                            "backgroundColor": rx.color("gray", 1),
                            "borderRadius": "var(--radius-2)",
                            "padding": "0.5rem",
                        },
                    ),
                    data=AppState.top_servicios_odontologo,
                    layout="vertical",
                    height=250,
                    width="100%"
                ),
                # Placeholder cuando no hay datos
                rx.center(
                    rx.vstack(
                        rx.icon("package", size=40, color=COLORS["gray"]["400"]),
                        rx.text("No hay servicios aplicados hoy", color=COLORS["gray"]["500"], size="2"),
                        spacing="2",
                        align="center"
                    ),
                    height="250px",
                    width="100%"
                )
            ),

            spacing="4",
            align_items="stretch",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["success"]["500"], hover_lift="4px"),
        padding="24px",
        width="100%"
    )


def consultation_queue_list() -> rx.Component:
    """Lista de consultas en cola del odontólogo"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text("Mi Cola de Atención", size="4", weight="bold", color=COLORS["gray"]["800"]),
                rx.spacer(),
                rx.badge(
                    f"{AppState.consultas_asignadas.length()}",
                    color_scheme="green",
                    variant="soft"
                ),
                rx.button(
                    "Ver Todas",
                    size="2",
                    variant="ghost",
                    color=COLORS["primary"]["500"],
                    on_click=rx.redirect("/odontologia")
                ),
                align="center",
                width="100%",
                margin_bottom="4"
            ),

            # Lista de consultas
            rx.cond(
                AppState.consultas_asignadas,
                rx.vstack(
                    rx.foreach(
                        AppState.consultas_asignadas[:5],  # Mostrar solo las primeras 5
                        lambda consulta: rx.box(
                            rx.hstack(
                                # Info del paciente
                                rx.vstack(
                                    rx.text(
                                        f"{consulta.paciente_nombre}",
                                        size="3",
                                        weight="medium",
                                        color=COLORS["gray"]["900"]
                                    ),
                                    rx.text(
                                        f"CI: {consulta.paciente_documento}",
                                        size="2",
                                        color=COLORS["gray"]["600"]
                                    ),
                                    spacing="0",
                                    align_items="start"
                                ),
                                rx.spacer(),
                                # Estado
                                rx.badge(
                                    rx.match(
                                        consulta.estado,
                                        ("en_espera", "En Espera"),
                                        ("en_atencion", "En Atención"),
                                        ("completada", "Completada"),
                                        "Desconocido"
                                    ),
                                    color_scheme=rx.match(
                                        consulta.estado,
                                        ("en_espera", "orange"),
                                        ("en_atencion", "blue"),
                                        ("completada", "green"),
                                        "gray"
                                    ),
                                    variant="soft"
                                ),
                                # Botón de acción
                                rx.button(
                                    rx.icon("arrow-right", size=16),
                                    size="2",
                                    variant="soft",
                                    on_click=rx.redirect("/intervencion")
                                ),
                                align="center",
                                width="100%"
                            ),
                            padding="16px",
                            background=COLORS["gray"]["50"],
                            border_radius="12px",
                            border=f"1px solid {COLORS['gray']['200']}",
                            _hover={
                                "background": COLORS["gray"]["100"],
                                "border_color": COLORS["primary"]["300"]
                            },
                            transition="all 0.2s",
                            width="100%",
                            cursor="pointer"
                        )
                    ),
                    spacing="3",
                    width="100%"
                ),
                # Placeholder cuando no hay consultas
                rx.center(
                    rx.vstack(
                        rx.icon("calendar-x", size=40, color=COLORS["gray"]["400"]),
                        rx.text("No hay consultas asignadas", color=COLORS["gray"]["500"], size="2"),
                        spacing="2",
                        align="center"
                    ),
                    height="150px",
                    width="100%"
                )
            ),

            spacing="4",
            align_items="stretch",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["blue"]["500"], hover_lift="4px"),
        padding="24px",
        width="100%"
    )


# ==========================================
# COMPONENTE PRINCIPAL DEL DASHBOARD ODONTÓLOGO
# ==========================================

def dashboard_odontologo_page() -> rx.Component:
    """Página principal del dashboard del odontólogo"""
    return medical_page_layout(
        rx.vstack(
            # Header de la página
            page_header(
                "Dashboard Odontológico",
                "Métricas y productividad personal",
                actions=[
                    refresh_button(
                        text="Actualizar datos",
                        on_click=AppState.cargar_dashboard_odontologo_completo,
                        loading=AppState.cargando_dashboard_odontologo
                    )
                ]
            ),

            # Contenido principal
            rx.cond(
                AppState.cargando_dashboard_odontologo,
                # Loading state
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3", color=COLORS["primary"]["500"]),
                        rx.text("Cargando datos...", color=COLORS["gray"]["600"], size="3"),
                        spacing="3",
                        align="center"
                    ),
                    padding="40px",
                    width="100%"
                ),
                # Contenido cargado
                rx.box(
                    # Grid de estadísticas principales (5 cards)
                    odontologist_stats_grid(),

                    # Grid de información adicional
                    rx.grid(
                        # Columna izquierda - Gráficos
                        odontologist_charts(),

                        # Columna derecha - Top servicios
                        top_services_chart(),

                        grid_template_columns=[
                            "1fr",                  # Móvil: 1 columna
                            "repeat(1, 1fr)",       # Móvil grande: 1 columna
                            "repeat(2, 1fr)",       # Tablet: 2 columnas
                            "repeat(2, 1fr)",       # Desktop: 2 columnas
                        ],
                        margin_top="24px",
                        spacing="6",
                        width="100%",
                    ),

                    # Lista de consultas en cola (ancho completo)
                    rx.box(
                        consultation_queue_list(),
                        margin_top="24px",
                        width="100%"
                    ),

                    spacing="6",
                    padding="24px",
                    width="100%",
                )
            ),

            spacing="3",
            width="100%",
            min_height="100vh",

            # 🚀 CARGAR DATOS AL MONTAR LA PÁGINA
            on_mount=AppState.cargar_dashboard_odontologo_completo()
        )
    )
