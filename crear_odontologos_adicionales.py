"""
Crear 5 Odontólogos Adicionales
==============================

Script para crear 5 odontólogos adicionales con:
- Documentos únicos (evitando duplicados)
- Especialidades variadas
- Solo registro en tabla personal (sin Auth por limitaciones)

Autor: Sistema Dental - Wilmer Aguirre
"""

import os
import sys
import asyncio
import random
import uuid
from datetime import datetime, timedelta

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
        "numero_documento": "12345678",  # Único
        "especialidad": "Odontología General",
        "numero_licencia": "ODG-12345",
        "celular": "+58-414-1234567",
        "salario": 800.00,
        "email_referencia": "carlos.rodriguez@clinica.com"
    },
    {
        "primer_nombre": "Dra. María",
        "segundo_nombre": "Elena",
        "primer_apellido": "González",
        "segundo_apellido": "Torres",
        "numero_documento": "23456789",  # Único
        "especialidad": "Ortodoncia",
        "numero_licencia": "ORT-23456",
        "celular": "+58-424-2345678",
        "salario": 950.00,
        "email_referencia": "maria.gonzalez@clinica.com"
    },
    {
        "primer_nombre": "Dr. Pedro",
        "segundo_nombre": "José",
        "primer_apellido": "Santos",
        "segundo_apellido": "Ramos",
        "numero_documento": "56789012",  # Único
        "especialidad": "Periodoncia",
        "numero_licencia": "PER-56789",
        "celular": "+58-412-3456789",
        "salario": 900.00,
        "email_referencia": "pedro.santos@clinica.com"
    },
    {
        "primer_nombre": "Dra. Sofia",
        "segundo_nombre": "Isabel",
        "primer_apellido": "Herrera",
        "segundo_apellido": "Castro",
        "numero_documento": "67890123",  # Único
        "especialidad": "Endodoncia",
        "numero_licencia": "END-67890",
        "celular": "+58-416-4567890",
        "salario": 900.00,
        "email_referencia": "sofia.herrera@clinica.com"
    },
    {
        "primer_nombre": "Dr. Ricardo",
        "segundo_nombre": "Manuel",
        "primer_apellido": "Vargas",
        "segundo_apellido": "Luna",
        "numero_documento": "78901234",  # Único
        "especialidad": "Cirugía Oral",
        "numero_licencia": "COR-78901",
        "celular": "+58-426-5678901",
        "salario": 1000.00,
        "email_referencia": "ricardo.vargas@clinica.com"
    }
]

async def verificar_documentos_existentes():
    """Verifica que no existan documentos duplicados"""
    try:
        documentos_nuevos = [odon["numero_documento"] for odon in NUEVOS_ODONTOLOGOS]

        result = supabase.table("personal").select("numero_documento").in_("numero_documento", documentos_nuevos).execute()

        if result.data:
            documentos_existentes = [d["numero_documento"] for d in result.data]
            log_progreso(f"ADVERTENCIA: Documentos que ya existen: {documentos_existentes}", "WARN")
            return documentos_existentes

        log_progreso("OK: Todos los documentos son únicos")
        return []

    except Exception as e:
        log_progreso(f"ERROR verificando documentos: {str(e)}", "ERROR")
        return []

async def crear_odontologos_adicionales():
    """Crea 5 odontólogos adicionales en la tabla personal"""
    log_progreso("INICIANDO CREACIÓN DE 5 ODONTÓLOGOS ADICIONALES")
    log_progreso("=" * 55)

    try:
        # Verificar documentos existentes
        documentos_existentes = await verificar_documentos_existentes()

        # Filtrar odontólogos que no tengan documentos duplicados
        odontologos_a_crear = [
            odon for odon in NUEVOS_ODONTOLOGOS
            if odon["numero_documento"] not in documentos_existentes
        ]

        if not odontologos_a_crear:
            log_progreso("ADVERTENCIA: Todos los odontólogos ya existen", "WARN")
            return []

        log_progreso(f"Odontólogos a crear: {len(odontologos_a_crear)}")

        # Obtener el próximo orden de preferencia
        orden_result = supabase.table("personal").select("orden_preferencia").eq("tipo_personal", "Odontólogo").order("orden_preferencia", desc=True).limit(1).execute()

        proximo_orden = 1
        if orden_result.data:
            proximo_orden = (orden_result.data[0]["orden_preferencia"] or 0) + 1

        odontologos_creados = []

        for i, odontologo_data in enumerate(odontologos_a_crear, 1):
            try:
                log_progreso(f"Creando odontólogo {i}/{len(odontologos_a_crear)}: {odontologo_data['primer_nombre']} {odontologo_data['primer_apellido']}")

                # Preparar datos para inserción
                personal_data = {
                    "id": str(uuid.uuid4()),
                    "usuario_id": None,  # Sin usuario Auth por limitaciones
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
                    "observaciones": f"Odontólogo especialista en {odontologo_data['especialidad']} - Contacto: {odontologo_data['email_referencia']}"
                }

                # Insertar en tabla personal
                result = supabase.table("personal").insert(personal_data).execute()

                if result.data:
                    personal_creado = result.data[0]
                    odontologos_creados.append({
                        "id": personal_creado["id"],
                        "nombre": f"{personal_data['primer_nombre']} {personal_data['primer_apellido']}",
                        "especialidad": personal_data["especialidad"],
                        "documento": personal_data["numero_documento"],
                        "celular": personal_data["celular"]
                    })

                    log_progreso(f"   OK: {personal_data['primer_nombre']} {personal_data['primer_apellido']} - {personal_data['especialidad']}")
                else:
                    log_progreso(f"   ERROR: No se recibieron datos de inserción", "ERROR")

            except Exception as e:
                log_progreso(f"   ERROR creando odontólogo {i}: {str(e)}", "ERROR")
                continue

        log_progreso("=" * 55)
        log_progreso(f"SUCCESS: Odontólogos creados exitosamente: {len(odontologos_creados)}/5")

        # Mostrar resumen
        if odontologos_creados:
            log_progreso("RESUMEN DE ODONTÓLOGOS CREADOS:")
            for odon in odontologos_creados:
                log_progreso(f"   • {odon['nombre']} - {odon['especialidad']} - Doc: {odon['documento']}")

        return odontologos_creados

    except Exception as e:
        log_progreso(f"ERROR en función principal: {str(e)}", "ERROR")
        return []

async def verificar_total_odontologos():
    """Verifica el total final de odontólogos"""
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
    """Función principal"""
    try:
        # Crear odontólogos adicionales
        odontologos_nuevos = await crear_odontologos_adicionales()

        # Verificar totales finales
        total_odontologos = await verificar_total_odontologos()

        log_progreso("=" * 55)
        log_progreso("PROCESO COMPLETADO")
        log_progreso(f"   • Odontólogos nuevos agregados: {len(odontologos_nuevos)}")
        log_progreso(f"   • Total odontólogos activos: {len(total_odontologos)}")
        log_progreso("=" * 55)

    except Exception as e:
        log_progreso(f"ERROR en main: {str(e)}", "ERROR")

if __name__ == "__main__":
    asyncio.run(main())