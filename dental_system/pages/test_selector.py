"""
🧪 PÁGINA DE PRUEBA PARA EL SELECTOR DE DIENTES
===============================================

Página temporal para probar el selector visual de dientes 
sin tener que pasar por el login problemático.
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.selector_dientes_visual import selector_dientes_visual

@rx.page(route="/test-selector", title="🧪 Test Selector")
def test_selector_page() -> rx.Component:
    """🧪 Página de prueba para el selector de dientes"""
    
    return rx.vstack(
        rx.heading("🧪 Test del Selector Visual de Dientes", size="6"),
        rx.text("Esta es una página de prueba para verificar que funciona el selector", size="3"),
        
        # Mostrar estado actual
        rx.card(
            rx.vstack(
                rx.text("Estado actual del formulario:"),
                rx.text(f"Dientes afectados: {AppState.formulario_intervencion.dientes_afectados}"),
                spacing="2"
            ),
            padding="4",
            margin_bottom="4"
        ),
        
        # Selector de dientes
        selector_dientes_visual(),
        
        spacing="6",
        padding="6",
        width="100%",
        max_width="1200px",
        margin="0 auto"
    )