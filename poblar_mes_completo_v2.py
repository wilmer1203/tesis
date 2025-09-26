"""
Sistema de Poblado Completo V2 - Un Mes de Operación Clínica
============================================================

Version corregida que maneja:
- Creación directa de personal (sin Auth por permisos)
- Consultas sin colisión de números
- Intervenciones y odontogramas realistas
- Pagos y datos complementarios

Autor: Sistema Dental - Wilmer Aguirre
Universidad de Oriente - Trabajo de Grado
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta, time
import random
from typing import List, Dict, Any, Optional, Tuple
import uuid
from decimal import Decimal
import json

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

# Rango de fechas para el poblado (30 días atrás desde hoy)
FECHA_FIN = datetime.now().date()
FECHA_INICIO = FECHA_FIN - timedelta(days=30)

# Horarios de atención
HORA_INICIO = time(8, 0)  # 8:00 AM
HORA_FIN = time(18, 0)   # 6:00 PM

# Distribución de consultas por día de semana
CONSULTAS_POR_DIA = {
    0: 8,  # Lunes
    1: 9,  # Martes
    2: 8,  # Miércoles
    3: 10, # Jueves
    4: 9,  # Viernes
    5: 6,  # Sábado
    6: 0   # Domingo (cerrado)
}

# Estados de consulta y probabilidades
ESTADOS_CONSULTA = {
    "completada": 0.70,    # 70%
    "en_atencion": 0.05,   # 5%
    "cancelada": 0.15,     # 15%
    "en_espera": 0.10      # 10%
}

# Nuevos odontólogos (solo datos de personal)
NUEVOS_ODONTOLOGOS = [
    {
        "primer_nombre": "Dr. Carlos",
        "segundo_nombre": "Alberto",
        "primer_apellido": "Rodriguez",
        "segundo_apellido": "Mendez",
        "numero_documento": "12345678",
        "especialidad": "Odontología General",
        "numero_licencia": "ODG-12345",
        "celular": "+58-414-1234567",
        "salario": Decimal("800.00")
    },
    {
        "primer_nombre": "Dra. María",
        "segundo_nombre": "Elena",
        "primer_apellido": "González",
        "segundo_apellido": "Torres",
        "numero_documento": "23456789",
        "especialidad": "Odontología General",
        "numero_licencia": "ODG-23456",
        "celular": "+58-424-2345678",
        "salario": Decimal("800.00")
    },
    {
        "primer_nombre": "Dr. Pedro",
        "segundo_nombre": "José",
        "primer_apellido": "Santos",
        "segundo_apellido": "Ramos",
        "numero_documento": "34567890",
        "especialidad": "Ortodoncia",
        "numero_licencia": "ORT-34567",
        "celular": "+58-412-3456789",
        "salario": Decimal("950.00")
    },
    {
        "primer_nombre": "Dra. Sofia",
        "segundo_nombre": "Isabel",
        "primer_apellido": "Herrera",
        "segundo_apellido": "Castro",
        "numero_documento": "45678901",
        "especialidad": "Endodoncia",
        "numero_licencia": "END-45678",
        "celular": "+58-416-4567890",
        "salario": Decimal("900.00")
    },
    {
        "primer_nombre": "Dr. Ricardo",
        "segundo_nombre": "Manuel",
        "primer_apellido": "Vargas",
        "segundo_apellido": "Luna",
        "numero_documento": "56789012",
        "especialidad": "Cirugía Oral",
        "numero_licencia": "COR-56789",
        "celular": "+58-426-5678901",
        "salario": Decimal("1000.00")
    }
]

# Condiciones de dientes y sus progresiones
CONDICIONES_DIENTES = [
    "sano", "inicial_caries", "caries_superficial", "caries_profunda",
    "obturado", "endodoncia", "corona", "extraccion", "implante",
    "fractura", "desgaste", "sensibilidad"
]

# Distribución de servicios por frecuencia real
SERVICIOS_FRECUENCIA = [
    ("CONS001", 0.30),  # Consulta General (30%)
    ("LIMP001", 0.20),  # Profilaxis (20%)
    ("OBTU001", 0.25),  # Obturación (25%)
    ("ENDO001", 0.08),  # Endodoncia (8%)
    ("EXTR001", 0.06),  # Extracción Simple (6%)
    ("EXTR002", 0.03),  # Extracción Compleja (3%)
    ("RADI001", 0.05),  # Radiografía (5%)
    ("CORO001", 0.02),  # Corona (2%)
    ("IMPL001", 0.01),  # Implante (1%)
]

def log_progreso(mensaje: str, nivel: str = "INFO"):
    """Registra el progreso del poblado"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {nivel}: {mensaje}")

