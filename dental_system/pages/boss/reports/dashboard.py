"""
Dashboard principal para el rol de Gerente/Jefe
Muestra estadísticas generales y resumen del estado de la clínica
"""

import reflex as rx
from dental_system.components.role_specific.boss import ( 
    loading_spinner,
    main_header
)
from dental_system.components.common import stat_card, primary_button
from dental_system.state.boss_state import BossState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS
from dental_system.components.charts import render_chart, custom_segmented_control,chart_toggle

# ==========================================
# COMPONENTES DEL DASHBOARD
# ==========================================

def quick_stats_grid() -> rx.Component:
    """Grid de estadísticas rápidas - Solo 4 métricas principales"""
    return rx.grid(
        stat_card(
            title="Total Pacientes",
            value=BossState.dashboard_stats["total_pacientes"].to_string(),
            icon="users",
            color=COLORS["primary"]["500"],
            trend="up",
            trend_value=rx.cond(
                BossState.dashboard_stats["total_pacientes"] > 0,
                "Registrados",
                "Sin datos"
            )
        ),
        stat_card(
            title="Consultas Hoy",
            value=BossState.dashboard_stats["consultas_hoy"].to_string(),
            icon="calendar",
            color=COLORS["secondary"]["500"],
            trend="up",
            trend_value=rx.cond(
                BossState.dashboard_stats["consultas_hoy"] > 0,
                "Programadas",
                "Sin consultas"
            )
        ),
        stat_card(
            title="Personal Activo",
            value=BossState.dashboard_stats["personal_activo"].to_string(),
            icon="user-check",
            color=COLORS["blue"]["500"],
            trend="up",
            trend_value=rx.cond(
                BossState.dashboard_stats["personal_activo"] > 0,
                "En servicio",
                "Sin personal"
            )
        ),
        stat_card(
            title="Ingresos del Mes",
            value=rx.cond(
                BossState.dashboard_stats["ingresos_mes"] > 0,
                f"${BossState.dashboard_stats['ingresos_mes']:,.0f}".replace(",", "."),
                "$0"
            ),
            icon="dollar-sign",
            color=COLORS["success"],
            trend="up",
            trend_value=rx.cond(
                BossState.dashboard_stats["ingresos_mes"] > 0,
                "Generados",
                "Sin ingresos"
            )
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

def graficas_resume() -> rx.Component:
    """Renderiza el gráfico según la pestaña seleccionada."""
    return rx.box(
        rx.hstack(
            chart_toggle(BossState),
            custom_segmented_control(BossState),      
        ),
        rx.match(
            BossState.selected_tab,
            (
                "Pacientes", 
                render_chart(
                    state=BossState,
                    key="Pacientes",
                    color="blue",
                    gradient_id="gradient-blue"
                )
            ),
            (
                "Ingresos", 
                render_chart(
                    state=BossState,
                    key="Ingresos",
                    color="green",
                    gradient_id="gradient-green"
                )
            ),
            (
                "Citas", 
                render_chart(
                    state=BossState,
                    key="Citas",
                    color="orange",
                    gradient_id="gradient-orange"
                )
            ),
        ),
        padding="24px",
        background="white",
        border_radius="16px",
        border=f"1px solid {COLORS['gray']['200']}",
        box_shadow= SHADOWS["xl"],
        width="100%"
    )

# ==========================================
# COMPONENTE PRINCIPAL DEL DASHBOARD
# ==========================================

def boss_dashboard_page() -> rx.Component:
    """Página principal del dashboard del gerente"""
    return rx.box(
        # Header de la página
        main_header(
            "Dashboard Gerencial", 
            "Resumen ejecutivo y métricas principales de la clínica"
        ),
        
        # Contenido principal
        rx.cond(
            BossState.is_loading,
            loading_spinner(),
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
        
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================

def boss_dashboard() -> rx.Component:
    """Dashboard del gerente con inicialización de datos"""
    return rx.box(
        boss_dashboard_page(),
        on_mount=BossState.load_dashboard_data  # Cargar datos al montar el componente
    )
