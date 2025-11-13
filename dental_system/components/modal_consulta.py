"""
📝 MODAL NUEVA CONSULTA - VERSIÓN MEJORADA UI/UX
=================================================

🎯 ESPECIFICACIONES:
- Diseño consistente con el patrón de forms.py
- Glassmorphism effects y tema oscuro
- Enhanced form fields con validaciones
- Iconografía médica profesional
- Feedback visual en tiempo real

✨ Modal enterprise-level para crear consultas por orden de llegada
"""

import reflex as rx
from dental_system.state.app_state import AppState
from typing import  Optional, Callable, Any
from dental_system.components.forms import enhanced_form_field, form_section_header
from dental_system.styles.themes import (
    COLORS, SHADOWS, RADIUS, SPACING, ANIMATIONS, 
    GRADIENTS, GLASS_EFFECTS, DARK_THEME
)

# ==========================================
# 📝 COMPONENTES DEL FORMULARIO MEJORADO
# ==========================================


def enhanced_form_field_dinamico(
    label: str,
    field_name: str,
    value: Any,
    on_change: Callable,
    placeholder: str = "",
    required: bool = False,
    validation_error: str = "",
    help_text: str = "",
    icon: Optional[str] = None
) -> rx.Component:
    """📝 Campo de formulario con select dinámico de odontólogos"""
    
    return rx.vstack(
        # Label con indicador de requerido
        rx.hstack(
            rx.hstack(
                *([rx.icon(icon, size=18, color=COLORS["primary"]["500"])] if icon else []),
                rx.text(
                    label,
                    style={
                        "font_size": "1rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="2",
                align="center"
            ),
            
            *([rx.text(
                "*",
                style={
                    "color": COLORS["error"]["500"],
                    "font_weight": "700",
                    "margin_left": "2px"
                }
            )] if required else []),
            
            rx.spacer(),
            
            # Texto de ayuda opcional
            *([rx.text(
                help_text,
                style={
                    "font_size": "0.75rem",
                    "color": COLORS["gray"]["500"],
                    "font_style": "italic"
                }
            )] if help_text else []),
            
            width="100%",
            align="center"
        ),
        
        # Select dinámico con estructura correcta
        rx.box(
            rx.select.root(
                rx.select.trigger(
                    placeholder=placeholder,
                    style={
                        "width": "100%",
                        "height": "2.5em",
                        "padding": f"{SPACING['1']} {SPACING['3']}",
                        "border_radius": RADIUS["lg"],
                        "font_size": "1rem",
                        "background": DARK_THEME["colors"]["surface_secondary"],
                        "border": f"2px solid {DARK_THEME['colors']['border']}",
                        "transition": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)",
                        "color": DARK_THEME["colors"]["text_primary"],
                        "placeholder_color": DARK_THEME["colors"]["text_primary"],
                        "_focus": {
                            "outline": "none",
                            "border_color": COLORS["primary"]["400"],
                            "box_shadow": f"0 0 0 3px {COLORS['primary']['200']}",
                            "background": DARK_THEME["colors"]["surface_elevated"]
                        },
                        "_hover": {
                            "border_color": COLORS["primary"]["300"],
                            "box_shadow": f"0 2px 8px rgba(0, 0, 0, 0.2)"
                        }
                    }
                ),
                rx.select.content(
                    rx.cond(
                        AppState.odontologos_disponibles.length() > 0,
                        rx.foreach(
                            AppState.odontologos_disponibles,
                            lambda doctor: rx.select.item(
                                f"Dr(a). {doctor.primer_nombre} {doctor.primer_apellido} ({doctor.especialidad})",
                                value=doctor.id
                            )
                        ),
                        rx.select.item(
                            "No hay odontólogos disponibles",
                            value="",
                            disabled=True
                        )
                    )
                ),
                value=value,
                on_change=lambda v: on_change(field_name, v) if on_change else None,
                width="100%"
            ),
            width="100%"
        ),
        
        # Mensaje de error
        rx.cond(
            validation_error != "",
            rx.hstack(
                rx.icon("triangle-alert", size=14, color=COLORS["error"]["500"]),
                rx.text(
                    validation_error,
                    style={
                        "font_size": "0.75rem",
                        "color": COLORS["error"]["500"],
                        "font_weight": "500"
                    }
                ),
                spacing="2",
                align="center"
            ),
            rx.box()
        ),
        
        spacing="2",
        align="start",
        width="100%"
    )



def selector_odontologo() -> rx.Component:
    """👨‍⚕️ Selector de odontólogo dinámico con enhanced_form_field"""
    return enhanced_form_field_dinamico(
        label="Odontólogo",
        field_name="primer_odontologo_id",
        value=rx.cond(AppState.formulario_consulta_data, AppState.formulario_consulta_data.primer_odontologo_id, ""),
        on_change=lambda field, value: AppState.set_formulario_consulta_field(field, value),
        placeholder="Seleccionar odontólogo...",
        required=True,
        icon="stethoscope",
        help_text="Odontólogo que atenderá la consulta",
        validation_error=rx.cond(
            AppState.errores_validacion_consulta,
            AppState.errores_validacion_consulta.get("odontologo", ""),
            ""
        )
    )


def buscador_paciente() -> rx.Component:
    """🔍 Buscador y selector de paciente con enhanced_form_field"""
    return rx.vstack(
        # Campo de búsqueda mejorado
        enhanced_form_field(
            label="Paciente",
            field_name="busqueda_paciente",
            value=rx.cond(
                AppState.formulario_consulta_data, 
                AppState.formulario_consulta_data.paciente_nombre, 
                AppState.consulta_form_busqueda_paciente
            ),
            on_change=lambda field, value: AppState.actualizar_campo_paciente_consulta(value),
            placeholder="Buscar por nombre o documento...",
            required=True,
            icon="search",
            help_text="Escriba el nombre o número de documento del paciente",
            validation_error=rx.cond(
                AppState.errores_validacion_consulta,
                AppState.errores_validacion_consulta.get("paciente", ""),
                ""
            )
        ),
        
        # Lista de resultados filtrados con glassmorphism
        rx.cond(
            (AppState.consulta_form_busqueda_paciente != "") & ~AppState.modal_editar_consulta_abierto,
            rx.box(
                rx.cond(
                    AppState.pacientes_filtrados_modal_count > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.pacientes_filtrados_modal,
                            paciente_resultado_item
                        ),
                        spacing="0",
                        width="100%"
                    ),
                    rx.box(
                        rx.hstack(
                            rx.icon("search-x", size=16, color=COLORS["gray"]["400"]),
                            rx.text(
                                "No se encontraron pacientes",
                                style={
                                    "color": DARK_THEME["colors"]["text_secondary"],
                                    "font_size": "0.9rem",
                                    "font_style": "italic"
                                }
                            ),
                            spacing="2",
                            align="center",
                            justify="center",
                            width="100%",
                            padding="1rem"
                        )
                    )
                ),
                style={
                    "background": DARK_THEME["colors"]["surface_secondary"],
                    "border": f"2px solid {DARK_THEME['colors']['border']}",
                    "border_radius": RADIUS["lg"],
                    "max_height": "200px",
                    "overflow_y": "auto",
                    "box_shadow": SHADOWS["md"]
                }
            ),
            rx.box()
        ),     
        spacing="4",
        width="100%",
        align="start"
    )