def obtener_tasa_cambio(fecha: datetime) -> Decimal:
    """Genera tasas de cambio realistas para Venezuela"""
    dias_desde_inicio = (fecha.date() - FECHA_INICIO).days
    tasa_base = Decimal("36.50")  # Tasa inicial
    incremento_diario = Decimal("0.10")  # Incremento diario
    variacion_aleatoria = Decimal(str(random.uniform(-0.5, 0.5)))

    tasa_final = tasa_base + (incremento_diario * dias_desde_inicio) + variacion_aleatoria
    return round(tasa_final, 2)

def generar_fecha_hora_consulta(fecha: datetime.date, orden: int) -> datetime:
    """Genera hora realista para una consulta según su orden"""
    minutos_inicio = HORA_INICIO.hour * 60 + HORA_INICIO.minute
    minutos_por_consulta = 45  # 45 minutos promedio por consulta

    minutos_consulta = minutos_inicio + (orden * minutos_por_consulta)
    horas = minutos_consulta // 60
    minutos = minutos_consulta % 60

    # Agregar variación aleatoria de ±15 minutos
    variacion = random.randint(-15, 15)
    minutos += variacion

    if minutos >= 60:
        horas += 1
        minutos -= 60
    elif minutos < 0:
        horas -= 1
        minutos += 60

    # Asegurar que esté dentro del horario laboral
    if horas < HORA_INICIO.hour:
        horas = HORA_INICIO.hour
        minutos = HORA_INICIO.minute
    elif horas >= HORA_FIN.hour:
        horas = HORA_FIN.hour - 1
        minutos = 30

    fecha_hora = datetime.combine(fecha, time(horas, minutos))
    return fecha_hora

# ==========================================
# FASE 1: CREAR PERSONAL ADICIONAL (SIN AUTH)
# ==========================================

async def crear_personal_adicional():
    """Crea 5 odontólogos adicionales como personal (sin usuarios Auth)"""
    log_progreso("FASE 1: Iniciando creación de 5 odontólogos adicionales...")

    personal_creado = []

    for i, odontologo_data in enumerate(NUEVOS_ODONTOLOGOS, 1):
        try:
            log_progreso(f"Creando odontólogo {i}/5: {odontologo_data['primer_nombre']} {odontologo_data['primer_apellido']}")

            # Crear directamente en tabla personal (sin usuario Auth por ahora)
            personal_data = {
                **odontologo_data,
                "id": str(uuid.uuid4()),
                "usuario_id": None,  # Sin usuario Auth por ahora
                "tipo_documento": "CI",
                "tipo_personal": "Odontólogo",
                "fecha_contratacion": FECHA_INICIO,
                "estado_laboral": "activo",
                "acepta_pacientes_nuevos": True,
                "orden_preferencia": i + 2  # Después de los 2 existentes
            }

            result = supabase.table("personal").insert(personal_data).execute()

            if result.data:
                personal_creado.append({
                    "id": personal_data["id"],
                    "nombre": f"{personal_data['primer_nombre']} {personal_data['primer_apellido']}",
                    "especialidad": personal_data["especialidad"]
                })
                log_progreso(f"   OK Personal creado: {personal_data['primer_nombre']} {personal_data['primer_apellido']}")

        except Exception as e:
            log_progreso(f"   ERROR creando odontólogo {i}: {str(e)}", "ERROR")
            continue

    log_progreso(f"OK Personal adicional creado: {len(personal_creado)}/5")
    return personal_creado

# ==========================================
# OBTENER DATOS BASE
# ==========================================

