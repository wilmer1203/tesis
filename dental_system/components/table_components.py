"""
🎯 ADAPTADOR SIMPLE PARA TUS COMPONENTES GENÉRICOS - CORREGIDO
Sin foreach problemático - Filtros estáticos y funcionales
"""

import reflex as rx
from typing import Dict, List, Callable, Any
from dental_system.state.app_state import AppState

# ==========================================
# 🔧 ADAPTADOR SIMPLE PARA TABLAS - CORREGIDO
# ==========================================

class SimpleTableAdapter:
    """Adaptador que conecta tus componentes genéricos con AppState"""
    
    @staticmethod
    def patients_table() -> rx.Component:
        """📋 Tabla de pacientes usando componentes genéricos - CORREGIDO"""
        return rx.box(
            # Header con filtros - SIN FOREACH PROBLEMÁTICO
            patiente_table_header(),
            
            # Tabla principal
            simple_generic_table(
                data=AppState.pacientes_filtrados,  # Usar tu método filtrado
                columns=[
                    {"key": "nombre_completo", "label": "Paciente", "renderer": patient_name_cell},
                    {"key": "numero_documento", "label": "Documento", "renderer": document_cell},
                    {"key": "telefono_1", "label": "Teléfono", "renderer": phone_cell},
                    {"key": "activo", "label": "Estado", "renderer": status_cell},
                    {"key": "actions", "label": "Acciones", "renderer": patient_actions_cell}
                ],
                # loading=AppState.loading,
                empty_message="No hay pacientes registrados"
            ),
            
            class_name="space-y-4"
        )
    
    @staticmethod
    def consultas_table() -> rx.Component:
        """📅 Tabla de consultas con filtros avanzados"""
        return rx.box(
            # Header con filtros avanzados
            consultas_table_header(),
            
            # Tabla principal
            consultas_generic_table(
                data=AppState.consultas_filtradas,
                loading=AppState.is_loading_consultas,
                empty_message="No hay consultas registradas"
            ),
            
            class_name="space-y-4"
        )

    @staticmethod
    def personal_table() -> rx.Component:
        """📋 Tabla de personal usando adaptador genérico"""
        return rx.box(
            # Header con filtros
            personal_table_header(),
            
            # Tabla principal usando componente genérico
            personal_generic_table(
                data=AppState.personal_filtrados,
                loading=AppState.is_loading_personal,
                empty_message="No hay personal registrado"
            ),
            
            class_name="space-y-4"
        )

# ==========================================
# 🎨 HEADERS ESPECÍFICOS POR TABLA - SIN FOREACH
# ==========================================

def patiente_table_header() -> rx.Component:
    """Header específico para tabla de pacientes - SIN FOREACH"""
    return rx.box(
        rx.hstack(
            # Título
            rx.text("Pacientes", size="6", weight="bold", color="gray.800"),
            rx.spacer(),
            
            # Botón crear
            rx.button(
                rx.icon("plus", size=16),
                "Nuevo Paciente",
                on_click=AppState.abrir_modal_paciente,
                color_scheme="teal",
                size="3"
            ),
            
            align="center",
            width="100%"
        ),
        
        # Barra de búsqueda y filtros - ESTÁTICOS  
        rx.hstack(
            # Búsqueda
            rx.input(
                placeholder="Buscar pacientes por nombre, documento...",
                value=AppState.pacientes_search,
                on_change=AppState.set_pacientes_search,
                size="3",
                width="300px"
            ),
            
            # Filtro de estado - ESTÁTICO
            rx.select(
                ["Todos", "Activos", "Inactivos"],
                placeholder="Estado",
                value=AppState.pacientes_filter_activos,
                on_change=AppState.set_pacientes_filter_activos,
                size="3"
            ),
            
            spacing="3",
            align="center",
            margin_top="4"
        ),
        
        background="white",
        padding="4",
        border_radius="8px",
        border="1px solid var(--gray-6)",
        margin_bottom="4"
    )

# En table_components.py - CORREGIR consultas_table_header()