def paciente_resultado_item(paciente: rx.Var) -> rx.Component:
    """👤 Item individual de resultado de búsqueda con tema oscuro"""
    return rx.box(
        rx.hstack(
            # Icono con glassmorphism
            rx.box(
                rx.icon("user", size=16, color=COLORS["primary"]["400"]),
                style={
                    "width": "32px",
                    "height": "32px",
                    "border_radius": RADIUS["lg"],
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center",
                    "background": f"linear-gradient(135deg, {COLORS['primary']['500']}15 0%, {COLORS['primary']['300']}10 100%)",
                    "border": f"1px solid {COLORS['primary']['500']}30"
                }
            ),
            
            # Información del paciente
            rx.vstack(
                rx.text(
                    f"{paciente.primer_nombre} {paciente.primer_apellido}",
                    style={
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"],
                        "font_size": "0.9rem"
                    }
                ),
                rx.text(
                    f"CC: {paciente.numero_documento}",
                    style={
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "font_size": "0.8rem"
                    }
                ),
                spacing="1",
                align="start"
            ),
            
            rx.spacer(),
            
            # Botón mejorado
            rx.button(
                rx.hstack(
                    rx.icon("user-plus", size=14),
                    rx.text("Seleccionar"),
                    spacing="1",
                    align="center"
                ),
                size="1",
                style={
                    "background": GRADIENTS["neon_primary"],
                    "color": "white",
                    "border": "none",
                    "border_radius": RADIUS["md"],
                    "font_size": "0.8rem",
                    "padding": f"{SPACING['1']} {SPACING['3']}",
                    "transition": ANIMATIONS["presets"]["fade_in"],
                    "_hover": {
                        "transform": "translateY(-1px)",
                        "box_shadow": SHADOWS["md"]
                    }
                },
                # 🔄 CORREGIDO: seleccionar_paciente_modal → gestionar_modal_operacion
                on_click=lambda: AppState.gestionar_modal_operacion("seleccionar_paciente_modal", datos={"paciente_id": paciente.id})
            ),
            
            spacing="3",
            align="center",
            width="100%"
        ),
        style={
            "padding": SPACING["3"],
            "border_bottom": f"1px solid {DARK_THEME['colors']['border']}",
            "transition": ANIMATIONS["presets"]["fade_in"],
            "_hover": {
                "background": DARK_THEME["colors"]["surface_elevated"],
                "transform": "translateX(2px)"
            },
            "_last": {
                "border_bottom": "none"
            }
        },
        width="100%"
    )

