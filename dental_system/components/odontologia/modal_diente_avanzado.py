"""
Modal Avanzado de Diente con 4 Tabs Especializados
Modal detallado para edición completa de diente individual
"""
import reflex as rx
from typing import List, Dict, Any

# Imports del sistema
from dental_system.models.odontologia_avanzado_models import (
    DienteInteractivoModel,
    CondicionCaraModel,
    TipoCondicion,
    SeveridadCondicion,
    CaraDiente
)
from dental_system.state.app_state import AppState
from dental_system.components.odontologia.diente_interactivo import diente_interactivo_grande
from dental_system.styles.themes import COLORS, DARK_THEME, SHADOWS


def modal_diente_avanzado() -> rx.Component:
    """
    Modal principal con 4 tabs especializados para diente seleccionado

    Tabs:
    1. Superficies - Edición interactiva de condiciones por cara
    2. Historial - Timeline de cambios del diente
    3. Tratamientos - Plan de tratamiento y costos
    4. Notas - Notas clínicas y observaciones

    Returns:
        Modal completo con navegación por tabs
    """
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Modal Trigger", style={"display": "none"})  # Trigger invisible
        ),

        rx.dialog.content(
            # =============================================
            # HEADER DEL MODAL
            # =============================================
            rx.dialog.header(
                rx.hstack(
                    # Información del diente
                    rx.vstack(
                        rx.heading(
                            f"Diente {AppState.numero_diente_seleccionado}",
                            size="6",
                            color=COLORS["gray"]["100"]
                        ),
                        rx.cond(
                            AppState.diente_seleccionado,
                            rx.text(
                                AppState.diente_seleccionado.nombre_diente,
                                size="3",
                                color=COLORS["gray"]["400"]
                            )
                        ),
                        spacing="1",
                        align="start"
                    ),

                    rx.spacer(),

                    # Badges de estado
                    rx.hstack(
                        rx.cond(
                            AppState.diente_seleccionado,
                            rx.cond(
                                AppState.diente_seleccionado.tiene_condiciones,
                                rx.badge(
                                    f"{AppState.diente_seleccionado.numero_condiciones_activas} condiciones",
                                    color_scheme="orange",
                                    size="2"
                                ),
                                rx.badge(
                                    "Sano",
                                    color_scheme="green",
                                    size="2"
                                )
                            )
                        ),

                        rx.cond(
                            AppState.modo_edicion,
                            rx.badge(
                                "Modo Edición",
                                color_scheme="blue",
                                size="2"
                            )
                        ),

                        spacing="2"
                    ),

                    # Botón cerrar
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            color_scheme="gray",
                            on_click=AppState.cerrar_modal_diente
                        )
                    ),

                    justify="between",
                    align="start",
                    width="100%"
                )
            ),

            # =============================================
            # NAVEGACIÓN POR TABS
            # =============================================
            rx.tabs.root(
                # Lista de tabs
                rx.tabs.list(
                    rx.tabs.trigger(
                        "Superficies",
                        value="superficies",
                        color=COLORS["primary"]["400"]
                    ),
                    rx.tabs.trigger(
                        "Historial",
                        value="historial",
                        color=COLORS["blue"]["400"]
                    ),
                    rx.tabs.trigger(
                        "Tratamientos",
                        value="tratamientos",
                        color=COLORS["green"]["400"]
                    ),
                    rx.tabs.trigger(
                        "Notas",
                        value="notas",
                        color=COLORS["purple"]["400"]
                    ),
                    justify="start"
                ),

                # =============================================
                # TAB 1: SUPERFICIES
                # =============================================
                rx.tabs.content(
                    tab_superficies_diente(),
                    value="superficies"
                ),

                # =============================================
                # TAB 2: HISTORIAL
                # =============================================
                rx.tabs.content(
                    tab_historial_diente(),
                    value="historial"
                ),

                # =============================================
                # TAB 3: TRATAMIENTOS
                # =============================================
                rx.tabs.content(
                    tab_tratamientos_diente(),
                    value="tratamientos"
                ),

                # =============================================
                # TAB 4: NOTAS
                # =============================================
                rx.tabs.content(
                    tab_notas_diente(),
                    value="notas"
                ),

                default_value="superficies",
                orientation="horizontal",
                value=AppState.tab_activo_diente,
                on_value_change=AppState.cambiar_tab_modal
            ),

            # =============================================
            # FOOTER CON ACCIONES
            # =============================================
            rx.dialog.footer(
                rx.hstack(
                    # Acciones de diente completo
                    rx.button(
                        "Resetear Diente",
                        left_icon="refresh_cw",
                        variant="outline",
                        color_scheme="red",
                        on_click=AppState.resetear_diente_completo,
                        disabled=~AppState.modo_edicion
                    ),

                    rx.spacer(),

                    # Estado de guardado
                    rx.cond(
                        AppState.guardando_cambios,
                        rx.hstack(
                            rx.spinner(size="1"),
                            rx.text("Guardando...", size="2", color=COLORS["gray"]["400"]),
                            spacing="2"
                        ),
                        rx.cond(
                            AppState.hay_cambios_sin_guardar,
                            rx.text("Cambios sin guardar", size="2", color=COLORS["orange"]["400"]),
                            rx.text("Todo guardado", size="2", color=COLORS["green"]["400"])
                        )
                    ),

                    # Botones principales
                    rx.button(
                        "Cerrar",
                        variant="outline",
                        on_click=AppState.cerrar_modal_diente
                    ),

                    spacing="3",
                    justify="between",
                    width="100%"
                )
            ),

            # Configuración del modal
            max_width="900px",
            width="95vw",
            max_height="90vh",
            background=f"linear-gradient(135deg, {DARK_THEME['colors']['surface']} 0%, {DARK_THEME['colors']['surface_secondary']} 100%)",
            border=f"1px solid {DARK_THEME['colors']['border']}",
            box_shadow="0 25px 50px rgba(0, 0, 0, 0.5)"
        ),

        open=AppState.show_modal_diente
    )


