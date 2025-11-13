"""
🦷 COMPONENTE: TARJETAS DE CONSULTA ODONTOLÓGICA
==============================================

Componentes especializados para mostrar información de consultas
y pacientes en el dashboard del odontólogo.

Tipos de tarjetas:
- Consulta asignada (pacientes propios)
- Consulta disponible (de otros odontólogos)
- Consulta en progreso
- Consulta completada
"""

import reflex as rx
from typing import Optional
from dental_system.state.app_state import AppState
from dental_system.models import PacienteModel, ConsultaModel
from dental_system.components.common import primary_button, secondary_button
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING, GRADIENTS, ANIMATIONS

# ==========================================
# 🎨 ESTILOS PARA TARJETAS DE CONSULTA - TEMA OSCURO
# ==========================================

# Importar colores de tema oscuro de consultas
DARK_COLORS = {
    "background": "#0f1419",
    "surface": "#1a1f2e",
    "surface_hover": "#252b3a",
    "border": "#2d3748",
    "border_hover": "#4a5568",
    "text_primary": "#f7fafc",
    "text_secondary": "#a0aec0",
    "text_muted": "#718096",
    "accent_blue": "#3182ce",
    "accent_green": "#38a169",
    "accent_yellow": "#d69e2e",
    "accent_red": "#e53e3e",
    "glass_bg": "rgba(26, 31, 46, 0.8)",
    "glass_border": "rgba(255, 255, 255, 0.1)",
    "priority_urgent": "#dc2626",
    "priority_high": "#ea580c",
    "priority_normal": "#6b7280",
    "priority_urgent_bg": "rgba(220, 38, 38, 0.1)",
    "priority_high_bg": "rgba(234, 88, 12, 0.1)",
    "priority_normal_bg": "rgba(107, 114, 128, 0.1)",
}

# Estilo base moderno con tema oscuro
CONSULTA_CARD_DARK_BASE = {
    "background": DARK_COLORS["glass_bg"],
    "border": f"1px solid {DARK_COLORS['glass_border']}",
    "border_radius": RADIUS["xl"],
    "backdrop_filter": "blur(15px)",
    "box_shadow": "0 4px 20px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
    "transition": "all 0.3s ease",
    "position": "relative",
    "_hover": {
        "transform": "translateY(-2px)",
        "background": "rgba(255, 255, 255, 0.12)",
        "border_color": "rgba(255, 255, 255, 0.3)",
        "box_shadow": "0 8px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
    }
}

# Estilo compacto para vista optimizada
CONSULTA_COMPACTA_STYLE = {
    **CONSULTA_CARD_DARK_BASE,
    "padding": SPACING["3"],
    "margin_bottom": SPACING["2"],
    "min_height": "80px",
    "max_height": "120px",
}

CONSULTA_CARD_BASE_STYLE = {
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
    "border": "1px solid",
    "padding": SPACING["6"],
    "margin_bottom": SPACING["4"],
    "width": "100%",
    "transition": "all 0.3s ease",
    "_hover": {
        "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.15), 0 3px 10px rgba(0, 0, 0, 0.1)",
        "transform": "translateY(-2px)"
    }
}

BADGE_DISPONIBLE_STYLE = {
    "background": COLORS["success"]["500"],
    "color": COLORS["success"]["700"],
    "padding": f"{SPACING['1']} {SPACING['2']}",
    "border_radius": RADIUS["full"],
    "font_size": "12px",
    "font_weight": "medium"
}



# ==========================================
# 🧩 COMPONENTES AUXILIARES MODERNOS
# ==========================================

def badge_prioridad_moderno(prioridad: rx.Var[str]) -> rx.Component:
    """🏷️ Badge de prioridad moderno con animaciones"""
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
                 rx.text("ALTA", font_weight="700", font_size="0.65rem", color="white"),
                 spacing="1", align="center"
             ),
             style={
                 "background": DARK_COLORS["priority_high"],
                 "border_radius": RADIUS["sm"],
                 "padding": f"{SPACING['1']} {SPACING['2']}",
                 "box_shadow": f"0 2px 8px {DARK_COLORS['priority_high_bg']}"
             }
         )),
        rx.box(
            rx.text("Normal", font_size="0.65rem", color=DARK_COLORS["text_muted"]),
            style={
                "background": DARK_COLORS["priority_normal_bg"],
                "border_radius": RADIUS["sm"],
                "padding": f"{SPACING['1']} {SPACING['2']}"
            }
        )
    )

