
"""
=====================================================
ESTADO DE AUTENTICACIÓN
=====================================================
✅ Manejo robusto de errores y sesiones
=====================================================
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from ..supabase.auth import auth
import logging
import asyncio

logger = logging.getLogger(__name__)

class AuthState(rx.State):
    """Estado de autenticación CORREGIDO - Versión optimizada y segura"""
    
    # ==========================================
    # 🔐 ESTADO DE AUTENTICACIÓN PRINCIPAL
    # ==========================================
    current_user: Optional[Dict[str, Any]] = None
    is_authenticated: bool = False
    
    user_profile: Optional[Dict[str, Any]] = None
    user_role: str = ""
    user_permissions: Dict[str, List[str]] = {}

    # ==========================================
    # 🎨 ESTADO DE UI Y MENSAJES
    # ==========================================
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # ==========================================
    # 🔑 TOKENS Y SESIÓN DE SUPABASE
    # ==========================================
    access_token: str = ""
    refresh_token: str = ""
    session_expires: Optional[datetime] = None
    session_last_check: Optional[datetime] = None
    
    # ==========================================
    # 👤 INFORMACIÓN ADICIONAL DEL USUARIO
    # ==========================================
    personal_info: Optional[Dict[str, Any]] = None
    theme: str = "light"
    
    # ==========================================
    # 📝 FORMULARIOS DE AUTENTICACIÓN
    # ==========================================
    login_email: str = ""
    login_password: str = ""
    
    # ==========================================
    # 🔧 CONFIGURACIÓN DE SEGURIDAD
    # ==========================================
    auto_logout_enabled: bool = True
    session_timeout_minutes: int = 60  # 1 hora por defecto
    failed_login_attempts: int = 0
    max_failed_attempts: int = 5
    lockout_until: Optional[datetime] = None

    # ==========================================
    # 🚀 INICIALIZACIÓN MEJORADA
    # ==========================================
    
    def on_load(self):
        """Verificación de autenticación mejorada al cargar la app"""
        print("[DEBUG] 🔄 Iniciando verificación de autenticación...")
        return self.check_authentication_enhanced()
        
    async def check_authentication_enhanced(self):
        """
        ✅ VERSIÓN MEJORADA: Verificación completa de autenticación
        """
        print("[DEBUG] 🔍 Ejecutando check_authentication_enhanced...")
        
        try:
            # 1. Verificar si hay lockout activo
            if self.is_locked_out():
                print("[DEBUG] 🚫 Usuario bloqueado por intentos fallidos")
                self.clear_auth_state()
                return
            
            # 2. Obtener usuario actual con manejo de errores
            user = await self._safe_get_current_user()
            
            if user:
                print(f"[DEBUG] ✅ Usuario encontrado: {user.get('email', 'N/A')}")
                
                # 3. Validar que la sesión no haya expirado
                if not self.is_session_valid:
                    print("[DEBUG] ⏰ Sesión expirada, limpiando estado")
                    await self.logout_silent()
                    return
                
                # 4. Actualizar estado de autenticación
                self._update_auth_state(user)
                
                # 5. Registrar último check
                self.session_last_check = datetime.now()
                
                print(f"[DEBUG] 🎯 Usuario autenticado exitosamente - Rol: {self.user_role}")
                
            else:
                print("[DEBUG] ❌ No hay usuario autenticado")
                self.clear_auth_state()
                
        except Exception as e:
            logger.error(f"💥 Error en check_authentication_enhanced: {e}")
            print(f"[DEBUG] ⚠️ Error verificando autenticación: {e}")
            self.clear_auth_state()

    async def _safe_get_current_user(self) -> Optional[Dict[str, Any]]:
        """Obtener usuario actual con manejo seguro de errores"""
        try:
            # Intentar con timeout
            return await asyncio.wait_for(
                asyncio.create_task(self._get_user_async()), 
                timeout=10.0  # 10 segundos máximo
            )
        except asyncio.TimeoutError:
            logger.error("Timeout obteniendo usuario actual")
            return None
        except Exception as e:
            logger.error(f"Error obteniendo usuario: {e}")
            return None

    async def _get_user_async(self) -> Optional[Dict[str, Any]]:
        """Wrapper async para obtener usuario"""
        return auth.get_current_user()

    def _update_auth_state(self, user: Dict[str, Any]):
        """Actualizar estado de autenticación de forma segura"""
        try:
            self.current_user = user
            self.is_authenticated = True
            self.user_role = user.get("rol", {}).get("nombre", "")
            self.user_permissions = user.get("rol", {}).get("permisos", {})
            self.user_profile = user
            
            # Resetear intentos fallidos en login exitoso
            self.failed_login_attempts = 0
            self.lockout_until = None
            
        except Exception as e:
            logger.error(f"Error actualizando estado de auth: {e}")
            self.clear_auth_state()

    # ==========================================
    # 🔐 LOGIN MEJORADO CON VALIDACIONES
    # ==========================================
    
    async def login(self, form_data: Dict[str, Any]) -> None:
        """
        ✅ LOGIN MEJORADO con validaciones exhaustivas y manejo de errores
        """
        print("[DEBUG] 🚀 ===== INICIANDO LOGIN MEJORADO =====")
        
        # Verificar lockout antes de intentar login
        if self.is_locked_out():
            remaining_time = (self.lockout_until - datetime.now()).seconds // 60
            self.error_message = f"Cuenta bloqueada. Intenta en {remaining_time} minutos"
            return
        
        self.set_loading(True)
        self.clear_messages()
        
        try:
            # 1. VALIDACIONES MEJORADAS
            validation_result = self._validate_login_form(form_data)
            if not validation_result["valid"]:
                self.error_message = validation_result["message"]
                return
            
            email = form_data.get("email", "").strip().lower()
            password = form_data.get("password", "").strip()
            
            print(f"[DEBUG] 🔑 Intentando login para: {email}")
            
            # 2. AUTENTICACIÓN CON TIMEOUT
            try:
                session, user_info = await asyncio.wait_for(
                    self._authenticate_user(email, password),
                    timeout=15.0  # 15 segundos máximo
                )
            except asyncio.TimeoutError:
                raise Exception("Timeout de conexión. Verifica tu internet")
            
            print(f"[DEBUG] ✅ Autenticación exitosa para: {email}")
            
            # 3. ACTUALIZAR ESTADO COMPLETO
            await self._complete_login_process(session, user_info, email)
            
            # 4. REDIRECT MEJORADO CON VALIDACIÓN
            redirect_url = self._get_role_redirect_url()
            print(f"[DEBUG] 🎯 Redirigiendo a: {redirect_url}")
            
            return rx.redirect(redirect_url)
            
        except Exception as e:
            # Manejar intentos fallidos
            await self._handle_login_failure(str(e))
            
        finally:
            self.set_loading(False)
            print("[DEBUG] 🏁 ===== FIN DEL LOGIN =====")

    def _validate_login_form(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """Validar formulario de login con reglas específicas"""
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        
        if not email or not password:
            return {"valid": False, "message": "Email y contraseña son requeridos"}
        
        if len(email) < 5 or "@" not in email or "." not in email.split("@")[-1]:
            return {"valid": False, "message": "Formato de email inválido"}
        
        if len(password) < 6:
            return {"valid": False, "message": "Contraseña debe tener al menos 6 caracteres"}
            
        return {"valid": True, "message": ""}

    async def _authenticate_user(self, email: str, password: str):
        """Autenticar usuario con Supabase"""
        return auth.sign_in(email, password)

    async def _complete_login_process(self, session, user_info: Dict[str, Any], email: str):
        """Completar proceso de login exitoso"""
        # Actualizar estado de autenticación
        self._update_auth_state(user_info)
        
        # Guardar tokens de sesión
        if session:
            self.access_token = session.access_token
            self.refresh_token = session.refresh_token
            if hasattr(session, 'expires_at'):
                self.session_expires = datetime.fromtimestamp(session.expires_at)
            else:
                # Sesión por defecto de 1 hora
                self.session_expires = datetime.now() + timedelta(hours=1)
        
        # Limpiar formulario y mostrar éxito
        self.login_email = ""
        self.login_password = ""
        self.success_message = "¡Inicio de sesión exitoso!"
        
        print(f"[DEBUG] 📊 Usuario loggeado - Rol: {self.user_role}")

    async def _handle_login_failure(self, error_message: str):
        """Manejar fallos de login con incremento de intentos"""
        self.failed_login_attempts += 1
        
        print(f"[DEBUG] ❌ Intento fallido #{self.failed_login_attempts}: {error_message}")
        
        # Bloquear después de máximo intentos
        if self.failed_login_attempts >= self.max_failed_attempts:
            self.lockout_until = datetime.now() + timedelta(minutes=15)  # Bloqueo 15 minutos
            self.error_message = "Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos"
            print("[DEBUG] 🚫 Cuenta bloqueada por intentos excesivos")
            return
        
        # Mensaje de error específico
        remaining_attempts = self.max_failed_attempts - self.failed_login_attempts
        error_str = error_message.lower()
        
        if "invalid" in error_str or "incorrect" in error_str or "credenciales inválidas" in error_str:
            self.error_message = f"Credenciales incorrectas ({remaining_attempts} intentos restantes)"
        elif "not found" in error_str or "no encontrado" in error_str:
            self.error_message = "Usuario no encontrado en el sistema"
        elif "timeout" in error_str:
            self.error_message = "Tiempo de espera agotado. Revisa tu conexión"
        else:
            self.error_message = f"Error de conexión ({remaining_attempts} intentos restantes)"

    def _get_role_redirect_url(self) -> str:
        """Obtener URL de redirect según rol con validación"""
        role_redirects = {
            "gerente": "/boss",
            "administrador": "/admin", 
            "odontologo": "/dentist",
            "asistente": "/assistant"
        }
        
        # Validar que el rol existe y tiene redirect
        if self.user_role in role_redirects:
            return role_redirects[self.user_role]
        
        # Fallback seguro
        print(f"[WARNING] ⚠️ Rol desconocido: {self.user_role}, usando dashboard genérico")
        return "/dashboard"

    # ==========================================
    # 🚪 LOGOUT MEJORADO
    # ==========================================
    
    async def logout(self):
        """Logout público con confirmación"""
        print("[DEBUG] 🚪 Logout iniciado por usuario")
        return await self._logout_internal(show_message=True, redirect=True)

    async def logout_silent(self):
        """Logout silencioso para expiración de sesión"""
        print("[DEBUG] 🔕 Logout silencioso por expiración")
        return await self._logout_internal(show_message=False, redirect=True)

    async def _logout_internal(self, show_message: bool = True, redirect: bool = True):
        """Logout interno unificado"""
        self.set_loading(True)
        
        try:
            # Cerrar sesión en Supabase
            success = auth.sign_out()
            
            if success:
                # Limpiar todo el estado
                self.clear_auth_state()
                
                # Mensaje de confirmación
                if show_message:
                    self.success_message = "Sesión cerrada correctamente"
                
                print("[DEBUG] ✅ Logout exitoso")
                
                # Redirect condicional
                if redirect:
                    return rx.redirect("/login")
            else:
                if show_message:
                    self.error_message = "Error al cerrar sesión"
                
        except Exception as e:
            print(f"[ERROR] 💥 Error en logout: {e}")
            if show_message:
                self.error_message = "Error al cerrar sesión"
            # Limpiar estado de todas formas por seguridad
            self.clear_auth_state()
            
        finally:
            self.set_loading(False)

    # ==========================================
    # 🔍 VALIDACIONES DE SESIÓN MEJORADAS
    # ==========================================
    @rx.var
    def is_session_valid(self) -> bool:
        """
        ✅ VALIDACIÓN MEJORADA: Verificar si la sesión sigue siendo válida
        """
        if not self.is_authenticated:
            return False
        
        # Si no hay token, la sesión es inválida
        if not self.access_token:
            return False
        
        # Verificar expiración
        if self.session_expires:
            try:
                if isinstance(self.session_expires, str):
                    expiry_time = datetime.fromisoformat(self.session_expires.replace('Z', '+00:00'))
                else:
                    expiry_time = self.session_expires
                
                # Sesión válida si no ha expirado
                is_valid = datetime.now() < expiry_time
                
                if not is_valid:
                    print(f"[DEBUG] ⏰ Sesión expirada: {expiry_time}")
                
                return is_valid
                
            except Exception as e:
                print(f"[DEBUG] ⚠️ Error parseando fecha de expiración: {e}")
                return True  # Asumir válida si hay error
        
        return True

    def is_locked_out(self) -> bool:
        """Verificar si la cuenta está bloqueada por intentos fallidos"""
        if not self.lockout_until:
            return False
            
        return datetime.now() < self.lockout_until

    def get_lockout_remaining_minutes(self) -> int:
        """Obtener minutos restantes de bloqueo"""
        if not self.is_locked_out():
            return 0
            
        return max(0, (self.lockout_until - datetime.now()).seconds // 60)

    # ==========================================
    # 🔐 MÉTODOS DE PERMISOS (Extendidos)
    # ==========================================
    
    def check_permission(self, module: str, action: str) -> bool:
        """
        Verificar permiso específico con logging mejorado
        """
        if not self.is_authenticated:
            print(f"[DEBUG] ❌ Permiso denegado - No autenticado: {module}.{action}")
            return False
        
        if not self.is_session_valid:
            print(f"[DEBUG] ⏰ Permiso denegado - Sesión expirada: {module}.{action}")
            return False
        
        module_permissions = self.user_permissions.get(module, [])
        has_permission = action in module_permissions
        
        if has_permission:
            print(f"[DEBUG] ✅ Permiso otorgado: {self.user_role} -> {module}.{action}")
        else:
            print(f"[DEBUG] ❌ Permiso denegado: {self.user_role} -> {module}.{action}")
        
        return has_permission
    
    def require_auth(self):
        """Requerir autenticación con validación de sesión"""
        if not self.is_authenticated or not self.is_session_valid:
            return rx.redirect("/login")
    
    def require_role(self, *allowed_roles):
        """Requerir rol específico con validaciones"""
        if not self.is_authenticated:
            return rx.redirect("/login")
            
        if not self.is_session_valid:
            return rx.redirect("/login")
        
        if self.user_role not in allowed_roles:
            return rx.redirect("/unauthorized")

    # ==========================================
    # 🧹 MÉTODOS DE LIMPIEZA Y UTILIDAD
    # ==========================================
    
    def clear_messages(self):
        """Limpiar todos los mensajes"""
        self.error_message = ""
        self.success_message = ""

    def set_loading(self, loading: bool):
        """Establecer estado de carga"""
        self.is_loading = loading

    def clear_auth_state(self):
        """Limpiar completamente el estado de autenticación"""
        print("[DEBUG] 🧹 Limpiando estado de autenticación completo")
        
        self.current_user = None
        self.is_authenticated = False
        self.user_role = ""
        self.user_permissions = {}
        self.user_profile = None
        self.personal_info = None
        self.access_token = ""
        self.refresh_token = ""
        self.session_expires = None
        self.session_last_check = None
    
    # ==========================================
    # 📊 PROPIEDADES COMPUTADAS MEJORADAS
    # ==========================================
    
    @property
    def user_display_name(self) -> str:
        """Nombre para mostrar del usuario con fallbacks"""
        if not self.current_user:
            return "Usuario"
        
        # Intentar nombre completo desde personal
        if self.current_user.get("nombre_completo"):
            return self.current_user["nombre_completo"]
        
        # Fallback al email sin dominio
        email = self.current_user.get("email", "Usuario")
        return email.split("@")[0].title()
    
    @property
    def user_avatar(self) -> str:
        """URL del avatar con fallback"""
        if self.current_user and self.current_user.get("avatar_url"):
            return self.current_user["avatar_url"]
        return "/default-avatar.png"

    @property 
    def session_status(self) -> str:
        """Estado de la sesión en texto"""
        if not self.is_authenticated:
            return "No autenticado"
        
        if not self.is_session_valid:
            return "Sesión expirada"
        
        if self.session_expires:
            remaining = (self.session_expires - datetime.now()).seconds // 60
            return f"Sesión válida ({remaining} min restantes)"
        
        return "Sesión válida"

    @property
    def security_status(self) -> Dict[str, Any]:
        """Estado de seguridad completo"""
        return {
            "authenticated": self.is_authenticated,
            "session_valid": self.is_session_valid,
            "locked_out": self.is_locked_out(),
            "failed_attempts": self.failed_login_attempts,
            "session_expires": self.session_expires,
            "last_check": self.session_last_check
        }