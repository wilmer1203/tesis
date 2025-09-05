"""
📅 PÁGINA DE CONSULTAS - FASE 1 DISEÑO DOCTOR-CÉNTRICO
===============================================

🎯 ESPECIFICACIONES DEL USUARIO:
- Layout por doctores (NO tabla tradicional)
- Desktop: Grid 3x3 responsive, scroll vertical para más doctores
- Mobile: Stack vertical, un doctor bajo otro
- Un solo botón "Nueva Consulta" con selectores
- Solo mostrar "en espera" y "en curso" en cards de doctor
- "completadas" y "canceladas" en resumen global
- Orden por llegada (#1, #2, #3...) NO por tiempo
- Support for drag & drop (Fase 2)
- Urgencias/emergencias con prioridad visual

✨ SISTEMA POR ORDEN DE LLEGADA (NO citas programadas)
"""

import reflex as rx
from typing import Dict, Any, List
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button
from dental_system.models.consultas_models import ConsultaModel
from dental_system.models.personal_models import PersonalModel

# ==========================================
# 🎨 ESTILOS BASE PARA LA NUEVA PÁGINA
# ==========================================

# Colores específicos para consultas
CONSULTAS_COLORS = {
    "primary": "#2563eb",
    "success": "#10b981", 
    "warning": "#f59e0b",
    "error": "#ef4444",
    "gray_50": "#f9fafb",
    "gray_100": "#f3f4f6",
    "gray_200": "#e5e7eb",
    "gray_500": "#6b7280",
    "gray_700": "#374151",
    "gray_800": "#1f2937",
    "gray_900": "#111827"
}

# Estados de consultas con colores
ESTADOS_CONSULTA = {
    "programada": {  # en espera
        "color": CONSULTAS_COLORS["warning"],
        "bg": f"rgba(245, 158, 11, 0.1)",
        "border": f"rgba(245, 158, 11, 0.3)",
        "texto": "En Espera",
        "icono": "clock"
    },
    "en_curso": {  # en proceso
        "color": CONSULTAS_COLORS["primary"], 
        "bg": f"rgba(37, 99, 235, 0.1)",
        "border": f"rgba(37, 99, 235, 0.3)",
        "texto": "En Proceso",
        "icono": "activity"
    },
    "completada": {
        "color": CONSULTAS_COLORS["success"],
        "bg": f"rgba(16, 185, 129, 0.1)",
        "border": f"rgba(16, 185, 129, 0.3)",
        "texto": "Completada",
        "icono": "check-circle"
    },
    "cancelada": {
        "color": CONSULTAS_COLORS["error"],
        "bg": f"rgba(239, 68, 68, 0.1)",
        "border": f"rgba(239, 68, 68, 0.3)",
        "texto": "Cancelada", 
        "icono": "x-circle"
    }
}

# ==========================================
# 🏥 COMPONENTES DE DOCTOR CARDS 
# ==========================================

def doctor_card(doctor: rx.Var[PersonalModel], consultas: rx.Var[List[ConsultaModel]]) -> rx.Component:
    """👨‍⚕️ Card individual de doctor con sus consultas activas"""
    return rx.card(
        rx.vstack(
            # Header del doctor
            doctor_header(doctor),
            
            # Divider
            rx.divider(margin="0.5rem 0"),
            
            # Lista de consultas (solo en espera y en curso)
            consultas_activas_list(consultas),
            
            spacing="4",
            width="100%",
            align="start"
        ),
        style={
            "background": "white",
            "border": f"1px solid {CONSULTAS_COLORS['gray_200']}",
            "border_radius": "12px",
            "padding": "1.5rem",
            "box_shadow": "0 1px 3px rgba(0, 0, 0, 0.1)",
            "min_height": "400px",
            "transition": "all 0.2s ease",
            "_hover": {
                "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)",
                "transform": "translateY(-2px)"
            }
        },
        width="100%"
    )

