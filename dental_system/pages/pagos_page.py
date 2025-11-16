"""
💳 PÁGINA DE PAGOS CON SISTEMA DUAL USD/BS - VERSIÓN PRODUCCIÓN
================================================================

MIGRADO DESDE: pagos_page_mockup.py
DATOS: Conectado a AppState (datos reales de BD)
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.constants import METODOS_PAGO, ESTADOS_PAGO
from dental_system.components.modal_pago import modal_factura_profesional, modal_detalle_pago
from dental_system.components.common import page_header, medical_page_layout, stat_card, refresh_button
from dental_system.components.table_components import pagos_table, empty_state
from dental_system.styles.themes import COLORS, GLASS_EFFECTS, SPACING, RADIUS, SHADOWS
# ==========================================
# 🎨 COLORES Y ESTILOS DEL SISTEMA
# ==========================================

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
    "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
}

# Alias para compatibilidad con código existente
METODOS_PAGO_DISPONIBLES = METODOS_PAGO

# ==========================================
# 📊 COMPONENTE: ESTADÍSTICAS SUPERIORES
# ==========================================

def estadisticas_financieras() -> rx.Component:
    """Cards de estadísticas financieras del día"""
    return rx.box(
        rx.grid(
            # Card 1: Consultas pendientes
            stat_card(
                "Consultas Pendientes",
                # f"{AppState.consultas_pendientes_pagar.length()}",
                "10",
                "clock",
                color=COLORS["primary"]["600"]
            ),
            stat_card(
                "Recaudado hoy USD",
                f"$ {AppState.recaudacion_usd_hoy}",
                "dollar-sign",
                color=COLORS["success"]["500"]
            ),
            stat_card(
                "Recaudado hoy BS",
                f"{AppState.recaudacion_bs_hoy}",
                "banknote",
                color=COLORS["warning"]["500"]
            ),
            # Card de tasa con botón para cambiar
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("banknote", size=20, color=COLORS["primary"]["600"]),
                        rx.text("Tasa BS/USD", size="2", color=COLORS["gray"]["25"], weight="medium"),
                        rx.spacer(),
                        rx.button(
                            rx.icon("edit", size=14),
                            on_click=lambda: AppState.set_modal_cambiar_tasa_abierto(True),
                            variant="ghost",
                            size="1",
                            color_scheme="cyan"
                        ),
                        width="100%",
                        align="center"
                    ),
                    rx.text(f"{AppState.tasa_del_dia:.2f} BS/$", size="6", weight="bold", color=COLORS["gray"]["25"]),
                    rx.text("Click para cambiar", size="1", color=COLORS["primary"]["600"]),
                    spacing="2",
                    align="start",
                    width="100%"
                ),
                style={
                    "max_width": "800px",
                    "padding": SPACING["8"],
                    "border_radius": RADIUS["2xl"],
                    **GLASS_EFFECTS["strong"],
                    "box_shadow": SHADOWS["2xl"],
                    "border": f"1px solid {COLORS['primary']['200']}30",
                    "overflow_y": "auto"
                }
            ),
            columns="4",
            spacing="6",
            width="100%"
        ),
        width="100%"
    )

# ==========================================
# 🏥 COMPONENTE: CONSULTAS PENDIENTES
# ==========================================

def consultas_pendientes_lista() -> rx.Component:
    """Lista de consultas pendientes de facturación"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.hstack(
                rx.icon("clipboard-list", size=16, color=COLORS_2["primary"]),
                rx.heading(
                    "Consultas Pendientes de Facturación",
                    size="4",
                    color=COLORS_2["text_primary"],
                    weight="bold"
                ),
                spacing="3"
            ),
            width="100%",
            align="center"
        ),

        # Lista de consultas
        rx.cond(
            AppState.consultas_pendientes_pagar,
            rx.box(
                rx.vstack(
                    rx.foreach(
                        AppState.consultas_pendientes_pagar,
                        consulta_card
                    ),
                    spacing="3",
                    width="100%"
                ),
                style={
                    "max_height": "calc(100vh - 350px)",
                    "overflow_y": "auto",
                    "padding_right": "4px",
                    "::-webkit-scrollbar": {"width": "6px"},
                    "::-webkit-scrollbar-track": {"background": "transparent"},
                    "::-webkit-scrollbar-thumb": {"background": COLORS_2["border"], "border_radius": "4px"},
                    "::-webkit-scrollbar-thumb:hover": {"background": COLORS_2["primary"]}
                }
            ),
            empty_state(
                    "No hay Consultas Pendientes de Facturación",
                    "",
                    "clipboard-list"
                )
        ),
        
        spacing="3",
        width="100%"
    )

