"""
Servicio centralizado para gestión de servicios odontológicos
Sigue el mismo patrón que PacientesService
"""

from typing import Dict, List, Optional, Any
from decimal import Decimal
from .base_service import BaseService
from dental_system.supabase.tablas import services_table
from dental_system.models import ServicioModel, ServicioFormModel
from .cache_invalidation_hooks import invalidate_after_service_operation, track_cache_invalidation
import logging

logger = logging.getLogger(__name__)

class ServiciosService(BaseService):
    """
    Servicio que maneja toda la lógica de servicios odontológicos
    Usado por Jefe (CRUD completo) y otros roles según permisos
    """
    
    def __init__(self):
        super().__init__()
        self.table = services_table
    
    async def get_filtered_services(self, 
                                  search: str = None, 
                                  categoria: str = None, 
                                  activos_only: Optional[bool] = True) -> List[ServicioModel]:
        """
        Obtiene servicios filtrados 
        
        Args:
            search: Término de búsqueda
            categoria: Filtro por categoría
            activos_only: Solo servicios activos
            
        Returns:
            Lista de servicios como modelos tipados
        """
        try:
            # Verificar permisos
            if not self.check_permission("servicios", "leer"):
                raise PermissionError("Sin permisos para acceder a servicios")
            # Si hay búsqueda, usar search
            if search and search.strip():
                servicios_data = self.table.search_services(search.strip())
            # Si hay categoría específica
            elif categoria and categoria != "todas":
                servicios_data = self.table.get_by_categoria(categoria)
            # Por defecto, obtener activos
            elif activos_only:
                servicios_data = self.table.get_active_services()
            else:
                servicios_data = self.table.get_all()
            
            # Filtrar por activos si es necesario
            if activos_only and not search:
                servicios_data = [s for s in servicios_data if s.get("activo", True)]
            
            # Convertir a modelos tipados
            servicios_models = []
            for item in servicios_data:
                try:
                    model = ServicioModel.from_dict(item)
                    servicios_models.append(model)
                except Exception as e:
                    logger.warning(f"Error convirtiendo servicio: {e}")
                    continue
            
            logger.info(f"✅ Servicios obtenidos: {len(servicios_models)} registros")
            return servicios_models
            
        except PermissionError:
            logger.warning("Usuario sin permisos para acceder a servicios")
            raise
        except Exception as e:
            self.handle_error("Error obteniendo servicios filtrados", e)
            return []
    
    async def create_service(self, servicio_form: ServicioFormModel, user_id: str) -> Optional[ServicioModel]:
        """
        Crea un nuevo servicio odontológico
        
        Args:
            form_data: Datos del formulario
            user_id: ID del usuario que crea
            
        Returns:
            Servicio creado o None si hay error
        """
        try:
            logger.info("Creando nuevo servicio")
            
            # Verificar permisos
            self.require_permission("servicios", "crear")
            
            # Validar datos usando el modelo
            errores_validacion = servicio_form.validate_form()
            if errores_validacion:
                raise ValueError(f"Errores de validación: {errores_validacion}")

            # Convertir modelo a diccionario para la tabla
            form_data = servicio_form.to_dict()

            # Verificar que no exista el código
            existing = self.table.get_by_codigo(form_data["codigo"])
            if existing:
                raise ValueError("Ya existe un servicio con este código")

            # Crear servicio usando el método de la tabla
            result = self.table.create_service(
                codigo=form_data["codigo"],
                nombre=form_data["nombre"],
                categoria=form_data["categoria"],
                precio_base_usd=form_data["precio_base_usd"],
                alcance_servicio=form_data.get("alcance_servicio", "superficie_especifica"),
                descripcion=form_data.get("descripcion"),
                material_incluido=form_data.get("material_incluido"),
                condicion_resultante=form_data.get("condicion_resultante"),
                creado_por=user_id
            )
            
            if result:
                logger.info(f"✅ Servicio creado: {form_data['nombre']}")

                # 🗑️ INVALIDAR CACHE - servicio creado afecta servicios activos
                try:
                    invalidate_after_service_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras crear servicio: {cache_error}")

                # Convertir resultado a modelo tipado
                return ServicioModel.from_dict(result)
            else:
                raise ValueError("Error creando servicio en la base de datos")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para crear servicios")
            raise
        except ValueError as e:
            logger.warning(f"Error de validación: {e}")
            raise
        except Exception as e:
            self.handle_error("Error creando servicio", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def update_service(self, service_id: str, servicio_form: ServicioFormModel) -> Optional[ServicioModel]:
        """
        Actualiza un servicio existente

        Args:
            service_id: ID del servicio a actualizar
            servicio_form: Formulario con datos actualizados

        Returns:
            ServicioModel actualizado o None si hay error

        Raises:
            ValueError: Si hay errores de validación
            PermissionError: Si no tiene permisos
        """
        try:
            # Verificar permisos
            if not self.check_permission("servicios", "actualizar"):
                raise PermissionError("No tiene permisos para actualizar servicios")

            # Validar que exista el servicio
            servicio_actual = self.table.get_by_id(service_id)
            if not servicio_actual:
                raise ValueError("Servicio no encontrado")

            # Validar formulario
            errores = servicio_form.validate_form()
            if errores:
                raise ValueError(f"Errores de validación: {errores}")

            # Si se cambió el código, verificar que no exista
            if servicio_form.codigo != servicio_actual["codigo"]:
                existing = self.table.get_by_codigo(servicio_form.codigo)
                if existing:
                    raise ValueError("Ya existe un servicio con este código")

            # Convertir formulario a diccionario
            data = servicio_form.to_dict()
            
            # Mantener campos que no se actualizan
            data["activo"] = servicio_actual["activo"]
            data["fecha_creacion"] = servicio_actual["fecha_creacion"]
            data["creado_por"] = servicio_actual["creado_por"]
            
            # Actualizar
            result = self.table.update(
                service_id,
                data
            )

            if result:
                # Invalidar caché
                try:
                    invalidate_after_service_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras actualizar servicio: {cache_error}")

                return ServicioModel.from_dict(result)

        except Exception as e:
            logger.error(f"Error actualizando servicio {service_id}: {e}")
            raise

        return None

    
    async def deactivate_service(self, service_id: str, motivo: str = None) -> bool:
        """
        Desactiva un servicio (soft delete)
        
        Args:
            service_id: ID del servicio
            motivo: Motivo de desactivación
            
        Returns:
            True si se desactivó correctamente
        """
        try:
            logger.info(f"Desactivando servicio: {service_id}")
            
            # Verificar permisos
            self.require_permission("servicios", "eliminar")
            
            # TODO: Verificar que no tenga intervenciones activas
            
            # Desactivar
            result = self.table.update(service_id, {"activo": False})
            
            if result:
                logger.info(f"✅ Servicio desactivado correctamente")
                
                # 🗑️ INVALIDAR CACHE - servicio desactivado afecta servicios activos
                try:
                    invalidate_after_service_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras desactivar servicio: {cache_error}")
                
                return True
            else:
                raise ValueError("Error desactivando servicio")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para desactivar servicios")
            raise
        except Exception as e:
            self.handle_error("Error desactivando servicio", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def reactivate_service(self, service_id: str) -> bool:
        """
        Reactiva un servicio
        
        Args:
            service_id: ID del servicio
            
        Returns:
            True si se reactivó correctamente
        """
        try:
            logger.info(f"Reactivando servicio: {service_id}")
            
            # Verificar permisos
            self.require_permission("servicios", "crear")  # Reactivar = crear de nuevo
            
            result = self.table.update(service_id, {"activo": True})
            
            if result:
                logger.info(f"✅ Servicio reactivado correctamente")
                
                # 🗑️ INVALIDAR CACHE - servicio reactivado afecta servicios activos
                try:
                    invalidate_after_service_operation()
                except Exception as cache_error:
                    logger.warning(f"Error invalidando cache tras reactivar servicio: {cache_error}")
                
                return True
            else:
                raise ValueError("Error reactivando servicio")
                
        except PermissionError:
            logger.warning("Usuario sin permisos para reactivar servicios")
            raise
        except Exception as e:
            self.handle_error("Error reactivando servicio", e)
            raise ValueError(f"Error inesperado: {str(e)}")
    
    async def get_service_by_id(self, service_id: str) -> Optional[ServicioModel]:
        """
        Obtiene un servicio por ID
        
        Args:
            service_id: ID del servicio
            
        Returns:
            Modelo del servicio o None
        """
        try:
            # Verificar permisos
            self.require_permission("servicios", "leer")
            
            data = self.table.get_by_id(service_id)
            if data:
                return ServicioModel.from_dict(data)
            return None
            
        except Exception as e:
            self.handle_error("Error obteniendo servicio por ID", e)
            return None
    
    async def get_categorias(self) -> List[str]:
        """
        Obtiene todas las categorías disponibles
        
        Returns:
            Lista de categorías
        """
        try:
            # Verificar permisos
            self.require_permission("servicios", "leer")
            
            categorias = self.table.get_categorias()
            logger.info(f"Categorías obtenidas: {categorias}")
            return categorias
            
        except Exception as e:
            self.handle_error("Error obteniendo categorías", e)
            return []
    
    async def get_all_services(self, activos_only: bool = True) -> List[ServicioModel]:
        """
        Obtiene todos los servicios (método requerido por estado_servicios)

        Args:
            activos_only: Solo servicios activos

        Returns:
            Lista de servicios como modelos tipados
        """
        try:
            # Verificar permisos
            if not self.check_permission("servicios", "leer"):
                raise PermissionError("Sin permisos para acceder a servicios")

            return await self.get_filtered_services(activos_only=activos_only)

        except Exception as e:
            self.handle_error("Error obteniendo todos los servicios", e)
            return []

    async def get_servicios_stats(self) -> Dict[str, Any]:
        """
        Alias para get_service_stats (requerido por estado_servicios)
        """
        return await self.get_service_stats()

    async def get_service_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de servicios
        Usado por dashboard_service pero disponible independientemente
        """
        try:
            # Obtener todos los servicios
            servicios = self.table.get_all()

            # Calcular estadísticas básicas
            total = len(servicios)
            activos = len([s for s in servicios if s.get("activo", True)])
            inactivos = total - activos

            # Agrupar por categoría
            categorias = {}
            precios_totales = []

            for servicio in servicios:
                if servicio.get("activo", True):  # Solo contar activos
                    cat = servicio.get("categoria", "Sin categoría")
                    categorias[cat] = categorias.get(cat, 0) + 1

                    precio = servicio.get("precio_base", 0)
                    if precio:
                        precios_totales.append(precio)

            # Calcular precio promedio
            precio_promedio = sum(precios_totales) / len(precios_totales) if precios_totales else 0

            stats = {
                "total": total,
                "activos": activos,
                "inactivos": inactivos,
                "categorias": len(categorias),
                "precio_promedio": round(precio_promedio, 2),
                "por_categoria": categorias
            }

            logger.info(f"Estadísticas de servicios: {stats}")
            return stats

        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de servicios", e)
            return {
                "total": 0,
                "activos": 0,
                "inactivos": 0,
                "categorias": 0,
                "precio_promedio": 0,
                "por_categoria": {}
            }

# Instancia única para importar
servicios_service = ServiciosService()