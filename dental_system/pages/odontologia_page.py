# 🦷 PÁGINA PRINCIPAL DE ODONTOLOGÍA - ATENCIÓN CLÍNICA
# dental_system/pages/odontologia_page.py

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import page_header, primary_button, secondary_button
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS ESPECÍFICOS PARA ODONTOLOGÍA
# ==========================================

CARD_STYLE = {
    "background": "white",
    "border_radius": RADIUS["xl"],
    "box_shadow": SHADOWS["md"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["6"],
    "width": "100%",
    "margin_bottom": SPACING["4"]
}

PACIENTE_CARD_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["sm"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["4"],
    "margin_bottom": SPACING["3"],
    "width": "100%",
    "_hover": {
        "box_shadow": SHADOWS["lg"],
        "border_color": COLORS["primary"]["300"]
    }
}

STATS_CARD_STYLE = {
    "background": COLORS["primary"]["50"],
    "border_radius": RADIUS["lg"],
    "padding": SPACING["4"],
    "text_align": "center",
    "border": f"1px solid {COLORS['primary']['200']}"
}

ASIGNADO_BADGE_STYLE = {
    "background": COLORS["blue"]["100"],
    "color": COLORS["blue"]["700"],
    "padding": f"{SPACING['1']} {SPACING['2']}",
    "border_radius": RADIUS["full"],
    "font_size": "12px",
    "font_weight": "medium"
}

DISPONIBLE_BADGE_STYLE = {
    "background": COLORS["success"]["100"],
    "color": COLORS["success"]["700"],
    "padding": f"{SPACING['1']} {SPACING['2']}",
    "border_radius": RADIUS["full"],
    "font_size": "12px",
    "font_weight": "medium"
}

# ==========================================
# 📊 COMPONENTE: ESTADÍSTICAS DEL ODONTÓLOGO
# ==========================================

def stats_cards() -> rx.Component:
    """📊 Tarjetas con estadísticas del día del odontólogo"""
    return rx.hstack(
        # Pacientes Asignados
        rx.box(
            rx.vstack(
                rx.text(
                    AppState.pacientes_asignados_count,
                    size="6",
                    weight="bold",
                    color=COLORS["blue"]["600"]
                ),
                rx.text(
                    "Pacientes Asignados",
                    size="2",
                    color=COLORS["gray"]["600"]
                ),
                spacing="1",
                align_items="center"
            ),
            style=STATS_CARD_STYLE
        ),
        
        # Pacientes Disponibles
        rx.box(
            rx.vstack(
                rx.text(
                    AppState.pacientes_disponibles_odontologia_count,
                    size="6",
                    weight="bold",
                    color=COLORS["success"]["600"]
                ),
                rx.text(
                    "Disponibles",
                    size="2",
                    color=COLORS["gray"]["600"]
                ),
                spacing="1",
                align_items="center"
            ),
            style=STATS_CARD_STYLE
        ),
        
        # Intervenciones Completadas
        rx.box(
            rx.vstack(
                rx.text(
                    AppState.intervenciones_hoy_count,
                    size="6",
                    weight="bold",
                    color=COLORS["primary"]["600"]
                ),
                rx.text(
                    "Completadas Hoy",
                    size="2",
                    color=COLORS["gray"]["600"]
                ),
                spacing="1",
                align_items="center"
            ),
            style=STATS_CARD_STYLE
        ),
        
        # Tiempo Promedio
        rx.box(
            rx.vstack(
                rx.text(
                    "25 min",  # Placeholder - implementar computed variable después
                    size="6",
                    weight="bold",
                    color=COLORS["success"]["600"]
                ),
                rx.text(
                    "Tiempo Promedio",
                    size="2",
                    color=COLORS["gray"]["600"]
                ),
                spacing="1",
                align_items="center"
            ),
            style=STATS_CARD_STYLE
        ),
        
        spacing="4",
        width="100%"
    )

# ==========================================
# 👥 COMPONENTE: TARJETA DE PACIENTE
# ==========================================

def paciente_card(paciente) -> rx.Component:
    """👤 Tarjeta individual de paciente con información y acciones - USANDO MODELOS TIPADOS"""
    return rx.box(
        rx.vstack(
            # Header con nombre y badge
            rx.hstack(
                rx.vstack(
                    rx.text(
                        paciente.nombre_completo,
                        size="4",
                        weight="bold",
                        color=COLORS["gray"]["800"]
                    ),
                    rx.text(
                        f"HC: {paciente.numero_historia} | Cédula: {paciente.numero_documento}",
                        size="2",
                        color=COLORS["gray"]["600"]
                    ),
                    spacing="1",
                    align_items="start"
                ),
                
                rx.spacer(),
                
                # Badge de estado - usando lista de asignados vs disponibles
                rx.box(
                    "Asignado",
                    style=ASIGNADO_BADGE_STYLE
                ),
                
                spacing="3",
                align_items="start",
                width="100%"
            ),
            
            # Información médica importante
            rx.cond(
                (paciente.alergias.length() > 0) | (paciente.condiciones_medicas.length() > 0),
                rx.vstack(
                    rx.cond(
                        paciente.alergias.length() > 0,
                        rx.hstack(
                            rx.box(
                                "⚠️",
                                color=COLORS["error"]["500"],
                                font_size="16px"
                            ),
                            rx.text(
                                f"Alergias: {paciente.alergias_display}",
                                size="2",
                                color=COLORS["error"]["600"],
                                weight="medium"
                            ),
                            spacing="2"
                        )
                    ),
                    rx.cond(
                        paciente.condiciones_medicas.length() > 0,
                        rx.hstack(
                            rx.box(
                                "🏥",
                                color=COLORS["warning"]["500"],
                                font_size="16px"
                            ),
                            rx.text(
                                f"Condiciones: {paciente.condiciones_display}",
                                size="2",
                                color=COLORS["warning"]["600"],
                                weight="medium"
                            ),
                            spacing="2"
                        )
                    ),
                    spacing="2",
                    width="100%"
                )
            ),
            
            # Información de contacto adicional
            rx.text(
                f"Teléfono: {paciente.telefono_display}",
                size="2",
                color=COLORS["gray"]["600"]
            ),
            
            # Botones de acción
            rx.hstack(
                # Información del paciente
                secondary_button(
                    text="Ver Historial",
                    icon="user",
                    on_click=lambda: AppState.ver_historial_paciente(paciente.id)
                ),
                
                rx.spacer(),
                
                # Botón principal - iniciar intervención
                primary_button(
                    text="Iniciar Intervención",
                    icon="play-circle",
                    on_click=lambda p=paciente: AppState.iniciar_intervencion_paciente(p),
                    loading=AppState.is_loading_intervencion
                ),
                spacing="3",
                align_items="center",
                width="100%"
            ),
            spacing="4",
            width="100%"
                
        ),
        style=PACIENTE_CARD_STYLE,
            
    )
    #     
    # )

# ==========================================
# 📋 COMPONENTE: LISTA DE PACIENTES
# ==========================================

def lista_pacientes(titulo: str, pacientes: rx.Var, empty_message: str) -> rx.Component:
    """📋 Lista de pacientes con título y mensaje de estado vacío"""
    return rx.box(
        rx.vstack(
            # Título de la sección
            rx.hstack(
                rx.text(
                    titulo,
                    size="5",
                    weight="bold",
                    color=COLORS["gray"]["800"]
                ),
                rx.spacer(),
                rx.text(
                    f"{pacientes.length()} pacientes",
                    size="3",
                    color=COLORS["gray"]["600"],
                    weight="medium"
                ),
                spacing="3",
                align_items="center",
                width="100%"
            ),
            
            rx.divider(margin_y="4"),
            
            # Lista de pacientes o mensaje vacío
            rx.cond(
                pacientes.length() > 0,
                rx.vstack(
                    rx.foreach(
                        pacientes,
                        paciente_card
                    ),
                    spacing="3",
                    width="100%"
                ),
                # Mensaje cuando no hay pacientes
                rx.box(
                    rx.vstack(
                        rx.text(
                            "📋",
                            font_size="48px",
                            color=COLORS["gray"]["400"]
                        ),
                        rx.text(
                            empty_message,
                            size="3",
                            color=COLORS["gray"]["500"],
                            text_align="center"
                        ),
                        spacing="3",
                        align_items="center",
                        padding="8"
                    ),
                    width="100%"
                )
            ),
            
            spacing="4",
            width="100%"
        ),
        style=CARD_STYLE
    )

# ==========================================
# 🔄 COMPONENTE: CONTROLES DE ACTUALIZACIÓN
# ==========================================

def controles_actualizacion() -> rx.Component:
    """🔄 Controles para actualizar datos y acciones rápidas"""
    return rx.hstack(
        # Información de última actualización
        rx.text(
            "Datos de odontología - Sistema actualizado",
            size="2",
            color=COLORS["gray"]["600"]
        ),
        
        rx.spacer(),
        
        # Botones de control
        secondary_button(
            text="Actualizar Datos",
            icon="refresh-cw",
            on_click=AppState.load_pacientes_asignados_odontologo,
            loading=AppState.is_loading_pacientes_asignados
        ),
        
        spacing="4",
        align_items="center",
        width="100%",
        padding_bottom="4"
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL
# ==========================================

def odontologia_page() -> rx.Component:
    """
    🦷 Página principal de odontología
    
    Funcionalidades:
    - Dashboard con estadísticas del día
    - Lista de pacientes asignados directamente
    - Lista de pacientes disponibles (de otros odontólogos)
    - Acciones para iniciar/continuar intervenciones
    """
    return rx.vstack(
        # Header de la página
        page_header(
            "🦷 Atención Odontológica", 
            "Panel de trabajo odontológico - Atención especializada"
        ),
        
        # Estadísticas del día
        stats_cards(),
        
        # Controles de actualización
        controles_actualizacion(),
        
        # Layout de dos columnas
        rx.hstack(
            # Columna izquierda: Pacientes Asignados
            rx.box(
                lista_pacientes(
                    titulo="👥 Pacientes Asignados",
                    pacientes=AppState.pacientes_asignados,
                    empty_message="No tienes pacientes asignados en este momento"
                ),
                width="50%"
            ),
            
            # Columna derecha: Pacientes Disponibles
            rx.box(
                lista_pacientes(
                    titulo="🔄 Pacientes Disponibles",
                    pacientes=AppState.pacientes_disponibles_odontologia,
                    empty_message="No hay pacientes disponibles para nueva intervención"
                ),
                width="50%"
            ),
            
            spacing="6",
            width="100%",
            align_items="start"
        ),
        
        # Loading state
        rx.cond(
            AppState.is_loading_pacientes_asignados,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color="primary"),
                    rx.text(
                        "Cargando datos de odontología...",
                        size="3",
                        color=COLORS["gray"]["600"]
                    ),
                    spacing="3",
                    align_items="center"
                ),
                padding="8"
            )
        ),
        
        spacing="6",
        padding="6",
        width="100%",
        min_height="100vh"
    )