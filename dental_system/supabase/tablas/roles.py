"""
Operaciones CRUD para la tabla roles
"""
from typing import Dict, List, Optional, Any
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class RolesTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla roles
    """
    
    def __init__(self):
        super().__init__('roles')
    
    @handle_supabase_error
    def get_active_roles(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los roles activos del sistema
        
        Returns:
            Lista de roles activos
        """
        logger.info("Obteniendo roles activos")
        query = self.table.select("*").eq("activo", True).order("nombre")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_name(self, nombre: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un rol por su nombre
        
        Args:
            nombre: Nombre del rol
            
        Returns:
            Rol encontrado o None
        """
        logger.info(f"Obteniendo rol por nombre: {nombre}")
        response = self.table.select("*").eq("nombre", nombre).eq("activo", True).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def create_role(self, 
                   nombre: str,
                   descripcion: Optional[str] = None,
                   permisos: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Crea un nuevo rol
        
        Args:
            nombre: Nombre único del rol
            descripcion: Descripción del rol
            permisos: Diccionario de permisos del rol
            
        Returns:
            Rol creado
        """
        data = {
            "nombre": nombre.lower().strip(),
            "descripcion": descripcion or "",
            "permisos": permisos or {},
            "activo": True
        }
        
        logger.info(f"Creando nuevo rol: {nombre}")
        return self.create(data)
    
    @handle_supabase_error
    def update_permissions(self, role_id: str, permisos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza los permisos de un rol
        
        Args:
            role_id: ID del rol
            permisos: Nuevos permisos
            
        Returns:
            Rol actualizado
        """
        data = {"permisos": permisos}
        
        logger.info(f"Actualizando permisos del rol {role_id}")
        return self.update(role_id, data)


# Instancia única para importar
roles_table = RolesTable()