# 📚 COMPONENTE: BOTÓN HISTORIAL FLOTANTE
# dental_system/components/odontologia/floating_history_button.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS DEL BOTÓN FLOTANTE
# ==========================================

FLOATING_BUTTON_STYLE = {
    "position": "fixed",
    "bottom": "30px",
    "right": "30px",
    "z_index": "999",
    "width": "60px",
    "height": "60px",
    "border_radius": "50%",
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.3), 0 2px 6px rgba(0, 0, 0, 0.2)",
    "border": f"2px solid rgba(255, 255, 255, 0.1)",
    "cursor": "pointer",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "transition": "all 0.3s ease",
    "_hover": {
        "transform": "translateY(-3px) scale(1.05)",
        "box_shadow": "0 12px 35px rgba(0, 0, 0, 0.4), 0 4px 8px rgba(0, 0, 0, 0.3)"
    },
    "_active": {
        "transform": "translateY(-1px) scale(0.98)"
    }
}

TOOLTIP_STYLE = {
    "position": "absolute",
    "bottom": "70px",
    "right": "0px",
    "background": "rgba(0, 0, 0, 0.8)",
    "color": "white",
    "padding": "8px 12px",
    "border_radius": "8px",
    "font_size": "12px",
    "white_space": "nowrap",
    "opacity": "0",
    "visibility": "hidden",
    "transition": "all 0.2s ease",
    "_parent_hover": {
        "opacity": "1",
        "visibility": "visible"
    }
}

MODAL_OVERLAY_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "width": "100vw",
    "height": "100vh",
    "background": "rgba(0, 0, 0, 0.6)",
    "backdrop_filter": "blur(5px)",
    "z_index": "1000",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center"
}

MODAL_CONTENT_STYLE = {
    "background": "white",
    "border_radius": RADIUS["2xl"],
    "width": "90%",
    "max_width": "600px",
    "max_height": "80%",
    "overflow": "hidden",
    "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.3)",
    "animation": "slideInUp 0.3s ease-out"
}

# ==========================================
# 🧩 COMPONENTES INTERNOS
# ==========================================

def notification_badge() -> rx.Component:
    """🔔 Badge de notificación con número de items"""
    return rx.cond(
        AppState.total_historial_items > 0,
        rx.box(
            rx.text(
                rx.cond(
                    AppState.total_historial_items > 9,
                    "9+",
                    AppState.total_historial_items
                ),
                color="white",
                font_size="10px",
                font_weight="bold"
            ),
            style={
                "position": "absolute",
                "top": "-5px",
                "right": "-5px",
                "background": COLORS["error"]["500"],
                "border_radius": "50%",
                "width": "20px",
                "height": "20px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "border": "2px solid white"
            }
        )
    )

def history_modal_header() -> rx.Component:
    """📚 Header del modal de historial"""
    return rx.hstack(
        rx.hstack(
            rx.icon("history", size=24, color=COLORS["primary"]["600"]),
            rx.vstack(
                rx.text("📚 Historial Clínico", font_size="20px", font_weight="bold"),
                rx.text(f"Paciente: {AppState.paciente_actual.nombre_completo}", 
                       font_size="14px", color=DARK_THEME["colors"]["text_secondary"]),
                spacing="1", align_items="start"
            ),
            spacing="3", align_items="center"
        ),
        
        rx.spacer(),
        
        rx.button(
            rx.icon("x", size=18),
            size="3",
            variant="ghost",
            color_scheme="gray",
            on_click=AppState.cerrar_modal_historial_completo
        ),
        
        width="100%",
        align_items="center",
        padding="6",
        border_bottom=f"1px solid {COLORS['gray']['200']}"
    )

def history_modal_content() -> rx.Component:
    """📋 Contenido del modal de historial - Versión simplificada temporal"""
    # NOTA: panel_historial fue archivado, implementando versión básica

    return rx.box(
        rx.vstack(
            # Mensaje temporal mientras se implementa el historial completo
            rx.center(
                rx.vstack(
                    rx.icon("history", size=40, color=COLORS["gray"]["400"]),
                    rx.text(
                        "Historial del Paciente",
                        font_size="18px",
                        font_weight="600",
                        color=COLORS["gray"]["700"]
                    ),
                    rx.text(
                        "La funcionalidad completa de historial está en desarrollo",
                        font_size="14px",
                        color=COLORS["gray"]["500"],
                        text_align="center"
                    ),
                    spacing="3",
                    align_items="center"
                ),
                padding="8"
            ),

            rx.divider(),

            # Historial de consultas - TEMPORAL: Funcionalidad simplificada
            rx.box(
                rx.text(
                    "📋 Historial de Consultas",
                    font_size="16px",
                    font_weight="600",
                    color=COLORS["gray"]["700"],
                    margin_bottom="3"
                ),
                rx.text(
                    "Las consultas previas aparecerán aquí próximamente",
                    font_size="14px",
                    color=COLORS["gray"]["500"]
                ),
                padding="4"
            ),

            rx.divider(),

            # Notas rápidas - TEMPORAL: Funcionalidad simplificada
            rx.box(
                rx.text(
                    "📝 Notas Clínicas",
                    font_size="16px",
                    font_weight="600",
                    color=COLORS["gray"]["700"],
                    margin_bottom="3"
                ),
                rx.text(
                    "Las notas del historial clínico estarán disponibles próximamente",
                    font_size="14px",
                    color=COLORS["gray"]["500"]
                ),
                padding="4"
            ),
            
            spacing="6",
            width="100%",
            align_items="start"
        ),
        style={
            "padding": SPACING["6"],
            "max_height": "60vh",
            "overflow_y": "auto"
        }
    )

def history_modal() -> rx.Component:
    """📚 Modal completo de historial"""
    return rx.cond(
        AppState.modal_historial_completo_abierto,
        rx.box(
            rx.box(
                rx.vstack(
                    history_modal_header(),
                    history_modal_content(),
                    spacing="0",
                    width="100%"
                ),
                style=MODAL_CONTENT_STYLE,
                # Evitar cerrar al hacer click dentro - Manejado por el overlay
            ),
            style=MODAL_OVERLAY_STYLE,
            on_click=AppState.cerrar_modal_historial_completo  # Cerrar al hacer click fuera
        )
    )

# ==========================================
# 📋 COMPONENTE PRINCIPAL
# ==========================================

def floating_history_button() -> rx.Component:
    """
    📚 Botón flotante para acceder al historial completo del paciente
    
    Aparece en la esquina inferior derecha solo cuando hay datos de historial.
    Al hacer click, abre un modal completo con todo el historial del paciente.
    """
    return rx.fragment(
        # Botón flotante principal
        rx.cond(
            AppState.tiene_historial_disponible,
            rx.box(
                # Contenido del botón
                rx.icon("history", size=24, color="white"),
                
                # Badge de notificación
                notification_badge(),
                
                # Tooltip
                rx.box(
                    "Ver historial completo",
                    style=TOOLTIP_STYLE
                ),
                
                style=FLOATING_BUTTON_STYLE,
                on_click=AppState.abrir_modal_historial_completo
            )
        ),
        
        # Modal de historial
        history_modal()
    )

# ==========================================
# 🧪 UTILIDADES Y HELPERS
# ==========================================

# CSS Animation para el modal
MODAL_ANIMATION_CSS = """
@keyframes slideInUp {
  0% {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
"""