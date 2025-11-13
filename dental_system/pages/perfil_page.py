"""
Página de perfil de usuario
Permite al usuario ver y editar su información personal
"""
import reflex as rx
from ..components.common import (
    page_header,medical_page_layout,medical_toast_container,primary_button,secondary_button)
from ..components.modal_perfil import modal_cambiar_email, modal_cambiar_password
from ..components.forms import form_section_header
from ..styles.themes import COLORS, SPACING, RADIUS, GRADIENTS, SHADOWS, dark_crystal_card,glassmorphism_card
from ..state.app_state import AppState
from typing import Dict, Any, List


# ========================================
# HELPERS LOCALES (específicos de perfil)
# ========================================

def _readonly_field_style() -> Dict[str, Any]:
    """Estilos consistentes para campos readonly"""
    return {
        "background": COLORS["gray"]["800"],
        "border": f"1px solid {COLORS['gray']['700']}",
        "color": COLORS["gray"]["400"],
        "cursor": "not-allowed",
        "opacity": "0.8"
    }


def _readonly_input(
    label: str,
    value: str,
    help_text: str = "",
    special_style: Dict[str, Any] = None
) -> rx.Component:
    """Campo readonly estilizado para perfil"""
    base_style = _readonly_field_style()
    if special_style:
        base_style.update(special_style)

    return rx.vstack(
        rx.text(label, size="2", weight="bold", color=COLORS["gray"]["300"]),
        rx.input(
            value=value,
            readonly=True,
            width="100%",
            style=base_style
        ),
        rx.cond(
            help_text != "",
            rx.text(help_text, size="1", color=COLORS["gray"]["500"]),
            rx.box()
        ),
        spacing="1",
        width="100%"
    )



def readonly_style() -> dict:
    """Estilo readonly consistente con tema"""
    return {
        "background": f"{COLORS['gray']['900']}90",
        "border": f"1px solid {COLORS['gray']['700']}",
        "color": COLORS["gray"]["400"],
        "cursor": "not-allowed",
        "opacity": "0.9",
        "border_radius": RADIUS["md"],
        "backdrop_filter": "blur(2px)"
    }

def editable_input_style() -> dict:
    """Estilo input editable con foco turquesa"""
    return {
        "background": COLORS["gray"]["900"],
        "border": f"2px solid {COLORS['primary']['500']}30",
        "color": COLORS["gray"]["100"],
        "border_radius": RADIUS["md"],
        "padding": SPACING["2"],
        "_focus": {
            "border_color": COLORS["primary"]["400"],
            "box_shadow": f"0 0 0 3px {COLORS['primary']['500']}25",
            "outline": "none"
        },
        "_placeholder": {"color": COLORS["gray"]["500"]}
    }

