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
        
        # Limpiar cache
        self.cache_pagos_recientes = []
        self.cache_cuentas_por_cobrar = []
        self.cache_timestamp_pagos = ""
        
        # Estados de carga
        self.cargando_estadisticas_pagos = False
        self.cargando_operacion_pago = False
        self.procesando_pago = False
        
        logger.info("🧹 Datos de pagos limpiados")