def posicion_badge_moderno(posicion) -> rx.Component:
    """🔢 Badge de posición como en página de consultas"""
    return rx.box(
        rx.text(
            f"#{posicion}",
            font_weight="800",
            font_size="0.9rem",
            color="white",
            style={"text_shadow": "0 0 10px rgba(255, 255, 255, 0.5)"}
        ),
        style={
            "background": rx.cond(
                posicion == 1,
                f"linear-gradient(135deg, {DARK_COLORS['accent_green']} 0%, #48bb78 100%)",
                f"linear-gradient(135deg, {DARK_COLORS['accent_blue']} 0%, #4299e1 100%)"
            ),
            "border_radius": RADIUS["full"],
            "width": "36px",
            "height": "36px",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",
            "box_shadow": f"0 4px 12px rgba(0, 188, 212, 0.3)",
            "border": "2px solid rgba(255, 255, 255, 0.2)"
        }
    )



# ==========================================
# 📋 COMPONENTES PRINCIPALES DE TARJETAS
# ==========================================

def consulta_compacta_odontologo_card(consulta: rx.Var[ConsultaModel], posicion: int) -> rx.Component:
    """🎯 TARJETA COMPACTA INSPIRADA EN PÁGINA DE CONSULTAS - TEMA OSCURO"""
    return rx.box(
        rx.hstack(
            # Posición prominente (lado izquierdo)
            posicion_badge_moderno(posicion),

            # Información principal del paciente (centro expandido)
            rx.vstack(
                # Nombre del paciente
                rx.text(
                    consulta.paciente_nombre,
                    font_size="1rem",
                    font_weight="700",
                    color=DARK_COLORS["text_primary"],
                    style={"line_height": "1.2"}
                ),

                # Info secundaria compacta
                rx.hstack(
                    rx.text(
                        f"🕐 {consulta.fecha_llegada}",
                        font_size="0.75rem",
                        color=DARK_COLORS["accent_blue"],
                        font_weight="600"
                    ),
                    rx.text("•", color=DARK_COLORS["text_muted"], font_size="0.75rem"),
                    rx.text(
                        consulta.paciente_documento,
                        size="1",
                        weight="medium",
                        color=DARK_COLORS["text_secondary"]
                    ),
                    spacing="2",
                    align="center"
                ),

                # Motivo de consulta (truncado) - Si existe
                rx.cond(
                    (consulta.motivo_consulta != "") & (consulta.motivo_consulta != None),
                    rx.text(
                        f"📝 {consulta.motivo_consulta}",
                        font_size="0.7rem",
                        color=DARK_COLORS["text_muted"],
                        white_space="nowrap",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        max_width="200px"
                    )
                ),

                spacing="1",
                align_items="start",
                flex="1"
            ),

            # Badge de prioridad y estado (lado derecho)
            rx.vstack(
                badge_prioridad_moderno(consulta.tipo_consulta),

                # Botón de acción compacto
                rx.button(
                    rx.cond(
                        consulta.estado == "en_espera",
                        rx.hstack(rx.icon("play", size=12), rx.text("Atender", font_size="0.7rem"), spacing="1"),
                        rx.cond(
                            consulta.estado == "en_atencion",
                            rx.hstack(rx.icon("arrow-right", size=12), rx.text("Continuar", font_size="0.7rem"), spacing="1"),
                            rx.hstack(rx.icon("eye", size=12), rx.text("Ver", font_size="0.7rem"), spacing="1")
                        )
                    ),
                    style={
                        "background": GRADIENTS["neon_primary"],
                        "color": "white",
                        "border": "none",
                        "border_radius": RADIUS["lg"],
                        "padding": f"{SPACING['1']} {SPACING['3']}",
                        "font_weight": "700",
                        "font_size": "0.7rem",
                        "cursor": "pointer",
                        "transition": ANIMATIONS["presets"]["crystal_hover"],
                        "position": "relative",
                        "_hover": {
                            "transform": "translateY(-3px) scale(1.05)",
                            "box_shadow": SHADOWS["crystal_lg"],
                            "_before": {
                                "content": "''",
                                "position": "absolute",
                                "inset": "-2px",
                                "border_radius": RADIUS["lg"],
                                "z_index": "-1",
                                "opacity": "0.8"
                            }
                        },
                        "_active": {"transform": "translateY(-1px) scale(1.02)"}
                    },
                    on_click=AppState.seleccionar_paciente_consulta(consulta.paciente_id,consulta.id)
                ),

                spacing="2",
                align="center"
            ),

            spacing="4",
            align="center",
            width="100%"
        ),
        style=CONSULTA_COMPACTA_STYLE
    )


