"""
Componentes para gestión de consultas - Siguiendo el patrón de pacientes
Para crear en: dental_system/pages/admin/consultas/list.py
"""

import reflex as rx
from dental_system.components.role_specific.boss import (
    modal_overlay,
    form_field,
    success_alert,
    error_alert,
    loading_spinner,
    main_header,
)
from dental_system.components.common import (
    stat_card, 
    primary_button, 
    secondary_button, 
    eliminar_button
)
from dental_system.state.admin_state import AdminState
from dental_system.models import ConsultaModel
from dental_system.styles.themes import COLORS

# ==========================================
# MODAL DE CONSULTA
# ==========================================

def consulta_modal() -> rx.Component:
    """Modal para crear/editar consulta"""
    return modal_overlay(
        AdminState.show_consulta_modal,
        rx.box(
            # Header del modal
            rx.hstack(
                rx.text(
                    rx.cond(
                        AdminState.selected_consulta.length() > 0,
                        "Editar Consulta",
                        "Nueva Consulta"
                    ),
                    size="6",
                    weight="bold",
                    color=COLORS["gray"]["800"]
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("x", size=20),
                    background="transparent",
                    border="none",
                    cursor="pointer",
                    on_click=AdminState.close_consulta_modal,
                    _hover={"background": COLORS["gray"]["100"]}
                ),
                align="center",
                width="100%"
            ),
            
            # Alertas
            success_alert(AdminState.success_message),
            error_alert(AdminState.error_message),
            
            # Formulario
            rx.form(
                rx.vstack(
                    # SECCIÓN 1: INFORMACIÓN PRINCIPAL
                    rx.text("Información de la Consulta", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    # Selección de Paciente
                    rx.vstack(
                        rx.text("Paciente *", size="3", weight="medium", color=COLORS["gray"]["700"]),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Seleccionar paciente",
                                width="100%"
                            ),
                            rx.select.content(
                                rx.foreach(
                                    AdminState.pacientes_list,
                                    lambda paciente: rx.select.item(
                                        f"{paciente.primer_nombre} {paciente.primer_apellido} - {paciente.numero_documento}".split(),
                                        value=paciente.id
                                    )
                                )
                            ),
                            value=AdminState.consulta_form["paciente_id"],
                            on_change=lambda val: AdminState.update_consulta_form("paciente_id", val),
                            width="100%"
                        ),
                        spacing="1",
                        align_items="start",
                        width="100%"
                    ),
                    
                    # Selección de Odontólogo
                    rx.vstack(
                        rx.text("Odontólogo *", size="3", weight="medium", color=COLORS["gray"]["700"]),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Seleccionar odontólogo",
                                width="100%"
                            ),
                            rx.select.content(
                                rx.foreach(
                                    AdminState.odontologos_list,
                                    lambda odontologo: rx.select.item(
                                        f"{odontologo.primer_nombre} {odontologo.primer_apellido} - {odontologo.especialidad}".split(),
                                        value=odontologo.id
                                    )
                                )
                            ),
                            value=AdminState.consulta_form["odontologo_id"],
                            on_change=lambda val: AdminState.update_consulta_form("odontologo_id", val),
                            width="100%"
                        ),
                        spacing="1",
                        align_items="start",
                        width="100%"
                    ),
                    
                    # Configuración de la consulta
                    rx.grid(
                        form_field(
                            "Tipo de Consulta",
                            "tipo_consulta",
                            AdminState.consulta_form["tipo_consulta"],
                            AdminState.update_consulta_form,
                            field_type="select",
                            options=["general", "control", "urgencia", "cirugia", "otro"],
                            required=True
                        ),
                        form_field(
                            "Prioridad",
                            "prioridad",
                            AdminState.consulta_form["prioridad"],
                            AdminState.update_consulta_form,
                            field_type="select",
                            options=["normal", "alta", "urgente"],
                            required=True
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    # SECCIÓN 2: INFORMACIÓN CLÍNICA
                    rx.divider(margin="15px 0"),
                    rx.text("Información Clínica", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    form_field(
                        "Motivo de la Consulta",
                        "motivo_consulta",
                        AdminState.consulta_form["motivo_consulta"],
                        AdminState.update_consulta_form,
                        field_type="textarea",
                        placeholder="¿Por qué viene el paciente? Síntomas, molestias..."
                    ),
                    
                    form_field(
                        "Observaciones de la Cita",
                        "observaciones_cita",
                        AdminState.consulta_form["observaciones_cita"],
                        AdminState.update_consulta_form,
                        field_type="textarea",
                        placeholder="Observaciones adicionales sobre la cita"
                    ),
                    
                    # Solo mostrar notas internas en creación
                    rx.cond(
                        AdminState.selected_consulta.length() == 0,
                        form_field(
                            "Notas Internas (Admin)",
                            "notas_internas",
                            AdminState.consulta_form["notas_internas"],
                            AdminState.update_consulta_form,
                            field_type="textarea",
                            placeholder="Notas internas para el personal (opcional)"
                        ),
                        rx.box()
                    ),
                    
                    spacing="4",
                    width="100%"
                ),
                
                # Botones del modal
                rx.hstack(
                    secondary_button(
                        "Cancelar",
                        on_click=AdminState.close_consulta_modal
                    ),
                    primary_button(
                        rx.cond(
                            AdminState.selected_consulta.length() > 0,
                            "Actualizar",
                            "Crear Consulta"
                        ),
                        icon="calendar-plus",
                        on_click=AdminState.save_consulta,
                        loading=AdminState.is_loading
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    margin_top="24px"
                ),
                
                reset_on_submit=False
            ),
            
            background="white",
            padding="32px",
            border_radius="16px",
            box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1)",
            width="100%",
            max_width="700px",
            max_height="90vh",
            overflow_y="auto"
        )
    )

