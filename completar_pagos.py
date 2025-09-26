"""
Completar Pagos Faltantes
========================

Script para crear los pagos que faltaron debido al problema de duplicados
en numero_recibo. Este script evita el trigger automático.

Autor: Sistema Dental - Wilmer Aguirre
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
import random
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

ADMIN_USER_ID = "6214feee-9786-4d6d-8157-439b1d9e379a"

def log_progreso(mensaje: str, nivel: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {nivel}: {mensaje}")

def obtener_tasa_cambio(fecha: datetime) -> float:
    dias = (fecha.date() - datetime.now().date() + timedelta(days=30)).days
    tasa_base = 36.50
    incremento_diario = 0.10
    variacion = random.uniform(-0.5, 0.5)
    return round(tasa_base + (incremento_diario * dias) + variacion, 2)

async def completar_pagos_faltantes():
    log_progreso("Iniciando completado de pagos faltantes...")

    try:
        # Obtener consultas completadas que NO tienen pago
        query = """
        SELECT c.* FROM consultas c
        LEFT JOIN pagos p ON c.id = p.consulta_id
        WHERE c.estado = 'completada' AND p.id IS NULL
        ORDER BY c.fecha_llegada
        """

        # Usar una consulta directa para evitar limitaciones de Supabase
        consultas_result = supabase.table("consultas").select("*").eq("estado", "completada").execute()
        consultas_completadas = consultas_result.data

        # Obtener IDs de consultas que YA tienen pago
        pagos_existentes = supabase.table("pagos").select("consulta_id").execute()
        consultas_con_pago = {p["consulta_id"] for p in pagos_existentes.data if p["consulta_id"]}

        # Filtrar consultas sin pago
        consultas_sin_pago = [c for c in consultas_completadas if c["id"] not in consultas_con_pago]

        log_progreso(f"Consultas completadas total: {len(consultas_completadas)}")
        log_progreso(f"Consultas que ya tienen pago: {len(consultas_con_pago)}")
        log_progreso(f"Consultas sin pago a procesar: {len(consultas_sin_pago)}")

        # Obtener el último número de recibo para continuar la secuencia
        ultimo_recibo_result = supabase.table("pagos").select("numero_recibo").order("numero_recibo", desc=True).limit(1).execute()

        # Generar número base para evitar duplicados
        if ultimo_recibo_result.data:
            ultimo_numero = ultimo_recibo_result.data[0]["numero_recibo"]
            # Extraer número y incrementar
            if "REC" in ultimo_numero:
                numero_base = int(ultimo_numero.replace("REC", "")) + 1
            else:
                numero_base = 20250925001  # Número base si no hay patrón
        else:
            numero_base = 20250925001

        pagos_creados = []

        for i, consulta in enumerate(consultas_sin_pago, 1):
            try:
                if i % 50 == 0:
                    log_progreso(f"   Procesando pago {i}/{len(consultas_sin_pago)}")

                # Obtener costos de intervenciones
                intervenciones_result = supabase.table("intervenciones").select("total_bs, total_usd").eq("consulta_id", consulta["id"]).execute()
                intervenciones = intervenciones_result.data

                costo_total_bs = sum(float(interv.get("total_bs", 0)) for interv in intervenciones)
                costo_total_usd = sum(float(interv.get("total_usd", 0)) for interv in intervenciones)

                # Valores mínimos si no hay costos
                if costo_total_bs == 0 and costo_total_usd == 0:
                    costo_total_bs = random.uniform(50, 300)
                    costo_total_usd = random.uniform(2, 15)

                # Método de pago
                metodos_disponibles = [
                    ["efectivo_bs"],
                    ["efectivo_usd"],
                    ["transferencia_bs"],
                    ["tarjeta_bs"],
                    ["efectivo_bs", "efectivo_usd"],
                    ["transferencia_bs", "efectivo_usd"],
                ]
                metodos_pago = random.choice(metodos_disponibles)

                # Distribución de pagos
                if len(metodos_pago) == 1:
                    if "bs" in metodos_pago[0]:
                        monto_pagado_bs = costo_total_bs
                        monto_pagado_usd = 0.0
                    else:
                        monto_pagado_bs = 0.0
                        monto_pagado_usd = costo_total_usd
                else:
                    porcentaje_bs = random.uniform(0.3, 0.7)
                    monto_pagado_bs = costo_total_bs * porcentaje_bs
                    monto_pagado_usd = costo_total_usd * (1 - porcentaje_bs)

                # Fecha y tasa
                fecha_consulta = datetime.fromisoformat(consulta["fecha_llegada"])
                dias_diferencia = random.randint(0, 5)
                fecha_pago = fecha_consulta + timedelta(days=dias_diferencia)
                tasa_cambio = obtener_tasa_cambio(fecha_pago)

                # Estado del pago
                estado_pago = "completado" if random.random() > 0.1 else "parcial"

                if estado_pago == "completado":
                    saldo_bs = 0.0
                    saldo_usd = 0.0
                else:
                    saldo_bs = costo_total_bs * random.uniform(0.1, 0.3)
                    saldo_usd = costo_total_usd * random.uniform(0.1, 0.3)
                    monto_pagado_bs = costo_total_bs - saldo_bs
                    monto_pagado_usd = costo_total_usd - saldo_usd

                # Generar número de recibo manual
                numero_recibo = f"REC{numero_base + i:010d}"

                # Conceptos
                conceptos = [
                    "Pago de consulta odontológica y procedimientos realizados",
                    "Tratamiento dental completado según plan terapéutico",
                    "Servicios odontológicos - Consulta y procedimientos",
                    "Atención dental integral - Pago de servicios",
                    "Consulta odontológica - Procedimientos realizados"
                ]

                pago_data = {
                    "id": str(uuid.uuid4()),
                    "numero_recibo": numero_recibo,  # Manual para evitar trigger
                    "consulta_id": consulta["id"],
                    "paciente_id": consulta["paciente_id"],
                    "fecha_pago": fecha_pago.isoformat(),
                    "monto_total_bs": round(costo_total_bs, 2),
                    "monto_total_usd": round(costo_total_usd, 2),
                    "monto_pagado_bs": round(monto_pagado_bs, 2),
                    "monto_pagado_usd": round(monto_pagado_usd, 2),
                    "saldo_pendiente_bs": round(saldo_bs, 2),
                    "saldo_pendiente_usd": round(saldo_usd, 2),
                    "tasa_cambio_bs_usd": tasa_cambio,
                    "metodos_pago": metodos_pago,
                    "concepto": random.choice(conceptos),
                    "estado_pago": estado_pago,
                    "procesado_por": ADMIN_USER_ID,
                    "descuento_bs": 0.0,
                    "descuento_usd": 0.0,
                    "impuestos_bs": 0.0,
                    "impuestos_usd": 0.0,
                    "observaciones": f"Pago {estado_pago} - Métodos: {', '.join(metodos_pago)} - Tasa: {tasa_cambio}"
                }

                # Insertar pago
                result = supabase.table("pagos").insert(pago_data).execute()

                if result.data:
                    pagos_creados.append(pago_data)
                else:
                    log_progreso(f"   ERROR: No se insertó el pago {i}", "ERROR")

            except Exception as e:
                log_progreso(f"   ERROR creando pago {i}: {str(e)}", "ERROR")
                continue

        log_progreso(f"OK Pagos creados exitosamente: {len(pagos_creados)}")
        return pagos_creados

    except Exception as e:
        log_progreso(f"ERROR en completado de pagos: {str(e)}", "ERROR")
        return []

async def main():
    log_progreso("INICIANDO COMPLETADO DE PAGOS")
    log_progreso("=" * 50)

    try:
        pagos = await completar_pagos_faltantes()

        # Verificar totales finales
        total_pagos = supabase.table("pagos").select("id", count="exact").execute()
        total_consultas = supabase.table("consultas").select("id", count="exact").eq("estado", "completada").execute()

        log_progreso("=" * 50)
        log_progreso("SUCCESS COMPLETADO DE PAGOS")
        log_progreso(f"   • Pagos nuevos creados: {len(pagos)}")
        log_progreso(f"   • Total pagos en sistema: {total_pagos.count}")
        log_progreso(f"   • Total consultas completadas: {total_consultas.count}")
        log_progreso("=" * 50)

    except Exception as e:
        log_progreso(f"ERROR: {str(e)}", "ERROR")

if __name__ == "__main__":
    asyncio.run(main())