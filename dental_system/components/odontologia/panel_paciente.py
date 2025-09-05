"""
🦷 COMPONENTE: PANEL DE INFORMACIÓN DEL PACIENTE
==============================================

Panel lateral izquierdo para la página de intervención que muestra:
- Información personal del paciente
- Datos médicos importantes (alergias, condiciones)
- Información de contacto
- Foto/avatar del paciente
- Datos de la consulta actual
"""

import reflex as rx
from typing import Optional
from dental_system.state.app_state import AppState
from dental_system.models import PacienteModel, ConsultaModel
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS DEL PANEL DE PACIENTE
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
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "padding": SPACING["6"],
    "color": "white",
    "border_radius": f"{RADIUS['xl']} {RADIUS['xl']} 0 0"
}

PANEL_CONTENT_STYLE = {
    "padding": SPACING["6"],
    "height": "calc(100% - 180px)",  # Espacio para header
    "overflow_y": "auto"
}

AVATAR_CONTAINER_STYLE = {
    "width": "80px",
    "height": "80px",
    "border_radius": "50%",
    "background": "rgba(255, 255, 255, 0.2)",
    "border": "3px solid rgba(255, 255, 255, 0.3)",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "font_size": "36px",
    "color": "white"
}

INFO_CARD_STYLE = {
    "background": COLORS["gray"]["50"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "margin_bottom": SPACING["4"]
}

ALERT_CARD_STYLE = {
    "background": COLORS["error"]["50"],
    "border": f"1px solid {COLORS['error']['200']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "margin_bottom": SPACING["4"]
}

WARNING_CARD_STYLE = {
    "background": COLORS["warning"]["50"],
    "border": f"1px solid {COLORS['warning']['200']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "margin_bottom": SPACING["4"]
}

# ==========================================
# 🧩 COMPONENTES AUXILIARES
# ==========================================

def avatar_paciente(paciente: rx.Var[PacienteModel]) -> rx.Component:
    """👤 Avatar del paciente con iniciales"""
    return rx.box(
        # Usar iniciales del nombre como avatar
        rx.cond(
            (paciente.primer_nombre.length() > 0) & (paciente.primer_apellido.length() > 0),
            f"{paciente.primer_nombre[0]}{paciente.primer_apellido[0]}",
            rx.cond(
                paciente.primer_nombre.length() > 0,
                f"{paciente.primer_nombre[0]}?",
                "??"
            )
        ),
        style=AVATAR_CONTAINER_STYLE
    )

def badge_prioridad_consulta(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """🚨 Badge de prioridad de la consulta"""
    return rx.cond(
        consulta.prioridad == "urgente",
        rx.badge(
            "🚨 URGENTE",
            color_scheme="red",
            size="3",
            font_weight="bold"
        ),
        rx.cond(
            consulta.prioridad == "alta",
            rx.badge(
                "⚡ ALTA PRIORIDAD",
                color_scheme="orange",
                size="2"
            ),
            rx.cond(
                consulta.prioridad != "normal",
                rx.badge(
                    consulta.prioridad.upper(),
                    color_scheme="gray",
                    size="2"
                )
            )
        )
    )

def info_item(icono: str, titulo: str, valor: rx.Var, color: str = "gray") -> rx.Component:
    """📋 Item de información individual"""
    return rx.hstack(
        rx.text(icono, font_size="16px"),
        rx.vstack(
            rx.text(
                titulo,
                font_size="12px",
                font_weight="medium",
                color=COLORS["gray"]["500"],
                margin_bottom="1px"
            ),
            rx.text(
                valor,
                font_size="14px",
                font_weight="medium",
                color=COLORS[color]["700"]
            ),
            spacing="0",
            align_items="start"
        ),
        spacing="3",
        align_items="start",
        width="100%"
    )

# ==========================================
# 📋 COMPONENTES PRINCIPALES
# ==========================================

def panel_header_paciente() -> rx.Component:
    """👤 Header del panel con información principal del paciente"""
    return rx.box(
        rx.hstack(
            # Avatar del paciente
            avatar_paciente(AppState.paciente_actual),
            
            # Información principal
            rx.vstack(
                rx.text(
                    AppState.paciente_actual.nombre_completo,
                    font_size="20px",
                    font_weight="bold",
                    color="white"
                ),
                rx.text(
                    f"HC: {AppState.paciente_actual.numero_historia}",
                    font_size="14px",
                    color="rgba(255, 255, 255, 0.8)"
                ),
                rx.text(
                    f"{AppState.paciente_actual.tipo_documento}: {AppState.paciente_actual.numero_documento}",
                    font_size="14px",
                    color="rgba(255, 255, 255, 0.8)"
                ),
                # Badge de prioridad si aplica
                badge_prioridad_consulta(AppState.consulta_actual),
                spacing="1",
                align_items="start"
            ),
            
            spacing="4",
            align_items="start",
            width="100%"
        ),
        style=PANEL_HEADER_STYLE
    )

def informacion_personal() -> rx.Component:
    """👤 Información personal del paciente"""
    return rx.box(
        rx.vstack(
            rx.text(
                "👤 Información Personal",
                font_size="16px",
                font_weight="bold",
                color=COLORS["gray"]["700"],
                margin_bottom="3"
            ),
            
            # Edad y género
            rx.hstack(
                info_item(
                    "🎂", 
                    "Edad", 
                    rx.cond(
                        AppState.paciente_actual.edad > 0,
                        f"{AppState.paciente_actual.edad} años",
                        "No especificada"
                    )
                ),
                info_item(
                    "👤", 
                    "Género", 
                    rx.cond(
                        AppState.paciente_actual.genero.length() > 0,
                        AppState.paciente_actual.genero,
                        "No especificado"
                    )
                ),
                spacing="4",
                width="100%"
            ),
            
            # Contacto
            info_item("📞", "Teléfono Principal", AppState.paciente_actual.celular_display),
            
            rx.cond(
                AppState.paciente_actual.email != "",
                info_item("📧", "Email", AppState.paciente_actual.email)
            ),
            
            # Dirección si está disponible
            rx.cond(
                AppState.paciente_actual.direccion != "",
                info_item("🏠", "Dirección", AppState.paciente_actual.direccion)
            ),
            
            spacing="3",
            align_items="start",
            width="100%"
        ),
        style=INFO_CARD_STYLE
    )

def informacion_medica() -> rx.Component:
    """🏥 Información médica importante"""
    return rx.vstack(
        # Alergias (si las hay)
        rx.cond(
            AppState.paciente_actual.alergias.length() > 0,
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("⚠️", font_size="20px", color=COLORS["error"]["500"]),
                        rx.text(
                            "ALERGIAS IMPORTANTES",
                            font_size="14px",
                            font_weight="bold",
                            color=COLORS["error"]["700"]
                        ),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.text(
                        AppState.paciente_actual.alergias_display,
                        font_size="13px",
                        color=COLORS["error"]["600"],
                        font_weight="medium"
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                style=ALERT_CARD_STYLE
            )
        ),
        
        # Condiciones médicas (si las hay)
        rx.cond(
            AppState.paciente_actual.condiciones_medicas.length() > 0,
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("🏥", font_size="20px", color=COLORS["warning"]["500"]),
                        rx.text(
                            "CONDICIONES MÉDICAS",
                            font_size="14px",
                            font_weight="bold",
                            color=COLORS["warning"]["700"]
                        ),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.text(
                        AppState.paciente_actual.condiciones_display,
                        font_size="13px",
                        color=COLORS["warning"]["600"],
                        font_weight="medium"
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                style=WARNING_CARD_STYLE
            )
        ),
        
        # Medicamentos actuales (si los hay)
        rx.cond(
            AppState.paciente_actual.medicamentos_actuales.length() > 0,
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("💊", font_size="16px", color=COLORS["blue"]["500"]),
                        rx.text(
                            "Medicamentos Actuales",
                            font_size="14px",
                            font_weight="bold",
                            color=COLORS["blue"]["700"]
                        ),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.text(
                        AppState.paciente_actual.medicamentos_display if hasattr(AppState.paciente_actual, 'medicamentos_display') else "Ver lista",
                        font_size="13px",
                        color=COLORS["blue"]["600"]
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                style=INFO_CARD_STYLE
            )
        ),
        
        spacing="4",
        width="100%"
    )

def informacion_consulta_actual() -> rx.Component:
    """📋 Información de la consulta actual"""
    return rx.box(
        rx.vstack(
            rx.text(
                "📋 Consulta Actual",
                font_size="16px",
                font_weight="bold",
                color=COLORS["gray"]["700"],
                margin_bottom="3"
            ),
            
            info_item("🔢", "N° Consulta", AppState.consulta_actual.numero_consulta),
            
            info_item(
                "📅", 
                "Fecha", 
                AppState.consulta_actual.fecha_llegada_display if hasattr(AppState.consulta_actual, 'fecha_llegada_display') else AppState.consulta_actual.fecha_llegada
            ),
            
            info_item("🎯", "Estado", AppState.texto_estado_consulta_actual, "blue"),
            
            rx.cond(
                AppState.consulta_actual.motivo_consulta != "",
                info_item("📝", "Motivo", AppState.consulta_actual.motivo_consulta)
            ),
            
            rx.cond(
                AppState.consulta_actual.observaciones != "",
                info_item("💬", "Observaciones", AppState.consulta_actual.observaciones)
            ),
            
            spacing="3",
            align_items="start",
            width="100%"
        ),
        style=INFO_CARD_STYLE
    )

def resumen_historial_previo() -> rx.Component:
    """📚 Resumen del historial clínico previo"""
    return rx.cond(
        AppState.tiene_historial_cargado,
        rx.box(
            rx.vstack(
                rx.text(
                    "📚 Historial Clínico",
                    font_size="16px",
                    font_weight="bold",
                    color=COLORS["gray"]["700"],
                    margin_bottom="3"
                ),
                
                rx.cond(
                    AppState.historial_paciente_resumen["tiene_historial"],
                    rx.vstack(
                        info_item("📊", "Total Consultas", AppState.historial_paciente_resumen["total_entradas"]),
                        info_item("🦷", "Intervenciones", AppState.historial_paciente_resumen["intervenciones_previas"]),
                        info_item("📅", "Última Consulta", AppState.historial_paciente_resumen["ultima_consulta"]),
                        
                        rx.cond(
                            AppState.historial_paciente_resumen["intervenciones_previas"].to(int) > 0,
                            info_item("🔧", "Última Intervención", AppState.historial_paciente_resumen["ultima_intervencion"])
                        ),
                        
                        spacing="2",
                        width="100%"
                    ),
                    rx.text(
                        "Sin historial clínico previo",
                        font_size="13px",
                        color=COLORS["gray"]["500"],
                        font_style="italic"
                    )
                ),
                
                spacing="3",
                align_items="start",
                width="100%"
            ),
            style=INFO_CARD_STYLE
        ),
        # Mostrar loading o botón para cargar historial
        rx.box(
            rx.center(
                rx.button(
                    "📚 Cargar Historial",
                    size="2",
                    variant="outline",
                    on_click=lambda: AppState.cargar_historial_paciente(AppState.paciente_actual.id),
                    loading=AppState.cargando_intervencion
                ),
                width="100%"
            ),
            style=INFO_CARD_STYLE
        )
    )

def acciones_rapidas_paciente() -> rx.Component:
    """⚡ Acciones rápidas para el paciente"""
    return rx.hstack(
        rx.button(
            "👤 Ver Completo",
            size="2",
            variant="outline",
            width="50%"
        ),
        rx.button(
            "📞 Contactar",
            size="2",
            variant="outline",
            width="50%"
        ),
        spacing="2",
        width="100%",
        margin_top="4"
    )

# ==========================================
# 📋 COMPONENTE PRINCIPAL
# ==========================================

def panel_informacion_paciente() -> rx.Component:
    """
    👤 Panel completo de información del paciente
    
    Panel lateral izquierdo para la página de intervención.
    Incluye toda la información relevante del paciente y consulta actual.
    """
    return rx.box(
        rx.vstack(
            # Header con información principal
            panel_header_paciente(),
            
            # Contenido scrolleable
            rx.box(
                rx.vstack(
                    # Información personal
                    informacion_personal(),
                    
                    # Información médica (alergias, condiciones)
                    informacion_medica(),
                    
                    # Información de la consulta actual
                    informacion_consulta_actual(),
                    
                    # Resumen del historial previo
                    resumen_historial_previo(),
                    
                    # Acciones rápidas
                    acciones_rapidas_paciente(),
                    
                    spacing="4",
                    width="100%"
                ),
                style=PANEL_CONTENT_STYLE
            ),
            
            spacing="0",
            height="100%"
        ),
        style=PANEL_CONTAINER_STYLE
    )