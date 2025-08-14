# 📄 PÁGINA DE PAGOS - SIGUIENDO PATRÓN DE SERVICIOS
# dental_system/pages/pagos_page.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, primary_button, secondary_button
from dental_system.components.table_components import payments_table


def payment_form_modal() -> rx.Component:
    """📝 Modal para crear/editar pago"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AppState.selected_pago.length() > 0,
                    "Editar Pago",
                    "Nuevo Pago"
                )
            ),
            
            # Formulario
            rx.vstack(
                # Paciente y Concepto
                rx.hstack(
                    rx.vstack(
                        rx.text("Paciente *", size="2", weight="medium"),
                        rx.select(
                            # TODO: Cargar lista de pacientes dinámicamente
                            ["Paciente 1", "Paciente 2", "Paciente 3"],
                            value=AppState.pago_form["paciente_id"],
                            on_change=lambda v: AppState.update_pago_form("paciente_id", v),
                            placeholder="Seleccionar paciente"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Concepto *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.pago_form["concepto"],
                            on_change=lambda v: AppState.update_pago_form("concepto", v),
                            placeholder="Consulta general, tratamiento..."
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Montos
                rx.hstack(
                    rx.vstack(
                        rx.text("Monto Total *", size="2", weight="medium"),
                        rx.input(
                            type="number",
                            value=AppState.pago_form["monto_total"],
                            on_change=lambda v: AppState.update_pago_form("monto_total", v),
                            placeholder="0.00"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Monto Pagado *", size="2", weight="medium"),
                        rx.input(
                            type="number",
                            value=AppState.pago_form["monto_pagado"],
                            on_change=lambda v: AppState.update_pago_form("monto_pagado", v),
                            placeholder="0.00"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Método de pago y referencia
                rx.hstack(
                    rx.vstack(
                        rx.text("Método de Pago *", size="2", weight="medium"),
                        rx.select(
                            [
                                "efectivo",
                                "tarjeta_credito",
                                "tarjeta_debito", 
                                "transferencia",
                                "pago_movil",
                                "cheque"
                            ],
                            value=AppState.pago_form["metodo_pago"],
                            on_change=lambda v: AppState.update_pago_form("metodo_pago", v),
                            placeholder="Seleccionar método"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Referencia", size="2", weight="medium"),
                        rx.input(
                            value=AppState.pago_form["referencia_pago"],
                            on_change=lambda v: AppState.update_pago_form("referencia_pago", v),
                            placeholder="Número de transacción..."
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Descuentos e impuestos (opcional)
                rx.vstack(
                    rx.text("Ajustes Adicionales", size="3", weight="medium", color="gray.700"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Descuento", size="2", weight="medium"),
                            rx.input(
                                type="number",
                                value=AppState.pago_form["descuento_aplicado"],
                                on_change=lambda v: AppState.update_pago_form("descuento_aplicado", v),
                                placeholder="0.00"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Impuestos", size="2", weight="medium"),
                            rx.input(
                                type="number",
                                value=AppState.pago_form["impuestos"],
                                on_change=lambda v: AppState.update_pago_form("impuestos", v),
                                placeholder="0.00"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    spacing="2"
                ),
                
                # Motivo del descuento (si aplica)
                rx.cond(
                    AppState.pago_form["descuento_aplicado"] != "",
                    rx.vstack(
                        rx.text("Motivo del Descuento", size="2", weight="medium"),
                        rx.input(
                            value=AppState.pago_form["motivo_descuento"],
                            on_change=lambda v: AppState.update_pago_form("motivo_descuento", v),
                            placeholder="Especificar motivo del descuento"
                        ),
                        spacing="1",
                        width="100%"
                    )
                ),
                
                # Consulta relacionada (opcional)
                rx.vstack(
                    rx.text("Consulta Relacionada", size="2", weight="medium"),
                    rx.select(
                        # TODO: Cargar consultas del paciente dinámicamente
                        ["Sin consulta", "Consulta 1", "Consulta 2"],
                        value=AppState.pago_form["consulta_id"],
                        on_change=lambda v: AppState.update_pago_form("consulta_id", v),
                        placeholder="Seleccionar consulta (opcional)"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                # Observaciones
                rx.vstack(
                    rx.text("Observaciones", size="2", weight="medium"),
                    rx.text_area(
                        value=AppState.pago_form["observaciones"],
                        on_change=lambda v: AppState.update_pago_form("observaciones", v),
                        placeholder="Observaciones adicionales...",
                        height="80px"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                spacing="4",
                width="100%"
            ),
            
            # Error message
            rx.cond(
                AppState.error_message != "",
                rx.callout(
                    AppState.error_message,
                    icon="triangle-alert",
                    color_scheme="red",
                    variant="surface",
                    margin_bottom="16px"
                )
            ),
            
            # Botones de acción
            rx.hstack(
                rx.dialog.close(
                    secondary_button("Cancelar"),
                ),
                primary_button(
                    text=rx.cond(
                        AppState.selected_pago.length() > 0,
                        "Actualizar",
                        "Crear Pago"
                    ),
                    icon="check",
                    on_click=AppState.save_pago,
                    loading=AppState.is_loading_pagos
                ),
                spacing="2",
                justify="end"
            ),
            
            max_width="800px",
            padding="6"
        ),
        open=AppState.show_pago_modal,
        on_open_change=AppState.toggle_pago_modal
    )


def payments_controls() -> rx.Component:
    """🎛️ Controles de la página de pagos"""
    return rx.hstack(
        # Búsqueda
        rx.input(
            placeholder="🔍 Buscar por número de recibo...",
            value=AppState.pagos_search,
            on_change=AppState.set_pagos_search,
            on_key_down=AppState.handle_pagos_search_keydown,
            size="3",
            width="300px"
        ),
        
        # Filtro por estado
        rx.select(
            ["todos", "completado", "pendiente", "anulado"],
            placeholder="Todos los estados",
            value=AppState.pagos_estado_filter,
            on_change=AppState.set_pagos_estado_filter,
            size="3"
        ),
        
        # Filtro por método de pago
        rx.select(
            ["todos", "efectivo", "tarjeta_credito", "tarjeta_debito", "transferencia", "pago_movil", "cheque"],
            placeholder="Todos los métodos",
            value=AppState.pagos_metodo_filter,
            on_change=AppState.set_pagos_metodo_filter,
            size="3"
        ),
        
        # Filtros de fecha (básico)
        rx.input(
            type="date",
            value=AppState.pagos_fecha_inicio,
            on_change=AppState.set_pagos_fecha_inicio,
            size="3"
        ),
        rx.input(
            type="date", 
            value=AppState.pagos_fecha_fin,
            on_change=AppState.set_pagos_fecha_fin,
            size="3"
        ),
        
        rx.spacer(),
        
        # Botón nuevo pago
        primary_button(
            text="Nuevo Pago",
            icon="plus",
            on_click=AppState.open_new_pago_modal,
            loading=AppState.is_loading_pagos
        ),
        
        spacing="3",
        align="center",
        width="100%",
        padding_bottom="4"
    )


def pagos_page() -> rx.Component:
    """
    📄 Página principal de gestión de pagos
    Accesible por: Administrador y Gerente
    """
    return rx.vstack(
        page_header("💳 Gestión de Pagos", "Administrar pagos y facturación"),
        
        # Controles
        payments_controls(),
        
        # Tabla de pagos
        payments_table(),
        
        # Modal de formulario
        payment_form_modal(),
        
        spacing="6",
        padding="6",
        width="100%",
        min_height="100vh"
    )