"""
🏥 SISTEMA DE DISEÑO MÉDICO PROFESIONAL
========================================

Sistema de diseño especializado para aplicaciones médicas odontológicas
basado en estándares internacionales WHO/ADA/ISO.

Características:
- Paleta de colores médica estandarizada
- Espaciado sistemático 8/16/24/32px
- Tipografía médica profesional
- Sombras sutiles y profesionales
- Sin animaciones distractoras

Versión: 3.0 Professional Medical
Fecha: Enero 2025
"""

from typing import Dict, Any

# ==========================================
# 🎨 PALETA MÉDICA PROFESIONAL ISO/WHO/ADA
# ==========================================

MEDICAL_COLORS = {
    # Condiciones dentales - Estándares internacionales
    "dental": {
        # Estados básicos
        "healthy": {
            "base": "#10B981",      # Verde médico ISO (sano)
            "light": "#D1FAE5",     # Fondo muy suave
            "dark": "#047857",      # Borde/texto
            "hover": "#34D399"      # Hover sutil
        },
        "caries": {
            "base": "#DC2626",      # Rojo alerta médica
            "light": "#FEE2E2",
            "dark": "#991B1B",
            "hover": "#EF4444",
            "urgent": True          # Requiere atención
        },
        "restored": {
            "base": "#3B82F6",      # Azul restauración
            "light": "#DBEAFE",
            "dark": "#1E40AF",
            "hover": "#60A5FA"
        },
        "crown": {
            "base": "#F59E0B",      # Ámbar prótesis
            "light": "#FEF3C7",
            "dark": "#B45309",
            "hover": "#FBBF24"
        },
        "endodontic": {
            "base": "#8B5CF6",      # Púrpura endodoncia
            "light": "#EDE9FE",
            "dark": "#6D28D9",
            "hover": "#A78BFA"
        },
        "missing": {
            "base": "#9CA3AF",      # Gris neutral ausente
            "light": "#F3F4F6",
            "dark": "#4B5563",
            "hover": "#D1D5DB",
            "opacity": 0.7          # Indicador visual
        },
        "fractured": {
            "base": "#EF4444",      # Rojo urgente
            "light": "#FEE2E2",
            "dark": "#B91C1C",
            "hover": "#F87171",
            "urgent": True
        },
        "implant": {
            "base": "#14B8A6",      # Turquesa implante
            "light": "#CCFBF1",
            "dark": "#0F766E",
            "hover": "#2DD4BF"
        },
        "bridge": {
            "base": "#6366F1",      # Índigo puente
            "light": "#E0E7FF",
            "dark": "#4338CA",
            "hover": "#818CF8"
        },
        "planning": {
            "base": "#F97316",      # Naranja planificación
            "light": "#FFEDD5",
            "dark": "#C2410C",
            "hover": "#FB923C",
            "animated": True        # Indicador proceso
        }
    },

    # UI Médica profesional
    "medical_ui": {
        # Fondos
        "background": "#FFFFFF",
        "surface": "#F9FAFB",
        "surface_elevated": "#FFFFFF",
        "surface_overlay": "rgba(0, 0, 0, 0.75)",  # Overlay modal

        # Bordes
        "border_light": "#E5E7EB",
        "border_medium": "#D1D5DB",
        "border_strong": "#9CA3AF",
        "border_focus": "#3B82F6",

        # Texto
        "text_primary": "#111827",
        "text_secondary": "#4B5563",
        "text_muted": "#9CA3AF",
        "text_on_primary": "#FFFFFF",

        # Acentos médicos
        "accent_primary": "#0EA5E9",      # Azul médico confiable
        "accent_success": "#10B981",      # Verde confirmación
        "accent_warning": "#F59E0B",      # Ámbar precaución
        "accent_error": "#DC2626",        # Rojo error/urgencia
        "accent_info": "#3B82F6",         # Azul información

        # Estados interactivos
        "hover_overlay": "rgba(0, 0, 0, 0.05)",
        "active_overlay": "rgba(0, 0, 0, 0.1)",
        "selected_overlay": "rgba(59, 130, 246, 0.1)",
        "disabled_overlay": "rgba(0, 0, 0, 0.05)",

        # Sombras profesionales
        "shadow_color": "rgba(0, 0, 0, 0.1)"
    }
}

