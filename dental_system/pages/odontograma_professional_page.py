"""
🏥 PÁGINA PROFESIONAL: ODONTOGRAMA CLÍNICO
==========================================

Página de producción profesional para el odontograma clínico.
Elimina elementos de desarrollo/prueba y presenta interfaz médica limpia.

Características:
- Sin emojis ni badges de desarrollo
- Header médico con información real del paciente
- Controles contextuales según permisos
- Layout profesional con espaciado estandarizado
- Leyenda fija en sidebar
- Sistema de diseño médico ISO/WHO/ADA

Versión: 3.0 Professional Medical
Fecha: Enero 2025
Ruta: /odontograma-clinico
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.medical_odontogram_grid import medical_odontogram_page
from dental_system.styles.medical_design_system import (
    MEDICAL_COLORS,
    MEDICAL_SPACING,
    MEDICAL_TYPOGRAPHY,
    MEDICAL_SHADOWS,
    MEDICAL_RADIUS
)

# ==========================================
# 📋 HEADER MÉDICO PROFESIONAL
# ==========================================

def professional_header() -> rx.Component:
    """
    📋 Header médico profesional con información del paciente

    Incluye:
    - Datos del paciente (HC, nombre completo, edad)
    - Fecha actual y hora
    - Odontólogo responsable
    - Botón de navegación

    Returns:
        Header médico profesional
    """

    return rx.box(
        rx.hstack(
            # Información del paciente
            rx.vstack(
                rx.hstack(
                    rx.icon(
                        tag="file-text",
                        size=20,
                        color=MEDICAL_COLORS["medical_ui"]["accent_primary"]
                    ),
                    rx.heading(
                        "Odontograma Clínico",
                        size="6",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.text(
                    f"HC: {AppState.paciente_actual.numero_historia}",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                ),
                spacing="1",
                align="start"
            ),

            rx.spacer(),

            # Información contextual
            rx.vstack(
                rx.text(
                    f"{AppState.paciente_actual.primer_nombre} {AppState.paciente_actual.primer_apellido}",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["md"],
                    font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["semibold"],
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                ),
                rx.text(
                    f"Odontólogo: {AppState.nombre_usuario_display}",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                ),
                spacing="1",
                align="end"
            ),

            rx.spacer(),

            # Navegación
            rx.button(
                rx.hstack(
                    rx.icon(tag="arrow-left", size=18),
                    rx.text("Volver", font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"]),
                    spacing="2"
                ),
                size="2",
                variant="outline",
                color_scheme="gray",
                on_click=lambda: rx.redirect("/dashboard")
            ),

            spacing="4",
            align="center",
            width="100%"
        ),

        # Estilos del header
        padding=MEDICAL_SPACING["lg"],
        background=MEDICAL_COLORS["medical_ui"]["surface"],
        border_bottom=f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
        box_shadow=MEDICAL_SHADOWS["xs"],
        width="100%"
    )


# ==========================================
# 🚨 ALERTAS MÉDICAS (SI EXISTEN)
# ==========================================

def medical_alerts() -> rx.Component:
    """
    🚨 Alertas médicas importantes del paciente

    Muestra alergias, condiciones especiales, medicamentos, etc.

    Returns:
        Componente de alertas médicas
    """

    return rx.cond(
        # Verificar si hay alertas médicas
        AppState.paciente_actual.tiene_alertas_medicas,
        rx.box(
            rx.hstack(
                rx.icon(
                    tag="triangle-alert",
                    size=20,
                    color=MEDICAL_COLORS["medical_ui"]["accent_warning"]
                ),
                rx.vstack(
                    rx.text(
                        "Alertas Médicas Importantes",
                        font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["semibold"],
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    rx.text(
                        rx.cond(
                            AppState.paciente_actual.alergias_medicamentos,
                            AppState.paciente_actual.alergias_medicamentos,
                            "Ver historial médico completo"
                        ),
                        font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                    ),
                    spacing="1",
                    align="start"
                ),
                spacing="3",
                align="center"
            ),
            style={
                "background": f"{MEDICAL_COLORS['medical_ui']['accent_warning']}10",
                "border": f"1px solid {MEDICAL_COLORS['medical_ui']['accent_warning']}",
                "border_radius": MEDICAL_RADIUS["md"],
                "padding": MEDICAL_SPACING["md"],
                "margin_bottom": MEDICAL_SPACING["md"]
            }
        )
    )


# ==========================================
# 📊 ESTADÍSTICAS RÁPIDAS
# ==========================================

def quick_stats() -> rx.Component:
    """
    📊 Estadísticas rápidas del odontograma

    Muestra:
    - Dientes sanos
    - Dientes con condiciones
    - Condiciones críticas
    - Último tratamiento

    Returns:
        Componente de estadísticas rápidas
    """

    def stat_card(icon: str, label: str, value: str, color: str) -> rx.Component:
        """Card individual de estadística"""
        return rx.box(
            rx.vstack(
                rx.icon(tag=icon, size=24, color=color),
                rx.text(
                    value,
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["lg"],
                    font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["bold"],
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                ),
                rx.text(
                    label,
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["xs"],
                    color=MEDICAL_COLORS["medical_ui"]["text_muted"],
                    text_align="center"
                ),
                spacing="1",
                align="center"
            ),
            style={
                "background": MEDICAL_COLORS["medical_ui"]["surface"],
                "border": f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
                "border_radius": MEDICAL_RADIUS["md"],
                "padding": MEDICAL_SPACING["md"],
                "min_width": "120px",
                "text_align": "center"
            }
        )

    return rx.hstack(
        stat_card(
            "circle-check",
            "Dientes Sanos",
            AppState.estadisticas_resumen["dientes_sanos"],
            MEDICAL_COLORS["medical_ui"]["accent_success"]
        ),
        stat_card(
            "clipboard",
            "Con Condiciones",
            AppState.estadisticas_resumen["dientes_afectados"],
            MEDICAL_COLORS["medical_ui"]["accent_info"]
        ),
        stat_card(
            "circle-alert",
            "Críticos",
            AppState.estadisticas_resumen["condiciones_criticas"],
            MEDICAL_COLORS["medical_ui"]["accent_error"]
        ),
        stat_card(
            "activity",
            "Última Intervención",
            rx.cond(
                AppState.ultima_intervencion_fecha == "today",
                "Hoy",
                "Ver historial"
            ),
            MEDICAL_COLORS["medical_ui"]["accent_primary"]
        ),
        spacing="3",
        width="100%",
        padding=MEDICAL_SPACING["md"]
    )


# ==========================================
# 🏥 PÁGINA PRINCIPAL PROFESIONAL
# ==========================================

def odontograma_professional_page() -> rx.Component:
    """
    🏥 Página principal profesional del odontograma clínico

    Layout completo:
    - Header médico con info paciente
    - Alertas médicas (si existen)
    - Estadísticas rápidas
    - Grid del odontograma con leyenda
    - Modal de condiciones

    Returns:
        Página completa profesional
    """

    return rx.box(
        # Header profesional
        professional_header(),

        # Contenido principal
        rx.box(
            rx.vstack(
                # Alertas médicas importantes
                medical_alerts(),

                # Estadísticas rápidas
                quick_stats(),

                # Grid del odontograma (incluye todo el sistema)
                medical_odontogram_page(),

                spacing="6",  # Reflex scale: 6 = 24px
                width="100%",
                height="100%"
            ),

            width="100%",
            height="calc(100vh - 80px)",
            overflow="auto"
        ),

        # Estilos del contenedor principal
        width="100%",
        height="100vh",
        background=MEDICAL_COLORS["medical_ui"]["background"],
        overflow="hidden"
    )


# ==========================================
# 🎯 EXPORTS
# ==========================================

__all__ = ["odontograma_professional_page"]