"""
📅 PÁGINA DE CONSULTAS - ESQUEMA v4.1 CONSOLIDADA
================================================

🎯 CARACTERÍSTICAS PRINCIPALES:
✅ Compatible con esquema BD v4.1
✅ Sistema de colas por orden de llegada (NO citas)
✅ Múltiples odontólogos por consulta
✅ Estados: en_espera → en_atencion → completada
✅ Dashboard de colas en tiempo real
✅ Tema oscuro profesional con glassmorphism
✅ Responsive design (Desktop + Mobile)
✅ Formularios tipados con ConsultaFormModel

🔄 CONSOLIDACIÓN:
- Integra lo mejor de consultas_page.py
- Actualizado para esquema v4.1 
- EstadoConsultas refactorizado a modelos tipados
- Dashboard de colas en tiempo real
"""

import reflex as rx
from typing import Dict, Any, List
from dental_system.state.app_state import AppState
from dental_system.models.consultas_models import ConsultaModel, ConsultaFormModel
from dental_system.models.personal_models import PersonalModel

# 🌙 TEMA OSCURO PROFESIONAL v4.1
DARK_THEME = {
    "bg_primary": "#0f1419",           # Fondo principal 
    "bg_secondary": "#1a1f2e",         # Superficie de cards
    "bg_hover": "#252b3a",             # Surface al hover
    "border": "#2d3748",               # Bordes sutiles
    "border_hover": "#4a5568",         # Bordes en hover
    "text_primary": "#f7fafc",         # Texto principal
    "text_secondary": "#a0aec0",       # Texto secundario
    "text_muted": "#718096",           # Texto apagado
    "accent_blue": "#3182ce",          # Azul principal
    "accent_green": "#38a169",         # Verde éxito
    "accent_yellow": "#d69e2e",        # Amarillo advertencia
    "accent_red": "#e53e3e",           # Rojo error
    "glass_bg": "rgba(26, 31, 46, 0.8)",
    "glass_border": "rgba(255, 255, 255, 0.1)",
}

# 📊 ESTADOS v4.1 CON COLORES
ESTADOS_V41 = {
    "en_espera": {
        "color": DARK_THEME["accent_yellow"],
        "bg": "rgba(214, 158, 46, 0.15)",
        "icon": "clock",
        "label": "En Espera"
    },
    "en_atencion": {
        "color": DARK_THEME["accent_blue"],
        "bg": "rgba(49, 130, 206, 0.15)", 
        "icon": "stethoscope",
        "label": "En Atención"
    },
    "entre_odontologos": {
        "color": DARK_THEME["accent_yellow"],
        "bg": "rgba(214, 158, 46, 0.15)",
        "icon": "arrow-right",
        "label": "Cambio Dr."
    },
    "completada": {
        "color": DARK_THEME["accent_green"],
        "bg": "rgba(56, 161, 105, 0.15)",
        "icon": "check-circle",
        "label": "Completada"
    },
    "cancelada": {
        "color": DARK_THEME["accent_red"],
        "bg": "rgba(229, 62, 62, 0.15)",
        "icon": "x-circle", 
        "label": "Cancelada"
    }
}

def boton_nueva_consulta_v41() -> rx.Component:
    """🚀 Botón flotante para nueva consulta - v4.1"""
    return rx.button(
        rx.hstack(
            rx.icon("calendar-plus", size=20, color=DARK_THEME["text_primary"]),
            rx.text("Nueva Consulta", font_weight="600", color=DARK_THEME["text_primary"]),
            spacing="2",
            align="center"
        ),
        style={
            "background": f"linear-gradient(135deg, {DARK_THEME['accent_blue']} 0%, #2b6cb8 100%)",
            "color": DARK_THEME["text_primary"],
            "border": f"1px solid {DARK_THEME['glass_border']}",
            "border_radius": "16px",
            "padding": "1rem 2rem",
            "position": "fixed",
            "top": "2rem",
            "right": "2rem", 
            "z_index": "1000",
            "backdrop_filter": "blur(10px)",
            "box_shadow": f"0 8px 32px rgba(49, 130, 206, 0.3)",
            "transition": "all 0.3s ease",
            "_hover": {
                "transform": "translateY(-3px)",
                "box_shadow": f"0 12px 40px rgba(49, 130, 206, 0.4)"
            }
        },
        on_click=lambda: AppState.abrir_modal_consulta("crear")
    )

