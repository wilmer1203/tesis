"""
Modelos de datos para el módulo de PAGOS
Centraliza todos los modelos relacionados con facturación y pagos
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class PagoModel(rx.Base):
    """
    Modelo para datos de pagos y facturación con sistema dual USD/BS

    SISTEMA DUAL:
    - USD como moneda principal de trabajo
    - BS calculado automáticamente con tasa del día
    - Soporte para pagos mixtos (USD + BS simultáneo)
    """
    id: Optional[str] = ""
    numero_recibo: str = ""
    consulta_id: Optional[str] = ""
    paciente_id: str = ""
    fecha_pago: str = ""

    # 💰 SISTEMA DUAL USD/BS - CAMPOS PRINCIPALES
    monto_total_usd: float = 0.0           # Monto principal en USD
    monto_pagado_usd: float = 0.0          # Lo que pagó en USD
    saldo_pendiente_usd: float = 0.0       # Saldo pendiente en USD

    # 💰 CONVERSIÓN AUTOMÁTICA BS
    monto_total_bs: float = 0.0            # Auto-calculado: total_usd * tasa
    monto_pagado_bs: float = 0.0           # Lo que pagó en BS
    saldo_pendiente_bs: float = 0.0        # Auto-calculado: pendiente_usd * tasa
    tasa_cambio_bs_usd: float = 36.50      # Tasa del día usada en el pago

    # 🎛️ MÉTODOS DE PAGO MÚLTIPLES (JSONB)
    metodos_pago: List[Dict[str, Any]] = []  # [{"tipo": "efectivo_usd", "monto": 100, "referencia": ""}, ...]

    # 📋 CAMPOS TRADICIONALES (BACKWARD COMPATIBILITY)
    monto_total: float = 0.0               # Alias para monto_total_usd
    monto_pagado: float = 0.0              # Alias para monto_pagado_usd
    saldo_pendiente: float = 0.0           # Alias para saldo_pendiente_usd
    metodo_pago: str = ""                  # Método principal (compatibilidad)
    referencia_pago: Optional[str] = ""

    # 📊 INFORMACIÓN ADICIONAL
    concepto: str = ""
    estado_pago: str = "completado"
    descuento_aplicado: float = 0.0        # Descuento en USD
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
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PagoModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # Manejar datos relacionados
        paciente_data = data.get("pacientes", {})

        # Construir nombre del paciente con diferentes formatos posibles
        paciente_nombre = ""
        if paciente_data:
            # Intentar nombre_completo primero
            if paciente_data.get("nombre_completo"):
                paciente_nombre = str(paciente_data.get("nombre_completo", ""))
            else:
                # Construir desde nombres separados
                primer_nombre = paciente_data.get("primer_nombre", "")
                primer_apellido = paciente_data.get("primer_apellido", "")
                paciente_nombre = f"{primer_nombre} {primer_apellido}".strip()

        return cls(
            id=str(data.get("id", "")),
            numero_recibo=str(data.get("numero_recibo", "")),
            consulta_id=str(data.get("consulta_id", "") if data.get("consulta_id") else ""),
            paciente_id=str(data.get("paciente_id", "")),
            fecha_pago=str(data.get("fecha_pago", "")),

            # 💰 CAMPOS DUALES USD/BS
            monto_total_usd=float(data.get("monto_total_usd", data.get("monto_total", 0))),
            monto_pagado_usd=float(data.get("monto_pagado_usd", data.get("monto_pagado", 0))),
            saldo_pendiente_usd=float(data.get("saldo_pendiente_usd", data.get("saldo_pendiente", 0))),
            monto_total_bs=float(data.get("monto_total_bs", 0)),
            monto_pagado_bs=float(data.get("monto_pagado_bs", 0)),
            saldo_pendiente_bs=float(data.get("saldo_pendiente_bs", 0)),
            tasa_cambio_bs_usd=float(data.get("tasa_cambio_bs_usd", 36.50)),

            # 🎛️ MÉTODOS DE PAGO (JSONB o string legacy)
            metodos_pago=data.get("metodos_pago", []) if isinstance(data.get("metodos_pago"), list) else [],

            # 📋 CAMPOS TRADICIONALES (BACKWARD COMPATIBILITY)
            monto_total=float(data.get("monto_total_usd", data.get("monto_total", 0))),
            monto_pagado=float(data.get("monto_pagado_usd", data.get("monto_pagado", 0))),
            saldo_pendiente=float(data.get("saldo_pendiente_usd", data.get("saldo_pendiente", 0))),
            metodo_pago=str(data.get("metodo_pago", "")),
            referencia_pago=str(data.get("referencia_pago", "") if data.get("referencia_pago") else ""),

            # 📊 INFORMACIÓN ADICIONAL
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

            # Información relacionada (usando la variable construida arriba)
            paciente_nombre=paciente_nombre,
            paciente_documento=str(paciente_data.get("numero_documento", "") if paciente_data else ""),
        )

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

    # ==========================================
    # 💰 NUEVAS COMPUTED PROPERTIES - SISTEMA DUAL USD/BS
    # ==========================================

    @property
    def monto_total_usd_display(self) -> str:
        """Monto total en USD formateado"""
        return f"${self.monto_total_usd:,.2f}"

    @property
    def monto_total_bs_display(self) -> str:
        """Monto total en BS formateado"""
        return f"{self.monto_total_bs:,.0f} BS"

    @property
    def monto_pagado_usd_display(self) -> str:
        """Monto pagado en USD formateado"""
        return f"${self.monto_pagado_usd:,.2f}"

    @property
    def monto_pagado_bs_display(self) -> str:
        """Monto pagado en BS formateado"""
        return f"{self.monto_pagado_bs:,.0f} BS"

    @property
    def saldo_pendiente_usd_display(self) -> str:
        """Saldo pendiente en USD formateado"""
        return f"${self.saldo_pendiente_usd:,.2f}"

    @property
    def saldo_pendiente_bs_display(self) -> str:
        """Saldo pendiente en BS formateado"""
        return f"{self.saldo_pendiente_bs:,.0f} BS"

    @property
    def tasa_cambio_display(self) -> str:
        """Tasa de cambio formateada"""
        return f"1 USD = {self.tasa_cambio_bs_usd:,.2f} BS"

    @property
    def es_pago_mixto(self) -> bool:
        """True si pagó en USD y BS simultáneamente"""
        return self.monto_pagado_bs > 0 and self.monto_pagado_usd > 0

    @property
    def total_pagado_equivalente_usd(self) -> float:
        """Total pagado convertido a USD para cálculos"""
        bs_to_usd = self.monto_pagado_bs / self.tasa_cambio_bs_usd if self.tasa_cambio_bs_usd > 0 else 0
        return self.monto_pagado_usd + bs_to_usd

    @property
    def porcentaje_pagado_dual(self) -> float:
        """Porcentaje pagado considerando ambas monedas"""
        if self.monto_total_usd > 0:
            return (self.total_pagado_equivalente_usd / self.monto_total_usd) * 100
        return 0.0

    @property
    def porcentaje_pagado_display(self) -> str:
        """Porcentaje pagado formateado para mostrar"""
        return f"{self.porcentaje_pagado_dual:.1f}%"

    @property
    def resumen_pago_display(self) -> str:
        """Resumen legible del pago dual"""
        partes = []
        if self.monto_pagado_usd > 0:
            partes.append(f"${self.monto_pagado_usd:.2f} USD")
        if self.monto_pagado_bs > 0:
            partes.append(f"{self.monto_pagado_bs:,.0f} BS")
        return " + ".join(partes) if partes else "Sin pagos"

    @property
    def distribucion_monedas(self) -> Dict[str, float]:
        """Distribución porcentual por moneda"""
        total_equivalente = self.total_pagado_equivalente_usd
        if total_equivalente <= 0:
            return {"usd": 0.0, "bs": 0.0}

        pct_usd = (self.monto_pagado_usd / total_equivalente) * 100 if total_equivalente > 0 else 0
        pct_bs = 100 - pct_usd

        return {
            "usd": round(pct_usd, 1),
            "bs": round(pct_bs, 1)
        }
        
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


# ==========================================
# 📝 FORMULARIOS DE PAGOS
# ==========================================

class PagoFormModel(rx.Base):
    """
    📝 FORMULARIO DUAL USD/BS SIMPLIFICADO

    ENFOQUE:
    - USD como moneda principal de trabajo
    - Conversión automática a BS con tasa del día
    - Soporte para pagos mixtos (USD + BS simultáneo)
    - Cálculos automáticos de equivalencias
    """

    # 📋 REFERENCIAS BÁSICAS
    pago_id: str = ""  # ✅ ID del pago a actualizar (más importante que consulta_id)
    paciente_id: str = ""
    consulta_id: str = ""  # Opcional
    paciente_nombre: str = ""  # Nombre del paciente (display)
    numero_consulta: str = ""  # Número de consulta (display)

    # 💰 MONTO PRINCIPAL EN USD
    monto_total_usd: float = 0.0           # Monto base en USD
    monto_total_bs: float = 0.0            # Monto total en BS (calculado)

    # 💱 TASA DE CONVERSIÓN
    tasa_cambio: float = 36.50             # Tasa del día
    tasa_cambio_del_dia: str = "36.50"     # Tasa editable por usuario (string para input)

    # 💵 PAGOS EN AMBAS MONEDAS
    monto_pagado_usd: float = 0.0          # Cuánto paga en USD
    monto_pagado_bs: float = 0.0           # Cuánto paga en BS
    pago_usd: str = "0.00"                 # Cuánto paga en USD (string para input)
    pago_bs: str = "0"                     # Cuánto paga en BS (string para input)

    # 🎛️ MÉTODOS DE PAGO DUALES
    metodo_pago_usd: str = "efectivo"      # efectivo, tarjeta, transferencia
    metodo_pago_bs: str = "efectivo"       # efectivo, tarjeta, transferencia
    referencia_usd: str = ""               # Referencia pago USD
    referencia_bs: str = ""                # Referencia pago BS

    # 📝 CAMPOS ADICIONALES
    concepto: str = ""
    descuento_usd: float = 0.0             # Descuento en USD
    motivo_descuento: str = ""
    observaciones: str = ""
    notas: str = ""                        # Alias para observaciones

    # 📊 CAMPOS DE ESTADO
    estado_pago: str = "completado"        # pendiente, completado, anulado
    autorizado_por: str = ""

    def validate_dual_payment(self) -> Dict[str, List[str]]:
        """Validar pagos duales con lógica inteligente"""
        errors = {}

        # Validar campos requeridos
        if not self.paciente_id.strip():
            errors.setdefault("paciente_id", []).append("Paciente es requerido")

        if not self.concepto.strip():
            errors.setdefault("concepto", []).append("Concepto es requerido")

        try:
            # Validar montos numéricos
            total_usd = float(self.monto_total_usd)
            pago_usd = float(self.pago_usd)
            pago_bs = float(self.pago_bs)
            tasa = float(self.tasa_cambio_del_dia)
            descuento = float(self.descuento_usd)

            # Validar rangos
            if total_usd <= 0:
                errors.setdefault("monto_total_usd", []).append("Monto total debe ser mayor a 0")

            if tasa <= 0:
                errors.setdefault("tasa_cambio_del_dia", []).append("Tasa de cambio debe ser mayor a 0")

            if pago_usd < 0 or pago_bs < 0:
                errors.setdefault("pagos", []).append("Los pagos no pueden ser negativos")

            # Validar que al menos haya un pago
            if pago_usd <= 0 and pago_bs <= 0:
                errors.setdefault("pagos", []).append("Debe ingresar al menos un monto de pago")

            # Calcular total pagado en USD equivalente
            bs_to_usd = pago_bs / tasa if tasa > 0 else 0
            total_pagado_usd = pago_usd + bs_to_usd
            total_con_descuento = total_usd - descuento

            if total_pagado_usd > total_con_descuento:
                errors.setdefault("pagos", []).append("El pago total no puede exceder el monto adeudado")

            # Validar descuento
            if descuento > total_usd:
                errors.setdefault("descuento_usd", []).append("El descuento no puede ser mayor al monto total")

            if descuento > 0 and not self.motivo_descuento.strip():
                errors.setdefault("motivo_descuento", []).append("Debe especificar motivo del descuento")

        except (ValueError, TypeError):
            errors.setdefault("formato", []).append("Todos los montos deben ser números válidos")

        return errors

    # 🧮 COMPUTED PROPERTIES PARA CÁLCULOS AUTOMÁTICOS
    @property
    def monto_total_bs_calculado(self) -> float:
        """Total en BS automático"""
        try:
            return float(self.monto_total_usd) * float(self.tasa_cambio_del_dia)
        except:
            return 0.0

    @property
    def saldo_pendiente_usd(self) -> float:
        """Saldo pendiente en USD"""
        try:
            total = float(self.monto_total_usd)
            pagado_usd = float(self.pago_usd)
            pagado_bs = float(self.pago_bs) / float(self.tasa_cambio_del_dia)
            descuento = float(self.descuento_usd)

            return max(0, total - descuento - pagado_usd - pagado_bs)
        except:
            return 0.0

    @property
    def saldo_pendiente_bs(self) -> float:
        """Saldo pendiente en BS"""
        return self.saldo_pendiente_usd * float(self.tasa_cambio_del_dia) if self.tasa_cambio_del_dia else 0.0

    @property
    def total_pagado_equivalente_usd(self) -> float:
        """Total pagado convertido a USD"""
        try:
            pagado_usd = float(self.pago_usd)
            pagado_bs = float(self.pago_bs)
            tasa = float(self.tasa_cambio_del_dia)

            bs_to_usd = pagado_bs / tasa if tasa > 0 else 0
            return pagado_usd + bs_to_usd
        except:
            return 0.0

    @property
    def porcentaje_pagado(self) -> float:
        """Porcentaje del total que se ha pagado"""
        try:
            total = float(self.monto_total_usd)
            if total > 0:
                return (self.total_pagado_equivalente_usd / total) * 100
            return 0.0
        except:
            return 0.0

    @property
    def es_pago_mixto(self) -> bool:
        """True si paga en USD y BS"""
        try:
            return float(self.pago_usd) > 0 and float(self.pago_bs) > 0
        except:
            return False

    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad con servicios"""
        return {
            # Referencias
            "paciente_id": self.paciente_id,
            "consulta_id": self.consulta_id,

            # Montos duales
            "monto_total_usd": self.monto_total_usd,
            "tasa_cambio_del_dia": self.tasa_cambio_del_dia,
            "pago_usd": self.pago_usd,
            "pago_bs": self.pago_bs,

            # Métodos de pago
            "metodo_pago_usd": self.metodo_pago_usd,
            "metodo_pago_bs": self.metodo_pago_bs,
            "referencia_usd": self.referencia_usd,
            "referencia_bs": self.referencia_bs,

            # Información adicional
            "concepto": self.concepto,
            "descuento_usd": self.descuento_usd,
            "motivo_descuento": self.motivo_descuento,
            "observaciones": self.observaciones,
            "estado_pago": self.estado_pago,
            "autorizado_por": self.autorizado_por,
        }


class ServicioFormateado(rx.Base):
    """Modelo simple para servicios formateados en accordion"""
    nombre: str = ""
    odontologo: str = "" 
    precio_usd: str = "0.00"
    precio_bs: str = "0"


class ConsultaPendientePago(rx.Base):
    """Modelo tipado para consulta pendiente de pago"""
    pago_id: str = ""  
    consulta_id: str = ""
    numero_consulta: str = ""
    paciente_id: str = ""
    paciente_nombre: str = ""
    paciente_documento: str = ""
    paciente_numero_historia: str = ""  
    paciente_telefono: str = ""  
    odontologo_nombre: str = ""
    fecha_consulta: str = ""
    dias_pendiente: int = 0
    prioridad: str = "baja"
    servicios_count: int = 0
    concepto: str = ""
    total_usd: float = 0.0
    total_bs: float = 0.0
    servicios_formateados: list[ServicioFormateado] = []
