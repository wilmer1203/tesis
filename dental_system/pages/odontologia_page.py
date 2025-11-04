# 🦷 PÁGINA PRINCIPAL DE ODONTOLOGÍA - ATENCIÓN CLÍNICA REFACTORIZADA
# dental_system/pages/odontologia_page.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import  secondary_button
from dental_system.components.odontologia.consulta_card import (
    lista_consultas_disponibles,
    lista_consultas_compactas,
    estadisticas_cola_odontologo,
    seccion_header
)
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING,ANIMATIONS,
    dark_crystal_card, dark_header_style,
    DARK_THEME,  create_dark_style
)
from dental_system.components.common import medical_page_layout
# ==========================================
# 🎨 ESTILOS PROFESIONALES TEMA OSCURO V2.0
# ==========================================

def odontologia_column_card(color: str = None, hover_lift: str = "4px") -> dict:
    """
    💎 Card estandarizado para columnas de odontología

    MEJORAS V2.0:
    - Sin altura fija (usa flex para adaptarse)
    - Padding consistente
    - Display flex para contenido interno
    """
    return {
        **dark_crystal_card(
            color=color or COLORS["primary"]["500"],
            hover_lift=hover_lift,
            padding=SPACING["5"],  # ✅ Padding estandarizado
        ),
        # ✅ MEJORA: Usar flex en vez de altura fija
        "display": "flex",
        "flex_direction": "column",
        "min_height": "500px",
        "max_height": "calc(100vh - 280px)",  # Espacio para header y stats
        "width": "100%",
        "overflow": "hidden"
    }

def medical_scrollable_content_v2() -> dict:
    """
    📜 Contenido scrolleable mejorado V2.0

    MEJORAS:
    - Usa flex: 1 para tomar espacio disponible
    - No depende de cálculos de altura
    - Scroll más suave
    """
    return {
        "flex": "1",  # ✅ Toma todo el espacio disponible
        "overflow_y": "auto",
        "overflow_x": "hidden",
        "padding_right": SPACING["2"],
        "scrollbar_width": "thin",
        "scrollbar_color": f"{DARK_THEME['colors']['accent']} {DARK_THEME['colors']['surface']}",
        # ✅ Scroll behavior suave
        "scroll_behavior": "smooth"
    }

# ==========================================
# 🚨 COMPONENTES MÉDICOS ESPECIALIZADOS
# ==========================================

def stat_card_odontologo(titulo: str, valor: str, color: str = "blue") -> rx.Component:
    """📊 Tarjeta de estadística simple para odontólogo"""
    color_map = {
        "blue": COLORS["blue"]["500"],
        "yellow": COLORS["warning"]["500"],  # Usar warning como amarillo
        "green": COLORS["success"]["500"],
        "red": COLORS["error"]["500"],
        "primary": COLORS["primary"]["500"]
    }

    return rx.box(
        rx.vstack(
            rx.text(titulo, size="2", color=DARK_THEME["colors"]["text_secondary"]),
            rx.text(valor, size="4", weight="bold", color=DARK_THEME["colors"]["text_primary"]),
            spacing="1",
            align="center"
        ),
        style={
            "background": DARK_THEME["colors"]["surface"],
            "border": f"1px solid {DARK_THEME['colors']['border']}",
            "border_radius": RADIUS["lg"],
            "padding": SPACING["4"],
            "backdrop_filter": "blur(10px)",
            "min_width": "100px",
            "border_left": f"4px solid {color_map.get(color, COLORS['blue']['500'])}",
            "transition": ANIMATIONS["easing"]["smooth"],
            "_hover": {
                "transform": "translateY(-2px)",
                "box_shadow": f"0 4px 12px {color_map.get(color, COLORS['blue']['500'])}20"
            }
        }
    )

