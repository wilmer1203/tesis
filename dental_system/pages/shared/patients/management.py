"""
Página de gestión de pacientes compartida - Accesible por Administradores y Gerentes
Incluye todas las funcionalidades CRUD siguiendo el patrón del personal
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
from dental_system.state.boss_state import BossState
from dental_system.styles.themes import COLORS, GRADIENTS

# ==========================================
# MODAL DE CONFIRMACIÓN DE ELIMINACIÓN
# ==========================================

def delete_confirmation_modal(state_class) -> rx.Component:
    """Modal de confirmación para eliminar paciente"""
    return modal_overlay(
        state_class.show_delete_confirmation,
        rx.box(
            # Header del modal
            rx.hstack(
                rx.icon("alert-triangle", size=24, color=COLORS["error"]),
                rx.text(
                    "Confirmar Eliminación",
                    size="5",
                    weight="bold",
                    color=COLORS["error"]
                ),
                align="center"
            ),
            
            # Contenido
            rx.vstack(
                rx.text(
                    "¿Está seguro que desea eliminar a este paciente?",
                    size="4",
                    color=COLORS["gray"]["700"],
                    text_align="center"
                ),
                rx.text(
                    rx.cond(
                        state_class.paciente_to_delete.length() > 0,
                        state_class.paciente_to_delete["nombre_completo"],
                        ""
                    ),
                    size="3",
                    weight="bold",
                    color=COLORS["gray"]["900"],
                    text_align="center"
                ),
                rx.text(
                    "Esta acción desactivará al paciente pero mantendrá su historial en el sistema.",
                    size="2",
                    color=COLORS["gray"]["500"],
                    text_align="center"
                ),
                spacing="3",
                align="center",
                padding="20px 0"
            ),
            
            # Botones
            rx.hstack(
                secondary_button(
                    "Cancelar",
                    on_click=state_class.close_delete_confirmation
                ),
                eliminar_button(
                    "Eliminar",
                    icon="trash-2",
                    on_click=state_class.delete_paciente,
                    loading=state_class.is_loading,
                ),
                spacing="3",
                justify="center",
                width="100%"
            ),
            
            background="white",
            padding="32px",
            border_radius="16px",
            box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1)",
            width="100%",
            max_width="400px",
            text_align="center"
        )
    )

# ==========================================
# MODAL DE PACIENTE 
# ==========================================

def patient_modal(state_class) -> rx.Component:
    """Modal para crear/editar paciente"""
    return modal_overlay(
        state_class.show_paciente_modal,
        rx.box(
            # Header del modal
            rx.hstack(
                rx.text(
                    rx.cond(
                        state_class.selected_paciente.length() > 0,
                        "Editar Paciente",
                        "Nuevo Paciente"
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
                    on_click=state_class.close_paciente_modal,
                    _hover={"background": COLORS["gray"]["100"]}
                ),
                align="center",
                width="100%"
            ),
            
            # Alertas
            success_alert(state_class.success_message),
            error_alert(state_class.error_message),
            
            # Formulario
            rx.form(
                rx.vstack(
                    # Información Personal Básica
                    rx.text("Información Personal", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    rx.grid(
                        form_field(
                            "Nombre Completo",
                            "nombre_completo",
                            state_class.paciente_form["nombre_completo"],
                            state_class.update_paciente_form,
                            required=True,
                            placeholder="Nombre completo del paciente"
                        ),
                        form_field(
                            "Número de Documento",
                            "numero_documento",
                            state_class.paciente_form["numero_documento"],
                            state_class.update_paciente_form,
                            required=True,
                            placeholder="12345678"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    rx.grid(
                        form_field(
                            "Tipo de Documento",
                            "tipo_documento",
                            state_class.paciente_form["tipo_documento"],
                            state_class.update_paciente_form,
                            field_type="select",
                            options=["CC", "TI", "CE", "PA"],
                            required=True
                        ),
                        form_field(
                            "Fecha de Nacimiento",
                            "fecha_nacimiento",
                            state_class.paciente_form["fecha_nacimiento"],
                            state_class.update_paciente_form,
                            field_type="date",
                            placeholder="YYYY-MM-DD"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    rx.grid(
                        form_field(
                            "Género",
                            "genero",
                            state_class.paciente_form["genero"],
                            state_class.update_paciente_form,
                            field_type="select",
                            options=["masculino", "femenino", "otro"],
                            placeholder="Seleccionar género"
                        ),
                        form_field(
                            "Estado Civil",
                            "estado_civil",
                            state_class.paciente_form["estado_civil"],
                            state_class.update_paciente_form,
                            field_type="select",
                            options=["soltero", "casado", "divorciado", "viudo", "union_libre"],
                            placeholder="Seleccionar estado civil"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),

                    # Información de Contacto
                    rx.divider(margin="20px 0"),
                    rx.text("Información de Contacto", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    rx.grid(
                        form_field(
                            "Teléfono",
                            "telefono",
                            state_class.paciente_form["telefono"],
                            state_class.update_paciente_form,
                            placeholder="+58 281-1234567"
                        ),
                        form_field(
                            "Celular",
                            "celular",
                            state_class.paciente_form["celular"],
                            state_class.update_paciente_form,
                            placeholder="+58 424-1234567"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    form_field(
                        "Email",
                        "email",
                        state_class.paciente_form["email"],
                        state_class.update_paciente_form,
                        field_type="email",
                        placeholder="usuario@email.com"
                    ),
                    
                    form_field(
                        "Dirección",
                        "direccion",
                        state_class.paciente_form["direccion"],
                        state_class.update_paciente_form,
                        field_type="textarea",
                        placeholder="Dirección completa"
                    ),
                    
                    rx.grid(
                        form_field(
                            "Ciudad",
                            "ciudad",
                            state_class.paciente_form["ciudad"],
                            state_class.update_paciente_form,
                            placeholder="Ciudad de residencia"
                        ),
                        form_field(
                            "Ocupación",
                            "ocupacion",
                            state_class.paciente_form["ocupacion"],
                            state_class.update_paciente_form,
                            placeholder="Profesión u ocupación"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    # Información Médica (Opcional)
                    rx.divider(margin="20px 0"),
                    rx.text("Información Médica (Opcional)", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    form_field(
                        "Alergias",
                        "alergias",
                        state_class.paciente_form["alergias"],
                        state_class.update_paciente_form,
                        field_type="textarea",
                        placeholder="Separar con comas: alergia1, alergia2"
                    ),
                    
                    form_field(
                        "Medicamentos Actuales",
                        "medicamentos_actuales",
                        state_class.paciente_form["medicamentos_actuales"],
                        state_class.update_paciente_form,
                        field_type="textarea",
                        placeholder="Separar con comas: medicamento1, medicamento2"
                    ),
                    
                    form_field(
                        "Condiciones Médicas",
                        "condiciones_medicas",
                        state_class.paciente_form["condiciones_medicas"],
                        state_class.update_paciente_form,
                        field_type="textarea",
                        placeholder="Separar con comas: condición1, condición2"
                    ),
                    
                    form_field(
                        "Observaciones",
                        "observaciones",
                        state_class.paciente_form["observaciones"],
                        state_class.update_paciente_form,
                        field_type="textarea",
                        placeholder="Observaciones adicionales"
                    ),
                    
                    spacing="4",
                    width="100%"
                ),
                
                # Botones del modal
                rx.hstack(
                    secondary_button(
                        "Cancelar",
                        on_click=state_class.close_paciente_modal
                    ),
                    primary_button(
                        rx.cond(
                            state_class.selected_paciente.length() > 0,
                            "Actualizar",
                            "Crear"
                        ),
                        icon="save",
                        on_click=state_class.save_paciente,
                        loading=state_class.is_loading
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
# TABLA DE PACIENTES 
# ==========================================

def patient_table_row(patient_data: dict, state_class) -> rx.Component:
    """Fila individual de la tabla de pacientes"""
    return rx.hstack(
        # Información básica
        rx.vstack(
            rx.text(
                patient_data.get("nombre_completo", "N/A"),
                size="3", 
                weight="medium",
                color=COLORS["gray"]["800"]
            ),
            rx.text(
                f"HC: {patient_data.get('numero_historia', 'N/A')}",
                size="2", 
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="start",
            flex="3"
        ),
        
        # Documento
        rx.vstack(
            rx.text(
                patient_data.get("numero_documento", "N/A"),
                size="3", 
                color=COLORS["gray"]["700"]
            ),
            rx.text(
                patient_data.get("tipo_documento", "CC"),
                size="2", 
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="start",
            flex="2"
        ),
        
        # Género con badge
        rx.badge(
            patient_data.get("genero", "No especificado").capitalize(),
            variant="soft",
            color_scheme=rx.match(
                patient_data.get("genero", ""),
                ("masculino", "blue"),
                ("femenino", "pink"),
                ("otro", "gray"),
                "gray"
            ),
            flex="1"
        ),
        
        # Edad
        rx.text(
            f"{patient_data.get('edad', 'N/A')} años" if patient_data.get('edad') else "N/A",
            size="3", 
            color=COLORS["gray"]["600"], 
            flex="1",
            text_align="center"
        ),
        
        # Contacto
        rx.vstack(
            rx.text(
                patient_data.get("telefono") or patient_data.get("celular", "N/A"),
                size="3", 
                color=COLORS["gray"]["600"]
            ),
            rx.text(
                patient_data.get("email", "N/A")[:20] + "..." if patient_data.get("email") and len(patient_data.get("email", "")) > 20 else patient_data.get("email", "N/A"),
                size="2", 
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="start",
            flex="2"
        ),
        
        # Estado con badge
        rx.badge(
            "Activo" if patient_data.get("activo", True) else "Inactivo",
            variant="soft",
            color_scheme="green" if patient_data.get("activo", True) else "red",
            flex="1"
        ),
        
        # Acciones
        rx.hstack(
            rx.tooltip(
                rx.button(
                    rx.icon("edit", size=16),
                    size="2",
                    variant="ghost",
                    color=COLORS["primary"]["500"],
                    on_click=lambda: state_class.open_paciente_modal(patient_data)
                ),
                content="Editar paciente"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("file-text", size=16),
                    size="2",
                    variant="ghost",
                    color=COLORS["secondary"]["500"]
                ),
                content="Ver historial"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("trash-2", size=16),
                    size="2",
                    variant="ghost",
                    color=COLORS["error"],
                    on_click=lambda: state_class.open_delete_confirmation(patient_data)
                ),
                content="Eliminar paciente"
            ),
            # Botón de reactivar solo si está inactivo
            rx.cond(
                not patient_data.get("activo", True),
                rx.tooltip(
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        size="2",
                        variant="ghost",
                        color=COLORS["success"],
                        on_click=lambda: state_class.reactivate_paciente(patient_data)
                    ),
                    content="Reactivar paciente"
                ),
                rx.box()
            ),
            spacing="1",
            align="center",
            flex="1"
        ),
        
        spacing="4",
        align="center",
        padding="16px 20px",
        border_bottom=f"1px solid {COLORS['gray']['100']}",
        _hover={"background": COLORS["gray"]["50"]},
        width="100%"
    )

def patients_table(state_class) -> rx.Component:
    """Tabla de pacientes con datos y acciones"""
    return rx.box(
        # Header de la tabla
        rx.hstack(
            rx.text("Paciente", size="3", weight="medium", color=COLORS["gray"]["600"], flex="3", text_align="left"),
            rx.text("Documento", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2", text_align="left"),
            rx.text("Género", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", text_align="center"),
            rx.text("Edad", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", text_align="center"),
            rx.text("Contacto", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2", text_align="left"),
            rx.text("Estado", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", text_align="center"),
            rx.text("Acciones", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", text_align="center"),
            spacing="4",
            align="center",
            padding="16px 20px",
            background=COLORS["gray"]["50"],
            border_bottom=f"1px solid {COLORS['gray']['200']}",
            width="100%"
        ),
        
        # Filas de datos
        rx.foreach(
            state_class.pacientes_list,
            lambda patient: patient_table_row(patient, state_class)
        ),
        
        # Mensaje cuando no hay datos
        rx.cond(
            state_class.pacientes_list.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("users", size=48, color=COLORS["gray"]["400"]),
                    rx.text("No hay pacientes registrados", 
                           size="4", 
                           color=COLORS["gray"]["500"],
                           weight="medium"),
                    rx.text("Haz clic en 'Nuevo Paciente' para agregar el primer paciente", 
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

def patients_filters(state_class) -> rx.Component:
    """Filtros y búsqueda para pacientes"""
    return rx.box(
        rx.vstack(
            # Primera fila: Búsqueda y botón principal
            rx.hstack(
                # Búsqueda
                rx.hstack(
                    rx.icon("search", size=20, color=COLORS["gray"]["600"]),
                    rx.input(
                        placeholder="Buscar por nombre o documento...",
                        value=state_class.pacientes_search,
                        on_change=state_class.set_pacientes_search,
                        on_blur=state_class.apply_pacientes_filters,
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
                        "Exportar",
                        icon="download"
                    ),
                    primary_button(
                        "Nuevo Paciente",
                        icon="user-plus",
                        on_click=lambda: state_class.open_paciente_modal()
                    ),
                    spacing="3"
                ),
                
                align="center",
                width="100%"
            ),
            
            # Segunda fila: Filtros
            rx.hstack(
                rx.select(
                    ["todos", "masculino", "femenino", "otro"],
                    placeholder="Género",
                    value=state_class.pacientes_filter_genero,
                    on_change=state_class.set_pacientes_filter_genero,
                    width="150px"
                ),
                rx.select(
                    ["activos", "todos", "inactivos"],
                    placeholder="Estado",
                    value=state_class.pacientes_filter_activos,
                    on_change=state_class.set_pacientes_filter_activos,
                    width="150px"
                ),
                rx.button(
                    "Aplicar Filtros",
                    icon="filter",
                    variant="soft",
                    on_click=state_class.apply_pacientes_filters
                ),
                rx.button(
                    "Limpiar",
                    icon="x",
                    variant="ghost",
                    on_click=lambda: [
                        state_class.set_pacientes_search(""),
                        state_class.set_pacientes_filter_genero(""),
                        state_class.set_pacientes_filter_activos("activos"),
                        state_class.apply_pacientes_filters()
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
# ESTADÍSTICAS DE PACIENTES
# ==========================================

def patients_stats(state_class) -> rx.Component:
    """Estadísticas de pacientes"""
    return rx.grid(
        stat_card(
            title="Total Pacientes",
            value=state_class.total_pacientes.to_string(),
            icon="users",
            color=COLORS["primary"]["500"],
            trend="Pacientes registrados"
        ),
        stat_card(
            title="Activos",
            value=state_class.pacientes_activos.to_string(),
            icon="user-check",
            color=COLORS["success"],
            trend="Pacientes activos"
        ),
        stat_card(
            title="Hombres",
            value=state_class.pacientes_hombres.to_string(),
            icon="male",
            color=COLORS["blue"]["500"],
            trend="Pacientes masculinos"
        ),
        stat_card(
            title="Mujeres",
            value=state_class.pacientes_mujeres.to_string(),
            icon="female",
            color=COLORS["secondary"]["500"],
            trend="Pacientes femeninos"
        ),
        columns="4",
        spacing="6",
        width="100%",
        margin_bottom="24px"
    )

# ==========================================
# FUNCIÓN PARA DETERMINAR EL ESTADO BASADO EN EL ROL
# ==========================================

def get_state_by_role():
    """Determina qué estado usar basado en el rol del usuario actual"""
    # Por ahora retornamos AdminState, pero esto se puede hacer más dinámico
    return AdminState

# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

def patients_management_page() -> rx.Component:
    """Página de gestión de pacientes"""
    # Determinar qué estado usar basado en el rol
    state_class = get_state_by_role()
    
    return rx.box(
        # Header
        main_header(
            "Gestión de Pacientes",
            "Administrar pacientes y su información médica"
        ),
        
        # Alertas globales
        rx.cond(
            state_class.global_message != "",
            rx.box(
                rx.cond(
                    state_class.global_message_type == "success",
                    success_alert(state_class.global_message),
                    error_alert(state_class.global_message)
                ),
                padding="0 24px",
                margin_bottom="20px"
            ),
            rx.box()
        ),
        
        # Contenido
        rx.cond(
            state_class.is_loading,
            loading_spinner(),
            rx.box(
                # Estadísticas
                patients_stats(state_class),
                
                # Filtros y búsqueda
                patients_filters(state_class),
                
                # Tabla de pacientes
                patients_table(state_class),
            
                spacing="0",
                padding="24px"
            )
        ),
        
        # Modales
        patient_modal(state_class),
        delete_confirmation_modal(state_class),
        
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

# ==========================================
# PUNTO DE ENTRADA CON CARGA AUTOMÁTICA
# ==========================================

def patients_management() -> rx.Component:
    """Gestión de pacientes con carga inicial automática"""
    state_class = get_state_by_role()
    
    return rx.box(
        patients_management_page(),
        on_mount=state_class.load_pacientes_data
    )
