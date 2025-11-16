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
from dental_system.components.common import medical_page_layout, stat_card, page_header, confirmation_modal, refresh_button
from dental_system.components.forms import service_form_modal
from dental_system.components.table_components import servicios_table
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, DARK_THEME, GRADIENTS,
    dark_crystal_card, dark_header_style, create_dark_style
)

# ==========================================
# 📊 ESTADÍSTICAS DE SERVICIOS
# ==========================================

def servicios_stats() -> rx.Component:
    """📊 Grid de estadísticas minimalistas y elegantes para servicios"""
    return rx.grid(
        stat_card(
            title="Total Servicios",
            value=AppState.total_servicios_computed.to_string(),
            icon="layers",
            color=COLORS["primary"]["600"],
            # subtitle="en catálogo"
        ),
        stat_card(
            title="Servicios Activos",
            value=AppState.servicios_activos_count.to_string(),
            icon="check",
            color=COLORS["success"]["600"],
            # subtitle="disponibles"
        ),
        stat_card(
            title="Precio Promedio USD",
            value=f"${AppState.precio_promedio_servicios:,.0f}",
            icon="dollar-sign",
            color=COLORS["warning"]["500"],
            # subtitle="USD promedio"
        ),
        stat_card(
            title="Categorías",
            value=AppState.categorias_servicios.length().to_string(),
            icon="grid-3x3",
            color=COLORS["secondary"]["600"],
            # subtitle="especializadas"
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="4"),
        spacing="6",
        width="100%",
        # margin_bottom="8"
    )

# ==========================================
# 📋 TABLA DE SERVICIOS
# ==========================================


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
    - Tabla reutilizable de table_components.py
    - Formularios modernizados con efectos cristal
    - Tema oscuro unificado
    - Animaciones suaves y micro-interacciones
    """
    return rx.fragment(
        medical_page_layout(
            rx.vstack(
                page_header(
                   "Gestión de Servicios",
                   "Administra el catálogo completo de servicios odontológicos",
                   actions=[
                       refresh_button(
                           text="Actualizar datos",
                           on_click=AppState.cargar_lista_servicios,
                           loading=AppState.cargando_operacion_servicio
                       )
                   ]
                ),

                # Estadísticas con cards modernos
                servicios_stats(),

                rx.box(
                    servicios_table(),
                    style=create_dark_style("dark_table"),
                    width="100%"
                ),

                spacing="3",
                width="100%"
            ),
        ),
        # Modales usando componentes de forms.py
        service_form_modal(),
        confirmation_modal()
    )