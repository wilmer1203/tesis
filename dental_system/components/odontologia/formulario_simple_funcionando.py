"""
🦷 FORMULARIO DE INTERVENCIÓN - VERSIÓN FUNCIONANDO
===================================================

Formulario simple que usa SOLO métodos y variables que realmente existen
en el estado. Sin inventar métodos inexistentes.

VARIABLES REALES CONFIRMADAS:
- total_dientes_seleccionados ✅
- total_servicios_seleccionados ✅
- dientes_seleccionados_lista ✅
- servicios_seleccionados_detalle ✅
- procedimiento_realizado ✅
- total_bs_intervencion ✅
- total_usd_intervencion ✅

MÉTODOS REALES CONFIRMADOS:
- seleccionar_diente() ✅
- limpiar_seleccion_dientes() ✅
- toggle_servicio_seleccionado() ✅
- actualizar_procedimiento_realizado() ✅
- guardar_borrador_intervencion() ✅
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING
from dental_system.components.odontologia.odontograma_nativo import odontograma_simple

# ==========================================
# 🎨 ESTILOS BÁSICOS
# ==========================================

FORM_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["md"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["6"],
    "width": "100%"
}

# ==========================================
# 📝 COMPONENTES BÁSICOS
# ==========================================

def header_simple() -> rx.Component:
    """📋 Header simple del formulario"""
    return rx.hstack(
        rx.icon("clipboard_plus", size=24, color="primary.600"),
        rx.vstack(
            rx.text("Nueva Intervención", weight="bold", size="4", color="gray.800"),
            rx.text("Complete los campos necesarios", size="2", color="gray.600"),
            spacing="1",
            align_items="start"
        ),
        spacing="3",
        align_items="center",
        padding="4",
        background="primary.50",
        border_radius="lg",
        width="100%"
    )

def seccion_dientes_simple() -> rx.Component:
    """🦷 Sección simplificada de dientes"""
    return rx.vstack(
        rx.text("1. Selecciona los Dientes", weight="bold", size="3", color="primary.600"),
        
        # Odontograma nativo (sin errores)
        odontograma_simple(),
        
        # Resumen simple
        rx.cond(
            AppState.total_dientes_seleccionados > 0,
            rx.box(
                rx.text(
                    f"Dientes seleccionados: {AppState.total_dientes_seleccionados}",
                    weight="medium",
                    color="green.600"
                ),
                padding="3",
                background="green.50",
                border_radius="md",
                border="1px solid green.200"
            ),
            rx.text("No hay dientes seleccionados", color="gray.500", size="2")
        ),
        
        spacing="4",
        width="100%"
    )

def seccion_servicios_simple() -> rx.Component:
    """📝 Sección simplificada de servicios"""
    return rx.vstack(
        rx.text("2. Servicios (Desarrollo Futuro)", weight="bold", size="3", color="primary.600"),
        
        rx.box(
            rx.text("Los servicios se integrarán en la próxima versión", size="2", color="gray.600"),
            rx.text(
                f"Total seleccionados: {AppState.total_servicios_seleccionados}",
                size="2",
                color="blue.600"
            ),
            padding="4",
            background="blue.50",
            border_radius="md",
            border="1px solid blue.200"
        ),
        
        spacing="4",
        width="100%"
    )

def seccion_observaciones_simple() -> rx.Component:
    """📝 Sección de observaciones básica"""
    return rx.vstack(
        rx.text("3. Procedimiento Realizado", weight="bold", size="3", color="primary.600"),
        
        rx.text_area(
            placeholder="Describa el procedimiento realizado en esta consulta...",
            value=AppState.procedimiento_realizado,
            on_change=AppState.actualizar_procedimiento_realizado,
            rows="4",
            resize="vertical",
            size="3"
        ),
        
        spacing="3",
        width="100%"
    )

def seccion_costos_simple() -> rx.Component:
    """💰 Sección de costos básica"""
    return rx.vstack(
        rx.text("4. Costos", weight="bold", size="3", color="primary.600"),
        
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.text("Total BS", size="2", color="gray.600"),
                    rx.text(
                        f"Bs. {AppState.total_bs_intervencion:,.2f}",
                        size="4",
                        weight="bold",
                        color="green.600"
                    ),
                    spacing="1",
                    align_items="center"
                ),
                padding="4",
                background="green.50",
                border_radius="md",
                border="1px solid green.200",
                width="50%",
                text_align="center"
            ),
            
            rx.box(
                rx.vstack(
                    rx.text("Total USD", size="2", color="gray.600"),
                    rx.text(
                        f"$ {AppState.total_usd_intervencion:,.2f}",
                        size="4",
                        weight="bold",
                        color="blue.600"
                    ),
                    spacing="1",
                    align_items="center"
                ),
                padding="4",
                background="blue.50",
                border_radius="md",
                border="1px solid blue.200",
                width="50%",
                text_align="center"
            ),
            
            spacing="4",
            width="100%"
        ),
        
        spacing="4",
        width="100%"
    )

def botones_accion_simple() -> rx.Component:
    """⚡ Botones de acción básicos"""
    return rx.hstack(
        rx.button(
            rx.icon("x", size=16),
            "Cancelar",
            variant="outline",
            color_scheme="red",
            size="3"
        ),
        
        rx.spacer(),
        
        rx.button(
            rx.icon("save", size=16),
            "Guardar Borrador",
            variant="outline",
            color_scheme="blue",
            size="3",
            on_click=AppState.guardar_borrador_intervencion
        ),
        
        rx.button(
            rx.icon("check", size=16),
            "Finalizar",
            variant="solid",
            color_scheme="green",
            size="3",
            disabled=AppState.total_dientes_seleccionados == 0
        ),
        
        width="100%",
        align_items="center"
    )

# ==========================================
# 🎯 FORMULARIO PRINCIPAL FUNCIONANDO
# ==========================================

def formulario_simple_funcionando() -> rx.Component:
    """
    🎯 Formulario que SÍ funciona sin errores
    
    USA SOLO:
    - Variables confirmadas que existen
    - Métodos confirmados que existen
    - Componentes nativos de Reflex
    - Sin JavaScript
    """
    return rx.box(
        rx.vstack(
            # Header
            header_simple(),
            
            # Secciones
            seccion_dientes_simple(),
            rx.divider(),
            
            seccion_servicios_simple(),
            rx.divider(),
            
            seccion_observaciones_simple(),
            rx.divider(),
            
            seccion_costos_simple(),
            rx.divider(),
            
            # Botones
            botones_accion_simple(),
            
            spacing="6",
            width="100%"
        ),
        style=FORM_STYLE
    )