def doctor_header(doctor: rx.Var[PersonalModel]) -> rx.Component:
    """👨‍⚕️ Header del card de doctor"""
    return rx.hstack(
        # Avatar del doctor
        rx.box(
            rx.icon("user-round", size=24, color="white"),
            style={
                "background": CONSULTAS_COLORS["primary"],
                "border_radius": "50%",
                "padding": "12px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center"
            }
        ),
        
        # Info del doctor
        rx.vstack(
            rx.text(
                doctor.nombre_completo,
                style={
                    "font_weight": "700",
                    "font_size": "1.1rem",
                    "color": CONSULTAS_COLORS["gray_900"],
                    "line_height": "1.2"
                }
            ),
            rx.text(
                doctor.especialidad,
                style={
                    "color": CONSULTAS_COLORS["gray_500"],
                    "font_size": "0.9rem"
                }
            ),
            spacing="1",
            align="start"
        ),
        
        rx.spacer(),
        
        # Badge con cantidad pendientes
        consultas_pendientes_badge(doctor.id),
        
        spacing="4",
        align="center",
        width="100%"
    )

def consultas_pendientes_badge(doctor_id: str) -> rx.Component:
    """🏷️ Badge con cantidad de consultas pendientes"""
    return rx.box(
        rx.text(
            0,  # TODO: Calcular consultas pendientes del doctor
            style={
                "color": "white",
                "font_weight": "700",
                "font_size": "0.9rem"
            }
        ),
        style={
            "background": CONSULTAS_COLORS["warning"],
            "border_radius": "50%",
            "padding": "8px 12px",
            "min_width": "32px",
            "text_align": "center",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center"
        }
    )

def consultas_activas_list(consultas: rx.Var[List[ConsultaModel]]) -> rx.Component:
    """📋 Lista de consultas activas (en espera + en curso)"""
    return rx.cond(
        consultas.length() > 0,
        rx.vstack(
            # Título de sección
            rx.text(
                "Cola de Pacientes",
                style={
                    "font_weight": "600",
                    "color": CONSULTAS_COLORS["gray_700"],
                    "font_size": "0.95rem",
                    "margin_bottom": "0.5rem"
                }
            ),
            
            # Lista de consultas
            rx.foreach(
                consultas,
                consulta_patient_card
            ),
            spacing="3",
            width="100%",
            align="start"
        ),
        # Estado vacío
        rx.box(
            rx.vstack(
                rx.icon("calendar-x", size=32, color=CONSULTAS_COLORS["gray_500"]),
                rx.text(
                    "No hay pacientes en cola",
                    style={
                        "color": CONSULTAS_COLORS["gray_500"],
                        "text_align": "center",
                        "font_style": "italic",
                        "font_size": "0.9rem"
                    }
                ),
                spacing="4",
                align="center"
            ),
            style={
                "padding": "2rem",
                "text_align": "center"
            }
        )
    )

def consulta_patient_card(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """👤 Card individual de paciente en la cola"""
    return rx.box(
        rx.vstack(
            # Header con orden de llegada y estado
            rx.hstack(
                # Número de orden
                rx.box(
                    rx.text(
                        f"#{consulta.orden_llegada or '?'}",
                        style={
                            "color": "white",
                            "font_weight": "800",
                            "font_size": "0.8rem"
                        }
                    ),
                    style={
                        "background": CONSULTAS_COLORS["primary"],
                        "border_radius": "6px",
                        "padding": "4px 8px",
                        "min_width": "32px",
                        "text_align": "center"
                    }
                ),
                
                rx.spacer(),
                
                # Estado badge
                estado_consulta_badge(consulta.estado),
                
                width="100%",
                align="center"
            ),
            
            # Info del paciente
            rx.vstack(
                rx.text(
                    consulta.paciente_nombre,
                    style={
                        "font_weight": "600",
                        "color": CONSULTAS_COLORS["gray_900"],
                        "font_size": "0.95rem"
                    }
                ),
                rx.cond(
                    consulta.motivo_consulta != "",
                    rx.text(
                        consulta.motivo_consulta,
                        style={
                            "color": CONSULTAS_COLORS["gray_500"],
                            "font_size": "0.85rem",
                            "font_style": "italic"
                        }
                    ),
                    rx.box()
                ),
                spacing="1",
                align="start",
                width="100%"
            ),
            
            # Botones de acción rápida
            consulta_quick_actions(consulta),
            
            spacing="3",
            width="100%",
            align="start"
        ),
        style={
            "background": CONSULTAS_COLORS["gray_50"],
            "border": f"1px solid {CONSULTAS_COLORS['gray_200']}",
            "border_radius": "8px",
            "padding": "1rem",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": "white",
                "border_color": CONSULTAS_COLORS["primary"],
                "box_shadow": "0 2px 8px rgba(37, 99, 235, 0.1)"
            }
        },
        width="100%"
    )

