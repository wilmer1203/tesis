#!/usr/bin/env python3
"""
🏥 POBLADO COMPLETO SIN AUTH - VERSIÓN DEFINITIVA
================================================

Crea datos completos sin autenticación real.
Funciona igual que el simple pero con MUCHO más contenido.
"""

import asyncio
import random
from datetime import datetime, date, timedelta
import uuid
from dental_system.supabase.client import supabase_client

# Obtener cliente
supabase = supabase_client.get_client()

# =====================================================
# 🎭 DATOS FICTICIOS REALISTAS
# =====================================================

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

ESPECIALIDADES = [
    "Endodoncia", "Periodoncia", "Ortodoncía", "Cirugía Oral", 
    "Implantología", "Odontopediatría", "Estética Dental", "Odontología General"
]

MOTIVOS_CONSULTA = [
    "Dolor de muela", "Limpieza dental", "Control rutinario", "Sensibilidad dental",
    "Sangrado de encías", "Caries", "Revisión de brackets", "Dolor en mandíbula",
    "Consulta de implante", "Blanqueamiento", "Revisión post-tratamiento",
    "Emergencia dental", "Consulta estética", "Tratamiento de conducto"
]

class PobladorCompleto:
    def __init__(self):
        self.odontologos_ids = []
        self.admin_id = None
        self.pacientes_ids = []
        self.servicios_disponibles = []
        print("🚀 Poblador Completo - SIN AUTH pero con TODOS los datos")
        
    async def poblar_todo(self):
        """🎯 Poblado completo sin auth"""
        try:
            print("\n" + "="*60)
            print("🎬 POBLADO COMPLETO - VERSIÓN SIN AUTH")
            print("="*60)
            
            # 1. Limpiar datos existentes (opcional)
            await self.limpiar_datos_existentes()
            
            # 2. Verificar/crear roles
            await self.verificar_roles()
            
            # 3. Crear 6 odontólogos + 1 admin
            await self.crear_personal_completo()
            
            # 4. Crear 50 pacientes
            await self.crear_pacientes_variados()
            
            # 5. Crear servicios si no existen
            await self.verificar_servicios()
            
            # 6. Simular 3 semanas de consultas
            await self.simular_semanas_operacion()
            
            print("\n" + "🎉"*20)
            print("✅ POBLADO COMPLETO EXITOSO")
            print(f"👨‍⚕️ Odontólogos: {len(self.odontologos_ids)}")
            print(f"👥 Pacientes: {len(self.pacientes_ids)}")
            print(f"🏥 Servicios: {len(self.servicios_disponibles)}")
            print("📅 3 semanas de datos simulados")
            print("🎉"*20)
            
        except Exception as e:
            print(f"❌ Error general: {e}")
            
    async def limpiar_datos_existentes(self):
        """🧹 Limpiar datos existentes para evitar duplicados"""
        print("\n🧹 Limpiando datos existentes...")
        
        try:
            # Eliminar en orden inverso por foreign keys
            supabase.table("pagos").delete().neq("id", "").execute()
            supabase.table("intervenciones_servicios").delete().neq("id", "").execute()
            supabase.table("intervenciones").delete().neq("id", "").execute()
            supabase.table("consultas").delete().neq("id", "").execute()
            supabase.table("pacientes").delete().neq("id", "").execute()
            supabase.table("personal").delete().neq("id", "").execute()
            supabase.table("usuarios").delete().neq("id", "").execute()
            
            print("✅ Datos anteriores limpiados")
            
        except Exception as e:
            print(f"⚠️ Error limpiando (normal si está vacío): {e}")
    
    async def verificar_roles(self):
        """👔 Verificar/crear roles"""
        try:
            roles = supabase.table("roles").select("*").execute()
            if not roles.data:
                print("📋 Creando roles básicos...")
                roles_data = [
                    {"id": str(uuid.uuid4()), "nombre": "gerente", "descripcion": "Acceso completo", "permisos": {"all": True}},
                    {"id": str(uuid.uuid4()), "nombre": "odontologo", "descripcion": "Atención clínica", "permisos": {"consultas": True}},
                    {"id": str(uuid.uuid4()), "nombre": "administrador", "descripcion": "Gestión administrativa", "permisos": {"pacientes": True}}
                ]
                supabase.table("roles").insert(roles_data).execute()
                print("✅ Roles creados")
            else:
                print(f"✅ Roles existentes: {len(roles.data)}")
        except Exception as e:
            print(f"❌ Error con roles: {e}")
    
    async def crear_personal_completo(self):
        """👨‍⚕️ Crear personal completo"""
        print("\n👨‍⚕️ Creando personal completo...")
        
        # Obtener IDs de roles
        rol_odontologo = supabase.table("roles").select("id").eq("nombre", "odontologo").execute()
        rol_admin = supabase.table("roles").select("id").eq("nombre", "administrador").execute()
        
        if not rol_odontologo.data or not rol_admin.data:
            print("❌ Roles no encontrados")
            return
            
        rol_odontologo_id = rol_odontologo.data[0]["id"]
        rol_admin_id = rol_admin.data[0]["id"]
        
        # Datos reales de odontólogos
        odontologos_data = [
            {"nombres": ["Carlos", "Alberto"], "apellidos": ["García", "Mendoza"], "doc": "12345678", "esp": "Endodoncia"},
            {"nombres": ["María", "Elena"], "apellidos": ["Rodríguez", "Silva"], "doc": "23456789", "esp": "Periodoncia"},
            {"nombres": ["Luis", "Fernando"], "apellidos": ["Martínez", "López"], "doc": "34567890", "esp": "Ortodoncía"},
            {"nombres": ["Ana", "Patricia"], "apellidos": ["González", "Herrera"], "doc": "45678901", "esp": "Odontopediatría"},
            {"nombres": ["Roberto", "José"], "apellidos": ["Fernández", "Castro"], "doc": "56789012", "esp": "Cirugía Oral"},
            {"nombres": ["Gabriela", "Isabel"], "apellidos": ["Morales", "Ruiz"], "doc": "67890123", "esp": "Implantología"}
        ]
        
        # Crear odontólogos
        for i, data in enumerate(odontologos_data):
            try:
                # Crear usuario SIN AUTH
                usuario_id = str(uuid.uuid4())
                usuario_data = {
                    "id": usuario_id,
                    "email": f"{data['nombres'][0].lower()}.{data['apellidos'][0].lower()}@odontomarva.com",
                    "rol_id": rol_odontologo_id,
                    "activo": True,
                    "metadata": {"tipo": "datos_prueba", "sin_auth": True}
                }
                
                user_result = supabase.table("usuarios").insert(usuario_data).execute()
                
                if user_result.data:
                    # Crear personal
                    personal_data = {
                        "id": str(uuid.uuid4()),
                        "usuario_id": usuario_id,
                        "primer_nombre": data["nombres"][0],
                        "segundo_nombre": data["nombres"][1],
                        "primer_apellido": data["apellidos"][0],
                        "segundo_apellido": data["apellidos"][1],
                        "numero_documento": data["doc"],
                        "tipo_documento": "CI",
                        "celular": f"+58 281-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                        "tipo_personal": "Odontólogo",
                        "especialidad": data["esp"],
                        "numero_licencia": f"COV-{20000 + i}",
                        "estado_laboral": "activo",
                        "acepta_pacientes_nuevos": True,
                        "orden_preferencia": i + 1,
                        "salario": random.randint(800, 1500)
                    }
                    
                    personal_result = supabase.table("personal").insert(personal_data).execute()
                    
                    if personal_result.data:
                        self.odontologos_ids.append(personal_result.data[0]["id"])
                        print(f"   ✅ Dr(a). {data['nombres'][0]} {data['apellidos'][0]} - {data['esp']}")
                        
            except Exception as e:
                print(f"   ❌ Error con odontólogo {i+1}: {e}")
        
        # Crear 1 administrador
        try:
            admin_usuario_id = str(uuid.uuid4())
            admin_usuario_data = {
                "id": admin_usuario_id,
                "email": "admin@odontomarva.com",
                "rol_id": rol_admin_id,
                "activo": True,
                "metadata": {"tipo": "datos_prueba", "sin_auth": True}
            }
            
            admin_user_result = supabase.table("usuarios").insert(admin_usuario_data).execute()
            
            if admin_user_result.data:
                admin_personal_data = {
                    "id": str(uuid.uuid4()),
                    "usuario_id": admin_usuario_id,
                    "primer_nombre": "Carmen",
                    "segundo_nombre": "Victoria",
                    "primer_apellido": "López",
                    "segundo_apellido": "Méndez",
                    "numero_documento": "98765432",
                    "tipo_documento": "CI",
                    "celular": "+58 281-987-6543",
                    "tipo_personal": "Administrador",
                    "estado_laboral": "activo",
                    "salario": 600
                }
                
                admin_personal_result = supabase.table("personal").insert(admin_personal_data).execute()
                
                if admin_personal_result.data:
                    self.admin_id = admin_personal_result.data[0]["id"]
                    print("   ✅ Administradora: Carmen López")
                    
        except Exception as e:
            print(f"   ❌ Error creando admin: {e}")
            
        print(f"✅ Personal creado: {len(self.odontologos_ids)} odontólogos + 1 admin")
    
    async def crear_pacientes_variados(self):
        """👥 Crear 50 pacientes variados"""
        print("\n👥 Creando 50 pacientes...")
        
        for i in range(50):
            try:
                es_masculino = random.choice([True, False])
                nombres = NOMBRES_MASCULINOS if es_masculino else NOMBRES_FEMENINOS
                
                nombre1 = random.choice(nombres)
                nombre2 = random.choice(nombres) if random.random() > 0.4 else ""
                apellido1 = random.choice(APELLIDOS)
                apellido2 = random.choice(APELLIDOS)
                
                paciente_data = {
                    "id": str(uuid.uuid4()),
                    "primer_nombre": nombre1,
                    "segundo_nombre": nombre2,
                    "primer_apellido": apellido1,
                    "segundo_apellido": apellido2,
                    "numero_documento": f"{random.randint(10000000, 30000000)}",
                    "tipo_documento": "CI",
                    "genero": "masculino" if es_masculino else "femenino",
                    "fecha_nacimiento": self.generar_fecha_nacimiento(),
                    "celular_1": f"+58 {random.randint(281, 424)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    "celular_2": f"+58 {random.randint(281, 424)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}" if random.random() > 0.6 else None,
                    "email": f"{nombre1.lower()}{random.randint(1, 99)}@gmail.com",
                    "direccion": f"Calle {random.randint(1, 100)}, {random.choice(CIUDADES_VENEZUELA)}",
                    "ciudad": random.choice(CIUDADES_VENEZUELA),
                    "ocupacion": random.choice(["Empleado", "Comerciante", "Estudiante", "Profesional", "Jubilado"]),
                    "estado_civil": random.choice(["soltero", "casado", "divorciado", "viudo"]),
                    "contacto_emergencia": {
                        "nombre": f"{random.choice(nombres)} {random.choice(APELLIDOS)}",
                        "celular": f"+58 {random.randint(281, 424)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                        "relacion": random.choice(["Esposo/a", "Hijo/a", "Padre/Madre"])
                    },
                    "alergias": ["Ninguna conocida"] if random.random() > 0.3 else [random.choice(["Penicilina", "Lidocaína", "Látex"])],
                    "condiciones_medicas": ["Ninguna conocida"] if random.random() > 0.4 else [random.choice(["Hipertensión", "Diabetes", "Asma"])],
                    "activo": True,
                    "registrado_por": self.admin_id
                }
                
                result = supabase.table("pacientes").insert(paciente_data).execute()
                
                if result.data:
                    self.pacientes_ids.append(result.data[0]["id"])
                    if (i + 1) % 10 == 0:
                        print(f"   ✅ {i + 1} pacientes creados...")
                        
            except Exception as e:
                print(f"   ❌ Error paciente {i+1}: {e}")
        
        print(f"✅ Total pacientes: {len(self.pacientes_ids)}")
    
    def generar_fecha_nacimiento(self):
        """📅 Generar fecha de nacimiento realista"""
        inicio = date.today() - timedelta(days=365*80)
        fin = date.today() - timedelta(days=365*18)
        dias = (fin - inicio).days
        fecha = inicio + timedelta(days=random.randint(0, dias))
        return fecha.isoformat()
    
    async def verificar_servicios(self):
        """🏥 Verificar/crear servicios"""
        try:
            servicios = supabase.table("servicios").select("*").execute()
            if servicios.data:
                self.servicios_disponibles = servicios.data
                print(f"✅ Servicios existentes: {len(servicios.data)}")
            else:
                print("📋 Creando servicios básicos...")
                await self.crear_servicios_basicos()
        except Exception as e:
            print(f"❌ Error servicios: {e}")
    
    async def crear_servicios_basicos(self):
        """🏥 Crear servicios básicos"""
        servicios_data = [
            {"codigo": "CONS001", "nombre": "Consulta General", "categoria": "Consulta", "precio_base_bs": 1825.00, "precio_base_usd": 50.00},
            {"codigo": "LIMP001", "nombre": "Profilaxis Dental", "categoria": "Preventiva", "precio_base_bs": 2920.00, "precio_base_usd": 80.00},
            {"codigo": "OBTU001", "nombre": "Obturación Simple", "categoria": "Restaurativa", "precio_base_bs": 4380.00, "precio_base_usd": 120.00},
            {"codigo": "ENDO001", "nombre": "Endodoncia", "categoria": "Endodoncia", "precio_base_bs": 12775.00, "precio_base_usd": 350.00},
            {"codigo": "EXTR001", "nombre": "Extracción Simple", "categoria": "Cirugía", "precio_base_bs": 2920.00, "precio_base_usd": 80.00},
            {"codigo": "EXTR002", "nombre": "Extracción Compleja", "categoria": "Cirugía", "precio_base_bs": 5475.00, "precio_base_usd": 150.00},
            {"codigo": "CORO001", "nombre": "Corona Dental", "categoria": "Prótesis", "precio_base_bs": 29200.00, "precio_base_usd": 800.00},
            {"codigo": "BLAN001", "nombre": "Blanqueamiento", "categoria": "Estética", "precio_base_bs": 10950.00, "precio_base_usd": 300.00}
        ]
        
        for servicio in servicios_data:
            servicio["id"] = str(uuid.uuid4())
            servicio["activo"] = True
            servicio["descripcion"] = f"Servicio de {servicio['nombre']}"
        
        result = supabase.table("servicios").insert(servicios_data).execute()
        if result.data:
            self.servicios_disponibles = result.data
            print(f"✅ Servicios creados: {len(result.data)}")
    
    async def simular_semanas_operacion(self):
        """📅 Simular 3 semanas de operación"""
        print("\n📅 Simulando 3 semanas de operación...")
        
        if not self.odontologos_ids or not self.pacientes_ids:
            print("❌ No hay personal u pacientes para crear consultas")
            return
        
        fecha_inicio = date.today() - timedelta(weeks=3)
        
        total_consultas = 0
        for semana in range(3):
            fecha_semana = fecha_inicio + timedelta(weeks=semana)
            print(f"   📅 Semana {semana + 1}: {fecha_semana}")
            
            for dia in range(5):  # 5 días laborales
                fecha_dia = fecha_semana + timedelta(days=dia)
                if fecha_dia <= date.today():
                    consultas_dia = await self.crear_consultas_dia(fecha_dia)
                    total_consultas += consultas_dia
        
        print(f"✅ Total consultas simuladas: {total_consultas}")
    
    async def crear_consultas_dia(self, fecha):
        """📅 Crear consultas para un día específico"""
        num_consultas = random.randint(8, 15)
        horas = ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "14:00", "14:30", "15:00", "15:30", "16:00"]
        
        consultas_creadas = 0
        
        for i in range(num_consultas):
            try:
                consulta_data = {
                    "id": str(uuid.uuid4()),
                    "paciente_id": random.choice(self.pacientes_ids),
                    "primer_odontologo_id": random.choice(self.odontologos_ids),
                    "fecha_llegada": f"{fecha} {random.choice(horas)}:00",
                    "motivo_consulta": random.choice(MOTIVOS_CONSULTA),
                    "tipo_consulta": random.choice(["general", "control", "urgencia"]),
                    "estado": "completada",  # Consultas pasadas completadas
                    "prioridad": random.choices(["normal", "alta", "urgente"], weights=[0.8, 0.15, 0.05])[0],
                    "creada_por": self.admin_id
                }
                
                result = supabase.table("consultas").insert(consulta_data).execute()
                
                if result.data:
                    consulta_id = result.data[0]["id"]
                    # Crear intervención para la consulta
                    await self.crear_intervencion(consulta_id, consulta_data["primer_odontologo_id"])
                    consultas_creadas += 1
                    
            except Exception as e:
                if i == 0:  # Solo mostrar el primer error del día
                    print(f"      ❌ Error consulta {fecha}: {e}")
        
        return consultas_creadas
    
    async def crear_intervencion(self, consulta_id, odontologo_id):
        """🦷 Crear intervención para la consulta"""
        try:
            # Seleccionar 1-2 servicios
            servicios_seleccionados = random.sample(self.servicios_disponibles, random.randint(1, 2))
            
            # Crear intervención
            intervencion_data = {
                "id": str(uuid.uuid4()),
                "consulta_id": consulta_id,
                "odontologo_id": odontologo_id,
                "procedimiento_realizado": f"Procedimiento: {', '.join([s['nombre'] for s in servicios_seleccionados])}",
                "dientes_afectados": [random.randint(11, 48) for _ in range(random.randint(1, 3))],
                "estado": "completada"
            }
            
            result = supabase.table("intervenciones").insert(intervencion_data).execute()
            
            if result.data:
                intervencion_id = result.data[0]["id"]
                total_bs = 0
                total_usd = 0
                
                # Crear servicios de la intervención
                for servicio in servicios_seleccionados:
                    servicio_intervencion = {
                        "id": str(uuid.uuid4()),
                        "intervencion_id": intervencion_id,
                        "servicio_id": servicio["id"],
                        "cantidad": 1,
                        "precio_unitario_bs": servicio["precio_base_bs"],
                        "precio_unitario_usd": servicio["precio_base_usd"],
                        "precio_total_bs": servicio["precio_base_bs"],
                        "precio_total_usd": servicio["precio_base_usd"]
                    }
                    
                    total_bs += servicio["precio_base_bs"]
                    total_usd += servicio["precio_base_usd"]
                    
                    supabase.table("intervenciones_servicios").insert(servicio_intervencion).execute()
                
                # Actualizar totales
                supabase.table("intervenciones").update({
                    "total_bs": total_bs,
                    "total_usd": total_usd
                }).eq("id", intervencion_id).execute()
                
                # Crear pago (80% completado)
                if random.random() > 0.2:
                    await self.crear_pago(consulta_id, total_bs, total_usd)
                    
        except Exception as e:
            pass  # No mostrar errores de intervención para no saturar
    
    async def crear_pago(self, consulta_id, monto_bs, monto_usd):
        """💰 Crear pago para la consulta"""
        try:
            # Consulta data para obtener paciente_id
            consulta = supabase.table("consultas").select("paciente_id").eq("id", consulta_id).execute()
            if not consulta.data:
                return
            
            paciente_id = consulta.data[0]["paciente_id"]
            
            # 90% pago completo, 10% parcial
            pago_completo = random.random() > 0.1
            
            if pago_completo:
                pagado_bs = monto_bs
                pagado_usd = monto_usd
                estado = "completado"
            else:
                pagado_bs = monto_bs * random.uniform(0.4, 0.8)
                pagado_usd = monto_usd * random.uniform(0.4, 0.8)
                estado = "parcial"
            
            pago_data = {
                "id": str(uuid.uuid4()),
                "consulta_id": consulta_id,
                "paciente_id": paciente_id,
                "monto_total_bs": monto_bs,
                "monto_total_usd": monto_usd,
                "monto_pagado_bs": pagado_bs,
                "monto_pagado_usd": pagado_usd,
                "tasa_cambio_bs_usd": 36.50,
                "metodos_pago": [{"metodo": random.choice(["efectivo", "tarjeta", "transferencia"]), "monto": pagado_bs}],
                "concepto": "Pago consulta odontológica",
                "estado_pago": estado,
                "procesado_por": self.admin_id
            }
            
            supabase.table("pagos").insert(pago_data).execute()
            
        except Exception as e:
            pass

async def main():
    """🎬 Ejecutar poblado completo"""
    print("POBLADO COMPLETO SIN AUTH - CLINICA DENTAL")
    print("="*50)
    
    poblador = PobladorCompleto()
    await poblador.poblar_todo()
    
    print("\n✅ SISTEMA LISTO CON DATOS COMPLETOS")
    print("🔗 Ejecuta 'reflex run' para ver todo funcionando")
    print("\n💡 NOTA: Los usuarios NO tienen login real.")
    print("   Pero tienes TODOS los datos para probar el sistema.")

if __name__ == "__main__":
    asyncio.run(main())