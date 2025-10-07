"""
💳 PÁGINA DE PAGOS CON SISTEMA DUAL USD/BS - VERSIÓN COMPLETA
================================================================

DISEÑO IMPLEMENTADO:
- 📊 Estadísticas financieras en tiempo real
- 🏥 Lista de consultas pendientes de facturación
- 💰 Formulario de pago dual USD/BS
- 📋 Historial de pagos procesados
- 🧮 Calculadora de conversión
- 📱 Diseño responsive

FLUJO:
1. Cargar consultas pendientes de pago
2. Seleccionar consulta → Pre-llenar formulario
3. Procesar pago dual → Actualizar listas
4. Ver historial y estadísticas
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button, medical_page_layout
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,
    dark_crystal_card, dark_header_style, dark_page_background,
    create_dark_style
)

# ==========================================
# 🎨 ESTILOS ESPECÍFICOS DE PAGOS
# ==========================================

PAGOS_COLORS = {
    "primary": COLORS["primary"]["400"],        # Turquesa sistema
    "secondary": COLORS["blue"]["500"],         # Azul secundario
    "success": COLORS["success"]["500"],        # Verde para completados
    "warning": COLORS["warning"]["500"],        # Naranja para pendientes
    "error": COLORS["error"]["500"],           # Rojo para errores
    "surface": DARK_THEME["colors"]["surface_secondary"],
    "border": DARK_THEME["colors"]["border"],
    "text_primary": DARK_THEME["colors"]["text_primary"],
    "text_secondary": DARK_THEME["colors"]["text_secondary"]
}

def pagos_card_style():
    return {
        "background": "rgba(255, 255, 255, 0.05)",
        "border": f"1px solid {PAGOS_COLORS['border']}",
        "border_radius": RADIUS["lg"],
        "padding": SPACING["4"],
        "backdrop_filter": "blur(10px)",
        "box_shadow": SHADOWS["lg"],
        "_hover": {
            "background": "rgba(255, 255, 255, 0.08)",
            "border_color": PAGOS_COLORS["primary"]
        }
    }

# ==========================================
# 📊 COMPONENTE: ESTADÍSTICAS FINANCIERAS
# ==========================================

def estadisticas_financieras() -> rx.Component:
    """📊 Cards de estadísticas financieras del día"""
    return rx.vstack(
        rx.heading(
            "📊 Resumen Financiero del Día",
            size="6",
            color=PAGOS_COLORS["text_primary"],
            weight="bold"
        ),

        rx.grid(
            # Consultas Pendientes
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("clock", size=24, color=PAGOS_COLORS["warning"]),
                        rx.text("Pendientes", size="3", color=PAGOS_COLORS["text_secondary"]),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.text(
                        AppState.total_consultas_pendientes_pago,
                        size="7",
                        weight="bold",
                        color=PAGOS_COLORS["warning"]
                    ),
                    rx.text("consultas", size="2", color=PAGOS_COLORS["text_secondary"]),
                    spacing="1",
                    align_items="center"
                ),
                style=pagos_card_style(),
                text_align="center"
            ),

            # Recaudado USD
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("dollar-sign", size=24, color=PAGOS_COLORS["success"]),
                        rx.text("Recaudado USD", size="3", color=PAGOS_COLORS["text_secondary"]),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.text(
                        f"${AppState.recaudacion_usd_hoy:.2f}",
                        size="7",
                        weight="bold",
                        color=PAGOS_COLORS["success"]
                    ),
                    rx.text("dólares", size="2", color=PAGOS_COLORS["text_secondary"]),
                    spacing="1",
                    align_items="center"
                ),
                style=pagos_card_style(),
                text_align="center"
            ),

            # Recaudado BS
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("banknote", size=24, color=PAGOS_COLORS["success"]),
                        rx.text("Recaudado BS", size="3", color=PAGOS_COLORS["text_secondary"]),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.text(
                        f"{AppState.recaudacion_bs_hoy:,.0f}",
                        size="7",
                        weight="bold",
                        color=PAGOS_COLORS["success"]
                    ),
                    rx.text("bolívares", size="2", color=PAGOS_COLORS["text_secondary"]),
                    spacing="1",
                    align_items="center"
                ),
                style=pagos_card_style(),
                text_align="center"
            ),

            # Tasa del Día
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("trending-up", size=24, color=PAGOS_COLORS["primary"]),
                        rx.text("Tasa BS/USD", size="3", color=PAGOS_COLORS["text_secondary"]),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.text(
                        f"{AppState.tasa_del_dia:.2f}",
                        size="7",
                        weight="bold",
                        color=PAGOS_COLORS["primary"]
                    ),
                    rx.hstack(
                        rx.button(
                            rx.icon("edit", size=12),
                            size="1",
                            variant="soft",
                            color_scheme="cyan",
                            on_click=AppState.alternar_calculadora_conversion
                        ),
                        rx.text("BS/$", size="2", color=PAGOS_COLORS["text_secondary"]),
                        spacing="1",
                        align_items="center"
                    ),
                    spacing="1",
                    align_items="center"
                ),
                style=pagos_card_style(),
                text_align="center"
            ),

            columns="4",
            spacing="4",
            width="100%"
        ),

        spacing="4",
        width="100%"
    )

# ==========================================
# 🏥 COMPONENTE: CONSULTAS PENDIENTES
# ==========================================

def consultas_pendientes_lista() -> rx.Component:
    """🏥 Lista de consultas completadas pendientes de facturación"""
    return rx.vstack(
        rx.hstack(
            rx.heading(
                "🏥 Consultas Pendientes de Facturación",
                size="5",
                color=PAGOS_COLORS["text_primary"],
                weight="bold"
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("refresh-cw", size=16),
                    rx.text("Actualizar", size="2"),
                    spacing="2"
                ),
                on_click=AppState.cargar_consultas_pendientes_pago,
                loading=AppState.cargando_consultas_pendientes,
                variant="soft",
                color_scheme="cyan",
                size="2"
            ),
            width="100%",
            align_items="center"
        ),

        rx.cond(
            AppState.cargando_consultas_pendientes,
            rx.center(
                rx.spinner(size="3", color=PAGOS_COLORS["primary"]),
                padding="4"
            ),
            rx.cond(
                AppState.total_consultas_pendientes_pago > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.consultas_pendientes_facturacion,
                        lambda consulta: consulta_pendiente_card(consulta)
                    ),
                    spacing="3",
                    width="100%"
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("circle-check", size=32, color=PAGOS_COLORS["success"]),
                        rx.text(
                            "No hay consultas pendientes de pago",
                            size="4",
                            color=PAGOS_COLORS["text_secondary"]
                        ),
                        spacing="2",
                        align_items="center"
                    ),
                    padding="8"
                )
            )
        ),

        spacing="4",
        width="100%"
    )

def consulta_pendiente_card(consulta) -> rx.Component:
    """🏥 Card individual de consulta pendiente"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        consulta["numero_consulta"],
                        size="4",
                        weight="bold",
                        color=PAGOS_COLORS["primary"]
                    ),
                    rx.text(
                        consulta["paciente_nombre"],
                        size="3",
                        weight="medium",
                        color=PAGOS_COLORS["text_primary"]
                    ),
                    spacing="1",
                    align_items="start"
                ),

                rx.spacer(),

                rx.vstack(
                    rx.text(
                        consulta["odontologo_nombre"],
                        size="2",
                        color=PAGOS_COLORS["text_secondary"]
                    ),
                    rx.text(
                        f"{consulta['servicios_count']} servicios",
                        size="2",
                        color=PAGOS_COLORS["text_secondary"]
                    ),
                    spacing="1",
                    align_items="end"
                ),

                rx.vstack(
                    rx.text(
                        f"${consulta['total_usd']:.2f}",
                        size="4",
                        weight="bold",
                        color=PAGOS_COLORS["success"]
                    ),
                    rx.text(
                        f"{consulta['total_bs']:,.0f} BS",
                        size="2",
                        color=PAGOS_COLORS["text_secondary"]
                    ),
                    spacing="1",
                    align_items="end"
                ),

                rx.button(
                    rx.hstack(
                        rx.icon("credit-card", size=16),
                        rx.text("FACTURAR", size="2"),
                        spacing="2"
                    ),
                    on_click=lambda: AppState.seleccionar_consulta_para_pago(consulta["consulta_id"]),
                    variant="solid",
                    color_scheme="cyan",
                    size="2"
                ),

                width="100%",
                align_items="center"
            ),

            rx.text(
                f"Concepto: {consulta['concepto']}",
                size="2",
                color=PAGOS_COLORS["text_secondary"],
                style={"font_style": "italic"}
            ),

            spacing="2",
            width="100%"
        ),
        style=pagos_card_style(),
        width="100%"
    )

