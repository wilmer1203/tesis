
import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout, page_header, stat_card, refresh_button
from dental_system.components.charts import graficas_resume
from dental_system.components.table_components import crystal_search_input, consultas_dashboard_table, empty_state
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

def activity_item(actividad: rx.Var) -> rx.Component:
    """📌 Item individual de actividad reciente - CON DATOS REALES"""
    return rx.hstack(
        # Icono con color dinámico basado en tipo
        rx.box(
            rx.icon(
                rx.match(
                    actividad["tipo"],
                    ("paciente", "user-plus"),
                    ("consulta", "check-circle"),
                    ("pago", "dollar-sign"),
                    "circle"  # default
                ),
                size=16,
                color="white"
            ),
            background=rx.match(
                actividad["tipo"],
                ("paciente", "#00D4FF"),  # cyan
                ("consulta", "#00FF9D"),  # green
                ("pago", "#FFD700"),      # gold
                COLORS["gray"]["500"]     # default
            ),
            border_radius="50%",
            padding="8px"
        ),
        # Contenido
        rx.vstack(
            rx.text(
                actividad["titulo"],
                size="3",
                weight="medium",
                color=COLORS["gray"]["100"]  # ✅ FIXED: texto claro para tema oscuro
            ),
            rx.text(
                actividad["descripcion"],
                size="2",
                color=COLORS["gray"]["400"]  # ✅ FIXED: gris más claro
            ),
            spacing="0",
            align_items="start"
        ),
        rx.spacer(),
        # Tiempo relativo
        rx.text(
            actividad["tiempo_relativo"],
            size="2",
            color=COLORS["gray"]["400"]  # ✅ FIXED
        ),
        align="center",
        width="100%"
    )


