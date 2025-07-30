
import reflex as rx
from dental_system.state.auth_state import AuthState

def login_form() -> rx.Component:
    """Formulario de inicio de sesión con debug y mensajes en español"""
    print("[DEBUG] Renderizando formulario de login...")
    
    return rx.box(
        rx.vstack(
            # Logo y título principal
            rx.center(
                rx.image(
                    src="/logo.png",
                    width="120px",
                    height="120px",
                    border_radius="50%",
                    alt="Logo Clínica Dental"
                ),
            ),
            rx.heading(
                "Sistema Odontológico",
                size="9",
                text_align="center",
                color="#1CBBBA",
                margin_bottom="2rem"
            ),
            
            # Mensajes de error y éxito
            rx.cond(
                AuthState.error_message != "",
                rx.callout(
                    AuthState.error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                    margin_bottom="1rem"
                )
            ),
            rx.cond(
                AuthState.success_message != "",
                rx.callout(
                    AuthState.success_message,
                    icon="check",
                    color_scheme="green",
                    role="status",
                    margin_bottom="1rem"
                )
            ),
            
            # Formulario
            rx.form(
                rx.vstack(
                    rx.vstack(
                        rx.text("Email", size="3", weight="medium"),
                        rx.input(
                            name="email",
                            type="email",
                            placeholder="tu@email.com",
                            required=True,
                            size="3",
                            width="100%"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Contraseña", size="3", weight="medium"),
                        rx.input(
                            name="password",
                            type="password",
                            placeholder="••••••••",
                            required=True,
                            size="3",
                            width="100%"
                        ),
                        spacing="1",
                        width="100%"
                    ),
                    rx.button(
                        rx.cond(
                            AuthState.is_loading,
                            rx.hstack(
                                rx.spinner(size="1"),
                                rx.text("Iniciando sesión...")
                            ),
                            rx.text("Iniciar Sesión")
                        ),
                        type="submit",
                        size="3",
                        width="100%",
                        color_scheme="teal",
                        disabled=AuthState.is_loading
                    ),
                    spacing="4",
                    width="100%"
                ),
                on_submit=AuthState.login,
                width="100%"
            ),
            
            # Enlaces adicionales
            rx.divider(margin="2rem 0"),
            rx.center(
                rx.link(
                    "¿Olvidaste tu contraseña?",
                    href="/reset-password",
                    color_scheme="teal"
                )
            ),
            
            spacing="6",
            width="100%",
            max_width="400px"
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        min_height="100vh",
        background="linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        padding="2rem"
    )
