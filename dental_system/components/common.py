import reflex as rx
from typing import List, Dict, Optional
from ..state.app_state import AppState
from dental_system.styles.themes import (
    COLORS, SHADOWS, ROLE_THEMES, RADIUS, GRADIENTS, ANIMATIONS, SPACING, dark_page_background
)

# ==========================================
# COMPONENTES DE BOTONES
# ==========================================


def primary_button(
    text: str,
    icon: Optional[str] = None,
    on_click = None,
    loading: bool = False,
    size: str = "md"
) -> rx.Component:
    """Botón primario con estilo del sistema"""
    return rx.button(
        rx.cond(
            loading,
            rx.hstack(
                rx.spinner(size="2", color="white"),
                rx.text("Cargando...", color="white", size="3"),
                spacing="2",
                align="center"
            ),
            rx.hstack(
                *([rx.icon(icon, size=16)] if icon is not None else []),
                rx.text(text, size="3"),
                spacing="2",
                align="center"
            )
        ),
        style={
            "background": GRADIENTS["neon_primary"],
            "color": "white",
            "border": "none",
            "border_radius": RADIUS["2xl"],
            "padding": "14px 24px" if size == "md" else "10px 20px",
            "font_weight": "700",
            "font_size": "15px" if size == "md" else "13px",
            "cursor": "pointer",
            "transition": ANIMATIONS["presets"]["crystal_hover"],
            "position": "relative",
            "_hover": {
                "transform": "translateY(-3px) scale(1.02)",
                "box_shadow": SHADOWS["crystal_lg"],
                "_before": {
                    "content": "''",
                    "position": "absolute",
                    "inset": "-2px",
                    "border_radius": RADIUS["2xl"],
                    "z_index": "-1",
                    "opacity": "0.8"
                }
            },
            "_active": {"transform": "translateY(-1px) scale(1.01)"},
        },
        on_click=on_click,
        disabled=loading
    )

def secondary_button(
    text: str,
    icon: Optional[str] = None,
    on_click = None,
    variant: str = "outline",
    loading: bool = False
) -> rx.Component:
    """Botón secundario"""
    return rx.button(
        rx.cond(
            loading,
            rx.hstack(
                rx.spinner(size="2", color=COLORS["gray"]["600"]),
                rx.text("Cargando...", color=COLORS["gray"]["600"], size="3"),
                spacing="2",
                align="center"
            ),
            rx.hstack(
                *([rx.icon(icon, size=16)] if icon is not None else []),
                rx.text(text, size="3"),
                spacing="2",
                align="center"
            )
        ),
        background="transparent" if variant == "outline" else COLORS["gray"]["100"],
        color=COLORS["gray"]["600"],
        border=f"1px solid {COLORS['gray']['300']}" if variant == "outline" else "none",
        border_radius="8px",
        padding="12px 20px",
        font_weight="500",
        font_size="14px",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background": COLORS["gray"]["50"] if variant == "outline" else COLORS["gray"]["200"],
            "border_color": COLORS["gray"]["400"] if variant == "outline" else "none"
        },
        on_click=on_click,
        disabled=loading
    )


def eliminar_button(
    text: str,
    icon: Optional[str] = None,
    on_click = None,
    loading: bool = False,
    size: str = "md"
) -> rx.Component:
    """Botón primario con estilo del sistema"""
    return rx.button(
        rx.cond(
            loading,
            rx.hstack(
                rx.spinner(size="2", color="white"),
                rx.text("Cargando...", color="white", size="3"),
                spacing="2",
                align="center"
            ),
            rx.hstack(
                *([rx.icon(icon, size=16)] if icon is not None else []),
                rx.text(text, size="3"),
                spacing="2",
                align="center"
            )
        ),
        background=COLORS["error"]["500"],
        color="white",
        border="none",
        border_radius="8px",
        padding="12px 20px" if size == "md" else "8px 16px",
        font_weight="600",
        font_size="14px" if size == "md" else "12px",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "transform": "translateY(-1px)",
            "box_shadow": SHADOWS["lg"]
        },
        _active={"transform": "translateY(0)"},
        on_click=on_click,
        disabled=loading
    )

# ==========================================
# COMPONENTES DE FORMULARIOS
# ==========================================

