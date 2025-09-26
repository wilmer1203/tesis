"""
🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA V3 - DISEÑO ENTERPRISE
==============================================================

REDISEÑO COMPLETO aplicando patrones de consultas_page_v41.py y personal_page.py:
- ✨ Glassmorphism médico premium con tema oscuro consistente
- 🎨 Clean page header con gradiente de texto
- 💎 Crystal cards con animaciones de hover
- 📱 Layout responsive mobile-first
- 🎯 Integración completa con themes.py
- 🚀 Componentes reutilizables del sistema
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button, medical_page_layout
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
from dental_system.components.odontologia.intervention_tabs_v2 import intervention_tabs_integrated, REFINED_COLORS
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,
    dark_crystal_card, dark_header_style, dark_page_background,
    create_dark_style
)

# ==========================================
# 🎨 ESTILOS ENTERPRISE CONSISTENTES
# ==========================================

# Usando REFINED_COLORS importado de intervention_tabs_v2.py
# que está basado en DARK_THEME y componentes exitosos

# ==========================================
# 🏥 COMPONENTES ENTERPRISE REDESIGNED
# ==========================================

def clean_page_header_intervencion() -> rx.Component:
    """🏥 Header limpio aplicando patrón de personal_page.py"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "🦷 Intervención Odontológica",
                    style={
                        "font_size": "2.75rem",
                        "font_weight": "800",
                        "line_height": "1.2",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent"
                    }
                ),
                rx.text(
                    "Registro completo de tratamiento dental con odontograma interactivo",
                    size="4",
                    color=DARK_THEME["colors"]["text_secondary"],
                    font_weight="medium"
                ),
                spacing="1",
                align_items="start"
            ),
            
            rx.spacer(),
            
            # Acciones header consistentes con personal_page
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("arrow-left", size=16),
                        rx.text("Volver", size="3"),
                        spacing="2"
                    ),
                    on_click=lambda: AppState.navigate_to("odontologia"),
                    variant="outline",
                    size="3",
                    style={
                        "background": REFINED_COLORS["surface"],
                        "border": f"1px solid {REFINED_COLORS['border']}",
                        "color": DARK_THEME["colors"]["text_primary"],
                        "backdrop_filter": "blur(10px)",
                        "_hover": {
                            "background": REFINED_COLORS["surface_elevated"],
                            "transform": "translateY(-2px)"
                        }
                    }
                ),
                spacing="3"
            ),
            
            width="100%",
            align="center"
        ),
        style=dark_header_style(),
        width="100%"
    )

def stats_intervencion() -> rx.Component:
    """📊 Stats de intervención aplicando patrón minimal_stat_card"""
    return rx.grid(
        # Paciente actual
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("user", size=20, color=COLORS["primary"]["400"]),
                    rx.vstack(
                        rx.text(
                            AppState.paciente_actual.nombre_completo,
                            font_weight="700",
                            size="4",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),
                        rx.text(
                            f"HC: {AppState.paciente_actual.numero_historia}",
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align_items="center"
                ),
                spacing="2",
                width="100%"
            ),
            style=dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px")
        ),
        
        # Estado consulta
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("activity", size=20, color=COLORS["success"]["400"]),
                    rx.vstack(
                        rx.text(
                            "Estado: En Atención",
                            font_weight="700",
                            size="4",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),
                        rx.text(
                            f"Consulta: {AppState.consulta_actual.numero_consulta}",
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align_items="center"
                ),
                spacing="2",
                width="100%"
            ),
            style=dark_crystal_card(color=COLORS["success"]["500"], hover_lift="4px")
        ),
        
        # Tab activo
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("clipboard-list", size=20, color=COLORS["warning"]["500"]),
                    rx.vstack(
                        rx.text(
                            AppState.active_intervention_tab.capitalize(),
                            font_weight="700",
                            size="4",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),
                        rx.text(
                            "Sección Activa",
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align_items="center"
                ),
                spacing="2",
                width="100%"
            ),
            style=dark_crystal_card(color=COLORS["warning"]["500"], hover_lift="4px")
        ),
        
        columns=rx.breakpoints(initial="1", sm="2", lg="3"),
        spacing="4",
        width="100%",
        margin_bottom="6"
    )

def panel_paciente_enterprise() -> rx.Component:
    """👤 Panel paciente con diseño enterprise"""
    return rx.box(
        panel_informacion_paciente(),
        style={
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="6px"),
            "height": "fit-content",
            "min_height": "500px"
        },
        width="100%"
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL ENTERPRISE REDESIGNED
# ==========================================

def intervencion_page_v2() -> rx.Component:
    """
    🦷 PÁGINA INTERVENCIÓN ODONTOLÓGICA V3 - ENTERPRISE DESIGN
    
    ✨ CARACTERÍSTICAS ENTERPRISE APLICADAS:
    - 🎨 Clean page header con gradiente de texto (patrón personal_page)
    - 💎 Stats cards con glassmorphism (patrón minimal_stat_card)
    - 🌙 Tema oscuro consistente con consultas_page_v41
    - 📱 Layout responsive mobile-first
    - 🔄 Animaciones de hover y microinteracciones
    - 🎯 Crystal cards con efectos premium
    - 🚀 Integración completa themes.py
    
    🏗️ ARQUITECTURA:
    - Layout: medical_page_layout wrapper (PATRÓN CONSULTAS)
    - Grid responsive: Adapta de 1 col (móvil) a 2 cols (desktop) 
    - Colores: REFINED_COLORS basado en DARK_THEME y componentes exitosos
    - Componentes: Reutiliza funciones dark_crystal_card, clean_header
    """
    return rx.box(
        medical_page_layout(
            rx.vstack(
                # Header enterprise con gradiente
                clean_page_header_intervencion(),
                
                # Stats cards aplicando patrón minimal_stat_card
                stats_intervencion(),
                
                # Layout principal responsive
                rx.grid(
                    # Panel paciente (sidebar)
                    panel_paciente_enterprise(),
                    
                    # Panel central con tabs

                    intervention_tabs_integrated(),
                    columns=rx.breakpoints(
                        initial="1",    # Móvil: stack vertical
                        md="1",         # Tablet: stack vertical  
                        lg="320px 1fr", # Desktop: sidebar + main
                        xl="350px 1fr"  # XL: sidebar más ancho
                    ),
                    spacing="6",
                    width="100%",
                    min_height="calc(100vh - 220px)"
                ),
                
                spacing="6",
                width="100%",
                max_width="1600px",
                align="center"
            )
        ),
        
        # Eventos de inicialización médica (solo específicos del paciente actual)
        on_mount=[
            # cargar_servicios_disponibles eliminado: se carga en post_login_inicializacion()
            AppState.cargar_historial_paciente(AppState.paciente_actual.id),
            # cargar_estadisticas_dia eliminado: se carga en post_login_inicializacion()
            # 🆕 V2.0: Inicializar odontograma interactivo específico del paciente
            AppState.cargar_odontograma_paciente(AppState.paciente_actual.id),
            # Asegurar tab inicial - INTERVENCIÓN PRIMERO
            AppState.set_active_intervention_tab("intervencion")
        ]
    )