
import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout, page_header, stat_card, refresh_button
from dental_system.components.charts import graficas_resume
from dental_system.styles.themes import COLORS, SHADOWS,GRADIENTS,dark_header_style,DARK_THEME, dark_crystal_card

# ==========================================
# COMPONENTES DEL DASHBOARD - GERENTE
# ==========================================

def quick_stats_grid() -> rx.Component:
    """Grid de estadísticas rápidas - 5 métricas principales con DATOS REALES"""
    return rx.grid(
        # Card 1: Ingresos del Mes
        stat_card(
            title="Ingresos del Mes",
            value=rx.cond(
                AppState.dashboard_stats,
                f"${AppState.dashboard_stats.get('ingresos_mes', 0):,.0f}",
                "$0"
            ),
            icon="dollar-sign",
            color=COLORS["success"]["500"],
        ),
        stat_card(
            title="Ingresos Hoy",
            value=rx.cond(
                AppState.dashboard_stats,
                f"${AppState.dashboard_stats.get('ingresos_hoy_total', 0):,.0f}",
                "$0"
            ),
            icon="dollar-sign",
            color=COLORS["secondary"]["500"]
        ),
        stat_card(
            title="Consultas Hoy",
            value=rx.cond(
                AppState.dashboard_stats,
                f"{AppState.dashboard_stats.get('consultas_completadas', 0)}/{AppState.dashboard_stats.get('consultas_hoy_total', 0)}",
                "0/0"
            ),
            icon="calendar",
            color=COLORS["primary"]["500"]
        ),
        stat_card(
            title="Servicios Aplicados Hoy",
            value=rx.cond(
                AppState.dashboard_stats,
                f"{AppState.dashboard_stats.get('servicios_aplicados', 0)}",
                "0"
            ),
            icon="activity",
            color=COLORS["blue"]["500"]
        ),
        stat_card(
            title="Tiempo Promedio",
            value=rx.cond(
                AppState.dashboard_stats,
                f"{AppState.dashboard_stats.get('tiempo_promedio_minutos', 0):.0f} min",
                "0 min"
            ),
            icon="clock",
            color=COLORS["warning"]["500"]
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

def recent_activity_card() -> rx.Component:
    """Tarjeta de actividad reciente"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Actividad Reciente", size="4", weight="bold", color=COLORS["gray"]["800"]),
                rx.spacer(),
                rx.button(
                    "Ver Todo",
                    size="2",
                    variant="ghost",
                    color=COLORS["primary"]["500"]
                ),
                align="center",
                width="100%"
            ),
            
            rx.vstack(
                # Actividad 1
                rx.hstack(
                    rx.box(
                        rx.icon("user-plus", size=16, color="white"),
                        background=COLORS["success"],
                        border_radius="50%",
                        padding="8px"
                    ),
                    rx.vstack(
                        rx.text("Nuevo paciente registrado", size="2", weight="medium"),
                        rx.text("Carlos Rodríguez - HC000156", size="2", color=COLORS["gray"]["600"]),
                        spacing="0",
                        align_items="start"
                    ),
                    rx.spacer(),
                    rx.text("hace 2h", size="2", color=COLORS["gray"]["600"]),
                    align="center",
                    width="100%"
                ),
                
                # Actividad 2
                rx.hstack(
                    rx.box(
                        rx.icon("calendar-check", size=16, color="white"),
                        background=COLORS["primary"]["500"],
                        border_radius="50%",
                        padding="8px"
                    ),
                    rx.vstack(
                        rx.text("Consulta completada", size="3", weight="medium"),
                        rx.text("Dra. María González - Endodoncia", size="2", color=COLORS["gray"]["600"]),
                        spacing="0",
                        align_items="start"
                    ),
                    rx.spacer(),
                    rx.text("hace 1h", size="2", color=COLORS["gray"]["600"]),
                    align="center",
                    width="100%"
                ),
                
                # Actividad 3
                rx.hstack(
                    rx.box(
                        rx.icon("dollar-sign", size=16, color="white"),
                        background=COLORS["secondary"]["500"],
                        border_radius="50%",
                        padding="8px"
                    ),
                    rx.vstack(
                        rx.text("Pago procesado", size="3", weight="medium"),
                        rx.text("$125.000 - Consulta General", size="2", color=COLORS["gray"]["600"]),
                        spacing="0",
                        align_items="start"
                    ),
                    rx.spacer(),
                    rx.text("hace 30m", size="2", color=COLORS["gray"]["600"]),
                    align="center",
                    width="100%"
                ),
                
                spacing="4",
                width="100%"
            ),
            
            spacing="6",
            align_items="stretch",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["warning"]["500"], hover_lift="4px"),
        width="100%"
    )

# ==========================================
# COMPONENTES DEL DASHBOARD - ADMINISTRADOR
# ==========================================

def quick_stats_grid_admin() -> rx.Component:
    """Grid de estadísticas rápidas - 6 métricas principales para ADMINISTRADOR (HOY)"""
    return rx.grid(
        # Card 1: Consultas Hoy
        stat_card(
            title="Consultas Hoy",
            value=rx.cond(
                AppState.dashboard_stats_admin,
                f"{AppState.dashboard_stats_admin.get('consultas_hoy_completadas', 0)}/{AppState.dashboard_stats_admin.get('consultas_hoy_total', 0)}",
                "0/0"
            ),
            icon="calendar",
            color=COLORS["primary"]["500"],
        ),
        # Card 2: Ingresos Hoy
        stat_card(
            title="Ingresos Hoy (USD)",
            value=rx.cond(
                AppState.dashboard_stats_admin,
                f"${AppState.dashboard_stats_admin.get('ingresos_hoy', 0):,.2f}",
                "$0.00"
            ),
            icon="dollar-sign",
            color=COLORS["success"]["500"]
        ),
        # Card 3: Pagos Realizados
        stat_card(
            title="Pagos Realizados",
            value=rx.cond(
                AppState.dashboard_stats_admin,
                f"{AppState.dashboard_stats_admin.get('pagos_realizados_hoy', 0)}",
                "0"
            ),
            icon="credit-card",
            color=COLORS["secondary"]["500"]
        ),
        # Card 4: Servicios Aplicados
        stat_card(
            title="Servicios Aplicados",
            value=rx.cond(
                AppState.dashboard_stats_admin,
                f"{AppState.dashboard_stats_admin.get('servicios_aplicados_hoy', 0)}",
                "0"
            ),
            icon="activity",
            color=COLORS["blue"]["500"]
        ),
        # Card 5: Intervenciones Hoy
        stat_card(
            title="Intervenciones",
            value=rx.cond(
                AppState.dashboard_stats_admin,
                f"{AppState.dashboard_stats_admin.get('intervenciones_hoy', 0)}",
                "0"
            ),
            icon="zap",
            color=COLORS["warning"]["500"]  # Naranja/amarillo
        ),
        # Card 6: Pacientes Nuevos Hoy
        stat_card(
            title="Pacientes Nuevos",
            value=rx.cond(
                AppState.dashboard_stats_admin,
                f"{AppState.dashboard_stats_admin.get('pacientes_nuevos_hoy', 0)}",
                "0"
            ),
            icon="user-plus",
            color=COLORS["info"]["500"]  # Azul
        ),
        grid_template_columns=[
            "1fr",                  # Móvil: 1 columna
            "repeat(1, 1fr)",       # Móvil grande: 1 columna
            "repeat(2, 1fr)",       # Tablet: 2 columnas
            "repeat(3, 1fr)",       # Desktop pequeño: 3 columnas
            "repeat(6, 1fr)",       # Desktop: 6 columnas
        ],
        spacing="6",
        width="100%"
    )

def consultas_por_estado_chart_admin() -> rx.Component:
    """Gráfico de barras horizontales: Consultas por Estado (HOY)"""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Consultas por Estado (Hoy)",
                size="5",
                weight="bold",
                style={
                    "color": DARK_THEME["colors"]["text_primary"],
                    "margin_bottom": "16px"
                }
            ),
            rx.cond(
                AppState.consultas_hoy_por_estado_admin,
                rx.recharts.bar_chart(
                    rx.recharts.bar(
                        data_key="cantidad",
                        fill=rx.color("blue", 7),
                        radius=[0, 4, 4, 0]
                    ),
                    rx.recharts.x_axis(data_key="estado", axis_line=False, tick_line=False),
                    rx.recharts.y_axis(axis_line=False, tick_line=False),
                    rx.recharts.graphing_tooltip(
                        content_style={
                            "backgroundColor": rx.color("gray", 1),
                            "borderRadius": "var(--radius-2)",
                            "borderWidth": "1px",
                            "borderColor": rx.color("blue", 7),
                            "padding": "0.5rem",
                        }
                    ),
                    data=AppState.consultas_hoy_por_estado_admin,
                    layout="vertical",
                    height=300,
                    width="100%"
                ),
                rx.center(
                    rx.text("No hay datos de consultas para hoy", color=DARK_THEME["colors"]["text_secondary"]),
                    height="300px"
                )
            ),
            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )

def consultas_por_odontologo_chart_admin() -> rx.Component:
    """Gráfico de barras: Consultas por Odontólogo (HOY)"""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Consultas por Odontólogo (Hoy)",
                size="5",
                weight="bold",
                style={
                    "color": DARK_THEME["colors"]["text_primary"],
                    "margin_bottom": "16px"
                }
            ),
            rx.cond(
                AppState.consultas_hoy_por_odontologo_admin,
                rx.recharts.bar_chart(
                    rx.recharts.bar(
                        data_key="cantidad",
                        fill=rx.color("green", 7),
                        radius=[4, 4, 0, 0]
                    ),
                    rx.recharts.x_axis(data_key="nombre", axis_line=False, tick_line=False),
                    rx.recharts.y_axis(axis_line=False, tick_line=False),
                    rx.recharts.graphing_tooltip(
                        content_style={
                            "backgroundColor": rx.color("gray", 1),
                            "borderRadius": "var(--radius-2)",
                            "borderWidth": "1px",
                            "borderColor": rx.color("green", 7),
                            "padding": "0.5rem",
                        }
                    ),
                    data=AppState.consultas_hoy_por_odontologo_admin,
                    height=300,
                    width="100%"
                ),
                rx.center(
                    rx.text("No hay odontólogos atendiendo hoy", color=DARK_THEME["colors"]["text_secondary"]),
                    height="300px"
                )
            ),
            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["success"]["500"], hover_lift="4px"),
        width="100%"
    )

# ==========================================
# PÁGINAS COMPLETAS POR ROL
# ==========================================

def dashboard_page_admin() -> rx.Component:
    """Página del dashboard del ADMINISTRADOR - Tiempo real (HOY)"""
    return medical_page_layout(
        rx.vstack(
            # Header de la página
            page_header(
                "Dashboard Administrativo",
                "Monitoreo en tiempo real de las operaciones del día",
                actions=[
                    refresh_button(
                        text="Actualizar datos",
                        on_click=AppState.cargar_dashboard_admin,
                        loading=AppState.cargando_dashboard_admin
                    )
                ]
            ),
            # Contenido principal
            rx.cond(
                AppState.cargando_dashboard_admin,
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3", color=COLORS["primary"]["500"]),
                        rx.text("Cargando datos de hoy...", color=COLORS["gray"]["600"], size="3"),
                        spacing="3",
                        align="center"
                    ),
                    padding="40px",
                    width="100%"
                ),
                rx.box(
                    # Grid de 6 estadísticas principales
                    quick_stats_grid_admin(),

                    # Grid de gráficos (2 columnas)
                    rx.grid(
                        consultas_por_estado_chart_admin(),
                        consultas_por_odontologo_chart_admin(),
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
                    spacing="6",
                    padding="24px",
                    width="100%",
                )
            ),
            spacing="3",
            width="100%",
            min_height="100vh",
            # 🚀 CARGAR DATOS REALES AL MONTAR
            on_mount=AppState.cargar_dashboard_admin()
        )
    )

def dashboard_page() -> rx.Component:
    """Página principal del dashboard del gerente - V2.0 CON DATOS REALES"""
    return medical_page_layout(
        rx.vstack(
        # Header de la página
        page_header(
            "Dashboard de Monitoreo",
            "Monitoreo en tiempo real del flujo de pacientes por orden de llegada",
            actions=[
                refresh_button(
                    text="Actualizar datos",
                    on_click=AppState.cargar_dashboard_gerente_completo,
                    loading=AppState.cargando_dashboard
                )
            ]
        ),
        # Contenido principal
        rx.cond(
            AppState.cargando_dashboard,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color=COLORS["primary"]["500"]),
                    rx.text("Cargando datos reales...", color=COLORS["gray"]["600"], size="3"),
                    spacing="3",
                    align="center"
                ),
                padding="40px",
                width="100%"
            ),
            rx.box(
                # Grid de estadísticas principales (5 cards con datos reales)
                quick_stats_grid(),

                # Grid de información adicional
                rx.grid(
                    # Columna izquierda - Gráficos con toggle real/random
                    graficas_resume(),
                    # Columna derecha - Actividad reciente
                    recent_activity_card(),
                    grid_template_columns=[
                        "1fr",                  # Móvil: 1 columna
                        "repeat(1, 1fr)",       # Móvil grande: 1 columna
                        "repeat(2, 1fr)",       # Tablet: 2 columnas
                        "repeat(2, 1fr)",       # Desktop pequeño: 2 columnas
                    ],
                    margin_top="24px",
                    spacing="6",
                    width="100%",
                ),
                spacing="6",
                padding="24px",
                width="100%",
            )
        ),
        spacing="3",
        width="100%",
        min_height="100vh",
        # 🚀 CARGAR DATOS REALES AL MONTAR
        on_mount=AppState.cargar_dashboard_gerente_completo()
    )
    )

