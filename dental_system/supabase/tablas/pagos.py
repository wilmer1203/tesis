"""
Operaciones CRUD para la tabla pagos
"""
from typing import Dict, List, Optional, Any
from datetime import date, datetime
from decimal import Decimal
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class PaymentsTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla pagos
    """
    
    def __init__(self):
        super().__init__('pagos')
    
    @handle_supabase_error
    def create_payment(self,
                      paciente_id: str,
                      monto_total: Decimal,
                      monto_pagado: Decimal,
                      concepto: str,
                      procesado_por: str,
                      consulta_id: Optional[str] = None,
                      metodo_pago: str = 'efectivo',
                      referencia_pago: Optional[str] = None,
                      descuento_aplicado: Decimal = Decimal('0'),
                      motivo_descuento: Optional[str] = None,
                      impuestos: Decimal = Decimal('0'),
                      autorizado_por: Optional[str] = None,
                      observaciones: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea un nuevo pago
        
        Args:
            paciente_id: ID del paciente
            monto_total: Monto total a pagar
            monto_pagado: Monto pagado
            concepto: Concepto del pago
            procesado_por: ID del usuario que procesa el pago
            consulta_id: ID de la consulta relacionada (opcional)
            metodo_pago: Método de pago (efectivo, tarjeta_credito, etc.)
            referencia_pago: Referencia del pago (número de transacción, etc.)
            descuento_aplicado: Descuento aplicado
            motivo_descuento: Motivo del descuento
            impuestos: Impuestos aplicados
            autorizado_por: ID del usuario que autoriza (para descuentos)
            observaciones: Observaciones adicionales
            
        Returns:
            Pago creado con número de recibo generado
        """
        # Calcular saldo pendiente
        saldo_pendiente = float(monto_total) - float(monto_pagado)
        
        data = {
            "paciente_id": paciente_id,
            "monto_total": float(monto_total),
            "monto_pagado": float(monto_pagado),
            "saldo_pendiente": saldo_pendiente,
            "concepto": concepto,
            "procesado_por": procesado_por,
            "metodo_pago": metodo_pago,
            "descuento_aplicado": float(descuento_aplicado),
            "impuestos": float(impuestos),
            "estado_pago": "completado" if saldo_pendiente <= 0 else "pendiente"
        }
        
        # Agregar campos opcionales
        if consulta_id:
            data["consulta_id"] = consulta_id
        if referencia_pago:
            data["referencia_pago"] = referencia_pago
        if motivo_descuento and descuento_aplicado > 0:
            data["motivo_descuento"] = motivo_descuento
        if autorizado_por:
            data["autorizado_por"] = autorizado_por
        if observaciones:
            data["observaciones"] = observaciones
        
        logger.info(f"Creando pago para paciente {paciente_id}: ${monto_pagado}")
        return self.create(data)
    
    @handle_supabase_error
    def get_by_recibo(self, numero_recibo: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un pago por su número de recibo
        
        Args:
            numero_recibo: Número de recibo (formato RECYYYYMM####)
            
        Returns:
            Pago encontrado o None
        """
        response = self.table.select("*").eq("numero_recibo", numero_recibo).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_payment_details(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un pago con información completa
        
        Args:
            payment_id: ID del pago
            
        Returns:
            Pago con información expandida
        """
        response = self.table.select("""
            *,
            pacientes!inner(
                id, numero_historia, nombre_completo, 
                numero_documento
            ),
            consultas(
                numero_consulta, fecha_programada,
                personal!odontologo_id(
                    usuario:usuarios!inner(nombre_completo)
                )
            ),
            procesador:usuarios!procesado_por(nombre_completo),
            autorizador:usuarios!autorizado_por(nombre_completo)
        """).eq("id", payment_id).execute()
        
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_payments_by_patient(self, 
                               paciente_id: str,
                               incluir_anulados: bool = False) -> List[Dict[str, Any]]:
        """
        Obtiene todos los pagos de un paciente
        
        Args:
            paciente_id: ID del paciente
            incluir_anulados: Si incluir pagos anulados
            
        Returns:
            Lista de pagos del paciente
        """
        query = self.table.select("*").eq("paciente_id", paciente_id)
        
        if not incluir_anulados:
            query = query.neq("estado_pago", "anulado")
        
        query = query.order("fecha_pago", desc=True)
        response = query.execute()
        
        return response.data
    
    @handle_supabase_error
    def get_pending_payments(self, paciente_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene pagos pendientes
        
        Args:
            paciente_id: Filtrar por paciente (opcional)
            
        Returns:
            Lista de pagos pendientes
        """
        query = self.table.select("""
            *,
            pacientes(nombre_completo, numero_historia, telefono)
        """).eq("estado_pago", "pendiente")
        
        if paciente_id:
            query = query.eq("paciente_id", paciente_id)
        
        query = query.order("fecha_pago")
        response = query.execute()
        
        return response.data
    
    @handle_supabase_error
    def get_payments_by_date_range(self,
                                  fecha_inicio: date,
                                  fecha_fin: date,
                                  metodo_pago: Optional[str] = None,
                                  estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene pagos en un rango de fechas
        
        Args:
            fecha_inicio: Fecha inicial
            fecha_fin: Fecha final
            metodo_pago: Filtrar por método de pago
            estado: Filtrar por estado
            
        Returns:
            Lista de pagos en el rango
        """
        # Convertir dates a datetime para la comparación
        fecha_inicio_dt = datetime.combine(fecha_inicio, datetime.min.time())
        fecha_fin_dt = datetime.combine(fecha_fin, datetime.max.time())
        
        query = self.table.select("""
            *,
            pacientes(nombre_completo, numero_historia)
        """).gte("fecha_pago", fecha_inicio_dt.isoformat()
        ).lte("fecha_pago", fecha_fin_dt.isoformat())
        
        if metodo_pago:
            query = query.eq("metodo_pago", metodo_pago)
        if estado:
            query = query.eq("estado_pago", estado)
        
        query = query.order("fecha_pago", desc=True)
        response = query.execute()
        
        return response.data
    
    @handle_supabase_error
    def process_partial_payment(self,
                               payment_id: str,
                               monto_adicional: Decimal,
                               metodo_pago: str,
                               procesado_por: str,
                               referencia: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesa un pago parcial sobre un pago existente
        
        Args:
            payment_id: ID del pago original
            monto_adicional: Monto adicional pagado
            metodo_pago: Método del pago adicional
            procesado_por: ID del usuario que procesa
            referencia: Referencia del pago adicional
            
        Returns:
            Nuevo pago creado
        """
        # Obtener pago original
        pago_original = self.get_by_id(payment_id)
        if not pago_original:
            raise ValueError(f"Pago {payment_id} no encontrado")
        
        # Crear nuevo pago parcial
        nuevo_pago = self.create_payment(
            paciente_id=pago_original["paciente_id"],
            monto_total=Decimal(str(pago_original["saldo_pendiente"])),
            monto_pagado=monto_adicional,
            concepto=f"Pago parcial - Ref: {pago_original['numero_recibo']}",
            procesado_por=procesado_por,
            consulta_id=pago_original.get("consulta_id"),
            metodo_pago=metodo_pago,
            referencia_pago=referencia
        )
        
        return nuevo_pago
    
    @handle_supabase_error
    def cancel_payment(self, payment_id: str, motivo: str, autorizado_por: str) -> Dict[str, Any]:
        """
        Anula un pago
        
        Args:
            payment_id: ID del pago
            motivo: Motivo de anulación
            autorizado_por: ID del usuario que autoriza
            
        Returns:
            Pago anulado
        """
        data = {
            "estado_pago": "anulado",
            "observaciones": f"ANULADO: {motivo}",
            "autorizado_por": autorizado_por
        }
        
        logger.info(f"Anulando pago {payment_id}")
        return self.update(payment_id, data)
    
    @handle_supabase_error
    def issue_refund(self,
                    payment_id: str,
                    monto_reembolso: Decimal,
                    motivo: str,
                    procesado_por: str,
                    autorizado_por: str) -> Dict[str, Any]:
        """
        Procesa un reembolso
        
        Args:
            payment_id: ID del pago original
            monto_reembolso: Monto a reembolsar
            motivo: Motivo del reembolso
            procesado_por: ID del usuario que procesa
            autorizado_por: ID del usuario que autoriza
            
        Returns:
            Registro de reembolso creado
        """
        # Obtener pago original
        pago_original = self.get_by_id(payment_id)
        if not pago_original:
            raise ValueError(f"Pago {payment_id} no encontrado")
        
        # Crear registro de reembolso (pago negativo)
        reembolso = self.create_payment(
            paciente_id=pago_original["paciente_id"],
            monto_total=-abs(float(monto_reembolso)),
            monto_pagado=-abs(float(monto_reembolso)),
            concepto=f"REEMBOLSO - {motivo} - Ref: {pago_original['numero_recibo']}",
            procesado_por=procesado_por,
            consulta_id=pago_original.get("consulta_id"),
            metodo_pago=pago_original["metodo_pago"],
            autorizado_por=autorizado_por,
            observaciones=f"Reembolso del pago {pago_original['numero_recibo']}"
        )
        
        # Actualizar pago original
        self.update(payment_id, {
            "estado_pago": "reembolsado",
            "observaciones": f"Reembolsado: {motivo}"
        })
        
        return reembolso
    
    @handle_supabase_error
    def get_daily_summary(self, fecha: Optional[date] = None) -> Dict[str, Any]:
        """
        Obtiene resumen de pagos del día
        
        Args:
            fecha: Fecha a consultar (por defecto hoy)
            
        Returns:
            Resumen con totales por método de pago
        """
        if not fecha:
            fecha = date.today()
        
        pagos_dia = self.get_payments_by_date_range(fecha, fecha)
        
        # Calcular resumen
        resumen = {
            "fecha": fecha.isoformat(),
            "total_pagos": len(pagos_dia),
            "total_recaudado": 0,
            "por_metodo": {},
            "pagos_pendientes": 0,
            "pagos_completados": 0,
            "pagos_anulados": 0
        }
        
        for pago in pagos_dia:
            if pago["estado_pago"] == "completado":
                resumen["total_recaudado"] += pago["monto_pagado"]
                resumen["pagos_completados"] += 1
                
                metodo = pago["metodo_pago"]
                if metodo not in resumen["por_metodo"]:
                    resumen["por_metodo"][metodo] = {"cantidad": 0, "total": 0}
                
                resumen["por_metodo"][metodo]["cantidad"] += 1
                resumen["por_metodo"][metodo]["total"] += pago["monto_pagado"]
                
            elif pago["estado_pago"] == "pendiente":
                resumen["pagos_pendientes"] += 1
            elif pago["estado_pago"] == "anulado":
                resumen["pagos_anulados"] += 1
        
        return resumen
    
    @handle_supabase_error
    def get_patient_balance(self, paciente_id: str) -> Dict[str, Any]:
        """
        Obtiene el balance de pagos de un paciente
        
        Args:
            paciente_id: ID del paciente
            
        Returns:
            Balance con totales y saldos
        """
        pagos = self.get_payments_by_patient(paciente_id, incluir_anulados=False)
        
        balance = {
            "paciente_id": paciente_id,
            "total_facturado": 0,
            "total_pagado": 0,
            "total_descuentos": 0,
            "saldo_pendiente": 0,
            "pagos_completados": 0,
            "pagos_pendientes": 0
        }
        
        for pago in pagos:
            if pago["estado_pago"] != "anulado":
                balance["total_facturado"] += pago["monto_total"]
                balance["total_pagado"] += pago["monto_pagado"]
                balance["total_descuentos"] += pago["descuento_aplicado"]
                
                if pago["estado_pago"] == "completado":
                    balance["pagos_completados"] += 1
                elif pago["estado_pago"] == "pendiente":
                    balance["pagos_pendientes"] += 1
                    balance["saldo_pendiente"] += pago.get("saldo_pendiente", 0)
        
        return balance