# ==========================================
# 💰 COMPONENTE: FORMULARIO PAGO DUAL
# ==========================================

def formulario_pago_dual() -> rx.Component:
    """💰 Formulario de procesamiento de pago dual USD/BS"""
    return rx.vstack(
        rx.heading(
            "💰 Procesar Pago Dual USD/BS",
            size="5",
            color=PAGOS_COLORS["text_primary"],
            weight="bold"
        ),

        rx.box(
            rx.cond(
                AppState.formulario_pago_dual.consulta_id != "",
                formulario_pago_activo(),
                formulario_pago_vacio()
            ),
            style=pagos_card_style(),
            width="100%"
        ),

        spacing="4",
        width="100%"
    )

def formulario_pago_vacio() -> rx.Component:
    """💳 Estado cuando no hay consulta seleccionada"""
    return rx.center(
        rx.vstack(
            rx.icon("arrow-up", size=32, color=PAGOS_COLORS["text_secondary"]),
            rx.text(
                "Selecciona una consulta pendiente para procesar el pago",
                size="3",
                color=PAGOS_COLORS["text_secondary"],
                text_align="center"
            ),
            spacing="3",
            align_items="center"
        ),
        padding="8"
    )

def formulario_pago_activo() -> rx.Component:
    """💳 Formulario activo con datos pre-llenados"""
    return rx.vstack(
        # Información de la consulta
        rx.box(
            rx.vstack(
                rx.text("Consulta Seleccionada", size="3", weight="medium", color=PAGOS_COLORS["text_primary"]),
                rx.text(
                    AppState.formulario_pago_dual.concepto,
                    size="4",
                    weight="bold",
                    color=PAGOS_COLORS["primary"]
                ),
                spacing="1"
            ),
            style={
                "background": "rgba(0, 188, 212, 0.1)",
                "border": f"1px solid {PAGOS_COLORS['primary']}",
                "border_radius": RADIUS["md"],
                "padding": SPACING["3"]
            }
        ),

        # Montos adeudados
        rx.grid(
            rx.vstack(
                rx.text("Total Adeudado USD", size="2", color=PAGOS_COLORS["text_secondary"]),
                rx.text(
                    f"${AppState.formulario_pago_dual.monto_total_usd:.2f}",
                    size="5",
                    weight="bold",
                    color=PAGOS_COLORS["success"]
                ),
                spacing="1",
                align_items="center"
            ),
            rx.vstack(
                rx.text("Equivalente en BS", size="2", color=PAGOS_COLORS["text_secondary"]),
                rx.text(
                    f"{AppState.monto_total_bs_calculado:,.0f} BS",
                    size="5",
                    weight="bold",
                    color=PAGOS_COLORS["success"]
                ),
                spacing="1",
                align_items="center"
            ),
            columns="2",
            spacing="4",
            width="100%"
        ),

        # Campos de pago
        rx.grid(
            rx.vstack(
                rx.text("Pago en USD", size="3", weight="medium", color=PAGOS_COLORS["text_primary"]),
                rx.input(
                    value=AppState.formulario_pago_dual.pago_usd,
                    on_change=lambda v: AppState.recalcular_formulario_dual(),
                    placeholder="0.00",
                    type="number",
                    step="0.01"
                ),
                spacing="1",
                width="100%"
            ),
            rx.vstack(
                rx.text("Pago en BS", size="3", weight="medium", color=PAGOS_COLORS["text_primary"]),
                rx.input(
                    value=AppState.formulario_pago_dual.pago_bs,
                    on_change=lambda v: AppState.recalcular_formulario_dual(),
                    placeholder="0.00",
                    type="number",
                    step="0.01"
                ),
                spacing="1",
                width="100%"
            ),
            columns="2",
            spacing="4",
            width="100%"
        ),

        # Saldo pendiente
        rx.cond(
            AppState.saldo_pendiente_usd_calculado > 0,
            rx.box(
                rx.vstack(
                    rx.text("Saldo Pendiente", size="3", weight="medium", color=PAGOS_COLORS["warning"]),
                    rx.hstack(
                        rx.text(
                            f"${AppState.saldo_pendiente_usd_calculado:.2f} USD",
                            size="3",
                            weight="bold",
                            color=PAGOS_COLORS["warning"]
                        ),
                        rx.text("|", color=PAGOS_COLORS["text_secondary"]),
                        rx.text(
                            f"{AppState.saldo_pendiente_bs_calculado:,.0f} BS",
                            size="3",
                            weight="bold",
                            color=PAGOS_COLORS["warning"]
                        ),
                        spacing="2"
                    ),
                    spacing="1",
                    align_items="center"
                ),
                style={
                    "background": "rgba(255, 193, 7, 0.1)",
                    "border": f"1px solid {PAGOS_COLORS['warning']}",
                    "border_radius": RADIUS["md"],
                    "padding": SPACING["3"],
                    "text_align": "center"
                }
            ),
            rx.box()  # Elemento vacío cuando no hay saldo
        ),

        # Tasa del día
        rx.hstack(
            rx.text("Tasa del día:", size="3", color=PAGOS_COLORS["text_secondary"]),
            rx.text(
                f"{AppState.tasa_del_dia:.2f} BS/USD",
                size="3",
                weight="bold",
                color=PAGOS_COLORS["primary"]
            ),
            rx.button(
                rx.icon("calculator", size=14),
                size="1",
                variant="soft",
                color_scheme="cyan",
                on_click=AppState.alternar_calculadora_conversion
            ),
            spacing="2",
            align_items="center",
            justify="center"
        ),

        # Errores de validación
        rx.cond(
            AppState.errores_validacion_pago.keys().length() > 0,
            rx.box(
                rx.foreach(
                    AppState.errores_validacion_pago.values(),
                    lambda error: rx.text(
                        error,
                        size="2",
                        color=PAGOS_COLORS["error"]
                    )
                ),
                style={
                    "background": "rgba(244, 67, 54, 0.1)",
                    "border": f"1px solid {PAGOS_COLORS['error']}",
                    "border_radius": RADIUS["md"],
                    "padding": SPACING["3"]
                }
            ),
            rx.box()
        ),

        # Botones de acción
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon("calculator", size=16),
                    rx.text("Calculadora", size="2"),
                    spacing="2"
                ),
                on_click=AppState.alternar_calculadora_conversion,
                variant="outline",
                color_scheme="cyan",
                size="2"
            ),

            rx.spacer(),

            rx.button(
                rx.hstack(
                    rx.icon("x", size=16),
                    rx.text("Cancelar", size="2"),
                    spacing="2"
                ),
                on_click=AppState.cancelar_formulario_pago,
                variant="outline",
                color_scheme="gray",
                size="2"
            ),

            rx.button(
                rx.cond(
                    AppState.procesando_pago,
                    rx.hstack(
                        rx.spinner(size="2", color="white"),
                        rx.text("Procesando...", size="2"),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.icon("credit-card", size=16),
                        rx.text("PROCESAR PAGO", size="2"),
                        spacing="2"
                    )
                ),
                on_click=AppState.procesar_pago_consulta,
                loading=AppState.procesando_pago,
                variant="solid",
                color_scheme="cyan",
                size="2"
            ),

            width="100%",
            align_items="center"
        ),

        spacing="4",
        width="100%"
    )

