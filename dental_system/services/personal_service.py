"""
Servicio centralizado para gestión de personal
Maneja toda la lógica de personal, usuarios y roles
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from decimal import Decimal
from .base_service import BaseService
from dental_system.models import PersonalModel, PersonalFormModel
import logging

logger = logging.getLogger(__name__)

class PersonalService(BaseService):
    """
    Servicio que maneja toda la lógica de personal
    Incluye creación de usuarios, asignación de roles y gestión de personal
    """

    def __init__(self):
        super().__init__()
    
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
            # Construir query base con JOIN a usuarios
            query = self.client.table("personal").select(
                "*, usuario!personal_usuario_id_fkey(*)"
            )

            # Aplicar filtros dinámicos
            if activos_only:
                query = query.eq("estado_laboral", "activo")

            if tipo_personal and tipo_personal != "todos":
                query = query.eq("tipo_personal", tipo_personal)

            if estado_laboral and estado_laboral != "todos":
                query = query.eq("estado_laboral", estado_laboral)

            if search and search.strip():
                search_term = search.strip()
                query = query.or_(
                    f"numero_documento.ilike.%{search_term}%,"
                    f"celular.ilike.%{search_term}%"
                )

            # Ordenar por primer nombre
            query = query.order("primer_nombre")

            # Ejecutar query
            response = query.execute()
            personal_data = response.data if response.data else []

            # Convertir a modelos tipados
            personal_models = []
            for item in personal_data:
                try:
                    model = PersonalModel.from_dict(item)
                    personal_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo personal: {e}")
                    continue

            logger.info(f"✅ Personal obtenido: {len(personal_models)} registros")
            return personal_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a personal")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo personal filtrado", e)
            return []
    
    async def create_staff_member(self, personal_form: PersonalFormModel) -> Optional[PersonalModel]:
        """
        Crea un nuevo miembro del personal - PROCESO COMPLETO

        Args:
            personal_form: Formulario tipado de personal (PersonalFormModel)

        Returns:
            PersonalModel: Personal creado o None si hay error

        Nota:
            El contexto del usuario (user_id, user_profile) debe establecerse
            antes con set_user_context()
        """
        try:
            print("Creando nuevo miembro del personal")
            
            # Convertir formulario tipado a dict
            form_data = personal_form.to_dict()
            
            # Validar campos requeridos
            required_fields = ["primer_nombre", "primer_apellido", "numero_documento", "email", "celular", "tipo_personal"]
            if not form_data.get("id"):  # Solo para nuevos usuarios
                required_fields.append("password")
            
            missing_fields = self.validate_required_fields(form_data, required_fields)
            
            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)

            # ✅ VALIDACIONES ESPECÍFICAS - SINCRONIZADO CON ESTADO_PERSONAL.PY

            # Número de documento válido
            numero_documento = form_data.get("numero_documento", "").strip()
            if numero_documento and len(numero_documento) < 7:
                raise ValueError("El número de documento debe tener al menos 7 dígitos")

            # Email válido
            email = form_data.get("email", "").strip()
            if email and "@" not in email:
                raise ValueError("Email inválido")

            # Celular válido
            celular = form_data.get("celular", "").strip()
            if celular and len(celular) < 10:
                raise ValueError("Celular debe tener al menos 10 dígitos")

            # Contraseña válida (solo para usuarios nuevos)
            if not form_data.get("id"):  # Solo para nuevos usuarios
                password = form_data.get("password", "").strip()
                if password and len(password) < 6:
                    raise ValueError("La contraseña debe tener al menos 6 caracteres")

            # Verificar que no exista el documento
            response = self.client.table("personal").select("id").eq("numero_documento", form_data["numero_documento"]).execute()
            existing_personal = response.data[0] if response.data else None
            if existing_personal:
                raise ValueError("Ya existe personal con este número de documento")

            # Verificar que no exista el email
            response = self.client.table("usuario").select("id").eq("email", form_data["email"]).execute()
            existing_user = response.data[0] if response.data else None
            if existing_user:
                raise ValueError("Ya existe un usuario con este email")
            
            # verificar el monto antes de crear ____________________________________
            # Paso 1: Crear usuario en Supabase Auth
            rol = self._map_tipo_personal_to_rol(form_data["tipo_personal"])
            
            # 1.1. Crear usuario en Supabase Auth usando cliente administrativo
            print(f"📝 Creando usuario en Auth con email: {form_data['email']}")
            auth_response = self.admin_client.auth.admin.create_user({
                "email": form_data["email"],
                "password": form_data["password"],
                "email_confirm": True
            })

            if not auth_response or not auth_response.user:
                raise ValueError("Error creando usuario en autenticación")

            usuario_id = auth_response.user.id
            print(f"✅ Usuario creado en Supabase Auth: {usuario_id}")

            # 1.2. Obtener ID del rol
            rol_response = self.client.table("rol").select("id").eq("nombre", rol).execute()
            rol_id = rol_response.data[0]["id"] if rol_response.data else None

            if not rol_id:
                raise ValueError(f"No se encontró el rol: {rol}")

            # 1.3. Crear registro en tabla usuarios
            user_data = {
                "id": usuario_id,
                "email": form_data["email"],
                "rol_id": rol_id,
                "activo": True
            }

            user_response = self.client.table("usuario").insert(user_data).execute()
            user_result = user_response.data[0] if user_response.data else None
            if not user_result:
                raise ValueError("Error creando registro de usuario en la base de datos")
            
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
                

                # Preparar datos para insertar en tabla personal
                personal_data = {
                    "usuario_id": usuario_id,
                    "primer_nombre": form_data["primer_nombre"].strip(),
                    "primer_apellido": form_data["primer_apellido"].strip(),
                    "segundo_nombre": form_data.get("segundo_nombre", "").strip() or None,
                    "segundo_apellido": form_data.get("segundo_apellido", "").strip() or None,
                    "tipo_documento": form_data.get("tipo_documento", "CI"),
                    "numero_documento": form_data["numero_documento"],
                    "celular": form_data["celular"],
                    "tipo_personal": form_data["tipo_personal"],
                    "fecha_nacimiento": fecha_nacimiento.isoformat() if fecha_nacimiento else None,
                    "direccion": form_data.get("direccion") if form_data.get("direccion") else None,
                    "especialidad": form_data.get("especialidad") if form_data.get("especialidad") else None,
                    "numero_licencia": form_data.get("numero_licencia") if form_data.get("numero_licencia") else None,
                    "fecha_contratacion": fecha_contratacion.isoformat() if fecha_contratacion else None,
                    "estado_laboral": "activo"
                }

                personal_response = self.client.table("personal").insert(personal_data).execute()
                personal_result = personal_response.data[0] if personal_response.data else None
                if personal_result:
                    nombre_display = self.construct_full_name(
                        form_data["primer_nombre"],
                        form_data.get("segundo_nombre"),
                        form_data["primer_apellido"],
                        form_data.get("segundo_apellido")
                    )
                    logger.info(f"✅ Personal creado: {nombre_display}")
                    

                    # Convertir el diccionario a PersonalModel para consistency
                    return PersonalModel.from_dict(personal_result)
                else:
                    raise ValueError("Error creando registro de personal")
                    
            except Exception as e:
                # aqui va la funcion de eliminar el usuario____________________-
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
    
    async def update_staff_member(self, personal_id: str, personal_form: PersonalFormModel) -> Optional[PersonalModel]:
        """
        Actualiza un miembro del personal existente
        
        Args:
            personal_id: ID del personal
            personal_form: Formulario tipado de personal
            
        Returns:
            Personal actualizado o None si hay error
        """
        try:
            logger.info(f"Actualizando personal: {personal_id}")
            
            # Verificar permisos
            self.require_permission("personal", "actualizar")
            
            # Convertir formulario tipado a dict
            form_data = personal_form.to_dict()

            # Validar campos requeridos (email NO es requerido para actualización)
            required_fields = ["primer_nombre", "primer_apellido", "numero_documento", "celular", "tipo_personal"]
            missing_fields = self.validate_required_fields(form_data, required_fields)

            if missing_fields:
                error_msg = self.format_error_message("Datos incompletos", missing_fields)
                raise ValueError(error_msg)

            # ✅ VALIDACIONES ESPECÍFICAS - SINCRONIZADO CON ESTADO_PERSONAL.PY

            # Número de documento válido
            numero_documento = form_data.get("numero_documento", "").strip()
            if numero_documento and len(numero_documento) < 7:
                raise ValueError("El número de documento debe tener al menos 7 dígitos")

            # Email válido (solo si se proporciona)
            email = form_data.get("email", "").strip()
            if email and "@" not in email:
                raise ValueError("Email inválido")

            # Celular válido
            celular = form_data.get("celular", "").strip()
            if celular and len(celular) < 10:
                raise ValueError("Celular debe tener al menos 10 dígitos")

            # Obtener personal actual
            response = self.client.table("personal").select("*").eq("id", personal_id).execute()
            current_personal = response.data[0] if response.data else None
            if not current_personal:
                raise ValueError("Personal no encontrado")

            # Verificar documento único (excluyendo el actual)
            response = self.client.table("personal").select("id").eq("numero_documento", form_data["numero_documento"]).execute()
            existing_personal = response.data[0] if response.data else None
            if existing_personal and existing_personal.get("id") != personal_id:
                raise ValueError("Ya existe otro personal con este número de documento")
            
            # Actualizar información del usuario si cambió el email
            usuario_id = current_personal.get("usuario_id")
            if usuario_id and form_data.get("email"):
                # Obtener usuario actual
                user_response = self.client.table("usuario").select("*").eq("id", usuario_id).execute()
                current_user = user_response.data[0] if user_response.data else None

                if current_user and current_user.get("email") != form_data["email"]:
                    # Verificar que el nuevo email no esté en uso
                    email_check = self.client.table("usuario").select("id").eq("email", form_data["email"]).execute()
                    existing_user = email_check.data[0] if email_check.data else None
                    if existing_user and existing_user.get("id") != usuario_id:
                        raise ValueError("Ya existe otro usuario con este email")

                    # Actualizar email del usuario
                    update_user_data = {"email": form_data["email"]}
                    self.client.table("usuario").update(update_user_data).eq("id", usuario_id).execute()
            
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
                "tipo_documento": form_data.get("tipo_documento", "CI"),
                "celular": form_data["celular"],
                "tipo_personal": form_data["tipo_personal"],
                
                # Información adicional
                "direccion": form_data.get("direccion") if form_data.get("direccion") else None,
                "especialidad": form_data.get("especialidad") if form_data.get("especialidad") else None,
                "numero_licencia": form_data.get("numero_licencia") if form_data.get("numero_licencia") else None,
            }
            
            if fecha_nacimiento:
                data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
            
            if salario is not None:
                data["salario"] = float(salario)

            # Actualizar con query directa
            update_response = self.client.table("personal").update(data).eq("id", personal_id).execute()
            result = update_response.data[0] if update_response.data else None
            
            if result:
                nombre_display = self.construct_full_name(
                    form_data["primer_nombre"],
                    form_data.get("segundo_nombre"),
                    form_data["primer_apellido"],
                    form_data.get("segundo_apellido")
                )
                logger.info(f"✅ Personal actualizado: {nombre_display}")
                
                # Convertir el diccionario a PersonalModel para consistency
                return PersonalModel.from_dict(result)
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
            
            # Desactivar con query directa
            user_name = self.get_current_user_name()
            motivo_completo = motivo or f"Desactivado desde dashboard por {user_name}"

            update_data = {
                "estado_laboral": "inactivo"
            }

            response = self.client.table("personal").update(update_data).eq("id", personal_id).execute()
            result = response.data[0] if response.data else None
            
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

            update_data = {
                "estado_laboral": "activo"
            }

            response = self.client.table("personal").update(update_data).eq("id", personal_id).execute()
            result = response.data[0] if response.data else None
            
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
            # Obtener todos los registros de personal
            response = self.client.table("personal").select("*").execute()
            personal_list = response.data if response.data else []

            # Calcular estadísticas manualmente en Python
            total = len(personal_list)
            activos = len([p for p in personal_list if p.get("estado_laboral") == "activo"])

            # Agrupar por tipo
            por_tipo = {}
            for p in personal_list:
                tipo = p.get("tipo_personal", "Sin tipo")
                por_tipo[tipo] = por_tipo.get(tipo, 0) + 1

            stats = {
                "total": total,
                "activos": activos,
                "odontologos": por_tipo.get("Odontólogo", 0),
                "administradores": por_tipo.get("Administrador", 0),
                "asistentes": por_tipo.get("Asistente", 0),
                "gerentes": por_tipo.get("Gerente", 0),
                "por_tipo": por_tipo
            }

            logger.info(f"✅ Estadísticas de personal obtenidas: {stats}")
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
    
    async def obtener_personal_id_por_usuario(self, user_id: str) -> Optional[str]:
        """
        🔍 Obtener el ID de personal correspondiente a un usuario
        """
        try:
            # Query directa a tabla personal
            response = self.client.table("personal").select("id").eq("usuario_id", user_id).execute()
            personal_data = response.data[0] if response.data else None
            if personal_data:
                return personal_data.get('id')
            return None

        except Exception as e:
            logger.warning(f"⚠️ No se encontró personal para usuario {user_id}: {e}")
            return None


# Instancia única para importar
personal_service = PersonalService()