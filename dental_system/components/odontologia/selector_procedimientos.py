"""
📝 SELECTOR DE PROCEDIMIENTOS - MEJORADO
=========================================

Selector de procedimientos con autocompletado y búsqueda inteligente.
Reemplaza la lista estática con funcionalidad moderna.

CARACTERÍSTICAS:
- Búsqueda en tiempo real
- Autocompletado inteligente
- Filtros por categoría
- Selección múltiple
- Integración con AppState
"""

import reflex as rx
from typing import Dict, List, Optional
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🔍 COMPONENTE DE BÚSQUEDA
# ==========================================

def campo_busqueda_procedimientos() -> rx.Component:
    """🔍 Campo de búsqueda con filtros inteligentes"""
    return rx.box(
        rx.vstack(
            # Campo de búsqueda principal
            rx.hstack(
                rx.icon("search", size=18, color="gray.500"),
                rx.input(
                    placeholder="Buscar procedimiento (ej: obturación, limpieza, endodoncia...)",
                    value=AppState.estado_odontologia.filtro_procedimientos,
                    on_change=AppState.estado_odontologia.set_filtro_procedimientos,
                    size="3",
                    width="100%",
                    variant="soft"
                ),
                rx.cond(
                    AppState.estado_odontologia.filtro_procedimientos != "",
                    rx.button(
                        rx.icon("x", size=16),
                        variant="ghost",
                        size="2",
                        on_click=AppState.estado_odontologia.limpiar_filtro_procedimientos
                    ),
                    rx.fragment()
                ),
                width="100%",
                align_items="center",
                spacing="2"
            ),
            
            # Filtros por categoría
            rx.hstack(
                rx.text("Categorías:", size="2", weight="medium", color="gray.700"),
                rx.select(
                    ["Todas", "Preventiva", "Restaurativa", "Estética", "Cirugía", "Endodoncia", "Ortodoncia"],
                    placeholder="Filtrar por categoría",
                    value=AppState.estado_odontologia.categoria_filtro_procedimientos,
                    on_change=AppState.estado_odontologia.set_categoria_filtro_procedimientos,
                    size="2"
                ),
                spacing="3",
                align_items="center"
            ),
            
            spacing="3",
            width="100%"
        ),
        padding="4",
        background="white",
        border_radius="lg",
        border="1px solid gray.200"
    )

# ==========================================
# 📋 LISTA DE RESULTADOS
# ==========================================

def item_procedimiento(servicio) -> rx.Component:
    """📋 Item individual de procedimiento con información completa"""
    return rx.box(
        rx.hstack(
            # Checkbox de selección
            rx.checkbox(
                checked=servicio.get("seleccionado", False),
                on_change=lambda checked: AppState.estado_odontologia.toggle_servicio_seleccionado(
                    servicio["codigo"], checked
                ),
                size="3"
            ),
            
            # Información del servicio
            rx.vstack(
                # Línea principal: nombre y categoría
                rx.hstack(
                    rx.text(servicio["nombre"], size="3", weight="bold"),
                    rx.badge(
                        servicio.get("categoria", "General").title(),
                        color_scheme=get_color_categoria(servicio.get("categoria", "")),
                        variant="soft"
                    ),
                    spacing="2",
                    align_items="center"
                ),
                
                # Línea secundaria: descripción y código
                rx.hstack(
                    rx.text(servicio.get("codigo", ""), size="2", color="gray.500", weight="medium"),
                    rx.text("•", size="2", color="gray.400"),
                    rx.text(
                        servicio.get("descripcion", "Sin descripción"),
                        size="2",
                        color="gray.600",
                        style={"overflow": "hidden", "text_overflow": "ellipsis", "white_space": "nowrap"}
                    ),
                    spacing="2",
                    align_items="center",
                    width="100%"
                ),
                
                # Línea de precios
                rx.hstack(
                    rx.text(
                        f"${servicio.get('precio_bs', 0):,.0f} BS",
                        size="2",
                        weight="bold",
                        color="green.600"
                    ),
                    rx.text("•", size="2", color="gray.400"),
                    rx.text(
                        f"${servicio.get('precio_usd', 0):,.2f} USD",
                        size="2",
                        weight="bold",
                        color="blue.600"
                    ),
                    rx.text("•", size="2", color="gray.400"),
                    rx.text(
                        servicio.get("duracion_estimada", "30 min"),
                        size="2",
                        color="gray.500"
                    ),
                    spacing="2",
                    align_items="center"
                ),
                
                spacing="1",
                align_items="start",
                width="100%"
            ),
            
            spacing="3",
            align_items="start",
            width="100%"
        ),
        padding="3",
        border="1px solid gray.200",
        border_radius="md",
        background="white",
        _hover={"background": "gray.50", "border_color": "blue.300"},
        cursor="pointer",
        width="100%"
    )

def get_color_categoria(categoria: str) -> str:
    """🎨 Color scheme por categoría"""
    colores = {
        "preventiva": "green",
        "restaurativa": "blue",
        "estetica": "pink",
        "cirugia": "red",
        "endodoncia": "orange",
        "protesis": "gray",
        "ortodoncia": "cyan",
        "implantes": "indigo",
        "pediatrica": "yellow",
        "diagnostico": "teal",
        "emergencia": "red"
    }
    return colores.get(categoria.lower(), "gray")

