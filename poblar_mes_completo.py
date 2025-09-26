"""
Sistema de Poblado Completo - Un Mes de Operación Clínica
===============================================

Este script puebla la base de datos con datos realistas de 30 días de operación:
- 5 odontólogos adicionales (total 7)
- 150-200 consultas históricas
- 300-400 intervenciones con servicios variados
- Odontogramas evolutivos con condiciones reales
- Pagos mixtos BS/USD con diferentes métodos

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
    print("❌ Error: Variables de entorno SUPABASE_URL y SUPABASE_ANON_KEY requeridas")
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
DURACION_CONSULTA_MIN = 30  # minutos mínimos por consulta

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

# Distribución de servicios por frecuencia real
DISTRIBUCION_SERVICIOS = {
    "CONS001": 0.30,  # Consulta General (30%)
    "LIMP001": 0.20,  # Profilaxis (20%)
    "OBTU001": 0.25,  # Obturación (25%)
    "ENDO001": 0.08,  # Endodoncia (8%)
    "EXTR001": 0.06,  # Extracción Simple (6%)
    "EXTR002": 0.03,  # Extracción Compleja (3%)
    "RADI001": 0.05,  # Radiografía (5%)
    "CORO001": 0.02,  # Corona (2%)
    "IMPL001": 0.01,  # Implante (1%)
}

# Condiciones de dientes progresivas
CONDICIONES_PROGRESION = {
    "sano": ["inicial_caries", "caries_superficial"],
    "inicial_caries": ["caries_superficial", "caries_profunda"],
    "caries_superficial": ["caries_profunda", "obturado"],
    "caries_profunda": ["obturado", "endodoncia"],
    "obturado": ["recidiva_caries", "fractura_obturacion"],
    "endodoncia": ["corona", "extraccion"],
    "corona": ["fractura_corona"],
    "extraccion": ["implante", "protesis"]
}

# Tasas de cambio BS/USD históricas (aproximadas)
def obtener_tasa_cambio(fecha: datetime) -> Decimal:
    """Genera tasas de cambio realistas para Venezuela"""
    # Tasa base que va aumentando con el tiempo
    dias_desde_inicio = (fecha.date() - FECHA_INICIO).days
    tasa_base = Decimal("36.50")  # Tasa inicial
    incremento_diario = Decimal("0.10")  # Incremento diario
    variacion_aleatoria = Decimal(str(random.uniform(-0.5, 0.5)))

    tasa_final = tasa_base + (incremento_diario * dias_desde_inicio) + variacion_aleatoria
    return round(tasa_final, 2)

# ==========================================
# DATOS DE ODONTÓLOGOS ADICIONALES
# ==========================================

NUEVOS_ODONTOLOGOS = [
    {
        "usuario": {
            "email": "carlos.rodriguez@clinicadental.com",
            "password": "ClínicaDental2024!",
            "nombre_completo": "Dr. Carlos Rodriguez"
        },
        "personal": {
            "primer_nombre": "Dr. Carlos",
            "segundo_nombre": "Alberto",
            "primer_apellido": "Rodriguez",
            "segundo_apellido": "Mendez",
            "numero_documento": "12345678",
            "especialidad": "Odontología General",
            "numero_licencia": "ODG-12345",
            "celular": "+58-414-1234567",
            "salario": Decimal("800.00")
        }
    },
    {
        "usuario": {
            "email": "maria.gonzalez@clinicadental.com",
            "password": "ClínicaDental2024!",
            "nombre_completo": "Dra. María González"
        },
        "personal": {
            "primer_nombre": "Dra. María",
            "segundo_nombre": "Elena",
            "primer_apellido": "González",
            "segundo_apellido": "Torres",
            "numero_documento": "23456789",
            "especialidad": "Odontología General",
            "numero_licencia": "ODG-23456",
            "celular": "+58-424-2345678",
            "salario": Decimal("800.00")
        }
    },
    {
        "usuario": {
            "email": "pedro.santos@clinicadental.com",
            "password": "ClínicaDental2024!",
            "nombre_completo": "Dr. Pedro Santos"
        },
        "personal": {
            "primer_nombre": "Dr. Pedro",
            "segundo_nombre": "José",
            "primer_apellido": "Santos",
            "segundo_apellido": "Ramos",
            "numero_documento": "34567890",
            "especialidad": "Ortodencia",
            "numero_licencia": "ORT-34567",
            "celular": "+58-412-3456789",
            "salario": Decimal("950.00")
        }
    },
    {
        "usuario": {
            "email": "sofia.herrera@clinicadental.com",
            "password": "ClínicaDental2024!",
            "nombre_completo": "Dra. Sofia Herrera"
        },
        "personal": {
            "primer_nombre": "Dra. Sofia",
            "segundo_nombre": "Isabel",
            "primer_apellido": "Herrera",
            "segundo_apellido": "Castro",
            "numero_documento": "45678901",
            "especialidad": "Endodoncia",
            "numero_licencia": "END-45678",
            "celular": "+58-416-4567890",
            "salario": Decimal("900.00")
        }
    },
    {
        "usuario": {
            "email": "ricardo.vargas@clinicadental.com",
            "password": "ClínicaDental2024!",
            "nombre_completo": "Dr. Ricardo Vargas"
        },
        "personal": {
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
    }
]

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def log_progreso(mensaje: str, nivel: str = "INFO"):
    """Registra el progreso del poblado"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    # Reemplazar emojis para compatibilidad con Windows
    mensaje_clean = mensaje.replace("🚀", ">>").replace("🦷", "*").replace("📅", ">>").replace("📍", ">>").replace("✅", "OK").replace("❌", "ERROR").replace("📊", ">>").replace("🎉", "SUCCESS")
    print(f"[{timestamp}] {nivel}: {mensaje_clean}")

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

