"""
Layout principal del dashboard del administrador - ACTUALIZADO CON GESTIÓN DE PACIENTES
Incluye sidebar de navegación y contenido dinámico según la página seleccionada
"""

import reflex as rx
from dental_system.components.role_specific.admin import admin_sidebar
from dental_system.state.admin_state import AdminState
from dental_system.pages.pacientes_page import patients_management_page  # ✅ IMPORTAR GESTIÓN DE PACIENTES
from dental_system.pages.consultas_page import consultas_management  # ✅ IMPORTAR GESTIÓN DE CONSULTAS
from dental_system.styles.themes import COLORS

# ==========================================
# PÁGINAS DE VISTA SIMPLIFICADAS (PLACEHOLDERS)
# ==========================================

def admin_dashboard_page() -> rx.Component:
    """Dashboard principal del administrador"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text("Dashboard Administrativo", size="6", weight="bold", color=COLORS["gray"]["800"]),
                    rx.text("Gestión de pacientes, consultas y pagos", size="3", color=COLORS["gray"]["600"]),
                    spacing="1",
                    align_items="start"
                ),
                align="center",
                width="100%"
            ),
            
            # Estadísticas principales del admin
            rx.grid(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("users", size=24, color=COLORS["primary"]["500"]),
                            rx.text("Total Pacientes", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text(AdminState.admin_stats.get("total_pacientes", 0).to_string(), size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("Registrados en el sistema", size="2", color=COLORS["gray"]["600"]),
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
                            rx.icon("user-plus", size=24, color=COLORS["success"]),
                            rx.text("Nuevos este Mes", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text(AdminState.admin_stats.get("nuevos_pacientes_mes", 0).to_string(), size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("Pacientes registrados", size="2", color=COLORS["gray"]["600"]),
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
                            rx.icon("calendar", size=24, color=COLORS["secondary"]["500"]),
                            rx.text("Consultas Hoy", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text(AdminState.admin_stats.get("consultas_hoy", 0).to_string(), size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("Programadas", size="2", color=COLORS["gray"]["600"]),
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
                            rx.icon("credit-card", size=24, color=COLORS["blue"]["500"]),
                            rx.text("Pagos Pendientes", size="3", color=COLORS["gray"]["600"]),
                            spacing="2"
                        ),
                        rx.text(AdminState.admin_stats.get("pagos_pendientes", 0).to_string(), size="6", weight="bold", color=COLORS["gray"]["800"]),
                        rx.text("Por procesar", size="2", color=COLORS["gray"]["600"]),
                        spacing="2",
                        align_items="start"
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    border=f"1px solid {COLORS['gray']['200']}"
                ),
                
                columns="4",
                spacing="6",
                width="100%"
            ),
            
            # Acceso rápido a gestión de pacientes
            rx.divider(margin="24px 0"),
            rx.text("Accesos Rápidos", size="4", weight="medium", color=COLORS["gray"]["700"]),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("user-plus", size=20),
                        rx.text("Nuevo Paciente"),
                        spacing="2"
                    ),
                    background=COLORS["primary"]["500"],
                    color="white",
                    on_click=lambda: AdminState.navigate_to("pacientes"),
                    size="3"
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("calendar", size=20),
                        rx.text("Nueva Cita"),
                        spacing="2"
                    ),
                    background=COLORS["secondary"]["500"],
                    color="white",
                    on_click=lambda: AdminState.navigate_to("consultas"),
                    size="3"
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("credit-card", size=20),
                        rx.text("Registrar Pago"),
                        spacing="2"
                    ),
                    background=COLORS["success"],
                    color="white",
                    on_click=lambda: AdminState.navigate_to("pagos"),
                    size="3"
                ),
                spacing="4"
            ),
            
            spacing="6",
            padding="24px",
            width="100%"
        ),
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

def consultas_placeholder() -> rx.Component:
    """Placeholder para gestión de consultas"""
    return rx.center(
        rx.vstack(
            rx.heading("Gestión de Consultas", size="9", color=COLORS["primary"]["500"]),
            rx.text("Módulo en desarrollo", size="4", color=COLORS["gray"]["600"]),
            rx.text("Aquí podrás programar y gestionar las citas", text_align="center"),
            rx.button(
                "Volver al Dashboard",
                on_click=lambda: AdminState.navigate_to("dashboard"),
                color_scheme="teal"
            ),
            spacing="4",
            align="center"
        ),
        height="50vh"
    )

def pagos_placeholder() -> rx.Component:
    """Placeholder para gestión de pagos"""
    return rx.center(
        rx.vstack(
            rx.heading("Gestión de Pagos", size="9", color=COLORS["secondary"]["500"]),
            rx.text("Módulo en desarrollo", size="4", color=COLORS["gray"]["600"]),
            rx.text("Aquí podrás procesar pagos y generar reportes", text_align="center"),
            rx.button(
                "Volver al Dashboard",
                on_click=lambda: AdminState.navigate_to("dashboard"),
                color_scheme="teal"
            ),
            spacing="4",
            align="center"
        ),
        height="50vh"
    )

# ==========================================
# ROUTER DE CONTENIDO
# ==========================================

def admin_main_content() -> rx.Component:
    """Contenido principal que cambia según la página seleccionada"""
    return rx.match(
        AdminState.current_page,
        ("dashboard", admin_dashboard_page()),
        ("pacientes", patients_management_page()),  # ✅ PÁGINA REAL DE GESTIÓN DE PACIENTES
        ("consultas", consultas_management()),
        ("pagos", pagos_placeholder()),
        # Página por defecto
        admin_dashboard_page(),
    )

# ==========================================
# LAYOUT PRINCIPAL DEL ADMINISTRADOR
# ==========================================

def admin_layout() -> rx.Component:
    """Layout principal del dashboard del administrador"""
    return rx.box(
        # Sidebar del admin
        admin_sidebar(),
        
        # Contenido principal
        rx.box(
            admin_main_content(),
            margin_left=rx.cond(AdminState.sidebar_collapsed, "80px", "280px"),
            transition="margin-left 0.3s ease",
            width=rx.cond(
                AdminState.sidebar_collapsed, 
                "calc(100% - 80px)", 
                "calc(100% - 280px)"
            ),
            min_height="100vh"
        ),
        
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"],
        position="relative",
        on_mount=AdminState.load_dashboard_data  # ✅ CARGAR DATOS AL MONTAR
    )
