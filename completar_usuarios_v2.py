"""
Completar Usuarios para Odontólogos - V2
========================================

Script corregido con estructura real de tabla usuarios
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

# ID del rol odontólogo obtenido de la BD
ROL_ODONTOLOGO_ID = "023f29cb-7640-486d-8b73-43e2d71c6ba2"

def log_progreso(mensaje: str, nivel: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {nivel}: {mensaje}")

# Emails para los odontólogos
USUARIOS_ODONTOLOGOS = {
    "67890123": "sofia.herrera1@clinica.com",  # Dra. Sofia Herrera (previa)
    "11111111": "carlos.rodriguez@clinica.com",  # Dr. Carlos Rodriguez
    "22222222": "maria.gonzalez@clinica.com",    # Dra. María González
    "33333333": "pedro.santos@clinica.com",      # Dr. Pedro Santos
    "44444444": "sofia.herrera2@clinica.com",    # Dra. Sofia Herrera
    "55555555": "ricardo.vargas@clinica.com"     # Dr. Ricardo Vargas
}

async def crear_usuarios_odontologos():
    log_progreso("INICIANDO CREACIÓN DE USUARIOS PARA ODONTÓLOGOS")
    log_progreso("=" * 60)

    try:
        # Obtener odontólogos sin usuario
        odontologos_sin_usuario = supabase.table("personal").select("*").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").is_("usuario_id", "null").execute()

        log_progreso(f"Odontólogos sin usuario: {len(odontologos_sin_usuario.data)}")

        usuarios_creados = []

        for i, odontologo in enumerate(odontologos_sin_usuario.data, 1):
            try:
                documento = odontologo["numero_documento"]
                nombre_completo = f"{odontologo['primer_nombre']} {odontologo['primer_apellido']}"

                if documento not in USUARIOS_ODONTOLOGOS:
                    log_progreso(f"   SKIP: No hay email para {nombre_completo} - Doc: {documento}", "WARN")
                    continue

                email = USUARIOS_ODONTOLOGOS[documento]

                log_progreso(f"Creando usuario {i}: {nombre_completo} - {email}")

                # Generar UUID para el usuario
                usuario_id = str(uuid.uuid4())

                # Datos para tabla usuarios (con estructura real)
                usuario_data = {
                    "id": usuario_id,
                    "email": email,
                    "rol_id": ROL_ODONTOLOGO_ID,  # Rol odontólogo
                    "activo": True,
                    "fecha_creacion": datetime.now().isoformat(),
                    "ultimo_acceso": None,
                    "configuraciones": {
                        "tema": "oscuro",
                        "notificaciones": True,
                        "idioma": "es"
                    },
                    "auth_user_id": None,  # Sin Auth por limitaciones
                    "metadata": {
                        "nombre_completo": nombre_completo,
                        "especialidad": odontologo.get("especialidad", "Odontología General"),
                        "numero_licencia": odontologo.get("numero_licencia", ""),
                        "creado_automaticamente": True,
                        "fecha_contratacion": odontologo.get("fecha_contratacion")
                    }
                }

                # Insertar usuario
                result_usuario = supabase.table("usuarios").insert(usuario_data).execute()

                if result_usuario.data:
                    log_progreso(f"   OK Usuario creado: {email}")

                    # Vincular con personal
                    update_result = supabase.table("personal").update({
                        "usuario_id": usuario_id
                    }).eq("id", odontologo["id"]).execute()

                    if update_result.data:
                        log_progreso(f"   OK Personal vinculado con usuario")

                        usuarios_creados.append({
                            "usuario_id": usuario_id,
                            "personal_id": odontologo["id"],
                            "email": email,
                            "nombre": nombre_completo,
                            "documento": documento,
                            "especialidad": odontologo.get("especialidad", "N/A")
                        })
                    else:
                        log_progreso(f"   ERROR: No se pudo vincular personal", "ERROR")
                else:
                    log_progreso(f"   ERROR: No se pudo crear usuario", "ERROR")

            except Exception as e:
                log_progreso(f"   ERROR procesando {i}: {str(e)}", "ERROR")
                continue

        log_progreso("=" * 60)
        log_progreso(f"SUCCESS: Usuarios creados: {len(usuarios_creados)}")

        if usuarios_creados:
            log_progreso("USUARIOS CREADOS:")
            for usuario in usuarios_creados:
                log_progreso(f"   • {usuario['nombre']} - {usuario['email']}")
                log_progreso(f"     Especialidad: {usuario['especialidad']} - Doc: {usuario['documento']}")

        return usuarios_creados

    except Exception as e:
        log_progreso(f"ERROR: {str(e)}", "ERROR")
        return []

async def verificar_estado_final():
    """Verifica el estado final de usuarios y personal"""
    try:
        log_progreso("=" * 60)
        log_progreso("VERIFICACIÓN FINAL")

        # Contar odontólogos con y sin usuario
        con_usuario = supabase.table("personal").select("primer_nombre, primer_apellido, usuario_id").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").not_.is_("usuario_id", "null").execute()

        sin_usuario = supabase.table("personal").select("primer_nombre, primer_apellido").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").is_("usuario_id", "null").execute()

        # Usuarios odontólogos en BD
        usuarios_odontologos = supabase.table("usuarios").select("email, metadata").eq("rol_id", ROL_ODONTOLOGO_ID).execute()

        log_progreso(f"Odontólogos CON usuario: {len(con_usuario.data)}")
        log_progreso(f"Odontólogos SIN usuario: {len(sin_usuario.data)}")
        log_progreso(f"Total usuarios odontólogos: {len(usuarios_odontologos.data)}")

        if con_usuario.data:
            log_progreso("\nODONTÓLOGOS CON USUARIO:")
            for i, odon in enumerate(con_usuario.data, 1):
                log_progreso(f"   {i}. {odon['primer_nombre']} {odon['primer_apellido']} - ID: {odon['usuario_id'][:8]}...")

        if sin_usuario.data:
            log_progreso("\nODONTÓLOGOS SIN USUARIO:")
            for i, odon in enumerate(sin_usuario.data, 1):
                log_progreso(f"   {i}. {odon['primer_nombre']} {odon['primer_apellido']}")

        if usuarios_odontologos.data:
            log_progreso("\nUSUARIOS ODONTÓLOGOS EN BD:")
            for i, usuario in enumerate(usuarios_odontologos.data, 1):
                nombre = usuario.get("metadata", {}).get("nombre_completo", "N/A")
                especialidad = usuario.get("metadata", {}).get("especialidad", "N/A")
                log_progreso(f"   {i}. {nombre} - {usuario['email']} - {especialidad}")

        return len(con_usuario.data), len(sin_usuario.data)

    except Exception as e:
        log_progreso(f"ERROR en verificación: {str(e)}", "ERROR")
        return 0, 0

async def main():
    try:
        usuarios_creados = await crear_usuarios_odontologos()
        con_usuario, sin_usuario = await verificar_estado_final()

        log_progreso("=" * 60)
        log_progreso("PROCESO COMPLETADO")
        log_progreso(f"   • Usuarios nuevos: {len(usuarios_creados)}")
        log_progreso(f"   • Total con usuario: {con_usuario}")
        log_progreso(f"   • Total sin usuario: {sin_usuario}")

        if sin_usuario == 0:
            log_progreso("SUCCESS: Todos los odontólogos tienen usuarios!")
        else:
            log_progreso(f"PENDIENTE: {sin_usuario} odontólogos sin usuario", "WARN")

        log_progreso("=" * 60)

    except Exception as e:
        log_progreso(f"ERROR en main: {str(e)}", "ERROR")

if __name__ == "__main__":
    asyncio.run(main())