# 🎨 COMPONENTES UNIVERSALES - ELIMINAN DUPLICACIÓN
# dental_system/components/ui/universal.py

import reflex as rx
from typing import List, Dict, Any, Callable, Optional, Union
from dental_system.styles.themes import COLORS
from dental_system.components.common import paciente_table_row
# ==========================================
# 🔧 FORMULARIO UNIVERSAL - UN COMPONENTE HACE TODO
# ==========================================

def universal_form(
    title: str,
    fields: List[Dict[str, Any]],
    form_data: Dict[str, str],
    on_save: Callable,
    on_cancel: Callable,
    loading: bool = False,
    save_text: str = "Guardar"
) -> rx.Component:
    """
    🎯 FORMULARIO UNIVERSAL QUE REEMPLAZA TODOS LOS MODALES
    
    Tienes UN solo componente que hace todo.
    
    Args:
        title: "Nuevo Paciente", "Nueva Consulta", etc.
        fields: Lista de campos [{"name": "primer_nombre", "label": "Primer Nombre", "type": "text"}]
        form_data: Datos actuales del formulario
        on_save: Función a ejecutar al guardar
        on_cancel: Función a ejecutar al cancelar
        loading: Si está guardando
        save_text: Texto del botón (Guardar, Actualizar, etc.)
    """
    return rx.box(
        # Header del modal
        rx.hstack(
            rx.text(
                title,
                size="6",
                weight="bold",
                color=COLORS["gray"]["800"]
            ),
            rx.spacer(),
            rx.button(
                rx.icon("x", size=20),
                variant="ghost",
                size="2",
                on_click=on_cancel,
                color_scheme="gray"
            ),
            width="100%",
            align="center",
            padding_bottom="4"
        ),
        
        # Campos del formulario
        rx.vstack(
            *[_create_form_field(field, form_data) for field in fields],
            spacing="4",
            width="100%"
        ),
        
        # Botones
        rx.hstack(
            rx.button(
                "Cancelar",
                variant="outline",
                size="3",
                on_click=on_cancel,
                color_scheme="gray"
            ),
            rx.button(
                rx.cond(
                    loading,
                    rx.hstack(
                        rx.spinner(size="3"),
                        rx.text(save_text),
                        spacing="2",
                        align="center"
                    ),
                    rx.text(save_text)
                ),
                size="3",
                on_click=on_save,
                disabled=loading,
                color_scheme="teal"
            ),
            spacing="3",
            justify="end",
            width="100%",
            padding_top="6"
        ),
        
        # Estilo del modal
        background="white",
        border_radius="12px",
        box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        padding="6",
        width="100%",
        max_width="500px"
    )


def _create_form_field(field_config: Dict[str, Any], form_data: Dict[str, str]) -> rx.Component:
    """🔧 Crear campo individual basado en configuración"""
    name = field_config["name"]
    label = field_config["label"]
    field_type = field_config.get("type", "text")
    required = field_config.get("required", False)
    options = field_config.get("options", [])
    placeholder = field_config.get("placeholder", f"Ingrese {label.lower()}")
    
    # Label con asterisco si es requerido
    label_component = rx.text(
        f"{label}{'*' if required else ''}",
        size="3",
        weight="medium",
        color=COLORS["gray"]["700"]
    )
    
    # Input según el tipo
    if field_type == "select":
        # Si las opciones son un Var de Reflex, usa rx.foreach
        if hasattr(options, "_var_name") or isinstance(options, rx.Var):
            input_component = rx.select.root(
                rx.select.trigger(placeholder=f"Seleccionar {label.lower()}"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            options,
                            lambda p: rx.select.item(
                                f"{p['primer_nombre']} {p['primer_apellido']} - {p['numero_documento']}",
                                value=p['id'] 
                            )
                        )
                    )
                ),
                size="3",
                value=form_data.get(name, ""),
                name=name
            )
        else:
            # Si es una lista Python normal, como para selects estáticos
            input_component = rx.select(
                options,
                placeholder=f"Seleccionar {label.lower()}",
                size="3",
                value=form_data.get(name, ""),
                name=name
            )
    elif field_type == "textarea":
        input_component = rx.text_area(
            placeholder=placeholder,
            size="3",
            resize="vertical",
            height="80px",
            value=form_data.get(name, ""),
            name=name
        )
    elif field_type == "date":
        input_component = rx.input(
            type="date",
            size="3",
            value=form_data.get(name, ""),
            name=name
        )
    elif field_type == "datetime-local":
        input_component = rx.input(
            type="datetime-local",
            size="3",
            value=form_data.get(name, ""),
            name=name
        )
    elif field_type == "email":
        input_component = rx.input(
            type="email",
            placeholder=placeholder,
            size="3",
            value=form_data.get(name, ""),
            name=name
        )
    elif field_type == "tel":
        input_component = rx.input(
            type="tel",
            placeholder=placeholder,
            size="3",
            value=form_data.get(name, ""),
            name=name
        )
    else:  # text por defecto
        input_component = rx.input(
            type="text",
            placeholder=placeholder,
            size="3",
            value=form_data.get(name, ""),
            name=name
        )
    
    return rx.vstack(
        label_component,
        input_component,
        spacing="2",
        align_items="start",
        width="100%"
    )