def form_field(
    label: str,
    field_name: str,
    value: str,
    on_change,
    field_type: str = "text",
    options: Optional[List[str]] = None,
    required: bool = False,
    placeholder: str = ""
) -> rx.Component:
    """Campo de formulario reutilizable"""
    return rx.vstack(
        rx.text(
            label + ("*" if required else ""),
            size="3",
            weight="medium",
            color=COLORS["gray"]["700"]
        ),
        rx.cond(
            field_type == "select",
            rx.select.root(
                rx.select.trigger(
                    placeholder=placeholder or f"Seleccionar {label.lower()}",
                    width="100%"
                ),
                rx.select.content(
                    rx.foreach(
                        options or [],
                        lambda option: rx.select.item(option, value=option)
                    )
                ),
                value=value,
                on_change=lambda val: on_change(field_name, val),
                width="100%"
            ),
            rx.cond(
                field_type == "textarea",
                rx.text_area(
                    value=value,
                    on_change=lambda val: on_change(field_name, val),
                    placeholder=placeholder,
                    width="100%",
                    min_height="80px"
                ),
                rx.input(
                    value=value,
                    on_change=lambda val: on_change(field_name, val),
                    placeholder=placeholder,
                    type=field_type,
                    width="100%"
                )
            )
        ),
        spacing="1",
        align_items="start",
        width="100%"
    )

# ==========================================
# COMPONENTES DE ALERTAS
# ==========================================

def success_alert(message: str) -> rx.Component:
    """Alerta de éxito"""
    return rx.cond(
        message != "",
        rx.box(
            rx.hstack(
                rx.icon("check", size=20, color=COLORS["success"]),
                rx.text(message, color="#1B5E20", size="3"),
                spacing="2",
                align="center"
            ),
            padding="12px 16px",
            background="#E8F5E8",
            border=f"1px solid {COLORS['success']}",
            border_radius="8px",
            margin_bottom="16px"
        ),
        rx.box()
    )

def error_alert(message: str) -> rx.Component:
    """Alerta de error"""
    return rx.cond(
        message != "",
        rx.box(
            rx.hstack(
                rx.icon("triangle-alert", size=20, color=COLORS["error"]),
                rx.text(message, color="#C62828", size="3"),
                spacing="2",
                align="center"
            ),
            padding="12px 16px",
            background="#FFEBEE",
            border=f"1px solid {COLORS['error']}",
            border_radius="8px",
            margin_bottom="16px"
        ),
        rx.box()
    )







# ==========================================
# COMPONENTES DE ESTADÍSTICAS
# ==========================================


def stat_card(
    title: str, 
    value: str, 
    icon: str, 
    color: str = "",
    trend: Optional[str] = None,
    trend_value: Optional[str] = None
) -> rx.Component:
    """Tarjeta de estadística con trend opcional"""
    final_color = color if color else COLORS["primary"]["500"]
    trend_var = rx.Var.create(trend_value)
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon, size=30, color="white"),
                    padding="12px",
                    border_radius="16px",
                    background=final_color
                ),
                rx.spacer(),
                rx.cond(
                    trend is not None,
                    rx.hstack(
                        rx.icon(
                            rx.cond(trend == "up", "trending-up", "trending-down"),
                            size=16,
                            color=rx.cond(trend == "up", COLORS["success"], COLORS["error"])
                        ),
                        
                        rx.text(
                            rx.cond(
                                trend_var.is_none(),
                                "0%",
                                trend_var,
                            ),
                            size="2",
                            color=rx.cond(trend == "up", COLORS["success"], COLORS["error"]),
                            weight="medium"
                        ),
                        spacing="1",
                        align="center"
                    ),
                    rx.box()
                ),
                align="center",
                width="100%"
            ),
            rx.vstack(
                rx.text(value, size="6", weight="bold", color=COLORS["gray"]["800"]),
                rx.text(title, size="3", color=COLORS["gray"]["600"]),
                spacing="1",
                align_items="start",
                width="100%"
            ),
            spacing="4",
            align_items="stretch",
            width="100%"
        ),
        padding="24px",
        background="white",
        border_radius="16px",
        border=f"1px solid {COLORS['gray']['200']}",
        box_shadow=SHADOWS["lg"],
        _hover={
            "box_shadow": SHADOWS["xl"],
            "transform": "translateY(-2px)"
        },
        transition="all 0.2s ease",
        width="100%"
    )

