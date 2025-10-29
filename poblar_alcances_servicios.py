# -*- coding: utf-8 -*-
"""
Script para poblar alcances de servicios existentes
====================================================

Actualiza servicios con el alcance correcto según su naturaleza.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dental_system.supabase.client import get_client

def poblar_alcances():
    """Actualizar alcances de servicios existentes"""

    client = get_client()

    print("\n" + "="*80)
    print("🔧 ACTUALIZANDO ALCANCES DE SERVICIOS")
    print("="*80 + "\n")

    # PASO 1: Servicios de diente completo
    servicios_diente_completo = [
        "extraccion", "exodoncia", "implante", "corona",
        "endodoncia", "incrustacion", "perno", "pivot"
    ]

    print("📋 Actualizando servicios de DIENTE COMPLETO...")
    for keyword in servicios_diente_completo:
        try:
            response = client.table("servicios")\
                .update({"alcance_servicio": "diente_completo"})\
                .ilike("nombre", f"%{keyword}%")\
                .execute()

            if response.data:
                print(f"   ✅ {len(response.data)} servicios con '{keyword}' → diente_completo")
        except Exception as e:
            print(f"   ❌ Error con '{keyword}': {e}")

    # PASO 2: Servicios de boca completa
    servicios_boca_completa = [
        "blanqueamiento", "limpieza", "profilaxis",
        "fluorizacion", "sellante", "control", "consulta general"
    ]

    print("\n📋 Actualizando servicios de BOCA COMPLETA...")
    for keyword in servicios_boca_completa:
        try:
            response = client.table("servicios")\
                .update({"alcance_servicio": "boca_completa"})\
                .ilike("nombre", f"%{keyword}%")\
                .execute()

            if response.data:
                print(f"   ✅ {len(response.data)} servicios con '{keyword}' → boca_completa")
        except Exception as e:
            print(f"   ❌ Error con '{keyword}': {e}")

    # PASO 3: Verificar distribución final
    print("\n📊 DISTRIBUCIÓN FINAL POR ALCANCE:")
    print("-" * 80)

    try:
        # Contar por alcance
        for alcance in ["superficie_especifica", "diente_completo", "boca_completa"]:
            response = client.table("servicios")\
                .select("id, nombre", count="exact")\
                .eq("alcance_servicio", alcance)\
                .execute()

            count = response.count if hasattr(response, 'count') else len(response.data)
            icon_map = {
                "superficie_especifica": "🎯",
                "diente_completo": "🦷",
                "boca_completa": "👄"
            }

            print(f"{icon_map[alcance]} {alcance.replace('_', ' ').title()}: {count} servicios")

            # Mostrar primeros 3 ejemplos
            if response.data and len(response.data) > 0:
                ejemplos = [s['nombre'] for s in response.data[:3]]
                print(f"   Ejemplos: {', '.join(ejemplos)}")

    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")

    print("\n" + "="*80)
    print("✅ ACTUALIZACIÓN COMPLETADA")
    print("="*80 + "\n")

if __name__ == "__main__":
    poblar_alcances()
