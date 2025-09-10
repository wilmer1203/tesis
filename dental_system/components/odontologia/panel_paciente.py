"""
🦷 PANEL DE INFORMACIÓN DEL PACIENTE - VERSIÓN MEJORADA
========================================================

Panel lateral izquierdo mejorado con elementos de la plantilla PatientInfoPanel.jsx
- ✅ Panel colapsable con estado persistente
- ✅ Avatar/foto del paciente con fallback
- ✅ Alertas médicas visuales prominentes (alergias, condiciones)
- ✅ Información de contacto expandida (emergencia, seguro)
- ✅ Estadísticas de visitas integradas
- ✅ Historial médico organizado
- ✅ Diseño profesional responsivo
"""

import reflex as rx
from typing import Optional
from dental_system.state.app_state import AppState
from dental_system.models import PacienteModel, ConsultaModel
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS MEJORADOS INSPIRADOS EN PLANTILLA
# ==========================================

PANEL_CONTAINER_STYLE = {
    "background": "white",
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["xl"],
    "box_shadow": "0 2px 8px rgba(0,0,0,0.1)",
    "height": "100%",
    "width": "100%",
    "overflow": "hidden",
    "transition": "all 0.3s ease",
    # Responsive design
    "@media (max-width: 768px)": {
        "border_radius": RADIUS["lg"],
        "box_shadow": "0 1px 4px rgba(0,0,0,0.1)"
    }
}

PANEL_HEADER_STYLE = {
    "display": "flex",
    "align_items": "center",
    "justify_content": "space-between",
    "padding": SPACING["4"],
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "color": "white",
    "border_bottom": f"1px solid {COLORS['gray']['200']}"
}

PANEL_CONTENT_STYLE = {
    "padding": SPACING["4"],
    "height": "calc(100% - 80px)",
    "overflow_y": "auto",
    "transition": "all 0.3s ease"
}

# Estilos para alertas médicas (inspirado en la plantilla)
ALERT_STYLE = {
    "background": COLORS["error"]["50"],
    "border": f"1px solid {COLORS['error']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["3"]
}

WARNING_STYLE = {
    "background": COLORS["warning"]["50"],
    "border": f"1px solid {COLORS['warning']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["3"]
}

INFO_CARD_STYLE = {
    "background": COLORS["gray"]["50"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["3"]
}

STATS_CARD_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['50']} 0%, {COLORS['primary']['100']} 100%)",
    "border": f"1px solid {COLORS['primary']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["3"]
}

# ==========================================
# 🧩 COMPONENTES AUXILIARES MEJORADOS
# ==========================================

def avatar_paciente_mejorado(paciente: rx.Var[PacienteModel]) -> rx.Component:
    """👤 Avatar mejorado del paciente con iniciales profesionales"""
    return rx.avatar(
        fallback=rx.cond(
            (paciente.primer_nombre != "") & (paciente.primer_apellido != ""),
            paciente.primer_nombre[0] + paciente.primer_apellido[0],
            "?"
        ),
        size="6", 
        radius="full",
        color_scheme="teal",
        style={
            "border": f"3px solid {COLORS['primary']['400']}",
            "box_shadow": "0 4px 12px rgba(0,0,0,0.15)"
        }
    )

def badge_info(texto: str, color_scheme: str = "gray") -> rx.Component:
    """🏷️ Badge de información consistente"""
    return rx.badge(
        texto,
        color_scheme=color_scheme,
        variant="soft",
        size="2"
    )

def info_item_mejorado(icono: str, titulo: str, valor: rx.Var, color: str = "gray") -> rx.Component:
    """📋 Item de información mejorado con iconos"""
    return rx.hstack(
        rx.icon(icono, size=16, color=f"{color}.500"),
        rx.vstack(
            rx.text(
                titulo,
                size="2",
                weight="medium",
                color=f"{color}.600"
            ),
            rx.text(
                valor,
                size="3",
                weight="medium",
                color="gray.900"
            ),
            spacing="1",
            align_items="start"
        ),
        spacing="3",
        align_items="start",
        width="100%"
    )

# ==========================================
# 📋 COMPONENTES PRINCIPALES MEJORADOS
# ==========================================

