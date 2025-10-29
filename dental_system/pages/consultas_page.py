"""
🌙 PÁGINA DE CONSULTAS V4
============================================================
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.modal_nueva_consulta import modal_nueva_consulta
from dental_system.components.common import medical_page_layout
from dental_system.components.forms import (
        enhanced_form_field, enhanced_form_field_dinamico, form_section_header, 
        success_feedback
    )
from dental_system.styles.themes import (
    SPACING, RADIUS, ROLE_THEMES, GRADIENTS, DARK_THEME,SHADOWS,GLASS_EFFECTS, COLORS, ANIMATIONS, 
    dark_header_style, glassmorphism_card
)

# ==========================================
# 📊 QUEUE CONTROL BAR - PANEL SUPERIOR NUEVO
# ==========================================

def stat_card_simple(titulo: str, valor, color: str = "blue") -> rx.Component:
    """📊 Tarjeta de estadística simple"""
    # Mapeo de colores a COLORS del sistema
    color_map = {
        "blue": COLORS["primary"]["500"],
        "yellow": COLORS["warning"]["500"],
        "green": COLORS["success"]["500"],
        "red": COLORS["error"]["500"]
    }
    accent_color = color_map.get(color, COLORS["primary"]["500"])

    return rx.box(
        rx.vstack(
            rx.text(titulo, size="2", color=DARK_THEME["colors"]["text_muted"]),
            rx.text(valor, size="4", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            spacing="1",
            align="center"
        ),
        style={
            **glassmorphism_card(opacity="80", blur="10px"),
            "padding": SPACING["4"],
            "min_width": "100px",
            "border_left": f"4px solid {accent_color}"
        }
    )

def queue_control_bar_simple() -> rx.Component:
    """📊 Panel de control superior simplificado"""
    return rx.box(
        rx.vstack(
            # Título
            rx.heading("📋 Panel de Control - Consultas del Día", size="4", color=DARK_THEME["colors"]["text_primary"]),
            
            # Stats en grid
            rx.grid(
                # 🔄 ACTUALIZADO: Usar computed vars específicos tipados
                stat_card_simple("Total", AppState.total_consultas_dashboard.to_string()),
                stat_card_simple("En Espera", AppState.total_en_espera_dashboard.to_string(), "yellow"),
                stat_card_simple("En Atención", AppState.total_en_atencion_dashboard.to_string(), "green"),
                stat_card_simple("Canceladas", AppState.total_canceladas_dashboard.to_string(), "red"),
                stat_card_simple("Completadas", AppState.total_completadas_dashboard.to_string(), "blue"),
                stat_card_simple("Dentistas", AppState.total_odontologos_activos_dashboard.to_string(), "blue"),
                columns="6",
                spacing="3",
                width="100%"
            ), 
             spacing="4",
            width="100%"
        ),
        style={
            **glassmorphism_card(opacity="80", blur="15px"),
            "padding": SPACING["6"],
            "margin": f"{SPACING['4']} 0",
            "width": "100%"
        }
    )

def boton_nueva_consulta_flotante() -> rx.Component:
    """🚀 Botón flotante con efecto glassmorphism - TEMA OSCURO"""
    return rx.button(
        rx.hstack(
            rx.icon("calendar-plus", size=20, color=DARK_THEME["colors"]["text_primary"]),
            rx.text("Nueva Consulta", font_weight="600", color=DARK_THEME["colors"]["text_primary"]),
            spacing="2",
            align="center"
        ),
        style={
            "background": ROLE_THEMES['gerente']['gradient'],
            "color": DARK_THEME["colors"]["text_primary"],
            "border": f"1px solid rgba(255, 255, 255, 0.1)",
            "border_radius": RADIUS["xl"],
            "padding": f"{SPACING['4']} {SPACING['8']}",
            "position": "fixed",
            "top": SPACING["8"],
            "right": SPACING["8"],
            "z_index": "1000",
            "backdrop_filter": "blur(10px)",
            "box_shadow": f"0 8px 32px {COLORS['primary']['500']}30, inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "transition": "all 0.3s ease",
            "_hover": {
                "background": f"linear-gradient(135deg, {COLORS['blue']['600']} 0%, {COLORS['primary']['500']} 100%)",
                "transform": "translateY(-2px)",
                "box_shadow": f"0 12px 40px {COLORS['primary']['500']}40, inset 0 1px 0 rgba(255, 255, 255, 0.2)"
            }
        },
        # 🔄 ACTUALIZADO: Usar método directo de abrir modal
        on_click=AppState.abrir_modal_nueva_consulta
    )
# ==========================================
# 🏷️ BADGE CONSULTAS UNIFICADO 
# ==========================================
def badge_consultas_unificado(
    doctor_id: str,
    size: str = "md", 
    badge_type: str = "total"
) -> rx.Component:
    """🏷️ Badge unificado para todos los contextos de consultas"""
    
    # Configuración por tamaño
    size_config = {
        "sm": {"padding": f"{SPACING['1.5']} {SPACING['2.5']}", "font_size": "0.8rem", "icon_size": 12},
        "md": {"padding": f"{SPACING['2.5']} {SPACING['3.5']}", "font_size": "1.0rem", "icon_size": 14}, 
        "lg": {"padding": f"{SPACING['3.5']} {SPACING['5']}", "font_size": "1.2rem", "icon_size": 16}
    }
    
    config = size_config[size]
    
    # # Obtener contador según tipo
    # if badge_type == "total":
    #     # 🔄 ACTUALIZADO: Total por odontólogo específico
    #     count = AppState.totales_por_odontologo_dict.get(doctor_id, 0)
    #     description_text = rx.cond(
    #         count == 0, "Sin cola",
    #         rx.cond(count == 1, "1 paciente", f"{count} pacientes")
    #     )
    # elif badge_type == "urgentes":
    #     # 🔄 ACTUALIZADO: Urgentes por odontólogo específico
    #     count = AppState.urgentes_por_odontologo_dict.get(doctor_id, 0)
    #     description_text = rx.cond(
    #         count == 0, "Sin urgentes",
    #         rx.cond(count == 1, "1 urgente", f"{count} urgentes")
    #     )
    # else:
    count = 0

    count = AppState.totales_por_odontologo_dict.get(doctor_id, 0)
    return rx.vstack(
        # Contador principal
        rx.box(
            rx.text(
                count.to_string(),
                font_weight="800",
                font_size=config["font_size"],
                color=DARK_THEME["colors"]["text_primary"],
                style={"text_shadow": "0 0 10px rgba(255, 255, 255, 0.5)"}
            ),
            style={
                "background": rx.cond(
                    count > 3,
                    f"linear-gradient(135deg, {COLORS['error']['500']} 0%, {COLORS['error']['400']} 100%)",
                    rx.cond(
                        count > 0,
                        f"linear-gradient(135deg, {COLORS['warning']['500']} 0%, {COLORS['warning']['400']} 100%)",
                        f"linear-gradient(135deg, {DARK_THEME['colors']['border']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)"
                    )  
                ),
                "border": f"1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": RADIUS["xl"],
                "padding": config["padding"],
                "text_align": "center",
                "backdrop_filter": "blur(10px)",
                "transition": "all 0.3s ease",
                "animation": rx.cond(
                    count > 0,
                    "pulse 2s infinite",
                    "none"
                ),
                "_hover": {"transform": "scale(1.05)"}
            }
        ), 
        spacing="2",
        align="center"
    )

def badge_prioridad(prioridad: rx.Var[str]) -> rx.Component:
    """🏷️ NUEVO: Badge de prioridad como en React - FUNCIONAL"""
    return rx.match(
        prioridad,
        ("urgente",
         rx.box(
             rx.hstack(
                 rx.icon("triangle-alert", size=10, color="white"),
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
                 "background": COLORS["error"]["600"],
                 "border": f"1px solid {COLORS['error']['600']}",
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
                 "backdrop_filter": "blur(10px)",
                 "box_shadow": f"0 2px 8px {COLORS['error']['600']}30",
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
                 "background": COLORS["warning"]["700"],
                 "border": f"1px solid {COLORS['warning']['700']}",
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
                 "backdrop_filter": "blur(10px)",
                 "box_shadow": f"0 2px 8px {COLORS['warning']['700']}30"
             }
         )),
        ("normal",
         rx.box(
             rx.text(
                 "Normal",
                 font_weight="600",
                 font_size="0.65rem",
                 color=DARK_THEME["colors"]["text_muted"],
                 style={"letter_spacing": "0.05em"}
             ),
             style={
                 "background": f"{COLORS['gray']['600']}10",
                 "border": f"1px solid {COLORS['gray']['600']}",
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
                 "backdrop_filter": "blur(5px)"
             }
         )),
        ("baja",
         rx.box(
             rx.hstack(
                 rx.icon("arrow-down", size=10, color="white"),
                 rx.text(
                     "BAJA",
                     font_weight="700",
                     font_size="0.65rem",
                     color="white",
                     style={"letter_spacing": "0.05em"}
                 ),
                 spacing="1",
                 align="center"
             ),
             style={
                 "background": COLORS["success"]["600"],
                 "border": f"1px solid {COLORS['success']['600']}",
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
                 "backdrop_filter": "blur(5px)",
                 "box_shadow": f"0 2px 8px {COLORS['success']['600']}30"
             }
         )),
    )

def consulta_card_mejorada_v41(consulta_data: rx.Var, posicion: int) -> rx.Component:
    """🎯 TARJETA DE PACIENTE MEJORADA - Inspirada en React"""
    return rx.box(
        rx.vstack(
            # Header mejorado con posición y prioridad
            rx.hstack(
                # Número de posición 
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
                            f"linear-gradient(135deg, {COLORS["success"]["500"]} 0%, #48bb78 100%)",
                            f"linear-gradient(135deg, {COLORS["primary"]["500"]} 0%, #4299e1 100%)"
                        ),
                        "border": f"1px solid {"rgba(255, 255, 255, 0.1)"}",
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
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    spacing="1",
                    align="start"
                ),
                
                rx.spacer(),
                
                # Badge de prioridad (NUEVO) - FUNCIONAL
                badge_prioridad(consulta_data.prioridad),
                
                width="100%",
                align="center"
            ),
            
            # Botones de acción mejorados - usando los existentes
            rx.match(
                consulta_data.estado,
                ("en_espera",
                 rx.hstack(
                     rx.box(
                         rx.hstack(
                             rx.icon("clock", size=14, color="white"),
                             rx.text("En Espera", size="1", color="white"),
                             spacing="2",
                             align="center"
                         ),
                         style={
                             "background": f"linear-gradient(135deg, {COLORS["success"]["500"]} 0%, #48bb78 100%)",
                             "border": f"1px solid {"rgba(255, 255, 255, 0.1)"}",
                             "border_radius": RADIUS["lg"],
                             "padding": f"{SPACING['1']}",
                             "backdrop_filter": "blur(10px)"
                         },
                     ),
                     
                     # Botón de transferir (NUEVO) - FUNCIONAL
                     rx.button(
                         rx.icon("arrow-left-right", size=14, color=COLORS["primary"]["500"]),
                         # 🔄 ACTUALIZADO: Usar gestionar_modal_operacion
                         on_click=lambda: AppState.gestionar_modal_operacion("abrir_transferencia", consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {COLORS["primary"]["500"]}",
                             "border_radius": RADIUS["lg"],
                             "padding": SPACING["2.5"],
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
                     
                     
                     # NUEVO: Botones de orden en cola
                     rx.button(
                         rx.icon("chevron-up", size=12, color=COLORS["success"]["500"]),
                         # ℹ️ LEGACY: subir_en_cola - mantener si existe o crear wrapper
                         on_click=lambda: AppState.subir_en_cola(consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {COLORS["success"]["500"]}",
                             "border_radius": RADIUS["md"],
                             "padding": SPACING["1.5"],
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
                         rx.icon("chevron-down", size=12, color=COLORS["warning"]["500"]),
                         # ℹ️ LEGACY: bajar_en_cola - mantener si existe o crear wrapper
                         on_click=lambda: AppState.bajar_en_cola(consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {COLORS["warning"]["500"]}",
                             "border_radius": RADIUS["md"],
                             "padding": SPACING["1.5"],
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
                         rx.icon("x", size=14, color=COLORS["error"]["500"]),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {COLORS["error"]["500"]}",
                             "border_radius": RADIUS["lg"],
                             "padding": SPACING["2.5"],
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "_hover": {
                                 "background": f"rgba(229, 62, 62, 0.1)",
                                 "transform": "translateY(-2px)"
                             }
                         },
                         # 🔄 ACTUALIZADO: Usar operacion_consulta_master
                         on_click=lambda: AppState.operacion_consulta_master("cancelar", consulta_data.id, {"motivo": "Cancelada desde interfaz"}),
                         loading=AppState.cargando_consultas
                     ),
                     
                     spacing="2",
                     width="100%",
                     align="center"
                 )),
                ("entre_odontologos",
                 rx.hstack(
                     rx.button(
                         rx.hstack(
                             rx.icon("check", size=14, color="white"),
                             rx.text("Finalizar", font_weight="600", color="white"),
                             spacing="2",
                             align="center"
                         ),
                         style={
                             "background": f"linear-gradient(135deg, {COLORS["primary"]["500"]} 0%, #4299e1 100%)",
                             "border": f"1px solid {"rgba(255, 255, 255, 0.1)"}",
                             "border_radius": RADIUS["lg"],
                             "padding": f"{SPACING['2.5']} {SPACING['5']}",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "flex": "1",
                             "_hover": {
                                 "transform": "translateY(-2px)",
                                 "box_shadow": f"0 8px 25px rgba(49, 130, 206, 0.4)"
                             }
                         },
                         # 🔄 ACTUALIZADO: Usar completar_consulta_completa con protección anti-doble-clic
                        on_click=lambda: AppState.completar_consulta_completa(consulta_data.id),
                        loading=AppState.cargando_consultas,
                        disabled=AppState.finalizando_consulta  # 🛡️ Deshabilitar durante ejecución
                     ),
                     spacing="2",
                     width="100%",
                     align="center"
                 )),
                ("en_atencion",
                rx.box(
                    rx.hstack(
                        rx.icon("activity", size=14, color=COLORS["success"]["500"]),
                        rx.text(
                            "En Atención Médica",
                            font_weight="700",
                            size="3",
                            color=COLORS["success"]["500"]
                        ),
                        spacing="2"
                    ),
                    style={
                        "background": f"rgba(56, 161, 105, 0.1)",
                        "border": f"2px solid {COLORS['success']['500']}",
                        "border_radius": RADIUS["lg"],
                        "padding": f"{SPACING['3']} {SPACING['6']}",
                        "backdrop_filter": "blur(10px)",
                        "animation": "pulse 2s infinite"  # Indicador visual de atención activa
                    }
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
                f"linear-gradient(135deg, {"rgba(26, 31, 46, 0.8)"} 0%, rgba(56, 161, 105, 0.1) 100%)",
                f"rgba(26, 31, 46, 0.8)"
            ),
            "border": rx.cond(
                posicion == 1,
                f"2px solid {COLORS["success"]["500"]}",
                f"1px solid {"rgba(255, 255, 255, 0.1)"}"
            ),
            "border_radius": RADIUS["xl"],
            "padding": SPACING["6"],
            "backdrop_filter": "blur(20px)",
            "box_shadow": rx.cond(
                posicion == 1,
                f"0 12px 40px rgba(56, 161, 105, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
                f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)"
            ),
            "transition": "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            "cursor": "grab",
            "_hover": {
                "transform": "translateY(-4px) scale(1.02)",
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
        # 🔄 ACTUALIZADO: Verificar si tiene consultas el odontólogo
        AppState.totales_por_odontologo_dict.get(doctor_id, 0) > 0,
        rx.vstack(
            rx.foreach(
                # 🔄 ACTUALIZADO: Consultas específicas del odontólogo
                AppState.consultas_por_odontologo_dict.get(doctor_id, []),
                lambda consulta_data, index: consulta_card_mejorada_v41(consulta_data, index + 1)
            ),
            spacing="4",
            width="100%"
        ),
        # Estado vacío mejorado
        rx.box(
            rx.vstack(
                rx.icon("calendar-x", size=40, color=DARK_THEME["colors"]["text_muted"]),
                rx.text(
                    "No hay pacientes en cola",
                    color=DARK_THEME["colors"]["text_muted"],
                    size="3",
                    font_weight="600",
                    style={"text_align": "center"}
                ),
                rx.text(
                    "La cola está vacía en este momento",
                    color=DARK_THEME["colors"]["text_muted"],
                    size="2",
                    style={"text_align": "center", "opacity": "0.7"}
                ),
                spacing="3",
                align="center"
            ),
            style={
                "padding": SPACING["12"],
                "text_align": "center",
                "border": f"2px dashed {DARK_THEME["colors"]["border"]}",
                "border_radius": RADIUS["xl"],
                "background": f"rgba({DARK_THEME["colors"]["surface"]}, 0.3)",
                "backdrop_filter": "blur(10px)"
            }
        )
    )

# ==========================================
# 🧩 SUBCOMPONENTES DEL DOCTOR CARD V41
# ==========================================

def doctor_header(doctor: rx.Var) -> rx.Component:
    """👨‍⚕️ Header con foto, nombre, especialidad y estado"""
    return rx.hstack(
        # Avatar con estado
        rx.box(
            rx.icon("user-round", size=24, color=DARK_THEME["colors"]["text_primary"]),
            style={
                "background": f"linear-gradient(135deg, {COLORS["primary"]["500"]} 0%, #48bb78 100%)",
                "border_radius": "50%",
                "padding": SPACING["3"],
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
                "Dr(a). " + doctor.primer_nombre + " " + doctor.primer_apellido,
                font_weight="600",
                size="2",
                color=DARK_THEME["colors"]["text_primary"]
            ),
            rx.text(
                doctor.especialidad,
                color=DARK_THEME["colors"]["text_secondary"],
                size="1",
                font_weight="500"
            ),
            spacing="1",
            align="start"
        ),
        
        rx.spacer(),
        
        # Estado disponibilidad
        rx.box(
            rx.hstack(
                rx.icon("circle-check", size=9, color=COLORS["success"]["500"]),
                rx.text(
                    "Disponible",
                    font_weight="600",
                    font_size="0.6rem",
                    color=COLORS["success"]["500"]
                ),
                spacing="1",
                align="center"
            ),
            style={
                "background": "rgba(56, 161, 105, 0.1)",
                "border": f"1px solid rgba(56, 161, 105, 0.3)",
                "border_radius": RADIUS["md"],
                "padding": f"{SPACING['1.5']} {SPACING['3']}",
                "backdrop_filter": "blur(5px)"
            }
        ),
        margin=  f"{SPACING['4']} 0",
        spacing="2",
        align="center",
        width="100%"
    )

def patient_queue_header(doctor_id: str) -> rx.Component:
    """📋 Header de la cola de pacientes con contador"""
    return rx.hstack(
        rx.icon("users", size=16, color=COLORS["primary"]["500"]),
        rx.text(
            "Cola de Pacientes",
            font_weight="700",
            color=DARK_THEME["colors"]["text_primary"],
            size="3"
        ),
        # Contador en header usando badge_consultas_unificado
        badge_consultas_unificado(
            doctor_id=doctor_id,
            size="sm",
            badge_type="total"
        ),
        spacing="2",
        align="center",
        width="100%",
        justify="center"
    )

def patient_queue_area(doctor_id: str) -> rx.Component:
    """👥 Área de lista de pacientes con drop zone"""
    return rx.box(
        lista_consultas_mejorada_v41(doctor_id),
        style={
            "min_height": "200px",
            "border_radius": RADIUS["lg"],
            "border": f"2px dashed transparent",
            "padding": SPACING["2"],
            "transition": "all 0.3s ease",
            "position": "relative",
            "_hover": {
                "border_color": f"{COLORS["primary"]["500"]}40",
                "background": f"rgba(14, 165, 233, 0.05)"
            }
        }
    )

# def patient_queue(doctor_id: str) -> rx.Component:
#     """👥 Sección completa de cola de pacientes"""
#     return rx.vstack(
#         patient_queue_header(doctor_id),
#         patient_queue_area(doctor_id),
#         spacing="4",
#         width="100%",
#         align="CENTER"
#     )

def doctor_card_v41(doctor: rx.Var) -> rx.Component:
    """👨‍⚕️ Card de doctor modular v4.1 - Componente contenedor principal"""
    return rx.box(
        rx.vstack(
            # Header con avatar, nombre, especialidad y estado
            doctor_header(doctor),
            # Divider
            rx.box(
                width="100%",
                height="2px",
                background=f"linear-gradient(90deg, transparent 0%, {COLORS['primary']['400']}80 50%, transparent 100%)",
                border_radius="2px",
                box_shadow=f"0 0 8px {COLORS['primary']['400']}40"
            ),
            
            # Cola de pacientes
            # patient_queue(doctor.id),
            patient_queue_header(doctor.id),
            patient_queue_area(doctor.id),
            spacing="3",
            width="100%",
            align="center"
        ),
        style={
            "background": f"rgba(26, 31, 46, 0.8)",
            "border": f"1px solid {"rgba(255, 255, 255, 0.1)"}",
            "border_radius": RADIUS["xl"],
            "padding": SPACING["5"],
            "min_height": "500px",
            "backdrop_filter": "blur(20px)",
            "transition": "all 0.4s ease",
            "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "_hover": {
                "transform": "translateY(-4px)",
                "box_shadow": f"0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15)",
                "border_color": DARK_THEME["colors"]["border_strong"]
            },
            "_before": {
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "height": "2px",
                "background": f"linear-gradient(90deg, transparent 0%, {COLORS["primary"][ "600"]} 50%, transparent 100%)",
                "opacity": "0.9",
                "box_shadow": f"0 0 8px {COLORS["primary"][ "600"]}60"
            }
        },
        width="100%"
    )

def modal_transferir_paciente() -> rx.Component:
    """🔄 MODAL PARA TRANSFERIR PACIENTE - VERSIÓN ENTERPRISE MEJORADA"""
    return rx.dialog.root(
        rx.dialog.content(
            # Header elegante con glassmorphism
            rx.vstack(
                rx.hstack(
                    form_section_header(
                        "Transferir Paciente",
                        "Cambiar odontólogo asignado a la consulta",
                        "arrow-right-left",
                        COLORS["blue"]["500"]
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=20),
                            style={
                                "background": "transparent",
                                "border": "none",
                                "color": COLORS["gray"]["500"],
                                "cursor": "pointer",
                                "_hover": {"color": COLORS["gray"]["700"]}
                            }
                        )
                    ),
                    width="100%",
                    align="center"
                ),
                spacing="4",
                width="100%"
            ),
            
            # Formulario mejorado
            rx.form(
                rx.vstack(
                    # Info del paciente con feedback visual mejorado
                    rx.cond(
                        AppState.consulta_para_transferir,
                        rx.vstack(
                            rx.text(
                                "Información del Paciente",
                                style={
                                    "font_size": "1rem",
                                    "font_weight": "600",
                                    "color": DARK_THEME["colors"]["text_primary"],
                                    "margin_bottom": SPACING["2"]
                                }
                            ),
                            success_feedback(
                                rx.text(
                                    rx.cond(
                                        AppState.consulta_para_transferir.orden_cola_odontologo,
                                        f"Paciente: {AppState.consulta_para_transferir.paciente_nombre} | Posición: #{AppState.consulta_para_transferir.orden_cola_odontologo}",
                                        f"Paciente: {AppState.consulta_para_transferir.paciente_nombre} | Posición: #1"
                                    )
                                ),
                                "user-check"
                            ),
                            spacing="2",
                            width="100%"
                        ),
                        rx.box()
                    ),
                    
                    # Selector dinámico de odontólogo 
                    enhanced_form_field_dinamico(
                        label="Odontólogo de Destino",
                        field_name="odontologo_destino",
                        value=rx.cond(AppState.odontologo_destino_seleccionado, AppState.odontologo_destino_seleccionado, ""),
                        # 🔄 ACTUALIZADO: Usar gestionar_modal_operacion
                        on_change=lambda field, value: AppState.gestionar_modal_operacion("set_odontologo_destino", datos={"odontologo_id": value}),
                        placeholder="Seleccionar odontólogo de destino...",
                        required=True,
                        icon="user-round",
                        help_text="Odontólogo que recibirá al paciente",
                        validation_error=""
                    ),
                    
                    # Campo de justificación mejorado
                    enhanced_form_field(
                        label="Motivo de la Transferencia",
                        field_name="motivo_transferencia",
                        value=rx.cond(AppState.motivo_transferencia, AppState.motivo_transferencia, ""),
                        # 🔄 ACTUALIZADO: Usar gestionar_modal_operacion
                        on_change=lambda field, value: AppState.gestionar_modal_operacion("set_motivo_transferencia", datos={"motivo": value}),
                        field_type="textarea",
                        placeholder="Explique por qué se transfiere al paciente...",
                        required=True,
                        icon="file-text",
                        help_text="Justificación requerida para transferencias",
                        max_length=500,
                        validation_error=""
                    ),
                    # Botones de navegación mejorados
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", size=16),
                                    rx.text("Cancelar"),
                                    spacing="2",
                                    align="center"
                                ),
                                style={
                                    **GLASS_EFFECTS["light"],
                                    "border": f"1px solid {COLORS['gray']['300']}",
                                    "color": COLORS["gray"]["700"],
                                    "border_radius": RADIUS["xl"],
                                    "padding": f"{SPACING['3']} {SPACING['5']}",
                                    "font_weight": "600",
                                    "transition": ANIMATIONS["presets"]["crystal_hover"],
                                    "_hover": {
                                        **GLASS_EFFECTS["medium"],
                                        "transform": "translateY(-2px)",
                                        "box_shadow": SHADOWS["sm"]
                                    }
                                },
                                # 🔄 CORREGIDO: cerrar_modal_transferir_paciente → gestionar_modal_operacion
                                on_click=lambda: AppState.gestionar_modal_operacion("cerrar_transferencia")
                            )
                        ),
                        
                        rx.spacer(),
                        
                        rx.button(
                            rx.hstack(
                                rx.text("Transferir Paciente"),
                                rx.icon("arrow-right-left", size=16),
                                spacing="2",
                                align="center"
                            ),
                            style={
                                "background": f"linear-gradient(135deg, {COLORS['blue']['500']}, {COLORS['blue']['600']})",
                                "color": "white",
                                "border": "none",
                                "border_radius": RADIUS["xl"],
                                "padding": f"{SPACING['3']} {SPACING['6']}",
                                "font_weight": "700",
                                "font_size": "1rem",
                                "box_shadow": f"0 0 20px {COLORS['blue']['500']}40",
                                "transition": ANIMATIONS["presets"]["crystal_hover"],
                                "_hover": {
                                    "transform": "translateY(-2px) scale(1.02)",
                                    "box_shadow": f"0 0 30px {COLORS['blue']['500']}50, {SHADOWS['crystal_lg']}"
                                },
                                "_disabled": {
                                    "opacity": "0.6",
                                    "cursor": "not-allowed",
                                    "transform": "none"
                                }
                            },
                            on_click=AppState.ejecutar_transferencia_paciente
                        ),
                        
                        width="100%",
                        align="center",
                        margin_top=SPACING["8"]
                    ),
                    
                    spacing="6",
                    width="100%",
                    align="start"
                ),
            ),
            
            style={
                "max_width": "600px",
                "width": "90vw",
                "max_height": "90vh",
                "padding": SPACING["8"],
                "border_radius": RADIUS["3xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['blue']['200']}30",
                "overflow_y": "auto",
                "backdrop_filter": "blur(20px)"
            }
        ),
        open=AppState.modal_transferir_paciente_abierto,
        on_open_change=lambda open: rx.cond(~open, AppState.gestionar_modal_operacion("cerrar_transferencia"), rx.noop())
    )

def clean_consultas_page_header() -> rx.Component:
    """📋 Header limpio para página de consultas (igual que personal/pacientes)"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                # Título principal con gradiente (igual que personal)
                rx.heading(
                    "Gestión de Consultas",
                    style={
                        "font_size": "2.75rem",
                        "font_weight": "800",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent",
                        "line_height": "1.2",
                        "text_align": "left"
                    }
                ),
                
                # Subtítulo elegante (igual que personal)
                rx.text(
                    "Monitoreo en tiempo real del flujo de pacientes por orden de llegada",
                    style={
                        "font_size": "1.125rem",
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "line_height": "1.5"
                    }
                ),
                
                spacing="1",
                justify="start",
                align="start"
            ),
            
            width="100%",
            align="center"
        ),
        style=dark_header_style(),
        width="100%"
    )

