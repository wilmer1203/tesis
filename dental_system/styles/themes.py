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
import reflex as rx

# ==========================================
# 🎨 PALETA DE COLORES PRINCIPAL - EXPANDIDA
# ==========================================

COLORS = {
    # Colores primarios (Turquesa dental) - Más azulados y vibrantes
    "primary": {
        "50": "#E6F8FF",
        "100": "#B3ECFF", 
        "200": "#80E0FF",
        "300": "#4DD4FF",
        "400": "#1AC8FF",
        "500": "#00BCD4",  # Color principal turquesa vibrante
        "600": "#00ACC1",
        "700": "#0097A7",
        "800": "#00838F",
        "900": "#006064"
    },
    
    # Colores secundarios (dorado) - Optimizados
    "secondary": {
        "500": "#E6B012",  # Color secundario
        "600": "#D4A212"
    },
    
    # Azules (complementarios) - Optimizados
    "blue": {
        "25": "#F7FAFC",
        "50": "#E6F0F7",
        "100": "#B3D4E8",
        "200": "#80B8D9",
        "500": "#186289",  # Azul medio
        "600": "#15587A",
        "700": "#124E6B",
        "800": "#0F445C",
        "900": "#003A5D",   # Azul marino
        "950": "#002A42"
    },
    
    # Grises - Sistema optimizado
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
        "800": "#14532D"
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
        "700": "#B91C1C"
    },
    
    "warning": {
        "25": "#FFFCF5",
        "50": "#FEF3C7",
        "100": "#FEF3C7",
        "200": "#FDE68A",
        "300": "#FCD34D",
        "400": "#FBBF24",  # Agregado el 400 faltante
        "500": "#F59E0B",  # Principal
        "700": "#B45309",
        "800": "#92400E"
    },
    
    "info": {
        "500": "#3B82F6"  # Principal
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
        "background": "#0a0b0d",           # Fondo sólido muy oscuro
        "surface": "#1a1b1e",             # Superficie principal
        "surface_secondary": "#242529",    # Superficie secundaria
        "surface_elevated": "#2d2f33",     # Superficie elevada
        "text_primary": COLORS["gray"]["100"],      # Texto principal
        "text_secondary": COLORS["gray"]["300"],    # Texto secundario
        "text_muted": COLORS["gray"]["500"],        # Texto desactivado
        "border": "#3a3b3f",              # Bordes principales
        "border_strong": "#4a4b4f",       # Bordes fuertes
        "primary": COLORS["primary"]["400"],        # Color primario
        "primary_hover": COLORS["primary"]["300"],  # Hover primario
        "primary_light": COLORS["primary"]["800"],  # Primario claro
        "shadow": "rgba(0, 0, 0, 0.5)",   # Sombras más pronunciadas
        "accent": COLORS["secondary"]["500"]        # Color de acento
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
# 🔮 EFECTOS GLASSMORPHISM SIMPLIFICADOS
# ==========================================

def glassmorphism_card(opacity: str = "90", blur: str = "20px") -> dict:
    """🔮 Función glassmorphism simplificada y eficiente"""
    return {
        "background": f"linear-gradient(135deg, {COLORS['gray']['900']}{opacity} 0%, {COLORS['gray']['800']}{opacity} 100%)",
        "backdrop_filter": f"blur({blur}) saturate(180%)",
        "border": f"1px solid {COLORS['primary']['500']}30",
        "box_shadow": f"""
            0 25px 50px -12px {COLORS['gray']['900']}80,
            0 0 0 1px {COLORS['primary']['500']}20,
            inset 0 1px 0 {COLORS['gray']['700']}50
        """,
        "border_radius": RADIUS["2xl"],
        "position": "relative"
    }

def glassmorphism_input() -> dict:
    """🔮 Input glassmorphism para formularios"""
    return {
        "background": f"{COLORS['gray']['800']}60",
        "backdrop_filter": "blur(10px)",
        "border": f"1px solid {COLORS['primary']['500']}30",
        "border_radius": RADIUS["md"],
        "color": COLORS["gray"]["50"],
        "_focus": {
            "border_color": COLORS["primary"]["400"],
            "box_shadow": f"0 0 0 3px {COLORS['primary']['500']}20",
            "background": f"{COLORS['gray']['700']}80"
        },
        "_hover": {
            "border_color": COLORS["primary"]["500"],
            "background": f"{COLORS['gray']['700']}70"
        }
    }



def primary_button() -> dict:
    """🔘 Botón primario turquesa con efectos premium"""
    return {
        "background": ROLE_THEMES['gerente']['gradient'],
        "border": f"1px solid {COLORS['primary']['700']}50",
        "border_radius": RADIUS["xl"],
        "color": "white",
        "font_weight": "600",
        "font_size": "1.1em",
        "padding": f"{SPACING['2']} {SPACING['4']}",
        "min_height": "48px",
        "cursor": "pointer",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "_hover": {
            "transform": "translateY(-2px)",
            "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['400']} 100%)",
            "box_shadow": f"0 8px 25px {COLORS['primary']['500']}40",
        },
        "_active": {
            "transform": "translateY(0px)"
        },
        "_disabled": {
            "opacity": "0.6",
            "cursor": "not-allowed",
            "transform": "none"
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
    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)",
    
    # 🌟 SOMBRAS CRISTALINAS AVANZADAS
    "crystal_sm": f"0 4px 12px rgba(28, 187, 186, 0.15), 0 2px 6px rgba(28, 187, 186, 0.1)",
    "crystal_md": f"0 8px 25px rgba(28, 187, 186, 0.2), 0 4px 10px rgba(28, 187, 186, 0.15)",
    "crystal_lg": f"0 15px 35px rgba(28, 187, 186, 0.25), 0 8px 15px rgba(28, 187, 186, 0.2)",
    "crystal_xl": f"0 25px 50px rgba(28, 187, 186, 0.3), 0 15px 25px rgba(28, 187, 186, 0.25)",
    
    "glow_primary": f"0 0 20px {COLORS['primary']['500']}40, 0 0 40px {COLORS['primary']['500']}20, 0 0 60px {COLORS['primary']['500']}10",
    "glow_secondary": f"0 0 20px {COLORS['secondary']['500']}40, 0 0 40px {COLORS['secondary']['500']}20",
    "glow_success": f"0 0 20px {COLORS['success']['500']}40, 0 0 40px {COLORS['success']['500']}20",
    
    "glass_light": "0 8px 32px rgba(255, 255, 255, 0.37), inset 0 1px 0 rgba(255, 255, 255, 0.5)",
    "glass_dark": "0 8px 32px rgba(0, 0, 0, 0.37), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
    "glass_colored": f"0 8px 32px {COLORS['primary']['500']}25, inset 0 1px 0 rgba(255, 255, 255, 0.3)",
    
    "neon_border": f"inset 0 0 10px {COLORS['primary']['500']}30, 0 0 10px {COLORS['primary']['500']}20",
    "premium_depth": "0 32px 64px rgba(0, 0, 0, 0.12), 0 16px 32px rgba(0, 0, 0, 0.08), 0 8px 16px rgba(0, 0, 0, 0.04)"
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
# 🎬 ANIMACIONES Y TRANSICIONES CRISTALINAS
# ==========================================

ANIMATIONS = {
    "duration": {
        "ultra_fast": "100ms",
        "fast": "150ms",
        "normal": "250ms", 
        "slow": "350ms",
        "slower": "500ms",
        "ultra_slow": "800ms"
    },
    
    "easing": {
        "linear": "linear",
        "ease": "ease",
        "ease_in": "ease-in",
        "ease_out": "ease-out", 
        "ease_in_out": "ease-in-out",
        "bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
        "smooth": "cubic-bezier(0.4, 0, 0.2, 1)",
        "crystal": "cubic-bezier(0.25, 0.46, 0.45, 0.94)",
        "elastic": "cubic-bezier(0.175, 0.885, 0.32, 1.275)",
        "premium": "cubic-bezier(0.23, 1, 0.32, 1)"
    },
    
    "presets": {
        "fade_in": "opacity 250ms ease-in-out",
        "slide_up": "transform 250ms ease-out", 
        "scale": "transform 150ms ease-out",
        "button_hover": "all 150ms ease-in-out",
        "modal": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)",
        "crystal_hover": "all 300ms cubic-bezier(0.25, 0.46, 0.45, 0.94)",
        "floating": "transform 3s ease-in-out infinite alternate",
        "pulse": "all 2s ease-in-out infinite",
        "glow": "box-shadow 300ms ease-in-out",
        "glass_hover": "all 200ms cubic-bezier(0.23, 1, 0.32, 1)",
        "premium_slide": "all 400ms cubic-bezier(0.25, 0.46, 0.45, 0.94)"
    },
    
    "keyframes": {
        "floating": {
            "0%": {"transform": "translateY(0px)"},
            "50%": {"transform": "translateY(-10px)"},
            "100%": {"transform": "translateY(0px)"}
        },
        "pulse_glow": {
            "0%": {"box-shadow": f"0 0 5px {COLORS['primary']['400']}, 0 0 10px {COLORS['primary']['400']}, 0 0 15px {COLORS['primary']['400']}"},
            "50%": {"box-shadow": f"0 0 10px {COLORS['primary']['500']}, 0 0 20px {COLORS['primary']['500']}, 0 0 30px {COLORS['primary']['500']}"},
            "100%": {"box-shadow": f"0 0 5px {COLORS['primary']['400']}, 0 0 10px {COLORS['primary']['400']}, 0 0 15px {COLORS['primary']['400']}"}
        },
        "shimmer": {
            "0%": {"background-position": "-200% center"},
            "100%": {"background-position": "200% center"}
        },
        "rotate_glow": {
            "0%": {"transform": "rotate(0deg)", "box-shadow": f"0 0 20px {COLORS['primary']['500']}40"},
            "100%": {"transform": "rotate(360deg)", "box-shadow": f"0 0 20px {COLORS['secondary']['500']}40"}
        },
        
        # 🦷 ANIMACIONES MÉDICAS ESPECÍFICAS PARA ODONTOGRAMA
        "pulse_urgent": {
            "0%, 100%": { 
                "box-shadow": "0 0 0 0 rgba(220, 38, 38, 0.7)",
                "border-color": "#dc2626"
            },
            "50%": { 
                "box-shadow": "0 0 0 10px rgba(220, 38, 38, 0)",
                "border-color": "#ef4444"
            }
        },
        
        "glow_healthy": {
            "0%, 100%": { 
                "box-shadow": "0 2px 8px rgba(22, 163, 74, 0.15)"
            },
            "50%": { 
                "box-shadow": "0 4px 16px rgba(22, 163, 74, 0.3)"
            }
        },
        
        "subtle_lift": {
            "0%": {"transform": "translateY(0px)"},
            "100%": {"transform": "translateY(-2px)"}
        },
        
        "medical_attention": {
            "0%": {"background-position": "-200% center"},
            "100%": {"background-position": "200% center"}
        },
        
        "tooth_selected": {
            "0%": {"transform": "scale(1)", "box-shadow": "0 2px 8px rgba(37, 99, 235, 0.15)"},
            "50%": {"transform": "scale(1.05)", "box-shadow": "0 8px 25px rgba(37, 99, 235, 0.4)"},
            "100%": {"transform": "scale(1.02)", "box-shadow": "0 6px 20px rgba(37, 99, 235, 0.3)"}
        }
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
            "border_radius": RADIUS["xl"],
            "border": f"1px solid {COLORS['gray']['300']}",
            # "padding": f"{SPACING['1']} {SPACING['2']}",
            "font_size": TYPOGRAPHY["font_size"]["base"],
            "transition": ANIMATIONS["presets"]["fade_in"],
            "_focus": {
                "outline": "none",
                "border_color": COLORS["primary"]["500"],
                "box_shadow": SHADOWS["xl"]
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

# ==========================================
# 🌈 GRADIENTES OPTIMIZADOS (SOLO UTILIZADOS)
# ==========================================

GRADIENTS = {
    # Gradientes activamente utilizados en el sistema
    "neon_primary": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['blue']['600']} 50%, {COLORS['primary']['600']} 100%)",
    "text_gradient_primary": f"linear-gradient(135deg, {COLORS['primary']['600']} 0%, {COLORS['blue']['500']} 100%)"
}

# ==========================================
# 🎭 EFECTOS GLASSMORPHISM OPTIMIZADOS (SOLO UTILIZADOS)
# ==========================================

GLASS_EFFECTS = {
    # Efectos activamente utilizados en el sistema
    "light": {
        "background": "rgba(255, 255, 255, 0.25)",
        "backdrop_filter": "blur(20px)",
        "border": "1px solid rgba(255, 255, 255, 0.18)",
        "box_shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.37)"
    },
    "medium": {
        "background": "rgba(255, 255, 255, 0.15)",
        "backdrop_filter": "blur(25px)",
        "border": "1px solid rgba(255, 255, 255, 0.25)",
        "box_shadow": "0 12px 40px 0 rgba(31, 38, 135, 0.4)"
    },
    "strong": {
        "background": "rgba(255, 255, 255, 0.1)",
        "backdrop_filter": "blur(30px)",
        "border": "1px solid rgba(255, 255, 255, 0.3)",
        "box_shadow": "0 16px 48px 0 rgba(31, 38, 135, 0.45)"
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

# Función get_responsive_value removida - no se usa en el proyecto actual

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

# Función create_theme_object removida - no se usa en el proyecto actual

# ==========================================
# 🌙 SISTEMA DE ESTILOS TEMA OSCURO REUTILIZABLE
# ==========================================

DARK_THEME_STYLES = {
    # Fondos profesionales
    "page_background": {
        "background": f"linear-gradient(180deg, {COLORS['blue']['950']} 0%,{COLORS['gray']['900']} 20%, {COLORS['gray']['950']} 100%);",
        "position": "relative",
        "_before": {
            "content": "''",
            "position": "absolute",
            "inset": "0",
            "background": f"""
                radial-gradient(circle at 15% 20%, {COLORS['primary']['500']}12 0%, transparent 50%),
                radial-gradient(circle at 85% 80%, {COLORS['secondary']['500']}08 0%, transparent 50%),
                radial-gradient(circle at 45% 10%, {COLORS['blue']['950']}06 0%, transparent 40%),
                radial-gradient(circle at 75% 40%, {COLORS['success']['500']}04 0%, transparent 30%)
            """,
            "pointer_events": "none",
            "z_index": "1"
        },
        "_after": {
            "content": "''",
            "position": "absolute",
            "inset": "0",
            "background": "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\" viewBox=\"0 0 100 100\"><defs><pattern id=\"grain\" width=\"100\" height=\"100\" patternUnits=\"userSpaceOnUse\"><circle cx=\"25\" cy=\"25\" r=\"0.5\" fill=\"%23ffffff\" opacity=\"0.02\"/><circle cx=\"75\" cy=\"25\" r=\"0.3\" fill=\"%23ffffff\" opacity=\"0.015\"/><circle cx=\"50\" cy=\"50\" r=\"0.4\" fill=\"%23ffffff\" opacity=\"0.02\"/><circle cx=\"25\" cy=\"75\" r=\"0.2\" fill=\"%23ffffff\" opacity=\"0.01\"/><circle cx=\"75\" cy=\"75\" r=\"0.6\" fill=\"%23ffffff\" opacity=\"0.025\"/></pattern></defs><rect width=\"100\" height=\"100\" fill=\"url(%23grain)\"/></svg>')",
            "opacity": "0.6",
            "pointer_events": "none",
            "z_index": "1"
        }
    },
    
    # Cards cristal reutilizables
    "crystal_card": {
        "background": "rgba(255, 255, 255, 0.08)",
        "backdrop_filter": "blur(20px) saturate(180%)",
        "border": "1px solid rgba(255, 255, 255, 0.2)",
        "border_radius": RADIUS["3xl"],
        "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
        "transition": "all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
        "position": "relative",
        "overflow": "hidden"
    },
    
    # Tabla oscura profesional
    "dark_table": {
        "background": "rgba(255, 255, 255, 0.05)",
        "backdrop_filter": "blur(20px) saturate(180%)",
        "border": "1px solid rgba(255, 255, 255, 0.1)",
        "border_radius": RADIUS["3xl"],
        "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
        "overflow": "hidden"
    },
    
    # Header de tabla
    "table_header": {
        "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
        "border_radius": RADIUS["xl"],
        "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
        "border": f"1px solid {DARK_THEME['colors']['border']}",
        "backdrop_filter": "blur(10px)"
    },
    
    # Input de búsqueda
    "search_input": {
        "background": DARK_THEME["colors"]["surface_secondary"],
        "border": f"2px solid {DARK_THEME['colors']['border']}",
        "border_radius": RADIUS["2xl"],
        "color": DARK_THEME["colors"]["text_primary"],
        "transition": "all 0.2s ease-in-out",
        "_focus": {
            "outline": "none",
            "border_color": COLORS["primary"]["400"],
            "box_shadow": f"0 0 12px {COLORS['primary']['400']}40",
            "background": DARK_THEME["colors"]["surface_elevated"]
        },
        "_hover": {
            "border_color": COLORS["primary"]["300"],
            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.2)"
        }
    },
    
    # Sidebar cristal
    "sidebar": {
        "background": "rgba(255, 255, 255, 0.06)",
        "backdrop_filter": "blur(25px) saturate(150%)",
        "border_right": "1px solid rgba(255, 255, 255, 0.15)",
        "box_shadow": "4px 0 24px rgba(0, 0, 0, 0.4), inset 1px 0 0 rgba(255, 255, 255, 0.1)",
        "position": "relative"
    }
}

# ==========================================
# 🎯 ESTILOS ESPECÍFICOS DENTALES EXPANDIDOS
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
    
    "consultation_status": {
        "scheduled": COLORS["info"]["500"],
        "confirmed": COLORS["primary"]["500"],
        "waiting": COLORS["warning"]["500"],
        "in_progress": COLORS["info"]["500"],
        "completed": COLORS["success"]["500"],
        "cancelled": COLORS["error"]["500"],
        "no_show": COLORS["gray"]["500"]
    },
    
    "priority_system": {
        "urgent": {
            "color": "#dc2626",
            "background": "rgba(220, 38, 38, 0.1)",
            "border": "rgba(220, 38, 38, 0.3)",
            "icon": "🚨"
        },
        "high": {
            "color": "#ea580c",
            "background": "rgba(234, 88, 12, 0.1)", 
            "border": "rgba(234, 88, 12, 0.3)",
            "icon": "⚡"
        },
        "normal": {
            "color": COLORS["gray"]["500"],
            "background": "rgba(107, 114, 128, 0.1)",
            "border": "rgba(107, 114, 128, 0.3)",
            "icon": "📋"
        }
    }
}

# ==========================================
# 🏥 COLORES ESPECÍFICOS MÉDICOS EXPANDIDOS
# ==========================================

MEDICAL_COLORS = {
    # Estados de consulta médica
    "consultation": {
        "waiting": COLORS["warning"]["500"],
        "in_progress": COLORS["info"]["500"], 
        "completed": COLORS["success"]["500"],
        "cancelled": COLORS["error"]["500"],
        "urgent": "#dc2626",
        "high_priority": "#ea580c",
        "normal_priority": COLORS["gray"]["500"]
    },
    
    # Colores específicos dental tema oscuro
    "dark_medical": {
        "background": "#0f1419",
        "surface": "#1a1f2e",
        "surface_hover": "#252b3a",
        "border": "#2d3748",
        "border_hover": "#4a5568",
        "text_primary": "#f7fafc",
        "text_secondary": "#a0aec0",
        "text_muted": "#718096",
        "glass_bg": "rgba(26, 31, 46, 0.8)",
        "glass_border": "rgba(255, 255, 255, 0.1)",
        "accent_cyan": COLORS["primary"]["400"],
        "accent_turquoise": "#1CBBBA"
    }
}

# ==========================================
# 🛠️ FUNCIONES UTILITARIAS TEMA OSCURO
# ==========================================

def create_dark_style(
    style_key: Optional[str] = None,
    base_style: Optional[Dict[str, Any]] = None,
    custom_logic: Optional[callable] = None,
    **overrides
) -> Dict[str, Any]:
    """
    🎨 Función genérica OPTIMIZADA para crear estilos de tema oscuro reutilizables
    
    Args:
        style_key: Clave en DARK_THEME_STYLES para usar como base
        base_style: Diccionario de estilo base personalizado
        custom_logic: Función que recibe (**kwargs) y retorna Dict para lógica específica
        **overrides: Propiedades CSS que sobrescriben el estilo base
        
    Returns:
        Dict con el estilo CSS final
        
    Examples:
        # Patrón simple (usa DARK_THEME_STYLES)
        create_dark_style("crystal_card")
        
        # Patrón médico específico
        create_dark_style("medical_card", priority="urgent")
        
        # Patrón con lógica personalizada
        create_dark_style(
            custom_logic=lambda color=None, **kw: {"background": color} if color else {},
            color="#123456"
        )
    """
    final_style = {}
    
    # 1. Aplicar estilo base desde DARK_THEME_STYLES si se especifica
    if style_key and style_key in DARK_THEME_STYLES:
        final_style = DARK_THEME_STYLES[style_key].copy()
    
    # 2. Aplicar estilo base personalizado
    elif base_style:
        final_style = base_style.copy()
    
    # 3. Aplicar lógica personalizada si existe
    if custom_logic and callable(custom_logic):
        try:
            custom_result = custom_logic(**overrides)
            if isinstance(custom_result, dict):
                final_style.update(custom_result)
        except Exception:
            # Fallback silencioso si la lógica personalizada falla
            pass
    
    # 4. Aplicar overrides finales
    final_style.update(overrides)
    
    return final_style

def dark_page_background(**overrides) -> Dict[str, Any]:
    """🌙 Fondo de página profesional para tema oscuro"""
    return create_dark_style("page_background", **overrides)

def dark_crystal_card(color: str = None, hover_lift: str = "6px", **overrides) -> Dict[str, Any]:
    """💎 Card cristal con color personalizable"""
    base_style = DARK_THEME_STYLES["crystal_card"].copy()
    
    if color:
        # Agregar efectos de color específico
        base_style.update({
            "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.5), 0 4px 16px {color}20, inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "_hover": {
                "transform": f"translateY(-{hover_lift})",
                "box_shadow": f"0 12px 40px rgba(0, 0, 0, 0.6), 0 8px 24px {color}30, inset 0 1px 0 rgba(255, 255, 255, 0.2)",
                "border_color": "rgba(255, 255, 255, 0.3)",
                "background": "rgba(255, 255, 255, 0.12)"
            },
            # Borde superior con glow
            "_before": {
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "height": "2px",
                "background": f"linear-gradient(90deg, transparent 0%, {color} 50%, transparent 100%)",
                "opacity": "0.9",
                "box_shadow": f"0 0 8px {color}60"
            }
        })
    
    base_style.update(overrides)
    return base_style

def dark_sidebar_style(**overrides) -> Dict[str, Any]:
    """🎭 Estilo de sidebar profesional con glassmorphism"""
    return create_dark_style("sidebar", **overrides)

def dark_table_container(**overrides) -> Dict[str, Any]:
    """📊 Contenedor de tabla con efectos cristal"""
    return create_dark_style("dark_table", **overrides)

def dark_header_style(gradient_colors: List[str] = None, **overrides) -> Dict[str, Any]:
    """📋 Header profesional con gradiente personalizable"""
    def _header_logic(gradient_colors=None, **kwargs):
        if not gradient_colors:
            gradient_colors = [DARK_THEME["colors"]["surface"], DARK_THEME["colors"]["surface_secondary"]]
        
        return {
            "background": f"linear-gradient(135deg, {gradient_colors[0]} 0%, {gradient_colors[1]} 100%)",
            "border_radius": RADIUS["xl"],
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
            "border": f"1px solid {DARK_THEME['colors']['border']}",
            "backdrop_filter": "blur(10px)",
            "padding": f"{SPACING['3']} {SPACING['6']}",
            "border_bottom": f"1px solid {DARK_THEME['colors']['border']}"
        }
    
    return create_dark_style(
        custom_logic=_header_logic,
        gradient_colors=gradient_colors,
        **overrides
    )

def dark_search_input(**overrides) -> Dict[str, Any]:
    """🔍 Input de búsqueda con tema oscuro"""
    return create_dark_style("search_input", **overrides)

def dark_nav_item_style(color: str = None) -> Dict[str, Any]:
    """🧭 Estilo base para items de navegación (sin lógica condicional)"""
    def _nav_logic(color=None, **kwargs):
        if not color:
            color = COLORS["primary"]["500"]
        
        return {
            "background": "transparent",
            "color": DARK_THEME["colors"]["text_secondary"],
            "border_radius": RADIUS["lg"],
            "transition": "all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
            "position": "relative",
            "_hover": {
                "background": "rgba(255, 255, 255, 0.08)",
                "color": DARK_THEME["colors"]["text_primary"],
                "transform": "translateX(2px)",
                "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.2)"
            }
        }
    
    return create_dark_style(custom_logic=_nav_logic, color=color)

def dark_nav_item_active_style(color: str = None) -> Dict[str, Any]:
    """🧭 Estilo para items de navegación activos"""
    def _nav_active_logic(color=None, **kwargs):
        if not color:
            color = COLORS["primary"]["500"]
        
        return {
            "background": f"linear-gradient(135deg, {color}40 0%, {color}20 100%)",
            "border": f"1px solid {color}60",
            "border_radius": RADIUS["xl"],
            "color": "white",
            "box_shadow": f"0 4px 12px {color}30, inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "transform": "translateX(4px)",
            "backdrop_filter": "blur(10px)",
            "position": "relative",
            "_before": {
                "content": "''",
                "position": "absolute",
                "left": "0",
                "top": "50%",
                "transform": "translateY(-50%)",
                "width": "4px",
                "height": "60%",
                "background": f"linear-gradient(to bottom, {color} 0%, transparent 100%)",
                "border_radius": "0 4px 4px 0",
                "box_shadow": f"0 0 8px {color}80"
            }
        }
    
    return create_dark_style(custom_logic=_nav_active_logic, color=color)

# ==========================================
# 🌟 FUNCIONES DE CONVENIENCIA ADICIONALES
# ==========================================

def create_button_style(variant: str = "primary", size: str = "md", **overrides) -> Dict[str, Any]:
    """🔘 Crear estilo de botón usando la función genérica"""
    def _button_logic(variant="primary", size="md", **kwargs):
        base = COMPONENT_STYLES["button"]["base"].copy()
        base.update(COMPONENT_STYLES["button"]["sizes"].get(size, {}))
        base.update(COMPONENT_STYLES["button"]["variants"].get(variant, {}))
        return base
    
    return create_dark_style(
        custom_logic=_button_logic,
        variant=variant,
        size=size,
        **overrides
    )

def create_input_style(focus_color: str = None, **overrides) -> Dict[str, Any]:
    """📝 Crear estilo de input usando la función genérica"""
    def _input_logic(focus_color=None, **kwargs):
        if not focus_color:
            focus_color = COLORS["primary"]["500"]
        
        base = COMPONENT_STYLES["input"]["base"].copy()
        base["_focus"]["border_color"] = focus_color
        return base
    
    return create_dark_style(
        custom_logic=_input_logic,
        focus_color=focus_color,
        **overrides
    )

def create_card_style(variant: str = "base", shadow_level: str = "md", **overrides) -> Dict[str, Any]:
    """💳 Crear estilo de card usando la función genérica"""
    def _card_logic(variant="base", shadow_level="md", **kwargs):
        base = COMPONENT_STYLES["card"]["base"].copy()
        base.update(COMPONENT_STYLES["card"]["variants"].get(variant, {}))
        base["box_shadow"] = SHADOWS.get(shadow_level, SHADOWS["md"])
        return base
    
    return create_dark_style(
        custom_logic=_card_logic,
        variant=variant,
        shadow_level=shadow_level,
        **overrides
    )

def create_gradient_background(color1: str, color2: str, direction: str = "135deg", **overrides) -> Dict[str, Any]:
    """🌈 Crear fondo con gradiente usando la función genérica"""
    gradient_style = {
        "background": f"linear-gradient({direction}, {color1} 0%, {color2} 100%)"
    }
    
    return create_dark_style(
        base_style=gradient_style,
        **overrides
    )

def create_glass_effect(intensity: str = "medium", tint_color: str = None, **overrides) -> Dict[str, Any]:
    """🔮 Crear efecto glassmorphism usando la función genérica"""
    def _glass_logic(intensity="medium", tint_color=None, **kwargs):
        if tint_color:
            # Efecto glass con color personalizado
            return {
                "background": f"{tint_color}15",
                "backdrop_filter": "blur(20px)",
                "border": f"1px solid {tint_color}30",
                "box_shadow": f"0 12px 40px 0 {tint_color}25"
            }
        else:
            # Usar efecto predefinido
            return GLASS_EFFECTS.get(intensity, GLASS_EFFECTS["medium"])
    
    return create_dark_style(
        custom_logic=_glass_logic,
        intensity=intensity,
        tint_color=tint_color,
        **overrides
    )

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
    "DARK_THEME_STYLES",
    
    # 🌟 Elementos cristalinos utilizados
    "GRADIENTS",
    "GLASS_EFFECTS",
    
    # Funciones de utilidad activamente usadas
    "get_color",
    "get_role_theme",
    "create_gradient",
    "darken_color",
    "lighten_color", 
    "get_contrast_color",
    
    # 🌙 Funciones tema oscuro activamente usadas
    "create_dark_style",      # 🌟 NUEVA FUNCIÓN GENÉRICA
    "dark_page_background",
    "dark_crystal_card", 
    "dark_sidebar_style",
    "dark_table_container",
    "dark_header_style",
    "dark_search_input",
    "dark_nav_item_style",
    "dark_nav_item_active_style",
    
    # 🌟 Funciones de conveniencia nuevas
    "create_button_style",
    "create_input_style",
    "create_card_style",
    "create_gradient_background",
    "create_glass_effect",
    
    # Estilos especializados
    "botton_login",
    "input_login",
    
    # Funciones médicas específicas optimizadas
    "MEDICAL_COLORS",
    "create_medical_card_style",
    "create_priority_badge_style", 
    "create_consultation_status_style"
]

