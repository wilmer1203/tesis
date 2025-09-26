# 🦷 COMPONENTE: TABS INTEGRADO CON CONTENIDO ESPECÍFICO - VERSION SIMPLIFICADA
# dental_system/components/odontologia/intervention_tabs_v2.py

import reflex as rx
from typing import List, Any
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS, dark_crystal_card, GRADIENTS

# ==========================================
# 🆕 IMPORTS ODONTOGRAMA INTERACTIVO V2.0
# ==========================================
from dental_system.components.odontologia.odontograma_interactivo_grid import (
    odontograma_principal_con_estados
)

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
    "historial": {"title": "🦷 Historial", "icon": "clipboard-list", "color": ODONTOLOGO_COLORS["primary"]}
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

def tab_content_historial() -> rx.Component:
    """🦷 Contenido del historial V2.0 - MODO CONSULTA COMPLETO"""

    return rx.vstack(
        # Header del odontograma interactivo
        rx.hstack(
            rx.icon(tag="clipboard-list", size=32, color=ODONTOLOGO_COLORS["primary"]),
            rx.vstack(
                rx.text("🦷 Odontograma Interactivo V2.0", size="6", weight="bold", color=REFINED_COLORS["text_primary"]),
                rx.text("Registra condiciones por diente y superficie con sistema FDI profesional", size="3", color=REFINED_COLORS["text_secondary"]),
                spacing="1", align_items="start"
            ),
            rx.spacer(),

            # Indicadores de estado V2.0
            rx.hstack(
                rx.badge("✏️ Edición Interactiva", color_scheme="cyan", variant="soft"),
                rx.badge("🦷 FDI Standard", color_scheme="blue", variant="soft"),
                rx.badge(f"👤 {AppState.paciente_actual.nombre_completo}", color_scheme="green", variant="soft"),
                spacing="2"
            ),

            spacing="3", align_items="start", width="100%"
        ),

        # Separador visual
        rx.divider(margin_y="4", border_color=REFINED_COLORS["border"]),

        # 🏥 COMPONENTE PROFESIONAL V2.0 - BD REAL CON ESTADOS
        tab_content_odontograma_profesional_with_states(),

        spacing="6",
        width="100%",
        align_items="start",
        min_height="800px",
        # Cargar historial automáticamente al montar el componente
        on_mount=AppState.inicializar_historial_paciente
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
                    rx.text("Finalizar MI Intervención"),
                    spacing="2"
                ),
                size="4",
                loading=AppState.guardando_intervencion,
                disabled=AppState.guardando_intervencion,
                on_click=AppState.finalizar_mi_intervencion_odontologo,
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


# ==========================================
# 📦 CONTENEDOR PRINCIPAL INTEGRADO
# ==========================================