def consulta_card(consulta) -> rx.Component:
    """Card individual de consulta pendiente con accordion de servicios"""
    # ✅ Ahora consulta es ConsultaPendientePago (tipado)
    return rx.box(
        rx.vstack(
            # Fila 1: Número de consulta, paciente y badge de días
            rx.hstack(
                rx.vstack(
                    rx.box(
                        rx.text(
                            consulta.numero_consulta,  # ✅ Notación de punto
                            size="2",
                            weight="bold",
                            color=COLORS_2["text_primary"]
                        ),
                        style={
                            "background": COLORS_2["primary"] + "20",
                            "border_radius": "6px",
                            "padding": "4px 8px",
                            "border": f"1px solid {COLORS_2['primary']}30"
                        }
                    ),
                    rx.text(
                        consulta.paciente_nombre,  # ✅ Notación de punto
                        size="3",
                        weight="medium"
                    ),
                    rx.text(
                        consulta.paciente_documento,  # ✅ Notación de punto
                        size="1",
                        color=COLORS_2["text_secondary"]
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.spacer(),

                # Badge de días pendientes
                rx.cond(
                    consulta.dias_pendiente > 0,  # ✅ Notación de punto
                    rx.badge(
                        rx.hstack(
                            rx.icon("alert-circle", size=12),
                            rx.text(consulta.dias_pendiente, size="2"),  # ✅ Notación de punto
                            rx.text(" días", size="2"),
                            spacing="1"
                        ),
                        color_scheme=rx.cond(consulta.dias_pendiente > 3, "red", "yellow"),  # ✅ Notación de punto
                        variant="solid"
                    ),
                    rx.badge(
                        rx.hstack(
                            rx.icon("clock", size=12),
                            rx.text("Hoy", size="2", color=COLORS_2["text_primary"]),
                            spacing="1"
                        ),
                        color_scheme="blue",
                        variant="soft"
                    )
                ),
                width="100%",
                align="center"
            ),

            # Fila 2: Accordion de servicios detallados
            rx.accordion.root(
                rx.accordion.item(
                    header=rx.hstack(
                        rx.icon("list", size=14, color=COLORS_2["primary"]),
                        rx.text(
                            consulta.servicios_count, " servicio(s) - Ver detalle",  # ✅ Notación de punto
                            size="2",
                            color=COLORS_2["primary"]
                        ),
                        spacing="2",
                        width="100%",
                        style={
                            "align_items": "center"
                        }
                    ),
                    content=rx.box(
                        rx.vstack(
                            rx.foreach(
                                consulta.servicios_formateados,  # ✅ Notación de punto - lista tipada
                                lambda srv: rx.hstack(
                                    rx.box(
                                        style={
                                            "width": "6px",
                                            "height": "6px",
                                            "background": COLORS_2["primary"],
                                            "border_radius": "50%"
                                        }
                                    ),
                                    rx.text(
                                        srv.nombre,  # ✅ Acceso con punto (atributo del modelo)
                                        color=COLORS_2["text_primary"],
                                        size="2",
                                        flex="1"
                                    ),
                                    rx.hstack(
                                        rx.text("$", srv.precio_usd, size="2", weight="bold", color=COLORS_2["success"]),
                                        rx.text("|", size="2", color=COLORS_2["border"]),
                                        rx.text(srv.precio_bs, " BS", size="2", color=COLORS_2["text_secondary"]),
                                        spacing="1"
                                    ),
                                    spacing="2",
                                    width="100%",
                                    align="center",
                                    padding="4px 0"
                                )
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        style={
                            "background": "rgba(0, 188, 212, 0.05)",
                            "border_left": f"2px solid {COLORS_2['primary']}",
                            "padding": "8px",
                            "border_radius": "6px",
                            "margin_top": "4px"
                        }
                    ),
                    value="servicios"
                ),
                collapsible=True,
                width="100%",
                variant="ghost",
                style={
                    "margin": "0",
                    "padding": "0",
                    # ✅ Reducir padding cuando está cerrado
                    "--accordion-content-padding": "0",
                    "--accordion-trigger-padding": "4px 0"
                }
            ),

            # Fila 3: Totales y botón de acción
            rx.hstack(
                rx.vstack(
                    rx.text("TOTAL A PAGAR", size="1", color=COLORS_2["text_secondary"], weight="bold"),
                    rx.hstack(
                        rx.text("$", consulta.total_usd, size="3", weight="bold", color=COLORS_2["success"]),  # ✅ Notación de punto
                        rx.box(style={"width": "2px", "height": "40px", "background": COLORS_2["border"]}),
                        rx.text(consulta.total_bs, " BS", size="3", weight="bold", color=COLORS_2["success"]),  # ✅ Notación de punto
                        spacing="2",
                        align="center"
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("credit-card", size=16),
                        rx.text("FACTURAR", size="1", weight="bold"),
                        spacing="1"
                    ),
                    on_click=lambda: AppState.seleccionar_consulta_para_pago(consulta.pago_id),  # ✅ Notación de punto
                    variant="solid",
                    color_scheme="cyan",
                    size="1",
                    style={
                        "padding": "6px 12px",
                        "cursor": "pointer",
                        "transition": "all 0.2s ease",
                        "_hover": {
                            "transform": "translateY(-1px)",
                            "box_shadow": f"0 4px 12px {COLORS_2['primary']}30"
                        }
                    }
                ),
                width="100%",
                align="center"
            ),

            spacing="2",
            width="100%"
        ),
        style={
            "background": COLORS_2["surface"],
            "border": f"1px solid {COLORS_2['border']}",
            "border_radius": "8px",
            "padding": "12px",
            "position": "relative",
            "overflow": "hidden",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": COLORS_2["surface_hover"],
                "border_color": COLORS_2["primary"] + "50",
                "box_shadow": f"0 2px 8px {COLORS_2['primary']}15"
            },
            "_before": {
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "height": "2px",
                "background": f"linear-gradient(90deg, transparent 0%, {COLORS_2['primary']} 50%, transparent 100%)",
                "opacity": "0.9",
                "box_shadow": f"0 0 8px {COLORS_2['primary']}60"
            },
        },
        width="100%"
    )

# ==========================================
# 📋 COMPONENTE: HISTORIAL DE PAGOS (Ahora usa pagos_table de table_components.py)
# ==========================================
# Las funciones historial_pagos() y fila_pago() han sido reemplazadas por
# pagos_table() de table_components.py para mayor consistencia y reutilización

# ==========================================
# 🧮 MODAL CALCULADORA DE CONVERSIÓN
# ==========================================

def modal_pago_dual() -> rx.Component:
    """Modal completo de pago dual USD/BS con validaciones"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("credit-card", size=24, color=COLORS_2["success"]),
                    rx.text("Procesar Pago", size="6", weight="bold"),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon("x", size=20, style={"cursor": "pointer"}),
                        on_click=AppState.limpiar_formulario_pago_dual
                    ),
                    width="100%",
                    align="center"
                ),
                rx.divider(),

                # Info consulta seleccionada
                rx.cond(
                    AppState.formulario_pago_dual.consulta_id != "",
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Consulta:", size="2", color=COLORS_2["text_secondary"]),
                                rx.text(AppState.formulario_pago_dual.numero_consulta, size="2", weight="bold"),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.text("Paciente:", size="2", color=COLORS_2["text_secondary"]),
                                rx.text(AppState.formulario_pago_dual.paciente_nombre, size="2", weight="bold"),
                                spacing="2"
                            ),
                            spacing="2"
                        ),
                        style={
                            "background": f"{COLORS_2['primary']}15",
                            "padding": "12px",
                            "border_radius": "8px",
                            "border": f"1px solid {COLORS_2['primary']}40"
                        }
                    )
                ),

                # Totales
                rx.grid(
                    rx.vstack(
                        rx.text("Total USD", size="2", color=COLORS_2["text_secondary"]),
                        rx.text(f"${AppState.formulario_pago_dual.monto_total_usd:.2f}", size="5", weight="bold", color=COLORS_2["success"]),
                        spacing="1",
                        align="center",
                        style={"background": f"{COLORS_2['success']}15", "padding": "12px", "border_radius": "8px"}
                    ),
                    rx.vstack(
                        rx.text(f"Total BS (x{AppState.formulario_pago_dual.tasa_cambio})", size="2", color=COLORS_2["text_secondary"]),
                        rx.text(f"Bs. {AppState.formulario_pago_dual.monto_total_bs:,.0f}", size="5", weight="bold", color=COLORS_2["primary"]),
                        spacing="1",
                        align="center",
                        style={"background": f"{COLORS_2['primary']}15", "padding": "12px", "border_radius": "8px"}
                    ),
                    columns="2",
                    spacing="3",
                    width="100%"
                ),

                # Pago USD
                rx.box(
                    rx.vstack(
                        rx.text("💵 Pago en USD", size="3", weight="bold", color=COLORS_2["success"]),
                        rx.input(
                            placeholder="Monto en USD",
                            value=AppState.formulario_pago_dual.monto_pagado_usd,
                            on_change=lambda val: AppState.actualizar_campo_pago_dual("monto_pagado_usd", val),
                            type="number",
                            size="3"
                        ),
                        rx.select(
                            METODOS_PAGO_DISPONIBLES,
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
                        rx.cond(
                            AppState.errores_validacion_pago.get("metodo_usd", "") != "",
                            rx.text(AppState.errores_validacion_pago.get("metodo_usd", ""), size="1", color=COLORS_2["error"])
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    style={"background": f"{COLORS_2['success']}10", "padding": "12px", "border_radius": "8px"}
                ),

                # Pago BS
                rx.box(
                    rx.vstack(
                        rx.text("💰 Pago en BS", size="3", weight="bold", color=COLORS_2["primary"]),
                        rx.input(
                            placeholder="Monto en BS",
                            value=AppState.formulario_pago_dual.monto_pagado_bs,
                            on_change=lambda val: AppState.actualizar_campo_pago_dual("monto_pagado_bs", val),
                            type="number",
                            size="3"
                        ),
                        rx.select(
                            METODOS_PAGO_DISPONIBLES,
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
                        rx.cond(
                            AppState.errores_validacion_pago.get("metodo_bs", "") != "",
                            rx.text(AppState.errores_validacion_pago.get("metodo_bs", ""), size="1", color=COLORS_2["error"])
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    style={"background": f"{COLORS_2['primary']}10", "padding": "12px", "border_radius": "8px"}
                ),

                # Auto-cálculos
                rx.cond(
                    AppState.formulario_pago_dual.monto_pagado_usd > 0,
                    rx.text(
                        f"${AppState.formulario_pago_dual.monto_pagado_usd:.2f} USD = Bs. {AppState.equivalente_bs_de_usd_pagado:,.2f}",
                        size="2",
                        color=COLORS_2["text_secondary"]
                    )
                ),
                rx.cond(
                    AppState.formulario_pago_dual.monto_pagado_bs > 0,
                    rx.text(
                        f"Bs. {AppState.formulario_pago_dual.monto_pagado_bs:,.2f} = ${AppState.equivalente_usd_de_bs_pagado:.2f} USD",
                        size="2",
                        color=COLORS_2["text_secondary"]
                    )
                ),

                # Descuento opcional
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Descuento (opcional):", size="2", weight="medium"),
                            spacing="2"
                        ),
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
                    style={"background": COLORS_2["surface"], "padding": "12px", "border_radius": "8px"}
                ),

                # Notas
                rx.text_area(
                    placeholder="Notas u observaciones...",
                    value=AppState.formulario_pago_dual.notas,
                    on_change=lambda val: AppState.actualizar_campo_pago_dual("notas", val),
                    rows="2",
                    size="2"
                ),

                # Resumen - usando computed var para evitar problemas con max()
                rx.box(
                    rx.vstack(
                        rx.text("Resumen del Pago", size="3", weight="bold"),
                        rx.divider(),
                        rx.hstack(
                            rx.text("Total a pagar:", size="2"),
                            rx.spacer(),
                            rx.text(f"${AppState.formulario_pago_dual.monto_total_usd:.2f}", size="2", weight="bold"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Pagando:", size="2", color=COLORS_2["success"]),
                            rx.spacer(),
                            rx.text(
                                f"${AppState.total_pagando_usd:.2f}",
                                size="2",
                                weight="bold",
                                color=COLORS_2["success"]
                            ),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Saldo pendiente:", size="2", color=COLORS_2["warning"]),
                            rx.spacer(),
                            rx.text(
                                f"${AppState.saldo_pendiente_calculado:.2f}",
                                size="2",
                                weight="bold",
                                color=COLORS_2["warning"]
                            ),
                            width="100%"
                        ),
                        spacing="2"
                    ),
                    style={
                        "background": f"linear-gradient(135deg, {COLORS_2['success']}20, {COLORS_2['primary']}20)",
                        "padding": "16px",
                        "border_radius": "8px",
                        "border": f"2px solid {COLORS_2['success']}"
                    }
                ),

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
                        rx.button("Cancelar", variant="soft", color_scheme="gray", size="3", on_click=AppState.limpiar_formulario_pago_dual)
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
                width="100%"
            ),
            style={
                "max_width": "600px",
                "max_height": "90vh",
                "overflow_y": "auto"
            }
        ),
        open=AppState.modal_pago_dual_abierto,
    )

def modal_cambiar_tasa() -> rx.Component:
    """💱 Modal compacto para cambiar tasa de cambio"""
    from dental_system.components.forms import form_section_header, enhanced_form_field,validated_input
    from dental_system.styles.themes import ANIMATIONS, GRADIENTS, SHADOWS, GLASS_EFFECTS, DARK_THEME

    return rx.dialog.root(
        rx.dialog.content(
            # Header elegante
            rx.vstack(
                rx.hstack(
                    form_section_header(
                        "Cambiar Tasa del Día",
                        "Actualizar tasa de cambio BS/USD",
                        "trending-up",
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
                        )
                    ),
                    width="100%",
                    align="center"
                ),
                spacing="4",
                width="100%",
                margin_bottom=SPACING["4"]
            ),

            # Formulario compacto
            rx.form(
                rx.vstack(
                    # Input de tasa con validated_input
                    validated_input(
                        label="Nueva Tasa BS/USD",
                        field_name="tasa_temporal",
                        value=AppState.tasa_temporal,
                        on_change=lambda field, value: AppState.set_tasa_temporal(value),
                        input_type="number",
                        placeholder="Ej: 37.50",
                        required=True,
                        icon="dollar-sign",
                        help_text=f"Tasa actual: {AppState.tasa_del_dia:.2f} BS/$",
                        validation_error=""
                    ),

                    # Botones
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", size=16),
                                    rx.text("Cancelar"),
                                    spacing="2",
                                    align="center"
                                ),
                                style={
                                    **GLASS_EFFECTS["light"],
                                    "border": f"1px solid {COLORS['gray']['300']}",
                                    "color": COLORS["gray"]["700"],
                                    "border_radius": RADIUS["xl"],
                                    "padding": f"{SPACING['3']} {SPACING['5']}",
                                    "font_weight": "600",
                                    "transition": ANIMATIONS["presets"]["crystal_hover"],
                                    "_hover": {
                                        **GLASS_EFFECTS["medium"],
                                        "transform": "translateY(-2px)",
                                        "box_shadow": SHADOWS["sm"]
                                    }
                                },
                                on_click=AppState.set_modal_cambiar_tasa_abierto(False)
                            )
                        ),

                        rx.spacer(),

                        rx.button(
                            rx.hstack(
                                rx.text("Actualizar Tasa"),
                                rx.icon("check", size=16),
                                spacing="2",
                                align="center"
                            ),
                            style={
                                "background": GRADIENTS["neon_primary"],
                                "color": "white",
                                "border": "none",
                                "border_radius": RADIUS["xl"],
                                "padding": f"{SPACING['3']} {SPACING['6']}",
                                "font_weight": "700",
                                "font_size": "1rem",
                                "box_shadow": SHADOWS["glow_primary"],
                                "transition": ANIMATIONS["presets"]["crystal_hover"],
                                "_hover": {
                                    "transform": "translateY(-2px) scale(1.02)",
                                    "box_shadow": f"0 0 30px {COLORS['primary']['500']}40, {SHADOWS['crystal_lg']}"
                                }
                            },
                            on_click=lambda: AppState.actualizar_tasa_del_dia(AppState.tasa_temporal)
                        ),

                        width="100%",
                        align="center"
                    ),

                    spacing="4",
                    width="100%",
                    align="start"
                )
            ),

            style={
                "max_width": "500px",
                "padding": SPACING["8"],
                "border_radius": RADIUS["3xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['primary']['200']}30",
                "overflow_y": "auto",
                "backdrop_filter": "blur(20px)"
            }
        ),
        open=AppState.modal_cambiar_tasa_abierto,
        on_open_change=AppState.set_modal_cambiar_tasa_abierto(False)
    )


# ==========================================
# 📱 PÁGINA PRINCIPAL
# ==========================================

def pagos_page() -> rx.Component:
    """Página principal de gestión de pagos"""
    return rx.box(
        medical_page_layout(
            rx.vstack(
                # Header principal
                page_header(
                    "Gestión de Pagos",
                    "Sistema dual USD/BS para facturación y control de pagos",
                    actions=[
                        refresh_button(
                            text="Actualizar datos",
                            on_click=AppState.recargar_todo_pagos,
                            loading=AppState.procesando_pago
                        )
                    ]
                ),
                # Estadísticas superiores
                estadisticas_financieras(),

                # Layout principal en 2 columnas
                rx.grid(
                    # Columna izquierda: Consultas pendientes
                    rx.box(
                        consultas_pendientes_lista(),
                        style={
                            "background": "rgba(255, 255, 255, 0.02)",
                            "border": f"1px solid {COLORS_2['border']}",
                            "border_radius": "12px",
                            "padding": "20px",
                            "height": "fit-content",
                            "min_height": "500px"
                        }
                    ),

                    # Columna derecha: Historial de pagos (tabla reutilizable)
                    rx.box(
                        pagos_table(),  # ✅ Nueva tabla reutilizable
                        style={
                            "background": "rgba(255, 255, 255, 0.02)",
                            "border": f"1px solid {COLORS_2['border']}",
                            "border_radius": "12px",
                            "min_height": "550px"
                        }
                    ),
                    columns=rx.breakpoints(initial="1", md="1", lg="1fr 3fr", xl="1fr 3fr"),
                    spacing="6",
                    width="100%",
                    align_items="start"
                ),
                spacing="6",
                width="100%"
            ),
        ),
        modal_factura_profesional(),  # ✨ NUEVO MODAL PROFESIONAL
        modal_detalle_pago(),  # 👁️ Modal de detalle de pago
        modal_cambiar_tasa(),  # ✨ Modal para cambiar tasa de cambio
        on_mount=AppState.cargar_datos_pagos_page
    )
