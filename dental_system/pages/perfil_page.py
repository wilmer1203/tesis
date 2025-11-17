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
# COMPONENTE: SEPARADOR VISUAL
# ========================================

def separador_sutil() -> rx.Component:
    """Separador visual sutil con gradiente"""
    return rx.box(
        width="100%",
        height="2px",
        background=f"linear-gradient(90deg, transparent 0%, {COLORS['gray']['700']}80 50%, transparent 100%)",
        margin_y=SPACING["5"]
    )


# ========================================
# COMPONENTE: HEADER DE PERFIL
# ========================================

def perfil_header() -> rx.Component:
    """Header visual premium para perfil de usuario CON BOTONES DE ACCIÓN"""
    return rx.box(
        rx.hstack(
            # Avatar con iniciales
            rx.box(
                rx.text(
                    AppState.iniciales_usuario,  # "WA" para Wilmer Aguirre
                    style={
                        "font_size": "2.5rem",
                        "font_weight": "800",
                        "color": "white"
                    }
                ),
                style={
                    "width": "80px",
                    "height": "80px",
                    "border_radius": RADIUS["full"],
                    "background": GRADIENTS["neon_primary"],
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center",
                    "border": f"4px solid {COLORS['primary']['400']}40",
                    "box_shadow": f"0 8px 25px {COLORS['primary']['500']}40"
                }
            ),

            # Información principal del usuario
            rx.vstack(
                # Nombre grande con gradiente
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

                # Email + Badges (rol y estado)
                rx.hstack(
                    # Email con icono
                    rx.hstack(
                        rx.icon("mail", size=16, color=COLORS["gray"]["400"]),
                        rx.text(
                            AppState.email_usuario,
                            size="3",
                            color=COLORS["gray"]["300"]
                        ),
                        spacing="2",
                        align="center"
                    ),

                    # Badge de rol
                    rx.badge(
                        AppState.rol_usuario.upper(),
                        color_scheme="cyan",
                        size="2",
                        variant="solid"
                    ),

                    # Badge de estado laboral
                    rx.badge(
                        AppState.estado_laboral_str,
                        color_scheme=rx.cond(
                            AppState.estado_laboral_activo,
                            "green",
                            "red"
                        ),
                        size="2"
                    ),

                    spacing="3",
                    align="center",
                    wrap="wrap"
                ),

                spacing="2",
                align="start"
            ),

            # Spacer (empuja botones a la derecha)
            rx.spacer(),

            # BOTONES DE ACCIÓN (condicionales)
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
                # Estado sin cambios
                rx.hstack(
                    rx.icon("check-circle", size=18, color=COLORS["success"]["400"]),
                    rx.text(
                        "Sin cambios pendientes",
                        color=COLORS["gray"]["300"],
                        size="2",
                        weight="medium"
                    ),
                    spacing="2",
                    align="center"
                )
            ),

            spacing="5",
            align="center",
            width="100%",
            wrap="wrap"  # Permite que los botones bajen en mobile
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="2px"),
        margin_bottom="6",
        width="100%"
    )


# ========================================
# COMPONENTE: CARD DE DATOS PERSONALES
# ========================================

