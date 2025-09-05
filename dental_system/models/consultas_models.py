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
    
    # ✅ MÚLTIPLES ODONTÓLOGOS (esquema v4.1)
    primer_odontologo_id: str = ""         # Campo principal BD
    odontologo_preferido_id: Optional[str] = ""  # Campo opcional BD
    
    # ✅ SISTEMA DE COLAS (esquema v4.1) 
    fecha_llegada: str = ""                # Momento real de llegada
    orden_llegada_general: Optional[int] = None    # Orden global del día
    orden_cola_odontologo: Optional[int] = None    # Orden en cola específica
    
    # ✅ ESTADOS ESPECÍFICOS DEL NEGOCIO (esquema v4.1)
    estado: str = "en_espera"  # en_espera, en_atencion, entre_odontologos, completada, cancelada
    tipo_consulta: str = "general"  # general, control, urgencia, emergencia
    prioridad: str = "normal"       # baja, normal, alta, urgente
    
    # Detalles de la consulta
    motivo_consulta: Optional[str] = ""
    observaciones: Optional[str] = ""
    notas_internas: Optional[str] = ""
    
    # ✅ COSTOS DUALES (esquema v4.1)
    costo_total_bs: float = 0.0
    costo_total_usd: float = 0.0
    
    # Control administrativo
    creada_por: Optional[str] = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""
    fecha_inicio_atencion: Optional[str] = ""
    fecha_fin_atencion: Optional[str] = ""
    
    # ✅ INFORMACIÓN RELACIONADA (JOINs con otras tablas)
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
        
        return cls(
            # Campos principales
            id=str(data.get("id", "")),
            numero_consulta=str(data.get("numero_consulta", "")),
            paciente_id=str(data.get("paciente_id", "")),
            
            # ✅ MÚLTIPLES ODONTÓLOGOS
            primer_odontologo_id=str(data.get("primer_odontologo_id", "") or data.get("odontologo_id", "")),  # Compatibility
            odontologo_preferido_id=str(data.get("odontologo_preferido_id", "") if data.get("odontologo_preferido_id") else ""),
            
            # ✅ SISTEMA DE COLAS
            fecha_llegada=str(data.get("fecha_llegada", "") or data.get("fecha_programada", "")),  # Compatibility
            orden_llegada_general=data.get("orden_llegada_general") or data.get("orden_llegada"),  # Compatibility
            orden_cola_odontologo=data.get("orden_cola_odontologo"),
            
            # ✅ ESTADOS ESPECÍFICOS
            estado=str(data.get("estado", "en_espera")),
            tipo_consulta=str(data.get("tipo_consulta", "general")),
            prioridad=str(data.get("prioridad", "normal")),
            
            # Detalles
            motivo_consulta=str(data.get("motivo_consulta", "") if data.get("motivo_consulta") else ""),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            notas_internas=str(data.get("notas_internas", "") if data.get("notas_internas") else ""),
            
            # ✅ COSTOS DUALES
            costo_total_bs=float(data.get("costo_total_bs", 0) or data.get("costo_total", 0)),  # Compatibility
            costo_total_usd=float(data.get("costo_total_usd", 0)),
            
            # Control administrativo
            creada_por=str(data.get("creada_por", "") if data.get("creada_por") else ""),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            fecha_inicio_atencion=str(data.get("fecha_inicio_atencion", "") if data.get("fecha_inicio_atencion") else ""),
            fecha_fin_atencion=str(data.get("fecha_fin_atencion", "") if data.get("fecha_fin_atencion") else ""),
            
            # ✅ INFORMACIÓN RELACIONADA (JOINs)
            paciente_nombre=str(data.get("paciente_nombre_completo", "") or data.get("paciente_nombre", "")),
            odontologo_nombre=str(data.get("odontologo_nombre_completo", "") or data.get("odontologo_nombre", "")),
            paciente_telefono=str(data.get("paciente_telefono", "") if data.get("paciente_telefono") else ""),
            paciente_documento=str(data.get("paciente_documento", "") if data.get("paciente_documento") else ""),
            odontologo_especialidad=str(data.get("odontologo_especialidad", "") if data.get("odontologo_especialidad") else "")
        )
    
    @property
    def estado_display(self) -> str:
        """Propiedad para mostrar el estado formateado - ESQUEMA v4.1"""
        estados_map = {
            "en_espera": "🕐 En Espera",           # Esperando en cola
            "en_atencion": "👨‍⚕️ En Atención",        # Siendo atendido
            "entre_odontologos": "🔄 Entre Odontólogos",  # Cambio de odontólogo
            "completada": "✅ Completada",          # Finalizada
            "cancelada": "❌ Cancelada",            # Cancelada
            # Compatibility con estados anteriores
            "programada": "🕐 En Espera",
            "en_progreso": "👨‍⚕️ En Atención",
            "no_asistio": "👻 No Asistió"
        }
        return estados_map.get(self.estado, self.estado.capitalize())
    
    @property
    def fecha_display(self) -> str:
        """Propiedad para mostrar la fecha de llegada formateada - ESQUEMA v4.1"""
        try:
            if self.fecha_llegada:
                fecha_obj = datetime.fromisoformat(self.fecha_llegada.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y %H:%M")
            return "Sin fecha"
        except:
            return str(self.fecha_llegada)
    
    @property
    def hora_display(self) -> str:
        """Propiedad para mostrar solo la hora de llegada - ESQUEMA v4.1"""
        try:
            if self.fecha_llegada:
                fecha_obj = datetime.fromisoformat(self.fecha_llegada.replace('Z', '+00:00'))
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
        """Indica si la consulta está en progreso - ESQUEMA v4.1"""
        return self.estado in ["en_atencion", "en_progreso"]  # Compatibility
    
    @property
    def puede_iniciar(self) -> bool:
        """Indica si la consulta puede iniciarse (está en espera) - ESQUEMA v4.1"""
        return self.estado in ["en_espera", "programada"]  # Compatibility
    
    @property
    def puede_finalizar(self) -> bool:
        """Indica si la consulta puede finalizarse (está en atención) - ESQUEMA v4.1"""
        return self.estado in ["en_atencion", "en_progreso"]  # Compatibility
    
    @property
    def posicion_cola_display(self) -> str:
        """Muestra la posición en cola del odontólogo"""
        if self.orden_cola_odontologo:
            return f"#{self.orden_cola_odontologo}"
        return "Sin asignar"
    
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
    
    @property
    def es_urgente(self) -> bool:
        """Indica si la consulta es urgente o de alta prioridad"""
        return self.prioridad in ["urgente", "alta"]


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


class ConsultaConOrdenModel(rx.Base):
    """Modelo tipado para consultas con información de orden de llegada"""
    consulta: ConsultaModel = ConsultaModel()
    orden: int = 0
    tiempo_espera_estimado: str = "~30 min"
    es_siguiente: bool = False
    
    @classmethod
    def from_consulta(cls, consulta: ConsultaModel, orden: int, tiempo_espera: str, es_siguiente: bool = False) -> "ConsultaConOrdenModel":
        """Crear instancia desde ConsultaModel con datos de orden"""
        return cls(
            consulta=consulta,
            orden=orden,
            tiempo_espera_estimado=tiempo_espera,
            es_siguiente=es_siguiente
        )
    
    @property
    def numero_turno_display(self) -> str:
        """Número de turno formateado para mostrar"""
        return f"#{self.orden:02d}"
    
    @property
    def estado_con_orden(self) -> str:
        """Estado con información de orden"""
        if self.es_siguiente:
            return "Siguiente"
        elif self.orden == 1:
            return "En atención"
        else:
            return f"Turno #{self.orden}"
    
    @property
    def paciente_nombre(self) -> str:
        """Acceso directo al nombre del paciente"""
        return self.consulta.paciente_nombre
    
    @property
    def paciente_documento(self) -> str:
        """Acceso directo al documento del paciente"""
        return self.consulta.paciente_documento
    
    @property
    def motivo_consulta(self) -> str:
        """Acceso directo al motivo de consulta"""
        return self.consulta.motivo_consulta
    
    @property
    def estado_display(self) -> str:
        """Estado formateado para mostrar"""
        return self.consulta.estado_display
    
    @property
    def prioridad_color(self) -> str:
        """Color de prioridad"""
        return self.consulta.prioridad_color


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


# ==========================================
# 📝 FORMULARIOS DE CONSULTAS
# ==========================================

class ConsultaFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE CONSULTAS - ESQUEMA BD v4.1
    
    Alineado con ConsultaModel y tabla `consultas` del esquema
    Reemplaza: form_data: Dict[str, str] en consultas_service
    """
    
    # ✅ REFERENCIAS MÚLTIPLES ODONTÓLOGOS (esquema v4.1)
    paciente_id: str = ""
    paciente_nombre: str = ""              # Para mostrar en UI
    primer_odontologo_id: str = ""         # Campo principal BD
    odontologo_preferido_id: str = ""      # Campo opcional BD
    
    # ✅ DETALLES DE LA CONSULTA (esquema v4.1)
    tipo_consulta: str = "general"  # general, control, urgencia, emergencia
    motivo_consulta: str = ""
    observaciones: str = ""         # Campo BD unificado
    notas_internas: str = ""        # Campo BD nuevo
    
    # ✅ PRIORIDAD Y ESTADO (esquema v4.1)
    prioridad: str = "normal"  # baja, normal, alta, urgente
    estado: str = "en_espera"  # en_espera, en_atencion, entre_odontologos, completada, cancelada
    
    # ✅ INFORMACIÓN MÉDICA (opcional para formulario)
    diagnostico_preliminar: str = ""
    diagnostico_final: str = ""
    tratamiento_realizado: str = ""
    receta_medicamentos: str = ""
    
    # ✅ SEGUIMIENTO Y CITAS (opcional)
    proxima_consulta: str = ""  # Fecha sugerida
    requiere_seguimiento: bool = False
    notas_seguimiento: str = ""
    
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
        
        # Validación de prioridad válida
        prioridades_validas = ["baja", "normal", "alta", "urgente"]
        if self.prioridad not in prioridades_validas:
            errors.setdefault("prioridad", []).append(f"Prioridad debe ser una de: {', '.join(prioridades_validas)}")
        
        return errors
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad - ESQUEMA BD v4.1"""
        return {
            # Referencias múltiples odontólogos
            "paciente_id": self.paciente_id,
            "primer_odontologo_id": self.primer_odontologo_id,
            "odontologo_preferido_id": self.odontologo_preferido_id,
            
            # Detalles de la consulta
            "tipo_consulta": self.tipo_consulta,
            "motivo_consulta": self.motivo_consulta,
            "observaciones": self.observaciones,
            "notas_internas": self.notas_internas,
            
            # Estado y prioridad
            "prioridad": self.prioridad,
            "estado": self.estado,
            
            # Información médica
            "diagnostico_preliminar": self.diagnostico_preliminar,
            "diagnostico_final": self.diagnostico_final,
            "tratamiento_realizado": self.tratamiento_realizado,
            "receta_medicamentos": self.receta_medicamentos,
            
            # Seguimiento
            "proxima_consulta": self.proxima_consulta,
            "requiere_seguimiento": str(self.requiere_seguimiento),
            "notas_seguimiento": self.notas_seguimiento,
            
            # Compatibility con nombres anteriores
            "odontologo_id": self.primer_odontologo_id,  # Alias para backward compatibility
        }
    
    def to_consulta_model(self) -> ConsultaModel:
        """Convertir formulario a modelo de consulta completo"""
        return ConsultaModel(
            paciente_id=self.paciente_id,
            primer_odontologo_id=self.primer_odontologo_id,
            odontologo_preferido_id=self.odontologo_preferido_id,
            tipo_consulta=self.tipo_consulta,
            motivo_consulta=self.motivo_consulta,
            observaciones=self.observaciones,
            notas_internas=self.notas_internas,
            prioridad=self.prioridad,
            estado=self.estado
        )


# ==========================================
# 📊 MODELOS DE FINALIZACIÓN Y RESUMEN
# ==========================================

class ConsultaFinalizacionModel(rx.Base):
    """
    ✅ MODELO PARA FINALIZACIÓN DE CONSULTAS
    
    Reemplaza: Dict[str, Any] en completar_consulta()
    Usado por: EstadoConsultas.completar_consulta()
    """
    
    # Diagnóstico final
    diagnostico_final: str = ""
    tratamiento_realizado: str = ""
    receta_medicamentos: str = ""
    
    # Seguimiento
    requiere_seguimiento: bool = False
    proxima_consulta: str = ""  # Fecha sugerida
    notas_seguimiento: str = ""
    
    # Información administrativa
    duracion_minutos: str = ""
    observaciones_finales: str = ""
    satisfaccion_paciente: str = "buena"  # excelente, buena, regular, mala
    
    # Información de costos (si aplica)
    costo_total_bs: str = "0"
    costo_total_usd: str = "0"
    metodo_pago: str = ""  # efectivo, tarjeta, transferencia, pendiente
    
    def validate_finalizacion(self) -> Dict[str, List[str]]:
        """Validar datos de finalización"""
        errors = {}
        
        if not self.diagnostico_final.strip():
            errors.setdefault("diagnostico_final", []).append("Diagnóstico final es requerido")
        
        if not self.tratamiento_realizado.strip():
            errors.setdefault("tratamiento_realizado", []).append("Tratamiento realizado es requerido")
        
        # Validar fecha de próxima consulta si requiere seguimiento
        if self.requiere_seguimiento and not self.proxima_consulta.strip():
            errors.setdefault("proxima_consulta", []).append("Fecha de próxima consulta requerida para seguimiento")
        
        # Validar satisfacción
        satisfacciones_validas = ["excelente", "buena", "regular", "mala"]
        if self.satisfaccion_paciente not in satisfacciones_validas:
            errors.setdefault("satisfaccion_paciente", []).append(f"Satisfacción debe ser una de: {', '.join(satisfacciones_validas)}")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a dict para compatibilidad con servicio"""
        return {
            "diagnostico_final": self.diagnostico_final,
            "tratamiento_realizado": self.tratamiento_realizado,
            "receta_medicamentos": self.receta_medicamentos,
            "requiere_seguimiento": self.requiere_seguimiento,
            "proxima_consulta": self.proxima_consulta if self.proxima_consulta.strip() else None,
            "notas_seguimiento": self.notas_seguimiento,
            "duracion_minutos": self.duracion_minutos,
            "observaciones_finales": self.observaciones_finales,
            "satisfaccion_paciente": self.satisfaccion_paciente,
            "costo_total_bs": self.costo_total_bs,
            "costo_total_usd": self.costo_total_usd,
            "metodo_pago": self.metodo_pago
        }


class ConsultaResumenModel(rx.Base):
    """
    📊 MODELO PARA RESUMEN DIARIO DE CONSULTAS
    
    Reemplaza: Dict[str, Any] en resumen_dia_actual computed var
    Usado por: EstadoConsultas.resumen_dia_actual
    """
    
    # Estadísticas básicas
    total_consultas: int = 0
    consultas_programadas: int = 0
    consultas_en_progreso: int = 0
    consultas_completadas: int = 0
    consultas_canceladas: int = 0
    
    # Métricas de tiempo
    tiempo_promedio_atencion: float = 0.0  # En minutos
    tiempo_total_atencion: float = 0.0     # En minutos
    pacientes_en_espera: int = 0
    tiempo_espera_promedio: float = 0.0    # En minutos
    
    # Información por odontólogo
    odontologos_activos: int = 0
    consultas_por_odontologo: Dict[str, int] = {}
    
    # Próximas actividades
    proximas_consultas: int = 0
    urgencias_pendientes: int = 0
    
    # Estado del día
    fecha_resumen: str = ""
    esta_activo: bool = True  # Si hay consultas activas
    proximo_numero_turno: int = 1
    
    @classmethod
    def from_consultas(cls, consultas: List[ConsultaModel], fecha: str = "") -> "ConsultaResumenModel":
        """Crear resumen desde lista de consultas"""
        if not consultas:
            return cls(fecha_resumen=fecha)
        
        # Contar por estado
        programadas = len([c for c in consultas if c.estado == "programada"])
        en_progreso = len([c for c in consultas if c.estado == "en_progreso"])
        completadas = len([c for c in consultas if c.estado == "completada"])
        canceladas = len([c for c in consultas if c.estado == "cancelada"])
        
        # Contar por odontólogo
        por_odontologo = {}
        for consulta in consultas:
            odontologo_id = consulta.primer_odontologo_id or "sin_asignar"
            por_odontologo[odontologo_id] = por_odontologo.get(odontologo_id, 0) + 1
        
        # Calcular métricas
        pacientes_esperando = programadas
        urgencias = len([c for c in consultas if c.prioridad == "urgente"])
        
        return cls(
            total_consultas=len(consultas),
            consultas_programadas=programadas,
            consultas_en_progreso=en_progreso,
            consultas_completadas=completadas,
            consultas_canceladas=canceladas,
            pacientes_en_espera=pacientes_esperando,
            consultas_por_odontologo=por_odontologo,
            odontologos_activos=len(por_odontologo),
            urgencias_pendientes=urgencias,
            fecha_resumen=fecha,
            esta_activo=(programadas + en_progreso) > 0,
            proximo_numero_turno=len(consultas) + 1
        )
    
    @property
    def porcentaje_completadas(self) -> float:
        """Porcentaje de consultas completadas"""
        if self.total_consultas == 0:
            return 0.0
        return (self.consultas_completadas / self.total_consultas) * 100
    
    @property
    def estado_dia_display(self) -> str:
        """Estado del día formateado"""
        if not self.esta_activo:
            return "Sin actividad"
        elif self.consultas_en_progreso > 0:
            return "En atención"
        elif self.pacientes_en_espera > 0:
            return "Pacientes esperando"
        else:
            return "Día completado"
    
    @property
    def odontologo_mas_activo(self) -> str:
        """Odontólogo con más consultas"""
        if not self.consultas_por_odontologo:
            return "N/A"
        
        max_consultas = max(self.consultas_por_odontologo.values())
        for odontologo_id, consultas in self.consultas_por_odontologo.items():
            if consultas == max_consultas:
                return odontologo_id
        
        return "N/A"