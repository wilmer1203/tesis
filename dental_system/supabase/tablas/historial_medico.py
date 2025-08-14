"""
Operaciones CRUD para la tabla historial_medico
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class MedicalHistoryTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla historial_medico
    """
    
    def __init__(self):
        super().__init__('historial_medico')
    
    @handle_supabase_error
    def create_medical_record(self,
                            paciente_id: str,
                            odontologo_id: str,
                            tipo_registro: str = 'consulta',
                            consulta_id: Optional[str] = None,
                            sintomas_principales: Optional[str] = None,
                            examen_clinico: Optional[str] = None,
                            diagnostico_principal: Optional[str] = None,
                            diagnosticos_secundarios: Optional[List[str]] = None,
                            plan_tratamiento: Optional[str] = None,
                            pronostico: Optional[str] = None,
                            medicamentos_recetados: Optional[List[Dict[str, Any]]] = None,
                            recomendaciones: Optional[str] = None,
                            contraindicaciones: Optional[str] = None,
                            presion_arterial: Optional[str] = None,
                            frecuencia_cardiaca: Optional[int] = None,
                            temperatura: Optional[float] = None,
                            imagenes_url: Optional[List[str]] = None,
                            documentos_url: Optional[List[str]] = None,
                            proxima_cita: Optional[date] = None,
                            observaciones: Optional[str] = None,
                            confidencial: bool = False) -> Dict[str, Any]:
        """
        Crea un nuevo registro en el historial médico
        
        Args:
            paciente_id: ID del paciente
            odontologo_id: ID del odontólogo
            tipo_registro: Tipo (consulta, tratamiento, control, urgencia, nota)
            consulta_id: ID de la consulta relacionada (opcional)
            sintomas_principales: Síntomas reportados
            examen_clinico: Resultados del examen clínico
            diagnostico_principal: Diagnóstico principal
            diagnosticos_secundarios: Lista de diagnósticos secundarios
            plan_tratamiento: Plan de tratamiento propuesto
            pronostico: Pronóstico del caso
            medicamentos_recetados: Lista de medicamentos [{nombre, dosis, frecuencia, duracion}]
            recomendaciones: Recomendaciones al paciente
            contraindicaciones: Contraindicaciones identificadas
            presion_arterial: Presión arterial (ej: "120/80")
            frecuencia_cardiaca: Frecuencia cardíaca
            temperatura: Temperatura corporal
            imagenes_url: URLs de imágenes adjuntas
            documentos_url: URLs de documentos adjuntos
            proxima_cita: Fecha sugerida para próxima cita
            observaciones: Observaciones adicionales
            confidencial: Si el registro es confidencial
            
        Returns:
            Registro médico creado
        """
        data = {
            "paciente_id": paciente_id,
            "odontologo_id": odontologo_id,
            "tipo_registro": tipo_registro,
            "confidencial": confidencial
        }
        
        # Agregar campos opcionales
        if consulta_id:
            data["consulta_id"] = consulta_id
        if sintomas_principales:
            data["sintomas_principales"] = sintomas_principales
        if examen_clinico:
            data["examen_clinico"] = examen_clinico
        if diagnostico_principal:
            data["diagnostico_principal"] = diagnostico_principal
        if diagnosticos_secundarios:
            data["diagnosticos_secundarios"] = diagnosticos_secundarios
        if plan_tratamiento:
            data["plan_tratamiento"] = plan_tratamiento
        if pronostico:
            data["pronostico"] = pronostico
        if medicamentos_recetados:
            data["medicamentos_recetados"] = medicamentos_recetados
        if recomendaciones:
            data["recomendaciones"] = recomendaciones
        if contraindicaciones:
            data["contraindicaciones"] = contraindicaciones
        if presion_arterial:
            data["presion_arterial"] = presion_arterial
        if frecuencia_cardiaca:
            data["frecuencia_cardiaca"] = frecuencia_cardiaca
        if temperatura:
            data["temperatura"] = temperatura
        if imagenes_url:
            data["imagenes_url"] = imagenes_url
        if documentos_url:
            data["documentos_url"] = documentos_url
        if proxima_cita:
            data["proxima_cita"] = proxima_cita.isoformat()
        if observaciones:
            data["observaciones"] = observaciones
        
        logger.info(f"Creando registro médico para paciente {paciente_id}")
        return self.create(data)
    
    @handle_supabase_error
    def get_patient_history(self, 
                          paciente_id: str,
                          incluir_confidencial: bool = False,
                          tipo_registro: Optional[str] = None,
                          limite: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtiene el historial médico completo de un paciente
        
        Args:
            paciente_id: ID del paciente
            incluir_confidencial: Si incluir registros confidenciales
            tipo_registro: Filtrar por tipo de registro
            limite: Límite de registros a retornar
            
        Returns:
            Lista de registros médicos del paciente
        """
        query = self.table.select("""
            *,
            odontologo:personal!odontologo_id(
                usuario:usuarios!inner(nombre_completo)
            ),
            consultas(numero_consulta, fecha_programada)
        """).eq("paciente_id", paciente_id)
        
        if not incluir_confidencial:
            query = query.eq("confidencial", False)
        
        if tipo_registro:
            query = query.eq("tipo_registro", tipo_registro)
        
        query = query.order("fecha_registro", desc=True)
        
        if limite:
            query = query.limit(limite)
        
        response = query.execute()
        return response.data
    
    @handle_supabase_error
    def get_record_details(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un registro médico con información completa
        
        Args:
            record_id: ID del registro
            
        Returns:
            Registro con información expandida
        """
        response = self.table.select("""
            *,
            pacientes!inner(
                id, numero_historia, nombre_completo,
                fecha_nacimiento, alergias, medicamentos_actuales,
                condiciones_medicas
            ),
            odontologo:personal!odontologo_id(
                usuario:usuarios!inner(nombre_completo, email)
            ),
            consultas(
                numero_consulta, fecha_programada,
                intervenciones(
                    servicios(nombre, categoria),
                    procedimiento_realizado
                )
            )
        """).eq("id", record_id).execute()
        
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_latest_diagnosis(self, paciente_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el diagnóstico más reciente de un paciente
        
        Args:
            paciente_id: ID del paciente
            
        Returns:
            Último registro con diagnóstico
        """
        response = self.table.select("""
            *,
            odontologo:personal!odontologo_id(
                usuario:usuarios!inner(nombre_completo)
            )
        """).eq("paciente_id", paciente_id
        ).not_.is_("diagnostico_principal", None
        ).order("fecha_registro", desc=True
        ).limit(1).execute()
        
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_prescriptions(self, 
                         paciente_id: str,
                         activas_solo: bool = True) -> List[Dict[str, Any]]:
        """
        Obtiene las prescripciones médicas de un paciente
        
        Args:
            paciente_id: ID del paciente
            activas_solo: Si solo obtener prescripciones activas
            
        Returns:
            Lista de registros con prescripciones
        """
        query = self.table.select("""
            id, fecha_registro, medicamentos_recetados, 
            odontologo:personal!odontologo_id(
                usuario:usuarios!inner(nombre_completo)
            )
        """).eq("paciente_id", paciente_id
        ).not_.is_("medicamentos_recetados", None
        ).order("fecha_registro", desc=True)
        
        response = query.execute()
        registros = response.data
        
        if activas_solo:
            # Filtrar prescripciones activas basándose en la duración
            registros_activos = []
            fecha_actual = datetime.now()
            
            for registro in registros:
                medicamentos_activos = []
                
                for med in registro.get("medicamentos_recetados", []):
                    # Verificar si el medicamento aún está activo
                    fecha_inicio = datetime.fromisoformat(registro["fecha_registro"].replace('Z', '+00:00'))
                    duracion_dias = med.get("duracion_dias", 0)
                    
                    if duracion_dias > 0:
                        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
                        if fecha_actual <= fecha_fin:
                            medicamentos_activos.append(med)
                
                if medicamentos_activos:
                    registro["medicamentos_recetados"] = medicamentos_activos
                    registros_activos.append(registro)
            
            return registros_activos
        
        return registros
    
    @handle_supabase_error
    def add_clinical_note(self,
                         paciente_id: str,
                         odontologo_id: str,
                         nota: str,
                         confidencial: bool = False) -> Dict[str, Any]:
        """
        Agrega una nota clínica rápida
        
        Args:
            paciente_id: ID del paciente
            odontologo_id: ID del odontólogo
            nota: Contenido de la nota
            confidencial: Si la nota es confidencial
            
        Returns:
            Nota creada
        """
        return self.create_medical_record(
            paciente_id=paciente_id,
            odontologo_id=odontologo_id,
            tipo_registro='nota',
            observaciones=nota,
            confidencial=confidencial
        )
    
    @handle_supabase_error
    def search_in_history(self, 
                         paciente_id: str,
                         termino_busqueda: str) -> List[Dict[str, Any]]:
        """
        Busca un término en el historial médico de un paciente
        
        Args:
            paciente_id: ID del paciente
            termino_busqueda: Término a buscar
            
        Returns:
            Registros que contienen el término
        """
        # Obtener todo el historial del paciente
        historial = self.get_patient_history(paciente_id, incluir_confidencial=False)
        
        # Buscar el término en varios campos
        resultados = []
        campos_busqueda = [
            'sintomas_principales', 'examen_clinico', 'diagnostico_principal',
            'plan_tratamiento', 'recomendaciones', 'observaciones'
        ]
        
        termino_lower = termino_busqueda.lower()
        
        for registro in historial:
            encontrado = False
            
            # Buscar en campos de texto
            for campo in campos_busqueda:
                if registro.get(campo) and termino_lower in registro[campo].lower():
                    encontrado = True
                    break
            
            # Buscar en diagnósticos secundarios
            if not encontrado and registro.get('diagnosticos_secundarios'):
                for diag in registro['diagnosticos_secundarios']:
                    if termino_lower in diag.lower():
                        encontrado = True
                        break
            
            # Buscar en medicamentos
            if not encontrado and registro.get('medicamentos_recetados'):
                for med in registro['medicamentos_recetados']:
                    if termino_lower in med.get('nombre', '').lower():
                        encontrado = True
                        break
            
            if encontrado:
                resultados.append(registro)
        
        return resultados
    
    @handle_supabase_error
    def get_treatment_timeline(self, paciente_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene línea de tiempo de tratamientos del paciente
        
        Args:
            paciente_id: ID del paciente
            
        Returns:
            Lista cronológica de tratamientos
        """
        # Obtener registros de tipo tratamiento
        registros = self.get_patient_history(
            paciente_id=paciente_id,
            tipo_registro='tratamiento'
        )
        
        # También obtener intervenciones
        consultas_response = self.client.table("consultas").select(
            "id"
        ).eq("paciente_id", paciente_id).execute()
        
        consulta_ids = [c["id"] for c in consultas_response.data]
        
        if consulta_ids:
            intervenciones_response = self.client.table("intervenciones").select("""
                *,
                servicios(nombre, categoria),
                consultas(fecha_programada)
            """).in_("consulta_id", consulta_ids
            ).order("hora_inicio", desc=True).execute()
            
            # Combinar registros e intervenciones en línea de tiempo
            timeline = []
            
            # Agregar registros médicos
            for registro in registros:
                timeline.append({
                    "tipo": "registro_medico",
                    "fecha": registro["fecha_registro"],
                    "descripcion": registro.get("plan_tratamiento", "Tratamiento registrado"),
                    "odontologo": registro["odontologo"]["usuario"]["nombre_completo"],
                    "detalles": registro
                })
            
            # Agregar intervenciones
            for intervencion in intervenciones_response.data:
                if intervencion["estado"] == "completada":
                    timeline.append({
                        "tipo": "intervencion",
                        "fecha": intervencion["hora_inicio"],
                        "descripcion": f"{intervencion['servicios']['nombre']} - {intervencion['procedimiento_realizado']}",
                        "odontologo": "N/A",  # Necesitaría join adicional
                        "detalles": intervencion
                    })
            
            # Ordenar por fecha
            timeline.sort(key=lambda x: x["fecha"], reverse=True)
            
            return timeline
        
        return []
    
    @handle_supabase_error
    def mark_as_confidential(self, record_id: str) -> Dict[str, Any]:
        """
        Marca un registro como confidencial
        
        Args:
            record_id: ID del registro
            
        Returns:
            Registro actualizado
        """
        return self.update(record_id, {"confidencial": True})
    
    @handle_supabase_error
    def get_vital_signs_history(self, 
                              paciente_id: str,
                              limite: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene historial de signos vitales
        
        Args:
            paciente_id: ID del paciente
            limite: Número de registros a obtener
            
        Returns:
            Lista de registros con signos vitales
        """
        response = self.table.select(
            "fecha_registro, presion_arterial, frecuencia_cardiaca, temperatura"
        ).eq("paciente_id", paciente_id
        ).or_(
            "presion_arterial.not.is.null,"
            "frecuencia_cardiaca.not.is.null,"
            "temperatura.not.is.null"
        ).order("fecha_registro", desc=True
        ).limit(limite).execute()
        
        return response.data


# Instancia única para importar
historial_medico_table = MedicalHistoryTable()

# Alias para compatibilidad
HistorialMedicoTable = MedicalHistoryTable
    