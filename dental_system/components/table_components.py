import reflex as rx
from typing import Dict, List, Any
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button
from dental_system.models.personal_models import PersonalModel
from dental_system.models.pacientes_models import PacienteModel
from dental_system.models.consultas_models import ConsultaModel
# Importar sistema de temas
from dental_system.styles.themes import (
    COLORS, SHADOWS, RADIUS, SPACING, TYPOGRAPHY, 
    ANIMATIONS, create_gradient, get_color, COMPONENT_STYLES,
    GRADIENTS, GLASS_EFFECTS, DARK_THEME
)

# ==========================================
# 🎨 ESTILOS BASE SIMPLIFICADOS
# ==========================================

# Contenedor principal de tabla para tema oscuro
TABLE_STYLE = {
    "background": DARK_THEME["colors"]["surface_secondary"],
    "border_radius": RADIUS["2xl"],
    "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.4)",
    "border": f"1px solid {DARK_THEME['colors']['border']}",
    "overflow": "hidden",
    "backdrop_filter": "blur(10px)"
}


# Select elegante
SELECT_STYLE = {
    "border": f"2px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["lg"],
    "background": "white",
    "box_shadow": SHADOWS["xs"],
    "_focus": {
        "border_color": COLORS["primary"]["500"],
        "box_shadow": f"0 0 0 3px {COLORS['primary']['100']}"
    }
}

# Header de columna para tema oscuro
COLUMN_HEADER = {
    "background": f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
    "font_weight": TYPOGRAPHY["font_weight"]["bold"],
    "color": DARK_THEME["colors"]["text_primary"],
    "font_size": TYPOGRAPHY["font_size"]["sm"],
    "padding": f"{SPACING['4']} {SPACING['3']}",
    "border_bottom": f"2px solid {DARK_THEME['colors']['border']}"
}

# Celda de datos para tema oscuro
DATA_CELL = {
    "padding": f"{SPACING['4']} {SPACING['3']}",
    "border_bottom": f"1px solid {DARK_THEME['colors']['border']}",
    "color": DARK_THEME["colors"]["text_primary"],
    "transition": "all 0.2s ease-in-out"
}

# Fila con hover sutil para tema oscuro
ROW_HOVER = {
    "transition": "all 0.2s ease-in-out",
    "_hover": {
        "background": f"{DARK_THEME['colors']['surface_elevated']}80",
        "box_shadow": f"0 2px 8px {COLORS['primary']['400']}30"
    }
}

# ==========================================
# 🧩 COMPONENTES REUTILIZABLES
# ==========================================

def crystal_search_input(placeholder: str, value, on_change) -> rx.Component:
    """Input de búsqueda con efectos cristalinos"""
    return rx.box(
        rx.input(
            rx.input.slot(
                rx.icon("search", size=18, color=COLORS["primary"]["500"]), 
                color=COLORS["primary"]["500"]
            ),
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            style={
                "background": DARK_THEME["colors"]["surface_secondary"],
                "border": f"2px solid {DARK_THEME['colors']['border']}",
                "border_radius": RADIUS["2xl"],
                "padding": f"{SPACING['1']} {SPACING['3']}",
                "font_size": TYPOGRAPHY["font_size"]["base"],
                "color": DARK_THEME["colors"]["text_primary"],
                "transition": "all 0.2s ease-in-out",
                "_focus": {
                    "outline": "none",
                    "border_color": COLORS["primary"]["400"],
                    "box_shadow": f"0 0 12px {COLORS['primary']['400']}40",
                    "background": DARK_THEME["colors"]["surface_elevated"]
                },
                "_hover": {
                    "border_color": COLORS["primary"]["300"],
                    "box_shadow": f"0 2px 8px rgba(0, 0, 0, 0.2)"
                }
            },
            width="400px"
        ),
    )

def filter_select(icon: str, options: List[str], value, on_change, placeholder: str = "Filtrar") -> rx.Component:
    """Select de filtro elegante"""
    return rx.hstack(
        rx.icon(icon, size=18, color=COLORS["gray"]["500"]),
        rx.select(
            options,
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            style=SELECT_STYLE,
            size="3"
        ),
        spacing="2",
        align="center"
    )

def status_badge(is_active: bool, active_text: str = "Activo", inactive_text: str = "Inactivo") -> rx.Component:
    """Badge de estado elegante"""
    return rx.badge(
        rx.hstack(
            rx.icon(
                rx.cond(is_active, "check", "x"),
                size=14
            ),
            rx.text(rx.cond(is_active, active_text, inactive_text)),
            spacing="1"
        ),
        color_scheme=rx.cond(is_active, "green", "red"),
        variant="soft",
        size="2"
    )

