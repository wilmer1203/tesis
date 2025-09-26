"""
Sistema de Métricas de Performance para Sistema Odontológico
Monitoreo en tiempo real de rendimiento y métricas del sistema
"""
import time
import psutil
import functools
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import threading
import json

# Import del logger
from dental_system.utils.logger import dental_logger


@dataclass
class PerformanceMetric:
    """Estructura para una métrica de performance individual"""
    operation: str
    start_time: float
    end_time: float
    execution_time: float
    success: bool
    error_message: Optional[str] = None
    memory_usage_mb: Optional[float] = None
    cpu_percent: Optional[float] = None
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para serialización"""
        return asdict(self)


class PerformanceMonitor:
    """
    Monitor de performance en tiempo real para el sistema odontológico

    Características:
    - Medición automática de tiempo de ejecución
    - Monitoreo de memoria y CPU
    - Alertas automáticas para operaciones lentas
    - Historial de métricas con ventana deslizante
    - Estadísticas agregadas en tiempo real
    - Detección de bottlenecks automática
    """

    def __init__(self, history_size: int = 1000):
        self.history_size = history_size
        self.metrics_history: deque = deque(maxlen=history_size)
        self.operation_stats = defaultdict(list)
        self.active_operations = {}  # Para trackear operaciones en curso
        self.system_stats = {
            "start_time": datetime.now(),
            "total_operations": 0,
            "total_errors": 0,
            "slow_operations_count": 0,
            "average_response_time": 0.0
        }

        # Umbrales de performance (configurables)
        self.thresholds = {
            "slow_operation_seconds": 2.0,
            "very_slow_operation_seconds": 5.0,
            "high_memory_usage_mb": 500.0,
            "high_cpu_percent": 80.0
        }

        # Lock para thread safety
        self._lock = threading.Lock()

    def start_operation(self, operation_name: str, details: Optional[Dict[str, Any]] = None) -> str:
        """
        Iniciar medición de una operación

        Args:
            operation_name: Nombre de la operación
            details: Detalles adicionales

        Returns:
            ID único de la operación para tracking
        """
        operation_id = f"{operation_name}_{int(time.time()*1000000)}"

        with self._lock:
            self.active_operations[operation_id] = {
                "name": operation_name,
                "start_time": time.time(),
                "start_memory": self._get_memory_usage(),
                "start_cpu": self._get_cpu_percent(),
                "details": details or {}
            }

        return operation_id

    def end_operation(self,
                     operation_id: str,
                     success: bool = True,
                     error_message: Optional[str] = None,
                     additional_details: Optional[Dict[str, Any]] = None) -> PerformanceMetric:
        """
        Finalizar medición de una operación

        Args:
            operation_id: ID de la operación
            success: Si la operación fue exitosa
            error_message: Mensaje de error si falló
            additional_details: Detalles adicionales

        Returns:
            Métrica de performance generada
        """
        end_time = time.time()

        with self._lock:
            if operation_id not in self.active_operations:
                raise ValueError(f"Operación {operation_id} no encontrada")

            operation_data = self.active_operations.pop(operation_id)

            # Crear métrica
            metric = PerformanceMetric(
                operation=operation_data["name"],
                start_time=operation_data["start_time"],
                end_time=end_time,
                execution_time=end_time - operation_data["start_time"],
                success=success,
                error_message=error_message,
                memory_usage_mb=self._get_memory_usage(),
                cpu_percent=self._get_cpu_percent(),
                details={
                    **operation_data["details"],
                    **(additional_details or {})
                }
            )

            # Agregar a historial
            self.metrics_history.append(metric)
            self.operation_stats[metric.operation].append(metric)

            # Actualizar estadísticas del sistema
            self._update_system_stats(metric)

            # Verificar si es operación lenta y generar alerta
            self._check_slow_operation(metric)

            # Log la métrica
            dental_logger.log_performance(
                metric.operation,
                metric.execution_time,
                metric.details
            )

            return metric

    def measure_operation(self, operation_name: str, details: Optional[Dict[str, Any]] = None):
        """
        Context manager para medir operaciones automáticamente

        Args:
            operation_name: Nombre de la operación
            details: Detalles adicionales

        Usage:
            with monitor.measure_operation("cargar_pacientes"):
                # ... código a medir
        """
        return OperationMeasurer(self, operation_name, details)

    def get_operation_stats(self, operation_name: str) -> Dict[str, Any]:
        """
        Obtener estadísticas de una operación específica

        Args:
            operation_name: Nombre de la operación

        Returns:
            Estadísticas agregadas de la operación
        """
        if operation_name not in self.operation_stats:
            return {"error": "Operación no encontrada"}

        metrics = self.operation_stats[operation_name]
        execution_times = [m.execution_time for m in metrics]
        success_count = sum(1 for m in metrics if m.success)
        error_count = len(metrics) - success_count

        return {
            "operation_name": operation_name,
            "total_executions": len(metrics),
            "success_count": success_count,
            "error_count": error_count,
            "success_rate_percent": (success_count / len(metrics)) * 100 if metrics else 0,
            "avg_execution_time": sum(execution_times) / len(execution_times) if execution_times else 0,
            "min_execution_time": min(execution_times) if execution_times else 0,
            "max_execution_time": max(execution_times) if execution_times else 0,
            "last_execution": metrics[-1].end_time if metrics else None,
            "slow_executions": len([m for m in metrics if m.execution_time > self.thresholds["slow_operation_seconds"]]),
            "very_slow_executions": len([m for m in metrics if m.execution_time > self.thresholds["very_slow_operation_seconds"]])
        }

    def get_system_overview(self) -> Dict[str, Any]:
        """
        Obtener resumen general del sistema

        Returns:
            Métricas generales del sistema
        """
        with self._lock:
            uptime = (datetime.now() - self.system_stats["start_time"]).total_seconds()

            # Métricas de las últimas 24 horas
            recent_metrics = [
                m for m in self.metrics_history
                if m.end_time > time.time() - 86400  # 24 horas
            ]

            # Top operaciones más lentas
            all_metrics = list(self.metrics_history)
            slowest_operations = sorted(all_metrics, key=lambda x: x.execution_time, reverse=True)[:10]

            # Operaciones más frecuentes
            operation_frequency = defaultdict(int)
            for metric in recent_metrics:
                operation_frequency[metric.operation] += 1

            most_frequent = sorted(operation_frequency.items(), key=lambda x: x[1], reverse=True)[:10]

            return {
                "system_uptime_seconds": uptime,
                "total_operations": self.system_stats["total_operations"],
                "total_errors": self.system_stats["total_errors"],
                "error_rate_percent": (self.system_stats["total_errors"] / self.system_stats["total_operations"]) * 100 if self.system_stats["total_operations"] > 0 else 0,
                "average_response_time": self.system_stats["average_response_time"],
                "slow_operations_count": self.system_stats["slow_operations_count"],
                "active_operations": len(self.active_operations),
                "metrics_in_memory": len(self.metrics_history),
                "current_memory_usage_mb": self._get_memory_usage(),
                "current_cpu_percent": self._get_cpu_percent(),
                "recent_metrics_24h": len(recent_metrics),
                "slowest_operations": [
                    {
                        "operation": m.operation,
                        "execution_time": m.execution_time,
                        "timestamp": m.end_time
                    } for m in slowest_operations
                ],
                "most_frequent_operations": [
                    {
                        "operation": op,
                        "count": count
                    } for op, count in most_frequent
                ]
            }

    def get_bottleneck_analysis(self) -> Dict[str, Any]:
        """
        Análisis automático de bottlenecks del sistema

        Returns:
            Análisis de bottlenecks y recomendaciones
        """
        analysis = {
            "detected_bottlenecks": [],
            "recommendations": [],
            "performance_score": 100
        }

        # Analizar operaciones lentas
        for operation_name, metrics in self.operation_stats.items():
            if len(metrics) >= 5:  # Solo analizar operaciones con suficientes datos
                stats = self.get_operation_stats(operation_name)

                # Bottleneck: Operación consistentemente lenta
                if stats["avg_execution_time"] > self.thresholds["slow_operation_seconds"]:
                    analysis["detected_bottlenecks"].append({
                        "type": "slow_operation",
                        "operation": operation_name,
                        "avg_time": stats["avg_execution_time"],
                        "severity": "high" if stats["avg_time"] > self.thresholds["very_slow_operation_seconds"] else "medium"
                    })

                    analysis["recommendations"].append(f"Optimizar operación '{operation_name}' - promedio {stats['avg_execution_time']:.2f}s")
                    analysis["performance_score"] -= 10

                # Bottleneck: Alta tasa de errores
                if stats["error_count"] > 0 and stats["success_rate_percent"] < 90:
                    analysis["detected_bottlenecks"].append({
                        "type": "high_error_rate",
                        "operation": operation_name,
                        "error_rate": 100 - stats["success_rate_percent"],
                        "severity": "high"
                    })

                    analysis["recommendations"].append(f"Investigar errores en '{operation_name}' - {100 - stats['success_rate_percent']:.1f}% de fallos")
                    analysis["performance_score"] -= 15

        # Analizar uso de memoria
        current_memory = self._get_memory_usage()
        if current_memory > self.thresholds["high_memory_usage_mb"]:
            analysis["detected_bottlenecks"].append({
                "type": "high_memory_usage",
                "current_usage_mb": current_memory,
                "threshold_mb": self.thresholds["high_memory_usage_mb"],
                "severity": "medium"
            })

            analysis["recommendations"].append(f"Uso alto de memoria: {current_memory:.1f}MB")
            analysis["performance_score"] -= 5

        # Analizar CPU
        current_cpu = self._get_cpu_percent()
        if current_cpu > self.thresholds["high_cpu_percent"]:
            analysis["detected_bottlenecks"].append({
                "type": "high_cpu_usage",
                "current_cpu_percent": current_cpu,
                "threshold_percent": self.thresholds["high_cpu_percent"],
                "severity": "medium"
            })

            analysis["recommendations"].append(f"Uso alto de CPU: {current_cpu:.1f}%")
            analysis["performance_score"] -= 8

        # Score final
        analysis["performance_score"] = max(0, analysis["performance_score"])

        # Clasificación general
        if analysis["performance_score"] >= 90:
            analysis["overall_status"] = "excellent"
        elif analysis["performance_score"] >= 70:
            analysis["overall_status"] = "good"
        elif analysis["performance_score"] >= 50:
            analysis["overall_status"] = "fair"
        else:
            analysis["overall_status"] = "poor"

        return analysis

    def export_metrics(self, operation_name: Optional[str] = None, last_hours: int = 24) -> List[Dict[str, Any]]:
        """
        Exportar métricas para análisis externo

        Args:
            operation_name: Filtrar por operación específica
            last_hours: Últimas N horas de datos

        Returns:
            Lista de métricas en formato JSON
        """
        cutoff_time = time.time() - (last_hours * 3600)

        filtered_metrics = [
            m for m in self.metrics_history
            if m.end_time > cutoff_time and (operation_name is None or m.operation == operation_name)
        ]

        return [metric.to_dict() for metric in filtered_metrics]

    def reset_stats(self):
        """Resetear todas las estadísticas"""
        with self._lock:
            self.metrics_history.clear()
            self.operation_stats.clear()
            self.active_operations.clear()
            self.system_stats = {
                "start_time": datetime.now(),
                "total_operations": 0,
                "total_errors": 0,
                "slow_operations_count": 0,
                "average_response_time": 0.0
            }

    def _update_system_stats(self, metric: PerformanceMetric):
        """Actualizar estadísticas del sistema con nueva métrica"""
        self.system_stats["total_operations"] += 1

        if not metric.success:
            self.system_stats["total_errors"] += 1

        if metric.execution_time > self.thresholds["slow_operation_seconds"]:
            self.system_stats["slow_operations_count"] += 1

        # Calcular promedio móvil de tiempo de respuesta
        total_ops = self.system_stats["total_operations"]
        current_avg = self.system_stats["average_response_time"]
        self.system_stats["average_response_time"] = ((current_avg * (total_ops - 1)) + metric.execution_time) / total_ops

    def _check_slow_operation(self, metric: PerformanceMetric):
        """Verificar si la operación es lenta y generar alerta"""
        if metric.execution_time > self.thresholds["very_slow_operation_seconds"]:
            dental_logger.warning(
                f"Operación muy lenta detectada: {metric.operation}",
                {
                    "execution_time": metric.execution_time,
                    "threshold": self.thresholds["very_slow_operation_seconds"],
                    "details": metric.details
                }
            )
        elif metric.execution_time > self.thresholds["slow_operation_seconds"]:
            dental_logger.info(
                f"Operación lenta detectada: {metric.operation}",
                {
                    "execution_time": metric.execution_time,
                    "threshold": self.thresholds["slow_operation_seconds"]
                }
            )

    def _get_memory_usage(self) -> float:
        """Obtener uso actual de memoria en MB"""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convertir a MB
        except:
            return 0.0

    def _get_cpu_percent(self) -> float:
        """Obtener porcentaje actual de CPU"""
        try:
            return psutil.cpu_percent(interval=None)
        except:
            return 0.0


class OperationMeasurer:
    """Context manager para medir operaciones"""

    def __init__(self, monitor: PerformanceMonitor, operation_name: str, details: Optional[Dict[str, Any]] = None):
        self.monitor = monitor
        self.operation_name = operation_name
        self.details = details
        self.operation_id = None

    def __enter__(self):
        self.operation_id = self.monitor.start_operation(self.operation_name, self.details)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        success = exc_type is None
        error_message = str(exc_val) if exc_val else None

        self.monitor.end_operation(
            self.operation_id,
            success=success,
            error_message=error_message
        )


# Instancia global del monitor
performance_monitor = PerformanceMonitor()


def measure_performance(operation_name: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
    """
    Decorador para medir performance de funciones automáticamente

    Args:
        operation_name: Nombre de la operación (usa nombre de función si no se especifica)
        details: Detalles adicionales

    Usage:
        @measure_performance("cargar_pacientes_bd")
        def get_pacientes():
            # ... función a medir
            return resultado
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__

            with performance_monitor.measure_operation(op_name, details):
                return func(*args, **kwargs)

        return wrapper
    return decorator