def intervention_tabs_integrated() -> rx.Component:
    """🦷 Sistema de tabs completo con contenido integrado"""
    return rx.vstack(
        # Navegación de tabs
        tabs_navigation(),

        # Contenido dinámico - Solo 2 tabs
        rx.box(
            rx.cond(
                AppState.active_intervention_tab == "intervencion",
                tab_content_intervencion(),
                tab_content_historial()
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

    def diente_historial_real(numero_diente: int) -> rx.Component:
        """Diente que muestra estado real desde BD con colores dinámicos"""
        return rx.button(
            rx.vstack(
                rx.text(numero_diente, size="2", weight="bold", color="white"),
                rx.text("🦷", size="1"),
                spacing="0", align_items="center"
            ),
            on_click=lambda: AppState.seleccionar_diente_para_historial(numero_diente),
            style={
                "width": "45px",
                "height": "45px",
                "background": AppState.color_diente_historial(numero_diente),
                "border": rx.cond(
                    AppState.diente_seleccionado == numero_diente,
                    f"3px solid {COLORS['blue']['400']}",
                    "2px solid rgba(255,255,255,0.2)"
                ),
                "border_radius": RADIUS["md"],
                "transition": "all 0.3s ease",
                "cursor": "pointer",
                "_hover": {
                    "transform": "scale(1.08)",
                    "box_shadow": f"0 4px 15px rgba({AppState.color_diente_historial(numero_diente)}, 0.4)"
                }
            }
        )

    return rx.vstack(
        # INFO: Los cuadrantes se cargan automáticamente del AppState
        rx.vstack(
            rx.text("Arcada Superior", size="2", color=REFINED_COLORS["text_secondary"], text_align="center"),
            rx.hstack(
                # Cuadrante 1 (Superior Derecho: 18-11)
                rx.hstack(
                    rx.foreach(AppState.cuadrante_1, diente_historial_real),
                    spacing="1"
                ),
                rx.box(width="10px"),
                # Cuadrante 2 (Superior Izquierdo: 21-28)
                rx.hstack(
                    rx.foreach(AppState.cuadrante_2, diente_historial_real),
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
                    rx.foreach(AppState.cuadrante_4, diente_historial_real),
                    spacing="1"
                ),
                rx.box(width="10px"),
                # Cuadrante 3 (Inferior Izquierdo: 31-38)
                rx.hstack(
                    rx.foreach(AppState.cuadrante_3, diente_historial_real),
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

# ==========================================
# 🏥 COMPONENTE PROFESIONAL - BD REAL INTEGRADA
# ==========================================

def tab_content_odontograma_profesional() -> rx.Component:
    """
    🏥 TAB HISTORIAL PROFESIONAL - VERSION 2.0 CON BD REAL

    Arquitectura de 3 paneles médicos:
    - Panel izquierdo: Odontograma FDI interactivo (32 dientes)
    - Panel central: Detalles del diente seleccionado
    - Panel derecho: Historial y estadísticas del paciente
    """
    return rx.vstack(
        # Header profesional con información del paciente
        rx.box(
            rx.hstack(
                # Información del paciente
                rx.hstack(
                    rx.icon("user-check", size=24, color=ODONTOLOGO_COLORS["primary"]),
                    rx.vstack(
                        rx.text(
                            rx.cond(
                                AppState.paciente_actual.primer_nombre != "",
                                f"{AppState.paciente_actual.primer_nombre} {AppState.paciente_actual.primer_apellido}",
                                "Paciente no seleccionado"
                            ),
                            size="4",
                            weight="bold",
                            color=REFINED_COLORS["text_primary"]
                        ),
                        rx.text(
                            f"HC: {AppState.paciente_actual.numero_historia}",
                            size="2",
                            color=REFINED_COLORS["text_muted"]
                        ),
                        spacing="0",
                        align_items="start"
                    ),
                    spacing="3"
                ),

                rx.spacer(),

                # Estadísticas rápidas del paciente
                rx.hstack(
                    stats_card_mini("Intervenciones", AppState.estadisticas_paciente_resumen["total_intervenciones"]),
                    stats_card_mini("Dientes", AppState.estadisticas_paciente_resumen["dientes_afectados"]),
                    stats_card_mini("Última Visita", AppState.estadisticas_paciente_resumen["ultima_visita"]),
                    spacing="3"
                ),

                # Estado de carga
                rx.cond(
                    AppState.cargando_odontograma_historial,
                    rx.hstack(
                        rx.spinner(size="3", color=ODONTOLOGO_COLORS["primary"]),
                        rx.text("Cargando historial...", size="2", color=REFINED_COLORS["text_muted"]),
                        spacing="2"
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("refresh-cw", size=16),
                            rx.text("Actualizar"),
                            spacing="2"
                        ),
                        size="2",
                        variant="soft",
                        # on_click=AppState.cargar_historial_diente_especifico
                    )
                ),

                width="100%",
                align_items="center",
                justify_content="space-between"
            ),
            width="100%",
            padding="4",
            style={
                "background": f"linear-gradient(135deg, {ODONTOLOGO_COLORS['primary']}, rgba(255,255,255,0.02))",
                "border_radius": RADIUS["xl"],
                "border": f"1px solid {REFINED_COLORS['border']}"
            }
        ),

        # Contenido principal - 3 paneles
        rx.hstack(
            # Panel izquierdo: Odontograma interactivo
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("activity", size=20, color=ODONTOLOGO_COLORS["primary"]),
                        rx.text("Odontograma FDI", size="3", weight="bold", color=REFINED_COLORS["text_primary"]),
                        rx.spacer(),
                        rx.badge(
                            rx.cond(
                                AppState.diente_seleccionado != 0,
                                f"Diente {AppState.diente_seleccionado}",
                                "Sin selección"
                            ),
                            color_scheme="blue",
                            variant="soft"
                        ),
                        width="100%",
                        align_items="center"
                    ),

                    rx.divider(margin_y="3"),

                    # Odontograma con 32 dientes usando componente existente optimizado
                    odontograma_medico_profesional(),

                    spacing="3",
                    width="100%"
                ),
                width="40%",
                padding="4",
                style={
                    "background": "rgba(255, 255, 255, 0.02)",
                    "border_radius": RADIUS["lg"],
                    "border": f"1px solid {REFINED_COLORS['border']}",
                    "min_height": "500px"
                }
            ),

            # Panel central: Detalles del diente seleccionado
            rx.box(
                rx.vstack(
                    # Header del panel central
                    rx.hstack(
                        rx.icon("search", size=20, color=ODONTOLOGO_COLORS["secondary"]),
                        rx.text("Detalles del Diente", size="3", weight="bold", color=REFINED_COLORS["text_primary"]),
                        rx.spacer(),
                        rx.text(
                            AppState.diente_seleccionado_nombre,
                            size="2",
                            color=REFINED_COLORS["text_muted"],
                            style={"font_family": "monospace"}
                        ),
                        width="100%",
                        align_items="center"
                    ),

                    rx.divider(margin_y="3"),

                    # Información del diente seleccionado
                    rx.cond(
                        AppState.diente_seleccionado == 0,
                        # Sin diente seleccionado
                        rx.center(
                            rx.vstack(
                                rx.icon("mouse-pointer-click", size=32, color=REFINED_COLORS["text_muted"]),
                                rx.text("Seleccione un diente", size="3", color=REFINED_COLORS["text_muted"]),
                                rx.text("Haga clic en cualquier diente del odontograma", size="2", color=REFINED_COLORS["text_muted"]),
                                spacing="2",
                                align_items="center"
                            ),
                            height="200px"
                        ),
                        # Con diente seleccionado
                        panel_detalles_diente_profesional()
                    ),

                    spacing="3",
                    width="100%",
                    height="100%"
                ),
                width="35%",
                padding="4",
                style={
                    "background": "rgba(255, 255, 255, 0.02)",
                    "border_radius": RADIUS["lg"],
                    "border": f"1px solid {REFINED_COLORS['border']}",
                    "min_height": "500px"
                }
            ),

            # Panel derecho: Historial y estadísticas
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("history", size=20, color=ODONTOLOGO_COLORS["accent"]),
                        rx.text("Historial Clínico", size="3", weight="bold", color=REFINED_COLORS["text_primary"]),
                        rx.spacer(),
                        rx.text(
                            AppState.resumen_historial_diente,
                            size="2",
                            color=REFINED_COLORS["text_muted"]
                        ),
                        width="100%",
                        align_items="center"
                    ),

                    rx.divider(margin_y="3"),

                    # Historial del diente o paciente
                    panel_historial_avanzado_con_filtros(),

                    spacing="3",
                    width="100%"
                ),
                width="25%",
                padding="4",
                style={
                    "background": "rgba(255, 255, 255, 0.02)",
                    "border_radius": RADIUS["lg"],
                    "border": f"1px solid {REFINED_COLORS['border']}",
                    "min_height": "500px"
                }
            ),

            spacing="4",
            width="100%",
            align_items="start"
        ),

        spacing="4",
        width="100%",
        min_height="600px"
    )