# ==========================================
# 🔧 MODAL UNIVERSAL - REEMPLAZA TODOS LOS MODALES
# ==========================================

def universal_modal(
    is_open: bool,
    content: rx.Component,
    size: str = "md"
) -> rx.Component:
    """
    🎯 MODAL UNIVERSAL - Reemplaza modal_overlay y todos los modales específicos

    Tienes UN modal que maneja todo.
    """
    sizes = {
        "sm": "400px",
        "md": "600px", 
        "lg": "800px",
        "xl": "1000px"
    }
    
    return rx.cond(
        is_open,
        rx.box(
            # Overlay de fondo
            rx.box(
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                background="rgba(0, 0, 0, 0.5)",
                z_index="50",
                backdrop_filter="blur(4px)"
            ),
            
            # Contenido del modal
            rx.center(
                content,
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                z_index="51",
                padding="4"
            ),
            
            # Evitar scroll del body
            overflow="hidden"
        )
    )

# ==========================================
# 🔧 TABLA UNIVERSAL - UNA TABLA PARA TODO
# ==========================================

def universal_table(
    headers: List[str],
    data: List[Dict[str, Any]],
    actions: Optional[List[Dict[str, Any]]] = None,
    empty_message: str = "No hay datos para mostrar"
) -> rx.Component:
    """
    🎯 TABLA UNIVERSAL - Reemplaza todas las tablas específicas
    
    
    Tienes UNA tabla que muestra todo.
    
    Args:
        headers: ["Nombre", "Documento", "Teléfono"] 
        data: Lista de diccionarios con los datos
        actions: [{"icon": "edit", "label": "Editar", "action": edit_func, "color": "blue"}]
        empty_message: Mensaje cuando no hay datos
    """
    return rx.cond(
        data.length() == 0,
        rx.center(
            rx.vstack(
                rx.icon("inbox", size=48, color=COLORS["gray"]["400"]),
                rx.text(
                    empty_message,
                    size="4",
                    color=COLORS["gray"]["500"],
                    text_align="center"
                ),
                spacing="3",
                align="center"
            ),
            height="200px",
            width="100%"
        ),
        rx.table.root(
            print(data),
            # Header
            rx.table.header(
                rx.table.row(
                    *[
                        rx.table.column_header_cell(
                            header,
                            font_weight="600",
                            color=COLORS["gray"]["700"],
                            size="3",
                            align="center"
                        ) for header in headers
                    ],
                    rx.table.column_header_cell(
                        "Acciones",
                        font_weight="600",
                        color=COLORS["gray"]["700"],
                        text_align="center"
                    ) if actions else rx.fragment()
                )
            ),
            # Body
            rx.table.body(
                rx.foreach(
                    data,
                    paciente_table_row
                )
            ),
            variant="surface",
            size="3",
            width="100%"
        )
    )
def _create_table_row(
    row_data: Dict[str, Any], 
    headers: List[str], 
    actions: Optional[List[Dict[str, Any]]]
) -> rx.Component:
    """🔧 Crear fila de tabla"""
    # Crear celdas basadas en los headers
    cells = []
    for header in headers:
        # Convertir header a key (ej: "Primer Nombre" -> "primer_nombre")
        key = header.lower().replace(" ", "_")
        value = row_data.get(key, "")
        
        
        cells.append(
            rx.table.cell(
                str(value),
                color=COLORS["gray"]["800"]
            )
        )
    
    # Agregar celda de acciones si existen
    if actions:
        action_buttons = rx.hstack(
            *[
                rx.button(
                    rx.icon(action["icon"], size=16),
                    size="1",
                    variant="ghost",
                    color_scheme=action.get("color", "gray"),
                    on_click=lambda row=row_data, action=action: action["action"](row["id"]),
                    title=action.get("label", "")
                )
                for action in actions
            ],
            spacing="1",
            justify="center"
        )
        cells.append(rx.table.cell(action_buttons))
    
    return rx.table.row(*cells)

