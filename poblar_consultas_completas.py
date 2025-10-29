"""
Script para poblar la base de datos con consultas de prueba realistas
Genera consultas en diferentes estados para probar todo el flujo del sistema

ESTADOS GENERADOS:
- 5 consultas en "en_espera"
- 8 consultas en "entre_odontologos"
- 7 consultas "completadas" (4 con pago pendiente, 3 con pago completado)

Total: 20 consultas de prueba
"""

import random
from datetime import datetime, timedelta
from supabase import create_client
from typing import List, Dict, Any

# =====================================================
# CONFIGURACIÓN SUPABASE LOCAL
# =====================================================
SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =====================================================
# DATOS BASE (IDs obtenidos de la BD)
# =====================================================

# IDs de PERSONAL (tabla personal, NO tabla usuarios)
ODONTOLOGOS = [
    'f110064a-846e-4e12-af1c-92ab081d3b94',  # Dr. Luis García
    'c801c016-ada5-4533-96ef-a7ddeb911334',  # Dra. Ana Martinez
    'c8037464-5ad3-4da6-ba37-e17607164422',  # Dr. Carlos Rodriguez
    'fbfc41df-88af-4a49-98b0-b67bc6419f95',  # Dra. María González
    '1d86dfab-5420-499b-bd2e-11aeb4c9f9a7',  # Dr. Pedro Santos
    '0ba2f54e-f63e-49e7-a832-2eae697d8e9d',  # Dra. Sofia Herrera
    '56a2feb9-5b99-48ba-b1f8-5fbe512ab9e6',  # Dr. Ricardo Vargas
    'f13e5c47-84d5-46c5-81f6-755c6e7f4774',  # Dra. Sofia Herrera (2)
]

PACIENTES = [
    '546bb212-d549-492c-a5c1-803d43f69f00',  # HC000001: Gabriel Martínez
    '6948e9de-290c-4781-813e-0d42ecbc88c7',  # HC000002: Rosa Álvarez
    'cbe19a5c-dfc8-4c4b-9342-7f1b2168ad50',  # HC000003: José Fernández
    '50b055af-40e4-4378-bb97-7d332af58e9c',  # HC000004: Teresa Sánchez
    'e04e892e-5e91-422a-99c9-3987302ee7b5',  # HC000005: Rafael Díaz
    '491abeaf-7449-455e-9484-707626c1aca6',  # HC000006: Isabella Ruiz
    '97cd0017-61a1-406f-afaa-b1906156931b',  # HC000007: Ricardo Gutiérrez
    '17190193-78ea-46d2-8a25-bf87a3b86d0f',  # HC000008: Antonio González
    'af9a7d81-65d3-4066-8704-99560f29eb4b',  # HC000009: Diego Álvarez
    'eaaa81ae-6f30-4a22-a417-a48351f2e92e',  # HC000010: Claudia Alonso
    '08b0d19f-df0b-4107-ac85-7a14371759ca',  # HC000011: Alejandro Sánchez
    'a38d7d6e-a7f8-4674-9686-c18b01e603a4',  # HC000012: Patricia Martínez
    '5ca97b83-21de-44f8-a1b3-09870d85cfcf',  # HC000013: Isabel Pérez
    '26798f99-329c-4bde-856f-09f08d40b915',  # HC000014: Francisco López
    '377b3c4d-f9b8-4a70-aeb7-00258b9eb69b',  # HC000015: Fernando Martín
]

# ID del administrador (tabla usuarios)
ADMIN_ID = '6214feee-9786-4d6d-8157-439b1d9e379a'  # admin@odontomara.com

