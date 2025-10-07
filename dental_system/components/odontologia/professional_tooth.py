"""
🦷 COMPONENTE PROFESIONAL: DIENTE INTERACTIVO MÉDICO
===================================================

Componente unificado y profesional para representar dientes en odontogramas.
Basado en estándares médicos internacionales WHO/ADA/ISO.

Características:
- Tamaño estandarizado 60x60px (óptimo anatomía + clickabilidad)
- 5 superficies anatómicas interactivas
- Paleta médica profesional ISO
- Tooltip médico informativo completo
- Animaciones sutiles 150ms
- Sin efectos distractores

Versión: 3.0 Professional Medical
Fecha: Enero 2025
"""

import reflex as rx
from typing import Dict, Optional
from dental_system.state.app_state import AppState
from dental_system.styles.medical_design_system import (
    MEDICAL_COLORS,
    MEDICAL_SPACING,
    MEDICAL_TYPOGRAPHY,
    MEDICAL_SHADOWS,
    MEDICAL_RADIUS,
    MEDICAL_TRANSITIONS,
    TOOTH_DIMENSIONS,
    get_dental_condition_color,
    is_urgent_condition
)

# ==========================================
# 🦷 SUPERFICIE INDIVIDUAL DEL DIENTE
# ==========================================

def tooth_surface_medical(
    tooth_number: int,
    surface_name: str
) -> rx.Component:
    """
    🦷 Superficie individual anatómica del diente - Versión médica profesional

    Args:
        tooth_number: Número FDI del diente (11-48)
        surface_name: Nombre de la superficie (oclusal, mesial, distal, vestibular, lingual)

    Returns:
        Componente de superficie interactivo profesional
    """

    # Obtener posición anatómica de la superficie
    surface_position = TOOTH_DIMENSIONS["surface"].get(surface_name, {})

    # Obtener condición actual de la superficie
    # condicion = AppState.condiciones_por_diente.get(tooth_number, {}).get(surface_name, "sano")

    return rx.tooltip(
        rx.box(
            # Superficie interactiva
            style={
                # Posicionamiento anatómico
                "position": "absolute",
                **surface_position,

                # Color según condición médica
                "background": rx.cond(
                    AppState.condiciones_por_diente.get(tooth_number, {}).get(surface_name) != None,
                    get_dental_condition_color(
                        AppState.condiciones_por_diente.get(tooth_number, {}).get(surface_name, "sano"),
                        "light"
                    ),
                    get_dental_condition_color("sano", "light")
                ),

                # Borde médico profesional
                "border": f"{rx.cond(AppState.diente_seleccionado == tooth_number, '2px', '1px')} solid",
                "border_color": rx.cond(
                    AppState.diente_seleccionado == tooth_number,
                    MEDICAL_COLORS["medical_ui"]["border_focus"],
                    rx.cond(
                        AppState.condiciones_por_diente.get(tooth_number, {}).get(surface_name) != None,
                        get_dental_condition_color(
                            AppState.condiciones_por_diente.get(tooth_number, {}).get(surface_name, "sano"),
                            "dark"
                        ),
                        MEDICAL_COLORS["medical_ui"]["border_light"]
                    )
                ),

                "border_radius": MEDICAL_RADIUS["sm"],

                # Interactividad profesional
                "cursor": "pointer",
                "transition": MEDICAL_TRANSITIONS["base"],
                "opacity": rx.cond(
                    AppState.diente_seleccionado == tooth_number,
                    "1.0",
                    "0.9"
                ),

                # Z-index para capas
                "z_index": rx.cond(
                    AppState.diente_seleccionado == tooth_number,
                    "5",
                    "2"
                ),

                # Hover sutil médico
                "_hover": {
                    "opacity": "1.0",
                    "transform": "scale(1.05)",
                    "z_index": "6",
                    "box_shadow": MEDICAL_SHADOWS["sm"]
                }
            },

            # Evento de selección médica
            on_click=lambda: AppState.seleccionar_diente_superficie(tooth_number, surface_name)
        ),

        # Tooltip médico informativo
        content=f"{surface_name.title()} - Click para editar",
        side="top",
        delay_duration=300
    )


