"""
🌙 PÁGINA DE REPORTES V1.0
============================================================
Reportes especializados por rol:
- GERENTE: Reportes financieros y operativos completos
- ODONTÓLOGO: Reportes clínicos personales
- ADMINISTRADOR: Reportes operativos del día a día
============================================================
"""

import reflex as rx
from dental_system.state.app_state import AppState
from dental_system.components.common import (
    medical_page_layout, page_header, stat_card, refresh_button,
    ranking_table, filtro_fecha_rango, mini_stat_card, horizontal_bar_chart
)
from dental_system.components.charts import pie_chart_card, graficas_reportes, graficas_reportes_odontologo, graficas_reportes_admin
from dental_system.styles.themes import (
    COLORS, SHADOWS, DARK_THEME, dark_crystal_card, SPACING, RADIUS, GRADIENTS
)

# ==========================================
# 👔 LAYOUT GERENTE
# ==========================================

def ranking_odontologos_gerente() -> rx.Component:
    """🏆 Ranking de odontólogos con toggle de ordenamiento"""
    return rx.box(
        rx.vstack(
            # Header con toggle
            rx.hstack(
                rx.heading(
                    "Ranking de Odontólogos",
                    size="5",
                    weight="bold",
                    style={"color": DARK_THEME["colors"]["text_primary"]}
                ),
                rx.spacer(),
                rx.segmented_control.root(
                    rx.segmented_control.item("Intervenciones", value="intervenciones"),
                    rx.segmented_control.item("Ingresos", value="ingresos"),
                    default_value=AppState.ordenar_odontologos_por,
                    on_change=AppState.cambiar_orden_ranking_odontologos,
                    radius="full",
                    size="2"
                ),
                width="100%",
                align="center",
                margin_bottom="4"
            ),

            # Tabla de ranking (cambia dinámicamente según ordenamiento)
            rx.cond(
                AppState.ordenar_odontologos_por == "intervenciones",
                ranking_table(
                    title="",
                    data=AppState.ranking_odontologos,
                    columns=["nombre", "total_intervenciones", "total_ingresos"],
                    show_progress_bar=True,
                    max_items=10
                ),
                ranking_table(
                    title="",
                    data=AppState.ranking_odontologos,
                    columns=["nombre", "total_ingresos", "total_intervenciones"],
                    show_progress_bar=True,
                    max_items=10
                )
            ),

            spacing="2",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )

def layout_gerente() -> rx.Component:
    """📊 Layout completo de reportes para GERENTE - V2.0 CON DATOS COMPLETOS"""
    return rx.vstack(
        # Filtro de fecha
        filtro_fecha_rango(),

        # ========================================
        # SECCIÓN 1: 8 CARDS DEL DASHBOARD
        # ========================================
        rx.grid(
            stat_card(
                title="Ingresos del Mes",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"${AppState.dashboard_cards_gerente.get('ingresos_mes', 0):,.2f}",
                    "$0.00"
                ),
                icon="dollar-sign",
                color=COLORS["success"]["500"]
            ),
            stat_card(
                title="Consultas del Mes",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"{AppState.dashboard_cards_gerente.get('consultas_mes', 0)}",
                    "0"
                ),
                icon="calendar",
                color=COLORS["primary"]["500"]
            ),
            stat_card(
                title="Servicios Aplicados",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"{AppState.dashboard_cards_gerente.get('servicios_aplicados', 0)}",
                    "0"
                ),
                icon="activity",
                color=COLORS["blue"]["500"]
            ),
            stat_card(
                title="Pagos Pendientes",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"{AppState.dashboard_cards_gerente.get('pagos_pendientes_count', 0)} (${AppState.dashboard_cards_gerente.get('pagos_pendientes_monto', 0):,.0f})",
                    "0 ($0)"
                ),
                icon="alert-circle",
                color=COLORS["warning"]["500"]
            ),
            stat_card(
                title="Total Pacientes",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"{AppState.dashboard_cards_gerente.get('total_pacientes', 0)}",
                    "0"
                ),
                icon="users",
                color=COLORS["secondary"]["500"]
            ),
            stat_card(
                title="Pacientes Masculino",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"{AppState.dashboard_cards_gerente.get('pacientes_masculino', 0)}",
                    "0"
                ),
                icon="user",
                color=COLORS["blue"]["500"]
            ),
            stat_card(
                title="Pacientes Femenino",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"{AppState.dashboard_cards_gerente.get('pacientes_femenino', 0)}",
                    "0"
                ),
                icon="user",
                color=COLORS["secondary"]["500"]
            ),
            stat_card(
                title="Consultas Canceladas",
                value=rx.cond(
                    AppState.dashboard_cards_gerente,
                    f"{AppState.dashboard_cards_gerente.get('consultas_canceladas', 0)}",
                    "0"
                ),
                icon="x-circle",
                color=COLORS["error"]["500"]
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="4",
            width="100%",
            margin_bottom="6"
        ),

        # ========================================
        # SECCIÓN 2: RANKINGS (2 COLUMNAS)
        # ========================================
        rx.grid(
            # Ranking de servicios
            ranking_table(
                title="Ranking de Servicios Más Solicitados",
                data=AppState.ranking_servicios,
                columns=["servicio_nombre", "veces_aplicado", "ingresos_generados"],
                show_progress_bar=True,
                max_items=10
            ),

            # Ranking de odontólogos
            ranking_odontologos_gerente(),

            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="6",
            width="100%",
            margin_bottom="6"
        ),

        # ========================================
        # SECCIÓN 3: GRÁFICOS FINANCIEROS (2 COLUMNAS)
        # ========================================
        rx.grid(
            # Métodos de pago (horizontal bar)
            horizontal_bar_chart(
                title="Métodos de Pago Más Usados",
                data=AppState.metodos_pago_populares,
                color=COLORS["secondary"]["500"]
            ),

            # Distribución USD vs BS (pie chart con %)
            pie_chart_card(
                title="Distribución USD vs BS",
                data=AppState.datos_grafico_distribucion_pagos,
                subtitle=rx.cond(
                    AppState.distribucion_pagos,
                    f"USD {AppState.distribucion_pagos.get('porcentaje_usd', 0):.1f}% | BS {AppState.distribucion_pagos.get('porcentaje_bs', 0):.1f}%",
                    "USD 0% | BS 0%"
                ),
                height=320
            ),

            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="6",
            width="100%",
            margin_bottom="6"
        ),

        # ========================================
        # SECCIÓN 4: GRÁFICO DE EVOLUCIÓN CON TABS
        # ========================================
        graficas_reportes(),

        spacing="6",
        width="100%"
    )

