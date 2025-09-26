"""
Crear 5 Odontólogos Adicionales - Version 2
==========================================

Script corregido para crear odontólogos sin caracteres especiales
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

# Nuevos odontólogos con documentos únicos
NUEVOS_ODONTOLOGOS = [
    {
        "primer_nombre": "Dr. Carlos",
        "segundo_nombre": "Alberto",
        "primer_apellido": "Rodriguez",
        "segundo_apellido": "Mendez",
        "numero_documento": "11111111",
        "especialidad": "Odontología General",
        "numero_licencia": "ODG-11111",
        "celular": "+58-414-1111111",
        "salario": 800.00
    },
    {
        "primer_nombre": "Dra. María",
        "segundo_nombre": "Elena",
        "primer_apellido": "González",
        "segundo_apellido": "Torres",
        "numero_documento": "22222222",
        "especialidad": "Ortodoncia",
        "numero_licencia": "ORT-22222",
        "celular": "+58-424-2222222",
        "salario": 950.00
    },
    {
        "primer_nombre": "Dr. Pedro",
        "segundo_nombre": "José",
        "primer_apellido": "Santos",
        "segundo_apellido": "Ramos",
        "numero_documento": "33333333",
        "especialidad": "Periodoncia",
        "numero_licencia": "PER-33333",
        "celular": "+58-412-3333333",
        "salario": 900.00
    },
    {
        "primer_nombre": "Dra. Sofia",
        "segundo_nombre": "Isabel",
        "primer_apellido": "Herrera",
        "segundo_apellido": "Castro",
        "numero_documento": "44444444",
        "especialidad": "Endodoncia",
        "numero_licencia": "END-44444",
        "celular": "+58-416-4444444",
        "salario": 900.00
    },
    {
        "primer_nombre": "Dr. Ricardo",
        "segundo_nombre": "Manuel",
        "primer_apellido": "Vargas",
        "segundo_apellido": "Luna",
        "numero_documento": "55555555",
        "especialidad": "Cirugía Oral",
        "numero_licencia": "COR-55555",
        "celular": "+58-426-5555555",
        "salario": 1000.00
    }
]

async def crear_odontologos():
    log_progreso("INICIANDO CREACIÓN DE 5 ODONTÓLOGOS ADICIONALES")
    log_progreso("=" * 55)

    try:
        # Obtener el próximo orden de preferencia
        orden_result = supabase.table("personal").select("orden_preferencia").eq("tipo_personal", "Odontólogo").order("orden_preferencia", desc=True).limit(1).execute()

        proximo_orden = 3  # Empezar desde 3 (ya hay 2 odontólogos)
        if orden_result.data:
            proximo_orden = (orden_result.data[0]["orden_preferencia"] or 0) + 1

        odontologos_creados = []

        for i, odontologo_data in enumerate(NUEVOS_ODONTOLOGOS, 1):
            try:
                log_progreso(f"Creando odontologo {i}/5: {odontologo_data['primer_nombre']} {odontologo_data['primer_apellido']}")

                personal_data = {
                    "id": str(uuid.uuid4()),
                    "usuario_id": None,
                    "primer_nombre": odontologo_data["primer_nombre"],
                    "segundo_nombre": odontologo_data["segundo_nombre"],
                    "primer_apellido": odontologo_data["primer_apellido"],
                    "segundo_apellido": odontologo_data["segundo_apellido"],
                    "tipo_documento": "CI",
                    "numero_documento": odontologo_data["numero_documento"],
                    "tipo_personal": "Odontólogo",
                    "especialidad": odontologo_data["especialidad"],
                    "numero_licencia": odontologo_data["numero_licencia"],
                    "celular": odontologo_data["celular"],
                    "salario": odontologo_data["salario"],
                    "fecha_contratacion": datetime.now().date().isoformat(),
                    "estado_laboral": "activo",
                    "acepta_pacientes_nuevos": True,
                    "orden_preferencia": proximo_orden + i - 1,
                    "observaciones": f"Especialista en {odontologo_data['especialidad']}"
                }

                result = supabase.table("personal").insert(personal_data).execute()

                if result.data:
                    personal_creado = result.data[0]
                    odontologos_creados.append({
                        "id": personal_creado["id"],
                        "nombre": f"{personal_data['primer_nombre']} {personal_data['primer_apellido']}",
                        "especialidad": personal_data["especialidad"],
                        "documento": personal_data["numero_documento"]
                    })

                    log_progreso(f"   OK: {personal_data['primer_nombre']} {personal_data['primer_apellido']} - {personal_data['especialidad']}")

            except Exception as e:
                log_progreso(f"   ERROR creando odontologo {i}: {str(e)}", "ERROR")
                continue

        log_progreso("=" * 55)
        log_progreso(f"SUCCESS: Odontologos creados: {len(odontologos_creados)}/5")

        if odontologos_creados:
            log_progreso("RESUMEN DE ODONTOLOGOS CREADOS:")
            for odon in odontologos_creados:
                log_progreso(f"   • {odon['nombre']} - {odon['especialidad']} - Doc: {odon['documento']}")

        return odontologos_creados

    except Exception as e:
        log_progreso(f"ERROR en función principal: {str(e)}", "ERROR")
        return []

async def verificar_total():
    try:
        result = supabase.table("personal").select("primer_nombre, primer_apellido, especialidad, numero_documento").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").execute()

        log_progreso("=" * 55)
        log_progreso(f"VERIFICACIÓN FINAL - TOTAL ODONTÓLOGOS: {len(result.data)}")
        log_progreso("LISTA COMPLETA DE ODONTÓLOGOS ACTIVOS:")

        for i, odon in enumerate(result.data, 1):
            log_progreso(f"   {i}. {odon['primer_nombre']} {odon['primer_apellido']} - {odon['especialidad']} - Doc: {odon['numero_documento']}")

        return result.data

    except Exception as e:
        log_progreso(f"ERROR verificando total: {str(e)}", "ERROR")
        return []

async def main():
    try:
        odontologos_nuevos = await crear_odontologos()
        total_odontologos = await verificar_total()

        log_progreso("=" * 55)
        log_progreso("PROCESO COMPLETADO")
        log_progreso(f"   • Odontologos nuevos agregados: {len(odontologos_nuevos)}")
        log_progreso(f"   • Total odontologos activos: {len(total_odontologos)}")
        log_progreso("=" * 55)

    except Exception as e:
        log_progreso(f"ERROR en main: {str(e)}", "ERROR")

if __name__ == "__main__":
    asyncio.run(main())