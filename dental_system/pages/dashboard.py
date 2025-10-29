
import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout
from dental_system.components.common import stat_card, primary_button
from dental_system.components.charts import graficas_resume
from dental_system.styles.themes import COLORS, SHADOWS,GRADIENTS,dark_header_style,DARK_THEME

# ==========================================
# COMPONENTES DEL DASHBOARD
# ==========================================

def quick_stats_grid() -> rx.Component:
    """Grid de estadísticas rápidas - Solo 4 métricas principales"""
    return rx.grid(
        stat_card(
            title="Total Pacientes",
            value="100",   # BossState.dashboard_stats["total_pacientes"].to_string(),
            icon="users",
            color=COLORS["primary"]["500"],
            trend="up",
            # trend_value=rx.cond(
            #     BossState.dashboard_stats["total_pacientes"] > 0,
            #     "Registrados",
            #     "Sin datos"
            # )
        ),
        stat_card(
            title="Consultas Hoy",
            value="100",   #BossState.dashboard_stats["consultas_hoy"].to_string(),
            icon="calendar",
            color=COLORS["secondary"]["500"],
            trend="up",
            # trend_value=rx.cond(
            #     BossState.dashboard_stats["consultas_hoy"] > 0,
            #     "Programadas",
            #     "Sin consultas"
            # )
        ),
        stat_card(
            title="Personal Activo",
            value="100",   #BossState.dashboard_stats["personal_activo"].to_string(),
            icon="user-check",
            color=COLORS["blue"]["500"],
            trend="up",
            # trend_value=rx.cond(
            #     BossState.dashboard_stats["personal_activo"] > 0,
            #     "En servicio",
            #     "Sin personal"
            # )
        ),
        stat_card(
            title="Ingresos del Mes",
           value="100",   #rx.cond(
            #     BossState.dashboard_stats["ingresos_mes"] > 0,
            #     f"${BossState.dashboard_stats['ingresos_mes']:,.0f}".replace(",", "."),
            #     "$0"
            # ),
            icon="dollar-sign",
            color=COLORS["success"]["500"],
            trend="up",
            # trend_value=rx.cond(
            #     BossState.dashboard_stats["ingresos_mes"] > 0,
            #     "Generados",
            #     "Sin ingresos"
            # )
        ),
        grid_template_columns=[
            "1fr",                  # Móvil: 1 columna
            "repeat(1, 1fr)",       # Móvil grande: 1 columna
            "repeat(2, 1fr)",       # Tablet: 2 columnas
            "repeat(2, 1fr)",       # Desktop pequeño: 2 columnas  
            "repeat(4, 1fr)",       # Desktop: 4 columnas
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
        padding="24px",
        background="white",
        border_radius="16px",
        border=f"1px solid {COLORS['gray']['200']}",
        box_shadow= SHADOWS["xl"],
        width="100%"
    )


def page_header() -> rx.Component:
    """📋 Header limpio para página de consultas (igual que personal/pacientes)"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                # Título principal con gradiente (igual que personal)
                rx.heading(
                    "dashboard de Monitoreo",
                    style={
                        "font_size": "2.75rem",
                        "font_weight": "800",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent",
                        "line_height": "1.2",
                        "text_align": "left"
                    }
                ),
                
                # Subtítulo elegante (igual que personal)
                rx.text(
                    "Monitoreo en tiempo real del flujo de pacientes por orden de llegada",
                    style={
                        "font_size": "1.125rem",
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "line_height": "1.5"
                    }
                ),
                
                spacing="1",
                justify="start",
                align="start"
            ),
            
            width="100%",
            align="center"
        ),
        style=dark_header_style(),
        width="100%"
    )


# ==========================================
# COMPONENTE PRINCIPAL DEL DASHBOARD
# ==========================================

def dashboard_page() -> rx.Component:
    """Página principal del dashboard del gerente"""
    return medical_page_layout(
        rx.vstack(
        # Header de la página
        page_header(),
        # Contenido principal
        rx.cond(
            AppState.cargando_dashboard,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color=COLORS["primary"]["500"]),
                    rx.text("Cargando...", color=COLORS["gray"]["600"], size="3"),
                    spacing="3",
                    align="center"
                ),
                padding="40px",
                width="100%"
            ),
            rx.box(
                # Grid de estadísticas principales
                quick_stats_grid(),
                
                # Grid de información adicional
                rx.grid(
                    # Columna izquierda - Actividad reciente
                    graficas_resume(),   
                    # Columna derecha - Consultas del día
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
        on_mount=AppState.randomize_data()
    )
    )
# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================

