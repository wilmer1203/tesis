"""
📋 CARD DE SERVICIO DEL HISTORIAL
==================================

Muestra UN servicio/intervención del historial del paciente.
100% declarativo - Usa datos procesados desde el servicio.

Características:
- Card simple sin expand/collapse
- Muestra: Fecha | Odontólogo | Diente | Superficies | Servicio | Condición | Material | Observaciones
- NO muestra precios (enfoque 100% clínico)
- Diseño médico con glassmorphism
"""

import reflex as rx
from dental_system.styles.medical_design_system import MEDICAL_COLORS, medical_card_style

# ==========================================
# 📊 COMPONENTE CARD DE SERVICIO HISTÓRICO
# ==========================================

def history_service_card(service: dict) -> rx.Component:
    """
    📋 Card de servicio individual del historial

    Estructura esperada de `service`:
    {
        "id": "uuid",
        "fecha": "2025-10-15T10:30:00",
        "odontologo_nombre": "Dr. Juan Pérez",
        "especialidad": "Endodoncista",
        "diente_numero": 16,
        "diente_nombre": "Primer Molar Superior Derecho",
        "superficies": ["oclusal", "mesial"],
        "alcance": "diente_especifico",  # o "boca_completa"
        "servicio_nombre": "Obturación",
        "servicio_categoria": "Restaurativa",
        "condicion_aplicada": "obturacion",  # puede ser None
        "material_utilizado": "Resina compuesta",  # puede ser None
        "observaciones": "Texto libre..."
    }

    Args:
        service: Diccionario con información del servicio

    Returns:
        Card individual con toda la información
    """

    # 🎨 Color de categoría
    category_colors = {
        "Preventiva": "green",
        "Restaurativa": "blue",
        "Endodoncia": "purple",
        "Periodoncia": "pink",
        "Cirugía Oral": "red",
        "Ortodoncia": "orange",
        "Prótesis": "amber",
        "Estética Dental": "cyan",
        "Implantología": "indigo",
        "Odontopediatría": "teal",
        "Urgencias": "crimson",
        "General": "gray",
    }

    return rx.box(
        # 📅 Header: Fecha + Odontólogo + Especialidad
        rx.hstack(
            # Fecha
            rx.hstack(
                rx.icon("calendar", size=16, color=MEDICAL_COLORS["medical_ui"]["accent_primary"]),
                rx.text(
                    rx.moment(
                        service["fecha"],
                        format="DD/MM/YYYY HH:mm",
                    ),
                    font_size="13px",
                    font_weight="600",
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                ),
                spacing="2",
            ),

            rx.spacer(),

            # Odontólogo + Especialidad
            rx.vstack(
                rx.text(
                    service["odontologo_nombre"],
                    font_size="13px",
                    font_weight="600",
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    text_align="right",
                ),
                rx.text(
                    service["especialidad"],
                    font_size="11px",
                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                    text_align="right",
                ),
                spacing="0",
                align="end",
            ),

            width="100%",
            align="center",
            padding_bottom="12px",
            border_bottom=f"1px solid {MEDICAL_COLORS['medical_ui']['border_focus']}",
            margin_bottom="12px",
        ),

        # 🦷 Info Principal: Diente + Servicio
        rx.hstack(
            # Columna Izquierda: Diente + Superficies
            rx.vstack(
                # Diente
                rx.hstack(
                    rx.icon("circle-dot", size=14, color=MEDICAL_COLORS["medical_ui"]["accent_info"]),
                    rx.text(
                        "Diente:",
                        font_size="12px",
                        font_weight="600",
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                    ),
                    spacing="1",
                ),
                rx.cond(
                    service["alcance"] == "boca_completa",
                    # Boca completa
                    rx.badge(
                        "Boca Completa",
                        color_scheme="purple",
                        variant="soft",
                        size="2",
                    ),
                    # Diente específico
                    rx.vstack(
                        rx.badge(
                            f"Diente {service['diente_numero']}",
                            color_scheme="cyan",
                            variant="soft",
                            size="2",
                        ),
                        rx.text(
                            service["diente_nombre"],
                            font_size="11px",
                            color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                        ),
                        spacing="1",
                        align="start",
                    ),
                ),

                # Superficies (solo si no es boca completa)
                rx.cond(
                    service["alcance"] != "boca_completa",
                    rx.vstack(
                        rx.hstack(
                            rx.icon("layers", size=14, color=MEDICAL_COLORS["medical_ui"]["accent_info"]),
                            rx.text(
                                "Superficies:",
                                font_size="12px",
                                font_weight="600",
                                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                            ),
                            spacing="1",
                        ),
                        # Superficies como texto separado por comas (sin foreach)
                        rx.text(
                            service["superficies_texto"],
                            font_size="12px",
                            color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.box(),  # Placeholder vacío
                ),

                spacing="3",
                align="start",
                width="40%",
            ),

            # Columna Derecha: Servicio + Condición + Material
            rx.vstack(
                # Servicio
                rx.hstack(
                    rx.icon("stethoscope", size=14, color=MEDICAL_COLORS["medical_ui"]["accent_success"]),
                    rx.text(
                        "Servicio:",
                        font_size="12px",
                        font_weight="600",
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                    ),
                    spacing="1",
                ),
                rx.hstack(
                    rx.text(
                        service["servicio_nombre"],
                        font_size="14px",
                        font_weight="700",
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    ),
                    rx.badge(
                        service["servicio_categoria"],
                        color_scheme=category_colors.get(service["servicio_categoria"], "gray"),
                        variant="soft",
                        size="1",
                    ),
                    spacing="2",
                    align="center",
                ),

                # Condición Aplicada (si existe)
                rx.cond(
                    service["condicion_aplicada"],
                    rx.vstack(
                        rx.hstack(
                            rx.icon("check-circle", size=14, color=MEDICAL_COLORS["medical_ui"]["accent_success"]),
                            rx.text(
                                "Condición Aplicada:",
                                font_size="12px",
                                font_weight="600",
                                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                            ),
                            spacing="1",
                        ),
                        rx.badge(
                            service["condicion_aplicada"].replace("_", " ").title(),
                            color_scheme="green",
                            variant="soft",
                            size="2",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.box(),  # Placeholder vacío
                ),

                # Material Utilizado (si existe)
                rx.cond(
                    service["material_utilizado"],
                    rx.vstack(
                        rx.hstack(
                            rx.icon("package", size=14, color=MEDICAL_COLORS["medical_ui"]["accent_info"]),
                            rx.text(
                                "Material:",
                                font_size="12px",
                                font_weight="600",
                                color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                            ),
                            spacing="1",
                        ),
                        rx.text(
                            service["material_utilizado"],
                            font_size="13px",
                            color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.box(),  # Placeholder vacío
                ),

                spacing="3",
                align="start",
                width="60%",
            ),

            width="100%",
            align="start",
            spacing="4",
        ),

        # 📝 Observaciones (si existen)
        rx.cond(
            service["observaciones"],
            rx.box(
                rx.hstack(
                    rx.icon("file-text", size=14, color=MEDICAL_COLORS["medical_ui"]["accent_warning"]),
                    rx.text(
                        "Observaciones:",
                        font_size="12px",
                        font_weight="600",
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"],
                    ),
                    spacing="1",
                    margin_bottom="6px",
                ),
                rx.text(
                    service["observaciones"],
                    font_size="12px",
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"],
                    line_height="1.5",
                ),
                padding="12px",
                background=f"{MEDICAL_COLORS['medical_ui']['surface']}",
                border_radius="6px",
                border=f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
                margin_top="12px",
            ),
            rx.box(),  # Placeholder vacío
        ),

        # Estilos del card
        style={
            **medical_card_style(),
            "transition": "all 0.2s ease",
            "_hover": {
                "transform": "translateY(-2px)",
                "box_shadow": f"0 8px 24px {MEDICAL_COLORS['medical_ui']['accent_primary']}30",
            },
        },
        width="100%",
        margin_bottom="12px",
    )
