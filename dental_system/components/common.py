import reflex as rx
from typing import List, Dict, Any, Optional
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS

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
                rx.cond(icon is not None, rx.icon(icon, size=16), rx.box()),
                rx.text(text, size="3"),
                spacing="2",
                align="center"
            )
        ),
        background=COLORS["primary"]["500"],
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

def secondary_button(
    text: str,
    icon: Optional[str] = None,
    on_click = None,
    variant: str = "outline"
) -> rx.Component:
    """Botón secundario"""
    icon_component = rx.icon(icon, size=16) if icon is not None else rx.box()
    return rx.button(
        rx.hstack(
            icon_component,
            rx.text(text, size="3"),
            spacing="2",
            align="center"
        ),
        background="transparent" if variant == "outline" else COLORS["gray"]["100"],
        color=COLORS["gray"]["600"],
        border=f"1px solid {COLORS['gray']['300']}" if variant == "outline" else "none",
        border_radius="8px",
        padding="8px 16px",
        font_weight="500",
        font_size="14px",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background": COLORS["gray"]["50"] if variant == "outline" else COLORS["gray"]["200"],
            "border_color": COLORS["gray"]["400"] if variant == "outline" else "none"
        },
        on_click=on_click
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
                rx.cond(icon is not None, rx.icon(icon, size=16), rx.box()),
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
                rx.icon("check-circle", size=20, color=COLORS["success"]),
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
                rx.icon("alert-circle", size=20, color=COLORS["error"]),
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
    return rx.box(
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