def action_button(icon: str, tooltip: str, color: str, action) -> rx.Component:
    """Botón de acción elegante con tooltip"""
    return rx.tooltip(
        rx.button(
            rx.icon(icon, size=16),
            size="2",
            variant="ghost",
            style={
                "color": color,
                "transition": ANIMATIONS["presets"]["button_hover"],
                "_hover": {
                    "background": f"{color}20",
                    "transform": "scale(1.1)"
                }
            },
            on_click=action
        ),
        content=tooltip
    )

def loading_state(message: str) -> rx.Component:
    """Estado de carga elegante"""
    return rx.center(
        rx.vstack(
            rx.spinner(size="3", color=COLORS["primary"]["500"]),
            rx.text(message, size="4", color=COLORS["gray"]["700"]),
            spacing="4",
            align="center"
        ),
        padding=SPACING["12"]
    )

def empty_state(title: str, subtitle: str, icon: str) -> rx.Component:
    """Estado vacío elegante"""
    return rx.center(
        rx.vstack(
            rx.box(
                rx.icon(icon, size=48, color=COLORS["gray"]["400"]),
                padding=SPACING["6"],
                background=COLORS["gray"]["50"],
                border_radius=RADIUS["full"]
            ),
            rx.text(title, size="5", weight="bold", color=COLORS["gray"]["800"]),
            rx.text(subtitle, size="3", color=COLORS["gray"]["600"]),
            spacing="4",
            align="center"
        ),
        padding=SPACING["12"]
    )

# ==========================================
# 👥 TABLA DE PACIENTES
# ==========================================

def patients_table() -> rx.Component:
    """Tabla de pacientes elegante y funcional"""
    return rx.box(
        
        # Filtros
        rx.hstack(
            crystal_search_input(
                placeholder="Buscar por nombre, documento o teléfono...",
                value=AppState.termino_busqueda_pacientes,
                on_change=AppState.buscar_pacientes
            ),
            filter_select(
                icon="filter",
                options=["Todos", "Activos", "Inactivos"],
                value=AppState.filtro_estado,
                on_change=lambda v: AppState.aplicar_filtros({"estado": v.lower()}),
                placeholder="Estado"
            ),
            rx.spacer(),
            primary_button(
                text="Nuevo Paciente",
                icon="plus",
                on_click=lambda: AppState.seleccionar_y_abrir_modal_paciente(""),
                size="lg"
            ),
            
            # spacing="4",
            # margin_bottom="6",
            wrap="wrap",
            align="center",
            
            
        ),
        
        # Tabla
        rx.cond(
            AppState.cargando_lista_pacientes,
            loading_state("Cargando pacientes..."),
            
            rx.cond(
                AppState.pacientes_filtrados_display.length() > 0,
                
                # Tabla con datos
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Paciente", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Edad", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Género", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Documento", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Contacto", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Estado", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Acciones", style=COLUMN_HEADER),
                            )
                        ),
                        
                        rx.table.body(
                            rx.foreach(
                                AppState.pacientes_filtrados_display,
                                patient_row
                            )
                        ),
                    ),
                    style=TABLE_STYLE
                ),
                
                # Estado vacío
                empty_state(
                    "No hay pacientes",
                    "Registra tu primer paciente",
                    "users"
                )
            )
        ),
        
        class_name="space-y-6",
        padding="20px"
    )