async def obtener_datos_base():
    """Obtiene pacientes, odontólogos y servicios existentes"""
    try:
        # Obtener pacientes activos
        pacientes_result = supabase.table("pacientes").select("id, numero_historia, primer_nombre, primer_apellido").eq("activo", True).execute()
        pacientes = pacientes_result.data

        # Obtener odontólogos activos
        odontologos_result = supabase.table("personal").select("id, primer_nombre, primer_apellido, especialidad").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").execute()
        odontologos = odontologos_result.data

        # Obtener servicios activos
        servicios_result = supabase.table("servicios").select("id, codigo, nombre, precio_base_bs, precio_base_usd, categoria").eq("activo", True).execute()
        servicios = servicios_result.data

        log_progreso(f"Datos base: {len(pacientes)} pacientes, {len(odontologos)} odontólogos, {len(servicios)} servicios")

        return pacientes, odontologos, servicios

    except Exception as e:
        log_progreso(f"ERROR obteniendo datos base: {str(e)}", "ERROR")
        return [], [], []

# ==========================================
# FASE 2: GENERAR CONSULTAS HISTÓRICAS
# ==========================================

async def obtener_ultimo_numero_consulta():
    """Obtiene el último número de consulta para evitar duplicados"""
    try:
        result = supabase.table("consultas").select("numero_consulta").order("numero_consulta", desc=True).limit(1).execute()
        if result.data and len(result.data) > 0:
            ultimo_numero = result.data[0]["numero_consulta"]
            # Extraer el número (formato: 2025092401, 2025092402, etc.)
            if ultimo_numero and len(ultimo_numero) >= 8:
                return int(ultimo_numero[-2:]) if ultimo_numero[-2:].isdigit() else 0
        return 0
    except Exception as e:
        log_progreso(f"ERROR obteniendo último número consulta: {str(e)}", "ERROR")
        return 0

async def generar_consultas_historicas(pacientes: List[Dict], odontologos: List[Dict]):
    """Genera consultas distribuidas en 30 días (sin triggers automáticos)"""
    log_progreso("FASE 2: Iniciando generación de consultas históricas...")

    # Obtener último número para evitar duplicados
    ultimo_numero = await obtener_ultimo_numero_consulta()
    numero_consulta_actual = ultimo_numero + 1

    consultas_creadas = []
    fecha_actual = FECHA_INICIO
    orden_general = 1

    while fecha_actual <= FECHA_FIN:
        dia_semana = fecha_actual.weekday()
        consultas_dia = CONSULTAS_POR_DIA[dia_semana]

        if consultas_dia > 0:
            log_progreso(f"   Generando {consultas_dia} consultas para {fecha_actual.strftime('%Y-%m-%d')} ({['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'][dia_semana]})")

            # Distribuir pacientes aleatoriamente
            pacientes_dia = random.choices(pacientes, k=consultas_dia)

            for orden_dia in range(consultas_dia):
                try:
                    paciente = pacientes_dia[orden_dia]

                    # Seleccionar odontólogo (distribuir equitativamente)
                    odontologo = odontologos[orden_general % len(odontologos)]

                    # Generar hora realista
                    fecha_hora_llegada = generar_fecha_hora_consulta(fecha_actual, orden_dia)

                    # Determinar estado de la consulta
                    estado = random.choices(
                        list(ESTADOS_CONSULTA.keys()),
                        weights=list(ESTADOS_CONSULTA.values())
                    )[0]

                    # Generar número de consulta manual
                    fecha_str = fecha_actual.strftime("%Y%m%d")
                    numero_consulta = f"{fecha_str}{numero_consulta_actual:02d}"
                    numero_consulta_actual += 1

                    # Generar datos de consulta
                    consulta_data = {
                        "id": str(uuid.uuid4()),
                        "numero_consulta": numero_consulta,  # Manual para evitar duplicados
                        "paciente_id": paciente["id"],
                        "primer_odontologo_id": odontologo["id"],
                        "fecha_llegada": fecha_hora_llegada.isoformat(),
                        "orden_llegada_general": orden_general,
                        "orden_cola_odontologo": orden_dia + 1,
                        "estado": estado,
                        "tipo_consulta": random.choice(["general", "control", "urgencia"]),
                        "prioridad": "normal",
                        "motivo_consulta": f"Consulta odontológica - {random.choice(['control rutinario', 'dolor dental', 'revisión general', 'continuación tratamiento'])}"
                    }

                    # Calcular tiempos si la consulta está completada
                    if estado == "completada":
                        inicio_atencion = fecha_hora_llegada + timedelta(minutes=random.randint(5, 30))
                        duracion_consulta = random.randint(30, 120)  # 30-120 minutos
                        fin_atencion = inicio_atencion + timedelta(minutes=duracion_consulta)

                        consulta_data.update({
                            "fecha_inicio_atencion": inicio_atencion.isoformat(),
                            "fecha_fin_atencion": fin_atencion.isoformat()
                        })

                    # Insertar consulta
                    result = supabase.table("consultas").insert(consulta_data).execute()

                    if result.data:
                        consultas_creadas.append({
                            **consulta_data,
                            "paciente_nombre": f"{paciente['primer_nombre']} {paciente['primer_apellido']}",
                            "odontologo_nombre": f"{odontologo['primer_nombre']} {odontologo['primer_apellido']}"
                        })

                except Exception as e:
                    log_progreso(f"   ERROR creando consulta {orden_general}: {str(e)}", "ERROR")

                orden_general += 1

        fecha_actual += timedelta(days=1)

    log_progreso(f"OK Consultas históricas creadas: {len(consultas_creadas)}")
    return consultas_creadas

