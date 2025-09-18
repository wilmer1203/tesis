# 🔐 PÁGINA DE LOGIN ENTERPRISE MEDICAL - Sistema Odontológico Odontomara
# ============================================================================
# Login profesional médico con glassmorphism sin dark_crystal_card problemático
# ============================================================================

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.state.estado_auth import EstadoAuth
from ..styles.themes import (
    COLORS, SHADOWS, SPACING, RADIUS,
    glassmorphism_card, glassmorphism_input, primary_button
)


def fondo_medico_premium() -> rx.Component:
    """🌟 Fondo médico profesional con efectos cristalinos"""
    return rx.box(
        style={
            "width": "100%",
            "height": "100vh",
            "background": f"""
                linear-gradient(135deg, {COLORS['blue']['950']} 0%, {COLORS['gray']['900']} 25%, {COLORS['primary']['800']} 75%, {COLORS['blue']['900']} 100%),
                radial-gradient(circle at 20% 80%, {COLORS['primary']['500']}15 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, {COLORS['secondary']['500']}12 0%, transparent 50%)
            """,
            "position": "fixed",
            "top": "0",
            "left": "0",
            "z_index": "-10",
            "overflow": "hidden"
        }
    )


def logo_flotante_medico() -> rx.Component:
    """🏥 Logo flotante profesional sin dark_crystal_card"""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.image(
                    src="/images/logo-odontomara.png",
                    width="80px",
                    height="80px",
                    border_radius="50%",
                    alt="Odontomara Logo"
                ),
                style={
                    "padding": SPACING["1"],
                    "border_radius": "50%",
                    "background": f"""
                        linear-gradient(135deg, 
                            {COLORS['primary']['500']}20 0%, 
                            {COLORS['blue']['600']}15 100%
                        )
                    """,
                    "backdrop_filter": "blur(20px) saturate(180%)",
                    "border": f"2px solid {COLORS['primary']['400']}40",
                    "box_shadow": f"0 0 30px {COLORS['primary']['500']}40"
                }
            ),
            rx.heading(
                "ODONTOMARA",
                size="6",
                weight="bold",
                color=COLORS["gray"]["50"],
                text_align="center",
                letter_spacing="0.1em",
                text_shadow=f"0 0 20px {COLORS['primary']['500']}80"
            ),
            rx.text(
                "Sistema Médico Profesional",
                size="2",
                color=COLORS["gray"]["300"],
                text_align="center",
                letter_spacing="0.05em",
                opacity="0.8"
            ),
            spacing="4",
            align="center"
        ),
        margin_bottom="8"
    )


def toast_error_flotante() -> rx.Component:
    """🚨 Notificación flotante tipo toast para errores de login"""
    return rx.cond(
        AppState.error_login != "",
        rx.box(
            rx.hstack(
                rx.icon("circle_alert", size=20, color="white"),
                rx.text(
                    "Credenciales inválidas",  # Mensaje simplificado
                    size="3",
                    color="white",
                    weight="medium"
                ),
                justify="between",
                align="center",
                width="100%"
            ),
            style={
                "position": "fixed",
                "top": "20px",
                "right": "20px",
                "z_index": "9999",
                "background": f"linear-gradient(135deg, {COLORS['error']['600']} 0%, {COLORS['error']['500']} 100%)",
                "border": f"1px solid {COLORS['error']['400']}60",
                "border_radius": RADIUS["lg"],
                "padding": f"{SPACING['4']} {SPACING['5']}",
                "min_width": "320px",
                "max_width": "400px",
                "backdrop_filter": "blur(20px)",
                "box_shadow": f"0 10px 25px {COLORS['error']['500']}30",
                "animation": "slideInRight 0.4s ease-out"
            }
        ),
        rx.fragment()
    )

