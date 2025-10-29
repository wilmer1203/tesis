"""
Operaciones CRUD para la tabla dientes (catálogo FDI)
"""
from typing import Dict, List, Optional, Any
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class DientesTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla dientes
    Catálogo de dientes según numeración FDI internacional
    """
    
    def __init__(self):
        super().__init__('dientes')
    
    @handle_supabase_error
    def get_all_active(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los dientes activos ordenados por número
        
        Returns:
            Lista de dientes activos
        """
        logger.info("Obteniendo catálogo completo de dientes")
        query = self.table.select("*").eq("activo", True).order("numero_diente")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_numero(self, numero_diente: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un diente por su número FDI
        
        Args:
            numero_diente: Número FDI del diente (11-18, 21-28, etc.)
            
        Returns:
            Diente encontrado o None
        """
        logger.info(f"Obteniendo diente número {numero_diente}")
        response = self.table.select("*").eq("numero_diente", numero_diente).eq("activo", True).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_by_cuadrante(self, cuadrante: int) -> List[Dict[str, Any]]:
        """
        Obtiene todos los dientes de un cuadrante específico
        
        Args:
            cuadrante: Número de cuadrante (1-4 para adultos, 5-8 para temporales)
            
        Returns:
            Lista de dientes del cuadrante
        """
        logger.info(f"Obteniendo dientes del cuadrante {cuadrante}")
        query = self.table.select("*").eq("cuadrante", cuadrante).eq("activo", True).order("posicion_en_cuadrante")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_adult_teeth(self) -> List[Dict[str, Any]]:
        """
        Obtiene solo los dientes permanentes (adultos)
        
        Returns:
            Lista de dientes permanentes
        """
        logger.info("Obteniendo dientes permanentes")
        query = self.table.select("*").eq("es_temporal", False).eq("activo", True).order("numero_diente")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_temporary_teeth(self) -> List[Dict[str, Any]]:
        """
        Obtiene solo los dientes temporales (infantiles)
        
        Returns:
            Lista de dientes temporales
        """
        logger.info("Obteniendo dientes temporales")
        query = self.table.select("*").eq("es_temporal", True).eq("activo", True).order("numero_diente_pediatrico")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_tipo(self, tipo_diente: str) -> List[Dict[str, Any]]:
        """
        Obtiene dientes por tipo
        
        Args:
            tipo_diente: Tipo (incisivo, canino, premolar, molar)
            
        Returns:
            Lista de dientes del tipo especificado
        """
        logger.info(f"Obteniendo dientes tipo {tipo_diente}")
        query = self.table.select("*").eq("tipo_diente", tipo_diente).eq("activo", True).order("numero_diente")
        response = query.execute()
        return response.data or []
    
    def get_odontograma_structure(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtiene la estructura completa para construir un odontograma
        Organiza los dientes por cuadrantes
        
        Returns:
            Diccionario con dientes organizados por cuadrantes
        """
        dientes = self.get_adult_teeth()
        
        estructura = {
            "superior_derecho": [],  # Cuadrante 1
            "superior_izquierdo": [], # Cuadrante 2
            "inferior_izquierdo": [], # Cuadrante 3
            "inferior_derecho": []    # Cuadrante 4
        }
        
        for diente in dientes:
            cuadrante = diente.get("cuadrante")
            ubicacion = diente.get("ubicacion", "")
            
            if cuadrante == 1 or "superior_derecha" in ubicacion:
                estructura["superior_derecho"].append(diente)
            elif cuadrante == 2 or "superior_izquierda" in ubicacion:
                estructura["superior_izquierdo"].append(diente)
            elif cuadrante == 3 or "inferior_izquierda" in ubicacion:
                estructura["inferior_izquierdo"].append(diente)
            elif cuadrante == 4 or "inferior_derecha" in ubicacion:
                estructura["inferior_derecho"].append(diente)
        
        return estructura


# Instancia única para importar
dientes_table = DientesTable()