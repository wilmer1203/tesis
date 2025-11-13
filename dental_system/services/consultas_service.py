"""
Servicio centralizado para gestión de consultas/citas
Elimina duplicación entre boss_state y admin_state
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from .base_service import BaseService
from dental_system.models import ConsultaModel, ConsultaFormModel
import logging

logger = logging.getLogger(__name__)

class ConsultasService(BaseService):
    """
    Servicio que maneja toda la lógica de consultas/citas
    Usado tanto por Boss (vista) como Admin (CRUD completo)
    """
    
    def __init__(self):
        super().__init__()
    
    async def get_today_consultations(self,odontologo_id: str = None) -> List[ConsultaModel]:
        """
        Obtiene consultas del día 
        Args:
            odontologo_id: Filtrar por odontólogo (opcional)   
        Returns:
            Lista de consultas del día
        """
        try:
            logger.info("Obteniendo consultas del día")
            
            # Verificar permisos
            self.require_permission("consultas", "leer")
            
            # Query directa a consultas del día
            today = date.today().isoformat()

            # Intentar usar vista optimizada primero
            try:
                query = self.client.table("vista_consultas_dia").select("*")

                if odontologo_id:
                    query = query.eq("primer_odontologo_id", odontologo_id)

                response = query.execute()
                consultas_data = response.data if response.data else []

            except Exception as vista_error:
                # Fallback a tabla consultas
                logger.debug(f"Vista no disponible, usando tabla consultas: {vista_error}")

                query = self.client.table("consulta").select("*, paciente(*), personal!primer_odontologo_id(*)").gte(
                    "fecha_llegada", f"{today}T00:00:00"
                ).lt(
                    "fecha_llegada", f"{today}T23:59:59"
                )

                if odontologo_id:
                    query = query.eq("primer_odontologo_id", odontologo_id)

                query = query.order("orden_cola_odontologo")

                response = query.execute()
                consultas_data = response.data if response.data else []
            
            # Convertir a modelos tipados
            consultas_models = []
            for i, item in enumerate(consultas_data, 1):
                try:
                    # Asegurar que tenga orden de llegada
                    if not item.get('orden_cola_odontologo'):
                        item['orden_cola_odontologo'] = i
                    
                    model = ConsultaModel.from_dict(item)
                    consultas_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo consulta: {e}")
                    continue
            
            print(f"✅ Consultas del día obtenidas: {len(consultas_models)} registros")
            return consultas_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a consultas")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo consultas del día", e)
            return []
    

    
    async def create_consultation(self, consulta_data: Dict[str, Any] = None) -> Optional[ConsultaModel]:
        """
        Crea nueva consulta por orden de llegada - ESQUEMA v4.1
        
        Args:
            consulta_data: Datos de la consulta (Dict o ConsultaFormModel)
            user_id: ID del usuario que crea
            
        Returns:
            ConsultaModel creada o None si hay error
        """
        try:
            print("🏥 Creando nueva consulta por orden de llegada...")
            
            # # Manejar tanto Dict como ConsultaFormModel (compatibilidad)
            # if hasattr(consulta_data, 'validate_form'):
            #     # Es ConsultaFormModel
            #     validation_errors = consulta_data.validate_form()
            #     if validation_errors:
            #         error_msg = f"Errores de validación: {validation_errors}"
            #         raise ValueError(error_msg)
                
            #     datos_consulta = {
            #         "paciente_id": consulta_data.paciente_id,
            #         "primer_odontologo_id": consulta_data.primer_odontologo_id,
            #         "motivo_consulta": consulta_data.motivo_consulta,
            #         "observaciones": consulta_data.observaciones,
            #         "tipo_consulta": consulta_data.tipo_consulta or "general",
            #     }
            # else:
            #     # Es Dict (compatibilidad backward)
            #     datos_consulta = consulta_data or {}
            
            # Crear consulta con esquema v4.1 - INSERT directo
            consulta_data = {
                "paciente_id": consulta_data["paciente_id"],
                "primer_odontologo_id": consulta_data.get("primer_odontologo_id") or datos_consulta.get("odontologo_id"),
                "fecha_llegada": datetime.now().isoformat(),
                "estado": "en_espera",  # Estado inicial v4.1
                "tipo_consulta": consulta_data.get("tipo_consulta", "primera_vez"),  # ✅ Corregido: default debe ser "primera_vez" según constraint
                "motivo_consulta": consulta_data.get("motivo_consulta"),
                "observaciones": consulta_data.get("observaciones"),
            }
            print("🆕 Datos de nueva consulta antes de ingresar:", consulta_data)
            response = self.client.table("consulta").insert(consulta_data).execute()
            print("🆕 Datos de nueva consulta:", response)
            result = response.data[0] if response.data else None
            
            if result:
                # Crear modelo tipado del resultado
                consulta_model = ConsultaModel.from_dict(result)
                
                logger.info(f"✅ Consulta creada: {consulta_model.numero_consulta}")
   
                return consulta_model
            else:
                raise ValueError("Error creando consulta en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para crear consultas")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error creando consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def update_consultation(self, consultation_id: str, consulta_form: ConsultaFormModel) -> Optional[ConsultaModel]:
        """
        Actualiza una consulta existente
        
        Args:
            consultation_id: ID de la consulta
            consulta_form: Formulario tipado de consulta
            
        Returns:
            ConsultaModel actualizada o None si hay error
        """
        try:
            logger.info(f"Actualizando consulta: {consultation_id}")
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Validar formulario tipado
            validation_errors = consulta_form.validate_form()
            if validation_errors:
                error_msg = f"Errores de validación: {validation_errors}"
                raise ValueError(error_msg)
        
            # Preparar datos de actualización
            data = {
                "motivo_consulta": consulta_form.motivo_consulta if consulta_form.motivo_consulta else None,
                "observaciones": consulta_form.observaciones if consulta_form.observaciones else None,
                "tipo_consulta": consulta_form.tipo_consulta or "general",
                "prioridad": consulta_form.prioridad or "normal"
            }
            
            # Permitir actualización del estado si está presente
            if hasattr(consulta_form, 'estado') and consulta_form.estado:
                data["estado"] = consulta_form.estado
                logger.info(f"[DEBUG] Actualizando estado a: {consulta_form.estado}")
            
            # Solo permitir cambiar odontólogo si está en estado programada o en_espera
            response = self.client.table("consulta").select("*").eq("id", consultation_id).execute()
            current_consulta = response.data[0] if response.data else None

            if current_consulta and current_consulta.get("estado") in ["programada", "en_espera"]:
                # Usar el campo correcto del esquema v4.1
                nuevo_odontologo = consulta_form.primer_odontologo_id or getattr(consulta_form, 'odontologo_id', None)
                odontologo_actual = current_consulta.get("primer_odontologo_id") or current_consulta.get("odontologo_id")

                if nuevo_odontologo and nuevo_odontologo != odontologo_actual:
                    data["primer_odontologo_id"] = nuevo_odontologo
                    logger.info(f"[DEBUG] ✅ Cambiando odontólogo de {odontologo_actual} a {nuevo_odontologo}")
                else:
                    logger.info(f"[DEBUG] ❌ No se cambiará odontólogo: nuevo={nuevo_odontologo}, actual={odontologo_actual}")

            # UPDATE directo
            update_response = self.client.table("consulta").update(data).eq("id", consultation_id).execute()
            result = update_response.data[0] if update_response.data else None
            
            if result:
                # Crear modelo tipado del resultado
                consulta_model = ConsultaModel.from_dict(result)

                return consulta_model
            else:
                raise ValueError("Error actualizando consulta")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para actualizar consultas")
            raise
        except Exception as e:
            self.handle_error("Error actualizando consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")


    async def transferir_consulta(self,
                                 consulta_id: str,
                                 nuevo_odontologo_id: str,
                                 motivo: str) -> bool:
        """
        Transferir consulta de un odontólogo a otro

        Args:
            consulta_id: ID de la consulta
            nuevo_odontologo_id: ID del nuevo odontólogo
            motivo: Motivo de la transferencia (OBLIGATORIO)

        Returns:
            True si la transferencia fue exitosa
        """
        try:
            logger.info(f"Transfiriendo consulta {consulta_id} a odontólogo {nuevo_odontologo_id}")

            # Verificar permisos
            self.require_permission("consultas", "actualizar")

            # VALIDACIÓN OBLIGATORIA: Motivo requerido
            if not motivo or motivo.strip() == "":
                raise ValueError("El motivo de transferencia es obligatorio")

            # Actualizar directamente la consulta en la tabla principal
            current_time = datetime.now().isoformat()
            observaciones_previas = ""

            # Obtener observaciones actuales
            response = self.client.table("consulta").select("observaciones").eq("id", consulta_id).execute()
            consulta_actual = response.data[0] if response.data else None
            if consulta_actual and consulta_actual.get('observaciones'):
                observaciones_previas = consulta_actual['observaciones'] + "\n\n"

            update_data = {
                'primer_odontologo_id': nuevo_odontologo_id,
                'observaciones': f"{observaciones_previas}TRANSFERENCIA: {motivo} - {current_time}"
            }

            update_response = self.client.table("consulta").update(update_data).eq("id", consulta_id).execute()
            consulta_actualizada = update_response.data[0] if update_response.data else None

            if consulta_actualizada:
                logger.info(f"✅ Consulta {consulta_id} transferida exitosamente")
                return True
            else:
                raise ValueError("Error actualizando consulta en transferencia")

        except ValueError as ve:
            logger.warning(f"Error de validación en transferencia: {str(ve)}")
            raise
        except Exception as e:
            self.handle_error("Error transfiriendo consulta", e)
            return False


    async def change_consultation_status(self, consultation_id: str, nuevo_estado: str, notas: str = None) -> bool:
        """
        Cambia el estado de una consulta
        
        Args:
            consultation_id: ID de la consulta
            nuevo_estado: Nuevo estado
            notas: Notas adicionales
            
        Returns:
            True si se cambió correctamente
        """
        try:
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Validar transición de estado
            response = self.client.table("consulta").select("estado").eq("id", consultation_id).execute()
            consulta_actual = response.data[0] if response.data else None
            print(consulta_actual)
            if consulta_actual.get("estado") != "en_atencion":
                if consulta_actual and not self._is_valid_status_transition(consulta_actual.get("estado"), nuevo_estado):
                    raise ValueError(f"Transición de estado no válida")

            # UPDATE estado con notas
            update_data = {"estado": nuevo_estado}
            if notas:
                update_data["observaciones"] = notas

            update_response = self.client.table("consulta").update(update_data).eq("id", consultation_id).execute()
            result = update_response.data[0] if update_response.data else None
            
            if result:
                logger.info(f"✅ Estado de consulta cambiado a: {nuevo_estado}")
      
                return True
            else:
                raise ValueError("Error cambiando estado de consulta")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para cambiar estado de consultas")
            raise
        except Exception as e:
            self.handle_error("Error cambiando estado de consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    def _is_valid_status_transition(self, estado_actual: str, nuevo_estado: str) -> bool:
        """Validar transición de estado usando esquema v4.1"""
        # ✅ TRANSICIONES VÁLIDAS ESQUEMA v4.1
        valid_transitions = {
            "en_espera": ["en_atencion", "cancelada"],            # Espera → Atención o Cancelar
            "en_atencion": ["completada", "entre_odontologos", "cancelada"],  # Atención → Completar, Transferir o Cancelar
            "entre_odontologos": ["en_atencion", "en_espera"],    # Transferencia → Volver a atención o espera
            "completada": [],                                      # Estado final
            "cancelada": ["en_espera"],                           # Cancelada → Puede reactivarse
            
            # ✅ COMPATIBILITY con estados anteriores
            "programada": ["en_atencion", "en_espera", "cancelada", "no_asistio"],
            "en_progreso": ["completada", "en_atencion", "cancelada"],
            "no_asistio": ["en_espera", "programada"]
        }
        
        return nuevo_estado in valid_transitions.get(estado_actual, [])
    
    
    
    async def get_consultation_by_id(self, consultation_id: str) -> Optional[ConsultaModel]:
        """
        Obtiene una consulta por ID con información completa
        
        Args:
            consultation_id: ID de la consulta
            
        Returns:
            Modelo de la consulta o None
        """
        try:
            # Verificar permisos
            self.require_permission("consultas", "leer")

            # Query con detalles completos (JOIN a pacientes y personal/odontólogos)
            response = self.client.table("consulta").select("*, paciente(*), personal!primer_odontologo_id(*)").eq("id", consultation_id).execute()
            data = response.data[0] if response.data else None

            if data:
                return ConsultaModel.from_dict(data)
            return None
            
        except Exception as e:
            self.handle_error("Error obteniendo consulta por ID", e)
            return None



    async def cancel_consultation(self, consultation_id: str, motivo: str = None) -> bool:
        """
        Cancela una consulta con motivo específico
        
        Args:
            consultation_id: ID de la consulta
            motivo: Motivo de la cancelación
            
        Returns:
            True si se canceló correctamente
        """
        try:
            logger.info(f"Cancelando consulta: {consultation_id}")
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Obtener consulta actual para validar
            response = self.client.table("consulta").select("estado").eq("id", consultation_id).execute()
            consulta_actual = response.data[0] if response.data else None
            if not consulta_actual:
                raise ValueError("Consulta no encontrada")

            # Validar que se pueda cancelar
            if consulta_actual.get("estado") in ["completada"]:
                raise ValueError("No se puede cancelar una consulta completada")

            # Actualizar con motivo en observaciones
            data = {
                "estado": "cancelada",
                "observaciones": f"CANCELADA: {motivo}" if motivo else "CANCELADA"
            }

            update_response = self.client.table("consulta").update(data).eq("id", consultation_id).execute()
            result = update_response.data[0] if update_response.data else None
            
            if result:
                print(f"✅ Consulta cancelada: {consultation_id}")
                return True
            else:
                raise ValueError("Error actualizando consulta en la base de datos")
                
        except PermissionError:
            print("Usuario sin permisos para cancelar consultas")
            raise
        except Exception as e:
            self.handle_error("Error cancelando consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")


    # ==========================================
    # 🔧 MÉTODOS HELPER PARA LÓGICA DE COLAS v4.1
    # ==========================================

    async def _calcular_siguiente_orden_cola_doctor(self, odontologo_id: str) -> int:
        """👨‍⚕️ Calcular siguiente posición en cola específica del doctor usando modelos tipados"""
        try:
            if not odontologo_id:
                return 1
                
            # Usar el método tipado existente
            consultas_hoy: List[ConsultaModel] = await self.get_today_consultations(odontologo_id)
            
            if not consultas_hoy:
                return 1
            
            # Filtrar por este odontólogo específico usando campos v4.1
            consultas_doctor = [
                c for c in consultas_hoy 
                if c.primer_odontologo_id == odontologo_id
            ]
            
            if not consultas_doctor:
                return 1
            
            max_orden_cola = max(
                (c.orden_cola_odontologo or 0 for c in consultas_doctor),
                default=0
            )
            return max_orden_cola + 1
            
        except Exception as e:
            logger.warning(f"Error calculando orden cola doctor: {e}")
            return 1
    
    async def intercambiar_orden_cola(self,
                                  consulta_id: str,
                                  odontologo_id: str,
                                  orden_actual: int,
                                  orden_nuevo: int) -> Dict[str, Any]:
        """
        🔄 Intercambiar posiciones de dos pacientes en la cola del odontólogo.
        Usa el método robusto de intercambio de valores de orden_cola_odontologo.
        """
        try:
            self.require_permission("consultas", "actualizar")

            if orden_actual == orden_nuevo:
                return {"success": False, "message": "Las posiciones son iguales."}

            await self.reindexar_cola_doctor(odontologo_id)
            
            consultas_doctor: List[ConsultaModel] = await self.get_today_consultations(odontologo_id)

            cola_activa = [
                c for c in consultas_doctor
                if c.estado in ["programada", "en_espera"] and c.primer_odontologo_id == odontologo_id
            ]
            cola_activa.sort(key=lambda c: c.orden_cola_odontologo or 0)

            consulta_a_mover = next((c for c in cola_activa if c.id == consulta_id), None)
            consulta_destino = next((c for c in cola_activa if c.orden_cola_odontologo == orden_nuevo), None)

            if not consulta_a_mover:
                return {"success": False, "message": "Consulta a mover no encontrada en la cola activa."}
            if not consulta_destino:
                # Si falla aquí tras la reindexación, es un error de límite o DB.
                return {"success": False, "message": f"No hay consulta en la posición destino ({orden_nuevo})."}

            response1 = self.client.table("consulta").update({
                "orden_cola_odontologo": consulta_destino.orden_cola_odontologo
            }).eq("id", consulta_a_mover.id).execute()
            resultado_1 = response1.data[0] if response1.data else None

            response2 = self.client.table("consulta").update({
                "orden_cola_odontologo": consulta_a_mover.orden_cola_odontologo
            }).eq("id", consulta_destino.id).execute()
            resultado_2 = response2.data[0] if response2.data else None

            if resultado_1 and resultado_2:
                logger.info(f"✅ Intercambio exitoso: {consulta_a_mover.paciente_nombre} ↔ {consulta_destino.paciente_nombre}")
                return {"success": True, "message": f"Paciente {consulta_a_mover.paciente_nombre} movido a posición {orden_nuevo}"}
            else:
                raise ValueError("Error actualizando posiciones en la base de datos. Falla en el UPDATE.")

        except PermissionError:
            logger.warning("Usuario sin permisos para reordenar cola")
            return {"success": False, "message": "Permiso denegado."}
        except Exception as e:
            logger.error(f"❌ Error intercambiando orden en cola: {str(e)}")
            # Aquí puedes llamar a self.handle_error si es una función de tu clase
            return {"success": False, "message": f"Error inesperado: {str(e)}"}

    async def reindexar_cola_doctor(self, odontologo_id: str) -> bool:
        """Sanea la columna 'orden_cola_odontologo' del doctor a 1, 2, 3..."""
        try:
            logger.info(f"🔄 Saneando/Reindexando cola para odontólogo: {odontologo_id}")
            
            # 1. Obtener todas las consultas en cola para ese odontólogo HOY.
            # Usa el método que trae las consultas del día (asume que están ordenadas por orden_llegada si la orden_cola es None)
            consultas_raw: List[ConsultaModel] = await self.get_today_consultations(odontologo_id)
            
            # 2. Filtrar solo las que están en el estado de cola.
            cola_activa = [
                c for c in consultas_raw
                if c.estado in ["programada", "en_espera"] and c.primer_odontologo_id == odontologo_id
            ]
            
            # 3. Ordenar por la hora de llegada (fecha_llegada) como criterio secundario
            # y por el orden_cola_odontologo actual como criterio principal.
            cola_activa.sort(key=lambda c: (c.orden_cola_odontologo or 99999, c.fecha_llegada))
            
            updates = []
            
            # 4. Iterar y crear una lista de actualizaciones (i+1)
            for i, consulta in enumerate(cola_activa, 1):
                if consulta.orden_cola_odontologo != i:
                    updates.append({
                        "id": consulta.id,
                        "orden_cola_odontologo": i
                    })
            
            # 5. Ejecutar la actualización en masa (bucle de updates)
            if updates:
                for item in updates:
                    self.client.table("consulta").update({
                        "orden_cola_odontologo": item["orden_cola_odontologo"]
                    }).eq("id", item["id"]).execute()

                logger.info(f"✅ Reindexación completa. {len(updates)} consultas reordenadas.")
            else:
                logger.info("✅ Cola ya estaba saneada. No se requirieron cambios.")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Fallo crítico en reindexación de cola: {str(e)}")
            return False

    async def complete_consultation_with_payment(self, consultation_id: str, user_id: str) -> Dict[str, Any]:
        """
        🏥 COMPLETAR CONSULTA + CREAR PAGO PENDIENTE (TRANSACCIONAL)

        Ejecuta atómicamente:
        1. Validar consulta en estado "entre_odontologos"
        2. Calcular monto total de servicios realizados
        3. Actualizar estado consulta a "completada"
        4. Crear registro en pagos con estado "pendiente"

        Args:
            consultation_id: ID de la consulta a completar
            user_id: ID del usuario que finaliza (Gerente/Admin)

        Returns:
            {
                "consulta": {...},
                "pago": {...},
                "monto_total_bs": 1500.00,
                "monto_total_usd": 50.00
            }

        Raises:
            ValueError: Si consulta no existe o estado incorrecto
            PermissionError: Si usuario sin permisos
        """
        try:
            logger.info(f"🏥 Completando consulta {consultation_id} con pago...")

            # ✅ PASO 1: Verificar permisos
            self.require_permission("consultas", "actualizar")
            # self.require_permission("pagos", "crear")

            # ✅ PASO 2: Validar consulta existe y está en "entre_odontologos"
            response = self.client.table("consulta").select("*").eq("id", consultation_id).execute()
            consulta = response.data[0] if response.data else None
            if not consulta:
                raise ValueError(f"Consulta {consultation_id} no encontrada")

            if consulta.get("estado") != "entre_odontologos":
                raise ValueError(
                    f"Consulta debe estar en estado 'entre_odontologos'. "
                    f"Estado actual: {consulta.get('estado')}"
                )

            paciente_id = consulta.get("paciente_id")
            if not paciente_id:
                raise ValueError("Consulta sin paciente asignado")

            # 🛡️ PROTECCIÓN ANTI-DUPLICADOS: Verificar que NO existe ya un pago para esta consulta
            existing_payment = self.client.table('pago')\
                .select('id, numero_recibo')\
                .eq('consulta_id', consultation_id)\
                .execute()

            if existing_payment.data and len(existing_payment.data) > 0:
                logger.warning(f"⚠️ Ya existe un pago para la consulta {consultation_id}: {existing_payment.data[0].get('numero_recibo')}")
                # Retornar el pago existente sin crear duplicado
                return {
                    "success": True,
                    "consulta": consulta,
                    "pago": existing_payment.data[0],
                    "monto_total_bs": existing_payment.data[0].get('monto_total_bs', 0),
                    "monto_total_usd": existing_payment.data[0].get('monto_total_usd', 0),
                    "numero_recibo": existing_payment.data[0].get('numero_recibo'),
                    "mensaje": "Pago ya existía - no se creó duplicado"
                }

            # ✅ PASO 3: Calcular monto total de servicios
            monto_total = await self._calcular_monto_total_servicios(consultation_id)
            total_bs = monto_total.get("total_bs", 0)
            total_usd = monto_total.get("total_usd", 0)

            logger.info(f"💰 Monto total calculado: BS {total_bs} | USD {total_usd}")

            # ✅ PASO 4: TRANSACCIÓN - Cambiar estado + Crear pago
            # Nota: Supabase Python client no tiene transacciones explícitas,
            # pero podemos hacer rollback manual si algo falla

            # 4.1 - Actualizar estado consulta
            update_data = {
                "estado": "completada",
                "observaciones": "Consulta finalizada - Pago pendiente creado"
            }
            update_response = self.client.table("consulta").update(update_data).eq("id", consultation_id).execute()
            consulta_updated = update_response.data[0] if update_response.data else None

            if not consulta_updated:
                raise ValueError("Error actualizando estado de consulta")

            # 4.2 - Crear pago pendiente
            pago_data = {
                "consulta_id": consultation_id,
                "paciente_id": paciente_id,
                "monto_total_bs": float(total_bs),
                "monto_total_usd": float(total_usd),
                "monto_pagado_bs": 0,
                "monto_pagado_usd": 0,
                "saldo_pendiente_bs": float(total_bs),
                "saldo_pendiente_usd": float(total_usd),
                "metodos_pago": "pendiente",  # Sin pago aún
                "estado_pago": "pendiente",
                "concepto": f"Consulta #{consulta.get('numero_consulta')} - Servicios odontológicos",
                "procesado_por": user_id
            }

            # INSERT directo a tabla pagos
            pago_response = self.client.table("pago").insert(pago_data).execute()
            pago_creado = pago_response.data[0] if pago_response.data else None

            if not pago_creado:
                # ❌ ROLLBACK: Revertir estado consulta
                logger.error("Error creando pago - Revirtiendo estado consulta")
                rollback_data = {
                    "estado": "entre_odontologos",
                    "observaciones": "Rollback: error creando pago"
                }
                self.client.table("consulta").update(rollback_data).eq("id", consultation_id).execute()
                raise ValueError("Error creando registro de pago")

            logger.info(f"✅ Consulta completada + Pago {pago_creado.get('numero_recibo')} creado")


            # ✅ RETORNAR RESULTADO COMPLETO
            return {
                "success": True,
                "consulta": consulta_updated,
                "pago": pago_creado,
                "monto_total_bs": float(total_bs),
                "monto_total_usd": float(total_usd),
                "numero_recibo": pago_creado.get("numero_recibo")
            }

        except PermissionError:
            logger.warning("Usuario sin permisos para completar consulta")
            raise
        except ValueError as ve:
            logger.error(f"Error de validación: {ve}")
            raise
        except Exception as e:
            self.handle_error("Error completando consulta con pago", e)
            raise ValueError(f"Error inesperado: {str(e)}")


    async def _calcular_monto_total_servicios(self, consulta_id: str) -> Dict[str, float]:
        """
        🧮 Calcular monto total de servicios de una consulta

        Args:
            consulta_id: ID de la consulta

        Returns:
            {"total_bs": 1500.00, "total_usd": 50.00}
        """
        try:
            intervenciones = self.client.table('intervencion')\
                .select('total_bs, total_usd')\
                .eq('consulta_id', consulta_id)\
                .execute()
                    
            total_bs = 0
            total_usd = 0
                
            for serv in intervenciones.data:
                total_bs += serv.get('total_bs', 0)
                total_usd += serv.get('total_usd', 0)

            return {"total_bs": total_bs, "total_usd": total_usd}


        except Exception as e:
            logger.error(f"Error calculando monto total: {e}")
            # En caso de error, retornar 0 (consulta sin servicios registrados)
            return {"total_bs": 0, "total_usd": 0}




# Instancia única para importar
consultas_service = ConsultasService()