"""
Estado base común para toda la aplicación
Extiende el AuthState existente con funcionalidades adicionales
"""

import reflex as rx
from typing import Dict, Any, Optional
from datetime import datetime
from .auth_state import AuthState

class BaseState(AuthState):
    """Estado base que extiende AuthState con funcionalidades adicionales"""
    
    # ==========================================
    # CONFIGURACIÓN DE LA APLICACIÓN
    # ==========================================
    app_name: str = "DentalSys"
    app_version: str = "1.0.0"
    clinic_name: str = "Clínica Dental Odontomara"
    clinic_address: str = "Puerto La Cruz, Anzoátegui"
    clinic_phone: str = "+58 281-1234567"
    
    # ==========================================
    # ESTADO DE LA UI GLOBAL
    # ==========================================
    global_message: str = ""
    global_message_type: str = ""  # "success", "error", "warning", "info"
    
    # ==========================================
    # MÉTODOS DE MENSAJES GLOBALES
    # ==========================================
    def show_success(self, message: str):
        """Mostrar mensaje de éxito"""
        self.global_message = message
        self.global_message_type = "success"
        self.success_message = message  # Mantener compatibilidad con AuthState
    
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        self.global_message = message
        self.global_message_type = "error"
        self.error_message = message  # Mantener compatibilidad con AuthState
    
    def show_warning(self, message: str):
        """Mostrar mensaje de advertencia"""
        self.global_message = message
        self.global_message_type = "warning"
    
    def show_info(self, message: str):
        """Mostrar mensaje informativo"""
        self.global_message = message
        self.global_message_type = "info"
    
    def clear_global_message(self):
        """Limpiar mensaje global"""
        self.global_message = ""
        self.global_message_type = ""
        self.clear_messages()  # Limpiar también mensajes de AuthState
    
    # ==========================================
    # MÉTODOS DE PERMISOS (Extienden AuthState)
    # ==========================================
    def can_create(self, module: str) -> bool:
        """Verificar permiso de creación"""
        return self.check_permission(module, "crear")
    
    def can_read(self, module: str) -> bool:
        """Verificar permiso de lectura"""
        return self.check_permission(module, "leer")
    
    def can_update(self, module: str) -> bool:
        """Verificar permiso de actualización"""
        return self.check_permission(module, "actualizar")
    
    def can_delete(self, module: str) -> bool:
        """Verificar permiso de eliminación"""
        return self.check_permission(module, "eliminar")
    
    # ==========================================
    # MÉTODOS DE NAVEGACIÓN
    # ==========================================
    def redirect_to_dashboard(self):
        """Redirigir al dashboard según el rol del usuario"""
        if not self.is_authenticated:
            return rx.redirect("/login")
        
        role_dashboards = {
            "gerente": "/boss",
            "administrador": "/admin", 
            "odontologo": "/dentist",
            "asistente": "/assistant"
        }
        
        dashboard_url = role_dashboards.get(self.user_role, "/dashboard")
        return rx.redirect(dashboard_url)
    
    # ==========================================
    # MÉTODOS DE VALIDACIÓN DE SESIÓN
    # ==========================================
    def is_session_valid(self) -> bool:
        """Verificar si la sesión sigue siendo válida"""
        if not self.is_authenticated:
            return False
        
        # Si hay fecha de expiración de sesión, verificarla
        if self.session_expires:
            try:
                if isinstance(self.session_expires, str):
                    expiry_time = datetime.fromisoformat(self.session_expires.replace('Z', '+00:00'))
                else:
                    expiry_time = self.session_expires
                
                return datetime.now() < expiry_time
            except:
                return True  # Si hay error parseando fecha, asumir válida
        
        return True  # Si no hay fecha de expiración, asumir válida
    
    # ==========================================
    # MÉTODOS DE UTILIDAD
    # ==========================================
    def format_date(self, date_string: str, format: str = "%d/%m/%Y") -> str:
        """Formatear fecha para mostrar"""
        try:
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date_obj.strftime(format)
        except:
            return date_string
    
    def format_currency(self, amount: float) -> str:
        """Formatear cantidad como moneda"""
        return f"${amount:,.0f}"
    
    def get_user_initials(self) -> str:
        """Obtener iniciales del usuario"""
        if not self.user_profile or not self.user_profile.get("nombre_completo"):
            return "U"
        
        name = self.user_profile["nombre_completo"]
        words = name.split()
        if len(words) >= 2:
            return f"{words[0][0]}{words[1][0]}".upper()
        elif len(words) == 1:
            return words[0][:2].upper()
        else:
            return "U"
    
    def get_greeting(self) -> str:
        """Obtener saludo según la hora del día"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            return "Buenos días"
        elif 12 <= current_hour < 18:
            return "Buenas tardes"
        else:
            return "Buenas noches"
    
    # ==========================================
    # CONFIGURACIÓN DE LA APLICACIÓN
    # ==========================================
    def get_app_config(self) -> Dict[str, str]:
        """Obtener configuración de la aplicación"""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "clinic_name": self.clinic_name,
            "clinic_address": self.clinic_address,
            "clinic_phone": self.clinic_phone
        }
