"""
👥 PÁGINA DE GESTIÓN DE PACIENTES - VERSIÓN REFACTORIZADA
========================================================

✨ Sistema moderno de gestión de pacientes:
- Header elegante con búsqueda integrada
- Cards de estadísticas con glassmorphism effect
- Modales de formulario optimizados con mejor UX
- Sistema de filtros avanzado y responsive
- Tabla moderna con acciones contextuales
- Diseño mobile-first con animaciones suaves

Desarrollado para Reflex.dev con patrones modernos
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import stat_card, page_header, medical_page_layout, refresh_button
from dental_system.components.table_components import patients_table
from dental_system.components.modal_paciente import multi_step_patient_form
from dental_system.styles.themes import (
    COLORS, 
    SHADOWS, 
    RADIUS, 
    SPACING, 
    ANIMATIONS, 
    GRADIENTS,
    GLASS_EFFECTS,
    DARK_THEME,
    dark_crystal_card,
    create_dark_style,
    dark_header_style
)

# ==========================================
# 🎨 COMPONENTES MODERNOS PARA PACIENTES
# ==========================================

def clean_patients_header() -> rx.Component:
    """🎯 Header limpio y elegante para pacientes (patrón Personal)"""
    return rx.box(
        rx.vstack(
            # Título principal alineado a la izquierda
            rx.heading(
                "Gestión de Pacientes",
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
                "Administra el registro completo de pacientes con historial médico digital",
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
        # Utilizar función utilitaria para header
        style=dark_header_style(),
        width="100%"
    )

def patients_stats() -> rx.Component:
    """📈 Grid de estadísticas minimalistas y elegantes para pacientes"""
    return rx.grid(
        stat_card(
            title="Total Pacientes",
            value=AppState.lista_pacientes.length().to_string(),
            icon="users",
            color=COLORS["primary"]["600"]
        ),
        stat_card(
            title="Pacientes Masculinos",
            value=AppState.total_pacientes_masculinos.to_string(),
            icon="user-check",
            color=COLORS["success"]["600"]
        ),
        stat_card(
            title="Pacientes Femeninos",
            value=AppState.total_pacientes_femeninos.to_string(),
            icon="user-plus",
            color=COLORS["secondary"]["600"]
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="3"),
        spacing="6",
        width="100%",
        margin_bottom="8"
    )

      

def pacientes_page() -> rx.Component:
    """
    👥 PÁGINA DE GESTIÓN DE PACIENTES - REFACTORIZADA CON TEMA ELEGANTE
    
    ✨ Características actualizadas:
    - Diseño moderno con glassmorphism siguiendo patrón Personal
    - Header limpio y elegante
    - Cards de estadísticas minimalistas
    - Búsqueda y controles simplificados
    - Tema oscuro con efectos cristal
    - Animaciones suaves y micro-interacciones
    """
    return rx.fragment(
        medical_page_layout(
            rx.vstack(
                # Header limpio y elegante
                page_header(
                    "Gestión de Pacientes",
                    "Administra el registro completo de pacientes con historial médico digital",
                    actions=[
                        refresh_button(
                            text="Actualizar datos",
                            on_click=AppState.cargar_lista_pacientes,
                            loading=AppState.cargando_lista_pacientes
                        )
                    ]
                ),
                # Estadísticas con cards modernos
                patients_stats(),
                    
                # Tabla de pacientes con diseño actualizado - Usar función utilitaria
                rx.box(
                    patients_table(),
                    style=create_dark_style("dark_table"),
                    width="100%"
                ),
                spacing="3",
                width="100%"
            ),
        ),
        multi_step_patient_form(),  # ✅ Formulario multi-step reactivado
    )
