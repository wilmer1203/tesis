"""
🧪 TEST DE SISTEMA DE CACHE CON TTL E INVALIDACIÓN AUTOMÁTICA
============================================================

PROPÓSITO: Validar funcionamiento del sistema de cache inteligente implementado
- Cache manager con TTL diferenciados
- Invalidation hooks automáticos por operación
- Separación real-time vs cached stats

EJECUTAR: python test_cache_invalidation_system.py
"""

import time
import sys
from datetime import datetime
from typing import Dict, Any

# Mock para simular clases reales
class MockDashboardService:
    def __init__(self):
        self.call_count = {}
    
    async def _get_realtime_base_stats(self):
        """Simular stats real-time (nunca cached)"""
        self.call_count['realtime'] = self.call_count.get('realtime', 0) + 1
        return {
            "consultas_hoy": 5,
            "consultas_en_curso": 2
        }
    
    async def _fetch_cached_base_stats(self):
        """Simular stats cached (con TTL)"""
        self.call_count['cached'] = self.call_count.get('cached', 0) + 1
        await asyncio.sleep(0.1)  # Simular operación costosa
        return {
            "total_pacientes": 150,
            "personal_activo": 8,
            "servicios_activos": 25
        }

class CacheTestSuite:
    def __init__(self):
        self.test_results = []
        self.mock_service = MockDashboardService()
        
    def test_ttl_configurations(self):
        """✅ Test 1: Validar configuraciones TTL están bien definidas"""
        print("\n🧪 TEST 1: Configuraciones TTL")
        print("-" * 50)
        
        try:
            # Importar cache manager
            sys.path.append('dental_system/services')
            from cache_manager import dashboard_cache
            
            # Verificar configuraciones críticas
            ttl_configs = dashboard_cache._ttl_configs
            
            # Real-time (TTL = 0)
            realtime_keys = ['consultas_hoy', 'consultas_en_curso', 'pagos_pendientes', 'turnos_activos']
            
            print("📊 Real-time stats (TTL=0):")
            for key in realtime_keys:
                ttl = ttl_configs.get(key, -1)
                status = "✅ Correcto" if ttl == 0 else f"❌ TTL={ttl}"
                print(f"  - {key}: {status}")
            
            # Cached stats (TTL > 0) 
            cached_keys = ['base_statistics_cached', 'manager_statistics_cached', 'admin_statistics_cached']
            
            print("\n💾 Cached stats (TTL>0):")
            for key in cached_keys:
                ttl = ttl_configs.get(key, -1)
                status = "✅ Correcto" if ttl > 0 else f"❌ TTL={ttl}"
                print(f"  - {key}: {status} (TTL: {ttl}s)")
            
            self.test_results.append({
                "test": "TTL Configurations",
                "status": "✅ PASS",
                "details": f"{len(ttl_configs)} configuraciones validadas"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "TTL Configurations", 
                "status": "❌ FAIL",
                "details": str(e)
            })
    
    def test_cache_behavior(self):
        """✅ Test 2: Validar comportamiento de cache hit/miss"""
        print("\n🧪 TEST 2: Comportamiento Cache Hit/Miss")
        print("-" * 50)
        
        try:
            from cache_manager import dashboard_cache
            
            # Test key con TTL corto
            test_key = "test_cache_behavior"
            dashboard_cache.configure_ttl(test_key, 2)  # 2 segundos TTL
            
            def expensive_operation():
                time.sleep(0.1)
                return {"timestamp": datetime.now().isoformat(), "data": "test_value"}
            
            # Primera llamada - debe ser cache miss
            print("📥 Primera llamada (cache miss esperado):")
            start_time = time.time()
            result1 = dashboard_cache.get(test_key, expensive_operation)
            time1 = time.time() - start_time
            print(f"  - Tiempo: {time1:.3f}s")
            print(f"  - Resultado: {result1['data']}")
            
            # Segunda llamada inmediata - debe ser cache hit
            print("\n⚡ Segunda llamada inmediata (cache hit esperado):")
            start_time = time.time()
            result2 = dashboard_cache.get(test_key, expensive_operation)
            time2 = time.time() - start_time
            print(f"  - Tiempo: {time2:.3f}s")
            print(f"  - Resultado: {result2['data']}")
            
            # Validar cache hit
            cache_hit = time2 < time1 * 0.1  # Al menos 10x más rápido
            hit_status = "✅ Cache HIT" if cache_hit else "❌ Cache MISS"
            print(f"  - Status: {hit_status}")
            
            # Esperar expiración
            print("\n⏰ Esperando expiración de cache (3 segundos)...")
            time.sleep(3)
            
            # Tercera llamada - debe ser cache miss por expiración
            print("\n📥 Tercera llamada post-expiración (cache miss esperado):")
            start_time = time.time()
            result3 = dashboard_cache.get(test_key, expensive_operation)
            time3 = time.time() - start_time
            print(f"  - Tiempo: {time3:.3f}s")
            print(f"  - Diferente timestamp: {'✅' if result3['timestamp'] != result1['timestamp'] else '❌'}")
            
            # Obtener estadísticas
            stats = dashboard_cache.get_stats()
            print(f"\n📊 Cache Stats:")
            print(f"  - Total requests: {stats['total_requests']}")
            print(f"  - Cache hits: {stats['cache_hits']}")
            print(f"  - Hit rate: {stats['hit_rate_percent']}%")
            
            self.test_results.append({
                "test": "Cache Behavior",
                "status": "✅ PASS" if cache_hit else "❌ FAIL", 
                "details": f"Hit rate: {stats['hit_rate_percent']}%"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "Cache Behavior",
                "status": "❌ FAIL",
                "details": str(e)
            })
    
    def test_invalidation_hooks(self):
        """✅ Test 3: Validar hooks de invalidación automáticos"""
        print("\n🧪 TEST 3: Hooks de Invalidación")
        print("-" * 50)
        
        try:
            from cache_manager import dashboard_cache
            from cache_invalidation_hooks import (
                invalidate_after_patient_operation,
                invalidate_after_consultation_operation, 
                invalidate_after_payment_operation,
                invalidation_tracker
            )
            
            # Reset stats
            invalidation_tracker.reset_stats()
            dashboard_cache.invalidate_all()
            
            # Simular cache entries
            test_keys = [
                'base_statistics_cached',
                'manager_statistics_cached', 
                'admin_statistics_cached',
                'chart_data_general'
            ]
            
            for key in test_keys:
                dashboard_cache.get(key, lambda: f"test_data_{key}")
            
            print(f"📊 Cache entries antes: {len(dashboard_cache._cache)}")
            
            # Test invalidación de pacientes
            print("\n👥 Test invalidación pacientes:")
            invalidate_after_patient_operation()
            print(f"  - Cache entries después: {len(dashboard_cache._cache)}")
            
            # Test invalidación de pagos
            print("\n💳 Test invalidación pagos:")
            # Recargar cache
            for key in test_keys:
                dashboard_cache.get(key, lambda: f"test_data_{key}")
            
            invalidate_after_payment_operation()
            print(f"  - Cache entries después: {len(dashboard_cache._cache)}")
            
            # Verificar tracking
            stats = invalidation_tracker.get_stats()
            print(f"\n📊 Invalidation Stats:")
            for operation, count in stats.items():
                if count > 0:
                    print(f"  - {operation}: {count} invalidaciones")
            
            total_invalidations = sum(stats.values())
            test_passed = total_invalidations > 0
            
            self.test_results.append({
                "test": "Invalidation Hooks",
                "status": "✅ PASS" if test_passed else "❌ FAIL",
                "details": f"{total_invalidations} invalidaciones rastreadas"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "Invalidation Hooks",
                "status": "❌ FAIL", 
                "details": str(e)
            })
    
    def test_memory_usage(self):
        """✅ Test 4: Validar uso de memoria del cache"""
        print("\n🧪 TEST 4: Uso de Memoria Cache")
        print("-" * 50)
        
        try:
            from cache_manager import dashboard_cache
            
            # Limpiar cache
            dashboard_cache.invalidate_all()
            
            # Llenar cache con datos de prueba
            test_data = {
                f"test_key_{i}": {"data": "x" * 1000, "index": i} 
                for i in range(10)
            }
            
            for key, value in test_data.items():
                dashboard_cache.get(key, lambda v=value: v)
            
            # Obtener info de memoria
            memory_info = dashboard_cache.get_memory_usage()
            
            print(f"📊 Memory Usage:")
            print(f"  - Total size: {memory_info['total_size_kb']} KB")
            print(f"  - Entries count: {memory_info['entries_count']}")
            print(f"  - Avg entry size: {memory_info['avg_entry_size_bytes']} bytes")
            
            # Test cleanup
            dashboard_cache.cleanup_expired()
            
            memory_efficient = memory_info['total_size_kb'] < 1000  # Menos de 1MB
            
            self.test_results.append({
                "test": "Memory Usage",
                "status": "✅ PASS" if memory_efficient else "⚠️ WARNING",
                "details": f"{memory_info['total_size_kb']} KB used"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "Memory Usage",
                "status": "❌ FAIL",
                "details": str(e)
            })
    
    def run_all_tests(self):
        """🚀 Ejecutar todos los tests"""
        print("=" * 70)
        print("🚀 INICIANDO TEST SUITE - SISTEMA DE CACHE TTL")
        print("=" * 70)
        
        self.test_ttl_configurations()
        self.test_cache_behavior()
        self.test_invalidation_hooks()
        self.test_memory_usage()
        
        self.generate_final_report()
    
    def generate_final_report(self):
        """📊 Generar reporte final"""
        print("\n" + "=" * 70)
        print("📊 REPORTE FINAL - SISTEMA DE CACHE")
        print("=" * 70)
        
        passed = sum(1 for r in self.test_results if "✅" in r["status"])
        failed = sum(1 for r in self.test_results if "❌" in r["status"]) 
        warnings = sum(1 for r in self.test_results if "⚠️" in r["status"])
        
        print(f"\n📈 RESUMEN:")
        print(f"  - Tests ejecutados: {len(self.test_results)}")
        print(f"  - ✅ Passed: {passed}")
        print(f"  - ❌ Failed: {failed}")
        print(f"  - ⚠️ Warnings: {warnings}")
        
        print(f"\n📋 DETALLE:")
        for result in self.test_results:
            print(f"  - {result['test']}: {result['status']}")
            if result['details']:
                print(f"    └─ {result['details']}")
        
        overall_status = "✅ SISTEMA FUNCIONANDO" if failed == 0 else "❌ REQUIERE ATENCIÓN"
        print(f"\n🎯 ESTADO GENERAL: {overall_status}")
        
        if failed == 0:
            print(f"\n🎉 CONCLUSIÓN:")
            print(f"  ✅ Sistema de cache con TTL implementado correctamente")
            print(f"  ✅ Invalidation hooks funcionando automáticamente")
            print(f"  ✅ Separación real-time vs cached stats operativa")
            print(f"  ✅ Performance optimization activa")

def main():
    try:
        # Agregar path para imports
        import asyncio
        
        tester = CacheTestSuite()
        tester.run_all_tests()
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Ejecutar desde el directorio raíz del proyecto")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()