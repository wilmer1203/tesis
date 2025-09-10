"""
🧪 MÓDULO DE TESTING COMPONENTS - SUITE COMPLETA V2.0
=====================================================

Suite completa de componentes especializados para testing, debugging, 
optimización y monitoreo del sistema odontológico dental.

COMPONENTES PRINCIPALES:
- odontologia_testing_suite: Testing integral con validación de flujo completo
- performance_optimizer: Optimización con lazy loading y cache inteligente
- data_validator: Validación de integridad de datos reales con auto-corrección
- error_recovery_system: Manejo robusto de errores con circuit breakers
- performance_benchmarker: Benchmarking avanzado y análisis de métricas

CARACTERÍSTICAS:
✅ Testing de integración con datos reales de Supabase
✅ Optimización automática de performance y memoria
✅ Validación exhaustiva de modelos tipados vs BD
✅ Recovery automático ante errores críticos
✅ Benchmarking detallado con recomendaciones
✅ Monitoreo en tiempo real de salud del sistema
✅ Circuit breakers para alta disponibilidad
✅ Cache inteligente con invalidación automática
"""

from .odontologia_testing_suite import (
    odontologia_testing_suite,
    EstadoTestingOdontologia
)

from .performance_optimizer import (
    EstadoPerformanceOptimizer,
    performance_monitor_dashboard,
    with_performance_tracking,
    with_caching,
    lazy_component
)

from .data_validator import (
    EstadoDataValidator,
    data_validation_dashboard,
    validation_configuration_panel
)

from .error_recovery_system import (
    EstadoErrorRecovery,
    error_recovery_dashboard,
    error_history_panel,
    complete_error_recovery_suite
)

from .performance_benchmarker import (
    EstadoPerformanceBenchmarker,
    performance_benchmark_dashboard,
    benchmark_results_table,
    complete_performance_benchmarker
)

__all__ = [
    # Testing Suite Principal
    "odontologia_testing_suite",
    "EstadoTestingOdontologia",
    
    # Performance Optimizer
    "EstadoPerformanceOptimizer", 
    "performance_monitor_dashboard",
    "with_performance_tracking",
    "with_caching", 
    "lazy_component",
    
    # Data Validator
    "EstadoDataValidator",
    "data_validation_dashboard",
    "validation_configuration_panel",
    
    # Error Recovery System
    "EstadoErrorRecovery",
    "error_recovery_dashboard", 
    "error_history_panel",
    "complete_error_recovery_suite",
    
    # Performance Benchmarker
    "EstadoPerformanceBenchmarker",
    "performance_benchmark_dashboard",
    "benchmark_results_table", 
    "complete_performance_benchmarker"
]