# SERVICIOS con alcance definido
SERVICIOS = {
    '5ae0f1ac-8dac-467c-ae0e-cc243b74380a': {  # OBTU001: Obturación Simple
        'alcance': 'superficie_especifica',
        'precio_bs': 4380.0,
        'precio_usd': 120.0,
        'nombre': 'Obturación Simple'
    },
    '88315f2b-8b5c-4fb4-9b08-37540ef93a49': {  # ENDO001: Endodoncia
        'alcance': 'superficie_especifica',
        'precio_bs': 12775.0,
        'precio_usd': 350.0,
        'nombre': 'Endodoncia'
    },
    'ba4d1129-122e-46e0-9f6d-881cf417007b': {  # CORO001: Corona Dental
        'alcance': 'superficie_especifica',
        'precio_bs': 29200.0,
        'precio_usd': 800.0,
        'nombre': 'Corona Dental'
    },
    '07427cae-6fda-4796-b56e-f15c3411b095': {  # RADI001: Radiografía Panorámica
        'alcance': 'superficie_especifica',
        'precio_bs': 2190.0,
        'precio_usd': 60.0,
        'nombre': 'Radiografía Panorámica'
    },
    'c9a9e1cc-f6eb-4cce-bdf3-50e112e6938b': {  # EXTR001: Extracción Simple
        'alcance': 'diente_completo',
        'precio_bs': 2920.0,
        'precio_usd': 80.0,
        'nombre': 'Extracción Simple'
    },
    'f889dbaa-e449-4b74-9097-c61f94b16b7e': {  # EXTR002: Extracción Compleja
        'alcance': 'diente_completo',
        'precio_bs': 5475.0,
        'precio_usd': 150.0,
        'nombre': 'Extracción Compleja'
    },
    'edee7290-aa68-41c7-82aa-6bba097799fb': {  # IMPL001: Implante Dental
        'alcance': 'diente_completo',
        'precio_bs': 73000.0,
        'precio_usd': 2000.0,
        'nombre': 'Implante Dental'
    },
    '208019f4-29b1-4062-8c6a-c79129096386': {  # LIMP001: Profilaxis Dental
        'alcance': 'boca_completa',
        'precio_bs': 2920.0,
        'precio_usd': 80.0,
        'nombre': 'Profilaxis Dental'
    },
}

MOTIVOS_CONSULTA = [
    "Control odontológico de rutina",
    "Dolor en molar superior derecho",
    "Revisión de tratamiento anterior",
    "Sensibilidad dental al frío",
    "Fractura de diente frontal",
    "Limpieza dental programada",
    "Dolor al masticar",
    "Sangrado de encías",
    "Consulta estética dental",
    "Evaluación para ortodoncia",
]

DIENTES_FDI = [
    # Cuadrante 1 (superior derecho)
    11, 12, 13, 14, 15, 16, 17, 18,
    # Cuadrante 2 (superior izquierdo)
    21, 22, 23, 24, 25, 26, 27, 28,
    # Cuadrante 3 (inferior izquierdo)
    31, 32, 33, 34, 35, 36, 37, 38,
    # Cuadrante 4 (inferior derecho)
    41, 42, 43, 44, 45, 46, 47, 48,
]

SUPERFICIES = ["oclusal", "mesial", "distal", "vestibular", "lingual"]

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def obtener_usuario_admin():
    """Obtener ID del administrador para 'creada_por'"""
    return ADMIN_ID

def generar_numero_consulta():
    """Generar número de consulta único"""
    # Obtener último número
    response = supabase.table("consultas").select("numero_consulta").order("numero_consulta", desc=True).limit(1).execute()
    if response.data and response.data[0].get("numero_consulta"):
        ultimo_numero = int(response.data[0]["numero_consulta"].replace("CON", ""))
        return f"CON{ultimo_numero + 1:06d}"
    else:
        return "CON000001"

