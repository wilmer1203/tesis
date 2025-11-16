"""
Modelos de datos para el módulo de PERSONAL
Centraliza todos los modelos relacionados con gestión de empleados y usuarios
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class UsuarioModel(rx.Base):
    """Modelo para datos de usuario del sistema"""
    id: Optional[str] = ""
    email: str = ""
    activo: bool = True
    rol_id: str = ""
    auth_user_id: Optional[str] = ""
    fecha_creacion: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsuarioModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            email=str(data.get("email", "")),
            activo=bool(data.get("activo", True)),
            rol_id=str(data.get("rol_id", "")),
            auth_user_id=str(data.get("auth_user_id", "") if data.get("auth_user_id") else ""),
            fecha_creacion=str(data.get("fecha_creacion", ""))
        )


class PersonalModel(rx.Base):
    """Modelo para datos de personal - ALINEADO CON ESQUEMA BD v4.1"""
    id: Optional[str] = ""
    usuario_id: Optional[str] = ""  # Relación con usuarios
    numero_documento: str = ""
    tipo_personal: str = ""
    especialidad: Optional[str] = ""
    estado_laboral: str = "activo"
    numero_licencia: Optional[str] = ""
    celular: str = ""  # REQUERIDO según esquema
    direccion: Optional[str] = ""
    fecha_contratacion: Optional[str] = ""
    fecha_nacimiento: Optional[str] = ""
    tipo_documento: str = "CI"  # CORREGIDO: CI para Venezuela
    
    # ✅ CAMPOS DE TIMESTAMP (FALTABAN)
    fecha_creacion: Optional[str] = ""
    fecha_actualizacion: Optional[str] = ""
    
    # Información de rol
    rol_nombre: Optional[str] = ""
    rol_id: Optional[str] = ""
    
    # ✅ CAMPOS DE NOMBRES SEPARADOS
    primer_nombre: str = ""
    segundo_nombre: Optional[str] = ""
    primer_apellido: str = ""
    segundo_apellido: Optional[str] = ""
    
    # Relaciones
    usuario: UsuarioModel = UsuarioModel()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalModel":
        """Crear instancia desde diccionario - VERSIÓN OPTIMIZADA"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # ✅ CAMPOS SEPARADOS DESDE LA VISTA
        primer_nombre = str(data.get("primer_nombre", ""))
        segundo_nombre = str(data.get("segundo_nombre", ""))
        primer_apellido = str(data.get("primer_apellido", ""))
        segundo_apellido = str(data.get("segundo_apellido", ""))
        
        # ✅ CONSTRUIR USUARIO desde datos aplanados (como vienen de la vista)
        usuario = UsuarioModel(
            id=str(data.get("usuario_id", "")),
            email=str(data.get("email", "")),
            activo=bool(data.get("usuario_activo", True))
        )
        
        return cls(
            id=str(data.get("id", "")),
            usuario_id=str(data.get("usuario_id", "") if data.get("usuario_id") else ""),
            numero_documento=str(data.get("numero_documento", "")),
            tipo_personal=str(data.get("tipo_personal", "")),
            especialidad=str(data.get("especialidad", "") if data.get("especialidad") else ""),
            estado_laboral=str(data.get("estado_laboral", "activo")),
            numero_licencia=str(data.get("numero_licencia", "") if data.get("numero_licencia") else ""),
            celular=str(data.get("celular", "")),
            direccion=str(data.get("direccion", "") if data.get("direccion") else ""),
            fecha_contratacion=str(data.get("fecha_contratacion", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "") if data.get("fecha_nacimiento") else ""),
            tipo_documento=str(data.get("tipo_documento", "CI")),

            # ✅ TIMESTAMPS
            fecha_creacion=str(data.get("fecha_creacion", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            
            # ✅ CAMPOS SEPARADOS
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            
            # ✅ INFORMACIÓN DE ROL
            rol_nombre=str(data.get("rol_nombre", "")),
            rol_id=str(data.get("rol_id", "")),
            
            usuario=usuario
        )

    @property
    def nombre_completo(self) -> str:
        """Propiedad para mostrar el nombre completo"""
        nombres = []
        if self.primer_nombre:
            nombres.append(self.primer_nombre)
        if self.segundo_nombre:
            nombres.append(self.segundo_nombre)
        if self.primer_apellido:
            nombres.append(self.primer_apellido)
        if self.segundo_apellido:
            nombres.append(self.segundo_apellido)
        
        return " ".join(nombres) if nombres else self.usuario.nombre_completo
    
    
    @property  
    def rol_nombre_computed(self) -> str:
        """Mapea tipo_personal a rol_nombre si rol_nombre está vacío"""
        if self.rol_nombre:
            return self.rol_nombre
        
        # Mapeo de tipo_personal a rol_nombre
        mapping = {
            "Gerente": "gerente",
            "Administrador": "administrador", 
            "Odontólogo": "odontologo",
            "Asistente": "asistente"
        }
        return mapping.get(self.tipo_personal, "administrador")

    @property
    def edad_calculada(self) -> int:
        """Calcular edad desde fecha de nacimiento"""
        if not self.fecha_nacimiento:
            return 0

        try:
            from datetime import date
            # Convertir string fecha a objeto date si es necesario
            if isinstance(self.fecha_nacimiento, str) and self.fecha_nacimiento:
                from datetime import datetime
                fecha_nac = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d").date()
            else:
                fecha_nac = self.fecha_nacimiento

            if not fecha_nac:
                return 0

            hoy = date.today()
            edad = hoy.year - fecha_nac.year
            if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
                edad -= 1
            return max(0, edad)
        except:
            return 0

    @property
    def tipo_display(self) -> str:
        """Tipo de personal formateado"""
        tipos_map = {
            "Odontólogo": "🦷 Odontólogo",
            "Asistente": "👩‍⚕️ Asistente",
            "Administrador": "👨‍💼 Administrador",
            "Gerente": "👔 Gerente"
        }
        return tipos_map.get(self.tipo_personal, self.tipo_personal)
    
    @property
    def fecha_contratacion_display(self) -> str:
        """Fecha de contratación formateada"""
        try:
            if self.fecha_contratacion:
                fecha_obj = datetime.fromisoformat(str(self.fecha_contratacion))
                return fecha_obj.strftime("%d/%m/%Y")
            return "Sin fecha"
        except:
            return str(self.fecha_contratacion)
    
    @property
    def es_odontologo(self) -> bool:
        """Indica si es odontólogo"""
        return self.tipo_personal == "Odontólogo"

    @property
    def puede_atender_pacientes(self) -> bool:
        """Indica si puede atender pacientes directamente"""
        return (self.tipo_personal in ["Odontólogo"] and
                self.estado_laboral == "activo")
    
    @property
    def tipo_documento_display(self) -> str:
        """Tipo documento formateado"""
        tipos_map = {
            "CI": "C.I.",
            "Pasaporte": "Pasaporte"
        }
        return tipos_map.get(self.tipo_documento, self.tipo_documento)


class PersonalStatsModel(rx.Base):
    """Modelo para estadísticas de personal"""
    total: int = 0
    activos: int = 0
    odontologos: int = 0
    administradores: int = 0
    asistentes: int = 0
    gerentes: int = 0

    # Por estado
    en_vacaciones: int = 0
    en_licencia: int = 0
    inactivos: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalStatsModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            total=int(data.get("total", 0)),
            activos=int(data.get("activos", 0)),
            odontologos=int(data.get("odontologos", 0)),
            administradores=int(data.get("administradores", 0)),
            asistentes=int(data.get("asistentes", 0)),
            gerentes=int(data.get("gerentes", 0)),
            en_vacaciones=int(data.get("en_vacaciones", 0)),
            en_licencia=int(data.get("en_licencia", 0)),
            inactivos=int(data.get("inactivos", 0))
        )



# ==========================================
# 📝 FORMULARIOS DE PERSONAL
# ==========================================

class PersonalFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE PERSONAL
    
    Reemplaza: form_data: Dict[str, str] en personal_service
    """
    
    # Datos personales
    primer_nombre: str = ""
    segundo_nombre: str = ""
    primer_apellido: str = ""
    segundo_apellido: str = ""
    
    # Identificación
    numero_documento: str = ""
    tipo_documento: str = "CI"  
    celular: str = ""
    codigo_pais_celular: str = "+58 (VE)"  # Código de país para celular
    direccion: str = ""
    
    # Datos profesionales
    tipo_personal: str = "asistente"  # odontologo, asistente, administrador
    especialidad: str = ""
    numero_colegiatura: str = ""
    fecha_ingreso: str = ""  # YYYY-MM-DD
    
    # Información laboral
    estado_laboral: str = "activo"  # activo, inactivo, vacaciones, licencia

    # Usuario del sistema
    crear_usuario: bool = True
    usuario_email: str = ""
    usuario_password: str = ""
    rol_sistema: str = "asistente"  # gerente, administrador, odontologo, asistente
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos"""
        errors = {}
        
        if not self.primer_nombre.strip():
            errors.setdefault("primer_nombre", []).append("Primer nombre es requerido")
        
        if not self.primer_apellido.strip():
            errors.setdefault("primer_apellido", []).append("Primer apellido es requerido")
        
        if not self.numero_documento.strip():
            errors.setdefault("numero_documento", []).append("Número de documento es requerido")
        
        if self.crear_usuario:
            if not self.usuario_email.strip():
                errors.setdefault("usuario_email", []).append("Email de usuario es requerido")
            
            if not self.usuario_password.strip():
                errors.setdefault("usuario_password", []).append("Password es requerida")
        
        return errors
    
    @property
    def nombre_completo(self) -> str:
        """Nombre completo formateado"""
        nombres = [self.primer_nombre, self.segundo_nombre]
        apellidos = [self.primer_apellido, self.segundo_apellido]
        
        nombres_str = " ".join(n for n in nombres if n.strip())
        apellidos_str = " ".join(a for a in apellidos if a.strip())
        
        return f"{nombres_str} {apellidos_str}".strip()
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad"""
        return {
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "primer_apellido": self.primer_apellido,
            "segundo_apellido": self.segundo_apellido,
            "numero_documento": self.numero_documento,
            "tipo_documento": self.tipo_documento,
            "celular": self.celular,  # ✅ CAMBIO: telefono → celular
            "direccion": self.direccion,
            "tipo_personal": self.tipo_personal,
            "especialidad": self.especialidad,
            "numero_colegiatura": self.numero_colegiatura,
            "fecha_ingreso": self.fecha_ingreso,
            "estado_laboral": self.estado_laboral,

            "crear_usuario": str(self.crear_usuario),
            "email": self.usuario_email,  # ✅ MAPEO: usuario_email → email para servicio
            "password": self.usuario_password,  # ✅ MAPEO: usuario_password → password para servicio
            "rol_sistema": self.rol_sistema,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalFormModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            primer_nombre=str(data.get("primer_nombre", "")),
            segundo_nombre=str(data.get("segundo_nombre", "")),
            primer_apellido=str(data.get("primer_apellido", "")),
            segundo_apellido=str(data.get("segundo_apellido", "")),
            numero_documento=str(data.get("numero_documento", "")),
            tipo_documento=str(data.get("tipo_documento", "CI")),
            celular=str(data.get("celular", "")),
            codigo_pais_celular=str(data.get("codigo_pais_celular", "+58 (VE)")),
            direccion=str(data.get("direccion", "")),
            tipo_personal=str(data.get("tipo_personal", "asistente")),
            especialidad=str(data.get("especialidad", "")),
            numero_colegiatura=str(data.get("numero_colegiatura", "")),
            fecha_ingreso=str(data.get("fecha_ingreso", "")),
            estado_laboral=str(data.get("estado_laboral", "activo")),

            crear_usuario=data.get("crear_usuario", True) if isinstance(data.get("crear_usuario"), bool) else str(data.get("crear_usuario", "True")).lower() == "true",
            usuario_email=str(data.get("usuario_email", "")),
            usuario_password=str(data.get("usuario_password", "")),
            rol_sistema=str(data.get("rol_sistema", "asistente"))
        )