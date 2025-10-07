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
    tipo_documento: str = "CI"
    fecha_nacimiento: Optional[str] = ""
    edad: Optional[int] = None
    genero: Optional[str] = ""
    
    # ✅ CELULARES SEPARADOS (según esquema v4.1)
    celular_1: Optional[str] = ""
    celular_2: Optional[str] = ""
    
    email: Optional[str] = ""
    direccion: Optional[str] = ""
    ciudad: Optional[str] = ""
    departamento: Optional[str] = ""
    ocupacion: Optional[str] = ""
    estado_civil: Optional[str] = ""
    
    # Contacto de emergencia (JSONB en BD)
    contacto_emergencia: Dict[str, Any] = {}
    
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
            tipo_documento=str(data.get("tipo_documento", "CI")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "") if data.get("fecha_nacimiento") else ""),
            edad=data.get("edad") if isinstance(data.get("edad"), int) else None,
            genero=str(data.get("genero", "") if data.get("genero") else ""),
            
            # ✅ CELULARES SEPARADOS
            celular_1=str(data.get("celular_1", "") if data.get("celular_1") else ""),
            celular_2=str(data.get("celular_2", "") if data.get("celular_2") else ""),
            
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
            activo=bool(data.get("activo", True)),
            
            # Contacto emergencia
            contacto_emergencia=data.get("contacto_emergencia", {}) if isinstance(data.get("contacto_emergencia"), dict) else {}
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
    def edad_display(self) -> str:
        """Propiedad para mostrar la edad"""
        # Usar edad de BD si existe, sino calcular desde fecha nacimiento
        edad = self.edad if self.edad else self.edad_calculada
        return f"{edad} años" if edad and edad > 0 else "N/A"
    
    @property
    def celular_display(self) -> str:
        """Propiedad para mostrar el celular principal"""
        if self.celular_1:
            return self.celular_1
        elif self.celular_2:
            return self.celular_2
        else:
            return "Sin celular"
    
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
        if self.celular_1:
            contactos.append(f"Cel1: {self.celular_1}")
        if self.celular_2:
            contactos.append(f"Cel2: {self.celular_2}")
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

    @property
    def contacto_emergencia_display(self) -> str:
        """Propiedad para mostrar contacto de emergencia"""
        if not self.contacto_emergencia or not isinstance(self.contacto_emergencia, dict):
            return "Sin contacto emergencia"

        nombre = self.contacto_emergencia.get("nombre", "")
        telefono = self.contacto_emergencia.get("telefono", "")
        relacion = self.contacto_emergencia.get("relacion", "")

        if nombre and telefono:
            return f"{nombre} ({relacion}) - {telefono}" if relacion else f"{nombre} - {telefono}"
        elif nombre:
            return f"{nombre} ({relacion})" if relacion else nombre
        else:
            return "Sin contacto emergencia"

    @property
    def tiene_alertas_medicas(self) -> bool:
        """🚨 Verificar si el paciente tiene alertas médicas importantes"""
        return bool(
            self.alergias or
            self.medicamentos_actuales or
            self.condiciones_medicas
        )

    @property
    def alergias_medicamentos(self) -> str:
        """💊 Concatenar alergias y medicamentos para mostrar en alertas"""
        alertas = []
        if self.alergias:
            alertas.append(f"Alergias: {', '.join(self.alergias)}")
        if self.medicamentos_actuales:
            alertas.append(f"Medicamentos: {', '.join(self.medicamentos_actuales)}")
        if self.condiciones_medicas:
            alertas.append(f"Condiciones: {', '.join(self.condiciones_medicas)}")

        return " | ".join(alertas) if alertas else None

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
            self.celular_1.lower() if self.celular_1 else "",
            self.celular_2.lower() if self.celular_2 else "",
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


# ==========================================
# 📝 FORMULARIOS DE PACIENTES
# ==========================================

class PacienteFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE PACIENTES
    
    Reemplaza: form_data: Dict[str, str] en pacientes_service
    """
    
    # Datos personales básicos
    primer_nombre: str = ""
    segundo_nombre: str = ""
    primer_apellido: str = ""
    segundo_apellido: str = ""
    
    # Identificación y contacto
    numero_documento: str = ""
    numero_historia: str = ""
    tipo_documento: str = "CI"  # CI, Pasaporte (según esquema v4.1)
    celular_1: str = ""
    celular_2: str = ""
    email: str = ""
    
    # Datos demográficos
    fecha_nacimiento: str = ""  # YYYY-MM-DD format
    edad: str = ""
    genero: str = ""  # masculino, femenino, otro
    direccion: str = ""
    ciudad: str = ""
    departamento: str = ""
    estado_civil: str = ""
    ocupacion: str = ""
    
    # Información médica
    alergias: str = ""
    medicamentos_actuales: str = ""
    condiciones_medicas: str = ""
    antecedentes_familiares: str = ""
    observaciones_medicas: str = ""
    
    # Contacto emergencia
    contacto_emergencia_nombre: str = ""
    contacto_emergencia_telefono: str = ""
    contacto_emergencia_relacion: str = ""
    contacto_emergencia_direccion: str = ""
    
    # Estado
    activo: bool = True
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos y formato"""
        errors = {}
        
        if not self.primer_nombre.strip():
            errors.setdefault("primer_nombre", []).append("Primer nombre es requerido")
        
        if not self.primer_apellido.strip():
            errors.setdefault("primer_apellido", []).append("Primer apellido es requerido")
        
        if not self.numero_documento.strip():
            errors.setdefault("numero_documento", []).append("Número de documento es requerido")
        
        if self.email:
            email_clean = self.email.strip()
            if not email_clean:
                pass  # Email vacío es válido
            elif "@" not in email_clean or "." not in email_clean.split("@")[-1] or email_clean.endswith(","):
                errors.setdefault("email", []).append("Email debe tener formato válido (ej: usuario@dominio.com)")
        
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
        """Convertir a dict para compatibilidad con servicios existentes"""
        return {
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "primer_apellido": self.primer_apellido,
            "segundo_apellido": self.segundo_apellido,
            "numero_documento": self.numero_documento,
            "numero_historia": self.numero_historia,
            "tipo_documento": self.tipo_documento,
            "celular_1": self.celular_1,
            "celular_2": self.celular_2,
            "email": self.email,
            "fecha_nacimiento": self.fecha_nacimiento,
            "edad": self.edad,
            "genero": self.genero,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "departamento": self.departamento,
            "estado_civil": self.estado_civil,
            "ocupacion": self.ocupacion,
            "alergias": self.alergias,
            "medicamentos_actuales": self.medicamentos_actuales,
            "condiciones_medicas": self.condiciones_medicas,
            "antecedentes_familiares": self.antecedentes_familiares,
            "observaciones_medicas": self.observaciones_medicas,
            
            # Contacto emergencia como JSONB
            "contacto_emergencia": {
                "nombre": self.contacto_emergencia_nombre,
                "telefono": self.contacto_emergencia_telefono,
                "relacion": self.contacto_emergencia_relacion,
                "direccion": self.contacto_emergencia_direccion
            } if any([self.contacto_emergencia_nombre, self.contacto_emergencia_telefono]) else {},
            
            "activo": str(self.activo)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PacienteFormModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            primer_nombre=str(data.get("primer_nombre", "")),
            segundo_nombre=str(data.get("segundo_nombre", "")),
            primer_apellido=str(data.get("primer_apellido", "")),
            segundo_apellido=str(data.get("segundo_apellido", "")),
            numero_documento=str(data.get("numero_documento", "")),
            numero_historia=str(data.get("numero_historia", "")),
            tipo_documento=str(data.get("tipo_documento", "CI")),
            celular_1=str(data.get("celular_1", "")),
            celular_2=str(data.get("celular_2", "")),
            email=str(data.get("email", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "")),
            edad=str(data.get("edad", "")),
            genero=str(data.get("genero", "")),
            direccion=str(data.get("direccion", "")),
            ciudad=str(data.get("ciudad", "")),
            departamento=str(data.get("departamento", "")),
            estado_civil=str(data.get("estado_civil", "")),
            ocupacion=str(data.get("ocupacion", "")),
            alergias=str(data.get("alergias", "")),
            medicamentos_actuales=str(data.get("medicamentos_actuales", "")),
            condiciones_medicas=str(data.get("condiciones_medicas", "")),
            antecedentes_familiares=str(data.get("antecedentes_familiares", "")),
            observaciones_medicas=str(data.get("observaciones_medicas", "")),
            
            # Contacto emergencia desde JSONB
            contacto_emergencia_nombre=str(data.get("contacto_emergencia", {}).get("nombre", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),
            contacto_emergencia_telefono=str(data.get("contacto_emergencia", {}).get("telefono", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),
            contacto_emergencia_relacion=str(data.get("contacto_emergencia", {}).get("relacion", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),
            contacto_emergencia_direccion=str(data.get("contacto_emergencia", {}).get("direccion", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),
            
            activo=data.get("activo", True) if isinstance(data.get("activo"), bool) else str(data.get("activo", "True")).lower() == "true"
        )