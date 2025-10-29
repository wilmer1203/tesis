"""
💳 PÁGINA DE PAGOS CON SISTEMA DUAL USD/BS - VERSIÓN PRODUCCIÓN
================================================================

MIGRADO DESDE: pagos_page_mockup.py
DATOS: Conectado a AppState (datos reales de BD)
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.constants import METODOS_PAGO, ESTADOS_PAGO
from dental_system.components.modal_pago import modal_factura_profesional

# ==========================================
# 🎨 COLORES Y ESTILOS DEL SISTEMA
# ==========================================

COLORS = {
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
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("clock", size=24, color=COLORS["warning"]),
                        rx.text("Pendientes", size="3", color=COLORS["text_secondary"]),
                        spacing="2",
                        align="center"
                    ),
                    rx.text(
                        AppState.total_consultas_pendientes_pago,
                        size="8",
                        weight="bold",
                        color=COLORS["warning"]
                    ),
                    rx.text("consultas", size="2", color=COLORS["text_secondary"]),
                    spacing="2",
                    align="center"
                ),
                style={
                    "background": COLORS["surface"],
                    "border": f"1px solid {COLORS['border']}",
                    "border_radius": "16px",
                    "padding": "24px",
                    "text_align": "center",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "background": COLORS["surface_hover"],
                        "border_color": COLORS["warning"],
                        "transform": "translateY(-2px)"
                    }
                }
            ),

            # Card 2: Recaudado USD
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("dollar-sign", size=24, color=COLORS["success"]),
                        rx.text("Recaudado USD", size="3", color=COLORS["text_secondary"]),
                        spacing="2",
                        align="center"
                    ),
                    rx.text(
                        "$", AppState.recaudacion_usd_hoy,
                        size="8",
                        weight="bold",
                        color=COLORS["success"]
                    ),
                    rx.text("dólares hoy", size="2", color=COLORS["text_secondary"]),
                    spacing="2",
                    align="center"
                ),
                style={
                    "background": COLORS["surface"],
                    "border": f"1px solid {COLORS['border']}",
                    "border_radius": "16px",
                    "padding": "24px",
                    "text_align": "center",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "background": COLORS["surface_hover"],
                        "border_color": COLORS["success"],
                        "transform": "translateY(-2px)"
                    }
                }
            ),

            # Card 3: Recaudado BS
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("banknote", size=24, color=COLORS["success"]),
                        rx.text("Recaudado BS", size="3", color=COLORS["text_secondary"]),
                        spacing="2",
                        align="center"
                    ),
                    rx.text(
                        AppState.recaudacion_bs_hoy,
                        size="8",
                        weight="bold",
                        color=COLORS["success"]
                    ),
                    rx.text("bolívares hoy", size="2", color=COLORS["text_secondary"]),
                    spacing="2",
                    align="center"
                ),
                style={
                    "background": COLORS["surface"],
                    "border": f"1px solid {COLORS['border']}",
                    "border_radius": "16px",
                    "padding": "24px",
                    "text_align": "center",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "background": COLORS["surface_hover"],
                        "border_color": COLORS["success"],
                        "transform": "translateY(-2px)"
                    }
                }
            ),

            # Card 4: Tasa del día (editable)
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("trending-up", size=24, color=COLORS["primary"]),
                        rx.text("Tasa BS/USD", size="3", color=COLORS["text_secondary"]),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.text(
                            AppState.tasa_del_dia,
                            size="8",
                            weight="bold",
                            color=COLORS["primary"]
                        ),
                        rx.button(
                            rx.icon("edit", size=14),
                            size="1",
                            variant="soft",
                            color_scheme="cyan",
                            on_click=AppState.alternar_calculadora_conversion
                        ),
                        spacing="2",
                        align="center"
                    ),
                    rx.text("BS por dólar", size="2", color=COLORS["text_secondary"]),
                    spacing="2",
                    align="center"
                ),
                style={
                    "background": COLORS["surface"],
                    "border": f"1px solid {COLORS['border']}",
                    "border_radius": "16px",
                    "padding": "24px",
                    "text_align": "center",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "background": COLORS["surface_hover"],
                        "border_color": COLORS["primary"],
                        "transform": "translateY(-2px)",
                        "cursor": "pointer"
                    }
                },
                on_click=AppState.alternar_calculadora_conversion
            ),

            columns="4",
            spacing="4",
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
                rx.icon("clipboard-list", size=16, color=COLORS["primary"]),
                rx.heading(
                    "Consultas Pendientes de Facturación",
                    size="4",
                    color=COLORS["text_primary"],
                    weight="bold"
                ),
                spacing="3"
            ),
            width="100%",
            align="center"
        ),

        # Lista de consultas
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
                "::-webkit-scrollbar-thumb": {"background": COLORS["border"], "border_radius": "4px"},
                "::-webkit-scrollbar-thumb:hover": {"background": COLORS["primary"]}
            }
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
                            color=COLORS["text_primary"]
                        ),
                        style={
                            "background": COLORS["primary"] + "20",
                            "border_radius": "6px",
                            "padding": "4px 8px",
                            "border": f"1px solid {COLORS['primary']}30"
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
                        color=COLORS["text_secondary"]
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
                            rx.text("Hoy", size="2", color=COLORS["text_primary"]),
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
                        rx.icon("list", size=14, color=COLORS["primary"]),
                        rx.text(
                            consulta.servicios_count, " servicio(s) - Ver detalle",  # ✅ Notación de punto
                            size="2",
                            color=COLORS["primary"]
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
                                            "background": COLORS["primary"],
                                            "border_radius": "50%"
                                        }
                                    ),
                                    rx.text(
                                        srv.nombre,  # ✅ Acceso con punto (atributo del modelo)
                                        color=COLORS["text_primary"],
                                        size="2",
                                        flex="1"
                                    ),
                                    rx.hstack(
                                        rx.text("$", srv.precio_usd, size="2", weight="bold", color=COLORS["success"]),
                                        rx.text("|", size="2", color=COLORS["border"]),
                                        rx.text(srv.precio_bs, " BS", size="2", color=COLORS["text_secondary"]),
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
                            "border_left": f"2px solid {COLORS['primary']}",
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
                    rx.text("TOTAL A PAGAR", size="1", color=COLORS["text_secondary"], weight="bold"),
                    rx.hstack(
                        rx.text("$", consulta.total_usd, size="3", weight="bold", color=COLORS["success"]),  # ✅ Notación de punto
                        rx.box(style={"width": "2px", "height": "40px", "background": COLORS["border"]}),
                        rx.text(consulta.total_bs, " BS", size="3", weight="bold", color=COLORS["success"]),  # ✅ Notación de punto
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
                            "box_shadow": f"0 4px 12px {COLORS['primary']}30"
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
            "background": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "border_radius": "8px",
            "padding": "12px",
            "position": "relative",
            "overflow": "hidden",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": COLORS["surface_hover"],
                "border_color": COLORS["primary"] + "50",
                "box_shadow": f"0 2px 8px {COLORS['primary']}15"
            },
            "_before": {
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "height": "2px",
                "background": f"linear-gradient(90deg, transparent 0%, {COLORS['primary']} 50%, transparent 100%)",
                "opacity": "0.9",
                "box_shadow": f"0 0 8px {COLORS['primary']}60"
            },
        },
        width="100%"
    )

# ==========================================
# 📋 COMPONENTE: HISTORIAL DE PAGOS
# ==========================================

def historial_pagos() -> rx.Component:
    """Historial de pagos procesados"""
    return rx.vstack(
        # Header con búsqueda
        rx.hstack(
            rx.hstack(
                rx.icon("receipt", size=24, color=COLORS["primary"]),
                rx.heading("Historial de Pagos", size="4", color=COLORS["text_primary"], weight="bold"),
                spacing="3"
            ),
            rx.spacer(),
            rx.input(
                placeholder="Buscar por paciente o recibo...",
                value=AppState.termino_busqueda_pagos,
                on_change=AppState.buscar_pagos,
                size="2",
                width=["200px", "200px", "250px", "300px"],
                style={
                    "background": COLORS["surface"],
                    "border": f"1px solid {COLORS['border']}",
                    "color": COLORS["text_primary"]
                }
            ),
            rx.button(
                rx.icon("download", size=16),
                variant="soft",
                color_scheme="cyan",
                size="2"
            ),
            width="100%",
            align="center",
            spacing="4"
        ),

        # Tabla de historial
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Recibo", style={"color": COLORS["text_secondary"], "font_weight": "bold"}),
                        rx.table.column_header_cell("Paciente", style={"color": COLORS["text_secondary"], "font_weight": "bold"}),
                        rx.table.column_header_cell("USD", style={"color": COLORS["text_secondary"], "font_weight": "bold"}),
                        rx.table.column_header_cell("BS", style={"color": COLORS["text_secondary"], "font_weight": "bold"}),
                        rx.table.column_header_cell("Estado", style={"color": COLORS["text_secondary"], "font_weight": "bold"}),
                        rx.table.column_header_cell("Fecha", style={"color": COLORS["text_secondary"], "font_weight": "bold"}),
                        rx.table.column_header_cell("", style={"width": "50px"})
                    )
                ),
                rx.table.body(
                    rx.foreach(AppState.pagos_historial_formateados, fila_pago)
                ),
                variant="ghost",
                size="2",
                width="100%"
            ),
            style={
                "background": "rgba(255, 255, 255, 0.02)",
                "border": f"1px solid {COLORS['border']}",
                "border_radius": "12px",
                "padding": "20px",
                "max_height": "calc(100vh - 400px)",
                "overflow_y": "auto",
                "::-webkit-scrollbar": {"width": "8px"},
                "::-webkit-scrollbar-track": {"background": COLORS["surface"]},
                "::-webkit-scrollbar-thumb": {"background": COLORS["border"], "border_radius": "4px"},
                "::-webkit-scrollbar-thumb:hover": {"background": COLORS["primary"]}
            }
        ),

        spacing="4",
        width="100%"
    )

def fila_pago(pago) -> rx.Component:
    """Fila individual del historial de pagos"""
    return rx.table.row(
        rx.table.cell(rx.text(pago["numero_recibo"], size="2", weight="bold", color=COLORS["primary"])),
        rx.table.cell(
            rx.vstack(
                rx.text(pago["paciente_nombre"], size="2", color=COLORS["text_primary"], weight="medium"),
                rx.text(pago["paciente_documento"], size="1", color=COLORS["text_secondary"]),
                spacing="1",
                align="start"
            )
        ),
        rx.table.cell(
            rx.cond(
                pago["monto_pagado_usd"].to(float) > 0,
                rx.text("$", pago["monto_pagado_usd"], size="2", weight="bold", color=COLORS["success"]),
                rx.text("-", size="2", color=COLORS["text_secondary"])
            )
        ),
        rx.table.cell(
            rx.cond(
                pago["monto_pagado_bs"].to(float) > 0,
                rx.text(pago["monto_pagado_bs"], " BS", size="2", weight="bold", color=COLORS["success"]),
                rx.text("-", size="2", color=COLORS["text_secondary"])
            )
        ),
        rx.table.cell(
            rx.badge(
                pago["estado_pago"],
                color_scheme=rx.cond(pago["estado_pago"] == "completado", "green", "yellow"),
                variant="solid"
            )
        ),
        rx.table.cell(rx.text(pago["fecha_pago"], size="2", color=COLORS["text_secondary"])),
        rx.table.cell(
            rx.button(
                rx.icon("eye", size=14),
                variant="ghost",
                color_scheme="cyan",
                size="1"
            )
        ),
        style={"_hover": {"background": COLORS["surface"]}}
    )

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
                    rx.icon("credit-card", size=24, color=COLORS["success"]),
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
                                rx.text("Consulta:", size="2", color=COLORS["text_secondary"]),
                                rx.text(AppState.formulario_pago_dual.numero_consulta, size="2", weight="bold"),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.text("Paciente:", size="2", color=COLORS["text_secondary"]),
                                rx.text(AppState.formulario_pago_dual.paciente_nombre, size="2", weight="bold"),
                                spacing="2"
                            ),
                            spacing="2"
                        ),
                        style={
                            "background": f"{COLORS['primary']}15",
                            "padding": "12px",
                            "border_radius": "8px",
                            "border": f"1px solid {COLORS['primary']}40"
                        }
                    )
                ),

                # Totales
                rx.grid(
                    rx.vstack(
                        rx.text("Total USD", size="2", color=COLORS["text_secondary"]),
                        rx.text(f"${AppState.formulario_pago_dual.monto_total_usd:.2f}", size="5", weight="bold", color=COLORS["success"]),
                        spacing="1",
                        align="center",
                        style={"background": f"{COLORS['success']}15", "padding": "12px", "border_radius": "8px"}
                    ),
                    rx.vstack(
                        rx.text(f"Total BS (x{AppState.formulario_pago_dual.tasa_cambio})", size="2", color=COLORS["text_secondary"]),
                        rx.text(f"Bs. {AppState.formulario_pago_dual.monto_total_bs:,.0f}", size="5", weight="bold", color=COLORS["primary"]),
                        spacing="1",
                        align="center",
                        style={"background": f"{COLORS['primary']}15", "padding": "12px", "border_radius": "8px"}
                    ),
                    columns="2",
                    spacing="3",
                    width="100%"
                ),

                # Pago USD
                rx.box(
                    rx.vstack(
                        rx.text("💵 Pago en USD", size="3", weight="bold", color=COLORS["success"]),
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
                            rx.text(AppState.errores_validacion_pago.get("metodo_usd", ""), size="1", color=COLORS["error"])
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    style={"background": f"{COLORS['success']}10", "padding": "12px", "border_radius": "8px"}
                ),

                # Pago BS
                rx.box(
                    rx.vstack(
                        rx.text("💰 Pago en BS", size="3", weight="bold", color=COLORS["primary"]),
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
                            rx.text(AppState.errores_validacion_pago.get("metodo_bs", ""), size="1", color=COLORS["error"])
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    style={"background": f"{COLORS['primary']}10", "padding": "12px", "border_radius": "8px"}
                ),

                # Auto-cálculos
                rx.cond(
                    AppState.formulario_pago_dual.monto_pagado_usd > 0,
                    rx.text(
                        f"${AppState.formulario_pago_dual.monto_pagado_usd:.2f} USD = Bs. {AppState.equivalente_bs_de_usd_pagado:,.2f}",
                        size="2",
                        color=COLORS["text_secondary"]
                    )
                ),
                rx.cond(
                    AppState.formulario_pago_dual.monto_pagado_bs > 0,
                    rx.text(
                        f"Bs. {AppState.formulario_pago_dual.monto_pagado_bs:,.2f} = ${AppState.equivalente_usd_de_bs_pagado:.2f} USD",
                        size="2",
                        color=COLORS["text_secondary"]
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
                    style={"background": COLORS["surface"], "padding": "12px", "border_radius": "8px"}
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
                            rx.text("Pagando:", size="2", color=COLORS["success"]),
                            rx.spacer(),
                            rx.text(
                                f"${AppState.total_pagando_usd:.2f}",
                                size="2",
                                weight="bold",
                                color=COLORS["success"]
                            ),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Saldo pendiente:", size="2", color=COLORS["warning"]),
                            rx.spacer(),
                            rx.text(
                                f"${AppState.saldo_pendiente_calculado:.2f}",
                                size="2",
                                weight="bold",
                                color=COLORS["warning"]
                            ),
                            width="100%"
                        ),
                        spacing="2"
                    ),
                    style={
                        "background": f"linear-gradient(135deg, {COLORS['success']}20, {COLORS['primary']}20)",
                        "padding": "16px",
                        "border_radius": "8px",
                        "border": f"2px solid {COLORS['success']}"
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
        on_open_change=AppState.set_modal_pago_dual_abierto
    )

def modal_calculadora_conversion() -> rx.Component:
    """Modal de calculadora USD/BS"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("calculator", size=24, color=COLORS["primary"]),
                    rx.heading("Calculadora USD ⇄ BS", size="6", weight="bold"),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon("x", size=20, style={"cursor": "pointer"}),
                        on_click=AppState.alternar_calculadora_conversion
                    ),
                    width="100%",
                    align="center"
                ),

                # Tasa del día
                rx.box(
                    rx.hstack(
                        rx.icon("trending-up", size=16, color=COLORS["success"]),
                        rx.text("Tasa del día:", size="3", weight="medium", color=COLORS["text_primary"]),
                        rx.text("1 USD = ", AppState.tasa_del_dia, " BS", size="3", weight="bold", color=COLORS["success"]),
                        spacing="2",
                        align="center"
                    ),
                    style={
                        "background": "rgba(34, 197, 94, 0.1)",
                        "border": f"1px solid {COLORS['success']}40",
                        "border_radius": "8px",
                        "padding": "12px"
                    }
                ),

                # Convertidor USD → BS
                rx.vstack(
                    rx.text("💵 USD → BS", size="4", weight="bold", color=COLORS["primary"]),
                    rx.input(
                        placeholder="Ingrese monto en USD...",
                        value=AppState.monto_calculadora_usd,
                        on_change=AppState.calcular_conversion_usd_a_bs,
                        type="number",
                        min="0",
                        step="0.01",
                        size="3"
                    ),
                    rx.hstack(
                        rx.icon("arrow-down", size=20, color=COLORS["primary"]),
                        rx.text("=", size="5", weight="bold", color=COLORS["primary"]),
                        spacing="2"
                    ),
                    rx.box(
                        rx.text(AppState.monto_calculadora_bs, " BS", size="5", weight="bold", color=COLORS["success"]),
                        style={
                            "padding": "12px",
                            "background": "rgba(34, 197, 94, 0.1)",
                            "border": f"2px solid {COLORS['success']}60",
                            "border_radius": "8px",
                            "text_align": "center",
                            "width": "100%"
                        }
                    ),
                    spacing="3",
                    width="100%"
                ),

                # Divider
                rx.separator(size="4"),

                # Convertidor BS → USD
                rx.vstack(
                    rx.text("💰 BS → USD", size="4", weight="bold", color=COLORS["primary"]),
                    rx.input(
                        placeholder="Ingrese monto en BS...",
                        value=AppState.monto_calculadora_bs,
                        on_change=AppState.calcular_conversion_bs_a_usd,
                        type="number",
                        min="0",
                        step="0.01",
                        size="3"
                    ),
                    rx.hstack(
                        rx.icon("arrow-down", size=20, color=COLORS["primary"]),
                        rx.text("=", size="5", weight="bold", color=COLORS["primary"]),
                        spacing="2"
                    ),
                    rx.box(
                        rx.text("$", AppState.monto_calculadora_usd, " USD", size="5", weight="bold", color=COLORS["primary"]),
                        style={
                            "padding": "12px",
                            "background": "rgba(6, 182, 212, 0.1)",
                            "border": f"2px solid {COLORS['primary']}60",
                            "border_radius": "8px",
                            "text_align": "center",
                            "width": "100%"
                        }
                    ),
                    spacing="3",
                    width="100%"
                ),

                # Botones
                rx.hstack(
                    rx.button(
                        rx.hstack(rx.icon("rotate-ccw", size=16), rx.text("Limpiar", size="2"), spacing="2"),
                        on_click=AppState.limpiar_calculadora,
                        variant="outline",
                        color_scheme="gray",
                        size="2"
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.hstack(rx.icon("check", size=16), rx.text("Cerrar", size="2"), spacing="2"),
                            variant="solid",
                            color_scheme="cyan",
                            size="2",
                            on_click=AppState.alternar_calculadora_conversion
                        )
                    ),
                    spacing="3",
                    justify="center",
                    width="100%"
                ),

                spacing="6",
                width="100%"
            ),
            style={
                "max_width": "450px",
                "padding": "24px",
                "background": COLORS["bg_dark"],
                "border": f"1px solid {COLORS['border']}",
                "backdrop_filter": "blur(12px)"
            }
        ),
        open=AppState.calculadora_activa
    )

