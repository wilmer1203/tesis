"""
Servicio centralizado para gestión de pagos y facturación
Sigue el mismo patrón que ServiciosService
"""

from typing import Dict, List, Optional, Any
from decimal import Decimal
from datetime import date, datetime
from .base_service import BaseService
from dental_system.supabase.tablas import payments_table
from dental_system.models import PagoModel
from .cache_invalidation_hooks import invalidate_after_payment_operation, track_cache_invalidation
import logging

logger = logging.getLogger(__name__)

class PagosService(BaseService):
    """
    Servicio que maneja toda la lógica de pagos y facturación
    Usado por Administrador y Gerente según permisos
    """
    
    def __init__(self):
        super().__init__()
        self.table = payments_table
    
    async def get_filtered_payments(self, 
                                  search: str = None, 
                                  estado: str = None, 
                                  metodo_pago: str = None,
                                  fecha_inicio: str = None,
                                  fecha_fin: str = None) -> List[PagoModel]:
        """
        Obtiene pagos filtrados 
        
        Args:
            search: Término de búsqueda (número de recibo, paciente)
            estado: Filtro por estado (completado, pendiente, anulado)
            metodo_pago: Filtro por método de pago
            fecha_inicio: Fecha inicial (YYYY-MM-DD)
            fecha_fin: Fecha final (YYYY-MM-DD)
            
        Returns:
            Lista de pagos como modelos tipados
        """
        try:
            # Verificar permisos
            if not self.check_permission("pagos", "leer"):
                raise PermissionError("Sin permisos para acceder a pagos")
            
            # Obtener datos según filtros
            if fecha_inicio and fecha_fin:
                # Búsqueda por rango de fechas
                fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
                pagos_data = self.table.get_payments_by_date_range(
                    fecha_inicio_obj, fecha_fin_obj, metodo_pago, estado
                )
            elif search and search.strip():
                # Búsqueda por número de recibo
                if search.startswith("REC"):
                    pago = self.table.get_by_recibo(search.strip())
                    pagos_data = [pago] if pago else []
                else:
                    # TODO: Implementar búsqueda por nombre de paciente
                    pagos_data = self.table.get_all()
            elif estado == "pendiente":
                pagos_data = self.table.get_pending_payments()
            else:
                # Obtener todos con filtros básicos
                pagos_data = self.table.get_all()
            
            # Aplicar filtros adicionales si es necesario
            if estado and not fecha_inicio:
                pagos_data = [p for p in pagos_data if p.get("estado_pago") == estado]
            
            if metodo_pago and not fecha_inicio:
                pagos_data = [p for p in pagos_data if p.get("metodo_pago") == metodo_pago]
            
            # Convertir a modelos tipados
            pagos_models = []
            for item in pagos_data:
                try:
                    model = PagoModel.from_dict(item)
                    pagos_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo pago: {e}")
                    continue
            
            logger.info(f"✅ Pagos obtenidos: {len(pagos_models)} registros")
            return pagos_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a pagos")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo pagos filtrados", e)
            return []
    
    async def create_payment(self, form_data: Dict[str, str], user_id: str) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo pago
        
        Args:
            form_data: Datos del formulario
            user_id: ID del usuario que crea
            
        Returns:
            Pago creado o None si hay error
        """
        try:
            logger.info("Creando nuevo pago")
            
            # Verificar permisos
            self.require_permission("pagos", "crear")
            
            # Validar campos requeridos
            required_fields = ["paciente_id", "monto_total", "monto_pagado", "concepto", "metodo_pago"]
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)
            
            # Procesar montos
            try:
                monto_total = Decimal(str(form_data["monto_total"]))
                monto_pagado = Decimal(str(form_data["monto_pagado"]))
                descuento_aplicado = Decimal(str(form_data.get("descuento_aplicado", "0")))
                impuestos = Decimal(str(form_data.get("impuestos", "0")))
            except (ValueError, TypeError) as e:
                raise ValueError(f"Formato de monto inválido: {e}")
            
            # Validar montos
            if monto_pagado > monto_total:
                raise ValueError("El monto pagado no puede ser mayor al monto total")
            
            if monto_total <= 0:
                raise ValueError("El monto total debe ser mayor a cero")
            
            # Crear pago usando el método de la tabla
            result = self.table.create_payment(
                paciente_id=form_data["paciente_id"],
                monto_total=monto_total,
                monto_pagado=monto_pagado,
                concepto=form_data["concepto"].strip(),
                procesado_por=user_id,
                consulta_id=form_data.get("consulta_id") if form_data.get("consulta_id") else None,
                metodo_pago=form_data["metodo_pago"],
                referencia_pago=form_data.get("referencia_pago", "").strip() or None,
                descuento_aplicado=descuento_aplicado,
                motivo_descuento=form_data.get("motivo_descuento", "").strip() or None,
                impuestos=impuestos,
                autorizado_por=form_data.get("autorizado_por") if form_data.get("autorizado_por") else None,
                observaciones=form_data.get("observaciones", "").strip() or None
            )
            
            if result:
                logger.info(f"✅ Pago creado: {result.get('numero_recibo', '???')} - ${monto_pagado}")
                
                # 🗑️ INVALIDAR CACHE - pago creado afecta estadísticas financieras
                try:
                    invalidate_after_payment_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras crear pago: {cache_error}")
                
                return result
            else:
                raise ValueError("Error creando pago en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para crear pagos")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error creando pago", e)
            raise ValueError(f"Error inesperado: {str(e)}")

    async def create_dual_payment(self, form_data: Dict[str, str], user_id: str) -> Optional[Dict[str, Any]]:
        """
        Crear pago con sistema dual USD/BS

        Args:
            form_data: Datos del formulario dual
            user_id: ID del usuario que crea

        form_data esperado:
        {
            "paciente_id": "...",
            "monto_total_usd": "100.00",
            "pago_usd": "50.00",
            "pago_bs": "1825.00",
            "tasa_cambio_del_dia": "36.50",
            "concepto": "Consulta general",
            "metodo_pago_usd": "efectivo",
            "metodo_pago_bs": "transferencia",
            "referencia_usd": "",
            "referencia_bs": "TRF123456"
        }

        Returns:
            Pago creado o None si hay error
        """
        try:
            logger.info("Creando pago dual USD/BS")

            # Verificar permisos
            self.require_permission("pagos", "crear")

            # Validar campos requeridos del sistema dual
            required_fields = ["paciente_id", "monto_total_usd", "concepto", "tasa_cambio_del_dia"]
            missing_fields = self.validate_required_fields(form_data, required_fields)

            if missing_fields:
                error_msg = self.format_error_message("Campos requeridos faltantes", missing_fields)
                raise ValueError(error_msg)

            # Procesar montos duales
            try:
                monto_total_usd = Decimal(str(form_data["monto_total_usd"]))
                pago_usd = Decimal(str(form_data.get("pago_usd", "0")))
                pago_bs = Decimal(str(form_data.get("pago_bs", "0")))
                tasa_cambio = Decimal(str(form_data["tasa_cambio_del_dia"]))
                descuento_usd = Decimal(str(form_data.get("descuento_usd", "0")))
            except (ValueError, TypeError) as e:
                raise ValueError(f"Formato de monto inválido: {e}")

            # Validaciones de negocio
            if monto_total_usd <= 0:
                raise ValueError("El monto total debe ser mayor a cero")

            if tasa_cambio <= 0:
                raise ValueError("La tasa de cambio debe ser mayor a cero")

            if pago_usd < 0 or pago_bs < 0:
                raise ValueError("Los pagos no pueden ser negativos")

            # Validar que al menos haya un pago
            if pago_usd <= 0 and pago_bs <= 0:
                raise ValueError("Debe especificar al menos un monto de pago")

            # Construir array de métodos de pago
            metodos_pago = []

            if pago_usd > 0:
                metodos_pago.append({
                    "tipo": form_data.get("metodo_pago_usd", "efectivo"),
                    "moneda": "USD",
                    "monto": float(pago_usd),
                    "referencia": form_data.get("referencia_usd", "").strip() or None
                })

            if pago_bs > 0:
                metodos_pago.append({
                    "tipo": form_data.get("metodo_pago_bs", "efectivo"),
                    "moneda": "BS",
                    "monto": float(pago_bs),
                    "referencia": form_data.get("referencia_bs", "").strip() or None
                })

            # Crear pago usando tabla especializada
            result = self.table.create_dual_payment(
                paciente_id=form_data["paciente_id"],
                monto_total_usd=monto_total_usd,
                pago_usd=pago_usd,
                pago_bs=pago_bs,
                tasa_cambio=tasa_cambio,
                concepto=form_data["concepto"].strip(),
                procesado_por=user_id,
                metodos_pago=metodos_pago,
                consulta_id=form_data.get("consulta_id") if form_data.get("consulta_id") else None,
                descuento_usd=descuento_usd,
                motivo_descuento=form_data.get("motivo_descuento", "").strip() or None,
                autorizado_por=form_data.get("autorizado_por") if form_data.get("autorizado_por") else None,
                observaciones=form_data.get("observaciones", "").strip() or None
            )

            if result:
                logger.info(f"✅ Pago dual creado: ${pago_usd} USD + {pago_bs} BS (Recibo: {result.get('numero_recibo', '???')})")

                # 🗑️ INVALIDAR CACHE - pago dual afecta estadísticas financieras
                try:
                    invalidate_after_payment_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras crear pago dual: {cache_error}")

                return result
            else:
                raise ValueError("Error creando pago dual en la base de datos")

        except PermissionError:
            logger.warning("Usuario sin permisos para crear pagos duales")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación en pago dual: {e}")
            raise
        except Exception as e:
            self.handle_error("Error creando pago dual", e)
            raise ValueError(f"Error inesperado: {str(e)}")

    async def update_payment(self, payment_id: str, form_data: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Actualiza un pago existente (limitado a ciertos campos)
        
        Args:
            payment_id: ID del pago
            form_data: Datos del formulario
            
        Returns:
            Pago actualizado o None si hay error
        """
        try:
            logger.info(f"Actualizando pago: {payment_id}")
            
            # Verificar permisos
            self.require_permission("pagos", "actualizar")
            
            # Obtener pago original
            original = self.table.get_by_id(payment_id)
            if not original:
                raise ValueError("Pago no encontrado")
            
            # Solo permitir actualizar ciertos campos por seguridad
            allowed_updates = {
                "referencia_pago": form_data.get("referencia_pago", "").strip() or None,
                "observaciones": form_data.get("observaciones", "").strip() or None,
            }
            
            # Actualizar
            result = self.table.update(payment_id, allowed_updates)
            
            if result:
                logger.info(f"✅ Pago actualizado: {original.get('numero_recibo', payment_id)}")
                
                # 🗑️ INVALIDAR CACHE - pago actualizado puede afectar estadísticas
                try:
                    invalidate_after_payment_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras actualizar pago: {cache_error}")
                
                return result
            else:
                raise ValueError("Error actualizando pago en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para actualizar pagos")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error actualizando pago", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def cancel_payment(self, payment_id: str, motivo: str, user_id: str) -> bool:
        """
        Anula un pago
        
        Args:
            payment_id: ID del pago
            motivo: Motivo de anulación
            user_id: ID del usuario que autoriza
            
        Returns:
            True si se anuló correctamente
        """
        try:
            logger.info(f"Anulando pago: {payment_id}")
            
            # Verificar permisos
            self.require_permission("pagos", "eliminar")
            
            # Verificar que el pago existe
            pago = self.table.get_by_id(payment_id)
            if not pago:
                raise ValueError("Pago no encontrado")
            
            if pago.get("estado_pago") == "anulado":
                raise ValueError("El pago ya está anulado")
            
            # Anular
            result = self.table.cancel_payment(payment_id, motivo, user_id)
            
            if result:
                logger.info(f"✅ Pago anulado correctamente: {pago.get('numero_recibo')}")
                return True
            else:
                raise ValueError("Error anulando pago")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para anular pagos")
            raise
        except Exception as e:
            self.handle_error("Error anulando pago", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def process_partial_payment(self, payment_id: str, form_data: Dict[str, str], user_id: str) -> Optional[Dict[str, Any]]:
        """
        Procesa un pago parcial
        
        Args:
            payment_id: ID del pago original
            form_data: Datos del pago parcial
            user_id: ID del usuario que procesa
            
        Returns:
            Nuevo pago creado o None si hay error
        """
        try:
            logger.info(f"Procesando pago parcial para: {payment_id}")
            
            # Verificar permisos
            self.require_permission("pagos", "crear")
            
            # Validar campos requeridos
            required_fields = ["monto_adicional", "metodo_pago"]
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)
            
            # Procesar monto
            try:
                monto_adicional = Decimal(str(form_data["monto_adicional"]))
            except (ValueError, TypeError):
                raise ValueError("Monto adicional debe ser un número válido")
            
            if monto_adicional <= 0:
                raise ValueError("El monto adicional debe ser mayor a cero")
            
            # Procesar pago parcial
            result = self.table.process_partial_payment(
                payment_id=payment_id,
                monto_adicional=monto_adicional,
                metodo_pago=form_data["metodo_pago"],
                procesado_por=user_id,
                referencia=form_data.get("referencia_pago", "").strip() or None
            )
            
            if result:
                logger.info(f"✅ Pago parcial procesado: ${monto_adicional}")
                
                # 🗑️ INVALIDAR CACHE - pago parcial afecta ingresos y estadísticas
                try:
                    invalidate_after_payment_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras procesar pago parcial: {cache_error}")
                
                return result
            else:
                raise ValueError("Error procesando pago parcial")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para procesar pagos parciales")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error procesando pago parcial", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def get_payment_by_id(self, payment_id: str) -> Optional[PagoModel]:
        """
        Obtiene un pago por ID con información completa
        
        Args:
            payment_id: ID del pago
            
        Returns:
            Modelo del pago o None
        """
        try:
            # Verificar permisos
            self.require_permission("pagos", "leer")
            
            data = self.table.get_payment_details(payment_id)
            if data:
                return PagoModel.from_dict(data)
            return None
            
        except Exception as e:
            self.handle_error("Error obteniendo pago por ID", e)
            return None
    
    async def get_daily_summary(self, fecha: date = None) -> Dict[str, Any]:
        """
        Obtiene resumen diario de pagos
        
        Args:
            fecha: Fecha a consultar (por defecto hoy)
            
        Returns:
            Resumen del día
        """
        try:
            # Verificar permisos
            self.require_permission("pagos", "leer")
            
            if not fecha:
                fecha = date.today()
            
            summary = self.table.get_daily_summary(fecha)
            logger.info(f"Resumen diario obtenido: {summary.get('total_recaudado', 0)}")
            return summary
            
        except Exception as e:
            self.handle_error("Error obteniendo resumen diario", e)
            return {
                "fecha": fecha.isoformat() if fecha else date.today().isoformat(),
                "total_pagos": 0,
                "total_recaudado": 0,
                "por_metodo": {},
                "pagos_pendientes": 0,
                "pagos_completados": 0,
                "pagos_anulados": 0
            }
    
    async def get_patient_balance(self, paciente_id: str) -> Dict[str, Any]:
        """
        Obtiene el balance de un paciente
        
        Args:
            paciente_id: ID del paciente
            
        Returns:
            Balance del paciente
        """
        try:
            # Verificar permisos
            self.require_permission("pagos", "leer")
            
            balance = self.table.get_patient_balance(paciente_id)
            logger.info(f"Balance obtenido para paciente {paciente_id}")
            return balance
            
        except Exception as e:
            self.handle_error("Error obteniendo balance del paciente", e)
            return {
                "paciente_id": paciente_id,
                "total_facturado": 0,
                "total_pagado": 0,
                "total_descuentos": 0,
                "saldo_pendiente": 0,
                "pagos_completados": 0,
                "pagos_pendientes": 0
            }
    
    async def get_payment_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de pagos
        Usado por dashboard_service pero disponible independientemente
        """
        try:
            # Obtener resumen del día actual
            today_summary = await self.get_daily_summary()
            
            # Obtener pagos pendientes
            pending_payments = self.table.get_pending_payments()
            
            # Calcular estadísticas básicas
            stats = {
                "hoy": {
                    "total_recaudado": today_summary.get("total_recaudado", 0),
                    "total_pagos": today_summary.get("total_pagos", 0),
                    "pagos_completados": today_summary.get("pagos_completados", 0),
                },
                "pendientes": {
                    "cantidad": len(pending_payments),
                    "monto_total": sum(p.get("saldo_pendiente", 0) for p in pending_payments)
                },
                "metodos_populares": today_summary.get("por_metodo", {})
            }
            
            logger.info(f"Estadísticas de pagos: {stats}")
            return stats
            
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de pagos", e)
            return {
                "hoy": {"total_recaudado": 0, "total_pagos": 0, "pagos_completados": 0},
                "pendientes": {"cantidad": 0, "monto_total": 0},
                "metodos_populares": {}
            }

    async def get_currency_stats(self) -> Dict[str, Any]:
        """
        Estadísticas duales USD/BS para dashboard

        Returns:
            Estadísticas completas con ambas monedas
        """
        try:
            # Verificar permisos
            self.require_permission("pagos", "leer")

            # Resumen del día actual con moneda dual
            today_summary = self.table.get_currency_summary()

            # Obtener pagos pendientes
            pending_payments = self.table.get_pending_payments()

            # Tasa promedio de la semana para comparación
            from datetime import timedelta
            week_ago = date.today() - timedelta(days=7)
            week_payments = self.table.get_payments_by_date_range(week_ago, date.today())

            tasas_semana = []
            for pago in week_payments:
                tasa = pago.get("tasa_cambio_bs_usd", 0)
                if tasa > 0:
                    tasas_semana.append(tasa)

            tasa_promedio_semana = round(sum(tasas_semana) / len(tasas_semana), 2) if tasas_semana else 36.50

            # Calcular saldos pendientes duales
            total_pendiente_usd = sum(p.get("saldo_pendiente_usd", p.get("saldo_pendiente", 0)) for p in pending_payments)
            total_pendiente_bs = sum(p.get("saldo_pendiente_bs", 0) for p in pending_payments)

            stats = {
                "hoy": {
                    "total_recaudado_usd": today_summary.get("total_recaudado_usd", 0),
                    "total_recaudado_bs": today_summary.get("total_recaudado_bs", 0),
                    "total_pagos": today_summary.get("total_pagos", 0),
                    "pagos_completados": today_summary.get("pagos_completados", 0),
                    "pagos_pendientes": today_summary.get("pagos_pendientes", 0),
                    "tasa_promedio": today_summary.get("tasa_promedio", 36.50),
                },
                "pendientes": {
                    "cantidad": len(pending_payments),
                    "monto_total_usd": total_pendiente_usd,
                    "monto_total_bs": total_pendiente_bs
                },
                "distribucion_pagos": {
                    "pagos_mixtos": today_summary.get("pagos_mixtos", 0),
                    "pagos_solo_usd": today_summary.get("pagos_solo_usd", 0),
                    "pagos_solo_bs": today_summary.get("pagos_solo_bs", 0)
                },
                "tendencias": {
                    "tasa_promedio_semana": tasa_promedio_semana,
                    "variacion_tasa": round(today_summary.get("tasa_promedio", 36.50) - tasa_promedio_semana, 2),
                    "preferencia_moneda": "USD" if today_summary.get("pagos_solo_usd", 0) > today_summary.get("pagos_solo_bs", 0) else "BS"
                }
            }

            logger.info(f"Estadísticas duales generadas: ${stats['hoy']['total_recaudado_usd']} USD + {stats['hoy']['total_recaudado_bs']} BS")
            return stats

        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de moneda dual", e)
            return {
                "hoy": {"total_recaudado_usd": 0, "total_recaudado_bs": 0, "total_pagos": 0, "pagos_completados": 0, "tasa_promedio": 36.50},
                "pendientes": {"cantidad": 0, "monto_total_usd": 0, "monto_total_bs": 0},
                "distribucion_pagos": {"pagos_mixtos": 0, "pagos_solo_usd": 0, "pagos_solo_bs": 0},
                "tendencias": {"tasa_promedio_semana": 36.50, "variacion_tasa": 0, "preferencia_moneda": "USD"}
            }

    async def get_all_payments(self, estado: str = "todos") -> List[PagoModel]:
        """
        Obtiene todos los pagos (método requerido por estado_pagos)

        Args:
            estado: Filtro por estado (todos, pendiente, completado, anulado)

        Returns:
            Lista de pagos como modelos tipados
        """
        try:
            # Verificar permisos
            if not self.check_permission("pagos", "leer"):
                raise PermissionError("Sin permisos para acceder a pagos")

            # Usar método filtrado para obtener todos los pagos
            estado_filtro = None if estado == "todos" else estado
            return await self.get_filtered_payments(estado=estado_filtro)

        except Exception as e:
            self.handle_error("Error obteniendo todos los pagos", e)
            return []

    async def get_consultas_pendientes_pago(self) -> List[Dict[str, Any]]:
        """
        🏥 Obtener consultas completadas pendientes de facturación

        Returns:
            Lista de consultas con información para facturación
        """
        try:
            # Verificar permisos
            self.require_permission("pagos", "leer")

            # Query especializada para consultas pendientes de pago
            consultas_pendientes = self.table.get_consultas_pendientes_facturacion()

            # Procesar y enriquecer datos para la UI
            consultas_procesadas = []

            for consulta in consultas_pendientes:
                consulta_data = {
                    "consulta_id": consulta.get("id"),
                    "numero_consulta": consulta.get("numero_consulta", "CONS-000"),
                    "paciente_id": consulta.get("paciente_id"),
                    "paciente_nombre": f"{consulta.get('paciente_nombre', '')} {consulta.get('paciente_apellido', '')}".strip(),
                    "paciente_documento": consulta.get("paciente_documento", ""),
                    "odontologo_id": consulta.get("primer_odontologo_id"),
                    "odontologo_nombre": consulta.get("odontologo_nombre", "Dr. Sistema"),
                    "fecha_consulta": consulta.get("fecha_llegada", ""),
                    "servicios_realizados": consulta.get("servicios_detalle", []),
                    "servicios_count": consulta.get("servicios_count", 0),
                    "total_usd": float(consulta.get("total_usd", 0.0)),
                    "total_bs": float(consulta.get("total_bs", 0.0)),
                    "concepto": f"Consulta {consulta.get('numero_consulta', 'CONS-000')} - {consulta.get('servicios_count', 0)} servicios",
                    "estado_consulta": consulta.get("estado", "completada"),
                    "dias_pendiente": consulta.get("dias_pendiente", 0),
                    "prioridad": "alta" if consulta.get("dias_pendiente", 0) > 7 else "normal"
                }
                consultas_procesadas.append(consulta_data)

            # Ordenar por fecha más reciente primero
            consultas_procesadas.sort(
                key=lambda x: x.get("fecha_consulta", ""),
                reverse=True
            )

            logger.info(f"✅ {len(consultas_procesadas)} consultas pendientes de pago obtenidas")
            return consultas_procesadas

        except Exception as e:
            self.handle_error("Error obteniendo consultas pendientes de pago", e)
            return []


# Instancia única para importar
pagos_service = PagosService()