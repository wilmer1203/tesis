"""
Componentes específicos para el rol de Administrador
Siguiendo el patrón de boss.py pero enfocado en funcionalidades de admin
"""

import reflex as rx
from typing import List, Dict, Any, Optional
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS

# ==========================================
# COMPONENTES DE NAVEGACIÓN
# ==========================================

def admin_sidebar_item(icon: str, text: str, page_id: str, current_page: str) -> rx.Component:
    """Item individual del sidebar para admin"""
    is_active = current_page == page_id
    
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=20),
            rx.text(text, size="3", weight="medium"),
            spacing="3",
            align="center",
        ),
        padding="12px 16px",
        border_radius="8px",
        background=rx.cond(
            is_active,
            COLORS["primary"]["500"],
            "transparent"
        ),
        color=rx.cond(is_active, "white", COLORS["gray"]["600"]),
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background": rx.cond(
                is_active,
                COLORS["primary"]["500"],
                COLORS["gray"]["50"]
            ),
            "color": rx.cond(is_active, "white", COLORS["gray"]["700"])
        },
        on_click=lambda: navigate_to_admin_page(page_id),
        width="100%"
    )

def navigate_to_admin_page(page_id: str):
    """Función auxiliar para navegación del admin"""
    from dental_system.state.admin_state import AdminState
    return AdminState.navigate_to(page_id)

def admin_sidebar() -> rx.Component:
    """Sidebar de navegación para el administrador"""
    from dental_system.state.admin_state import AdminState
    
    return rx.box(
        # Header del sidebar
        rx.hstack(
            rx.image(
                src="/images/logo-odontomara.png",
                width="60px",
                border_radius="50%",
                alt=""
            ),
            rx.vstack(
                rx.text("Odontomara", size="6", weight="bold", color=COLORS["secondary"]["700"], text_shadow=SHADOWS["xl"]),
                rx.text("Panel Administrativo", size="2", color=COLORS["gray"]["500"]),
                spacing="0",
                align_items="start"
            ),
            spacing="3",
            align="center",
            padding="20px",
            border_bottom=f"1px solid {COLORS['gray']['200']}"
        ),
        
        # Navegación principal
        rx.vstack(
            rx.text("Principal", size="2", weight="medium", color=COLORS["gray"]["500"], margin_bottom="8px"),
            admin_sidebar_item("layout-dashboard", "Dashboard", "dashboard", AdminState.current_page),
            admin_sidebar_item("users", "Pacientes", "pacientes", AdminState.current_page),
            
            rx.text("Gestión", size="2", weight="medium", color=COLORS["gray"]["500"], margin_top="24px", margin_bottom="8px"),
            admin_sidebar_item("calendar", "Consultas", "consultas", AdminState.current_page),
            admin_sidebar_item("credit-card", "Pagos", "pagos", AdminState.current_page),
            
            spacing="2",
            align_items="stretch",
            padding="20px",
            width="100%"
        ),
        
        # Footer del sidebar
        rx.spacer(),
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        rx.cond(
                            AdminState.user_profile,
                            AdminState.user_profile["nombre_completo"],
                            "Usuario"
                        ), 
                        size="3", 
                        weight="medium"
                    ),
                    rx.text(
                        rx.cond(
                            AdminState.user_profile,
                            AdminState.user_profile["email"],
                            "email@dental.com"
                        ), 
                        size="2", 
                        color=COLORS["gray"]["500"]
                    ),
                    spacing="0",
                    align_items="start"
                ),
                spacing="3",
                align="center"
            ),
            padding="20px",
            border_top=f"1px solid {COLORS['gray']['200']}"
        ),
        
        width=rx.cond(AdminState.sidebar_collapsed, "80px", "280px"),
        height="100vh",
        background="white",
        border_right=f"1px solid {COLORS['gray']['200']}",
        position="fixed",
        left="0",
        top="0",
        z_index="1000",
        transition="width 0.3s ease",
        overflow_y="auto"
    )

# ==========================================
# COMPONENTES DE PACIENTES
# ==========================================

