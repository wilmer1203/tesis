# 🛒 SELECTOR DE SERVICIOS CON TABLA DE INTERVENCIONES AGREGADAS
# dental_system/components/odontologia/selector_intervenciones_v2.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, DARK_THEME, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS PARA EL NUEVO FLUJO
# ==========================================

SELECTOR_CARD_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['50']} 0%, white 100%)",
    "border": f"1px solid {COLORS['primary']['200']}",
    "border_radius": RADIUS["xl"],
    "padding": SPACING["6"],
    "box_shadow": SHADOWS["lg"],
    "margin_bottom": SPACING["6"]
}

TABLA_SERVICIOS_STYLE = {
    "background": "white",
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["lg"],
    "overflow": "hidden",
    "margin_bottom": SPACING["6"]
}

TOTAL_ROW_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['success']['50']} 0%, {COLORS['success']['25']} 100%)",
    "border_top": f"2px solid {COLORS['success']['200']}",
    "font_weight": "bold",
    "color": COLORS["success"]["700"]
}

# ==========================================
# 🔧 SELECTOR DE SERVICIOS PRINCIPAL
# ==========================================

def selector_servicio_formulario() -> rx.Component:
    """🔧 Formulario para agregar servicios a la intervención"""
    return rx.box(
        rx.vstack(
            # Header del selector
            rx.hstack(
                rx.icon("stethoscope", size=24, color=COLORS["primary"]["500"]),
                rx.text(
                    "Agregar Servicio a la Intervención",
                    size="5",
                    weight="bold",
                    color=COLORS["gray"]["800"]
                ),
                spacing="3",
                align_items="center",
                margin_bottom="4"
            ),
            
            # Estado de los servicios y botón de carga
            rx.hstack(
                rx.cond(
                    AppState.servicios_para_selector.length() > 5,  # Si hay más de 5 servicios, son reales
                    rx.hstack(
                        rx.icon("database", size=16, color="green.500"),
                        rx.text(
                            rx.cond(
                                AppState.servicios_para_selector.length() > 0,
                                f"{AppState.servicios_para_selector.length()} servicios de la BD",
                                "Cargando servicios..."
                            ),
                            size="2",
                            color="green.600",
                            weight="medium"
                        ),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.icon("alert_circle", size=16, color="orange.500"),
                        rx.text(
                            rx.cond(
                                AppState.servicios_para_selector.length() > 0,
                                f"Usando {AppState.servicios_para_selector.length()} servicios de ejemplo",
                                "No hay servicios cargados"
                            ),
                            size="2",
                            color="orange.600"
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("refresh_cw", size=14),
                                rx.text("Cargar desde BD"),
                                spacing="1"
                            ),
                            size="1",
                            variant="outline",
                            color_scheme="blue",
                            on_click=AppState.cargar_servicios_para_intervencion
                        ),
                        spacing="2",
                        align_items="center"
                    )
                ),
                rx.spacer(),
                justify="between",
                width="100%",
                margin_bottom="3"
            ),
            
            # Grid del formulario
            rx.grid(
                # Columna 1: Selector de servicio
                rx.vstack(
                    rx.text(
                        "Servicio *",
                        size="3",
                        weight="medium",
                        color=COLORS["gray"]["600"]
                    ),
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Seleccionar servicio...",
                            style={
                                "width": "100%",
                                "padding": "0.75rem",
                                "border": f"1px solid {COLORS['gray']['300']}",
                                "border_radius": "8px",
                                "_focus": {
                                    "border_color": COLORS["primary"]["400"],
                                    "box_shadow": f"0 0 0 3px {COLORS['primary']['100']}"
                                }
                            }
                        ),
                        rx.select.content(
                            rx.foreach(
                                AppState.servicios_para_selector,
                                lambda servicio: rx.select.item(
                                    rx.vstack(
                                        rx.text(servicio.nombre, weight="medium"),
                                        rx.hstack(
                                            rx.text(
                                                servicio.categoria,
                                                size="2",
                                                color=COLORS["gray"]["500"]
                                            ),
                                            rx.text("•", size="2", color=COLORS["gray"]["400"]),
                                            rx.text(
                                                servicio.precios_dual_display,
                                                size="2",
                                                color=COLORS["primary"]["600"],
                                                weight="medium"
                                            ),
                                            spacing="1"
                                        ),
                                        align_items="start",
                                        spacing="1"
                                    ),
                                    value=servicio.id
                                )
                            )
                        ),
                        value=AppState.servicio_temporal.id,
                        on_change=AppState.seleccionar_servicio_temporal
                    ),
                    spacing="2",
                    width="100%"
                ),
                
                # Columna 2: Dientes afectados - DINÁMICO según servicio
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            AppState.texto_campo_dientes,  # 🔥 Texto dinámico
                            size="3",
                            weight="medium",
                            color=rx.cond(
                                AppState.servicio_actual_requiere_dientes,
                                COLORS["gray"]["600"],      # Color normal si es requerido
                                COLORS["gray"]["500"]       # Color más tenue si es opcional
                            )
                        ),
                        rx.cond(
                            AppState.servicio_actual_requiere_dientes,
                            rx.text("*", color="red.500", weight="bold"),  # Asterisco solo si es requerido
                            rx.text("(opcional)", size="2", color=COLORS["gray"]["400"])  # Texto opcional
                        ),
                        spacing="1"
                    ),
                    rx.input(
                        placeholder=AppState.placeholder_campo_dientes,  # 🔥 Placeholder dinámico
                        value=AppState.dientes_seleccionados_texto,
                        on_change=AppState.set_dientes_seleccionados_texto,
                        style={
                            "width": "100%",
                            "padding": "0.75rem",
                            "border": rx.cond(
                                AppState.servicio_actual_requiere_dientes,
                                f"1px solid {COLORS['gray']['300']}",      # Borde normal si es requerido
                                f"1px solid {COLORS['gray']['200']}"       # Borde más tenue si es opcional
                            ),
                            "border_radius": "8px",
                            "opacity": rx.cond(
                                AppState.servicio_actual_requiere_dientes,
                                "1.0",      # Opacidad normal si es requerido
                                "0.8"       # Opacidad reducida si es opcional
                            )
                        }
                    ),
                    # Ejemplos rápidos de dientes comunes - SOLO para servicios específicos
                    rx.cond(
                        AppState.servicio_actual_requiere_dientes,  # Solo mostrar si requiere dientes
                        rx.vstack(
                            rx.hstack(
                                rx.text("Rápido:", size="2", color=COLORS["gray"]["500"]),
                                rx.button(
                                    "Todos",
                                    size="1",
                                    variant="ghost",
                                    on_click=lambda: AppState.set_dientes_seleccionados_texto("Todos")
                                ),
                                rx.button(
                                    "11, 21",
                                    size="1",
                                    variant="ghost",
                                    on_click=lambda: AppState.set_dientes_seleccionados_texto("11, 21")
                                ),
                                rx.button(
                                    "16, 26, 36, 46",
                                    size="1",
                                    variant="ghost",
                                    on_click=lambda: AppState.set_dientes_seleccionados_texto("16, 26, 36, 46")
                                ),
                                spacing="1",
                                align_items="center"
                            ),
                            rx.text(
                                "Usar números FDI (11-18, 21-28, 31-38, 41-48) o 'Todos' para limpieza general",
                                size="1",
                                color=COLORS["gray"]["500"]
                            ),
                            spacing="1"
                        ),
                        rx.text(
                            "💡 Este servicio se aplicará a toda la boca automáticamente",
                            size="2",
                            color=COLORS["gray"]["400"],
                            style={"font_style": "italic"}
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),
                
                # Columna 3: Cantidad
                rx.vstack(
                    rx.text(
                        "Cantidad",
                        size="3",
                        weight="medium",
                        color=COLORS["gray"]["600"]
                    ),
                    rx.input(
                        type="number",
                        value=AppState.cantidad_temporal,
                        on_change=AppState.set_cantidad_temporal,
                        min="1",
                        placeholder="1",
                        style={
                            "width": "100%",
                            "padding": "0.75rem",
                            "border": f"1px solid {COLORS['gray']['300']}",
                            "border_radius": "8px"
                        }
                    ),
                    spacing="2",
                    width="100%"
                ),
                
                columns="3",
                spacing="6",
                width="100%"
            ),
            
            # Mensaje de error si existe
            rx.cond(
                AppState.mensaje_error_intervencion != "",
                rx.box(
                    rx.hstack(
                        rx.icon("triangle_alert", size=16, color="red.500"),
                        rx.text(
                            AppState.mensaje_error_intervencion,
                            size="3",
                            color="red.600",
                            weight="medium"
                        ),
                        spacing="2"
                    ),
                    padding="3",
                    border_radius="8px",
                    background="red.50",
                    border="1px solid",
                    border_color="red.200",
                    width="100%"
                ),
                rx.box()
            ),
            
            # Botones de acción
            rx.hstack(
                rx.cond(
                    AppState.servicio_actual_requiere_dientes,
                    rx.button(
                        rx.hstack(
                            rx.icon("mouse_pointer", size=16),
                            rx.text("Usar del Odontograma"),
                            spacing="2"
                        ),
                        size="2",
                        variant="outline",
                        color_scheme="blue",
                        on_click=AppState.usar_dientes_del_odontograma
                    ),
                    rx.box()  # Empty box when service doesn't require specific teeth
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=16),
                        rx.text("Agregar Servicio"),
                        spacing="2"
                    ),
                    size="3",
                    color_scheme="green",
                    disabled=AppState.servicio_temporal.id == "",
                    on_click=AppState.agregar_servicio_a_intervencion,
                    style={
                        "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['success']['600']} 100%)",
                        "box_shadow": f"0 4px 15px {COLORS['success']['200']}"
                    }
                ),
                spacing="3",
                width="100%",
                margin_top="4"
            ),
            
            spacing="4",
            width="100%"
        ),
        style=SELECTOR_CARD_STYLE
    )

