"""
Layout principal del dashboard del gerente - ACTUALIZADO CON GESTIÓN DE PACIENTES
Incluye sidebar de navegación y contenido dinámico según la página seleccionada
"""

import reflex as rx
from dental_system.components.role_specific.boss import boss_sidebar
from dental_system.state.app_state import AppState
from dental_system.state.admin_state import AdminState  
from dental_system.pages.dashboard import boss_dashboard
from dental_system.pages.personal_page import personal_management_page
from dental_system.pages.pacientes_page import patients_management
from dental_system.pages.consultas_page import consultas_management
from dental_system.styles.themes import COLORS

# ==========================================
# PÁGINAS DE VISTA SIMPLIFICADAS
# ==========================================

def servicios_page_placeholder() -> rx.Component:
    """Placeholder para gestión de servicios"""
    return rx.center(
        rx.vstack(
            rx.heading("Gestión de Servicios", size="9", color=COLORS["secondary"]["500"]),
            rx.text("Módulo en desarrollo", size="4", color=COLORS["gray"]["600"]),
            rx.text("Aquí podrás gestionar el catálogo de servicios", text_align="center"),
            rx.button(
                "Volver al Dashboard",
                on_click=lambda: AppState.navigate_to("dashboard"),
                color_scheme="teal"
            ),
            spacing="4",
            align="center"
        ),
        height="50vh"
    )

def consultas_view_page() -> rx.Component:
    """Vista de consultas para el gerente"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text("Vista de Consultas", size="6", weight="bold", color=COLORS["gray"]["800"]),
                    rx.text("Programación y estado de consultas", size="3", color=COLORS["gray"]["600"]),
                    spacing="1",
                    align_items="start"
                ),
                align="center",
                width="100%"
            ),
            
            # Métricas del día
            rx.grid(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("calendar", size=24, color=COLORS["primary"]["500"]),
                            rx.text("Consultas Hoy", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text("12", size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("8 completadas", size="2", color=COLORS["gray"]["600"]),
                        spacing="2",
                        align_items="start"
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    border=f"1px solid {COLORS['gray']['200']}"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("clock", size=24, color=COLORS["secondary"]["500"]),
                            rx.text("Promedio Espera", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text("15 min", size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("Excelente", size="2", color=COLORS["success"]),
                        spacing="2",
                        align_items="start"
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    border=f"1px solid {COLORS['gray']['200']}"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("user-check", size=24, color=COLORS["success"]),
                            rx.text("Tasa Asistencia", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text("95%", size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("+3% vs mes anterior", size="2", color=COLORS["success"]),
                        spacing="2",
                        align_items="start"
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    border=f"1px solid {COLORS['gray']['200']}"
                ),
                
                columns="3",
                spacing="6",
                width="100%"
            ),
            
            rx.button(
                "Volver al Dashboard",
                on_click=lambda: AppState.navigate_to("dashboard"),
                color_scheme="teal",
                margin_top="20px"
            ),
            
            spacing="6",
            padding="24px",
            width="100%"
        ),
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

def pagos_view_page() -> rx.Component:
    """Vista de pagos para el gerente"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text("Vista de Pagos", size="6", weight="bold", color=COLORS["gray"]["800"]),
                    rx.text("Resumen financiero y transacciones", size="3", color=COLORS["gray"]["600"]),
                    spacing="1",
                    align_items="start"
                ),
                align="center",
                width="100%"
            ),
            
            # Métricas financieras
            rx.grid(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("dollar-sign", size=24, color=COLORS["success"]),
                            rx.text("Ingresos del Mes", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text("$45,230", size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("+18% vs mes anterior", size="2", color=COLORS["success"]),
                        spacing="2",
                        align_items="start"
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    border=f"1px solid {COLORS['gray']['200']}"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("credit-card", size=24, color=COLORS["primary"]["500"]),
                            rx.text("Pagos Procesados", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text("68", size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("Este mes", size="2", color=COLORS["gray"]["600"]),
                        spacing="2",
                        align_items="start"
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    border=f"1px solid {COLORS['gray']['200']}"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("alert-circle", size=24, color=COLORS["error"]),
                            rx.text("Pagos Pendientes", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text("3", size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("$2,150 total", size="2", color=COLORS["error"]),
                        spacing="2",
                        align_items="start"
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    border=f"1px solid {COLORS['gray']['200']}"
                ),
                
                columns="3",
                spacing="6",
                width="100%"
            ),
            
            rx.button(
                "Volver al Dashboard",
                on_click=lambda: AppState.navigate_to("dashboard"),
                color_scheme="teal",
                margin_top="20px"
            ),
            
            spacing="6",
            padding="24px",
            width="100%"
        ),
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )


# ==========================================
# ROUTER DE CONTENIDO
# ==========================================

def main_content() -> rx.Component:
    """Contenido principal que cambia según la página seleccionada"""
    return rx.match(
        BossState.current_page,
        ("dashboard", boss_dashboard()),
        ("personal", personal_management_page()),  # ✅ PÁGINA REAL DE PERSONAL
        ("servicios", servicios_page_placeholder()),
        ("pacientes", patients_management()),  # ✅ GESTIÓN COMPLETA DE PACIENTES
        ("consultas", consultas_management()),
        ("pagos", pagos_view_page()),
        # Página por defecto
        boss_dashboard(),
    )

# ==========================================
# LAYOUT PRINCIPAL
# ==========================================

def boss_layout() -> rx.Component:
    """Layout principal del dashboard del gerente"""
    return rx.box(
        # Sidebar
        boss_sidebar(),
        
        # Contenido principal
        rx.box(
            main_content(),
            margin_left=rx.cond(AppState.sidebar_collapsed, "80px", "280px"),
            transition="margin-left 0.3s ease",
            width=rx.cond(
                AppState.sidebar_collapsed, 
                "calc(100% - 80px)", 
                "calc(100% - 280px)"
            ),
            min_height="100vh"
        ),
        
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"],
        position="relative",
        on_mount=BossState.load_dashboard_data  # ✅ CARGAR DATOS AL MONTAR
    )
