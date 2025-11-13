"""
Funciones de autenticación con Supabase Auth - VERSIÓN AUTOCONTENIDA
SIN dependencias externas a usuarios.py - Todo consolidado aquí
"""
from typing import Dict, Optional, Tuple, Any, List
from .client import handle_supabase_error, supabase_client
import logging

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Excepción personalizada para errores de autenticación"""
    pass


class SupabaseAuth:
    """
    Maneja todas las operaciones de autenticación + gestión de usuarios
    AUTOCONTENIDA - No depende de usuarios.py
    """

    def __init__(self):
        self._client = None

    @property
    def client(self):
        """Cliente de Supabase (lazy loading)"""
        if self._client is None:
            self._client = supabase_client.get_client()
        return self._client

    # ========================================
    # MÉTODOS DE GESTIÓN DE USUARIOS
    # ========================================

    @handle_supabase_error
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su email"""
        response = self.client.table("usuario").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None

    @handle_supabase_error
    def get_by_auth_id(self, auth_user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su ID de auth.users"""
        logger.info(f"Buscando usuario con auth_user_id: {auth_user_id}")
        response = self.client.table("usuario").select("*").eq("auth_user_id", auth_user_id).execute()
        result = response.data[0] if response.data else None
        logger.info(f"Usuario encontrado: {result is not None}")
        return result

    @handle_supabase_error
    def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su ID"""
        response = self.client.table("usuario").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None

    @handle_supabase_error
    def get_user_basic_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información básica del usuario con su rol"""
        logger.info(f"Obteniendo info básica del usuario: {user_id}")

        user = self.get_by_id(user_id)
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado")
            return None

        rol_response = self.client.table("rol").select("nombre, descripcion").eq("id", user["rol_id"]).execute()

        if rol_response.data:
            user["rol"] = rol_response.data[0]
        else:
            logger.warning(f"Rol no encontrado para usuario {user_id}")
            user["rol"] = {"nombre": "sin_rol", "descripcion": "Sin rol"}

        logger.info(f"Usuario con rol obtenido: {user.get('email', 'N/A')} - {user['rol']['nombre']}")
        return user

    @handle_supabase_error
    def get_user_complete_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información completa del usuario incluyendo datos del personal"""
        logger.info(f"Obteniendo info completa del usuario: {user_id}")

        user_info = self.get_user_basic_info(user_id)
        if not user_info:
            return None

        personal_response = self.client.table("personal").select("*").eq("usuario_id", user_id).execute()

        if personal_response.data:
            personal_data = personal_response.data[0]

            nombres = []
            if personal_data.get("primer_nombre"):
                nombres.append(personal_data["primer_nombre"])
            if personal_data.get("segundo_nombre"):
                nombres.append(personal_data["segundo_nombre"])
            if personal_data.get("primer_apellido"):
                nombres.append(personal_data["primer_apellido"])
            if personal_data.get("segundo_apellido"):
                nombres.append(personal_data["segundo_apellido"])

            nombre_completo = " ".join(nombres) if nombres else "Usuario"

            user_info["personal"] = personal_data
            user_info["nombre_completo"] = nombre_completo
        else:
            logger.warning(f"No se encontró información de personal para usuario {user_id}")
            user_info["personal"] = None
            user_info["nombre_completo"] = user_info.get("email", "Usuario").split("@")[0]

        return user_info

    @handle_supabase_error
    def verify_user_permission(self, user_id: str, module: str, action: str) -> bool:
        """
        Verifica si un usuario tiene permiso para realizar una acción
        Sistema de permisos por nombre de rol
        """
        user = self.get_user_basic_info(user_id)

        if not user or not user.get("activo"):
            return False

        rol_nombre = user.get("rol", {}).get("nombre", "")

        # Gerente: acceso total
        if rol_nombre == "gerente":
            return True

        # Administrador: casi todo excepto personal y configuración
        if rol_nombre == "administrador":
            return module not in ["personal", "configuracion"]

        # Odontólogo: solo su módulo
        if rol_nombre == "odontologo":
            return module in ["odontologia", "pacientes"]

        # Asistente: solo lectura
        if rol_nombre == "asistente":
            return action == "read"

        return False

    def _get_role_id(self, rol_name: str) -> Optional[str]:
        """Obtener ID del rol con fallbacks"""
        try:
            logger.info(f"Buscando ID para rol: {rol_name}")

            # Buscar rol exacto
            rol_response = self.client.table("rol").select("id").eq("nombre", rol_name).eq("activo", True).execute()
            if rol_response.data:
                logger.info(f"✅ Rol '{rol_name}' encontrado: {rol_response.data[0]['id']}")
                return rol_response.data[0]["id"]

            # Fallback a administrador
            admin_response = self.client.table("rol").select("id").eq("nombre", "administrador").eq("activo", True).execute()
            if admin_response.data:
                logger.warning(f"⚠️ Rol '{rol_name}' no encontrado, usando administrador")
                return admin_response.data[0]["id"]

            # Fallback al primer rol disponible
            first_response = self.client.table("rol").select("id").eq("activo", True).order("nombre").limit(1).execute()
            if first_response.data:
                logger.warning("⚠️ Rol administrador no encontrado, usando primer rol disponible")
                return first_response.data[0]["id"]

            logger.error("❌ No se encontraron roles activos en la base de datos")
            return None

        except Exception as e:
            logger.error(f"❌ Error obteniendo rol ID: {e}")
            return None

    # ========================================
    # MÉTODOS DE AUTENTICACIÓN
    # ========================================

    @handle_supabase_error
    def create_auth_user(self, email: str, password: str) -> Dict[str, Any]:
        """Crear usuario en Supabase Auth con admin.create_user"""
        admin_client = supabase_client.get_admin_client()

        if not admin_client:
            raise ValueError("No hay cliente administrativo disponible")

        auth_response = admin_client.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
        })

        if not auth_response or not hasattr(auth_response, 'user') or not auth_response.user:
            raise ValueError("Error en respuesta de admin.create_user")

        return {
            'id': auth_response.user.id,
            'email': auth_response.user.email,
            'email_confirmed': True
        }

    @handle_supabase_error
    def crear_usuario(
        self,
        email: str,
        password: str,
        rol: str = 'administrador',
        avatar_url: str = '',
        activo: bool = True,
        configuraciones: dict = None,
        method: str = 'admin'
    ) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo usuario completo (auth + tabla usuarios)

        Args:
            email: Correo electrónico
            password: Contraseña
            rol: Rol del usuario
            avatar_url: URL del avatar
            activo: Estado del usuario
            configuraciones: Configuraciones adicionales
            method: Método a usar ('admin' o 'signup')

        Returns:
            dict: Información del usuario creado
        """
        logger.info(f"🚀 Creando usuario con método {method}: {email}")

        try:
            # Validaciones básicas
            if not email or not password:
                raise ValueError("Email y contraseña son requeridos")

            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")

            # Verificar que el email no exista
            existing_user = self.get_by_email(email)
            if existing_user:
                raise ValueError("El email ya está registrado")

            # Paso 1: Crear en auth.users
            user_metadata = {
                'rol': rol,
                'avatar_url': avatar_url,
                'managed_by': 'python'
            }
            auth_user = self.create_auth_user(email, password, user_metadata)

            if not auth_user:
                raise ValueError("No se pudo crear usuario en auth.users")

            logger.info(f"✅ Usuario creado en auth.users - ID: {auth_user['id']}")

            # Paso 2: Crear en tabla usuarios
            try:
                db_user = self._create_user_record(
                    auth_user_id=auth_user['id'],
                    email=email,
                    rol=rol,
                    avatar_url=avatar_url,
                    configuraciones=configuraciones
                )

                if not db_user:
                    self._cleanup_auth_user(auth_user['id'], method)
                    raise ValueError("No se pudo crear registro en tabla usuarios")

                logger.info(f"✅ Registro creado en tabla usuarios - ID: {db_user['id']}")

                return {
                    'success': True,
                    'message': 'Usuario creado exitosamente',
                    'user_id': db_user['id'],
                    'auth_user_id': auth_user['id'],
                }

            except Exception as e:
                logger.error(f"❌ Error creando registro en tabla usuarios: {e}")
                self._cleanup_auth_user(auth_user['id'], method)
                raise ValueError(f"Error al crear registro de usuario: {str(e)}")

        except Exception as e:
            logger.error(f"❌ Error general creando usuario {email}: {e}")
            raise ValueError(f"Error al crear usuario: {str(e)}")

    def _create_user_record(self, auth_user_id: str, email: str, rol: str, avatar_url: str, configuraciones: dict) -> Optional[Dict[str, Any]]:
        """Crear registro en tabla usuarios"""
        logger.info("📝 Creando registro en tabla usuarios...")

        try:
            # Obtener ID del rol
            rol_id = self._get_role_id(rol)
            if not rol_id:
                raise ValueError(f"No se pudo obtener ID para rol: {rol}")

            # Preparar datos
            user_data = {
                'auth_user_id': auth_user_id,
                'email': email,
                'rol_id': rol_id,
                'avatar_url': avatar_url if avatar_url else None,
                'activo': True,
                'metadata': configuraciones or {},
                'configuraciones': configuraciones or {}
            }

            # Insertar
            response = self.client.table("usuario").insert(user_data).execute()

            if response.data:
                result = response.data[0]
                logger.info("✅ Registro creado en tabla usuarios")
                return result
            else:
                logger.error("❌ No se obtuvo datos al insertar usuario")
                return None

        except Exception as e:
            logger.error(f"❌ Error insertando en tabla usuarios: {e}")
            raise

    def _cleanup_auth_user(self, auth_user_id: str, method: str):
        """Limpiar usuario de auth.users si falló la creación"""
        try:
            logger.warning(f"🧹 Limpiando usuario de auth.users: {auth_user_id}")

            if method == 'admin':
                admin_client = supabase_client.get_admin_client()
                if admin_client:
                    admin_client.auth.admin.delete_user(auth_user_id)
                    logger.info("✅ Usuario eliminado de auth.users")
            else:
                logger.warning("⚠️ Usuario de signup no eliminado automáticamente")

        except Exception as e:
            logger.error(f"❌ Error limpiando auth.users: {e}")


    @handle_supabase_error
    def sign_in(self, email: str, password: str) -> Tuple[Any, Dict[str, Any]]:
        """
        Inicia sesión de un usuario

        Args:
            email: Email del usuario
            password: Contraseña

        Returns:
            Tupla de (session, user_info con rol)
        """
        try:
            # 1. Autenticar con Supabase Auth
            logger.info(f"🔐 Autenticando usuario: {email}")

            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not auth_response.session:
                raise AuthError("Credenciales inválidas")

            session = auth_response.session
            auth_user = auth_response.user

            if not auth_user:
                raise AuthError("Error obteniendo información del usuario autenticado")

            logger.info(f"✅ Autenticación con Supabase exitosa para: {email}")

            # 2. Buscar usuario en nuestra BD
            logger.info(f"🔍 Buscando usuario en BD con auth_user_id: {auth_user.id}")
            db_user = self.get_by_auth_id(auth_user.id)

            if not db_user:
                logger.error(f"❌ Usuario no encontrado en BD para auth_user_id: {auth_user.id}")
                raise AuthError("Usuario no encontrado en el sistema")

            logger.info(f"✅ Usuario encontrado en BD: {db_user['email']}")

            # 3. Obtener información básica con rol
            logger.info(f"📋 Obteniendo información básica del usuario: {db_user['id']}")
            user_info = self.get_user_basic_info(db_user["id"])

            if not user_info:
                logger.error(f"❌ No se pudo obtener información del usuario: {db_user['id']}")
                raise AuthError("Error obteniendo información del usuario")

            logger.info(f"✅ Información del usuario obtenida - Rol: {user_info['rol']['nombre']}")

            return session, user_info

        except Exception as e:
            logger.error(f"💥 Error en inicio de sesión: {str(e)}")
            raise AuthError(f"Error al iniciar sesión: {str(e)}")
    
    @handle_supabase_error
    def sign_out(self) -> bool:
        """
        Cierra la sesión actual
        
        Returns:
            True si se cerró correctamente
        """
        try:
            logger.info("🚪 Cerrando sesión")
            self.client.auth.sign_out()
            logger.info("✅ Sesión cerrada exitosamente")
            return True
        except Exception as e:
            logger.error(f"❌ Error al cerrar sesión: {str(e)}")
            return False
    
    @handle_supabase_error
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene el usuario actual autenticado con información básica

        Returns:
            Usuario con rol o None
        """
        try:
            # Obtener usuario de Auth
            auth_response = self.client.auth.get_user()

            if not auth_response or not auth_response.user:
                return None

            # Obtener información completa de la BD
            db_user = self.get_by_auth_id(auth_response.user.id)

            if not db_user:
                return None

            # Obtener con información básica
            return self.get_user_basic_info(db_user["id"])

        except Exception as e:
            logger.error(f"Error obteniendo usuario actual: {e}")
            return None

    @handle_supabase_error
    def get_current_user_complete(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene el usuario actual con información completa (incluyendo personal)

        Returns:
            Usuario con información completa o None
        """
        try:
            # Obtener usuario de Auth
            auth_response = self.client.auth.get_user()

            if not auth_response or not auth_response.user:
                return None

            # Obtener información completa de la BD
            db_user = self.get_by_auth_id(auth_response.user.id)

            if not db_user:
                return None

            # Obtener con información completa
            return self.get_user_complete_info(db_user["id"])

        except Exception as e:
            logger.error(f"Error obteniendo usuario completo: {e}")
            return None

    def verify_user_permission_for_current(self, module: str, action: str) -> bool:
        """
        Verifica si el usuario actual tiene permiso para una acción

        Args:
            module: Módulo del sistema
            action: Acción a realizar

        Returns:
            True si tiene permiso
        """
        try:
            user = self.get_current_user()

            if not user:
                return False

            return self.verify_user_permission(
                user_id=user["id"],
                module=module,
                action=action
            )

        except Exception:
            return False
    
    def get_session(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene la sesión actual

        Returns:
            Sesión actual o None
        """
        try:
            session = self.client.auth.get_session()
            return session
        except Exception:
            return None

    # ========================================
    # MÉTODOS DE GESTIÓN DE PERFIL
    # ========================================

    @handle_supabase_error
    async def update_user_password(self, current_password: str, new_password: str, user_email: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña del usuario actual

        Args:
            current_password: Contraseña actual del usuario
            new_password: Nueva contraseña
            user_email: Email del usuario (para validar)

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # 1. Validar contraseña actual intentando hacer login
            try:
                auth_response = self.client.auth.sign_in_with_password({
                    "email": user_email,
                    "password": current_password
                })
                if not auth_response.session:
                    return False, "Contraseña actual incorrecta"
            except Exception:
                return False, "Contraseña actual incorrecta"

            # 2. Actualizar contraseña con Supabase Auth
            logger.info(f"🔐 Actualizando contraseña para usuario: {user_email}")

            update_response = self.client.auth.update_user({
                "password": new_password
            })

            if update_response and update_response.user:
                logger.info("✅ Contraseña actualizada exitosamente")
                return True, "Contraseña actualizada correctamente"
            else:
                logger.error("❌ Error al actualizar contraseña")
                return False, "Error al actualizar la contraseña"

        except Exception as e:
            logger.error(f"❌ Error cambiando contraseña: {str(e)}")
            return False, f"Error: {str(e)}"

    @handle_supabase_error
    async def update_user_email(self, new_email: str, current_password: str, user_id: str, current_email: str) -> Tuple[bool, str]:
        """
        Cambia el email del usuario actual

        Args:
            new_email: Nuevo email
            current_password: Contraseña actual (para confirmar)
            user_id: ID del usuario en tabla usuario
            current_email: Email actual

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # 1. Validar contraseña actual
            try:
                auth_response = self.client.auth.sign_in_with_password({
                    "email": current_email,
                    "password": current_password
                })
                if not auth_response.session:
                    return False, "Contraseña incorrecta"
            except Exception:
                return False, "Contraseña incorrecta"

            # 2. Verificar que el nuevo email no exista
            existing_user = self.get_by_email(new_email)
            if existing_user and existing_user.get("id") != user_id:
                return False, "El email ya está registrado por otro usuario"

            # 3. Actualizar email en Supabase Auth
            logger.info(f"📧 Actualizando email: {current_email} → {new_email}")

            update_response = self.client.auth.update_user({
                "email": new_email
            })

            if not update_response or not update_response.user:
                return False, "Error al actualizar email en autenticación"

            # 4. Actualizar email en tabla usuario
            update_db = self.client.table("usuario").update({
                "email": new_email,
                "fecha_actualizacion": "now()"
            }).eq("id", user_id).execute()

            if update_db.data:
                logger.info("✅ Email actualizado correctamente en BD")
                return True, "Email actualizado. Verifica tu nuevo email para confirmarlo"
            else:
                logger.error("❌ Error actualizando email en BD")
                return False, "Error al actualizar email en la base de datos"

        except Exception as e:
            logger.error(f"❌ Error cambiando email: {str(e)}")
            return False, f"Error: {str(e)}"


# Instancia singleton
auth = SupabaseAuth()

# Funciones de conveniencia para importar directamente
sign_in = auth.sign_in
sign_out = auth.sign_out
get_current_user = auth.get_current_user
get_current_user_complete = auth.get_current_user_complete
get_session = auth.get_session

# Métodos de gestión de usuarios (para compatibilidad con código existente)
crear_usuario = auth.crear_usuario
get_by_email = auth.get_by_email
get_by_auth_id = auth.get_by_auth_id
get_by_id = auth.get_by_id
get_user_basic_info = auth.get_user_basic_info
get_user_complete_info = auth.get_user_complete_info
verify_user_permission = auth.verify_user_permission
verify_user_permission_for_current = auth.verify_user_permission_for_current

# Alias para compatibilidad con código que importaba users_table
class UsersTableCompat:
    """Clase de compatibilidad para reemplazar users_table"""

    def __init__(self, auth_instance):
        self._auth = auth_instance

    def crear_usuario(self, *args, **kwargs):
        return self._auth.crear_usuario(*args, **kwargs)

    def get_by_email(self, email: str):
        return self._auth.get_by_email(email)

    def get_by_auth_id(self, auth_user_id: str):
        return self._auth.get_by_auth_id(auth_user_id)

    def get_by_id(self, user_id: str):
        return self._auth.get_by_id(user_id)

    def get_user_basic_info(self, user_id: str):
        return self._auth.get_user_basic_info(user_id)

    def get_user_complete_info(self, user_id: str):
        return self._auth.get_user_complete_info(user_id)

    def verify_user_permission(self, user_id: str, module: str, action: str):
        return self._auth.verify_user_permission(user_id, module, action)

# Instancia para compatibilidad
users_table = UsersTableCompat(auth)
usuarios_table = users_table  # Alias español