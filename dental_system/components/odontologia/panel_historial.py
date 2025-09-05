"""
🦷 COMPONENTE: PANEL DE HISTORIAL CLÍNICO
=======================================

Panel lateral derecho para la página de intervención que muestra:
- Historial cronológico de intervenciones
- Timeline de consultas anteriores
- Notas clínicas previas
- Evolución del tratamiento
- Notas rápidas del odontólogo actual
"""

import reflex as rx
from typing import List, Dict, Any
from dental_system.state.app_state import AppState
from dental_system.models import IntervencionModel
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS DEL PANEL DE HISTORIAL
# ==========================================

PANEL_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": SHADOWS["sm"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["0"],
    "height": "100%",
    "width": "100%",
    "overflow": "hidden"
}

PANEL_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['blue']['500']} 0%, {COLORS['blue']['600']} 100%)",
    "padding": SPACING["4"],
    "color": "white",
    "border_radius": f"{RADIUS['xl']} {RADIUS['xl']} 0 0"
}

SCROLLABLE_CONTENT_STYLE = {
    "height": "calc(100% - 140px)",
    "overflow_y": "auto",
    "overflow_x": "hidden",
    "padding": SPACING["4"]
}

TIMELINE_ITEM_STYLE = {
    "background": COLORS["gray"]["50"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "margin_bottom": SPACING["3"],
    "border_left": f"4px solid {COLORS['primary']['400']}"
}

INTERVENCION_ITEM_STYLE = {
    "background": COLORS["blue"]["25"],
    "border": f"1px solid {COLORS['blue']['200']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "margin_bottom": SPACING["3"],
    "border_left": f"4px solid {COLORS['blue']['400']}"
}

NOTA_RAPIDA_STYLE = {
    "background": COLORS["warning"]["50"],
    "border": f"1px solid {COLORS['warning']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["2"]
}

# ==========================================
# 🧩 COMPONENTES DE TIMELINE
# ==========================================

def timeline_fecha(fecha: str) -> rx.Component:
    """📅 Indicador de fecha en timeline"""
    return rx.hstack(
        rx.box(
            width="12px",
            height="12px",
            border_radius="50%",
            background=COLORS["primary"]["400"],
            border=f"3px solid {COLORS['primary']['100']}"
        ),
        rx.text(
            fecha,
            font_size="12px",
            font_weight="bold",
            color=COLORS["primary"]["600"]
        ),
        spacing="2",
        align_items="center",
        margin_bottom="2"
    )

def intervencion_timeline_item(intervencion: rx.Var[IntervencionModel]) -> rx.Component:
    """🦷 Item de intervención en timeline"""
    return rx.box(
        rx.vstack(
            # Fecha de la intervención
            timeline_fecha(intervencion.fecha_creacion_display if hasattr(intervencion, 'fecha_creacion_display') else "Fecha no disponible"),
            
            # Información principal
            rx.hstack(
                rx.box(
                    "🦷",
                    font_size="20px",
                    color=COLORS["blue"]["500"]
                ),
                rx.vstack(
                    rx.text(
                        intervencion.procedimiento_realizado,
                        font_size="14px",
                        font_weight="bold",
                        color=COLORS["gray"]["800"]
                    ),
                    rx.text(
                        f"Dr. {intervencion.odontologo_nombre}" if hasattr(intervencion, 'odontologo_nombre') else "Odontólogo",
                        font_size="12px",
                        color=COLORS["gray"]["600"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                rx.spacer(),
                rx.text(
                    rx.cond(
                        intervencion.precio_final,
                        f"${intervencion.precio_final:,.0f}",
                        "Sin costo"
                    ),
                    font_size="13px",
                    font_weight="medium",
                    color=COLORS["success"]["600"]
                ),
                spacing="3",
                align_items="start",
                width="100%"
            ),
            
            # Dientes afectados si está disponible
            rx.cond(
                hasattr(intervencion, 'dientes_afectados') and intervencion.dientes_afectados,
                rx.text(
                    f"🦷 Dientes: {intervencion.dientes_display}",
                    font_size="12px",
                    color=COLORS["gray"]["600"]
                )
            ),
            
            # Materiales utilizados si está disponible
            rx.cond(
                intervencion.materiales_utilizados != "",
                rx.text(
                    f"🛠️ Materiales: {intervencion.materiales_utilizados}",
                    font_size="12px",
                    color=COLORS["gray"]["600"]
                )
            ),
            
            # Complicaciones si las hay
            rx.cond(
                intervencion.complicaciones != "",
                rx.text(
                    intervencion.complicaciones,
                    font_size="12px",
                    color=COLORS["gray"]["500"],
                    font_style="italic"
                )
            ),
            
            spacing="2",
            align_items="start",
            width="100%"
        ),
        style=INTERVENCION_ITEM_STYLE
    )

def consulta_timeline_item(consulta_info: Dict[str, Any]) -> rx.Component:
    """📋 Item de consulta general en timeline"""
    return rx.box(
        rx.vstack(
            # Fecha de la consulta
            timeline_fecha(
                rx.cond(
                    consulta_info.fecha_llegada,
                    consulta_info.fecha_llegada,
                    "Fecha no disponible"
                )
            ),
            
            # Información de la consulta
            rx.hstack(
                rx.box(
                    "📋",
                    font_size="18px",
                    color=COLORS["gray"]["500"]
                ),
                rx.vstack(
                    rx.text(
                        rx.cond(
                            consulta_info.motivo_consulta,
                            consulta_info.motivo_consulta,
                            "Consulta general"
                        ),
                        font_size="14px",
                        font_weight="medium",
                        color=COLORS["gray"]["700"]
                    ),
                    rx.text(
                        f"Estado: {consulta_info.estado}",
                        font_size="12px",
                        color=COLORS["gray"]["600"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                spacing="3",
                align_items="start",
                width="100%"
            ),
            
            # Observaciones si las hay
            rx.cond(
                consulta_info.get("observaciones"),
                rx.text(
                    consulta_info.get("observaciones"),
                    font_size="12px",
                    color=COLORS["gray"]["500"],
                    font_style="italic"
                )
            ),
            
            spacing="2",
            align_items="start",
            width="100%"
        ),
        style=TIMELINE_ITEM_STYLE
    )

# ==========================================
# 📝 COMPONENTES DE NOTAS RÁPIDAS
# ==========================================

def nota_rapida_item(nota_text: str, timestamp: str) -> rx.Component:
    """📝 Item individual de nota rápida"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("📝", font_size="14px"),
                rx.text(
                    timestamp,
                    font_size="11px",
                    color=COLORS["gray"]["500"]
                ),
                rx.spacer(),
                rx.button(
                    "❌",
                    size="1",
                    variant="ghost",
                    color_scheme="red"
                ),
                spacing="2",
                align_items="center",
                width="100%"
            ),
            rx.text(
                nota_text,
                font_size="12px",
                color=COLORS["gray"]["700"]
            ),
            spacing="1",
            width="100%"
        ),
        style=NOTA_RAPIDA_STYLE
    )

def formulario_nota_rapida() -> rx.Component:
    """📝 Formulario para agregar notas rápidas"""
    return rx.vstack(
        rx.text_area(
            placeholder="Agregar nota rápida sobre el tratamiento...",
            height="60px",
            font_size="13px"
        ),
        rx.hstack(
            rx.spacer(),
            rx.button(
                "💾 Guardar Nota",
                size="2",
                color_scheme="blue"
            ),
            spacing="2",
            width="100%"
        ),
        spacing="2",
        width="100%",
        background=COLORS["blue"]["25"],
        padding=SPACING["3"],
        border_radius=RADIUS["lg"],
        border=f"1px solid {COLORS['blue']['200']}"
    )

# ==========================================
# 📋 SECCIONES PRINCIPALES
# ==========================================

def seccion_intervenciones_previas() -> rx.Component:
    """🦷 Lista de intervenciones previas"""
    return rx.cond(
        AppState.intervenciones_anteriores.length() > 0,
        rx.vstack(
            rx.hstack(
                rx.text(
                    "🦷 Intervenciones Previas",
                    font_size="14px",
                    font_weight="bold",
                    color=COLORS["blue"]["700"]
                ),
                rx.spacer(),
                rx.badge(
                    AppState.intervenciones_anteriores.length(),
                    color_scheme="blue",
                    size="2"
                ),
                spacing="2",
                align_items="center",
                width="100%",
                margin_bottom="3"
            ),
            
            # Timeline de intervenciones
            rx.vstack(
                rx.foreach(
                    AppState.intervenciones_anteriores,
                    intervencion_timeline_item
                ),
                spacing="0",
                width="100%"
            ),
            
            spacing="0",
            width="100%"
        ),
        # Estado vacío
        rx.center(
            rx.vstack(
                rx.text("🦷", font_size="32px", color=COLORS["gray"]["400"]),
                rx.text(
                    "Sin intervenciones previas",
                    font_size="13px",
                    color=COLORS["gray"]["500"]
                ),
                spacing="2",
                align_items="center"
            ),
            padding="6"
        )
    )

def seccion_historial_consultas() -> rx.Component:
    """📋 Historial general de consultas"""
    return rx.cond(
        AppState.historial_paciente_actual.length() > 0,
        rx.vstack(
            rx.hstack(
                rx.text(
                    "📋 Historial de Consultas",
                    font_size="14px",
                    font_weight="bold",
                    color=COLORS["gray"]["700"]
                ),
                rx.spacer(),
                rx.badge(
                    AppState.historial_paciente_actual.length(),
                    color_scheme="gray",
                    size="2"
                ),
                spacing="2",
                align_items="center",
                width="100%",
                margin_bottom="3"
            ),
            
            # Timeline de consultas (limitado a las últimas 5)
            rx.vstack(
                rx.foreach(
                    rx.cond(
                        AppState.historial_paciente_actual.length() > 5,
                        AppState.historial_paciente_actual[:5],
                        AppState.historial_paciente_actual
                    ),
                    lambda item: consulta_timeline_item(item)
                ),
                spacing="0",
                width="100%"
            ),
            
            # Enlace para ver más si hay más de 5
            rx.cond(
                AppState.historial_paciente_actual.length() > 5,
                rx.center(
                    rx.button(
                        f"Ver {AppState.historial_paciente_actual.length() - 5} consultas más...",
                        size="2",
                        variant="ghost",
                        color_scheme="gray"
                    ),
                    width="100%",
                    margin_top="2"
                )
            ),
            
            spacing="0",
            width="100%"
        ),
        # Estado vacío
        rx.center(
            rx.vstack(
                rx.text("📋", font_size="32px", color=COLORS["gray"]["400"]),
                rx.text(
                    "Sin historial previo",
                    font_size="13px",
                    color=COLORS["gray"]["500"]
                ),
                spacing="2",
                align_items="center"
            ),
            padding="6"
        )
    )

def seccion_notas_rapidas() -> rx.Component:
    """📝 Sección de notas rápidas del odontólogo"""
    return rx.vstack(
        rx.hstack(
            rx.text(
                "📝 Notas Rápidas",
                font_size="14px",
                font_weight="bold",
                color=COLORS["warning"]["700"]
            ),
            rx.spacer(),
            rx.button(
                "➕ Nueva",
                size="1",
                variant="outline",
                color_scheme="orange"
            ),
            spacing="2",
            align_items="center",
            width="100%",
            margin_bottom="3"
        ),
        
        # Formulario para nueva nota
        formulario_nota_rapida(),
        
        # Lista de notas existentes (placeholder)
        nota_rapida_item(
            "Paciente responde bien al tratamiento. Continuar con obturación en próxima cita.",
            "Hace 2 horas"
        ),
        nota_rapida_item(
            "Revisar sensibilidad dental en diente 24",
            "Ayer"
        ),
        
        spacing="3",
        width="100%"
    )

# ==========================================
# 📋 COMPONENTE PRINCIPAL
# ==========================================

def panel_historial_notas() -> rx.Component:
    """
    📚 Panel completo de historial clínico y notas
    
    Panel lateral derecho para la página de intervención.
    Muestra cronológicamente el historial del paciente.
    """
    return rx.box(
        rx.vstack(
            # Header del panel
            rx.box(
                rx.hstack(
                    rx.text(
                        "📚",
                        font_size="24px",
                        color="white"
                    ),
                    rx.text(
                        "Historial Clínico",
                        font_size="18px",
                        font_weight="bold",
                        color="white"
                    ),
                    rx.spacer(),
                    rx.button(
                        "🔄",
                        size="2",
                        variant="ghost",
                        color="white",
                        on_click=lambda: AppState.cargar_historial_paciente(AppState.paciente_actual.id),
                        loading=AppState.cargando_intervencion
                    ),
                    spacing="3",
                    align_items="center",
                    width="100%"
                ),
                style=PANEL_HEADER_STYLE
            ),
            
            # Contenido scrolleable
            rx.box(
                rx.vstack(
                    # Sección de intervenciones previas (más importante)
                    seccion_intervenciones_previas(),
                    
                    rx.divider(margin_y="4"),
                    
                    # Sección de notas rápidas
                    seccion_notas_rapidas(),
                    
                    rx.divider(margin_y="4"),
                    
                    # Sección de historial general
                    seccion_historial_consultas(),
                    
                    spacing="4",
                    width="100%"
                ),
                style=SCROLLABLE_CONTENT_STYLE
            ),
            
            spacing="0",
            height="100%"
        ),
        style=PANEL_CONTAINER_STYLE
    )