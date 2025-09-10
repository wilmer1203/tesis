"""
🦷 SERVICIO DE ODONTOLOGÍA - ATENCIÓN CLÍNICA ESPECIALIZADA
=========================================================

Servicio centralizado para la atención odontológica especializada.
Maneja el flujo completo de atención: pacientes asignados, disponibles, 
intervenciones, odontogramas y condiciones dentales.

Funcionalidades principales:
- Gestión de pacientes del odontólogo (asignados + disponibles)
- Inicio y finalización de intervenciones
- Manejo completo de odontogramas por superficies
- Registro de condiciones dentales con historial
- Integración con consultas y servicios
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date
from decimal import Decimal
from .base_service import BaseService
from dental_system.supabase.tablas import (
    consultas_table, interventions_table, pacientes_table,
    odontograms_table, dientes_table, condiciones_diente_table,
    servicios_table, historial_medico_table
)
from dental_system.models import ConsultaModel, PacienteModel
from .cache_invalidation_hooks import invalidate_after_intervention_operation, track_cache_invalidation
import logging

logger = logging.getLogger(__name__)

# Definición de condiciones y colores para odontograma
CONDICIONES_DIENTE = {
    "sano": {"color": "#90EE90", "descripcion": "Diente sano", "simbolo": "✓"},
    "caries": {"color": "#FF0000", "descripcion": "Caries dental", "simbolo": "C"},
    "obturado": {"color": "#C0C0C0", "descripcion": "Obturación/empaste", "simbolo": "O"},
    "endodoncia": {"color": "#FFD700", "descripcion": "Tratamiento de conducto", "simbolo": "E"},
    "corona": {"color": "#4169E1", "descripcion": "Corona dental", "simbolo": "R"},
    "puente": {"color": "#800080", "descripcion": "Puente dental", "simbolo": "P"},
    "extraccion": {"color": "#8B0000", "descripcion": "Para extraer", "simbolo": "X"},
    "ausente": {"color": "#FFFFFF", "descripcion": "Diente ausente", "simbolo": "-"},
    "fractura": {"color": "#FF6347", "descripcion": "Fractura dental", "simbolo": "F"},
    "implante": {"color": "#32CD32", "descripcion": "Implante dental", "simbolo": "I"},
    "protesis": {"color": "#DA70D6", "descripcion": "Prótesis removible", "simbolo": "PT"},
    "giroversion": {"color": "#FF8C00", "descripcion": "Diente rotado", "simbolo": "G"}
}

class OdontologiaService(BaseService):
    """
    🦷 Servicio especializado para la atención odontológica
    
    Funcionalidades:
    - Gestión de pacientes del odontólogo
    - Control de intervenciones
    - Manejo de odontogramas
    - Registro de condiciones dentales
    """
    
    def __init__(self):
        super().__init__()
        self.consultas_table = consultas_table
        self.interventions_table = interventions_table
        self.pacientes_table = pacientes_table
        self.services_table = servicios_table  # ✅ Agregar tabla de servicios faltante
        # ✅ Usar instancia importada en lugar de crear nueva
        self.odontograms_table = odontograms_table
    
    def _get_personal_id_from_user_id(self, usuario_id: str) -> str:
        """
        🔄 CONVERTIR: ID de usuario → ID de personal
        
        Args:
            usuario_id: ID del usuario logueado
            
        Returns:
            ID del registro en la tabla personal
        """
        try:
            # Buscar el registro en personal donde usuario_id coincida
            response = self.client.table("personal").select("id").eq("usuario_id", usuario_id).execute()
            
            if response.data:
                personal_id = response.data[0]["id"]
                print(f"[DEBUG] 🔄 Conversión ID: usuario {usuario_id} → personal {personal_id}")
                return personal_id
            else:
                print(f"[DEBUG] ⚠️ No se encontró registro en personal para usuario {usuario_id}")
                return usuario_id  # Fallback al mismo ID
                
        except Exception as e:
            print(f"[DEBUG] ❌ Error convirtiendo ID: {e}")
            return usuario_id  # Fallback al mismo ID

    async def get_pacientes_asignados(self, personal_id: str) -> List[PacienteModel]:
        """
        📋 Obtener pacientes asignados directamente al odontólogo
        
        Args:
            personal_id: ID del personal en tabla personal (ya no necesita conversión)
            
        Returns:
            Lista de pacientes con consultas asignadas al odontólogo
        """
        try:
            logger.info(f"Obteniendo pacientes asignados para personal_id: {personal_id}")
            
            # Verificar permisos - usar consultas ya que manejamos consultas asignadas
            if not self.check_permission("consultas", "leer"):
                raise PermissionError("Sin permisos para acceder a las consultas")
            
            # Usar personal_id directamente sin conversión
            # Obtener consultas del día
            consultas_hoy = self.consultas_table.get_today_consultations(personal_id)
            
            # Filtrar solo las programadas y en progreso
            consultas = [c for c in consultas_hoy if c.get("estado") in ["programada", "en_progreso"]]
            
            # Enriquecer con datos del paciente
            pacientes_asignados = []
            for consulta in consultas:
                try:
                    # Obtener datos completos del paciente
                    paciente_data = self.pacientes_table.get_by_id(consulta["paciente_id"])
                    if paciente_data:
                        paciente_completo = {
                            **consulta,
                            # Campos mapeados correctamente desde la BD
                            "primer_nombre": paciente_data.get("primer_nombre", ""),
                            "segundo_nombre": paciente_data.get("segundo_nombre", ""),
                            "primer_apellido": paciente_data.get("primer_apellido", ""),
                            "segundo_apellido": paciente_data.get("segundo_apellido", ""),
                            "numero_documento": paciente_data.get("numero_documento", ""),
                            "telefono_1": paciente_data.get("telefono_1", ""),
                            "telefono_2": paciente_data.get("telefono_2", ""),
                            "numero_historia": paciente_data.get("numero_historia", ""),
                            "alergias": paciente_data.get("alergias", []),
                            "condiciones_medicas": paciente_data.get("condiciones_medicas", []),
                            "tipo_asignacion": "directo"
                        }
                        pacientes_asignados.append(paciente_completo)
                except Exception as e:
                    logger.warning(f"Error procesando paciente {consulta.get('paciente_id')}: {e}")
                    continue
            
            # Convertir diccionarios a modelos PacienteModel con información de consulta
            pacientes_models = []
            for paciente_data in pacientes_asignados:
                try:
                    # Extraer campos de paciente (ya correctamente mapeados arriba)
                    campos_paciente = {k: v for k, v in paciente_data.items() 
                                     if k not in ['id', 'numero_consulta', 'estado', 'fecha_programada', 'odontologo_id', 'motivo_consulta', 'tipo_consulta', 'tipo_asignacion']}
                    
                    # El ID del paciente está en paciente_id, no en id (que es consulta_id)
                    campos_paciente['id'] = paciente_data.get("paciente_id", "")
                    
                    paciente_model = PacienteModel.from_dict(campos_paciente)
                    
                    # Agregar información de consulta como atributos temporales
                    paciente_model._consulta_id = paciente_data.get("id", "")  # ID de la consulta
                    paciente_model._estado_consulta = paciente_data.get("estado", "")
                    paciente_model._numero_consulta = paciente_data.get("numero_consulta", "")
                    paciente_model._fecha_consulta = paciente_data.get("fecha_programada", "")
                    
                    print(f"[DEBUG] 🔧 Paciente procesado: {paciente_model.nombre_completo}, consulta_id: {paciente_model._consulta_id}")
                    
                    pacientes_models.append(paciente_model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo paciente a modelo: {e}")
                    print(f"[DEBUG] ❌ Datos problemáticos: {paciente_data}")
                    continue
            
            logger.info(f"✅ {len(pacientes_models)} pacientes asignados convertidos a modelos")
            return pacientes_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para ver pacientes asignados")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo pacientes asignados", e)
            return []
    
    async def get_pacientes_disponibles(self, personal_id: str) -> List[PacienteModel]:
        """
        📋 Obtener pacientes disponibles para intervención
        
        Pacientes que ya completaron una intervención con otro odontólogo
        y están listos para recibir una nueva intervención.
        
        Args:
            personal_id: ID del personal en tabla personal
            
        Returns:
            Lista de pacientes disponibles para nueva intervención
        """
        try:
            logger.info(f"Obteniendo pacientes disponibles para personal_id: {personal_id}")
            
            # Verificar permisos - usar consultas ya que manejamos consultas asignadas
            if not self.check_permission("consultas", "leer"):
                raise PermissionError("Sin permisos para acceder a las consultas")
            
            # Usar personal_id directamente
            print(f"[DEBUG] 🔄 Pacientes disponibles para personal_id: {personal_id}")
            
            # Por ahora, simplificar la lógica hasta implementar los métodos correctos
            logger.info("Funcionalidad de pacientes disponibles simplificada temporalmente")
            return []
            
        except PermissionError:
            logger.warning("Usuario sin permisos para ver pacientes disponibles")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo pacientes disponibles", e)
            return []
    
    async def iniciar_intervencion(self, consulta_id: str, odontologo_id: str, servicio_id: str) -> Dict[str, Any]:
        """
        🚀 Iniciar una nueva intervención
        
        Args:
            consulta_id: ID de la consulta
            odontologo_id: ID del odontólogo
            servicio_id: ID del servicio a realizar
            
        Returns:
            Datos de la intervención iniciada
        """
        try:
            logger.info(f"Iniciando intervención: consulta={consulta_id}, odontologo={odontologo_id}")
            
            # Verificar permisos
            self.require_permission("intervenciones", "crear")
            
            # Obtener precio base del servicio para cumplir restricción
            servicio_response = self.client.table("servicios").select("precio_base").eq("id", servicio_id).execute()
            precio_base = 50.00  # Precio por defecto
            if servicio_response.data:
                precio_base = float(servicio_response.data[0].get("precio_base", 50.00))
            
            print(f"[DEBUG] 💰 Precio base del servicio: {precio_base}")
            
            # CONVERSIÓN CRÍTICA: usuario_id → personal_id para intervención
            personal_id = self._get_personal_id_from_user_id(odontologo_id)
            print(f"[DEBUG] 🔄 Intervención: usuario {odontologo_id} → personal {personal_id}")
            
            # Crear nueva intervención en estado "en_progreso"
            intervencion = self.interventions_table.create_intervention(
                consulta_id=consulta_id,
                servicio_id=servicio_id,
                odontologo_id=personal_id,  # Usar personal_id convertido
                hora_inicio=datetime.now(),
                procedimiento_realizado="Intervención en progreso...",
                precio_acordado=precio_base,  # Usar precio del servicio
                precio_final=0.0,             # Se actualizará al finalizar
                estado="en_progreso"
            )
            
            # Actualizar estado de la consulta a "en_progreso" si no lo está
            consulta_actual = self.consultas_table.get_by_id(consulta_id)
            if consulta_actual and consulta_actual.get("estado") == "programada":
                self.consultas_table.update_status(consulta_id, "en_progreso")
            
            logger.info(f"✅ Intervención iniciada: {intervencion.get('id')}")
            
            # 🗑️ INVALIDAR CACHE - intervención iniciada afecta estadísticas del odontólogo
            try:
                invalidate_after_intervention_operation()
            except Exception as cache_error:
                logger.warning(f"Error invalidando cache tras iniciar intervención: {cache_error}")
            
            return intervencion
            
        except Exception as e:
            self.handle_error("Error iniciando intervención", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def finalizar_intervencion(self, intervencion_id: str, datos_intervencion: Dict[str, Any]) -> bool:
        """
        ✅ Finalizar una intervención en progreso
        
        Args:
            intervencion_id: ID de la intervención
            datos_intervencion: Datos finales de la intervención
            
        Returns:
            True si se finalizó correctamente
        """
        try:
            logger.info(f"Finalizando intervención: {intervencion_id}")
            
            # Verificar permisos
            self.require_permission("intervenciones", "actualizar")
            
            # Preparar datos para actualizar
            update_data = {
                "hora_fin": datetime.now().isoformat(),
                "procedimiento_realizado": datos_intervencion.get("procedimiento_realizado", ""),
                "precio_final": float(datos_intervencion.get("precio_final", "0")),
                "dientes_afectados": datos_intervencion.get("dientes_afectados", []),
                "materiales_utilizados": datos_intervencion.get("materiales_utilizados", []),
                "anestesia_utilizada": datos_intervencion.get("anestesia_utilizada", ""),
                "complicaciones": datos_intervencion.get("complicaciones", ""),
                "instrucciones_paciente": datos_intervencion.get("instrucciones_paciente", ""),
                "requiere_control": datos_intervencion.get("requiere_control") == "true" if isinstance(datos_intervencion.get("requiere_control"), str) else bool(datos_intervencion.get("requiere_control", False)),
                "fecha_control_sugerida": datos_intervencion.get("fecha_control_sugerida") if datos_intervencion.get("fecha_control_sugerida") and str(datos_intervencion.get("fecha_control_sugerida")).strip() else None,
                "estado": "completada"
            }
            
            # Actualizar la intervención
            result = self.interventions_table.update(intervencion_id, update_data)
            
            if result:
                logger.info(f"✅ Intervención finalizada: {intervencion_id}")
                
                # 🗑️ INVALIDAR CACHE - intervención finalizada afecta estadísticas e ingresos
                try:
                    invalidate_after_intervention_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras finalizar intervención: {cache_error}")
                
                return True
            else:
                raise ValueError("Error actualizando intervención en la base de datos")
                
        except Exception as e:
            self.handle_error("Error finalizando intervención", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def get_odontograma_paciente(self, paciente_id: str, odontologo_id: str) -> Dict[str, Any]:
        """
        🦷 Obtener odontograma activo del paciente
        
        Args:
            paciente_id: ID del paciente
            odontologo_id: ID del odontólogo
            
        Returns:
            Odontograma con condiciones actuales
        """
        try:
            logger.info(f"Obteniendo odontograma para paciente: {paciente_id}")
            
            # Verificar permisos
            self.require_permission("consultas", "leer")
            
            # Obtener odontograma activo
            odontograma = self.odontograms_table.get_active_odontogram(paciente_id)
            
            if not odontograma:
                # Crear odontograma inicial si no existe
                odontograma = self.odontograms_table.create_odontogram(
                    paciente_id=paciente_id,
                    odontologo_id=odontologo_id,
                    tipo_odontograma="adulto",
                    notas_generales="Odontograma inicial"
                )
            
            # Obtener condiciones de todos los dientes
            condiciones = self.odontograms_table.get_teeth_conditions(odontograma["id"])
            
            # Estructurar odontograma completo
            odontograma_completo = {
                **odontograma,
                "condiciones": condiciones,
                "condiciones_disponibles": CONDICIONES_DIENTE
            }
            
            logger.info(f"✅ Odontograma obtenido con {len(condiciones)} condiciones")
            return odontograma_completo
            
        except Exception as e:
            self.handle_error("Error obteniendo odontograma", e)
            return {}
    
    async def actualizar_condicion_diente(self, 
                                        paciente_id: str, 
                                        numero_diente: int, 
                                        cara: str, 
                                        condicion: str,
                                        odontologo_id: str,
                                        observaciones: str = "") -> bool:
        """
        🦷 Actualizar condición de una cara específica de un diente
        
        Args:
            paciente_id: ID del paciente
            numero_diente: Número del diente (11-48)
            cara: Cara del diente (incisal, oclusal, mesial, distal, vestibular, lingual, palatino)
            condicion: Nueva condición (sano, caries, obturado, etc.)
            odontologo_id: ID del odontólogo que hace el cambio
            observaciones: Observaciones adicionales
            
        Returns:
            True si se actualizó correctamente
        """
        try:
            logger.info(f"Actualizando diente {numero_diente}, cara {cara} → {condicion}")
            
            # Verificar permisos
            self.require_permission("intervenciones", "actualizar")
            
            # Validar condición
            if condicion not in CONDICIONES_DIENTE:
                raise ValueError(f"Condición inválida: {condicion}")
            
            # CONVERSIÓN CRÍTICA: usuario_id → personal_id
            personal_id = self._get_personal_id_from_user_id(odontologo_id)
            
            # Obtener odontograma activo
            odontograma = self.odontograms_table.get_active_odontogram(paciente_id)
            if not odontograma:
                # Crear odontograma si no existe
                odontograma = self.odontograms_table.create_odontogram(
                    paciente_id=paciente_id,
                    odontologo_id=personal_id,  # Usar personal_id convertido
                    tipo_odontograma="adulto"
                )
            
            # Actualizar condición específica
            success = self.odontograms_table.update_tooth_condition(
                odontograma_id=odontograma["id"],
                numero_diente=numero_diente,
                cara=cara,
                condicion=condicion,
                observaciones=observaciones,
                actualizado_por=odontologo_id  # Este campo podría ser de usuarios, no de personal
            )
            
            if success:
                logger.info(f"✅ Condición actualizada: diente {numero_diente} - {cara} - {condicion}")
                return True
            else:
                raise ValueError("Error actualizando condición en la base de datos")
                
        except Exception as e:
            self.handle_error("Error actualizando condición del diente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def get_historial_cambios_diente(self, paciente_id: str, numero_diente: int) -> List[Dict[str, Any]]:
        """
        📊 Obtener historial de cambios de un diente específico
        
        Args:
            paciente_id: ID del paciente
            numero_diente: Número del diente
            
        Returns:
            Historial de cambios ordenado cronológicamente
        """
        try:
            # Verificar permisos
            self.require_permission("consultas", "leer")
            
            # Obtener historial del diente
            historial = self.odontograms_table.get_tooth_history(paciente_id, numero_diente)
            
            logger.info(f"✅ Historial obtenido: diente {numero_diente} - {len(historial)} cambios")
            return historial
            
        except Exception as e:
            self.handle_error("Error obteniendo historial del diente", e)
            return []
    
    async def get_estadisticas_odontologo(self, personal_id: str) -> Dict[str, Any]:
        """
        📊 Obtener estadísticas del día para el odontólogo
        
        Args:
            personal_id: ID del personal en tabla personal
            
        Returns:
            Estadísticas del día
        """
        try:
            # Obtener estadísticas del día
            today = date.today()
            
            # Pacientes asignados usando personal_id directamente
            pacientes_asignados = await self.get_pacientes_asignados(personal_id)
            
            # Pacientes disponibles usando personal_id directamente
            pacientes_disponibles = await self.get_pacientes_disponibles(personal_id)
            
            # Estadísticas simplificadas por ahora
            intervenciones_completadas = []
            intervenciones_en_progreso = []
            tiempo_promedio = 0
            
            estadisticas = {
                "pacientes_asignados": len(pacientes_asignados),
                "pacientes_disponibles": len(pacientes_disponibles),
                "intervenciones_completadas": len(intervenciones_completadas),
                "intervenciones_en_progreso": len(intervenciones_en_progreso),
                "tiempo_promedio_minutos": round(tiempo_promedio, 1),
                "total_pacientes_atendidos": len(set(i.get("paciente_id") for i in intervenciones_completadas))
            }
            
            logger.info(f"✅ Estadísticas obtenidas para personal {personal_id}")
            return estadisticas
            
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas del odontólogo", e)
            return {
                "pacientes_asignados": 0,
                "pacientes_disponibles": 0,
                "intervenciones_completadas": 0,
                "intervenciones_en_progreso": 0,
                "tiempo_promedio_minutos": 0,
                "total_pacientes_atendidos": 0
            }

    # ==========================================
    # 🦷 MÉTODOS PARA ODONTOGRAMA INTERACTIVO - FASE 2
    # ==========================================

    async def get_or_create_patient_odontogram(self, paciente_id: str, odontologo_id: str) -> Dict[str, Any]:
        """
        🔄 Obtener o crear odontograma del paciente para interacción
        
        Args:
            paciente_id: ID del paciente
            odontologo_id: ID del odontólogo que creará/accederá
            
        Returns:
            Diccionario con estructura de odontograma y condiciones
        """
        try:
            # Verificar permisos de odontología
            if not self.check_permission("odontologia", "leer"):
                raise PermissionError("Sin permisos para acceder a odontogramas")
                
            # Buscar odontograma existente activo
            existing_odontogram = odontograms_table.get_active_by_patient(paciente_id)
            
            if existing_odontogram:
                # Cargar condiciones del odontograma existente
                conditions = condiciones_diente_table.get_by_odontogram_id(existing_odontogram['id'])
                
                # Organizar condiciones por diente y superficie
                organized_conditions = self._organize_conditions_by_tooth(conditions)
                
                logger.info(f"✅ Odontograma existente cargado para paciente {paciente_id}")
                return {
                    "id": existing_odontogram['id'],
                    "conditions": organized_conditions,
                    "version": existing_odontogram.get('version', 1),
                    "is_new": False
                }
            else:
                # Crear nuevo odontograma con condiciones "sano" por defecto
                new_odontogram_data = {
                    "paciente_id": paciente_id,
                    "odontologo_id": odontologo_id,
                    "tipo_odontograma": "adulto",
                    "activo": True,
                    "notas_generales": "",
                    "template_usado": "universal"
                }
                
                new_odontogram = odontograms_table.create(new_odontogram_data)
                
                # Crear condiciones iniciales "sano" para todos los 32 dientes
                initial_conditions = self._create_initial_tooth_conditions(new_odontogram['id'])
                
                logger.info(f"✅ Nuevo odontograma creado para paciente {paciente_id}")
                return {
                    "id": new_odontogram['id'],
                    "conditions": initial_conditions,
                    "version": 1,
                    "is_new": True
                }
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo/creando odontograma: {str(e)}")
            raise ValueError(f"Error de odontograma: {str(e)}")

    async def save_odontogram_conditions(self, odontogram_id: str, conditions_changes: Dict[int, Dict[str, str]]) -> bool:
        """
        💾 Guardar cambios de condiciones del odontograma en base de datos
        
        Args:
            odontogram_id: ID del odontograma
            conditions_changes: Diccionario {diente_num: {superficie: condicion}}
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            if not self.check_permission("odontologia", "actualizar"):
                raise PermissionError("Sin permisos para actualizar odontogramas")
                
            success_count = 0
            error_count = 0
            
            # Procesar cada diente con cambios
            for tooth_number, surfaces in conditions_changes.items():
                try:
                    # Obtener información del diente desde catálogo
                    tooth_info = dientes_table.get_by_numero(tooth_number)
                    if not tooth_info:
                        logger.warning(f"⚠️ Diente {tooth_number} no encontrado en catálogo FDI")
                        continue
                    
                    # Procesar cada superficie del diente
                    for surface_name, new_condition in surfaces.items():
                        try:
                            # Buscar condición existente para esta superficie
                            existing_condition = condiciones_diente_table.get_condition_by_surface(
                                odontogram_id, str(tooth_info['id']), surface_name
                            )
                            
                            condition_data = {
                                "odontograma_id": odontogram_id,
                                "diente_id": str(tooth_info['id']),
                                "tipo_condicion": new_condition,
                                "caras_afectadas": [surface_name],
                                "estado": "actual",
                                "fecha_registro": datetime.now().isoformat(),
                                "registrado_por": self.user_id
                            }
                            
                            if existing_condition:
                                # Actualizar condición existente
                                updated = condiciones_diente_table.update(existing_condition['id'], {
                                    "tipo_condicion": new_condition,
                                    "fecha_registro": datetime.now().isoformat(),
                                    "registrado_por": self.user_id
                                })
                                if updated:
                                    success_count += 1
                            else:
                                # Crear nueva condición
                                created = condiciones_diente_table.create_condicion(
                                    odontogram_id=odontogram_id,
                                    diente_id=str(tooth_info['id']),
                                    tipo_condicion=new_condition,
                                    registrado_por=self.user_id,
                                    caras_afectadas=[surface_name]
                                )
                                if created:
                                    success_count += 1
                                    
                        except Exception as surface_error:
                            logger.error(f"❌ Error guardando superficie {surface_name} diente {tooth_number}: {surface_error}")
                            error_count += 1
                            
                except Exception as tooth_error:
                    logger.error(f"❌ Error procesando diente {tooth_number}: {tooth_error}")
                    error_count += 1
            
            # Actualizar timestamp del odontograma
            odontograms_table.update(odontogram_id, {
                "fecha_ultima_actualizacion": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Odontograma guardado: {success_count} cambios exitosos, {error_count} errores")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error guardando odontograma: {str(e)}")
            raise ValueError(f"Error guardando cambios: {str(e)}")

    def _organize_conditions_by_tooth(self, conditions: List[Dict[str, Any]]) -> Dict[int, Dict[str, str]]:
        """
        🗂️ Organizar condiciones de BD en estructura por diente y superficie
        
        Args:
            conditions: Lista de condiciones desde BD
            
        Returns:
            Diccionario {numero_diente: {superficie: condicion}}
        """
        organized = {}
        
        for condition in conditions:
            try:
                # Obtener información del diente
                diente_info = dientes_table.get_by_id(condition['diente_id'])
                if not diente_info:
                    continue
                
                tooth_number = diente_info['numero_diente']
                condition_type = condition['tipo_condicion']
                affected_surfaces = condition.get('caras_afectadas', [])
                
                if tooth_number not in organized:
                    organized[tooth_number] = {}
                
                # Asignar condición a cada superficie afectada
                for surface in affected_surfaces:
                    organized[tooth_number][surface] = condition_type
                    
            except Exception as e:
                logger.warning(f"⚠️ Error procesando condición: {e}")
                continue
        
        return organized

    def _create_initial_tooth_conditions(self, odontogram_id: str) -> Dict[int, Dict[str, str]]:
        """
        🦷 Crear condiciones iniciales "sano" para todos los 32 dientes FDI
        
        Args:
            odontogram_id: ID del odontograma recién creado
            
        Returns:
            Diccionario con condiciones iniciales organizadas
        """
        # Números FDI de 32 dientes permanentes
        adult_teeth_fdi = [
            # Cuadrante 1 (Superior Derecho): 18-11
            18, 17, 16, 15, 14, 13, 12, 11,
            # Cuadrante 2 (Superior Izquierdo): 21-28
            21, 22, 23, 24, 25, 26, 27, 28,
            # Cuadrante 3 (Inferior Izquierdo): 31-38
            31, 32, 33, 34, 35, 36, 37, 38,
            # Cuadrante 4 (Inferior Derecho): 41-48
            41, 42, 43, 44, 45, 46, 47, 48
        ]
        
        # 5 superficies por diente
        surfaces = ["oclusal", "mesial", "distal", "vestibular", "lingual"]
        
        initial_conditions = {}
        
        for tooth_number in adult_teeth_fdi:
            try:
                # Obtener información del diente del catálogo
                tooth_info = dientes_table.get_by_numero(tooth_number)
                if not tooth_info:
                    logger.warning(f"⚠️ Diente {tooth_number} no encontrado en catálogo")
                    continue
                
                initial_conditions[tooth_number] = {}
                
                # Crear condición "sano" para cada superficie
                for surface in surfaces:
                    try:
                        condiciones_diente_table.create_condicion(
                            odontogram_id=odontogram_id,
                            diente_id=str(tooth_info['id']),
                            tipo_condicion="sano",
                            registrado_por=self.user_id,
                            caras_afectadas=[surface],
                            descripcion=f"Condición inicial para {surface}",
                            estado="actual"
                        )
                        
                        initial_conditions[tooth_number][surface] = "sano"
                        
                    except Exception as surface_error:
                        logger.error(f"❌ Error creando condición inicial para diente {tooth_number} superficie {surface}: {surface_error}")
                
            except Exception as tooth_error:
                logger.error(f"❌ Error creando condiciones para diente {tooth_number}: {tooth_error}")
        
        logger.info(f"✅ Condiciones iniciales creadas para {len(initial_conditions)} dientes")
        return initial_conditions

    async def get_tooth_condition_history(self, paciente_id: str, tooth_number: int, surface: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        📜 Obtener historial de condiciones de un diente específico
        
        Args:
            paciente_id: ID del paciente
            tooth_number: Número FDI del diente
            surface: Superficie específica (opcional)
            
        Returns:
            Lista de condiciones históricas ordenadas por fecha
        """
        try:
            if not self.check_permission("odontologia", "leer"):
                raise PermissionError("Sin permisos para leer historiales odontológicos")
            
            # Obtener odontograma(s) del paciente
            patient_odontograms = odontograms_table.get_all_by_patient(paciente_id)
            
            history = []
            for odontogram in patient_odontograms:
                # Obtener condiciones de este diente en este odontograma
                conditions = condiciones_diente_table.get_tooth_conditions_history(
                    odontogram['id'], tooth_number, surface
                )
                history.extend(conditions)
            
            # Ordenar por fecha de registro
            history.sort(key=lambda x: x.get('fecha_registro', ''), reverse=True)
            
            return history
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo historial de diente: {str(e)}")
            return []

    async def get_historial_paciente_completo(self, paciente_id: str) -> List[Dict[str, Any]]:
        """
        📜 Obtener historial clínico completo del paciente
        
        Args:
            paciente_id: ID del paciente
            
        Returns:
            Lista de entradas del historial médico completo
        """
        try:
            logger.info(f"Obteniendo historial completo para paciente: {paciente_id}")
            
            # Verificar permisos
            if not self.check_permission("consultas", "leer"):
                raise PermissionError("Sin permisos para leer historial de pacientes")
            
            # Obtener historial médico desde la tabla historial_medico
            try:
                historial_response = self.client.table("historial_medico") \
                    .select("*") \
                    .eq("paciente_id", paciente_id) \
                    .order("fecha_registro", desc=True) \
                    .execute()
                
                historial_medico = historial_response.data if historial_response.data else []
            except Exception as e:
                logger.warning(f"Error obteniendo historial médico: {e}")
                historial_medico = []
            
            # Obtener intervenciones relacionadas
            try:
                intervenciones_response = self.client.table("intervenciones") \
                    .select("*, consultas(fecha_programada, motivo_consulta)") \
                    .eq("paciente_id", paciente_id) \
                    .order("fecha_inicio", desc=True) \
                    .execute()
                
                intervenciones = intervenciones_response.data if intervenciones_response.data else []
            except Exception as e:
                logger.warning(f"Error obteniendo intervenciones: {e}")
                intervenciones = []
            
            # Combinar historial médico e intervenciones
            historial_completo = []
            
            # Agregar entradas del historial médico
            for entrada in historial_medico:
                historial_completo.append({
                    "id": entrada.get("id"),
                    "tipo": "historial_medico",
                    "fecha": entrada.get("fecha_registro"),
                    "titulo": entrada.get("tipo_entrada", "Entrada médica"),
                    "descripcion": entrada.get("descripcion", ""),
                    "datos_adicionales": entrada.get("datos_adicionales", {}),
                    "registrado_por": entrada.get("registrado_por", "")
                })
            
            # Agregar intervenciones como entradas de historial
            for intervencion in intervenciones:
                consulta_info = intervencion.get("consultas", {})
                historial_completo.append({
                    "id": intervencion.get("id"),
                    "tipo": "intervencion",
                    "fecha": intervencion.get("fecha_inicio"),
                    "titulo": f"Intervención - {consulta_info.get('motivo_consulta', 'Sin especificar')}",
                    "descripcion": intervencion.get("procedimiento_realizado", ""),
                    "datos_adicionales": {
                        "precio_final": intervencion.get("precio_final"),
                        "dientes_afectados": intervencion.get("dientes_afectados", []),
                        "materiales": intervencion.get("materiales_utilizados", []),
                        "estado": intervencion.get("estado")
                    },
                    "registrado_por": intervencion.get("odontologo_id", "")
                })
            
            # Ordenar todo el historial por fecha (más reciente primero)
            historial_completo.sort(
                key=lambda x: x.get("fecha") or "", 
                reverse=True
            )
            
            logger.info(f"✅ Historial completo obtenido: {len(historial_completo)} entradas")
            return historial_completo
            
        except PermissionError:
            logger.warning("Usuario sin permisos para leer historial completo")
            raise
        except Exception as e:
            logger.error(f"❌ Error obteniendo historial completo: {str(e)}")
            return []

    async def crear_intervencion_con_servicios(self, datos_intervencion: Dict[str, Any]) -> Dict[str, Any]:
        """
        💾 Crear intervención con múltiples servicios (nueva implementación para shopping cart)
        
        Args:
            datos_intervencion: {
                "consulta_id": str,
                "odontologo_id": str,  # ID del usuario (se convertirá a personal_id)
                "servicios": [
                    {
                        "servicio_id": str,
                        "cantidad": int,
                        "precio_unitario_bs": float,
                        "precio_unitario_usd": float,
                        "dientes_texto": str,
                        "observaciones": str
                    }
                ],
                "observaciones_generales": str
            }
            
        Returns:
            Dict con información de la intervención creada
        """
        try:
            logger.info(f"🚀 Iniciando creación de intervención con servicios")
            
            # Verificar permisos
            self.require_permission("intervenciones", "crear")
            
            # Validaciones básicas
            consulta_id = datos_intervencion.get("consulta_id")
            if not consulta_id:
                raise ValueError("consulta_id es requerido")
            
            servicios = datos_intervencion.get("servicios", [])
            if not servicios:
                raise ValueError("Al menos un servicio es requerido")
            
            odontologo_user_id = datos_intervencion.get("odontologo_id")
            if not odontologo_user_id:
                raise ValueError("odontologo_id es requerido")
            
            # CONVERSIÓN CRÍTICA: usuario_id → personal_id
            personal_id = self._get_personal_id_from_user_id(odontologo_user_id)
            logger.info(f"🔄 Conversión: usuario {odontologo_user_id} → personal {personal_id}")
            
            # Calcular totales desde los servicios
            total_bs = sum(
                float(servicio.get("precio_unitario_bs", 0)) * int(servicio.get("cantidad", 1)) 
                for servicio in servicios
            )
            total_usd = sum(
                float(servicio.get("precio_unitario_usd", 0)) * int(servicio.get("cantidad", 1)) 
                for servicio in servicios
            )
            
            logger.info(f"💰 Totales calculados: BS {total_bs:,.2f}, USD ${total_usd:,.2f}")
            
            # Crear la intervención principal
            intervencion_data = {
                "consulta_id": consulta_id,
                "odontologo_id": personal_id,  # Usar personal_id convertido
                "procedimiento_realizado": datos_intervencion.get("observaciones_generales", f"Intervención con {len(servicios)} servicios"),
                "total_bs": float(total_bs),  # Convertir a float para BD
                "total_usd": float(total_usd), # Convertir a float para BD
                "hora_inicio": datetime.now().isoformat(),  # Convertir a string ISO
                "hora_fin": datetime.now().isoformat(),    # Convertir a string ISO
                "estado": "completada",
                "requiere_control": datos_intervencion.get("requiere_control", False)
            }
            
            # Recopilar dientes afectados de todos los servicios
            dientes_todos = []
            for servicio in servicios:
                dientes_texto = servicio.get("dientes_texto", "")
                if dientes_texto.strip():
                    # Parse dientes: "11, 12, 21" → [11, 12, 21]
                    try:
                        dientes_servicio = [
                            int(d.strip()) for d in dientes_texto.split(",") 
                            if d.strip().isdigit()
                        ]
                        dientes_todos.extend(dientes_servicio)
                    except:
                        logger.warning(f"Error parseando dientes: {dientes_texto}")
            
            # Remover duplicados y ordenar
            dientes_unicos = sorted(list(set(dientes_todos)))
            intervencion_data["dientes_afectados"] = dientes_unicos
            
            logger.info(f"🦷 Dientes afectados: {dientes_unicos}")
            
            # Crear la intervención usando el método directo de BaseTable ya que create_intervention 
            # no está sincronizado con la estructura de BD actual
            nueva_intervencion = self.interventions_table.create(intervencion_data)
            
            if not nueva_intervencion or not nueva_intervencion.get("id"):
                raise ValueError("Error creando intervención principal")
                
            intervencion_id = nueva_intervencion["id"]
            logger.info(f"✅ Intervención principal creada: {intervencion_id}")
            
            # ✅ Crear registros en intervenciones_servicios para cada servicio del shopping cart
            servicios_creados = 0
            for servicio in servicios:
                try:
                    # Datos del servicio individual
                    cantidad = int(servicio.get("cantidad", 1))
                    precio_unitario_bs = float(servicio.get("precio_unitario_bs", 0))
                    precio_unitario_usd = float(servicio.get("precio_unitario_usd", 0))
                    precio_total_bs = cantidad * precio_unitario_bs
                    precio_total_usd = cantidad * precio_unitario_usd
                    
                    # Parsear dientes específicos para este servicio
                    dientes_texto = servicio.get("dientes_texto", "")
                    dientes_especificos = []
                    if dientes_texto.strip():
                        try:
                            dientes_especificos = [
                                int(d.strip()) for d in dientes_texto.split(",") 
                                if d.strip().isdigit()
                            ]
                        except:
                            logger.warning(f"Error parseando dientes del servicio: {dientes_texto}")
                    
                    # Crear registro en intervenciones_servicios
                    servicio_data = {
                        "intervencion_id": intervencion_id,
                        "servicio_id": servicio.get("servicio_id"),
                        "cantidad": cantidad,
                        "precio_unitario_bs": precio_unitario_bs,
                        "precio_unitario_usd": precio_unitario_usd,
                        "precio_total_bs": precio_total_bs,
                        "precio_total_usd": precio_total_usd,
                        "dientes_especificos": dientes_especificos,
                        "observaciones_servicio": servicio.get("observaciones", "")
                    }
                    
                    # Insertar usando cliente directo de Supabase
                    response = self.client.table("intervenciones_servicios").insert(servicio_data).execute()
                    
                    if response.data:
                        servicios_creados += 1
                        logger.info(f"✅ Servicio creado en BD: {servicio.get('servicio_id')} x{cantidad}")
                    else:
                        logger.error(f"❌ Error creando servicio: {servicio.get('servicio_id')}")
                        
                except Exception as e:
                    logger.error(f"❌ Error procesando servicio individual: {e}")
                    continue
            
            logger.info(f"📋 Servicios creados en intervenciones_servicios: {servicios_creados}/{len(servicios)}")
            
            # Verificar que se crearon todos los servicios
            if servicios_creados != len(servicios):
                logger.warning(f"⚠️ Solo se crearon {servicios_creados} de {len(servicios)} servicios")
            
            # Generar descripción detallada de servicios
            descripcion_servicios = []
            for i, servicio in enumerate(servicios, 1):
                # Obtener nombre del servicio
                servicio_info = self.services_table.get_by_id(servicio.get("servicio_id"))
                nombre_servicio = servicio_info.get("nombre", "Servicio desconocido") if servicio_info else "Servicio desconocido"
                
                descripcion = f"{i}. {nombre_servicio}"
                if servicio.get("cantidad", 1) > 1:
                    descripcion += f" (x{servicio.get('cantidad')})"
                if servicio.get("dientes_texto"):
                    descripcion += f" - Dientes: {servicio.get('dientes_texto')}"
                
                precios = []
                if servicio.get("precio_unitario_bs", 0) > 0:
                    precios.append(f"{servicio.get('precio_unitario_bs'):,.0f} Bs")
                if servicio.get("precio_unitario_usd", 0) > 0:
                    precios.append(f"${servicio.get('precio_unitario_usd'):,.0f}")
                
                if precios:
                    descripcion += f" - {' / '.join(precios)}"
                
                if servicio.get("observaciones"):
                    descripcion += f" - {servicio.get('observaciones')}"
                
                descripcion_servicios.append(descripcion)
            
            # Actualizar procedimiento_realizado con detalles
            procedimiento_detallado = (
                f"{datos_intervencion.get('observaciones_generales', 'Intervención múltiple')}\n\n"
                f"Servicios realizados:\n" + "\n".join(descripcion_servicios)
            )
            
            # Actualizar la intervención con la descripción completa
            self.interventions_table.update(intervencion_id, {
                "procedimiento_realizado": procedimiento_detallado
            })
            
            # Actualizar estado de la consulta a completada
            self.consultas_table.update_status(consulta_id, "completada")
            logger.info(f"✅ Consulta {consulta_id} marcada como completada")
            
            # Invalidar caché
            try:
                invalidate_after_intervention_operation()
            except Exception as cache_error:
                logger.warning(f"Error invalidando cache: {cache_error}")
            
            logger.info(f"🎉 Intervención con servicios completada exitosamente: {intervencion_id}")
            
            return {
                "success": True,
                "intervencion_id": intervencion_id,
                "total_bs": total_bs,
                "total_usd": total_usd,
                "servicios_count": len(servicios),
                "servicios_creados": servicios_creados,
                "dientes_afectados": dientes_unicos,
                "message": f"Intervención creada con {servicios_creados}/{len(servicios)} servicios guardados"
            }
            
        except PermissionError:
            logger.error("❌ Sin permisos para crear intervención")
            raise
        except Exception as e:
            logger.error(f"❌ Error creando intervención con servicios: {str(e)}")
            raise ValueError(f"Error inesperado: {str(e)}")

# Instancia única para importar
odontologia_service = OdontologiaService()