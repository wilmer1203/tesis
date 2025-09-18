# 🦷 COMPONENTE: DIENTE INTERACTIVO CON 5 SUPERFICIES
# dental_system/components/odontologia/interactive_tooth.py

import reflex as rx
from typing import Dict, Optional, Any
from dental_system.state.app_state import AppState
from dental_system.models.odontologia_models import DienteModel, CondicionDienteModel
from dental_system.services.odontograma_service import odontograma_service
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS, ANIMATIONS

# ==========================================
# 🎨 CONFIGURACIÓN DE COLORES Y CONDICIONES
# ==========================================

# Sistema de colores médico profesional basado en convenciones internacionales
MEDICAL_CONDITION_PALETTE = {
    # Estados básicos - Paleta médica profesional
    "sano": {
        "bg": "#dcfce7",        # Verde más visible para testing
        "border": "#16a34a",    # Verde médico estándar
        "text": "#14532d",
        "shadow": "0 2px 8px rgba(22, 163, 74, 0.15)",
        "hover_bg": "#bbf7d0",  # Verde aún más brillante en hover
        "hover_shadow": "0 8px 25px rgba(22, 163, 74, 0.3)"
    },
    
    # Patología - Rojo médico con urgencia visual
    "caries": {
        "bg": "#fef2f2",        # Rojo muy suave
        "border": "#dc2626",    # Rojo médico de alerta
        "text": "#7f1d1d",
        "shadow": "0 2px 8px rgba(220, 38, 38, 0.2)",
        "hover_bg": "#fee2e2",
        "hover_shadow": "0 8px 25px rgba(220, 38, 38, 0.4)",
        "pulse": True           # Animación para casos urgentes
    },
    
    # Restauraciones - Azul médico confiable
    "obturado": {
        "bg": "#eff6ff",        # Azul muy suave
        "border": "#2563eb",    # Azul médico profesional
        "text": "#1e3a8a",
        "shadow": "0 2px 8px rgba(37, 99, 235, 0.15)",
        "hover_bg": "#dbeafe",
        "hover_shadow": "0 8px 25px rgba(37, 99, 235, 0.3)"
    },
    
    # Prótesis - Dorado elegante médico
    "corona": {
        "bg": "#fffbeb",        # Amarillo muy suave
        "border": "#d97706",    # Dorado médico
        "text": "#92400e",
        "shadow": "0 2px 8px rgba(217, 119, 6, 0.15)",
        "hover_bg": "#fef3c7",
        "hover_shadow": "0 8px 25px rgba(217, 119, 6, 0.3)",
        "metallic": True        # Efecto metálico sutil
    },
    
    # Implantes - Verde esmeralda médico
    "implante": {
        "bg": "#f0fdfa",
        "border": "#059669",
        "text": "#064e3b",
        "shadow": "0 2px 8px rgba(5, 150, 105, 0.15)",
        "hover_bg": "#ccfbf1",
        "hover_shadow": "0 8px 25px rgba(5, 150, 105, 0.3)"
    },
    
    # Endodoncia - Dorado especializado
    "endodoncia": {
        "bg": "#fffbeb",
        "border": "#f59e0b",
        "text": "#92400e",
        "shadow": "0 2px 8px rgba(245, 158, 11, 0.15)",
        "hover_bg": "#fef3c7",
        "hover_shadow": "0 8px 25px rgba(245, 158, 11, 0.3)"
    },
    
    # Ausente - Gris médico neutral
    "ausente": {
        "bg": "#f9fafb",
        "border": "#6b7280",
        "text": "#374151",
        "shadow": "0 2px 8px rgba(107, 114, 128, 0.15)",
        "hover_bg": "#f3f4f6",
        "hover_shadow": "0 8px 25px rgba(107, 114, 128, 0.2)",
        "opacity": 0.6         # Indicador visual de ausencia
    },
    
    # Fractura - Rojo intenso de urgencia
    "fractura": {
        "bg": "#fef2f2",
        "border": "#ef4444",
        "text": "#7f1d1d",
        "shadow": "0 2px 8px rgba(239, 68, 68, 0.2)",
        "hover_bg": "#fee2e2",
        "hover_shadow": "0 8px 25px rgba(239, 68, 68, 0.4)",
        "pulse": True,
        "urgent": True
    },
    
    # En tratamiento - Naranja profesional
    "en_tratamiento": {
        "bg": "#fff7ed",
        "border": "#ea580c",
        "text": "#9a3412",
        "shadow": "0 2px 8px rgba(234, 88, 12, 0.15)",
        "hover_bg": "#fed7aa",
        "hover_shadow": "0 8px 25px rgba(234, 88, 12, 0.3)",
        "animated": True        # Indicador de proceso activo
    }
}

