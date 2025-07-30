"""
Funciones de autenticación con Supabase Auth - VERSIÓN CORREGIDA
"""
from typing import Dict, Optional, Tuple, Any, List
from .client import handle_supabase_error, supabase_client
from .tablas.usuarios import users_table
import logging

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Excepción personalizada para errores de autenticación"""
    pass


class SupabaseAuth:
    """
    Maneja todas las operaciones de autenticación con Supabase - VERSIÓN SIMPLIFICADA
    """
    
    def __init__(self):
        self._client = None
    
    @property
    def client(self):
        """Cliente de Supabase (lazy loading)"""
        if self._client is None:
            self._client = supabase_client.get_client()
        return self._client

    @handle_supabase_error
    def create_auth_user(self, email: str, password: str, user_metadata: dict) -> Dict[str, Any]:
        """Crear usuario con admin.create_user"""
        admin_client = supabase_client.get_admin_client()
        
        if not admin_client:
            raise ValueError("No hay cliente administrativo disponible")
        
        auth_response = self._client.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,  # Confirmar automáticamente
            "user_metadata": user_metadata
        })
        
        if not auth_response or not hasattr(auth_response, 'user') or not auth_response.user:
            raise ValueError("Error en respuesta de admin.create_user")
        
        return {
            'id': auth_response.user.id,
            'email': auth_response.user.email,
            'email_confirmed': True
        }


    @handle_supabase_error
    def sign_in(self, email: str, password: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Inicia sesión de un usuario - VERSIÓN SIMPLIFICADA
        
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
            
            logger.info(f"✅ Autenticación con Supabase exitosa para: {email}")
            
            # 2. Buscar usuario en nuestra BD
            logger.info(f"🔍 Buscando usuario en BD con auth_user_id: {auth_user.id}")
            db_user = users_table.get_by_auth_id(auth_user.id)
            
            if not db_user:
                logger.error(f"❌ Usuario no encontrado en BD para auth_user_id: {auth_user.id}")
                raise AuthError("Usuario no encontrado en el sistema")
            
            logger.info(f"✅ Usuario encontrado en BD: {db_user['email']}")
            
            # 3. Obtener información básica con rol
            logger.info(f"📋 Obteniendo información básica del usuario: {db_user['id']}")
            user_info = users_table.get_user_basic_info(db_user["id"])
            
            if not user_info:
                logger.error(f"❌ No se pudo obtener información del usuario: {db_user['id']}")
                raise AuthError("Error obteniendo información del usuario")
            
            logger.info(f"✅ Información del usuario obtenida - Rol: {user_info['rol']['nombre']}")
            
            # 4. Actualizar último acceso
            logger.info(f"⏰ Actualizando último acceso para: {db_user['id']}")
            users_table.update_last_access(db_user["id"])
            
            logger.info(f"🎉 Inicio de sesión completado exitosamente para: {email}")
            
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
            db_user = users_table.get_by_auth_id(auth_response.user.id)
            
            if not db_user:
                return None
            
            # Obtener con información básica
            return users_table.get_user_basic_info(db_user["id"])
            
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
            db_user = users_table.get_by_auth_id(auth_response.user.id)
            
            if not db_user:
                return None
            
            # Obtener con información completa
            return users_table.get_user_complete_info(db_user["id"])
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario completo: {e}")
            return None
    
    @handle_supabase_error
    def verify_user_permission(self, module: str, action: str) -> bool:
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
            
            return users_table.verify_user_permission(
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


# Instancia singleton
auth = SupabaseAuth()

# Funciones de conveniencia para importar directamente

sign_in = auth.sign_in
sign_out = auth.sign_out
get_current_user = auth.get_current_user
get_current_user_complete = auth.get_current_user_complete
verify_user_permission = auth.verify_user_permission
get_session = auth.get_session