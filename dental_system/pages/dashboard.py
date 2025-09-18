"""
🏥 DASHBOARD PRINCIPAL - VERSIÓN REFACTORIZADA  
==============================================

✨ Dashboard moderno y personalizado por rol:
- Header dinámico con gradientes por rol de usuario
- Cards de estadísticas con glassmorphism effect
- Gráficos interactivos y modernos
- Acciones rápidas contextuales por rol
- Diseño responsive mobile-first
- Animaciones suaves y micro-interacciones

Desarrollado para Reflex.dev con patrones modernos
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, secondary_button, stat_card
from dental_system.components.charts import graficas_resume
from dental_system.styles.themes import (
    COLORS, 
    SHADOWS, 
    RADIUS, 
    SPACING, 
    ANIMATIONS, 
    ROLE_THEMES,
    get_color
)
# ==========================================
# 🎨 COMPONENTES MODERNOS DEL DASHBOARD  
# ==========================================

def role_based_header() -> rx.Component:
    """🎭 Header personalizado dinámicamente según el rol del usuario"""
    role_config = {
        "gerente": {
            "emoji": "👔",
            "title": "Dashboard Gerencial",
            "subtitle": "Control total y métricas ejecutivas de la clínica odontológica",
            "gradient": ROLE_THEMES["gerente"]["gradient"]
        },
        "administrador": {
            "emoji": "👤", 
            "title": "Dashboard Administrativo",
            "subtitle": "Gestión de pacientes, consultas y operaciones diarias",
            "gradient": ROLE_THEMES["administrador"]["gradient"]
        },
        "odontologo": {
            "emoji": "🦷",
            "title": "Dashboard Clínico",
            "subtitle": "Panel de atención odontológica y seguimiento de pacientes", 
            "gradient": ROLE_THEMES["odontologo"]["gradient"]
        },
        "asistente": {
            "emoji": "🩺",
            "title": "Dashboard Asistencial",
            "subtitle": "Apoyo en consultas y gestión básica del día",
            "gradient": ROLE_THEMES["asistente"]["gradient"]
        }
    }
    
    # En lugar de usar .get(), crear el config dinámicamente con rx.cond
    emoji = rx.match(
        AppState.rol_usuario,
        ("gerente", "👔"),
        ("odontologo", "🦷"),
        ("administrador", "👤"),
        ("asistente", "📋"),
        "👤"  # Default
    )
    
    title = rx.match(
        AppState.rol_usuario,
        ("gerente", "Dashboard Gerencial"),
        ("odontologo", "Dashboard Clínico"),
        ("administrador", "Dashboard Administrativo"), 
        ("asistente", "Dashboard Asistente"),
        "Dashboard Administrativo"  # Default
    )
    
    gradient = rx.match(
        AppState.rol_usuario,
        ("gerente", ROLE_THEMES["gerente"]["gradient"]),
        ("odontologo", ROLE_THEMES["odontologo"]["gradient"]),
        ("administrador", ROLE_THEMES["administrador"]["gradient"]),
        ("asistente", ROLE_THEMES["asistente"]["gradient"]),
        ROLE_THEMES["administrador"]["gradient"]  # Default
    )
    
    subtitle = rx.match(
        AppState.rol_usuario,
        ("gerente", "Control total del consultorio y métricas avanzadas"),
        ("odontologo", "Atención de pacientes y gestión clínica especializada"),
        ("administrador", "Gestión completa de pacientes y operaciones diarias"),
        ("asistente", "Soporte en consultas y tareas administrativas básicas"),
        "Gestión completa de pacientes y operaciones diarias"  # Default
    )
    
    return rx.box(
        rx.vstack(
            # Header principal con gradiente por rol
            rx.hstack(
                rx.vstack(
                    # Título principal con icono del rol
                    rx.hstack(
                        rx.text(
                            emoji, 
                            font_size="2.5rem",
                            margin_right=SPACING["3"]
                        ),
                        rx.heading(
                            title,
                            style={
                                "font_size": "2.8rem",
                                "font_weight": "900",
                                "background": gradient,
                                "background_clip": "text", 
                                "color": "transparent",
                                "line_height": "1.1"
                            }
                        ),
                        spacing="2",
                        align="center"
                    ),
                    # Subtítulo descriptivo
                    rx.text(
                        subtitle,
                        size="4",
                        color=COLORS["gray"]["600"],
                        line_height="1.5",
                        max_width="600px"
                    ),
                    spacing="3",
                    align_items="start"
                ),
                rx.spacer(),
                # Botones de acción dinámicos
                role_action_buttons(),
                width="100%",
                align="center"
            ),
            # Barra de información del usuario logueado
            user_info_bar(),
            spacing="6",
            width="100%"
        ),
        style={
            "background": f"linear-gradient(135deg, {COLORS['gray']['50']} 0%, {COLORS['primary']['100']} 100%)",
            "padding": f"{SPACING['8']} {SPACING['6']}",
            "border_bottom": f"1px solid {COLORS['gray']['200']}"
        }
    )

def role_action_buttons() -> rx.Component:
    """⚡ Botones de acción rápida según el rol"""
    return rx.hstack(
        # Botón de actualizar datos
        rx.button(
            rx.hstack(
                rx.icon("refresh-ccw", size=18),
                rx.text("Actualizar", font_weight="600"),
                spacing="2",
                align="center"
            ),
            on_click=AppState.cargar_estadisticas_dashboard,
            style={
                "background": "transparent",
                "border": f"2px solid {COLORS['gray']['300']}",
                "color": COLORS["gray"]["700"],
                "border_radius": RADIUS["xl"],
                "padding": f"{SPACING['3']} {SPACING['5']}",
                "transition": ANIMATIONS["presets"]["button_hover"],
                "_hover": {
                    "border_color": COLORS["primary"]["500"],
                    "background": COLORS["primary"]["50"],
                    "transform": "translateY(-1px)",
                    "color": COLORS["primary"]["700"]
                }
            }
        ),
        # Botón contextual por rol
        rx.cond(
            AppState.rol_usuario == "gerente",
            rx.button(
                rx.hstack(
                    rx.icon("settings", size=18),
                    rx.text("Configuración", font_weight="600"),
                    spacing="2",
                    align="center"
                ),
                style={
                    "background": ROLE_THEMES["gerente"]["gradient"],
                    "color": "white",
                    "border": "none",
                    "border_radius": RADIUS["xl"],
                    "padding": f"{SPACING['3']} {SPACING['6']}",
                    "font_weight": "600",
                    "transition": ANIMATIONS["presets"]["button_hover"],
                    "box_shadow": SHADOWS["md"],
                    "_hover": {
                        "transform": "translateY(-2px)",
                        "box_shadow": SHADOWS["xl"]
                    }
                }
            ),
            rx.cond(
                AppState.rol_usuario == "odontologo", 
                rx.button(
                    rx.hstack(
                        rx.icon("users", size=18),
                        rx.text("Mis Pacientes", font_weight="600"),
                        spacing="2",
                        align="center"
                    ),
                    on_click=lambda: AppState.navigate_to("odontologia"),
                    style={
                        "background": ROLE_THEMES["odontologo"]["gradient"],
                        "color": "white",
                        "border": "none",
                        "border_radius": RADIUS["xl"],
                        "padding": f"{SPACING['3']} {SPACING['6']}",
                        "font_weight": "600",
                        "transition": ANIMATIONS["presets"]["button_hover"],
                        "box_shadow": SHADOWS["md"],
                        "_hover": {
                            "transform": "translateY(-2px)",
                            "box_shadow": SHADOWS["xl"]
                        }
                    }
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("calendar", size=18), 
                        rx.text("Consultas", font_weight="600"),
                        spacing="2",
                        align="center"
                    ),
                    on_click=lambda: AppState.navigate_to("consultas"),
                    style={
                        "background": ROLE_THEMES["administrador"]["gradient"],
                        "color": "white", 
                        "border": "none",
                        "border_radius": RADIUS["xl"],
                        "padding": f"{SPACING['3']} {SPACING['6']}",
                        "font_weight": "600",
                        "transition": ANIMATIONS["presets"]["button_hover"],
                        "box_shadow": SHADOWS["md"],
                        "_hover": {
                            "transform": "translateY(-2px)",
                            "box_shadow": SHADOWS["xl"]
                        }
                    }
                )
            )
        ),
        spacing="4",
        align="center"
    )

def user_info_bar() -> rx.Component:
    """👤 Barra de información del usuario actual"""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.box(
                    rx.icon("user", size=16, color="white"),
                    style={
                        "background": COLORS["primary"]["500"],
                        "border_radius": RADIUS["full"],
                        "padding": SPACING["2"]
                    }
                ),
                rx.vstack(
                    rx.text(
                        f"Bienvenido/a, {AppState.rol_usuario.title()}",
                        size="3",
                        font_weight="600",
                        color=COLORS["gray"]["800"]
                    ),
                    rx.text(
                        "Sesión iniciada exitosamente",
                        size="2",
                        color=COLORS["gray"]["500"]
                    ),
                    spacing="0",
                    align_items="start"
                ),
                spacing="3",
                align="center"
            ),
            rx.spacer(),
            # Indicador de estado en tiempo real
            rx.hstack(
                rx.box(
                    style={
                        "width": "8px",
                        "height": "8px",
                        "border_radius": RADIUS["full"],
                        "background": COLORS["success"]["500"],
                        "animation": "pulse 2s infinite"
                    }
                ),
                rx.text(
                    "Sistema Activo",
                    size="2",
                    color=COLORS["success"]["600"],
                    font_weight="500"
                ),
                spacing="2",
                align="center"
            ),
            width="100%",
            align="center"
        ),
        style={
            "background": "rgba(255, 255, 255, 0.9)",
            "backdrop_filter": "blur(10px)",
            "border": f"1px solid {COLORS['gray']['200']}",
            "border_radius": RADIUS["xl"],
            "padding": f"{SPACING['4']} {SPACING['5']}",
            "box_shadow": SHADOWS["sm"]
        }
    )

def dashboard_page() -> rx.Component:
    """
    🏥 DASHBOARD PRINCIPAL REFACTORIZADO
    
    ✨ Características:
    - Header personalizado por rol con gradientes
    - Cards de estadísticas modernas con animaciones
    - Acciones rápidas contextuales por rol 
    - Gráficos interactivos mejorados
    - Diseño responsive mobile-first
    """
    return rx.box(
        rx.vstack(
            # Header moderno personalizado por rol
            role_based_header(),
            
            # Contenido principal
            rx.box(
                rx.vstack(
                    # Grid de estadísticas principales
                    quick_stats_grid(),
                    
                    # Grid de contenido secundario
                    rx.grid(
                        # Columna izquierda - Acciones rápidas por rol
                        rx.cond(
                            AppState.rol_usuario == "gerente",
                            manager_quick_actions(),
                            rx.cond(
                                AppState.rol_usuario == "administrador",
                                admin_quick_actions(),
                                staff_quick_actions()
                            )
                        ),
                        
                        # Columna derecha - Gráficos mejorados
                        # rx.box(
                        #     graficas_resume(),
                        #     style={
                        #         "background": "rgba(255, 255, 255, 0.95)",
                        #         "backdrop_filter": "blur(20px)",
                        #         "border": f"1px solid {COLORS['gray']['200']}",
                        #         "border_radius": RADIUS["2xl"],
                        #         "box_shadow": SHADOWS["lg"],
                        #         "overflow": "hidden"
                        #     }
                        # ),
                        
                        columns=rx.breakpoints(initial="1", sm="1", md="1", lg="2"),  # Responsive
                        spacing="8",
                        width="100%"
                    ),
                    
                    spacing="9",
                    width="100%"
                ),
                style={
                    "padding": f"{SPACING['8']} {SPACING['6']}",
                    "max_width": "1600px",
                    "margin": "0 auto"
                }
            ),
            
            spacing="0",
            width="100%"
        ),
        
        style={
            "min_height": "100vh",
            "background": f"linear-gradient(to bottom right, {COLORS['gray']['50']} 0%, {COLORS['primary']['50']} 50%, {COLORS['secondary']['50']} 100%)",
            "position": "relative"
        },
        width="100%"
    )

def manager_quick_actions() -> rx.Component:
    """👔 Acciones rápidas para gerente con diseño moderno"""
    return rx.vstack(
        rx.heading(
            "⚡ Acciones Rápidas - Gerente",
            size="6",
            font_weight="800",
            color=COLORS["gray"]["800"],
            margin_bottom="6"
        ),
        rx.grid(
            modern_quick_action_card(
                "Gestionar Pacientes", 
                "users", 
                "Administrar base de datos de pacientes",
                lambda: AppState.navigate_to("pacientes"),
                COLORS["primary"]["500"]
            ),
            modern_quick_action_card(
                "Ver Consultas", 
                "calendar", 
                "Supervisar agenda y consultas",
                lambda: AppState.navigate_to("consultas"),
                COLORS["secondary"]["500"]
            ),
            modern_quick_action_card(
                "Gestionar Personal", 
                "user-plus", 
                "Administrar empleados y roles",
                lambda: AppState.navigate_to("personal"),
                COLORS["blue"]["500"]
            ),
            modern_quick_action_card(
                "Sistema de Pagos", 
                "credit-card", 
                "Gestionar facturación y cobros",
                lambda: AppState.navigate_to("pagos"),
                COLORS["success"]["500"]
            ),
            modern_quick_action_card(
                "Catálogo Servicios", 
                "list", 
                "Administrar servicios odontológicos",
                lambda: AppState.navigate_to("servicios"),
                COLORS["warning"]["500"]
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="3", lg="3", xl="5"),  # Responsive
            spacing="6"
        ),
        width="100%",
        spacing="6"
    )
        
    

def admin_quick_actions() -> rx.Component:
    """👤 Acciones rápidas para administrador"""
    return rx.vstack(
        rx.heading(
            "📋 Acciones Rápidas - Administrador",
            size="6",
            font_weight="800",
            color=COLORS["gray"]["800"],
            margin_bottom="6"
        ),
        rx.grid(
            modern_quick_action_card(
                "Gestionar Pacientes", 
                "users", 
                "Registrar y administrar pacientes",
                lambda: AppState.navigate_to("pacientes"),
                COLORS["primary"]["500"]
            ),
            modern_quick_action_card(
                "Consultas Médicas", 
                "calendar", 
                "Programar y gestionar consultas",
                lambda: AppState.navigate_to("consultas"),
                COLORS["secondary"]["500"]
            ),
            modern_quick_action_card(
                "Sistema de Pagos", 
                "credit-card", 
                "Procesar pagos y facturación",
                lambda: AppState.navigate_to("pagos"),
                COLORS["success"]["500"]
            ),
            columns=rx.breakpoints(initial="1", sm="1", md="2", lg="3"),  # Responsive
            spacing="6"
        ),
        width="100%",
        spacing="6"
    )

def staff_quick_actions() -> rx.Component:
    """👥 Acciones rápidas para personal (odontólogo/asistente)"""
    return rx.vstack(
        rx.heading(
            f"🩺 Acciones Rápidas - {AppState.rol_usuario.title()}",
            size="6",
            font_weight="800",
            color=COLORS["gray"]["800"],
            margin_bottom="6"
        ),
        rx.grid(
            modern_quick_action_card(
                "Ver Pacientes", 
                "users", 
                "Consultar información de pacientes",
                lambda: AppState.navigate_to("pacientes"),
                COLORS["primary"]["500"]
            ),
            modern_quick_action_card(
                "Mis Consultas", 
                "calendar", 
                "Ver mi agenda del día",
                lambda: AppState.navigate_to("consultas"),
                COLORS["secondary"]["500"]
            ),
            rx.cond(
                AppState.rol_usuario == "odontologo",
                modern_quick_action_card(
                    "Panel Odontológico", 
                    "stethoscope", 
                    "Atender pacientes y odontogramas",
                    lambda: AppState.navigate_to("odontologia"),
                    COLORS["success"]["500"]
                ),
                rx.box()  # Placeholder para asistentes
            ),
            columns=rx.breakpoints(initial="1", sm="1", md="2", lg="3"),  # Responsive
            spacing="6"
        ),
        width="100%",
        spacing="6"
    )

def modern_quick_action_card(title: str, icon: str, description: str, on_click, color: str = "") -> rx.Component:
    """⚡ Tarjeta de acción rápida moderna"""
    card_color = color if color else COLORS["primary"]["500"]
    return rx.box(
        rx.vstack(
            # Icono con gradiente de fondo
            rx.box(
                rx.icon(icon, size=40, color="white"),
                style={
                    "background": f"linear-gradient(135deg, {card_color} 0%, {card_color}CC 100%)",
                    "border_radius": RADIUS["2xl"],
                    "padding": SPACING["5"],
                    "box_shadow": f"0 8px 20px {card_color}40",
                    "margin_bottom": SPACING["4"]
                }
            ),
            # Título y descripción
            rx.vstack(
                rx.text(
                    title, 
                    size="4", 
                    font_weight="700", 
                    color=COLORS["gray"]["800"],
                    text_align="center"
                ),
                rx.text(
                    description, 
                    size="3", 
                    color=COLORS["gray"]["600"],
                    text_align="center",
                    line_height="1.4"
                ),
                spacing="2",
                align_items="center"
            ),
            spacing="4",
            align="center",
            height="100%",
            justify="center"
        ),
        style={
            "background": "rgba(255, 255, 255, 0.95)",
            "backdrop_filter": "blur(20px)", 
            "border": f"1px solid {COLORS['gray']['200']}",
            "border_radius": RADIUS["2xl"],
            "padding": SPACING["8"],
            "cursor": "pointer",
            "transition": ANIMATIONS["presets"]["button_hover"],
            "box_shadow": SHADOWS["md"],
            "_hover": {
                "transform": "translateY(-4px) scale(1.02)",
                "box_shadow": SHADOWS["2xl"],
                "border_color": card_color,
                "background": "rgba(255, 255, 255, 1)"
            }
        },
        on_click=on_click,
        width="100%",
        min_height="180px"
    )


def modern_dashboard_stat_card(
    title: str,
    value: str,
    icon: str,
    color: str,
    subtitle: str = "",
    trend: str = "up",
    trend_value: str = "",
    progress: int = 0
) -> rx.Component:
    """🎨 Tarjeta de estadística moderna para dashboard"""
    return rx.box(
        rx.vstack(
            # Header con icono animado y trend
            rx.hstack(
                # Icono con efecto pulsante
                rx.box(
                    rx.icon(icon, size=28, color="white"),
                    style={
                        "background": f"linear-gradient(135deg, {color} 0%, {color}DD 100%)",
                        "border_radius": RADIUS["2xl"],
                        "padding": SPACING["4"],
                        "box_shadow": f"0 8px 16px {color}30",
                        "animation": "pulse 3s infinite"
                    }
                ),
                rx.spacer(),
                # Trend indicator mejorado
                rx.cond(
                    trend_value != "",
                    rx.box(
                        rx.hstack(
                            rx.icon(
                                "trending-up" if trend == "up" else "trending-down",
                                size=16,
                                color="white"
                            ),
                            rx.text(
                                trend_value,
                                size="2",
                                font_weight="700",
                                color="white"
                            ),
                            spacing="1",
                            align="center"
                        ),
                        style={
                            "background": COLORS["success"]["500"] if trend == "up" else COLORS["error"]["500"],
                            "border_radius": RADIUS["full"],
                            "padding": f"{SPACING['1']} {SPACING['3']}",
                            "box_shadow": SHADOWS["sm"]
                        }
                    ),
                    rx.box()
                ),
                width="100%",
                align="center"
            ),
            
            # Valor principal con efecto brillante
            rx.text(
                value,
                style={
                    "font_size": "3rem",
                    "font_weight": "900",
                    "color": COLORS["gray"]["800"],
                    "line_height": "1",
                    "text_shadow": f"2px 2px 4px {COLORS['gray']['200']}",
                    "margin": f"{SPACING['3']} 0 {SPACING['2']} 0"
                }
            ),
            
            # Título y descripción
            rx.vstack(
                rx.text(
                    title,
                    size="4",
                    font_weight="700",
                    color=COLORS["gray"]["700"]
                ),
                rx.cond(
                    subtitle != "",
                    rx.text(
                        subtitle,
                        size="2",
                        color=COLORS["gray"]["500"],
                        text_align="center"
                    ),
                    rx.box()
                ),
                spacing="1",
                align_items="center",
                width="100%"
            ),
            
            # Barra de progreso si se proporciona
            rx.cond(
                progress > 0,
                rx.box(
                    rx.box(
                        style={
                            "width": f"{progress}%",
                            "height": "4px",
                            "background": f"linear-gradient(90deg, {color} 0%, {color}AA 100%)",
                            "border_radius": RADIUS["full"],
                            "transition": "width 1s ease-in-out"
                        }
                    ),
                    style={
                        "width": "100%",
                        "height": "4px",
                        "background": COLORS["gray"]["200"],
                        "border_radius": RADIUS["full"],
                        "overflow": "hidden"
                    }
                ),
                rx.box()
            ),
            
            spacing="5",
            align_items="center",
            width="100%",
            height="100%"
        ),
        style={
            "background": "rgba(255, 255, 255, 0.98)",
            "backdrop_filter": "blur(20px)",
            "border": f"1px solid {COLORS['gray']['200']}",
            "border_radius": RADIUS["2xl"],
            "padding": SPACING["8"],
            "box_shadow": SHADOWS["xl"],
            "transition": ANIMATIONS["presets"]["button_hover"],
            "position": "relative",
            "overflow": "hidden",
            "_hover": {
                "transform": "translateY(-6px) scale(1.02)",
                "box_shadow": SHADOWS["2xl"],
                "border_color": color
            },
            "_before": {
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "height": "4px",
                "background": f"linear-gradient(90deg, {color} 0%, {color}60 100%)",
                "border_radius": f"{RADIUS['2xl']} {RADIUS['2xl']} 0 0"
            }
        },
        width="100%",
        min_height="220px"
    )

def quick_stats_grid() -> rx.Component:   
    """📊 Grid de estadísticas principales con diseño moderno"""
    return rx.grid(
        modern_dashboard_stat_card(
            title="Total Pacientes",
            value="0",  # AppState.dashboard_stats["total_pacientes"].to_string(),
            icon="users",
            color=COLORS["primary"]["500"],
            subtitle="Pacientes registrados en el sistema",
            trend="up",
            trend_value="Sin datos",  # rx.cond(AppState.dashboard_stats["total_pacientes"] > 0, "+5 este mes", "Sin datos"),
            progress=85
        ),
        modern_dashboard_stat_card(
            title="Consultas Hoy",
            value="0",  # AppState.dashboard_stats["consultas_hoy"].to_string(),
            icon="calendar",
            color=COLORS["secondary"]["500"],
            subtitle="Consultas programadas para hoy",
            trend="up",
            trend_value="Sin consultas",  # rx.cond(AppState.dashboard_stats["consultas_hoy"] > 0, "Por atender", "Sin consultas"),
            progress=60
        ),
        modern_dashboard_stat_card(
            title="Personal Activo",
            value="0",  # AppState.dashboard_stats["personal_activo"].to_string(),
            icon="user-check",
            color=COLORS["blue"]["500"],
            subtitle="Miembros trabajando actualmente",
            trend="up",
            trend_value="Sin personal",  # rx.cond(AppState.dashboard_stats["personal_activo"] > 0, "En servicio", "Sin personal"),
            progress=100
        ),
        modern_dashboard_stat_card(
            title="Ingresos del Mes",
            value="$0",  # rx.cond(AppState.dashboard_stats["ingresos_mes"] > 0, f"${AppState.dashboard_stats['ingresos_mes']:,.0f}".replace(",", "."), "$0"),
            icon="dollar-sign",
            color=COLORS["success"]["500"],
            subtitle="Facturación del mes actual",
            trend="up",
            trend_value="Sin ingresos",  # rx.cond(AppState.dashboard_stats["ingresos_mes"] > 0, "+12%", "Sin ingresos"),
            progress=75
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="4"),  # Responsive
        spacing="8",     
        width="100%"
    )









# """
# Dashboard principal para el rol de Gerente/Jefe
# Muestra estadísticas generales y resumen del estado de la clínica
# """

