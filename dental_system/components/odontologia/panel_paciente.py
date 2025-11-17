"""
🏥 PANEL DE INFORMACIÓN DEL PACIENTE - VERSIÓN COMPACTA V2.1
=============================================================

Panel lateral simplificado y profesional:
- ✨ Sin avatar innecesario
- 🎨 Usa tema global del proyecto (COLORS de themes.py)
- 💎 Iconos profesionales (sin emojis)
- 📊 Siempre visible (sin toggle de colapsar)
- 📱 Layout compacto y responsive
- 💊 Información médica completa (alergias + medicamentos + condición)
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, DARK_THEME, GRADIENTS, dark_crystal_card
)


# ==========================================
# 🧩 COMPONENTES AUXILIARES COMPACTOS
# ==========================================

def info_item_compact(icon: str, label: str, value: rx.Var, show_empty: bool = False) -> rx.Component:
    """📋 Item de información compacto (inline)"""
    return rx.hstack(
        rx.icon(icon, size=16, color=COLORS["primary"]["400"]),
        rx.text(
            f"{label}:",
            size="3",
            color=COLORS["gray"]["400"],
            weight="medium"
        ),
        rx.text(
            value,
            size="3",
            weight="bold",
            color=COLORS["gray"]["100"]
        ),
        spacing="2",
        align="center"
    )


def seccion_header(icon: str, titulo: str, color: str = None) -> rx.Component:
    """🏷️ Header de sección con icono"""
    final_color = color if color else COLORS["primary"]["400"]

    return rx.hstack(
        rx.icon(icon, size=18, color=final_color),
        rx.text(
            titulo,
            size="4",
            weight="bold",
            color=COLORS["gray"]["100"]
        ),
        spacing="2",
        align="center",
        margin_bottom=SPACING["3"]
    )


def separador_sutil() -> rx.Component:
    """━━━ Separador visual sutil"""
    return rx.box(
        width="100%",
        height="1px",
        background=f"linear-gradient(90deg, transparent 0%, {COLORS['gray']['700']}80 50%, transparent 100%)",
        margin_y=SPACING["4"]
    )


# ==========================================
# 📋 SECCIONES PRINCIPALES
# ==========================================

def seccion_datos_principales() -> rx.Component:
    """👤 Datos principales del paciente (compacto)"""
    return rx.vstack(
        # Nombre principal con icono
        rx.hstack(
            rx.icon("user", size=22, color=COLORS["primary"]["400"]),
            rx.vstack(
                rx.text(
                    AppState.paciente_actual.nombre_completo,
                    style={
                        "font_size": "1.5rem",
                        "font_weight": "800",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent",
                        "line_height": "1.2"
                    }
                ),

                # HC y CI inline
                rx.hstack(
                    rx.text(
                        f"HC: {AppState.paciente_actual.numero_historia}",
                        size="3",
                        color=COLORS["gray"]["400"],
                        weight="medium"
                    ),
                    rx.text("•", size="2", color=COLORS["gray"]["600"]),
                    rx.text(
                        AppState.paciente_actual.numero_documento,
                        size="3",
                        color=COLORS["gray"]["400"],
                        weight="medium"
                    ),
                    spacing="2",
                    align="center"
                ),

                spacing="1",
                align="start"
            ),
            spacing="3",
            align="start",
            width="100%"
        ),

        spacing="3",
        width="100%"
    )


def seccion_datos_basicos() -> rx.Component:
    """📋 Datos básicos del paciente"""
    return rx.vstack(
        seccion_header("clipboard-list", "Datos Básicos"),

        # Edad y género (inline)
        rx.hstack(
            info_item_compact(
                "calendar",
                "Edad",
                rx.cond(
                    AppState.paciente_actual.fecha_nacimiento,
                    AppState.paciente_actual.edad.to_string() + " años",
                    "No especificada"
                )
            ),
            rx.text("•", size="2", color=COLORS["gray"]["600"]),
            info_item_compact(
                "user",
                "Género",
                rx.cond(
                    AppState.paciente_actual.genero != "",
                    AppState.paciente_actual.genero,
                    "No especificado"
                )
            ),
            spacing="2",
            wrap="wrap",
            width="100%"
        ),

        # Teléfono
        info_item_compact(
            "phone",
            "Teléfono",
            rx.cond(
                AppState.paciente_actual.celular_1 != "",
                AppState.paciente_actual.celular_1,
                "No registrado"
            )
        ),

        # Email (condicional)
        rx.cond(
            AppState.paciente_actual.email != "",
            info_item_compact(
                "mail",
                "Email",
                AppState.paciente_actual.email
            )
        ),

        spacing="3",
        width="100%"
    )


def seccion_alertas_medicas() -> rx.Component:
    """🚨 Alertas médicas críticas (solo si hay alergias)"""
    return rx.cond(
        AppState.paciente_actual.alergias.length() > 0,
        rx.box(
            rx.vstack(
                seccion_header("alert-triangle", "ALERTAS MÉDICAS", color=COLORS["error"]["300"]),
                # Lista de alergias
                rx.vstack(
                    rx.foreach(
                        AppState.paciente_actual.alergias,
                        lambda alergia: rx.hstack(
                            rx.icon("circle", size=8, color=COLORS["error"]["400"]),
                            rx.text(
                                alergia,
                                size="3",
                                color=COLORS["error"]["300"],
                                weight="medium"
                            ),
                            spacing="2",
                            align="center"
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),

                spacing="3",
                width="100%"
            ),
            style={
                "padding": SPACING["4"],
                "background": f"{COLORS['error']['500']}10",
                "border": f"1px solid {COLORS['error']['500']}40",
                "border_radius": RADIUS["lg"],
                "border_left": f"4px solid {COLORS['error']['500']}"
            }
        )
    )


def seccion_medicamentos() -> rx.Component:
    """💊 Medicamentos actuales del paciente"""
    return rx.cond(
        AppState.paciente_actual.medicamentos_actuales.length() > 0,
        rx.box(
            rx.vstack(
                seccion_header("pill", "MEDICAMENTOS ACTUALES", COLORS["primary"]["500"]),

                # Lista de medicamentos
                rx.vstack(
                    rx.foreach(
                        AppState.paciente_actual.medicamentos_actuales,
                        lambda med: rx.hstack(
                            rx.icon("circle", size=8, color=COLORS["primary"]["500"]),
                            rx.text(
                                med,
                                size="3",
                                color=COLORS["gray"]["200"],
                                weight="medium"
                            ),
                            spacing="2",
                            align="center"
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),

                spacing="2",
                width="100%"
            ),
            style={
                "padding": SPACING["4"],
                "background": f"{COLORS['primary']['500']}10",
                "border": f"1px solid {COLORS['primary']['500']}40",
                "border_radius": RADIUS["lg"],
                "border_left": f"4px solid {COLORS['primary']['500']}"
            }
        )
    )


def seccion_condicion_medica() -> rx.Component:
    """🏥 Condición médica general"""
    return rx.cond(
        AppState.paciente_actual.condiciones_medicas.length() > 0,
        rx.box(
            rx.vstack(
                seccion_header("heart-pulse", "CONDICIÓN MÉDICA", COLORS["warning"]["400"]),
                rx.vstack(
                    rx.foreach(
                        AppState.paciente_actual.condiciones_medicas,
                        lambda condicion: rx.hstack(
                            rx.icon("circle", size=8, color=COLORS["warning"]["400"]),
                            rx.text(
                                condicion,
                                size="3",
                                color=COLORS["warning"]["300"],
                                weight="medium"
                            ),
                            spacing="2",
                            align="center"
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),
                spacing="2",
                width="100%"
            ),
            style={
                "padding": SPACING["4"],
                "background": f"{COLORS['warning']['400']}10",
                "border": f"1px solid {COLORS['warning']['400']}40",
                "border_radius": RADIUS["lg"],
                "border_left": f"4px solid {COLORS['warning']['400']}"
            }
        )
        
    )


def seccion_estadisticas_consulta() -> rx.Component:
    """📊 Estadísticas y consulta actual (compacto inline)"""
    return rx.vstack(
        seccion_header("activity", "Actividad"),

        # Estadísticas inline
        rx.hstack(
            rx.vstack(
                rx.text(
                    AppState.total_visitas_paciente_actual.to(str),
                    size="7",
                    weight="bold",
                    color=COLORS["primary"]["400"]
                ),
                rx.text(
                    "Visitas",
                    size="2",
                    color=COLORS["gray"]["500"]
                ),
                spacing="0",
                align="center"
            ),

            rx.box(
                width="1px",
                height="45px",
                background=COLORS["gray"]["700"]
            ),

            rx.vstack(
                rx.text(
                    "0",
                    size="7",
                    weight="bold",
                    color=COLORS["warning"]["400"]
                ),
                rx.text(
                    "Pendientes",
                    size="2",
                    color=COLORS["gray"]["500"]
                ),
                spacing="0",
                align="center"
            ),

            spacing="5",
            justify="center",
            width="100%"
        ),

        separador_sutil(),

        # Consulta actual
        seccion_header("clipboard-check", "Consulta Actual", COLORS["success"]["400"]),

        info_item_compact(
            "hash",
            "N° Consulta",
            AppState.consulta_actual.numero_consulta
        ),

        info_item_compact(
            "calendar",
            "Fecha",
            AppState.consulta_actual.fecha_llegada.split("T")[0]
        ),

        spacing="3",
        width="100%"
    )


# ==========================================
# 📋 COMPONENTE PRINCIPAL
# ==========================================

def panel_informacion_paciente() -> rx.Component:
    """
    🏥 PANEL DE INFORMACIÓN DEL PACIENTE V2.1 - COMPACTO Y PROFESIONAL

    ✨ CARACTERÍSTICAS:
    - Sin avatar innecesario
    - Usa tema global (COLORS)
    - Iconos profesionales (sin emojis)
    - Siempre visible (sin toggle)
    - Layout compacto
    - Información médica completa (alergias + medicamentos + condición)
    """
    return rx.box(
        rx.vstack(
            # Header simple (tamaño aumentado)
            rx.hstack(
                rx.icon("user-check", size=20, color=COLORS["primary"]["400"]),
                rx.text(
                    "Información del Paciente",
                    size="5",
                    weight="bold",
                    color=COLORS["gray"]["100"]
                ),
                spacing="2",
                align="center",
                margin_bottom=SPACING["4"]
            ),

            # Datos principales
            seccion_datos_principales(),

            separador_sutil(),

            # Datos básicos
            seccion_datos_basicos(),

            separador_sutil(),

            # Alertas médicas (condicional)
            seccion_alertas_medicas(),

            # Separador solo si hay alertas
            rx.cond(
                AppState.paciente_actual.alergias.length() > 0,
                separador_sutil()
            ),

            # NUEVO: Medicamentos actuales
            seccion_medicamentos(),

            # Separador solo si hay medicamentos
            rx.cond(
                AppState.paciente_actual.medicamentos_actuales.length() > 0,
                separador_sutil()
            ),

            # NUEVO: Condición médica general
            seccion_condicion_medica(),

            # Separador solo si hay condición médica
            rx.cond(
                AppState.paciente_actual.medicamentos_actuales != "",
                separador_sutil()
            ),

            # Estadísticas y consulta actual
            seccion_estadisticas_consulta(),

            spacing="0",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%",
        height="fit-content"
    )