# Mantener compatibilidad con código existente
CONDITION_COLORS = {
    condition: palette["border"] 
    for condition, palette in MEDICAL_CONDITION_PALETTE.items()
}

# Nombres legibles para mostrar en UI
CONDITION_NAMES = {
    "sano": "Sano",
    "caries": "Caries",
    "obturado": "Obturado",
    "corona": "Corona",
    "puente": "Puente",
    "implante": "Implante",
    "ausente": "Ausente",
    "fractura": "Fractura",
    "endodoncia": "Endodoncia",
    "extraccion": "Extracción",
    "protesis": "Prótesis",
    "sellantes": "Sellantes",
    "composite": "Composite",
    "amalgama": "Amalgama",
    "ceramica": "Cerámica",
    "metal": "Metal",
    "resina": "Resina",
    "temporal": "Temporal",
    "planificado": "Planificado",
    "en_tratamiento": "En Tratamiento",
    "completado": "Completado"
}

# Categorías para organizar condiciones
CONDITION_CATEGORIES = {
    "basicas": ["sano", "caries", "fractura"],
    "restaurativas": ["obturado", "composite", "amalgama", "resina"],
    "protesicas": ["corona", "puente", "protesis", "implante"],
    "preventivas": ["sellantes"],
    "quirurgicas": ["extraccion", "ausente"],
    "endodonticas": ["endodoncia"],
    "materiales": ["ceramica", "metal"],
    "estados": ["temporal", "planificado", "en_tratamiento", "completado"]
}

# ==========================================
# 🦷 ESTILOS PARA DIENTE Y SUPERFICIES
# ==========================================

# Dimensiones y estilo del diente
TOOTH_STYLE = {
    "width": "60px",
    "height": "60px",
    "border_radius": RADIUS["xl"],
    "position": "relative",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "font_size": "12px",
    "font_weight": "bold",
    "color": DARK_THEME["colors"]["text_primary"],
    "border": f"2px solid {DARK_THEME['colors']['primary']}",
    "background": DARK_THEME["colors"]["surface_secondary"]
}

# Estilo cuando el diente está seleccionado
TOOTH_SELECTED_STYLE = {
    **TOOTH_STYLE,
    "border": f"3px solid {COLORS['primary']['500']}",
    "box_shadow": f"0 0 20px {COLORS['primary']['500']}40",
    "transform": "scale(1.05)"
}

# Posicionamiento anatómico de las 5 superficies
SURFACE_POSITIONS = {
    "oclusal": {
        "position": "absolute",
        "top": "15%",
        "left": "25%",
        "width": "50%",
        "height": "25%",
        "border_radius": f"{RADIUS['md']} {RADIUS['md']} 0 0"
    },
    "mesial": {
        "position": "absolute",
        "left": "8%",
        "top": "25%",
        "width": "25%",
        "height": "50%",
        "border_radius": f"{RADIUS['md']} 0 0 {RADIUS['md']}"
    },
    "distal": {
        "position": "absolute",
        "right": "8%",
        "top": "25%",
        "width": "25%",
        "height": "50%",
        "border_radius": f"0 {RADIUS['md']} {RADIUS['md']} 0"
    },
    "vestibular": {
        "position": "absolute",
        "bottom": "25%",
        "left": "25%",
        "width": "50%",
        "height": "25%",
        "border_radius": f"0 0 {RADIUS['md']} {RADIUS['md']}"
    },
    "lingual": {
        "position": "absolute",
        "bottom": "8%",
        "left": "25%",
        "width": "50%",
        "height": "20%",
        "border_radius": f"0 0 {RADIUS['lg']} {RADIUS['lg']}"
    }
}

# ==========================================
# 🧩 COMPONENTE: SUPERFICIE INDIVIDUAL
# ==========================================

