"""
🦷 SERVICIO DE ODONTOLOGÍA V2.0 - MODELO PLANO SIMPLIFICADO
===========================================================

Versión simplificada sin sistema de versiones complejo.
Arquitectura directa: paciente → condiciones_diente

CAMBIOS PRINCIPALES:
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
from dental_system.supabase.client import supabase_client, get_client
import logging
import re

logger = logging.getLogger(__name__)



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
            response = self.client.table("diente").select(
                "diente_numero, superficie, tipo_condicion, color_hex, fecha_registro"
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

                # SIMPLIFICADO: Solo almacenar el string de condición
                # El color se obtiene dinámicamente en get_surface_color()
                conditions[diente][superficie] = cond['tipo_condicion']

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

            response = self.client.table("diente").select("""
                id,
                superficie,
                tipo_condicion,
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
            response = self.client.table("diente").select("""
                intervencion_id,
                diente_numero,
                superficie,
                tipo_condicion,
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
            response = self.client.table("diente").select(
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

    # ==========================================
    # ✨ V3.0: CATÁLOGO DE CONDICIONES Y BATCH UPDATE
    # ==========================================
    
    async def actualizar_condiciones_batch(
        self,
        actualizaciones: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        ✨ V3.0: Actualizar múltiples condiciones dentales en 1 transacción

        Este método llama a la función SQL actualizar_condiciones_batch() que:
        1. Marca condiciones anteriores como activo=FALSE (histórico)
        2. Inserta nuevas condiciones como activo=TRUE
        3. Todo en una sola transacción (atomicidad)

        Args:
            actualizaciones: Lista de dicts con:
                - paciente_id: UUID del paciente
                - diente_numero: Número FDI (11-48)
                - superficie: oclusal, mesial, distal, vestibular, lingual
                - nueva_condicion: Código de condición del catálogo
                - intervencion_id: UUID de la intervención
                - material: Material utilizado (opcional)
                - descripcion: Descripción del cambio (opcional)

        Returns:
            {
                "success": bool,
                "exitosos": int,
                "fallidos": int,
                "ids_creados": List[str]
            }
        """
        try:
            if not actualizaciones:
                logger.warning("⚠️ No hay actualizaciones para procesar")
                return {"success": True, "exitosos": 0, "fallidos": 0, "ids_creados": []}

            logger.info(f"🔄 Procesando {len(actualizaciones)} actualizaciones en batch")

            # Agregar registrado_por a cada actualización
            for upd in actualizaciones:
                upd["registrado_por"] = self.current_user_id or ""

            # ✅ CORRECCIÓN: Enviar array de Python directamente
            # Supabase convierte automáticamente a JSONB
            print(f"🔧 DEBUG: Enviando {len(actualizaciones)} actualizaciones como array Python")

            # MOSTRAR CADA ACTUALIZACIÓN EN DETALLE
            print("\n📋 DATOS COMPLETOS QUE SE ENVÍAN:")
            for i, upd in enumerate(actualizaciones, 1):
                print(f"\n  Actualización #{i}:")
                print(f"    paciente_id: {upd.get('paciente_id')} (tipo: {type(upd.get('paciente_id'))})")
                print(f"    diente_numero: {upd.get('diente_numero')} (tipo: {type(upd.get('diente_numero'))})")
                print(f"    superficie: {upd.get('superficie')} (tipo: {type(upd.get('superficie'))})")
                print(f"    tipo_condicion: {upd.get('tipo_condicion')} (tipo: {type(upd.get('tipo_condicion'))})")
                print(f"    descripcion: {upd.get('descripcion')}")
                print(f"    intervencion_id: {upd.get('intervencion_id')} (tipo: {type(upd.get('intervencion_id'))})")
                print(f"    registrado_por: {upd.get('registrado_por')}")

            # ✅ IMPLEMENTACIÓN DIRECTA EN PYTHON (sin función SQL)
            exitosos = 0
            fallidos = 0
            ids_creados = []

            logger.info("🔄 Procesando actualizaciones directamente en Python...")

            for i, upd in enumerate(actualizaciones, 1):
                try:
                    logger.info(f"\n📝 Procesando actualización {i}/{len(actualizaciones)}:")
                    logger.info(f"   Diente: {upd.get('diente_numero')} - Superficie: {upd.get('superficie')}")
                    logger.info(f"   Nueva condición: {upd.get('tipo_condicion')}")

                    # PASO 1: Desactivar condición anterior (si existe)
                    update_result = self.client.table('diente').update({
                        'activo': False
                    }).eq('paciente_id', upd['paciente_id'])\
                      .eq('diente_numero', upd['diente_numero'])\
                      .eq('superficie', upd['superficie'])\
                      .eq('activo', True).execute()

                    logger.info(f"   ✅ Desactivadas {len(update_result.data)} condiciones anteriores")

                    # PASO 2: Insertar nueva condición (activa)
                    nueva_condicion = {
                        'paciente_id': upd['paciente_id'],
                        'diente_numero': upd['diente_numero'],
                        'superficie': upd['superficie'],
                        'tipo_condicion': upd['tipo_condicion'],
                        'intervencion_id': upd.get('intervencion_id'),
                        'activo': True
                    }

                    insert_result = self.client.table('diente').insert(
                        nueva_condicion
                    ).execute()

                    if insert_result.data:
                        nuevo_id = insert_result.data[0]['id']
                        ids_creados.append(nuevo_id)
                        exitosos += 1
                        logger.info(f"   ✅ Nueva condición creada: {nuevo_id}")
                    else:
                        fallidos += 1
                        logger.warning(f"   ⚠️ No se obtuvo ID de la nueva condición")

                except Exception as e:
                    fallidos += 1
                    logger.error(f"   ❌ Error en actualización {i}: {str(e)}")
                    import traceback
                    traceback.print_exc()

            # Resultado final
            logger.info(f"\n✅ Batch completado: {exitosos} exitosos, {fallidos} fallidos")

            return {
                "success": fallidos == 0,
                "exitosos": exitosos,
                "fallidos": fallidos,
                "ids_creados": [str(id) for id in ids_creados]
            }

        except Exception as e:
            logger.error(f"❌ Error en batch update: {str(e)}")
            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "exitosos": 0,
                "fallidos": len(actualizaciones),
                "ids_creados": [],
                "error": str(e)
            }

    # ==========================================
    # 💾 CREAR INTERVENCIÓN CON SERVICIOS
    # ==========================================

    async def crear_intervencion_con_servicios(self, datos_intervencion: Dict[str, Any]) -> Dict[str, Any]:
        """
        💾 Crear intervención con múltiples servicios

        ARQUITECTURA V2.0:
        - Crea 1 registro en intervenciones
        - Crea N registros en intervenciones_servicios (uno por diente/superficie)
        - Usa campos actualizados: diente_numero, superficie

        Args:
            datos_intervencion: {
                "consulta_id": str,
                "odontologo_id": str,  # ID del usuario (se convierte a personal_id)
                "servicios": [
                    {
                        "servicio_id": str,
                        "cantidad": int,
                        "precio_unitario_bs": float,
                        "precio_unitario_usd": float,
                        "dientes_texto": str,           # "11, 12, 21"
                        "material_utilizado": str,
                        "superficie": str,              # "oclusal", "completa", etc.
                        "observaciones": str
                    }
                ],
                "observaciones_generales": str,
                "requiere_control": bool
            }

        Returns:
            {
                "success": True,
                "intervencion_id": "uuid",
                "total_bs": float,
                "total_usd": float,
                "servicios_count": int,
                "registros_creados": int
            }
        """
        try:
            logger.info("🚀 Iniciando creación de intervención con servicios V2.0")

            # === VALIDACIONES BÁSICAS ===
            consulta_id = datos_intervencion.get("consulta_id")
            if not consulta_id:
                raise ValueError("consulta_id es requerido")

            servicios = datos_intervencion.get("servicios", [])
            if not servicios:
                raise ValueError("Al menos un servicio es requerido")

            odontologo_user_id = datos_intervencion.get("odontologo_id")
            if not odontologo_user_id:
                raise ValueError("odontologo_id es requerido")

            # === CONVERSIÓN USUARIO → PERSONAL ===
            personal_response = self.client.table("personal").select("id").eq(
                "usuario_id", odontologo_user_id
            ).execute()

            if not personal_response.data:
                raise ValueError(f"No se encontró personal asociado al usuario {odontologo_user_id}")

            personal_id = personal_response.data[0]["id"]
            logger.info(f"🔄 Conversión: usuario {odontologo_user_id} → personal {personal_id}")

            # === CALCULAR TOTALES ===
            total_bs = sum(
                float(servicio.get("precio_unitario_bs", 0)) * int(servicio.get("cantidad", 1))
                for servicio in servicios
            )
            total_usd = sum(
                float(servicio.get("precio_unitario_usd", 0)) * int(servicio.get("cantidad", 1))
                for servicio in servicios
            )

            logger.info(f"💰 Totales calculados: BS {total_bs:,.2f}, USD ${total_usd:,.2f}")

            # === RECOPILAR DIENTES ÚNICOS ===
            # ✅ CORRECCIÓN V2.2: Diferenciar entre boca completa y dientes específicos
            dientes_todos = []
            tiene_boca_completa = False

            for servicio in servicios:
                alcance = servicio.get("alcance", "superficie_especifica")

                # Detectar si algún servicio es de boca completa
                if alcance == "boca_completa":
                    tiene_boca_completa = True
                    continue  # No agregar dientes individuales

                # Para diente_completo y superficie_especifica, agregar dientes
                dientes_texto = servicio.get("dientes_texto", "")
                if dientes_texto.strip():
                    try:
                        dientes_servicio = self._extraer_numeros_dientes(dientes_texto)
                        dientes_todos.extend(dientes_servicio)
                    except Exception as e:
                        logger.warning(f"Error parseando dientes '{dientes_texto}': {e}")

            # Determinar valor final de dientes_afectados
            if tiene_boca_completa:
                dientes_unicos = None  # NULL = boca completa
                logger.info(f"🦷 Dientes afectados: BOCA COMPLETA (NULL)")
            else:
                dientes_unicos = sorted(list(set(dientes_todos))) if dientes_todos else []
                logger.info(f"🦷 Dientes afectados específicos: {dientes_unicos}")

            # === CREAR INTERVENCIÓN PRINCIPAL ===
            # 🔧 NOTA: No incluimos fecha_inicio/fecha_fin/hora_inicio/hora_fin
            # Supabase usará los valores por defecto de la tabla
            intervencion_data = {
                "consulta_id": consulta_id,
                "odontologo_id": personal_id,
                "procedimiento_realizado": datos_intervencion.get(
                    "observaciones_generales",
                    f"Intervención con {len(servicios)} servicios"
                ),
                "total_bs": float(total_bs),
                "total_usd": float(total_usd),
                "estado": "completada"
            }

            nueva_intervencion = self.client.table("intervencion").insert(
                intervencion_data
            ).execute()

            if not nueva_intervencion.data:
                raise ValueError("Error creando intervención principal")

            intervencion_id = nueva_intervencion.data[0]["id"]
            logger.info(f"✅ Intervención principal creada: {intervencion_id}")

            # === CREAR REGISTROS EN INTERVENCIONES_SERVICIOS ===
            # ✅ CORRECCIÓN V2.2: Lógica diferenciada por alcance del servicio
            registros_creados = 0

            for servicio in servicios:
                try:
                    servicio_id = servicio.get("servicio_id")
                    precio_unitario_bs = float(servicio.get("precio_unitario_bs", 0))
                    precio_unitario_usd = float(servicio.get("precio_unitario_usd", 0))
                    alcance = servicio.get("alcance", "superficie_especifica")

                    # Preparar observaciones base (incluir material)
                    observaciones_base = servicio.get("observaciones", "")
                    material = servicio.get("material_utilizado", "")

                    # ✅ ESCENARIO 1: BOCA COMPLETA (Blanqueamiento, Limpieza General)
                    if alcance == "boca_completa":
                        observaciones_completa = "Servicio aplicado a boca completa."
                        if material:
                            observaciones_completa += f" Material: {material}."
                        if observaciones_base:
                            observaciones_completa += f" {observaciones_base}"

                        # UN SOLO REGISTRO con diente_numero=NULL, superficie=NULL
                        registro = {
                            "intervencion_id": intervencion_id,
                            "servicio_id": servicio_id,
                            "precio_unitario_bs": precio_unitario_bs,
                            "precio_unitario_usd": precio_unitario_usd,
                            "precio_total_bs": precio_unitario_bs,
                            "precio_total_usd": precio_unitario_usd,
                            "diente_numero": None,  # NULL = boca completa
                            "superficie": None      # NULL = todas las superficies
                        }

                        response = self.client.table("historia_medica").insert(registro).execute()
                        if response.data:
                            registros_creados += 1
                            logger.info(f"✅ Servicio boca completa creado: {servicio_id}")

                    # ✅ ESCENARIO 2: DIENTE COMPLETO (Obturación, Corona, Extracción)
                    elif alcance == "diente_completo":
                        dientes_texto = servicio.get("dientes_texto", "")
                        dientes_servicio = []
                        if dientes_texto.strip():
                            dientes_servicio = self._extraer_numeros_dientes(dientes_texto)

                        if not dientes_servicio:
                            logger.warning(f"⚠️ Servicio diente_completo sin dientes específicos: {servicio_id}")
                            continue

                        # UN REGISTRO por cada diente con superficie=NULL
                        for diente_num in dientes_servicio:
                            observaciones_completa = f"Servicio aplicado a diente {diente_num} completo."
                            if material:
                                observaciones_completa += f" Material: {material}."
                            if observaciones_base:
                                observaciones_completa += f" {observaciones_base}"

                            registro = {
                                "intervencion_id": intervencion_id,
                                "servicio_id": servicio_id,
                                "precio_unitario_bs": precio_unitario_bs,
                                "precio_unitario_usd": precio_unitario_usd,
                                "precio_total_bs": precio_unitario_bs,
                                "precio_total_usd": precio_unitario_usd,
                                "diente_numero": diente_num,
                                "superficie": None  # NULL = diente completo
                            }

                            response = self.client.table("historia_medica").insert(registro).execute()
                            if response.data:
                                registros_creados += 1
                                logger.debug(f"✅ Servicio diente completo creado: {diente_num}")

                    # ✅ ESCENARIO 3: SUPERFICIE ESPECÍFICA (Caries, Resina)
                    else:  # superficie_especifica
                        dientes_texto = servicio.get("dientes_texto", "")
                        dientes_servicio = []
                        if dientes_texto.strip():
                            dientes_servicio = self._extraer_numeros_dientes(dientes_texto)

                        if not dientes_servicio:
                            logger.warning(f"⚠️ Servicio superficie_especifica sin dientes: {servicio_id}")
                            continue

                        # Parsear superficies específicas (sin expansión)
                        superficie_str = servicio.get("superficie", "")
                        superficies = self._mapear_superficie_especifica(superficie_str)

                        if not superficies:
                            # Fallback: Si no hay superficie, asumir "oclusal"
                            superficies = ["oclusal"]
                            logger.debug(f"⚠️ Sin superficie específica, usando oclusal por defecto")

                        # UN REGISTRO por cada combinación diente+superficie
                        for diente_num in dientes_servicio:
                            for superficie in superficies:
                                observaciones_completa = f"Servicio aplicado a diente {diente_num}, superficie {superficie}."
                                if material:
                                    observaciones_completa += f" Material: {material}."
                                if observaciones_base:
                                    observaciones_completa += f" {observaciones_base}"

                                registro = {
                                    "intervencion_id": intervencion_id,
                                    "servicio_id": servicio_id,
                                    "precio_unitario_bs": precio_unitario_bs,
                                    "precio_unitario_usd": precio_unitario_usd,
                                    "precio_total_bs": precio_unitario_bs,
                                    "precio_total_usd": precio_unitario_usd,
                                    "diente_numero": diente_num,
                                    "superficie": superficie
                                }

                                response = self.client.table("historia_medica").insert(registro).execute()
                                if response.data:
                                    registros_creados += 1
                                    logger.debug(f"✅ Servicio superficie creado: {diente_num}-{superficie}")

                except Exception as e:
                    logger.error(f"❌ Error procesando servicio {servicio.get('servicio_id')}: {e}")
                    continue

            logger.info(f"📋 Registros creados en intervenciones_servicios: {registros_creados}")

            # === RETORNAR RESULTADO ===
            return {
                "success": True,
                "intervencion_id": intervencion_id,
                "total_bs": total_bs,
                "total_usd": total_usd,
                "servicios_count": len(servicios),
                "registros_creados": registros_creados,
                "message": f"Intervención creada con {registros_creados} registros de servicios"
            }

        except Exception as e:
            logger.error(f"❌ Error creando intervención con servicios: {str(e)}")
            raise ValueError(f"Error inesperado: {str(e)}")

    # ==========================================
    # 🔧 MÉTODOS HELPER
    # ==========================================

    def _extraer_numeros_dientes(self, texto_dientes: str) -> List[int]:
        """
        🦷 Extraer números de dientes válidos del texto

        Args:
            texto_dientes: "11, 12, 21" o "todos" o "toda la boca"

        Returns:
            Lista de números FDI válidos [11, 12, 21]
        """
        if not texto_dientes:
            return []

        # Casos especiales: toda la boca
        if "todos" in texto_dientes.lower() or "toda" in texto_dientes.lower():
            return DIENTES_FDI_ADULTO

        # Extraer números usando regex (patrón FDI: 11-48)
        numeros = re.findall(r'\b([1-4][1-8])\b', texto_dientes)

        # Validar y convertir
        dientes_validos = []
        for num_str in numeros:
            num = int(num_str)
            if num in DIENTES_FDI_ADULTO:
                dientes_validos.append(num)

        return dientes_validos

    def _mapear_superficie(self, superficie_str: str) -> List[str]:
        """
        🦷 Mapear superficie dental a lista de superficies BD

        ⚠️ DEPRECATED: Usar _mapear_superficie_especifica para evitar expansión no deseada

        Args:
            superficie_str: "oclusal", "completa", "todas", etc.

        Returns:
            Lista de superficies ["oclusal"] o ["oclusal", "mesial", ...]
        """
        if not superficie_str:
            return SUPERFICIES

        superficie_lower = superficie_str.lower().strip()

        # Mapeo de nombres comunes
        mapeo = {
            "oclusal": ["oclusal"],
            "mesial": ["mesial"],
            "distal": ["distal"],
            "vestibular": ["vestibular"],
            "lingual": ["lingual"],
            "palatino": ["lingual"],
            "completa": SUPERFICIES,
            "todas": SUPERFICIES,
            "todo": SUPERFICIES,
            "no específica": SUPERFICIES
        }

        return mapeo.get(superficie_lower, SUPERFICIES)

    def _mapear_superficie_especifica(self, superficie_str: str) -> List[str]:
        """
        🦷 V2.2: Mapear SOLO superficies específicas (sin expansión automática)

        Diferencia con _mapear_superficie:
        - NO expande "completa" a todas las superficies
        - Retorna lista vacía para valores nulos/vacíos (en vez de SUPERFICIES)
        - Pensado para usar con campo "alcance" explícito

        Args:
            superficie_str: "oclusal", "mesial, distal", etc.

        Returns:
            Lista de superficies específicas ["oclusal"] o ["mesial", "distal"]
            Lista vacía [] si no hay superficie específica
        """
        if not superficie_str:
            return []

        superficie_lower = superficie_str.lower().strip()

        # Mapeo ESTRICTO (sin expansión a "completa")
        mapeo_simple = {
            "oclusal": ["oclusal"],
            "mesial": ["mesial"],
            "distal": ["distal"],
            "vestibular": ["vestibular"],
            "lingual": ["lingual"],
            "palatino": ["lingual"],
        }

        # Si es combinación (ej: "oclusal, mesial")
        if "," in superficie_str:
            superficies = [s.strip() for s in superficie_str.split(",") if s.strip()]
            # Validar que todas sean superficies válidas
            return [s for s in superficies if s in ["oclusal", "mesial", "distal", "vestibular", "lingual", "palatino"]]

        # Mapeo simple
        return mapeo_simple.get(superficie_lower, [])

    async def get_historial_servicios_paciente(self, paciente_id: str) -> List[Dict[str, Any]]:
        """
        Obtener historial de servicios del paciente (uno por card).
        Retorna lista ordenada por fecha (más reciente primero).
        """
        try:
            logger.info(f"📋 Cargando historial de servicios para paciente {paciente_id}")

            # Query con joins necesarios (ordenamiento en Python porque PostgREST no lo soporta en relaciones)
            response = self.client.table("historia_medica").select("""
                id,
                diente_numero,
                superficie,
                intervencion!inner(
                    id,
                    fecha_registro,
                    odontologo_id,
                    procedimiento_realizado,
                    consulta!inner(
                        paciente_id
                    )
                ),
                servicio!inner(
                    nombre,
                    categoria,
                    alcance_servicio
                )
            """).eq("intervencion.consulta.paciente_id", paciente_id).execute()

            logger.info(f"📊 Historial: {len(response.data)} registros encontrados")

            servicios_historial = []

            for servicio_data in response.data:
                odontologo_id = servicio_data["intervencion"]["odontologo_id"]
                odontologo_info = await self._get_personal_info(odontologo_id)

                superficies = []
                if servicio_data.get("superficie"):
                    superficies = [s.strip() for s in servicio_data["superficie"].split(",")]

                item = {
                    "id": servicio_data["id"],
                    "fecha": servicio_data["intervencion"]["fecha_registro"],
                    "odontologo_nombre": odontologo_info.get("nombre_completo", "Sin nombre"),
                    "especialidad": odontologo_info.get("especialidad", "General"),
                    "diente_numero": servicio_data.get("diente_numero"),
                    "diente_nombre": self._get_diente_nombre(servicio_data.get("diente_numero")),
                    "superficies": superficies,
                    "superficies_texto": ", ".join([s.capitalize() for s in superficies]) if superficies else "",
                    "alcance": servicio_data["servicio"]["alcance_servicio"],
                    "servicio_nombre": servicio_data["servicio"]["nombre"],
                    "servicio_categoria": servicio_data["servicio"]["categoria"],
                    "condicion_aplicada": None,
                    "material_utilizado": None,
                    "observaciones": servicio_data["intervencion"].get("procedimiento_realizado", "")
                }

                # Obtener condición aplicada si es un diente específico
                if servicio_data.get("diente_numero"):
                    condicion = await self._get_condicion_por_intervencion(
                        paciente_id,
                        servicio_data.get("diente_numero"),
                        servicio_data["intervencion"]["id"]
                    )
                    if condicion:
                        item["condicion_aplicada"] = condicion.get("tipo_condicion")
                        item["material_utilizado"] = condicion.get("material_utilizado")

                servicios_historial.append(item)

            # Ordenar por fecha (más reciente primero)
            servicios_historial.sort(key=lambda x: x["fecha"], reverse=True)

            logger.info(f"✅ Historial cargado: {len(servicios_historial)} servicios")
            return servicios_historial

        except Exception as e:
            logger.error(f"❌ Error cargando historial de servicios: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def _get_personal_info(self, personal_id: str) -> Dict[str, Any]:
        """🆕 Helper: Obtener info del personal desde vista"""
        try:
            response = self.client.table("vista_personal_completo").select(
                "nombre_completo, especialidad"
            ).eq("id", personal_id).execute()

            return response.data[0] if response.data else {}
        except Exception as e:
            logger.warning(f"Error obteniendo info personal: {e}")
            return {}

    async def _get_condicion_por_intervencion(
        self,
        paciente_id: str,
        diente_numero: int,
        intervencion_id: str
    ) -> Optional[Dict[str, Any]]:
        """🆕 Helper: Obtener condición aplicada en una intervención específica"""
        try:
            response = self.client.table("diente").select(
                "tipo_condicion"
            ).eq("paciente_id", paciente_id
            ).eq("diente_numero", diente_numero
            ).eq("intervencion_id", intervencion_id
            ).eq("activo", True  # Solo la condición actual
            ).execute()

            return response.data[0] if response.data else None
        except Exception as e:
            logger.warning(f"Error obteniendo condición: {e}")
            return None

    def _get_diente_nombre(self, diente_numero: Optional[int]) -> str:
        """🆕 Helper: Nombre legible del diente FDI"""
        if not diente_numero:
            return ""

        nombres_dientes = {
            # Cuadrante 1 (Superior Derecho)
            18: "Tercer Molar Superior Derecho",
            17: "Segundo Molar Superior Derecho",
            16: "Primer Molar Superior Derecho",
            15: "Segundo Premolar Superior Derecho",
            14: "Primer Premolar Superior Derecho",
            13: "Canino Superior Derecho",
            12: "Incisivo Lateral Superior Derecho",
            11: "Incisivo Central Superior Derecho",
            # Cuadrante 2 (Superior Izquierdo)
            21: "Incisivo Central Superior Izquierdo",
            22: "Incisivo Lateral Superior Izquierdo",
            23: "Canino Superior Izquierdo",
            24: "Primer Premolar Superior Izquierdo",
            25: "Segundo Premolar Superior Izquierdo",
            26: "Primer Molar Superior Izquierdo",
            27: "Segundo Molar Superior Izquierdo",
            28: "Tercer Molar Superior Izquierdo",
            # Cuadrante 3 (Inferior Izquierdo)
            38: "Tercer Molar Inferior Izquierdo",
            37: "Segundo Molar Inferior Izquierdo",
            36: "Primer Molar Inferior Izquierdo",
            35: "Segundo Premolar Inferior Izquierdo",
            34: "Primer Premolar Inferior Izquierdo",
            33: "Canino Inferior Izquierdo",
            32: "Incisivo Lateral Inferior Izquierdo",
            31: "Incisivo Central Inferior Izquierdo",
            # Cuadrante 4 (Inferior Derecho)
            41: "Incisivo Central Inferior Derecho",
            42: "Incisivo Lateral Inferior Derecho",
            43: "Canino Inferior Derecho",
            44: "Primer Premolar Inferior Derecho",
            45: "Segundo Premolar Inferior Derecho",
            46: "Primer Molar Inferior Derecho",
            47: "Segundo Molar Inferior Derecho",
            48: "Tercer Molar Inferior Derecho",
        }

        return nombres_dientes.get(diente_numero, f"Diente {diente_numero}")

    # ==========================================
    # 🔄 PACIENTES DISPONIBLES DE OTROS ODONTÓLOGOS
    # ==========================================

    async def get_pacientes_disponibles(self, personal_id: str) -> List[Dict[str, Any]]:
        """
        🔄 Obtener pacientes disponibles de otros odontólogos

        Estos son pacientes que:
        - Tienen consultas en estado "entre_odontologos"
        - Fueron atendidos por OTRO odontólogo
        - Están disponibles para ser tomados por el odontólogo actual

        Args:
            personal_id: ID del odontólogo actual (en tabla personal)

        Returns:
            Lista de pacientes con información de consulta
        """
        try:
            logger.info(f"🔄 Cargando pacientes disponibles para personal {personal_id}")

            # Query con joins para obtener información completa
            response = self.client.table("consulta").select("""
                id,
                numero_consulta,
                paciente_id,
                primer_odontologo_id,
                fecha_llegada,
                estado,
                tipo_consulta,
                motivo_consulta,
                observaciones,
                paciente!inner(
                    id,
                    numero_historia,
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    numero_documento,
                    celular_1,
                    celular_2,
                    email,
                    genero,
                    fecha_nacimiento,
                    alergias
                )
            """).eq(
                "estado", "entre_odontologos"
            ).neq(
                "primer_odontologo_id", personal_id  # Excluir consultas propias
            ).execute()

            if not response.data:
                logger.info("✅ No hay pacientes disponibles de otros odontólogos")
                return []

            # Transformar datos a formato PacienteModel
            pacientes_disponibles = []

            for consulta_data in response.data:
                paciente_info = consulta_data.get("pacientes", {})

                # Construir objeto paciente con información de consulta
                paciente = {
                    # Información del paciente
                    "id": paciente_info.get("id"),
                    "numero_historia": paciente_info.get("numero_historia", ""),
                    "primer_nombre": paciente_info.get("primer_nombre", ""),
                    "segundo_nombre": paciente_info.get("segundo_nombre", ""),
                    "primer_apellido": paciente_info.get("primer_apellido", ""),
                    "segundo_apellido": paciente_info.get("segundo_apellido", ""),
                    "numero_documento": paciente_info.get("numero_documento", ""),
                    "celular_1": paciente_info.get("celular_1", ""),
                    "celular_2": paciente_info.get("celular_2", ""),
                    "email": paciente_info.get("email", ""),
                    "genero": paciente_info.get("genero", ""),
                    "fecha_nacimiento": paciente_info.get("fecha_nacimiento", ""),
                    "edad": paciente_info.get("edad", 0),
                    "alergias": paciente_info.get("alergias", []),

                    # Información de la consulta asociada
                    "consulta_id": consulta_data.get("id"),
                    "consulta_numero": consulta_data.get("numero_consulta", ""),
                    "consulta_estado": consulta_data.get("estado", ""),
                    "motivo_derivacion": consulta_data.get("observaciones", ""),

                    # Nombre completo calculado
                    "nombre_completo": f"{paciente_info.get('primer_nombre', '')} {paciente_info.get('segundo_nombre', '') or ''} {paciente_info.get('primer_apellido', '')} {paciente_info.get('segundo_apellido', '') or ''}".strip()
                }

                pacientes_disponibles.append(paciente)

            logger.info(f"✅ Pacientes disponibles cargados: {len(pacientes_disponibles)}")
            return pacientes_disponibles

        except Exception as e:
            logger.error(f"❌ Error obteniendo pacientes disponibles: {str(e)}")
            import traceback
            traceback.print_exc()
            return []


# Instancia única (compatible con código anterior)
odontologia_service = OdontologiaServiceV2()
OdontologiaService = OdontologiaServiceV2  # Alias para compatibilidad
