# 📄 PÁGINAS SIMPLIFICADAS - CÓDIGO CLARO Y FÁCIL DE ENCONTRAR
# dental_system/pages/

import reflex as rx
from dental_system.state.app_state import AppState

from dental_system.components.common import page_header, primary_button, secondary_button
from dental_system.components.table_components import SimpleTableAdapter



def patient_form_modal() -> rx.Component:
    """📝 Modal para crear/editar paciente"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AppState.selected_paciente.length() > 0,
                    "Editar Paciente",
                    "Nuevo Paciente"
                )
            ),
            
            # Formulario
            rx.vstack(
                # Nombres
                rx.hstack(
                    rx.vstack(
                        rx.text("Primer Nombre *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.paciente_form["primer_nombre"],
                            on_change=lambda v: AppState.update_paciente_form("primer_nombre", v),
                            placeholder="Juan"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Primer Apellido *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.paciente_form["primer_apellido"],
                            on_change=lambda v: AppState.update_paciente_form("primer_apellido", v),
                            placeholder="Pérez"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Documento
                rx.hstack(
                    rx.vstack(
                        rx.text("Tipo Documento", size="2", weight="medium"),
                        rx.select(
                            ["CC", "TI", "CE", "PA"],
                            value=AppState.paciente_form["tipo_documento"],
                            on_change=lambda v: AppState.update_paciente_form("tipo_documento", v)
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Número Documento *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.paciente_form["numero_documento"],
                            on_change=lambda v: AppState.update_paciente_form("numero_documento", v),
                            placeholder="12345678"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Contacto
                rx.hstack(
                    rx.vstack(
                        rx.text("Teléfono", size="2", weight="medium"),
                        rx.input(
                            value=AppState.paciente_form["telefono_1"],
                            on_change=lambda v: AppState.update_paciente_form("telefono_1", v),
                            placeholder="300-123-4567"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Email", size="2", weight="medium"),
                        rx.input(
                            value=AppState.paciente_form["email"],
                            on_change=lambda v: AppState.update_paciente_form("email", v),
                            placeholder="paciente@email.com"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Información adicional (opcional)
                rx.vstack(
                    rx.text("Información Adicional", size="3", weight="medium", color="gray.700"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Género", size="2", weight="medium"),
                            rx.select(
                                ["masculino", "femenino", "otro"],
                                placeholder="Seleccionar género",
                                value=AppState.paciente_form["genero"],
                                on_change=lambda v: AppState.update_paciente_form("genero", v)
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Fecha Nacimiento", size="2", weight="medium"),
                            rx.input(
                                type="date",
                                value=AppState.paciente_form["fecha_nacimiento"],
                                on_change=lambda v: AppState.update_paciente_form("fecha_nacimiento", v)
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    
                    rx.vstack(
                        rx.text("Dirección", size="2", weight="medium"),
                        rx.text_area(
                            value=AppState.paciente_form["direccion"],
                            on_change=lambda v: AppState.update_paciente_form("direccion", v),
                            placeholder="Dirección completa"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    
                    spacing="3",
                    width="100%"
                ),
                
                spacing="4",
                width="100%"
            ),
            
            # Botones
            rx.hstack(
                secondary_button(
                    "Cancelar",
                    on_click=AppState.cerrar_modal_paciente
                ),
                primary_button(
                    text=rx.cond(
                        AppState.selected_paciente.length() > 0,
                        "Actualizar",
                        "Crear Paciente"
                    ),
                    icon="plus",
                    on_click=AppState.guardar_paciente,
                    loading=AppState.is_loading_pacientes
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="4"
            ),
            
            max_width="700px",
            padding="6",
            max_height="80vh",
            overflow_y="auto"
        ),
        open=AppState.show_paciente_modal,
        on_open_change=AppState.set_show_paciente_modal
    )

def delete_confirmation_modal() -> rx.Component:
    """❌ Modal de confirmación de eliminación"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar Eliminación"),
            
            rx.vstack(
                rx.icon("alert_triangle", size=48, color="red.500"),
                rx.text(
                    "¿Estás seguro de que quieres eliminar este paciente?",
                    size="3",
                    text_align="center"
                ),
                rx.text(
                    "Esta acción desactivará al paciente pero mantendrá su historial médico.",
                    size="2",
                    color="gray.500",
                    text_align="center"
                ),
                spacing="3",
                align="center"
            ),
            
            rx.hstack(
                secondary_button(
                    "Cancelar",
                    on_click=lambda: AppState.set_show_delete_paciente_confirmation(False)
                ),
                rx.button(
                    "Eliminar",
                    color_scheme="red",
                    on_click=AppState.eliminar_paciente,
                    loading=AppState.is_loading_pacientes
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="4"
            ),
            
            max_width="400px",
            padding="6"
        ),
        open=AppState.show_delete_paciente_confirmation,
        on_open_change=AppState.set_show_delete_paciente_confirmation(False)
    )