def tooth_surface(
    tooth_number: int, 
    surface_name: str, 
    condition: str = "sano",
    is_selected: bool = False,
    is_modified: bool = False
) -> rx.Component:
    """
    🦷 Renderiza una superficie individual del diente
    
    Args:
        tooth_number: Número FDI del diente (11-48)
        surface_name: Nombre de la superficie (oclusal, mesial, distal, vestibular, lingual)
        condition: Condición actual de la superficie
        is_selected: Si esta superficie está seleccionada
        is_modified: Si esta superficie tiene cambios pendientes
    """
    
    # Color base según condición
    base_color = CONDITION_COLORS.get(condition, CONDITION_COLORS["sano"])
    
    # Estilos base
    base_style = {
        **SURFACE_POSITIONS[surface_name],
        "background": base_color,
        "cursor": "pointer",
        "transition": "all 0.2s ease",
        "opacity": "0.8",
        "_hover": {
            "opacity": "1.0",
            "transform": "scale(1.1)",
            "z_index": "10",
            "box_shadow": f"0 4px 12px {base_color}60"
        }
    }
    
    # Estilos condicionales usando rx.cond
    surface_style = rx.cond(
        is_selected,
        {
            **base_style,
            "border": f"2px solid {COLORS['primary']['400']}",
            "box_shadow": f"0 0 8px {COLORS['primary']['400']}80",
            "z_index": "5"
        },
        rx.cond(
            is_modified,
            {
                **base_style,
                "border": f"2px solid {COLORS['warning']['300']}",
                "box_shadow": f"0 0 8px {COLORS['warning']['300']}60",
                "animation": "pulse 2s infinite"
            },
            {
                **base_style,
                "border": f"1px solid {DARK_THEME['colors']['primary']}"
            }
        )
    )
    
    return rx.tooltip(
        rx.box(
            style=surface_style,
            on_click=lambda: AppState.seleccionar_diente_superficie(tooth_number, surface_name)
        ),
        content=f"{surface_name.title()}: {CONDITION_NAMES.get(condition, condition)}"
    )

# ==========================================
# ⚡ SUPERFICIE OPTIMIZADA - SIN RX.COND ANIDADOS
# ==========================================

def tooth_surface_optimized(tooth_number: int, surface_name: str) -> rx.Component:
    """
    ⚡ Superficie individual optimizada - Elimina rx.cond anidados complejos
    
    Args:
        tooth_number: Número FDI del diente
        surface_name: Nombre de la superficie
    """
    
    # Obtener posición anatómica
    surface_style = SURFACE_POSITIONS.get(surface_name, {})
    
    return rx.tooltip(
        rx.box(
            style={
                **surface_style,
                "background": rx.color_mode_cond(
                    # Usar la computed var optimizada para obtener el color
                    rx.match(
                        AppState.dientes_estados[tooth_number].get(surface_name, "sano"),
                        *[(cond, color) for cond, color in CONDITION_COLORS.items()],
                        CONDITION_COLORS["sano"]  # Valor por defecto
                    )
                ),
                "border": rx.cond(
                    AppState.diente_seleccionado == tooth_number,
                    f"2px solid {COLORS['primary']['500']}",
                    rx.cond(
                        AppState.diente_tiene_cambios(tooth_number),
                        f"2px solid {COLORS['warning']['500']}",
                        f"1px solid {DARK_THEME['colors']['border']}"
                    )
                ),
                "cursor": "pointer",
                "transition": "all 0.2s ease",
                "opacity": rx.cond(
                    (AppState.diente_seleccionado == tooth_number) | 
                    AppState.diente_tiene_cambios(tooth_number),
                    "1.0",
                    "0.8"
                ),
                "z_index": rx.cond(
                    AppState.diente_seleccionado == tooth_number,
                    "3",
                    "2"
                ),
                "box_shadow": rx.cond(
                    AppState.diente_tiene_cambios(tooth_number),
                    f"0 0 8px {COLORS['warning']['500']}40",
                    "none"
                )
            },
            # Event handler optimizado - usar el método optimizado del estado
            on_click=AppState.seleccionar_diente(tooth_number),
            
            # Hover effects mejorados
            _hover={
                "opacity": "1.0",
                "transform": "scale(1.1)",
                "z_index": "4"
            }
        ),
        content=f"{surface_name.title()}: {AppState.dientes_estados[tooth_number].get(surface_name, 'sano')}"
    )

# ==========================================
# 🦷 COMPONENTE: DIENTE COMPLETO INTERACTIVO
# ==========================================