def formulario_login_enterprise() -> rx.Component:
    """📝 Formulario de login enterprise con validaciones avanzadas"""
    return rx.form(
        rx.vstack(
            # Campo Email con validación
            rx.vstack(
                rx.text(
                    "Correo Electrónico",
                    size="3",
                    weight="medium",
                    color=COLORS["gray"]["200"],
                    margin_bottom="2"
                ),
                rx.input(
                    rx.input.slot(
                        rx.icon("mail", size=18),
                        color=COLORS["primary"]["400"]
                    ),
                    placeholder="medico@odontomara.com",
                    type_="email",
                    name="email",
                    required=True,
                    disabled=AppState.esta_cargando_auth,
                    style={
                        **glassmorphism_input(),
                        "padding": SPACING["1"],
                        "height": "1.5em",
                        "font_size": "1.3em"
                    },
                    width="100%"
                ),
                spacing="1",
                width="100%"
            ),

            # Campo Contraseña con validación
            rx.vstack(
                rx.text(
                    "Contraseña",
                    size="3", 
                    weight="medium",
                    color=COLORS["gray"]["200"],
                    margin_bottom="2"
                ),
                rx.input(
                    rx.input.slot(
                        rx.icon("lock", size=18),
                        color=COLORS["primary"]["400"]
                    ),
                    placeholder="••••••••••••",
                    type_="password",
                    name="password",
                    required=True,
                    disabled=AppState.esta_cargando_auth,
                    style={
                        **glassmorphism_input(),
                        "padding": SPACING["1"],
                        "height": "1.5em",
                        "font_size": "1.3em"
                    },
                    width="100%"
                ),
                spacing="1",
                width="100%"
            ),

            # Link de recuperación
            rx.box(
                rx.link(
                    "¿Olvidaste tu contraseña?",
                    href="#",
                    color=COLORS["primary"]["300"],
                    text_decoration="none",
                    _hover={
                        "color": COLORS["primary"]["200"],
                        "text_decoration": "underline"
                    },
                    size="2"
                ),
                text_align="right",
                width="100%",
                margin_bottom="4"
            ),

            # Botón de login enterprise
            
            rx.button(
                rx.cond(
                    AppState.esta_cargando_auth,
                    rx.hstack(
                        rx.spinner(color="white", size="3"),
                        rx.text("Autenticando...", size="4", weight="medium"),
                        spacing="3",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("log-in", size=20, color="white"),
                        rx.text("Iniciar Sesión", size="4", weight="medium"),
                        spacing="3",
                        align="center"
                    )
                ),
                type="submit",
                disabled=AppState.esta_cargando_auth,
                style={
                    **primary_button(),
                    "width": "100%"
                }
            ),

            spacing="6",
            width="100%"
        ),
        on_submit=AppState.iniciar_sesion,
        reset_on_submit=False,
        width="100%",
    )


def contenedor_principal_glassmorphism() -> rx.Component:
    """🏗️ Contenedor principal con efectos glassmorphism sin dark_crystal_card"""
    return rx.center(
        rx.box(
            rx.vstack(
                # Logo y branding
                logo_flotante_medico(),
                
                # Formulario de login
                formulario_login_enterprise(),
                
                # Footer institucional
                rx.box(
                    rx.text(
                        "© 2025 Odontomara - Sistema Médico Profesional",
                        size="1",
                        color=COLORS["gray"]["400"],
                        text_align="center",
                        opacity="0.7"
                    ),
                    margin_top="8",
                    width="100%"
                ),
                
                spacing="6",
                align="center",
                width="100%"
            ),
            style={
                **glassmorphism_card(),
                "padding": SPACING["8"],
                "width": "100%",
                "max_width": "420px",
                "overflow": "hidden"
            }
        ),
        height="100vh",
        width="100%",
        padding="4"
    )


def login_page() -> rx.Component:
    """🔐 Página principal de login enterprise médico sin componentes problemáticos"""
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
            """),
            rx.fragment()
        ),
        
        # Fondo premium
        fondo_medico_premium(),
        
        # Toast de error flotante
        toast_error_flotante(),
        
        # Contenido principal
        contenedor_principal_glassmorphism(),
        
        # Estilos CSS adicionales para animaciones
        rx.script("""
            // CSS personalizado para animaciones
            const style = document.createElement('style');
            style.textContent = `
                @keyframes pulse-glow {
                    0% { box-shadow: 0 0 20px rgba(28, 187, 186, 0.3); }
                    100% { box-shadow: 0 0 30px rgba(28, 187, 186, 0.6); }
                }
                
                @keyframes float {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-10px); }
                }
                
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                    20%, 40%, 60%, 80% { transform: translateX(5px); }
                }
                
                @keyframes fadeInDown {
                    from {
                        opacity: 0;
                        transform: translateY(-10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                @keyframes slideInRight {
                    from {
                        opacity: 0;
                        transform: translateX(100%);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
            `;
            document.head.appendChild(style);
        """)
    )