def campos_adicionales() -> rx.Component:
    """📝 Campos adicionales con enhanced_form_field"""
    return rx.vstack(
        # Grid responsive para campos
        rx.grid(
            # Tipo de consulta
            enhanced_form_field(
                label="Tipo de Consulta",
                field_name="tipo_consulta",
                value=rx.cond(AppState.formulario_consulta_data, AppState.formulario_consulta_data.tipo_consulta, "general"),
                on_change=lambda field, value: AppState.set_formulario_consulta_field(field, value),
                field_type="select",
                options=["general", "control", "urgencia", "emergencia"],
                icon="activity",
                help_text="Predeterminado: general"
            ),
            
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="5",
            width="100%"
        ),
        
        # Motivo de la consulta con enhanced_form_field
        enhanced_form_field(
            label="Motivo de la Consulta",
            field_name="motivo_consulta",
            value=rx.cond(AppState.formulario_consulta_data, AppState.formulario_consulta_data.motivo_consulta, ""),
            on_change=lambda field, value: AppState.set_formulario_consulta_field(field, value),
            field_type="textarea",
            placeholder="¿Por qué viene el paciente? (opcional)",
            icon="file-text",
            help_text="Descripción del motivo de la consulta",
            max_length=400
        ),
        
        spacing="4",
        width="100%",
        align="start"
    )

# ==========================================
# 📱 MODAL PRINCIPAL MEJORADO
# ==========================================

