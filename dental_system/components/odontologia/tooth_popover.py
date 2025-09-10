# 🦷 COMPONENTE: POPOVER CONTEXTUAL DEL DIENTE
# dental_system/components/odontologia/tooth_popover.py

import reflex as rx
from typing import Dict, Any, Optional, List
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS DEL POPOVER MEJORADOS
# ==========================================

# Overlay de fondo para cerrar el popover
POPOVER_OVERLAY_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0", 
    "width": "100vw",
    "height": "100vh",
    "background": "rgba(0, 0, 0, 0.1)",
    "z_index": "999",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center"
}

# Contenedor principal del popover - centrado
POPOVER_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.3)",
    "border": f"1px solid {COLORS['gray']['200']}",
    "width": "350px",
    "max_height": "500px",
    "max_width": "90vw",
    "overflow": "hidden",
    "position": "relative"
}

# Header con botón de cerrar
POPOVER_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "color": "white",
    "padding": SPACING["4"],
    "display": "flex",
    "justify_content": "space-between",
    "align_items": "center"
}

# Contenido con scroll si es necesario
POPOVER_CONTENT_STYLE = {
    "padding": SPACING["4"],
    "max_height": "400px",
    "overflow_y": "auto",
    "color": COLORS["gray"]["800"]  # Texto oscuro para visibilidad
}

# Estilos para el contenido interno
SURFACE_INDICATOR_STYLE = {
    "display": "flex",
    "align_items": "center",
    "gap": SPACING["2"],
    "margin_bottom": SPACING["1"]
}

# Estilo para secciones con texto visible
SECTION_STYLE = {
    "background": COLORS["gray"]["50"],
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["2"]
}

# Estilo para títulos de sección
SECTION_TITLE_STYLE = {
    "font_weight": "bold",
    "color": COLORS["gray"]["700"],
    "margin_bottom": SPACING["2"]
}

CONDITION_COLORS = {
    "sano": "#22C55E",      # Verde
    "caries": "#EF4444",    # Rojo
    "obturado": "#6B7280",  # Gris
    "corona": "#3B82F6",    # Azul
    "ausente": "#1F2937",   # Gris oscuro
    "fractura": "#F59E0B",  # Amarillo
    "endodoncia": "#8B5CF6" # Púrpura
}

# ==========================================
# 🧩 COMPONENTES INTERNOS
# ==========================================

def surface_condition_indicator(surface_name: str, condition: str) -> rx.Component:
    """🎨 Indicador visual de condición por superficie"""
    color = CONDITION_COLORS.get(condition, CONDITION_COLORS["sano"])
    
    return rx.hstack(
        # Círculo de color
        rx.box(
            width="12px",
            height="12px",
            border_radius="50%",
            background=color,
            border="2px solid rgba(255, 255, 255, 0.8)"
        ),
        
        # Nombre de superficie
        rx.text(
            surface_name.title(),
            font_size="13px",
            font_weight="medium",
            color=COLORS["gray"]["700"],
            min_width="70px"
        ),
        
        # Condición actual
        rx.text(
            condition.title(),
            font_size="12px",
            color=color,
            font_weight="bold"
        ),
        
        spacing="2",
        align_items="center",
        width="100%"
    )

def tooth_info_header(tooth_number: int) -> rx.Component:
    """🦷 Header con información básica del diente y botón cerrar"""
    return rx.hstack(
        # Información principal
        rx.vstack(
            rx.text(
                f"Diente {tooth_number}",
                font_size="18px",
                font_weight="bold",
                color="white"
            ),
            rx.text(
                AppState.obtener_nombre_diente_fdi,
                font_size="13px",
                color="rgba(255, 255, 255, 0.9)"
            ),
            spacing="1",
            align_items="start"
        ),
        
        rx.spacer(),
        
        # Botón de cerrar
        rx.button(
            rx.icon("x", size=18),
            size="2",
            variant="ghost",
            color="white",
            on_click=AppState.cerrar_popover_diente,
            _hover={
                "background": "rgba(255, 255, 255, 0.1)"
            }
        ),
        
        width="100%",
        align_items="center"
    )

def surfaces_section() -> rx.Component:
    """🎨 Sección de condiciones por superficie"""
    return rx.box(
        rx.vstack(
            rx.text(
                "🎨 Condiciones por Superficie",
                style=SECTION_TITLE_STYLE
            ),
            
            # Lista de superficies
            surface_condition_indicator("oclusal", "sano"),
            surface_condition_indicator("mesial", "sano"),
            surface_condition_indicator("distal", "caries"),
            surface_condition_indicator("vestibular", "sano"),
            surface_condition_indicator("lingual", "sano"),
            
            spacing="2",
            width="100%",
            align_items="start"
        ),
        style=SECTION_STYLE
    )