# ==========================================
# 📋 COMPONENTE: HISTORIAL DE PAGOS
# ==========================================

def historial_pagos() -> rx.Component:
    """📋 Tabla de historial de pagos procesados"""
    return rx.vstack(
        rx.hstack(
            rx.heading(
                "📋 Historial de Pagos Procesados",
                size="5",
                color=PAGOS_COLORS["text_primary"],
                weight="bold"
            ),
            rx.spacer(),
            rx.hstack(
                rx.input(
                    placeholder="Buscar por paciente o recibo...",
                    value=AppState.termino_busqueda_pagos,
                    on_change=AppState.buscar_pagos,
                    size="2"
                ),
                rx.button(
                    rx.icon("download", size=16),
                    variant="outline",
                    color_scheme="cyan",
                    size="2"
                ),
                spacing="2"
            ),
            width="100%",
            align_items="center"
        ),

        # Tabla de pagos
        rx.cond(
            AppState.lista_pagos.length() > 0,
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Recibo"),
                            rx.table.column_header_cell("Paciente"),
                            rx.table.column_header_cell("Concepto"),
                            rx.table.column_header_cell("USD"),
                            rx.table.column_header_cell("BS"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Fecha"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            AppState.pagos_filtrados_display,
                            lambda pago: fila_historial_pago(pago)
                        )
                    ),
                    variant="ghost",
                    size="2"
                ),
                style={
                    "background": "rgba(255, 255, 255, 0.02)",
                    "border": f"1px solid {PAGOS_COLORS['border']}",
                    "border_radius": RADIUS["lg"],
                    "padding": SPACING["2"],
                    "max_height": "400px",
                    "overflow_y": "auto"
                }
            ),
            rx.center(
                rx.text(
                    "No hay pagos registrados",
                    size="3",
                    color=PAGOS_COLORS["text_secondary"]
                ),
                padding="8"
            )
        ),

        spacing="4",
        width="100%"
    )

