"""
🦷 PÁGINA DE INTERVENCIÓN ODONTOLÓGICA V3 - DISEÑO ENTERPRISE
==============================================================

"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import  medical_page_layout, page_header
from dental_system.components.odontologia.panel_paciente import panel_informacion_paciente

# 🚀 V4.0 - COMPONENTES PROFESIONALES
from dental_system.components.odontologia.professional_odontogram_grid import professional_odontogram_grid
from dental_system.components.odontologia.odontogram_controls_bar import odontogram_controls_bar

# 🆕 NUEVA ESTRUCTURA - COMPONENTES SIN TABS

from dental_system.components.odontologia.current_consultation_services_table import current_consultation_services_table
from dental_system.components.odontologia.modal_add_intervention import modal_add_intervention
from dental_system.components.odontologia.modal_change_condition import modal_change_condition
from dental_system.components.odontologia.patient_history_section import patient_history_section
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING, SHADOWS, DARK_THEME, GRADIENTS,
    dark_crystal_card, dark_header_style, glassmorphism_card
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
                    style=glassmorphism_card()
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
            # ⚠️ COMENTADO TEMPORALMENTE - Este componente usa funciones obsoletas
            odontogram_controls_bar(
                patient_name=f"{AppState.paciente_actual.primer_nombre} {AppState.paciente_actual.primer_apellido}",
                patient_hc=AppState.paciente_actual.numero_historia,
                show_timeline=AppState.show_timeline,
                has_odontogram_changes=AppState.tiene_cambios_odontograma,
                has_selected_services=AppState.tiene_servicios_seleccionados,
                is_saving=AppState.odontograma_guardando,
                on_save_intervention=AppState.finalizar_mi_intervencion_odontologo,
                on_export=lambda: rx.window_alert("Exportar PDF (próximamente)"),
                on_print=lambda: rx.window_alert("Imprimir (próximamente)"),

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

                spacing="4",
                width="100%",
                align_items="start"
            ),

            # 📋 TABLA DE SERVICIOS DE CONSULTA ACTUAL (NUEVA ESTRUCTURA)
            current_consultation_services_table(),

            # 📚 HISTORIAL DE INTERVENCIONES DEL PACIENTE (2025-10-16)
            patient_history_section(),

            spacing="4",
            width="100%"
        ),

        # Estilos del contenedor principal
        style={
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="0px"),
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

    """
    return rx.box(
        medical_page_layout(
            rx.vstack(
                page_header(
                    "Intervención Odontológica",
                    "Registro completo de tratamiento dental con odontograma interactivo",
                    actions=[
                        rx.button(
                            rx.hstack(
                                rx.icon("arrow-left", size=16),
                                rx.text("Volver", size="3"),
                                spacing="2"
                            ),
                            on_click=lambda: AppState.navigate_to("odontologia"),
                            variant="outline",
                            size="3",
                            style=glassmorphism_card()
                        ),
                    ]
                ),
                # Stats cards aplicando patrón minimal_stat_card
                stats_intervencion(),

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