# ==========================================
# 📐 SISTEMA DE ESPACIADO MÉDICO
# ==========================================

MEDICAL_SPACING = {
    # Espaciado base (múltiplos de 8px)
    "xs": "4px",        # Extra tight
    "sm": "8px",        # Tight - Elementos muy relacionados
    "md": "16px",       # Normal - Separación estándar
    "lg": "24px",       # Relaxed - Secciones
    "xl": "32px",       # Loose - Áreas principales
    "2xl": "48px",      # Section - Separación mayor
    "3xl": "64px",      # Large section - Muy espaciado

    # Aplicaciones específicas médicas
    "tooth_gap": "8px",         # Espacio entre dientes
    "quadrant_gap": "16px",     # Espacio entre cuadrantes
    "section_gap": "24px",      # Espacio entre secciones
    "modal_padding": "24px",    # Padding modal
    "card_padding": "16px",     # Padding cards
    "button_padding": "12px 20px",  # Padding botones
}

# ==========================================
# 🔤 TIPOGRAFÍA MÉDICA
# ==========================================

MEDICAL_TYPOGRAPHY = {
    "font_family": {
        "primary": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "secondary": "'Roboto', 'Helvetica Neue', Arial, sans-serif",
        "mono": "'JetBrains Mono', 'Fira Code', Consolas, monospace"
    },

    "font_size": {
        "xs": "11px",       # Tooltips, labels pequeños
        "sm": "13px",       # Texto secundario
        "base": "14px",     # Texto base
        "md": "15px",       # Texto destacado
        "lg": "18px",       # Subtítulos
        "xl": "24px",       # Títulos
        "2xl": "32px",      # Títulos principales
    },

    "font_weight": {
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700"
    },

    "line_height": {
        "tight": "1.2",
        "normal": "1.5",
        "relaxed": "1.75"
    }
}

# ==========================================
# 🎭 SOMBRAS MÉDICAS PROFESIONALES
# ==========================================

MEDICAL_SHADOWS = {
    # Sombras sutiles y profesionales
    "none": "none",
    "xs": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "sm": "0 2px 4px rgba(0, 0, 0, 0.08)",
    "base": "0 2px 8px rgba(0, 0, 0, 0.1)",
    "md": "0 4px 12px rgba(0, 0, 0, 0.12)",
    "lg": "0 8px 16px rgba(0, 0, 0, 0.15)",
    "xl": "0 12px 24px rgba(0, 0, 0, 0.18)",

    # Sombras especializadas médicas
    "tooth": "0 2px 4px rgba(0, 0, 0, 0.1)",
    "tooth_hover": "0 4px 8px rgba(0, 0, 0, 0.15)",
    "tooth_selected": "0 0 0 2px rgba(59, 130, 246, 0.3)",
    "modal": "0 24px 48px rgba(0, 0, 0, 0.25)",
    "dropdown": "0 8px 16px rgba(0, 0, 0, 0.12)",
    "button": "0 2px 4px rgba(0, 0, 0, 0.08)",
    "button_hover": "0 4px 8px rgba(0, 0, 0, 0.12)",

    # Sombras internas
    "inner_light": "inset 0 1px 2px rgba(0, 0, 0, 0.05)",
    "inner_strong": "inset 0 2px 4px rgba(0, 0, 0, 0.1)"
}

# ==========================================
# 📐 BORDES Y RADIOS
# ==========================================

