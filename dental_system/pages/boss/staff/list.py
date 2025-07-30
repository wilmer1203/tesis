"""
Página de gestión de personal para el gerente - VERSIÓN ACTUALIZADA CON CRUD COMPLETO
Incluye todas las funcionalidades corregidas del boss_state
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
# from dental_system.components.common import stat_card, primary_button,secondary_button,eliminar_button
from dental_system.components.common import ( stat_card, primary_button, secondary_button, eliminar_button )
from dental_system.state.boss_state import BossState
from dental_system.models import PersonalModel
from dental_system.styles.themes import COLORS

# ==========================================
# MODAL DE CONFIRMACIÓN DE ELIMINACIÓN
# ==========================================

def delete_confirmation_modal() -> rx.Component:
    """Modal de confirmación para eliminar personal"""
    return modal_overlay(
        BossState.show_delete_confirmation,
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
                    "¿Está seguro que desea eliminar a este personal?",
                    size="4",
                    color=COLORS["gray"]["700"],
                    text_align="center"
                ),
                rx.text(
                    rx.cond(
                        BossState.personal_to_delete.length() > 0,
                        BossState.personal_to_delete["usuarios"]["nombre_completo"],
                        ""
                    ),
                    size="3",
                    weight="bold",
                    color=COLORS["gray"]["900"],
                    text_align="center"
                ),
                rx.text(
                    "Esta acción desactivará al personal pero mantendrá su historial en el sistema.",
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
                    on_click=BossState.close_delete_confirmation
                ),
                eliminar_button(
                    "Eliminar",
                    icon="trash-2",
                    on_click=BossState.delete_personal,
                    loading=BossState.is_loading,
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
# MODAL DE PERSONAL 
# ==========================================

def personal_modal() -> rx.Component:
    """Modal para crear/editar personal - ACTUALIZADO"""
    return modal_overlay(
        BossState.show_personal_modal,
        rx.box(
            # Header del modal
            rx.hstack(
                rx.text(
                    rx.cond(
                        BossState.selected_personal.length() > 0,
                        "Editar Personal",
                        "Nuevo Personal"
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
                    on_click=BossState.close_personal_modal,
                    _hover={"background": COLORS["gray"]["100"]}
                ),
                align="center",
                width="100%"
            ),
            
            # Alertas
            success_alert(BossState.success_message),
            error_alert(BossState.error_message),
            
            # Formulario
            rx.form(
                rx.vstack(
                    # Información Personal
                    rx.text("Información Personal", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                   rx.grid(
                        form_field(
                            "Primer Nombre",
                            "primer_nombre",
                            BossState.personal_form["primer_nombre"],
                            BossState.update_personal_form,
                            required=True,
                            placeholder="Juan"
                        ),
                        form_field(
                            "Segundo Nombre",
                            "segundo_nombre",
                            BossState.personal_form["segundo_nombre"],
                            BossState.update_personal_form,
                            placeholder="Carlos (opcional)"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    rx.grid(
                        form_field(
                            "Primer Apellido",
                            "primer_apellido",
                            BossState.personal_form["primer_apellido"],
                            BossState.update_personal_form,
                            required=True,
                            placeholder="Pérez"
                        ),
                        form_field(
                            "Segundo Apellido",
                            "segundo_apellido",
                            BossState.personal_form["segundo_apellido"],
                            BossState.update_personal_form,
                            placeholder="González (opcional)"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),

                    rx.grid(
                        form_field(
                            "Email",
                            "email",
                            BossState.personal_form["email"],
                            BossState.update_personal_form,
                            field_type="email",
                            required=True,
                            placeholder="usuario@dental.com"
                        ),
                        # CONTRASEÑA - Solo para nuevos usuarios
                        rx.cond(
                            BossState.selected_personal.length() == 0,
                            form_field(
                                "Contraseña",
                                "password",
                                BossState.personal_form["password"],
                                BossState.update_personal_form,
                                field_type="password",
                                required=True,
                                placeholder="Mínimo 8 caracteres"
                            ),
                            form_field(
                                "Teléfono",
                                "telefono",
                                BossState.personal_form["telefono"],
                                BossState.update_personal_form,
                                placeholder="+58 414-1234567"
                            )
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    # Solo mostrar teléfono separado si estamos editando
                    rx.cond(
                        BossState.selected_personal.length() > 0,
                        form_field(
                            "Teléfono",
                            "telefono",
                            BossState.personal_form["telefono"],
                            BossState.update_personal_form,
                            placeholder="+58 414-1234567"
                        ),
                        rx.box()
                    ),
                    
                    rx.grid(
                        form_field(
                            "Número de Documento",
                            "numero_documento",
                            BossState.personal_form["numero_documento"],
                            BossState.update_personal_form,
                            required=True,
                            placeholder="12345678"
                        ),
                        form_field(
                            "Celular",
                            "celular",
                            BossState.personal_form["celular"],
                            BossState.update_personal_form,
                            placeholder="+58 424-7654321"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    form_field(
                        "Dirección",
                        "direccion",
                        BossState.personal_form["direccion"],
                        BossState.update_personal_form,
                        field_type="textarea",
                        placeholder="Dirección completa"
                    ),
                    
                    # Información Profesional
                    rx.divider(margin="20px 0"),
                    rx.text("Información Profesional", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    rx.grid(
                        form_field(
                            "Tipo de Personal",
                            "tipo_personal",
                            BossState.personal_form["tipo_personal"],
                            BossState.update_personal_form,
                            field_type="select",
                            options=["Odontólogo", "Asistente", "Administrador", "Gerente"],
                            required=True
                        ),
                        form_field(
                            "Especialidad",
                            "especialidad",
                            BossState.personal_form["especialidad"],
                            BossState.update_personal_form,
                            placeholder="Ej: Endodoncia, Ortodoncia"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    rx.grid(
                        form_field(
                            "Número de Licencia",
                            "numero_licencia",
                            BossState.personal_form["numero_licencia"],
                            BossState.update_personal_form,
                            placeholder="Número de licencia profesional"
                        ),
                        form_field(
                            "Salario",
                            "salario",
                            BossState.personal_form["salario"],
                            BossState.update_personal_form,
                            field_type="number",
                            placeholder="1000000"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    spacing="4",
                    width="100%"
                ),
                
                # Botones del modal
                rx.hstack(
                    secondary_button(
                        "Cancelar",
                        on_click=BossState.close_personal_modal
                    ),
                    primary_button(
                        rx.cond(
                            BossState.selected_personal.length() > 0,
                            "Actualizar",
                            "Crear"
                        ),
                        icon="save",
                        on_click=BossState.save_personal,
                        loading=BossState.is_loading
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    margin_top="24px"
                ),
                
                # on_submit=BossState.save_personal,
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
# TABLA DE PERSONAL 
# ==========================================

def personal_table_row(person_data: PersonalModel) -> rx.Component:
    """Fila individual de la tabla de personal - ACTUALIZADA"""
    return rx.hstack(
        # Avatar y nombre
       
        rx.vstack(
            rx.text(
                rx.cond(
                    person_data.primer_nombre,
                    f"{person_data.primer_nombre} {person_data.primer_apellido}".strip(),
                    "N/A"
                ),
                size="3", 
                weight="medium",
                color=COLORS["gray"]["800"]
            ),
            rx.text(
                rx.cond(
                    person_data.usuarios.email,
                    person_data.usuarios.email,
                    "N/A"
                ),
                size="2", 
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align="center",
            flex="3"
        ),
        
        # Tipo con badge
        rx.badge(
            person_data.tipo_personal,
            variant="soft",
            color_scheme=rx.match(
                person_data.tipo_personal,
                ("Odontólogo", "green"),
                ("Administrador", "blue"),
                ("Asistente", "yellow"),
                ("Gerente", "purple"),
                "gray"
            ),
            
            align="center",
            flex="1",
            
        ),
        
        # Especialidad
        rx.text(
            rx.cond(
                person_data.especialidad,
                person_data.especialidad,
                "-"   
            ),
            size="3", 
            color=COLORS["gray"]["600"], 
            flex="2",
            align="center",
        ),
        
        # Estado con badge
        rx.badge(
            person_data.estado_laboral.capitalize(),
            variant="soft",
            color_scheme=rx.match(
                person_data.estado_laboral,
                ("activo", "green"),
                ("inactivo", "red"),
                ("vacaciones", "yellow"),
                "gray"
            ),
            flex="1"
        ),
        
        # Teléfono
        rx.text(
            rx.cond(
                person_data.usuarios.telefono,
                person_data.usuarios.telefono,
                "-"
            ),
            size="3", 
            color=COLORS["gray"]["600"], 
            align="center",
            flex="2"
        ),
        
        # Acciones
        rx.hstack(
            rx.tooltip(
                rx.button(
                    rx.icon("edit", size=16),
                    size="2",
                    variant="ghost",
                    color=COLORS["primary"]["500"],
                    on_click=lambda: BossState.open_personal_modal({
                        "id": person_data.id,
                        "numero_documento": person_data.numero_documento,
                        "tipo_personal": person_data.tipo_personal,
                        "especialidad": person_data.especialidad,
                        "estado_laboral": person_data.estado_laboral,
                        "numero_licencia": person_data.numero_licencia,
                        "celular": person_data.celular,
                        "direccion": person_data.direccion,
                        "salario": person_data.salario,
                        # CAMPOS SEPARADOS
                        "primer_nombre": person_data.primer_nombre,
                        "segundo_nombre": person_data.segundo_nombre,
                        "primer_apellido": person_data.primer_apellido,
                        "segundo_apellido": person_data.segundo_apellido,
                        "usuarios": {
                            "id": person_data.usuarios.id,
                            "nombre_completo": person_data.nombre_completo_display,
                            "email": person_data.usuarios.email,
                            "telefono": person_data.usuarios.telefono,
                            "activo": person_data.usuarios.activo
                        }
                    }) # type: ignore
                ),
                content="Editar personal"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("key", size=16),
                    size="2",
                    variant="ghost",
                    color=COLORS["secondary"]["500"]
                ),
                content="Resetear contraseña"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("trash-2", size=16),
                    size="2",
                    variant="ghost",
                    color=COLORS["error"],
                    on_click=lambda: BossState.open_delete_confirmation({
                        "id": person_data.id,
                        "usuarios": {
                            "id": person_data.usuarios.id,
                            "nombre_completo": person_data.nombre_completo_display,
                            "email": person_data.usuarios.email
                        }
                    })
                ),
                content="Eliminar personal"
            ),
            # Botón de reactivar solo si está inactivo
            rx.cond(
                person_data.estado_laboral == "inactivo",
                rx.tooltip(
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        size="2",
                        variant="ghost",
                        color=COLORS["success"],
                        on_click=lambda: BossState.reactivate_personal({
                            "id": person_data.id,
                            "usuarios": {
                                "id": person_data.usuarios.id,
                                "nombre_completo": person_data.nombre_completo_display
                            }
                        })
                    ),
                    content="Reactivar personal"
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


def personal_table() -> rx.Component:
    """Tabla de personal con datos y acciones - ACTUALIZADA"""
    return rx.box(
        # Header de la tabla
        rx.hstack(
            rx.text("Nombre", size="3", weight="medium", color=COLORS["gray"]["600"], flex="3",align="center"),
            rx.text("Tipo", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1",align="center"),
            rx.text("Especialidad", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2",align="center"),
            rx.text("Estado", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1",align="center"),
            rx.text("Teléfono", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2",align="center"),
            rx.text("Acciones", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1",align="center"),
            spacing="4",
            align="center",
            padding="16px 20px",
            background=COLORS["gray"]["50"],
            border_bottom=f"1px solid {COLORS['gray']['200']}",
            width="100%"
        ),
        
        # Filas de datos
        rx.foreach(
            BossState.personal_list,
            personal_table_row
        ),
        
        # Mensaje cuando no hay datos
        rx.cond(
            BossState.personal_list.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("users", size=48, color=COLORS["gray"]["400"]),
                    rx.text("No hay personal registrado", 
                           size="4", 
                           color=COLORS["gray"]["500"],
                           weight="medium"),
                    rx.text("Haz clic en 'Nuevo Personal' para agregar el primer miembro del equipo", 
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
# FILTROS Y BÚSQUEDA - FUNCIONALES
# ==========================================

def personal_filters() -> rx.Component:
    """Filtros y búsqueda para el personal - FUNCIONALES"""
    return rx.box(
        rx.vstack(
            # Primera fila: Búsqueda y botón principal
            rx.hstack(
                # Búsqueda
                rx.hstack(
                    rx.icon("search", size=20, color=COLORS["gray"]["600"]),
                    rx.input(
                        placeholder="Buscar por nombre, email o documento...",
                        value=BossState.personal_search,
                        on_change=BossState.set_personal_search,
                        on_blur=BossState.apply_personal_filters,
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
                        "Nuevo Personal",
                        icon="user-plus",
                        on_click=lambda: BossState.open_personal_modal()
                    ),
                    spacing="3"
                ),
                
                align="center",
                width="100%"
            ),
            
            # Segunda fila: Filtros
            rx.hstack(
                rx.select(
                    ["todos", "Odontólogo", "Administrador", "Asistente", "Gerente"],
                    placeholder="Tipo de personal",
                    value=BossState.personal_filter_tipo,
                    on_change=BossState.set_personal_filter_tipo,
                    width="200px"
                ),
                rx.select(
                    ["todos", "activo", "inactivo", "vacaciones"],
                    placeholder="Estado laboral",
                    value=BossState.personal_filter_estado,
                    on_change=BossState.set_personal_filter_estado,
                    width="200px"
                ),
                rx.button(
                    "Aplicar Filtros",
                    icon="filter",
                    variant="soft",
                    on_click=BossState.apply_personal_filters
                ),
                rx.button(
                    "Limpiar",
                    icon="x",
                    variant="ghost",
                    on_click=lambda: [
                        BossState.set_personal_search(""),
                        BossState.set_personal_filter_tipo(""),
                        BossState.set_personal_filter_estado(""),
                        BossState.apply_personal_filters()
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
# ESTADÍSTICAS DEL PERSONAL - ACTUALIZADAS
# ==========================================

def personal_stats() -> rx.Component:
    """Estadísticas rápidas del personal - ACTUALIZADAS"""
    return rx.grid(
        stat_card(
            title="Total Personal",
            value=BossState.total_personal.to_string(),
            icon="users",
            color=COLORS["primary"]["500"],
            trend="Miembros del equipo"
        ),
        stat_card(
            title="Activos",
            value=BossState.total_activos.to_string(),
            icon="user-check",
            color=COLORS["success"],
            trend="Personal activo"
        ),
        stat_card(
            title="Odontólogos",
            value=BossState.total_odontologos.to_string(),
            icon="graduation-cap",
            color=COLORS["secondary"]["500"],
            trend="Profesionales"
        ),
        stat_card(
            title="Otros Roles",
            value=BossState.total_otros_roles.to_string(),
            icon="briefcase",
            color=COLORS["blue"]["500"],
            trend="Admin y asistentes"
        ),
        columns="4",
        spacing="6",
        width="100%",
        margin_bottom="24px"
    )

# ==========================================
# PÁGINA PRINCIPAL - ACTUALIZADA
# ==========================================

def personal_management_page() -> rx.Component:
    """Página de gestión de personal - ACTUALIZADA"""
    return rx.box(
        # Header
        main_header(
            "Gestión de Personal",
            "Administrar empleados y sus roles en el sistema"
        ),
        
        # Alertas globales
        rx.cond(
            BossState.global_message != "",
            rx.box(
                rx.cond(
                    BossState.global_message_type == "success",
                    success_alert(BossState.global_message),
                    error_alert(BossState.global_message)
                ),
                padding="0 24px",
                margin_bottom="20px"
            ),
            rx.box()
        ),
        
        # Contenido
        rx.cond(
            BossState.is_loading,
            loading_spinner(),
            rx.box(
                # Estadísticas
                personal_stats(),
                
                # Filtros y búsqueda
                personal_filters(),
                
                # Tabla de personal
                personal_table(),
            
                spacing="0",
                padding="24px"
            )
        ),
        
        # Modales
        personal_modal(),
        delete_confirmation_modal(),
        
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

# ==========================================
# PUNTO DE ENTRADA CON CARGA AUTOMÁTICA
# ==========================================

def personal_management() -> rx.Component:
    """Gestión de personal con carga inicial automática"""
    return rx.box(
        personal_management_page(),
        on_mount=BossState.load_personal_data
    )
