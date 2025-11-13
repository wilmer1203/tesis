import reflex as rx
from typing import List
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button
from dental_system.models.personal_models import PersonalModel
from dental_system.models.pacientes_models import PacienteModel
# Importar sistema de temas
from dental_system.styles.themes import (
    COLORS, SHADOWS, RADIUS, SPACING, TYPOGRAPHY, 
    ANIMATIONS, DARK_THEME
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
        "box_shadow": f"0 0 0 3px {COLORS['primary']['200']}"
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

# def status_badge(is_active: bool, active_text: str = "Activo", inactive_text: str = "Inactivo") -> rx.Component:
#     """Badge de estado elegante"""
#     return rx.badge(
#         rx.hstack(
#             rx.icon(
#                 rx.cond(is_active, "check", "x"),
#                 size=14
#             ),
#             rx.text(rx.cond(is_active, active_text, inactive_text)),
#             spacing="1"
#         ),
#         color_scheme=rx.cond(is_active, "green", "red"),
#         variant="soft",
#         size="2"
#     )

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
            rx.spacer(),
            primary_button(
                text="Nuevo Paciente",
                icon="plus",
                on_click=lambda: AppState.seleccionar_y_abrir_modal_paciente(""),
                size="lg"
            ),
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
                patient.fecha_nacimiento,
                rx.text(
                    patient.fecha_nacimiento.to(str),
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
                # Botón Ver Historial
                action_button(
                    icon="file-text",
                    tooltip="Ver Historial Completo",
                    color=COLORS["primary"]["500"],
                    action=lambda: AppState.navegar_a_historial_paciente(patient.id)
                ),

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
                                rx.table.column_header_cell("Nombre"),
                                rx.table.column_header_cell("Documento"),
                                rx.table.column_header_cell("Cargo"),
                                rx.table.column_header_cell("Especialidad"),
                                rx.table.column_header_cell("Estado"),
                                rx.table.column_header_cell("Contacto"),
                                rx.table.column_header_cell("Acciones"),
                            ),
                            style=COLUMN_HEADER
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
                        color=COLORS["gray"]["100"]  # Texto principal claro
                    ),
                    rx.text(
                        personal.usuario.email,
                        size="2",
                        color=COLORS["gray"]["300"]  # Texto secundario
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
                    font_family="monospace",  # Familia mono simplificada
                    color=COLORS["gray"]["100"],  # Texto principal claro
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
                    color=COLORS["gray"]["100"],  # Texto principal claro
                    weight="medium"
                ),
                rx.text(
                    "General", 
                    size="3", 
                    color=COLORS["gray"]["500"],  # Texto muted
                    style={"font_style": "italic"}
                )
            ),
            style=DATA_CELL
        ),
        
        # Estado
        rx.table.cell(
            status_badge(personal.estado_laboral),
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
                        color=COLORS["gray"]["100"],  # Texto principal claro
                        weight="medium"
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("phone-off", size=16, color=COLORS["gray"]["500"]),  # Icono muted
                    rx.text(
                        "Sin celular", 
                        size="3", 
                        color=COLORS["gray"]["500"],  # Texto muted
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
                        tooltip="Inhabilitar",
                        color=COLORS["error"]["600"],
                        action=lambda: AppState.activar_desactivar_empleado(personal.id, False)
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
                ("Asistente", f"linear-gradient(135deg, {COLORS['warning']['500']}40 0%, {COLORS['warning']['700']}80 100%)"),  # warning 700 existe
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

def status_badge(estado: rx.Var[str]) -> rx.Component:
    """Badge de estado laboral"""
    return rx.badge(
        rx.hstack(
            rx.text(
                rx.match(
                    estado,
                    ("activo", "Activo"),
                    ("inactivo", "Inactivo"),
                    "Activo"
                )
            ),
            spacing="1"
        ),
        color_scheme=rx.match(
            estado,
            ("activo", "green"),
            ("inactivo", "red"),
            "green"
        ),
        color="white",
        variant="soft",
        size="2"
    )



def servicios_table() -> rx.Component:
    """📋 Tabla principal de servicios con glassmorphism"""
    return rx.box(

        # Filtros
        rx.hstack(
            crystal_search_input(
                placeholder="Buscar servicios por nombre o descripción...",
                value=AppState.termino_busqueda_servicios,
                on_change=AppState.buscar_servicios,
            ),

            # Filtros funcionales
            rx.hstack(
                # Filtro por categoría
                rx.vstack(
                    rx.text("Categoría", size="2", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.select(
                        AppState.categorias_servicios,
                        value=AppState.filtro_categoria,
                        on_change=AppState.filtrar_por_categoria,
                        placeholder="Todas las categorías",
                        width="150px"
                    ),
                    spacing="1",
                    align="start"
                ),

                # Filtro por estado
                rx.vstack(
                    rx.text("Estado", size="2", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.select(
                        ["todos", "activos", "inactivos"],
                        value=AppState.filtro_estado_servicio,
                        on_change=AppState.filtrar_por_estado_servicio,
                        placeholder="Todos los estados",
                        width="150px"
                    ),
                    spacing="1",
                    align="start"
                ),

                spacing="4",
                align="end"
            ),
            rx.spacer(),
            primary_button(
                text="Nuevo Servicio",
                icon="plus",
                on_click=lambda: AppState.seleccionar_y_abrir_modal_servicio(""),
                size="lg"
            ),
            wrap="wrap",
            align="center",
        ),


        # Tabla
        rx.cond(
            AppState.cargando_lista_servicios,
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
                                rx.table.column_header_cell("Alcance", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Estado", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Acciones", style=COLUMN_HEADER),
                            )
                        ),

                        rx.table.body(
                            rx.foreach(
                                AppState.servicios_filtrados,
                                servicio_row
                            )
                        ),
                    ),
                    style=TABLE_STYLE
                ),

                # Estado vacío
                empty_state(
                    "No hay servicios",
                    "Agrega tu primer servicio odontológico",
                    "clipboard-list"
                )
            )
        ),
        class_name="space-y-6",
        padding="20px"

    )