MEDICAL_RADIUS = {
    "none": "0",
    "sm": "4px",        # Bordes sutiles
    "base": "6px",      # Base estándar
    "md": "8px",        # Médico estándar
    "lg": "12px",       # Componentes grandes
    "xl": "16px",       # Cards, modales
    "2xl": "20px",      # Contenedores principales
    "full": "9999px",   # Circular

    # Aplicaciones específicas
    "tooth": "8px",     # Diente
    "button": "6px",    # Botones
    "input": "6px",     # Inputs
    "card": "12px",     # Cards
    "modal": "16px"     # Modales
}

MEDICAL_BORDERS = {
    "width": {
        "thin": "1px",
        "base": "1px",
        "medium": "2px",
        "thick": "3px"
    },
    "style": {
        "solid": "solid",
        "dashed": "dashed",
        "dotted": "dotted"
    }
}

# ==========================================
# ⚡ TRANSICIONES MÉDICAS (SUTILES)
# ==========================================

MEDICAL_TRANSITIONS = {
    # Transiciones profesionales y sutiles
    "fast": "all 100ms ease",
    "base": "all 150ms ease",
    "normal": "all 200ms ease",
    "slow": "all 300ms ease",

    # Transiciones específicas
    "color": "color 150ms ease, background-color 150ms ease, border-color 150ms ease",
    "transform": "transform 150ms ease",
    "opacity": "opacity 200ms ease",
    "shadow": "box-shadow 200ms ease",

    # NO usamos transiciones complejas ni rebotes
    "cubic_medical": "cubic-bezier(0.4, 0, 0.2, 1)",  # Suave estándar
}

# ==========================================
# 🎨 EFECTOS DE HOVER MÉDICOS
# ==========================================

MEDICAL_HOVER_EFFECTS = {
    "tooth": {
        "transform": "scale(1.02)",         # Muy sutil
        "box_shadow": MEDICAL_SHADOWS["tooth_hover"],
        "transition": MEDICAL_TRANSITIONS["base"]
    },
    "button_primary": {
        "background": MEDICAL_COLORS["medical_ui"]["accent_primary"],
        "transform": "translateY(-1px)",
        "box_shadow": MEDICAL_SHADOWS["button_hover"]
    },
    "card": {
        "box_shadow": MEDICAL_SHADOWS["md"],
        "border_color": MEDICAL_COLORS["medical_ui"]["border_medium"]
    }
}

# ==========================================
# 📏 DIMENSIONES ANATÓMICAS DIENTE
# ==========================================

TOOTH_DIMENSIONS = {
    # Tamaño estándar optimizado
    "standard": {
        "width": "60px",
        "height": "60px"
    },

    # Por tipo de diente (opcionales para futuro)
    "incisor": {
        "width": "56px",
        "height": "64px"
    },
    "canine": {
        "width": "58px",
        "height": "66px"
    },
    "premolar": {
        "width": "60px",
        "height": "60px"
    },
    "molar": {
        "width": "64px",
        "height": "58px"
    },

    # Superficies internas (grid 3x3)
    "surface": {
        "oclusal": {"width": "50%", "height": "30%", "top": "15%", "left": "25%"},
        "mesial": {"width": "25%", "height": "50%", "top": "25%", "left": "10%"},
        "distal": {"width": "25%", "height": "50%", "top": "25%", "right": "10%"},
        "vestibular": {"width": "50%", "height": "25%", "bottom": "25%", "left": "25%"},
        "lingual": {"width": "50%", "height": "20%", "bottom": "10%", "left": "25%"}
    }
}

# ==========================================
# 🏥 COMPONENTES BASE MÉDICOS
# ==========================================

