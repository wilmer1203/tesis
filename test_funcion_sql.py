# -*- coding: utf-8 -*-
"""
Test de la función SQL actualizar_condiciones_batch
"""
from dental_system.supabase.client import supabase_client

def test_funcion():
    """Probar que la función SQL existe y funciona"""

    print("Probando función actualizar_condiciones_batch...")

    client = supabase_client.get_client()

    # Obtener un paciente real de la BD
    try:
        pacientes = client.table('pacientes').select('id').limit(1).execute()
        if not pacientes.data:
            print("ERROR: No hay pacientes en la BD")
            return False

        paciente_id = pacientes.data[0]['id']
        print(f"OK: Usando paciente_id: {paciente_id}")
    except Exception as e:
        print(f"ERROR obteniendo paciente: {e}")
        return False

    # Obtener una intervención real
    try:
        intervenciones = client.table('intervenciones').select('id').limit(1).execute()
        if not intervenciones.data:
            print("WARNING: No hay intervenciones, usando UUID dummy")
            intervencion_id = "00000000-0000-0000-0000-000000000001"
        else:
            intervencion_id = intervenciones.data[0]['id']

        print(f"OK: Usando intervencion_id: {intervencion_id}")
    except Exception as e:
        print(f"WARNING: {e}")
        intervencion_id = "00000000-0000-0000-0000-000000000001"

    # Preparar datos de prueba
    test_data = [
        {
            "paciente_id": str(paciente_id),
            "diente_numero": 11,
            "superficie": "oclusal",
            "tipo_condicion": "caries",
            "material_utilizado": "Test",
            "descripcion": "Prueba automatica",
            "intervencion_id": str(intervencion_id),
            "registrado_por": str(paciente_id)  # Usando un ID válido
        }
    ]

    print(f"\nDatos de prueba:")
    print(f"  paciente_id: {test_data[0]['paciente_id']}")
    print(f"  diente_numero: {test_data[0]['diente_numero']}")
    print(f"  superficie: {test_data[0]['superficie']}")
    print(f"  tipo_condicion: {test_data[0]['tipo_condicion']}")

    # Intentar llamar la función
    try:
        print("\nLlamando a actualizar_condiciones_batch...")
        result = client.rpc('actualizar_condiciones_batch', {
            'actualizaciones': test_data
        }).execute()

        print(f"\nRESULTADO:")
        print(f"  {result.data}")

        if result.data:
            data = result.data[0] if isinstance(result.data, list) else result.data
            print(f"\n  Exitosos: {data.get('exitosos', 0)}")
            print(f"  Fallidos: {data.get('fallidos', 0)}")
            print(f"  Total: {data.get('total', 0)}")
            print(f"  Tasa exito: {data.get('tasa_exito_pct', 0)}%")

            if data.get('exitosos', 0) > 0:
                print("\nOK: La función SQL funciona correctamente!")

                # Limpiar test
                print("\nLimpiando test...")
                client.table('condiciones_diente').delete().eq(
                    'descripcion', 'Prueba automatica'
                ).execute()
                print("OK: Test limpiado")

                return True
            else:
                print("\nERROR: La función no actualizó ningún registro")
                print("Revisa los logs de PostgreSQL para ver el error exacto")
                return False
        else:
            print("\nERROR: No hubo respuesta de la función")
            return False

    except Exception as e:
        print(f"\nERROR llamando función: {e}")
        print("\nPosibles causas:")
        print("  1. La función no existe - ejecuta crear_funcion_batch.sql")
        print("  2. Error en los datos - revisa los tipos")
        print("  3. Error en la BD - revisa logs de PostgreSQL")
        return False

if __name__ == "__main__":
    exito = test_funcion()
    if not exito:
        print("\n***** TEST FALLIDO *****")