# ==========================================
# 🏥 FUNCIONES MÉDICAS ESPECÍFICAS OPTIMIZADAS
# ==========================================

def create_medical_card_style(priority: str = "normal", status: str = "waiting", **overrides) -> Dict[str, Any]:
    """
    🏥 Crear tarjeta médica con prioridad y estado visual
    
    Args:
        priority: 'urgent', 'high', 'normal'
        status: 'waiting', 'in_progress', 'completed', 'cancelled'
        **overrides: Propiedades adicionales CSS
    
    Returns:
        Dict con estilo CSS completo para tarjeta médica
    """
    def _medical_logic(priority="normal", status="waiting", **kwargs):
        base_style = DARK_THEME_STYLES["crystal_card"].copy()
        
        # Obtener colores según prioridad
        priority_config = DENTAL_SPECIFIC["priority_system"].get(priority, DENTAL_SPECIFIC["priority_system"]["normal"])
        status_color = DENTAL_SPECIFIC["consultation_status"].get(status, COLORS["gray"]["500"])
        
        # Personalización por prioridad
        if priority == "urgent":
            base_style.update({
                "border_left": f"4px solid {priority_config['color']}",
                "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.5), 0 4px 16px {priority_config['color']}30, inset 0 1px 0 rgba(255, 255, 255, 0.1)",
                "_hover": {
                    "transform": "translateY(-6px)",
                    "box_shadow": f"0 20px 40px rgba(0, 0, 0, 0.6), 0 8px 24px {priority_config['color']}40",
                    "border_color": "rgba(255, 255, 255, 0.3)"
                }
            })
        elif priority == "high":
            base_style.update({
                "border_left": f"3px solid {priority_config['color']}",
                "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.5), 0 2px 8px {priority_config['color']}20, inset 0 1px 0 rgba(255, 255, 255, 0.1)"
            })
        
        # Personalización por estado
        if status == "in_progress":
            base_style.update({
                "background": "rgba(255, 255, 255, 0.12)",
                "_after": {
                    "content": "''",
                    "position": "absolute",
                    "top": "0",
                    "left": "0", 
                    "right": "0",
                    "height": "2px",
                    "background": f"linear-gradient(90deg, transparent 0%, {status_color} 50%, transparent 100%)",
                    "animation": "shimmer 2s infinite"
                }
            })
        elif status == "completed":
            base_style.update({
                "opacity": "0.8",
                "background": "rgba(255, 255, 255, 0.05)"
            })
        
        return base_style
    
    return create_dark_style(
        custom_logic=_medical_logic,
        priority=priority,
        status=status,
        **overrides
    )

