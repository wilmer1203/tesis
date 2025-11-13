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
        "200": "#80E0FF",
        "300": "#4DD4FF",
        "400": "#1AC8FF",
        "500": "#00BCD4",  # Color principal turquesa vibrante
        "600": "#00ACC1",
        "800": "#00838F",
    },
    
    # Colores secundarios (dorado) - Optimizados
    "secondary": {
        "500": "#E6B012",  # Color secundario
        "600": "#D4A212"
    },
    
    # Azules (complementarios) - Optimizados
    "blue": {
        "200": "#80B8D9",
        "500": "#186289",  
        "600": "#15587A",
        "900": "#003A5D",   
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
        "200": "#86EFAC",
        "300": "#4ADE80",
        "400": "#22C55E",
        "500": "#16A34A",  # Principal
        "600": "#15803D",
        "700": "#166534",
        "800": "#14532D"
    },
    
    "error": {
        "300": "#FCA5A5",
        "400": "#F87171",
        "500": "#EF4444",  # Principal
        "600": "#DC2626",
        "700": "#B91C1C"
    },
    
    "warning": {
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



def primary_button() -> dict:
    """🔘 Botón primario turquesa con efectos premium"""
    return {
        "background": GRADIENTS['text_gradient_primary'],
        "border": f"1px solid {COLORS['primary']['800']}50",
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
# 🌈 GRADIENTES OPTIMIZADOS (SOLO UTILIZADOS)
# ==========================================

GRADIENTS = {
    # Gradientes activamente utilizados en el sistema
    "neon_primary": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['blue']['600']} 50%, {COLORS['primary']['600']} 100%)",
    "text_gradient_primary": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['blue']['600']} 100%)"
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

# ==========================================
# 🌙 SISTEMA DE ESTILOS TEMA OSCURO REUTILIZABLE
# ==========================================

DARK_THEME_STYLES = {
    # Fondos profesionales
    "page_background": {
        "background": f"linear-gradient(180deg, {COLORS['blue']['950']} 0%,{COLORS['gray']['900']} 20%, {COLORS['gray']['950']} 100%);",
         "background-attachment": "fixed",
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
        "background": "rgba(255, 255, 255,  0.0)",
        "border": "1px solid rgba(255, 255, 255, 0.2)",
        "border_radius": RADIUS["2xl"],
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

def dark_crystal_card(color: str = "", hover_lift: str = "6px", padding: str = SPACING["6"], **overrides) -> Dict[str, Any]:
    """💎 Card cristal con color personalizable y padding por defecto

    Args:
        color: Color de acento opcional para efectos visuales (puede ser un Var de Reflex)
        hover_lift: Altura del efecto hover (default: "6px")
        padding: Padding interno del card (default: SPACING["6"] = 24px)
        **overrides: Estilos adicionales para sobreescribir
    """
    base_style = DARK_THEME_STYLES["crystal_card"].copy()

    # Agregar padding por defecto
    base_style["padding"] = padding

    # Siempre agregar efectos de color (funciona con Vars de Reflex también)
    # Si color está vacío, los efectos simplemente no se notarán
    base_style.update({
        "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.5), 0 4px 16px {color}20, inset 0 1px 0 rgba(255, 255, 255, 0.1)",
        "_hover": {
            "transform": f"translateY(-{hover_lift})",
            "box_shadow": f"0 12px 40px rgba(0, 0, 0, 0.4), 0 8px 24px {color}30, inset 0 1px 0 rgba(255, 255, 255, 0.2)",
            "border": f"1px solid {color}",
            "background": "rgba(255, 255, 255, 0.03)"
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
    

# ==========================================
# 📤 EXPORTS
# ==========================================

__all__ = [
    # Colores y temas
    "COLORS",
    "DARK_THEME", 
    # Espaciado y dimensiones
    "SPACING",
    "RADIUS", 
    "SHADOWS",
    "TYPOGRAPHY",
    "ANIMATIONS",
    "BREAKPOINTS",
    # Componentes
    "DENTAL_SPECIFIC",
    "DARK_THEME_STYLES",
    # 🌟 Elementos cristalinos utilizados
    "GRADIENTS",
    "GLASS_EFFECTS",
    # 🌙 Funciones tema oscuro activamente usadas
    "create_dark_style",      # 🌟 NUEVA FUNCIÓN GENÉRICA
    "dark_crystal_card", 
    "dark_header_style",

]


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

