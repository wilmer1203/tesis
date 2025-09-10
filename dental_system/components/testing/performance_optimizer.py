"""
⚡ OPTIMIZADOR DE PERFORMANCE PARA MÓDULO ODONTOLÓGICO
=====================================================

Componente especializado en optimizar performance del módulo odontológico
mediante lazy loading, cache inteligente y preloading estratégico.

CARACTERÍSTICAS:
- Lazy loading de componentes pesados
- Cache automático con invalidación inteligente
- Preloading de datos críticos
- Monitoreo de performance en tiempo real
- Optimización de computed vars
- Memory management avanzado

INTEGRACIÓN: EstadoOdontologia + AppState
"""

import reflex as rx
from typing import Dict, Any, List, Optional, Callable, TypeVar, Generic
from datetime import datetime, timedelta
import asyncio
import time
import weakref
from dataclasses import dataclass, field

from dental_system.state.app_state import AppState
from dental_system.models import (
    PacienteModel, ConsultaModel, ServicioModel, 
    OdontogramaModel, DienteModel
)

# ==========================================
# 🎯 DATACLASSES PARA PERFORMANCE TRACKING
# ==========================================

@dataclass
class PerformanceMetric:
    """Métrica individual de performance"""
    operation_name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    memory_before: Optional[float] = None
    memory_after: Optional[float] = None
    cache_hit: bool = False
    error: Optional[str] = None

@dataclass
class CacheEntry:
    """Entrada del cache con metadatos"""
    key: str
    value: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    ttl_seconds: int = 300  # 5 minutos por defecto
    
    @property
    def is_expired(self) -> bool:
        """Verificar si la entrada ha expirado"""
        return datetime.now() > self.created_at + timedelta(seconds=self.ttl_seconds)
    
    @property
    def age_seconds(self) -> float:
        """Edad de la entrada en segundos"""
        return (datetime.now() - self.created_at).total_seconds()

@dataclass
class LazyComponentConfig:
    """Configuración para lazy loading de componentes"""
    component_name: str
    load_condition: Callable[[], bool]
    preload_trigger: Optional[Callable[[], bool]] = None
    cache_duration: int = 600  # 10 minutos
    priority: int = 1  # 1 = alta, 2 = media, 3 = baja

# ==========================================
# 🚀 ESTADO DE PERFORMANCE OPTIMIZER
# ==========================================

T = TypeVar('T')

