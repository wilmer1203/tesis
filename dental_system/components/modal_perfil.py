import reflex as rx
from ..components.common import primary_button,secondary_button,modal_wrapper
from ..components.forms import enhanced_form_field
from ..styles.themes import COLORS
from ..state.app_state import AppState

# ========================================
# COMPONENTES - MODALES
# ========================================

def modal_cambiar_password() -> rx.Component:
    """Modal para cambiar contraseña con estilo glassmorphism"""
    return modal_wrapper(
        title="Cambiar Contraseña",
        subtitle="Actualiza tu contraseña para mayor seguridad",
        icon="lock",
        color=COLORS["warning"]["500"],
        is_open=AppState.modal_cambio_password_abierto,
        on_open_change=AppState.cerrar_modal_cambio_password,
        children=rx.vstack(
            # Formulario con enhanced_form_field
            rx.vstack(
                # Contraseña actual
                enhanced_form_field(
                    label="Contraseña Actual",
                    field_name="current_password",
                    value=AppState.current_password,
                    on_change=lambda field, value: AppState.set_current_password(value),
                    field_type="password",
                    placeholder="Ingresa tu contraseña actual",
                    required=True,
                    icon="key",
                    validation_error=AppState.errores_password.get("current_password", "")
                ),

                # Nueva contraseña
                enhanced_form_field(
                    label="Nueva Contraseña",
                    field_name="new_password",
                    value=AppState.new_password,
                    on_change=lambda field, value: AppState.set_new_password(value),
                    field_type="password",
                    placeholder="Mínimo 6 caracteres",
                    required=True,
                    icon="lock",
                    help_text="Mínimo 6 caracteres",
                    validation_error=AppState.errores_password.get("new_password", "")
                ),

                # Confirmar nueva contraseña
                enhanced_form_field(
                    label="Confirmar Nueva Contraseña",
                    field_name="confirm_password",
                    value=AppState.confirm_password,
                    on_change=lambda field, value: AppState.set_confirm_password(value),
                    field_type="password",
                    placeholder="Repite la nueva contraseña",
                    required=True,
                    icon="shield-check",
                    validation_error=AppState.errores_password.get("confirm_password", "")
                ),

                spacing="4",
                width="100%"
            ),

            # Botones de acción
            rx.hstack(
                rx.dialog.close(
                    secondary_button(
                        "Cancelar",
                        icon="x",
                        on_click=AppState.cerrar_modal_cambio_password
                    )
                ),
                primary_button(
                    "Cambiar Contraseña",
                    icon="check",
                    on_click=AppState.confirmar_cambio_password,
                    loading=AppState.cambiando_password
                ),
                spacing="3",
                width="100%",
                justify="end"
            ),

            spacing="6",
            width="100%"
        )
    )



def modal_cambiar_email() -> rx.Component:
    """Modal para cambiar email con estilo glassmorphism"""
    return modal_wrapper(
        title="Cambiar Email",
        subtitle="Actualiza tu email de acceso al sistema",
        icon="mail",
        color=COLORS["blue"]["500"],
        is_open=AppState.modal_cambio_email_abierto,
        on_open_change=AppState.cerrar_modal_cambio_email,
        children=rx.vstack(
            # Warning callout
            rx.callout(
                "Deberás verificar tu nuevo email antes del próximo inicio de sesión",
                icon="alert-triangle",
                color_scheme="orange",
                size="1",
                width="100%"
            ),

            # Formulario con enhanced_form_field
            rx.vstack(
                # Nuevo email
                enhanced_form_field(
                    label="Nuevo Email",
                    field_name="new_email",
                    value=AppState.new_email,
                    on_change=lambda field, value: AppState.set_new_email(value),
                    field_type="email",
                    placeholder="nuevo@email.com",
                    required=True,
                    icon="mail",
                    validation_error=AppState.errores_email.get("new_email", "")
                ),

                # Contraseña actual (para confirmar)
                enhanced_form_field(
                    label="Contraseña Actual",
                    field_name="password_for_email",
                    value=AppState.password_for_email,
                    on_change=lambda field, value: AppState.set_password_for_email(value),
                    field_type="password",
                    placeholder="Ingresa tu contraseña",
                    required=True,
                    icon="key",
                    help_text="Para confirmar tu identidad",
                    validation_error=AppState.errores_email.get("password", "")
                ),

                spacing="4",
                width="100%"
            ),

            # Botones de acción
            rx.hstack(
                rx.dialog.close(
                    secondary_button(
                        "Cancelar",
                        icon="x",
                        on_click=AppState.cerrar_modal_cambio_email
                    )
                ),
                primary_button(
                    "Cambiar Email",
                    icon="check",
                    on_click=AppState.confirmar_cambio_email,
                    loading=AppState.cambiando_email
                ),
                spacing="3",
                width="100%",
                justify="end"
            ),

            spacing="6",
            width="100%"
        )
    )

