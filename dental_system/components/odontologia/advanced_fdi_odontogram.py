"""
🦷 ODONTOGRAMA FDI AVANZADO CON DATOS REALES
============================================

Componente completo que integra:
- Catálogo FDI real de 32 dientes desde BD
- Servicio avanzado con versionado
- Interactividad por diente con condiciones
- Colores médicos profesionales

NOTA: El estado se encuentra en estado_odontograma_avanzado.py
      y se accede vía AppState (patrón mixin)
"""

import reflex as rx
from typing import Dict, List, Optional, Any

from dental_system.styles.themes import COLORS, DARK_THEME

# ==========================================
# 🦷 COMPONENTE DE DIENTE AVANZADO
# ==========================================

def advanced_fdi_tooth(
    numero_fdi: int,
    diente_info: Dict[str, Any],
    estado: Dict[str, Any],
    is_selected: bool = False
) -> rx.Component:
    """🦷 Componente de diente con datos FDI reales"""
    
    color_fondo = estado.get("color", "#16a34a")
    es_urgente = estado.get("codigo") in ["CAR", "FRAC", "MOV"]
    
    return rx.box(
        rx.vstack(
            # Número FDI
            rx.heading(
                str(numero_fdi),
                size="4",
                color="white",
                font_weight="bold"
            ),
            # Tipo de diente
            rx.text(
                diente_info.get("tipo_diente", "").capitalize(),
                font_size="xs",
                color="white",
                opacity="0.9"
            ),
            # Código de condición
            rx.badge(
                estado.get("codigo", "SAO"),
                color_scheme="gray",
                size="1"
            ),
            spacing="1",
            align="center",
            justify="center"
        ),
        
        # Estilos del diente
        width="60px",
        height="60px",
        background=color_fondo,
        border_radius="8px",
        border=f"2px solid {'#fff' if is_selected else 'transparent'}",
        cursor="pointer",
        position="relative",
        
        # Efectos hover y selección
        _hover={
            "transform": "scale(1.1)",
            "box_shadow": f"0 4px 12px {color_fondo}50",
            "z_index": "10"
        },
        
        # Animación para urgentes
        animation=rx.cond(
            es_urgente,
            "pulse 2s infinite",
            "none"
        ),
        
        # Evento de click
        on_click=AppState.seleccionar_diente(numero_fdi),
        
        transition="all 0.3s ease"
    )

# ==========================================
# 🏗️ GRID DEL ODONTOGRAMA FDI
# ==========================================

def advanced_fdi_grid() -> rx.Component:
    """🏗️ Grid completo del odontograma FDI - versión simplificada temporal"""
    
    return rx.vstack(
        # Cuadrante 2 (Superior Izquierdo: 21-28) + Cuadrante 1 (Superior Derecho: 11-18)
        rx.hstack(
            rx.foreach(
                [28, 27, 26, 25, 24, 23, 22, 21],
                lambda fdi: advanced_fdi_tooth_simple(fdi)
            ),
            rx.foreach(
                [11, 12, 13, 14, 15, 16, 17, 18],
                lambda fdi: advanced_fdi_tooth_simple(fdi)
            ),
            spacing="2",
            justify="center"
        ),
        
        # Separador central
        rx.divider(size="4", color_scheme="gray"),
        
        # Cuadrante 3 (Inferior Izquierdo: 31-38) + Cuadrante 4 (Inferior Derecho: 41-48)
        rx.hstack(
            rx.foreach(
                [38, 37, 36, 35, 34, 33, 32, 31],
                lambda fdi: advanced_fdi_tooth_simple(fdi)
            ),
            rx.foreach(
                [41, 42, 43, 44, 45, 46, 47, 48],
                lambda fdi: advanced_fdi_tooth_simple(fdi)
            ),
            spacing="2",
            justify="center"
        ),
        
        spacing="4",
        align="center",
        width="100%"
    )

