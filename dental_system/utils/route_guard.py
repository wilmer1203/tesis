# 🔒 PROTECCIÓN DE RUTAS - VERSIÓN SIMPLIFICADA Y FUNCIONAL
# dental_system/utils/route_guard.py

import reflex as rx
from dental_system.state.app_state import AppState
from typing import List, Optional, Callable
import functools

# ==========================================
# 🛡️ DECORADOR PRINCIPAL - SIMPLE Y CLARO
# ==========================================

def protected_route(required_roles: Optional[List[str]] = None):
    """
    🔒 DECORADOR PRINCIPAL para rutas protegidas
    
    Args:
        required_roles: Lista de roles permitidos ["gerente", "administrador", "odontologo"]
    
    Usage:
        @protected_route(required_roles=["gerente"])
        def boss_page():
            return rx.text("Solo gerentes")
    """
    def decorator(component_func: Callable) -> Callable:
        @functools.wraps(component_func)
        def wrapper(*args, **kwargs) -> rx.Component:
            return create_protected_component(
                component_func=component_func,
                required_roles=required_roles,
                args=args,
                kwargs=kwargs
            )
        return wrapper
    return decorator

# ==========================================
# 🔧 LÓGICA DE PROTECCIÓN - SIMPLE Y FUNCIONAL
# ==========================================

def create_protected_component(
    component_func: Callable,
    required_roles: Optional[List[str]] = None,
    args: tuple = (),
    kwargs: dict = {}
) -> rx.Component:
    """
    🛡️ CREAR COMPONENTE PROTEGIDO - LÓGICA CORREGIDA PARA REFLEX
    """
    return rx.cond(
        # PASO 1: ¿Está autenticado?
        ~AppState.esta_autenticado,
        
        # ❌ NO AUTENTICADO → Página de login
        login_required_page(),
        
        # ✅ SÍ AUTENTICADO → Verificar rol
        rx.cond(
            # PASO 2: ¿Tiene el rol correcto?
            build_role_check(required_roles),
            
            # ✅ ROL CORRECTO → Mostrar contenido
            component_func(*args, **kwargs),
            
            # ❌ ROL INCORRECTO → Página de acceso denegado
            unauthorized_page(required_roles)
        )
    )

def build_role_check(required_roles: Optional[List[str]]):
    """
    🔍 CONSTRUIR VERIFICACIÓN DE ROLES USANDO OPERADORES DE REFLEX
    """
    # Si no hay restricciones de rol, permitir acceso
    if not required_roles:
        return True
    
    # Si solo hay un rol requerido, verificación simple
    if len(required_roles) == 1:
        return AppState.rol_usuario == required_roles[0]
    
    # Si hay múltiples roles, usar OR bitwise (|)
    conditions = [AppState.rol_usuario == role for role in required_roles]
    result = conditions[0]
    for condition in conditions[1:]:
        result = result | condition
    
    return result

# ==========================================
# 🎯 DECORADORES ESPECÍFICOS POR ROL - SHORTCUTS
# ==========================================

def boss_only_component(component_func: Callable) -> Callable:
    """🎯 Solo para gerentes"""
    return protected_route(required_roles=["gerente"])(component_func)

def admin_or_boss_component(component_func: Callable) -> Callable:
    """👥 Para administradores y gerentes"""
    return protected_route(required_roles=["gerente", "administrador"])(component_func)

def dentist_component(component_func: Callable) -> Callable:
    """🦷 Solo para odontólogos"""
    return protected_route(required_roles=["odontologo"])(component_func)

def assistant_component(component_func: Callable) -> Callable:
    """👩‍⚕️ Solo para asistentes"""
    return protected_route(required_roles=["asistente"])(component_func)

def authenticated_only_component(component_func: Callable) -> Callable:
    """🔐 Para cualquier usuario autenticado"""
    return protected_route()(component_func)

# ==========================================
# 📄 PÁGINAS DE ERROR - SIMPLES Y CLARAS
# ==========================================

