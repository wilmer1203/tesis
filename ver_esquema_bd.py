"""Script para ver esquema de tablas"""
from supabase import create_client

SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Ver algunas filas de usuarios
print("=== MUESTRA DE USUARIOS ===")
usuarios_sample = supabase.table("usuarios").select("*").limit(2).execute()
if usuarios_sample.data:
    print(f"Campos disponibles: {list(usuarios_sample.data[0].keys())}")
    for u in usuarios_sample.data:
        print(f"\nUsuario: {u}")

print("\n=== MUESTRA DE PACIENTES ===")
pacientes_sample = supabase.table("pacientes").select("*").limit(1).execute()
if pacientes_sample.data:
    print(f"Campos disponibles: {list(pacientes_sample.data[0].keys())}")

print("\n=== MUESTRA DE SERVICIOS ===")
servicios_sample = supabase.table("servicios").select("*").limit(1).execute()
if servicios_sample.data:
    print(f"Campos disponibles: {list(servicios_sample.data[0].keys())}")

print("\n=== MUESTRA DE CONSULTAS ===")
consultas_sample = supabase.table("consultas").select("*").limit(1).execute()
if consultas_sample.data:
    print(f"Campos disponibles: {list(consultas_sample.data[0].keys())}")
