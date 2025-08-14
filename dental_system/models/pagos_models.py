"""
Modelos de datos para el módulo de PAGOS
Centraliza todos los modelos relacionados con facturación y pagos
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class PagoModel(rx.Base):
    """Modelo para datos de pagos y facturación"""
    id: Optional[str] = ""
    numero_recibo: str = ""
    consulta_id: Optional[str] = ""
    paciente_id: str = ""
    fecha_pago: str = ""
    monto_total: float = 0.0
    monto_pagado: float = 0.0
    saldo_pendiente: float = 0.0
    metodo_pago: str = ""
    referencia_pago: Optional[str] = ""
    concepto: str = ""
    estado_pago: str = "completado"
    descuento_aplicado: float = 0.0
    motivo_descuento: Optional[str] = ""
    impuestos: float = 0.0
    numero_factura: Optional[str] = ""
    fecha_facturacion: Optional[str] = ""
    observaciones: Optional[str] = ""
    procesado_por: str = ""
    autorizado_por: Optional[str] = ""
    
    # Información relacionada
    paciente_nombre: str = ""
    paciente_documento: str = ""
    procesado_por_nombre: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PagoModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # Manejar datos relacionados
        paciente_data = data.get("pacientes", {})
        procesado_por_data = data.get("procesado_por_usuario", {})
        
        return cls(
            id=str(data.get("id", "")),
            numero_recibo=str(data.get("numero_recibo", "")),
            consulta_id=str(data.get("consulta_id", "") if data.get("consulta_id") else ""),
            paciente_id=str(data.get("paciente_id", "")),
            fecha_pago=str(data.get("fecha_pago", "")),
            monto_total=float(data.get("monto_total", 0)),
            monto_pagado=float(data.get("monto_pagado", 0)),
            saldo_pendiente=float(data.get("saldo_pendiente", 0)),
            metodo_pago=str(data.get("metodo_pago", "")),
            referencia_pago=str(data.get("referencia_pago", "") if data.get("referencia_pago") else ""),
            concepto=str(data.get("concepto", "")),
            estado_pago=str(data.get("estado_pago", "completado")),
            descuento_aplicado=float(data.get("descuento_aplicado", 0)),
            motivo_descuento=str(data.get("motivo_descuento", "") if data.get("motivo_descuento") else ""),
            impuestos=float(data.get("impuestos", 0)),
            numero_factura=str(data.get("numero_factura", "") if data.get("numero_factura") else ""),
            fecha_facturacion=str(data.get("fecha_facturacion", "") if data.get("fecha_facturacion") else ""),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            procesado_por=str(data.get("procesado_por", "")),
            autorizado_por=str(data.get("autorizado_por", "") if data.get("autorizado_por") else ""),
            
            # Información relacionada
            paciente_nombre=str(paciente_data.get("nombre_completo", "") if paciente_data else ""),
            paciente_documento=str(paciente_data.get("numero_documento", "") if paciente_data else ""),
            procesado_por_nombre=str(procesado_por_data.get("email", "") if procesado_por_data else "")
        )
    
    @property
    def estado_display(self) -> str:
        """Propiedad para mostrar el estado del pago"""
        estados_map = {
            "pendiente": "⏳ Pendiente",
            "completado": "✅ Completado",
            "anulado": "❌ Anulado",
            "reembolsado": "🔄 Reembolsado"
        }
        return estados_map.get(self.estado_pago, self.estado_pago.capitalize())
    
    @property
    def monto_total_display(self) -> str:
        """Propiedad para mostrar el monto total formateado"""
        return f"${self.monto_total:,.2f}"
    
    @property
    def monto_pagado_display(self) -> str:
        """Propiedad para mostrar el monto pagado formateado"""
        return f"${self.monto_pagado:,.2f}"
    
    @property
    def saldo_pendiente_display(self) -> str:
        """Propiedad para mostrar el saldo pendiente formateado"""
        return f"${self.saldo_pendiente:,.2f}"
    
    @property
    def fecha_display(self) -> str:
        """Propiedad para mostrar la fecha formateada"""
        try:
            if self.fecha_pago:
                fecha_obj = datetime.fromisoformat(self.fecha_pago.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y")
            return "Sin fecha"
        except:
            return str(self.fecha_pago)
    
    @property
    def metodo_pago_display(self) -> str:
        """Método de pago formateado para mostrar"""
        metodos_map = {
            "efectivo": "💵 Efectivo",
            "tarjeta_credito": "💳 Tarjeta de Crédito",
            "tarjeta_debito": "💳 Tarjeta Débito",
            "transferencia": "🏦 Transferencia",
            "cheque": "📄 Cheque",
            "otro": "📋 Otro"
        }
        return metodos_map.get(self.metodo_pago, self.metodo_pago.title())
    
    @property
    def descuento_display(self) -> str:
        """Descuento formateado para mostrar"""
        if self.descuento_aplicado > 0:
            return f"-${self.descuento_aplicado:,.2f}"
        return "Sin descuento"
    
    @property
    def impuestos_display(self) -> str:
        """Impuestos formateados para mostrar"""
        if self.impuestos > 0:
            return f"${self.impuestos:,.2f}"
        return "Sin impuestos"
    
    @property
    def tiene_saldo_pendiente(self) -> bool:
        """Indica si tiene saldo pendiente"""
        return self.saldo_pendiente > 0
    
    @property
    def esta_completamente_pagado(self) -> bool:
        """Indica si está completamente pagado"""
        return self.saldo_pendiente == 0 and self.estado_pago == "completado"
    
    @property
    def porcentaje_pagado(self) -> float:
        """Porcentaje del monto total que ha sido pagado"""
        if self.monto_total > 0:
            return (self.monto_pagado / self.monto_total) * 100
        return 0.0


class PagosStatsModel(rx.Base):
    """Modelo para estadísticas de pagos"""
    total_mes: float = 0.0
    pendientes: float = 0.0
    completados: float = 0.0
    reembolsados: float = 0.0
    anulados: float = 0.0
    
    # Contadores
    cantidad_pagos: int = 0
    cantidad_pendientes: int = 0
    cantidad_completados: int = 0
    
    # Por método de pago
    por_metodo: Dict[str, float] = {}
    
    # Promedio
    monto_promedio: float = 0.0


class FacturaModel(rx.Base):
    """Modelo para facturas detalladas"""
    id: str = ""
    numero_factura: str = ""
    fecha_factura: str = ""
    paciente_id: str = ""
    consulta_id: str = ""
    
    # Información del paciente
    paciente_nombre: str = ""
    paciente_documento: str = ""
    paciente_direccion: str = ""
    
    # Información de la clínica
    clinica_nombre: str = ""
    clinica_nit: str = ""
    clinica_direccion: str = ""
    clinica_telefono: str = ""
    
    # Detalles de la factura
    items: List[Dict[str, Any]] = []
    subtotal: float = 0.0
    descuentos: float = 0.0
    impuestos: float = 0.0
    total: float = 0.0
    
    # Estado
    estado_factura: str = "emitida"  # emitida, pagada, anulada
    fecha_vencimiento: Optional[str] = ""
    observaciones: Optional[str] = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FacturaModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            numero_factura=str(data.get("numero_factura", "")),
            fecha_factura=str(data.get("fecha_factura", "")),
            paciente_id=str(data.get("paciente_id", "")),
            consulta_id=str(data.get("consulta_id", "")),
            paciente_nombre=str(data.get("paciente_nombre", "")),
            paciente_documento=str(data.get("paciente_documento", "")),
            paciente_direccion=str(data.get("paciente_direccion", "")),
            clinica_nombre=str(data.get("clinica_nombre", "")),
            clinica_nit=str(data.get("clinica_nit", "")),
            clinica_direccion=str(data.get("clinica_direccion", "")),
            clinica_telefono=str(data.get("clinica_telefono", "")),
            items=data.get("items", []),
            subtotal=float(data.get("subtotal", 0)),
            descuentos=float(data.get("descuentos", 0)),
            impuestos=float(data.get("impuestos", 0)),
            total=float(data.get("total", 0)),
            estado_factura=str(data.get("estado_factura", "emitida")),
            fecha_vencimiento=str(data.get("fecha_vencimiento", "") if data.get("fecha_vencimiento") else ""),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else "")
        )


class ConceptoPagoModel(rx.Base):
    """Modelo para conceptos de pago predefinidos"""
    id: str = ""
    nombre: str = ""
    descripcion: str = ""
    categoria: str = ""  # consulta, tratamiento, producto, etc.
    precio_sugerido: Optional[float] = None
    activo: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConceptoPagoModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            nombre=str(data.get("nombre", "")),
            descripcion=str(data.get("descripcion", "")),
            categoria=str(data.get("categoria", "")),
            precio_sugerido=float(data.get("precio_sugerido")) if data.get("precio_sugerido") else None,
            activo=bool(data.get("activo", True))
        )


class BalanceGeneralModel(rx.Base):
    """Modelo para balance general de pagos"""
    fecha_desde: str = ""
    fecha_hasta: str = ""
    
    # Ingresos
    total_ingresos: float = 0.0
    ingresos_efectivo: float = 0.0
    ingresos_tarjetas: float = 0.0
    ingresos_transferencias: float = 0.0
    ingresos_otros: float = 0.0
    
    # Pendientes
    total_pendientes: float = 0.0
    cantidad_pendientes: int = 0
    
    # Descuentos
    total_descuentos: float = 0.0
    
    # Impuestos
    total_impuestos: float = 0.0
    
    # Comparativa
    crecimiento_vs_periodo_anterior: float = 0.0
    porcentaje_cumplimiento_meta: float = 0.0


class CuentaPorCobrarModel(rx.Base):
    """Modelo para cuentas por cobrar"""
    paciente_id: str = ""
    paciente_nombre: str = ""
    paciente_documento: str = ""
    paciente_telefono: str = ""
    
    total_pendiente: float = 0.0
    cantidad_facturas: int = 0
    dias_vencimiento_promedio: int = 0
    fecha_ultima_factura: str = ""
    
    # Desglose por antigüedad
    vencido_0_30_dias: float = 0.0
    vencido_31_60_dias: float = 0.0
    vencido_61_90_dias: float = 0.0
    vencido_mas_90_dias: float = 0.0
    
    @property
    def nivel_riesgo(self) -> str:
        """Determina el nivel de riesgo de la cuenta"""
        if self.dias_vencimiento_promedio <= 30:
            return "bajo"
        elif self.dias_vencimiento_promedio <= 60:
            return "medio"
        else:
            return "alto"
    
    @property
    def color_riesgo(self) -> str:
        """Color según el nivel de riesgo"""
        colors = {
            "bajo": "#28a745",    # Verde
            "medio": "#ffc107",   # Amarillo
            "alto": "#dc3545"     # Rojo
        }
        return colors.get(self.nivel_riesgo, "#007bff")