"""
Clase base para todos los servicios del sistema
Maneja funcionalidad común: permisos, errores, validaciones
CORREGIDA - Extracción correcta de rol y permisos
"""

from typing import Dict, List, Optional, Any, Union
from dental_system.supabase.client import supabase_client
import logging

logger = logging.getLogger(__name__)

class BaseService:
    """
    Clase base que proporciona funcionalidad común para todos los servicios
    """
    
    def __init__(self):
        self._client = None
        self.current_user_id: Optional[str] = None
        self.current_user_profile: Optional[Dict] = None
    
    @property
    def client(self):
        """Cliente de Supabase (lazy loading)"""
        if self._client is None:
            self._client = supabase_client.get_client()
        return self._client
    
    def set_user_context(self, user_id: str, user_profile: Dict[str, Any]):
        """Establece el contexto del usuario actual"""
        self.current_user_id = user_id
        self.current_user_profile = user_profile
        user_role = self._extract_user_role()
    
    def _extract_user_role(self) -> str:
        """
        CORREGIDO: Extrae el rol del usuario desde la estructura correcta
        """
        if not self.current_user_profile:
            return "unknown"
        
        # OPCIÓN 1: Desde estructura anidada rol.nombre (MÁS COMÚN)
        rol_obj = self.current_user_profile.get("rol", {})
        if isinstance(rol_obj, dict) and "nombre" in rol_obj:
            return rol_obj["nombre"]
        
        # OPCIÓN 2: Desde campo plano rol_nombre (FALLBACK)
        if "rol_nombre" in self.current_user_profile:
            return self.current_user_profile["rol_nombre"]
        
        # OPCIÓN 3: Desde campo role en inglés (FALLBACK ADICIONAL)
        if "role" in self.current_user_profile:
            return self.current_user_profile["role"]
        
        return "unknown"
    
    def _extract_user_permissions(self) -> Dict[str, List[str]]:
        """
        CORREGIDO: Extrae los permisos del usuario desde la estructura correcta
        """
        if not self.current_user_profile:
            return {}
        
        # OPCIÓN 1: Desde estructura anidada rol.permisos (MÁS COMÚN)
        rol_obj = self.current_user_profile.get("rol", {})
        if isinstance(rol_obj, dict) and "permisos" in rol_obj:
            permisos = rol_obj["permisos"]
            if isinstance(permisos, dict):
                return permisos
        
        # OPCIÓN 2: Desde campo plano rol_permisos (FALLBACK)
        if "rol_permisos" in self.current_user_profile:
            permisos = self.current_user_profile["rol_permisos"]
            if isinstance(permisos, dict):
                return permisos
        
        # OPCIÓN 3: Desde campo permisos directo (FALLBACK ADICIONAL)
        if "permisos" in self.current_user_profile:
            permisos = self.current_user_profile["permisos"]
            if isinstance(permisos, dict):
                return permisos
        
        return {}
    
    def check_permission(self, module: str, action: str) -> bool:
        """
        CORREGIDO: Verifica permisos del usuario actual con extracción mejorada
        
        Args:
            module: Módulo (pacientes, consultas, etc.)
            action: Acción (crear, leer, actualizar, eliminar)
            
        Returns:
            True si tiene permiso
        """
        if not self.current_user_profile:
            return False
        
        try:
            # CORREGIDO: Usar método mejorado de extracción
            permisos = self._extract_user_permissions()
            user_role = self._extract_user_role()

            if not permisos:
                return False

            module_permisos = permisos.get(module, [])
            has_permission = action in module_permisos

            # Permiso verificado

            return has_permission
            
        except Exception as e:
            logger.warning(f"Error verificando permisos: {e}")
            # Error verificando permisos
            return False
    
    def require_permission(self, module: str, action: str):
        """
        CORREGIDO: Requiere un permiso específico con extracción mejorada
        
        Args:
            module: Módulo requerido
            action: Acción requerida
            
        Raises:
            PermissionError: Si no tiene permiso
        """
        if not self.check_permission(module, action):
            # CORREGIDO: Usar método mejorado para obtener rol
            user_role = self._extract_user_role()
            
            error_msg = f"Usuario con rol '{user_role}' no tiene permiso para {action} en {module}"
            print(f"[ERROR] ❌ {error_msg}")
            
            # DEBUG adicional para diagnóstico
            permisos = self._extract_user_permissions()
            # Permisos disponibles para debug si es necesario
            
            raise PermissionError(error_msg)
    
    def handle_error(self, message: str, exception: Exception = None) -> None:
        """
        Maneja errores de forma consistente
        
        Args:
            message: Mensaje de error
            exception: Excepción opcional
        """
        if exception:
            logger.error(f"{message}: {exception}")
        else:
            logger.error(message)
        
        # Aquí podrías agregar notificaciones, métricas, etc.
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """
        Valida que los campos requeridos estén presentes
        
        Args:
            data: Datos a validar
            required_fields: Lista de campos requeridos
            
        Returns:
            Lista de campos faltantes
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field] or (isinstance(data[field], str) and not data[field].strip()):
                missing_fields.append(field)
        
        return missing_fields
    
    def format_error_message(self, base_message: str, validation_errors: List[str] = None) -> str:
        """
        Formatea mensajes de error de forma consistente
        
        Args:
            base_message: Mensaje base
            validation_errors: Lista de errores de validación
            
        Returns:
            Mensaje formateado
        """
        if validation_errors:
            return f"{base_message}. Campos faltantes: {', '.join(validation_errors)}"
        return base_message
    
    def safe_execute(self, operation_name: str, operation_func, *args, **kwargs):
        """
        Ejecuta una operación de forma segura con manejo de errores
        
        Args:
            operation_name: Nombre de la operación para logs
            operation_func: Función a ejecutar
            *args, **kwargs: Argumentos para la función
            
        Returns:
            Resultado de la operación o None si hay error
        """
        try:
            logger.info(f"Ejecutando operación: {operation_name}")
            result = operation_func(*args, **kwargs)
            logger.info(f"Operación '{operation_name}' completada exitosamente")
            return result
            
        except Exception as e:
            self.handle_error(f"Error en operación '{operation_name}'", e)
            return None
    
    def get_current_user_name(self) -> str:
        """
        MEJORADO: Obtiene el nombre del usuario actual de forma segura
        """
        if not self.current_user_profile:
            return "Usuario"
        
        # Intentar múltiples fuentes para el nombre
        name = (
            self.current_user_profile.get("nombre_completo") or
            self.current_user_profile.get("full_name") or
            self.current_user_profile.get("name") or
            ""
        )
        
        if name:
            return name
        
        # Fallback al email sin dominio
        email = self.current_user_profile.get("email", "")
        if email and "@" in email:
            return email.split("@")[0].title()
        
        return "Usuario"
    
    def build_success_message(self, action: str, entity: str, name: str = "") -> str:
        """
        Construye mensajes de éxito consistentes
        
        Args:
            action: Acción realizada (creado, actualizado, eliminado)
            entity: Entidad afectada (paciente, consulta, etc.)
            name: Nombre específico
            
        Returns:
            Mensaje de éxito formateado
        """
        if name:
            return f"{entity.capitalize()} '{name}' {action} exitosamente"
        return f"{entity.capitalize()} {action} exitosamente"
    
    def process_array_field(self, value: str, separator: str = ",") -> List[str]:
        """
        Procesa campos de array desde strings (como alergias, medicamentos)
        
        Args:
            value: String separado por comas
            separator: Separador usado
            
        Returns:
            Lista limpia de valores
        """
        if not value or not value.strip():
            return []
        
        return [item.strip() for item in value.split(separator) if item.strip()]
    
    def construct_full_name(self, primer_nombre: str, segundo_nombre: str = None, 
                          primer_apellido: str = None, segundo_apellido: str = None) -> str:
        """
        Construye nombre completo desde campos separados
        
        Args:
            primer_nombre: Primer nombre (requerido)
            segundo_nombre: Segundo nombre (opcional)
            primer_apellido: Primer apellido (opcional)
            segundo_apellido: Segundo apellido (opcional)
            
        Returns:
            Nombre completo construido
        """
        nombres = [primer_nombre]
        
        if segundo_nombre and segundo_nombre.strip():
            nombres.append(segundo_nombre.strip())
        if primer_apellido and primer_apellido.strip():
            nombres.append(primer_apellido.strip())
        if segundo_apellido and segundo_apellido.strip():
            nombres.append(segundo_apellido.strip())
        
        return " ".join(nombres) if nombres else "Sin nombre"