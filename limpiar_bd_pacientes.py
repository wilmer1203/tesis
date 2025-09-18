#!/usr/bin/env python3
"""
SCRIPT PARA LIMPIAR BASE DE DATOS DE PACIENTES
Elimina todos los datos relacionados con pacientes de forma segura
"""

import asyncio
import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dental_system.supabase.client import get_client

async def limpiar_datos_pacientes():
    """Eliminar todos los datos de pacientes y relacionados"""

    print("LIMPIEZA DE BASE DE DATOS - PACIENTES")
    print("=" * 50)

    supabase = get_client()

    # Confirmar antes de proceder
    respuesta = input("ATENCION: Estas seguro de eliminar TODOS los datos de pacientes? (SI/no): ")
    if respuesta.upper() != 'SI':
        print("Operacion cancelada")
        return

    try:
        # Orden de eliminación (respetando foreign keys)
        tablas_limpiar = [
            ("condiciones_diente", "Condiciones de dientes"),
            ("historial_medico", "Historial médico"),
            ("odontograma", "Odontogramas"),
            ("intervenciones_servicios", "Servicios de intervenciones"),
            ("intervenciones", "Intervenciones"),
            ("cola_atencion", "Cola de atención"),
            ("pagos", "Pagos"),
            ("consultas", "Consultas"),
            ("auditoria", "Auditoría (solo pacientes)"),
            ("pacientes", "Pacientes")
        ]

        total_eliminados = 0

        for tabla, descripcion in tablas_limpiar:
            print(f"\nLimpiando {descripcion}...")

            try:
                if tabla == "auditoria":
                    # Solo eliminar auditoría relacionada con pacientes
                    response = supabase.table(tabla).delete().in_("tabla_afectada", ["pacientes", "odontograma", "historial_medico", "condiciones_diente"]).execute()
                elif tabla == "pacientes":
                    # Para pacientes, usar numero_historia
                    response = supabase.table(tabla).delete().neq("numero_historia", "").execute()
                else:
                    # Para otras tablas con UUID, usar una condición válida
                    response = supabase.table(tabla).delete().is_("id", "not.null").execute()

                if response.data:
                    eliminados = len(response.data)
                    total_eliminados += eliminados
                    print(f"   EXITO: {eliminados} registros eliminados de {tabla}")
                else:
                    print(f"   INFO: Sin registros en {tabla}")

            except Exception as e:
                if "No rows found" in str(e) or "PGRST116" in str(e):
                    print(f"   INFO: Tabla {tabla} ya estaba vacia")
                else:
                    print(f"   ERROR: {tabla}: {e}")

        print(f"\nLIMPIEZA COMPLETADA")
        print(f"Total de registros eliminados: {total_eliminados}")
        print(f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()

async def verificar_limpieza():
    """Verificar que las tablas están vacías"""
    print("\nVERIFICANDO LIMPIEZA...")

    supabase = get_client()

    tablas_verificar = [
        "pacientes",
        "consultas",
        "odontograma",
        "historial_medico",
        "condiciones_diente"
    ]

    for tabla in tablas_verificar:
        try:
            response = supabase.table(tabla).select("*").limit(1).execute()
            if response.data:
                print(f"   ATENCION: {tabla}: Aun tiene {len(response.data)} registros")
            else:
                print(f"   EXITO: {tabla}: Vacia")
        except Exception as e:
            print(f"   ERROR verificando {tabla}: {e}")

if __name__ == "__main__":
    print("SCRIPT DE LIMPIEZA DE BASE DE DATOS\n")
    asyncio.run(limpiar_datos_pacientes())
    asyncio.run(verificar_limpieza())