def page_header(
    title: str,
    subtitle: Optional[str] = None,
    actions: Optional[List[rx.Component]] = None
) -> rx.Component:
    """
    📄 Header universal para todas las páginas
    
    Reemplaza todos los headers duplicados que tienes
    """
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    title,
                    size="7",
                    weight="bold",
                    color=COLORS["gray"]["800"]
                ),
                rx.text(
                    subtitle,
                    size="4",
                    color=COLORS["gray"]["600"]
                ),
                spacing="1",
                align_items="start"
            ),
            rx.spacer(),
            rx.hstack(
                *actions if actions else [],
                spacing="3",
                align="center"
            ),
            width="100%",
            align="center"
        ),
        padding="12px 24px",
        background="white",
        border_bottom=f"1px solid {COLORS['gray']['200']}",
        position="sticky",
        top="0",
        z_index="100"
    )
    
    
def sidebar() -> rx.Component:
    """🎯 Sidebar profesional con tema oscuro y glassmorphism"""
    return rx.box(
        rx.vstack(
            # Header del sidebar con glassmorphism
            rx.box(
                rx.vstack(
                    # Logo y marca
                    rx.hstack(
                        
                            rx.image(
                                src="/images/logo-odontomara.png",
                                width="45px",
                                height="45px",
                                border_radius="50%"
                            ),
                        rx.vstack(
                            rx.text(
                                "Odontomara",
                                font_size="1.5rem",
                                font_weight="800", 
                                color="white",
                                line_height="1.2"
                            ),
                            rx.text(
                                AppState.rol_usuario.title(),
                                font_size="0.875rem",
                                color="#d7d7db",
                                font_weight="500"
                            ),
                            spacing="1",
                            align_items="start"
                        ),
                        spacing="3",
                        align="center",
                        width="100%"
                    ),
                    
                    # Línea decorativa
                    rx.box(
                        width="100%",
                        height="2px",
                        background=f"linear-gradient(90deg, transparent 0%, {COLORS['primary']['400']}80 50%, transparent 100%)",
                        border_radius="2px",
                        margin_top=SPACING["4"],
                        box_shadow=f"0 0 8px {COLORS['primary']['400']}40"
                    ),
                    
                    spacing="2",
                    width="100%"
                ),
                padding=SPACING["4"],
                width="100%"
            ),
            
            # Navegación moderna
            rx.box(
                rx.vstack(
                    _modern_nav_item("Dashboard", "home", "dashboard"),
                    _modern_nav_item("Pacientes", "users", "pacientes"),

                    # Consultas solo para gerente y administrador
                    rx.cond(
                        (AppState.rol_usuario == "gerente") | (AppState.rol_usuario == "administrador"),
                        _modern_nav_item("Consultas", "calendar", "consultas")
                    ),

                    # Opciones específicas por rol
                    rx.cond(
                        AppState.rol_usuario == "gerente",
                        rx.fragment(
                            _modern_nav_item("Pagos", "credit-card", "pagos"),
                            _modern_nav_item("Personal", "user-plus", "personal"),
                            _modern_nav_item("Servicios", "list", "servicios"),
                            _modern_nav_item("Reportes", "bar-chart", "reportes")
                        )
                    ),

                    rx.cond(
                        AppState.rol_usuario == "administrador",
                        _modern_nav_item("Pagos", "credit-card", "pagos")
                    ),

                    rx.cond(
                        AppState.rol_usuario == "odontologo",
                        _modern_nav_item("Odontología", "activity", "odontologia")
                    ),
                    
                    spacing="2",
                    align_items="stretch",
                    width="100%"
                ),
                padding=SPACING["4"],
                flex="1",
                width="100%",
                overflow_y="auto"
            ),
            
            # Footer moderno con botón de logout
            rx.box(
                _modern_logout_button(),
                padding=SPACING["6"],
                border_top="1px solid rgba(255, 255, 255, 0.1)",
                background="linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%)",
                backdrop_filter="blur(10px)",
                width="100%"
            ),
            
            spacing="0",
            height="100vh",
            width="100%"
        ),
        
        width="240px",
        min_width="240px", 
        height="100vh",
        flex_shrink="0",
        # Fondo principal del sidebar
        background="rgba(15, 23, 42, 0.95)",
        backdrop_filter="blur(25px) saturate(150%)",
        border_right="1px solid rgba(255, 255, 255, 0.15)",
        box_shadow="4px 0 24px rgba(0, 0, 0, 0.4), inset 1px 0 0 rgba(255, 255, 255, 0.1)",
        position="relative"
    )