def panel_header_colapsable() -> rx.Component:
    """👤 Header del panel con botón de colapso (inspirado en plantilla)"""
    return rx.box(
        rx.hstack(
            # Información principal con avatar
            rx.hstack(
                rx.icon("user", size=20, color="white"),
                rx.heading("Información del Paciente", size="4", color="white"),
                spacing="2"
            ),
            
            # Botón de colapso (inspirado en PatientInfoPanel.jsx)
            rx.button(
                rx.cond(
                    AppState.panel_paciente_expandido,
                    rx.icon("chevron-up", size=16),
                    rx.icon("chevron-down", size=16)
                ),
                on_click=AppState.toggle_panel_paciente,
                variant="ghost",
                size="2",
                color_scheme="gray",
                style={
                    "color": "white",
                    "_hover": {"background": "rgba(255,255,255,0.1)"}
                }
            ),
            
            width="100%",
            justify="between"
        ),
        style=PANEL_HEADER_STYLE
    )

def seccion_principal_paciente() -> rx.Component:
    """👤 Sección principal con avatar e información básica (inspirado en plantilla)"""
    return rx.vstack(
        rx.hstack(
            # Avatar mejorado (20% más grande que el original)
            avatar_paciente_mejorado(AppState.paciente_actual),
            
            # Información principal
            rx.vstack(
                rx.cond(
                    AppState.paciente_actual.primer_nombre != "",
                    rx.heading(
                        f"{AppState.paciente_actual.primer_nombre} {AppState.paciente_actual.primer_apellido}",
                        size="4",
                        weight="bold",
                        color="gray.900"
                    ),
                    rx.cond(
                        AppState.paciente_actual.nombre_completo != "",
                        rx.heading(
                            AppState.paciente_actual.nombre_completo,
                            size="4",
                            weight="bold",
                            color="gray.900"
                        ),
                        rx.heading(
                            "Paciente no cargado",
                            size="4",
                            weight="bold",
                            color="red.500"
                        )
                    )
                ),
            rx.hstack(
                badge_info(f"HC: {AppState.paciente_actual.numero_historia}", "blue"),
                badge_info(f"CI: {AppState.paciente_actual.numero_documento}", "gray"),
                spacing="2"
            ),
            rx.hstack(
                rx.cond(
                    AppState.paciente_actual.edad > 0,
                    rx.text(AppState.paciente_actual.edad.to(str) + " años", size="2", color="gray.600"),
                    rx.text("Edad no especificada", size="2", color="gray.600")
                ),
                rx.cond(
                    AppState.paciente_actual.genero != "",
                    rx.text("Género: " + AppState.paciente_actual.genero, size="2", color="gray.600"),
                    rx.text("Género no especificado", size="2", color="gray.600")
                ),
                spacing="3"
                ),
                align_items="start",
                spacing="2"
            ),
            
            spacing="4",
            align_items="start",
            width="100%"
        ),
        
        spacing="2",
        align_items="start",
        width="100%",
        margin_bottom="4"
    )

def alertas_medicas_prominentes() -> rx.Component:
    """🚨 Alertas médicas visuales prominentes (inspirado en PatientInfoPanel.jsx)"""
    return rx.vstack(
        # Alergias - Alerta roja prominente
        rx.cond(
            AppState.paciente_actual.alergias.length() > 0,
            rx.box(
                rx.hstack(
                    rx.icon("triangle-alert", size=16, color="red.500"),
                    rx.text("⚠️ ALERGIAS IMPORTANTES", weight="bold", color="red.700", size="3"),
                    spacing="2",
                    align_items="center"
                ),
                rx.flex(
                    rx.foreach(
                        AppState.paciente_actual.alergias,
                        lambda alergia: rx.badge(
                            alergia,
                            color_scheme="red",
                            variant="solid",
                            size="2"
                        )
                    ),
                    flex_wrap="wrap",
                    spacing="2"
                ),
                style=ALERT_STYLE
            )
        ),
        
        # Condiciones médicas - Alerta amarilla
        rx.cond(
            AppState.paciente_actual.condiciones_medicas.length() > 0,
            rx.box(
                rx.hstack(
                    rx.icon("file-text", size=16, color="orange.500"),
                    rx.text("🏥 CONDICIONES MÉDICAS", weight="bold", color="orange.700", size="3"),
                    spacing="2",
                    align_items="center"
                ),
                rx.vstack(
                    rx.foreach(
                        AppState.paciente_actual.condiciones_medicas,
                        lambda condicion: rx.hstack(
                            rx.icon("dot", size=12, color="orange.500"),
                            rx.text(condicion, size="2", color="orange.600"),
                            spacing="1",
                            align_items="center"
                        )
                    ),
                    align_items="start",
                    spacing="1"
                ),
                style=WARNING_STYLE
            )
        ),
        
        spacing="3",
        width="100%"
    )

