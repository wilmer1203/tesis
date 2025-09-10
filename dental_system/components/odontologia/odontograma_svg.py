"""
🦷 COMPONENTE: ODONTOGRAMA SVG INTERACTIVO
==============================================

Odontograma SVG interactivo inspirado en el template React DigitalOdontogramViewer.
Implementa la numeración FDI estándar con 32 dientes y soporte para 5 caras por diente.

CARACTERÍSTICAS:
- SVG interactivo con hover y click
- Numeración FDI (11-18, 21-28, 31-38, 41-48)
- 5 caras por diente (oclusal, mesial, distal, vestibular, lingual)
- Estados visuales por condición
- Integración con estado de Reflex
- Responsive design
"""

import reflex as rx
from typing import Dict, List, Optional
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🦷 CONFIGURACIÓN FDI Y COORDENADAS
# ==========================================

# Numeración FDI estándar para adultos (32 dientes)
CUADRANTES_FDI = {
    "superior_derecho": [18, 17, 16, 15, 14, 13, 12, 11],  # Cuadrante 1
    "superior_izquierdo": [21, 22, 23, 24, 25, 26, 27, 28],  # Cuadrante 2
    "inferior_izquierdo": [31, 32, 33, 34, 35, 36, 37, 38],  # Cuadrante 3
    "inferior_derecho": [48, 47, 46, 45, 44, 43, 42, 41]   # Cuadrante 4
}

# Coordenadas SVG para cada diente (calculadas para disposición anatómica)
COORDENADAS_DIENTES = {
    # Cuadrante superior derecho (maxilar derecho)
    18: {"x": 160, "y": 120}, 17: {"x": 200, "y": 115}, 16: {"x": 240, "y": 110},
    15: {"x": 280, "y": 108}, 14: {"x": 320, "y": 106}, 13: {"x": 360, "y": 105},
    12: {"x": 380, "y": 104}, 11: {"x": 400, "y": 103},
    
    # Cuadrante superior izquierdo (maxilar izquierdo)
    21: {"x": 420, "y": 103}, 22: {"x": 440, "y": 104}, 23: {"x": 480, "y": 105},
    24: {"x": 520, "y": 106}, 25: {"x": 560, "y": 108}, 26: {"x": 600, "y": 110},
    27: {"x": 640, "y": 115}, 28: {"x": 680, "y": 120},
    
    # Cuadrante inferior izquierdo (mandíbula izquierda)
    31: {"x": 420, "y": 297}, 32: {"x": 440, "y": 296}, 33: {"x": 480, "y": 295},
    34: {"x": 520, "y": 294}, 35: {"x": 560, "y": 292}, 36: {"x": 600, "y": 290},
    37: {"x": 640, "y": 285}, 38: {"x": 680, "y": 280},
    
    # Cuadrante inferior derecho (mandíbula derecha)
    48: {"x": 160, "y": 280}, 47: {"x": 200, "y": 285}, 46: {"x": 240, "y": 290},
    45: {"x": 280, "y": 292}, 44: {"x": 320, "y": 294}, 43: {"x": 360, "y": 295},
    42: {"x": 380, "y": 296}, 41: {"x": 400, "y": 297}
}

# Colores por condición dental (inspirado en estándares odontológicos)
COLORES_CONDICIONES = {
    "sano": "#10B981",       # Verde - Diente sano
    "caries": "#EF4444",     # Rojo - Caries
    "obturado": "#3B82F6",   # Azul - Obturación
    "corona": "#F59E0B",     # Amarillo - Corona
    "extraccion": "#6B7280", # Gris - Extracción
    "implante": "#8B5CF6",   # Púrpura - Implante
    "endodoncia": "#EC4899", # Rosa - Endodoncia
    "protesis": "#14B8A6",   # Teal - Prótesis
    "defecto": "#F97316",    # Naranja - Defecto
    "sellante": "#06B6D4",   # primary - Sellante
    "seleccionado": "#FCD34D" # Amarillo claro - Seleccionado
}

# ==========================================
# 🎨 ESTILOS DEL COMPONENTE
# ==========================================

ODONTOGRAMA_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["sm"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["4"],
    "width": "100%",
    "height": "500px",
    "overflow": "hidden"
}

ODONTOGRAMA_HEADER_STYLE = {
    "display": "flex",
    "justify_content": "space-between",
    "align_items": "center",
    "margin_bottom": SPACING["4"],
    "padding_bottom": SPACING["2"],
    "border_bottom": f"1px solid {COLORS['gray']['200']}"
}

# ==========================================
# 🦷 COMPONENTES SVG AUXILIARES
# ==========================================

