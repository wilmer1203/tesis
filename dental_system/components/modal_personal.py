import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.forms import form_step_indicator ,form_navigation_buttons,form_section_header,enhanced_form_field,_role_selection_card
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING, GLASS_EFFECTS, DARK_THEME



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