def medical_button_style(variant: str = "primary", size: str = "md") -> Dict[str, Any]:
    """Estilo de botón médico profesional"""

    base_style = {
        "font_family": MEDICAL_TYPOGRAPHY["font_family"]["primary"],
        "font_weight": MEDICAL_TYPOGRAPHY["font_weight"]["medium"],
        "border_radius": MEDICAL_RADIUS["button"],
        "transition": MEDICAL_TRANSITIONS["base"],
        "cursor": "pointer",
        "border": f"{MEDICAL_BORDERS['width']['thin']} {MEDICAL_BORDERS['style']['solid']}",
        "outline": "none",
        "user_select": "none"
    }

    # Tamaños
    sizes = {
        "sm": {"padding": "8px 16px", "font_size": MEDICAL_TYPOGRAPHY["font_size"]["sm"]},
        "md": {"padding": "12px 20px", "font_size": MEDICAL_TYPOGRAPHY["font_size"]["base"]},
        "lg": {"padding": "16px 28px", "font_size": MEDICAL_TYPOGRAPHY["font_size"]["md"]}
    }

    # Variantes
    variants = {
        "primary": {
            "background": MEDICAL_COLORS["medical_ui"]["accent_primary"],
            "color": MEDICAL_COLORS["medical_ui"]["text_on_primary"],
            "border_color": MEDICAL_COLORS["medical_ui"]["accent_primary"],
            "box_shadow": MEDICAL_SHADOWS["button"]
        },
        "secondary": {
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "color": MEDICAL_COLORS["medical_ui"]["text_primary"],
            "border_color": MEDICAL_COLORS["medical_ui"]["border_medium"],
            "box_shadow": MEDICAL_SHADOWS["xs"]
        },
        "outline": {
            "background": "transparent",
            "color": MEDICAL_COLORS["medical_ui"]["accent_primary"],
            "border_color": MEDICAL_COLORS["medical_ui"]["accent_primary"],
            "box_shadow": "none"
        },
        "ghost": {
            "background": "transparent",
            "color": MEDICAL_COLORS["medical_ui"]["text_secondary"],
            "border_color": "transparent",
            "box_shadow": "none"
        }
    }

    return {**base_style, **sizes.get(size, sizes["md"]), **variants.get(variant, variants["primary"])}


def medical_input_style() -> Dict[str, Any]:
    """Estilo de input médico profesional"""
    return {
        "font_family": MEDICAL_TYPOGRAPHY["font_family"]["primary"],
        "font_size": MEDICAL_TYPOGRAPHY["font_size"]["base"],
        "padding": "10px 14px",
        "border": f"{MEDICAL_BORDERS['width']['thin']} {MEDICAL_BORDERS['style']['solid']} {MEDICAL_COLORS['medical_ui']['border_medium']}",
        "border_radius": MEDICAL_RADIUS["input"],
        "background": MEDICAL_COLORS["medical_ui"]["background"],
        "color": MEDICAL_COLORS["medical_ui"]["text_primary"],
        "transition": MEDICAL_TRANSITIONS["color"],
        "outline": "none",
        "_focus": {
            "border_color": MEDICAL_COLORS["medical_ui"]["border_focus"],
            "box_shadow": f"0 0 0 3px {MEDICAL_COLORS['medical_ui']['accent_primary']}20"
        },
        "_hover": {
            "border_color": MEDICAL_COLORS["medical_ui"]["border_strong"]
        },
        "_disabled": {
            "background": MEDICAL_COLORS["medical_ui"]["surface"],
            "color": MEDICAL_COLORS["medical_ui"]["text_muted"],
            "cursor": "not-allowed"
        }
    }


def medical_card_style(elevated: bool = False) -> Dict[str, Any]:
    """Estilo de card médico profesional"""
    return {
        "background": MEDICAL_COLORS["medical_ui"]["surface_elevated"] if elevated else MEDICAL_COLORS["medical_ui"]["surface"],
        "border": f"{MEDICAL_BORDERS['width']['thin']} {MEDICAL_BORDERS['style']['solid']} {MEDICAL_COLORS['medical_ui']['border_light']}",
        "border_radius": MEDICAL_RADIUS["card"],
        "padding": MEDICAL_SPACING["card_padding"],
        "box_shadow": MEDICAL_SHADOWS["sm"] if elevated else MEDICAL_SHADOWS["xs"],
        "transition": MEDICAL_TRANSITIONS["normal"]
    }