# ==========================================
# 📊 TABLA DE SERVICIOS AGREGADOS
# ==========================================

def tabla_servicios_agregados() -> rx.Component:
    """📊 Tabla con los servicios agregados a la intervención"""
    return rx.box(
        rx.vstack(
            # Header de la tabla
            rx.hstack(
                rx.icon("list", size=24, color=COLORS["primary"]["500"]),
                rx.text(
                    "Servicios en la Intervención",
                    size="5",
                    weight="bold",
                    color=COLORS["gray"]["800"]
                ),
                rx.spacer(),
                rx.badge(
                    f"{AppState.servicios_en_intervencion.length()} servicios",
                    color_scheme="blue",
                    variant="soft"
                ),
                spacing="3",
                align_items="center",
                margin_bottom="4"
            ),
            
            # Tabla responsiva
            rx.cond(
                AppState.servicios_en_intervencion.length() > 0,
                
                # Tabla con datos
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell(
                                "Servicio",
                                style={"background": COLORS["gray"]["50"]}
                            ),
                            rx.table.column_header_cell(
                                "Diente(s)",
                                style={"background": COLORS["gray"]["50"]}
                            ),
                            rx.table.column_header_cell(
                                "Cant.",
                                style={"background": COLORS["gray"]["50"]}
                            ),
                            rx.table.column_header_cell(
                                "Precio BS",
                                style={"background": COLORS["gray"]["50"]}
                            ),
                            rx.table.column_header_cell(
                                "Precio USD",
                                style={"background": COLORS["gray"]["50"]}
                            ),
                            rx.table.column_header_cell(
                                "Acciones",
                                style={"background": COLORS["gray"]["50"]}
                            ),
                        )
                    ),
                    rx.table.body(
                        # Filas de servicios
                        rx.foreach(
                            AppState.servicios_en_intervencion,
                            lambda servicio, idx: rx.table.row(
                                rx.table.row_header_cell(
                                    rx.vstack(
                                        rx.text(
                                            servicio.nombre_servicio,
                                            weight="medium",
                                            color=COLORS["gray"]["800"]
                                        ),
                                        rx.text(
                                            servicio.categoria_servicio,
                                            size="2",
                                            color=COLORS["gray"]["500"]
                                        ),
                                        align_items="start",
                                        spacing="1"
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        servicio.dientes_texto,
                                        size="3",
                                        color=COLORS["gray"]["700"]
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        servicio.cantidad,
                                        size="3",
                                        color=COLORS["gray"]["700"],
                                        text_align="center"
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        f"{servicio.total_bs:,.0f} Bs",
                                        size="3",
                                        color=COLORS["gray"]["700"],
                                        weight="medium"
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        f"${servicio.total_usd:.2f}",
                                        size="3",
                                        color=COLORS["primary"]["600"],
                                        weight="medium"
                                    )
                                ),
                                rx.table.cell(
                                    rx.button(
                                        rx.icon("trash-2", size=16),
                                        size="2",
                                        variant="ghost",
                                        color_scheme="red",
                                        on_click=lambda: AppState.remover_servicio_de_intervencion(idx)
                                    )
                                ),
                                style={
                                    "_hover": {"background": COLORS["gray"]["50"]}
                                }
                            )
                        ),
                        
                        # Fila de totales
                        rx.table.row(
                            rx.table.cell(""),
                            rx.table.cell(""),
                            rx.table.cell(
                                rx.text("TOTAL:", weight="bold"),
                                style={"text_align": "center"}
                            ),
                            rx.table.cell(
                                rx.text(
                                    f"{AppState.total_intervencion_bs:,.0f} Bs",
                                    weight="bold",
                                    color=COLORS["success"]["600"]
                                )
                            ),
                            rx.table.cell(
                                rx.text(
                                    f"${AppState.total_intervencion_usd:.2f}",
                                    weight="bold",
                                    color=COLORS["success"]["600"]
                                )
                            ),
                            rx.table.cell(""),
                            style=TOTAL_ROW_STYLE
                        )
                    ),
                    style={"width": "100%"}
                ),
                
                # Estado vacío
                rx.box(
                    rx.vstack(
                        rx.icon("inbox", size=48, color=COLORS["gray"]["300"]),
                        rx.text(
                            "No hay servicios agregados",
                            size="4",
                            color=COLORS["gray"]["500"],
                            weight="medium"
                        ),
                        rx.text(
                            "Selecciona servicios arriba para agregarlos a la intervención",
                            size="3",
                            color=COLORS["gray"]["400"],
                            text_align="center"
                        ),
                        spacing="3",
                        align_items="center"
                    ),
                    padding="12",
                    text_align="center",
                    style={
                        "border": f"2px dashed {COLORS['gray']['200']}",
                        "border_radius": RADIUS["lg"],
                        "background": COLORS["gray"]["25"]
                    }
                )
            ),
            
            spacing="4",
            width="100%"
        ),
        style=TABLA_SERVICIOS_STYLE
    )

