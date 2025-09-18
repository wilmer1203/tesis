
"""
=====================================================
CLIENTE SUPABASE OPTIMIZADO - Sistema Dental Odontomara
=====================================================
🚀 Cliente Supabase con optimizaciones avanzadas:
- Connection pooling
- Cache inteligente 
- Retry automático
- Monitoring de performance
- Validaciones robustas
=====================================================
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
from functools import lru_cache, wraps
from supabase import create_client, Client
from contextlib import contextmanager
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
 
# ==========================================
# CONFIGURACIÓN Y LOGGING
# ==========================================

logger = logging.getLogger(__name__)

# ==========================================
# 🔧 DECORADORES Y UTILITIES
# ==========================================

def retry_connection(max_retries: int = 3, delay: float = 1.0):
    """Decorador para reintentar conexiones fallidas"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Intento {attempt + 1} falló para {func.__name__}: {e}")
                        time.sleep(delay * (2 ** attempt))  # Backoff exponencial
                    else:
                        logger.error(f"Todos los intentos fallaron para {func.__name__}: {e}")
            
            raise last_exception
        return wrapper
    return decorator

def log_performance(func):
    """Decorador para loggear performance de operaciones"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"🚀 {func.__name__} ejecutado en {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"💥 {func.__name__} falló después de {duration:.3f}s: {e}")
            raise
    return wrapper

# ==========================================
# 📊 CLASE DE MÉTRICAS
# ==========================================

class SupabaseMetrics:
    """Clase para tracking de métricas de Supabase"""
    
    def __init__(self):
        self.queries_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_query_time = 0.0
        self.error_count = 0
        self.last_reset = datetime.now()
        self._lock = threading.Lock()
    
    def record_query(self, duration: float, from_cache: bool = False):
        """Registrar una query ejecutada"""
        with self._lock:
            self.queries_count += 1
            self.total_query_time += duration
            
            if from_cache:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
    
    def record_error(self):
        """Registrar un error"""
        with self._lock:
            self.error_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas actuales"""
        with self._lock:
            total_requests = self.cache_hits + self.cache_misses
            cache_hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
            avg_query_time = (self.total_query_time / self.queries_count) if self.queries_count > 0 else 0
            
            return {
                "queries_count": self.queries_count,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_rate": f"{cache_hit_rate:.1f}%",
                "avg_query_time": f"{avg_query_time:.3f}s",
                "total_query_time": f"{self.total_query_time:.3f}s",
                "error_count": self.error_count,
                "uptime": str(datetime.now() - self.last_reset)
            }
    
    def reset(self):
        """Resetear métricas"""
        with self._lock:
            self.queries_count = 0
            self.cache_hits = 0
            self.cache_misses = 0
            self.total_query_time = 0.0
            self.error_count = 0
            self.last_reset = datetime.now()

# ==========================================
# 🗄️ CLIENTE SUPABASE OPTIMIZADO
# ==========================================