def stats_card_mini(label: str, value: Any) -> rx.Component:
    """💹 Card de estadística mini para header"""
    return rx.box(
        rx.vstack(
            rx.text(value, size="3", weight="bold", color=ODONTOLOGO_COLORS["primary"]),
            rx.text(label, size="1", color=REFINED_COLORS["text_muted"]),
            spacing="0",
            align_items="center"
        ),
        padding="2",
        style={
            "background": "rgba(255, 255, 255, 0.03)",
            "border_radius": RADIUS["md"],
            "border": f"1px solid rgba(255, 255, 255, 0.1)",
            "min_width": "80px"
        }
    )


def odontograma_medico_profesional() -> rx.Component:
    """
    🦷 Odontograma médico profesional con 32 dientes FDI
    Versión optimizada que usa el backend BD real
    """
    return rx.vstack(
        # Cuadrantes superiores
        rx.hstack(
            # Cuadrante 2 (Superior Izquierdo)
            cuadrante_profesional(2, "Superior Izquierdo"),
            rx.spacer(),
            # Cuadrante 1 (Superior Derecho)
            cuadrante_profesional(1, "Superior Derecho"),
            width="100%",
            spacing="4"
        ),

        rx.divider(margin_y="2", border_color="rgba(255,255,255,0.1)"),

        # Cuadrantes inferiores
        rx.hstack(
            # Cuadrante 3 (Inferior Izquierdo)
            cuadrante_profesional(3, "Inferior Izquierdo"),
            rx.spacer(),
            # Cuadrante 4 (Inferior Derecho)
            cuadrante_profesional(4, "Inferior Derecho"),
            width="100%",
            spacing="4"
        ),

        spacing="2",
        width="100%"
    )


