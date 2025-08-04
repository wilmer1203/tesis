"""
Preprocesadores de datos para el sistema genérico de tablas
dental_system/utils/data_preprocessors.py

Estas funciones transforman los datos RAW de la base de datos 
en formatos listos para mostrar, evitando transformaciones de texto sobre Vars.
"""

from typing import Dict, List, Any
from datetime import datetime

def preprocess_patients_data(raw_patients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Preprocesa datos de pacientes para la tabla
    Hace todas las transformaciones de texto ANTES de pasarlos a Reflex
    """
    processed_data = []
    
    for patient in raw_patients:
        if isinstance(patient, dict):
            # Crear nombre completo
            nombre_completo = f"{patient.get('primer_nombre', '')} {patient.get('primer_apellido', '')}".strip()
            
            # Formatear fecha de registro
            fecha_registro = patient.get('fecha_registro', '')
            fecha_formateada = ""
            if fecha_registro:
                try:
                    dt = datetime.fromisoformat(fecha_registro.replace('Z', '+00:00'))
                    fecha_formateada = dt.strftime('%d/%m/%Y')
                except:
                    fecha_formateada = fecha_registro
            
            # Formatear género para mostrar
            genero = patient.get('genero', '')
            genero_display = {
                'masculino': 'Masculino',
                'femenino': 'Femenino', 
                'otro': 'Otro'
            }.get(genero, genero.title() if genero else '')
            
            # Estado como texto legible
            activo = patient.get('activo', True)
            estado_display = "Activo" if activo else "Inactivo"
            
            processed_data.append({
                "id": patient.get("id", ""),
                "nombre_completo": nombre_completo,
                "numero_historia": patient.get("numero_historia", ""),
                "numero_documento": patient.get("numero_documento", ""),
                "telefono_1": patient.get("telefono_1", ""),
                "fecha_registro": fecha_formateada,
                "fecha_registro_raw": patient.get('fecha_registro', ''),  # Para ordenamiento
                "activo": activo,  # Boolean para lógica
                "estado_display": estado_display,  # String para mostrar
                "genero": genero,  # Valor original para filtros
                "genero_display": genero_display,  # Texto para mostrar
                # Datos adicionales para acciones
                "primer_nombre": patient.get("primer_nombre", ""),
                "primer_apellido": patient.get("primer_apellido", ""),
            })
    
    return processed_data

def preprocess_staff_data(raw_staff: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Preprocesa datos de personal para la tabla
    """
    processed_data = []
    
    for staff in raw_staff:
        if isinstance(staff, dict):
            # Crear nombre completo
            nombre_completo = f"{staff.get('primer_nombre', '')} {staff.get('primer_apellido', '')}".strip()
            
            # Formatear tipo de personal para mostrar
            tipo_personal = staff.get('tipo_personal', '')
            tipo_display = {
                'odontologo': 'Odontólogo',
                'administrador': 'Administrador',
                'asistente': 'Asistente',
                'recepcionista': 'Recepcionista'
            }.get(tipo_personal, tipo_personal.replace('_', ' ').title())
            
            # Formatear estado laboral para mostrar
            estado_laboral = staff.get('estado_laboral', '')
            estado_display = {
                'activo': 'Activo',
                'inactivo': 'Inactivo',
                'licencia': 'Licencia',
                'vacaciones': 'Vacaciones'
            }.get(estado_laboral, estado_laboral.replace('_', ' ').title())
            
            # Especialidad formateada
            especialidad = staff.get('especialidad', '')
            especialidad_display = especialidad.title() if especialidad else ''
            
            processed_data.append({
                "id": staff.get("id", ""),
                "usuario_id": staff.get("usuario_id", ""),
                "nombre_completo": nombre_completo,
                "tipo_personal": tipo_personal,  # Valor original para filtros
                "tipo_personal_display": tipo_display,  # Texto para mostrar
                "telefono": staff.get("telefono", "") or staff.get("celular", ""),
                "email": staff.get("email", ""),
                "estado_laboral": estado_laboral,  # Valor original para filtros
                "estado_laboral_display": estado_display,  # Texto para mostrar
                "especialidad": especialidad,  # Valor original
                "especialidad_display": especialidad_display,  # Texto para mostrar
                "activo": staff.get("usuario_activo", True),
                # Datos adicionales
                "primer_nombre": staff.get("primer_nombre", ""),
                "primer_apellido": staff.get("primer_apellido", ""),
            })
    
    return processed_data

def preprocess_consultations_data(raw_consultations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Preprocesa datos de consultas para la tabla
    """
    processed_data = []
    
    for consultation in raw_consultations:
        if isinstance(consultation, dict):
            # Formatear fecha programada
            fecha_programada = consultation.get('fecha_programada', '')
            fecha_formateada = ""
            if fecha_programada:
                try:
                    dt = datetime.fromisoformat(fecha_programada.replace('Z', '+00:00'))
                    fecha_formateada = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    fecha_formateada = fecha_programada
            
            # Formatear prioridad para mostrar
            prioridad = consultation.get('prioridad', 'normal')
            prioridad_display = {
                'baja': 'Baja',
                'normal': 'Normal',
                'alta': 'Alta',
                'urgente': 'Urgente'
            }.get(prioridad, prioridad.title())
            
            # Formatear estado para mostrar
            estado = consultation.get('estado', 'programada')
            estado_display = {
                'programada': 'Programada',
                'confirmada': 'Confirmada',
                'en_progreso': 'En Progreso',
                'completada': 'Completada',
                'cancelada': 'Cancelada',
                'no_asistio': 'No Asistió'
            }.get(estado, estado.replace('_', ' ').title())
            
            # Truncar motivo para mostrar en tabla
            motivo_consulta = consultation.get('motivo_consulta', '')
            motivo_truncado = motivo_consulta[:50] + "..." if len(motivo_consulta) > 50 else motivo_consulta
            
            processed_data.append({
                "id": consultation.get("id", ""),
                "numero_consulta": consultation.get("numero_consulta", ""),
                "paciente_id": consultation.get("paciente_id", ""),
                "odontologo_id": consultation.get("odontologo_id", ""),
                "paciente_nombre": consultation.get("paciente_nombre", ""),
                "odontologo_nombre": consultation.get("odontologo_nombre", ""),
                "motivo_consulta": motivo_consulta,  # Completo para tooltip
                "motivo_truncado": motivo_truncado,  # Truncado para tabla
                "prioridad": prioridad,  # Valor original para filtros
                "prioridad_display": prioridad_display,  # Texto para mostrar
                "estado": estado,  # Valor original para filtros
                "estado_display": estado_display,  # Texto para mostrar
                "fecha_programada": fecha_formateada,
                "fecha_programada_raw": consultation.get("fecha_programada", ""),  # Para ordenamiento
            })
    
    return processed_data

def preprocess_filter_values(raw_values: List[str], filter_type: str = "generic") -> List[Dict[str, str]]:
    """
    Preprocesa valores de filtros para tener tanto el valor original como el display
    
    Returns:
        Lista de diccionarios con 'value' (original) y 'display' (formateado)
    """
    processed_values = []
    
    for value in raw_values:
        if filter_type == "staff_type":
            display = {
                'odontologo': 'Odontólogo',
                'administrador': 'Administrador',
                'asistente': 'Asistente',
                'recepcionista': 'Recepcionista'
            }.get(value, value.replace('_', ' ').title())
        
        elif filter_type == "labor_status":
            display = {
                'activo': 'Activo',
                'inactivo': 'Inactivo', 
                'licencia': 'Licencia',
                'vacaciones': 'Vacaciones'
            }.get(value, value.replace('_', ' ').title())
        
        elif filter_type == "consultation_status":
            display = {
                'programada': 'Programada',
                'confirmada': 'Confirmada',
                'en_progreso': 'En Progreso',
                'completada': 'Completada',
                'cancelada': 'Cancelada',
                'no_asistio': 'No Asistió'
            }.get(value, value.replace('_', ' ').title())
        
        elif filter_type == "priority":
            display = {
                'baja': 'Baja',
                'normal': 'Normal',
                'alta': 'Alta',
                'urgente': 'Urgente'
            }.get(value, value.title())
        
        elif filter_type == "gender":
            display = {
                'masculino': 'Masculino',
                'femenino': 'Femenino',
                'otro': 'Otro'
            }.get(value, value.title())
        
        else:
            # Formateo genérico
            display = value.replace('_', ' ').title()
        
        processed_values.append({
            'value': value,  # Valor original para lógica
            'display': display  # Texto para mostrar
        })
    
    return processed_values

# Funciones de utilidad para usar en los servicios
def format_date_for_display(date_str: str) -> str:
    """Formatea una fecha ISO para mostrar"""
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y')
    except:
        return date_str

def format_datetime_for_display(datetime_str: str) -> str:
    """Formatea una fecha-hora ISO para mostrar"""
    if not datetime_str:
        return ""
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return datetime_str

def truncate_text(text: str, max_length: int = 50) -> str:
    """Trunca texto agregando '...' si es necesario"""
    if not text:
        return ""
    return text[:max_length] + "..." if len(text) > max_length else text