def diente_svg(numero: int, condicion: str = "sano", seleccionado: bool = False) -> str:
    """Genera el SVG para un diente individual con sus 5 caras"""
    coords = COORDENADAS_DIENTES.get(numero, {"x": 0, "y": 0})
    color_base = COLORES_CONDICIONES.get(condicion, COLORES_CONDICIONES["sano"])
    color_seleccion = COLORES_CONDICIONES["seleccionado"] if seleccionado else color_base
    
    # Tamaño del diente (adaptado por tipo)
    ancho = 32 if numero in [16, 17, 26, 27, 36, 37, 46, 47] else 24  # Molares más grandes
    alto = 40
    
    return f'''
    <g class="diente-{numero}" 
       onclick="selectTooth({numero})" 
       onmouseover="hoverTooth({numero})" 
       onmouseout="unhoverTooth({numero})"
       style="cursor: pointer;">
       
        <!-- Contorno principal del diente -->
        <rect x="{coords['x'] - ancho//2}" 
              y="{coords['y'] - alto//2}" 
              width="{ancho}" 
              height="{alto}" 
              fill="{color_seleccion}" 
              stroke="#374151" 
              stroke-width="2" 
              rx="4"
              class="diente-base"/>
        
        <!-- Número FDI -->
        <text x="{coords['x']}" 
              y="{coords['y'] + 5}" 
              text-anchor="middle" 
              font-size="12" 
              font-weight="bold" 
              fill="white" 
              class="numero-fdi">{numero}</text>
        
        <!-- Caras del diente (5 divisiones) -->
        <!-- Cara oclusal (superior) -->
        <rect x="{coords['x'] - ancho//2 + 4}" 
              y="{coords['y'] - alto//2 + 2}" 
              width="{ancho - 8}" 
              height="8" 
              fill="{color_base}" 
              opacity="0.8" 
              class="cara-oclusal"/>
        
        <!-- Cara mesial (izquierda) -->
        <rect x="{coords['x'] - ancho//2 + 2}" 
              y="{coords['y'] - alto//2 + 10}" 
              width="6" 
              height="{alto - 20}" 
              fill="{color_base}" 
              opacity="0.7" 
              class="cara-mesial"/>
        
        <!-- Cara distal (derecha) -->
        <rect x="{coords['x'] + ancho//2 - 8}" 
              y="{coords['y'] - alto//2 + 10}" 
              width="6" 
              height="{alto - 20}" 
              fill="{color_base}" 
              opacity="0.7" 
              class="cara-distal"/>
        
        <!-- Cara vestibular (frontal) -->
        <rect x="{coords['x'] - ancho//2 + 8}" 
              y="{coords['y'] - 6}" 
              width="{ancho - 16}" 
              height="4" 
              fill="{color_base}" 
              opacity="0.6" 
              class="cara-vestibular"/>
        
        <!-- Cara lingual (posterior) -->
        <rect x="{coords['x'] - ancho//2 + 8}" 
              y="{coords['y'] + 2}" 
              width="{ancho - 16}" 
              height="4" 
              fill="{color_base}" 
              opacity="0.6" 
              class="cara-lingual"/>
    </g>
    '''

def anatomia_svg() -> str:
    """Genera las líneas de referencia anatómica"""
    return '''
    <!-- Línea media -->
    <line x1="410" y1="80" x2="410" y2="320" 
          stroke="#CBD5E1" stroke-width="2" stroke-dasharray="5,5"/>
    
    <!-- Línea oclusal -->
    <line x1="140" y1="200" x2="700" y2="200" 
          stroke="#CBD5E1" stroke-width="1" stroke-dasharray="3,3"/>
    
    <!-- Contorno maxilar superior -->
    <path d="M 140 130 Q 410 90 700 130 L 680 170 Q 410 130 160 170 Z"
          fill="none" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="8,4"/>
    
    <!-- Contorno mandibular inferior -->
    <path d="M 160 230 Q 410 270 680 230 L 700 270 Q 410 310 140 270 Z"
          fill="none" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="8,4"/>
    
    <!-- Etiquetas de cuadrantes -->
    <text x="280" y="95" text-anchor="middle" font-size="12" fill="#6B7280" font-weight="medium">Cuadrante 1</text>
    <text x="540" y="95" text-anchor="middle" font-size="12" fill="#6B7280" font-weight="medium">Cuadrante 2</text>
    <text x="540" y="325" text-anchor="middle" font-size="12" fill="#6B7280" font-weight="medium">Cuadrante 3</text>
    <text x="280" y="325" text-anchor="middle" font-size="12" fill="#6B7280" font-weight="medium">Cuadrante 4</text>
    '''

# ==========================================
# 🎮 COMPONENTES DE INTERACCIÓN
# ==========================================