def interactive_tooth(
    tooth_number: int,
    conditions: Optional[Dict[str, str]] = None,
    is_selected: bool = False,
    pending_changes: Optional[Dict[str, str]] = None
) -> rx.Component:
    """
    🦷 Componente principal del diente interactivo con 5 superficies
    
    Args:
        tooth_number: Número FDI del diente (11-48)
        conditions: Diccionario con condiciones por superficie
        is_selected: Si este diente está seleccionado actualmente
        pending_changes: Cambios pendientes sin guardar
    """
    
    # Condiciones por defecto si no se proporcionan
    if conditions is None:
        conditions = {
            "oclusal": "sano",
            "mesial": "sano", 
            "distal": "sano",
            "vestibular": "sano",
            "lingual": "sano"
        }
    
    # Cambios pendientes si existen (usando rx.cond para evitar error de Reflex)
    pending = rx.cond(pending_changes, pending_changes, {})
    
    # Determinar si el diente tiene modificaciones
    has_modifications = rx.cond(pending_changes, True, False)
    
    # Estilo del contenedor principal
    container_style = rx.cond(is_selected, TOOTH_SELECTED_STYLE, TOOTH_STYLE)
    
    return rx.box(
        # Número del diente (centrado)
        rx.text(
            str(tooth_number),
            style={
                "position": "absolute",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "z_index": "1",
                "font_size": "11px",
                "font_weight": "bold",
                "color": DARK_THEME["colors"]["text_primary"],
                "text_shadow": "1px 1px 2px rgba(0,0,0,0.8)",
                "pointer_events": "none"
            }
        ),
        
        # 5 superficies del diente - VERSIÓN OPTIMIZADA
        *[
            tooth_surface_optimized(tooth_number, surface)
            for surface in ["oclusal", "mesial", "distal", "vestibular", "lingual"]
        ],
        
        # Indicador de modificaciones (pequeño punto naranja)
        rx.cond(
            has_modifications,
            rx.box(
                style={
                    "position": "absolute",
                    "top": "5px",
                    "right": "5px",
                    "width": "8px",
                    "height": "8px",
                    "background": COLORS["warning"]["500"],
                    "border_radius": "50%",
                    "z_index": "20",
                    "box_shadow": f"0 0 4px {COLORS['warning']['500']}80",
                    "animation": "pulse 1.5s infinite"
                }
            )
        ),
        
        style=container_style,
        on_click=lambda: AppState.abrir_popover_diente(tooth_number, 200, 200)  # Posición fija por ahora
    )

# ==========================================
# 🦷 DIENTE MEJORADO CON MICRO-INTERACCIONES
# ==========================================

