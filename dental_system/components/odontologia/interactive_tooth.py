# 🦷 COMPONENTE: DIENTE INTERACTIVO CON 5 SUPERFICIES
# dental_system/components/odontologia/interactive_tooth.py

import reflex as rx
from typing import Dict, Optional, Any
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 CONFIGURACIÓN DE COLORES Y CONDICIONES
# ==========================================

# Sistema de colores médicamente apropiado para condiciones dentales
CONDITION_COLORS = {
    # Condiciones básicas
    "sano": "#90EE90",              # Verde claro - diente sano
    "caries": "#FF4500",            # Rojo-naranja - caries activa
    "obturado": "#C0C0C0",          # Plata - obturación
    
    # Protésicas
    "corona": "#4169E1",            # Azul real - corona
    "puente": "#800080",            # Púrpura - puente
    "implante": "#32CD32",          # Verde lima - implante
    
    # Estados especiales
    "ausente": "#2F2F2F",           # Gris oscuro - diente ausente
    "fractura": "#FF6347",          # Tomate - fractura
    "endodoncia": "#FFD700",        # Oro - tratamiento endodóntico
    "extraccion": "#8B0000",        # Rojo oscuro - para extracción
    
    # Materiales específicos
    "protesis": "#DA70D6",          # Orquídea - prótesis
    "sellantes": "#87CEEB",         # Azul cielo - sellantes
    "composite": "#F0E68C",         # Caqui - composite
    "amalgama": "#696969",          # Gris dim - amalgama
    "ceramica": "#FFF8DC",          # Cornsilk - cerámica
    "metal": "#708090",             # Gris pizarra - metal
    "resina": "#F5DEB3",            # Trigo - resina
    
    # Estados de tratamiento
    "temporal": "#DDA0DD",          # Ciruela - tratamiento temporal
    "planificado": "#FFE4B5",       # Mocasín - tratamiento planificado
    "en_tratamiento": "#FFA500",    # Naranja - en tratamiento
    "completado": "#98FB98"         # Verde pálido - tratamiento completado
}

# Nombres legibles para mostrar en UI
CONDITION_NAMES = {
    "sano": "Sano",
    "caries": "Caries",
    "obturado": "Obturado",
    "corona": "Corona",
    "puente": "Puente",
    "implante": "Implante",
    "ausente": "Ausente",
    "fractura": "Fractura",
    "endodoncia": "Endodoncia",
    "extraccion": "Extracción",
    "protesis": "Prótesis",
    "sellantes": "Sellantes",
    "composite": "Composite",
    "amalgama": "Amalgama",
    "ceramica": "Cerámica",
    "metal": "Metal",
    "resina": "Resina",
    "temporal": "Temporal",
    "planificado": "Planificado",
    "en_tratamiento": "En Tratamiento",
    "completado": "Completado"
}

# Categorías para organizar condiciones
CONDITION_CATEGORIES = {
    "basicas": ["sano", "caries", "fractura"],
    "restaurativas": ["obturado", "composite", "amalgama", "resina"],
    "protesicas": ["corona", "puente", "protesis", "implante"],
    "preventivas": ["sellantes"],
    "quirurgicas": ["extraccion", "ausente"],
    "endodonticas": ["endodoncia"],
    "materiales": ["ceramica", "metal"],
    "estados": ["temporal", "planificado", "en_tratamiento", "completado"]
}

# ==========================================
# 🦷 ESTILOS PARA DIENTE Y SUPERFICIES
# ==========================================

# Dimensiones y estilo del diente
TOOTH_STYLE = {
    "width": "60px",
    "height": "60px",
    "border_radius": RADIUS["xl"],
    "position": "relative",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "font_size": "12px",
    "font_weight": "bold",
    "color": DARK_THEME["colors"]["text_primary"],
    "border": f"2px solid {DARK_THEME['colors']['primary']}",
    "background": DARK_THEME["colors"]["surface_secondary"]
}

# Estilo cuando el diente está seleccionado
TOOTH_SELECTED_STYLE = {
    **TOOTH_STYLE,
    "border": f"3px solid {COLORS['primary']['500']}",
    "box_shadow": f"0 0 20px {COLORS['primary']['500']}40",
    "transform": "scale(1.05)"
}