def advanced_fdi_tooth_simple_with_state(numero_fdi: int, app_state) -> rx.Component:
    """🦷 Diente FDI con estado dinámico desde AppState pasado como parámetro"""
    
    return rx.box(
        rx.vstack(
            # Número FDI
            rx.heading(
                numero_fdi,
                size="4",
                color="white",
                font_weight="bold"
            ),
            # Tipo de diente usando rx.cond
            rx.cond(
                (numero_fdi == 16) | (numero_fdi == 17) | (numero_fdi == 26) | (numero_fdi == 27) | 
                (numero_fdi == 36) | (numero_fdi == 37) | (numero_fdi == 46) | (numero_fdi == 47),
                rx.text("Molar", font_size="xs", color="white", opacity="0.9"),
                rx.text("Diente", font_size="xs", color="white", opacity="0.9")
            ),
            # Código de condición dinámico desde el estado
            rx.badge(
                app_state.dientes_estados[numero_fdi]["codigo"].to(str),
                color_scheme=rx.cond(
                    app_state.dientes_estados[numero_fdi]["codigo"] == "SAO",
                    "green",
                    rx.cond(
                        app_state.dientes_estados[numero_fdi]["codigo"] == "CAR",
                        "red",
                        rx.cond(
                            app_state.dientes_estados[numero_fdi]["codigo"] == "OBT",
                            "blue",
                            rx.cond(
                                app_state.dientes_estados[numero_fdi]["codigo"] == "COR",
                                "orange",
                                rx.cond(
                                    app_state.dientes_estados[numero_fdi]["codigo"] == "ENDO",
                                    "pink",
                                    rx.cond(
                                        app_state.dientes_estados[numero_fdi]["codigo"] == "EXT",
                                        "brown",
                                        rx.cond(
                                            app_state.dientes_estados[numero_fdi]["codigo"] == "AUS",
                                            "gray",
                                            "yellow"
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                size="1"
            ),
            spacing="1",
            align="center",
            justify="center"
        ),
        
        # Estilos del diente con color dinámico
        width="60px",
        height="60px",
        background=app_state.dientes_estados[numero_fdi]["color"].to(str),
        border_radius="8px",
        border=rx.cond(
            app_state.diente_seleccionado == numero_fdi,
            "3px solid #E6B012",  # Borde dorado para diente seleccionado
            "2px solid transparent"
        ),
        cursor="pointer",
        position="relative",
        
        # Efectos hover dinámicos
        _hover={
            "transform": "scale(1.1)",
            "box_shadow": f"0 4px 12px rgba(22, 163, 74, 0.5)",
            "z_index": "10"
        },
        
        # Evento de click
        on_click=app_state.seleccionar_diente(numero_fdi),
        
        transition="all 0.3s ease"
    )

def advanced_fdi_tooth_simple(numero_fdi: int) -> rx.Component:
    """🦷 Versión simplificada temporal"""
    
    return rx.box(
        rx.vstack(
            # Número FDI
            rx.heading(
                numero_fdi,
                size="4",
                color="white",
                font_weight="bold"
            ),
            # Tipo de diente usando rx.cond
            rx.cond(
                (numero_fdi == 16) | (numero_fdi == 17) | (numero_fdi == 26) | (numero_fdi == 27) | 
                (numero_fdi == 36) | (numero_fdi == 37) | (numero_fdi == 46) | (numero_fdi == 47),
                rx.text("Molar", font_size="xs", color="white", opacity="0.9"),
                rx.text("Diente", font_size="xs", color="white", opacity="0.9")
            ),
            # Badge estático por ahora
            rx.badge(
                "SAO",
                color_scheme="green",
                size="1"
            ),
            spacing="1",
            align="center",
            justify="center"
        ),
        
        # Estilos del diente estáticos por ahora
        width="60px",
        height="60px",
        background="#16a34a",  # Verde por defecto
        border_radius="8px",
        border="2px solid transparent",
        cursor="pointer",
        position="relative",
        
        # Efectos hover dinámicos
        _hover={
            "transform": "scale(1.1)",
            "box_shadow": f"0 4px 12px rgba(22, 163, 74, 0.5)",
            "z_index": "10"
        },
        
        transition="all 0.3s ease"
    )

# ==========================================
# 🎨 PANEL DE CONDICIONES
# ==========================================

def conditions_panel() -> rx.Component:
    """🎨 Panel para aplicar condiciones - versión simplificada"""
    
    return rx.card(
        rx.text(
            "🦷 Panel de condiciones disponible (funcionalidad completa pendiente)",
            text_align="center",
            color=DARK_THEME["colors"]["text_secondary"]
        ),
        width="100%"
    )

# ==========================================
# 📊 ESTADÍSTICAS DEL ODONTOGRAMA
# ==========================================

def odontogram_stats() -> rx.Component:
    """📊 Estadísticas en tiempo real - versión simplificada"""
    
    return rx.hstack(
        rx.card(
            rx.vstack(
                rx.heading("32", size="4", color="#16a34a"),
                rx.text("Sanos", font_size="sm"),
                spacing="1",
                align="center"
            ),
            padding="3"
        ),
        rx.card(
            rx.vstack(
                rx.heading("0", size="4", color="#dc2626"),
                rx.text("Patología", font_size="sm"),
                spacing="1",
                align="center"
            ),
            padding="3"
        ),
        rx.card(
            rx.vstack(
                rx.heading("0", size="4", color="#2563eb"),
                rx.text("Tratados", font_size="sm"),
                spacing="1",
                align="center"
            ),
            padding="3"
        ),
        spacing="3",
        justify="center",
        width="100%"
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL
# ==========================================

def advanced_fdi_odontogram() -> rx.Component:
    """🦷 Odontograma FDI avanzado completo - versión simplificada"""
    
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("🦷 Odontograma FDI Profesional", size="5", color=COLORS["primary"]),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("database"),
                    rx.text("Funcionalidad Completa Pendiente"),
                    spacing="2"
                ),
                variant="outline",
                color_scheme="blue",
                disabled=True
            ),
            justify="between",
            align="center",
            width="100%"
        ),
        
        # Estadísticas estáticas por ahora
        odontogram_stats(),
        
        # Grid del odontograma
        advanced_fdi_grid(),
        
        # Panel de condiciones
        conditions_panel(),
        
        spacing="6",
        width="100%",
        align="center"
    )