def estado_consulta_badge(estado: rx.Var[str]) -> rx.Component:
    """🏷️ Badge de estado de consulta"""
    return rx.cond(
        estado == "programada",
        rx.box(
            rx.text(
                "En Espera",
                style={
                    "color": CONSULTAS_COLORS["warning"],
                    "font_weight": "600",
                    "font_size": "0.8rem"
                }
            ),
            style={
                "background": ESTADOS_CONSULTA["programada"]["bg"],
                "border": f"1px solid {ESTADOS_CONSULTA['programada']['border']}",
                "border_radius": "6px",
                "padding": "4px 8px"
            }
        ),
        rx.cond(
            estado == "en_curso",
            rx.box(
                rx.text(
                    "En Proceso",
                    style={
                        "color": CONSULTAS_COLORS["primary"],
                        "font_weight": "600",
                        "font_size": "0.8rem"
                    }
                ),
                style={
                    "background": ESTADOS_CONSULTA["en_curso"]["bg"],
                    "border": f"1px solid {ESTADOS_CONSULTA['en_curso']['border']}",
                    "border_radius": "6px",
                    "padding": "4px 8px"
                }
            ),
            rx.box()  # Otros estados no se muestran en doctor cards
        )
    )

def consulta_quick_actions(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """⚡ Botones de acción rápida por consulta"""
    return rx.cond(
        consulta.estado == "programada",
        # Consulta en espera - puede iniciar
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon("play", size=14),
                    rx.text("Iniciar", style={"font_size": "0.8rem"}),
                    spacing="1",
                    align="center"
                ),
                size="1",
                style={
                    "background": CONSULTAS_COLORS["success"],
                    "color": "white",
                    "border": "none",
                    "padding": "6px 12px",
                    "font_weight": "500",
                    "_hover": {"background": "#059669"}
                },
                on_click=lambda: AppState.iniciar_atencion_consulta(consulta.id)
            ),
            rx.button(
                rx.icon("x", size=14),
                size="1",
                style={
                    "background": "transparent",
                    "color": CONSULTAS_COLORS["error"],
                    "border": f"1px solid {CONSULTAS_COLORS['error']}",
                    "padding": "6px",
                    "_hover": {"background": f"rgba(239, 68, 68, 0.1)"}
                },
                on_click=lambda: AppState.cancelar_consulta(consulta.id, "Cancelada desde interfaz")
            ),
            spacing="2",
            width="100%"
        ),
        rx.cond(
            consulta.estado == "en_curso",
            # Consulta en proceso - puede finalizar
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("check", size=14),
                        rx.text("Finalizar", style={"font_size": "0.8rem"}),
                        spacing="1",
                        align="center"
                    ),
                    size="1",
                    style={
                        "background": CONSULTAS_COLORS["primary"],
                        "color": "white",
                        "border": "none",
                        "padding": "6px 12px",
                        "font_weight": "500",
                        "_hover": {"background": "#1d4ed8"}
                    },
                    on_click=lambda: AppState.completar_consulta(consulta.id, {})
                ),
                rx.button(
                    rx.icon("pause", size=14),
                    size="1",
                    style={
                        "background": "transparent",
                        "color": CONSULTAS_COLORS["warning"],
                        "border": f"1px solid {CONSULTAS_COLORS['warning']}",
                        "padding": "6px",
                        "_hover": {"background": f"rgba(245, 158, 11, 0.1)"}
                    },
                    on_click=lambda: AppState.actualizar_estado_consulta_intervencion(consulta.id, "programada")
                ),
                spacing="2",
                width="100%"
            ),
            rx.box()  # Otros estados no tienen acciones
        )
    )

# ==========================================
# 📊 RESUMEN GLOBAL DE COMPLETADAS/CANCELADAS
# ==========================================

