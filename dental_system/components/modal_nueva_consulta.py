"""
📝 MODAL NUEVA CONSULTA - FASE 1 SIMPLIFICADO
===============================================

🎯 ESPECIFICACIONES:
- UN solo botón con selectores
- Selector de odontólogo
- Buscador/selector de paciente  
- Campos mínimos necesarios
- Diseño limpio y funcional

✨ Modal optimizado para crear consultas por orden de llegada
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import primary_button, secondary_button

# ==========================================
# 🎨 ESTILOS DEL MODAL
# ==========================================

MODAL_STYLES = {
    "surface": "#ffffff",
    "border": "#e5e7eb", 
    "text_primary": "#111827",
    "text_secondary": "#6b7280",
    "primary": "#2563eb",
    "success": "#10b981",
    "gray_50": "#f9fafb"
}

# ==========================================
# 📝 COMPONENTES DEL FORMULARIO  
# ==========================================

def selector_odontologo() -> rx.Component:
    """👨‍⚕️ Selector de odontólogo"""
    return rx.vstack(
        rx.text(
            "Odontólogo *",
            style={
                "font_weight": "600",
                "color": MODAL_STYLES["text_primary"],
                "font_size": "0.95rem"
            }
        ),
        rx.select.root(
            rx.select.trigger(
                placeholder="Seleccionar odontólogo...",
                style={
                    "background": MODAL_STYLES["surface"],
                    "border": f"1px solid {MODAL_STYLES['border']}",
                    "border_radius": "8px",
                    "padding": "0.75rem",
                    "color": MODAL_STYLES["text_primary"],
                    "width": "100%",
                    "_focus": {
                        "border_color": MODAL_STYLES["primary"],
                        "box_shadow": f"0 0 0 3px rgba(37, 99, 235, 0.1)"
                    }
                }
            ),
            rx.select.content(
                rx.foreach(
                    AppState.odontologos_list,
                    lambda odontologo: rx.select.item(
                        rx.hstack(
                            rx.icon("user-round", size=16),
                            rx.text(odontologo.nombre_completo),
                            rx.text(
                                f"({odontologo.especialidad})",
                                style={"color": MODAL_STYLES["text_secondary"], "font_size": "0.85rem"}
                            ),
                            spacing="0.5rem",
                            align="center"
                        ),
                        value=odontologo.id
                    )
                ),
                style={
                    "background": MODAL_STYLES["surface"],
                    "border": f"1px solid {MODAL_STYLES['border']}",
                    "border_radius": "8px",
                    "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)",
                    "max_height": "200px",
                    "overflow_y": "auto"
                }
            ),
            value=AppState.consulta_form_odontologo_id,
            on_value_change=AppState.set_consulta_form_odontologo_id,
            size="3"
        ),
        spacing="0.5rem",
        width="100%",
        align="start"
    )

def buscador_paciente() -> rx.Component:
    """🔍 Buscador y selector de paciente"""
    return rx.vstack(
        rx.text(
            "Paciente *",
            style={
                "font_weight": "600",
                "color": MODAL_STYLES["text_primary"],
                "font_size": "0.95rem"
            }
        ),
        
        # Input de búsqueda
        rx.input(
            placeholder="🔍 Buscar por nombre o documento...",
            value=AppState.consulta_form_busqueda_paciente,
            on_change=AppState.set_consulta_form_busqueda_paciente,
            style={
                "background": MODAL_STYLES["surface"],
                "border": f"1px solid {MODAL_STYLES['border']}",
                "border_radius": "8px",
                "padding": "0.75rem",
                "color": MODAL_STYLES["text_primary"],
                "width": "100%",
                "_focus": {
                    "border_color": MODAL_STYLES["primary"],
                    "box_shadow": f"0 0 0 3px rgba(37, 99, 235, 0.1)"
                },
                "_placeholder": {"color": MODAL_STYLES["text_secondary"]}
            }
        ),
        
        # Lista de resultados filtrados
        rx.cond(
            AppState.consulta_form_busqueda_paciente != "",
            rx.box(
                rx.cond(
                    AppState.pacientes_filtrados_modal.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.pacientes_filtrados_modal,
                            paciente_resultado_item
                        ),
                        spacing="0",
                        width="100%"
                    ),
                    rx.box(
                        rx.text(
                            "No se encontraron pacientes",
                            style={
                                "color": MODAL_STYLES["text_secondary"],
                                "font_size": "0.9rem",
                                "text_align": "center",
                                "padding": "1rem"
                            }
                        )
                    )
                ),
                style={
                    "background": MODAL_STYLES["surface"],
                    "border": f"1px solid {MODAL_STYLES['border']}",
                    "border_radius": "8px",
                    "max_height": "200px",
                    "overflow_y": "auto",
                    "margin_top": "0.5rem"
                }
            ),
            rx.box()
        ),
        
        # Paciente seleccionado (si hay)
        rx.cond(
            AppState.consulta_form_paciente_seleccionado.nombre_completo != "",
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.icon("user-check", size=16, color="white"),
                        style={
                            "background": MODAL_STYLES["success"],
                            "border_radius": "6px",
                            "padding": "8px",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center"
                        }
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.consulta_form_paciente_seleccionado.nombre_completo,
                            style={
                                "font_weight": "600",
                                "color": MODAL_STYLES["text_primary"]
                            }
                        ),
                        rx.text(
                            f"CC: {AppState.consulta_form_paciente_seleccionado.numero_documento}",
                            style={
                                "color": MODAL_STYLES["text_secondary"],
                                "font_size": "0.85rem"
                            }
                        ),
                        spacing="0.25rem",
                        align="start"
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=16),
                        size="1",
                        style={
                            "background": "transparent",
                            "color": MODAL_STYLES["text_secondary"],
                            "border": "none",
                            "padding": "4px"
                        },
                        on_click=AppState.limpiar_paciente_seleccionado
                    ),
                    spacing="0.75rem",
                    align="center",
                    width="100%"
                ),
                style={
                    "background": f"rgba(16, 185, 129, 0.05)",
                    "border": f"1px solid rgba(16, 185, 129, 0.2)",
                    "border_radius": "8px",
                    "padding": "1rem",
                    "margin_top": "0.5rem"
                }
            ),
            rx.box()
        ),
        
        spacing="0.5rem",
        width="100%",
        align="start"
    )

def paciente_resultado_item(paciente: rx.Var[dict]) -> rx.Component:
    """👤 Item individual de resultado de búsqueda"""
    return rx.box(
        rx.hstack(
            rx.icon("user", size=16, color=MODAL_STYLES["text_secondary"]),
            rx.vstack(
                rx.text(
                    paciente.nombre_completo,
                    style={
                        "font_weight": "600",
                        "color": MODAL_STYLES["text_primary"],
                        "font_size": "0.9rem"
                    }
                ),
                rx.text(
                    f"CC: {paciente.numero_documento} | Tel: {paciente.telefono_1}",
                    style={
                        "color": MODAL_STYLES["text_secondary"],
                        "font_size": "0.8rem"
                    }
                ),
                spacing="0.25rem",
                align="start"
            ),
            rx.spacer(),
            rx.button(
                "Seleccionar",
                size="1",
                style={
                    "background": MODAL_STYLES["primary"],
                    "color": "white",
                    "border": "none",
                    "font_size": "0.8rem"
                },
                on_click=lambda: AppState.seleccionar_paciente_modal(paciente.id)
            ),
            spacing="0.75rem",
            align="center",
            width="100%"
        ),
        style={
            "padding": "0.75rem",
            "border_bottom": f"1px solid {MODAL_STYLES['border']}",
            "transition": "background 0.2s ease",
            "_hover": {
                "background": MODAL_STYLES["gray_50"]
            },
            "_last": {
                "border_bottom": "none"
            }
        },
        width="100%"
    )

def campos_adicionales() -> rx.Component:
    """📝 Campos adicionales del formulario"""
    return rx.vstack(
        # Tipo de consulta
        rx.vstack(
            rx.text(
                "Tipo de Consulta",
                style={
                    "font_weight": "600",
                    "color": MODAL_STYLES["text_primary"],
                    "font_size": "0.95rem"
                }
            ),
            rx.select.root(
                rx.select.trigger(
                    placeholder="Seleccionar tipo...",
                    style={
                        "background": MODAL_STYLES["surface"],
                        "border": f"1px solid {MODAL_STYLES['border']}",
                        "border_radius": "8px",
                        "padding": "0.75rem",
                        "color": MODAL_STYLES["text_primary"],
                        "width": "100%"
                    }
                ),
                rx.select.content(
                    rx.select.item("General", value="general"),
                    rx.select.item("Control", value="control"),
                    rx.select.item("Urgencia", value="urgencia"),
                    rx.select.item("Cirugía", value="cirugia"),
                    rx.select.item("Otro", value="otro")
                ),
                value=AppState.consulta_form_tipo_consulta,
                on_value_change=AppState.set_consulta_form_tipo_consulta,
                default_value="general"
            ),
            spacing="0.5rem",
            width="100%",
            align="start"
        ),
        
        # Prioridad
        rx.vstack(
            rx.text(
                "Prioridad",
                style={
                    "font_weight": "600",
                    "color": MODAL_STYLES["text_primary"],
                    "font_size": "0.95rem"
                }
            ),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("circle", size=12, color="#10b981"),
                        rx.text("Normal", style={"font_size": "0.85rem"}),
                        spacing="0.25rem",
                        align="center"
                    ),
                    size="2",
                    style={
                        "background": rx.cond(
                            AppState.consulta_form_prioridad == "normal",
                            "rgba(16, 185, 129, 0.1)",
                            "transparent"
                        ),
                        "border": f"1px solid {MODAL_STYLES['border']}",
                        "color": MODAL_STYLES["text_primary"],
                        "_hover": {"background": "rgba(16, 185, 129, 0.1)"}
                    },
                    on_click=lambda: AppState.set_consulta_form_prioridad("normal")
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("circle", size=12, color="#f59e0b"),
                        rx.text("Urgente", style={"font_size": "0.85rem"}),
                        spacing="0.25rem",
                        align="center"
                    ),
                    size="2",
                    style={
                        "background": rx.cond(
                            AppState.consulta_form_prioridad == "urgente",
                            "rgba(245, 158, 11, 0.1)",
                            "transparent"
                        ),
                        "border": f"1px solid {MODAL_STYLES['border']}",
                        "color": MODAL_STYLES["text_primary"],
                        "_hover": {"background": "rgba(245, 158, 11, 0.1)"}
                    },
                    on_click=lambda: AppState.set_consulta_form_prioridad("urgente")
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("circle", size=12, color="#ef4444"),
                        rx.text("Emergencia", style={"font_size": "0.85rem"}),
                        spacing="0.25rem",
                        align="center"
                    ),
                    size="2",
                    style={
                        "background": rx.cond(
                            AppState.consulta_form_prioridad == "emergencia",
                            "rgba(239, 68, 68, 0.1)",
                            "transparent"
                        ),
                        "border": f"1px solid {MODAL_STYLES['border']}",
                        "color": MODAL_STYLES["text_primary"],
                        "_hover": {"background": "rgba(239, 68, 68, 0.1)"}
                    },
                    on_click=lambda: AppState.set_consulta_form_prioridad("emergencia")
                ),
                spacing="0.5rem",
                width="100%"
            ),
            spacing="0.5rem",
            width="100%",
            align="start"
        ),
        
        # Motivo de la consulta
        rx.vstack(
            rx.text(
                "Motivo de la Consulta",
                style={
                    "font_weight": "600",
                    "color": MODAL_STYLES["text_primary"],
                    "font_size": "0.95rem"
                }
            ),
            rx.text_area(
                placeholder="¿Por qué viene el paciente? (opcional)",
                value=AppState.consulta_form_motivo,
                on_change=AppState.set_consulta_form_motivo,
                rows=3,
                style={
                    "background": MODAL_STYLES["surface"],
                    "border": f"1px solid {MODAL_STYLES['border']}",
                    "border_radius": "8px",
                    "padding": "0.75rem",
                    "color": MODAL_STYLES["text_primary"],
                    "width": "100%",
                    "_focus": {
                        "border_color": MODAL_STYLES["primary"],
                        "box_shadow": f"0 0 0 3px rgba(37, 99, 235, 0.1)"
                    },
                    "_placeholder": {"color": MODAL_STYLES["text_secondary"]}
                }
            ),
            spacing="0.5rem",
            width="100%",
            align="start"
        ),
        
        spacing="1.5rem",
        width="100%",
        align="start"
    )

# ==========================================
# 📱 MODAL PRINCIPAL 
# ==========================================

def modal_nueva_consulta() -> rx.Component:
    """📝 Modal principal para crear nueva consulta"""
    return rx.dialog.root(
        rx.dialog.content(
            # Header
            rx.dialog.title(
                "Nueva Consulta",
                style={
                    "color": MODAL_STYLES["text_primary"],
                    "font_size": "1.5rem",
                    "font_weight": "700",
                    "margin_bottom": "1.5rem"
                }
            ),
            
            # Formulario
            rx.form(
                rx.vstack(
                    # Selector de odontólogo
                    selector_odontologo(),
                    
                    # Buscador de paciente
                    buscador_paciente(),
                    
                    # Campos adicionales
                    campos_adicionales(),
                    
                    # Botones de acción
                    rx.hstack(
                        rx.dialog.close(
                            secondary_button(
                                "Cancelar",
                                style={"background": "transparent", "color": MODAL_STYLES["text_secondary"]}
                            )
                        ),
                        primary_button(
                            "Crear Consulta",
                            icon="calendar-plus",
                            loading=AppState.cargando_crear_consulta,
                            style={"background": MODAL_STYLES["primary"]}
                        ),
                        spacing="1rem",
                        justify="end",
                        width="100%"
                    ),
                    
                    spacing="1.5rem",
                    width="100%",
                    align="start"
                ),
                on_submit=AppState.crear_nueva_consulta
            ),
            
            style={
                "background": MODAL_STYLES["surface"],
                "border": f"1px solid {MODAL_STYLES['border']}",
                "border_radius": "12px",
                "box_shadow": "0 10px 25px rgba(0, 0, 0, 0.15)",
                "padding": "2rem",
                "max_width": "500px",
                "max_height": "90vh",
                "overflow_y": "auto"
            }
        ),
        open=AppState.modal_crear_consulta_abierto,
        on_open_change=AppState.set_modal_crear_consulta_abierto
    )