# import reflex as rx
# from dental_system.components.role_specific.boss import ( 
#     loading_spinner,
#     main_header
# )
# from dental_system.components.common import stat_card, primary_button
# from dental_system.state.boss_state import BossState
# from dental_system.styles.themes import COLORS, SHADOWS, RADIUS
# from dental_system.components.charts import render_chart, custom_segmented_control,chart_toggle

# # ==========================================
# # COMPONENTES DEL DASHBOARD
# # ==========================================

# def quick_stats_grid() -> rx.Component:
#     """Grid de estadísticas rápidas - Solo 4 métricas principales"""
#     return rx.grid(
#         stat_card(
#             title="Total Pacientes",
#             value=BossState.dashboard_stats["total_pacientes"].to_string(),
#             icon="users",
#             color=COLORS["primary"]["500"],
#             trend="up",
#             trend_value=rx.cond(
#                 BossState.dashboard_stats["total_pacientes"] > 0,
#                 "Registrados",
#                 "Sin datos"
#             )
#         ),
#         stat_card(
#             title="Consultas Hoy",
#             value=BossState.dashboard_stats["consultas_hoy"].to_string(),
#             icon="calendar",
#             color=COLORS["secondary"]["500"],
#             trend="up",
#             trend_value=rx.cond(
#                 BossState.dashboard_stats["consultas_hoy"] > 0,
#                 "Programadas",
#                 "Sin consultas"
#             )
#         ),
#         stat_card(
#             title="Personal Activo",
#             value=BossState.dashboard_stats["personal_activo"].to_string(),
#             icon="user-check",
#             color=COLORS["blue"]["500"],
#             trend="up",
#             trend_value=rx.cond(
#                 BossState.dashboard_stats["personal_activo"] > 0,
#                 "En servicio",
#                 "Sin personal"
#             )
#         ),
#         stat_card(
#             title="Ingresos del Mes",
#             value=rx.cond(
#                 BossState.dashboard_stats["ingresos_mes"] > 0,
#                 f"${BossState.dashboard_stats['ingresos_mes']:,.0f}".replace(",", "."),
#                 "$0"
#             ),
#             icon="dollar-sign",
#             color=COLORS["success"],
#             trend="up",
#             trend_value=rx.cond(
#                 BossState.dashboard_stats["ingresos_mes"] > 0,
#                 "Generados",
#                 "Sin ingresos"
#             )
#         ),
#         grid_template_columns=[
#             "1fr",                  # Móvil: 1 columna
#             "repeat(1, 1fr)",       # Móvil grande: 1 columna
#             "repeat(2, 1fr)",       # Tablet: 2 columnas
#             "repeat(2, 1fr)",       # Desktop pequeño: 2 columnas  
#             "repeat(4, 1fr)",       # Desktop: 4 columnas
#         ],
        
