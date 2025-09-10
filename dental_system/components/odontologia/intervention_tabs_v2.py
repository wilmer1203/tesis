# 🦷 COMPONENTE: TABS INTEGRADO CON CONTENIDO ESPECÍFICO - VERSION SIMPLIFICADA
# dental_system/components/odontologia/intervention_tabs_v2.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS, dark_crystal_card
from dental_system.components.odontologia.odontogram_grid import (
    odontogram_interactive_grid, odontogram_toolbar, odontogram_toolbar_professional
)
from dental_system.components.odontologia.condition_selector_modal import (
    condition_selector_modal, odontogram_legend
)
from dental_system.components.odontologia.interactive_tooth import selected_tooth_info_panel
from dental_system.components.odontologia.tooth_popover import tooth_popover
from dental_system.components.odontologia.floating_history_button import floating_history_button

# ==========================================
# 🎨 ESTILOS PARA TABS INTEGRADO
# ==========================================

ODONTOLOGO_COLORS = {
    "primary": COLORS["success"]["500"],        # Verde profesional
    "secondary": COLORS["primary"]["500"],      # Turquesa dental
    "accent": COLORS["primary"]["400"],         # Acento turquesa claro
    "surface": "rgba(255, 255, 255, 0.08)",   # Glassmorphism
    "border": "rgba(255, 255, 255, 0.2)"      # Bordes cristal
}

TAB_CONFIG = {
    "odontograma": {"title": "🦷 Odontograma", "icon": "clipboard-list", "color": ODONTOLOGO_COLORS["primary"]},
    "intervencion": {"title": "⚕️ Intervención", "icon": "activity", "color": COLORS["warning"]["500"]},
    "finalizar": {"title": "💾 Finalizar", "icon": "check", "color": ODONTOLOGO_COLORS["accent"]}
}

# ==========================================
# 🎯 TAB INDIVIDUAL SIMPLIFICADO
# ==========================================

def tab_button_simple(tab_id: str) -> rx.Component:
    """🎯 Botón de tab simplificado con condiciones reactivas"""
    config = TAB_CONFIG[tab_id]
    
    return rx.button(
        rx.hstack(
            rx.icon(tag=config["icon"], size=18),
            rx.text(config["title"], weight="medium"),
            spacing="2",
            align_items="center"
        ),
        
        on_click=AppState.set_active_intervention_tab(tab_id),
        
        style=rx.cond(
            AppState.active_intervention_tab == tab_id,
            # Estilo activo
            {
                "background": f"linear-gradient(135deg, {config['color']}40 0%, {config['color']}20 100%)",
                "border": f"1px solid {config['color']}60",
                "color": "white",
                "border_radius": RADIUS["xl"],
                "padding": f"{SPACING['2']} {SPACING['4']}",
                "transition": "all 0.3s ease",
                "box_shadow": f"0 4px 12px {config['color']}30"
            },
            # Estilo inactivo
            {
                "background": "rgba(255, 255, 255, 0.03)",
                "border": "1px solid transparent",
                "color": DARK_THEME["colors"]["text_secondary"],
                "border_radius": RADIUS["xl"],
                "padding": f"{SPACING['2']} {SPACING['4']}",
                "transition": "all 0.3s ease",
                "_hover": {
                    "background": f"linear-gradient(135deg, {config['color']}30 0%, {config['color']}15 100%)",
                    "color": DARK_THEME["colors"]["text_primary"]
                }
            }
        )
    )

# ==========================================
# 🧭 NAVEGACIÓN SIMPLIFICADA
# ==========================================

def tabs_navigation() -> rx.Component:
    """🧭 Navegación de tabs horizontal"""
    return rx.hstack(
        *[
            tab_button_simple(tab_id)
            for tab_id in TAB_CONFIG.keys()
        ],
        spacing="2",
        width="100%",
        justify_content="center",
        padding="4",
        style={
            "background": "rgba(255, 255, 255, 0.06)",
            "backdrop_filter": "blur(20px)",
            "border_radius": RADIUS["2xl"],
            "border": f"1px solid {ODONTOLOGO_COLORS['border']}"
        }
    )

# ==========================================
# 📋 CONTENIDO DE TABS ESPECÍFICOS
# ==========================================

# Función eliminada - la información del paciente ahora se muestra en el panel izquierdo

