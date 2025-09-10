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
    
    @classmethod
    def from_servicio(cls, servicio: ServicioModel, dientes: str, cantidad: int = 1):
        """Crear desde ServicioModel con dientes y cantidad"""
        return cls(
            id_servicio=servicio.id,
            nombre_servicio=servicio.nombre,
            categoria_servicio=servicio.categoria or "General",
            dientes_texto=dientes,
            cantidad=cantidad,
            precio_unitario_bs=servicio.precio_bs or 0.0,
            precio_unitario_usd=servicio.precio_usd or 0.0,
            total_bs=(servicio.precio_bs or 0.0) * cantidad,
            total_usd=(servicio.precio_usd or 0.0) * cantidad
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
                precio_bs=1460.0,
                precio_usd=40.0,
                activo=True
            ),
            ServicioModel(
                id="serv_002", 
                nombre="Limpieza Dental",
                categoria="Preventiva",
                precio_bs=2920.0,
                precio_usd=80.0,
                activo=True
            ),
            ServicioModel(
                id="serv_003",
                nombre="Endodoncia",
                categoria="Restaurativa", 
                precio_bs=11680.0,
                precio_usd=320.0,
                activo=True
            ),
            ServicioModel(
                id="serv_004",
                nombre="Obturación Simple",
                categoria="Restaurativa",
                precio_bs=1825.0,
                precio_usd=50.0,
                activo=True
            ),
            ServicioModel(
                id="serv_005",
                nombre="Extracción Simple",
                categoria="Cirugía",
                precio_bs=2190.0,
                precio_usd=60.0,
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
            return "Dientes (opcional - dejar vacío para toda la boca):"
    
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
        """📋 Cargar servicios para el selector de intervención"""
        try:
            logger.info("Cargando servicios para intervención...")
            
            # Prioridad 1: Cargar desde EstadoOdontologia si existe el método
            if hasattr(self, 'cargar_servicios_disponibles'):
                await self.cargar_servicios_disponibles()
                if self.servicios_disponibles:
                    logger.info(f"✅ Servicios cargados desde EstadoOdontologia: {len(self.servicios_disponibles)}")
                    return
            
            # Prioridad 2: Cargar desde EstadoServicios si existe el método
            if hasattr(self, 'cargar_lista_servicios'):
                await self.cargar_lista_servicios()
                if self.lista_servicios:
                    servicios_activos = [s for s in self.lista_servicios if s.activo]
                    logger.info(f"✅ Servicios cargados desde EstadoServicios: {len(servicios_activos)} activos")
                    return
            
            # Prioridad 3: Cargar directamente desde el servicio
            from dental_system.services.servicios_service import servicios_service
            
            # Establecer contexto de usuario si está disponible
            if hasattr(self, 'id_usuario') and hasattr(self, 'perfil_usuario'):
                servicios_service.set_user_context(self.id_usuario, self.perfil_usuario)
            
            # Cargar servicios activos
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
                print(f"✅ Servicio seleccionado: {servicio_encontrado.nombre} - ${servicio_encontrado.precio_usd} / {servicio_encontrado.precio_bs:,.0f} Bs")
            else:
                print(f"❌ Servicio no encontrado: {servicio_id}")
                print(f"📋 Servicios disponibles: {len(servicios_disponibles)}")
                
        except Exception as e:
            logger.error(f"Error seleccionando servicio temporal: {e}")
            import traceback
            traceback.print_exc()
    
    @rx.event
    def set_dientes_seleccionados_texto(self, texto: str):
        """🦷 Establecer texto de dientes seleccionados"""
        self.dientes_seleccionados_texto = texto.strip()
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
                cantidad=self.cantidad_temporal
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
        self.mensaje_error_intervencion = ""
    
    # ==========================================
    # 💾 MÉTODOS PARA FINALIZAR INTERVENCIÓN
    # ==========================================
    
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
                
                # Limpiar datos temporales
                self._limpiar_datos_intervencion()
                
                # Mostrar mensaje de éxito temporal
                self.mensaje_error_intervencion = f"✅ {resultado.get('message')} - Redirigiendo..."
                
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