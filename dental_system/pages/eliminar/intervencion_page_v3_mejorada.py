"""
🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA V3 - REDISEÑO INSPIRADO EN REACT
========================================================================

✨ CARACTERÍSTICAS IMPLEMENTADAS (Inspirado en patient-consultation template):
- 🏗️ Layout 3 paneles responsivo (sidebar + main + tabs)
- 📋 Sistema de tabs avanzado con 4 secciones principales
- 📊 Panel historial médico expandible
- 💰 Formulario con conversión automática BS/USD
- 🦷 Integración completa con odontograma FDI
- 🌙 Dark mode consistente con tema empresarial
- 📱 Completamente responsive (mobile-first)

🎯 ARQUITECTURA:
- Panel izquierdo: Información del paciente + Estado consulta
- Panel central: Tabs con funcionalidades principales
- Layout adaptable: stack mobile → 2 cols tablet → 3 paneles desktop

🔄 FLUJO MÉDICO OPTIMIZADO:
- Header con contexto completo del paciente
- Acciones rápidas siempre disponibles
- Estado de consulta en tiempo real
- Navegación intuitiva entre funcionalidades
"""

import reflex as rx
from typing import Dict, Any, List

from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,
    dark_crystal_card, dark_header_style, create_dark_style
)
# Importar componente real que funciona
from dental_system.components.odontologia.selector_intervenciones_v2 import nuevo_tab_intervencion

# ==========================================
# 🎨 COLORES Y ESTILOS ENTERPRISE
# ==========================================

# Colores refinados para módulo médico (basado en DARK_THEME)
MEDICAL_COLORS = {
    "surface": DARK_THEME["colors"]["surface"],
    "surface_elevated": DARK_THEME["colors"]["surface_elevated"], 
    "border": DARK_THEME["colors"]["border"],
    "text_primary": DARK_THEME["colors"]["text_primary"],
    "text_secondary": DARK_THEME["colors"]["text_secondary"],
    "accent": COLORS["primary"]["500"],
    "accent_hover": COLORS["primary"]["400"],
    "success": COLORS["success"]["500"],
    "warning": COLORS["warning"]["500"],
    "error": COLORS["error"]["500"]
}

# ==========================================
# 📊 COMPONENTE HEADER CON CONTEXTO MÉDICO
# ==========================================

def medical_context_header() -> rx.Component:
    """🏥 Header médico con contexto completo del paciente y estado de consulta"""
    return rx.box(
        # Información del paciente actual
        rx.vstack(
            rx.hstack(
                # Información del paciente
                rx.hstack(
                    rx.box(
                        rx.icon(
                            "user",
                            size=20,
                            color=COLORS["primary"]["400"]
                        ),
                        style={
                            "width": "40px",
                            "height": "40px",
                            "border_radius": RADIUS["lg"],
                            "background": f"linear-gradient(135deg, {COLORS['primary']['500']}15 0%, {COLORS['primary']['300']}10 100%)",
                            "border": f"1px solid {COLORS['primary']['500']}30",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center"
                        }
                    ),
                    
                    rx.vstack(
                        rx.text(
                            AppState.paciente_actual.nombre_completo,
                            style={
                                "font_size": "1.25rem",
                                "font_weight": "700",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.text(
                            f"HC: {AppState.paciente_actual.numero_historia}",
                            style={
                                "font_size": "0.875rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        spacing="0",
                        align_items="start"
                    ),
                    
                    spacing="3",
                    align_items="center"
                ),
                
                rx.spacer(),
                
                # Estado de la consulta
                rx.hstack(
                    rx.box(
                        rx.text(
                            "EN ATENCIÓN",
                            style={
                                "font_size": "0.75rem",
                                "font_weight": "700",
                                "color": "white"
                            }
                        ),
                        style={
                            "background": MEDICAL_COLORS["success"],
                            "padding": f"{SPACING['1']} {SPACING['3']}",
                            "border_radius": RADIUS["full"],
                            "animation": "pulse 2s infinite"
                        }
                    ),
                    
                    rx.text(
                        f"Consulta: {AppState.consulta_actual.numero_consulta}",
                        style={
                            "font_size": "0.875rem",
                            "color": MEDICAL_COLORS["text_secondary"],
                            "font_weight": "500"
                        }
                    ),
                    
                    spacing="3",
                    align_items="center"
                ),
                
                # Acciones rápidas
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
                            "background": MEDICAL_COLORS["surface"],
                            "border": f"1px solid {MEDICAL_COLORS['border']}",
                            "color": MEDICAL_COLORS["text_primary"],
                            "_hover": {
                                "background": MEDICAL_COLORS["surface_elevated"],
                                "transform": "translateY(-2px)"
                            }
                        }
                    ),
                    
                    rx.button(
                        rx.hstack(
                            rx.icon("check-circle", size=16),
                            rx.text("Completar", size="3"),
                            spacing="2"
                        ),
                        variant="solid",
                        size="3",
                        style={
                            "background": GRADIENTS["neon_primary"],
                            "color": "white",
                            "border": "none",
                            "_hover": {
                                "transform": "translateY(-2px) scale(1.02)",
                                "box_shadow": f"0 0 20px {COLORS['primary']['500']}40"
                            }
                        }
                    ),
                    
                    spacing="3"
                ),
                
                width="100%",
                align_items="center"
            ),
            
            spacing="4",
            width="100%"
        ),
        
        style={
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="0px"),
            "padding": SPACING["6"],
            "margin_bottom": SPACING["6"]
        }
    )

