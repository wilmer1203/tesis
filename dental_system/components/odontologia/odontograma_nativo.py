"""
🦷 ODONTOGRAMA NATIVO - VERSIÓN 2.0
===================================

Odontograma interactivo usando SOLO componentes nativos de Reflex.
Sin JavaScript, sin SVG, solo botones y grids de Reflex.

CARACTERÍSTICAS:
- 32 dientes FDI usando rx.button
- Estados visuales con colores
- Interactividad completa con Reflex
- Responsive design
- Sin errores JavaScript
"""

import reflex as rx
from typing import Dict, List, Optional
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🦷 CONFIGURACIÓN FDI Y ESTILOS
# ==========================================

# Numeración FDI estándar para adultos (32 dientes)
CUADRANTES_FDI = {
    "superior_derecho": [18, 17, 16, 15, 14, 13, 12, 11],  # Cuadrante 1
    "superior_izquierdo": [21, 22, 23, 24, 25, 26, 27, 28],  # Cuadrante 2
    "inferior_izquierdo": [31, 32, 33, 34, 35, 36, 37, 38],  # Cuadrante 3
    "inferior_derecho": [48, 47, 46, 45, 44, 43, 42, 41]   # Cuadrante 4
}

# Colores por condición dental
COLORES_CONDICIONES = {
    "sano": "green",
    "caries": "red",
    "obturado": "blue",
    "corona": "orange",
    "extraccion": "gray",
    "implante": "purple",
    "endodoncia": "pink",
    "protesis": "teal",
    "defecto": "orange",
    "sellante": "cyan",
    "seleccionado": "yellow"
}

# Estilos para dientes
def get_diente_style(numero: int, condicion: str = "sano", seleccionado: bool = False) -> Dict:
    """Obtener estilo para un diente específico"""
    
    # Determinar tamaño según tipo de diente
    es_molar = numero in [16, 17, 18, 26, 27, 28, 36, 37, 38, 46, 47, 48]
    width = "50px" if es_molar else "40px"
    height = "60px" if es_molar else "50px"
    
    # Color base según condición
    color_base = COLORES_CONDICIONES.get(condicion, "green")
    
    # Override si está seleccionado
    if seleccionado:
        color_base = "yellow"
    
    return {
        "width": width,
        "height": height,
        "font_size": "12px",
        "font_weight": "bold",
        "border_radius": "8px",
        "margin": "2px",
        "display": "flex",
        "flex_direction": "column",
        "align_items": "center",
        "justify_content": "center",
        "cursor": "pointer",
        "transition": "all 0.2s ease",
        "_hover": {
            "transform": "scale(1.05)",
            "box_shadow": "0 4px 12px rgba(0,0,0,0.15)"
        }
    }

# ==========================================
# 🦷 COMPONENTES DE DIENTE INDIVIDUAL
# ==========================================

def diente_boton(numero: int, cuadrante: str = "") -> rx.Component:
    """
    🦷 Botón individual para cada diente
    
    Args:
        numero: Número FDI del diente (11-48)
        cuadrante: Nombre del cuadrante para referencia
    """
    
    return rx.button(
        rx.vstack(
            rx.text(str(numero), size="2", weight="bold"),
            rx.text("🦷", size="1"),
            spacing="0",
            align_items="center"
        ),
        variant="solid",
        color_scheme="green",  # Por ahora todos verdes, después integrar con estado real
        style=get_diente_style(numero, "sano", False),
        on_click=AppState.seleccionar_diente(numero)  # Con mixin=True acceso directo
    )

def cuadrante_superior_derecho() -> rx.Component:
    """🦷 Cuadrante 1 - Superior Derecho"""
    return rx.vstack(
        rx.text("Cuadrante 1", size="2", weight="medium", color="gray.600"),
        rx.hstack(
            *[diente_boton(numero, "superior_derecho") 
              for numero in CUADRANTES_FDI["superior_derecho"]],
            spacing="1"
        ),
        spacing="2",
        align_items="center"
    )

def cuadrante_superior_izquierdo() -> rx.Component:
    """🦷 Cuadrante 2 - Superior Izquierdo"""
    return rx.vstack(
        rx.text("Cuadrante 2", size="2", weight="medium", color="gray.600"),
        rx.hstack(
            *[diente_boton(numero, "superior_izquierdo") 
              for numero in CUADRANTES_FDI["superior_izquierdo"]],
            spacing="1"
        ),
        spacing="2",
        align_items="center"
    )

def cuadrante_inferior_izquierdo() -> rx.Component:
    """🦷 Cuadrante 3 - Inferior Izquierdo"""
    return rx.vstack(
        rx.hstack(
            *[diente_boton(numero, "inferior_izquierdo") 
              for numero in CUADRANTES_FDI["inferior_izquierdo"]],
            spacing="1"
        ),
        rx.text("Cuadrante 3", size="2", weight="medium", color="gray.600"),
        spacing="2",
        align_items="center"
    )

def cuadrante_inferior_derecho() -> rx.Component:
    """🦷 Cuadrante 4 - Inferior Derecho"""
    return rx.vstack(
        rx.hstack(
            *[diente_boton(numero, "inferior_derecho") 
              for numero in CUADRANTES_FDI["inferior_derecho"]],
            spacing="1"
        ),
        rx.text("Cuadrante 4", size="2", weight="medium", color="gray.600"),
        spacing="2",
        align_items="center"
    )

# ==========================================
# 🎨 COMPONENTES AUXILIARES
# ==========================================

