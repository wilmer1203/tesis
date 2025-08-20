"""
📝 MODAL NUEVA CONSULTA - VERSIÓN SIMPLIFICADA FUNCIONAL
========================================================

Modal básico que funciona sin errores de sintaxis
Fase 1 - Versión funcional mínima
"""

import reflex as rx
from dental_system.state.app_state import AppState

def modal_nueva_consulta_simple() -> rx.Component:
    """📝 Modal simplificado para crear consulta"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Nueva Consulta"),
            
            rx.vstack(
                # Mensaje de testing
                rx.text(
                    "🧪 Modal de prueba - Fase 1",
                    style={
                        "background": "#e0f2fe",
                        "padding": "1rem",
                        "border_radius": "8px",
                        "text_align": "center",
                        "color": "#0277bd",
                        "font_weight": "600"
                    }
                ),
                
                # Selector de odontólogo con lista desplegable
                rx.vstack(
                    rx.text("Odontólogo *", font_weight="600"),
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Seleccionar odontólogo...",
                            style={
                                "width": "100%",
                                "background": "white",
                                "border": "1px solid #d1d5db",
                                "border_radius": "6px",
                                "padding": "0.5rem"
                            }
                        ),
                        rx.select.content(
                            rx.foreach(
                                AppState.odontologos_disponibles,
                                lambda doctor: rx.select.item(
                                    f"Dr. {doctor.nombre_completo} - {doctor.especialidad}",
                                    value=doctor.id
                                )
                            )
                        ),
                        value=AppState.consulta_form_odontologo_id,
                        on_change=AppState.set_consulta_form_odontologo_id,
                        width="100%"
                    ),
                    align="start",
                    width="100%"
                ),
                
                # Paciente simple
                rx.vstack(
                    rx.text("Buscar Paciente:", font_weight="600"),
                    rx.input(
                        placeholder="Nombre o documento del paciente...",
                        value=AppState.consulta_form_busqueda_paciente,
                        on_change=AppState.set_consulta_form_busqueda_paciente
                    ),
                    align="start",
                    width="100%"
                ),
                
                # Lista de pacientes encontrados con información completa
                rx.cond(
                    AppState.pacientes_filtrados_modal.length() > 0,
                    rx.vstack(
                        rx.text("Pacientes encontrados:", font_weight="600", color="#374151"),
                        rx.foreach(
                            AppState.pacientes_filtrados_modal,
                            lambda paciente: rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text(
                                                paciente.nombre_completo,
                                                font_weight="600",
                                                color="#111827"
                                            ),
                                            rx.text(
                                                f"CC: {paciente.numero_documento}",
                                                size="2",
                                                color="#6b7280"
                                            ),
                                            rx.cond(
                                                paciente.telefono_display != "",
                                                rx.text(
                                                    f"📞 {paciente.telefono_display}",
                                                    size="2",
                                                    color="#2563eb"
                                                ),
                                                rx.box()
                                            ),
                                            spacing="1",
                                            align="start"
                                        ),
                                        rx.spacer(),
                                        rx.button(
                                            "✅ Seleccionar",
                                            size="2",
                                            style={
                                                "background": "#10b981",
                                                "color": "white",
                                                "_hover": {"background": "#059669"}
                                            },
                                            on_click=lambda: AppState.seleccionar_paciente_modal(paciente.id)
                                        ),
                                        width="100%",
                                        align="center"
                                    ),
                                    spacing="2",
                                    width="100%"
                                ),
                                style={
                                    "padding": "0.75rem",
                                    "border": "1px solid #e5e7eb",
                                    "border_radius": "8px",
                                    "margin_bottom": "0.5rem",
                                    "background": "#f9fafb",
                                    "transition": "all 0.2s ease",
                                    "_hover": {
                                        "background": "white",
                                        "border_color": "#2563eb",
                                        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
                                    }
                                }
                            )
                        ),
                        max_height="300px",
                        overflow_y="auto",
                        width="100%"
                    ),
                    # Estado cuando no hay resultados pero sí hay búsqueda
                    rx.cond(
                        AppState.consulta_form_busqueda_paciente.length() > 1,
                        rx.box(
                            rx.text(
                                "❌ No se encontraron pacientes con ese nombre o documento",
                                style={
                                    "padding": "1rem",
                                    "background": "#fef2f2",
                                    "border": "1px solid #fecaca",
                                    "border_radius": "6px",
                                    "color": "#dc2626",
                                    "text_align": "center",
                                    "font_style": "italic"
                                }
                            )
                        ),
                        rx.box()
                    )
                ),
                
                # Paciente seleccionado
                rx.cond(
                    AppState.consulta_form_paciente_seleccionado.id != "",
                    rx.box(
                        rx.text(
                            f"✅ Paciente: {AppState.consulta_form_paciente_seleccionado.nombre_completo}",
                            style={
                                "background": "#e8f5e8",
                                "padding": "0.75rem",
                                "border_radius": "8px",
                                "color": "#2e7d32"
                            }
                        )
                    ),
                    rx.box()
                ),
                
                # Tipo de consulta
                rx.vstack(
                    rx.text("Tipo de consulta:", font_weight="600"),
                    rx.hstack(
                        rx.button(
                            "General",
                            size="2",
                            style={
                                "background": rx.cond(
                                    AppState.consulta_form_tipo_consulta == "general",
                                    "#2563eb",
                                    "#f3f4f6"
                                ),
                                "color": rx.cond(
                                    AppState.consulta_form_tipo_consulta == "general",
                                    "white",
                                    "#374151"
                                )
                            },
                            on_click=lambda: AppState.set_consulta_form_tipo_consulta("general")
                        ),
                        rx.button(
                            "Urgencia",
                            size="2",
                            style={
                                "background": rx.cond(
                                    AppState.consulta_form_tipo_consulta == "urgencia",
                                    "#2563eb",
                                    "#f3f4f6"
                                ),
                                "color": rx.cond(
                                    AppState.consulta_form_tipo_consulta == "urgencia",
                                    "white",
                                    "#374151"
                                )
                            },
                            on_click=lambda: AppState.set_consulta_form_tipo_consulta("urgencia")
                        ),
                        spacing="1"
                    ),
                    align="start",
                    width="100%"
                ),
                
                # Prioridad
                rx.vstack(
                    rx.text("Prioridad:", font_weight="600"),
                    rx.hstack(
                        rx.button(
                            "🟢 Normal",
                            size="2",
                            style={
                                "background": rx.cond(
                                    AppState.consulta_form_prioridad == "normal",
                                    "#10b981",
                                    "#f3f4f6"
                                ),
                                "color": rx.cond(
                                    AppState.consulta_form_prioridad == "normal",
                                    "white",
                                    "#374151"
                                )
                            },
                            on_click=lambda: AppState.set_consulta_form_prioridad("normal")
                        ),
                        rx.button(
                            "🟡 Urgente",
                            size="2",
                            style={
                                "background": rx.cond(
                                    AppState.consulta_form_prioridad == "urgente",
                                    "#f59e0b",
                                    "#f3f4f6"
                                ),
                                "color": rx.cond(
                                    AppState.consulta_form_prioridad == "urgente",
                                    "white",
                                    "#374151"
                                )
                            },
                            on_click=lambda: AppState.set_consulta_form_prioridad("urgente")
                        ),
                        rx.button(
                            "🔴 Emergencia",
                            size="2",
                            style={
                                "background": rx.cond(
                                    AppState.consulta_form_prioridad == "emergencia",
                                    "#ef4444",
                                    "#f3f4f6"
                                ),
                                "color": rx.cond(
                                    AppState.consulta_form_prioridad == "emergencia",
                                    "white",
                                    "#374151"
                                )
                            },
                            on_click=lambda: AppState.set_consulta_form_prioridad("emergencia")
                        ),
                        spacing="1"
                    ),
                    align="start",
                    width="100%"
                ),
                
                # Motivo
                rx.vstack(
                    rx.text("Motivo (opcional):", font_weight="600"),
                    rx.text_area(
                        placeholder="¿Por qué viene el paciente?",
                        value=AppState.consulta_form_motivo,
                        on_change=AppState.set_consulta_form_motivo,
                        rows="3"
                    ),
                    align="start",
                    width="100%"
                ),
                
                # Botones
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            style={"background": "#6b7280", "color": "white"}
                        )
                    ),
                    rx.button(
                        "Crear Consulta",
                        style={"background": "#2563eb", "color": "white"},
                        loading=AppState.cargando_crear_consulta,
                        on_click=AppState.crear_nueva_consulta
                    ),
                    spacing="1",
                    justify="end",
                    width="100%"
                ),
                
                spacing="1",
                width="100%",
                align="start"
            ),
            
            style={
                "padding": "2rem",
                "max_width": "500px",
                "max_height": "80vh",
                "overflow_y": "auto"
            }
        ),
        open=AppState.modal_crear_consulta_abierto,
        on_open_change=lambda x: AppState.set_modal_crear_consulta_abierto(x)
    )