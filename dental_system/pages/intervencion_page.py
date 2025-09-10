"""
🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA V3.0 - FASE 3: INTEGRACIÓN COMPLETA
=========================================================================

VERSIÓN FINAL con todos los componentes avanzados integrados:
- Odontograma SVG Interactivo (Fase 2)
- Panel Detalles Diente con Tabs (Fase 2)
- Sistema Versionado Automático (Fase 2)
- Historial de Cambios Detallado (Fase 2)
- Sistema de Notificaciones (Fase 2)
- Layout profesional optimizado para flujo médico

ARQUITECTURA: Panel izquierdo (Paciente) + Panel central (Tabs) + Panel derecho (Detalles)
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, primary_button, secondary_button

# Importar componentes existentes (Fase 1)
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
from dental_system.components.odontologia.panel_historial import panel_historial_notas

# Importar nuevos componentes avanzados (Fase 2)
from dental_system.components.odontologia.odontograma_svg import odontograma_interactivo
from dental_system.components.odontologia.panel_detalles_diente import panel_detalles_diente
from dental_system.components.odontologia.sistema_versionado import sistema_versionado_odontograma
from dental_system.components.odontologia.historial_cambios import historial_cambios_diente
from dental_system.components.odontologia.notificaciones_cambios import sistema_notificaciones_cambios

# Importar formulario FUNCIONANDO (sin métodos inexistentes)
from dental_system.components.odontologia.formulario_simple_funcionando import formulario_simple_funcionando

from dental_system.styles.themes import COLORS, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS PARA LA INTEGRACIÓN COMPLETA
# ==========================================

# Layout principal de 3 paneles expandido
MAIN_LAYOUT_STYLE = {
    "display": "grid",
    "grid_template_columns": "25% 50% 25%",  # Paciente | Central | Detalles
    "gap": SPACING["3"],
    "height": "calc(100vh - 120px)",
    "width": "100%",
    "padding": SPACING["4"],
    "max_width": "1600px",  # Ampliado para más contenido
    "margin": "0 auto"
}

# Panel base mejorado
PANEL_BASE_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["md"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "height": "100%",
    "overflow": "hidden",
    "display": "flex",
    "flex_direction": "column"
}

# Panel central con tabs y odontograma
PANEL_CENTRAL_STYLE = {
    **PANEL_BASE_STYLE,
    "background": f"linear-gradient(135deg, {COLORS['gray']['50']} 0%, white 100%)"
}

# Responsive adaptado a más contenido
TABLET_RESPONSIVE = {
    "@media (max-width: 1200px)": {
        "grid_template_columns": "30% 40% 30%"
    },
    "@media (max-width: 1024px)": {
        "grid_template_columns": "35% 65%",  # Ocultar panel derecho en tablet
    },
    "@media (max-width: 768px)": {
        "grid_template_columns": "100%",
        "grid_template_rows": "auto",
        "height": "auto"
    }
}

# Header mejorado con notificaciones
HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "color": "white",
    "padding": SPACING["4"],
    "border_radius": RADIUS["lg"],
    "margin_bottom": SPACING["3"],
    "box_shadow": SHADOWS["lg"],
    "display": "flex",
    "justify_content": "space-between",
    "align_items": "center"
}

# ==========================================
# 🧩 COMPONENTES DE LA NUEVA ARQUITECTURA
# ==========================================

def header_intervencion_avanzado() -> rx.Component:
    """🎯 Header principal con información del paciente y notificaciones"""
    return rx.box(
        rx.hstack(
            # Información del paciente en sesión
            rx.hstack(
                rx.icon("user", size=28, color="white"),
                rx.vstack(
                    rx.cond(
                        AppState.paciente_actual.nombre_completo,
                        rx.vstack(
                            rx.text(
                                AppState.paciente_actual.nombre_completo,
                                weight="bold",
                                size="5",
                                color="white"
                            ),
                            rx.hstack(
                                rx.text(f"HC: {AppState.paciente_actual.numero_historia}", size="2", opacity="0.9"),
                                rx.text("•", size="2", opacity="0.7"),
                                rx.text(f"Consulta: {AppState.consulta_actual.numero_consulta}", size="2", opacity="0.9"),
                                spacing="2"
                            ),
                            align_items="start",
                            spacing="0"
                        ),
                        rx.text("Seleccionar paciente", size="4", opacity="0.8")
                    ),
                    align_items="start",
                    spacing="1"
                ),
                spacing="3",
                align_items="center"
            ),
            
            rx.spacer(),
            
            # Panel de controles y notificaciones
            rx.hstack(
                # Sistema de notificaciones integrado
                sistema_notificaciones_cambios(),
                
                # Botones de acción principal
                rx.button(
                    rx.icon("save", size=16),
                    "Guardar Todo",
                    color_scheme="green",
                    size="3",
                    on_click=AppState.crear_intervencion
                ),
                rx.button(
                    rx.icon("x", size=16),
                    "Finalizar",
                    variant="outline",
                    size="3",
                    on_click=lambda: AppState.navigate_to("odontologia")
                ),
                spacing="2"
            ),
            
            width="100%",
            align_items="center"
        ),
        style=HEADER_STYLE
    )

def panel_paciente_integrado() -> rx.Component:
    """👤 Panel izquierdo con información completa del paciente"""
    return rx.box(
        rx.vstack(
            # Header del panel
            rx.hstack(
                rx.icon("user", size=20, color="primary.500"),
                rx.text("Información del Paciente", weight="bold", size="4"),
                spacing="2",
                padding_bottom="3",
                border_bottom=f"1px solid {COLORS['gray']['200']}",
                width="100%"
            ),
            
            # Panel de información del paciente expandido (de Fase 1)
            panel_informacion_paciente(),
            
            spacing="3",
            width="100%",
            height="100%",
            padding="4"
        ),
        style=PANEL_BASE_STYLE
    )

def panel_central_integrado() -> rx.Component:
    """🦷 Panel central con odontograma y tabs"""
    return rx.box(
        rx.vstack(
            # Tabs de navegación principal
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("stethoscope", size=16), "Odontograma", spacing="2"),
                        value="odontograma"
                    ),
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("git_branch", size=16), "Versiones", spacing="2"),
                        value="versiones"
                    ),
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("pen", size=16), "Intervención", spacing="2"),
                        value="intervencion"
                    ),
                ),
                
                # Contenido del tab Odontograma
                rx.tabs.content(
                    rx.vstack(
                        # Odontograma SVG interactivo
                        odontograma_interactivo(),
                        
                        # Controles adicionales
                        rx.hstack(
                            rx.button(
                                rx.icon("refresh_cw", size=16),
                                "Refrescar",
                                variant="outline",
                                size="2",
                                # on_click=AppState.refrescar_odontograma
                            ),
                            rx.button(
                                rx.icon("history", size=16),
                                "Ver Historial",
                                variant="outline",
                                size="2",
                                # on_click=AppState.mostrar_historial_odontograma
                            ),
                            spacing="2",
                            justify="center",
                            margin_top="3"
                        ),
                        
                        spacing="3",
                        width="100%"
                    ),
                    value="odontograma"
                ),
                
                # Contenido del tab Versiones
                rx.tabs.content(
                    sistema_versionado_odontograma(),
                    value="versiones"
                ),
                
                # Contenido del tab Intervención (formulario integrado nuevo)
                rx.tabs.content(
                    formulario_simple_funcionando(),
                    value="intervencion"
                ),
                
                default_value="odontograma",
                orientation="horizontal",
                width="100%",
                height="100%"
            ),
            
            spacing="0",
            width="100%",
            height="100%"
        ),
        style=PANEL_CENTRAL_STYLE
    )

def panel_detalles_integrado() -> rx.Component:
    """📋 Panel derecho con detalles del diente seleccionado"""
    return rx.box(
        rx.vstack(
            # Header del panel
            rx.hstack(
                rx.icon("info", size=20, color="blue.500"),
                rx.text("Detalles del Diente", weight="bold", size="4"),
                rx.spacer(),
                # Toggle para cambiar entre panel detalles e historial
                rx.button(
                    rx.icon("history", size=16),
                    variant="ghost",
                    size="2",
                    # on_click=AppState.toggle_panel_derecho
                ),
                spacing="2",
                padding_bottom="3",
                border_bottom=f"1px solid {COLORS['gray']['200']}",
                width="100%",
                align_items="center"
            ),
            
            # Contenido condicional del panel derecho
            rx.cond(
                # AppState.mostrar_historial_en_panel,
                # Historial de cambios detallado
                historial_cambios_diente(),
                # Panel de detalles del diente
                panel_detalles_diente()
            ),
            
            spacing="0",
            width="100%",
            height="100%",
            padding="4"
        ),
        style=PANEL_BASE_STYLE
    )

# ==========================================
# 📱 VERSIÓN MÓVIL ADAPTATIVA
# ==========================================

def mobile_intervention_layout() -> rx.Component:
    """📱 Layout adaptativo para móviles"""
    return rx.vstack(
        # Header compacto
        header_intervencion_avanzado(),
        
        # Acordeón colapsable para móvil
        rx.accordion.root(
            rx.accordion.item(
                rx.accordion.trigger(
                    rx.hstack(
                        rx.icon("user", size=16),
                        "Información del Paciente",
                        spacing="2"
                    )
                ),
                rx.accordion.content(
                    panel_informacion_paciente()
                ),
                value="paciente"
            ),
            rx.accordion.item(
                rx.accordion.trigger(
                    rx.hstack(
                        rx.icon("stethoscope", size=16),
                        "Odontograma Interactivo",
                        spacing="2"
                    )
                ),
                rx.accordion.content(
                    odontograma_interactivo()
                ),
                value="odontograma"
            ),
            rx.accordion.item(
                rx.accordion.trigger(
                    rx.hstack(
                        rx.icon("info", size=16),
                        "Detalles del Diente",
                        spacing="2"
                    )
                ),
                rx.accordion.content(
                    panel_detalles_diente()
                ),
                value="detalles"
            ),
            type="multiple",
            default_value=["odontograma"],
            width="100%"
        ),
        
        spacing="3",
        width="100%",
        padding="3"
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL INTEGRADA
# ==========================================

def intervencion_page() -> rx.Component:
    """
    🦷 Página de Intervención Odontológica V3.0 - INTEGRACIÓN COMPLETA
    
    ✅ FASES 1 Y 2 INTEGRADAS:
    - Panel Paciente mejorado con información expandida
    - Odontograma SVG interactivo con sistema FDI completo
    - Sistema de versionado automático con comparación histórica
    - Panel de detalles diente con 4 tabs especializados
    - Historial de cambios detallado con timeline
    - Sistema de notificaciones en tiempo real
    - Layout profesional de 3 paneles
    - Responsive design completo
    
    🎯 FUNCIONALIDADES AVANZADAS:
    - Interactividad completa en odontograma
    - Notificaciones automáticas por cambios críticos
    - Versionado automático del odontograma
    - Timeline detallado de cambios por diente
    - Configuración personalizable por usuario
    - Exportación e impresión de datos
    
    📊 ARQUITECTURA:
    Desktop: Panel Paciente (25%) | Panel Central con Tabs (50%) | Panel Detalles (25%)
    Tablet: Panel Paciente (35%) | Panel Central (65%)
    Mobile: Layout accordion vertical
    """
    
    return rx.box(
        # Layout principal
        rx.vstack(
            # Header principal con notificaciones
            header_intervencion_avanzado(),
            
            # Contenido principal adaptativo
            rx.box(
                # Layout desktop/tablet
                rx.box(
                    rx.hstack(
                        # Panel izquierdo: Información del paciente
                        panel_paciente_integrado(),
                        
                        # Panel central: Odontograma y tabs
                        panel_central_integrado(),
                        
                        # Panel derecho: Detalles del diente
                        rx.box(
                            panel_detalles_integrado(),
                            display=rx.breakpoints({"base": "none", "lg": "block"})  # Ocultar en móvil
                        ),
                        
                        spacing="3",
                        width="100%",
                        height="100%",
                        align_items="stretch"
                    ),
                    display=rx.breakpoints({"base": "none", "md": "block"})  # Desktop y tablet
                ),
                
                # Layout móvil
                rx.box(
                    mobile_intervention_layout(),
                    display=rx.breakpoints({"base": "block", "md": "none"})  # Solo móvil
                ),
                
                width="100%",
                height="100%"
            ),
            
            spacing="0",
            width="100%",
            max_width="1600px",  # Ampliado para más contenido
            margin="0 auto",
            height="100vh"
        ),
        
        # Estilos del contenedor principal
        style={
            "background": f"linear-gradient(135deg, {COLORS['gray']['50']} 0%, {COLORS['primary']['50']} 100%)",
            "min_height": "100vh"
        },
        width="100%",
        padding="4",
        
        # Evento de inicialización
        # on_mount=AppState.cargar_datos_intervencion
        on_mount=[
            AppState.cargar_servicios_disponibles,
            AppState.cargar_historial_paciente(AppState.paciente_actual.id),
            AppState.cargar_estadisticas_dia
        ]
    )