def toolbar_odontograma_v2() -> rx.Component:
    """🎨 Toolbar con herramientas del odontograma nativo"""
    return rx.hstack(
        rx.hstack(
            rx.icon("smile", size=24, color="primary.600"),
            rx.vstack(
                rx.text("🦷 Odontograma Nativo", weight="bold", size="4", color="gray.700"),
                rx.text("Selecciona los dientes para la intervención", size="2", color="gray.600"),
                spacing="0",
                align_items="start"
            ),
            spacing="3"
        ),
        rx.spacer(),
        rx.hstack(
            rx.text(
                rx.cond(
                    AppState.total_dientes_seleccionados > 0,
                    f"Seleccionados: {AppState.total_dientes_seleccionados}",
                    "Ningún diente seleccionado"
                ),
                size="2",
                color="blue.600",
                weight="medium"
            ),
            rx.button(
                rx.icon("rotate_ccw", size=16),
                "Limpiar",
                size="2",
                variant="outline",
                on_click=AppState.limpiar_seleccion_dientes
            ),
            spacing="3"
        ),
        width="100%",
        justify="space-between",
        align_items="center",
        padding="4",
        background="white",
        border_radius="lg",
        box_shadow="sm"
    )

def leyenda_condiciones_v2() -> rx.Component:
    """🎨 Leyenda mejorada de colores"""
    return rx.box(
        rx.vstack(
            rx.text("Leyenda de Estados", weight="bold", size="3", margin_bottom="3"),
            rx.grid(
                *[
                    rx.hstack(
                        rx.box(
                            width="20px",
                            height="20px",
                            background=COLORES_CONDICIONES[condicion],
                            border_radius="4px",
                            border="1px solid gray"
                        ),
                        rx.text(condicion.title(), size="2"),
                        spacing="2",
                        align_items="center"
                    )
                    for condicion in ["sano", "caries", "obturado", "corona", "extraccion", "implante"]
                ],
                columns="2",
                spacing="2"
            ),
            align_items="start",
            width="100%"
        ),
        padding="4",
        background="white",
        border_radius="lg",
        box_shadow="sm",
        width="100%"
    )

def resumen_seleccion() -> rx.Component:
    """📋 Resumen de dientes seleccionados"""
    return rx.box(
        rx.vstack(
            rx.text("Dientes Seleccionados", weight="bold", size="3", margin_bottom="3"),
            rx.cond(
                AppState.total_dientes_seleccionados > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.dientes_seleccionados_lista,
                        lambda diente: rx.hstack(
                            rx.text(f"🦷 {diente['numero']}", size="2", weight="medium"),
                            rx.text(diente.get("condicion", "sano").title(), size="2", color="gray.600"),
                            rx.spacer(),
                            rx.button(
                                rx.icon("x", size=12),
                                size="1",
                                variant="ghost",
                                color_scheme="red",
                                on_click=AppState.remover_diente_seleccionado(diente["numero"])
                            ),
                            width="100%",
                            align_items="center",
                            padding="2",
                            border_radius="md",
                            border="1px solid gray.200"
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.text("No hay dientes seleccionados", size="2", color="gray.500", style={"fontStyle": "italic"})
            ),
            align_items="start",
            width="100%"
        ),
        padding="4",
        background="white",
        border_radius="lg",
        box_shadow="sm",
        width="100%"
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL NATIVO
# ==========================================

def odontograma_nativo() -> rx.Component:
    """
    🦷 Odontograma completamente nativo usando solo componentes Reflex
    
    VENTAJAS:
    - Sin errores JavaScript 
    - Interactividad completa con state
    - Responsive design
    - Integración perfecta con AppState
    - Fácil personalización
    """
    
    return rx.box(
        rx.vstack(
            # Toolbar superior
            toolbar_odontograma_v2(),
            
            # Layout principal
            rx.hstack(
                # Odontograma principal (70% del ancho)
                rx.box(
                    rx.vstack(
                        # Maxilar superior
                        rx.hstack(
                            cuadrante_superior_derecho(),
                            rx.divider(orientation="vertical", height="80px"),
                            cuadrante_superior_izquierdo(),
                            spacing="4",
                            align_items="center"
                        ),
                        
                        # Línea media horizontal
                        rx.divider(width="100%", margin_y="4"),
                        
                        # Mandíbula inferior
                        rx.hstack(
                            cuadrante_inferior_derecho(),
                            rx.divider(orientation="vertical", height="80px"),
                            cuadrante_inferior_izquierdo(),
                            spacing="4",
                            align_items="center"
                        ),
                        
                        spacing="6",
                        align_items="center",
                        width="100%"
                    ),
                    width="70%",
                    padding="6",
                    background="gray.50",
                    border_radius="xl",
                    border="2px dashed gray.300"
                ),
                
                # Panel lateral derecho (30% del ancho)
                rx.box(
                    rx.vstack(
                        leyenda_condiciones_v2(),
                        resumen_seleccion(),
                        spacing="4",
                        width="100%"
                    ),
                    width="30%"
                ),
                
                spacing="6",
                width="100%",
                align_items="start"
            ),
            
            spacing="6",
            width="100%"
        ),
        padding="6",
        background="white",
        border_radius="xl",
        box_shadow="lg",
        width="100%"
    )

# ==========================================
# 🎯 COMPONENTE SIMPLIFICADO PARA INTEGRAR
# ==========================================

def odontograma_simple() -> rx.Component:
    """🦷 Versión simplificada para integrar en el formulario"""
    return rx.box(
        rx.vstack(
            # Solo los 4 cuadrantes sin extras
            rx.hstack(
                cuadrante_superior_derecho(),
                cuadrante_superior_izquierdo(),
                spacing="6"
            ),
            rx.divider(width="100%"),
            rx.hstack(
                cuadrante_inferior_derecho(),
                cuadrante_inferior_izquierdo(),
                spacing="6"
            ),
            spacing="4",
            align_items="center"
        ),
        padding="4",
        background="gray.50",
        border_radius="lg",
        width="100%"
    )