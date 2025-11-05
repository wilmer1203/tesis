import subprocess
import json

def ejecutar_query(query):
    cmd = [
        'docker', 'exec', 'supabase_db_tesis-main',
        'psql', '-U', 'postgres', '-d', 'postgres',
        '-t', '-A', '-F', '|', '-c', query
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

# Extraer estructura básica de cada tabla
tablas = [
    'usuarios', 'roles', 'personal', 'servicios', 'pacientes', 
    'historial_medico', 'imagenes_clinicas', 'consultas', 
    'intervenciones', 'intervenciones_servicios', 'condiciones_diente', 
    'dientes', 'pagos', 'pagos_secuencias'
]

print("# 📊 RESUMEN EJECUTIVO - BASE DE DATOS SISTEMA DENTAL")
print("=" * 80)
print()

for tabla in tablas:
    # Columnas
    query_cols = f"""
    SELECT 
        column_name, 
        data_type,
        CASE WHEN is_nullable = 'NO' THEN 'NOT NULL' ELSE 'NULL' END as nullable,
        column_default
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = '{tabla}'
    ORDER BY ordinal_position;
    """
    
    # Foreign Keys
    query_fks = f"""
    SELECT 
        kcu.column_name,
        ccu.table_name AS foreign_table,
        ccu.column_name AS foreign_column
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu 
        ON tc.constraint_name = ccu.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY' 
        AND tc.table_schema = 'public'
        AND tc.table_name = '{tabla}'
    ORDER BY kcu.column_name;
    """
    
    # Indexes únicos
    query_uniques = f"""
    SELECT kcu.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
    WHERE tc.constraint_type = 'UNIQUE' 
        AND tc.table_schema = 'public'
        AND tc.table_name = '{tabla}'
    ORDER BY kcu.column_name;
    """
    
    print(f"## 📋 TABLA: `{tabla}`")
    print()
    
    # Columnas
    cols = ejecutar_query(query_cols)
    if cols:
        print("**Columnas:**")
        for line in cols.split('\n'):
            if line.strip():
                parts = line.split('|')
                col_name = parts[0]
                col_type = parts[1]
                nullable = parts[2]
                default = parts[3] if len(parts) > 3 and parts[3] else ''
                print(f"  - `{col_name}` ({col_type}) {nullable} {default}")
        print()
    
    # Foreign Keys
    fks = ejecutar_query(query_fks)
    if fks:
        print("**Relaciones (FK):**")
        for line in fks.split('\n'):
            if line.strip():
                parts = line.split('|')
                print(f"  - `{parts[0]}` → `{parts[1]}.{parts[2]}`")
        print()
    
    # Unique constraints
    uniques = ejecutar_query(query_uniques)
    if uniques:
        print("**Campos únicos:**")
        for line in uniques.split('\n'):
            if line.strip():
                print(f"  - `{line}`")
        print()
    
    print("-" * 80)
    print()

# Triggers
print("## 🔄 TRIGGERS")
print()
query_triggers = """
SELECT 
    trigger_name,
    event_object_table,
    action_timing || ' ' || event_manipulation as evento
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;
"""
triggers = ejecutar_query(query_triggers)
if triggers:
    for line in triggers.split('\n'):
        if line.strip():
            parts = line.split('|')
            print(f"  - **{parts[0]}** en `{parts[1]}` ({parts[2]})")
print()

# Funciones
print("## ⚙️ FUNCIONES")
print()
query_funciones = "SELECT proname FROM pg_proc WHERE pronamespace = 'public'::regnamespace ORDER BY proname;"
funciones = ejecutar_query(query_funciones)
if funciones:
    for line in funciones.split('\n'):
        if line.strip():
            print(f"  - `{line}()`")

