"""
🎨 SISTEMA DE DESIGN OPTIMIZADO - Clínica Dental Odontomara
============================================================
Sistema completo de diseño con:
- Paleta de colores profesional
- Temas claro/oscuro dinámicos  
- Componentes reutilizables
- Estilos por roles específicos
- Responsive design utilities
- Animaciones y transiciones
============================================================
"""

from typing import Dict, Any, Optional, Union, List
from functools import lru_cache
import colorsys

# ==========================================
# 🎨 PALETA DE COLORES PRINCIPAL - EXPANDIDA
# ==========================================

COLORS = {
    # Colores primarios (Turquesa dental) - Expandidos
    "primary": {
        "25": "#F0FDFC",
        "50": "#E6F9F8",
        "100": "#B3F0ED", 
        "200": "#80E7E2",
        "300": "#4DDED7",
        "400": "#1AD5CC",
        "500": "#1CBBBA",  # Color principal
        "600": "#18A8A7",
        "700": "#159594",
        "800": "#118281",
        "900": "#0E6F6E",
        "950": "#0A5555"
    },
    
    # Colores secundarios (dorado) - Expandidos
    "secondary": {
        "25": "#FFFDF5",
        "50": "#FEF7E0",
        "100": "#FCEAAD",
        "200": "#FADD7A",
        "300": "#F8D047",
        "400": "#F6C314",
        "500": "#E6B012",  # Color secundario
        "600": "#D4A212",
        "700": "#C29411",
        "800": "#B08610",
        "900": "#9E780F",
        "950": "#7D5F0A"
    },
    
    # Azules (complementarios) - Expandidos
    "blue": {
        "25": "#F7FAFC", 
        "50": "#E6F0F7",
        "100": "#B3D4E8",
        "200": "#80B8D9",
        "300": "#4D9CCA",
        "400": "#1A80BB",
        "500": "#186289",  # Azul medio
        "600": "#15587A",
        "700": "#124E6B",
        "800": "#0F445C",
        "900": "#003A5D",   # Azul marino
        "950": "#002A42"
    },
    
    # Grises - Sistema completo
    "gray": {
        "25": "#FCFCFD",
        "50": "#F8FAFC",
        "100": "#F1F5F9",
        "200": "#E2E8F0",
        "300": "#CBD5E1",
        "400": "#94A3B8",
        "500": "#64748B",
        "600": "#475569",
        "700": "#334155",
        "800": "#1E293B",
        "900": "#0F172A",
        "950": "#020617"
    },
    
    # Estados semánticos
    "success": {
        "25": "#F0FDF4",
        "50": "#DCFCE7", 
        "100": "#BBF7D0",
        "200": "#86EFAC",
        "300": "#4ADE80",
        "400": "#22C55E",
        "500": "#16A34A",  # Principal
        "600": "#15803D",
        "700": "#166534",
        "800": "#14532D",
        "900": "#14532D"
    },
    
    "error": {
        "25": "#FFFBFA",
        "50": "#FEF2F2",
        "100": "#FEE2E2", 
        "200": "#FECACA",
        "300": "#FCA5A5",
        "400": "#F87171",
        "500": "#EF4444",  # Principal
        "600": "#DC2626",
        "700": "#B91C1C",
        "800": "#991B1B",
        "900": "#7F1D1D"
    },
    
    "warning": {
        "25": "#FFFCF5",
        "50": "#FEF3C7",
        "100": "#FEF3C7",
        "200": "#FDE68A", 
        "300": "#FCD34D",
        "400": "#FBBF24",
        "500": "#F59E0B",  # Principal
        "600": "#D97706",
        "700": "#B45309",
        "800": "#92400E",
        "900": "#78350F"
    },
    
    "info": {
        "25": "#F8FAFC",
        "50": "#EFF6FF",
        "100": "#DBEAFE",
        "200": "#BFDBFE",
        "300": "#93C5FD", 
        "400": "#60A5FA",
        "500": "#3B82F6",  # Principal
        "600": "#2563EB",
        "700": "#1D4ED8",
        "800": "#1E40AF",
        "900": "#1E3A8A"
    }
}