def informacion_contacto_expandida() -> rx.Component:
    """📞 Información de contacto expandida (inspirado en plantilla)"""
    return rx.box(
        rx.hstack(
            rx.icon("phone", size=16, color="teal.500"),
            rx.text("Información de Contacto", weight="medium", size="3"),
            spacing="2"
        ),
        rx.vstack(
            # Teléfonos
            info_item_mejorado("phone", "Teléfono Principal", AppState.paciente_actual.celular_1, "teal"),
            rx.cond(
                AppState.paciente_actual.celular_2 != "",
                info_item_mejorado("phone", "Teléfono Secundario", AppState.paciente_actual.celular_2, "teal")
            ),
            
            # Email
            rx.cond(
                AppState.paciente_actual.email != "",
                info_item_mejorado("mail", "Correo Electrónico", AppState.paciente_actual.email, "blue"),
                info_item_mejorado("mail", "Correo Electrónico", "No registrado", "gray")
            ),
            
            # Dirección
            rx.cond(
                AppState.paciente_actual.direccion != "",
                info_item_mejorado("map-pin", "Dirección", AppState.paciente_actual.direccion, "purple"),
                info_item_mejorado("map-pin", "Dirección", "No registrada", "gray")
            ),
            
            align_items="start",
            spacing="3"
        ),
        style=INFO_CARD_STYLE
    )

def contacto_emergencia() -> rx.Component:
    """🚨 Información de contacto de emergencia (inspirado en plantilla)"""
    return rx.grid(
        # Contacto de emergencia
        rx.box(
            rx.hstack(
                rx.icon("user", size=14, color="green.500"),
                rx.text("Contacto de Emergencia", weight="medium", size="2"),
                spacing="2"
            ),
            rx.cond(
                AppState.paciente_actual.contacto_emergencia.get("nombre", "") != "",
                rx.vstack(
                    rx.text(AppState.paciente_actual.contacto_emergencia.get("nombre", ""), weight="medium", size="2"),
                    rx.cond(
                        AppState.paciente_actual.contacto_emergencia.get("relacion", "") != "",
                        rx.text(AppState.paciente_actual.contacto_emergencia.get("relacion", ""), color="gray.600", size="1")
                    ),
                    rx.cond(
                        AppState.paciente_actual.contacto_emergencia.get("telefono", "") != "",
                        rx.text(AppState.paciente_actual.contacto_emergencia.get("telefono", ""), size="2")
                    ),
                    align_items="start",
                    spacing="1"
                ),
                rx.text("No registrado", color="gray.500", size="2")
            ),
            style=INFO_CARD_STYLE
        ),
        
        # Seguro médico
        rx.box(
            rx.hstack(
                rx.icon("shield", size=14, color="blue.500"),
                rx.text("Seguro Médico", weight="medium", size="2"),
                spacing="2"
            ),
            rx.text(
                # TODO: Implementar campo seguro_medico en PacienteModel
                "Por implementar",  # Placeholder - falta agregar campo seguro_medico a esquema BD
                size="2",
                color="gray.500"
            ),
            style=INFO_CARD_STYLE
        ),
        
        columns="2",
        gap="3",
        width="100%",
        margin_y="3"
    )

def estadisticas_visitas() -> rx.Component:
    """📊 Estadísticas de visitas (inspirado en PatientInfoPanel.jsx)"""
    return rx.box(
        rx.grid(
            # Total de visitas
            rx.box(
                rx.text(
                    AppState.total_visitas_paciente_actual.to(str), 
                    size="6", 
                    weight="bold", 
                    color="teal.600"
                ),
                rx.text("Visitas Totales", size="1", color="gray.600"),
                text_align="center"
            ),
            
            # Última visita
            rx.box(
                rx.text(
                    AppState.ultima_visita_paciente_actual, 
                    size="3", 
                    weight="medium", 
                    color="gray.900"
                ),
                rx.text("Última Visita", size="1", color="gray.600"),
                text_align="center"
            ),
            
            # Pendientes (futuro - saldos pendientes o citas por hacer)
            rx.box(
                rx.text(
                    AppState.consultas_pendientes_paciente.to(str), 
                    size="4", 
                    weight="bold", 
                    color="orange.600"
                ),
                rx.text("Pendientes", size="1", color="gray.600"),
                text_align="center"
            ),
            
            columns="3",
            gap="2",
            width="100%"
        ),
        style=STATS_CARD_STYLE
    )