def consultas_table_header() -> rx.Component:
    """Header TOTALMENTE SIMPLIFICADO - SIN ITERACIONES"""
    return rx.box(
        # Título y botón
        rx.hstack(
            rx.text("Consultas del Día", size="6", weight="bold", color="gray.800"),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=16),
                "Nueva Consulta",
                on_click=AppState.abrir_modal_consulta,
                color_scheme="teal",
                size="3"
            ),
            align="center",
            width="100%"
        ),
        
        # Solo búsqueda por ahora - SIN FILTROS COMPLEJOS
        rx.hstack(
            rx.input(
                placeholder="Buscar consultas...",
                value=AppState.consultas_search,
                on_change=AppState.set_consultas_search,
                size="3",
                width="300px"
            ),
            
            rx.button(
                "Buscar",
                size="3",
                variant="soft",
                on_click=AppState.aplicar_filtros_consultas
            ),
            
            spacing="3",
            align="center",
            margin_top="4"
        ),
        
        background="white",
        padding="4",
        border_radius="8px",
        border="1px solid var(--gray-6)",
        margin_bottom="4"
    )

# def consultas_table_header() -> rx.Component:
#     """Header SIMPLIFICADO para consultas"""
#     return rx.box(
#         # Título y botón
#         rx.hstack(
#             rx.text("Consultas del Día", size="6", weight="bold", color="gray.800"),
#             rx.spacer(),
#             rx.button(
#                 rx.icon("plus", size=16),
#                 "Nueva Consulta",
#                 on_click=AppState.abrir_modal_consulta,
#                 color_scheme="teal",
#                 size="3"
#             ),
#             align="center",
#             width="100%"
#         ),
        
#         # Filtros básicos
#         rx.hstack(
#             # Búsqueda
#             rx.input(
#                 placeholder="Buscar consultas...",
#                 value=AppState.consultas_search,
#                 on_change=AppState.set_consultas_search,
#                 size="3",
#                 width="300px"
#             ),
            
#             # Filtro por estado
#             rx.select(
#                 ["Todos", "Programada", "En Progreso", "Completada", "Cancelada"],
#                 placeholder="Estado",
#                 value=AppState.consultas_filter_estado,
#                 on_change=AppState.set_consultas_filter_estado,
#                 size="3"
#             ),
            
#             # Filtro por odontólogo
#             rx.select(
#                 ["Todos"] + [o.get('nombre_completo', '') for o in AppState.odontologos_list],
#                 placeholder="Odontólogo",
#                 value=AppState.consultas_filter_odontologo,
#                 on_change=AppState.set_consultas_filter_odontologo,
#                 size="3"
#             ),
            
#             spacing="3",
#             align="center",
#             margin_top="4"
#         ),
        
#         background="white",
#         padding="4",
#         border_radius="8px",
#         border="1px solid var(--gray-6)",
#         margin_bottom="4"
#     )

def personal_table_header() -> rx.Component:
    """Header específico para tabla de personal"""
    return rx.box(
        rx.hstack(
            # Título
            rx.text("Personal", size="6", weight="bold", color="gray.800"),
            rx.spacer(),
            
            # Botón crear
            rx.button(
                rx.icon("plus", size=16),
                "Nuevo Personal",
                on_click=AppState.abrir_modal_personal,
                color_scheme="teal",
                size="3"
            ),
            
            align="center",
            width="100%"
        ),
        
        # Barra de búsqueda y filtros
        rx.hstack(
            # Búsqueda
            rx.input(
                placeholder="Buscar por nombre, email o documento...",
                value=AppState.personal_search,
                on_change=AppState.set_personal_search,
                size="3",
                width="300px"
            ),
            
            # Filtro por tipo
            rx.select(
                ["Todos", "Odontólogo", "Administrador", "Asistente", "Gerente"],
                placeholder="Tipo Personal",
                value=AppState.personal_filter_tipo,
                on_change=AppState.set_personal_filter_tipo,
                size="3"
            ),
            
            # Filtro por estado
            rx.select(
                ["Todos", "Activo", "Inactivo", "Vacaciones"],
                placeholder="Estado",
                value=AppState.personal_filter_estado,
                on_change=AppState.set_personal_filter_estado,
                size="3"
            ),
            
            spacing="3",
            align="center",
            margin_top="4"
        ),
        
        background="white",
        padding="4",
        border_radius="8px",
        border="1px solid var(--gray-6)",
        margin_bottom="4"
    )
# ==========================================
# 🎨 TABLA GENÉRICA SIMPLIFICADA - SIN PROBLEMAS
# ==========================================

