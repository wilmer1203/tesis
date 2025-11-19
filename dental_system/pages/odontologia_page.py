# 🦷 PÁGINA PRINCIPAL DE ODONTOLOGÍA - ATENCIÓN CLÍNICA REFACTORIZADA
# dental_system/pages/odontologia_page.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import  secondary_button,page_header,stat_card,medical_page_layout
from dental_system.components.odontologia.consulta_card import (
    lista_consultas_disponibles,
    lista_consultas_compactas,
    seccion_header
)
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING,ANIMATIONS,
    dark_crystal_card, dark_header_style,
    DARK_THEME,  create_dark_style
)

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
        "scroll_behavior": "smooth",
        "width": "100%",
        "align_items": "stretch",
        "height": "90%"
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

def estadisticas_odontologo() -> rx.Component:
    """📊 Tarjetas de estadísticas superiores para odontólogo"""
    return rx.grid(
        # 1. Consultas del día
        stat_card(
            title="Hoy",
            value=AppState.estadisticas_odontologo_tiempo_real["pacientes_asignados"].to_string(),
            icon="calendar-day",
            color=COLORS["primary"]["600"]
        ),

        # 2. En espera
        stat_card(
            title="En Espera",
            value=AppState.estadisticas_odontologo_tiempo_real["consultas_en_espera"].to_string(),
            icon="hourglass-split",
            color=COLORS["warning"]["500"]
        ),

        # 3. Completadas hoy
        stat_card(
            title="Completadas",
            value=AppState.estadisticas_odontologo_tiempo_real["consultas_completadas"].to_string(),
            icon="check-circle",
            color=COLORS["success"]["500"]
        ),

        # 4. Entre odontólogos (derivados)
        stat_card(
            title="Derivados",
            value=AppState.estadisticas_odontologo_tiempo_real["pacientes_disponibles"].to_string(),
            icon="users-switch",
            color=COLORS["primary"]["500"]
        ),

        # 5. En progreso
        stat_card(
            title="En Atención",
            value=AppState.estadisticas_odontologo_tiempo_real["consultas_en_atencion"].to_string(),
            icon="stethoscope",
            color=COLORS["blue"]["500"]
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="3", lg="5"),
        spacing="6",
        width="100%",
        margin_bottom="8"
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
        
        page_header(
            "Atención Odontológica",
            "Dashboard profesional - Sistema por orden de llegada",
        ),
        estadisticas_odontologo(),

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
                            titulo="Mi Cola de Atención",
                            cantidad=AppState.estadisticas_odontologo_tiempo_real["pacientes_asignados"],
                            icono="stethoscope",
                            color="blue"
                        ),
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
                        titulo="Pacientes Disponibles",
                        cantidad=AppState.estadisticas_odontologo_tiempo_real["pacientes_disponibles"],
                        icono="users-switch",
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