def _modern_nav_item(label: str, icon: str, page: str) -> rx.Component:
    """🧭 Item de navegación moderno simplificado"""
    is_active = AppState.current_page == page
    
    return rx.box(
        rx.hstack(
            # Icono simple
            rx.icon(
                icon, 
                size=20,
                color=rx.cond(is_active, "white", "#ededed")
            ),
            
            # Texto del label
            rx.text(
                label,
                font_size="1rem",
                font_weight=rx.cond(is_active, "600", "500"),
                color=rx.cond(is_active, "white", "#a1a1aa")
            ),
            
            spacing="3",
            align="center",
            width="100%"
        ),
        
        padding=f"{SPACING['3']} {SPACING['4']}",
        border_radius=RADIUS["lg"],
        background=rx.cond(
            is_active,
            f"linear-gradient(135deg, {COLORS['primary']['500']}60 0%, {COLORS['blue']['600']}40 100%)",
            "transparent"
        ),
        border=rx.cond(
            is_active,
            f"1px solid {COLORS['primary']['400']}80",
            "1px solid transparent"
        ),
        box_shadow=rx.cond(
            is_active,
            f"0 4px 12px {COLORS['primary']['500']}40",
            "none"
        ),
        cursor="pointer",
        transition="all 0.3s ease",
        _hover={
            "background": rx.cond(
                is_active,
                f"linear-gradient(135deg, {COLORS['primary']['500']}70 0%, {COLORS['primary']['600']}50 100%)",
                "rgba(255, 255, 255, 0.08)"
            ),
            "transform": "translateX(2px)"
        },
        on_click=lambda: AppState.navigate_to(page)
    )

def _modern_logout_button() -> rx.Component:
    """🚪 Botón de logout moderno"""
    return rx.button(
        rx.hstack(
            rx.icon("log-out", size=18, color="#e8e8e8"),
            rx.text("Cerrar Sesión", font_weight="500", color="#cfcfcf"),
            spacing="3",
            align="center"
        ),
        width="100%",
        background="rgba(255, 255, 255, 0.05)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius=RADIUS["xl"],
        padding=f"{SPACING['3']} {SPACING['4']}",
        cursor="pointer",
        transition="all 0.3s ease",
        _hover={
            "background": f"linear-gradient(135deg, {COLORS['error']['500']}20 0%, {COLORS['error']['600']}10 100%)",
            "border_color": f"{COLORS['error']['400']}60",
            "color": COLORS["error"]["400"],
            "transform": "translateY(-2px)",
            "box_shadow": f"0 4px 12px {COLORS['error']['500']}30"
        },
        on_click=AppState.cerrar_sesion
    )
    
def _nav_item(label: str, icon: str, page: str) -> rx.Component:
    """🧭 Item de navegación"""
    is_active = AppState.current_page == page
    
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(label, size="3",weight="medium"),
            spacing="3",
            align="center"
        ),
        padding="12px 16px",
        border_radius="8px",
        background=rx.cond(is_active, f"{ROLE_THEMES['gerente']['gradient']}", "transparent"),
        color=rx.cond(is_active,  "white", COLORS["gray"]["600"]),
        cursor="pointer",
        width="100%",
        transition="all 0.2s ease",
        _hover={
            "background": rx.cond(is_active,f"{ROLE_THEMES['gerente']['gradient']}",  COLORS["gray"]["50"])
        },
        on_click=lambda: AppState.navigate_to(page) # type: ignore
    )

# ==========================================
# LAYOUT Y PÁGINAS MÉDICAS
# ==========================================