# Posicionamiento anatómico de las 5 superficies
SURFACE_POSITIONS = {
    "oclusal": {
        "position": "absolute",
        "top": "15%",
        "left": "25%",
        "width": "50%",
        "height": "25%",
        "border_radius": f"{RADIUS['md']} {RADIUS['md']} 0 0"
    },
    "mesial": {
        "position": "absolute",
        "left": "8%",
        "top": "25%",
        "width": "25%",
        "height": "50%",
        "border_radius": f"{RADIUS['md']} 0 0 {RADIUS['md']}"
    },
    "distal": {
        "position": "absolute",
        "right": "8%",
        "top": "25%",
        "width": "25%",
        "height": "50%",
        "border_radius": f"0 {RADIUS['md']} {RADIUS['md']} 0"
    },
    "vestibular": {
        "position": "absolute",
        "bottom": "25%",
        "left": "25%",
        "width": "50%",
        "height": "25%",
        "border_radius": f"0 0 {RADIUS['md']} {RADIUS['md']}"
    },
    "lingual": {
        "position": "absolute",
        "bottom": "8%",
        "left": "25%",
        "width": "50%",
        "height": "20%",
        "border_radius": f"0 0 {RADIUS['lg']} {RADIUS['lg']}"
    }
}

# ==========================================
# 🧩 COMPONENTE: SUPERFICIE INDIVIDUAL
# ==========================================

def tooth_surface(
    tooth_number: int, 
    surface_name: str, 
    condition: str = "sano",
    is_selected: bool = False,
    is_modified: bool = False
) -> rx.Component:
    """
    🦷 Renderiza una superficie individual del diente
    
    Args:
        tooth_number: Número FDI del diente (11-48)
        surface_name: Nombre de la superficie (oclusal, mesial, distal, vestibular, lingual)
        condition: Condición actual de la superficie
        is_selected: Si esta superficie está seleccionada
        is_modified: Si esta superficie tiene cambios pendientes
    """
    
    # Color base según condición
    base_color = CONDITION_COLORS.get(condition, CONDITION_COLORS["sano"])
    
    # Estilos base
    base_style = {
        **SURFACE_POSITIONS[surface_name],
        "background": base_color,
        "cursor": "pointer",
        "transition": "all 0.2s ease",
        "opacity": "0.8",
        "_hover": {
            "opacity": "1.0",
            "transform": "scale(1.1)",
            "z_index": "10",
            "box_shadow": f"0 4px 12px {base_color}60"
        }
    }
    
    # Estilos condicionales usando rx.cond
    surface_style = rx.cond(
        is_selected,
        {
            **base_style,
            "border": f"2px solid {COLORS['primary']['400']}",
            "box_shadow": f"0 0 8px {COLORS['primary']['400']}80",
            "z_index": "5"
        },
        rx.cond(
            is_modified,
            {
                **base_style,
                "border": f"2px solid {COLORS['warning']['400']}",
                "box_shadow": f"0 0 8px {COLORS['warning']['400']}60",
                "animation": "pulse 2s infinite"
            },
            {
                **base_style,
                "border": f"1px solid {DARK_THEME['colors']['primary']}"
            }
        )
    )
    
    return rx.tooltip(
        rx.box(
            style=surface_style,
            on_click=lambda: AppState.select_tooth_surface(tooth_number, surface_name)
        ),
        content=f"{surface_name.title()}: {CONDITION_NAMES.get(condition, condition)}"
    )

# ==========================================
# 🦷 COMPONENTE: DIENTE COMPLETO INTERACTIVO
# ==========================================

