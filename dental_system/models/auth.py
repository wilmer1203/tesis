# =====================================================
# MODELOS DE DATOS PARA AUTENTICACIÓN
# =====================================================

from dataclasses import dataclass
from typing import Optional, Dict, List, Any
from datetime import datetime

@dataclass
class UserRole:
    """Modelo para roles de usuario"""
    id: str
    nombre: str
    descripcion: str
    permisos: Dict[str, List[str]]
    activo: bool

@dataclass
class UserProfile:
    """Modelo para perfil de usuario completo"""
    id: str
    auth_user_id: str
    email: str
    nombre_completo: str
    telefono: Optional[str]
    rol: UserRole
    activo: bool
    fecha_creacion: datetime
    ultimo_acceso: Optional[datetime]
    configuraciones: Dict[str, Any]
    avatar_url: Optional[str]

@dataclass
class PersonalInfo:
    """Información adicional del personal"""
    id: str
    usuario_id: str
    numero_documento: str
    tipo_documento: str
    fecha_nacimiento: Optional[datetime]
    direccion: Optional[str]
    celular: str
    tipo_personal: str
    especialidad: Optional[str]
    numero_licencia: Optional[str]
    estado_laboral: str

@dataclass
class AuthSession:
    """Información de sesión de usuario"""
    access_token: str
    refresh_token: str
    expires_at: datetime
    user_id: str