def medical_page_layout(children) -> rx.Component:
    """🏥 Wrapper universal para todas las páginas médicas
    
    Aplica el fondo estándar y layout consistente.
    Usar en todas las páginas para mantener diseño uniforme.
    """
    return rx.box(
        rx.box(
            children,
            style={
                "position": "relative",
                "z_index": "10"
            }
        ),
        style={
            **dark_page_background(),
            "padding": f"{SPACING['3']} {SPACING['5']}",
            "min_height": "100vh"
        },
        width="100%"
    )

# ==========================================
# SISTEMA DE TOASTS FLOTANTES
# ==========================================

def medical_toast(
    message: str,
    toast_type: str = "success", 
    duration: int = 4000
) -> rx.Component:
    """🚨 Toast médico flotante individual"""
    
    # Configuración por tipo usando rx.cond
    icon = rx.cond(
        toast_type == "success", "circle_check",
        rx.cond(
            toast_type == "error", "circle_alert",
            rx.cond(
                toast_type == "warning", "triangle_alert",
                "info"  # default
            )
        )
    )
    
    # Configuración de colores por tipo
    success_color = COLORS["success"]
    error_color = COLORS["error"] 
    warning_color = COLORS["warning"]
    primary_color = COLORS["primary"]
    
    gradient = rx.cond(
        toast_type == "success", f"linear-gradient(135deg, {success_color['600']} 0%, {success_color['500']} 100%)",
        rx.cond(
            toast_type == "error", f"linear-gradient(135deg, {error_color['600']} 0%, {error_color['500']} 100%)",
            rx.cond(
                toast_type == "warning", f"linear-gradient(135deg, {warning_color['500']} 0%, {warning_color['500']} 100%)",
                f"linear-gradient(135deg, {primary_color['600']} 0%, {primary_color['500']} 100%)"
            )
        )
    )
    
    border_color = rx.cond(
        toast_type == "success", f"1px solid {success_color['400']}60",
        rx.cond(
            toast_type == "error", f"1px solid {error_color['400']}60",
            rx.cond(
                toast_type == "warning", f"1px solid {warning_color['500']}60",
                f"1px solid {primary_color['400']}60"
            )
        )
    )
    
    shadow_color = rx.cond(
        toast_type == "success", f"0 10px 25px {success_color['500']}30",
        rx.cond(
            toast_type == "error", f"0 10px 25px {error_color['500']}30", 
            rx.cond(
                toast_type == "warning", f"0 10px 25px {warning_color['500']}30",
                f"0 10px 25px {primary_color['500']}30"
            )
        )
    )
    
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=20, color="white"),
            rx.text(
                message,
                size="3",
                color="white",
                weight="medium"
            ),
            rx.button(
                rx.icon("x", size=16, color="white"),
                size="1",
                variant="ghost",
                on_click=lambda: AppState.remove_toast(message),
                style={
                    "background": "transparent",
                    "border": "none",
                    "padding": "2px",
                    "_hover": {"background": "rgba(255,255,255,0.1)"}
                }
            ),
            justify="between",
            align="center",
            width="100%"
        ),
        style={
            "background": gradient,
            "border": border_color,
            "border_radius": RADIUS["lg"],
            "padding": f"{SPACING['4']} {SPACING['5']}",
            "min_width": "320px",
            "max_width": "400px",
            "backdrop_filter": "blur(20px)",
            "box_shadow": shadow_color,
            "animation": "slideInRight 0.4s ease-out, fadeOut 0.3s ease-out forwards",
            "animation_delay": f"0s, {duration/1000}s",
            "margin_bottom": SPACING["3"]
        }
    )

def medical_toast_container() -> rx.Component:
    """📱 Contenedor de toasts flotantes"""
    return rx.box(
        rx.foreach(
            AppState.active_toasts,
            lambda toast: medical_toast(
                toast.message,
                toast.toast_type,
                toast.duration
            )
        ),
        style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "z_index": "9999",
            "max_width": "400px"
        }
    )

