# 🦷 COMPONENTE: LAYOUT FDI PROFESIONAL CON 32 DIENTES
# dental_system/components/odontologia/odontogram_grid.py

import reflex as rx
from typing import Dict, Optional, List, Any
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.interactive_tooth import interactive_tooth, enhanced_tooth_component
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS

# ==========================================
# 🏗️ CONFIGURACIÓN DE CUADRANTES FDI
# ==========================================

# Organización estándar FDI de 32 dientes permanentes
FDI_QUADRANTS = {
    "superior_derecho": {
        "teeth": [18, 17, 16, 15, 14, 13, 12, 11],
        "label": "Superior Derecho",
        "position": "top-right"
    },
    "superior_izquierdo": {
        "teeth": [21, 22, 23, 24, 25, 26, 27, 28],
        "label": "Superior Izquierdo", 
        "position": "top-left"
    },
    "inferior_izquierdo": {
        "teeth": [31, 32, 33, 34, 35, 36, 37, 38],
        "label": "Inferior Izquierdo",
        "position": "bottom-left"
    },
    "inferior_derecho": {
        "teeth": [41, 42, 43, 44, 45, 46, 47, 48],
        "label": "Inferior Derecho",
        "position": "bottom-right"
    }
}

# Estilos para cuadrantes
QUADRANT_CONTAINER_STYLE = {
    "background": DARK_THEME["colors"]["surface_secondary"],
    "border": f"1px solid {DARK_THEME['colors']['primary']}",
    "border_radius": RADIUS["xl"],
    "padding": SPACING["4"],
    "min_width": "320px"
}

QUADRANT_HEADER_STYLE = {
    "font_size": "14px",
    "font_weight": "600",
    "color": COLORS["primary"]["400"],
    "margin_bottom": SPACING["3"],
    "text_align": "center",
    "border_bottom": f"1px solid {DARK_THEME['colors']['border']}",
    "padding_bottom": SPACING["2"]
}

# ==========================================
# 🦷 COMPONENTE: CUADRANTE INDIVIDUAL
# ==========================================

def odontogram_quadrant(
    quadrant_key: str,
    teeth_conditions: Optional[Dict[int, Dict[str, str]]] = None,
    selected_tooth: Optional[int] = None,
    pending_changes: Optional[Dict[int, Dict[str, str]]] = None
) -> rx.Component:
    """
    🦷 Renderiza un cuadrante FDI con 8 dientes
    
    Args:
        quadrant_key: Clave del cuadrante (superior_derecho, etc.)
        teeth_conditions: Condiciones actuales de los dientes
        selected_tooth: Diente actualmente seleccionado
        pending_changes: Cambios pendientes por diente
    """
    
    quadrant_info = FDI_QUADRANTS[quadrant_key]
    teeth_list = quadrant_info["teeth"]
    label = quadrant_info["label"]
    
    # Condiciones por defecto si no se proporcionan
    if teeth_conditions is None:
        teeth_conditions = {}
    
    if pending_changes is None:
        pending_changes = {}
    
    return rx.box(
        # Header del cuadrante
        rx.text(
            label,
            style=QUADRANT_HEADER_STYLE
        ),
        
        # Grid de 8 dientes del cuadrante
        rx.hstack(
            *[
                enhanced_tooth_component(
                    tooth_number=tooth_num,
                    estado="sano" if not teeth_conditions.get(tooth_num) else list(teeth_conditions.get(tooth_num, {}).values())[0] if teeth_conditions.get(tooth_num) else "sano",
                    is_selected=(selected_tooth == tooth_num)
                )
                for tooth_num in teeth_list
            ],
            spacing="3",
            justify_content="center",
            wrap="nowrap"
        ),
        
        style=QUADRANT_CONTAINER_STYLE
    )

# ==========================================
# 🏗️ COMPONENTE: GRID COMPLETO FDI
# ==========================================