def consulta_mini_card_v41(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """🏥 Mini card de consulta para mostrar en cola de odontólogo"""
    return rx.box(
        rx.hstack(
            # Indicador de posición y estado
            rx.box(
                rx.text(
                    consulta.orden_cola_odontologo or consulta.orden_llegada_general or "?",
                    font_weight="700",
                    color=DARK_THEME["text_primary"],
                    font_size="0.9rem"
                ),
                style={
                    "background": ESTADOS_V41.get("en_espera", {}).get("bg", DARK_THEME["bg_hover"]),
                    "border": f"1px solid {ESTADOS_V41.get(consulta.estado, {}).get('color', DARK_THEME['border'])}",
                    "border_radius": "8px",
                    "padding": "0.5rem",
                    "min_width": "2rem",
                    "text_align": "center"
                }
            ),
            
            # Información del paciente
            rx.vstack(
                rx.text(
                    consulta.paciente_nombre or "Paciente",
                    font_weight="600",
                    color=DARK_THEME["text_primary"],
                    font_size="0.9rem",
                    max_width="150px",
                    overflow="hidden",
                    white_space="nowrap",
                    text_overflow="ellipsis"
                ),
                rx.text(
                    consulta.motivo_consulta or "Sin motivo especificado",
                    color=DARK_THEME["text_secondary"],
                    font_size="0.8rem",
                    max_width="150px",
                    overflow="hidden",
                    white_space="nowrap", 
                    text_overflow="ellipsis"
                ),
                spacing="0.5",
                align="start",
                flex="1"
            ),
            
            # Botones de acción
            rx.hstack(
                # Botón iniciar/finalizar según estado
                rx.cond(
                    consulta.estado == "en_espera",
                    rx.button(
                        rx.icon("play", size=14),
                        size="1",
                        variant="soft",
                        color_scheme="blue",
                        on_click=lambda consulta_id=consulta.id: AppState.iniciar_atencion_consulta(consulta_id)
                    ),
                    rx.cond(
                        consulta.estado == "en_atencion",
                        rx.hstack(
                            rx.button(
                                rx.icon("stethoscope", size=12),
                                size="1",
                                variant="soft", 
                                color_scheme="purple",
                                on_click=AppState.navegar_a_odontologia_consulta(consulta.id)
                            ),
                            rx.button(
                                rx.icon("check", size=14),
                                size="1",
                                variant="soft", 
                                color_scheme="green",
                                on_click=AppState.finalizar_atencion_consulta(consulta.id)
                            ),
                            spacing="1"
                        ),
                        rx.cond(
                            consulta.estado == "completada",
                            rx.button(
                                rx.icon("credit-card", size=12),
                                size="1",
                                variant="soft", 
                                color_scheme="green",
                                on_click=AppState.navegar_a_pagos_consulta(consulta.id)
                            ),
                            rx.fragment()  # Empty component for other states
                        )
                    )
                ),
                
                # Botón menú de opciones
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.icon("more-horizontal", size=14),
                            size="1",
                            variant="ghost"
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Editar",
                            on_click=AppState.abrir_modal_editar_consulta(consulta.id)
                        ),
                        rx.menu.item(
                            "Cambiar Odontólogo",
                            on_click=AppState.abrir_modal_cambio_odontologo(consulta.id)
                        ),
                        rx.menu.separator(),
                        
                        # Links a otros módulos (solo si la consulta está en atención o completada)
                        rx.cond(
                            consulta.estado == "en_atencion",
                            rx.menu.item(
                                "🦷 Ir a Odontología",
                                on_click=AppState.navegar_a_odontologia_consulta(consulta.id)
                            ),
                            rx.fragment()  # Empty component when condition is false
                        ),
                        
                        rx.cond(
                            consulta.estado == "completada",
                            rx.menu.item(
                                "💳 Procesar Pago",
                                on_click=AppState.navegar_a_pagos_consulta(consulta.id)
                            ),
                            rx.fragment()  # Empty component when condition is false
                        ),
                        
                        rx.menu.separator(),
                        rx.menu.item(
                            "Cancelar",
                            color="red",
                            on_click=AppState.preparar_cancelacion_consulta(consulta.id)
                        )
                    )
                ),
                spacing="1"
            ),
            
            spacing="2",
            align="center",
            width="100%"
        ),
        
        style={
            "background": DARK_THEME["bg_hover"],
            "border": f"1px solid {DARK_THEME['border']}",
            "border_radius": "8px",
            "padding": "0.75rem",
            "transition": "all 0.2s ease",
            "_hover": {
                "border_color": ESTADOS_V41.get(consulta.estado, {}).get("color", DARK_THEME["border_hover"]),
                "background": DARK_THEME["bg_secondary"]
            }
        }
    )

