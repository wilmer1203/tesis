"""
🦷 COMPONENTE: HISTORIAL DE CAMBIOS POR DIENTE
==============================================

Sistema de tracking detallado de todos los cambios realizados en cada diente,
con timeline, comparaciones visuales y vinculación automática con intervenciones.

CARACTERÍSTICAS:
- Timeline cronológico de cambios por diente
- Comparaciones antes/después
- Vinculación automática con intervenciones
- Sistema de alertas y recordatorios
- Exportación de historial
- Filtros avanzados por tipo de cambio
"""

import reflex as rx
from typing import Dict, List, Optional
from datetime import datetime, date, timedelta
from dental_system.state.app_state import AppState
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING

# ==========================================
# 🎨 ESTILOS DEL HISTORIAL
# ==========================================

HISTORIAL_CONTAINER_STYLE = {
    "background": "white",
    "border_radius": RADIUS["lg"],
    "box_shadow": SHADOWS["sm"],
    "border": f"1px solid {COLORS['gray']['200']}",
    "padding": SPACING["4"],
    "height": "100%",
    "overflow": "hidden"
}

TIMELINE_CHANGE_STYLE = {
    "border_left": f"4px solid {COLORS['blue']['400']}",
    "padding_left": SPACING["3"],
    "margin_left": SPACING["2"],
    "margin_bottom": SPACING["3"],
    "position": "relative"
}

CHANGE_CARD_STYLE = {
    "background": COLORS['gray']['50'],
    "border": f"1px solid {COLORS['gray']['200']}",
    "border_radius": RADIUS["md"],
    "padding": SPACING["3"],
    "transition": "all 0.2s ease",
    "_hover": {
        "border_color": COLORS['blue']['400'],
        "box_shadow": SHADOWS["sm"]
    }
}

# ==========================================
# 📊 PANEL ESTADÍSTICAS DIENTE
# ==========================================

def panel_estadisticas_diente() -> rx.Component:
    """📊 Panel de estadísticas y métricas del diente"""
    return rx.vstack(
        rx.text("📊 Estadísticas del Diente", weight="bold", size="4", margin_bottom="3"),
        
        # Grid de estadísticas
        rx.grid(
            # Total cambios
            stat_card("Cambios Totales", "8", "trending_up", "green"),
            # Último cambio  
            stat_card("Último Cambio", "5 días", "clock", "blue"),
            # Intervenciones
            stat_card("Intervenciones", "3", "wrench", "orange"),
            # Estado actual
            stat_card("Estado", "Estable", "circle_check", "green"),
            
            columns="2",
            spacing="3",
            width="100%"
        ),
        
        # Gráfico de evolución (simplificado)
        rx.vstack(
            rx.text("📈 Evolución Temporal", weight="medium", size="3"),
            rx.box(
                rx.text("Gráfico de evolución del estado del diente", size="2", color="gray.500", text_align="center"),
                width="100%",
                height="100px",
                border=f"2px dashed {COLORS['gray']['300']}",
                border_radius=RADIUS["md"],
                display="flex",
                align_items="center",
                justify_content="center"
            ),
            align_items="start",
            width="100%",
            margin_top="3"
        ),
        
        spacing="3",
        width="100%"
    )