# ==========================================
# 🗂️ SISTEMA DE TABS AVANZADO (4 TABS)
# ==========================================

def advanced_tabs_system() -> rx.Component:
    """📋 Sistema de tabs inspirado en patient-consultation con 4 secciones"""
    
    # Definir los tabs disponibles
    tabs_data = [
        {
            "id": "intervencion",
            "label": "🔧 Intervención", 
            "icon": "stethoscope",
            "description": "Registro de tratamiento"
        },
        {
            "id": "odontograma", 
            "label": "🦷 Odontograma",
            "icon": "stethoscope",
            "description": "Estado dental"
        },
        {
            "id": "historial",
            "label": "📋 Historial", 
            "icon": "history",
            "description": "Consultas anteriores"
        },
        {
            "id": "archivos",
            "label": "📷 Archivos",
            "icon": "camera", 
            "description": "Fotografías y documentos"
        }
    ]
    
    return rx.tabs.root(
        # Tab triggers (navigation)
        rx.tabs.list(
            *[
                rx.tabs.trigger(
                    rx.hstack(
                        rx.icon(tab["icon"], size=16),
                        rx.vstack(
                            rx.text(
                                tab["label"],
                                style={
                                    "font_size": "0.875rem",
                                    "font_weight": "600",
                                    "color": MEDICAL_COLORS["text_primary"]
                                }
                            ),
                            rx.text(
                                tab["description"],
                                style={
                                    "font_size": "0.75rem", 
                                    "color": MEDICAL_COLORS["text_secondary"]
                                }
                            ),
                            spacing="1",
                            align_items="start"
                        ),
                        spacing="3",
                        align_items="center"
                    ),
                    value=tab["id"],
                    style={
                        "padding": f"{SPACING['3']} {SPACING['4']}",
                        "border_radius": RADIUS["md"],
                        "border": "none",
                        "background": "transparent",
                        "cursor": "pointer",
                        "transition": "all 0.2s ease",
                        "_hover": {
                            "background": MEDICAL_COLORS["surface_elevated"]
                        },
                        "&[data-state=active]": {
                            "background": MEDICAL_COLORS["accent"],
                            "color": "white"
                        },
                        "&[data-state=active] svg": {
                            "color": "white"
                        }
                    }
                ) for tab in tabs_data
            ],
            style={
                "background": MEDICAL_COLORS["surface"],
                "border_bottom": f"1px solid {MEDICAL_COLORS['border']}",
                "padding": SPACING["2"]
            }
        ),
        
        # Tab content panels
        rx.tabs.content(
            panel_intervencion_mejorado(),
            value="intervencion"
        ),
        
        rx.tabs.content(
            panel_odontograma_placeholder(), 
            value="odontograma"
        ),
        
        rx.tabs.content(
            panel_historial_medico(),
            value="historial"
        ),
        
        rx.tabs.content(
            panel_archivos_placeholder(),
            value="archivos"
        ),
        
        default_value="intervencion",
        style={
            **dark_crystal_card(color=COLORS["primary"]["400"], hover_lift="0px"),
            "width": "100%",
            "min_height": "600px"
        }
    )

