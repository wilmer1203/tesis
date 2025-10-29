"""
🏥 COMPONENTES DE FORMULARIOS AVANZADOS - SISTEMA ODONTOLÓGICO
==============================================================

✨ Formularios modernos enterprise-level con:
- Multi-step forms con navegación intuitiva
- Validaciones en tiempo real
- Responsive design mobile-first  
- Micro-animaciones y transiciones suaves
- Estados de carga y feedback visual
- Campos médicos especializados
- Auto-save y recuperación de drafts
- Accesibilidad WCAG 2.1 AA compliant

Desarrollado para Reflex.dev con patrones UX/UI modernos
"""

import reflex as rx
from typing import Dict, List, Optional, Callable, Any
from dental_system.state.app_state import AppState
from dental_system.models import PersonalModel, PacienteModel
from dental_system.styles.themes import (
    COLORS, SHADOWS, RADIUS, SPACING, ANIMATIONS, 
    GRADIENTS, GLASS_EFFECTS, DARK_THEME, get_color
)
import re

# ==========================================
# 🎯 COMPONENTES BASE PARA FORMULARIOS
# ==========================================

def form_step_indicator(current_step: int, total_steps: int, step_titles: List[str]) -> rx.Component:
    """📊 Indicador de progreso multi-step con diseño médico profesional"""
    return rx.box(
        rx.hstack(
            *[
                rx.hstack(
                    # Círculo del paso
                    rx.box(
                        rx.cond(
                            current_step > i,
                            rx.icon("check", size=18, color="white"),
                            rx.text(str(i + 1), 
                                   font_size=" 1rem", 
                                   font_weight="700",
                                   color="white")
                        ),
                        style={
                            "width": "40px",
                            "height": "40px",
                            "border_radius": "50%",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center",
                            "background": rx.cond(
                                current_step > i,
                                COLORS["success"]["400"],
                                rx.cond(
                                    current_step == i,
                                    GRADIENTS["neon_primary"],
                                    COLORS["gray"]["300"]
                                )
                            ),
                            "box_shadow": rx.cond(
                                current_step == i,
                                f"0 0 0 4px {COLORS['primary']['100']}, 0 0 20px {COLORS['primary']['300']}40",
                                "none"
                            ),
                            "transition": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)"
                        }
                    ),
                    
                    # Título del paso (solo en desktop)
                    rx.text(
                        step_titles[i],
                        style={
                            "font_size": "1rem",
                            "font_weight": rx.cond(current_step == i, "600", "500"),
                            "color": rx.cond(
                                current_step > i,
                                COLORS["success"]["400"],
                                rx.cond(current_step == i, COLORS["primary"]["400"], COLORS["gray"]["100"])
                            ),
                            "margin_left": SPACING["2"],
                            "display": ["none", "none", "block"]  # Hidden on mobile
                        }
                    ),
                    
                    # Línea conectora (excepto último paso)
                    *([
                        rx.box(
                            style={
                                "width": "60px",
                                "height": "2px",
                                "background": rx.cond(
                                    current_step > i,
                                    COLORS["success"]["400"],
                                    COLORS["gray"]["200"]
                                ),
                                "margin": f"0 {SPACING['3']}",
                                "transition": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)"
                            }
                        )
                    ] if i < len(step_titles) - 1 else []),
                    
                    align="center"
                ) for i in range(len(step_titles))
            ],
            align="center",
            width="100%",
            justify="center",
            wrap="wrap"
        ),
        style={
            # "background": "rgba(255, 255, 255, 0.95)",
            # "border": f"1px solid {COLORS['gray']['200']}",
            "border_radius": RADIUS["2xl"],
            "padding": f"{SPACING['4']} {SPACING['6']}",
            "margin_bottom": SPACING["8"],
            "backdrop_filter": "invert(1)",
            "box_shadow": SHADOWS["md"]
        },
        width="100%"
    )

def form_section_header(title: str, subtitle: str, icon: str, color: str = None) -> rx.Component:
    """📋 Header elegante para secciones de formulario"""
    final_color = color or COLORS["primary"]["500"]
    
    return rx.hstack(
        # Icono con efecto glassmorphism
        rx.box(
            rx.icon(icon, size=24, color=final_color),
            style={
                "width": "50px",
                "height": "50px",
                "border_radius": RADIUS["xl"],
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "background": f"linear-gradient(135deg, {final_color}10 0%, {final_color}05 100%)",
                "border": f"1px solid {final_color}20"
            }
        ),
        
        # Textos
        rx.vstack(
            rx.heading(
                title,
                style={
                    "font_size": "1.5rem",
                    "font_weight": "700",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "line_height": "1.2"
                }
            ),
            rx.text(
                subtitle,
                style={
                    "font_size": "0.875rem",
                    "color": DARK_THEME["colors"]["text_secondary"],
                    "line_height": "1.4"
                }
            ),
            spacing="1",
            align="start"
        ),
        
        spacing="4",
        align="center",
        width="100%",
        margin_bottom=SPACING["4"]
    )

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
                    style=_get_field_style()
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

