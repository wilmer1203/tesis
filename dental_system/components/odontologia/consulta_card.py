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
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS PARA TARJETAS DE CONSULTA
# ==========================================

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

CONSULTA_ASIGNADA_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["primary"]["200"],
    "background": "white",
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["primary"]["400"],
        "background": COLORS["primary"]["200"]
    }
}

CONSULTA_DISPONIBLE_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["success"]["200"],
    "background": "white",
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["success"]["400"],
        "background": COLORS["success"]["25"]
    }
}

CONSULTA_EN_PROGRESO_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["warning"]["200"],
    "background": "white",
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["warning"]["500"],
        "background": COLORS["warning"]["25"]
    }
}

CONSULTA_URGENTE_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["error"]["400"],
    "background": "white",
    "border_width": "2px",
    "box_shadow": "0 4px 6px rgba(239, 68, 68, 0.1), 0 1px 3px rgba(239, 68, 68, 0.08)",
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["error"]["500"],
        "background": COLORS["error"]["25"],
        "box_shadow": "0 8px 25px rgba(239, 68, 68, 0.2), 0 3px 10px rgba(239, 68, 68, 0.1)"
    }
}

# Estilos para badges
BADGE_ASIGNADO_STYLE = {
    "background": COLORS["primary"]["100"],
    "color": COLORS["primary"]["700"],
    "padding": f"{SPACING['1']} {SPACING['2']}",
    "border_radius": RADIUS["full"],
    "font_size": "12px",
    "font_weight": "medium"
}

BADGE_DISPONIBLE_STYLE = {
    "background": COLORS["success"]["100"],
    "color": COLORS["success"]["700"],
    "padding": f"{SPACING['1']} {SPACING['2']}",
    "border_radius": RADIUS["full"],
    "font_size": "12px",
    "font_weight": "medium"
}

BADGE_EN_PROGRESO_STYLE = {
    "background": COLORS["warning"]["100"],
    "color": COLORS["warning"]["700"],
    "padding": f"{SPACING['1']} {SPACING['2']}",
    "border_radius": RADIUS["full"],
    "font_size": "12px",
    "font_weight": "medium"
}

BADGE_URGENTE_STYLE = {
    "background": COLORS["error"]["100"],
    "color": COLORS["error"]["700"],
    "padding": f"{SPACING['1']} {SPACING['2']}",
    "border_radius": RADIUS["full"],
    "font_size": "12px",
    "font_weight": "bold"
}

# ==========================================
# 🧩 COMPONENTES AUXILIARES
# ==========================================

def badge_estado_consulta(estado: rx.Var, prioridad: rx.Var = None) -> rx.Component:
    """🏷️ Badge que muestra el estado de la consulta con colores - Estados BD v4.1"""
    
    # Estados reales de BD con colores actualizados
    return rx.cond(
        prioridad == "urgente",
        rx.box("🚨 URGENTE", style=BADGE_URGENTE_STYLE),
        rx.cond(
            estado == "en_espera",
            rx.box("⏳ En Espera", style=BADGE_ASIGNADO_STYLE),
            rx.cond(
                estado == "en_atencion",
                rx.box("👨‍⚕️ En Atención", style=BADGE_EN_PROGRESO_STYLE),
                rx.cond(
                    estado == "entre_odontologos",
                    rx.box("🔄 Entre Odontólogos", style=BADGE_DISPONIBLE_STYLE),
                    rx.cond(
                        estado == "completada",
                        rx.box("✅ Completada", style=BADGE_DISPONIBLE_STYLE),
                        rx.cond(
                            estado == "cancelada",
                            rx.box("❌ Cancelada", style={**BADGE_URGENTE_STYLE, "background": COLORS["gray"]["100"], "color": COLORS["gray"]["700"]}),
                            # Compatibility con estados antiguos
                            rx.cond(
                                estado == "programada", 
                                rx.box("⏳ En Espera", style=BADGE_ASIGNADO_STYLE),
                                rx.cond(
                                    estado == "en_progreso",
                                    rx.box("👨‍⚕️ En Atención", style=BADGE_EN_PROGRESO_STYLE),
                                    rx.box("❓ Desconocido", style=BADGE_ASIGNADO_STYLE)
                                )
                            )
                        )
                    )
                )
            )
        )
    )