def enhanced_tooth_component(
    tooth_number: int, 
    estado: str = "sano",
    conditions: Optional[Dict[str, str]] = None,
    is_selected: bool = False
) -> rx.Component:
    """🦷 Diente con micro-interacciones médicas profesionales mejoradas"""
    
    # Obtener configuración de color médico
    condition_config = MEDICAL_CONDITION_PALETTE.get(estado, MEDICAL_CONDITION_PALETTE["sano"])
    
    # Obtener dimensiones del diente según su tipo
    tooth_dimensions = get_tooth_dimensions(tooth_number)
    
    # Configurar animaciones específicas
    animation_css = ""
    if condition_config.get("pulse"):
        animation_css = "pulse-urgent 2s cubic-bezier(0.4, 0, 0.6, 1) infinite"
    elif condition_config.get("animated"):
        animation_css = "medical-attention 3s ease-in-out infinite"
    elif is_selected:
        animation_css = "tooth-selected 1.5s ease-in-out infinite"
    
    return rx.tooltip(
        rx.box(
            # Número del diente con tipografía médica mejorada
            rx.text(
                str(tooth_number),
                style={
                    "font_size": "11px",
                    "font_weight": "700",
                    "color": condition_config["text"],
                    "font_family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
                    "text_align": "center",
                    "line_height": "1",
                    "user_select": "none",
                    "pointer_events": "none"
                }
            ),
            
            # Indicador visual de estado con glassmorphism
            rx.cond(
                estado != "sano",
                rx.box(
                    style={
                        "width": "8px",
                        "height": "8px", 
                        "border_radius": "50%",
                        "background": f"linear-gradient(135deg, {condition_config['border']}, {condition_config['hover_bg']})",
                        "position": "absolute",
                        "top": "2px",
                        "right": "2px",
                        "box_shadow": f"0 2px 6px {condition_config['border']}40",
                        "border": "1px solid rgba(255,255,255,0.2)",
                        "backdrop_filter": "blur(4px)"
                    }
                )
            ),
            
            # Badge de urgencia para casos críticos
            rx.cond(
                condition_config.get("urgent", False),
                rx.box(
                    "!",
                    style={
                        "position": "absolute",
                        "top": "-2px",
                        "left": "-2px",
                        "width": "12px",
                        "height": "12px",
                        "border_radius": "50%",
                        "background": "linear-gradient(135deg, #ef4444, #dc2626)",
                        "color": "white",
                        "font_size": "8px",
                        "font_weight": "bold",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "animation": "pulse-urgent 1.5s infinite",
                        "z_index": "10"
                    }
                )
            ),
            
            style={
                # Dimensiones dinámicas
                **tooth_dimensions,
                
                # Estilos médicos profesionales
                "background": f"linear-gradient(135deg, {condition_config['bg']}, {condition_config['hover_bg']}08)",
                "border": f"2px solid {condition_config['border']}",
                "border_radius": "14px",
                "position": "relative",
                "cursor": "pointer",
                "user_select": "none",
                
                # Sistema de sombras médicas
                "box_shadow": condition_config["shadow"],
                
                # Transiciones suaves premium
                "transition": "all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
                
                # Animaciones contextuales
                **({"animation": animation_css} if animation_css else {}),
                
                # Opacidad para dientes ausentes
                "opacity": condition_config.get("opacity", 1),
                
                # Estados interactivos médicos avanzados
                "_hover": {
                    "transform": "translateY(-3px) scale(1.08)",
                    "box_shadow": condition_config["hover_shadow"],
                    "border_color": condition_config["border"],
                    "background": f"linear-gradient(135deg, {condition_config['hover_bg']}, {condition_config['border']}15)",
                    "z_index": "20"
                },
                
                "_active": {
                    "transform": "translateY(-1px) scale(1.02)",
                    "transition": "all 0.15s ease",
                    "box_shadow": f"0 4px 12px {condition_config['border']}50"
                },
                
                # Estado seleccionado
                **({"border_color": COLORS["primary"]["400"],
                    "box_shadow": f"0 0 0 2px {COLORS['primary']['400']}40, {condition_config['shadow']}",
                    "background": f"linear-gradient(135deg, {condition_config['bg']}, {COLORS['primary']['100']})"
                } if is_selected else {}),
                
                # Efectos especiales
                **({"backdrop_filter": "blur(8px)"} if condition_config.get("metallic") else {})
            },
            
            # Eventos interactivos mejorados
            on_click=lambda: [
                AppState.seleccionar_diente_con_feedback(tooth_number),
                AppState.abrir_popover_diente(tooth_number, 200, 200)
            ],
            on_mouse_enter=lambda: AppState.highlight_tooth(tooth_number, True),
            on_mouse_leave=lambda: AppState.highlight_tooth(tooth_number, False)
        ),
        
        # Tooltip médico informativo
        content=rx.vstack(
            rx.hstack(
                rx.text(f"🦷 Diente {tooth_number}", weight="bold", size="3"),
                rx.badge(
                    get_condition_name(estado),
                    style={
                        "background": condition_config["border"],
                        "color": "white"
                    }
                ),
                spacing="2"
            ),
            rx.text(
                get_tooth_type_name(tooth_number), 
                size="2", 
                color=DARK_THEME["colors"]["text_secondary"]
            ),
            rx.text(
                "Click para detalles médicos", 
                size="1", 
                color=DARK_THEME["colors"]["text_muted"]
            ),
            spacing="1",
            align_items="start"
        ),
        
        # Configuración del tooltip
        side="top",
        delay_duration=500
    )

def get_tooth_dimensions(tooth_number: int) -> Dict[str, str]:
    """🦷 Obtener dimensiones específicas según el tipo de diente"""
    if tooth_number in [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]:  # Anteriores
        return {"width": "24px", "height": "32px"}
    elif tooth_number in [14, 15, 24, 25, 34, 35, 44, 45]:  # Premolares
        return {"width": "26px", "height": "28px"}
    else:  # Molares
        return {"width": "30px", "height": "26px"}

