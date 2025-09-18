"""
🧪 PÁGINA PRINCIPAL DE TESTING - SISTEMA ODONTOLÓGICO
=====================================================

Página central que integra todos los componentes de testing, debugging,
optimización y monitoreo del sistema odontológico. Proporciona una
interfaz unificada para desarrolladores y administradores del sistema.

FUNCIONALIDADES:
- Testing Suite Integral: Validación completa del flujo odontológico
- Performance Monitoring: Monitoreo en tiempo real de métricas
- Data Validation: Validación de integridad de datos con corrección automática
- Error Recovery: Manejo robusto de errores y fallbacks
- Performance Benchmarking: Análisis detallado de performance
- System Health Dashboard: Monitoreo general del sistema

USUARIOS OBJETIVO:
- Desarrolladores: Para debugging y optimización
- Administradores: Para monitoreo del sistema
- QA Team: Para validación integral
- DevOps: Para health monitoring

ACCESO: Solo usuarios con rol 'gerente' o modo desarrollo
"""

import reflex as rx
from datetime import datetime

from dental_system.state.app_state import AppState
from dental_system.components.common import page_header
from dental_system.components.testing import (
    odontologia_testing_suite,
    performance_monitor_dashboard,
    data_validation_dashboard,
    complete_error_recovery_suite,
    complete_performance_benchmarker,
    EstadoTestingOdontologia,
    EstadoPerformanceOptimizer,
    EstadoDataValidator,
    EstadoErrorRecovery,
    EstadoPerformanceBenchmarker
)
from dental_system.styles.themes import COLORS, RADIUS, SPACING, SHADOWS

# ==========================================
# 🎨 ESTILOS PARA LA PÁGINA DE TESTING
# ==========================================

TESTING_PAGE_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['gray']['100']} 0%, {COLORS['purple']['100']} 50%, {COLORS['blue']['100']} 100%)",
    "min_height": "100vh",
    "padding": SPACING["6"]
}

TAB_CONTENT_STYLE = {
    "width": "100%",
    "max_width": "1600px",
    "margin": "0 auto",
    "padding": SPACING["4"]
}

TESTING_HEADER_STYLE = {
    "background": f"linear-gradient(135deg, {COLORS['purple']['600']} 0%, {COLORS['blue']['600']} 100%)",
    "color": "white",
    "padding": SPACING["6"],
    "border_radius": RADIUS["lg"],
    "margin_bottom": SPACING["6"],
    "box_shadow": SHADOWS["xl"]
}

# ==========================================
# 🎯 COMPONENTES DE LA PÁGINA
# ==========================================

def testing_page_header() -> rx.Component:
    """🎯 Header especializado para la página de testing"""
    return rx.box(
        rx.vstack(
            # Título principal con iconos
            rx.hstack(
                rx.icon("test_tube_2", size=40, color="white"),
                rx.vstack(
                    rx.heading(
                        "Testing & Optimization Suite v2.0",
                        size="8",
                        color="white",
                        weight="bold"
                    ),
                    rx.text(
                        "Sistema integral de testing, optimización y monitoreo para el módulo odontológico",
                        size="4",
                        color="white",
                        opacity="0.9"
                    ),
                    align_items="start",
                    spacing="2"
                ),
                spacing="4",
                align_items="center"
            ),
            
            # Métricas rápidas del sistema
            rx.grid(
                rx.stat(
                    rx.stat_label("System Health", color="white", opacity="0.8"),
                    rx.stat_number(
                        rx.cond(
                            EstadoErrorRecovery.system_health.value == "healthy",
                            "✅ HEALTHY",
                            "⚠️ DEGRADED"
                        ),
                        color="white"
                    )
                ),
                rx.stat(
                    rx.stat_label("Performance Score", color="white", opacity="0.8"), 
                    rx.stat_number(
                        f"{EstadoPerformanceBenchmarker.overall_performance_score:.0f}%",
                        color="white"
                    )
                ),
                rx.stat(
                    rx.stat_label("Cache Efficiency", color="white", opacity="0.8"),
                    rx.stat_number(
                        f"{EstadoPerformanceOptimizer.cache_hit_rate:.0f}%",
                        color="white"
                    )
                ),
                rx.stat(
                    rx.stat_label("Data Quality", color="white", opacity="0.8"),
                    rx.stat_number(
                        f"{EstadoDataValidator.overall_data_quality_score:.0f}%",
                        color="white"
                    )
                ),
                columns="4",
                spacing="6",
                margin_top="6"
            ),
            
            spacing="6",
            width="100%"
        ),
        style=TESTING_HEADER_STYLE
    )

