#!/usr/bin/env python3
"""
POBLADOR DE PACIENTES CON ECOSISTEMA COMPLETO - VERSION SIN EMOJIS
Crea múltiples pacientes usando el nuevo sistema de inicialización automática
"""

import asyncio
import random
from datetime import datetime, date, timedelta
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dental_system.services.pacientes_service import PacientesService
from dental_system.models.pacientes_models import PacienteFormModel

# IDs REALES DE USUARIOS Y PERSONAL (los que me diste)
USER_IDS = [
    "0077e929-327c-43ae-9495-25918db10b72",
    "f2324186-6d7c-4a78-8258-36855fad23dd"
]

PERSONAL_IDS = [
    "db443ae0-b106-404f-abdd-8f05f6090cf6",
    "b2aa6bd5-d57e-4c09-b7af-1b1a0c06847f"
]

# DATOS FICTICIOS REALISTAS
NOMBRES_MASCULINOS = [
    "Carlos", "José", "Luis", "Miguel", "Rafael", "Antonio", "Francisco",
    "Manuel", "Jesús", "Daniel", "Pedro", "Juan", "Fernando", "Roberto",
    "Alejandro", "Diego", "Andrés", "Gabriel", "David", "Ricardo"
]

NOMBRES_FEMENINOS = [
    "María", "Carmen", "Ana", "Rosa", "Teresa", "Isabel", "Patricia",
    "Claudia", "Sofía", "Gabriela", "Alejandra", "Daniela", "Andrea",
    "Valentina", "Isabella", "Victoria", "Camila", "Natalia", "Carolina"
]

APELLIDOS = [
    "García", "Rodríguez", "González", "Fernández", "López", "Martínez",
    "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández",
    "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez"
]

CIUDADES_VENEZUELA = [
    "Puerto La Cruz", "Barcelona", "Caracas", "Maracaibo", "Valencia",
    "Barquisimeto", "Maracay", "Ciudad Guayana", "San Cristóbal", "Maturín"
]

