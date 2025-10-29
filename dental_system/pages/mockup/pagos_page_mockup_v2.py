"""
💳 PÁGINA DE PAGOS - VERSIÓN MOCKUP COMPLETA
=============================================

UI completa con datos estáticos para diseño y validación visual
Todos los componentes usan datos mock realistas

CARACTERÍSTICAS:
- Layout de 2 columnas responsive
- Estadísticas financieras en tiempo real
- Lista de consultas pendientes con detalles expandibles
- Formulario de pago dual USD/BS interactivo
- Historial de pagos con búsqueda y filtros
- Calculadora de conversión
- Estados visuales (loading, error, success)
- Badges de estado y prioridad

PARA MIGRAR A DATOS REALES:
Solo cambiar imports de mock_data por AppState
"""

import reflex as rx
from .mock_data_pagos import (
    CONSULTAS_PENDIENTES_MOCK,
    PAGOS_HISTORIAL_MOCK,
    ESTADISTICAS_DIA_MOCK,
    FORMULARIO_PAGO_MOCK,
    METODOS_PAGO_DISPONIBLES
)
from .pagos_mockup_state import PagosMockupState
from dental_system.components.common import sidebar
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

# ==========================================
# 📊 COMPONENTE: ESTADÍSTICAS SUPERIORES
# ==========================================

def estadisticas_financieras_mockup() -> rx.Component:
    """Cards de estadísticas financieras del día"""
    stats = ESTADISTICAS_DIA_MOCK

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
                        str(stats["consultas_pendientes_pago"]),
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
                        f"${stats['recaudacion_usd_hoy']:.2f}",
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
                        f"{stats['recaudacion_bs_hoy']:,.0f}",
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
                            f"{stats['tasa_del_dia']:.2f}",
                            size="8",
                            weight="bold",
                            color=COLORS["primary"]
                        ),
                        rx.button(
                            rx.icon("edit", size=14),
                            size="1",
                            variant="soft",
                            color_scheme="cyan"
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
                }
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

def consultas_pendientes_lista_mockup() -> rx.Component:
    """Lista de consultas pendientes de facturación - MEJORADO"""
    return rx.vstack(
        # Header simplificado y más elegante
        rx.hstack(
            rx.badge(
                rx.hstack(
                    rx.icon("clipboard-list", size=16),
                    rx.text(f"{len(CONSULTAS_PENDIENTES_MOCK)} Pendientes", size="2"),
                    spacing="2"
                ),
                variant="soft",
                color_scheme="blue",
                radius="full"
            ),
            rx.spacer(),
            rx.button(
                rx.icon("filter", size=14),
                "Filtrar",
                size="1",
                variant="ghost",
                color_scheme="gray"
            ),
            width="100%",
            align="center"
        ),

        # Lista de consultas con mejor scroll
        rx.box(
            rx.vstack(
                *[consulta_card_mockup(c) for c in CONSULTAS_PENDIENTES_MOCK],
                spacing="3",
                width="100%"
            ),
            style={
                "max_height": "calc(100vh - 350px)",  # Más espacio
                "overflow_y": "auto",
                "padding_right": "4px",
                # Scrollbar mejorada
                "::-webkit-scrollbar": {
                    "width": "6px"
                },
                "::-webkit-scrollbar-track": {
                    "background": "transparent"
                },
                "::-webkit-scrollbar-thumb": {
                    "background": COLORS["border"],
                    "border_radius": "3px"
                },
                "::-webkit-scrollbar-thumb:hover": {
                    "background": COLORS["primary"]
                }
            }
        ),

        spacing="3",  # Menos espaciado
        width="100%"
    )
    
