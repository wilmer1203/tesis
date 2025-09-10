"""
🦷 COMPONENTE: SISTEMA VERSIONADO ODONTOGRAMA
============================================

Sistema automático de versionado para el odontograma con detección de cambios
significativos, comparación entre versiones y vinculación con intervenciones.

CARACTERÍSTICAS:
- Versionado automático cuando se detectan cambios significativos
- Comparación visual entre versiones (antes/después)
- Timeline histórico de versiones
- Vinculación automática con intervenciones
- Modal de confirmación para nuevas versiones
- Sistema de comentarios por versión
"""

import reflex as rx
from typing import Dict, List, Optional
from datetime import datetime, date
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS DEL SISTEMA VERSIONADO
# ==========================================

VERSIONADO_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["sm"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["4"],
    "height": "100%"
}

VERSION_CARD_STYLE = {
    "background": COLORS['gray']['50'],
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "margin_bottom": SPACING["2"],
    "transition": "all 0.2s ease",
    "_hover": {
        "border_color": COLORS['primary']['400'],
        "box_shadow": SHADOWS["sm"]
    }
}

TIMELINE_ITEM_STYLE = {
    "border_left": f"3px solid {COLORS['primary']['400']}",
    "padding_left": SPACING["3"],
    "margin_bottom": SPACING["4"],
    "position": "relative"
}

# ==========================================
# 🕘 TIMELINE DE VERSIONES
# ==========================================

def timeline_versiones() -> rx.Component:
    """📜 Timeline cronológico de todas las versiones del odontograma"""
    return rx.vstack(
        rx.hstack(
            rx.text("📜 Historial de Versiones", weight="bold", size="4"),
            rx.spacer(),
            rx.button(
                rx.icon("refresh_cw", size=16),
                "Refrescar",
                size="2",
                variant="outline",
                on_click=AppState.cargar_historial_versiones
            ),
            width="100%",
            align_items="center",
            margin_bottom="4"
        ),
        
        # Timeline items
        rx.vstack(
            # Versión actual (primera en timeline)
            item_version_timeline(
                "v2.1",
                "Versión Actual",
                "15/08/2024 14:30",
                "Dr. García",
                "Obturación diente 16 - superficie oclusal",
                "current",
                cambios_detectados=[
                    "Diente 16: Sano → Obturado",
                    "Superficie oclusal: Nueva obturación con resina compuesta"
                ]
            ),
            
            # Versiones anteriores
            item_version_timeline(
                "v2.0",
                "Intervención Anterior",
                "10/08/2024 10:15",
                "Dr. García",
                "Limpieza dental general",
                "completed",
                cambios_detectados=[
                    "Diente 21: Caries superficial → Limpieza",
                    "Profilaxis general realizada"
                ]
            ),
            
            item_version_timeline(
                "v1.0",
                "Primera Evaluación",
                "05/08/2024 09:00",
                "Dr. García",
                "Evaluación inicial del paciente",
                "initial",
                cambios_detectados=[
                    "Odontograma inicial creado",
                    "Estado general: Bueno"
                ]
            ),
            
            spacing="0",
            width="100%"
        ),
        
        spacing="3",
        width="100%"
    )

