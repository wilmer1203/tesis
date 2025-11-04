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
    nombre_completo: str = ""
    celular: Optional[str] = ""
    activo: bool = True
    rol_id: str = ""
    rol_nombre: str = ""
    auth_user_id: Optional[str] = ""
    avatar_url: Optional[str] = ""
    ultimo_acceso: Optional[str] = ""
    fecha_creacion: str = ""
    configuraciones: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsuarioModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            email=str(data.get("email", "")),
            nombre_completo=str(data.get("nombre_completo", "")),
            celular=str(data.get("celular", "")),
            activo=bool(data.get("activo", True)),
            rol_id=str(data.get("rol_id", "")),
            rol_nombre=str(data.get("rol_nombre", "")),
            auth_user_id=str(data.get("auth_user_id", "") if data.get("auth_user_id") else ""),
            avatar_url=str(data.get("avatar_url", "") if data.get("avatar_url") else ""),
            ultimo_acceso=str(data.get("ultimo_acceso", "") if data.get("ultimo_acceso") else ""),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            configuraciones=data.get("configuraciones", {}),
            metadata=data.get("metadata", {})
        )


class RolModel(rx.Base):
    """Modelo para datos de roles del sistema"""
    id: Optional[str] = ""
    nombre: str = ""
    descripcion: Optional[str] = ""
    permisos: Dict[str, Any] = {}
    activo: bool = True
    fecha_creacion: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RolModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            nombre=str(data.get("nombre", "")),
            descripcion=str(data.get("descripcion", "") if data.get("descripcion") else ""),
            permisos=data.get("permisos", {}),
            activo=bool(data.get("activo", True)),
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
    salario: Optional[float] = None
    fecha_contratacion: Optional[str] = ""
    fecha_nacimiento: Optional[str] = ""
    tipo_documento: str = "CI"  # CORREGIDO: CI para Venezuela
    observaciones: Optional[str] = ""
    
    # ✅ CAMPOS CRÍTICOS PARA SISTEMA DE COLAS (FALTABAN)
    acepta_pacientes_nuevos: bool = True
    orden_preferencia: int = 1
    
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
            salario=data.get("salario") if isinstance(data.get("salario"), (int, float)) else None,
            fecha_contratacion=str(data.get("fecha_contratacion", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "") if data.get("fecha_nacimiento") else ""),
            tipo_documento=str(data.get("tipo_documento", "CI")),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            
            # ✅ CAMPOS CRÍTICOS SISTEMA DE COLAS
            acepta_pacientes_nuevos=bool(data.get("acepta_pacientes_nuevos", True)),
            orden_preferencia=int(data.get("orden_preferencia", 1)),
            
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
    def nombre_completo_display(self) -> str:
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
    def nombre_completo(self) -> str:
        """Alias para compatibilidad - mismo que nombre_completo_display"""
        return self.nombre_completo_display
    
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
    def salario_display(self) -> str:
        """Salario formateado para mostrar"""
        if self.salario:
            return f"${self.salario:,.0f}"
        return "No asignado"
    
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
                self.estado_laboral == "activo" and 
                self.acepta_pacientes_nuevos)
    
    @property
    def disponible_para_cola(self) -> bool:
        """Indica si está disponible para recibir pacientes en cola"""
        return self.puede_atender_pacientes
    
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
    
    # Estadísticas salariales
    salario_promedio: float = 0.0
    salario_total_mensual: float = 0.0
    
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
            inactivos=int(data.get("inactivos", 0)),
            salario_promedio=float(data.get("salario_promedio", 0.0)),
            salario_total_mensual=float(data.get("salario_total_mensual", 0.0))
        )


