# 🦷 PÁGINA PRINCIPAL DE ODONTOLOGÍA - ATENCIÓN CLÍNICA REFACTORIZADA
# dental_system/pages/odontologia_page.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, secondary_button
from dental_system.components.odontologia.dashboard_stats import odontologia_dashboard_stats
from dental_system.components.odontologia.consulta_card import (
    lista_consultas_asignadas, 
    lista_consultas_disponibles,
    seccion_header
)
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS ESPECÍFICOS PARA ODONTOLOGÍA
# ==========================================

SECTION_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": SHADOWS["sm"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["6"],
    "width": "100%",
    "height": "calc(100vh - 200px)",  # Altura fija para scroll
    "overflow": "hidden"
}

SCROLLABLE_CONTENT_STYLE = {
    "height": "calc(100% - 60px)",  # Espacio para header
    "overflow_y": "auto",
    "overflow_x": "hidden",
    "padding_right": SPACING["2"]
}

# ==========================================
# 🔍 COMPONENTES DE BÚSQUEDA Y FILTROS
# ==========================================

def barra_busqueda_y_filtros() -> rx.Component:
    """🔍 Barra de búsqueda y filtros para pacientes"""
    return rx.hstack(
        # Campo de búsqueda
        rx.input(
            placeholder="Buscar paciente por nombre, documento o HC...",
            value=AppState.termino_busqueda_pacientes,
            on_change=AppState.buscar_pacientes_asignados,
            width="40%"
        ),
        
        rx.spacer(),
        
        # Filtros rápidos
        rx.hstack(
            rx.select(
                ["Todos", "Programada", "En Progreso", "Completada"],
                value=AppState.filtro_estado_consulta,
                on_change=AppState.filtrar_por_estado_consulta,
                placeholder="Estado",
                width="120px"
            ),
            
            rx.button(
                "🚨 Solo Urgentes",
                size="2",
                variant=rx.cond(AppState.mostrar_solo_urgencias, "solid", "outline"),
                color_scheme=rx.cond(AppState.mostrar_solo_urgencias, "red", "gray"),
                on_click=AppState.alternar_mostrar_urgencias
            ),
            
            spacing="2"
        ),
        
        # Botón de actualización
        rx.button(
            "🔄 Actualizar",
            size="2",
            variant="outline",
            loading=AppState.cargando_pacientes_asignados,
            on_click=[
                AppState.cargar_pacientes_asignados,
                AppState.cargar_consultas_disponibles_otros,
                AppState.cargar_estadisticas_dia
            ]
        ),
        
        spacing="4",
        align_items="center",
        width="100%",
        margin_bottom="6"
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL REFACTORIZADA
# ==========================================

def odontologia_page() -> rx.Component:
    """
    🦷 Página principal de odontología - VERSIÓN REFACTORIZADA
    
    Nueva arquitectura con componentes especializados:
    - Dashboard de estadísticas optimizado
    - Dos columnas: Mis consultas + Disponibles
    - Componentes reutilizables y tipados
    - Navegación fluida y UX mejorada
    """
    return rx.vstack(
        # Header principal
        page_header(
            "🦷 Atención Odontológica", 
            "Dashboard profesional - Sistema por orden de llegada"
        ),
        
        # Dashboard de estadísticas (nuevo componente especializado)
        odontologia_dashboard_stats(),
        
        # Barra de búsqueda y filtros
        barra_busqueda_y_filtros(),
        
        # Layout principal de dos columnas
        rx.hstack(
            # ==========================================
            # COLUMNA IZQUIERDA: MIS CONSULTAS ASIGNADAS
            # ==========================================
            rx.box(
                rx.vstack(
                    # Header de sección
                    seccion_header(
                        titulo="Mis Consultas",
                        cantidad=AppState.estadisticas_dashboard_optimizadas["pacientes_asignados"],
                        icono="👥",
                        color="blue"
                    ),
                    
                    # Contenido scrolleable
                    rx.box(
                        lista_consultas_asignadas(),
                        style=SCROLLABLE_CONTENT_STYLE
                    ),
                    
                    spacing="0",
                    height="100%"
                ),
                style=SECTION_CONTAINER_STYLE,
                width="50%"
            ),
            
            # ==========================================  
            # COLUMNA DERECHA: CONSULTAS DISPONIBLES
            # ==========================================
            rx.box(
                rx.vstack(
                    # Header de sección
                    seccion_header(
                        titulo="Pacientes Disponibles",
                        cantidad=AppState.estadisticas_dashboard_optimizadas["pacientes_disponibles"],
                        icono="🔄",
                        color="success"
                    ),
                    
                    # Contenido scrolleable
                    rx.box(
                        lista_consultas_disponibles(),
                        style=SCROLLABLE_CONTENT_STYLE
                    ),
                    
                    spacing="0",
                    height="100%"
                ),
                style=SECTION_CONTAINER_STYLE,
                width="50%"
            ),
            
            spacing="6",
            width="100%",
            align_items="start",
            height="calc(100vh - 200px)"
        ),
        
        # Footer con información y accesos rápidos
        rx.box(
            rx.hstack(
                rx.text(
                    AppState.resumen_actividad_dia,
                    font_size="14px",
                    color=COLORS["gray"]["600"]
                ),
                
                rx.spacer(),
                
                # Accesos rápidos
                rx.hstack(
                    rx.cond(
                        AppState.en_formulario_intervencion,
                        rx.button(
                            "← Volver a Intervención",
                            size="2",
                            color_scheme="blue",
                            on_click=lambda: AppState.navigate_to("intervencion")
                        )
                    ),
                    
                    secondary_button(
                        text="Ver Reportes",
                        icon="bar-chart"
                    ),
                    
                    spacing="2"
                ),
                
                spacing="4",
                align_items="center",
                width="100%"
            ),
            background=COLORS["gray"]["50"],
            border_top=f"1px solid {COLORS['gray']['200']}",
            padding=SPACING["4"],
            width="100%"
        ),
        
        # Loading overlay global
        rx.cond(
            AppState.cargando_pacientes_asignados,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color="primary"),
                    rx.text(
                        "Actualizando datos de odontología...",
                        font_size="14px",
                        color=COLORS["gray"]["600"]
                    ),
                    spacing="3",
                    align_items="center"
                ),
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                background="rgba(255, 255, 255, 0.8)",
                z_index="999"
            )
        ),
        
        spacing="6",
        padding="6",
        width="100%",
        min_height="100vh",
        background=COLORS["gray"]["25"]
    )