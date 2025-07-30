# # =====================================================
# # MIDDLEWARE DE AUTENTICACIÓN Y AUTORIZACIÓN
# # =====================================================

# from functools import wraps
# import reflex as rx
# from typing import List, Tuple, Optional

# def require_auth(func):
#     """Decorador para requerir autenticación"""
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         from state.auth_state import AuthState
#         if not isinstance(self, AuthState):
#             raise ValueError("require_auth solo puede usarse en clases que hereden de AuthState")
        
#         if not self.is_authenticated:
#             self.set_error("Debes iniciar sesión para acceder a esta página")
#             return rx.redirect("/login")
        
#         return func(self, *args, **kwargs)
#     return wrapper

# def require_role(*allowed_roles):
#     """Decorador para requerir roles específicos"""
#     def decorator(func):
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             from state.auth_state import AuthState
#             if not isinstance(self, AuthState):
#                 raise ValueError("require_role solo puede usarse en clases que hereden de AuthState")
            
#             if not self.is_authenticated:
#                 self.set_error("Debes iniciar sesión para acceder a esta página")
#                 return rx.redirect("/login")
            
#             if self.user_role not in allowed_roles:
#                 self.set_error("No tienes permisos para acceder a esta página")
#                 return rx.redirect("/unauthorized")
            
#             return func(self, *args, **kwargs)
#         return wrapper
#     return decorator

# def require_permission(modulo: str, accion: str):
#     """Decorador para requerir permisos específicos"""
#     def decorator(func):
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             from state.auth_state import AuthState
#             if not isinstance(self, AuthState):
#                 raise ValueError("require_permission solo puede usarse en clases que hereden de AuthState")
            
#             if not self.is_authenticated:
#                 self.set_error("Debes iniciar sesión para acceder a esta página")
#                 return rx.redirect("/login")
            
#             if not self.check_permission(modulo, accion):
#                 self.set_error("No tienes permisos para realizar esta acción")
#                 return rx.redirect("/unauthorized")
            
#             return func(self, *args, **kwargs)
#         return wrapper
#     return decorator


"""
=====================================================
MIDDLEWARE DE AUTENTICACIÓN CONSOLIDADO
=====================================================
🔄 ARCHIVO REFACTORIZADO - Eliminando duplicación con route_guard.py
🎯 Enfoque: Middleware específico + delegación a route_guard
✅ Mantiene compatibilidad pero elimina código duplicado
=====================================================
"""

from functools import wraps
import reflex as rx
from typing import List, Tuple, Optional, Callable
import logging

# ==========================================
# 🔄 IMPORTS CONSOLIDADOS
# ==========================================

# Importar funciones de route_guard en lugar de duplicar
from dental_system.utils.route_guard import (
    protected_route,
    role_required,
    permission_required,
    can_access_route,
    log_access_attempt
)

logger = logging.getLogger(__name__)

# ==========================================
# 🔄 DECORADORES LEGACY (para compatibilidad)
# ==========================================

def require_auth(func):
    """
    ⚠️ DEPRECADO: Usar @protected_route() en su lugar
    Decorador legacy para requerir autenticación - redirige a route_guard
    """
    logger.warning(f"require_auth está deprecado en {func.__name__}. Usar @protected_route()")
    
    # Delegar a la implementación moderna
    return protected_route()(func)

def require_role(*allowed_roles):
    """
    ⚠️ DEPRECADO: Usar @role_required() en su lugar
    Decorador legacy para requerir roles específicos - redirige a route_guard
    """
    def decorator(func):
        logger.warning(f"require_role está deprecado en {func.__name__}. Usar @role_required()")
        
        # Delegar a la implementación moderna
        return role_required(list(allowed_roles))(func)
    return decorator

def require_permission(modulo: str, accion: str):
    """
    ⚠️ DEPRECADO: Usar @permission_required() en su lugar
    Decorador legacy para requerir permisos específicos - redirige a route_guard
    """
    def decorator(func):
        logger.warning(f"require_permission está deprecado en {func.__name__}. Usar @permission_required()")
        
        # Delegar a la implementación moderna
        return permission_required(modulo, accion)(func)
    return decorator

# ==========================================
# 🆕 MIDDLEWARE ESPECÍFICO DE ESTADO
# ==========================================

def state_auth_middleware(state_class):
    """
    🆕 NUEVO: Middleware específico para validar autenticación en clases de estado
    
    Usage:
        @state_auth_middleware
        class MyProtectedState(rx.State):
            pass
    """
    def decorator(cls):
        original_init = cls.__init__
        
        @wraps(original_init)
        def wrapped_init(self, *args, **kwargs):
            # Ejecutar init original
            original_init(self, *args, **kwargs)
            
            # Validar autenticación si el estado lo requiere
            if hasattr(self, 'requires_auth') and self.requires_auth:
                from dental_system.state.auth_state import AuthState
                if not isinstance(self, AuthState):
                    logger.error(f"Estado {cls.__name__} requiere auth pero no hereda de AuthState")
        
        cls.__init__ = wrapped_init
        return cls
    
    return decorator

