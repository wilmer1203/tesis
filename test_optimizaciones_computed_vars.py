#!/usr/bin/env python3
"""
🧪 TEST DE OPTIMIZACIONES - COMPUTED VARIABLES CON CACHE
===========================================================

Script para validar que las optimizaciones aplicadas funcionan correctamente.
"""

import sys
import time
from typing import List

def test_imports():
    """Verificar que los imports funcionen después de los cambios"""
    try:
        # Intentar importar el AppState modificado
        from dental_system.state.app_state import AppState
        print("✅ Import de AppState exitoso")
        return True
    except Exception as e:
        print(f"❌ Error importando AppState: {e}")
        return False

def test_computed_variables_structure():
    """Verificar que las computed variables optimizadas mantengan su estructura"""
    try:
        from dental_system.state.app_state import AppState
        
        # Crear instancia de prueba
        app_state = AppState()
        
        # Lista de computed variables que deberían tener cache
        optimized_vars = [
            'pacientes_filtrado',
            'consultas_programadas', 
            'consultas_en_progreso',
            'consultas_completadas',
            'servicios_opciones',
            'precio_servicio_base',
            'consultas_filtradas',
            'personal_filtrados',
            'odontologos_options',
            'tipos_personal_options',
            'estados_consulta_options',
            'estados_personal_options',
            'consultas_canceladas',
            'pacientes_asignados_count',
            'pacientes_disponibles_odontologia_count',
            'intervenciones_hoy_count',
            'tiene_odontograma_actual',
            'servicio_seleccionado_nombre',
            'condiciones_registradas_count'
        ]
        
        print("🔍 Verificando computed variables optimizadas:")
        
        for var_name in optimized_vars:
            if hasattr(app_state, var_name):
                # Intentar acceder a la variable
                try:
                    _ = getattr(app_state, var_name)
                    print(f"  ✅ {var_name}: Funciona correctamente")
                except Exception as e:
                    print(f"  ❌ {var_name}: Error - {e}")
                    return False
            else:
                print(f"  ⚠️ {var_name}: No encontrada")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de estructura: {e}")
        return False

def verificar_archivo_modificado():
    """Verificar que el archivo fue modificado correctamente"""
    try:
        with open("dental_system/state/app_state.py", "r", encoding="utf-8") as f:
            contenido = f.read()
        
        # Contar optimizaciones aplicadas
        optimizaciones_encontradas = contenido.count("@rx.var(cache=True)")
        
        print(f"📊 Optimizaciones encontradas: {optimizaciones_encontradas}")
        
        # Verificar algunas optimizaciones específicas
        optimizaciones_clave = [
            "def pacientes_filtrado(self) -> List[PacienteModel]:",
            "def consultas_programadas(self) -> int:",  
            "def consultas_en_progreso(self) -> int:",
            "def servicios_opciones(self) -> List[str]:",
        ]
        
        for opt in optimizaciones_clave:
            if opt in contenido:
                print(f"  ✅ Optimización aplicada: {opt.split('def ')[1].split('(')[0]}")
            else:
                print(f"  ❌ Optimización NO aplicada: {opt.split('def ')[1].split('(')[0]}")
                return False
        
        return optimizaciones_encontradas >= 15  # Esperamos al menos 15 optimizaciones
        
    except Exception as e:
        print(f"❌ Error verificando archivo: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("🚀 INICIANDO TESTS DE OPTIMIZACIÓN COMPUTED VARIABLES")
    print("=" * 60)
    
    tests = [
        ("📁 Verificar archivo modificado", verificar_archivo_modificado),
        ("📦 Test de imports", test_imports),
        ("🧮 Test estructura computed variables", test_computed_variables_structure),
    ]
    
    resultados = []
    
    for nombre_test, funcion_test in tests:
        print(f"\n{nombre_test}:")
        print("-" * 40)
        
        start_time = time.time()
        resultado = funcion_test()
        end_time = time.time()
        
        resultados.append(resultado)
        
        if resultado:
            print(f"✅ ÉXITO en {end_time - start_time:.3f}s")
        else:
            print(f"❌ FALLO en {end_time - start_time:.3f}s")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS:")
    
    exitos = sum(resultados)
    total = len(resultados)
    
    for i, (nombre, _) in enumerate(tests):
        status = "✅ EXITOSO" if resultados[i] else "❌ FALLÓ"
        print(f"  {nombre}: {status}")
    
    print(f"\n🎯 RESULTADO FINAL: {exitos}/{total} tests exitosos")
    
    if exitos == total:
        print("🏆 ¡TODAS LAS OPTIMIZACIONES APLICADAS CORRECTAMENTE!")
        return True
    else:
        print("⚠️ Algunas optimizaciones requieren revisión")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)