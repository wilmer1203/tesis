"""
🦷 FORMULARIO DE INTERVENCIÓN INTEGRADO V3.0
==============================================

Formulario completamente integrado con el odontograma interactivo que permite:
- Selección visual de dientes desde el odontograma
- Registro de procedimientos por diente
- Cálculo automático de costos
- Integración con servicios y materiales
- Sincronización bidireccional con el odontograma

Autor: Sistema de Gestión Dental
Versión: 3.0 - Integración Completa
Fecha: Septiembre 2025
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS DEL FORMULARIO INTEGRADO
# ==========================================

FORM_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": SHADOWS["lg"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["4"],
    "height": "100%",
    "overflow_y": "auto"
}

SECTION_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['gray']['25']} 0%, {COLORS['primary']['25']} 100%)",
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "margin_bottom": SPACING["3"]
}

DIENTE_CARD_STYLE = {
    "background": "white",
    "border": f"2px solid {COLORS['primary']['300']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["2"],
    "transition": "all 0.2s ease",
    "_hover": {
        "border_color": COLORS['primary']['500'],
        "box_shadow": SHADOWS["md"]
    }
}

SERVICE_ITEM_STYLE = {
    "background": COLORS['gray']['50'],
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["2"],
    "_hover": {
        "background": COLORS['primary']['50'],
        "border_color": COLORS['primary']['300']
    }
}

COST_SUMMARY_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['success']['50']} 0%, {COLORS['gray']['50']} 100%)",
    "border": f"2px solid {COLORS['success']['300']}",
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "box_shadow": SHADOWS["md"]
}

# ==========================================
# 🦷 SELECCIÓN DE DIENTES INTEGRADA
# ==========================================

def selector_dientes_integrado() -> rx.Component:
    """🦷 Panel de selección de dientes sincronizado con odontograma"""
    return rx.box(
        rx.vstack(
            # Header de sección
            rx.hstack(
                rx.icon("target", size=20, color="primary.600"),
                rx.text("Dientes a Intervenir", weight="bold", size="4", color="primary.700"),
                rx.spacer(),
                rx.badge(
                    f"{rx.cond(AppState.total_dientes_seleccionados, AppState.total_dientes_seleccionados, 0)} seleccionados",
                    color=COLORS["primary"]['500'],
                    size="2"
                ),
                spacing="2",
                align_items="center",
                width="100%",
                margin_bottom="3"
            ),
            
            # Instrucciones
            rx.cond(
                AppState.total_dientes_seleccionados == 0,
                rx.callout(
                    "💡 Selecciona los dientes desde el Odontograma en el panel central",
                    icon="info",
                    color_scheme="blue",
                    size="2",
                    width="100%"
                ),
                rx.box()
            ),
            
            # Lista de dientes seleccionados
            rx.cond(
                AppState.total_dientes_seleccionados > 0,
                rx.vstack(
                    rx.text("🦷 Dientes Seleccionados:", weight="medium", size="3", margin_bottom="2"),
                    rx.foreach(
                        AppState.dientes_seleccionados_lista,
                        diente_seleccionado_card
                    ),
                    width="100%"
                ),
                rx.box()
            ),
            
            # Botones de gestión
            rx.cond(
                AppState.total_dientes_seleccionados > 0,
                rx.hstack(
                    rx.button(
                        rx.icon("x", size=16),
                        "Limpiar Selección",
                        variant="outline",
                        color_scheme="red",
                        size="2",
                        on_click=AppState.limpiar_seleccion_dientes
                    ),
                    rx.button(
                        rx.icon("plus", size=16),
                        "Agregar Más",
                        variant="outline",
                        color_scheme="blue", 
                        size="2",
                        on_click=AppState.activar_modo_seleccion_multiple
                    ),
                    spacing="2",
                    width="100%",
                    margin_top="3"
                ),
                rx.box()
            ),
            
            spacing="2",
            width="100%"
        ),
        style=SECTION_STYLE
    )

def diente_seleccionado_card(diente_info: dict) -> rx.Component:
    """🦷 Card de diente individual seleccionado"""
    return rx.card(
        rx.hstack(
            # Número y ubicación del diente
            rx.vstack(
                rx.text(f"Diente #{diente_info['numero']}", weight="bold", size="3", color="primary.600"),
                rx.text(f"{diente_info['tipo']} - {diente_info['cuadrante']}", size="2", color="gray.600"),
                align_items="start",
                spacing="0"
            ),
            
            rx.spacer(),
            
            # Estado actual
            rx.vstack(
                rx.badge(
                    diente_info.get('estado_actual', 'Normal'), 
                    color_scheme=rx.match(
                        diente_info.get('estado_actual', 'Normal'),
                        ("Sano", "green"),
                        ("Caries", "orange"),
                        ("Caries Profunda", "red"),
                        ("Obturado", "blue"),
                        ("Extraído", "gray"),
                        "gray"
                    ),
                    size="2"
                ),
                rx.text("Estado actual", size="1", color="gray.500"),
                align_items="center",
                spacing="1"
            ),
            
            # Botón remover
            rx.button(
                rx.icon("x", size=14),
                size="1",
                variant="ghost",
                color_scheme="red",
                on_click=lambda: AppState.remover_diente_seleccionado(diente_info['numero'])
            ),
            
            spacing="3",
            align_items="center",
            width="100%"
        ),
        style=DIENTE_CARD_STYLE,
        width="100%"
    )

# ==========================================
# 🛠️ SELECCIÓN DE SERVICIOS/PROCEDIMIENTOS
# ==========================================

def selector_servicios() -> rx.Component:
    """🛠️ Panel de selección de servicios odontológicos"""
    return rx.box(
        rx.vstack(
            # Header de servicios
            rx.hstack(
                rx.icon("wrench", size=20, color="blue.600"),
                rx.text("Procedimientos a Realizar", weight="bold", size="4", color="blue.700"),
                rx.spacer(),
                rx.button(
                    rx.icon("refresh_cw", size=16),
                    "Actualizar",
                    variant="outline",
                    size="2",
                    on_click=AppState.cargar_servicios_disponibles
                ),
                spacing="2",
                align_items="center",
                width="100%",
                margin_bottom="3"
            ),
            
            # Búsqueda rápida
            rx.input(
                placeholder="🔍 Buscar procedimiento...",
                value=AppState.filtro_servicios,
                on_change=AppState.filtrar_servicios,
                size="3",
                width="100%",
                margin_bottom="3"
            ),
            
            # Lista de servicios disponibles
            rx.vstack(
                rx.foreach(
                    AppState.servicios_disponibles,
                    servicio_item_card
                ),
                width="100%",
                max_height="400px",
                overflow_y="auto",
                spacing="2"
            ),
            
            spacing="2",
            width="100%"
        ),
        style=SECTION_STYLE
    )

def servicio_item_card(servicio) -> rx.Component:
    """🛠️ Card de servicio individual"""
    return rx.card(
        rx.hstack(
            # Checkbox de selección
            rx.checkbox(
                checked=AppState.servicios_seleccionados.contains(servicio.codigo),
                on_change=lambda checked, codigo=servicio.codigo: AppState.toggle_servicio_seleccionado(codigo, checked)
            ),
            
            # Información del servicio
            rx.vstack(
                rx.text(servicio.nombre, weight="bold", size="3"),
                rx.text(servicio.descripcion, size="2", color="gray.600"),
                rx.hstack(
                    rx.badge(servicio.categoria, color_scheme="gray", size="1"),
                    rx.badge(f"~30 min", color_scheme="blue", size="1"),
                    spacing="2"
                ),
                align_items="start",
                spacing="1",
                flex="1"
            ),
            
            # Precios
            rx.vstack(
                rx.text(f"${servicio.precio_base:.2f}", weight="bold", size="3", color="green.600"),
                rx.text(f"Bs {servicio.precio_base * 36:.0f}", size="2", color="green.500"),
                align_items="end",
                spacing="0"
            ),
            
            spacing="3",
            align_items="start",
            width="100%"
        ),
        style=SERVICE_ITEM_STYLE,
        width="100%"
    )

# ==========================================
# 💰 RESUMEN DE COSTOS
# ==========================================

def resumen_costos() -> rx.Component:
    """💰 Panel de resumen de costos de la intervención"""
    return rx.box(
        rx.vstack(
            # Header de costos
            rx.hstack(
                rx.icon("dollar_sign", size=20, color="green.600"),
                rx.text("Resumen de Costos", weight="bold", size="4", color="green.700"),
                rx.spacer(),
                rx.button(
                    rx.icon("calculator", size=16),
                    "Recalcular",
                    variant="outline",
                    size="2",
                    on_click=AppState.recalcular_costos_intervencion
                ),
                spacing="2",
                align_items="center",
                width="100%",
                margin_bottom="3"
            ),
            
            # Desglose por servicio
            rx.cond(
                AppState.total_servicios_seleccionados > 0,
                rx.vstack(
                    rx.text("📋 Servicios Seleccionados:", weight="medium", size="3"),
                    rx.foreach(
                        AppState.servicios_seleccionados_detalle,
                        costo_servicio_item
                    ),
                    width="100%",
                    margin_bottom="3"
                ),
                rx.callout(
                    "Selecciona servicios para ver el desglose de costos",
                    icon="info",
                    color_scheme="blue",
                    size="2"
                )
            ),
            
            # Totales generales
            rx.cond(
                AppState.total_servicios_seleccionados > 0,
                rx.vstack(
                    rx.divider(),
                    rx.hstack(
                        rx.text("Total USD:", weight="bold", size="4"),
                        rx.spacer(),
                        rx.text(f"${AppState.total_usd_intervencion:.2f}", weight="bold", size="5", color="green.600"),
                        width="100%",
                        align_items="center"
                    ),
                    rx.hstack(
                        rx.text("Total BS:", weight="bold", size="4"),
                        rx.spacer(),
                        rx.text(f"Bs {AppState.total_bs_intervencion:,.0f}", weight="bold", size="5", color="green.600"),
                        width="100%",
                        align_items="center"
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.box()
            ),
            
            spacing="2",
            width="100%"
        ),
        style=COST_SUMMARY_STYLE
    )

def costo_servicio_item(servicio_detalle: dict) -> rx.Component:
    """💰 Item de costo por servicio"""
    return rx.hstack(
        rx.text(servicio_detalle['nombre'], size="2", flex="1"),
        rx.text(f"x{servicio_detalle['cantidad']}", size="2", color="gray.600"),
        rx.vstack(
            rx.text(f"${servicio_detalle['total_usd']:.2f}", size="2", color="green.600"),
            rx.text(f"Bs {servicio_detalle['total_bs']:,.0f}", size="1", color="green.500"),
            align_items="end",
            spacing="0"
        ),
        spacing="2",
        align_items="center",
        width="100%",
        padding_y="2"
    )

# ==========================================
# 📝 OBSERVACIONES Y NOTAS
# ==========================================

def seccion_observaciones() -> rx.Component:
    """📝 Sección para observaciones y notas médicas"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.icon("file_text", size=20, color="purple.600"),
                rx.text("Observaciones Médicas", weight="bold", size="4", color="purple.700"),
                spacing="2",
                align_items="center",
                width="100%",
                margin_bottom="3"
            ),
            
            # Diagnóstico previo
            rx.vstack(
                rx.text("🔍 Diagnóstico Previo:", weight="medium", size="3"),
                rx.text_area(
                    placeholder="Describe el estado inicial del paciente...",
                    rows="3",
                    width="100%"
                ),
                align_items="start",
                width="100%",
                margin_bottom="3"
            ),
            
            # Procedimiento realizado
            rx.vstack(
                rx.text("🛠️ Procedimiento Realizado:", weight="medium", size="3"),
                rx.text_area(
                    placeholder="Detalla exactamente que procedimientos se realizaron, materiales usados, tecnicas aplicadas...",
                    value=AppState.procedimiento_realizado,
                    on_change=AppState.actualizar_procedimiento_realizado,
                    rows="4",
                    width="100%"
                ),
                align_items="start",
                width="100%",
                margin_bottom="3"
            ),
            
            # Observaciones post-tratamiento
            rx.vstack(
                rx.text("📋 Observaciones Post-Tratamiento:", weight="medium", size="3"),
                rx.text_area(
                    placeholder="Reacciones del paciente, complicaciones, resultados inmediatos...",
                    value=AppState.observaciones_post_tratamiento,
                    on_change=AppState.actualizar_observaciones_post,
                    rows="3",
                    width="100%"
                ),
                align_items="start",
                width="100%",
                margin_bottom="3"
            ),
            
            # Recomendaciones
            rx.vstack(
                rx.text("💡 Recomendaciones para el Paciente:", weight="medium", size="3"),
                rx.text_area(
                    placeholder="Cuidados post-operatorios, medicamentos, proxima cita...",
                    value=AppState.recomendaciones_paciente,
                    on_change=AppState.actualizar_recomendaciones_paciente,
                    rows="3",
                    width="100%"
                ),
                align_items="start",
                width="100%"
            ),
            
            spacing="2",
            width="100%"
        ),
        style=SECTION_STYLE
    )

