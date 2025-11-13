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
