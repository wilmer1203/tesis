
import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.forms import form_step_indicator ,form_navigation_buttons,form_section_header,enhanced_form_field
from dental_system.styles.themes import COLORS, SHADOWS, RADIUS, SPACING, GLASS_EFFECTS, DARK_THEME

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