# ==========================================
# 🦷 LAYOUT ODONTÓLOGO
# ==========================================

def estadisticas_odontograma_odontologo() -> rx.Component:
    """🦷 Estadísticas de odontograma del odontólogo"""
    return rx.grid(
        mini_stat_card(
            title="Condiciones Registradas",
            items=[
                {"label": "Caries", "value": AppState.estadisticas_odontograma_odontologo.get("caries", 0), "color": COLORS["error"]["500"]},
                {"label": "Obturaciones", "value": AppState.estadisticas_odontograma_odontologo.get("obturacion", 0), "color": COLORS["blue"]["500"]},
                {"label": "Coronas", "value": AppState.estadisticas_odontograma_odontologo.get("corona", 0), "color": COLORS["warning"]["500"]},
            ],
            icon="clipboard-list",
            color=COLORS["primary"]["500"]
        ),
        mini_stat_card(
            title="Dientes Tratados",
            items=[
                {"label": "Total dientes", "value": AppState.estadisticas_odontograma_odontologo.get("total_dientes_tratados", 0), "color": COLORS["success"]["500"]},
                {"label": "Superficies", "value": AppState.estadisticas_odontograma_odontologo.get("total_superficies_tratadas", 0), "color": COLORS["secondary"]["500"]},
            ],
            icon="activity",
            color=COLORS["blue"]["500"]
        ),
        columns=rx.breakpoints(initial="1", md="2"),
        spacing="4",
        width="100%"
    )