def card_perfil_datos() -> rx.Component:
    """Card con datos personales y laborales (2 columnas balanceadas)"""
    return rx.box(
        rx.vstack(
            # === GRID: 2 COLUMNAS BALANCEADAS ===
            rx.grid(
                # ══════════════════════════════════════
                # COLUMNA 1: DATOS PERSONALES
                # ══════════════════════════════════════
                rx.vstack(
                    # Nombre completo
                    info_field_readonly(
                        "Nombre Completo",
                        AppState.formulario_perfil.get("nombre_completo", ""),
                        icon="user",
                         help_text="No editable"
                    ),

                    # Documento de identidad (condicional)
                    rx.cond(
                        AppState.formulario_perfil.get("numero_documento", ""),
                        info_field_readonly(
                            "Documento de Identidad",
                            f"{AppState.formulario_perfil.get('tipo_documento', '')} {AppState.formulario_perfil.get('numero_documento', '')}",
                            icon="credit-card",
                            help_text="No editable"
                        )
                    ),

                    # Fecha de nacimiento (condicional)
                    rx.cond(
                        AppState.formulario_perfil.get("fecha_nacimiento", ""),
                        info_field_readonly(
                            "Fecha de Nacimiento",
                            AppState.fecha_nacimiento_formateada.to_string(),
                            icon="calendar",
                            help_text="No editable"
                        )
                    ),

                    # Teléfono celular (EDITABLE)
                    rx.vstack(
                        rx.hstack(
                            rx.icon("phone", size=16, color=COLORS["primary"]["400"]),
                            rx.text(
                                "Teléfono Celular *",
                                size="3",
                                weight="bold",
                                color=COLORS["gray"]["100"]
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
                                "border": f"2px solid {rx.cond(AppState.errores_validacion.get('celular'), COLORS['error']['500'], f'{COLORS["primary"]["500"]}30')}",
                                "color": COLORS["gray"]["100"],
                                "border_radius": RADIUS["lg"],
                                "padding": f"{SPACING['2']} {SPACING['3']}",
                                "font_size": "1rem",
                                "_focus": {
                                    "border_color": rx.cond(
                                        AppState.errores_validacion.get("celular"),
                                        COLORS["error"]["500"],
                                        COLORS["primary"]["400"]
                                    ),
                                    "box_shadow": f"0 0 0 3px {rx.cond(AppState.errores_validacion.get('celular'), f'{COLORS["error"]["500"]}25', f'{COLORS["primary"]["500"]}25')}",
                                    "outline": "none"
                                },
                                "_placeholder": {"color": COLORS["gray"]["500"]}
                            }
                        ),

                        # Error (si existe)
                        rx.cond(
                            AppState.errores_validacion.get("celular"),
                            rx.box(
                                rx.hstack(
                                    rx.icon("alert-circle", size=14, color=COLORS["error"]["400"]),
                                    rx.text(
                                        AppState.errores_validacion.get("celular"),
                                        size="1",
                                        color=COLORS["error"]["300"],
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

                    spacing="4",
                    width="100%"
                ),

                # ══════════════════════════════════════
                # COLUMNA 2: DATOS LABORALES
                # ══════════════════════════════════════
                rx.vstack(
                    # Especialidad (condicional)
                    rx.cond(
                        AppState.formulario_perfil.get("especialidad", ""),
                        info_field_readonly(
                            "Especialidad",
                            AppState.formulario_perfil.get("especialidad", ""),
                            icon="stethoscope",
                            help_text="Especialidad médica"
                        )
                    ),

                    # Licencia profesional (condicional)
                    rx.cond(
                        AppState.formulario_perfil.get("numero_licencia", ""),
                        info_field_readonly(
                            "Licencia Profesional",
                            AppState.formulario_perfil.get("numero_licencia", ""),
                            help_text="Número de licencia médica",
                            icon="badge-check"
                        )
                    ),

                    # Fecha de contratación (condicional)
                    rx.cond(
                        AppState.formulario_perfil.get("fecha_contratacion", ""),
                        info_field_readonly(
                            "Fecha de Contratación",
                            AppState.fecha_contratacion_formateada.to_string(),
                            icon="briefcase"
                        )
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.icon("map-pin", size=16, color=COLORS["primary"]["400"]),
                            rx.text(
                                "Dirección de Residencia *",
                                size="3",
                                weight="bold",
                                color=COLORS["gray"]["100"]
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
                                "border": f"2px solid {rx.cond(AppState.errores_validacion.get('direccion'), COLORS['error']['500'], f'{COLORS["primary"]["500"]}30')}",
                                "color": COLORS["gray"]["100"],
                                "border_radius": RADIUS["lg"],
                                "padding": f"{SPACING['3']} {SPACING['3']}",
                                "font_size": "1rem",
                                "line_height": "1.5",
                                "resize": "vertical",
                                "width": "100%",
                                "_focus": {
                                    "border_color": rx.cond(
                                        AppState.errores_validacion.get("direccion"),
                                        COLORS["error"]["500"],
                                        COLORS["primary"]["400"]
                                    ),
                                    "box_shadow": f"0 0 0 3px {rx.cond(AppState.errores_validacion.get('direccion'), f'{COLORS["error"]["500"]}25', f'{COLORS["primary"]["500"]}25')}",
                                    "outline": "none"
                                },
                                "_placeholder": {"color": COLORS["gray"]["500"]}
                            }
                        ),

                        # Error (si existe)
                        rx.cond(
                            AppState.errores_validacion.get("direccion"),
                            rx.box(
                                rx.hstack(
                                    rx.icon("alert-circle", size=14, color=COLORS["error"]["400"]),
                                    rx.text(
                                        AppState.errores_validacion.get("direccion"),
                                        size="1",
                                        color=COLORS["error"]["300"],
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
                columns=rx.breakpoints(initial="1", md="2"),  # 2 columnas balanceadas
                spacing="6",
                width="100%"
            ),
            spacing="6",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )


# ========================================
# COMPONENTE: CARD DE SEGURIDAD
# ========================================

def card_seguridad() -> rx.Component:
    """Card independiente para gestión de seguridad"""
    return rx.box(
        rx.vstack(
            # Header de seguridad
            rx.hstack(
                # Icono de escudo
                rx.box(
                    rx.icon("shield", size=20, color=COLORS["warning"]["400"]),
                    style={
                        "padding": SPACING["3"],
                        "background": f"{COLORS['warning']['500']}20",
                        "border_radius": RADIUS["full"],
                        "border": f"1px solid {COLORS['warning']['500']}30"
                    }
                ),

                # Título y subtítulo
                rx.vstack(
                    rx.text(
                        "Seguridad de la Cuenta",
                        size="4",
                        weight="bold",
                        color=COLORS["gray"]["100"]
                    ),
                    rx.text(
                        "Gestiona tu contraseña y correo electrónico",
                        size="2",
                        color=COLORS["gray"]["300"]
                    ),
                    spacing="1",
                    align="start"
                ),

                spacing="4",
                align="center"
            ),

            # Botones de seguridad
            rx.grid(
                # Botón: Cambiar contraseña
                rx.button(
                    rx.hstack(
                        rx.icon("lock", size=20, color=COLORS["primary"]["400"]),
                        rx.text(
                            "Cambiar Contraseña",
                            size="4",
                            weight="bold",
                            color=COLORS["gray"]["100"]
                        ),
                        spacing="3",
                        align="center"  # Centra iconos y texto
                    ),
                    on_click=AppState.abrir_modal_cambio_password,
                    style={
                        "width": "100%",
                        # "min_height": "140px",
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
                ),

                # Botón: Cambiar email
                rx.button(
                    rx.hstack(
                        rx.icon("mail", size=28, color=COLORS["success"]["400"]),
                        rx.text(
                            "Cambiar Email",
                            size="4",
                            weight="bold",
                            color=COLORS["gray"]["100"]
                        ),
                        spacing="3",
                        align="center"  # Centra iconos y texto
                    ),
                    on_click=AppState.abrir_modal_cambio_email,
                    style={
                        "width": "100%",
                        # "min_height": "140px",
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
                ),

                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="6",  # Más espacio entre botones
                width="100%"
            ),

            spacing="6",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["warning"]["500"], hover_lift="4px"),
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
                # Header con avatar, info y botones
                perfil_header(),

                # Card de datos personales/laborales
                card_perfil_datos(),

                # Card de seguridad (separado)
                card_seguridad(),

                spacing="6",
                width="100%"
            )
        ),

        # Modales
        modal_cambiar_password(),
        modal_cambiar_email(),

        on_mount=AppState.cargar_datos_perfil()
    )
