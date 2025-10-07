"""
🛡️ MODAL DE VALIDACIÓN ODONTOGRAMA - FASE 5
==============================================

Modal flotante para mostrar errores y warnings de validación médica.

CARACTERÍSTICAS:
- Lista de errores críticos (bloquean guardado)
- Lista de warnings (permiten continuar)
- Detalles por regla con sugerencias
- Botones contextuales según tipo de validación

USADO EN: intervencion_page.py

Autor: Sistema Dental V3.0
Fecha: Septiembre 2025
"""

import reflex as rx
from typing import Dict, Any
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, RADIUS, SPACING

def error_item(error: Dict[str, Any]) -> rx.Component:
    """
    ❌ Item individual de error crítico

    Args:
        error: Dict con mensaje, diente, superficie, sugerencia
    """
    return rx.box(
        rx.hstack(
            # Ícono de error
            rx.box(
                rx.icon("x-circle", size=20, color="red"),
                flex_shrink=0
            ),

            # Contenido
            rx.vstack(
                # Mensaje principal
                rx.text(
                    error["mensaje"],
                    font_weight="600",
                    color="red",
                    size="3"
                ),

                # Sugerencia
                # FIX: COLORS["text"] no existe, usar DARK_THEME["colors"]["text_secondary"]
                rx.text(
                    error["sugerencia"],
                    size="2",
                    color=COLORS["gray"]["500"],
                    font_style="italic"
                ),

                spacing="1",
                align_items="start",
                flex="1"
            ),

            spacing="3",
            align_items="start",
            width="100%"
        ),

        padding="3",
        border=f"1px solid {COLORS['error']['500']}",
        border_radius=RADIUS["md"],
        background=f"{COLORS['error']['500']}10",
        width="100%"
    )


def warning_item(warning: Dict[str, Any]) -> rx.Component:
    """
    ⚠️ Item individual de warning (advertencia)

    Args:
        warning: Dict con mensaje, diente, sugerencia
    """
    return rx.box(
        rx.hstack(
            # Ícono de warning
            rx.box(
                rx.icon("triangle-alert", size=20, color=COLORS["warning"]["500"]),
                flex_shrink=0
            ),

            # Contenido
            rx.vstack(
                # Mensaje principal
                rx.text(
                    warning["mensaje"],
                    font_weight="600",
                    color=COLORS["warning"]["500"],
                    size="3"
                ),

                # Sugerencia
                # FIX: COLORS["text"] no existe, usar gray["500"] como color secundario
                rx.text(
                    warning["sugerencia"],
                    size="2",
                    color=COLORS["gray"]["500"],
                    font_style="italic"
                ),

                spacing="1",
                align_items="start",
                flex="1"
            ),

            spacing="3",
            align_items="start",
            width="100%"
        ),

        padding="3",
        border=f"1px solid {COLORS['warning']['500']}",
        border_radius=RADIUS["md"],
        background=f"{COLORS['warning']['500']}10",
        width="100%"
    )