def tabla_intervenciones_odontologo() -> rx.Component:
    """📋 Tabla de intervenciones del odontólogo con paginación"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "Mis Intervenciones",
                    size="5",
                    weight="bold",
                    style={"color": DARK_THEME["colors"]["text_primary"]}
                ),
                rx.spacer(),
                rx.input(
                    placeholder="Buscar paciente o servicio...",
                    value=AppState.busqueda_intervenciones_odontologo,
                    on_change=AppState.set_busqueda_intervenciones_odontologo,
                    size="2",
                    style={"max_width": "300px"}
                ),
                width="100%",
                align="center",
                margin_bottom="4"
            ),

            # Tabla
            rx.cond(
                AppState.intervenciones_odontologo,
                rx.vstack(
                    # Headers
                    rx.hstack(
                        rx.text("Fecha", weight="bold", size="2", style={"flex": "1"}),
                        rx.text("Paciente", weight="bold", size="2", style={"flex": "2"}),
                        rx.text("Servicio", weight="bold", size="2", style={"flex": "2"}),
                        rx.text("Diente", weight="bold", size="2", style={"flex": "1"}),
                        rx.text("Monto", weight="bold", size="2", style={"flex": "1", "text_align": "right"}),
                        width="100%",
                        padding="3",
                        border_bottom=f"2px solid {DARK_THEME['colors']['border']}",
                        style={"color": DARK_THEME["colors"]["text_secondary"]}
                    ),

                    # Rows
                    rx.foreach(
                        AppState.intervenciones_odontologo,
                        lambda interv: rx.hstack(
                            rx.text(
                                interv.get("fecha_intervencion", "N/A"),
                                size="2",
                                style={"flex": "1", "color": DARK_THEME["colors"]["text_primary"]}
                            ),
                            rx.text(
                                interv.get("paciente_nombre", "N/A"),
                                size="2",
                                style={"flex": "2", "color": DARK_THEME["colors"]["text_primary"]}
                            ),
                            rx.text(
                                interv.get("servicio_nombre", "N/A"),
                                size="2",
                                style={"flex": "2", "color": DARK_THEME["colors"]["text_secondary"]}
                            ),
                            rx.text(
                                interv.get("diente_numero", "N/A"),
                                size="2",
                                style={"flex": "1", "color": DARK_THEME["colors"]["text_secondary"]}
                            ),
                            rx.text(
                                f"${interv.get('monto_servicio', 0):,.2f}",
                                size="2",
                                weight="medium",
                                style={
                                    "flex": "1",
                                    "text_align": "right",
                                    "color": COLORS["success"]["500"]
                                }
                            ),
                            width="100%",
                            padding="3",
                            border_bottom=f"1px solid {DARK_THEME['colors']['border']}",
                            # _hover={
                            #     "background": DARK_THEME["colors"]["hover"],
                            #     "cursor": "pointer"
                            # }
                        )
                    ),

                    # Paginación
                    rx.hstack(
                        rx.button(
                            "Anterior",
                            on_click=AppState.pagina_anterior_intervenciones,
                            disabled=AppState.pagina_actual_intervenciones == 1,
                            size="2",
                            variant="soft"
                        ),
                        rx.text(
                            f"Página {AppState.pagina_actual_intervenciones} de {AppState.total_paginas_intervenciones}",
                            size="2",
                            style={"color": DARK_THEME["colors"]["text_secondary"]}
                        ),
                        rx.button(
                            "Siguiente",
                            on_click=AppState.pagina_siguiente_intervenciones,
                            disabled=AppState.pagina_actual_intervenciones >= AppState.total_paginas_intervenciones,
                            size="2",
                            variant="soft"
                        ),
                        width="100%",
                        justify="center",
                        align="center",
                        margin_top="4",
                        spacing="4"
                    ),

                    spacing="2",
                    width="100%"
                ),
                rx.center(
                    rx.text(
                        "No hay intervenciones registradas",
                        size="3",
                        style={"color": DARK_THEME["colors"]["text_muted"]}
                    ),
                    padding="8",
                    width="100%"
                )
            ),

            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["blue"]["500"], hover_lift="4px"),
        width="100%"
    )

def layout_odontologo() -> rx.Component:
    """🦷 Layout completo de reportes para ODONTÓLOGO - V2.0 CON DATOS COMPLETOS"""
    return rx.vstack(
        # Filtro de fecha
        filtro_fecha_rango(),

        # ========================================
        # SECCIÓN 1: 7 CARDS DEL DASHBOARD
        # ========================================
        rx.grid(
            stat_card(
                title="Ingresos Totales",
                value=rx.cond(
                    AppState.dashboard_cards_odontologo,
                    f"${AppState.dashboard_cards_odontologo.get('ingresos_total', 0):,.2f}",
                    "$0.00"
                ),
                icon="dollar-sign",
                color=COLORS["success"]["500"]
            ),
            stat_card(
                title="Consultas Realizadas",
                value=rx.cond(
                    AppState.dashboard_cards_odontologo,
                    f"{AppState.dashboard_cards_odontologo.get('num_consultas', 0)}",
                    "0"
                ),
                icon="calendar",
                color=COLORS["primary"]["500"]
            ),
            stat_card(
                title="Servicios Aplicados",
                value=rx.cond(
                    AppState.dashboard_cards_odontologo,
                    f"{AppState.dashboard_cards_odontologo.get('servicios_aplicados', 0)}",
                    "0"
                ),
                icon="activity",
                color=COLORS["blue"]["500"]
            ),
            stat_card(
                title="Consultas Canceladas",
                value=rx.cond(
                    AppState.dashboard_cards_odontologo,
                    f"{AppState.dashboard_cards_odontologo.get('consultas_canceladas', 0)}",
                    "0"
                ),
                icon="x-circle",
                color=COLORS["error"]["500"]
            ),
            stat_card(
                title="Promedio por Consulta",
                value=rx.cond(
                    AppState.dashboard_cards_odontologo,
                    f"${AppState.dashboard_cards_odontologo.get('promedio_por_consulta', 0):,.2f}",
                    "$0.00"
                ),
                icon="trending-up",
                color=COLORS["secondary"]["500"]
            ),
            stat_card(
                title="Pacientes Únicos",
                value=rx.cond(
                    AppState.dashboard_cards_odontologo,
                    f"{AppState.dashboard_cards_odontologo.get('pacientes_unicos', 0)}",
                    "0"
                ),
                icon="users",
                color=COLORS["blue"]["600"]
            ),
            stat_card(
                title="Dientes Tratados",
                value=rx.cond(
                    AppState.dashboard_cards_odontologo,
                    f"{AppState.dashboard_cards_odontologo.get('dientes_tratados', 0)}",
                    "0"
                ),
                icon="smile",
                color=COLORS["info"]["500"]
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
            spacing="4",
            width="100%",
            margin_bottom="6"
        ),

        # ========================================
        # SECCIÓN 2: GRÁFICOS FINANCIEROS (2 COLUMNAS)
        # ========================================
        rx.grid(
            # Métodos de pago (horizontal bar)
            horizontal_bar_chart(
                title="Métodos de Pago Más Usados",
                data=AppState.metodos_pago_odontologo,
                color=COLORS["secondary"]["500"]
            ),

            # Distribución USD vs BS (pie chart con %)
            pie_chart_card(
                title="Distribución USD vs BS",
                data=AppState.datos_grafico_ingresos_odontologo,
                subtitle=rx.cond(
                    AppState.distribucion_ingresos_odontologo,
                    f"USD {AppState.distribucion_ingresos_odontologo.get('porcentaje_usd', 0):.1f}% | BS {AppState.distribucion_ingresos_odontologo.get('porcentaje_bs', 0):.1f}%",
                    "USD 0% | BS 0%"
                ),
                height=320
            ),

            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="6",
            width="100%",
            margin_bottom="6"
        ),

        # ========================================
        # SECCIÓN 3: RANKING DE SERVICIOS (ANCHO COMPLETO)
        # ========================================
        ranking_table(
            title="Mis Servicios Más Realizados",
            data=AppState.ranking_servicios_odontologo,
            columns=["servicio_nombre", "veces_aplicado", "ingresos_generados"],
            show_progress_bar=True,
            max_items=10
        ),

        # ========================================
        # SECCIÓN 4: GRÁFICO DE EVOLUCIÓN CON TABS
        # ========================================
        graficas_reportes_odontologo(),

        # ========================================
        # SECCIÓN 5: ESTADÍSTICAS ODONTOLÓGICAS (3 COLUMNAS)
        # ========================================
        rx.grid(
            # Condiciones más tratadas
            mini_stat_card(
                title="Condiciones Más Tratadas",
                items=AppState.condiciones_mas_tratadas_top5,
                icon="clipboard-list",
                color=COLORS["error"]["500"]
            ),

            # Dientes más intervenidos
            mini_stat_card(
                title="Dientes Más Intervenidos",
                items=AppState.dientes_mas_intervenidos_top5,
                icon="smile",
                color=COLORS["success"]["500"]
            ),

            # Superficies más tratadas
            mini_stat_card(
                title="Superficies Más Tratadas",
                items=AppState.superficies_mas_tratadas_top5,
                icon="layers",
                color=COLORS["warning"]["500"]
            ),

            columns=rx.breakpoints(initial="1", md="3"),
            spacing="6",
            width="100%"
        ),

        spacing="6",
        width="100%"
    )

# ==========================================
# 👤 LAYOUT ADMINISTRADOR
# ==========================================

def consultas_por_estado_admin() -> rx.Component:
    """📊 Consultas por estado para administrador"""
    return rx.grid(
        rx.foreach(
            AppState.consultas_por_estado_dash,
            lambda item: stat_card(
                title=item.get("estado", "N/A"),
                value=item.get("total", 0),
                icon=rx.match(
                    item.get("estado", ""),
                    ("en_espera", "clock"),
                    ("en_atencion", "stethoscope"),
                    ("completada", "check-circle"),
                    ("cancelada", "x-circle"),
                    "activity"
                ),
                color=rx.match(
                    item.get("estado", ""),
                    ("en_espera", COLORS["warning"]["500"]),
                    ("en_atencion", COLORS["blue"]["500"]),
                    ("completada", COLORS["success"]["500"]),
                    ("cancelada", COLORS["error"]["500"]),
                    COLORS["primary"]["500"]
                )
            )
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="4"),
        spacing="4",
        width="100%"
    )

def pagos_pendientes_admin() -> rx.Component:
    """💰 Pagos pendientes para administrador"""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Pagos Pendientes",
                size="5",
                weight="bold",
                style={"color": DARK_THEME["colors"]["text_primary"]},
                margin_bottom="4"
            ),

            rx.cond(
                AppState.pagos_pendientes,
                rx.vstack(
                    rx.foreach(
                        AppState.pagos_pendientes,
                        lambda pago: rx.hstack(
                            rx.vstack(
                                rx.text(
                                    pago.get("paciente_nombre", "N/A"),
                                    weight="bold",
                                    size="3",
                                    style={"color": DARK_THEME["colors"]["text_primary"]}
                                ),
                                rx.text(
                                    f"Consulta: {pago.get('numero_consulta', 'N/A')}",
                                    size="2",
                                    style={"color": DARK_THEME["colors"]["text_secondary"]}
                                ),
                                spacing="1",
                                align="start"
                            ),
                            rx.spacer(),
                            rx.vstack(
                                rx.text(
                                    f"Saldo: ${pago.get('saldo_pendiente', 0):,.2f}",
                                    weight="bold",
                                    size="3",
                                    style={"color": COLORS["error"]["500"]}
                                ),
                                rx.text(
                                    f"Total: ${pago.get('monto_total', 0):,.2f}",
                                    size="2",
                                    style={"color": DARK_THEME["colors"]["text_secondary"]}
                                ),
                                spacing="1",
                                align="end"
                            ),
                            width="100%",
                            padding="3",
                            border_bottom=f"1px solid {DARK_THEME['colors']['border']}",
                            # _hover={
                            #     "background": DARK_THEME["colors"]["hover"],
                            #     "cursor": "pointer"
                            # }
                        )
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.center(
                    rx.text(
                        "No hay pagos pendientes",
                        size="3",
                        style={"color": DARK_THEME["colors"]["text_muted"]}
                    ),
                    padding="8",
                    width="100%"
                )
            ),

            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["warning"]["500"], hover_lift="4px"),
        width="100%"
    )

def tabla_consultas_admin() -> rx.Component:
    """📋 Tabla de consultas para administrador con paginación"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "Consultas del Período",
                    size="5",
                    weight="bold",
                    style={"color": DARK_THEME["colors"]["text_primary"]}
                ),
                rx.spacer(),
                rx.input(
                    placeholder="Buscar consulta...",
                    value=AppState.busqueda_consultas_admin,
                    on_change=AppState.set_busqueda_consultas_admin,
                    size="2",
                    style={"max_width": "300px"}
                ),
                width="100%",
                align="center",
                margin_bottom="4"
            ),

            # Tabla
            rx.cond(
                AppState.consultas_tabla,
                rx.vstack(
                    # Headers
                    rx.hstack(
                        rx.text("N° Consulta", weight="bold", size="2", style={"flex": "1"}),
                        rx.text("Fecha", weight="bold", size="2", style={"flex": "1"}),
                        rx.text("Paciente", weight="bold", size="2", style={"flex": "2"}),
                        rx.text("Odontólogo", weight="bold", size="2", style={"flex": "2"}),
                        rx.text("Estado", weight="bold", size="2", style={"flex": "1"}),
                        width="100%",
                        padding="3",
                        border_bottom=f"2px solid {DARK_THEME['colors']['border']}",
                        style={"color": DARK_THEME["colors"]["text_secondary"]}
                    ),

                    # Rows
                    rx.foreach(
                        AppState.consultas_tabla,
                        lambda cons: rx.hstack(
                            rx.text(
                                cons.get("numero_consulta", "N/A"),
                                size="2",
                                style={"flex": "1", "color": DARK_THEME["colors"]["text_primary"]}
                            ),
                            rx.text(
                                cons.get("fecha_consulta", "N/A"),
                                size="2",
                                style={"flex": "1", "color": DARK_THEME["colors"]["text_primary"]}
                            ),
                            rx.text(
                                cons.get("paciente_nombre", "N/A"),
                                size="2",
                                style={"flex": "2", "color": DARK_THEME["colors"]["text_primary"]}
                            ),
                            rx.text(
                                cons.get("odontologo_nombre", "N/A"),
                                size="2",
                                style={"flex": "2", "color": DARK_THEME["colors"]["text_secondary"]}
                            ),
                            rx.badge(
                                cons.get("estado", "N/A"),
                                variant="soft",
                                color_scheme=rx.match(
                                    cons.get("estado", ""),
                                    ("en_espera", "yellow"),
                                    ("en_atencion", "blue"),
                                    ("completada", "green"),
                                    ("cancelada", "red"),
                                    "gray"
                                ),
                                style={"flex": "1"}
                            ),
                            width="100%",
                            padding="3",
                            border_bottom=f"1px solid {DARK_THEME['colors']['border']}",
                            # _hover={
                            #     "background": DARK_THEME["colors"]["hover"],
                            #     "cursor": "pointer"
                            # }
                        )
                    ),

                    # Paginación
                    rx.hstack(
                        rx.button(
                            "Anterior",
                            on_click=AppState.pagina_anterior_consultas,
                            disabled=AppState.pagina_actual_consultas == 1,
                            size="2",
                            variant="soft"
                        ),
                        rx.text(
                            f"Página {AppState.pagina_actual_consultas} de {AppState.total_paginas_consultas}",
                            size="2",
                            style={"color": DARK_THEME["colors"]["text_secondary"]}
                        ),
                        rx.button(
                            "Siguiente",
                            on_click=AppState.pagina_siguiente_consultas,
                            disabled=AppState.pagina_actual_consultas >= AppState.total_paginas_consultas,
                            size="2",
                            variant="soft"
                        ),
                        width="100%",
                        justify="center",
                        align="center",
                        margin_top="4",
                        spacing="4"
                    ),

                    spacing="2",
                    width="100%"
                ),
                rx.center(
                    rx.text(
                        "No hay consultas para mostrar",
                        size="3",
                        style={"color": DARK_THEME["colors"]["text_muted"]}
                    ),
                    padding="8",
                    width="100%"
                )
            ),

            spacing="4",
            width="100%"
        ),
        **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
        width="100%"
    )