def patient_row(patient: rx.Var[PacienteModel]) -> rx.Component:
    """Fila de paciente elegante con edad y género"""
    return rx.table.row(
        # Nombre
        rx.table.cell(
            rx.vstack(
                rx.text(
                    patient.primer_nombre + " " + patient.primer_apellido,
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["50"]
                ),
                rx.text(
                    rx.cond(
                        patient.numero_historia,
                        "HC: " + patient.numero_historia,
                        "HC: Sin asignar"
                    ),
                    size="2",
                    color=COLORS["gray"]["500"]
                ),
                spacing="1",
                align_items="start"
            ),
            style=DATA_CELL
        ),
        
        # Edad
        rx.table.cell(
            rx.cond(
                patient.edad,
                rx.text(
                    patient.edad.to(str) + " años",
                    size="3",
                    color=COLORS["gray"]["50"]
                ),
                rx.text(
                    "N/A",
                    size="3",
                    color=COLORS["gray"]["400"]
                )
            ),
            style=DATA_CELL
        ),
        
        # Género con iconos
        rx.table.cell(
            rx.cond(
                patient.genero == "masculino",
                rx.hstack(
                    rx.text("♂️", size="3"),
                    rx.text("Masc.", size="3"),
                    spacing="1",
                    align="center"
                ),
                rx.cond(
                    patient.genero == "femenino", 
                    rx.hstack(
                        rx.text("♀️", size="3"),
                        rx.text("Fem.", size="3"),
                        spacing="1",
                        align="center"
                    ),
                    rx.hstack(
                        rx.text("⚧️", size="3"),
                        rx.text("Otro", size="3"),
                        spacing="1",
                        align="center"
                    )
                )
            ),
            style=DATA_CELL
        ),
        
        # Documento
        rx.table.cell(
            rx.box(
                rx.text(
                    patient.tipo_documento + "-" + patient.numero_documento,
                    size="3",
                    font_family=TYPOGRAPHY["font_family"]["mono"]
                ),
                padding=SPACING["2"],
                background=COLORS["gray"]["800"],
                border_radius=RADIUS["md"]
            ),
            style=DATA_CELL
        ),
        
        # Contacto
        rx.table.cell(
            rx.cond(
                patient.celular_1,
                rx.hstack(
                    rx.icon("phone", size=16, color=COLORS["primary"]["500"]),
                    rx.text(patient.celular_1, size="3"),
                    spacing="2"
                ),
                rx.text("Sin celular", size="3", color=COLORS["gray"]["400"])
            ),
            style=DATA_CELL
        ),
        
        # Estado
        rx.table.cell(
            status_badge(patient.activo),
            style=DATA_CELL
        ),
        
        # Acciones
        rx.table.cell(
            rx.hstack(
                action_button(
                    icon="pencil",
                    tooltip="Editar",
                    color=COLORS["blue"]["600"],
                    action=lambda: AppState.seleccionar_y_abrir_modal_paciente(patient.id)
                ),
                
                # Botón Nueva Consulta
                action_button(
                    icon="calendar-plus",
                    tooltip="Nueva Consulta",
                    color=COLORS["secondary"]["600"],
                    action=lambda: AppState.abrir_modal_consulta("crear", {"paciente_id": patient.id, "paciente_nombre": patient.nombre_completo})
                ),
                
                rx.cond(
                    patient.activo,
                    action_button(
                        icon="trash-2",
                        tooltip="Desactivar",
                        color=COLORS["error"]["600"],
                        action=lambda: AppState.abrir_modal_confirmacion("Eliminar Paciente", "¿Está seguro de eliminar a " + patient.nombre_completo + "?", "eliminar_paciente:" + patient.id)
                    ),
                    action_button(
                        icon="refresh-cw",
                        tooltip="Reactivar",
                        color=COLORS["success"]["600"],
                        action=lambda: AppState.abrir_modal_confirmacion("Reactivar Paciente", "¿Está seguro de reactivar a " + patient.nombre_completo + "?", "reactivar_paciente:" + patient.id)
                    )
                ),
                
                spacing="1"
            ),
            style=DATA_CELL
        ),
        
        style=ROW_HOVER
    )


# ==========================================
# 🦷 TABLA DE SERVICIOS
# ==========================================

def services_table() -> rx.Component:
    """Tabla de servicios odontológicos elegante y funcional"""
    return rx.box(
        # Tabla
        rx.cond(
            AppState.is_loading_servicios,
            loading_state("Cargando servicios..."),
            
            rx.cond(
                AppState.servicios_filtrados.length() > 0,
                
                # Tabla con datos
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Código", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Servicio", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Categoría", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Precio", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Estado", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Acciones", style=COLUMN_HEADER),
                            )
                        ),
                        
                        rx.table.body(
                            rx.foreach(
                                AppState.servicios_filtrados,
                                service_row
                            )
                        ),
                    ),
                    style=TABLE_STYLE
                ),
                
                # Estado vacío
                empty_state(
                    "No hay servicios",
                    "Registra tu primer servicio odontológico",
                    "activity"
                )
            )
        ),
        
        class_name="space-y-6",
        padding="20px"
    )