def cuadrante_profesional(numero: int, nombre: str) -> rx.Component:
    """🦷 Cuadrante profesional con dientes interactivos"""

    # Mapeo directo de cuadrantes con números FDI
    dientes_cuadrante = {
        1: [11, 12, 13, 14, 15, 16, 17, 18],  # Superior derecho
        2: [21, 22, 23, 24, 25, 26, 27, 28],  # Superior izquierdo
        3: [31, 32, 33, 34, 35, 36, 37, 38],  # Inferior izquierdo
        4: [41, 42, 43, 44, 45, 46, 47, 48]   # Inferior derecho
    }

    dientes = dientes_cuadrante.get(numero, [])

    return rx.vstack(
        # Header del cuadrante
        rx.text(
            f"Q{numero}",
            size="1",
            color=REFINED_COLORS["text_muted"],
            style={"font_family": "monospace"}
        ),

        # Dientes del cuadrante - usando números directos
        rx.hstack(
            *[diente_profesional_interactivo(num_diente) for num_diente in dientes],
            spacing="1",
            justify="center",
            wrap="wrap"
        ),

        spacing="1",
        align_items="center"
    )


def diente_profesional_interactivo(numero_diente: int) -> rx.Component:
    """🦷 Diente individual profesional con estado BD real"""
    return rx.button(
        rx.vstack(
            rx.text(
                str(numero_diente),
                size="1",
                weight="bold",
                color=rx.cond(
                    AppState.diente_seleccionado == numero_diente,
                    "white",
                    REFINED_COLORS["text_primary"]
                )
            ),
            spacing="0"
        ),
        size="1",
        width="35px",
        height="35px",
        on_click=lambda: AppState.seleccionar_diente(numero_diente),
        style={
            "background": rx.cond(
                AppState.diente_seleccionado == numero_diente,
                ODONTOLOGO_COLORS["primary"],
                AppState.obtener_color_diente(numero_diente)
            ),
            "border": rx.cond(
                AppState.diente_seleccionado == numero_diente,
                f"2px solid {ODONTOLOGO_COLORS['secondary']}",
                f"1px solid {REFINED_COLORS['border']}"
            ),
            "border_radius": RADIUS["md"],
            "cursor": "pointer",
            "_hover": {
                "transform": "scale(1.05)",
                "box_shadow": f"0 4px 20px {ODONTOLOGO_COLORS['primary']}30",
                "border": f"2px solid {ODONTOLOGO_COLORS['accent']}"
            },
            "transition": "all 0.2s ease"
        }
    )


def panel_detalles_diente_profesional() -> rx.Component:
    """📋 Panel de detalles del diente seleccionado - Versión profesional"""
    return rx.vstack(
        # Estado actual del diente
        rx.hstack(
            rx.icon("info", size=16, color=ODONTOLOGO_COLORS["secondary"]),
            rx.text("Estado Actual", size="2", weight="medium", color=REFINED_COLORS["text_primary"]),
            spacing="2"
        ),

        rx.box(
            rx.hstack(
                rx.box(
                    width="20px",
                    height="20px",
                    style={
                        "background": AppState.color_diente_actual,
                        "border_radius": RADIUS["full"],
                        "border": f"1px solid {REFINED_COLORS['border']}"
                    }
                ),
                rx.text(
                    "Estado determinado por BD",
                    size="2",
                    color=REFINED_COLORS["text_muted"]
                ),
                spacing="2",
                align_items="center"
            ),
            padding="2",
            style={
                "background": "rgba(255, 255, 255, 0.02)",
                "border_radius": RADIUS["md"]
            }
        ),

        # Cuadrante
        rx.hstack(
            rx.icon("grid-3x3", size=16, color=ODONTOLOGO_COLORS["accent"]),
            rx.text("Ubicación", size="2", weight="medium", color=REFINED_COLORS["text_primary"]),
            spacing="2"
        ),

        rx.text(
            f"Cuadrante {AppState.cuadrante_diente_seleccionado}",
            size="2",
            color=REFINED_COLORS["text_muted"]
        ),

        # Historial disponible
        rx.cond(
            AppState.historial_diente_disponible,
            rx.vstack(
                rx.hstack(
                    rx.icon("check-circle", size=16, color=COLORS["success"]["400"]),
                    rx.text("Historial Disponible", size="2", weight="medium", color=COLORS["success"]["400"]),
                    spacing="2"
                ),
                rx.text(
                    AppState.resumen_historial_diente,
                    size="2",
                    color=REFINED_COLORS["text_muted"]
                ),
                spacing="1"
            ),
            rx.hstack(
                rx.icon("x-circle", size=16, color=REFINED_COLORS["text_muted"]),
                rx.text("Sin historial registrado", size="2", color=REFINED_COLORS["text_muted"]),
                spacing="2"
            )
        ),

        spacing="3",
        width="100%",
        align_items="start"
    )


