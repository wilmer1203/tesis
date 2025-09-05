"""
Servicio centralizado para gestión de pacientes
Elimina duplicación entre boss_state y admin_state
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from .base_service import BaseService
from .cache_invalidation_hooks import invalidate_after_patient_operation, track_cache_invalidation
from dental_system.supabase.tablas import pacientes_table
from dental_system.models import PacienteModel, PacienteFormModel
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
                                  activos_only: Optional[bool] = None) -> List[PacienteModel]:
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
    
    async def create_patient(self, patient_form: PacienteFormModel, user_id: str) -> Optional[PacienteModel]:
        """
        Crea un nuevo paciente con modelo tipado
        
        Args:
            patient_form: Formulario tipado de paciente
            user_id: ID del usuario que crea
            
        Returns:
            PacienteModel creado o None si hay error
        """
        try:
            logger.info("Creando nuevo paciente")
            
            # Verificar permisos
            self.require_permission("pacientes", "crear")
            
            # Validar formulario tipado
            validation_errors = patient_form.validate_form()
            if validation_errors:
                error_msg = f"Errores de validación: {validation_errors}"
                raise ValueError(error_msg)
            
            # Verificar que no exista el documento
            existing = self.table.get_by_documento(patient_form.numero_documento)
            if existing:
                raise ValueError("Ya existe un paciente con este número de documento")
            
            # Procesar campos de fecha
            fecha_nacimiento = None
            if patient_form.fecha_nacimiento:
                try:
                    fecha_nacimiento = datetime.strptime(patient_form.fecha_nacimiento, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            # Procesar arrays (alergias, medicamentos, etc.)
            alergias = self.process_array_field(patient_form.alergias)
            medicamentos = self.process_array_field(patient_form.medicamentos_actuales)
            # Procesar información médica adicional
            condiciones = self.process_array_field(patient_form.observaciones_medicas)
            
            # Procesar información médica adicional
            condiciones_medicas = self.process_array_field(patient_form.condiciones_medicas) if hasattr(patient_form, 'condiciones_medicas') and patient_form.condiciones_medicas else None
            antecedentes_familiares = self.process_array_field(patient_form.antecedentes_familiares) if hasattr(patient_form, 'antecedentes_familiares') and patient_form.antecedentes_familiares else None
            
            # Crear paciente usando el método de la tabla
            result = self.table.create_patient_complete(
                # Nombres separados
                primer_nombre=patient_form.primer_nombre.strip(),
                primer_apellido=patient_form.primer_apellido.strip(),
                segundo_nombre=patient_form.segundo_nombre.strip() or None,
                segundo_apellido=patient_form.segundo_apellido.strip() or None,
                
                # Documentación
                numero_documento=patient_form.numero_documento,
                registrado_por=user_id,
                tipo_documento=patient_form.tipo_documento or "CI",
                fecha_nacimiento=fecha_nacimiento,
                genero=patient_form.genero if patient_form.genero else None,
                
                # Teléfonos separados
                celular_1=patient_form.celular_1 if patient_form.celular_1 else None,
                celular_2=patient_form.celular_2 if patient_form.celular_2 else None,
                
                # Contacto y ubicación
                email=patient_form.email.strip() if patient_form.email and patient_form.email.strip() else None,
                direccion=patient_form.direccion if patient_form.direccion else None,
                ciudad=patient_form.ciudad if patient_form.ciudad else None,
                departamento=patient_form.departamento if patient_form.departamento else None,
                ocupacion=patient_form.ocupacion if patient_form.ocupacion else None,
                estado_civil=patient_form.estado_civil if patient_form.estado_civil else None,
                
                # Información médica
                alergias=alergias if alergias else None,
                medicamentos_actuales=medicamentos if medicamentos else None,
                condiciones_medicas=condiciones_medicas,
                antecedentes_familiares=antecedentes_familiares,
                observaciones=patient_form.observaciones_medicas if patient_form.observaciones_medicas else None,
                
                # Contacto de emergencia como JSONB (esquema v4.1)
                contacto_emergencia={
                    "nombre": patient_form.contacto_emergencia_nombre if patient_form.contacto_emergencia_nombre else "",
                    "telefono": patient_form.contacto_emergencia_telefono if patient_form.contacto_emergencia_telefono else "",
                    "relacion": patient_form.contacto_emergencia_relacion if patient_form.contacto_emergencia_relacion else "",
                    "direccion": patient_form.contacto_emergencia_direccion if patient_form.contacto_emergencia_direccion else ""
                } if any([patient_form.contacto_emergencia_nombre, patient_form.contacto_emergencia_telefono]) else {}
            )
            
            if result:
                # Crear modelo tipado del resultado
                paciente_model = PacienteModel.from_dict(result)
                
                # 🗑️ INVALIDAR CACHE después de crear paciente
                try:
                    invalidate_after_patient_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras crear paciente: {cache_error}")
                
                logger.info(f"✅ Paciente creado: {paciente_model.nombre_completo}")
                return paciente_model
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
    
    async def update_patient(self, patient_id: str, patient_form: PacienteFormModel) -> Optional[PacienteModel]:
        """
        Actualiza un paciente existente con modelo tipado
        
        Args:
            patient_id: ID del paciente
            patient_form: Formulario tipado de paciente
            
        Returns:
            PacienteModel actualizado o None si hay error
        """
        try:
            logger.info(f"Actualizando paciente: {patient_id}")
            
            # Verificar permisos
            self.require_permission("pacientes", "actualizar")
            
            # Validar formulario tipado
            validation_errors = patient_form.validate_form()
            if validation_errors:
                error_msg = f"Errores de validación: {validation_errors}"
                raise ValueError(error_msg)
            
            # Verificar documento único (excluyendo el actual)
            existing = self.table.get_by_documento(patient_form.numero_documento)
            if existing and existing.get("id") != patient_id:
                raise ValueError("Ya existe otro paciente con este número de documento")
            
            # Procesar fecha
            fecha_nacimiento = None
            if patient_form.fecha_nacimiento:
                try:
                    fecha_nacimiento = datetime.strptime(patient_form.fecha_nacimiento, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            # Procesar arrays
            alergias = self.process_array_field(patient_form.alergias)
            medicamentos = self.process_array_field(patient_form.medicamentos_actuales)
            
            # Preparar datos para actualización
            data = {
                # Nombres separados
                "primer_nombre": patient_form.primer_nombre.strip(),
                "primer_apellido": patient_form.primer_apellido.strip(),
                "segundo_nombre": patient_form.segundo_nombre.strip() or None,
                "segundo_apellido": patient_form.segundo_apellido.strip() or None,
                
                # Documentación
                "numero_documento": patient_form.numero_documento,
                "tipo_documento": patient_form.tipo_documento or "cedula",
                "genero": patient_form.genero if patient_form.genero else None,
                
                # Teléfonos separados
                "celular_1": patient_form.celular_1 if patient_form.celular_1 else None,
                "celular_2": patient_form.celular_2 if patient_form.celular_2 else None,
                
                # Contacto y ubicación
                "email": patient_form.email if patient_form.email else None,
                "direccion": patient_form.direccion if patient_form.direccion else None,
                "ciudad": patient_form.ciudad if patient_form.ciudad else None,
                "estado_civil": patient_form.estado_civil if patient_form.estado_civil else None,
                
                # Información médica
                "alergias": alergias if alergias else None,
                "medicamentos_actuales": medicamentos if medicamentos else None,
                # "enfermedades_cronicas": patient_form.enfermedades_cronicas if patient_form.enfermedades_cronicas else None,
                "observaciones": patient_form.observaciones_medicas if patient_form.observaciones_medicas else None,
                
                # Contacto de emergencia como JSONB (esquema v4.1)
                "contacto_emergencia": {
                    "nombre": patient_form.contacto_emergencia_nombre if patient_form.contacto_emergencia_nombre else "",
                    "telefono": patient_form.contacto_emergencia_telefono if patient_form.contacto_emergencia_telefono else "",
                    "relacion": patient_form.contacto_emergencia_relacion if patient_form.contacto_emergencia_relacion else "",
                    "direccion": patient_form.contacto_emergencia_direccion if patient_form.contacto_emergencia_direccion else ""
                } if any([patient_form.contacto_emergencia_nombre, patient_form.contacto_emergencia_telefono]) else {}
            }
            
            if fecha_nacimiento:
                data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
            
            # Actualizar
            result = self.table.update(patient_id, data)
            
            if result:
                nombre_display = self.construct_full_name(
                    data["primer_nombre"],
                    data.get("segundo_nombre"),
                    data["primer_apellido"],
                    data.get("segundo_apellido")
                )
                
                # 🗑️ INVALIDAR CACHE después de actualizar paciente
                invalidate_after_patient_operation()
                
                logger.info(f"✅ Paciente actualizado: {nombre_display} (cache invalidado)")
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