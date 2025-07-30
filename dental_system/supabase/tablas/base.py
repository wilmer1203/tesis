"""
Clase base para operaciones CRUD en Supabase
"""
from typing import Dict, List, Optional, Any, Union
from ..client import  handle_supabase_error, supabase_client
import logging

logger = logging.getLogger(__name__)


class BaseTable:
    """
    Clase base que proporciona operaciones CRUD comunes para todas las tablas
    """
    
    def __init__(self, table_name: str):
        """
        Inicializa la tabla con su nombre
        
        Args:
            table_name: Nombre de la tabla en Supabase
        """
        self.table_name = table_name
        self._client = None
    
    @property
    def client(self):
        """Cliente de Supabase (lazy loading)"""
        if self._client is None:
            self._client = supabase_client.get_client()
        return self._client
    
    def client_admin(self):
        self._client = supabase_client.get_admin_client()
        return self._client

    @property
    def table(self):
        """Referencia a la tabla"""
        return self.client.table(self.table_name)
    
    @handle_supabase_error
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo registro
        
        Args:
            data: Diccionario con los datos del registro
            
        Returns:
            Registro creado
        """
        logger.info(f"Creando registro en {self.table_name}")
        print(f"Creando registro en {self.table_name} con datos: {data}")
        response = self.table.insert(data).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un registro por ID
        
        Args:
            id: UUID del registro
            
        Returns:
            Registro encontrado o None
        """
        logger.info(f"Obteniendo registro {id} de {self.table_name}")
        response = self.table.select("*").eq("id", id).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_all(self, 
                filters: Optional[Dict[str, Any]] = None,
                order_by: Optional[str] = None,
                limit: Optional[int] = None,
                offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros con filtros opcionales
        
        Args:
            filters: Diccionario de filtros {campo: valor}
            order_by: Campo para ordenar (usar '-campo' para descendente)
            limit: Límite de registros
            offset: Desplazamiento para paginación
            
        Returns:
            Lista de registros
        """
        query = self.table.select("*")
        
        # Aplicar filtros
        if filters:
            for field, value in filters.items():
                if value is not None:
                    query = query.eq(field, value)
        
        # Aplicar ordenamiento
        if order_by:
            if order_by.startswith('-'):
                query = query.order(order_by[1:], desc=True)
            else:
                query = query.order(order_by)
        
        # Aplicar límite y offset
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.range(offset, offset + (limit or 100) - 1)
        
        logger.info(f"Obteniendo registros de {self.table_name} con filtros: {filters}")
        response = query.execute()
        return response.data
    
    @handle_supabase_error
    def update(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un registro
        
        Args:
            id: UUID del registro
            data: Datos a actualizar
            
        Returns:
            Registro actualizado
        """
        logger.info(f"Actualizando registro {id} en {self.table_name}")
        response = self.table.update(data).eq("id", id).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def delete(self, id: str) -> bool:
        """
        Elimina un registro (soft delete si tiene campo 'activo')
        
        Args:
            id: UUID del registro
            
        Returns:
            True si se eliminó correctamente
        """
        logger.info(f"Eliminando registro {id} de {self.table_name}")
        
        # Verificar si la tabla tiene campo 'activo' para soft delete
        registro = self.get_by_id(id)
        if registro and 'activo' in registro:
            # Soft delete
            response = self.table.update({"activo": False}).eq("id", id).execute()
        else:
            # Hard delete
            response = self.table.delete().eq("id", id).execute()
        
        return bool(response.data)
    
    @handle_supabase_error
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Cuenta registros con filtros opcionales
        
        Args:
            filters: Diccionario de filtros
            
        Returns:
            Número de registros
        """
        query = self.table.select("id", count="exact")
        
        if filters:
            for field, value in filters.items():
                if value is not None:
                    query = query.eq(field, value)
        
        response = query.execute()
        return response.count
    
    @handle_supabase_error
    def search(self, search_term: str, fields: List[str]) -> List[Dict[str, Any]]:
        """
        Busca registros en múltiples campos
        
        Args:
            search_term: Término de búsqueda
            fields: Lista de campos donde buscar
            
        Returns:
            Lista de registros que coinciden
        """
        # Construir query de búsqueda con OR
        or_conditions = []
        for field in fields:
            or_conditions.append(f"{field}.ilike.%{search_term}%")
        
        query_string = f"or=({','.join(or_conditions)})"
        
        logger.info(f"Buscando '{search_term}' en {self.table_name}")
        response = self.table.select("*").or_(query_string).execute()
        return response.data
    
    @handle_supabase_error
    def batch_create(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Crea múltiples registros de una vez
        
        Args:
            data_list: Lista de diccionarios con datos
            
        Returns:
            Lista de registros creados
        """
        logger.info(f"Creando {len(data_list)} registros en {self.table_name}")
        response = self.table.insert(data_list).execute()
        return response.data
    
    @handle_supabase_error
    def exists(self, filters: Dict[str, Any]) -> bool:
        """
        Verifica si existe un registro con los filtros dados
        
        Args:
            filters: Diccionario de filtros
            
        Returns:
            True si existe al menos un registro
        """
        query = self.table.select("id")
        
        for field, value in filters.items():
            query = query.eq(field, value)
        
        query = query.limit(1)
        response = query.execute()
        return bool(response.data)