def create_priority_badge_style(priority: str = "normal", **overrides) -> Dict[str, Any]:
    """
    🚨 Crear badge de prioridad con colores y efectos específicos
    
    Args:
        priority: 'urgent', 'high', 'normal'
        **overrides: Propiedades adicionales CSS
    
    Returns:
        Dict con estilo CSS para badge de prioridad
    """
    priority_config = DENTAL_SPECIFIC["priority_system"].get(priority, DENTAL_SPECIFIC["priority_system"]["normal"])
    
    base_style = {
        "background": priority_config["background"],
        "border": f"1px solid {priority_config['border']}",
        "color": priority_config["color"],
        "border_radius": RADIUS["lg"],
        "padding": f"{SPACING['1']} {SPACING['2']}",
        "font_size": TYPOGRAPHY["font_size"]["xs"],
        "font_weight": TYPOGRAPHY["font_weight"]["bold"],
        "text_transform": "uppercase",
        "letter_spacing": "0.05em",
        "backdrop_filter": "blur(10px)",
        "transition": ANIMATIONS["presets"]["fade_in"]
    }
    
    rx.cond(
        priority == "urgent",
        base_style.update({
            "animation": "pulse 2s infinite",
            "box_shadow": f"0 2px 8px {priority_config['color']}30"
        }),
        rx.fragment()
    )
    
    base_style.update(overrides)
    return base_style

