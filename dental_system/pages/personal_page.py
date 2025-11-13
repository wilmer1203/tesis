"""
🏥 PÁGINA DE GESTIÓN DE PERSONAL - VERSIÓN REFACTORIZADA
=======================================================

✨ Diseño moderno y elegante con:
- UI cards con glassmorphism effect
- Animaciones suaves y micro-interacciones 
- Diseño responsive mobile-first
- Modales optimizados con mejor UX
- Componentes reutilizables y escalables
- Tema oscuro/claro compatible

Desarrollado para Reflex.dev con patrones modernos
"""

import reflex as rx
from dental_system.components.common import (
    medical_page_layout,
    medical_toast_container,
    confirmation_modal,
    stat_card,
    page_header,
    refresh_button
)
from dental_system.components.table_components import personal_table
from dental_system.state.app_state import AppState
from dental_system.components.modal_personal import multi_step_staff_form
from dental_system.styles.themes import (
    COLORS, 
    SHADOWS, 
    RADIUS, 
    SPACING, 
    ANIMATIONS, 
    GRADIENTS,
    GLASS_EFFECTS,
    DARK_THEME,
    create_dark_style,
    dark_header_style
)

# ==========================================
# ESTADÍSTICAS DE PERSONAL
# ==========================================

def personal_stats() -> rx.Component:
    """📊 Grid de estadísticas minimalistas y elegantes"""
    return rx.grid(
        stat_card(
            title="Total Personal",
            value="10",#  AppState.estadisticas_personal.total.to_string(),
            icon="users",
            color=COLORS["secondary"]["600"]
        ),
        stat_card(
            title="Odontólogos",
            value="10",# AppState.estadisticas_personal.odontologos.to_string(),
            icon="stethoscope",
            color=COLORS["secondary"]["600"]
        ),
        stat_card(
            title="Administrativos",
            value= "10",#(AppState.estadisticas_personal.administradores + 
                #    AppState.estadisticas_personal.asistentes + 
                #    AppState.estadisticas_personal.gerentes).to_string(),
            icon="briefcase",
            color=COLORS["secondary"]["600"]
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="3"),
        spacing="6",
        width="100%",
        margin_bottom="6"
    )



def personal_page() -> rx.Component:
    """
    🏥 PÁGINA DE GESTIÓN DE PERSONAL - REFACTORIZADA CON TOASTS
    
    ✨ Características mejoradas:
    - Diseño moderno con glassmorphism
    - Animaciones suaves y micro-interacciones
    - Layout responsive mobile-first 
    - Cards de estadísticas elegantes
    - Header con gradientes y efectos
    - Sistema de toasts flotantes
    """
    return rx.fragment(
        # Contenedor de toasts flotantes
        medical_toast_container(),
        
        # Layout principal usando el wrapper
        medical_page_layout(
            rx.vstack(
                # Header limpio y elegante
                # clean_page_header(),
                page_header(
                   "Gestión de Personal",
                   "Administra empleados, roles y permisos del sistema",
                   actions=[
                       refresh_button(
                           text="Actualizar datos",
                           on_click=AppState.cargar_lista_personal,
                           loading=AppState.cargando_operacion_personal
                       )
                   ]
                ),
                personal_stats(),
                # Tabla de personal con diseño actualizado
                rx.box(
                    personal_table(),
                    style=create_dark_style("dark_table"),
                    width="100%"
                ),
                
                spacing="3",
                width="100%"
            )
        ),

        # Modales
        multi_step_staff_form(),
        confirmation_modal()  # Modal genérico de confirmación para inhabilitación
    )