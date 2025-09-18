# 🦷 COMPONENTE: TABS INTEGRADO CON CONTENIDO ESPECÍFICO - VERSION SIMPLIFICADA
# dental_system/components/odontologia/intervention_tabs_v2.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS, dark_crystal_card, GRADIENTS

# Paleta REAL basada en DARK_THEME y componentes que funcionan
REFINED_COLORS = {
    # Fondos usando DARK_THEME real
    "background": DARK_THEME["colors"]["background"],           # #0a0b0d
    "surface": DARK_THEME["colors"]["surface_secondary"],      # #242529
    "surface_hover": DARK_THEME["colors"]["surface_elevated"], # #2d2f33
    "surface_elevated": DARK_THEME["colors"]["surface_elevated"], # #2d2f33

    # Bordes usando DARK_THEME real
    "border": DARK_THEME["colors"]["border"],                  # #3a3b3f
    "border_strong": DARK_THEME["colors"]["border_strong"],    # #4a4b4f
    "border_hover": COLORS["primary"]["400"],                  # Color primario para hover
    "border_focus": COLORS["primary"]["300"],                  # Color primario más suave

    # Textos usando DARK_THEME real
    "text_primary": DARK_THEME["colors"]["text_primary"],      # gray 100
    "text_secondary": DARK_THEME["colors"]["text_secondary"],  # gray 300
    "text_muted": DARK_THEME["colors"]["text_muted"],          # gray 500
    "text_accent": COLORS["primary"]["400"],                   # Color primario

    # Colores principales del sistema (COLORS reales)
    "primary": COLORS["primary"]["400"],                       # Turquesa sistema
    "primary_hover": COLORS["primary"]["300"],                 # Turquesa hover
    "primary_light": f"rgba({COLORS['primary']['400']}, 0.1)", # Turquesa suave

    "secondary": COLORS["blue"]["500"],                        # Azul sistema
    "secondary_hover": COLORS["blue"]["200"],                  # Azul hover
    "secondary_light": f"rgba({COLORS['blue']['500']}, 0.1)",  # Azul suave

    "success": COLORS["success"]["500"],                       # Verde sistema
    "success_hover": COLORS["success"]["400"],                 # Verde hover
    "success_light": f"rgba({COLORS['success']['500']}, 0.1)", # Verde suave

    "warning": COLORS["warning"]["500"],                       # Naranja sistema
    "warning_hover": COLORS["warning"]["300"],                 # Naranja hover
    "warning_light": f"rgba({COLORS['warning']['500']}, 0.1)", # Naranja suave

    "error": COLORS["error"]["500"],                           # Rojo sistema
    "error_hover": COLORS["error"]["400"],                     # Rojo hover
    "error_light": f"rgba({COLORS['error']['500']}, 0.1)",     # Rojo suave

    # Gradientes suaves como en consultas_page_v41.py

    "gradient_neon": GRADIENTS["neon_primary"],                              # Del sistema
    "gradient_text": GRADIENTS["text_gradient_primary"],                     # Del sistema
}

# Colores del módulo odontólogo (usando REFINED_COLORS)
ODONTOLOGO_COLORS = {
    "primary": REFINED_COLORS["primary"],          # Turquesa sistema
    "secondary": REFINED_COLORS["secondary"],      # Azul médico
    "accent": REFINED_COLORS["success"],           # Verde para acentos
    "surface": REFINED_COLORS["surface"],          # Superficie glassmorphism
    "border": REFINED_COLORS["border"]             # Bordes cristal
}

# ==========================================
# 🎨 ESTILOS PARA TABS INTEGRADO
# ==========================================