def create_consultation_status_style(status: str = "waiting", size: str = "md", **overrides) -> Dict[str, Any]:
    """
    📊 Crear indicador de estado de consulta
    
    Args:
        status: 'waiting', 'in_progress', 'completed', 'cancelled'
        size: 'sm', 'md', 'lg'
        **overrides: Propiedades adicionales CSS
    
    Returns:
        Dict con estilo CSS para indicador de estado
    """
    status_color = DENTAL_SPECIFIC["consultation_status"].get(status, COLORS["gray"]["500"])
    
    sizes = {
        "sm": {"padding": f"{SPACING['1']} {SPACING['2']}", "font_size": TYPOGRAPHY["font_size"]["2xs"]},
        "md": {"padding": f"{SPACING['2']} {SPACING['3']}", "font_size": TYPOGRAPHY["font_size"]["xs"]},
        "lg": {"padding": f"{SPACING['2.5']} {SPACING['4']}", "font_size": TYPOGRAPHY["font_size"]["sm"]}
    }
    
    base_style = {
        "background": f"{status_color}20",
        "border": f"1px solid {status_color}40",
        "color": status_color,
        "border_radius": RADIUS["xl"],
        "font_weight": TYPOGRAPHY["font_weight"]["semibold"],
        "text_align": "center",
        "backdrop_filter": "blur(10px)",
        "transition": ANIMATIONS["presets"]["fade_in"],
        **sizes.get(size, sizes["md"])
    }
    
    rx.cond(
        status == "in_progress",
        base_style.update({
            "animation": "pulse 2s infinite"
        }),
        rx.cond(
            status == "completed",
            base_style.update({
            "background": f"{COLORS['success']['500']}15",
            "border_color": f"{COLORS['success']['500']}40",
            "color": COLORS["success"]["500"]
            }),
            rx.fragment(),
        ),
        
    )


    base_style.update(overrides)
    return base_style