def badge_estado_v41(estado: str) -> rx.Component:
    """🏷️ Badge de estado según esquema v4.1"""
    estado_info = ESTADOS_V41.get(estado, ESTADOS_V41["en_espera"])
    
    return rx.badge(
        rx.hstack(
            rx.icon(estado_info["icon"], size=12),
            rx.text(estado_info["label"], font_size="0.75rem", font_weight="600"),
            spacing="1",
            align="center"
        ),
        style={
            "background": estado_info["bg"],
            "color": estado_info["color"],
            "border": f"1px solid {estado_info['color']}",
            "border_radius": "8px",
            "padding": "4px 8px"
        }
    )

def consulta_item_v41(consulta: rx.Var[ConsultaModel]) -> rx.Component:
    """📋 Item de consulta individual - esquema v4.1"""
    return rx.box(
        rx.vstack(
            # Paciente y posición en cola
            rx.hstack(
                rx.box(
                    rx.text(
                        consulta.orden_cola_odontologo,
                        font_weight="700",
                        font_size="1.2rem",
                        color=DARK_THEME["accent_blue"]
                    ),
                    style={
                        "background": f"rgba(49, 130, 206, 0.2)",
                        "border_radius": "50%",
                        "width": "32px",
                        "height": "32px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                rx.vstack(
                    rx.text(
                        consulta.paciente_nombre,
                        font_weight="600",
                        color=DARK_THEME["text_primary"],
                        size="3"
                    ),
                    rx.text(
                        consulta.motivo_consulta,
                        color=DARK_THEME["text_secondary"],
                        size="2"
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.spacer(),
                badge_estado_v41(consulta.estado),
                spacing="3",
                align="center",
                width="100%"
            ),
            
            # Tiempo estimado y prioridad
            rx.hstack(
                rx.text(
                    consulta.tiempo_espera_estimado,
                    color=DARK_THEME["text_muted"],
                    font_size="0.85rem"
                ),
                rx.cond(
                    consulta.es_urgente,
                    rx.badge(
                        "URGENTE",
                        color=DARK_THEME["accent_red"],
                        style={
                            "background": "rgba(229, 62, 62, 0.15)",
                            "border": f"1px solid {DARK_THEME['accent_red']}"
                        }
                    ),
                    rx.fragment()  # Empty component when not urgent
                ),
                spacing="2",
                justify="between",
                width="100%"
            ),
            
            spacing="3",
            width="100%",
            align="start"
        ),
        style={
            "background": DARK_THEME["bg_secondary"],
            "border": f"1px solid {DARK_THEME['border']}",
            "border_radius": "12px",
            "padding": "1rem",
            "margin": "0.5rem 0",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": DARK_THEME["bg_hover"],
                "border_color": DARK_THEME["border_hover"],
                "transform": "translateY(-1px)"
            }
        }
    )

def doctor_card_v41(doctor: rx.Var[PersonalModel]) -> rx.Component:
    """👨‍⚕️ Card de odontólogo con cola - esquema v4.1"""
    return rx.box(
        rx.vstack(
            # Header del odontólogo
            rx.hstack(
                rx.box(
                    rx.icon("user-round", size=24, color=DARK_THEME["text_primary"]),
                    style={
                        "background": f"linear-gradient(135deg, {DARK_THEME['accent_green']} 0%, #48bb78 100%)",
                        "border_radius": "50%",
                        "padding": "12px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                rx.vstack(
                    rx.text(
                        doctor.nombre_completo_display,
                        font_weight="700",
                        size="4",
                        color=DARK_THEME["text_primary"]
                    ),
                    rx.text(
                        doctor.especialidad,
                        color=DARK_THEME["text_secondary"],
                        size="2"
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.spacer(),
                rx.badge(
                    rx.text(
                        AppState.get_total_consultas_por_odontologo(doctor.id),
                        font_weight="700"
                    ),
                    color=DARK_THEME["accent_blue"],
                    style={"background": "rgba(49, 130, 206, 0.2)"}
                ),
                spacing="3",
                align="center",
                width="100%"
            ),
            
            rx.divider(color=DARK_THEME["border"], margin="1rem 0"),
            
            # Cola de consultas
            rx.vstack(
                rx.hstack(
                    rx.icon("users", size=16, color=DARK_THEME["accent_blue"]),
                    rx.text(
                        "Cola de Atención",
                        font_weight="600",
                        color=DARK_THEME["text_primary"],
                        size="3"
                    ),
                    spacing="2",
                    align="center"
                ),
                
                # Lista de consultas pendientes y en atención
                rx.cond(
                    AppState.get_total_consultas_por_odontologo(doctor.id) > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.get_consultas_por_odontologo(doctor.id),
                            consulta_mini_card_v41
                        ),
                        width="100%",
                        spacing="2",
                        max_height="300px",
                        overflow_y="auto"
                    ),
                    rx.box(
                        rx.text(
                            "Sin consultas pendientes",
                            color=DARK_THEME["text_muted"],
                            font_style="italic",
                            text_align="center"
                        ),
                        padding="2rem",
                        width="100%"
                    )
                ),
                
                spacing="3",
                width="100%",
                align="start"
            ),
            
            spacing="0",
            width="100%",
            align="start"
        ),
        style={
            "background": DARK_THEME["glass_bg"],
            "border": f"1px solid {DARK_THEME['glass_border']}",
            "border_radius": "16px",
            "padding": "1.5rem",
            "backdrop_filter": "blur(10px)",
            "transition": "all 0.3s ease",
            "_hover": {
                "transform": "translateY(-2px)",
                "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.3)"
            }
        }
    )

def sidebar_resumen_v41() -> rx.Component:
    """📊 Sidebar con resumen del día - esquema v4.1"""
    return rx.box(
        rx.vstack(
            # Header del resumen
            rx.hstack(
                rx.icon("calendar", size=20, color=DARK_THEME["accent_blue"]),
                rx.text(
                    "Resumen del Día",
                    font_weight="700",
                    size="4",
                    color=DARK_THEME["text_primary"]
                ),
                spacing="2",
                align="center"
            ),
            
            rx.divider(color=DARK_THEME["border"], margin="1rem 0"),
            
            # Métricas principales
            rx.vstack(
                # Total de consultas
                metric_card_v41(
                    "Total Consultas",
                    AppState.get_total_consultas_hoy,
                    "calendar",
                    DARK_THEME["accent_blue"]
                ),
                
                # En espera
                metric_card_v41(
                    "En Espera", 
                    AppState.get_consultas_en_espera_hoy,
                    "clock",
                    DARK_THEME["accent_yellow"]
                ),
                
                # En atención
                metric_card_v41(
                    "En Atención",
                    AppState.get_consultas_en_atencion_hoy,
                    "stethoscope", 
                    DARK_THEME["accent_blue"]
                ),
                
                # Completadas
                metric_card_v41(
                    "Completadas",
                    AppState.get_consultas_completadas_hoy,
                    "check-circle",
                    DARK_THEME["accent_green"]
                ),
                
                spacing="3",
                width="100%"
            ),
            
            spacing="4",
            width="100%",
            align="start"
        ),
        style={
            "background": DARK_THEME["glass_bg"],
            "border": f"1px solid {DARK_THEME['glass_border']}",
            "border_radius": "16px",
            "padding": "1.5rem",
            "backdrop_filter": "blur(10px)",
            "position": "sticky",
            "top": "2rem"
        }
    )

def metric_card_v41(titulo: str, valor: rx.Var, icono: str, color: str) -> rx.Component:
    """📈 Card de métrica individual"""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon(icono, size=16),
                style={
                    "background": f"rgba({color.replace('#', '').replace('rgb(', '').replace(')', '')}, 0.2)",
                    "border_radius": "8px",
                    "padding": "8px",
                    "color": color
                }
            ),
            rx.vstack(
                rx.text(titulo, size="2", color=DARK_THEME["text_secondary"]),
                rx.text(valor, font_weight="700", size="3", color=DARK_THEME["text_primary"]),
                spacing="0",
                align="start"
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        style={
            "background": DARK_THEME["bg_secondary"],
            "border": f"1px solid {DARK_THEME['border']}",
            "border_radius": "12px",
            "padding": "1rem"
        }
    )

def dashboard_colas_tiempo_real() -> rx.Component:
    """🔄 Dashboard principal de colas en tiempo real"""
    return rx.hstack(
        # Grid de odontólogos (izquierda)
        rx.box(
            rx.vstack(
                # Header con título
                rx.hstack(
                    rx.icon("users", size=24, color=DARK_THEME["accent_blue"]),
                    rx.text(
                        "Sistema de Colas por Odontólogo",
                        font_weight="700",
                        size="5",
                        color=DARK_THEME["text_primary"]
                    ),
                    rx.spacer(),
                    rx.text(
                        "Hoy: " + AppState.get_fecha_actual,
                        color=DARK_THEME["text_secondary"],
                        size="3"
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                    margin_bottom="2rem"
                ),
                
                # Grid responsive de doctores
                rx.grid(
                    rx.foreach(
                        AppState.get_lista_odontologos_activos,
                        doctor_card_v41
                    ),
                    columns=rx.breakpoints({
                        "0px": "1",      # Mobile: 1 columna
                        "768px": "2",    # Tablet: 2 columnas
                        "1200px": "3"    # Desktop: 3 columnas
                    }),
                    spacing="6",
                    width="100%"
                ),
                
                spacing="6",
                width="100%",
                align="start"
            ),
            flex="1"
        ),
        
        # Sidebar con resumen (derecha)
        rx.box(
            sidebar_resumen_v41(),
            width="350px",
            style={
                "position": "sticky",
                "top": "2rem",
                "max_height": "calc(100vh - 4rem)",
                "overflow_y": "auto"
            }
        ),
        
        spacing="6",
        align="start",
        width="100%"
    )

def modal_consulta_v41() -> rx.Component:
    """🪟 Modal para crear/editar consulta - esquema v4.1"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.cond(
                        AppState.consulta_seleccionada,
                        rx.icon("edit", size=20),
                        rx.icon("calendar-plus", size=20)
                    ),
                    rx.cond(
                        AppState.consulta_seleccionada,
                        rx.text("Editar Consulta"),
                        rx.text("Nueva Consulta")
                    ),
                    spacing="2",
                    align="center"
                )
            ),
            
            rx.form(
                rx.vstack(
                    # Selección de paciente con buscador
                    rx.form.field(
                        rx.form.label("Paciente *"),
                        rx.vstack(
                            # Input de búsqueda
                            rx.input(
                                placeholder="Buscar paciente por nombre, apellido o HC...",
                                value=AppState.termino_busqueda_pacientes_modal,
                                on_change=AppState.buscar_pacientes_modal,
                                style={
                                    "background": DARK_THEME["bg_hover"],
                                    "border": f"1px solid {DARK_THEME['border']}",
                                    "color": DARK_THEME["text_primary"],
                                    "border_radius": "8px",
                                    "padding": "0.75rem"
                                }
                            ),
                            # Select con opciones filtradas
                            rx.select(
                                AppState.get_opciones_pacientes_filtradas,
                                placeholder="Seleccionar de la lista...",
                                name="paciente_id",
                                value=AppState.formulario_consulta_data.paciente_id,
                                on_change=lambda val: AppState.update_formulario_consulta("paciente_id", val)
                            ),
                            spacing="2",
                            width="100%"
                        )
                    ),
                    
                    # Odontólogo principal
                    rx.form.field(
                        rx.form.label("Odontólogo Principal"),
                        rx.select(
                            AppState.get_opciones_odontologos,
                            placeholder="Seleccionar odontólogo...",
                            name="primer_odontologo_id",
                            value=AppState.formulario_consulta_data.primer_odontologo_id,
                            on_change=lambda val: AppState.update_formulario_consulta("primer_odontologo_id", val)
                        )
                    ),
                    
                    # Motivo de consulta
                    rx.form.field(
                        rx.form.label("Motivo de Consulta"),
                        rx.text_area(
                            placeholder="Describe el motivo de la consulta...",
                            name="motivo_consulta",
                            value=AppState.formulario_consulta_data.motivo_consulta,
                            on_change=lambda val: AppState.update_formulario_consulta("motivo_consulta", val)
                        )
                    ),
                    
                    # Tipo y prioridad
                    rx.hstack(
                        rx.form.field(
                            rx.form.label("Tipo"),
                            rx.select(
                                ["general", "control", "urgencia", "emergencia"],
                                value=AppState.formulario_consulta_data.tipo_consulta,
                                on_change=lambda val: AppState.update_formulario_consulta("tipo_consulta", val)
                            ),
                            flex="1"
                        ),
                        rx.form.field(
                            rx.form.label("Prioridad"), 
                            rx.select(
                                ["baja", "normal", "alta", "urgente"],
                                value=AppState.formulario_consulta_data.prioridad,
                                on_change=lambda val: AppState.update_formulario_consulta("prioridad", val)
                            ),
                            flex="1"
                        ),
                        spacing="4",
                        width="100%"
                    ),
                    
                    # Observaciones
                    rx.form.field(
                        rx.form.label("Observaciones"),
                        rx.text_area(
                            placeholder="Observaciones adicionales...",
                            name="observaciones",
                            value=AppState.formulario_consulta_data.observaciones,
                            on_change=lambda val: AppState.update_formulario_consulta("observaciones", val)
                        )
                    ),
                    
                    spacing="4",
                    width="100%"
                ),
                
                rx.dialog.close(
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            variant="soft",
                            color_scheme="gray"
                        ),
                        rx.button(
                            rx.cond(
                                AppState.consulta_seleccionada,
                                "Actualizar Consulta",
                                "Crear Consulta"
                            ),
                            type="submit",
                            color_scheme="blue"
                        ),
                        spacing="3",
                        justify="end",
                        margin_top="1rem"
                    )
                ),
                
                on_submit=AppState.guardar_consulta_desde_formulario
            ),
            
            style={
                "background": DARK_THEME["bg_secondary"],
                "border": f"1px solid {DARK_THEME['glass_border']}",
                "max_width": "600px"
            }
        ),
        open=AppState.modal_crear_consulta_abierto
    )

def modal_confirmacion_cancelar_consulta() -> rx.Component:
    """❌ Modal de confirmación para cancelar consulta"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Icono de advertencia
                rx.box(
                    rx.icon("triangle-alert", size=48, color=DARK_THEME["accent_red"]),
                    style={
                        "padding": "1rem",
                        "border_radius": "50%",
                        "background": "rgba(229, 62, 62, 0.15)",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center"
                    }
                ),
                
                # Título y mensaje
                rx.heading(
                    "Confirmar Cancelación",
                    size="5",
                    color=DARK_THEME["text_primary"],
                    text_align="center"
                ),
                
                rx.text(
                    "¿Está seguro de que desea cancelar esta consulta?",
                    size="3",
                    color=DARK_THEME["text_secondary"],
                    text_align="center",
                    line_height="1.5"
                ),
                
                rx.text(
                    "La consulta será marcada como cancelada pero se mantendrá en el historial del sistema.",
                    size="2",
                    color=DARK_THEME["text_muted"],
                    text_align="center",
                    line_height="1.4",
                    font_style="italic"
                ),
                
                # Información de la consulta (simplificada)
                rx.cond(
                    AppState.consulta_para_eliminar,
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("ID Consulta:", font_weight="600", color=DARK_THEME["text_primary"]),
                                rx.text(AppState.consulta_para_eliminar.id, color=DARK_THEME["text_secondary"]),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.text("Estado:", font_weight="600", color=DARK_THEME["text_primary"]),
                                rx.text(AppState.consulta_para_eliminar.estado, color=DARK_THEME["text_secondary"]),
                                spacing="2"
                            ),
                            spacing="2",
                            align="start"
                        ),
                        style={
                            "background": DARK_THEME["bg_hover"],
                            "border": f"1px solid {DARK_THEME['border']}",
                            "border_radius": "8px",
                            "padding": "1rem",
                            "width": "100%"
                        }
                    ),
                    rx.fragment()  # Empty component when no consultation selected for deletion
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=AppState.cerrar_todos_los_modales,
                        style={
                            "border_radius": "8px",
                            "padding": "0.75rem 1.5rem"
                        }
                    ),
                    rx.button(
                        "Confirmar Cancelación",
                        color_scheme="red",
                        on_click=AppState.confirmar_cancelacion_consulta,
                        style={
                            "border_radius": "8px", 
                            "padding": "0.75rem 1.5rem"
                        }
                    ),
                    spacing="3",
                    justify="end",
                    width="100%"
                ),
                
                spacing="4",
                align="center",
                width="100%"
            ),
            
            style={
                "background": DARK_THEME["bg_secondary"],
                "border": f"1px solid {DARK_THEME['glass_border']}",
                "max_width": "500px",
                "border_radius": "16px"
            }
        ),
        open=AppState.modal_confirmacion_abierto
    )

