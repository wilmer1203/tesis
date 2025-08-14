"""
📅 PÁGINA DE CONSULTAS REDISEÑADA - TEMA OSCURO
===============================================

🌟 Características del nuevo diseño:
- Tema oscuro profesional con efectos glassmorphism
- Layout por odontólogo (NO tabla tradicional)
- Cards de pacientes con estados visuales
- Columna de resumen lateral
- Header con contadores integrados
- Modal optimizado para nueva consulta
- Diseño responsive mobile-first

✨ CONSULTAS POR ORDEN DE LLEGADA (NO citas programadas)
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button
from dental_system.styles.themes import (
    COLORS, 
    SHADOWS, 
    RADIUS, 
    SPACING, 
    ANIMATIONS, 
    DARK_THEME,
    GRADIENTS,
    GLASS_EFFECTS,
    dark_page_background,
    dark_crystal_card,
    dark_header_style
)

# ==========================================
# 🎨 CONSTANTES CSS CENTRALIZADAS
# ==========================================

# 🎨 Colores especializados para consultas
CONSULTAS_COLORS = {
    "primary_gradient": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
    "warning_gradient": f"linear-gradient(135deg, {COLORS['warning']['500']} 0%, #F59E0B 100%)",
    "success_gradient": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, #10B981 100%)",
    "danger_gradient": f"linear-gradient(135deg, #EF4444 0%, #DC2626 100%)",
    "surface_subtle": f"rgba({DARK_THEME['colors']['surface']}, 0.3)",
    "surface_hover": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
    "border_subtle": f"rgba({DARK_THEME['colors']['border']}, 0.2)",
    "border_hover": f"rgba({DARK_THEME['colors']['border']}, 0.4)",
    "divider_gradient": f"linear-gradient(90deg, transparent 0%, rgba({DARK_THEME['colors']['border']}, 0.6) 50%, transparent 100%)"
}

# 📏 Espaciado reutilizable
CONSULTAS_SPACING = {
    "card_padding": SPACING["5"],
    "section_padding": SPACING["4"],
    "compact_padding": f"{SPACING['2']} {SPACING['3']}",
    "button_padding": f"{SPACING['4']} {SPACING['8']}",
    "divider_margin": f"{SPACING['4']} 0",
    "header_margin": SPACING["8"],
    "card_margin": SPACING["4"]
}

# 🔘 Radius centralizados
CONSULTAS_RADIUS = {
    "card": RADIUS["lg"],
    "compact": RADIUS["md"],
    "button": RADIUS["xl"],
    "badge": RADIUS["full"]
}

# 📝 Tipografía especializada
CONSULTAS_TEXT = {
    "header_large": {
        "font_size": "1.5rem",
        "font_weight": "700",
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "header_medium": {
        "font_size": "1.1rem",
        "font_weight": "700", 
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "header_small": {
        "font_size": "1rem",
        "font_weight": "600",
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "body_primary": {
        "font_size": "0.9rem",
        "font_weight": "600",
        "color": DARK_THEME["colors"]["text_primary"]
    },
    "body_secondary": {
        "font_size": "0.85rem",
        "color": DARK_THEME["colors"]["text_secondary"]
    },
    "body_accent": {
        "font_size": "0.85rem",
        "font_weight": "500",
        "color": DARK_THEME["colors"]["accent"]
    },
    "caption": {
        "font_size": "0.8rem",
        "color": DARK_THEME["colors"]["text_secondary"]
    },
    "badge": {
        "color": "white",
        "font_weight": "700",
        "font_size": "0.9rem"
    }
}

# 🎭 Efectos y animaciones
CONSULTAS_EFFECTS = {
    "card_hover": {
        "transform": "translateY(-2px)",
        "box_shadow": f"0 8px 25px rgba({DARK_THEME['colors']['shadow']}, 0.3)",
        "border_color": CONSULTAS_COLORS["border_hover"]
    },
    "button_hover": {
        "box_shadow": f"0 12px 40px {DARK_THEME['colors']['primary']}60",
        "transform": "translateY(-1px)"
    },
    "compact_hover": {
        "background": CONSULTAS_COLORS["surface_hover"],
        "border_color": CONSULTAS_COLORS["border_hover"]
    }
}

# ==========================================
# 🌙 COMPONENTES DEL TEMA OSCURO
# ==========================================

def dark_consultas_header() -> rx.Component:
    """🌟 Header oscuro con contadores integrados"""
    return rx.box(
        rx.vstack(
            # Título principal
            rx.heading(
                "Sistema de Consultas",
                style={
                    **dark_header_style(),
                    "font_size": "3rem",
                    "background": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
                    "background_clip": "text",
                    "color": "transparent",
                    "margin_bottom": SPACING["2"]
                }
            ),
            
            # Subtítulo
            rx.text(
                "Gestión por orden de llegada - Sin citas programadas",
                style={
                    "color": DARK_THEME["colors"]["text_secondary"],
                    "font_size": "1.1rem",
                    "margin_bottom": SPACING["6"]
                }
            ),
            
            # Contadores del día
            header_status_counters(),
            
            # Botón Nueva Consulta
            rx.button(
                rx.hstack(
                    rx.icon("calendar-plus", size=20),
                    rx.text("Nueva Consulta", font_weight="600"),
                    spacing="3",
                    align="center"
                ),
                on_click=lambda: AppState.abrir_modal_consulta(""),
                style={
                    "background": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
                    "color": "white",
                    "border": "none",
                    "border_radius": RADIUS["xl"],
                    "padding": f"{SPACING['4']} {SPACING['8']}",
                    "font_size": "1.1rem",
                    "font_weight": "600",
                    "box_shadow": f"0 8px 32px {DARK_THEME['colors']['primary']}40",
                    "transition": ANIMATIONS["presets"]["button_hover"],
                    "_hover": {
                        "transform": "translateY(-2px)",
                        "box_shadow": f"0 12px 40px {DARK_THEME['colors']['primary']}60",
                    }
                }
            ),
            
            spacing="6",
            align="center",
            width="100%"
        ),
        style={
            **dark_crystal_card(),
            "margin_bottom": SPACING["8"],
            "text_align": "center"
        }
    )

def header_status_counters() -> rx.Component:
    """📊 Contadores de estado en el header"""
    return rx.grid(
        # Total del día
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("calendar", size=20, color="white"),
                        style={
                            "background": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['primary']} 100%)",
                            "border_radius": RADIUS["lg"],
                            "padding": SPACING["3"]
                        }
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.consultas_list.length(),
                            style={
                                "font_size": "2rem",
                                "font_weight": "800",
                                "color": DARK_THEME["colors"]["text_primary"],
                                "line_height": "1"
                            }
                        ),
                        rx.text(
                            "Total Hoy",
                            style={
                                "font_size": "0.9rem",
                                "color": DARK_THEME["colors"]["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align="center"
                ),
                spacing="2",
                width="100%"
            ),
            style={
                **dark_crystal_card(),
                "padding": SPACING["4"]
            }
        ),
        
        # En proceso
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("activity", size=20, color="white"),
                        style={
                            "background": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
                            "border_radius": RADIUS["lg"],
                            "padding": SPACING["3"]
                        }
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.consultas_en_progreso,
                            style={
                                "font_size": "2rem",
                                "font_weight": "800",
                                "color": DARK_THEME["colors"]["text_primary"],
                                "line_height": "1"
                            }
                        ),
                        rx.text(
                            "En Proceso",
                            style={
                                "font_size": "0.9rem",
                                "color": DARK_THEME["colors"]["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align="center"
                ),
                spacing="2",
                width="100%"
            ),
            style={
                **dark_crystal_card(),
                "padding": SPACING["4"]
            }
        ),
        
        # Completadas
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("check-check", size=20, color="white"),
                        style={
                            "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, #10B981 100%)",
                            "border_radius": RADIUS["lg"],
                            "padding": SPACING["3"]
                        }
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.consultas_completadas,
                            style={
                                "font_size": "2rem",
                                "font_weight": "800",
                                "color": DARK_THEME["colors"]["text_primary"],
                                "line_height": "1"
                            }
                        ),
                        rx.text(
                            "Completadas",
                            style={
                                "font_size": "0.9rem",
                                "color": DARK_THEME["colors"]["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align="center"
                ),
                spacing="2",
                width="100%"
            ),
            style={
                **dark_crystal_card(),
                "padding": SPACING["4"]
            }
        ),
        
        # Canceladas
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("x-circle", size=20, color="white"),
                        style={
                            "background": f"linear-gradient(135deg, {COLORS['error']['500']} 0%, #DC2626 100%)",
                            "border_radius": RADIUS["lg"],
                            "padding": SPACING["3"]
                        }
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.consultas_canceladas,
                            style={
                                "font_size": "2rem",
                                "font_weight": "800",
                                "color": DARK_THEME["colors"]["text_primary"],
                                "line_height": "1"
                            }
                        ),
                        rx.text(
                            "Canceladas",
                            style={
                                "font_size": "0.9rem",
                                "color": DARK_THEME["colors"]["text_secondary"]
                            }
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align="center"
                ),
                spacing="2",
                width="100%"
            ),
            style={
                **dark_crystal_card(),
                "padding": SPACING["4"]
            }
        ),
        
        columns=rx.breakpoints(initial="2", md="4"),
        spacing="6",
        width="100%"
    )

# ==========================================
# 🦷 LAYOUT POR ODONTÓLOGO
# ==========================================

def consultas_by_odontologo_layout() -> rx.Component:
    """🏥 Layout principal organizado por odontólogo - TODOS LOS ODONTÓLOGOS"""
    return rx.grid(
        # Columna 1: Odontólogos impares (1, 3, 5, 7...)
        rx.vstack(
            rx.foreach(
                AppState.odontologos_list,
                lambda odontologo, index: rx.cond(
                    index % 2 == 0,  # Índices pares (0, 2, 4...) = Odontólogos 1, 3, 5...
                    odontologo_section_card(odontologo, index),
                    rx.box()
                )
            ),
            spacing="6",
            width="100%"
        ),
        
        # Columna 2: Odontólogos pares (2, 4, 6, 8...)
        rx.vstack(
            rx.foreach(
                AppState.odontologos_list,
                lambda odontologo, index: rx.cond(
                    index % 2 == 1,  # Índices impares (1, 3, 5...) = Odontólogos 2, 4, 6...
                    odontologo_section_card(odontologo, index),
                    rx.box()
                )
            ),
            spacing="6",
            width="100%"
        ),
        
        # Columna 3: Resumen completo del día (altura completa)
        resumen_completo_column(),
        
        columns=rx.breakpoints(initial="1", md="3"),
        spacing="6",
        width="100%",
        min_height="600px",
        align_items="start"
    )

def odontologo_section_card(odontologo: rx.Var[dict], index: rx.Var[int]) -> rx.Component:
    """👨‍⚕️ Tarjeta unificada de odontólogo con divisor único"""
    return rx.box(
        rx.vstack(
            # ========== HEADER DEL ODONTÓLOGO ==========
            rx.hstack(
                # Avatar del odontólogo
                rx.box(
                    rx.icon("user-round", size=24, color="white"),
                    style={
                        "background": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
                        "border_radius": RADIUS["full"],
                        "padding": SPACING["3"]
                    }
                ),
                
                # Información personal
                rx.vstack(
                    rx.text(
                        odontologo.primer_nombre + " " + odontologo.primer_apellido,
                        style={
                            "font_weight": "700",
                            "font_size": "1.1rem",
                            "color": DARK_THEME["colors"]["text_primary"]
                        }
                    ),
                    rx.text(
                        f"CC: {odontologo.numero_documento}",
                        style={
                            "color": DARK_THEME["colors"]["text_secondary"],
                            "font_size": "0.85rem"
                        }
                    ),
                    rx.text(
                        odontologo.especialidad,
                        style={
                            "color": DARK_THEME["colors"]["accent"],
                            "font_size": "0.85rem",
                            "font_weight": "500"
                        }
                    ),
                    spacing="1",
                    align_items="start"
                ),
                
                rx.spacer(),
                
                # Badge de consultas pendientes
                rx.box(
                    rx.text(
                        AppState.get_consultas_pendientes_odontologo.get(odontologo.id, 0),
                        style={
                            "color": "white",
                            "font_weight": "700",
                            "font_size": "0.9rem"
                        }
                    ),
                    style={
                        "background": f"linear-gradient(135deg, {COLORS['warning']['500']} 0%, #F59E0B 100%)",
                        "border_radius": RADIUS["full"],
                        "padding": f"{SPACING['2']} {SPACING['3']}",
                        "min_width": "32px",
                        "text_align": "center"
                    }
                ),
                
                spacing="4",
                align="center",
                width="100%"
            ),
            
            # ========== DIVISOR ÚNICO ==========
            rx.box(
                style={
                    "width": "100%",
                    "height": "1px",
                    "background": f"linear-gradient(90deg, transparent 0%, rgba({DARK_THEME['colors']['border']}, 0.6) 50%, transparent 100%)",
                    "margin": f"{SPACING['4']} 0"
                }
            ),
            
            # ========== SECCIÓN DE PACIENTES ==========
            rx.vstack(
                # Título de la sección
                rx.hstack(
                    rx.text(
                        "Pacientes en Cola",
                        style={
                            "font_weight": "600",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_size": "1rem"
                        }
                    ),
                    rx.spacer(),
                    rx.box(
                        rx.text(
                            AppState.get_consultas_pendientes_odontologo.get(odontologo.id, 0),
                            style={
                                "color": DARK_THEME["colors"]["text_secondary"],
                                "font_size": "0.85rem",
                                "font_weight": "500"
                            }
                        ),
                        style={
                            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
                            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.3)",
                            "border_radius": RADIUS["md"],
                            "padding": f"{SPACING['1']} {SPACING['3']}"
                        }
                    ),
                    width="100%",
                    align="center",
                    margin_bottom=SPACING["3"]
                ),
                
                # Lista de consultas optimizada
                rx.cond(
                    AppState.consultas_por_odontologo.get(odontologo.id, []),
                    rx.vstack(
                        rx.foreach(
                            AppState.consultas_por_odontologo.get(odontologo.id, []),
                            patient_consultation_card
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    # Estado vacío con diseño mejorado
                    rx.box(
                        rx.vstack(
                            rx.icon("calendar-x", size=28, color=DARK_THEME["colors"]["text_secondary"]),
                            rx.text(
                                "No hay consultas programadas",
                                style={
                                    "color": DARK_THEME["colors"]["text_secondary"],
                                    "text_align": "center",
                                    "font_style": "italic",
                                    "font_size": "0.9rem"
                                }
                            ),
                            spacing="2",
                            align="center"
                        ),
                        style={
                            "padding": SPACING["6"],
                            "text_align": "center"
                        }
                    )
                ),
                
                spacing="3",
                width="100%"
            ),
            
            spacing="0",
            width="100%"
        ),
        style={
            **dark_crystal_card(),
            "padding": SPACING["5"],
            "min_height": "300px"
        }
    )

def patient_consultation_card(consulta: rx.Var[dict]) -> rx.Component:
    """👤 Card individual de paciente con acciones"""
    return rx.box(
        rx.vstack(
            # Información del paciente
            rx.hstack(
                rx.vstack(
                    rx.text(
                        consulta.paciente_nombre,
                        style={
                            "font_weight": "600",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_size": "1rem"
                        }
                    ),
                    rx.text(
                        f"CC: {consulta.paciente_documento}",
                        style={
                            "color": DARK_THEME["colors"]["text_secondary"],
                            "font_size": "0.9rem"
                        }
                    ),
                    spacing="1",
                    align_items="start"
                ),
                rx.spacer(),
                # Badge de estado
                consultation_status_badge(consulta.estado),
                spacing="3",
                align="center",
                width="100%"
            ),
            
            # Botones de acción
            rx.hstack(
                # Botón iniciar consulta
                rx.cond(
                    consulta.estado == "programada",
                    rx.button(
                        rx.icon("play-circle", size=16),
                        size="2",
                        style={
                            "background": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
                            "color": "white",
                            "border": "none",
                            "_hover": {
                                "transform": "scale(1.05)",
                                "box_shadow": f"0 4px 12px {DARK_THEME['colors']['primary']}60"
                            }
                        },
                        on_click=lambda: AppState.cambiar_estado_consulta(consulta.id, "en_curso")
                    ),
                    rx.box()
                ),
                
                rx.spacer(),
                
                # Botón cancelar
                rx.button(
                    rx.icon("x-circle", size=16),
                    size="2",
                    style={
                        "background": "transparent",
                        "color": COLORS['error']['500'],
                        "border": f"1px solid {COLORS['error']['500']}",
                        "_hover": {
                            "background": f"{COLORS['error']['500']}20",
                            "transform": "scale(1.05)"
                        }
                    },
                    on_click=lambda: AppState.confirmar_cancelar_consulta(consulta.id)
                ),
                
                width="100%",
                align="center"
            ),
            
            spacing="3",
            width="100%"
        ),
        style={
            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.3)",
            "backdrop_filter": "blur(10px)",
            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.2)",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "transition": ANIMATIONS["presets"]["button_hover"],
            "_hover": {
                "transform": "translateY(-2px)",
                "box_shadow": f"0 8px 25px rgba({DARK_THEME['colors']['shadow']}, 0.3)",
                "border_color": f"rgba({DARK_THEME['colors']['border']}, 0.4)"
            }
        },
        width="100%"
    )

def consultation_status_badge(estado: rx.Var[str]) -> rx.Component:
    """🏷️ Badge colorido para el estado de la consulta"""
    return rx.cond(
        estado == "programada",
        rx.box(
            rx.text(
                "En Espera",
                style={
                    "color": "white",
                    "font_weight": "600",
                    "font_size": "0.8rem"
                }
            ),
            style={
                "background": f"linear-gradient(135deg, {COLORS['warning']['500']} 0%, #F59E0B 100%)",
                "border_radius": RADIUS["full"],
                "padding": f"{SPACING['1']} {SPACING['3']}"
            }
        ),
        rx.cond(
            estado == "en_curso",
            rx.box(
                rx.text(
                    "En Proceso",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "font_size": "0.8rem"
                    }
                ),
                style={
                    "background": f"linear-gradient(135deg, {DARK_THEME['colors']['primary']} 0%, {DARK_THEME['colors']['accent']} 100%)",
                    "border_radius": RADIUS["full"],
                    "padding": f"{SPACING['1']} {SPACING['3']}"
                }
            ),
            rx.box(
                rx.text(
                    "Completada",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "font_size": "0.8rem"
                    }
                ),
                style={
                    "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, #10B981 100%)",
                    "border_radius": RADIUS["full"],
                    "padding": f"{SPACING['1']} {SPACING['3']}"
                }
            )
        )
    )

def compact_consultation_card(consulta: rx.Var[dict]) -> rx.Component:
    """📋 Tarjeta compacta de consulta para la columna de resumen"""
    return rx.box(
        rx.hstack(
            # Información básica del paciente
            rx.vstack(
                rx.text(
                    consulta.paciente_nombre,
                    style={
                        "font_weight": "600",
                        "font_size": "0.9rem",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                rx.text(
                    f"Dr. {consulta.odontologo_nombre}",
                    style={
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "font_size": "0.8rem"
                    }
                ),
                spacing="1",
                align_items="start"
            ),
            
            rx.spacer(),
            
            # Hora de la consulta
            rx.text(
                consulta.hora_display,
                style={
                    "color": DARK_THEME["colors"]["accent"],
                    "font_size": "0.8rem",
                    "font_weight": "500"
                }
            ),
            
            spacing="3",
            align="center",
            width="100%"
        ),
        style={
            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.3)",
            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.2)",
            "border_radius": RADIUS["md"],
            "padding": f"{SPACING['2']} {SPACING['3']}",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
                "border_color": f"rgba({DARK_THEME['colors']['border']}, 0.4)"
            }
        },
        width="100%"
    )

# ==========================================
# 📊 COLUMNA DE RESUMEN
# ==========================================

def resumen_completo_column() -> rx.Component:
    """📊 Columna de resumen completo del día - Solo completadas y canceladas"""
    return rx.box(
        rx.vstack(
            # Header del resumen
            rx.box(
                rx.vstack(
                    rx.text(
                        "Resumen del Día",
                        style={
                            "font_weight": "700",
                            "font_size": "1.5rem",
                            "color": DARK_THEME["colors"]["text_primary"]
                        }
                    ),
                    rx.text(
                        "Consultas finalizadas y cancelaciones",
                        style={
                            "color": DARK_THEME["colors"]["text_secondary"],
                            "font_size": "0.9rem"
                        }
                    ),
                    spacing="2",
                    align="center",
                    width="100%"
                ),
                style={
                    **dark_crystal_card(),
                    "padding": SPACING["4"],
                    "text_align": "center",
                    "margin_bottom": SPACING["6"]
                }
            ),
            
            # ✅ SECCIÓN COMPLETADAS
            rx.box(
                rx.vstack(
                    # Header de completadas
                    rx.hstack(
                        rx.box(
                            rx.icon("check-check", size=20, color="white"),
                            style={
                                "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, #10B981 100%)",
                                "border_radius": RADIUS["lg"],
                                "padding": SPACING["3"]
                            }
                        ),
                        rx.vstack(
                            rx.text(
                                AppState.consultas_completadas,
                                style={
                                    "font_size": "1.8rem",
                                    "font_weight": "800",
                                    "color": DARK_THEME["colors"]["text_primary"],
                                    "line_height": "1"
                                }
                            ),
                            rx.text(
                                "Completadas",
                                style={
                                    "color": DARK_THEME["colors"]["text_secondary"],
                                    "font_size": "0.9rem"
                                }
                            ),
                            spacing="1",
                            align_items="start"
                        ),
                        rx.spacer(),
                        rx.box(
                            rx.icon("chevron-right", size=16, color=DARK_THEME["colors"]["text_secondary"]),
                            style={
                                "cursor": "pointer",
                                "transition": "transform 0.2s",
                                "_hover": {"transform": "translateX(2px)"}
                            }
                        ),
                        spacing="3",
                        align="center",
                        width="100%"
                    ),
                    
                    # Divider
                    rx.divider(
                        color=f"rgba({DARK_THEME['colors']['border']}, 0.3)", 
                        margin=f"{SPACING['3']} 0"
                    ),
                    
                    # Lista de consultas completadas (REAL DATA)
                    rx.cond(
                        AppState.consultas_completadas_list,
                        rx.vstack(
                            rx.foreach(
                                AppState.consultas_completadas_list,
                                compact_consultation_card
                            ),
                            spacing="2",
                            width="100%"
                        ),
                        # Estado vacío si no hay completadas
                        rx.box(
                            rx.vstack(
                                rx.icon("check-circle-2", size=24, color=DARK_THEME["colors"]["text_secondary"]),
                                rx.text(
                                    "No hay consultas completadas hoy",
                                    style={
                                        "color": DARK_THEME["colors"]["text_secondary"],
                                        "font_size": "0.9rem",
                                        "text_align": "center",
                                        "font_style": "italic"
                                    }
                                ),
                                spacing="2",
                                align="center"
                            ),
                            style={"padding": SPACING["4"]}
                        )
                    ),
                    
                    spacing="3",
                    width="100%"
                ),
                style={
                    **dark_crystal_card(),
                    "padding": SPACING["5"],
                    "margin_bottom": SPACING["6"]
                }
            ),
            
            # ❌ SECCIÓN CANCELADAS
            rx.box(
                rx.vstack(
                    # Header de canceladas
                    rx.hstack(
                        rx.box(
                            rx.icon("x-circle", size=20, color="white"),
                            style={
                                "background": f"linear-gradient(135deg, {COLORS['error']['500']} 0%, #DC2626 100%)",
                                "border_radius": RADIUS["lg"],
                                "padding": SPACING["3"]
                            }
                        ),
                        rx.vstack(
                            rx.text(
                                AppState.consultas_canceladas,
                                style={
                                    "font_size": "1.8rem",
                                    "font_weight": "800",
                                    "color": DARK_THEME["colors"]["text_primary"],
                                    "line_height": "1"
                                }
                            ),
                            rx.text(
                                "Canceladas",
                                style={
                                    "color": DARK_THEME["colors"]["text_secondary"],
                                    "font_size": "0.9rem"
                                }
                            ),
                            spacing="1",
                            align_items="start"
                        ),
                        rx.spacer(),
                        rx.box(
                            rx.icon("chevron-right", size=16, color=DARK_THEME["colors"]["text_secondary"]),
                            style={
                                "cursor": "pointer",
                                "transition": "transform 0.2s",
                                "_hover": {"transform": "translateX(2px)"}
                            }
                        ),
                        spacing="3",
                        align="center",
                        width="100%"
                    ),
                    
                    # Divider
                    rx.divider(
                        color=f"rgba({DARK_THEME['colors']['border']}, 0.3)", 
                        margin=f"{SPACING['3']} 0"
                    ),
                    
                    # Lista de consultas canceladas (REAL DATA)
                    rx.cond(
                        AppState.consultas_canceladas_list,
                        rx.vstack(
                            rx.foreach(
                                AppState.consultas_canceladas_list,
                                compact_consultation_card
                            ),
                            spacing="2",
                            width="100%"
                        ),
                        # Estado vacío si no hay canceladas
                        rx.box(
                            rx.vstack(
                                rx.icon("calendar-x", size=24, color=DARK_THEME["colors"]["text_secondary"]),
                                rx.text(
                                    "No hay cancelaciones hoy",
                                    style={
                                        "color": DARK_THEME["colors"]["text_secondary"],
                                        "font_size": "0.9rem",
                                        "text_align": "center",
                                        "font_style": "italic"
                                    }
                                ),
                                spacing="2",
                                align="center"
                            ),
                            style={"padding": SPACING["4"]}
                        )
                    ),
                    
                    spacing="3",
                    width="100%"
                ),
                style={
                    **dark_crystal_card(),
                    "padding": SPACING["5"]
                }
            ),
            
            spacing="0",
            width="100%"
        ),
        width="100%",
        height="100%"
    )

def consulta_completada_card(consulta: rx.Var[dict]) -> rx.Component:
    """✅ Card para consulta completada"""
    return rx.box(
        rx.vstack(
            # Info principal
            rx.hstack(
                rx.box(
                    rx.icon("check", size=16, color=COLORS['success']['500']),
                    style={
                        "background": f"rgba({COLORS['success']['500']}, 0.1)",
                        "border_radius": RADIUS["full"],
                        "padding": SPACING["2"],
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                rx.vstack(
                    rx.text(
                        consulta.paciente_nombre,
                        style={
                            "font_weight": "600",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_size": "0.9rem"
                        }
                    ),
                    rx.text(
                        consulta.servicio_realizado,
                        style={
                            "color": DARK_THEME["colors"]["text_secondary"],
                            "font_size": "0.8rem"
                        }
                    ),
                    spacing="1",
                    align_items="start"
                ),
                rx.spacer(),
                rx.text(
                    consulta.hora_fin,
                    style={
                        "color": COLORS['success']['500'],
                        "font_size": "0.8rem",
                        "font_weight": "600"
                    }
                ),
                spacing="3",
                align="center",
                width="100%"
            ),
            
            # Odontólogo
            rx.text(
                f"Dr. {consulta.odontologo_nombre}",
                style={
                    "color": DARK_THEME["colors"]["text_secondary"],
                    "font_size": "0.75rem",
                    "margin_top": SPACING["1"]
                }
            ),
            
            spacing="2",
            width="100%"
        ),
        style={
            "background": f"rgba({COLORS['success']['500']}, 0.05)",
            "border": f"1px solid rgba({COLORS['success']['500']}, 0.2)",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["3"],
            "transition": ANIMATIONS["presets"]["button_hover"],
            "_hover": {
                "background": f"rgba({COLORS['success']['500']}, 0.08)",
                "border_color": f"rgba({COLORS['success']['500']}, 0.3)"
            }
        },
        width="100%"
    )

def consulta_cancelada_card(consulta: rx.Var[dict]) -> rx.Component:
    """❌ Card para consulta cancelada"""
    return rx.box(
        rx.vstack(
            # Info principal
            rx.hstack(
                rx.box(
                    rx.icon("x", size=16, color=COLORS['error']['500']),
                    style={
                        "background": f"rgba({COLORS['error']['500']}, 0.1)",
                        "border_radius": RADIUS["full"],
                        "padding": SPACING["2"],
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                rx.vstack(
                    rx.text(
                        consulta.paciente_nombre,
                        style={
                            "font_weight": "600",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_size": "0.9rem"
                        }
                    ),
                    rx.text(
                        consulta.motivo_consulta,
                        style={
                            "color": DARK_THEME["colors"]["text_secondary"],
                            "font_size": "0.8rem"
                        }
                    ),
                    spacing="1",
                    align_items="start"
                ),
                rx.spacer(),
                rx.text(
                    consulta.hora_programada,
                    style={
                        "color": COLORS['error']['500'],
                        "font_size": "0.8rem",
                        "font_weight": "600"
                    }
                ),
                spacing="3",
                align="center",
                width="100%"
            ),
            
            # Motivo de cancelación
            rx.hstack(
                rx.icon("info", size=12, color=DARK_THEME["colors"]["text_secondary"]),
                rx.text(
                    consulta.motivo_cancelacion or "Sin motivo especificado",
                    style={
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "font_size": "0.75rem",
                        "font_style": "italic"
                    }
                ),
                spacing="2",
                align="center"
            ),
            
            spacing="2",
            width="100%"
        ),
        style={
            "background": f"rgba({COLORS['error']['500']}, 0.05)",
            "border": f"1px solid rgba({COLORS['error']['500']}, 0.2)",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["3"],
            "transition": ANIMATIONS["presets"]["button_hover"],
            "_hover": {
                "background": f"rgba({COLORS['error']['500']}, 0.08)",
                "border_color": f"rgba({COLORS['error']['500']}, 0.3)"
            }
        },
        width="100%"
    )

# ==========================================
# 📱 MODAL OPTIMIZADO
# ==========================================

def dark_consulta_form_modal() -> rx.Component:
    """📝 Modal de nueva consulta con tema oscuro"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Nueva Consulta",
                style={
                    "color": DARK_THEME["colors"]["text_primary"],
                    "font_size": "1.5rem",
                    "font_weight": "700"
                }
            ),
            
            rx.vstack(
                # Búsqueda de paciente
                rx.vstack(
                    rx.text(
                        "Seleccionar Paciente *",
                        style={
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_weight": "600"
                        }
                    ),
                    rx.input(
                        placeholder="🔍 Buscar por nombre o documento...",
                        value=AppState.pacientes_search_modal,
                        on_change=AppState.buscar_pacientes_modal,
                        style={
                            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
                            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.3)",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "_placeholder": {"color": DARK_THEME["colors"]["text_secondary"]}
                        }
                    ),
                    spacing="2",
                    width="100%"
                ),
                
                # Selección de odontólogo
                rx.vstack(
                    rx.text(
                        "Odontólogo *",
                        style={
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_weight": "600"
                        }
                    ),
                    rx.input(
                        placeholder="Seleccionar odontólogo...",
                        value=AppState.consulta_form["odontologo_id"],
                        on_change=lambda v: AppState.update_consulta_form("odontologo_id", v),
                        style={
                            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
                            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.3)",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "_placeholder": {"color": DARK_THEME["colors"]["text_secondary"]}
                        }
                    ),
                    spacing="2",
                    width="100%"
                ),
                
                # Tipo de consulta
                rx.vstack(
                    rx.text(
                        "Tipo de Consulta *",
                        style={
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_weight": "600"
                        }
                    ),
                    rx.input(
                        placeholder="Tipo de consulta...",
                        value=AppState.consulta_form["tipo_consulta"],
                        on_change=lambda v: AppState.update_consulta_form("tipo_consulta", v),
                        style={
                            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
                            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.3)",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "_placeholder": {"color": DARK_THEME["colors"]["text_secondary"]}
                        }
                    ),
                    spacing="2",
                    width="100%"
                ),
                
                # Motivo de consulta
                rx.vstack(
                    rx.text(
                        "Motivo de la Consulta *",
                        style={
                            "color": DARK_THEME["colors"]["text_primary"],
                            "font_weight": "600"
                        }
                    ),
                    rx.text_area(
                        placeholder="¿Por qué viene el paciente?",
                        value=AppState.consulta_form["motivo_consulta"],
                        on_change=lambda v: AppState.update_consulta_form("motivo_consulta", v),
                        rows="3",
                        style={
                            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.5)",
                            "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.3)",
                            "color": DARK_THEME["colors"]["text_primary"],
                            "_placeholder": {"color": DARK_THEME["colors"]["text_secondary"]}
                        }
                    ),
                    spacing="2",
                    width="100%"
                ),
                
                spacing="4",
                width="100%"
            ),
            
            # Botones
            rx.hstack(
                secondary_button(
                    "Cancelar",
                    on_click=lambda: AppState.set_show_consulta_modal(False)
                ),
                primary_button(
                    "Crear Consulta",
                    icon="calendar-plus",
                    on_click=AppState.guardar_consulta,
                    loading=AppState.is_loading_consultas
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="6"
            ),
            
            style={
                "background": DARK_THEME["colors"]["surface"],
                "border": f"1px solid rgba({DARK_THEME['colors']['border']}, 0.2)",
                "box_shadow": f"0 25px 50px rgba({DARK_THEME['colors']['shadow']}, 0.5)",
                "backdrop_filter": "blur(20px)"
            },
            max_width="600px",
            padding="6"
        ),
        open=AppState.show_consulta_modal,
        on_open_change=AppState.set_show_consulta_modal
    )

