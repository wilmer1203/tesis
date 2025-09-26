#!/usr/bin/env python3
"""
📅 POBLADO RÁPIDO PARA HOY
==========================

Script pequeño que solo crea consultas para el día de hoy.
Útil para pruebas rápidas sin poblar toda la base de datos.
"""

import asyncio
import random
from datetime import datetime, date
from dental_system.supabase.client import supabase_client


# Obtener cliente
supabase = supabase_client.get_client()

async def poblar_consultas_hoy():
    """📅 Crear 10 consultas para hoy con datos existentes"""
    print("Creando consultas para hoy...")
    
    try:
        # Obtener odontólogos existentes
        personal_result = supabase.table("personal").select("id").eq("tipo_personal", "Odontólogo").eq("estado_laboral", "activo").execute()
        if not personal_result.data:
            print("❌ No hay odontólogos en la base de datos. Ejecuta el poblado completo primero.")
            return
            
        odontologos = [p["id"] for p in personal_result.data]
        
        # Obtener pacientes existentes
        pacientes_result = supabase.table("pacientes").select("id").eq("activo", True).limit(20).execute()
        if not pacientes_result.data:
            print("❌ No hay pacientes en la base de datos. Ejecuta el poblado completo primero.")
            return
            
        pacientes = [p["id"] for p in pacientes_result.data]
        
        # Obtener administradores (usuario_id, no personal_id)
        admin_result = supabase.table("personal").select("usuario_id").eq("tipo_personal", "Administrador").execute()
        admin_id = admin_result.data[0]["usuario_id"] if admin_result.data else None
        
        print(f"👨‍⚕️ Odontólogos disponibles: {len(odontologos)}")
        print(f"👥 Pacientes disponibles: {len(pacientes)}")
        
        # Crear 10 consultas para hoy
        motivos = [
            "Control rutinario", "Dolor de muela", "Limpieza dental", 
            "Consulta urgente", "Revisión de tratamiento", "Sangrado de encías",
            "Sensibilidad dental", "Consulta preventiva"
        ]
        
        horas = ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", 
                "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]
        
        for i in range(10):
            try:
                consulta_data = {
                    "paciente_id": random.choice(pacientes),
                    "primer_odontologo_id": random.choice(odontologos),
                    "fecha_llegada": f"{date.today()} {random.choice(horas)}:00",
                    "tipo_consulta": random.choice(["general", "control", "urgencia"]),
                    "motivo_consulta": random.choice(motivos),
                    "estado": "en_espera",
                    "prioridad": "normal",
                    "creada_por": admin_id
                }
                
                result = supabase.table("consultas").insert(consulta_data).execute()
                
                if result.data:
                    print(f"✅ Consulta {i+1} creada - {consulta_data['motivo_consulta']}")
                    
            except Exception as e:
                print(f"❌ Error en consulta {i+1}: {e}")
        
        print(f"\n🎉 ¡Listo! Creadas 10 consultas para hoy")
        print("🔗 Ahora puedes ver las colas en tiempo real en tu sistema")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(poblar_consultas_hoy())