def layout_administrador() -> rx.Component:
    """👤 Layout completo de reportes para ADMINISTRADOR - V2.0 CON DATOS FINANCIEROS"""
    return rx.vstack(
        # Filtro de fecha
        filtro_fecha_rango(),

        # ========================================
        # SECCIÓN 1: 4 CARDS FINANCIEROS
        # ========================================
        rx.grid(
            stat_card(
                title="Ingresos del Período",
                value=rx.cond(
                    AppState.dashboard_cards_admin,
                    f"${AppState.dashboard_cards_admin.get('ingresos_periodo', 0):,.2f}",
                    "$0.00"
                ),
                icon="dollar-sign",
                color=COLORS["success"]["500"]
            ),
            stat_card(
                title="Pagos Realizados",
                value=rx.cond(
                    AppState.dashboard_cards_admin,
                    f"{AppState.dashboard_cards_admin.get('pagos_realizados', 0)}",
                    "0"
                ),
                icon="check-circle",
                color=COLORS["primary"]["500"]
            ),
            stat_card(
                title="Saldo Pendiente",
                value=rx.cond(
                    AppState.dashboard_cards_admin,
                    f"${AppState.dashboard_cards_admin.get('saldo_pendiente', 0):,.2f}",
                    "$0.00"
                ),
                icon="alert-circle",
                color=COLORS["warning"]["500"]
            ),
            stat_card(
                title="Método Más Usado",
                value=rx.cond(
                    AppState.dashboard_cards_admin,
                    f"{AppState.dashboard_cards_admin.get('metodo_mas_usado', 'N/A')}",
                    "N/A"
                ),
                icon="credit-card",
                color=COLORS["blue"]["500"]
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="4",
            width="100%",
            margin_bottom="6"
        ),

        # ========================================
        # SECCIÓN 2: CONSULTAS POR ESTADO
        # ========================================
        rx.box(
            rx.vstack(
                rx.heading(
                    "Estado de Consultas",
                    size="5",
                    weight="bold",
                    style={"color": DARK_THEME["colors"]["text_primary"]},
                    margin_bottom="4"
                ),
                consultas_por_estado_admin(),
                spacing="4",
                width="100%"
            ),
            **dark_crystal_card(color=COLORS["primary"]["500"], hover_lift="4px"),
            width="100%"
        ),

        # ========================================
        # SECCIÓN 3: DATOS FINANCIEROS (2 COLUMNAS)
        # ========================================
        rx.grid(
            # Métodos de pago (horizontal bar)
            horizontal_bar_chart(
                title="Métodos de Pago Más Usados",
                data=AppState.metodos_pago_admin,
                color=COLORS["secondary"]["500"]
            ),

            # Distribución USD vs BS (pie chart con %)
            pie_chart_card(
                title="Distribución USD vs BS",
                data=AppState.datos_grafico_distribucion_pagos_admin,
                subtitle=rx.cond(
                    AppState.distribucion_pagos_admin,
                    f"USD {AppState.distribucion_pagos_admin.get('porcentaje_usd', 0):.1f}% | BS {AppState.distribucion_pagos_admin.get('porcentaje_bs', 0):.1f}%",
                    "USD 0% | BS 0%"
                ),
                height=320
            ),

            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="6",
            width="100%",
            margin_top="6"
        ),

        # ========================================
        # SECCIÓN 4: GRÁFICO DE EVOLUCIÓN CON TABS
        # ========================================
        graficas_reportes_admin(),

        # ========================================
        # SECCIÓN 5: CONSULTAS Y PAGOS (2 COLUMNAS)
        # ========================================
        rx.grid(
            # Columna izquierda - Consultas
            rx.vstack(
                # Distribución de consultas por odontólogo
                horizontal_bar_chart(
                    title="Consultas por Odontólogo",
                    data=AppState.distribucion_consultas_odontologo,
                    color=COLORS["blue"]["500"]
                ),

                # Tipos de consulta
                horizontal_bar_chart(
                    title="Tipos de Consulta",
                    data=AppState.tipos_consulta_distribucion,
                    color=COLORS["secondary"]["500"]
                ),

                spacing="6",
                width="100%"
            ),

            # Columna derecha - Pagos pendientes
            rx.vstack(
                # Pagos pendientes
                pagos_pendientes_admin(),

                spacing="6",
                width="100%"
            ),

            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="6",
            width="100%",
            margin_top="6"
        ),

        # ========================================
        # SECCIÓN 6: TABLA DE CONSULTAS (ANCHO COMPLETO)
        # ========================================
        tabla_consultas_admin(),

        spacing="6",
        width="100%",
        margin_top="6"
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL
# ==========================================

def reportes_page() -> rx.Component:
    """📊 Página principal de reportes - diferenciada por rol"""
    return medical_page_layout(
        rx.vstack(
            # Header de la página
            page_header(
                "Reportes y Análisis",
                rx.match(
                    AppState.rol_usuario,
                    ("gerente", "Reportes financieros y operativos completos"),
                    ("odontologo", "Reportes clínicos personales y estadísticas"),
                    ("administrador", "Reportes operativos del día a día"),
                    "Reportes del sistema"
                ),
                actions=[
                    refresh_button(
                        text="Actualizar reportes",
                        on_click=AppState.cargar_reportes_completos,
                        loading=AppState.cargando_reportes
                    )
                ]
            ),

            # Contenido principal - diferenciado por rol
            rx.cond(
                AppState.cargando_reportes,
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3", color=COLORS["primary"]["500"]),
                        rx.text(
                            "Generando reportes...",
                            color=COLORS["gray"]["600"],
                            size="3"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="40px",
                    width="100%"
                ),
                rx.match(
                    AppState.rol_usuario,
                    ("gerente", layout_gerente()),
                    ("odontologo", layout_odontologo()),
                    ("administrador", layout_administrador()),
                    rx.center(
                        rx.text(
                            "No tienes permisos para ver reportes",
                            size="4",
                            style={"color": DARK_THEME["colors"]["text_muted"]}
                        ),
                        padding="40px",
                        width="100%"
                    )
                )
            ),

            spacing="6",
            width="100%",
            min_height="100vh",
            padding="24px",

            # 🚀 CARGAR DATOS AL MONTAR
            on_mount=AppState.cargar_reportes_completos()
        )
    )