#         spacing="6",     
#         width="100%"
#     )

# def recent_activity_card() -> rx.Component:
#     """Tarjeta de actividad reciente"""
#     return rx.box(
#         rx.vstack(
#             rx.hstack(
#                 rx.text("Actividad Reciente", size="4", weight="bold", color=COLORS["gray"]["800"]),
#                 rx.spacer(),
#                 rx.button(
#                     "Ver Todo",
#                     size="2",
#                     variant="ghost",
#                     color=COLORS["primary"]["500"]
#                 ),
#                 align="center",
#                 width="100%"
#             ),
            
#             rx.vstack(
#                 # Actividad 1
#                 rx.hstack(
#                     rx.box(
#                         rx.icon("user-plus", size=16, color="white"),
#                         background=COLORS["success"],
#                         border_radius="50%",
#                         padding="8px"
#                     ),
#                     rx.vstack(
#                         rx.text("Nuevo paciente registrado", size="2", weight="medium"),
#                         rx.text("Carlos Rodríguez - HC000156", size="2", color=COLORS["gray"]["600"]),
#                         spacing="0",
#                         align_items="start"
#                     ),
#                     rx.spacer(),
#                     rx.text("hace 2h", size="2", color=COLORS["gray"]["600"]),
#                     align="center",
#                     width="100%"
#                 ),
                
