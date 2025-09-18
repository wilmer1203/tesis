#!/usr/bin/env python3
"""
SCRIPT SIMPLE PARA LIMPIAR BASE DE DATOS DE PACIENTES
Enfoque directo usando consultas SQL
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dental_system.supabase.client import get_client

async def limpiar_datos_directamente():
    """Eliminar datos usando un approach más directo"""

    print("LIMPIEZA DIRECTA DE BASE DE DATOS")
    print("=" * 40)

    respuesta = input("Confirma eliminacion de TODOS los pacientes (SI/no): ")
    if respuesta.upper() != 'SI':
        print("Cancelado")
        return

    supabase = get_client()

    try:
        # 1. Obtener todos los pacientes primero
        print("\n1. Obteniendo lista de pacientes...")
        pacientes_response = supabase.table("pacientes").select("numero_historia").execute()

        if not pacientes_response.data:
            print("No hay pacientes para eliminar")
            return

        print(f"Encontrados {len(pacientes_response.data)} pacientes")

        # 2. Para cada paciente, eliminar en orden correcto
        for paciente in pacientes_response.data:
            hc = paciente['numero_historia']
            print(f"\n2. Eliminando datos del paciente HC: {hc}")

            # 2.1 Condiciones de dientes
            try:
                cond_response = supabase.table("condiciones_diente").delete().eq("numero_historia", hc).execute()
                print(f"   - Condiciones: {len(cond_response.data) if cond_response.data else 0}")
            except Exception as e:
                print(f"   - Error condiciones: {e}")

            # 2.2 Odontograma
            try:
                odonto_response = supabase.table("odontograma").delete().eq("numero_historia", hc).execute()
                print(f"   - Odontograma: {len(odonto_response.data) if odonto_response.data else 0}")
            except Exception as e:
                print(f"   - Error odontograma: {e}")

            # 2.3 Historial médico
            try:
                hist_response = supabase.table("historial_medico").delete().eq("numero_historia", hc).execute()
                print(f"   - Historial: {len(hist_response.data) if hist_response.data else 0}")
            except Exception as e:
                print(f"   - Error historial: {e}")

            # 2.4 Consultas (esto debe eliminar automáticamente intervenciones por CASCADE)
            try:
                consulta_response = supabase.table("consultas").delete().eq("numero_historia", hc).execute()
                print(f"   - Consultas: {len(consulta_response.data) if consulta_response.data else 0}")
            except Exception as e:
                print(f"   - Error consultas: {e}")

            # 2.5 Finalmente el paciente
            try:
                pac_response = supabase.table("pacientes").delete().eq("numero_historia", hc).execute()
                print(f"   - Paciente: {len(pac_response.data) if pac_response.data else 0}")
            except Exception as e:
                print(f"   - Error paciente: {e}")

        print("\nLIMPIEZA COMPLETADA")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(limpiar_datos_directamente())