def lista_procedimientos_filtrada() -> rx.Component:
    """📋 Lista de procedimientos con filtros aplicados"""
    return rx.box(
        rx.vstack(
            # Header con contador
            rx.hstack(
                rx.text("Procedimientos Disponibles", size="3", weight="bold"),
                rx.badge(
                    rx.text(f"{AppState.estado_odontologia.total_servicios_disponibles} servicios"),
                    color_scheme="blue",
                    variant="soft"
                ),
                spacing="2",
                align_items="center"
            ),
            
            # Lista de resultados
            rx.cond(
                AppState.estado_odontologia.servicios_filtrados.length() > 0,
                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(
                            AppState.estado_odontologia.servicios_filtrados,
                            item_procedimiento
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    type="always",
                    scrollbars="vertical",
                    style={"height": "400px", "width": "100%"}
                ),
                rx.box(
                    rx.vstack(
                        rx.icon("search_x", size=48, color="gray.400"),
                        rx.text("No se encontraron procedimientos", size="3", color="gray.500"),
                        rx.text(
                            "Intenta con otros términos de búsqueda o cambia los filtros",
                            size="2",
                            color="gray.400",
                            text_align="center"
                        ),
                        spacing="2",
                        align_items="center"
                    ),
                    padding="8",
                    width="100%",
                    text_align="center"
                )
            ),
            
            spacing="4",
            width="100%"
        ),
        background="white",
        border_radius="lg",
        padding="4",
        border="1px solid gray.200"
    )

# ==========================================
# ✅ RESUMEN DE SELECCIONADOS
# ==========================================

def resumen_procedimientos_seleccionados() -> rx.Component:
    """✅ Panel con resumen de procedimientos seleccionados"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text("Procedimientos Seleccionados", size="3", weight="bold"),
                rx.badge(
                    rx.text(f"{AppState.estado_odontologia.total_servicios_seleccionados}"),
                    color_scheme="green",
                    variant="solid"
                ),
                rx.spacer(),
                rx.cond(
                    AppState.estado_odontologia.total_servicios_seleccionados > 0,
                    rx.button(
                        rx.icon("x", size=14),
                        "Limpiar",
                        variant="ghost",
                        size="2",
                        color_scheme="red",
                        on_click=AppState.estado_odontologia.limpiar_servicios_seleccionados
                    ),
                    rx.fragment()
                ),
                width="100%",
                align_items="center"
            ),
            
            # Lista de seleccionados
            rx.cond(
                AppState.estado_odontologia.total_servicios_seleccionados > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.estado_odontologia.servicios_seleccionados_detalle,
                        lambda servicio: rx.hstack(
                            rx.text(servicio["nombre"], size="2", weight="medium"),
                            rx.spacer(),
                            rx.text(f"${servicio.get('precio_usd', 0):,.2f}", size="2", color="green.600", weight="bold"),
                            rx.button(
                                rx.icon("x", size=12),
                                variant="ghost",
                                size="1",
                                color_scheme="red",
                                on_click=AppState.estado_odontologia.toggle_servicio_seleccionado(
                                    servicio["codigo"], False
                                )
                            ),
                            width="100%",
                            align_items="center",
                            padding="2",
                            border="1px solid gray.200",
                            border_radius="md"
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.text(
                    "No hay procedimientos seleccionados",
                    size="2",
                    color="gray.500",
                    style={"fontStyle": "italic"}
                )
            ),
            
            # Total
            rx.cond(
                AppState.estado_odontologia.total_servicios_seleccionados > 0,
                rx.box(
                    rx.hstack(
                        rx.text("Total Estimado:", size="3", weight="bold"),
                        rx.spacer(),
                        rx.vstack(
                            rx.text(
                                f"${AppState.estado_odontologia.total_bs_intervencion:,.0f} BS",
                                size="3",
                                color="green.600",
                                weight="bold"
                            ),
                            rx.text(
                                f"${AppState.estado_odontologia.total_usd_intervencion:,.2f} USD",
                                size="3",
                                color="blue.600",
                                weight="bold"
                            ),
                            spacing="1",
                            align_items="end"
                        ),
                        width="100%",
                        align_items="center"
                    ),
                    padding="3",
                    background="gray.50",
                    border_radius="md",
                    border="1px solid gray.300"
                ),
                rx.fragment()
            ),
            
            spacing="4",
            width="100%"
        ),
        padding="4",
        background="white",
        border_radius="lg",
        border="1px solid gray.200"
    )

# ==========================================
# 🎯 COMPONENTE PRINCIPAL
# ==========================================

def selector_procedimientos_mejorado() -> rx.Component:
    """
    🎯 Selector de procedimientos completo y mejorado
    
    FUNCIONALIDADES:
    - Búsqueda en tiempo real
    - Filtros por categoría
    - Selección múltiple
    - Resumen con precios
    - Integración con AppState
    """
    return rx.vstack(
        # Campo de búsqueda
        campo_busqueda_procedimientos(),
        
        # Layout principal con 2 columnas
        rx.hstack(
            # Columna izquierda: Lista de procedimientos
            rx.box(
                lista_procedimientos_filtrada(),
                width="60%"
            ),
            
            # Columna derecha: Resumen de seleccionados
            rx.box(
                resumen_procedimientos_seleccionados(),
                width="40%"
            ),
            
            spacing="4",
            width="100%",
            align_items="start"
        ),
        
        spacing="6",
        width="100%"
    )