def toolbar_odontograma() -> rx.Component:
    """🎨 Toolbar con herramientas de odontograma"""
    return rx.hstack(
        rx.text("🦷 Odontograma Interactivo", weight="bold", size="4", color="gray.700"),
        rx.spacer(),
        rx.hstack(
            rx.button(
                rx.icon("rotate_ccw", size=16),
                "Resetear",
                size="2",
                variant="outline",
                on_click=AppState.resetear_seleccion_odontograma
            ),
            rx.button(
                rx.icon("save", size=16),
                "Guardar",
                size="2",
                color_scheme="blue",
                on_click=AppState.guardar_odontograma
            ),
            spacing="2"
        ),
        **ODONTOGRAMA_HEADER_STYLE
    )

def leyenda_condiciones() -> rx.Component:
    """🎨 Leyenda de colores por condición"""
    return rx.vstack(
        rx.text("Leyenda", weight="medium", size="3", margin_bottom="2"),
        rx.grid(
            *[
                rx.hstack(
                    rx.box(
                        width="16px",
                        height="16px",
                        background=color,
                        border_radius="4px",
                        border="1px solid #D1D5DB"
                    ),
                    rx.text(condicion.title(), size="2", color="gray.700"),
                    spacing="2",
                    align_items="center"
                )
                for condicion, color in COLORES_CONDICIONES.items()
                if condicion != "seleccionado"
            ],
            columns="2",
            spacing="2"
        ),
        align_items="start",
        width="100%"
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL
# ==========================================

def odontograma_interactivo() -> rx.Component:
    """
    🦷 Odontograma SVG interactivo completo
    
    Componente principal que integra:
    - SVG con 32 dientes FDI
    - Interactividad (hover, click)
    - Estados visuales por condición
    - Toolbar con herramientas
    - Leyenda de colores
    """
    
    # Generar todos los dientes con sus condiciones actuales
    todos_dientes = []
    for cuadrante_dientes in CUADRANTES_FDI.values():
        todos_dientes.extend(cuadrante_dientes)
    
    # SVG del odontograma
    svg_content = f'''
    <svg width="100%" height="400" viewBox="0 0 840 400" 
         style="border: 1px solid #E5E7EB; border-radius: 8px; background: #FAFAFA;">
         
        <!-- Anatomía de referencia -->
        {anatomia_svg()}
        
        <!-- Todos los dientes -->
        {''.join([
            diente_svg(
                numero, 
                "sano",  # Por ahora todos sanos, después integrar con AppState
                False    # Selección
            ) 
            for numero in todos_dientes
        ])}
    </svg>
    '''
    
    return rx.box(
        # JavaScript para interactividad del odontograma
        rx.script("""
            // Funciones globales para el odontograma interactivo
            function selectTooth(numero) {
                console.log('Diente seleccionado:', numero);
                
                // Visual feedback inmediato
                const diente = document.querySelector('.diente-' + numero + ' .diente-base');
                if (diente) {
                    // Cambiar estilo para mostrar selección
                    diente.style.stroke = '#3B82F6';
                    diente.style.strokeWidth = '3';
                    diente.style.filter = 'brightness(1.1)';
                }
                
                // Trigger evento Reflex (conexión con Python)
                if (typeof window !== 'undefined' && window._reflex_state) {
                    // Llamar función de Reflex si está disponible
                    try {
                        window._reflex_state.seleccionar_diente(numero);
                    } catch (e) {
                        console.log('Reflex state no disponible, usando fallback');
                    }
                }
            }
            
            function hoverTooth(numero) {
                const diente = document.querySelector('.diente-' + numero + ' .diente-base');
                if (diente) {
                    diente.style.filter = 'brightness(1.2)';
                    diente.style.strokeWidth = '3';
                    diente.style.transition = 'all 0.2s ease';
                }
            }
            
            function unhoverTooth(numero) {
                const diente = document.querySelector('.diente-' + numero + ' .diente-base');
                if (diente) {
                    diente.style.filter = 'brightness(1)';
                    diente.style.strokeWidth = '2';
                }
            }
            
            // Inicializar cuando el DOM esté listo
            document.addEventListener('DOMContentLoaded', function() {
                console.log('Odontograma JavaScript inicializado correctamente');
            });
        """),
        
        rx.vstack(
            # Toolbar superior
            toolbar_odontograma(),
            
            # Contenido principal
            rx.hstack(
                # Odontograma SVG
                rx.box(
                    rx.html(svg_content),
                    width="70%"
                ),
                
                # Panel lateral con leyenda
                rx.box(
                    leyenda_condiciones(),
                    width="30%",
                    padding_left="4"
                ),
                
                spacing="4",
                width="100%",
                align_items="start"
            ),
            
            spacing="4",
            width="100%"
        ),
        style=ODONTOGRAMA_CONTAINER_STYLE
    )