def get_tooth_type_name(tooth_number: int) -> str:
    """🦷 Obtener nombre del tipo de diente"""
    if tooth_number in [11, 12, 21, 22, 31, 32, 41, 42]:
        return "Incisivo"
    elif tooth_number in [13, 23, 33, 43]:
        return "Canino"
    elif tooth_number in [14, 15, 24, 25, 34, 35, 44, 45]:
        return "Premolar"
    else:
        return "Molar"

# ==========================================
# 🎨 UTILIDADES DE ESTILO Y COLORES
# ==========================================

def get_condition_color(condition: str) -> str:
    """Obtener color hexadecimal para una condición específica"""
    return CONDITION_COLORS.get(condition, CONDITION_COLORS["sano"])

def get_condition_name(condition: str) -> str:
    """Obtener nombre legible para una condición"""
    return CONDITION_NAMES.get(condition, condition.title())

def get_conditions_by_category(category: str) -> list:
    """Obtener lista de condiciones por categoría"""
    return CONDITION_CATEGORIES.get(category, [])

def is_condition_valid_for_surface(condition: str, surface: str, tooth_type: str = "molar") -> bool:
    """
    Validar si una condición es válida para una superficie específica
    
    Args:
        condition: Condición a validar
        surface: Superficie del diente
        tooth_type: Tipo de diente (incisivo, canino, premolar, molar)
    
    Returns:
        True si la condición es válida para la superficie
    """
    
    # Validaciones básicas
    if condition == "ausente":
        # Si el diente está ausente, no puede tener otras condiciones
        return surface == "oclusal"  # Solo marcar en oclusal para simplificar
    
    if surface == "oclusal" and tooth_type in ["incisivo", "canino"]:
        # Incisivos y caninos usan superficie "incisal" en lugar de "oclusal"
        return condition not in ["sellantes"]  # Sellantes principalmente en molares
    
    # Implantes requieren al menos superficie oclusal
    if condition == "implante":
        return True  # Implantes pueden ir en cualquier superficie
        
    # Por defecto, todas las condiciones son válidas
    return True

# ==========================================
# 📊 INFORMACIÓN DE DIENTE SELECCIONADO
# ==========================================

def selected_tooth_info_panel() -> rx.Component:
    """Panel informativo del diente seleccionado"""
    return rx.cond(
        AppState.diente_seleccionado,
        rx.box(
            rx.vstack(
                rx.text(
                    f"Diente: {AppState.diente_seleccionado}",
                    size="4",
                    weight="bold",
                    color=COLORS["primary"]["500"]
                ),
                rx.cond(
                    AppState.superficie_seleccionada,
                    rx.text(
                        f"Superficie: {AppState.superficie_seleccionada}",
                        size="3",
                        color=DARK_THEME["colors"]["text_secondary"]
                    )
                ),
                rx.text(
                    "Click en una superficie para cambiar condición",
                    size="2",
                    color=DARK_THEME["colors"]["text_muted"]
                ),
                spacing="2",
                align_items="start"
            ),
            style={
                "background": DARK_THEME["colors"]["surface_secondary"],
                "border": f"1px solid {DARK_THEME['colors']['primary']}",
                "border_radius": RADIUS["lg"],
                "padding": SPACING["4"],
                "min_width": "200px"
            }
        )
    )

# ==========================================
# 🔧 FUNCIONES AUXILIARES DE VALIDACIÓN
# ==========================================

def validate_tooth_number(tooth_number: int) -> bool:
    """Validar que el número de diente sea válido según FDI"""
    valid_adult_teeth = [
        # Cuadrante 1 (Superior Derecho)
        18, 17, 16, 15, 14, 13, 12, 11,
        # Cuadrante 2 (Superior Izquierdo) 
        21, 22, 23, 24, 25, 26, 27, 28,
        # Cuadrante 3 (Inferior Izquierdo)
        31, 32, 33, 34, 35, 36, 37, 38,
        # Cuadrante 4 (Inferior Derecho)
        41, 42, 43, 44, 45, 46, 47, 48
    ]
    return tooth_number in valid_adult_teeth