def service_row(service: rx.Var[Dict]) -> rx.Component:
    """Fila de servicio elegante"""
    return rx.table.row(
        # Código
        rx.table.cell(
            rx.box(
                rx.text(
                    service["codigo"],
                    size="3",
                    weight="medium",
                    color=COLORS["primary"]["600"]
                ),
                padding=SPACING["2"],
                background=COLORS["primary"]["50"],
                border_radius=RADIUS["md"]
            ),
            style=DATA_CELL
        ),
        
        # Nombre del servicio
        rx.table.cell(
            rx.vstack(
                rx.text(
                    service["nombre"],
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["800"]
                ),
                rx.cond(
                    service["descripcion"],
                    rx.text(
                        service["descripcion"],
                        size="2",
                        color=COLORS["gray"]["500"]
                    )
                ),
                spacing="1",
                align_items="start"
            ),
            style=DATA_CELL
        ),
        
        # Categoría
        rx.table.cell(
            rx.box(
                rx.text(
                    service["categoria"],
                    size="2",
                    weight="medium"
                ),
                padding=f"{SPACING['1']} {SPACING['3']}",
                background=COLORS["blue"]["100"],
                color=COLORS["blue"]["700"],
                border_radius=RADIUS["full"]
            ),
            style=DATA_CELL
        ),
        
        # Precio
        rx.table.cell(
            rx.text(
                f"${service['precio_base']:,.0f}",
                size="3",
                weight="medium",
                color=COLORS["success"]["600"]
            ),
            style=DATA_CELL
        ),
        
        # Estado
        rx.table.cell(
            status_badge(service['activo']),
            style=DATA_CELL
        ),
        
        # Acciones
        rx.table.cell(
            rx.hstack(
                action_button(
                    icon="pencil",
                    tooltip="Editar",
                    color=COLORS["blue"]["600"],
                    action=lambda: AppState.abrir_modal_servicio(service['id'])
                ),
                
                rx.cond(
                    service['activo'],
                    action_button(
                        icon="x-circle",
                        tooltip="Desactivar",
                        color=COLORS["error"]["600"],
                        action=lambda: AppState.confirmar_eliminar_servicio(service['id'])
                    ),
                    action_button(
                        icon="check",
                        tooltip="Reactivar",
                        color=COLORS["success"]["600"],
                        action=lambda: AppState.confirmar_reactivar_servicio(service['id'])
                    )
                ),
                
                spacing="1"
            ),
            style=DATA_CELL
        ),
        
        style=ROW_HOVER
    )


# ==========================================
# 💳 TABLA DE PAGOS
# ==========================================

def payments_table() -> rx.Component:
    """Tabla de pagos elegante y funcional"""
    return rx.box(
        # Tabla
        rx.cond(
            AppState.is_loading_pagos,
            loading_state("Cargando pagos..."),
            
            rx.cond(
                AppState.pagos_con_formato.length() > 0,
                
                # Tabla con datos
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Recibo", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Paciente", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Concepto", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Monto", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Método", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Estado", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Acciones", style=COLUMN_HEADER),
                            )
                        ),
                        
                        rx.table.body(
                            rx.foreach(
                                AppState.pagos_con_formato,
                                payment_row
                            )
                        ),
                    ),
                    style=TABLE_STYLE
                ),
                
                # Estado vacío
                empty_state(
                    "No hay pagos",
                    "Registra el primer pago del sistema",
                    "credit-card"
                )
            )
        ),
        
        class_name="space-y-6",
        padding="20px"
    )