# ==========================================
# 🔧 BOTONES ESTANDARIZADOS 
# ==========================================

def primary_button(
    text: str,
    on_click: Callable,
    icon: Optional[str] = None,
    loading: bool = False,
    disabled: bool = False,
    size: str = '3'
) -> rx.Component:
    """🔵 Botón primario estandarizado"""
    content = []
    
    if icon and not loading:
        content.append(rx.icon(icon, size=16))
    
    if loading:
        content.append(rx.spinner(size="3"))
    
    content.append(rx.text(text))
    
    return rx.button(
        rx.hstack(*content, spacing="2", align="center") if len(content) > 1 else content[0],
        size=size,
        color_scheme="teal",
        on_click=on_click,
        disabled=disabled or loading
    )

def secondary_button(
    text: str,
    on_click: Callable,
    icon: Optional[str] = None,
    loading: bool = False,
    disabled: bool = False,
    size: str = "3"
) -> rx.Component:
    """⚪ Botón secundario estandarizado"""
    content = []
    
    if icon and not loading:
        content.append(rx.icon(icon, size=16))
    
    if loading:
        content.append(rx.spinner(size="3"))
    
    content.append(rx.text(text))
    
    return rx.button(
        rx.hstack(*content, spacing="2", align="center") if len(content) > 1 else content[0],
        size=size,
        variant="outline",
        color_scheme="gray",
        on_click=on_click,
        disabled=disabled or loading
    )

def danger_button(
    text: str,
    on_click: Callable,
    icon: Optional[str] = "trash",
    loading: bool = False,
    disabled: bool = False,
    size: str = "3"
) -> rx.Component:
    """🔴 Botón de peligro estandarizado"""
    content = []
    
    if icon and not loading:
        content.append(rx.icon(icon, size=16))
    
    if loading:
        content.append(rx.spinner(size="3"))
    
    content.append(rx.text(text))
    
    return rx.button(
        rx.hstack(*content, spacing="2", align="center") if len(content) > 1 else content[0],
        size=size,
        color_scheme="red",
        variant="outline",
        on_click=on_click,
        disabled=disabled or loading
    )

# ==========================================
# 🔧 COMPONENTE DE BÚSQUEDA UNIVERSAL
# ==========================================

def universal_search(
    placeholder: str,
    value: str,
    on_change: Callable,
    filters: Optional[List[Dict[str, Any]]] = None
) -> rx.Component:
    """
    🔍 Barra de búsqueda universal con filtros opcionales
    
    Args:
        placeholder: "Buscar pacientes...", "Buscar consultas..."
        value: Valor actual de búsqueda
        on_change: Función cuando cambia el texto
        filters: [{"label": "Estado", "value": filter_var, "options": ["Todos", "Activos"]}]
    """
    components = [
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            size="3",
            width="300px"
        )
    ]
    
    # Agregar filtros si existen
    if filters:
        for filter_config in filters:
            components.append(
                rx.select(
                    filter_config["options"],
                    placeholder=filter_config["label"],
                    value=filter_config["value"],
                    on_change=filter_config["on_change"],
                    size="3"
                )
            )
    
    return rx.hstack(
        *components,
        spacing="3",
        align="center"
    )

# ==========================================
# 🔧 HEADER DE PÁGINA UNIVERSAL
# ==========================================

def page_header(
    title: str,
    subtitle: Optional[str] = None,
    actions: Optional[List[rx.Component]] = None
) -> rx.Component:
    """
    📄 Header universal para todas las páginas
    
    Reemplaza todos los headers duplicados que tienes
    """
    return rx.hstack(
        rx.vstack(
            rx.text(
                title,
                size="7",
                weight="bold",
                color=COLORS["gray"]["800"]
            ),
            rx.text(
                subtitle,
                size="4",
                color=COLORS["gray"]["600"]
            ) if subtitle else rx.fragment(),
            spacing="1",
            align_items="start"
        ),
        rx.spacer(),
        rx.hstack(
            *actions if actions else [],
            spacing="3",
            align="center"
        ),
        width="100%",
        align="center",
        padding_bottom="6"
    )

# ==========================================
# 🔧 ALERTAS/MENSAJES UNIVERSALES
# ==========================================