def consultas_page_v41() -> rx.Component:
    """📅 Página de consultas V4.1 con estilo consistente"""
    return rx.fragment(
        # Modal de nueva consulta
        modal_nueva_consulta(),
        
        # Modal de transferir paciente
        modal_transferir_paciente(),
        
        # Botón flotante
        boton_nueva_consulta_flotante(),
        
        # Layout principal usando el wrapper (igual que personal/pacientes)
        medical_page_layout(
            rx.vstack(
                # Header limpio y elegante (igual que personal/pacientes)
                clean_consultas_page_header(),
                
                # Panel de control superior con estadísticas
                queue_control_bar_simple(),
                
                # Grid de odontólogos mejorado
                rx.cond(
                    AppState.odontologos_disponibles.length() > 0,
                    rx.grid(
                        rx.foreach(
                            AppState.odontologos_disponibles,
                            lambda doctor: doctor_card_v41(doctor)
                        ),
                        columns={
                            "base": "1",     # Móvil: 1 columna
                            "md": "2",       # Tablet: 2 columnas  
                            "lg": "3",       # Desktop: 3 columnas
                            "xl": "4"        # Pantallas grandes: 4 columnas
                        },
                        gap=SPACING["8"],
                        width="100%"
                    ),
                    # Estado vacío
                    rx.box(
                        rx.vstack(
                            rx.icon("user-x", size=64, color=DARK_THEME["colors"]["text_muted"]),
                            rx.text(
                                "No hay odontólogos disponibles",
                                color=DARK_THEME["colors"]["text_primary"],
                                size="5",
                                font_weight="700",
                                style={"text_align": "center"}
                            ),
                            rx.text(
                                "Contacte al administrador para configurar el personal médico",
                                color=DARK_THEME["colors"]["text_secondary"],
                                size="3",
                                style={"text_align": "center"}
                            ),
                            spacing="4",
                            align="center"
                        ),
                        style={
                            "padding": SPACING["16"],
                            "text_align": "center",
                            "background": f"rgba(26, 31, 46, 0.8)",
                            "border": f"2px dashed {DARK_THEME["colors"]["border"]}",
                            "border_radius": RADIUS["2xl"],
                            "backdrop_filter": "blur(10px)",
                            "margin": f"{SPACING['8']} 0"
                        }
                    )
                ),
                
                spacing="3",
                width="100%"
            )
        )
    )