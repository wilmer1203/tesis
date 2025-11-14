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
    genero: Optional[str] = ""

    # ✅ CELULARES SEPARADOS (según esquema v4.1)
    celular_1: Optional[str] = ""
    celular_2: Optional[str] = ""

    email: Optional[str] = ""
    direccion: Optional[str] = ""
    ciudad: Optional[str] = ""

    # Contacto de emergencia (JSONB en BD)
    contacto_emergencia: Dict[str, Any] = {}

    # Información médica
    alergias: List[str] = []
    medicamentos_actuales: List[str] = []
    condiciones_medicas: List[str] = []

    # Control del sistema
    fecha_registro: str = ""
    fecha_actualizacion: str = ""
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
            genero=str(data.get("genero", "") if data.get("genero") else ""),

            # ✅ CELULARES SEPARADOS
            celular_1=str(data.get("celular_1", "") if data.get("celular_1") else ""),
            celular_2=str(data.get("celular_2", "") if data.get("celular_2") else ""),

            email=str(data.get("email", "") if data.get("email") else ""),
            direccion=str(data.get("direccion", "") if data.get("direccion") else ""),
            ciudad=str(data.get("ciudad", "") if data.get("ciudad") else ""),

            # Información médica (arrays)
            alergias=data.get("alergias", []) if isinstance(data.get("alergias"), list) else [],
            medicamentos_actuales=data.get("medicamentos_actuales", []) if isinstance(data.get("medicamentos_actuales"), list) else [],
            condiciones_medicas=data.get("condiciones_medicas", []) if isinstance(data.get("condiciones_medicas"), list) else [],

            # Control del sistema
            fecha_registro=str(data.get("fecha_registro", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            activo=bool(data.get("activo", True)),

            # Contacto emergencia
            contacto_emergencia=data.get("contacto_emergencia", {}) if isinstance(data.get("contacto_emergencia"), dict) else {},
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
    tipo_documento: str = "CI"  
    celular_1: str = ""
    celular_2: str = ""
    codigo_pais_celular_1: str = "+58"  # Código de país para celular 1
    codigo_pais_celular_2: str = "+58"  # Código de país para celular 2
    email: str = ""

    # Datos demográficos
    fecha_nacimiento: str = ""  # YYYY-MM-DD format
    genero: str = ""  # masculino, femenino, otro
    direccion: str = ""
    ciudad: str = ""

    # Información médica
    alergias: str = ""
    medicamentos_actuales: str = ""
    condiciones_medicas: str = ""

    # Contacto emergencia
    contacto_emergencia_nombre: str = ""
    contacto_emergencia_telefono: str = ""
    codigo_pais_emergencia: str = "+58 (VE)"  # Código de país para contacto emergencia
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
            "genero": self.genero,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "alergias": self.alergias,
            "medicamentos_actuales": self.medicamentos_actuales,
            "condiciones_medicas": self.condiciones_medicas,

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
            codigo_pais_celular_1=str(data.get("codigo_pais_celular_1", "+58 (VE)")),
            codigo_pais_celular_2=str(data.get("codigo_pais_celular_2", "+58 (VE)")),
            email=str(data.get("email", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "")),
            genero=str(data.get("genero", "")),
            direccion=str(data.get("direccion", "")),
            ciudad=str(data.get("ciudad", "")),
            alergias=str(data.get("alergias", "")),
            medicamentos_actuales=str(data.get("medicamentos_actuales", "")),
            condiciones_medicas=str(data.get("condiciones_medicas", "")),

            # Contacto emergencia desde JSONB
            contacto_emergencia_nombre=str(data.get("contacto_emergencia", {}).get("nombre", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),
            contacto_emergencia_telefono=str(data.get("contacto_emergencia", {}).get("telefono", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),
            codigo_pais_emergencia=str(data.get("codigo_pais_emergencia", "+58 (VE)")),
            contacto_emergencia_relacion=str(data.get("contacto_emergencia", {}).get("relacion", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),
            contacto_emergencia_direccion=str(data.get("contacto_emergencia", {}).get("direccion", "") if isinstance(data.get("contacto_emergencia"), dict) else ""),

            activo=data.get("activo", True) if isinstance(data.get("activo"), bool) else str(data.get("activo", "True")).lower() == "true"
        )


# ==========================================
# 📋 MODELO PARA HISTORIAL COMPLETO DEL PACIENTE
# ==========================================

class ServicioHistorial(rx.Base):
    """Modelo para servicio dentro del historial"""
    nombre: str = ""
    cantidad: int = 1
    precio_unitario_usd: float = 0.0
    precio_unitario_bs: float = 0.0
    subtotal_usd: float = 0.0
    subtotal_bs: float = 0.0


class IntervencionHistorial(rx.Base):
    """Modelo para intervención dentro del historial"""
    id: str = ""
    odontologo_id: str = ""
    odontologo_nombre: str = ""
    procedimiento_realizado: str = ""
    total_usd: float = 0.0
    total_bs: float = 0.0
    # Servicios aplicados en la intervención
    servicios: List[ServicioHistorial] = []


class ConsultaHistorial(rx.Base):
    """Modelo para consulta con detalles completos en historial"""
    id: str = ""
    numero_consulta: str = ""
    fecha_llegada: str = ""
    estado: str = ""
    motivo_consulta: str = ""

    # Odontólogo principal
    primer_odontologo_id: str = ""
    primer_odontologo_nombre: str = ""

    # Intervenciones realizadas en la consulta
    intervenciones: List[IntervencionHistorial] = []

    # Totales de la consulta
    costo_total_usd: float = 0.0
    costo_total_bs: float = 0.0

    # Pago
    pago_id: str = ""
    pago_estado: str = "pendiente"  # pendiente, parcial, completado
    pago_usd: float = 0.0
    pago_bs: float = 0.0
    saldo_pendiente_usd: float = 0.0
    saldo_pendiente_bs: float = 0.0


class HistorialCompletoPaciente(rx.Base):
    """
    Modelo completo con toda la información del historial del paciente
    Usado en página de historial_paciente_page.py
    """
    # Lista de consultas con intervenciones y servicios
    consultas: List[ConsultaHistorial] = []

    # Estadísticas generales
    total_consultas: int = 0
    total_intervenciones: int = 0
    total_pagado_usd: float = 0.0
    total_pagado_bs: float = 0.0
    total_pendiente_usd: float = 0.0
    total_pendiente_bs: float = 0.0
