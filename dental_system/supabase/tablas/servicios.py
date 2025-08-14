"""
Operaciones CRUD para la tabla servicios
"""
from typing import Dict, List, Optional, Any
from decimal import Decimal
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class ServicesTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla servicios
    """
    
    def __init__(self):
        super().__init__('servicios')
    
    @handle_supabase_error
    def create_service(self,
                      codigo: str,
                      nombre: str,
                      categoria: str,
                      precio_base: Decimal,
                      descripcion: Optional[str] = None,
                      subcategoria: Optional[str] = None,
                      duracion_estimada: str = "30 minutes",
                      precio_minimo: Optional[Decimal] = None,
                      precio_maximo: Optional[Decimal] = None,
                      requiere_cita_previa: bool = True,
                      requiere_autorizacion: bool = False,
                      material_incluido: Optional[List[str]] = None,
                      instrucciones_pre: Optional[str] = None,
                      instrucciones_post: Optional[str] = None,
                      creado_por: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea un nuevo servicio odontológico
        
        Args:
            codigo: Código único del servicio
            nombre: Nombre del servicio
            categoria: Categoría (Consulta, Preventiva, Restaurativa, etc.)
            precio_base: Precio base del servicio
            ... otros campos opcionales
            
        Returns:
            Servicio creado
        """
        data = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio_base": float(precio_base),
            "duracion_estimada": duracion_estimada,
            "requiere_cita_previa": requiere_cita_previa,
            "requiere_autorizacion": requiere_autorizacion,
            "activo": True
        }
        
        # Agregar campos opcionales
        if descripcion:
            data["descripcion"] = descripcion
        if subcategoria:
            data["subcategoria"] = subcategoria
        if precio_minimo:
            data["precio_minimo"] = float(precio_minimo)
        if precio_maximo:
            data["precio_maximo"] = float(precio_maximo)
        if material_incluido:
            data["material_incluido"] = material_incluido
        if instrucciones_pre:
            data["instrucciones_pre"] = instrucciones_pre
        if instrucciones_post:
            data["instrucciones_post"] = instrucciones_post
        if creado_por:
            data["creado_por"] = creado_por
        
        logger.info(f"Creando servicio: {nombre}")
        return self.create(data)
    
    @handle_supabase_error
    def get_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un servicio por su código
        
        Args:
            codigo: Código del servicio
            
        Returns:
            Servicio encontrado o None
        """
        response = self.table.select("*").eq("codigo", codigo).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_by_categoria(self, categoria: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los servicios de una categoría
        
        Args:
            categoria: Categoría de servicios
            
        Returns:
            Lista de servicios en esa categoría
        """
        return self.get_all(
            filters={"categoria": categoria, "activo": True},
            order_by="nombre"
        )
    
    @handle_supabase_error
    def get_active_services(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los servicios activos agrupados por categoría
        
        Returns:
            Lista de servicios activos ordenados por categoría y nombre
        """
        response = self.table.select("*").eq("activo", True).order("nombre").execute()
        return response.data
    
    @handle_supabase_error
    def get_services_by_price_range(self,
                                   precio_min: Optional[Decimal] = None,
                                   precio_max: Optional[Decimal] = None) -> List[Dict[str, Any]]:
        """
        Obtiene servicios dentro de un rango de precios
        
        Args:
            precio_min: Precio mínimo
            precio_max: Precio máximo
            
        Returns:
            Lista de servicios en el rango
        """
        query = self.table.select("*").eq("activo", True)
        
        if precio_min:
            query = query.gte("precio_base", float(precio_min))
        if precio_max:
            query = query.lte("precio_base", float(precio_max))
        
        response = query.order("precio_base").execute()
        return response.data
    
    @handle_supabase_error
    def update_price(self,
                    service_id: str,
                    nuevo_precio: Decimal,
                    precio_minimo: Optional[Decimal] = None,
                    precio_maximo: Optional[Decimal] = None) -> Dict[str, Any]:
        """
        Actualiza el precio de un servicio
        
        Args:
            service_id: ID del servicio
            nuevo_precio: Nuevo precio base
            precio_minimo: Nuevo precio mínimo (opcional)
            precio_maximo: Nuevo precio máximo (opcional)
            
        Returns:
            Servicio actualizado
        """
        data = {"precio_base": float(nuevo_precio)}
        
        if precio_minimo:
            data["precio_minimo"] = float(precio_minimo)
        if precio_maximo:
            data["precio_maximo"] = float(precio_maximo)
        
        logger.info(f"Actualizando precio del servicio {service_id}")
        return self.update(service_id, data)
    
    @handle_supabase_error
    def get_service_statistics(self, service_id: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso de un servicio
        
        Args:
            service_id: ID del servicio
            
        Returns:
            Diccionario con estadísticas del servicio
        """
        # Obtener servicio
        service = self.get_by_id(service_id)
        if not service:
            return None
        
        # Obtener intervenciones con este servicio
        intervenciones_response = self.client.table("intervenciones").select(
            "precio_final, fecha_registro, estado"
        ).eq("servicio_id", service_id).execute()
        
        intervenciones = intervenciones_response.data
        
        # Calcular estadísticas
        stats = {
            "servicio": service,
            "estadisticas": {
                "total_realizadas": len(intervenciones),
                "completadas": len([i for i in intervenciones if i["estado"] == "completada"]),
                "ingresos_totales": sum(i["precio_final"] for i in intervenciones),
                "precio_promedio": sum(i["precio_final"] for i in intervenciones) / len(intervenciones) if intervenciones else 0,
                "ultima_vez_realizada": max(
                    (i["fecha_registro"] for i in intervenciones), 
                    default=None
                )
            }
        }
        
        return stats
    
    @handle_supabase_error
    def get_categorias(self) -> List[str]:
        """
        Obtiene todas las categorías de servicios disponibles
        
        Returns:
            Lista de categorías únicas
        """
        response = self.table.select("categoria").eq("activo", True).execute()
        categorias = list(set(item["categoria"] for item in response.data))
        return sorted(categorias)
    
    @handle_supabase_error
    def search_services(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Busca servicios por código, nombre o descripción
        
        Args:
            search_term: Término de búsqueda
            
        Returns:
            Lista de servicios que coinciden
        """
        return self.search(search_term, ["codigo", "nombre", "descripcion"])
    
    @handle_supabase_error
    def duplicate_service(self, service_id: str, nuevo_codigo: str, nuevo_nombre: str) -> Dict[str, Any]:
        """
        Duplica un servicio existente con nuevo código y nombre
        
        Args:
            service_id: ID del servicio a duplicar
            nuevo_codigo: Código para el nuevo servicio
            nuevo_nombre: Nombre para el nuevo servicio
            
        Returns:
            Nuevo servicio creado
        """
        # Obtener servicio original
        original = self.get_by_id(service_id)
        if not original:
            raise ValueError(f"Servicio {service_id} no encontrado")
        
        # Crear copia con nuevos valores
        nuevo_servicio = original.copy()
        del nuevo_servicio["id"]
        del nuevo_servicio["fecha_creacion"]
        
        nuevo_servicio["codigo"] = nuevo_codigo
        nuevo_servicio["nombre"] = nuevo_nombre
        
        logger.info(f"Duplicando servicio {original['nombre']} como {nuevo_nombre}")
        return self.create(nuevo_servicio)


# Instancia única para importar
services_table = ServicesTable()
servicios_table = services_table  # Alias para consistencia