def get_tooth_type(tooth_number: int) -> str:
    """Determinar el tipo de diente basado en el número FDI"""
    if not validate_tooth_number(tooth_number):
        return "unknown"
    
    # Obtener el último dígito para determinar el tipo
    last_digit = tooth_number % 10
    
    if last_digit in [1, 2]:
        return "incisivo"
    elif last_digit == 3:
        return "canino"
    elif last_digit in [4, 5]:
        return "premolar"
    elif last_digit in [6, 7, 8]:
        return "molar"
    else:
        return "unknown"

def get_tooth_quadrant(tooth_number: int) -> int:
    """Obtener el cuadrante FDI del diente"""
    if not validate_tooth_number(tooth_number):
        return 0
    
    return tooth_number // 10


# ==========================================
# 🦷 COMPONENTE AVANZADO CON CATÁLOGO FDI
# ==========================================

def advanced_fdi_tooth_component(
    diente_fdi: DienteModel,
    condicion: Optional[CondicionDienteModel] = None,
    is_selected: bool = False,
    is_urgent: bool = False
) -> rx.Component:
    """
    🦷 Componente avanzado usando catálogo FDI real
    
    Características:
    - Usa datos reales del catálogo FDI
    - Colores médicos profesionales desde BD
    - Dimensiones anatómicas correctas
    - Tooltips con información médica
    - Animaciones contextuales para urgencias
    """
    
    # Obtener información de la condición
    if condicion:
        condition_name = condicion.nombre_condicion or "sano"
        condition_color = condicion.color_condicion or "#16a34a"
        is_urgent = condicion.es_urgente
        categoria = condicion.categoria or "normal"
    else:
        condition_name = "sano"
        condition_color = "#16a34a"
        is_urgent = False
        categoria = "normal"
    
    # Obtener dimensiones anatómicas reales
    tooth_dimensions = {
        "width": "30px",
        "height": "28px"
    }
    
    # Coordenadas SVG del catálogo
    svg_pos = diente_fdi.posicion_svg
    
    # Configurar animación según urgencia y condición
    animation_style = {}
    if is_urgent:
        animation_style = {"animation": "pulse-urgent 2s infinite"}
    elif is_selected:
        animation_style = {"animation": "tooth-selected 1.5s ease-in-out infinite"}
    
    return rx.tooltip(
        rx.box(
            # Número FDI del diente
            rx.text(
                str(diente_fdi.numero_fdi),
                style={
                    "font_size": "11px",
                    "font_weight": "700",
                    "color": "#1f2937",
                    "font_family": "Inter, system-ui, sans-serif",
                    "text_align": "center",
                    "line_height": "1",
                    "user_select": "none"
                }
            ),
            
            # Indicador de condición (punto de color)
            rx.cond(
                condition_name != "sano",
                rx.box(
                    style={
                        "position": "absolute",
                        "top": "2px",
                        "right": "2px",
                        "width": "8px",
                        "height": "8px",
                        "border_radius": "50%",
                        "background": condition_color,
                        "box_shadow": f"0 2px 6px {condition_color}40",
                        "border": "1px solid rgba(255,255,255,0.3)"
                    }
                )
            ),
            
            # Badge de urgencia
            rx.cond(
                is_urgent,
                rx.box(
                    "!",
                    style={
                        "position": "absolute",
                        "top": "-2px",
                        "left": "-2px",
                        "width": "12px",
                        "height": "12px",
                        "border_radius": "50%",
                        "background": "linear-gradient(135deg, #ef4444, #dc2626)",
                        "color": "white",
                        "font_size": "8px",
                        "font_weight": "bold",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "z_index": "10"
                    }
                )
            ),
            
            style={
                # Dimensiones anatómicas
                **tooth_dimensions,
                
                # Posición según catálogo FDI
                "position": "relative",
                
                # Estilo médico profesional
                "background": f"linear-gradient(135deg, {condition_color}15, {condition_color}08)",
                "border": f"2px solid {condition_color}",
                "border_radius": "12px",
                "cursor": "pointer",
                "user_select": "none",
                
                # Sombras médicas
                "box_shadow": f"0 2px 8px {condition_color}20",
                
                # Transiciones suaves
                "transition": "all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
                
                # Animaciones contextuales
                **animation_style,
                
                # Estados interactivos
                "_hover": {
                    "transform": "translateY(-2px) scale(1.05)",
                    "box_shadow": f"0 6px 20px {condition_color}30",
                    "background": f"linear-gradient(135deg, {condition_color}25, {condition_color}15)",
                    "z_index": "20"
                },
                
                "_active": {
                    "transform": "translateY(-1px) scale(1.02)",
                    "transition": "all 0.15s ease"
                },
                
                # Estado seleccionado
                **({"border_color": COLORS["primary"]["400"],
                    "box_shadow": f"0 0 0 2px {COLORS['primary']['400']}40, 0 4px 12px {condition_color}30"
                } if is_selected else {})
            },
            
            # Eventos de interacción
            on_click=lambda: [
                AppState.seleccionar_diente_fdi(diente_fdi.numero_fdi),
                AppState.cargar_detalles_diente_fdi(diente_fdi.numero_fdi)
            ]
        ),
        
        # Tooltip informativo médico
        content=rx.vstack(
            # Header del tooltip
            rx.hstack(
                rx.text(f"🦷 {diente_fdi.nombre_completo}", weight="bold", size="3"),
                rx.badge(
                    condition_name.title(),
                    style={
                        "background": condition_color,
                        "color": "white"
                    }
                ),
                spacing="2"
            ),
            
            # Información anatómica
            rx.text(
                f"Tipo: {diente_fdi.tipo_diente.title()}", 
                size="2", 
                color=DARK_THEME["colors"]["text_secondary"]
            ),
            rx.text(
                f"Cuadrante: {diente_fdi.cuadrante}", 
                size="2", 
                color=DARK_THEME["colors"]["text_secondary"]
            ),
            
            # Superficies disponibles
            rx.cond(
                len(diente_fdi.superficies_disponibles) > 0,
                rx.text(
                    f"Superficies: {', '.join(diente_fdi.superficies_disponibles)}", 
                    size="1", 
                    color=DARK_THEME["colors"]["text_muted"]
                )
            ),
            
            # Indicador de urgencia
            rx.cond(
                is_urgent,
                rx.hstack(
                    rx.text("🚨", size="2"),
                    rx.text("Requiere atención urgente", size="2", color="#ef4444", weight="bold"),
                    spacing="1"
                )
            ),
            
            # Call to action
            rx.text(
                "Click para ver detalles médicos", 
                size="1", 
                color=DARK_THEME["colors"]["text_muted"]
            ),
            
            spacing="1",
            align_items="start"
        ),
        
        side="top",
        delay_duration=300
    )


