"""
🦷 PÁGINA DE CONSULTAS CORREGIDA - MODAL FUNCIONAL
Solución al problema de selección de odontólogos
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import (page_header, primary_button, secondary_button)
from dental_system.components.table_components import SimpleTableAdapter

# ==========================================
# 📝 MODAL CORREGIDO DE CONSULTA
# ==========================================

def consulta_form_modal() -> rx.Component:
    """📝 Modal CORREGIDO para consultas - Soluciona problema de odontólogos"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AppState.selected_consulta.length() > 0,
                    "Editar Consulta",
                    "Nueva Consulta"
                )
            ),
            
            # Formulario corregido
            rx.vstack(
                # ✅ SECCIÓN 1: BÚSQUEDA DE PACIENTE
                rx.text("Seleccionar Paciente", size="4", weight="medium", color="gray.700"),
                
                # Buscador inteligente de pacientes
                buscador_pacientes_simple(),
                
                rx.divider(margin="4"),
                
                # ✅ SECCIÓN 2: INFORMACIÓN DE LA CONSULTA CORREGIDA
                rx.text("Información de la Consulta", size="4", weight="medium", color="gray.700"),
                
                # ✅ ODONTÓLOGO CORREGIDO - USAR SELECT SIMPLE
                odontologo_select_corregido(),
                
                # Tipo de consulta y prioridad
                rx.hstack(
                    rx.vstack(
                        rx.text("Tipo de Consulta", size="2", weight="medium"),
                        rx.select(
                            ["general", "control", "urgencia", "cirugia", "otro"],
                            value=AppState.consulta_form["tipo_consulta"],
                            on_change=lambda v: AppState.update_consulta_form("tipo_consulta", v),
                            size="3"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Prioridad", size="2", weight="medium"),
                        rx.select(
                            ["normal", "alta", "urgente"],
                            value=AppState.consulta_form["prioridad"],
                            on_change=lambda v: AppState.update_consulta_form("prioridad", v),
                            size="3"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                
                # ✅ SECCIÓN 3: DETALLES CLÍNICOS
                rx.divider(margin="4"),
                rx.text("Detalles Clínicos", size="4", weight="medium", color="gray.700"),
                
                # Motivo de consulta
                rx.vstack(
                    rx.text("Motivo de la Consulta *", size="2", weight="medium"),
                    rx.text_area(
                        placeholder="¿Por qué viene el paciente? Síntomas, molestias, procedimiento requerido...",
                        value=AppState.consulta_form["motivo_consulta"],
                        on_change=lambda v: AppState.update_consulta_form("motivo_consulta", v),
                        rows="3",
                        resize="vertical"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                # Observaciones adicionales
                rx.vstack(
                    rx.text("Observaciones Adicionales", size="2", weight="medium"),
                    rx.text_area(
                        placeholder="Observaciones sobre la cita, preparación especial, etc.",
                        value=AppState.consulta_form["observaciones_cita"],
                        on_change=lambda v: AppState.update_consulta_form("observaciones_cita", v),
                        rows="2",
                        resize="vertical"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                spacing="4",
                width="100%"
            ),
            
            # Botones
            rx.hstack(
                secondary_button(
                    "Cancelar",
                    on_click=AppState.cerrar_modal_consulta
                ),
                primary_button(
                    text=rx.cond(
                        AppState.selected_consulta.length() > 0,
                        "Actualizar Consulta",
                        "Crear Consulta"
                    ),
                    icon="calendar-plus",
                    on_click=AppState.guardar_consulta,
                    loading=AppState.is_loading_consultas
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="6"
            ),
            
            max_width="700px",
            padding="6",
            max_height="90vh",
            overflow_y="auto"
        ),
        open=AppState.show_consulta_modal,
        on_open_change=AppState.set_show_consulta_modal
    )

# ==========================================
# 🔍 COMPONENTES AUXILIARES CORREGIDOS
# ==========================================

def buscador_pacientes_simple() -> rx.Component:
    """🔍 Buscador de pacientes SIMPLIFICADO y funcional"""
    return rx.vstack(
        rx.text("Paciente *", size="2", weight="medium"),
        
        # Contenedor del input con dropdown
        rx.box(
            # Input de búsqueda
            rx.input(
                placeholder="🔍 Buscar por nombre o documento del paciente...",
                value=AppState.pacientes_search_modal,
                on_change=AppState.buscar_pacientes_modal,
                size="3",
                width="100%"
            ),
            
            # Dropdown de resultados
            rx.cond(
                AppState.show_pacientes_dropdown,
                rx.box(
                    rx.vstack(
                        # Resultados de búsqueda
                        rx.cond(
                            AppState.pacientes_disponibles.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    AppState.pacientes_disponibles,
                                    lambda paciente: paciente_dropdown_item_simple(paciente)
                                ),
                                spacing="0",
                                width="100%"
                            ),
                            # Mensaje cuando no hay resultados
                            rx.box(
                                rx.text(
                                    "No se encontraron pacientes",
                                    size="3",
                                    color="gray.500",
                                    text_align="center"
                                ),
                                padding="3"
                            )
                        ),
                        spacing="0",
                        width="100%"
                    ),
                    
                    background="white",
                    border="1px solid var(--gray-6)",
                    border_radius="8px",
                    box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                    position="absolute",
                    top="100%",
                    left="0",
                    right="0",
                    z_index="50",
                    max_height="300px",
                    overflow_y="auto"
                ),
                rx.box()  # No mostrar dropdown
            ),
            
            position="relative",
            width="100%"
        ),
        
        # Información del paciente seleccionado
        rx.cond(
            AppState.selected_paciente_modal.length() > 0,
            rx.box(
                rx.hstack(
                    rx.icon("user", size=16, color="green.500"),
                    rx.text(
                        f"Paciente: {AppState.selected_paciente_modal.get('display_text', '')}",
                        size="2",
                        color="green.700",
                        weight="medium"
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=14),
                        size="1",
                        variant="ghost",
                        color_scheme="red",
                        on_click=AppState.limpiar_seleccion_paciente
                    ),
                    align="center",
                    width="100%"
                ),
                background="green.50",
                border="1px solid var(--green-6)",
                border_radius="6px",
                padding="2",
                margin_top="2"
            ),
            rx.box()
        ),
        
        spacing="1",
        width="100%"
    )

def paciente_dropdown_item_simple(paciente: rx.Var[dict]) -> rx.Component:
    """Item individual en el dropdown de pacientes - SIMPLIFICADO"""
    return rx.box(
        rx.hstack(
            # Información del paciente
            rx.vstack(
                rx.text(
                    f"{paciente.get('primer_nombre', '')} {paciente.get('primer_apellido', '')}",
                    size="3",
                    weight="medium",
                    color="gray.800"
                ),
                rx.text(
                    f"CC: {paciente.get('numero_documento', '')}",
                    size="2",
                    color="gray.600"
                ),
                spacing="1",
                align_items="start"
            ),
            
            spacing="3",
            align="center",
            width="100%"
        ),
        
        on_click=lambda: AppState.seleccionar_paciente_modal(paciente),
        cursor="pointer",
        padding="3",
        _hover={"background": "var(--gray-3)"},
        border_bottom="1px solid var(--gray-4)",
        width="100%"
    )

def odontologo_select_corregido() -> rx.Component:
    """✅ SELECT DE ODONTÓLOGO CORREGIDO - USA IDs CORRECTAMENTE"""
    return rx.vstack(
        rx.text("Odontólogo *", size="2", weight="medium"),
        
        # Mostrar estado de carga primero
        rx.cond(
            AppState.odontologos_list.length() > 0,
            
            # ✅ SELECT CORREGIDO - MAPEA CORRECTAMENTE ID A NOMBRE
            rx.select.root(
                rx.select.trigger(
                    placeholder="Seleccionar odontólogo...",
                    width="100%"
                ),
                rx.select.content(
                    rx.foreach(
                        AppState.odontologos_list,
                        lambda odontologo: rx.select.item(
                            f"{odontologo.primer_nombre} {odontologo.primer_apellido} - {odontologo.especialidad}".split(),
                            value=odontologo.id
                        )
                    )
                ),
                value=AppState.consulta_form["odontologo_id"],
                on_change=lambda val: AppState.update_consulta_form("odontologo_id", val),
                width="100%"
            ),
            
            # Estado de carga
            rx.hstack(
                rx.spinner(size="2"),
                rx.text("Cargando odontólogos...", size="2", color="gray.500"),
                spacing="2"
            )
        ),
        
        # ✅ MOSTRAR ODONTÓLOGO SELECCIONADO PARA DEBUG
        rx.cond(
            AppState.consulta_form["odontologo_id"] != "",
            rx.text(
                f"ID seleccionado: {AppState.consulta_form['odontologo_id']}",
                size="1",
                color="blue.600"
            ),
            rx.box()
        ),
        
        spacing="1",
        width="100%"
    )

# ==========================================
# 📊 ESTADÍSTICAS SIMPLES
# ==========================================

def consultas_stats() -> rx.Component:
    """Estadísticas simples"""
    return rx.grid(
        rx.box(
            rx.hstack(
                rx.icon("calendar", size=24, color="blue.500"),
                rx.vstack(
                    rx.text(
                        AppState.consultas_list.length().to_string(),
                        size="6",
                        weight="bold",
                        color="blue.700"
                    ),
                    rx.text("Total Hoy", size="2", color="gray.600"),
                    spacing="0"
                ),
                align="center"
            ),
            background="blue.50",
            padding="4",
            border_radius="8px"
        ),
        
        rx.box(
            rx.hstack(
                rx.icon("clock", size=24, color="yellow.500"),
                rx.vstack(
                    rx.text(
                        AppState.consultas_en_progreso.to_string(),
                        size="6",
                        weight="bold",
                        color="yellow.700"
                    ),
                    rx.text("En Progreso", size="2", color="gray.600"),
                    spacing="0"
                ),
                align="center"
            ),
            background="yellow.50",
            padding="4",
            border_radius="8px"
        ),
        
        rx.box(
            rx.hstack(
                rx.icon("check", size=24, color="green.500"),
                rx.vstack(
                    rx.text(
                        AppState.consultas_completadas.to_string(),
                        size="6",
                        weight="bold",
                        color="green.700"
                    ),
                    rx.text("Completadas", size="2", color="gray.600"),
                    spacing="0"
                ),
                align="center"
            ),
            background="green.50",
            padding="4",
            border_radius="8px"
        ),
        
        columns="3",
        spacing="4",
        width="100%",
        margin_bottom="6"
    )

# ==========================================
# 🗑️ MODAL DE CONFIRMACIÓN DE CANCELACIÓN
# ==========================================

def cancel_confirmation_modal() -> rx.Component:
    """Modal de confirmación para cancelar consulta"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Cancelar Consulta"),
            
            rx.vstack(
                rx.icon("alert_triangle", size=48, color="orange.500"),
                rx.text(
                    "¿Estás seguro de que quieres cancelar esta consulta?",
                    size="3",
                    text_align="center"
                ),
                rx.text(
                    f"Consulta: {AppState.consulta_to_cancel.get('numero_consulta', '')}",
                    size="2",
                    weight="medium",
                    text_align="center"
                ),
                rx.text(
                    f"Paciente: {AppState.consulta_to_cancel.get('paciente_nombre_completo', '')}",
                    size="2",
                    color="gray.600",
                    text_align="center"
                ),
                
                # Campo para motivo de cancelación
                rx.vstack(
                    rx.text("Motivo de cancelación:", size="2", weight="medium"),
                    rx.text_area(
                        placeholder="Escriba el motivo de la cancelación...",
                        value=AppState.motivo_cancelacion,
                        on_change=AppState.set_motivo_cancelacion,
                        rows="3",
                        width="100%"
                    ),
                    spacing="1",
                    width="100%",
                    margin_top="4"
                ),
                
                spacing="3",
                align="center"
            ),
            
            rx.hstack(
                secondary_button(
                    "No Cancelar",
                    on_click=lambda: AppState.set_show_cancel_confirmation(False)
                ),
                rx.button(
                    "Cancelar Consulta",
                    color_scheme="red",
                    on_click=AppState.ejecutar_cancelar_consulta,
                    loading=AppState.is_loading_consultas
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="4"
            ),
            
            max_width="500px",
            padding="6"
        ),
        open=AppState.show_cancel_confirmation,
        on_open_change=AppState.set_show_cancel_confirmation
    )

# ==========================================
# 🦷 PÁGINA PRINCIPAL CORREGIDA
# ==========================================

def consultas_page() -> rx.Component:
    """🦷 Página de consultas CORREGIDA - Soluciona problema de odontólogos"""
    return rx.box(
        # Header
        page_header(
            title="Gestión de Consultas",
            subtitle="Programar y administrar citas del día"
        ),
        
        # Contenido
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
            
            # Stats simples
            consultas_stats(),
            
            # Tabla usando el adaptador existente
            SimpleTableAdapter.consultas_table(),
            
            padding="6"
        ),
        
        # Modales
        consulta_form_modal(),
        cancel_confirmation_modal(),
        
        width="100%",
        min_height="100vh",
        
        # ✅ CARGAR DATOS AL MONTAR - CORREGIDO
        on_mount=[
            # AppState.load_odontologos_list,  # ✅ CARGAR PRIMERO LOS ODONTÓLOGOS
            AppState.load_consultas_list     # LUEGO LAS CONSULTAS
        ]
    )
# """
# 🦷 PÁGINA DE CONSULTAS COMPLETA - VERSIÓN FINAL
# Incluye todos los modales, filtros, búsqueda y acciones necesarias
# """

# import reflex as rx
# from dental_system.state.app_state import AppState
# from dental_system.components.common import (page_header, primary_button, secondary_button)
# from dental_system.components.table_components import SimpleTableAdapter

# # ==========================================
# # 📝 MODAL PRINCIPAL DE CONSULTA - MEJORADO
# # ==========================================

# def consulta_form_modal() -> rx.Component:
#     """📝 Modal para crear/editar consulta con validación mejorada"""
#     return rx.dialog.root(
#         rx.dialog.content(
#             rx.dialog.title(
#                 rx.cond(
#                     AppState.selected_consulta.length() > 0,
#                     "Editar Consulta",
#                     "Nueva Consulta"
#                 )
#             ),
            
#             # Formulario completo
#             rx.vstack(
#                 # ✅ SECCIÓN 1: BÚSQUEDA DE PACIENTE
#                 rx.text("Seleccionar Paciente", size="4", weight="medium", color="gray.700"),
                
#                 # Buscador inteligente de pacientes
#                 buscador_pacientes_inteligente(),
                
#                 rx.divider(margin="4"),
                
#                 # ✅ SECCIÓN 2: INFORMACIÓN DE LA CONSULTA
#                 rx.text("Información de la Consulta", size="4", weight="medium", color="gray.700"),
                
#                 # Odontólogo (usando ID como value)
#                 rx.vstack(
#                     rx.text("Odontólogo *", size="2", weight="medium"),
#                     rx.cond(
#                         AppState.odontologos_list.length() > 0,
#                         rx.select(
#                             # Lista de opciones con formato "Nombre - Especialidad"
#                             [f"{o.get('nombre_completo', '')} - {o.get('especialidad', 'General')}" for o in AppState.odontologos_list],
#                             placeholder="Seleccionar odontólogo",
#                             value=AppState.consulta_form["odontologo_id"], 
#                             on_change=lambda v: AppState.update_consulta_form("odontologo_id", v),
#                             size="3"
#                         ),
#                         rx.text("Cargando odontólogos...", size="2", color="gray.500")
#                     ),
#                     spacing="1",
#                     width="100%"
#                 ),
                
#                 # Fecha y hora - USANDO LOS CAMPOS EXACTOS DEL APPSTATE
#                 rx.hstack(
#                     rx.vstack(
#                         rx.text("Fecha *", size="2", weight="medium"),
#                         rx.input(
#                             type="date",
#                             value=AppState.consulta_form["fecha_programada"],
#                             on_change=lambda v: AppState.update_consulta_form("fecha_programada", v),
#                             size="3"
#                         ),
#                         spacing="1",
#                         width="100%"
#                     ),
#                     rx.vstack(
#                         rx.text("Hora *", size="2", weight="medium"),
#                         rx.input(
#                             type="time",
#                             value=AppState.consulta_form["hora_programada"],
#                             on_change=lambda v: AppState.update_consulta_form("hora_programada", v),
#                             size="3"
#                         ),
#                         spacing="1",
#                         width="100%"
#                     ),
#                     spacing="3",
#                     width="100%"
#                 ),
                
#                 # Tipo de consulta y prioridad
#                 rx.hstack(
#                     rx.vstack(
#                         rx.text("Tipo de Consulta", size="2", weight="medium"),
#                         rx.select(
#                             ["general", "control", "urgencia", "cirugia", "otro"],
#                             value=AppState.consulta_form["tipo_consulta"],
#                             on_change=lambda v: AppState.update_consulta_form("tipo_consulta", v),
#                             size="3"
#                         ),
#                         spacing="1",
#                         width="100%"
#                     ),
#                     rx.vstack(
#                         rx.text("Prioridad", size="2", weight="medium"),
#                         rx.select(
#                             ["normal", "alta", "urgente"],
#                             value=AppState.consulta_form["prioridad"],
#                             on_change=lambda v: AppState.update_consulta_form("prioridad", v),
#                             size="3"
#                         ),
#                         spacing="1",
#                         width="100%"
#                     ),
#                     spacing="3",
#                     width="100%"
#                 ),
                
#                 # ✅ SECCIÓN 3: DETALLES CLÍNICOS
#                 rx.divider(margin="4"),
#                 rx.text("Detalles Clínicos", size="4", weight="medium", color="gray.700"),
                
#                 # Motivo de consulta
#                 rx.vstack(
#                     rx.text("Motivo de la Consulta *", size="2", weight="medium"),
#                     rx.text_area(
#                         placeholder="¿Por qué viene el paciente? Síntomas, molestias, procedimiento requerido...",
#                         value=AppState.consulta_form["motivo_consulta"],
#                         on_change=lambda v: AppState.update_consulta_form("motivo_consulta", v),
#                         rows="3",
#                         resize="vertical"
#                     ),
#                     spacing="1",
#                     width="100%"
#                 ),
                
#                 # Observaciones adicionales
#                 rx.vstack(
#                     rx.text("Observaciones Adicionales", size="2", weight="medium"),
#                     rx.text_area(
#                         placeholder="Observaciones sobre la cita, preparación especial, etc.",
#                         value=AppState.consulta_form["observaciones_cita"],
#                         on_change=lambda v: AppState.update_consulta_form("observaciones_cita", v),
#                         rows="2",
#                         resize="vertical"
#                     ),
#                     spacing="1",
#                     width="100%"
#                 ),
                
#                 spacing="4",
#                 width="100%"
#             ),
            
#             # Botones
#             rx.hstack(
#                 secondary_button(
#                     "Cancelar",
#                     on_click=AppState.cerrar_modal_consulta
#                 ),
#                 primary_button(
#                     text=rx.cond(
#                         AppState.selected_consulta.length() > 0,
#                         "Actualizar Consulta",
#                         "Crear Consulta"
#                     ),
#                     icon="calendar-plus",
#                     on_click=AppState.guardar_consulta,
#                     loading=AppState.is_loading_consultas
#                 ),
#                 spacing="3",
#                 justify="end",
#                 width="100%",
#                 margin_top="6"
#             ),
            
#             max_width="700px",
#             padding="6",
#             max_height="90vh",
#             overflow_y="auto"
#         ),
#         open=AppState.show_consulta_modal,
#         on_open_change=AppState.set_show_consulta_modal
#     )

# # ==========================================
# # 🔍 BUSCADOR DE PACIENTES INTELIGENTE
# # ==========================================

# def buscador_pacientes_inteligente() -> rx.Component:
#     """🔍 Buscador de pacientes con dropdown en tiempo real"""
#     return rx.box(
#         # Input principal con información del paciente seleccionado
#         rx.vstack(
#             rx.text("Paciente *", size="2", weight="medium"),
            
#             # Contenedor del input con dropdown
#             rx.box(
#                 # Input de búsqueda
#                 rx.input(
#                     placeholder="🔍 Buscar por nombre o documento del paciente...",
#                     value=AppState.pacientes_search_modal,
#                     on_change=AppState.buscar_pacientes_modal,
#                     on_focus=lambda: AppState.buscar_pacientes_modal(AppState.pacientes_search_modal),
#                     size="3",
#                     width="100%"
#                 ),
                
#                 # Dropdown de resultados
#                 rx.cond(
#                     AppState.show_pacientes_dropdown,
#                     rx.box(
#                         rx.vstack(
#                             # Resultados de búsqueda
#                             rx.cond(
#                                 AppState.pacientes_disponibles.length() > 0,
#                                 rx.vstack(
#                                     rx.foreach(
#                                         AppState.pacientes_disponibles,
#                                         lambda paciente: paciente_dropdown_item(paciente)
#                                     ),
#                                     spacing="0",
#                                     width="100%"
#                                 ),
#                                 # Mensaje cuando no hay resultados
#                                 rx.box(
#                                     rx.text(
#                                         "No se encontraron pacientes",
#                                         size="3",
#                                         color="gray.500",
#                                         text_align="center"
#                                     ),
#                                     padding="3"
#                                 )
#                             ),
                            
#                             # Opción para crear nuevo paciente
#                             rx.divider(),
#                             rx.box(
#                                 rx.button(
#                                     rx.icon("plus", size=16),
#                                     "Crear nuevo paciente", 
#                                     variant="ghost",
#                                     color_scheme="blue",
#                                     size="2",
#                                     width="100%",
#                                     on_click=AppState.abrir_modal_consulta
#                                 ),
#                                 padding="2"
#                             ),
                            
#                             spacing="0",
#                             width="100%"
#                         ),
                        
#                         background="white",
#                         border="1px solid var(--gray-6)",
#                         border_radius="8px",
#                         box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
#                         position="absolute",
#                         top="100%",
#                         left="0",
#                         right="0",
#                         z_index="50",
#                         max_height="300px",
#                         overflow_y="auto"
#                     ),
#                     rx.box()  # No mostrar dropdown
#                 ),
                
#                 position="relative",
#                 width="100%"
#             ),
            
#             # Información del paciente seleccionado
#             rx.cond(
#                 AppState.selected_paciente_modal.length() > 0,
#                 rx.box(
#                     rx.hstack(
#                         rx.icon("user", size=16, color="green.500"),
#                         rx.text(
#                             f"Paciente: {AppState.selected_paciente_modal.get('display_text', '')}",
#                             size="2",
#                             color="green.700",
#                             weight="medium"
#                         ),
#                         rx.spacer(),
#                         rx.button(
#                             rx.icon("x", size=14),
#                             size="1",
#                             variant="ghost",
#                             color_scheme="red",
#                             on_click=AppState.limpiar_seleccion_paciente
#                         ),
#                         align="center",
#                         width="100%"
#                     ),
#                     background="green.50",
#                     border="1px solid var(--green-6)",
#                     border_radius="6px",
#                     padding="2",
#                     margin_top="2"
#                 ),
#                 rx.box()
#             ),
            
#             spacing="1",
#             width="100%"
#         ),
        
#         width="100%"
#     )
    
# def paciente_dropdown_item(paciente: rx.Var[dict]) -> rx.Component:
#     """Item individual en el dropdown de pacientes"""
#     return rx.box(
#         rx.hstack(
#             # Avatar o icono
#             rx.box(
#                 rx.icon("user", size=16, color="gray.500"),
#                 background="gray.100",
#                 border_radius="50%",
#                 padding="2",
#                 width="32px",
#                 height="32px",
#                 display="flex",
#                 align_items="center",
#                 justify_content="center"
#             ),
            
#             # Información del paciente
#             rx.vstack(
#                 rx.text(
#                     f"{paciente.get('primer_nombre', '')} {paciente.get('primer_apellido', '')}",
#                     size="3",
#                     weight="medium",
#                     color="gray.800"
#                 ),
#                 rx.hstack(
#                     rx.text(
#                         f"CC: {paciente.get('numero_documento', '')}",
#                         size="2",
#                         color="gray.600"
#                     ),
#                     rx.cond(
#                         paciente.get('telefono_1'),
#                         rx.text(
#                             f"Tel: {paciente.get('telefono_1', '')}",
#                             size="2",
#                             color="gray.600"
#                         ),
#                         rx.box()
#                     ),
#                     spacing="3"
#                 ),
#                 spacing="1",
#                 align_items="start"
#             ),
            
#             spacing="3",
#             align="center",
#             width="100%"
#         ),
        
#         on_click=lambda: AppState.seleccionar_paciente_modal(paciente),
#         cursor="pointer",
#         padding="3",
#         _hover={"background": "var(--gray-3)"},
#         border_bottom="1px solid var(--gray-4)",
#         width="100%"
#     )

# # ==========================================
# # 🗑️ MODAL DE CONFIRMACIÓN DE ACCIONES
# # ==========================================

# def cancel_confirmation_modal() -> rx.Component:
#     """Modal de confirmación para cancelar consulta"""
#     return rx.dialog.root(
#         rx.dialog.content(
#             rx.dialog.title("Cancelar Consulta"),
            
#             rx.vstack(
#                 rx.icon("alert_triangle", size=48, color="orange.500"),
#                 rx.text(
#                     "¿Estás seguro de que quieres cancelar esta consulta?",
#                     size="3",
#                     text_align="center"
#                 ),
#                 rx.text(
#                     f"Consulta: {AppState.consulta_to_cancel.get('numero_consulta', '')}",
#                     size="2",
#                     weight="medium",
#                     text_align="center"
#                 ),
#                 rx.text(
#                     f"Paciente: {AppState.consulta_to_cancel.get('paciente_nombre', '')}",
#                     size="2",
#                     color="gray.600",
#                     text_align="center"
#                 ),
                
#                 # Campo para motivo de cancelación
#                 rx.vstack(
#                     rx.text("Motivo de cancelación:", size="2", weight="medium"),
#                     rx.text_area(
#                         placeholder="Escriba el motivo de la cancelación...",
#                         value=AppState.motivo_cancelacion,
#                         on_change=AppState.set_motivo_cancelacion,
#                         rows="3",
#                         width="100%"
#                     ),
#                     spacing="1",
#                     width="100%",
#                     margin_top="4"
#                 ),
                
#                 spacing="3",
#                 align="center"
#             ),
            
#             rx.hstack(
#                 secondary_button(
#                     "No Cancelar",
#                     on_click=lambda: AppState.set_show_cancel_confirmation(False)
#                 ),
#                 rx.button(
#                     "Cancelar Consulta",
#                     color_scheme="red",
#                     on_click=AppState.ejecutar_cancelar_consulta,
#                     loading=AppState.is_loading_consultas
#                 ),
#                 spacing="3",
#                 justify="end",
#                 width="100%",
#                 margin_top="4"
#             ),
            
#             max_width="500px",
#             padding="6"
#         ),
#         open=AppState.show_cancel_confirmation,
#         on_open_change=AppState.set_show_cancel_confirmation
#     )

# # ==========================================
# # 📊 ESTADÍSTICAS DE CONSULTAS
# # ==========================================

# def consultas_stats() -> rx.Component:
#     """Estadísticas rápidas de consultas del día"""
#     return rx.grid(
#         # Total consultas hoy
#         rx.box(
#             rx.hstack(
#                 rx.icon("calendar", size=24, color="blue.500"),
#                 rx.vstack(
#                     rx.text(
#                         AppState.consultas_filtradas.length().to_string(),
#                         size="6",
#                         weight="bold",
#                         color="blue.700"
#                     ),
#                     rx.text(
#                         "Consultas Hoy",
#                         size="2",
#                         color="gray.600"
#                     ),
#                     spacing="0",
#                     align_items="start"
#                 ),
#                 align="center"
#             ),
#             background="blue.50",
#             padding="4",
#             border_radius="8px",
#             border="1px solid var(--blue-6)"
#         ),
        
#         # En progreso
#         rx.box(
#             rx.hstack(
#                 rx.icon("clock", size=24, color="yellow.500"),
#                 rx.vstack(
#                     rx.text(
#                         AppState.consultas_en_progreso.to_string(),
#                         size="6",
#                         weight="bold",
#                         color="yellow.700"
#                     ),
#                     rx.text(
#                         "En Progreso",
#                         size="2",
#                         color="gray.600"
#                     ),
#                     spacing="0",
#                     align_items="start"
#                 ),
#                 align="center"
#             ),
#             background="yellow.50",
#             padding="4",
#             border_radius="8px",
#             border="1px solid var(--yellow-6)"
#         ),
        
#         # Completadas
#         rx.box(
#             rx.hstack(
#                 rx.icon("check_circle", size=24, color="green.500"),
#                 rx.vstack(
#                     rx.text(
#                         AppState.consultas_completadas.to_string(),
#                         size="6",
#                         weight="bold",
#                         color="green.700"
#                     ),
#                     rx.text(
#                         "Completadas",
#                         size="2",
#                         color="gray.600"
#                     ),
#                     spacing="0",
#                     align_items="start"
#                 ),
#                 align="center"
#             ),
#             background="green.50",
#             padding="4",
#             border_radius="8px",
#             border="1px solid var(--green-6)"
#         ),
        
#         # Programadas
#         rx.box(
#             rx.hstack(
#                 rx.icon("calendar_check", size=24, color="purple.500"),
#                 rx.vstack(
#                     rx.text(
#                         AppState.consultas_programadas.to_string(),
#                         size="6",
#                         weight="bold",
#                         color="purple.700"
#                     ),
#                     rx.text(
#                         "Programadas",
#                         size="2",
#                         color="gray.600"
#                     ),
#                     spacing="0",
#                     align_items="start"
#                 ),
#                 align="center"
#             ),
#             background="purple.50",
#             padding="4",
#             border_radius="8px",
#             border="1px solid var(--purple-6)"
#         ),
        
#         columns="4",
#         spacing="4",
#         width="100%",
#         margin_bottom="6"
#     )

# # ==========================================
# # 🦷 PÁGINA DE CONSULTAS - VERSIÓN COMPLETA
# # ==========================================

# def consultas_page() -> rx.Component:
#     """
#     🦷 PÁGINA DE CONSULTAS COMPLETA
#     - Lista completa de consultas con información detallada
#     - Búsqueda y filtros avanzados
#     - Modal para crear/editar consultas con buscador de pacientes
#     - Acciones contextuales por estado
#     - Estadísticas en tiempo real
#     """
#     return rx.box(
#         # Header de la página
#         page_header(
#             title="Gestión de Consultas",
#             subtitle="Programar y administrar citas médicas del día",
#         ),
        
#         # Contenido principal
#         rx.box(
#             # Alertas de estado
#             rx.cond(
#                 AppState.success_message != "",
#                 rx.callout(
#                     AppState.success_message,
#                     icon="check_circle",
#                     color_scheme="green",
#                     margin_bottom="4"
#                 ),
#                 rx.box()
#             ),
            
#             rx.cond(
#                 AppState.error_message != "",
#                 rx.callout(
#                     AppState.error_message,
#                     icon="warning",
#                     color_scheme="red",
#                     margin_bottom="4"
#                 ),
#                 rx.box()
#             ),
            
#             # Estadísticas rápidas
#             consultas_stats(),
            
#             # Tabla principal de consultas
#             SimpleTableAdapter.consultas_table(),
            
#             padding="6"
#         ),
        
#         # Modales
#         consulta_form_modal(),
#         cancel_confirmation_modal(),
        
#         width="100%",
#         min_height="100vh",
        
#         # Cargar datos al montar la página - CORREGIDO
#         on_mount=[
#             AppState.load_consultas_list,
#             AppState.load_odontologos_list  # Cargar odontólogos para filtros
#         ]
#     )