def item_version_timeline(
    version: str,
    titulo: str,
    fecha: str,
    doctor: str,
    descripcion: str,
    tipo: str,
    cambios_detectados: List[str] = []
) -> rx.Component:
    """📝 Item individual del timeline de versiones"""
    
    # Colores según tipo de versión
    color_schemes = {
        "current": "green",
        "completed": "blue",
        "initial": "gray"
    }
    
    iconos = {
        "current": "circle_check",
        "completed": "clock",
        "initial": "star"
    }
    
    return rx.box(
        rx.vstack(
            # Header de la versión
            rx.hstack(
                rx.badge(
                    version,
                    color_scheme=color_schemes.get(tipo, "blue"),
                    size="2"
                ),
                rx.vstack(
                    rx.text(titulo, weight="bold", size="3"),
                    rx.text(descripcion, size="2", color="gray.600"),
                    align_items="start",
                    spacing="0"
                ),
                rx.spacer(),
                rx.icon(iconos.get(tipo, "clock"), size=20, color=COLORS['primary']['500']),
                spacing="3",
                align_items="start",
                width="100%"
            ),
            
            # Metadatos de la versión
            rx.hstack(
                rx.hstack(
                    rx.icon("calendar", size=14),
                    rx.text(fecha, size="1", color="gray.500"),
                    spacing="1",
                    align_items="center"
                ),
                rx.hstack(
                    rx.icon("user", size=14),
                    rx.text(doctor, size="1", color="gray.500"),
                    spacing="1",
                    align_items="center"
                ),
                spacing="4",
                align_items="center"
            ),
            
            # Cambios detectados (expandible)
            rx.cond(
                len(cambios_detectados) > 0,
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.hstack(
                            rx.icon("file_diff", size=14),
                            rx.text(f"{len(cambios_detectados)} cambios detectados", size="2", color="primary.600"),
                            spacing="1"
                        )
                    ),
                    rx.dialog.content(
                        rx.vstack(
                            *[
                                rx.hstack(
                                    rx.icon("chevron_right", size=12, color="green.500"),
                                    rx.text(cambio, size="1", color="gray.700"),
                                    spacing="1",
                                    align_items="center"
                                )
                                for cambio in cambios_detectados
                            ],
                            spacing="1",
                            align_items="start",
                            padding_top="2"
                        )
                    ),
                    width="100%"
                ),
                rx.box()
            ),
            
            # Botones de acción
            rx.hstack(
                rx.button(
                    rx.icon("eye", size=14),
                    "Ver",
                    size="1",
                    variant="outline",
                    on_click=lambda: AppState.ver_version_odontograma(version)
                ),
                rx.button(
                    rx.icon("git_compare", size=14),
                    "Comparar",
                    size="1",
                    variant="outline",
                    on_click=lambda: AppState.comparar_version(version)
                ),
                rx.cond(
                    tipo != "current",
                    rx.button(
                        rx.icon("rotate_ccw", size=14),
                        "Restaurar",
                        size="1",
                        color_scheme="orange",
                        on_click=lambda: AppState.restaurar_version(version)
                    ),
                    rx.box()
                ),
                spacing="2"
            ),
            
            spacing="2",
            align_items="start",
            width="100%"
        ),
        style=TIMELINE_ITEM_STYLE,
        width="100%"
    )

# ==========================================
# 🔄 MODAL CONFIRMACIÓN NUEVA VERSIÓN
# ==========================================

def modal_nueva_version() -> rx.Component:
    """📋 Modal para confirmar la creación de una nueva versión"""
    return rx.dialog.root(
        rx.dialog.trigger(rx.box()),  # Trigger invisible
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("git_branch", size=24, color="primary.500"),
                    rx.vstack(
                        rx.text("Nueva Versión Detectada", weight="bold", size="5"),
                        rx.text("Se han detectado cambios significativos en el odontograma", size="3", color="gray.600"),
                        align_items="start",
                        spacing="0"
                    ),
                    spacing="3",
                    align_items="center",
                    width="100%",
                    margin_bottom="4"
                ),
                
                # Cambios detectados
                rx.vstack(
                    rx.text("🔍 Cambios Detectados:", weight="medium", size="3"),
                    rx.vstack(
                        cambio_detectado("Diente 16", "Sano", "Obturado", "Nueva obturación con resina compuesta"),
                        cambio_detectado("Diente 21", "Caries", "Restaurado", "Limpieza y aplicación de flúor"),
                        spacing="2",
                        width="100%"
                    ),
                    align_items="start",
                    width="100%",
                    margin_bottom="4"
                ),
                
                # Formulario de comentarios
                rx.vstack(
                    rx.text("💬 Comentarios de la Versión:", weight="medium", size="3"),
                    rx.text_area(
                        placeholder="Describe los cambios realizados en esta sesión...\n\nEjemplo: Obturación diente 16 con resina compuesta. Limpieza general y aplicación de flúor preventivo.",
                        value=AppState.comentario_nueva_version,
                        on_change=AppState.actualizar_comentario_version,
                        rows="4",
                        width="100%"
                    ),
                    align_items="start",
                    width="100%",
                    margin_bottom="4"
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="outline",
                        on_click=AppState.cancelar_nueva_version
                    ),
                    rx.button(
                        rx.icon("save", size=16),
                        "Crear Versión",
                        color_scheme="blue",
                        on_click=AppState.confirmar_nueva_version
                    ),
                    spacing="2",
                    justify="end",
                    width="100%"
                ),
                
                spacing="4",
                width="100%"
            ),
            max_width="500px",
            width="90vw"
        ),
        open=AppState.modal_nueva_version_abierto
    )

def cambio_detectado(diente: str, estado_anterior: str, estado_nuevo: str, descripcion: str) -> rx.Component:
    """🔄 Visualización de un cambio detectado"""
    return rx.card(
        rx.hstack(
            rx.text(diente, weight="bold", size="2", color="primary.600"),
            rx.hstack(
                rx.badge(estado_anterior, color_scheme="gray", size="1"),
                rx.icon("arrow_right", size=14),
                rx.badge(estado_nuevo, color_scheme="green", size="1"),
                spacing="1",
                align_items="center"
            ),
            spacing="3",
            align_items="center",
            width="100%"
        ),
        rx.text(descripcion, size="1", color="gray.600", margin_top="1"),
        size="1",
        width="100%"
    )

