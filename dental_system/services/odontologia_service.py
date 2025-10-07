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
                                     if k not in ['id', 'numero_consulta', 'estado', 'fecha_llegada', 'odontologo_id', 'motivo_consulta', 'tipo_consulta', 'tipo_asignacion']}
                    
                    # El ID del paciente está en paciente_id, no en id (que es consulta_id)
                    campos_paciente['id'] = paciente_data.get("paciente_id", "")
                    
                    paciente_model = PacienteModel.from_dict(campos_paciente)
                    
                    # Agregar información de consulta como atributos temporales
                    paciente_model._consulta_id = paciente_data.get("id", "")  # ID de la consulta
                    paciente_model._estado_consulta = paciente_data.get("estado", "")
                    paciente_model._numero_consulta = paciente_data.get("numero_consulta", "")
                    paciente_model._fecha_consulta = paciente_data.get("fecha_llegada", "")
                    
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
            
            # ✅ FIX: Obtener odontograma completo con condiciones usando método correcto
            odontograma_completo = self.odontograms_table.get_odontogram_with_conditions(odontograma["id"])

            if not odontograma_completo:
                # Si no hay odontograma completo, usar el básico
                odontograma_completo = {
                    **odontograma,
                    "condiciones": [],
                    "condiciones_disponibles": CONDICIONES_DIENTE
                }
            else:
                # Agregar condiciones disponibles
                odontograma_completo["condiciones_disponibles"] = CONDICIONES_DIENTE
            
            condiciones_count = len(odontograma_completo.get("condiciones", []))
            logger.info(f"✅ Odontograma obtenido con {condiciones_count} condiciones")
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
            # # Verificar permisos de odontología
            # if not self.check_permission("odontograma", "leer"):
            #     raise PermissionError("Sin permisos para acceder a odontogramas")
                
            # Buscar odontograma existente activo
            existing_odontogram = odontograms_table.get_active_odontogram(paciente_id)
            
            if existing_odontogram:
                # Cargar condiciones del odontograma existente
                conditions = condiciones_diente_table.get_by_odontograma(existing_odontogram['id'])
                
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
                user_role = self._extract_user_role()
                error_msg = (
                    f"❌ PERMISO DENEGADO: Rol '{user_role}' no puede actualizar odontogramas.\n"
                    f"✅ Roles autorizados: 'gerente' o 'odontologo'"
                )
                logger.error(error_msg)
                raise PermissionError(error_msg)

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

    # ==========================================
    # 🚀 MÉTODOS V3.0 - FASE 3: VERSIONADO AUTOMÁTICO
    # ==========================================

    async def detectar_cambios_significativos(
        self,
        condiciones_anteriores: Dict[int, Dict[str, str]],
        condiciones_nuevas: Dict[int, Dict[str, str]]
    ) -> Tuple[bool, List[Dict[str, Any]], str]:
        """
        🔍 FASE 3.1: Detectar si los cambios ameritan nueva versión del odontograma

        Criterios para nueva versión:
        1. Cambio de "sano" a condición crítica
        2. Cambio entre condiciones críticas diferentes
        3. 5+ superficies modificadas (threshold)
        4. Cualquier extracción o ausencia

        Args:
            condiciones_anteriores: Estado previo {diente: {superficie: condicion}}
            condiciones_nuevas: Estado nuevo {diente: {superficie: condicion}}

        Returns:
            (requiere_nueva_version, lista_cambios_criticos, motivo_resumen)
        """
        # Condiciones críticas que requieren versionado
        CONDICIONES_CRITICAS = {
            "caries", "extraccion", "ausente", "fractura",
            "implante", "endodoncia"
        }

        cambios_criticos = []
        total_cambios = 0

        # Analizar todos los dientes modificados
        for tooth_num, surfaces_nuevas in condiciones_nuevas.items():
            condiciones_prev = condiciones_anteriores.get(tooth_num, {})

            for surface, nueva_condicion in surfaces_nuevas.items():
                condicion_prev = condiciones_prev.get(surface, "sano")

                # Contar todos los cambios
                if condicion_prev != nueva_condicion:
                    total_cambios += 1

                    # REGLA 1: Sano → Crítico (deterioro)
                    if condicion_prev == "sano" and nueva_condicion in CONDICIONES_CRITICAS:
                        cambios_criticos.append({
                            "diente": tooth_num,
                            "superficie": surface,
                            "antes": condicion_prev,
                            "despues": nueva_condicion,
                            "tipo": "deterioro_critico",
                            "descripcion": f"Diente {tooth_num} {surface}: {condicion_prev} → {nueva_condicion}"
                        })

                    # REGLA 2: Crítico → Otro Crítico (cambio importante)
                    elif (condicion_prev in CONDICIONES_CRITICAS and
                          nueva_condicion in CONDICIONES_CRITICAS and
                          condicion_prev != nueva_condicion):
                        cambios_criticos.append({
                            "diente": tooth_num,
                            "superficie": surface,
                            "antes": condicion_prev,
                            "despues": nueva_condicion,
                            "tipo": "cambio_critico",
                            "descripcion": f"Diente {tooth_num} {surface}: {condicion_prev} → {nueva_condicion}"
                        })

                    # REGLA 3: Extracción o ausencia (siempre crítico)
                    elif nueva_condicion in ["extraccion", "ausente"]:
                        cambios_criticos.append({
                            "diente": tooth_num,
                            "superficie": surface,
                            "antes": condicion_prev,
                            "despues": nueva_condicion,
                            "tipo": "perdida_dental",
                            "descripcion": f"Diente {tooth_num}: marcado como {nueva_condicion}"
                        })

        # Determinar si requiere nueva versión
        requiere_version = False
        motivo = ""

        if len(cambios_criticos) > 0:
            requiere_version = True
            if len(cambios_criticos) == 1:
                motivo = f"Cambio crítico: {cambios_criticos[0]['descripcion']}"
            else:
                motivo = f"Cambios críticos en {len(cambios_criticos)} superficies"

        # REGLA 4: Muchos cambios aunque no sean críticos (threshold)
        elif total_cambios >= 5:
            requiere_version = True
            motivo = f"Actualización masiva: {total_cambios} superficies modificadas"

        logger.info(
            f"🔍 Detección de cambios: {total_cambios} totales, "
            f"{len(cambios_criticos)} críticos, "
            f"requiere versión: {requiere_version}"
        )

        return (requiere_version, cambios_criticos, motivo)

    async def crear_nueva_version_odontograma(
        self,
        odontograma_actual_id: str,
        paciente_id: str,
        odontologo_id: str,
        intervencion_id: Optional[str],
        cambios_criticos: List[Dict[str, Any]],
        motivo: str
    ) -> Dict[str, Any]:
        """
        📚 FASE 3.2: Crear nueva versión del odontograma con versionado automático

        Proceso:
        1. Obtener versión actual
        2. Marcar versión actual como histórica
        3. Crear nueva versión con número incrementado
        4. Copiar condiciones actuales a nueva versión
        5. Registrar cambios críticos en metadata
        6. Vincular con intervención

        Args:
            odontograma_actual_id: ID del odontograma actual
            paciente_id: ID del paciente
            odontologo_id: ID del odontólogo que hace los cambios
            intervencion_id: ID de la intervención que origina el cambio
            cambios_criticos: Lista de cambios que justifican la versión
            motivo: Descripción del motivo de la nueva versión

        Returns:
            Diccionario con información de la nueva versión creada
        """
        try:
            # 1. Obtener odontograma actual
            odontograma_actual = odontograms_table.get_by_id(odontograma_actual_id)
            if not odontograma_actual:
                raise ValueError(f"Odontograma {odontograma_actual_id} no encontrado")

            version_actual = odontograma_actual.get("version", 1)

            logger.info(f"📚 Creando nueva versión del odontograma (v{version_actual} → v{version_actual + 1})")

            # 2. Marcar versión actual como histórica
            odontograms_table.update(odontograma_actual_id, {
                "es_version_actual": False,
                "fecha_archivado": datetime.now().isoformat()
            })

            # 3. Crear nueva versión
            nueva_version_data = {
                "numero_historia": paciente_id,
                "version": version_actual + 1,
                "id_version_anterior": odontograma_actual_id,
                "id_intervencion_origen": intervencion_id,
                "es_version_actual": True,
                "motivo_nueva_version": motivo,
                "odontologo_id": odontologo_id,
                "tipo_odontograma": odontograma_actual.get("tipo_odontograma", "adulto"),
                "fecha_creacion": datetime.now().isoformat(),
                "notas_generales": odontograma_actual.get("notas_generales", ""),
                "template_usado": odontograma_actual.get("template_usado", "universal")
            }

            nueva_version = odontograms_table.create(nueva_version_data)

            if not nueva_version:
                raise ValueError("Error creando nueva versión del odontograma")

            # 4. Copiar condiciones actuales a nueva versión
            condiciones_actuales = condiciones_diente_table.get_by_odontogram_id(
                odontograma_actual_id,
                estado="actual"
            )

            condiciones_copiadas = 0
            for condicion in condiciones_actuales:
                try:
                    condiciones_diente_table.create_condicion(
                        odontogram_id=nueva_version["id"],
                        diente_id=condicion["diente_id"],
                        tipo_condicion=condicion["tipo_condicion"],
                        registrado_por=odontologo_id,
                        caras_afectadas=condicion.get("caras_afectadas", [])
                    )
                    condiciones_copiadas += 1
                except Exception as e:
                    logger.warning(f"⚠️ Error copiando condición: {e}")

            logger.info(
                f"✅ Nueva versión creada: v{nueva_version['version']} "
                f"({condiciones_copiadas} condiciones copiadas)"
            )

            return {
                "id": nueva_version["id"],
                "version": nueva_version["version"],
                "version_anterior_id": odontograma_actual_id,
                "motivo": motivo,
                "cambios_criticos": cambios_criticos,
                "total_condiciones": condiciones_copiadas,
                "fecha_creacion": nueva_version["fecha_creacion"]
            }

        except Exception as e:
            logger.error(f"❌ Error creando nueva versión: {e}")
            raise ValueError(f"Error en versionado: {str(e)}")

    # ==========================================
    # 📜 MÉTODOS V3.0 - FASE 4: HISTORIAL TIMELINE
    # ==========================================

    async def get_odontogram_full_history(
        self,
        paciente_id: str
    ) -> List[Dict[str, Any]]:
        """
        📜 FASE 4.1: Obtener historial completo de odontogramas con comparación

        Retorna todas las versiones del odontograma del paciente,
        ordenadas de más reciente a más antigua, con:
        - Información de cada versión
        - Condiciones de esa versión
        - Cambios respecto a versión anterior
        - Estadísticas de dientes afectados

        Args:
            paciente_id: ID del paciente

        Returns:
            Lista de versiones con toda la información
        """
        try:
            # 1. Obtener todas las versiones del paciente
            versiones = odontograms_table.get_all_by_patient(paciente_id)

            if not versiones:
                logger.info(f"ℹ️ No hay historial de odontogramas para paciente {paciente_id}")
                return []

            # 2. Ordenar por versión descendente (más reciente primero)
            versiones_ordenadas = sorted(
                versiones,
                key=lambda x: x.get("version", 0),
                reverse=True
            )

            # 3. Procesar cada versión
            historial_completo = []

            for i, version in enumerate(versiones_ordenadas):
                try:
                    # Información básica de la versión
                    version_data = {
                        "id": version["id"],
                        "version": version.get("version", 1),
                        "fecha": version.get("fecha_creacion", ""),
                        "odontologo_id": version.get("odontologo_id", ""),
                        "odontologo_nombre": await self._get_odontologo_nombre(version.get("odontologo_id")),
                        "motivo": version.get("motivo_nueva_version", "Versión inicial"),
                        "intervencion_id": version.get("id_intervencion_origen"),
                        "es_version_actual": version.get("es_version_actual", False),
                        "tipo_odontograma": version.get("tipo_odontograma", "adulto")
                    }

                    # Obtener condiciones de esta versión
                    condiciones = condiciones_diente_table.get_by_odontogram_id(
                        version["id"],
                        estado="actual"
                    )

                    version_data["condiciones"] = self._organize_conditions_by_tooth(condiciones)
                    version_data["total_dientes_afectados"] = len(version_data["condiciones"])

                    # Calcular diferencias con versión anterior
                    if i < len(versiones_ordenadas) - 1:
                        version_anterior = versiones_ordenadas[i + 1]
                        condiciones_anteriores = condiciones_diente_table.get_by_odontogram_id(
                            version_anterior["id"],
                            estado="actual"
                        )

                        condiciones_ant_org = self._organize_conditions_by_tooth(condiciones_anteriores)

                        version_data["cambios_vs_anterior"] = self._calcular_diferencias(
                            condiciones_ant_org,
                            version_data["condiciones"]
                        )
                    else:
                        version_data["cambios_vs_anterior"] = []

                    historial_completo.append(version_data)

                except Exception as e:
                    logger.warning(f"⚠️ Error procesando versión {version.get('id')}: {e}")
                    continue

            logger.info(f"✅ Historial completo obtenido: {len(historial_completo)} versiones")
            return historial_completo

        except Exception as e:
            logger.error(f"❌ Error obteniendo historial completo: {e}")
            return []

    def _calcular_diferencias(
        self,
        condiciones_anteriores: Dict[int, Dict[str, str]],
        condiciones_nuevas: Dict[int, Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        🔍 Calcular diferencias entre dos versiones del odontograma

        Args:
            condiciones_anteriores: Condiciones de versión anterior
            condiciones_nuevas: Condiciones de versión actual

        Returns:
            Lista de diferencias detectadas
        """
        diferencias = []

        # Todos los dientes que aparecen en cualquiera de las dos versiones
        todos_dientes = set(list(condiciones_anteriores.keys()) + list(condiciones_nuevas.keys()))

        for tooth_num in todos_dientes:
            cond_prev = condiciones_anteriores.get(tooth_num, {})
            cond_nueva = condiciones_nuevas.get(tooth_num, {})

            # Todas las superficies afectadas
            todas_superficies = set(list(cond_prev.keys()) + list(cond_nueva.keys()))

            for surface in todas_superficies:
                valor_prev = cond_prev.get(surface, "sano")
                valor_nuevo = cond_nueva.get(surface, "sano")

                if valor_prev != valor_nuevo:
                    tipo_cambio = self._clasificar_cambio(valor_prev, valor_nuevo)

                    diferencias.append({
                        "diente": tooth_num,
                        "superficie": surface,
                        "antes": valor_prev,
                        "despues": valor_nuevo,
                        "tipo_cambio": tipo_cambio,
                        "descripcion": f"Diente {tooth_num} {surface}: {valor_prev} → {valor_nuevo}"
                    })

        return diferencias

    def _clasificar_cambio(self, antes: str, despues: str) -> str:
        """
        🏷️ Clasificar el tipo de cambio entre dos condiciones

        Args:
            antes: Condición anterior
            despues: Condición nueva

        Returns:
            Tipo de cambio: deterioro, mejora, modificacion, sin_cambio
        """
        CONDICIONES_CRITICAS = {"caries", "fractura", "extraccion", "ausente"}
        CONDICIONES_TRATAMIENTO = {"obturado", "corona", "endodoncia", "implante"}

        # Deterioro: sano → crítico
        if antes == "sano" and despues in CONDICIONES_CRITICAS:
            return "deterioro"

        # Mejora: crítico → tratamiento o sano
        elif antes in CONDICIONES_CRITICAS and (despues in CONDICIONES_TRATAMIENTO or despues == "sano"):
            return "mejora"

        # Sin cambio
        elif antes == despues:
            return "sin_cambio"

        # Modificación (otros casos)
        else:
            return "modificacion"

    async def _get_odontologo_nombre(self, odontologo_id: Optional[str]) -> str:
        """
        👨‍⚕️ Obtener nombre del odontólogo

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Nombre completo del odontólogo
        """
        if not odontologo_id:
            return "Desconocido"

        try:
            from dental_system.supabase.tablas import personal_table
            personal = personal_table.get_by_id(odontologo_id)

            if personal:
                nombre = f"{personal.get('primer_nombre', '')} {personal.get('primer_apellido', '')}"
                return nombre.strip()

            return "Desconocido"

        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo nombre odontólogo: {e}")
            return "Desconocido"

    # ==========================================
    # 🛡️ FASE 5: VALIDACIONES MÉDICAS
    # ==========================================

    def validar_cambios_odontograma(
        self,
        condiciones_anteriores: Dict[int, Dict[str, str]],
        cambios_nuevos: Dict[int, Dict[str, str]]
    ) -> Tuple[bool, List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        🛡️ FASE 5.1: Validar cambios del odontograma con 16 reglas médicas

        Valida lógica y consistencia médica de los cambios antes de guardar.

        Args:
            condiciones_anteriores: Estado actual del odontograma
            cambios_nuevos: Nuevos cambios a aplicar

        Returns:
            Tupla (es_valido, errores, warnings)
            - es_valido: True si no hay errores críticos
            - errores: Lista de errores que bloquean el guardado
            - warnings: Lista de advertencias que permiten continuar
        """
        errores = []
        warnings = []

        # Aplicar cambios para obtener estado final
        estado_final = condiciones_anteriores.copy()
        for diente, superficies in cambios_nuevos.items():
            if diente not in estado_final:
                estado_final[diente] = {}
            estado_final[diente].update(superficies)

        # ==========================================
        # REGLA 1: No cambiar diente ausente a otro estado
        # ==========================================
        for diente, superficies_nuevas in cambios_nuevos.items():
            condiciones_previas = condiciones_anteriores.get(diente, {})

            for superficie, nueva_condicion in superficies_nuevas.items():
                condicion_previa = condiciones_previas.get(superficie, "sano")

                if condicion_previa == "ausente" and nueva_condicion != "ausente":
                    errores.append({
                        "regla": "REGLA_1_DIENTE_AUSENTE",
                        "severidad": "error",
                        "mensaje": f"❌ Diente {diente} está ausente. No puede cambiar a '{nueva_condicion}'.",
                        "diente": diente,
                        "superficie": superficie,
                        "sugerencia": "Un diente ausente solo puede recibir implante en intervención separada."
                    })

        # ==========================================
        # REGLA 2: Extracción invalida otras condiciones en el mismo diente
        # ==========================================
        for diente, superficies_nuevas in cambios_nuevos.items():
            condiciones_finales_diente = estado_final.get(diente, {})

            if "extraccion" in condiciones_finales_diente.values():
                otras_condiciones = [
                    (sup, cond) for sup, cond in condiciones_finales_diente.items()
                    if cond not in ["extraccion", "ausente"]
                ]

                if otras_condiciones:
                    warnings.append({
                        "regla": "REGLA_2_EXTRACCION_INCONSISTENTE",
                        "severidad": "warning",
                        "mensaje": f"⚠️ Diente {diente} marcado para extracción pero tiene otras condiciones.",
                        "diente": diente,
                        "detalles": otras_condiciones,
                        "sugerencia": "Si se extraerá el diente, las demás condiciones son irrelevantes."
                    })

        # ==========================================
        # REGLA 3: Fractura crítica requiere tratamiento
        # ==========================================
        for diente, superficies_nuevas in cambios_nuevos.items():
            if "fractura" in superficies_nuevas.values():
                # Verificar si hay tratamiento asociado
                condiciones_finales_diente = estado_final.get(diente, {})
                tiene_tratamiento = any(
                    cond in ["endodoncia", "corona", "extraccion"]
                    for cond in condiciones_finales_diente.values()
                )

                if not tiene_tratamiento:
                    warnings.append({
                        "regla": "REGLA_3_FRACTURA_SIN_TRATAMIENTO",
                        "severidad": "warning",
                        "mensaje": f"⚠️ Diente {diente} tiene fractura pero no tratamiento asociado.",
                        "diente": diente,
                        "sugerencia": "Considere agregar endodoncia, corona o programar extracción."
                    })

        # ==========================================
        # REGLA 4: Caries múltiples en mismo diente
        # ==========================================
        for diente, superficies in estado_final.items():
            caries_count = sum(1 for cond in superficies.values() if cond == "caries")

            if caries_count >= 3:
                warnings.append({
                    "regla": "REGLA_4_CARIES_MULTIPLES",
                    "severidad": "warning",
                    "mensaje": f"⚠️ Diente {diente} tiene {caries_count} superficies con caries.",
                    "diente": diente,
                    "sugerencia": "Considere endodoncia o extracción si el daño es extenso."
                })

        # ==========================================
        # REGLA 5: Obturación sobre diente ausente
        # ==========================================
        for diente, superficies_nuevas in cambios_nuevos.items():
            condiciones_previas = condiciones_anteriores.get(diente, {})

            if any(c == "ausente" for c in condiciones_previas.values()):
                if any(c == "obturado" for c in superficies_nuevas.values()):
                    errores.append({
                        "regla": "REGLA_5_OBTURACION_DIENTE_AUSENTE",
                        "severidad": "error",
                        "mensaje": f"❌ No puede obturar diente {diente} que está ausente.",
                        "diente": diente,
                        "sugerencia": "Primero debe colocar implante o prótesis."
                    })

        # ==========================================
        # REGLA 6: Endodoncia en diente con extracción
        # ==========================================
        for diente, superficies in estado_final.items():
            tiene_endodoncia = "endodoncia" in superficies.values()
            tiene_extraccion = "extraccion" in superficies.values()

            if tiene_endodoncia and tiene_extraccion:
                warnings.append({
                    "regla": "REGLA_6_ENDODONCIA_Y_EXTRACCION",
                    "severidad": "warning",
                    "mensaje": f"⚠️ Diente {diente} tiene endodoncia Y extracción marcadas.",
                    "diente": diente,
                    "sugerencia": "Si se extraerá, la endodoncia es innecesaria. Considere eliminar una."
                })

        # ==========================================
        # REGLA 7: Implante sin ausencia previa
        # ==========================================
        for diente, superficies_nuevas in cambios_nuevos.items():
            if "implante" in superficies_nuevas.values():
                condiciones_previas = condiciones_anteriores.get(diente, {})
                estaba_ausente = any(c == "ausente" for c in condiciones_previas.values())

                if not estaba_ausente:
                    warnings.append({
                        "regla": "REGLA_7_IMPLANTE_SIN_AUSENCIA",
                        "severidad": "warning",
                        "mensaje": f"⚠️ Diente {diente} recibe implante pero no estaba ausente.",
                        "diente": diente,
                        "sugerencia": "Verifique que el diente fue extraído previamente."
                    })

        # ==========================================
        # REGLA 8: Corona sin tratamiento previo
        # ==========================================
        for diente, superficies_nuevas in cambios_nuevos.items():
            if "corona" in superficies_nuevas.values():
                condiciones_previas = condiciones_anteriores.get(diente, {})
                tenia_tratamiento = any(
                    c in ["endodoncia", "obturado"]
                    for c in condiciones_previas.values()
                )

                if not tenia_tratamiento:
                    warnings.append({
                        "regla": "REGLA_8_CORONA_SIN_TRATAMIENTO",
                        "severidad": "warning",
                        "mensaje": f"⚠️ Diente {diente} recibe corona sin tratamiento previo.",
                        "diente": diente,
                        "sugerencia": "Usualmente la corona requiere endodoncia u obturación previa."
                    })

        # ==========================================
        # REGLA 9: Cambio de sano a ausente sin extracción
        # ==========================================
        for diente, superficies_nuevas in cambios_nuevos.items():
            condiciones_previas = condiciones_anteriores.get(diente, {})

            for superficie, nueva_condicion in superficies_nuevas.items():
                condicion_previa = condiciones_previas.get(superficie, "sano")

                if condicion_previa == "sano" and nueva_condicion == "ausente":
                    errors_intermedios = []
                    # Verificar si hubo extracción en el historial intermedio
                    if "extraccion" not in estado_final.get(diente, {}).values():
                        warnings.append({
                            "regla": "REGLA_9_AUSENCIA_SIN_EXTRACCION",
                            "severidad": "warning",
                            "mensaje": f"⚠️ Diente {diente} cambió de sano a ausente sin registro de extracción.",
                            "diente": diente,
                            "superficie": superficie,
                            "sugerencia": "Considere registrar extracción primero para trazabilidad."
                        })

        # ==========================================
        # REGLA 10: Puente incompleto (mínimo 3 dientes)
        # ==========================================
        dientes_con_puente = [
            diente for diente, superficies in estado_final.items()
            if "puente" in superficies.values()
        ]

        if len(dientes_con_puente) > 0 and len(dientes_con_puente) < 3:
            warnings.append({
                "regla": "REGLA_10_PUENTE_INCOMPLETO",
                "severidad": "warning",
                "mensaje": f"⚠️ Puente dental requiere mínimo 3 dientes (actual: {len(dientes_con_puente)}).",
                "dientes": dientes_con_puente,
                "sugerencia": "Un puente necesita al menos 2 pilares + 1 póntico."
            })

        # ==========================================
        # REGLA 11: Giroversión en diente con otro tratamiento
        # ==========================================
        for diente, superficies in estado_final.items():
            tiene_giroversion = "giroversion" in superficies.values()
            tiene_tratamiento = any(
                cond in ["obturado", "corona", "endodoncia"]
                for cond in superficies.values()
            )

            if tiene_giroversion and tiene_tratamiento:
                warnings.append({
                    "regla": "REGLA_11_GIROVERSION_CON_TRATAMIENTO",
                    "severidad": "warning",
                    "mensaje": f"⚠️ Diente {diente} tiene giroversión y tratamiento.",
                    "diente": diente,
                    "sugerencia": "La giroversión debería corregirse antes del tratamiento final."
                })

        # ==========================================
        # REGLA 12: Validar transiciones lógicas
        # ==========================================
        TRANSICIONES_INVALIDAS = {
            "obturado": ["caries"],  # Obturado no puede volver a caries (se descompuso)
            "endodoncia": ["caries"],  # Endodoncia no puede volver a caries
            "corona": ["caries", "obturado"],  # Corona no regresa a estados inferiores
        }

        for diente, superficies_nuevas in cambios_nuevos.items():
            condiciones_previas = condiciones_anteriores.get(diente, {})

            for superficie, nueva_condicion in superficies_nuevas.items():
                condicion_previa = condiciones_previas.get(superficie, "sano")

                invalidas = TRANSICIONES_INVALIDAS.get(condicion_previa, [])
                if nueva_condicion in invalidas:
                    errores.append({
                        "regla": "REGLA_12_TRANSICION_INVALIDA",
                        "severidad": "error",
                        "mensaje": f"❌ Transición inválida en diente {diente} {superficie}: {condicion_previa} → {nueva_condicion}",
                        "diente": diente,
                        "superficie": superficie,
                        "sugerencia": f"Un diente {condicion_previa} no puede volver a {nueva_condicion}."
                    })

        # ==========================================
        # REGLA 13: Máximo de cambios simultáneos
        # ==========================================
        total_cambios = sum(len(superficies) for superficies in cambios_nuevos.values())

        if total_cambios > 20:
            warnings.append({
                "regla": "REGLA_13_CAMBIOS_EXCESIVOS",
                "severidad": "warning",
                "mensaje": f"⚠️ Se están registrando {total_cambios} cambios simultáneos.",
                "total_cambios": total_cambios,
                "sugerencia": "Verifique que todos los cambios sean correctos. Considere dividir en múltiples sesiones."
            })

        # ==========================================
        # REGLA 14: Dientes consecutivos críticos
        # ==========================================
        CONDICIONES_CRITICAS = ["caries", "fractura", "extraccion", "ausente"]

        for cuadrante in [range(11, 19), range(21, 29), range(31, 39), range(41, 49)]:
            dientes_criticos_consecutivos = []
            for diente in cuadrante:
                if diente in estado_final:
                    superficies = estado_final[diente]
                    if any(cond in CONDICIONES_CRITICAS for cond in superficies.values()):
                        dientes_criticos_consecutivos.append(diente)
                    else:
                        if len(dientes_criticos_consecutivos) >= 3:
                            warnings.append({
                                "regla": "REGLA_14_DIENTES_CRITICOS_CONSECUTIVOS",
                                "severidad": "warning",
                                "mensaje": f"⚠️ {len(dientes_criticos_consecutivos)} dientes consecutivos con condiciones críticas.",
                                "dientes": dientes_criticos_consecutivos.copy(),
                                "sugerencia": "Considere prótesis o implantes múltiples."
                            })
                        dientes_criticos_consecutivos = []

        # ==========================================
        # REGLA 15: Validar existencia de condición
        # ==========================================
        CONDICIONES_VALIDAS = {
            "sano", "caries", "obturado", "endodoncia", "corona",
            "puente", "extraccion", "ausente", "fractura", "implante",
            "protesis", "giroversion"
        }

        for diente, superficies_nuevas in cambios_nuevos.items():
            for superficie, condicion in superficies_nuevas.items():
                if condicion not in CONDICIONES_VALIDAS:
                    errores.append({
                        "regla": "REGLA_15_CONDICION_INVALIDA",
                        "severidad": "error",
                        "mensaje": f"❌ Condición desconocida '{condicion}' en diente {diente} {superficie}.",
                        "diente": diente,
                        "superficie": superficie,
                        "condicion": condicion,
                        "sugerencia": f"Condiciones válidas: {', '.join(sorted(CONDICIONES_VALIDAS))}"
                    })

        # ==========================================
        # REGLA 16: Validar superficies válidas
        # ==========================================
        SUPERFICIES_VALIDAS = {
            "oclusal", "mesial", "distal", "vestibular", "lingual", "palatina"
        }

        for diente, superficies_nuevas in cambios_nuevos.items():
            for superficie in superficies_nuevas.keys():
                if superficie not in SUPERFICIES_VALIDAS:
                    errores.append({
                        "regla": "REGLA_16_SUPERFICIE_INVALIDA",
                        "severidad": "error",
                        "mensaje": f"❌ Superficie desconocida '{superficie}' en diente {diente}.",
                        "diente": diente,
                        "superficie": superficie,
                        "sugerencia": f"Superficies válidas: {', '.join(sorted(SUPERFICIES_VALIDAS))}"
                    })

        # ==========================================
        # RESULTADO FINAL
        # ==========================================
        es_valido = len(errores) == 0

        if not es_valido:
            logger.warning(f"⚠️ Validación falló con {len(errores)} errores y {len(warnings)} advertencias")
        elif len(warnings) > 0:
            logger.info(f"ℹ️ Validación exitosa con {len(warnings)} advertencias")
        else:
            logger.info("✅ Validación completamente exitosa")

        return (es_valido, errores, warnings)

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
            
            # ⚠️ TEMP FIX: Comentar consulta problemática para que funcione el odontograma
            # Las intervenciones requieren JOIN complejo que está causando errores
            try:
                # TODO: Implementar consulta correcta para intervenciones por paciente
                logger.info("Intervenciones temporalmente deshabilitadas para evitar errores de esquema")
                intervenciones = []
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

    # ============================================================================
    # 🦷 MÉTODOS V4.0 - SOPORTE DUAL WORKFLOW (DIAGNÓSTICO + INTERVENCIÓN)
    # ============================================================================

    async def get_latest_odontogram(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """📋 Obtener la versión más reciente del odontograma del paciente"""
        try:
            response = self.client.table("odontogramas").select("*").eq(
                "numero_historia", patient_id
            ).eq("es_version_actual", True).execute()

            if response.data:
                return response.data[0]
            return None

        except Exception as e:
            logger.error(f"❌ Error obteniendo último odontograma: {str(e)}")
            return None

    async def get_odontogram_conditions(self, odontogram_id: str) -> Dict[int, Dict[str, str]]:
        """🦷 Obtener condiciones de todos los dientes del odontograma"""
        try:
            response = self.client.table("condiciones_diente").select("*").eq(
                "id_odontograma", odontogram_id
            ).execute()

            conditions = {}
            if response.data:
                for cond in response.data:
                    tooth_num = cond["numero_diente"]
                    surface = cond.get("superficie", "general")
                    condition = cond["condicion"]

                    if tooth_num not in conditions:
                        conditions[tooth_num] = {}
                    conditions[tooth_num][surface] = condition

            return conditions

        except Exception as e:
            logger.error(f"❌ Error obteniendo condiciones: {str(e)}")
            return {}

    async def create_odontogram_version(self, patient_id: str, dentist_id: str,
                                       conditions: Dict[int, Dict[str, str]],
                                       reason: str) -> Optional[Dict[str, Any]]:
        """📝 Crear nueva versión del odontograma con cambios detectados"""
        try:
            # Obtener versión anterior
            previous_version = await self.get_latest_odontogram(patient_id)

            # Marcar versión anterior como no actual
            if previous_version:
                self.client.table("odontogramas").update({
                    "es_version_actual": False
                }).eq("id", previous_version["id"]).execute()

            # Crear nueva versión
            new_version_data = {
                "numero_historia": patient_id,
                "id_personal": dentist_id,
                "version": (previous_version["version"] + 1) if previous_version else 1,
                "id_version_anterior": previous_version["id"] if previous_version else None,
                "es_version_actual": True,
                "motivo_nueva_version": reason,
                "fecha_creacion": datetime.now().isoformat()
            }

            response = self.client.table("odontogramas").insert(new_version_data).execute()

            if response.data:
                new_odontogram_id = response.data[0]["id"]

                # Guardar condiciones de la nueva versión
                for tooth_num, surfaces in conditions.items():
                    for surface, condition in surfaces.items():
                        await self.save_tooth_condition(
                            odontogram_id=new_odontogram_id,
                            tooth_number=tooth_num,
                            surface=surface,
                            condition=condition
                        )

                logger.info(f"✅ Nueva versión de odontograma creada: {new_odontogram_id}")
                return response.data[0]

            return None

        except Exception as e:
            logger.error(f"❌ Error creando versión de odontograma: {str(e)}")
            return None

    async def save_tooth_condition(self, odontogram_id: str, tooth_number: int,
                                   surface: str, condition: str) -> bool:
        """💾 Guardar condición de un diente específico"""
        try:
            # Buscar si ya existe
            existing = self.client.table("condiciones_diente").select("*").eq(
                "id_odontograma", odontogram_id
            ).eq("numero_diente", tooth_number).eq("superficie", surface).execute()

            if existing.data:
                # Actualizar existente
                self.client.table("condiciones_diente").update({
                    "condicion": condition,
                    "fecha_registro": datetime.now().isoformat()
                }).eq("id", existing.data[0]["id"]).execute()
            else:
                # Crear nuevo
                self.client.table("condiciones_diente").insert({
                    "id_odontograma": odontogram_id,
                    "numero_diente": tooth_number,
                    "superficie": surface,
                    "condicion": condition,
                    "fecha_registro": datetime.now().isoformat()
                }).execute()

            return True

        except Exception as e:
            logger.error(f"❌ Error guardando condición de diente: {str(e)}")
            return False

    async def create_intervention(self, consultation_id: str, dentist_id: str,
                                  total_bs: float, total_usd: float,
                                  odontogram_version_id: Optional[str] = None,
                                  observations: str = "") -> Optional[Dict[str, Any]]:
        """🏥 Crear intervención completa en BD"""
        try:
            intervention_data = {
                "id_consulta": consultation_id,
                "id_odontologo": dentist_id,
                "costo_total_bs": total_bs,
                "costo_total_usd": total_usd,
                "id_odontograma": odontogram_version_id,
                "observaciones": observations,
                "fecha_inicio": datetime.now().isoformat(),
                "estado": "completada"
            }

            response = self.client.table("intervenciones").insert(intervention_data).execute()

            if response.data:
                logger.info(f"✅ Intervención creada: {response.data[0]['id']}")
                return response.data[0]

            return None

        except Exception as e:
            logger.error(f"❌ Error creando intervención: {str(e)}")
            return None

    async def add_service_to_intervention(self, intervention_id: str, service_id: str,
                                         tooth_numbers: List[int], price_bs: float,
                                         price_usd: float, quantity: int = 1) -> bool:
        """➕ Agregar servicio a intervención con dientes específicos"""
        try:
            service_data = {
                "id_intervencion": intervention_id,
                "id_servicio": service_id,
                "dientes_tratados": tooth_numbers,  # Array de integers
                "precio_bs": price_bs,
                "precio_usd": price_usd,
                "cantidad": quantity,
                "fecha_aplicacion": datetime.now().isoformat()
            }

            response = self.client.table("intervenciones_servicios").insert(service_data).execute()

            if response.data:
                logger.info(f"✅ Servicio {service_id} agregado a intervención {intervention_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"❌ Error agregando servicio a intervención: {str(e)}")
            return False

    # ============================================================================
    # 📋 MÉTODOS TIMELINE V4.0 - OBTENER HISTORIAL DE INTERVENCIONES
    # ============================================================================

    async def get_patient_interventions(self, patient_id: str) -> List[Dict[str, Any]]:
        """📋 Obtener todas las intervenciones del paciente con datos completos para timeline"""
        try:
            # Paso 1: Obtener todas las consultas del paciente
            consultas_response = self.client.table("consultas").select("id").eq(
                "numero_historia", patient_id
            ).execute()

            if not consultas_response.data:
                return []

            # Obtener IDs de consultas
            consulta_ids = [c['id'] for c in consultas_response.data]

            # Paso 2: Obtener intervenciones de esas consultas
            interventions_response = self.client.table("intervenciones").select(
                "id, fecha_inicio, procedimiento_realizado, observaciones, id_consulta, id_odontologo"
            ).in_("id_consulta", consulta_ids).execute()

            if not interventions_response.data:
                return []

            interventions = []
            for intervention in interventions_response.data:
                # Obtener datos del odontólogo
                dentist_response = self.client.table("personal").select(
                    "nombres, apellidos"
                ).eq("id", intervention['id_odontologo']).execute()

                dentist_name = "Sin registro"
                if dentist_response.data:
                    dentist = dentist_response.data[0]
                    dentist_name = f"{dentist['nombres']} {dentist['apellidos']}"

                # Obtener servicios de la intervención
                services_response = self.client.table("intervenciones_servicios").select(
                    "dientes_tratados, id_servicio"
                ).eq("id_intervencion", intervention['id']).execute()

                tooth_numbers = []
                service_names = []

                if services_response.data:
                    for service in services_response.data:
                        # Agregar dientes tratados
                        if service.get('dientes_tratados'):
                            tooth_numbers.extend(service['dientes_tratados'])

                        # Obtener nombre del servicio
                        service_detail = self.client.table("servicios").select("nombre").eq(
                            "id", service['id_servicio']
                        ).execute()
                        if service_detail.data:
                            service_names.append(service_detail.data[0]['nombre'])

                # Formatear fecha
                fecha_inicio = datetime.fromisoformat(intervention['fecha_inicio']) if intervention.get('fecha_inicio') else datetime.now()

                interventions.append({
                    "id": intervention['id'],
                    "date": fecha_inicio.strftime("%Y-%m-%d"),
                    "time": fecha_inicio.strftime("%H:%M"),
                    "dentist": dentist_name,
                    "dentist_id": intervention['id_odontologo'],
                    "procedure": ", ".join(service_names) if service_names else intervention.get('procedimiento_realizado', 'Intervención general'),
                    "tooth_numbers": list(set(tooth_numbers)),  # Eliminar duplicados
                    "notes": intervention.get('observaciones', ''),
                    "changes": []
                })

            logger.info(f"✅ Obtenidas {len(interventions)} intervenciones para paciente {patient_id}")
            return interventions

        except Exception as e:
            logger.error(f"❌ Error obteniendo intervenciones del paciente: {str(e)}")
            return []

    async def get_patient_dentists(self, patient_id: str) -> List[str]:
        """👨‍⚕️ Obtener lista de dentistas que han atendido al paciente"""
        try:
            # Paso 1: Obtener consultas del paciente
            consultas_response = self.client.table("consultas").select("id").eq(
                "numero_historia", patient_id
            ).execute()

            if not consultas_response.data:
                return []

            consulta_ids = [c['id'] for c in consultas_response.data]

            # Paso 2: Obtener IDs de odontólogos que han atendido
            interventions_response = self.client.table("intervenciones").select(
                "id_odontologo"
            ).in_("id_consulta", consulta_ids).execute()

            if not interventions_response.data:
                return []

            # Obtener dentistas únicos
            dentist_ids = list(set([i['id_odontologo'] for i in interventions_response.data if i.get('id_odontologo')]))

            dentists = []
            for dentist_id in dentist_ids:
                dentist_response = self.client.table("personal").select(
                    "nombres, apellidos"
                ).eq("id", dentist_id).execute()

                if dentist_response.data:
                    dentist = dentist_response.data[0]
                    dentists.append(f"{dentist['nombres']} {dentist['apellidos']}")

            dentists.sort()
            logger.info(f"✅ Obtenidos {len(dentists)} dentistas para paciente {patient_id}")
            return dentists

        except Exception as e:
            logger.error(f"❌ Error obteniendo dentistas: {str(e)}")
            return []

    async def get_patient_procedures(self, patient_id: str) -> List[str]:
        """🦷 Obtener lista de procedimientos realizados al paciente"""
        try:
            # Paso 1: Obtener consultas del paciente
            consultas_response = self.client.table("consultas").select("id").eq(
                "numero_historia", patient_id
            ).execute()

            if not consultas_response.data:
                return []

            consulta_ids = [c['id'] for c in consultas_response.data]

            # Paso 2: Obtener IDs de intervenciones del paciente
            interventions_response = self.client.table("intervenciones").select(
                "id"
            ).in_("id_consulta", consulta_ids).execute()

            if not interventions_response.data:
                return []

            intervention_ids = [i['id'] for i in interventions_response.data]

            # Obtener servicios de las intervenciones
            services_response = self.client.table("intervenciones_servicios").select(
                "id_servicio"
            ).in_("id_intervencion", intervention_ids).execute()

            if not services_response.data:
                return []

            # Obtener nombres de servicios únicos
            service_ids = list(set([s['id_servicio'] for s in services_response.data if s.get('id_servicio')]))

            procedures = []
            for service_id in service_ids:
                service_response = self.client.table("servicios").select("nombre").eq("id", service_id).execute()
                if service_response.data:
                    procedures.append(service_response.data[0]['nombre'])

            procedures.sort()
            logger.info(f"✅ Obtenidos {len(procedures)} procedimientos para paciente {patient_id}")
            return procedures

        except Exception as e:
            logger.error(f"❌ Error obteniendo procedimientos: {str(e)}")
            return []


# Instancia única para importar
odontologia_service = OdontologiaService()