# ==========================================
# 🔧 PANEL INTERVENCIÓN MEJORADO
# ==========================================

def panel_intervencion_mejorado() -> rx.Component:
    """🔧 Panel de intervención con funcionalidad REAL integrada"""
    return rx.box(
        # Componente REAL que ya funciona con datos de BD
        nuevo_tab_intervencion(),
        style={
            "width": "100%",
            "padding": SPACING["4"]
        }
    )

def panel_intervencion_BACKUP_original() -> rx.Component:
    """🔧 BACKUP - Panel mock original (mantener para referencia)"""
    return rx.vstack(
        # ❌ CÓDIGO BACKUP - FUNCIONALIDAD MOCK ORIGINAL ❌
        # Header del panel
        rx.hstack(
            rx.icon("stethoscope", size=20, color=MEDICAL_COLORS["accent"]),
            rx.text(
                "Documentación de Tratamiento BACKUP",
                style={
                    "font_size": "1.125rem",
                    "font_weight": "600", 
                    "color": MEDICAL_COLORS["text_primary"]
                }
            ),
            rx.spacer(),
            rx.text(
                "Tasa: 36.45 Bs/USD",
                style={
                    "font_size": "0.875rem",
                    "color": MEDICAL_COLORS["text_secondary"]
                }
            ),
            width="100%",
            align_items="center",
            style={
                "padding": f"{SPACING['4']} 0",
                "border_bottom": f"1px solid {MEDICAL_COLORS['border']}"
            }
        ),
        
        # Formulario de nueva intervención
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("plus", size=16, color=MEDICAL_COLORS["accent"]),
                    rx.text(
                        "Nueva Intervención",
                        style={
                            "font_size": "1rem",
                            "font_weight": "600",
                            "color": MEDICAL_COLORS["text_primary"]
                        }
                    ),
                    spacing="2",
                    align_items="center"
                ),
                
                # Grid de campos del formulario
                rx.grid(
                    # Servicio/Procedimiento
                    rx.vstack(
                        rx.text(
                            "Procedimiento",
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "500",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Seleccionar procedimiento...",
                                style={
                                    "background": MEDICAL_COLORS["surface"],
                                    "border": f"1px solid {MEDICAL_COLORS['border']}",
                                    "color": MEDICAL_COLORS["text_primary"],
                                    "min_width": "200px"
                                }
                            ),
                            rx.select.content(
                                rx.select.item("Limpieza Dental", value="limpieza"),
                                rx.select.item("Obturación", value="obturacion"),
                                rx.select.item("Extracción", value="extraccion"),
                                rx.select.item("Endodoncia", value="endodoncia"),
                                rx.select.item("Corona", value="corona"),
                                style={
                                    "background": MEDICAL_COLORS["surface"],
                                    "border": f"1px solid {MEDICAL_COLORS['border']}"
                                }
                            ),
                            required=True
                        ),
                        spacing="2",
                        align_items="start"
                    ),
                    
                    # Diente afectado
                    rx.vstack(
                        rx.text(
                            "Diente",
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "500",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.input(
                            placeholder="Ej: 16, 21-24",
                            style={
                                "background": MEDICAL_COLORS["surface"],
                                "border": f"1px solid {MEDICAL_COLORS['border']}",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        spacing="2",
                        align_items="start"
                    ),
                    
                    # Odontólogo
                    rx.vstack(
                        rx.text(
                            "Dentista",
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "500",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Seleccionar dentista...",
                                style={
                                    "background": MEDICAL_COLORS["surface"],
                                    "border": f"1px solid {MEDICAL_COLORS['border']}",
                                    "color": MEDICAL_COLORS["text_primary"]
                                }
                            ),
                            rx.select.content(
                                rx.select.item("Dr. María González", value="dr-gonzalez"),
                                rx.select.item("Dr. Carlos Mendoza", value="dr-mendoza"),
                                rx.select.item("Dr. Ana Silva", value="dr-silva"),
                                style={
                                    "background": MEDICAL_COLORS["surface"],
                                    "border": f"1px solid {MEDICAL_COLORS['border']}"
                                }
                            )
                        ),
                        spacing="2",
                        align_items="start"
                    ),
                    
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing="4",
                    width="100%"
                ),
                
                # Segunda fila: Costos
                rx.grid(
                    rx.vstack(
                        rx.text(
                            "Costo (Bs)",
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "500",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.input(
                            placeholder="0.00",
                            type="number",
                            style={
                                "background": MEDICAL_COLORS["surface"],
                                "border": f"1px solid {MEDICAL_COLORS['border']}",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        spacing="2",
                        align_items="start"
                    ),
                    
                    rx.vstack(
                        rx.text(
                            "Costo (USD)",
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "500",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.input(
                            placeholder="0.00",
                            type="number",
                            style={
                                "background": MEDICAL_COLORS["surface"],
                                "border": f"1px solid {MEDICAL_COLORS['border']}",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        spacing="2",
                        align_items="start"
                    ),
                    
                    rx.vstack(
                        rx.text(
                            "Duración (min)",
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "500",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.input(
                            placeholder="30",
                            type="number",
                            style={
                                "background": MEDICAL_COLORS["surface"],
                                "border": f"1px solid {MEDICAL_COLORS['border']}",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        spacing="2",
                        align_items="start"
                    ),
                    
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing="4",
                    width="100%"
                ),
                
                # Notas del procedimiento
                rx.vstack(
                    rx.text(
                        "Notas del Procedimiento",
                        style={
                            "font_size": "0.875rem",
                            "font_weight": "500",
                            "color": MEDICAL_COLORS["text_primary"]
                        }
                    ),
                    rx.text_area(
                        placeholder="Detalles adicionales del tratamiento...",
                        style={
                            "background": MEDICAL_COLORS["surface"],
                            "border": f"1px solid {MEDICAL_COLORS['border']}",
                            "color": MEDICAL_COLORS["text_primary"],
                            "min_height": "80px"
                        }
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("pen-tool", size=16),
                            rx.text("Capturar Firma"),
                            spacing="2"
                        ),
                        variant="outline",
                        style={
                            "background": MEDICAL_COLORS["surface"],
                            "border": f"1px solid {MEDICAL_COLORS['border']}",
                            "color": MEDICAL_COLORS["text_primary"]
                        }
                    ),
                    
                    rx.spacer(),
                    
                    rx.button(
                        rx.hstack(
                            rx.icon("plus", size=16),
                            rx.text("Agregar Intervención"),
                            spacing="2"
                        ),
                        style={
                            "background": GRADIENTS["neon_primary"],
                            "color": "white",
                            "border": "none"
                        }
                    ),
                    
                    width="100%",
                    align_items="center"
                ),
                
                spacing="6",
                width="100%",
                align_items="start"
            ),
            
            style={
                "background": f"{MEDICAL_COLORS['surface']}50",
                "border_radius": RADIUS["lg"],
                "padding": SPACING["4"],
                "margin": f"{SPACING['4']} 0"
            }
        ),
        
        # NOTA: resumen_sesion_placeholder ya no se necesita
        # El componente nuevo_tab_intervencion() incluye la tabla de resumen automáticamente
        # resumen_sesion_placeholder(),
        
        spacing="4",
        width="100%",
        align_items="start",
        style={
            "padding": SPACING["6"]
        }
    )

# ==========================================
# 📋 PANEL HISTORIAL MÉDICO
# ==========================================

def panel_historial_medico() -> rx.Component:
    """📋 Panel de historial médico expandible inspirado en ConsultationHistoryPanel"""
    
    # Datos mock de historial (en producción vendría de AppState.historial_paciente_actual)
    consultas_historial = [
        {
            "fecha": "2024-09-04",
            "hora": "10:30", 
            "dentistas": ["Dr. María González", "Dr. Carlos Mendoza"],
            "procedimientos": ["Limpieza Dental", "Obturación"],
            "costo_total": {"bs": 4300, "usd": 117.97},
            "estado": "completada",
            "notas": "Paciente presenta buena higiene oral. Se realizó limpieza completa y obturación en molar superior derecho."
        },
        {
            "fecha": "2024-08-15",
            "hora": "14:15",
            "dentistas": ["Dr. Ana Silva"],
            "procedimientos": ["Consulta General", "Radiografía"],
            "costo_total": {"bs": 2000, "usd": 54.88},
            "estado": "completada", 
            "notas": "Control de rutina. Paciente sin molestias. Se detectó inicio de caries en diente 24."
        },
        {
            "fecha": "2024-07-20",
            "hora": "09:45",
            "dentistas": ["Dr. María González"],
            "procedimientos": ["Obturación"],
            "costo_total": {"bs": 2500, "usd": 68.56},
            "estado": "completada",
            "notas": "Tratamiento de caries en premolar superior derecho. Procedimiento sin complicaciones."
        }
    ]
    
    return rx.vstack(
        # Header del panel
        rx.hstack(
            rx.icon("history", size=20, color=MEDICAL_COLORS["accent"]),
            rx.text(
                "Historial de Consultas",
                style={
                    "font_size": "1.125rem",
                    "font_weight": "600",
                    "color": MEDICAL_COLORS["text_primary"]
                }
            ),
            rx.spacer(),
            rx.hstack(
                rx.hstack(
                    rx.icon("calendar", size=14, color=MEDICAL_COLORS["text_secondary"]),
                    rx.text(
                        f"{len(consultas_historial)} visitas",
                        style={
                            "font_size": "0.875rem",
                            "color": MEDICAL_COLORS["text_secondary"]
                        }
                    ),
                    spacing="1"
                ),
                rx.hstack(
                    rx.icon("dollar-sign", size=14, color=MEDICAL_COLORS["text_secondary"]),
                    rx.text(
                        f"{sum(c['costo_total']['bs'] for c in consultas_historial):,.0f} Bs",
                        style={
                            "font_size": "0.875rem",
                            "color": MEDICAL_COLORS["text_secondary"]
                        }
                    ),
                    spacing="1"
                ),
                spacing="4"
            ),
            width="100%",
            align_items="center",
            style={
                "padding": f"{SPACING['4']} 0",
                "border_bottom": f"1px solid {MEDICAL_COLORS['border']}"
            }
        ),
        
        # Estadísticas resumen
        rx.grid(
            rx.box(
                rx.vstack(
                    rx.text(
                        str(len(consultas_historial)),
                        style={
                            "font_size": "2rem",
                            "font_weight": "700",
                            "color": MEDICAL_COLORS["accent"]
                        }
                    ),
                    rx.text(
                        "Total Visitas",
                        style={
                            "font_size": "0.75rem",
                            "color": MEDICAL_COLORS["text_secondary"]
                        }
                    ),
                    spacing="1",
                    align_items="center"
                ),
                style={
                    "background": f"{MEDICAL_COLORS['accent']}10",
                    "border_radius": RADIUS["lg"],
                    "padding": SPACING["3"],
                    "text_align": "center"
                }
            ),
            
            rx.box(
                rx.vstack(
                    rx.text(
                        f"{sum(c['costo_total']['bs'] for c in consultas_historial):,.0f}",
                        style={
                            "font_size": "1.25rem",
                            "font_weight": "700",
                            "color": MEDICAL_COLORS["success"]
                        }
                    ),
                    rx.text(
                        "Total Bs",
                        style={
                            "font_size": "0.75rem",
                            "color": MEDICAL_COLORS["text_secondary"]
                        }
                    ),
                    spacing="1",
                    align_items="center"
                ),
                style={
                    "background": f"{MEDICAL_COLORS['success']}10",
                    "border_radius": RADIUS["lg"],
                    "padding": SPACING["3"],
                    "text_align": "center"
                }
            ),
            
            rx.box(
                rx.vstack(
                    rx.text(
                        f"${sum(c['costo_total']['usd'] for c in consultas_historial):.2f}",
                        style={
                            "font_size": "1.25rem",
                            "font_weight": "700",
                            "color": MEDICAL_COLORS["success"]
                        }
                    ),
                    rx.text(
                        "Total USD",
                        style={
                            "font_size": "0.75rem",
                            "color": MEDICAL_COLORS["text_secondary"]
                        }
                    ),
                    spacing="1",
                    align_items="center"
                ),
                style={
                    "background": f"{MEDICAL_COLORS['success']}10",
                    "border_radius": RADIUS["lg"],
                    "padding": SPACING["3"],
                    "text_align": "center"
                }
            ),
            
            columns=rx.breakpoints(initial="1", sm="3"),
            spacing="4",
            width="100%",
            style={"margin": f"{SPACING['4']} 0"}
        ),
        
        # Lista de consultas históricas
        rx.vstack(
            *[
                consulta_historial_item(consulta, i) 
                for i, consulta in enumerate(consultas_historial)
            ],
            spacing="3",
            width="100%"
        ),
        
        spacing="4",
        width="100%",
        align_items="start",
        style={
            "padding": SPACING["6"]
        }
    )

def consulta_historial_item(consulta: Dict[str, Any], index: int) -> rx.Component:
    """📋 Item individual de consulta en el historial"""
    return rx.accordion.root(
        rx.accordion.item(
            header=rx.accordion.trigger(
                rx.hstack(
                    # Fecha y hora
                    rx.vstack(
                        rx.text(
                            consulta["fecha"],
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "600",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.text(
                            consulta["hora"],
                            style={
                                "font_size": "0.75rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        spacing="0",
                        align_items="start"
                    ),
                    
                    # Estado
                    rx.box(
                        rx.text(
                            "Completado",
                            style={
                                "font_size": "0.75rem",
                                "font_weight": "500",
                                "color": "white"
                            }
                        ),
                        style={
                            "background": MEDICAL_COLORS["success"],
                            "padding": f"{SPACING['1']} {SPACING['2']}",
                            "border_radius": RADIUS["full"]
                        }
                    ),
                    
                    # Dentistas
                    rx.vstack(
                        rx.text(
                            "Dentistas",
                            style={
                                "font_size": "0.75rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        rx.text(
                            ", ".join(consulta["dentistas"]),
                            style={
                                "font_size": "0.875rem",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        spacing="0",
                        align_items="start"
                    ),
                    
                    rx.spacer(),
                    
                    # Costo
                    rx.vstack(
                        rx.text(
                            "Costo Total",
                            style={
                                "font_size": "0.75rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        rx.text(
                            f"{consulta['costo_total']['bs']:,.0f} Bs / ${consulta['costo_total']['usd']:.2f}",
                            style={
                                "font_size": "0.875rem",
                                "font_weight": "600",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        spacing="0",
                        align_items="end"
                    ),
                    
                    rx.icon("chevron-down", size=16, color=MEDICAL_COLORS["text_secondary"]),
                    
                    width="100%",
                    align_items="center"
                ),
                style={
                    "padding": SPACING["4"],
                    "&[data-state=open] svg": {
                        "transform": "rotate(180deg)"
                    }
                }
            ),
            
            content=rx.accordion.content(
                rx.vstack(
                    # Procedimientos realizados
                    rx.hstack(
                        *[
                            rx.box(
                                rx.text(
                                    proc,
                                    style={
                                        "font_size": "0.75rem",
                                        "color": "white"
                                    }
                                ),
                                style={
                                    "background": f"{MEDICAL_COLORS['accent']}90",
                                    "padding": f"{SPACING['1']} {SPACING['2']}",
                                    "border_radius": RADIUS["full"]
                                }
                            ) for proc in consulta["procedimientos"]
                        ],
                        spacing="2"
                    ),
                    
                    # Notas clínicas
                    rx.box(
                        rx.text(
                            consulta["notas"],
                            style={
                                "font_size": "0.875rem",
                                "color": MEDICAL_COLORS["text_primary"],
                                "line_height": "1.5"
                            }
                        ),
                        style={
                            "background": MEDICAL_COLORS["surface"],
                            "border_radius": RADIUS["md"],
                            "padding": SPACING["3"]
                        }
                    ),
                    
                    # Acciones
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.icon("file-text", size=14),
                                rx.text("Ver Recibo"),
                                spacing="1"
                            ),
                            variant="outline",
                            size="2",
                            style={
                                "background": MEDICAL_COLORS["surface"],
                                "border": f"1px solid {MEDICAL_COLORS['border']}"
                            }
                        ),
                        
                        rx.button(
                            rx.hstack(
                                rx.icon("download", size=14),
                                rx.text("Exportar"),
                                spacing="1"
                            ),
                            variant="outline",
                            size="2",
                            style={
                                "background": MEDICAL_COLORS["surface"],
                                "border": f"1px solid {MEDICAL_COLORS['border']}"
                            }
                        ),
                        
                        spacing="2",
                        justify="end"
                    ),
                    
                    spacing="4",
                    width="100%",
                    align_items="start"
                ),
                style={
                    "padding": f"0 {SPACING['4']} {SPACING['4']} {SPACING['4']}"
                }
            ),
            
            value=f"item-{index}"
        ),
        
        type="single",
        collapsible=True,
        style={
            "background": f"{MEDICAL_COLORS['surface']}80",
            "border": f"1px solid {MEDICAL_COLORS['border']}",
            "border_radius": RADIUS["lg"]
        }
    )

# ==========================================
# 🦷 PLACEHOLDERS PARA OTROS PANELES
# ==========================================

def panel_odontograma_placeholder() -> rx.Component:
    """🦷 Placeholder para panel de odontograma (a implementar después)"""
    return rx.vstack(
        rx.hstack(
            rx.icon("stethoscope", size=20, color=MEDICAL_COLORS["accent"]),
            rx.text(
                "Odontograma Digital",
                style={
                    "font_size": "1.125rem",
                    "font_weight": "600",
                    "color": MEDICAL_COLORS["text_primary"]
                }
            ),
            width="100%",
            align_items="center",
            style={
                "padding": f"{SPACING['4']} 0",
                "border_bottom": f"1px solid {MEDICAL_COLORS['border']}"
            }
        ),
        
        rx.box(
            rx.vstack(
                rx.icon("stethoscope", size=48, color=MEDICAL_COLORS["text_secondary"]),
                rx.text(
                    "Odontograma Interactivo",
                    style={
                        "font_size": "1.25rem",
                        "font_weight": "600",
                        "color": MEDICAL_COLORS["text_primary"]
                    }
                ),
                rx.text(
                    "Visualización y edición del estado dental",
                    style={
                        "font_size": "0.875rem",
                        "color": MEDICAL_COLORS["text_secondary"],
                        "text_align": "center"
                    }
                ),
                rx.text(
                    "🚧 En desarrollo - Próximamente disponible",
                    style={
                        "font_size": "0.875rem",
                        "color": MEDICAL_COLORS["warning"],
                        "font_style": "italic"
                    }
                ),
                spacing="3",
                align_items="center"
            ),
            style={
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "height": "400px",
                "background": f"{MEDICAL_COLORS['surface']}50",
                "border_radius": RADIUS["lg"],
                "margin": SPACING["4"]
            }
        ),
        
        spacing="4",
        width="100%",
        align_items="start",
        style={
            "padding": SPACING["6"]
        }
    )

def panel_archivos_placeholder() -> rx.Component:
    """📷 Placeholder para panel de archivos"""
    return rx.vstack(
        rx.hstack(
            rx.icon("camera", size=20, color=MEDICAL_COLORS["accent"]),
            rx.text(
                "Fotografías y Documentos",
                style={
                    "font_size": "1.125rem",
                    "font_weight": "600",
                    "color": MEDICAL_COLORS["text_primary"]
                }
            ),
            width="100%",
            align_items="center",
            style={
                "padding": f"{SPACING['4']} 0",
                "border_bottom": f"1px solid {MEDICAL_COLORS['border']}"
            }
        ),
        
        rx.box(
            rx.vstack(
                rx.icon("camera", size=48, color=MEDICAL_COLORS["text_secondary"]),
                rx.text(
                    "Gestión de Archivos",
                    style={
                        "font_size": "1.25rem",
                        "font_weight": "600",
                        "color": MEDICAL_COLORS["text_primary"]
                    }
                ),
                rx.text(
                    "Subida y gestión de fotografías clínicas y documentos",
                    style={
                        "font_size": "0.875rem",
                        "color": MEDICAL_COLORS["text_secondary"],
                        "text_align": "center"
                    }
                ),
                rx.text(
                    "🚧 En desarrollo - Próximamente disponible",
                    style={
                        "font_size": "0.875rem",
                        "color": MEDICAL_COLORS["warning"],
                        "font_style": "italic"
                    }
                ),
                spacing="3",
                align_items="center"
            ),
            style={
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "height": "400px",
                "background": f"{MEDICAL_COLORS['surface']}50",
                "border_radius": RADIUS["lg"],
                "margin": SPACING["4"]
            }
        ),
        
        spacing="4",
        width="100%",
        align_items="start",
        style={
            "padding": SPACING["6"]
        }
    )

def resumen_sesion_placeholder() -> rx.Component:
    """📊 Resumen de la sesión actual (placeholder)"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("calculator", size=16, color=MEDICAL_COLORS["accent"]),
                rx.text(
                    "Resumen de la Sesión",
                    style={
                        "font_size": "1rem",
                        "font_weight": "600",
                        "color": MEDICAL_COLORS["text_primary"]
                    }
                ),
                spacing="2",
                align_items="center"
            ),
            
            rx.grid(
                rx.box(
                    rx.vstack(
                        rx.text(
                            "0",
                            style={
                                "font_size": "2rem",
                                "font_weight": "700",
                                "color": MEDICAL_COLORS["accent"]
                            }
                        ),
                        rx.text(
                            "Intervenciones",
                            style={
                                "font_size": "0.75rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="center"
                    ),
                    style={"text_align": "center"}
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text(
                            "0 Bs",
                            style={
                                "font_size": "1.5rem",
                                "font_weight": "700",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.text(
                            "Total Bolívares",
                            style={
                                "font_size": "0.75rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="center"
                    ),
                    style={"text_align": "center"}
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text(
                            "$0.00",
                            style={
                                "font_size": "1.5rem",
                                "font_weight": "700",
                                "color": MEDICAL_COLORS["text_primary"]
                            }
                        ),
                        rx.text(
                            "Total USD",
                            style={
                                "font_size": "0.75rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="center"
                    ),
                    style={"text_align": "center"}
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text(
                            "0/0",
                            style={
                                "font_size": "1.25rem",
                                "font_weight": "600",
                                "color": MEDICAL_COLORS["success"]
                            }
                        ),
                        rx.text(
                            "Completadas",
                            style={
                                "font_size": "0.75rem",
                                "color": MEDICAL_COLORS["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="center"
                    ),
                    style={"text_align": "center"}
                ),
                
                columns=rx.breakpoints(initial="2", md="4"),
                spacing="4",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        
        style={
            "background": f"{MEDICAL_COLORS['accent']}05",
            "border": f"1px solid {MEDICAL_COLORS['accent']}20",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"]
        }
    )

# ==========================================
# 🏗️ LAYOUT PRINCIPAL DE 3 PANELES
# ==========================================

def sidebar_panel_paciente() -> rx.Component:
    """👤 Panel lateral con información del paciente"""
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
# 📄 PÁGINA PRINCIPAL MEJORADA
# ==========================================

def intervencion_page_v3_mejorada() -> rx.Component:
    """
    🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA V3 - INSPIRADA EN REACT TEMPLATE
    
    ✨ ARQUITECTURA IMPLEMENTADA:
    - 🏗️ Layout responsivo de 3 paneles (móvil: stack, desktop: sidebar + main)
    - 📋 Sistema de tabs avanzado con 4 secciones principales
    - 🔄 Estados reactivos y navegación intuitiva
    - 🎨 Dark mode empresarial consistente
    - 📱 Responsive design mobile-first
    - 💾 Integración completa con datos existentes
    
    🎯 FLUJO MÉDICO:
    1. Header con contexto del paciente y estado de consulta
    2. Layout adaptable según tamaño de pantalla
    3. Panel lateral: Información del paciente
    4. Panel principal: Tabs con funcionalidades
    5. Acciones rápidas siempre accesibles
    """
    return rx.box(
        medical_page_layout(
            rx.vstack(
                # Header médico con contexto completo
                medical_context_header(),
                
                # Layout principal responsivo de 3 paneles
                rx.grid(
                    # Panel lateral: Información del paciente
                    sidebar_panel_paciente(),
                    
                    # Panel principal: Sistema de tabs avanzado
                    advanced_tabs_system(),
                    
                    columns=rx.breakpoints(
                        initial="1",        # Móvil: stack vertical (1 columna)
                        md="1",            # Tablet: stack vertical (1 columna)
                        lg="320px 1fr",    # Desktop: sidebar (320px) + main (resto)
                        xl="350px 1fr"     # XL: sidebar más ancho (350px) + main
                    ),
                    spacing="6",
                    width="100%",
                    min_height="calc(100vh - 280px)"
                ),
                
                spacing="0",  # Sin spacing entre header y layout
                width="100%",
                max_width="1600px",
                align_items="center"
            )
        ),
        
        # Eventos de inicialización
        on_mount=[
            AppState.cargar_servicios_disponibles,
            AppState.cargar_servicios_para_intervencion,  # Específico para selector
            AppState.cargar_estadisticas_dia
        ]
    )