def info_medica_urgente(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """🏥 Alertas médicas urgentes visibles en las cards"""
    return rx.vstack(
        # Alerta de prioridad urgente
        rx.cond(
            consulta.es_urgente,
            rx.box(
                rx.hstack(
                    rx.icon("triangle_alert", size=14, color=COLORS["error"]["500"]),
                    rx.text(
                        "ATENCIÓN URGENTE",
                        font_size="11px",
                        color=COLORS["error"]["700"],
                        font_weight="bold"
                    ),
                    spacing="1"
                ),
                style={
                    "background": COLORS["error"]["50"],
                    "border": f"1px solid {COLORS['error']['200']}",
                    "border_radius": RADIUS["md"],
                    "padding": "4px 8px",
                    "margin_bottom": "2px"
                }
            )
        ),
        
        # Nota: La información médica detallada estará disponible en el historial del paciente
        # que se puede acceder con el botón "Ver Historial"
        
        spacing="1",
        width="100%"
    )

def info_consulta_adicional(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """📋 Información adicional de la consulta con detalles médicos mejorados"""
    return rx.vstack(
        # Fila 1: Número de consulta y hora de llegada
        rx.hstack(
            rx.text(
                f"#{consulta.numero_consulta}",
                font_size="12px",
                color=COLORS["gray"]["500"],
                font_weight="medium"
            ),
            rx.spacer(),
            rx.text(
                f"🕐 {consulta.hora_display}",  # Hora de llegada
                font_size="12px",
                color=COLORS["blue"]["500"],
                font_weight="medium"
            ),
            width="100%"
        ),
        
        # Fila 2: Posición en cola y tiempo estimado
        rx.hstack(
            rx.text(
                f"🔢 {consulta.posicion_cola_display}",  # Posición en cola
                font_size="12px",
                color=COLORS["primary"]["500"],
                font_weight="medium"
            ),
            rx.spacer(),
            rx.text(
                f"⏱️ {consulta.tiempo_espera_estimado}",  # Tiempo estimado
                font_size="12px",
                color=COLORS["warning"]["500"],
                font_weight="medium"
            ),
            width="100%"
        ),
        
        # Fila 3: Tipo de consulta y duración estimada
        rx.hstack(
            rx.text(
                f"🦷 {consulta.tipo_consulta.title()}",
                font_size="12px",
                color=COLORS["primary"]["400"],
                font_weight="medium"
            ),
            rx.spacer(),
            rx.text(
                f"📅 {consulta.duracion_estimada_display}",
                font_size="12px",
                color=COLORS["gray"]["500"]
            ),
            width="100%"
        ),
        
        # Motivo de consulta si existe (con truncado)
        rx.cond(
            consulta.motivo_consulta != "",
            rx.text(
                f"📝 {consulta.motivo_consulta}",
                font_size="12px",
                color=COLORS["gray"]["600"],
                white_space="nowrap",
                overflow="hidden",
                text_overflow="ellipsis",
                max_width="100%"
            )
        ),
        
        spacing="2",
        width="100%",
        align_items="start"
    )

# ==========================================
# 📋 COMPONENTES PRINCIPALES DE TARJETAS
# ==========================================

def consulta_asignada_card(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """👤 Tarjeta de consulta asignada directamente al odontólogo - SOLO CONSULTA"""
    
    # Determinar el estilo según la prioridad
    card_style = rx.cond(
        consulta.prioridad == "urgente",
        CONSULTA_URGENTE_STYLE,
        rx.cond(
            consulta.esta_en_progreso,
            CONSULTA_EN_PROGRESO_STYLE,
            CONSULTA_ASIGNADA_STYLE
        )
    )
    
    return rx.box(
        rx.vstack(
            # Header con degradado y posición
            rx.box(
                rx.hstack(
                    # Posición en cola (lado izquierdo)
                    rx.box(
                        rx.text(
                            consulta.posicion_cola_display,
                            font_size="20px",
                            font_weight="800",
                            color="white",
                            style={"text_shadow": "0 0 10px rgba(255, 255, 255, 0.5)"}
                        ),
                        style={
                            "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['400']} 100%)",
                            "border_radius": RADIUS["full"],
                            "width": "48px",
                            "height": "48px",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center",
                            "box_shadow": "0 4px 12px rgba(0, 188, 212, 0.3)"
                        }
                    ),
                    
                    # Información del paciente (centro)
                    rx.vstack(
                        rx.text(
                            consulta.paciente_nombre,
                            font_size="18px",
                            font_weight="700",
                            color=COLORS["gray"]["900"]
                        ),
                        rx.text(
                            f"Consulta #{consulta.numero_consulta} | {consulta.paciente_documento}",
                            font_size="14px",
                            color=COLORS["gray"]["600"],
                            font_weight="500"
                        ),
                        spacing="1",
                        align_items="start",
                        flex="1"
                    ),
                    
                    # Badge de estado (lado derecho)
                    badge_estado_consulta(
                        consulta.estado, 
                        consulta.prioridad
                    ),
                    
                    spacing="4",
                    align_items="center",
                    width="100%"
                ),
                style={
                    "background": f"linear-gradient(135deg, {COLORS['gray']['25']} 0%, {COLORS['gray']['50']} 100%)",
                    "border_radius": f"{RADIUS['xl']} {RADIUS['xl']} 0 0",
                    "padding": SPACING["4"],
                    "margin": f"-{SPACING['6']} -{SPACING['6']} {SPACING['4']} -{SPACING['6']}",
                    "border_bottom": f"1px solid {COLORS['gray']['200']}"
                }
            ),
            
            # Información del paciente (usar la propiedad display existente)
            rx.text(
                f"👤 {consulta.paciente_info_display}",
                font_size="14px",
                color=COLORS["gray"]["700"],
                font_weight="500"
            ),
            
            # Alertas médicas urgentes
            info_medica_urgente(consulta),
            
            # Información adicional de consulta mejorada
            info_consulta_adicional(consulta),
            
            # Botones de acción
            rx.hstack(
                # Ver historial
                secondary_button(
                    text="Ver Historial",
                    icon="user",
                    on_click=lambda c=consulta: AppState.ver_historial_paciente(c.paciente_id)
                ),
                
                rx.spacer(),
                
                # Acción principal según estado - SIMPLIFICADO PARA DEBUG
                rx.vstack(
                    # MOSTRAR ESTADO Y ID PARA DEBUG
                    rx.text(
                        f"Estado: {consulta.estado} | ID: {consulta.id}",
                        font_size="10px",
                        color=COLORS["gray"]["500"]
                    ),
                    
                    # BOTONES SEGÚN ESTADO
                    rx.cond(
                        consulta.estado == "en_espera",
                        primary_button(
                            text="🟢 Iniciar Atención",
                            icon="play",
                            on_click=lambda: AppState.navegar_a_odontologia_consulta(consulta.id)
                        ),
                        rx.cond(
                            consulta.estado == "programada", 
                            primary_button(
                                text="🟡 Iniciar Consulta",
                                icon="play", 
                                on_click=lambda c=consulta: AppState.navegar_a_odontologia_consulta(c.id)
                            ),
                            rx.cond(
                                consulta.esta_en_progreso,
                                primary_button(
                                    text="🔄 Continuar",
                                    icon="arrow-right",
                                    on_click=lambda c=consulta: AppState.navegar_a_odontologia_consulta(c.id)
                                ),
                                secondary_button(
                                    text="👁️ Ver Detalles", 
                                    icon="eye",
                                    on_click=lambda c=consulta: AppState.ver_historial_completo(c.id)
                                )
                            )
                        )
                    ),
                    
                    spacing="1",
                    align_items="center"
                ),
                
                spacing="3",
                align_items="center",
                width="100%"
            ),
            
            spacing="0",
            width="100%"
        ),
        style=card_style
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
                    f"🎂 {paciente.edad_display}",
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
                secondary_button(
                    text="Ver Historial",
                    icon="user",
                    on_click=lambda p=paciente: AppState.ver_historial_paciente(p.id)
                ),
                
                rx.spacer(),
                
                primary_button(
                    text="Tomar Paciente",
                    icon="plus",
                    on_click=lambda p=paciente, cid=consulta_id: AppState.navegar_a_odontologia_consulta(cid)
                ),
                
                spacing="3",
                align_items="center",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        style=CONSULTA_DISPONIBLE_STYLE
    )

# ==========================================
# 📋 LISTAS DE CONSULTAS
# ==========================================

def lista_consultas_asignadas() -> rx.Component:
    """📋 Lista completa de consultas asignadas"""
    return rx.cond(
        AppState.consultas_asignadas.length() > 0,
        rx.vstack(
            rx.foreach(
                AppState.consultas_asignadas,
                lambda consulta: consulta_asignada_card(consulta)
            ),
            spacing="3",
            width="100%"
        ),
        # Estado vacío
        rx.center(
            rx.vstack(
                rx.text("👥", font_size="48px", color=COLORS["gray"]["400"]),
                rx.text(
                    "No hay consultas asignadas",
                    font_size="16px",
                    color=COLORS["gray"]["500"],
                    font_weight="medium"
                ),
                rx.text(
                    "Las consultas asignadas aparecerán aquí cuando lleguen pacientes",
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
    text_color = COLORS.get(color, COLORS["gray"])["700"]
    
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