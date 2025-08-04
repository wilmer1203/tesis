"""
Servicio centralizado para gestión de pacientes
Elimina duplicación entre boss_state y admin_state
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from .base_service import BaseService
from dental_system.supabase.tablas import pacientes_table
from dental_system.models import PacienteModel
import logging

logger = logging.getLogger(__name__)

class PacientesService(BaseService):
    """
    Servicio que maneja toda la lógica de pacientes
    Usado tanto por Boss (vista) como Admin (CRUD completo)
    """
    
    def __init__(self):
        super().__init__()
        self.table = pacientes_table
  
    
    
    async def get_filtered_patients(self, 
                                  search: str = None, 
                                  genero: str = None, 
                                  activos_only: Optional[bool] = True) -> List[PacienteModel]:
        """
        Obtiene pacientes filtrados 
        
        Args:
            search: Término de búsqueda
            genero: Filtro por género (masculino, femenino, todos)
            activos_only: Solo pacientes activos
            
        Returns:
            Lista de pacientes como modelos tipados
        """
        try:
                        
            # Obtener datos usando el table ya existente
            pacientes_data = self.table.get_filtered_patients(
                activos_only=activos_only,
                busqueda=search if search and search.strip() else None,
                genero=genero if genero and genero != "todos" else None
            )
            
            # Convertir a modelos tipados
            pacientes_models = []
            for item in pacientes_data:
                try:
                    model = PacienteModel.from_dict(item)
                    pacientes_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo paciente: {e}")
                    continue
            
            print(f"✅ Pacientes obtenidos: {len(pacientes_models)} registros")
            return pacientes_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a pacientes")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo pacientes filtrados", e)
            return []
    
    async def create_patient(self, form_data: Dict[str, str], user_id: str) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo paciente - REEMPLAZA lógica duplicada
        
        Args:
            form_data: Datos del formulario
            user_id: ID del usuario que crea
            
        Returns:
            Paciente creado o None si hay error
        """
        try:
            logger.info("Creando nuevo paciente")
            
            # Verificar permisos
            self.require_permission("pacientes", "crear")
            
            # Validar campos requeridos
            required_fields = ["primer_nombre", "primer_apellido", "numero_documento"]
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)
            
            # Verificar que no exista el documento
            existing = self.table.get_by_documento(form_data["numero_documento"])
            if existing:
                raise ValueError("Ya existe un paciente con este número de documento")
            
            # Procesar campos de fecha
            fecha_nacimiento = None
            if form_data.get("fecha_nacimiento"):
                try:
                    fecha_nacimiento = datetime.strptime(form_data["fecha_nacimiento"], "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            # Procesar arrays (alergias, medicamentos, etc.)
            alergias = self.process_array_field(form_data.get("alergias", ""))
            medicamentos = self.process_array_field(form_data.get("medicamentos_actuales", ""))
            condiciones = self.process_array_field(form_data.get("condiciones_medicas", ""))
            antecedentes = self.process_array_field(form_data.get("antecedentes_familiares", ""))
            
            # Crear paciente usando el método de la tabla
            result = self.table.create_patient_complete(
                # Nombres separados
                primer_nombre=form_data["primer_nombre"].strip(),
                primer_apellido=form_data["primer_apellido"].strip(),
                segundo_nombre=form_data.get("segundo_nombre", "").strip() or None,
                segundo_apellido=form_data.get("segundo_apellido", "").strip() or None,
                
                # Documentación
                numero_documento=form_data["numero_documento"],
                registrado_por=user_id,
                tipo_documento=form_data.get("tipo_documento", "CC"),
                fecha_nacimiento=fecha_nacimiento,
                genero=form_data.get("genero") if form_data.get("genero") else None,
                
                # Teléfonos separados
                telefono_1=form_data.get("telefono_1") if form_data.get("telefono_1") else None,
                telefono_2=form_data.get("telefono_2") if form_data.get("telefono_2") else None,
                
                # Contacto y ubicación
                email=form_data.get("email") if form_data.get("email") else None,
                direccion=form_data.get("direccion") if form_data.get("direccion") else None,
                ciudad=form_data.get("ciudad") if form_data.get("ciudad") else None,
                departamento=form_data.get("departamento") if form_data.get("departamento") else None,
                ocupacion=form_data.get("ocupacion") if form_data.get("ocupacion") else None,
                estado_civil=form_data.get("estado_civil") if form_data.get("estado_civil") else None,
                
                # Información médica
                alergias=alergias if alergias else None,
                medicamentos_actuales=medicamentos if medicamentos else None,
                condiciones_medicas=condiciones if condiciones else None,
                antecedentes_familiares=antecedentes if antecedentes else None,
                observaciones=form_data.get("observaciones") if form_data.get("observaciones") else None
            )
            
            if result:
                nombre_display = self.construct_full_name(
                    form_data["primer_nombre"],
                    form_data.get("segundo_nombre"),
                    form_data["primer_apellido"],
                    form_data.get("segundo_apellido")
                )
                logger.info(f"✅ Paciente creado: {nombre_display}")
                return result
            else:
                raise ValueError("Error creando paciente en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para crear pacientes")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error creando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def update_patient(self, patient_id: str, form_data: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Actualiza un paciente existente
        
        Args:
            patient_id: ID del paciente
            form_data: Datos del formulario
            
        Returns:
            Paciente actualizado o None si hay error
        """
        try:
            logger.info(f"Actualizando paciente: {patient_id}")
            
            # Verificar permisos
            self.require_permission("pacientes", "actualizar")
            
            # Validar campos requeridos
            required_fields = ["primer_nombre", "primer_apellido", "numero_documento"]
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)
            
            # Verificar documento único (excluyendo el actual)
            existing = self.table.get_by_documento(form_data["numero_documento"])
            if existing and existing.get("id") != patient_id:
                raise ValueError("Ya existe otro paciente con este número de documento")
            
            # Procesar fecha
            fecha_nacimiento = None
            if form_data.get("fecha_nacimiento"):
                try:
                    fecha_nacimiento = datetime.strptime(form_data["fecha_nacimiento"], "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            # Procesar arrays
            alergias = self.process_array_field(form_data.get("alergias", ""))
            medicamentos = self.process_array_field(form_data.get("medicamentos_actuales", ""))
            condiciones = self.process_array_field(form_data.get("condiciones_medicas", ""))
            antecedentes = self.process_array_field(form_data.get("antecedentes_familiares", ""))
            
            # Preparar datos para actualización
            data = {
                # Nombres separados
                "primer_nombre": form_data["primer_nombre"].strip(),
                "primer_apellido": form_data["primer_apellido"].strip(),
                "segundo_nombre": form_data.get("segundo_nombre", "").strip() or None,
                "segundo_apellido": form_data.get("segundo_apellido", "").strip() or None,
                
                # Documentación
                "numero_documento": form_data["numero_documento"],
                "tipo_documento": form_data.get("tipo_documento", "CC"),
                "genero": form_data.get("genero") if form_data.get("genero") else None,
                
                # Teléfonos separados
                "telefono_1": form_data.get("telefono_1") if form_data.get("telefono_1") else None,
                "telefono_2": form_data.get("telefono_2") if form_data.get("telefono_2") else None,
                
                # Contacto y ubicación
                "email": form_data.get("email") if form_data.get("email") else None,
                "direccion": form_data.get("direccion") if form_data.get("direccion") else None,
                "ciudad": form_data.get("ciudad") if form_data.get("ciudad") else None,
                "departamento": form_data.get("departamento") if form_data.get("departamento") else None,
                "ocupacion": form_data.get("ocupacion") if form_data.get("ocupacion") else None,
                "estado_civil": form_data.get("estado_civil") if form_data.get("estado_civil") else None,
                
                # Información médica
                "alergias": alergias if alergias else None,
                "medicamentos_actuales": medicamentos if medicamentos else None,
                "condiciones_medicas": condiciones if condiciones else None,
                "antecedentes_familiares": antecedentes if antecedentes else None,
                "observaciones": form_data.get("observaciones") if form_data.get("observaciones") else None
            }
            
            if fecha_nacimiento:
                data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
            
            # Actualizar
            result = self.table.update(patient_id, data)
            
            if result:
                nombre_display = self.construct_full_name(
                    form_data["primer_nombre"],
                    form_data.get("segundo_nombre"),
                    form_data["primer_apellido"],
                    form_data.get("segundo_apellido")
                )
                logger.info(f"✅ Paciente actualizado: {nombre_display}")
                return result
            else:
                raise ValueError("Error actualizando paciente en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para actualizar pacientes")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error actualizando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def deactivate_patient(self, patient_id: str, motivo: str = None) -> bool:
        """
        Desactiva un paciente (soft delete)
        
        Args:
            patient_id: ID del paciente
            motivo: Motivo de desactivación
            
        Returns:
            True si se desactivó correctamente
        """
        try:
            logger.info(f"Desactivando paciente: {patient_id}")
            
            # Verificar permisos
            self.require_permission("pacientes", "eliminar")
            
            # TODO: Verificar que no tenga consultas activas
            
            # Desactivar usando el método de la tabla
            user_name = self.get_current_user_name()
            motivo_completo = motivo or f"Desactivado desde dashboard por {user_name}"
            
            result = self.table.deactivate_patient(patient_id, motivo_completo)
            
            if result:
                logger.info(f"✅ Paciente desactivado correctamente")
                return True
            else:
                raise ValueError("Error desactivando paciente")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para desactivar pacientes")
            raise
        except Exception as e:
            self.handle_error("Error desactivando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def reactivate_patient(self, patient_id: str) -> bool:
        """
        Reactiva un paciente
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            True si se reactivó correctamente
        """
        try:
            logger.info(f"Reactivando paciente: {patient_id}")
            
            # Verificar permisos
            self.require_permission("pacientes", "crear")  # Reactivar = crear de nuevo
            
            result = self.table.reactivate_patient(patient_id)
            
            if result:
                logger.info(f"✅ Paciente reactivado correctamente")
                return True
            else:
                raise ValueError("Error reactivando paciente")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para reactivar pacientes")
            raise
        except Exception as e:
            self.handle_error("Error reactivando paciente", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def get_patient_by_id(self, patient_id: str) -> Optional[PacienteModel]:
        """
        Obtiene un paciente por ID
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            Modelo del paciente o None
        """
        try:
            # Verificar permisos
            self.require_permission("pacientes", "leer")
            
            data = self.table.get_by_id(patient_id)
            if data:
                return PacienteModel.from_dict(data)
            return None
            
        except Exception as e:
            self.handle_error("Error obteniendo paciente por ID", e)
            return None

    
    async def get_patient_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de pacientes
        Usado por dashboard_service pero disponible independientemente
        """
        try:
            stats = self.table.get_patient_stats()
            logger.info(f"Estadísticas de pacientes obtenidas: {stats}")
            return stats
            
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de pacientes", e)
            return {
                "total": 0,
                "nuevos_mes": 0,
                "activos": 0,
                "hombres": 0,
                "mujeres": 0
            }


# Instancia única para importar
pacientes_service = PacientesService()