# ==========================================
# 🚨 SISTEMA DE ALERTAS OSCURO
# ==========================================

def dark_alerts_system() -> rx.Component:
    """🚨 Sistema de alertas con tema oscuro"""
    return rx.vstack(
        # Alerta de éxito
        rx.cond(
            AppState.success_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("check-check", size=20, color=COLORS['success']['500']),
                    rx.text(
                        AppState.success_message,
                        style={
                            "color": COLORS['success']['500'],
                            "font_weight": "500"
                        }
                    ),
                    spacing="3",
                    align="center"
                ),
                style={
                    "background": f"rgba({COLORS['success']['500']}, 0.1)",
                    "border": f"1px solid rgba({COLORS['success']['500']}, 0.2)",
                    "border_left": f"4px solid {COLORS['success']['500']}",
                    "border_radius": RADIUS["lg"],
                    "padding": f"{SPACING['4']} {SPACING['5']}",
                    "margin_bottom": SPACING["4"]
                }
            ),
            rx.box()
        ),
        
        # Alerta de error
        rx.cond(
            AppState.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("triangle-alert", size=20, color=COLORS['error']['500']),
                    rx.text(
                        AppState.error_message,
                        style={
                            "color": COLORS['error']['500'],
                            "font_weight": "500"
                        }
                    ),
                    spacing="3",
                    align="center"
                ),
                style={
                    "background": f"rgba({COLORS['error']['500']}, 0.1)",
                    "border": f"1px solid rgba({COLORS['error']['500']}, 0.2)",
                    "border_left": f"4px solid {COLORS['error']['500']}",
                    "border_radius": RADIUS["lg"],
                    "padding": f"{SPACING['4']} {SPACING['5']}",
                    "margin_bottom": SPACING["4"]
                }
            ),
            rx.box()
        ),
        
        spacing="0",
        width="100%"
    )