def interactive_tooth(
    tooth_number: int,
    conditions: Optional[Dict[str, str]] = None,
    is_selected: bool = False,
    pending_changes: Optional[Dict[str, str]] = None
) -> rx.Component:
    """
    🦷 Componente principal del diente interactivo con 5 superficies
    
    Args:
        tooth_number: Número FDI del diente (11-48)
        conditions: Diccionario con condiciones por superficie
        is_selected: Si este diente está seleccionado actualmente
        pending_changes: Cambios pendientes sin guardar
    """
    
    # Condiciones por defecto si no se proporcionan
    if conditions is None:
        conditions = {
            "oclusal": "sano",
            "mesial": "sano", 
            "distal": "sano",
            "vestibular": "sano",
            "lingual": "sano"
        }
    
    # Cambios pendientes si existen (usando rx.cond para evitar error de Reflex)
    pending = rx.cond(pending_changes, pending_changes, {})
    
    # Determinar si el diente tiene modificaciones
    has_modifications = rx.cond(pending_changes, True, False)
    
    # Estilo del contenedor principal
    container_style = rx.cond(is_selected, TOOTH_SELECTED_STYLE, TOOTH_STYLE)
    
    return rx.box(
        # Número del diente (centrado)
        rx.text(
            str(tooth_number),
            style={
                "position": "absolute",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "z_index": "1",
                "font_size": "11px",
                "font_weight": "bold",
                "color": DARK_THEME["colors"]["text_primary"],
                "text_shadow": "1px 1px 2px rgba(0,0,0,0.8)",
                "pointer_events": "none"
            }
        ),
        
        # 5 superficies del diente
        tooth_surface(
            tooth_number, 
            "oclusal", 
            rx.cond(pending_changes, 
                   rx.cond(pending_changes["oclusal"], pending_changes["oclusal"], conditions.get("oclusal", "sano")),
                   conditions.get("oclusal", "sano")),
            is_selected & (AppState.selected_surface == "oclusal"),
            rx.cond(pending_changes, rx.cond(pending_changes["oclusal"], True, False), False)
        ),
        tooth_surface(
            tooth_number,
            "mesial",
            rx.cond(pending_changes, 
                   rx.cond(pending_changes["mesial"], pending_changes["mesial"], conditions.get("mesial", "sano")),
                   conditions.get("mesial", "sano")),
            is_selected & (AppState.selected_surface == "mesial"),
            rx.cond(pending_changes, rx.cond(pending_changes["mesial"], True, False), False)
        ),
        tooth_surface(
            tooth_number,
            "distal", 
            rx.cond(pending_changes, 
                   rx.cond(pending_changes["distal"], pending_changes["distal"], conditions.get("distal", "sano")),
                   conditions.get("distal", "sano")),
            is_selected & (AppState.selected_surface == "distal"),
            rx.cond(pending_changes, rx.cond(pending_changes["distal"], True, False), False)
        ),
        tooth_surface(
            tooth_number,
            "vestibular",
            rx.cond(pending_changes, 
                   rx.cond(pending_changes["vestibular"], pending_changes["vestibular"], conditions.get("vestibular", "sano")),
                   conditions.get("vestibular", "sano")),
            is_selected & (AppState.selected_surface == "vestibular"), 
            rx.cond(pending_changes, rx.cond(pending_changes["vestibular"], True, False), False)
        ),
        tooth_surface(
            tooth_number,
            "lingual",
            rx.cond(pending_changes, 
                   rx.cond(pending_changes["lingual"], pending_changes["lingual"], conditions.get("lingual", "sano")),
                   conditions.get("lingual", "sano")),
            is_selected & (AppState.selected_surface == "lingual"),
            rx.cond(pending_changes, rx.cond(pending_changes["lingual"], True, False), False)
        ),
        
        # Indicador de modificaciones (pequeño punto naranja)
        rx.cond(
            has_modifications,
            rx.box(
                style={
                    "position": "absolute",
                    "top": "5px",
                    "right": "5px",
                    "width": "8px",
                    "height": "8px",
                    "background": COLORS["warning"]["500"],
                    "border_radius": "50%",
                    "z_index": "20",
                    "box_shadow": f"0 0 4px {COLORS['warning']['500']}80",
                    "animation": "pulse 1.5s infinite"
                }
            )
        ),
        
        style=container_style,
        on_click=lambda: AppState.select_tooth(tooth_number)
    )

# ==========================================
# 🎨 UTILIDADES DE ESTILO Y COLORES
# ==========================================

def get_condition_color(condition: str) -> str:
    """Obtener color hexadecimal para una condición específica"""
    return CONDITION_COLORS.get(condition, CONDITION_COLORS["sano"])

