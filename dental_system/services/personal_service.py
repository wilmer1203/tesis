"""
Servicio centralizado para gestión de personal
Maneja toda la lógica de personal, usuarios y roles
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from decimal import Decimal
from .base_service import BaseService
from dental_system.supabase.tablas import personal_table, users_table
from dental_system.models import PersonalModel
import logging

logger = logging.getLogger(__name__)

class PersonalService(BaseService):
    """
    Servicio que maneja toda la lógica de personal
    Incluye creación de usuarios, asignación de roles y gestión de personal
    """
    
    def __init__(self):
        super().__init__()
        self.personal_table = personal_table
        self.users_table = users_table
    
    async def get_filtered_personal(self, 
                                  search: str = None, 
                                  tipo_personal: str = None,
                                  estado_laboral: str = None,
                                  activos_only: bool = True) -> List[PersonalModel]:
        """
        Obtiene personal filtrado 
        
        Args:
            search: Término de búsqueda
            tipo_personal: Filtro por tipo (Odontólogo, Administrador, etc.)
            estado_laboral: Filtro por estado laboral
            activos_only: Solo personal activo
            
        Returns:
            Lista de personal como modelos tipados
        """
        try:
            # Obtener datos usando el table ya existente
            personal_data = self.personal_table.get_filtered_personal(
                tipo_personal=tipo_personal if tipo_personal and tipo_personal != "todos" else None,
                estado_laboral=estado_laboral if estado_laboral and estado_laboral != "todos" else None,
                solo_activos=activos_only,
                busqueda=search if search and search.strip() else None
            )
            
            # Convertir a modelos tipados
            personal_models = []
            for item in personal_data:
                try:
                    model = PersonalModel.from_dict(item)
                    personal_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo personal: {e}")
                    continue
            
            print(f"✅ Personal obtenido: {len(personal_models)} registros")
            return personal_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a personal")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo personal filtrado", e)
            return []
    
    async def create_staff_member(self, form_data: Dict[str, str], creator_user_id: str) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo miembro del personal - PROCESO COMPLETO
        
        Args:
            form_data: Datos del formulario
            creator_user_id: ID del usuario que crea
            
        Returns:
            Personal creado o None si hay error
        """
        try:
            logger.info("Creando nuevo miembro del personal")
            
            # Verificar permisos
            self.require_permission("personal", "crear")
            
            # Validar campos requeridos
            required_fields = ["primer_nombre", "primer_apellido", "numero_documento", "email", "celular", "tipo_personal"]
            if not form_data.get("id"):  # Solo para nuevos usuarios
                required_fields.append("password")
            
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)
            
            # Verificar que no exista el documento
            existing_personal = self.personal_table.get_by_documento(form_data["numero_documento"])
            if existing_personal:
                raise ValueError("Ya existe personal con este número de documento")
            
            # Verificar que no exista el email
            existing_user = self.users_table.get_by_email(form_data["email"])
            if existing_user:
                raise ValueError("Ya existe un usuario con este email")
            
            # Paso 1: Crear usuario en auth.users y tabla usuarios
            rol = self._map_tipo_personal_to_rol(form_data["tipo_personal"])
            
            user_result = self.users_table.crear_usuario(
                email=form_data["email"],
                password=form_data["password"],
                rol=rol,
                telefono=form_data.get("telefono", ""),
                nombre=form_data["primer_nombre"],
                apellido=form_data["primer_apellido"],
                activo=True,
                method='admin'
            )
            
            if not user_result or not user_result.get("success"):
                raise ValueError("Error creando usuario: " + user_result.get("message", "Error desconocido"))
            
            usuario_id = user_result["user_id"]
            
            try:
                # Paso 2: Crear registro en tabla personal
                fecha_nacimiento = None
                if form_data.get("fecha_nacimiento"):
                    try:
                        fecha_nacimiento = datetime.strptime(form_data["fecha_nacimiento"], "%Y-%m-%d").date()
                    except ValueError:
                        raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
                
                fecha_contratacion = None
                if form_data.get("fecha_contratacion"):
                    try:
                        fecha_contratacion = datetime.strptime(form_data["fecha_contratacion"], "%Y-%m-%d").date()
                    except ValueError:
                        fecha_contratacion = date.today()
                else:
                    fecha_contratacion = date.today()
                
                salario = None
                if form_data.get("salario"):
                    try:
                        salario = Decimal(form_data["salario"])
                    except (ValueError, TypeError):
                        salario = None
                
                personal_result = self.personal_table.create_staff_complete(
                    usuario_id=usuario_id,
                    primer_nombre=form_data["primer_nombre"].strip(),
                    primer_apellido=form_data["primer_apellido"].strip(),
                    segundo_nombre=form_data.get("segundo_nombre", "").strip() or None,
                    segundo_apellido=form_data.get("segundo_apellido", "").strip() or None,
                    numero_documento=form_data["numero_documento"],
                    celular=form_data["celular"],
                    tipo_personal=form_data["tipo_personal"],
                    tipo_documento=form_data.get("tipo_documento", "CC"),
                    fecha_nacimiento=fecha_nacimiento,
                    direccion=form_data.get("direccion") if form_data.get("direccion") else None,
                    especialidad=form_data.get("especialidad") if form_data.get("especialidad") else None,
                    numero_licencia=form_data.get("numero_licencia") if form_data.get("numero_licencia") else None,
                    fecha_contratacion=fecha_contratacion,
                    salario=salario,
                    observaciones=form_data.get("observaciones") if form_data.get("observaciones") else None
                )
                
                if personal_result:
                    nombre_display = self.construct_full_name(
                        form_data["primer_nombre"],
                        form_data.get("segundo_nombre"),
                        form_data["primer_apellido"],
                        form_data.get("segundo_apellido")
                    )
                    logger.info(f"✅ Personal creado: {nombre_display}")
                    return {
                        "success": True,
                        "personal": personal_result,
                        "usuario": user_result
                    }
                else:
                    raise ValueError("Error creando registro de personal")
                    
            except Exception as e:
                # Si falla la creación del personal, limpiar el usuario creado
                logger.error(f"Error creando personal, limpiando usuario: {e}")
                # TODO: Implementar limpieza del usuario si es necesario
                raise ValueError(f"Error creando personal: {str(e)}")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para crear personal")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error creando personal", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def update_staff_member(self, personal_id: str, form_data: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Actualiza un miembro del personal existente
        
        Args:
            personal_id: ID del personal
            form_data: Datos del formulario
            
        Returns:
            Personal actualizado o None si hay error
        """
        try:
            logger.info(f"Actualizando personal: {personal_id}")
            
            # Verificar permisos
            self.require_permission("personal", "actualizar")
            
            # Validar campos requeridos (sin password para actualización)
            required_fields = ["primer_nombre", "primer_apellido", "numero_documento", "email", "celular", "tipo_personal"]
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)
            
            # Obtener personal actual
            current_personal = self.personal_table.get_by_id(personal_id)
            if not current_personal:
                raise ValueError("Personal no encontrado")
            
            # Verificar documento único (excluyendo el actual)
            existing_personal = self.personal_table.get_by_documento(form_data["numero_documento"])
            if existing_personal and existing_personal.get("id") != personal_id:
                raise ValueError("Ya existe otro personal con este número de documento")
            
            # Actualizar información del usuario si cambió el email
            usuario_id = current_personal.get("usuario_id")
            if usuario_id and form_data.get("email"):
                current_user = self.users_table.get_by_id(usuario_id)
                if current_user and current_user.get("email") != form_data["email"]:
                    # Verificar que el nuevo email no esté en uso
                    existing_user = self.users_table.get_by_email(form_data["email"])
                    if existing_user and existing_user.get("id") != usuario_id:
                        raise ValueError("Ya existe otro usuario con este email")
                    
                    # Actualizar email del usuario
                    self.users_table.update(usuario_id, {
                        "email": form_data["email"],
                        "telefono": form_data.get("telefono", "")
                    })
            
            # Procesar fecha de nacimiento
            fecha_nacimiento = None
            if form_data.get("fecha_nacimiento"):
                try:
                    fecha_nacimiento = datetime.strptime(form_data["fecha_nacimiento"], "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            # Procesar salario
            salario = None
            if form_data.get("salario"):
                try:
                    salario = Decimal(form_data["salario"])
                except (ValueError, TypeError):
                    salario = None
            
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
                "celular": form_data["celular"],
                "tipo_personal": form_data["tipo_personal"],
                
                # Información adicional
                "direccion": form_data.get("direccion") if form_data.get("direccion") else None,
                "especialidad": form_data.get("especialidad") if form_data.get("especialidad") else None,
                "numero_licencia": form_data.get("numero_licencia") if form_data.get("numero_licencia") else None,
                "observaciones": form_data.get("observaciones") if form_data.get("observaciones") else None
            }
            
            if fecha_nacimiento:
                data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
            
            if salario is not None:
                data["salario"] = float(salario)
            
            # Actualizar
            result = self.personal_table.update(personal_id, data)
            
            if result:
                nombre_display = self.construct_full_name(
                    form_data["primer_nombre"],
                    form_data.get("segundo_nombre"),
                    form_data["primer_apellido"],
                    form_data.get("segundo_apellido")
                )
                logger.info(f"✅ Personal actualizado: {nombre_display}")
                return result
            else:
                raise ValueError("Error actualizando personal en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para actualizar personal")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error actualizando personal", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def deactivate_staff_member(self, personal_id: str, motivo: str = None) -> bool:
        """
        Desactiva un miembro del personal
        
        Args:
            personal_id: ID del personal
            motivo: Motivo de desactivación
            
        Returns:
            True si se desactivó correctamente
        """
        try:
            logger.info(f"Desactivando personal: {personal_id}")
            
            # Verificar permisos
            self.require_permission("personal", "eliminar")
            
            # Desactivar usando el método de la tabla
            user_name = self.get_current_user_name()
            motivo_completo = motivo or f"Desactivado desde dashboard por {user_name}"
            
            result = self.personal_table.update_work_status(
                personal_id, 
                "inactivo", 
                motivo_completo
            )
            
            if result:
                logger.info(f"✅ Personal desactivado correctamente")
                return True
            else:
                raise ValueError("Error desactivando personal")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para desactivar personal")
            raise
        except Exception as e:
            self.handle_error("Error desactivando personal", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def reactivate_staff_member(self, personal_id: str) -> bool:
        """
        Reactiva un miembro del personal
        
        Args:
            personal_id: ID del personal
            
        Returns:
            True si se reactivó correctamente
        """
        try:
            logger.info(f"Reactivando personal: {personal_id}")
            
            # Verificar permisos
            self.require_permission("personal", "crear")
            
            user_name = self.get_current_user_name()
            result = self.personal_table.update_work_status(
                personal_id, 
                "activo", 
                f"Reactivado desde dashboard por {user_name}"
            )
            
            if result:
                logger.info(f"✅ Personal reactivado correctamente")
                return True
            else:
                raise ValueError("Error reactivando personal")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para reactivar personal")
            raise
        except Exception as e:
            self.handle_error("Error reactivando personal", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def get_staff_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de personal
        """
        try:
            stats = self.personal_table.get_stats()
            logger.info(f"Estadísticas de personal obtenidas: {stats}")
            return stats
            
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de personal", e)
            return {
                "total": 0,
                "activos": 0,
                "odontologos": 0,
                "administradores": 0,
                "asistentes": 0,
                "gerentes": 0
            }
    
    def _map_tipo_personal_to_rol(self, tipo_personal: str) -> str:
        """Mapea el tipo de personal al rol del sistema"""
        mapping = {
            'Gerente': 'gerente',
            'Administrador': 'administrador', 
            'Odontólogo': 'odontologo',
            'Asistente': 'asistente'
        }
        return mapping.get(tipo_personal, 'administrador')


# Instancia única para importar
personal_service = PersonalService()