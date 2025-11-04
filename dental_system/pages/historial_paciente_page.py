"""
PÁGINA DE HISTORIAL COMPLETO DEL PACIENTE - V3.0 PROFESIONAL REDISEÑADO
=========================================================================

Rediseño completo siguiendo patrones de consultas_page y personal_page:
- Uso de componentes genéricos (page_header, stat_card)
- Reutilización de theme.py y common.py
- Iconos profesionales (sin emojis)
- Tabs simplificados (2 tabs en vez de 4)
- UX/UI compacta y moderna
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import (
    medical_page_layout,
    page_header,
    stat_card,
    refresh_button
)
from dental_system.components.odontologia.professional_odontogram_grid import professional_odontogram_grid
from dental_system.styles.themes import (
    COLORS,
    SPACING,
    RADIUS,
    DARK_THEME,
    glassmorphism_card,
)


# ==========================================
# COMPONENTES HELPER
# ==========================================

def info_row(label: str, value) -> rx.Component:
    """Fila de información label: value (reutilizable)"""
    return rx.hstack(
        rx.text(
            f"{label}:",
            weight="medium",
            color=DARK_THEME["colors"]["text_muted"],
            size="2",
            min_width="140px",
        ),
        rx.text(
            value,
            color=DARK_THEME["colors"]["text_primary"],
            size="2",
        ),
        spacing="3",
        width="100%",
    )


def info_field_vertical(label: str, value) -> rx.Component:
    """Campo de información con label arriba y valor abajo"""
    return rx.vstack(
        rx.text(
            label,
            size="1",
            weight="medium",
            color=DARK_THEME["colors"]["text_muted"]
        ),
        rx.text(
            rx.cond(value,value,"No registrado"),
            size="2",
            weight="bold",
            color=DARK_THEME["colors"]["text_primary"]
        ),
        spacing="1",
        align="start",
        width="100%"
    )


# ==========================================
# HEADER COMPACTO DEL PACIENTE
# ==========================================

def patient_header_card() -> rx.Component:
    """Card compacto con datos clave del paciente + botón volver"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Datos principales del paciente
                rx.hstack(
                    rx.icon("user-circle", size=24, color=COLORS["primary"]["400"]),
                    rx.vstack(
                        rx.heading(
                            f"{AppState.paciente_seleccionado.primer_nombre} {AppState.paciente_seleccionado.segundo_nombre} {AppState.paciente_seleccionado.primer_apellido} {AppState.paciente_seleccionado.segundo_apellido}",
                            size="5",
                            weight="bold",
                            color=DARK_THEME["colors"]["text_primary"],
                        ),
                        rx.hstack(
                            rx.text(
                                f"HC: {AppState.paciente_seleccionado.numero_historia}",
                                size="2",
                                color=DARK_THEME["colors"]["text_secondary"]
                            ),
                            rx.text("|", size="2", color=DARK_THEME["colors"]["text_muted"]),
                            rx.text(
                                f"CI: {AppState.paciente_seleccionado.numero_documento}",
                                size="2",
                                color=DARK_THEME["colors"]["text_secondary"]
                            ),
                            rx.text("|", size="2", color=DARK_THEME["colors"]["text_muted"]),
                            rx.text(
                                f"{AppState.paciente_seleccionado.edad} años",
                                size="2",
                                color=DARK_THEME["colors"]["text_secondary"]
                            ),
                            spacing="2",
                            align="center"
                        ),
                        spacing="1",
                        align="start"
                    ),
                    spacing="3",
                    align="center"
                ),

                rx.spacer(),

                # Estado y acciones
                rx.hstack(
                    rx.cond(
                        AppState.paciente_seleccionado.activo,
                        rx.badge(
                            rx.hstack(
                                rx.icon("check-circle", size=14),
                                rx.text("Activo"),
                                spacing="1",
                                align="center"
                            ),
                            color_scheme="green",
                            size="2"
                        ),
                        rx.badge(
                            rx.hstack(
                                rx.icon("x-circle", size=14),
                                rx.text("Inactivo"),
                                spacing="1",
                                align="center"
                            ),
                            color_scheme="red",
                            size="2"
                        )
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("arrow-left", size=16),
                            rx.text("Volver"),
                            spacing="2",
                            align="center"
                        ),
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: AppState.navigate_to("pacientes")
                    ),
                    spacing="3",
                    align="center"
                ),

                width="100%",
                align="center"
            ),

            spacing="3",
            width="100%"
        ),
        style={
            **glassmorphism_card(opacity="90", blur="15px"),
            "padding": SPACING["4"],
            "border_left": f"4px solid {COLORS['primary']['500']}"
        }
    )


