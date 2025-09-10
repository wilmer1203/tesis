"""
🦷 COMPONENTE: PANEL DETALLES DIENTE CON TABS
==============================================

Panel lateral detallado para mostrar información específica de cada diente seleccionado.
Incluye tabs para diferentes aspectos: superficies, historial, tratamientos, notas.

CARACTERÍSTICAS:
- Tabs navegables (Superficies, Historial, Tratamientos, Notas)
- Información FDI completa del diente
- Estado visual por superficie dental
- Historial de cambios con timestamps
- Formularios de edición inline
- Integración completa con odontograma SVG
"""

import reflex as rx
from typing import Dict, List, Optional
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS DEL PANEL
# ==========================================

PANEL_DIENTE_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["md"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "height": "100%",
    "min_height": "600px",
    "display": "flex",
    "flex_direction": "column"
}

HEADER_DIENTE_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['primary']['500']}, {COLORS['primary']['600']})",
    "color": "white",
    "padding": SPACING["4"],
    "border_radius": f"{RADIUS['lg']} {RADIUS['lg']} 0 0",
    "text_align": "center"
}

TAB_CONTENT_STYLE = {
    "padding": SPACING["4"],
    "height": "100%",
    "overflow_y": "auto"
}

# ==========================================
# 🦷 INFORMACIÓN DEL DIENTE
# ==========================================

def info_basica_diente() -> rx.Component:
    """📋 Información básica del diente seleccionado"""
    return rx.cond(
        AppState.diente_seleccionado,
        rx.vstack(
            rx.heading(
                f"Diente #{AppState.diente_seleccionado}",
                size="5",
                color="white"
            ),
            rx.text(
                f"FDI: {AppState.diente_seleccionado}",
                size="3",
                opacity="0.9"
            ),
            rx.text(
                f"Cuadrante: {AppState.obtener_cuadrante_diente()}",
                size="2",
                opacity="0.8"
            ),
            rx.text(
                f"Tipo: {AppState.obtener_tipo_diente()}",
                size="2",
                opacity="0.8"
            ),
            spacing="1",
            align_items="center"
        ),
        rx.vstack(
            rx.icon("stethoscope", size=32, color="white"),
            rx.text("Selecciona un diente", color="white", opacity="0.8"),
            align_items="center",
            spacing="2"
        )
    )

# ==========================================
# 📑 TAB: SUPERFICIES DEL DIENTE
# ==========================================

def tab_superficies() -> rx.Component:
    """🎨 Tab de superficies dentales con estados visuales"""
    return rx.vstack(
        rx.text(
            "Superficies Dentales",
            weight="bold",
            size="4",
            margin_bottom="3"
        ),
        
        # Grid de superficies
        rx.grid(
            # Superficie Oclusal
            superficie_card("oclusal", "Oclusal", "🔝", "Superficie de masticación"),
            # Superficie Mesial
            superficie_card("mesial", "Mesial", "⬅️", "Superficie hacia línea media"),
            # Superficie Distal
            superficie_card("distal", "Distal", "➡️", "Superficie alejada de línea media"),
            # Superficie Vestibular
            superficie_card("vestibular", "Vestibular", "👄", "Superficie hacia mejillas"),
            # Superficie Lingual
            superficie_card("lingual", "Lingual", "👅", "Superficie hacia lengua"),
            
            columns="2",
            spacing="3",
            width="100%"
        ),
        
        # Botones de acción
        rx.hstack(
            rx.button(
                rx.icon("pen", size=16),
                "Editar Superficie",
                size="2",
                color_scheme="blue",
                disabled=~AppState.superficie_seleccionada,
                on_click=AppState.abrir_editor_superficie
            ),
            rx.button(
                rx.icon("history", size=16),
                "Ver Historial",
                size="2",
                variant="outline",
                on_click=AppState.mostrar_historial_superficie
            ),
            spacing="2",
            justify="center",
            margin_top="4"
        ),
        
        spacing="3",
        width="100%"
    )