# CSS para animaciones
def toast_animations_css() -> rx.Component:
    """🎬 CSS para animaciones de toasts"""
    return rx.script("""
        if (!document.getElementById('toast-animations')) {
            const style = document.createElement('style');
            style.id = 'toast-animations';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        opacity: 0;
                        transform: translateX(100%);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
                @keyframes fadeOut {
                    from {
                        opacity: 1;
                        transform: translateX(0) scale(1);
                    }
                    to {
                        opacity: 0;
                        transform: translateX(100%) scale(0.95);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    """)

# ==========================================
# MODAL DE CONFIRMACIÓN GENÉRICO
# ==========================================

def confirmation_modal() -> rx.Component:
    """
    ⚠️ MODAL DE CONFIRMACIÓN GENÉRICO

    Modal reutilizable para cualquier acción que requiera confirmación.
    Lee los datos desde AppState:
    - modal_confirmacion_abierto: bool
    - titulo_modal_confirmacion: str
    - mensaje_modal_confirmacion: str
    - accion_modal_confirmacion: str (nombre del método a llamar)
    """
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
                    AppState.titulo_modal_confirmacion,
                    size="5",
                    color=COLORS["gray"]["800"],
                    text_align="center"
                ),
                rx.text(
                    AppState.mensaje_modal_confirmacion,
                    size="3",
                    color=COLORS["gray"]["600"],
                    text_align="center",
                    line_height="1.5",
                    max_width="400px"
                ),
                spacing="4",
                align="center",
                margin_bottom="6"
            ),

            # Botones de acción
            rx.hstack(
                rx.button(
                    "Cancelar",
                    on_click=AppState.cerrar_todos_los_modales,
                    style={
                        "background": "transparent",
                        "border": f"1px solid {COLORS['gray']['300']}",
                        "color": COLORS["gray"]["700"],
                        "border_radius": RADIUS["2xl"],
                        "padding": f"{SPACING['3']} {SPACING['6']}",
                        "font_weight": "600",
                        "transition": ANIMATIONS["presets"]["crystal_hover"],
                        "cursor": "pointer",
                        "_hover": {
                            "background": COLORS["gray"]["50"],
                            "transform": "translateY(-2px)",
                            "box_shadow": SHADOWS["sm"]
                        }
                    },
                    width="100%"
                ),
                rx.button(
                    "Confirmar",
                    on_click=AppState.ejecutar_accion_confirmacion,
                    loading=AppState.cargando_operacion_personal,
                    style={
                        "background": GRADIENTS["neon_primary"].replace(
                            COLORS["primary"]["500"],
                            COLORS["error"]["500"]
                        ).replace(
                            COLORS["blue"]["600"],
                            COLORS["error"]["600"]
                        ),
                        "color": "white",
                        "border": "none",
                        "border_radius": RADIUS["2xl"],
                        "padding": f"{SPACING['3']} {SPACING['6']}",
                        "font_weight": "700",
                        "cursor": "pointer",
                        "box_shadow": SHADOWS["glow_primary"].replace(
                            COLORS["primary"]["500"],
                            COLORS["error"]["500"]
                        ),
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
                "background": f"linear-gradient(135deg, white 0%, {COLORS['gray']['50']} 100%)",
                "box_shadow": SHADOWS["crystal_xl"],
                "border": f"1px solid {COLORS['error']['200']}40",
            }
        ),
        open=AppState.modal_confirmacion_abierto,
        on_open_change=AppState.cerrar_todos_los_modales
    )

# ==========================================
# BREADCRUMBS MÉDICOS
# ==========================================

def medical_breadcrumb(
    current_page: str,
    parent_pages: List[Dict[str, str]] = None
) -> rx.Component:
    """🧭 Breadcrumb médico profesional"""
    if parent_pages is None:
        parent_pages = []
    
    return rx.hstack(
        rx.foreach(
            parent_pages,
            lambda page: rx.hstack(
                rx.link(
                    page["name"],
                    href=page["url"],
                    color=COLORS["gray"]["400"],
                    text_decoration="none",
                    _hover={"color": COLORS["primary"]["400"]}
                ),
                rx.icon("chevron_right", size=14, color=COLORS["gray"]["500"]),
                spacing="2"
            )
        ),
        rx.text(
            current_page,
            color=COLORS["primary"]["400"],
            font_weight="500"
        ),
        spacing="2",
        align="center",
        margin_bottom=SPACING["4"]
    )