def servicio_row(servicio) -> rx.Component:
    """🔗 Fila de servicio en tabla - estilo consistente con personal_row"""
    return rx.table.row(
        # Código
        rx.table.cell(
            rx.box(
                rx.text(
                    servicio.codigo,
                    size="3",
                    font_family=TYPOGRAPHY["font_family"]["mono"],
                    color=COLORS["primary"]["400"],
                    weight="medium"
                ),
                padding=SPACING["2"],
                background=COLORS["gray"]["800"],
                border_radius=RADIUS["md"]
            ),
            style=DATA_CELL
        ),

        # Nombre y descripción
        rx.table.cell(
            rx.vstack(
                rx.text(
                    servicio.nombre,
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["100"]
                ),
                rx.text(
                    servicio.descripcion,
                    size="2",
                    color=COLORS["gray"]["400"],
                    style={
                        "overflow": "hidden",
                        "text_overflow": "ellipsis",
                        "white_space": "nowrap",
                        "max_width": "250px"
                    }
                ),
                spacing="1",
                align_items="start"
            ),
            style=DATA_CELL
        ),

        # Categoría
        rx.table.cell(
            servicio_categoria_badge(servicio.categoria),
            style=DATA_CELL
        ),

        # Precio
        rx.table.cell(
            rx.hstack(
                rx.icon("dollar-sign", size=16, color=COLORS["warning"]["400"]),
                rx.text(
                    f"${servicio.precio_base_usd:,.0f}",
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["100"]
                ),
                spacing="2",
                align="center"
            ),
            style=DATA_CELL
        ),

        # Alcance
        rx.table.cell(
            rx.text(
                servicio.alcance_servicio,
                size="3",
                color=COLORS["gray"]["100"],
                weight="medium"
            ),
            style=DATA_CELL
        ),

        # Estado
        rx.table.cell(
            status_badge(rx.cond(servicio.activo, "activo","inactivo")),
            style=DATA_CELL
        ),

        # Acciones
        rx.table.cell(
            rx.hstack(
                action_button(
                    icon="pencil",
                    tooltip="Editar",
                    color=COLORS["blue"]["600"],
                    action=lambda: AppState.seleccionar_y_abrir_modal_servicio(servicio.id)
                ),

                rx.cond(
                    servicio.activo,
                    action_button(
                        icon="eye-off",
                        tooltip="Desactivar",
                        color=COLORS["error"]["600"],
                        action=lambda: AppState.activar_desactivar_servicio(servicio.id, False)
                    ),
                    action_button(
                        icon="eye",
                        tooltip="Reactivar",
                        color=COLORS["success"]["600"],
                        action=lambda: AppState.activar_desactivar_servicio(servicio.id, True)
                    )
                ),
                align="center",
                spacing="2"
            ),
            style=DATA_CELL,
            display=rx.cond(AppState.rol_usuario == "gerente", "table-cell", "none")
        ),

        style=ROW_HOVER
    )