def enhanced_form_field(
    label: str,
    field_name: str,
    value: Any,
    on_change: Callable,
    field_type: str = "text",
    placeholder: str = "",
    required: bool = False,
    options: Optional[List[str]] = None,
    validation_error: str = "",
    help_text: str = "",
    icon: Optional[str] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None
) -> rx.Component:
    """📝 Campo de formulario avanzado con validación en tiempo real"""
    
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
        
        # Campo de entrada
        rx.box(
            rx.cond(
                field_type == "select",
                rx.select(
                    options or [],
                    value=value,
                    on_change=lambda v: on_change(field_name, v) if on_change else None,
                    placeholder=placeholder,
                    style=_get_field_style()
                ),
                rx.cond(
                    field_type == "textarea",
                    rx.text_area(
                        value=value,
                        on_change=lambda v: on_change(field_name, v) if on_change else None,
                        placeholder=placeholder,
                        style={
                            **_get_field_style(),
                            "min_height": "80px",
                            "resize": "vertical"
                        }
                    ),
                    rx.cond(
                        field_type == "date",
                        rx.input(
                            type="date",
                            value=value,
                            on_change=lambda v: on_change(field_name, v) if on_change else None,
                            style=_get_field_style()
                        ),
                        rx.input(
                            type=field_type,
                            value=value,
                            on_change=lambda v: on_change(field_name, v) if on_change else None,
                            placeholder=placeholder,
                            max_length=max_length,
                            pattern=pattern,
                            style=_get_field_style()
                        )
                    )
                )
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

def _get_field_style() -> Dict[str, str]:
    """🎨 Estilos consistentes para campos de formulario"""
    return {
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
            "box_shadow": f"0 0 0 3px {COLORS['primary']['100']}",
            "background": DARK_THEME["colors"]["surface_elevated"]
        },
        "_hover": {
            "border_color": COLORS["primary"]["300"],
            "box_shadow": f"0 2px 8px rgba(0, 0, 0, 0.2)"
        }
    }


def form_navigation_buttons(
    current_step: int,
    total_steps: int,
    on_previous: Callable,
    on_next: Callable,
    on_submit: Callable,
    is_loading: bool = False,
    can_continue: bool = True
) -> rx.Component:
    """🔄 Botones de navegación del formulario multi-step"""
    
    return rx.hstack(
        # Botón Anterior
        rx.cond(
            current_step == 0,
            rx.box(),  # Espacio vacío en primer paso
            rx.button(
                rx.hstack(
                    rx.icon("chevron-left", size=16),
                    rx.text("Anterior"),
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
                on_click=on_previous,
                disabled=is_loading
            )
        ),
        
        rx.spacer(),
        
        # Botón Siguiente/Finalizar
        rx.button(
            rx.cond(
                is_loading,
                rx.hstack(
                    rx.spinner(size="3", color="white"),
                    rx.text("Procesando..."),
                    spacing="3",
                    align="center"
                ),
                rx.hstack(
                    rx.text(rx.cond(current_step == total_steps - 1, "Crear Paciente", "Continuar")),
                    rx.cond(
                        current_step == total_steps - 1,
                        rx.icon("user-plus", size=16),
                        rx.icon("chevron-right", size=16)
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
            on_click=rx.cond(current_step == total_steps - 1, on_submit, on_next),
            disabled=is_loading | ~can_continue
        ),
        
        width="100%",
        align="center",
        margin_top=SPACING["8"]
    )

# ==========================================
# 🏥 FORMULARIO MULTI-STEP DE PACIENTES
# ==========================================

def multi_step_patient_form() -> rx.Component:
    """👥 Formulario multi-step moderno para crear/editar pacientes"""
    
    step_titles = ["Datos Personales", "Contacto", "Información Médica"]
    
    return rx.dialog.root(
        rx.dialog.content(
            # Header del modal
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        rx.cond(
                            AppState.paciente_seleccionado,
                            "Editar Paciente",
                            "Nuevo Paciente"
                        ),
                        style={
                            "font_size": "1.75rem",
                            "font_weight": "700",
                            "color": DARK_THEME["colors"]["text_primary"]
                        }
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
                
                # Indicador de progreso
                form_step_indicator(
                    AppState.paso_formulario_paciente,
                    len(step_titles), 
                    step_titles
                ),
                
                spacing="4",
                width="100%"
            ),
            
            # Contenido del formulario por pasos
            rx.box(
                rx.cond(
                    AppState.paso_formulario_paciente == 0,
                    _patient_form_step_1(),
                    rx.cond(
                        AppState.paso_formulario_paciente == 1,
                        _patient_form_step_2(),
                        _patient_form_step_3()
                    )
                ),
                width="100%",
                min_height="400px"
            ),
            
            # Botones de navegación
            form_navigation_buttons(
                current_step=AppState.paso_formulario_paciente,
                total_steps=len(step_titles),
                on_previous=AppState.retroceder_paso_paciente,
                on_next=AppState.avanzar_paso_paciente,
                on_submit=AppState.guardar_paciente_formulario,
                is_loading=AppState.cargando_operacion,
                can_continue=AppState.puede_continuar_form_paciente
            ),
            
            style={
                "max_width": "800px",
                "width": "90vw",
                "max_height": "90vh",
                "padding": SPACING["8"],
                "border_radius": RADIUS["3xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['primary']['200']}30",
                "overflow_y": "auto"
            }
        ),
        
        open=AppState.modal_crear_paciente_abierto | AppState.modal_editar_paciente_abierto,
        on_open_change=AppState.cerrar_todos_los_modales
    )

def _patient_form_step_1() -> rx.Component:
    """👤 Paso 1: Datos Personales"""
    return rx.vstack(
        form_section_header(
            "Datos Personales",
            "Información básica de identificación del paciente",
            "user",
            COLORS["primary"]["500"]
        ),
        
        # Nombres en grid responsive
        rx.grid(
            enhanced_form_field(
                label="Primer Nombre",
                field_name="primer_nombre",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.primer_nombre, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="Juan",
                required=True,
                icon="user",
                max_length=50,
                validation_error=rx.cond(AppState.errores_validacion_paciente, AppState.errores_validacion_paciente.get("primer_nombre", ""), "")
            ),
            enhanced_form_field(
                label="Segundo Nombre",
                field_name="segundo_nombre", 
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.segundo_nombre, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="Carlos",
                icon="user",
                max_length=50
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        rx.grid(
            enhanced_form_field(
                label="Primer Apellido",
                field_name="primer_apellido",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.primer_apellido, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="Pérez",
                required=True,
                icon="user",
                max_length=50,
                validation_error=rx.cond(AppState.errores_validacion_paciente, AppState.errores_validacion_paciente.get("primer_apellido", ""), "")
            ),
            enhanced_form_field(
                label="Segundo Apellido",
                field_name="segundo_apellido",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.segundo_apellido, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="González",
                icon="user",
                max_length=50
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        # Documento y género
        rx.grid(
            enhanced_form_field(
                label="Tipo de Documento",
                field_name="tipo_documento",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.tipo_documento, ""),
                on_change=AppState.actualizar_campo_paciente,
                field_type="select",
                options=["CI", "Pasaporte"],
                required=True,
                icon="id-card"
            ),
            enhanced_form_field(
                label="Número de Documento",
                field_name="numero_documento",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.numero_documento, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="12345678",
                required=True,
                icon="hash",
                pattern="[0-9]+",
                max_length=20,
                validation_error=rx.cond(AppState.errores_validacion_paciente, AppState.errores_validacion_paciente.get("numero_documento", ""), "")
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        rx.grid(
            enhanced_form_field(
                label="Género",
                field_name="genero",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.genero, ""),
                on_change=AppState.actualizar_campo_paciente,
                field_type="select",
                options=["masculino", "femenino", "otro"],
                icon="users"
            ),
            enhanced_form_field(
                label="Fecha de Nacimiento",
                field_name="fecha_nacimiento",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.fecha_nacimiento, ""),
                on_change=AppState.actualizar_campo_paciente,
                field_type="date",
                icon="calendar"
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        spacing="6",
        width="100%",
        align="stretch"
    )

def _patient_form_step_2() -> rx.Component:
    """📞 Paso 2: Información de Contacto"""
    return rx.vstack(
        form_section_header(
            "Información de Contacto",
            "Datos de contacto y ubicación del paciente",
            "phone",
            COLORS["secondary"]["600"]
        ),
        
        # Contacto principal
        rx.grid(
            enhanced_form_field(
                label="Celular Principal",
                field_name="celular_1",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.celular_1, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="0414-1234567",
                icon="phone",
                help_text="Formato: 0414-1234567"
            ),
            enhanced_form_field(
                label="Celular Secundario",
                field_name="celular_2", 
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.celular_2, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="0424-7654321",
                icon="phone",
                help_text="Opcional - Celular alternativo"
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        # Email
        enhanced_form_field(
            label="Email",
            field_name="email",
            value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.email, ""),
            on_change=AppState.actualizar_campo_paciente,
            field_type="email",
            placeholder="paciente@email.com",
            icon="mail",
            validation_error=rx.cond(AppState.errores_validacion_paciente, AppState.errores_validacion_paciente.get("email", ""), "")
        ),
        
        # Información demográfica
        rx.grid(
            enhanced_form_field(
                label="Ocupación",
                field_name="ocupacion",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.ocupacion, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="Ingeniero, Médico, Estudiante...",
                icon="briefcase"
            ),
            enhanced_form_field(
                label="Estado Civil",
                field_name="estado_civil",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.estado_civil, ""),
                on_change=AppState.actualizar_campo_paciente,
                field_type="select",
                options=["soltero", "casado", "divorciado", "viudo", "unión libre"],
                icon="heart"
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        # Dirección y ubicación
        rx.grid(
            enhanced_form_field(
                label="Ciudad",
                field_name="ciudad",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.ciudad, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="Caracas",
                icon="map-pin"
            ),
            enhanced_form_field(
                label="Departamento/Estado",
                field_name="departamento", 
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.departamento, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="Distrito Capital",
                icon="map"
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        enhanced_form_field(
            label="Dirección Completa",
            field_name="direccion",
            value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.direccion, ""),
            on_change=AppState.actualizar_campo_paciente,
            field_type="textarea",
            placeholder="Calle, número, urbanización...",
            icon="home",
            max_length=500
        ),
        
        # Contacto de emergencia
        form_section_header(
            "Contacto de Emergencia",
            "Persona a contactar en caso de emergencia",
            "triangle-alert",
            COLORS["error"]["500"]
        ),
        
        rx.grid(
            enhanced_form_field(
                label="Nombre Completo",
                field_name="contacto_emergencia_nombre",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.contacto_emergencia_nombre, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="María Pérez",
                icon="user-check",
                max_length=100
            ),
            enhanced_form_field(
                label="Teléfono de Emergencia",
                field_name="contacto_emergencia_telefono",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.contacto_emergencia_telefono, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="0424-7654321",
                icon="phone-call",
                help_text="Disponible 24/7"
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        rx.grid(
            enhanced_form_field(
                label="Relación",
                field_name="contacto_emergencia_relacion",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.contacto_emergencia_relacion, ""),
                on_change=AppState.actualizar_campo_paciente,
                field_type="select",
                options=["Madre", "Padre", "Esposo/a", "Hijo/a", "Hermano/a", "Familiar", "Amigo/a", "Otro"],
                icon="heart"
            ),
            enhanced_form_field(
                label="Dirección del Contacto",
                field_name="contacto_emergencia_direccion",
                value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.contacto_emergencia_direccion, ""),
                on_change=AppState.actualizar_campo_paciente,
                placeholder="Dirección del contacto de emergencia",
                icon="map-pin"
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        spacing="6",
        width="100%",
        align="stretch"
    )

def _patient_form_step_3() -> rx.Component:
    """🏥 Paso 3: Información Médica"""
    return rx.vstack(
        form_section_header(
            "Historia Médica",
            "Información médica relevante para el tratamiento odontológico",
            "heart",
            COLORS["error"]["400"]
        ),
        
        # Alergias y enfermedades
        enhanced_form_field(
            label="Alergias Conocidas",
            field_name="alergias",
            value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.alergias, ""),
            on_change=AppState.actualizar_campo_paciente,
            field_type="textarea",
            placeholder="Penicilina, láter, anestésicos, otros...",
            icon="circle_alert",
            help_text="Especifique cualquier alergia conocida",
            max_length=1000
        ),
        
        enhanced_form_field(
            label="Medicamentos Actuales",
            field_name="medicamentos_actuales",
            value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.medicamentos_actuales, ""),
            on_change=AppState.actualizar_campo_paciente,
            field_type="textarea", 
            placeholder="Aspirina 100mg diaria, Losartán 50mg...",
            icon="pill",
            help_text="Incluya dosis y frecuencia",
            max_length=1000
        ),
        
        enhanced_form_field(
            label="Condiciones Médicas",
            field_name="condiciones_medicas",
            value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.condiciones_medicas, ""),
            on_change=AppState.actualizar_campo_paciente,
            field_type="textarea",
            placeholder="Diabetes, hipertensión, problemas cardíacos...",
            icon="activity",
            help_text="Enfermedades crónicas o condiciones relevantes",
            max_length=1000
        ),
        
        enhanced_form_field(
            label="Antecedentes Familiares",
            field_name="antecedentes_familiares",
            value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.antecedentes_familiares, ""),
            on_change=AppState.actualizar_campo_paciente,
            field_type="textarea",
            placeholder="Historia familiar de enfermedades relevantes...",
            icon="users",
            help_text="Enfermedades hereditarias o familiares importantes",
            max_length=1000
        ),
        
        enhanced_form_field(
            label="Observaciones Médicas Adicionales",
            field_name="observaciones_medicas",
            value=rx.cond(AppState.formulario_paciente, AppState.formulario_paciente.observaciones_medicas, ""),
            on_change=AppState.actualizar_campo_paciente,
            field_type="textarea",
            placeholder="Cualquier información médica relevante...",
            icon="file-text",
            max_length=2000
        ),
        
        spacing="6",
        width="100%",
        align="stretch"
    )

# ==========================================
# 👩‍⚕️ FORMULARIO MULTI-STEP DE PERSONAL
# ==========================================

def multi_step_staff_form() -> rx.Component:
    """👨‍⚕️ Formulario multi-step moderno para crear/editar personal médico"""
    
    step_titles = ["Datos Personales", "Información Profesional", "Configuración de Usuario"]
    
    return rx.dialog.root(
        rx.dialog.content(
            # Header del modal
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        rx.cond(
                            AppState.empleado_seleccionado,
                            "Editar Personal",
                            "Nuevo Personal"
                        ),
                        style={
                            "font_size": "1.75rem",
                            "font_weight": "700",
                            "color": DARK_THEME["colors"]["text_primary"]
                        }
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
                
                # Indicador de progreso
                form_step_indicator(
                    AppState.paso_formulario_personal,
                    len(step_titles), 
                    step_titles
                ),
                
                spacing="4",
                width="100%"
            ),
            
            # Contenido del formulario por pasos
            rx.box(
                rx.cond(
                    AppState.paso_formulario_personal == 0,
                    _staff_form_step_1(),
                    rx.cond(
                        AppState.paso_formulario_personal == 1,
                        _staff_form_step_2(),
                        _staff_form_step_3()
                    )
                ),
                width="100%",
                min_height="400px"
            ),
            
            # Botones de navegación
            form_navigation_buttons(
                current_step=AppState.paso_formulario_personal,
                total_steps=len(step_titles),
                on_previous=AppState.retroceder_paso_personal,
                on_next=AppState.avanzar_paso_personal,
                on_submit=AppState.guardar_personal_formulario,
                is_loading=AppState.cargando_operacion_personal,
                can_continue=AppState.puede_continuar_form_personal
            ),
            
            style={
                "max_width": "800px",
                "width": "90vw",
                "max_height": "90vh",
                "padding": SPACING["8"],
                "border_radius": RADIUS["3xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['secondary']['600']}30",
                "overflow_y": "auto"
            }
        ),
        
        open=AppState.modal_crear_personal_abierto | AppState.modal_editar_personal_abierto,
        on_open_change=AppState.cerrar_todos_los_modales
    )

def _staff_form_step_1() -> rx.Component:
    """👤 Paso 1: Datos Personales del Personal"""
    return rx.vstack(
        form_section_header(
            "Datos Personales",
            "Información básica de identificación del empleado",
            "user",
            COLORS["secondary"]["500"]
        ),
        
        # Nombres en grid responsive
        rx.grid(
            enhanced_form_field(
                label="Primer Nombre",
                field_name="primer_nombre",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.primer_nombre, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="María",
                required=True,
                icon="user",
                max_length=50,
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("primer_nombre", ""), "")
            ),
            enhanced_form_field(
                label="Segundo Nombre",
                field_name="segundo_nombre", 
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.segundo_nombre, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="Esperanza",
                icon="user",
                max_length=50
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        rx.grid(
            enhanced_form_field(
                label="Primer Apellido",
                field_name="primer_apellido",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.primer_apellido, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="García",
                required=True,
                icon="user",
                max_length=50,
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("primer_apellido", ""), "")
            ),
            enhanced_form_field(
                label="Segundo Apellido",
                field_name="segundo_apellido",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.segundo_apellido, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="Rodríguez",
                icon="user",
                max_length=50
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        # Documento y contacto
        rx.grid(
            enhanced_form_field(
                label="Número de Documento",
                field_name="numero_documento",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.numero_documento, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="12345678",
                required=True,
                icon="id-card",
                pattern="[0-9]+",
                max_length=20,
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("numero_documento", ""), "")
            ),
            enhanced_form_field(
                label="Número de Celular",
                field_name="celular",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.celular, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="0424-7654321",
                required=True,
                icon="smartphone",
                help_text="Número de celular requerido",
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("celular", ""), "")
            ),
            enhanced_form_field(
                label="Email Personal (Opcional)",
                field_name="email",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.email, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                field_type="email",
                placeholder="maria.garcia@gmail.com",
                required=False,  # Email personal es opcional
                icon="mail",
                help_text="Email personal de contacto (opcional)",
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("email", ""), "")
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        # Dirección
        enhanced_form_field(
            label="Dirección Completa",
            field_name="direccion",
            value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.direccion, ""),
            on_change=AppState.actualizar_campo_formulario_empleado,
            field_type="textarea",
            placeholder="Calle, número, urbanización, ciudad, estado...",
            icon="map-pin",
            max_length=500
        ),
        
        spacing="6",
        width="100%",
        align="stretch"
    )

def _staff_form_step_2() -> rx.Component:
    """💼 Paso 2: Información Profesional"""
    return rx.vstack(
        form_section_header(
            "Información Profesional",
            "Datos del cargo, especialidad y experiencia",
            "briefcase",
            COLORS["primary"]["500"]
        ),
        
        # Selector visual de rol
        rx.vstack(
            rx.text(
                "Tipo de Personal *",
                style={
                    "font_size": "0.875rem",
                    "font_weight": "600",
                    "color": DARK_THEME["colors"]["text_primary"],
                    "margin_bottom": SPACING["3"]
                }
            ),
            
            # Cards visuales para selección de rol
            rx.grid(
                _role_selection_card("Gerente", "crown", "Administración total del sistema", COLORS["secondary"]["500"]),
                _role_selection_card("Administrador", "settings", "Gestión administrativa", COLORS["blue"]["500"]),
                _role_selection_card("Odontólogo", "stethoscope", "Atención médica especializada", COLORS["success"]["500"]),
                _role_selection_card("Asistente", "user-check", "Apoyo en consultas", COLORS["warning"]["500"]),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="4",
                width="100%"
            ),
            
            spacing="2",
            width="100%"
        ),
        
        # Especialidad (condicional para odontólogos)
        rx.cond(
            rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.tipo_personal, "") == "Odontólogo",
            enhanced_form_field(
                label="Especialidad Odontológica",
                field_name="especialidad",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.especialidad, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                field_type="select",
                options=[
                    "Odontología General",
                    "Endodoncia", 
                    "Ortodoncia",
                    "Periodoncia",
                    "Cirugía Oral",
                    "Odontopediatría",
                    "Prostodoncia",
                    "Estética Dental"
                ],
                icon="award",
                help_text="Especialización principal"
            ),
            rx.box()  # Espacio vacío si no es odontólogo
        ),
        
        # Licencia y experiencia
        rx.grid(
            enhanced_form_field(
                label="Número de Licencia Profesional",
                field_name="numero_colegiatura",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.numero_colegiatura, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="COV-12345",
                icon="badge",
                help_text="Número de colegiatura profesional"
            ),
            columns=rx.breakpoints(initial="1"),
            spacing="4",
            width="100%"
        ),
        
        spacing="6",
        width="100%",
        align="stretch"
    )

def _staff_form_step_3() -> rx.Component:
    """🔐 Paso 3: Configuración de Usuario y Salario"""
    return rx.vstack(
        form_section_header(
            "Configuración de Usuario",
            "Acceso al sistema y información salarial",
            "key",
            COLORS["info"]["500"]
        ),
        
        # Email del sistema y contraseña (solo para usuarios nuevos)
        rx.cond(
            ~AppState.empleado_seleccionado,  # Solo para nuevos usuarios
            rx.vstack(
                enhanced_form_field(
                    label="Email del Sistema",
                    field_name="usuario_email",
                    value=rx.cond(AppState.formulario_empleado, getattr(AppState.formulario_empleado, "usuario_email", ""), ""),
                    on_change=AppState.actualizar_campo_formulario_empleado,
                    field_type="email",
                    placeholder="usuario@clinica.com",
                    required=True,
                    icon="mail",
                    help_text="Email para acceso al sistema",
                    validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("usuario_email", ""), "")
                ),
                enhanced_form_field(
                    label="Contraseña de Acceso",
                    field_name="usuario_password",  # ✅ CORREGIDO: usar nombre real del modelo
                    value=rx.cond(AppState.formulario_empleado, getattr(AppState.formulario_empleado, "usuario_password", ""), ""),
                    on_change=AppState.actualizar_campo_formulario_empleado,
                    field_type="password",
                    placeholder="Mínimo 8 caracteres",
                    required=True,
                    icon="lock",
                    help_text="Contraseña segura con al menos 8 caracteres",
                    validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("usuario_password", ""), "")
                ),
                
                rx.box(
                    rx.hstack(
                        rx.icon("info", size=16, color=COLORS["blue"]["500"]),
                        rx.text(
                            "El empleado podrá cambiar su contraseña después del primer acceso.",
                            style={
                                "font_size": "0.75rem",
                                "color": COLORS["blue"]["600"],
                                "font_style": "italic"
                            }
                        ),
                        spacing="2",
                        align="center"
                    ),
                    style={
                        "background": COLORS["blue"]["50"],
                        "border": f"1px solid {COLORS['blue']['200']}",
                        "border_radius": RADIUS["lg"],
                        "padding": SPACING["3"],
                        "margin_top": SPACING["2"]
                    }
                ),
                
                spacing="3",
                width="100%"
            ),
            rx.box()  # Espacio vacío para usuarios existentes
        ),
        
        # Información salarial
        form_section_header(
            "Información Salarial",
            "Salario base y comisiones del empleado",
            "dollar-sign",
            COLORS["success"]["500"]
        ),
        
        rx.grid(
            enhanced_form_field(
                label="Salario Base Mensual (Bs.)",
                field_name="salario",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.salario, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                field_type="number",
                placeholder="500.00",
                icon="dollar-sign",
                help_text="Salario fijo mensual en bolívares"
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        # Fecha de ingreso
        enhanced_form_field(
            label="Fecha de Ingreso",
            field_name="fecha_ingreso",
            value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.fecha_ingreso, ""),
            on_change=AppState.actualizar_campo_formulario_empleado,
            field_type="date",
            icon="calendar",
            help_text="Fecha de inicio en la empresa"
        ),
        
        # Resumen del usuario a crear
        rx.cond(
            AppState.formulario_empleado & (AppState.formulario_empleado.tipo_personal != ""),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("user-plus", size=20, color=COLORS["primary"]["500"]),
                        rx.text(
                            "Resumen del Usuario",
                            style={
                                "font_size": "1rem",
                                "font_weight": "600",
                                "color": COLORS["primary"]["600"]
                            }
                        ),
                        spacing="2",
                        align="center"
                    ),
                    
                    rx.text(
                        f"Se creará un usuario {rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.tipo_personal, '')} con acceso al sistema odontológico.",
                        style={
                            "font_size": "0.875rem",
                            "color": COLORS["gray"]["600"],
                            "line_height": "1.4"
                        }
                    ),
                    
                    spacing="3"
                ),
                style={
                    "background": f"linear-gradient(135deg, {COLORS['primary']['50']} 0%, {COLORS['primary']['100']} 100%)",  # primary 100 existe
                    "border": f"1px solid {COLORS['primary']['200']}",
                    "border_radius": RADIUS["xl"],
                    "padding": SPACING["4"],
                    "margin_top": SPACING["4"]
                }
            ),
            rx.box()
        ),
        
        spacing="6",
        width="100%",
        align="stretch"
    )

def service_form_modal() -> rx.Component:
    """🏥 Modal simple para crear/editar servicios (patrón Personal/Pacientes)"""

    return rx.dialog.root(
        rx.dialog.content(
            # Header del modal
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        rx.cond(
                            AppState.servicio_seleccionado_valido,
                            "Editar Servicio",
                            "Nuevo Servicio"
                        ),
                        style={
                            "font_size": "1.75rem",
                            "font_weight": "700",
                            "color": DARK_THEME["colors"]["text_primary"]
                        }
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
                            },
                            on_click=AppState.limpiar_formulario_servicio
                        )
                    ),
                    width="100%",
                    align="center"
                ),

                # Formulario completo en una sola página
                service_form_fields(),

                # Botones de acción
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        style={
                            **GLASS_EFFECTS["light"],
                            "border": f"1px solid {COLORS['gray']['300']}60",
                            "color": COLORS["gray"]["700"],
                            "border_radius": RADIUS["xl"],
                            "padding": f"{SPACING['3']} {SPACING['6']}",
                            "font_weight": "600",
                            "transition": ANIMATIONS["presets"]["crystal_hover"],
                            "_hover": {
                                **GLASS_EFFECTS["medium"],
                                "transform": "translateY(-2px)",
                                "box_shadow": SHADOWS["crystal_sm"]
                            }
                        },
                        on_click=lambda: [AppState.limpiar_formulario_servicio(), AppState.cerrar_todos_los_modales()],
                    ),
                    rx.button(
                        rx.cond(
                            AppState.cargando_operacion_servicio,
                            rx.hstack(
                                rx.spinner(size="1"),
                                rx.text(rx.cond(AppState.servicio_seleccionado_valido, "Guardando...", "Creando..."), size="2"),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.icon("save", size=16),
                                rx.text(rx.cond(AppState.servicio_seleccionado_valido, "Guardar Cambios", "Crear Servicio"), size="2"),
                                spacing="2"
                            )
                        ),
                        on_click=rx.cond(
                            AppState.servicio_seleccionado_valido,
                            AppState.actualizar_servicio,
                            AppState.crear_servicio
                        ),
                        style={
                            "background": GRADIENTS["neon_primary"],
                            "color": "white",
                            "border": "none",
                            "border_radius": RADIUS["xl"],
                            "padding": f"{SPACING['3']} {SPACING['6']}",
                            "font_weight": "700",
                            "box_shadow": SHADOWS["glow_primary"],
                            "transition": ANIMATIONS["presets"]["crystal_hover"],
                            "_hover": {
                                "transform": "translateY(-2px) scale(1.02)",
                                "box_shadow": f"0 0 30px {COLORS['primary']['500']}50, 0 8px 16px {COLORS['primary']['500']}30"
                            }
                        },
                        disabled=AppState.cargando_operacion_servicio
                    ),
                    spacing="3",
                    justify="end",
                    width="100%"
                ),

                spacing="6",
                width="100%"
            ),

            style={
                "max_width": "700px",
                "width": "85vw",
                "max_height": "85vh",
                "padding": SPACING["8"],
                "border_radius": RADIUS["3xl"],
                **GLASS_EFFECTS["strong"],
                "box_shadow": SHADOWS["2xl"],
                "border": f"1px solid {COLORS['primary']['500']}30",
                "overflow_y": "auto"
            }
        ),

        open=AppState.modal_crear_servicio_abierto | AppState.modal_editar_servicio_abierto,
        on_open_change=AppState.cerrar_todos_los_modales
    )