def tab_superficies_diente() -> rx.Component:
    """
    Tab de superficies - Edición interactiva por cara

    Contenido:
    - Diente grande interactivo
    - Selector de condiciones
    - Información detallada por cara
    """
    return rx.vstack(
        # Diente interactivo grande
        rx.center(
            rx.cond(
                AppState.diente_seleccionado,
                diente_interactivo_grande(AppState.diente_seleccionado),
                rx.text("No hay diente seleccionado", color=COLORS["gray"]["400"])
            ),
            margin_bottom="6"
        ),

        # Información de caras
        rx.cond(
            AppState.diente_seleccionado,
            detalle_caras_diente()
        ),

        spacing="6",
        padding="6",
        width="100%"
    )


def detalle_caras_diente() -> rx.Component:
    """Detalle de todas las caras del diente"""
    return rx.grid(
        # Cara Oclusal
        cara_detalle_card(
            "Oclusal",
            AppState.diente_seleccionado.cara_oclusal,
            "🦷"
        ),

        # Cara Mesial
        cara_detalle_card(
            "Mesial",
            AppState.diente_seleccionado.cara_mesial,
            "⬅️"
        ),

        # Cara Distal
        cara_detalle_card(
            "Distal",
            AppState.diente_seleccionado.cara_distal,
            "➡️"
        ),

        # Cara Vestibular
        cara_detalle_card(
            "Vestibular",
            AppState.diente_seleccionado.cara_vestibular,
            "⬆️"
        ),

        # Cara Lingual
        cara_detalle_card(
            "Lingual",
            AppState.diente_seleccionado.cara_lingual,
            "⬇️"
        ),

        columns="2",
        spacing="4",
        width="100%"
    )


