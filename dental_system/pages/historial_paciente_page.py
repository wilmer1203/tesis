"""
📋 PÁGINA DE HISTORIAL COMPLETO DEL PACIENTE - Mockup Profesional
============================================================
Diseñada usando los componentes y estilos del proyecto
"""

import reflex as rx
from typing import Dict, List
from dental_system.styles.themes import (
    SPACING, RADIUS, DARK_THEME, COLORS, glassmorphism_card
)


# ==================== DATOS ESTÁTICOS MOCKUP ====================

PACIENTE_MOCKUP = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "numero_historia": "HC-0023",
    "primer_nombre": "Juan Carlos",
    "segundo_nombre": "Alberto",
    "primer_apellido": "Pérez",
    "segundo_apellido": "González",
    "cedula": "V-12345678",
    "fecha_nacimiento": "1985-03-15",
    "edad": 39,
    "genero": "Masculino",
    "telefono": "+58 414-1234567",
    "email": "juan.perez@email.com",
    "direccion": "Av. Principal, Urb. Los Médanos, Casa 45, Cumaná, Edo. Sucre",
    "estado_civil": "Casado",
    "ocupacion": "Ingeniero Civil",
    "estado": "activo",
    "created_at": "2023-01-10",
    "tipo_sangre": "O+",
    "alergias": ["Penicilina", "Anestesia con epinefrina"],
    "condiciones_preexistentes": ["Diabetes tipo 2 controlada", "Hipertensión arterial"],
    "medicamentos_actuales": ["Metformina 850mg", "Losartán 50mg"],
    "observaciones_medicas": "Paciente requiere profilaxis antibiótica antes de procedimientos invasivos. Control glicémico estable.",
    "contacto_emergencia_nombre": "María González",
    "contacto_emergencia_relacion": "Esposa",
    "contacto_emergencia_telefono": "+58 424-7654321",
}

CONSULTAS_MOCKUP = [
    {
        "id": "c1",
        "numero_consulta": "C-0156",
        "fecha_consulta": "2024-10-20",
        "hora_inicio": "09:30",
        "hora_fin": "10:45",
        "motivo_consulta": "Control rutinario + dolor molar inferior derecho",
        "diagnostico": "Caries profunda en diente 46, gingivitis leve generalizada",
        "estado": "completada",
        "odontologo": "Dra. Carmen Rodríguez",
        "intervenciones": [
            {
                "tipo": "Obturación con resina",
                "dientes": ["46"],
                "superficies": ["Oclusal", "Distal"],
                "descripcion": "Eliminación de tejido cariado y obturación con resina fotopolimerizable color A2",
                "material": "Resina compuesta Filtek Z350",
                "duracion": "45 min",
                "servicios": ["Obturación dental", "Anestesia local"]
            },
            {
                "tipo": "Profilaxis dental",
                "dientes": ["Todas las piezas"],
                "superficies": [],
                "descripcion": "Limpieza profunda con ultrasonido y pulido dental",
                "material": "Pasta profiláctica",
                "duracion": "30 min",
                "servicios": ["Limpieza dental profesional"]
            }
        ],
        "total_pagado_bs": 180.00,
        "total_pagado_usd": 5.00,
    },
    {
        "id": "c2",
        "numero_consulta": "C-0098",
        "fecha_consulta": "2024-07-15",
        "hora_inicio": "14:00",
        "hora_fin": "15:30",
        "motivo_consulta": "Extracción de muela de juicio",
        "diagnostico": "Tercer molar inferior derecho impactado con dolor recurrente",
        "estado": "completada",
        "odontologo": "Dr. Luis Martínez",
        "intervenciones": [
            {
                "tipo": "Exodoncia quirúrgica",
                "dientes": ["48"],
                "superficies": [],
                "descripcion": "Extracción quirúrgica de tercer molar inferior derecho impactado. Osteotomía y odontosección realizada.",
                "material": "Sutura reabsorbible 3-0",
                "duracion": "60 min",
                "servicios": ["Extracción quirúrgica", "Anestesia infiltrativa", "Sutura"]
            }
        ],
        "total_pagado_bs": 250.00,
        "total_pagado_usd": 0.00,
    },
    {
        "id": "c3",
        "numero_consulta": "C-0045",
        "fecha_consulta": "2024-03-10",
        "hora_inicio": "10:00",
        "hora_fin": "11:00",
        "motivo_consulta": "Revisión general y limpieza",
        "diagnostico": "Salud oral estable, sin hallazgos patológicos",
        "estado": "completada",
        "odontologo": "Dra. Carmen Rodríguez",
        "intervenciones": [
            {
                "tipo": "Profilaxis dental",
                "dientes": ["Todas las piezas"],
                "superficies": [],
                "descripcion": "Limpieza dental de rutina con ultrasonido",
                "material": "Pasta profiláctica con flúor",
                "duracion": "40 min",
                "servicios": ["Limpieza dental profesional", "Aplicación de flúor"]
            }
        ],
        "total_pagado_bs": 80.00,
        "total_pagado_usd": 0.00,
    },
]