def system_overview_panel() -> rx.Component:
    """📊 Panel de overview general del sistema"""
    return rx.box(
        rx.vstack(
            # Header del panel
            rx.hstack(
                rx.icon("activity", size=24, color="blue.600"),
                rx.text("System Overview", weight="bold", size="5"),
                rx.spacer(),
                rx.text(
                    datetime.now().strftime("%H:%M:%S"),
                    size="3",
                    color="gray.600"
                ),
                width="100%",
                align_items="center"
            ),
            
            # Grid de métricas principales
            rx.grid(
                # Testing Status
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("test_tube", size=20, color="purple.500"),
                            rx.text("Testing Status", weight="bold", size="4"),
                            spacing="2",
                            align_items="center"
                        ),
                        rx.text(
                            EstadoTestingOdontologia.estado_testing_general,
                            size="3",
                            color="gray.700"
                        ),
                        rx.hstack(
                            rx.text(f"{EstadoTestingOdontologia.tests_exitosos}", color="green.600", weight="bold"),
                            rx.text("exitosos", size="2"),
                            rx.text("•", size="2", opacity="0.5"),
                            rx.text(f"{EstadoTestingOdontologia.tests_fallidos}", color="red.600", weight="bold"),
                            rx.text("fallidos", size="2"),
                            spacing="1",
                            align_items="center"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    padding="4",
                    border_radius="md",
                    border="1px solid",
                    border_color="gray.200",
                    background="white"
                ),
                
                # Performance Status
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("zap", size=20, color="orange.500"),
                            rx.text("Performance", weight="bold", size="4"),
                            spacing="2",
                            align_items="center"
                        ),
                        rx.text(
                            f"{EstadoPerformanceOptimizer.total_operaciones} operaciones",
                            size="3",
                            color="gray.700"
                        ),
                        rx.hstack(
                            rx.text(f"{EstadoPerformanceOptimizer.cache_hit_rate:.1f}%", color="blue.600", weight="bold"),
                            rx.text("cache hit rate", size="2"),
                            spacing="1",
                            align_items="center"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    padding="4",
                    border_radius="md",
                    border="1px solid",
                    border_color="gray.200",
                    background="white"
                ),
                
                # Data Quality Status
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("shield_check", size=20, color="green.500"),
                            rx.text("Data Quality", weight="bold", size="4"),
                            spacing="2",
                            align_items="center"
                        ),
                        rx.text(
                            f"{EstadoDataValidator.total_records_validated} registros validados",
                            size="3",
                            color="gray.700"
                        ),
                        rx.hstack(
                            rx.text(f"{len(EstadoDataValidator.critical_issues)}", color="red.600", weight="bold"),
                            rx.text("issues críticos", size="2"),
                            spacing="1",
                            align_items="center"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    padding="4",
                    border_radius="md",
                    border="1px solid",
                    border_color="gray.200",
                    background="white"
                ),
                
                # Error Recovery Status
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("shield", size=20, color="blue.500"),
                            rx.text("Error Recovery", weight="bold", size="4"),
                            spacing="2",
                            align_items="center"
                        ),
                        rx.text(
                            f"{EstadoErrorRecovery.total_errors} errores totales",
                            size="3",
                            color="gray.700"
                        ),
                        rx.hstack(
                            rx.text(f"{EstadoErrorRecovery.recovery_success_rate:.1f}%", color="green.600", weight="bold"),
                            rx.text("recovery rate", size="2"),
                            spacing="1",
                            align_items="center"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    padding="4",
                    border_radius="md",
                    border="1px solid",
                    border_color="gray.200",
                    background="white"
                ),
                
                columns="2",
                spacing="4",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        padding="4",
        border_radius="lg",
        border="1px solid",
        border_color="gray.200",
        background="gray.50",
        width="100%"
    )