def simple_generic_table(
    data: List[Dict],
    columns: List[Dict],
    loading: bool = False,
    empty_message: str = "No hay datos"
) -> rx.Component:
    """Tabla genérica simplificada que usa tus renderers - CORREGIDA"""
    
    return rx.box(
        rx.cond(
            loading,
            # Estado de carga
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color="teal"),
                    rx.text("Cargando datos...", size="3", color="gray.600"),
                    spacing="3",
                    align="center"
                ),
                padding="8"
            ),
            
            # Tabla con datos
            rx.cond(
                data.length() > 0,
                
                # Tabla principal  
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            # Headers estáticos - SIN FOREACH
                            rx.table.column_header_cell("Paciente", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Documento", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Teléfono", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Estado", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Acciones", class_name="font-semibold text-gray-700"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            data,
                            lambda row: rx.table.row(
                                # Celdas específicas para pacientes
                                rx.table.cell(patient_name_cell(row), class_name="py-3"),
                                rx.table.cell(document_cell(row), class_name="py-3"),
                                rx.table.cell(phone_cell(row), class_name="py-3"),
                                rx.table.cell(status_cell(row), class_name="py-3"),
                                rx.table.cell(patient_actions_cell(row), class_name="py-3"),
                                class_name="hover:bg-gray-50"
                            )
                        )
                    ),
                    class_name="w-full"
                ),
                
                # Estado vacío
                rx.center(
                    rx.vstack(
                        rx.icon("inbox", size=48, color="gray.400"),
                        rx.text(empty_message, size="4", color="gray.500"),
                        spacing="3",
                        align="center"
                    ),
                    padding="8"
                )
            )
        ),
        
        background="white",
        border_radius="8px",
        border="1px solid var(--gray-6)",
        overflow="hidden"
    )

def consultas_generic_table(
    data: rx.Var,
    loading: bool = False,
    empty_message: str = "No hay consultas"
) -> rx.Component:
    """Tabla específica para consultas con columnas personalizadas"""
    
    return rx.box(
        rx.cond(
            loading,
            # Estado de carga
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color="teal"),
                    rx.text("Cargando consultas...", size="3", color="gray.600"),
                    spacing="3",
                    align="center"
                ),
                padding="8"
            ),
            
            # Tabla con datos
            rx.cond(
                data.length() > 0,
                
                # Tabla principal  
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("#", class_name="font-semibold text-gray-700 w-12"),
                            rx.table.column_header_cell("Paciente", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Odontólogo", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Tipo", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Motivo", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Estado", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Acciones", class_name="font-semibold text-gray-700"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            data,
                            lambda row, index: rx.table.row(
                                rx.table.cell(consulta_orden_cell(row, index), class_name="py-3"),
                                rx.table.cell(consulta_paciente_cell(row), class_name="py-3"),
                                rx.table.cell(consulta_odontologo_cell(row), class_name="py-3"),
                                rx.table.cell(consulta_fecha_cell(row), class_name="py-3"),
                                rx.table.cell(consulta_motivo_cell(row), class_name="py-3"),
                                rx.table.cell(consulta_estado_cell(row), class_name="py-3"),
                                rx.table.cell(consulta_actions_cell(row), class_name="py-3"),
                                class_name="hover:bg-gray-50"
                            )
                        )
                    ),
                    class_name="w-full"
                ),
                
                # Estado vacío
                rx.center(
                    rx.vstack(
                        rx.icon("calendar", size=48, color="gray.400"),
                        rx.text(empty_message, size="4", color="gray.500"),
                        rx.text("¡Crea la primera consulta del día!", size="3", color="gray.400"),
                        spacing="3",
                        align="center"
                    ),
                    padding="8"
                )
            )
        ),
        
        background="white",
        border_radius="8px",
        border="1px solid var(--gray-6)",
        overflow="hidden"
    )

def personal_generic_table(
    data: rx.Var,
    loading: bool = False,
    empty_message: str = "No hay datos"
) -> rx.Component:
    """Tabla genérica específica para personal"""
    
    return rx.box(
        rx.cond(
            loading,
            # Estado de carga
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color="teal"),
                    rx.text("Cargando personal...", size="3", color="gray.600"),
                    spacing="3",
                    align="center"
                ),
                padding="8"
            ),
            
            # Tabla con datos
            rx.cond(
                data.length() > 0,
                
                # Tabla principal  
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Nombre", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Documento", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Tipo", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Especialidad", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Estado", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Teléfono", class_name="font-semibold text-gray-700"),
                            rx.table.column_header_cell("Acciones", class_name="font-semibold text-gray-700"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            data,
                            lambda row: rx.table.row(
                                rx.table.cell(personal_name_cell(row), class_name="py-3"),
                                rx.table.cell(document_cell(row), class_name="py-3"),
                                rx.table.cell(personal_type_cell(row), class_name="py-3"),
                                rx.table.cell(personal_specialty_cell(row), class_name="py-3"),
                                rx.table.cell(personal_status_cell(row), class_name="py-3"),
                                rx.table.cell(personal_phone_cell(row), class_name="py-3"),
                                rx.table.cell(personal_actions_cell(row), class_name="py-3"),
                                class_name="hover:bg-gray-50"
                            )
                        )
                    ),
                    class_name="w-full"
                ),
                
                # Estado vacío
                rx.center(
                    rx.vstack(
                        rx.icon("users", size=48, color="gray.400"),
                        rx.text(empty_message, size="4", color="gray.500"),
                        spacing="3",
                        align="center"
                    ),
                    padding="8"
                )
            )
        ),
        
        background="white",
        border_radius="8px",
        border="1px solid var(--gray-6)",
        overflow="hidden"
    )