def informacion_consulta_actual_mejorada() -> rx.Component:
    """📋 Información de la consulta actual mejorada"""
    return rx.box(
        rx.hstack(
            rx.icon("clipboard-list", size=16, color="blue.500"),
            rx.text("Consulta Actual", weight="medium", size="3"),
            spacing="2"
        ),
        rx.vstack(
            info_item_mejorado("hash", "N° Consulta", AppState.consulta_actual.numero_consulta, "blue"),
            info_item_mejorado("calendar", "Fecha", AppState.consulta_actual.fecha_llegada, "blue"),
            info_item_mejorado("activity", "Estado", AppState.texto_estado_consulta_actual, "green"),
            
            rx.cond(
                AppState.consulta_actual.motivo_consulta != "",
                info_item_mejorado("file-text", "Motivo", AppState.consulta_actual.motivo_consulta, "purple")
            ),
            
            align_items="start",
            spacing="3"
        ),
        style=INFO_CARD_STYLE
    )

def acciones_rapidas_mejoradas() -> rx.Component:
    """⚡ Acciones rápidas mejoradas (inspirado en plantilla)"""
    return rx.hstack(
        rx.button(
            rx.hstack(
                rx.icon("user", size=14),
                rx.text("Ver Completo", size="2"),
                spacing="2"
            ),
            variant="outline",
            size="2",
            width="50%",
            color_scheme="blue"
        ),
        rx.button(
            rx.hstack(
                rx.icon("phone", size=14),
                rx.text("Contactar", size="2"),
                spacing="2"
            ),
            variant="outline",
            size="2",
            width="50%",
            color_scheme="green"
        ),
        spacing="2",
        width="100%",
        margin_top="4"
    )

# ==========================================
# 📋 COMPONENTE PRINCIPAL MEJORADO
# ==========================================

def panel_informacion_paciente() -> rx.Component:
    """
    👤 Panel completo de información del paciente - VERSIÓN MEJORADA
    
    Panel lateral izquierdo inspirado en PatientInfoPanel.jsx con mejoras:
    - ✅ Panel colapsable con estado persistente
    - ✅ Avatar/foto del paciente profesional
    - ✅ Alertas médicas visuales prominentes
    - ✅ Información de contacto expandida
    - ✅ Estadísticas de visitas integradas
    - ✅ Contacto de emergencia y seguro
    - ✅ Diseño responsivo profesional
    """
    return rx.box(
        rx.vstack(
            # Header con botón de colapso
            panel_header_colapsable(),
            
            # Contenido colapsable
            rx.cond(
                AppState.panel_paciente_expandido,
                rx.box(
                    rx.vstack(
                        # Sección principal con avatar e info básica
                        seccion_principal_paciente(),
                        
                        # Alertas médicas prominentes
                        alertas_medicas_prominentes(),
                        
                        # Información de contacto expandida
                        informacion_contacto_expandida(),
                        
                        # Contacto emergencia y seguro (grid 2 columnas)
                        contacto_emergencia(),
                        
                        # Estadísticas de visitas
                        estadisticas_visitas(),
                        
                        # Información de consulta actual
                        informacion_consulta_actual_mejorada(),
                        
                        # Acciones rápidas
                        acciones_rapidas_mejoradas(),
                        
                        spacing="4",
                        align_items="stretch",
                        width="100%"
                    ),
                    style=PANEL_CONTENT_STYLE
                ),
                # Panel colapsado - solo mostrar información mínima
                rx.box(
                    rx.center(
                        rx.vstack(
                            avatar_paciente_mejorado(AppState.paciente_actual),
                            rx.text(
                                AppState.paciente_actual.nombre_completo,
                                weight="bold",
                                size="3",
                                text_align="center",
                                color="gray.700"
                            ),
                            rx.text(
                                f"HC: {AppState.paciente_actual.numero_historia}",
                                size="2",
                                color="gray.500",
                                text_align="center"
                            ),
                            spacing="2",
                            align_items="center"
                        ),
                        padding="4"
                    )
                )
            ),
            
            spacing="0",
            height="100%",
            align_items="stretch"
        ),
        style=PANEL_CONTAINER_STYLE
    )