def medical_modal_overlay_style() -> Dict[str, Any]:
    """Estilo de overlay de modal médico profesional"""
    return {
        "position": "fixed",
        "top": "0",
        "left": "0",
        "width": "100vw",
        "height": "100vh",
        "background": MEDICAL_COLORS["medical_ui"]["surface_overlay"],
        "z_index": "1000",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "animation": "fadeIn 200ms ease-out"  # Animación simple y rápida
    }


def medical_modal_container_style() -> Dict[str, Any]:
    """Estilo de container de modal médico profesional"""
    return {
        "background": MEDICAL_COLORS["medical_ui"]["background"],
        "border": f"{MEDICAL_BORDERS['width']['thin']} {MEDICAL_BORDERS['style']['solid']} {MEDICAL_COLORS['medical_ui']['border_light']}",
        "border_radius": MEDICAL_RADIUS["modal"],
        "box_shadow": MEDICAL_SHADOWS["modal"],
        "max_width": "90vw",
        "max_height": "90vh",
        "overflow": "hidden",
        "animation": "slideIn 200ms ease-out"  # Animación simple sin rebote
    }


# ==========================================
# 📊 UTILIDADES DE CONVERSIÓN
# ==========================================

def get_dental_condition_color(condition: str, property: str = "base") -> str:
    """
    Obtener color de una condición dental

    Args:
        condition: Nombre de la condición (healthy, caries, etc)
        property: Propiedad del color (base, light, dark, hover)

    Returns:
        Código hexadecimal del color
    """
    condition_map = {
        "sano": "healthy",
        "caries": "caries",
        "obturado": "restored",
        "corona": "crown",
        "endodoncia": "endodontic",
        "ausente": "missing",
        "fractura": "fractured",
        "implante": "implant",
        "puente": "bridge",
        "planificado": "planning"
    }

    mapped_condition = condition_map.get(condition, "healthy")
    return MEDICAL_COLORS["dental"].get(mapped_condition, {}).get(property, "#10B981")


def is_urgent_condition(condition: str) -> bool:
    """Verificar si una condición requiere atención urgente"""
    urgent_conditions = ["caries", "fractura", "fractured"]
    return condition.lower() in urgent_conditions


# ==========================================
# 🌙 PALETA DARK MODE SIMPLIFICADA (V4.0)
# ==========================================

DARK_COLORS = {
    # Colores de fondo
    "background": "#0f1419",
    "surface": "#1a1f2e",
    "surface_hover": "#252b3b",
    "card": "#1e2433",
    "border": "#2d3748",

    # Texto
    "foreground": "#f7fafc",
    "text_primary": "#e2e8f0",
    "text_secondary": "#a0aec0",
    "text_muted": "#718096",

    # Acentos  (mismos de consultas_page.py)
    "accent_blue": "#3182ce",
    "accent_green": "#38a169",
    "accent_yellow": "#d69e2e",
    "accent_orange": "#dd6b20",
    "accent_red": "#e53e3e",
    "accent_purple": "#805ad5",

    # Prioridades
    "priority_urgent": "#dc2626",
    "priority_high": "#f59e0b",
    "priority_medium": "#3b82f6",
    "priority_low": "#10b981",
}

# ==========================================
# 🎯 EXPORTS
# ==========================================

__all__ = [
    "MEDICAL_COLORS",
    "DARK_COLORS",
    "MEDICAL_SPACING",
    "MEDICAL_TYPOGRAPHY",
    "MEDICAL_SHADOWS",
    "MEDICAL_RADIUS",
    "MEDICAL_BORDERS",
    "MEDICAL_TRANSITIONS",
    "MEDICAL_HOVER_EFFECTS",
    "TOOTH_DIMENSIONS",
    "medical_button_style",
    "medical_input_style",
    "medical_card_style",
    "medical_modal_overlay_style",
    "medical_modal_container_style",
    "get_dental_condition_color",
    "is_urgent_condition"
]