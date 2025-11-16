"""
💳 MODAL DE FACTURA PROFESIONAL V2.0 - REDISEÑADO
===================================================

✨ Versión mejorada con:
- Diseño compacto y limpio
- Componentes genéricos (enhanced_form_field, form_section_header)
- Consistencia con otros modales (consulta, paciente)
- UX/UI optimizada para reducir espacio visual
- Sistema dual USD/BS simplificado

"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.constants import METODOS_PAGO
from dental_system.components.forms import form_section_header, enhanced_form_field
from dental_system.styles.themes import (
    COLORS, SHADOWS, RADIUS, SPACING, ANIMATIONS,
    GRADIENTS, GLASS_EFFECTS, DARK_THEME
)

def seccion_datos_paciente_consulta() -> rx.Component:
    """📋 Sección compacta de datos del paciente y consulta"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("user", size=20, color=COLORS["primary"]["400"]),
            rx.text(
                "Información del Paciente",
                style={
                    "font_size": "1rem",
                    "font_weight": "700",
                    "color": DARK_THEME["colors"]["text_primary"]
                }
            ),
            spacing="2",
            align="center"
        ),

        # Grid compacto de datos
        rx.grid(
            # Nombre completo (ocupa 2 columnas)
            rx.vstack(
                rx.text("Paciente", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                rx.text(
                    AppState.consulta_pagar.paciente_nombre,
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="1",
                align="start",
                style={"grid_column": "span 2"}
            ),

            # HC
            rx.vstack(
                rx.text("HC", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                rx.text(
                    AppState.consulta_pagar.paciente_numero_historia,
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="1",
                align="start"
            ),

            # CI
            rx.vstack(
                rx.text("Documento", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                rx.text(
                    AppState.consulta_pagar.paciente_documento,
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="1",
                align="start"
            ),

            # Teléfono
            rx.vstack(
                rx.text("Teléfono", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                rx.text(
                    AppState.consulta_pagar.paciente_telefono,
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="1",
                align="start"
            ),

            # N° Consulta
            rx.vstack(
                rx.text("N° Consulta", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                rx.text(
                    AppState.consulta_pagar.numero_consulta,
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "600",
                        "color": COLORS["primary"]["400"]
                    }
                ),
                spacing="1",
                align="start"
            ),

            columns="3",
            spacing="4",
            width="100%"
        ),

        spacing="3",
        style={
            "background": DARK_THEME["colors"]["surface_secondary"],
            "border": f"1px solid {DARK_THEME['colors']['border']}",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "width": "100%"
        }
    )


def tabla_servicios_factura() -> rx.Component:
    """📄 Lista compacta de servicios realizados"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("clipboard-list", size=20, color=COLORS["secondary"]["500"]),
            rx.text(
                "Servicios Realizados",
                style={
                    "font_size": "1rem",
                    "font_weight": "700",
                    "color": DARK_THEME["colors"]["text_primary"]
                }
            ),
            spacing="2",
            align="center"
        ),

        # Lista de servicios
        rx.cond(
            AppState.consulta_pagar.servicios_formateados.length() > 0,
            rx.vstack(
                rx.foreach(
                    AppState.consulta_pagar.servicios_formateados,
                    lambda servicio: rx.hstack(
                        # Servicio y odontólogo
                        rx.vstack(
                            rx.text(
                                servicio.nombre,
                                style={
                                    "font_size": "0.9rem",
                                    "font_weight": "600",
                                    "color": DARK_THEME["colors"]["text_primary"]
                                }
                            ),
                            rx.hstack(
                                rx.icon("user-round", size=12, color=COLORS["gray"]["500"]),
                                rx.text(
                                    servicio.odontologo,
                                    size="1",
                                    color=DARK_THEME["colors"]["text_secondary"]
                                ),
                                spacing="1",
                                align="center"
                            ),
                            spacing="1",
                            align="start",
                            style={"flex": "1"}
                        ),

                        # Precios
                        rx.hstack(
                            rx.text(
                                f"${servicio.precio_usd}",
                                style={
                                    "font_size": "0.9rem",
                                    "font_weight": "600",
                                    "color": COLORS["success"]["400"]
                                }
                            ),
                            rx.text("|", size="2", color=COLORS["gray"]["500"]),
                            rx.text(
                                f"{servicio.precio_bs} Bs",
                                style={
                                    "font_size": "0.9rem",
                                    "font_weight": "600",
                                    "color": COLORS["primary"]["400"]
                                }
                            ),
                            spacing="2",
                            align="center"
                        ),

                        width="100%",
                        align="center",
                        justify="between",
                        style={
                            "padding": SPACING["3"],
                            "border_bottom": f"1px solid {DARK_THEME['colors']['border']}",
                            "_last": {"border_bottom": "none"}
                        }
                    )
                ),
                width="100%",
                spacing="0"
            ),
            # Mensaje si no hay servicios
            rx.box(
                rx.text(
                    "No hay servicios registrados",
                    size="2",
                    color=DARK_THEME["colors"]["text_secondary"],
                    style={"text_align": "center", "padding": SPACING["4"]}
                ),
                width="100%"
            )
        ),

        # Total destacado
        rx.hstack(
            rx.text("Total:", size="3", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            rx.spacer(),
            rx.hstack(
                rx.text(
                    f"${AppState.formulario_pago_dual.monto_total_usd:.2f}",
                    style={
                        "font_size": "1.1rem",
                        "font_weight": "700",
                        "color": COLORS["success"]["400"]
                    }
                ),
                rx.text("|", size="3", color=COLORS["gray"]["500"]),
                rx.text(
                    f"Bs. {AppState.formulario_pago_dual.monto_total_bs:,.0f}",
                    style={
                        "font_size": "1.1rem",
                        "font_weight": "700",
                        "color": COLORS["primary"]["400"]
                    }
                ),
                spacing="2",
                align="center"
            ),
            width="100%",
            align="center",
            style={
                "padding": SPACING["3"],
                "border_top": f"2px solid {DARK_THEME['colors']['border']}",
                "margin_top": SPACING["2"]
            }
        ),

        spacing="3",
        style={
            "background": DARK_THEME["colors"]["surface_secondary"],
            "border": f"1px solid {DARK_THEME['colors']['border']}",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "width": "100%"
        }
    )


def formulario_pago_dual() -> rx.Component:
    """💰 Formulario compacto de pago dual USD/BS usando enhanced_form_field"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("wallet", size=20, color=COLORS["success"]["400"]),
            rx.text(
                "Información de Pago",
                style={
                    "font_size": "1rem",
                    "font_weight": "700",
                    "color": DARK_THEME["colors"]["text_primary"]
                }
            ),
            spacing="2",
            align="center"
        ),

        # Grid de pagos USD y BS (2 columnas)
        rx.grid(
            # Columna USD
            rx.vstack(
                enhanced_form_field(
                    label="Monto USD",
                    field_name="monto_pagado_usd",
                    value=str(AppState.formulario_pago_dual.monto_pagado_usd),
                    on_change=AppState.actualizar_campo_pago_dual,
                    field_type="number",
                    placeholder="0.00",
                    icon="dollar-sign"
                ),
                enhanced_form_field(
                    label="Método",
                    field_name="metodo_pago_usd",
                    value=rx.cond(AppState.formulario_pago_dual.metodo_pago_usd != "", AppState.formulario_pago_dual.metodo_pago_usd, METODOS_PAGO[0] if len(METODOS_PAGO) > 0 else ""),
                    on_change=AppState.actualizar_campo_pago_dual,
                    field_type="select",
                    options=METODOS_PAGO,
                    placeholder="Seleccionar método",
                    icon="credit-card",
                    help_text="Predeterminado: primer método disponible"
                ),
                enhanced_form_field(
                    label="Referencia",
                    field_name="referencia_usd",
                    value=AppState.formulario_pago_dual.referencia_usd,
                    on_change=AppState.actualizar_campo_pago_dual,
                    placeholder="Opcional",
                    icon="hash"
                ),
                spacing="3",
                width="100%"
            ),

            # Columna BS
            rx.vstack(
                enhanced_form_field(
                    label="Monto BS",
                    field_name="monto_pagado_bs",
                    value=str(AppState.formulario_pago_dual.monto_pagado_bs),
                    on_change=AppState.actualizar_campo_pago_dual,
                    field_type="number",
                    placeholder="0.00",
                    icon="banknote"
                ),
                enhanced_form_field(
                    label="Método",
                    field_name="metodo_pago_bs",
                    value=rx.cond(AppState.formulario_pago_dual.metodo_pago_bs != "", AppState.formulario_pago_dual.metodo_pago_bs, METODOS_PAGO[0] if len(METODOS_PAGO) > 0 else ""),
                    on_change=AppState.actualizar_campo_pago_dual,
                    field_type="select",
                    options=METODOS_PAGO,
                    placeholder="Seleccionar método",
                    icon="credit-card",
                    help_text="Predeterminado: primer método disponible"
                ),
                enhanced_form_field(
                    label="Referencia",
                    field_name="referencia_bs",
                    value=AppState.formulario_pago_dual.referencia_bs,
                    on_change=AppState.actualizar_campo_pago_dual,
                    placeholder="Opcional",
                    icon="hash"
                ),
                spacing="3",
                width="100%"
            ),

            columns="2",
            spacing="4",
            width="100%"
        ),

        # Info de tasa de cambio (compacta)
        rx.hstack(
            rx.icon("info", size=14, color=COLORS["primary"]["400"]),
            rx.text(
                f"Tasa del día: 1 USD = {AppState.formulario_pago_dual.tasa_cambio} BS",
                size="1",
                color=DARK_THEME["colors"]["text_secondary"]
            ),
            spacing="2",
            align="center",
            style={
                "padding": SPACING["2"],
                "border_radius": RADIUS["md"],
                "background": f"{COLORS['primary']['400']}10",
                "border": f"1px solid {COLORS['primary']['400']}30"
            }
        ),

        # Descuento (compacto)
        rx.grid(
            enhanced_form_field(
                label="Descuento USD",
                field_name="descuento_usd",
                value=str(AppState.formulario_pago_dual.descuento_usd),
                on_change=AppState.actualizar_campo_pago_dual,
                field_type="number",
                placeholder="0.00",
                icon="tag",
                help_text="Opcional"
            ),
            rx.cond(
                AppState.formulario_pago_dual.descuento_usd > 0,
                enhanced_form_field(
                    label="Motivo del descuento",
                    field_name="motivo_descuento",
                    value=AppState.formulario_pago_dual.motivo_descuento,
                    on_change=AppState.actualizar_campo_pago_dual,
                    placeholder="Razón del descuento",
                    icon="message-square"
                ),
                rx.box()
            ),
            columns="2",
            spacing="4",
            width="100%"
        ),

        # Notas (compacto)
        enhanced_form_field(
            label="Observaciones",
            field_name="notas",
            value=AppState.formulario_pago_dual.notas,
            on_change=AppState.actualizar_campo_pago_dual,
            field_type="textarea",
            placeholder="Notas adicionales del pago...",
            icon="file-text",
            max_length=500
        ),

        spacing="4",
        width="100%"
    )


def resumen_pago() -> rx.Component:
    """📊 Resumen compacto del pago con cálculos"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("calculator", size=20, color=COLORS["success"]["400"]),
            rx.text(
                "Resumen del Pago",
                style={
                    "font_size": "1rem",
                    "font_weight": "700",
                    "color": DARK_THEME["colors"]["text_primary"]
                }
            ),
            spacing="2",
            align="center"
        ),

        # Líneas de resumen
        rx.vstack(
            # Total a pagar
            rx.hstack(
                rx.text("Total a pagar:", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                rx.spacer(),
                rx.text(
                    f"${AppState.formulario_pago_dual.monto_total_usd:.2f}",
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                width="100%",
                align="center"
            ),

            # Descuento (solo si existe)
            rx.cond(
                AppState.formulario_pago_dual.descuento_usd > 0,
                rx.hstack(
                    rx.text("Descuento:", size="2", color=COLORS["warning"]["400"]),
                    rx.spacer(),
                    rx.text(
                        f"-${AppState.formulario_pago_dual.descuento_usd:.2f}",
                        style={
                            "font_size": "0.9rem",
                            "font_weight": "600",
                            "color": COLORS["warning"]["400"]
                        }
                    ),
                    width="100%",
                    align="center"
                ),
                rx.box()
            ),

            # Pagando ahora
            rx.hstack(
                rx.text("Pagando ahora:", size="2", color=COLORS["success"]["400"]),
                rx.spacer(),
                rx.text(
                    f"${AppState.total_pagando_usd:.2f}",
                    style={
                        "font_size": "0.9rem",
                        "font_weight": "600",
                        "color": COLORS["success"]["400"]
                    }
                ),
                width="100%",
                align="center"
            ),

            spacing="2",
            width="100%"
        ),

        # Divider
        rx.box(
            style={
                "width": "100%",
                "height": "2px",
                "background": DARK_THEME["colors"]["border"]
            }
        ),

        # Saldo pendiente (destacado)
        rx.hstack(
            rx.hstack(
                rx.icon("alert-circle", size=18, color=COLORS["warning"]["400"]),
                rx.text(
                    "Saldo pendiente:",
                    style={
                        "font_size": "1rem",
                        "font_weight": "700",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="2",
                align="center"
            ),
            rx.spacer(),
            rx.text(
                f"${AppState.saldo_pendiente_calculado:.2f}",
                style={
                    "font_size": "1.1rem",
                    "font_weight": "700",
                    "color": rx.cond(
                        AppState.saldo_pendiente_calculado > 0,
                        COLORS["warning"]["400"],
                        COLORS["success"]["400"]
                    )
                }
            ),
            width="100%",
            align="center"
        ),

        spacing="3",
        style={
            "background": DARK_THEME["colors"]["surface_secondary"],
            "border": f"2px solid {COLORS['success']['400']}40",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "width": "100%"
        }
    )


def modal_factura_profesional() -> rx.Component:
    """
    💳 Modal Profesional de Facturación V2.0 - REDISEÑADO

    ✨ Características:
    - Diseño compacto y limpio
    - Componentes genéricos reutilizables
    - Sistema dual USD/BS simplificado
    - Consistencia con otros modales del sistema
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header mejorado
                rx.hstack(
                    form_section_header(
                        "Facturación de Consulta",
                        "Sistema Dual USD/BS",
                        "receipt",
                        COLORS["success"]["500"]
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

                # Secciones rediseñadas
                seccion_datos_paciente_consulta(),
                tabla_servicios_factura(),
                formulario_pago_dual(),
                resumen_pago(),

                # Errores de validación
                rx.cond(
                    AppState.errores_validacion_pago.get("general", "") != "",
                    rx.hstack(
                        rx.icon("alert-circle", size=16, color=COLORS["error"]["500"]),
                        rx.text(
                            AppState.errores_validacion_pago.get("general", ""),
                            size="2",
                            color=COLORS["error"]["500"]
                        ),
                        spacing="2",
                        style={
                            "padding": SPACING["3"],
                            "background": f"{COLORS['error']['500']}15",
                            "border": f"1px solid {COLORS['error']['500']}40",
                            "border_radius": RADIUS["md"],
                            "width": "100%"
                        }
                    )
                ),

                # Botones de acción
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
                            on_click=AppState.limpiar_formulario_pago_dual
                        )
                    ),

                    rx.spacer(),

                    rx.button(
                        rx.cond(
                            AppState.procesando_pago,
                            rx.hstack(
                                rx.spinner(size="3", color="white"),
                                rx.text("Procesando..."),
                                spacing="3",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Procesar Pago"),
                                rx.icon("check-circle", size=16),
                                spacing="2",
                                align="center"
                            )
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
                            },
                            "_disabled": {
                                "opacity": "0.6",
                                "cursor": "not-allowed",
                                "transform": "none"
                            }
                        },
                        on_click=AppState.crear_pago_dual,
                        disabled=AppState.procesando_pago
                    ),

                    spacing="3",
                    width="100%",
                    align="center"
                ),

                spacing="4",
                width="100%",
                align="stretch"
            ),

            style={
                "max_width": "700px",
                "padding": SPACING["4"],
                "border_radius": RADIUS["xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['primary']['200']}30",
                "overflow_y": "auto",
                "max_height": "90vh",
                "backdrop_filter": "blur(20px)"
            }
        ),
        open=AppState.modal_pago_dual_abierto,
        on_open_change=AppState.set_modal_pago_dual_abierto
    )


def estado_pago_badge(estado: str) -> rx.Component:
    """Badge de estado de pago con colores dinámicos"""
    return rx.badge(
        rx.hstack(
            rx.icon(
                rx.match(
                    estado,
                    ("completado", "check-circle"),
                    ("pendiente", "clock"),
                    ("anulado", "x-circle"),
                    "circle"
                ),
                size=14
            ),
            rx.text(
                rx.match(
                    estado,
                    ("completado", "Completado"),
                    ("pendiente", "Pendiente"),
                    ("anulado", "Anulado"),
                    estado.capitalize()
                ),
                weight="medium"
            ),
            spacing="2",
            align="center"
        ),
        color_scheme=rx.match(
            estado,
            ("completado", "green"),
            ("pendiente", "yellow"),
            ("anulado", "red"),
            "gray"
        ),
        variant="solid",
        size="2"
    )


def modal_detalle_pago() -> rx.Component:
    """
    👁️ MODAL DE DETALLE DE PAGO - SOLO LECTURA

    ✨ Muestra información completa de un pago procesado:
    - Datos del paciente
    - Montos en USD y BS
    - Métodos de pago utilizados
    - Descuentos y observaciones
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                AppState.pago_seleccionado,
                rx.vstack(
                    # ==========================================
                    # HEADER CON RECIBO Y ESTADO
                    # ==========================================
                    rx.hstack(
                        rx.hstack(
                            rx.icon("receipt", size=24, color=COLORS["primary"]["500"]),
                            rx.vstack(
                                rx.text(
                                    "Detalle de Pago",
                                    style={
                                        "font_size": "1.2rem",
                                        "font_weight": "700",
                                        "color": DARK_THEME["colors"]["text_primary"]
                                    }
                                ),
                                rx.text(
                                    AppState.pago_seleccionado.numero_recibo,
                                    size="2",
                                    color=COLORS["primary"]["400"],
                                    weight="medium"
                                ),
                                spacing="1",
                                align="start"
                            ),
                            spacing="3",
                            align="center"
                        ),
                        rx.spacer(),
                        rx.hstack(
                            estado_pago_badge(AppState.pago_seleccionado.estado_pago),
                            rx.dialog.close(
                                rx.button(
                                    rx.icon("x", size=20),
                                    style={
                                        "background": "transparent",
                                        "border": "none",
                                        "color": COLORS["gray"]["500"],
                                        "cursor": "pointer",
                                        "_hover": {"color": COLORS["gray"]["700"]}
                                    },
                                    on_click=AppState.cerrar_modal_detalle_pago
                                )
                            ),
                            spacing="3",
                            align="center"
                        ),
                        width="100%",
                        align="center"
                    ),

                    rx.divider(),

                    # ==========================================
                    # INFORMACIÓN DEL PACIENTE
                    # ==========================================
                    rx.vstack(
                        rx.hstack(
                            rx.icon("user", size=18, color=COLORS["primary"]["400"]),
                            rx.text(
                                "Información del Paciente",
                                style={
                                    "font_size": "1rem",
                                    "font_weight": "700",
                                    "color": DARK_THEME["colors"]["text_primary"]
                                }
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.grid(
                            # Nombre
                            rx.vstack(
                                rx.text("Paciente", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                rx.text(
                                    AppState.pago_seleccionado.paciente_nombre,
                                    style={
                                        "font_size": "0.9rem",
                                        "font_weight": "600",
                                        "color": DARK_THEME["colors"]["text_primary"]
                                    }
                                ),
                                spacing="1",
                                align="start",
                                style={"grid_column": "span 2"}
                            ),
                            # Documento
                            rx.vstack(
                                rx.text("Documento", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                rx.text(
                                    AppState.pago_seleccionado.paciente_documento,
                                    style={
                                        "font_size": "0.9rem",
                                        "font_weight": "600",
                                        "color": DARK_THEME["colors"]["text_primary"]
                                    }
                                ),
                                spacing="1",
                                align="start"
                            ),
                            # Fecha
                            rx.vstack(
                                rx.text("Fecha de Pago", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                rx.text(
                                    rx.cond(
                                        AppState.pago_seleccionado.fecha_pago.contains("T"),
                                        AppState.pago_seleccionado.fecha_pago.split("T")[0],
                                        AppState.pago_seleccionado.fecha_pago
                                    ),
                                    style={
                                        "font_size": "0.9rem",
                                        "font_weight": "600",
                                        "color": DARK_THEME["colors"]["text_primary"]
                                    }
                                ),
                                spacing="1",
                                align="start"
                            ),
                            columns="3",
                            spacing="4",
                            width="100%"
                        ),
                        spacing="3",
                        style={
                            "background": DARK_THEME["colors"]["surface_secondary"],
                            "border": f"1px solid {DARK_THEME['colors']['border']}",
                            "border_radius": RADIUS["lg"],
                            "padding": SPACING["4"],
                            "width": "100%"
                        }
                    ),

                    # ==========================================
                    # SECCIÓN FINANCIERA DUAL USD/BS
                    # ==========================================
                    rx.vstack(
                        rx.hstack(
                            rx.icon("wallet", size=18, color=COLORS["success"]["400"]),
                            rx.text(
                                "Información Financiera",
                                style={
                                    "font_size": "1rem",
                                    "font_weight": "700",
                                    "color": DARK_THEME["colors"]["text_primary"]
                                }
                            ),
                            spacing="2",
                            align="center"
                        ),

                        # Grid de montos USD y BS
                        rx.grid(
                            # Card USD
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("dollar-sign", size=16, color=COLORS["success"]["500"]),
                                    rx.text("USD", size="2", weight="bold", color=COLORS["success"]["400"]),
                                    spacing="2"
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Total:", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                        rx.spacer(),
                                        rx.text(f"${AppState.pago_seleccionado.monto_total_usd:.2f}", size="2", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                                        width="100%"
                                    ),
                                    rx.hstack(
                                        rx.text("Pagado:", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                        rx.spacer(),
                                        rx.text(f"${AppState.pago_seleccionado.monto_pagado_usd:.2f}", size="2", weight="bold", color=COLORS["success"]["400"]),
                                        width="100%"
                                    ),
                                    rx.hstack(
                                        rx.text("Saldo:", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                        rx.spacer(),
                                        rx.text(
                                            f"${AppState.pago_seleccionado.saldo_pendiente_usd:.2f}",
                                            size="2",
                                            weight="bold",
                                            color=rx.cond(
                                                AppState.pago_seleccionado.saldo_pendiente_usd > 0,
                                                COLORS["warning"]["400"],
                                                COLORS["success"]["400"]
                                            )
                                        ),
                                        width="100%"
                                    ),
                                    spacing="2",
                                    width="100%"
                                ),
                                spacing="3",
                                style={
                                    "background": f"{COLORS['success']['500']}10",
                                    "border": f"1px solid {COLORS['success']['500']}40",
                                    "border_radius": RADIUS["lg"],
                                    "padding": SPACING["4"],
                                    "width": "100%"
                                }
                            ),

                            # Card BS
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("banknote", size=16, color=COLORS["primary"]["500"]),
                                    rx.text("BS", size="2", weight="bold", color=COLORS["primary"]["400"]),
                                    spacing="2"
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Total:", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                        rx.spacer(),
                                        rx.text(f"{AppState.pago_seleccionado.monto_total_bs:,.0f} Bs", size="2", weight="medium", color=DARK_THEME["colors"]["text_primary"]),
                                        width="100%"
                                    ),
                                    rx.hstack(
                                        rx.text("Pagado:", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                        rx.spacer(),
                                        rx.text(f"{AppState.pago_seleccionado.monto_pagado_bs:,.0f} Bs", size="2", weight="bold", color=COLORS["primary"]["400"]),
                                        width="100%"
                                    ),
                                    rx.hstack(
                                        rx.text("Saldo:", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                        rx.spacer(),
                                        rx.text(
                                            f"{AppState.pago_seleccionado.saldo_pendiente_bs:,.0f} Bs",
                                            size="2",
                                            weight="bold",
                                            color=rx.cond(
                                                AppState.pago_seleccionado.saldo_pendiente_bs > 0,
                                                COLORS["warning"]["400"],
                                                COLORS["success"]["400"]
                                            )
                                        ),
                                        width="100%"
                                    ),
                                    spacing="2",
                                    width="100%"
                                ),
                                spacing="3",
                                style={
                                    "background": f"{COLORS['primary']['500']}10",
                                    "border": f"1px solid {COLORS['primary']['500']}40",
                                    "border_radius": RADIUS["lg"],
                                    "padding": SPACING["4"],
                                    "width": "100%"
                                }
                            ),

                            columns="2",
                            spacing="4",
                            width="100%"
                        ),

                        # Tasa de cambio
                        rx.hstack(
                            rx.icon("trending-up", size=14, color=COLORS["primary"]["400"]),
                            rx.text(
                                f"Tasa de cambio: 1 USD = {AppState.pago_seleccionado.tasa_cambio_bs_usd:.2f} BS",
                                size="1",
                                color=DARK_THEME["colors"]["text_secondary"]
                            ),
                            spacing="2",
                            align="center",
                            style={
                                "padding": SPACING["2"],
                                "border_radius": RADIUS["md"],
                                "background": f"{COLORS['primary']['400']}10",
                                "border": f"1px solid {COLORS['primary']['400']}30"
                            }
                        ),

                        spacing="3",
                        width="100%"
                    ),

                    # ==========================================
                    # MÉTODOS DE PAGO UTILIZADOS
                    # ==========================================
                    
                    rx.cond(
                        AppState.pago_seleccionado.metodos_pago.length() > 0,
                        rx.vstack(
                            rx.hstack(
                                rx.icon("credit-card", size=18, color=COLORS["secondary"]["500"]),
                                rx.text(
                                    "Métodos de Pago",
                                    style={
                                        "font_size": "1rem",
                                        "font_weight": "700",
                                        "color": DARK_THEME["colors"]["text_primary"]
                                    }
                                ),
                                spacing="2",
                                align="center"
                            ),
                            rx.vstack(
                                rx.foreach(
                                    AppState.pago_seleccionado.metodos_pago,
                                    lambda metodo: rx.hstack(
                                        rx.icon(
                                            rx.match(
                                                metodo.tipo,
                                                ("efectivo", "wallet"),
                                                ("tarjeta_credito", "credit-card"),
                                                ("tarjeta_debito", "credit-card"),
                                                ("transferencia", "arrow-right-left"),
                                                ("pago_movil", "smartphone"),
                                                "circle"
                                            ),
                                            size=16,
                                            color=COLORS["primary"]["400"]
                                        ),
                                        rx.text(
                                            metodo.tipo.replace("_", " ").title(),
                                            size="2",
                                            weight="medium",
                                            color=DARK_THEME["colors"]["text_primary"],
                                            style={"flex": "1"}
                                        ),
                                        rx.badge(
                                            metodo.moneda,
                                            color_scheme=rx.match(
                                                metodo.moneda,
                                                ("USD", "green"),
                                                ("BS", "cyan"),
                                                "gray"
                                            ),
                                            variant="soft"
                                        ),
                                        rx.text(
                                            rx.cond(
                                                metodo.moneda == "USD",
                                                f"${metodo.monto:.2f}",
                                                f"{metodo.monto:,.0f} Bs"
                                            ),
                                            size="2",
                                            weight="bold",
                                            color=COLORS["success"]["400"]
                                        ),
                                        width="100%",
                                        align="center",
                                        spacing="3",
                                        style={
                                            "padding": SPACING["3"],
                                            "border_bottom": f"1px solid {DARK_THEME['colors']['border']}",
                                            "_last": {"border_bottom": "none"}
                                        }
                                    )
                                ),
                                spacing="0",
                                width="100%"
                            ),
                            spacing="3",
                            style={
                                "background": DARK_THEME["colors"]["surface_secondary"],
                                "border": f"1px solid {DARK_THEME['colors']['border']}",
                                "border_radius": RADIUS["lg"],
                                "padding": SPACING["4"],
                                "width": "100%"
                            }
                        ),
                        rx.box()  # No mostrar si no hay métodos de pago
                    ),

                    # ==========================================
                    # INFORMACIÓN ADICIONAL
                    # ==========================================
                    rx.vstack(
                        rx.hstack(
                            rx.icon("info", size=18, color=COLORS["gray"]["400"]),
                            rx.text(
                                "Información Adicional",
                                style={
                                    "font_size": "1rem",
                                    "font_weight": "700",
                                    "color": DARK_THEME["colors"]["text_primary"]
                                }
                            ),
                            spacing="2",
                            align="center"
                        ),

                        # Concepto
                        rx.cond(
                            AppState.pago_seleccionado.concepto != "",
                            rx.vstack(
                                rx.text("Concepto", size="1", color=DARK_THEME["colors"]["text_secondary"]),
                                rx.text(
                                    AppState.pago_seleccionado.concepto,
                                    size="2",
                                    color=DARK_THEME["colors"]["text_primary"]
                                ),
                                spacing="1",
                                align="start",
                                width="100%"
                            ),
                            rx.box()
                        ),

                        # Descuento
                        rx.cond(
                            AppState.pago_seleccionado.descuento_aplicado > 0,
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Descuento Aplicado:", size="2", color=COLORS["warning"]["400"], weight="bold"),
                                    rx.text(f"${AppState.pago_seleccionado.descuento_aplicado:.2f}", size="2", weight="bold", color=COLORS["warning"]["400"]),
                                    spacing="2"
                                ),
                                rx.cond(
                                    AppState.pago_seleccionado.motivo_descuento != "",
                                    rx.hstack(
                                        rx.icon("message-square", size=14, color=DARK_THEME["colors"]["text_secondary"]),
                                        rx.text(
                                            AppState.pago_seleccionado.motivo_descuento,
                                            size="1",
                                            color=DARK_THEME["colors"]["text_secondary"],
                                            style={"font_style": "italic"}
                                        ),
                                        spacing="2"
                                    ),
                                    rx.box()
                                ),
                                spacing="1",
                                align="start",
                                width="100%",
                                style={
                                    "padding": SPACING["3"],
                                    "background": f"{COLORS['warning']['400']}10",
                                    "border": f"1px solid {COLORS['warning']['400']}40",
                                    "border_radius": RADIUS["md"]
                                }
                            ),
                            rx.box()
                        ),

                        spacing="3",
                        style={
                            "background": DARK_THEME["colors"]["surface_secondary"],
                            "border": f"1px solid {DARK_THEME['colors']['border']}",
                            "border_radius": RADIUS["lg"],
                            "padding": SPACING["4"],
                            "width": "100%"
                        }
                    ),

                    # ==========================================
                    # FOOTER CON BOTÓN IMPRIMIR
                    # ==========================================
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", size=16),
                                    rx.text("Cerrar"),
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
                                on_click=AppState.cerrar_modal_detalle_pago
                            )
                        ),

                        rx.spacer(),

                        rx.button(
                            rx.hstack(
                                rx.icon("printer", size=16),
                                rx.text("Imprimir Recibo"),
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
                                "box_shadow": SHADOWS["glow_primary"],
                                "transition": ANIMATIONS["presets"]["crystal_hover"],
                                "_hover": {
                                    "transform": "translateY(-2px) scale(1.02)",
                                    "box_shadow": f"0 0 30px {COLORS['primary']['500']}40, {SHADOWS['crystal_lg']}"
                                }
                            },
                            on_click=lambda: AppState.imprimir_recibo(AppState.pago_seleccionado.id)
                        ),

                        spacing="3",
                        width="100%",
                        align="center"
                    ),

                    spacing="4",
                    width="100%",
                    align="stretch"
                ),

                # Estado vacío (cuando no hay pago seleccionado)
                rx.vstack(
                    rx.icon("alert-circle", size=48, color=COLORS["gray"]["400"]),
                    rx.text(
                        "No hay pago seleccionado",
                        size="4",
                        weight="bold",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    spacing="4",
                    align="center",
                    style={"padding": SPACING["8"]}
                )
            ),

            style={
                "max_width": "700px",
                "padding": SPACING["6"],
                "border_radius": RADIUS["2xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['primary']['200']}30",
                "overflow_y": "auto",
                "max_height": "90vh",
                "backdrop_filter": "blur(20px)"
            }
        ),
        open=AppState.modal_detalle_pago_abierto,
        on_open_change=AppState.cerrar_modal_detalle_pago
    )