# ==========================================
# 🎨 RENDERERS ESPECÍFICOS PARA CADA TABLA 
# ==========================================

def patient_name_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de nombre de paciente"""
    return rx.vstack(
        rx.text(
            f"{row.get('primer_nombre', '')} {row.get('primer_apellido', '')}",
            size="3",
            weight="medium"
        ),
        rx.text(
            f"HC: {row.get('numero_historia', 'Sin asignar')}",
            size="2",
            color="gray.500"
        ),
        spacing="1",
        align_items="start"
    )

def document_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de documento"""
    return rx.text(
        f"{row.get('tipo_documento', 'CC')}-{row.get('numero_documento', '')}",
        size="3"
    )

def phone_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de teléfono"""
    return rx.text(
        row.get('telefono_1', 'Sin teléfono'),
        size="3"
    )

def status_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de estado activo/inactivo"""
    return rx.badge(
        rx.cond(row['activo'], "Activo", "Inactivo"),
        color_scheme=rx.cond(row['activo'], "green", "red"),
        variant="soft"
    )


def patient_actions_cell(row: rx.Var[Dict]) -> rx.Component:
    """Acciones para pacientes"""
    return rx.hstack(
        rx.tooltip(
            rx.button(
                rx.icon("edit", size=16),
                size="2",
                variant="ghost",
                color_scheme="blue",
                on_click=lambda: AppState.abrir_modal_paciente(row['id'])
            ),
            content="Editar paciente"
        ),
        rx.cond(
            row['activo'],
            rx.tooltip(
                rx.button(
                    rx.icon("trash", size=16),
                    size="2",
                    variant="ghost",
                    color_scheme="red",
                    on_click=lambda: AppState.confirmar_eliminar_paciente(row['id'])
                ),
                content="Eliminar paciente"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    size="2",
                    variant="ghost",
                    color_scheme="green",
                    on_click=lambda: AppState.confirmar_reactivar_paciente(row['id'])  # ✅ MÉTODO NUEVO
                ),
                content="Reactivar paciente"
            )
        ),
        spacing="2"
    )

    
def personal_actions_cell(row: rx.Var[dict]) -> rx.Component:
    """Acciones para personal"""
    return rx.hstack(
        rx.tooltip(
            rx.button(
                rx.icon("edit", size=16),
                size="2",
                variant="ghost",
                color_scheme="blue",
                on_click=lambda: AppState.abrir_modal_personal(row['id'])
            ),
            content="Editar personal"
        ),
        rx.cond(
            row.get('estado_laboral') == "activo",
            rx.tooltip(
                rx.button(
                    rx.icon("trash", size=16),
                    size="2",
                    variant="ghost",
                    color_scheme="red",
                    on_click=lambda: AppState.confirmar_eliminar_personal(row['id'])
                ),
                content="Desactivar personal"
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    size="2",
                    variant="ghost",
                    color_scheme="green",
                    on_click=lambda: AppState.confirmar_reactivar_personal(row['id'])
                ),
                content="Reactivar personal"
            )
        ),
        spacing="2"
    )

def personal_name_cell(row: rx.Var[dict]) -> rx.Component:
    """Celda de nombre del personal"""
    return rx.vstack(
        rx.text(
            f"{row.get('primer_nombre', '')} {row.get('primer_apellido', '')}",
            size="3",
            weight="medium"
        ),
        rx.text(
            row.get('email', ''),
            size="2",
            color="gray.500"
        ),
        spacing="1",
        align_items="start"
    )

def personal_type_cell(row: rx.Var[dict]) -> rx.Component:
    """Celda de tipo de personal"""
    return rx.badge(
        row.get('tipo_personal', ''),
        color_scheme=rx.match(
            row.get('tipo_personal', ''),
            ("Odontólogo", "green"),
            ("Administrador", "blue"),
            ("Asistente", "yellow"),
            ("Gerente", "purple"),
            "gray"
        ),
        variant="soft"
    )

