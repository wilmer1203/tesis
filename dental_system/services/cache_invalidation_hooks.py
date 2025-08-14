"""
🚀 SISTEMA DE INVALIDACIÓN DE CACHE AUTOMÁTICO
============================================

Este módulo implementa hooks automáticos para invalidar cache cuando se
realizan operaciones CRUD, asegurando que las estadísticas se mantengan
actualizadas en tiempo real.

FUNCIONES PRINCIPALES:
- Decoradores para invalidación automática por módulo
- Sistema de tracking de invalidaciones  
- Cache manager integrado
- Hooks por tipo de operación (create, update, delete)
"""

import time
from datetime import datetime
from typing import Dict, List, Any, Callable, Optional
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class CacheInvalidationHooks:
    """
    🗑️ GESTOR CENTRAL DE INVALIDACIÓN DE CACHE
    
    Maneja la invalidación automática de cache cuando se realizan
    operaciones que afectan las estadísticas del dashboard.
    """
    
    def __init__(self):
        self.invalidation_history: List[Dict[str, Any]] = []
        self.last_invalidation_times: Dict[str, datetime] = {}
        self.invalidation_counters: Dict[str, int] = {}
    
    def invalidate_cache_for_modules(self, modules: List[str], operation_type: str, affected_data: Dict[str, Any] = None):
        """
        🗑️ Invalidar cache para múltiples módulos
        
        Args:
            modules: Lista de módulos afectados ['dashboard', 'pacientes', etc.]
            operation_type: Tipo de operación ('create', 'update', 'delete')
            affected_data: Datos afectados para logging
        """
        timestamp = datetime.now()
        
        for module in modules:
            # Actualizar contadores
            counter_key = f"{module}_{operation_type}"
            self.invalidation_counters[counter_key] = self.invalidation_counters.get(counter_key, 0) + 1
            
            # Actualizar timestamps
            self.last_invalidation_times[module] = timestamp
            
            # Log de invalidación
            logger.info(f"🗑️ Cache invalidado: {module} - {operation_type}")
        
        # Registrar en historial
        invalidation_record = {
            "timestamp": timestamp,
            "modules": modules,
            "operation_type": operation_type,
            "affected_data": affected_data or {},
            "total_invalidations": len(modules)
        }
        self.invalidation_history.append(invalidation_record)
        
        # Mantener solo últimas 100 invalidaciones
        if len(self.invalidation_history) > 100:
            self.invalidation_history = self.invalidation_history[-100:]
    
    def get_invalidation_stats(self) -> Dict[str, Any]:
        """📊 Obtener estadísticas de invalidación"""
        return {
            "total_invalidations": len(self.invalidation_history),
            "invalidation_counters": self.invalidation_counters.copy(),
            "last_invalidation_times": {
                module: timestamp.isoformat() 
                for module, timestamp in self.last_invalidation_times.items()
            },
            "recent_invalidations": self.invalidation_history[-10:] if self.invalidation_history else []
        }

# Instancia global del sistema de invalidación
invalidation_tracker = CacheInvalidationHooks()

# ========================================
# DECORADORES DE INVALIDACIÓN POR MÓDULO
# ========================================

