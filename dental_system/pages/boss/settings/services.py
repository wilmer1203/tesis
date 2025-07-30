"""
Página de gestión de servicios para el gerente
Permite CRUD completo de los servicios odontológicos
"""

import reflex as rx
from dental_system.components.role_specific.boss import (
    data_table, 
    primary_button, 
    secondary_button,
    modal_overlay,
    form_field,
    success_alert,
    error_alert,
    loading_spinner,
    main_header,
    stat_card
)
from dental_system.state.boss_state import BossState
from dental_system.styles.themes import COLORS, GRADIENTS

# ==========================================
# MODAL DE SERVICIOS
# ==========================================

def servicio_modal() -> rx.Component:
    """Modal para crear/editar servicios"""
    return modal_overlay(
        BossState.show_servicio_modal,
        rx.box(
            # Header del modal
            rx.hstack(
                rx.text(
                    rx.cond(
                        BossState.selected_servicio.length() > 0,
                        "Editar Servicio",
                        "Nuevo Servicio"
                    ),
                    size="4",
                    weight="bold",
                    color=COLORS["gray"]["800"]
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("x", size=20),
                    background="transparent",
                    border="none",
                    cursor="pointer",
                    on_click=BossState.close_servicio_modal,
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
                    # Información Básica
                    rx.text("Información Básica", size="5", weight="medium", color=COLORS["gray"]["700"]),
                    
                    rx.grid(
                        form_field(
                            "Código",
                            "codigo",
                            BossState.servicio_form["codigo"],
                            BossState.update_servicio_form,
                            required=True,
                            placeholder="CONS001"
                        ),
                        form_field(
                            "Nombre del Servicio",
                            "nombre",
                            BossState.servicio_form["nombre"],
                            BossState.update_servicio_form,
                            required=True,
                            placeholder="Consulta General"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    form_field(
                        "Descripción",
                        "descripcion",
                        BossState.servicio_form["descripcion"],
                        BossState.update_servicio_form,
                        field_type="textarea",
                        placeholder="Descripción detallada del servicio"
                    ),
                    
                    # Categorización
                    rx.divider(margin="20px 0"),
                    rx.text("Categorización", size="5", weight="medium", color=COLORS["gray"]["700"]),
                    
                    rx.grid(
                        form_field(
                            "Categoría",
                            "categoria",
                            BossState.servicio_form["categoria"],
                            BossState.update_servicio_form,
                            field_type="select",
                            options=[
                                "Consulta", 
                                "Preventiva", 
                                "Restaurativa", 
                                "Endodoncia", 
                                "Cirugía", 
                                "Prótesis", 
                                "Implantología", 
                                "Estética", 
                                "Ortodoncia", 
                                "Diagnóstico"
                            ],
                            required=True
                        ),
                        form_field(
                            "Subcategoría",
                            "subcategoria",
                            BossState.servicio_form["subcategoria"],
                            BossState.update_servicio_form,
                            placeholder="Subcategoría específica"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    # Tiempo y Pricing
                    rx.divider(margin="20px 0"),
                    rx.text("Tiempo y Precios", size="5", weight="medium", color=COLORS["gray"]["700"]),
                    
                    rx.grid(
                        form_field(
                            "Duración Estimada (min)",
                            "duracion_estimada",
                            BossState.servicio_form["duracion_estimada"],
                            BossState.update_servicio_form,
                            field_type="number",
                            placeholder="30"
                        ),
                        form_field(
                            "Precio Base",
                            "precio_base",
                            BossState.servicio_form["precio_base"],
                            BossState.update_servicio_form,
                            field_type="number",
                            required=True,
                            placeholder="50000"
                        ),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    
                    rx.grid(
                        form_field(
                            "Precio Mínimo",
                            "precio_minimo",
                            BossState.servicio_form["precio_minimo"],
                            BossState.update_servicio_form,
                            field_type="number",
                            placeholder="40000"
                        ),
                        form_field(
                            "Precio Máximo",
                            "precio_maximo",
                            BossState.servicio_form["precio_maximo"],
                            BossState.update_servicio_form,
                            field_type="number",
                            placeholder="60000"
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
                        on_click=BossState.close_servicio_modal
                    ),
                    primary_button(
                        rx.cond(
                            BossState.selected_servicio.length() > 0,
                            "Actualizar",
                            "Crear"
                        ),
                        icon="save",
                        on_click=BossState.save_servicio,
                        loading=BossState.is_loading
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    margin_top="24px"
                ),
                
                on_submit=BossState.save_servicio,
                reset_on_submit=False
            ),
            
            background="white",
            padding="32px",
            border_radius="16px",
            box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1)",
            width="100%",
            max_width="700px"
        )
    )

# ==========================================
# TABLA DE SERVICIOS
# ==========================================

def format_currency(amount) -> str:
    """Formatear cantidad como moneda"""
    try:
        return f"${float(amount):,.0f}"
    except:
        return f"${amount}"

def servicio_actions(servicio: dict) -> list:
    """Acciones para cada fila de servicio"""
    return [
        rx.button(
            rx.icon("edit", size=16),
            size="3",
            variant="ghost",
            color=COLORS["primary"]["500"],
            on_click=lambda: BossState.open_servicio_modal(servicio),
            title="Editar"
        ),
        rx.button(
            rx.icon("eye", size=16),
            size="3",
            variant="ghost",
            color=COLORS["secondary"]["500"],
            title="Ver Detalles"
        ),
        rx.button(
            rx.icon("trash-2", size=16),
            size="3",
            variant="ghost",
            color=COLORS["error"],
            title="Eliminar"
        )
    ]

def format_servicios_for_table(servicios_data):
    """Formatear datos de servicios para mostrar en tabla"""
    if not servicios_data:
        return []
    
    formatted_data = []
    for servicio in servicios_data:
        formatted_data.append({
            "código": servicio.get("codigo", "N/A"),
            "nombre": servicio.get("nombre", "N/A"),
            "categoría": servicio.get("categoria", "N/A"),
            "precio_base": format_currency(servicio.get("precio_base", 0)),
            "duración": servicio.get("duracion_estimada", "N/A"),
            "estado": "Activo" if servicio.get("activo", True) else "Inactivo",
            # Mantener datos originales para edición
            "_original": servicio
        })
    
    return formatted_data

def servicios_table() -> rx.Component:
    """Tabla de servicios con datos y acciones"""
    formatted_data = format_servicios_for_table(BossState.servicios_list)
    
    return data_table(
        formatted_data,
        ["Código", "Nombre", "Categoría", "Precio Base", "Duración", "Estado"],
        "Catálogo de Servicios",
        lambda item: servicio_actions(item.get("_original", {}))
    )

# ==========================================
# FILTROS Y BÚSQUEDA
# ==========================================

def servicios_filters() -> rx.Component:
    """Filtros y búsqueda para servicios"""
    return rx.box(
        rx.hstack(
            # Búsqueda
            rx.hstack(
                rx.icon("search", size=20, color=COLORS["gray"]["600"]),
                rx.input(
                    placeholder="Buscar servicios...",
                    width="300px",
                    border=f"1px solid {COLORS['gray']['300']}",
                    border_radius="8px",
                    _focus={"border_color": COLORS["primary"]["500"]}
                ),
                spacing="2",
                align="center"
            ),
            
            # Filtros
            rx.select.root(
                rx.select.trigger(
                    rx.select.value(placeholder="Categoría"),
                    width="200px"
                ),
                rx.select.content(
                    rx.select.item("Todas", value="all"),
                    rx.select.item("Consulta", value="consulta"),
                    rx.select.item("Preventiva", value="preventiva"),
                    rx.select.item("Restaurativa", value="restaurativa"),
                    rx.select.item("Endodoncia", value="endodoncia"),
                    rx.select.item("Cirugía", value="cirugia"),
                    rx.select.item("Prótesis", value="protesis"),
                    rx.select.item("Estética", value="estetica"),
                    rx.select.item("Ortodoncia", value="ortodoncia")
                )
            ),
            
            rx.select.root(
                rx.select.trigger(
                    rx.select.value(placeholder="Rango de Precio"),
                    width="180px"
                ),
                rx.select.content(
                    rx.select.item("Todos", value="all"),
                    rx.select.item("< $50.000", value="low"),
                    rx.select.item("$50.000 - $150.000", value="medium"),
                    rx.select.item("$150.000 - $500.000", value="high"),
                    rx.select.item("> $500.000", value="premium")
                )
            ),
            
            rx.spacer(),
            
            # Botones de acción
            rx.hstack(
                secondary_button(
                    "Exportar",
                    icon="download",
                    variant="outline"
                ),
                primary_button(
                    "Nuevo Servicio",
                    icon="plus",
                    on_click=lambda: BossState.open_servicio_modal()
                ),
                spacing="3"
            ),
            
            align="center",
            width="100%"
        ),
        padding="20px 24px",
        background="white",
        border_radius="12px",
        border=f"1px solid {COLORS['gray']['200']}",
        margin_bottom="24px"
    )

# ==========================================
# ESTADÍSTICAS DE SERVICIOS
# ==========================================

def servicios_stats() -> rx.Component:
    """Estadísticas de servicios"""
    total_servicios = len(BossState.servicios_list)
    servicios_activos = len([s for s in BossState.servicios_list if s.get("activo", True)])
    
    # Calcular precio promedio
    precios = [s.get("precio_base", 0) for s in BossState.servicios_list if s.get("precio_base")]
    precio_promedio = sum(precios) / len(precios) if precios else 0
    
    return rx.grid(
        stat_card(
            title="Total Servicios",
            value=str(total_servicios),
            icon="package",
            color=COLORS["primary"]["500"]
        ),
        stat_card(
            title="Servicios Activos",
            value=str(servicios_activos),
            icon="check-circle",
            color=COLORS["success"]
        ),
        stat_card(
            title="Precio Promedio",
            value=format_currency(precio_promedio),
            icon="dollar-sign",
            color=COLORS["secondary"]["500"]
        ),
        stat_card(
            title="Más Solicitado",
            value="Consulta General",
            icon="trending-up",
            color="#9C27B0"
        ),
        columns="4",
        spacing="6",
        width="100%",
        margin_bottom="24px"
    )

# ==========================================
# CATEGORÍAS DE SERVICIOS
# ==========================================

def servicios_by_category() -> rx.Component:
    """Distribución de servicios por categoría"""
    # Contar servicios por categoría
    categories_count = {}
    for servicio in BossState.servicios_list:
        categoria = servicio.get("categoria", "Sin categoría")
        categories_count[categoria] = categories_count.get(categoria, 0) + 1
    
    categories = [
        {"name": "Consulta", "count": categories_count.get("Consulta", 0), "color": COLORS["primary"]["500"]},
        {"name": "Preventiva", "count": categories_count.get("Preventiva", 0), "color": COLORS["success"]},
        {"name": "Restaurativa", "count": categories_count.get("Restaurativa", 0), "color": COLORS["secondary"]["500"]},
        {"name": "Endodoncia", "count": categories_count.get("Endodoncia", 0), "color": COLORS["error"]},
        {"name": "Cirugía", "count": categories_count.get("Cirugía", 0), "color": "#9C27B0"},
        {"name": "Prótesis", "count": categories_count.get("Prótesis", 0), "color": "#FF9800"}
    ]
    
    return rx.box(
        rx.vstack(
            rx.text("Servicios por Categoría", size="6", weight="bold", color=COLORS["gray"]["800"]),
            
            rx.vstack(
                *[
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            background=cat["color"],
                            border_radius="50%"
                        ),
                        rx.text(cat["name"], size="3", weight="medium"),
                        rx.spacer(),
                        rx.badge(
                            str(cat["count"]),
                            color_scheme="gray",
                            variant="soft"
                        ),
                        align="center",
                        width="100%"
                    )
                    for cat in categories if cat["count"] > 0
                ],
                spacing="3",
                width="100%"
            ),
            
            spacing="6",
            align_items="stretch",
            width="100%"
        ),
        padding="24px",
        background="white",
        border_radius="16px",
        border=f"1px solid {COLORS['gray']['200']}",
        box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
        width="100%"
    )

# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

def services_management_page() -> rx.Component:
    """Página de gestión de servicios"""
    return rx.box(
        # Header
        main_header(
            "Gestión de Servicios",
            "Administrar el catálogo de servicios odontológicos"
        ),
        
        # Contenido
        rx.cond(
            BossState.is_loading,
            loading_spinner(),
            rx.box(
                # Estadísticas
                servicios_stats(),
                
                # Grid con tabla y categorías
                rx.grid(
                    # Columna principal - Tabla
                    rx.vstack(
                        servicios_filters(),
                        servicios_table(),
                        spacing="0",
                        width="100%"
                    ),
                    
                    # Columna lateral - Categorías
                    servicios_by_category(),
                    
                    columns="3fr 1fr",
                    spacing="6",
                    width="100%"
                ),
                
                spacing="0",
                padding="24px"
            )
        ),
        
        # Modal de servicios
        servicio_modal(),
        
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["50"]
    )

def services_management() -> rx.Component:
    """Gestión de servicios con carga inicial"""
    return services_management_page()