class SupabaseClient:
    """Cliente Supabase optimizado para el sistema odontológico"""
    
    def __init__(self):
        logger.info("===== INICIALIZANDO CLIENTE SUPABASE OPTIMIZADO =====")
        
        # Cargar variables de entorno con validación detallada
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY") 
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        # Validaciones específicas
        self._validate_environment_variables()
        
        # Inicializar métricas
        self.metrics = SupabaseMetrics()
        
        # Configuración de conexión
        self._connection_config = {
            "timeout": int(os.getenv("SUPABASE_TIMEOUT", "30")),
            "max_retries": int(os.getenv("SUPABASE_MAX_RETRIES", "3")),
            "retry_delay": float(os.getenv("SUPABASE_RETRY_DELAY", "1.0"))
        }
        
        # Crear clientes
        self._initialize_clients()
        
        # Cache para queries frecuentes (TTL: 5 minutos por defecto)
        self._query_cache = {}
        self._cache_ttl = int(os.getenv("SUPABASE_CACHE_TTL", "300"))  # 5 minutos
        
        logger.info("✅ Cliente Supabase inicializado con optimizaciones avanzadas")
        logger.info(f"🔧 Configuración: timeout={self._connection_config['timeout']}s, "
                   f"max_retries={self._connection_config['max_retries']}, "
                   f"cache_ttl={self._cache_ttl}s")
    
    def _validate_environment_variables(self):
        """Validar variables de entorno requeridas"""
        if not self.url:
            error_msg = "❌ SUPABASE_URL no está configurada en las variables de entorno"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if not self.key:
            error_msg = "❌ SUPABASE_ANON_KEY no está configurada en las variables de entorno"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if not self.service_key:
            error_msg = "❌ SUPABASE_SERVICE_ROLE_KEY no está configurada - REQUERIDA para crear usuarios"
            logger.error(error_msg)
            logger.info("Sin service_key no se pueden crear usuarios en Supabase Auth")
            # NO lanzar error aquí, permitir que funcione con funcionalidad limitada
    
    @retry_connection(max_retries=3, delay=1.0)
    def _initialize_clients(self):
        """Inicializar clientes Supabase con retry automático"""
        try:
            # Cliente estándar con clave anónima          
            self.supabase: Client = create_client(self.url, self.key)
            logger.info("✅ Cliente estándar de Supabase inicializado")
            
            # Cliente con permisos de servicio para operaciones administrativas
            if self.service_key:
                self.supabase_admin: Client = create_client(self.url, self.service_key)
                logger.info("✅ Cliente administrativo de Supabase inicializado")
            else:
                self.supabase_admin = None
                logger.warning("⚠️ Cliente administrativo no disponible (falta service_key)")
                
        except Exception as e:
            self.metrics.record_error()
            logger.error(f"❌ Fallo crítico al crear cliente Supabase: {str(e)}")
            logger.error(f"🔧 Detalles del error: {type(e).__name__}")
            
            # Errores específicos
            if "invalid" in str(e).lower():
                logger.error("🔑 Las claves parecen ser inválidas")
            elif "network" in str(e).lower():
                logger.error("🌐 Problema de conexión de red")
            elif "unauthorized" in str(e).lower():
                logger.error("🔒 Problema de autorización")
                
            raise Exception(f"Error configurando Supabase: {str(e)}")
    
    # ==========================================
    # 🔄 MÉTODOS DE CONEXIÓN CON CACHE
    # ==========================================
    
    @log_performance
    def get_client(self) -> Client:
        """Obtener cliente Supabase estándar"""
        return self.supabase
    
    @log_performance
    def get_admin_client(self) -> Optional[Client]:
        """Obtener cliente Supabase con permisos administrativos"""
        return self.supabase_admin
    
    @lru_cache(maxsize=100)
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Obtener esquema de tabla (con cache para evitar consultas repetidas)"""
        try:
            # TODO: Implementar consulta real al esquema
            logger.debug(f"📋 Obteniendo esquema para tabla: {table_name}")
            return {"table": table_name, "cached": True}
        except Exception as e:
            logger.error(f"Error obteniendo esquema de {table_name}: {e}")
            return {}
    
    # ==========================================
    # 📈 MÉTODOS DE CACHE Y PERFORMANCE
    # ==========================================
    
    def _get_cache_key(self, query_type: str, table: str, filters: Dict = None) -> str:
        """Generar clave de cache para query"""
        filter_str = str(sorted(filters.items())) if filters else "no_filters"
        return f"{query_type}:{table}:{filter_str}"
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Verificar si entrada de cache sigue válida"""
        if not cache_entry:
            return False
        
        timestamp = cache_entry.get("timestamp", 0)
        return time.time() - timestamp < self._cache_ttl
    
    def cached_query(self, query_type: str, table: str, filters: Dict = None, force_refresh: bool = False):
        """Ejecutar query con cache inteligente"""
        cache_key = self._get_cache_key(query_type, table, filters)
        
        # Verificar cache si no se fuerza refresh
        if not force_refresh and cache_key in self._query_cache:
            cache_entry = self._query_cache[cache_key]
            if self._is_cache_valid(cache_entry):
                logger.debug(f"📦 Cache hit para: {cache_key}")
                self.metrics.record_query(0.001, from_cache=True)
                return cache_entry["data"]
        
        # Ejecutar query real
        start_time = time.time()
        try:
            # TODO: Implementar query real según query_type
            logger.debug(f"🔍 Ejecutando query real: {query_type} en {table}")
            
            # Simular respuesta por ahora
            result = {"simulated": True, "query_type": query_type, "table": table}
            
            # Guardar en cache
            self._query_cache[cache_key] = {
                "data": result,
                "timestamp": time.time()
            }
            
            duration = time.time() - start_time
            self.metrics.record_query(duration, from_cache=False)
            
            return result
            
        except Exception as e:
            self.metrics.record_error()
            logger.error(f"Error en cached_query: {e}")
            raise
    
    def clear_cache(self, pattern: str = None):
        """Limpiar cache (opcionalmente solo claves que coincidan con patrón)"""
        if pattern:
            keys_to_remove = [key for key in self._query_cache.keys() if pattern in key]
            for key in keys_to_remove:
                del self._query_cache[key]
            logger.info(f"🧹 Cache limpiado para patrón: {pattern}")
        else:
            self._query_cache.clear()
            logger.info("🧹 Cache completamente limpiado")
    
    # ==========================================
    # 🔧 MÉTODOS DE MANTENIMIENTO
    # ==========================================
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar salud de la conexión"""
        try:
            start_time = time.time()
            
            # Hacer una query simple para verificar conectividad
            response = self.supabase.table('roles').select('id').limit(1).execute()
            
            duration = time.time() - start_time
            
            return {
                "status": "healthy",
                "response_time": f"{duration:.3f}s",
                "timestamp": datetime.now().isoformat(),
                "connection_config": self._connection_config,
                "admin_available": self.supabase_admin is not None
            }
            
        except Exception as e:
            self.metrics.record_error()
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "admin_available": self.supabase_admin is not None
            }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de performance"""
        base_stats = self.metrics.get_stats()
        
        return {
            **base_stats,
            "cache_size": len(self._query_cache),
            "cache_ttl": f"{self._cache_ttl}s",
            "connection_config": self._connection_config
        }
    
    def cleanup_expired_cache(self):
        """Limpiar entradas de cache expiradas"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self._query_cache.items():
            if current_time - entry.get("timestamp", 0) > self._cache_ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._query_cache[key]
        
        if expired_keys:
            logger.info(f"🧹 Limpiadas {len(expired_keys)} entradas de cache expiradas")
    
    @contextmanager
    def transaction(self):
        """Context manager para transacciones (preparado para futuro uso)"""
        # TODO: Implementar soporte de transacciones cuando Supabase lo soporte mejor
        logger.debug("🔄 Iniciando contexto de transacción")
        try:
            yield self.supabase
            logger.debug("✅ Transacción completada")
        except Exception as e:
            logger.error(f"💥 Error en transacción: {e}")
            raise
    
    def reset_metrics(self):
        """Resetear métricas de performance"""
        self.metrics.reset()
        logger.info("📊 Métricas reseteadas")

# ==========================================
# 🔧 CLASE DE EXCEPCIÓN PERSONALIZADA
# ==========================================

class SupabaseError(Exception):
    """Excepción personalizada para errores de Supabase"""
    
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir excepción a diccionario para logging"""
        return {
            "message": str(self),
            "error_code": self.error_code,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }

