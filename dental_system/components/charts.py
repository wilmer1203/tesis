from ..state.app_state import AppState
import reflex as rx
# =============================================
# Componentes Reutilizables
# =============================================



def chart_toggle() -> rx.Component:
    """Botón para alternar entre gráficos de área/barras."""
    return rx.icon_button(
        rx.cond(
            AppState.area_toggle,
            rx.icon("area-chart"),  # Ícono de gráfico de área
            rx.icon("bar-chart-3")  # Ícono de gráfico de barras
        ),
        on_click=AppState.toggle_areachart(),  # Alterna el estado
        variant="soft",
        color_scheme="blue"
    )
    
    
def custom_segmented_control() -> rx.Component:
    """
    🎛️ Control segmentado MEJORADO - Se adapta según el rol del usuario
    
    CAMBIOS:
    - Gerente/Admin: Pacientes, Ingresos, Citas
    - Odontólogo: Solo Citas y Ingresos por Tipo
    """
    return rx.cond(
        AppState.user_role == "odontologo",
        # 🦷 OPCIONES PARA ODONTÓLOGO
        rx.segmented_control.root(
            rx.segmented_control.item("Mis Consultas", value="Citas"),
            rx.segmented_control.item("Ingresos por Tipo", value="IngresosTipo"),
            default_value="Consultas",
            on_change=AppState.set_selected_tab,
            margin_bottom="1.5em",
            radius="full"
        ),
        # 👑 OPCIONES PARA GERENTE/ADMIN
        rx.segmented_control.root(
            rx.segmented_control.item("Pacientes", value="Pacientes"),
            rx.segmented_control.item("Ingresos", value="Ingresos"),
            rx.segmented_control.item("Consultas", value="Consultas"),
            default_value="Pacientes",
            on_change=AppState.set_selected_tab,
            margin_bottom="1.5em",
            radius="full"
        )
    )

    

def create_gradient(color: str, id: str) -> rx.Component:
    """Crea un gradiente SVG reutilizable."""
    return rx.el.svg.defs(
        rx.el.svg.linear_gradient(
            rx.el.svg.stop(offset="5%", stop_color=rx.color(color, 7), stop_opacity=0.8),
            rx.el.svg.stop(offset="95%", stop_color=rx.color(color, 7), stop_opacity=0),
            id=id,
            x1="0",
            x2="0",
            y1="0",
            y2="1",
        )
    )



def custom_tooltip(color: str, ) -> rx.Component:
    """Tooltip personalizado con sombra y borde."""
    return rx.recharts.graphing_tooltip(
        
        content_style={
            "backgroundColor": rx.color("gray", 1),
            "borderRadius": "var(--radius-2)",
            "borderWidth": "1px",
            "borderColor": rx.color(color, 7),
            "padding": "0.5rem",
            "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        },
        #separator=" : ",  # Separador entre el nombre y el valor

    )

# =============================================
# Gráfico Dinámico (Reutilizable)
# =============================================
def render_chart(key: str, color: str, gradient_id: str) -> rx.Component:
    """
    📊 Renderiza gráfico dinámico
    
    MEJORAS:
    - Verifica si hay datos antes de renderizar
    - Muestra estado de carga
    - Maneja errores gracefully
    """
    return rx.box(
        # ✅ ESTADO DE CARGA
        rx.cond(
            AppState.is_loading_chart_data,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Cargando datos...", color="gray"),
                    spacing="2"
                ),
                height="300px"
            ),
            rx.cond(
                AppState.has_chart_data,  # Solo mostrar si hay datos
                rx.cond(
                    AppState.area_toggle,
                    # 🔵 AREA CHART
                    rx.recharts.area_chart(
                        rx.recharts.area(
                            data_key=key,
                            fill=f"url(#{gradient_id})",
                            stroke=rx.color(color, 7),
                            type_="natural"
                        ),
                        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                        create_gradient(color, gradient_id),
                        custom_tooltip(color),
                        data=AppState.get_current_data,  # ✅ TU MÉTODO EXISTENTE
                        height=300,
                        width="100%"
                    ),
                    # 📊 BAR CHART
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key=key,
                            fill=rx.color(color, 7),
                            radius=[4, 4, 0, 0]
                        ),
                        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False),
                        custom_tooltip(color),
                        data=AppState.get_current_data,  # ✅ TU MÉTODO EXISTENTE
                        height=300,
                        width="100%"
                    )
                ),
                # ❌ SIN DATOS
                rx.center(
                    rx.text("📊 Sin datos disponibles", color="gray"),
                    height="300px"
                )
            )
        ),
        width="100%"
    )
    