# ==========================================
# 🌗 TEMAS CLARO Y OSCURO
# ==========================================

LIGHT_THEME = {
    "name": "light",
    "colors": {
        "background": COLORS["gray"]["25"],
        "surface": COLORS["gray"]["50"],
        "surface_secondary": COLORS["gray"]["100"],
        "text_primary": COLORS["gray"]["900"],
        "text_secondary": COLORS["gray"]["700"],
        "text_muted": COLORS["gray"]["500"],
        "border": COLORS["gray"]["200"],
        "border_strong": COLORS["gray"]["300"],
        "primary": COLORS["primary"]["500"],
        "primary_hover": COLORS["primary"]["600"],
        "primary_light": COLORS["primary"]["100"],
        "shadow": "rgba(0, 0, 0, 0.1)"
    }
}

DARK_THEME = {
    "name": "dark", 
    "colors": {
        "background": COLORS["gray"]["950"],
        "surface": COLORS["gray"]["900"],
        "surface_secondary": COLORS["gray"]["800"],
        "text_primary": COLORS["gray"]["50"],
        "text_secondary": COLORS["gray"]["300"],
        "text_muted": COLORS["gray"]["500"],
        "border": COLORS["gray"]["700"],
        "border_strong": COLORS["gray"]["600"],
        "primary": COLORS["primary"]["400"],
        "primary_hover": COLORS["primary"]["300"],
        "primary_light": COLORS["primary"]["900"],
        "shadow": "rgba(0, 0, 0, 0.3)"
    }
}

# ==========================================
# 🎭 ESTILOS POR ROLES - EXPANDIDOS
# ==========================================

ROLE_THEMES = {
    "gerente": {
        "primary": COLORS["primary"]["500"],
        "secondary": COLORS["secondary"]["500"],
        "gradient": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['blue']['600']} 100%)",
        "accent": COLORS["secondary"]["500"],
        "icon": "👔",
        "bg_pattern": "subtle-grid"
    },
    "administrador": {
        "primary": COLORS["blue"]["500"],
        "secondary": COLORS["primary"]["500"], 
        "gradient": f"linear-gradient(135deg, {COLORS['blue']['500']} 0%, {COLORS['blue']['700']} 100%)",
        "accent": COLORS["primary"]["500"],
        "icon": "👤",
        "bg_pattern": "dots"
    },
    "odontologo": {
        "primary": COLORS["success"]["500"],
        "secondary": COLORS["primary"]["500"],
        "gradient": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['primary']['500']} 100%)",
        "accent": COLORS["primary"]["500"],
        "icon": "🦷",
        "bg_pattern": "waves"
    },
    "asistente": {
        "primary": COLORS["secondary"]["500"],
        "secondary": COLORS["blue"]["500"],
        "gradient": f"linear-gradient(135deg, {COLORS['secondary']['500']} 0%, {COLORS['secondary']['600']} 100%)",
        "accent": COLORS["blue"]["500"],
        "icon": "🩺",
        "bg_pattern": "geometric"
    }
}

# ==========================================
# 📐 ESPACIADO Y DIMENSIONES - SISTEMA COMPLETO
# ==========================================

SPACING = {
    "0": "0px",
    "px": "1px",
    "0.5": "2px",
    "1": "4px",
    "1.5": "6px", 
    "2": "8px",
    "2.5": "10px",
    "3": "12px",
    "3.5": "14px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "7": "28px",
    "8": "32px",
    "9": "36px",
    "10": "40px",
    "11": "44px",
    "12": "48px",
    "14": "56px",
    "16": "64px",
    "20": "80px",
    "24": "96px",
    "28": "112px",
    "32": "128px",
    "36": "144px",
    "40": "160px",
    "44": "176px",
    "48": "192px",
    "52": "208px",
    "56": "224px",
    "60": "240px",
    "64": "256px",
    "72": "288px",
    "80": "320px",
    "96": "384px"
}

