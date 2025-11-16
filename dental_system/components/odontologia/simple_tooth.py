"""
🦷 COMPONENTE SIMPLE DE DIENTE - VERSIÓN PROFESIONAL
====================================================

FILOSOFÍA: Un diente = Un componente único
- Click en diente completo → Abre panel de detalles
- Color representa estado GENERAL del diente
- Sin división visual por superficies (eso va en el panel lateral)

INSPIRADO EN: Plantilla React professional-odontogram-viewer
"""

import reflex as rx
from typing import Optional
from dental_system.styles.medical_design_system import DARK_COLORS


def get_tooth_color(status: str) -> str:
    """
    🎨 Obtener color según estado del diente

    Paleta médica profesional basada en consultas_page.py
    """
    color_map = {
        "sano": DARK_COLORS["accent_green"],      # #38a169 - Verde
        "caries": DARK_COLORS["priority_urgent"], # #dc2626 - Rojo
        "obturado": DARK_COLORS["accent_blue"],   # #3182ce - Azul
        "corona": DARK_COLORS["accent_yellow"],   # #d69e2e - Amarillo
        "endodoncia": DARK_COLORS["accent_orange"], # #dd6b20 - Naranja
        "ausente": DARK_COLORS["border"],         # #718096 - Gris
        "fractura": DARK_COLORS["priority_urgent"], # #dc2626 - Rojo
        "implante": DARK_COLORS["accent_purple"], # #805ad5 - Púrpura
    }

    # 🔍 DEBUG: Imprimir status recibido
    color_resultado = color_map.get(status, DARK_COLORS["surface"])
    return color_resultado


def simple_tooth(
    tooth_number: int,
    status: str = "sano",
    has_conditions: bool = False,
    is_selected: bool = False,
    is_hovered: bool = False,
    on_click = None
) -> rx.Component:
    """
    🦷 COMPONENTE DIENTE SIMPLIFICADO PROFESIONAL

    Args:
        tooth_number: Número FDI (11-48)
        status: Estado general ("sano", "caries", "obturado", etc.)
        has_conditions: Si tiene condiciones activas (muestra badge rojo)
        is_selected: Si está seleccionado (borde resaltado)
        is_hovered: Si está en hover (efecto visual)
        on_click: Callback al hacer click

    Returns:
        Box único con número del diente, color de fondo y badge opcional
    """

    # ✅ Mapeo COMPLETO de status → color (sincronizado con get_teeth_data)
    # Orden de prioridad: ausente > fractura > caries > endodoncia > obturado > corona > implante > sano
    bg_color = rx.match(
        status,
        ("ausente", DARK_COLORS["border"]),           # ⚫ #718096 - Gris (diente extraído)
        ("fractura", DARK_COLORS["priority_urgent"]), # 🔴 #dc2626 - Rojo (fractura urgente)
        ("caries", DARK_COLORS["priority_urgent"]),   # 🔴 #dc2626 - Rojo (caries)
        ("endodoncia", DARK_COLORS["accent_orange"]), # 🟠 #dd6b20 - Naranja (conducto)
        ("obturado", DARK_COLORS["accent_blue"]),     # 🔵 #3182ce - Azul (obturación)
        ("corona", DARK_COLORS["accent_yellow"]),     # 🟡 #d69e2e - Amarillo (corona)
        ("implante", DARK_COLORS["accent_purple"]),   # 🟣 #805ad5 - Púrpura (implante)
        ("sano", DARK_COLORS["accent_green"]),        # 🟢 #38a169 - Verde (saludable)
        DARK_COLORS["surface"]  # Default: gris oscuro
    )

    return rx.box(
        # Número del diente centrado
        rx.text(
            str(tooth_number),
            font_size="14px",
            font_weight="800",
            color="white",
            text_align="center",
        ),

        # Estilos del contenedor
        width="36px",
        height="48px",
        background=bg_color,
        # Borde más grueso si está seleccionado (usando rx.cond)
        border=rx.cond(
            is_selected,
            f"3px solid {DARK_COLORS['foreground']}",
            f"2px solid {DARK_COLORS['border']}"
        ),
        border_radius="6px",
        display="flex",
        align_items="center",
        justify_content="center",
        cursor="pointer",
        transition="all 0.2s ease",
        # Efecto hover (usando rx.cond)
        box_shadow=rx.cond(
            is_hovered,
            "0 4px 6px rgba(0,0,0,0.3)",
            "0 2px 4px rgba(0,0,0,0.2)"
        ),
        position="relative",

        # Hover effect
        _hover={
            "transform": "scale(1.05)",
            "box_shadow": "0 6px 12px rgba(0,0,0,0.4)",
        },

        # Click handler
        on_click=on_click,
    )


def tooth_with_tooltip(
    tooth_number: int,
    tooth_name: str,
    status: str = "sano",
    has_conditions: bool = False,
    is_selected: bool = False,
    on_click = None
) -> rx.Component:
    """
    🦷 Diente con tooltip informativo al hacer hover

    Muestra nombre completo del diente en español
    """
    return rx.tooltip(
        simple_tooth(
            tooth_number=tooth_number,
            status=status,
            has_conditions=has_conditions,
            is_selected=is_selected,
            on_click=on_click,
        ),
        content=f"Diente {tooth_number} - {tooth_name}",
    )


# Mapeo de números FDI a nombres en español
TOOTH_NAMES = {
    # Cuadrante 1 (Superior Derecho)
    11: "Incisivo Central Superior Derecho",
    12: "Incisivo Lateral Superior Derecho",
    13: "Canino Superior Derecho",
    14: "Primer Premolar Superior Derecho",
    15: "Segundo Premolar Superior Derecho",
    16: "Primer Molar Superior Derecho",
    17: "Segundo Molar Superior Derecho",
    18: "Tercer Molar Superior Derecho",

    # Cuadrante 2 (Superior Izquierdo)
    21: "Incisivo Central Superior Izquierdo",
    22: "Incisivo Lateral Superior Izquierdo",
    23: "Canino Superior Izquierdo",
    24: "Primer Premolar Superior Izquierdo",
    25: "Segundo Premolar Superior Izquierdo",
    26: "Primer Molar Superior Izquierdo",
    27: "Segundo Molar Superior Izquierdo",
    28: "Tercer Molar Superior Izquierdo",

    # Cuadrante 3 (Inferior Izquierdo)
    31: "Incisivo Central Inferior Izquierdo",
    32: "Incisivo Lateral Inferior Izquierdo",
    33: "Canino Inferior Izquierdo",
    34: "Primer Premolar Inferior Izquierdo",
    35: "Segundo Premolar Inferior Izquierdo",
    36: "Primer Molar Inferior Izquierdo",
    37: "Segundo Molar Inferior Izquierdo",
    38: "Tercer Molar Inferior Izquierdo",

    # Cuadrante 4 (Inferior Derecho)
    41: "Incisivo Central Inferior Derecho",
    42: "Incisivo Lateral Inferior Derecho",
    43: "Canino Inferior Derecho",
    44: "Primer Premolar Inferior Derecho",
    45: "Segundo Premolar Inferior Derecho",
    46: "Primer Molar Inferior Derecho",
    47: "Segundo Molar Inferior Derecho",
    48: "Tercer Molar Inferior Derecho",
}
