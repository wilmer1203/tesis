"""Script para verificar estructura actual de la BD usando SQL directo"""
import os
from supabase import create_client

# Configuración Supabase LOCAL
SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=== USUARIOS/ODONTÓLOGOS ===")
# Obtener usuarios con sus roles
usuarios = supabase.table("usuarios").select("id, email, rol_id").execute()
personal = supabase.table("personal").select("usuario_id, primer_nombre, primer_apellido, tipo_personal").execute()

# Crear map de usuario_id -> datos personales
personal_map = {p["usuario_id"]: p for p in personal.data}

odontologos = []
for u in usuarios.data:
    rol_id = u.get("rol_id", "")
    # Obtener nombre del rol
    if rol_id:
        rol_data = supabase.table("roles").select("nombre").eq("id", rol_id).execute()
        rol_nombre = rol_data.data[0]["nombre"] if rol_data.data else "desconocido"
    else:
        rol_nombre = "sin_rol"

    # Obtener nombre desde personal si existe
    persona_data = personal_map.get(u["id"])
    if persona_data:
        nombre = f"{persona_data['primer_nombre']} {persona_data['primer_apellido']}"
    else:
        nombre = u["email"].split("@")[0]

    print(f'{rol_nombre}: {nombre} (ID: {u["id"][:8]}...)')
    if rol_nombre == "odontologo":
        u["rol"] = rol_nombre
        u["nombre_completo"] = nombre
        odontologos.append(u)

print(f"\n=== PACIENTES ===")
pacientes = supabase.table("pacientes").select("id, numero_historia, primer_nombre, primer_apellido").execute()
print(f"Total: {len(pacientes.data)}")
for p in pacientes.data[:3]:
    print(f'- {p["numero_historia"]}: {p["primer_nombre"]} {p["primer_apellido"]} (ID: {p["id"][:8]}...)')

print(f"\n=== SERVICIOS ===")
servicios = supabase.table("servicios").select("id, codigo, nombre, precio_base_bs, precio_base_usd, alcance_servicio").execute()
print(f"Total: {len(servicios.data)}")
for s in servicios.data[:8]:
    alcance = s.get("alcance_servicio", "N/A")
    print(f'{s["codigo"]}: {s["nombre"]} - BS{s["precio_base_bs"]}/USD{s["precio_base_usd"]} (Alcance: {alcance})')

print(f"\n=== CONSULTAS EXISTENTES ===")
consultas = supabase.table("consultas").select("id, estado, fecha_creacion").execute()
print(f"Total: {len(consultas.data)}")
estados = {}
for c in consultas.data:
    estado = c.get("estado", "sin_estado")
    estados[estado] = estados.get(estado, 0) + 1
print(f"Por estado: {estados}")

print(f"\n=== IDs DE ODONTÓLOGOS (para script) ===")
for odon in odontologos:
    print(f"'{odon['id']}',  # {odon['nombre_completo']}")

print(f"\n=== IDs DE PACIENTES (primeros 10) ===")
for pac in pacientes.data[:10]:
    print(f"'{pac['id']}',  # {pac['numero_historia']}: {pac['primer_nombre']} {pac['primer_apellido']}")

print(f"\n=== IDs DE SERVICIOS (primeros 10) ===")
for serv in servicios.data[:10]:
    alcance = serv.get('alcance_servicio', 'N/A')
    print(f"'{serv['id']}': {{  # {serv['codigo']}: {serv['nombre']}")
    print(f"    'alcance': '{alcance}',")
    print(f"    'precio_bs': {serv['precio_base_bs']},")
    print(f"    'precio_usd': {serv['precio_base_usd']}")
    print(f"}},")
print("\n" + "="*60)
