"""
🦷 ODONTOGRAMA AVANZADO - VERSIÓN SIMPLE PARA PRUEBAS
============================================================

Versión mínima para verificar que se puede importar sin errores.
"""

import reflex as rx
from dental_system.styles.themes import DARK_THEME, COLORS

# ==========================================
# 🦷 COMPONENTE SIMPLE SIN ESTADO
# ==========================================

def advanced_fdi_odontogram() -> rx.Component:
    """🦷 Componente simple del odontograma sin estado para testing"""
    
    return rx.vstack(
        rx.heading("🦷 Odontograma FDI Avanzado", size="5", color=COLORS["primary"]["400"]),
        rx.text("Versión simple de prueba", color=DARK_THEME["colors"]["text_secondary"]),
        
        rx.box(
            rx.text("Aquí iría el odontograma completo", text_align="center"),
            padding="6",
            border=f"1px solid {COLORS['primary']['400']}",
            border_radius="8px",
            min_height="200px",
            display="flex",
            align_items="center",
            justify_content="center"
        ),
        
        spacing="4",
        align="center",
        width="100%"
    )