def servicio_categoria_badge(categoria: rx.Var[str]) -> rx.Component:
    """Badge de categoría de servicio con colores distintivos"""
    return rx.box(
        rx.hstack(
            rx.icon(
                rx.match(
                    categoria,
                    ("Preventiva", "shield-check"),
                    ("Restaurativa", "wrench"),
                    ("Endodoncia", "activity"),
                    ("Cirugía", "scissors"),
                    ("Prótesis", "box"),
                    ("Estética", "sparkles"),
                    ("Implantología", "anchor"),
                    ("Diagnóstico", "search"),
                    ("Consulta", "clipboard-list"),
                    "stethoscope"
                ),
                size=14,
                color="white"
            ),
            rx.text(
                categoria,
                color="white",
                weight="medium",
                size="2"
            ),
            spacing="2",
            align="center"
        ),
        style={
            "background": rx.match(
                categoria,
                ("Preventiva", f"linear-gradient(135deg, {COLORS['success']['500']}40 0%, {COLORS['success']['600']}80 100%)"),
                ("Restaurativa", f"linear-gradient(135deg, {COLORS['blue']['500']}40 0%, {COLORS['blue']['600']}80 100%)"),
                ("Endodoncia", f"linear-gradient(135deg, {COLORS['warning']['500']}40 0%, {COLORS['warning']['700']}80 100%)"),
                ("Cirugía", f"linear-gradient(135deg, {COLORS['error']['500']}40 0%, {COLORS['error']['600']}80 100%)"),
                ("Prótesis", f"linear-gradient(135deg, {COLORS['secondary']['500']}40 0%, {COLORS['secondary']['600']}80 100%)"),
                ("Estética", f"linear-gradient(135deg, {COLORS['primary']['500']}40 0%, {COLORS['primary']['600']}80 100%)"),
                ("Implantología", f"linear-gradient(135deg, {COLORS['gray']['500']}40 0%, {COLORS['gray']['600']}80 100%)"),
                ("Diagnóstico", f"linear-gradient(135deg, {COLORS['primary']['400']}40 0%, {COLORS['blue']['500']}80 100%)"),
                ("Consulta", f"linear-gradient(135deg, {COLORS['gray']['400']}40 0%, {COLORS['gray']['500']}80 100%)"),
                f"linear-gradient(135deg, {COLORS['gray']['500']} 0%, {COLORS['gray']['600']} 100%)"
            ),
            "padding": f"{SPACING['1']} {SPACING['3']}",
            "border_radius": RADIUS["full"],
            "box_shadow": rx.match(
                categoria,
                ("Preventiva", f"0 2px 8px {COLORS['success']['500']}40"),
                ("Restaurativa", f"0 2px 8px {COLORS['blue']['500']}40"),
                ("Endodoncia", f"0 2px 8px {COLORS['warning']['500']}40"),
                ("Cirugía", f"0 2px 8px {COLORS['error']['500']}40"),
                ("Prótesis", f"0 2px 8px {COLORS['secondary']['500']}40"),
                ("Estética", f"0 2px 8px {COLORS['primary']['500']}40"),
                f"0 2px 8px {COLORS['gray']['500']}40"
            ),
            "border": "1px solid rgba(255, 255, 255, 0.2)",
            "backdrop_filter": "blur(10px)"
        }
    )

# ==========================================
# 💳 TABLA DE PAGOS - HISTORIAL
# ==========================================

