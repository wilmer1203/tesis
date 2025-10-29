"""
💳 ESTADO DE PAGOS - SUBSTATE SEPARADO
=======================================

PROPÓSITO: Manejo centralizado y especializado de pagos y facturación
- Sistema completo de facturación y pagos
- CRUD completo de pagos con validaciones
- Múltiples métodos de pago
- Manejo de pagos parciales y saldos pendientes
- Generación de recibos auto-numerados
- Estadísticas financieras
- Cache inteligente para performance

USADO POR: AppState como coordinador principal  
PATRÓN: Substate con get_estado_pagos() en AppState
"""

import reflex as rx
from datetime import date, datetime
from typing import Dict, Any, List, Optional, Union
import logging

# Servicios y modelos
from dental_system.services.pagos_service import pagos_service
from dental_system.constants import METODOS_PAGO, ESTADOS_PAGO
from dental_system.models import (
    PagoModel,
    PagosStatsModel,
    BalanceGeneralModel,
    CuentaPorCobrarModel,
    PagoFormModel,
    ConsultaPendientePago,
    ServicioFormateado
)

logger = logging.getLogger(__name__)


class EstadoPagos(rx.State,mixin=True):
    """
    💳 ESTADO ESPECIALIZADO EN GESTIÓN DE PAGOS Y FACTURACIÓN
    
    RESPONSABILIDADES:
    - CRUD completo de pagos con validaciones de negocio
    - Sistema de facturación con auto-numeración
    - Manejo de múltiples métodos de pago
    - Gestión de pagos parciales y saldos pendientes
    - Generación de recibos y facturas
    - Estadísticas financieras y métricas
    - Cache inteligente para operaciones pesadas
    """
    
    # ==========================================
    # 💳 VARIABLES PRINCIPALES DE PAGOS
    # ==========================================
    
    # Lista principal de pagos (modelos tipados)
    lista_pagos: List[PagoModel] = []
    total_pagos: int = 0
    errores_validacion_pago: Dict[str, str] = {}

    # Variables auxiliares para operaciones
    cargando_lista_pagos: bool = False

    # ==========================================
    # 💰 NUEVAS VARIABLES SISTEMA DUAL USD/BS
    # ==========================================

    # 📊 FORMULARIO DUAL SIMPLIFICADO
    formulario_pago_dual: PagoFormModel = PagoFormModel()
    modal_pago_dual_abierto: bool = False

    # 💱 TASA DE CAMBIO DINÁMICA
    tasa_del_dia: float = 36.50              # Tasa editable por usuario
    tasa_sugerida: float = 36.50             # Tasa sugerida del sistema
    tasa_historica: List[Dict[str, Any]] = [] # Historial de tasas usadas

    # 📊 ESTADÍSTICAS DUALES EN TIEMPO REAL
    estadisticas_dual: Dict[str, Any] = {}
    recaudacion_usd_hoy: float = 0.0
    recaudacion_bs_hoy: float = 0.0
    pendiente_usd_total: float = 0.0
    pendiente_bs_total: float = 0.0

    # 🎛️ CALCULADORA DE CONVERSIÓN EN VIVO
    calculadora_activa: bool = False
    monto_calculadora_usd: str = "0"
    monto_calculadora_bs: str = "0"
    calculando_conversion: bool = False

    # 📈 DISTRIBUCIÓN DE PAGOS POR MONEDA
    pagos_mixtos_count: int = 0
    pagos_solo_usd_count: int = 0
    pagos_solo_bs_count: int = 0
    preferencia_moneda_del_dia: str = "USD"  # USD, BS, MIXTO

    # 🎨 MODO DE VISTA DUAL
    vista_dual_activa: bool = True           # Si mostrar ambas monedas
    moneda_principal_vista: str = "USD"      # USD o BS para simplificar UI
    mostrar_conversion_automatica: bool = True

    # ==========================================
    # 🏥 CONSULTAS PENDIENTES DE FACTURACIÓN
    # ==========================================

    # Lista de consultas completadas pendientes de pago
    consultas_pendientes_facturacion: List[Dict[str, Any]] = []
    consulta_seleccionada_pago: Optional[Dict[str, Any]] = None
    cargando_consultas_pendientes: bool = False

    # 📝 DATOS ADICIONALES DE LA CONSULTA SELECCIONADA (para el modal)
    consulta_actual_numero_historia: str = ""
    consulta_actual_documento: str = ""
    consulta_actual_telefono: str = ""
    
    consulta_pagar : Optional[ConsultaPendientePago] = None
    consultas_pendientes_pagar: List[ConsultaPendientePago] = None
    # ==========================================
    # 💳 MÉTODOS DE PAGO Y CONFIGURACIÓN
    # ==========================================

    # Métodos de pago disponibles (importados desde constants.py)
    # Mantenemos como variable de estado para posible personalización por clínica
    metodos_pago_disponibles: List[str] = METODOS_PAGO

    # ==========================================
    # 💳 FILTROS Y BÚSQUEDAS ESPECIALIZADAS
    # ==========================================
    
    # Búsqueda principal
    termino_busqueda_pagos: str = ""
    buscar_por_paciente: str = ""
    buscar_por_numero_recibo: str = ""
    
    # Filtros avanzados
    filtro_metodo_pago: str = "todos"  # todos, efectivo, tarjeta, etc.
    filtro_estado_pago: str = "todos"  # todos, pendiente, completado, etc.
    filtro_fecha_pagos: str = date.today().isoformat()
    filtro_rango_monto: Dict[str, float] = {"min": 0.0, "max": 999999.0}
    
    # Filtros de fechas
    rango_fecha_inicio: str = ""
    rango_fecha_fin: str = ""
    
    # Ordenamiento
    campo_ordenamiento_pagos: str = "fecha_pago"  # fecha_pago, monto, numero_recibo
    direccion_ordenamiento_pagos: str = "desc"  # asc, desc
    
    # Paginación
    pagina_actual_pagos: int = 1
    pagos_por_pagina: int = 15
    total_paginas_pagos: int = 1
    
    # ==========================================
    # 💳 ESTADÍSTICAS Y MÉTRICAS FINANCIERAS
    # ==========================================
    
    # Estadísticas principales
    estadisticas_pagos: PagosStatsModel = PagosStatsModel()
    balance_general: BalanceGeneralModel = BalanceGeneralModel()
    ultima_actualizacion_stats: str = ""
    
    # Métricas financieras rápidas
    recaudacion_hoy: float = 0.0
    recaudacion_mes: float = 0.0
    saldo_pendiente_total: float = 0.0
    total_facturas_pendientes: int = 0
    
    # Cache de operaciones pesadas
    cache_pagos_recientes: List[PagoModel] = []
    cache_cuentas_por_cobrar: List[CuentaPorCobrarModel] = []
    cache_timestamp_pagos: str = ""
    cache_validez_minutos: int = 10  # Cache más corto para datos financieros
    
    # Estados de carga
    cargando_estadisticas_pagos: bool = False
    cargando_operacion_pago: bool = False
    procesando_pago: bool = False
    
    # ==========================================
    # 💳 COMPUTED VARS PARA UI (SIN ASYNC)
    # ==========================================
    
    
    @rx.var(cache=True)
    def pagos_pendientes(self) -> List[PagoModel]:
        """⏳ Pagos pendientes"""
        return [p for p in self.lista_pagos if p.estado_pago == "pendiente"]
   
    @rx.var(cache=True)
    def total_pagos_pendientes(self) -> int:
        """📊 Total de pagos pendientes"""
        return len(self.pagos_pendientes)
    
    @rx.var(cache=True)
    def total_saldo_pendiente(self) -> float:
        """💰 Total saldo pendiente"""
        return sum(p.saldo_pendiente for p in self.lista_pagos)
    
    # @rx.var(cache=True)
    # def recaudacion_del_dia(self) -> float:
    #     """💵 Recaudación del día"""
    #     hoy = date.today()
    #     return sum(
    #         p.monto_pagado for p in self.lista_pagos 
    #         if p.fecha_pago.date() == hoy and p.estado_pago == "completado"
    #     )
    

    # ==========================================
    # 💳 MÉTODOS PRINCIPALES DE CRUD
    # ==========================================
    
    @rx.event
    async def cargar_lista_pagos(self, force_refresh: bool = False):
        """💳 CARGAR LISTA COMPLETA DE PAGOS"""
        try:
            self.cargando_lista_pagos = True

            print(f"🔍 DEBUG: Cargando lista de pagos...")
            # Cargar desde el servicio
            pagos_data = await pagos_service.get_all_payments()
            print(f"🔍 Pagos recibidos: {len(pagos_data) if pagos_data else 0}")
            # Convertir a modelos tipados
            self.lista_pagos = pagos_data
            self.total_pagos = len(self.lista_pagos)

            # Actualizar métricas rápidas
            # await self._actualizar_metricas_rapidas()

            logger.info(f"✅ {len(self.lista_pagos)} pagos cargados")
            
        except Exception as e:
            logger.error(f"❌ Error cargando pagos: {str(e)}")
        finally:
            self.cargando_lista_pagos = False

    @rx.event
    async def buscar_pagos(self, query: str):
        """🔍 BUSCAR PAGOS"""
        self.termino_busqueda_pagos = query.strip()
        logger.info(f"🔍 Búsqueda de pagos: '{query}'")

    # ==========================================
    # 💰 MÉTODOS SISTEMA DUAL USD/BS
    # ==========================================

    @rx.var(cache=True)
    def total_pagando_usd(self) -> float:
        """💰 Calcular total pagando en USD (conversión automática de BS)"""
        try:
            pago_usd = float(self.formulario_pago_dual.monto_pagado_usd or 0)
            pago_bs = float(self.formulario_pago_dual.monto_pagado_bs or 0)
            tasa = float(self.formulario_pago_dual.tasa_cambio or 36.50)

            bs_a_usd = pago_bs / tasa if tasa > 0 else 0
            return pago_usd + bs_a_usd
        except:
            return 0.0

    @rx.var(cache=True)
    def saldo_pendiente_calculado(self) -> float:
        """💰 Calcular saldo pendiente después del pago"""
        try:
            total = float(self.formulario_pago_dual.monto_total_usd or 0)
            pagando = self.total_pagando_usd
            descuento = float(self.formulario_pago_dual.descuento_usd or 0)

            saldo = total - descuento - pagando
            return saldo if saldo > 0 else 0.0
        except:
            return 0.0

    @rx.var(cache=True)
    def equivalente_bs_de_usd_pagado(self) -> float:
        """💱 Convertir USD pagado a BS"""
        try:
            pago_usd = float(self.formulario_pago_dual.monto_pagado_usd or 0)
            tasa = float(self.formulario_pago_dual.tasa_cambio or 36.50)
            return pago_usd * tasa if tasa > 0 else 0
        except:
            return 0.0

    @rx.var(cache=True)
    def equivalente_usd_de_bs_pagado(self) -> float:
        """💱 Convertir BS pagado a USD"""
        try:
            pago_bs = float(self.formulario_pago_dual.monto_pagado_bs or 0)
            tasa = float(self.formulario_pago_dual.tasa_cambio or 36.50)
            return pago_bs / tasa if tasa > 0 else 0
        except:
            return 0.0

    @rx.event
    def actualizar_campo_pago_dual(self, campo: str, valor: str):
        """Actualizar campo del formulario de pago dual"""
        try:
            if campo == "monto_pagado_usd":
                self.formulario_pago_dual.monto_pagado_usd = float(valor) if valor else 0.0
            elif campo == "monto_pagado_bs":
                self.formulario_pago_dual.monto_pagado_bs = float(valor) if valor else 0.0
            elif campo == "metodo_pago_usd":
                self.formulario_pago_dual.metodo_pago_usd = valor
            elif campo == "metodo_pago_bs":
                self.formulario_pago_dual.metodo_pago_bs = valor
            elif campo == "referencia_usd":
                self.formulario_pago_dual.referencia_usd = valor
            elif campo == "referencia_bs":
                self.formulario_pago_dual.referencia_bs = valor
            elif campo == "descuento_usd":
                self.formulario_pago_dual.descuento_usd = float(valor) if valor else 0.0
            elif campo == "motivo_descuento":
                self.formulario_pago_dual.motivo_descuento = valor
            elif campo == "notas":
                self.formulario_pago_dual.notas = valor
        except Exception as e:
            logger.error(f"Error actualizando campo {campo}: {str(e)}")

    @rx.event
    def limpiar_formulario_pago_dual(self):
        """Limpiar formulario de pago dual"""
        self.formulario_pago_dual = PagoFormModel()
        self.errores_validacion_pago = {}
        self.modal_pago_dual_abierto = False

        # Limpiar datos adicionales del modal
        self.consulta_actual_numero_historia = ""
        self.consulta_actual_documento = ""
        self.consulta_actual_telefono = ""

    @rx.event
    async def crear_pago_dual(self):
        """💰 PROCESAR PAGO DUAL USD/BS (Actualizar pago pendiente)"""
        try:
            print("ejecutando el proceso de pago")
            self.procesando_pago = True
            self.errores_validacion_pago = {}

            # Validar formulario dual
            errores = await self._validar_formulario_dual()
            print(errores)
            if errores:
                self.errores_validacion_pago = errores
                return  # ✅ Return None
            print(self.formulario_pago_dual.pago_id)
            # ✅ VERIFICAR QUE HAY PAGO_ID (directo, sin buscar por consulta)
            if not self.formulario_pago_dual.pago_id:
                self.errores_validacion_pago["general"] = "No hay pago seleccionado"
                logger.error("❌ pago_id está vacío en formulario_pago_dual")
                return  # ✅ Return None

            # Establecer contexto de usuario antes de llamar al servicio
            pagos_service.set_user_context(self.id_usuario, self.perfil_usuario)
            print("--------------preparando los datos----------------")
            # 📊 PREPARAR DATOS DE ACTUALIZACIÓN
            datos_actualizacion = {
                "monto_pagado_usd": float(self.formulario_pago_dual.monto_pagado_usd),
                "monto_pagado_bs": float(self.formulario_pago_dual.monto_pagado_bs),
                "descuento_usd": float(self.formulario_pago_dual.descuento_usd),
                "motivo_descuento": self.formulario_pago_dual.motivo_descuento if self.formulario_pago_dual.descuento_usd > 0 else None,
                "observaciones": self.formulario_pago_dual.notas or self.formulario_pago_dual.observaciones,
                "tasa_cambio_bs_usd": float(self.formulario_pago_dual.tasa_cambio)
            }

            # 🎛️ CONSTRUIR metodos_pago JSONB
            metodos_pago = []
            if self.formulario_pago_dual.monto_pagado_usd > 0:
                metodos_pago.append({
                    "tipo": self.formulario_pago_dual.metodo_pago_usd,
                    "moneda": "USD",
                    "monto": float(self.formulario_pago_dual.monto_pagado_usd),
                    "referencia": self.formulario_pago_dual.referencia_usd or None
                })

            if self.formulario_pago_dual.monto_pagado_bs > 0:
                metodos_pago.append({
                    "tipo": self.formulario_pago_dual.metodo_pago_bs,
                    "moneda": "BS",
                    "monto": float(self.formulario_pago_dual.monto_pagado_bs),
                    "referencia": self.formulario_pago_dual.referencia_bs or None
                })

            datos_actualizacion["metodos_pago"] = metodos_pago

            # 🧮 CALCULAR SALDOS
            total_pagado_usd = float(self.formulario_pago_dual.monto_pagado_usd) + (float(self.formulario_pago_dual.monto_pagado_bs) / float(self.formulario_pago_dual.tasa_cambio))
            saldo_pendiente_usd = max(0, float(self.formulario_pago_dual.monto_total_usd) - float(self.formulario_pago_dual.descuento_usd) - total_pagado_usd)

            datos_actualizacion["saldo_pendiente_usd"] = saldo_pendiente_usd
            datos_actualizacion["saldo_pendiente_bs"] = saldo_pendiente_usd * float(self.formulario_pago_dual.tasa_cambio)
            datos_actualizacion["estado_pago"] = "completado" if saldo_pendiente_usd <= 0.01 else "pendiente"
            datos_actualizacion["monto_total_bs"] = float(self.formulario_pago_dual.monto_total_usd) * float(self.formulario_pago_dual.tasa_cambio)

            print("vamos a entar a la funcion de servicio para agregar el pago ")
            # 💾 ACTUALIZAR PAGO EXISTENTE usando pago_id directamente
            pago_actualizado = await pagos_service.update_payment(self.formulario_pago_dual.pago_id, datos_actualizacion)

            if pago_actualizado:
                # Recargar consultas pendientes (quitar la que se pagó si está completa)
                await self.cargar_consultas_pendientes_pago()

                # ✅ Recargar lista de pagos para actualizar historial en la tabla
                await self.cargar_lista_pagos()

                # Limpiar formulario y cerrar modal
                self.formulario_pago_dual = PagoFormModel()
                self.errores_validacion_pago = {}
                self.modal_pago_dual_abierto = False

                logger.info(f"✅ Pago actualizado exitosamente ID: {self.formulario_pago_dual.pago_id}")
            else:
                self.errores_validacion_pago["general"] = "Error al actualizar el pago"

        except Exception as e:
            error_msg = f"Error procesando pago dual: {str(e)}"
            self.errores_validacion_pago["general"] = error_msg
            logger.error(error_msg)
        finally:
            self.modal_pago_dual_abierto = False
            self.procesando_pago = False

    @rx.event
    async def actualizar_tasa_del_dia(self, nueva_tasa: float):
        """💱 ACTUALIZAR TASA DE CAMBIO DEL DÍA"""
        try:
            if nueva_tasa <= 0:
                logger.warning("⚠️ Tasa de cambio debe ser mayor a 0")
                return False

            # Guardar tasa anterior en historial
            if self.tasa_del_dia != nueva_tasa:
                self.tasa_historica.append({
                    "fecha": datetime.now().isoformat(),
                    "tasa_anterior": self.tasa_del_dia,
                    "tasa_nueva": nueva_tasa,
                    "usuario": "usuario_actual"
                })

            # Actualizar tasa actual
            self.tasa_del_dia = nueva_tasa

            # Recalcular formulario automáticamente
            await self.recalcular_formulario_dual()

            logger.info(f"✅ Tasa actualizada: {nueva_tasa} BS/USD")
            return True

        except Exception as e:
            logger.error(f"❌ Error actualizando tasa: {str(e)}")
            return False

    @rx.event
    async def recalcular_formulario_dual(self):
        """🧮 RECALCULAR CONVERSIONES AUTOMÁTICAS EN FORMULARIO"""
        try:
            self.calculando_conversion = True

            # Si hay monto USD, calcular BS equivalente
            if hasattr(self.formulario_pago_dual, 'monto_total_usd') and self.formulario_pago_dual.monto_total_usd > 0:
                monto_bs_calculado = self.formulario_pago_dual.monto_total_usd * self.tasa_del_dia
                self.formulario_pago_dual.monto_total_bs = round(monto_bs_calculado, 2)

            # Recalcular saldos pendientes si aplica
            if hasattr(self.formulario_pago_dual, 'monto_pagado_usd'):
                saldo_usd = self.formulario_pago_dual.monto_total_usd - self.formulario_pago_dual.monto_pagado_usd
                self.formulario_pago_dual.saldo_pendiente_usd = max(0, saldo_usd)
                self.formulario_pago_dual.saldo_pendiente_bs = self.formulario_pago_dual.saldo_pendiente_usd * self.tasa_del_dia

        except Exception as e:
            logger.error(f"❌ Error recalculando formulario dual: {str(e)}")
        finally:
            self.calculando_conversion = False


    @rx.event
    async def alternar_calculadora_conversion(self):
        """🧮 MOSTRAR/OCULTAR CALCULADORA DE CONVERSIÓN"""
        self.calculadora_activa = not self.calculadora_activa
        if self.calculadora_activa:
            self.monto_calculadora_usd = "0"
            self.monto_calculadora_bs = "0"

    @rx.event
    async def calcular_conversion_usd_a_bs(self, monto_usd: str):
        """💱 CALCULAR CONVERSIÓN USD → BS"""
        try:
            if monto_usd and monto_usd.replace(".", "").isdigit():
                usd_valor = float(monto_usd)
                bs_calculado = usd_valor * self.tasa_del_dia
                self.monto_calculadora_usd = monto_usd
                self.monto_calculadora_bs = f"{bs_calculado:.2f}"
            else:
                self.monto_calculadora_bs = "0"

        except Exception as e:
            logger.error(f"❌ Error calculando conversión: {str(e)}")
            self.monto_calculadora_bs = "Error"

    @rx.event
    async def calcular_conversion_bs_a_usd(self, monto_bs: str):
        """💱 CALCULAR CONVERSIÓN BS → USD"""
        try:
            if monto_bs and monto_bs.replace(".", "").isdigit() and self.tasa_del_dia > 0:
                bs_valor = float(monto_bs)
                usd_calculado = bs_valor / self.tasa_del_dia
                self.monto_calculadora_bs = monto_bs
                self.monto_calculadora_usd = f"{usd_calculado:.2f}"
            else:
                self.monto_calculadora_usd = "0"

        except Exception as e:
            logger.error(f"❌ Error calculando conversión: {str(e)}")
            self.monto_calculadora_usd = "Error"


    @rx.event
    async def limpiar_calculadora(self):
        """🧹 LIMPIAR CALCULADORA DE CONVERSIÓN"""
        self.monto_calculadora_usd = "0"
        self.monto_calculadora_bs = "0"

    @rx.event
    async def cargar_estadisticas_duales(self):
        """📊 CARGAR ESTADÍSTICAS DEL SISTEMA DUAL USD/BS"""
        try:
            # Cargar datos de recaudación del día
            today = datetime.now().strftime("%Y-%m-%d")

            # ✅ ESTABLECER CONTEXTO DEL USUARIO ANTES DE USAR EL SERVICIO
            pagos_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Obtener estadísticas duales usando el servicio importado
            stats = await pagos_service.get_currency_stats()

            # Extraer datos del día
            hoy_stats = stats.get("hoy", {})
            self.recaudacion_usd_hoy = hoy_stats.get("total_recaudado_usd", 0.0)
            self.recaudacion_bs_hoy = hoy_stats.get("total_recaudado_bs", 0.0)

            # Extraer saldos pendientes
            pendientes_stats = stats.get("pendientes", {})
            self.pendiente_usd_total = pendientes_stats.get("monto_total_usd", 0.0)
            self.pendiente_bs_total = pendientes_stats.get("monto_total_bs", 0.0)

            # Extraer distribución de pagos
            distribucion = stats.get("distribucion_pagos", {})
            self.pagos_mixtos_count = distribucion.get("pagos_mixtos", 0)
            self.pagos_solo_usd_count = distribucion.get("pagos_solo_usd", 0)
            self.pagos_solo_bs_count = distribucion.get("pagos_solo_bs", 0)

            logger.info("📊 Estadísticas duales cargadas exitosamente")

        except Exception as e:
            logger.error(f"❌ Error cargando estadísticas duales: {str(e)}")
            # Valores por defecto en caso de error
            self.recaudacion_usd_hoy = 0.0
            self.recaudacion_bs_hoy = 0.0
            self.pendiente_usd_total = 0.0
            self.pendiente_bs_total = 0.0
            self.pagos_mixtos_count = 0
            self.pagos_solo_usd_count = 0
            self.pagos_solo_bs_count = 0



    # ==========================================
    # 💰 VALIDACIONES SISTEMA DUAL
    # ==========================================

    async def _validar_formulario_dual(self) -> Dict[str, str]:
        """✅ Validar formulario de pago dual"""
        errores = {}

        # Validaciones básicas
        if not self.formulario_pago_dual.paciente_id:
            errores["paciente_id"] = "Paciente es requerido"

        # Validar monto total en USD
        if self.formulario_pago_dual.monto_total_usd <= 0:
            errores["monto_total_usd"] = "Monto total en USD debe ser mayor a 0"

        # Validar tasa de cambio
        if self.tasa_del_dia <= 0:
            errores["tasa_cambio"] = "Tasa de cambio debe ser mayor a 0"

        # Validar que al menos hay un pago (USD o BS)
        pago_usd = self.formulario_pago_dual.monto_pagado_usd or 0
        pago_bs = self.formulario_pago_dual.monto_pagado_bs or 0

        if pago_usd <= 0 and pago_bs <= 0:
            errores["monto_pago"] = "Debe especificar al menos un monto de pago (USD o BS)"

        # Validar que el pago no exceda el total
        pago_usd_total = pago_usd + (pago_bs / self.tasa_del_dia if pago_bs > 0 else 0)
        if pago_usd_total > self.formulario_pago_dual.monto_total_usd:
            errores["monto_pago"] = "El pago total no puede exceder el monto adeudado"

        return errores

    # ==========================================
    # 🏥 MÉTODOS PARA CONSULTAS PENDIENTES DE PAGO
    # ==========================================
    
    @rx.event
    async def cargar_consultas_pendientes_pago(self):
        try:
            self.cargando_lista_pagos = True

            print(f"🔍 DEBUG: Cargando consultas pendientes de pago...")
         
            pagos_service.set_user_context(self.id_usuario, self.perfil_usuario)
            consultas_pendientes = await pagos_service.get_consultas_pendientes_pago()
            print(consultas_pendientes)
            if consultas_pendientes:
                # Actualizar lista interna para computed vars
                self.consultas_pendientes_pagar = consultas_pendientes
                
        except Exception as e:
            logger.error(f"❌ Error cargando consultas pendientes: {str(e)}")
            self.consultas_pendientes_pagar = []
            print(f"❌ Error cargando consultas pendientes: {str(e)}")
        finally:
            self.cargando_lista_pagos = False
            

    @rx.event
    async def seleccionar_consulta_para_pago(self, pago_id: str):
        """🎯 Seleccionar consulta para procesar pago y abrir modal"""
        print(pago_id)
        print(self.consultas_pendientes_pagar)
        try:
           
            # Buscar la consulta en la lista pendiente enriquecida (tipada)
            consulta_encontrada = next(
                (c for c in self.consultas_pendientes_pagar if c.pago_id == pago_id),
                None
            )
            self.consulta_pagar =  consulta_encontrada
            print(f"🔍 consulta_pagar seteada: {self.consulta_pagar}")
            if consulta_encontrada:
                # Pre-llenar formulario dual con datos de la consulta
                self.formulario_pago_dual.pago_id = consulta_encontrada.pago_id  # ✅ LO MÁS IMPORTANTE
                self.formulario_pago_dual.consulta_id = consulta_encontrada.consulta_id
                self.formulario_pago_dual.paciente_id = consulta_encontrada.paciente_id
                self.formulario_pago_dual.paciente_nombre = consulta_encontrada.paciente_nombre
                self.formulario_pago_dual.numero_consulta = consulta_encontrada.numero_consulta
                self.formulario_pago_dual.monto_total_usd = consulta_encontrada.total_usd
                self.formulario_pago_dual.monto_total_bs = consulta_encontrada.total_bs
                self.formulario_pago_dual.concepto = consulta_encontrada.concepto
                self.formulario_pago_dual.tasa_cambio = self.tasa_del_dia

                # ✨ GUARDAR DATOS ADICIONALES en variables simples del estado
                self.consulta_actual_numero_historia = consulta_encontrada.paciente_numero_historia or "Sin HC"
                self.consulta_actual_documento = consulta_encontrada.paciente_documento or "Sin documento"
                self.consulta_actual_telefono = consulta_encontrada.paciente_telefono or "Sin teléfono"

                # Calcular conversión con tasa actual
                await self.recalcular_formulario_dual()

                # ✅ Abrir modal de pago dual
                self.modal_pago_dual_abierto = True

                logger.info(f"✅ Consulta seleccionada para pago: {consulta_encontrada.numero_consulta}")
            else:
                logger.warning(f"⚠️ Consulta no encontrada: {pago_id}")
                # Mostrar mensaje de error al usuario
                self.errores_validacion_pago["general"] = "Consulta no encontrada"

        except Exception as e:
            logger.error(f"❌ Error seleccionando consulta: {str(e)}")
            self.errores_validacion_pago["general"] = f"Error: {str(e)}"

    
    # ==========================================
    # 🏥 COMPUTED VARS PARA CONSULTAS PENDIENTES
    # ==========================================

    @rx.var(cache=True)
    def total_consultas_pendientes_pago(self) -> int:
        """📊 Total de consultas pendientes de pago"""
        return len(getattr(self, 'consultas_pendientes_facturacion', []))


    @rx.var(cache=True)
    def consultas_por_odontologo(self) -> Dict[str, List[Dict[str, Any]]]:
        """👨‍⚕️ Consultas pendientes agrupadas por odontólogo"""
        consultas = getattr(self, 'consultas_pendientes_facturacion', [])
        agrupadas = {}

        for consulta in consultas:
            odontologo = consulta.get("odontologo_nombre", "Sin asignar")
            if odontologo not in agrupadas:
                agrupadas[odontologo] = []
            agrupadas[odontologo].append(consulta)

        return agrupadas


    # Variable de estado para almacenar ID de consulta seleccionada para accordion
    consulta_id_seleccionada_accordion: str = ""


    @rx.var(cache=True)
    def servicios_factura_seleccionada(self) -> List[ServicioFormateado]:
        """🧾 Lista de servicios de la consulta seleccionada para la factura"""
        if self.formulario_pago_dual.consulta_id:
            consulta = next(
                (c for c in self.consultas_pendientes_pagar if c.pago_id == self.formulario_pago_dual.pago_id),
                None
            )
            return consulta.servicios_formateados if consulta else []
        return []

    @rx.var(cache=True)
    def pagos_historial_formateados(self) -> List[Dict[str, Any]]:
        """📋 Pagos formateados con info adicional para tabla de historial"""
        resultado = []
        for pago in self.lista_pagos:
            # Convertir PagoModel a dict y formatear
            pago_dict = {
                "id": pago.id,
                "numero_recibo": pago.numero_recibo,
                "monto_pagado_usd": getattr(pago, 'monto_pagado_usd', 0.0),
                "monto_pagado_bs": getattr(pago, 'monto_pagado_bs', 0.0),
                "estado_pago": pago.estado_pago,
                "fecha_pago": pago.fecha_pago.isoformat() if hasattr(pago.fecha_pago, 'isoformat') else str(pago.fecha_pago),
                # Campos que pueden faltar - usar valores por defecto
                "paciente_nombre": getattr(pago, 'paciente_nombre', 'N/A'),
                "paciente_documento": getattr(pago, 'paciente_documento', 'N/A'),
            }
            resultado.append(pago_dict)
        return resultado

    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.lista_pagos = []
        self.total_pagos = 0
        self.errores_validacion_pago = {}
        self.cargando_lista_pagos = False

        # Limpiar filtros
        self.termino_busqueda_pagos = ""
        self.buscar_por_paciente = ""
        self.buscar_por_numero_recibo = ""
        self.filtro_metodo_pago = "todos"
        self.filtro_estado_pago = "todos"
        self.filtro_fecha_pagos = date.today().isoformat()
        self.filtro_rango_monto = {"min": 0.0, "max": 999999.0}
        self.rango_fecha_inicio = ""
        self.rango_fecha_fin = ""

        # Limpiar métricas
        self.recaudacion_hoy = 0.0
        self.recaudacion_mes = 0.0
        self.saldo_pendiente_total = 0.0
        self.total_facturas_pendientes = 0

        # 💰 LIMPIAR VARIABLES SISTEMA DUAL
        self.formulario_pago_dual = PagoFormModel()
        self.tasa_del_dia = 36.50
        self.tasa_sugerida = 36.50
        self.tasa_historica = []
        self.estadisticas_dual = {}
        self.recaudacion_usd_hoy = 0.0
        self.recaudacion_bs_hoy = 0.0
        self.pendiente_usd_total = 0.0
        self.pendiente_bs_total = 0.0
        self.calculadora_activa = False
        self.monto_calculadora_usd = "0"
        self.monto_calculadora_bs = "0"
        self.calculando_conversion = False
        self.pagos_mixtos_count = 0
        self.pagos_solo_usd_count = 0
        self.pagos_solo_bs_count = 0
        self.preferencia_moneda_del_dia = "USD"
        self.vista_dual_activa = True
        self.moneda_principal_vista = "USD"
        self.mostrar_conversion_automatica = True

        # 🏥 LIMPIAR CONSULTAS PENDIENTES
        self.consultas_pendientes_facturacion = []
        self.consulta_seleccionada_pago = None
        self.cargando_consultas_pendientes = False

        # Limpiar cache
        self.cache_pagos_recientes = []
        self.cache_cuentas_por_cobrar = []
        self.cache_timestamp_pagos = ""

        # Estados de carga
        self.cargando_estadisticas_pagos = False
        self.cargando_operacion_pago = False
        self.procesando_pago = False

    @rx.event
    def cancelar_formulario_pago(self):
        """🚫 Cancelar formulario de pago y limpiar datos"""
        self.formulario_pago_dual = PagoFormModel()
        self.consulta_seleccionada_pago = None

        logger.info("🧹 Datos de pagos limpiados (incluye sistema dual)")
        
        
    async def cargar_datos_pagos_page(self):
        """Carga todos los datos necesarios al entrar a la página de pagos"""
        await self.cargar_consultas_pendientes_pago()
        await self.cargar_lista_pagos(force_refresh=True)
        await self.cargar_estadisticas_duales()
        
    @rx.event
    async def recargar_todo_pagos(self):
        """🔄 RECARGAR TODA LA PÁGINA DE PAGOS (consultas pendientes, lista de pagos y  estadísticas)"""
        try:
           logger.info("🔄 Recargando toda la página de pagos...")

           # Cargar todo en paralelo
           await self.cargar_consultas_pendientes_pago()
           await self.cargar_lista_pagos(force_refresh=True)
           await self.cargar_estadisticas_duales()

           logger.info("✅ Página de pagos recargada completamente")
        except Exception as e:
           logger.error(f"❌ Error recargando página de pagos: {str(e)}")