async def crear_pacientes_masivos():
    """Crear múltiples pacientes con ecosistema completo"""

    print("POBLADOR DE PACIENTES CON ECOSISTEMA MEDICO COMPLETO")
    print("=" * 60)
    print("EXITO: Cada paciente incluye:")
    print("   - Historia Clinica automatica (HC000001, HC000002...)")
    print("   - Odontograma FDI completo (32 dientes marcados como 'sano')")
    print("   - Historial medico inicial")
    print("   - Auditoria completa del proceso")
    print("=" * 60)

    # Pregunta cuántos pacientes crear
    try:
        cantidad = int(input("CANTIDAD: Cuantos pacientes crear? (recomendado 10-20): "))
        if cantidad <= 0 or cantidad > 50:
            print("ERROR: Cantidad invalida. Usando 10 por defecto.")
            cantidad = 10
    except ValueError:
        print("ERROR: Numero invalido. Usando 10 por defecto.")
        cantidad = 10

    print(f"\nINICIANDO: Creando {cantidad} pacientes con ecosistema completo...")

    # Inicializar servicio
    pacientes_service = PacientesService()

    # Configurar contexto como usuario admin (necesario para permisos)
    mock_admin_profile = {
        "rol": {"nombre": "administrador", "permisos": {"pacientes": ["crear", "leer", "actualizar", "eliminar"]}}
    }
    pacientes_service.set_user_context(USER_IDS[0], mock_admin_profile)

    pacientes_creados = []
    errores = []

    for i in range(cantidad):
        try:
            # Generar datos aleatorios
            es_masculino = random.choice([True, False])
            nombres = NOMBRES_MASCULINOS if es_masculino else NOMBRES_FEMENINOS

            nombre1 = random.choice(nombres)
            nombre2 = random.choice(nombres) if random.random() > 0.4 else None
            apellido1 = random.choice(APELLIDOS)
            apellido2 = random.choice(APELLIDOS)

            # NOTA: PacienteFormModel espera STRINGS, no listas ni None
            paciente_data = {
                "numero_documento": f"{random.randint(10000000, 30000000)}",
                "primer_nombre": nombre1,
                "segundo_nombre": nombre2 if nombre2 else "",  # String vacío en vez de None
                "primer_apellido": apellido1,
                "segundo_apellido": apellido2,
                "tipo_documento": "CI",
                "genero": "masculino" if es_masculino else "femenino",
                "fecha_nacimiento": generar_fecha_nacimiento(),
                "celular_1": f"0{random.randint(281, 424)}{random.randint(1000000, 9999999)}",
                "celular_2": f"0{random.randint(281, 424)}{random.randint(1000000, 9999999)}" if random.random() > 0.6 else "",  # String vacío en vez de None
                "email": f"{nombre1.lower().replace(' ', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')}{random.randint(1, 999)}@gmail.com",
                "direccion": f"Calle {random.randint(1, 100)}, {random.choice(CIUDADES_VENEZUELA)}",
                "ciudad": random.choice(CIUDADES_VENEZUELA),
                "ocupacion": random.choice(["Empleado", "Comerciante", "Estudiante", "Profesional", "Jubilado"]),
                "estado_civil": random.choice(["soltero", "casado", "divorciado", "viudo"]),

                # Contacto de emergencia - campos separados que espera el FormModel
                "contacto_emergencia_nombre": f"{random.choice(nombres)} {random.choice(APELLIDOS)}",
                "contacto_emergencia_telefono": f"0{random.randint(281, 424)}{random.randint(1000000, 9999999)}",
                "contacto_emergencia_relacion": random.choice(["Esposo/a", "Hijo/a", "Padre/Madre"]),

                # Información médica como STRINGS separados por comas (no listas)
                "alergias": "Ninguna conocida" if random.random() > 0.3 else random.choice(["Penicilina", "Lidocaina", "Latex"]),
                "condiciones_medicas": "Ninguna conocida" if random.random() > 0.4 else random.choice(["Hipertension", "Diabetes", "Asma"]),
                "observaciones_medicas": "",
                "medicamentos_actuales": "",
                "antecedentes_familiares": "",
                "activo": True
            }

            # CREAR PACIENTE CON ECOSISTEMA COMPLETO
            # Convertir dict a modelo tipado
            paciente_form = PacienteFormModel(**paciente_data)
            resultado = await pacientes_service.create_patient(paciente_form, random.choice(USER_IDS))

            if resultado:
                hc = resultado.numero_historia
                nombre_completo = f"{nombre1} {apellido1}"
                pacientes_creados.append({
                    "hc": hc,
                    "nombre": nombre_completo
                })
                print(f"   EXITO {i+1:2d}. {hc} - {nombre_completo}")
            else:
                errores.append(f"Paciente {i+1}: Error en la creacion")
                print(f"   ERROR {i+1:2d}. Error en la creacion")

        except Exception as e:
            errores.append(f"Paciente {i+1}: {str(e)}")
            print(f"   ERROR {i+1:2d}. Error inesperado: {e}")

    # RESUMEN FINAL
    print("\n" + "=" * 60)
    print("RESUMEN DE CREACION")
    print("=" * 60)
    print(f"EXITO: Pacientes creados exitosamente: {len(pacientes_creados)}")
    print(f"ERROR: Errores encontrados: {len(errores)}")

    if pacientes_creados:
        print("\nPACIENTES CREADOS:")
        for paciente in pacientes_creados:
            print(f"   HC: {paciente['hc']} - {paciente['nombre']}")

    if errores:
        print("\nERRORES ENCONTRADOS:")
        for error in errores[:5]:  # Solo primeros 5 errores
            print(f"   ERROR: {error}")
        if len(errores) > 5:
            print(f"   ... y {len(errores) - 5} errores mas")

    print(f"\nPROCESO COMPLETADO")
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Tasa de exito: {len(pacientes_creados)}/{cantidad} ({(len(pacientes_creados)/cantidad)*100:.1f}%)")

    if len(pacientes_creados) > 0:
        print(f"\nNOTA: Cada paciente tiene:")
        print(f"   DIENTES: Odontograma FDI con 32 dientes marcados como 'sano'")
        print(f"   HISTORIAL: Historial medico inicial")
        print(f"   AUDITORIA: Auditoria completa del proceso de creacion")

def generar_fecha_nacimiento():
    """Generar fecha de nacimiento realista"""
    inicio = date.today() - timedelta(days=365*80)  # 80 años atrás
    fin = date.today() - timedelta(days=365*18)     # 18 años atrás
    dias = (fin - inicio).days
    fecha = inicio + timedelta(days=random.randint(0, dias))
    return fecha.isoformat()

if __name__ == "__main__":
    print("POBLADOR DE PACIENTES CON ECOSISTEMA MEDICO COMPLETO")
    print("Sistema Dental - Universidad de Oriente")
    print("-" * 50)
    asyncio.run(crear_pacientes_masivos())