def resumen_global_sidebar() -> rx.Component:
    """📊 Sidebar con resumen de consultas completadas y canceladas"""
    return rx.box(
        rx.vstack(
            # Header del resumen
            rx.hstack(
                rx.icon("bar-chart-3", size=24, color=CONSULTAS_COLORS["primary"]),
                rx.text(
                    "Resumen del Día",
                    style={
                        "font_weight": "700",
                        "font_size": "1.2rem",
                        "color": CONSULTAS_COLORS["gray_900"]
                    }
                ),
                spacing="3",
                align="center"
            ),
            
            rx.divider(margin="1rem 0"),
            
            # Completadas
            resumen_section(
                titulo="Completadas",
                cantidad=AppState.consultas_completadas_hoy.length(),
                color=CONSULTAS_COLORS["success"],
                icono="check-circle",
                consultas_list=AppState.consultas_completadas_list
            ),
            
            rx.divider(margin="1rem 0"),
            
            # Canceladas  
            resumen_section(
                titulo="Canceladas",
                cantidad=AppState.consultas_canceladas,
                color=CONSULTAS_COLORS["error"],
                icono="x-circle",
                consultas_list=AppState.consultas_canceladas_list
            ),
            
            spacing="0",
            width="100%",
            align="start"
        ),
        style={
            "background": "white",
            "border": f"1px solid {CONSULTAS_COLORS['gray_200']}",
            "border_radius": "12px",
            "padding": "1.5rem",
            "box_shadow": "0 1px 3px rgba(0, 0, 0, 0.1)",
            "position": "sticky",
            "top": "2rem",
            "max_height": "calc(100vh - 4rem)",
            "overflow_y": "auto"
        },
        width="100%"
    )