def payment_row(payment: rx.Var[Dict]) -> rx.Component:
    """Fila de pago elegante"""
    return rx.table.row(
        # Número de recibo
        rx.table.cell(
            rx.box(
                rx.text(
                    payment["numero_recibo"],
                    size="3",
                    weight="medium",
                    color=COLORS["primary"]["600"]
                ),
                padding=SPACING["2"],
                background=COLORS["primary"]["50"],
                border_radius=RADIUS["md"]
            ),
            style=DATA_CELL
        ),
        
        # Paciente
        rx.table.cell(
            rx.vstack(
                rx.text(
                    payment["paciente_nombre"],  # Asumiendo que viene con JOIN
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["800"]
                ),
                rx.text(
                    payment["paciente_historia"],  # HC000001
                    size="2",
                    color=COLORS["gray"]["500"]
                ),
                spacing="1",
                align_items="start"
            ),
            style=DATA_CELL
        ),
        
        # Concepto
        rx.table.cell(
            rx.text(
                payment["concepto"],
                size="3",
                color=COLORS["gray"]["700"],
                max_width="200px",
                white_space="nowrap",
                overflow="hidden",
                text_overflow="ellipsis"
            ),
            style=DATA_CELL
        ),
        
        # Monto
        rx.table.cell(
            rx.vstack(
                rx.text(
                    f"${payment['monto_total']:,.0f}",
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["800"]
                ),
                rx.cond(
                    payment.get("estado_pago") == "pendiente",
                    rx.text(
                        f"Pendiente: ${payment['saldo_pendiente']:,.0f}",
                        size="1",
                        color=COLORS["error"]["600"]
                    ),
                    rx.text(
                        f"Completado: ${payment['monto_pagado']:,.0f}",
                        size="1", 
                        color=COLORS["success"]["600"]
                    )
                ),
                spacing="0",
                align_items="start"
            ),
            style=DATA_CELL
        ),
        
        # Método de pago
        rx.table.cell(
            rx.box(
                rx.text(
                    payment["metodo_pago_formatted"],
                    size="2",
                    weight="medium"
                ),
                padding=f"{SPACING['1']} {SPACING['3']}",
                background=COLORS["blue"]["100"],
                color=COLORS["blue"]["700"],
                border_radius=RADIUS["full"]
            ),
            style=DATA_CELL
        ),
        
        # Estado
        rx.table.cell(
            payment_status_badge(payment["estado_pago"]),
            style=DATA_CELL
        ),
        
        # Acciones
        rx.table.cell(
            rx.hstack(
                action_button(
                    icon="eye",
                    tooltip="Ver detalles",
                    color=COLORS["blue"]["600"],
                    action=lambda: AppState.ver_detalle_pago(payment['id'])
                ),
                
                rx.cond(
                    payment["estado_pago"] == "completado",
                    action_button(
                        icon="printer",
                        tooltip="Imprimir recibo",
                        color=COLORS["gray"]["600"],
                        action=lambda: AppState.imprimir_recibo(payment['id'])
                    )
                ),
                
                rx.cond(
                    payment["estado_pago"] == "pendiente",
                    action_button(
                        icon="plus-circle",
                        tooltip="Pago parcial",
                        color=COLORS["success"]["600"],
                        action=lambda: AppState.procesar_pago_parcial(payment['id'])
                    )
                ),
                
                rx.cond(
                    payment["estado_pago"] != "anulado",
                    action_button(
                        icon="x-circle",
                        tooltip="Anular",
                        color=COLORS["error"]["600"],
                        action=lambda: AppState.confirmar_anular_pago(payment['id'])
                    )
                ),
                
                spacing="1"
            ),
            style=DATA_CELL
        ),
        
        style=ROW_HOVER
    )


def payment_status_badge(estado: rx.Var) -> rx.Component:
    """Badge de estado del pago"""
    return rx.match(
        estado,
        ("completado", rx.badge("Completado", color_scheme="green", variant="soft")),
        ("pendiente", rx.badge("Pendiente", color_scheme="yellow", variant="soft")),  
        ("anulado", rx.badge("Anulado", color_scheme="red", variant="soft")),
        ("reembolsado", rx.badge("Reembolsado", color_scheme="gray", variant="soft")),
        rx.badge("Desconocido", color_scheme="gray", variant="soft")
    )


# ==========================================
# 📅 TABLA DE CONSULTAS
# ==========================================

def consultas_table() -> rx.Component:
    """Tabla de consultas elegante y funcional"""
    return rx.box(
        # Header

        
        # Filtros
        rx.hstack(
            crystal_search_input(
                placeholder="Buscar por paciente o motivo...",
                value=AppState.consultas_search,
                on_change=AppState.set_consultas_search
            ),
            
            filter_select(
                icon="activity",
                options=AppState.estados_consulta_options,
                value=AppState.consultas_filter_estado,
                on_change=AppState.set_consultas_filter_estado,
                placeholder="Estado"
            ),
            
            # Filtro de odontólogo usando directamente odontologos_list
            rx.hstack(
                rx.icon("user-md", size=18, color=COLORS["gray"]["500"]),
                rx.select.root(
                    rx.select.trigger(
                        placeholder="Odontólogo",
                        style=SELECT_STYLE,
                        width="200px"
                    ),
                    rx.select.content(
                        rx.select.item("Todos", value="Todos"),
                        rx.foreach(
                            AppState.odontologos_list,
                            lambda odontologo: rx.select.item(
                                f"{odontologo.primer_nombre} {odontologo.primer_apellido}".strip(),
                                value=odontologo.id
                            )
                        )
                    ),
                    value=AppState.consultas_filter_odontologo,
                    on_change=AppState.set_consultas_filter_odontologo,
                    size="3"
                ),
                spacing="2",
                align="center"
            ),
            rx.spacer(),
            primary_button(
                text="Nuevo Consulta",
                icon="plus",
                on_click=lambda: AppState.abrir_modal_consulta("crear"),
                size="lg"
            ),
            spacing="4",
            margin_bottom="6",
            wrap="wrap"
        ),
        
        # Tabla
        rx.cond(
            AppState.is_loading_consultas,
            loading_state("Cargando consultas..."),
            
            rx.cond(
                AppState.consultas_filtradas.length() > 0,
                
                # Tabla con datos
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("#", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Paciente", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Odontólogo", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Motivo", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Estado", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Acciones", style=COLUMN_HEADER),
                            )
                        ),
                        
                        rx.table.body(
                            rx.foreach(
                                AppState.consultas_filtradas,
                                lambda consulta, index: consulta_row(consulta, index)
                            )
                        ),
                    ),
                    style=TABLE_STYLE
                ),
                
                # Estado vacío
                empty_state(
                    "No hay consultas",
                    "Programa la primera consulta",
                    "calendar"
                )
            )
        ),
        
        class_name="space-y-6"
    )