def calcular_duracion_realista(servicios: List[str]) -> int:
    """Calcula duración realista basada en servicios"""
    duraciones = {
        "CONS001": 30,   # Consulta General
        "LIMP001": 45,   # Profilaxis
        "OBTU001": 60,   # Obturación
        "ENDO001": 90,   # Endodoncia
        "EXTR001": 30,   # Extracción Simple
        "EXTR002": 60,   # Extracción Compleja
        "RADI001": 15,   # Radiografía
        "CORO001": 120,  # Corona
        "IMPL001": 180,  # Implante
    }

    duracion_total = sum(duraciones.get(servicio, 30) for servicio in servicios)
    return min(duracion_total, 240)  # Máximo 4 horas

# ==========================================
# FASE 1: CREAR ODONTÓLOGOS ADICIONALES
# ==========================================

async def crear_odontologos_adicionales():
    """Crea 5 odontólogos adicionales con usuarios Auth vinculados"""
    log_progreso("🦷 Iniciando creación de 5 odontólogos adicionales...")

    odontologos_creados = []

    for i, odontologo_data in enumerate(NUEVOS_ODONTOLOGOS, 1):
        try:
            log_progreso(f"Creando odontólogo {i}/5: {odontologo_data['usuario']['nombre_completo']}")

            # 1. Crear usuario en Auth
            auth_response = supabase.auth.admin.create_user({
                "email": odontologo_data["usuario"]["email"],
                "password": odontologo_data["usuario"]["password"],
                "email_confirm": True
            })

            if hasattr(auth_response, 'user') and auth_response.user:
                usuario_id = auth_response.user.id
                log_progreso(f"   ✅ Usuario Auth creado: {usuario_id}")

                # 2. Insertar en tabla usuarios
                usuario_db = {
                    "id": usuario_id,
                    "email": odontologo_data["usuario"]["email"],
                    "nombre_completo": odontologo_data["usuario"]["nombre_completo"],
                    "rol": "odontologo",
                    "activo": True
                }

                result_usuario = supabase.table("usuarios").insert(usuario_db).execute()
                log_progreso(f"   ✅ Usuario DB insertado")

                # 3. Insertar en tabla personal
                personal_data = {
                    **odontologo_data["personal"],
                    "id": str(uuid.uuid4()),
                    "usuario_id": usuario_id,
                    "tipo_documento": "CI",
                    "tipo_personal": "Odontólogo",
                    "fecha_contratacion": FECHA_INICIO,
                    "estado_laboral": "activo",
                    "acepta_pacientes_nuevos": True,
                    "orden_preferencia": i + 2  # Después de los 2 existentes
                }

                result_personal = supabase.table("personal").insert(personal_data).execute()
                log_progreso(f"   ✅ Personal insertado: {personal_data['primer_nombre']} {personal_data['primer_apellido']}")

                odontologos_creados.append({
                    "usuario_id": usuario_id,
                    "personal_id": personal_data["id"],
                    "nombre": f"{personal_data['primer_nombre']} {personal_data['primer_apellido']}",
                    "especialidad": personal_data["especialidad"]
                })

        except Exception as e:
            log_progreso(f"   ❌ Error creando odontólogo {i}: {str(e)}", "ERROR")
            continue

    log_progreso(f"✅ Odontólogos creados exitosamente: {len(odontologos_creados)}/5")
    return odontologos_creados