def reactivate_confirmation_modal() -> rx.Component:
    """✅ Modal de confirmación de reactivación"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar Reactivación"),
            
            rx.vstack(
                rx.icon("refresh_cw", size=48, color="green.500"),
                rx.text(
                    "¿Estás seguro de que quieres reactivar este paciente?",
                    size="3",
                    text_align="center"
                ),
                rx.text(
                    f"Paciente: {AppState.paciente_to_reactivate.get('primer_nombre', '')} {AppState.paciente_to_reactivate.get('primer_apellido', '')}",
                    size="2",
                    weight="medium",
                    text_align="center"
                ),
                rx.text(
                    "El paciente volverá a estar disponible para nuevas consultas.",
                    size="2",
                    color="gray.500",
                    text_align="center"
                ),
                spacing="3",
                align="center"
            ),
            
            rx.hstack(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    on_click=lambda: AppState.set_show_reactivate_paciente_confirmation(False)
                ),
                rx.button(
                    "Reactivar",
                    color_scheme="green",
                    on_click=AppState.ejecutar_reactivar_paciente,
                    loading=AppState.is_loading_pacientes
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="4"
            ),
            
            max_width="400px",
            padding="6"
        ),
        open=AppState.show_reactivate_paciente_confirmation,
        on_open_change=AppState.set_show_reactivate_paciente_confirmation
    )
        
# ==========================================
# 📋 PÁGINA PRINCIPAL - USANDO COMPONENTES GENÉRICOS
# ==========================================

def pacientes_page() -> rx.Component:
    """
    📋 PÁGINA DE PACIENTES CON COMPONENTES GENÉRICOS
    
    ✅ Usa tu AppState
    ✅ Usa tus componentes genéricos (simplificados)
    ✅ Mantiene filtros y búsqueda
    ✅ Fácil de entender y modificar
    """
    return rx.box(
        # Header principal
        page_header(
            title="Gestión de Pacientes",
            subtitle="Administrar información de pacientes del consultorio"
        ),
        
        # Contenido principal
        rx.box(
            # Alertas
            rx.cond(
                AppState.success_message != "",
                rx.callout(
                    AppState.success_message,
                    icon="check_circle",
                    color_scheme="green",
                    margin_bottom="4"
                ),
                rx.box()
            ),
            
            rx.cond(
                AppState.error_message != "",
                rx.callout(
                    AppState.error_message,
                    icon="warning",
                    color_scheme="red",
                    margin_bottom="4"
                ),
                rx.box()
            ),
            
            # 🎯 TABLA USANDO TUS COMPONENTES GENÉRICOS (SIMPLIFICADOS)
            SimpleTableAdapter.patients_table(),
            
            padding="6"
        ),
        
        # Modales
        patient_form_modal(),
        delete_confirmation_modal(),
        reactivate_confirmation_modal(),
        
        
        width="100%",
        min_height="100vh"
    )
