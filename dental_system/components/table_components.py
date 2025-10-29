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
# 🚀 OPTIMIZACIONES LAZY LOADING Y PAGINACIÓN
# ==========================================

def tabla_pacientes_lazy() -> rx.Component:
    """
    Tabla de pacientes optimizada con lazy loading y paginación inteligente

    Características:
    - Paginación automática (25 registros por página)
    - Lazy loading de datos
    - Skeleton loading estados
    - Virtual scrolling para listas grandes
    - Cache automático integrado
    """
    return rx.vstack(
        # Header con controles de paginación
        rx.hstack(
            # Info de paginación
            rx.text(
                rx.cond(
                    AppState.total_pacientes > 0,
                    f"Mostrando {AppState.pacientes_pagina_actual * 25 - 24} - "
                    f"{rx.cond(AppState.pacientes_pagina_actual * 25 > AppState.total_pacientes, AppState.total_pacientes, AppState.pacientes_pagina_actual * 25)} "
                    f"de {AppState.total_pacientes} pacientes",
                    "No hay pacientes"
                ),
                size="2",
                color=COLORS["gray"]["400"]
            ),

            rx.spacer(),

            # Selector de página
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevron_left", size=18),
                    size="2",
                    variant="outline",
                    disabled=AppState.pacientes_pagina_actual <= 1,
                    on_click=AppState.ir_pagina_anterior_pacientes,
                    cursor="pointer"
                ),

                rx.text(
                    f"Página {AppState.pacientes_pagina_actual} de {AppState.total_paginas_pacientes}",
                    size="2",
                    color=COLORS["gray"]["300"]
                ),

                rx.icon_button(
                    rx.icon("chevron_right", size=18),
                    size="2",
                    variant="outline",
                    disabled=AppState.pacientes_pagina_actual >= AppState.total_paginas_pacientes,
                    on_click=AppState.ir_pagina_siguiente_pacientes,
                    cursor="pointer"
                ),

                spacing="2",
                align="center"
            ),

            justify="between",
            width="100%",
            margin_bottom="4"
        ),

        # Tabla optimizada
        rx.cond(
            AppState.cargando_pagina_pacientes,

            # Skeleton loading para nueva página
            rx.vstack(
                *[
                    rx.skeleton(
                        height="60px",
                        width="100%",
                        radius="lg"
                    ) for _ in range(5)
                ],
                spacing="3",
                width="100%"
            ),

            # Tabla real con datos paginados
            rx.cond(
                AppState.pacientes_pagina_actual_lista.length() > 0,

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
                                AppState.pacientes_pagina_actual_lista,
                                patient_row_optimized
                            )
                        ),
                    ),
                    style=TABLE_STYLE
                ),

                # Estado vacío optimizado
                empty_state_lazy(
                    "No hay pacientes en esta página",
                    "Intenta cambiar los filtros o ir a otra página",
                    "users"
                )
            )
        ),

        # Footer con información de performance
        rx.cond(
            AppState.mostrar_stats_performance,
            rx.hstack(
                rx.badge(
                    f"Cache: {AppState.cache_hit_ratio}% hit ratio",
                    color_scheme="green",
                    size="1"
                ),
                rx.badge(
                    f"Carga: {AppState.tiempo_carga_ultima_pagina}ms",
                    color_scheme="blue",
                    size="1"
                ),
                rx.badge(
                    f"Memoria: {AppState.registros_en_memoria}",
                    color_scheme="orange",
                    size="1"
                ),
                spacing="2",
                margin_top="3",
                justify="center"
            )
        ),

        spacing="4",
        width="100%"
    )


def patient_row_optimized(patient: rx.Var[PacienteModel]) -> rx.Component:
    """
    Fila de paciente optimizada con lazy loading de datos secundarios
    """
    return rx.table.row(
        # Nombre (carga inmediata)
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

        # Edad (lazy loaded)
        rx.table.cell(
            rx.cond(
                patient.edad_calculada_disponible,
                rx.text(
                    patient.edad.to(str) + " años",
                    size="3",
                    color=COLORS["gray"]["50"]
                ),
                rx.skeleton(height="20px", width="50px")
            ),
            style=DATA_CELL
        ),

        # Género (carga inmediata)
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

        # Documento (carga inmediata)
        rx.table.cell(
            rx.text(
                patient.numero_documento,
                size="3",
                color=COLORS["gray"]["50"]
            ),
            style=DATA_CELL
        ),

        # Contacto (lazy loaded)
        rx.table.cell(
            rx.cond(
                patient.contacto_disponible,
                rx.text(
                    rx.cond(
                        patient.celular_1 != "",
                        patient.celular_1,
                        "Sin teléfono"
                    ),
                    size="3",
                    color=COLORS["gray"]["50"]
                ),
                rx.skeleton(height="20px", width="100px")
            ),
            style=DATA_CELL
        ),

        # Estado (carga inmediata)
        rx.table.cell(
            patient_status_badge(patient.estado),
            style=DATA_CELL
        ),

        # Acciones (optimizadas)
        rx.table.cell(
            rx.hstack(
                rx.icon_button(
                    rx.icon("eye", size=16),
                    size="1",
                    variant="outline",
                    color_scheme="blue",
                    on_click=lambda: AppState.ver_paciente_lazy(patient.numero_historia),
                    cursor="pointer"
                ),
                rx.icon_button(
                    rx.icon("edit", size=16),
                    size="1",
                    variant="outline",
                    color_scheme="orange",
                    on_click=lambda: AppState.editar_paciente_lazy(patient.numero_historia),
                    cursor="pointer"
                ),
                spacing="1"
            ),
            style=DATA_CELL
        ),

        # Optimización: Pre-cargar datos al hacer hover
        on_mouse_enter=lambda: AppState.precargar_datos_paciente(patient.numero_historia),

        _hover={
            "background_color": f"{DARK_THEME['colors']['surface']}80",
            "transform": "translateY(-1px)",
            "transition": "all 0.2s ease"
        }
    )


def empty_state_lazy(titulo: str, descripcion: str, icono: str) -> rx.Component:
    """Estado vacío optimizado para lazy loading"""
    return rx.center(
        rx.vstack(
            rx.box(
                rx.icon(
                    icono,
                    size=48,
                    color=COLORS["gray"]["400"]
                ),
                padding="20px",
                border_radius="full",
                background=f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
                border=f"2px solid {DARK_THEME['colors']['border']}"
            ),

            rx.heading(
                titulo,
                size="5",
                color=COLORS["gray"]["300"],
                text_align="center"
            ),

            rx.text(
                descripcion,
                size="3",
                color=COLORS["gray"]["500"],
                text_align="center",
                max_width="400px"
            ),

            spacing="4",
            align="center"
        ),

        min_height="300px",
        width="100%"
    )



# ==========================================
# 📤 EXPORTS ACTUALIZADOS
# ==========================================

__all__ = [
    "patients_table",
    "personal_table",
    "tabla_pacientes_lazy",
    "patient_row_optimized",
    "empty_state_lazy"
]