def calcular_costos_intervencion(servicio_id: str, alcance: str, dientes_afectados: int = 1, superficies_afectadas: int = 1) -> Dict[str, float]:
    """
    Calcula los costos según el alcance del servicio

    IMPORTANTE: Evitar el problema de 160 registros
    - boca_completa: 1 registro total
    - diente_completo: 1 registro por diente
    - superficie_especifica: 1 registro por superficie
    """
    servicio = SERVICIOS[servicio_id]

    if alcance == "boca_completa":
        # Un solo cargo por toda la boca
        return {
            "precio_final_bs": servicio["precio_bs"], # Clave en BS
            "precio_final_usd": servicio["precio_usd"], # ✅ CLAVE AGREGADA
            "cantidad_registros": 1
        }
    elif alcance == "diente_completo":
        # Un cargo por cada diente afectado
        return {
            "precio_final_bs": servicio["precio_bs"] * dientes_afectados, # Clave en BS
            "precio_final_usd": servicio["precio_usd"] * dientes_afectados, # ✅ CLAVE AGREGADA
            "cantidad_registros": dientes_afectados
        }
    else:  # superficie_especifica
        # Un cargo por cada superficie afectada
        return {
            "precio_final_bs": servicio["precio_bs"] * superficies_afectadas, # Clave en BS
            "precio_final_usd": servicio["precio_usd"] * superficies_afectadas, # ✅ CLAVE AGREGADA
            "cantidad_registros": superficies_afectadas
        }

# =====================================================
# CREAR CONSULTAS EN DIFERENTES ESTADOS
# =====================================================

def crear_consulta_en_espera(paciente_id: str, odontologo_id: str, admin_id: str) -> Dict[str, Any]:
    """
    Crear consulta en estado 'en_espera'
    Sin intervenciones realizadas
    """
    numero_consulta = generar_numero_consulta()
    fecha_llegada = datetime.now() - timedelta(minutes=random.randint(10, 120))

    consulta_data = {
        "numero_consulta": numero_consulta,
        "paciente_id": paciente_id,
        "primer_odontologo_id": odontologo_id,
        "fecha_llegada": fecha_llegada.isoformat(),
        "orden_llegada_general": random.randint(1, 50),
        "orden_cola_odontologo": random.randint(1, 10),
        "estado": "en_espera",
        "tipo_consulta": random.choice(["general", "control", "urgencia"]),
        "prioridad": random.choice(["normal", "urgente"]),
        "motivo_consulta": random.choice(MOTIVOS_CONSULTA),
        "costo_total_bs": 0.0,
        "costo_total_usd": 0.0,
        "creada_por": admin_id,
    }

    response = supabase.table("consultas").insert(consulta_data).execute()
    print(f"[OK] Consulta EN_ESPERA creada: {numero_consulta}")
    return response.data[0] if response.data else None