def fila_historial_pago(pago) -> rx.Component:
    """📋 Fila individual del historial"""
    return rx.table.row(
        rx.table.cell(
            rx.text(
                pago["numero_recibo"],
                size="2",
                weight="medium",
                color=PAGOS_COLORS["primary"]
            )
        ),
        rx.table.cell(
            rx.text(
                pago["paciente_nombre"],
                size="2",
                color=PAGOS_COLORS["text_primary"]
            )
        ),
        rx.table.cell(
            rx.text(
                pago["concepto"],
                size="2",
                color=PAGOS_COLORS["text_secondary"]
            )
        ),
        rx.table.cell(
            rx.text(
                f"${pago['monto_pagado_usd']:.2f}",
                size="2",
                weight="medium",
                color=PAGOS_COLORS["success"]
            )
        ),
        rx.table.cell(
            rx.text(
                f"{pago['monto_pagado_bs']:,.0f}",
                size="2",
                weight="medium",
                color=PAGOS_COLORS["success"]
            )
        ),
        rx.table.cell(
            rx.badge(
                pago["estado_pago"],
                color_scheme=rx.cond(
                    pago["estado_pago"] == "completado",
                    "green",
                    rx.cond(
                        pago["estado_pago"] == "pendiente",
                        "yellow",
                        "gray"
                    )
                ),
                size="1"
            )
        ),
        rx.table.cell(
            rx.text(
                pago["fecha_pago"],
                size="2",
                color=PAGOS_COLORS["text_secondary"]
            )
        ),
    )