def odontogram_interactive_grid() -> rx.Component:
    """
    🦷 Layout completo del odontograma con 32 dientes en cuadrantes FDI
    Responsive design optimizado para tablets clínicos
    """
    
    return rx.vstack(
        # Título principal
        rx.hstack(
            rx.icon(tag="grid-3x3", size=24, color=COLORS["primary"]["500"]),
            rx.text(
                "Odontograma Digital FDI - 32 Dientes Permanentes",
                size="5",
                weight="bold",
                color=DARK_THEME["colors"]["text_primary"]
            ),
            spacing="3",
            align_items="center",
            justify_content="center",
            margin_bottom="4"
        ),
        
        # Cuadrantes superiores
        rx.hstack(
            # Superior derecho (18-11)
            odontogram_quadrant(
                "superior_derecho",
                AppState.condiciones_odontograma,
                AppState.diente_seleccionado,
                AppState.cambios_pendientes_odontograma
            ),
            
            # Separador central (línea media)
            rx.box(
                rx.divider(
                    orientation="vertical",
                    color=COLORS["primary"]["400"],
                    height="120px"
                ),
                margin_x="4"
            ),
            
            # Superior izquierdo (21-28)
            odontogram_quadrant(
                "superior_izquierdo", 
                AppState.condiciones_odontograma,
                AppState.diente_seleccionado,
                AppState.cambios_pendientes_odontograma
            ),
            
            spacing="2",
            justify_content="center",
            width="100%"
        ),
        
        # Separador horizontal (línea de oclusión)
        rx.box(
            rx.divider(
                color=COLORS["primary"]["400"],
                margin_y="4"
            ),
            width="80%"
        ),
        
        # Cuadrantes inferiores  
        rx.hstack(
            # Inferior derecho (48-41)
            odontogram_quadrant(
                "inferior_derecho",
                AppState.condiciones_odontograma, 
                AppState.diente_seleccionado,
                AppState.cambios_pendientes_odontograma
            ),
            
            # Separador central (línea media)
            rx.box(
                rx.divider(
                    orientation="vertical",
                    color=COLORS["primary"]["400"],
                    height="120px"
                ),
                margin_x="4"
            ),
            
            # Inferior izquierdo (31-38)
            odontogram_quadrant(
                "inferior_izquierdo",
                AppState.condiciones_odontograma,
                AppState.diente_seleccionado, 
                AppState.cambios_pendientes_odontograma
            ),
            
            spacing="2",
            justify_content="center",
            width="100%"
        ),
        
        # Leyenda de orientación
        rx.hstack(
            rx.badge("D", color_scheme="blue", variant="soft"),
            rx.text("Derecho", size="2", color=DARK_THEME["colors"]["text_muted"]),
            rx.spacer(),
            rx.badge("I", color_scheme="green", variant="soft"),
            rx.text("Izquierdo", size="2", color=DARK_THEME["colors"]["text_muted"]),
            spacing="2",
            width="200px",
            justify_content="center",
            margin_top="4"
        ),
        
        spacing="4",
        width="100%",
        align_items="center"
    )

# ==========================================
# 🛠️ TOOLBAR DE HERRAMIENTAS
# ==========================================