def crear_consulta_entre_odontologos(paciente_id: str, odontologo_id: str, admin_id: str) -> Dict[str, Any]:
    """
    Crear consulta en estado 'entre_odontologos'
    Mínimo 1 intervención completada
    Servicios aplicados (respetando alcance)
    """
    numero_consulta = generar_numero_consulta()
    fecha_llegada = datetime.now() - timedelta(hours=random.randint(1, 4))

    # Crear consulta base
    consulta_data = {
        "numero_consulta": numero_consulta,
        "paciente_id": paciente_id,
        "primer_odontologo_id": odontologo_id,
        "fecha_llegada": fecha_llegada.isoformat(),
        "orden_llegada_general": random.randint(1, 50),
        "orden_cola_odontologo": random.randint(1, 10),
        "estado": "entre_odontologos",  # ✨ Estado clave
        "tipo_consulta": random.choice(["general", "control"]),
        "prioridad": "normal",
        "motivo_consulta": random.choice(MOTIVOS_CONSULTA),
        "costo_total_bs": 0.0,
        "costo_total_usd": 0.0,
        "creada_por": admin_id,
    }

    response_consulta = supabase.table("consultas").insert(consulta_data).execute()
    consulta = response_consulta.data[0] if response_consulta.data else None

    if not consulta:
        print("[ERROR] Error al crear consulta entre_odontologos")
        return None

    # Crear 1-2 intervenciones completadas
    num_intervenciones = random.randint(1, 2)
    costo_total_bs = 0.0
    costo_total_usd = 0.0

    for i in range(num_intervenciones):
        # Seleccionar servicio aleatorio
        servicio_id = random.choice(list(SERVICIOS.keys()))
        servicio = SERVICIOS[servicio_id]
        alcance = servicio["alcance"]

        # Calcular costos según alcance
        if alcance == "boca_completa":
            costos = calcular_costos_intervencion(servicio_id, alcance)
            dientes_afectados = None
            superficie = None
        elif alcance == "diente_completo":
            num_dientes = random.randint(1, 3)
            costos = calcular_costos_intervencion(servicio_id, alcance, dientes_afectados=num_dientes)
            dientes_afectados = ','.join([str(random.choice(DIENTES_FDI)) for _ in range(num_dientes)])
            superficie = None
        else:  # superficie_especifica
            num_superficies = random.randint(1, 3)
            costos = calcular_costos_intervencion(servicio_id, alcance, superficies_afectadas=num_superficies)
            dientes_afectados = str(random.choice(DIENTES_FDI))
            superficie = random.choice(SUPERFICIES)

        costo_total_bs += costos["precio_final_bs"]
        costo_total_usd += costos["precio_final_usd"]

        # Crear intervención
        intervencion_data = {
            "consulta_id": consulta["id"],
            "odontologo_id": odontologo_id,
            "servicio_id": servicio_id,
            "hora_inicio": fecha_llegada.isoformat(),
            "hora_fin": (fecha_llegada + timedelta(minutes=random.randint(20, 60))).isoformat(),
            "estado": "completada",
            "dientes_afectados": dientes_afectados,
            "superficie": superficie,
            "procedimiento_realizado": f"Intervención {i+1}: {servicio['nombre']} aplicada correctamente",
            "total_bs": costos["precio_final_bs"], # ✅ CLAVE AGREGADA
            "total_usd": costos["precio_final_usd"], # ✅ CLAVE AGREGADA
        }

        supabase.table("intervenciones").insert(intervencion_data).execute()

    # Actualizar costos de la consulta
    supabase.table("consultas").update({
        "costo_total_bs": costo_total_bs,
        "costo_total_usd": costo_total_usd
    }).eq("id", consulta["id"]).execute()

    print(f"[OK] Consulta ENTRE_ODONTOLOGOS creada: {numero_consulta} (BS{costo_total_bs:.2f} / USD{costo_total_usd:.2f})")
    return consulta

