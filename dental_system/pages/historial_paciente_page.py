"""
🏥 PÁGINA DE HISTORIAL COMPLETO DEL PACIENTE - V2.0 PROFESIONAL
==================================================================
Conectada con datos reales de Reflex.dev + Theme.py
"""

import reflex as rx
from typing import Dict, List, Any
from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout
from dental_system.styles.themes import (
    SPACING, RADIUS, DARK_THEME, COLORS, glassmorphism_card, dark_header_style
)


# ==================== COMPONENTES UI ====================

def header_paciente() -> rx.Component:
    """Header sticky con información del paciente"""
    return rx.box(
        rx.hstack(
            # Avatar y datos
            rx.hstack(
                rx.avatar(
                    fallback=rx.cond(
                        AppState.paciente_seleccionado.primer_nombre,
                        f"{AppState.paciente_seleccionado.primer_nombre[0]}{AppState.paciente_seleccionado.primer_apellido[0]}",
                        "??"
                    ),
                    size="8",
                    color_scheme="cyan",
                ),
                rx.vstack(
                    rx.heading(
                        AppState.paciente_seleccionado.nombre_completo,
                        size="6",
                        weight="bold",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    rx.hstack(
                        rx.badge(
                            AppState.paciente_seleccionado.numero_historia,
                            color_scheme="cyan",
                            variant="soft",
                        ),
                        rx.badge(
                            AppState.paciente_seleccionado.numero_documento,
                            variant="outline",
                        ),
                        rx.badge(
                            f"{AppState.paciente_seleccionado.edad} años",
                            variant="surface",
                        ),
                        spacing="2",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                spacing="4",
            ),

            rx.spacer(),

            # Acciones
            rx.hstack(
                rx.cond(
                    AppState.paciente_seleccionado.activo,
                    rx.badge("🟢 Activo", color_scheme="green", size="3"),
                    rx.badge("🔴 Inactivo", color_scheme="red", size="3")
                ),
                rx.button(
                    rx.icon("printer", size=18),
                    "Imprimir",
                    variant="soft",
                    color_scheme="gray",
                ),
                rx.button(
                    rx.icon("arrow_left", size=18),
                    "Volver",
                    variant="soft",
                    on_click=lambda: AppState.navigate_to("pacientes")
                ),
                spacing="3",
            ),

            width="100%",
            align="center",
        ),

        style={
            **glassmorphism_card(opacity="95", blur="20px"),
            "padding": SPACING["6"],
            "position": "sticky",
            "top": "0",
            "z_index": "50",
            "margin_bottom": SPACING["6"],
        }
    )


def stat_card_mini(icono: str, titulo: str, valor: str, color: str = "primary") -> rx.Component:
    """Card de estadística pequeña"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(icono, size=20, color=COLORS[color]["500"]),
                rx.text(titulo, size="2", color=DARK_THEME["colors"]["text_muted"]),
                spacing="2",
                align="center",
            ),
            rx.text(
                valor,
                size="6",
                weight="bold",
                color=DARK_THEME["colors"]["text_primary"],
            ),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        style={
            **glassmorphism_card(opacity="80", blur="10px"),
            "padding": SPACING["4"],
            "border_left": f"4px solid {COLORS[color]['500']}",
        }
    )


def info_row(label: str, value: Any) -> rx.Component:
    """Fila de información label: value"""
    return rx.hstack(
        rx.text(
            f"{label}:",
            weight="medium",
            color=DARK_THEME["colors"]["text_muted"],
            size="2",
            min_width="160px",
        ),
        rx.text(
            value,
            color=DARK_THEME["colors"]["text_primary"],
            size="2",
        ),
        spacing="4",
        width="100%",
    )


def tab_resumen() -> rx.Component:
    """Tab de resumen general"""

    # # Calcular estadísticas del paciente
    # consultas_paciente = rx.State.computed_var(
    #     lambda self: [c for c in self.lista_consultas if c.paciente_id == self.id_paciente_seleccionado]
    # )

    return rx.vstack(
        # KPIs
        rx.heading(
            "📊 Estadísticas Generales",
            size="5",
            color=DARK_THEME["colors"]["text_primary"],
            margin_bottom=SPACING["4"],
        ),
        rx.grid(
            stat_card_mini("calendar", "Consultas", "0", "primary"),  # TODO: calcular real
            stat_card_mini("activity", "Intervenciones", "0", "primary"),
            stat_card_mini("dollar_sign", "Pagado BS", "Bs. 0.00", "success"),
            stat_card_mini("dollar_sign", "Pagado USD", "$0.00", "success"),
            columns="4",
            spacing="4",
            width="100%",
        ),

        rx.divider(margin_y=SPACING["6"]),

        # Datos personales y contacto
        rx.grid(
            # Personales
            rx.box(
                rx.vstack(
                    rx.heading("👤 Datos Personales", size="4", color=DARK_THEME["colors"]["text_primary"], margin_bottom=SPACING["4"]),
                    rx.vstack(
                        info_row("Nombre Completo", AppState.paciente_seleccionado.nombre_completo),
                        info_row("Cédula", AppState.paciente_seleccionado.numero_documento),
                        info_row("Fecha Nacimiento", AppState.paciente_seleccionado.fecha_nacimiento),
                        info_row("Género", AppState.paciente_seleccionado.genero),
                        info_row("Estado Civil", AppState.paciente_seleccionado.estado_civil),
                        info_row("Ocupación", AppState.paciente_seleccionado.ocupacion),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                style={
                    **glassmorphism_card(opacity="80", blur="10px"),
                    "padding": SPACING["6"],
                }
            ),

            # Contacto
            rx.box(
                rx.vstack(
                    rx.heading("📞 Contacto", size="4", color=DARK_THEME["colors"]["text_primary"], margin_bottom=SPACING["4"]),
                    rx.vstack(
                        info_row("Teléfono", AppState.paciente_seleccionado.celular_1),
                        info_row("Email", AppState.paciente_seleccionado.email),
                        info_row("Dirección", AppState.paciente_seleccionado.direccion),

                        rx.divider(margin_y=SPACING["4"]),

                        rx.text("🚨 Contacto de Emergencia", weight="bold", color=COLORS["error"]["500"], size="3"),
                        info_row("Nombre", AppState.paciente_seleccionado.contacto_emergencia.get("nombre", "N/A")),
                        info_row("Relación", AppState.paciente_seleccionado.contacto_emergencia.get("relacion", "N/A")),
                        info_row("Teléfono", AppState.paciente_seleccionado.contacto_emergencia.get("telefono", "N/A")),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                style={
                    **glassmorphism_card(opacity="80", blur="10px"),
                    "padding": SPACING["6"],
                }
            ),

            columns="2",
            spacing="4",
            width="100%",
        ),

        spacing="4",
        width="100%",
    )


def tab_consultas() -> rx.Component:
    """Tab de historial de consultas"""
    return rx.vstack(
        rx.heading(
            "📅 Historial de Consultas",
            size="5",
            color=DARK_THEME["colors"]["text_primary"],
            margin_bottom=SPACING["4"],
        ),

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
                rx.text(
                    f"No hay consultas registradas para este paciente { AppState.historial_completo.consultas.length()}",
                    size="3",
                    color=DARK_THEME["colors"]["text_muted"]
                ),
                style={
                    **glassmorphism_card(opacity="80", blur="10px"),
                    "padding": SPACING["6"],
                    "text_align": "center"
                }
            )
        ),

        spacing="4",
        width="100%",
    )


def consulta_card(consulta) -> rx.Component:
    """Card de consulta individual"""
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
                    rx.badge(consulta.numero_consulta, color_scheme="cyan"),
                    spacing="2",
                ),

                rx.spacer(),

                rx.vstack(
                    rx.cond(
                        consulta.estado == "completada",
                        rx.badge("✅ Completada", color_scheme="green"),
                        rx.cond(
                            consulta.estado == "en_atencion",
                            rx.badge("🔄 En Atención", color_scheme="blue"),
                            rx.badge("⏳ En Espera", color_scheme="yellow")
                        )
                    ),
                    # rx.text(
                    #     f"Dr. {consulta.primer_odontologo_nombre or 'No asignado'}",
                    #     size="2",
                    #     color=DARK_THEME["colors"]["text_muted"]
                    # ),
                    spacing="1",
                    align_items="end",
                ),

                width="100%",
            ),

            rx.divider(margin_y=SPACING["3"]),

            # Detalles
            rx.vstack(
                rx.vstack(
                    rx.text("💬 Motivo:", weight="bold", color=DARK_THEME["colors"]["text_secondary"], size="2"),
                    rx.text(consulta.motivo_consulta, color=DARK_THEME["colors"]["text_muted"], size="2"),
                    spacing="1",
                    align_items="start",
                ),
            ),

            # Total (si existe)
            rx.cond(
                consulta.costo_total_usd > 0,
                rx.box(
                    rx.divider(margin_y=SPACING["3"]),
                    rx.hstack(
                        rx.text("Total Pagado:", weight="medium", color=DARK_THEME["colors"]["text_muted"]),
                        rx.text(f"Bs. {consulta.costo_total_bs:.2f}", weight="bold", color=COLORS["success"]["500"]),
                        rx.text("+", color=DARK_THEME["colors"]["text_muted"]),
                        rx.text(f"${consulta.costo_total_usd:.2f} USD", weight="bold", color=COLORS["success"]["500"]),
                        spacing="2",
                    ),
                ),
                rx.box()
            ),

            spacing="4",
            width="100%",
        ),
        style={
            **glassmorphism_card(opacity="80", blur="10px"),
            "padding": SPACING["6"],
            "border_left": f"4px solid {COLORS['primary']['500']}",
        }
    )


def tab_odontograma() -> rx.Component:
    """Tab de odontograma actual"""
    return rx.vstack(
        rx.heading(
            "🦷 Odontograma Actual",
            size="5",
            color=DARK_THEME["colors"]["text_primary"],
            margin_bottom=SPACING["4"],
        ),

        rx.box(
            rx.vstack(
                # Leyenda
                rx.hstack(
                    rx.text("Leyenda:", weight="bold", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.hstack(
                        rx.box(width="16px", height="16px", background=COLORS["success"]["400"], border_radius=RADIUS["sm"]),
                        rx.text("Sano", size="1", color=DARK_THEME["colors"]["text_muted"]),
                        spacing="1",
                    ),
                    rx.hstack(
                        rx.box(width="16px", height="16px", background=COLORS["primary"]["500"], border_radius=RADIUS["sm"]),
                        rx.text("Obturado", size="1", color=DARK_THEME["colors"]["text_muted"]),
                        spacing="1",
                    ),
                    rx.hstack(
                        rx.box(width="16px", height="16px", background="#9333EA", border_radius=RADIUS["sm"]),
                        rx.text("Endodoncia", size="1", color=DARK_THEME["colors"]["text_muted"]),
                        spacing="1",
                    ),
                    rx.hstack(
                        rx.box(width="16px", height="16px", background=COLORS["error"]["500"], border_radius=RADIUS["sm"]),
                        rx.text("Extraído", size="1", color=DARK_THEME["colors"]["text_muted"]),
                        spacing="1",
                    ),
                    rx.hstack(
                        rx.box(width="16px", height="16px", background=COLORS["gray"]["600"], border_radius=RADIUS["sm"]),
                        rx.text("Ausente", size="1", color=DARK_THEME["colors"]["text_muted"]),
                        spacing="1",
                    ),
                    spacing="4",
                    wrap="wrap",
                ),

                rx.divider(margin_y=SPACING["4"]),

                # Odontograma Grid
                rx.vstack(
                    rx.text("SUPERIORES", size="1", color=DARK_THEME["colors"]["text_muted"], weight="bold"),
                    rx.hstack(
                        odontograma_cuadrante([18, 17, 16, 15, 14, 13, 12, 11]),
                        rx.divider(orientation="vertical", height="100px"),
                        odontograma_cuadrante([21, 22, 23, 24, 25, 26, 27, 28]),
                        spacing="4",
                        align="center",
                    ),

                    rx.divider(margin_y=SPACING["4"]),

                    rx.text("INFERIORES", size="1", color=DARK_THEME["colors"]["text_muted"], weight="bold"),
                    rx.hstack(
                        odontograma_cuadrante([48, 47, 46, 45, 44, 43, 42, 41]),
                        rx.divider(orientation="vertical", height="100px"),
                        odontograma_cuadrante([38, 37, 36, 35, 34, 33, 32, 31]),
                        spacing="4",
                        align="center",
                    ),

                    spacing="4",
                    align_items="center",
                    width="100%",
                ),

                spacing="4",
                width="100%",
            ),
            style={
                **glassmorphism_card(opacity="80", blur="10px"),
                "padding": SPACING["6"],
            }
        ),

        spacing="4",
        width="100%",
    )


def odontograma_cuadrante(dientes: List[int]) -> rx.Component:
    """Cuadrante del odontograma"""
    return rx.hstack(
        *[diente_visual(d) for d in dientes],
        spacing="2",
    )


def diente_visual(numero: int) -> rx.Component:
    """Diente visual conectado con get_teeth_data"""

    # Obtener datos del diente desde AppState
    teeth_data = AppState.get_teeth_data
    diente_info = teeth_data.get(numero, {"status": "sano", "has_conditions": False})

    # Mapeo de colores por estado
    color_map = {
        "sano": COLORS["success"]["400"],
        "obturado": COLORS["primary"]["500"],
        "caries": COLORS["error"]["500"],
        "endodoncia": "#9333EA",
        "ausente": COLORS["gray"]["600"]
    }

    color = color_map.get(diente_info.get("status", "sano"), COLORS["success"]["400"])

    return rx.tooltip(
        rx.box(
            rx.text(
                str(numero),
                size="2",
                weight="bold",
                color="white",
            ),
            width="50px",
            height="60px",
            background=color,
            border_radius=RADIUS["lg"],
            border=f"2px solid {DARK_THEME['colors']['border']}",
            display="flex",
            align_items="center",
            justify_content="center",
            cursor="pointer",
            style={
                "_hover": {
                    "transform": "scale(1.1)",
                    "box_shadow": f"0 0 12px {color}",
                },
                "transition": "all 0.2s ease",
            }
        ),
        content=f"Diente {numero}: {diente_info.get('status', 'sano').upper()}",
    )


def tab_datos_medicos() -> rx.Component:
    """Tab de información médica"""
    return rx.vstack(
        rx.heading(
            "🩺 Información Médica",
            size="5",
            color=DARK_THEME["colors"]["text_primary"],
            margin_bottom=SPACING["4"],
        ),

        rx.grid(
            # Alergias
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("triangle_alert", size=20, color=COLORS["error"]["500"]),
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
                                        "padding": SPACING["3"],
                                        "border_radius": RADIUS["lg"],
                                        "border_left": f"4px solid {COLORS['error']['500']}",
                                    }
                                )
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.text("Sin alergias registradas", size="2", color=DARK_THEME["colors"]["text_muted"])
                    ),
                    spacing="4",
                    width="100%",
                ),
                style={
                    **glassmorphism_card(opacity="80", blur="10px"),
                    "padding": SPACING["6"],
                }
            ),

            # Condiciones
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
                                        "padding": SPACING["3"],
                                        "border_radius": RADIUS["lg"],
                                        "border_left": f"4px solid {COLORS['warning']['500']}",
                                    }
                                )
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.text("Sin condiciones registradas", size="2", color=DARK_THEME["colors"]["text_muted"])
                    ),
                    spacing="4",
                    width="100%",
                ),
                style={
                    **glassmorphism_card(opacity="80", blur="10px"),
                    "padding": SPACING["6"],
                }
            ),

            columns="2",
            spacing="4",
            width="100%",
        ),

        # Medicamentos
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("pill", size=20, color=COLORS["primary"]["500"]),
                    rx.heading("Medicamentos Actuales", size="4", color=COLORS["primary"]["500"]),
                    spacing="2",
                ),
                rx.cond(
                    AppState.paciente_seleccionado.medicamentos_actuales.length() > 0,
                    rx.hstack(
                        rx.foreach(
                            AppState.paciente_seleccionado.medicamentos_actuales,
                            lambda med: rx.badge(med, color_scheme="blue", variant="soft")
                        ),
                        spacing="2",
                        wrap="wrap",
                    ),
                    rx.text("Sin medicamentos registrados", size="2", color=DARK_THEME["colors"]["text_muted"])
                ),
                spacing="4",
                width="100%",
            ),
            style={
                **glassmorphism_card(opacity="80", blur="10px"),
                "padding": SPACING["6"],
            },
            margin_top=SPACING["4"],
        ),

        # Observaciones
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("file_text", size=20, color=COLORS["primary"]["500"]),
                    rx.heading("Observaciones Médicas", size="4", color=COLORS["primary"]["500"]),
                    spacing="2",
                ),
                rx.text(
                    rx.cond(AppState.paciente_seleccionado.observaciones,
                            AppState.paciente_seleccionado.observaciones,
                            "Sin observaciones médicas registradas"),
                    size="2",
                    color=DARK_THEME["colors"]["text_secondary"],
                    line_height="1.6",
                ),
                spacing="4",
                width="100%",
            ),
            style={
                **glassmorphism_card(opacity="80", blur="10px"),
                "padding": SPACING["6"],
            },
            margin_top=SPACING["4"],
        ),

        spacing="4",
        width="100%",
    )


# ==================== PÁGINA PRINCIPAL ====================

def historial_paciente_page() -> rx.Component:
    """Página completa de historial del paciente"""
    return medical_page_layout(
        rx.box(
            rx.vstack(
                # Header
                header_paciente(),

                # Tabs
                rx.box(
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                "📊 Resumen",
                                value="resumen",
                                style={"color": DARK_THEME["colors"]["text_primary"]},
                            ),
                            rx.tabs.trigger(
                                "📅 Consultas",
                                value="consultas",
                                style={"color": DARK_THEME["colors"]["text_primary"]},
                            ),
                            rx.tabs.trigger(
                                "🦷 Odontograma",
                                value="odontograma",
                                style={"color": DARK_THEME["colors"]["text_primary"]},
                            ),
                            rx.tabs.trigger(
                                "🩺 Datos Médicos",
                                value="medicos",
                                style={"color": DARK_THEME["colors"]["text_primary"]},
                            ),
                            style={
                                "border_bottom": f"1px solid {DARK_THEME['colors']['border']}",
                            }
                        ),

                        rx.box(
                            rx.tabs.content(tab_resumen(), value="resumen"),
                            rx.tabs.content(tab_consultas(), value="consultas"),
                            # rx.tabs.content(tab_odontograma(), value="odontograma"),
                            rx.tabs.content(tab_datos_medicos(), value="medicos"),
                            padding=SPACING["6"],
                        ),

                        default_value="resumen",
                    ),

                    width="100%",
                    max_width="1400px",
                    margin="0 auto",
                ),

                spacing="0",
                width="100%",
                min_height="100vh",
                padding=SPACING["6"],
            ),
            min_height="100vh",
            width="100%",
        )
    )
