"""
🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA V3 - DISEÑO ENTERPRISE
==============================================================

REDISEÑO COMPLETO aplicando patrones de consultas_page_v41.py y personal_page.py:
- ✨ Glassmorphism médico premium con tema oscuro consistente
- 🎨 Clean page header con gradiente de texto
- 💎 Crystal cards con animaciones de hover
- 📱 Layout responsive mobile-first
- 🎯 Integración completa con themes.py
- 🚀 Componentes reutilizables del sistema
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button, medical_page_layout
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente
from dental_system.components.odontologia.panel_intervenciones_previas import panel_intervenciones_previas
from dental_system.components.odontologia.odontograma_status_bar_v3 import odontograma_status_bar_v3
from dental_system.components.odontologia.timeline_odontograma import (
    boton_ver_historial,
    modal_historial_odontograma
)
from dental_system.components.odontologia.modal_validacion import (
    modal_validacion_odontograma
)

# 🚀 V4.0 - COMPONENTES PROFESIONALES
from dental_system.components.odontologia.professional_odontogram_grid import professional_odontogram_grid
from dental_system.components.odontologia.tooth_detail_sidebar import tooth_detail_sidebar
from dental_system.components.odontologia.intervention_timeline import intervention_timeline
from dental_system.components.odontologia.odontogram_controls_bar import odontogram_controls_bar

# 🆕 NUEVA ESTRUCTURA - COMPONENTES SIN TABS
from dental_system.components.odontologia.tooth_conditions_table import tooth_conditions_table
from dental_system.components.odontologia.current_consultation_services_table import current_consultation_services_table
from dental_system.components.odontologia.modal_add_intervention import modal_add_intervention
from dental_system.components.odontologia.modal_change_condition import modal_change_condition
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,
    dark_crystal_card, dark_header_style, dark_page_background,
    create_dark_style, glassmorphism_card
)

# ==========================================
# 🎨 ESTILOS ENTERPRISE CONSISTENTES
# ==========================================

# Usando REFINED_COLORS importado de intervention_tabs_v2.py
# que está basado en DARK_THEME y componentes exitosos

# ==========================================
# 🏥 COMPONENTES ENTERPRISE REDESIGNED
# ==========================================

def clean_page_header_intervencion() -> rx.Component:
    """🏥 Header limpio aplicando patrón de personal_page.py"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "🦷 Intervención Odontológica",
                    style={
                        "font_size": "2.75rem",
                        "font_weight": "800",
                        "line_height": "1.2",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent"
                    }
                ),
                rx.text(
                    "Registro completo de tratamiento dental con odontograma interactivo",
                    size="4",
                    color=DARK_THEME["colors"]["text_secondary"],
                    font_weight="medium"
                ),
                spacing="1",
                align_items="start"
            ),
            
            rx.spacer(),
            
            # Acciones header consistentes con personal_page
            rx.hstack(
                # 🚀 FASE 4: Botón Ver Historial de Versiones (HABILITADO)
                boton_ver_historial(),

                # Botón Derivar a otro odontólogo
                rx.button(
                    rx.hstack(
                        rx.icon("arrow-right-left", size=16),
                        rx.text("Derivar Paciente", size="3"),
                        spacing="2"
                    ),
                    on_click=AppState.derivar_paciente_a_otro_odontologo,
                    variant="outline",
                    size="3",
                    style={
                        "background": f"linear-gradient(135deg, {COLORS['warning']['500']} 0%, {COLORS['warning']['400']} 100%)",
                        "border": f"1px solid {COLORS['warning']['400']}",
                        "color": "white",
                        "backdrop_filter": "blur(10px)",
                        "font_weight": "600",
                        "_hover": {
                            "transform": "translateY(-2px)",
                            "box_shadow": f"0 4px 12px {COLORS['warning']['500']}40"
                        }
                    }
                ),

                # Botón Volver
                rx.button(
                    rx.hstack(
                        rx.icon("arrow-left", size=16),
                        rx.text("Volver", size="3"),
                        spacing="2"
                    ),
                    on_click=lambda: AppState.navigate_to("odontologia"),
                    variant="outline",
                    size="3",
                    style={
                        **glassmorphism_card(),
                    #     "background": COLORS["background"]["card"],
                    #     "border": f"1px solid {COLORS['border']['default']}",
                    #     "color": COLORS["text"]["primary"],
                    #     "backdrop_filter": "blur(10px)",
                    #     "_hover": {
                    #         "background": COLORS["background"]["elevated"],
                    #         "transform": "translateY(-2px)"
                    #     }
                    }
                    
                ),
                spacing="3"
            ),
            
            width="100%",
            align="center"
        ),
        style=dark_header_style(),
        width="100%"
    )

