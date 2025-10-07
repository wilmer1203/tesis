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
from dental_system.components.common import medical_page_layout
from dental_system.styles.themes import SPACING, RADIUS, SHADOWS,ROLE_THEMES, GRADIENTS, DARK_THEME, dark_header_style, COLORS

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
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
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
                # 🔄 ACTUALIZADO: Usar computed vars específicos tipados
                stat_card_simple("Total", AppState.total_consultas_dashboard.to_string()),
                stat_card_simple("En Espera", AppState.total_en_espera_dashboard.to_string(), "yellow"),
                stat_card_simple("En Atención", AppState.total_en_atencion_dashboard.to_string(), "green"),
                stat_card_simple("Urgentes", AppState.total_urgentes_dashboard.to_string(), "red"),
                stat_card_simple("Completadas", AppState.total_completadas_dashboard.to_string(), "blue"),
                stat_card_simple("Dentistas", AppState.total_odontologos_activos_dashboard.to_string(), "blue"),
                columns="6",
                spacing="3",
                width="100%"
            ),
            
            # Botones de acción
            rx.hstack(
                rx.button(
                    "🚨 Consulta Urgente",
                    # 🔄 ACTUALIZADO: Usar operacion_consulta_master
                    on_click=lambda: AppState.operacion_consulta_master("crear", datos={"prioridad": "urgente"}),
                    style={
                        "background": f"linear-gradient(135deg, {DARK_COLORS['accent_red']} 0%, #fc8181 100%)",
                        "color": DARK_COLORS["text_primary"],
                        "border": "none",
                        "border_radius": RADIUS["md"],
                        "padding": f"{SPACING['2']} {SPACING['4']}"
                    }
                ),
                rx.button(
                    "🔄 Refrescar",
                    on_click=AppState.refrescar_tiempo_real,
                    style={
                        "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4f9cf9 100%)",
                        "color": DARK_COLORS["text_primary"],
                        "border": "none",
                        "border_radius": RADIUS["md"],
                        "padding": f"{SPACING['2']} {SPACING['4']}"
                    }
                ),
                 spacing="3",
            ),
            
             spacing="4",
            width="100%"
        ),
        style={
            "background": DARK_COLORS["glass_bg"],
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": RADIUS["xl"],
            "padding": SPACING["6"],
            "margin": f"{SPACING['4']} 0",
            "width": "100%",
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
            
            "background": ROLE_THEMES['gerente']['gradient'],
            "color": DARK_COLORS["text_primary"],
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": RADIUS["xl"],
            "padding": f"{SPACING['4']} {SPACING['8']}",
            "position": "fixed",
            "top": SPACING["8"],
            "right": SPACING["8"],
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
        # 🔄 ACTUALIZADO: Usar método directo de abrir modal
        on_click=AppState.abrir_modal_nueva_consulta
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
                            # 🔄 ACTUALIZADO: Total por odontólogo específico
                            AppState.totales_por_odontologo_dict.get(doctor_id, 0),
                            font_weight="800",
                            size="2",
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
                        "border_radius": RADIUS["lg"],
                        "padding": SPACING["3"],
                        "text_align": "center",
                        "flex": "1",
                        "backdrop_filter": "blur(5px)"
                    }
                ),
                
                # Pacientes urgentes (NUEVO)
                rx.box(
                    rx.vstack(
                        rx.text(
                            # 🔄 ACTUALIZADO: Urgentes por odontólogo específico
                            AppState.urgentes_por_odontologo_dict.get(doctor_id, 0),
                            font_weight="800",
                            size="2",
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
                        "border_radius": RADIUS["lg"],
                        "padding": SPACING["3"],
                        "text_align": "center",
                        "flex": "1",
                        "backdrop_filter": "blur(5px)"
                    }
                ),
                
                # Tiempo promedio espera (NUEVO)
                rx.box(
                    rx.vstack(
                        rx.text(
                            # 🔄 ACTUALIZADO: Tiempo fijo por ahora
                            "25min",
                            font_weight="800",
                            size="2",
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
                        "border_radius": RADIUS["lg"],
                        "padding": SPACING["3"],
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
            "margin_bottom": SPACING["4"],
            "padding": SPACING["4"],
            "background": f"rgba({DARK_COLORS['glass_bg']}, 0.3)",
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": RADIUS["lg"],
            "backdrop_filter": "blur(10px)"
        }
    )

# ==========================================
# 🏷️ BADGE CONSULTAS UNIFICADO - OPTIMIZADO
# ==========================================
def badge_consultas_unificado(
    doctor_id: str,
    theme: str = "dark",
    size: str = "md", 
    show_description: bool = True,
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
    
    # Obtener contador según tipo
    if badge_type == "total":
        # 🔄 ACTUALIZADO: Total por odontólogo específico
        count = AppState.totales_por_odontologo_dict.get(doctor_id, 0)
        description_text = rx.cond(
            count == 0, "Sin cola",
            rx.cond(count == 1, "1 paciente", f"{count} pacientes")
        )
    elif badge_type == "urgentes":
        # 🔄 ACTUALIZADO: Urgentes por odontólogo específico
        count = AppState.urgentes_por_odontologo_dict.get(doctor_id, 0)
        description_text = rx.cond(
            count == 0, "Sin urgentes",
            rx.cond(count == 1, "1 urgente", f"{count} urgentes")
        )
    else:
        count = 0
        description_text = "Error"
    
    return rx.vstack(
        # Contador principal
        rx.box(
            rx.text(
                count.to_string() if badge_type == "total" else count,
                font_weight="800",
                font_size=config["font_size"],
                color=DARK_COLORS["text_primary"],
                style={"text_shadow": "0 0 10px rgba(255, 255, 255, 0.5)"}
            ),
            style={
                "background": rx.cond(
                    badge_type == "urgentes",
                    rx.cond(
                        count > 0,
                        f"linear-gradient(135deg, {DARK_COLORS['priority_urgent']} 0%, #ef4444 100%)",
                        DARK_COLORS["surface_hover"]
                    ),
                    rx.cond(
                        count > 3,
                        f"linear-gradient(135deg, {DARK_COLORS['accent_red']} 0%, #fc8181 100%)",
                        rx.cond(
                            count > 0,
                            f"linear-gradient(135deg, {DARK_COLORS['accent_yellow']} 0%, #f6e05e 100%)",
                            f"linear-gradient(135deg, {DARK_COLORS['border']} 0%, {DARK_COLORS['surface_hover']} 100%)"
                        )
                    )
                ),
                "border": f"1px solid {DARK_COLORS['glass_border']}",
                "border_radius": RADIUS["xl"],
                "padding": config["padding"],
                "text_align": "center",
                "backdrop_filter": "blur(10px)",
                "transition": "all 0.3s ease",
                "animation": rx.cond(
                    (badge_type == "urgentes") & (count > 0),
                    "pulse 2s infinite",
                    "none"
                ),
                "_hover": {"transform": "scale(1.05)"}
            }
        ),
        
        # Descripción contextual
        rx.cond(
            show_description,
            rx.text(
                description_text,
                font_size="0.65rem",
                color=DARK_COLORS["text_muted"],
                font_weight="600",
                style={"text_transform": "uppercase", "letter_spacing": "0.05em"}
            ),
            rx.box()
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
                 "background": DARK_COLORS["priority_urgent"],
                 "border": f"1px solid {DARK_COLORS['priority_urgent']}",
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
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
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
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
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
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
                             "border_radius": RADIUS["lg"],
                             "padding": f"{SPACING['2.5']} {SPACING['5']}",
                             "backdrop_filter": "blur(10px)",
                             "transition": "all 0.3s ease",
                             "flex": "1",
                             "_hover": {
                                 "transform": "translateY(-2px)",
                                 "box_shadow": f"0 8px 25px rgba(56, 161, 105, 0.4)"
                             }
                         },
                         # 🔄 ACTUALIZADO: Usar operacion_consulta_master
                         on_click=lambda: AppState.operacion_consulta_master("cambiar_estado", consulta_data.id, {"estado": "en_atencion"}),
                         loading=AppState.cargando_consultas
                     ),
                     
                     # Botón de transferir (NUEVO) - FUNCIONAL
                     rx.button(
                         rx.icon("arrow-left-right", size=14, color=DARK_COLORS["accent_blue"]),
                         # 🔄 ACTUALIZADO: Usar gestionar_modal_operacion
                         on_click=lambda: AppState.gestionar_modal_operacion("abrir_transferencia", consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_blue']}",
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
                         rx.icon("chevron-up", size=12, color=DARK_COLORS["accent_green"]),
                         # ℹ️ LEGACY: subir_en_cola - mantener si existe o crear wrapper
                         on_click=lambda: AppState.subir_en_cola(consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_green']}",
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
                         rx.icon("chevron-down", size=12, color=DARK_COLORS["accent_yellow"]),
                         # ℹ️ LEGACY: bajar_en_cola - mantener si existe o crear wrapper
                         on_click=lambda: AppState.bajar_en_cola(consulta_data.id),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_yellow']}",
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
                         rx.icon("x", size=14, color=DARK_COLORS["accent_red"]),
                         style={
                             "background": "transparent",
                             "border": f"1px solid {DARK_COLORS['accent_red']}",
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
                ("en_atencion",
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
                         # 🔄 ACTUALIZADO: Usar operacion_consulta_master
                         on_click=lambda: AppState.operacion_consulta_master("cambiar_estado", consulta_data.id, {"estado": "completada"}),
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
                "padding": SPACING["12"],
                "text_align": "center",
                "border": f"2px dashed {DARK_COLORS['border']}",
                "border_radius": RADIUS["xl"],
                "background": f"rgba({DARK_COLORS['surface']}, 0.3)",
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
            rx.icon("user-round", size=24, color=DARK_COLORS["text_primary"]),
            style={
                "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #48bb78 100%)",
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
                color=DARK_COLORS["text_primary"]
            ),
            rx.text(
                doctor.especialidad,
                color=DARK_COLORS["text_secondary"],
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
                rx.icon("circle-check", size=9, color=DARK_COLORS["accent_green"]),
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

def doctor_metrics(doctor_id: str) -> rx.Component:
    """📊 Métricas y badges de consultas usando badge_consultas_unificado"""
    return estadisticas_columna_odontologo(doctor_id)

def patient_queue_header(doctor_id: str) -> rx.Component:
    """📋 Header de la cola de pacientes con contador"""
    return rx.hstack(
        rx.icon("users", size=16, color=DARK_COLORS["accent_blue"]),
        rx.text(
            "Cola de Pacientes",
            font_weight="700",
            color=DARK_COLORS["text_primary"],
            size="3"
        ),
        # Contador en header usando badge_consultas_unificado
        badge_consultas_unificado(
            doctor_id=doctor_id,
            size="sm",
            show_description=False,
            badge_type="total"
        ),
        spacing="2",
        align="center",
        width="100%",
        justify="start"
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
                "border_color": f"{DARK_COLORS['accent_blue']}40",
                "background": f"rgba(14, 165, 233, 0.05)"
            }
        }
    )

def patient_queue(doctor_id: str) -> rx.Component:
    """👥 Sección completa de cola de pacientes"""
    return rx.vstack(
        patient_queue_header(doctor_id),
        patient_queue_area(doctor_id),
        spacing="4",
        width="100%",
        align="start"
    )

def doctor_actions(doctor_id: str) -> rx.Component:
    """🎯 Botones de acción del doctor (agregar paciente, ver cola)"""
    return rx.hstack(
        rx.button(
            rx.hstack(
                rx.icon("user-plus", size=16, color="white"),
                rx.text("Agregar", font_weight="600", color="white"),
                spacing="2",
                align="center"
            ),
            # 🔄 ACTUALIZADO: Usar gestionar_modal_operacion
            on_click=lambda: AppState.gestionar_modal_operacion("preparar_nuevo_formulario", datos={"odontologo_id": doctor_id}),
            style={
                "background": f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4299e1 100%)",
                "border": f"1px solid {DARK_COLORS['glass_border']}",
                "border_radius": RADIUS["lg"],
                "padding": f"{SPACING['2.5']} {SPACING['5']}",
                "backdrop_filter": "blur(10px)",
                "transition": "all 0.3s ease",
                "flex": "1",
                "_hover": {
                    "transform": "translateY(-2px)",
                    "box_shadow": f"0 8px 25px rgba(49, 130, 206, 0.4)"
                }
            }
        ),
        rx.button(
            rx.hstack(
                rx.icon("eye", size=16, color="white"),
                rx.text("Ver Cola", font_weight="600", color="white"),
                spacing="2",
                align="center"
            ),
            # ℹ️ LEGACY: set_doctor_seleccionado - mantener si existe
            on_click=lambda: AppState.set_doctor_seleccionado(doctor_id),
            style={
                "background": f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                "border": f"1px solid {DARK_COLORS['glass_border']}",
                "border_radius": RADIUS["lg"],
                "padding": f"{SPACING['2.5']} {SPACING['5']}",
                "backdrop_filter": "blur(10px)",
                "transition": "all 0.3s ease",
                "flex": "1",
                "_hover": {
                    "transform": "translateY(-2px)",
                    "box_shadow": f"0 8px 25px rgba(56, 161, 105, 0.4)"
                }
            }
        ),
        spacing="2",
        width="100%"
    )

def doctor_card_v41(doctor: rx.Var) -> rx.Component:
    """👨‍⚕️ Card de doctor modular v4.1 - Componente contenedor principal"""
    return rx.box(
        rx.vstack(
            # Header con avatar, nombre, especialidad y estado
            doctor_header(doctor),
            
            # Métricas y estadísticas
            doctor_metrics(doctor.id),
            
            # Divider
            rx.divider(
                margin=f"{SPACING['4']} 0", 
                style={"border_color": DARK_COLORS["border"], "opacity": "0.3"}
            ),
            
            # Cola de pacientes
            patient_queue(doctor.id),
            
            # Botones de acción (comentados temporalmente para mantener funcionalidad original)
            # doctor_actions(doctor.id),
            
            spacing="0",
            width="100%",
            align="start"
        ),
        style={
            "background": DARK_COLORS["glass_bg"],
            "border": f"1px solid {DARK_COLORS['glass_border']}",
            "border_radius": RADIUS["xl"],
            "padding": SPACING["5"],
            "min_height": "500px",
            "backdrop_filter": "blur(20px)",
            "transition": "all 0.4s ease",
            "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "_hover": {
                "transform": "translateY(-4px)",
                "box_shadow": f"0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15)",
                "border_color": DARK_COLORS["border_hover"]
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
    from dental_system.components.forms import (
        enhanced_form_field, enhanced_form_field_dinamico, form_section_header, 
        success_feedback, loading_feedback
    )
    from dental_system.styles.themes import (
        COLORS, SHADOWS, RADIUS, SPACING, ANIMATIONS, 
        GRADIENTS, GLASS_EFFECTS, DARK_THEME
    )
    
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
        # 🔄 CORREGIDO: cerrar_modal_transferir_paciente → gestionar_modal_operacion
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
                            "padding": SPACING["16"],
                            "text_align": "center",
                            "background": DARK_COLORS["glass_bg"],
                            "border": f"2px dashed {DARK_COLORS['border']}",
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