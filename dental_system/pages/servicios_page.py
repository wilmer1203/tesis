"""
🏥 PÁGINA DE SERVICIOS MODERNA - GESTIÓN COMPLETA DE CATÁLOGO
==============================================================

FUNCIONALIDADES:
- ✅ CRUD completo de servicios (solo Gerente)
- ✅ Catálogo con 14 servicios precargados
- ✅ Activar/desactivar servicios
- ✅ Filtros por categoría y estado
- ✅ Búsqueda avanzada
- ✅ Estadísticas en tiempo real
- ✅ Modal moderno para crear/editar
- ✅ Diseño glassmorphism profesional

INTEGRACIÓN:
- Estado: EstadoServicios (integrado en AppState)
- Servicios: 14 servicios precargados con códigos SER001-014
- Permisos: Solo Gerente puede CRUD, otros ven catálogo
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import medical_page_layout, primary_button, secondary_button
from dental_system.components.forms import service_form_modal
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS, GLASS_EFFECTS, ANIMATIONS,
    dark_crystal_card, dark_header_style, create_dark_style, dark_table_container
)

# ==========================================
# 🎨 COMPONENTES MODERNOS PARA SERVICIOS
# ==========================================

def minimal_servicios_stat_card(
    title: str,
    value: str,
    icon: str,
    color: str,
    subtitle: str = ""
) -> rx.Component:
    """🎯 Card de estadística minimalista para servicios (patrón Personal/Pacientes)"""
    return rx.box(
        rx.vstack(
            # Layout superior: Icono a la izquierda, Número a la derecha
            rx.hstack(
                # Icono pequeño a la izquierda
                rx.box(
                    rx.icon(icon, size=24, color=color),
                    style={
                        "width": "50px",
                        "height": "50px",
                        "background": f"{color}100",
                        "border_radius": RADIUS["xl"],
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "border": f"1px solid {color}35"
                    }
                ),

                rx.spacer(),

                # Número grande a la derecha
                rx.text(
                    value,
                    style={
                        "font_size": "2.5rem",
                        "font_weight": "800",
                        "color": color,
                        "line_height": "1"
                    }
                ),

                align="center",
                width="100%"
            ),

            # Título descriptivo abajo
            rx.text(
                title,
                style={
                    "font_size": "1rem",
                    "font_weight": "600",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "text_align": "center",
                    "margin_top": SPACING["1"]
                }
            ),

            spacing="3",
            align="stretch",
            width="100%",
            padding=SPACING["3"]
        ),

        # Utilizar función utilitaria de cristal reutilizable
        style=dark_crystal_card(color=color, hover_lift="6px"),
        width="100%"
    )

# ==========================================
# 📊 ESTADÍSTICAS DE SERVICIOS
# ==========================================

def servicios_stats() -> rx.Component:
    """📊 Grid de estadísticas minimalistas y elegantes para servicios"""
    return rx.grid(
        minimal_servicios_stat_card(
            title="Total Servicios",
            value=AppState.total_servicios.to_string(),
            icon="layers",
            color=COLORS["primary"]["600"],
            subtitle="en catálogo"
        ),
        minimal_servicios_stat_card(
            title="Servicios Activos",
            value=AppState.servicios_activos_count.to_string(),
            icon="check",
            color=COLORS["success"]["600"],
            subtitle="disponibles"
        ),
        minimal_servicios_stat_card(
            title="Precio Promedio",
            value=f"${AppState.precio_promedio_servicios:,.0f}",
            icon="dollar-sign",
            color=COLORS["warning"]["500"],
            subtitle="USD promedio"
        ),
        minimal_servicios_stat_card(
            title="Categorías",
            value=AppState.categorias_servicios.length().to_string(),
            icon="grid-3x3",
            color=COLORS["secondary"]["600"],
            subtitle="especializadas"
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="4"),
        spacing="6",
        width="100%",
        margin_bottom="8"
    )

# ==========================================
# 🔍 FILTROS Y BÚSQUEDA
# ==========================================

def filtros_servicios() -> rx.Component:
    """🔍 Panel de filtros y búsqueda con glassmorphism"""
    return rx.box(
        rx.vstack(
            # Header de filtros
            rx.hstack(
                rx.icon("filter", size=20, color=COLORS["primary"]["500"]),
                rx.text(
                    "Filtros y Búsqueda",
                    size="4",
                    weight="bold",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                spacing="2",
                align_items="center"
            ),

            # Búsqueda principal
            rx.input(
                placeholder="Buscar servicios por nombre o descripción...",
                value=AppState.termino_busqueda_servicios,
                on_change=AppState.buscar_servicios,
                style={
                    "width": "100%",
                    "background": DARK_THEME["colors"]["surface_secondary"],
                    "border": f"1px solid {DARK_THEME['colors']['border']}",
                    "border_radius": RADIUS["md"],
                    "padding": SPACING["3"],
                    "_focus": {
                        "border_color": COLORS["primary"]["500"],
                        "box_shadow": f"0 0 0 3px {COLORS['primary']['500']}20"
                    }
                }
            ),

            # Filtros en línea
            rx.hstack(
                # Filtro por categoría
                rx.vstack(
                    rx.text("Categoría", size="2", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.select(
                        AppState.opciones_categoria_completas,
                        value=AppState.filtro_categoria,
                        on_change=AppState.filtrar_por_categoria,
                        placeholder="Todas las categorías",
                        style={"width": "200px"}
                    ),
                    spacing="1"
                ),

                # Filtro por estado
                rx.vstack(
                    rx.text("Estado", size="2", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.select(
                        ["todos", "activos", "inactivos"],
                        value=AppState.filtro_estado_servicio,
                        on_change=AppState.filtrar_por_estado_servicio,
                        placeholder="Todos los estados",
                        style={"width": "150px"}
                    ),
                    spacing="1"
                ),

                # Solo activos switch
                rx.vstack(
                    rx.text("Vista", size="2", weight="medium", color=DARK_THEME["colors"]["text_secondary"]),
                    rx.switch(
                        checked=AppState.mostrar_solo_activos_servicios,
                        on_change=lambda v: AppState.set_mostrar_solo_activos_servicios(v),
                        color_scheme="cyan"
                    ),
                    spacing="1"
                ),

                spacing="6",
                align_items="end",
                width="100%"
            ),

            spacing="4",
            width="100%"
        ),
        style=dark_crystal_card(color=COLORS["primary"]["500"]),
        width="100%"
    )

# ==========================================
# 🎯 HEADER ELEGANTE PARA SERVICIOS
# ==========================================

def clean_servicios_header() -> rx.Component:
    """🎯 Header limpio y elegante para servicios (patrón Personal/Pacientes)"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                # Título principal alineado a la izquierda
                rx.heading(
                    "🏥 Gestión de Servicios",
                    style={
                        "font_size": "2.75rem",
                        "font_weight": "800",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent",
                        "line_height": "1.2",
                        "text_align": "left"
                    }
                ),

                # Subtítulo elegante
                rx.text(
                    "Administra el catálogo completo de servicios odontológicos",
                    style={
                        "font_size": "1.125rem",
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "line_height": "1.5",
                        "opacity": "0.8"
                    }
                ),

                spacing="1",
                align="start",
                width="100%"
            ),

            rx.spacer(),

            # Botón de actualización
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("refresh-cw", size=16),
                        rx.text("Actualizar", size="2"),
                        spacing="2"
                    ),
                    on_click=AppState.cargar_lista_servicios,
                    variant="outline",
                    color_scheme="cyan",
                    size="2"
                ),
                spacing="2"
            ),

            width="100%",
            align_items="center"
        ),
        # Utilizar función utilitaria para header
        style=dark_header_style(),
        width="100%"
    )