def service_form_fields() -> rx.Component:
    """📝 Campos del formulario de servicio (todo en una página)"""
    return rx.vstack(
        # Información Básica
        form_section_header(
            "Información Básica",
            "Datos fundamentales del servicio odontológico",
            "info",
            COLORS["primary"]["500"]
        ),

        # Código y Nombre en grid
        rx.grid(
            enhanced_form_field(
                label="Código del Servicio",
                field_name="codigo",
                value= AppState.formulario_servicio.codigo,
                on_change=AppState.actualizar_campo_formulario_servicio,
                placeholder="SER015",
                required=True,
                icon="hash",
                max_length=10,
                validation_error=rx.cond(AppState.errores_validacion_servicio, AppState.errores_validacion_servicio.get("codigo", ""), "")
            ),
            enhanced_form_field(
                label="Nombre del Servicio",
                field_name="nombre",
                value=AppState.formulario_servicio.nombre,
                on_change=AppState.actualizar_campo_formulario_servicio,
                placeholder="Ej: Limpieza profunda",
                required=True,
                icon="clipboard",
                max_length=100,
                validation_error=rx.cond(AppState.errores_validacion_servicio, AppState.errores_validacion_servicio.get("nombre", ""), "")
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),

        # Descripción
        enhanced_form_field(
            label="Descripción",
            field_name="descripcion",
            value=AppState.formulario_servicio.descripcion,
            on_change=AppState.actualizar_campo_formulario_servicio,
            field_type="textarea",
            placeholder="Descripción detallada del servicio...",
            required=False,
            icon="file-text"
        ),

        # Categoría y Precios
        form_section_header(
            "Categoría y Precios",
            "Clasificación y costos del servicio",
            "tag",
            COLORS["secondary"]["500"]
        ),

        # Categoría
        enhanced_form_field_select(
            label="Categoría",
            field_name="categoria",
            value=AppState.formulario_servicio.categoria,
            on_change=AppState.actualizar_campo_formulario_servicio,
            options=AppState.categorias_servicios,
            placeholder="Seleccionar categoría",
            required=True,
            icon="grid"
        ),

        # Alcance del Servicio
        enhanced_form_field_select(
            label="Alcance del Servicio",
            field_name="alcance_servicio",
            value=AppState.formulario_servicio.alcance_servicio,
            on_change=AppState.actualizar_campo_formulario_servicio,
            options=["superficie_especifica", "diente_completo", "boca_completa"],
            placeholder="Seleccionar alcance",
            required=True,
            icon="target",
            help_text="Superficie específica: una cara del diente | Diente completo: todo el diente | Boca completa: todo el odontograma"
        ),

        # Precio Base USD
        enhanced_form_field(
            label="Precio Base USD",
            field_name="precio_base_usd",
            value=AppState.formulario_precio_usd_value,
            on_change=AppState.actualizar_campo_formulario_servicio,
            field_type="number",
            placeholder="50.00",
            required=True,
            icon="dollar-sign",
            help_text="El precio en Bolívares se calculará automáticamente usando la tasa de cambio actual",
            validation_error=rx.cond(AppState.errores_validacion_servicio, AppState.errores_validacion_servicio.get("precio_base_usd", ""), "")
        ),

        # Material incluido
        enhanced_form_field(
            label="Material Incluido",
            field_name="material_incluido",
            value=AppState.formulario_servicio.material_incluido,
            on_change=AppState.actualizar_campo_formulario_servicio,
            placeholder="Ej: Amalgama, anestesia local",
            icon="package"
        ),

        # ==========================================
        # 🦷 V3.0: CONDICIÓN DENTAL RESULTANTE
        # ==========================================
        form_section_header(
            "Condición Dental Resultante",
            "¿Este servicio modifica el odontograma del paciente?",
            "tooth",
            COLORS["success"]["500"]
        ),

        rx.vstack(
            rx.text(
                "Si el servicio modifica la condición de un diente, selecciona la condición resultante. "
                "Los servicios preventivos (limpiezas, consultas) no modifican el odontograma.",
                style={
                    "font_size": "0.9rem",
                    "color": COLORS["gray"]["400"],
                    "line_height": "1.5",
                    "margin_bottom": SPACING["3"]
                }
            ),
            enhanced_form_field_select(
                label="Condición Resultante",
                field_name="condicion_resultante",
                value=AppState.formulario_servicio.condicion_resultante,
                on_change=AppState.actualizar_campo_formulario_servicio,
                options=[
                    "",  # Preventivo (sin condición)
                    "sano",
                    "caries",
                    "obturacion",
                    "endodoncia",
                    "corona",
                    "puente",
                    "implante",
                    "protesis",
                    "ausente",
                    "fractura",
                    "extraccion_indicada"
                ],
                placeholder="Preventivo (no modifica)",
                required=False,
                icon="activity",
                help_text="Deja vacío para servicios preventivos"
            ),
            spacing="3",
            width="100%"
        ),

        # Mostrar errores
        rx.cond(
            AppState.errores_validacion_servicio,
            rx.vstack(
                rx.foreach(
                    AppState.errores_validacion_servicio,
                    lambda error: rx.text(
                        error,
                        size="2",
                        color=COLORS["error"]["500"]
                    )
                ),
                spacing="1",
                width="100%"
            )
        ),

        spacing="6",
        width="100%",
        align="stretch"
    )

def enhanced_form_field_select(
    label: str,
    field_name: str,
    value: Any,
    on_change: Callable,
    options: List[str],
    placeholder: str = "",
    required: bool = False,
    validation_error: str = "",
    help_text: str = "",
    icon: Optional[str] = None
) -> rx.Component:
    """📝 Campo select mejorado para formularios"""

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
                *([rx.text("*", color=COLORS["error"]["500"], font_weight="bold")] if required else []),
                spacing="2",
                align="center"
            ),
            spacing="2",
            align="center"
        ),

        # Select field
        rx.select(
            options,
            value=value,
            on_change=lambda v: on_change(field_name, v),
            placeholder=placeholder,
            style={
                "width": "100%",
                "min_height": "44px",
                "background": DARK_THEME["colors"]["surface_secondary"],
                "border": f"2px solid {COLORS['error']['300'] if validation_error else DARK_THEME['colors']['border']}",
                "border_radius": RADIUS["lg"],
                "padding": f"0 {SPACING['4']}",
                "font_size": "1rem",
                "color": DARK_THEME["colors"]["text_primary"],
                "transition": "all 200ms ease",
                "_focus": {
                    "border_color": COLORS["primary"]["400"],
                    "box_shadow": f"0 0 0 3px {COLORS['primary']['100']}"
                }
            }
        ),

        # Texto de ayuda y errores
        rx.cond(
            validation_error != "",
            rx.text(
                validation_error,
                style={
                    "font_size": "0.875rem",
                    "color": COLORS["error"]["500"],
                    "margin_top": SPACING["1"]
                }
            ),
            rx.cond(
                help_text != "",
                rx.text(
                    help_text,
                    style={
                        "font_size": "0.875rem",
                        "color": DARK_THEME["colors"]["text_secondary"],
                        "margin_top": SPACING["1"]
                    }
                ),
                rx.box()
            )
        ),

        spacing="2",
        width="100%",
        align="stretch"
    )