# ==========================================
# 🏥 ESTILOS MÉDICOS PROFESIONALES
# ==========================================

MEDICAL_PROFESSIONAL_COLORS = {
    # Paleta médica especializada para historial odontológico
    "medical_primary": "#0066CC",      # Azul médico confiable
    "medical_secondary": "#00A896",    # Verde médico (salud)
    "medical_accent": "#FF6B35",       # Naranja médico (atención)

    # Estados dentales con códigos de color médicos
    "tooth_healthy": "#90EE90",        # Verde claro - diente sano
    "tooth_caries": "#FF4500",         # Rojo naranja - caries
    "tooth_filled": "#C0C0C0",         # Plata - obturado
    "tooth_crown": "#4169E1",          # Azul real - corona
    "tooth_extraction": "#8B0000",     # Rojo oscuro - extracción
    "tooth_implant": "#32CD32",        # Verde lima - implante
    "tooth_endodontics": "#FFD700",    # Dorado - endodoncia
    "tooth_missing": "#FFFFFF",        # Blanco - ausente

    # Gradientes médicos profesionales
    "medical_bg_gradient": "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0f9ff 100%)",
    "medical_card_gradient": "linear-gradient(135deg, rgba(0,102,204,0.05) 0%, rgba(0,168,150,0.05) 100%)",
    "medical_header_gradient": "linear-gradient(90deg, #0066CC 0%, #00A896 100%)",

    # Sombras médicas
    "medical_shadow_light": "0 1px 3px rgba(0,102,204,0.1)",
    "medical_shadow_medium": "0 4px 12px rgba(0,102,204,0.15)",
    "medical_shadow_heavy": "0 8px 30px rgba(0,102,204,0.2)",

    # Bordes médicos
    "medical_border_light": "1px solid rgba(0,102,204,0.1)",
    "medical_border_medium": "1px solid rgba(0,102,204,0.2)",
    "medical_border_focus": "2px solid rgba(0,102,204,0.4)",
}