# ==========================================
# 🧮 CALCULADORA DE CONVERSIÓN USD/BS
# ==========================================

def modal_calculadora_conversion() -> rx.Component:
    """🧮 Modal de calculadora de conversión USD/BS"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(""),  # Botón invisible, se activa por AppState
            style={"display": "none"}
        ),
        rx.dialog.content(
            rx.vstack(
                # Header de la calculadora
                rx.hstack(
                    rx.icon("calculator", size=24, color=PAGOS_COLORS["primary"]),
                    rx.heading(
                        "Calculadora USD ⇄ BS",
                        size="6",
                        weight="bold",
                        style={
                            "background": GRADIENTS["text_gradient_primary"],
                            "background_clip": "text",
                            "color": "transparent"
                        }
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            size="3",
                            on_click=AppState.alternar_calculadora_conversion
                        )
                    ),
                    width="100%",
                    align_items="center"
                ),

                # Tasa del día
                rx.box(
                    rx.hstack(
                        rx.icon("trending-up", size=16, color=PAGOS_COLORS["success"]),
                        rx.text(
                            "Tasa del día:",
                            size="3",
                            weight="medium",
                            color=PAGOS_COLORS["text_primary"]
                        ),
                        rx.text(
                            f"1 USD = {AppState.tasa_del_dia} BS",
                            size="3",
                            weight="bold",
                            color=PAGOS_COLORS["success"]
                        ),
                        spacing="2",
                        align_items="center"
                    ),
                    style={
                        **pagos_card_style(),
                        "padding": SPACING["3"],
                        "background": "rgba(34, 197, 94, 0.1)",
                        "border": f"1px solid {PAGOS_COLORS['success']}40"
                    }
                ),

                # Convertidor USD → BS
                rx.vstack(
                    rx.text(
                        "💵 USD → BS",
                        size="4",
                        weight="bold",
                        color=PAGOS_COLORS["primary"]
                    ),
                    rx.input(
                        placeholder="Ingrese monto en USD...",
                        value=AppState.monto_calculadora_usd,
                        on_change=AppState.calcular_conversion_usd_a_bs,
                        type="number",
                        min="0",
                        step="0.01",
                        style={
                            "width": "100%",
                            "padding": SPACING["3"],
                            "background": DARK_THEME["colors"]["surface_secondary"],
                            "border": f"2px solid {PAGOS_COLORS['primary']}40",
                            "border_radius": RADIUS["md"],
                            "color": PAGOS_COLORS["text_primary"],
                            "font_size": "1.1rem",
                            "font_weight": "500",
                            "_focus": {
                                "border_color": PAGOS_COLORS["primary"],
                                "box_shadow": f"0 0 0 3px {PAGOS_COLORS['primary']}20"
                            }
                        }
                    ),
                    rx.hstack(
                        rx.icon("arrow-down", size=20, color=PAGOS_COLORS["primary"]),
                        rx.text("=", size="5", weight="bold", color=PAGOS_COLORS["primary"]),
                        spacing="2"
                    ),
                    rx.box(
                        rx.text(
                            f"{AppState.monto_calculadora_bs} BS",
                            size="5",
                            weight="bold",
                            color=PAGOS_COLORS["success"]
                        ),
                        style={
                            "padding": SPACING["3"],
                            "background": "rgba(34, 197, 94, 0.1)",
                            "border": f"2px solid {PAGOS_COLORS['success']}60",
                            "border_radius": RADIUS["md"],
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
                    rx.text(
                        "💰 BS → USD",
                        size="4",
                        weight="bold",
                        color=PAGOS_COLORS["secondary"]
                    ),
                    rx.input(
                        placeholder="Ingrese monto en BS...",
                        value=AppState.monto_calculadora_bs,
                        on_change=AppState.calcular_conversion_bs_a_usd,
                        type="number",
                        min="0",
                        step="0.01",
                        style={
                            "width": "100%",
                            "padding": SPACING["3"],
                            "background": DARK_THEME["colors"]["surface_secondary"],
                            "border": f"2px solid {PAGOS_COLORS['secondary']}40",
                            "border_radius": RADIUS["md"],
                            "color": PAGOS_COLORS["text_primary"],
                            "font_size": "1.1rem",
                            "font_weight": "500",
                            "_focus": {
                                "border_color": PAGOS_COLORS["secondary"],
                                "box_shadow": f"0 0 0 3px {PAGOS_COLORS['secondary']}20"
                            }
                        }
                    ),
                    rx.hstack(
                        rx.icon("arrow-down", size=20, color=PAGOS_COLORS["secondary"]),
                        rx.text("=", size="5", weight="bold", color=PAGOS_COLORS["secondary"]),
                        spacing="2"
                    ),
                    rx.box(
                        rx.text(
                            f"${AppState.monto_calculadora_usd} USD",
                            size="5",
                            weight="bold",
                            color=PAGOS_COLORS["primary"]
                        ),
                        style={
                            "padding": SPACING["3"],
                            "background": "rgba(6, 182, 212, 0.1)",
                            "border": f"2px solid {PAGOS_COLORS['primary']}60",
                            "border_radius": RADIUS["md"],
                            "text_align": "center",
                            "width": "100%"
                        }
                    ),
                    spacing="3",
                    width="100%"
                ),

                # Botones de acción rápida
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("rotate-ccw", size=16),
                            rx.text("Limpiar", size="2"),
                            spacing="2"
                        ),
                        on_click=AppState.limpiar_calculadora,
                        variant="outline",
                        color_scheme="gray",
                        size="2"
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.hstack(
                                rx.icon("check", size=16),
                                rx.text("Cerrar", size="2"),
                                spacing="2"
                            ),
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
                **dark_crystal_card(),
                "max_width": "450px",
                "padding": SPACING["6"],
                "background": DARK_THEME["colors"]["surface_primary"],
                "border": f"1px solid {PAGOS_COLORS['border']}",
                "backdrop_filter": "blur(12px)"
            }
        ),
        open=AppState.calculadora_activa
    )

# ==========================================
# 📱 PÁGINA PRINCIPAL
# ==========================================

def pagos_page() -> rx.Component:
    """💳 Página principal de gestión de pagos"""
    return medical_page_layout(
        rx.vstack(
            # Header de la página
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            "💳 Gestión de Pagos",
                            size="8",
                            weight="bold",
                            style={
                                "background": GRADIENTS["text_gradient_primary"],
                                "background_clip": "text",
                                "color": "transparent"
                            }
                        ),
                        rx.text(
                            "Sistema dual USD/BS para facturación y control de pagos",
                            size="4",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.icon("refresh-cw", size=16),
                                rx.text("Actualizar Todo", size="2"),
                                spacing="2"
                            ),
                            on_click=lambda: [
                                AppState.cargar_consultas_pendientes_pago(),
                                AppState.cargar_lista_pagos(),
                                AppState.cargar_estadisticas_duales()
                            ],
                            variant="outline",
                            color_scheme="cyan",
                            size="2"
                        ),
                        spacing="2"
                    ),
                    width="100%",
                    align_items="center"
                ),
                style=dark_header_style(),
                width="100%"
            ),

            # Estadísticas financieras
            estadisticas_financieras(),

            # Layout principal en 2 columnas
            rx.grid(
                # Columna izquierda: Consultas pendientes + Formulario
                rx.vstack(
                    consultas_pendientes_lista(),
                    formulario_pago_dual(),
                    spacing="6",
                    width="100%"
                ),

                # Columna derecha: Historial de pagos
                rx.vstack(
                    historial_pagos(),
                    spacing="6",
                    width="100%"
                ),

                columns="2",
                spacing="6",
                width="100%"
            ),

            spacing="6",
            width="100%",
            padding="4"
            # on_mount eliminado: datos se cargan en post_login_inicializacion()
        )
    )