def pago_estado_badge(estado: rx.Var[str]) -> rx.Component:
    """Badge de estado de pago con iconos distintivos"""
    return rx.box(
        rx.hstack(
            rx.icon(
                rx.match(
                    estado,
                    ("completado", "check-circle"),
                    ("pendiente", "clock"),
                    ("anulado", "x-circle"),
                    "help-circle"
                ),
                size=14,
                color="white"
            ),
            rx.text(
                rx.match(
                    estado,
                    ("completado", "Pagado"),
                    ("pendiente", "Pendiente"),
                    ("anulado", "Anulado"),
                    estado
                ),
                color="white",
                weight="medium",
                size="2"
            ),
            spacing="2",
            align="center"
        ),
        style={
            "background": rx.match(
                estado,
                ("completado", f"linear-gradient(135deg, {COLORS['success']['500']} 0%, {COLORS['success']['600']} 100%)"),
                ("pendiente", f"linear-gradient(135deg, {COLORS['warning']['500']} 0%, {COLORS['warning']['700']} 100%)"),
                ("anulado", f"linear-gradient(135deg, {COLORS['error']['500']} 0%, {COLORS['error']['600']} 100%)"),
                f"linear-gradient(135deg, {COLORS['gray']['500']} 0%, {COLORS['gray']['600']} 100%)"
            ),
            "padding": f"{SPACING['1']} {SPACING['3']}",
            "border_radius": RADIUS["full"],
            "box_shadow": rx.match(
                estado,
                ("completado", f"0 2px 8px {COLORS['success']['500']}40"),
                ("pendiente", f"0 2px 8px {COLORS['warning']['500']}40"),
                ("anulado", f"0 2px 8px {COLORS['error']['500']}40"),
                "none"
            ),
            "border": "1px solid rgba(255, 255, 255, 0.2)",
            "backdrop_filter": "blur(10px)"
        }
    )