# ==========================================
# 🏁 BOTÓN FINALIZAR INTERVENCIÓN
# ==========================================

def boton_finalizar_intervencion() -> rx.Component:
    """🏁 Botón principal para finalizar y guardar la intervención"""
    return rx.cond(
        AppState.servicios_en_intervencion.length() > 0,
        
        rx.box(
            rx.vstack(
                # Resumen final
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "Resumen de la Intervención",
                            size="4",
                            weight="bold",
                            color=COLORS["gray"]["700"]
                        ),
                        rx.hstack(
                            rx.text(
                                f"Total de servicios: {AppState.servicios_en_intervencion.length()}",
                                size="3",
                                color=COLORS["gray"]["600"]
                            ),
                            rx.text("•", color=COLORS["gray"]["400"]),
                            rx.text(
                                f"Paciente: {AppState.paciente_actual.nombre_completo}",
                                size="3",
                                color=COLORS["gray"]["600"]
                            ),
                            spacing="2"
                        ),
                        align_items="start",
                        spacing="1"
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.text(
                            f"{AppState.total_intervencion_bs:,.0f} Bs",
                            size="5",
                            weight="bold",
                            color=COLORS["success"]["600"]
                        ),
                        rx.text(
                            f"${AppState.total_intervencion_usd:.2f} USD",
                            size="5",
                            weight="bold",
                            color=COLORS["success"]["600"]
                        ),
                        align_items="end",
                        spacing="1"
                    ),
                    align_items="center",
                    width="100%",
                    margin_bottom="6"
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("x", size=16),
                            rx.text("Cancelar"),
                            spacing="2"
                        ),
                        size="3",
                        variant="outline",
                        color_scheme="gray",
                        on_click=AppState.cancelar_intervencion
                    ),
                    
                    rx.spacer(),
                    
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                AppState.guardando_intervencion,
                                rx.spinner(size="3", color="white"),
                                rx.icon("check", size=16)
                            ),
                            rx.text("Finalizar Consulta"),
                            spacing="2"
                        ),
                        size="4",
                        loading=AppState.guardando_intervencion,
                        disabled=AppState.guardando_intervencion,
                        on_click=AppState.finalizar_consulta_completa,
                        style={
                            "background": f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['success']['600']} 100%)",
                            "box_shadow": f"0 6px 25px {COLORS['success']['300']}",
                            "color": "white",
                            "_hover": {
                                "transform": "translateY(-2px)",
                                "box_shadow": f"0 10px 35px {COLORS['success']['400']}"
                            }
                        }
                    ),
                    
                    spacing="4",
                    width="100%",
                    align_items="center"
                ),
                
                spacing="6",
                width="100%"
            ),
            style={
                "background": f"linear-gradient(135deg, {COLORS['success']['25']} 0%, white 100%)",
                "border": f"1px solid {COLORS['success']['200']}",
                "border_radius": RADIUS["xl"],
                "padding": SPACING["6"],
                "box_shadow": SHADOWS["lg"]
            }
        )
    )

# ==========================================
# 📦 COMPONENTE PRINCIPAL
# ==========================================

def nuevo_tab_intervencion() -> rx.Component:
    """📦 Tab completo de intervención con el nuevo flujo"""
    return rx.vstack(
        # Selector de servicios
        selector_servicio_formulario(),
        
        # Tabla de servicios agregados
        tabla_servicios_agregados(),
        
        # Botón finalizar
        boton_finalizar_intervencion(),
        
        spacing="6",
        width="100%",
        padding="4",
        
        # Cargar servicios al montar el componente
        on_mount=AppState.cargar_servicios_para_intervencion
    )