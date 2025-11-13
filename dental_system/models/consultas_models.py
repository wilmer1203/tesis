"""
Modelos de datos para el módulo de CONSULTAS
Centraliza todos los modelos relacionados con gestión de consultas por orden de llegada
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class ConsultaModel(rx.Base):
    """
    🏥 MODELO PRINCIPAL DE CONSULTAS - ESQUEMA BD v4.1
    
    Sistema de colas por orden de llegada (NO citas programadas)
    Alineado completamente con tabla `consultas` del esquema
    """
    # Campos principales de la tabla
    id: Optional[str] = ""
    numero_consulta: str = ""
    paciente_id: str = ""

    primer_odontologo_id: str = ""         # Campo principal BD

    fecha_llegada: str = ""                # Momento real de llegada
    orden_cola_odontologo: Optional[int] = None    # Orden en cola específica

    estado: str = "en_espera"  # en_espera, en_atencion, entre_odontologos, completada, cancelada
    tipo_consulta: str = "general"  # general, control, urgencia, emergencia

    motivo_consulta: Optional[str] = ""
    observaciones: Optional[str] = ""

    fecha_creacion: str = ""
    fecha_actualizacion: str = ""

    paciente_nombre: str = ""          
    odontologo_nombre: str = ""        
    paciente_telefono: str = ""        
    paciente_documento: str = ""       
    odontologo_especialidad: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConsultaModel":
        """Crear instancia desde diccionario de Supabase - ESQUEMA v4.1"""
        if not data or not isinstance(data, dict):
            return cls()

        # ✅ EXTRAER DATOS RELACIONADOS DE OBJETOS ANIDADOS
        paciente_obj = data.get("paciente", {}) or {}
        personal_obj = data.get("personal", {}) or {}

        # Construir nombre completo del paciente
        paciente_nombre = ""
        if paciente_obj:
            nombre_parts = [
                paciente_obj.get("primer_nombre", ""),
                paciente_obj.get("segundo_nombre", ""),
                paciente_obj.get("primer_apellido", ""),
                paciente_obj.get("segundo_apellido", "")
            ]
            paciente_nombre = " ".join([p for p in nombre_parts if p]).strip()

        # Construir nombre completo del odontólogo
        odontologo_nombre = ""
        if personal_obj:
            nombre_parts = [
                personal_obj.get("primer_nombre", ""),
                personal_obj.get("segundo_nombre", ""),
                personal_obj.get("primer_apellido", ""),
                personal_obj.get("segundo_apellido", "")
            ]
            odontologo_nombre = " ".join([p for p in nombre_parts if p]).strip()

        return cls(
            # Campos principales
            id=str(data.get("id", "")),
            numero_consulta=str(data.get("numero_consulta", "")),
            paciente_id=str(data.get("paciente_id", "")),

            # ✅ MÚLTIPLES ODONTÓLOGOS
            primer_odontologo_id=str(data.get("primer_odontologo_id", "") or data.get("odontologo_id", "")),

            # ✅ SISTEMA DE COLAS
            fecha_llegada=str(data.get("fecha_llegada", "") or data.get("fecha_programada", "")),
            orden_cola_odontologo=data.get("orden_cola_odontologo"),

            # ✅ ESTADOS ESPECÍFICOS
            estado=str(data.get("estado", "en_espera")),
            tipo_consulta=str(data.get("tipo_consulta", "general")),

            # Detalles
            motivo_consulta=str(data.get("motivo_consulta", "") if data.get("motivo_consulta") else ""),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),

            # Control administrativo
            fecha_creacion=str(data.get("fecha_creacion", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),

            # ✅ INFORMACIÓN RELACIONADA (extraída de objetos anidados)
            paciente_nombre=paciente_nombre or str(data.get("paciente_nombre_completo", "") or data.get("paciente_nombre", "")),
            odontologo_nombre=odontologo_nombre or str(data.get("odontologo_nombre_completo", "") or data.get("odontologo_nombre", "")),
            paciente_telefono=str(paciente_obj.get("celular", "") or paciente_obj.get("telefono", "") or data.get("paciente_telefono", "")),
            paciente_documento=str(paciente_obj.get("numero_documento", "") or data.get("paciente_documento", "")),
            odontologo_especialidad=str(personal_obj.get("especialidad", "") or data.get("odontologo_especialidad", ""))
        )


    @property
    def tiempo_espera_estimado(self) -> str:
        """Calcula tiempo estimado de espera basado en posición en cola"""
        if self.orden_cola_odontologo:
            # Estimación: 30 min por consulta anterior
            minutos = (self.orden_cola_odontologo - 1) * 30
            if minutos <= 0:
                return "Próximo"
            elif minutos < 60:
                return f"{minutos} min"
            else:
                horas = minutos // 60
                min_restantes = minutos % 60
                return f"{horas}h {min_restantes}m"
        return "N/A"
    

class TurnoModel(rx.Base):
    """Modelo para manejo de turnos por orden de llegada"""
    consulta_id: str = ""
    numero_turno: int = 0
    paciente_nombre: str = ""
    hora_llegada: str = ""
    estado_turno: str = "esperando"  # esperando, llamado, atendido
    odontologo_id: str = ""
    odontologo_nombre: str = ""
    tiempo_espera_minutos: int = 0
    
    @classmethod
    def from_consulta(cls, consulta: ConsultaModel, numero_turno: int) -> "TurnoModel":
        """Crear turno desde una consulta - ESQUEMA v4.1"""
        return cls(
            consulta_id=consulta.id,
            numero_turno=numero_turno,
            paciente_nombre=consulta.paciente_nombre,
            hora_llegada=consulta.fecha_llegada,  # Actualizado de fecha_programada a fecha_llegada
            odontologo_id=consulta.primer_odontologo_id,  # Actualizado de odontologo_id a primer_odontologo_id
            odontologo_nombre=consulta.odontologo_nombre
        )


# ==========================================
# 📝 FORMULARIOS DE CONSULTAS
# ==========================================

class ConsultaFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE CONSULTAS - ESQUEMA BD v4.1
    
    Alineado con ConsultaModel y tabla `consultas` del esquema
    Reemplaza: form_data: Dict[str, str] en consultas_service
    """

    paciente_id: str = ""
    paciente_nombre: str = ""              # Para mostrar en UI
    primer_odontologo_id: str = ""         # Campo principal BD

    tipo_consulta: str = "general"  # general, control, urgencia, emergencia
    motivo_consulta: str = ""
    observaciones: str = ""         # Campo BD unificado

    estado: str = "en_espera"  # en_espera, en_atencion, entre_odontologos, completada, cancelada

    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos - ESQUEMA BD v4.1"""
        errors = {}
        
        if not self.paciente_id.strip():
            errors.setdefault("paciente_id", []).append("Paciente es requerido")
        
        if not self.primer_odontologo_id.strip():
            errors.setdefault("primer_odontologo_id", []).append("Odontólogo principal es requerido")
        
        if not self.motivo_consulta.strip():
            errors.setdefault("motivo_consulta", []).append("Motivo de consulta es requerido")
        
        # Validación de estado válido
        estados_validos = ["en_espera", "en_atencion", "entre_odontologos", "completada", "cancelada"]
        if self.estado not in estados_validos:
            errors.setdefault("estado", []).append(f"Estado debe ser uno de: {', '.join(estados_validos)}")

        return errors
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad - ESQUEMA BD v4.1 LIMPIEZA 2025-10-21"""
        return {
            # Referencias múltiples odontólogos
            "paciente_id": self.paciente_id,
            "primer_odontologo_id": self.primer_odontologo_id,

            # Detalles de la consulta
            "tipo_consulta": self.tipo_consulta,
            "motivo_consulta": self.motivo_consulta,
            "observaciones": self.observaciones,

            # Estado
            "estado": self.estado,
            # Compatibility con nombres anteriores
            "odontologo_id": self.primer_odontologo_id,  # Alias para backward compatibility
        }
    
    def to_consulta_model(self) -> ConsultaModel:
        """Convertir formulario a modelo de consulta completo"""
        return ConsultaModel(
            paciente_id=self.paciente_id,
            primer_odontologo_id=self.primer_odontologo_id,
            tipo_consulta=self.tipo_consulta,
            motivo_consulta=self.motivo_consulta,
            observaciones=self.observaciones,
            estado=self.estado
        )

