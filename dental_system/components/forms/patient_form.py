"""
Formulario de pacientes.

Formulario completo para crear y editar información de pacientes.
Incluye validaciones y manejo de errores.
"""

import reflex as rx
from typing import Dict, List, Optional, Any
from datetime import date


def patient_form_fields() -> Dict[str, Any]:
    """
    Configuración de campos del formulario de pacientes.
    
    Returns:
        Dict[str, Any]: Configuración de campos
    """
    return {
        "nombre_completo": {
            "label": "Nombre Completo *",
            "type": "text",
            "placeholder": "Ingrese el nombre completo",
            "required": True,
        },
        "tipo_documento": {
            "label": "Tipo de Documento",
            "type": "select",
            "options": [
                {"value": "CC", "label": "Cédula de Ciudadanía"},
                {"value": "TI", "label": "Tarjeta de Identidad"},
                {"value": "CE", "label": "Cédula de Extranjería"},
                {"value": "PA", "label": "Pasaporte"},
            ],
            "default": "CC",
        },
        "numero_documento": {
            "label": "Número de Documento *",
            "type": "text",
            "placeholder": "Número de documento",
            "required": True,
        },
        "fecha_nacimiento": {
            "label": "Fecha de Nacimiento",
            "type": "date",
            "required": False,
        },
        "genero": {
            "label": "Género",
            "type": "select",
            "options": [
                {"value": "masculino", "label": "Masculino"},
                {"value": "femenino", "label": "Femenino"},
                {"value": "otro", "label": "Otro"},
            ],
        },
        "telefono": {
            "label": "Teléfono",
            "type": "tel",
            "placeholder": "Número de teléfono",
        },
        "celular": {
            "label": "Celular",
            "type": "tel", 
            "placeholder": "Número de celular",
        },
        "email": {
            "label": "Correo Electrónico",
            "type": "email",
            "placeholder": "correo@ejemplo.com",
        },
        "direccion": {
            "label": "Dirección",
            "type": "textarea",
            "placeholder": "Dirección completa",
        },
        "ciudad": {
            "label": "Ciudad",
            "type": "text",
            "placeholder": "Ciudad de residencia",
        },
        "ocupacion": {
            "label": "Ocupación",
            "type": "text",
            "placeholder": "Ocupación o profesión",
        },
        "estado_civil": {
            "label": "Estado Civil",
            "type": "select",
            "options": [
                {"value": "soltero", "label": "Soltero(a)"},
                {"value": "casado", "label": "Casado(a)"},
                {"value": "divorciado", "label": "Divorciado(a)"},
                {"value": "viudo", "label": "Viudo(a)"},
                {"value": "union_libre", "label": "Unión Libre"},
            ],
        },
    }


def form_field(
    field_name: str,
    field_config: Dict[str, Any],
    value: Any = None,
    on_change = None,
    error: Optional[str] = None
) -> rx.Component:
    """
    Renderiza un campo individual del formulario.
    
    Args:
        field_name: Nombre del campo
        field_config: Configuración del campo
        value: Valor actual
        on_change: Función callback para cambios
        error: Mensaje de error
        
    Returns:
        rx.Component: Campo del formulario
    """
    field_type = field_config.get("type", "text")
    label = field_config.get("label", field_name)
    placeholder = field_config.get("placeholder", "")
    required = field_config.get("required", False)
    
    # Label
    label_component = rx.text(
        label,
        size="3",
        font_weight="500",
        color="#374151",
        margin_bottom="1",
    )
    
    # Input component based on type
    if field_type == "select":
        options = field_config.get("options", [])
        input_component = rx.select.root(
            rx.select.trigger(
                placeholder=placeholder or "Seleccione una opción",
                width="100%",
            ),
            rx.select.content(
                *[
                    rx.select.item(
                        option["label"],
                        value=option["value"]
                    )
                    for option in options
                ]
            ),
            value=value,
            on_value_change=on_change,
            width="100%",
        )
    elif field_type == "textarea":
        input_component = rx.text_area(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            width="100%",
            min_height="80px",
        )
    elif field_type == "date":
        input_component = rx.input(
            type="date",
            value=value,
            on_change=on_change,
            width="100%",
        )
    else:
        input_component = rx.input(
            type=field_type,
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            width="100%",
        )
    
    # Error message
    error_component = rx.cond(
        error,
        rx.text(
            error,
            size="2",
            color="#EF4444",
            margin_top="1",
        ),
        rx.fragment(),
    )
    
    return rx.vstack(
        label_component,
        input_component,
        error_component,
        spacing="1",
        width="100%",
        margin_bottom="4",
    )


def patient_form(
    patient_data: Optional[Dict[str, Any]] = None,
    on_submit = None,
    on_cancel = None,
    is_loading: bool = False
) -> rx.Component:
    """
    Formulario completo de pacientes.
    
    Args:
        patient_data: Datos del paciente (para edición)
        on_submit: Función callback para envío
        on_cancel: Función callback para cancelar
        is_loading: Estado de carga
        
    Returns:
        rx.Component: Formulario de pacientes
    """
    fields = patient_form_fields()
    
    return rx.box(
        rx.vstack(
            # Título
            rx.heading(
                "Información del Paciente",
                size="6",
                color="#1CBBBA",
                margin_bottom="6",
            ),
            
            # Campos del formulario en grid
            rx.grid(
                *[
                    form_field(
                        field_name=field_name,
                        field_config=field_config,
                        value=patient_data.get(field_name) if patient_data else None,
                    )
                    for field_name, field_config in fields.items()
                ],
                columns="2",
                spacing="4",
                width="100%",
            ),
            
            # Sección de información médica
            rx.vstack(
                rx.heading(
                    "Información Médica",
                    size="4",
                    color="#374151",
                    margin_bottom="4",
                ),
                
                form_field(
                    "alergias",
                    {
                        "label": "Alergias",
                        "type": "textarea",
                        "placeholder": "Describa las alergias conocidas"
                    }
                ),
                
                form_field(
                    "medicamentos_actuales",
                    {
                        "label": "Medicamentos Actuales",
                        "type": "textarea", 
                        "placeholder": "Liste los medicamentos que toma actualmente"
                    }
                ),
                
                form_field(
                    "condiciones_medicas",
                    {
                        "label": "Condiciones Médicas",
                        "type": "textarea",
                        "placeholder": "Condiciones médicas relevantes"
                    }
                ),
                
                spacing="4",
                width="100%",
                margin_top="6",
            ),
            
            # Botones de acción
            rx.hstack(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    on_click=on_cancel,
                    disabled=is_loading,
                ),
                rx.button(
                    rx.cond(
                        is_loading,
                        rx.hstack(
                            rx.icon("loader-2", class_name="animate-spin"),
                            rx.text("Guardando..."),
                            spacing="2",
                        ),
                        rx.text("Guardar Paciente"),
                    ),
                    on_click=on_submit,
                    disabled=is_loading,
                    background_color="#1CBBBA",
                    _hover={"background_color": "#16A5A4"},
                ),
                justify="end",
                spacing="3",
                width="100%",
                margin_top="6",
            ),
            
            spacing="4",
            width="100%",
        ),
        padding="6",
        background_color="white",
        border_radius="12px",
        border="1px solid #E5E7EB",
        max_width="800px",
    )