#                 # Actividad 2
#                 rx.hstack(
#                     rx.box(
#                         rx.icon("calendar-check", size=16, color="white"),
#                         background=COLORS["primary"]["500"],
#                         border_radius="50%",
#                         padding="8px"
#                     ),
#                     rx.vstack(
#                         rx.text("Consulta completada", size="3", weight="medium"),
#                         rx.text("Dra. María González - Endodoncia", size="2", color=COLORS["gray"]["600"]),
#                         spacing="0",
#                         align_items="start"
#                     ),
#                     rx.spacer(),
#                     rx.text("hace 1h", size="2", color=COLORS["gray"]["600"]),
#                     align="center",
#                     width="100%"
#                 ),
                
#                 # Actividad 3
#                 rx.hstack(
#                     rx.box(
#                         rx.icon("dollar-sign", size=16, color="white"),
#                         background=COLORS["secondary"]["500"],
#                         border_radius="50%",
#                         padding="8px"
#                     ),
#                     rx.vstack(
#                         rx.text("Pago procesado", size="3", weight="medium"),
#                         rx.text("$125.000 - Consulta General", size="2", color=COLORS["gray"]["600"]),
#                         spacing="0",
#                         align_items="start"
#                     ),
#                     rx.spacer(),
#                     rx.text("hace 30m", size="2", color=COLORS["gray"]["600"]),
#                     align="center",
#                     width="100%"
#                 ),
                