MEDICAL_TYPOGRAPHY = {
    # Tipografía médica especializada
    "medical_title": {
        "font_family": "'Inter', 'Segoe UI', system-ui, sans-serif",
        "font_weight": "600",
        "letter_spacing": "-0.025em",
        "line_height": "1.2",
        "color": MEDICAL_PROFESSIONAL_COLORS["medical_primary"]
    },

    "medical_subtitle": {
        "font_family": "'Inter', 'Segoe UI', system-ui, sans-serif",
        "font_weight": "500",
        "letter_spacing": "-0.015em",
        "line_height": "1.4",
        "color": MEDICAL_PROFESSIONAL_COLORS["medical_secondary"]
    },

    "medical_body": {
        "font_family": "'Inter', 'Segoe UI', system-ui, sans-serif",
        "font_weight": "400",
        "line_height": "1.6",
        "color": MEDICAL_PROFESSIONAL_COLORS["medical_primary"]
    },

    "medical_code": {
        "font_family": "'JetBrains Mono', 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace",
        "font_weight": "500",
        "font_size": "0.875em",
        "color": MEDICAL_PROFESSIONAL_COLORS["medical_accent"]
    }
}

def medical_card_style(variant: str = "default", **overrides) -> Dict[str, Any]:
    """
    🏥 Crear estilo de card médico profesional

    Args:
        variant: 'default', 'elevated', 'outline', 'filled'
        **overrides: Propiedades adicionales CSS

    Returns:
        Dict con estilo CSS para card médico
    """
    base_style = {
        "background": "rgba(255, 255, 255, 0.95)",
        "backdrop_filter": "blur(10px)",
        "border_radius": RADIUS["lg"],
        "padding": SPACING["4"],
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "position": "relative",
        "_hover": {
            "transform": "translateY(-2px)",
            "box_shadow": MEDICAL_PROFESSIONAL_COLORS["medical_shadow_medium"]
        }
    }

    variants = {
        "default": {
            "border": MEDICAL_PROFESSIONAL_COLORS["medical_border_light"],
            "box_shadow": MEDICAL_PROFESSIONAL_COLORS["medical_shadow_light"]
        },
        "elevated": {
            "border": "none",
            "box_shadow": MEDICAL_PROFESSIONAL_COLORS["medical_shadow_heavy"],
            "background": MEDICAL_PROFESSIONAL_COLORS["medical_card_gradient"]
        },
        "outline": {
            "border": MEDICAL_PROFESSIONAL_COLORS["medical_border_medium"],
            "box_shadow": "none",
            "background": "transparent"
        },
        "filled": {
            "border": "none",
            "background": MEDICAL_PROFESSIONAL_COLORS["medical_card_gradient"],
            "box_shadow": "inset 0 1px 0 rgba(255,255,255,0.1)"
        }
    }

    base_style.update(variants.get(variant, variants["default"]))
    base_style.update(overrides)
    return base_style

