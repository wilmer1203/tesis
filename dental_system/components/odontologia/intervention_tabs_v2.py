# 🦷 COMPONENTE: TABS INTEGRADO CON CONTENIDO ESPECÍFICO - VERSION SIMPLIFICADA
# dental_system/components/odontologia/intervention_tabs_v2.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS, dark_crystal_card
from dental_system.components.odontologia.odontogram_grid import (
    odontogram_interactive_grid, odontogram_toolbar
)
from dental_system.components.odontologia.condition_selector_modal import (
    condition_selector_modal, odontogram_legend
)
from dental_system.components.odontologia.interactive_tooth import selected_tooth_info_panel

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
    "paciente": {"title": "📋 Información Paciente", "icon": "user-check", "color": COLORS["info"]["500"]},
    "odontograma": {"title": "🦷 Odontograma", "icon": "clipboard-list", "color": ODONTOLOGO_COLORS["primary"]},
    "intervencion": {"title": "⚕️ Intervención", "icon": "activity", "color": COLORS["warning"]["500"]},
    "finalizar": {"title": "💾 Finalizar", "icon": "check-circle", "color": ODONTOLOGO_COLORS["accent"]}
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

def tab_content_paciente() -> rx.Component:
    """📋 Contenido del tab de información del paciente"""
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="user-check", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.text("📋 Información del Paciente", size="6", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            spacing="3", align_items="center", margin_bottom="6"
        ),
        
        rx.grid(
            # Datos personales
            rx.box(
                rx.vstack(
                    rx.text("👤 Datos Personales", size="4", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                    rx.vstack(
                        rx.hstack(rx.text("Nombre:", weight="medium", color=DARK_THEME["colors"]["text_secondary"]), 
                                 rx.text(AppState.paciente_en_atencion.nombre_completo, color=DARK_THEME["colors"]["text_primary"]), spacing="2"),
                        rx.hstack(rx.text("Documento:", weight="medium", color=DARK_THEME["colors"]["text_secondary"]), 
                                 rx.text(AppState.paciente_en_atencion.numero_documento, color=DARK_THEME["colors"]["text_primary"]), spacing="2"),
                        rx.hstack(rx.text("Teléfono:", weight="medium", color=DARK_THEME["colors"]["text_secondary"]), 
                                 rx.text(AppState.paciente_en_atencion.telefono_display, color=DARK_THEME["colors"]["text_primary"]), spacing="2"),
                        spacing="2", align_items="start"
                    ),
                    spacing="4", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=COLORS["info"]["500"])
            ),
            
            # Información médica
            rx.box(
                rx.vstack(
                    rx.text("🏥 Información Médica", size="4", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                    rx.vstack(
                        rx.cond(AppState.paciente_en_atencion.alergias != [], 
                               rx.vstack(rx.text("⚠️ Alergias:", weight="medium", color=COLORS["error"]["400"]),
                                        rx.text(AppState.paciente_en_atencion.alergias_display, color=DARK_THEME["colors"]["text_primary"]), 
                                        spacing="1", align_items="start"),
                               rx.text("✅ Sin alergias conocidas", color=COLORS["success"]["400"])),
                        
                        rx.cond(AppState.paciente_en_atencion.condiciones_medicas != [],
                               rx.vstack(rx.text("🏥 Condiciones:", weight="medium", color=COLORS["warning"]["400"]),
                                        rx.text(AppState.paciente_en_atencion.condiciones_display, color=DARK_THEME["colors"]["text_primary"]),
                                        spacing="1", align_items="start"),
                               rx.text("✅ Sin condiciones reportadas", color=COLORS["success"]["400"])),
                        spacing="4", align_items="start"
                    ),
                    spacing="4", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=COLORS["warning"]["500"])
            ),
            columns="2", spacing="6", width="100%"
        ),
        spacing="6", width="100%", align_items="start"
    )

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
                AppState.is_loading_odontograma,
                rx.badge("🔄 Cargando...", color_scheme="blue", variant="soft"),
                rx.cond(
                    AppState.odontogram_modified,
                    rx.badge("⚠️ Cambios sin guardar", color_scheme="orange", variant="soft"),
                    rx.badge("✅ Sincronizado", color_scheme="green", variant="soft")
                )
            ),
            
            spacing="3", align_items="start", width="100%"
        ),
        
        # Toolbar de herramientas
        odontogram_toolbar(),
        
        # Contenedor principal del odontograma
        rx.box(
            rx.cond(
                AppState.is_loading_odontograma,
                
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
                AppState.selected_tooth,
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
        
        spacing="6", width="100%", align_items="start",
        
        # Event handler para inicializar el odontograma cuando se carga el tab
        on_mount=AppState.initialize_odontogram_for_intervention
    )

def tab_content_intervencion() -> rx.Component:
    """⚕️ Contenido del formulario de intervención"""
    return rx.vstack(
        # Event handler para cargar servicios cuando se abre el tab
       
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
                            AppState.servicios_list.length() > 0,
                            rx.badge(f"{AppState.servicios_list.length()} disponibles", color_scheme="green", variant="soft", size="1"),
                            rx.badge("Cargando servicios...", color_scheme="orange", variant="soft", size="1")
                        ),
                        spacing="2", align_items="center"
                    ),
                    rx.select(AppState.servicios_opciones, value=AppState.servicio_seleccionado_nombre,
                             on_change=AppState.update_servicio_seleccionado, placeholder="Seleccionar servicio...",
                             style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
                    spacing="2", width="100%"
                ),
                rx.vstack(
                    rx.text("Procedimiento Realizado *", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.text_area(value=AppState.intervencion_form["procedimiento"], 
                               on_change=lambda v: AppState.update_intervencion_form("procedimiento", v),
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
                    rx.text_area(value=AppState.intervencion_form["materiales"],
                               on_change=lambda v: AppState.update_intervencion_form("materiales", v),
                               placeholder="Lista de materiales...", height="80px",
                               style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
                    spacing="2", width="100%"
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("Anestesia", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                        rx.select(["Ninguna", "Lidocaína", "Articaína", "Mepivacaína", "Otra"],
                                 value=AppState.intervencion_form["anestesia"], on_change=lambda v: AppState.update_intervencion_form("anestesia", v),
                                 style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
                        spacing="2", width="100%"
                    ),
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
                            rx.input(type="number", value=AppState.intervencion_form["precio_final"],
                                   on_change=lambda v: AppState.update_intervencion_form("precio_final", v), placeholder="0.00",
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
            on_mount=AppState.load_servicios_for_intervention,
        ),
        
        # Instrucciones y control
        rx.vstack(
            rx.text("Instrucciones para el Paciente", size="3", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
            rx.text_area(value=AppState.intervencion_form["instrucciones"],
                       on_change=lambda v: AppState.update_intervencion_form("instrucciones", v),
                       placeholder="Instrucciones post-tratamiento...", height="80px",
                       style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]}),
            
            rx.checkbox("Requiere Control", checked=AppState.intervencion_form["requiere_control"] == "true",
                       on_change=AppState.toggle_control_requerido),
            
            rx.cond(AppState.intervencion_form["requiere_control"] == "true",
                   rx.input(type="date", value=AppState.intervencion_form["fecha_control"],
                           on_change=lambda v: AppState.update_intervencion_form("fecha_control", v),
                           style={"background": DARK_THEME["colors"]["surface_secondary"], "border": f"1px solid {ODONTOLOGO_COLORS['border']}", "color": DARK_THEME["colors"]["text_primary"]})),
            
            spacing="3", align_items="start", width="100%"
        ),
        
        spacing="6", width="100%", align_items="start"
    )

def tab_content_finalizar() -> rx.Component:
    """💾 Contenido de finalización"""
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="check-circle", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.text("💾 Revisar y Finalizar", size="6", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            spacing="3", align_items="center", margin_bottom="6"
        ),
        
        rx.grid(
            rx.box(
                rx.vstack(
                    rx.text("👤 Paciente", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),
                    rx.text(AppState.paciente_en_atencion.nombre_completo, size="3", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                    rx.text(f"HC: {AppState.paciente_en_atencion.numero_historia}", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                    spacing="2", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=COLORS["info"]["500"])
            ),
            rx.box(
                rx.vstack(
                    rx.text("⚕️ Intervención", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),
                    rx.cond(
                        AppState.servicio_seleccionado_nombre != "",
                        rx.text(f"Servicio: {AppState.servicio_seleccionado_nombre}", size="3", color=DARK_THEME["colors"]["text_primary"]),
                        rx.text("Sin servicio seleccionado", size="3", color=COLORS["warning"]["400"])
                    ),
                    rx.hstack(
                        rx.text(rx.cond(AppState.intervencion_form["precio_final"], f"Precio: ${AppState.intervencion_form['precio_final']}", "Precio: $0.00"), color=ODONTOLOGO_COLORS["primary"], weight="bold"),
                        rx.cond(
                            (AppState.precio_servicio_base > 0) & (AppState.intervencion_form["precio_final"] != str(AppState.precio_servicio_base)),
                            rx.badge("Modificado", color_scheme="orange", variant="soft", size="1"),
                            rx.cond(
                                AppState.precio_servicio_base > 0,
                                rx.badge("Precio estándar", color_scheme="green", variant="soft", size="1"),
                                rx.fragment()
                            )
                        ),
                        spacing="2", align_items="center"
                    ),
                    rx.text(rx.cond(AppState.intervencion_form["requiere_control"] == "true", "Control: Sí", "Control: No"), color=COLORS["success"]["400"]),
                    spacing="2", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=ODONTOLOGO_COLORS["primary"])
            ),
            columns="2", spacing="6", width="100%"
        ),
        
        rx.box(
            rx.vstack(
                rx.text("📝 Procedimiento", size="4", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                rx.text(rx.cond(AppState.intervencion_form["procedimiento"], AppState.intervencion_form["procedimiento"], "No especificado"), color=DARK_THEME["colors"]["text_secondary"]),
                spacing="3", align_items="start", width="100%"
            ),
            style=dark_crystal_card(color=COLORS["warning"]["500"]), margin_top="6"
        ),
        
        # Resumen del odontograma si hay cambios
        rx.cond(
            AppState.odontogram_modified,
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
                AppState.active_intervention_tab == "paciente", tab_content_paciente(),
                rx.cond(
                    AppState.active_intervention_tab == "odontograma", tab_content_odontograma(),
                    rx.cond(
                        AppState.active_intervention_tab == "intervencion", tab_content_intervencion(),
                        tab_content_finalizar()
                    )
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
        max_width="1400px"
    )