#!/usr/bin/env python3
"""
PRUEBA DIRECTA DE BASE DE DATOS
Verifica directamente la base de datos sin usar los servicios
"""

import asyncio
import sys
import os
from datetime import datetime
import uuid

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dental_system.supabase.client import get_client

async def test_crear_paciente_directo():
    """Crear paciente directamente en la base de datos y verificar resultado"""

    print("PRUEBA DIRECTA - CREACION DE PACIENTE")
    print("=" * 50)

    supabase = get_client()

    # Datos de paciente de prueba
    paciente_id = str(uuid.uuid4())
    numero_documento = f"{datetime.now().strftime('%m%d%H%M%S')}"  # Solo numeros

    paciente_data = {
        "id": paciente_id,
        "numero_documento": numero_documento,
        "primer_nombre": "Juan",
        "primer_apellido": "Perez",
        "tipo_documento": "CI",
        "genero": "masculino",
        "fecha_nacimiento": "1985-05-15",
        "celular_1": "04123456789",
        "email": f"test.{datetime.now().strftime('%H%M%S')}@email.com",
        "direccion": "Caracas, Venezuela"
    }

    try:
        # 1. CREAR PACIENTE
        print("1. Creando paciente en BD...")
        response = supabase.table("pacientes").insert(paciente_data).execute()

        if response.data:
            paciente_creado = response.data[0]
            numero_historia = paciente_creado.get('numero_historia')
            print(f"EXITO: Paciente creado con HC: {numero_historia}")

            # 2. VERIFICAR SI EXISTE TABLA ODONTOGRAMA
            print("\n2. Verificando estructura de BD...")
            await verificar_tablas_bd()

            # 3. MOSTRAR RESULTADO
            print(f"\nRESUMEN:")
            print(f"ID Paciente: {paciente_id}")
            print(f"HC: {numero_historia}")
            print(f"Documento: {numero_documento}")

        else:
            print("ERROR: No se pudo crear paciente")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

async def verificar_tablas_bd():
    """Verificar que las tablas existen"""
    supabase = get_client()

    tablas_a_verificar = [
        "pacientes",
        "odontograma",
        "historial_medico",
        "auditoria",
        "condiciones_diente"
    ]

    for tabla in tablas_a_verificar:
        try:
            response = supabase.table(tabla).select("*").limit(1).execute()
            print(f"EXITO: Tabla '{tabla}' existe y es accesible")
        except Exception as e:
            print(f"ERROR: Tabla '{tabla}' - {e}")

if __name__ == "__main__":
    print("PRUEBA DIRECTA DE BASE DE DATOS\n")
    asyncio.run(test_crear_paciente_directo())