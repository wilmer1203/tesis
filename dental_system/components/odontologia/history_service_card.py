"""
📋 CARD DE SERVICIO DEL HISTORIAL - VERSIÓN COMPACTA DARK
===========================================================

Muestra UN servicio/intervención del historial del paciente.
100% declarativo - Tema oscuro consistente - Diseño compacto.

Características:
- Card compacto con diseño eficiente
- Tema oscuro glassmorphism
- Información agrupada inteligentemente
- Muestra: Fecha | Odontólogo | Diente | Superficies | Servicio | Condición | Material | Observaciones
- NO muestra precios (enfoque 100% clínico)
"""

import reflex as rx
from dental_system.styles.themes import (
    COLORS, DARK_THEME, SPACING, RADIUS, SHADOWS,
    dark_crystal_card, glassmorphism_card
)

# ==========================================
# 📊 COMPONENTE CARD DE SERVICIO HISTÓRICO
# ==========================================

def history_service_card(service: dict) -> rx.Component:
    """
    📋 Card compacto de servicio individual del historial

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
        Card compacto con toda la información
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
        # 📅 Header Compacto: Fecha + Odontólogo en línea
        rx.hstack(
            # Fecha con icono
            rx.hstack(
                rx.icon("calendar", size=16, color=COLORS["primary"]["400"]),
                rx.text(
                    rx.moment(service["fecha"], format="DD/MM/YY HH:mm"),
                    font_size="13px",
                    font_weight="600",
                    color=DARK_THEME["colors"]["text_primary"],
                ),
                spacing="2",
            ),

            rx.spacer(),

            # Odontólogo compacto
            rx.hstack(
                rx.icon("user-round", size=16, color=COLORS["blue"]["500"]),
                rx.text(
                    service["odontologo_nombre"],
                    font_size="12px",
                    font_weight="500",
                    color=DARK_THEME["colors"]["text_secondary"],
                ),
                rx.badge(
                    service["especialidad"],
                    color_scheme="gray",
                    variant="soft",
                    size="2",
                ),
                spacing="2",
                align="center",
            ),

            width="100%",
            align="center",
            padding_bottom="10px",
            border_bottom=f"1px solid {DARK_THEME['colors']['border']}",
            margin_bottom="10px",
        ),

        # 🦷 Info Principal EN 2 FILAS: Grid de 4 columnas
        rx.grid(
            # Columna 1: Diente + Superficies
            rx.vstack(
                rx.cond(
                    service["alcance"] == "boca_completa",
                    rx.badge(
                        "Boca Completa",
                        color_scheme="purple",
                        variant="soft",
                        size="2"
                    ),
                    rx.vstack(
                        rx.badge(
                            rx.cond(
                                service['diente_numero'] == "Boca completa",
                                service['diente_numero'],
                                f"Diente {service['diente_numero']}"
                            ),
                            color_scheme="cyan",
                            variant="soft",
                            size="2",
                        ),
                        rx.text(
                            service["diente_nombre"],
                            font_size="11px",
                            color=DARK_THEME["colors"]["text_secondary"],
                        ),
                        # Superficies inline
                        rx.cond(
                            service["alcance"] != "boca_completa",
                            rx.text(
                                service["superficies_texto"],
                                font_size="11px",
                                color=DARK_THEME["colors"]["text_muted"],
                                font_style="italic",
                            ),
                            rx.box(),
                        ),
                        spacing="1",
                        align="start",
                    ),
                ),
                spacing="1",
                align="start",
            ),

            # Columna 2: Servicio + Categoría
            rx.vstack(
                rx.text(
                    service["servicio_nombre"],
                    font_size="14px",
                    font_weight="700",
                    color=DARK_THEME["colors"]["text_primary"],
                ),
                rx.badge(
                    service["servicio_categoria"],
                    color_scheme=category_colors.get(service["servicio_categoria"], "gray"),
                    variant="soft",
                    size="2",
                ),
                # Material inline
                rx.cond(
                    service["material_utilizado"],
                    rx.text(
                        f"Material: {service['material_utilizado']}",
                        font_size="11px",
                        color=DARK_THEME["colors"]["text_secondary"],
                    ),
                    rx.box(),
                ),
                spacing="1",
                align="start",
            ),

            # Columna 3: Condición
            rx.vstack(
                rx.cond(
                    service["condicion_aplicada"],
                    rx.vstack(
                        rx.text(
                            "Condición aplicada:",
                            font_size="11px",
                            color=DARK_THEME["colors"]["text_muted"],
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
                    rx.text(
                        "Sin cambio de condición",
                        font_size="11px",
                        color=DARK_THEME["colors"]["text_muted"],
                        font_style="italic",
                    ),
                ),
                spacing="1",
                align="start",
            ),

            # Columna 4: Observaciones inline
            rx.vstack(
                rx.cond(
                    service["observaciones"],
                    rx.vstack(
                        rx.hstack(
                            rx.icon("message-square", size=14, color=COLORS["warning"]["500"]),
                            rx.text(
                                "Observaciones:",
                                font_size="11px",
                                color=DARK_THEME["colors"]["text_muted"],
                                font_weight="600",
                            ),
                            spacing="1",
                        ),
                        rx.text(
                            service["observaciones"],
                            font_size="12px",
                            color=DARK_THEME["colors"]["text_secondary"],
                            line_height="1.4",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.text(
                        "Sin observaciones",
                        font_size="11px",
                        color=DARK_THEME["colors"]["text_muted"],
                        font_style="italic",
                    ),
                ),
                spacing="1",
                align="start",
            ),

            columns="4",
            spacing="4",
            width="100%",
        ),

        # Estilos del card - Versión mejorada
        style={
            "background": f"rgba({DARK_THEME['colors']['surface']}, 0.6)",
            "border": f"1px solid {DARK_THEME['colors']['border']}",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],  # Padding ajustado para legibilidad
            "backdrop_filter": "blur(10px)",
            "transition": "all 0.2s ease",
            "box_shadow": f"0 2px 8px rgba(0, 0, 0, 0.3)",
            "_hover": {
                "transform": "translateY(-2px)",
                "box_shadow": f"0 4px 16px {COLORS['primary']['500']}20, 0 2px 8px rgba(0, 0, 0, 0.4)",
                "border_color": f"{COLORS['primary']['500']}60",
            },
        },
        width="100%",
        margin_bottom=SPACING["3"],  # Margen apropiado entre cards
    )
