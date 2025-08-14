# 🚀 APLICACIÓN PRINCIPAL - CORREGIDA PARA SPA POR ROLES
# dental_system.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS
from dental_system.pages.dashboard import dashboard_page
from dental_system.pages.pacientes_page import pacientes_page
from dental_system.pages.personal_page import personal_page
# from dental_system.pages.consultas_page import consultas_page_new
# from dental_system.pages.servicios_page import servicios_page
# from dental_system.pages.pagos_page import pagos_page
# from dental_system.pages.odontologia_page import odontologia_page
# from dental_system.pages.intervencion_page import intervencion_page
from dental_system.pages.login import login_page
from dental_system.components.common import sidebar
from dental_system.utils.route_guard import (
    boss_only_component,
    admin_or_boss_component, 
    dentist_component,
    authenticated_only_component
)
# test_generic_tables.py


# ==========================================
# 🎨 CONFIGURACIÓN DEL TEMA SIMPLIFICADA
# ==========================================

app_theme = rx.theme(
    appearance="light",
    accent_color="teal",
    gray_color="gray",
    radius="large",
    scaling="100%"
)

# ==========================================
# 🧭 LAYOUT PRINCIPAL - SIMPLE Y CLARO
# ==========================================

def main_layout(page_content: rx.Component) -> rx.Component:
    """
    🎯 LAYOUT PRINCIPAL SIMPLIFICADO
    ✅ UNA SOLA estructura que se adapta al rol
    """
    return rx.box(
        rx.cond(
        AppState.esta_autenticado,
        
            rx.hstack(
                # Sidebar de navegación
                sidebar(),
                
                # 🔥 AQUÍ ESTÁ EL CAMBIO PRINCIPAL - USAR EL CONTENIDO DINÁMICO
                rx.box(
                    page_content,  # Esto recibe el contenido que cambia
                    flex="1",
                    height="100vh",
                    overflow_y="auto",
                ),
                
                width="100%",
                height="100vh",
                spacing="0",
                position= "absolute"
            ),
        # Si no está autenticado, solo mostrar login
        page_content,
        )
    )


# ==========================================
# 🎯 CONTENIDO DINÁMICO - AQUÍ ESTÁ LA MAGIA
# ==========================================

def main_content() -> rx.Component:
    """
    🔥 CONTENIDO PRINCIPAL QUE CAMBIA SEGÚN current_page
    ✅ ESTO ES LO QUE ESTABA FALTANDO EN TU CÓDIGO
    """
    return rx.match(
        AppState.current_page,
        ("dashboard", dashboard_page()),
        ("pacientes", pacientes_page()),
        # ("consultas", consultas_page_new()),
        ("personal", personal_page()),
        # ("servicios", servicios_page()),
        # ("pagos", pagos_page()),
        # ("odontologia", odontologia_page()),
        # ("intervencion", intervencion_page()),
        ("reportes", reportes_placeholder()),
        # Página por defecto
        dashboard_page(),
    ) # type: ignore

# ==========================================
# 📄 PÁGINAS POR ROL - SPA APPROACH
# ==========================================

@boss_only_component
def boss_page() -> rx.Component:
    """👔 Página del gerente - SPA con contenido dinámico"""
    return main_layout(main_content())

@admin_or_boss_component 
def admin_page() -> rx.Component:
    """👤 Página del administrador - SPA con contenido dinámico"""  
    return main_layout(main_content())

@dentist_component
def dentist_page() -> rx.Component:
    """🦷 Página del odontólogo - SPA con contenido dinámico"""
    return main_layout(main_content())

# ==========================================
# 🏠 PÁGINA DE INICIO - REDIRECCIÓN INTELIGENTE
# ==========================================