def modal_nueva_consulta() -> rx.Component:
    """📝 Modal principal para crear nueva consulta con diseño enterprise"""
    return rx.dialog.root(
        rx.dialog.content(
            # Header elegante con glassmorphism
            rx.vstack(
                rx.hstack(
                    form_section_header(
                        # rx.cond(
                        #     AppState.modal_editar_consulta_abierto,
                        #     "Editar Consulta",
                        #     "Nueva Consulta"
                        # ),
                        "Nueva Consulta",
                        "Registrar consulta por orden de llegada",
                        "calendar-plus",
                        COLORS["primary"]["500"]
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=20),
                            style={
                                "background": "transparent",
                                "border": "none",
                                "color": COLORS["gray"]["500"],
                                "cursor": "pointer",
                                "_hover": {"color": COLORS["gray"]["700"]}
                            }
                        )
                    ),
                    width="100%",
                    align="center"
                ),
                spacing="4",
                width="100%",
                margin_bottom=SPACING["6"]
            ),
            
            # Formulario mejorado
            rx.form(
                rx.vstack(
                    # Selector de odontólogo
                    selector_odontologo(),
                    
                    # Buscador de paciente
                    buscador_paciente(),
                    
                    # Campos adicionales
                    campos_adicionales(),
                    
                    
                    # Botones de navegación mejorados
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", size=16),
                                    rx.text("Cancelar"),
                                    spacing="2",
                                    align="center"
                                ),
                                style={
                                    **GLASS_EFFECTS["light"],
                                    "border": f"1px solid {COLORS['gray']['300']}",
                                    "color": COLORS["gray"]["700"],
                                    "border_radius": RADIUS["xl"],
                                    "padding": f"{SPACING['3']} {SPACING['5']}",
                                    "font_weight": "600",
                                    "transition": ANIMATIONS["presets"]["crystal_hover"],
                                    "_hover": {
                                        **GLASS_EFFECTS["medium"],
                                        "transform": "translateY(-2px)",
                                        "box_shadow": SHADOWS["sm"]
                                    }
                                }
                            )
                        ),
                        
                        rx.spacer(),
                        
                        rx.button(
                            rx.cond(
                                AppState.cargando_crear_consulta,
                                rx.hstack(
                                    rx.spinner(size="3", color="white"),
                                    rx.text("Procesando..."),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text(
                                        rx.cond(
                                            AppState.modal_editar_consulta_abierto,
                                            "Actualizar Consulta",
                                            "Crear Consulta"
                                        )
                                    ),
                                    rx.icon(
                                        rx.cond(
                                            AppState.modal_editar_consulta_abierto,
                                            "edit",
                                            "calendar-plus"
                                        ), 
                                        size=16
                                    ),
                                    spacing="2",
                                    align="center"
                                )
                            ),
                            style={
                                "background": GRADIENTS["neon_primary"],
                                "color": "white",
                                "border": "none",
                                "border_radius": RADIUS["xl"],
                                "padding": f"{SPACING['3']} {SPACING['6']}",
                                "font_weight": "700",
                                "font_size": "1rem",
                                "box_shadow": SHADOWS["glow_primary"],
                                "transition": ANIMATIONS["presets"]["crystal_hover"],
                                "_hover": {
                                    "transform": "translateY(-2px) scale(1.02)",
                                    "box_shadow": f"0 0 30px {COLORS['primary']['500']}40, {SHADOWS['crystal_lg']}"
                                },
                                "_disabled": {
                                    "opacity": "0.6",
                                    "cursor": "not-allowed",
                                    "transform": "none"
                                }
                            },
                            on_click=rx.cond(
                                AppState.modal_editar_consulta_abierto,
                                AppState.actualizar_consulta,
                                AppState.guardar_consulta_modal
                            ),
                            disabled=AppState.cargando_crear_consulta
                        ),  
                        width="100%",
                        align="center"
                    ),
                    
                    spacing="4",
                    width="100%",
                    align="start"
                ),
            ),
            
            style={
                "max_width": "600px",
                # "width": "90vw",
                # "max_height": "90vh",
                "padding": SPACING["4"],
                "border_radius": RADIUS["xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['primary']['200']}30",
                "overflow_y": "auto",
                "backdrop_filter": "blur(20px)"
            }
        ),
        open=AppState.modal_crear_consulta_abierto | AppState.modal_editar_consulta_abierto,
        on_open_change=AppState.cerrar_todos_los_modales
    )
    
    
    
    