def consulta_row(consulta: rx.Var[ConsultaModel], index: rx.Var[int]) -> rx.Component:
    """Fila de consulta elegante"""
    return rx.table.row(
        # Número
        rx.table.cell(
            rx.box(
                rx.text(f"#{index + 1}", size="3", weight="bold", color="white"),
                width="32px",
                height="32px",
                background=create_gradient(COLORS["secondary"]["500"], COLORS["secondary"]["600"]),
                border_radius=RADIUS["full"],
                display="flex",
                align_items="center",
                justify_content="center"
            ),
            style=DATA_CELL
        ),
        
        # Paciente
        rx.table.cell(
            rx.vstack(
                rx.text(
                    rx.cond(consulta.paciente_nombre, consulta.paciente_nombre, 'Sin paciente'),
                    size="3",
                    weight="medium"
                ),
                rx.text(
                    rx.cond(consulta.paciente_documento, f"CC: {consulta.paciente_documento}", "CC: Sin documento"),
                    size="2",
                    color=COLORS["gray"]["500"]
                ),
                spacing="1",
                align_items="start"
            ),
            style=DATA_CELL
        ),
        
        # Odontólogo
        rx.table.cell(
            rx.hstack(
                rx.box(
                    rx.icon("stethoscope", size=16, color=COLORS["success"]["600"]),
                    padding=SPACING["2"],
                    background=COLORS["success"]["100"],
                    border_radius=RADIUS["md"]
                ),
                rx.vstack(
                    rx.text(
                        rx.cond(consulta.odontologo_nombre, consulta.odontologo_nombre, 'Sin asignar'),
                        size="3",
                        weight="medium"
                    ),
                    rx.text(
                        rx.cond(consulta.odontologo_especialidad, consulta.odontologo_especialidad, 'General'),
                        size="2",
                        color=COLORS["gray"]["500"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                spacing="2"
            ),
            style=DATA_CELL
        ),
        
        # Motivo
        rx.table.cell(
            rx.text(
                rx.cond(consulta.motivo_consulta, consulta.motivo_consulta, 'Sin motivo'),
                size="3",
                max_width="200px",
                overflow="hidden",
                text_overflow="ellipsis"
            ),
            style=DATA_CELL
        ),
        
        # Estado
        rx.table.cell(
            consulta_status_badge(rx.cond(consulta.estado, consulta.estado, 'programada')),
            style=DATA_CELL
        ),
        
        # Acciones
        rx.table.cell(
            consulta_actions(consulta),
            style=DATA_CELL
        ),
        
        style=ROW_HOVER
    )

def consulta_status_badge(estado: rx.Var[str]) -> rx.Component:
    """Badge de estado de consulta"""
    return rx.badge(
        rx.hstack(
            rx.icon(
                rx.match(
                    estado,
                    ("programada", "clock"),
                    ("en_progreso", "play"),
                    ("completada", "check"),
                    ("cancelada", "x"),
                    "clock"
                ),
                size=12
            ),
            rx.text(
                rx.match(
                    estado,
                    ("programada", "Programada"),
                    ("en_progreso", "En Progreso"),
                    ("completada", "Completada"),
                    ("cancelada", "Cancelada"),
                    "Programada"
                )
            ),
            spacing="1"
        ),
        color_scheme=rx.match(
            estado,
            ("programada", "blue"),
            ("en_progreso", "yellow"),
            ("completada", "green"),
            ("cancelada", "red"),
            "gray"
        ),
        variant="soft",
        size="2"
    )

def consulta_actions(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """Acciones para consultas"""
    return rx.hstack(
        action_button(
            icon="pencil",
            tooltip="Editar",
            color=COLORS["blue"]["600"],
            action=lambda: AppState.abrir_modal_consulta(consulta.id)
        ),
        
        action_button(
            icon="play",
            tooltip="Iniciar",
            color=COLORS["warning"]["600"],
            action=lambda: AppState.iniciar_atencion_consulta(consulta.id)
        ),
        
        action_button(
            icon="check",
            tooltip="Completar",
            color=COLORS["success"]["600"],
            action=lambda: AppState.completar_consulta(consulta.id, {})
        ),
        
        action_button(
            icon="x",
            tooltip="Cancelar",
            color=COLORS["error"]["600"],
            action=lambda: AppState.confirmar_cancelar_consulta(consulta.id)
        ),
        
        spacing="1"
    )

# ==========================================
# 👨‍⚕️ TABLA DE PERSONAL
# ==========================================

def personal_table() -> rx.Component:
    """Tabla de personal elegante y funcional"""
    return rx.box(

        # Filtros
        rx.hstack(
            crystal_search_input(
                placeholder="Buscar por nombre, email o documento...",
                value=AppState.termino_busqueda_personal,
                on_change=AppState.buscar_personal
            ),
            
            # Filtros funcionales
            rx.hstack(
                # Filtro por tipo de cargo/rol
                rx.vstack(
                    rx.text("Cargo:", size="2", weight="medium", color="gray.700"),
                    rx.select(
                        ["todos", "Gerente", "Administrador", "Odontólogo", "Asistente"],
                        placeholder="Seleccionar cargo",
                        value=AppState.filtro_rol,
                        on_change=AppState.filtrar_por_rol,
                        width="150px"
                    ),
                    spacing="1",
                    align="start"
                ),
                
                # Filtro por estado
                rx.vstack(
                    rx.text("Estado:", size="2", weight="medium", color="gray.700"),
                    rx.select(
                        ["todos", "activos", "inactivos"],
                        placeholder="Seleccionar estado", 
                        value=AppState.filtro_estado_empleado,
                        on_change=AppState.filtrar_por_estado,
                        width="120px"
                    ),
                    spacing="1",
                    align="start"
                ),
                
                spacing="4",
                align="end"
            ),

            # Botón Nuevo Personal movido aquí
            rx.spacer(),
            primary_button(
                text="Nuevo Personal",
                icon="user-plus",
                on_click=lambda: AppState.seleccionar_y_abrir_modal_personal(""),
                size="lg"
            ),
            wrap="wrap",
            align="center",
        ),
        
        # Tabla
        rx.cond(
            AppState.cargando_lista_personal,
            loading_state("Cargando personal..."),
            
            rx.cond(
                AppState.personal_filtrado.length() > 0,
                
                # Tabla con datos
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Nombre", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Documento", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Cargo", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Especialidad", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Estado", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Contacto", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Acciones", style=COLUMN_HEADER),
                            )
                        ),
                        
                        rx.table.body(
                            rx.foreach(
                                AppState.personal_filtrado,
                                personal_row
                            )
                        ),
                    ),
                    style=TABLE_STYLE
                ),
                
                # Estado vacío
                empty_state(
                    "No hay personal",
                    "Agrega tu primer empleado",
                    "briefcase"
                )
            )
        ),
        class_name="space-y-6",
        padding="20px"
    )

