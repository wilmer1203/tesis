"""
Sistema de Logging Centralizado para Sistema Odontológico
Logger profesional con rotación de archivos y múltiples niveles
"""
import logging
import logging.handlers
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, Union
from pathlib import Path
import sys


class DentalLogger:
    """
    Logger centralizado del sistema odontológico

    Características:
    - Rotación automática de archivos (10MB, 5 backups)
    - Múltiples niveles de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Formato estructurado con timestamp, usuario, acción
    - Logging de acciones de usuario para auditoría
    - Logging de errores con contexto completo
    - Logging de performance para optimización
    - Logging de seguridad para compliance
    """

    def __init__(self, name: str = "dental_system"):
        self.logger_name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Prevenir duplicación de handlers
        if not self.logger.handlers:
            self.setup_logger()

        self.session_stats = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
            "session_start": datetime.now()
        }

    def setup_logger(self):
        """Configurar logger con múltiples handlers"""

        # Crear directorio de logs si no existe
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # 1. Handler para archivo general (INFO y superior)
        file_handler = logging.handlers.RotatingFileHandler(
            logs_dir / 'dental_system.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)

        # 2. Handler para errores críticos (ERROR y superior)
        error_handler = logging.handlers.RotatingFileHandler(
            logs_dir / 'dental_errors.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=10,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)

        # 3. Handler para auditoría de usuarios
        audit_handler = logging.handlers.RotatingFileHandler(
            logs_dir / 'dental_audit.log',
            maxBytes=20*1024*1024,  # 20MB
            backupCount=20,
            encoding='utf-8'
        )
        audit_handler.setLevel(logging.INFO)

        # 4. Handler para consola (desarrollo)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)

        # 5. Handler para performance
        performance_handler = logging.handlers.RotatingFileHandler(
            logs_dir / 'dental_performance.log',
            maxBytes=15*1024*1024,  # 15MB
            backupCount=5,
            encoding='utf-8'
        )
        performance_handler.setLevel(logging.INFO)

        # Formatters diferenciados
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        json_formatter = JsonFormatter()

        audit_formatter = logging.Formatter(
            '%(asctime)s | AUDIT | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        performance_formatter = logging.Formatter(
            '%(asctime)s | PERF | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Asignar formatters
        file_handler.setFormatter(detailed_formatter)
        error_handler.setFormatter(json_formatter)
        audit_handler.setFormatter(audit_formatter)
        console_handler.setFormatter(detailed_formatter)
        performance_handler.setFormatter(performance_formatter)

        # Agregar handlers al logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)

        # Loggers especializados
        self.audit_logger = logging.getLogger(f"{self.logger_name}.audit")
        self.audit_logger.setLevel(logging.INFO)
        self.audit_logger.addHandler(audit_handler)

        self.performance_logger = logging.getLogger(f"{self.logger_name}.performance")
        self.performance_logger.setLevel(logging.INFO)
        self.performance_logger.addHandler(performance_handler)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log nivel DEBUG"""
        self.session_stats["debug"] += 1
        self.logger.debug(self._format_message(message, extra))

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log nivel INFO"""
        self.session_stats["info"] += 1
        self.logger.info(self._format_message(message, extra))

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log nivel WARNING"""
        self.session_stats["warning"] += 1
        self.logger.warning(self._format_message(message, extra))

    def error(self, message: str,
              error: Optional[Exception] = None,
              context: Optional[Dict[str, Any]] = None):
        """Log nivel ERROR con contexto completo"""
        self.session_stats["error"] += 1

        error_data = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }

        if error:
            error_data.update({
                "error_type": type(error).__name__,
                "error_message": str(error),
                "error_args": error.args
            })

        self.logger.error(json.dumps(error_data, ensure_ascii=False, indent=2))

    def critical(self, message: str,
                error: Optional[Exception] = None,
                context: Optional[Dict[str, Any]] = None):
        """Log nivel CRITICAL para errores graves del sistema"""
        self.session_stats["critical"] += 1

        critical_data = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "severity": "CRITICAL",
            "context": context or {}
        }

        if error:
            critical_data.update({
                "error_type": type(error).__name__,
                "error_message": str(error),
                "error_args": error.args
            })

        self.logger.critical(json.dumps(critical_data, ensure_ascii=False, indent=2))

    def log_user_action(self,
                       user_id: str,
                       action: str,
                       details: Dict[str, Any],
                       ip_address: str = "unknown",
                       user_agent: str = "unknown"):
        """
        Log acciones de usuario para auditoría

        Args:
            user_id: ID del usuario
            action: Acción realizada
            details: Detalles de la acción
            ip_address: Dirección IP del usuario
            user_agent: User agent del navegador
        """
        audit_data = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "details": details,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "session_id": getattr(self, 'session_id', 'unknown')
        }

        audit_message = json.dumps(audit_data, ensure_ascii=False)
        self.audit_logger.info(audit_message)

    def log_performance(self,
                       operation: str,
                       execution_time: float,
                       details: Optional[Dict[str, Any]] = None):
        """
        Log métricas de performance

        Args:
            operation: Nombre de la operación
            execution_time: Tiempo de ejecución en segundos
            details: Detalles adicionales de performance
        """
        performance_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "execution_time_seconds": round(execution_time, 4),
            "details": details or {}
        }

        # Categorizar performance
        if execution_time < 0.1:
            category = "FAST"
        elif execution_time < 1.0:
            category = "NORMAL"
        elif execution_time < 5.0:
            category = "SLOW"
        else:
            category = "VERY_SLOW"

        performance_data["performance_category"] = category

        performance_message = json.dumps(performance_data, ensure_ascii=False)
        self.performance_logger.info(performance_message)

    def log_security_event(self,
                          event_type: str,
                          severity: str,
                          details: Dict[str, Any],
                          user_id: Optional[str] = None):
        """
        Log eventos de seguridad

        Args:
            event_type: Tipo de evento (login_failed, unauthorized_access, etc.)
            severity: Severidad (low, medium, high, critical)
            details: Detalles del evento
            user_id: ID del usuario involucrado
        """
        security_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "severity": severity.upper(),
            "user_id": user_id,
            "details": details
        }

        message = f"SECURITY_EVENT: {json.dumps(security_data, ensure_ascii=False)}"

        # Log según severidad
        if severity.lower() in ['critical', 'high']:
            self.critical(message)
        elif severity.lower() == 'medium':
            self.warning(message)
        else:
            self.info(message)

    def log_database_operation(self,
                             table: str,
                             operation: str,
                             affected_rows: int,
                             execution_time: float,
                             query_hash: Optional[str] = None):
        """
        Log operaciones de base de datos

        Args:
            table: Tabla afectada
            operation: Tipo de operación (SELECT, INSERT, UPDATE, DELETE)
            affected_rows: Número de filas afectadas
            execution_time: Tiempo de ejecución
            query_hash: Hash de la consulta (para privacy)
        """
        db_data = {
            "timestamp": datetime.now().isoformat(),
            "table": table,
            "operation": operation.upper(),
            "affected_rows": affected_rows,
            "execution_time_seconds": round(execution_time, 4),
            "query_hash": query_hash
        }

        message = f"DB_OPERATION: {json.dumps(db_data, ensure_ascii=False)}"
        self.info(message)

    def log_system_health(self, metrics: Dict[str, Any]):
        """
        Log métricas de salud del sistema

        Args:
            metrics: Métricas del sistema (CPU, memoria, conexiones, etc.)
        """
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "SYSTEM_HEALTH",
            "metrics": metrics
        }

        message = json.dumps(health_data, ensure_ascii=False)
        self.info(message)

    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la sesión actual"""
        uptime = (datetime.now() - self.session_stats["session_start"]).total_seconds()
        total_logs = sum(self.session_stats[level] for level in ["debug", "info", "warning", "error", "critical"])

        return {
            **self.session_stats,
            "total_logs": total_logs,
            "uptime_seconds": round(uptime, 2),
            "logs_per_minute": round((total_logs / (uptime / 60)) if uptime > 0 else 0, 2)
        }

    def _format_message(self, message: str, extra: Optional[Dict[str, Any]] = None) -> str:
        """Formatear mensaje con información adicional"""
        if extra:
            return f"{message} | Extra: {json.dumps(extra, ensure_ascii=False)}"
        return message

    def set_session_id(self, session_id: str):
        """Establecer ID de sesión para tracking"""
        self.session_id = session_id


class JsonFormatter(logging.Formatter):
    """Formatter para logs en formato JSON"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage()
        }

        if hasattr(record, 'exc_info') and record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


# Instancia global del logger
dental_logger = DentalLogger()


# Funciones de conveniencia para uso directo
def log_info(message: str, extra: Optional[Dict[str, Any]] = None):
    """Log información general"""
    dental_logger.info(message, extra)


def log_error(message: str, error: Optional[Exception] = None, context: Optional[Dict[str, Any]] = None):
    """Log error con contexto"""
    dental_logger.error(message, error, context)


def log_user_action(user_id: str, action: str, details: Dict[str, Any]):
    """Log acción de usuario para auditoría"""
    dental_logger.log_user_action(user_id, action, details)


def log_performance(operation: str, execution_time: float, details: Optional[Dict[str, Any]] = None):
    """Log métrica de performance"""
    dental_logger.log_performance(operation, execution_time, details)


def log_security_event(event_type: str, severity: str, details: Dict[str, Any], user_id: Optional[str] = None):
    """Log evento de seguridad"""
    dental_logger.log_security_event(event_type, severity, details, user_id)


def log_database_operation(table: str, operation: str, affected_rows: int, execution_time: float):
    """Log operación de base de datos"""
    dental_logger.log_database_operation(table, operation, affected_rows, execution_time)


def get_logger_stats() -> Dict[str, Any]:
    """Obtener estadísticas del logger"""
    return dental_logger.get_session_stats()


# Context manager para logging automático de performance
class LogPerformance:
    """Context manager para medir y loggear performance automáticamente"""

    def __init__(self, operation_name: str, details: Optional[Dict[str, Any]] = None):
        self.operation_name = operation_name
        self.details = details or {}
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            execution_time = (datetime.now() - self.start_time).total_seconds()

            if exc_type:
                self.details["error"] = str(exc_val)
                self.details["error_type"] = exc_type.__name__

            dental_logger.log_performance(self.operation_name, execution_time, self.details)


# Decorador para logging automático de funciones
def log_function_performance(operation_name: Optional[str] = None):
    """
    Decorador para loggear performance de funciones automáticamente

    Args:
        operation_name: Nombre de la operación (usa nombre de función si no se especifica)

    Usage:
        @log_function_performance("cargar_pacientes")
        def get_pacientes_list():
            # ... función costosa
            return resultado
    """
    def decorator(func):
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__

            with LogPerformance(op_name):
                return func(*args, **kwargs)

        return wrapper
    return decorator


# Inicialización del sistema de logging
def init_logging_system():
    """Inicializar sistema de logging al arranque de la aplicación"""
    dental_logger.info("Sistema de logging inicializado", {
        "version": "1.0",
        "log_directory": str(Path("logs").absolute()),
        "handlers": ["file", "error", "audit", "console", "performance"]
    })

    print("✅ Sistema de logging inicializado correctamente")


# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar
    init_logging_system()

    # Ejemplos de logging
    log_info("Sistema iniciado correctamente")
    log_user_action("USR001", "login", {"ip": "192.168.1.100", "successful": True})

    # Performance logging
    with LogPerformance("test_operation", {"test": True}):
        import time
        time.sleep(0.1)  # Simular trabajo

    # Stats
    print(get_logger_stats())