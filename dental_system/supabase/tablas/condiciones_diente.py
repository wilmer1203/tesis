"""
Operaciones CRUD para la tabla condiciones_diente
Maneja las condiciones específicas de cada diente en el odontograma
"""
from typing import Dict, List, Optional, Any
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class CondicionesDienteTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para condiciones específicas de dientes
    """
    
    def __init__(self):
        super().__init__('condiciones_diente')
    
    @handle_supabase_error
    def create_condicion(self,
                        odontograma_id: str,
                        diente_id: str,
                        tipo_condicion: str,
                        registrado_por: str,
                        caras_afectadas: Optional[List[str]] = None,
                        severidad: str = "leve",
                        descripcion: Optional[str] = None,
                        material_utilizado: Optional[str] = None,
                        color_material: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea una nueva condición para un diente
        
        Args:
            odontograma_id: ID del odontograma
            diente_id: ID del diente
            tipo_condicion: Tipo (sano, caries, obturacion, corona, etc.)
            registrado_por: Usuario que registra la condición
            caras_afectadas: Lista de caras afectadas (oclusal, mesial, distal, etc.)
            severidad: Severidad (leve, moderada, severa)
            descripcion: Descripción adicional
            material_utilizado: Material utilizado en tratamiento
            color_material: Color del material para visualización
            
        Returns:
            Condición creada
        """
        data = {
            "odontograma_id": odontograma_id,
            "diente_id": diente_id,
            "tipo_condicion": tipo_condicion,
            "registrado_por": registrado_por,
            "caras_afectadas": caras_afectadas or [],
            "severidad": severidad,
            "estado": "actual"
        }
        
        if descripcion:
            data["descripcion"] = descripcion
        if material_utilizado:
            data["material_utilizado"] = material_utilizado
        if color_material:
            data["color_material"] = color_material
        
        logger.info(f"Creando condición {tipo_condicion} para diente {diente_id}")
        return self.create(data)
    
    @handle_supabase_error
    def get_by_odontograma(self, odontograma_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las condiciones de un odontograma
        
        Args:
            odontograma_id: ID del odontograma
            
        Returns:
            Lista de condiciones del odontograma
        """
        logger.info(f"Obteniendo condiciones del odontograma {odontograma_id}")
        query = self.table.select("""
            *,
            dientes(numero_diente, nombre, tipo_diente, ubicacion)
        """).eq("odontograma_id", odontograma_id).eq("estado", "actual").order("fecha_registro", desc=True)
        
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_diente(self, diente_id: str, odontograma_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todas las condiciones de un diente específico
        
        Args:
            diente_id: ID del diente
            odontograma_id: ID del odontograma (opcional para filtrar)
            
        Returns:
            Lista de condiciones del diente
        """
        query = self.table.select("*").eq("diente_id", diente_id).eq("estado", "actual")
        
        if odontograma_id:
            query = query.eq("odontograma_id", odontograma_id)
        
        query = query.order("fecha_registro", desc=True)
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def update_condicion(self, 
                        condicion_id: str,
                        nuevo_tipo: Optional[str] = None,
                        nuevas_caras: Optional[List[str]] = None,
                        nueva_severidad: Optional[str] = None,
                        nueva_descripcion: Optional[str] = None,
                        nuevo_material: Optional[str] = None,
                        nuevo_color: Optional[str] = None) -> Dict[str, Any]:
        """
        Actualiza una condición existente
        
        Args:
            condicion_id: ID de la condición
            nuevo_tipo: Nuevo tipo de condición
            nuevas_caras: Nuevas caras afectadas
            nueva_severidad: Nueva severidad
            nueva_descripcion: Nueva descripción
            nuevo_material: Nuevo material
            nuevo_color: Nuevo color
            
        Returns:
            Condición actualizada
        """
        data = {}
        
        if nuevo_tipo:
            data["tipo_condicion"] = nuevo_tipo
        if nuevas_caras is not None:
            data["caras_afectadas"] = nuevas_caras
        if nueva_severidad:
            data["severidad"] = nueva_severidad
        if nueva_descripcion:
            data["descripcion"] = nueva_descripcion
        if nuevo_material:
            data["material_utilizado"] = nuevo_material
        if nuevo_color:
            data["color_material"] = nuevo_color
        
        if data:
            logger.info(f"Actualizando condición {condicion_id}")
            return self.update(condicion_id, data)
        
        return self.get_by_id(condicion_id)
    
    @handle_supabase_error
    def historificar_condicion(self, condicion_id: str, motivo: str) -> Dict[str, Any]:
        """
        Marca una condición como histórica (no actual)
        
        Args:
            condicion_id: ID de la condición
            motivo: Motivo del cambio al historial
            
        Returns:
            Condición actualizada
        """
        data = {
            "estado": "historico",
            "observaciones": f"Historificada: {motivo}"
        }
        
        logger.info(f"Historificando condición {condicion_id}")
        return self.update(condicion_id, data)
    
    @handle_supabase_error
    def get_condiciones_por_tipo(self, tipo_condicion: str, odontograma_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene condiciones por tipo específico
        
        Args:
            tipo_condicion: Tipo de condición a buscar
            odontograma_id: Filtrar por odontograma (opcional)
            
        Returns:
            Lista de condiciones del tipo especificado
        """
        query = self.table.select("*").eq("tipo_condicion", tipo_condicion).eq("estado", "actual")
        
        if odontograma_id:
            query = query.eq("odontograma_id", odontograma_id)
        
        response = query.execute()
        return response.data or []
    
    def get_tipos_condiciones(self) -> List[str]:
        """
        Obtiene la lista de tipos de condiciones disponibles
        
        Returns:
            Lista de tipos de condiciones
        """
        return [
            "sano",
            "caries",
            "obturacion", 
            "corona",
            "puente",
            "implante",
            "ausente",
            "extraccion_indicada",
            "endodoncia",
            "protesis",
            "fractura",
            "mancha",
            "desgaste",
            "sensibilidad",
            "movilidad",
            "impactado",
            "en_erupcion",
            "retenido",
            "supernumerario",
            "otro"
        ]
    
    def get_caras_disponibles(self) -> List[str]:
        """
        Obtiene la lista de caras dentales disponibles
        
        Returns:
            Lista de caras dentales
        """
        return [
            "oclusal",
            "mesial", 
            "distal",
            "vestibular",
            "lingual"
        ]


# Instancia única para importar
condiciones_diente_table = CondicionesDienteTable()