# -*- coding: utf-8 -*-
"""
Script para verificar que la función actualizar_condiciones_batch existe
"""
from dental_system.supabase.client import supabase_client

def verificar_funcion():
    """Verificar que la función SQL existe y funciona"""

    print("Verificando función actualizar_condiciones_batch...")

    client = supabase_client.get_client()

    # Intentar llamar la función con datos de prueba vacíos
    try:
        result = client.rpc('actualizar_condiciones_batch', {
            'actualizaciones': '[]'  # Array vacío como prueba
        }).execute()

        print("OK: Función actualizar_condiciones_batch existe y funciona")
        print(f"  Resultado de prueba: {result.data}")
        return True

    except Exception as e:
        error_msg = str(e).lower()

        if 'function' in error_msg and 'does not exist' in error_msg:
            print("ERROR: Función actualizar_condiciones_batch NO EXISTE")
            print("\nDEBES EJECUTAR MANUALMENTE:")
            print("  1. Abre Supabase Studio (http://localhost:54323)")
            print("  2. Ve a SQL Editor")
            print("  3. Ejecuta la migracion 20251019_fix_batch_transaccionalidad.sql")
            return False
        else:
            print(f"ERROR inesperado: {e}")
            return False

if __name__ == "__main__":
    resultado = verificar_funcion()
    if not resultado:
        print("\n***** FUNCION NO ENCONTRADA *****")
