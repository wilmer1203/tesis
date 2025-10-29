"""
🔍 SCRIPT DE DEPURACIÓN - ODONTOGRAMA
====================================

Ejecutar este script para diagnosticar por qué los dientes no se ven verdes.

Uso:
    python test_odontologia.py
"""

import asyncio
import sys
import os

# Agregar el path del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dental_system.services.odontologia_service import odontologia_service


async def test_odontogram_colors():
    """Probar carga de odontograma y verificar colores"""

    print("\n" + "="*80)
    print("🔍 TEST DE DIAGNÓSTICO DE COLORES DEL ODONTOGRAMA")
    print("="*80)

    # PASO 1: Verificar conexión
    print("\n📡 PASO 1: Verificando conexión a BD...")
    try:
        from dental_system.supabase.client import get_client
        client = get_client()
        print("✅ Conexión exitosa")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # PASO 2: Buscar un paciente de prueba
    print("\n👤 PASO 2: Buscando paciente de prueba...")
    try:
        response = client.table("pacientes").select("id, primer_nombre, primer_apellido").limit(1).execute()
        if not response.data:
            print("❌ No hay pacientes en BD")
            return

        paciente = response.data[0]
        paciente_id = paciente['id']
        print(f"✅ Paciente encontrado: {paciente['primer_nombre']} {paciente['primer_apellido']}")
        print(f"   ID: {paciente_id}")
    except Exception as e:
        print(f"❌ Error buscando paciente: {e}")
        return

    # PASO 3: Cargar odontograma
    print(f"\n🦷 PASO 3: Cargando odontograma del paciente...")
    try:
        result = await odontologia_service.get_patient_odontogram(paciente_id)

        print(f"\n📊 RESULTADO DEL SERVICIO:")
        print(f"   - Total dientes: {result.get('total_dientes', 0)}")
        print(f"   - Total condiciones: {result.get('total_condiciones', 0)}")
        print(f"   - Última actualización: {result.get('fecha_ultima_actualizacion', 'N/A')}")

        conditions = result.get("conditions", {})

        if not conditions:
            print("\n⚠️ PROBLEMA DETECTADO: conditions está vacío!")
            print("   Posible causa: El paciente no tiene odontograma auto-creado")
            print("   Solución: Verificar que el trigger SQL esté activo")
            return

        print(f"\n✅ Condiciones cargadas correctamente")
        print(f"   - Tipo de keys: {type(list(conditions.keys())[0]) if conditions else 'N/A'}")
        print(f"   - Muestra de keys: {list(conditions.keys())[:5]}")

    except Exception as e:
        print(f"❌ Error cargando odontograma: {e}")
        import traceback
        traceback.print_exc()
        return

    # PASO 4: Simular get_teeth_data()
    print(f"\n🎨 PASO 4: Simulando get_teeth_data()...")

    teeth_data = {}
    for diente_num in range(11, 19):  # Solo cuadrante 1 para prueba
        # Probar ambas versiones (int y string)
        condiciones = conditions.get(diente_num, {})
        if not condiciones:
            condiciones = conditions.get(str(diente_num), {})

        if not condiciones:
            print(f"   ⚠️ Diente {diente_num}: SIN CONDICIONES")
            continue

        # Determinar estado
        condiciones_no_sanas = [c for c in condiciones.values() if c != "sano"]

        if any(cond in ["caries", "fractura", "ausente"] for cond in condiciones.values()):
            status = "caries"
        elif any(cond in ["obturacion", "corona", "implante"] for cond in condiciones.values()):
            status = "obturado"
        elif any(cond in ["endodoncia"] for cond in condiciones.values()):
            status = "endodoncia"
        else:
            status = "sano"

        teeth_data[diente_num] = {
            "status": status,
            "has_conditions": len(condiciones_no_sanas) > 0,
            "condiciones": condiciones
        }

        # Simular get_tooth_color()
        from dental_system.components.odontologia.simple_tooth import get_tooth_color
        color = get_tooth_color(status)

        print(f"   🦷 Diente {diente_num}:")
        print(f"      - Condiciones: {condiciones}")
        print(f"      - Status calculado: {status}")
        print(f"      - Color: {color}")
        print(f"      - has_conditions: {teeth_data[diente_num]['has_conditions']}")

    # PASO 5: Diagnóstico final
    print(f"\n" + "="*80)
    print("📋 DIAGNÓSTICO FINAL:")
    print("="*80)

    if not teeth_data:
        print("❌ PROBLEMA: teeth_data está vacío")
        print("   Causa: Las keys de conditions no coinciden con el rango 11-18")
        print(f"   Keys en conditions: {list(conditions.keys())}")
    else:
        sanos = sum(1 for d in teeth_data.values() if d['status'] == 'sano')
        total = len(teeth_data)
        print(f"✅ teeth_data generado correctamente")
        print(f"   - Total dientes procesados: {total}")
        print(f"   - Dientes sanos: {sanos}")
        print(f"   - Dientes con problemas: {total - sanos}")

        # Verificar si todos deberían ser verdes
        if sanos == total:
            print(f"\n✅ TODOS LOS DIENTES DEBERÍAN SER VERDES (#38a169)")
        else:
            print(f"\n⚠️ Solo {sanos}/{total} dientes deberían ser verdes")


if __name__ == "__main__":
    asyncio.run(test_odontogram_colors())
