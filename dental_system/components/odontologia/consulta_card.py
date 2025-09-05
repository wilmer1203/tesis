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
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["sm"],
    "border": "1px solid",
    "padding": SPACING["4"],
    "margin_bottom": SPACING["3"],
    "width": "100%",
    "transition": "all 0.3s ease",
    "_hover": {
        "box_shadow": SHADOWS["lg"],
        "transform": "translateY(-1px)"
    }
}

CONSULTA_ASIGNADA_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["primary"]["200"],
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["primary"]["300"]
    }
}

CONSULTA_DISPONIBLE_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["success"]["200"],
    "background": COLORS["success"]["25"],
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["success"]["300"]
    }
}

CONSULTA_EN_PROGRESO_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["warning"]["200"],
    "background": COLORS["warning"]["25"],
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["warning"]["300"]
    }
}

CONSULTA_URGENTE_STYLE = {
    **CONSULTA_CARD_BASE_STYLE,
    "border_color": COLORS["error"]["200"],
    "background": COLORS["error"]["25"],
    "border_width": "2px",
    "_hover": {
        **CONSULTA_CARD_BASE_STYLE["_hover"],
        "border_color": COLORS["error"]["300"]
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
    """🏷️ Badge que muestra el estado de la consulta con colores - REACTIVO"""
    
    # Usar rx.cond en lugar de if
    return rx.cond(
        prioridad == "urgente",
        rx.box("🚨 URGENTE", style=BADGE_URGENTE_STYLE),
        rx.cond(
            estado == "en_espera",
            rx.box("⏳ En Espera", style=BADGE_ASIGNADO_STYLE),
            rx.cond(
                estado == "programada", 
                rx.box("⏳ En Espera", style=BADGE_ASIGNADO_STYLE),
                rx.cond(
                    estado == "en_progreso",
                    rx.box("🔄 En Atención", style=BADGE_EN_PROGRESO_STYLE),
                    rx.cond(
                        estado == "en_atencion",
                        rx.box("🔄 En Atención", style=BADGE_EN_PROGRESO_STYLE),
                        rx.cond(
                            estado == "completada",
                            rx.box("✅ Completada", style=BADGE_DISPONIBLE_STYLE),
                            rx.cond(
                                estado == "entre_odontologos",
                                rx.box("🔄 Disponible", style=BADGE_DISPONIBLE_STYLE),
                                rx.box("❓ Desconocido", style=BADGE_ASIGNADO_STYLE)
                            )
                        )
                    )
                )
            )
        )
    )

# FUNCIÓN DESHABILITADA: Ya no se usa porque ConsultaModel no tiene info médica detallada
# def info_medica_paciente(paciente: rx.Var[PacienteModel]) -> rx.Component:
#     """🏥 Información médica importante del paciente (alergias, condiciones)"""
#     # Esta función se puede restaurar cuando se implemente info médica en ConsultaModel
#     return rx.box()

def info_consulta_adicional(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """📋 Información adicional de la consulta"""
    return rx.vstack(
        # Número de consulta y fecha
        rx.hstack(
            rx.text(
                f"#{consulta.numero_consulta}",
                font_size="12px",
                color=COLORS["gray"]["500"],
                font_weight="medium"
            ),
            rx.spacer(),
            rx.text(
                consulta.fecha_display,  # ConsultaModel siempre tiene fecha_display
                font_size="12px",
                color=COLORS["gray"]["500"]
            ),
            width="100%"
        ),
        
        # Motivo de consulta si existe
        rx.cond(
            consulta.motivo_consulta != "",
            rx.text(
                f"Motivo: {consulta.motivo_consulta}",
                font_size="13px",
                color=COLORS["gray"]["600"],
                font_style="italic"
            )
        ),
        
        spacing="1",
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
            # Header con nombre y estado
            rx.hstack(
                rx.vstack(
                    rx.text(
                        consulta.paciente_nombre,
                        font_size="16px",
                        font_weight="bold",
                        color=COLORS["gray"]["800"]
                    ),
                    rx.text(
                        f"Consulta #{consulta.numero_consulta} | {consulta.paciente_documento}",
                        font_size="13px",
                        color=COLORS["gray"]["600"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                
                rx.spacer(),
                
                # Badge de estado
                badge_estado_consulta(
                    consulta.estado, 
                    consulta.prioridad  # ConsultaModel siempre tiene prioridad
                ),
                
                spacing="3",
                align_items="start",
                width="100%"
            ),
            
            # Información del paciente (usar la propiedad display existente)
            rx.text(
                f"👤 {consulta.paciente_info_display}",
                font_size="13px",
                color=COLORS["gray"]["600"]
            ),
            
            # Información adicional de consulta
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
                            icon="play-circle",
                            on_click=lambda: AppState.navegar_a_odontologia_consulta(consulta.id)
                        ),
                        rx.cond(
                            consulta.estado == "programada", 
                            primary_button(
                                text="🟡 Iniciar Consulta",
                                icon="play-circle", 
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
            
            spacing="4",
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
                        font_size="16px",
                        font_weight="bold",
                        color=COLORS["gray"]["800"]
                    ),
                    rx.text(
                        f"HC: {paciente.numero_historia} | {paciente.numero_documento}",
                        font_size="13px",
                        color=COLORS["gray"]["600"]
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
            
            # Información médica importante (simplificada por ahora)
            rx.box(),  # Placeholder - se puede restaurar cuando se implemente info médica completa
            
            # Info adicional para disponibles
            rx.text(
                "Paciente ya atendido por otro odontólogo. Puede requerir intervención adicional.",
                font_size="13px",
                color=COLORS["gray"]["600"],
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
                    icon="plus-circle",
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