def crear_consulta_completada(paciente_id: str, odontologos: List[str], admin_id: str, con_pago: bool = False) -> Dict[str, Any]:
    """
    Crear consulta en estado 'completada'
    Múltiples intervenciones de diferentes odontólogos
    Opcionalmente con pago (pendiente o completado)
    """
    numero_consulta = generar_numero_consulta()
    fecha_llegada = datetime.now() - timedelta(days=random.randint(1, 30))

    # Crear consulta base
    consulta_data = {
        "numero_consulta": numero_consulta,
        "paciente_id": paciente_id,
        "primer_odontologo_id": odontologos[0],
        "fecha_llegada": fecha_llegada.isoformat(),
        "orden_llegada_general": random.randint(1, 50),
        "orden_cola_odontologo": random.randint(1, 10),
        "estado": "completada",  # ✨ Estado clave
        "tipo_consulta": random.choice(["general", "control"]),
        "prioridad": "normal",
        "motivo_consulta": random.choice(MOTIVOS_CONSULTA),
        "costo_total_bs": 0.0,
        "costo_total_usd": 0.0,
        "creada_por": admin_id,
    }

    response_consulta = supabase.table("consultas").insert(consulta_data).execute()
    consulta = response_consulta.data[0] if response_consulta.data else None

    if not consulta:
        print("[ERROR] Error al crear consulta completada")
        return None

    # Crear 2-4 intervenciones de diferentes odontólogos
    num_intervenciones = random.randint(2, min(4, len(odontologos)))
    costo_total_bs = 0.0
    costo_total_usd = 0.0

    for i in range(num_intervenciones):
        odontologo_id = odontologos[i % len(odontologos)]

        # Seleccionar servicio aleatorio
        servicio_id = random.choice(list(SERVICIOS.keys()))
        servicio = SERVICIOS[servicio_id]
        alcance = servicio["alcance"]

        # Calcular costos según alcance
        if alcance == "boca_completa":
            costos = calcular_costos_intervencion(servicio_id, alcance)
            dientes_afectados = None
            superficie = None
        elif alcance == "diente_completo":
            num_dientes = random.randint(1, 2)
            costos = calcular_costos_intervencion(servicio_id, alcance, dientes_afectados=num_dientes)
            dientes_afectados = ','.join([str(random.choice(DIENTES_FDI)) for _ in range(num_dientes)])
            superficie = None
        else:  # superficie_especifica
            num_superficies = random.randint(1, 2)
            costos = calcular_costos_intervencion(servicio_id, alcance, superficies_afectadas=num_superficies)
            dientes_afectados = str(random.choice(DIENTES_FDI))
            superficie = random.choice(SUPERFICIES)

        costo_total_bs += costos["precio_final_bs"]
        costo_total_usd += costos["precio_final_usd"]

        # Crear intervención
        fecha_inicio_intervencion = fecha_llegada + timedelta(minutes=i*30)
        intervencion_data = {
            "consulta_id": consulta["id"],
            "odontologo_id": odontologo_id,
            "servicio_id": servicio_id,
            "hora_inicio": fecha_inicio_intervencion.isoformat(),
            "hora_fin": (fecha_inicio_intervencion + timedelta(minutes=random.randint(30, 90))).isoformat(),
            "estado": "completada",
            "dientes_afectados": dientes_afectados,
            "superficie": superficie,
            "procedimiento_realizado": f"Intervención {i+1}: {servicio['nombre']}",
            "total_bs": costos["precio_final_bs"], # ✅ CLAVE AGREGADA
            "total_usd": costos["precio_final_usd"], # ✅ CLAVE AGREGADA
        }

        supabase.table("intervenciones").insert(intervencion_data).execute()

    # Actualizar costos de la consulta
    supabase.table("consultas").update({
        "costo_total_bs": costo_total_bs,
        "costo_total_usd": costo_total_usd
    }).eq("id", consulta["id"]).execute()

    # Crear registro de pago si corresponde
    estado_pago = "sin_pago"
    if con_pago:
        tasa_cambio = round(random.uniform(35.0, 37.0), 2)

        # Decidir si pago está completado o pendiente
        pago_completado = random.choice([True, False])

        if pago_completado:
            # Pago completo
            monto_pagado_bs = costo_total_bs
            monto_pagado_usd = costo_total_usd
            estado_pago = "completado"
        else:
            # Pago parcial (50-80% del total)
            porcentaje_pago = random.uniform(0.5, 0.8)
            monto_pagado_bs = round(costo_total_bs * porcentaje_pago, 2)
            monto_pagado_usd = round(costo_total_usd * porcentaje_pago, 2)
            estado_pago = "pendiente"

        pago_data = {
            "consulta_id": consulta["id"],
            "paciente_id": paciente_id,
            "monto_total_bs": costo_total_bs,
            "monto_total_usd": costo_total_usd,
            "monto_pagado_bs": monto_pagado_bs,
            "monto_pagado_usd": monto_pagado_usd,
            "saldo_pendiente_bs": costo_total_bs - monto_pagado_bs,
            "saldo_pendiente_usd": costo_total_usd - monto_pagado_usd,
            "estado": estado_pago,
            "metodo_pago": random.choice(["efectivo", "transferencia", "tarjeta"]),
            "tasa_cambio": tasa_cambio,
            "fecha_pago": (fecha_llegada + timedelta(hours=random.randint(1, 24))).isoformat(),
            "registrado_por": admin_id,
        }

        supabase.table("pagos").insert(pago_data).execute()

    print(f"[OK] Consulta COMPLETADA creada: {numero_consulta} (BS{costo_total_bs:.2f} / USD{costo_total_usd:.2f}) - Pago: {estado_pago}")
    return consulta