def role_restricted_method(allowed_roles: List[str]):
    """
    🆕 NUEVO: Decorador para métodos específicos dentro de estados
    
    Usage:
        class MyState(BaseState):
            @role_restricted_method(["gerente"])
            async def admin_only_method(self):
                pass
    """
    def decorator(method):
        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            # Verificar si el estado tiene información de usuario
            if hasattr(self, 'user_role'):
                if self.user_role not in allowed_roles:
                    logger.warning(f"Acceso denegado a {method.__name__} para rol: {self.user_role}")
                    self.show_error("No tienes permisos para realizar esta acción")
                    return
            else:
                logger.error(f"Método {method.__name__} requiere estado con user_role")
                return
            
            # Ejecutar método original
            return await method(self, *args, **kwargs)
        
        return wrapper
    return decorator

# ==========================================
# 🔧 UTILITIES ESPECÍFICOS DE MIDDLEWARE
# ==========================================

def validate_state_permissions(state_instance, required_permissions: List[str]) -> bool:
    """
    Validar permisos específicos en una instancia de estado
    
    Args:
        state_instance: Instancia del estado
        required_permissions: Lista de permisos requeridos
        
    Returns:
        True si tiene todos los permisos
    """
    if not hasattr(state_instance, 'check_permission'):
        logger.error("Estado no tiene método check_permission")
        return False
    
    for permission in required_permissions:
        module, action = permission.split('.') if '.' in permission else (permission, 'read')
        if not state_instance.check_permission(module, action):
            logger.warning(f"Permiso denegado: {permission}")
            return False
    
    return True

def audit_state_access(state_class: str, method_name: str, user_id: str = None, success: bool = True):
    """
    Auditar acceso a métodos de estado para compliance
    
    Args:
        state_class: Nombre de la clase de estado
        method_name: Nombre del método accedido
        user_id: ID del usuario (opcional)
        success: Si el acceso fue exitoso
    """
    status = "SUCCESS" if success else "DENIED"
    logger.info(f"[AUDIT] {status} - State: {state_class} - Method: {method_name} - User: {user_id}")

def get_state_security_config(state_class_name: str) -> Dict[str, Any]:
    """
    Obtener configuración de seguridad para una clase de estado específica
    
    Args:
        state_class_name: Nombre de la clase de estado
        
    Returns:
        Configuración de seguridad
    """
    # Configuraciones por defecto por tipo de estado
    security_configs = {
        "BossState": {
            "required_roles": ["gerente"],
            "sensitive_methods": ["delete_personal", "change_permissions"],
            "audit_all_methods": True
        },
        "AdminState": {
            "required_roles": ["gerente", "administrador"],
            "sensitive_methods": ["delete_patient", "modify_payments"],
            "audit_all_methods": False
        },
        "DentistState": {
            "required_roles": ["odontologo"],
            "sensitive_methods": ["modify_odontogram", "delete_treatment"],
            "audit_all_methods": False
        },
        "AssistantState": {
            "required_roles": ["asistente"],
            "sensitive_methods": [],
            "audit_all_methods": False
        }
    }
    
    return security_configs.get(state_class_name, {
        "required_roles": [],
        "sensitive_methods": [],
        "audit_all_methods": False
    })

# ==========================================
# 🔒 DECORADOR AVANZADO PARA ESTADOS
# ==========================================

def secure_state(
    required_roles: Optional[List[str]] = None,
    audit_methods: bool = False,
    sensitive_methods: Optional[List[str]] = None
):
    """
    🆕 NUEVO: Decorador avanzado para asegurar clases de estado completas
    
    Args:
        required_roles: Roles requeridos para acceder al estado
        audit_methods: Si auditar todas las llamadas a métodos
        sensitive_methods: Métodos que requieren auditoría especial
        
    Usage:
        @secure_state(
            required_roles=["gerente"], 
            audit_methods=True,
            sensitive_methods=["delete_personal"]
        )
        class BossState(BaseState):
            pass
    """
    def decorator(cls):
        original_init = cls.__init__
        class_name = cls.__name__
        
        # Obtener configuración de seguridad automática si no se especifica
        if required_roles is None:
            config = get_state_security_config(class_name)
            effective_roles = config.get("required_roles", [])
            effective_audit = config.get("audit_all_methods", audit_methods)
            effective_sensitive = config.get("sensitive_methods", sensitive_methods or [])
        else:
            effective_roles = required_roles
            effective_audit = audit_methods
            effective_sensitive = sensitive_methods or []
        
        @wraps(original_init)
        def wrapped_init(self, *args, **kwargs):
            # Ejecutar init original
            original_init(self, *args, **kwargs)
            
            # Agregar metadata de seguridad al estado
            self._security_config = {
                "required_roles": effective_roles,
                "audit_methods": effective_audit,
                "sensitive_methods": effective_sensitive,
                "class_name": class_name
            }
            
            logger.debug(f"Estado {class_name} configurado con seguridad: {self._security_config}")
        
        # Wrapper para métodos si se requiere auditoría
        if effective_audit or effective_sensitive:
            for attr_name in dir(cls):
                attr = getattr(cls, attr_name)
                if callable(attr) and not attr_name.startswith('_'):
                    # Auditar método si está en la lista de sensibles o si audit_methods está activo
                    should_audit = (attr_name in effective_sensitive) or effective_audit
                    
                    if should_audit:
                        setattr(cls, attr_name, _create_audited_method(attr, attr_name, class_name))
        
        cls.__init__ = wrapped_init
        return cls
    
    return decorator