# ==========================================
# 📋 TABLA DE SERVICIOS
# ==========================================

def servicios_table() -> rx.Component:
    """📋 Tabla principal de servicios con glassmorphism"""
    return rx.box(
        rx.vstack(
            # Header de tabla
            rx.hstack(
                rx.text(
                    "📋 Catálogo de Servicios",
                    size="5",
                    weight="bold",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                rx.spacer(),
                rx.cond(
                    AppState.rol_usuario == "gerente",
                    rx.button(
                        rx.hstack(
                            rx.icon("plus", size=16),
                            rx.text("Nuevo Servicio", size="2"),
                            spacing="2"
                        ),
                        on_click=lambda: AppState.seleccionar_y_abrir_modal_servicio(""),
                        variant="solid",
                        color_scheme="cyan",
                        size="2"
                    ),
                    rx.text("Vista de solo lectura", size="2", color=DARK_THEME["colors"]["text_secondary"])
                ),
                width="100%",
                align_items="center"
            ),

            # Tabla responsive
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Código"),
                        rx.table.column_header_cell("Servicio"),
                        rx.table.column_header_cell("Categoría"),
                        rx.table.column_header_cell("Precio"),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Acciones", display=rx.cond(AppState.rol_usuario == "gerente", "table-cell", "none"))
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        AppState.servicios_filtrados,
                        servicio_row
                    )
                ),
                style={
                    "width": "100%",
                    "background": DARK_THEME["colors"]["surface_secondary"]
                },
                size="2"
            ),

            spacing="4",
            width="100%"
        ),
        style=dark_table_container(),
        width="100%"
    )