def estadisticas_odontologo_superiores() -> rx.Component:
    """📊 Tarjetas de estadísticas superiores para odontólogo"""
    return rx.grid(
        # 1. Consultas del día
        stat_card_odontologo(
            "Hoy",
            AppState.estadisticas_odontologo_tiempo_real["pacientes_asignados"].to_string(),
            "blue"
        ),

        # 2. En espera
        stat_card_odontologo(
            "En Espera",
            AppState.estadisticas_odontologo_tiempo_real["consultas_en_espera"].to_string(),
            "yellow"
        ),

        # 3. Completadas hoy
        stat_card_odontologo(
            "Completadas",
            AppState.estadisticas_odontologo_tiempo_real["consultas_completadas"].to_string(),
            "green"
        ),

        # 4. Entre odontólogos (derivados)
        stat_card_odontologo(
            "Derivados",
            AppState.estadisticas_odontologo_tiempo_real["pacientes_disponibles"].to_string(),
            "primary"
        ),

        # 5. En progreso
        stat_card_odontologo(
            "En Progreso",
            AppState.estadisticas_odontologo_tiempo_real["consultas_en_atencion"].to_string(),
            "red"
        ),

        columns="6",
        spacing="3",
        width="100%"
    )

# ==========================================
# 🔍 COMPONENTES DE BÚSQUEDA Y FILTROS
# ==========================================

