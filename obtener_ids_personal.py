"""Script para obtener IDs correctos de personal (odontólogos)"""
from supabase import create_client

SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Obtener TODO el personal primero para ver qué hay
personal_all = supabase.table("personal").select("*").execute()
print(f"=== TODO EL PERSONAL ===")
print(f"Total registros: {len(personal_all.data)}")
if personal_all.data:
    print(f"Campos: {list(personal_all.data[0].keys())}\n")
    for p in personal_all.data[:5]:
        print(f"ID: {p['id'][:8]}... | Usuario: {p.get('usuario_id', 'N/A')[:8] if p.get('usuario_id') else 'N/A'}... | Tipo: {p.get('tipo_personal', 'N/A')}")
        print(f"  Nombre: {p.get('primer_nombre')} {p.get('primer_apellido')}")
        print()

# Obtener personal que es odontólogo (con mayúscula y tilde)
personal = supabase.table("personal").select("id, usuario_id, primer_nombre, primer_apellido, tipo_personal").eq("tipo_personal", "Odontólogo").execute()

print(f"\n=== IDs DE PERSONAL (ODONTOLOGOS) ===")
print(f"Total: {len(personal.data)}\n")

for p in personal.data:
    print(f"'{p['id']}',  # {p['primer_nombre']} {p['primer_apellido']}")

# También obtener IDs de pacientes para verificar
pacientes = supabase.table("pacientes").select("id, numero_historia, primer_nombre, primer_apellido").limit(15).execute()

print(f"\n=== IDS DE PACIENTES (primeros 15) ===")
for pac in pacientes.data:
    print(f"'{pac['id']}',  # {pac['numero_historia']}: {pac['primer_nombre']} {pac['primer_apellido']}")

# Obtener ID de admin
usuarios = supabase.table("usuarios").select("id, email").execute()
admin = [u for u in usuarios.data if "admin" in u["email"]][0]
print(f"\n=== ADMIN ID ===")
print(f"'{admin['id']}'  # {admin['email']}")