# ==========================================
# COMPONENTES DE CAMBIO DE ESTADO
# ==========================================

def estado_badge(estado: str) -> rx.Component:
    """Badge del estado de la consulta con colores"""
    color_scheme = rx.match(
        estado,
        ("programada", "blue"),
        ("confirmada", "cyan"),
        ("en_progreso", "orange"),
        ("completada", "green"),
        ("cancelada", "red"),
        ("no_asistio", "gray"),
        "gray"
    )
    
    estado_text = rx.match(
        estado,
        ("programada", "Programada"),
        ("confirmada", "Confirmada"),
        ("en_progreso", "En Progreso"),
        ("completada", "Completada"),
        ("cancelada", "Cancelada"),
        ("no_asistio", "No Asistió"),
        estado.capitalize()
    )
    
    return rx.badge(
        estado_text,
        variant="soft",
        color_scheme=color_scheme,
        size="2"
    )

def status_change_buttons(consulta_data: ConsultaModel) -> rx.Component:
    """Botones para cambiar el estado de la consulta"""
    estado_actual = consulta_data.estado
    
    return rx.hstack(
        # Programada -> Confirmada
        rx.cond(
            estado_actual == "programada",
            rx.tooltip(
                rx.button(
                    rx.icon("check", size=14),
                    size="1",
                    variant="ghost",
                    color=COLORS["secondary"]["500"],
                    on_click=lambda: AdminState.change_consulta_status(consulta_data.id, "confirmada", consulta_data)
                ),
                content="Confirmar"
            ),
            rx.box()
        ),
        
        # Programada/Confirmada -> En Progreso
        rx.cond(
           
            (estado_actual == "programada") | (estado_actual== "confirmada"),
            rx.tooltip(
                rx.button(
                    rx.icon("play", size=14),
                    size="1",
                    variant="ghost",
                    color=COLORS["blue"]["500"],
                    on_click=lambda: AdminState.change_consulta_status(consulta_data.id, "en_progreso", consulta_data)
                ),
                content="Iniciar Consulta"
            ),
            rx.box()
        ),
        
        # En Progreso -> Completada
        rx.cond(
            estado_actual == "en_progreso",
            rx.tooltip(
                rx.button(
                    rx.icon("check-circle", size=14),
                    size="1",
                    variant="ghost",
                    color=COLORS["success"],
                    on_click=lambda: AdminState.change_consulta_status(consulta_data.id, "completada", consulta_data)
                ),
                content="Completar"
            ),
            rx.box()
        ),
        
        # Cancelar (solo si no está completada)
        rx.cond(
            (estado_actual == "programada") | (estado_actual== "confirmada") | (estado_actual== "en_progreso"),
            rx.tooltip(
                rx.button(
                    rx.icon("x-circle", size=14),
                    size="1",
                    variant="ghost",
                    color=COLORS["error"],
                    on_click=lambda: AdminState.change_consulta_status(consulta_data.id, "cancelada", consulta_data)
                ),
                content="Cancelar"
            ),
            rx.box()
        ),
        
        # Editar (solo si está programada)
        rx.cond(
            estado_actual == "programada",
            rx.tooltip(
                rx.button(
                    rx.icon("edit", size=14),
                    size="1",
                    variant="ghost",
                    color=COLORS["primary"]["500"],
                    on_click=lambda: AdminState.open_consulta_modal(consulta_data)
                ),
                content="Editar"
            ),
            rx.box()
        ),
        
        spacing="1",
        align="center"
    )