# Funciones de conveniencia
def get_performance_overview() -> Dict[str, Any]:
    """Obtener resumen general de performance"""
    return performance_monitor.get_system_overview()


def get_operation_performance(operation_name: str) -> Dict[str, Any]:
    """Obtener performance de una operación específica"""
    return performance_monitor.get_operation_stats(operation_name)


def analyze_bottlenecks() -> Dict[str, Any]:
    """Analizar bottlenecks del sistema"""
    return performance_monitor.get_bottleneck_analysis()


def export_performance_data(operation_name: Optional[str] = None, last_hours: int = 24) -> List[Dict[str, Any]]:
    """Exportar datos de performance"""
    return performance_monitor.export_metrics(operation_name, last_hours)


def reset_performance_stats():
    """Resetear estadísticas de performance"""
    performance_monitor.reset_stats()


# Inicialización del sistema de métricas
def init_metrics_system():
    """Inicializar sistema de métricas al arranque"""
    dental_logger.info("Sistema de métricas de performance inicializado", {
        "monitor_type": "PerformanceMonitor",
        "history_size": performance_monitor.history_size,
        "thresholds": performance_monitor.thresholds
    })

    print("✅ Sistema de métricas de performance inicializado correctamente")


# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar
    init_metrics_system()

    # Ejemplo con decorador
    @measure_performance("test_function")
    def test_function():
        time.sleep(0.1)
        return "resultado"

    # Ejemplo con context manager
    with performance_monitor.measure_operation("test_operation"):
        time.sleep(0.05)

    # Ejecutar función decorada
    result = test_function()

    # Ver estadísticas
    print(json.dumps(get_performance_overview(), indent=2))
    print(json.dumps(analyze_bottlenecks(), indent=2))