def index_page() -> rx.Component:
    """🏠 Página de inicio que redirige según rol"""
    return rx.cond(
        AppState.esta_autenticado,
        rx.cond(
            AppState.rol_usuario == "gerente",
            rx.fragment(
                rx.script('window.location.href = "/boss";'),
                rx.center("Redirigiendo al dashboard del gerente...")
            ),
            rx.cond(
                AppState.rol_usuario == "administrador", 
                rx.fragment(
                    rx.script('window.location.href = "/admin";'),
                    rx.center("Redirigiendo al dashboard del administrador...")
                ),
                rx.cond(
                    AppState.rol_usuario == "odontologo",
                    rx.fragment(
                        rx.script('window.location.href = "/dentist";'),
                        rx.center("Redirigiendo al dashboard del odontólogo...")
                    ),
                    rx.center("Rol no reconocido")
                )
            )
        ),
        login_page()
    )

# ==========================================
# 🚧 PLACEHOLDERS PARA MÓDULOS EN DESARROLLO
# ==========================================


def servicios_placeholder() -> rx.Component:
    """📋 Placeholder para gestión de servicios"""
    return rx.center(
        rx.vstack(
            rx.text("📋 Gestión de Servicios", size="7", weight="bold"),
            rx.text("Módulo en desarrollo", size="4", color="gray.600"),
            rx.text("Aquí podrás gestionar los servicios odontológicos"),
            rx.button(
                "Volver al Dashboard",
                on_click=lambda: AppState.navigate_to("dashboard") # type: ignore
            ),
            spacing="4",
            align="center"
        ),
        height="50vh"
    )

def reportes_placeholder() -> rx.Component:
    """📊 Placeholder para reportes"""
    return rx.center(
        rx.vstack(
            rx.text("📊 Reportes", size="7", weight="bold"),
            rx.text("Módulo en desarrollo", size="4", color="gray.600"),
            rx.text("Aquí podrás ver estadísticas y reportes"),
            rx.button(
                "Volver al Dashboard",
                # on_click=lambda: AppState.navigate_to("dashboard") # type: ignore
            ),
            spacing="4",
            align="center"
        ),
        height="50vh"
    )

def pagos_placeholder() -> rx.Component:
    """💳 Placeholder para gestión de pagos"""
    return rx.center(
        rx.vstack(
            rx.text("💳 Gestión de Pagos", size="7", weight="bold"),
            rx.text("Módulo en desarrollo", size="4", color="gray.600"),
            rx.text("Aquí podrás gestionar los pagos y facturación"),
            rx.button(
                "Volver al Dashboard",
                # on_click=lambda: AppState.navigate_to("dashboard") # type: ignore
            ),
            spacing="4",
            align="center"
        ),
        height="50vh"
    )

def odontologia_placeholder() -> rx.Component:
    """🦷 Placeholder para módulo de odontología"""
    return rx.center(
        rx.vstack(
            rx.text("🦷 Módulo de Odontología", size="7", weight="bold"),
            rx.text("En desarrollo", size="4", color="gray.600"),
            rx.vstack(
                rx.text("✅ Funcionalidades preparadas:", weight="bold"),
                rx.text("• Atender pacientes"),
                rx.text("• Gestionar intervenciones"), 
                rx.text("• Odontograma interactivo"),
                rx.text("• Registrar tratamientos"),
                rx.text("• Calcular costos por intervención"),
                spacing="2",
                align_items="start"
            ),
            rx.button(
                "Volver al Dashboard",
                on_click=lambda: AppState.navigate_to("dashboard")  # type: ignore
            ),
            spacing="4",
            align="center"
        ),
        height="50vh"
    )

# ==========================================
# 🚀 CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================

def create_app() -> rx.App:
    """🚀 CREAR APLICACIÓN CON RUTAS POR ROL"""
    
    app = rx.App(
        theme=app_theme,
        
    )
    
    # 🎯 RUTAS ESPECÍFICAS POR ROL - COMO QUERÍAS
    app.add_page(index_page, route="/")           # Redirige según rol
    app.add_page(login_page, route="/login")      # Login público
    app.add_page(boss_page, route="/boss")        # Gerente
    app.add_page(admin_page, route="/admin")      # Administrador  
    app.add_page(dentist_page, route="/dentist")  # Odontólogo
    # Agregar ruta temporal
    
    return app

# Crear la aplicación
app = create_app()

# Para desarrollo
if __name__ == "__main__":
    app.run() # type: ignore