def consulta_card_mockup(consulta: dict) -> rx.Component:
    """Card individual de consulta pendiente - ARQUITECTURA MEJORADA"""
    
    # Sistema de prioridad mejorado
    PRIORITY_CONFIG = {
        "alta": {"color": COLORS["error"], "icon": "alert-triangle", "scheme": "red"},
        "media": {"color": COLORS["warning"], "icon": "alert-circle", "scheme": "yellow"},
        "baja": {"color": COLORS["success"], "icon": "info", "scheme": "green"}
    }
    
    config = PRIORITY_CONFIG.get(consulta["prioridad"], PRIORITY_CONFIG["media"])
    
    # Badge de días mejorado
    days_config = (
        {"scheme": "red", "label": f"{consulta['dias_pendiente']} días"} 
        if consulta["dias_pendiente"] > 3 else
        {"scheme": "yellow", "label": f"{consulta['dias_pendiente']} días"} 
        if consulta["dias_pendiente"] > 0 else
        {"scheme": "blue", "label": "Hoy", "icon": "clock"}
    )

    return rx.box(
        rx.vstack(
            # 🔄 Fila 1: Header compacto
            rx.hstack(
                # Avatar y info principal
                rx.hstack(
                    rx.box(
                        rx.text(
                            consulta["numero_consulta"].split()[-1],  # Solo el número
                            size="1",
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
                    rx.vstack(
                        rx.text(
                            consulta["paciente_nombre"],
                            size="3",
                            weight="bold",
                            truncate=True
                        ),
                        rx.text(
                            f"CI: {consulta['paciente_documento']}",
                            size="1",
                            color=COLORS["text_secondary"]
                        ),
                        spacing="0",
                        align="start"
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.spacer(),
                
                # Badges de estado
                rx.hstack(
                    rx.badge(
                        rx.hstack(
                            rx.icon(days_config.get("icon", "alert-circle"), size=10),
                            rx.text(days_config["label"], size="1"),
                            spacing="1"
                        ),
                        color_scheme=days_config["scheme"],
                        size="1",
                        variant="soft"
                    ),
                    spacing="1"
                ),
                width="100%",
                align="center"
            ),

            # 🔄 Fila 2: Meta información compacta
            rx.hstack(
                rx.hstack(
                    rx.icon("user", size=12, color=COLORS["text_secondary"]),
                    rx.text(
                        consulta["odontologo_nombre"].split()[0],  # Solo primer nombre
                        size="1",
                        color=COLORS["text_secondary"]
                    ),
                    spacing="1"
                ),
                rx.box(
                    style={
                        "width": "1px",
                        "height": "12px",
                        "background": COLORS["border"]
                    }
                ),
                rx.hstack(
                    rx.icon("stethoscope", size=12, color=COLORS["text_secondary"]),
                    rx.text(
                        f"{consulta['servicios_count']} serv.",
                        size="1",
                        color=COLORS["text_secondary"]
                    ),
                    spacing="1"
                ),
                spacing="2",
                width="100%",
                justify="start"
            ),

            # 🔄 Fila 3: Servicios con accordion mejorado
            rx.accordion.root(
                rx.accordion.item(
                    header=rx.hstack(
                        rx.icon("list", size=12, color=COLORS["primary"]),
                        rx.text(
                            f"Ver {len(consulta['servicios_realizados'])} servicios", 
                            size="1", 
                            color=COLORS["primary"]
                        ),
                        rx.spacer(),
                        rx.accordion.trigger(
                            rx.icon("chevron-down", size=12),
                            style={"transition": "transform 0.2s"}
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    content=rx.box(
                        rx.vstack(
                            *[
                                rx.hstack(
                                    rx.box(
                                        style={
                                            "width": "4px",
                                            "height": "4px",
                                            "background": COLORS["primary"],
                                            "border_radius": "50%"
                                        }
                                    ),
                                    rx.text(
                                        srv["nombre"],
                                        size="1",
                                        flex="1",
                                        truncate=True
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            f"${srv['precio_usd']:.2f}",
                                            size="1",
                                            weight="bold",
                                            color=COLORS["success"]
                                        ),
                                        rx.text(
                                            "|",
                                            size="1",
                                            color=COLORS["border"]
                                        ),
                                        rx.text(
                                            f"{srv['precio_bs']:,.0f} BS",
                                            size="1",
                                            color=COLORS["text_secondary"]
                                        ),
                                        spacing="1"
                                    ),
                                    spacing="2",
                                    width="100%",
                                    align="center"
                                )
                                for srv in consulta["servicios_realizados"]
                            ],
                            spacing="2",
                            width="100%"
                        ),
                        style={
                            "background": "rgba(0, 188, 212, 0.03)",
                            "border_left": f"2px solid {COLORS['primary']}30",
                            "padding": "8px 12px",
                            "border_radius": "6px",
                            "margin_top": "6px"
                        }
                    ),
                    value="servicios"
                ),
                collapsible=True,
                width="100%",
                variant="ghost",
                style={"font_size": "12px"}
            ),

            # 🔄 Fila 4: Totales y acción - COMPACTADO
            rx.hstack(
                # Totales compactos
                rx.vstack(
                    rx.text(
                        "TOTAL A PAGAR",
                        size="1",
                        color=COLORS["text_secondary"],
                        weight="bold"
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                f"${consulta['total_usd']:.2f}",
                                size="3",
                                weight="bold",
                                color=COLORS["success"]
                            ),
                            rx.text("USD", size="1", color=COLORS["text_secondary"]),
                            spacing="0",
                            align="start"
                        ),
                        rx.box(
                            style={
                                "width": "1px",
                                "height": "20px",
                                "background": COLORS["border"]
                            }
                        ),
                        rx.vstack(
                            rx.text(
                                f"{consulta['total_bs']:,.0f}",
                                size="3",
                                weight="bold",
                                color=COLORS["success"]
                            ),
                            rx.text("BS", size="1", color=COLORS["text_secondary"]),
                            spacing="0",
                            align="start"
                        ),
                        spacing="2",
                        align="center"
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.spacer(),
                
                # Botón mejorado
                rx.button(
                    rx.hstack(
                        rx.icon("credit-card", size=14),
                        rx.text("FACTURAR", size="1", weight="bold"),
                        spacing="1"
                    ),
                    on_click=lambda: PagosMockupState.abrir_modal_pago(consulta),
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

            spacing="2",  # Menor espaciado interno
            width="100%"
        ),
        style={
            "background": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "border_radius": "8px",  # Border radius más pequeño
            "padding": "12px",  # Padding reducido
            "transition": "all 0.2s ease",
            "border_left": f"3px solid {config['color']}",
            "_hover": {
                "background": COLORS["surface_hover"],
                "border_color": COLORS["primary"] + "50",
                "box_shadow": f"0 2px 8px {COLORS['primary']}15"
            }
        },
        width="100%"
    )
# ==========================================
# 📋 COMPONENTE: HISTORIAL DE PAGOS
# ==========================================

def historial_pagos_mockup() -> rx.Component:
    """Historial de pagos procesados"""
    return rx.vstack(
        # Header con búsqueda
        rx.hstack(
            rx.hstack(
                rx.icon("receipt", size=24, color=COLORS["primary"]),
                rx.heading(
                    "Historial de Pagos",
                    size="4",
                    color=COLORS["text_primary"],
                    weight="bold"
                ),
                spacing="3"
            ),
            rx.spacer(),
            rx.input(
                placeholder="Buscar por paciente o recibo...",
                size="2",
                width=["200px", "200px", "250px", "300px"],  # Responsive
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
            align="center"
        ),

        # Tabla de historial
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Recibo", style={"color": COLORS["text_secondary"]}),
                        rx.table.column_header_cell("Paciente", style={"color": COLORS["text_secondary"]}),
                        rx.table.column_header_cell("Concepto", style={"color": COLORS["text_secondary"]}),
                        rx.table.column_header_cell("USD", style={"color": COLORS["text_secondary"]}),
                        rx.table.column_header_cell("BS", style={"color": COLORS["text_secondary"]}),
                        rx.table.column_header_cell("Estado", style={"color": COLORS["text_secondary"]}),
                        rx.table.column_header_cell("Fecha", style={"color": COLORS["text_secondary"]}),
                        rx.table.column_header_cell("", style={"width": "50px"}),
                    )
                ),
                rx.table.body(
                    *[fila_pago_mockup(pago) for pago in PAGOS_HISTORIAL_MOCK]
                ),
                variant="ghost",
                size="2",
                width="100%"
            ),
            style={
                "background": "rgba(255, 255, 255, 0.02)",
                "border": f"1px solid {COLORS['border']}",
                "border_radius": "12px",
                "padding": "12px",
                "max_height": "calc(100vh - 400px)",
                "overflow_y": "auto",
                # Scrollbar custom
                "::-webkit-scrollbar": {
                    "width": "8px"
                },
                "::-webkit-scrollbar-track": {
                    "background": COLORS["surface"]
                },
                "::-webkit-scrollbar-thumb": {
                    "background": COLORS["border"],
                    "border_radius": "4px"
                },
                "::-webkit-scrollbar-thumb:hover": {
                    "background": COLORS["primary"]
                }
            }
        ),

        spacing="4",
        width="100%"
    )

def fila_pago_mockup(pago: dict) -> rx.Component:
    """Fila individual del historial de pagos"""

    # Determinar tipo de pago
    if pago["monto_pagado_usd"] > 0 and pago["monto_pagado_bs"] > 0:
        tipo_pago = "mixto"
    elif pago["monto_pagado_usd"] > 0:
        tipo_pago = "usd"
    else:
        tipo_pago = "bs"

    return rx.table.row(
        # Número de recibo
        rx.table.cell(
            rx.text(
                pago["numero_recibo"],
                size="2",
                weight="bold",
                color=COLORS["primary"]
            )
        ),

        # Paciente
        rx.table.cell(
            rx.vstack(
                rx.text(pago["paciente_nombre"], size="2", weight="medium"),
                rx.text(pago["paciente_documento"], size="1", color=COLORS["text_secondary"]),
                spacing="0",
                align="start"
            )
        ),

        # Concepto
        rx.table.cell(
            rx.text(pago["concepto"], size="2", color=COLORS["text_secondary"])
        ),

        # Monto USD
        rx.table.cell(
            rx.text(
                f"${pago['monto_pagado_usd']:.2f}" if pago["monto_pagado_usd"] > 0 else "-",
                size="2",
                weight="bold",
                color=COLORS["success"] if pago["monto_pagado_usd"] > 0 else COLORS["text_secondary"]
            )
        ),

        # Monto BS
        rx.table.cell(
            rx.text(
                f"{pago['monto_pagado_bs']:,.0f}" if pago["monto_pagado_bs"] > 0 else "-",
                size="2",
                weight="bold",
                color=COLORS["success"] if pago["monto_pagado_bs"] > 0 else COLORS["text_secondary"]
            )
        ),

        # Estado
        rx.table.cell(
            rx.badge(
                pago["estado_pago"].upper(),
                color_scheme="green" if pago["estado_pago"] == "completado" else "yellow",
                variant="solid"
            )
        ),

        # Fecha
        rx.table.cell(
            rx.text(
                pago["fecha_pago"][:10],
                size="2",
                color=COLORS["text_secondary"]
            )
        ),

        # Acciones
        rx.table.cell(
            rx.button(
                rx.icon("eye", size=14),
                variant="ghost",
                color_scheme="cyan",
                size="1"
            )
        ),

        style={
            "_hover": {
                "background": COLORS["surface"]
            }
        }
    )

# ==========================================
# 💳 MODAL DE PAGO INTERACTIVO
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
                        rx.icon("x", size=20, style={"cursor": "pointer"})
                    ),
                    width="100%",
                    align="center"
                ),
                rx.divider(),

                # Info consulta
                rx.cond(
                    PagosMockupState.consulta_seleccionada,
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Consulta:", size="2", color=COLORS["text_secondary"]),
                                rx.text(PagosMockupState.consulta_seleccionada["numero_consulta"], size="2", weight="bold"),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.text("Paciente:", size="2", color=COLORS["text_secondary"]),
                                rx.text(PagosMockupState.consulta_seleccionada["paciente_nombre"], size="2", weight="bold"),
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
                        rx.text(f"${PagosMockupState.total_usd_calculado:.2f}", size="5", weight="bold", color=COLORS["success"]),
                        spacing="1",
                        align="center",
                        style={"background": f"{COLORS['success']}15", "padding": "12px", "border_radius": "8px"}
                    ),
                    rx.vstack(
                        rx.text(f"Total BS (x{PagosMockupState.tasa_cambio})", size="2", color=COLORS["text_secondary"]),
                        rx.text(f"Bs. {PagosMockupState.total_bs_calculado:,.0f}", size="5", weight="bold", color=COLORS["primary"]),
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
                            value=PagosMockupState.monto_usd,
                            on_change=PagosMockupState.set_monto_usd,
                            type="number",
                            size="3"
                        ),
                        rx.select(
                            METODOS_PAGO_DISPONIBLES,
                            placeholder="Método de pago",
                            value=PagosMockupState.metodo_pago_usd,
                            on_change=PagosMockupState.set_metodo_pago_usd,
                            size="2"
                        ),
                        rx.input(
                            placeholder="Referencia (opcional)",
                            value=PagosMockupState.referencia_usd,
                            on_change=PagosMockupState.set_referencia_usd,
                            size="2"
                        ),
                        rx.cond(
                            PagosMockupState.errores.get("metodo_usd"),
                            rx.text(PagosMockupState.errores["metodo_usd"], size="1", color=COLORS["error"])
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
                            value=PagosMockupState.monto_bs,
                            on_change=PagosMockupState.set_monto_bs,
                            type="number",
                            size="3"
                        ),
                        rx.select(
                            METODOS_PAGO_DISPONIBLES,
                            placeholder="Método de pago",
                            value=PagosMockupState.metodo_pago_bs,
                            on_change=PagosMockupState.set_metodo_pago_bs,
                            size="2"
                        ),
                        rx.input(
                            placeholder="Referencia (opcional)",
                            value=PagosMockupState.referencia_bs,
                            on_change=PagosMockupState.set_referencia_bs,
                            size="2"
                        ),
                        rx.cond(
                            PagosMockupState.errores.get("metodo_bs"),
                            rx.text(PagosMockupState.errores["metodo_bs"], size="1", color=COLORS["error"])
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    style={"background": f"{COLORS['primary']}10", "padding": "12px", "border_radius": "8px"}
                ),

                # Auto-cálculos
                rx.cond(
                    PagosMockupState.monto_usd_float > 0,
                    rx.text(f"${PagosMockupState.monto_usd_float:.2f} USD = Bs. {PagosMockupState.equivalente_bs_de_usd:,.2f}", size="2", color=COLORS["text_secondary"])
                ),
                rx.cond(
                    PagosMockupState.monto_bs_float > 0,
                    rx.text(f"Bs. {PagosMockupState.monto_bs_float:,.2f} = ${PagosMockupState.equivalente_usd_de_bs:.2f} USD", size="2", color=COLORS["text_secondary"])
                ),

                # Descuento opcional
                rx.box(
                    rx.vstack(
                        rx.checkbox(
                            "Aplicar descuento",
                            checked=PagosMockupState.aplicar_descuento,
                            on_change=PagosMockupState.set_aplicar_descuento
                        ),
                        rx.cond(
                            PagosMockupState.aplicar_descuento,
                            rx.vstack(
                                rx.input(
                                    placeholder="Monto descuento USD",
                                    value=PagosMockupState.descuento_usd,
                                    on_change=PagosMockupState.set_descuento_usd,
                                    type="number",
                                    size="2"
                                ),
                                rx.input(
                                    placeholder="Motivo",
                                    value=PagosMockupState.motivo_descuento,
                                    on_change=PagosMockupState.set_motivo_descuento,
                                    size="2"
                                ),
                                spacing="2",
                                width="100%"
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
                    value=PagosMockupState.notas,
                    on_change=PagosMockupState.set_notas,
                    rows="2",
                    size="2"
                ),

                # Resumen
                rx.box(
                    rx.vstack(
                        rx.text("Resumen del Pago", size="3", weight="bold"),
                        rx.divider(),
                        rx.hstack(
                            rx.text("Total a pagar:", size="2"),
                            rx.spacer(),
                            rx.text(f"${PagosMockupState.total_usd_calculado:.2f}", size="2", weight="bold"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Pagando:", size="2", color=COLORS["success"]),
                            rx.spacer(),
                            rx.text(f"${PagosMockupState.total_pagado_usd:.2f}", size="2", weight="bold", color=COLORS["success"]),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Saldo pendiente:", size="2", color=COLORS["warning"]),
                            rx.spacer(),
                            rx.text(f"${PagosMockupState.saldo_pendiente_usd:.2f}", size="2", weight="bold", color=COLORS["warning"]),
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
                    PagosMockupState.errores.get("monto"),
                    rx.callout(
                        PagosMockupState.errores["monto"],
                        icon="alert-circle",
                        color_scheme="red",
                        size="1"
                    )
                ),

                # Botones
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", color_scheme="gray", size="3")
                    ),
                    rx.button(
                        "PROCESAR PAGO",
                        on_click=PagosMockupState.validar_y_procesar_pago,
                        disabled=~PagosMockupState.formulario_valido | PagosMockupState.procesando,
                        loading=PagosMockupState.procesando,
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
        open=PagosMockupState.modal_pago_abierto,
        on_open_change=PagosMockupState.set_modal_pago_abierto
    )

# ==========================================
# 📱 PÁGINA PRINCIPAL MOCKUP
# ==========================================

@rx.page(route="/pagos-mockup-v2", title="Módulo de Pagos - Mockup")
def pagos_mockup_v2_page() -> rx.Component:
    """Página completa de pagos con datos mockup"""
    return rx.box(
        rx.hstack(
            sidebar(),
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
                    rx.box(
                        rx.badge(
                            rx.hstack(
                                rx.icon("palette", size=16),
                                rx.text("MOCKUP UI/UX", size="2", weight="bold"),
                                spacing="2"
                            ),
                            size="2",
                            color_scheme="purple",
                            variant="solid",
                            radius="full",
                            padding_x="12px"
                        ),
                        align_self="start"
                    ),
                    
                    width="100%",
                    align="center",
                    spacing="4"
                ), 
                

                # Estadísticas superiores
                estadisticas_financieras_mockup(),

                # Layout principal en 2 columnas
                rx.grid(
                    # Columna izquierda: Consultas pendientes
                    rx.box(
                        consultas_pendientes_lista_mockup(),
                        style={
                            "background": "rgba(255, 255, 255, 0.02)",
                            "border": f"1px solid {COLORS['border']}",
                            "border_radius": "12px",
                            "padding": "20px",
                            "height": "fit-content",
                            "min_height": "500px"  # Altura mínima consistente
                        }
                    ),

                    # Columna derecha: Historial de pagos
                    rx.box(
                        historial_pagos_mockup(),
                         style={
                            "background": "rgba(255, 255, 255, 0.02)",
                            "border": f"1px solid {COLORS['border']}",
                            "border_radius": "12px",
                            "padding": "20px",
                            "min_height": "500px"
                            
                        }
                    ),
                    columns=rx.breakpoints(
                        initial="1",
                        md="1", 
                        lg="1fr 2fr",  # 40% / 60% más preciso
                        xl="1fr 2fr"
                    ),
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
        modal_pago_dual(),  # Modal interactivo
        style={
            "background": COLORS["bg_gradient"],
            "min_height": "100vh",
            "color": COLORS["text_primary"]
        }
    )
