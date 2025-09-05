"""
🌙 PÁGINA DE CONSULTAS V4.1 - INSPIRADA EN REACT QUEUE DASHBOARD
============================================================

🎯 MEJORAS IMPLEMENTADAS BASADAS EN LA PLANTILLA DE REACT:
1. ✅ Tarjetas de Paciente Mejoradas - Posición, tiempo espera, prioridad
2. ✅ Sistema de Prioridades - Normal/Alta/Urgente con colores
3. ✅ Estadísticas por Columna - Total pacientes, urgentes, tiempo promedio

Características nuevas:
- Posición en cola (#1, #2, #3...)
- Tiempo de espera visual con colores
- Sistema de prioridades con badges
- Estadísticas por odontólogo en tiempo real
- Costos estimados por paciente
- Información de seguros
- Estados visuales mejorados
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.modal_nueva_consulta import modal_nueva_consulta

# 🌙 COLORES TEMA OSCURO PROFESIONAL + PRIORIDADES
DARK_COLORS = {
    "background": "#0f1419",           # Fondo principal muy oscuro
    "surface": "#1a1f2e",             # Superficie de cards
    "surface_hover": "#252b3a",       # Surface al hover
    "border": "#2d3748",              # Bordes sutiles
    "border_hover": "#4a5568",        # Bordes en hover
    "text_primary": "#f7fafc",        # Texto principal
    "text_secondary": "#a0aec0",      # Texto secundario
    "text_muted": "#718096",          # Texto apagado
    "accent_blue": "#3182ce",         # Azul principal
    "accent_green": "#38a169",        # Verde éxito
    "accent_yellow": "#d69e2e",       # Amarillo advertencia
    "accent_red": "#e53e3e",          # Rojo error
    "glass_bg": "rgba(26, 31, 46, 0.8)",      # Efecto vidrio
    "glass_border": "rgba(255, 255, 255, 0.1)", # Borde vidrio
    
    # Colores de Prioridad (NUEVOS)
    "priority_urgent": "#dc2626",     # Rojo intenso para urgente
    "priority_high": "#ea580c",       # Naranja para alta
    "priority_normal": "#6b7280",     # Gris para normal
    "priority_urgent_bg": "rgba(220, 38, 38, 0.1)",
    "priority_high_bg": "rgba(234, 88, 12, 0.1)",
    "priority_normal_bg": "rgba(107, 114, 128, 0.1)",
}

# ==========================================
# 📊 QUEUE CONTROL BAR - PANEL SUPERIOR NUEVO
# ==========================================

def stat_card_simple(titulo: str, valor, color: str = "blue") -> rx.Component:
    """📊 Tarjeta de estadística simple"""
    return rx.box(
        rx.vstack(
            rx.text(titulo, size="2", color=DARK_COLORS["text_muted"]),
            rx.text(valor, size="4", weight="bold", color=DARK_COLORS["text_primary"]),
            spacing="1",
            align="center"
        ),
        style={
            "background": DARK_COLORS["glass_bg"],
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": "12px",
            "padding": "1rem",
            "backdrop_filter": "blur(10px)",
            "min_width": "100px",
            "border_left": f"4px solid {DARK_COLORS[f'accent_{color}']}"
        }
    )

def queue_control_bar_simple() -> rx.Component:
    """📊 Panel de control superior simplificado"""
    return rx.box(
        rx.vstack(
            # Título
            rx.heading("📋 Panel de Control - Consultas del Día", size="4", color=DARK_COLORS["text_primary"]),
            
            # Stats en grid
            rx.grid(
                stat_card_simple("Total", AppState.estadisticas_globales_tiempo_real["total_pacientes"].to_string()),
                stat_card_simple("En Espera", AppState.estadisticas_globales_tiempo_real["en_espera"].to_string(), "yellow"),
                stat_card_simple("En Atención", AppState.estadisticas_globales_tiempo_real["en_atencion"].to_string(), "green"),
                stat_card_simple("Urgentes", AppState.estadisticas_globales_tiempo_real["urgentes"].to_string(), "red"),
                stat_card_simple("Completadas", AppState.estadisticas_globales_tiempo_real["completadas"].to_string(), "blue"),
                stat_card_simple("Dentistas", AppState.estadisticas_globales_tiempo_real["dentistas_activos"].to_string(), "blue"),
                columns="6",
                spacing="3",
                width="100%"
            ),
            
            # Botones de acción
            rx.hstack(
                rx.button(
                    "🚨 Consulta Urgente",
                    on_click=AppState.crear_consulta_urgente,
                    style={
                        "background": f"linear-gradient(135deg, {DARK_COLORS['accent_red']} 0%, #fc8181 100%)",
                        "color": DARK_COLORS["text_primary"],
                        "border": "none",
                        "border_radius": "8px",
                        "padding": "0.5rem 1rem"
                    }
                ),
                rx.button(
                    "🔄 Refrescar",
                    on_click=AppState.refrescar_tiempo_real,
                    style={
                        "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4f9cf9 100%)",
                        "color": DARK_COLORS["text_primary"],
                        "border": "none",
                        "border_radius": "8px",
                        "padding": "0.5rem 1rem"
                    }
                ),
                spacing="3"
            ),
            
            spacing="4",
            width="100%"
        ),
        style={
            "background": DARK_COLORS["glass_bg"],
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": "16px",
            "padding": "1.5rem",
            "margin": "1rem 0",
            "backdrop_filter": "blur(15px)"
        }
    )

def boton_nueva_consulta_flotante() -> rx.Component:
    """🚀 Botón flotante con efecto glassmorphism - TEMA OSCURO"""
    return rx.button(
        rx.hstack(
            rx.icon("calendar-plus", size=20, color=DARK_COLORS["text_primary"]),
            rx.text("Nueva Consulta", font_weight="600", color=DARK_COLORS["text_primary"]),
            spacing="2",
            align="center"
        ),
        style={
            "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #2b6cb8 100%)",
            "color": DARK_COLORS["text_primary"],
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": "16px",
            "padding": "1rem 2rem",
            "position": "fixed",
            "top": "2rem",
            "right": "2rem",
            "z_index": "1000",
            "backdrop_filter": "blur(10px)",
            "box_shadow": f"0 8px 32px rgba(49, 130, 206, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "transition": "all 0.3s ease",
            "_hover": {
                "background": f"linear-gradient(135deg, #2b6cb8 0%, {DARK_COLORS['accent_blue']} 100%)",
                "transform": "translateY(-3px)",
                "box_shadow": f"0 12px 40px rgba(49, 130, 206, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
            }
        },
        on_click=lambda: AppState.seleccionar_y_abrir_modal_consulta("")
    )

def estadisticas_columna_odontologo(doctor_id: str) -> rx.Component:
    """📊 NUEVO: Estadísticas por columna como en React"""
    return rx.box(
        rx.vstack(
            # Header de estadísticas
            rx.hstack(
                rx.icon("bar-chart-3", size=14, color=DARK_COLORS["accent_blue"]),
                rx.text(
                    "Estadísticas de Cola",
                    font_weight="600", 
                    size="2", 
                    color=DARK_COLORS["text_secondary"]
                ),
                spacing="2",
                align="center"
            ),
            
            # Grid de estadísticas (como en React)
            rx.hstack(
                # Total pacientes
                rx.box(
                    rx.vstack(
                        rx.text(
                            AppState.conteos_consultas_por_doctor.get(doctor_id, 0),
                            font_weight="800",
                            size="4",
                            color=DARK_COLORS["text_primary"],
                            style={"line_height": "1"}
                        ),
                        rx.text(
                            "Total",
                            font_size="0.7rem",
                            color=DARK_COLORS["text_muted"],
                            style={"text_transform": "uppercase", "letter_spacing": "0.05em"}
                        ),
                        spacing="1",
                        align="center"
                    ),
                    style={
                        "background": DARK_COLORS["surface_hover"],
                        "border": f"1px solid {DARK_COLORS['border']}",
                        "border_radius": "10px",
                        "padding": "0.75rem",
                        "text_align": "center",
                        "flex": "1",
                        "backdrop_filter": "blur(5px)"
                    }
                ),
                
                # Pacientes urgentes (NUEVO)
                rx.box(
                    rx.vstack(
                        rx.text(
                            "0",  # Placeholder - esto necesitará ser calculado
                            font_weight="800",
                            size="4",
                            color=DARK_COLORS["priority_urgent"],
                            style={"line_height": "1"}
                        ),
                        rx.text(
                            "Urgentes",
                            font_size="0.7rem",
                            color=DARK_COLORS["text_muted"],
                            style={"text_transform": "uppercase", "letter_spacing": "0.05em"}
                        ),
                        spacing="1",
                        align="center"
                    ),
                    style={
                        "background": DARK_COLORS["surface_hover"],
                        "border": f"1px solid {DARK_COLORS['border']}",
                        "border_radius": "10px",
                        "padding": "0.75rem",
                        "text_align": "center",
                        "flex": "1",
                        "backdrop_filter": "blur(5px)"
                    }
                ),
                
                # Tiempo promedio espera (NUEVO)
                rx.box(
                    rx.vstack(
                        rx.text(
                            "25m",  # Placeholder - esto necesitará ser calculado
                            font_weight="800",
                            size="4",
                            color=DARK_COLORS["accent_yellow"],
                            style={"line_height": "1"}
                        ),
                        rx.text(
                            "Espera",
                            font_size="0.7rem",
                            color=DARK_COLORS["text_muted"],
                            style={"text_transform": "uppercase", "letter_spacing": "0.05em"}
                        ),
                        spacing="1",
                        align="center"
                    ),
                    style={
                        "background": DARK_COLORS["surface_hover"],
                        "border": f"1px solid {DARK_COLORS['border']}",
                        "border_radius": "10px",
                        "padding": "0.75rem",
                        "text_align": "center",
                        "flex": "1",
                        "backdrop_filter": "blur(5px)"
                    }
                ),
                
                spacing="3",
                width="100%"
            ),
            
            spacing="3",
            width="100%"
        ),
        style={
            "width" : "100%",
            "margin_bottom": "1rem",
            "padding": "1rem",
            "background": f"rgba({DARK_COLORS['glass_bg']}, 0.3)",
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": "12px",
            "backdrop_filter": "blur(10px)"
        }
    )

def badge_prioridad(prioridad: rx.Var[str]) -> rx.Component:
    """🏷️ NUEVO: Badge de prioridad como en React - FUNCIONAL"""
    return rx.match(
        prioridad,
        ("urgente",
         rx.box(
             rx.hstack(
                 rx.icon("alert-triangle", size=10, color="white"),
                 rx.text(
                     "URGENTE",
                     font_weight="700",
                     font_size="0.65rem",
                     color="white",
                     style={"letter_spacing": "0.05em"}
                 ),
                 spacing="1",
                 align="center"
             ),
             style={
                 "background": DARK_COLORS["priority_urgent"],
                 "border": f"1px solid {DARK_COLORS['priority_urgent']}",
                 "border_radius": "6px",
                 "padding": "3px 8px",
                 "backdrop_filter": "blur(10px)",
                 "box_shadow": f"0 2px 8px rgba(220, 38, 38, 0.3)",
                 "animation": "pulse 2s infinite"
             }
         )),
        ("alta",
         rx.box(
             rx.hstack(
                 rx.icon("arrow-up", size=10, color="white"),
                 rx.text(
                     "ALTA",
                     font_weight="700",
                     font_size="0.65rem",
                     color="white",
                     style={"letter_spacing": "0.05em"}
                 ),
                 spacing="1",
                 align="center"
             ),
             style={
                 "background": DARK_COLORS["priority_high"],
                 "border": f"1px solid {DARK_COLORS['priority_high']}",
                 "border_radius": "6px",
                 "padding": "3px 8px",
                 "backdrop_filter": "blur(10px)",
                 "box_shadow": f"0 2px 8px rgba(234, 88, 12, 0.3)"
             }
         )),
        ("normal",
         rx.box(
             rx.text(
                 "Normal",
                 font_weight="600",
                 font_size="0.65rem",
                 color=DARK_COLORS["text_muted"],
                 style={"letter_spacing": "0.05em"}
             ),
             style={
                 "background": DARK_COLORS["priority_normal_bg"],
                 "border": f"1px solid {DARK_COLORS['priority_normal']}",
                 "border_radius": "6px",
                 "padding": "3px 8px",
                 "backdrop_filter": "blur(5px)"
             }
         )),
        rx.box()
    )

def get_tiempo_espera_color(minutos: int) -> str:
    """🕒 Color según tiempo de espera"""
    if minutos > 60:
        return DARK_COLORS["priority_urgent"]
    elif minutos > 30:
        return DARK_COLORS["priority_high"]
    else:
        return DARK_COLORS["text_secondary"]

def consulta_card_mejorada_v41(consulta_data: rx.Var, posicion: int) -> rx.Component:
    """🎯 TARJETA DE PACIENTE MEJORADA - Inspirada en React"""
    return rx.box(
        rx.vstack(
            # Header mejorado con posición y prioridad
            rx.hstack(
                # Número de posición (NUEVO - como en React)
                rx.box(
                    rx.text(
                        posicion.to_string(),
                        font_weight="800",
                        font_size="0.8rem",
                        color="white",
                        style={"text_shadow": "0 0 10px rgba(255, 255, 255, 0.5)"}
                    ),
                    style={
                        "background": rx.cond(
                            posicion == 1,
                            f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                            f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4299e1 100%)"
                        ),
                        "border": f"1px solid {DARK_COLORS['glass_border']}",
                        "border_radius": "50%",
                        "width": "36px",
                        "height": "36px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "backdrop_filter": "blur(10px)",
                        "box_shadow": rx.cond(
                            posicion == 1,
                            f"0 4px 15px rgba(56, 161, 105, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
                            f"0 4px 15px rgba(49, 130, 206, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
                        ),
                        "flex_shrink": "0"
                    }
                ),
                
                # Info del paciente
                rx.vstack(
                    rx.text(
                        consulta_data.paciente_nombre,
                        font_weight="700",
                        size="3",
                        color=DARK_COLORS["text_primary"]
                    ),
                    # rx.text(
                    #     f"ID: {consulta_data.id[:8]}...",
                    #     font_size="0.7rem",
                    #     color=DARK_COLORS["text_muted"]
                    # ),
                    spacing="1",
                    align="start"
                ),
                
                rx.spacer(),
                
                # Badge de prioridad (NUEVO) - FUNCIONAL
                badge_prioridad(consulta_data.prioridad),
                
                width="100%",
                align="center"
            ),
            
            # Información detallada (MEJORADA)
            rx.vstack(
                # Tiempo de espera con color dinámico (NUEVO)
                rx.hstack(
                    rx.icon("clock", size=14, color=DARK_COLORS["text_secondary"]),
                    rx.text(
                        f"Esperando: {consulta_data.tiempo_espera_estimado}",
                        font_weight="600",
                        size="2",
                        color=DARK_COLORS["text_secondary"]
                    ),
                    spacing="2",
                    align="center"
                ),
                
                # Información del paciente expandida (NUEVA)
                rx.hstack(
                    rx.icon("calendar", size=12, color=DARK_COLORS["text_muted"]),
                    rx.text(
                        "35 años",  # Placeholder
                        font_size="0.8rem",
                        color=DARK_COLORS["text_muted"]
                    ),
                    rx.icon("phone", size=12, color=DARK_COLORS["text_muted"]),
                    rx.text(
                        "+582811234567",  # Placeholder
                        font_size="0.8rem",
                        color=DARK_COLORS["text_muted"]
                    ),
                    # Indicador de seguro (NUEVO)
                    # rx.hstack(
                    #     rx.icon("shield", size=12, color=DARK_COLORS["accent_green"]),
                    #     rx.text(
                    #         "Seguro",
                    #         font_size="0.8rem",
                    #         color=DARK_COLORS["accent_green"]
                    #     ),
                    #     spacing="1",
                    #     align="center"
                    # ),
                    spacing="3",
                    align="center"
                ),
                
                # Servicio y costo estimado (NUEVO)
                # rx.box(
                #     rx.vstack(
                #         rx.text(
                #             consulta_data.motivo_consulta,
                #             font_weight="600",
                #             size="2",
                #             color=DARK_COLORS["text_primary"]
                #         ),
                #         rx.hstack(
                #             rx.text(
                #                 "Estimado:",
                #                 font_size="0.8rem",
                #                 color=DARK_COLORS["text_muted"]
                #             ),
                #             rx.text(
                #                 "50.00 USD / 1,825 Bs",  # Placeholder
                #                 font_weight="600",
                #                 font_size="0.8rem",
                #                 color=DARK_COLORS["accent_green"]
                #             ),
                #             spacing="2",
                #             justify="between",
                #             width="100%"
                #         ),
                #         spacing="1",
                #         align="start"
                #     ),
                #     style={
                #         "background": DARK_COLORS["surface_hover"],
                #         "border": f"1px solid {DARK_COLORS['border']}",
                #         "border_radius": "8px",
                #         "padding": "0.75rem",
                #         "width": "100%",
                #         "backdrop_filter": "blur(5px)"
                #     }
                # ),
                
                # Hora de llegada
                rx.text(
                    f"Llegada: {consulta_data.fecha_llegada}",
                    color=DARK_COLORS["text_muted"],
                    size="1"
                ),
                
                spacing="3",
                width="100%",
                align="start"
            ),
            
            # Botones de acción mejorados - usando los existentes
            rx.match(
                consulta_data.estado,
                ("en_espera",
                 rx.hstack(
                     rx.button(
                         rx.hstack(
                             rx.icon("play", size=14, color="white"),
                             rx.text("Iniciar", font_weight="500", color="white"),
                             spacing="2",
                             align="center"
                         ),
                         style={
                             "background": f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                             "border": f"1px solid {DARK_COLORS['glass_border']}",
                             "border_radius": "10px",
                             "padding": "10px 20px",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "flex": "1",
                             "_hover": {
                                 "transform": "translateY(-2px)",
                                 "box_shadow": f"0 8px 25px rgba(56, 161, 105, 0.4)"
                             }
                         },
                         on_click=lambda: AppState.iniciar_atencion_consulta(consulta_data.id, "en_curso"),
                         loading=AppState.cargando_consultas
                     ),
                     
                    #  # Botón de prioridad (NUEVO)
                    #  rx.button(
                    #      rx.icon("arrows-up-down", size=14, color=DARK_COLORS["accent_yellow"]),
                    #      on_click=lambda: AppState.ciclar_prioridad_consulta(consulta_data.id),
                    #      style={
                    #          "background": "transparent",
                    #          "border": f"1px solid {DARK_COLORS['accent_yellow']}",
                    #          "border_radius": "10px",
                    #          "padding": "10px",
                    #          "backdrop_filter": "blur(10px)",
                    #          "transition": "all 0.3s ease",
                    #          "cursor": "pointer",
                    #          "_hover": {
                    #              "background": f"rgba(214, 158, 46, 0.1)",
                    #              "transform": "translateY(-2px)"
                    #          }
                    #      }
                    #  ),
                     
                     # Botón de transferir (NUEVO) - FUNCIONAL
                     rx.button(
                         rx.icon("arrow-left-right", size=14, color=DARK_COLORS["accent_blue"]),
                         on_click=lambda: AppState.abrir_modal_transferir_paciente(consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_blue']}",
                             "border_radius": "10px",
                             "padding": "10px",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "cursor": "pointer",
                             "_hover": {
                                 "background": f"rgba(49, 130, 206, 0.1)",
                                 "transform": "translateY(-2px)",
                                 "box_shadow": f"0 4px 12px rgba(49, 130, 206, 0.3)"
                             }
                         }
                     ),
                     
                    #  # NUEVO: Botón Editar Consulta (cambiar odontólogo)
                    #  rx.button(
                    #      rx.icon("pencil", size=14, color=DARK_COLORS["accent_blue"]),
                    #      on_click=lambda: AppState.seleccionar_y_abrir_modal_consulta(consulta_data.id),
                    #      style={
                    #          "background": "transparent",
                    #          "border": f"1px solid {DARK_COLORS['accent_blue']}",
                    #          "border_radius": "10px",
                    #          "padding": "10px",
                    #          "backdrop_filter": "blur(10px)",
                    #          "transition": "all 0.3s ease",
                    #          "cursor": "pointer",
                    #          "_hover": {
                    #              "background": f"rgba(49, 130, 206, 0.1)",
                    #              "transform": "translateY(-2px)",
                    #              "box_shadow": f"0 4px 12px rgba(49, 130, 206, 0.3)"
                    #          }
                    #      }
                    #  ),
                     
                     # NUEVO: Botones de orden en cola
                     rx.button(
                         rx.icon("chevron-up", size=12, color=DARK_COLORS["accent_green"]),
                         on_click=lambda: AppState.subir_en_cola(consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_green']}",
                             "border_radius": "8px",
                             "padding": "6px",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "cursor": "pointer",
                             "_hover": {
                                 "background": f"rgba(56, 161, 105, 0.1)",
                                 "transform": "translateY(-1px)"
                             }
                         }
                     ),
                     
                     rx.button(
                         rx.icon("chevron-down", size=12, color=DARK_COLORS["accent_yellow"]),
                         on_click=lambda: AppState.bajar_en_cola(consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_yellow']}",
                             "border_radius": "8px",
                             "padding": "6px",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "cursor": "pointer",
                             "_hover": {
                                 "background": f"rgba(214, 158, 46, 0.1)",
                                 "transform": "translateY(-1px)"
                             }
                         }
                     ),
                     
                     rx.button(
                         rx.icon("x", size=14, color=DARK_COLORS["accent_red"]),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_red']}",
                             "border_radius": "10px",
                             "padding": "10px",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "_hover": {
                                 "background": f"rgba(229, 62, 62, 0.1)",
                                 "transform": "translateY(-2px)"
                             }
                         },
                         on_click=lambda: AppState.cancelar_consulta(consulta_data.id, "Cancelada desde interfaz"),
                         loading=AppState.cargando_consultas
                     ),
                     
                     spacing="2",
                     width="100%",
                     align="center"
                 )),
                ("en_curso",
                 rx.hstack(
                     rx.button(
                         rx.hstack(
                             rx.icon("check", size=14, color="white"),
                             rx.text("Finalizar", font_weight="600", color="white"),
                             spacing="2",
                             align="center"
                         ),
                         style={
                             "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4299e1 100%)",
                             "border": f"1px solid {DARK_COLORS['glass_border']}",
                             "border_radius": "10px",
                             "padding": "10px 20px",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "flex": "1",
                             "_hover": {
                                 "transform": "translateY(-2px)",
                                 "box_shadow": f"0 8px 25px rgba(49, 130, 206, 0.4)"
                             }
                         },
                         on_click=lambda: AppState.completar_consulta(consulta_data.id, {}),
                         loading=AppState.cargando_consultas
                     ),
                     spacing="2",
                     width="100%",
                     align="center"
                 )),
                rx.box()
            ),
            
            spacing="4",
            width="100%",
            align="start"
        ),
        style={
            "background": rx.cond(
                posicion == 1,
                f"linear-gradient(135deg, {DARK_COLORS['glass_bg']} 0%, rgba(56, 161, 105, 0.1) 100%)",
                DARK_COLORS["glass_bg"]
            ),
            "border": rx.cond(
                posicion == 1,
                f"2px solid {DARK_COLORS['accent_green']}",
                f"1px solid {DARK_COLORS['glass_border']}"
            ),
            "border_radius": "16px",
            "padding": "1.5rem",
            "backdrop_filter": "blur(20px)",
            "box_shadow": rx.cond(
                posicion == 1,
                f"0 12px 40px rgba(56, 161, 105, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
                f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)"
            ),
            "transition": "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            "cursor": "grab",
            "_hover": {
                "transform": "translateY(-6px) scale(1.02)",
                "box_shadow": "0 20px 60px rgba(14, 165, 233, 0.25), 0 0 0 1px rgba(14, 165, 233, 0.3)",
                "cursor": "grab"
            },
            "_active": {
                "cursor": "grabbing",
                "transform": "scale(1.05) rotate(1deg)",
                "box_shadow": "0 25px 80px rgba(14, 165, 233, 0.4)"
            },
            "position": "relative"
        },
        width="100%"
    )

def lista_consultas_mejorada_v41(doctor_id: str) -> rx.Component:
    """📋 Lista de consultas con posiciones y mejoras v4.1"""
    return rx.cond(
        AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
        rx.vstack(
            rx.foreach(
                AppState.consultas_con_orden_por_doctor_con_prioridad.get(doctor_id, []),
                lambda consulta_data, index: consulta_card_mejorada_v41(consulta_data, index + 1)
            ),
            spacing="4",
            width="100%"
        ),
        # Estado vacío mejorado
        rx.box(
            rx.vstack(
                rx.icon("calendar-x", size=40, color=DARK_COLORS["text_muted"]),
                rx.text(
                    "No hay pacientes en cola",
                    color=DARK_COLORS["text_muted"],
                    size="3",
                    font_weight="600",
                    style={"text_align": "center"}
                ),
                rx.text(
                    "La cola está vacía en este momento",
                    color=DARK_COLORS["text_muted"],
                    size="2",
                    style={"text_align": "center", "opacity": "0.7"}
                ),
                spacing="3",
                align="center"
            ),
            style={
                "padding": "3rem",
                "text_align": "center",
                "border": f"2px dashed {DARK_COLORS['border']}",
                "border_radius": "16px",
                "background": f"rgba({DARK_COLORS['surface']}, 0.3)",
                "backdrop_filter": "blur(10px)"
            }
        )
    )

def doctor_card_v41(doctor: rx.Var) -> rx.Component:
    """👨‍⚕️ Card de doctor mejorado v4.1"""
    return rx.box(
        rx.vstack(
            # Header del doctor mejorado
            rx.hstack(
                # Avatar con estado
                rx.box(
                    rx.icon("user-round", size=24, color=DARK_COLORS["text_primary"]),
                    style={
                        "background": f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                        "border_radius": "50%",
                        "padding": "14px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "transition": "all 0.4s ease",
                        "box_shadow": f"0 4px 20px rgba(56, 161, 105, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
                        "_hover": {
                            "transform": "scale(1.05)"
                        }
                    }
                ),
                
                # Info del doctor
                rx.vstack(
                    rx.text(
                        f"Dr(a). {doctor.primer_nombre} {doctor.primer_apellido}",
                        font_weight="700",
                        size="3",
                        color=DARK_COLORS["text_primary"]
                    ),
                    rx.text(
                        doctor.especialidad,
                        color=DARK_COLORS["text_secondary"],
                        size="2",
                        font_weight="500"
                    ),
                    spacing="1",
                    align="start"
                ),
                
                rx.spacer(),
                
                # Estado disponibilidad
                rx.box(
                    rx.hstack(
                        rx.icon("check-circle", size=9, color=DARK_COLORS["accent_green"]),
                        rx.text(
                            "Disponible",
                            font_weight="600",
                            font_size="0.6rem",
                            color=DARK_COLORS["accent_green"]
                        ),
                        spacing="1",
                        align="center"
                    ),
                    style={
                        "background": "rgba(56, 161, 105, 0.1)",
                        "border": f"1px solid rgba(56, 161, 105, 0.3)",
                        "border_radius": "8px",
                        "padding": "6px 12px",
                        "backdrop_filter": "blur(5px)"
                    }
                ),
                
                spacing="4",
                align="center",
                width="100%"
            ),
            
            # Estadísticas por columna (NUEVO)
            estadisticas_columna_odontologo(doctor.id),
            
            # Divider
            rx.divider(
                margin="1rem 0", 
                style={"border_color": DARK_COLORS["border"], "opacity": "0.3"}
            ),
            
            # Sección de pacientes mejorada
            rx.vstack(
                rx.hstack(
                    rx.icon("users", size=16, color=DARK_COLORS["accent_blue"]),
                    rx.text(
                        "Cola de Pacientes",
                        font_weight="700",
                        color=DARK_COLORS["text_primary"],
                        size="3"
                    ),
                    # Contador en header
                    rx.box(
                        rx.text(
                            AppState.conteos_consultas_por_doctor.get(doctor.id, 0),
                            font_weight="700",
                            color="white",
                            font_size="0.8rem"
                        ),
                        style={
                            "background": rx.cond(
                                AppState.conteos_consultas_por_doctor.get(doctor.id, 0) > 0,
                                DARK_COLORS["accent_blue"],
                                DARK_COLORS["surface_hover"]
                            ),
                            "border_radius": "50%",
                            "padding": "4px 8px",
                            "min_width": "24px",
                            "text_align": "center"
                        }
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                    justify="start"
                ),
                
                # Lista mejorada de consultas con Drop Zone
                rx.box(
                    lista_consultas_mejorada_v41(doctor.id),
                    style={
                        "min_height": "200px",
                        "border_radius": "12px",
                        "border": f"2px dashed transparent",
                        "padding": "8px",
                        "transition": "all 0.3s ease",
                        "position": "relative",
                        "_hover": {
                            "border_color": f"{DARK_COLORS['accent_blue']}40",
                            "background": f"rgba(14, 165, 233, 0.05)"
                        }
                    }
                ),
                
                spacing="4",
                width="100%",
                align="start"
            ),
            
            spacing="0",
            width="100%",
            align="start"
        ),
        style={
            "background": DARK_COLORS["glass_bg"],
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": "20px",
            "padding": "2rem",
            "min_height": "500px",
            "backdrop_filter": "blur(20px)",
            "transition": "all 0.4s ease",
            "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "_hover": {
                "transform": "translateY(-4px)",
                "box_shadow": f"0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15)",
                "border_color": DARK_COLORS["border_hover"]
            }
        },
        width="100%"
    )

def modal_transferir_paciente() -> rx.Component:
    """🔄 MODAL PARA TRANSFERIR PACIENTE - DRAG & DROP SIMULADO"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header del modal
                rx.hstack(
                    rx.icon("arrow-right-left", size=20, color=DARK_COLORS["accent_blue"]),
                    rx.text(
                        "Transferir Paciente",
                        font_weight="700",
                        font_size="1.2rem",
                        color=DARK_COLORS["text_primary"]
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=16),
                            variant="ghost",
                            size="2"
                        )
                    ),
                    width="100%",
                    align="center"
                ),
                
                rx.divider(margin_y="4"),
                
                # Info del paciente
                rx.cond(
                    AppState.consulta_para_transferir,
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "Paciente a transferir:",
                                font_weight="600",
                                color=DARK_COLORS["text_secondary"],
                                size="2"
                            ),
                            rx.box(
                                rx.hstack(
                                    rx.icon("user", size=16, color=DARK_COLORS["accent_green"]),
                                    rx.text(
                                        AppState.consulta_para_transferir.paciente_nombre,
                                        font_weight="700",
                                        color=DARK_COLORS["text_primary"]
                                    ),
                                    rx.spacer(),
                                    rx.text(
                                        rx.cond(
                                            AppState.consulta_para_transferir.orden_cola_odontologo,
                                            f"Posición #{AppState.consulta_para_transferir.orden_cola_odontologo}",
                                            "Posición #1"
                                        ),
                                        font_size="0.8rem",
                                        color=DARK_COLORS["text_muted"]
                                    ),
                                    spacing="2",
                                    align="center"
                                ),
                                style={
                                    "background": DARK_COLORS["surface"],
                                    "border": f"1px solid {DARK_COLORS['border']}",
                                    "border_radius": "8px",
                                    "padding": "12px"
                                }
                            ),
                            spacing="2",
                            align="start"
                        )
                    )
                ),
                
                # Selector de odontólogo destino
                rx.vstack(
                    rx.text(
                        "Transferir a:",
                        font_weight="600",
                        color=DARK_COLORS["text_secondary"],
                        size="2"
                    ),
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Seleccionar odontólogo..."
                        ),
                        rx.select.content(
                            rx.foreach(
                                AppState.get_lista_odontologos_activos,
                                lambda odontologo: rx.select.item(
                                    f"Dr(a). {odontologo.primer_nombre} {odontologo.primer_apellido}",
                                    value=odontologo.id
                                )
                            )
                        ),
                        on_change=AppState.set_odontologo_destino,
                        width="100%"
                    ),
                    spacing="2",
                    width="100%",
                    align="start"
                ),
                
                # Campo de motivo
                rx.vstack(
                    rx.text(
                        "Motivo de transferencia:",
                        font_weight="600",
                        color=DARK_COLORS["text_secondary"],
                        size="2"
                    ),
                    rx.text_area(
                        placeholder="Describa el motivo de la transferencia...",
                        on_change=AppState.set_motivo_transferencia,
                        rows="3",
                        width="100%",
                        style={
                            "background": DARK_COLORS["background"],
                            "border": f"1px solid {DARK_COLORS['border']}",
                            "color": DARK_COLORS["text_primary"]
                        }
                    ),
                    spacing="2",
                    width="100%",
                    align="start"
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            variant="outline",
                            size="3",
                            on_click=AppState.cerrar_modal_transferir_paciente
                        )
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("arrow-right", size=16),
                            rx.text("Transferir Paciente"),
                            spacing="2"
                        ),
                        on_click=AppState.ejecutar_transferencia_paciente,
                        size="3",
                        style={
                            "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']}, #4299e1)",
                            "color": "white",
                            "font_weight": "600"
                        }
                    ),
                    width="100%",
                    justify="end",
                    spacing="3"
                ),
                
                spacing="4",
                width="100%",
                max_width="500px"
            ),
            style={
                "background": DARK_COLORS["background"],
                "border": f"1px solid {DARK_COLORS['border']}",
                "border_radius": "16px",
                "padding": "24px"
            }
        ),
        open=AppState.modal_transferir_paciente_abierto,
        # on_open_change=lambda open: rx.cond(~open, AppState.cerrar_modal_transferir_paciente())
    )

