"""Estilos y temas del sistema"""

# Sistema de temas legacy
from .themes import COLORS, SHADOWS

# Sistema de diseño médico profesional V3.0
from .medical_design_system import (
    MEDICAL_COLORS,
    MEDICAL_SPACING,
    MEDICAL_TYPOGRAPHY,
    MEDICAL_SHADOWS,
    MEDICAL_RADIUS,
    MEDICAL_TRANSITIONS,
    TOOTH_DIMENSIONS,
    get_dental_condition_color,
    is_urgent_condition,
    medical_card_style,
    medical_button_style,
    medical_modal_overlay_style,
    medical_modal_container_style
)

__all__ = [
    # Legacy
    "COLORS",
    "SHADOWS",

    # Medical Design System V3.0
    "MEDICAL_COLORS",
    "MEDICAL_SPACING",
    "MEDICAL_TYPOGRAPHY",
    "MEDICAL_SHADOWS",
    "MEDICAL_RADIUS",
    "MEDICAL_TRANSITIONS",
    "TOOTH_DIMENSIONS",
    "get_dental_condition_color",
    "is_urgent_condition",
    "medical_card_style",
    "medical_button_style",
    "medical_modal_overlay_style",
    "medical_modal_container_style"
]