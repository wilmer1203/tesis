"""
Modelos de datos tipados para Reflex
Usando rx.Base para que Reflex pueda inferir correctamente los tipos
"""

import reflex as rx
from typing import Optional, Dict, Any
from datetime import datetime

class UsuarioModel(rx.Base):
    """Modelo para datos de usuario"""
    id: Optional[str] = ""
    email: str = ""
    nombre_completo: str = ""
    telefono: Optional[str] = ""
    activo: bool = True

class RolModel(rx.Base):
    """Modelo para datos de rol"""
    id: Optional[str] = ""
    nombre: str = ""
    descripcion: Optional[str] = ""
    permisos: Dict[str, Any] = {}


class PersonalModel(rx.Base):
    """Modelo para datos de personal - ACTUALIZADO CON CAMPOS SEPARADOS"""
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
    
    # CAMPOS DE NOMBRES SEPARADOS
    primer_nombre: str = ""
    segundo_nombre: Optional[str] = ""
    primer_apellido: str = ""
    segundo_apellido: Optional[str] = ""
    
    # Relaciones
    usuarios: UsuarioModel = UsuarioModel()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalModel":
        """Crear instancia desde diccionario - VERSIÓN PARA VISTA CORREGIDA"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # ✅ AHORA SÍ VIENEN LOS CAMPOS SEPARADOS DESDE LA VISTA
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
            
            # ✅ CAMPOS SEPARADOS (ahora SÍ vienen de la vista)
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            
            usuarios=usuario
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
        
        return " ".join(nombres) if nombres else self.usuarios.nombre_completo

class ServicioModel(rx.Base):
    """Modelo para datos de servicios"""
    id: Optional[str] = ""
    codigo: str = ""
    nombre: str = ""
    descripcion: Optional[str] = ""
    categoria: str = ""
    subcategoria: Optional[str] = ""
    duracion_estimada: str = "30 minutes"
    precio_base: float = 0.0
    precio_minimo: Optional[float] = None
    precio_maximo: Optional[float] = None
    activo: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServicioModel":
        """Crear instancia desde diccionario de Supabase"""
        return cls(
            id=data.get("id", ""),
            codigo=data.get("codigo", ""),
            nombre=data.get("nombre", ""),
            descripcion=data.get("descripcion", ""),
            categoria=data.get("categoria", ""),
            subcategoria=data.get("subcategoria", ""),
            duracion_estimada=data.get("duracion_estimada", "30 minutes"),
            precio_base=float(data.get("precio_base", 0)),
            precio_minimo=float(data.get("precio_minimo", 0)) if data.get("precio_minimo") else None,
            precio_maximo=float(data.get("precio_maximo", 0)) if data.get("precio_maximo") else None,
            activo=data.get("activo", True)
        )

class DashboardStatsModel(rx.Base):
    """Modelo para estadísticas del dashboard"""
    total_pacientes: int = 0
    consultas_hoy: int = 0
    ingresos_mes: float = 0.0
    personal_activo: int = 0
    servicios_activos: int = 0
    pagos_pendientes: int = 0

# class PacientesStatsModel(rx.Base):
#     """Modelo para estadísticas de pacientes"""
#     total: int = 0
#     nuevos_mes: int = 0
#     activos: int = 0

class PagosStatsModel(rx.Base):
    """Modelo para estadísticas de pagos"""
    total_mes: float = 0.0
    pendientes: float = 0.0
    completados: float = 0.0
