"""
🏥 PANEL DE INFORMACIÓN DEL PACIENTE - VERSIÓN MÉDICA PREMIUM
=============================================================

Panel lateral con glassmorphism médico profesional y efectos premium:
- ✨ Glassmorphism avanzado con efectos cristal multicapa
- 🎨 Gradientes médicos dinámicos por rol profesional
- 💎 Micro-interacciones premium y animaciones fluidas
- 🚨 Alertas médicas visuales con efectos de urgencia
- 📊 Estadísticas en tiempo real con indicadores premium
- 🔮 Bordes luminosos y efectos de partículas sutiles
- 📱 Responsive design adaptativo médico
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.models import PacienteModel
from dental_system.styles.themes import (
    COLORS, RADIUS, SPACING,DARK_THEME, GRADIENTS,
)

# ==========================================
# 🌙 ESTILOS CONSISTENTES CON CONSULTAS_PAGE_V41
# ==========================================

# Colores consistentes con la página de consultas
CONSULTAS_COLORS = {
    "background": "#0f1419",           # Fondo principal muy oscuro
    "surface": "#1a1f2e",             # Superficie de cards
    "surface_hover": "#252b3a",       # Surface al hover
    "border": "#2d3748",              # Bordes sutiles
    "border_hover": "#4a5568",        # Bordes en hover
    "text_primary": "#f7fafc",        # Texto principal
    "text_secondary": "#a0aec0",      # Texto secundario
    "text_muted": "#718096",          # Texto apagado
    "accent_blue": "#3182ce",         # Azul principal
    "accent_green": "#38a169",        # Verde éxito
    "accent_yellow": "#d69e2e",       # Amarillo advertencia
    "accent_red": "#e53e3e",          # Rojo error
    "glass_bg": "rgba(26, 31, 46, 0.8)",      # Efecto vidrio
    "glass_border": "rgba(255, 255, 255, 0.1)", # Borde vidrio
    "accent_cyan": "#1CBBBA",         # Turquesa médico
}

# Contenedor principal unificado (ESTILO CONSULTAS)
PANEL_CONTAINER_UNIFIED = {
    "background": CONSULTAS_COLORS["glass_bg"],
    "border": f"1px solid {CONSULTAS_COLORS['glass_border']}",
    "border_radius": RADIUS["2xl"],
    "padding": "0",  # Sin padding interno - se maneja por secciones
    "min_height": "500px",
    "backdrop_filter": "blur(20px)",
    "transition": "all 0.4s ease",
    "box_shadow": f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
    "overflow": "hidden",
    "_hover": {
        "transform": "translateY(-4px)",
        "box_shadow": f"0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15)",
        "border_color": CONSULTAS_COLORS["border_hover"]
    }
}

# Header unificado con gradiente médico
UNIFIED_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {CONSULTAS_COLORS['accent_cyan']} 0%, {CONSULTAS_COLORS['accent_blue']} 100%)",
    "color": "white",
    "padding": SPACING["4"],
    "border_radius": f"{RADIUS['2xl']} {RADIUS['2xl']} 0 0",
    "position": "relative",
    "_after": {
        "content": "''",
        "position": "absolute",
        "bottom": "0",
        "left": "0",
        "right": "0",
        "height": "1px",
        "background": f"linear-gradient(90deg, transparent 0%, {CONSULTAS_COLORS['glass_border']} 50%, transparent 100%)",
    }
}

# Sección interna sin borders separados
UNIFIED_SECTION_STYLE = {
    "padding": f"{SPACING['4']} {SPACING['5']}",
    "border_bottom": f"1px solid {CONSULTAS_COLORS['border']}",
    "transition": "all 0.3s ease",
    "_hover": {
        "background": "rgba(255, 255, 255, 0.02)"
    },
    "_last_child": {
        "border_bottom": "none"
    }
}



# ==========================================
# 🧩 COMPONENTES AUXILIARES MEJORADOS
# ==========================================

def avatar_paciente_unified(paciente: rx.Var[PacienteModel]) -> rx.Component:
    """👤 Avatar simplificado con colores consistentes"""
    return rx.box(
        rx.avatar(
            fallback=rx.cond(
                (paciente.primer_nombre != "") & (paciente.primer_apellido != ""),
                paciente.primer_nombre[0] + paciente.primer_apellido[0],
                "?"
            ),
            size="6", 
            radius="full",
            color_scheme="cyan",
            style={
                "border": f"2px solid {CONSULTAS_COLORS['accent_cyan']}",
                "box_shadow": f"0 4px 16px rgba(0,0,0,0.3)",
                "transition": "all 0.3s ease"
            }
        ),
        
        # Indicador de estado simple
        rx.box(
            style={
                "position": "absolute",
                "bottom": "2px",
                "right": "2px",
                "width": "12px",
                "height": "12px",
                "background": CONSULTAS_COLORS["accent_green"],
                "border": f"2px solid {CONSULTAS_COLORS['surface']}",
                "border_radius": "50%",
            }
        ),
        
        position="relative",
        style={
            "_hover": {
                "transform": "scale(1.05)",
                "transition": "all 0.3s ease"
            }
        }
    )

def badge_unified(texto: str, color_scheme: str = "cyan") -> rx.Component:
    """🏷️ Badge simplificado con colores consistentes"""
    return rx.box(
        rx.text(texto, weight="medium", size="2", color=CONSULTAS_COLORS["text_primary"]),
        style={
            "background": f"{CONSULTAS_COLORS['accent_cyan']}20",
            "border": f"1px solid {CONSULTAS_COLORS['accent_cyan']}40",
            "padding": f"{SPACING['1']} {SPACING['2']}",
            "border_radius": RADIUS["lg"],
            "backdrop_filter": "blur(5px)",
        }
    )

def info_item_unified(icono: str, titulo: str, valor: rx.Var) -> rx.Component:
    """📋 Item de información unificado sin bordes separados"""
    return rx.hstack(
        rx.icon(icono, size=16, color=CONSULTAS_COLORS["accent_cyan"]),
        rx.vstack(
            rx.text(
                titulo,
                size="2",
                weight="medium",
                color=CONSULTAS_COLORS["text_secondary"]
            ),
            rx.text(
                valor,
                size="3",
                weight="bold",
                color=CONSULTAS_COLORS["text_primary"]
            ),
            spacing="1",
            align_items="start"
        ),
        spacing="3",
        align_items="center",
        width="100%",
        style={
            "padding": f"{SPACING['2']} 0",
        }
    )

# ==========================================
# 📋 COMPONENTES PRINCIPALES MEJORADOS
# ==========================================

def unified_header() -> rx.Component:
    """🏥 Header unificado con estilo consistente"""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("user-check", size=18, color="white"),
                rx.text(
                    "Información del Paciente", 
                    size="4",
                    weight="bold",
                    color="white"
                ),
                spacing="3",
                align_items="center"
            ),
            
            rx.button(
                rx.cond(
                    AppState.panel_paciente_expandido,
                    rx.icon("chevron-up", size=16, color="white"),
                    rx.icon("chevron-down", size=16, color="white")
                ),
                variant="ghost",
                size="2",
                style={
                    "background": "rgba(255, 255, 255, 0.1)",
                    "border": "1px solid rgba(255, 255, 255, 0.2)",
                    "border_radius": RADIUS["lg"],
                    "_hover": {
                        "background": "rgba(255, 255, 255, 0.2)"
                    }
                },
                on_click=AppState.toggle_panel_paciente
            ),
            
            width="100%",
            justify="between",
            align_items="center"
        ),
        style=UNIFIED_HEADER_STYLE
    )

def seccion_principal_premium() -> rx.Component:
    """🏥 Sección principal premium con avatar y información médica"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Avatar premium médico
                avatar_paciente_unified(AppState.paciente_actual),
                
                # Información principal con efectos
                rx.vstack(
                    rx.cond(
                        AppState.paciente_actual.primer_nombre != "",
                        rx.text(
                            f"{AppState.paciente_actual.primer_nombre} {AppState.paciente_actual.primer_apellido}",
                            size="5",
                            weight="bold",
                            color=DARK_THEME["colors"]["text_primary"],
                            style={
                                "text_shadow": "0 2px 4px rgba(0,0,0,0.1)",
                                "background": GRADIENTS["text_gradient_primary"],
                                "background_clip": "text",
                                "color": "transparent"
                            }
                        ),
                        rx.cond(
                            AppState.paciente_actual.nombre_completo != "",
                            rx.text(
                                AppState.paciente_actual.nombre_completo,
                                size="5",
                                weight="bold",
                                color=DARK_THEME["colors"]["text_primary"]
                            ),
                            rx.text(
                                "⚠️ Paciente no cargado",
                                size="4",
                                weight="bold",
                                color=COLORS["error"]["400"]
                            )
                        )
                    ),
                    
                    # Badges informativos premium
                    rx.hstack(
                        badge_unified(f"HC: {AppState.paciente_actual.numero_historia}", "cyan"),
                        badge_unified(f"CI: {AppState.paciente_actual.numero_documento}", "cyan"),
                        spacing="2",
                        wrap="wrap"
                    ),
                    
                    # Información adicional
                    rx.hstack(
                        rx.cond(
                            AppState.paciente_actual.edad > 0,
                            rx.text(
                                AppState.paciente_actual.edad.to(str) + " años", 
                                size="3", 
                                color=DARK_THEME["colors"]["text_secondary"],
                                weight="medium"
                            ),
                            rx.text("Edad no especificada", size="3", color=DARK_THEME["colors"]["text_muted"])
                        ),
                        rx.text("•", color=DARK_THEME["colors"]["text_muted"]),
                        rx.cond(
                            AppState.paciente_actual.genero != "",
                            rx.text(AppState.paciente_actual.genero, size="3", color=DARK_THEME["colors"]["text_secondary"]),
                            rx.text("Sin género", size="3", color=DARK_THEME["colors"]["text_muted"])
                        ),
                        spacing="2",
                        align_items="center"
                    ),
                    
                    align_items="start",
                    spacing="3"
                ),
                
                spacing="5",
                align_items="center",
                width="100%"
            ),
            
            spacing="4",
            align_items="center",
            width="100%"
        ),
        
        style={
            **UNIFIED_SECTION_STYLE,
            "background": f"linear-gradient(135deg, {COLORS['primary']['500']}08 0%, {COLORS['success']['500']}05 100%)",
            "border": f"2px solid {COLORS['primary']['400']}40"
        }
    )