# ==========================================
# 🦷 DIENTE COMPLETO PROFESIONAL
# ==========================================

def professional_tooth(tooth_number: int) -> rx.Component:
    """
    🦷 Componente principal unificado del diente médico profesional

    Características:
    - Tamaño 60x60px estandarizado
    - 5 superficies anatómicas interactivas
    - Paleta médica ISO/WHO/ADA
    - Tooltip informativo completo
    - Animaciones sutiles 150ms
    - Indicadores de urgencia médicos

    Args:
        tooth_number: Número FDI del diente (11-48)

    Returns:
        Componente de diente profesional completo
    """

    # Verificar si tiene condiciones urgentes
    has_urgent = rx.cond(
        # Lógica para detectar urgencias (simplificada por ahora)
        False,  # TODO: Implementar lógica de urgencia real
        True,
        False
    )

    # Determinar si está seleccionado
    is_selected = AppState.diente_seleccionado == tooth_number

    return rx.box(
        # ===================================
        # NÚMERO DEL DIENTE (CENTRADO)
        # ===================================
        rx.text(
            str(tooth_number),
            style={
                "position": "absolute",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "z_index": "1",
                "font_family": MEDICAL_TYPOGRAPHY["font_family"]["primary"],
                "font_size": MEDICAL_TYPOGRAPHY["font_size"]["xs"],
                "font_weight": MEDICAL_TYPOGRAPHY["font_weight"]["bold"],
                "color": MEDICAL_COLORS["medical_ui"]["text_primary"],
                "text_shadow": "0 1px 2px rgba(255, 255, 255, 0.8)",
                "pointer_events": "none",
                "user_select": "none"
            }
        ),

        # ===================================
        # 5 SUPERFICIES ANATÓMICAS
        # ===================================
        tooth_surface_medical(tooth_number, "oclusal"),
        tooth_surface_medical(tooth_number, "mesial"),
        tooth_surface_medical(tooth_number, "distal"),
        tooth_surface_medical(tooth_number, "vestibular"),
        tooth_surface_medical(tooth_number, "lingual"),

        # ===================================
        # INDICADOR DE URGENCIA MÉDICA
        # ===================================
        rx.cond(
            has_urgent,
            rx.box(
                "!",
                style={
                    "position": "absolute",
                    "top": "-2px",
                    "right": "-2px",
                    "width": "14px",
                    "height": "14px",
                    "border_radius": MEDICAL_RADIUS["full"],
                    "background": "linear-gradient(135deg, #EF4444, #DC2626)",
                    "color": "white",
                    "font_size": "9px",
                    "font_weight": MEDICAL_TYPOGRAPHY["font_weight"]["bold"],
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center",
                    "box_shadow": MEDICAL_SHADOWS["md"],
                    "z_index": "10",
                    "border": "2px solid white"
                }
            )
        ),

        # ===================================
        # INDICADOR DE CAMBIOS PENDIENTES
        # ===================================
        rx.cond(
            AppState.cambios_sin_guardar,
            rx.box(
                style={
                    "position": "absolute",
                    "top": "2px",
                    "left": "2px",
                    "width": "6px",
                    "height": "6px",
                    "background": MEDICAL_COLORS["medical_ui"]["accent_warning"],
                    "border_radius": MEDICAL_RADIUS["full"],
                    "z_index": "10",
                    "box_shadow": f"0 0 0 2px {MEDICAL_COLORS['medical_ui']['background']}"
                }
            )
        ),

        # ===================================
        # ESTILOS DEL CONTENEDOR PRINCIPAL
        # ===================================
        style={
            # Dimensiones estandarizadas
            **TOOTH_DIMENSIONS["standard"],

            # Posicionamiento
            "position": "relative",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",

            # Fondo médico profesional
            "background": rx.cond(
                is_selected,
                f"linear-gradient(145deg, {MEDICAL_COLORS['medical_ui']['selected_overlay']}, {MEDICAL_COLORS['medical_ui']['surface']})",
                MEDICAL_COLORS["medical_ui"]["surface"]
            ),

            # Borde médico
            "border": f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
            "border_radius": MEDICAL_RADIUS["tooth"],

            # Sombra profesional
            "box_shadow": rx.cond(
                is_selected,
                MEDICAL_SHADOWS["tooth_selected"],
                MEDICAL_SHADOWS["tooth"]
            ),

            # Transición suave
            "transition": MEDICAL_TRANSITIONS["base"],

            # Cursor médico
            "cursor": "pointer",
            "user_select": "none",

            # Hover profesional muy sutil
            "_hover": {
                "transform": "scale(1.02)",
                "box_shadow": MEDICAL_SHADOWS["tooth_hover"],
                "border_color": MEDICAL_COLORS["medical_ui"]["border_medium"]
            },

            # Active sutil
            "_active": {
                "transform": "scale(1.0)",
                "transition": MEDICAL_TRANSITIONS["fast"]
            }
        },

        # Evento de click general del diente
        on_click=lambda: AppState.seleccionar_diente(tooth_number)
    )