def stats_intervencion() -> rx.Component:
    """📊 Stats de intervención aplicando patrón minimal_stat_card"""
    return rx.grid(
        # Paciente actual
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("user", size=20, color=COLORS["primary"]["400"]),
                    rx.vstack(
                        rx.text(
                            AppState.paciente_actual.nombre_completo,
                            font_weight="700",
                            size="4",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),
                        rx.text(
                            f"HC: {AppState.paciente_actual.numero_historia}",
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align_items="center"
                ),
                spacing="2",
                width="100%"
            ),
            style=dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px")
        ),
        
        # Estado consulta
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("activity", size=20, color=COLORS["success"]["400"]),
                    rx.vstack(
                        rx.text(
                            "Estado: En Atención",
                            font_weight="700",
                            size="4",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),
                        rx.text(
                            f"Consulta: {AppState.consulta_actual.numero_consulta}",
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align_items="center"
                ),
                spacing="2",
                width="100%"
            ),
            style=dark_crystal_card(color=COLORS["success"]["500"], hover_lift="4px")
        ),
        
        # Tab activo
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("clipboard-list", size=20, color=COLORS["warning"]["500"]),
                    rx.vstack(
                        rx.text(
                            AppState.active_intervention_tab.capitalize(),
                            font_weight="700",
                            size="4",
                            color=DARK_THEME["colors"]["text_primary"]
                        ),
                        rx.text(
                            "Sección Activa",
                            size="2",
                            color=DARK_THEME["colors"]["text_secondary"]
                        ),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="3",
                    align_items="center"
                ),
                spacing="2",
                width="100%"
            ),
            style=dark_crystal_card(color=COLORS["warning"]["500"], hover_lift="4px")
        ),
        
        columns=rx.breakpoints(initial="1", sm="2", lg="3"),
        spacing="4",
        width="100%",
        margin_bottom="6"
    )

# ==========================================
# 🦷 V4.0 - TAB ODONTOGRAMA PROFESIONAL
# ==========================================

def odontogram_tab_v4() -> rx.Component:
    """
    🦷 TAB DE ODONTOGRAMA V4.0 - DISEÑO PROFESIONAL SIMPLIFICADO

    ✨ CARACTERÍSTICAS V4.0:
    - 1 diente = 1 componente (sin división de superficies)
    - NO muestra costos/precios (solo información clínica)
    - 2 tabs laterales: Historial + Info (sin planificación)
    - Timeline filtrable de intervenciones
    - 100% componentes declarativos rx.*

    🎨 ARQUITECTURA:
    - Control bar superior: Info paciente + acciones
    - Grid principal: Odontograma 32 dientes FDI
    - Sidebar condicional: Detalles del diente seleccionado
    - Timeline expandible: Historial filtrable
    """
    return rx.box(
        rx.vstack(
            # 📊 BARRA DE CONTROL SUPERIOR V4.0
            odontogram_controls_bar(
                patient_name=AppState.get_patient_display_name,
                patient_id=AppState.get_patient_id_display,
                show_timeline=AppState.show_timeline,
                has_odontogram_changes=AppState.tiene_cambios_odontograma,
                has_selected_services=AppState.tiene_servicios_seleccionados,
                is_saving=AppState.odontograma_guardando,
                on_save_diagnosis=AppState.guardar_solo_diagnostico_odontograma,
                on_save_intervention=AppState.guardar_intervencion_completa,
                on_export=lambda: rx.window_alert("Exportar PDF (próximamente)"),
                on_print=lambda: rx.window_alert("Imprimir (próximamente)"),
                on_toggle_timeline=AppState.toggle_timeline,
            ),

            # 📋 TIMELINE EXPANDIBLE V4.0 (CON DATOS REALES)
            rx.cond(
                AppState.show_timeline,
                rx.box(
                    intervention_timeline(
                        selected_tooth=AppState.selected_tooth,
                        interventions=AppState.get_filtered_interventions,
                        dentists=AppState.get_available_dentists,
                        procedures=AppState.get_available_procedures,
                        total_count=AppState.get_interventions_count,
                        filter_dentist=AppState.timeline_filter_dentist,
                        filter_procedure=AppState.timeline_filter_procedure,
                        filter_period=AppState.timeline_filter_period,
                        on_filter_change=AppState.update_timeline_filter,
                    ),
                    width="100%",
                    margin_bottom="4"
                ),
            ),

            # 🦷 LAYOUT PRINCIPAL: ODONTOGRAMA + SIDEBAR
            rx.hstack(
                # Grid de odontograma (ancho completo o 70% si hay sidebar)
                rx.box(
                    professional_odontogram_grid(
                        selected_tooth=AppState.selected_tooth,
                        teeth_data=AppState.get_teeth_data,
                        on_tooth_click=AppState.select_tooth,
                    ),
                    flex="1",
                    min_width="0"  # Evita overflow
                ),

                # Sidebar de detalles del diente (condicional)
                rx.cond(
                    AppState.selected_tooth,
                    rx.box(
                        tooth_detail_sidebar(
                            tooth_number=AppState.selected_tooth,
                            status=AppState.get_tooth_status,
                            active_tab=AppState.active_sidebar_tab,
                            interventions=AppState.get_tooth_interventions,
                            conditions=AppState.get_tooth_conditions,
                            on_close=AppState.close_sidebar,
                            on_tab_change=AppState.change_sidebar_tab,
                        ),
                        width="400px",
                        flex_shrink="0"
                    ),
                ),

                spacing="4",
                width="100%",
                align_items="start"
            ),

            # 📋 TABLA DE SERVICIOS DE CONSULTA ACTUAL (NUEVA ESTRUCTURA)
            current_consultation_services_table(),

            spacing="4",
            width="100%"
        ),

        # Estilos del contenedor principal
        style={
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="0px"),
            "padding": "24px",
            "min_height": "600px"
        },
        width="100%"
    )