# ==========================================
# FASE 3: CREAR INTERVENCIONES
# ==========================================

async def crear_intervenciones_consultas(consultas: List[Dict], servicios: List[Dict]):
    """Crea intervenciones realistas para consultas completadas"""
    log_progreso("FASE 3: Iniciando creación de intervenciones...")

    intervenciones_creadas = []
    consultas_completadas = [c for c in consultas if c["estado"] == "completada"]

    # Crear mapa de servicios por código para búsqueda rápida
    servicios_map = {s["codigo"]: s for s in servicios}

    for i, consulta in enumerate(consultas_completadas, 1):
        try:
            if i % 20 == 0:
                log_progreso(f"   Procesando consulta {i}/{len(consultas_completadas)}")

            # Determinar número de intervenciones (1-3 por consulta)
            num_intervenciones = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]

            for interv_num in range(num_intervenciones):
                # Seleccionar servicios según frecuencia
                servicios_seleccionados = random.choices(
                    [s[0] for s in SERVICIOS_FRECUENCIA],
                    weights=[s[1] for s in SERVICIOS_FRECUENCIA],
                    k=random.randint(1, 2)  # 1-2 servicios por intervención
                )

                # Calcular costo total de la intervención
                costo_bs = Decimal("0.00")
                costo_usd = Decimal("0.00")

                for codigo_servicio in servicios_seleccionados:
                    if codigo_servicio in servicios_map:
                        servicio = servicios_map[codigo_servicio]
                        costo_bs += Decimal(str(servicio["precio_base_bs"]))
                        costo_usd += Decimal(str(servicio["precio_base_usd"]))

                # Generar datos de intervención
                fecha_inicio = datetime.fromisoformat(consulta["fecha_inicio_atencion"]) if consulta.get("fecha_inicio_atencion") else datetime.now()
                duracion_minutos = random.randint(30, 90)
                fecha_fin = fecha_inicio + timedelta(minutes=duracion_minutos)

                intervencion_data = {
                    "id": str(uuid.uuid4()),
                    "consulta_id": consulta["id"],
                    "odontologo_id": consulta["primer_odontologo_id"],
                    "hora_inicio": fecha_inicio.isoformat(),
                    "hora_fin": fecha_fin.isoformat(),
                    "duracion_real": f"{duracion_minutos} minutes",
                    "dientes_afectados": [random.randint(11, 48) for _ in range(random.randint(1, 4))],  # Numeración FDI
                    "diagnostico_inicial": f"Diagnóstico clínico - {random.choice(['caries dental', 'gingivitis', 'periodontitis', 'desgaste', 'fractura'])}",
                    "procedimiento_realizado": f"Procedimientos: {', '.join(servicios_seleccionados)}",
                    "materiales_utilizados": [
                        random.choice(["Resina compuesta", "Amalgama", "Ionómero de vidrio", "Cemento temporal"])
                        for _ in range(random.randint(1, 3))
                    ],
                    "anestesia_utilizada": random.choice([None, "Lidocaína 2%", "Articaína 4%"]),
                    "complicaciones": None if random.random() > 0.1 else "Complicación menor durante el procedimiento",
                    "total_bs": float(costo_bs),
                    "total_usd": float(costo_usd),
                    "descuento_bs": 0.00,
                    "descuento_usd": 0.00,
                    "estado": "completada",
                    "requiere_control": random.choice([True, False]),
                    "fecha_control_sugerida": (fecha_fin + timedelta(days=random.randint(7, 30))).date() if random.random() > 0.7 else None,
                    "instrucciones_paciente": f"Instrucciones post-tratamiento: {random.choice(['Evitar alimentos duros', 'Enjuague con agua salada', 'Tomar analgésicos si hay dolor', 'Mantener higiene oral'])}",
                    "cambios_odontograma": []  # Se llenará después
                }

                # Insertar intervención
                result = supabase.table("intervenciones").insert(intervencion_data).execute()

                if result.data:
                    intervencion_id = result.data[0]["id"]

                    # Insertar servicios de la intervención
                    for codigo_servicio in servicios_seleccionados:
                        if codigo_servicio in servicios_map:
                            servicio = servicios_map[codigo_servicio]

                            intervencion_servicio_data = {
                                "id": str(uuid.uuid4()),
                                "intervencion_id": intervencion_id,
                                "servicio_id": servicio["id"],
                                "cantidad": 1,
                                "precio_unitario_bs": float(servicio["precio_base_bs"]),
                                "precio_unitario_usd": float(servicio["precio_base_usd"]),
                                "subtotal_bs": float(servicio["precio_base_bs"]),
                                "subtotal_usd": float(servicio["precio_base_usd"]),
                                "notas": f"Servicio realizado: {servicio['nombre']}"
                            }

                            supabase.table("intervenciones_servicios").insert(intervencion_servicio_data).execute()

                    intervenciones_creadas.append(intervencion_data)

        except Exception as e:
            log_progreso(f"   ERROR creando intervención para consulta {i}: {str(e)}", "ERROR")

    log_progreso(f"OK Intervenciones creadas: {len(intervenciones_creadas)}")
    return intervenciones_creadas

# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================

async def main():
    """Función principal del poblado completo V2"""
    log_progreso("INICIANDO POBLADO COMPLETO V2 - UN MES DE OPERACIÓN CLÍNICA")
    log_progreso(f"Período: {FECHA_INICIO} al {FECHA_FIN} (30 días)")
    log_progreso("=" * 60)

    try:
        # FASE 1: Crear personal adicional
        personal_nuevo = await crear_personal_adicional()

        # Obtener datos base actualizados
        log_progreso("Obteniendo datos base actualizados...")
        pacientes, odontologos, servicios = await obtener_datos_base()

        if not pacientes or not odontologos:
            log_progreso("ERROR: No se pudieron obtener datos base. Abortando.", "ERROR")
            return

        # FASE 2: Generar consultas históricas
        consultas = await generar_consultas_historicas(pacientes, odontologos)

        # FASE 3: Crear intervenciones
        intervenciones = await crear_intervenciones_consultas(consultas, servicios)

        log_progreso("=" * 60)
        log_progreso("SUCCESS POBLADO COMPLETO V2 EXITOSO")
        log_progreso(f"   Resumen:")
        log_progreso(f"   • Personal nuevo: {len(personal_nuevo)}")
        log_progreso(f"   • Consultas generadas: {len(consultas)}")
        log_progreso(f"   • Intervenciones creadas: {len(intervenciones)}")
        log_progreso(f"   • Total pacientes: {len(pacientes)}")
        log_progreso(f"   • Total odontólogos: {len(odontologos)}")
        log_progreso("=" * 60)

    except Exception as e:
        log_progreso(f"ERROR en función principal: {str(e)}", "ERROR")
        raise

if __name__ == "__main__":
    asyncio.run(main())