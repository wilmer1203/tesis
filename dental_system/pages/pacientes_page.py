"""
👥 PÁGINA DE GESTIÓN DE PACIENTES - VERSIÓN REFACTORIZADA
========================================================

✨ Sistema moderno de gestión de pacientes:
- Header elegante con búsqueda integrada
- Cards de estadísticas con glassmorphism effect
- Modales de formulario optimizados con mejor UX
- Sistema de filtros avanzado y responsive
- Tabla moderna con acciones contextuales
- Diseño mobile-first con animaciones suaves

Desarrollado para Reflex.dev con patrones modernos
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.table_components import patients_table
from dental_system.components.modal_paciente import multi_step_patient_form
from dental_system.styles.themes import (
    COLORS, 
    SHADOWS, 
    RADIUS, 
    SPACING, 
    ANIMATIONS, 
    GRADIENTS,
    GLASS_EFFECTS,
    DARK_THEME,
    dark_page_background,
    dark_crystal_card,
    dark_table_container,
    dark_header_style
)

# ==========================================
# 🎨 COMPONENTES MODERNOS PARA PACIENTES
# ==========================================

def clean_patients_header() -> rx.Component:
    """🎯 Header limpio y elegante para pacientes (patrón Personal)"""
    return rx.box(
        rx.vstack(
            # Título principal alineado a la izquierda
            rx.heading(
                "Gestión de Pacientes",
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
                "Administra el registro completo de pacientes con historial médico digital",
                style={
                    "font_size": "1.125rem",
                    "color": DARK_THEME["colors"]["text_secondary"],
                    "line_height": "1.5",
                    "opacity": "0.8"
                }
            ),
            
            spacing="1",
            align="start",
            width="100%"
        ),
        # Utilizar función utilitaria para header
        style=dark_header_style(),
        width="100%"
    )

def minimal_patients_stat_card(
    title: str,
    value: str, 
    icon: str,
    color: str,
    subtitle: str = ""
) -> rx.Component:
    """🎯 Card de estadística minimalista para pacientes (patrón Personal)"""
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
                
                rx.spacer(),
                
                # Número grande a la derecha
                rx.text(
                    value,
                    style={
                        "font_size": "2.5rem",
                        "font_weight": "800",
                        "color": color,
                        "line_height": "1"
                    }
                ),
                
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
                    "margin_top": SPACING["1"]
                }
            ),
            
            spacing="3",
            align="stretch",
            width="100%",
            padding=SPACING["3"]
        ),
        
        # Utilizar función utilitaria de cristal reutilizable
        style=dark_crystal_card(color=color, hover_lift="6px"),
        width="100%"
    )

def patients_stats() -> rx.Component:
    """📈 Grid de estadísticas minimalistas y elegantes para pacientes"""
    return rx.grid(
        minimal_patients_stat_card(
            title="Total Pacientes",
            value=AppState.lista_pacientes.length().to_string(),
            icon="users",
            color=COLORS["primary"]["600"],
            subtitle="Registrados en el sistema"
        ),
        minimal_patients_stat_card(
            title="Pacientes Activos",
            value=AppState.total_pacientes_activos.to_string(),
            icon="user-check",
            color=COLORS["success"]["600"],
            subtitle="Con estado activo"
        ),
        minimal_patients_stat_card(
            title="Nuevos Este Mes",
            value="47",  # Podrías conectar con AppState
            icon="user-plus",
            color=COLORS["secondary"]["600"],
            subtitle="Registros recientes"
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="3"),
        spacing="6",
        width="100%",
        margin_bottom="8"
    )


def delete_paciente_confirmation_modal() -> rx.Component:
    """❌ Modal de confirmación moderno con mejor UX para pacientes"""
    return rx.dialog.root(
        rx.dialog.content(
            # Header con icono de advertencia
            rx.vstack(
                rx.box(
                    rx.icon("triangle_alert", size=48, color=COLORS["error"]["500"]),
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
                    "¿Estás seguro de que deseas eliminar este paciente?",
                    size="3",
                    color=COLORS["gray"]["600"],
                    text_align="center",
                    line_height="1.5"
                ),
                rx.text(
                    "Esta acción desactivará al paciente pero conservará su historial médico completo.",
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
                    on_click=AppState.cerrar_todos_los_modales,
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
                    "Eliminar Paciente",
                    on_click=AppState.ejecutar_eliminar_paciente,
                    loading=AppState.cargando_pacientes,
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
        on_open_change=AppState.cerrar_todos_los_modales
    )
      
# ==========================================
# 📋 PÁGINA PRINCIPAL - USANDO COMPONENTES GENÉRICOS
# ==========================================

def modern_alerts() -> rx.Component:
    """🚨 Sistema de alertas moderno para pacientes"""
    return rx.vstack(
        # Alerta de éxito
        rx.cond(
            AppState.mensaje_modal_confirmacion != "",
            rx.box(
                rx.hstack(
                    rx.icon("check", size=20, color=COLORS["success"]["500"]),
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
                    rx.icon("circle_alert", size=20, color=COLORS["error"]["500"]),
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

def pacientes_page() -> rx.Component:
    """
    👥 PÁGINA DE GESTIÓN DE PACIENTES - REFACTORIZADA CON TEMA ELEGANTE
    
    ✨ Características actualizadas:
    - Diseño moderno con glassmorphism siguiendo patrón Personal
    - Header limpio y elegante
    - Cards de estadísticas minimalistas
    - Búsqueda y controles simplificados
    - Tema oscuro con efectos cristal
    - Animaciones suaves y micro-interacciones
    """
    return rx.box(
        rx.box(
            rx.vstack(
                # Header limpio y elegante
                clean_patients_header(),
                # Sistema de alertas mejorado
                modern_alerts(),
                    
                # Estadísticas con cards modernos
                patients_stats(),
                    
                # Tabla de pacientes con diseño actualizado - Usar función utilitaria
                rx.box(
                    patients_table(),
                    style=dark_table_container(),
                    width="100%"
                ),
                spacing="3",
                width="100%"
            ),
            style={
                "position": "relative",
                "z_index": "10"
            }
        ),
        multi_step_patient_form(),  # ✅ Formulario multi-step reactivado
        style={
            **dark_page_background(),
            "padding": f"{SPACING['4']} {SPACING['6']}",
            "min_height": "100vh"
        },   
        width="100%"
    )