# ==========================================
# 🌟 PÁGINA PRINCIPAL REDISEÑADA
# ==========================================

def consultas_page_new() -> rx.Component:
    """
    📅 PÁGINA DE CONSULTAS REDISEÑADA - TEMA OSCURO
    
    🌟 Características del nuevo diseño:
    - Tema oscuro profesional con efectos glassmorphism
    - Layout por odontólogo (NO tabla tradicional)
    - Cards de pacientes con estados visuales
    - Columna de resumen lateral
    - Header con contadores integrados
    - Modal optimizado para nueva consulta
    - Diseño responsive mobile-first
    
    ✨ CONSULTAS POR ORDEN DE LLEGADA (NO citas programadas)
    """
    return rx.box(
        rx.vstack(
            # Header oscuro con contadores
            dark_consultas_header(),
            
            # Sistema de alertas
            dark_alerts_system(),
            
            # Layout principal por odontólogo con loading state
            rx.cond(
                AppState.is_loading_consultas,
                # Loading state mejorado
                rx.box(
                    rx.vstack(
                        rx.spinner(
                            size="3",
                            color=DARK_THEME["colors"]["primary"]
                        ),
                        rx.text(
                            "Cargando consultas...",
                            style=CONSULTAS_TEXT["body_secondary"]
                        ),
                        spacing="4",
                        align="center"
                    ),
                    style={
                        "padding": CONSULTAS_SPACING["header_margin"],
                        "text_align": "center",
                        "min_height": "400px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                # Layout principal cuando los datos están cargados
                consultas_by_odontologo_layout()
            ),
            
            spacing="8",
            width="100%",
            max_width="1400px",
            margin="0 auto",
            padding=f"{SPACING['6']} {SPACING['4']}"
        ),
        
        # Modal de nueva consulta
        dark_consulta_form_modal(),
        
        # Fondo oscuro de la página
        style=dark_page_background(),
        min_height="100vh",
        width="100%"
    )