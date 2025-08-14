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
    telefono: Optional[str] = ""
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
            telefono=str(data.get("telefono", "") if data.get("telefono") else ""),
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
    """Modelo para datos de personal - OPTIMIZADO CON CAMPOS SEPARADOS"""
    id: Optional[str] = ""
    numero_documento: str = ""
    tipo_personal: str = ""
    especialidad: Optional[str] = ""
    estado_laboral: str = "activo"
    numero_licencia: Optional[str] = ""
    celular: Optional[str] = ""
    direccion: Optional[str] = ""
    salario: Optional[float] = None
    fecha_contratacion: Optional[str] = ""
    fecha_nacimiento: Optional[str] = ""
    tipo_documento: str = "CC"
    horario_trabajo: Dict[str, Any] = {}
    observaciones: Optional[str] = ""
    
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
            nombre_completo=str(data.get("nombre_completo", "")),  # ← Viene calculado de la vista
            telefono=str(data.get("telefono", "")),
            activo=bool(data.get("usuario_activo", True))
        )
        
        return cls(
            id=str(data.get("id", "")),
            numero_documento=str(data.get("numero_documento", "")),
            tipo_personal=str(data.get("tipo_personal", "")),
            especialidad=str(data.get("especialidad", "")),
            estado_laboral=str(data.get("estado_laboral", "activo")),
            numero_licencia=str(data.get("numero_licencia", "")),
            celular=str(data.get("celular", "")),
            direccion=str(data.get("direccion", "")),
            salario=data.get("salario") if isinstance(data.get("salario"), (int, float)) else None,
            fecha_contratacion=str(data.get("fecha_contratacion", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "") if data.get("fecha_nacimiento") else ""),
            tipo_documento=str(data.get("tipo_documento", "CC")),
            horario_trabajo=data.get("horario_trabajo", {}),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            
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
    def estado_display(self) -> str:
        """Estado laboral formateado para mostrar"""
        estados_map = {
            "activo": "Activo",
            "vacaciones": "En Vacaciones",
            "licencia": "En Licencia",
            "inactivo": "Inactivo"
        }
        return estados_map.get(self.estado_laboral, self.estado_laboral.capitalize())
    
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
        return self.tipo_personal in ["Odontólogo"] and self.estado_laboral == "activo"


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