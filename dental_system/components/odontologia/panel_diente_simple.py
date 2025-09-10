"""
🦷 PANEL DIENTE SIMPLIFICADO - VERSIÓN PRÁCTICA
==============================================

Panel básico y útil que muestra solo información esencial del diente.
Reemplaza el panel complejo con 4 tabs por algo más práctico.

CARACTERÍSTICAS:
- Solo información realmente útil
- Sin tabs complicados
- Enfoque en lo esencial para la consulta
"""

import reflex as rx
from typing import Dict, List, Optional
from dental_system.state.app_state import AppState

# ==========================================
# 🦷 COMPONENTE SIMPLIFICADO
# ==========================================

def panel_diente_simplificado() -> rx.Component:
    """
    🦷 Panel simple que muestra información básica del diente seleccionado
    
    MUESTRA:
    - Número FDI del diente
    - Estado actual
    - Última intervención (si existe)
    - Notas rápidas para agregar
    """
    
    return rx.cond(
        # Mostrar solo si hay un diente seleccionado para detalles
        AppState.estado_odontologia.diente_activo != 0,
        
        # Panel con información del diente
        rx.box(
            rx.vstack(
                # Header del diente
                rx.hstack(
                    rx.text(
                        f"🦷 Diente {AppState.estado_odontologia.diente_activo}",
                        size="4",
                        weight="bold",
                        color="blue.600"
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=14),
                        variant="ghost",
                        size="2",
                        on_click=AppState.estado_odontologia.cerrar_detalles_diente
                    ),
                    width="100%",
                    align_items="center"
                ),
                
                rx.divider(),
                
                # Estado actual
                rx.vstack(
                    rx.text("Estado Actual", size="2", weight="bold", color="gray.700"),
                    rx.select(
                        ["Sano", "Caries", "Obturado", "Corona", "Extracción", "Implante", "Endodoncia"],
                        value=AppState.estado_odontologia.get_condicion_diente(AppState.estado_odontologia.diente_activo),
                        on_change=AppState.estado_odontologia.cambiar_condicion_diente,
                        size="2",
                        width="100%"
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                
                # Última intervención
                rx.vstack(
                    rx.text("Última Intervención", size="2", weight="bold", color="gray.700"),
                    rx.cond(
                        AppState.estado_odontologia.tiene_historial_diente,
                        rx.box(
                            rx.text("Fecha: 15/08/2024", size="2", color="gray.600"),
                            rx.text("Procedimiento: Obturación", size="2", color="gray.600"),
                            rx.text("Odontólogo: Dr. Pérez", size="2", color="gray.600"),
                            padding="3",
                            background="blue.50",
                            border_radius="md"
                        ),
                        rx.text("Sin intervenciones previas", size="2", color="gray.500", style={"fontStyle": "italic"})
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                
                # Notas rápidas
                rx.vstack(
                    rx.text("Notas para esta Consulta", size="2", weight="bold", color="gray.700"),
                    rx.text_area(
                        placeholder="Ej: Paciente refiere dolor al masticar, sensibilidad al frío...",
                        value=AppState.estado_odontologia.nota_diente_actual,
                        on_change=AppState.estado_odontologia.set_nota_diente_actual,
                        rows="3",
                        resize="vertical",
                        size="2"
                    ),
                    rx.button(
                        rx.icon("save", size=14),
                        "Guardar Nota",
                        size="2",
                        color_scheme="green",
                        on_click=AppState.estado_odontologia.guardar_nota_diente,
                        width="100%"
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%"
                ),
                
                spacing="4",
                width="100%",
                align_items="start"
            ),
            padding="4",
            background="white",
            border_radius="lg",
            border="1px solid gray.200",
            width="100%",
            height="fit-content"
        ),
        
        # Mensaje cuando no hay diente seleccionado
        rx.box(
            rx.vstack(
                rx.icon("mouse_pointer_click", size=48, color="gray.400"),
                rx.text("Haz clic en un diente", size="3", weight="medium", color="gray.500"),
                rx.text(
                    "Selecciona un diente del odontograma para ver sus detalles y agregar notas",
                    size="2",
                    color="gray.400",
                    text_align="center"
                ),
                spacing="3",
                align_items="center"
            ),
            padding="8",
            background="gray.50",
            border_radius="lg",
            border="2px dashed gray.300",
            width="100%",
            text_align="center",
            min_height="300px",
            justify_content="center",
            display="flex",
            align_items="center"
        )
    )

# ==========================================
# 🎯 ALTERNATIVA MÁS SIMPLE
# ==========================================

def info_diente_basica() -> rx.Component:
    """🎯 Información muy básica, solo lo esencial"""
    
    return rx.cond(
        AppState.estado_odontologia.total_dientes_seleccionados > 0,
        
        rx.box(
            rx.vstack(
                rx.text("Dientes Seleccionados para Intervención", size="3", weight="bold"),
                
                # Lista simple de dientes seleccionados
                rx.foreach(
                    AppState.estado_odontologia.dientes_seleccionados_lista,
                    lambda diente: rx.hstack(
                        rx.text(f"🦷 {diente['numero']}", size="2", weight="medium"),
                        rx.text(diente.get("condicion", "sano").title(), size="2", color="blue.600"),
                        rx.spacer(),
                        rx.text_area(
                            placeholder="Notas sobre este diente...",
                            rows="1",
                            size="1",
                            width="200px"
                        ),
                        width="100%",
                        align_items="center",
                        padding="2",
                        border="1px solid gray.200",
                        border_radius="md"
                    )
                ),
                
                spacing="3",
                width="100%"
            ),
            padding="4",
            background="white",
            border_radius="lg",
            border="1px solid gray.200"
        ),
        
        rx.text("No hay dientes seleccionados", size="2", color="gray.500", style={"fontStyle": "italic"})
    )