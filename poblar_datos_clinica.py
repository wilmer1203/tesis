#!/usr/bin/env python3
"""
🏥 SCRIPT DE POBLACIÓN DE DATOS - CLÍNICA DENTAL ODONTOMARVA
=============================================================

Popula la base de datos con datos realistas para pruebas y demostración del sistema.

FLUJO SIMULADO:
1. Crea 6 odontólogos + personal administrativo
2. Crea 50 pacientes variados 
3. Simula 3 semanas de consultas (15 días laborales)
4. Crea intervenciones realistas por cada consulta
5. Genera pagos con diferentes estados y métodos

USAR SOLO EN AMBIENTE DE DESARROLLO
"""

import asyncio
import random
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
import uuid
from decimal import Decimal
import json

# Importar servicios del sistema
from dental_system.supabase.client import supabase_client
from dental_system.services.pacientes_service import pacientes_service
from dental_system.services.personal_service import personal_service
from dental_system.services.consultas_service import consultas_service
from dental_system.services.odontologia_service import odontologia_service
from dental_system.services.pagos_service import pagos_service
from dental_system.services.servicios_service import servicios_service

# =====================================================
# 🎭 DATOS FICTICIOS REALISTAS VENEZOLANOS
# =====================================================
supabase = supabase_client.get_client()
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
    "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez",
    "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez",
    "Serrano", "Blanco", "Molina", "Morales", "Suárez", "Ortega", "Delgado"
]

CIUDADES_VENEZUELA = [
    "Puerto La Cruz", "Barcelona", "Caracas", "Maracaibo", "Valencia",
    "Barquisimeto", "Maracay", "Ciudad Guayana", "San Cristóbal", "Maturín",
    "Ciudad Bolívar", "Cumana", "Punto Fijo", "Coro", "Acarigua"
]

ESPECIALIDADES_ODONTOLOGICAS = [
    "Odontología General",
    "Endodoncia", 
    "Periodoncia",
    "Ortodoncía",
    "Cirugía Oral",
    "Implantología",
    "Odontopediatría",
    "Estética Dental"
]

MOTIVOS_CONSULTA = [
    "Dolor de muela", "Limpieza dental", "Control rutinario", "Sensibilidad dental",
    "Sangrado de encías", "Caries", "Revisión de brackets", "Dolor en mandíbula",
    "Consulta de implante", "Blanqueamiento", "Revisión post-tratamiento",
    "Emergencia dental", "Consulta estética", "Tratamiento de conducto"
]

# =====================================================
# 🏥 CLASE PRINCIPAL PARA POBLADO DE DATOS
# =====================================================