class HorarioTrabajoModel(rx.Base):
    """Modelo para horarios de trabajo del personal"""
    personal_id: str = ""
    dia_semana: str = ""  # lunes, martes, etc.
    hora_entrada: str = "08:00"
    hora_salida: str = "17:00"
    hora_almuerzo_inicio: Optional[str] = "12:00"
    hora_almuerzo_fin: Optional[str] = "13:00"
    activo: bool = True
    
    @property
    def horas_trabajadas_dia(self) -> float:
        """Calcula las horas trabajadas en el día"""
        try:
            from datetime import datetime, timedelta
            
            entrada = datetime.strptime(self.hora_entrada, "%H:%M")
            salida = datetime.strptime(self.hora_salida, "%H:%M")
            
            total_horas = (salida - entrada).total_seconds() / 3600
            
            # Restar hora de almuerzo si está definida
            if self.hora_almuerzo_inicio and self.hora_almuerzo_fin:
                almuerzo_inicio = datetime.strptime(self.hora_almuerzo_inicio, "%H:%M")
                almuerzo_fin = datetime.strptime(self.hora_almuerzo_fin, "%H:%M")
                horas_almuerzo = (almuerzo_fin - almuerzo_inicio).total_seconds() / 3600
                total_horas -= horas_almuerzo
            
            return max(0, total_horas)
        except:
            return 8.0  # Default


class EspecialidadModel(rx.Base):
    """Modelo para especialidades odontológicas"""
    id: str = ""
    nombre: str = ""
    descripcion: str = ""
    requiere_licencia_especial: bool = False
    codigo_especialidad: str = ""
    activa: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EspecialidadModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            nombre=str(data.get("nombre", "")),
            descripcion=str(data.get("descripcion", "")),
            requiere_licencia_especial=bool(data.get("requiere_licencia_especial", False)),
            codigo_especialidad=str(data.get("codigo_especialidad", "")),
            activa=bool(data.get("activa", True))
        )


class PermisoModel(rx.Base):
    """Modelo para permisos granulares del sistema"""
    modulo: str = ""          # pacientes, consultas, personal, etc.
    acciones: List[str] = []  # crear, leer, actualizar, eliminar
    descripcion: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PermisoModel":
        """Crear instancia desde diccionario de permisos"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            modulo=str(data.get("modulo", "")),
            acciones=data.get("acciones", []),
            descripcion=str(data.get("descripcion", ""))
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
    celular: str = ""
    email: str = ""
    direccion: str = ""
    
    # Datos profesionales
    tipo_personal: str = "asistente"  # odontologo, asistente, administrador
    especialidad: str = ""
    numero_colegiatura: str = ""
    fecha_ingreso: str = ""  # YYYY-MM-DD
    
    # Información laboral
    salario: str = "0"
    estado_laboral: str = "activo"  # activo, inactivo, vacaciones, licencia
    
    # ✅ CAMPOS CRÍTICOS PARA SISTEMA DE COLAS
    acepta_pacientes_nuevos: bool = True
    orden_preferencia: int = 1
    
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
            "celular": self.celular,  # ✅ CAMBIO: telefono → celular
            "email_personal": self.email,  # ✅ SEPARAR: email personal del sistema
            "direccion": self.direccion,
            "tipo_personal": self.tipo_personal,
            "especialidad": self.especialidad,
            "numero_colegiatura": self.numero_colegiatura,
            "fecha_ingreso": self.fecha_ingreso,
            "salario": self.salario,
            "estado_laboral": self.estado_laboral,
            
            # ✅ CAMPOS CRÍTICOS SISTEMA DE COLAS
            "acepta_pacientes_nuevos": self.acepta_pacientes_nuevos,
            "orden_preferencia": self.orden_preferencia,
            
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
            celular=str(data.get("celular", "")),
            email=str(data.get("email", "")),
            direccion=str(data.get("direccion", "")),
            tipo_personal=str(data.get("tipo_personal", "asistente")),
            especialidad=str(data.get("especialidad", "")),
            numero_colegiatura=str(data.get("numero_colegiatura", "")),
            fecha_ingreso=str(data.get("fecha_ingreso", "")),
            salario=str(data.get("salario", "0")),
            estado_laboral=str(data.get("estado_laboral", "activo")),
            
            # ✅ CAMPOS CRÍTICOS SISTEMA DE COLAS
            acepta_pacientes_nuevos=bool(data.get("acepta_pacientes_nuevos", True)),
            orden_preferencia=int(data.get("orden_preferencia", 1)),
            crear_usuario=data.get("crear_usuario", True) if isinstance(data.get("crear_usuario"), bool) else str(data.get("crear_usuario", "True")).lower() == "true",
            usuario_email=str(data.get("usuario_email", "")),
            usuario_password=str(data.get("usuario_password", "")),
            rol_sistema=str(data.get("rol_sistema", "asistente"))
        )