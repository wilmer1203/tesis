"""
💳 MODAL DE FACTURA PROFESIONAL - SISTEMA DUAL USD/BS
=====================================================

Modal completo de facturación con:
- Datos del paciente y consulta
- Lista detallada de servicios por odontólogo
- Formulario de pago dual USD/BS
- Validaciones y procesamiento

"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.constants import METODOS_PAGO
from dental_system.components.forms import (
    enhanced_form_field, enhanced_form_field_dinamico, form_section_header, 
    success_feedback, loading_feedback
)
from dental_system.styles.themes import (
    COLORS, SHADOWS, RADIUS, SPACING, ANIMATIONS, 
    GRADIENTS, GLASS_EFFECTS, DARK_THEME
)

# Colores del sistema (tema oscuro consistente)
COLORS_2 = {
    "primary": "#00BCD4",
    "primary_hover": "#00ACC1",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "surface": "rgba(255, 255, 255, 0.05)",
    "surface_hover": "rgba(255, 255, 255, 0.08)",
    "border": "rgba(255, 255, 255, 0.1)",
    "text_primary": "#FFFFFF",
    "text_secondary": "#94A3B8",
    "bg_dark": "#0f172a",
    "bg_darker": "#0a0f1f",
}

def seccion_datos_paciente_consulta() -> rx.Component:
    """Tarjeta unificada: Paciente (izq) + Consulta (der)"""
    return rx.box(
        rx.grid(
            # IZQUIERDA: Datos del Paciente
            rx.vstack(
                rx.text("Datos del Paciente", size="4", weight="bold", color=COLORS_2["success"]),
                rx.divider(margin="8px 0"),
                rx.vstack(
                    rx.hstack(
                        rx.text("Nombre:", size="2", color=COLORS_2["text_secondary"], width="80px"),
                        rx.text(AppState.consulta_pagar.paciente_nombre, size="2", weight="bold", flex="1"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.text("Cédula:", size="2", color=COLORS_2["text_secondary"], width="80px"),
                        rx.text(AppState.consulta_pagar.paciente_documento, size="2", weight="bold", flex="1"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.text("Teléfono:", size="2", color=COLORS_2["text_secondary"], width="80px"),
                        rx.text(AppState.consulta_pagar.paciente_telefono, size="2", weight="bold", flex="1"),
                        spacing="2",
                        align="center"
                    ),
                    spacing="1",
                    align="start"
                ),
                spacing="2",
                align="start"
            ),

            # DERECHA: Datos de la Consulta
            rx.vstack(
                rx.text("Datos de la Consulta", size="4", weight="bold", color=COLORS_2["primary"]),
                rx.divider(margin="8px 0"),
                rx.vstack(
                    rx.hstack(
                        rx.text("H. Clínica:", size="2", color=COLORS_2["text_secondary"], width="100px"),
                        rx.text(AppState.consulta_pagar.paciente_numero_historia, size="2", weight="bold", flex="1"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.text("N° Consulta:", size="2", color=COLORS_2["text_secondary"], width="100px"),
                        rx.text(AppState.consulta_pagar.numero_consulta, size="2", weight="bold", flex="1"),
                        spacing="2",
                        align="center"
                    ),
                    spacing="1",
                    align="start"
                ),
                spacing="2",
                align="start"
            ),

            columns="2",
            spacing="6",
            width="100%",
            align_items="start"
        ),

        # Estilo de la tarjeta unificada
        style={
            "background": COLORS_2["surface"],
            "backdrop_filter": "blur(10px)",
            "border": f"1px solid {COLORS_2['border']}",
            "border_radius": "12px",
            "padding": "20px",
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "width": "100%"
        }
    )


def tabla_servicios_factura() -> rx.Component:
    """Tabla de servicios realizados en formato factura"""
    return rx.box(
        rx.vstack(
            rx.text("Servicios Realizados", size="4", weight="bold"),
            rx.divider(),

            # Header de la tabla
            rx.hstack(
                rx.text("Servicio", size="2", weight="bold", style={"flex": "3"}),
                # rx.text("Odontólogo", size="2", weight="bold", style={"flex": "2"}),
                rx.text("USD", size="2", weight="bold", text_align="right", style={"flex": "1"}),
                rx.text("BS", size="2", weight="bold", text_align="right", style={"flex": "1"}),
                width="100%",
                style={
                    "background": COLORS_2["primary"] + "20",
                    "padding": "12px",
                    "border_radius": "6px"
                }
            ),

            # Filas de servicios con rx.foreach (datos reales)
            rx.cond(
                AppState.consulta_pagar.servicios_formateados.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.consulta_pagar.servicios_formateados,
                        lambda servicio: rx.hstack(
                            rx.vstack(
                                rx.text(servicio.nombre, size="2",weight="bold"),
                                rx.text(servicio.odontologo, size="2", color=COLORS_2["text_secondary"]),
                                style={"flex": "4"}
                            ),
                            # rx.text(servicio.nombre, size="2", style={"flex": "3"}),
                            # rx.text(servicio.odontologo, size="2", color=COLORS_2["text_secondary"], style={"flex": "2"}),
                            rx.text(f"${servicio.precio_usd}", size="2", text_align="right", style={"flex": "1"}),
                            rx.text(f"{servicio.precio_bs} Bs", size="2", text_align="right", style={"flex": "1"}),
                            width="100%",
                            style={
                                "padding": "10px",
                                "border_bottom": f"1px solid {COLORS_2['border']}"
                            }
                        )
                    ),
                    width="100%",
                    spacing="0"
                ),
                # Mensaje si no hay servicios
                rx.box(
                    rx.text("No hay servicios registrados", size="2", color=COLORS_2["text_secondary"], style={"text_align": "center", "padding": "20px"}),
                    width="100%"
                )
            ),

            # Total
            rx.hstack(
                rx.text("TOTAL:", size="3", weight="bold"),
                rx.spacer(),
                rx.text(
                    f"${AppState.formulario_pago_dual.monto_total_usd:.2f}",
                    size="4",
                    weight="bold",
                    color=COLORS_2["success"]
                ),
                rx.text("|", size="3", color=COLORS_2["text_secondary"]),
                rx.text(
                    f"Bs. {AppState.formulario_pago_dual.monto_total_bs:,.0f}",
                    size="4",
                    weight="bold",
                    color=COLORS_2["primary"]
                ),
                width="100%",
                style={
                    "background": f"linear-gradient(135deg, {COLORS_2['success']}20, {COLORS_2['primary']}20)",
                    "padding": "16px",
                    "border_radius": "8px",
                    "margin_top": "8px"
                }
            ),

            spacing="3",
            width="100%"
        ),
        style={
            "background": COLORS_2["surface"],
            "border": f"1px solid {COLORS_2['border']}",
            "border_radius": "8px",
            "padding": "16px"
        }
    )


def formulario_pago_dual() -> rx.Component:
    """Formulario de pago dual USD/BS"""
    return rx.vstack(
        rx.text("Información de Pago", size="4", weight="bold"),
        rx.divider(),

        # Grid de pagos USD/BS
        rx.grid(
            # Pago en USD
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("dollar-sign", size=18, color=COLORS_2["success"]),
                        rx.text("Pago en USD", size="3", weight="bold", color=COLORS_2["success"]),
                        spacing="2"
                    ),
                    rx.input(
                        placeholder="Monto en USD",
                        value=AppState.formulario_pago_dual.monto_pagado_usd,
                        on_change=lambda val: AppState.actualizar_campo_pago_dual("monto_pagado_usd", val),
                        type="number",
                        size="3"
                    ),
                    rx.select(
                        METODOS_PAGO,
                        placeholder="Método de pago",
                        value=AppState.formulario_pago_dual.metodo_pago_usd,
                        on_change=lambda val: AppState.actualizar_campo_pago_dual("metodo_pago_usd", val),
                        size="2"
                    ),
                    rx.input(
                        placeholder="Referencia (opcional)",
                        value=AppState.formulario_pago_dual.referencia_usd,
                        on_change=lambda val: AppState.actualizar_campo_pago_dual("referencia_usd", val),
                        size="2"
                    ),
                    spacing="2",
                    width="100%"
                ),
                style={
                    "background": COLORS_2["success"] + "15",
                    "border": f"1px solid {COLORS_2['success']}40",
                    "border_radius": "8px",
                    "padding": "16px"
                }
            ),

            # Pago en BS
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("wallet", size=18, color=COLORS_2["primary"]),
                        rx.text("Pago en BS", size="3", weight="bold", color=COLORS_2["primary"]),
                        spacing="2"
                    ),
                    rx.input(
                        placeholder="Monto en BS",
                        value=AppState.formulario_pago_dual.monto_pagado_bs,
                        on_change=lambda val: AppState.actualizar_campo_pago_dual("monto_pagado_bs", val),
                        type="number",
                        size="3"
                    ),
                    rx.select(
                        METODOS_PAGO,
                        placeholder="Método de pago",
                        value=AppState.formulario_pago_dual.metodo_pago_bs,
                        on_change=lambda val: AppState.actualizar_campo_pago_dual("metodo_pago_bs", val),
                        size="2"
                    ),
                    rx.input(
                        placeholder="Referencia (opcional)",
                        value=AppState.formulario_pago_dual.referencia_bs,
                        on_change=lambda val: AppState.actualizar_campo_pago_dual("referencia_bs", val),
                        size="2"
                    ),
                    spacing="2",
                    width="100%"
                ),
                style={
                    "background": COLORS_2["primary"] + "15",
                    "border": f"1px solid {COLORS_2['primary']}40",
                    "border_radius": "8px",
                    "padding": "16px"
                }
            ),

            columns="2",
            spacing="4",
            width="100%"
        ),

        # Info de tasa de cambio
        rx.callout(
            rx.hstack(
                rx.icon("info", size=16),
                rx.text(f"Tasa del día: 1 USD = {AppState.formulario_pago_dual.tasa_cambio} BS", size="2"),
                spacing="2"
            ),
            color_scheme="cyan",
            size="1"
        ),

        # Descuento opcional
        rx.box(
            rx.vstack(
                rx.text("Descuento (opcional)", size="3", weight="medium"),
                rx.input(
                    placeholder="Monto descuento USD",
                    value=AppState.formulario_pago_dual.descuento_usd,
                    on_change=lambda val: AppState.actualizar_campo_pago_dual("descuento_usd", val),
                    type="number",
                    size="2"
                ),
                rx.cond(
                    AppState.formulario_pago_dual.descuento_usd > 0,
                    rx.input(
                        placeholder="Motivo del descuento",
                        value=AppState.formulario_pago_dual.motivo_descuento,
                        on_change=lambda val: AppState.actualizar_campo_pago_dual("motivo_descuento", val),
                        size="2"
                    )
                ),
                spacing="2",
                width="100%"
            ),
            style={
                "background": COLORS_2["warning"] + "10",
                "border": f"1px solid {COLORS_2['warning']}30",
                "border_radius": "8px",
                "padding": "12px"
            }
        ),

        # Notas
        rx.text_area(
            placeholder="Notas u observaciones...",
            value=AppState.formulario_pago_dual.notas,
            on_change=lambda val: AppState.actualizar_campo_pago_dual("notas", val),
            rows="2",
            size="2"
        ),

        spacing="4",
        width="100%"
    )


def resumen_pago() -> rx.Component:
    """Resumen del pago con saldos"""
    return rx.box(
        rx.vstack(
            rx.text("Resumen del Pago", size="4", weight="bold"),
            rx.divider(),
            rx.hstack(
                rx.text("Total a pagar:", size="2"),
                rx.spacer(),
                rx.text(
                    f"${AppState.formulario_pago_dual.monto_total_usd:.2f}",
                    size="2",
                    weight="bold"
                ),
                width="100%"
            ),
            rx.hstack(
                rx.text("Descuento:", size="2", color=COLORS_2["warning"]),
                rx.spacer(),
                rx.text(
                    f"-${AppState.formulario_pago_dual.descuento_usd:.2f}",
                    size="2",
                    weight="bold",
                    color=COLORS_2["warning"]
                ),
                width="100%"
            ),
            rx.hstack(
                rx.text("Pagando ahora:", size="2", color=COLORS_2["success"]),
                rx.spacer(),
                rx.text(
                    f"${AppState.total_pagando_usd:.2f}",
                    size="2",
                    weight="bold",
                    color=COLORS_2["success"]
                ),
                width="100%"
            ),
            rx.divider(),
            rx.hstack(
                rx.text("Saldo pendiente:", size="3", weight="bold", color=COLORS_2["warning"]),
                rx.spacer(),
                rx.text(
                    f"${AppState.saldo_pendiente_calculado:.2f}",
                    size="3",
                    weight="bold",
                    color=COLORS_2["warning"]
                ),
                width="100%"
            ),
            spacing="2"
        ),
        style={
            "background": f"linear-gradient(135deg, {COLORS_2['success']}15, {COLORS_2['primary']}15)",
            "border": f"2px solid {COLORS_2['success']}",
            "border_radius": "8px",
            "padding": "16px"
        }
    )


def modal_factura_profesional() -> rx.Component:
    """
    Modal profesional de factura con sistema dual USD/BS

    Incluye:
    - Datos del paciente y consulta
    - Lista de servicios por odontólogo
    - Formulario de pago dual
    - Validaciones y resumen
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header con fondo oscuro
                
                rx.hstack(
                    form_section_header(
                        "Facturación de Consulta",
                        "Sistema Dual USD/BS",
                        "receipt",
                        COLORS["primary"]["500"]
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=20),
                            style={
                                "background": "transparent",
                                "border": "none",
                                "color": COLORS["gray"]["500"],
                                "cursor": "pointer",
                                "_hover": {"color": COLORS["gray"]["700"]}
                            }
                        ),
                        align="center"
                    ),
                    width="100%",
                    align="center"
                ),

                # Datos del paciente y consulta
                seccion_datos_paciente_consulta(),

                # Tabla de servicios
                tabla_servicios_factura(),

                # Formulario de pago
                formulario_pago_dual(),

                # Resumen
                resumen_pago(),

                # Error general
                rx.cond(
                    AppState.errores_validacion_pago.get("general", "") != "",
                    rx.callout(
                        AppState.errores_validacion_pago.get("general", ""),
                        icon="alert-circle",
                        color_scheme="red",
                        size="1"
                    )
                ),

                # Botones
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            variant="soft",
                            color_scheme="gray",
                            size="3",
                            on_click=AppState.limpiar_formulario_pago_dual
                        )
                    ),
                    rx.button(
                        "PROCESAR PAGO",
                        on_click=AppState.crear_pago_dual,
                        disabled=AppState.procesando_pago,
                        loading=AppState.procesando_pago,
                        color_scheme="green",
                        size="3",
                        style={"flex": "1"}
                    ),
                    spacing="2",
                    width="100%"
                ),

                spacing="4",
                width="100%",
                align="center"
            ),
            
            # style={
            #     "max_width": "900px",
            #     "max_height": "90vh",
            #     "overflow_y": "auto",
            #     "background": COLORS_2["bg_dark"],
            #     "color": COLORS_2["text_primary"],
            #     "border": f"1px solid {COLORS_2['border']}",
            #     "border_radius": "12px",
            #     "padding": "20px"
            # }
            
            style={
                "max_width": "600px",
                # "width": "90vw",
                # "max_height": "90vh",
                "padding": SPACING["4"],
                "border_radius": RADIUS["xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['primary']['200']}30",
                "overflow_y": "auto",
                "backdrop_filter": "blur(20px)"
            }
        ),
        open=AppState.modal_pago_dual_abierto,
        on_open_change=AppState.set_modal_pago_dual_abierto
    )