def paciente_modal() -> rx.Component:
    """Modal para crear/editar pacientes"""
    from dental_system.state.admin_state import AdminState
    from dental_system.components.role_specific.boss import (
        modal_overlay, form_field, success_alert, error_alert
    )
    from dental_system.components.common import primary_button, secondary_button
    
    return modal_overlay(
        AdminState.show_paciente_modal,
        rx.box(
            # Header del modal
            rx.hstack(
                rx.text(
                    rx.cond(
                        AdminState.selected_paciente.length() > 0,
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
                    on_click=AdminState.close_paciente_modal,
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
                    # Información Personal
                    rx.text("Información Personal", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    rx.grid(
                        form_field(
                            "Nombre Completo",
                            "nombre_completo",
                            AdminState.paciente_form["nombre_completo"],
                            AdminState.update_paciente_form,
                            required=True,
                            placeholder="Juan Carlos Pérez González"
                        ),
                        form_field(
                            "Número de Documento",
                            "numero_documento",
                            AdminState.paciente_form["numero_documento"],
                            AdminState.update_paciente_form,
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
                            AdminState.paciente_form["tipo_documento"],
                            AdminState.update_paciente_form,
                            field_type="select",
                            options=["CC", "TI", "CE", "PP"],
                            required=True
                        ),
                        form_field(
                            "Fecha de Nacimiento",
                            "fecha_nacimiento",
                            AdminState.paciente_form["fecha_nacimiento"],
                            AdminState.update_paciente_form,
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
                            AdminState.paciente_form["genero"],
                            AdminState.update_paciente_form,
                            field_type="select",
                            options=["masculino", "femenino", "otro"],
                            placeholder="Seleccionar género"
                        ),
                        form_field(
                            "Estado Civil",
                            "estado_civil",
                            AdminState.paciente_form["estado_civil"],
                            AdminState.update_paciente_form,
                            field_type="select",
                            options=["soltero", "casado", "divorciado", "viudo", "union_libre"],
                            placeholder="Seleccionar estado"
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
                            AdminState.paciente_form["telefono"],
                            AdminState.update_paciente_form,
                            placeholder="+58 281-1234567"
                        ),
                        form_field(
                            "Celular",
                            "celular",
                            AdminState.paciente_form["celular"],
                            AdminState.update_paciente_form,
                            placeholder="+58 414-7654321"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    form_field(
                        "Email",
                        "email",
                        AdminState.paciente_form["email"],
                        AdminState.update_paciente_form,
                        field_type="email",
                        placeholder="paciente@email.com"
                    ),
                    
                    form_field(
                        "Dirección",
                        "direccion",
                        AdminState.paciente_form["direccion"],
                        AdminState.update_paciente_form,
                        field_type="textarea",
                        placeholder="Dirección completa de residencia"
                    ),
                    
                    rx.grid(
                        form_field(
                            "Ciudad",
                            "ciudad",
                            AdminState.paciente_form["ciudad"],
                            AdminState.update_paciente_form,
                            placeholder="Puerto La Cruz"
                        ),
                        form_field(
                            "Departamento/Estado",
                            "departamento",
                            AdminState.paciente_form["departamento"],
                            AdminState.update_paciente_form,
                            placeholder="Anzoátegui"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    form_field(
                        "Ocupación",
                        "ocupacion",
                        AdminState.paciente_form["ocupacion"],
                        AdminState.update_paciente_form,
                        placeholder="Profesión u ocupación"
                    ),
                    
                    # Información Médica
                    rx.divider(margin="20px 0"),
                    rx.text("Información Médica", size="4", weight="medium", color=COLORS["gray"]["700"]),
                    
                    form_field(
                        "Alergias",
                        "alergias",
                        AdminState.paciente_form["alergias"],
                        AdminState.update_paciente_form,
                        field_type="textarea",
                        placeholder="Penicilina, mariscos, etc. (separar con comas)"
                    ),
                    
                    form_field(
                        "Medicamentos Actuales",
                        "medicamentos_actuales",
                        AdminState.paciente_form["medicamentos_actuales"],
                        AdminState.update_paciente_form,
                        field_type="textarea",
                        placeholder="Medicamentos que toma actualmente (separar con comas)"
                    ),
                    
                    form_field(
                        "Condiciones Médicas",
                        "condiciones_medicas",
                        AdminState.paciente_form["condiciones_medicas"],
                        AdminState.update_paciente_form,
                        field_type="textarea",
                        placeholder="Diabetes, hipertensión, etc. (separar con comas)"
                    ),
                    
                    form_field(
                        "Antecedentes Familiares",
                        "antecedentes_familiares",
                        AdminState.paciente_form["antecedentes_familiares"],
                        AdminState.update_paciente_form,
                        field_type="textarea",
                        placeholder="Enfermedades familiares relevantes (separar con comas)"
                    ),
                    
                    form_field(
                        "Observaciones",
                        "observaciones",
                        AdminState.paciente_form["observaciones"],
                        AdminState.update_paciente_form,
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
                        on_click=AdminState.close_paciente_modal
                    ),
                    primary_button(
                        rx.cond(
                            AdminState.selected_paciente.length() > 0,
                            "Actualizar",
                            "Crear"
                        ),
                        icon="save",
                        on_click=AdminState.save_paciente,
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
            max_width="800px",
            max_height="90vh",
            overflow_y="auto"
        )
    )

def paciente_delete_modal() -> rx.Component:
    """Modal de confirmación para eliminar paciente"""
    from dental_system.state.admin_state import AdminState
    from dental_system.components.role_specific.boss import modal_overlay
    from dental_system.components.common import secondary_button, eliminar_button
    
    return modal_overlay(
        AdminState.show_delete_confirmation,
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
                        AdminState.paciente_to_delete.length() > 0,
                        AdminState.paciente_to_delete["nombre_completo"],
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
                    on_click=AdminState.close_delete_confirmation
                ),
                eliminar_button(
                    "Eliminar",
                    icon="trash-2",
                    on_click=AdminState.delete_paciente,
                    loading=AdminState.is_loading,
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
# TABLA DE PACIENTES
# ==========================================

def pacientes_table_row(paciente: Dict[str, Any]) -> rx.Component:
    """Fila individual de la tabla de pacientes"""
    from dental_system.state.admin_state import AdminState
    
    return rx.hstack(
        # Información básica
        rx.vstack(
            rx.text(
                paciente.get("nombre_completo", "N/A"),
                size="3", 
                weight="medium",
                color=COLORS["gray"]["800"]
            ),
            rx.text(
                f"HC: {paciente.get('numero_historia', 'N/A')}",
                size="2", 
                color=COLORS["gray"]["500"]
            ),
            spacing="1",
            align_items="start",
            flex="3"
        ),
        
        # Documento
        rx.text(
            paciente.get("numero_documento", "N/A"),
            size="3", 
            color=COLORS["gray"]["600"], 
            flex="2",
            align="center"
        ),
        
        # Género con badge
        rx.badge(
            paciente.get("genero", "N/A").capitalize() if paciente.get("genero") else "N/A",
            variant="soft",
            color_scheme=rx.match(
                paciente.get("genero", ""),
                ("masculino", "blue"),
                ("femenino", "pink"),
                ("otro", "gray"),
                "gray"
            ),
            flex="1"
        ),
        
        # Edad
        rx.text(
            f"{paciente.get('edad', 'N/A')} años" if paciente.get("edad") else "N/A",
            size="3", 
            color=COLORS["gray"]["600"], 
            flex="1",
            align="center"
        ),
        
        # Teléfono/Celular
        rx.text(
            paciente.get("celular") or paciente.get("telefono") or "-",
            size="3", 
            color=COLORS["gray"]["600"], 
            align="center",
            flex="2"
        ),
        
        # Estado
        rx.badge(
            "Activo" if paciente.get("activo", False) else "Inactivo",
            variant="soft",
            color_scheme="green" if paciente.get("activo", False) else "red",
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
                    on_click=lambda: AdminState.open_paciente_modal(paciente)
                ),
                content="Editar paciente"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("trash-2", size=16),
                    size="2",
                    variant="ghost",
                    color=COLORS["error"],
                    on_click=lambda: AdminState.open_delete_confirmation(paciente)
                ),
                content="Eliminar paciente"
            ),
            # Botón de reactivar solo si está inactivo
            rx.cond(
                ~paciente.get("activo", True),
                rx.tooltip(
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        size="2",
                        variant="ghost",
                        color=COLORS["success"],
                        on_click=lambda: AdminState.reactivate_paciente(paciente)
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

def pacientes_table() -> rx.Component:
    """Tabla de pacientes con datos y acciones"""
    from dental_system.state.admin_state import AdminState
    
    return rx.box(
        # Header de la tabla
        rx.hstack(
            rx.text("Paciente", size="3", weight="medium", color=COLORS["gray"]["600"], flex="3", align="center"),
            rx.text("Documento", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2", align="center"),
            rx.text("Género", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", align="center"),
            rx.text("Edad", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", align="center"),
            rx.text("Teléfono", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2", align="center"),
            rx.text("Estado", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", align="center"),
            rx.text("Acciones", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1", align="center"),
            spacing="4",
            align="center",
            padding="16px 20px",
            background=COLORS["gray"]["50"],
            border_bottom=f"1px solid {COLORS['gray']['200']}",
            width="100%"
        ),
        
        # Filas de datos
        rx.foreach(
            AdminState.pacientes_list,
            pacientes_table_row
        ),
        
        # Mensaje cuando no hay datos
        rx.cond(
            AdminState.pacientes_list.length() == 0,
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

def pacientes_filters() -> rx.Component:
    """Filtros y búsqueda para pacientes"""
    from dental_system.state.admin_state import AdminState
    from dental_system.components.common import primary_button, secondary_button
    
    return rx.box(
        rx.vstack(
            # Primera fila: Búsqueda y botón principal
            rx.hstack(
                # Búsqueda
                rx.hstack(
                    rx.icon("search", size=20, color=COLORS["gray"]["600"]),
                    rx.input(
                        placeholder="Buscar por nombre, documento, email...",
                        value=AdminState.pacientes_search,
                        on_change=AdminState.set_pacientes_search,
                        on_blur=AdminState.apply_pacientes_filters,
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
                        on_click=lambda: AdminState.open_paciente_modal()
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
                    value=AdminState.pacientes_filter_genero,
                    on_change=AdminState.set_pacientes_filter_genero,
                    width="150px"
                ),
                rx.select(
                    ["activos", "inactivos", "todos"],
                    placeholder="Estado",
                    value=AdminState.pacientes_filter_activos,
                    on_change=AdminState.set_pacientes_filter_activos,
                    width="150px"
                ),
                rx.button(
                    "Aplicar Filtros",
                    icon="filter",
                    variant="soft",
                    on_click=AdminState.apply_pacientes_filters
                ),
                rx.button(
                    "Limpiar",
                    icon="x",
                    variant="ghost",
                    on_click=lambda: [
                        AdminState.set_pacientes_search(""),
                        AdminState.set_pacientes_filter_genero(""),
                        AdminState.set_pacientes_filter_activos("activos"),
                        AdminState.apply_pacientes_filters()
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

def pacientes_stats() -> rx.Component:
    """Estadísticas rápidas de pacientes"""
    from dental_system.state.admin_state import AdminState
    from dental_system.components.common import stat_card
    
    return rx.grid(
        stat_card(
            title="Total Pacientes",
            value=AdminState.pacientes_stats["total"].to_string(),
            icon="users",
            color=COLORS["primary"]["500"],
            trend="Pacientes registrados"
        ),
        stat_card(
            title="Nuevos este Mes",
            value=AdminState.pacientes_stats["nuevos_mes"].to_string(),
            icon="user-plus",
            color=COLORS["success"],
            trend="Registros recientes"
        ),
        stat_card(
            title="Hombres",
            value=AdminState.pacientes_stats["hombres"].to_string(),
            icon="male",
            color=COLORS["blue"]["500"],
            trend="Género masculino"
        ),
        stat_card(
            title="Mujeres",
            value=AdminState.pacientes_stats["mujeres"].to_string(),
            icon="female",
            color=COLORS["secondary"]["500"],
            trend="Género femenino"
        ),
        columns="4",
        spacing="6",
        width="100%",
        margin_bottom="24px"
    )
