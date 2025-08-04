import reflex as rx
from typing import List, Dict, Any, Optional
from ..state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, ROLE_THEMES,RADIUS

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
        background=f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['blue']['600']} 100%)",
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
        padding="12px 20px",
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
    """🎯 Sidebar unificado que se adapta al rol"""
    return rx.box(
        rx.vstack(
            # Header del sidebar
            rx.hstack(
                rx.image(
                    src="/images/logo-odontomara.png",
                    width="50px",
                    border_radius="50%"
                ),
                rx.vstack(
                    rx.text("Odontomara", size="5", weight="bold", color=COLORS["secondary"]["700"],text_shadow=SHADOWS["xl"]),
                    rx.text(AppState.user_role.title(), size="2",  color=COLORS["gray"]["500"]),
                    spacing="0",
                    align_items="start"
                ),
                spacing="3",
                align="center",
                padding="20px",
                border_bottom=f"1px solid {COLORS['gray']['200']}"
            ),
            
            # Navegación
            rx.vstack(
                _nav_item("Dashboard", "home", "dashboard"),
                _nav_item("Pacientes", "users", "pacientes"),
                _nav_item("Consultas", "calendar", "consultas"),
                
                # Opciones específicas por rol
                rx.cond(
                    AppState.user_role == "gerente",
                    rx.fragment(
                        _nav_item("Personal", "user-plus", "personal"),
                        _nav_item("Servicios", "list", "servicios"),
                        _nav_item("Reportes", "bar-chart", "reportes")
                    )
                ),
                
                rx.cond(
                    AppState.user_role == "administrador",
                    _nav_item("Pagos", "credit-card", "pagos")
                ),
                
                rx.cond(
                    AppState.user_role == "odontologo",
                    _nav_item("Odontología", "tooth", "odontologia")
                ),
                
                spacing="2",
                align_items="stretch",
                width="100%",
                padding="15px"
            ),
            
            rx.spacer(),
            
            # Footer del sidebar
            rx.box(
               secondary_button(
                    text="Cerrar Sesión",
                    icon="log-out",
                    on_click=AppState.logout_user,
                    variant="ghost" 
                ), 
                width="100%",
                # margin="24px",
                padding="20px 18px",
               
            ),
            spacing="5",
            height="100%",
            width="100%",
        ),
        
        width="220px",
        height="100%",
        background="white",
        border_right=f"1px solid {COLORS['gray']['200']}",
        # overflow_y="auto"
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



# # ==========================================
# # ✅ TABLA DE PACIENTES CORREGIDA
# # ==========================================

def paciente_table_row(paciente_data) -> rx.Component:
    """✅ CORREGIDA: Fila individual de la tabla de pacientes con campos separados"""
    return rx.hstack(
        # ✅ INFORMACIÓN PRINCIPAL - USANDO nombre_completo del modelo
        rx.vstack(
            rx.text(
               rx.cond(
                    paciente_data.primer_nombre,
                    f"{paciente_data.primer_nombre} {paciente_data.primer_apellido}".strip(),
                    "N/A"
               ),
                size="3", 
                weight="medium",
                color=COLORS["gray"]["800"]
            ),
            rx.text(
                rx.cond(
                    paciente_data.numero_historia,
                    f"HC: {paciente_data.numero_historia}",
                    'Sin asignar'
                ),        
                size="2", 
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="center",
            flex="3"
        ),
        
        # ✅ DOCUMENTO - SIN CAMBIOS
        rx.vstack(
            rx.text(
                f"{paciente_data.tipo_documento}-{paciente_data.numero_documento}",
                size="3", 
                color=COLORS["gray"]["700"]
            ),
            rx.text(
                f"edad: {paciente_data.edad}".strip(),
                size="2",
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="center",
            flex="2"
        ),
        
        # ✅ GÉNERO - SIN CAMBIOS
        rx.badge(
            paciente_data.genero,
            variant="soft",
            color_scheme=rx.match(
                paciente_data.genero,
                ("masculino", "blue"),
                ("femenino", "pink"),
                ("otro", "gray"),
                "gray"
            ),
            align="center",
            flex="1"
        ),
        
        # ✅ CONTACTO - ACTUALIZADO PARA USAR telefono_display
        rx.vstack(
            rx.text(
                f"{paciente_data.telefono_1}".strip(),  # ✅ Usa la propiedad que maneja telefono_1 y telefono_2
                size="3", 
                color=COLORS["gray"]["600"]
            ),
            rx.text(
                rx.cond(
                    paciente_data.email,
                    paciente_data.email,
                    "Sin email"
                ),
                size="2",
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="center",
            flex="3"
        ),
        
        # ✅ ESTADO - SIN CAMBIOS
        rx.badge(
            paciente_data.activo,
            variant="soft",
            color_scheme=rx.match(
                paciente_data.activo,
                (True, "green"),
                (False, "red"),
                "gray"
            ),
            
            align="center",
            flex="1"
        ),
        
        # # ✅ ACCIONES - SIN CAMBIOS
        # rx.hstack(
        #     rx.tooltip(
        #         rx.button(
        #             rx.icon("edit", size=16),
        #             size="2",
        #             variant="ghost",
        #             color=COLORS["primary"]["500"],
        #             on_click=lambda: AdminState.open_paciente_modal(paciente_data)
        #         ),
        #         content="Editar paciente"
        #     ),
        #     rx.tooltip(
        #         rx.button(
        #             rx.icon("trash-2", size=16),
        #             size="2",
        #             variant="ghost",
        #             color=COLORS["error"],
        #             on_click=lambda: AdminState.open_delete_confirmation(paciente_data)
        #         ),
        #         content="Eliminar paciente"
        #     ),
        #     # Botón de reactivar solo si está inactivo
        #     rx.cond(
        #         paciente_data.activo == False,
        #         rx.tooltip(
        #             rx.button(
        #                 rx.icon("refresh-cw", size=16),
        #                 size="2",
        #                 variant="ghost",
        #                 color=COLORS["success"],
        #                 on_click=lambda: AdminState.reactivate_paciente(paciente_data)
        #             ),
        #             content="Reactivar paciente"
        #         ),
        #         rx.box()
        #     ),
        #     spacing="1",
        #     align="center",
        #     flex="1"
        # ),
        
        spacing="4",
        align="center",
        padding="16px 20px",
        border_bottom=f"1px solid {COLORS['gray']['100']}",
        _hover={"background": COLORS["gray"]["50"]},
        width="100%"
    )
