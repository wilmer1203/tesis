# 🛒 ESTADO PARA GESTIÓN DE SERVICIOS EN INTERVENCIONES
# dental_system/state/estado_intervencion_servicios.py

import reflex as rx
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

# Modelos necesarios
from dental_system.models import ServicioModel, IntervencionModel

logger = logging.getLogger(__name__)

# Modelo para servicio temporal en el selector
class ServicioIntervencionTemporal(rx.Base):
    """🛒 Modelo temporal para servicios en intervención"""
    id_servicio: str = ""
    nombre_servicio: str = ""
    categoria_servicio: str = ""
    dientes_texto: str = ""
    cantidad: int = 1
    precio_unitario_bs: float = 0.0
    precio_unitario_usd: float = 0.0
    total_bs: float = 0.0
    total_usd: float = 0.0

    # 🆕 Nuevos campos clínicos
    material_utilizado: str = ""      # Amalgama, Resina, Composite, etc.
    superficie_dental: str = ""       # Oclusal, Mesial, Distal, etc.
    observaciones: str = ""           # Notas específicas del procedimiento
    
    @classmethod
    def from_servicio(cls, servicio: ServicioModel, dientes: str, cantidad: int = 1,
                     material: str = "", superficie: str = "", observaciones: str = ""):
        """Crear desde ServicioModel con dientes, cantidad y datos clínicos"""
        return cls(
            id_servicio=servicio.id,
            nombre_servicio=servicio.nombre,
            categoria_servicio=servicio.categoria or "General",
            dientes_texto=dientes,
            cantidad=cantidad,
            precio_unitario_bs=servicio.precio_base_bs or 0.0,
            precio_unitario_usd=servicio.precio_base_usd or 0.0,
            total_bs=(servicio.precio_base_bs or 0.0) * cantidad,
            total_usd=(servicio.precio_base_usd or 0.0) * cantidad,
            # 🆕 Nuevos campos clínicos
            material_utilizado=material,
            superficie_dental=superficie,
            observaciones=observaciones
        )

