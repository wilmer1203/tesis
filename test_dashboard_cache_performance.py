"""
🧪 TEST DE PERFORMANCE - Dashboard Cache System
==============================================

PROPÓSITO: Validar y medir mejoras de performance del nuevo sistema de cache

TESTS INCLUIDOS:
1. ✅ Funcionalidad básica del cache manager
2. ⚡ Performance comparison: sin cache vs con cache  
3. 🗑️ Validación de invalidación automática
4. 📊 Métricas de hit rate del cache
5. 🚀 Testing de computed vars optimizados

EJECUTAR: python test_dashboard_cache_performance.py
"""

import asyncio
import time
from datetime import datetime
import sys
import os

# Añadir el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dental_system.services.cache_manager import dashboard_cache, get_cache_info
from dental_system.services.dashboard_service import dashboard_service
from dental_system.services.cache_invalidation_hooks import (
    invalidate_after_patient_operation, 
    CacheInvalidationHooks,
    invalidation_tracker
)

class DashboardCachePerformanceTest:
    """
    🧪 SUITE DE TESTS DE PERFORMANCE PARA DASHBOARD CACHE
    """
    
    def __init__(self):
        self.results = {
            'cache_functionality': False,
            'performance_improvement': 0.0,
            'invalidation_working': False,
            'hit_rate': 0.0,
            'memory_usage_kb': 0.0,
            'test_errors': []
        }
    
    def log_test(self, test_name: str, status: str, message: str = ""):
        """📝 Log de tests con formato consistente"""
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏳"
        print(f"{status_emoji} {test_name}: {message}")
    
    async def test_cache_basic_functionality(self):
        """
        ✅ TEST 1: FUNCIONALIDAD BÁSICA DEL CACHE
        
        Verifica que el cache almacene y recupere valores correctamente
        """
        try:
            print("\n🧪 TEST 1: Funcionalidad básica del cache")
            
            # Función mock para testear
            async def mock_expensive_function():
                await asyncio.sleep(0.1)  # Simular operación costosa
                return {"test_value": 42, "timestamp": time.time()}
            
            # Primera llamada - debe ejecutar la función
            start_time = time.time()
            result1 = await dashboard_cache.get_async('test_key', mock_expensive_function)
            first_call_time = time.time() - start_time
            
            # Segunda llamada - debe usar cache
            start_time = time.time()
            result2 = await dashboard_cache.get_async('test_key', mock_expensive_function)
            second_call_time = time.time() - start_time
            
            # Validaciones
            cache_working = (
                result1['test_value'] == result2['test_value'] and
                result1['timestamp'] == result2['timestamp'] and
                second_call_time < first_call_time / 2  # Cache debe ser mucho más rápido
            )
            
            if cache_working:
                self.results['cache_functionality'] = True
                self.log_test("Cache Functionality", "PASS", 
                             f"Primera: {first_call_time:.3f}s, Segunda: {second_call_time:.3f}s")
            else:
                self.log_test("Cache Functionality", "FAIL", "Cache no está funcionando correctamente")
            
        except Exception as e:
            self.results['test_errors'].append(f"Cache functionality test: {str(e)}")
            self.log_test("Cache Functionality", "FAIL", f"Error: {e}")
    
    async def test_dashboard_stats_performance(self):
        """
        ⚡ TEST 2: PERFORMANCE DE ESTADÍSTICAS DEL DASHBOARD
        
        Compara performance sin cache vs con cache
        """
        try:
            print("\n🧪 TEST 2: Performance de estadísticas del dashboard")
            
            # Limpiar cache para empezar limpio
            dashboard_cache.invalidate_all()
            
            # Mock user context para testing
            dashboard_service.set_user_context(
                "test_user_id", 
                {"rol": {"nombre": "gerente"}, "email": "test@test.com"}
            )
            
            # Test sin cache (primera ejecución)
            times_without_cache = []
            for i in range(3):
                dashboard_cache.invalidate_all()  # Forzar recarga
                
                start_time = time.time()
                stats = await dashboard_service.get_dashboard_stats("gerente")
                execution_time = time.time() - start_time
                times_without_cache.append(execution_time)
                
                print(f"   Ejecución {i+1} sin cache: {execution_time:.3f}s")
            
            # Test con cache (ejecuciones posteriores)
            times_with_cache = []
            for i in range(3):
                start_time = time.time()
                stats = await dashboard_service.get_dashboard_stats("gerente")
                execution_time = time.time() - start_time
                times_with_cache.append(execution_time)
                
                print(f"   Ejecución {i+1} con cache: {execution_time:.3f}s")
            
            # Calcular mejora de performance
            avg_without_cache = sum(times_without_cache) / len(times_without_cache)
            avg_with_cache = sum(times_with_cache) / len(times_with_cache)
            
            if avg_without_cache > 0:
                improvement = ((avg_without_cache - avg_with_cache) / avg_without_cache) * 100
                self.results['performance_improvement'] = improvement
                
                if improvement > 30:  # Esperamos al menos 30% de mejora
                    self.log_test("Performance Improvement", "PASS", 
                                 f"Mejora: {improvement:.1f}% ({avg_without_cache:.3f}s → {avg_with_cache:.3f}s)")
                else:
                    self.log_test("Performance Improvement", "FAIL", 
                                 f"Mejora insuficiente: {improvement:.1f}%")
            else:
                self.log_test("Performance Improvement", "FAIL", "No se pudo medir performance")
            
        except Exception as e:
            self.results['test_errors'].append(f"Performance test: {str(e)}")
            self.log_test("Performance Improvement", "FAIL", f"Error: {e}")
    
    async def test_cache_invalidation(self):
        """
        🗑️ TEST 3: INVALIDACIÓN AUTOMÁTICA DE CACHE
        
        Verifica que el cache se invalide correctamente
        """
        try:
            print("\n🧪 TEST 3: Invalidación automática de cache")
            
            # Llenar cache con datos
            await dashboard_service.get_dashboard_stats("gerente")
            
            # Verificar que hay entradas en cache
            cache_info_before = get_cache_info()
            entries_before = cache_info_before['stats']['current_entries']
            
            if entries_before == 0:
                self.log_test("Cache Invalidation", "FAIL", "No hay entradas en cache para invalidar")
                return
            
            # Invalidar cache de pacientes
            invalidate_after_patient_operation()
            
            # Verificar invalidación
            cache_info_after = get_cache_info()
            entries_after = cache_info_after['stats']['current_entries']
            
            # Verificar que se invalidaron algunas entradas
            invalidation_working = entries_after < entries_before
            
            if invalidation_working:
                self.results['invalidation_working'] = True
                self.log_test("Cache Invalidation", "PASS", 
                             f"Entradas: {entries_before} → {entries_after}")
            else:
                self.log_test("Cache Invalidation", "FAIL", 
                             f"No se invalidó cache: {entries_before} → {entries_after}")
            
        except Exception as e:
            self.results['test_errors'].append(f"Invalidation test: {str(e)}")
            self.log_test("Cache Invalidation", "FAIL", f"Error: {e}")
    
    async def test_cache_hit_rate(self):
        """
        📊 TEST 4: HIT RATE DEL CACHE
        
        Verifica que el cache tenga un hit rate aceptable
        """
        try:
            print("\n🧪 TEST 4: Hit rate del cache")
            
            # Limpiar estadísticas
            dashboard_cache._stats = {'hits': 0, 'misses': 0, 'total_requests': 0, 'invalidations': 0}
            dashboard_cache.invalidate_all()
            
            # Hacer múltiples llamadas
            for i in range(10):
                await dashboard_service.get_dashboard_stats("gerente")
            
            # Obtener estadísticas
            cache_stats = dashboard_cache.get_stats()
            hit_rate = cache_stats.get('hit_rate_percent', 0)
            
            self.results['hit_rate'] = hit_rate
            
            if hit_rate >= 50:  # Esperamos al menos 50% hit rate
                self.log_test("Cache Hit Rate", "PASS", 
                             f"Hit rate: {hit_rate:.1f}% ({cache_stats['cache_hits']}/{cache_stats['total_requests']})")
            else:
                self.log_test("Cache Hit Rate", "FAIL", 
                             f"Hit rate bajo: {hit_rate:.1f}%")
            
        except Exception as e:
            self.results['test_errors'].append(f"Hit rate test: {str(e)}")
            self.log_test("Cache Hit Rate", "FAIL", f"Error: {e}")
    
    async def test_memory_usage(self):
        """
        💾 TEST 5: USO DE MEMORIA DEL CACHE
        
        Verifica que el uso de memoria sea razonable
        """
        try:
            print("\n🧪 TEST 5: Uso de memoria del cache")
            
            # Llenar cache con datos
            for role in ["gerente", "administrador", "odontologo"]:
                await dashboard_service.get_dashboard_stats(role)
            
            # Obtener información de memoria
            memory_info = dashboard_cache.get_memory_usage()
            memory_kb = memory_info['total_size_kb']
            
            self.results['memory_usage_kb'] = memory_kb
            
            # Considerar aceptable menos de 1MB
            if memory_kb < 1024:
                self.log_test("Memory Usage", "PASS", 
                             f"Memoria usada: {memory_kb:.2f} KB ({memory_info['entries_count']} entradas)")
            else:
                self.log_test("Memory Usage", "FAIL", 
                             f"Uso de memoria alto: {memory_kb:.2f} KB")
            
        except Exception as e:
            self.results['test_errors'].append(f"Memory test: {str(e)}")
            self.log_test("Memory Usage", "FAIL", f"Error: {e}")
    
    def print_summary(self):
        """
        📋 IMPRIMIR RESUMEN FINAL DE TESTS
        """
        print("\n" + "="*60)
        print("📋 RESUMEN DE TESTS - DASHBOARD CACHE PERFORMANCE")
        print("="*60)
        
        print(f"✅ Cache Functionality:     {'PASS' if self.results['cache_functionality'] else 'FAIL'}")
        print(f"⚡ Performance Improvement: {self.results['performance_improvement']:.1f}%")
        print(f"🗑️ Cache Invalidation:      {'PASS' if self.results['invalidation_working'] else 'FAIL'}")
        print(f"📊 Cache Hit Rate:          {self.results['hit_rate']:.1f}%")
        print(f"💾 Memory Usage:            {self.results['memory_usage_kb']:.2f} KB")
        
        if self.results['test_errors']:
            print("\n❌ Errores encontrados:")
            for error in self.results['test_errors']:
                print(f"   - {error}")
        
        # Evaluación general
        success_count = sum([
            self.results['cache_functionality'],
            self.results['performance_improvement'] > 30,
            self.results['invalidation_working'],
            self.results['hit_rate'] >= 50,
            self.results['memory_usage_kb'] < 1024
        ])
        
        print(f"\n🎯 RESULTADO GENERAL: {success_count}/5 tests pasados")
        
        if success_count >= 4:
            print("🚀 ÉXITO: Sistema de cache funcionando correctamente!")
        elif success_count >= 2:
            print("⚠️ PARCIAL: Cache funcional con algunas mejoras necesarias")
        else:
            print("❌ FALLO: Sistema de cache requiere revisión")
    
    async def run_all_tests(self):
        """
        🏃‍♂️ EJECUTAR TODOS LOS TESTS
        """
        print("🧪 INICIANDO TESTS DE PERFORMANCE - DASHBOARD CACHE")
        print("=" * 60)
        
        start_time = time.time()
        
        # Ejecutar tests en secuencia
        await self.test_cache_basic_functionality()
        await self.test_dashboard_stats_performance()
        await self.test_cache_invalidation()
        await self.test_cache_hit_rate()
        await self.test_memory_usage()
        
        total_time = time.time() - start_time
        
        # Mostrar resumen
        self.print_summary()
        print(f"\n⏱️ Tiempo total de tests: {total_time:.2f}s")

async def main():
    """
    🎯 FUNCIÓN PRINCIPAL DE TESTING
    """
    try:
        # Crear y ejecutar suite de tests
        test_suite = DashboardCachePerformanceTest()
        await test_suite.run_all_tests()
        
        # Información adicional del cache
        print("\n📊 INFORMACIÓN ADICIONAL DEL CACHE:")
        cache_info = get_cache_info()
        print(f"   Stats: {cache_info['stats']}")
        print(f"   Timestamp: {cache_info['timestamp']}")
        
    except Exception as e:
        print(f"❌ Error ejecutando tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ejecutar tests
    asyncio.run(main())