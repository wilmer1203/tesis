# 🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA - ARQUITECTURA DE 3 PANELES
# dental_system/pages/intervencion_page_v2.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, primary_button, secondary_button
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
from dental_system.components.odontologia.panel_historial import panel_historial_notas
from dental_system.components.odontologia.intervention_tabs_v2 import intervention_tabs_integrated
from dental_system.styles.themes import COLORS, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS PARA LA NUEVA ARQUITECTURA
# ==========================================

# Layout principal de 3 paneles
MAIN_LAYOUT_STYLE = {
    "display": "grid",
    "grid_template_columns": "30% 50% 20%",  # Panel paciente | Panel central | Panel historial
    "gap": SPACING["4"],
    "height": "calc(100vh - 140px)",  # Altura total menos header
    "width": "100%",
    "padding": "0"
}

# Estilos para cada panel
PANEL_BASE_STYLE = {
    "height": "100%",
    "overflow": "hidden",
    "position": "relative"
}

PANEL_CENTRAL_STYLE = {
    **PANEL_BASE_STYLE,
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": SHADOWS["lg"],
    "border": f"1px solid {COLORS['gray']['200']}"
}

# Header de navegación para la página
PAGE_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['600']} 100%)",
    "color": "white",
    "padding": SPACING["4"],
    "border_radius": RADIUS["lg"],
    "margin_bottom": SPACING["4"],
    "box_shadow": SHADOWS["lg"]
}

# Botones de acción en el header
ACTION_BUTTONS_STYLE = {
    "position": "fixed",
    "top": SPACING["4"],
    "right": SPACING["4"],
    "z_index": "999",
    "display": "flex",
    "gap": SPACING["2"]
}

# Responsive para tablets
TABLET_RESPONSIVE = {
    "@media (max-width: 1024px)": {
        "grid_template_columns": "35% 45% 20%"  # Más espacio para paciente en tablet
    },
    "@media (max-width: 768px)": {
        "grid_template_columns": "100%",  # Stack vertical en móvil
        "grid_template_rows": "auto auto auto",
        "height": "auto"
    }
}

# ==========================================
# 🧩 COMPONENTES DE LA NUEVA ARQUITECTURA
# ==========================================

def header_intervencion() -> rx.Component:
    """🦷 Header principal de la página de intervención"""
    return rx.box(
        rx.hstack(
            # Información de navegación
            rx.hstack(
                rx.button(
                    "← Volver al Dashboard",
                    size="2",
                    variant="ghost",
                    color="white",
                    on_click=lambda: AppState.navigate_to("odontologia")
                ),
                rx.text("|", color="rgba(255, 255, 255, 0.5)"),
                rx.text(
                    "🦷 Intervención Odontológica",
                    font_size="20px",
                    font_weight="bold",
                    color="white"
                ),
                spacing="3",
                align_items="center"
            ),
            
            rx.spacer(),
            
            # Información de la sesión
            rx.hstack(
                rx.text(
                    AppState.texto_estado_consulta_actual,
                    font_size="14px",
                    color="rgba(255, 255, 255, 0.8)"
                ),
                rx.text("|", color="rgba(255, 255, 255, 0.5)"),
                rx.text(
                    "Sesión iniciada",
                    font_size="14px",
                    color="rgba(255, 255, 255, 0.8)"
                ),
                spacing="2",
                align_items="center"
            ),
            
            spacing="4",
            align_items="center",
            width="100%"
        ),
        style=PAGE_HEADER_STYLE
    )

def botones_accion_principales() -> rx.Component:
    """⚡ Botones de acción principales en el header"""
    return rx.box(
        rx.hstack(
            # Guardar borrador
            rx.button(
                "💾 Guardar",
                size="2",
                variant="outline",
                color="white",
                border_color="rgba(255, 255, 255, 0.3)",
                on_click=lambda: AppState.navigate_to("dashboard"),  # Placeholder - guardar_borrador_intervencion
                _hover={
                    "background": "rgba(255, 255, 255, 0.1)",
                    "border_color": "rgba(255, 255, 255, 0.5)"
                }
            ),
            
            # Cancelar
            rx.button(
                "❌ Cancelar",
                size="2",
                variant="outline",
                color_scheme="red",
                on_click=lambda: AppState.navigate_to("odontologia")
            ),
            
            # Finalizar (principal)
            rx.button(
                rx.hstack(
                    rx.text("✅", font_size="16px"),
                    rx.text("Finalizar Intervención", color="white"),
                    spacing="2"
                ),
                size="2",
                color_scheme="green",
                loading=False,  # AppState.creando_intervencion
                disabled=False,  # AppState.formulario_intervencion_valido
                on_click=lambda: AppState.navigate_to("dashboard")  # Placeholder - crear_intervencion
            ),
            
            spacing="2"
        ),
        style=ACTION_BUTTONS_STYLE
    )

