"""
Componentes específicos para el rol de Gerente/Jefe - VERSIÓN CORREGIDA
Incluye sidebar, cards de estadísticas, tablas y modales
"""

import reflex as rx
from typing import List, Dict, Any, Optional
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS

# ==========================================
# COMPONENTES DE NAVEGACIÓN
# ==========================================

def sidebar_item(icon: str, text: str, page_id: str, current_page: str) -> rx.Component:
    """Item individual del sidebar con icon y texto"""
    is_active = current_page == page_id
    
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=20),
            rx.text(text, size="3", weight="medium"),
            spacing="3",
            align="center",
        ),
        padding="12px 16px",
        border_radius="8px",
        background=rx.cond(
            is_active,
            COLORS["primary"]["500"],
            "transparent"
        ),
        color=rx.cond(is_active, "white", COLORS["gray"]["600"]),
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background": rx.cond(
                is_active,
                COLORS["primary"]["500"],
                COLORS["gray"]["50"]
            ),
            "color": rx.cond(is_active, "white", COLORS["gray"]["700"])
        },
        on_click=lambda: navigate_to_page(page_id),
        width="100%"
    )

def navigate_to_page(page_id: str):
    """Función auxiliar para navegación"""
    from dental_system.state.boss_state import BossState
    return BossState.navigate_to(page_id)

def boss_sidebar() -> rx.Component:
    """Sidebar de navegación para el gerente"""
    from dental_system.state.boss_state import BossState
    
    return rx.box(
        # Header del sidebar
        rx.hstack(
            # rx.icon("activity", size=32, color=COLORS["primary"]["500"]),
            rx.image(
                        src="/images/logo-odontomara.png",
                        width="60px",
                        border_radius="50%",
                        alt=""
                    ),
            rx.vstack(
                rx.text("Odontomara", size="6", weight="bold", color=COLORS["secondary"]["700"],text_shadow=SHADOWS["xl"]),
                rx.text("Panel Gerencial", size="2", color=COLORS["gray"]["500"]),
                spacing="0",
                align_items="start"
            ),
            spacing="3",
            align="center",
            padding="20px",
            border_bottom=f"1px solid {COLORS['gray']['200']}"
        ),
        
        # Navegación principal
        rx.vstack(
            rx.text("Principal", size="2", weight="medium", color=COLORS["gray"]["500"], margin_bottom="8px"),
            sidebar_item("layout-dashboard", "Dashboard", "dashboard", BossState.current_page),
            sidebar_item("users", "Personal", "personal", BossState.current_page),
            sidebar_item("package", "Servicios", "servicios", BossState.current_page),
            
            rx.text("Gestión", size="2", weight="medium", color=COLORS["gray"]["500"], margin_top="24px", margin_bottom="8px"),
            sidebar_item("user-check", "Pacientes", "pacientes", BossState.current_page),
            sidebar_item("calendar", "Consultas", "consultas", BossState.current_page),
            sidebar_item("credit-card", "Pagos", "pagos", BossState.current_page),
            
            rx.text("Análisis", size="2", weight="medium", color=COLORS["gray"]["500"], margin_top="24px", margin_bottom="8px"),
            sidebar_item("bar-chart-3", "Reportes", "reportes", BossState.current_page),
            sidebar_item("settings", "Configuración", "settings", BossState.current_page),
            
            spacing="2",
            align_items="stretch",
            padding="20px",
            width="100%"
        ),
        
        # Footer del sidebar
        rx.spacer(),
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        rx.cond(
                            BossState.user_profile,
                            BossState.user_profile["nombre_completo"],
                            "Usuario"
                        ), 
                        size="3", 
                        weight="medium"
                    ),
                    rx.text(
                        rx.cond(
                            BossState.user_profile,
                            BossState.user_profile["email"],
                            "email@dental.com"
                        ), 
                        size="2", 
                        color=COLORS["gray"]["500"]
                    ),
                    spacing="0",
                    align_items="start"
                ),
                spacing="3",
                align="center"
            ),
            padding="20px",
            border_top=f"1px solid {COLORS['gray']['200']}"
        ),
        
        width=rx.cond(BossState.sidebar_collapsed, "80px", "280px"),
        height="100vh",
        background="white",
        border_right=f"1px solid {COLORS['gray']['200']}",
        position="fixed",
        left="0",
        top="0",
        z_index="1000",
        transition="width 0.3s ease",
        overflow_y="auto"
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
# COMPONENTE DE LOADING
# ==========================================