def tab_content_odontograma() -> rx.Component:
    """🦷 Contenido del tab del odontograma - VERSIÓN INTERACTIVA FASE 2"""
    return rx.vstack(
        # Header mejorado con indicadores
        rx.hstack(
            rx.icon(tag="clipboard-list", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.vstack(
                rx.text("🦷 Odontograma Digital Interactivo", size="6", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
                rx.text("Click en cualquier superficie para modificar condiciones", size="3", color=DARK_THEME["colors"]["text_secondary"]),
                spacing="1", align_items="start"
            ),
            rx.spacer(),
            
            # Indicador de estado del odontograma
            rx.cond(
                AppState.cargando_odontograma,
                rx.badge("🔄 Cargando...", color_scheme="blue", variant="soft"),
                rx.cond(
                    AppState.cambios_pendientes_odontograma.length() > 0,
                    rx.badge("⚠️ Cambios sin guardar", color_scheme="orange", variant="soft"),
                    rx.badge("✅ Sincronizado", color_scheme="green", variant="soft")
                )
            ),
            
            spacing="3", align_items="start", width="100%"
        ),
        
        # Toolbar profesional optimizado
        odontogram_toolbar_professional(),
        
        # Contenedor principal del odontograma
        rx.box(
            rx.cond(
                AppState.cargando_odontograma,
                
                # Estado de carga
                rx.vstack(
                    rx.spinner(size="3", color=ODONTOLOGO_COLORS["primary"]),
                    rx.text("Cargando odontograma del paciente...", size="4", color=DARK_THEME["colors"]["text_secondary"]),
                    spacing="4", align_items="center", height="400px", justify_content="center"
                ),
                
                # Odontograma interactivo completo
                odontogram_interactive_grid()
            ),
            
            style={
                "background": "rgba(255, 255, 255, 0.03)",
                "backdrop_filter": "blur(20px) saturate(150%)",
                "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
                "border_radius": RADIUS["2xl"],
                "padding": SPACING["6"],
                "min_height": "500px"
            },
            width="100%"
        ),
        
        # Panel inferior con información y leyenda
        rx.hstack(
            # Leyenda de condiciones (lado izquierdo)
            odontogram_legend(),
            
            rx.spacer(),
            
            # Panel de información del diente seleccionado (lado derecho)
            rx.cond(
                AppState.diente_seleccionado,
                selected_tooth_info_panel(),
                rx.box(
                    rx.vstack(
                        rx.icon(tag="info", size=24, color=DARK_THEME["colors"]["text_muted"]),
                        rx.text("Selecciona un diente para ver información detallada", 
                               size="3", color=DARK_THEME["colors"]["text_muted"], text_align="center"),
                        rx.text("Click en cualquier superficie para cambiar condiciones",
                               size="2", color=DARK_THEME["colors"]["text_muted"], text_align="center"),
                        spacing="2", align_items="center"
                    ),
                    style={
                        "background": DARK_THEME["colors"]["surface_secondary"],
                        "border": f"1px solid {DARK_THEME['colors']['primary']}",
                        "border_radius": RADIUS["lg"],
                        "padding": SPACING["6"],
                        "min_width": "250px",
                        "min_height": "120px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                )
            ),
            
            spacing="6", width="100%", align_items="start"
        ),
        
        # Modal selector de condiciones
        condition_selector_modal(),
        
        # 🎈 Popover contextual del diente (flotante)
        tooth_popover(),
        
        # 📚 Botón historial flotante
        floating_history_button(),
        
        spacing="6", width="100%", align_items="start",
        
        # Event handler para inicializar el odontograma cuando se carga el tab
        on_mount=AppState.cargar_odontograma_paciente("")
    )

def panel_contexto_paciente() -> rx.Component:
    """👤 Panel de contexto del paciente - MEJORA CRÍTICA"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.avatar(size="3", fallback="P"),
                rx.vstack(
                    rx.text(AppState.paciente_actual.nombre_completo, size="4", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
                    rx.hstack(
                        rx.text(f"HC: {AppState.paciente_actual.numero_historia}", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                        rx.text("•", size="2", color=DARK_THEME["colors"]["text_muted"]),
                        rx.text(f"Edad: {AppState.paciente_actual.edad_display}", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                        spacing="2"
                    ),
                    spacing="1", align_items="start"
                ),
                spacing="3", align_items="center"
            ),
            
            # Alerta de alergias si las hay
            rx.cond(
                AppState.alergias_conocidas.length() > 0,
                rx.callout(
                    rx.hstack(
                        rx.icon(tag="triangle-alert", size=16),
                        rx.text("⚠️ ALERGIAS: " + AppState.alergias_display, size="2", weight="medium"),
                        spacing="2"
                    ),
                    color_scheme="red", size="1", width="100%"
                )
            ),
            
            spacing="3", width="100%"
        ),
        style={
            "background": f"linear-gradient(135deg, {COLORS['info']['500']}20 0%, {COLORS['info']['600']}10 100%)",
            "border": f"1px solid {COLORS['info']['200']}",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "margin_bottom": SPACING["4"]
        }
    )

def panel_validacion_tiempo_real() -> rx.Component:
    """⚠️ Panel de validación en tiempo real - MEJORA CRÍTICA"""
    return rx.cond(
        AppState.errores_validacion_tiempo_real.length() > 0,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon(tag="triangle-alert", size=18, color=COLORS["warning"]["500"]),
                    rx.text("⚠️ Campos requeridos:", size="3", weight="medium", color=COLORS["warning"]["700"]),
                    spacing="2", align_items="center"
                ),
                rx.foreach(
                    AppState.errores_validacion_tiempo_real,
                    lambda error: rx.text(f"• {error}", size="2", color=COLORS["warning"]["600"])
                ),
                spacing="2", width="100%"
            ),
            style={
                "background": COLORS["warning"]["50"],
                "border": f"1px solid {COLORS['warning']['200']}",
                "border_radius": RADIUS["lg"],
                "padding": SPACING["4"],
                "margin_bottom": SPACING["4"]
            }
        )
    )

def selector_anestesia_profesional() -> rx.Component:
    """💉 Selector de anestesia profesional - MEJORA CRÍTICA"""
    return rx.vstack(
        rx.text("Anestesia Utilizada", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
        rx.select.root(
            rx.select.trigger(
                placeholder="Seleccionar tipo de anestesia...",
                style={
                    "background": DARK_THEME["colors"]["surface_secondary"],
                    "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "border_radius": "8px",
                    "padding": "0.75rem",
                    "width": "100%"
                }
            ),
            rx.select.content(
                rx.select.item("Sin anestesia", value="ninguna"),
                rx.select.item("Lidocaína 2% + Epinefrina", value="lidocaina_epi"),
                rx.select.item("Lidocaína 2% simple", value="lidocaina_simple"),
                rx.select.item("Articaína 4% + Epinefrina", value="articaina_epi"),
                rx.select.item("Mepivacaína 3% simple", value="mepivacaina"),
                rx.select.item("Otra (especificar)", value="otra"),
                style={
                    "background": DARK_THEME["colors"]["surface_secondary"],
                    "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
                    "border_radius": "8px"
                }
            ),
            value=rx.cond(AppState.formulario_intervencion.anestesia_utilizada, AppState.formulario_intervencion.anestesia_utilizada, "ninguna"),
            on_change=lambda value: AppState.actualizar_campo_intervencion("anestesia_utilizada", value)
        ),
        spacing="2", width="100%"
    )

def tab_content_intervencion() -> rx.Component:
    """⚕️ Contenido NUEVO con selector de servicios y tabla agregada"""
    from dental_system.components.odontologia.selector_intervenciones_v2 import nuevo_tab_intervencion
    
    return rx.vstack(
        # Header del tab
        rx.hstack(
            rx.icon(tag="activity", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.text("⚕️ Registro de Intervención", size="6", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            spacing="3", align_items="center", margin_bottom="6"
        ),
        
        # Nuevo componente con flujo mejorado
        nuevo_tab_intervencion(),
        
        spacing="6", width="100%", align_items="start"
    )

def tab_content_intervencion_BACKUP() -> rx.Component:
    """⚕️ Contenido del formulario de intervención MEJORADO - BACKUP"""
    return rx.vstack(
        # Contexto del paciente - NUEVO
        panel_contexto_paciente(),
        
        # Panel de validación en tiempo real - NUEVO
        panel_validacion_tiempo_real(),
       
        rx.hstack(
            rx.icon(tag="activity", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.text("⚕️ Registro de Intervención", size="6", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            spacing="3", align_items="center", margin_bottom="6"
        ),
        
        rx.grid(
            # Columna 1: Servicio y procedimiento
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.text("Servicio a Realizar *", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                        rx.cond(
                            AppState.servicios_disponibles.length() > 0,
                            rx.badge(f"{AppState.servicios_disponibles.length()} disponibles", color_scheme="green", variant="soft", size="1"),
                            rx.badge("Cargando servicios...", color_scheme="orange", variant="soft", size="1")
                        ),
                        spacing="2", align_items="center"
                    ),
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Seleccionar servicio...",
                            style={
                                "background": DARK_THEME["colors"]["surface_secondary"], 
                                "border": f"1px solid {ODONTOLOGO_COLORS['border']}", 
                                "color": DARK_THEME["colors"]["text_primary"],
                                "border_radius": "8px",
                                "padding": "0.75rem",
                                "width": "100%",
                                "_focus": {
                                    "border_color": ODONTOLOGO_COLORS["primary"],
                                    "box_shadow": f"0 0 0 3px rgba({ODONTOLOGO_COLORS['primary']}, 0.1)"
                                }
                            }
                        ),
                        rx.select.content(
                            rx.foreach(
                                AppState.servicios_disponibles,
                                lambda servicio: rx.select.item(
                                    rx.hstack(
                                        rx.icon("stethoscope", size=16),
                                        rx.vstack(
                                            rx.text(servicio.nombre, weight="medium"),
                                            rx.text(
                                                f"{servicio.categoria} - ${servicio.precio_base}",
                                                size="1",
                                                color=DARK_THEME["colors"]["text_secondary"]
                                            ),
                                            spacing="1",
                                            align="start"
                                        ),
                                        spacing="2",
                                        align="center"
                                    ),
                                    value=servicio.id
                                )
                            ),
                            style={
                                "background": DARK_THEME["colors"]["surface_secondary"],
                                "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
                                "border_radius": "8px",
                                "max_height": "200px",
                                "overflow_y": "auto"
                            }
                        ),
                        value=AppState.id_servicio_seleccionado,
                        on_change=AppState.seleccionar_servicio
                    ),
                    spacing="2", width="100%"
                ),
                rx.vstack(
                    rx.text("Procedimiento Realizado *", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.text_area(value=rx.cond(AppState.formulario_intervencion.procedimiento_realizado, AppState.formulario_intervencion.procedimiento_realizado, ""),
                               on_change=lambda value: AppState.actualizar_campo_intervencion("procedimiento_realizado", value),
                               placeholder="Describe el procedimiento...", height="120px",
                               style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
                    spacing="2", width="100%"
                ),
                spacing="6", width="100%"
            ),
            
            # Columna 2: Materiales y precio
            rx.vstack(
                rx.vstack(
                    rx.text("Materiales Utilizados", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.text_area(value=rx.cond(AppState.formulario_intervencion.materiales_utilizados, AppState.formulario_intervencion.materiales_utilizados, ""),
                               on_change=lambda value: AppState.actualizar_campo_intervencion("materiales_utilizados", value),
                               placeholder="Lista de materiales...", height="80px",
                               style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
                    spacing="2", width="100%"
                ),
                rx.hstack(
                    # Nuevo selector de anestesia profesional
                    selector_anestesia_profesional(),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Precio Final *", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                            rx.cond(
                                AppState.precio_servicio_base > 0,
                                rx.badge(f"Base: ${AppState.precio_servicio_base:,.2f}", color_scheme="blue", variant="soft", size="1"),
                                rx.fragment()
                            ),
                            spacing="2", align_items="center"
                        ),
                        rx.hstack(
                            rx.input(type="number", value=rx.cond(AppState.formulario_intervencion.precio_final, AppState.formulario_intervencion.precio_final, "0"),
                                   on_change=lambda value: AppState.actualizar_campo_intervencion("precio_final", value),
                                   placeholder="0.00",
                                   style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
                            rx.cond(
                                AppState.precio_servicio_base > 0,
                                rx.button(
                                    "↻",
                                    size="2",
                                    variant="ghost",
                                    on_click=AppState.restaurar_precio_base,
                                    style={"color": COLORS["primary"]["400"], "_hover": {"background": COLORS["primary"]["900"]}}
                                ),
                                rx.fragment()
                            ),
                            spacing="2", width="100%"
                        ),
                        spacing="2", width="100%"
                    ),
                    spacing="4", width="100%"
                ),
                spacing="6", width="100%"
            ),
            columns="2", spacing="8", width="100%",
            # on_mount=AppState.load_servicios_for_intervention,  # Placeholder
        ),
        
        # Instrucciones y control
        rx.vstack(
            rx.text("Instrucciones para el Paciente", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
            rx.text_area(value="",  # Placeholder - AppState.intervencion_form["instrucciones"]
                       on_change=rx.noop,  # Placeholder - AppState.update_intervencion_form
                       placeholder="Instrucciones post-tratamiento...", height="80px",
                       style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
            
            rx.checkbox("Requiere Control", checked=False,  # Placeholder - AppState.intervencion_form["requiere_control"] == "true"
                       on_change=rx.noop),  # Placeholder - AppState.toggle_control_requerido
            
            rx.cond(False,  # Placeholder - AppState.intervencion_form["requiere_control"] == "true"
                   rx.input(type="date", value="",  # Placeholder - AppState.intervencion_form["fecha_control"]
                           on_change=rx.noop,  # Placeholder - AppState.update_intervencion_form
                           style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]})),
            
            spacing="3", align_items="start", width="100%"
        ),
        
        spacing="6", width="100%", align_items="start",
        
        # Cargar servicios cuando se abre este tab
        on_mount=AppState.cargar_servicios_disponibles
    )



def tab_content_finalizar() -> rx.Component:
    """💾 Contenido de finalización"""
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="check", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.text("💾 Revisar y Finalizar", size="6", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            spacing="3", align_items="center", margin_bottom="6"
        ),
        
        rx.grid(
            rx.box(
                rx.vstack(
                    rx.text("👤 Paciente", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),
                    rx.text(AppState.paciente_actual.nombre_completo, size="3", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                    rx.text(f"HC: {AppState.paciente_actual.numero_historia}", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                    spacing="2", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=COLORS["info"]["500"])
            ),
            rx.box(
                rx.vstack(
                    rx.text("⚕️ Intervención", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),
                    rx.cond(
                        AppState.servicio_seleccionado.nombre,
                        rx.text(f"Servicio: {AppState.servicio_seleccionado.nombre}", size="3", color=DARK_THEME["colors"]["text_primary"]),
                        rx.text("Sin servicio seleccionado", size="3", color=COLORS["warning"]["400"])
                    ),
                    rx.hstack(
                        rx.text(rx.cond(AppState.formulario_intervencion.precio_final, f"Precio: ${AppState.formulario_intervencion.precio_final:.2f}", "Precio: $0.00"), color=ODONTOLOGO_COLORS["primary"], weight="bold"),
                        rx.cond(
                            (AppState.precio_servicio_base > 0) & (AppState.formulario_intervencion.precio_final != AppState.precio_servicio_base),
                            rx.badge("Modificado", color_scheme="orange", variant="soft", size="1"),
                            rx.cond(
                                AppState.precio_servicio_base > 0,
                                rx.badge("Precio estándar", color_scheme="green", variant="soft", size="1"),
                                rx.fragment()
                            )
                        ),
                        spacing="2", align_items="center"
                    ),
                    rx.cond(
                        AppState.formulario_intervencion.requiere_control,
                        rx.text("Control: Sí", color=COLORS["warning"]["400"]),
                        rx.text("Control: No", color=COLORS["success"]["400"])
                    ),
                    spacing="2", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=ODONTOLOGO_COLORS["primary"])
            ),
            columns="2", spacing="6", width="100%"
        ),
        
        rx.box(
            rx.vstack(
                rx.text("📝 Procedimiento", size="4", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                rx.cond(
                    AppState.formulario_intervencion.procedimiento_realizado,
                    rx.cond(
                        AppState.formulario_intervencion.procedimiento_realizado.strip() != "",
                        rx.text(AppState.formulario_intervencion.procedimiento_realizado, color=DARK_THEME["colors"]["text_primary"]),
                        rx.text("No especificado", color=DARK_THEME["colors"]["text_secondary"])
                    ),
                    rx.text("No especificado", color=DARK_THEME["colors"]["text_secondary"])
                ),
                spacing="3", align_items="start", width="100%"
            ),
            style=dark_crystal_card(color=COLORS["warning"]["500"]), margin_top="6"
        ),
        
        # Resumen del odontograma si hay cambios
        rx.cond(
            AppState.cambios_pendientes_odontograma.length() > 0,
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="clipboard-list", size=20, color=ODONTOLOGO_COLORS["primary"]),
                        rx.text("🦷 Cambios en Odontograma", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),
                        spacing="2", align_items="center"
                    ),
                    rx.text("⚠️ Hay cambios sin guardar en el odontograma que se incluirán en la intervención", 
                           color=COLORS["warning"]["400"], size="3"),
                    rx.hstack(
                        rx.foreach(
                            AppState.odontogram_stats_summary,
                            lambda item: rx.cond(
                                item[1] > 0,
                                rx.badge(f"{item[0]}: {item[1]}", color_scheme="blue", variant="soft"),
                                rx.fragment()
                            )
                        ),
                        spacing="2", wrap="wrap"
                    ),
                    spacing="3", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=ODONTOLOGO_COLORS["primary"]), margin_top="6"
            )
        ),
        
        # Panel de validaciones
        rx.cond(
            AppState.errores_validacion_intervencion.length() > 0,
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="triangle-alert", size=20, color=COLORS["error"]["400"]),
                        rx.text("⚠️ Errores de Validación", size="4", weight="medium", color=COLORS["error"]["400"]),
                        spacing="2", align_items="center"
                    ),
                    rx.foreach(
                        AppState.errores_validacion_intervencion,
                        lambda error: rx.text(f"• {error}", size="2", color=COLORS["error"]["400"])
                    ),
                    spacing="2", align_items="start", width="100%"
                ),
                style={
                    **dark_crystal_card(color=COLORS["error"]["500"]),
                    "background": f"rgba(239, 68, 68, 0.1)"
                },
                margin_top="6"
            )
        ),
        
        # Botones de acción
        rx.hstack(
            # Botón guardar borrador
            rx.button(
                rx.hstack(
                    rx.icon(tag="save", size=18),
                    rx.text("💾 Guardar Borrador"),
                    spacing="2"
                ),
                size="3",
                variant="outline",
                color_scheme="cyan",
                on_click=AppState.guardar_borrador_intervencion,
                disabled=AppState.guardando_intervencion,
                style={
                    "border_color": ODONTOLOGO_COLORS["border"],
                    "_hover": {"background": "rgba(0, 188, 212, 0.1)"}
                }
            ),
            
            rx.spacer(),
            
            # Botón cancelar
            rx.button(
                rx.hstack(
                    rx.icon(tag="x", size=18),
                    rx.text("❌ Cancelar"),
                    spacing="2"
                ),
                size="3",
                variant="outline", 
                color_scheme="red",
                on_click=lambda: AppState.navigate_to("odontologia"),
                disabled=AppState.guardando_intervencion
            ),
            
            # Botón finalizar intervención
            rx.button(
                rx.hstack(
                    rx.cond(
                        AppState.guardando_intervencion,
                        rx.spinner(size="3", color="white"),
                        rx.icon(tag="circle-check", size=18)
                    ),
                    rx.text("✅ Finalizar Intervención"),
                    spacing="2"
                ),
                size="3",
                color_scheme="green",
                loading=AppState.guardando_intervencion,
                disabled=rx.cond(
                    AppState.errores_validacion_intervencion.length() > 0,
                    True,
                    AppState.guardando_intervencion
                ),
                on_click=lambda: AppState.navigate_to("dashboard"),
                style={
                    "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['success']['600']} 100%)",
                    "box_shadow": f"0 4px 20px rgba(34, 197, 94, 0.4)",
                    "_hover": {
                        "transform": "translateY(-2px)",
                        "box_shadow": f"0 8px 30px rgba(34, 197, 94, 0.5)"
                    }
                }
            ),
            
            spacing="4",
            align_items="center",
            width="100%",
            margin_top="8",
            padding="4",
            style={
                "background": "rgba(255, 255, 255, 0.02)",
                "border_top": f"1px solid {ODONTOLOGO_COLORS['border']}",
                "border_radius": f"0 0 {RADIUS['2xl']} {RADIUS['2xl']}"
            }
        ),
        
        spacing="6", width="100%", align_items="start"
    )

# ==========================================
# 📦 CONTENEDOR PRINCIPAL INTEGRADO
# ==========================================

def intervention_tabs_integrated() -> rx.Component:
    """🦷 Sistema de tabs completo con contenido integrado"""
    return rx.vstack(
        # Navegación de tabs
        tabs_navigation(),
        
        # Contenido dinámico
        rx.box(
            rx.cond(
                AppState.active_intervention_tab == "odontograma", tab_content_odontograma(),
                rx.cond(
                    AppState.active_intervention_tab == "intervencion", tab_content_intervencion(),
                    tab_content_finalizar()
                )
            ),
            
            style={
                "background": "rgba(255, 255, 255, 0.05)",
                "backdrop_filter": "blur(20px) saturate(180%)",
                "border": f"1px solid {ODONTOLOGO_COLORS['border']}",
                "border_radius": RADIUS["3xl"],
                "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
                "padding": SPACING["8"],
                "min_height": "600px"
            }
        ),
        
        spacing="6",
        width="100%",
        max_width="1400px",
        
        # Click handler removido - el popover se cierra por el overlay principal
    )