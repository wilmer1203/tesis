"""
TEST DE SINCRONIZACION - INTERVENCIONES CON SERVICIOS
=====================================================

Script de testing para verificar que la sincronizacion entre modelos
y base de datos funcione correctamente despues de las actualizaciones.

TESTS IMPLEMENTADOS:
1. Test modelo ServicioIntervencionTemporal con campo superficie
2. Test metodo crear_intervencion_con_servicios existe
3. Test parseo de dientes individuales
4. Test parseo toda la boca
5. Test mapeo de superficies

AUTOR: Claude Code
FECHA: 2025-10-13
"""

import sys
import os

# Agregar path del proyecto
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("\n" + "="*80)
print("INICIANDO TESTS DE SINCRONIZACION")
print("="*80 + "\n")

# ==========================================
# TEST 1: Modelo ServicioIntervencionTemporal
# ==========================================
print("TEST 1: Verificar modelo ServicioIntervencionTemporal...")
try:
    from dental_system.state.estado_intervencion_servicios import ServicioIntervencionTemporal

    # Verificar que tiene el campo correcto
    assert hasattr(ServicioIntervencionTemporal, '__annotations__'), "[FAIL] No tiene annotations"
    annotations = ServicioIntervencionTemporal.__annotations__

    # Verificar campo 'superficie' existe
    assert 'superficie' in annotations, "[FAIL] Campo 'superficie' no encontrado"
    print("  [OK] Campo 'superficie' existe en el modelo")

    # Verificar campo 'diente_numero' existe
    assert 'diente_numero' in annotations, "[FAIL] Campo 'diente_numero' no encontrado"
    print("  [OK] Campo 'diente_numero' existe en el modelo")

    # Verificar que NO existe 'superficie_dental'
    assert 'superficie_dental' not in annotations, "[FAIL] Campo obsoleto 'superficie_dental' aun existe"
    print("  [OK] Campo obsoleto 'superficie_dental' fue eliminado correctamente")

    print("[PASS] TEST 1\n")

except AssertionError as e:
    print(f"[FAIL] TEST 1: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] TEST 1: {e}\n")
    sys.exit(1)


# ==========================================
# TEST 2: Metodo crear_intervencion_con_servicios existe
# ==========================================
print("TEST 2: Verificar metodo crear_intervencion_con_servicios...")
try:
    from dental_system.services.odontologia_service import odontologia_service

    # Verificar que el metodo existe
    assert hasattr(odontologia_service, 'crear_intervencion_con_servicios'), \
        "[FAIL] Metodo 'crear_intervencion_con_servicios' no encontrado"
    print("  [OK] Metodo 'crear_intervencion_con_servicios' existe")

    # Verificar que es async
    import inspect
    metodo = getattr(odontologia_service, 'crear_intervencion_con_servicios')
    assert inspect.iscoroutinefunction(metodo), "[FAIL] Metodo no es async"
    print("  [OK] Metodo es correctamente async")

    print("[PASS] TEST 2\n")

except AssertionError as e:
    print(f"[FAIL] TEST 2: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] TEST 2: {e}\n")
    sys.exit(1)


# ==========================================
# TEST 3: Metodo helper _extraer_numeros_dientes
# ==========================================
print("TEST 3: Verificar metodo _extraer_numeros_dientes...")
try:
    from dental_system.services.odontologia_service import odontologia_service

    # Test con dientes individuales
    dientes = odontologia_service._extraer_numeros_dientes("11, 12, 21")
    assert dientes == [11, 12, 21], f"[FAIL] Esperado [11, 12, 21], obtenido {dientes}"
    print(f"  [OK] Parseo individual: '11, 12, 21' -> {dientes}")

    # Test con "toda la boca"
    dientes_todos = odontologia_service._extraer_numeros_dientes("toda la boca")
    assert len(dientes_todos) == 32, f"[FAIL] Esperado 32 dientes, obtenido {len(dientes_todos)}"
    print(f"  [OK] Parseo 'toda la boca' -> {len(dientes_todos)} dientes")

    # Test con string vacio
    dientes_vacio = odontologia_service._extraer_numeros_dientes("")
    assert dientes_vacio == [], f"[FAIL] Esperado [], obtenido {dientes_vacio}"
    print(f"  [OK] Parseo string vacio -> {dientes_vacio}")

    print("[PASS] TEST 3\n")

except AssertionError as e:
    print(f"[FAIL] TEST 3: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] TEST 3: {e}\n")
    sys.exit(1)


# ==========================================
# TEST 4: Metodo helper _mapear_superficie
# ==========================================
print("TEST 4: Verificar metodo _mapear_superficie...")
try:
    from dental_system.services.odontologia_service import odontologia_service

    # Test superficie individual
    superficie = odontologia_service._mapear_superficie("oclusal")
    assert superficie == ["oclusal"], f"[FAIL] Esperado ['oclusal'], obtenido {superficie}"
    print(f"  [OK] Mapeo 'oclusal' -> {superficie}")

    # Test "completa"
    completa = odontologia_service._mapear_superficie("completa")
    assert len(completa) == 5, f"[FAIL] Esperado 5 superficies, obtenido {len(completa)}"
    print(f"  [OK] Mapeo 'completa' -> {len(completa)} superficies")

    # Test string vacio (todas las superficies)
    todas = odontologia_service._mapear_superficie("")
    assert len(todas) == 5, f"[FAIL] Esperado 5 superficies, obtenido {len(todas)}"
    print(f"  [OK] Mapeo string vacio -> {len(todas)} superficies (todas)")

    print("[PASS] TEST 4\n")

except AssertionError as e:
    print(f"[FAIL] TEST 4: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] TEST 4: {e}\n")
    sys.exit(1)


# ==========================================
# TEST 5: Verificar import de re modulo
# ==========================================
print("TEST 5: Verificar import de modulo 're'...")
try:
    import dental_system.services.odontologia_service as mod
    import inspect

    # Verificar que el modulo usa 're'
    source = inspect.getsource(mod)
    assert 'import re' in source, "[FAIL] Modulo 're' no esta importado"
    print("  [OK] Modulo 're' correctamente importado")

    print("[PASS] TEST 5\n")

except AssertionError as e:
    print(f"[FAIL] TEST 5: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] TEST 5: {e}\n")
    sys.exit(1)


# ==========================================
# RESUMEN FINAL
# ==========================================
print("\n" + "="*80)
print("TODOS LOS TESTS PASARON EXITOSAMENTE")
print("="*80)
print("\nSincronizacion de modelos y servicios completada correctamente")
print("Campo 'superficie' actualizado en modelo")
print("Metodo 'crear_intervencion_con_servicios' implementado")
print("Metodos helper funcionando correctamente")
print("\nProximo paso: Probar en interfaz real con datos de prueba\n")
