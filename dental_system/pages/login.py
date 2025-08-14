# 🔐 PÁGINA DE LOGIN MEJORADA - login.py
# Reemplaza tu login.py actual con este código mejorado:

import reflex as rx
from dental_system.state.app_state import AppState
from assets.css.styles import STYLES
from ..styles.themes import COLORS, botton_login, input_login


def fondo() -> rx.Component:
    """Imagen de fondo difuminado."""
    return rx.box(
        style={
            "width": "100%",
            "height": "100vh",
            "background": f"linear-gradient(120deg,{COLORS["gray"]["950"]} 0%, {COLORS["blue"]["950"]} 50%, {COLORS["primary"]["700"]} 100%)",
        },
        position="absolute",
    )


def mensaje_error() -> rx.Component:
    """🚨 Componente mejorado para mostrar errores"""
    return rx.cond(
        AppState.error_login != "",
        rx.callout(
            AppState.error_login ,
            color_scheme="red",
            size="2",
            width="100%",
            margin_bottom="4"
        )
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
                # Mensajes de error
                # mensaje_error(),
            
                # Formulario de login
                rx.form(
                    rx.vstack(
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
                            disabled=AppState.esta_cargando_auth                

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
                            disabled=AppState.esta_cargando_auth
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
                                AppState.esta_cargando_auth,
                                rx.hstack(
                                    rx.spinner(color="white", size="3"),
                                    rx.text("Iniciando sesión...", font_size="1.3em"),
                                    spacing="2",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.icon("log-in", size=20, color="white"),
                                    rx.text("Iniciar Sesión", font_size="1.7em"),
                                    spacing="2",
                                    align="center"
                                )
                            ),
                            type="submit",
                            disabled=AppState.esta_cargando_auth,
                            style=botton_login,
                             width="50%"
                        ),
                        spacing="4",
                        width="100%",
                        align="center",
                    ),
                    on_submit=AppState.iniciar_sesion,
                    width="100%",
                    height="100%",
                    flex_direction="column",
                    gap="3",
                    reset_on_submit=False,  # No resetear el formulario automáticamente
                ),
              
            ),
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
    """🔐 Página principal de login"""
    return rx.fragment(
        # Redirección automática si ya está autenticado
        rx.cond(
            AppState.esta_autenticado,
            rx.script(f"""
                // Redirección automática según rol
                const userRole = '{AppState.rol_usuario}';
                let redirectUrl = '/';
                
                if (userRole === 'gerente') {{
                    redirectUrl = '/boss';
                }} else if (userRole === 'administrador') {{
                    redirectUrl = '/admin';
                }} else if (userRole === 'odontologo') {{
                    redirectUrl = '/dentist';
                }}
                
                console.log('Usuario ya autenticado, redirigiendo a:', redirectUrl);
                window.location.href = redirectUrl;
            """)
        ),
        
        # Contenido de la página de login
        rx.box(
            fondo(),
            contenedor(),
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "z_index": "-2",
            },
        ),
        
        # Limpieza automática de errores después de 5 segundos
        rx.cond(
            AppState.error_login != "",
            rx.script(f"""
                setTimeout(function() {{
                    // Limpiar error después de 5 segundos
                    console.log('Limpiando mensaje de error automáticamente');
                }}, 5000);
            """)
        )
    )