def odontogram_toolbar_professional() -> rx.Component:
    """🛠️ Barra de herramientas profesional optimizada para odontólogos"""
    
    return rx.vstack(
        # Fila 1: Estado del paciente y navegación rápida
        rx.hstack(
            # Estado del paciente
            rx.hstack(
                rx.icon(tag="user", size=16, color=COLORS["info"]["500"]),
                rx.text(
                    AppState.paciente_actual.nombre_completo,
                    size="3", weight="bold", color=DARK_THEME["colors"]["text_primary"]
                ),
                rx.badge(
                    f"HC: {AppState.paciente_actual.numero_historia}",
                    color_scheme="blue", variant="soft", size="1"
                ),
                spacing="2", align_items="center"
            ),
            
            rx.spacer(),
            
            # Navegación rápida por cuadrantes
            rx.hstack(
                rx.text("Cuadrantes:", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                rx.button(
                    "Q1", size="1", variant="soft", color_scheme="blue",
                    on_click=AppState.select_quadrant_optimized(1)
                ),
                rx.button(
                    "Q2", size="1", variant="soft", color_scheme="green", 
                    on_click=AppState.select_quadrant_optimized(2)
                ),
                rx.button(
                    "Q3", size="1", variant="soft", color_scheme="orange",
                    on_click=AppState.select_quadrant_optimized(3)
                ),
                rx.button(
                    "Q4", size="1", variant="soft", color_scheme="red",
                    on_click=AppState.select_quadrant_optimized(4)
                ),
                spacing="1", align_items="center"
            ),
            
            spacing="4", width="100%", align_items="center"
        ),
        
        # Fila 2: Herramientas principales
        rx.hstack(
            # Indicadores de estado
            rx.hstack(
                rx.icon(tag="activity", size=16, color=COLORS["success"]["500"]),
                rx.text("Modo Edición", size="2", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                rx.cond(
                    AppState.diente_seleccionado,
                    rx.badge(
                        f"Diente {AppState.diente_seleccionado}",
                        color_scheme="cyan", variant="soft"
                    )
                ),
                spacing="2", align_items="center"
            ),
            
            rx.spacer(),
            
            # Estadísticas rápidas
            rx.hstack(
                rx.foreach(
                    AppState.odontogram_stats_summary,
                    lambda stat: rx.cond(
                        stat[1] > 0,
                        rx.badge(
                            f"{stat[0]}: {stat[1]}",
                            color_scheme=rx.match(
                                stat[0],
                                ("Sanos", "green"),
                                ("Caries", "red"),
                                ("Obturaciones", "blue"),
                                ("Otros", "orange"),
                                "gray"
                            ),
                            variant="soft", size="1"
                        )
                    )
                ),
                spacing="1"
            ),
            
            rx.spacer(),
            
            # Acciones principales
            rx.hstack(
                rx.button(
                    rx.icon(tag="save", size=14),
                    "Guardar",
                    size="2", variant="soft", color_scheme="green",
                    disabled=AppState.cambios_pendientes_odontograma.length() == 0,
                    on_click=AppState.save_odontogram_changes_optimized
                ),
                rx.button(
                    rx.icon(tag="undo", size=14),
                    "Deshacer", 
                    size="2", variant="soft", color_scheme="gray",
                    disabled=AppState.cambios_pendientes_odontograma.length() == 0
                ),
                spacing="2"
            ),
            
            spacing="4", width="100%", align_items="center"
        ),
        
        spacing="2", width="100%",
        padding="3",
        style={
            "background": "rgba(255, 255, 255, 0.06)",
            "backdrop_filter": "blur(20px)",
            "border_radius": RADIUS["lg"],
            "border": f"1px solid {DARK_THEME['colors']['primary']}"
        }
    )

# Función de compatibilidad con el toolbar anterior
def odontogram_toolbar() -> rx.Component:
    """🛠️ Barra de herramientas para el odontograma interactivo"""
    
    return rx.hstack(
        # Indicador de estado
        rx.hstack(
            rx.icon(tag="activity", size=16, color=COLORS["primary"]["500"]),
            rx.text("Modo Edición", size="3", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
            spacing="2"
        ),
        
        rx.spacer(),
        
        # Herramientas de acción
        rx.hstack(
            # Botón deshacer
            rx.tooltip(
                rx.button(
                    rx.icon(tag="undo", size=16),
                    size="2",
                    variant="ghost",
                    color_scheme="gray",
                    on_click=rx.noop,  # Placeholder - AppState.undo_last_change
                    disabled=True  # Placeholder - rx.cond(AppState.can_undo, False, True)
                ),
                content="Deshacer último cambio"
            ),
            
            # Botón rehacer  
            rx.tooltip(
                rx.button(
                    rx.icon(tag="redo", size=16),
                    size="2", 
                    variant="ghost",
                    color_scheme="gray",
                    on_click=rx.noop,  # Placeholder - AppState.redo_last_change
                    disabled=True  # Placeholder - rx.cond(AppState.can_redo, False, True)
                ),
                content="Rehacer último cambio"
            ),
            
            rx.divider(orientation="vertical", height="24px"),
            
            # Botón resetear
            rx.tooltip(
                rx.button(
                    rx.icon(tag="rotate-ccw", size=16),
                    size="2",
                    variant="ghost", 
                    color_scheme="orange",
                    on_click=AppState.resetear_seleccion_odontograma
                ),
                content="Resetear todos los cambios"
            ),
            
            # Botón guardar cambios
            rx.tooltip(
                rx.button(
                    rx.cond(
                        False,  # Placeholder - AppState.is_saving_odontogram
                        rx.spinner(size="3"),
                        rx.icon(tag="save", size=16)
                    ),
                    "Guardar Cambios",
                    size="2",
                    color_scheme="green",
                    on_click=AppState.guardar_odontograma,
                    disabled=AppState.cambios_pendientes_odontograma.length() == 0
                ),
                content="Guardar cambios en base de datos"
            ),
            
            spacing="2"
        ),
        
        spacing="4",
        align_items="center",
        width="100%",
        padding="3",
        style={
            "background": DARK_THEME["colors"]["surface"],
            "border": f"1px solid {DARK_THEME['colors']['primary']}",
            "border_radius": RADIUS["lg"]
        }
    )

# ==========================================
# 📊 ESTADÍSTICAS DEL ODONTOGRAMA
# ==========================================

def odontogram_stats_panel() -> rx.Component:
    """📊 Panel con estadísticas del odontograma actual"""
    
    return rx.box(
        rx.vstack(
            rx.text("Estadísticas del Odontograma", size="4", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            
            # Contadores por condición
            rx.vstack(
                rx.hstack(
                    rx.box(width="12px", height="12px", background="#90EE90", border_radius="2px"),
                    rx.text("Sanos:", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.text("24", size="2", weight="bold", color=COLORS["success"]["400"]),
                    spacing="2", align_items="center"
                ),
                rx.hstack(
                    rx.box(width="12px", height="12px", background="#FF4500", border_radius="2px"),
                    rx.text("Caries:", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.text("3", size="2", weight="bold", color=COLORS["error"]["400"]),
                    spacing="2", align_items="center"
                ),
                rx.hstack(
                    rx.box(width="12px", height="12px", background="#C0C0C0", border_radius="2px"),
                    rx.text("Obturados:", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.text("5", size="2", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
                    spacing="2", align_items="center"
                ),
                spacing="2", align_items="start"
            ),
            
            rx.divider(color=DARK_THEME["colors"]["border_secondary"]),
            
            # Resumen de salud oral
            rx.vstack(
                rx.text("Índice de Salud Oral:", size="3", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                rx.progress(value=75, color_scheme="green", size="2"),
                rx.text("Bueno (75%)", size="2", color=COLORS["success"]["400"]),
                spacing="1", align_items="start"
            ),
            
            spacing="4", align_items="start", width="100%"
        ),
        style={
            "background": DARK_THEME["colors"]["surface_secondary"],
            "border": f"1px solid {DARK_THEME['colors']['border_primary']}",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "min_width": "200px"
        }
    )

# ==========================================
# 🎯 UTILIDADES PARA EL GRID
# ==========================================

def get_quadrant_teeth_count() -> Dict[str, int]:
    """Obtener conteo de dientes por cuadrante"""
    return {quadrant: len(info["teeth"]) for quadrant, info in FDI_QUADRANTS.items()}

def get_all_fdi_teeth() -> List[int]:
    """Obtener lista completa de todos los dientes FDI"""
    all_teeth = []
    for quadrant_info in FDI_QUADRANTS.values():
        all_teeth.extend(quadrant_info["teeth"])
    return sorted(all_teeth)

def validate_fdi_layout() -> bool:
    """Validar que el layout FDI tenga exactamente 32 dientes"""
    return len(get_all_fdi_teeth()) == 32

def get_tooth_quadrant_info(tooth_number: int) -> Optional[Dict[str, Any]]:
    """Obtener información del cuadrante para un diente específico"""
    for quadrant_key, quadrant_info in FDI_QUADRANTS.items():
        if tooth_number in quadrant_info["teeth"]:
            return {
                "quadrant": quadrant_key,
                "label": quadrant_info["label"],
                "position": quadrant_info["position"]
            }
    return None