# ==========================================
# 📋 COMPONENTE PRINCIPAL MEJORADO
# ==========================================

def panel_informacion_paciente() -> rx.Component:
    """
    🏥 PANEL MÉDICO PREMIUM - INFORMACIÓN DEL PACIENTE 

    """
    return rx.box(
        # Efectos de fondo médico
        rx.box(
            style={
                "position": "absolute",
                "inset": "0",
                "background": f"""
                    radial-gradient(circle at 15% 15%, {COLORS['primary']['500']}06 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, {COLORS['success']['500']}04 0%, transparent 40%)
                """,
                "pointer_events": "none",
                "z_index": "1"
            }
        ),
        
        rx.vstack(
            # Header médico premium
            unified_header(),
            
            # Contenido colapsable premium
            rx.cond(
                AppState.panel_paciente_expandido,
                rx.box(
                    rx.vstack(
                        # Sección principal premium con avatar 
                        seccion_principal_premium(),
                        
                        # Alertas médicas críticas
                        rx.cond(
                            AppState.paciente_actual.alergias.length() > 0,
                            rx.box(
                                rx.hstack(
                                    rx.icon("triangle_alert", size=20, color=COLORS["error"]["300"]),
                                    rx.vstack(
                                        rx.text("🚨 ALERGIAS CRÍTICAS", weight="bold", size="3", color=COLORS["error"]["300"]),
                                        rx.flex(
                                            rx.foreach(
                                                AppState.paciente_actual.alergias,
                                                lambda alergia: badge_unified(alergia, "red")
                                            ),
                                            wrap="wrap",
                                            spacing="2"
                                        ),
                                        spacing="2",
                                        align_items="start"
                                    ),
                                    spacing="3",
                                    align_items="start"
                                ),
                                style={
                                    **UNIFIED_SECTION_STYLE,
                                    "margin_bottom": SPACING["5"]
                                }
                            )
                        ),
                        
                        # Información de contacto premium
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("phone", size=18, color=COLORS["info"]["500"]),
                                    rx.text("📞 Información de Contacto", weight="bold", size="4", color=DARK_THEME["colors"]["text_primary"]),
                                    spacing="3"
                                ),
                                info_item_unified("phone", "Teléfono Principal", AppState.paciente_actual.celular_1),
                                rx.cond(
                                    AppState.paciente_actual.celular_2 != "",
                                    info_item_unified("phone", "Teléfono Secundario", AppState.paciente_actual.celular_2)
                                ),
                                info_item_unified("mail", "Correo", rx.cond(AppState.paciente_actual.email, AppState.paciente_actual.email, "No registrado")),
                                spacing="3",
                                width="100%"
                            ),
                            style=UNIFIED_SECTION_STYLE
                        ),
                        
                        # Estadísticas médicas premium
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("activity", size=18, color=COLORS["primary"]["400"]),
                                    rx.text("📊 Estadísticas Médicas", weight="bold", size="4", color=DARK_THEME["colors"]["text_primary"]),
                                    spacing="3"
                                ),
                                rx.grid(
                                    rx.box(
                                        rx.text(AppState.total_visitas_paciente_actual.to(str), size="7", weight="bold", color=COLORS["primary"]["300"]),
                                        rx.text("Visitas", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                                        text_align="center"
                                    ),
                                    rx.box(
                                        rx.text("0", size="6", weight="bold", color=COLORS["warning"]["500"]),
                                        rx.text("Pendientes", size="2", color=DARK_THEME["colors"]["text_secondary"]),
                                        text_align="center"
                                    ),
                                    columns="2",
                                    spacing="4",
                                    width="100%"
                                ),
                                spacing="4",
                                width="100%"
                            ),
                            style={
                                **UNIFIED_SECTION_STYLE,
                                "cursor": "pointer"
                            }
                        ),
                        
                        # Consulta actual premium
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("clipboard-list", size=18, color=COLORS["success"]["400"]),
                                    rx.text("🏥 Consulta Actual", weight="bold", size="4", color=DARK_THEME["colors"]["text_primary"]),
                                    spacing="3"
                                ),
                                info_item_unified("hash", "N° Consulta", AppState.consulta_actual.numero_consulta),
                                info_item_unified("calendar", "Fecha", AppState.consulta_actual.fecha_llegada),
                                spacing="3",
                                width="100%"
                            ),
                            style=UNIFIED_SECTION_STYLE
                        ),
                        
                        spacing="5",
                        width="100%"
                    ),
                    style={
                        **UNIFIED_SECTION_STYLE,
                        "position": "relative",
                        "z_index": "2"
                    }
                ),
                # Panel colapsado premium
                rx.box(
                    rx.center(
                        rx.vstack(
                            avatar_paciente_unified(AppState.paciente_actual),
                            rx.text(
                                AppState.paciente_actual.nombre_completo,
                                weight="bold",
                                size="3",
                                text_align="center",
                                color=DARK_THEME["colors"]["text_primary"]
                            ),
                            rx.text(
                                f"HC: {AppState.paciente_actual.numero_historia}",
                                size="2",
                                color=DARK_THEME["colors"]["text_secondary"],
                                text_align="center"
                            ),
                            spacing="3",
                            align_items="center"
                        ),
                        padding="6"
                    ),
                    style={"position": "relative", "z_index": "2"}
                )
            ),
            
            spacing="0",
            height="100%",
            position="relative"
        ),
        
        style={
            **PANEL_CONTAINER_UNIFIED,
            "position": "relative"
        }
    )