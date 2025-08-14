"""
Operaciones CRUD para la tabla pacientes
Siguiendo el patrón establecido por PersonalTable
"""
from typing import Dict, List, Optional, Any
from datetime import date, datetime
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class PacientesTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla pacientes
    """
    
    def __init__(self):
        super().__init__('pacientes')
    
    @handle_supabase_error
    def create_patient_complete(
        self,
        # ✅ NOMBRES SEPARADOS (requeridos)
        primer_nombre: str,
        primer_apellido: str,
        numero_documento: str,
        registrado_por: str,
        
        # ✅ NOMBRES OPCIONALES
        segundo_nombre: Optional[str] = None,
        segundo_apellido: Optional[str] = None,
        
        # Documentación y datos básicos
        tipo_documento: str = "CC",
        fecha_nacimiento: Optional[date] = None,
        genero: Optional[str] = None,
        
        # ✅ TELÉFONOS SEPARADOS
        telefono_1: Optional[str] = None,
        telefono_2: Optional[str] = None,
        
        # Contacto y ubicación
        email: Optional[str] = None,
        direccion: Optional[str] = None,
        ciudad: Optional[str] = None,
        departamento: Optional[str] = None,
        ocupacion: Optional[str] = None,
        estado_civil: Optional[str] = None,
        
        # Información médica
        alergias: Optional[List[str]] = None,
        medicamentos_actuales: Optional[List[str]] = None,
        condiciones_medicas: Optional[List[str]] = None,
        antecedentes_familiares: Optional[List[str]] = None,
        observaciones: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo paciente con información completa
        """
        print(f"[DEBUG] Creando paciente: {primer_nombre} {primer_apellido}")
        data = {
            "primer_nombre": primer_nombre.strip(),
            "primer_apellido": primer_apellido.strip(),
            "numero_documento": numero_documento.strip(),
            "registrado_por": registrado_por,
            "tipo_documento": tipo_documento,
            "activo": True
        }
        
        # Agregar campos opcionales solo si no están vacíos
        if  segundo_nombre:
            data["segundo_nombre"] = segundo_nombre.strip()       
        if segundo_apellido: 
            data["segundo_apellido"] = segundo_apellido.strip()
        if fecha_nacimiento:
            data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
        if genero and genero.strip():
            data["genero"] = genero.strip()
        if telefono_1 and telefono_1.strip():
            data["telefono_1"] = telefono_1.strip()
        if telefono_2 and telefono_2.strip():
            data["telefono_2"] = telefono_2.strip()
        if email and email.strip():
            data["email"] = email.strip().lower()
        if direccion and direccion.strip():
            data["direccion"] = direccion.strip()
        if ciudad and ciudad.strip():
            data["ciudad"] = ciudad.strip()
        if departamento and departamento.strip():
            data["departamento"] = departamento.strip()
        if ocupacion and ocupacion.strip():
            data["ocupacion"] = ocupacion.strip()
        if estado_civil and estado_civil.strip():
            data["estado_civil"] = estado_civil.strip()
        if alergias:
            data["alergias"] = alergias
        if medicamentos_actuales:
            data["medicamentos_actuales"] = medicamentos_actuales
        if condiciones_medicas:
            data["condiciones_medicas"] = condiciones_medicas
        if antecedentes_familiares:
            data["antecedentes_familiares"] = antecedentes_familiares
        if observaciones and observaciones.strip():
            data["observaciones"] = observaciones.strip()
        return self.create(data)
     
    @handle_supabase_error
    def get_filtered_patients(
        self,
        activos_only: Optional[bool] = None,
        busqueda: Optional[str] = None,
        genero: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """✅ OBTENER PACIENTES FILTRADOS con búsqueda en campos separados"""
        try:
            print(f"[DEBUG] Obteniendo pacientes filtrados - activos: {activos_only}, búsqueda: {busqueda}")
            
            # ✅ QUERY CON CAMPOS SEPARADOS
            query = self.table.select("*")
            
            # Filtro por estado activo
            if activos_only is True:
                query = query.eq("activo", True)  # Solo activos
            elif activos_only is False:
                query = query.eq("activo", False)
            
            # Filtro por género
            if genero:
                query = query.eq("genero", genero)
            
            # ✅ BÚSQUEDA EN CAMPOS SEPARADOS
            if busqueda:
                search_term = busqueda.strip()
                # Usar or() para buscar en múltiples campos
                query = query.or_(
                    f"primer_nombre.ilike.%{search_term}%,"
                    f"segundo_nombre.ilike.%{search_term}%,"
                    f"primer_apellido.ilike.%{search_term}%,"
                    f"segundo_apellido.ilike.%{search_term}%,"
                    f"numero_documento.ilike.%{search_term}%,"
                    f"email.ilike.%{search_term}%,"
                    f"telefono_1.ilike.%{search_term}%,"
                    f"telefono_2.ilike.%{search_term}%"
                )
            
            # Ordenar por fecha de registro (más recientes primero)
            query = query.order("fecha_registro", desc=True)
            
            # Aplicar límite
            query = query.limit(limit)
            
            response = query.execute()
            
            if response.data:
                print(f"[DEBUG] ✅ Pacientes obtenidos: {len(response.data)} registros")
                return response.data
            else:
                print("[DEBUG] No se encontraron pacientes")
                return []
                
        except Exception as e:
            print(f"[ERROR] Error obteniendo pacientes filtrados: {e}")
            return []
    
    def _apply_search_filter(self, items: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
        """Aplicar filtro de búsqueda en memoria"""
        search_lower = search_term.lower()
        filtered = []
        
        for item in items:
            # Campos donde buscar
            search_fields = [
                str(item.get('nombre_completo', '')).lower(),
                str(item.get('numero_documento', '')).lower(),
                str(item.get('email', '')).lower(),
                str(item.get('telefono', '')).lower(),
                str(item.get('celular', '')).lower(),
                str(item.get('numero_historia', '')).lower()
            ]
            
            # Si algún campo contiene el término
            if any(search_lower in field for field in search_fields):
                filtered.append(item)
        
        return filtered
    
    @handle_supabase_error
    def get_by_documento(self, numero_documento: str) -> Optional[Dict[str, Any]]:
        """Obtiene paciente por número de documento"""
        response = self.table.select("*").eq("numero_documento", numero_documento).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Obtiene paciente por email"""
        response = self.table.select("*").eq("email", email.lower()).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_by_historia(self, numero_historia: str) -> Optional[Dict[str, Any]]:
        """Obtiene paciente por número de historia"""
        response = self.table.select("*").eq("numero_historia", numero_historia).execute()
        return response.data[0] if response.data else None
    
    
    @handle_supabase_error
    def deactivate_patient(self, patient_id: str, motivo: Optional[str] = None) -> Dict[str, Any]:
        """
        Desactiva un paciente (soft delete)
        """
        data = {"activo": False}
        
        if motivo:
            # Agregar motivo a observaciones
            patient = self.get_by_id(patient_id)
            if patient:
                obs_actuales = patient.get("observaciones", "") 
                data["observaciones"] = f"{obs_actuales}\n{date.today()}: Desactivado - {motivo}"
        
        logger.info(f"Desactivando paciente {patient_id}")
        return self.update(patient_id, data)
    


    @handle_supabase_error
    def reactivate_patient(self, patient_id: str) -> Dict[str, Any]:
        """
        Reactiva un paciente
        """
        patient = self.get_by_id(patient_id)
        if not patient:
            raise ValueError(f"Paciente {patient_id} no encontrado")
        
        obs_actuales = patient.get("observaciones", "")
        data = {
            "activo": True,
            "observaciones": f"{obs_actuales}\n{date.today()}: Reactivado"
        }
        
        logger.info(f"Reactivando paciente {patient_id}")
        return self.update(patient_id, data)
    
    @handle_supabase_error
    def get_patient_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas básicas de pacientes"""
        try:
            # Total pacientes activos
            total_response = self.table.select('id', count='exact').eq('activo', True).execute()
            total = total_response.count or 0
            
            # Pacientes nuevos este mes
            current_month = datetime.now().strftime('%Y-%m')
            nuevos_response = self.table.select('id', count='exact').eq('activo', True).gte('fecha_registro', f"{current_month}-01").execute()
            nuevos_mes = nuevos_response.count or 0
            
            # Pacientes por género
            hombres_response = self.table.select('id', count='exact').eq('activo', True).eq('genero', 'masculino').execute()
            mujeres_response = self.table.select('id', count='exact').eq('activo', True).eq('genero', 'femenino').execute()
            
            stats = {
                "total": total,
                "nuevos_mes": nuevos_mes,
                "activos": total,  # Por ahora igual al total
                "hombres": hombres_response.count or 0,
                "mujeres": mujeres_response.count or 0
            }
            
            logger.info(f"Estadísticas de pacientes: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de pacientes: {e}")
            return {
                "total": 0,
                "nuevos_mes": 0,
                "activos": 0,
                "hombres": 0,
                "mujeres": 0
            }
    
    
    @handle_supabase_error
    def update_medical_info(self, 
                           patient_id: str,
                           alergias: Optional[List[str]] = None,
                           medicamentos_actuales: Optional[List[str]] = None,
                           condiciones_medicas: Optional[List[str]] = None,
                           antecedentes_familiares: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Actualiza información médica del paciente
        """
        data = {}
        
        if alergias is not None:
            data["alergias"] = alergias
        if medicamentos_actuales is not None:
            data["medicamentos_actuales"] = medicamentos_actuales
        if condiciones_medicas is not None:
            data["condiciones_medicas"] = condiciones_medicas
        if antecedentes_familiares is not None:
            data["antecedentes_familiares"] = antecedentes_familiares
        
        if data:
            logger.info(f"Actualizando información médica del paciente {patient_id}")
            return self.update(patient_id, data)
        
        return self.get_by_id(patient_id)
    
    @handle_supabase_error
    def get_recent_patients(self, days: int = 30) -> List[Dict[str, Any]]:
        """Obtiene pacientes registrados en los últimos días"""
        from datetime import timedelta
        
        fecha_limite = (datetime.now() - timedelta(days=days)).isoformat()
        
        query = self.table.select("*").eq('activo', True).gte('fecha_registro', fecha_limite).order('fecha_registro', desc=True)
        
        response = query.execute()
        return response.data or []


# Instancia única para importar
pacientes_table = PacientesTable()