def consulta_disponible_card(paciente: rx.Var[PacienteModel], consulta_id: str) -> rx.Component:
    """🔄 Tarjeta de consulta disponible de otro odontólogo"""
    return rx.box(
        rx.vstack(
            # Header con nombre y badge
            rx.hstack(
                rx.vstack(
                    rx.text(
                        paciente.nombre_completo,
                        font_size="18px",
                        font_weight="700",
                        color=COLORS["gray"]["900"]
                    ),
                    rx.text(
                        f"HC: {paciente.numero_historia} | {paciente.numero_documento}",
                        font_size="14px",
                        color=COLORS["gray"]["600"],
                        font_weight="500"
                    ),
                    spacing="1",
                    align_items="start"
                ),
                
                rx.spacer(),
                
                rx.box("🔄 Disponible", style=BADGE_DISPONIBLE_STYLE),
                
                spacing="3",
                align_items="start",
                width="100%"
            ),
            
            # Información del paciente disponible
            rx.text(
                f"👤 {paciente.contacto_display}",
                font_size="13px",
                color=COLORS["gray"]["600"]
            ),
            
            # Información médica disponible
            rx.vstack(
                # Edad del paciente
                rx.text(
                    f"Edad #",
                    font_size="12px",
                    color=COLORS["blue"]["500"],
                    font_weight="medium"
                ),
                
                # Alergias si tiene
                rx.cond(
                    paciente.alergias_display != "Sin alergias conocidas",
                    rx.text(
                        f"⚠️ Alergias: {paciente.alergias_display}",
                        font_size="12px",
                        color=COLORS["warning"]["500"],
                        font_weight="medium",
                        white_space="nowrap",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        max_width="100%"
                    )
                ),
                
                spacing="1",
                width="100%",
                align_items="start"
            ),
            
            # Info adicional para disponibles
            rx.text(
                "Paciente derivado - puede requerir intervención adicional",
                font_size="12px",
                color=COLORS["success"]["500"],
                font_style="italic"
            ),
            
            # Botones de acción
            rx.hstack(
                # secondary_button(
                #     text="Ver Historial",
                #     icon="user",
                #     on_click=AppState.ver_historial_paciente(paciente.id)
                # ),
                
                rx.spacer(),
                
                primary_button(
                    text="Tomar Paciente",
                    icon="plus",
                    on_click=AppState.seleccionar_paciente_consulta(paciente.id,consulta_id)
                ),
                
                spacing="3",
                align_items="center",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
       
    )

# ==========================================
# 📋 LISTAS DE CONSULTAS
# ==========================================

def estadisticas_cola_odontologo() -> rx.Component:
    """📊 Mini estadísticas de cola como en página de consultas"""
    return rx.hstack(
        # Total en cola
        rx.box(
            rx.vstack(
                rx.text(
                    AppState.estadisticas_odontologo_tiempo_real["pacientes_asignados"],
                    font_weight="800",
                    font_size="1.1rem",
                    color=DARK_COLORS["text_primary"],
                    style={"line_height": "1"}
                ),
                rx.text(
                    "En Cola",
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

        # Urgentes (con animación si hay)
        rx.box(
            rx.vstack(
                rx.text(
                    AppState.alerta_pacientes_urgentes["cantidad"],
                    font_weight="800",
                    font_size="1.1rem",
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
                "backdrop_filter": "blur(5px)",
                "animation": rx.cond(
                    AppState.alerta_pacientes_urgentes["tiene_urgentes"],
                    "pulse 2s infinite",
                    "none"
                )
            }
        ),


        spacing="3",
        width="100%"
    )


def lista_consultas_compactas() -> rx.Component:
    """📋 NUEVA: Lista compacta inspirada en página de consultas"""
    return rx.cond(
        AppState.consultas_asignadas.length() > 0,
        rx.vstack(
            rx.foreach(
                AppState.consultas_asignadas,
                lambda consulta, index: consulta_compacta_odontologo_card(consulta, index + 1)
            ),
            spacing="2",
            width="100%"
        ),
        # Estado vacío con tema oscuro
        rx.center(
            rx.vstack(
                rx.icon("calendar-x", size=40, color=DARK_COLORS["text_muted"]),
                rx.text(
                    "No hay pacientes en cola",
                    color=DARK_COLORS["text_muted"],
                    font_size="1rem",
                    font_weight="600",
                    style={"text_align": "center"}
                ),
                rx.text(
                    "La cola está vacía en este momento",
                    color=DARK_COLORS["text_muted"],
                    font_size="0.875rem",
                    style={"text_align": "center", "opacity": "0.7"}
                ),
                spacing="3",
                align="center"
            ),
            padding="8",
            width="100%",
            style={
                "background": DARK_COLORS["glass_bg"],
                "border": f"1px solid {DARK_COLORS['glass_border']}",
                "border_radius": RADIUS["xl"],
                "backdrop_filter": "blur(10px)"
            }
        )
    )

def lista_consultas_disponibles() -> rx.Component:
    """🔄 Lista de consultas disponibles de otros odontólogos"""
    return rx.cond(
        AppState.pacientes_disponibles_filtrados.length() > 0,
        rx.vstack(
            rx.foreach(
                AppState.pacientes_disponibles_filtrados,
                lambda paciente: consulta_disponible_card(
                    paciente,
                    # ID de consulta temporal - se debería obtener del modelo
                    paciente.id + "_consulta"
                )
            ),
            spacing="3",
            width="100%"
        ),
        # Estado vacío
        rx.center(
            rx.vstack(
                rx.text("🔄", font_size="48px", color=COLORS["gray"]["400"]),
                rx.text(
                    "No hay pacientes disponibles",
                    font_size="16px",
                    color=COLORS["gray"]["500"],
                    font_weight="medium"
                ),
                rx.text(
                    "Pacientes que requieran intervención adicional aparecerán aquí",
                    font_size="14px",
                    color=COLORS["gray"]["400"],
                    text_align="center"
                ),
                spacing="2",
                align_items="center"
            ),
            padding="8",
            width="100%"
        )
    )

# ==========================================
# 📊 HEADERS DE SECCIÓN
# ==========================================

def seccion_header(titulo: str, cantidad: rx.Var, icono: str, color: str = "gray") -> rx.Component:
    """📋 Header para las secciones de consultas"""
    
    # Mapear colores del sistema a colores válidos para badge
    color_mapping = {
        "success": "green",
        "primary": "blue", 
        "error": "red",
        "warning": "orange",
        "info": "blue"
    }
    
    badge_color = color_mapping.get(color, color)
    text_color = COLORS.get(color, COLORS["gray"]["700"])
    
    return rx.hstack(
        rx.hstack(
            rx.text(icono, font_size="20px"),
            rx.text(
                titulo,
                font_size="18px",
                font_weight="bold",
                color=text_color
            ),
            spacing="2",
            align_items="center"
        ),
        
        rx.spacer(),
        
        rx.badge(
            cantidad,
            color_scheme=badge_color,
            size="2"
        ),
        
        spacing="3",
        align_items="center",
        width="100%",
        margin_bottom="4"
    )