RADIUS = {
    "none": "0px",
    "sm": "2px",
    "base": "4px",
    "md": "6px",
    "lg": "8px",
    "xl": "12px",
    "2xl": "16px",
    "3xl": "24px",
    "full": "9999px"
}

SHADOWS = {
    "xs": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "sm": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
    "base": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
    "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)"
}

# ==========================================
# 🔤 TIPOGRAFÍA COMPLETA
# ==========================================

TYPOGRAPHY = {
    "font_family": {
        "sans": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
        "serif": "'Georgia', 'Times New Roman', Times, serif",
        "mono": "'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace",
        "display": "'Inter Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    },
    
    "font_size": {
        "2xs": "10px",
        "xs": "12px",
        "sm": "14px", 
        "base": "16px",
        "lg": "18px",
        "xl": "20px",
        "2xl": "24px",
        "3xl": "30px",
        "4xl": "36px",
        "5xl": "48px",
        "6xl": "60px",
        "7xl": "72px",
        "8xl": "96px",
        "9xl": "128px"
    },
    
    "font_weight": {
        "thin": "100",
        "extralight": "200", 
        "light": "300",
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
        "extrabold": "800",
        "black": "900"
    },
    
    "line_height": {
        "none": "1",
        "tight": "1.25",
        "snug": "1.375", 
        "normal": "1.5",
        "relaxed": "1.625",
        "loose": "2"
    },
    
    "letter_spacing": {
        "tighter": "-0.05em",
        "tight": "-0.025em",
        "normal": "0em", 
        "wide": "0.025em",
        "wider": "0.05em",
        "widest": "0.1em"
    }
}

# ==========================================
# 🎬 ANIMACIONES Y TRANSICIONES
# ==========================================

ANIMATIONS = {
    "duration": {
        "fast": "150ms",
        "normal": "250ms", 
        "slow": "350ms",
        "slower": "500ms"
    },
    
    "easing": {
        "linear": "linear",
        "ease": "ease",
        "ease_in": "ease-in",
        "ease_out": "ease-out", 
        "ease_in_out": "ease-in-out",
        "bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
        "smooth": "cubic-bezier(0.4, 0, 0.2, 1)"
    },
    
    "presets": {
        "fade_in": "opacity 250ms ease-in-out",
        "slide_up": "transform 250ms ease-out", 
        "scale": "transform 150ms ease-out",
        "button_hover": "all 150ms ease-in-out",
        "modal": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)"
    }
}

# ==========================================
# 📱 BREAKPOINTS RESPONSIVE
# ==========================================

BREAKPOINTS = {
    "xs": "475px",
    "sm": "640px", 
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px"
}

# ==========================================
# 🧩 COMPONENTES REUTILIZABLES
# ==========================================