# ==========================================
# 🦷 DIENTE CON TOOLTIP MÉDICO COMPLETO
# ==========================================

def professional_tooth_with_tooltip(tooth_number: int) -> rx.Component:
    """
    🦷 Diente profesional con tooltip médico informativo completo

    Incluye:
    - Número FDI y nombre anatómico
    - Tipo de diente (incisivo, canino, premolar, molar)
    - Cuadrante FDI
    - Condiciones actuales
    - Fecha última intervención
    - Notas clínicas (si existen)

    Args:
        tooth_number: Número FDI del diente

    Returns:
        Componente con tooltip médico profesional
    """

    # Determinar tipo de diente usando rx.cond para compatibilidad con Vars
    last_digit = tooth_number % 10
    tooth_type = rx.cond(
        (last_digit == 1) | (last_digit == 2),
        "Incisivo",
        rx.cond(
            last_digit == 3,
            "Canino",
            rx.cond(
                (last_digit == 4) | (last_digit == 5),
                "Premolar",
                "Molar"
            )
        )
    )

    # Obtener cuadrante
    quadrant = tooth_number // 10

    # Usar hover_card para contenido rico (acepta componentes complejos)
    return rx.hover_card.root(
        rx.hover_card.trigger(
            # Componente del diente
            professional_tooth(tooth_number)
        ),
        rx.hover_card.content(
            rx.vstack(
                # Header: Número + Tipo
                rx.hstack(
                    rx.text(
                        f"Diente {tooth_number}",
                        font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["bold"],
                        font_size=MEDICAL_TYPOGRAPHY["font_size"]["md"],
                        color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                    ),
                    rx.badge(
                        tooth_type,
                        style={
                            "background": MEDICAL_COLORS["medical_ui"]["accent_info"],
                            "color": "white",
                            "font_size": MEDICAL_TYPOGRAPHY["font_size"]["xs"]
                        }
                    ),
                    spacing="2",
                    align="center"
                ),

                # Cuadrante FDI
                rx.text(
                    f"Cuadrante {quadrant}",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                    color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                ),

                # Separador
                rx.divider(
                    border_color=MEDICAL_COLORS["medical_ui"]["border_light"],
                    margin_y="2"
                ),

                # Instrucción
                rx.text(
                    "Click en superficie para editar condición",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["xs"],
                    color=MEDICAL_COLORS["medical_ui"]["text_muted"],
                    style={"font_style": "italic"}
                ),

                spacing="1",
                align="start",
                padding=MEDICAL_SPACING["sm"]
            ),
            side="top",
            align="center"
        )
    )