def superficie_card(superficie: str, nombre: str, emoji: str, descripcion: str) -> rx.Component:
    """🎨 Card individual para cada superficie dental"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(emoji, size="6"),
                rx.vstack(
                    rx.text(nombre, weight="bold", size="3"),
                    rx.text(descripcion, size="1", color="gray.600"),
                    align_items="start",
                    spacing="0"
                ),
                spacing="2",
                align_items="center"
            ),
            
            # Estado actual de la superficie
            rx.hstack(
                rx.badge(
                    "Sano",  # Esto debe venir del estado
                    color_scheme="green",
                    size="1"
                ),
                rx.text("Sin tratamientos", size="1", color="gray.500"),
                spacing="2",
                justify="between",
                width="100%"
            ),
            
            spacing="2",
            width="100%"
        ),
        
        # Interactividad
        on_click=lambda: AppState.seleccionar_superficie(superficie),
        style={
            "cursor": "pointer",
            "border": f"2px solid {COLORS['gray']['200']}",
            "_hover": {
                "border_color": COLORS['primary']['400'],
                "transform": "translateY(-2px)",
                "box_shadow": SHADOWS["md"]
            },
            "transition": "all 0.2s ease"
        }
    )

# ==========================================
# 📑 TAB: HISTORIAL MÉDICO
# ==========================================

def tab_historial() -> rx.Component:
    """📜 Tab de historial médico del diente"""
    return rx.vstack(
        rx.hstack(
            rx.text("Historial Médico", weight="bold", size="4"),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=16),
                "Agregar Entrada",
                size="2",
                color_scheme="green",
                on_click=AppState.abrir_formulario_historial
            ),
            width="100%",
            align_items="center",
            margin_bottom="3"
        ),
        
        # Timeline de historial
        rx.vstack(
            entrada_historial(
                "15/08/2024",
                "Obturación",
                "Obturación con resina compuesta en superficie oclusal",
                "Dr. García",
                "success"
            ),
            entrada_historial(
                "10/06/2024",
                "Diagnóstico",
                "Caries profunda detectada, programar tratamiento",
                "Dr. García",
                "warning"
            ),
            entrada_historial(
                "05/03/2024",
                "Revisión",
                "Diente sano, sin cambios desde última visita",
                "Dr. García",
                "info"
            ),
            spacing="3",
            width="100%"
        ),
        
        spacing="3",
        width="100%"
    )

def entrada_historial(fecha: str, titulo: str, descripcion: str, doctor: str, tipo: str = "info") -> rx.Component:
    """📝 Entrada individual del historial"""
    color_schemes = {
        "success": "green",
        "warning": "yellow", 
        "info": "blue",
        "error": "red"
    }
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(titulo, color_scheme=color_schemes.get(tipo, "blue")),
                rx.spacer(),
                rx.text(fecha, size="1", color="gray.500"),
                width="100%",
                align_items="center"
            ),
            rx.text(descripcion, size="2"),
            rx.hstack(
                rx.icon("user", size=12),
                rx.text(doctor, size="1", color="gray.600"),
                spacing="1",
                align_items="center"
            ),
            spacing="2",
            align_items="start",
            width="100%"
        ),
        width="100%"
    )

# ==========================================
# 📑 TAB: TRATAMIENTOS
# ==========================================

def tab_tratamientos() -> rx.Component:
    """🏥 Tab de tratamientos planificados y realizados"""
    return rx.vstack(
        rx.hstack(
            rx.text("Tratamientos", weight="bold", size="4"),
            rx.spacer(),
            rx.button(
                rx.icon("calendar", size=16),
                "Nuevo Tratamiento",
                size="2",
                color_scheme="blue",
                on_click=AppState.abrir_planificador_tratamiento
            ),
            width="100%",
            align_items="center",
            margin_bottom="3"
        ),
        
        # Tratamientos activos
        rx.vstack(
            rx.text("🔄 En Curso", weight="medium", size="3", color="blue.600"),
            tratamiento_card(
                "Endodoncia",
                "Tratamiento de conducto en proceso",
                "2/3 sesiones",
                "in_progress",
                "Próxima cita: 20/08/2024"
            ),
            spacing="2",
            width="100%"
        ),
        
        rx.divider(),
        
        # Tratamientos completados
        rx.vstack(
            rx.text("✅ Completados", weight="medium", size="3", color="green.600"),
            tratamiento_card(
                "Limpieza Dental",
                "Profilaxis y fluorización",
                "Completado",
                "completed",
                "Realizado: 10/08/2024"
            ),
            tratamiento_card(
                "Obturación",
                "Resina compuesta oclusal",
                "Completado",
                "completed",
                "Realizado: 05/08/2024"
            ),
            spacing="2",
            width="100%"
        ),
        
        spacing="4",
        width="100%"
    )

def tratamiento_card(titulo: str, descripcion: str, estado: str, tipo: str, fecha: str) -> rx.Component:
    """🏥 Card de tratamiento individual"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(titulo, weight="bold", size="3"),
                rx.spacer(),
                rx.badge(
                    estado,
                    color_scheme="blue" if tipo == "in_progress" else "green"
                ),
                width="100%",
                align_items="center"
            ),
            rx.text(descripcion, size="2", color="gray.700"),
            rx.text(fecha, size="1", color="gray.500"),
            spacing="1",
            align_items="start",
            width="100%"
        )
    )