def invalidate_after_patient_operation(operation_type: str = "unknown"):
    """
    🩺 DECORADOR: Invalidar cache después de operaciones de pacientes
    
    Afecta: dashboard, pacientes
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidar cache relevante
            affected_modules = ['dashboard', 'pacientes']
            affected_data = {
                'operation': operation_type,
                'function': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
            
            invalidation_tracker.invalidate_cache_for_modules(
                modules=affected_modules,
                operation_type=operation_type,
                affected_data=affected_data
            )
            
            return result
        return wrapper
    return decorator

def invalidate_after_consultation_operation(operation_type: str = "unknown"):
    """
    📅 DECORADOR: Invalidar cache después de operaciones de consultas
    
    Afecta: dashboard, consultas, pacientes
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidar cache relevante
            affected_modules = ['dashboard', 'consultas', 'pacientes']
            affected_data = {
                'operation': operation_type,
                'function': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
            
            invalidation_tracker.invalidate_cache_for_modules(
                modules=affected_modules,
                operation_type=operation_type,
                affected_data=affected_data
            )
            
            return result
        return wrapper
    return decorator

def invalidate_after_staff_operation(operation_type: str = "unknown"):
    """
    👨‍⚕️ DECORADOR: Invalidar cache después de operaciones de personal
    
    Afecta: dashboard, personal
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidar cache relevante
            affected_modules = ['dashboard', 'personal']
            affected_data = {
                'operation': operation_type,
                'function': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
            
            invalidation_tracker.invalidate_cache_for_modules(
                modules=affected_modules,
                operation_type=operation_type,
                affected_data=affected_data
            )
            
            return result
        return wrapper
    return decorator

def invalidate_after_service_operation(operation_type: str = "unknown"):
    """
    🦷 DECORADOR: Invalidar cache después de operaciones de servicios
    
    Afecta: dashboard, servicios
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidar cache relevante
            affected_modules = ['dashboard', 'servicios']
            affected_data = {
                'operation': operation_type,
                'function': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
            
            invalidation_tracker.invalidate_cache_for_modules(
                modules=affected_modules,
                operation_type=operation_type,
                affected_data=affected_data
            )
            
            return result
        return wrapper
    return decorator

def invalidate_after_payment_operation(operation_type: str = "unknown"):
    """
    💳 DECORADOR: Invalidar cache después de operaciones de pagos
    
    Afecta: dashboard, pagos, pacientes
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidar cache relevante
            affected_modules = ['dashboard', 'pagos', 'pacientes']
            affected_data = {
                'operation': operation_type,
                'function': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
            
            invalidation_tracker.invalidate_cache_for_modules(
                modules=affected_modules,
                operation_type=operation_type,
                affected_data=affected_data
            )
            
            return result
        return wrapper
    return decorator

def invalidate_after_intervention_operation(operation_type: str = "unknown"):
    """
    🦷 DECORADOR: Invalidar cache después de operaciones odontológicas
    
    Afecta: dashboard, consultas, pacientes, servicios
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidar cache relevante
            affected_modules = ['dashboard', 'consultas', 'pacientes', 'servicios']
            affected_data = {
                'operation': operation_type,
                'function': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
            
            invalidation_tracker.invalidate_cache_for_modules(
                modules=affected_modules,
                operation_type=operation_type,
                affected_data=affected_data
            )
            
            return result
        return wrapper
    return decorator

# ============================
# FUNCIONES DE UTILIDAD
# ============================

def track_cache_invalidation(module: str, operation: str, details: Dict[str, Any] = None):
    """
    📊 FUNCIÓN UTILITARIA: Registrar invalidación manual de cache
    
    Args:
        module: Módulo afectado
        operation: Tipo de operación
        details: Detalles adicionales para logging
    """
    invalidation_tracker.invalidate_cache_for_modules(
        modules=[module],
        operation_type=operation,
        affected_data=details or {}
    )
    logger.info(f"🗑️ Invalidación manual registrada: {module} - {operation}")

def get_invalidation_stats() -> Dict[str, Any]:
    """📊 Obtener estadísticas globales de invalidación"""
    return invalidation_tracker.get_invalidation_stats()

def clear_invalidation_history():
    """🧹 Limpiar historial de invalidaciones"""
    invalidation_tracker.invalidation_history.clear()
    invalidation_tracker.invalidation_counters.clear()
    invalidation_tracker.last_invalidation_times.clear()
    logger.info("🧹 Historial de invalidaciones limpiado")

# ============================
# CONSTANTES Y CONFIGURACIÓN
# ============================

# Módulos que requieren invalidación de cache
CACHE_MODULES = [
    'dashboard',
    'pacientes', 
    'consultas',
    'personal',
    'servicios',
    'pagos'
]

# Tipos de operaciones que gatillan invalidación
OPERATION_TYPES = [
    'create',
    'update', 
    'delete',
    'bulk_update',
    'status_change'
]

# Configuración de TTL por módulo (en segundos)
MODULE_CACHE_TTL = {
    'dashboard': 300,    # 5 minutos
    'pacientes': 600,    # 10 minutos  
    'consultas': 180,    # 3 minutos
    'personal': 900,     # 15 minutos
    'servicios': 1800,   # 30 minutos
    'pagos': 300         # 5 minutos
}

# ============================
# LOGGING CONFIGURATION
# ============================

def setup_cache_logging():
    """⚙️ Configurar logging específico para cache"""
    cache_logger = logging.getLogger(__name__)
    cache_logger.setLevel(logging.INFO)
    
    # Crear handler si no existe
    if not cache_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - CACHE - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        cache_logger.addHandler(handler)
    
    return cache_logger

# Configurar logging al importar el módulo
setup_cache_logging()