def login_required_page() -> rx.Component:
    """🚪 Página que pide iniciar sesión"""
    return rx.center(
        rx.card(
            rx.vstack(
                # Ícono
                rx.icon("shield-alert", size=64, color="orange"),
                
                # Título
                rx.heading(
                    "🔒 Inicia Sesión",
                    size="8",
                    color="orange.600"
                ),
                
                # Mensaje
                rx.text(
                    "Debes iniciar sesión para acceder a esta página",
                    color="gray.600",
                    text_align="center",
                    size="4"
                ),
                
                # Botón
                rx.button(
                    rx.hstack(
                        rx.icon("log-in", size=20),
                        rx.text("Iniciar Sesión"),
                        spacing="2"
                    ),
                    on_click=lambda: rx.redirect("/login"),
                    color_scheme="teal",
                    size="3"
                ),
                
                spacing="4",
                text_align="center",
                padding="2rem"
            ),
            
            width="100%",
            max_width="400px",
            box_shadow="lg"
        ),
        
        min_height="100vh",
        background="gray.50",
        padding="2rem"
    )

def unauthorized_page(required_roles: Optional[List[str]] = None) -> rx.Component:
    """❌ Página de acceso denegado"""
    
    # Mensaje específico según los roles requeridos
    if required_roles:
        roles_text = ", ".join(required_roles)
        message = f"Esta página requiere uno de estos roles: {roles_text}"
    else:
        message = "No tienes permisos para acceder a esta página"
    
    return rx.center(
        rx.card(
            rx.vstack(
                # Ícono
                rx.icon("shield-x", size=64, color="red"),
                
                # Título
                rx.heading(
                    "🚫 Acceso Denegado", 
                    size="8",
                    color="red.600"
                ),
                
                # Mensaje
                rx.text(
                    message,
                    color="gray.600",
                    text_align="center",
                    size="4"
                ),
                
                # Info del usuario actual
                rx.box(
                    rx.text(f"Tu rol actual: {AppState.rol_usuario}", color="gray.500", size="3"),
                    text_align="center",
                    padding="2"
                ),
                
                # Botones
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("arrow-left", size=20),
                            rx.text("Volver"),
                            spacing="2"
                        ),
                        on_click=lambda: rx.redirect("/"),
                        color_scheme="teal",
                        size="3"
                    ),
                    
                    rx.button(
                        rx.hstack(
                            rx.icon("log-out", size=20),
                            rx.text("Cerrar Sesión"),
                            spacing="2"
                        ),
                        on_click=AppState.cerrar_sesion,
                        color_scheme="red",
                        size="3",
                        variant="outline"
                    ),
                    
                    spacing="3"
                ),
                
                spacing="4",
                text_align="center",
                padding="2rem"
            ),
            
            width="100%",
            max_width="500px",
            box_shadow="lg"
        ),
        
        min_height="100vh",
        background="gray.50",
        padding="2rem"
    )

# ==========================================
# 🔍 FUNCIONES AUXILIARES - SOLO LAS NECESARIAS
# ==========================================

def can_access_route(user_role: str, required_roles: Optional[List[str]] = None) -> bool:
    """
    🔍 Verificar programáticamente si un usuario puede acceder (Python normal)
    
    Usage:
        if can_access_route("gerente", ["gerente", "administrador"]):
            # Permitir acceso
    
    Nota: Esta función es para lógica de Python normal, no para Vars de Reflex
    """
    if not required_roles:
        return True
    
    return user_role in required_roles

def get_accessible_routes(user_role: str) -> List[str]:
    """📋 Obtener rutas accesibles para un rol"""
    route_permissions = {
        "gerente": ["/", "/boss", "/admin", "/dentist", "/assistant"],  # Gerente accede a todo
        "administrador": ["/", "/admin"],
        "odontologo": ["/", "/dentist"],
        "asistente": ["/", "/assistant"]
    }

    return route_permissions.get(user_role, ["/"])

# ==========================================
# 📤 EXPORTACIONES - SOLO LO ESENCIAL
# ==========================================

__all__ = [
    # Decorador principal
    "protected_route",

    # Decoradores por rol
    "boss_only_component",
    "admin_or_boss_component",
    "dentist_component",
    "assistant_component",
    "authenticated_only_component",

    # Páginas de error
    "login_required_page",
    "unauthorized_page",

    # Utilidades
    "can_access_route",
    "get_accessible_routes"
]

"""

🔧 CÓMO USAR:
@boss_only_component
def boss_page():
    return rx.text("Solo gerentes")

@admin_or_boss_component  
def admin_page():
    return rx.text("Admins y gerentes")

@protected_route(required_roles=["odontologo"])
def custom_page():
    return rx.text("Solo odontólogos")
"""
