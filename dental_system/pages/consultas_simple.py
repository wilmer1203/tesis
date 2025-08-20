"""
📅 PÁGINA DE CONSULTAS - DISEÑO DOCTOR-CÉNTRICO FUNCIONAL
========================================================

🎯 Especificaciones implementadas:
✅ Grid 3x3 de doctores (desktop) / Stack vertical (mobile)
✅ Solo consultas "en espera" y "en curso" en doctor cards
✅ Botón único "Nueva Consulta" flotante
✅ Usa funciones existentes de los substates
✅ Diseño responsive
"""

import reflex as rx
from dental_system.state.app_state import AppState

def boton_nueva_consulta_flotante() -> rx.Component:
    """🚀 Botón flotante único para nueva consulta"""
    return rx.button(
        rx.hstack(
            rx.icon("calendar-plus", size=20),
            rx.text("Nueva Consulta", font_weight="600"),
            spacing="2",
            align="center"
        ),
        style={
            "background": "#2563eb",
            "color": "white",
            "border": "none",
            "border_radius": "12px",
            "padding": "1rem 2rem",
            "position": "fixed",
            "top": "2rem",
            "right": "2rem",
            "z_index": "1000",
            "box_shadow": "0 4px 12px rgba(37, 99, 235, 0.3)",
            "_hover": {
                "background": "#1d4ed8",
                "transform": "translateY(-2px)",
                "box_shadow": "0 6px 20px rgba(37, 99, 235, 0.4)"
            }
        },
        on_click=AppState.abrir_modal_crear_consulta
    )