def _role_selection_card(role: str, icon: str, description: str, color: str) -> rx.Component:
    """👤 Card visual para selección de rol del personal"""
    is_selected = rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.tipo_personal, "") == role

    return rx.box(
        rx.vstack(
            # Icono del rol
            rx.box(
                rx.icon(icon, size=32, color=rx.cond(is_selected, "white", color)),
                style={
                    "width": "60px",
                    "height": "60px",
                    "border_radius": "50%",
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center",
                    "background": rx.cond(
                        is_selected,
                        color,
                        f"{color}15"
                    ),
                    "border": f"2px solid {color}",
                    "transition": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)"
                }
            ),
            
            # Título del rol
            rx.text(
                role,
                style={
                    "font_size": "1rem",
                    "font_weight": "700",
                    "color": rx.cond(is_selected, color, COLORS["gray"]["800"]),
                    "text_align": "center"
                }
            ),
            
            # Descripción
            rx.text(
                description,
                style={
                    "font_size": "0.75rem",
                    "color": COLORS["gray"]["600"],
                    "text_align": "center",
                    "line_height": "1.3"
                }
            ),
            
            spacing="3",
            align="center",
            padding=SPACING["4"]
        ),
        
        style={
            "border": rx.cond(
                is_selected,
                f"2px solid {color}",
                f"2px solid {COLORS['gray']['200']}"
            ),
            "border_radius": RADIUS["xl"],
            "background": rx.cond(
                is_selected,
                f"linear-gradient(135deg, {color}10 0%, {color}05 100%)",
                "white"
            ),
            "cursor": "pointer",
            "transition": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)",
            "box_shadow": rx.cond(
                is_selected,
                f"0 0 0 3px {color}20, 0 4px 12px {color}15",
                SHADOWS["sm"]
            ),
            "_hover": {
                "transform": "translateY(-2px)",
                "box_shadow": rx.cond(
                    is_selected,
                    f"0 0 0 3px {color}30, 0 6px 16px {color}25",
                    SHADOWS["md"]
                ),
                "border_color": color
            }
        },
        
        on_click=lambda: AppState.actualizar_campo_formulario_empleado("tipo_personal", role),
        width="100%"
    )