# ==========================================
# 📑 TAB: NOTAS CLÍNICAS
# ==========================================

def tab_notas() -> rx.Component:
    """📝 Tab de notas clínicas del odontólogo"""
    return rx.vstack(
        rx.hstack(
            rx.text("Notas Clínicas", weight="bold", size="4"),
            rx.spacer(),
            rx.button(
                rx.icon("save", size=16),
                "Guardar",
                size="2",
                color_scheme="green",
                on_click=AppState.guardar_notas_diente
            ),
            width="100%",
            align_items="center",
            margin_bottom="3"
        ),
        
        # Área de notas
        rx.vstack(
            rx.text_area(
                placeholder="Escribe las observaciones clínicas del diente...\n\nEjemplo:\n- Sensibilidad al frío\n- Desgaste en superficie oclusal\n- Cambio de coloración leve",
                value=AppState.notas_diente_actual,
                on_change=AppState.actualizar_notas_diente,
                rows="12",
                width="100%",
                resize="vertical"
            ),
            
            # Información de la nota
            rx.hstack(
                rx.text(
                    f"Última modificación: {AppState.fecha_ultima_nota}",
                    size="1",
                    color="gray.500"
                ),
                rx.spacer(),
                rx.text(
                    f"Por: {AppState.autor_ultima_nota}",
                    size="1",
                    color="gray.500"
                ),
                width="100%",
                align_items="center"
            ),
            
            spacing="2",
            width="100%"
        ),
        
        # Notas históricas rápidas
        rx.vstack(
            rx.text("📋 Notas Recientes", weight="medium", size="3", margin_top="4"),
            rx.vstack(
                nota_historica("12/08/2024", "Paciente reporta sensibilidad"),
                nota_historica("08/08/2024", "Revisión post-tratamiento OK"),
                nota_historica("01/08/2024", "Planificada obturación oclusal"),
                spacing="2"
            ),
            spacing="2",
            width="100%"
        ),
        
        spacing="3",
        width="100%"
    )

def nota_historica(fecha: str, texto: str) -> rx.Component:
    """📝 Nota histórica compacta"""
    return rx.card(
        rx.hstack(
            rx.text(fecha, size="1", color="gray.500", width="80px"),
            rx.text(texto, size="2", color="gray.700"),
            spacing="2",
            align_items="center",
            width="100%"
        ),
        size="1",
        width="100%"
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL
# ==========================================

def panel_detalles_diente() -> rx.Component:
    """
    🦷 Panel lateral completo con detalles del diente seleccionado
    
    CARACTERÍSTICAS:
    - Header con información básica FDI
    - Tabs navegables con contenido especializado
    - Integración completa con estado de odontología
    - Responsive y adaptable
    """
    
    return rx.box(
        rx.vstack(
            # Header con información del diente
            rx.box(
                info_basica_diente(),
                style=HEADER_DIENTE_STYLE
            ),
            
            # Tabs de contenido
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Superficies", value="superficies"),
                    rx.tabs.trigger("Historial", value="historial"),
                    rx.tabs.trigger("Tratamientos", value="tratamientos"),
                    rx.tabs.trigger("Notas", value="notas"),
                ),
                
                # Contenido de cada tab
                rx.tabs.content(
                    tab_superficies(),
                    value="superficies"
                ),
                rx.tabs.content(
                    tab_historial(),
                    value="historial"
                ),
                rx.tabs.content(
                    tab_tratamientos(),
                    value="tratamientos"
                ),
                rx.tabs.content(
                    tab_notas(),
                    value="notas"
                ),
                
                default_value="superficies",
                orientation="horizontal",
                width="100%",
                height="100%"
            ),
            
            spacing="0",
            height="100%",
            width="100%"
        ),
        style=PANEL_DIENTE_STYLE
    )