def render_pie_chart() -> rx.Component:
    """
    🥧 NUEVO: Gráfico de torta para ingresos por tipo (solo odontólogos)
    """
    return rx.box(
        rx.cond(
            AppState.ingresos_por_tipo_data.length() > 0,
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=AppState.ingresos_por_tipo_data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    outer_radius=120,
                    fill="#8884d8",
                    label=True
                ),
                rx.recharts.tooltip(),
                rx.recharts.legend(),
                width="100%",
                height=300
            ),
            rx.center(
                rx.text("💰 Sin datos de ingresos por tipo", color="gray"),
                height="300px"
            )
        ),
        width="100%"
    )
    
# def graficas_resume() -> rx.Component:
#     """
#     📊 COMPONENTE PRINCIPAL DE GRÁFICOS - MEJORADO
    
#     MEJORAS:
#     - Botón para cargar datos reales
#     - Adaptación por rol de usuario  
#     - Mejor manejo de errores
#     - Estadísticas resumidas
#     """
#     return rx.box(
#         rx.hstack(
#             chart_toggle(),
#             custom_segmented_control(),      
#         ),
#         rx.match(
#             AppState.selected_tab,
#             (
#                 "Pacientes", 
#                 render_chart(
#                     key="Pacientes",
#                     color="blue",
#                     gradient_id="gradient-blue"
#                 )
#             ),
#             (
#                 "Ingresos", 
#                 render_chart(
#                     key="Ingresos",
#                     color="green",
#                     gradient_id="gradient-green"
#                 )
#             ),
#             (
#                 "Citas", 
#                 render_chart(
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

def graficas_resume() -> rx.Component:
    """
    📊 COMPONENTE PRINCIPAL DE GRÁFICOS - MEJORADO
    
    MEJORAS:
    - Botón para cargar datos reales
    - Adaptación por rol de usuario  
    - Mejor manejo de errores
    - Estadísticas resumidas
    """
    return rx.vstack(
        # 🎮 CONTROLES SUPERIORES
        rx.hstack(
            rx.hstack(
                chart_toggle(),
                custom_segmented_control(),
                spacing="3"
            ),
            rx.spacer(),
            # ✅ BOTÓN PARA CARGAR DATOS REALES (reemplaza randomize_data)
            rx.button(
                rx.cond(
                    AppState.is_loading_chart_data,
                    rx.hstack(
                        rx.spinner(size="1"),
                        rx.text("Cargando..."),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.icon("refresh-cw"),
                        rx.text("Actualizar Datos"),
                        spacing="2"
                    )
                ),
                on_click=AppState.load_chart_data,  # ✅ CAMBIO PRINCIPAL
                variant="soft",
                color_scheme="blue",
                disabled=AppState.is_loading_chart_data
            ),
            width="100%",
            align="center"
        ),
        
        # # 📊 ESTADÍSTICAS RÁPIDAS (NUEVO)
        # rx.cond(
        #     AppState.user_role.in_(["gerente", "administrador"]),
        #     rx.hstack(
        #         rx.stat(
        #             rx.stat_label("📅 Consultas (30d)"),
        #             rx.stat_number(AppState.total_consultas_30_dias),
        #             rx.stat_help_text("Últimos 30 días")
        #         ),
        #         rx.stat(
        #             rx.stat_label("👥 Pacientes Nuevos (30d)"),
        #             rx.stat_number(AppState.total_pacientes_nuevos_30_dias),
        #             rx.stat_help_text("Últimos 30 días")
        #         ),
        #         rx.stat(
        #             rx.stat_label("💰 Ingresos (30d)"),
        #             rx.stat_number(f"${AppState.total_ingresos_30_dias:,.0f}"),
        #             rx.stat_help_text("Últimos 30 días")
        #         ),
        #         spacing="6",
        #         width="100%"
        #     )
        # ),
        
        # # ❌ MOSTRAR ERRORES SI LOS HAY
        # rx.cond(
        #     AppState.chart_data_error != "",
        #     rx.callout(
        #         rx.callout_icon(tag="triangle_alert"),
        #         rx.callout_text(AppState.chart_data_error),
        #         color_scheme="red"
        #     )
        # ),
        
        # 📊 GRÁFICOS PRINCIPALES
        rx.match(
            AppState.selected_tab,
            (
                "Pacientes", 
                render_chart(
                    key="Pacientes",
                    color="blue",
                    gradient_id="gradient-blue"
                )
            ),
            (
                "Ingresos", 
                render_chart(
                    key="Ingresos",
                    color="green",
                    gradient_id="gradient-green"
                )
            ),
            (
                "Consultas", 
                render_chart(
                    key="Consultas",  # Funciona tanto para 'Consultas' como 'Consultas'
                    color="orange",
                    gradient_id="gradient-orange"
                )
            ),
            # 🦷 NUEVO: Gráfico específico para odontólogos
            (
                "IngresosTipo",
                render_pie_chart()  # Gráfico de torta
            ),
        ),
        
        padding="24px",
        background="white",
        border_radius="16px",
        border=f"1px solid {rx.color('gray', 4)}",  # Usando rx.color en lugar de COLORS
        box_shadow="0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",  # Inline shadow
        width="100%",
        spacing="4"
    )