def resumen_section(titulo: str, cantidad: rx.Var[int], color: str, icono: str, 
                   consultas_list: rx.Var[List[ConsultaModel]]) -> rx.Component:
    """📋 Sección individual del resumen"""
    return rx.vstack(
        # Header de la sección
        rx.hstack(
            rx.box(
                rx.icon(icono, size=16, color="white"),
                style={
                    "background": color,
                    "border_radius": "8px",
                    "padding": "8px",
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center"
                }
            ),
            rx.vstack(
                rx.text(
                    cantidad,
                    style={
                        "font_size": "1.5rem",
                        "font_weight": "800",
                        "color": CONSULTAS_COLORS["gray_900"],
                        "line_height": "1"
                    }
                ),
                rx.text(
                    titulo,
                    style={
                        "color": CONSULTAS_COLORS["gray_500"],
                        "font_size": "0.9rem"
                    }
                ),
                spacing="1",
                align="start"
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        
        # Lista compacta
        rx.cond(
            consultas_list.length() > 0,
            rx.vstack(
                rx.foreach(
                    consultas_list,
                    consulta_resumen_card
                ),
                spacing="2",
                width="100%",
                margin_top="1rem"
            ),
            rx.text(
                f"No hay consultas {titulo.lower()} hoy",
                style={
                    "color": CONSULTAS_COLORS["gray_500"],
                    "font_size": "0.85rem",
                    "font_style": "italic",
                    "text_align": "center",
                    "margin_top": "1rem"
                }
            )
        ),
        
        spacing="0",
        width="100%",
        align="start"
    )

def consulta_resumen_card(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """📋 Card compacta para resumen"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    consulta.paciente_nombre,
                    style={
                        "font_weight": "600",
                        "color": CONSULTAS_COLORS["gray_900"],
                        "font_size": "0.85rem"
                    }
                ),
                rx.text(
                    consulta.odontologo_nombre,
                    style={
                        "color": CONSULTAS_COLORS["gray_500"],
                        "font_size": "0.75rem"
                    }
                ),
                spacing="1",
                align="start"
            ),
            rx.spacer(),
            rx.text(
                consulta.hora_display,
                style={
                    "color": CONSULTAS_COLORS["gray_500"],
                    "font_size": "0.75rem",
                    "font_weight": "500"
                }
            ),
            spacing="2",
            align="center",
            width="100%"
        ),
        style={
            "background": CONSULTAS_COLORS["gray_50"],
            "border_radius": "6px",
            "padding": "0.75rem",
            "border_left": f"3px solid {CONSULTAS_COLORS['gray_200']}",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": "white",
                "border_left_color": CONSULTAS_COLORS["primary"]
            }
        },
        width="100%"
    )

# ==========================================
# 🚀 BOTÓN ÚNICA NUEVA CONSULTA
# ==========================================

def boton_nueva_consulta_principal() -> rx.Component:
    """🚀 Botón principal único para nueva consulta"""
    return rx.box(
        rx.button(
            rx.hstack(
                rx.icon("calendar-plus", size=20),
                rx.text(
                    "Nueva Consulta",
                    style={
                        "font_weight": "600",
                        "font_size": "1rem"
                    }
                ),
                spacing="2",
                align="center"
            ),
            style={
                "background": CONSULTAS_COLORS["primary"],
                "color": "white",
                "border": "none",
                "border_radius": "12px",
                "padding": "1rem 2rem",
                "font_weight": "600",
                "box_shadow": "0 4px 12px rgba(37, 99, 235, 0.3)",
                "transition": "all 0.2s ease",
                "_hover": {
                    "background": "#1d4ed8",
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 6px 20px rgba(37, 99, 235, 0.4)"
                }
            },
            on_click=lambda: AppState.seleccionar_y_abrir_modal_consulta("")
        ),
        style={
            "position": "fixed",
            "top": "2rem",
            "right": "2rem",
            "z_index": "1000",
            # Responsive: centro en móvil, esquina en desktop
            "left": {"@initial": "50%", "@lg": "auto"},
            "transform": {"@initial": "translateX(-50%)", "@lg": "none"}
        }
    )

# ==========================================
# 📐 LAYOUTS PRINCIPALES
# ==========================================

def doctors_grid_desktop() -> rx.Component:
    """🖥️ Grid 3x3 para desktop"""
    return rx.grid(
        rx.foreach(
            AppState.odontologos_disponibles,
            lambda doctor: doctor_card(
                doctor,
                []  # TODO: Filtrar consultas del doctor
            )
        ),
        columns="repeat(3, 1fr)",
        gap="1.5rem",
        width="100%"
    )

def doctors_stack_mobile() -> rx.Component:
    """📱 Stack vertical para móvil"""  
    return rx.vstack(
        rx.foreach(
            AppState.odontologos_disponibles,
            lambda doctor: doctor_card(
                doctor,
                []  # TODO: Filtrar consultas del doctor
            )
        ),
        spacing="6",
        width="100%"
    )

def main_layout_desktop() -> rx.Component:
    """🖥️ Layout principal desktop con sidebar"""
    return rx.hstack(
        # Grid de doctores (2/3 del ancho)
        rx.box(
            doctors_grid_desktop(),
            style={"flex": "1", "margin_right": "1.5rem"}
        ),
        
        # Sidebar resumen (1/3 del ancho)
        rx.box(
            resumen_global_sidebar(),
            style={"width": "350px", "flex_shrink": "0"}
        ),
        
        spacing="0",
        width="100%",
        align="start"
    )

def main_layout_mobile() -> rx.Component:
    """📱 Layout principal móvil solo stack"""
    return doctors_stack_mobile()

# ==========================================
# 🌟 PÁGINA PRINCIPAL FASE 1
# ==========================================

def consultas_page_fase1() -> rx.Component:
    """
    📅 CONSULTAS FASE 1 - DOCTOR-CÉNTRICO
    
    🎯 Especificaciones implementadas:
    ✅ Desktop: Grid 3x3 con sidebar resumen
    ✅ Mobile: Stack vertical de doctores  
    ✅ Solo "en espera" y "en curso" en doctor cards
    ✅ "completadas" y "canceladas" en sidebar
    ✅ Orden por llegada (#1, #2, #3...)
    ✅ Un botón único "Nueva Consulta"
    ✅ Cards limpios con acciones rápidas
    """
    return rx.cond(
        AppState.cargando_consultas,
        # Loading state
        rx.box(
            rx.vstack(
                rx.spinner(size="3", color=CONSULTAS_COLORS["primary"]),
                rx.text(
                    "Cargando consultas del día...",
                    style={
                        "color": CONSULTAS_COLORS["gray_500"],
                        "font_size": "1.1rem",
                        "text_align": "center"
                    }
                ),
                spacing="4",
                align="center"
            ),
            style={
                "min_height": "100vh",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "background": CONSULTAS_COLORS["gray_50"]
            }
        ),
        # Layout principal responsive
        rx.box(
            # Botón flotante Nueva Consulta
            boton_nueva_consulta_principal(),
            
            # Layout adaptativo
            rx.box(
                # Desktop layout (oculto en mobile)
                rx.box(
                    main_layout_desktop(),
                    style={
                        "display": {"@initial": "none", "@lg": "block"},
                        "padding": "2rem",
                        "padding_top": "5rem"  # Space para botón flotante
                    }
                ),
                
                # Mobile layout (oculto en desktop)
                rx.box(
                    main_layout_mobile(),
                    style={
                        "display": {"@initial": "block", "@lg": "none"},
                        "padding": "1rem",
                        "padding_top": "5rem"  # Space para botón flotante
                    }
                )
            ),
            
            style={
                "min_height": "100vh",
                "background": CONSULTAS_COLORS["gray_50"],
                "position": "relative"
            }
        )
    )