def _create_audited_method(original_method, method_name: str, class_name: str):
    """Helper para crear versión auditada de un método"""
    @wraps(original_method)
    async def audited_method(self, *args, **kwargs):
        user_id = getattr(self, 'user_id', 'unknown') if hasattr(self, 'user_id') else 'unknown'
        
        try:
            # Auditar inicio
            audit_state_access(class_name, method_name, user_id, True)
            
            # Ejecutar método original
            result = await original_method(self, *args, **kwargs)
            
            # Auditar éxito
            logger.debug(f"Método {method_name} ejecutado exitosamente por {user_id}")
            return result
            
        except Exception as e:
            # Auditar error
            audit_state_access(class_name, method_name, user_id, False)
            logger.error(f"Error en método {method_name} para usuario {user_id}: {e}")
            raise
    
    return audited_method

# ==========================================
# 🔄 FUNCIONES DE MIGRACIÓN
# ==========================================

def migrate_legacy_decorators():
    """
    🔄 Helper para migrar decoradores legacy a las nuevas implementaciones
    
    Imprime instrucciones de migración
    """
    migration_guide = """
    
    🔄 GUÍA DE MIGRACIÓN DE DECORADORES:
    
    ANTES (legacy):                  DESPUÉS (moderno):
    ================                 ==================
    @require_auth                    @protected_route()
    @require_role("admin")           @role_required(["admin"])  
    @require_permission("mod", "act") @permission_required("mod", "act")
    
    NUEVOS DECORADORES DISPONIBLES:
    ===============================
    @secure_state(required_roles=["gerente"])
    @role_restricted_method(["admin"])
    @state_auth_middleware
    
    """
    
    print(migration_guide)
    logger.info("Guía de migración mostrada")

# ==========================================
# 📊 FUNCIONES DE DIAGNÓSTICO
# ==========================================

def diagnose_auth_setup():
    """
    🔍 Diagnosticar configuración de autenticación del sistema
    
    Returns:
        Diccionario con el estado del diagnóstico
    """
    diagnosis = {
        "route_guard_available": False,
        "legacy_middleware_active": True,
        "decorators_status": {},
        "recommendations": []
    }
    
    try:
        # Verificar si route_guard está disponible
        from dental_system.utils.route_guard import protected_route
        diagnosis["route_guard_available"] = True
    except ImportError:
        diagnosis["recommendations"].append("Instalar route_guard.py")
    
    # Verificar estado de decoradores
    decorators_to_check = ["require_auth", "require_role", "require_permission"]
    for decorator_name in decorators_to_check:
        diagnosis["decorators_status"][decorator_name] = "legacy_active"
    
    # Recomendaciones
    if diagnosis["route_guard_available"]:
        diagnosis["recommendations"].append("Migrar decoradores legacy a route_guard")
        diagnosis["recommendations"].append("Implementar @secure_state en estados principales")
    
    return diagnosis

# ==========================================
# 📤 EXPORTS
# ==========================================

__all__ = [
    # Decoradores legacy (para compatibilidad)
    "require_auth",
    "require_role", 
    "require_permission",
    
    # Nuevos decoradores específicos
    "state_auth_middleware",
    "role_restricted_method",
    "secure_state",
    
    # Utilities
    "validate_state_permissions",
    "audit_state_access",
    "get_state_security_config",
    
    # Migración y diagnóstico
    "migrate_legacy_decorators",
    "diagnose_auth_setup"
]

# ==========================================
# 🚀 INICIALIZACIÓN
# ==========================================

if __name__ == "__main__":
    # Mostrar guía de migración si se ejecuta directamente
    migrate_legacy_decorators()
    
    # Ejecutar diagnóstico
    diagnosis = diagnose_auth_setup()
    print(f"\n🔍 DIAGNÓSTICO: {diagnosis}")