#                 spacing="4",
#                 width="100%"
#             ),
            
#             spacing="6",
#             align_items="stretch",
#             width="100%"
#         ),
#         padding="24px",
#         background="white",
#         border_radius="16px",
#         border=f"1px solid {COLORS['gray']['200']}",
#         box_shadow= SHADOWS["xl"],
#         width="100%"
#     )

# def graficas_resume() -> rx.Component:
#     """Renderiza el gráfico según la pestaña seleccionada."""
#     return rx.box(
#         rx.hstack(
#             chart_toggle(BossState),
#             custom_segmented_control(BossState),      
#         ),
#         rx.match(
#             BossState.selected_tab,
#             (
#                 "Pacientes", 
#                 render_chart(
#                     state=BossState,
#                     key="Pacientes",
#                     color="blue",
#                     gradient_id="gradient-blue"
#                 )
#             ),
#             (
#                 "Ingresos", 
#                 render_chart(
#                     state=BossState,
#                     key="Ingresos",
#                     color="green",
#                     gradient_id="gradient-green"
#                 )
#             ),
#             (
#                 "Citas", 
#                 render_chart(
#                     state=BossState,
#                     key="Citas",
#                     color="orange",
#                     gradient_id="gradient-orange"
#                 )
#             ),
#         ),
#         padding="24px",
#         background="white",
#         border_radius="16px",
#         border=f"1px solid {COLORS['gray']['200']}",
#         box_shadow= SHADOWS["xl"],
#         width="100%"
#     )