def stat_card(titulo: str, valor: str, icono: str, color: str) -> rx.Component:
    """📈 Card de estadística individual"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(icono, size=16, color=f"{color}.500"),
                rx.text(titulo, size="2", color="gray.600"),
                spacing="2",
                align_items="center"
            ),
            rx.text(valor, weight="bold", size="4", color=f"{color}.600"),
            spacing="1",
            align_items="center",
            width="100%"
        ),
        variant="ghost",
        size="2"
    )

# ==========================================
# 📋 TIMELINE DE CAMBIOS DETALLADO
# ==========================================

def timeline_cambios_diente() -> rx.Component:
    """📜 Timeline cronológico completo de cambios del diente"""
    return rx.vstack(
        # Header con filtros
        rx.hstack(
            rx.text("📜 Historial Detallado", weight="bold", size="4"),
            rx.spacer(),
            rx.hstack(
                # Filtro por tipo
                rx.select(
                    ["Todos", "Intervenciones", "Diagnósticos", "Tratamientos", "Seguimiento"],
                    value=AppState.filtro_historial_tipo,
                    on_change=AppState.filtrar_historial_por_tipo,
                    size="2"
                ),
                # Filtro por fecha
                rx.select(
                    ["Todo el tiempo", "Último mes", "Últimos 3 meses", "Último año"],
                    value=AppState.filtro_historial_tiempo,
                    on_change=AppState.filtrar_historial_por_tiempo,
                    size="2"
                ),
                rx.button(
                    rx.icon("download", size=16),
                    "Exportar",
                    size="2",
                    variant="outline",
                    on_click=AppState.exportar_historial_diente
                ),
                spacing="2"
            ),
            width="100%",
            align_items="center",
            margin_bottom="4"
        ),
        
        # Timeline de cambios
        rx.box(
            rx.vstack(
                # Cambios recientes
                cambio_timeline(
                    "15/08/2024",
                    "14:30",
                    "Obturación Completada",
                    "intervencion",
                    "Dr. García",
                    "Obturación con resina compuesta en superficie oclusal. Procedimiento exitoso sin complicaciones.",
                    {"antes": "Caries profunda", "despues": "Obturado", "materiales": "Resina compuesta A2"}
                ),
                
                cambio_timeline(
                    "10/08/2024", 
                    "10:15",
                    "Diagnóstico Actualizado",
                    "diagnostico",
                    "Dr. García",
                    "Se detecta progresión de caries. Requiere intervención inmediata.",
                    {"antes": "Caries superficial", "despues": "Caries profunda", "recomendacion": "Obturación urgente"}
                ),
                
                cambio_timeline(
                    "05/08/2024",
                    "09:00", 
                    "Primera Evaluación",
                    "evaluacion",
                    "Dr. García",
                    "Evaluación inicial del diente. Se detecta caries superficial en superficie oclusal.",
                    {"estado_inicial": "Caries superficial", "riesgo": "Medio", "seguimiento": "2 semanas"}
                ),
                
                cambio_timeline(
                    "01/07/2024",
                    "11:45",
                    "Limpieza Preventiva", 
                    "prevencion",
                    "Dr. García",
                    "Limpieza dental general. Aplicación de flúor preventivo.",
                    {"tratamiento": "Profilaxis", "fluoracion": "Aplicada", "estado": "Preventivo"}
                ),
                
                spacing="0",
                width="100%"
            ),
            width="100%",
            max_height="400px",
            overflow_y="auto",
            padding_right="2"
        ),
        
        spacing="3",
        width="100%"
    )

def cambio_timeline(
    fecha: str,
    hora: str, 
    titulo: str,
    tipo: str,
    doctor: str,
    descripcion: str,
    detalles: Dict[str, str]
) -> rx.Component:
    """📝 Item individual del timeline de cambios"""
    
    # Configuración por tipo de cambio
    config_tipos = {
        "intervencion": {"color": "green", "icon": "wrench", "bg": "green.50"},
        "diagnostico": {"color": "yellow", "icon": "search", "bg": "yellow.50"},
        "evaluacion": {"color": "blue", "icon": "eye", "bg": "blue.50"},
        "prevencion": {"color": "primary", "icon": "shield", "bg": "primary.50"},
        "seguimiento": {"color": "purple", "icon": "clock", "bg": "purple.50"}
    }
    
    config = config_tipos.get(tipo, config_tipos["evaluacion"])
    
    return rx.box(
        rx.card(
            rx.vstack(
                # Header del cambio
                rx.hstack(
                    rx.icon(config["icon"], size=18, color=f"{config['color']}.500"),
                    rx.vstack(
                        rx.text(titulo, weight="bold", size="3", color=f"{config['color']}.700"),
                        rx.hstack(
                            rx.text(f"{fecha} {hora}", size="1", color="gray.500"),
                            rx.text("•", size="1", color="gray.400"),
                            rx.text(doctor, size="1", color="gray.600"),
                            spacing="1",
                            align_items="center"
                        ),
                        align_items="start",
                        spacing="0"
                    ),
                    rx.spacer(),
                    rx.badge(tipo.title(), color=config["color"], size="1"),
                    spacing="3",
                    align_items="start",
                    width="100%"
                ),
                
                # Descripción
                rx.text(descripcion, size="2", color="gray.700", margin_y="2"),
                
                # Detalles técnicos (expandible)
                rx.cond(
                    len(detalles) > 0,
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.hstack(
                                rx.icon("info", size=14),
                                rx.text("Ver detalles técnicos", size="2", color=f"{config['color']}.600"),
                                spacing="1"
                            )
                        ),
                        rx.dialog.content(
                            rx.vstack(
                                *[
                                    rx.hstack(
                                        rx.text(f"{key.replace('_', ' ').title()}:", weight="medium", size="1"),
                                        rx.text(value, size="1", color="gray.700"),
                                        spacing="2",
                                        align_items="center"
                                    )
                                    for key, value in detalles.items()
                                ],
                                spacing="1",
                                align_items="start",
                                padding_top="2",
                                width="100%"
                            )
                        ),
                        width="100%"
                    ),
                    rx.box()
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.button(
                        rx.icon("external_link", size=14),
                        "Ver Completo",
                        size="1",
                        variant="outline",
                        on_click=lambda: AppState.ver_cambio_completo(f"{fecha}-{titulo}")
                    ),
                    rx.cond(
                        tipo == "intervencion",
                        rx.button(
                            rx.icon("image", size=14),
                            "Imágenes",
                            size="1",
                            variant="outline",
                            on_click=lambda: AppState.ver_imagenes_cambio(f"{fecha}-{titulo}")
                        ),
                        rx.box()
                    ),
                    spacing="2"
                ),
                
                spacing="2",
                align_items="start",
                width="100%"
            ),
            style={
                **CHANGE_CARD_STYLE,
                # "background": COLORS[config["color"].split(".")[0]]["50"]
                "background": config["color"].split(".")[0]
            }
        ),
        style={
            **TIMELINE_CHANGE_STYLE,
            # "border_left_color": COLORS[config["color"].split(".")[0]]["400"]
            "border_left_color": config["color"].split(".")[0]
        },
        width="100%"
    )

# ==========================================
# 🔔 PANEL ALERTAS Y RECORDATORIOS
# ==========================================

def panel_alertas_diente() -> rx.Component:
    """🔔 Panel de alertas, recordatorios y seguimiento"""
    return rx.vstack(
        rx.text("🔔 Alertas y Seguimiento", weight="bold", size="4", margin_bottom="3"),
        
        # Alertas activas
        rx.vstack(
            rx.text("⚠️ Alertas Activas", weight="medium", size="3", color="orange.600"),
            
            alerta_card(
                "Seguimiento Requerido",
                "Control post-obturación programado para el 25/08/2024",
                "warning",
                "25/08/2024"
            ),
            
            alerta_card(
                "Sensibilidad Reportada", 
                "Paciente reportó sensibilidad al frío - revisar en próxima cita",
                "info",
                "Pendiente"
            ),
            
            spacing="2",
            width="100%"
        ),
        
        rx.divider(),
        
        # Recordatorios programados
        rx.vstack(
            rx.text("📅 Recordatorios", weight="medium", size="3", color="blue.600"),
            
            recordatorio_card(
                "Control Rutinario",
                "Revisión general programada",
                "30/09/2024",
                "programado"
            ),
            
            recordatorio_card(
                "Radiografía de Control",
                "Control radiográfico post-tratamiento", 
                "15/11/2024",
                "programado"
            ),
            
            spacing="2",
            width="100%"
        ),
        
        # Botón agregar recordatorio
        rx.button(
            rx.icon("plus", size=16),
            "Agregar Recordatorio",
            color_scheme="blue",
            size="2",
            width="100%",
            on_click=AppState.abrir_formulario_recordatorio,
            margin_top="3"
        ),
        
        spacing="3",
        width="100%"
    )

def alerta_card(titulo: str, descripcion: str, tipo: str, fecha: str) -> rx.Component:
    """⚠️ Card de alerta individual"""
    colores = {
        "warning": "orange",
        "error": "red", 
        "info": "blue",
        "success": "green"
    }
    
    iconos = {
        "warning": "triangle_alert",
        "error": "circle_alert",
        "info": "info",
        "success": "circle_check"
    }
    
    return rx.card(
        rx.hstack(
            rx.icon(iconos[tipo], size=16, color=f"{colores[tipo]}.500"),
            rx.vstack(
                rx.text(titulo, weight="bold", size="2", color=f"{colores[tipo]}.700"),
                rx.text(descripcion, size="1", color="gray.600"),
                rx.text(f"Fecha: {fecha}", size="1", color="gray.500"),
                align_items="start",
                spacing="0"
            ),
            rx.spacer(),
            rx.button(
                rx.icon("x", size=12),
                size="1",
                variant="ghost",
                on_click=lambda: AppState.marcar_alerta_leida(titulo)
            ),
            spacing="3",
            align_items="start",
            width="100%"
        ),
        variant="ghost",
        size="1",
        width="100%"
    )

def recordatorio_card(titulo: str, descripcion: str, fecha: str, estado: str) -> rx.Component:
    """📅 Card de recordatorio individual"""
    return rx.card(
        rx.hstack(
            rx.icon("calendar", size=16, color="blue.500"),
            rx.vstack(
                rx.text(titulo, weight="bold", size="2"),
                rx.text(descripcion, size="1", color="gray.600"),
                rx.text(fecha, size="1", color="blue.600", weight="medium"),
                align_items="start",
                spacing="0"
            ),
            rx.spacer(),
            rx.badge(estado.title(), color_scheme="blue", size="1"),
            spacing="3",
            align_items="start",
            width="100%"
        ),
        variant="ghost",
        size="1",
        width="100%"
    )

# ==========================================
# 🦷 COMPONENTE PRINCIPAL HISTORIAL
# ==========================================

def historial_cambios_diente() -> rx.Component:
    """
    🦷 Sistema completo de historial de cambios del diente
    
    FUNCIONALIDADES:
    - Timeline cronológico detallado
    - Estadísticas y métricas
    - Sistema de alertas y recordatorios
    - Filtros avanzados
    - Exportación de historial
    """
    
    return rx.box(
        rx.vstack(
            # Header principal
            rx.hstack(
                rx.icon("history", size=24, color="blue.500"),
                rx.vstack(
                    rx.text(
                        f"Historial - Diente #{rx.cond(AppState.diente_seleccionado,AppState.diente_seleccionado,'N/A')}", 
                        weight="bold", 
                        size="4"
                    ),
                    rx.text(
                        f"{AppState.obtener_tipo_diente()} - {AppState.obtener_cuadrante_diente()}", 
                        size="2", 
                        color="gray.600"
                    ),
                    align_items="start",
                    spacing="0"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        rx.icon("refresh_cw", size=16),
                        "Refrescar",
                        size="2",
                        variant="outline",
                        on_click=AppState.refrescar_historial_diente
                    ),
                    rx.button(
                        rx.icon("plus", size=16),
                        "Agregar Entrada",
                        size="2",
                        color_scheme="blue",
                        on_click=AppState.abrir_formulario_entrada_historial
                    ),
                    spacing="2"
                ),
                spacing="3",
                align_items="center",
                width="100%",
                margin_bottom="4"
            ),
            
            # Layout principal en grid
            rx.grid(
                # Columna izquierda: Timeline y estadísticas
                rx.vstack(
                    panel_estadisticas_diente(),
                    timeline_cambios_diente(),
                    spacing="4",
                    width="100%",
                    height="100%"
                ),
                
                # Columna derecha: Alertas y recordatorios
                panel_alertas_diente(),
                
                columns="2",
                spacing="4",
                width="100%",
                height="100%"
            ),
            
            spacing="4",
            width="100%",
            height="100%"
        ),
        style=HISTORIAL_CONTAINER_STYLE,
        width="100%",
        height="100%"
    )