def modal_transferir_paciente() -> rx.Component:
    """🔄 MODAL PARA TRANSFERIR PACIENTE - VERSIÓN ENTERPRISE MEJORADA"""
    return rx.dialog.root(
        rx.dialog.content(
            # Header elegante con glassmorphism
            rx.vstack(
                rx.hstack(
                    form_section_header(
                        "Transferir Paciente",
                        "Cambiar odontólogo asignado a la consulta",
                        "arrow-right-left",
                        COLORS["blue"]["500"]
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=20),
                            style={
                                "background": "transparent",
                                "border": "none",
                                "color": COLORS["gray"]["500"],
                                "cursor": "pointer",
                                "_hover": {"color": COLORS["gray"]["700"]}
                            }
                        )
                    ),
                    width="100%",
                    align="center"
                ),
                spacing="4",
                width="100%"
            ),
            
            # Formulario mejorado
            rx.form(
                rx.vstack(
                    # Info del paciente con feedback visual mejorado
                    rx.cond(
                        AppState.consulta_para_transferir,
                        rx.vstack(
                            rx.text(
                                "Información del Paciente",
                                style={
                                    "font_size": "1rem",
                                    "font_weight": "600",
                                    "color": DARK_THEME["colors"]["text_primary"],
                                    "margin_bottom": SPACING["2"]
                                }
                            ),
                            rx.text(
                                f"Paciente: {AppState.consulta_para_transferir.paciente_nombre} | Posición: #{AppState.consulta_para_transferir.orden_cola_odontologo}",
                                color= DARK_THEME["colors"]["text_primary"],
                            ),
                            spacing="2",
                            width="100%"
                        ),
                        rx.box()
                    ),
                    
                    # Selector dinámico de odontólogo 
                    enhanced_form_field_dinamico(
                        label="Odontólogo de Destino",
                        field_name="odontologo_destino",
                        value=rx.cond(AppState.odontologo_destino_seleccionado, AppState.odontologo_destino_seleccionado, ""),
                        on_change=lambda field, value: AppState.gestionar_modal_operacion("set_odontologo_destino", datos={"odontologo_id": value}),
                        placeholder="Seleccionar odontólogo de destino...",
                        required=True,
                        icon="user-round",
                        help_text="Odontólogo que recibirá al paciente",
                        validation_error=""
                    ),
                    
                    
                    enhanced_form_field(
                        label="Motivo de la Transferencia",
                        field_name="motivo_transferencia",
                        value=rx.cond(AppState.motivo_transferencia, AppState.motivo_transferencia, ""),
                        on_change=lambda field, value: AppState.gestionar_modal_operacion("set_motivo_transferencia", datos={"motivo": value}),
                        field_type="textarea",
                        placeholder="Explique por qué se transfiere al paciente...",
                        required=True,
                        icon="file-text",
                        help_text="Justificación requerida para transferencias",
                        max_length=500,
                        validation_error=""
                    ),
                    # Botones de navegación mejorados
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", size=16),
                                    rx.text("Cancelar"),
                                    spacing="2",
                                    align="center"
                                ),
                                style={
                                    **GLASS_EFFECTS["light"],
                                    "border": f"1px solid {COLORS['gray']['300']}",
                                    "color": COLORS["gray"]["700"],
                                    "border_radius": RADIUS["xl"],
                                    "padding": f"{SPACING['3']} {SPACING['5']}",
                                    "font_weight": "600",
                                    "transition": ANIMATIONS["presets"]["crystal_hover"],
                                    "_hover": {
                                        **GLASS_EFFECTS["medium"],
                                        "transform": "translateY(-2px)",
                                        "box_shadow": SHADOWS["sm"]
                                    }
                                },
                                # 🔄 CORREGIDO: cerrar_modal_transferir_paciente → gestionar_modal_operacion
                                on_click=lambda: AppState.gestionar_modal_operacion("cerrar_transferencia")
                            )
                        ),
                        
                        rx.spacer(),
                        
                        rx.button(
                            rx.hstack(
                                rx.text("Transferir Paciente"),
                                rx.icon("arrow-right-left", size=16),
                                spacing="2",
                                align="center"
                            ),
                            style={
                                "background": f"linear-gradient(135deg, {COLORS['blue']['500']}, {COLORS['blue']['600']})",
                                "color": "white",
                                "border": "none",
                                "border_radius": RADIUS["xl"],
                                "padding": f"{SPACING['3']} {SPACING['6']}",
                                "font_weight": "700",
                                "font_size": "1rem",
                                "box_shadow": f"0 0 20px {COLORS['blue']['500']}40",
                                "transition": ANIMATIONS["presets"]["crystal_hover"],
                                "_hover": {
                                    "transform": "translateY(-2px) scale(1.02)",
                                    "box_shadow": f"0 0 30px {COLORS['blue']['500']}50, {SHADOWS['crystal_lg']}"
                                },
                                "_disabled": {
                                    "opacity": "0.6",
                                    "cursor": "not-allowed",
                                    "transform": "none"
                                }
                            },
                            on_click=AppState.ejecutar_transferencia_paciente
                        ),
                        
                        width="100%",
                        align="center",
                        margin_top=SPACING["8"]
                    ),
                    
                    spacing="6",
                    width="100%",
                    align="start"
                ),
            ),
            
            style={
                "max_width": "600px",
                "width": "90vw",
                "max_height": "90vh",
                "padding": SPACING["8"],
                "border_radius": RADIUS["3xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['blue']['200']}30",
                "overflow_y": "auto",
                "backdrop_filter": "blur(20px)"
            }
        ),
        open=AppState.modal_transferir_paciente_abierto,
        on_open_change=lambda open: rx.cond(~open, AppState.gestionar_modal_operacion("cerrar_transferencia"), rx.noop())
    )