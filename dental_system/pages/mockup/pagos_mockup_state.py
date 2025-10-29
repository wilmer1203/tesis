"""
Estado simple para mockup de pagos con formulario interactivo
"""
import reflex as rx
from typing import Dict, Any, Optional

class PagosMockupState(rx.State):
    """Estado para gestionar el formulario de pago en el mockup"""

    # Modal y selección
    modal_pago_abierto: bool = False
    consulta_seleccionada: Dict[str, Any] = {}

    # Formulario de pago
    monto_usd: str = ""
    monto_bs: str = ""
    metodo_pago_usd: str = ""
    metodo_pago_bs: str = ""
    referencia_usd: str = ""
    referencia_bs: str = ""
    descuento_usd: str = "0"
    motivo_descuento: str = ""
    aplicar_descuento: bool = False
    notas: str = ""

    # Tasa de cambio
    tasa_cambio: float = 36.50

    # Validación y estado
    errores: Dict[str, str] = {}
    procesando: bool = False

    # Computed: Totales calculados
    @rx.var
    def total_usd_calculado(self) -> float:
        """Total en USD después de descuento"""
        try:
            if not self.consulta_seleccionada:
                return 0.0
            total = float(self.consulta_seleccionada.get("total_usd", 0))
            if self.aplicar_descuento and self.descuento_usd:
                total -= float(self.descuento_usd)
            return max(0, total)
        except:
            return 0.0

    @rx.var
    def total_bs_calculado(self) -> float:
        """Total en BS calculado desde USD"""
        return self.total_usd_calculado * self.tasa_cambio

    @rx.var
    def monto_usd_float(self) -> float:
        """Monto pagado en USD"""
        try:
            return float(self.monto_usd) if self.monto_usd else 0.0
        except:
            return 0.0

    @rx.var
    def monto_bs_float(self) -> float:
        """Monto pagado en BS"""
        try:
            return float(self.monto_bs) if self.monto_bs else 0.0
        except:
            return 0.0

    @rx.var
    def equivalente_usd_de_bs(self) -> float:
        """Conversión de BS pagados a USD"""
        if self.tasa_cambio > 0:
            return self.monto_bs_float / self.tasa_cambio
        return 0.0

    @rx.var
    def equivalente_bs_de_usd(self) -> float:
        """Conversión de USD pagados a BS"""
        return self.monto_usd_float * self.tasa_cambio

    @rx.var
    def total_pagado_usd(self) -> float:
        """Total pagado en equivalente USD"""
        return self.monto_usd_float + self.equivalente_usd_de_bs

    @rx.var
    def saldo_pendiente_usd(self) -> float:
        """Saldo pendiente en USD"""
        return max(0, self.total_usd_calculado - self.total_pagado_usd)

    @rx.var
    def formulario_valido(self) -> bool:
        """Validar si el formulario está completo"""
        tiene_pago = (self.monto_usd_float > 0 or self.monto_bs_float > 0)
        tiene_metodo_usd = (not self.monto_usd or bool(self.metodo_pago_usd))
        tiene_metodo_bs = (not self.monto_bs or bool(self.metodo_pago_bs))
        return tiene_pago and tiene_metodo_usd and tiene_metodo_bs

    # Eventos
    def abrir_modal_pago(self, consulta: Dict[str, Any]):
        """Abrir modal con consulta seleccionada"""
        self.consulta_seleccionada = consulta
        self.modal_pago_abierto = True
        self.limpiar_formulario()

    def cerrar_modal_pago(self):
        """Cerrar modal y limpiar"""
        self.modal_pago_abierto = False
        self.consulta_seleccionada = {}
        self.limpiar_formulario()

    def limpiar_formulario(self):
        """Resetear formulario"""
        self.monto_usd = ""
        self.monto_bs = ""
        self.metodo_pago_usd = ""
        self.metodo_pago_bs = ""
        self.referencia_usd = ""
        self.referencia_bs = ""
        self.descuento_usd = "0"
        self.motivo_descuento = ""
        self.aplicar_descuento = False
        self.notas = ""
        self.errores = {}

    def validar_y_procesar_pago(self):
        """Validar y simular procesamiento"""
        self.errores = {}

        # Validaciones
        if self.monto_usd_float <= 0 and self.monto_bs_float <= 0:
            self.errores["monto"] = "Debe ingresar al menos un monto"
            return

        if self.monto_usd_float > 0 and not self.metodo_pago_usd:
            self.errores["metodo_usd"] = "Seleccione método de pago USD"
            return

        if self.monto_bs_float > 0 and not self.metodo_pago_bs:
            self.errores["metodo_bs"] = "Seleccione método de pago BS"
            return

        if self.total_pagado_usd > self.total_usd_calculado:
            self.errores["monto"] = "El pago excede el total"
            return

        # Simular procesamiento
        self.procesando = True
        return PagosMockupState.confirmar_pago

    def confirmar_pago(self):
        """Confirmar pago (simulado)"""
        self.procesando = False
        # En producción: guardar en BD
        yield rx.toast.success(
            f"Pago procesado: ${self.total_pagado_usd:.2f} USD",
            position="top-right",
            duration=3000
        )
        self.cerrar_modal_pago()
