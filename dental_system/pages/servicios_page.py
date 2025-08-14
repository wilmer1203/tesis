# 📄 PÁGINA DE SERVICIOS - SIGUIENDO PATRÓN DE PACIENTES
# dental_system/pages/servicios_page.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, primary_button, secondary_button
from dental_system.components.table_components import services_table


def service_form_modal() -> rx.Component:
    """📝 Modal para crear/editar servicio"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AppState.selected_servicio,
                    "Editar Servicio",
                    "Nuevo Servicio"
                )
            ),
            
            # Formulario
            rx.vstack(
                # Código y Nombre
                rx.hstack(
                    rx.vstack(
                        rx.text("Código *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.servicio_form["codigo"],
                            on_change=lambda v: AppState.update_servicio_form("codigo", v),
                            placeholder="CON001"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Nombre del Servicio *", size="2", weight="medium"),
                        rx.input(
                            value=AppState.servicio_form["nombre"],
                            on_change=lambda v: AppState.update_servicio_form("nombre", v),
                            placeholder="Consulta General"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Categoría y Precio
                rx.hstack(
                    rx.vstack(
                        rx.text("Categoría *", size="2", weight="medium"),
                        rx.select(
                            [
                                "Consulta", 
                                "Preventiva", 
                                "Restaurativa", 
                                "Endodoncia", 
                                "Periodoncia",
                                "Cirugía",
                                "Ortodoncia",
                                "Prostodoncia",
                                "Estética"
                            ],
                            value=AppState.servicio_form["categoria"],
                            on_change=lambda v: AppState.update_servicio_form("categoria", v),
                            placeholder="Seleccionar categoría"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Precio Base *", size="2", weight="medium"),
                        rx.input(
                            type="number",
                            value=AppState.servicio_form["precio_base"],
                            on_change=lambda v: AppState.update_servicio_form("precio_base", v),
                            placeholder="50000"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                
                # Descripción
                rx.vstack(
                    rx.text("Descripción", size="2", weight="medium"),
                    rx.text_area(
                        value=AppState.servicio_form["descripcion"],
                        on_change=lambda v: AppState.update_servicio_form("descripcion", v),
                        placeholder="Descripción del servicio...",
                        height="100px"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                # Información adicional (opcional)
                rx.vstack(
                    rx.text("Información Adicional", size="3", weight="medium", color="gray.700"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Subcategoría", size="2", weight="medium"),
                            rx.input(
                                value=AppState.servicio_form["subcategoria"],
                                on_change=lambda v: AppState.update_servicio_form("subcategoria", v),
                                placeholder="Subcategoría específica"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Duración Estimada", size="2", weight="medium"),
                            rx.input(
                                value=AppState.servicio_form["duracion_estimada"],
                                on_change=lambda v: AppState.update_servicio_form("duracion_estimada", v),
                                placeholder="30 minutes"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Precio Mínimo", size="2", weight="medium"),
                            rx.input(
                                type="number",
                                value=AppState.servicio_form["precio_minimo"],
                                on_change=lambda v: AppState.update_servicio_form("precio_minimo", v),
                                placeholder="40000"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Precio Máximo", size="2", weight="medium"),
                            rx.input(
                                type="number",
                                value=AppState.servicio_form["precio_maximo"],
                                on_change=lambda v: AppState.update_servicio_form("precio_maximo", v),
                                placeholder="80000"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    spacing="2"
                ),
                
                # Opciones adicionales
                rx.vstack(
                    rx.text("Configuraciones", size="3", weight="medium", color="gray.700"),
                    rx.hstack(
                        rx.checkbox(
                            # checked=AppState.servicio_form["requiere_cita_previa"],
                            checked= rx.cond(AppState.servicio_form["requiere_cita_previa"].split() == "true",
                                             True,
                                             False),
                            on_change=lambda v: AppState.update_servicio_form("requiere_cita_previa", str(v).lower()),
                            color_scheme="teal"
                        ),
                        rx.text("Requiere cita previa", size="2"),
                        spacing="2",
                        align_items="center"
                    ),
                    rx.hstack(
                        rx.checkbox(
                            # checked=AppState.servicio_form["requiere_autorizacion"],
                            checked= rx.cond(AppState.servicio_form["requiere_autorizacion"].split() == "true",
                                             True,
                                             False),
                            on_change=lambda v: AppState.update_servicio_form("requiere_autorizacion", str(v).lower()),
                            color_scheme="teal"
                        ),
                        rx.text("Requiere autorización", size="2"),
                        spacing="2",
                        align_items="center"
                    ),
                    spacing="2"
                ),
                
                # Material incluido
                rx.vstack(
                    rx.text("Material Incluido", size="2", weight="medium"),
                    rx.text_area(
                        value=AppState.servicio_form["material_incluido"],
                        on_change=lambda v: AppState.update_servicio_form("material_incluido", v),
                        placeholder="Materiales incluidos en el servicio (separados por comas)",
                        height="60px"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                # Instrucciones
                rx.hstack(
                    rx.vstack(
                        rx.text("Instrucciones Pre", size="2", weight="medium"),
                        rx.text_area(
                            value=AppState.servicio_form["instrucciones_pre"],
                            on_change=lambda v: AppState.update_servicio_form("instrucciones_pre", v),
                            placeholder="Instrucciones antes del procedimiento",
                            height="80px"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Instrucciones Post", size="2", weight="medium"),
                        rx.text_area(
                            value=AppState.servicio_form["instrucciones_post"],
                            on_change=lambda v: AppState.update_servicio_form("instrucciones_post", v),
                            placeholder="Instrucciones después del procedimiento",
                            height="80px"
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
            
            # Error message
            rx.cond(
                AppState.error_message != "",
                rx.callout(
                    AppState.error_message,
                    icon="triangle-alert",
                    color_scheme="red",
                    variant="surface",
                    margin_bottom="16px"
                )
            ),
            
            # Botones de acción
            rx.hstack(
                rx.dialog.close(
                    secondary_button("Cancelar"),
                ),
                primary_button(
                    text=rx.cond(
                        AppState.selected_servicio,
                        "Actualizar",
                        "Crear Servicio"
                    ),
                    icon="check",
                    on_click=AppState.save_servicio,
                    loading=AppState.is_loading_servicios
                ),
                spacing="2",
                justify="end"
            ),
            
            max_width="800px",
            padding="6"
        ),
        open=AppState.show_servicio_modal,
        on_open_change=AppState.toggle_servicio_modal
    )


def services_controls() -> rx.Component:
    """🎛️ Controles de la página de servicios"""
    return rx.hstack(
        # Búsqueda
        rx.input(
            placeholder="🔍 Buscar por código, nombre o descripción...",
            value=AppState.servicios_search,
            on_change=AppState.set_servicios_search,
            on_key_down=AppState.handle_servicios_search_keydown,
            size="3",
            width="400px"
        ),
        
        # Filtro por categoría
        rx.select(
            ["todas", "Consulta", "Preventiva", "Restaurativa", "Endodoncia", "Periodoncia", "Cirugía", "Ortodoncia", "Prostodoncia", "Estética"],
            placeholder="Todas las categorías",
            value=AppState.servicios_categoria_filter,
            on_change=AppState.set_servicios_categoria_filter,
            size="3"
        ),
        
        # Toggle activos/todos
        rx.switch(
            checked=AppState.servicios_show_only_active,
            on_change=AppState.set_servicios_show_only_active,
            color_scheme="teal"
        ),
        rx.text("Solo activos", size="2", color="gray.700"),
        
        rx.spacer(),
        
        # Botón nuevo servicio
        primary_button(
            text="Nuevo Servicio",
            icon="plus",
            on_click=AppState.open_new_servicio_modal,
            loading=AppState.is_loading_servicios
        ),
        
        spacing="3",
        align="center",
        width="100%",
        padding_bottom="4"
    )


def servicios_page() -> rx.Component:
    """
    📄 Página principal de gestión de servicios
    Accesible por: Jefe (CRUD completo), otros según permisos
    """
    return rx.vstack(
        page_header("🦷 Gestión de Servicios", "Administrar servicios odontológicos"),
        
        # Controles
        services_controls(),
        
        # Tabla de servicios
        services_table(),
        
        # Modal de formulario
        service_form_modal(),
        
        spacing="6",
        padding="6",
        width="100%",
        min_height="100vh"
    )