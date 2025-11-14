"""
Servicio centralizado para gestión de pagos y facturación
Sigue el mismo patrón que ServiciosService
"""

from typing import Dict, List, Optional, Any
from decimal import Decimal
from datetime import date, datetime
from .base_service import BaseService
from dental_system.models import PagoModel, ServicioFormateado, ConsultaPendientePago
import logging

logger = logging.getLogger(__name__)

class PagosService(BaseService):
    """
    Servicio que maneja toda la lógica de pagos y facturación
    Usado por Administrador y Gerente según permisos
    """

    def __init__(self):
        super().__init__()
    
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
            query = self.client.table("pago").select("*")

            # Aplicar filtros
            if fecha_inicio and fecha_fin:
                query = query.gte("fecha_pago", fecha_inicio).lte("fecha_pago", fecha_fin)

            if search and search.strip():
                if search.startswith("REC"):
                    query = query.eq("numero_recibo", search.strip())

            if estado:
                query = query.eq("estado_pago", estado)

            if metodo_pago:
                # Búsqueda en array JSONB metodos_pago
                query = query.contains("metodos_pago", [{"tipo": metodo_pago}])

            # Ordenar por fecha descendente
            query = query.order("fecha_pago", desc=True)

            # Ejecutar query
            response = query.execute()
            pagos_data = response.data if response.data else []

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
            
            # Calcular saldo pendiente
            saldo_pendiente_usd = monto_total - monto_pagado
            estado_pago = "completado" if saldo_pendiente_usd <= 0 else "pendiente"

            # Generar número de recibo
            today = datetime.now().strftime("%Y%m%d")
            count_response = self.client.table("pago").select("id", count="exact").like("numero_recibo", f"REC{today}%").execute()
            count = count_response.count if count_response.count else 0
            numero_recibo = f"REC{today}{str(count + 1).zfill(4)}"

            # Construir array de métodos de pago
            metodos_pago = [{
                "tipo": form_data["metodo_pago"],
                "moneda": "USD",
                "monto": float(monto_pagado),
                "referencia": form_data.get("referencia_pago", "").strip() or None
            }]

            # Crear pago directamente
            insert_data = {
                "paciente_id": form_data["paciente_id"],
                "consulta_id": form_data.get("consulta_id") if form_data.get("consulta_id") else None,
                "numero_recibo": numero_recibo,
                "concepto": form_data["concepto"].strip(),
                "monto_total_usd": float(monto_total),
                "monto_pagado_usd": float(monto_pagado),
                "saldo_pendiente_usd": float(saldo_pendiente_usd),
                "estado_pago": estado_pago,
                "metodos_pago": metodos_pago,
                "procesado_por": user_id,
                "motivo_descuento": form_data.get("motivo_descuento", "").strip() or None
            }

            response = self.client.table("pago").insert(insert_data).execute()
            result = response.data[0] if response.data else None

            if result:
                logger.info(f"✅ Pago creado: {result.get('numero_recibo', '???')} - ${monto_pagado}")
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

            # Calcular totales
            pago_usd_equivalente = pago_usd + (pago_bs / tasa_cambio)
            saldo_pendiente_usd = monto_total_usd - pago_usd_equivalente - descuento_usd
            estado_pago = "completado" if saldo_pendiente_usd <= Decimal('0.01') else "pendiente"

            # Calcular montos en BS
            monto_total_bs = monto_total_usd * tasa_cambio
            monto_pagado_bs = pago_bs + (pago_usd * tasa_cambio)
            saldo_pendiente_bs = saldo_pendiente_usd * tasa_cambio

            # Generar número de recibo
            today = datetime.now().strftime("%Y%m%d")
            count_response = self.client.table("pago").select("id", count="exact").like("numero_recibo", f"REC{today}%").execute()
            count = count_response.count if count_response.count else 0
            numero_recibo = f"REC{today}{str(count + 1).zfill(4)}"

            # Crear pago dual directamente
            insert_data = {
                "paciente_id": form_data["paciente_id"],
                "consulta_id": form_data.get("consulta_id") if form_data.get("consulta_id") else None,
                "numero_recibo": numero_recibo,
                "concepto": form_data["concepto"].strip(),
                "monto_total_usd": float(monto_total_usd),
                "monto_total_bs": float(monto_total_bs),
                "monto_pagado_usd": float(pago_usd_equivalente),
                "monto_pagado_bs": float(monto_pagado_bs),
                "saldo_pendiente_usd": float(saldo_pendiente_usd),
                "saldo_pendiente_bs": float(saldo_pendiente_bs),
                "tasa_cambio_bs_usd": float(tasa_cambio),
                "descuento_usd": float(descuento_usd),
                "estado_pago": estado_pago,
                "metodos_pago": metodos_pago,
                "procesado_por": user_id,
                "motivo_descuento": form_data.get("motivo_descuento", "").strip() or None
            }

            response = self.client.table("pago").insert(insert_data).execute()
            result = response.data[0] if response.data else None

            if result:
                logger.info(f"✅ Pago dual creado: ${pago_usd} USD + {pago_bs} BS (Recibo: {result.get('numero_recibo', '???')})")
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

    async def get_pago_by_consulta(self, consulta_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el pago asociado a una consulta

        Args:
            consulta_id: ID de la consulta

        Returns:
            Pago encontrado o None
        """
        try:
            response = self.client.table("pago").select("*").eq("consulta_id", consulta_id).execute()
            if response.data and len(response.data) > 0:
                logger.info(f"✅ Pago encontrado para consulta {consulta_id}")
                return response.data[0]
            else:
                logger.warning(f"⚠️ No se encontró pago para consulta {consulta_id}")
                return None
        except Exception as e:
            logger.error(f"❌ Error buscando pago por consulta: {str(e)}")
            return None

    async def update_payment(self, payment_id: str, form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Actualiza un pago existente

        Args:
            payment_id: ID del pago
            form_data: Datos a actualizar

        Returns:
            Pago actualizado o None si hay error
        """
        try:
            logger.info(f"Actualizando pago: {payment_id}")

            # Verificar permisos
            self.require_permission("pagos", "actualizar")

            # Obtener pago original
            original_response = self.client.table("pago").select("*").eq("id", payment_id).execute()
            if not original_response.data:
                raise ValueError("Pago no encontrado")
            original = original_response.data[0]

            # Preparar datos de actualización (permitir todos los campos del form_data)
            allowed_updates = {}

            # Campos numéricos
            for field in ["monto_pagado_usd", "monto_pagado_bs", "saldo_pendiente_usd",
                         "saldo_pendiente_bs", "tasa_cambio_bs_usd", "descuento_usd", "monto_total_bs"]:
                if field in form_data:
                    allowed_updates[field] = float(form_data[field])

            # Campos de texto
            for field in ["motivo_descuento", "estado_pago"]:
                if field in form_data:
                    allowed_updates[field] = form_data[field]

            # Campo JSONB
            if "metodos_pago" in form_data:
                allowed_updates["metodos_pago"] = form_data["metodos_pago"]

            logger.info(f"Actualizando con datos: {allowed_updates}")

            # Actualizar directamente
            update_response = self.client.table("pago").update(allowed_updates).eq("id", payment_id).execute()
            result = update_response.data[0] if update_response.data else None

            if result:
                logger.info(f"✅ Pago actualizado: {original.get('numero_recibo', payment_id)}")

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
            pago_response = self.client.table("pago").select("*").eq("id", payment_id).execute()
            if not pago_response.data:
                raise ValueError("Pago no encontrado")
            pago = pago_response.data[0]

            if pago.get("estado_pago") == "anulado":
                raise ValueError("El pago ya está anulado")

            # Anular directamente
            update_data = {
                "estado_pago": "anulado",
                "motivo_descuento": motivo  # Usar este campo para motivo de anulación
            }

            update_response = self.client.table("pago").update(update_data).eq("id", payment_id).execute()
            result = update_response.data[0] if update_response.data else None

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

            # Obtener pago original
            pago_response = self.client.table("pago").select("*").eq("id", payment_id).execute()
            if not pago_response.data:
                raise ValueError("Pago no encontrado")
            pago = pago_response.data[0]

            # Calcular nuevos saldos
            monto_pagado_actual = Decimal(str(pago.get("monto_pagado_usd", 0)))
            nuevo_monto_pagado = monto_pagado_actual + monto_adicional

            saldo_pendiente_usd = Decimal(str(pago.get("saldo_pendiente_usd", 0)))
            nuevo_saldo = saldo_pendiente_usd - monto_adicional

            nuevo_estado = "completado" if nuevo_saldo <= Decimal('0.01') else "pendiente"

            # Actualizar metodos_pago
            metodos_pago = pago.get("metodos_pago", [])
            metodos_pago.append({
                "tipo": form_data["metodo_pago"],
                "moneda": "USD",
                "monto": float(monto_adicional),
                "referencia": form_data.get("referencia_pago", "").strip() or None
            })

            # Actualizar pago
            update_data = {
                "monto_pagado_usd": float(nuevo_monto_pagado),
                "saldo_pendiente_usd": float(nuevo_saldo),
                "estado_pago": nuevo_estado,
                "metodos_pago": metodos_pago
            }

            update_response = self.client.table("pago").update(update_data).eq("id", payment_id).execute()
            result = update_response.data[0] if update_response.data else None

            if result:
                logger.info(f"✅ Pago parcial procesado: ${monto_adicional}")

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

            response = self.client.table("pago").select("*").eq("id", payment_id).execute()
            if response.data:
                return PagoModel.from_dict(response.data[0])
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

            # Obtener pagos del día
            fecha_str = fecha.isoformat()
            response = self.client.table("pago").select("*").gte("fecha_pago", fecha_str).lt("fecha_pago", f"{fecha_str}T23:59:59").execute()
            pagos = response.data if response.data else []

            # Calcular estadísticas
            total_recaudado = sum(p.get("monto_pagado_usd", 0) for p in pagos)
            completados = [p for p in pagos if p.get("estado_pago") == "completado"]
            pendientes = [p for p in pagos if p.get("estado_pago") == "pendiente"]
            anulados = [p for p in pagos if p.get("estado_pago") == "anulado"]

            # Agrupar por método de pago
            por_metodo = {}
            for pago in pagos:
                metodos = pago.get("metodos_pago", [])
                for metodo in metodos:
                    tipo = metodo.get("tipo", "efectivo")
                    por_metodo[tipo] = por_metodo.get(tipo, 0) + metodo.get("monto", 0)

            summary = {
                "fecha": fecha.isoformat(),
                "total_pagos": len(pagos),
                "total_recaudado": total_recaudado,
                "por_metodo": por_metodo,
                "pagos_pendientes": len(pendientes),
                "pagos_completados": len(completados),
                "pagos_anulados": len(anulados)
            }

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

            # Obtener todos los pagos del paciente
            response = self.client.table("pago").select("*").eq("paciente_id", paciente_id).execute()
            pagos = response.data if response.data else []

            # Calcular balance
            total_facturado = sum(p.get("monto_total_usd", 0) for p in pagos if p.get("estado_pago") != "anulado")
            total_pagado = sum(p.get("monto_pagado_usd", 0) for p in pagos if p.get("estado_pago") != "anulado")
            total_descuentos = sum(p.get("descuento_usd", 0) for p in pagos if p.get("estado_pago") != "anulado")
            saldo_pendiente = sum(p.get("saldo_pendiente_usd", 0) for p in pagos if p.get("estado_pago") == "pendiente")

            completados = len([p for p in pagos if p.get("estado_pago") == "completado"])
            pendientes = len([p for p in pagos if p.get("estado_pago") == "pendiente"])

            balance = {
                "paciente_id": paciente_id,
                "total_facturado": total_facturado,
                "total_pagado": total_pagado,
                "total_descuentos": total_descuentos,
                "saldo_pendiente": saldo_pendiente,
                "pagos_completados": completados,
                "pagos_pendientes": pendientes
            }

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

            # Obtener pagos pendientes directamente
            pending_response = self.client.table("pago").select("*").eq("estado_pago", "pendiente").execute()
            pending_payments = pending_response.data if pending_response.data else []

            # Calcular estadísticas básicas
            stats = {
                "hoy": {
                    "total_recaudado": today_summary.get("total_recaudado", 0),
                    "total_pagos": today_summary.get("total_pagos", 0),
                    "pagos_completados": today_summary.get("pagos_completados", 0),
                },
                "pendientes": {
                    "cantidad": len(pending_payments),
                    "monto_total": sum(p.get("saldo_pendiente_usd", 0) for p in pending_payments)
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

            # Obtener pagos del día actual
            today = date.today()
            today_str = today.isoformat()
            today_response = self.client.table("pago").select("*").gte("fecha_pago", today_str).lt("fecha_pago", f"{today_str}T23:59:59").execute()
            today_payments = today_response.data if today_response.data else []

            # Calcular totales del día
            total_recaudado_usd = sum(p.get("monto_pagado_usd", 0) for p in today_payments)
            total_recaudado_bs = sum(p.get("monto_pagado_bs", 0) for p in today_payments)
            completados = len([p for p in today_payments if p.get("estado_pago") == "completado"])
            pendientes = len([p for p in today_payments if p.get("estado_pago") == "pendiente"])

            # Calcular tasa promedio del día
            tasas_hoy = [p.get("tasa_cambio_bs_usd", 0) for p in today_payments if p.get("tasa_cambio_bs_usd", 0) > 0]
            tasa_promedio_hoy = round(sum(tasas_hoy) / len(tasas_hoy), 2) if tasas_hoy else 36.50

            # Obtener pagos pendientes
            pending_response = self.client.table("pago").select("*").eq("estado_pago", "pendiente").execute()
            pending_payments = pending_response.data if pending_response.data else []

            # Tasa promedio de la semana para comparación
            from datetime import timedelta
            week_ago = today - timedelta(days=7)
            week_ago_str = week_ago.isoformat()
            week_response = self.client.table("pago").select("*").gte("fecha_pago", week_ago_str).lte("fecha_pago", today_str).execute()
            week_payments = week_response.data if week_response.data else []

            tasas_semana = [p.get("tasa_cambio_bs_usd", 0) for p in week_payments if p.get("tasa_cambio_bs_usd", 0) > 0]
            tasa_promedio_semana = round(sum(tasas_semana) / len(tasas_semana), 2) if tasas_semana else 36.50

            # Calcular saldos pendientes duales
            total_pendiente_usd = sum(p.get("saldo_pendiente_usd", 0) for p in pending_payments)
            total_pendiente_bs = sum(p.get("saldo_pendiente_bs", 0) for p in pending_payments)

            # Clasificar tipos de pago
            pagos_mixtos = 0
            pagos_solo_usd = 0
            pagos_solo_bs = 0

            for pago in today_payments:
                usd = pago.get("monto_pagado_usd", 0)
                bs = pago.get("monto_pagado_bs", 0)
                tasa = pago.get("tasa_cambio_bs_usd", 36.50)

                usd_from_bs = bs / tasa if tasa > 0 else 0

                if usd > 0 and bs > 0:
                    pagos_mixtos += 1
                elif usd > usd_from_bs:
                    pagos_solo_usd += 1
                elif bs > 0:
                    pagos_solo_bs += 1

            stats = {
                "hoy": {
                    "total_recaudado_usd": total_recaudado_usd,
                    "total_recaudado_bs": total_recaudado_bs,
                    "total_pagos": len(today_payments),
                    "pagos_completados": completados,
                    "pagos_pendientes": pendientes,
                    "tasa_promedio": tasa_promedio_hoy,
                },
                "pendientes": {
                    "cantidad": len(pending_payments),
                    "monto_total_usd": total_pendiente_usd,
                    "monto_total_bs": total_pendiente_bs
                },
                "distribucion_pagos": {
                    "pagos_mixtos": pagos_mixtos,
                    "pagos_solo_usd": pagos_solo_usd,
                    "pagos_solo_bs": pagos_solo_bs
                },
                "tendencias": {
                    "tasa_promedio_semana": tasa_promedio_semana,
                    "variacion_tasa": round(tasa_promedio_hoy - tasa_promedio_semana, 2),
                    "preferencia_moneda": "USD" if pagos_solo_usd > pagos_solo_bs else "BS"
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

    async def get_consultas_pendientes_pago(self) -> List[ConsultaPendientePago]:
        try:

            self.require_permission("pagos", "leer")

            # Query directa a consultas completadas con pago pendiente
            # Obtener consultas completadas
            consultas_response = self.client.table("consulta").select(
                "*, paciente(*), personal!primer_odontologo_id(*)"
            ).eq("estado", "completada").execute()
            consultas = consultas_response.data if consultas_response.data else []

            # Filtrar las que tienen pago pendiente
            consultas_pendientes = []
            for consulta in consultas:
                # Verificar si tiene pago pendiente
                pago_response = self.client.table("pago").select("*").eq("consulta_id", consulta["id"]).eq("estado_pago", "pendiente").execute()
                if pago_response.data:
                    # ✅ CORRECCIÓN: Obtener intervenciones con información del odontólogo
                    intervenciones_response = self.client.table("intervencion").select(
                        "id, odontologo_id, personal!odontologo_id(primer_nombre, primer_apellido)"
                    ).eq("consulta_id", consulta["id"]).execute()
                    intervenciones = intervenciones_response.data if intervenciones_response.data else []

                    # ✅ CORRECCIÓN: Obtener servicios a través de historia_medica
                    servicios_detalle = []
                    for interv in intervenciones:
                        historia_response = self.client.table("historia_medica").select(
                            "*, servicio(nombre, precio_base_usd)"
                        ).eq("intervencion_id", interv["id"]).execute()

                        if historia_response.data:
                            for historia in historia_response.data:
                                servicios_detalle.append({
                                    "nombre": historia.get("servicio", {}).get("nombre", "Servicio"),
                                    "odontologo": f"{interv.get('personal', {}).get('primer_nombre', '')} {interv.get('personal', {}).get('primer_apellido', '')}".strip(),
                                    "precio_usd": historia.get("precio_unitario_usd", 0),
                                    "precio_bs": historia.get("precio_unitario_bs", 0)
                                })

                    # Construir objeto consulta con información completa
                    consulta_completa = {
                        "id": consulta["id"],
                        "numero_consulta": consulta.get("numero_consulta", ""),
                        "paciente_id": consulta.get("paciente_id", ""),
                        "paciente_nombre": f"{consulta.get('paciente', {}).get('primer_nombre', '')} {consulta.get('paciente', {}).get('primer_apellido', '')}".strip(),
                        "paciente_documento": consulta.get("paciente", {}).get("numero_documento", ""),
                        "paciente_numero_historia": consulta.get("paciente", {}).get("numero_historia", ""),
                        "paciente_telefono": consulta.get("paciente", {}).get("celular_1", ""),
                        "odontologo_nombre": f"{consulta.get('personal', {}).get('primer_nombre', '')} {consulta.get('personal', {}).get('primer_apellido', '')}".strip(),
                        "fecha_llegada": consulta.get("fecha_llegada", ""),
                        "total_usd": pago_response.data[0].get("monto_total_usd", 0),
                        "total_bs": pago_response.data[0].get("monto_total_bs", 0),
                        "pagos": pago_response.data,
                        "servicios_detalle": servicios_detalle
                    }
                    consultas_pendientes.append(consulta_completa)

            resultado: List[ConsultaPendientePago] = []
            
            for consulta in consultas_pendientes:
                # Calcular días pendientes
                fecha_consulta_str = consulta.get("fecha_consulta", "")
                dias_pendiente = 0
                if fecha_consulta_str:
                    try:
                        if isinstance(fecha_consulta_str, str):
                            fecha_consulta = datetime.fromisoformat(fecha_consulta_str.replace('Z', '+00:00')).date()
                        else:
                            fecha_consulta = fecha_consulta_str
                        dias_pendiente = (date.today() - fecha_consulta).days
                    except:
                        dias_pendiente = 0

                # Determinar prioridad
                if dias_pendiente > 3:
                    prioridad = "alta"
                elif dias_pendiente > 0:
                    prioridad = "media"
                else:
                    prioridad = "baja"
                servicios_detalle_raw = consulta.get("servicios_detalle", [])  # ✅ CORREGIDO: era servicios_realizados
                servicios_count = len(servicios_detalle_raw)

                # ✅ FORMATEAR SERVICIOS PARA UI (lista tipada con modelo)
                servicios_formateados: List[ServicioFormateado] = []
                for srv in servicios_detalle_raw:
                    servicios_formateados.append(ServicioFormateado(
                        nombre=str(srv.get("nombre", "Servicio")),
                        odontologo=str(srv.get("odontologo", "Odontólogo")),
                        precio_usd=f"{float(srv.get('precio_usd', 0)):.2f}",
                        precio_bs=f"{float(srv.get('precio_bs', 0)):,.0f}"
                    ))

                # 🔍 EXTRAER PAGO_ID del array de pagos
                pagos_array = consulta.get("pagos", [])
                pago_id = ""
                if pagos_array and len(pagos_array) > 0:
                    pago_id = str(pagos_array[0].get("id", ""))

                # ✅ CREAR INSTANCIA DEL MODELO (no diccionario)
                resultado.append(ConsultaPendientePago(
                    pago_id=pago_id,  # ✅ ID del pago pendiente
                    consulta_id=consulta.get("id", ""),
                    numero_consulta=consulta.get("numero_consulta", ""),
                    paciente_id=consulta.get("paciente_id", ""),
                    paciente_nombre=consulta.get("paciente_nombre", ""),
                    paciente_documento=consulta.get("paciente_documento", ""),
                    paciente_numero_historia=consulta.get("paciente_numero_historia", ""),  # ✨ NUEVO
                    paciente_telefono=consulta.get("paciente_telefono", ""),  # ✨ NUEVO
                    odontologo_nombre=consulta.get("odontologo_nombre", ""),
                    fecha_consulta=consulta.get("fecha_llegada", ""),
                    dias_pendiente=dias_pendiente,
                    prioridad=prioridad,
                    servicios_count=servicios_count,
                    total_usd=float(consulta.get("total_usd", 0)),
                    total_bs=float(consulta.get("total_bs", 0)),
                    servicios_formateados=servicios_formateados  # ✅ Lista tipada
                ))
            return resultado
        except Exception as e: 
            self.handle_error("Error obteniendo consultas pendientes de pago", e)
            return [] 
     

# Instancia única para importar
pagos_service = PagosService()