def cara_detalle_card(nombre_cara: str, cara: rx.Var[CondicionCaraModel], icono: str) -> rx.Component:
    """
    Card detallada de una cara específica

    Args:
        nombre_cara: Nombre de la cara
        cara: Modelo de la cara
        icono: Emoji representativo

    Returns:
        Card con información detallada
    """
    return rx.card(
        rx.vstack(
            # Header de la cara
            rx.hstack(
                rx.text(icono, font_size="20px"),
                rx.heading(nombre_cara, size="4", color=COLORS["gray"]["100"]),
                rx.spacer(),
                rx.box(
                    width="20px",
                    height="20px",
                    background=cara.color_hex,
                    border_radius="4px",
                    border="1px solid rgba(255,255,255,0.3)"
                ),
                justify="between",
                align="center",
                width="100%"
            ),

            # Estado de la cara
            rx.text(
                cara.descripcion_condicion,
                size="3",
                weight="medium",
                color=rx.cond(
                    cara.tiene_condicion,
                    COLORS["orange"]["400"],
                    COLORS["green"]["400"]
                )
            ),

            # Severidad (si aplica)
            rx.cond(
                cara.tiene_condicion,
                rx.badge(
                    cara.severidad.title(),
                    color_scheme=rx.match(
                        cara.severidad,
                        ("leve", "green"),
                        ("moderada", "orange"),
                        ("severa", "red"),
                        ("critica", "red"),
                        "gray"
                    ),
                    size="1"
                )
            ),

            # Costo estimado
            rx.cond(
                cara.costo_estimado_usd > 0,
                rx.text(
                    f"Costo estimado: ${cara.costo_estimado_usd:.0f}",
                    size="2",
                    color=COLORS["yellow"]["400"]
                )
            ),

            # Notas (si hay)
            rx.cond(
                cara.notas != "",
                rx.text(
                    cara.notas,
                    size="2",
                    color=COLORS["gray"]["400"],
                    style={"font_style": "italic"}
                )
            ),

            # Botón editar (solo en modo edición)
            rx.cond(
                AppState.modo_edicion,
                rx.button(
                    "Editar",
                    left_icon="edit",
                    size="2",
                    variant="outline",
                    color_scheme="blue",
                    on_click=lambda: AppState.seleccionar_cara_diente(nombre_cara.lower()),
                    width="100%"
                )
            ),

            spacing="3",
            align="start"
        ),

        padding="4",
        cursor="pointer" if AppState.modo_edicion else "default",
        on_click=lambda: AppState.seleccionar_cara_diente(nombre_cara.lower()) if AppState.modo_edicion else None,
        _hover={
            "transform": "scale(1.02)" if AppState.modo_edicion else "none",
            "box_shadow": SHADOWS["lg"] if AppState.modo_edicion else "none"
        }
    )


def tab_historial_diente() -> rx.Component:
    """
    Tab de historial - Timeline de cambios del diente

    Contenido:
    - Timeline de modificaciones
    - Comparación entre versiones
    - Fechas y responsables
    """
    return rx.vstack(
        rx.heading("Historial de Cambios", size="5", color=COLORS["gray"]["100"]),

        # Timeline simulado (en implementación real vendría de BD)
        rx.vstack(
            historial_item(
                "2024-09-18 14:30",
                "Condición aplicada",
                "Caries detectada en superficie oclusal",
                "Dr. Smith",
                "warning"
            ),

            historial_item(
                "2024-09-15 10:15",
                "Revisión general",
                "Diente evaluado sin alteraciones",
                "Dr. García",
                "info"
            ),

            historial_item(
                "2024-09-01 09:00",
                "Creación inicial",
                "Diente registrado en odontograma",
                "Sistema",
                "success"
            ),

            spacing="3",
            width="100%"
        ),

        spacing="4",
        padding="6",
        width="100%"
    )


def historial_item(fecha: str, accion: str, descripcion: str, responsable: str, tipo: str) -> rx.Component:
    """Item individual del historial"""
    return rx.card(
        rx.hstack(
            # Indicador de tiempo
            rx.vstack(
                rx.box(
                    width="12px",
                    height="12px",
                    background=rx.match(
                        tipo,
                        ("success", COLORS["green"]["500"]),
                        ("warning", COLORS["orange"]["500"]),
                        ("info", COLORS["blue"]["500"]),
                        COLORS["gray"]["500"]
                    ),
                    border_radius="50%"
                ),
                rx.box(
                    width="2px",
                    height="40px",
                    background=COLORS["gray"]["600"],
                    margin_x="5px"
                ),
                spacing="0"
            ),

            # Contenido
            rx.vstack(
                rx.hstack(
                    rx.text(accion, size="3", weight="medium", color=COLORS["gray"]["100"]),
                    rx.spacer(),
                    rx.text(fecha, size="2", color=COLORS["gray"]["400"]),
                    justify="between",
                    width="100%"
                ),

                rx.text(descripcion, size="2", color=COLORS["gray"]["300"]),

                rx.text(
                    f"Por: {responsable}",
                    size="1",
                    color=COLORS["gray"]["500"],
                    style={"font_style": "italic"}
                ),

                spacing="1",
                align="start",
                flex="1"
            ),

            spacing="3",
            align="start",
            width="100%"
        ),

        padding="3"
    )