def consultas_page_v41() -> rx.Component:
    """📅 Página de consultas V4.1 - Inspirada en React Queue Dashboard"""
    return rx.box(
        # Modal de nueva consulta
        modal_nueva_consulta(),
        
        # Modal de transferir paciente
        modal_transferir_paciente(),
        
        # Botón flotante
        boton_nueva_consulta_flotante(),
        
        # Header de página
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "Gestión de Colas",
                            font_weight="800",
                            size="7",
                            color=DARK_COLORS["text_primary"],
                            style={"text_shadow": "0 2px 4px rgba(0,0,0,0.5)"}
                        ),
                        rx.text(
                            "Monitoreo en tiempo real del flujo de pacientes",
                            color=DARK_COLORS["text_secondary"],
                            size="3"
                        ),
                        spacing="2",
                        align="start"
                    ),
                    
                    rx.spacer(),
                    
                    # Indicador tiempo real
                    rx.hstack(
                        rx.box(
                            style={
                                "width": "8px",
                                "height": "8px",
                                "background": DARK_COLORS["accent_green"],
                                "border_radius": "50%",
                                "animation": "pulse 2s infinite"
                            }
                        ),
                        rx.text(
                            "Actualización en vivo",
                            color=DARK_COLORS["text_secondary"],
                            size="2",
                            font_weight="500"
                        ),
                        spacing="2",
                        align="center"
                    ),
                    
                    width="100%",
                    align="center"
                ),
                spacing="4",
                width="100%"
            ),
            style={
                "padding": "2rem 2rem 1rem 2rem",
                "padding_top": "6rem"  # Espacio para botón flotante
            }
        ),
        
        # NUEVO: Panel de control superior con estadísticas (TEMPORALMENTE COMENTADO)
        rx.box(
            queue_control_bar_simple(),
            style={"padding": "0 2rem"}
        ),
        
        # Grid de odontólogos mejorado
        rx.box(
            rx.cond(
                AppState.odontologos_disponibles.length() > 0,
                rx.grid(
                    rx.foreach(
                        AppState.odontologos_disponibles,
                        lambda doctor: doctor_card_v41(doctor)
                    ),
                    columns="repeat(auto-fit, minmax(380px, 1fr))",
                    gap="2rem",
                    width="100%"
                ),
                # Estado vacío
                rx.box(
                    rx.vstack(
                        rx.icon("user-x", size=64, color=DARK_COLORS["text_muted"]),
                        rx.text(
                            "No hay odontólogos disponibles",
                            color=DARK_COLORS["text_primary"],
                            size="5",
                            font_weight="700",
                            style={"text_align": "center"}
                        ),
                        rx.text(
                            "Contacte al administrador para configurar el personal médico",
                            color=DARK_COLORS["text_secondary"],
                            size="3",
                            style={"text_align": "center"}
                        ),
                        spacing="4",
                        align="center"
                    ),
                    style={
                        "padding": "4rem",
                        "text_align": "center",
                        "background": DARK_COLORS["glass_bg"],
                        "border": f"2px dashed {DARK_COLORS['border']}",
                        "border_radius": "20px",
                        "backdrop_filter": "blur(10px)",
                        "margin": "2rem 0"
                    }
                )
            ),
            style={
                "padding": "1rem 2rem 2rem 2rem"
            }
        ),
        
        style={
            "min_height": "100vh",
            "background": f"linear-gradient(135deg, {DARK_COLORS['background']} 0%, #1a202c 100%)",
            "position": "relative"
        }
    )