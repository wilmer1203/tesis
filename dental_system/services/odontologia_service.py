"""
🦷 SERVICIO DE ODONTOLOGÍA V2.0 - MODELO PLANO SIMPLIFICADO
===========================================================

Versión simplificada sin sistema de versiones complejo.
Arquitectura directa: paciente → condiciones_diente

CAMBIOS PRINCIPALES:
- ❌ Eliminada tabla odontograma intermedia
- ✅ Relación directa paciente_id en condiciones_diente
- ✅ Campo activo (true/false) en vez de sistema de versiones
- ✅ Auto-creación de odontograma al crear paciente (trigger SQL)
- ✅ Historial completo via activo = false

FUNCIONALIDADES:
- Cargar odontograma actual del paciente
- Actualizar condición de diente (mantiene historial automáticamente)
- Ver historial completo de un diente
- Ver intervenciones realizadas
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from .base_service import BaseService
from dental_system.supabase.client import supabase_client
import logging

logger = logging.getLogger(__name__)

# Colores estándar por condición
CONDICIONES_COLORES = {
    "sano": "#90EE90",           # Verde claro
    "caries": "#FF6B6B",         # Rojo
    "obturacion": "#C0C0C0",     # Plateado
    "corona": "#FFD700",         # Dorado
    "endodoncia": "#FF8C00",     # Naranja
    "puente": "#9370DB",         # Púrpura
    "implante": "#32CD32",       # Verde lima
    "ausente": "#D3D3D3",        # Gris claro
    "extraccion_indicada": "#DC143C",  # Rojo oscuro
    "fractura": "#FF4500",       # Naranja rojizo
    "protesis": "#DDA0DD",       # Ciruela
}

# Dientes FDI adulto (32 dientes)
DIENTES_FDI_ADULTO = [
    18, 17, 16, 15, 14, 13, 12, 11,  # Cuadrante 1 (Superior Derecho)
    21, 22, 23, 24, 25, 26, 27, 28,  # Cuadrante 2 (Superior Izquierdo)
    31, 32, 33, 34, 35, 36, 37, 38,  # Cuadrante 3 (Inferior Izquierdo)
    41, 42, 43, 44, 45, 46, 47, 48   # Cuadrante 4 (Inferior Derecho)
]

# Superficies dentales
SUPERFICIES = ["oclusal", "mesial", "distal", "vestibular", "lingual"]


class OdontologiaServiceV2(BaseService):
    """
    Servicio simplificado de odontología con modelo plano
    """

    def __init__(self):
        super().__init__()
        self.client = supabase_client.get_client()

    # ==========================================
    # 🦷 CARGAR ODONTOGRAMA ACTUAL
    # ==========================================

    async def get_patient_odontogram(self, paciente_id: str) -> Dict[str, Any]:
        """
        📋 Obtener odontograma ACTUAL del paciente

        SIMPLIFICADO: Query directo a condiciones_diente con activo = TRUE

        Args:
            paciente_id: ID del paciente (UUID)

        Returns:
            {
                "conditions": {
                    11: {"oclusal": "sano", "mesial": "sano", ...},
                    12: {"oclusal": "obturacion", "mesial": "caries", ...},
                    ...
                },
                "total_dientes": 32,
                "total_condiciones": 160,
                "fecha_ultima_actualizacion": "2025-10-07T10:30:00"
            }
        """
        try:
            logger.info(f"📋 Cargando odontograma actual para paciente {paciente_id}")

            # Query simple: solo condiciones activas
            response = self.client.table("condiciones_diente").select(
                "diente_numero, superficie, tipo_condicion, color_hex, fecha_registro, material_utilizado"
            ).eq("paciente_id", paciente_id).eq("activo", True).execute()

            if not response.data:
                logger.warning(f"⚠️ Paciente {paciente_id} sin odontograma. Se creará automáticamente al crear paciente.")
                return {
                    "conditions": {},
                    "total_dientes": 0,
                    "total_condiciones": 0,
                    "mensaje": "Odontograma no inicializado"
                }

            # Organizar por diente y superficie
            conditions = {}
            fecha_mas_reciente = None

            for cond in response.data:
                diente = cond['diente_numero']
                superficie = cond['superficie']

                if diente not in conditions:
                    conditions[diente] = {}

                conditions[diente][superficie] = {
                    "condicion": cond['tipo_condicion'],
                    "color": cond.get('color_hex', CONDICIONES_COLORES.get(cond['tipo_condicion'], '#FFFFFF')),
                    "material": cond.get('material_utilizado')
                }

                # Tracking fecha más reciente
                fecha = cond.get('fecha_registro')
                if fecha and (not fecha_mas_reciente or fecha > fecha_mas_reciente):
                    fecha_mas_reciente = fecha

            logger.info(f"✅ Odontograma cargado: {len(conditions)} dientes, {len(response.data)} condiciones")

            return {
                "conditions": conditions,
                "total_dientes": len(conditions),
                "total_condiciones": len(response.data),
                "fecha_ultima_actualizacion": fecha_mas_reciente
            }

        except Exception as e:
            logger.error(f"❌ Error cargando odontograma: {str(e)}")
            raise ValueError(f"Error al cargar odontograma: {str(e)}")

    # ==========================================
    # ✏️ ACTUALIZAR CONDICIÓN DE DIENTE
    # ==========================================

    async def actualizar_condicion_diente(
        self,
        paciente_id: str,
        diente_numero: int,
        superficie: str,
        nueva_condicion: str,
        intervencion_id: Optional[str] = None,
        material: Optional[str] = None,
        descripcion: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        ✏️ Actualizar condición de un diente

        SIMPLIFICADO: Usa función SQL que automáticamente:
        1. Marca condición anterior como activo = FALSE (historial)
        2. Crea nueva condición con activo = TRUE

        Args:
            paciente_id: ID del paciente
            diente_numero: Número FDI (11-48)
            superficie: oclusal, mesial, distal, vestibular, lingual
            nueva_condicion: sano, caries, obturacion, etc.
            intervencion_id: ID de la intervención que origina el cambio
            material: Material utilizado (opcional)
            descripcion: Descripción del cambio (opcional)

        Returns:
            {"success": True, "condicion_id": "uuid"}
        """
        try:
            logger.info(f"✏️ Actualizando diente {diente_numero} ({superficie}) → {nueva_condicion}")

            # Llamar función SQL que maneja el historial automáticamente
            result = self.client.rpc('actualizar_condicion_diente', {
                'p_paciente_id': paciente_id,
                'p_diente_numero': diente_numero,
                'p_superficie': superficie,
                'p_nueva_condicion': nueva_condicion,
                'p_intervencion_id': intervencion_id,
                'p_material': material,
                'p_descripcion': descripcion,
                'p_registrado_por': self.current_user_id
            }).execute()

            nueva_condicion_id = result.data

            logger.info(f"✅ Condición actualizada correctamente: {nueva_condicion_id}")

            return {
                "success": True,
                "condicion_id": nueva_condicion_id,
                "diente": diente_numero,
                "superficie": superficie,
                "condicion": nueva_condicion
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando condición: {str(e)}")
            raise ValueError(f"Error al actualizar condición: {str(e)}")

    # ==========================================
    # 📜 HISTORIAL DE UN DIENTE
    # ==========================================

    async def get_historial_diente(
        self,
        paciente_id: str,
        diente_numero: int
    ) -> List[Dict[str, Any]]:
        """
        📜 Obtener historial COMPLETO de un diente

        Incluye condiciones activas E históricas (activo = true y false)

        Args:
            paciente_id: ID del paciente
            diente_numero: Número FDI del diente

        Returns:
            Lista de cambios ordenados por fecha (más reciente primero)
        """
        try:
            logger.info(f"📜 Obteniendo historial del diente {diente_numero}")

            response = self.client.table("condiciones_diente").select("""
                id,
                superficie,
                tipo_condicion,
                material_utilizado,
                descripcion,
                fecha_registro,
                activo,
                intervencion_id
            """).eq("paciente_id", paciente_id).eq(
                "diente_numero", diente_numero
            ).order("fecha_registro", desc=True).execute()

            historial = []
            for cond in response.data:
                historial.append({
                    "fecha": cond['fecha_registro'],
                    "superficie": cond['superficie'],
                    "condicion": cond['tipo_condicion'],
                    "material": cond.get('material_utilizado'),
                    "descripcion": cond.get('descripcion'),
                    "es_actual": cond['activo'],
                    "intervencion_id": cond.get('intervencion_id')
                })

            logger.info(f"✅ Historial obtenido: {len(historial)} registros")
            return historial

        except Exception as e:
            logger.error(f"❌ Error obteniendo historial: {str(e)}")
            return []

    # ==========================================
    # 📊 INTERVENCIONES DEL PACIENTE
    # ==========================================

    async def get_intervenciones_paciente(
        self,
        paciente_id: str
    ) -> List[Dict[str, Any]]:
        """
        📊 Obtener intervenciones realizadas al paciente

        Agrupa condiciones por intervención para mostrar "qué se hizo en cada visita"

        Returns:
            Lista de intervenciones con dientes tratados
        """
        try:
            logger.info(f"📊 Obteniendo intervenciones del paciente {paciente_id}")

            # Obtener todas las condiciones del paciente agrupadas por intervención
            response = self.client.table("condiciones_diente").select("""
                intervencion_id,
                diente_numero,
                superficie,
                tipo_condicion,
                material_utilizado,
                fecha_registro
            """).eq("paciente_id", paciente_id).not_.is_(
                "intervencion_id", "null"
            ).order("fecha_registro", desc=True).execute()

            # Agrupar por intervención
            intervenciones_dict = {}
            for cond in response.data:
                interv_id = cond['intervencion_id']

                if interv_id not in intervenciones_dict:
                    intervenciones_dict[interv_id] = {
                        "intervencion_id": interv_id,
                        "fecha": cond['fecha_registro'],
                        "dientes_tratados": set(),
                        "detalles": []
                    }

                intervenciones_dict[interv_id]["dientes_tratados"].add(cond['diente_numero'])
                intervenciones_dict[interv_id]["detalles"].append({
                    "diente": cond['diente_numero'],
                    "superficie": cond['superficie'],
                    "condicion": cond['tipo_condicion'],
                    "material": cond.get('material_utilizado')
                })

            # Convertir a lista
            intervenciones = [
                {
                    **interv,
                    "dientes_tratados": sorted(list(interv["dientes_tratados"]))
                }
                for interv in intervenciones_dict.values()
            ]

            logger.info(f"✅ Obtenidas {len(intervenciones)} intervenciones")
            return intervenciones

        except Exception as e:
            logger.error(f"❌ Error obteniendo intervenciones: {str(e)}")
            return []

    # ==========================================
    # 📈 ESTADÍSTICAS DEL ODONTOGRAMA
    # ==========================================

    async def get_estadisticas_odontograma(
        self,
        paciente_id: str
    ) -> Dict[str, Any]:
        """
        📈 Estadísticas del odontograma actual

        Returns:
            Conteo de dientes por condición
        """
        try:
            response = self.client.table("condiciones_diente").select(
                "tipo_condicion"
            ).eq("paciente_id", paciente_id).eq("activo", True).execute()

            # Contar por tipo de condición
            stats = {}
            for cond in response.data:
                tipo = cond['tipo_condicion']
                stats[tipo] = stats.get(tipo, 0) + 1

            return {
                "total_superficies": len(response.data),
                "por_condicion": stats,
                "dientes_sanos": stats.get("sano", 0) // 5,  # Aprox (5 superficies por diente)
                "dientes_con_problemas": (len(response.data) - stats.get("sano", 0)) // 5
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas: {str(e)}")
            return {}


# Instancia única (compatible con código anterior)
odontologia_service = OdontologiaServiceV2()
OdontologiaService = OdontologiaServiceV2  # Alias para compatibilidad
