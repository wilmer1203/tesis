import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, secondary_button, stat_card
from dental_system.styles.themes import COLORS
# from dental_system.components.ui.universal import (
#     universal_form,
#     universal_modal,
#     universal_table,
#     universal_search,
#     page_header,
#     universal_alert,
#     primary_button,
#     secondary_button,
#     PACIENTE_FORM_CONFIG,
#     CONSULTA_FORM_CONFIG,
#     PACIENTES_TABLE_HEADERS,
#     CONSULTAS_TABLE_HEADERS,
#     get_pacientes_table_actions,
#     get_consultas_table_actions
# )

# ==========================================
# 📊 DASHBOARD 
# ==========================================

def dashboard_page() -> rx.Component:
    """
    📊 DASHBOARD PRINCIPAL
    """
    return rx.box(
        # Header del dashboard
        page_header(
            title=f"Dashboard -  {AppState.user_role.title()}",
            subtitle=f"Resumen ejecutivo y métricas principales",
            # actions=[
            #     secondary_button(
            #         text="Actualizar",
            #         icon="refresh-ccw",
            #         on_click=lambda: _refresh_dashboard()
            #     )
            # ]
        ),
        rx.box(
            quick_stats_grid(),
             # Accesos rápidos por rol
            rx.cond(
                AppState.user_role == "gerente",
                _manager_quick_actions(),
                rx.cond(
                    AppState.user_role == "administrador",
                    _admin_quick_actions(),
                    _staff_quick_actions()
                )
            ),
            
            spacing="6",
            padding="20px",
            width="100%",
        ),
   
        # width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

def _manager_quick_actions() -> rx.Component:
    """👔 Acciones rápidas para gerente"""
    return rx.vstack(
            rx.text("Acciones Rápidas - Gerente", size="5", weight="bold", margin_bottom="4"),
            rx.grid(
                _quick_action_card("Gestionar Pacientes", "users", "Administrar pacientes", lambda: AppState.navigate_to("pacientes")),
                _quick_action_card("Ver Consultas", "calendar", "Programar citas", lambda: AppState.navigate_to("consultas")),
                _quick_action_card("Gestionar Personal", "user-plus", "Administrar empleados", lambda: AppState.navigate_to("personal")),
                _quick_action_card("Reportes", "bar-chart", "Ver estadísticas", lambda: AppState.navigate_to("reportes")),
                _quick_action_card("Pagos", "credit-card", "Gestionar pagos", lambda: AppState.navigate_to("pagos")),
                columns="4",
                spacing="4"
            ),
            width="100%",
            align_items="start"
        )
        
    

def _admin_quick_actions() -> rx.Component:
    """👤 Acciones rápidas para administrador"""
    return rx.vstack(
        rx.text("Acciones Rápidas - Administrador", size="5", weight="bold", margin_bottom="4"),
        rx.grid(
            _quick_action_card("Pacientes", "users", "Gestionar pacientes", lambda: AppState.navigate_to("pacientes")),
            _quick_action_card("Consultas", "calendar", "Administrar citas", lambda: AppState.navigate_to("consultas")),
            _quick_action_card("Pagos", "credit-card", "Gestionar pagos", lambda: AppState.navigate_to("pagos")),
            columns="3",
            spacing="4"
        ),
        width="100%",
        align_items="start"
    )

def _staff_quick_actions() -> rx.Component:
    """👥 Acciones rápidas para personal (odontólogo/asistente)"""
    return rx.vstack(
        rx.text("Acciones Rápidas", size="5", weight="bold", margin_bottom="4"),
        rx.grid(
            _quick_action_card("Ver Pacientes", "users", "Consultar pacientes", lambda: AppState.navigate_to("pacientes")),
            _quick_action_card("Mis Consultas", "calendar", "Ver mi agenda", lambda: AppState.navigate_to("consultas")),
            rx.cond(
                AppState.user_role == "odontologo",
                _quick_action_card("Odontología", "tooth", "Atender pacientes", lambda: AppState.navigate_to("odontologia")),
                rx.fragment()
            ),
            columns="3",
            spacing="4"
        ),
        width="100%",
        align_items="start"
    )

def _quick_action_card(title: str, icon: str, description: str, on_click: callable) -> rx.Component:
    """🔧 Tarjeta de acción rápida"""
    return rx.container(
        rx.vstack(
            rx.icon(icon, size=32, color="var(--teal-9)"),
            rx.text(title, size="4", weight="bold", color="gray.800"),
            rx.text(description, size="2", color="gray.600", text_align="center"),
            spacing="3",
            align="center"
        ),
        background="white",
        border="1px solid var(--gray-6)",
        border_radius="12px",
        padding="5",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)",
            "transform": "translateY(-2px)"
        },
        on_click=on_click
    )


def quick_stats_grid() -> rx.Component:   
        # Estadísticas principales
    return rx.grid(
            stat_card(
                title="Total Pacientes",
                value=AppState.dashboard_stats["total_pacientes"].to_string(),
                icon="users",
                color=COLORS["primary"]["500"],
                trend="up",
                trend_value=rx.cond(
                    AppState.dashboard_stats["total_pacientes"] > 0, # type: ignore
                    "Registrados",
                    "Sin datos"
                )
            ),
            stat_card(
                title="Consultas Hoy",
                value=AppState.dashboard_stats["consultas_hoy"].to_string(),
                icon="calendar",
                color=COLORS["secondary"]["500"],
                trend="up",
                trend_value=rx.cond(
                    AppState.dashboard_stats["consultas_hoy"] > 0, # type: ignore
                    "Programadas",
                    "Sin consultas"
                )
            ),
            stat_card(
                title="Personal Activo",
                value=AppState.dashboard_stats["personal_activo"].to_string(),
                icon="user-check",
                color=COLORS["blue"]["500"],
                trend="up",
                trend_value=rx.cond(
                    AppState.dashboard_stats["personal_activo"] > 0, # type: ignore
                    "En servicio",
                    "Sin personal"
                )
            ),
            stat_card(
                title="Ingresos del Mes",
                value=rx.cond(
                    AppState.dashboard_stats["ingresos_mes"] > 0, # type: ignore
                    f"${AppState.dashboard_stats['ingresos_mes']:,.0f}".replace(",", "."),
                    "$0"
                ),
                icon="dollar-sign",
                color=COLORS["success"]["500"],
                trend="up",
                trend_value=rx.cond(
                    AppState.dashboard_stats["ingresos_mes"] > 0, # type: ignore
                    "Generados",
                    "Sin ingresos"
                )
            ),
            grid_template_columns=[
                "1fr",                  # Móvil: 1 columna
                "repeat(1, 1fr)",       # Móvil grande: 1 columna
                "repeat(2, 1fr)",       # Tablet: 2 columnas
                "repeat(2, 1fr)",       # Desktop pequeño: 2 columnas  
                "repeat(4, 1fr)",       # Desktop: 4 columnas
            ],
            
            spacing="6",     
            width="100%"
        ),

def _refresh_dashboard():
    """🔄 Refrescar datos del dashboard"""
    # TODO: Implementar recarga de datos
    print("Refrescando dashboard...")







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
