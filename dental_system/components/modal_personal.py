import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.forms import (
    form_step_indicator, form_navigation_buttons, form_section_header,
    enhanced_form_field, _role_selection_card, validated_input, select_input_combo
)
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING, GLASS_EFFECTS, DARK_THEME



# ==========================================
# 👩‍⚕️ FORMULARIO MULTI-STEP DE PERSONAL
# ==========================================

def multi_step_staff_form() -> rx.Component:
    """👨‍⚕️ Formulario multi-step moderno para crear/editar personal médico"""

    step_titles = ["Datos Personales", "Información Profesional y Usuario"]

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

                spacing="3",
                width="100%"
            ),

            # Contenido del formulario por pasos
            rx.box(
                rx.cond(
                    AppState.paso_formulario_personal == 0,
                    _staff_form_step_1(),
                    _staff_form_step_2_unified()
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
                can_continue=AppState.puede_continuar_form_personal,
                submit_text=rx.cond(
                    AppState.empleado_seleccionado,
                    "Actualizar Personal",
                    "Crear Personal"
                ),
                submit_icon=rx.cond(
                    AppState.empleado_seleccionado,
                    "edit",
                    "user-plus"
                )
            ),
            
            style={
                "max_width": "700px",
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
        
        # Nombres en grid responsive (SOLO LETRAS - Componente genérico)
        rx.grid(
            validated_input(
                label="Primer Nombre",
                field_name="primer_nombre",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.primer_nombre, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                input_type="text",
                validation_mode="letters_only",
                placeholder="María",
                required=True,
                icon="user",
                max_length=50,
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("primer_nombre", ""), "")
            ),
            validated_input(
                label="Segundo Nombre",
                field_name="segundo_nombre",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.segundo_nombre, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                input_type="text",
                validation_mode="letters_only",
                placeholder="Esperanza",
                icon="user",
                max_length=50
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),

        rx.grid(
            validated_input(
                label="Primer Apellido",
                field_name="primer_apellido",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.primer_apellido, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                input_type="text",
                validation_mode="letters_only",
                placeholder="García",
                required=True,
                icon="user",
                max_length=50,
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("primer_apellido", ""), "")
            ),
            validated_input(
                label="Segundo Apellido",
                field_name="segundo_apellido",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.segundo_apellido, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                input_type="text",
                validation_mode="letters_only",
                placeholder="Rodríguez",
                icon="user",
                max_length=50
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),
        
        rx.grid(
            select_input_combo(
                label="Documento de Identidad",
                field_name_select="tipo_documento",
                field_name_input="numero_documento",
                value_select=rx.cond(AppState.formulario_empleado, AppState.formulario_paciente.tipo_documento, "CI"),
                value_input=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.numero_documento, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                select_options=["CI", "Pasaporte"],
                select_default="CI",
                input_type="number",
                input_placeholder="12345678",
                select_width="90px",
                required=True,
                icon="id-card",
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("numero_documento", ""), "")
            ),
            # Celular (CÓDIGO PAÍS + NÚMERO - Componente genérico)
            select_input_combo(
                label="Número de Celular",
                field_name_select="codigo_pais_celular",
                field_name_input="celular",
                value_select=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.codigo_pais_celular, "+58"),
                value_input=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.celular, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                select_options=["+58", "+1", "+52", "+57", "+51", "+54", "+56", "+55", "+34"],
                select_default="+58",
                input_type="number",
                input_placeholder="4241234567",
                required=True,
                icon="smartphone",
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("celular", ""), "")
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
        
        spacing="4",
        width="100%",
        align="stretch"
    )

def _staff_form_step_2_unified() -> rx.Component:
    """💼 Paso 2 UNIFICADO: Información Profesional + Usuario"""
    return rx.vstack(
        form_section_header(
            "Información Profesional y Acceso",
            "Datos del cargo, especialidad y configuración de usuario",
            "briefcase",
            COLORS["primary"]["500"]
        ),

        # Tipo de Personal - SELECT COMPACTO
        rx.grid(
            enhanced_form_field(
                label="Tipo de Personal",
                field_name="tipo_personal",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.tipo_personal, "Odontólogo"),
                on_change=AppState.actualizar_campo_formulario_empleado,
                field_type="select",
                options=["Gerente", "Administrador", "Odontólogo", "Asistente"],
                required=True,
                icon="user-cog",
                validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("tipo_personal", ""), "")
            ),

            # Número de Licencia Profesional
            enhanced_form_field(
                label="Número de Licencia Profesional",
                field_name="numero_colegiatura",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.numero_colegiatura, ""),
                on_change=AppState.actualizar_campo_formulario_empleado,
                placeholder="COV-12345",
                icon="badge",
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%"
        ),

        # Especialidad (condicional para odontólogos)
        rx.cond(
            rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.tipo_personal, "") == "Odontólogo",
            enhanced_form_field(
                label="Especialidad Odontológica",
                field_name="especialidad",
                value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.especialidad, "Odontología General"),
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
                help_text="Predeterminado: Odontología General"
            ),
            rx.box()
        ),

        # Sección Usuario (solo para nuevos)
        rx.cond(
            ~AppState.empleado_seleccionado,
            rx.vstack(
                rx.divider(margin_y="4"),

                rx.text(
                    "Configuración de Acceso",
                    style={
                        "font_size": "1rem",
                        "font_weight": "600",
                        "color": DARK_THEME["colors"]["text_primary"],
                        "margin_bottom": SPACING["2"]
                    }
                ),

                rx.grid(
                    enhanced_form_field(
                        label="Email del Sistema",
                        field_name="usuario_email",
                        value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.usuario_email, ""),
                        on_change=AppState.actualizar_campo_formulario_empleado,
                        field_type="email",
                        placeholder="usuario@clinica.com",
                        required=True,
                        icon="mail",
                        validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("usuario_email", ""), "")
                    ),
                    enhanced_form_field(
                        label="Contraseña de Acceso",
                        field_name="usuario_password",
                        value=rx.cond(AppState.formulario_empleado, AppState.formulario_empleado.usuario_password, ""),
                        on_change=AppState.actualizar_campo_formulario_empleado,
                        field_type="password",
                        placeholder="Mínimo 8 caracteres",
                        required=True,
                        icon="lock",
                        validation_error=rx.cond(AppState.errores_validacion_empleado, AppState.errores_validacion_empleado.get("usuario_password", ""), "")
                    ),
                    columns=rx.breakpoints(initial="1", sm="2"),
                    spacing="4",
                    width="100%"
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
                        "background": f"{COLORS['blue']['900']}10",
                        "border": f"1px solid {COLORS['blue']['500']}30",
                        "border_radius": RADIUS["lg"],
                        "padding": SPACING["3"],
                        "margin_top": SPACING["2"]
                    }
                ),

                spacing="3",
                width="100%"
            ),
            rx.box()
        ),

        spacing="4",
        width="100%",
        align="stretch"
    )