# ==========================================
# 🎨 LEYENDA DE CONDICIONES MÉDICAS
# ==========================================

def medical_conditions_legend() -> rx.Component:
    """
    🎨 Leyenda de condiciones médicas profesional

    Muestra todas las condiciones disponibles con sus colores médicos estándar.
    Versión compacta y profesional para sidebar.

    Returns:
        Componente de leyenda médica
    """

    # Condiciones médicas estándar a mostrar
    conditions = [
        {"key": "healthy", "name": "Sano", "es": "sano"},
        {"key": "caries", "name": "Caries", "es": "caries"},
        {"key": "restored", "name": "Obturado", "es": "obturado"},
        {"key": "crown", "name": "Corona", "es": "corona"},
        {"key": "endodontic", "name": "Endodoncia", "es": "endodoncia"},
        {"key": "missing", "name": "Ausente", "es": "ausente"},
        {"key": "fractured", "name": "Fractura", "es": "fractura"},
        {"key": "implant", "name": "Implante", "es": "implante"}
    ]

    return rx.box(
        rx.vstack(
            # Header de leyenda
            rx.hstack(
                rx.icon(tag="palette", size=18, color=MEDICAL_COLORS["medical_ui"]["text_primary"]),
                rx.text(
                    "Leyenda de Condiciones",
                    font_size=MEDICAL_TYPOGRAPHY["font_size"]["md"],
                    font_weight=MEDICAL_TYPOGRAPHY["font_weight"]["semibold"],
                    color=MEDICAL_COLORS["medical_ui"]["text_primary"]
                ),
                spacing="2",
                align="center",
                margin_bottom="3"
            ),

            # Lista de condiciones
            *[
                rx.hstack(
                    # Muestra de color
                    rx.box(
                        style={
                            "width": "20px",
                            "height": "20px",
                            "background": get_dental_condition_color(cond["key"], "base"),
                            "border": f"1px solid {MEDICAL_COLORS['medical_ui']['border_medium']}",
                            "border_radius": MEDICAL_RADIUS["sm"],
                            "flex_shrink": "0"
                        }
                    ),
                    # Nombre de condición
                    rx.text(
                        cond["name"],
                        font_size=MEDICAL_TYPOGRAPHY["font_size"]["sm"],
                        color=MEDICAL_COLORS["medical_ui"]["text_secondary"]
                    ),
                    spacing="2",
                    align="center"
                )
                for cond in conditions
            ],

            spacing="2",
            align="start",
            width="100%"
        ),

        style={
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "border": f"1px solid {MEDICAL_COLORS['medical_ui']['border_light']}",
            "border_radius": MEDICAL_RADIUS["lg"],
            "padding": MEDICAL_SPACING["md"],
            "box_shadow": MEDICAL_SHADOWS["sm"]
        }
    )


# ==========================================
# 🔧 FUNCIONES AUXILIARES
# ==========================================

def validate_fdi_number(tooth_number: int) -> bool:
    """
    Validar que el número de diente sea válido según FDI

    Args:
        tooth_number: Número a validar

    Returns:
        True si es válido, False si no
    """
    valid_teeth = [
        # Cuadrante 1 (Superior Derecho)
        18, 17, 16, 15, 14, 13, 12, 11,
        # Cuadrante 2 (Superior Izquierdo)
        21, 22, 23, 24, 25, 26, 27, 28,
        # Cuadrante 3 (Inferior Izquierdo)
        31, 32, 33, 34, 35, 36, 37, 38,
        # Cuadrante 4 (Inferior Derecho)
        41, 42, 43, 44, 45, 46, 47, 48
    ]
    return tooth_number in valid_teeth


# ==========================================
# 🎯 EXPORTS
# ==========================================

__all__ = [
    "professional_tooth",
    "professional_tooth_with_tooltip",
    "tooth_surface_medical",
    "medical_conditions_legend",
    "validate_fdi_number"
]