# Estilos base para componentes comunes
COMPONENT_STYLES = {
    "button": {
        "base": {
            "font_family": TYPOGRAPHY["font_family"]["sans"],
            "font_weight": TYPOGRAPHY["font_weight"]["medium"],
            "border_radius": RADIUS["lg"],
            "transition": ANIMATIONS["presets"]["button_hover"],
            "cursor": "pointer",
            "display": "inline-flex",
            "align_items": "center",
            "justify_content": "center",
            "gap": SPACING["2"]
        },
        "sizes": {
            "sm": {
                "padding": f"{SPACING['2']} {SPACING['3']}",
                "font_size": TYPOGRAPHY["font_size"]["sm"],
                "height": "32px"
            },
            "md": {
                "padding": f"{SPACING['2.5']} {SPACING['4']}",
                "font_size": TYPOGRAPHY["font_size"]["base"],
                "height": "40px"
            },
            "lg": {
                "padding": f"{SPACING['3']} {SPACING['5']}",
                "font_size": TYPOGRAPHY["font_size"]["lg"],
                "height": "48px"
            }
        },
        "variants": {
            "primary": {
                "background": COLORS["primary"]["500"],
                "color": "white",
                "_hover": {
                    "background": COLORS["primary"]["600"],
                    "transform": "translateY(-1px)",
                    "box_shadow": SHADOWS["md"]
                }
            },
            "secondary": {
                "background": COLORS["gray"]["100"],
                "color": COLORS["gray"]["700"],
                "border": f"1px solid {COLORS['gray']['300']}",
                "_hover": {
                    "background": COLORS["gray"]["200"],
                    "border_color": COLORS["gray"]["400"]
                }
            },
            "success": {
                "background": COLORS["success"]["500"],
                "color": "white",
                "_hover": {
                    "background": COLORS["success"]["600"]
                }
            },
            "danger": {
                "background": COLORS["error"]["500"],
                "color": "white",
                "_hover": {
                    "background": COLORS["error"]["600"]
                }
            }
        }
    },
    
    "input": {
        "base": {
            "border_radius": RADIUS["md"],
            "border": f"1px solid {COLORS['gray']['300']}",
            "padding": f"{SPACING['2.5']} {SPACING['3']}",
            "font_size": TYPOGRAPHY["font_size"]["base"],
            "transition": ANIMATIONS["presets"]["fade_in"],
            "_focus": {
                "outline": "none",
                "border_color": COLORS["primary"]["500"],
                "box_shadow": f"0 0 0 3px {COLORS['primary']['100']}"
            }
        }
    },
    
    "card": {
        "base": {
            "background": "white",
            "border_radius": RADIUS["xl"],
            "box_shadow": SHADOWS["sm"],
            "border": f"1px solid {COLORS['gray']['200']}",
            "overflow": "hidden"
        },
        "variants": {
            "elevated": {
                "box_shadow": SHADOWS["lg"]
            },
            "flat": {
                "box_shadow": "none",
                "border": f"1px solid {COLORS['gray']['200']}"
            }
        }
    }
}


botton_login = {
            "width": "80%",
            "height": "60px",
            "color": COLORS["gray"]["50"],
            # "background": GRADIENTS["primary"],
            "background": ROLE_THEMES['gerente']['gradient'],
            "border_radius": RADIUS["xl"],
            "font_weight": "bold",
            "transition": "all 0.2s ease-in-out",
            "margin_top": "25px",
            "_hover": {
                "transform": "translateY(-1px)",
                "box_shadow": SHADOWS["xl"],
                "background": f"linear-gradient(135deg, {COLORS['blue']['500']} 0%, {COLORS['primary']['400']} 100%)",
            },
},

input_login = {
        "border_radius": "15px",
        "padding": "5px",
        "height": "2.5em",
        "border": f"2px solid {COLORS['primary']['500']}",
        "box_shadow": f"0 0 10px {COLORS['primary']['500']}",
        "font_size": "1.3em",
}

# ==========================================
# 🔧 FUNCIONES DE UTILIDAD AVANZADAS
# ==========================================

@lru_cache(maxsize=256)
def get_color(color_key: str, shade: str = "500", theme: str = "light") -> str:
    """Obtener color de la paleta con cache"""
    try:
        if color_key in COLORS:
            return COLORS[color_key].get(shade, COLORS[color_key]["500"])
        
        # Fallback a tema si no se encuentra en COLORS
        theme_colors = LIGHT_THEME["colors"] if theme == "light" else DARK_THEME["colors"]
        return theme_colors.get(color_key, COLORS["gray"]["500"])
        
    except (KeyError, TypeError):
        return COLORS["gray"]["500"]

def get_role_theme(role: str) -> Dict[str, str]:
    """Obtener tema completo para un rol específico"""
    return ROLE_THEMES.get(role, ROLE_THEMES["administrador"])

def create_gradient(color1: str, color2: str, direction: str = "135deg") -> str:
    """Crear gradiente CSS personalizado"""
    return f"linear-gradient({direction}, {color1} 0%, {color2} 100%)"

