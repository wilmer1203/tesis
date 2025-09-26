"""
Poblado de Pagos y Odontogramas Evolutivos
==========================================

Script especializado para:
- Generar pagos realistas con campos correctos
- Crear odontogramas evolutivos con condiciones progresivas
- Actualizar condiciones de dientes por intervenciones

Autor: Sistema Dental - Wilmer Aguirre
Universidad de Oriente - Trabajo de Grado
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional
import uuid

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    print("ERROR: Variables de entorno SUPABASE_URL y SUPABASE_ANON_KEY requeridas")
    sys.exit(1)

# Cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ==========================================
# CONFIGURACIONES Y CONSTANTES
# ==========================================

# Usuario para procesado_por (obtenido de la BD)
ADMIN_USER_ID = "6214feee-9786-4d6d-8157-439b1d9e379a"

# Rango de fechas
FECHA_FIN = datetime.now().date()
FECHA_INICIO = FECHA_FIN - timedelta(days=30)

# Condiciones de dientes FDI (32 dientes)
DIENTES_FDI = [
    # Dientes superiores derechos
    18, 17, 16, 15, 14, 13, 12, 11,
    # Dientes superiores izquierdos
    21, 22, 23, 24, 25, 26, 27, 28,
    # Dientes inferiores izquierdos
    38, 37, 36, 35, 34, 33, 32, 31,
    # Dientes inferiores derechos
    41, 42, 43, 44, 45, 46, 47, 48
]

# Condiciones y sus progresiones
CONDICIONES_DIENTES = {
    "sano": ["inicial_caries", "desgaste", "sensibilidad"],
    "inicial_caries": ["caries_superficial", "obturado"],
    "caries_superficial": ["caries_profunda", "obturado"],
    "caries_profunda": ["endodoncia", "extraccion"],
    "obturado": ["recidiva_caries", "fractura_obturacion", "sano"],
    "endodoncia": ["corona", "extraccion"],
    "corona": ["fractura_corona", "sano"],
    "extraccion": ["implante", "protesis"],
    "implante": ["sano"],
    "desgaste": ["corona", "sensibilidad"],
    "sensibilidad": ["sano", "obturado"],
    "fractura": ["corona", "extraccion"],
    "fractura_obturacion": ["obturado", "corona"],
    "fractura_corona": ["corona", "extraccion"],
    "recidiva_caries": ["obturado", "endodoncia"],
    "protesis": ["sano"]
}

# Caras de dientes
CARAS_DIENTES = ["mesial", "distal", "oclusal", "vestibular", "lingual", "incisal"]

def log_progreso(mensaje: str, nivel: str = "INFO"):
    """Registra el progreso del poblado"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {nivel}: {mensaje}")

def obtener_tasa_cambio(fecha: datetime) -> float:
    """Genera tasas de cambio realistas para Venezuela"""
    dias_desde_inicio = (fecha.date() - FECHA_INICIO).days
    tasa_base = 36.50
    incremento_diario = 0.10
    variacion_aleatoria = random.uniform(-0.5, 0.5)
    tasa_final = tasa_base + (incremento_diario * dias_desde_inicio) + variacion_aleatoria
    return round(tasa_final, 2)

# ==========================================
# FASE 1: CREAR PAGOS CORREGIDOS
# ==========================================