def pago_row(pago) -> rx.Component:
    """🔗 Fila de pago en tabla - estilo consistente con otras tablas"""
    return rx.table.row(
        # Número de recibo
        rx.table.cell(
            rx.box(
                rx.text(
                    pago["numero_recibo"],
                    size="3",
                    font_family=TYPOGRAPHY["font_family"]["mono"],
                    color=COLORS["primary"]["400"],
                    weight="medium"
                ),
                padding=SPACING["2"],
                background=COLORS["gray"]["800"],
                border_radius=RADIUS["md"]
            ),
            style=DATA_CELL
        ),

        # Paciente (nombre + documento)
        rx.table.cell(
            rx.vstack(
                rx.text(
                    pago["paciente_nombre"],
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["100"]
                ),
                rx.text(
                    pago["paciente_documento"],
                    size="2",
                    color=COLORS["gray"]["400"]
                ),
                spacing="1",
                align_items="start"
            ),
            style=DATA_CELL
        ),

        # Monto USD
        rx.table.cell(
            rx.cond(
                pago["monto_pagado_usd"].to(float) > 0,
                rx.hstack(
                    rx.icon("dollar-sign", size=16, color=COLORS["success"]["400"]),
                    rx.text(
                        f"${pago['monto_pagado_usd']}",
                        size="3",
                        weight="medium",
                        color=COLORS["gray"]["100"]
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.text("-", size="2", color=COLORS["gray"]["600"])
            ),
            style=DATA_CELL
        ),

        # Monto BS
        rx.table.cell(
            rx.cond(
                pago["monto_pagado_bs"].to(float) > 0,
                rx.hstack(
                    rx.icon("banknote", size=16, color=COLORS["warning"]["400"]),
                    rx.text(
                        f"{pago['monto_pagado_bs']:,.0f} Bs",
                        size="3",
                        weight="medium",
                        color=COLORS["gray"]["100"]
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.text("-", size="2", color=COLORS["gray"]["600"])
            ),
            style=DATA_CELL
        ),

        # Estado
        rx.table.cell(
            pago_estado_badge(pago["estado_pago"]),
            style=DATA_CELL
        ),

        # Fecha (formateada a YYYY-MM-DD)
        rx.table.cell(
            rx.text(
                "texto de fecha",
                # pago["fecha_pago"].split("T")[0] if "T" in pago["fecha_pago"] else pago["fecha_pago"],
                size="3",
                color=COLORS["gray"]["100"],
                font_family=TYPOGRAPHY["font_family"]["mono"]
            ),
            style=DATA_CELL
        ),

        # Acciones
        rx.table.cell(
            rx.hstack(
                action_button(
                    icon="eye",
                    tooltip="Ver detalles",
                    color=COLORS["blue"]["600"],
                    action=lambda: AppState.ver_detalle_pago(pago["id"])
                ),
                action_button(
                    icon="printer",
                    tooltip="Imprimir recibo",
                    color=COLORS["gray"]["600"],
                    action=lambda: AppState.imprimir_recibo(pago["id"])
                ),
                align="center",
                spacing="2"
            ),
            style=DATA_CELL
        ),

        style=ROW_HOVER
    )

def pagos_table() -> rx.Component:
    """📋 Tabla de historial de pagos con componentes reutilizables"""
    return rx.box(
        # Header
        rx.hstack(
            rx.hstack(
                rx.icon("receipt", size=24, color=COLORS["primary"]["500"]),
                rx.heading("Historial de Pagos", size="5", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
                rx.badge(
                    f"{AppState.lista_pagos.length()} pagos",
                    color_scheme="cyan",
                    variant="soft"
                ),
                spacing="3",
                align="center"
            ),
            rx.spacer(),

            # Búsqueda
            crystal_search_input(
                placeholder="Buscar por paciente o recibo...",
                value=AppState.termino_busqueda_pagos,
                on_change=AppState.buscar_pagos
            ),

            # Botón exportar (solo icono)
            rx.tooltip(
                rx.button(
                    rx.icon("download", size=18),
                    on_click=AppState.exportar_pagos,
                    variant="soft",
                    color_scheme="cyan",
                    size="2",
                    style={
                        "cursor": "pointer",
                        "transition": "all 0.2s ease",
                        "_hover": {
                            "transform": "translateY(-2px)",
                            "box_shadow": f"0 4px 12px {COLORS['primary']['500']}30"
                        }
                    }
                ),
                content="Exportar pagos"
            ),

            wrap="wrap",
            align="center",
            spacing="4",
            width="100%"
        ),

        # Tabla con scroll vertical
        rx.cond(
            AppState.cargando_lista_pagos,
            loading_state("Cargando pagos..."),

            rx.cond(
                AppState.pagos_historial_formateados.length() > 0,

                # Tabla con datos y scroll
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Recibo", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Paciente", style=COLUMN_HEADER),
                                rx.table.column_header_cell("USD", style=COLUMN_HEADER),
                                rx.table.column_header_cell("BS", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Estado", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Fecha", style=COLUMN_HEADER),
                                rx.table.column_header_cell("Acciones", style=COLUMN_HEADER)
                            )
                        ),

                        rx.table.body(
                            rx.foreach(
                                AppState.pagos_historial_formateados,
                                pago_row
                            )
                        )
                    ),
                    style={
                        **TABLE_STYLE,
                        "max_height": "calc(100vh - 450px)",  # Altura máxima
                        "overflow_y": "auto",  # Scroll vertical
                        "overflow_x": "hidden",
                        # Estilos del scrollbar
                        "::-webkit-scrollbar": {
                            "width": "8px"
                        },
                        "::-webkit-scrollbar-track": {
                            "background": COLORS["gray"]["900"],
                            "border_radius": "4px"
                        },
                        "::-webkit-scrollbar-thumb": {
                            "background": COLORS["primary"]["600"],
                            "border_radius": "4px"
                        },
                        "::-webkit-scrollbar-thumb:hover": {
                            "background": COLORS["primary"]["500"]
                        }
                    }
                ),

                # Estado vacío
                empty_state(
                    "No hay pagos registrados",
                    "Los pagos procesados aparecerán aquí",
                    "receipt"
                )
            )
        ),

        class_name="space-y-6",
        padding="20px"
    )

# ==========================================
# 📤 EXPORTS ACTUALIZADOS
# ==========================================

__all__ = [
    "patients_table",
    "personal_table",
    "servicios_table",
    "pagos_table",
    "pago_row",
    "pago_estado_badge",
]

