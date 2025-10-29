# -*- coding: utf-8 -*-
"""
Ver logs de PostgreSQL para diagnosticar errores
"""

print("Para ver los logs de PostgreSQL en Supabase local:")
print("")
print("OPCION 1: Logs en tiempo real")
print("  docker logs -f supabase_db_tesis-main --tail=50")
print("")
print("OPCION 2: Logs en Supabase Studio")
print("  1. Abre http://localhost:54323")
print("  2. Ve a 'Logs' en el menu izquierdo")
print("  3. Selecciona 'Postgres Logs'")
print("  4. Busca mensajes con 'WARNING' o 'ERROR'")
print("")
print("OPCION 3: Ejecutar query manual para probar")
print("  1. Abre http://localhost:54323")
print("  2. Ve a SQL Editor")
print("  3. Ejecuta la siguiente query de prueba:")
print("")
print("""
-- Test manual de la función
DO $$
DECLARE
    resultado jsonb;
    test_data jsonb;
BEGIN
    -- Crear datos de prueba
    test_data := '[
        {
            "paciente_id": "123e4567-e89b-12d3-a456-426614174000",
            "diente_numero": 11,
            "superficie": "oclusal",
            "tipo_condicion": "caries",
            "material_utilizado": "Resina",
            "descripcion": "Test",
            "intervencion_id": "123e4567-e89b-12d3-a456-426614174001",
            "registrado_por": "123e4567-e89b-12d3-a456-426614174002"
        }
    ]'::jsonb;

    -- Llamar función
    SELECT actualizar_condiciones_batch(test_data) INTO resultado;

    RAISE NOTICE 'Resultado: %', resultado;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'ERROR: %', SQLERRM;
END $$;
""")
print("")
print("Si ves un error específico, compártelo para solucionarlo.")