async def crear_pagos_corregidos():
    """Crea pagos realistas con todos los campos requeridos"""
    log_progreso("FASE 1: Iniciando creación de pagos corregidos...")

    try:
        # Obtener consultas completadas
        consultas_result = supabase.table("consultas").select("*").eq("estado", "completada").execute()
        consultas_completadas = consultas_result.data

        log_progreso(f"Consultadas completadas encontradas: {len(consultas_completadas)}")

        pagos_creados = []

        for i, consulta in enumerate(consultas_completadas, 1):
            try:
                if i % 50 == 0:
                    log_progreso(f"   Procesando pago {i}/{len(consultas_completadas)}")

                # Obtener costo total de intervenciones de esta consulta
                intervenciones_result = supabase.table("intervenciones").select("total_bs, total_usd").eq("consulta_id", consulta["id"]).execute()
                intervenciones = intervenciones_result.data

                costo_total_bs = sum(float(interv.get("total_bs", 0)) for interv in intervenciones)
                costo_total_usd = sum(float(interv.get("total_usd", 0)) for interv in intervenciones)

                # Si no hay costos, usar valores mínimos
                if costo_total_bs == 0 and costo_total_usd == 0:
                    costo_total_bs = random.uniform(50, 200)
                    costo_total_usd = random.uniform(2, 10)

                # Determinar método de pago y distribución
                metodos_disponibles = [
                    ["efectivo_bs"],
                    ["efectivo_usd"],
                    ["transferencia_bs"],
                    ["tarjeta_bs"],
                    ["efectivo_bs", "efectivo_usd"],  # Pago mixto
                    ["transferencia_bs", "efectivo_usd"],  # Pago mixto
                ]

                metodos_pago = random.choice(metodos_disponibles)

                # Calcular montos de pago
                if len(metodos_pago) == 1:
                    if "bs" in metodos_pago[0]:
                        monto_pagado_bs = costo_total_bs
                        monto_pagado_usd = 0.0
                    else:
                        monto_pagado_bs = 0.0
                        monto_pagado_usd = costo_total_usd
                else:
                    # Pago mixto
                    porcentaje_bs = random.uniform(0.3, 0.7)
                    monto_pagado_bs = costo_total_bs * porcentaje_bs
                    monto_pagado_usd = costo_total_usd * (1 - porcentaje_bs)

                # Fecha de pago (mismo día o hasta 5 días después)
                fecha_consulta = datetime.fromisoformat(consulta["fecha_llegada"])
                dias_diferencia = random.randint(0, 5)
                fecha_pago = fecha_consulta + timedelta(days=dias_diferencia)

                # Tasa de cambio del día
                tasa_cambio = obtener_tasa_cambio(fecha_pago)

                # Estado del pago
                estado_pago = "completado" if random.random() > 0.1 else "parcial"  # 90% completados

                # Saldos pendientes
                if estado_pago == "completado":
                    saldo_bs = 0.0
                    saldo_usd = 0.0
                else:
                    saldo_bs = costo_total_bs * random.uniform(0.1, 0.3)
                    saldo_usd = costo_total_usd * random.uniform(0.1, 0.3)
                    monto_pagado_bs = costo_total_bs - saldo_bs
                    monto_pagado_usd = costo_total_usd - saldo_usd

                # Conceptos realistas
                conceptos_posibles = [
                    "Pago de consulta odontológica y procedimientos realizados",
                    "Tratamiento dental completado según plan terapéutico",
                    "Servicios odontológicos - Consulta y procedimientos",
                    "Atención dental integral - Pago de servicios",
                    "Consulta odontológica - Procedimientos realizados"
                ]

                pago_data = {
                    "id": str(uuid.uuid4()),
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
                    "concepto": random.choice(conceptos_posibles),  # Campo requerido
                    "estado_pago": estado_pago,
                    "procesado_por": ADMIN_USER_ID,  # Campo requerido
                    "descuento_bs": 0.0,
                    "descuento_usd": 0.0,
                    "impuestos_bs": 0.0,
                    "impuestos_usd": 0.0,
                    "observaciones": f"Pago procesado - Métodos: {', '.join(metodos_pago)} - Tasa: {tasa_cambio}"
                }

                # Insertar pago
                result = supabase.table("pagos").insert(pago_data).execute()

                if result.data:
                    pagos_creados.append(pago_data)

            except Exception as e:
                log_progreso(f"   ERROR creando pago {i}: {str(e)}", "ERROR")
                continue

        log_progreso(f"OK Pagos creados exitosamente: {len(pagos_creados)}")
        return pagos_creados

    except Exception as e:
        log_progreso(f"ERROR en creación de pagos: {str(e)}", "ERROR")
        return []

# ==========================================
# FASE 2: CREAR ODONTOGRAMAS EVOLUTIVOS
# ==========================================