# ==========================================
# 🎨 COMPONENTES DE VALIDACIÓN VISUAL
# ==========================================

def validation_indicator(value: str, validation_rules: List[str]) -> rx.Component:
    """✅ Indicador visual de validación en tiempo real"""
    
    def check_rule(rule: str, val: str) -> bool:
        """Verificar regla de validación"""
        if rule == "required":
            return bool(val.strip())
        elif rule == "email":
            return "@" in val and "." in val.split("@")[-1] if val else False
        elif rule == "phone":
            return bool(re.match(r'^\d{4}-\d{7}$', val)) if val else False
        elif rule == "min_8":
            return len(val) >= 8 if val else False
        elif rule == "numbers_only":
            return val.isdigit() if val else False
        return True
    
    return rx.vstack(
        *[
            rx.hstack(
                rx.icon(
                    "check" if check_rule(rule, value) else "x",
                    size=14,
                    color=COLORS["success"]["500"] if check_rule(rule, value) else COLORS["error"]["400"]
                ),
                rx.text(
                    _get_rule_text(rule),
                    style={
                        "font_size": "0.75rem",
                        "color": COLORS["success"]["600"] if check_rule(rule, value) else COLORS["gray"]["500"]
                    }
                ),
                spacing="2",
                align="center"
            ) for rule in validation_rules
        ],
        spacing="1",
        margin_top="2"
    )