def medical_button_style(intent: str = "primary", size: str = "md", **overrides) -> Dict[str, Any]:
    """
    🏥 Crear estilo de botón médico profesional

    Args:
        intent: 'primary', 'secondary', 'success', 'warning', 'danger'
        size: 'sm', 'md', 'lg'
        **overrides: Propiedades adicionales CSS

    Returns:
        Dict con estilo CSS para botón médico
    """
    sizes = {
        "sm": {
            "padding": f"{SPACING['1.5']} {SPACING['3']}",
            "font_size": TYPOGRAPHY["font_size"]["sm"],
            "min_height": "32px"
        },
        "md": {
            "padding": f"{SPACING['2.5']} {SPACING['4']}",
            "font_size": TYPOGRAPHY["font_size"]["base"],
            "min_height": "40px"
        },
        "lg": {
            "padding": f"{SPACING['3']} {SPACING['6']}",
            "font_size": TYPOGRAPHY["font_size"]["lg"],
            "min_height": "48px"
        }
    }

    intents = {
        "primary": {
            "background": MEDICAL_PROFESSIONAL_COLORS["medical_primary"],
            "color": "white",
            "_hover": {
                "background": "#0052A3",
                "box_shadow": f"0 4px 20px {MEDICAL_PROFESSIONAL_COLORS['medical_primary']}40"
            }
        },
        "secondary": {
            "background": MEDICAL_PROFESSIONAL_COLORS["medical_secondary"],
            "color": "white",
            "_hover": {
                "background": "#008C7A",
                "box_shadow": f"0 4px 20px {MEDICAL_PROFESSIONAL_COLORS['medical_secondary']}40"
            }
        },
        "success": {
            "background": COLORS["success"]["500"],
            "color": "white",
            "_hover": {
                "background": COLORS["success"]["600"],
                "box_shadow": f"0 4px 20px {COLORS['success']['500']}40"
            }
        },
        "warning": {
            "background": COLORS["warning"]["500"],
            "color": "white",
            "_hover": {
                "background": COLORS["warning"]["600"],
                "box_shadow": f"0 4px 20px {COLORS['warning']['500']}40"
            }
        },
        "danger": {
            "background": COLORS["error"]["500"],
            "color": "white",
            "_hover": {
                "background": COLORS["error"]["600"],
                "box_shadow": f"0 4px 20px {COLORS['error']['500']}40"
            }
        }
    }

    base_style = {
        "border": "none",
        "border_radius": RADIUS["md"],
        "font_weight": TYPOGRAPHY["font_weight"]["semibold"],
        "cursor": "pointer",
        "transition": "all 0.2s ease",
        "display": "inline-flex",
        "align_items": "center",
        "justify_content": "center",
        "text_align": "center",
        "white_space": "nowrap",
        "_focus": {
            "outline": "2px solid",
            "outline_color": f"{MEDICAL_PROFESSIONAL_COLORS['medical_primary']}50",
            "outline_offset": "2px"
        },
        "_disabled": {
            "opacity": "0.6",
            "cursor": "not-allowed",
            "pointer_events": "none"
        }
    }

    base_style.update(sizes.get(size, sizes["md"]))
    base_style.update(intents.get(intent, intents["primary"]))
    base_style.update(overrides)
    return base_style