def loading_spinner(show: bool = True) -> rx.Component:
    """Spinner de carga"""
    return rx.cond(
        show,
        rx.center(
            rx.vstack(
                rx.spinner(size="3", color=COLORS["primary"]["500"]),
                rx.text("Cargando...", color=COLORS["gray"]["600"], size="3"),
                spacing="3",
                align="center"
            ),
            padding="40px",
            width="100%"
        ),
        rx.box()
    )

# ==========================================
# HEADER PRINCIPAL
# ==========================================

def main_header(title: str, subtitle: str = "") -> rx.Component:
    """Header principal de las páginas"""
    from dental_system.state.boss_state import BossState
    
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(title, size="6", weight="bold", color=COLORS["gray"]["800"]),
                rx.cond(
                    subtitle != "",
                    rx.text(subtitle, size="3", color=COLORS["gray"]["600"]),
                    rx.box()
                ),
                spacing="1",
                align_items="start"
            ),
            rx.spacer(),
            rx.button(
                rx.icon("menu", size=20),
                background=COLORS["gray"]["900"],
                border=f"1px solid {COLORS['gray']['300']}",
                border_radius="8px",
                padding="8px",
                cursor="pointer",
                on_click=BossState.toggle_sidebar,
                _hover={"background": COLORS["gray"]["50"]}
            ),
            align="center",
            width="100%"
        ),
        padding="20px 24px",
        background="white",
        border_bottom=f"1px solid {COLORS['gray']['200']}",
        position="sticky",
        top="0",
        z_index="100"
    )

# ==========================================
# COMPONENTES DE TABLAS
# ==========================================

def data_table_header(columns: List[str]) -> rx.Component:
    """Header de tabla de datos"""
    return rx.hstack(
        *[
            rx.text(
                col,
                size="3",
                weight="medium",
                color=COLORS["gray"]["600"],
                text_align="left" if i == 0 else "center"
            )
            for i, col in enumerate(columns)
        ],
        spacing="4",
        align="center",
        padding="16px 20px",
        background=COLORS["gray"]["50"],
        border_bottom=f"1px solid {COLORS['gray']['200']}",
        width="100%"
    )

def data_table_row(data: Dict[str, Any], columns: List[str], actions: Optional[List[rx.Component]] = None) -> rx.Component:
    """Fila de tabla de datos"""
    return rx.hstack(
        *[
            rx.text(
                str(data.get(col.lower().replace(" ", "_"), "")),
                size="3",
                color=COLORS["gray"]["700"],
                text_align="left" if i == 0 else "center"
            )
            for i, col in enumerate(columns)
        ],
        rx.cond(
            actions is not None,
            rx.hstack(*actions, spacing="2", justify="center"),
            rx.box()
        ),
        spacing="4",
        align="center",
        padding="16px 20px",
        border_bottom=f"1px solid {COLORS['gray']['100']}",
        _hover={"background": COLORS["gray"]["50"]},
        width="100%"
    )

def data_table(
    data: List[Dict[str, Any]], 
    columns: List[str],
    title: str = "",
    actions_generator = None
) -> rx.Component:
    """Tabla de datos completa con header, filas y acciones"""
    return rx.box(
        rx.cond(
            title != "",
            rx.box(
                rx.text(title, size="5", weight="bold", color=COLORS["gray"]["800"]),
                padding="20px 20px 0 20px"
            ),
            rx.box()
        ),
        
        rx.box(
            data_table_header(columns + (["Acciones"] if actions_generator else [])),
            rx.foreach(
                data,
                lambda item: data_table_row(
                    item, 
                    columns,
                    actions_generator(item) if actions_generator else None
                )
            ),
            overflow_x="auto"
        ),
        
        background="white",
        border_radius="12px",
        border=f"1px solid {COLORS['gray']['200']}",
        overflow="hidden",
        width="100%"
    )

# ==========================================
# COMPONENTE DE MODAL
# ==========================================

def modal_overlay(show: rx.Var[bool], content: rx.Component) -> rx.Component:
    """Overlay del modal"""
    return rx.cond(
        show,
        rx.box(
            rx.box(
                content,
                position="relative",
                max_width="600px",
                width="90%",
                max_height="90vh",
                overflow_y="auto"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.5)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="2000",
            
        ),
        rx.box()
    )