def panel_historial_avanzado_con_filtros() -> rx.Component:
    """📚 Panel de historial avanzado con filtros - Versión profesional"""
    return rx.vstack(
        # Filtros rápidos
        rx.hstack(
            rx.select(
                ["Todos", "Últimos 30 días", "Último año"],
                value="Todos",
                size="1"
            ),
            rx.button(
                rx.icon("filter", size=12),
                size="1",
                variant="soft"
            ),
            spacing="2",
            width="100%"
        ),

        rx.divider(margin_y="2"),

        # Lista de historial
        rx.scroll_area(
            rx.cond(
                AppState.historial_diente_disponible,
                # Con historial disponible
                rx.foreach(
                    AppState.historial_diente_seleccionado,
                    lambda item: entrada_historial_profesional(item)
                ),
                # Sin historial
                rx.center(
                    rx.vstack(
                        rx.icon("file-x", size=24, color=REFINED_COLORS["text_muted"]),
                        rx.text("Sin historial", size="2", color=REFINED_COLORS["text_muted"]),
                        spacing="2",
                        align_items="center"
                    ),
                    height="200px"
                )
            ),
            width="100%",
            height="300px"
        ),

        spacing="3",
        width="100%"
    )


def entrada_historial_profesional(item) -> rx.Component:
    """📝 Entrada de historial profesional con datos BD reales"""
    return rx.card(
        rx.vstack(
            # Header de la entrada
            rx.hstack(
                rx.badge(
                    item.get("procedimiento", "Procedimiento"),
                    color_scheme="cyan",
                    variant="soft",
                    size="1"
                ),
                rx.spacer(),
                rx.text(
                    item.get("fecha", "Fecha"),
                    size="1",
                    color=REFINED_COLORS["text_muted"]
                ),
                width="100%",
                align_items="center"
            ),

            # Descripción
            rx.text(
                item.get("observaciones", "Sin observaciones"),
                size="2",
                color=REFINED_COLORS["text_primary"]
            ),

            # Footer con costo y odontólogo
            rx.hstack(
                rx.hstack(
                    rx.icon("user", size=10, color=REFINED_COLORS["text_muted"]),
                    rx.text(
                        item.get("odontologo", "Dr. Sistema"),
                        size="1",
                        color=REFINED_COLORS["text_muted"]
                    ),
                    spacing="1"
                ),
                rx.spacer(),
                rx.text(
                    f"${item.get('costo_bs', 0):.2f}",
                    size="1",
                    color=COLORS["success"]["400"],
                    weight="medium"
                ),
                width="100%",
                align_items="center"
            ),

            spacing="2",
            width="100%"
        ),
        size="1",
        width="100%",
        style={"margin_bottom": "2"}
    )


# ==========================================
# 🔄 COMPONENTES DE ESTADO PROFESIONALES
# ==========================================

def loading_state_odontograma() -> rx.Component:
    """⏳ Estado de carga profesional para odontograma"""
    return rx.center(
        rx.vstack(
            rx.spinner(size="3", color=ODONTOLOGO_COLORS["primary"]),
            rx.text("Cargando historial odontológico...", size="3", color=REFINED_COLORS["text_muted"]),
            rx.text("Conectando con base de datos", size="2", color=REFINED_COLORS["text_muted"]),
            spacing="3",
            align_items="center"
        ),
        height="400px",
        width="100%",
        style={
            "background": "rgba(255, 255, 255, 0.02)",
            "border_radius": RADIUS["lg"],
            "border": f"1px solid {REFINED_COLORS['border']}"
        }
    )