def get_condition_name(condition: str) -> str:
    """Obtener nombre legible para una condición"""
    return CONDITION_NAMES.get(condition, condition.title())

def get_conditions_by_category(category: str) -> list:
    """Obtener lista de condiciones por categoría"""
    return CONDITION_CATEGORIES.get(category, [])

def is_condition_valid_for_surface(condition: str, surface: str, tooth_type: str = "molar") -> bool:
    """
    Validar si una condición es válida para una superficie específica
    
    Args:
        condition: Condición a validar
        surface: Superficie del diente
        tooth_type: Tipo de diente (incisivo, canino, premolar, molar)
    
    Returns:
        True si la condición es válida para la superficie
    """
    
    # Validaciones básicas
    if condition == "ausente":
        # Si el diente está ausente, no puede tener otras condiciones
        return surface == "oclusal"  # Solo marcar en oclusal para simplificar
    
    if surface == "oclusal" and tooth_type in ["incisivo", "canino"]:
        # Incisivos y caninos usan superficie "incisal" en lugar de "oclusal"
        return condition not in ["sellantes"]  # Sellantes principalmente en molares
    
    # Implantes requieren al menos superficie oclusal
    if condition == "implante":
        return True  # Implantes pueden ir en cualquier superficie
        
    # Por defecto, todas las condiciones son válidas
    return True

# ==========================================
# 📊 INFORMACIÓN DE DIENTE SELECCIONADO
# ==========================================

def selected_tooth_info_panel() -> rx.Component:
    """Panel informativo del diente seleccionado"""
    return rx.cond(
        AppState.selected_tooth,
        rx.box(
            rx.vstack(
                rx.text(
                    f"Diente: {AppState.selected_tooth}",
                    size="4",
                    weight="bold",
                    color=COLORS["primary"]["500"]
                ),
                rx.cond(
                    AppState.selected_surface,
                    rx.text(
                        f"Superficie: {AppState.selected_surface}",
                        size="3",
                        color=DARK_THEME["colors"]["text_secondary"]
                    )
                ),
                rx.text(
                    "Click en una superficie para cambiar condición",
                    size="2",
                    color=DARK_THEME["colors"]["text_muted"]
                ),
                spacing="2",
                align_items="start"
            ),
            style={
                "background": DARK_THEME["colors"]["surface_secondary"],
                "border": f"1px solid {DARK_THEME['colors']['primary']}",
                "border_radius": RADIUS["lg"],
                "padding": SPACING["4"],
                "min_width": "200px"
            }
        )
    )

# ==========================================
# 🔧 FUNCIONES AUXILIARES DE VALIDACIÓN
# ==========================================

def validate_tooth_number(tooth_number: int) -> bool:
    """Validar que el número de diente sea válido según FDI"""
    valid_adult_teeth = [
        # Cuadrante 1 (Superior Derecho)
        18, 17, 16, 15, 14, 13, 12, 11,
        # Cuadrante 2 (Superior Izquierdo) 
        21, 22, 23, 24, 25, 26, 27, 28,
        # Cuadrante 3 (Inferior Izquierdo)
        31, 32, 33, 34, 35, 36, 37, 38,
        # Cuadrante 4 (Inferior Derecho)
        41, 42, 43, 44, 45, 46, 47, 48
    ]
    return tooth_number in valid_adult_teeth

def get_tooth_type(tooth_number: int) -> str:
    """Determinar el tipo de diente basado en el número FDI"""
    if not validate_tooth_number(tooth_number):
        return "unknown"
    
    # Obtener el último dígito para determinar el tipo
    last_digit = tooth_number % 10
    
    if last_digit in [1, 2]:
        return "incisivo"
    elif last_digit == 3:
        return "canino"
    elif last_digit in [4, 5]:
        return "premolar"
    elif last_digit in [6, 7, 8]:
        return "molar"
    else:
        return "unknown"

def get_tooth_quadrant(tooth_number: int) -> int:
    """Obtener el cuadrante FDI del diente"""
    if not validate_tooth_number(tooth_number):
        return 0
    
    return tooth_number // 10