TAB_CONFIG = {
    "intervencion": {"title": "📝 Intervención", "icon": "activity", "color": COLORS["warning"]["500"]},
    "odontograma": {"title": "🦷 Historial", "icon": "clipboard-list", "color": ODONTOLOGO_COLORS["primary"]},
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
                "color": REFINED_COLORS["text_secondary"],
                "border_radius": RADIUS["xl"],
                "padding": f"{SPACING['2']} {SPACING['4']}",
                "transition": "all 0.3s ease",
                "_hover": {
                    "background": f"linear-gradient(135deg, {config['color']}30 0%, {config['color']}15 100%)",
                    "color": REFINED_COLORS["text_primary"]
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

def tab_content_odontograma() -> rx.Component:
    """🦷 Contenido del odontograma - MODO HISTORIAL/CONSULTA"""

    return rx.vstack(
        # Header del historial
        rx.hstack(
            rx.icon(tag="history", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.vstack(
                rx.text("🦷 Historial Odontológico", size="6", weight="bold", color=REFINED_COLORS["text_primary"]),
                rx.text("Consulta el historial de tratamientos por diente del paciente", size="3", color=REFINED_COLORS["text_secondary"]),
                spacing="1", align_items="start"
            ),
            rx.spacer(),

            # Indicadores de modo consulta
            rx.hstack(
                rx.badge("👁️ Solo Lectura", color_scheme="blue", variant="soft"),
                rx.badge("📚 Historial", color_scheme="purple", variant="soft"),
                rx.badge(f"📊 {AppState.paciente_actual.nombre_completo}", color_scheme="green", variant="soft"),
                spacing="2"
            ),

            spacing="3", align_items="start", width="100%"
        ),

        # Layout principal: Odontograma + Panel de Detalles
        rx.hstack(
            # Odontograma de consulta (lado izquierdo)
            rx.box(
                rx.vstack(
                    rx.text("🦷 Selecciona un diente para ver su historial",
                           size="3", color=REFINED_COLORS["text_secondary"],
                           text_align="center", margin_bottom="4"),

                    # Odontograma simple para consulta
                    odontograma_consulta_historial(),

                    spacing="4",
                    align_items="center",
                    width="100%"
                ),
                width="60%"
            ),

            # Panel de historial del diente (lado derecho)
            rx.box(
                panel_historial_diente_seleccionado(),
                width="40%"
            ),

            spacing="6",
            width="100%",
            align_items="start"
        ),

        spacing="6", width="100%", align_items="start"
    )

def tab_content_intervencion() -> rx.Component:
    """⚕️ Contenido NUEVO con selector de servicios y tabla agregada"""
    from dental_system.components.odontologia.selector_intervenciones_v2 import nuevo_tab_intervencion

    return rx.vstack(
        # Header del tab
        rx.hstack(
            rx.icon(tag="activity", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.text("Registro de Intervención", size="6", weight="bold", color=REFINED_COLORS["text_primary"]),

            rx.spacer(),
             rx.button(
                rx.hstack(
                    rx.cond(
                        AppState.guardando_intervencion,
                        rx.spinner(size="3", color="white"),
                        rx.icon("check", size=16)
                    ),
                    rx.text("Finalizar Intervencion"),
                    spacing="2"
                ),
                size="4",
                loading=AppState.guardando_intervencion,
                disabled=AppState.guardando_intervencion,
                on_click=AppState.finalizar_consulta_completa,
                style={
                    "background": REFINED_COLORS["gradient_neon"],
                    "box_shadow": f"0 6px 25px {COLORS['blue']['600']}",
                    "color": "white",
                    "_hover": {
                        "transform": "translateY(-2px)",
                        "box_shadow": f"0 10px 35px {COLORS['blue']['600']}"
                    }
                }
            ),


            spacing="3", align_items="center", margin_bottom="6",
        ),

        # Nuevo componente con flujo mejorado
        nuevo_tab_intervencion(),

        spacing="6", width="100%", align_items="start"
    )

def tab_content_finalizar() -> rx.Component:
    """💾 Contenido de finalización"""
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="check", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.text("💾 Revisar y Finalizar", size="6", weight="bold", color=REFINED_COLORS["text_primary"]),
            spacing="3", align_items="center", margin_bottom="6"
        ),

        rx.grid(
            rx.box(
                rx.vstack(
                    rx.text("👤 Paciente", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),
                    rx.text(AppState.paciente_actual.nombre_completo, size="3", weight="medium", color=REFINED_COLORS["text_primary"]),
                    rx.text(f"HC: {AppState.paciente_actual.numero_historia}", size="2", color=REFINED_COLORS["text_secondary"]),
                    spacing="2", align_items="start", width="100%"
                ),
                style=dark_crystal_card(color=COLORS["info"]["500"])
            ),
            rx.box(
                rx.vstack(
                    rx.text("⚕️ Intervención", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),
                    rx.cond(
                        AppState.servicio_seleccionado.nombre,
                        rx.text(f"Servicio: {AppState.servicio_seleccionado.nombre}", size="3", color=REFINED_COLORS["text_primary"]),
                        rx.text("Sin servicio seleccionado", size="3", color=COLORS["warning"]["300"])
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
                        rx.text("Control: Sí", color=COLORS["warning"]["300"]),
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
                rx.text("📝 Procedimiento", size="4", weight="medium", color=REFINED_COLORS["text_primary"]),
                rx.cond(
                    AppState.formulario_intervencion.procedimiento_realizado,
                    rx.cond(
                        AppState.formulario_intervencion.procedimiento_realizado.strip() != "",
                        rx.text(AppState.formulario_intervencion.procedimiento_realizado, color=REFINED_COLORS["text_primary"]),
                        rx.text("No especificado", color=REFINED_COLORS["text_secondary"])
                    ),
                    rx.text("No especificado", color=REFINED_COLORS["text_secondary"])
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
                           color=COLORS["warning"]["300"], size="3"),
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
                        rx.icon(tag="triangle_alert", size=20, color=COLORS["error"]["400"]),
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
                AppState.active_intervention_tab == "intervencion", tab_content_intervencion(),
                rx.cond(
                    AppState.active_intervention_tab == "odontograma", tab_content_odontograma(),
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
    )

# ==========================================
# 🦷 COMPONENTES PARA TAB HISTORIAL - CON DATOS REALES
# ==========================================

def odontograma_consulta_historial() -> rx.Component:
    """🦷 Odontograma con datos reales de la BD - modo consulta"""

    def diente_consulta_real(numero_diente: int) -> rx.Component:
        """Diente que muestra estado real desde BD"""
        return rx.button(
            rx.vstack(
                rx.text(numero_diente, size="2", weight="bold", color="white"),
                rx.text("🦷", size="1"),
                spacing="0", align_items="center"
            ),
            # Color según estado real del diente desde BD
            color_scheme=rx.cond(
                AppState.diente_seleccionado == numero_diente,
                "blue",  # Seleccionado
                rx.cond(
                    AppState.obtener_color_diente(numero_diente) == "green",
                    "green",  # Sano
                    rx.cond(
                        AppState.obtener_color_diente(numero_diente) == "red",
                        "red",    # Caries
                        "gray"    # Otros estados
                    )
                )
            ),
            variant="solid",
            size="1",
            on_click=lambda: AppState.seleccionar_diente_para_historial(numero_diente),
            style={
                "width": "45px",
                "height": "45px",
                "transition": "all 0.2s ease",
                "_hover": {
                    "transform": "scale(1.05)"
                }
            }
        )

    return rx.vstack(
        # Usar los cuadrantes reales del AppState
        rx.vstack(
            rx.text("Arcada Superior", size="2", color=REFINED_COLORS["text_secondary"], text_align="center"),
            rx.hstack(
                # Cuadrante 1 (Superior Derecho: 18-11)
                rx.hstack(
                    rx.foreach(AppState.cuadrante_1, diente_consulta_real),
                    spacing="1"
                ),
                rx.box(width="10px"),
                # Cuadrante 2 (Superior Izquierdo: 21-28)
                rx.hstack(
                    rx.foreach(AppState.cuadrante_2, diente_consulta_real),
                    spacing="1"
                ),
                spacing="2", justify_content="center"
            ),
            spacing="2"
        ),

        rx.box(height="20px"),

        rx.vstack(
            rx.hstack(
                # Cuadrante 4 (Inferior Derecho: 48-41)
                rx.hstack(
                    rx.foreach(AppState.cuadrante_4, diente_consulta_real),
                    spacing="1"
                ),
                rx.box(width="10px"),
                # Cuadrante 3 (Inferior Izquierdo: 31-38)
                rx.hstack(
                    rx.foreach(AppState.cuadrante_3, diente_consulta_real),
                    spacing="1"
                ),
                spacing="2", justify_content="center"
            ),
            rx.text("Arcada Inferior", size="2", color=REFINED_COLORS["text_secondary"], text_align="center"),
            spacing="2"
        ),

        spacing="4",
        align_items="center",
        style={
            "background": REFINED_COLORS["surface"],
            "border": f"1px solid {REFINED_COLORS['border']}",
            "border_radius": RADIUS["xl"],
            "padding": SPACING["6"]
        }
    )

def panel_historial_diente_seleccionado() -> rx.Component:
    """📚 Panel que muestra historial REAL del diente desde BD"""

    return rx.box(
        rx.cond(
            AppState.diente_seleccionado,
            # Mostrar historial real del diente
            rx.vstack(
                # Header del diente con info real
                rx.hstack(
                    rx.text("🦷", size="6"),
                    rx.vstack(
                        rx.text(f"Diente #{AppState.diente_seleccionado}",
                               size="5", weight="bold", color=REFINED_COLORS["text_primary"]),
                        rx.text(f"Tipo: {AppState.obtener_tipo_diente()}",
                               size="2", color=REFINED_COLORS["text_secondary"]),
                        rx.text(f"Cuadrante: {AppState.obtener_cuadrante_diente()}",
                               size="2", color=REFINED_COLORS["text_secondary"]),
                        spacing="1", align_items="start"
                    ),
                    spacing="3", align_items="center", width="100%", margin_bottom="4"
                ),

                # Historial real desde BD
                rx.vstack(
                    rx.text("📅 Historial de Intervenciones", size="4", weight="medium", color=ODONTOLOGO_COLORS["primary"]),

                    # Lista real de intervenciones en este diente
                    rx.cond(
                        AppState.historial_diente_seleccionado.length() > 0,
                        rx.foreach(
                            AppState.historial_diente_seleccionado,
                            lambda intervencion: entrada_historial_real(intervencion)
                        ),
                        rx.text("Sin intervenciones registradas en este diente",
                               size="2", color=REFINED_COLORS["text_muted"],
                               style={"fontStyle": "italic"})
                    ),

                    spacing="3", width="100%"
                ),

                spacing="4", width="100%"
            ),

            # Sin diente seleccionado
            rx.center(
                rx.vstack(
                    rx.icon("mouse-pointer", size=48, color=REFINED_COLORS["text_muted"]),
                    rx.text("Selecciona un diente", size="4", color=REFINED_COLORS["text_muted"]),
                    rx.text("para ver su historial", size="3", color=REFINED_COLORS["text_muted"]),
                    spacing="2", align_items="center"
                ),
                height="300px"
            )
        ),

        style={
            "background": REFINED_COLORS["surface"],
            "border": f"1px solid {REFINED_COLORS['border']}",
            "border_radius": RADIUS["xl"],
            "padding": SPACING["6"],
            "min_height": "400px"
        }
    )

def entrada_historial_real(intervencion) -> rx.Component:
    """📝 Entrada de historial con datos reales de IntervencionModel"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(intervencion.get("servicio_nombre", "Servicio"), color_scheme="blue", variant="soft"),
                rx.spacer(),
                rx.text(intervencion.get("fecha_formateada", "Fecha"), size="1", color=REFINED_COLORS["text_muted"]),
                width="100%", align_items="center"
            ),
            rx.text(intervencion.get("observaciones", "Sin observaciones"),
                   size="2", color=REFINED_COLORS["text_primary"]),
            rx.hstack(
                rx.icon("user", size=12, color=REFINED_COLORS["text_muted"]),
                rx.text(intervencion.get("odontologo_nombre", "Dr. Sistema"),
                       size="1", color=REFINED_COLORS["text_muted"]),
                rx.spacer(),
                rx.text(f"${intervencion.get('costo_total', 0):.2f}",
                       size="1", color=COLORS["success"]["400"], weight="medium"),
                spacing="1", align_items="center", width="100%"
            ),
            spacing="2", align_items="start", width="100%"
        ),
        size="1", width="100%"
    )