# ==========================================
# 📱 PÁGINA PRINCIPAL
# ==========================================

def pagos_page() -> rx.Component:
    """Página principal de gestión de pagos"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                # Header principal
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            "💳 Gestión de Pagos",
                            size="8",
                            weight="bold",
                            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            background_clip="text",
                            style={"-webkit-background-clip": "text", "-webkit-text-fill-color": "transparent"}
                        ),
                        rx.text(
                            "Sistema dual USD/BS para facturación y control de pagos",
                            size="4",
                            color=COLORS["text_secondary"],
                            weight="medium"
                        ),
                        spacing="1",
                        align="start",
                        width="100%"
                    ),
                    rx.button(rx.text("actualizar datos"), on_click=AppState.recargar_todo_pagos, variant="outline", color_scheme="cyan", size="3"),
                    width="100%",
                    align="center",
                    spacing="4"
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
                            "border": f"1px solid {COLORS['border']}",
                            "border_radius": "12px",
                            "padding": "20px",
                            "height": "fit-content",
                            "min_height": "500px"
                        }
                    ),

                    # Columna derecha: Historial de pagos
                    rx.box(
                        historial_pagos(),
                        style={
                            "background": "rgba(255, 255, 255, 0.02)",
                            "border": f"1px solid {COLORS['border']}",
                            "border_radius": "12px",
                            "padding": "20px",
                            "min_height": "500px"
                        }
                    ),
                    columns=rx.breakpoints(initial="1", md="1", lg="1fr 2fr", xl="1fr 2fr"),
                    spacing="6",
                    width="100%",
                    align_items="start"
                ),

                spacing="6",
                width="100%",
                padding="32px",
                max_width="1800px",
                margin="0 auto"
            ),
            width="100%",
            align_items="start"
        ),
        modal_factura_profesional(),  # ✨ NUEVO MODAL PROFESIONAL
        modal_calculadora_conversion(),
        style={
            "background": COLORS["bg_gradient"],
            "min_height": "100vh",
            "color": COLORS["text_primary"]
        },
        on_mount=AppState.cargar_datos_pagos_page
    )