def servicio_row(servicio) -> rx.Component:
    """🔗 Fila de servicio en tabla"""
    return rx.table.row(
        rx.table.cell(
            rx.badge(
                servicio.codigo,
                color_scheme="blue",
                size="1"
            )
        ),
        rx.table.cell(
            rx.vstack(
                rx.text(
                    servicio.nombre,
                    size="3",
                    weight="medium",
                    color=DARK_THEME["colors"]["text_primary"]
                ),
                rx.text(
                    servicio.descripcion,
                    size="2",
                    color=DARK_THEME["colors"]["text_secondary"],
                    style={"overflow": "hidden", "text_overflow": "ellipsis", "white_space": "nowrap", "max_width": "200px"}
                ),
                spacing="1",
                align_items="start"
            )
        ),
        rx.table.cell(
            rx.badge(
                servicio.categoria,
                color_scheme="green",
                size="1"
            )
        ),
        rx.table.cell(
            rx.text(
                f"${servicio.precio_base_usd:,.0f} USD",
                size="3",
                weight="medium",
                color=COLORS["warning"]["500"]
            )
        ),
        rx.table.cell(
            rx.badge(
                rx.cond(
                    servicio.activo,
                    "Activo",
                    "Inactivo"
                ),
                color_scheme=rx.cond(
                    servicio.activo,
                    "green",
                    "gray"
                ),
                size="1"
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    rx.icon("pencil", size=14),
                    on_click=lambda: AppState.seleccionar_y_abrir_modal_servicio(servicio.id),
                    variant="ghost",
                    size="1",
                    color_scheme="blue"
                ),
                rx.cond(
                    servicio.activo,
                    # Si está activo, mostrar botón para desactivar
                    rx.button(
                        rx.icon("eye-off", size=14),
                        on_click=lambda: AppState.activar_desactivar_servicio(servicio.id, False),
                        variant="ghost",
                        size="1",
                        color_scheme="orange"
                    ),
                    # Si está inactivo, mostrar botón para activar
                    rx.button(
                        rx.icon("eye", size=14),
                        on_click=lambda: AppState.activar_desactivar_servicio(servicio.id, True),
                        variant="ghost",
                        size="1",
                        color_scheme="green"
                    )
                ),
                spacing="1"
            ),
            display=rx.cond(AppState.rol_usuario == "gerente", "table-cell", "none")
        )
    )

# ==========================================
# 📱 PÁGINA PRINCIPAL
# ==========================================


def servicios_page() -> rx.Component:
    """
    🏥 PÁGINA DE GESTIÓN DE SERVICIOS - REFACTORIZADA CON TEMA ELEGANTE

    ✨ Características actualizadas:
    - Diseño moderno con glassmorphism siguiendo patrón Personal/Pacientes
    - Header limpio y elegante con gradientes
    - Cards de estadísticas minimalistas
    - Formularios modernizados con efectos cristal
    - Tema oscuro unificado
    - Animaciones suaves y micro-interacciones
    """
    return rx.fragment(
        medical_page_layout(
            rx.vstack(
                # Header limpio y elegante
                clean_servicios_header(),

                # Estadísticas con cards modernos
                servicios_stats(),

                # Filtros con glassmorphism
                filtros_servicios(),

                # Tabla principal con diseño actualizado
                servicios_table(),

                spacing="6",
                width="100%"
            ),
        ),
        # Modales usando componentes de forms.py
        service_form_modal()
        # on_mount eliminado: datos se cargan en post_login_inicializacion()
    )