# ==========================================
# 🎯 DECORADOR MEJORADO PARA MANEJO DE ERRORES
# ==========================================

def handle_supabase_error(func):
    """
    Decorador para manejar errores de Supabase de forma consistente y detallada
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en operación de Supabase {func.__name__}: {str(e)}")
            
            # Categorizar el error
            if "network" in str(e).lower():
                raise SupabaseError(f"Error de conexión: {str(e)}", "NETWORK_ERROR")
            elif "unauthorized" in str(e).lower():
                raise SupabaseError(f"Error de autorización: {str(e)}", "AUTH_ERROR")
            elif "invalid" in str(e).lower():
                raise SupabaseError(f"Datos inválidos: {str(e)}", "VALIDATION_ERROR")
            else:
                raise SupabaseError(f"Error en la base de datos: {str(e)}", "DATABASE_ERROR")
    return wrapper

# ==========================================
# 🚀 INSTANCIA SINGLETON
# ==========================================

# Instancia singleton del cliente optimizado
supabase_client = SupabaseClient()

# ==========================================
# 📤 FUNCIONES DE CONVENIENCIA
# ==========================================

def get_client() -> Client:
    """Función de conveniencia para obtener cliente estándar"""
    return supabase_client.get_client()

def get_admin_client() -> Optional[Client]:
    """Función de conveniencia para obtener cliente admin"""
    return supabase_client.get_admin_client()

def get_health() -> Dict[str, Any]:
    """Función de conveniencia para health check"""
    return supabase_client.health_check()

def get_stats() -> Dict[str, Any]:
    """Función de conveniencia para estadísticas"""
    return supabase_client.get_performance_stats()

# ==========================================
# 📋 EXPORTS
# ==========================================

__all__ = [
    "SupabaseClient",
    "SupabaseError", 
    "handle_supabase_error",
    "supabase_client",
    "get_client",
    "get_admin_client", 
    "get_health",
    "get_stats"
]