def modal_cambio_odontologo_v41() -> rx.Component:
    """🔄 Modal para cambiar odontólogo de consulta"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header del modal
                rx.hstack(
                    rx.icon("user-switch", size=24, color=DARK_THEME["accent_blue"]),
                    rx.heading(
                        "Cambiar Odontólogo",
                        size="5",
                        color=DARK_THEME["text_primary"]
                    ),
                    spacing="2",
                    align="center",
                    width="100%"
                ),
                
                rx.divider(color=DARK_THEME["border"], margin="1rem 0"),
                
                # Información de la consulta actual
                rx.cond(
                    AppState.consulta_seleccionada,
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "Consulta Actual:",
                                font_weight="600",
                                color=DARK_THEME["text_primary"],
                                size="3"
                            ),
                            rx.hstack(
                                rx.text("Paciente:", font_weight="500", color=DARK_THEME["text_secondary"]),
                                rx.text(AppState.consulta_seleccionada.paciente_nombre, color=DARK_THEME["text_primary"]),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.text("Odontólogo Actual:", font_weight="500", color=DARK_THEME["text_secondary"]),
                                rx.text(AppState.consulta_seleccionada.odontologo_nombre, color=DARK_THEME["text_primary"]),
                                spacing="2"
                            ),
                            spacing="2",
                            align="start"
                        ),
                        style={
                            "background": DARK_THEME["bg_hover"],
                            "border": f"1px solid {DARK_THEME['border']}",
                            "border_radius": "8px",
                            "padding": "1rem",
                            "width": "100%"
                        }
                    ),
                    rx.fragment()  # Empty component when no consultation selected
                ),
                
                # Formulario de cambio
                rx.form(
                    rx.vstack(
                        # Nuevo odontólogo
                        rx.form.field(
                            rx.form.label("Nuevo Odontólogo *"),
                            rx.select(
                                AppState.get_opciones_odontologos,
                                placeholder="Seleccionar nuevo odontólogo...",
                                name="nuevo_odontologo_id",
                                required=True
                            )
                        ),
                        
                        # Motivo del cambio
                        rx.form.field(
                            rx.form.label("Motivo del Cambio *"),
                            rx.text_area(
                                placeholder="Explique el motivo del cambio de odontólogo (mínimo 10 caracteres)...",
                                name="motivo_cambio",
                                required=True,
                                rows="3",
                                style={
                                    "background": DARK_THEME["bg_hover"],
                                    "border": f"1px solid {DARK_THEME['border']}",
                                    "color": DARK_THEME["text_primary"],
                                    "border_radius": "8px"
                                }
                            )
                        ),
                        
                        # Botones de acción
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    variant="soft",
                                    color_scheme="gray"
                                )
                            ),
                            rx.button(
                                "Confirmar Cambio",
                                type="submit",
                                color_scheme="blue"
                            ),
                            spacing="3",
                            justify="end",
                            width="100%"
                        ),
                        
                        spacing="4",
                        width="100%"
                    ),
                    on_submit=AppState.procesar_cambio_odontologo
                ),
                
                spacing="4",
                width="100%",
                align="start"
            ),
            
            style={
                "background": DARK_THEME["bg_secondary"],
                "border": f"1px solid {DARK_THEME['glass_border']}",
                "max_width": "500px",
                "border_radius": "16px"
            }
        ),
        open=AppState.modal_cambio_odontologo_abierto
    )

def consultas_page_v41() -> rx.Component:
    """📅 Página principal de consultas - esquema v4.1 consolidado"""
    return rx.box(
        # Botón flotante
        boton_nueva_consulta_v41(),
        
        # Modal de consulta (crear/editar)
        modal_consulta_v41(),
        
        # Modal de confirmación para cancelar
        modal_confirmacion_cancelar_consulta(),
        
        # Modal de cambio de odontólogo
        modal_cambio_odontologo_v41(),
        
        # Dashboard principal
        dashboard_colas_tiempo_real(),
        
        style={
            "background": DARK_THEME["bg_primary"],
            "min_height": "100vh",
            "padding": "2rem"
        }
    )