ODONTOGRAMA_ACTUAL_MOCKUP = {
    # Cuadrante 1
    "18": {"estado": "ausente", "color": COLORS["gray"]["600"]},
    "17": {"estado": "sano", "color": COLORS["success"]["400"]},
    "16": {"estado": "sano", "color": COLORS["success"]["400"]},
    "15": {"estado": "sano", "color": COLORS["success"]["400"]},
    "14": {"estado": "sano", "color": COLORS["success"]["400"]},
    "13": {"estado": "sano", "color": COLORS["success"]["400"]},
    "12": {"estado": "sano", "color": COLORS["success"]["400"]},
    "11": {"estado": "sano", "color": COLORS["success"]["400"]},
    # Cuadrante 2
    "21": {"estado": "sano", "color": COLORS["success"]["400"]},
    "22": {"estado": "sano", "color": COLORS["success"]["400"]},
    "23": {"estado": "sano", "color": COLORS["success"]["400"]},
    "24": {"estado": "sano", "color": COLORS["success"]["400"]},
    "25": {"estado": "sano", "color": COLORS["success"]["400"]},
    "26": {"estado": "endodoncia", "color": "#9333EA"},
    "27": {"estado": "sano", "color": COLORS["success"]["400"]},
    "28": {"estado": "ausente", "color": COLORS["gray"]["600"]},
    # Cuadrante 3
    "38": {"estado": "ausente", "color": COLORS["gray"]["600"]},
    "37": {"estado": "sano", "color": COLORS["success"]["400"]},
    "36": {"estado": "sano", "color": COLORS["success"]["400"]},
    "35": {"estado": "sano", "color": COLORS["success"]["400"]},
    "34": {"estado": "sano", "color": COLORS["success"]["400"]},
    "33": {"estado": "sano", "color": COLORS["success"]["400"]},
    "32": {"estado": "sano", "color": COLORS["success"]["400"]},
    "31": {"estado": "sano", "color": COLORS["success"]["400"]},
    # Cuadrante 4
    "41": {"estado": "sano", "color": COLORS["success"]["400"]},
    "42": {"estado": "sano", "color": COLORS["success"]["400"]},
    "43": {"estado": "sano", "color": COLORS["success"]["400"]},
    "44": {"estado": "sano", "color": COLORS["success"]["400"]},
    "45": {"estado": "sano", "color": COLORS["success"]["400"]},
    "46": {"estado": "obturado", "color": COLORS["primary"]["500"]},
    "47": {"estado": "sano", "color": COLORS["success"]["400"]},
    "48": {"estado": "extraido", "color": COLORS["error"]["500"]},
}

ESTADISTICAS_MOCKUP = {
    "total_consultas": 3,
    "total_intervenciones": 4,
    "total_pagado_bs": 510.00,
    "total_pagado_usd": 5.00,
}


# ==================== COMPONENTES UI ====================

