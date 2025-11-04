
import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout, page_header, stat_card, refresh_button
from dental_system.components.charts import graficas_resume
from dental_system.styles.themes import COLORS, SHADOWS,GRADIENTS,dark_header_style,DARK_THEME, dark_crystal_card

# ==========================================
# COMPONENTES DEL DASHBOARD
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
        padding="24px",
        width="100%"
    )

# ==========================================
# COMPONENTE PRINCIPAL DEL DASHBOARD
# ==========================================

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
        # 🚀 CARGAR DATOS REALES AL MONTAR + mantener random para toggle
        on_mount=[
            AppState.cargar_dashboard_gerente_completo(),
            AppState.randomize_data()
        ]
    )
    )