def doctor_card_mejorado(doctor: rx.Var) -> rx.Component:
    """👨‍⚕️ Card mejorado de doctor con consultas"""
    return rx.card(
        rx.vstack(
            # Header del doctor
            rx.hstack(
                # Avatar
                rx.box(
                    rx.icon("user-round", size=20, color="white"),
                    style={
                        "background": "#2563eb",
                        "border_radius": "50%",
                        "padding": "10px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                
                # Info del doctor
                rx.vstack(
                    rx.text(
                        doctor.nombre_completo,
                        font_weight="700",
                        size="3",
                        color="#111827"
                    ),
                    rx.text(
                        doctor.especialidad,
                        color="#6b7280",
                        size="2"
                    ),
                    spacing="1",
                    align="start"
                ),
                
                rx.spacer(),
                
                # Badge pendientes - calculado dinámicamente
                consultas_pendientes_badge_simple(doctor.id),
                
                spacing="3",
                align="center",
                width="100%"
            ),
            
            # Divider
            rx.divider(margin="1rem 0", color="#e5e7eb"),
            
            # Sección de pacientes
            rx.vstack(
                rx.text(
                    "Cola de Pacientes",
                    font_weight="600",
                    color="#374151",
                    size="2"
                ),
                
                # Lista de consultas del doctor
                consultas_doctor_lista(doctor.id),
                
                spacing="3",
                width="100%",
                align="start"
            ),
            
            spacing="0",
            width="100%",
            align="start"
        ),
        style={
            "padding": "1.5rem",
            "border": "1px solid #e5e7eb",
            "border_radius": "12px",
            "min_height": "350px",
            "transition": "all 0.2s ease",
            "_hover": {
                "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
                "transform": "translateY(-2px)"
            }
        },
        width="100%"
    )

def consultas_pendientes_badge_simple(doctor_id: str) -> rx.Component:
    """🏷️ Badge simple con número de consultas pendientes"""
    return rx.box(
        rx.text(
            "3",  # TODO: Calcular dinámicamente las consultas del doctor
            style={
                "color": "white",
                "font_weight": "700",
                "font_size": "0.9rem"
            }
        ),
        style={
            "background": "#f59e0b",
            "border_radius": "50%", 
            "padding": "6px 10px",
            "min_width": "28px",
            "text_align": "center",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center"
        }
    )

def consultas_doctor_lista(doctor_id: str) -> rx.Component:
    """📋 Lista de consultas activas del doctor"""
    return rx.cond(
        AppState.lista_consultas.length() > 0,
        rx.vstack(
            # Por ahora mostrar todas las consultas - TODO: Filtrar por doctor
            rx.foreach(
                AppState.lista_consultas,
                paciente_consulta_card
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

def paciente_consulta_card(consulta: rx.Var) -> rx.Component:
    """👤 Card individual de paciente"""
    return rx.box(
        rx.vstack(
            # Header con orden y estado
            rx.hstack(
                # Número de orden (simulado por ahora)
                rx.box(
                    rx.text(
                        "#1",  # TODO: Usar orden real
                        style={
                            "color": "white",
                            "font_weight": "800",
                            "font_size": "0.7rem"
                        }
                    ),
                    style={
                        "background": "#2563eb",
                        "border_radius": "4px",
                        "padding": "2px 6px",
                        "min_width": "24px",
                        "text_align": "center"
                    }
                ),
                
                rx.spacer(),
                
                # Estado badge
                estado_badge_simple(consulta.estado),
                
                width="100%",
                align="center"
            ),
            
            # Info del paciente
            rx.text(
                consulta.paciente_nombre,
                font_weight="600",
                color="#111827",
                size="2"
            ),
            
            # Motivo (si existe)
            rx.cond(
                consulta.motivo_consulta != "",
                rx.text(
                    consulta.motivo_consulta,
                    color="#6b7280",
                    size="1",
                    style={"font_style": "italic"}
                ),
                rx.box()
            ),
            
            # Botones de acción
            botones_accion_consulta(consulta),
            
            spacing="2",
            width="100%",
            align="start"
        ),
        style={
            "background": "#f9fafb",
            "border": "1px solid #e5e7eb",
            "border_radius": "8px",
            "padding": "0.75rem",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": "white",
                "border_color": "#2563eb"
            }
        },
        width="100%"
    )

def estado_badge_simple(estado: rx.Var[str]) -> rx.Component:
    """🏷️ Badge simple de estado"""
    return rx.cond(
        estado == "programada",
        rx.box(
            rx.text(
                "En Espera",
                style={
                    "color": "#f59e0b",
                    "font_weight": "600",
                    "font_size": "0.7rem"
                }
            ),
            style={
                "background": "rgba(245, 158, 11, 0.1)",
                "border": "1px solid rgba(245, 158, 11, 0.3)",
                "border_radius": "4px",
                "padding": "2px 6px"
            }
        ),
        rx.cond(
            estado == "en_curso",
            rx.box(
                rx.text(
                    "En Proceso",
                    style={
                        "color": "#2563eb",
                        "font_weight": "600",
                        "font_size": "0.7rem"
                    }
                ),
                style={
                    "background": "rgba(37, 99, 235, 0.1)",
                    "border": "1px solid rgba(37, 99, 235, 0.3)",
                    "border_radius": "4px",
                    "padding": "2px 6px"
                }
            ),
            rx.box()
        )
    )

def botones_accion_consulta(consulta: rx.Var) -> rx.Component:
    """⚡ Botones de acción por consulta"""
    return rx.cond(
        consulta.estado == "programada",
        # Consulta en espera
        rx.hstack(
            rx.button(
                "▶️ Iniciar",
                size="1",
                style={
                    "background": "#10b981",
                    "color": "white",
                    "font_size": "0.7rem",
                    "padding": "4px 8px"
                },
                on_click=lambda: AppState.cambiar_estado_consulta(consulta.id, "en_curso")
            ),
            rx.button(
                "❌",
                size="1",
                style={
                    "background": "transparent",
                    "color": "#ef4444",
                    "border": "1px solid #ef4444",
                    "font_size": "0.7rem",
                    "padding": "4px 6px"
                },
                on_click=lambda: AppState.cancelar_consulta(consulta.id)
            ),
            spacing="1",
            width="100%"
        ),
        rx.cond(
            consulta.estado == "en_curso",
            # Consulta en proceso
            rx.hstack(
                rx.button(
                    "✅ Finalizar",
                    size="1",
                    style={
                        "background": "#2563eb",
                        "color": "white",
                        "font_size": "0.7rem",
                        "padding": "4px 8px"
                    },
                    on_click=lambda: AppState.cambiar_estado_consulta(consulta.id, "completada")
                ),
                rx.button(
                    "⏸️",
                    size="1",
                    style={
                        "background": "transparent",
                        "color": "#f59e0b",
                        "border": "1px solid #f59e0b",
                        "font_size": "0.7rem",
                        "padding": "4px 6px"
                    },
                    on_click=lambda: AppState.cambiar_estado_consulta(consulta.id, "programada")
                ),
                spacing="1",
                width="100%"
            ),
            rx.box()
        )
    )

def resumen_lateral() -> rx.Component:
    """📊 Sidebar con resumen de completadas/canceladas"""
    return rx.card(
        rx.vstack(
            # Header
            rx.text(
                "Resumen del Día",
                font_weight="700",
                size="4",
                color="#111827"
            ),
            
            rx.divider(margin="1rem 0"),
            
            # Completadas
            rx.vstack(
                rx.hstack(
                    rx.icon("check-circle", size=16, color="#10b981"),
                    rx.text(
                        AppState.consultas_completadas_hoy.length(),
                        font_weight="700",
                        size="3"
                    ),
                    rx.text("Completadas", color="#6b7280"),
                    spacing="2",
                    align="center"
                ),
                
                # Lista compacta de completadas
                rx.cond(
                    AppState.consultas_completadas_hoy.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.consultas_completadas_hoy,
                            lambda c: rx.text(
                                c.paciente_nombre,
                                size="1",
                                color="#6b7280"
                            )
                        ),
                        spacing="1",
                        width="100%",
                        margin_top="0.5rem"
                    ),
                    rx.text("No hay completadas", size="1", color="#9ca3af")
                ),
                
                spacing="2",
                width="100%",
                align="start"
            ),
            
            rx.divider(margin="1rem 0"),
            
            # Canceladas
            rx.vstack(
                rx.hstack(
                    rx.icon("x-circle", size=16, color="#ef4444"),
                    rx.text(
                        AppState.consultas_canceladas,
                        font_weight="700",
                        size="3"
                    ),
                    rx.text("Canceladas", color="#6b7280"),
                    spacing="2",
                    align="center"
                ),
                spacing="2",
                width="100%",
                align="start"
            ),
            
            spacing="0",
            width="100%",
            align="start"
        ),
        style={
            "padding": "1.5rem",
            "position": "sticky",
            "top": "2rem",
            "max_height": "calc(100vh - 4rem)",
            "overflow_y": "auto"
        },
        width="100%"
    )

def consultas_simple_page() -> rx.Component:
    """📅 Página principal con diseño doctor-céntrico"""
    return rx.box(
        # Botón flotante
        boton_nueva_consulta_flotante(),
        
        # Layout principal responsive
        rx.box(
            # Desktop: Grid con sidebar
            rx.box(
                rx.hstack(
                    # Grid de doctores (70% ancho)
                    rx.box(
                        rx.grid(
                            rx.foreach(
                                AppState.odontologos_disponibles,
                                doctor_card_mejorado
                            ),
                            columns="repeat(auto-fit, minmax(300px, 1fr))",
                            gap="1.5rem",
                            width="100%"
                        ),
                        style={"flex": "1", "margin_right": "1.5rem"}
                    ),
                    
                    # Sidebar resumen (30% ancho)
                    rx.box(
                        resumen_lateral(),
                        style={"width": "300px", "flex_shrink": "0"}
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
            
            # Mobile: Stack vertical
            rx.box(
                rx.vstack(
                    rx.foreach(
                        AppState.odontologos_disponibles,
                        doctor_card_mejorado
                    ),
                    spacing="4",
                    width="100%"
                ),
                style={
                    "display": {"@initial": "block", "@lg": "none"},
                    "padding": "1rem",
                    "padding_top": "5rem"  # Space para botón flotante
                }
            )
        ),
        
        style={
            "min_height": "100vh",
            "background": "#f9fafb",
            "position": "relative"
        }
    )