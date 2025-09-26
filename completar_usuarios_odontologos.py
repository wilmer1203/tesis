"""
Completar Usuarios para Odontólogos
==================================

Script para crear usuarios Auth para los odontólogos que solo están en personal
y vincularlos correctamente.

Autor: Sistema Dental - Wilmer Aguirre
"""

import os
import sys
import asyncio
import uuid
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def log_progreso(mensaje: str, nivel: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {nivel}: {mensaje}")

# Datos de usuarios para los odontólogos
USUARIOS_ODONTOLOGOS = {
    "11111111": {  # Dr. Carlos Rodriguez
        "email": "carlos.rodriguez@clinicadental.com",
        "password": "ClínicaDental2024!",
        "nombre_completo": "Dr. Carlos Rodriguez"
    },
    "22222222": {  # Dra. María González
        "email": "maria.gonzalez@clinicadental.com",
        "password": "ClínicaDental2024!",
        "nombre_completo": "Dra. María González"
    },
    "33333333": {  # Dr. Pedro Santos
        "email": "pedro.santos@clinicadental.com",
        "password": "ClínicaDental2024!",
        "nombre_completo": "Dr. Pedro Santos"
    },
    "44444444": {  # Dra. Sofia Herrera
        "email": "sofia.herrera@clinicadental.com",
        "password": "ClínicaDental2024!",
        "nombre_completo": "Dra. Sofia Herrera"
    },
    "55555555": {  # Dr. Ricardo Vargas
        "email": "ricardo.vargas@clinicadental.com",
        "password": "ClínicaDental2024!",
        "nombre_completo": "Dr. Ricardo Vargas"
    }
}

async def obtener_odontologos_sin_usuario():
    """Obtiene odontólogos que no tienen usuario_id vinculado"""
    try:
        result = supabase.table("personal").select("*").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").is_("usuario_id", "null").execute()

        log_progreso(f"Odontólogos sin usuario encontrados: {len(result.data)}")

        for odon in result.data:
            log_progreso(f"   • {odon['primer_nombre']} {odon['primer_apellido']} - Doc: {odon['numero_documento']}")

        return result.data

    except Exception as e:
        log_progreso(f"ERROR obteniendo odontólogos sin usuario: {str(e)}", "ERROR")
        return []

async def crear_usuarios_auth():
    """Crea usuarios Auth para los odontólogos y los vincula"""
    log_progreso("INICIANDO CREACIÓN DE USUARIOS PARA ODONTÓLOGOS")
    log_progreso("=" * 60)

    try:
        # Obtener odontólogos sin usuario
        odontologos_sin_usuario = await obtener_odontologos_sin_usuario()

        if not odontologos_sin_usuario:
            log_progreso("Todos los odontólogos ya tienen usuarios asignados")
            return []

        usuarios_creados = []

        for i, odontologo in enumerate(odontologos_sin_usuario, 1):
            try:
                documento = odontologo["numero_documento"]

                if documento not in USUARIOS_ODONTOLOGOS:
                    log_progreso(f"   SKIP: No hay datos de usuario para documento {documento}", "WARN")
                    continue

                usuario_data = USUARIOS_ODONTOLOGOS[documento]

                log_progreso(f"Procesando {i}/{len(odontologos_sin_usuario)}: {odontologo['primer_nombre']} {odontologo['primer_apellido']}")

                # OPCIÓN 1: Crear directamente en tabla usuarios (sin Auth admin)
                # Generar UUID para el usuario
                usuario_id = str(uuid.uuid4())

                # Datos para tabla usuarios
                usuario_db_data = {
                    "id": usuario_id,
                    "email": usuario_data["email"],
                    "nombre_completo": usuario_data["nombre_completo"],
                    "rol": "odontologo",
                    "activo": True,
                    "fecha_registro": datetime.now().isoformat(),
                    "ultimo_acceso": None,
                    "configuracion": {
                        "tema": "oscuro",
                        "notificaciones": True,
                        "idioma": "es"
                    },
                    "observaciones": f"Usuario creado para odontólogo: {usuario_data['nombre_completo']}"
                }

                # Insertar en tabla usuarios
                result_usuario = supabase.table("usuarios").insert(usuario_db_data).execute()

                if result_usuario.data:
                    log_progreso(f"   OK Usuario DB creado: {usuario_data['email']}")

                    # Actualizar tabla personal con usuario_id
                    update_result = supabase.table("personal").update({
                        "usuario_id": usuario_id
                    }).eq("id", odontologo["id"]).execute()

                    if update_result.data:
                        log_progreso(f"   OK Personal vinculado con usuario: {usuario_id}")

                        usuarios_creados.append({
                            "usuario_id": usuario_id,
                            "personal_id": odontologo["id"],
                            "email": usuario_data["email"],
                            "nombre": usuario_data["nombre_completo"],
                            "documento": documento
                        })
                    else:
                        log_progreso(f"   ERROR: No se pudo vincular personal con usuario", "ERROR")
                else:
                    log_progreso(f"   ERROR: No se pudo crear usuario en DB", "ERROR")

            except Exception as e:
                log_progreso(f"   ERROR procesando odontólogo {i}: {str(e)}", "ERROR")
                continue

        log_progreso("=" * 60)
        log_progreso(f"SUCCESS: Usuarios creados y vinculados: {len(usuarios_creados)}")

        if usuarios_creados:
            log_progreso("RESUMEN DE USUARIOS CREADOS:")
            for usuario in usuarios_creados:
                log_progreso(f"   • {usuario['nombre']} - {usuario['email']} - Doc: {usuario['documento']}")

        return usuarios_creados

    except Exception as e:
        log_progreso(f"ERROR en creación de usuarios: {str(e)}", "ERROR")
        return []

async def verificar_vinculacion_completa():
    """Verifica que todos los odontólogos tengan usuarios vinculados"""
    try:
        # Odontólogos con usuario
        con_usuario = supabase.table("personal").select("primer_nombre, primer_apellido, usuario_id").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").not_.is_("usuario_id", "null").execute()

        # Odontólogos sin usuario
        sin_usuario = supabase.table("personal").select("primer_nombre, primer_apellido").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").is_("usuario_id", "null").execute()

        log_progreso("=" * 60)
        log_progreso("VERIFICACIÓN DE VINCULACIÓN USUARIO-PERSONAL")
        log_progreso(f"Odontólogos CON usuario: {len(con_usuario.data)}")
        log_progreso(f"Odontólogos SIN usuario: {len(sin_usuario.data)}")

        if con_usuario.data:
            log_progreso("\nODONTÓLOGOS CON USUARIO VINCULADO:")
            for i, odon in enumerate(con_usuario.data, 1):
                log_progreso(f"   {i}. {odon['primer_nombre']} {odon['primer_apellido']} - Usuario: {odon['usuario_id'][:8]}...")

        if sin_usuario.data:
            log_progreso("\nODONTÓLOGOS SIN USUARIO:")
            for i, odon in enumerate(sin_usuario.data, 1):
                log_progreso(f"   {i}. {odon['primer_nombre']} {odon['primer_apellido']}")

        return len(con_usuario.data), len(sin_usuario.data)

    except Exception as e:
        log_progreso(f"ERROR verificando vinculación: {str(e)}", "ERROR")
        return 0, 0

async def verificar_usuarios_en_bd():
    """Verifica usuarios creados en tabla usuarios"""
    try:
        usuarios_odontologos = supabase.table("usuarios").select("email, nombre_completo, rol, activo").eq("rol", "odontologo").execute()

        log_progreso("=" * 60)
        log_progreso(f"USUARIOS ODONTÓLOGOS EN BD: {len(usuarios_odontologos.data)}")

        for i, usuario in enumerate(usuarios_odontologos.data, 1):
            estado = "ACTIVO" if usuario["activo"] else "INACTIVO"
            log_progreso(f"   {i}. {usuario['nombre_completo']} - {usuario['email']} - {estado}")

        return usuarios_odontologos.data

    except Exception as e:
        log_progreso(f"ERROR verificando usuarios: {str(e)}", "ERROR")
        return []

async def main():
    """Función principal"""
    try:
        # Crear usuarios y vincular
        usuarios_creados = await crear_usuarios_auth()

        # Verificar vinculación
        con_usuario, sin_usuario = await verificar_vinculacion_completa()

        # Verificar usuarios en BD
        usuarios_bd = await verificar_usuarios_en_bd()

        log_progreso("=" * 60)
        log_progreso("PROCESO COMPLETADO")
        log_progreso(f"   • Nuevos usuarios creados: {len(usuarios_creados)}")
        log_progreso(f"   • Odontólogos con usuario: {con_usuario}")
        log_progreso(f"   • Odontólogos sin usuario: {sin_usuario}")
        log_progreso(f"   • Total usuarios odontólogos en BD: {len(usuarios_bd)}")
        log_progreso("=" * 60)

        if sin_usuario == 0:
            log_progreso("SUCCESS: Todos los odontólogos tienen usuarios vinculados")
        else:
            log_progreso("ADVERTENCIA: Algunos odontólogos aún no tienen usuarios", "WARN")

    except Exception as e:
        log_progreso(f"ERROR en main: {str(e)}", "ERROR")

if __name__ == "__main__":
    asyncio.run(main())