"""
🧪 PÁGINA DE PRUEBA - CATÁLOGO FDI AVANZADO
============================================

Página temporal para probar la implementación del servicio
avanzado con los datos reales de la base de datos.
"""

import reflex as rx
from dental_system.components.odontologia.test_fdi_component import test_fdi_component
from dental_system.state.app_state import AppState

@rx.page(route="/test-fdi", title="🧪 Prueba FDI")
def test_fdi_page() -> rx.Component:
    """🧪 Página de prueba del catálogo FDI"""
    
    return rx.box(
        # Header de la aplicación
        rx.hstack(
            rx.heading(
                "🦷 Sistema Odontológico - Prueba FDI",
                size="6",
                color="cyan"
            ),
            rx.spacer(),
            rx.button(
                "← Volver al Dashboard",
                on_click=rx.redirect("/"),
                variant="ghost"
            ),
            justify="between",
            align="center",
            padding="4",
            width="100%",
            background="var(--gray-2)",
            border_bottom="1px solid var(--gray-6)"
        ),
        
        # Contenido principal
        test_fdi_component(),
        
        # Estilos globales
        min_height="100vh",
        background="var(--gray-1)",
        width="100%"
    )