def personal_specialty_cell(row: rx.Var[dict]) -> rx.Component:
    """Celda de especialidad"""
    return rx.text(
        rx.cond(
            row.get('especialidad'),
            row.get('especialidad', ''),
            "-"
        ),
        size="3"
    )

def personal_status_cell(row: rx.Var[dict]) -> rx.Component:
    """Celda de estado laboral"""
    return rx.badge(
        rx.cond(row["estado_laboral"],"Activo", "Inactivo"),
        color_scheme=rx.match(
            row.get('estado_laboral', 'activo'),
            ("activo", "green"),
            ("inactivo", "red"),
            ("vacaciones", "yellow"),
            "gray"
        ),
        variant="soft"
    )
    

def personal_phone_cell(row: rx.Var[dict]) -> rx.Component:
    """Celda de teléfono"""
    return rx.text(
        rx.cond(
            row.get('telefono'),
            row.get('telefono', ''),
            row.get('celular', 'Sin teléfono')
        ),
        size="3"
    )
    
def consulta_orden_cell(row: rx.Var[Dict], index: rx.Var[int]) -> rx.Component:
    """Celda de número de orden (#1, #2, #3...)"""
    return rx.box(
        rx.text(
            f"#{index + 1}",
            size="4",
            weight="bold",
            color="teal.600"
        ),
        text_align="center",
        flex="0 0 60px",     
    )

def consulta_paciente_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de paciente - SIMPLE con nombres completos"""
    return rx.vstack(
        rx.text(
            row.paciente_nombre,
            size="3",
            weight="medium"
        ),
        rx.text(
            f"CC: {row.paciente_documento}",
            size="2",
            color="gray.500"
        ),
        spacing="1",
        align_items="start"
    )

def consulta_odontologo_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de odontólogo - SIMPLE"""
    return rx.vstack(
        rx.text(
            row.odontologo_nombre,
            size="3",
            weight="medium"
        ),
        rx.text(
            row.odontologo_especialidad,
            size="2",
            color="gray.500"
        ),
        spacing="1",
        align_items="start"
    )

def consulta_motivo_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de motivo - SIMPLE"""
    return rx.text(
        row.get('motivo_consulta', 'Sin motivo'),
        size="3",
        color="gray.600"
    )

def consulta_fecha_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de fecha y hora"""
    return rx.badge(
            row.tipo_consulta,
            variant="outline",
            color_scheme="gray",
            size="2",
            flex="1"
        )
        
    



def consulta_estado_cell(row: rx.Var[Dict]) -> rx.Component:
    """Celda de estado con badge colorido (sin confirmada)"""
    estado = row.get('estado', 'programada')
    
    return rx.badge(
        rx.match(
            estado,
            ("programada", "Programada"),
            ("en_progreso", "En Progreso"),
            ("completada", "Completada"),
            ("cancelada", "Cancelada"),
            "Programada"  # Default
        ),
        color_scheme=rx.match(
            estado,
            ("programada", "blue"),
            ("en_progreso", "yellow"),
            ("completada", "green"),
            ("cancelada", "red"),
            "gray"  # Default
        ),
        variant="soft",
        size="2"
    )

def consulta_actions_cell(row: rx.Var[Dict]) -> rx.Component:
    """Acciones - SIMPLIFICADAS"""
    return rx.hstack(
        # Botón Editar (siempre visible)
        rx.tooltip(
            rx.button(
                rx.icon("edit", size=16),
                size="2",
                variant="ghost",
                color_scheme="blue",
                on_click=lambda: AppState.abrir_modal_consulta(row['id'])
            ),
            content="Editar consulta"
        ),
        
        # Botón Cancelar
        rx.tooltip(
            rx.button(
                rx.icon("x", size=16),
                size="2",
                variant="ghost",
                color_scheme="red",
                on_click=lambda: AppState.confirmar_cancelar_consulta(row['id'])
            ),
            content="Cancelar consulta"
        ),
        
        # Botón Cambiar Estado
        rx.tooltip(
            rx.button(
                rx.icon("refresh-cw", size=16),
                size="2",
                variant="ghost",
                color_scheme="green",
                on_click=lambda: AppState.cambiar_estado_consulta(row['id'], "completada")
            ),
            content="Cambiar estado"
        ),
        
        spacing="1"
    )