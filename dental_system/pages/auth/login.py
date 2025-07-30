# =====================================================
# PÁGINA DE INICIO DE SESIÓN
# =====================================================

import reflex as rx
from dental_system.components.auth.login_form import login_form
from dental_system.state.auth_state import AuthState
from assets.css.styles import COLORS, STYLES
from ...styles.themes import COLORS, botton_login,input_login


def fondo() -> rx.Component:
    """Imagen de fondo difuminado."""
    return rx.box(
        # rx.image(
        #     src="/images/background.jpg",
        #     width="100%",
        #     height="100vh",
        #     alt="Background"
        # ),
        style={
            "width": "100%",
            "height": "100vh",
            "background": "linear-gradient(120deg, #0f172a 0%, #1e293b 50%, #0d9488 100%)",
        },
        position="absolute",
        
    )

def contenedor() -> rx.Component:
    """Contenedor principal."""
    return rx.center(
        rx.flex(
            rx.vstack(
                rx.vstack(
                    rx.image(
                        src="/images/logo-odontomara.png",
                        width="80px",
                        border_radius="50%",
                        alt="Odontomara"
                    ),
                    rx.heading(
                        "Odontomara",
                        color=COLORS["primary"]["500"],
                        font_size="2.5em",
                        text_align="center",
                        margin_bottom="30px",
                        text_shadow=f"3px 3px 2px black",
                    ),
                    align="center",
                    justify="center",
                    width="100%",
                ),
                # Formulario de login
                rx.form(
                    rx.vstack(
                     # Mensajes de error y éxito
                        rx.cond(
                            AuthState.error_message != "",
                            rx.callout(
                                AuthState.error_message,
                                color="red.300",
                                font_weight="bold",
                                background="rgba(255, 0, 0, 0.1)",
                                padding="2",
                                border_radius="md",
                                width="80%",
                                text_align="center",
                                border="1px solid rgba(255, 0, 0, 0.3)"
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
                        
                        # Campo de email
                        rx.text(
                            "Usuario",
                            color=COLORS["gray"]["50"],
                            font_weight="bold",
                            font_size="1.7em",
                            text_align="left",
                            width="80%",
                            padding="2px",
                            text_shadow="3px 3px 2px black",
                        ),
                        rx.input(
                            rx.input.slot(rx.icon("user"), color=COLORS["primary"]["400"]),
                            placeholder="usuario@gmail.com",
                            width="80%",
                            style=input_login,
                            type_="email",
                            name="email",
                            required=True,                       

                        ),
                        # Campo de contraseña
                        rx.text(
                            "Contraseña",
                            color=COLORS["gray"]["50"],
                            font_size="1.7em",
                            font_weight="bold",
                            text_align="left",
                            width="80%",
                            padding="2px",
                            margin_top="20px",
                            text_shadow="3px 3px 2px black",
                        ),
                        rx.input(
                            rx.input.slot(rx.icon("lock"), color=COLORS["primary"]["400"]),
                            placeholder="••••••••",
                            width="80%",
                            style=input_login,
                            type_="password",
                            name="password",
                            required=True,
                        ),
                        rx.vstack(
                            rx.link(
                                "¿Olvidaste tu contraseña?",
                                href="/reset-password",
                                color_scheme="teal",

                            ),
                            width="80%",
                            align="end",
                        ),
                        rx.button(
                            rx.cond(
                                AuthState.is_loading,
                                rx.hstack(
                                    rx.spinner(color="white", size="3"),
                                    rx.text("Iniciando sesión...", font_size="1.3em"),
                                    spacing="2",
                                    align="center"
                                ),
                                rx.text("Iniciar Sesión", font_size="1.7em")
                            ),
                            
                            # **botton_login,
                            type="submit",
                            disabled=AuthState.is_loading,
                            style=botton_login,
                        ),
                        spacing="4",
                        width="100%",
                        align="center",
                    ),
                    on_submit=AuthState.login,
                    width="100%",
                    height="100%",
                    flex_direction="column",
                    gap="3",
                    reset_on_submit=False,  # No resetear el formulario automáticamente
                ),
              
            ),
            
            # **STYLES["login"]["form_panel"],
            direction="column",
            
            style={
                "position": "absolute",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "height": "90%",
                "background-position": "center",
                "border-radius": "30px",               
                "margin": "0 auto",
                "border": "5px double transparent",
                "justify_content": "center",          
                "overflow": "hidden",           
                "box_shadow": "1px 1px 32px 13px rgba(0, 0, 0, 0.4)",
                "padding":"10px",
            },
            
            width=rx.breakpoints(initial="95%", sm="75%", md="75", lg="50%", xl="50%"),           
        ),      
    )


def login_page() -> rx.Component:
    """Página de inicio de sesión"""
    return rx.box(
     
        fondo(),
        contenedor(),
        style= {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "width": "100%",
            "height": "100%",
            "z_index": "-2",
        },
        
    )