# Funciones eliminadas - contenido integrado directamente en el popover principal

# Función eliminada - contenido integrado directamente en el popover principal

# ==========================================
# 📋 COMPONENTE PRINCIPAL
# ==========================================

def tooth_popover() -> rx.Component:
    """
    🦷 Popover contextual con información detallada del diente seleccionado
    
    Aparece flotante cerca del diente clickeado con:
    - Información básica del diente (número FDI, tipo)
    - Condiciones actuales por superficie
    - Historial reciente de tratamientos
    - Botones de acción rápida
    """
    
    return rx.cond(
        AppState.popover_diente_abierto & (AppState.diente_seleccionado != None),
        
        # Overlay de fondo para centrar y cerrar el popover
        rx.box(
            # Contenedor del popover centrado
            rx.box(
                rx.vstack(
                    # Header con información básica
                    rx.box(
                        tooth_info_header(AppState.diente_seleccionado),
                        style=POPOVER_HEADER_STYLE
                    ),
                    
                    # Contenido principal
                    rx.box(
                        rx.vstack(
                            # Sección de superficies
                            surfaces_section(),
                            
                            # Sección de tratamientos recientes (simplificada)
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "📈 Últimos Tratamientos",
                                        style=SECTION_TITLE_STYLE
                                    ),
                                    rx.text(
                                        "Profilaxis dental - 2024-01-15",
                                        font_size="12px",
                                        color=COLORS["gray"]["600"]
                                    ),
                                    rx.text(
                                        "Revisión general - 2023-08-20",
                                        font_size="12px",
                                        color=COLORS["gray"]["600"]
                                    ),
                                    spacing="2",
                                    align_items="start"
                                ),
                                style=SECTION_STYLE
                            ),
                            
                            # Sección de acciones rápidas
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "⚡ Acciones Rápidas",
                                        style=SECTION_TITLE_STYLE
                                    ),
                                    rx.hstack(
                                        rx.button(
                                            "📝 Agregar Nota",
                                            size="2",
                                            variant="outline",
                                            color_scheme="blue"
                                        ),
                                        rx.button(
                                            "🩺 Iniciar Tratamiento",
                                            size="2",
                                            color_scheme="green"
                                        ),
                                        spacing="2",
                                        width="100%"
                                    ),
                                    spacing="2",
                                    align_items="start"
                                ),
                                style=SECTION_STYLE
                            ),
                            
                            spacing="3",
                            width="100%"
                        ),
                        style=POPOVER_CONTENT_STYLE
                    ),
                    
                    spacing="0",
                    width="100%"
                ),
                style=POPOVER_CONTAINER_STYLE
            ),
            
            style=POPOVER_OVERLAY_STYLE,
            on_click=AppState.cerrar_popover_diente  # Cerrar al clickear fuera
        ),
        
        # Estado vacío cuando no está abierto
        rx.fragment()
    )

# ==========================================
# 🧪 UTILIDADES Y HELPERS  
# ==========================================

def get_tooth_type_name(tooth_number: int) -> str:
    """Obtener nombre descriptivo del tipo de diente"""
    last_digit = tooth_number % 10
    quadrant = tooth_number // 10
    
    # Determinar tipo
    if last_digit in [1, 2]:
        tipo = "Incisivo"
    elif last_digit == 3:
        tipo = "Canino"
    elif last_digit in [4, 5]:
        tipo = "Premolar"
    elif last_digit in [6, 7, 8]:
        tipo = "Molar"
    else:
        tipo = "Desconocido"
    
    # Determinar posición
    if last_digit == 1:
        posicion = "Central"
    elif last_digit == 2:
        posicion = "Lateral"
    elif last_digit == 4:
        posicion = "Primer"
    elif last_digit == 5:
        posicion = "Segundo"
    elif last_digit == 6:
        posicion = "Primer"
    elif last_digit == 7:
        posicion = "Segundo"
    elif last_digit == 8:
        posicion = "Tercer"
    else:
        posicion = ""
    
    # Determinar cuadrante
    if quadrant == 1:
        cuadrante = "Superior Derecho"
    elif quadrant == 2:
        cuadrante = "Superior Izquierdo"
    elif quadrant == 3:
        cuadrante = "Inferior Izquierdo"
    elif quadrant == 4:
        cuadrante = "Inferior Derecho"
    else:
        cuadrante = "Desconocido"
    
    return f"{posicion} {tipo} {cuadrante}".strip()

# CSS Animation para el popover
POPOVER_ANIMATION_CSS = """
@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
"""