def barra_busqueda_y_filtros() -> rx.Component:
    """🔍 Barra de búsqueda médica optimizada para odontólogos"""
    return rx.vstack(
        # Primera fila: Búsqueda principal
        rx.hstack(
            # Campo de búsqueda expandido
            rx.input(
                placeholder="🔍 Buscar por nombre, documento, HC o diagnóstico...",
                value=AppState.termino_busqueda_pacientes,
                on_change=AppState.buscar_pacientes_asignados,
                style={
                    "background": DARK_THEME["colors"]["surface"],
                    "border": f"1px solid {DARK_THEME['colors']['border']}",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "border_radius": RADIUS["lg"],
                    "padding": "12px 16px",
                    "font_size": "14px",
                    "_focus": {
                        "border_color": COLORS["primary"]["500"],
                        "box_shadow": f"0 0 0 3px {COLORS['primary']['500']}30"
                    }
                },
                width=["100%", "100%", "50%"]
            ),
            
            rx.spacer(),
            
            # Botón de actualización mejorado
            rx.button(
                rx.hstack(
                    rx.cond(
                        AppState.cargando_pacientes_asignados,
                        rx.spinner(size="2", color="white"),
                        rx.icon("rotate-cw", size=16)
                    ),
                    rx.text("Actualizar", font_weight="600"),
                    spacing="2"
                ),
                style={
                    "background": f"linear-gradient(135deg, {COLORS['primary']['500']} 0%, {COLORS['primary']['400']} 100%)",
                    "color": "white",
                    "border": "none",
                    "border_radius": RADIUS["lg"],
                    "padding": "12px 20px",
                    "_hover": {
                        "transform": "translateY(-1px)",
                        "box_shadow": f"0 4px 12px {COLORS['primary']['500']}40"
                    },
                    "transition": ANIMATIONS["easing"]["smooth"] 
                },
                loading=AppState.cargando_pacientes_asignados,
                on_click=[
                    AppState.cargar_pacientes_asignados,
                    AppState.cargar_consultas_disponibles_otros,
                ]
            ),
            
            spacing="4",
            align_items="center",
            width="100%"
        ),
        
        # Segunda fila: Filtros médicos específicos
        rx.hstack(
            # Filtro por estado (Estados reales de BD)
            rx.select(
                ["Todos", "En Espera", "En Atención", "Entre Odontólogos", "Completada", "Cancelada"],
                value=AppState.filtro_estado_consulta,
                on_change=AppState.filtrar_por_estado_consulta,
                placeholder="📋 Estado",
                style={
                    "background": DARK_THEME["colors"]["surface"],
                    "border": f"1px solid {DARK_THEME['colors']['border']}",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "border_radius": RADIUS["md"]
                },
                width="160px"
            ),
            
            # Filtro urgencias mejorado
            rx.button(
                rx.hstack(
                    rx.icon("triangle-alert", size=16),
                    rx.text("Urgentes", font_weight="600"),
                    spacing="2"
                ),
                style=rx.cond(
                    AppState.mostrar_solo_urgencias,
                    {
                        "background": f"linear-gradient(135deg, {COLORS['error']['500']} 0%, {COLORS['error']['400']} 100%)",
                        "color": "white",
                        "border": "none",
                        "border_radius": RADIUS["md"],
                        "padding": "8px 12px",
                        "box_shadow": f"0 2px 8px {COLORS['error']['500']}40"
                    },
                    {
                        "background": "transparent",
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "border": f"1px solid {DARK_THEME['colors']['border']}",
                        "border_radius": RADIUS["md"],
                        "padding": "8px 12px",
                        "_hover": {
                            "background": DARK_THEME["colors"]["surface"],
                            "color": COLORS["error"]["400"]
                        }
                    }
                ),
                on_click=AppState.alternar_mostrar_urgencias
            ),
            
            # Filtro por tipo de consulta
            rx.select(
                ["Todas", "Primera Vez", "Control", "Emergencia", "Seguimiento"],
                placeholder="🦷 Tipo",
                style={
                    "background": DARK_THEME["colors"]["surface"],
                    "border": f"1px solid {DARK_THEME['colors']['border']}",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "border_radius": RADIUS["md"]
                },
                width="140px"
            ),
            
            rx.spacer(),
            
            # Indicador de resultados
            rx.text(
                f"📊 {AppState.estadisticas_odontologo_tiempo_real['pacientes_asignados'] } pacientes hoy",
                font_size="14px",
                color=DARK_THEME["colors"]["text_secondary"],
                font_weight="500"
            ),
            
            spacing="3",
            align_items="center",
            width="100%",
            wrap="wrap"
        ),
        
        spacing="3",
        width="100%"
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
    return medical_page_layout(
    rx.vstack(
        # Header profesional con tema oscuro
        rx.box(
            rx.vstack(
                rx.heading(
                    "🦷 Atención Odontológica",
                    style={
                        "font_size": "2.75rem",
                        "font_weight": "800",
                        "background": "linear-gradient(135deg, #00BCD4 0%, #4DD4FF 100%)",
                        "background_clip": "text",
                        "color": "transparent",
                        "line_height": "1.2"
                    }
                ),
                rx.text(
                    "Dashboard profesional - Sistema por orden de llegada",
                    style={
                        "font_size": "1.125rem",
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "line_height": "1.5"
                    }
                ),
                spacing="1",
                align="start",
                width="100%"
            ),
            style=dark_header_style(),
            width="100%"
        ),

        # Estadísticas superiores del odontólogo
        rx.box(
            estadisticas_odontologo_superiores(),
            style=dark_crystal_card(
                color=COLORS["primary"]["500"],
                hover_lift="2px",
                padding=SPACING["4"]
            ),
            width="100%"
        ),

        # Barra de búsqueda y filtros con tema oscuro
        rx.box(
            barra_busqueda_y_filtros(),
            style=dark_crystal_card(
                color=COLORS["primary"]["500"],
                hover_lift="2px",
                padding=SPACING["4"]
            ),
            width="100%"
        ),
        
        # ==========================================
        # 🎨 LAYOUT PRINCIPAL V2.0 - GRID RESPONSIVE
        # ==========================================
        rx.grid(
            # ==========================================
            # COLUMNA IZQUIERDA: MIS CONSULTAS COMPACTAS
            # ==========================================
            rx.box(
                rx.vstack(
                    # Header mejorado con estadísticas integradas
                    rx.vstack(
                        seccion_header(
                            titulo="🩺 Mi Cola de Atención",
                            cantidad=AppState.estadisticas_odontologo_tiempo_real["pacientes_asignados"],
                            icono="🦷",
                            color="blue"
                        ),

                        # Estadísticas mini como en página de consultas
                        estadisticas_cola_odontologo(),

                        spacing="3",
                        width="100%"
                    ),

                    # Lista compacta scrolleable con función V2
                    rx.box(
                        lista_consultas_compactas(),
                        style=medical_scrollable_content_v2()
                    ),

                    spacing="4",
                    height="100%"
                ),
                style=odontologia_column_card(COLORS["blue"]["500"])
            ),

            # ==========================================
            # COLUMNA DERECHA: DISPONIBLES
            # ==========================================
            rx.box(
                rx.vstack(
                    # Header de sección
                    seccion_header(
                        titulo="📋 Pacientes Disponibles",
                        cantidad=AppState.estadisticas_odontologo_tiempo_real["pacientes_disponibles"],
                        icono="🔄",
                        color="success"
                    ),

                    # Contenido scrolleable con función V2
                    rx.box(
                        lista_consultas_disponibles(),
                        style=medical_scrollable_content_v2()
                    ),

                    spacing="4",
                    height="100%"
                ),
                style=odontologia_column_card(COLORS["success"]["500"])
            ),

            # ✅ GRID CONFIG: Responsive y flexible
            columns="2",
            spacing="6",
            width="100%",
            style={
                "grid_template_columns": "1fr 1fr",  # 50/50 flexible
                "align_items": "start",
                # ✅ Responsive breakpoints
                "@media (max-width: 1280px)": {
                    "grid_template_columns": "1fr",  # 1 columna en pantallas pequeñas
                    "gap": SPACING["4"]
                }
            }
        ),
        
        # Footer con tema oscuro profesional
        rx.box(
            rx.hstack(
                rx.text(
                    AppState.resumen_actividad_dia,
                    font_size="14px",
                    color=DARK_THEME["colors"]["text_secondary"]
                ),
                
                rx.spacer(),
                
                # Accesos rápidos con tema oscuro
                rx.hstack(
                    rx.cond(
                        AppState.en_formulario_intervencion,
                        rx.button(
                            "← Volver a Intervención",
                            size="2",
                            style={
                                "background": COLORS["blue"]["500"],
                                "color": "white",
                                "border": "none",
                                "_hover": {
                                    "background": COLORS["blue"]["600"]
                                }
                            },
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
            style={
                "background": DARK_THEME["colors"]["surface"],
                "border_top": f"1px solid {DARK_THEME['colors']['border']}",
                "backdrop_filter": "blur(10px)",
                "padding": SPACING["4"]
            },
            width="100%"
        ),
        
        # CSS personalizado para animaciones
        rx.html(
            """
            <style>
                @keyframes pulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.05); opacity: 0.9; }
                }

                @keyframes slideInUp {
                    from { transform: translateY(20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }

                @keyframes glow {
                    0%, 100% { box-shadow: 0 0 5px rgba(0, 188, 212, 0.3); }
                    50% { box-shadow: 0 0 20px rgba(0, 188, 212, 0.6); }
                }

                .slide-in {
                    animation: slideInUp 0.3s ease-out;
                }

                .glow-effect:hover {
                    animation: glow 2s infinite;
                }
            </style>
            """
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
                        color=DARK_THEME["colors"]["text_secondary"]
                    ),
                    spacing="3",
                    align_items="center"
                ),
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                background="rgba(0, 0, 0, 0.8)",
                backdrop_filter="blur(8px)",
                z_index="999"
            )
        ),
        
        spacing="6",
        padding="6",
        width="100%",
        min_height="100vh",
        style=create_dark_style("page_background"),
        on_mount=[
                    AppState.cargar_pacientes_asignados,
                    AppState.cargar_consultas_disponibles_otros,
                ]
    )
    )