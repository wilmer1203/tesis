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
    def create_dual_payment(self,
                           paciente_id: str,
                           monto_total_usd: Decimal,
                           pago_usd: Decimal,
                           pago_bs: Decimal,
                           tasa_cambio: Decimal,
                           concepto: str,
                           procesado_por: str,
                           metodos_pago: List[Dict[str, Any]],
                           consulta_id: Optional[str] = None,
                           descuento_usd: Decimal = Decimal('0'),
                           motivo_descuento: Optional[str] = None,
                           autorizado_por: Optional[str] = None,
                           observaciones: Optional[str] = None) -> Dict[str, Any]:
        """
        Crear pago con sistema dual USD/BS simplificado

        Args:
            paciente_id: ID del paciente
            monto_total_usd: Monto total en USD (base)
            pago_usd: Cantidad pagada en USD
            pago_bs: Cantidad pagada en BS
            tasa_cambio: Tasa de conversión BS/USD del día
            concepto: Concepto del pago
            procesado_por: ID del usuario que procesa
            metodos_pago: Lista de métodos de pago [{"tipo": "efectivo_usd", "monto": 100, "referencia": ""}, ...]
            consulta_id: ID de la consulta relacionada (opcional)
            descuento_usd: Descuento aplicado en USD
            motivo_descuento: Motivo del descuento
            autorizado_por: ID del usuario que autoriza
            observaciones: Observaciones adicionales

        Returns:
            Pago creado con cálculos automáticos duales
        """

        # 🧮 CÁLCULOS AUTOMÁTICOS DUALES
        monto_total_bs = float(monto_total_usd) * float(tasa_cambio)

        # Convertir pago BS a USD para calcular total pagado
        pago_bs_to_usd = float(pago_bs) / float(tasa_cambio) if tasa_cambio > 0 else 0
        total_pagado_usd = float(pago_usd) + pago_bs_to_usd

        # Calcular saldos pendientes
        saldo_pendiente_usd = max(0, float(monto_total_usd) - float(descuento_usd) - total_pagado_usd)
        saldo_pendiente_bs = saldo_pendiente_usd * float(tasa_cambio)

        # Determinar estado automático
        estado_pago = "completado" if saldo_pendiente_usd <= 0.01 else "pendiente"

        data = {
            # 💰 CAMPOS DUALES USD/BS
            "monto_total_usd": float(monto_total_usd),
            "monto_total_bs": monto_total_bs,
            "monto_pagado_usd": float(pago_usd),
            "monto_pagado_bs": float(pago_bs),
            "saldo_pendiente_usd": saldo_pendiente_usd,
            "saldo_pendiente_bs": saldo_pendiente_bs,
            "tasa_cambio_bs_usd": float(tasa_cambio),

            # 🎛️ MÉTODOS DE PAGO MÚLTIPLES (JSONB)
            "metodos_pago": metodos_pago,

            # 📋 CAMPOS TRADICIONALES (BACKWARD COMPATIBILITY)
            "monto_total": float(monto_total_usd),  # Alias USD
            "monto_pagado": total_pagado_usd,       # Total pagado en USD equivalente
            "saldo_pendiente": saldo_pendiente_usd, # Saldo en USD
            "metodo_pago": metodos_pago[0].get("tipo", "efectivo") if metodos_pago else "efectivo",

            # 📊 INFORMACIÓN BÁSICA
            "paciente_id": paciente_id,
            "concepto": concepto,
            "procesado_por": procesado_por,
            "estado_pago": estado_pago,
            "descuento_aplicado": float(descuento_usd),
            "impuestos": 0.0  # No aplica en este sistema
        }

        # Agregar campos opcionales
        if consulta_id:
            data["consulta_id"] = consulta_id
        if motivo_descuento and descuento_usd > 0:
            data["motivo_descuento"] = motivo_descuento
        if autorizado_por:
            data["autorizado_por"] = autorizado_por
        if observaciones:
            data["observaciones"] = observaciones

        logger.info(f"Creando pago dual: ${pago_usd} USD + {pago_bs} BS (Tasa: {tasa_cambio}) para paciente {paciente_id}")
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
            pacientes(primer_nombre, primer_apellido, numero_historia, celular_1)
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
            pacientes(primer_nombre, primer_apellido, numero_historia)
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

    @handle_supabase_error
    def get_currency_summary(self, fecha: Optional[date] = None) -> Dict[str, Any]:
        """
        Resumen financiero dual USD/BS para estadísticas

        Args:
            fecha: Fecha a consultar (por defecto hoy)

        Returns:
            Resumen con totales por moneda y estadísticas de uso
        """
        if not fecha:
            fecha = date.today()

        pagos_dia = self.get_payments_by_date_range(fecha, fecha)

        resumen = {
            "fecha": fecha.isoformat(),
            "total_recaudado_usd": 0.0,
            "total_recaudado_bs": 0.0,
            "total_pendiente_usd": 0.0,
            "total_pendiente_bs": 0.0,
            "tasa_promedio": 0.0,
            "pagos_mixtos": 0,
            "pagos_solo_usd": 0,
            "pagos_solo_bs": 0,
            "total_pagos": len(pagos_dia),
            "pagos_completados": 0,
            "pagos_pendientes": 0
        }

        tasas = []
        for pago in pagos_dia:
            # Usar campos duales si están disponibles, sino fallback a campos legacy
            pagado_usd = pago.get("monto_pagado_usd", pago.get("monto_pagado", 0))
            pagado_bs = pago.get("monto_pagado_bs", 0)
            pendiente_usd = pago.get("saldo_pendiente_usd", pago.get("saldo_pendiente", 0))
            pendiente_bs = pago.get("saldo_pendiente_bs", 0)
            tasa = pago.get("tasa_cambio_bs_usd", 0)

            # Totales de recaudación (solo completados)
            if pago.get("estado_pago") == "completado":
                resumen["total_recaudado_usd"] += pagado_usd
                resumen["total_recaudado_bs"] += pagado_bs
                resumen["pagos_completados"] += 1
            elif pago.get("estado_pago") == "pendiente":
                resumen["pagos_pendientes"] += 1

            # Totales pendientes
            resumen["total_pendiente_usd"] += pendiente_usd
            resumen["total_pendiente_bs"] += pendiente_bs

            # Clasificar tipo de pago
            if pagado_usd > 0 and pagado_bs > 0:
                resumen["pagos_mixtos"] += 1
            elif pagado_usd > 0:
                resumen["pagos_solo_usd"] += 1
            elif pagado_bs > 0:
                resumen["pagos_solo_bs"] += 1

            # Acumular tasas para promedio
            if tasa > 0:
                tasas.append(tasa)

        # Calcular tasa promedio
        resumen["tasa_promedio"] = round(sum(tasas) / len(tasas), 2) if tasas else 36.50

        logger.info(f"Resumen dual currency generado: ${resumen['total_recaudado_usd']} USD + {resumen['total_recaudado_bs']} BS")
        return resumen

    @handle_supabase_error
    def get_consultas_pendientes_facturacion(self) -> List[Dict[str, Any]]:
        """
        🏥 Obtener consultas completadas pendientes de facturación

        Returns:
            Lista de consultas con pagos pendientes e información relacionada
        """
        try:
            # Query compleja para obtener consultas completadas con pagos pendientes
            query = self.client.table("consultas").select("""
                id,
                numero_consulta,
                paciente_id,
                primer_odontologo_id,
                fecha_llegada,
                estado,
                pacientes!inner(primer_nombre, primer_apellido, numero_documento),
                personal!primer_odontologo_id(primer_nombre, primer_apellido),
                intervenciones(
                    id,
                    total_usd,
                    total_bs,
                    procedimiento_realizado,
                    intervenciones_servicios(
                        cantidad,
                        servicios(nombre)
                    )
                ),
                pagos!inner(
                    id,
                    estado_pago,
                    monto_total_usd,
                    monto_total_bs,
                    saldo_pendiente_usd,
                    saldo_pendiente_bs
                )
            """).eq("estado", "completada").eq("pagos.estado_pago", "pendiente")

            response = query.execute()

            if not response.data:
                logger.info("No hay consultas pendientes de facturación")
                return []

            consultas_procesadas = []

            for consulta in response.data:
                # Calcular totales de intervenciones
                total_usd = sum(float(i.get("total_usd", 0)) for i in consulta.get("intervenciones", []))
                total_bs = sum(float(i.get("total_bs", 0)) for i in consulta.get("intervenciones", []))

                # Contar servicios realizados
                servicios_count = 0
                servicios_detalle = []
                for intervencion in consulta.get("intervenciones", []):
                    for is_item in intervencion.get("intervenciones_servicios", []):
                        servicios_count += is_item.get("cantidad", 1)
                        servicios_detalle.append({
                            "nombre": is_item.get("servicios", {}).get("nombre", "Servicio"),
                            "cantidad": is_item.get("cantidad", 1)
                        })

                # Información del paciente
                paciente = consulta.get("pacientes", {})
                paciente_nombre = f"{paciente.get('primer_nombre', '')} {paciente.get('primer_apellido', '')}".strip()

                # Información del odontólogo
                odontologo = consulta.get("personal", {})
                odontologo_nombre = f"Dr. {odontologo.get('primer_nombre', '')} {odontologo.get('primer_apellido', '')}".strip()

                # Calcular días pendientes
                from datetime import datetime, date
                fecha_consulta = consulta.get("fecha_llegada")
                dias_pendiente = 0
                if fecha_consulta:
                    try:
                        if isinstance(fecha_consulta, str):
                            fecha_obj = datetime.fromisoformat(fecha_consulta.replace('Z', '+00:00')).date()
                        else:
                            fecha_obj = fecha_consulta
                        dias_pendiente = (date.today() - fecha_obj).days
                    except:
                        dias_pendiente = 0

                consulta_data = {
                    "id": consulta["id"],
                    "numero_consulta": consulta.get("numero_consulta", "CONS-000"),
                    "paciente_id": consulta["paciente_id"],
                    "paciente_nombre": paciente_nombre,
                    "paciente_apellido": paciente.get("primer_apellido", ""),
                    "paciente_documento": paciente.get("numero_documento", ""),
                    "primer_odontologo_id": consulta["primer_odontologo_id"],
                    "odontologo_nombre": odontologo_nombre,
                    "fecha_llegada": consulta.get("fecha_llegada", ""),
                    "estado": consulta.get("estado", "completada"),
                    "total_usd": total_usd,
                    "total_bs": total_bs,
                    "servicios_count": servicios_count,
                    "servicios_detalle": servicios_detalle,
                    "dias_pendiente": dias_pendiente
                }

                consultas_procesadas.append(consulta_data)

            logger.info(f"✅ {len(consultas_procesadas)} consultas pendientes de facturación obtenidas")
            return consultas_procesadas

        except Exception as e:
            logger.error(f"❌ Error obteniendo consultas pendientes: {str(e)}")
            return []


# Instancia única para importar
payments_table = PaymentsTable()
pagos_table = payments_table  # Alias para consistencia