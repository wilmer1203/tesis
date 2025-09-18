"""
🎨 MODELOS UI - NOTIFICACIONES Y TOASTS
==========================================

Modelos específicos para sistema de notificaciones y toasts flotantes
"""

import reflex as rx
from typing import Optional, Dict, Any
from datetime import datetime

# ==========================================
# MODELOS DE TOASTS Y NOTIFICACIONES
# ==========================================

class ToastModel(rx.Base):
    """🍞 Modelo para toast notifications"""
    id: str = ""
    message: str = ""
    toast_type: str = "info"  # success, error, warning, info
    duration: int = 4000  # ms
    timestamp: str = ""
    auto_dismiss: bool = True
    
    @classmethod
    def success(cls, message: str, duration: int = 4000) -> "ToastModel":
        """Crear toast de éxito"""
        return cls(
            id=f"toast_{datetime.now().timestamp()}",
            message=message,
            toast_type="success",
            duration=duration,
            timestamp=datetime.now().isoformat(),
            auto_dismiss=True
        )
    
    @classmethod
    def error(cls, message: str, duration: int = 6000) -> "ToastModel":
        """Crear toast de error"""
        return cls(
            id=f"toast_{datetime.now().timestamp()}",
            message=message,
            toast_type="error",
            duration=duration,
            timestamp=datetime.now().isoformat(),
            auto_dismiss=True
        )
    
    @classmethod
    def warning(cls, message: str, duration: int = 5000) -> "ToastModel":
        """Crear toast de advertencia"""
        return cls(
            id=f"toast_{datetime.now().timestamp()}",
            message=message,
            toast_type="warning",
            duration=duration,
            timestamp=datetime.now().isoformat(),
            auto_dismiss=True
        )
    
    @classmethod
    def info(cls, message: str, duration: int = 4000) -> "ToastModel":
        """Crear toast informativo"""
        return cls(
            id=f"toast_{datetime.now().timestamp()}",
            message=message,
            toast_type="info", 
            duration=duration,
            timestamp=datetime.now().isoformat(),
            auto_dismiss=True
        )

class NotificationModel(rx.Base):
    """📢 Modelo para notificaciones persistentes"""
    id: str = ""
    title: str = ""
    message: str = ""
    notification_type: str = "info"  # success, error, warning, info
    timestamp: str = ""
    is_read: bool = False
    action_url: str = ""
    action_text: str = ""
    priority: str = "normal"  # high, normal, low
    
    @property
    def time_ago(self) -> str:
        """Tiempo transcurrido desde la notificación"""
        try:
            notif_time = datetime.fromisoformat(self.timestamp)
            now = datetime.now()
            diff = now - notif_time
            
            if diff.days > 0:
                return f"hace {diff.days} días"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"hace {hours} horas"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"hace {minutes} minutos"
            else:
                return "ahora"
        except:
            return "tiempo desconocido"
    
    @property
    def icon_name(self) -> str:
        """Icono según tipo de notificación"""
        icons_map = {
            "success": "circle_check",
            "error": "circle_alert", 
            "warning": "triangle_alert",
            "info": "info",
            "medical": "stethoscope",
            "patient": "user",
            "payment": "credit_card"
        }
        return icons_map.get(self.notification_type, "info")