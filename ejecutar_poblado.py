#!/usr/bin/env python3
"""
🎬 EJECUTOR SIMPLE DE POBLADO DE DATOS
=====================================

Script simple para ejecutar el poblado de datos sin complicaciones.
Solo ejecuta: python ejecutar_poblado.py
"""

import asyncio
import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def ejecutar_poblado_simple():
    """🎬 Ejecutar poblado de forma simple"""
    print("🏥 CLÍNICA DENTAL ODONTOMARVA - POBLADO DE DATOS")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        # Importar y ejecutar
        from poblar_datos_clinica import PobladorDatosClinica
        
        print("🚀 Iniciando poblado automático...")
        poblador = PobladorDatosClinica()
        await poblador.poblar_todo()
        
        print("\n🎉 ¡POBLADO COMPLETADO EXITOSAMENTE!")
        print("✅ Ahora tu sistema tiene datos realistas para probar")
        print("🔗 Puedes ejecutar 'reflex run' para ver el sistema funcionando")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de estar en el directorio correcto del proyecto")
        
    except Exception as e:
        print(f"❌ Error durante el poblado: {e}")
        print("💡 Revisa la conexión a la base de datos y los servicios")

if __name__ == "__main__":
    # Ejecutar sin preguntas
    asyncio.run(ejecutar_poblado_simple())