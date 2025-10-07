"""
🚀 BARRA DE ESTADO ODONTOGRAMA V3.0
====================================

Componente visual que muestra el estado del odontograma con:
- Indicador de cache (activo/expirado)
- Contador de cambios pendientes
- Último guardado
- Botones de acción (Guardar/Descartar)
- Auto-guardado activo

Usado en: intervencion_page_v2.py
"""

import reflex as rx
from dental_system.state.estado_odontologia import EstadoOdontologia


def odontograma_status_bar_v3() -> rx.Component:
    """
    📊 BARRA DE ESTADO ODONTOGRAMA V3.0

    Muestra información en tiempo real sobre el estado del odontograma
    """
    return rx.box(
        rx.hstack(
            # 🎯 SECCIÓN IZQUIERDA: Indicadores de estado
            rx.hstack(
                # Indicador de cache
                rx.cond(
                    EstadoOdontologia.odontograma_cargando,
                    rx.hstack(
                        rx.spinner(size="2"),
                        rx.text("Cargando odontograma...", size="2", weight="medium"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("database", size=16, color="green"),
                        rx.text("Cache activo", size="2", color="green"),
                        rx.badge(
                            "5 min TTL",
                            size="1",
                            color_scheme="green",
                            variant="soft"
                        ),
                        spacing="2",
                        align="center"
                    )
                ),

                # Separador
                rx.divider(orientation="vertical", height="24px"),

                # Contador de cambios pendientes
                rx.cond(
                    EstadoOdontologia.cambios_sin_guardar,
                    rx.hstack(
                        rx.icon("circle-alert", size=16, color="orange"),
                        rx.text(
                            f"cambios sin guardar",
                            size="2",
                            weight="medium",
                            color="orange"
                        ),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("circle-check", size=16, color="green"),
                        rx.text("Sin cambios pendientes", size="2", color="gray"),
                        spacing="2",
                        align="center"
                    )
                ),

                # Auto-guardado activo
                # rx.cond(
                #     EstadoOdontologia.auto_guardado_activo,
                #     rx.hstack(
                #         rx.icon("clock", size=14, color="blue"),
                #         rx.text("Auto-guardado: ON", size="1", color="blue"),
                #         spacing="1",
                #         align="center"
                #     ),
                #     rx.fragment()
                # ),

                spacing="4",
                align="center"
            ),

            # 📍 SECCIÓN DERECHA: Botones de acción
            rx.hstack(
                # TODO V3.0: Botón descartar temporalmente deshabilitado por problemas de compilación
                # El método descartar_cambios_pendientes() necesita refactoring para trabajar con Reflex
                # rx.cond(
                #     EstadoOdontologia.cambios_sin_guardar,
                #     rx.button(
                #         rx.icon("x", size=16),
                #         "Descartar",
                #         on_click=EstadoOdontologia.descartar_cambios_pendientes,
                #         size="2",
                #         variant="soft",
                #         color_scheme="gray"
                #     ),
                #     rx.fragment()
                # ),

                # TODO V3.0: Botón guardar temporalmente deshabilitado
                # El método guardar_cambios_batch() necesita @rx.event(background=True)
                # y refactoring completo con async with self:
                # rx.button(
                #     rx.cond(
                #         EstadoOdontologia.odontograma_guardando,
                #         rx.spinner(size="2"),
                #         rx.icon("save", size=16)
                #     ),
                #     rx.cond(
                #         EstadoOdontologia.odontograma_guardando,
                #         "Guardando...",
                #         "Guardar cambios"
                #     ),
                #     on_click=EstadoOdontologia.guardar_cambios_batch,
                #     disabled=EstadoOdontologia.odontograma_guardando | ~EstadoOdontologia.cambios_sin_guardar,
                #     size="2",
                #     color_scheme="blue"
                # ),

                # WORKAROUND TEMPORAL: Mensaje de estado
                # rx.cond(
                #     EstadoOdontologia.auto_guardado_activo,
                #     rx.badge(
                #         "Auto-guardado activo",
                #         color_scheme="green",
                #         size="2"
                #     ),
                #     rx.badge(
                #         "Guardado manual deshabilitado",
                #         color_scheme="gray",
                #         size="2"
                #     ),
                # ),

                spacing="2",
                align="center"
            ),

            justify="between",
            align="center",
            width="100%"
        ),

        # Error message (si existe)
        rx.cond(
            EstadoOdontologia.odontograma_error != "",
            rx.callout(
                EstadoOdontologia.odontograma_error,
                icon="triangle_alert",
                color_scheme="red",
                size="1",
                width="100%",
                style={"margin_top": "8px"}
            ),
            rx.fragment()
        ),

        # Estilos del contenedor
        padding="12px 16px",
        background="var(--gray-2)",
        border_radius="8px",
        border=f"1px solid var(--gray-4)",
        width="100%"
    )


def odontograma_cache_indicator() -> rx.Component:
    """
    🔄 INDICADOR DE CACHE COMPACTO

    Versión compacta del indicador de cache para usar en otros lugares
    """
    return rx.tooltip(
        rx.badge(
            rx.icon("database", size=12),
            "Cache",
            color_scheme="green",
            variant="soft",
            size="1"
        ),
        content="Odontograma cargado desde cache (5 min TTL)"
    )




def odontograma_stats_panel() -> rx.Component:
    """
    📊 PANEL DE ESTADÍSTICAS ODONTOGRAMA V3.0

    Muestra estadísticas detalladas del odontograma con métricas de cache
    """
    return rx.vstack(
        rx.heading("📊 Estadísticas del Odontograma", size="4"),

        # Grid de métricas
        rx.grid(
            # Métrica 1: Dientes con condiciones
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon("activity", size=18, color="blue"),
                        rx.text("Dientes registrados", size="2", color="gray"),
                        justify="between",
                        width="100%"
                    ),
                    rx.text(
                        f"{len(EstadoOdontologia.condiciones_por_diente)}",
                        size="6",
                        weight="bold",
                        color="blue"
                    ),
                    align="start",
                    spacing="2",
                    width="100%"
                ),
                size="1"
            ),

            # Métrica 2: Cambios pendientes
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon("edit", size=18, color="orange"),
                        rx.text("Cambios pendientes", size="2", color="gray"),
                        justify="between",
                        width="100%"
                    ),
                    # rx.text(
                    #     f"{EstadoOdontologia.contador_cambios_pendientes}",
                    #     size="6",
                    #     weight="bold",
                    #     color="orange"
                    # ),
                    align="start",
                    spacing="2",
                    width="100%"
                ),
                size="1"
            ),

            # Métrica 3: Estado de cache
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon("database", size=18, color="green"),
                        rx.text("Cache activo", size="2", color="gray"),
                        justify="between",
                        width="100%"
                    ),
                    # rx.text(
                    #     rx.cond(
                    #         len(EstadoOdontologia.odontograma_cache) > 0,
                    #         "Activo",
                    #         "Vacío"
                    #     ),
                    #     size="6",
                    #     weight="bold",
                    #     color="green"
                    # ),
                    align="start",
                    spacing="2",
                    width="100%"
                ),
                size="1"
            ),

            # Métrica 4: Auto-guardado
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon("clock", size=18, color="purple"),
                        rx.text("Auto-guardado", size="2", color="gray"),
                        justify="between",
                        width="100%"
                    ),
                    # rx.text(
                    #     rx.cond(
                    #         EstadoOdontologia.auto_guardado_activo,
                    #         "Activo",
                    #         "Inactivo"
                    #     ),
                    #     size="6",
                    #     weight="bold",
                    #     color="purple"
                    # ),
                    align="start",
                    spacing="2",
                    width="100%"
                ),
                size="1"
            ),

            columns="4",
            spacing="3",
            width="100%"
        ),

        # Información adicional
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("info", size=14),
                    rx.text("Información del sistema", size="2", weight="medium"),
                    spacing="2"
                ),
                rx.text(
                    "• Cache TTL: 5 minutos",
                    size="1",
                    color="gray"
                ),
                rx.text(
                    "• Auto-guardado: cada 30 segundos",
                    size="1",
                    color="gray"
                ),
                rx.text(
                    "• Batch updates: optimizado para múltiples cambios",
                    size="1",
                    color="gray"
                ),
                spacing="2",
                align="start"
            ),
            padding="12px",
            background="var(--gray-2)",
            border_radius="6px",
            width="100%"
        ),

        spacing="4",
        width="100%"
    )


def odontograma_action_buttons() -> rx.Component:
    """
    🎮 BOTONES DE ACCIÓN PRINCIPALES V3.0

    Botones de acción rápida para el odontograma
    """
    return rx.hstack(
        # Guardar cambios
        rx.button(
            rx.icon("save", size=18),
            "Guardar cambios",
            on_click=EstadoOdontologia.guardar_cambios_batch,
            disabled=~EstadoOdontologia.cambios_sin_guardar | EstadoOdontologia.odontograma_guardando,
            size="3",
            color_scheme="blue",
            variant="solid"
        ),

        # Descartar cambios
        rx.button(
            rx.icon("x", size=18),
            "Descartar",
            # on_click=EstadoOdontologia.descartar_cambios_pendientes,
            disabled=~EstadoOdontologia.cambios_sin_guardar,
            size="3",
            variant="soft",
            color_scheme="gray"
        ),

        # Invalidar cache
        rx.button(
            rx.icon("refresh-cw", size=18),
            "Recargar",
            # on_click=lambda: EstadoOdontologia.invalidar_cache_odontograma(
            #     EstadoOdontologia.paciente_actual.id
            # ),
            size="3",
            variant="ghost"
        ),

        spacing="3",
        justify="end",
        width="100%"
    )