class EstadoPerformanceOptimizer(rx.State):
    """
    ⚡ Estado especializado en optimización de performance
    """
    
    # ==========================================
    # 📊 MÉTRICAS DE PERFORMANCE
    # ==========================================
    
    # Métricas de operaciones
    metricas_operaciones: List[PerformanceMetric] = []
    operacion_actual: Optional[str] = None
    tiempo_inicio_operacion: Optional[float] = None
    
    # Performance counters
    total_operaciones: int = 0
    operaciones_exitosas: int = 0
    tiempo_promedio_operacion: float = 0.0
    operaciones_con_cache: int = 0
    
    # ==========================================
    # 🗄️ CACHE INTELIGENTE
    # ==========================================
    
    # Cache principal
    cache_entries: Dict[str, CacheEntry] = {}
    cache_hits: int = 0
    cache_misses: int = 0
    cache_size_mb: float = 0.0
    max_cache_size_mb: float = 50.0  # Límite de 50MB
    
    # Configuración de cache por tipo
    cache_ttl_config: Dict[str, int] = field(default_factory=lambda: {
        "pacientes": 300,      # 5 minutos
        "servicios": 600,      # 10 minutos  
        "odontograma": 900,    # 15 minutos
        "consultas": 180,      # 3 minutos
        "estadisticas": 60     # 1 minuto
    })
    
    # ==========================================
    # 🔄 LAZY LOADING CONFIGURATION
    # ==========================================
    
    # Componentes lazy-loaded
    lazy_components_config: Dict[str, LazyComponentConfig] = {}
    components_loaded: Dict[str, bool] = {}
    components_loading: Dict[str, bool] = {}
    components_preloading: Dict[str, bool] = {}
    
    # ==========================================
    # 📱 PRELOADING ESTRATÉGICO  
    # ==========================================
    
    # Estado del preloader
    preloading_activo: bool = False
    preload_queue: List[str] = []
    preload_completed: List[str] = []
    preload_progreso: float = 0.0
    
    # Datos preloadeados
    pacientes_preloaded: List[PacienteModel] = []
    servicios_preloaded: List[ServicioModel] = []
    odontogramas_preloaded: Dict[str, OdontogramaModel] = {}
    
    # ==========================================
    # ⚙️ CONFIGURACIÓN DEL OPTIMIZER
    # ==========================================
    
    # Configuración general
    optimizer_enabled: bool = True
    auto_cleanup_cache: bool = True
    preload_on_login: bool = True
    memory_monitoring: bool = True
    
    # Thresholds de performance
    slow_operation_threshold_ms: float = 1000.0
    cache_cleanup_interval_minutes: int = 15
    max_metrics_history: int = 1000
    
    # ==========================================
    # 💡 COMPUTED VARS PARA PERFORMANCE
    # ==========================================
    
    @rx.var(cache=True)
    def cache_hit_rate(self) -> float:
        """Tasa de aciertos del cache"""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    @rx.var(cache=True)
    def performance_summary(self) -> Dict[str, Any]:
        """Resumen general de performance"""
        return {
            "total_operaciones": self.total_operaciones,
            "operaciones_exitosas": self.operaciones_exitosas,
            "tasa_exito": (self.operaciones_exitosas / self.total_operaciones * 100) if self.total_operaciones > 0 else 0.0,
            "tiempo_promedio": f"{self.tiempo_promedio_operacion:.2f}ms",
            "cache_hit_rate": f"{self.cache_hit_rate:.1f}%",
            "cache_size": f"{self.cache_size_mb:.1f}MB"
        }
    
    @rx.var(cache=True)
    def slow_operations(self) -> List[PerformanceMetric]:
        """Lista de operaciones lentas"""
        return [
            metric for metric in self.metricas_operaciones[-50:]  # Últimas 50
            if metric.duration and metric.duration > self.slow_operation_threshold_ms
        ]
    
    @rx.var(cache=True)
    def cache_status(self) -> Dict[str, Any]:
        """Estado actual del cache"""
        total_entries = len(self.cache_entries)
        expired_entries = sum(1 for entry in self.cache_entries.values() if entry.is_expired)
        
        return {
            "total_entries": total_entries,
            "expired_entries": expired_entries,
            "valid_entries": total_entries - expired_entries,
            "size_mb": self.cache_size_mb,
            "hit_rate": self.cache_hit_rate
        }
    
    # ==========================================
    # ⚡ MÉTODOS PRINCIPALES DE OPTIMIZACIÓN
    # ==========================================
    
    def start_performance_tracking(self, operation_name: str) -> str:
        """
        🚀 Iniciar tracking de performance para una operación
        """
        if not self.optimizer_enabled:
            return operation_name
        
        metric = PerformanceMetric(
            operation_name=operation_name,
            start_time=time.time() * 1000,  # En millisegundos
            memory_before=self._get_memory_usage()
        )
        
        self.metricas_operaciones.append(metric)
        self.operacion_actual = operation_name
        self.tiempo_inicio_operacion = metric.start_time
        
        return operation_name
    
    def end_performance_tracking(self, operation_name: str, success: bool = True, error: Optional[str] = None):
        """
        🏁 Finalizar tracking de performance
        """
        if not self.optimizer_enabled:
            return
        
        # Encontrar la métrica correspondiente
        for metric in reversed(self.metricas_operaciones):
            if metric.operation_name == operation_name and metric.end_time is None:
                metric.end_time = time.time() * 1000
                metric.duration = metric.end_time - metric.start_time
                metric.memory_after = self._get_memory_usage()
                metric.error = error
                break
        
        # Actualizar contadores
        self.total_operaciones += 1
        if success and not error:
            self.operaciones_exitosas += 1
        
        # Actualizar tiempo promedio
        duraciones = [m.duration for m in self.metricas_operaciones if m.duration is not None]
        if duraciones:
            self.tiempo_promedio_operacion = sum(duraciones) / len(duraciones)
        
        # Limpiar métricas antiguas
        self._cleanup_old_metrics()
        
        self.operacion_actual = None
        self.tiempo_inicio_operacion = None
    
    def get_cached_data(self, key: str, data_type: str = "general") -> Optional[Any]:
        """
        🗄️ Obtener datos del cache con tracking
        """
        if not self.optimizer_enabled or key not in self.cache_entries:
            self.cache_misses += 1
            return None
        
        entry = self.cache_entries[key]
        
        # Verificar expiración
        if entry.is_expired:
            del self.cache_entries[key]
            self.cache_misses += 1
            return None
        
        # Actualizar estadísticas de acceso
        entry.last_accessed = datetime.now()
        entry.access_count += 1
        
        self.cache_hits += 1
        return entry.value
    
    def set_cached_data(self, key: str, value: Any, data_type: str = "general", ttl_override: Optional[int] = None):
        """
        💾 Guardar datos en cache
        """
        if not self.optimizer_enabled:
            return
        
        # Determinar TTL
        ttl = ttl_override or self.cache_ttl_config.get(data_type, 300)
        
        # Crear entrada de cache
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            ttl_seconds=ttl
        )
        
        self.cache_entries[key] = entry
        
        # Actualizar tamaño del cache (estimación)
        self._update_cache_size()
        
        # Limpiar cache si excede el límite
        if self.cache_size_mb > self.max_cache_size_mb:
            self._cleanup_cache_by_size()
    
    async def preload_critical_data(self, user_id: str, role: str = "odontologo"):
        """
        🚀 Preload datos críticos basado en rol de usuario
        """
        if not self.optimizer_enabled or self.preloading_activo:
            return
        
        self.preloading_activo = True
        self.preload_queue = []
        self.preload_completed = []
        self.preload_progreso = 0.0
        
        try:
            # Determinar qué preloadear según el rol
            if role == "odontologo":
                self.preload_queue = [
                    "servicios_odontologicos",
                    "pacientes_asignados", 
                    "dientes_fdi",
                    "estadisticas_basicas"
                ]
            elif role == "administrador":
                self.preload_queue = [
                    "todos_servicios",
                    "estadisticas_generales",
                    "configuracion_sistema"
                ]
            
            total_items = len(self.preload_queue)
            
            # Ejecutar preload
            for i, item in enumerate(self.preload_queue):
                try:
                    await self._preload_item(item, user_id)
                    self.preload_completed.append(item)
                    self.preload_progreso = (i + 1) / total_items * 100
                    
                except Exception as e:
                    print(f"Error preloading {item}: {e}")
                    continue
            
        finally:
            self.preloading_activo = False
    
    async def _preload_item(self, item: str, user_id: str):
        """
        📦 Preload de un item específico
        """
        self.start_performance_tracking(f"preload_{item}")
        
        try:
            if item == "servicios_odontologicos":
                # Preload servicios para odontólogos
                from dental_system.services.servicios_service import servicios_service
                servicios = await servicios_service.get_filtered_services(activos_only=True)
                self.set_cached_data("servicios_odontologicos", servicios, "servicios")
                self.servicios_preloaded = servicios
                
            elif item == "pacientes_asignados":
                # Preload pacientes del odontólogo
                app_state = self.get_state(AppState)
                if app_state.id_personal:
                    from dental_system.services.odontologia_service import odontologia_service
                    pacientes = await odontologia_service.get_pacientes_asignados(app_state.id_personal)
                    self.set_cached_data(f"pacientes_{app_state.id_personal}", pacientes, "pacientes")
                    self.pacientes_preloaded = pacientes
                
            elif item == "dientes_fdi":
                # Preload estructura FDI
                from dental_system.services.odontologia_service import odontologia_service
                dientes = await odontologia_service.get_dientes_fdi()
                self.set_cached_data("dientes_fdi", dientes, "odontograma", ttl_override=1800)  # 30 min
                
            elif item == "estadisticas_basicas":
                # Preload estadísticas básicas
                app_state = self.get_state(AppState)
                if app_state.id_personal:
                    from dental_system.services.odontologia_service import odontologia_service
                    stats = await odontologia_service.get_estadisticas_odontologo(app_state.id_personal)
                    self.set_cached_data(f"stats_{app_state.id_personal}", stats, "estadisticas")
            
            self.end_performance_tracking(f"preload_{item}", True)
            
        except Exception as e:
            self.end_performance_tracking(f"preload_{item}", False, str(e))
            raise
    
    # ==========================================
    # 🧹 MÉTODOS DE LIMPIEZA Y MANTENIMIENTO
    # ==========================================
    
    def _cleanup_old_metrics(self):
        """Limpiar métricas antiguas"""
        if len(self.metricas_operaciones) > self.max_metrics_history:
            self.metricas_operaciones = self.metricas_operaciones[-self.max_metrics_history:]
    
    def _update_cache_size(self):
        """Actualizar estimación del tamaño del cache"""
        # Estimación simple basada en número de entradas
        # En producción se podría usar sys.getsizeof para mayor precisión
        estimated_size = len(self.cache_entries) * 0.1  # 100KB por entrada promedio
        self.cache_size_mb = estimated_size
    
    def _cleanup_cache_by_size(self):
        """Limpiar cache por tamaño (LRU)"""
        if not self.auto_cleanup_cache:
            return
        
        # Ordenar por último acceso (LRU)
        sorted_entries = sorted(
            self.cache_entries.items(),
            key=lambda x: x[1].last_accessed
        )
        
        # Remover 25% de las entradas más antiguas
        entries_to_remove = len(sorted_entries) // 4
        for i in range(entries_to_remove):
            key = sorted_entries[i][0]
            del self.cache_entries[key]
        
        self._update_cache_size()
    
    def cleanup_expired_cache(self):
        """
        🧹 Limpiar entradas de cache expiradas
        """
        if not self.optimizer_enabled:
            return
        
        expired_keys = [
            key for key, entry in self.cache_entries.items()
            if entry.is_expired
        ]
        
        for key in expired_keys:
            del self.cache_entries[key]
        
        self._update_cache_size()
        
        if expired_keys:
            print(f"✅ Cache cleanup: Removed {len(expired_keys)} expired entries")
    
    def clear_all_cache(self):
        """🗑️ Limpiar todo el cache"""
        self.cache_entries = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache_size_mb = 0.0
        print("✅ All cache cleared")
    
    def _get_memory_usage(self) -> float:
        """Obtener uso de memoria (mock)"""
        # En producción usaría psutil o similar
        import sys
        return sys.getsizeof(self.cache_entries) / 1024 / 1024  # MB
    
    # ==========================================
    # 🔧 CONFIGURACIÓN Y UTILIDADES
    # ==========================================
    
    def configure_cache_ttl(self, data_type: str, ttl_seconds: int):
        """⚙️ Configurar TTL para tipo de datos"""
        self.cache_ttl_config[data_type] = ttl_seconds
    
    def toggle_optimizer(self):
        """🔄 Toggle del optimizer"""
        self.optimizer_enabled = not self.optimizer_enabled
        if not self.optimizer_enabled:
            self.clear_all_cache()
    
    def get_performance_report(self) -> Dict[str, Any]:
        """📊 Generar reporte completo de performance"""
        recent_metrics = self.metricas_operaciones[-100:]  # Últimas 100 operaciones
        
        return {
            "general": self.performance_summary,
            "cache": self.cache_status,
            "slow_operations": len(self.slow_operations),
            "recent_operations": len(recent_metrics),
            "preload_status": {
                "active": self.preloading_activo,
                "progress": self.preload_progreso,
                "completed_items": len(self.preload_completed)
            }
        }