# # ==========================================
# # COMPONENTE PRINCIPAL DEL DASHBOARD
# # ==========================================

# def boss_dashboard_page() -> rx.Component:
#     """Página principal del dashboard del gerente"""
#     return rx.box(
#         # Header de la página
#         main_header(
#             "Dashboard Gerencial", 
#             "Resumen ejecutivo y métricas principales de la clínica"
#         ),
        
#         # Contenido principal
#         rx.cond(
#             BossState.is_loading,
#             loading_spinner(),
#             rx.box(
#                 # Grid de estadísticas principales
#                 quick_stats_grid(),
                
#                 # Grid de información adicional
#                 rx.grid(
#                     # Columna izquierda - Actividad reciente
                    
                    
#                     graficas_resume(),
                    
#                     # Columna derecha - Consultas del día
#                     recent_activity_card(),
#                     grid_template_columns=[
#                         "1fr",                  # Móvil: 1 columna
#                         "repeat(1, 1fr)",       # Móvil grande: 1 columna
#                         "repeat(2, 1fr)",       # Tablet: 2 columnas
#                         "repeat(2, 1fr)",       # Desktop pequeño: 2 columnas  
#                     ],
#                     margin_top="24px",
#                     spacing="6",
#                     width="100%",
                    
#                 ),
                
                
#                 spacing="6",
#                 padding="24px",
#                 width="100%",
                
#             )
#         ),
        
#         width="100%",
#         min_height="100vh",
#         background=COLORS["gray"]["50"]
#     )

# # ==========================================
# # FUNCIÓN PRINCIPAL
# # ==========================================

# def boss_dashboard() -> rx.Component:
#     """Dashboard del gerente con inicialización de datos"""
#     return rx.box(
#         boss_dashboard_page(),
#         on_mount=BossState.load_dashboard_data  # Cargar datos al montar el componente
#     )