def header_paciente() -> rx.Component:
    """Header sticky con información del paciente"""
    return rx.box(
        rx.hstack(
            # Avatar y datos
            rx.hstack(
                rx.avatar(
                    fallback=f"{PACIENTE_MOCKUP['primer_nombre'][0]}{PACIENTE_MOCKUP['primer_apellido'][0]}",
                    size="8",
                    color_scheme="cyan",
                ),
                rx.vstack(
                    rx.heading(
                        f"{PACIENTE_MOCKUP['primer_nombre']} {PACIENTE_MOCKUP['primer_apellido']}",
                        size="6",
                        weight="bold",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    rx.hstack(
                        rx.badge(
                            PACIENTE_MOCKUP["numero_historia"],
                            color_scheme="cyan",
                            variant="soft",
                        ),
                        rx.badge(
                            PACIENTE_MOCKUP["cedula"],
                            variant="outline",
                        ),
                        rx.badge(
                            f"{PACIENTE_MOCKUP['edad']} años",
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
                rx.badge(
                    "🟢 Activo",
                    color_scheme="green",
                    size="3",
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
                rx.icon(icono, size=20, color=f"{color}.500"),
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


def info_row(label: str, value: str) -> rx.Component:
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
    return rx.vstack(
        # KPIs
        rx.heading(
            "📊 Estadísticas Generales",
            size="5",
            color=DARK_THEME["colors"]["text_primary"],
            margin_bottom=SPACING["4"],
        ),
        rx.grid(
            stat_card_mini("calendar", "Consultas", str(ESTADISTICAS_MOCKUP["total_consultas"]), "primary"),
            stat_card_mini("activity", "Intervenciones", str(ESTADISTICAS_MOCKUP["total_intervenciones"]), "blue"),
            stat_card_mini("dollar_sign", "Pagado BS", f"Bs. {ESTADISTICAS_MOCKUP['total_pagado_bs']:.2f}", "success"),
            stat_card_mini("dollar_sign", "Pagado USD", f"${ESTADISTICAS_MOCKUP['total_pagado_usd']:.2f}", "success"),
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
                        info_row("Nombre Completo", f"{PACIENTE_MOCKUP['primer_nombre']} {PACIENTE_MOCKUP['segundo_nombre']} {PACIENTE_MOCKUP['primer_apellido']} {PACIENTE_MOCKUP['segundo_apellido']}"),
                        info_row("Cédula", PACIENTE_MOCKUP["cedula"]),
                        info_row("Fecha Nacimiento", PACIENTE_MOCKUP["fecha_nacimiento"]),
                        info_row("Género", PACIENTE_MOCKUP["genero"]),
                        info_row("Estado Civil", PACIENTE_MOCKUP["estado_civil"]),
                        info_row("Ocupación", PACIENTE_MOCKUP["ocupacion"]),
                        info_row("Tipo Sangre", PACIENTE_MOCKUP["tipo_sangre"]),
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
                        info_row("Teléfono", PACIENTE_MOCKUP["telefono"]),
                        info_row("Email", PACIENTE_MOCKUP["email"]),
                        info_row("Dirección", PACIENTE_MOCKUP["direccion"]),

                        rx.divider(margin_y=SPACING["4"]),

                        rx.text("🚨 Contacto de Emergencia", weight="bold", color=COLORS["error"]["500"], size="3"),
                        info_row("Nombre", PACIENTE_MOCKUP["contacto_emergencia_nombre"]),
                        info_row("Relación", PACIENTE_MOCKUP["contacto_emergencia_relacion"]),
                        info_row("Teléfono", PACIENTE_MOCKUP["contacto_emergencia_telefono"]),
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

        rx.vstack(
            *[consulta_card(consulta) for consulta in CONSULTAS_MOCKUP],
            spacing="4",
            width="100%",
        ),

        spacing="4",
        width="100%",
    )


def consulta_card(consulta: Dict) -> rx.Component:
    """Card de consulta individual"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.hstack(
                    rx.icon("calendar", size=20, color=COLORS["primary"]["500"]),
                    rx.text(
                        consulta["fecha_consulta"],
                        size="4",
                        weight="bold",
                        color=DARK_THEME["colors"]["text_primary"],
                    ),
                    rx.badge(consulta["numero_consulta"], color_scheme="cyan"),
                    spacing="2",
                ),

                rx.spacer(),

                rx.vstack(
                    rx.badge("✅ Completada", color_scheme="green"),
                    rx.text(consulta["odontologo"], size="2", color=DARK_THEME["colors"]["text_muted"]),
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
                    rx.text(consulta["motivo_consulta"], color=DARK_THEME["colors"]["text_muted"], size="2"),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("🔍 Diagnóstico:", weight="bold", color=DARK_THEME["colors"]["text_secondary"], size="2"),
                    rx.text(consulta["diagnostico"], color=DARK_THEME["colors"]["text_muted"], size="2"),
                    spacing="1",
                    align_items="start",
                ),
                spacing="3",
                width="100%",
            ),

            # Intervenciones
            rx.vstack(
                rx.text("🦷 Intervenciones:", weight="bold", color=COLORS["primary"]["500"], size="3", margin_top=SPACING["3"]),
                rx.vstack(
                    *[intervencion_mini(interv) for interv in consulta["intervenciones"]],
                    spacing="3",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),

            # Total
            rx.divider(margin_y=SPACING["3"]),
            rx.hstack(
                rx.text("Total Pagado:", weight="medium", color=DARK_THEME["colors"]["text_muted"]),
                rx.text(f"Bs. {consulta['total_pagado_bs']:.2f}", weight="bold", color=COLORS["success"]["500"]),
                rx.text("+", color=DARK_THEME["colors"]["text_muted"]),
                rx.text(f"${consulta['total_pagado_usd']:.2f} USD", weight="bold", color=COLORS["success"]["500"]),
                spacing="2",
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


def intervencion_mini(intervencion: Dict) -> rx.Component:
    """Intervención mini dentro de consulta"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("zap", size=16, color=COLORS["warning"]["500"]),
                rx.text(intervencion["tipo"], weight="bold", color=DARK_THEME["colors"]["text_primary"], size="2"),
                rx.badge(f"⏱️ {intervencion['duracion']}", size="1", variant="soft"),
                spacing="2",
            ),

            rx.cond(
                len(intervencion["dientes"]) > 0,
                rx.hstack(
                    rx.text("Dientes:", size="1", color=DARK_THEME["colors"]["text_muted"]),
                    rx.hstack(
                        *[rx.badge(d, size="1", color_scheme="purple") for d in intervencion["dientes"]],
                        spacing="1",
                    ),
                    spacing="2",
                ),
                rx.box(),
            ),

            rx.text(intervencion["descripcion"], size="2", color=DARK_THEME["colors"]["text_muted"]),

            spacing="2",
            width="100%",
        ),
        style={
            "background": DARK_THEME["colors"]["surface_secondary"],
            "padding": SPACING["4"],
            "border_radius": RADIUS["lg"],
            "border_left": f"3px solid {COLORS['warning']['500']}",
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
        *[diente_visual(str(d)) for d in dientes],
        spacing="2",
    )


def diente_visual(numero: str) -> rx.Component:
    """Diente visual"""
    diente_data = ODONTOGRAMA_ACTUAL_MOCKUP.get(numero, {"estado": "sano", "color": COLORS["success"]["400"]})

    return rx.tooltip(
        rx.box(
            rx.text(
                numero,
                size="2",
                weight="bold",
                color="white",
            ),
            width="50px",
            height="60px",
            background=diente_data["color"],
            border_radius=RADIUS["lg"],
            border=f"2px solid {DARK_THEME['colors']['border']}",
            display="flex",
            align_items="center",
            justify_content="center",
            cursor="pointer",
            style={
                "_hover": {
                    "transform": "scale(1.1)",
                    "box_shadow": f"0 0 12px {diente_data['color']}",
                },
                "transition": "all 0.2s ease",
            }
        ),
        content=f"Diente {numero}: {diente_data['estado'].upper()}",
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
                    rx.vstack(
                        *[
                            rx.box(
                                rx.text(alergia, size="2", color=DARK_THEME["colors"]["text_primary"]),
                                style={
                                    "background": f"{COLORS['error']['500']}20",
                                    "padding": SPACING["3"],
                                    "border_radius": RADIUS["lg"],
                                    "border_left": f"4px solid {COLORS['error']['500']}",
                                }
                            )
                            for alergia in PACIENTE_MOCKUP["alergias"]
                        ],
                        spacing="2",
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

            # Condiciones
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("activity", size=20, color=COLORS["warning"]["500"]),
                        rx.heading("Condiciones", size="4", color=COLORS["warning"]["500"]),
                        spacing="2",
                    ),
                    rx.vstack(
                        *[
                            rx.box(
                                rx.text(cond, size="2", color=DARK_THEME["colors"]["text_primary"]),
                                style={
                                    "background": f"{COLORS['warning']['500']}20",
                                    "padding": SPACING["3"],
                                    "border_radius": RADIUS["lg"],
                                    "border_left": f"4px solid {COLORS['warning']['500']}",
                                }
                            )
                            for cond in PACIENTE_MOCKUP["condiciones_preexistentes"]
                        ],
                        spacing="2",
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

            columns="2",
            spacing="4",
            width="100%",
        ),

        # Medicamentos
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("pill", size=20, color=COLORS["info"]["500"]),
                    rx.heading("Medicamentos Actuales", size="4", color=COLORS["info"]["500"]),
                    spacing="2",
                ),
                rx.hstack(
                    *[rx.badge(med, color_scheme="blue", variant="soft") for med in PACIENTE_MOCKUP["medicamentos_actuales"]],
                    spacing="2",
                    wrap="wrap",
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
                    PACIENTE_MOCKUP["observaciones_medicas"],
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
    return rx.box(
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
                        rx.tabs.content(tab_odontograma(), value="odontograma"),
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

        background=DARK_THEME["colors"]["background"],
        min_height="100vh",
        width="100%",
    )