def recent_activity_card() -> rx.Component:
    """🔔 Tarjeta de actividad reciente - CON DATOS REALES del sistema"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text(
                    "Actividad Reciente",
                    size="4",
                    weight="bold",
                    color=COLORS["gray"]["100"]  # ✅ FIXED: texto claro
                ),
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

            # Lista de actividades usando rx.foreach con datos reales
            rx.cond(
                AppState.actividades_recientes,
                rx.vstack(
                    rx.foreach(
                        AppState.actividades_recientes,
                        activity_item
                    ),
                    spacing="4",
                    width="100%"
                ),
                # Si no hay actividades
                rx.vstack(
                    rx.icon("inbox", size=24, color=COLORS["gray"]["500"]),
                    rx.text(
                        "No hay actividades recientes",
                        size="2",
                        color=COLORS["gray"]["400"],
                        text_align="center"
                    ),
                    spacing="2",
                    align="center",
                    padding="4"
                )
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
                    height="90%",
                    width="100%"
                ),
                empty_state(
                    "No hay datos de consultas para hoy",
                    "Los datos de consultas aparecerán aquí cuando estén disponibles.",
                    "bar-chart-2"
                )
            ),
            spacing="4",
            width="100%",
            height="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%",
        height="100%"
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
                    width="100%",
                    height="100%"
                ),
                empty_state(
                    "No hay odontólogos atendiendo hoy",
                    "Los datos de consultas por odontólogo aparecerán aquí cuando estén disponibles.",
                    "bar-chart-2"
                )
            ),
            spacing="4",
            width="100%",
            height="100%"
        ),
        **dark_crystal_card(color=COLORS["success"]["500"], hover_lift="4px"),
        width="100%",
        height="100%"
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
                        height="90%",
                    ),
                    spacing="6",
                    padding="24px",
                    width="100%",
                    height="90%",
                )
            ),
            spacing="3",
            width="100%",
            height="100%",
            # 🚀 CARGAR DATOS REALES AL MONTAR
            on_mount=AppState.cargar_dashboard_admin()
        )
    )

# ==========================================
# COMPONENTES DEL DASHBOARD - ASISTENTE
# ==========================================

def quick_stats_grid_asistente() -> rx.Component:
    """Grid de estadísticas básicas para ASISTENTE (solo lectura, métricas del día)"""
    return rx.grid(
        # Card 1: Consultas Hoy Total
        stat_card(
            title="Consultas Hoy",
            value=rx.cond(
                AppState.dashboard_stats_asistente,
                f"{AppState.dashboard_stats_asistente.get('consultas_hoy_total', 0)}",
                "0"
            ),
            icon="calendar",
            color=COLORS["primary"]["500"],
        ),
        # Card 2: Consultas Completadas
        stat_card(
            title="Completadas",
            value=rx.cond(
                AppState.dashboard_stats_asistente,
                f"{AppState.dashboard_stats_asistente.get('consultas_completadas', 0)}",
                "0"
            ),
            icon="check-circle",
            color=COLORS["success"]["500"]
        ),
        # Card 3: En Espera
        stat_card(
            title="En Espera",
            value=rx.cond(
                AppState.dashboard_stats_asistente,
                f"{AppState.dashboard_stats_asistente.get('consultas_en_espera', 0)}",
                "0"
            ),
            icon="clock",
            color=COLORS["warning"]["500"]
        ),
        # Card 4: Pacientes Atendidos
        stat_card(
            title="Pacientes Atendidos",
            value=rx.cond(
                AppState.dashboard_stats_asistente,
                f"{AppState.dashboard_stats_asistente.get('pacientes_atendidos_hoy', 0)}",
                "0"
            ),
            icon="users",
            color=COLORS["blue"]["500"]
        ),
        grid_template_columns=[
            "1fr",                  # Móvil: 1 columna
            "repeat(2, 1fr)",       # Tablet: 2 columnas
            "repeat(4, 1fr)",       # Desktop: 4 columnas
        ],
        spacing="6",
        width="100%"
    )

def consultas_por_estado_chart_asistente() -> rx.Component:
    """Gráfico de consultas por estado para asistente (reutiliza datos del admin)"""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Estado de Consultas Hoy",
                size="4",
                weight="bold",
                color=DARK_THEME["colors"]["text_primary"],
            ),
            rx.cond(
                AppState.consultas_hoy_por_estado_admin,
                rx.recharts.bar_chart(
                    rx.recharts.bar(
                        data_key="cantidad",
                        fill=rx.color("cyan", 7),
                        radius=[0, 4, 4, 0]
                    ),
                    rx.recharts.x_axis(data_key="estado", axis_line=False, tick_line=False),
                    rx.recharts.y_axis(axis_line=False, tick_line=False),
                    rx.recharts.graphing_tooltip(
                        content_style={
                            "backgroundColor": rx.color("gray", 1),
                            "borderRadius": "var(--radius-2)",
                            "borderWidth": "1px",
                            "borderColor": rx.color("cyan", 7),
                            "padding": "0.5rem",
                        }
                    ),
                    data=AppState.consultas_hoy_por_estado_admin,
                    layout="vertical",
                    height=250,
                    width="100%"
                ),
                rx.center(
                    rx.text("No hay datos disponibles", color=DARK_THEME["colors"]["text_secondary"]),
                    height="250px"
                )
            ),
            spacing="3",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="2px"),
        width="100%"
    )

def consultas_por_odontologo_chart_asistente() -> rx.Component:
    """Gráfico de consultas por odontólogo para asistente"""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Consultas por Odontólogo Hoy",
                size="4",
                weight="bold",
                color=DARK_THEME["colors"]["text_primary"],
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
                    height=250,
                    width="100%"
                ),
                rx.center(
                    rx.text("No hay datos disponibles", color=DARK_THEME["colors"]["text_secondary"]),
                    height="250px"
                )
            ),
            spacing="3",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["success"]["500"], hover_lift="2px"),
        width="100%"
    )

def dashboard_page_asistente() -> rx.Component:
    """Página del dashboard del ASISTENTE - Mejorado con búsqueda y gráficos"""
    return medical_page_layout(
        rx.vstack(
            # Header de la página
            page_header(
                "Dashboard de Asistente",
                "Monitoreo de consultas y acceso rápido a historiales de pacientes",
                actions=[
                    refresh_button(
                        text="Actualizar datos",
                        on_click=AppState.cargar_dashboard_asistente,
                        loading=AppState.cargando_dashboard_asistente
                    )
                ]
            ),

            # Contenido principal
            rx.cond(
                AppState.cargando_dashboard_asistente,
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3", color=COLORS["primary"]["500"]),
                        rx.text("Cargando datos del día...", color=COLORS["gray"]["600"], size="3"),
                        spacing="3",
                        align="center"
                    ),
                    padding="40px",
                    width="100%"
                ),
                rx.box(
                    # Búsqueda arriba (reutilizando componente del sistema)
                    rx.hstack(
                        crystal_search_input(
                            placeholder="Buscar paciente por nombre, HC o CI...",
                            value=AppState.termino_busqueda_pacientes,
                            on_change=AppState.buscar_pacientes
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("users", size=18),
                                rx.text("Ver Pacientes", size="2"),
                                spacing="2"
                            ),
                            on_click=lambda: AppState.navigate_to("pacientes"),
                            size="3",
                            variant="soft"
                        ),
                        spacing="3",
                        align="center",
                        width="100%",
                        margin_bottom="24px"
                    ),

                    # Grid de 4 estadísticas básicas
                    quick_stats_grid_asistente(),

                    # Grid de 2 columnas: Tabla izquierda, Gráficos derecha
                    rx.grid(
                        # Columna 1: Tabla de consultas con búsqueda y filtros integrados
                        consultas_dashboard_table(),

                        # Columna 2: Stack de gráficos
                        rx.vstack(
                            consultas_por_estado_chart_asistente(),
                            consultas_por_odontologo_chart_asistente(),
                            spacing="6",
                            width="100%"
                        ),

                        grid_template_columns=[
                            "1fr",                  # Móvil: 1 columna
                            "repeat(1, 1fr)",       # Móvil grande: 1 columna
                            "repeat(2, 1fr)",       # Desktop: 2 columnas
                        ],
                        spacing="6",
                        width="100%",
                        margin_top="24px"
                    ),

                    spacing="6",
                    padding="24px",
                    width="100%",
                )
            ),
            spacing="3",
            width="100%",
            min_height="100vh",
            # 🚀 CARGAR DATOS AL MONTAR (con gráficos del admin también)
            on_mount=[
                AppState.cargar_dashboard_asistente(),
                AppState.cargar_dashboard_admin()  # Para los gráficos
            ]
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

