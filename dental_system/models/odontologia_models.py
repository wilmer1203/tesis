"""
Modelos de datos para el módulo de ODONTOLOGÍA
Centraliza todos los modelos relacionados con atención odontológica especializada
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class OdontogramaModel(rx.Base):
    """Modelo para odontogramas de pacientes"""
    id: Optional[str] = ""
    paciente_id: str = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""
    odontologo_id: str = ""
    tipo_odontograma: str = "adulto"  # adulto, pediatrico, mixto
    version: int = 1
    activo: bool = True
    notas_generales: Optional[str] = ""
    observaciones_clinicas: Optional[str] = ""
    template_usado: str = "universal"
    configuracion: Dict[str, Any] = {}
    
    # Información relacionada
    paciente_nombre: str = ""
    odontologo_nombre: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OdontogramaModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            paciente_id=str(data.get("paciente_id", "")),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            odontologo_id=str(data.get("odontologo_id", "")),
            tipo_odontograma=str(data.get("tipo_odontograma", "adulto")),
            version=int(data.get("version", 1)),
            activo=bool(data.get("activo", True)),
            notas_generales=str(data.get("notas_generales", "") if data.get("notas_generales") else ""),
            observaciones_clinicas=str(data.get("observaciones_clinicas", "") if data.get("observaciones_clinicas") else ""),
            template_usado=str(data.get("template_usado", "universal")),
            configuracion=data.get("configuracion", {}),
            paciente_nombre=str(data.get("paciente_nombre", "")),
            odontologo_nombre=str(data.get("odontologo_nombre", ""))
        )
    
    @property
    def fecha_creacion_display(self) -> str:
        """Fecha de creación formateada"""
        try:
            if self.fecha_creacion:
                fecha_obj = datetime.fromisoformat(self.fecha_creacion.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y")
            return "Sin fecha"
        except:
            return str(self.fecha_creacion)
    
    @property
    def tipo_display(self) -> str:
        """Tipo de odontograma formateado"""
        tipos_map = {
            "adulto": "👨 Adulto (32 dientes)",
            "pediatrico": "👶 Pediátrico (20 dientes)",
            "mixto": "👨‍👩‍👧‍👦 Mixto"
        }
        return tipos_map.get(self.tipo_odontograma, self.tipo_odontograma.title())


class DienteModel(rx.Base):
    """Modelo para dientes individuales (catálogo FDI)"""
    id: str = ""
    numero_diente: int = 0
    numero_diente_pediatrico: Optional[int] = None
    nombre: str = ""
    tipo_diente: str = ""  # incisivo, canino, premolar, molar
    ubicacion: str = ""    # superior_derecha, superior_izquierda, etc.
    cuadrante: int = 0
    es_temporal: bool = False
    posicion_en_cuadrante: Optional[int] = None
    caras: List[str] = []  # oclusal, mesial, distal, vestibular, lingual
    descripcion_anatomica: Optional[str] = ""
    activo: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DienteModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            numero_diente=int(data.get("numero_diente", 0)),
            numero_diente_pediatrico=int(data.get("numero_diente_pediatrico")) if data.get("numero_diente_pediatrico") else None,
            nombre=str(data.get("nombre", "")),
            tipo_diente=str(data.get("tipo_diente", "")),
            ubicacion=str(data.get("ubicacion", "")),
            cuadrante=int(data.get("cuadrante", 0)),
            es_temporal=bool(data.get("es_temporal", False)),
            posicion_en_cuadrante=int(data.get("posicion_en_cuadrante")) if data.get("posicion_en_cuadrante") else None,
            caras=data.get("caras", []),
            descripcion_anatomica=str(data.get("descripcion_anatomica", "") if data.get("descripcion_anatomica") else ""),
            activo=bool(data.get("activo", True))
        )
    
    @property
    def numero_display(self) -> str:
        """Número de diente formateado"""
        if self.es_temporal and self.numero_diente_pediatrico:
            return f"{self.numero_diente_pediatrico} (temp)"
        return str(self.numero_diente)
    
    @property
    def tipo_emoji(self) -> str:
        """Emoji según el tipo de diente"""
        emojis = {
            "incisivo": "🦷",
            "canino": "🔸",
            "premolar": "🔹",
            "molar": "🟫"
        }
        return emojis.get(self.tipo_diente.lower(), "🦷")
    
    @property
    def ubicacion_display(self) -> str:
        """Ubicación formateada"""
        ubicaciones_map = {
            "superior_derecha": "🔝➡️ Superior Derecha",
            "superior_izquierda": "🔝⬅️ Superior Izquierda",
            "inferior_derecha": "🔻➡️ Inferior Derecha",
            "inferior_izquierda": "🔻⬅️ Inferior Izquierda"
        }
        return ubicaciones_map.get(self.ubicacion, self.ubicacion.replace('_', ' ').title())


class CondicionDienteModel(rx.Base):
    """Modelo para condiciones específicas de cada diente"""
    id: Optional[str] = ""
    odontograma_id: str = ""
    diente_id: str = ""
    tipo_condicion: str = ""
    caras_afectadas: List[str] = []
    severidad: str = "leve"
    descripcion: Optional[str] = ""
    observaciones: Optional[str] = ""
    material_utilizado: Optional[str] = ""
    color_material: Optional[str] = ""
    fecha_tratamiento: Optional[str] = ""
    estado: str = "actual"  # planificado, en_tratamiento, actual, historico
    requiere_seguimiento: bool = False
    fecha_registro: str = ""
    registrado_por: str = ""
    posicion_x: Optional[float] = None
    posicion_y: Optional[float] = None
    color_hex: str = "#FFFFFF"
    
    # Información relacionada
    diente_numero: int = 0
    diente_nombre: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CondicionDienteModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # Procesar datos del diente relacionado
        diente_data = data.get("dientes", {})
        
        return cls(
            id=str(data.get("id", "")),
            odontograma_id=str(data.get("odontograma_id", "")),
            diente_id=str(data.get("diente_id", "")),
            tipo_condicion=str(data.get("tipo_condicion", "")),
            caras_afectadas=data.get("caras_afectadas", []),
            severidad=str(data.get("severidad", "leve")),
            descripcion=str(data.get("descripcion", "") if data.get("descripcion") else ""),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            material_utilizado=str(data.get("material_utilizado", "") if data.get("material_utilizado") else ""),
            color_material=str(data.get("color_material", "") if data.get("color_material") else ""),
            fecha_tratamiento=str(data.get("fecha_tratamiento", "") if data.get("fecha_tratamiento") else ""),
            estado=str(data.get("estado", "actual")),
            requiere_seguimiento=bool(data.get("requiere_seguimiento", False)),
            fecha_registro=str(data.get("fecha_registro", "")),
            registrado_por=str(data.get("registrado_por", "")),
            posicion_x=float(data.get("posicion_x")) if data.get("posicion_x") else None,
            posicion_y=float(data.get("posicion_y")) if data.get("posicion_y") else None,
            color_hex=str(data.get("color_hex", "#FFFFFF")),
            diente_numero=int(diente_data.get("numero_diente", 0)) if diente_data else 0,
            diente_nombre=str(diente_data.get("nombre", "")) if diente_data else ""
        )
    
    @property
    def tipo_condicion_display(self) -> str:
        """Tipo de condición formateado con emoji"""
        condiciones_map = {
            "sano": "✅ Sano",
            "caries": "🦠 Caries",
            "obturacion": "🔧 Obturación",
            "corona": "👑 Corona",
            "puente": "🌉 Puente",
            "implante": "🔩 Implante",
            "ausente": "❌ Ausente",
            "extraccion_indicada": "⚠️ Extracción Indicada",
            "endodoncia": "🦷 Endodoncia",
            "protesis": "🦾 Prótesis",
            "fractura": "💥 Fractura",
            "mancha": "🟤 Mancha",
            "desgaste": "📉 Desgaste",
            "sensibilidad": "⚡ Sensibilidad",
            "movilidad": "↔️ Movilidad",
            "impactado": "🧱 Impactado",
            "en_erupcion": "🌱 En Erupción",
            "retenido": "🔒 Retenido",
            "supernumerario": "➕ Supernumerario",
            "otro": "❓ Otro"
        }
        return condiciones_map.get(self.tipo_condicion.lower(), self.tipo_condicion.title())
    
    @property
    def severidad_display(self) -> str:
        """Severidad formateada con color"""
        severidades_map = {
            "leve": "🟢 Leve",
            "moderada": "🟡 Moderada",
            "severa": "🔴 Severa"
        }
        return severidades_map.get(self.severidad.lower(), self.severidad.title())
    
    @property
    def caras_display(self) -> str:
        """Caras afectadas formateadas"""
        if self.caras_afectadas:
            caras_map = {
                "oclusal": "O",
                "mesial": "M",
                "distal": "D",
                "vestibular": "V",
                "lingual": "L"
            }
            caras_abrev = [caras_map.get(cara, cara[0].upper()) for cara in self.caras_afectadas]
            return "-".join(caras_abrev)
        return "Todas"
    
    @property
    def color_condicion(self) -> str:
        """Color según el tipo de condición"""
        colores_condicion = {
            "sano": "#90EE90",           # Verde claro
            "caries": "#FF6B6B",         # Rojo
            "obturacion": "#4ECDC4",     # Turquesa
            "corona": "#FFD93D",         # Dorado
            "puente": "#6BCF7F",         # Verde
            "implante": "#95A5A6",       # Gris
            "ausente": "#FFFFFF",        # Blanco
            "extraccion_indicada": "#E74C3C",  # Rojo fuerte
            "endodoncia": "#F39C12",     # Naranja
            "protesis": "#9B59B6",       # Púrpura
            "fractura": "#E67E22",       # Naranja oscuro
            "mancha": "#8D6E63",         # Marrón
            "desgaste": "#BDC3C7",       # Gris claro
            "sensibilidad": "#F1C40F",   # Amarillo
            "movilidad": "#FF8C00",      # Naranja
            "otro": "#AED6F1"            # Azul claro
        }
        return self.color_hex if self.color_hex != "#FFFFFF" else colores_condicion.get(self.tipo_condicion.lower(), "#FFFFFF")


class HistorialClinicoModel(rx.Base):
    """Modelo para historial médico dental detallado"""
    id: Optional[str] = ""
    paciente_id: str = ""
    consulta_id: Optional[str] = ""
    odontologo_id: str = ""
    fecha_registro: str = ""
    tipo_registro: str = "consulta"  # consulta, tratamiento, control, urgencia, nota
    sintomas_principales: Optional[str] = ""
    examen_clinico: Optional[str] = ""
    diagnostico_principal: Optional[str] = ""
    diagnosticos_secundarios: List[str] = []
    plan_tratamiento: Optional[str] = ""
    pronostico: Optional[str] = ""
    medicamentos_recetados: List[Dict[str, Any]] = []
    recomendaciones: Optional[str] = ""
    contraindicaciones: Optional[str] = ""
    presion_arterial: Optional[str] = ""
    frecuencia_cardiaca: Optional[int] = None
    temperatura: Optional[float] = None
    imagenes_url: List[str] = []
    documentos_url: List[str] = []
    proxima_cita: Optional[str] = ""
    observaciones: Optional[str] = ""
    confidencial: bool = False
    
    # Información relacionada
    paciente_nombre: str = ""
    odontologo_nombre: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistorialClinicoModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            paciente_id=str(data.get("paciente_id", "")),
            consulta_id=str(data.get("consulta_id", "") if data.get("consulta_id") else ""),
            odontologo_id=str(data.get("odontologo_id", "")),
            fecha_registro=str(data.get("fecha_registro", "")),
            tipo_registro=str(data.get("tipo_registro", "consulta")),
            sintomas_principales=str(data.get("sintomas_principales", "") if data.get("sintomas_principales") else ""),
            examen_clinico=str(data.get("examen_clinico", "") if data.get("examen_clinico") else ""),
            diagnostico_principal=str(data.get("diagnostico_principal", "") if data.get("diagnostico_principal") else ""),
            diagnosticos_secundarios=data.get("diagnosticos_secundarios", []),
            plan_tratamiento=str(data.get("plan_tratamiento", "") if data.get("plan_tratamiento") else ""),
            pronostico=str(data.get("pronostico", "") if data.get("pronostico") else ""),
            medicamentos_recetados=data.get("medicamentos_recetados", []),
            recomendaciones=str(data.get("recomendaciones", "") if data.get("recomendaciones") else ""),
            contraindicaciones=str(data.get("contraindicaciones", "") if data.get("contraindicaciones") else ""),
            presion_arterial=str(data.get("presion_arterial", "") if data.get("presion_arterial") else ""),
            frecuencia_cardiaca=int(data.get("frecuencia_cardiaca")) if data.get("frecuencia_cardiaca") else None,
            temperatura=float(data.get("temperatura")) if data.get("temperatura") else None,
            imagenes_url=data.get("imagenes_url", []),
            documentos_url=data.get("documentos_url", []),
            proxima_cita=str(data.get("proxima_cita", "") if data.get("proxima_cita") else ""),
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            confidencial=bool(data.get("confidencial", False)),
            paciente_nombre=str(data.get("paciente_nombre", "")),
            odontologo_nombre=str(data.get("odontologo_nombre", ""))
        )
    
    @property
    def tipo_registro_display(self) -> str:
        """Tipo de registro formateado"""
        tipos_map = {
            "consulta": "🏥 Consulta",
            "tratamiento": "🔧 Tratamiento",
            "control": "👁️ Control",
            "urgencia": "🚨 Urgencia",
            "nota": "📝 Nota"
        }
        return tipos_map.get(self.tipo_registro, self.tipo_registro.title())
    
    @property
    def signos_vitales_display(self) -> List[str]:
        """Signos vitales formateados"""
        signos = []
        if self.presion_arterial:
            signos.append(f"PA: {self.presion_arterial}")
        if self.frecuencia_cardiaca:
            signos.append(f"FC: {self.frecuencia_cardiaca} bpm")
        if self.temperatura:
            signos.append(f"T°: {self.temperatura}°C")
        return signos
    
    @property
    def medicamentos_display(self) -> str:
        """Medicamentos recetados formateados"""
        if self.medicamentos_recetados:
            medicamentos = []
            for med in self.medicamentos_recetados:
                if isinstance(med, dict):
                    nombre = med.get("nombre", "")
                    dosis = med.get("dosis", "")
                    medicamentos.append(f"{nombre} - {dosis}")
                else:
                    medicamentos.append(str(med))
            return "; ".join(medicamentos)
        return "Ninguno"


class PlanTratamientoModel(rx.Base):
    """Modelo para planes de tratamiento personalizados"""
    id: str = ""
    paciente_id: str = ""
    odontologo_id: str = ""
    fecha_creacion: str = ""
    estado_plan: str = "propuesto"  # propuesto, aceptado, en_curso, completado, cancelado
    prioridad: str = "normal"       # baja, normal, alta, urgente
    
    # Descripción del plan
    titulo: str = ""
    descripcion_general: str = ""
    objetivo_tratamiento: str = ""
    duracion_estimada: str = ""     # Ej: "3 meses", "6 sesiones"
    costo_estimado: float = 0.0
    
    # Fases del tratamiento
    fases_tratamiento: List[Dict[str, Any]] = []
    
    # Seguimiento
    fecha_inicio: Optional[str] = ""
    fecha_finalizacion: Optional[str] = ""
    progreso_actual: int = 0         # Porcentaje 0-100
    observaciones_progreso: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlanTratamientoModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            paciente_id=str(data.get("paciente_id", "")),
            odontologo_id=str(data.get("odontologo_id", "")),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            estado_plan=str(data.get("estado_plan", "propuesto")),
            prioridad=str(data.get("prioridad", "normal")),
            titulo=str(data.get("titulo", "")),
            descripcion_general=str(data.get("descripcion_general", "")),
            objetivo_tratamiento=str(data.get("objetivo_tratamiento", "")),
            duracion_estimada=str(data.get("duracion_estimada", "")),
            costo_estimado=float(data.get("costo_estimado", 0)),
            fases_tratamiento=data.get("fases_tratamiento", []),
            fecha_inicio=str(data.get("fecha_inicio", "") if data.get("fecha_inicio") else ""),
            fecha_finalizacion=str(data.get("fecha_finalizacion", "") if data.get("fecha_finalizacion") else ""),
            progreso_actual=int(data.get("progreso_actual", 0)),
            observaciones_progreso=str(data.get("observaciones_progreso", ""))
        )
    
    @property
    def estado_display(self) -> str:
        """Estado del plan formateado"""
        estados_map = {
            "propuesto": "📋 Propuesto",
            "aceptado": "✅ Aceptado",
            "en_curso": "🔄 En Curso",
            "completado": "🏆 Completado",
            "cancelado": "❌ Cancelado"
        }
        return estados_map.get(self.estado_plan, self.estado_plan.title())
    
    @property
    def progreso_display(self) -> str:
        """Progreso formateado"""
        return f"{self.progreso_actual}%"