# ==========================================
# 📊 COMPARADOR DE VERSIONES
# ==========================================

def comparador_versiones() -> rx.Component:
    """🔍 Panel de comparación entre dos versiones del odontograma"""
    return rx.vstack(
        # Header del comparador
        rx.hstack(
            rx.text("🔍 Comparación de Versiones", weight="bold", size="4"),
            rx.spacer(),
            rx.button(
                "Cerrar Comparación",
                variant="outline",
                on_click=AppState.cerrar_comparador
            ),
            width="100%",
            align_items="center",
            margin_bottom="4"
        ),
        
        # Selectores de versiones a comparar
        rx.hstack(
            rx.vstack(
                rx.text("Versión A", weight="medium", size="2"),
                rx.select(
                    ["v2.1 (Actual)", "v2.0", "v1.0"],
                    value=AppState.version_comparar_a,
                    on_change=AppState.cambiar_version_a,
                    width="100%"
                ),
                align_items="start",
                width="48%"
            ),
            rx.vstack(
                rx.text("Versión B", weight="medium", size="2"),
                rx.select(
                    ["v2.1 (Actual)", "v2.0", "v1.0"],
                    value=AppState.version_comparar_b,
                    on_change=AppState.cambiar_version_b,
                    width="100%"
                ),
                align_items="start",
                width="48%"
            ),
            justify="between",
            width="100%",
            margin_bottom="4"
        ),
        
        # Panel de diferencias
        rx.vstack(
            rx.text("📋 Diferencias Encontradas:", weight="medium", size="3"),
            rx.vstack(
                diferencia_diente("Diente 16", "v2.0: Sano", "v2.1: Obturado", "added"),
                diferencia_diente("Diente 21", "v2.0: Caries", "v2.1: Restaurado", "modified"),
                diferencia_diente("Diente 34", "v2.0: Presente", "v2.1: Presente", "unchanged"),
                spacing="2",
                width="100%"
            ),
            align_items="start",
            width="100%"
        ),
        
        spacing="3",
        width="100%"
    )

def diferencia_diente(diente: str, estado_a: str, estado_b: str, tipo: str) -> rx.Component:
    """⚖️ Visualización de diferencias entre versiones por diente"""
    
    colores = {
        "added": "green",
        "modified": "yellow", 
        "removed": "red",
        "unchanged": "gray"
    }
    
    iconos = {
        "added": "plus",
        "modified": "edit",
        "removed": "minus",
        "unchanged": "check"
    }
    
    return rx.card(
        rx.hstack(
            rx.icon(iconos[tipo], size=16, color=f"{colores[tipo]}.500"),
            rx.text(diente, weight="bold", size="2"),
            rx.hstack(
                rx.text(estado_a, size="1", color="gray.600"),
                rx.icon("arrow_right", size=12) if tipo != "unchanged" else rx.box(),
                rx.text(estado_b, size="1", color="gray.600"),
                spacing="2",
                align_items="center"
            ),
            spacing="3",
            align_items="center",
            width="100%",
            justify="between"
        ),
        variant="ghost",
        size="1",
        width="100%"
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL VERSIONADO
# ==========================================

def sistema_versionado_odontograma() -> rx.Component:
    """
    🦷 Sistema completo de versionado del odontograma
    
    FUNCIONALIDADES:
    - Timeline histórico de versiones
    - Modal de confirmación para nuevas versiones
    - Comparador visual entre versiones
    - Detección automática de cambios significativos
    """
    
    return rx.box(
        rx.vstack(
            # Header del sistema
            rx.hstack(
                rx.icon("git_branch", size=24, color="primary.500"),
                rx.vstack(
                    rx.text("Sistema de Versiones", weight="bold", size="4"),
                    rx.text("Historial automático de cambios en el odontograma", size="2", color="gray.600"),
                    align_items="start",
                    spacing="0"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.badge(
                        f"v{AppState.version_actual_odontograma}",
                        color_scheme="green",
                        size="2"
                    ),
                    rx.button(
                        rx.icon("plus", size=16),
                        "Nueva Versión Manual",
                        size="2",
                        variant="outline",
                        on_click=AppState.crear_version_manual
                    ),
                    spacing="2"
                ),
                spacing="3",
                align_items="center",
                width="100%",
                margin_bottom="4"
            ),
            
            # Contenido principal
            rx.cond(
                AppState.modo_comparacion_activo,
                comparador_versiones(),
                timeline_versiones()
            ),
            
            spacing="3",
            width="100%",
            height="100%"
        ),
        
        # Modales
        modal_nueva_version(),
        
        style=VERSIONADO_CONTAINER_STYLE,
        width="100%",
        height="100%"
    )