def panel_paciente_enterprise() -> rx.Component:
    """👤 Panel paciente con diseño enterprise"""
    return rx.box(
        panel_informacion_paciente(),
        style={
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="6px"),
            "height": "fit-content",
            "min_height": "500px"
        },
        width="100%"
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL ENTERPRISE REDESIGNED
# ==========================================

def intervencion_page_v2() -> rx.Component:
    """
    🦷 PÁGINA INTERVENCIÓN ODONTOLÓGICA V3 - ENTERPRISE DESIGN
    
    ✨ CARACTERÍSTICAS ENTERPRISE APLICADAS:
    - 🎨 Clean page header con gradiente de texto (patrón personal_page)
    - 💎 Stats cards con glassmorphism (patrón minimal_stat_card)
    - 🌙 Tema oscuro consistente con consultas_page_v41
    - 📱 Layout responsive mobile-first
    - 🔄 Animaciones de hover y microinteracciones
    - 🎯 Crystal cards con efectos premium
    - 🚀 Integración completa themes.py
    
    🏗️ ARQUITECTURA:
    - Layout: medical_page_layout wrapper (PATRÓN CONSULTAS)
    - Grid responsive: Adapta de 1 col (móvil) a 2 cols (desktop) 
    - Colores: REFINED_COLORS basado en DARK_THEME y componentes exitosos
    - Componentes: Reutiliza funciones dark_crystal_card, clean_header
    """
    return rx.box(
        medical_page_layout(
            rx.vstack(
                # Header enterprise con gradiente
                clean_page_header_intervencion(),
                
                # Stats cards aplicando patrón minimal_stat_card
                stats_intervencion(),

                # 🚀 BARRA DE ESTADO ODONTOGRAMA V3.0
                rx.box(
                    odontograma_status_bar_v3(),
                    width="100%",
                    margin_bottom="4"
                ),

                # Panel de intervenciones previas (si existen)
                panel_intervenciones_previas(),

                # Layout principal responsive
                rx.grid(
                    # Panel paciente (sidebar)
                    panel_paciente_enterprise(),

                    # 🚀 V4.0 - Panel central con ODONTOGRAMA PROFESIONAL
                    # Reemplaza intervention_tabs_integrated() por odontogram_tab_v4()
                    odontogram_tab_v4(),

                    columns=rx.breakpoints(
                        initial="1",    # Móvil: stack vertical
                        md="1",         # Tablet: stack vertical
                        lg="320px 1fr", # Desktop: sidebar + main
                        xl="350px 1fr"  # XL: sidebar más ancho
                    ),
                    spacing="6",
                    width="100%",
                    min_height="calc(100vh - 220px)"
                ),
                
                spacing="6",
                width="100%",
                max_width="1600px",
                align="center"
            ),

            
        ),

        # 🆕 NUEVA ESTRUCTURA - MODALES
        modal_add_intervention(),
        modal_change_condition(),

    )