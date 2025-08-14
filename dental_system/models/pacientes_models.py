"""
Modelos de datos para el módulo de PACIENTES
Centraliza todos los modelos relacionados con gestión de pacientes
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class PacienteModel(rx.Base):
    """Modelo para datos de pacientes - OPTIMIZADO para nombres y teléfonos separados"""
    id: Optional[str] = ""
    numero_historia: str = ""
    
    # ✅ NOMBRES SEPARADOS (según estructura DB actualizada)
    primer_nombre: str = ""
    segundo_nombre: Optional[str] = ""
    primer_apellido: str = ""
    segundo_apellido: Optional[str] = ""
    
    # Documentación
    numero_documento: str = ""
    tipo_documento: str = "CC"
    fecha_nacimiento: Optional[str] = ""
    edad: Optional[int] = None
    genero: Optional[str] = ""
    
    # ✅ TELÉFONOS SEPARADOS (según estructura DB actualizada)
    telefono_1: Optional[str] = ""
    telefono_2: Optional[str] = ""
    
    email: Optional[str] = ""
    direccion: Optional[str] = ""
    ciudad: Optional[str] = ""
    departamento: Optional[str] = ""
    ocupacion: Optional[str] = ""
    estado_civil: Optional[str] = ""
    
    # Información médica
    alergias: List[str] = []
    medicamentos_actuales: List[str] = []
    condiciones_medicas: List[str] = []
    antecedentes_familiares: List[str] = []
    observaciones: Optional[str] = ""
    
    # Control del sistema
    fecha_registro: str = ""
    fecha_actualizacion: str = ""
    registrado_por: Optional[str] = ""
    activo: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PacienteModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            numero_historia=str(data.get("numero_historia", "")),
            
            # ✅ NOMBRES SEPARADOS
            primer_nombre=str(data.get("primer_nombre", "")),
            segundo_nombre=str(data.get("segundo_nombre", "") if data.get("segundo_nombre") else ""),
            primer_apellido=str(data.get("primer_apellido", "")),
            segundo_apellido=str(data.get("segundo_apellido", "") if data.get("segundo_apellido") else ""),
            
            numero_documento=str(data.get("numero_documento", "")),
            tipo_documento=str(data.get("tipo_documento", "CC")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "") if data.get("fecha_nacimiento") else ""),
            edad=data.get("edad") if isinstance(data.get("edad"), int) else None,
            genero=str(data.get("genero", "") if data.get("genero") else ""),
            
            # ✅ TELÉFONOS SEPARADOS
            telefono_1=str(data.get("telefono_1", "") if data.get("telefono_1") else ""),
            telefono_2=str(data.get("telefono_2", "") if data.get("telefono_2") else ""),
            
            email=str(data.get("email", "") if data.get("email") else ""),
            direccion=str(data.get("direccion", "") if data.get("direccion") else ""),
            ciudad=str(data.get("ciudad", "") if data.get("ciudad") else ""),
            departamento=str(data.get("departamento", "") if data.get("departamento") else ""),
            ocupacion=str(data.get("ocupacion", "") if data.get("ocupacion") else ""),
            estado_civil=str(data.get("estado_civil", "") if data.get("estado_civil") else ""),
            
            # Información médica (arrays)
            alergias=data.get("alergias", []) if isinstance(data.get("alergias"), list) else [],
            medicamentos_actuales=data.get("medicamentos_actuales", []) if isinstance(data.get("medicamentos_actuales"), list) else [],
            condiciones_medicas=data.get("condiciones_medicas", []) if isinstance(data.get("condiciones_medicas"), list) else [],
            antecedentes_familiares=data.get("antecedentes_familiares", []) if isinstance(data.get("antecedentes_familiares"), list) else [],
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            
            # Control del sistema
            fecha_registro=str(data.get("fecha_registro", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            registrado_por=str(data.get("registrado_por", "") if data.get("registrado_por") else ""),
            activo=bool(data.get("activo", True))
        )
    
    @property
    def nombre_completo(self) -> str:
        """Construir nombre completo desde campos separados"""
        nombres = []
        if self.primer_nombre:
            nombres.append(self.primer_nombre)
        if self.segundo_nombre:
            nombres.append(self.segundo_nombre)
        if self.primer_apellido:
            nombres.append(self.primer_apellido)
        if self.segundo_apellido:
            nombres.append(self.segundo_apellido)
        
        return " ".join(nombres) if nombres else "Sin nombre"

    @property
    def edad_display(self) -> str:
        """Propiedad para mostrar la edad"""
        return f"{self.edad} años" if self.edad else "N/A"
    
    @property
    def telefono_display(self) -> str:
        """Propiedad para mostrar el teléfono principal"""
        if self.telefono_1:
            return self.telefono_1
        elif self.telefono_2:
            return self.telefono_2
        else:
            return "Sin teléfono"
    
    @property
    def fecha_registro_display(self) -> str:
        """Propiedad para mostrar la fecha de registro formateada"""
        try:
            if self.fecha_registro:
                fecha_obj = datetime.fromisoformat(self.fecha_registro.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y")
            return "Sin fecha"
        except:
            return str(self.fecha_registro)
    
    @property
    def contacto_display(self) -> str:
        """Propiedad para mostrar información de contacto resumida"""
        contactos = []
        if self.telefono_1:
            contactos.append(f"Tel1: {self.telefono_1}")
        if self.telefono_2:
            contactos.append(f"Tel2: {self.telefono_2}")
        if self.email:
            contactos.append(f"Email: {self.email}")
        
        return " | ".join(contactos) if contactos else "Sin contacto"
    
    @property
    def alergias_display(self) -> str:
        """Propiedad para mostrar alergias como string"""
        return ", ".join(self.alergias) if self.alergias else "Sin alergias conocidas"
    
    @property
    def medicamentos_display(self) -> str:
        """Propiedad para mostrar medicamentos como string"""
        return ", ".join(self.medicamentos_actuales) if self.medicamentos_actuales else "Sin medicamentos"
    
    @property
    def condiciones_display(self) -> str:
        """Propiedad para mostrar condiciones médicas como string"""
        return ", ".join(self.condiciones_medicas) if self.condiciones_medicas else "Sin condiciones reportadas"

    def matches_search(self, search_term: str) -> bool:
        """Verificar si el paciente coincide con el término de búsqueda"""
        if not search_term:
            return True
        
        search_lower = search_term.lower()
        fields_to_search = [
            self.primer_nombre.lower(),
            self.segundo_nombre.lower() if self.segundo_nombre else "",
            self.primer_apellido.lower(),
            self.segundo_apellido.lower() if self.segundo_apellido else "",
            self.numero_documento.lower(),
            self.email.lower() if self.email else "",
            self.telefono_1.lower() if self.telefono_1 else "",
            self.telefono_2.lower() if self.telefono_2 else "",
            self.numero_historia.lower()
        ]
        
        return any(search_lower in field for field in fields_to_search)


class PacientesStatsModel(rx.Base):
    """Modelo para estadísticas de pacientes"""
    total: int = 0
    nuevos_mes: int = 0
    activos: int = 0
    hombres: int = 0
    mujeres: int = 0
    
    # Estadísticas adicionales
    edad_promedio: float = 0.0
    pacientes_con_email: int = 0
    pacientes_con_telefono: int = 0
    registros_ultima_semana: int = 0


class ContactoEmergenciaModel(rx.Base):
    """Modelo para datos de contacto de emergencia"""
    nombre: str = ""
    telefono: str = ""
    relacion: str = ""  # Familiar, amigo, etc.
    direccion: Optional[str] = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactoEmergenciaModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            nombre=str(data.get("nombre", "")),
            telefono=str(data.get("telefono", "")),
            relacion=str(data.get("relacion", "")),
            direccion=str(data.get("direccion", "") if data.get("direccion") else "")
        )


class AlergiaModel(rx.Base):
    """Modelo para datos de alergias específicas"""
    nombre: str = ""
    tipo: str = ""  # medicamento, alimento, ambiental, etc.
    severidad: str = "leve"  # leve, moderada, severa
    reaccion: str = ""
    fecha_diagnostico: Optional[str] = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlergiaModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            nombre=str(data.get("nombre", "")),
            tipo=str(data.get("tipo", "")),
            severidad=str(data.get("severidad", "leve")),
            reaccion=str(data.get("reaccion", "")),
            fecha_diagnostico=str(data.get("fecha_diagnostico", "") if data.get("fecha_diagnostico") else "")
        )