# ==========================================
# ESTADÍSTICAS DEL PACIENTE
# ==========================================

def patient_stats() -> rx.Component:
    """Estadísticas del historial usando stat_card de common.py"""
    return rx.grid(
        stat_card(
            title="Total Consultas",
            value=AppState.historial_completo.total_consultas.to_string(),
            icon="calendar-check",
            color=COLORS["primary"]["500"]
        ),
        stat_card(
            title="Intervenciones",
            value=AppState.historial_completo.total_intervenciones.to_string(),
            icon="activity",
            color=COLORS["success"]["500"]
        ),
        stat_card(
            title="Total ",
            value=AppState.historial_completo.total_pagado_usd.to_string(),
            icon="clock",
            color=COLORS["warning"]["500"]
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="3"),
        spacing="4",
        width="100%",
        margin_bottom="6"
    )


# ==========================================
# TAB 1: INFORMACIÓN COMPLETA
# ==========================================

def tab_informacion_completa() -> rx.Component:
    """Tab unificado: Datos básicos + Médicos + Odontograma"""
    return rx.vstack(
        # Sección 1: Información del paciente
        patient_info_section(),

        # Sección 2: Información médica
        medical_info_section(),

        # Sección 3: Odontograma actual
        odontogram_section(),

        spacing="4",
        width="100%"
    )