def card_perfil() -> rx.Component:
    """Perfil completo: diseño premium con glassmorphism + responsive"""
    return rx.box(
        rx.vstack(
            # === HEADER: Rol + Estado Laboral (destacado) ===
            rx.hstack(
                # Rol (único)
                rx.box(
                    rx.text(
                        f"ROL: {AppState.rol_usuario.upper()}",
                        size="2",
                        weight="bold",
                        color=COLORS["primary"]["300"],
                        style={
                            "padding": "6px 14px",
                            "border_radius": RADIUS["lg"],
                            "background": f"{COLORS['primary']['500']}15",
                            "border": f"1px solid {COLORS['primary']['600']}40",
                            "font_size": "0.85rem",
                            "backdrop_filter": "blur(4px)",
                            "box_shadow": f"0 1px 2px {COLORS['gray']['900']}60"
                        }
                    )
                ),
                # Estado laboral
                rx.box(
                    rx.text(
                        AppState.estado_laboral_str.upper(),
                        size="1",
                        weight="bold",
                        color=rx.cond(
                            AppState.estado_laboral_activo,
                            COLORS["success"]["300"],
                            COLORS["error"]["400"]
                        ),
                        style={
                            "padding": "4px 12px",
                            "border_radius": RADIUS["md"],
                            "background": rx.cond(
                                AppState.estado_laboral_activo,
                                f"{COLORS['success']['500']}10",
                                f"{COLORS['error']['500']}10"
                            ),
                            "border": rx.cond(AppState.estado_laboral_activo,f"1px solid {COLORS['success']['600']}30", f"1px solid {COLORS['error']['600']}30"),
                            "font_size": "0.8rem"
                        }
                    )
                ),
                spacing="3",
                width="100%",
                justify="between",
                wrap="wrap"
            ),

            # === GRID: 1 → 2 → 3 columnas ===
            rx.grid(
                # COL 1: Datos Personales
                rx.vstack(
                    _readonly_input(
                        "Nombre Completo",
                        AppState.formulario_perfil.get("nombre_completo", ""),
                        special_style=readonly_style()
                    ),
                    rx.cond(
                        AppState.formulario_perfil.get("numero_documento", ""),
                        _readonly_input(
                            "Documento",
                            f"{AppState.formulario_perfil.get('tipo_documento', '')} {AppState.formulario_perfil.get('numero_documento', '')}",
                            help_text="No editable por seguridad",
                            special_style=readonly_style()
                        )
                    ),
                    rx.cond(
                        AppState.formulario_perfil.get("fecha_nacimiento", ""),
                        _readonly_input(
                            "Nacimiento",
                            AppState.formulario_perfil.get("fecha_nacimiento", ""),
                            special_style=readonly_style()
                        )
                    ),
                    spacing="3",
                    width="100%"
                ),

                # COL 2: Datos Laborales
                rx.vstack(
                    rx.cond(
                        AppState.formulario_perfil.get("especialidad", ""),
                        _readonly_input(
                            "Especialidad",
                            AppState.formulario_perfil.get("especialidad", ""),
                            help_text="Especialidad médica",
                            special_style=readonly_style()
                        )
                    ),
                    rx.cond(
                        AppState.formulario_perfil.get("numero_licencia", ""),
                        _readonly_input(
                            "Licencia",
                            AppState.formulario_perfil.get("numero_licencia", ""),
                            help_text="Licencia profesional",
                            special_style=readonly_style()
                        )
                    ),
                    rx.cond(
                        AppState.formulario_perfil.get("fecha_contratacion", ""),
                        _readonly_input(
                            "Contratación",
                            AppState.formulario_perfil.get("fecha_contratacion", ""),
                            special_style=readonly_style()
                        )
                    ),
                    spacing="3",
                    width="100%"
                ),

                # COL 3: Contacto Editable
                rx.vstack(
                    rx.vstack(
                        rx.text("Celular *", size="2", weight="bold", color=COLORS["gray"]["200"]),
                        rx.input(
                            value=AppState.formulario_perfil.get("celular", ""),
                            on_change=lambda v: AppState.actualizar_campo_perfil("celular", v),
                            placeholder="+58 412 1234567",
                            style=editable_input_style()
                        ),
                        rx.cond(
                            AppState.errores_validacion.get("celular"),
                            rx.text(AppState.errores_validacion.get("celular"), color=COLORS["error"]["400"], size="1")
                        ),
                        rx.text("Formato: +58 412 1234567", size="1", color=COLORS["gray"]["500"]),
                        spacing="1"
                    ),
                    rx.vstack(
                        rx.text("Dirección *", size="2", weight="bold", color=COLORS["gray"]["200"]),
                        rx.text_area(
                            value=AppState.formulario_perfil.get("direccion", ""),
                            on_change=lambda v: AppState.actualizar_campo_perfil("direccion", v),
                            placeholder="Dirección completa",
                            rows="2",
                            style=editable_input_style()
                        ),
                        rx.cond(
                            AppState.errores_validacion.get("direccion"),
                            rx.text(AppState.errores_validacion.get("direccion"), color=COLORS["error"]["400"], size="1")
                        ),
                        rx.text("Máx. 200 caracteres", size="1", color=COLORS["gray"]["500"]),
                        spacing="1"
                    ),
                    spacing="3",
                    width="100%"
                ),

                columns=rx.breakpoints(initial="1", sm="1", md="2", lg="3"),
                spacing="5",
                width="100%"
            ),

            # === BOTONES ===
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
                        secondary_button("Cancelar", icon="x", on_click=AppState.cancelar_edicion),
                        spacing="3"
                    ),
                    rx.text("Sin cambios pendientes", color=COLORS["gray"]["500"], size="2")
                ),
                width="100%",
                justify="start",
                margin_top="5"
            ),

            # === SEGURIDAD ===
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("shield", size=22, color=COLORS["warning"]["400"]),
                        rx.text("Seguridad", size="3", weight="bold", color=COLORS["gray"]["200"]),
                        spacing="2"
                    ),
                    rx.grid(
                        rx.box(
                            secondary_button(
                                "Cambiar Contraseña",
                                icon="lock",
                                on_click=AppState.abrir_modal_cambio_password,
                            ),
                            padding="14px",
                            background=f"{COLORS['gray']['800']}60",
                            border_radius=RADIUS["lg"],
                            border=f"1px solid {COLORS['gray']['700']}",
                            _hover={"background": f"{COLORS['gray']['700']}40"}
                        ),
                        rx.box(
                            secondary_button(
                                "Cambiar Email",
                                icon="mail",
                                on_click=AppState.abrir_modal_cambio_email
                            ),
                            padding="14px",
                            background=f"{COLORS['gray']['800']}60",
                            border_radius=RADIUS["lg"],
                            border=f"1px solid {COLORS['gray']['700']}",
                            _hover={"background": f"{COLORS['gray']['700']}40"}
                        ),
                        columns=rx.breakpoints(initial="1", md="2"),
                        spacing="3",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%",
                    padding_top="5",
                    border_top=f"1px dashed {COLORS['gray']['700']}"
                )
            ),

            spacing="6",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        # padding=SPACING["6"],
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
                card_perfil(),
                spacing="6",
                width="100%"
            )
        ),

        # Modales
        modal_cambiar_password(),
        modal_cambiar_email()
    )