def error_state_odontograma(error_message: str = "Error cargando datos") -> rx.Component:
    """❌ Estado de error profesional para odontograma"""
    return rx.center(
        rx.vstack(
            rx.icon("alert-triangle", size=32, color=COLORS["error"]["500"]),
            rx.text("Error en Historial Odontológico", size="4", weight="bold", color=COLORS["error"]["500"]),
            rx.text(error_message, size="2", color=REFINED_COLORS["text_muted"]),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("refresh-cw", size=16),
                        rx.text("Reintentar"),
                        spacing="2"
                    ),
                    size="2",
                    variant="soft",
                    color_scheme="red",
                    # on_click=lambda: AppState.cargar_historial_diente_especifico(AppState.diente_seleccionado)
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("help-circle", size=16),
                        rx.text("Ayuda"),
                        spacing="2"
                    ),
                    size="2",
                    variant="outline"
                ),
                spacing="3"
            ),
            spacing="4",
            align_items="center"
        ),
        height="400px",
        width="100%",
        style={
            "background": "rgba(244, 63, 94, 0.03)",
            "border_radius": RADIUS["lg"],
            "border": f"1px solid {COLORS['error']['500']}20"
        }
    )

def empty_state_historial() -> rx.Component:
    """📭 Estado vacío profesional para historial"""
    return rx.center(
        rx.vstack(
            rx.icon("file-x", size=32, color=REFINED_COLORS["text_muted"]),
            rx.text("Sin Historial Disponible", size="4", weight="bold", color=REFINED_COLORS["text_primary"]),
            rx.text("Este paciente no tiene intervenciones registradas", size="2", color=REFINED_COLORS["text_muted"]),
            rx.text("Seleccione un diente o paciente con historial", size="2", color=REFINED_COLORS["text_muted"]),
            spacing="3",
            align_items="center"
        ),
        height="300px",
        width="100%"
    )

def skeleton_loading_historial() -> rx.Component:
    """💀 Skeleton loading para historial"""
    return rx.vstack(
        # Simulamos 3 entradas de historial
        *[skeleton_historial_entry() for _ in range(3)],
        spacing="3",
        width="100%"
    )

def skeleton_historial_entry() -> rx.Component:
    """💀 Entrada de skeleton para historial"""
    return rx.card(
        rx.vstack(
            # Header
            rx.hstack(
                rx.box(
                    width="60px",
                    height="16px",
                    style={
                        "background": f"{REFINED_COLORS['text_muted']}20",
                        "border_radius": RADIUS["sm"],
                        "animation": "pulse 2s infinite"
                    }
                ),
                rx.spacer(),
                rx.box(
                    width="40px",
                    height="12px",
                    style={
                        "background": f"{REFINED_COLORS['text_muted']}20",
                        "border_radius": RADIUS["sm"],
                        "animation": "pulse 2s infinite"
                    }
                ),
                width="100%",
                align_items="center"
            ),
            # Contenido
            rx.box(
                width="100%",
                height="14px",
                style={
                    "background": f"{REFINED_COLORS['text_muted']}15",
                    "border_radius": RADIUS["sm"],
                    "animation": "pulse 2s infinite"
                }
            ),
            # Footer
            rx.hstack(
                rx.box(
                    width="50px",
                    height="12px",
                    style={
                        "background": f"{REFINED_COLORS['text_muted']}20",
                        "border_radius": RADIUS["sm"],
                        "animation": "pulse 2s infinite"
                    }
                ),
                rx.spacer(),
                rx.box(
                    width="30px",
                    height="12px",
                    style={
                        "background": f"{REFINED_COLORS['text_muted']}20",
                        "border_radius": RADIUS["sm"],
                        "animation": "pulse 2s infinite"
                    }
                ),
                width="100%",
                align_items="center"
            ),
            spacing="2",
            width="100%"
        ),
        size="1",
        width="100%"
    )

# Wrapper mejorado para el tab profesional con estados de carga/error
def tab_content_odontograma_profesional_with_states() -> rx.Component:
    """
    🏥 Tab profesional con manejo completo de estados
    """
    return rx.cond(
        # Estado de carga
        AppState.cargando_odontograma_historial,
        loading_state_odontograma(),

        # Estado con datos o error
        rx.cond(
            # Verificar si hay error en la carga
            AppState.paciente_actual.id == "",
            # Sin paciente seleccionado
            rx.center(
                rx.vstack(
                    rx.icon("user-x", size=32, color=REFINED_COLORS["text_muted"]),
                    rx.text("Seleccione un paciente", size="3", color=REFINED_COLORS["text_muted"]),
                    rx.text("Para ver el historial odontológico", size="2", color=REFINED_COLORS["text_muted"]),
                    spacing="2",
                    align_items="center"
                ),
                height="400px"
            ),

            # Con paciente - mostrar componente principal
            tab_content_odontograma_profesional()
        )
    )