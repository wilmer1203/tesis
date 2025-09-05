#!/usr/bin/env python3
"""
🚀 POBLADO SIMPLE - DIRECTO A BASE DE DATOS
==========================================

Versión simplificada que inserta directamente en la BD
sin usar servicios ni crear usuarios Auth.
"""

import asyncio
import random
from datetime import datetime, date, timedelta
import uuid
from dental_system.supabase.client import supabase_client

# Obtener cliente
supabase = supabase_client.get_client()

# =====================================================
# 🎭 DATOS FICTICIOS
# =====================================================

NOMBRES_MASCULINOS = ["Carlos", "José", "Luis", "Miguel", "Rafael", "Roberto", "Fernando"]
NOMBRES_FEMENINOS = ["María", "Carmen", "Ana", "Rosa", "Patricia", "Gabriela", "Isabel"]
APELLIDOS = ["García", "Rodríguez", "González", "Martínez", "López", "Hernández", "Pérez"]
CIUDADES = ["Puerto La Cruz", "Barcelona", "Caracas", "Valencia", "Maracaibo"]
MOTIVOS_CONSULTA = ["Dolor de muela", "Limpieza dental", "Control rutinario", "Caries", "Sangrado encías"]

class PobladorSimple:
    def __init__(self):
        print("🚀 Poblador Simple - Inserción directa en BD")
        
    async def poblar_todo(self):
        """🎯 Poblar todo directamente en BD"""
        try:
            print("\n📋 INICIANDO POBLADO SIMPLE...")
            
            # 1. Verificar roles existentes
            await self.verificar_roles()
            
            # 2. Crear personal básico (sin auth)
            personal_ids = await self.crear_personal_basico()
            
            # 3. Crear pacientes básicos
            pacientes_ids = await self.crear_pacientes_basicos()
            
            # 4. Crear consultas para hoy
            if personal_ids and pacientes_ids:
                await self.crear_consultas_hoy(personal_ids, pacientes_ids)
            
            print("\n🎉 POBLADO SIMPLE COMPLETADO")
            print(f"👥 Personal: {len(personal_ids)}")
            print(f"🏥 Pacientes: {len(pacientes_ids)}")
            
        except Exception as e:
            print(f"❌ Error en poblado: {e}")
            
    async def verificar_roles(self):
        """🔍 Verificar que existan roles en BD"""
        try:
            roles = supabase.table("roles").select("*").execute()
            if roles.data:
                print(f"✅ Roles encontrados: {len(roles.data)}")
                for rol in roles.data:
                    print(f"   - {rol['nombre']}")
            else:
                print("⚠️ No hay roles en BD, creando básicos...")
                await self.crear_roles_basicos()
        except Exception as e:
            print(f"❌ Error verificando roles: {e}")
            
    async def crear_roles_basicos(self):
        """👔 Crear roles básicos si no existen"""
        try:
            roles_data = [
                {
                    "id": str(uuid.uuid4()),
                    "nombre": "gerente", 
                    "descripcion": "Acceso completo",
                    "permisos": {"all": True}
                },
                {
                    "id": str(uuid.uuid4()),
                    "nombre": "odontologo", 
                    "descripcion": "Atención clínica",
                    "permisos": {"consultas": True, "pacientes": True}
                },
                {
                    "id": str(uuid.uuid4()),
                    "nombre": "administrador", 
                    "descripcion": "Gestión administrativa",
                    "permisos": {"consultas": True, "pacientes": True}
                }
            ]
            
            result = supabase.table("roles").insert(roles_data).execute()
            if result.data:
                print(f"✅ Roles básicos creados: {len(result.data)}")
                
        except Exception as e:
            print(f"❌ Error creando roles: {e}")
    
    async def crear_personal_basico(self):
        """👨‍⚕️ Crear personal básico (sin usuarios Auth)"""
        print("\n👨‍⚕️ Creando personal básico...")
        
        try:
            # Obtener rol de odontólogo
            rol_result = supabase.table("roles").select("id").eq("nombre", "odontologo").execute()
            if not rol_result.data:
                print("❌ No se encontró rol odontologo")
                return []
            
            rol_odontologo_id = rol_result.data[0]["id"]
            
            # Crear 3 odontólogos básicos
            odontologos_data = []
            
            for i in range(3):
                # Usuario básico (sin auth)
                usuario_id = str(uuid.uuid4())
                usuario_data = {
                    "id": usuario_id,
                    "email": f"odontologo{i+1}@clinica.com",
                    "rol_id": rol_odontologo_id,
                    "activo": True,
                    "metadata": {"tipo": "datos_prueba"}
                }
                
                # Insertar usuario
                user_result = supabase.table("usuarios").insert(usuario_data).execute()
                
                if user_result.data:
                    # Crear registro de personal
                    nombres = random.choice(NOMBRES_MASCULINOS + NOMBRES_FEMENINOS)
                    apellido = random.choice(APELLIDOS)
                    
                    personal_data = {
                        "id": str(uuid.uuid4()),
                        "usuario_id": usuario_id,
                        "primer_nombre": nombres,
                        "primer_apellido": apellido,
                        "numero_documento": f"1234567{i}",
                        "celular": f"+58 281-123-456{i}",
                        "tipo_personal": "Odontólogo",
                        "especialidad": ["Endodoncia", "Periodoncia", "Cirugía"][i],
                        "estado_laboral": "activo",
                        "acepta_pacientes_nuevos": True
                    }
                    
                    personal_result = supabase.table("personal").insert(personal_data).execute()
                    
                    if personal_result.data:
                        odontologos_data.append(personal_result.data[0]["id"])
                        print(f"   ✅ Odontólogo {i+1}: Dr. {nombres} {apellido}")
            
            return odontologos_data
            
        except Exception as e:
            print(f"❌ Error creando personal: {e}")
            return []
    
    async def crear_pacientes_basicos(self):
        """👥 Crear pacientes básicos"""
        print("\n👥 Creando pacientes básicos...")
        
        try:
            pacientes_ids = []
            
            for i in range(10):
                # Generar datos realistas
                es_masculino = random.choice([True, False])
                nombres = NOMBRES_MASCULINOS if es_masculino else NOMBRES_FEMENINOS
                
                nombre = random.choice(nombres)
                apellido = random.choice(APELLIDOS)
                documento = f"2000000{i:02d}"
                
                paciente_data = {
                    "id": str(uuid.uuid4()),
                    "primer_nombre": nombre,
                    "primer_apellido": apellido,
                    "numero_documento": documento,
                    "tipo_documento": "CI",
                    "genero": "masculino" if es_masculino else "femenino",
                    "celular_1": f"+58 281-987-65{i:02d}",
                    "direccion": f"Calle {i+1}, {random.choice(CIUDADES)}",
                    "fecha_nacimiento": (date.today() - timedelta(days=random.randint(6000, 25000))).isoformat(),
                    "activo": True
                }
                
                result = supabase.table("pacientes").insert(paciente_data).execute()
                
                if result.data:
                    pacientes_ids.append(result.data[0]["id"])
                    if i % 3 == 0:
                        print(f"   ✅ Creados {i+1} pacientes...")
            
            print(f"✅ Total pacientes creados: {len(pacientes_ids)}")
            return pacientes_ids
            
        except Exception as e:
            print(f"❌ Error creando pacientes: {e}")
            return []
    
    async def crear_consultas_hoy(self, personal_ids, pacientes_ids):
        """📅 Crear consultas para hoy"""
        print("\n📅 Creando consultas para hoy...")
        
        try:
            horas = ["08:30", "09:00", "09:30", "10:00", "10:30", 
                    "14:00", "14:30", "15:00", "15:30", "16:00"]
            
            for i in range(8):
                consulta_data = {
                    "id": str(uuid.uuid4()),
                    "paciente_id": random.choice(pacientes_ids),
                    "primer_odontologo_id": random.choice(personal_ids),
                    "fecha_llegada": f"{date.today()} {random.choice(horas)}:00",
                    "motivo_consulta": random.choice(MOTIVOS_CONSULTA),
                    "tipo_consulta": "general",
                    "estado": "en_espera",
                    "prioridad": "normal"
                }
                
                result = supabase.table("consultas").insert(consulta_data).execute()
                
                if result.data:
                    print(f"   ✅ Consulta {i+1}: {consulta_data['motivo_consulta']}")
            
        except Exception as e:
            print(f"❌ Error creando consultas: {e}")

async def main():
    """🎬 Ejecutar poblado simple"""
    print("🏥 POBLADO SIMPLE - CLÍNICA DENTAL")
    print("="*40)
    
    poblador = PobladorSimple()
    await poblador.poblar_todo()
    
    print("\n✅ LISTO PARA USAR")
    print("🔗 Ejecuta 'reflex run' para ver el sistema")

if __name__ == "__main__":
    asyncio.run(main())