# -*- coding: utf-8 -*-
"""
Script para ejecutar migracion manual de condicion_resultante
"""
from dental_system.supabase.client import supabase_client

def ejecutar_migracion():
    """Ejecuta UPDATE directo para poblar condicion_resultante"""

    print("Iniciando migracion de condicion_resultante...")

    client = supabase_client.get_client()

    # PASO 1: Verificar si el campo existe
    try:
        result = client.table('servicios').select('nombre, condicion_resultante').limit(1).execute()
        print("OK: Campo condicion_resultante existe")
    except Exception as e:
        print(f"ERROR: Campo condicion_resultante NO existe: {e}")
        print("\nDEBES EJECUTAR MANUALMENTE:")
        print("  1. Abre Supabase Studio (http://localhost:54323)")
        print("  2. Ve a SQL Editor")
        print("  3. Ejecuta la migracion 20251027_agregar_condicion_resultante_servicios.sql")
        return False

    # PASO 2: Poblar condiciones por tipo de servicio
    updates = {
        "obturacion": ["obturaci", "empaste", "resina"],
        "ausente": ["extracci", "exodoncia"],
        "endodoncia": ["endodoncia", "conducto"],
        "corona": ["corona"],
        "puente": ["puente"],
        "implante": ["implante"],
        "protesis": ["protesis", "dentadura"]
    }

    total_actualizados = 0

    for condicion, keywords in updates.items():
        for keyword in keywords:
            try:
                # Obtener servicios que coincidan
                servicios = client.table('servicios').select('id, nombre').ilike('nombre', f'%{keyword}%').execute()

                if servicios.data:
                    print(f"\nActualizando {len(servicios.data)} servicios con '{keyword}' -> {condicion}")

                    for servicio in servicios.data:
                        # Actualizar uno por uno
                        client.table('servicios').update({
                            'condicion_resultante': condicion
                        }).eq('id', servicio['id']).execute()

                    total_actualizados += len(servicios.data)

            except Exception as e:
                print(f"  Error actualizando '{keyword}': {e}")

    # PASO 3: Servicios preventivos (boca_completa) deben tener NULL
    try:
        servicios_boca = client.table('servicios').select('id').eq('alcance_servicio', 'boca_completa').execute()

        if servicios_boca.data:
            print(f"\nLimpiando {len(servicios_boca.data)} servicios de boca completa...")

            for servicio in servicios_boca.data:
                client.table('servicios').update({
                    'condicion_resultante': None
                }).eq('id', servicio['id']).execute()

    except Exception as e:
        print(f"Error limpiando servicios boca completa: {e}")

    # PASO 4: Verificar resultado
    try:
        all_servicios = client.table('servicios').select('nombre, alcance_servicio, condicion_resultante').execute()

        con_condicion = sum(1 for s in all_servicios.data if s.get('condicion_resultante'))
        sin_condicion = len(all_servicios.data) - con_condicion

        print("\n" + "="*60)
        print("MIGRACION COMPLETADA:")
        print(f"  - Total servicios: {len(all_servicios.data)}")
        print(f"  - Con condicion_resultante: {con_condicion}")
        print(f"  - Sin condicion_resultante (preventivos): {sin_condicion}")
        print("="*60)

        print("\nMUESTRA DE SERVICIOS:")
        for servicio in all_servicios.data[:15]:
            nombre = servicio.get('nombre', 'N/A')[:45]
            condicion = servicio.get('condicion_resultante', 'NULL')
            print(f"  {nombre:45} -> {condicion}")

        return True

    except Exception as e:
        print(f"Error verificando resultados: {e}")
        return False

if __name__ == "__main__":
    resultado = ejecutar_migracion()
    if not resultado:
        print("\n***** MIGRACION FALLIDA *****")
