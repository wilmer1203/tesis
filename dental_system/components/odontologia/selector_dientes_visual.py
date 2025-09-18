"""
🦷 SELECTOR VISUAL DE DIENTES PARA INTERVENCIONES
==================================================

Componente para seleccionar dientes de forma visual en el tab de intervención.
Integra con el formulario existente usando los métodos ya disponibles en AppState.

DISEÑO:
- Grid de 32 dientes FDI estándar
- Click para seleccionar/deseleccionar
- Colores dinámicos (seleccionado/no seleccionado)
- Integración con formulario_intervencion.dientes_afectados existente
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS PARA EL SELECTOR DE DIENTES
# ==========================================

SELECTOR_DIENTES_STYLES = {
    "container": {
        "background": DARK_THEME["colors"]["surface_secondary"],
        "border": f"1px solid {DARK_THEME['colors']['border']}",
        "border_radius": RADIUS["xl"],
        "padding": SPACING["6"],
        "margin_bottom": SPACING["4"]
    },
    "diente_normal": {
        "width": "55px",          # Aumentar tamaño
        "height": "55px",
        "background": "#2D3748",  # Gris oscuro con buen contraste
        "border": "2px solid #4A5568",
        "border_radius": RADIUS["md"],
        "cursor": "pointer",
        "transition": "all 0.3s ease",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "position": "relative"
    },
    "diente_seleccionado": {
        "width": "55px",          # Mismo tamaño base
        "height": "55px",
        "background": COLORS["primary"]["500"],  # Azul vibrante
        "border": f"3px solid {COLORS['primary']['300']}",  # Borde más grueso
        "border_radius": RADIUS["md"],
        "cursor": "pointer",
        "transition": "all 0.3s ease",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "transform": "scale(1.05)",  # Menos exagerado
        "position": "relative"
    }
}

# ==========================================
# 🦷 COMPONENTE DE DIENTE INDIVIDUAL
# ==========================================

def diente_selector_visual(numero_fdi: int) -> rx.Component:
    """🦷 Diente individual clickeable para selección"""
    
    # Determinar si el diente está seleccionado
    dientes_str = AppState.formulario_intervencion.dientes_afectados
    
    return rx.box(
        rx.text(
            numero_fdi,
            size="3",  # Más grande que "sm"
            weight="bold",
            color=rx.cond(
                dientes_str.contains(str(numero_fdi)),
                "#FFFFFF",  # Blanco puro para seleccionado
                "#E2E8F0"   # Gris claro para no seleccionado
            ),
            style={
                "z_index": "10",
                "user_select": "none",  # Evitar selección de texto
                "pointer_events": "none"  # El click pasa al contenedor
            }
        ),

        # Estilos dinámicos según selección
        style=rx.cond(
            dientes_str.contains(str(numero_fdi)),
            {
                **SELECTOR_DIENTES_STYLES["diente_seleccionado"],
                "box_shadow": f"0 4px 15px rgba({COLORS['primary']['500']}, 0.4)"  # Sombra más visible
            },
            {
                **SELECTOR_DIENTES_STYLES["diente_normal"],
                "box_shadow": "0 2px 8px rgba(0,0,0,0.1)"
            }
        ),

        # Efectos hover mejorados
        _hover={
            "transform": "scale(1.08)",
            "border_color": COLORS["primary"]["400"],
            "box_shadow": f"0 6px 20px rgba({COLORS['primary']['500']}, 0.3)"
        },

        # Click para seleccionar/deseleccionar
        on_click=rx.cond(
            dientes_str.contains(str(numero_fdi)),
            AppState.quitar_diente_afectado(numero_fdi),
            AppState.agregar_diente_afectado(numero_fdi)
        )
    )

# ==========================================
# 🏗️ GRID COMPLETO DE DIENTES FDI
# ==========================================

def grid_dientes_fdi() -> rx.Component:
    """🏗️ Grid de 32 dientes FDI para selección"""
    
    return rx.vstack(
        # Cuadrante Superior (21-28 + 11-18)
        rx.hstack(
            # Superior Izquierdo (21-28)
            rx.foreach(
                [28, 27, 26, 25, 24, 23, 22, 21],
                lambda fdi: diente_selector_visual(fdi)
            ),
            # Separador
            rx.divider(orientation="vertical", size="4"),
            # Superior Derecho (11-18)
            rx.foreach(
                [11, 12, 13, 14, 15, 16, 17, 18],
                lambda fdi: diente_selector_visual(fdi)
            ),
            spacing="2",
            justify="center",
            align="center"
        ),
        
        # Separador horizontal
        rx.divider(size="4", color_scheme="gray"),
        
        # Cuadrante Inferior (31-38 + 41-48)
        rx.hstack(
            # Inferior Izquierdo (31-38)
            rx.foreach(
                [38, 37, 36, 35, 34, 33, 32, 31],
                lambda fdi: diente_selector_visual(fdi)
            ),
            # Separador
            rx.divider(orientation="vertical", size="4"),
            # Inferior Derecho (41-48)
            rx.foreach(
                [41, 42, 43, 44, 45, 46, 47, 48],
                lambda fdi: diente_selector_visual(fdi)
            ),
            spacing="2",
            justify="center",
            align="center"
        ),
        
        spacing="4",
        align="center"
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL EXPORTADO
# ==========================================

def selector_dientes_visual() -> rx.Component:
    """🦷 Selector visual de dientes para tab de intervención"""
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.icon("activity", size=24, color=COLORS["primary"]["500"]),
                rx.vstack(
                    rx.text(
                        "🦷 Seleccionar Dientes Afectados",
                        size="4",
                        font_weight="bold",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    rx.text(
                        "Click en los dientes para seleccionar/deseleccionar",
                        size="2",
                        color=DARK_THEME["colors"]["text_secondary"]
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.spacer(),
                
                # Contador de dientes seleccionados
                rx.badge(
                    rx.cond(
                        AppState.formulario_intervencion.dientes_afectados == "",
                        "0 dientes",
                        f"{AppState.total_dientes_seleccionados} diente(s)"
                    ),
                    color_scheme="blue",
                    size="2"
                ),
                
                spacing="4",
                align="center",
                width="100%"
            ),

            # Botones de control rápido
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("check-square", size=16),
                        rx.text("🦷 Toda la Boca"),
                        spacing="2"
                    ),
                    on_click=AppState.seleccionar_todos_los_dientes,
                    variant="outline",
                    color_scheme="green",
                    size="2"
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("x-square", size=16),
                        rx.text("🔄 Limpiar"),
                        spacing="2"
                    ),
                    on_click=AppState.limpiar_seleccion_dientes,
                    variant="outline",
                    color_scheme="red",
                    size="2"
                ),
                rx.spacer(),
                rx.text(
                    "💡 Para servicios generales usa 'Toda la Boca'",
                    size="1",
                    color=COLORS["primary"]["400"],
                    style={"fontStyle": "italic"}
                ),
                spacing="3",
                align="center",
                width="100%",
                margin_bottom="4"
            ),

            # Grid de dientes
            grid_dientes_fdi(),
            
            # Información adicional
            rx.cond(
                AppState.formulario_intervencion.dientes_afectados != "",
                rx.hstack(
                    rx.text(
                        "Dientes seleccionados:",
                        size="2",
                        color=DARK_THEME["colors"]["text_secondary"]
                    ),
                    rx.text(
                        AppState.formulario_intervencion.dientes_afectados,
                        size="2",
                        font_weight="bold",
                        color=COLORS["primary"]["500"]
                    ),
                    rx.button(
                        "Limpiar selección",
                        size="1",
                        variant="soft",
                        color_scheme="red",
                        on_click=AppState.limpiar_seleccion_dientes
                    ),
                    spacing="3",
                    align="center"
                )
            ),
            
            spacing="4",
            width="100%"
        ),
        
        style=SELECTOR_DIENTES_STYLES["container"]
    )