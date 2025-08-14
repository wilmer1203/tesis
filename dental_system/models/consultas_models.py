"""
Modelos de datos para el módulo de CONSULTAS
Centraliza todos los modelos relacionados con gestión de consultas por orden de llegada
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class ConsultaModel(rx.Base):
    """Modelo para datos de consultas/citas por orden de llegada"""
    id: Optional[str] = ""
    numero_consulta: str = ""
    paciente_id: str = ""
    odontologo_id: str = ""
    fecha_programada: str = ""
    fecha_inicio_real: Optional[str] = ""
    fecha_fin_real: Optional[str] = ""
    estado: str = "programada"  # programada = en espera por orden de llegada
    tipo_consulta: str = "general"
    prioridad: str = "normal"
    motivo_consulta: Optional[str] = ""
    observaciones_cita: Optional[str] = ""
    costo_total: float = 0.0
    
    # ✅ INFORMACIÓN RELACIONADA - Procesada desde las tablas
    paciente_nombre: str = ""          # Viene como paciente_nombre_completo
    odontologo_nombre: str = ""        # Viene como odontologo_nombre_completo
    paciente_telefono: str = ""        # Teléfono principal del paciente
    paciente_documento: str = ""       # Documento del paciente
    odontologo_especialidad: str = "" # Especialidad del odontólogo
    
    orden_llegada: Optional[int] = None  # Posición en la cola del odontólogo

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConsultaModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            numero_consulta=str(data.get("numero_consulta", "")),
            paciente_id=str(data.get("paciente_id", "")),
            odontologo_id=str(data.get("odontologo_id", "")),
            fecha_programada=str(data.get("fecha_programada", "")),
            fecha_inicio_real=str(data.get("fecha_inicio_real", "") if data.get("fecha_inicio_real") else ""),
            fecha_fin_real=str(data.get("fecha_fin_real", "") if data.get("fecha_fin_real") else ""),
            estado=str(data.get("estado", "programada")),
            tipo_consulta=str(data.get("tipo_consulta", "general")),
            prioridad=str(data.get("prioridad", "normal")),
            motivo_consulta=str(data.get("motivo_consulta", "") if data.get("motivo_consulta") else ""),
            observaciones_cita=str(data.get("observaciones_cita", "") if data.get("observaciones_cita") else ""),
            costo_total=float(data.get("costo_total", 0)),
            
            # Orden de llegada
            orden_llegada=data.get("orden_llegada"),
            
            # ✅ INFORMACIÓN RELACIONADA - Procesada por las tablas
            paciente_nombre=str(data.get("paciente_nombre_completo", "") or data.get("paciente_nombre", "")),
            odontologo_nombre=str(data.get("odontologo_nombre_completo", "") or data.get("odontologo_nombre", "")),
            paciente_telefono=str(data.get("paciente_telefono", "") if data.get("paciente_telefono") else ""),
            paciente_documento=str(data.get("paciente_documento", "") if data.get("paciente_documento") else ""),
            odontologo_especialidad=str(data.get("odontologo_especialidad", "") if data.get("odontologo_especialidad") else "")
        )
    
    @property
    def estado_display(self) -> str:
        """Propiedad para mostrar el estado formateado"""
        estados_map = {
            "programada": "En Espera",  # ← IMPORTANTE: programada = en espera por orden de llegada
            "confirmada": "Confirmada", 
            "en_progreso": "En Progreso",
            "completada": "Completada",
            "cancelada": "Cancelada",
            "no_asistio": "No Asistió"
        }
        return estados_map.get(self.estado, self.estado.capitalize())
    
    @property
    def fecha_display(self) -> str:
        """Propiedad para mostrar la fecha formateada"""
        try:
            if self.fecha_programada:
                fecha_obj = datetime.fromisoformat(self.fecha_programada.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y %H:%M")
            return "Sin fecha"
        except:
            return str(self.fecha_programada)
    
    @property
    def hora_display(self) -> str:
        """Propiedad para mostrar solo la hora"""
        try:
            if self.fecha_programada:
                fecha_obj = datetime.fromisoformat(self.fecha_programada.replace('Z', '+00:00'))
                return fecha_obj.strftime("%H:%M")
            return "00:00"
        except:
            return "00:00"
    
    @property
    def paciente_info_display(self) -> str:
        """Información completa del paciente para mostrar"""
        info_parts = [self.paciente_nombre]
        if self.paciente_documento:
            info_parts.append(f"CC: {self.paciente_documento}")
        if self.paciente_telefono:
            info_parts.append(f"Tel: {self.paciente_telefono}")
        return " | ".join(info_parts)
    
    @property
    def odontologo_info_display(self) -> str:
        """Información completa del odontólogo para mostrar"""
        info_parts = [self.odontologo_nombre]
        if self.odontologo_especialidad:
            info_parts.append(f"({self.odontologo_especialidad})")
        return " ".join(info_parts)
    
    @property
    def prioridad_color(self) -> str:
        """Color para mostrar según la prioridad"""
        colores_prioridad = {
            "baja": "#28a745",      # Verde
            "normal": "#007bff",    # Azul
            "alta": "#ffc107",      # Amarillo
            "urgente": "#dc3545"    # Rojo
        }
        return colores_prioridad.get(self.prioridad, "#007bff")
    
    @property
    def duracion_estimada_display(self) -> str:
        """Duración estimada basada en el tipo de consulta"""
        duraciones = {
            "general": "30 min",
            "control": "15 min",
            "urgencia": "45 min",
            "cirugia": "60 min",
            "otro": "30 min"
        }
        return duraciones.get(self.tipo_consulta, "30 min")
    
    @property
    def esta_en_progreso(self) -> bool:
        """Indica si la consulta está en progreso"""
        return self.estado == "en_progreso"
    
    @property
    def puede_iniciar(self) -> bool:
        """Indica si la consulta puede iniciarse (está programada)"""
        return self.estado == "programada"
    
    @property
    def puede_finalizar(self) -> bool:
        """Indica si la consulta puede finalizarse (está en progreso)"""
        return self.estado == "en_progreso"


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
        """Crear turno desde una consulta"""
        return cls(
            consulta_id=consulta.id,
            numero_turno=numero_turno,
            paciente_nombre=consulta.paciente_nombre,
            hora_llegada=consulta.fecha_programada,
            odontologo_id=consulta.odontologo_id,
            odontologo_nombre=consulta.odontologo_nombre
        )


class ConsultasStatsModel(rx.Base):
    """Modelo para estadísticas de consultas"""
    total_dia: int = 0
    en_espera: int = 0
    en_progreso: int = 0
    completadas: int = 0
    canceladas: int = 0
    
    # Por odontólogo
    por_odontologo: Dict[str, int] = {}
    
    # Por tipo
    por_tipo: Dict[str, int] = {}
    
    # Tiempo promedio
    tiempo_promedio_atencion: float = 0.0  # En minutos
    tiempo_promedio_espera: float = 0.0     # En minutos


class MotivosConsultaModel(rx.Base):
    """Modelo para categorización de motivos de consulta"""
    motivo_id: str = ""
    nombre: str = ""
    categoria: str = ""  # preventiva, urgencia, estetica, etc.
    descripcion: str = ""
    duracion_estimada: int = 30  # minutos
    requiere_autorizacion: bool = False
    activo: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MotivosConsultaModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            motivo_id=str(data.get("motivo_id", "")),
            nombre=str(data.get("nombre", "")),
            categoria=str(data.get("categoria", "")),
            descripcion=str(data.get("descripcion", "")),
            duracion_estimada=int(data.get("duracion_estimada", 30)),
            requiere_autorizacion=bool(data.get("requiere_autorizacion", False)),
            activo=bool(data.get("activo", True))
        )


class HorarioAtencionModel(rx.Base):
    """Modelo para horarios de atención por odontólogo"""
    odontologo_id: str = ""
    dia_semana: str = ""  # lunes, martes, etc.
    hora_inicio: str = "08:00"
    hora_fin: str = "17:00"
    duracion_cita: int = 30  # minutos
    activo: bool = True
    
    @property
    def slots_disponibles(self) -> List[str]:
        """Calcula los slots disponibles para el día"""
        slots = []
        try:
            from datetime import datetime, timedelta
            
            inicio = datetime.strptime(self.hora_inicio, "%H:%M")
            fin = datetime.strptime(self.hora_fin, "%H:%M")
            
            current = inicio
            while current + timedelta(minutes=self.duracion_cita) <= fin:
                slots.append(current.strftime("%H:%M"))
                current += timedelta(minutes=self.duracion_cita)
            
            return slots
        except:
            return []