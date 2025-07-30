
"""
Operaciones CRUD para usuarios - SIN TRIGGER, CONTROL TOTAL DESDE PYTHON
Maneja auth.users Y tabla usuarios de forma manual y confiable
"""
import json
from typing import Dict, List, Optional, Any
from .base import BaseTable
from ..client import handle_supabase_error, supabase_client
import logging


logger = logging.getLogger(__name__)


class UsersTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para usuarios - VERSIÓN SIN TRIGGER
    Control total desde Python para máxima confiabilidad
    """
    
    def __init__(self):
        super().__init__('usuarios')
    
    @handle_supabase_error
    def crear_usuario(
        self,
        email: str,
        password: str,
        rol: str = 'administrador',
        telefono: str = '',
        nombre: str = '',
        apellido: str = '',
        avatar_url: str = '',
        activo: bool = True,
        configuraciones: dict = None, # type: ignore
        method: str = 'admin'
    ) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo usuario manejando auth.users Y tabla usuarios desde Python
        
        Args:
            email: Correo electrónico del usuario
            password: Contraseña del usuario
            rol: Rol del usuario (por defecto 'administrador')
            telefono: Número de teléfono (opcional)
            nombre: Nombre del usuario (opcional)
            apellido: Apellido del usuario (opcional)
            avatar_url: URL del avatar (opcional)
            activo: Estado del usuario (por defecto True)
            configuraciones: Configuraciones adicionales (opcional)
            method: Método a usar ('admin' o 'signup')
        
        Returns:
            dict: Información del usuario creado o None si falla
        """
        logger.info(f"🚀 Creando usuario con método {method}: {email}")
        
        try:
            # Validaciones básicas
            if not email or not password:
                raise ValueError("Email y contraseña son requeridos")
            
            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            
            # Verificar que el email no exista ya
            existing_user = self.get_by_email(email)
            if existing_user:
                raise ValueError("El email ya está registrado en tabla usuarios")
            
            # Paso 1: Crear usuario en auth.users
            user_metadata = {
                'rol': rol,
                'telefono': telefono,
                'nombre': nombre,
                'apellido': apellido,
                'avatar_url': avatar_url,
                'managed_by': 'python'
            }
            auth_user = self.create_auth_user(email, password,user_metadata)
            
            
            if not auth_user:
                raise ValueError("No se pudo crear usuario en auth.users")
            
            logger.info(f"✅ Usuario creado en auth.users - ID: {auth_user['id']}")
            
            # Paso 2: Crear registro en tabla usuarios
            try:
                db_user = self._create_user_record(
                    auth_user_id=auth_user['id'],
                    email=email,
                    rol=rol,
                    telefono=telefono,
                    avatar_url=avatar_url,
                    configuraciones=configuraciones
                )
                
                if not db_user:
                    # Si falla, limpiar auth.users
                    self._cleanup_auth_user(auth_user['id'], method)
                    raise ValueError("No se pudo crear registro en tabla usuarios")
                
                logger.info(f"✅ Registro creado en tabla usuarios - ID: {db_user['id']}")
                
                return {
                    'success': True,
                    'message': 'Usuario creado exitosamente sin trigger',
                    'user_id': db_user['id'],
                    'auth_user_id': auth_user['id'],
    
                }
                
            except Exception as e:
                logger.error(f"❌ Error creando registro en tabla usuarios: {e}")
                # Limpiar usuario de auth.users si falló
                self._cleanup_auth_user(auth_user['id'], method)
                raise ValueError(f"Error al crear registro de usuario: {str(e)}")
                
        except Exception as e:
            logger.error(f"❌ Error general creando usuario {email}: {e}")
            raise ValueError(f"Error al crear usuario: {str(e)}")



    @handle_supabase_error
    def create_auth_user(self, email: str, password: str, user_metadata: dict) -> Dict[str, Any]:
        """Crear usuario con admin.create_user"""
        admin_client = supabase_client.get_admin_client()
        
        if not admin_client:
            raise ValueError("No hay cliente administrativo disponible")
        
        auth_response = admin_client.auth.admin.create_user({
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
      

    def _create_user_record(self, auth_user_id: str, email: str, rol: str, telefono: str, avatar_url: str, configuraciones: dict) -> Optional[Dict[str, Any]]:
        """Crear registro en tabla usuarios"""
        logger.info("📝 Creando registro en tabla usuarios...")
        
        try:
            # Obtener ID del rol
            rol_id = self._get_role_id(rol)
            if not rol_id:
                raise ValueError(f"No se pudo obtener ID para rol: {rol}")
            
            # Preparar datos del usuario
            user_data = {
                'auth_user_id': auth_user_id,
                'email': email,
                'telefono': telefono if telefono else None,
                'rol_id': rol_id,
                'avatar_url': avatar_url if avatar_url else None,
                'activo': True,
                'metadata': configuraciones or {},
                'configuraciones': configuraciones or {}
            }
            
            # Insertar en tabla usuarios
            response = self.table.insert(user_data).execute()
            
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
    
    def _get_role_id(self, rol_name: str) -> Optional[str]:
        """Obtener ID del rol con fallbacks"""
        try:
            # Usar función SQL que creamos
            result = self.client.rpc('get_role_id_by_name', {'role_name': rol_name}).execute()
            
            if result.data:
                return result.data[0] if isinstance(result.data, list) else result.data
            
            # Fallback manual si la función no existe
            logger.warning("Función get_role_id_by_name no disponible, usando fallback manual")
            
            # Buscar rol exacto
            rol_response = self.client.table("roles").select("id").eq("nombre", rol_name).eq("activo", True).execute()
            if rol_response.data:
                return rol_response.data[0]["id"]
            
            # Fallback a administrador
            admin_response = self.client.table("roles").select("id").eq("nombre", "administrador").eq("activo", True).execute()
            if admin_response.data:
                logger.warning(f"Rol '{rol_name}' no encontrado, usando administrador")
                return admin_response.data[0]["id"]
            
            # Fallback al primer rol disponible
            first_response = self.client.table("roles").select("id").eq("activo", True).order("nombre").limit(1).execute()
            if first_response.data:
                logger.warning("Rol administrador no encontrado, usando primer rol disponible")
                return first_response.data[0]["id"]
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo rol ID: {e}")
            return None
    
 
    
    def _cleanup_auth_user(self, auth_user_id: str, method: str):
        """Limpiar usuario de auth.users si falló la creación completa"""
        try:
            logger.warning(f"🧹 Limpiando usuario de auth.users: {auth_user_id}")
            
            if method == 'admin':
                admin_client = supabase_client.get_admin_client()
                if admin_client:
                    admin_client.auth.admin.delete_user(auth_user_id)
                    logger.info("✅ Usuario eliminado de auth.users con admin")
            else:
                # Para signup es más complejo eliminar, por ahora solo logeamos
                logger.warning("⚠️ Usuario de signup no eliminado automáticamente de auth.users")
                logger.warning("💡 Eliminar manualmente desde Supabase Dashboard si es necesario")
                
        except Exception as e:
            logger.error(f"❌ Error limpiando auth.users: {e}")
    
    def _map_rol_to_tipo_personal(self, rol: str) -> str:
        """Mapea el rol del sistema al tipo de personal"""
        mapping = {
            'gerente': 'Gerente',
            'administrador': 'Administrador', 
            'odontologo': 'Odontólogo',
            'asistente': 'Asistente'
        }
        return mapping.get(rol, 'Administrador')

    
    # ========================================
    # MÉTODOS EXISTENTES (sin cambios)
    # ========================================
    
    @handle_supabase_error
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su email"""
        response = self.table.select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_by_auth_id(self, auth_user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su ID de auth.users"""
        logger.info(f"Buscando usuario con auth_user_id: {auth_user_id}")
        response = self.table.select("*").eq("auth_user_id", auth_user_id).execute()
        result = response.data[0] if response.data else None
        logger.info(f"Usuario encontrado: {result is not None}")
        return result
    
    @handle_supabase_error  
    def get_user_basic_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información básica del usuario con su rol"""
        logger.info(f"Obteniendo info básica del usuario: {user_id}")
        
        user = self.get_by_id(user_id)
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado")
            return None
        
        rol_response = self.client.table("roles").select("nombre, descripcion, permisos").eq("id", user["rol_id"]).execute()
        
        if rol_response.data:
            user["rol"] = rol_response.data[0]
        else:
            logger.warning(f"Rol no encontrado para usuario {user_id}")
            user["rol"] = {"nombre": "sin_rol", "descripcion": "Sin rol", "permisos": {}}
        
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
    def update_last_access(self, user_id: str) -> bool:
        """Actualiza el último acceso del usuario"""
        from datetime import datetime
        response = self.table.update({
            "ultimo_acceso": datetime.now().isoformat()
        }).eq("id", user_id).execute()
        
        return bool(response.data)
    
    @handle_supabase_error
    def verify_user_permission(self, user_id: str, module: str, action: str) -> bool:
        """Verifica si un usuario tiene permiso para realizar una acción"""
        user = self.get_user_basic_info(user_id)
        
        if not user or not user.get("activo"):
            return False
        
        permisos = user.get("rol", {}).get("permisos", {})
        modulo_permisos = permisos.get(module, [])
        
        return action in modulo_permisos

# Instancia única para importar  
users_table = UsersTable()