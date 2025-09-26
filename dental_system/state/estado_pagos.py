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
from dental_system.models import (
    PagoModel,
    PagosStatsModel,
    FacturaModel,
    ConceptoPagoModel,
    BalanceGeneralModel,
    CuentaPorCobrarModel,
    PagoFormModel,
    PagoParcialFormModel
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
    
    # Pago seleccionado para operaciones
    pago_seleccionado: PagoModel = PagoModel()
    id_pago_seleccionado: str = ""
    
    # Formularios de pagos (datos temporales)
    formulario_pago: Dict[str, Any] = {}
    formulario_pago_data: PagoFormModel = PagoFormModel()
    formulario_pago_parcial_data: PagoParcialFormModel = PagoParcialFormModel()
    errores_validacion_pago: Dict[str, str] = {}

    # Variables auxiliares para operaciones
    pago_para_eliminar: Optional[PagoModel] = None
    cargando_lista_pagos: bool = False
    mostrar_solo_pendientes: bool = False

    # ==========================================
    # 💰 NUEVAS VARIABLES SISTEMA DUAL USD/BS
    # ==========================================

    # 📊 FORMULARIO DUAL SIMPLIFICADO
    formulario_pago_dual: PagoFormModel = PagoFormModel()

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
    
    # ==========================================
    # 💳 MÉTODOS DE PAGO Y CONFIGURACIÓN
    # ==========================================
    
    # Métodos de pago disponibles
    metodos_pago_disponibles: List[str] = [
        "efectivo",
        "tarjeta_credito", 
        "tarjeta_debito",
        "transferencia_bancaria",
        "cheque",
        "pago_movil",
        "otros"
    ]
    
    # Estados de pago
    estados_pago_disponibles: List[str] = [
        "pendiente",
        "completado", 
        "anulado",
        "reembolsado"
    ]
    
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
    def pagos_filtrados_display(self) -> List[PagoModel]:
        """🔍 Pagos filtrados según criterios actuales"""
        pagos = self.lista_pagos
        
        # Filtrar por búsqueda
        if self.termino_busqueda_pagos:
            pagos = [
                p for p in pagos 
                if (self.termino_busqueda_pagos.lower() in p.numero_recibo.lower() or
                    self.termino_busqueda_pagos.lower() in p.concepto.lower())
            ]
        
        # Filtrar por método de pago
        if self.filtro_metodo_pago != "todos":
            pagos = [p for p in pagos if p.metodo_pago == self.filtro_metodo_pago]
        
        # Filtrar por estado
        if self.filtro_estado_pago != "todos":
            pagos = [p for p in pagos if p.estado_pago == self.filtro_estado_pago]
        
        # Filtrar por solo pendientes
        if self.mostrar_solo_pendientes:
            pagos = [p for p in pagos if p.estado_pago == "pendiente"]
        
        # Filtrar por rango de monto
        monto_min = self.filtro_rango_monto.get("min", 0.0)
        monto_max = self.filtro_rango_monto.get("max", 999999.0)
        pagos = [
            p for p in pagos 
            if monto_min <= p.monto_total <= monto_max
        ]
        
        return pagos
    
    @rx.var(cache=True)
    def pagos_pendientes(self) -> List[PagoModel]:
        """⏳ Pagos pendientes"""
        return [p for p in self.lista_pagos if p.estado_pago == "pendiente"]
    
    @rx.var(cache=True)
    def pagos_completados_hoy(self) -> List[PagoModel]:
        """✅ Pagos completados hoy"""
        hoy = date.today()
        return [
            p for p in self.lista_pagos 
            if p.estado_pago == "completado" and p.fecha_pago.date() == hoy
        ]
    
    @rx.var(cache=True)
    def pagos_con_saldo_pendiente(self) -> List[PagoModel]:
        """💰 Pagos con saldo pendiente"""
        return [p for p in self.lista_pagos if p.saldo_pendiente > 0]
    
    @rx.var(cache=True)
    def total_pagos_pendientes(self) -> int:
        """📊 Total de pagos pendientes"""
        return len(self.pagos_pendientes)
    
    @rx.var(cache=True)
    def total_saldo_pendiente(self) -> float:
        """💰 Total saldo pendiente"""
        return sum(p.saldo_pendiente for p in self.lista_pagos)
    
    @rx.var(cache=True)
    def recaudacion_del_dia(self) -> float:
        """💵 Recaudación del día"""
        hoy = date.today()
        return sum(
            p.monto_pagado for p in self.lista_pagos 
            if p.fecha_pago.date() == hoy and p.estado_pago == "completado"
        )
    
    @rx.var(cache=True)
    def pago_seleccionado_valido(self) -> bool:
        """✅ Validar si hay pago seleccionado"""
        return (
            hasattr(self.pago_seleccionado, 'id') and 
            bool(self.pago_seleccionado.id)
        )
    
    @rx.var(cache=True)
    def proximo_numero_recibo(self) -> str:
        """🔢 Próximo número de recibo disponible"""
        # Generar formato: REC2024120001
        hoy = date.today()
        año = hoy.year
        mes = hoy.month
        
        # Contar recibos del mes actual
        recibos_mes = len([
            p for p in self.lista_pagos 
            if p.fecha_pago.month == mes and p.fecha_pago.year == año
        ])
        
        return f"REC{año}{mes:02d}{(recibos_mes + 1):04d}"
    
    # ==========================================
    # 💳 MÉTODOS PRINCIPALES DE CRUD
    # ==========================================
    
    @rx.event
    async def cargar_lista_pagos(self, force_refresh: bool = False):
        """💳 CARGAR LISTA COMPLETA DE PAGOS"""
        try:
            self.cargando_lista_pagos = True
            
            # Cargar desde el servicio
            pagos_data = await pagos_service.get_all_payments()
            
            # Convertir a modelos tipados
            self.lista_pagos = [
                PagoModel.from_dict(pago) 
                for pago in pagos_data
            ]
            self.total_pagos = len(self.lista_pagos)
            
            # Actualizar métricas rápidas
            await self._actualizar_metricas_rapidas()
            
            logger.info(f"✅ {len(self.lista_pagos)} pagos cargados")
            
        except Exception as e:
            logger.error(f"❌ Error cargando pagos: {str(e)}")
        finally:
            self.cargando_lista_pagos = False
    
    @rx.event
    async def crear_pago(self, form_data: Dict[str, Any]):
        """➕ CREAR NUEVO PAGO"""
        try:
            self.procesando_pago = True
            self.errores_validacion_pago = {}
            
            # Validar datos del formulario
            errores = await self._validar_formulario_pago(form_data)
            if errores:
                self.errores_validacion_pago = errores
                return False
            
            # Procesar pago a través del servicio
            pago_creado = await pagos_service.create_payment(form_data)
            
            if pago_creado:
                # Agregar a la lista local
                nuevo_pago = PagoModel.from_dict(pago_creado)
                self.lista_pagos.append(nuevo_pago)
                self.total_pagos += 1
                
                # Actualizar métricas
                await self._actualizar_metricas_rapidas()
                
                # Limpiar formulario
                self.formulario_pago = {}
                self.formulario_pago_data = PagoFormModel()
                
                logger.info(f"✅ Pago creado: {nuevo_pago.numero_recibo}")
                return True
            
            return False
            
        except Exception as e:
            error_msg = f"Error creando pago: {str(e)}"
            self.errores_validacion_pago["general"] = error_msg
            logger.error(error_msg)
            return False
        finally:
            self.procesando_pago = False
    
    @rx.event
    async def procesar_pago_parcial(self, pago_id: str, monto_pago: float):
        """💰 PROCESAR PAGO PARCIAL"""
        try:
            self.procesando_pago = True
            
            # Procesar a través del servicio
            resultado = await pagos_service.process_partial_payment(pago_id, monto_pago)
            
            if resultado:
                # Actualizar en la lista local
                for i, pago in enumerate(self.lista_pagos):
                    if pago.id == pago_id:
                        pago_actualizado = PagoModel.from_dict(resultado)
                        self.lista_pagos[i] = pago_actualizado
                        
                        # Si es el seleccionado, actualizarlo
                        if self.pago_seleccionado.id == pago_id:
                            self.pago_seleccionado = pago_actualizado
                        break
                
                # Actualizar métricas
                await self._actualizar_metricas_rapidas()
                
                logger.info(f"✅ Pago parcial procesado: ${monto_pago}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error procesando pago parcial: {str(e)}")
            return False
        finally:
            self.procesando_pago = False
    
    @rx.event
    async def anular_pago(self, pago_id: str, motivo: str):
        """❌ ANULAR PAGO"""
        try:
            self.procesando_pago = True
            
            # Anular a través del servicio
            resultado = await pagos_service.void_payment(pago_id, motivo)
            
            if resultado:
                # Actualizar en la lista local
                for i, pago in enumerate(self.lista_pagos):
                    if pago.id == pago_id:
                        pago_anulado = PagoModel.from_dict(resultado)
                        self.lista_pagos[i] = pago_anulado
                        break
                
                # Actualizar métricas
                await self._actualizar_metricas_rapidas()
                
                logger.info(f"✅ Pago anulado: {pago_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error anulando pago: {str(e)}")
            return False
        finally:
            self.procesando_pago = False
    
    @rx.event
    async def buscar_pagos(self, query: str):
        """🔍 BUSCAR PAGOS"""
        self.termino_busqueda_pagos = query.strip()
        logger.info(f"🔍 Búsqueda de pagos: '{query}'")
    
    @rx.event
    async def seleccionar_pago(self, pago_id: str):
        """🎯 SELECCIONAR PAGO"""
        try:
            pago_encontrado = next(
                (p for p in self.lista_pagos if p.id == pago_id),
                None
            )
            
            if pago_encontrado:
                self.pago_seleccionado = pago_encontrado
                self.id_pago_seleccionado = pago_id
                logger.info(f"✅ Pago seleccionado: {pago_encontrado.numero_recibo}")
            else:
                self.pago_seleccionado = PagoModel()
                self.id_pago_seleccionado = ""
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando pago: {str(e)}")
    
    @rx.event
    async def aplicar_filtros_pagos(self, filtros: Dict[str, Any]):
        """🔍 APLICAR FILTROS DE PAGOS - COORDINACIÓN CON APPSTATE"""
        try:
            # Aplicar filtros individuales
            if "metodo_pago" in filtros:
                self.filtro_metodo_pago = filtros["metodo_pago"]
            
            if "estado_pago" in filtros:
                self.filtro_estado_pago = filtros["estado_pago"]
            
            if "mostrar_solo_pendientes" in filtros:
                self.mostrar_solo_pendientes = filtros["mostrar_solo_pendientes"]
            
            if "rango_monto" in filtros:
                self.filtro_rango_monto = filtros["rango_monto"]
            
            if "fecha_inicio" in filtros:
                self.rango_fecha_inicio = filtros["fecha_inicio"]
                
            if "fecha_fin" in filtros:
                self.rango_fecha_fin = filtros["fecha_fin"]
            
            logger.info(f"✅ Filtros de pagos aplicados: {filtros}")
            
        except Exception as e:
            logger.error(f"❌ Error aplicando filtros pagos: {str(e)}")
    
    # ==========================================
    # 💳 MÉTODOS AUXILIARES Y ESTADÍSTICAS
    # ==========================================
    
    async def _actualizar_metricas_rapidas(self):
        """📊 ACTUALIZAR MÉTRICAS RÁPIDAS"""
        try:
            self.recaudacion_hoy = self.recaudacion_del_dia
            
            # Calcular recaudación del mes
            hoy = date.today()
            primer_dia_mes = date(hoy.year, hoy.month, 1)
            self.recaudacion_mes = sum(
                p.monto_pagado for p in self.lista_pagos
                if p.fecha_pago >= primer_dia_mes and p.estado_pago == "completado"
            )
            
            # Actualizar saldos pendientes
            self.saldo_pendiente_total = self.total_saldo_pendiente
            self.total_facturas_pendientes = self.total_pagos_pendientes
            
        except Exception as e:
            logger.error(f"❌ Error actualizando métricas rápidas: {str(e)}")
    
    async def _validar_formulario_pago(self, datos: Dict[str, Any]) -> Dict[str, str]:
        """✅ Validar datos del formulario de pago"""
        errores = {}
        
        # Validaciones básicas
        if not datos.get("paciente_id", "").strip():
            errores["paciente_id"] = "Paciente es requerido"
        
        if not datos.get("concepto", "").strip():
            errores["concepto"] = "Concepto es requerido"
        
        # Validar montos
        try:
            monto_total = float(datos.get("monto_total", 0))
            if monto_total <= 0:
                errores["monto_total"] = "Monto debe ser mayor a 0"
        except:
            errores["monto_total"] = "Monto inválido"
        
        # Validar método de pago
        metodo = datos.get("metodo_pago", "")
        if metodo not in self.metodos_pago_disponibles:
            errores["metodo_pago"] = "Método de pago inválido"
        
        return errores
    
    # ==========================================
    # 💰 MÉTODOS SISTEMA DUAL USD/BS
    # ==========================================

    @rx.event
    async def crear_pago_dual(self):
        """💰 CREAR PAGO CON SISTEMA DUAL USD/BS"""
        try:
            self.procesando_pago = True
            self.errores_validacion_pago = {}

            # Validar formulario dual
            errores = await self._validar_formulario_dual()
            if errores:
                self.errores_validacion_pago = errores
                return False

            # Preparar datos para el servicio
            form_data = {
                "paciente_id": self.formulario_pago_dual.paciente_id,
                "monto_total_usd": self.formulario_pago_dual.monto_total_usd,
                "monto_pagado_usd": self.formulario_pago_dual.monto_pagado_usd,
                "monto_pagado_bs": self.formulario_pago_dual.monto_pagado_bs,
                "tasa_cambio_del_dia": self.tasa_del_dia,
                "concepto": self.formulario_pago_dual.concepto,
                "metodos_pago": self.formulario_pago_dual.metodos_pago
            }

            # Crear pago a través del servicio dual
            pago_creado = await pagos_service.create_dual_payment(form_data, "usuario_actual")

            if pago_creado:
                # Agregar a lista local
                nuevo_pago = PagoModel.from_dict(pago_creado)
                self.lista_pagos.append(nuevo_pago)
                self.total_pagos += 1

                # Actualizar estadísticas duales
                await self.cargar_estadisticas_duales()

                # Limpiar formulario
                self.formulario_pago_dual = PagoFormModel()
                self.errores_validacion_pago = {}

                logger.info(f"✅ Pago dual creado: {nuevo_pago.numero_recibo}")
                return True

            return False

        except Exception as e:
            error_msg = f"Error creando pago dual: {str(e)}"
            self.errores_validacion_pago["general"] = error_msg
            logger.error(error_msg)
            return False
        finally:
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
    async def cargar_estadisticas_duales(self):
        """📊 CARGAR ESTADÍSTICAS DUALES USD/BS"""
        try:
            # Obtener estadísticas del servicio
            stats = await pagos_service.get_currency_stats()

            if stats:
                self.estadisticas_dual = stats
                self.recaudacion_usd_hoy = stats.get("recaudacion_usd_hoy", 0.0)
                self.recaudacion_bs_hoy = stats.get("recaudacion_bs_hoy", 0.0)
                self.pendiente_usd_total = stats.get("pendiente_usd_total", 0.0)
                self.pendiente_bs_total = stats.get("pendiente_bs_total", 0.0)
                self.pagos_mixtos_count = stats.get("pagos_mixtos_count", 0)
                self.pagos_solo_usd_count = stats.get("pagos_solo_usd_count", 0)
                self.pagos_solo_bs_count = stats.get("pagos_solo_bs_count", 0)

                logger.info(f"✅ Estadísticas duales actualizadas")

        except Exception as e:
            logger.error(f"❌ Error cargando estadísticas duales: {str(e)}")

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
    async def alternar_vista_dual(self):
        """🎨 ALTERNAR VISTA DUAL/SIMPLIFICADA"""
        self.vista_dual_activa = not self.vista_dual_activa
        if not self.vista_dual_activa:
            self.moneda_principal_vista = "USD" if self.preferencia_moneda_del_dia == "USD" else "BS"

    @rx.event
    async def cambiar_moneda_principal(self, moneda: str):
        """💰 CAMBIAR MONEDA PRINCIPAL DE VISTA"""
        if moneda in ["USD", "BS"]:
            self.moneda_principal_vista = moneda
            self.preferencia_moneda_del_dia = moneda

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
    # 💰 COMPUTED VARS SISTEMA DUAL
    # ==========================================

    @rx.var(cache=True)
    def monto_total_bs_calculado(self) -> float:
        """💱 Monto total calculado en BS automáticamente"""
        try:
            usd_value = float(self.formulario_pago_dual.monto_total_usd or "0")
            tasa = float(self.formulario_pago_dual.tasa_cambio_del_dia or "36.50")
            return usd_value * tasa
        except (ValueError, AttributeError):
            return 0.0

    @rx.var(cache=True)
    def saldo_pendiente_usd_calculado(self) -> float:
        """💰 Saldo pendiente en USD después del pago"""
        try:
            monto_total = float(self.formulario_pago_dual.monto_total_usd or "0")
            pago_usd = float(self.formulario_pago_dual.pago_usd or "0")
            pago_bs = float(self.formulario_pago_dual.pago_bs or "0")
            tasa = float(self.formulario_pago_dual.tasa_cambio_del_dia or "36.50")

            # Convertir pago en BS a USD
            pago_bs_en_usd = pago_bs / tasa if tasa > 0 else 0
            total_pagado_usd = pago_usd + pago_bs_en_usd

            saldo = monto_total - total_pagado_usd
            return max(0, saldo)  # No puede ser negativo
        except (ValueError, AttributeError):
            return 0.0

    @rx.var(cache=True)
    def saldo_pendiente_bs_calculado(self) -> float:
        """💱 Saldo pendiente en BS después del pago"""
        try:
            saldo_usd = self.saldo_pendiente_usd_calculado
            tasa = float(self.formulario_pago_dual.tasa_cambio_del_dia or "36.50")
            return saldo_usd * tasa
        except (ValueError, AttributeError):
            return 0.0

    @rx.var(cache=True)
    def total_recaudado_dual_hoy(self) -> Dict[str, float]:
        """💰 Total recaudado hoy en ambas monedas"""
        hoy = date.today()
        usd_total = 0.0
        bs_total = 0.0

        for pago in self.lista_pagos:
            if pago.fecha_pago.date() == hoy and pago.estado_pago == "completado":
                usd_total += getattr(pago, 'monto_pagado_usd', 0.0)
                bs_total += getattr(pago, 'monto_pagado_bs', 0.0)

        return {
            "usd": usd_total,
            "bs": bs_total,
            "tasa_promedio": bs_total / usd_total if usd_total > 0 else self.tasa_del_dia
        }

    @rx.var(cache=True)
    def pendientes_dual_totales(self) -> Dict[str, float]:
        """⏳ Saldos pendientes en ambas monedas"""
        usd_pendiente = 0.0
        bs_pendiente = 0.0

        for pago in self.lista_pagos:
            if pago.estado_pago == "pendiente":
                usd_pendiente += getattr(pago, 'saldo_pendiente_usd', 0.0)
                bs_pendiente += getattr(pago, 'saldo_pendiente_bs', 0.0)

        return {
            "usd": usd_pendiente,
            "bs": bs_pendiente,
            "total_facturas": len([p for p in self.lista_pagos if p.estado_pago == "pendiente"])
        }

    @rx.var(cache=True)
    def distribucion_metodos_pago_dual(self) -> Dict[str, Dict[str, float]]:
        """📊 Distribución de métodos de pago por moneda"""
        distribucion = {}

        for pago in self.lista_pagos:
            if hasattr(pago, 'metodos_pago') and pago.metodos_pago:
                for metodo_info in pago.metodos_pago:
                    metodo = metodo_info.get('metodo', 'otros')
                    if metodo not in distribucion:
                        distribucion[metodo] = {"usd": 0.0, "bs": 0.0, "count": 0}

                    distribucion[metodo]["usd"] += metodo_info.get('monto_usd', 0.0)
                    distribucion[metodo]["bs"] += metodo_info.get('monto_bs', 0.0)
                    distribucion[metodo]["count"] += 1

        return distribucion

    @rx.var(cache=True)
    def conversion_automatica_activa(self) -> bool:
        """🔄 Si la conversión automática está habilitada"""
        return self.mostrar_conversion_automatica and self.tasa_del_dia > 0

    # ==========================================
    # 💰 VALIDACIONES SISTEMA DUAL
    # ==========================================

    async def _validar_formulario_dual(self) -> Dict[str, str]:
        """✅ Validar formulario de pago dual"""
        errores = {}

        # Validaciones básicas
        if not self.formulario_pago_dual.paciente_id:
            errores["paciente_id"] = "Paciente es requerido"

        if not self.formulario_pago_dual.concepto.strip():
            errores["concepto"] = "Concepto es requerido"

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
        """🏥 Cargar consultas completadas pendientes de facturación"""
        try:
            self.cargando_lista_pagos = True

            # ✅ ESTABLECER CONTEXTO DEL USUARIO ANTES DE USAR EL SERVICIO
            pagos_service.set_user_context(self.id_usuario, self.perfil_usuario)

            # Obtener consultas completadas con pagos pendientes
            consultas_pendientes = await pagos_service.get_consultas_pendientes_pago()

            if consultas_pendientes:
                # Actualizar lista interna para computed vars
                self.consultas_pendientes_facturacion = consultas_pendientes
                logger.info(f"✅ {len(consultas_pendientes)} consultas pendientes de pago cargadas")
            else:
                self.consultas_pendientes_facturacion = []
                logger.info("📭 No hay consultas pendientes de pago")

        except Exception as e:
            logger.error(f"❌ Error cargando consultas pendientes: {str(e)}")
            self.consultas_pendientes_facturacion = []
        finally:
            self.cargando_lista_pagos = False

    @rx.event
    async def seleccionar_consulta_para_pago(self, consulta_id: str):
        """🎯 Seleccionar consulta para procesar pago"""
        try:
            # Buscar la consulta en la lista pendiente
            consulta_encontrada = next(
                (c for c in self.consultas_pendientes_facturacion if c.get("consulta_id") == consulta_id),
                None
            )

            if consulta_encontrada:
                # Pre-llenar formulario dual con datos de la consulta
                self.formulario_pago_dual.consulta_id = consulta_id
                self.formulario_pago_dual.paciente_id = consulta_encontrada.get("paciente_id", "")
                self.formulario_pago_dual.monto_total_usd = float(consulta_encontrada.get("total_usd", 0.0))
                self.formulario_pago_dual.monto_total_bs = float(consulta_encontrada.get("total_bs", 0.0))
                self.formulario_pago_dual.concepto = consulta_encontrada.get("concepto", f"Consulta {consulta_encontrada.get('numero_consulta', '')}")

                # Calcular conversión con tasa actual
                await self.recalcular_formulario_dual()

                logger.info(f"✅ Consulta seleccionada para pago: {consulta_encontrada.get('numero_consulta')}")
                return True
            else:
                logger.warning(f"⚠️ Consulta no encontrada: {consulta_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Error seleccionando consulta: {str(e)}")
            return False

    @rx.event
    async def procesar_pago_consulta(self):
        """💳 Procesar pago de consulta seleccionada"""
        try:
            self.procesando_pago = True

            # Validar que hay una consulta seleccionada
            if not hasattr(self.formulario_pago_dual, 'consulta_id') or not self.formulario_pago_dual.consulta_id:
                self.errores_validacion_pago["general"] = "No hay consulta seleccionada"
                return False

            # Usar el método dual existente
            resultado = await self.crear_pago_dual()

            if resultado:
                # Remover consulta de la lista de pendientes
                self.consultas_pendientes_facturacion = [
                    c for c in self.consultas_pendientes_facturacion
                    if c.get("consulta_id") != self.formulario_pago_dual.consulta_id
                ]

                # Limpiar formulario
                self.formulario_pago_dual = PagoFormModel()

                logger.info("✅ Pago de consulta procesado exitosamente")
                return True

            return False

        except Exception as e:
            error_msg = f"Error procesando pago de consulta: {str(e)}"
            self.errores_validacion_pago["general"] = error_msg
            logger.error(error_msg)
            return False
        finally:
            self.procesando_pago = False

    # ==========================================
    # 🏥 COMPUTED VARS PARA CONSULTAS PENDIENTES
    # ==========================================

    @rx.var(cache=True)
    def total_consultas_pendientes_pago(self) -> int:
        """📊 Total de consultas pendientes de pago"""
        return len(getattr(self, 'consultas_pendientes_facturacion', []))

    @rx.var(cache=True)
    def valor_total_pendiente_consultas(self) -> Dict[str, float]:
        """💰 Valor total pendiente de todas las consultas"""
        consultas = getattr(self, 'consultas_pendientes_facturacion', [])

        total_usd = sum(float(c.get("total_usd", 0)) for c in consultas)
        total_bs = sum(float(c.get("total_bs", 0)) for c in consultas)

        return {
            "usd": total_usd,
            "bs": total_bs,
            "count": len(consultas)
        }

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

    def limpiar_datos(self):
        """🧹 LIMPIAR TODOS LOS DATOS - USADO EN LOGOUT"""
        self.lista_pagos = []
        self.total_pagos = 0
        self.pago_seleccionado = PagoModel()
        self.id_pago_seleccionado = ""
        self.formulario_pago = {}
        self.formulario_pago_data = PagoFormModel()
        self.formulario_pago_parcial_data = PagoParcialFormModel()
        self.errores_validacion_pago = {}
        self.pago_para_eliminar = None
        self.cargando_lista_pagos = False
        self.mostrar_solo_pendientes = False

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