class EstadoIntervencionServicios(rx.State, mixin=True):
    """🛒 Estado especializado para gestión de servicios en intervenciones"""
    
    # ==========================================
    # 🛒 SELECTOR DE SERVICIOS TEMPORAL
    # ==========================================
    
    # Servicio temporal para selector
    servicio_temporal: ServicioModel = ServicioModel()
    dientes_seleccionados_texto: str = ""
    cantidad_temporal: int = 1

    # 🆕 Campos clínicos temporales
    material_temporal: str = ""
    superficie_temporal: str = ""
    observaciones_temporal: str = ""

    # 📋 Catálogos para selección
    materiales_disponibles: List[str] = [
        "Amalgama",
        "Resina Compuesta",
        "Composite",
        "Ionómero de Vidrio",
        "Porcelana",
        "Oro",
        "Temporal",
        "No Aplica"
    ]

    superficies_disponibles: List[str] = [
        "Oclusal",
        "Mesial",
        "Distal",
        "Vestibular",
        "Lingual/Palatino",
        "Incisal",
        "Completa",
        "No Específica"
    ]
    
    # ==========================================
    # 📋 LISTA DE SERVICIOS AGREGADOS
    # ==========================================
    
    # Lista de servicios agregados a la intervención actual
    servicios_en_intervencion: List[ServicioIntervencionTemporal] = []
    
    # Totales calculados
    total_intervencion_bs: float = 0.0
    total_intervencion_usd: float = 0.0
    
    # Estados de carga
    guardando_intervencion: bool = False
    
    # Mensajes de error para la UI
    mensaje_error_intervencion: str = ""
    
    # ==========================================
    # 💡 COMPUTED VARS PARA SERVICIOS
    # ==========================================
    
    @rx.var(cache=True)
    def servicios_para_selector(self) -> List[ServicioModel]:
        """📋 Lista unificada de servicios para el selector"""
        try:
            # Intentar usar servicios_disponibles primero (EstadoOdontologia)
            if hasattr(self, 'servicios_disponibles') and self.servicios_disponibles:
                servicios = self.servicios_disponibles
                logger.info(f"✅ Usando servicios_disponibles: {len(servicios)} servicios")
            # Fallback a lista_servicios (EstadoServicios)
            elif hasattr(self, 'lista_servicios') and self.lista_servicios:
                servicios = [s for s in self.lista_servicios if s.activo]
                logger.info(f"✅ Usando lista_servicios: {len(servicios)} servicios activos")
            else:
                # Crear servicios de ejemplo si no hay ninguno
                servicios = self._crear_servicios_ejemplo()
                logger.warning(f"⚠️ Usando servicios de ejemplo: {len(servicios)} servicios")
            
            return servicios
        except Exception as e:
            logger.error(f"Error obteniendo servicios para selector: {e}")
            return self._crear_servicios_ejemplo()
    
    def _crear_servicios_ejemplo(self) -> List[ServicioModel]:
        """🎯 Crear servicios de ejemplo para testing"""
        from dental_system.models import ServicioModel
        
        servicios_ejemplo = [
            ServicioModel(
                id="serv_001",
                nombre="Consulta General",
                categoria="Preventiva",
                precio_base_bs=1460.0,
                precio_base_usd=40.0,
                activo=True
            ),
            ServicioModel(
                id="serv_002",
                nombre="Limpieza Dental",
                categoria="Preventiva",
                precio_base_bs=2920.0,
                precio_base_usd=80.0,
                activo=True
            ),
            ServicioModel(
                id="serv_003",
                nombre="Endodoncia",
                categoria="Restaurativa",
                precio_base_bs=11680.0,
                precio_base_usd=320.0,
                activo=True
            ),
            ServicioModel(
                id="serv_004",
                nombre="Obturación Simple",
                categoria="Restaurativa",
                precio_base_bs=1825.0,
                precio_base_usd=50.0,
                activo=True
            ),
            ServicioModel(
                id="serv_005",
                nombre="Extracción Simple",
                categoria="Cirugía",
                precio_base_bs=2190.0,
                precio_base_usd=60.0,
                activo=True
            )
        ]
        
        logger.info(f"📋 Usando servicios de ejemplo: {len(servicios_ejemplo)} servicios")
        return servicios_ejemplo
    
    @rx.var
    def servicio_actual_requiere_dientes(self) -> bool:
        """🦷 Computed var: Si el servicio seleccionado requiere dientes específicos"""
        if not self.servicio_temporal or not self.servicio_temporal.id:
            return True  # Por defecto asumir que sí requiere
        return self.servicio_requiere_dientes(self.servicio_temporal)
    
    @rx.var 
    def texto_campo_dientes(self) -> str:
        """📝 Computed var: Texto del campo dientes según si es opcional o requerido"""
        if self.servicio_actual_requiere_dientes:
            return "Dientes afectados (requerido):"
        else:
            return "Dientes (opcional):"
    
    @rx.var
    def placeholder_campo_dientes(self) -> str:
        """💡 Computed var: Placeholder del campo dientes"""
        if self.servicio_actual_requiere_dientes:
            return "Requerido - Ej: 11, 12, 21"
        else:
            return "Opcional - Ej: 11, 12 o dejar vacío"
    
    # ==========================================
    # 🔧 MÉTODOS PARA SELECTOR DE SERVICIOS
    # ==========================================
    
    def servicio_requiere_dientes(self, servicio: ServicioModel) -> bool:
        """
        🦷 Determinar si un servicio requiere dientes específicos según su categoría
        
        Args:
            servicio: Modelo del servicio a evaluar
            
        Returns:
            True si requiere dientes específicos, False si es general
        """
        categorias_generales = ["Consulta", "Preventiva", "Diagnóstico", "Estética"]
        categoria = servicio.categoria if servicio.categoria else ""
        return categoria not in categorias_generales
    
    @rx.event
    async def cargar_servicios_para_intervencion(self):
        """📋 Reutilizar servicios ya cargados en el sistema"""
        try:
            # Simplificar: usar servicios ya disponibles en memoria
            if hasattr(self, 'servicios_disponibles') and self.servicios_disponibles:
                logger.info(f"✅ Reutilizando servicios de odontología: {len(self.servicios_disponibles)}")
                return

            if hasattr(self, 'lista_servicios') and self.lista_servicios:
                servicios_activos = [s for s in self.lista_servicios if s.activo]
                logger.info(f"✅ Reutilizando servicios del catálogo: {len(servicios_activos)} activos")
                return

            # Solo cargar si no hay servicios en memoria
            servicios_data = await servicios_service.get_filtered_services(activos_only=True)
            
            # Asignar a servicios_disponibles si existe el atributo
            if hasattr(self, 'servicios_disponibles'):
                self.servicios_disponibles = servicios_data
            # Si no, usar lista_servicios
            elif hasattr(self, 'lista_servicios'):
                self.lista_servicios = servicios_data
            
            logger.info(f"✅ Servicios cargados directamente: {len(servicios_data)}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando servicios para intervención: {e}")
            # En caso de error, los servicios de ejemplo se usarán automáticamente
    
    @rx.event
    def seleccionar_servicio_temporal(self, servicio_id: str):
        """🔧 Seleccionar servicio para agregar a la intervención"""
        try:
            # Limpiar mensaje de error cuando se selecciona servicio
            if self.mensaje_error_intervencion:
                self.mensaje_error_intervencion = ""
            
            # Si no hay servicios cargados, intentar cargarlos
            if not self.servicios_para_selector:
                logger.info("No hay servicios, intentando cargar...")
                # Nota: No podemos await aquí, se hará en background
                # El usuario tendrá que seleccionar de nuevo
            
            # Usar computed var unificado para buscar
            servicios_disponibles = self.servicios_para_selector
            
            servicio_encontrado = None
            for servicio in servicios_disponibles:
                if servicio.id == servicio_id:
                    servicio_encontrado = servicio
                    break
            
            if servicio_encontrado:
                self.servicio_temporal = servicio_encontrado
                print(f"✅ Servicio seleccionado: {servicio_encontrado.nombre} - ${servicio_encontrado.precio_base_usd} / {servicio_encontrado.precio_base_bs:,.0f} Bs")
            else:
                print(f"❌ Servicio no encontrado: {servicio_id}")
                print(f"📋 Servicios disponibles: {len(servicios_disponibles)}")
                
        except Exception as e:
            logger.error(f"Error seleccionando servicio temporal: {e}")
            import traceback
            traceback.print_exc()
    
    @rx.event
    def set_dientes_seleccionados_texto(self, texto: str):
        """🦷 Establecer texto de dientes seleccionados + sincronizar con odontograma"""
        self.dientes_seleccionados_texto = texto.strip()

        # ✨ SINCRONIZACIÓN: Campo manual → Odontograma visual
        try:
            # Actualizar formulario_intervencion.dientes_afectados para sincronizar con odontograma
            if hasattr(self, 'formulario_intervencion'):
                self.formulario_intervencion.dientes_afectados = texto.strip()
                # Actualizar la lista visual también
                if hasattr(self, 'actualizar_lista_dientes_seleccionados'):
                    self.actualizar_lista_dientes_seleccionados()
        except Exception as e:
            logger.warning(f"Error sincronizando odontograma: {e}")

        # Limpiar mensaje de error cuando el usuario empieza a escribir
        if self.mensaje_error_intervencion and texto.strip():
            self.mensaje_error_intervencion = ""
    
    @rx.event
    def set_cantidad_temporal(self, cantidad: str):
        """🔢 Establecer cantidad temporal"""
        try:
            cantidad_int = int(cantidad) if cantidad else 1
            self.cantidad_temporal = max(1, cantidad_int)  # Mínimo 1
        except ValueError:
            self.cantidad_temporal = 1

    # 🆕 Métodos para campos clínicos
    @rx.event
    def set_material_temporal(self, material: str):
        """🧱 Establecer material temporal"""
        self.material_temporal = material.strip()

    @rx.event
    def set_superficie_temporal(self, superficie: str):
        """🦷 Establecer superficie temporal"""
        self.superficie_temporal = superficie.strip()

    @rx.event
    def set_observaciones_temporal(self, observaciones: str):
        """📝 Establecer observaciones temporales"""
        self.observaciones_temporal = observaciones.strip()[:200]  # Límite 200 caracteres

    @rx.event
    def usar_dientes_del_odontograma(self):
        """🦷 Usar dientes seleccionados del odontograma"""
        try:
            # Limpiar mensaje de error
            self.mensaje_error_intervencion = ""
            
            # Si hay diente seleccionado en el odontograma, usarlo
            if hasattr(self, 'diente_seleccionado') and self.diente_seleccionado:
                self.dientes_seleccionados_texto = str(self.diente_seleccionado)
                logger.info(f"Dientes del odontograma: {self.diente_seleccionado}")
            elif hasattr(self, 'dientes_seleccionados') and self.dientes_seleccionados:
                # Si hay múltiples dientes seleccionados
                dientes_lista = [str(d) for d in self.dientes_seleccionados if d]
                if dientes_lista:
                    self.dientes_seleccionados_texto = ", ".join(dientes_lista)
                    logger.info(f"Dientes múltiples del odontograma: {dientes_lista}")
                else:
                    self.mensaje_error_intervencion = "🦷 Seleccione dientes en el odontograma o escriba manualmente"
            else:
                # Si no hay selección, mostrar mensaje
                self.mensaje_error_intervencion = "🦷 Seleccione dientes en el odontograma o escriba manualmente (ej: 11, 12, 21)"
                logger.info("No hay dientes seleccionados en el odontograma")
                
        except Exception as e:
            logger.error(f"Error usando dientes del odontograma: {e}")
            self.mensaje_error_intervencion = "❌ Error accediendo al odontograma"
    
    # ==========================================
    # ➕ MÉTODOS PARA AGREGAR/REMOVER SERVICIOS
    # ==========================================
    
    @rx.event
    def agregar_servicio_a_intervencion(self):
        """➕ Agregar servicio temporal a la lista de intervención"""
        try:
            # Limpiar mensaje de error previo
            self.mensaje_error_intervencion = ""
            
            # Validaciones básicas
            if not self.servicio_temporal.id:
                self.mensaje_error_intervencion = "⚠️ Debe seleccionar un servicio"
                logger.warning("No hay servicio seleccionado")
                return
            
            # Validación inteligente según tipo de servicio
            requiere_dientes = self.servicio_requiere_dientes(self.servicio_temporal)
            if requiere_dientes and not self.dientes_seleccionados_texto.strip():
                self.mensaje_error_intervencion = "🦷 Debe especificar los dientes afectados para este servicio (ej: 11, 12, 21)"
                logger.warning(f"Servicio {self.servicio_temporal.categoria} requiere dientes específicos")
                return
            elif not requiere_dientes and not self.dientes_seleccionados_texto.strip():
                # Para servicios generales, usar "Toda la boca" como valor por defecto
                self.dientes_seleccionados_texto = "Toda la boca"
                logger.info(f"Servicio {self.servicio_temporal.categoria} aplicado a toda la boca")
            
            # Crear servicio temporal para la intervención
            servicio_intervencion = ServicioIntervencionTemporal.from_servicio(
                servicio=self.servicio_temporal,
                dientes=self.dientes_seleccionados_texto,
                cantidad=self.cantidad_automatica,  # 🔢 Usar cantidad automática
                # 🆕 Incluir datos clínicos
                material=self.material_temporal,
                superficie=self.superficie_temporal,
                observaciones=self.observaciones_temporal
            )
            
            # Agregar a la lista
            self.servicios_en_intervencion.append(servicio_intervencion)
            
            # Recalcular totales
            self._recalcular_totales()
            
            # Limpiar selector temporal
            self._limpiar_selector_temporal()
            
            # Limpiar mensaje de error
            self.mensaje_error_intervencion = ""
            
            logger.info(f"Servicio agregado: {servicio_intervencion.nombre_servicio}")
            
        except Exception as e:
            logger.error(f"Error agregando servicio: {e}")
    
    @rx.event
    def remover_servicio_de_intervencion(self, index: int):
        """🗑️ Remover servicio de la intervención por índice"""
        try:
            if 0 <= index < len(self.servicios_en_intervencion):
                servicio_removido = self.servicios_en_intervencion.pop(index)
                self._recalcular_totales()
                logger.info(f"Servicio removido: {servicio_removido.nombre_servicio}")
            else:
                logger.warning(f"Índice inválido: {index}")
                
        except Exception as e:
            logger.error(f"Error removiendo servicio: {e}")
    
    def _recalcular_totales(self):
        """💰 Recalcular totales de la intervención"""
        try:
            total_bs = sum(servicio.total_bs for servicio in self.servicios_en_intervencion)
            total_usd = sum(servicio.total_usd for servicio in self.servicios_en_intervencion)
            
            self.total_intervencion_bs = total_bs
            self.total_intervencion_usd = total_usd
            
        except Exception as e:
            logger.error(f"Error recalculando totales: {e}")
            self.total_intervencion_bs = 0.0
            self.total_intervencion_usd = 0.0
    
    def _limpiar_selector_temporal(self):
        """🧹 Limpiar selector temporal después de agregar"""
        self.servicio_temporal = ServicioModel()
        self.dientes_seleccionados_texto = ""
        self.cantidad_temporal = 1
        # 🆕 Limpiar campos clínicos
        self.material_temporal = ""
        self.superficie_temporal = ""
        self.observaciones_temporal = ""
        self.mensaje_error_intervencion = ""
    
    # ==========================================
    # 🦷 MAPEO AUTOMÁTICO SERVICIO → CONDICIÓN ODONTOGRAMA
    # ==========================================

    # Diccionario que mapea servicios a condiciones de dientes automáticamente
    MAPEO_SERVICIOS_CONDICIONES = {
        # Restaurativos
        "obturacion": "obturacion",
        "resina": "obturacion",
        "restauracion": "obturacion",
        "amalgama": "obturacion",

        # Quirúrgicos
        "extraccion": "ausente",
        "cirugia": "ausente",
        "exodoncia": "ausente",

        # Endodoncia
        "endodoncia": "endodoncia",
        "conducto": "endodoncia",
        "tratamiento": "endodoncia",

        # Protésicos
        "corona": "corona",
        "puente": "puente",
        "protesis": "protesis",
        "implante": "implante",

        # Preventivos (no cambian condición - mantienen estado)
        "limpieza": None,
        "profilaxis": None,
        "consulta": None,
        "blanqueamiento": None,
        "radiografia": None
    }

    def obtener_tipo_condicion_por_servicio(self, nombre_servicio: str) -> str:
        """🦷 Determina automáticamente la condición del diente según el servicio aplicado"""
        if not nombre_servicio:
            return None

        nombre_lower = nombre_servicio.lower()

        # Buscar coincidencia en el mapeo
        for palabra_clave, condicion in self.MAPEO_SERVICIOS_CONDICIONES.items():
            if palabra_clave in nombre_lower:
                return condicion

        # Si no coincide con ninguna palabra clave, no modificar el odontograma
        return None

    # ==========================================
    # 💾 MÉTODOS PARA FINALIZAR INTERVENCIÓN
    # ==========================================
    
    @rx.event
    async def finalizar_mi_intervencion_odontologo(self):
        """
        🦷 NUEVO MÉTODO: Finalizar SOLO la intervención del odontólogo actual

        FLUJO CORRECTO:
        1. Guarda intervención con servicios en BD
        2. Actualiza odontograma automáticamente según servicios aplicados
        3. Crea nueva versión de odontograma (versionado)
        4. Cambia consulta a estado "entre_odontologos"
        5. Navega de vuelta a lista de pacientes

        NO completar la consulta (eso es del administrador)
        """
        try:
            self.guardando_intervencion = True

            # Validaciones previas
            if not self.servicios_en_intervencion:
                self.mensaje_error_intervencion = "❌ No hay servicios para guardar"
                logger.warning("No hay servicios para guardar")
                return

            if not hasattr(self, 'consulta_actual') or not self.consulta_actual.id:
                self.mensaje_error_intervencion = "❌ No hay consulta actual seleccionada"
                logger.warning("No hay consulta actual seleccionada")
                return

            logger.info(f"🦷 Iniciando finalización de MI intervención: {len(self.servicios_en_intervencion)} servicios")

            # Importar servicios necesarios
            from dental_system.services.odontologia_service import odontologia_service

            # Configurar contexto del usuario con información completa
            contexto_usuario = {
                **self.perfil_usuario,
                "rol": {"nombre": self.rol_usuario},  # Agregar rol explícitamente
                "usuario_id": self.id_usuario,
                "personal_id": getattr(self, 'id_personal', None)
            }
            odontologia_service.set_user_context(self.id_usuario, contexto_usuario)

            # 1. GUARDAR INTERVENCIÓN CON SERVICIOS
            servicios_backend = []
            for servicio in self.servicios_en_intervencion:
                servicio_data = {
                    "servicio_id": servicio.id_servicio,
                    "cantidad": servicio.cantidad,
                    "precio_unitario_bs": float(servicio.precio_unitario_bs),
                    "precio_unitario_usd": float(servicio.precio_unitario_usd),
                    "dientes_texto": servicio.dientes_texto,
                    "material_utilizado": servicio.material_utilizado,
                    "superficie_dental": servicio.superficie_dental,
                    "observaciones": servicio.observaciones or servicio.nombre_servicio
                }
                servicios_backend.append(servicio_data)

            datos_intervencion = {
                "consulta_id": self.consulta_actual.id,
                "odontologo_id": self.id_usuario,
                "servicios": servicios_backend,
                "observaciones_generales": f"Intervención del Dr. {self.perfil_usuario.get('nombre_completo', 'Usuario')} con {len(self.servicios_en_intervencion)} servicios",
                "requiere_control": False
            }

            # Crear intervención en BD
            resultado = await odontologia_service.crear_intervencion_con_servicios(datos_intervencion)

            if not resultado.get("success"):
                self.mensaje_error_intervencion = f"❌ Error guardando intervención: {resultado.get('message', 'Error desconocido')}"
                logger.error(f"Error en resultado del servicio: {resultado}")
                return

            intervencion_id = resultado.get("intervencion_id")
            logger.info(f"✅ Intervención guardada: {intervencion_id}")

            # 2. ACTUALIZAR ODONTOGRAMA AUTOMÁTICAMENTE
            await self._actualizar_odontograma_por_servicios(intervencion_id, self.servicios_en_intervencion)

            # 3. CAMBIAR ESTADO CONSULTA A "ENTRE_ODONTOLOGOS"
            await self._cambiar_estado_consulta_entre_odontologos()

            # 4. CREAR PAGO PENDIENTE
            try:
                await self._crear_pago_pendiente_consulta(
                    consulta_id=self.consulta_actual.id,
                    total_usd=resultado.get("total_usd", 0.0),
                    total_bs=resultado.get("total_bs", 0.0),
                    servicios_count=len(self.servicios_en_intervencion)
                )
                logger.info("💳 Pago pendiente creado automáticamente")
            except Exception as e:
                logger.warning(f"⚠️ Error creando pago pendiente: {str(e)}")

            # 5. LIMPIAR Y NAVEGAR
            self._limpiar_datos_intervencion()

            self.mensaje_error_intervencion = f"✅ Mi intervención finalizada exitosamente - Odontograma actualizado - Redirigiendo..."

            # Navegar después de 2 segundos
            await self.set_timeout(self.navegar_despues_guardado, 2000)

        except Exception as e:
            error_msg = f"Error finalizando mi intervención: {str(e)}"
            self.mensaje_error_intervencion = f"❌ {error_msg}"
            logger.error(error_msg)
        finally:
            self.guardando_intervencion = False

    async def _actualizar_odontograma_por_servicios(self, intervencion_id: str, servicios: List):
        """
        🦷 Actualizar odontograma automáticamente según servicios aplicados
        """
        try:
            from dental_system.supabase.tablas.condiciones_diente import condiciones_diente_table
            from dental_system.supabase.tablas.dientes import dientes_table
            from dental_system.supabase.tablas.odontograma import odontograms_table

            # Obtener odontograma actual del paciente
            if not self.paciente_actual or not self.paciente_actual.id:
                logger.warning("No hay paciente actual válido para actualizar odontograma")
                return

            odontograma_actual = await odontograms_table.get_active_odontogram(self.paciente_actual.id)

            if not odontograma_actual:
                logger.warning(f"No se encontró odontograma para paciente {self.paciente_actual.id}")
                return

            cambios_realizados = 0

            # Para cada servicio aplicado
            for servicio in servicios:
                # Determinar nueva condición automáticamente
                nueva_condicion = self.obtener_tipo_condicion_por_servicio(servicio.nombre_servicio)

                if not nueva_condicion:
                    logger.info(f"Servicio '{servicio.nombre_servicio}' no modifica odontograma (preventivo)")
                    continue

                # Procesar dientes afectados
                dientes_afectados = self._extraer_numeros_dientes(servicio.dientes_texto)

                if not dientes_afectados:
                    logger.warning(f"No se encontraron dientes válidos en '{servicio.dientes_texto}'")
                    continue

                # Actualizar cada diente afectado
                for numero_diente in dientes_afectados:
                    try:
                        # Buscar diente en catálogo FDI
                        diente_fdi = await dientes_table.get_by_numero(numero_diente)
                        if not diente_fdi:
                            logger.warning(f"Diente {numero_diente} no encontrado en catálogo FDI")
                            continue

                        # Crear nueva condición del diente usando método correcto
                        nueva_condicion_resultado = await condiciones_diente_table.create_condicion(
                            odontograma_id=odontograma_actual["id"],
                            diente_id=diente_fdi["id"],
                            tipo_condicion=nueva_condicion,
                            registrado_por=self.id_usuario,
                            caras_afectadas=[servicio.superficie_dental] if servicio.superficie_dental else ["oclusal"],
                            descripcion=f"Aplicado: {servicio.nombre_servicio}",
                            material_utilizado=servicio.material_utilizado
                        )
                        cambios_realizados += 1

                        logger.info(f"✅ Diente {numero_diente}: {nueva_condicion} - Material: {servicio.material_utilizado}")

                    except Exception as e:
                        logger.error(f"Error actualizando diente {numero_diente}: {str(e)}")

            # 3. CREAR NUEVA VERSIÓN DE ODONTOGRAMA (si hubo cambios)
            if cambios_realizados > 0:
                await self._crear_nueva_version_odontograma(
                    odontograma_actual["id"],
                    f"Intervención con {cambios_realizados} dientes modificados",
                    intervencion_id
                )
                logger.info(f"🆕 Nueva versión de odontograma creada - {cambios_realizados} cambios")
            else:
                logger.info("ℹ️ No se modificó el odontograma (servicios preventivos)")

        except Exception as e:
            logger.error(f"Error actualizando odontograma: {str(e)}")

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

    async def _crear_nueva_version_odontograma(self, odontograma_actual_id: str, motivo: str, intervencion_id: str):
        """🆕 Crear nueva versión del odontograma automáticamente"""
        try:
            from dental_system.supabase.tablas.odontograma import odontograms_table

            # Usar el método correcto para crear una nueva versión
            nueva_version = await odontograms_table.create_odontogram(
                paciente_id=self.paciente_actual.id,
                odontologo_id=self.id_usuario,
                tipo_odontograma="adulto",
                notas_generales=motivo,
                observaciones_clinicas=f"Intervención ID: {intervencion_id}"
            )
            logger.info(f"✅ Nueva versión de odontograma creada para paciente {self.paciente_actual.id}")

        except Exception as e:
            logger.error(f"Error creando nueva versión de odontograma: {str(e)}")

    async def _cambiar_estado_consulta_entre_odontologos(self):
        """🔄 Cambiar consulta a estado 'entre_odontologos'"""
        try:
            from dental_system.supabase.tablas.consultas import consultas_table

            await consultas_table.update_status(
                self.consulta_actual.id,
                "entre_odontologos"
            )

            logger.info(f"🔄 Consulta {self.consulta_actual.numero_consulta} marcada como 'entre_odontologos'")

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
            if hasattr(self, 'servicios_en_intervencion') and len(self.servicios_en_intervencion) > 0:
                logger.info(f"💾 Guardando intervención antes de derivar ({len(self.servicios_en_intervencion)} servicios)")

                # Guardar la intervención actual
                await self.finalizar_consulta_completa()

                # Esperar un momento para que se complete el guardado
                import asyncio
                await asyncio.sleep(0.5)

            # Cambiar estado de consulta a "entre_odontologos"
            await self._cambiar_estado_consulta_entre_odontologos()

            logger.info(f"✅ Paciente {self.paciente_actual.nombre_completo} derivado exitosamente")
            
            # Limpiar estado actual
            from dental_system.models import PacienteModel, ConsultaModel
            self.paciente_actual = PacienteModel()
            self.consulta_actual = ConsultaModel()
            self.servicios_en_intervencion = []

            # Navegar de vuelta a página de odontología
            self.navigate_to(
                "odontologia",
                "Atención Odontológica",
                "Dashboard de pacientes por orden de llegada"
            )

            logger.info(f"🔙 Navegación completada")

        except Exception as e:
            logger.error(f"❌ Error derivando paciente: {str(e)}")


    @rx.event
    async def finalizar_consulta_completa(self):
        """💾 Finalizar consulta creando intervención + servicios"""
        try:
            self.guardando_intervencion = True
            
            # Validaciones previas
            if not self.servicios_en_intervencion:
                self.mensaje_error_intervencion = "❌ No hay servicios para guardar"
                logger.warning("No hay servicios para guardar")
                return
                
            if not hasattr(self, 'consulta_actual') or not self.consulta_actual.id:
                self.mensaje_error_intervencion = "❌ No hay consulta actual seleccionada"
                logger.warning("No hay consulta actual seleccionada")
                return
            
            logger.info(f"💾 Iniciando guardado de {len(self.servicios_en_intervencion)} servicios")
            
            # Importar el servicio de odontología
            from dental_system.services.odontologia_service import odontologia_service
            
            # Configurar contexto del usuario para el servicio
            odontologia_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Preparar datos de servicios para el backend
            servicios_backend = []
            for servicio in self.servicios_en_intervencion:
                servicio_data = {
                    "servicio_id": servicio.id_servicio,
                    "cantidad": servicio.cantidad,
                    "precio_unitario_bs": float(servicio.precio_unitario_bs),
                    "precio_unitario_usd": float(servicio.precio_unitario_usd),
                    "dientes_texto": servicio.dientes_texto,
                    "observaciones": servicio.nombre_servicio  # Usar el nombre como observación base
                }
                servicios_backend.append(servicio_data)
            
            # Preparar datos de la intervención completa
            datos_intervencion = {
                "consulta_id": self.consulta_actual.id,
                "odontologo_id": self.id_usuario,  # El servicio hará la conversión a personal_id
                "servicios": servicios_backend,
                "observaciones_generales": f"Intervención realizada con {len(self.servicios_en_intervencion)} servicios",
                "requiere_control": False  # Valor por defecto
            }
            
            logger.info(f"📋 Datos preparados: {len(servicios_backend)} servicios, totales: BS {self.total_intervencion_bs:,.2f}, USD ${self.total_intervencion_usd:,.2f}")
            
            # Llamar al servicio para crear la intervención con servicios
            resultado = await odontologia_service.crear_intervencion_con_servicios(datos_intervencion)
            
            if resultado.get("success"):
                logger.info(f"🎉 Intervención guardada exitosamente: {resultado.get('message')}")

                # 💳 CREAR PAGO PENDIENTE AUTOMÁTICO
                try:
                    await self._crear_pago_pendiente_consulta(
                        consulta_id=self.consulta_actual.id,
                        total_usd=resultado.get("total_usd", 0.0),
                        total_bs=resultado.get("total_bs", 0.0),
                        servicios_count=len(self.servicios_en_intervencion)
                    )
                    logger.info("💳 Pago pendiente creado automáticamente")
                except Exception as e:
                    logger.warning(f"⚠️ Error creando pago pendiente: {str(e)}")
                    # No falla el proceso principal, solo log del error

                # Limpiar datos temporales
                self._limpiar_datos_intervencion()

                # Mostrar mensaje de éxito temporal
                self.mensaje_error_intervencion = f"✅ {resultado.get('message')} - Pago pendiente creado - Redirigiendo..."

                # Navegar de regreso después de un breve delay
                await self.set_timeout(self.navegar_despues_guardado, 2000)  # 2 segundos
                
            else:
                self.mensaje_error_intervencion = f"❌ Error guardando: {resultado.get('message', 'Error desconocido')}"
                logger.error(f"Error en resultado del servicio: {resultado}")
            
        except Exception as e:
            error_msg = f"Error finalizando consulta: {str(e)}"
            self.mensaje_error_intervencion = f"❌ {error_msg}"
            logger.error(error_msg)
        finally:
            self.guardando_intervencion = False
    
    @rx.event 
    async def navegar_despues_guardado(self):
        """📍 Navegar de regreso después del guardado exitoso"""
        try:
            # Limpiar mensaje de éxito
            self.mensaje_error_intervencion = ""
            
            # Navegar de regreso a la página de odontología
            self.navigate_to("odontologia")  # Via mixin EstadoUI
            
            logger.info("🔄 Navegación completada después del guardado")
            
        except Exception as e:
            logger.error(f"Error navegando después del guardado: {e}")
    
    async def set_timeout(self, callback, milliseconds):
        """⏰ Simula setTimeout de JavaScript"""
        import asyncio
        await asyncio.sleep(milliseconds / 1000)
        await callback()
    
    @rx.event
    def cancelar_intervencion(self):
        """❌ Cancelar intervención y limpiar datos"""
        try:
            self._limpiar_datos_intervencion()
            self.navigate_to("odontologia")  # Via mixin EstadoUI
            logger.info("Intervención cancelada")
            
        except Exception as e:
            logger.error(f"Error cancelando intervención: {e}")
    
    def _limpiar_datos_intervencion(self):
        """🧹 Limpiar todos los datos de la intervención"""
        self.servicios_en_intervencion = []
        self.total_intervencion_bs = 0.0
        self.total_intervencion_usd = 0.0
        self.servicio_temporal = ServicioModel()
        self.dientes_seleccionados_texto = ""
        self.cantidad_temporal = 1
        self.guardando_intervencion = False

    async def _crear_pago_pendiente_consulta(self, consulta_id: str, total_usd: float, total_bs: float, servicios_count: int):
        """💳 Crear pago pendiente automático al completar consulta"""
        try:
            # Importar el servicio de pagos
            from dental_system.services.pagos_service import pagos_service

            # Obtener número de consulta para el concepto
            consulta_numero = getattr(self.consulta_actual, 'numero_consulta', 'CONS-001')

            # Obtener tasa de cambio actual (desde EstadoPagos mixin)
            tasa_actual = getattr(self, 'tasa_del_dia', 36.50)

            # Preparar datos del pago pendiente
            pago_data = {
                "consulta_id": consulta_id,
                "paciente_id": getattr(self.paciente_actual, 'id', ''),
                "monto_total_usd": float(total_usd),
                "monto_total_bs": float(total_bs),
                "monto_pagado_usd": 0.0,
                "monto_pagado_bs": 0.0,
                "saldo_pendiente_usd": float(total_usd),
                "saldo_pendiente_bs": float(total_bs),
                "tasa_cambio_bs_usd": float(tasa_actual),
                "concepto": f"Consulta {consulta_numero} - {servicios_count} servicios realizados",
                "estado_pago": "pendiente",
                "procesado_por": self.id_usuario,
                "metodos_pago": []  # Se completará cuando se procese el pago
            }

            logger.info(f"💳 Creando pago pendiente: ${total_usd:.2f} USD ({total_bs:.2f} BS)")

            # Crear el pago pendiente usando el servicio dual
            resultado = await pagos_service.create_dual_payment(pago_data, self.id_usuario)

            if resultado:
                logger.info(f"✅ Pago pendiente creado: {resultado.get('numero_recibo', 'N/A')}")
                return True
            else:
                logger.error("❌ Error: Servicio de pagos no devolvió resultado")
                return False

        except Exception as e:
            logger.error(f"❌ Error creando pago pendiente: {str(e)}")
            return False

    # ==========================================
    # 🧮 COMPUTED VARS - CANTIDAD AUTOMÁTICA
    # ==========================================

    @rx.var
    def cantidad_automatica(self) -> int:
        """🔢 Calcular cantidad automáticamente basado en dientes seleccionados"""
        try:
            texto_dientes = self.dientes_seleccionados_texto.strip()

            if not texto_dientes:
                return 1

            # Casos especiales para servicios generales
            if texto_dientes.lower() in ["todos", "toda la boca", "todas"]:
                return 1  # Un servicio general para toda la boca

            # Contar dientes individuales separados por comas
            dientes = [x.strip() for x in texto_dientes.split(",") if x.strip()]
            dientes_validos = [d for d in dientes if d.isdigit() and 11 <= int(d) <= 48]

            return max(1, len(dientes_validos))  # Mínimo 1

        except Exception as e:
            logger.warning(f"Error calculando cantidad automática: {e}")
            return 1

    @rx.var
    def precio_total_calculado_bs(self) -> float:
        """💰 Precio total en BS basado en cantidad automática"""
        try:
            if hasattr(self.servicio_temporal, 'precio_base_bs') and self.servicio_temporal.precio_base_bs:
                return float(self.servicio_temporal.precio_base_bs) * self.cantidad_automatica
            return 0.0
        except Exception:
            return 0.0

    @rx.var
    def precio_total_calculado_usd(self) -> float:
        """💰 Precio total en USD basado en cantidad automática"""
        try:
            if hasattr(self.servicio_temporal, 'precio_usd') and self.servicio_temporal.precio_usd:
                return float(self.servicio_temporal.precio_usd) * self.cantidad_automatica
            return 0.0
        except Exception:
            return 0.0