def universal_alert(
    message: str,
    type: str = "info",  # success, error, warning, info
    on_close: Optional[Callable] = None
) -> rx.Component:
    """🚨 Alerta universal para todos los mensajes"""
    
    colors_map = {
        "success": {"bg": "green", "icon": "check-circle"},
        "error": {"bg": "red", "icon": "x-circle"},
        "warning": {"bg": "yellow", "icon": "alert-triangle"},
        "info": {"bg": "blue", "icon": "info"}
    }
    
    config = colors_map.get(type, colors_map["info"])
    
    return rx.cond(
        message != "",
        rx.box(
            rx.hstack(
                rx.icon(config["icon"], size=20),
                rx.text(
                    message,
                    size="3",
                    weight="medium"
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("x", size=16),
                    size="1",
                    variant="ghost",
                    on_click=on_close
                ) if on_close else rx.fragment(),
                align="center",
                spacing="3"
            ),
            background=f"var(--{config['bg']}-3)",
            border=f"1px solid var(--{config['bg']}-6)",
            border_radius="8px",
            padding="3",
            margin_bottom="4"
        )
    )

# ==========================================
# 🔧 CONFIGURACIONES DE FORMULARIOS PREDEFINIDAS
# ==========================================

# Configuración para formulario de pacientes
PACIENTE_FORM_CONFIG = {
    "title": "Paciente",
    "fields": [
        {"name": "primer_nombre", "label": "Primer Nombre", "type": "text", "required": True},
        {"name": "segundo_nombre", "label": "Segundo Nombre", "type": "text"},
        {"name": "primer_apellido", "label": "Primer Apellido", "type": "text", "required": True},
        {"name": "segundo_apellido", "label": "Segundo Apellido", "type": "text"},
        {"name": "numero_documento", "label": "Número de Documento", "type": "text", "required": True},
        {"name": "telefono_1", "label": "Teléfono Principal", "type": "tel", "required": True},
        {"name": "telefono_2", "label": "Teléfono Secundario", "type": "tel"},
        {"name": "email", "label": "Email", "type": "email"},
        {"name": "fecha_nacimiento", "label": "Fecha de Nacimiento", "type": "date"},
        {
            "name": "genero", 
            "label": "Género", 
            "type": "select",
            "options": ["Masculino", "Femenino", "Otro"]
        },
        {"name": "direccion", "label": "Dirección", "type": "textarea"}
    ]
}

# Configuración para formulario de consultas
CONSULTA_FORM_CONFIG = {
    "title": "Consulta",
    "fields": [
        {"name": "paciente_id", "label": "Paciente", "type": "select", "required": True},
        {"name": "fecha_programada", "label": "Fecha", "type": "date", "required": True},
        {"name": "hora_programada", "label": "Hora", "type": "time", "required": True},
        {"name": "motivo", "label": "Motivo de la Consulta", "type": "textarea", "required": True},
        {
            "name": "estado",
            "label": "Estado",
            "type": "select", 
            "options": ["programada", "confirmada", "en_progreso", "completada", "cancelada"]
        },
        {"name": "observaciones", "label": "Observaciones", "type": "textarea"}
    ]
}

# Headers para tablas
PACIENTES_TABLE_HEADERS = ["Paciente", "Documento", "Género", "Contacto"]
CONSULTAS_TABLE_HEADERS = ["Paciente Nombre", "Fecha Programada", "Hora Programada", "Motivo", "Estado"]

# Acciones para tablas
# def get_pacientes_table_actions():
#     """🔧 Acciones para tabla de pacientes"""
#     from dental_system.state.app_state import AppState
    
#     return [
#         {"icon": "edit", "label": "Editar", "action": AppState.abrir_modal_paciente, "color": "blue"},
#         {"icon": "trash", "label": "Eliminar", "action": lambda id: print(f"Eliminar {id}"), "color": "red"}
#     ]
    
def get_pacientes_table_actions():
    """🔧 Acciones para tabla de pacientes"""
    from dental_system.state.app_state import AppState
    return [
        {"icon": "edit", "label": "Editar", "action": AppState.abrir_modal_paciente, "color": "blue"},
        {"icon": "trash", "label": "Eliminar", "action": AppState.eliminar_paciente, "color": "red"}
    ]

def get_consultas_table_actions():
    """🔧 Acciones para tabla de consultas"""
    from dental_system.state.app_state import AppState
    
    return [
        {"icon": "edit", "label": "Editar", "action": AppState.abrir_modal_consulta, "color": "blue"},
        # {"icon": "calendar", "label": "Reagendar", "action": lambda id: print(f"Reagendar {id}"), "color": "green"},
        {"icon": "trash", "label": "Cancelar", "action": AppState.cancelar_consulta, "color": "red"}
    ]
    
    