def tab_tratamientos_diente() -> rx.Component:
    """
    Tab de tratamientos - Plan de tratamiento y costos

    Contenido:
    - Tratamientos requeridos
    - Costos estimados
    - Prioridades
    """
    return rx.vstack(
        rx.heading("Plan de Tratamiento", size="5", color=COLORS["gray"]["100"]),

        # Resumen de costos
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.text("Costo Total Estimado", size="3", weight="medium"),
                    rx.spacer(),
                    rx.cond(
                        AppState.diente_seleccionado,
                        rx.text(
                            f"${AppState.diente_seleccionado.costo_total_estimado:.0f}",
                            size="4",
                            weight="bold",
                            color=COLORS["green"]["400"]
                        )
                    ),
                    justify="between",
                    width="100%"
                ),

                rx.divider(),

                # Lista de tratamientos necesarios
                rx.cond(
                    AppState.diente_seleccionado,
                    rx.cond(
                        AppState.diente_seleccionado.tiene_condiciones,
                        tratamientos_necesarios(),
                        rx.text(
                            "✅ No se requieren tratamientos",
                            size="3",
                            color=COLORS["green"]["400"]
                        )
                    )
                ),

                spacing="3",
                width="100%"
            ),

            padding="4"
        ),

        spacing="4",
        padding="6",
        width="100%"
    )


def tratamientos_necesarios() -> rx.Component:
    """Lista de tratamientos necesarios según condiciones"""
    return rx.vstack(
        rx.text("Tratamientos Requeridos:", size="3", weight="medium"),

        # Simulación de tratamientos basados en condiciones
        tratamiento_item("Restauración Oclusal", "Caries superficie oclusal", 150, "Alta"),
        tratamiento_item("Profilaxis", "Limpieza general", 80, "Media"),
        tratamiento_item("Aplicación Flúor", "Prevención", 40, "Baja"),

        spacing="2",
        width="100%"
    )


def tratamiento_item(nombre: str, descripcion: str, costo: int, prioridad: str) -> rx.Component:
    """Item individual de tratamiento"""
    return rx.hstack(
        rx.vstack(
            rx.text(nombre, size="2", weight="medium", color=COLORS["gray"]["100"]),
            rx.text(descripcion, size="1", color=COLORS["gray"]["400"]),
            spacing="0",
            align="start"
        ),

        rx.spacer(),

        rx.badge(
            prioridad,
            color_scheme=rx.match(
                prioridad,
                ("Alta", "red"),
                ("Media", "orange"),
                ("Baja", "green"),
                "gray"
            ),
            size="1"
        ),

        rx.text(f"${costo}", size="2", weight="medium", color=COLORS["green"]["400"]),

        justify="between",
        align="center",
        width="100%",
        padding="2",
        border_bottom=f"1px solid {DARK_THEME['colors']['border']}"
    )


def tab_notas_diente() -> rx.Component:
    """
    Tab de notas - Notas clínicas y observaciones

    Contenido:
    - Editor de notas
    - Observaciones clínicas
    - Historia del paciente relevante
    """
    return rx.vstack(
        rx.heading("Notas Clínicas", size="5", color=COLORS["gray"]["100"]),

        # Editor de notas (solo en modo edición)
        rx.cond(
            AppState.modo_edicion,
            rx.vstack(
                rx.text("Agregar Observación:", size="3", weight="medium"),
                rx.text_area(
                    placeholder="Escriba sus observaciones clínicas sobre este diente...",
                    height="120px",
                    width="100%"
                ),
                rx.button(
                    "Guardar Nota",
                    left_icon="save",
                    color_scheme="blue",
                    size="2"
                ),
                spacing="3",
                width="100%"
            )
        ),

        # Notas existentes
        rx.vstack(
            rx.text("Observaciones Anteriores:", size="3", weight="medium"),

            nota_item(
                "2024-09-18",
                "Caries inicial detectada en superficie oclusal. Paciente refiere sensibilidad ocasional.",
                "Dr. Smith"
            ),

            nota_item(
                "2024-09-15",
                "Revisión preventiva. Diente en buen estado general.",
                "Dr. García"
            ),

            spacing="3",
            width="100%"
        ),

        spacing="6",
        padding="6",
        width="100%"
    )


def nota_item(fecha: str, contenido: str, autor: str) -> rx.Component:
    """Item individual de nota clínica"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(fecha, size="2", weight="medium", color=COLORS["gray"]["300"]),
                rx.spacer(),
                rx.text(autor, size="2", color=COLORS["blue"]["400"]),
                justify="between",
                width="100%"
            ),

            rx.text(
                contenido,
                size="2",
                color=COLORS["gray"]["200"],
                line_height="1.5"
            ),

            spacing="2",
            align="start"
        ),

        padding="3",
        background=f"{DARK_THEME['colors']['surface']}60"
    )


# ===========================================
# EXPORTS
# ===========================================

__all__ = [
    "modal_diente_avanzado",
    "tab_superficies_diente",
    "tab_historial_diente",
    "tab_tratamientos_diente",
    "tab_notas_diente"
]