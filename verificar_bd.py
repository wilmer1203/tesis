"""Script para verificar estructura actual de la BD"""
import asyncio
import sys
import os

# Agregar path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dental_system'))

from supabase.tablas import SupabaseTablas

async def verificar_estructura():
    supabase = SupabaseTablas()

    # Verificar usuarios/odontólogos
    usuarios = await supabase.usuarios.get_all()
    print('=== USUARIOS/ODONTÓLOGOS ===')
    odontologos = []
    for u in usuarios:
        print(f'{u.get("rol")}: {u.get("nombre")} (ID: {u.get("id")})')
        if u.get("rol") == "odontologo":
            odontologos.append(u)

    # Verificar pacientes
    pacientes = await supabase.pacientes.get_all()
    print(f'\n=== PACIENTES: {len(pacientes)} ===')
    if pacientes:
        for p in pacientes[:3]:
            print(f'- {p.get("numero_historia")}: {p.get("primer_nombre")} {p.get("primer_apellido")}')

    # Verificar servicios
    servicios = await supabase.servicios.get_all()
    print(f'\n=== SERVICIOS: {len(servicios)} ===')
    for s in servicios[:5]:
        alcance = s.get("alcance_servicio", "N/A")
        print(f'{s.get("codigo")}: {s.get("nombre")} - ${s.get("precio_base")} (Alcance: {alcance})')

    # Verificar consultas existentes
    consultas = await supabase.consultas.get_all()
    print(f'\n=== CONSULTAS EXISTENTES: {len(consultas)} ===')
    for c in consultas[:5]:
        print(f'Consulta ID {c.get("id")[:8]}...: Estado {c.get("estado")}')

    return {
        'odontologos': odontologos,
        'pacientes': pacientes,
        'servicios': servicios,
        'consultas': consultas
    }

if __name__ == "__main__":
    datos = asyncio.run(verificar_estructura())