async def crear_odontogramas_evolutivos():
    """Crea odontogramas evolutivos con condiciones progresivas"""
    log_progreso("FASE 2: Iniciando creación de odontogramas evolutivos...")

    try:
        # Obtener pacientes activos
        pacientes_result = supabase.table("pacientes").select("id, numero_historia, primer_nombre, primer_apellido").eq("activo", True).execute()
        pacientes = pacientes_result.data

        # Obtener odontólogos
        odontologos_result = supabase.table("personal").select("id").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").execute()
        odontologos = odontologos_result.data

        log_progreso(f"Procesando {len(pacientes)} pacientes para odontogramas...")

        odontogramas_creados = []
        condiciones_creadas = []

        for i, paciente in enumerate(pacientes, 1):
            try:
                if i % 5 == 0:
                    log_progreso(f"   Procesando paciente {i}/{len(pacientes)}")

                # Crear 2-4 versiones de odontograma por paciente
                num_versiones = random.randint(2, 4)
                odontologo_id = random.choice(odontologos)["id"]

                for version in range(1, num_versiones + 1):
                    # Fecha de creación progresiva
                    dias_desde_inicio = random.randint(0, 30)
                    fecha_creacion = FECHA_INICIO + timedelta(days=dias_desde_inicio) + timedelta(days=(version-1) * 7)

                    # Motivo de nueva versión
                    motivos = [
                        "Actualización tras intervención odontológica",
                        "Evolución del estado dental del paciente",
                        "Registro de nuevas condiciones detectadas",
                        "Seguimiento post-tratamiento",
                        "Control de rutina - Actualización condiciones"
                    ]

                    # Obtener versión anterior para referencia
                    version_anterior_id = None
                    if version > 1:
                        # Buscar la versión anterior
                        anterior_result = supabase.table("odontograma").select("id").eq("paciente_id", paciente["id"]).eq("version", version-1).execute()
                        if anterior_result.data:
                            version_anterior_id = anterior_result.data[0]["id"]

                    odontograma_data = {
                        "id": str(uuid.uuid4()),
                        "paciente_id": paciente["id"],
                        "fecha_creacion": fecha_creacion.isoformat(),
                        "fecha_actualizacion": fecha_creacion.isoformat(),
                        "odontologo_id": odontologo_id,
                        "version": version,
                        "es_version_actual": version == num_versiones,  # Solo la última es actual
                        "version_anterior_id": version_anterior_id,
                        "motivo_nueva_version": random.choice(motivos) if version > 1 else "Odontograma inicial del paciente",
                        "tipo_odontograma": "adulto",
                        "notas_generales": f"Odontograma versión {version} - Estado dental del paciente actualizado",
                        "observaciones_clinicas": f"Evaluación clínica realizada el {fecha_creacion.strftime('%Y-%m-%d')}",
                        "template_usado": "universal",
                        "configuracion": {},
                        "estadisticas_condiciones": {}
                    }

                    # Insertar odontograma
                    result = supabase.table("odontograma").insert(odontograma_data).execute()

                    if result.data:
                        odontograma_id = result.data[0]["id"]
                        odontogramas_creados.append(odontograma_data)

                        # Crear condiciones para cada diente
                        condiciones_diente = await crear_condiciones_dientes(odontograma_id, version)
                        condiciones_creadas.extend(condiciones_diente)

            except Exception as e:
                log_progreso(f"   ERROR procesando paciente {i}: {str(e)}", "ERROR")
                continue

        log_progreso(f"OK Odontogramas creados: {len(odontogramas_creados)}")
        log_progreso(f"OK Condiciones de dientes creadas: {len(condiciones_creadas)}")
        return odontogramas_creados, condiciones_creadas

    except Exception as e:
        log_progreso(f"ERROR en creación de odontogramas: {str(e)}", "ERROR")
        return [], []

async def crear_condiciones_dientes(odontograma_id: str, version: int) -> List[Dict]:
    """Crea condiciones realistas para todos los dientes de un odontograma"""
    condiciones_creadas = []

    # Determinar número de dientes afectados según la versión
    if version == 1:
        # Primera versión: 60-80% de dientes sanos, algunos con problemas iniciales
        prob_problema = 0.3
    else:
        # Versiones posteriores: más problemas y evolución
        prob_problema = 0.5

    for numero_diente in DIENTES_FDI:
        try:
            # Determinar si el diente tiene algún problema
            if random.random() < prob_problema:
                # Diente con alguna condición
                condiciones_posibles = ["inicial_caries", "caries_superficial", "obturado", "desgaste", "sensibilidad"]
                if version > 1:
                    condiciones_posibles.extend(["caries_profunda", "endodoncia", "corona", "fractura"])

                condicion_actual = random.choice(condiciones_posibles)
            else:
                # Diente sano
                condicion_actual = "sano"

            # Seleccionar caras afectadas
            num_caras_afectadas = random.randint(1, 3) if condicion_actual != "sano" else 0
            caras_afectadas = random.sample(CARAS_DIENTES, num_caras_afectadas) if num_caras_afectadas > 0 else []

            condicion_data = {
                "id": str(uuid.uuid4()),
                "odontograma_id": odontograma_id,
                "numero_diente": numero_diente,
                "condicion_actual": condicion_actual,
                "caras_afectadas": caras_afectadas,
                "severidad": random.choice(["leve", "moderada", "severa"]) if condicion_actual != "sano" else "normal",
                "requiere_tratamiento": condicion_actual not in ["sano", "obturado", "corona", "implante"],
                "prioridad_tratamiento": random.choice(["baja", "media", "alta"]) if condicion_actual not in ["sano", "obturado", "corona"] else "ninguna",
                "notas_condicion": f"Diente {numero_diente}: {condicion_actual}" + (f" en caras {', '.join(caras_afectadas)}" if caras_afectadas else ""),
                "fecha_deteccion": datetime.now().isoformat(),
                "intervencion_origen_id": None,  # Se puede vincular posteriormente
                "requiere_control": random.choice([True, False]) if condicion_actual not in ["sano"] else False,
                "fecha_proximo_control": (datetime.now() + timedelta(days=random.randint(30, 90))).isoformat() if random.random() > 0.7 else None
            }

            # Insertar condición
            result = supabase.table("condiciones_diente").insert(condicion_data).execute()

            if result.data:
                condiciones_creadas.append(condicion_data)

        except Exception as e:
            log_progreso(f"   ERROR creando condición para diente {numero_diente}: {str(e)}", "ERROR")
            continue

    return condiciones_creadas

# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================

async def main():
    """Función principal para pagos y odontogramas"""
    log_progreso("INICIANDO POBLADO DE PAGOS Y ODONTOGRAMAS")
    log_progreso(f"Período: {FECHA_INICIO} al {FECHA_FIN}")
    log_progreso("=" * 60)

    try:
        # FASE 1: Crear pagos corregidos
        pagos = await crear_pagos_corregidos()

        # FASE 2: Crear odontogramas evolutivos
        odontogramas, condiciones = await crear_odontogramas_evolutivos()

        log_progreso("=" * 60)
        log_progreso("SUCCESS POBLADO DE PAGOS Y ODONTOGRAMAS COMPLETADO")
        log_progreso(f"   Resumen:")
        log_progreso(f"   • Pagos creados: {len(pagos)}")
        log_progreso(f"   • Odontogramas creados: {len(odontogramas)}")
        log_progreso(f"   • Condiciones de dientes: {len(condiciones)}")
        log_progreso("=" * 60)

        # Verificar totales finales
        log_progreso("Verificando totales finales...")

        # Contar registros totales
        total_result = await verificar_totales_finales()
        log_progreso("VERIFICACION COMPLETA:")
        for tabla, total in total_result.items():
            log_progreso(f"   • {tabla}: {total}")

    except Exception as e:
        log_progreso(f"ERROR en función principal: {str(e)}", "ERROR")
        raise

async def verificar_totales_finales():
    """Verifica los totales finales de todas las tablas"""
    try:
        # Consulta de totales
        query = """
        SELECT
            'Pacientes' as tabla, COUNT(*) as total FROM pacientes WHERE activo = true
        UNION ALL
        SELECT 'Odontólogos' as tabla, COUNT(*) as total FROM personal WHERE tipo_personal = 'Odontólogo' AND estado_laboral = 'activo'
        UNION ALL
        SELECT 'Consultas' as tabla, COUNT(*) as total FROM consultas
        UNION ALL
        SELECT 'Intervenciones' as tabla, COUNT(*) as total FROM intervenciones
        UNION ALL
        SELECT 'Servicios Realizados' as tabla, COUNT(*) as total FROM intervenciones_servicios
        UNION ALL
        SELECT 'Pagos' as tabla, COUNT(*) as total FROM pagos
        UNION ALL
        SELECT 'Odontogramas' as tabla, COUNT(*) as total FROM odontograma
        UNION ALL
        SELECT 'Condiciones Dientes' as tabla, COUNT(*) as total FROM condiciones_diente
        ORDER BY tabla;
        """

        result = supabase.rpc('execute_sql', {'query': query}).execute()

        if result.data:
            return {row['tabla']: row['total'] for row in result.data}
        else:
            # Fallback: consultas individuales
            tablas = [
                ('Pacientes', "SELECT COUNT(*) FROM pacientes WHERE activo = true"),
                ('Consultas', "SELECT COUNT(*) FROM consultas"),
                ('Intervenciones', "SELECT COUNT(*) FROM intervenciones"),
                ('Pagos', "SELECT COUNT(*) FROM pagos"),
                ('Odontogramas', "SELECT COUNT(*) FROM odontograma")
            ]

            totales = {}
            for nombre, query in tablas:
                try:
                    res = supabase.rpc('execute_sql', {'query': query}).execute()
                    totales[nombre] = res.data[0]['count'] if res.data else 0
                except:
                    totales[nombre] = "Error"

            return totales

    except Exception as e:
        log_progreso(f"ERROR verificando totales: {str(e)}", "ERROR")
        return {}

if __name__ == "__main__":
    asyncio.run(main())