def personal_row(personal: rx.Var[PersonalModel]) -> rx.Component:
    """Fila de personal elegante"""
    return rx.table.row(
        # Nombre
        rx.table.cell(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        f"{personal.primer_nombre} {personal.primer_apellido}",
                        size="3",
                        weight="medium",
                        color=DARK_THEME["colors"]["text_primary"]
                    ),
                    rx.text(
                        personal.usuario.email,
                        size="2",
                        color=DARK_THEME["colors"]["text_secondary"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                spacing="3"
            ),
            style=DATA_CELL
        ),
        
        # Documento
        rx.table.cell(
            rx.box(
                rx.text(
                    f"{personal.tipo_documento}-{personal.numero_documento}",
                    size="3",
                    font_family=TYPOGRAPHY["font_family"]["mono"],
                    color=DARK_THEME["colors"]["text_primary"],
                    weight="medium"
                ),

            ),
            style=DATA_CELL
        ),
        
        # Cargo
        rx.table.cell(
            personal_type_badge(personal.tipo_personal),
            style=DATA_CELL
        ),
        
        # Especialidad
        rx.table.cell(
            rx.cond(
                personal.especialidad,
                rx.text(
                    personal.especialidad, 
                    size="3",
                    color=DARK_THEME["colors"]["text_primary"],
                    weight="medium"
                ),
                rx.text(
                    "General", 
                    size="3", 
                    color=DARK_THEME["colors"]["text_muted"],
                    style={"font_style": "italic"}
                )
            ),
            style=DATA_CELL
        ),
        
        # Estado
        rx.table.cell(
            personal_status_badge(personal.estado_laboral),
            style=DATA_CELL
        ),
        
        # Contacto
        rx.table.cell(
            rx.cond(
                personal.celular,
                rx.hstack(
                    rx.icon("phone", size=16, color=COLORS["success"]["400"]),
                    rx.text(
                        personal.celular,
                        size="3",
                        color=DARK_THEME["colors"]["text_primary"],
                        weight="medium"
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("phone-off", size=16, color=DARK_THEME["colors"]["text_muted"]),
                    rx.text(
                        "Sin celular", 
                        size="3", 
                        color=DARK_THEME["colors"]["text_muted"],
                        style={"font_style": "italic"}
                    ),
                    spacing="2",
                    align="center"
                )
            ),
            style=DATA_CELL
        ),
        
        # Acciones
        rx.table.cell(
            rx.hstack(
                action_button(
                    icon="pencil",
                    tooltip="Editar",
                    color=COLORS["blue"]["600"],
                    action=lambda: AppState.seleccionar_y_abrir_modal_personal(personal.id)
                ),
                
                rx.cond(
                    personal.estado_laboral == "activo",
                    action_button(
                        icon="user-x",
                        tooltip="Desactivar",
                        color=COLORS["error"]["600"],
                        action=lambda: AppState.seleccionar_personal_para_eliminar(personal.id)
                    ),
                    action_button(
                        icon="user-check",
                        tooltip="Reactivar",
                        color=COLORS["success"]["600"],
                        action=lambda: AppState.activar_desactivar_empleado(personal.id, True)
                    )
                ),
                align="center",
                spacing="2"
            ),
            style=DATA_CELL
        ),
        
        style=ROW_HOVER
    )

def personal_type_badge(tipo: rx.Var[str]) -> rx.Component:
    """Badge de tipo de personal con colores distintivos"""
    return rx.box(
        rx.hstack(
            rx.icon(
                rx.match(
                    tipo,
                    ("Odontólogo", "stethoscope"),
                    ("Administrador", "briefcase"),
                    ("Asistente", "user"),
                    ("Gerente", "crown"),
                    "user"
                ),
                size=14,
                color="white"
            ),
            rx.text(
                tipo,
                color="white",
                weight="medium",
                size="2"
            ),
            spacing="2",
            align="center"
        ),
        style={
            "background": rx.match(
                tipo,
                ("Odontólogo", f"linear-gradient(135deg, {COLORS['success']['500']}40 0%, {COLORS['success']['600']}80 100%)"),
                ("Administrador", f"linear-gradient(135deg, {COLORS['blue']['500']}40 0%, {COLORS['blue']['600']}80 100%)"),
                ("Asistente", f"linear-gradient(135deg, {COLORS['warning']['500']}40 0%, {COLORS['warning']['600']}80 100%)"),
                ("Gerente", f"linear-gradient(135deg, {COLORS['secondary']['500']}40 0%, {COLORS['secondary']['600']}80 100%)"),
                f"linear-gradient(135deg, {COLORS['gray']['500']} 0%, {COLORS['gray']['600']} 100%)"
            ),
            "padding": f"{SPACING['1']} {SPACING['3']}",
            "border_radius": RADIUS["full"],
            "box_shadow": rx.match(
                tipo,
                ("Odontólogo", f"0 2px 8px {COLORS['success']['500']}40"),
                ("Administrador", f"0 2px 8px {COLORS['blue']['500']}40"),
                ("Asistente", f"0 2px 8px {COLORS['warning']['500']}40"),
                ("Gerente", f"0 2px 8px {COLORS['secondary']['500']}40"),
                f"0 2px 8px {COLORS['gray']['500']}40"
            ),
            "border": "1px solid rgba(255, 255, 255, 0.2)",
            "backdrop_filter": "blur(10px)"
        }
    )

def personal_status_badge(estado: rx.Var[str]) -> rx.Component:
    """Badge de estado laboral"""
    return rx.badge(
        rx.hstack(
            rx.text(
                rx.match(
                    estado,
                    ("activo", "Activo"),
                    ("inactivo", "Inactivo"),
                    ("vacaciones", "Vacaciones"),
                    "Activo"
                )
            ),
            spacing="1"
        ),
        color_scheme=rx.match(
            estado,
            ("activo", "green"),
            ("inactivo", "red"),
            ("vacaciones", "yellow"),
            "gray"
        ),
        color="white",
        variant="soft",
        size="2"
    )

# ==========================================
# 📤 EXPORTS
# ==========================================

__all__ = [
    "patients_table",
    "consultas_table", 
    "personal_table"
]