# ==========================================
# 🎨 COMPONENTE UI DEL PERFORMANCE OPTIMIZER
# ==========================================

def performance_monitor_dashboard() -> rx.Component:
    """📊 Dashboard del monitor de performance"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.icon("zap", size=24, color="orange.500"),
                rx.text("Performance Monitor", weight="bold", size="5"),
                rx.spacer(),
                rx.switch(
                    checked=EstadoPerformanceOptimizer.optimizer_enabled,
                    on_change=EstadoPerformanceOptimizer.toggle_optimizer
                ),
                width="100%",
                align_items="center"
            ),
            
            # Métricas principales
            rx.grid(
                rx.stat(
                    rx.stat_label("Operaciones Totales"),
                    rx.stat_number(EstadoPerformanceOptimizer.total_operaciones),
                    rx.stat_help_text(f"{EstadoPerformanceOptimizer.operaciones_exitosas} exitosas")
                ),
                rx.stat(
                    rx.stat_label("Cache Hit Rate"),
                    rx.stat_number(f"{EstadoPerformanceOptimizer.cache_hit_rate:.1f}%"),
                    rx.stat_help_text(f"Hits: {EstadoPerformanceOptimizer.cache_hits}")
                ),
                rx.stat(
                    rx.stat_label("Tiempo Promedio"),
                    rx.stat_number(f"{EstadoPerformanceOptimizer.tiempo_promedio_operacion:.1f}ms"),
                    rx.stat_help_text("Por operación")
                ),
                rx.stat(
                    rx.stat_label("Cache Size"),
                    rx.stat_number(f"{EstadoPerformanceOptimizer.cache_size_mb:.1f}MB"),
                    rx.stat_help_text(f"{len(EstadoPerformanceOptimizer.cache_entries)} entradas")
                ),
                columns="4",
                spacing="4",
                width="100%"
            ),
            
            # Controles
            rx.hstack(
                rx.button(
                    "Cleanup Cache",
                    on_click=EstadoPerformanceOptimizer.cleanup_expired_cache,
                    size="2"
                ),
                rx.button(
                    "Clear All Cache", 
                    on_click=EstadoPerformanceOptimizer.clear_all_cache,
                    variant="outline",
                    size="2"
                ),
                spacing="2"
            ),
            
            spacing="4",
            width="100%"
        ),
        padding="4",
        border_radius="lg",
        border="1px solid",
        border_color="gray.200",
        background="white",
        width="100%"
    )


# ==========================================
# 🚀 DECORADORES PARA LAZY LOADING
# ==========================================

def with_performance_tracking(operation_name: str):
    """
    🎯 Decorador para tracking automático de performance
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            # Para métodos async
            optimizer = EstadoPerformanceOptimizer()
            optimizer.start_performance_tracking(operation_name)
            
            try:
                result = await func(*args, **kwargs)
                optimizer.end_performance_tracking(operation_name, True)
                return result
            except Exception as e:
                optimizer.end_performance_tracking(operation_name, False, str(e))
                raise
        
        def sync_wrapper(*args, **kwargs):
            # Para métodos sync
            optimizer = EstadoPerformanceOptimizer()
            optimizer.start_performance_tracking(operation_name)
            
            try:
                result = func(*args, **kwargs)
                optimizer.end_performance_tracking(operation_name, True)
                return result
            except Exception as e:
                optimizer.end_performance_tracking(operation_name, False, str(e))
                raise
        
        # Determinar si la función es async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def with_caching(cache_key_template: str, data_type: str = "general", ttl: Optional[int] = None):
    """
    🗄️ Decorador para cache automático
    """
    def decorator(func):
        async def async_wrapper(self, *args, **kwargs):
            optimizer = self.get_state(EstadoPerformanceOptimizer)
            
            # Generar key del cache
            cache_key = cache_key_template.format(*args, **kwargs)
            
            # Intentar obtener del cache
            cached_result = optimizer.get_cached_data(cache_key, data_type)
            if cached_result is not None:
                return cached_result
            
            # Ejecutar función y cachear resultado
            result = await func(self, *args, **kwargs)
            optimizer.set_cached_data(cache_key, result, data_type, ttl)
            
            return result
        
        def sync_wrapper(self, *args, **kwargs):
            optimizer = self.get_state(EstadoPerformanceOptimizer)
            
            cache_key = cache_key_template.format(*args, **kwargs)
            cached_result = optimizer.get_cached_data(cache_key, data_type)
            if cached_result is not None:
                return cached_result
            
            result = func(self, *args, **kwargs)
            optimizer.set_cached_data(cache_key, result, data_type, ttl)
            
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def lazy_component(condition_check: Callable[[], bool], fallback_component: rx.Component = None):
    """
    🔄 Decorador para lazy loading de componentes
    """
    def decorator(component_func):
        def wrapper(*args, **kwargs):
            if condition_check():
                return component_func(*args, **kwargs)
            else:
                return fallback_component or rx.box(
                    rx.spinner(size="4"),
                    rx.text("Loading...", size="2"),
                    display="flex",
                    flex_direction="column",
                    align_items="center",
                    padding="4"
                )
        return wrapper
    return decorator