"""
🦷 FORMULARIO DE INTERVENCIÓN V4.0 - COMPONENTES NATIVOS
========================================================

Formulario completamente actualizado con:
- Odontograma nativo sin JavaScript
- Selector de procedimientos mejorado
- Panel de dientes simplificado
- Sin errores de JavaScript
- Integración completa con AppState

Autor: Sistema de Gestión Dental
Versión: 4.0 - Componentes Nativos
Fecha: Septiembre 2025
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING
from dental_system.components.odontologia.odontograma_nativo import odontograma_simple
from dental_system.components.odontologia.selector_procedimientos import selector_procedimientos_mejorado
from dental_system.components.odontologia.panel_diente_simple import info_diente_basica

# ==========================================
# 🎨 ESTILOS DEL FORMULARIO V4
# ==========================================

FORM_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": SHADOWS["lg"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["6"],
    "width": "100%",
    "height": "100%"
}

SECTION_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "color": "white",
    "padding": SPACING["4"],
    "border_radius": f"{RADIUS['lg']} {RADIUS['lg']} 0 0",
    "margin_bottom": "0"
}

SECTION_CONTENT_STYLE = {
    "background": COLORS['gray']['25'],
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_top": "none",
    "border_radius": f"0 0 {RADIUS['lg']} {RADIUS['lg']}",
    "padding": SPACING["6"]
}

# ==========================================
# 📝 COMPONENTES DE FORMULARIO
# ==========================================

def header_intervencion() -> rx.Component:
    """📋 Header del formulario con información del paciente"""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("clipboard_plus", size=28, color="primary.600"),
                rx.vstack(
                    rx.text("Nueva Intervención Odontológica", weight="bold", size="5", color="gray.800"),
                    rx.text("Complete todos los campos para registrar la atención", size="3", color="gray.600"),
                    spacing="1",
                    align_items="start"
                ),
                spacing="3",
                align_items="center"
            ),
            rx.spacer(),
            rx.vstack(
                rx.text(
                    rx.cond(
                        AppState.paciente_actual.nombre_completo != "",
                        f"Paciente: {AppState.paciente_actual.nombre_completo}",
                        "No hay paciente seleccionado"
                    ),
                    size="3", 
                    weight="bold", 
                    color="primary.700"
                ),
                rx.text(
                    rx.cond(
                        AppState.paciente_actual.numero_historia != "",
                        f"HC: {AppState.paciente_actual.numero_historia}",
                        "HC: ---"
                    ),
                    size="2", 
                    color="gray.600"
                ),
                spacing="1",
                align_items="end"
            ),
            width="100%",
            align_items="center"
        ),
        **SECTION_HEADER_STYLE
    )

def seccion_dientes() -> rx.Component:
    """🦷 Sección de selección de dientes"""
    return rx.vstack(
        # Header de la sección
        rx.hstack(
            rx.icon("smile", size=20, color="primary.600"),
            rx.text("1. Selecciona los Dientes", weight="bold", size="4"),
            rx.text(
                f"({AppState.total_dientes_seleccionados} seleccionados)",
                size="2",
                color="primary.600",
                weight="medium"
            ),
            spacing="2",
            align_items="center"
        ),
        
        # Odontograma nativo
        odontograma_simple(),
        
        # Info de dientes seleccionados
        rx.cond(
            AppState.total_dientes_seleccionados > 0,
            info_diente_basica(),
            rx.fragment()
        ),
        
        spacing="4",
        width="100%"
    )

def seccion_procedimientos() -> rx.Component:
    """📝 Sección de selección de procedimientos"""
    return rx.vstack(
        # Header de la sección
        rx.hstack(
            rx.icon("file_medical", size=20, color="primary.600"),
            rx.text("2. Selecciona los Procedimientos", weight="bold", size="4"),
            rx.text(
                f"({AppState.total_servicios_seleccionados} procedimientos)",
                size="2",
                color="primary.600",
                weight="medium"
            ),
            spacing="2",
            align_items="center"
        ),
        
        # Selector mejorado
        selector_procedimientos_mejorado(),
        
        spacing="4",
        width="100%"
    )

def seccion_diagnostico() -> rx.Component:
    """🔍 Sección de diagnóstico y observaciones"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("stethoscope", size=20, color="primary.600"),
            rx.text("3. Diagnóstico y Observaciones", weight="bold", size="4"),
            spacing="2",
            align_items="center"
        ),
        
        # Campos del diagnóstico
        rx.vstack(
            # Diagnóstico inicial
            rx.vstack(
                rx.text("Diagnóstico Inicial", size="2", weight="medium", color="gray.700"),
                rx.text_area(
                    placeholder="Describa el diagnóstico inicial del paciente...",
                    value=AppState.diagnostico_inicial,
                    on_change=AppState.set_diagnostico_inicial,
                    rows="3",
                    resize="vertical"
                ),
                spacing="2",
                align_items="start",
                width="100%"
            ),
            
            # Procedimiento realizado
            rx.vstack(
                rx.text("Procedimiento Realizado", size="2", weight="medium", color="gray.700"),
                rx.text_area(
                    placeholder="Describa detalladamente el procedimiento realizado...",
                    value=AppState.procedimiento_realizado,
                    on_change=AppState.set_procedimiento_realizado,
                    rows="4",
                    resize="vertical"
                ),
                spacing="2",
                align_items="start",
                width="100%"
            ),
            
            # Materiales utilizados
            rx.hstack(
                rx.vstack(
                    rx.text("Materiales Utilizados", size="2", weight="medium", color="gray.700"),
                    rx.input(
                        placeholder="Ej: Composite Z350, Anestesia Lidocaína 2%...",
                        value=AppState.materiales_utilizados,
                        on_change=AppState.set_materiales_utilizados,
                        size="3"
                    ),
                    spacing="2",
                    align_items="start",
                    width="70%"
                ),
                rx.vstack(
                    rx.text("Anestesia", size="2", weight="medium", color="gray.700"),
                    rx.select(
                        ["Ninguna", "Lidocaína 2%", "Articaína 4%", "Mepivacaína 3%", "Otro"],
                        placeholder="Tipo de anestesia",
                        value=AppState.anestesia_utilizada,
                        on_change=AppState.set_anestesia_utilizada,
                        size="3"
                    ),
                    spacing="2",
                    align_items="start",
                    width="30%"
                ),
                spacing="4",
                width="100%",
                align_items="start"
            ),
            
            # Observaciones adicionales
            rx.vstack(
                rx.text("Observaciones Adicionales", size="2", weight="medium", color="gray.700"),
                rx.text_area(
                    placeholder="Notas adicionales, recomendaciones, cuidados post-tratamiento...",
                    value=AppState.observaciones_adicionales,
                    on_change=AppState.set_observaciones_adicionales,
                    rows="3",
                    resize="vertical"
                ),
                spacing="2",
                align_items="start",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        
        spacing="4",
        width="100%"
    )

def seccion_costos() -> rx.Component:
    """💰 Sección de resumen de costos"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("calculator", size=20, color="primary.600"),
            rx.text("4. Resumen de Costos", weight="bold", size="4"),
            spacing="2",
            align_items="center"
        ),
        
        # Resumen de costos
        rx.hstack(
            # Total en Bolívares
            rx.box(
                rx.vstack(
                    rx.text("Total Bolívares", size="2", weight="medium", color="gray.700"),
                    rx.text(
                        f"Bs. {AppState.total_bs_intervencion:,.2f}",
                        size="5",
                        weight="bold",
                        color="green.600"
                    ),
                    spacing="2",
                    align_items="center"
                ),
                padding="4",
                background="green.50",
                border="1px solid green.200",
                border_radius="lg",
                text_align="center",
                width="50%"
            ),
            
            # Total en Dólares
            rx.box(
                rx.vstack(
                    rx.text("Total Dólares", size="2", weight="medium", color="gray.700"),
                    rx.text(
                        f"$ {AppState.total_usd_intervencion:,.2f}",
                        size="5",
                        weight="bold",
                        color="blue.600"
                    ),
                    spacing="2",
                    align_items="center"
                ),
                padding="4",
                background="blue.50",
                border="1px solid blue.200",
                border_radius="lg",
                text_align="center",
                width="50%"
            ),
            
            spacing="4",
            width="100%"
        ),
        
        # Descuento opcional
        rx.hstack(
            rx.vstack(
                rx.text("Descuento (%)", size="2", weight="medium", color="gray.700"),
                rx.input(
                    placeholder="0",
                    type="number",
                    value=AppState.descuento_porcentaje,
                    on_change=AppState.set_descuento_porcentaje,
                    size="2",
                    width="100px"
                ),
                spacing="2",
                align_items="start"
            ),
            rx.vstack(
                rx.text("Motivo del Descuento", size="2", weight="medium", color="gray.700"),
                rx.input(
                    placeholder="Ej: Paciente frecuente, promoción...",
                    value=AppState.motivo_descuento,
                    on_change=AppState.set_motivo_descuento,
                    size="2"
                ),
                spacing="2",
                align_items="start",
                width="100%"
            ),
            spacing="4",
            width="100%",
            align_items="start"
        ),
        
        spacing="4",
        width="100%"
    )

def botones_accion() -> rx.Component:
    """⚡ Botones de acción del formulario"""
    return rx.hstack(
        # Botón cancelar
        rx.button(
            rx.icon("x", size=16),
            "Cancelar",
            variant="outline",
            size="3",
            color_scheme="red",
            on_click=AppState.cancelar_intervencion
        ),
        
        rx.spacer(),
        
        # Botón guardar borrador
        rx.button(
            rx.icon("save", size=16),
            "Guardar Borrador",
            variant="outline",
            size="3",
            color_scheme="blue",
            on_click=AppState.guardar_borrador_intervencion
        ),
        
        # Botón finalizar intervención
        rx.button(
            rx.icon("check", size=16),
            "Finalizar Intervención",
            variant="solid",
            size="3",
            color_scheme="green",
            on_click=AppState.finalizar_intervencion,
            disabled=AppState.total_dientes_seleccionados == 0
        ),
        
        width="100%",
        align_items="center",
        padding="4"
    )

# ==========================================
# 🎯 FORMULARIO PRINCIPAL V4
# ==========================================

def formulario_intervencion_v4() -> rx.Component:
    """
    🎯 Formulario de intervención V4.0 - Componentes Nativos
    
    CARACTERÍSTICAS:
    - Odontograma nativo sin JavaScript
    - Selector de procedimientos con autocompletado
    - Panel de dientes simplificado
    - Formulario completo integrado
    - Sin errores de JavaScript
    """
    return rx.box(
        rx.vstack(
            # Header del formulario
            header_intervencion(),
            
            # Contenido principal
            rx.box(
                rx.vstack(
                    # Sección 1: Dientes
                    seccion_dientes(),
                    rx.divider(),
                    
                    # Sección 2: Procedimientos  
                    seccion_procedimientos(),
                    rx.divider(),
                    
                    # Sección 3: Diagnóstico
                    seccion_diagnostico(),
                    rx.divider(),
                    
                    # Sección 4: Costos
                    seccion_costos(),
                    
                    spacing="6",
                    width="100%"
                ),
                **SECTION_CONTENT_STYLE
            ),
            
            # Botones de acción
            botones_accion(),
            
            spacing="0",
            width="100%"
        ),
        style=FORM_CONTAINER_STYLE
    )