# =====================================================
# SCRIPT PRINCIPAL
# =====================================================

def main():
    print("="*60)
    print("SCRIPT DE POBLAMIENTO DE CONSULTAS")
    print("="*60)

    admin_id = obtener_usuario_admin()
    if not admin_id:
        print("[ERROR] No se encontro usuario administrador")
        return

    print(f"\nConfiguracion:")
    print(f"   - Odontologos disponibles: {len(ODONTOLOGOS)}")
    print(f"   - Pacientes disponibles: {len(PACIENTES)}")
    print(f"   - Servicios configurados: {len(SERVICIOS)}")
    print(f"   - Admin ID: {admin_id[:8]}...")

    # Contador de consultas creadas
    consultas_creadas = {
        "en_espera": 0,
        "entre_odontologos": 0,
        "completadas_sin_pago": 0,
        "completadas_con_pago_pendiente": 0,
        "completadas_con_pago_completo": 0,
    }

    print("\n" + "="*60)
    print("[1] CREANDO CONSULTAS EN ESPERA (5)")
    print("="*60)

    for i in range(5):
        paciente_id = random.choice(PACIENTES)
        odontologo_id = random.choice(ODONTOLOGOS)
        crear_consulta_en_espera(paciente_id, odontologo_id, admin_id)
        consultas_creadas["en_espera"] += 1

    print("\n" + "="*60)
    print("[2] CREANDO CONSULTAS ENTRE ODONTOLOGOS (8)")
    print("="*60)

    for i in range(8):
        paciente_id = random.choice(PACIENTES)
        odontologo_id = random.choice(ODONTOLOGOS)
        crear_consulta_entre_odontologos(paciente_id, odontologo_id, admin_id)
        consultas_creadas["entre_odontologos"] += 1

    print("\n" + "="*60)
    print("[3] CREANDO CONSULTAS COMPLETADAS (7)")
    print("="*60)

    # 4 con pago pendiente
    for i in range(4):
        paciente_id = random.choice(PACIENTES)
        odontologos_seleccionados = random.sample(ODONTOLOGOS, random.randint(2, 3))
        crear_consulta_completada(paciente_id, odontologos_seleccionados, admin_id, con_pago=True)
        consultas_creadas["completadas_con_pago_pendiente"] += 1

    # 3 con pago completado
    for i in range(3):
        paciente_id = random.choice(PACIENTES)
        odontologos_seleccionados = random.sample(ODONTOLOGOS, random.randint(2, 3))
        crear_consulta_completada(paciente_id, odontologos_seleccionados, admin_id, con_pago=True)
        consultas_creadas["completadas_con_pago_completo"] += 1

    print("\n" + "="*60)
    print("[OK] RESUMEN DE POBLACION COMPLETADA")
    print("="*60)
    print(f"   [+] Consultas en espera: {consultas_creadas['en_espera']}")
    print(f"   [+] Consultas entre odontologos: {consultas_creadas['entre_odontologos']}")
    print(f"   [+] Consultas completadas con pago pendiente: {consultas_creadas['completadas_con_pago_pendiente']}")
    print(f"   [+] Consultas completadas con pago completo: {consultas_creadas['completadas_con_pago_completo']}")
    print(f"\n   [*] TOTAL: {sum(consultas_creadas.values())} consultas creadas")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error durante la ejecucion: {e}")
        import traceback
        traceback.print_exc()