def patient_info_section() -> rx.Component:
    """Información básica y contacto del paciente en grid compacto"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("user", size=20, color=COLORS["primary"]["400"]),
                rx.text(
                    "Información del Paciente",
                    size="4",
                    weight="bold",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                spacing="2",
                align="center"
            ),

            # Grid de 4 columnas para datos compactos
            rx.grid(
                info_field_vertical("Nombre Completo", AppState.paciente_seleccionado.nombre_completo),
                info_field_vertical("Documento", AppState.paciente_seleccionado.numero_documento),
                info_field_vertical("Fecha Nacimiento", AppState.paciente_seleccionado.fecha_nacimiento),
                info_field_vertical("Género", AppState.paciente_seleccionado.genero),

                info_field_vertical("Estado Civil", AppState.paciente_seleccionado.estado_civil),
                info_field_vertical("Ocupación", AppState.paciente_seleccionado.ocupacion),
                info_field_vertical("Teléfono", AppState.paciente_seleccionado.celular_1),
                info_field_vertical("Email", AppState.paciente_seleccionado.email),

                columns="4",
                spacing="4",
                width="100%",
                margin_bottom=SPACING["3"]
            ),

            # Dirección en fila completa
            info_field_vertical("Dirección", AppState.paciente_seleccionado.direccion),

            rx.divider(margin_y=SPACING["3"]),

            # Contacto de emergencia
            rx.hstack(
                rx.icon("alert-circle", size=16, color=COLORS["error"]["400"]),
                rx.text("Contacto de Emergencia", size="3", weight="bold", color=COLORS["error"]["400"]),
                spacing="2"
            ),

            rx.grid(
                info_field_vertical("Nombre", AppState.paciente_seleccionado.contacto_emergencia["nombre"]),
                info_field_vertical("Relación", AppState.paciente_seleccionado.contacto_emergencia["relacion"]),
                info_field_vertical("Teléfono", AppState.paciente_seleccionado.contacto_emergencia["telefono"]),
                columns="3",
                spacing="4",
                width="100%"
            ),

            spacing="4",
            width="100%"
        ),
        style={
            **glassmorphism_card(opacity="80", blur="15px"),
            "padding": SPACING["5"]
        }
    )


def medical_info_section() -> rx.Component:
    """Información médica con diseño visual mejorado"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("heart-pulse", size=20, color=COLORS["error"]["400"]),
                rx.text(
                    "Información Médica",
                    size="4",
                    weight="bold",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                spacing="2",
                align="center"
            ),

            rx.grid(
                # Alergias
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("alert-triangle", size=20, color=COLORS["error"]["500"]),
                            rx.heading("Alergias", size="4", color=COLORS["error"]["500"]),
                            spacing="2",
                        ),
                        rx.cond(
                            AppState.paciente_seleccionado.alergias.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    AppState.paciente_seleccionado.alergias,
                                    lambda alergia: rx.box(
                                        rx.text(alergia, size="2", color=DARK_THEME["colors"]["text_primary"]),
                                        style={
                                            "background": f"{COLORS['error']['500']}20",
                                            "padding": SPACING["2"],
                                            "border_radius": RADIUS["md"],
                                            "border_left": f"4px solid {COLORS['error']['500']}",
                                        }
                                    )
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.text("Sin alergias registradas", size="2", color=DARK_THEME["colors"]["text_muted"])
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    style={
                        "background": f"{COLORS['error']['500']}08",
                        "padding": SPACING["4"],
                        "border_radius": RADIUS["lg"],
                        "border": f"1px solid {COLORS['error']['500']}30"
                    }
                ),

                # Condiciones Médicas
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("activity", size=20, color=COLORS["warning"]["500"]),
                            rx.heading("Condiciones", size="4", color=COLORS["warning"]["500"]),
                            spacing="2",
                        ),
                        rx.cond(
                            AppState.paciente_seleccionado.condiciones_medicas.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    AppState.paciente_seleccionado.condiciones_medicas,
                                    lambda cond: rx.box(
                                        rx.text(cond, size="2", color=DARK_THEME["colors"]["text_primary"]),
                                        style={
                                            "background": f"{COLORS['warning']['500']}20",
                                            "padding": SPACING["2"],
                                            "border_radius": RADIUS["md"],
                                            "border_left": f"4px solid {COLORS['warning']['500']}",
                                        }
                                    )
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.text("Sin condiciones registradas", size="2", color=DARK_THEME["colors"]["text_muted"])
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    style={
                        "background": f"{COLORS['warning']['500']}08",
                        "padding": SPACING["4"],
                        "border_radius": RADIUS["lg"],
                        "border": f"1px solid {COLORS['warning']['500']}30"
                    }
                ),

                # Medicamentos
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("pill", size=20, color=COLORS["primary"]["500"]),
                            rx.heading("Medicamentos", size="4", color=COLORS["primary"]["500"]),
                            spacing="2",
                        ),
                        rx.cond(
                            AppState.paciente_seleccionado.medicamentos_actuales.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    AppState.paciente_seleccionado.medicamentos_actuales,
                                    lambda med: rx.badge(med, color_scheme="blue", variant="soft", size="2")
                                ),
                                spacing="2",
                                wrap="wrap",
                            ),
                            rx.text("Sin medicamentos registrados", size="2", color=DARK_THEME["colors"]["text_muted"])
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    style={
                        "background": f"{COLORS['primary']['500']}08",
                        "padding": SPACING["4"],
                        "border_radius": RADIUS["lg"],
                        "border": f"1px solid {COLORS['primary']['500']}30"
                    }
                ),

                columns="3",
                spacing="4",
                width="100%"
            ),

            # Observaciones adicionales
            rx.cond(
                AppState.paciente_seleccionado.observaciones,
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("file-text", size=18, color=COLORS["primary"]["400"]),
                            rx.heading("Observaciones Médicas", size="4", color=COLORS["primary"]["500"]),
                            spacing="2"
                        ),
                        rx.text(
                            AppState.paciente_seleccionado.observaciones,
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"],
                            style={"line_height": "1.6"}
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    style={
                        "background": f"{COLORS['primary']['500']}08",
                        "padding": SPACING["4"],
                        "border_radius": RADIUS["lg"],
                        "border": f"1px solid {COLORS['primary']['500']}30",
                        "margin_top": SPACING["4"]
                    }
                ),
                rx.box()
            ),

            spacing="4",
            width="100%"
        ),
        style={
            **glassmorphism_card(opacity="80", blur="15px"),
            "padding": SPACING["5"]
        }
    )