def tooth_visualization_style(condition: str = "healthy", selected: bool = False, **overrides) -> Dict[str, Any]:
    """
    🦷 Crear estilo de visualización de diente para odontograma

    Args:
        condition: 'healthy', 'caries', 'filled', 'crown', 'extraction', 'implant', 'endodontics', 'missing'
        selected: True si el diente está seleccionado
        **overrides: Propiedades adicionales CSS

    Returns:
        Dict con estilo CSS para visualización de diente
    """
    condition_colors = {
        "healthy": MEDICAL_PROFESSIONAL_COLORS["tooth_healthy"],
        "caries": MEDICAL_PROFESSIONAL_COLORS["tooth_caries"],
        "filled": MEDICAL_PROFESSIONAL_COLORS["tooth_filled"],
        "crown": MEDICAL_PROFESSIONAL_COLORS["tooth_crown"],
        "extraction": MEDICAL_PROFESSIONAL_COLORS["tooth_extraction"],
        "implant": MEDICAL_PROFESSIONAL_COLORS["tooth_implant"],
        "endodontics": MEDICAL_PROFESSIONAL_COLORS["tooth_endodontics"],
        "missing": MEDICAL_PROFESSIONAL_COLORS["tooth_missing"]
    }

    base_color = condition_colors.get(condition, condition_colors["healthy"])

    base_style = {
        "background": base_color,
        "border": f"1px solid {base_color}80",
        "border_radius": RADIUS["md"],
        "width": "35px",
        "height": "35px",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "cursor": "pointer",
        "transition": "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
        "font_weight": TYPOGRAPHY["font_weight"]["bold"],
        "font_size": TYPOGRAPHY["font_size"]["xs"],
        "_hover": {
            "transform": "scale(1.05)",
            "box_shadow": f"0 4px 20px {base_color}40",
            "border": f"2px solid {MEDICAL_PROFESSIONAL_COLORS['medical_accent']}"
        }
    }

    # Estilo cuando está seleccionado
    if selected:
        base_style.update({
            "border": f"2px solid {MEDICAL_PROFESSIONAL_COLORS['medical_primary']}",
            "box_shadow": f"0 0 0 2px {MEDICAL_PROFESSIONAL_COLORS['medical_primary']}40",
            "transform": "scale(1.1)"
        })

    # Ajustes específicos por condición
    if condition == "missing":
        base_style.update({
            "background": "transparent",
            "border": f"2px dashed {COLORS['gray']['300']}",
            "color": COLORS["gray"]["500"]
        })
    elif condition == "extraction":
        base_style.update({
            "background": f"linear-gradient(45deg, {base_color}, transparent 50%)",
            "position": "relative"
        })

    base_style.update(overrides)
    return base_style

# Export de todos los estilos médicos
MEDICAL_STYLES = {
    "colors": MEDICAL_PROFESSIONAL_COLORS,
    "typography": MEDICAL_TYPOGRAPHY,
    "card": medical_card_style,
    "button": medical_button_style,
    "tooth": tooth_visualization_style
}