def quick_actions_panel() -> rx.Component:
    """⚡ Panel de acciones rápidas"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("lightning", size=20, color="yellow.500"),
                rx.text("Quick Actions", weight="bold", size="4"),
                width="100%",
                align_items="center"
            ),
            
            # Botones de acciones rápidas
            rx.grid(
                rx.button(
                    rx.vstack(
                        rx.icon("play", size=20),
                        rx.text("Run All Tests", size="2"),
                        spacing="1",
                        align_items="center"
                    ),
                    color_scheme="purple",
                    size="3",
                    width="100%",
                    height="80px",
                    on_click=EstadoTestingOdontologia.iniciar_testing_completo,
                    disabled=EstadoTestingOdontologia.testing_activo
                ),
                rx.button(
                    rx.vstack(
                        rx.icon("bar_chart", size=20),
                        rx.text("Benchmark", size="2"),
                        spacing="1",
                        align_items="center"
                    ),
                    color_scheme="orange",
                    size="3",
                    width="100%",
                    height="80px",
                    on_click=EstadoPerformanceBenchmarker.run_full_benchmark_suite,
                    disabled=EstadoPerformanceBenchmarker.benchmarking_active
                ),
                rx.button(
                    rx.vstack(
                        rx.icon("shield_check", size=20),
                        rx.text("Validate Data", size="2"),
                        spacing="1",
                        align_items="center"
                    ),
                    color_scheme="green",
                    size="3",
                    width="100%",
                    height="80px",
                    on_click=EstadoDataValidator.run_full_validation,
                    disabled=EstadoDataValidator.validation_running
                ),
                rx.button(
                    rx.vstack(
                        rx.icon("activity", size=20),
                        rx.text("Health Check", size="2"),
                        spacing="1",
                        align_items="center"
                    ),
                    color_scheme="blue",
                    size="3", 
                    width="100%",
                    height="80px",
                    on_click=EstadoErrorRecovery.run_health_check
                ),
                columns="4",
                spacing="3",
                width="100%"
            ),
            
            spacing="3",
            width="100%"
        ),
        padding="4",
        border_radius="md",
        border="1px solid",
        border_color="gray.200",
        background="white"
    )

# ==========================================
# 📄 PÁGINA PRINCIPAL
# ==========================================

def testing_page() -> rx.Component:
    """
    🧪 PÁGINA PRINCIPAL DE TESTING & OPTIMIZATION SUITE
    
    Página integral que proporciona acceso a todos los componentes de testing,
    optimización, validación y monitoreo del sistema odontológico.
    
    FUNCIONALIDADES:
    ✅ Testing Suite Integral - Validación completa del flujo odontológico
    ✅ Performance Monitoring - Métricas en tiempo real y optimización automática  
    ✅ Data Validation - Validación de integridad con auto-corrección
    ✅ Error Recovery - Manejo robusto con circuit breakers y fallbacks
    ✅ Performance Benchmarking - Análisis detallado con recomendaciones
    ✅ System Health Dashboard - Monitoreo general y alertas
    
    ARQUITECTURA:
    - Header con métricas rápidas del sistema
    - Panel de overview con status general
    - Tabs principales con cada herramienta especializada
    - Panel de acciones rápidas para operaciones comunes
    
    ACCESO: Restringido a usuarios con permisos de testing (gerente/admin)
    """
    
    return rx.box(
        rx.vstack(
            # Header principal con métricas
            testing_page_header(),
            
            # Panel de overview y acciones rápidas
            rx.hstack(
                system_overview_panel(),
                quick_actions_panel(),
                spacing="6",
                width="100%",
                max_width="1600px",
                margin="0 auto"
            ),
            
            # Tabs principales con herramientas
            rx.box(
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("test_tube", size=16),
                                "Testing Suite",
                                spacing="2"
                            ),
                            value="testing"
                        ),
                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("zap", size=16), 
                                "Performance Monitor",
                                spacing="2"
                            ),
                            value="performance"
                        ),
                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("shield_check", size=16),
                                "Data Validator", 
                                spacing="2"
                            ),
                            value="validation"
                        ),
                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("shield", size=16),
                                "Error Recovery",
                                spacing="2" 
                            ),
                            value="recovery"
                        ),
                        rx.tabs.trigger(
                            rx.hstack(
                                rx.icon("bar_chart", size=16),
                                "Benchmarker",
                                spacing="2"
                            ),
                            value="benchmark"
                        ),
                        justify="start",
                        wrap="wrap"
                    ),
                    
                    # Testing Suite Tab
                    rx.tabs.content(
                        rx.box(
                            odontologia_testing_suite(),
                            style=TAB_CONTENT_STYLE
                        ),
                        value="testing"
                    ),
                    
                    # Performance Monitor Tab
                    rx.tabs.content(
                        rx.box(
                            performance_monitor_dashboard(),
                            style=TAB_CONTENT_STYLE
                        ),
                        value="performance"
                    ),
                    
                    # Data Validator Tab
                    rx.tabs.content(
                        rx.box(
                            data_validation_dashboard(),
                            style=TAB_CONTENT_STYLE
                        ),
                        value="validation"
                    ),
                    
                    # Error Recovery Tab
                    rx.tabs.content(
                        rx.box(
                            complete_error_recovery_suite(),
                            style=TAB_CONTENT_STYLE
                        ),
                        value="recovery"
                    ),
                    
                    # Benchmarker Tab
                    rx.tabs.content(
                        rx.box(
                            complete_performance_benchmarker(),
                            style=TAB_CONTENT_STYLE
                        ),
                        value="benchmark"
                    ),
                    
                    default_value="testing",
                    orientation="horizontal",
                    width="100%"
                ),
                width="100%",
                max_width="1600px", 
                margin="0 auto",
                margin_top="6"
            ),
            
            # Footer con información del sistema
            rx.box(
                rx.hstack(
                    rx.text(
                        "Testing Suite v2.0 - Sistema Odontológico",
                        size="2",
                        color="gray.600"
                    ),
                    rx.spacer(),
                    rx.text(
                        f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                        size="2", 
                        color="gray.600"
                    ),
                    width="100%",
                    align_items="center"
                ),
                padding="4",
                margin_top="8",
                border_top="1px solid",
                border_color="gray.200"
            ),
            
            spacing="0",
            width="100%"
        ),
        style=TESTING_PAGE_STYLE,
        
        # Auto-refresh cada 30 segundos para métricas en tiempo real
        on_mount=[
            # Inicializar sistemas de monitoreo
            EstadoPerformanceOptimizer.toggle_optimizer,
            EstadoErrorRecovery.run_health_check
        ]
    )