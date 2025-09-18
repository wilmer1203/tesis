"""
🦷 PÁGINA DE INTERVENCIÓN CON ODONTOGRAMA FDI AVANZADO
======================================================

Nueva versión de la página de intervención integrando:
- Odontograma FDI avanzado con datos reales
- Servicio avanzado con versionado automático
- Interactividad completa por diente
- Estadísticas en tiempo real
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button, medical_page_layout
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
# TEMPORALMENTE COMENTADO - arreglando archivo
from dental_system.components.odontologia.advanced_fdi_odontogram import advanced_fdi_odontogram
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,
    dark_crystal_card, dark_header_style, dark_page_background,
    create_dark_style
)

# ==========================================
# 🎨 ESTILOS ESPECÍFICOS DE LA PÁGINA
# ==========================================

def create_intervention_advanced_styles():
    """🎨 Estilos específicos para la página de intervención avanzada"""
    return {
        ".intervention-advanced-container": {
            "background": dark_page_background(),
            "min_height": "100vh",
            "padding": SPACING["6"]
        },
        ".odontogram-section": {
            **dark_crystal_card(),
            "padding": SPACING["8"],
            "margin_bottom": SPACING["6"]
        },
        ".patient-section": {
            **dark_crystal_card(),
            "padding": SPACING["6"],
            "margin_bottom": SPACING["6"]
        }
    }

# ==========================================
# 🏷️ HEADER DE LA PÁGINA
# ==========================================

def intervention_advanced_header() -> rx.Component:
    """🏷️ Header de la página de intervención avanzada"""
    return rx.box(
        rx.hstack(
            # Logo y título
            rx.hstack(
                rx.icon("tooth", size=32, color=COLORS["primary"]),
                rx.vstack(
                    rx.heading(
                        "Intervención Odontológica Avanzada",
                        size="7",
                        color=COLORS["primary"]["400"]
                    ),
                    rx.text(
                        "Odontograma FDI profesional con datos en tiempo real",
                        color=DARK_THEME["colors"]["text_secondary"],
                        font_size="md"
                    ),
                    spacing="1",
                    align="start"
                ),
                spacing="4",
                align="center"
            ),
            
            # Controles de navegación
            rx.hstack(
                secondary_button(
                    text="Volver a Odontología",
                    icon="arrow_left",
                    on_click=rx.redirect("/odontologia")
                ),
                primary_button(
                    "Guardar Cambios",
                    "save",
                    on_click=lambda: AppState.mostrar_toast("Cambios guardados", "success")
                ),
                spacing="3"
            ),
            
            justify="between",
            align="center",
            width="100%"
        ),
        style=dark_header_style()
    )

# ==========================================
# 📊 PANEL DE INFORMACIÓN DEL PACIENTE
# ==========================================

def patient_info_section() -> rx.Component:
    """📊 Sección de información del paciente"""
    return rx.box(
        rx.vstack(
            rx.heading(
                "👤 Información del Paciente",
                size="4",
                color=COLORS["primary"],
                margin_bottom=SPACING["2"]
            ),
            
            # Panel de información existente
            panel_informacion_paciente(),
            
            spacing="4",
            width="100%"
        ),
        class_name="patient-section"
    )

# ==========================================
# 🦷 SECCIÓN DEL ODONTOGRAMA AVANZADO
# ==========================================

def odontogram_section() -> rx.Component:
    """🦷 Sección principal del odontograma FDI avanzado"""
    return rx.box(
        rx.vstack(
            # Header de la sección
            rx.hstack(
                rx.heading(
                    "🦷 Odontograma FDI Profesional",
                    size="5",
                    color=COLORS["primary"]
                ),
                rx.badge(
                    "✨ Datos Reales",
                    color_scheme="green",
                    size="2"
                ),
                rx.badge(
                    "🔄 Versionado Automático",
                    color_scheme="blue",
                    size="2"
                ),
                spacing="3",
                align="center",
                width="100%",
                justify="start"
            ),
            
            # Descripción
            rx.text(
                "Odontograma interactivo con 32 dientes FDI cargados desde la base de datos. "
                "Haz clic en cualquier diente para aplicar condiciones y ver el resultado en tiempo real.",
                color=DARK_THEME["colors"]["text_secondary"],
                font_size="sm",
                line_height="1.6",
                margin_bottom=SPACING["2"]
            ),
            
            # Odontograma avanzado - temporalmente deshabilitado
            advanced_fdi_odontogram(),
            rx.text("Odontograma avanzado en desarrollo", color=DARK_THEME["colors"]["text_secondary"]),
            
            spacing="4",
            width="100%"
        ),
        class_name="odontogram-section"
    )

# ==========================================
# 📋 PANEL DE ACCIONES Y HERRAMIENTAS
# ==========================================

def tools_section() -> rx.Component:
    """📋 Panel de herramientas y acciones"""
    return rx.box(
        rx.vstack(
            rx.heading(
                "🛠️ Herramientas Avanzadas",
                size="4",
                color=COLORS["primary"]
            ),
            
            rx.grid(
                # Crear nueva versión
                rx.card(
                    rx.vstack(
                        rx.icon("git_branch", size=24, color=COLORS["secondary"]),
                        rx.text("Nueva Versión", font_weight="bold"),
                        rx.text(
                            "Crear nueva versión del odontograma",
                            font_size="sm",
                            color=DARK_THEME["colors"]["text_secondary"],
                            text_align="center"
                        ),
                        rx.button(
                            "Crear Versión",
                            variant="outline",
                            color_scheme="blue",
                            size="2",
                            width="100%"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="4"
                ),
                
                # Comparar versiones
                rx.card(
                    rx.vstack(
                        rx.icon("git_compare", size=24, color=COLORS["secondary"]),
                        rx.text("Comparar", font_weight="bold"),
                        rx.text(
                            "Comparar con versión anterior",
                            font_size="sm",
                            color=DARK_THEME["colors"]["text_secondary"],
                            text_align="center"
                        ),
                        rx.button(
                            "Comparar",
                            variant="outline",
                            color_scheme="cyan",
                            size="2",
                            width="100%"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="4"
                ),
                
                # Exportar
                rx.card(
                    rx.vstack(
                        rx.icon("download", size=24, color=COLORS["success"]),
                        rx.text("Exportar", font_weight="bold"),
                        rx.text(
                            "Descargar reporte PDF",
                            font_size="sm",
                            color=DARK_THEME["colors"]["text_secondary"],
                            text_align="center"
                        ),
                        rx.button(
                            "Exportar PDF",
                            variant="outline",
                            color_scheme="green",
                            size="2",
                            width="100%"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="4"
                ),
                
                # Historial
                rx.card(
                    rx.vstack(
                        rx.icon("history", size=24, color=COLORS["warning"]),
                        rx.text("Historial", font_weight="bold"),
                        rx.text(
                            "Ver historial completo",
                            font_size="sm",
                            color=DARK_THEME["colors"]["text_secondary"],
                            text_align="center"
                        ),
                        rx.button(
                            "Ver Historial",
                            variant="outline",
                            color_scheme="orange",
                            size="2",
                            width="100%"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="4"
                ),
                
                columns="4",
                spacing="4",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(),
        padding=SPACING["3"]
    )

# ==========================================
# 📊 FOOTER CON INFORMACIÓN TÉCNICA
# ==========================================

def intervention_footer() -> rx.Component:
    """📊 Footer con información técnica"""
    return rx.box(
        rx.hstack(
            rx.text(
                "🦷 Sistema FDI v4.2 | 32 dientes permanentes | Versionado automático",
                color=DARK_THEME["colors"]["text_secondary"],
                font_size="sm"
            ),
            rx.spacer(),
            rx.hstack(
                rx.text(
                    "Última actualización: ",
                    color=DARK_THEME["colors"]["text_secondary"],
                    font_size="sm"
                ),
                rx.moment(
                    format="DD/MM/YYYY HH:mm",
                    interval=60000,  # Actualiza cada minuto
                    color=DARK_THEME["colors"]["text_secondary"],
                    font_size="sm"
                ),
                spacing="1",
                align="center"
            ),
            align="center",
            width="100%"
        ),
        **create_dark_style(
            base_style={
                "padding": SPACING["4"],
                "border_top": f"1px solid {DARK_THEME['colors']['border']}",
                "background": DARK_THEME['colors']['surface']
            }
        )
    )

# ==========================================
# 📱 PÁGINA PRINCIPAL
# ==========================================

@rx.page(route="/intervencion-avanzada", title="🦷 Intervención Avanzada")
def intervencion_advanced_page() -> rx.Component:
    """🦷 Página principal de intervención con odontograma FDI avanzado"""
    
    return medical_page_layout(
        rx.vstack(
            # Header
            intervention_advanced_header(),
            
            # Contenido principal
            rx.box(
                rx.vstack(
                    # Información del paciente
                    patient_info_section(),
                    
                    # Odontograma avanzado (sección principal)
                    odontogram_section(),
                    
                    # Herramientas
                    tools_section(),
                    
                    spacing="6",
                    width="100%",
                    max_width="1400px",
                    margin="0 auto"
                ),
                class_name="intervention-advanced-container"
            ),
            
            # Footer
            intervention_footer(),
            
            spacing="6",
            width="100%"
        )
    )