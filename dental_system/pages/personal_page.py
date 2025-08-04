"""
Página de gestión de personal para el gerente - VERSIÓN ACTUALIZADA CON CRUD COMPLETO
Incluye todas las funcionalidades corregidas del boss_state
"""

import reflex as rx
# from dental_system.components.common import stat_card, primary_button,secondary_button,eliminar_button
from dental_system.components.common import ( stat_card, primary_button, secondary_button, eliminar_button, page_header )
from dental_system.components.table_components import SimpleTableAdapter
from dental_system.state.boss_state import BossState
from dental_system.state.app_state import AppState
from dental_system.models import PersonalModel
from dental_system.styles.themes import COLORS

# ==========================================
# MODAL DE CONFIRMACIÓN DE ELIMINACIÓN
# ==========================================

def delete_personal_confirmation_modal() -> rx.Component:
    """❌ Modal de confirmación de eliminación de personal"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar Eliminación"),
            
            rx.vstack(
                rx.icon("alert_triangle", size=48, color="red.500"),
                rx.text(
                    "¿Estás seguro de que quieres eliminar este personal?",
                    size="3",
                    text_align="center"
                ),
                rx.text(
                    "Esta acción desactivará al personal pero mantendrá su historial en el sistema.",
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
                    on_click=lambda: AppState.set_show_delete_personal_confirmation(False)
                ),
                rx.button(
                    "Eliminar",
                    color_scheme="red",
                    on_click=AppState.eliminar_personal,
                    loading=AppState.is_loading_personal
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="4"
            ),
            
            max_width="400px",
            padding="6"
        ),
        open=AppState.show_delete_personal_confirmation,
        on_open_change=lambda x: AppState.set_show_delete_personal_confirmation(x)
    )


# ==========================================
# MODAL DE PERSONAL 
# ==========================================

def personal_form_modal() -> rx.Component:
    """📝 Modal para crear/editar personal"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AppState.selected_personal.length() > 0,
                    "Editar Personal",
                    "Nuevo Personal"
                )
            ),
            
            # Formulario
            rx.vstack(
                # Información Personal
                rx.text("Información Personal", size="4", weight="medium", color="gray.700"),
                
                # Nombres
                rx.hstack(
                    rx.vstack(
                        rx.text("Primer Nombre *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["primer_nombre"],
                            on_change=lambda v: AppState.update_personal_form("primer_nombre", v),
                            placeholder="Juan"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Segundo Nombre", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["segundo_nombre"],
                            on_change=lambda v: AppState.update_personal_form("segundo_nombre", v),
                            placeholder="Carlos (opcional)"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Primer Apellido *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["primer_apellido"],
                            on_change=lambda v: AppState.update_personal_form("primer_apellido", v),
                            placeholder="Pérez"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Segundo Apellido", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["segundo_apellido"],
                            on_change=lambda v: AppState.update_personal_form("segundo_apellido", v),
                            placeholder="González (opcional)"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Email y contraseña
                rx.hstack(
                    rx.vstack(
                        rx.text("Email *", size="2", weight="medium"),
                        rx.input(
                            type="email",
                            value=AppState.personal_form["email"],
                            on_change=lambda v: AppState.update_personal_form("email", v),
                            placeholder="usuario@dental.com"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    # Contraseña solo para nuevos usuarios
                    rx.cond(
                        AppState.selected_personal.length() == 0,
                        rx.vstack(
                            rx.text("Contraseña *", size="2", weight="medium"),
                            rx.input(
                                type="password",
                                value=AppState.personal_form["password"],
                                on_change=lambda v: AppState.update_personal_form("password", v),
                                placeholder="Mínimo 8 caracteres"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Teléfono", size="2", weight="medium"),
                            rx.input(
                                value=AppState.personal_form["telefono"],
                                on_change=lambda v: AppState.update_personal_form("telefono", v),
                                placeholder="+58 414-1234567"
                            ),
                            spacing="1",
                            width="100%"
                        )
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Mostrar teléfono separado si estamos editando
                rx.cond(
                    AppState.selected_personal.length() > 0,
                    rx.vstack(
                        rx.text("Teléfono", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["telefono"],
                            on_change=lambda v: AppState.update_personal_form("telefono", v),
                            placeholder="+58 414-1234567"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.box()
                ),
                
                # Documento y celular
                rx.hstack(
                    rx.vstack(
                        rx.text("Número Documento *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["numero_documento"],
                            on_change=lambda v: AppState.update_personal_form("numero_documento", v),
                            placeholder="12345678"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Celular *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["celular"],
                            on_change=lambda v: AppState.update_personal_form("celular", v),
                            placeholder="+58 424-7654321"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Dirección
                rx.vstack(
                    rx.text("Dirección", size="2", weight="medium"),
                    rx.text_area(
                        value=AppState.personal_form["direccion"],
                        on_change=lambda v: AppState.update_personal_form("direccion", v),
                        placeholder="Dirección completa"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                # Información Profesional
                rx.text("Información Profesional", size="4", weight="medium", color="gray.700", margin_top="4"),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Tipo Personal *", size="2", weight="medium"),
                        rx.select(
                            ["Odontólogo", "Asistente", "Administrador", "Gerente"],
                            value=AppState.personal_form["tipo_personal"],
                            on_change=lambda v: AppState.update_personal_form("tipo_personal", v)
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Especialidad", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["especialidad"],
                            on_change=lambda v: AppState.update_personal_form("especialidad", v),
                            placeholder="Ej: Endodoncia, Ortodoncia"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Número Licencia", size="2", weight="medium"),
                        rx.input(
                            value=AppState.personal_form["numero_licencia"],
                            on_change=lambda v: AppState.update_personal_form("numero_licencia", v),
                            placeholder="Número de licencia profesional"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Salario", size="2", weight="medium"),
                        rx.input(
                            type="number",
                            value=AppState.personal_form["salario"],
                            on_change=lambda v: AppState.update_personal_form("salario", v),
                            placeholder="1000000"
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
                    on_click=AppState.cerrar_modal_personal
                ),
                primary_button(
                    text=rx.cond(
                        AppState.selected_personal.length() > 0,
                        "Actualizar",
                        "Crear Personal"
                    ),
                    icon="plus",
                    on_click=AppState.guardar_personal,
                    loading=AppState.is_loading_personal
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
        open=AppState.show_personal_modal,
        on_open_change=AppState.set_show_personal_modal
    )

# # ==========================================
# # TABLA DE PERSONAL 
# # ==========================================

# def personal_table_row(person_data: PersonalModel) -> rx.Component:
#     """Fila individual de la tabla de personal - ACTUALIZADA"""
#     return rx.hstack(
#         # Avatar y nombre
       
#         rx.vstack(
#             rx.text(
#                 rx.cond(
#                     person_data.primer_nombre,
#                     f"{person_data.primer_nombre} {person_data.primer_apellido}".strip(),
#                     "N/A"
#                 ),
#                 size="3", 
#                 weight="medium",
#                 color=COLORS["gray"]["800"]
#             ),
#             rx.text(
#                 rx.cond(
#                     person_data.usuarios.email,
#                     person_data.usuarios.email,
#                     "N/A"
#                 ),
#                 size="2", 
#                 color=COLORS["gray"]["500"]
#             ),
#             spacing="1",
#             align="center",
#             flex="3"
#         ),
        
#         # Tipo con badge
#         rx.badge(
#             person_data.tipo_personal,
#             variant="soft",
#             color_scheme=rx.match(
#                 person_data.tipo_personal,
#                 ("Odontólogo", "green"),
#                 ("Administrador", "blue"),
#                 ("Asistente", "yellow"),
#                 ("Gerente", "purple"),
#                 "gray"
#             ),
            
#             align="center",
#             flex="1",
            
#         ),
        
#         # Especialidad
#         rx.text(
#             rx.cond(
#                 person_data.especialidad,
#                 person_data.especialidad,
#                 "-"   
#             ),
#             size="3", 
#             color=COLORS["gray"]["600"], 
#             flex="2",
#             align="center",
#         ),
        
#         # Estado con badge
#         rx.badge(
#             person_data.estado_laboral.capitalize(),
#             variant="soft",
#             color_scheme=rx.match(
#                 person_data.estado_laboral,
#                 ("activo", "green"),
#                 ("inactivo", "red"),
#                 ("vacaciones", "yellow"),
#                 "gray"
#             ),
#             flex="1"
#         ),
        
#         # Teléfono
#         rx.text(
#             rx.cond(
#                 person_data.usuarios.telefono,
#                 person_data.usuarios.telefono,
#                 "-"
#             ),
#             size="3", 
#             color=COLORS["gray"]["600"], 
#             align="center",
#             flex="2"
#         ),
        
#         # Acciones
#         rx.hstack(
#             rx.tooltip(
#                 rx.button(
#                     rx.icon("edit", size=16),
#                     size="2",
#                     variant="ghost",
#                     color=COLORS["primary"]["500"],
#                     on_click=lambda: BossState.open_personal_modal({
#                         "id": person_data.id,
#                         "numero_documento": person_data.numero_documento,
#                         "tipo_personal": person_data.tipo_personal,
#                         "especialidad": person_data.especialidad,
#                         "estado_laboral": person_data.estado_laboral,
#                         "numero_licencia": person_data.numero_licencia,
#                         "celular": person_data.celular,
#                         "direccion": person_data.direccion,
#                         "salario": person_data.salario,
#                         # CAMPOS SEPARADOS
#                         "primer_nombre": person_data.primer_nombre,
#                         "segundo_nombre": person_data.segundo_nombre,
#                         "primer_apellido": person_data.primer_apellido,
#                         "segundo_apellido": person_data.segundo_apellido,
#                         "usuarios": {
#                             "id": person_data.usuarios.id,
#                             "nombre_completo": person_data.nombre_completo_display,
#                             "email": person_data.usuarios.email,
#                             "telefono": person_data.usuarios.telefono,
#                             "activo": person_data.usuarios.activo
#                         }
#                     }) # type: ignore
#                 ),
#                 content="Editar personal"
#             ),
#             rx.tooltip(
#                 rx.button(
#                     rx.icon("key", size=16),
#                     size="2",
#                     variant="ghost",
#                     color=COLORS["secondary"]["500"]
#                 ),
#                 content="Resetear contraseña"
#             ),
#             rx.tooltip(
#                 rx.button(
#                     rx.icon("trash-2", size=16),
#                     size="2",
#                     variant="ghost",
#                     color=COLORS["error"],
#                     on_click=lambda: BossState.open_delete_confirmation({
#                         "id": person_data.id,
#                         "usuarios": {
#                             "id": person_data.usuarios.id,
#                             "nombre_completo": person_data.nombre_completo_display,
#                             "email": person_data.usuarios.email
#                         }
#                     })
#                 ),
#                 content="Eliminar personal"
#             ),
#             # Botón de reactivar solo si está inactivo
#             rx.cond(
#                 person_data.estado_laboral == "inactivo",
#                 rx.tooltip(
#                     rx.button(
#                         rx.icon("refresh-cw", size=16),
#                         size="2",
#                         variant="ghost",
#                         color=COLORS["success"],
#                         on_click=lambda: BossState.reactivate_personal({
#                             "id": person_data.id,
#                             "usuarios": {
#                                 "id": person_data.usuarios.id,
#                                 "nombre_completo": person_data.nombre_completo_display
#                             }
#                         })
#                     ),
#                     content="Reactivar personal"
#                 ),
#                 rx.box()
#             ),
#             spacing="1",
#             align="center",
#             flex="1"
#         ),
        
#         spacing="4",
#         align="center",
#         padding="16px 20px",
#         border_bottom=f"1px solid {COLORS['gray']['100']}",
#         _hover={"background": COLORS["gray"]["50"]},
#         width="100%"
#     )


# def personal_table() -> rx.Component:
#     """Tabla de personal con datos y acciones - ACTUALIZADA"""
#     return rx.box(
#         # Header de la tabla
#         rx.hstack(
#             rx.text("Nombre", size="3", weight="medium", color=COLORS["gray"]["600"], flex="3",align="center"),
#             rx.text("Tipo", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1",align="center"),
#             rx.text("Especialidad", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2",align="center"),
#             rx.text("Estado", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1",align="center"),
#             rx.text("Teléfono", size="3", weight="medium", color=COLORS["gray"]["600"], flex="2",align="center"),
#             rx.text("Acciones", size="3", weight="medium", color=COLORS["gray"]["600"], flex="1",align="center"),
#             spacing="4",
#             align="center",
#             padding="16px 20px",
#             background=COLORS["gray"]["50"],
#             border_bottom=f"1px solid {COLORS['gray']['200']}",
#             width="100%"
#         ),
        
#         # Filas de datos
#         rx.foreach(
#             BossState.personal_list,
#             personal_table_row
#         ),
        
#         # Mensaje cuando no hay datos
#         rx.cond(
#             BossState.personal_list.length() == 0,
#             rx.center(
#                 rx.vstack(
#                     rx.icon("users", size=48, color=COLORS["gray"]["400"]),
#                     rx.text("No hay personal registrado", 
#                            size="4", 
#                            color=COLORS["gray"]["500"],
#                            weight="medium"),
#                     rx.text("Haz clic en 'Nuevo Personal' para agregar el primer miembro del equipo", 
#                            size="3", 
#                            color=COLORS["gray"]["400"],
#                            text_align="center"),
#                     spacing="3",
#                     align="center"
#                 ),
#                 padding="60px"
#             ),
#             rx.box()
#         ),
        
#         background="white",
#         border_radius="12px",
#         border=f"1px solid {COLORS['gray']['200']}",
#         overflow="hidden",
#         width="100%"
#     )

# ==========================================
# FILTROS Y BÚSQUEDA - FUNCIONALES
# ==========================================

# def personal_filters() -> rx.Component:
#     """Filtros y búsqueda para el personal - FUNCIONALES"""
#     return rx.box(
#         rx.vstack(
#             # Primera fila: Búsqueda y botón principal
#             rx.hstack(
#                 # Búsqueda
#                 rx.hstack(
#                     rx.icon("search", size=20, color=COLORS["gray"]["600"]),
#                     rx.input(
#                         placeholder="Buscar por nombre, email o documento...",
#                         value=BossState.personal_search,
#                         on_change=BossState.set_personal_search,
#                         on_blur=BossState.apply_personal_filters,
#                         width="350px",
#                         border=f"1px solid {COLORS['gray']['300']}",
#                         border_radius="8px",
#                         _focus={"border_color": COLORS["primary"]["500"]}
#                     ),
#                     spacing="2",
#                     align="center"
#                 ),
                
#                 rx.spacer(),
                
#                 # Botones de acción
#                 rx.hstack(
#                     secondary_button(
#                         "Exportar",
#                         icon="download"
#                     ),
#                     primary_button(
#                         "Nuevo Personal",
#                         icon="user-plus",
#                         on_click=lambda: BossState.open_personal_modal()
#                     ),
#                     spacing="3"
#                 ),
                
#                 align="center",
#                 width="100%"
#             ),
            
#             # Segunda fila: Filtros
#             rx.hstack(
#                 rx.select(
#                     ["todos", "Odontólogo", "Administrador", "Asistente", "Gerente"],
#                     placeholder="Tipo de personal",
#                     value=BossState.personal_filter_tipo,
#                     on_change=BossState.set_personal_filter_tipo,
#                     width="200px"
#                 ),
#                 rx.select(
#                     ["todos", "activo", "inactivo", "vacaciones"],
#                     placeholder="Estado laboral",
#                     value=BossState.personal_filter_estado,
#                     on_change=BossState.set_personal_filter_estado,
#                     width="200px"
#                 ),
#                 rx.button(
#                     "Aplicar Filtros",
#                     icon="filter",
#                     variant="soft",
#                     on_click=BossState.apply_personal_filters
#                 ),
#                 rx.button(
#                     "Limpiar",
#                     icon="x",
#                     variant="ghost",
#                     on_click=lambda: [
#                         BossState.set_personal_search(""),
#                         BossState.set_personal_filter_tipo(""),
#                         BossState.set_personal_filter_estado(""),
#                         BossState.apply_personal_filters()
#                     ]
#                 ),
#                 spacing="3",
#                 align="center"
#             ),
            
#             spacing="4",
#             width="100%"
#         ),
#         padding="20px 24px",
#         background="white",
#         border_radius="12px",
#         border=f"1px solid {COLORS['gray']['200']}",
#         margin_bottom="24px"
#     )

# ==========================================
# ESTADÍSTICAS DE PERSONAL
# ==========================================

def personal_stats() -> rx.Component:
    """Estadísticas del personal"""
    return rx.grid(
        stat_card(
            title="Total Personal",
            value=str(AppState.get_total_personal()),
            icon="users",
            color=COLORS["primary"]["500"],
            trend="Miembros del equipo"
        ),
        stat_card(
            title="Activos",
            value=AppState.personal_activos.to_string(),
            icon="user-check",
            color=COLORS["success"],
            trend="Personal activo"
        ),
        stat_card(
            title="Odontólogos",
            value=AppState.total_odontologos.to_string(),
            icon="graduation-cap",
            color=COLORS["secondary"]["500"],
            trend="Profesionales"
        ),
        stat_card(
            title="Otros Roles",
            value=AppState.otros_roles.to_string(),
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

def personal_page() -> rx.Component:
    """
    📋 PÁGINA DE GESTIÓN DE PERSONAL
    
    ✅ Usa AppState
    ✅ Componentes genéricos simplificados
    ✅ Filtros y búsqueda
    ✅ Fácil de entender y modificar
    """
    return rx.box(
        # Header principal
        page_header(
            title="Gestión de Personal",
            subtitle="Administrar empleados y sus roles en el sistema"
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
            
            # Estadísticas
            personal_stats(),
            
            # Tabla de personal
            SimpleTableAdapter.personal_table(),
            
            
            padding="6"
        ),
        
        # Modales
        personal_form_modal(),
        delete_personal_confirmation_modal(),
        
        width="100%",
        min_height="100vh"
    )
