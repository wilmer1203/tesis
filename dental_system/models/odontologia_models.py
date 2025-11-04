"""
Modelos de datos para el módulo de ODONTOLOGÍA
Centraliza todos los modelos relacionados con atención odontológica especializada
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class OdontogramaModel(rx.Base):
    """🦷 Modelo avanzado para odontogramas con versionado automático"""
    id: Optional[str] = None
    numero_historia: str = ""  # ← NUEVO: Link directo a paciente por HC
    version: int = 1           # ← MEJORADO: Versionado automático
    id_version_anterior: Optional[str] = None  # ← NUEVO: Historial de versiones
    id_intervencion_origen: Optional[str] = None  # ← NUEVO: Trazabilidad
    es_version_actual: bool = True             # ← NUEVO: Control de versión activa
    motivo_nueva_version: Optional[str] = ""  # ← NUEVO: Razón del cambio
    
    # Campos existentes mejorados
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""
    odontologo_id: str = ""
    tipo_odontograma: str = "adulto"  # adulto, pediatrico, mixto
    notas_generales: Optional[str] = ""
    observaciones_clinicas: Optional[str] = ""
    template_usado: str = "universal"
    configuracion: Dict[str, Any] = {}
    
    # Estados de dientes usando catálogo FDI
    dientes_estados: Dict[int, Dict[str, str]] = {}  # {numero_fdi: {condicion: estado}}
    
    # Información relacionada
    paciente_nombre: str = ""
    odontologo_nombre: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OdontogramaModel":
        """🔄 Crear instancia desde diccionario con esquema avanzado"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")) if data.get("id") else None,
            numero_historia=str(data.get("numero_historia", "")),
            version=int(data.get("version", 1)),
            id_version_anterior=str(data.get("id_version_anterior", "")) if data.get("id_version_anterior") else None,
            id_intervencion_origen=str(data.get("id_intervencion_origen", "")) if data.get("id_intervencion_origen") else None,
            es_version_actual=bool(data.get("es_version_actual", True)),
            motivo_nueva_version=str(data.get("motivo_nueva_version", "") if data.get("motivo_nueva_version") else ""),
            fecha_creacion=str(data.get("fecha_creacion", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            odontologo_id=str(data.get("odontologo_id", "")),
            tipo_odontograma=str(data.get("tipo_odontograma", "adulto")),
            notas_generales=str(data.get("notas_generales", "") if data.get("notas_generales") else ""),
            observaciones_clinicas=str(data.get("observaciones_clinicas", "") if data.get("observaciones_clinicas") else ""),
            template_usado=str(data.get("template_usado", "universal")),
            configuracion=data.get("configuracion", {}),
            dientes_estados=data.get("dientes_estados", {}),
            paciente_nombre=str(data.get("paciente_nombre", "")),
            odontologo_nombre=str(data.get("odontologo_nombre", ""))
        )
    



# ==========================================
# 📝 FORMULARIOS DE ODONTOLOGÍA
# ==========================================

class IntervencionFormModel(rx.Base):
    """
    📝 FORMULARIO DE INTERVENCIÓN ODONTOLÓGICA
    
    Usado en: odontologia_service para intervenciones
    """
    
    # Referencias
    consulta_id: str = ""
    servicio_id: str = ""
    odontologo_id: str = ""
    asistente_id: str = ""
    
    # Detalles clínicos
    diagnostico_inicial: str = ""
    procedimiento_realizado: str = ""
    dientes_afectados: str = ""  # Lista separada por comas
    
    # Materiales y anestesia
    materiales_utilizados: str = ""
    anestesia_utilizada: str = ""
    
    # Precio y seguimiento
    precio_acordado: str = "0"
    descuento: str = "0"
    precio_final: str = "0"
    
    # Control
    requiere_control: bool = False
    fecha_control_sugerida: str = ""
    instrucciones_paciente: str = ""
    
    # Observaciones
    complicaciones: str = ""
    observaciones: str = ""
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos de intervención"""
        errors = {}
        
        if not self.consulta_id.strip():
            errors.setdefault("consulta_id", []).append("Consulta es requerida")
        
        if not self.servicio_id.strip():
            errors.setdefault("servicio_id", []).append("Servicio es requerido")
        
        if not self.odontologo_id.strip():
            errors.setdefault("odontologo_id", []).append("Odontólogo es requerido")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a dict - Any porque puede contener listas"""
        return {
            "consulta_id": self.consulta_id,
            "servicio_id": self.servicio_id,
            "odontologo_id": self.odontologo_id,
            "asistente_id": self.asistente_id,
            "diagnostico_inicial": self.diagnostico_inicial,
            "procedimiento_realizado": self.procedimiento_realizado,
            "dientes_afectados": self.dientes_afectados,
            "materiales_utilizados": self.materiales_utilizados,
            "anestesia_utilizada": self.anestesia_utilizada,
            "precio_acordado": self.precio_acordado,
            "descuento": self.descuento,
            "precio_final": self.precio_final,
            "requiere_control": self.requiere_control,
            "fecha_control_sugerida": self.fecha_control_sugerida,
            "instrucciones_paciente": self.instrucciones_paciente,
            "complicaciones": self.complicaciones,
            "observaciones": self.observaciones,
        }


class HistorialMedicoModel(rx.Base):
    """📋 Modelo para historial médico inicial y evolución del paciente"""
    id: Optional[str] = None
    paciente_id: str = ""
    consulta_id: Optional[str] = ""
    intervencion_id: Optional[str] = ""
    odontologo_id: str = ""

    # Tipo de registro
    tipo_registro: str = "inicial"  # inicial, consulta, tratamiento, control, urgencia, nota

    # Información clínica principal
    sintomas_principales: str = ""
    examen_clinico: str = ""
    diagnostico_principal: str = ""
    diagnosticos_secundarios: List[str] = []
    plan_tratamiento: str = ""
    pronostico: str = ""

    # Medicamentos y recomendaciones
    medicamentos_recetados: List[Dict[str, Any]] = []
    recomendaciones: str = ""
    contraindicaciones: str = ""

    # Signos vitales (opcional)
    presion_arterial: Optional[str] = ""
    frecuencia_cardiaca: Optional[int] = None
    temperatura: Optional[float] = None

    # Archivos adjuntos
    imagenes_url: List[str] = []
    documentos_url: List[str] = []

    # Seguimiento
    proxima_consulta: Optional[str] = ""
    observaciones: str = ""
    confidencial: bool = False

    # Control del sistema
    fecha_registro: str = ""
    fecha_actualizacion: str = ""
    registrado_por: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistorialMedicoModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()

        return cls(
            id=str(data.get("id", "")) if data.get("id") else None,
            paciente_id=str(data.get("paciente_id", "")),
            consulta_id=str(data.get("consulta_id", "") if data.get("consulta_id") else ""),
            intervencion_id=str(data.get("intervencion_id", "") if data.get("intervencion_id") else ""),
            odontologo_id=str(data.get("odontologo_id", "")),

            tipo_registro=str(data.get("tipo_registro", "inicial")),

            sintomas_principales=str(data.get("sintomas_principales", "")),
            examen_clinico=str(data.get("examen_clinico", "")),
            diagnostico_principal=str(data.get("diagnostico_principal", "")),
            diagnosticos_secundarios=data.get("diagnosticos_secundarios", []) if isinstance(data.get("diagnosticos_secundarios"), list) else [],
            plan_tratamiento=str(data.get("plan_tratamiento", "")),
            pronostico=str(data.get("pronostico", "")),

            medicamentos_recetados=data.get("medicamentos_recetados", []) if isinstance(data.get("medicamentos_recetados"), list) else [],
            recomendaciones=str(data.get("recomendaciones", "")),
            contraindicaciones=str(data.get("contraindicaciones", "")),

            presion_arterial=str(data.get("presion_arterial", "") if data.get("presion_arterial") else ""),
            frecuencia_cardiaca=data.get("frecuencia_cardiaca") if isinstance(data.get("frecuencia_cardiaca"), int) else None,
            temperatura=data.get("temperatura") if isinstance(data.get("temperatura"), (int, float)) else None,

            imagenes_url=data.get("imagenes_url", []) if isinstance(data.get("imagenes_url"), list) else [],
            documentos_url=data.get("documentos_url", []) if isinstance(data.get("documentos_url"), list) else [],

            proxima_consulta=str(data.get("proxima_consulta", "") if data.get("proxima_consulta") else ""),
            observaciones=str(data.get("observaciones", "")),
            confidencial=bool(data.get("confidencial", False)),

            fecha_registro=str(data.get("fecha_registro", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            registrado_por=str(data.get("registrado_por", ""))
        )

class HistorialServicioModel(rx.Base):
    """
    Usado en: patient_history_section para mostrar servicios previos
    """
    id: str = ""
    fecha: str = ""
    odontologo_nombre: str = ""
    especialidad: str = ""
    diente_numero: Optional[int] = None
    diente_nombre: str = ""
    superficies: List[str] = []
    superficies_texto: str = ""
    alcance: str = ""
    servicio_nombre: str = ""
    servicio_categoria: str = ""
    condicion_aplicada: Optional[str] = None
    material_utilizado: Optional[str] = None
    observaciones: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistorialServicioModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()

        return cls(
            id=str(data.get("id", "")),
            fecha=str(data.get("fecha", "")),
            odontologo_nombre=str(data.get("odontologo_nombre", "")),
            especialidad=str(data.get("especialidad", "")),
            diente_numero=data.get("diente_numero"),
            diente_nombre=str(data.get("diente_nombre", "")),
            superficies=data.get("superficies", []),
            superficies_texto=str(data.get("superficies_texto", "")),
            alcance=str(data.get("alcance", "")),
            servicio_nombre=str(data.get("servicio_nombre", "")),
            servicio_categoria=str(data.get("servicio_categoria", "")),
            condicion_aplicada=data.get("condicion_aplicada"),
            material_utilizado=data.get("material_utilizado"),
            observaciones=str(data.get("observaciones", ""))
        )

class ActualizacionOdontogramaResult(rx.Base):
    """
    📊 Resultado de actualización batch del odontograma (V3.0)

    Modelo que encapsula el resultado de actualizar múltiples
    condiciones dentales en una sola operación transaccional.

    Usado en:
    - Retorno de _actualizar_odontograma_por_servicios()
    - Validación de éxito/fallos de actualizaciones
    - Logging y debugging de operaciones batch
    """

    # Contadores
    exitosos: int = 0  # Número de actualizaciones exitosas
    fallidos: int = 0  # Número de actualizaciones fallidas

    # Detalles
    advertencias: List[str] = []  # Advertencias durante el proceso
    ids_creados: List[str] = []  # IDs de las nuevas condiciones creadas

    @property
    def total(self) -> int:
        """Total de actualizaciones intentadas"""
        return self.exitosos + self.fallidos

    @property
    def porcentaje_exito(self) -> float:
        """Porcentaje de actualizaciones exitosas"""
        if self.total == 0:
            return 0.0
        return (self.exitosos / self.total) * 100.0

    @property
    def tuvo_errores(self) -> bool:
        """¿Hubo errores durante la actualización?"""
        return self.fallidos > 0

    @property
    def resultado_display(self) -> str:
        """Resumen formateado del resultado"""
        if self.total == 0:
            return "⚪ Sin actualizaciones"

        if not self.tuvo_errores:
            return f"✅ {self.exitosos} actualizaciones exitosas"

        return f"⚠️ {self.exitosos} exitosas, {self.fallidos} fallidas ({self.porcentaje_exito:.1f}% éxito)"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActualizacionOdontogramaResult":
        """Crear instancia desde resultado de BD"""
        if not data or not isinstance(data, dict):
            return cls()

        return cls(
            exitosos=int(data.get("exitosos", 0)),
            fallidos=int(data.get("fallidos", 0)),
            advertencias=data.get("advertencias", []),
            ids_creados=[str(id) for id in data.get("ids_creados", [])]
        )