def modal_validacion_odontograma() -> rx.Component:
    """
    🛡️ FASE 5.4: Modal principal de validación

    Muestra errores y warnings de validación médica.

    CASOS:
    1. Solo errores: Bloquea guardado, solo botón "Corregir"
    2. Solo warnings: Permite continuar, botones "Continuar" y "Revisar"
    3. Ambos: Bloquea guardado, muestra ambas listas
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("shield-alert", size=24, color=COLORS["warning"]["500"]),
                    rx.heading(
                        "Validación del Odontograma",
                        size="6",
                        font_weight="700"
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            size="2",
                            on_click=AppState.cerrar_modal_validacion
                        )
                    ),
                    spacing="3",
                    align_items="center",
                    width="100%"
                ),

                rx.divider(),

                # Contenido scroll
                rx.scroll_area(
                    rx.vstack(
                        # ==========================================
                        # SECCIÓN ERRORES CRÍTICOS
                        # ==========================================
                        rx.cond(
                            AppState.validacion_errores.length() > 0,
                            rx.vstack(
                                # Header errores
                                rx.hstack(
                                    rx.icon("x-circle", size=20, color="red"),
                                    rx.heading(
                                        "❌ Errores Críticos",
                                        size="4",
                                        color="red"
                                    ),
                                    rx.badge(
                                        AppState.validacion_errores.length(),
                                        color_scheme="red"
                                    ),
                                    spacing="2",
                                    align_items="center"
                                ),

                                # FIX: COLORS["text"] no existe, usar gray["500"]
                                rx.text(
                                    "Los siguientes errores deben corregirse antes de guardar:",
                                    size="2",
                                    color=COLORS["gray"]["500"]
                                ),

                                # Lista de errores
                                rx.vstack(
                                    rx.foreach(
                                        AppState.validacion_errores,
                                        error_item
                                    ),
                                    spacing="2",
                                    width="100%"
                                ),

                                spacing="3",
                                width="100%",
                                padding="4",
                                border=f"2px solid {COLORS['error']['500']}",
                                border_radius=RADIUS["lg"],
                                background=f"{COLORS['error']['500']}05"
                            )
                        ),

                        # ==========================================
                        # SECCIÓN WARNINGS (ADVERTENCIAS)
                        # ==========================================
                        rx.cond(
                            AppState.validacion_warnings.length() > 0,
                            rx.vstack(
                                # Header warnings
                                rx.hstack(
                                    rx.icon("triangle-alert", size=20, color=COLORS["warning"]["500"]),
                                    rx.heading(
                                        "⚠️ Advertencias",
                                        size="4",
                                        color=COLORS["warning"]["500"]
                                    ),
                                    rx.badge(
                                        AppState.validacion_warnings.length(),
                                        color_scheme="yellow"
                                    ),
                                    spacing="2",
                                    align_items="center"
                                ),

                                # FIX: COLORS["text"] no existe, usar gray["500"]
                                rx.text(
                                    "Revise las siguientes advertencias. Puede continuar guardando si lo desea:",
                                    size="2",
                                    color=COLORS["gray"]["500"]
                                ),

                                # Lista de warnings
                                rx.vstack(
                                    rx.foreach(
                                        AppState.validacion_warnings,
                                        warning_item
                                    ),
                                    spacing="2",
                                    width="100%"
                                ),

                                spacing="3",
                                width="100%",
                                padding="4",
                                border=f"2px solid {COLORS['warning']['500']}",
                                border_radius=RADIUS["lg"],
                                background=f"{COLORS['warning']['500']}05"
                            )
                        ),

                        spacing="4",
                        width="100%"
                    ),

                    max_height="60vh",
                    width="100%"
                ),

                rx.divider(),

                # Footer con botones contextuales
                rx.hstack(
                    # CASO 1: Solo warnings (puede continuar)
                    rx.cond(
                        (AppState.validacion_errores.length() == 0) & (AppState.validacion_warnings.length() > 0),
                        rx.hstack(
                            # Botón revisar
                            rx.button(
                                rx.hstack(
                                    rx.icon("pencil", size=16),
                                    rx.text("Revisar Cambios"),
                                    spacing="2"
                                ),
                                variant="outline",
                                size="3",
                                on_click=AppState.cerrar_modal_validacion
                            ),

                            # Botón continuar
                            rx.button(
                                rx.hstack(
                                    rx.icon("check", size=16),
                                    rx.text("Continuar Guardando"),
                                    spacing="2"
                                ),
                                size="3",
                                on_click=AppState.forzar_guardado_con_warnings,
                                style={
                                    "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['success']['400']} 100%)",
                                    "color": "white"
                                }
                            ),

                            spacing="3",
                            justify="end",
                            width="100%"
                        )
                    ),

                    # CASO 2: Hay errores (debe corregir)
                    rx.cond(
                        AppState.validacion_errores.length() > 0,
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", size=16),
                                    rx.text("Cerrar y Corregir"),
                                    spacing="2"
                                ),
                                size="3",
                                on_click=AppState.cerrar_modal_validacion,
                                style={
                                    "background": f"linear-gradient(135deg, {COLORS['error']['500']} 0%, {COLORS['error']['400']} 100%)",
                                    "color": "white"
                                }
                            ),

                            spacing="3",
                            justify="end",
                            width="100%"
                        )
                    ),

                    width="100%"
                ),

                spacing="4",
                width="100%"
            ),

            max_width="800px",
            padding="6"
        ),

        open=AppState.modal_validacion_abierto
    )


def boton_validar_manual() -> rx.Component:
    """
    🔘 Botón para validar manualmente sin guardar

    Útil para pre-validar cambios antes de intentar guardar
    """
    return rx.button(
        rx.hstack(
            rx.icon("shield-check", size=16),
            rx.text("Validar Cambios", size="3"),
            spacing="2"
        ),
        variant="outline",
        size="3",
        on_click=lambda: AppState.set_modal_validacion_abierto(True),  # TODO: Implementar validación previa
        style={
            "border": f"1px solid {COLORS['primary']['500']}",
            "color": COLORS["primary"]["500"],
            "_hover": {
                "background": f"{COLORS['primary']['500']}10"
            }
        }
    )