def odontogram_section() -> rx.Component:
    """Odontograma actual del paciente (solo lectura)"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("scan", size=20, color=COLORS["success"]["400"]),
                rx.text(
                    "Odontograma Actual",
                    size="4",
                    weight="bold",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                spacing="2",
                align="center"
            ),

            # Odontograma con leyenda horizontal
            rx.box(
                professional_odontogram_grid(
                    selected_tooth=AppState.selected_tooth,
                    teeth_data=AppState.get_teeth_data,
                    on_tooth_click=AppState.select_tooth,
                ),
                width="100%"
            ),

            spacing="4",
            width="100%"
        ),
        style={
            **glassmorphism_card(opacity="80", blur="15px"),
            "padding": SPACING["5"]
        }
    )


# ==========================================
# TAB 2: HISTORIAL DE CONSULTAS
# ==========================================

def tab_historial_consultas() -> rx.Component:
    """Tab de historial de consultas"""
    return rx.vstack(
        rx.cond(
            AppState.historial_completo.consultas.length() > 0,
            rx.vstack(
                rx.foreach(
                    AppState.historial_completo.consultas,
                    consulta_card
                ),
                spacing="4",
                width="100%",
            ),
            rx.box(
                rx.vstack(
                    rx.icon("inbox", size=48, color=DARK_THEME["colors"]["text_muted"]),
                    rx.text(
                        "No hay consultas registradas",
                        size="3",
                        color=DARK_THEME["colors"]["text_muted"],
                        weight="medium"
                    ),
                    spacing="3",
                    align="center"
                ),
                style={
                    **glassmorphism_card(opacity="80", blur="10px"),
                    "padding": SPACING["8"],
                    "text_align": "center"
                }
            )
        ),

        spacing="4",
        width="100%",
    )


def consulta_card(consulta) -> rx.Component:
    """Card de consulta individual (mantiene diseño original mejorado)"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.hstack(
                    rx.icon("calendar", size=20, color=COLORS["primary"]["500"]),
                    rx.text(
                        consulta.fecha_llegada,
                        size="4",
                        weight="bold",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    rx.badge(
                        consulta.numero_consulta,
                        color_scheme="cyan",
                        variant="soft"
                    ),
                    spacing="2",
                    align="center"
                ),

                rx.spacer(),

                rx.cond(
                    consulta.estado == "completada",
                    rx.badge(
                        rx.hstack(
                            rx.icon("check-circle", size=14),
                            rx.text("Completada"),
                            spacing="1"
                        ),
                        color_scheme="green"
                    ),
                    rx.cond(
                        consulta.estado == "en_atencion",
                        rx.badge(
                            rx.hstack(
                                rx.icon("loader", size=14),
                                rx.text("En Atención"),
                                spacing="1"
                            ),
                            color_scheme="blue"
                        ),
                        rx.badge(
                            rx.hstack(
                                rx.icon("clock", size=14),
                                rx.text("En Espera"),
                                spacing="1"
                            ),
                            color_scheme="yellow"
                        )
                    )
                ),

                width="100%",
                align="center"
            ),

            rx.divider(margin_y=SPACING["3"]),

            # Motivo
            rx.vstack(
                rx.hstack(
                    rx.icon("message-square", size=16, color=DARK_THEME["colors"]["text_secondary"]),
                    rx.text("Motivo:", weight="bold", color=DARK_THEME["colors"]["text_secondary"], size="2"),
                    spacing="2"
                ),
                rx.text(
                    consulta.motivo_consulta,
                    color=DARK_THEME["colors"]["text_muted"],
                    size="2",
                    style={"line_height": "1.5"}
                ),
                spacing="1",
                align="start",
                width="100%"
            ),

            # Total (si existe)
            rx.cond(
                consulta.costo_total_usd > 0,
                rx.box(
                    rx.divider(margin_y=SPACING["3"]),
                    rx.hstack(
                        rx.text("Total Pagado:", weight="medium", color=DARK_THEME["colors"]["text_muted"], size="2"),
                        rx.spacer(),
                        rx.text(
                            f"Bs. {consulta.costo_total_bs:,.2f}",
                            weight="bold",
                            color=COLORS["primary"]["500"],
                            size="3"
                        ),
                        rx.text("+", color=DARK_THEME["colors"]["text_muted"]),
                        rx.text(
                            f"${consulta.costo_total_usd:.2f}",
                            weight="bold",
                            color=COLORS["success"]["500"],
                            size="3"
                        ),
                        spacing="2",
                        align="center",
                        width="100%"
                    ),
                ),
                rx.box()
            ),

            spacing="3",
            width="100%",
        ),
        style={
            **glassmorphism_card(opacity="80", blur="10px"),
            "padding": SPACING["5"],
            "border_left": f"4px solid {COLORS['primary']['500']}",
        }
    )