def _get_rule_text(rule: str) -> str:
    """Obtener texto descriptivo para la regla"""
    rule_texts = {
        "required": "Campo obligatorio",
        "email": "Formato de email válido",
        "phone": "Formato: 0414-1234567",
        "min_8": "Mínimo 8 caracteres",
        "numbers_only": "Solo números"
    }
    return rule_texts.get(rule, rule)

def smart_input_with_validation(
    label: str,
    field_name: str,
    value: Any,
    on_change: Callable,
    field_type: str = "text",
    validation_rules: List[str] = None,
    placeholder: str = "",
    icon: Optional[str] = None,
    help_text: str = ""
) -> rx.Component:
    """📝 Input inteligente con validación en tiempo real y ayuda contextual"""
    
    validation_rules = validation_rules or []
    
    return rx.vstack(
        # Label con tooltip de ayuda
        rx.hstack(
            rx.hstack(
                *([rx.icon(icon, size=16, color=COLORS["primary"]["500"])] if icon else []),
                rx.text(
                    label,
                    style={
                        "font_size": "0.875rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                *([rx.text("*", color=COLORS["error"]["500"], font_weight="700")] if "required" in validation_rules else []),
                spacing="2",
                align="center"
            ),
            
            rx.spacer(),
            
            # Ayuda contextual
            *([
                rx.box(
                    rx.icon("help-circle", size=14, color=COLORS["gray"]["400"]),
                    style={
                        "cursor": "help",
                        "_hover": {"color": COLORS["primary"]["500"]}
                    }
                )
            ] if help_text else []),
            
            width="100%",
            align="center"
        ),
        
        # Campo de entrada
        rx.input(
            type=field_type,
            value=value,
            on_change=lambda v: on_change(field_name, v),
            placeholder=placeholder,
            style={
                "width": "100%",
                "padding": f"{SPACING['3']} {SPACING['4']}",
                "border_radius": RADIUS["lg"],
                "font_size": "1rem",
                "background": "rgba(255, 255, 255, 0.95)",
                "border": f"2px solid {COLORS['gray']['200']}",
                "transition": "all 250ms cubic-bezier(0.4, 0, 0.2, 1)",
                "_focus": {
                    "outline": "none",
                    "border_color": COLORS["primary"]["400"],
                    "box_shadow": f"0 0 0 3px {COLORS['primary']['100']}",
                    "background": "white"
                }
            }
        ),
        
        # Validación en tiempo real
        rx.cond(
            len(validation_rules) > 0,
            validation_indicator(value, validation_rules),
            rx.box()
        ),
        
        # Texto de ayuda
        rx.cond(
            help_text != "",
            rx.text(
                help_text,
                style={
                    "font_size": "0.75rem",
                    "color": COLORS["gray"]["500"],
                    "font_style": "italic",
                    "margin_top": "2px"
                }
            ),
            rx.box()
        ),
        
        spacing="2",
        width="100%",
        align="start"
    )

# ==========================================
# 📱 COMPONENTES RESPONSIVE AVANZADOS
# ==========================================

def responsive_form_grid(*fields) -> rx.Component:
    """📱 Grid responsive inteligente para formularios"""
    return rx.grid(
        *fields,
        columns=rx.breakpoints(
            initial="1",      # Móvil: 1 columna
            sm="1",          # Móvil grande: 1 columna  
            md="2",          # Tablet: 2 columnas
            lg="2",          # Desktop: 2 columnas
            xl="3"           # Desktop grande: 3 columnas (solo si hay 3+ campos)
        ),
        spacing="4",
        width="100%"
    )

def mobile_optimized_section(title: str, icon: str, *content) -> rx.Component:
    """📱 Sección optimizada para móviles con collapse"""
    return rx.box(
        rx.vstack(
            # Header colapsable en móvil
            rx.hstack(
                rx.icon(icon, size=20, color=COLORS["primary"]["500"]),
                rx.heading(
                    title,
                    style={
                        "font_size": ["1.25rem", "1.5rem"],  # Responsive font
                        "font_weight": "700",
                        "color": DARK_THEME["colors"]["text_primary"]
                    }
                ),
                spacing="3",
                align="center",
                width="100%"
            ),
            
            # Contenido de la sección
            rx.vstack(
                *content,
                spacing="4",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        
        style={
            "background": "rgba(255, 255, 255, 0.05)",
            "border": f"1px solid {COLORS['gray']['200']}30",
            "border_radius": RADIUS["xl"],
            "padding": [SPACING["4"], SPACING["6"]],  # Responsive padding
            "margin_bottom": SPACING["4"]
        },
        width="100%"
    )

def form_progress_bar(current_step: int, total_steps: int) -> rx.Component:
    """📊 Barra de progreso minimalista para móviles"""
    progress_percentage = ((current_step + 1) / total_steps) * 100
    
    return rx.vstack(
        # Barra de progreso
        rx.box(
            rx.box(
                style={
                    "width": f"{progress_percentage}%",
                    "height": "4px",
                    "background": GRADIENTS["neon_primary"],
                    "border_radius": "2px",
                    "transition": "width 0.3s ease"
                }
            ),
            style={
                "width": "100%",
                "height": "4px",
                "background": COLORS["gray"]["200"],
                "border_radius": "2px",
                "overflow": "hidden"
            }
        ),
        
        # Texto de progreso
        rx.text(
            f"Paso {current_step + 1} de {total_steps}",
            style={
                "font_size": "0.75rem",
                "color": COLORS["gray"]["500"],
                "text_align": "center",
                "margin_top": "4px"
            }
        ),
        
        spacing="1",
        width="100%",
        align="center"
    )

# ==========================================
# 🎯 COMPONENTES DE FEEDBACK VISUAL
# ==========================================

def success_feedback(message: str, icon: str = "check") -> rx.Component:
    """✅ Feedback de éxito animado"""
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=20, color=COLORS["success"]["500"]),
            rx.text(
                message,
                style={
                    "color": COLORS["success"]["600"],
                    "font_weight": "600",
                    "font_size": "0.875rem"
                }
            ),
            spacing="3",
            align="center"
        ),
        style={
            "background": f"linear-gradient(135deg, {COLORS['success']['50']} 0%, {COLORS['success']['25']} 100%)",
            "border": f"1px solid {COLORS['success']['200']}",
            "border_radius": RADIUS["lg"],
            "padding": f"{SPACING['3']} {SPACING['4']}",
            "animation": "fadeIn 0.3s ease-in-out"
        }
    )

def loading_feedback(message: str = "Procesando...") -> rx.Component:
    """⏳ Feedback de carga animado"""
    return rx.box(
        rx.hstack(
            rx.spinner(size="3", color=COLORS["primary"]["500"]),
            rx.text(
                message,
                style={
                    "color": COLORS["primary"]["600"],
                    "font_weight": "500",
                    "font_size": "0.875rem"
                }
            ),
            spacing="3",
            align="center"
        ),
        style={
            "background": f"linear-gradient(135deg, {COLORS['primary']['50']} 0%, {COLORS['primary']['100']} 100%)",
            "border": f"1px solid {COLORS['primary']['200']}",
            "border_radius": RADIUS["lg"],
            "padding": f"{SPACING['3']} {SPACING['4']}"
        }
    )