def get_responsive_value(
    values: Dict[str, str], 
    breakpoint: str = "base"
) -> str:
    """Obtener valor responsive según breakpoint"""
    if breakpoint in values:
        return values[breakpoint]
    
    # Fallback a valores más pequeños
    fallback_order = ["base", "sm", "md", "lg", "xl", "2xl"]
    for bp in fallback_order:
        if bp in values:
            return values[bp]
    
    return list(values.values())[0] if values else ""

@lru_cache(maxsize=128)
def darken_color(hex_color: str, factor: float = 0.1) -> str:
    """Oscurecer un color hex por un factor"""
    try:
        # Remover # si está presente
        hex_color = hex_color.lstrip('#')
        
        # Convertir a RGB
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convertir a HSV para manipular
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Oscurecer reduciendo el valor
        v = max(0, v - factor)
        
        # Convertir de vuelta a RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        # Convertir a hex
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        
    except (ValueError, IndexError):
        return hex_color

@lru_cache(maxsize=128)
def lighten_color(hex_color: str, factor: float = 0.1) -> str:
    """Aclarar un color hex por un factor"""
    try:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Aclarar aumentando el valor
        v = min(1, v + factor)
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        
    except (ValueError, IndexError):
        return hex_color

def get_contrast_color(background_color: str) -> str:
    """Obtener color de texto con buen contraste para un fondo"""
    try:
        # Calcular luminancia del color de fondo
        hex_color = background_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Fórmula de luminancia
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        
        # Retornar blanco o negro según luminancia
        return "#FFFFFF" if luminance < 0.5 else "#000000"
        
    except (ValueError, IndexError):
        return "#000000"

def create_theme_object(base_theme: str = "light", role: str = "administrador") -> Dict[str, Any]:
    """Crear objeto de tema completo combinando tema base y rol"""
    base = LIGHT_THEME if base_theme == "light" else DARK_THEME
    role_theme = get_role_theme(role)
    
    return {
        **base,
        "role": role_theme,
        "components": COMPONENT_STYLES,
        "spacing": SPACING,
        "typography": TYPOGRAPHY,
        "animations": ANIMATIONS,
        "breakpoints": BREAKPOINTS
    }

# ==========================================
# 🎯 ESTILOS ESPECÍFICOS DENTALES
# ==========================================

DENTAL_SPECIFIC = {
    "odontogram": {
        "tooth_healthy": COLORS["gray"]["100"],
        "tooth_caries": COLORS["error"]["500"],
        "tooth_filled": COLORS["primary"]["500"],
        "tooth_crown": COLORS["secondary"]["500"],
        "tooth_missing": COLORS["gray"]["300"],
        "tooth_root_canal": COLORS["warning"]["500"]
    },
    
    "status_colors": {
        "scheduled": COLORS["info"]["500"],
        "confirmed": COLORS["primary"]["500"],
        "in_progress": COLORS["warning"]["500"],
        "completed": COLORS["success"]["500"],
        "cancelled": COLORS["error"]["500"],
        "no_show": COLORS["gray"]["500"]
    }
}

# ==========================================
# 📤 EXPORTS
# ==========================================

__all__ = [
    # Colores y temas
    "COLORS",
    "LIGHT_THEME",
    "DARK_THEME", 
    "ROLE_THEMES",
    
    # Espaciado y dimensiones
    "SPACING",
    "RADIUS", 
    "SHADOWS",
    "TYPOGRAPHY",
    "ANIMATIONS",
    "BREAKPOINTS",
    
    # Componentes
    "COMPONENT_STYLES",
    "DENTAL_SPECIFIC",
    
    # Funciones de utilidad
    "get_color",
    "get_role_theme",
    "create_gradient",
    "get_responsive_value",
    "darken_color",
    "lighten_color", 
    "get_contrast_color",
    "create_theme_object"
]