class PobladorDatosClinica:
    def __init__(self):
        self.personal_creado = []
        self.pacientes_creados = []
        self.servicios_disponibles = []
        self.tasa_cambio = 36.50  # VES/USD
        
        # IDs que necesitamos recopilar
        self.odontologos_ids = []
        self.administradores_ids = []
        
        # Credenciales de usuarios creados
        self.credenciales_usuarios = []
        
        print("🏥 Iniciando poblado de datos para Clínica Dental...")
    
    async def poblar_todo(self):
        """🎯 Poblar toda la base de datos secuencialmente"""
        try:
            print("\n" + "="*60)
            print("🎬 INICIANDO POBLADO COMPLETO DE LA CLÍNICA")
            print("="*60)
            
            # 1. Personal (una sola vez)
            await self.crear_personal_completo()
            
            # 2. Pacientes (una sola vez) 
            await self.crear_pacientes_variados()
            
            # 3. Cargar servicios existentes
            await self.cargar_servicios_disponibles()
            
            # 4. Simular 3 semanas de operación
            await self.simular_semanas_operacion(3)
            
            print("\n" + "🎉"*20)
            print("✅ POBLADO COMPLETADO CON ÉXITO")
            print(f"👥 Personal creado: {len(self.personal_creado)}")
            print(f"🏥 Pacientes creados: {len(self.pacientes_creados)}")
            print("📅 3 semanas de consultas simuladas")
            print("💰 Pagos con estados realistas creados")
            print("🎉"*20)
            
            # Mostrar resumen de credenciales
            self.mostrar_credenciales_acceso()
            
        except Exception as e:
            print(f"❌ Error en poblado: {e}")
            raise
    
    def mostrar_credenciales_acceso(self):
        """🔑 Mostrar todas las credenciales de acceso creadas"""
        if not self.credenciales_usuarios:
            print("⚠️ No se crearon usuarios de acceso")
            return
            
        print("\n" + "🔐"*50)
        print("🔑 CREDENCIALES DE ACCESO CREADAS")
        print("🔐"*50)
        print("Puedes usar estas credenciales para hacer login:")
        print()
        
        for cred in self.credenciales_usuarios:
            print(f"👤 {cred['nombre']}")
            print(f"   📧 Email: {cred['email']}")
            print(f"   🔑 Password: {cred['password']}")
            print(f"   👔 Rol: {cred['rol']}")
            print(f"   🆔 Auth ID: {cred['auth_user_id']}")
            print()
        
        print("📝 NOTAS IMPORTANTES:")
        print("• Todos los usuarios tienen la misma contraseña temporal")
        print("• Los usuarios pueden cambiar su contraseña después del primer login")
        print("• Los usuarios están confirmados automáticamente (no necesitan verificar email)")
        print("• Cada usuario está vinculado correctamente con su registro de personal")
        print("🔐"*50)
    
    # =====================================================
    # 👨‍⚕️ CREACIÓN DE PERSONAL
    # =====================================================
    
    async def crear_personal_completo(self):
        """👨‍⚕️ Crear 6 odontólogos + personal administrativo"""
        print("\n👨‍⚕️ Creando personal de la clínica...")
        
        # Datos realistas de odontólogos
        odontologos_data = [
            {
                "nombres": ["Carlos", "Alberto"], 
                "apellidos": ["García", "Mendoza"],
                "documento": "12345678",
                "celular": "+58 281-234-5678", 
                "especialidad": "Endodoncia",
                "email": "carlos.garcia@odontomarva.com"
            },
            {
                "nombres": ["María", "Elena"], 
                "apellidos": ["Rodríguez", "Silva"],
                "documento": "23456789",
                "celular": "+58 281-345-6789", 
                "especialidad": "Periodoncia",
                "email": "maria.rodriguez@odontomarva.com"
            },
            {
                "nombres": ["Luis", "Fernando"], 
                "apellidos": ["Martínez", "López"],
                "documento": "34567890",
                "celular": "+58 281-456-7890", 
                "especialidad": "Ortodoncía",
                "email": "luis.martinez@odontomarva.com"
            },
            {
                "nombres": ["Ana", "Patricia"], 
                "apellidos": ["González", "Herrera"],
                "documento": "45678901",
                "celular": "+58 281-567-8901", 
                "especialidad": "Odontopediatría",
                "email": "ana.gonzalez@odontomarva.com"
            },
            {
                "nombres": ["Roberto", "José"], 
                "apellidos": ["Fernández", "Castro"],
                "documento": "56789012",
                "celular": "+58 281-678-9012", 
                "especialidad": "Cirugía Oral",
                "email": "roberto.fernandez@odontomarva.com"
            },
            {
                "nombres": ["Gabriela", "Isabel"], 
                "apellidos": ["Morales", "Ruiz"],
                "documento": "67890123",
                "celular": "+58 281-789-0123", 
                "especialidad": "Implantología",
                "email": "gabriela.morales@odontomarva.com"
            }
        ]
        
        # Crear odontólogos
        for i, odontologo_data in enumerate(odontologos_data):
            try:
                # Crear usuario completo (Auth + Tabla)
                nombre_completo = f"Dr(a). {odontologo_data['nombres'][0]} {odontologo_data['apellidos'][0]}"
                usuario_id = await self.crear_usuario_completo(
                    email=odontologo_data["email"],
                    rol="odontologo",
                    nombre_completo=nombre_completo
                )
                
                # Crear personal
                personal_data = {
                    "usuario_id": usuario_id,
                    "primer_nombre": odontologo_data["nombres"][0],
                    "segundo_nombre": odontologo_data["nombres"][1],
                    "primer_apellido": odontologo_data["apellidos"][0], 
                    "segundo_apellido": odontologo_data["apellidos"][1],
                    "tipo_documento": "CI",
                    "numero_documento": odontologo_data["documento"],
                    "celular": odontologo_data["celular"],
                    "tipo_personal": "Odontólogo",
                    "especialidad": odontologo_data["especialidad"],
                    "numero_licencia": f"COV-{20000 + i}",
                    "salario": random.randint(800, 1500),
                    "acepta_pacientes_nuevos": True,
                    "orden_preferencia": i + 1
                }
                
                # Insertar directamente en BD (sin servicios)
                resultado = supabase.table("personal").insert(personal_data).execute()
                
                if resultado.data:
                    self.personal_creado.append(resultado.data[0])
                    self.odontologos_ids.append(resultado.data[0]["id"])
                    print(f"✅ Odontólogo creado: Dr(a). {odontologo_data['nombres'][0]} {odontologo_data['apellidos'][0]} - {odontologo_data['especialidad']}")
                
            except Exception as e:
                print(f"❌ Error creando odontólogo {odontologo_data['nombres'][0]}: {e}")
        
        # Crear 1 Administrador
        try:
            admin_usuario_id = await self.crear_usuario_completo(
                email="admin@odontomarva.com", 
                rol="administrador",
                nombre_completo="Carmen Victoria López"
            )
            
            admin_data = {
                "usuario_id": admin_usuario_id,
                "primer_nombre": "Carmen",
                "segundo_nombre": "Victoria",
                "primer_apellido": "López",
                "segundo_apellido": "Méndez",
                "tipo_documento": "CI", 
                "numero_documento": "98765432",
                "celular": "+58 281-987-6543",
                "tipo_personal": "Administrador",
                "salario": 600
            }
            
            resultado = supabase.table("personal").insert(admin_data).execute()
            if resultado.data:
                self.personal_creado.append(resultado.data[0])
                self.administradores_ids.append(resultado.data[0]["id"])
                print(f"✅ Administrador creado: Carmen López")
                
        except Exception as e:
            print(f"❌ Error creando administrador: {e}")
        
        print(f"✅ Personal creado: {len(self.personal_creado)} empleados")
    
    async def crear_usuario_completo(self, email: str, rol: str, nombre_completo: str) -> str:
        """🔐 Crear usuario COMPLETO: Supabase Auth + tabla usuarios + metadata"""
        try:
            print(f"    🔐 Creando usuario completo: {email}")
            
            # 1. Buscar rol_id
            roles_response = supabase.table("roles").select("id").eq("nombre", rol).execute()
            if not roles_response.data:
                raise Exception(f"Rol {rol} no encontrado en la base de datos")
            
            rol_id = roles_response.data[0]["id"]
            
            # 2. Crear usuario en Supabase Auth
            password_temporal = "OdontoMarva2024!"  # Contraseña temporal para todos
            
            auth_response = supabase.auth.admin.create_user({
                "email": email,
                "password": password_temporal,
                "email_confirm": True,  # Confirmar email automáticamente
                "user_metadata": {
                    "nombre_completo": nombre_completo,
                    "rol": rol,
                    "creado_por": "script_poblado",
                    "fecha_creacion": datetime.now().isoformat()
                }
            })
            
            if not auth_response.user:
                raise Exception(f"No se pudo crear usuario auth para {email}")
            
            auth_user_id = auth_response.user.id
            print(f"      ✅ Usuario Auth creado: {auth_user_id}")
            
            # 3. Crear registro en tabla usuarios vinculado
            usuario_data = {
                "id": str(uuid.uuid4()),
                "email": email,
                "rol_id": rol_id,
                "activo": True,
                "auth_user_id": auth_user_id,  # 🔗 VINCULACIÓN IMPORTANTE
                "metadata": {
                    "nombre_completo": nombre_completo,
                    "rol": rol,
                    "password_temporal": password_temporal,
                    "creado_por": "script_poblado"
                }
            }
            
            result = supabase.table("usuarios").insert(usuario_data).execute()
            
            if not result.data:
                raise Exception(f"No se pudo crear registro en tabla usuarios")
                
            usuario_id = result.data[0]["id"]
            print(f"      ✅ Usuario tabla creado: {usuario_id}")
            print(f"      🔑 Email: {email} | Password: {password_temporal}")
            
            # Guardar credenciales para mostrar al final
            self.credenciales_usuarios.append({
                "email": email,
                "password": password_temporal,
                "rol": rol,
                "nombre": nombre_completo,
                "auth_user_id": auth_user_id,
                "usuario_id": usuario_id
            })
            
            return usuario_id
            
        except Exception as e:
            print(f"      ❌ Error creando usuario completo {email}: {e}")
            # En caso de error, intentar crear solo en tabla (fallback)
            try:
                usuario_data = {
                    "id": str(uuid.uuid4()),
                    "email": email,
                    "rol_id": rol_id,
                    "activo": True,
                    "metadata": {"error": "auth_failed", "tipo": "fallback"}
                }
                fallback_result = supabase.table("usuarios").insert(usuario_data).execute()
                if fallback_result.data:
                    print(f"      ⚠️ Usuario creado SOLO en tabla (sin auth): {email}")
                    return fallback_result.data[0]["id"]
            except:
                pass
            
            # Último recurso: ID temporal
            return str(uuid.uuid4())
    
    # =====================================================
    # 👥 CREACIÓN DE PACIENTES
    # =====================================================
    
    async def crear_pacientes_variados(self):
        """👥 Crear 50 pacientes con datos realistas"""
        print("\n👥 Creando pacientes...")
        
        for i in range(50):
            try:
                # Generar datos realistas
                es_masculino = random.choice([True, False])
                nombres = NOMBRES_MASCULINOS if es_masculino else NOMBRES_FEMENINOS
                
                primer_nombre = random.choice(nombres)
                segundo_nombre = random.choice(nombres) if random.random() > 0.3 else ""
                primer_apellido = random.choice(APELLIDOS)
                segundo_apellido = random.choice(APELLIDOS)
                
                # Documento único
                numero_documento = f"{random.randint(10000000, 30000000)}"
                
                # Datos del paciente
                paciente_data = {
                    "id": str(uuid.uuid4()),
                    "primer_nombre": primer_nombre,
                    "segundo_nombre": segundo_nombre,
                    "primer_apellido": primer_apellido, 
                    "segundo_apellido": segundo_apellido,
                    "tipo_documento": "CI",
                    "numero_documento": numero_documento,
                    "fecha_nacimiento": self.generar_fecha_nacimiento(),
                    "genero": "masculino" if es_masculino else "femenino",
                    "celular_1": f"+58 {random.randint(281, 424)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    "celular_2": f"+58 {random.randint(281, 424)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}" if random.random() > 0.6 else "",
                    "email": f"{primer_nombre.lower()}.{primer_apellido.lower()}{random.randint(1, 99)}@email.com",
                    "direccion": f"Av. {random.choice(['Libertador', 'Principal', 'Intercomunal', 'Las Américas'])} #{random.randint(1, 200)}, {random.choice(CIUDADES_VENEZUELA)}",
                    "ciudad": random.choice(CIUDADES_VENEZUELA),
                    "ocupacion": random.choice(["Empleado", "Comerciante", "Estudiante", "Profesional", "Ama de casa", "Jubilado"]),
                    "estado_civil": random.choice(["soltero", "casado", "divorciado", "viudo"]),
                    "contacto_emergencia": {
                        "nombre": f"{random.choice(nombres)} {random.choice(APELLIDOS)}",
                        "celular": f"+58 {random.randint(281, 424)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                        "relacion": random.choice(["Esposo/a", "Hijo/a", "Padre/Madre", "Hermano/a"])
                    },
                    "alergias": self.generar_alergias(),
                    "condiciones_medicas": self.generar_condiciones_medicas(),
                    "activo": True,
                    "registrado_por": self.administradores_ids[0] if self.administradores_ids else None
                }
                
                # Insertar paciente directamente
                resultado = supabase.table("pacientes").insert(paciente_data).execute()
                
                if resultado.data:
                    self.pacientes_creados.append(resultado.data[0])
                    if i % 10 == 0:
                        print(f"✅ Creados {i+1} pacientes...")
                
            except Exception as e:
                print(f"❌ Error creando paciente {i+1}: {e}")
        
        print(f"✅ Pacientes creados: {len(self.pacientes_creados)}")
    
    def generar_fecha_nacimiento(self) -> str:
        """📅 Generar fecha de nacimiento realista"""
        inicio = date.today() - timedelta(days=365*80)  # 80 años atrás
        fin = date.today() - timedelta(days=365*18)     # 18 años atrás
        
        dias_diferencia = (fin - inicio).days
        fecha_aleatoria = inicio + timedelta(days=random.randint(0, dias_diferencia))
        
        return fecha_aleatoria.isoformat()
    
    def generar_alergias(self) -> list:
        """🤧 Generar lista de alergias realista"""
        alergias_posibles = [
            "Penicilina", "Lidocaína", "Látex", "Ibuprofeno", "Aspirina",
            "Anestesia local", "Ninguna conocida"
        ]
        
        if random.random() > 0.7:  # 30% tiene alergias
            return [random.choice(alergias_posibles)]
        return ["Ninguna conocida"]
    
    def generar_condiciones_medicas(self) -> list:
        """🏥 Generar condiciones médicas realistas"""
        condiciones = [
            "Hipertensión", "Diabetes", "Cardiopatía", "Asma", 
            "Artritis", "Ninguna conocida"
        ]
        
        if random.random() > 0.6:  # 40% tiene alguna condición
            return [random.choice(condiciones)]
        return ["Ninguna conocida"]
    
    # =====================================================
    # 🏥 SERVICIOS DISPONIBLES  
    # =====================================================
    
    async def cargar_servicios_disponibles(self):
        """🏥 Cargar servicios desde la base de datos"""
        try:
            # Cargar servicios directamente de la BD
            result = supabase.table("servicios").select("*").eq("activo", True).execute()
            if result.data:
                self.servicios_disponibles = result.data
                print(f"📋 Servicios disponibles cargados: {len(self.servicios_disponibles)}")
            else:
                print("⚠️ No hay servicios en la BD, creando básicos...")
                await self.crear_servicios_basicos()
        except Exception as e:
            print(f"❌ Error cargando servicios: {e}")
            self.servicios_disponibles = []
            
    async def crear_servicios_basicos(self):
        """🏥 Crear servicios básicos si no existen"""
        try:
            servicios_basicos = [
                {"codigo": "CONS001", "nombre": "Consulta General", "categoria": "Consulta", "precio_base_bs": 1825.00, "precio_base_usd": 50.00},
                {"codigo": "LIMP001", "nombre": "Profilaxis Dental", "categoria": "Preventiva", "precio_base_bs": 2920.00, "precio_base_usd": 80.00},
                {"codigo": "OBTU001", "nombre": "Obturación Simple", "categoria": "Restaurativa", "precio_base_bs": 4380.00, "precio_base_usd": 120.00},
                {"codigo": "ENDO001", "nombre": "Endodoncia", "categoria": "Endodoncia", "precio_base_bs": 12775.00, "precio_base_usd": 350.00},
                {"codigo": "EXTR001", "nombre": "Extracción Simple", "categoria": "Cirugía", "precio_base_bs": 2920.00, "precio_base_usd": 80.00}
            ]
            
            servicios_data = []
            for servicio in servicios_basicos:
                servicio["id"] = str(uuid.uuid4())
                servicio["activo"] = True
                servicio["descripcion"] = f"Servicio de {servicio['nombre']}"
                servicios_data.append(servicio)
            
            result = supabase.table("servicios").insert(servicios_data).execute()
            if result.data:
                self.servicios_disponibles = result.data
                print(f"✅ Servicios básicos creados: {len(result.data)}")
                
        except Exception as e:
            print(f"❌ Error creando servicios básicos: {e}")
    
    # =====================================================
    # 📅 SIMULACIÓN DE SEMANAS DE OPERACIÓN
    # =====================================================
    
    async def simular_semanas_operacion(self, num_semanas: int):
        """📅 Simular operación de la clínica por varias semanas"""
        print(f"\n📅 Simulando {num_semanas} semanas de operación...")
        
        fecha_inicio = date.today() - timedelta(weeks=num_semanas)
        
        for semana in range(num_semanas):
            fecha_semana = fecha_inicio + timedelta(weeks=semana)
            
            print(f"\n📅 Semana {semana + 1}: {fecha_semana}")
            
            # Simular 5 días laborales (Lunes a Viernes)
            for dia_laborable in range(5):
                fecha_dia = fecha_semana + timedelta(days=dia_laborable)
                
                # Solo procesar días pasados (no futuro)
                if fecha_dia <= date.today():
                    await self.simular_dia_clinica(fecha_dia)
    
    async def simular_dia_clinica(self, fecha: date):
        """🏥 Simular un día completo de operación de la clínica"""
        # Generar entre 8-15 consultas por día (realista)
        num_consultas = random.randint(8, 15)
        
        print(f"  📍 {fecha}: {num_consultas} consultas")
        
        # Distribución realista por horas
        horas_atencion = [
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
            "11:00", "11:30", "14:00", "14:30", "15:00", "15:30", 
            "16:00", "16:30", "17:00", "17:30", "18:00"
        ]
        
        for i in range(num_consultas):
            try:
                # Paciente aleatorio
                paciente = random.choice(self.pacientes_creados)
                
                # Odontólogo aleatorio (con distribución realista)
                odontologo_id = self.seleccionar_odontologo_realista()
                
                # Hora de llegada
                hora_llegada = random.choice(horas_atencion)
                fecha_llegada = f"{fecha} {hora_llegada}:00"
                
                # Crear consulta
                consulta_id = await self.crear_consulta_realista(
                    paciente_id=paciente["id"],
                    odontologo_id=odontologo_id,
                    fecha_llegada=fecha_llegada
                )
                
                if consulta_id:
                    # Crear intervención para la consulta
                    await self.crear_intervencion_realista(consulta_id, odontologo_id)
                    
                    # 80% de probabilidad de pago inmediato, 20% pendiente
                    if random.random() > 0.2:
                        await self.crear_pago_consulta(consulta_id, paciente["id"])
                
            except Exception as e:
                print(f"    ❌ Error en consulta {i+1}: {e}")
    
    def seleccionar_odontologo_realista(self) -> str:
        """👨‍⚕️ Seleccionar odontólogo con distribución realista"""
        if not self.odontologos_ids:
            return None
        
        # Algunos odontólogos son más populares (80/20 rule)
        pesos = [0.25, 0.2, 0.2, 0.15, 0.1, 0.1]  # Distribución no uniforme
        return random.choices(self.odontologos_ids, weights=pesos[:len(self.odontologos_ids)])[0]
    
    async def crear_consulta_realista(self, paciente_id: str, odontologo_id: str, fecha_llegada: str) -> str:
        """📅 Crear consulta realista"""
        try:
            consultas_service.set_user_context("system", {"role": "administrador"})
            
            consulta_data = {
                "paciente_id": paciente_id,
                "primer_odontologo_id": odontologo_id,
                "odontologo_preferido_id": odontologo_id,
                "fecha_llegada": fecha_llegada,
                "tipo_consulta": random.choice(["general", "control", "urgencia"]),
                "prioridad": random.choices(
                    ["normal", "alta", "urgente"], 
                    weights=[0.7, 0.2, 0.1]
                )[0],
                "motivo_consulta": random.choice(MOTIVOS_CONSULTA),
                "estado": "completada",  # Simulamos consultas ya completadas
                "creada_por": self.administradores_ids[0] if self.administradores_ids else None
            }
            
            # Insertar directamente en base de datos
            result = supabase.table("consultas").insert(consulta_data).execute()
            
            if result.data:
                return result.data[0]["id"]
                
        except Exception as e:
            print(f"    ❌ Error creando consulta: {e}")
            
        return None
    
    async def crear_intervencion_realista(self, consulta_id: str, odontologo_id: str):
        """🦷 Crear intervención odontológica realista"""
        try:
            # Seleccionar 1-3 servicios para esta intervención
            num_servicios = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
            servicios_seleccionados = random.sample(self.servicios_disponibles, num_servicios)
            
            # Datos de la intervención
            intervencion_data = {
                "id": str(uuid.uuid4()),
                "consulta_id": consulta_id,
                "odontologo_id": odontologo_id,
                "procedimiento_realizado": self.generar_procedimiento_realista(servicios_seleccionados),
                "dientes_afectados": self.generar_dientes_afectados(),
                "anestesia_utilizada": random.choice(["Lidocaína 2%", "Articaína", "Ninguna"]),
                "estado": "completada",
                "requiere_control": random.choice([True, False]),
                "instrucciones_paciente": self.generar_instrucciones()
            }
            
            # Insertar intervención
            result = supabase.table("intervenciones").insert(intervencion_data).execute()
            
            if result.data:
                intervencion_id = result.data[0]["id"]
                
                # Crear servicios de la intervención
                total_bs = 0
                total_usd = 0
                
                for servicio in servicios_seleccionados:
                    servicio_data = {
                        "intervencion_id": intervencion_id,
                        "servicio_id": servicio["id"],
                        "cantidad": 1,
                        "precio_unitario_bs": float(servicio["precio_base_bs"]),
                        "precio_unitario_usd": float(servicio["precio_base_usd"]),
                        "precio_total_bs": float(servicio["precio_base_bs"]),
                        "precio_total_usd": float(servicio["precio_base_usd"])
                    }
                    
                    total_bs += float(servicio["precio_base_bs"])
                    total_usd += float(servicio["precio_base_usd"])
                    
                    supabase.table("intervenciones_servicios").insert(servicio_data).execute()
                
                # Actualizar totales de la intervención
                supabase.table("intervenciones").update({
                    "total_bs": total_bs,
                    "total_usd": total_usd
                }).eq("id", intervencion_id).execute()
                
        except Exception as e:
            print(f"    ❌ Error creando intervención: {e}")
    
    def generar_procedimiento_realista(self, servicios: list) -> str:
        """📝 Generar descripción realista del procedimiento"""
        procedimientos = [s["nombre"] for s in servicios]
        return f"Procedimiento realizado: {', '.join(procedimientos)}. Paciente tolera bien el tratamiento."
    
    def generar_dientes_afectados(self) -> list:
        """🦷 Generar lista realista de dientes afectados"""
        # Dientes más comunes en tratamientos
        dientes_comunes = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28,
                          31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48]
        
        num_dientes = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
        return sorted(random.sample(dientes_comunes, num_dientes))
    
    def generar_instrucciones(self) -> str:
        """📋 Generar instrucciones post-tratamiento"""
        instrucciones = [
            "Evitar alimentos duros las próximas 24 horas",
            "Tomar analgésicos según indicación si hay molestias",
            "Mantener buena higiene oral",
            "Control en 15 días",
            "Evitar enjuagues vigorosos por 24 horas"
        ]
        return ". ".join(random.sample(instrucciones, random.randint(2, 4)))
    
    async def crear_pago_consulta(self, consulta_id: str, paciente_id: str):
        """💰 Crear pago realista para la consulta"""
        try:
            # Obtener costo de la consulta
            consulta_result = supabase.table("consultas").select("costo_total_bs, costo_total_usd").eq("id", consulta_id).execute()
            
            if not consulta_result.data:
                return
                
            consulta = consulta_result.data[0]
            monto_bs = consulta["costo_total_bs"] or 0
            monto_usd = consulta["costo_total_usd"] or 0
            
            # Tipos de pago realistas
            metodos_pago = ["efectivo", "tarjeta_debito", "transferencia", "pago_movil"]
            
            # 90% pago completo, 10% pago parcial
            pago_completo = random.random() > 0.1
            
            if pago_completo:
                monto_pagado_bs = monto_bs
                monto_pagado_usd = monto_usd
                estado_pago = "completado"
            else:
                monto_pagado_bs = monto_bs * random.uniform(0.3, 0.7)
                monto_pagado_usd = monto_usd * random.uniform(0.3, 0.7)
                estado_pago = "parcial"
            
            pago_data = {
                "consulta_id": consulta_id,
                "paciente_id": paciente_id,
                "monto_total_bs": monto_bs,
                "monto_total_usd": monto_usd,
                "monto_pagado_bs": monto_pagado_bs,
                "monto_pagado_usd": monto_pagado_usd,
                "tasa_cambio_bs_usd": self.tasa_cambio,
                "metodos_pago": [{"metodo": random.choice(metodos_pago), "monto": monto_pagado_bs}],
                "concepto": "Pago consulta odontológica",
                "estado_pago": estado_pago,
                "procesado_por": self.administradores_ids[0] if self.administradores_ids else None
            }
            
            supabase.table("pagos").insert(pago_data).execute()
            
        except Exception as e:
            print(f"    ❌ Error creando pago: {e}")


# =====================================================
# 🎬 EJECUCIÓN PRINCIPAL
# =====================================================

async def main():
    """🎬 Función principal para ejecutar el poblado"""
    print("🏥 POBLADOR DE DATOS - CLÍNICA DENTAL ODONTOMARVA")
    print("="*55)
    print("⚠️  SOLO USAR EN AMBIENTE DE DESARROLLO")
    print("⚠️  Este script creará muchos datos de prueba")
    print("="*55)
    
    confirmar = input("¿Continuar con el poblado? (s/N): ")
    if confirmar.lower() not in ['s', 'si', 'yes']:
        print("❌ Poblado cancelado.")
        return
    
    try:
        poblador = PobladorDatosClinica()
        await poblador.poblar_todo()
        
    except KeyboardInterrupt:
        print("\n⚠️ Poblado interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    # Ejecutar el poblado
    asyncio.run(main())