def panel_central_intervencion() -> rx.Component:
    """🦷 Panel central con odontograma y formulario"""
    return rx.box(
        rx.vstack(
            # Header del panel central
            rx.hstack(
                rx.text(
                    "🦷 Odontograma y Tratamiento",
                    font_size="18px",
                    font_weight="bold",
                    color=COLORS["gray"]["800"]
                ),
                rx.spacer(),
                rx.badge(
                    f"Dientes: {AppState.resumen_dientes_seleccionados}",
                    color_scheme="blue",
                    size="2"
                ),
                spacing="3",
                align_items="center",
                width="100%",
                padding=SPACING["6"],
                border_bottom=f"1px solid {COLORS['gray']['200']}"
            ),
            
            # Contenido principal del panel central (Tabs existentes)
            rx.box(
                intervention_tabs_integrated(),
                flex="1",
                overflow="hidden",
                padding=SPACING["6"]
            ),
            
            spacing="0",
            height="100%"
        ),
        style=PANEL_CENTRAL_STYLE
    )

def validation_alert() -> rx.Component:
    """⚠️ Alerta de validación si faltan datos"""
    return rx.cond(
        AppState.errores_validacion_intervencion.length() > 0,
        rx.box(
            rx.hstack(
                rx.text("⚠️", font_size="20px", color=COLORS["warning"]["500"]),
                rx.vstack(
                    rx.text(
                        "Datos incompletos",
                        font_weight="bold",
                        color=COLORS["warning"]["700"]
                    ),
                    rx.text(
                        "Complete los campos requeridos para continuar",
                        font_size="14px",
                        color=COLORS["warning"]["600"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                spacing="3",
                align_items="center"
            ),
            background=COLORS["warning"]["50"],
            border=f"1px solid {COLORS['warning']['200']}",
            border_radius=RADIUS["lg"],
            padding=SPACING["4"],
            margin_bottom=SPACING["4"]
        )
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL DE INTERVENCIÓN - REDISEÑADA
# ==========================================

def intervencion_page_v2() -> rx.Component:
    """
    🦷 Página de intervención odontológica - ARQUITECTURA DE 3 PANELES
    
    ✅ NUEVA ARQUITECTURA IMPLEMENTADA:
    - Layout de 3 paneles: Paciente (30%) | Central (50%) | Historial (20%)
    - Panel izquierdo: Información completa del paciente + datos médicos
    - Panel central: Odontograma interactivo + Formulario de intervención
    - Panel derecho: Timeline de historial + Notas clínicas
    - Navigation header con breadcrumbs y acciones
    - Responsive design adaptable a tablets/desktop
    - Componentes reutilizables y tipados
    - UX optimizada para flujo médico profesional
    
    🎯 MEJORAS CLAVE:
    - Información contextual siempre visible
    - Navegación intuitiva entre paneles
    - Espacio optimizado para odontograma
    - Historial accesible sin interrumpir flujo
    - Validaciones en tiempo real
    - Estados visuales claros
    
    📊 MÉTRICAS OBJETIVO:
    - Tiempo de intervención: < 4 minutos
    - Eficiencia de navegación: +40%
    - Reducción de errores: 60%
    - Satisfacción de usuario: >95%
    """
    return rx.vstack(
        # Header superior con navegación y acciones
        rx.box(
            rx.hstack(
                header_intervencion(),
                botones_accion_principales(),
                spacing="0",
                justify="between",
                width="100%",
                position="relative"
            ),
            width="100%"
        ),
        
        # Alerta de validación si es necesaria
        validation_alert(),
        
        # Layout principal de 3 paneles
        rx.box(
            rx.hstack(
                # ==========================================
                # PANEL IZQUIERDO: INFORMACIÓN DEL PACIENTE (30%)
                # ==========================================
                rx.box(
                    panel_informacion_paciente(),
                    style={**PANEL_BASE_STYLE, "width": "30%"}
                ),
                
                # ==========================================
                # PANEL CENTRAL: ODONTOGRAMA + FORMULARIO (50%)
                # ==========================================
                rx.box(
                    panel_central_intervencion(),
                    style={**PANEL_BASE_STYLE, "width": "50%"}
                ),
                
                # ==========================================
                # PANEL DERECHO: HISTORIAL + NOTAS (20%)
                # ==========================================
                rx.box(
                    panel_historial_notas(),
                    style={**PANEL_BASE_STYLE, "width": "20%"}
                ),
                
                spacing="4",
                align_items="start",
                width="100%",
                height="100%"
            ),
            style={
                **MAIN_LAYOUT_STYLE,
                **TABLET_RESPONSIVE
            }
        ),
        
        # Footer con información de sesión
        rx.box(
            rx.hstack(
                rx.text(
                    rx.cond(
                        AppState.paciente_actual.nombre_completo,
                        f"Sesión iniciada: {AppState.paciente_actual.nombre_completo}",
                        "Sesión iniciada: Sin paciente"
                    ),
                    font_size="12px",
                    color=COLORS["gray"]["500"]
                ),
                rx.spacer(),
                rx.text(
                    "Sistema de Gestión Odontológica - Intervención Activa",
                    font_size="12px",
                    color=COLORS["gray"]["500"]
                ),
                spacing="4",
                align_items="center",
                width="100%"
            ),
            background=COLORS["gray"]["50"],
            border_top=f"1px solid {COLORS['gray']['200']}",
            padding=SPACING["2"],
            width="100%"
        ),
        
        spacing="0",
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["25"],
        padding=SPACING["6"],
        
        # Eventos de inicialización
        on_mount=[
            AppState.cargar_servicios_disponibles,
            AppState.cargar_historial_paciente(AppState.paciente_actual.id),
            AppState.cargar_estadisticas_dia
        ]
    )