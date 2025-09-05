"""
🌙 PÁGINA DE CONSULTAS - TEMA OSCURO PROFESIONAL
===============================================

🎯 Diseño completamente renovado con tema oscuro:
- Cards individuales por odontólogo con glassmorphism
- Sistema de orden de llegada (NO citas)
- Funcionalidad dinámica con servicios reales
- Responsive design (Desktop + Mobile)
- Sidebar con resumen del día
- Tema oscuro profesional con efectos avanzados

Reemplaza el diseño de tabla tradicional
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.modal_nueva_consulta import modal_nueva_consulta

# 🌙 COLORES TEMA OSCURO PROFESIONAL
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
}

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

def doctor_card_dinamico(doctor: rx.Var) -> rx.Component:
    """🌙 Card dinámico de doctor con glassmorphism - TEMA OSCURO"""
    return rx.box(
        rx.vstack(
            # Header del doctor con tema oscuro
            rx.hstack(
                # Avatar con estado disponible y glow effect
                rx.box(
                    rx.icon("user-round", size=24, color=DARK_COLORS["text_primary"]),
                    style={
                        "background": rx.cond(
                            AppState.metricas_avanzadas_por_doctor.get(doctor.id, {}).get("disponible", True),
                            f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                            f"linear-gradient(135deg, {DARK_COLORS['accent_red']} 0%, #fc8181 100%)"
                        ),
                        "border_radius": "50%",
                        "padding": "14px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "transition": "all 0.4s ease",
                        "box_shadow": rx.cond(
                            AppState.metricas_avanzadas_por_doctor.get(doctor.id, {}).get("disponible", True),
                            f"0 4px 20px rgba(56, 161, 105, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
                            f"0 4px 20px rgba(229, 62, 62, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
                        ),
                        "_hover": {
                            "transform": "scale(1.05)",
                            "box_shadow": rx.cond(
                                AppState.metricas_avanzadas_por_doctor.get(doctor.id, {}).get("disponible", True),
                                f"0 6px 25px rgba(56, 161, 105, 0.5)",
                                f"0 6px 25px rgba(229, 62, 62, 0.5)"
                            )
                        }
                    }
                ),
                
                # Info del doctor con tema oscuro
                rx.vstack(
                    rx.text(
                         f"{doctor.primer_nombre} {doctor.primer_apellido}",
                        font_weight="700",
                        size="4",
                        color=DARK_COLORS["text_primary"],
                        style={"text_shadow": "0 2px 4px rgba(0,0,0,0.5)"}
                    ),
                    rx.text(
                        doctor.especialidad,
                        color=DARK_COLORS["text_secondary"],
                        size="2",
                        font_weight="500"
                    ),
                    # Indicador de carga de trabajo con glassmorphism
                    rx.box(
                        rx.text(
                            AppState.metricas_avanzadas_por_doctor.get(doctor.id, {}).get("carga_trabajo", "Baja"),
                            style={
                                "font_size": "0.75rem",
                                "font_weight": "700",
                                "color": DARK_COLORS["text_primary"],
                                "text_transform": "uppercase",
                                "letter_spacing": "0.05em"
                            }
                        ),
                        style={
                            "background": rx.cond(
                                AppState.metricas_avanzadas_por_doctor.get(doctor.id, {}).get("carga_trabajo", "Baja") == "Alta",
                                f"linear-gradient(135deg, {DARK_COLORS['accent_red']} 0%, rgba(229, 62, 62, 0.8) 100%)",
                                rx.cond(
                                    AppState.metricas_avanzadas_por_doctor.get(doctor.id, {}).get("carga_trabajo", "Baja") == "Media",
                                    f"linear-gradient(135deg, {DARK_COLORS['accent_yellow']} 0%, rgba(214, 158, 46, 0.8) 100%)",
                                    f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, rgba(56, 161, 105, 0.8) 100%)"
                                )
                            ),
                            "border": f"1px solid {DARK_COLORS['glass_border']}",
                            "border_radius": "8px",
                            "padding": "4px 8px",
                            "backdrop_filter": "blur(10px)"
                        }
                    ),
                    spacing="2",
                    align="start"
                ),
                
                rx.spacer(),
                
                # Badge dinámico mejorado
                badge_consultas_dinamico_fase3_dark(doctor.id),
                
                spacing="4",
                align="center",
                width="100%"
            ),
            
            # Divider con tema oscuro
            rx.divider(
                margin="1.5rem 0", 
                style={
                    "border_color": DARK_COLORS["border"],
                    "opacity": "0.3"
                }
            ),
            
            # Sección de pacientes con tema oscuro
            rx.vstack(
                rx.hstack(
                    rx.icon("users", size=16, color=DARK_COLORS["accent_blue"]),
                    rx.text(
                        "Cola de Pacientes",
                        font_weight="700",
                        color=DARK_COLORS["text_primary"],
                        size="3"
                    ),
                    spacing="2",
                    align="center"
                ),
                
                # Lista dinámica de consultas del doctor
                lista_consultas_doctor_dinamica_dark(doctor.id),
                
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
            "min_height": "400px",
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

def badge_consultas_dinamico(doctor_id: str) -> rx.Component:
    """🏷️ Badge dinámico con conteo real"""
    return rx.box(
        rx.text(
            AppState.conteos_consultas_por_doctor.get(doctor_id, 0),
            style={
                "color": "white",
                "font_weight": "700",
                "font_size": "0.9rem"
            }
        ),
        style={
            "background": rx.cond(
                AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
                "#f59e0b",  # Amarillo si hay consultas
                "#9ca3af"   # Gris si no hay consultas
            ),
            "border_radius": "50%",
            "padding": "6px 10px",
            "min_width": "28px",
            "text_align": "center",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center"
        }
    )

def badge_consultas_dinamico_fase3(doctor_id: str) -> rx.Component:
    """🏷️ Badge avanzado con métricas - Fase 3"""
    return rx.vstack(
        # Contador principal
        rx.box(
            rx.text(
                AppState.conteos_consultas_por_doctor.get(doctor_id, 0),
                style={
                    "color": "white",
                    "font_weight": "800",
                    "font_size": "1.1rem",
                    "line_height": "1"
                }
            ),
            style={
                "background": rx.cond(
                    AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 3,
                    "#ef4444",  # Rojo si más de 3
                    rx.cond(
                        AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
                        "#f59e0b",  # Amarillo si hay consultas
                        "#9ca3af"   # Gris si no hay consultas
                    )
                ),
                "border_radius": "12px",
                "padding": "8px 12px",
                "min_width": "36px",
                "text_align": "center",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
                "transition": "all 0.3s ease"
            }
        ),
        # Label descriptivo
        rx.text(
            rx.cond(
                AppState.conteos_consultas_por_doctor.get(doctor_id, 0) == 0,
                "Sin cola",
                rx.cond(
                    AppState.conteos_consultas_por_doctor.get(doctor_id, 0) == 1,
                    "1 paciente",
                    f"{AppState.conteos_consultas_por_doctor.get(doctor_id, 0)} pacientes"
                )
            ),
            style={
                "font_size": "0.6rem",
                "color": "#6b7280",
                "font_weight": "500",
                "text_align": "center",
                "line_height": "1"
            }
        ),
        spacing="1",
        align="center"
    )

def badge_consultas_dinamico_fase3_dark(doctor_id: str) -> rx.Component:
    """🌙 Badge avanzado con glassmorphism - TEMA OSCURO"""
    return rx.vstack(
        # Contador principal con efecto glow
        rx.box(
            rx.text(
                AppState.conteos_consultas_por_doctor.get(doctor_id, 0),
                style={
                    "color": DARK_COLORS["text_primary"],
                    "font_weight": "800",
                    "font_size": "1.2rem",
                    "line_height": "1",
                    "text_shadow": "0 0 10px rgba(255, 255, 255, 0.5)"
                }
            ),
            style={
                "background": rx.cond(
                    AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 3,
                    f"linear-gradient(135deg, {DARK_COLORS['accent_red']} 0%, #fc8181 100%)",
                    rx.cond(
                        AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
                        f"linear-gradient(135deg, {DARK_COLORS['accent_yellow']} 0%, #f6e05e 100%)",
                        f"linear-gradient(135deg, {DARK_COLORS['border']} 0%, {DARK_COLORS['surface_hover']} 100%)"
                    )
                ),
                "border": f"1px solid {DARK_COLORS['glass_border']}",
                "border_radius": "16px",
                "padding": "10px 14px",
                "min_width": "44px",
                "text_align": "center",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "backdrop_filter": "blur(10px)",
                "box_shadow": rx.cond(
                    AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
                    "0 4px 20px rgba(214, 158, 46, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
                    "0 4px 20px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)"
                ),
                "transition": "all 0.3s ease",
                "_hover": {
                    "transform": "scale(1.05)",
                    "box_shadow": rx.cond(
                        AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
                        "0 6px 25px rgba(214, 158, 46, 0.4)",
                        "0 6px 25px rgba(0, 0, 0, 0.3)"
                    )
                }
            }
        ),
        # Label descriptivo con tema oscuro
        rx.text(
            rx.cond(
                AppState.conteos_consultas_por_doctor.get(doctor_id, 0) == 0,
                "Sin cola",
                rx.cond(
                    AppState.conteos_consultas_por_doctor.get(doctor_id, 0) == 1,
                    "1 paciente",
                    f"{AppState.conteos_consultas_por_doctor.get(doctor_id, 0)} pacientes"
                )
            ),
            style={
                "font_size": "0.65rem",
                "color": DARK_COLORS["text_muted"],
                "font_weight": "600",
                "text_align": "center",
                "line_height": "1",
                "text_transform": "uppercase",
                "letter_spacing": "0.05em"
            }
        ),
        spacing="2",
        align="center"
    )

def lista_consultas_doctor_dinamica_dark(doctor_id: str) -> rx.Component:
    """🌙 Lista dinámica de consultas - TEMA OSCURO"""
    return rx.cond(
        AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
        rx.vstack(
            rx.foreach(
                AppState.consultas_con_orden_por_doctor.get(doctor_id, []),
                lambda consulta_data: consulta_card_con_orden_dark(consulta_data)
            ),
            spacing="3",
            width="100%"
        ),
        # Estado vacío con tema oscuro
        rx.box(
            rx.vstack(
                rx.icon("calendar-x", size=32, color=DARK_COLORS["text_muted"]),
                rx.text(
                    "No hay pacientes en cola",
                    color=DARK_COLORS["text_muted"],
                    size="2",
                    style={
                        "font_style": "italic", 
                        "text_align": "center",
                        "font_weight": "500"
                    }
                ),
                rx.text(
                    "La cola está vacía",
                    color=DARK_COLORS["text_muted"],
                    size="1",
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
                "background": f"rgba({DARK_COLORS['surface']}, 0.3)"
            }
        )
    )

def consulta_card_con_orden_dark(consulta_data: rx.Var) -> rx.Component:
    """🌙 Card de consulta con glassmorphism - TEMA OSCURO"""
    return rx.box(
        rx.vstack(
            # Header con orden real y efectos oscuros
            rx.hstack(
                # Número de orden REAL con glow
                rx.box(
                    rx.text(
                        consulta_data.numero_turno_display,
                        style={
                            "color": DARK_COLORS["text_primary"],
                            "font_weight": "800",
                            "font_size": "0.9rem",
                            "text_shadow": "0 0 10px rgba(255, 255, 255, 0.5)"
                        }
                    ),
                    style={
                        "background": rx.cond(
                            consulta_data.es_siguiente,
                            f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                            f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4299e1 100%)"
                        ),
                        "border": f"1px solid {DARK_COLORS['glass_border']}",
                        "border_radius": "10px",
                        "padding": "6px 10px",
                        "min_width": "36px",
                        "text_align": "center",
                        "backdrop_filter": "blur(10px)",
                        "box_shadow": rx.cond(
                            consulta_data.es_siguiente,
                            f"0 4px 15px rgba(56, 161, 105, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
                            f"0 4px 15px rgba(49, 130, 206, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
                        )
                    }
                ),
                
                # Indicador de siguiente con tema oscuro
                rx.cond(
                    consulta_data.es_siguiente,
                    rx.box(
                        rx.hstack(
                            rx.icon("arrow-right", size=10, color=DARK_COLORS["accent_green"]),
                            rx.text(
                                "SIGUIENTE",
                                style={
                                    "color": DARK_COLORS["accent_green"],
                                    "font_weight": "700",
                                    "font_size": "0.65rem",
                                    "letter_spacing": "0.05em"
                                }
                            ),
                            spacing="1",
                            align="center"
                        ),
                        style={
                            "background": f"rgba(56, 161, 105, 0.1)",
                            "border": f"1px solid rgba(56, 161, 105, 0.3)",
                            "border_radius": "6px",
                            "padding": "3px 8px",
                            "backdrop_filter": "blur(5px)"
                        }
                    ),
                    rx.box()
                ),
                
                rx.spacer(),
                
                # Estado badge oscuro
                estado_badge_dinamico_dark(consulta_data.consulta.estado),
                
                width="100%",
                align="center"
            ),
            
            # Info del paciente con tema oscuro
            rx.text(
                consulta_data.paciente_nombre,
                font_weight="700",
                color=DARK_COLORS["text_primary"],
                size="3"
            ),
            
            # Tiempo de espera con icono
            rx.hstack(
                rx.icon("clock", size=14, color=DARK_COLORS["accent_yellow"]),
                rx.text(
                    consulta_data.tiempo_espera_estimado,
                    color=DARK_COLORS["text_secondary"],
                    size="2",
                    font_weight="600"
                ),
                spacing="2",
                align="center"
            ),
            
            # Motivo con tema oscuro
            rx.cond(
                consulta_data.motivo_consulta != "",
                rx.text(
                    consulta_data.motivo_consulta,
                    color=DARK_COLORS["text_muted"],
                    size="2",
                    style={"font_style": "italic"}
                ),
                rx.box()
            ),
            
            # Hora de llegada
            rx.text(
                f"🕒 Llegada: {consulta_data.consulta.hora_display}",
                color=DARK_COLORS["text_muted"],
                size="1"
            ),
            
            # Botones de acción oscuros
            botones_accion_dark(consulta_data.consulta),
            
            spacing="3",
            width="100%",
            align="start"
        ),
        style={
            "background": rx.cond(
                consulta_data.es_siguiente,
                f"linear-gradient(135deg, {DARK_COLORS['glass_bg']} 0%, rgba(56, 161, 105, 0.1) 100%)",
                DARK_COLORS["glass_bg"]
            ),
            "border": rx.cond(
                consulta_data.es_siguiente,
                f"2px solid {DARK_COLORS['accent_green']}",
                f"1px solid {DARK_COLORS['glass_border']}"
            ),
            "border_radius": "16px",
            "padding": "1.25rem",
            "backdrop_filter": "blur(20px)",
            "box_shadow": rx.cond(
                consulta_data.es_siguiente,
                f"0 8px 32px rgba(56, 161, 105, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
                f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)"
            ),
            "transition": "all 0.4s ease",
            "_hover": {
                "transform": "translateY(-2px)",
                "border_color": DARK_COLORS["border_hover"],
                "box_shadow": f"0 12px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)"
            }
        },
        width="100%"
    )

def estado_badge_dinamico_dark(estado: rx.Var[str]) -> rx.Component:
    """🌙 Badge de estado con tema oscuro"""
    return rx.match(
        estado,
        ("programada", 
         rx.box(
             rx.hstack(
                 rx.icon("clock", size=10, color=DARK_COLORS["accent_yellow"]),
                 rx.text("En Espera", style={"color": DARK_COLORS["accent_yellow"], "font_weight": "600", "font_size": "0.7rem"}),
                 spacing="1",
                 align="center"
             ),
             style={
                 "background": f"rgba(214, 158, 46, 0.2)", 
                 "border": f"1px solid rgba(214, 158, 46, 0.4)", 
                 "border_radius": "8px", 
                 "padding": "4px 8px",
                 "backdrop_filter": "blur(10px)"
             }
         )),
        ("en_curso",
         rx.box(
             rx.hstack(
                 rx.icon("activity", size=10, color=DARK_COLORS["accent_blue"]),
                 rx.text("Atendiendo", style={"color": DARK_COLORS["accent_blue"], "font_weight": "600", "font_size": "0.7rem"}),
                 spacing="1",
                 align="center"
             ),
             style={
                 "background": f"rgba(49, 130, 206, 0.2)", 
                 "border": f"1px solid rgba(49, 130, 206, 0.4)", 
                 "border_radius": "8px", 
                 "padding": "4px 8px",
                 "backdrop_filter": "blur(10px)",
                 "animation": "pulse 2s infinite"
             }
         )),
        rx.box()
    )

def botones_accion_dark(consulta: rx.Var) -> rx.Component:
    """🌙 Botones de acción con tema oscuro"""
    return rx.match(
        consulta.estado,
        ("programada",
         rx.hstack(
             rx.button(
                 rx.hstack(
                     rx.icon("play", size=12, color=DARK_COLORS["text_primary"]),
                     rx.text("Iniciar", font_weight="600", color=DARK_COLORS["text_primary"]),
                     spacing="1",
                     align="center"
                 ),
                 size="2",
                 style={
                     "background": f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                     "border": f"1px solid {DARK_COLORS['glass_border']}",
                     "border_radius": "10px",
                     "padding": "8px 16px",
                     "backdrop_filter": "blur(10px)",
                     "transition": "all 0.3s ease",
                     "_hover": {
                         "transform": "translateY(-2px)",
                         "box_shadow": f"0 8px 25px rgba(56, 161, 105, 0.4)"
                     }
                 },
                 on_click=lambda: AppState.iniciar_atencion_consulta(consulta.id, "en_curso"),
                 loading=AppState.cargando_consultas
             ),
             rx.button(
                 rx.icon("x", size=12, color=DARK_COLORS["accent_red"]),
                 size="2",
                 style={
                     "background": "transparent",
                     "border": f"1px solid {DARK_COLORS['accent_red']}",
                     "border_radius": "10px",
                     "padding": "8px",
                     "backdrop_filter": "blur(10px)",
                     "transition": "all 0.3s ease",
                     "_hover": {
                         "background": f"rgba(229, 62, 62, 0.1)",
                         "transform": "translateY(-2px)"
                     }
                 },
                 on_click=lambda: AppState.cancelar_consulta(consulta.id, "Cancelada desde interfaz"),
                 loading=AppState.cargando_consultas
             ),
             spacing="2",
             width="100%"
         )),
        ("en_curso",
         rx.hstack(
             rx.button(
                 rx.hstack(
                     rx.icon("check", size=12, color=DARK_COLORS["text_primary"]),
                     rx.text("Finalizar", font_weight="600", color=DARK_COLORS["text_primary"]),
                     spacing="1",
                     align="center"
                 ),
                 size="2",
                 style={
                     "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4299e1 100%)",
                     "border": f"1px solid {DARK_COLORS['glass_border']}",
                     "border_radius": "10px",
                     "padding": "8px 16px",
                     "backdrop_filter": "blur(10px)",
                     "transition": "all 0.3s ease",
                     "_hover": {
                         "transform": "translateY(-2px)",
                         "box_shadow": f"0 8px 25px rgba(49, 130, 206, 0.4)"
                     }
                 },
                 on_click=lambda: AppState.completar_consulta(consulta.id, {}),
                 loading=AppState.cargando_consultas
             ),
             rx.button(
                 rx.icon("pause", size=12, color=DARK_COLORS["accent_yellow"]),
                 size="2",
                 style={
                     "background": "transparent",
                     "border": f"1px solid {DARK_COLORS['accent_yellow']}",
                     "border_radius": "10px",
                     "padding": "8px",
                     "backdrop_filter": "blur(10px)",
                     "transition": "all 0.3s ease",
                     "_hover": {
                         "background": f"rgba(214, 158, 46, 0.1)",
                         "transform": "translateY(-2px)"
                     }
                 },
                 on_click=lambda: AppState.actualizar_estado_consulta_intervencion(consulta.id, "programada"),
                 loading=AppState.cargando_consultas
             ),
             spacing="2",
             width="100%"
         )),
        rx.box()
    )

def lista_consultas_doctor_dinamica(doctor_id: str) -> rx.Component:
    """📋 Lista dinámica de consultas con orden REAL"""
    return rx.cond(
        AppState.conteos_consultas_por_doctor.get(doctor_id, 0) > 0,
        rx.vstack(
            rx.foreach(
                AppState.consultas_con_orden_por_doctor.get(doctor_id, []),
                lambda consulta_data: consulta_card_con_orden_real(consulta_data)
            ),
            spacing="2",
            width="100%"
        ),
        # Estado vacío
        rx.box(
            rx.vstack(
                rx.icon("calendar-x", size=24, color="#9ca3af"),
                rx.text(
                    "No hay pacientes en cola",
                    color="#9ca3af",
                    size="2",
                    style={"font_style": "italic", "text_align": "center"}
                ),
                spacing="2",
                align="center"
            ),
            style={"padding": "2rem", "text_align": "center"}
        )
    )

def consulta_card_con_orden_real(consulta_data: rx.Var) -> rx.Component:
    """👤 Card de consulta con orden REAL calculado - FASE 3"""
    return rx.box(
        rx.vstack(
            # Header con orden real y indicadores avanzados
            rx.hstack(
                # Número de orden REAL
                rx.box(
                    rx.text(
                        consulta_data.numero_turno_display,
                        style={
                            "color": "white",
                            "font_weight": "800",
                            "font_size": "0.8rem"
                        }
                    ),
                    style={
                        "background": rx.cond(
                            consulta_data.es_siguiente,
                            "#10b981",  # Verde si es el siguiente
                            "#2563eb"   # Azul normal
                        ),
                        "border_radius": "6px",
                        "padding": "4px 8px",
                        "min_width": "32px",
                        "text_align": "center",
                        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
                    }
                ),
                
                # Indicador de siguiente
                rx.cond(
                    consulta_data.es_siguiente,
                    rx.box(
                        rx.text(
                            "SIGUIENTE",
                            style={
                                "color": "#10b981",
                                "font_weight": "700",
                                "font_size": "0.6rem",
                                "letter_spacing": "0.05em"
                            }
                        ),
                        style={
                            "background": "rgba(16, 185, 129, 0.1)",
                            "border": "1px solid rgba(16, 185, 129, 0.3)",
                            "border_radius": "4px",
                            "padding": "2px 6px"
                        }
                    ),
                    rx.box()
                ),
                
                rx.spacer(),
                
                # Estado badge mejorado
                estado_badge_dinamico_fase3(consulta_data.consulta.estado),
                
                width="100%",
                align="center"
            ),
            
            # Info del paciente
            rx.text(
                consulta_data.paciente_nombre,
                font_weight="600",
                color="#111827",
                size="2"
            ),
            
            # Tiempo de espera estimado - NUEVA FUNCIONALIDAD
            rx.hstack(
                rx.icon("clock", size=12, color="#6b7280"),
                rx.text(
                    consulta_data.tiempo_espera_estimado,
                    color="#6b7280",
                    size="1",
                    font_weight="500"
                ),
                spacing="1",
                align="center"
            ),
            
            # Motivo (si existe)
            rx.cond(
                consulta_data.motivo_consulta != "",
                rx.text(
                    consulta_data.motivo_consulta,
                    color="#6b7280",
                    size="1",
                    style={"font_style": "italic"}
                ),
                rx.box()
            ),
            
            # Hora de llegada
            rx.text(
                f"Llegada: {consulta_data.consulta.hora_display}",
                color="#9ca3af",
                size="1"
            ),
            
            # Botones de acción funcionales
            botones_accion_funcionales_fase3(consulta_data.consulta),
            
            spacing="2",
            width="100%",
            align="start"
        ),
        style={
            "background": rx.cond(
                consulta_data.es_siguiente,
                "#f0fdf4",  # Fondo verde claro si es el siguiente
                "#f9fafb"   # Fondo normal
            ),
            "border": rx.cond(
                consulta_data.es_siguiente, 
                "2px solid #10b981",  # Borde verde si es el siguiente
                "1px solid #e5e7eb"   # Borde normal
            ),
            "border_radius": "12px",
            "padding": "1rem",
            "transition": "all 0.3s ease",
            "_hover": {
                "background": "white",
                "border_color": "#2563eb",
                "box_shadow": "0 4px 12px rgba(37, 99, 235, 0.15)",
                "transform": "translateY(-1px)"
            }
        },
        width="100%"
    )

def estado_badge_dinamico(estado: rx.Var[str]) -> rx.Component:
    """🏷️ Badge de estado con colores dinámicos"""
    return rx.match(
        estado,
        ("programada", 
         rx.box(
             rx.text("En Espera", style={"color": "#f59e0b", "font_weight": "600", "font_size": "0.7rem"}),
             style={"background": "rgba(245, 158, 11, 0.1)", "border": "1px solid rgba(245, 158, 11, 0.3)", "border_radius": "4px", "padding": "2px 6px"}
         )),
        ("en_curso",
         rx.box(
             rx.text("En Proceso", style={"color": "#2563eb", "font_weight": "600", "font_size": "0.7rem"}),
             style={"background": "rgba(37, 99, 235, 0.1)", "border": "1px solid rgba(37, 99, 235, 0.3)", "border_radius": "4px", "padding": "2px 6px"}
         )),
        rx.box()  # Default case
    )

def estado_badge_dinamico_fase3(estado: rx.Var[str]) -> rx.Component:
    """🏷️ Badge de estado mejorado - Fase 3"""
    return rx.match(
        estado,
        ("programada", 
         rx.box(
             rx.hstack(
                 rx.icon("clock", size=10, color="#f59e0b"),
                 rx.text("En Espera", style={"color": "#f59e0b", "font_weight": "600", "font_size": "0.7rem"}),
                 spacing="1",
                 align="center"
             ),
             style={
                 "background": "rgba(245, 158, 11, 0.1)", 
                 "border": "1px solid rgba(245, 158, 11, 0.3)", 
                 "border_radius": "6px", 
                 "padding": "3px 8px"
             }
         )),
        ("en_curso",
         rx.box(
             rx.hstack(
                 rx.icon("activity", size=10, color="#2563eb"),
                 rx.text("Atendiendo", style={"color": "#2563eb", "font_weight": "600", "font_size": "0.7rem"}),
                 spacing="1",
                 align="center"
             ),
             style={
                 "background": "rgba(37, 99, 235, 0.1)", 
                 "border": "1px solid rgba(37, 99, 235, 0.3)", 
                 "border_radius": "6px", 
                 "padding": "3px 8px",
                 "animation": "pulse 2s infinite"
             }
         )),
        rx.box()  # Default case
    )

def botones_accion_funcionales(consulta: rx.Var) -> rx.Component:
    """⚡ Botones de acción conectados con servicios reales"""
    return rx.match(
        consulta.estado,
        ("programada",
         # Consulta en espera - puede iniciar o cancelar
         rx.hstack(
             rx.button(
                 "▶️ Iniciar",
                 size="1",
                 style={
                     "background": "#10b981",
                     "color": "white",
                     "font_size": "0.7rem",
                     "padding": "4px 8px",
                     "_hover": {"background": "#059669"}
                 },
                 on_click=lambda: AppState.iniciar_atencion_consulta(consulta.id, "en_curso"),
                 loading=AppState.cargando_consultas
             ),
             rx.button(
                 "❌",
                 size="1",
                 style={
                     "background": "transparent",
                     "color": "#ef4444",
                     "border": "1px solid #ef4444",
                     "font_size": "0.7rem",
                     "padding": "4px 6px",
                     "_hover": {"background": "rgba(239, 68, 68, 0.1)"}
                 },
                 on_click=lambda: AppState.cancelar_consulta(consulta.id, "Cancelada desde interfaz"),
                 loading=AppState.cargando_consultas
             ),
             spacing="1",
             width="100%"
         )),
        ("en_curso",
         # Consulta en proceso - puede finalizar o pausar
         rx.hstack(
             rx.button(
                 "✅ Finalizar",
                 size="1",
                 style={
                     "background": "#2563eb",
                     "color": "white",
                     "font_size": "0.7rem",
                     "padding": "4px 8px",
                     "_hover": {"background": "#1d4ed8"}
                 },
                 on_click=lambda: AppState.completar_consulta(consulta.id, {}),
                 loading=AppState.cargando_consultas
             ),
             rx.button(
                 "⏸️",
                 size="1",
                 style={
                     "background": "transparent",
                     "color": "#f59e0b",
                     "border": "1px solid #f59e0b",
                     "font_size": "0.7rem",
                     "padding": "4px 6px",
                     "_hover": {"background": "rgba(245, 158, 11, 0.1)"}
                 },
                 on_click=lambda: AppState.actualizar_estado_consulta_intervencion(consulta.id, "programada"),
                 loading=AppState.cargando_consultas
             ),
             spacing="1",
             width="100%"
         )),
        rx.box()  # Otros estados sin acciones
    )

def botones_accion_funcionales_fase3(consulta: rx.Var) -> rx.Component:
    """⚡ Botones de acción MEJORADOS - Fase 3"""
    return rx.match(
        consulta.estado,
        ("programada",
         # Consulta en espera - puede iniciar o cancelar
         rx.hstack(
             rx.button(
                 rx.hstack(
                     rx.icon("play", size=12),
                     rx.text("Iniciar", font_weight="600"),
                     spacing="1",
                     align="center"
                 ),
                 size="2",
                 style={
                     "background": "#10b981",
                     "color": "white",
                     "border": "none",
                     "font_size": "0.8rem",
                     "padding": "6px 12px",
                     "border_radius": "8px",
                     "transition": "all 0.2s ease",
                     "_hover": {
                         "background": "#059669",
                         "transform": "translateY(-1px)",
                         "box_shadow": "0 4px 12px rgba(16, 185, 129, 0.3)"
                     }
                 },
                 on_click=lambda: AppState.iniciar_atencion_consulta(consulta.id, "en_curso"),
                 loading=AppState.cargando_consultas
             ),
             rx.button(
                 rx.icon("x", size=12),
                 size="2",
                 style={
                     "background": "transparent",
                     "color": "#ef4444",
                     "border": "1px solid #ef4444",
                     "font_size": "0.8rem",
                     "padding": "6px 8px",
                     "border_radius": "8px",
                     "transition": "all 0.2s ease",
                     "_hover": {
                         "background": "rgba(239, 68, 68, 0.1)",
                         "transform": "translateY(-1px)"
                     }
                 },
                 on_click=lambda: AppState.cancelar_consulta(consulta.id, "Cancelada desde interfaz"),
                 loading=AppState.cargando_consultas
             ),
             spacing="2",
             width="100%"
         )),
        ("en_curso",
         # Consulta en proceso - puede finalizar o pausar
         rx.hstack(
             rx.button(
                 rx.hstack(
                     rx.icon("check", size=12),
                     rx.text("Finalizar", font_weight="600"),
                     spacing="1",
                     align="center"
                 ),
                 size="2",
                 style={
                     "background": "#2563eb",
                     "color": "white",
                     "border": "none",
                     "font_size": "0.8rem",
                     "padding": "6px 12px",
                     "border_radius": "8px",
                     "transition": "all 0.2s ease",
                     "_hover": {
                         "background": "#1d4ed8",
                         "transform": "translateY(-1px)",
                         "box_shadow": "0 4px 12px rgba(37, 99, 235, 0.3)"
                     }
                 },
                 on_click=lambda: AppState.completar_consulta(consulta.id, {}),
                 loading=AppState.cargando_consultas
             ),
             rx.button(
                 rx.icon("pause", size=12),
                 size="2",
                 style={
                     "background": "transparent",
                     "color": "#f59e0b",
                     "border": "1px solid #f59e0b",
                     "font_size": "0.8rem",
                     "padding": "6px 8px",
                     "border_radius": "8px",
                     "transition": "all 0.2s ease",
                     "_hover": {
                         "background": "rgba(245, 158, 11, 0.1)",
                         "transform": "translateY(-1px)"
                     }
                 },
                 on_click=lambda: AppState.actualizar_estado_consulta_intervencion(consulta.id, "programada"),
                 loading=AppState.cargando_consultas
             ),
             spacing="2",
             width="100%"
         )),
        rx.box()  # Otros estados sin acciones
    )

def resumen_lateral_dinamico() -> rx.Component:
    """🌙 Sidebar con datos dinámicos - TEMA OSCURO"""
    return rx.box(
        rx.vstack(
            # Header con tema oscuro
            rx.hstack(
                rx.icon("bar-chart-3", size=24, color=DARK_COLORS["accent_blue"]),
                rx.text(
                    "Resumen del Día",
                    font_weight="700",
                    size="4",
                    color=DARK_COLORS["text_primary"],
                    style={"text_shadow": "0 2px 4px rgba(0,0,0,0.5)"}
                ),
                spacing="3",
                align="center"
            ),
            
            rx.divider(
                margin="1.5rem 0",
                style={"border_color": DARK_COLORS["border"], "opacity": "0.3"}
            ),
            
            # Completadas dinámicas con tema oscuro
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("check-circle", size=16, color="white"),
                        style={
                            "background": "#10b981",
                            "border_radius": "8px",
                            "padding": "8px",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center"
                        }
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.consultas_completadas_hoy.length(),
                            font_weight="700",
                            size="6",
                            color="#111827",
                            style={"line_height": "1"}
                        ),
                        rx.text(
                            "Completadas",
                            color="#6b7280",
                            size="2"
                        ),
                        spacing="1",
                        align="start"
                    ),
                    spacing="3",
                    align="center",
                    width="100%"
                ),
                
                # Lista compacta de completadas
                rx.cond(
                    AppState.consultas_completadas_hoy.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.consultas_completadas_hoy,
                            lambda c: rx.box(
                                rx.hstack(
                                    rx.text(
                                        c.paciente_nombre,
                                        font_weight="600",
                                        size="1",
                                        color="#111827"
                                    ),
                                    rx.spacer(),
                                    rx.text(
                                        c.hora_display,
                                        size="1",
                                        color="#9ca3af"
                                    ),
                                    width="100%",
                                    align="center"
                                ),
                                style={
                                    "background": "#f0fdf4",
                                    "border_radius": "6px",
                                    "padding": "0.5rem",
                                    "border_left": "3px solid #10b981"
                                }
                            )
                        ),
                        spacing="2",
                        width="100%",
                        margin_top="1rem"
                    ),
                    rx.text(
                        "No hay completadas",
                        size="1",
                        color="#9ca3af",
                        style={"font_style": "italic"}
                    )
                ),
                
                spacing="0",
                width="100%",
                align="start"
            ),
            
            rx.divider(margin="1rem 0"),
            
            # Canceladas dinámicas
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("x-circle", size=16, color="white"),
                        style={
                            "background": "#ef4444",
                            "border_radius": "8px",
                            "padding": "8px",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center"
                        }
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.consultas_canceladas,
                            font_weight="700",
                            size="6",
                            color="#111827",
                            style={"line_height": "1"}
                        ),
                        rx.text(
                            "Canceladas",
                            color="#6b7280",
                            size="2"
                        ),
                        spacing="1",
                        align="start"
                    ),
                    spacing="3",
                    align="center",
                    width="100%"
                ),
                spacing="0",
                width="100%",
                align="start"
            ),
            
            # Botón de refrescar
            rx.button(
                rx.hstack(
                    rx.icon("refresh-cw", size=16),
                    rx.text("Actualizar", size="2"),
                    spacing="2",
                    align="center"
                ),
                style={
                    "background": "#f3f4f6",
                    "color": "#374151",
                    "border": "1px solid #d1d5db",
                    "width": "100%",
                    "margin_top": "1rem",
                    "_hover": {"background": "#e5e7eb"}
                },
                on_click=AppState.refrescar_consultas,
                loading=AppState.cargando_consultas
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
            "position": "sticky",
            "top": "2rem",
            "max_height": "calc(100vh - 4rem)",
            "overflow_y": "auto",
            "backdrop_filter": "blur(20px)",
            "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)"
        },
        width="100%"
    )

def consultas_page() -> rx.Component:
    """📅 Página principal de consultas con nuevo diseño"""
    return rx.box(
        # Modal de nueva consulta
        modal_nueva_consulta(),
        
        # Botón flotante
        boton_nueva_consulta_flotante(),
        
        # Loading overlay
        rx.cond(
            AppState.cargando_consultas,
            rx.box(
                rx.vstack(
                    rx.spinner(size="3", color=DARK_COLORS["accent_blue"]),
                    rx.text(
                        "Actualizando consultas...",
                        color=DARK_COLORS["text_primary"],
                        size="3"
                    ),
                    spacing="4",
                    align="center"
                ),
                style={
                    "position": "fixed",
                    "top": "50%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "background": DARK_COLORS["glass_bg"],
                    "border": f"1px solid {DARK_COLORS['glass_border']}",
                    "padding": "2rem",
                    "border_radius": "16px",
                    "backdrop_filter": "blur(20px)",
                    "box_shadow": f"0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
                    "z_index": "2000"
                }
            ),
            rx.box()
        ),
        
        # Layout principal responsive
        rx.box(
            # Desktop: Grid con sidebar
            rx.box(
                rx.hstack(
                    # Grid de doctores dinámico (70% ancho)
                    rx.box(
                        rx.cond(
                            AppState.odontologos_disponibles.length() > 0,
                            rx.grid(
                                rx.foreach(
                                    AppState.odontologos_disponibles,
                                    lambda doctor: doctor_card_dinamico(doctor)
                                ),
                                columns="repeat(auto-fit, minmax(300px, 2fr))",
                                
                                gap="1.5rem",
                                width="100%"
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.icon("user-x", size=48, color=DARK_COLORS["text_muted"]),
                                    rx.text(
                                        "No hay odontólogos disponibles",
                                        color=DARK_COLORS["text_secondary"],
                                        size="4",
                                        font_weight="600"
                                    ),
                                    rx.text(
                                        "Contacte al administrador para configurar el personal médico",
                                        color=DARK_COLORS["text_muted"],
                                        size="2",
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
                                    "backdrop_filter": "blur(10px)"
                                }
                            )
                        ),
                        style={"flex": "1", "margin_right": "1.5rem"}
                    ),
                    
                    # Sidebar resumen dinámico (30% ancho)
                    rx.box(
                        resumen_lateral_dinamico(),
                        style={"width": "300px", "flex_shrink": "0", "min_height": "100vh"}
                    ),
                    
                    spacing="0",
                    width="100%",
                    align="start"
                ),
                style={
                    "display": {"@initial": "none", "@lg": "block"},
                    "padding": "2rem",
                    "padding_top": "6rem"  # Space para botón flotante
                }
            ),
            
            # # Mobile: Stack vertical
            # rx.box(
            #     rx.cond(
            #         AppState.odontologos_disponibles.length() > 0,
            #         rx.vstack(
            #             rx.foreach(
            #                 AppState.odontologos_disponibles,
            #                 doctor_card_dinamico
            #             ),
            #             spacing="4",
            #             width="100%"
            #         ),
            #         rx.text("No hay odontólogos disponibles", color=DARK_COLORS["text_muted"])
            #     ),
            #     style={
            #         "display": {"@initial": "block", "@lg": "none"},
            #         "padding": "1rem",
            #         "padding_top": "5rem"  # Space para botón flotante
            #     }
            # )
        ),
        
        style={
            "min_height": "100vh",
            "background": f"linear-gradient(135deg, {DARK_COLORS['background']} 0%, #1a202c 100%)",
            "position": "relative"
        }
    )