# ==========================================
# 🎯 BOTONES DE ACCIÓN FINAL
# ==========================================

def botones_accion_intervencion() -> rx.Component:
    """🎯 Botones principales para guardar la intervención"""
    return rx.box(
        rx.vstack(
            # Botón principal: Guardar Intervención
            rx.button(
                rx.icon("save", size=18),
                "Guardar Intervención Completa",
                color_scheme="green",
                size="4",
                width="100%",
                on_click=AppState.guardar_intervencion_completa,
                disabled=AppState.is_guardando_intervencion
            ),
            
            # Botones secundarios
            rx.hstack(
                rx.button(
                    rx.icon("bookmark", size=16),
                    "Guardar Borrador",
                    variant="outline",
                    color_scheme="blue",
                    size="3",
                    flex="1",
                    on_click=AppState.guardar_borrador_intervencion
                ),
                rx.button(
                    rx.icon("eye", size=16),
                    "Vista Previa",
                    variant="outline",
                    color_scheme="purple",
                    size="3",
                    flex="1",
                    on_click=AppState.mostrar_vista_previa
                ),
                spacing="2",
                width="100%"
            ),
            
            # Estado del guardado
            rx.cond(
                AppState.is_guardando_intervencion,
                rx.hstack(
                    rx.spinner(size="3"),
                    rx.text("Guardando intervención...", size="3"),
                    spacing="2",
                    align_items="center",
                    justify="center",
                    width="100%",
                    margin_top="2"
                ),
                rx.box()
            ),
            
            spacing="3",
            width="100%"
        ),
        style={
            **SECTION_STYLE,
            "border_color": COLORS['success']['300'],
            "background": f"linear-gradient(135deg, {COLORS['success']['25']} 0%, {COLORS['gray']['25']} 100%)"
        }
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL INTEGRADO
# ==========================================

def formulario_intervencion_integrado() -> rx.Component:
    """
    🦷 FORMULARIO DE INTERVENCIÓN INTEGRADO V3.0
    
    ✅ CARACTERÍSTICAS PRINCIPALES:
    - Sincronización completa con odontograma SVG
    - Selección visual de dientes
    - Catálogo de servicios odontológicos
    - Cálculo automático de costos BS/USD
    - Observaciones médicas detalladas
    - Guardado completo en base de datos
    
    🎯 FLUJO DE TRABAJO:
    1. Odontólogo selecciona dientes en el odontograma
    2. Elige procedimientos del catálogo
    3. Sistema calcula costos automáticamente
    4. Registra observaciones médicas
    5. Guarda intervención completa
    
    🔄 INTEGRACIÓN:
    - Conectado con AppState
    - Sincronizado con servicios de Supabase
    - Compatible con el sistema de versiones
    - Actualiza odontograma automáticamente
    """
    
    return rx.box(
        rx.vstack(
            # Header del formulario
            rx.hstack(
                rx.icon("clipboard_plus", size=24, color="primary.600"),
                rx.vstack(
                    rx.text("Registro de Intervencion", weight="bold", size="5"),
                    rx.text("Complete los datos de la atencion odontologica", size="3", color="gray.600"),
                    align_items="start",
                    spacing="0"
                ),
                rx.spacer(),
                rx.badge(
                    rx.cond(
                        AppState.paciente_actual.nombre_completo,
                        f"Paciente: {AppState.paciente_actual.nombre_completo}",
                        "Sin paciente seleccionado"
                    ),
                    color_scheme="blue",
                    size="2"
                ),
                spacing="3",
                align_items="center",
                width="100%",
                margin_bottom="4"
            ),
            
            # Secciones del formulario
            selector_dientes_integrado(),
            selector_servicios(),
            resumen_costos(),
            seccion_observaciones(),
            botones_accion_intervencion(),
            
            spacing="3",
            width="100%"
        ),
        style=FORM_CONTAINER_STYLE
    )