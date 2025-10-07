"""
Servicio centralizado para gestión de consultas/citas
Elimina duplicación entre boss_state y admin_state
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from .base_service import BaseService
from dental_system.supabase.tablas import consultas_table, personal_table, services_table
from dental_system.supabase.tablas.cola_atencion import cola_atencion_table
from dental_system.models import ConsultaModel, PersonalModel, ConsultaFormModel
from .cache_invalidation_hooks import invalidate_after_consultation_operation
import logging

logger = logging.getLogger(__name__)

class ConsultasService(BaseService):
    """
    Servicio que maneja toda la lógica de consultas/citas
    Usado tanto por Boss (vista) como Admin (CRUD completo)
    """
    
    def __init__(self):
        super().__init__()
        self.consultas_table = consultas_table
        self.personal_table = personal_table
        self.services_table = services_table
        self.cola_atencion_table = cola_atencion_table
    
    async def get_today_consultations(self, 
                                    odontologo_id: str = None) -> List[ConsultaModel]:
        """
        Obtiene consultas del día - REEMPLAZA 150+ líneas duplicadas
        
        Args:
            odontologo_id: Filtrar por odontólogo (opcional)
            for_boss: Si es para vista del boss (solo lectura)
            
        Returns:
            Lista de consultas del día
        """
        try:
            logger.info("Obteniendo consultas del día")
            
            # Verificar permisos
            self.require_permission("consultas", "leer")
            
            # Usar vista optimizada si está disponible, sino fallback a método estándar
            try:
                consultas_data = self.consultas_table.get_vista_consultas_dia()

                # Filtrar por odontólogo si se especifica
                if odontologo_id:
                    consultas_data = [
                        c for c in consultas_data
                        if c.get('primer_odontologo_id') == odontologo_id
                    ]
            except Exception:
                # Fallback al método estándar
                consultas_data = self.consultas_table.get_today_consultations(odontologo_id)
            
            # Convertir a modelos tipados
            consultas_models = []
            for i, item in enumerate(consultas_data, 1):
                try:
                    # Asegurar que tenga orden de llegada
                    if not item.get('orden_llegada'):
                        item['orden_llegada'] = i
                    
                    model = ConsultaModel.from_dict(item)
                    consultas_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo consulta: {e}")
                    continue
            
            logger.info(f"✅ Consultas del día obtenidas: {len(consultas_models)} registros")
            return consultas_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a consultas")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo consultas del día", e)
            return []
    
    async def get_filtered_consultations(self,
                                       estado: str = None,
                                       odontologo_id: str = None,
                                       search: str = None,
                                       fecha_inicio: date = None,
                                       fecha_fin: date = None) -> List[ConsultaModel]:
        """
        Obtiene consultas filtradas
        
        Args:
            estado: Filtro por estado
            odontologo_id: Filtro por odontólogo
            search: Término de búsqueda
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
            
        Returns:
            Lista de consultas filtradas
        """
        try:
            logger.info("Obteniendo consultas filtradas")
            
            # Verificar permisos
            self.require_permission("consultas", "leer")
            
            # Si no se especifican fechas, usar hoy por defecto
            if not fecha_inicio and not fecha_fin:
                today = date.today()
                consultas_data = self.consultas_table.get_today_consultations(odontologo_id)
            else:
                # Usar rango de fechas
                fecha_inicio = fecha_inicio or date.today()
                fecha_fin = fecha_fin or date.today()
                consultas_data = self.consultas_table.get_by_date_range(
                    fecha_inicio, fecha_fin, odontologo_id, estado
                )
            
            # Convertir a modelos
            consultas_models = []
            for item in consultas_data:
                try:
                    model = ConsultaModel.from_dict(item)
                    consultas_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo consulta: {e}")
                    continue
            
            # Aplicar filtro de búsqueda en memoria si es necesario
            if search and search.strip():
                consultas_models = self._apply_search_filter(consultas_models, search.strip())
            
            # Aplicar filtro de estado en memoria si es necesario
            if estado and estado != "todos":
                consultas_models = [c for c in consultas_models if c.estado == estado]
            
            logger.info(f"✅ Consultas filtradas obtenidas: {len(consultas_models)} registros")
            return consultas_models
            
        except Exception as e:
            self.handle_error("Error obteniendo consultas filtradas", e)
            return []
    
    def _apply_search_filter(self, consultas: List[ConsultaModel], search_term: str) -> List[ConsultaModel]:
        """Aplica filtro de búsqueda en memoria"""
        search_lower = search_term.lower()
        filtered = []
        
        for consulta in consultas:
            # Campos donde buscar
            search_fields = [
                consulta.paciente_nombre.lower(),
                consulta.odontologo_nombre.lower(),
                consulta.numero_consulta.lower(),
                (consulta.motivo_consulta or "").lower()
            ]
            
            # Si algún campo contiene el término
            if any(search_lower in field for field in search_fields):
                filtered.append(consulta)
        
        return filtered
    
    async def create_consultation(self, consulta_data: Dict[str, Any] = None, user_id: str = None) -> Optional[ConsultaModel]:
        """
        Crea nueva consulta por orden de llegada - ESQUEMA v4.1
        
        Args:
            consulta_data: Datos de la consulta (Dict o ConsultaFormModel)
            user_id: ID del usuario que crea
            
        Returns:
            ConsultaModel creada o None si hay error
        """
        try:
            logger.info("🏥 Creando nueva consulta por orden de llegada...")
            
            # Verificar permisos
            self.require_permission("consultas", "crear")
            
            # Manejar tanto Dict como ConsultaFormModel (compatibilidad)
            if hasattr(consulta_data, 'validate_form'):
                # Es ConsultaFormModel
                validation_errors = consulta_data.validate_form()
                if validation_errors:
                    error_msg = f"Errores de validación: {validation_errors}"
                    raise ValueError(error_msg)
                
                datos_consulta = {
                    "paciente_id": consulta_data.paciente_id,
                    "primer_odontologo_id": consulta_data.primer_odontologo_id,
                    "odontologo_preferido_id": consulta_data.odontologo_preferido_id,
                    "motivo_consulta": consulta_data.motivo_consulta,
                    "observaciones": consulta_data.observaciones,
                    "notas_internas": consulta_data.notas_internas,
                    "tipo_consulta": consulta_data.tipo_consulta or "general",
                    "prioridad": consulta_data.prioridad or "normal"
                }
            else:
                # Es Dict (compatibilidad backward)
                datos_consulta = consulta_data or {}
            
            # ✅ LÓGICA DE COLAS v4.1
            # Calcular orden de llegada automáticamente
            orden_general = await self._calcular_siguiente_orden_general()
            orden_cola_doctor = await self._calcular_siguiente_orden_cola_doctor(
                datos_consulta.get("primer_odontologo_id") or datos_consulta.get("odontologo_id")
            )
            
            # Crear consulta con esquema v4.1 usando método actualizado
            result = self.consultas_table.create_consultation(
                paciente_id=datos_consulta["paciente_id"],
                primer_odontologo_id=datos_consulta.get("primer_odontologo_id") or datos_consulta.get("odontologo_id"),
                odontologo_preferido_id=datos_consulta.get("odontologo_preferido_id"),
                fecha_llegada=datetime.now(),  # Momento de llegada real
                orden_llegada_general=orden_general,
                orden_cola_odontologo=orden_cola_doctor,
                estado="en_espera",  # Estado inicial v4.1
                tipo_consulta=datos_consulta.get("tipo_consulta", "general"),
                motivo_consulta=datos_consulta.get("motivo_consulta"),
                observaciones=datos_consulta.get("observaciones"),
                notas_internas=datos_consulta.get("notas_internas"),
                prioridad=datos_consulta.get("prioridad", "normal"),
                creada_por=user_id
            )
            
            if result:
                # Crear modelo tipado del resultado
                consulta_model = ConsultaModel.from_dict(result)
                
                logger.info(f"✅ Consulta creada: {consulta_model.numero_consulta}")
                
                # 🗑️ INVALIDAR CACHE - consulta creada afecta estadísticas
                try:
                    invalidate_after_consultation_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras crear consulta: {cache_error}")
                
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
            
            # Debug para ver qué datos recibimos
            logger.info(f"[DEBUG] Actualizando consulta {consultation_id}")
            logger.info(f"[DEBUG] primer_odontologo_id: {getattr(consulta_form, 'primer_odontologo_id', 'No existe')}")
            logger.info(f"[DEBUG] odontologo_id: {getattr(consulta_form, 'odontologo_id', 'No existe')}")
            logger.info(f"[DEBUG] paciente_id: {getattr(consulta_form, 'paciente_id', 'No existe')}")
            
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
            current_consulta = self.consultas_table.get_by_id(consultation_id)
            logger.info(f"[DEBUG] Consulta actual estado: {current_consulta.get('estado') if current_consulta else 'No encontrada'}")
            
            if current_consulta and current_consulta.get("estado") in ["programada", "en_espera"]:
                # Usar el campo correcto del esquema v4.1
                nuevo_odontologo = consulta_form.primer_odontologo_id or getattr(consulta_form, 'odontologo_id', None)
                odontologo_actual = current_consulta.get("primer_odontologo_id") or current_consulta.get("odontologo_id")
                
                logger.info(f"[DEBUG] Nuevo odontólogo: {nuevo_odontologo}")
                logger.info(f"[DEBUG] Odontólogo actual: {odontologo_actual}")
                
                if nuevo_odontologo and nuevo_odontologo != odontologo_actual:
                    data["primer_odontologo_id"] = nuevo_odontologo
                    logger.info(f"[DEBUG] ✅ Cambiando odontólogo de {odontologo_actual} a {nuevo_odontologo}")
                else:
                    logger.info(f"[DEBUG] ❌ No se cambiará odontólogo: nuevo={nuevo_odontologo}, actual={odontologo_actual}")
            
            result = self.consultas_table.update(consultation_id, data)
            
            if result:
                # Crear modelo tipado del resultado
                consulta_model = ConsultaModel.from_dict(result)
                
                logger.info(f"✅ Consulta actualizada correctamente")
                
                # 🗑️ INVALIDAR CACHE - consulta actualizada afecta estadísticas
                try:
                    invalidate_after_consultation_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras actualizar consulta: {cache_error}")
                
                return consulta_model
            else:
                raise ValueError("Error actualizando consulta")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para actualizar consultas")
            raise
        except Exception as e:
            self.handle_error("Error actualizando consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")

    async def obtener_cola_odontologo(self, odontologo_id: str) -> List[Dict[str, Any]]:
        """
        Obtener cola de pacientes de un odontólogo específico

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Lista de consultas en cola ordenadas por prioridad y orden de llegada
        """
        try:
            logger.info(f"Obteniendo cola del odontólogo {odontologo_id}")

            # Verificar permisos
            self.require_permission("consultas", "leer")

            # Obtener cola usando la tabla especializada
            cola_data = self.cola_atencion_table.obtener_cola_odontologo(odontologo_id)

            return cola_data

        except Exception as e:
            self.handle_error("Error obteniendo cola de odontólogo", e)
            return []

    async def obtener_proximo_paciente(self, odontologo_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtener el próximo paciente en la cola del odontólogo

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Datos del próximo paciente o None
        """
        try:
            logger.info(f"Obteniendo próximo paciente para odontólogo {odontologo_id}")

            # Verificar permisos
            self.require_permission("consultas", "leer")

            # Usar función especializada de cola_atencion
            proximo_paciente = self.cola_atencion_table.obtener_proximo_paciente(odontologo_id)

            return proximo_paciente

        except Exception as e:
            self.handle_error("Error obteniendo próximo paciente", e)
            return None

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
            consulta_actual = self.consultas_table.get_by_id(consulta_id)
            if consulta_actual and consulta_actual.get('observaciones'):
                observaciones_previas = consulta_actual['observaciones'] + "\n\n"

            update_data = {
                'primer_odontologo_id': nuevo_odontologo_id,
                'observaciones': f"{observaciones_previas}TRANSFERENCIA: {motivo} - {current_time}"
            }

            consulta_actualizada = self.consultas_table.update(consulta_id, update_data)

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

    async def obtener_estadisticas_colas(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de todas las colas de odontólogos

        Returns:
            Diccionario con estadísticas por odontólogo
        """
        try:
            logger.info("Obteniendo estadísticas de colas")

            # Verificar permisos
            self.require_permission("consultas", "leer")

            # Obtener estadísticas usando tabla especializada
            estadisticas = self.cola_atencion_table.obtener_estadisticas_colas()

            return estadisticas

        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de colas", e)
            return {}

    async def obtener_estadisticas_optimizadas(self) -> Dict[str, Any]:
        """
        Obtener estadísticas usando vistas y funciones optimizadas de BD

        Returns:
            Diccionario con estadísticas completas del sistema
        """
        try:
            logger.info("Obteniendo estadísticas usando funciones optimizadas")

            # Verificar permisos
            self.require_permission("consultas", "leer")

            # Usar vista optimizada de colas
            estadisticas_colas = self.consultas_table.get_vista_cola_odontologos()

            # Procesar estadísticas para el formato esperado
            estadisticas_procesadas = {
                'colas_por_odontologo': estadisticas_colas,
                'resumen_global': {
                    'total_odontologos': len(estadisticas_colas),
                    'total_esperando': sum(cola.get('pacientes_esperando', 0) for cola in estadisticas_colas),
                    'total_atendiendo': sum(cola.get('pacientes_atendiendo', 0) for cola in estadisticas_colas),
                    'total_atendidos_hoy': sum(cola.get('pacientes_atendidos_hoy', 0) for cola in estadisticas_colas)
                }
            }

            return estadisticas_procesadas

        except Exception as e:
            self.handle_error("Error obteniendo estadísticas optimizadas", e)
            return {}

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
            consulta_actual = self.consultas_table.get_by_id(consultation_id)
            print(consulta_actual)
            if consulta_actual.get("estado") != "en_progreso":
                if consulta_actual and not self._is_valid_status_transition(consulta_actual.get("estado"), nuevo_estado):
                    raise ValueError(f"Transición de estado no válida")
            
            result = self.consultas_table.update_status(consultation_id, nuevo_estado, notas)
            
            if result:
                logger.info(f"✅ Estado de consulta cambiado a: {nuevo_estado}")
                
                # 🗑️ INVALIDAR CACHE - cambio de estado afecta estadísticas real-time
                try:
                    invalidate_after_consultation_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras cambiar estado consulta: {cache_error}")
                
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
    
    async def get_support_data(self) -> List[PersonalModel]:
        """
        Obtiene datos de apoyo para consultas (odontólogos)
        REEMPLAZA múltiples métodos duplicados
        
        Returns:
            Lista de PersonalModel con odontólogos activos
        """
        try:
            logger.info("Obteniendo datos de apoyo para consultas")
            
            # Obtener odontólogos activos
            odontologos_data = self.personal_table.get_dentists(incluir_inactivos=False)
            
            # ✅ Convertir a modelos PersonalModel
            odontologos_models = [
                PersonalModel.from_dict(odontologo_data) 
                for odontologo_data in odontologos_data
            ]
            
            return odontologos_models
                
        except Exception as e:
            self.handle_error("Error obteniendo datos de apoyo", e)
            return []
    
    
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
            
            data = self.consultas_table.get_consultation_details(consultation_id)
            if data:
                return ConsultaModel.from_dict(data)
            return None
            
        except Exception as e:
            self.handle_error("Error obteniendo consulta por ID", e)
            return None
    
    
    async def confirm_consultation(self, consultation_id: str) -> bool:
        """Confirma una consulta programada"""
        return await self.change_consultation_status(consultation_id, "confirmada")
    
    async def mark_no_show(self, consultation_id: str) -> bool:
        """Marca una consulta como no asistida"""
        return await self.change_consultation_status(consultation_id, "no_asistio")


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
            consulta_actual = self.consultas_table.get_by_id(consultation_id)
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
            
            result = self.consultas_table.update(consultation_id, data)
            
            if result:
                logger.info(f"✅ Consulta cancelada: {consultation_id}")
                return True
            else:
                raise ValueError("Error actualizando consulta en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para cancelar consultas")
            raise
        except Exception as e:
            self.handle_error("Error cancelando consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")


    # ==========================================
    # 🔧 MÉTODOS HELPER PARA LÓGICA DE COLAS v4.1
    # ==========================================
    
    async def _calcular_siguiente_orden_general(self) -> int:
        """📊 Calcular siguiente orden de llegada general del día usando modelos tipados"""
        try:
            hoy = date.today()
            # Usar el método tipado existente
            consultas_hoy: List[ConsultaModel] = await self.get_today_consultations()
            
            if not consultas_hoy:
                return 1
            
            max_orden = max(
                (c.orden_llegada_general or 0 for c in consultas_hoy),
                default=0
            )
            return max_orden + 1
            
        except Exception as e:
            logger.warning(f"Error calculando orden general: {e}")
            return 1
    
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
    
    async def obtener_cola_odontologo_tipada(self, odontologo_id: str) -> List[ConsultaModel]:
        """
        👨‍⚕️ OBTENER COLA ESPECÍFICA DE UN ODONTÓLOGO usando modelos tipados
        
        Args:
            odontologo_id: ID del odontólogo
            
        Returns:
            List[ConsultaModel]: Consultas en cola ordenadas
        """
        try:
            logger.info(f"📋 Obteniendo cola tipada del Dr. {odontologo_id}...")
            
            # Verificar permisos
            self.require_permission("consultas", "leer")
            
            # Obtener todas las consultas del día del odontólogo usando método tipado
            consultas_doctor: List[ConsultaModel] = await self.get_today_consultations(odontologo_id)
            
            # Filtrar solo las que están en proceso usando estados v4.1
            cola_activa = [
                c for c in consultas_doctor 
                if c.estado in ["en_espera", "en_atencion"] and
                c.primer_odontologo_id == odontologo_id
            ]
            
            # Ordenar por posición en cola usando campo v4.1
            cola_activa.sort(key=lambda c: c.orden_cola_odontologo or 0)
            
            logger.info(f"✅ Cola tipada Dr. {odontologo_id}: {len(cola_activa)} consultas")
            return cola_activa
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo cola tipada: {str(e)}")
            return []
    
    async def iniciar_atencion_consulta_tipada(self, 
                                             consulta_id: str, 
                                             odontologo_id: str) -> bool:
        """
        🏥 INICIAR ATENCIÓN DE CONSULTA usando modelos tipados - v4.1
        
        Args:
            consulta_id: ID de la consulta
            odontologo_id: ID del odontólogo
            
        Returns:
            bool: True si se inició correctamente
        """
        try:
            logger.info(f"🏥 Iniciando atención tipada consulta {consulta_id}...")
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Validar que el odontólogo no tenga otra consulta en curso usando modelos tipados
            cola_doctor: List[ConsultaModel] = await self.obtener_cola_odontologo_tipada(odontologo_id)
            en_atencion = [c for c in cola_doctor if c.estado == "en_atencion"]
            
            if len(en_atencion) > 0:
                raise ValueError("El odontólogo ya tiene una consulta en atención")
            
            # Cambiar estado usando estados v4.1
            success = await self.change_consultation_status(
                consulta_id, 
                "en_atencion",
                f"Iniciada atención por Dr. {odontologo_id}"
            )
            
            if success:
                logger.info(f"✅ Consulta tipada {consulta_id} iniciada por Dr. {odontologo_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error iniciando atención tipada: {str(e)}")
            return False
    
    async def completar_consulta_tipada(self, 
                                      consulta_id: str, 
                                      datos_finalizacion: Dict[str, Any] = None) -> bool:
        """
        ✅ COMPLETAR CONSULTA usando modelos tipados - v4.1
        
        Args:
            consulta_id: ID de la consulta
            datos_finalizacion: Datos adicionales de finalización
            
        Returns:
            bool: True si se completó correctamente
        """
        try:
            logger.info(f"✅ Completando consulta tipada {consulta_id}...")
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Obtener consulta actual usando modelo tipado
            consulta_actual: Optional[ConsultaModel] = await self.get_consultation_by_id(consulta_id)
            if not consulta_actual:
                raise ValueError("Consulta no encontrada")
            
            # Validar estado usando estados v4.1
            if consulta_actual.estado != "en_atencion":
                raise ValueError("Solo se pueden completar consultas en atención")
            
            # Preparar notas de finalización
            notas_finalizacion = "Consulta completada"
            if datos_finalizacion and datos_finalizacion.get("observaciones"):
                notas_finalizacion += f" - {datos_finalizacion['observaciones']}"
            
            # Cambiar estado usando estados v4.1
            success = await self.change_consultation_status(
                consulta_id,
                "completada", 
                notas_finalizacion
            )
            
            if success:
                logger.info(f"✅ Consulta tipada {consulta_id} completada exitosamente")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error completando consulta tipada: {str(e)}")
            return False
    
    async def obtener_metricas_cola_tiempo_real_tipadas(self, odontologo_id: str = None) -> Dict[str, Any]:
        """
        📊 MÉTRICAS DE COLA EN TIEMPO REAL usando modelos tipados
        
        Args:
            odontologo_id: ID específico o None para todos
            
        Returns:
            Dict con métricas de cola
        """
        try:
            logger.info("📊 Generando métricas tipadas de cola tiempo real...")
            
            # Verificar permisos
            self.require_permission("consultas", "leer")
            
            if odontologo_id:
                # Métricas de un odontólogo específico usando modelos tipados
                cola: List[ConsultaModel] = await self.obtener_cola_odontologo_tipada(odontologo_id)
                
                metricas = {
                    "odontologo_id": odontologo_id,
                    "total_en_cola": len(cola),
                    "en_espera": len([c for c in cola if c.estado == "en_espera"]),
                    "en_atencion": len([c for c in cola if c.estado == "en_atencion"]),
                    "tiempo_espera_promedio": self._calcular_tiempo_espera_promedio_tipado(cola),
                    "consultas": [
                        {
                            "id": c.id,
                            "paciente": c.paciente_nombre,
                            "estado": c.estado,
                            "orden": c.orden_cola_odontologo,
                            "tiempo_espera": c.tiempo_espera_estimado,
                            "es_urgente": c.es_urgente
                        }
                        for c in cola[:10]  # Primeras 10 usando propiedades del modelo
                    ]
                }
            else:
                # Métricas globales usando modelos tipados
                consultas_hoy: List[ConsultaModel] = await self.get_today_consultations()
                
                metricas = {
                    "total_consultas_hoy": len(consultas_hoy),
                    "en_espera": len([c for c in consultas_hoy if c.estado == "en_espera"]),
                    "en_atencion": len([c for c in consultas_hoy if c.estado == "en_atencion"]),
                    "completadas": len([c for c in consultas_hoy if c.estado == "completada"]),
                    "canceladas": len([c for c in consultas_hoy if c.estado == "cancelada"]),
                    "por_odontologo": {}
                }
                
                # Agrupar por odontólogo usando campos v4.1
                odontologos_con_consultas = set(
                    c.primer_odontologo_id for c in consultas_hoy if c.primer_odontologo_id
                )
                
                for odontologo_id_actual in odontologos_con_consultas:
                    cola_doctor = [c for c in consultas_hoy if c.primer_odontologo_id == odontologo_id_actual]
                    metricas["por_odontologo"][odontologo_id_actual] = {
                        "total": len(cola_doctor),
                        "en_espera": len([c for c in cola_doctor if c.estado == "en_espera"]),
                        "en_atencion": len([c for c in cola_doctor if c.estado == "en_atencion"])
                    }
            
            logger.info("✅ Métricas tipadas de cola generadas")
            return metricas
            
        except Exception as e:
            logger.error(f"❌ Error generando métricas tipadas: {str(e)}")
            return {}
    
    def _calcular_tiempo_espera_promedio_tipado(self, cola: List[ConsultaModel]) -> float:
        """⏰ Calcular tiempo de espera promedio usando modelos tipados"""
        consultas_espera = [c for c in cola if c.estado == "en_espera"]
        if not consultas_espera:
            return 0.0
        
        tiempos = []
        for consulta in consultas_espera:
            try:
                # Usar campos v4.1 del modelo tipado
                if consulta.fecha_llegada:
                    llegada = datetime.fromisoformat(consulta.fecha_llegada.replace('Z', '+00:00'))
                    espera_minutos = (datetime.now() - llegada).total_seconds() / 60
                    tiempos.append(max(0, espera_minutos))
            except Exception as e:
                logger.warning(f"Error calculando tiempo espera tipado: {e}")
                continue
        
        return sum(tiempos) / len(tiempos) if tiempos else 0.0
    
    async def change_consultation_dentist(self, 
                                        consulta_id: str, 
                                        nuevo_odontologo_id: str, 
                                        motivo: str) -> Optional[ConsultaModel]:
        """
        🔄 Cambiar odontólogo de una consulta
        
        Args:
            consulta_id: ID de la consulta
            nuevo_odontologo_id: ID del nuevo odontólogo
            motivo: Motivo del cambio (obligatorio)
            
        Returns:
            ConsultaModel actualizada o None
        """
        try:
            logger.info(f"🔄 Cambiando odontólogo de consulta {consulta_id} a {nuevo_odontologo_id}")
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Validar parámetros
            if not consulta_id or not nuevo_odontologo_id or not motivo:
                raise ValueError("Todos los parámetros son obligatorios")
            
            if len(motivo.strip()) < 10:
                raise ValueError("El motivo debe tener al menos 10 caracteres")
            
            # Obtener consulta actual
            consulta_actual = await self.get_consultation_by_id(consulta_id)
            if not consulta_actual:
                raise ValueError("Consulta no encontrada")
            
            # Validar que se pueda cambiar
            if consulta_actual.estado in ["completada", "cancelada"]:
                raise ValueError("No se puede cambiar odontólogo de una consulta completada o cancelada")
            
            # Calcular nueva posición en cola del nuevo odontólogo
            nueva_posicion_cola = await self._calcular_siguiente_orden_cola_doctor(nuevo_odontologo_id)
            
            # Preparar datos de actualización
            datos_actualizacion = {
                "primer_odontologo_id": nuevo_odontologo_id,
                "orden_cola_odontologo": nueva_posicion_cola,
                "estado": "en_espera",  # Resetear a espera en nueva cola
                "observaciones": f"{consulta_actual.observaciones or ''}\n[CAMBIO ODONTÓLOGO] {motivo}".strip(),
                "notas_internas": f"{consulta_actual.notas_internas or ''}\n[CAMBIO] {consulta_actual.odontologo_nombre} → Dr. {nuevo_odontologo_id}: {motivo}".strip()
            }
            
            # Actualizar en base de datos
            result = self.consultas_table.update(consulta_id, datos_actualizacion)
            
            if result:
                # Obtener consulta actualizada con datos completos
                consulta_actualizada = await self.get_consultation_by_id(consulta_id)
                
                logger.info(f"✅ Odontólogo cambiado: {consulta_id} → Dr. {nuevo_odontologo_id} (posición {nueva_posicion_cola})")
                
                # Invalidar cache
                try:
                    invalidate_after_consultation_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras cambio: {cache_error}")
                
                return consulta_actualizada
            else:
                raise ValueError("Error actualizando consulta en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para cambiar odontólogo")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación en cambio: {e}")
            raise
        except Exception as e:
            self.handle_error("Error cambiando odontólogo de consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")

    async def intercambiar_orden_cola(self,
                                    consulta_id: str,
                                    odontologo_id: str,
                                    orden_actual: int,
                                    orden_nuevo: int) -> Dict[str, Any]:
        """
        🔄 Intercambiar posiciones de dos pacientes en la cola del odontólogo

        Args:
            consulta_id: ID de la consulta a mover
            odontologo_id: ID del odontólogo (para validación)
            orden_actual: Posición actual en cola
            orden_nuevo: Nueva posición deseada

        Returns:
            Dict con resultado de la operación
        """
        try:
            logger.info(f"🔄 Intercambiando orden en cola: {consulta_id} de {orden_actual} a {orden_nuevo}")

            # Verificar permisos
            self.require_permission("consultas", "actualizar")

            # Validar parámetros
            if orden_actual == orden_nuevo:
                return {"success": False, "message": "Las posiciones son iguales"}

            # Obtener consultas del día del odontólogo usando método tipado
            consultas_doctor: List[ConsultaModel] = await self.get_today_consultations(odontologo_id)

            # Filtrar solo las consultas en espera del odontólogo específico (usar estado correcto)
            cola_activa = [
                c for c in consultas_doctor
                if c.estado in ["programada", "en_espera"] and c.primer_odontologo_id == odontologo_id
            ]

            # Ordenar por posición actual en cola
            cola_activa.sort(key=lambda c: c.orden_cola_odontologo or 0)

            # Validar que hay suficientes pacientes para intercambiar
            if len(cola_activa) < 2:
                return {"success": False, "message": "No hay suficientes pacientes para reordenar"}

            # Encontrar la consulta que se quiere mover
            consulta_a_mover = None
            for consulta in cola_activa:
                if consulta.id == consulta_id:
                    consulta_a_mover = consulta
                    break

            if not consulta_a_mover:
                return {"success": False, "message": "Consulta no encontrada en la cola"}

            # Validar que el orden_actual coincide con el de la consulta
            if consulta_a_mover.orden_cola_odontologo != orden_actual:
                logger.warning(f"⚠️ Orden actual inconsistente: esperado {orden_actual}, real {consulta_a_mover.orden_cola_odontologo}")
                orden_actual = consulta_a_mover.orden_cola_odontologo

            # Validar límites de movimiento basándose en las posiciones reales
            ordenes_existentes = sorted([c.orden_cola_odontologo for c in cola_activa if c.orden_cola_odontologo])
            if not ordenes_existentes:
                return {"success": False, "message": "No hay órdenes válidos en la cola"}

            orden_min = min(ordenes_existentes)
            orden_max = max(ordenes_existentes)

            if orden_nuevo < orden_min:
                orden_nuevo = orden_min
            elif orden_nuevo > orden_max:
                orden_nuevo = orden_max

            # Buscar la consulta que está en la posición destino
            consulta_destino = None
            for consulta in cola_activa:
                if consulta.orden_cola_odontologo == orden_nuevo:
                    consulta_destino = consulta
                    break

            if not consulta_destino:
                return {"success": False, "message": f"No hay consulta en la posición {orden_nuevo}"}

            if consulta_a_mover.id == consulta_destino.id:
                return {"success": False, "message": "Ya está en esa posición"}

            # Intercambiar las posiciones en la base de datos usando transacción implícita
            orden_temp = orden_actual
            orden_destino_temp = consulta_destino.orden_cola_odontologo

            # Actualizar consulta que se mueve a la nueva posición
            resultado_1 = self.consultas_table.update(consulta_a_mover.id, {
                "orden_cola_odontologo": orden_destino_temp
            })

            # Actualizar consulta que cede su posición
            resultado_2 = self.consultas_table.update(consulta_destino.id, {
                "orden_cola_odontologo": orden_temp
            })

            if resultado_1 and resultado_2:
                paciente_movido = getattr(consulta_a_mover, 'paciente_nombre', 'Paciente')
                paciente_destino = getattr(consulta_destino, 'paciente_nombre', 'Paciente')

                logger.info(f"✅ Intercambio exitoso: {paciente_movido} ↔ {paciente_destino}")

                # Invalidar cache
                try:
                    invalidate_after_consultation_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras intercambio: {cache_error}")

                return {
                    "success": True,
                    "message": f"Paciente movido de posición {orden_actual} a {orden_nuevo}",
                    "consulta_movida": {
                        "id": consulta_a_mover.id,
                        "paciente": paciente_movido,
                        "posicion_anterior": orden_actual,
                        "posicion_nueva": orden_nuevo
                    },
                    "consulta_intercambiada": {
                        "id": consulta_destino.id,
                        "paciente": consulta_destino.paciente_nombre,
                        "posicion_anterior": consulta_destino.orden_cola_odontologo,
                        "posicion_nueva": consulta_a_mover.orden_cola_odontologo
                    }
                }
            else:
                raise ValueError("Error actualizando posiciones en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para reordenar cola")
            raise
        except Exception as e:
            logger.error(f"❌ Error intercambiando orden en cola: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

# Instancia única para importar
consultas_service = ConsultasService()