"""
Página de perfil de usuario
Permite al usuario ver y editar su información personal
"""
import reflex as rx
from ..components.common import (
    page_header,
    medical_page_layout,
    medical_toast_container,
    primary_button,
    secondary_button,
    info_field_readonly
)
from ..components.modal_perfil import modal_cambiar_email, modal_cambiar_password
from ..components.forms import form_section_header
from ..styles.themes import COLORS, SPACING, RADIUS, GRADIENTS, DARK_THEME, dark_crystal_card
from ..state.app_state import AppState
from typing import Dict, Any


# ========================================
# COMPONENTE: HEADER DE PERFIL CON AVATAR
# ========================================

def perfil_header() -> rx.Component:
    """Header visual premium con avatar, nombre y badges de estado"""
    return rx.box(
        rx.hstack(
            # Avatar con iniciales
            rx.box(
                rx.text(
                    AppState.iniciales_usuario,
                    style={
                        "font_size": "2.5rem",
                        "font_weight": "800",
                        "color": "white"
                    }
                ),
                style={
                    "width": "100px",
                    "height": "100px",
                    "border_radius": RADIUS["full"],
                    "background": GRADIENTS["neon_primary"],
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center",
                    "border": f"4px solid {COLORS['primary']['400']}40",
                    "box_shadow": f"0 8px 25px {COLORS['primary']['500']}40",
                    "flex_shrink": "0"
                }
            ),

            # Información principal
            rx.vstack(
                # Nombre grande
                rx.text(
                    AppState.formulario_perfil.get("nombre_completo", ""),
                    style={
                        "font_size": "2.25rem",
                        "font_weight": "800",
                        "background": GRADIENTS["text_gradient_primary"],
                        "background_clip": "text",
                        "color": "transparent",
                        "line_height": "1.2"
                    }
                ),

                # Email + badges
                rx.hstack(
                    # Email
                    rx.hstack(
                        rx.icon("mail", size=16, color=COLORS["primary"]["400"]),
                        rx.text(
                            AppState.email_usuario,
                            size="3",
                            color=COLORS["gray"]["200"],
                            weight="medium"
                        ),
                        spacing="2",
                        align="center"
                    ),

                    # Badge de rol
                    rx.hstack(
                        rx.icon("shield-check", size=16, color=COLORS["primary"]["400"]),
                        rx.text(
                            AppState.rol_usuario.upper(),
                            size="2",
                            weight="bold",
                            color=COLORS["primary"]["300"],
                            style={
                                "padding": "6px 12px",
                                "border_radius": RADIUS["lg"],
                                "background": f"{COLORS['primary']['500']}20",
                                "border": f"1px solid {COLORS['primary']['500']}50"
                            }
                        ),
                        spacing="2",
                        align="center"
                    ),

                    # Badge de estado laboral
                    rx.hstack(
                        rx.icon(
                            rx.cond(AppState.estado_laboral_activo, "check-circle", "x-circle"),
                            size=16,
                            color=rx.cond(
                                AppState.estado_laboral_activo,
                                COLORS["success"]["400"],
                                COLORS["error"]["400"]
                            )
                        ),
                        rx.text(
                            AppState.estado_laboral_str,
                            size="2",
                            weight="bold",
                            color=rx.cond(
                                AppState.estado_laboral_activo,
                                COLORS["success"]["300"],
                                COLORS["error"]["400"]
                            ),
                            style={
                                "padding": "6px 12px",
                                "border_radius": RADIUS["md"],
                                "background": rx.cond(
                                    AppState.estado_laboral_activo,
                                    f"{COLORS['success']['500']}15",
                                    f"{COLORS['error']['500']}15"
                                ),
                                "border": rx.cond(
                                    AppState.estado_laboral_activo,
                                    f"1px solid {COLORS['success']['500']}40",
                                    f"1px solid {COLORS['error']['500']}40"
                                )
                            }
                        ),
                        spacing="2",
                        align="center"
                    ),

                    spacing="4",
                    align="center",
                    wrap="wrap"
                ),

                spacing="2",
                align="start",
                width="100%"
            ),

            spacing="5",
            align="center",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="2px"),
        width="100%",
        margin_bottom="6"
    )


# ========================================
# COMPONENTE: SKELETON LOADER
# ========================================

