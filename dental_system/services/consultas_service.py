"""
Servicio centralizado para gestión de consultas/citas
Elimina duplicación entre boss_state y admin_state
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from .base_service import BaseService
from dental_system.supabase.tablas import consultas_table, personal_table, services_table
from dental_system.models import ConsultaModel
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
            
            # Obtener consultas usando el método de la tabla (ya corregido)
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
    
    async def create_consultation(self, form_data: Dict[str, str], user_id: str) -> Optional[Dict[str, Any]]:
        """
        Crea una nueva consulta - REEMPLAZA lógica duplicada
        
        Args:
            form_data: Datos del formulario
            user_id: ID del usuario que crea
            
        Returns:
            Consulta creada o None si hay error
        """
        try:
            logger.info("Creando nueva consulta")
            
            # Verificar permisos
            self.require_permission("consultas", "crear")
            
            # Validar campos requeridos
            required_fields = ["paciente_id", "odontologo_id"]
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)
            
            # Crear consulta con fecha/hora actual (por orden de llegada)
            result = self.consultas_table.create_consultation(
                paciente_id=form_data["paciente_id"],
                odontologo_id=form_data["odontologo_id"],
                fecha_programada=datetime.now(),  # Fecha/hora actual
                tipo_consulta=form_data.get("tipo_consulta", "general"),
                motivo_consulta=form_data.get("motivo_consulta") if form_data.get("motivo_consulta") else None,
                observaciones_cita=form_data.get("observaciones_cita") if form_data.get("observaciones_cita") else None,
                prioridad=form_data.get("prioridad", "normal"),
                programada_por=user_id
            )
            
            if result:
                logger.info(f"✅ Consulta creada: {result.get('numero_consulta', 'N/A')}")
                return result
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
    
    async def update_consultation(self, consultation_id: str, form_data: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Actualiza una consulta existente
        
        Args:
            consultation_id: ID de la consulta
            form_data: Datos del formulario
            
        Returns:
            Consulta actualizada o None si hay error
        """
        try:
            logger.info(f"Actualizando consulta: {consultation_id}")
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Preparar datos de actualización
            data = {
                "motivo_consulta": form_data.get("motivo_consulta") if form_data.get("motivo_consulta") else None,
                "observaciones_cita": form_data.get("observaciones_cita") if form_data.get("observaciones_cita") else None,
                "tipo_consulta": form_data.get("tipo_consulta", "general"),
                "prioridad": form_data.get("prioridad", "normal")
            }
            
            # Solo permitir cambiar odontólogo si está en estado programada
            current_consulta = self.consultas_table.get_by_id(consultation_id)
            if current_consulta and current_consulta.get("estado") == "programada":
                if form_data.get("odontologo_id") and form_data["odontologo_id"] != current_consulta.get("odontologo_id"):
                    data["odontologo_id"] = form_data["odontologo_id"]
            
            result = self.consultas_table.update(consultation_id, data)
            
            if result:
                logger.info(f"✅ Consulta actualizada correctamente")
                return result
            else:
                raise ValueError("Error actualizando consulta")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para actualizar consultas")
            raise
        except Exception as e:
            self.handle_error("Error actualizando consulta", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
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
            logger.info(f"Cambiando estado de consulta {consultation_id} a {nuevo_estado}")
            
            # Verificar permisos
            self.require_permission("consultas", "actualizar")
            
            # Validar transición de estado
            consulta_actual = self.consultas_table.get_by_id(consultation_id)
            if consulta_actual and not self._is_valid_status_transition(consulta_actual.get("estado"), nuevo_estado):
                raise ValueError(f"Transición de estado no válida")
            
            result = self.consultas_table.update_status(consultation_id, nuevo_estado, notas)
            
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
        """Validar si la transición de estado es válida"""
        valid_transitions = {
            "programada": ["confirmada", "en_progreso", "cancelada", "no_asistio"],
            "confirmada": ["en_progreso", "cancelada", "no_asistio"],
            "en_progreso": ["completada", "cancelada"],
            "completada": [],  # Estado final
            "cancelada": ["programada"],  # Puede reprogramarse
            "no_asistio": ["programada"]  # Puede reprogramarse
        }
        
        return nuevo_estado in valid_transitions.get(estado_actual, [])
    
    async def get_support_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtiene datos de apoyo para consultas (odontólogos, servicios)
        REEMPLAZA múltiples métodos duplicados
        
        Returns:
            Diccionario con odontólogos y servicios
        """
        try:
            logger.info("Obteniendo datos de apoyo para consultas")
            
            # Obtener odontólogos activos
            odontologos_data  = self.personal_table.get_dentists(incluir_inactivos=False)
            
            # Obtener servicios activos
            servicios_data = await self._get_active_services()
            
            return {
                "odontologos": odontologos_data,
                "servicios": servicios_data
            }
            
        except Exception as e:
            self.handle_error("Error obteniendo datos de apoyo", e)
            return {
                "odontologos": [],
                "servicios": []
            }
    
    async def _get_active_dentists(self) -> List[Dict[str, Any]]:
        """Obtiene lista de odontólogos activos"""
        try:
            # Usar método existente con fallback
            odontologos_data = self.personal_table.get_dentists(incluir_inactivos=False)
            print("-*********************************************************")
            print(odontologos_data)
            processed_dentists = []
            for item in odontologos_data:
                # Manejo robusto de nombres desde vista
                nombre_completo = ""
                
                if 'nombre_completo' in item:
                    nombre_completo = item['nombre_completo']
                else:
                    # Fallback: construir desde campos separados
                    nombres = []
                    if item.get('primer_nombre'):
                        nombres.append(item['primer_nombre'])
                    if item.get('segundo_nombre'):
                        nombres.append(item['segundo_nombre'])
                    if item.get('primer_apellido'):
                        nombres.append(item['primer_apellido'])
                    if item.get('segundo_apellido'):
                        nombres.append(item['segundo_apellido'])
                    nombre_completo = ' '.join(nombres) if nombres else 'Sin nombre'
                
                processed_dentists.append({
                    'id': item.get('id', ''),
                    'nombre_completo': nombre_completo,
                    'especialidad': item.get('especialidad', ''),
                    'estado_laboral': item.get('estado_laboral', 'activo'),
                    'tipo_personal': item.get('tipo_personal', 'Odontólogo')
                })
            
            return processed_dentists
            
        except Exception as e:
            logger.error(f"Error obteniendo odontólogos: {e}")
            return []
    
    async def _get_active_services(self) -> List[Dict[str, Any]]:
        """Obtiene lista de servicios activos"""
        try:
            servicios_data = self.services_table.get_active_services()
            
            processed_services = []
            for item in servicios_data:
                processed_services.append({
                    'id': item['id'],
                    'codigo': item.get('codigo', ''),
                    'nombre': item.get('nombre', ''),
                    'categoria': item.get('categoria', ''),
                    'precio_base': item.get('precio_base', 0)
                })
            
            return processed_services
            
        except Exception as e:
            logger.error(f"Error obteniendo servicios: {e}")
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
    
    async def cancel_consultation(self, consultation_id: str, motivo: str) -> bool:
        """Cancela una consulta con motivo"""
        return await self.change_consultation_status(consultation_id, "cancelada", motivo)
    
    async def confirm_consultation(self, consultation_id: str) -> bool:
        """Confirma una consulta programada"""
        return await self.change_consultation_status(consultation_id, "confirmada")
    
    async def mark_no_show(self, consultation_id: str) -> bool:
        """Marca una consulta como no asistida"""
        return await self.change_consultation_status(consultation_id, "no_asistio")


# Instancia única para importar
consultas_service = ConsultasService()