"""
🏥 PÁGINA DE GESTIÓN DE PERSONAL - VERSIÓN REFACTORIZADA
=======================================================

✨ Diseño moderno y elegante con:
- UI cards con glassmorphism effect
- Animaciones suaves y micro-interacciones 
- Diseño responsive mobile-first
- Modales optimizados con mejor UX
- Componentes reutilizables y escalables
- Tema oscuro/claro compatible

Desarrollado para Reflex.dev con patrones modernos
"""

import reflex as rx
from dental_system.components.common import (
    medical_page_layout,
    medical_toast_container,
    toast_animations_css
)
from dental_system.components.table_components import personal_table
from dental_system.components.forms import multi_step_staff_form
from dental_system.state.app_state import AppState
from dental_system.styles.themes import (
    COLORS, 
    SHADOWS, 
    RADIUS, 
    SPACING, 
    ANIMATIONS, 
    GRADIENTS,
    GLASS_EFFECTS,
    DARK_THEME,
    dark_crystal_card,
    dark_table_container,
    dark_header_style
)

# ==========================================
# 🎨 COMPONENTES MODERNOS Y ELEGANTES  
# ==========================================

def delete_personal_confirmation_modal() -> rx.Component:
    """❌ Modal de confirmación moderno con mejor UX"""
    return rx.dialog.root(
        rx.dialog.content(
            # Header con icono de advertencia
            rx.vstack(
                rx.box(
                    rx.icon("triangle-alert", size=48, color=COLORS["error"]["500"]),
                    padding=SPACING["4"],
                    border_radius=RADIUS["full"],
                    background=COLORS["error"]["50"]
                ),
                rx.heading(
                    "Confirmar Eliminación",
                    size="5",
                    color=COLORS["gray"]["800"],
                    text_align="center"
                ),
                rx.text(
                    "¿Estás seguro de que deseas eliminar este miembro del personal?",
                    size="3",
                    color=COLORS["gray"]["600"],
                    text_align="center",
                    line_height="1.5"
                ),
                rx.text(
                    "Esta acción desactivará al empleado pero conservará su historial completo en el sistema.",
                    size="2",
                    color=COLORS["gray"]["500"],
                    text_align="center",
                    line_height="1.4"
                ),
                spacing="4",
                align="center",
                margin_bottom="6"
            ),
            
            # Botones de acción con mejor espaciado
            rx.hstack(
                rx.button(
                    "Cancelar",
                    on_click=AppState.cerrar_modal,
                    style={
                        **GLASS_EFFECTS["light"],
                        "border": f"1px solid {COLORS['gray']['300']}60",
                        "color": COLORS["gray"]["700"],
                        "border_radius": RADIUS["2xl"],
                        "padding": f"{SPACING['3']} {SPACING['6']}",
                        "font_weight": "600",
                        "transition": ANIMATIONS["presets"]["crystal_hover"],
                        "_hover": {
                            **GLASS_EFFECTS["medium"],
                            "transform": "translateY(-2px)",
                            "box_shadow": SHADOWS["crystal_sm"]
                        }
                    },
                    width="100%"
                ),
                rx.button(
                    "Eliminar Personal",
                    on_click=AppState.eliminar_personal,
                    loading=AppState.cargando_operacion_personal,
                    style={
                        "background": GRADIENTS["neon_primary"].replace(COLORS["primary"]["500"], COLORS["error"]["500"]).replace(COLORS["blue"]["600"], COLORS["error"]["600"]),
                        "color": "white",
                        "border": "none",
                        "border_radius": RADIUS["2xl"],
                        "padding": f"{SPACING['3']} {SPACING['6']}",
                        "font_weight": "700",
                        "box_shadow": SHADOWS["glow_primary"].replace(COLORS["primary"]["500"], COLORS["error"]["500"]),
                        "transition": ANIMATIONS["presets"]["crystal_hover"],
                        "_hover": {
                            "transform": "translateY(-2px) scale(1.02)",
                            "box_shadow": f"0 0 30px {COLORS['error']['500']}50, 0 8px 16px {COLORS['error']['500']}30"
                        }
                    },
                    width="100%"
                ),
                spacing="3",
                width="100%"
            ),
            
            style={
                "max_width": "480px",
                "padding": SPACING["8"],
                "border_radius": RADIUS["3xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["crystal_xl"],
                "border": f"1px solid {COLORS['error']['200']}40",
                "position": "relative",
                "_before": {
                    "content": "''",
                    "position": "absolute",
                    "inset": "-1px",
                    "background": f"linear-gradient(135deg, {COLORS['error']['100']}60 0%, {COLORS['error']['200']}60 50%, {COLORS['error']['100']}60 100%)",
                    "border_radius": RADIUS["3xl"],
                    "z_index": "-1",
                    "opacity": "0.7"
                }
            }
        ),
        open=AppState.modal_confirmacion_abierto,
        on_open_change=AppState.cerrar_modal
    )


# ==========================================
# ESTADÍSTICAS DE PERSONAL
# ==========================================

def minimal_stat_card(
    title: str,
    value: str, 
    icon: str,
    color: str,
    subtitle: str = ""
) -> rx.Component:
    """🎯 Card de estadística minimalista: Icono izq + Número der + Título abajo"""
    return rx.box(
        rx.vstack(
            # Layout superior: Icono a la izquierda, Número a la derecha
            rx.hstack(
                # Icono pequeño a la izquierda
                rx.box(
                    rx.icon(icon, size=24, color=color),
                    style={
                        "width": "50px",
                        "height": "50px",
                        "background": f"{color}100",
                        "border_radius": RADIUS["xl"],
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "border": f"1px solid {color}35"
                    }
                ),
                
                # Número grande a la derecha
                rx.text(
                    value,
                    style={
                        "font_size": "1.5rem",
                        "font_weight": "800",
                        "color": color,
                        "line_height": "1"
                    }
                ),
                justify="center",
                align="center",
                width="100%"
            ),
            
            # Título descriptivo abajo
            rx.text(
                title,
                style={
                    "font_size": "1rem",
                    "font_weight": "600",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "text_align": "center",
                }
            ),
            spacing="1",
            align="center",
            width="100%",
            padding=SPACING["3"]
        ),
        
        # Utilizar función utilitaria de cristal reutilizable
        style=dark_crystal_card(color=color, hover_lift="6px"),
        width="100%"
    )

def personal_stats() -> rx.Component:
    """📊 Grid de estadísticas minimalistas y elegantes"""
    return rx.grid(
        minimal_stat_card(
            title="Total Personal",
            value=AppState.estadisticas_personal.total.to_string(),
            icon="users",
            color=COLORS["secondary"]["600"],
            subtitle="Empleados trabajando"
        ),
        minimal_stat_card(
            title="Odontólogos",
            value=AppState.estadisticas_personal.odontologos.to_string(),
            icon="stethoscope",
            color=COLORS["secondary"]["600"],
            subtitle="Profesionales titulados"
        ),
        minimal_stat_card(
            title="Administrativos",
            value=(AppState.estadisticas_personal.administradores + 
                   AppState.estadisticas_personal.asistentes + 
                   AppState.estadisticas_personal.gerentes).to_string(),
            icon="briefcase",
            color=COLORS["secondary"]["600"],
            subtitle="Staff de apoyo"
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="3"),
        spacing="4",
        width="100%",
        margin_bottom="6"
    )

# ==========================================
# PÁGINA PRINCIPAL - ACTUALIZADA
# ==========================================

def clean_page_header() -> rx.Component:
    """🎯 Header limpio y elegante alineado a la izquierda"""
    return rx.box(
        rx.hstack(
            rx.vstack(
            # Título principal alineado a la izquierda
                rx.heading(
                    "Gestión de Personal",
                    style={
                        "font_size": "2.75rem",
                        "font_weight": "800",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent",
                        "line_height": "1.2",
                        "text_align": "left"
                    }
                ),
                
                # Subtítulo elegante
                rx.text(
                    "Administra empleados, roles y permisos del sistema",
                    style={
                        "font_size": "1.125rem",
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "line_height": "1.5"
                    }
                ),
                
                spacing="1",
                justify="start",
                # align="center",
                width="100%",
                
            ),
            personal_stats()
        ),
        
        # Utilizar función utilitaria para header
        style=dark_header_style(),
        width="100%"
    )

def modern_alerts() -> rx.Component:
    """🚨 Sistema de alertas moderno"""
    return rx.vstack(
        # Alerta de éxito
        rx.cond(
            AppState.mensaje_modal_confirmacion != "",
            rx.box(
                rx.hstack(
                    rx.icon("circle-check", size=20, color=COLORS["success"]["500"]),
                    rx.text(
                        AppState.mensaje_modal_confirmacion,
                        color=COLORS["success"]["700"],
                        font_weight="500"
                    ),
                    spacing="3",
                    align="center"
                ),
                style={
                    "background": COLORS["success"]["50"],
                    "border": f"1px solid {COLORS['success']['200']}",
                    "border_left": f"4px solid {COLORS['success']['500']}",
                    "border_radius": RADIUS["lg"],
                    "padding": f"{SPACING['4']} {SPACING['5']}",
                    "margin_bottom": SPACING["4"]
                }
            ),
            rx.box()
        ),
        # Alerta de error
        rx.cond(
            AppState.mensaje_modal_alerta != "",
            rx.box(
                rx.hstack(
                    rx.icon("circle-alert", size=20, color=COLORS["error"]["500"]),
                    rx.text(
                        AppState.mensaje_modal_alerta,
                        color=COLORS["error"]["700"],
                        font_weight="500"
                    ),
                    spacing="3",
                    align="center"
                ),
                style={
                    "background": COLORS["error"]["50"],
                    "border": f"1px solid {COLORS['error']['200']}",
                    "border_left": f"4px solid {COLORS['error']['500']}",
                    "border_radius": RADIUS["lg"],
                    "padding": f"{SPACING['4']} {SPACING['5']}",
                    "margin_bottom": SPACING["4"]
                }
            ),
            rx.box()
        ),
        width="100%",
        spacing="0"
    )

def personal_page() -> rx.Component:
    """
    🏥 PÁGINA DE GESTIÓN DE PERSONAL - REFACTORIZADA CON TOASTS
    
    ✨ Características mejoradas:
    - Diseño moderno con glassmorphism
    - Animaciones suaves y micro-interacciones
    - Layout responsive mobile-first 
    - Cards de estadísticas elegantes
    - Header con gradientes y efectos
    - Sistema de toasts flotantes
    """
    return rx.fragment(
        # CSS para animaciones de toasts
        toast_animations_css(),
        
        # Contenedor de toasts flotantes
        medical_toast_container(),
        
        # Layout principal usando el wrapper
        medical_page_layout(
            rx.vstack(
                # Header limpio y elegante
                clean_page_header(),
                
                # Sistema de alertas mejorado (mantener por compatibilidad)
                modern_alerts(), 
                
                # Tabla de personal con diseño actualizado
                rx.box(
                    personal_table(),
                    style=dark_table_container(),
                    width="100%"
                ),
                
                spacing="3",
                width="100%"
            )
        ),
        
        # Modales
        multi_step_staff_form(),
        # delete_personal_confirmation_modal()  # TODO: Arreglar modal
    )