# ==========================================
# 🔄 FUNCIONES DE INTEGRACIÓN CON SERVICIO
# ==========================================

async def cargar_diente_fdi_con_condicion(numero_fdi: int, numero_historia: str) -> rx.Component:
    """🔄 Cargar diente FDI con su condición actual desde BD"""
    
    try:
        # Cargar información del diente desde catálogo FDI
        diente = await odontograma_service.obtener_diente_por_fdi(numero_fdi)
        if not diente:
            # Fallback: crear diente básico
            diente = DienteModel(
                numero_fdi=numero_fdi,
                nombre_diente=f"Diente {numero_fdi}",
                tipo_diente=get_tooth_type(numero_fdi)
            )
        
        # Obtener odontograma actual del paciente
        odontograma = await odontograma_service.obtener_odontograma_actual(numero_historia)
        condicion = None
        
        if odontograma and odontograma.dientes_estados:
            estado_diente = odontograma.dientes_estados.get(numero_fdi, {})
            if estado_diente:
                # Crear modelo de condición desde estado
                condicion = CondicionDienteModel(
                    numero_fdi=numero_fdi,
                    codigo_condicion=estado_diente.get("codigo", "SAO"),
                    nombre_condicion=estado_diente.get("condicion", "sano"),
                    color_hex=estado_diente.get("color", "#16a34a"),
                    superficie_afectada=estado_diente.get("superficie", "completa"),
                    categoria=estado_diente.get("categoria", "normal"),
                    es_urgente=estado_diente.get("es_urgente", False)
                )
        
        # Renderizar componente avanzado
        return advanced_fdi_tooth_component(
            diente_fdi=diente,
            condicion=condicion,
            is_selected=False  # AppState.diente_seleccionado == numero_fdi
        )
        
    except Exception as e:
        print(f"❌ Error cargando diente FDI {numero_fdi}: {e}")
        # Fallback: componente básico
        return enhanced_tooth_component(
            tooth_number=numero_fdi,
            estado="sano"
        )