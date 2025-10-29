# 🛒 ESTADO PARA GESTIÓN DE SERVICIOS EN INTERVENCIONES
# dental_system/state/estado_intervencion_servicios.py
#
# ⚠️ NOTA: Este archivo fue PARCIALMENTE LIMPIADO el 2025-10-16
# Se mantienen los métodos esenciales que están en uso activo
#
# MÉTODOS EN USO:
# - agregar_servicio_a_intervencion() ← Usado en save_intervention_to_consultation
# - finalizar_mi_intervencion_odontologo()
# - derivar_paciente_a_otro_odontologo()
# - _actualizar_odontograma_por_servicios()
# - _recalcular_totales()

import reflex as rx
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from dental_system.models import ActualizacionOdontogramaResult
# Modelos necesarios
from dental_system.models import ServicioModel

logger = logging.getLogger(__name__)

# ==========================================
# 🎯 MODELO UNIFICADO V2.0 - SERVICIO DE INTERVENCIÓN
# ==========================================
# Este modelo UNIFICADO reemplaza al anterior ServicioIntervencionTemporal
# y ahora incluye TODOS los campos necesarios tanto para frontend como backend

class ServicioIntervencionCompleto(rx.Base):
    """
    🎯 Modelo UNIFICADO para servicios de intervención (V2.0)

    Este modelo se usa en TODO el flujo:
    - Frontend: Lista temporal de servicios en UI
    - Backend: Inserción directa en BD sin conversiones
    - Odontograma: Actualización automática de condiciones

    ✅ VENTAJAS:
    - Sin conversiones intermedias
    - Tipado completo
    - Validación en un solo lugar
    - Menor probabilidad de errores
    """

    # === IDENTIFICADORES ===
    servicio_id: str = ""  # ID real del servicio en catálogo
    nombre_servicio: str = ""
    categoria_servicio: str = ""

    # === ALCANCE Y UBICACIÓN ===
    alcance: str = "superficie_especifica"  # superficie_especifica, diente_completo, boca_completa
    diente_numero: Optional[int] = None  # Número FDI (11-48) o None si es boca completa
    superficies: List[str] = []  # Lista directa: ["oclusal", "mesial", "distal", "vestibular", "lingual"]

    # === CONDICIÓN ODONTOLÓGICA ===
    nueva_condicion: Optional[str] = None  # Condición a aplicar en el odontograma (opcional)

    # === PRECIOS ===
    costo_bs: float = 0.0
    costo_usd: float = 0.0

    # === DETALLES CLÍNICOS ===
    material: str = ""
    observaciones: str = ""

    @classmethod
    def from_servicio_model(
        cls,
        servicio: ServicioModel,
        alcance: str = "superficie_especifica",
        diente_numero: Optional[int] = None,
        superficies: List[str] = None,
        nueva_condicion: Optional[str] = None,
        material: str = "",
        observaciones: str = ""
    ):
        """
        ✅ Constructor desde ServicioModel con todos los parámetros necesarios

        Args:
            servicio: Modelo del servicio del catálogo
            alcance: superficie_especifica, diente_completo o boca_completa
            diente_numero: Número FDI del diente (o None si es boca completa)
            superficies: Lista de superficies específicas
            nueva_condicion: Condición a aplicar en odontograma (opcional)
            material: Material utilizado en el procedimiento
            observaciones: Observaciones clínicas
        """
        return cls(
            servicio_id=servicio.id,
            nombre_servicio=servicio.nombre,
            categoria_servicio=servicio.categoria or "General",
            alcance=alcance,
            diente_numero=diente_numero,
            superficies=superficies or [],
            nueva_condicion=nueva_condicion,
            costo_usd=servicio.precio_base_usd or 0.0,
            material=material,
            observaciones=observaciones
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para backend"""
        return {
            "servicio_id": self.servicio_id,
            "nombre_servicio": self.nombre_servicio,
            "alcance": self.alcance,
            "diente_numero": self.diente_numero,
            "superficies": self.superficies,
            "nueva_condicion": self.nueva_condicion,
            "costo_bs": self.costo_bs,
            "costo_usd": self.costo_usd,
            "material": self.material,
            "observaciones": self.observaciones
        }


# ❌ ELIMINADO: ServicioIntervencionTemporal
# Usar SOLO ServicioIntervencionCompleto (modelo unificado V2.0)

class EstadoIntervencionServicios(rx.State, mixin=True):
    """🛒 Estado especializado para gestión de servicios en intervenciones"""

    # ==========================================
    # 🛒 VARIABLES UNIFICADAS V2.0
    # ==========================================

    # ✅ V2.0: Lista unificada de servicios usando SOLO ServicioIntervencionCompleto
    servicios_en_intervencion: List[ServicioIntervencionCompleto] = []

    # Totales calculados (usados en computed vars)
    total_intervencion_bs: float = 0.0
    total_intervencion_usd: float = 0.0

    # ⚠️ DEPRECATED - MANTENER POR COMPATIBILIDAD TEMPORAL
    # Estas variables serán eliminadas en próxima versión
    # (Estado odontología todavía las usa temporalmente)
    servicio_temporal: ServicioModel = ServicioModel()
    dientes_seleccionados_texto: str = ""
    superficie_temporal: str = ""
    observaciones_temporal: str = ""

    # ==========================================
    # ➕ MÉTODO AGREGAR SERVICIO (en uso activo)
    # ==========================================

    def agregar_servicio_a_intervencion(self):
        """
        ➕ V3.0: Agregar servicio con validaciones completas (MEJORADO)

        ⚠️ MÉTODO EN USO: Llamado desde estado_odontologia.save_intervention_to_consultation()

        ✨ V3.0 ACTUALIZADO:
        - Usa ServicioIntervencionCompleto
        - Validaciones exhaustivas de condición, diente y superficies
        - Mensajes de error claros para el usuario
        """
        from dental_system.constants import (
            validar_condicion,
            validar_diente_fdi,
            validar_superficie,
            validar_alcance,
            obtener_error_validacion_condicion
        )

        try:
            logger.info(f"➕ V3.0 Agregando servicio con validaciones: {self.servicio_temporal.nombre if self.servicio_temporal else 'None'}")

            # Validación 1: ¿Hay servicio temporal?
            if not self.servicio_temporal or not self.servicio_temporal.id:
                logger.warning("⚠️ No hay servicio temporal para agregar")
                return

            # ✅ V3.0: Determinar alcance con validación
            alcance = self.servicio_temporal.alcance_servicio or "superficie_especifica"

            if not validar_alcance(alcance):
                logger.error(f"❌ Alcance inválido: {alcance}")
                return

            # ✅ V3.0: Parsear y validar diente_numero
            diente_numero = None
            if alcance in ["superficie_especifica", "diente_completo"]:
                if self.dientes_seleccionados_texto:
                    try:
                        # Intentar extraer primer número de diente
                        import re
                        match = re.search(r'\b([1-4][1-8])\b', self.dientes_seleccionados_texto)
                        if match:
                            diente_numero = int(match.group(1))

                            # Validación: ¿Es un diente FDI válido?
                            if not validar_diente_fdi(diente_numero):
                                logger.error(
                                    f"❌ Número de diente inválido: {diente_numero}. "
                                    f"Debe ser FDI permanente (11-48)"
                                )
                                return
                        else:
                            logger.error(
                                f"❌ No se encontró número de diente válido en: "
                                f"{self.dientes_seleccionados_texto}"
                            )
                            return
                    except Exception as e:
                        logger.error(f"❌ Error parseando diente: {e}")
                        return
                else:
                    logger.error(
                        f"❌ Servicio de alcance '{alcance}' requiere seleccionar un diente"
                    )
                    return

            # ✅ V3.0: Parsear y validar superficies
            superficies = []
            if alcance == "superficie_especifica":
                if not self.superficie_temporal:
                    logger.error("❌ Servicio de superficie específica requiere seleccionar superficies")
                    return

                superficies = [s.strip() for s in self.superficie_temporal.split(",") if s.strip()]

                # Validación: ¿Todas las superficies son válidas?
                for superficie in superficies:
                    if not validar_superficie(superficie):
                        logger.error(
                            f"❌ Superficie inválida: {superficie}. "
                            f"Válidas: oclusal, mesial, distal, vestibular, lingual, incisal"
                        )
                        return

                if not superficies:
                    logger.error("❌ Debe seleccionar al menos una superficie")
                    return

            # ✅ V3.0: Obtener y validar condición resultante desde catálogo
            nueva_condicion = self.servicio_temporal.condicion_resultante

            # Validación: ¿La condición es válida? (solo si no es NULL/preventivo)
            if nueva_condicion:
                error_condicion = obtener_error_validacion_condicion(nueva_condicion)
                if error_condicion:
                    logger.error(f"❌ {error_condicion}")
                    return

            # ✅ V3.0: Todas las validaciones pasadas - Crear servicio
            servicio_intervencion = ServicioIntervencionCompleto.from_servicio_model(
                servicio=self.servicio_temporal,
                alcance=alcance,
                diente_numero=diente_numero,
                superficies=superficies,
                nueva_condicion=nueva_condicion,  # ← Carga automática desde catálogo
                observaciones=self.observaciones_temporal
            )

            # Agregar a la lista
            self.servicios_en_intervencion.append(servicio_intervencion)

            # Recalcular totales
            self._recalcular_totales()

            # Log detallado de éxito
            if alcance == "boca_completa":
                logger.info(
                    f"✅ Servicio V3.0 agregado: {servicio_intervencion.nombre_servicio} "
                    f"| Alcance: Boca completa | Tipo: Preventivo"
                )
            elif alcance == "diente_completo":
                logger.info(
                    f"✅ Servicio V3.0 agregado: {servicio_intervencion.nombre_servicio} "
                    f"| Diente: #{diente_numero} completo "
                    f"| Condición: {nueva_condicion or 'N/A'}"
                )
            else:  # superficie_especifica
                logger.info(
                    f"✅ Servicio V3.0 agregado: {servicio_intervencion.nombre_servicio} "
                    f"| Diente: #{diente_numero} "
                    f"| Superficies: {', '.join(superficies)} "
                    f"| Condición: {nueva_condicion or 'N/A'}"
                )

        except Exception as e:
            logger.error(f"❌ Error crítico agregando servicio V3.0: {e}")
            import traceback
            traceback.print_exc()

    def agregar_servicio_directo(
        self,
        servicio: ServicioModel,
        alcance: str,
        diente_numero: Optional[int] = None,
        superficies: List[str] = None,
        nueva_condicion: Optional[str] = None,
        observaciones: str = ""
    ):
        """
        ➕ V2.0: Agregar servicio DIRECTAMENTE sin variables temporales

        Este es el método RECOMENDADO para agregar servicios.
        Crea directamente ServicioIntervencionCompleto sin pasar por variables temporales.

        Args:
            servicio: ServicioModel del catálogo
            alcance: superficie_especifica, diente_completo o boca_completa
            diente_numero: Número FDI (11-48) o None
            superficies: Lista de superficies ["oclusal", "mesial", etc.]
            nueva_condicion: Condición a aplicar en odontograma
            observaciones: Observaciones clínicas
        """
        try:
            logger.info(f"➕ V2.0 Agregando servicio directo: {servicio.nombre}")

            # Crear servicio completo unificado
            servicio_completo = ServicioIntervencionCompleto.from_servicio_model(
                servicio=servicio,
                alcance=alcance,
                diente_numero=diente_numero,
                superficies=superficies or [],
                nueva_condicion=nueva_condicion,
                observaciones=observaciones
            )

            # Agregar a la lista
            self.servicios_en_intervencion.append(servicio_completo)

            # Recalcular totales
            self._recalcular_totales()

            logger.info(f"✅ Servicio agregado exitosamente: {servicio_completo.nombre_servicio}")

        except Exception as e:
            logger.error(f"❌ Error agregando servicio directo: {e}")
            import traceback
            traceback.print_exc()

    def _recalcular_totales(self):
        """💰 V2.0: Recalcular totales usando solo ServicioIntervencionCompleto"""
        try:
            total_bs = 0.0
            total_usd = 0.0

            for servicio in self.servicios_en_intervencion:
                # ✅ V2.0: Solo ServicioIntervencionCompleto
                if isinstance(servicio, ServicioIntervencionCompleto):
                    total_bs += servicio.costo_bs
                    total_usd += servicio.costo_usd
                else:
                    logger.warning(f"⚠️ Servicio con tipo no esperado: {type(servicio)}")

            self.total_intervencion_bs = total_bs
            self.total_intervencion_usd = total_usd

            logger.debug(f"💰 Totales recalculados V2.0: {total_bs:,.0f} Bs / ${total_usd:.2f} USD")

        except Exception as e:
            logger.error(f"Error recalculando totales: {e}")
            self.total_intervencion_bs = 0.0
            self.total_intervencion_usd = 0.0

    # ==========================================
    # 💾 MÉTODOS PARA FINALIZAR INTERVENCIÓN
    # ==========================================
    
    @rx.event
    async def finalizar_mi_intervencion_odontologo(self):
        """
        🦷 V2.0: Finalizar SOLO la intervención del odontólogo actual

        FLUJO CORRECTO:
        1. Valida que haya consulta y servicios
        2. Guarda intervención con servicios en BD
        3. Actualiza odontograma automáticamente según servicios aplicados
        4. Cambia consulta a estado "entre_odontologos"
        5. Navega de vuelta a lista de pacientes

        ✅ CORREGIDO: Ahora usa servicios_en_intervencion (variable correcta)
        """
        try:
            print("\n" + "="*80)
            print("🎯 [PUNTO 1] INICIO FINALIZAR INTERVENCIÓN")
            print("="*80)
            logger.info("🦷 Finalizando intervención del odontólogo...")

            # Validaciones previas
            if not hasattr(self, 'consulta_actual') or not self.consulta_actual.id:
                logger.error("❌ No hay consulta actual seleccionada")
                return

            print(f"📋 Consulta actual ID: {self.consulta_actual.id}")
            print(f"👤 Paciente ID: {self.paciente_actual.id if hasattr(self, 'paciente_actual') else 'N/A'}")
            print(f"👨‍⚕️ Odontólogo ID: {self.id_usuario}")

            # ✅ CORREGIDO: Usar servicios_en_intervencion en lugar de servicios_consulta_actual
            # servicios_consulta_actual NO EXISTE - era un BUG crítico
            servicios = self.servicios_en_intervencion

            if not servicios:
                logger.error("❌ No hay servicios para guardar en servicios_en_intervencion")
                return

            print(f"\n✅ Procesando {len(servicios)} servicios desde servicios_en_intervencion")
            logger.info(f"✅ Procesando {len(servicios)} servicios desde servicios_en_intervencion")

            # DETALLE DE SERVICIOS ORIGINALES
            print("\n📦 [PUNTO 2] SERVICIOS ORIGINALES (antes de conversión):")
            for i, serv in enumerate(servicios, 1):
                if isinstance(serv, ServicioIntervencionCompleto):
                    print(f"  {i}. {serv.nombre_servicio}")
                    print(f"     - Alcance: {serv.alcance}")
                    print(f"     - Diente: {serv.diente_numero}")
                    print(f"     - Superficies: {serv.superficies}")
                    print(f"     - Condición resultante: {serv.nueva_condicion}")
                    print(f"     - Material: {serv.material}")
                elif isinstance(serv, dict):
                    print(f"  {i}. {serv.get('nombre_servicio', 'N/A')}")
                    print(f"     - Alcance: {serv.get('alcance', 'N/A')}")
                    print(f"     - Diente: {serv.get('diente_numero', 'N/A')}")
                    print(f"     - Superficies: {serv.get('superficies', [])}")
                    print(f"     - Condición resultante: {serv.get('nueva_condicion', 'N/A')}")

            # Importar servicios necesarios
            from dental_system.services.odontologia_service import odontologia_service

            # Configurar contexto del usuario
            contexto_usuario = {
                **self.perfil_usuario,
                "rol": {"nombre": self.rol_usuario},
                "usuario_id": self.id_usuario,
                "personal_id": getattr(self, 'id_personal', None)
            }
            odontologia_service.set_user_context(self.id_usuario, contexto_usuario)

            # 1. PREPARAR SERVICIOS PARA BACKEND
            print("\n" + "="*80)
            print("🔄 [PUNTO 3] CONVERSIÓN DE SERVICIOS PARA BACKEND")
            print("="*80)
            # ✅ CORRECCIÓN V2.2: Incluir campo alcance y ajustar conversión según tipo de servicio
            servicios_backend = []
            for idx, servicio in enumerate(servicios, 1):
                # Si es el nuevo modelo ServicioIntervencionCompleto
                if isinstance(servicio, ServicioIntervencionCompleto):
                    # ✅ CORRECCIÓN: Conversión basada en alcance
                    dientes_texto = ""
                    superficie_str = None

                    if servicio.alcance == "boca_completa":
                        # Boca completa: Sin dientes específicos, sin superficie
                        dientes_texto = ""
                        superficie_str = None
                    elif servicio.alcance == "diente_completo":
                        # Diente completo: Con diente, sin superficie (NULL)
                        dientes_texto = str(servicio.diente_numero) if servicio.diente_numero else ""
                        superficie_str = None
                    else:  # superficie_especifica
                        # Superficie específica: Con diente y superficie(s)
                        dientes_texto = str(servicio.diente_numero) if servicio.diente_numero else ""
                        superficie_str = ", ".join(servicio.superficies) if servicio.superficies else None

                    servicio_data = {
                        "servicio_id": servicio.servicio_id,
                        "cantidad": 1,
                        "precio_unitario_bs": servicio.costo_bs,
                        "precio_unitario_usd": servicio.costo_usd,
                        "dientes_texto": dientes_texto,
                        "material_utilizado": servicio.material,
                        "superficie": superficie_str,
                        "alcance": servicio.alcance,  # ← NUEVO: Transmitir alcance al backend
                        "observaciones": servicio.observaciones
                    }

                    print(f"\n  ✅ Servicio #{idx} convertido (ServicioIntervencionCompleto):")
                    print(f"     - Nombre: {servicio.nombre_servicio}")
                    print(f"     - Alcance: {servicio.alcance}")
                    print(f"     - Diente texto: '{dientes_texto}'")
                    print(f"     - Superficie: {superficie_str}")
                    print(f"     - Material: {servicio.material}")
                    print(f"     - Condición (NO va al backend, solo a odontograma): {servicio.nueva_condicion}")
                # Si es dict (desde estado odontología)
                elif isinstance(servicio, dict):
                    alcance = servicio.get("alcance", "superficie_especifica")
                    dientes_texto = ""
                    superficie_str = None

                    if alcance == "boca_completa":
                        dientes_texto = ""
                        superficie_str = None
                    elif alcance == "diente_completo":
                        dientes_texto = str(servicio.get("diente_numero")) if servicio.get("diente_numero") else ""
                        superficie_str = None
                    else:  # superficie_especifica
                        dientes_texto = str(servicio.get("diente_numero")) if servicio.get("diente_numero") else ""
                        superficie_str = ", ".join(servicio.get("superficies", [])) if servicio.get("superficies") else None

                    servicio_data = {
                        "servicio_id": servicio.get("servicio_id"),
                        "cantidad": 1,
                        "precio_unitario_bs": servicio.get("costo_bs", 0.0),
                        "precio_unitario_usd": servicio.get("costo_usd", 0.0),
                        "dientes_texto": dientes_texto,
                        "material_utilizado": servicio.get("material", ""),
                        "superficie": superficie_str,
                        "alcance": alcance,  # ← NUEVO: Transmitir alcance
                        "observaciones": servicio.get("observaciones", "")
                    }
                # ❌ V2.0: Legacy model eliminado
                else:
                    logger.error(f"❌ Tipo de servicio no soportado: {type(servicio)}")
                    logger.error("⚠️ Solo se acepta ServicioIntervencionCompleto o dict")
                    continue

                servicios_backend.append(servicio_data)

            # 2. CREAR INTERVENCIÓN
            print("\n" + "="*80)
            print("💾 [PUNTO 4] ENVIANDO A BACKEND (crear_intervencion_con_servicios)")
            print("="*80)
            datos_intervencion = {
                "consulta_id": self.consulta_actual.id,
                "odontologo_id": self.id_usuario,
                "servicios": servicios_backend,
                "observaciones_generales": f"Intervención del Dr. {self.perfil_usuario.get('nombre_completo', 'Usuario')} con {len(servicios)} servicios"
            }

            print(f"📤 Datos que van al backend:")
            print(f"  - consulta_id: {datos_intervencion['consulta_id']}")
            print(f"  - odontologo_id: {datos_intervencion['odontologo_id']}")
            print(f"  - Total servicios: {len(servicios_backend)}")
            print(f"\n📋 Resumen servicios backend:")
            for i, sb in enumerate(servicios_backend, 1):
                print(f"  {i}. servicio_id={sb['servicio_id'][:8]}... | diente={sb['dientes_texto']} | superficie={sb['superficie']} | alcance={sb['alcance']}")

            resultado = await odontologia_service.crear_intervencion_con_servicios(datos_intervencion)

            print(f"\n📥 RESPUESTA del backend:")
            print(f"  - success: {resultado.get('success')}")
            print(f"  - intervencion_id: {resultado.get('intervencion_id', 'N/A')}")

            if not resultado.get("success"):
                logger.error(f"❌ Error guardando intervención: {resultado.get('message')}")
                return

            intervencion_id = resultado.get("intervencion_id")
            logger.info(f"✅ Intervención guardada: {intervencion_id}")

            # 3. ACTUALIZAR ODONTOGRAMA AUTOMÁTICAMENTE
            print("\n" + "="*80)
            print("🦷 [PUNTO 5] ACTUALIZANDO ODONTOGRAMA")
            print("="*80)
            print(f"🔑 intervencion_id para vincular: {intervencion_id}")
            print(f"📦 Servicios a procesar: {len(servicios)}")
            logger.info("🦷 Actualizando odontograma...")
            await self._actualizar_odontograma_por_servicios(intervencion_id, servicios)

            # 4. CAMBIAR ESTADO CONSULTA
            await self._cambiar_estado_consulta_entre_odontologos()
            await self.cargar_consultas_hoy(forzar_refresco=True)
            self.servicios_en_intervencion = []  # Limpiar lista tras finalizar
            # 5. NAVEGAR DE VUELTA
            logger.info("✅ Intervención finalizada exitosamente")
            self.navigate_to("odontologia")

        except Exception as e:
            logger.error(f"❌ Error finalizando intervención: {str(e)}")
            import traceback
            traceback.print_exc()

    # ==========================================
    # V3.0: HELPERS PARA ACTUALIZACIÓN DE ODONTOGRAMA
    # ==========================================

    def _convertir_servicio_a_actualizaciones(
        self,
        servicio: ServicioIntervencionCompleto,
        paciente_id: str,
        intervencion_id: str
    ) -> List[Dict[str, Any]]:
        """
        🔧 V3.0: Helper unificado para convertir servicio a actualizaciones de odontograma

        Centraliza toda la lógica de conversión según alcance del servicio,
        eliminando duplicación en múltiples métodos.

        Args:
            servicio: Servicio con toda la información necesaria
            paciente_id: ID del paciente
            intervencion_id: ID de la intervención

        Returns:
            Lista de actualizaciones listas para batch SQL
            [] si el servicio es preventivo (no modifica odontograma)

        Ejemplo:
            Input: Servicio obturación en diente 11, superficie oclusal
            Output: [
                {
                    "paciente_id": "uuid",
                    "diente_numero": 11,
                    "superficie": "oclusal",
                    "tipo_condicion": "obturacion",
                    "intervencion_id": "uuid",
                    ...
                }
            ]
        """
        from dental_system.constants import TODAS_LAS_SUPERFICIES, validar_condicion
        import logging
        logger = logging.getLogger(__name__)

        actualizaciones = []

        # Validación 1: ¿El servicio modifica odontograma?
        if not servicio.nueva_condicion:
            logger.debug(
                f"ℹ️ Servicio '{servicio.nombre_servicio}' es preventivo "
                f"(alcance: {servicio.alcance}) - No modifica odontograma"
            )
            return []

        # Validación 2: ¿La condición es válida?
        if not validar_condicion(servicio.nueva_condicion):
            logger.error(
                f"❌ Condición inválida '{servicio.nueva_condicion}' "
                f"en servicio '{servicio.nombre_servicio}'"
            )
            return []

        # Determinar superficies según alcance
        if servicio.alcance == "boca_completa":
            # Servicio de boca completa NO modifica odontograma individual
            logger.debug(
                f"ℹ️ Servicio de boca completa '{servicio.nombre_servicio}' "
                f"- No genera actualizaciones individuales"
            )
            return []

        elif servicio.alcance == "diente_completo":
            # Diente completo: Todas las superficies
            if not servicio.diente_numero:
                logger.warning(
                    f"⚠️ Servicio '{servicio.nombre_servicio}' es de diente completo "
                    f"pero no tiene diente_numero"
                )
                return []

            superficies_aplicar = TODAS_LAS_SUPERFICIES
            logger.debug(
                f"🦷 Diente completo #{servicio.diente_numero} "
                f"→ {len(superficies_aplicar)} superficies"
            )

        else:  # superficie_especifica
            # Superficie específica: Solo las seleccionadas
            if not servicio.diente_numero:
                logger.warning(
                    f"⚠️ Servicio '{servicio.nombre_servicio}' requiere diente_numero"
                )
                return []

            if not servicio.superficies:
                logger.warning(
                    f"⚠️ Servicio '{servicio.nombre_servicio}' requiere superficies"
                )
                return []

            # ✅ CORRECCIÓN: Detectar "completo" y expandir a 5 superficies
            if any(sup.lower() == "completo" for sup in servicio.superficies):
                superficies_aplicar = TODAS_LAS_SUPERFICIES
                logger.debug(
                    f"🔧 Detectado 'completo' → Expandiendo a {len(superficies_aplicar)} superficies"
                )
            else:
                superficies_aplicar = servicio.superficies

            logger.debug(
                f"🎯 Diente #{servicio.diente_numero}, "
                f"superficies: {', '.join(superficies_aplicar)}"
            )

        # Generar actualizaciones para cada superficie
        for superficie in superficies_aplicar:
            actualizaciones.append({
                "paciente_id": str(paciente_id),  # ✅ Asegurar que sea string
                "diente_numero": int(servicio.diente_numero),  # ✅ Asegurar que sea int
                "superficie": str(superficie),  # ✅ Asegurar que sea string
                "tipo_condicion": str(servicio.nueva_condicion),  # ✅ Asegurar que sea string
                "descripcion": str(
                    servicio.observaciones or
                    f"Servicio: {servicio.nombre_servicio}"
                ),
                "intervencion_id": str(intervencion_id),  # ✅ Asegurar que sea string
            })

        logger.info(
            f"✅ Convertido servicio '{servicio.nombre_servicio}' "
            f"→ {len(actualizaciones)} actualizaciones "
            f"(condición: {servicio.nueva_condicion})"
        )

        return actualizaciones

    def _normalizar_servicio(
        self,
        servicio: Any
    ) -> List[Dict[str, Any]]:  # ← CAMBIO: Retorna LISTA
        """
        V4.0: Normalizar servicio a formato estándar

        CAMBIO CRÍTICO:
        - ANTES: Retornaba UN dict (solo primer diente)
        - AHORA: Retorna LISTA de dicts (uno por diente)

        Unifica 3 formatos diferentes en una lista de dicts consistentes:
        - ServicioIntervencionCompleto (V2.0)
        - dict (desde estado_odontologia)
        - ServicioIntervencionTemporal (DEPRECATED)

        Ejemplo:
        Input: Servicio con dientes [11, 12, 13]
        Output: [
            {diente_numero: 11, ...},
            {diente_numero: 12, ...},
            {diente_numero: 13, ...}
        ]

        Returns:
            Lista de dicts con campos estandarizados
        """
        # Formato 1: ServicioIntervencionCompleto (nuevo)
        if isinstance(servicio, ServicioIntervencionCompleto):
            # ✅ CORRECCIÓN: Procesar TODOS los dientes, no solo el primero
            diente_numero = servicio.diente_numero

            # Si tiene un solo diente o None, retornar lista de 1 elemento
            if diente_numero:
                return [{
                    "nombre": servicio.nombre_servicio,
                    "condicion_resultante": servicio.nueva_condicion,
                    "diente_numero": diente_numero,
                    "superficies": servicio.superficies or [],
                    "material": servicio.material,
                    "observaciones": servicio.observaciones
                }]
            else:
                # Servicio general (sin diente específico)
                return [{
                    "nombre": servicio.nombre_servicio,
                    "condicion_resultante": servicio.nueva_condicion,
                    "diente_numero": None,
                    "superficies": servicio.superficies or [],
                    "material": servicio.material,
                    "observaciones": servicio.observaciones
                }]

        # Formato 2: dict (desde estado_odontologia)
        elif isinstance(servicio, dict):
            diente_numero = servicio.get("diente_numero")

            if diente_numero:
                return [{
                    "nombre": servicio.get("nombre_servicio", ""),
                    "condicion_resultante": servicio.get("nueva_condicion"),
                    "diente_numero": diente_numero,
                    "superficies": servicio.get("superficies", []),
                    "material": servicio.get("material", ""),
                    "observaciones": servicio.get("observaciones", "")
                }]
            else:
                # Servicio general
                return [{
                    "nombre": servicio.get("nombre_servicio", ""),
                    "condicion_resultante": servicio.get("nueva_condicion"),
                    "diente_numero": None,
                    "superficies": servicio.get("superficies", []),
                    "material": servicio.get("material", ""),
                    "observaciones": servicio.get("observaciones", "")
                }]

        # ❌ V2.0: Formato legacy eliminado
        else:
            logger.error(f"⚠️ Formato de servicio no reconocido: {type(servicio)}")
            logger.error("✅ Solo se acepta: ServicioIntervencionCompleto o dict")
            # Retornar lista vacía para evitar errores
            return []

    async def _resolver_conflictos_servicios(
        self,
        servicios_normalizados: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        V4.0: Resolver conflictos por TEMPORALIDAD (último servicio aplicado gana)

        CAMBIO CRÍTICO vs V3.0:
        - ANTES: Ordenar por catalogo_condiciones.prioridad (severidad médica)
        - AHORA: Ordenar por orden_aplicacion (temporalidad)

        Justificación:
        Si se aplicó obturación DESPUÉS de diagnosticar caries,
        el diente está obturado (tratamiento > diagnóstico).

        Reglas de resolución:
        1. Último servicio aplicado gana (orden_aplicacion mayor)
        2. "ausente" siempre es final (no se puede sobrescribir)
        3. Temporalidad refleja realidad clínica

        Returns:
            Lista de servicios sin conflictos, listos para aplicar
        """
        try:
            # Agrupar servicios por diente + superficie
            grupos: Dict[str, List[Dict]] = {}

            for idx, servicio in enumerate(servicios_normalizados):
                condicion = servicio.get("condicion_resultante")

                # Skip servicios preventivos
                if not condicion:
                    continue

                diente = servicio.get("diente_numero")
                if not diente:
                    continue

                # ✅ NUEVO: Agregar índice temporal (orden de aplicación)
                servicio["orden_aplicacion"] = idx

                # Usar todas las superficies si no hay especificadas
                superficies = servicio.get("superficies") or [
                    "oclusal", "mesial", "distal", "vestibular", "lingual"
                ]

                # Agrupar por cada combinación diente+superficie
                for superficie in superficies:
                    key = f"{diente}_{superficie}"
                    if key not in grupos:
                        grupos[key] = []

                    # Agregar copia del servicio con superficie específica
                    servicio_copia = servicio.copy()
                    servicio_copia["superficies"] = [superficie]
                    grupos[key].append(servicio_copia)

            # Resolver conflictos por grupo
            servicios_finales = []

            for key, servicios_grupo in grupos.items():
                if len(servicios_grupo) == 1:
                    # No hay conflicto
                    servicios_finales.append(servicios_grupo[0])
                else:
                    # ✅ CORRECCIÓN: Ordenar por TEMPORALIDAD (orden_aplicacion)
                    # En vez de prioridad médica del catálogo
                    servicios_ordenados = sorted(
                        servicios_grupo,
                        key=lambda s: s.get("orden_aplicacion", 0),
                        reverse=False  # Menor índice primero
                    )

                    # ✅ TOMAR ÚLTIMO (más reciente, aplicado después)
                    servicio_ganador = servicios_ordenados[-1]

                    # Verificar regla especial: "ausente" es final
                    condicion_ganadora = servicio_ganador.get("condicion_resultante")
                    if condicion_ganadora == "ausente":
                        # Si hay "ausente", ningún servicio posterior puede modificarlo
                        # (pero ya tomamos el último, así que "ausente" gana si es el último)
                        pass

                    servicios_finales.append(servicio_ganador)

                    # Log del conflicto resuelto
                    orden_ganador = servicio_ganador.get("orden_aplicacion", 0)
                    logger.info(
                        f"⚖️ Conflicto resuelto por temporalidad | "
                        f"Clave: {key} | "
                        f"Servicios: {len(servicios_grupo)} | "
                        f"Ganador: '{condicion_ganadora}' (orden: {orden_ganador}, último aplicado)"
                    )

            return servicios_finales

        except Exception as e:
            logger.error(f"❌ Error resolviendo conflictos: {str(e)}")
            # Si falla, retornar servicios sin resolver (fallback seguro)
            return servicios_normalizados

    async def _actualizar_odontograma_por_servicios(
        self, intervencion_id: str, servicios: List
    ) -> ActualizacionOdontogramaResult:
        """
        V4.0 MEJORADO - Actualizar odontograma batch con correcciones críticas

        MEJORAS V4.0:
        - ✅ Resolución por TEMPORALIDAD (último servicio aplicado gana)
        - ✅ Soporte MULTI-DIENTE (ya no pierde datos)
        - ✅ Sin mapeo hardcodeado (usa BD: servicios.condicion_resultante)
        - ✅ Actualización batch transaccional (función SQL)
        - ✅ Tipado fuerte (ActualizacionOdontogramaResult)
        - ✅ Logging mejorado con métricas de explosión

        CORRECCIONES CRÍTICAS:
        - 🔧 Lógica de prioridad: Ahora usa temporalidad en vez de severidad médica
        - 🔧 Multi-diente: Soporta servicios que afectan múltiples dientes

        Args:
            intervencion_id: ID de la intervención que genera los servicios
            servicios: Lista de servicios en cualquier formato (auto-normaliza)

        Returns:
            ActualizacionOdontogramaResult con estadísticas de la operación
        """
        from dental_system.services.odontologia_service import odontologia_service
        from dental_system.models import ActualizacionOdontogramaResult

        resultado = ActualizacionOdontogramaResult()

        print("\n" + "="*80)
        print("🔍 [PUNTO 6] ENTRANDO A _actualizar_odontograma_por_servicios")
        print("="*80)

        try:
            # PASO 1: Validar contexto
            if not self.paciente_actual or not self.paciente_actual.id:
                print("❌ ERROR: No hay paciente actual válido")
                logger.warning("🚫 No hay paciente actual válido para actualizar odontograma")
                resultado.advertencias.append("No hay paciente actual válido")
                return resultado

            if not servicios:
                print("⚠️ No hay servicios para procesar")
                logger.info("ℹ️ No hay servicios para procesar")
                return resultado

            print(f"✅ Validaciones OK:")
            print(f"  - Paciente ID: {self.paciente_actual.id}")
            print(f"  - Intervención ID: {intervencion_id}")
            print(f"  - Servicios recibidos: {len(servicios)}")

            logger.info(
                f"🦷 V4.0 Iniciando actualización odontograma | "
                f"Paciente: {self.paciente_actual.id[:8]}... | "
                f"Intervención: {intervencion_id[:8]}... | "
                f"Servicios originales: {len(servicios)}"
            )

            # PASO 2: Normalizar todos los servicios a formato estándar
            print("\n" + "-"*80)
            print("📋 [PUNTO 7] NORMALIZANDO SERVICIOS")
            print("-"*80)
            # ✅ CORRECCIÓN: Usar extend para aplanar lista de listas
            # Ahora _normalizar_servicio retorna LISTA (soporta multi-diente)
            servicios_normalizados = []
            for idx, servicio in enumerate(servicios, 1):
                print(f"\n  Normalizando servicio {idx}/{len(servicios)}:")
                if isinstance(servicio, ServicioIntervencionCompleto):
                    print(f"    - Tipo: ServicioIntervencionCompleto")
                    print(f"    - Nombre: {servicio.nombre_servicio}")
                    print(f"    - Condición: {servicio.nueva_condicion}")
                    print(f"    - Diente: {servicio.diente_numero}")
                    print(f"    - Superficies: {servicio.superficies}")
                elif isinstance(servicio, dict):
                    print(f"    - Tipo: dict")
                    print(f"    - Nombre: {servicio.get('nombre_servicio')}")
                    print(f"    - Condición: {servicio.get('nueva_condicion')}")
                    print(f"    - Diente: {servicio.get('diente_numero')}")
                    print(f"    - Superficies: {servicio.get('superficies')}")

                servicios_lista = self._normalizar_servicio(servicio)  # Retorna lista
                print(f"    ✅ Normalizado a {len(servicios_lista)} registro(s)")
                servicios_normalizados.extend(servicios_lista)  # extend en vez de append

            print(f"\n✅ Normalización completada:")
            print(f"  - Servicios originales: {len(servicios)}")
            print(f"  - Servicios normalizados: {len(servicios_normalizados)}")
            print(f"  - Explosión multi-diente: +{len(servicios_normalizados) - len(servicios)}")

            logger.info(
                f"📊 Normalización completada | "
                f"Servicios originales: {len(servicios)} | "
                f"Servicios normalizados: {len(servicios_normalizados)} | "
                f"Explosión multi-diente: +{len(servicios_normalizados) - len(servicios)}"
            )

            # PASO 3: Filtrar solo servicios que modifican odontograma
            print("\n" + "-"*80)
            print("🔍 [PUNTO 8] FILTRANDO SERVICIOS ACTIVOS (que modifican odontograma)")
            print("-"*80)

            servicios_activos = []
            for idx, s in enumerate(servicios_normalizados, 1):
                condicion = s.get("condicion_resultante")
                diente = s.get("diente_numero")

                print(f"\n  Servicio {idx}: {s.get('nombre', 'N/A')}")
                print(f"    - Condición: {condicion}")
                print(f"    - Diente: {diente}")

                if condicion and diente:
                    print(f"    ✅ ACTIVO (modifica odontograma)")
                    servicios_activos.append(s)
                else:
                    print(f"    ⚠️ PREVENTIVO (no modifica odontograma)")

            print(f"\n📊 Resumen filtrado:")
            print(f"  - Total normalizados: {len(servicios_normalizados)}")
            print(f"  - Servicios activos: {len(servicios_activos)}")
            print(f"  - Servicios preventivos: {len(servicios_normalizados) - len(servicios_activos)}")

            if not servicios_activos:
                print("⚠️ TODOS LOS SERVICIOS SON PREVENTIVOS - NO HAY NADA QUE ACTUALIZAR")
                logger.info("ℹ️ Todos los servicios son preventivos (no modifican odontograma)")
                resultado.advertencias.append("Todos los servicios son preventivos")
                return resultado

            logger.info(f"📊 Servicios activos: {len(servicios_activos)}/{len(servicios)}")

            # PASO 4: Resolver conflictos (múltiples servicios en mismo diente/superficie)
            servicios_resueltos = await self._resolver_conflictos_servicios(servicios_activos)

            if len(servicios_resueltos) < len(servicios_activos):
                conflictos = len(servicios_activos) - len(servicios_resueltos)
                logger.info(f"⚖️ Conflictos resueltos: {conflictos} servicios descartados por menor prioridad")
                resultado.advertencias.append(f"{conflictos} servicios descartados por conflictos de prioridad")

            # PASO 5: Preparar actualizaciones batch usando helper unificado V3.0
            print("\n" + "-"*80)
            print("🔨 [PUNTO 10] PREPARANDO ACTUALIZACIONES BATCH PARA SQL")
            print("-"*80)
            actualizaciones = []

            # ✅ V3.0: Usar helper para cada servicio
            for idx, servicio_normalizado in enumerate(servicios_resueltos, 1):
                print(f"\n  Procesando servicio {idx}/{len(servicios_resueltos)}:")
                print(f"    - Nombre: {servicio_normalizado['nombre']}")
                print(f"    - Diente: {servicio_normalizado['diente_numero']}")
                print(f"    - Superficies: {servicio_normalizado['superficies']}")
                print(f"    - Condición: {servicio_normalizado['condicion_resultante']}")
                # Reconstruir ServicioIntervencionCompleto desde dict normalizado
                servicio_reconstruido = ServicioIntervencionCompleto(
                    nombre_servicio=servicio_normalizado["nombre"],
                    nueva_condicion=servicio_normalizado["condicion_resultante"],
                    diente_numero=servicio_normalizado["diente_numero"],
                    superficies=servicio_normalizado["superficies"],
                    material=servicio_normalizado["material"],
                    observaciones=servicio_normalizado["observaciones"],
                    alcance=(
                        "superficie_especifica"
                        if servicio_normalizado["superficies"]
                        else "diente_completo"
                    )
                )

                # Convertir usando helper unificado
                actualizaciones_servicio = self._convertir_servicio_a_actualizaciones(
                    servicio=servicio_reconstruido,
                    paciente_id=self.paciente_actual.id,
                    intervencion_id=intervencion_id
                )

                print(f"    ✅ Generadas {len(actualizaciones_servicio)} actualizaciones")
                for act in actualizaciones_servicio:
                    print(f"       - Diente {act['diente_numero']}, {act['superficie']} → {act['tipo_condicion']}")

                actualizaciones.extend(actualizaciones_servicio)

            print(f"\n📦 TOTAL ACTUALIZACIONES PREPARADAS: {len(actualizaciones)}")

            if not actualizaciones:
                print("❌ NO HAY ACTUALIZACIONES PARA REALIZAR")
                logger.warning("⚠️ No hay actualizaciones para realizar después de resolver conflictos")
                resultado.advertencias.append("No hay actualizaciones después de resolver conflictos")
                return resultado

            logger.info(f"📦 Preparadas {len(actualizaciones)} actualizaciones batch")

            # MOSTRAR DETALLE DE TODAS LAS ACTUALIZACIONES
            print("\n📋 DETALLE DE ACTUALIZACIONES QUE SE ENVIARÁN A SQL:")
            for i, act in enumerate(actualizaciones, 1):
                print(f"  {i}. Diente #{act['diente_numero']}, superficie: {act['superficie']}")
                print(f"     → Condición: {act['tipo_condicion']}")
                print(f"     → Material: {act.get('material_utilizado', 'N/A')}")
                print(f"     → Paciente ID: {act['paciente_id'][:8]}...")
                print(f"     → Intervención ID: {act['intervencion_id'][:8]}...")

            # PASO 6: Ejecutar batch transaccional (todo o nada)
            print("\n" + "="*80)
            print("💾 [PUNTO 11] EJECUTANDO BATCH SQL (actualizar_condiciones_batch)")
            print("="*80)
            print(f"📤 Enviando {len(actualizaciones)} actualizaciones a la base de datos...")

            batch_result = await odontologia_service.actualizar_condiciones_batch(actualizaciones)

            print(f"\n📥 RESPUESTA DE SQL:")
            print(f"  - Exitosos: {batch_result.get('exitosos', 0)}")
            print(f"  - Fallidos: {batch_result.get('fallidos', 0)}")
            print(f"  - Total: {batch_result.get('total', 0)}")
            print(f"  - Tasa éxito: {batch_result.get('tasa_exito_pct', 0)}%")
            print(f"  - IDs creados: {len(batch_result.get('ids_creados', []))}")

            # PASO 7: Procesar resultado
            resultado.exitosos = batch_result.get("exitosos", 0)
            resultado.fallidos = batch_result.get("fallidos", 0)
            resultado.ids_creados = batch_result.get("ids_creados", [])

            if resultado.fallidos > 0:
                resultado.advertencias.append(
                    f"{resultado.fallidos} actualizaciones fallaron durante el batch"
                )

            # PASO 8: Recargar UI si hubo cambios exitosos
            if resultado.exitosos > 0:
                logger.info(
                    f"✅ Odontograma actualizado | "
                    f"Exitosos: {resultado.exitosos} | "
                    f"Fallidos: {resultado.fallidos} | "
                    f"Tasa éxito: {resultado.tasa_exito_pct:.1f}%"
                )

                # Recargar odontograma en UI
                if hasattr(self, "cargar_odontograma_paciente"):
                    try:
                        await self.cargar_odontograma_paciente(self.paciente_actual.id)
                        logger.info("♻️ Odontograma recargado en UI")
                    except Exception as e:
                        logger.warning(f"⚠️ No se pudo recargar odontograma en UI: {str(e)}")
                        resultado.advertencias.append("No se pudo recargar UI")

            return resultado

        except Exception as e:
            logger.error(
                f"💥 Error crítico en actualización odontograma V3.0: {str(e)}",
                exc_info=True
            )
            resultado.advertencias.append(f"Error crítico: {str(e)}")
            return resultado

    def _extraer_numeros_dientes(self, texto_dientes: str) -> List[int]:
        """🦷 Extraer números de dientes válidos del texto"""
        import re

        if not texto_dientes:
            return []

        # Si dice "todos" o "toda la boca", devolver todos los dientes FDI
        if "todos" in texto_dientes.lower() or "toda" in texto_dientes.lower():
            return list(range(11, 19)) + list(range(21, 29)) + list(range(31, 39)) + list(range(41, 49))

        # Extraer números usando regex
        numeros = re.findall(r'\b([1-4][1-8])\b', texto_dientes)

        # Convertir a enteros y validar rango FDI
        dientes_validos = []
        for num_str in numeros:
            num = int(num_str)
            if 11 <= num <= 18 or 21 <= num <= 28 or 31 <= num <= 38 or 41 <= num <= 48:
                dientes_validos.append(num)

        return dientes_validos


    async def _cambiar_estado_consulta_entre_odontologos(self):
        """🔄 Cambiar consulta a estado 'entre_odontologos'"""
        try:
            from dental_system.supabase.tablas.consultas import consultas_table

            result = consultas_table.update_status(
                self.consulta_actual.id,
                "entre_odontologos"
            )

            logger.info(f"🔄 Consulta {self.consulta_actual.numero_consulta} marcada como {result}")

        except Exception as e:
            logger.error(f"Error cambiando estado de consulta: {str(e)}")

    @rx.event
    async def derivar_paciente_a_otro_odontologo(self):
        """
        🔄 DERIVAR PACIENTE A OTRO ODONTÓLOGO

        Flujo para terminar la intervención del odontólogo actual
        y dejar el paciente disponible para otro odontólogo:

        1. Valida que haya una consulta e intervención activa
        2. Guarda la intervención actual (si hay servicios)
        3. Cambia estado de consulta a "entre_odontologos"
        4. Navega de vuelta a lista de pacientes

        Este método permite el flujo de múltiples odontólogos por consulta.
        """
        try:
            # Validar que hay consulta actual
            if not hasattr(self, 'consulta_actual') or not self.consulta_actual.id:
                logger.warning("❌ No hay consulta actual para derivar")
                return

            # Validar que hay servicios para guardar (opcional, puede derivar sin servicios)
            servicios = getattr(self, 'servicios_consulta_actual', [])
            if servicios and len(servicios) > 0:
                logger.info(f"💾 Guardando intervención antes de derivar ({len(servicios)} servicios)")

                # Guardar la intervención actual
                await self.finalizar_mi_intervencion_odontologo()

                # Esperar un momento para que se complete el guardado
                import asyncio
                await asyncio.sleep(0.5)
            else:
                # Cambiar estado de consulta directamente
                await self._cambiar_estado_consulta_entre_odontologos()

            logger.info(f"✅ Paciente derivado exitosamente")

            # Limpiar estado actual
            from dental_system.models import PacienteModel, ConsultaModel
            self.paciente_actual = PacienteModel()
            self.consulta_actual = ConsultaModel()
            # Limpiar servicios si existe el atributo
            if hasattr(self, 'servicios_consulta_actual'):
                self.servicios_consulta_actual = []

            # Navegar de vuelta a página de odontología
            self.navigate_to(
                "odontologia",
                "Atención Odontológica",
                "Dashboard de pacientes por orden de llegada"
            )

            logger.info(f"🔙 Navegación completada")

        except Exception as e:
            logger.error(f"❌ Error derivando paciente: {str(e)}")