# ==========================================
# TABLA DE CONSULTAS
# ==========================================

def consulta_table_row(consulta_data: ConsultaModel) -> rx.Component:
    """Fila individual de la tabla de consultas"""
    return rx.hstack(
        # Número de orden (#1, #2, #3...)
        rx.box(
            rx.text(
                f"#{consulta_data.orden_llegada}",
                size="4",
                weight="bold",
                color=COLORS["primary"]["600"]
            ),
            flex="0 0 60px",
            text_align="center"
        ),
        
        # Información de la consulta
        rx.vstack(
            rx.text(
                consulta_data.numero_consulta,
                size="3", 
                weight="medium",
                color=COLORS["gray"]["800"]
            ),
            rx.text(
                consulta_data.fecha_display,
                size="2", 
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="start",
            flex="2"
        ),
        
        # Paciente
        rx.vstack(
            rx.text(
                consulta_data.paciente_nombre,
                size="3", 
                weight="medium",
                color=COLORS["gray"]["800"]
            ),
            rx.text(
                rx.cond(
                    consulta_data.motivo_consulta,
                    consulta_data.motivo_consulta,
                    "Sin motivo especificado"
                ),
                # consulta_data.motivo_consulta[:30] + "..." if len(consulta_data.motivo_consulta or "") > 30 else consulta_data.motivo_consulta or "Sin motivo especificado",
                size="2",
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="start",
            flex="3"
        ),
        
        # Odontólogo
        rx.text(
            consulta_data.odontologo_nombre,
            size="3", 
            color=COLORS["gray"]["700"],
            flex="2"
        ),
        
        # Tipo de consulta
        rx.badge(
            consulta_data.tipo_consulta.capitalize(),
            variant="outline",
            color_scheme="gray",
            size="2",
            flex="1"
        ),
        
        # Estado
        estado_badge(consulta_data.estado),
        
        # Acciones
        status_change_buttons(consulta_data),
        
        spacing="4",
        align="center",
        padding="16px 20px",
        border_bottom=f"1px solid {COLORS['gray']['100']}",
        _hover={"background": COLORS["gray"]["50"]},
        width="100%"
    )

def consultas_table() -> rx.Component:
    """Tabla de consultas del día"""
    return rx.box(
        # Header de la tabla
        rx.hstack(
            rx.text("#", size="3", weight="medium", color=COLORS["gray"]["600"], flex="0 0 60px", text_align="center"),
            rx.text("Consulta", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2"),
            rx.text("Paciente", size="3", weight="medium", color=COLORS["gray"]["600"], flex="3"),
            rx.text("Odontólogo", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2"),
            rx.text("Tipo", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1"),
            rx.text("Estado", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1"),
            rx.text("Acciones", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1"),
            spacing="4",
            align="center",
            padding="16px 20px",
            background=COLORS["gray"]["50"],
            border_bottom=f"1px solid {COLORS['gray']['200']}",
            width="100%"
        ),
        
        # Filas de consultas
        rx.foreach(
            AdminState.filtered_consultas_list,
            consulta_table_row
        ),
        
        # Mensaje cuando no hay datos
        rx.cond(
            AdminState.consultas_list.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("calendar", size=48, color=COLORS["gray"]["400"]),
                    rx.text("No hay consultas programadas para hoy", 
                           size="4", 
                           color=COLORS["gray"]["500"],
                           weight="medium"),
                    rx.text("Crea la primera consulta del día haciendo clic en 'Nueva Consulta'", 
                           size="3", 
                           color=COLORS["gray"]["400"],
                           text_align="center"),
                    spacing="3",
                    align="center"
                ),
                padding="60px"
            ),
            rx.box()
        ),
        
        background="white",
        border_radius="12px",
        border=f"1px solid {COLORS['gray']['200']}",
        overflow="hidden",
        width="100%"
    )

# ==========================================
# FILTROS Y BÚSQUEDA
# ==========================================

def consultas_filters() -> rx.Component:
    """Filtros y búsqueda para consultas"""
    return rx.box(
        rx.vstack(
            # Primera fila: Búsqueda y botón principal
            rx.hstack(
                # Búsqueda
                rx.hstack(
                    rx.icon("search", size=20, color=COLORS["gray"]["600"]),
                    rx.input(
                        placeholder="Buscar por paciente, número de consulta...",
                        value=AdminState.consultas_search,
                        on_change=AdminState.set_consultas_search,
                        # on_blur=AdminState.apply_consultas_filters,
                        width="350px",
                        border=f"1px solid {COLORS['gray']['300']}",
                        border_radius="8px",
                        _focus={"border_color": COLORS["primary"]["500"]}
                    ),
                    spacing="2",
                    align="center"
                ),
                
                rx.spacer(),
                
                # Botones de acción
                rx.hstack(
                    secondary_button(
                        "Actualizar",
                        icon="refresh-cw",
                        on_click=AdminState.load_consultas_data
                    ),
                    primary_button(
                        "Nueva Consulta",
                        icon="calendar-plus",
                        on_click=lambda: AdminState.open_consulta_modal()
                    ),
                    spacing="3"
                ),
                
                align="center",
                width="100%"
            ),
            
            # Segunda fila: Filtros
            rx.hstack(
                rx.select(
                    ["todos", "programada", "confirmada", "en_progreso", "completada", "cancelada"],
                    placeholder="Estado",
                    value=AdminState.consultas_filter_estado,
                    on_change=AdminState.set_consultas_filter_estado,
                    width="150px"
                ),
                rx.select.root(
                    rx.select.trigger(
                        placeholder="Odontólogo",
                        width="200px"
                    ),
                    rx.select.content(
                        rx.select.item("Todos", value="todos"),
                        rx.foreach(
                            AdminState.odontologos_list,
                            lambda odontologo: rx.select.item(
                                 f"{odontologo.primer_nombre} {odontologo.primer_apellido}",
                                value=odontologo['id']
                            )
                        )
                    ),
                    value=AdminState.consultas_filter_odontologo,
                    on_change=AdminState.set_consultas_filter_odontologo,
                    width="200px"
                ),
                rx.button(
                    "Aplicar Filtros",
                    icon="filter",
                    variant="soft",
                    # on_click=AdminState.apply_consultas_filters
                ),
                rx.button(
                    "Limpiar",
                    icon="x",
                    variant="ghost",
                    on_click=lambda: [
                        AdminState.set_consultas_search(""),
                        AdminState.set_consultas_filter_estado("todos"),
                        AdminState.set_consultas_filter_odontologo("todos"),
                        # AdminState.apply_consultas_filters()
                    ]
                ),
                spacing="3",
                align="center"
            ),
            
            spacing="4",
            width="100%"
        ),
        padding="20px 24px",
        background="white",
        border_radius="12px",
        border=f"1px solid {COLORS['gray']['200']}",
        margin_bottom="24px"
    )

# ==========================================
# ESTADÍSTICAS DE CONSULTAS
# ==========================================

def consultas_stats() -> rx.Component:
    """Estadísticas de consultas del día"""
    return rx.grid(
        stat_card(
            title="Total Hoy",
            value=AdminState.total_consultas_hoy.to_string(),
            icon="calendar",
            color=COLORS["primary"]["500"],
            trend="Consultas del día"
        ),
        stat_card(
            title="En Espera",
            value=AdminState.consultas_programadas.to_string(),
            icon="clock",
            color=COLORS["secondary"]["500"],
            trend="Programadas/Confirmadas"
        ),
        stat_card(
            title="En Progreso", 
            value=AdminState.consultas_en_progreso.to_string(),
            icon="activity",
            color=COLORS["blue"]["500"],
            trend="Siendo atendidas"
        ),
        stat_card(
            title="Completadas",
            value=AdminState.consultas_completadas.to_string(),
            icon="check-circle",
            color=COLORS["success"],
            trend="Consultas finalizadas"
        ),
        columns="4",
        spacing="6",
        width="100%",
        margin_bottom="24px"
    )

# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

def consultas_management_page() -> rx.Component:
    """Página de gestión de consultas"""
    return rx.box(
        # Header
        main_header(
            "Gestión de Consultas",
            "Consultas del día por orden de llegada"
        ),
        
        # Alertas globales
        rx.cond(
            AdminState.global_message != "",
            rx.box(
                rx.cond(
                    AdminState.global_message_type == "success",
                    success_alert(AdminState.global_message),
                    error_alert(AdminState.global_message)
                ),
                padding="0 24px",
                margin_bottom="20px"
            ),
            rx.box()
        ),
        
        # Contenido
        rx.cond(
            AdminState.is_loading,
            loading_spinner(),
            rx.box(
                # Estadísticas
                consultas_stats(),
                
                # Filtros y búsqueda
                consultas_filters(),
                
                # Tabla de consultas
                consultas_table(),
            
                spacing="0",
                padding="24px"
            )
        ),
        
        # Modales
        consulta_modal(),
        
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

# ==========================================
# PUNTO DE ENTRADA CON CARGA AUTOMÁTICA
# ==========================================

def consultas_management() -> rx.Component:
    """Gestión de consultas con carga inicial automática"""
    return rx.box(
        consultas_management_page(),
        on_mount=AdminState.load_consultas_data
    )