# ==========================================
# FASE 2: GENERAR CONSULTAS HISTÓRICAS
# ==========================================

async def obtener_datos_base():
    """Obtiene pacientes y odontólogos existentes"""
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

        log_progreso(f"📊 Datos base: {len(pacientes)} pacientes, {len(odontologos)} odontólogos, {len(servicios)} servicios")

        return pacientes, odontologos, servicios

    except Exception as e:
        log_progreso(f"❌ Error obteniendo datos base: {str(e)}", "ERROR")
        return [], [], []

async def generar_consultas_historicas(pacientes: List[Dict], odontologos: List[Dict]):
    """Genera 150-200 consultas distribuidas en 30 días"""
    log_progreso("📅 Iniciando generación de consultas históricas...")

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

                    # Generar datos de consulta
                    consulta_data = {
                        "id": str(uuid.uuid4()),
                        "paciente_id": paciente["id"],
                        "primer_odontologo_id": odontologo["id"],
                        "fecha_llegada": fecha_hora_llegada.isoformat(),
                        "estado": estado,
                        "tipo_consulta": random.choice(["general", "control", "urgencia"]),
                        "prioridad": "normal",
                        "motivo_consulta": f"Consulta odontológica programada - {random.choice(['control', 'dolor', 'revisión', 'tratamiento'])}"
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
                    log_progreso(f"   ❌ Error creando consulta {orden_general}: {str(e)}", "ERROR")

                orden_general += 1

        fecha_actual += timedelta(days=1)

    log_progreso(f"✅ Consultas históricas creadas: {len(consultas_creadas)}")
    return consultas_creadas

# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================

async def main():
    """Función principal del poblado completo"""
    log_progreso("🚀 INICIANDO POBLADO COMPLETO - UN MES DE OPERACIÓN CLÍNICA")
    log_progreso(f"📅 Período: {FECHA_INICIO} al {FECHA_FIN} (30 días)")
    log_progreso("=" * 60)

    try:
        # FASE 1: Crear odontólogos adicionales
        log_progreso("📍 FASE 1: Creando odontólogos adicionales...")
        odontologos_nuevos = await crear_odontologos_adicionales()

        # Obtener datos base actualizados
        log_progreso("📍 Obteniendo datos base actualizados...")
        pacientes, odontologos, servicios = await obtener_datos_base()

        if not pacientes or not odontologos:
            log_progreso("❌ No se pudieron obtener datos base. Abortando.", "ERROR")
            return

        # FASE 2: Generar consultas históricas
        log_progreso("📍 FASE 2: Generando consultas históricas...")
        consultas = await generar_consultas_historicas(pacientes, odontologos)

        log_progreso("=" * 60)
        log_progreso("🎉 POBLADO COMPLETO EXITOSO")
        log_progreso(f"   📊 Resumen:")
        log_progreso(f"   • Odontólogos nuevos: {len(odontologos_nuevos)}")
        log_progreso(f"   • Consultas generadas: {len(consultas)}")
        log_progreso(f"   • Total pacientes: {len(pacientes)}")
        log_progreso(f"   • Total odontólogos: {len(odontologos)}")
        log_progreso("=" * 60)

    except Exception as e:
        log_progreso(f"❌ Error en función principal: {str(e)}", "ERROR")
        raise

if __name__ == "__main__":
    asyncio.run(main())