def perfil_skeleton() -> rx.Component:
    """Skeleton loader mientras carga el perfil"""
    return rx.box(
        rx.vstack(
            # Header skeleton
            rx.skeleton(height="130px", width="100%", style={"border_radius": RADIUS["2xl"]}),

            # Grid skeleton
            rx.grid(
                rx.skeleton(height="250px", style={"border_radius": RADIUS["2xl"]}),
                rx.skeleton(height="250px", style={"border_radius": RADIUS["2xl"]}),
                rx.skeleton(height="250px", style={"border_radius": RADIUS["2xl"]}),
                columns=rx.breakpoints(initial="1", sm="1", md="2", lg="3"),
                spacing="6"
            ),

            spacing="6",
            width="100%"
        )
    )


# ========================================
# COMPONENTE: CARD DE PERFIL PRINCIPAL
# ========================================

def card_perfil() -> rx.Component:
    """Card de perfil completo con diseño mejorado y mejor contraste"""
    return rx.box(
        rx.vstack(
            # === GRID: 1 → 2 → 3 columnas ===
            rx.grid(
                # COL 1: Datos Personales
                rx.vstack(
                    # Email (ahora visible)
                    info_field_readonly(
                        "Correo Electrónico",
                        AppState.email_usuario,
                        icon="mail",
                        help_text="Puedes cambiarlo desde Seguridad"
                    ),

                    # Nombre completo
                    info_field_readonly(
                        "Nombre Completo",
                        AppState.formulario_perfil.get("nombre_completo", ""),
                        icon="user"
                    ),

                    # Documento de identidad
                    rx.cond(
                        AppState.formulario_perfil.get("numero_documento", ""),
                        info_field_readonly(
                            "Documento de Identidad",
                            f"{AppState.formulario_perfil.get('tipo_documento', '')} {AppState.formulario_perfil.get('numero_documento', '')}",
                            icon="credit-card"
                        )
                    ),

                    # Fecha de nacimiento (formateada)
                    rx.cond(
                        AppState.formulario_perfil.get("fecha_nacimiento", ""),
                        info_field_readonly(
                            "Fecha de Nacimiento",
                            AppState.fecha_nacimiento_formateada,
                            icon="calendar"
                        )
                    ),

                    spacing="4",
                    width="100%"
                ),

                # COL 2: Datos Laborales
                rx.vstack(
                    rx.cond(
                        AppState.formulario_perfil.get("especialidad", ""),
                        info_field_readonly(
                            "Especialidad",
                            AppState.formulario_perfil.get("especialidad", ""),
                            icon="stethoscope"
                        )
                    ),

                    rx.cond(
                        AppState.formulario_perfil.get("numero_licencia", ""),
                        info_field_readonly(
                            "Licencia Profesional",
                            AppState.formulario_perfil.get("numero_licencia", ""),
                            help_text="Número de licencia médica",
                            icon="badge-check"
                        )
                    ),

                    rx.cond(
                        AppState.formulario_perfil.get("fecha_contratacion", ""),
                        info_field_readonly(
                            "Fecha de Contratación",
                            AppState.fecha_contratacion_formateada,
                            icon="briefcase"
                        )
                    ),

                    spacing="4",
                    width="100%"
                ),

                # COL 3: Contacto Editable
                rx.vstack(
                    # Teléfono celular (editable)
                    rx.vstack(
                        rx.hstack(
                            rx.icon("phone", size=16, color=COLORS["primary"]["400"]),
                            rx.text(
                                "Teléfono Celular *",
                                size="3",
                                weight="bold",
                                color=COLORS["gray"]["100"]  # Mejor contraste
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.input(
                            value=AppState.formulario_perfil.get("celular", ""),
                            on_change=lambda v: AppState.actualizar_campo_perfil("celular", v),
                            placeholder="+58 412 1234567",
                            style={
                                "background": COLORS["gray"]["900"],
                                "border": f"2px solid {rx.cond(AppState.errores_validacion.get('celular'), COLORS['error']['500'], f\"{COLORS['primary']['500']}30\")}",
                                "color": COLORS["gray"]["100"],  # Mejor contraste
                                "border_radius": RADIUS["lg"],
                                "padding": f"{SPACING['2']} {SPACING['3']}",
                                "font_size": "1rem",
                                "_focus": {
                                    "border_color": rx.cond(
                                        AppState.errores_validacion.get("celular"),
                                        COLORS["error"]["500"],
                                        COLORS["primary"]["400"]
                                    ),
                                    "box_shadow": f"0 0 0 3px {rx.cond(AppState.errores_validacion.get('celular'), f\"{COLORS['error']['500']}25\", f\"{COLORS['primary']['500']}25\")}",
                                    "outline": "none"
                                },
                                "_placeholder": {"color": COLORS["gray"]["500"]}
                            }
                        ),
                        # Error mejorado
                        rx.cond(
                            AppState.errores_validacion.get("celular"),
                            rx.box(
                                rx.hstack(
                                    rx.icon("alert-circle", size=14, color=COLORS["error"]["400"]),
                                    rx.text(
                                        AppState.errores_validacion.get("celular"),
                                        size="1",
                                        color=COLORS["error"]["300"],  # Mejor contraste
                                        weight="medium"
                                    ),
                                    spacing="1",
                                    align="center"
                                ),
                                style={
                                    "background": f"{COLORS['error']['500']}15",
                                    "padding": f"{SPACING['2']} {SPACING['3']}",
                                    "border_radius": RADIUS["md"],
                                    "border": f"1px solid {COLORS['error']['500']}30",
                                    "margin_top": SPACING["1"]
                                }
                            )
                        ),
                        rx.text(
                            "Formato: +58 412 1234567",
                            size="1",
                            color=COLORS["gray"]["400"]
                        ),
                        spacing="2",
                        width="100%"
                    ),

                    # Dirección (editable - mejorada)
                    rx.vstack(
                        rx.hstack(
                            rx.icon("map-pin", size=16, color=COLORS["primary"]["400"]),
                            rx.text(
                                "Dirección de Residencia *",
                                size="3",
                                weight="bold",
                                color=COLORS["gray"]["100"]  # Mejor contraste
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.text_area(
                            value=AppState.formulario_perfil.get("direccion", ""),
                            on_change=lambda v: AppState.actualizar_campo_perfil("direccion", v),
                            placeholder="Dirección completa de residencia",
                            rows="3",
                            style={
                                "background": COLORS["gray"]["900"],
                                "border": f"2px solid {rx.cond(AppState.errores_validacion.get('direccion'), COLORS['error']['500'], f\"{COLORS['primary']['500']}30\")}",
                                "color": COLORS["gray"]["100"],  # Mejor contraste
                                "border_radius": RADIUS["lg"],
                                "padding": f"{SPACING['3']} {SPACING['3']}",
                                "font_size": "1rem",
                                "line_height": "1.5",
                                "resize": "vertical",
                                "min_height": "80px",
                                "_focus": {
                                    "border_color": rx.cond(
                                        AppState.errores_validacion.get("direccion"),
                                        COLORS["error"]["500"],
                                        COLORS["primary"]["400"]
                                    ),
                                    "box_shadow": f"0 0 0 3px {rx.cond(AppState.errores_validacion.get('direccion'), f\"{COLORS['error']['500']}25\", f\"{COLORS['primary']['500']}25\")}",
                                    "outline": "none"
                                },
                                "_placeholder": {"color": COLORS["gray"]["500"]}
                            }
                        ),
                        # Error mejorado
                        rx.cond(
                            AppState.errores_validacion.get("direccion"),
                            rx.box(
                                rx.hstack(
                                    rx.icon("alert-circle", size=14, color=COLORS["error"]["400"]),
                                    rx.text(
                                        AppState.errores_validacion.get("direccion"),
                                        size="1",
                                        color=COLORS["error"]["300"],  # Mejor contraste
                                        weight="medium"
                                    ),
                                    spacing="1",
                                    align="center"
                                ),
                                style={
                                    "background": f"{COLORS['error']['500']}15",
                                    "padding": f"{SPACING['2']} {SPACING['3']}",
                                    "border_radius": RADIUS["md"],
                                    "border": f"1px solid {COLORS['error']['500']}30",
                                    "margin_top": SPACING["1"]
                                }
                            )
                        ),
                        rx.text(
                            "Máx. 200 caracteres",
                            size="1",
                            color=COLORS["gray"]["400"]
                        ),
                        spacing="2",
                        width="100%"
                    ),

                    spacing="4",
                    width="100%"
                ),

                columns=rx.breakpoints(initial="1", sm="1", md="2", lg="3"),
                spacing="6",
                width="100%"
            ),

            # === BOTONES DE GUARDAR/CANCELAR ===
            rx.hstack(
                rx.cond(
                    AppState.tiene_cambios_pendientes,
                    rx.hstack(
                        primary_button(
                            "Guardar Cambios",
                            icon="save",
                            on_click=AppState.guardar_cambios_perfil,
                            loading=AppState.guardando_cambios
                        ),
                        secondary_button(
                            "Cancelar",
                            icon="x",
                            on_click=AppState.cancelar_edicion
                        ),
                        spacing="3"
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=18, color=COLORS["success"]["400"]),
                        rx.text(
                            "Sin cambios pendientes",
                            color=COLORS["gray"]["300"],  # Mejor contraste
                            size="2",
                            weight="medium"
                        ),
                        spacing="2",
                        align="center"
                    )
                ),
                width="100%",
                justify="start",
                margin_top="5"
            ),

            # === SECCIÓN DE SEGURIDAD MEJORADA ===
            rx.box(
                rx.vstack(
                    # Header más destacado
                    rx.hstack(
                        rx.box(
                            rx.icon("shield", size=24, color=COLORS["warning"]["400"]),
                            style={
                                "padding": SPACING["2"],
                                "background": f"{COLORS['warning']['500']}20",
                                "border_radius": RADIUS["full"]
                            }
                        ),
                        rx.vstack(
                            rx.text(
                                "Seguridad de la Cuenta",
                                size="4",
                                weight="bold",
                                color=COLORS["gray"]["100"]  # Mejor contraste
                            ),
                            rx.text(
                                "Gestiona tu contraseña y correo electrónico",
                                size="2",
                                color=COLORS["gray"]["300"]  # Mejor contraste
                            ),
                            spacing="0",
                            align="start"
                        ),
                        spacing="3",
                        align="center"
                    ),

                    # Botones de seguridad
                    rx.grid(
                        # Cambiar contraseña
                        rx.box(
                            rx.button(
                                rx.vstack(
                                    rx.icon("lock", size=24, color=COLORS["primary"]["400"]),
                                    rx.text(
                                        "Cambiar Contraseña",
                                        weight="600",
                                        size="3",
                                        color=COLORS["gray"]["100"]  # Mejor contraste
                                    ),
                                    rx.text(
                                        "Actualiza tu contraseña",
                                        size="1",
                                        color=COLORS["gray"]["400"]
                                    ),
                                    spacing="2",
                                    align="center"
                                ),
                                on_click=AppState.abrir_modal_cambio_password,
                                style={
                                    "width": "100%",
                                    "padding": SPACING["5"],
                                    "background": "transparent",
                                    "border": f"2px solid {COLORS['primary']['500']}40",
                                    "border_radius": RADIUS["xl"],
                                    "cursor": "pointer",
                                    "transition": "all 0.3s ease",
                                    "_hover": {
                                        "border_color": COLORS["primary"]["400"],
                                        "background": f"{COLORS['primary']['500']}10",
                                        "transform": "translateY(-2px)",
                                        "box_shadow": f"0 4px 12px {COLORS['primary']['500']}30"
                                    }
                                }
                            )
                        ),

                        # Cambiar email
                        rx.box(
                            rx.button(
                                rx.vstack(
                                    rx.icon("mail", size=24, color=COLORS["success"]["400"]),
                                    rx.text(
                                        "Cambiar Email",
                                        weight="600",
                                        size="3",
                                        color=COLORS["gray"]["100"]  # Mejor contraste
                                    ),
                                    rx.text(
                                        "Actualiza tu correo electrónico",
                                        size="1",
                                        color=COLORS["gray"]["400"]
                                    ),
                                    spacing="2",
                                    align="center"
                                ),
                                on_click=AppState.abrir_modal_cambio_email,
                                style={
                                    "width": "100%",
                                    "padding": SPACING["5"],
                                    "background": "transparent",
                                    "border": f"2px solid {COLORS['success']['500']}40",
                                    "border_radius": RADIUS["xl"],
                                    "cursor": "pointer",
                                    "transition": "all 0.3s ease",
                                    "_hover": {
                                        "border_color": COLORS["success"]["400"],
                                        "background": f"{COLORS['success']['500']}10",
                                        "transform": "translateY(-2px)",
                                        "box_shadow": f"0 4px 12px {COLORS['success']['500']}30"
                                    }
                                }
                            )
                        ),

                        columns=rx.breakpoints(initial="1", md="2"),
                        spacing="4",
                        width="100%"
                    ),

                    spacing="5",
                    width="100%",
                    padding_top="6",
                    border_top=f"2px solid {COLORS['gray']['700']}"
                )
            ),

            spacing="6",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )


# ========================================
# PÁGINA PRINCIPAL
# ========================================

def perfil_page() -> rx.Component:
    """Página principal de perfil de usuario"""
    return rx.fragment(
        medical_toast_container(),

        medical_page_layout(
            rx.vstack(
                # Header
                page_header(
                    "Mi Perfil",
                    "Gestiona tu información personal y preferencias del sistema",
                    actions=[]
                ),

                # Cargar datos al montar
                rx.moment(on_mount=AppState.cargar_datos_perfil),

                # Header de perfil con avatar
                rx.cond(
                    AppState.cargando_perfil,
                    perfil_skeleton(),
                    rx.fragment(
                        perfil_header(),
                        card_perfil()
                    )
                ),

                spacing="6",
                width="100%"
            )
        ),

        # Modales
        modal_cambiar_password(),
        modal_cambiar_email()
    )