# ==========================================
# TABS REORGANIZADOS
# ==========================================

def historial_tabs() -> rx.Component:
    """Tabs simplificados: Info Completa + Consultas"""
    return rx.tabs.root(
        # Lista de tabs con iconos
        rx.tabs.list(
            rx.tabs.trigger(
                rx.hstack(
                    rx.icon("user-circle", size=18, color=DARK_THEME["colors"]["text_primary"]),
                    rx.text("Información Completa", color=DARK_THEME["colors"]["text_primary"]),
                    spacing="2",
                    align="center"
                ),
                value="info"
            ),
            rx.tabs.trigger(
                rx.hstack(
                    rx.icon("history", size=18, color=DARK_THEME["colors"]["text_primary"]),
                    rx.text("Historial de Consultas", color=DARK_THEME["colors"]["text_primary"]),
                    spacing="2",
                    align="center"
                ),
                value="consultas"
            ),
            style={
                "border_bottom": f"1px solid {DARK_THEME['colors']['border']}"
            }
        ),

        # Contenido Tab 1: Info Completa
        rx.tabs.content(
            tab_informacion_completa(),
            value="info"
        ),

        # Contenido Tab 2: Consultas
        rx.tabs.content(
            tab_historial_consultas(),
            value="consultas"
        ),

        default_value="info",
        width="100%"
    )


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

def historial_paciente_page() -> rx.Component:
    """
    Página de Historial del Paciente - V3.0 Profesional

    Estructura:
    1. Header profesional con page_header()
    2. Card compacto con datos del paciente
    3. Stats del paciente con stat_card()
    4. Tabs reorganizados (2 tabs en vez de 4)
    """
    return medical_page_layout(
        rx.vstack(
            # 1. Header profesional
            page_header(
                "Historial Clínico del Paciente",
                "Registro completo de atención odontológica y evolución del tratamiento",
            ),

            # 2. Card compacto con datos del paciente
            patient_header_card(),

            # 3. Stats del paciente
            patient_stats(),

            # 4. Tabs rediseñados
            rx.box(
                historial_tabs(),
                padding=SPACING["6"],
                width="100%"
            ),

            spacing="3",
            width="100%"
        )
    )
