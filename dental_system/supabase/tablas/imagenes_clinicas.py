"""
Operaciones CRUD para la tabla imagenes_clinicas
Manejo de imágenes médicas (radiografías, fotografías, etc.)
"""
from typing import Dict, List, Optional, Any
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class ImagenesClinicasTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para imágenes clínicas
    """
    
    def __init__(self):
        super().__init__('imagenes_clinicas')
    
    @handle_supabase_error
    def create_imagen(self,
                     paciente_id: str,
                     titulo: str,
                     tipo_imagen: str,
                     url_imagen: str,
                     capturada_por: str,
                     consulta_id: Optional[str] = None,
                     odontograma_id: Optional[str] = None,
                     descripcion: Optional[str] = None,
                     url_thumbnail: Optional[str] = None,
                     tamaño_archivo: Optional[int] = None,
                     formato_archivo: Optional[str] = None,
                     equipo_utilizado: Optional[str] = None,
                     configuracion_equipo: Optional[Dict[str, Any]] = None,
                     es_confidencial: bool = False,
                     tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Registra una nueva imagen clínica
        
        Args:
            paciente_id: ID del paciente
            titulo: Título descriptivo de la imagen
            tipo_imagen: Tipo (radiografia_panoramica, radiografia_periapical, fotografia_intraoral, etc.)
            url_imagen: URL de la imagen
            capturada_por: Usuario que capturó/subió la imagen
            consulta_id: ID de la consulta relacionada (opcional)
            odontograma_id: ID del odontograma relacionado (opcional)
            descripcion: Descripción detallada
            url_thumbnail: URL de la miniatura
            tamaño_archivo: Tamaño en bytes
            formato_archivo: Formato (jpg, png, dicom, etc.)
            equipo_utilizado: Equipo usado para capturar
            configuracion_equipo: Configuración del equipo
            es_confidencial: Si la imagen es confidencial
            tags: Etiquetas de la imagen
            
        Returns:
            Imagen registrada
        """
        data = {
            "paciente_id": paciente_id,
            "titulo": titulo,
            "tipo_imagen": tipo_imagen,
            "url_imagen": url_imagen,
            "capturada_por": capturada_por,
            "es_confidencial": es_confidencial,
            "activo": True
        }
        
        # Agregar campos opcionales
        if consulta_id:
            data["consulta_id"] = consulta_id
        if odontograma_id:
            data["odontograma_id"] = odontograma_id
        if descripcion:
            data["descripcion"] = descripcion
        if url_thumbnail:
            data["url_thumbnail"] = url_thumbnail
        if tamaño_archivo:
            data["tamaño_archivo"] = tamaño_archivo
        if formato_archivo:
            data["formato_archivo"] = formato_archivo
        if equipo_utilizado:
            data["equipo_utilizado"] = equipo_utilizado
        if configuracion_equipo:
            data["configuracion_equipo"] = configuracion_equipo
        if tags:
            data["tags"] = tags
        
        logger.info(f"Registrando imagen clínica para paciente {paciente_id}: {titulo}")
        return self.create(data)
    
    @handle_supabase_error
    def get_by_paciente(self, paciente_id: str, incluir_confidenciales: bool = False) -> List[Dict[str, Any]]:
        """
        Obtiene todas las imágenes de un paciente
        
        Args:
            paciente_id: ID del paciente
            incluir_confidenciales: Si incluir imágenes confidenciales
            
        Returns:
            Lista de imágenes del paciente
        """
        logger.info(f"Obteniendo imágenes del paciente {paciente_id}")
        
        query = self.table.select("""
            *,
            usuarios!capturada_por(email),
            consultas(numero_consulta, fecha_programada)
        """).eq("paciente_id", paciente_id).eq("activo", True)
        
        if not incluir_confidenciales:
            query = query.eq("es_confidencial", False)
        
        query = query.order("fecha_captura", desc=True)
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_consulta(self, consulta_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las imágenes de una consulta específica
        
        Args:
            consulta_id: ID de la consulta
            
        Returns:
            Lista de imágenes de la consulta
        """
        logger.info(f"Obteniendo imágenes de la consulta {consulta_id}")
        
        query = self.table.select("""
            *,
            usuarios!capturada_por(email)
        """).eq("consulta_id", consulta_id).eq("activo", True).order("fecha_captura")
        
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_tipo(self, tipo_imagen: str, paciente_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene imágenes por tipo específico
        
        Args:
            tipo_imagen: Tipo de imagen a buscar
            paciente_id: Filtrar por paciente (opcional)
            
        Returns:
            Lista de imágenes del tipo especificado
        """
        query = self.table.select("*").eq("tipo_imagen", tipo_imagen).eq("activo", True)
        
        if paciente_id:
            query = query.eq("paciente_id", paciente_id)
        
        query = query.order("fecha_captura", desc=True)
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_odontograma(self, odontograma_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene imágenes asociadas a un odontograma
        
        Args:
            odontograma_id: ID del odontograma
            
        Returns:
            Lista de imágenes del odontograma
        """
        logger.info(f"Obteniendo imágenes del odontograma {odontograma_id}")
        
        query = self.table.select("*").eq("odontograma_id", odontograma_id).eq("activo", True).order("fecha_captura")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def search_by_tags(self, tags: List[str], paciente_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Busca imágenes por etiquetas
        
        Args:
            tags: Lista de etiquetas a buscar
            paciente_id: Filtrar por paciente (opcional)
            
        Returns:
            Lista de imágenes que contienen las etiquetas
        """
        query = self.table.select("*").eq("activo", True)
        
        if paciente_id:
            query = query.eq("paciente_id", paciente_id)
        
        # Buscar imágenes que contengan al menos uno de los tags
        for tag in tags:
            query = query.contains("tags", [tag])
        
        query = query.order("fecha_captura", desc=True)
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def update_imagen(self,
                     imagen_id: str,
                     titulo: Optional[str] = None,
                     descripcion: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     es_confidencial: Optional[bool] = None) -> Dict[str, Any]:
        """
        Actualiza metadatos de una imagen
        
        Args:
            imagen_id: ID de la imagen
            titulo: Nuevo título
            descripcion: Nueva descripción
            tags: Nuevas etiquetas
            es_confidencial: Nuevo estado de confidencialidad
            
        Returns:
            Imagen actualizada
        """
        data = {}
        
        if titulo:
            data["titulo"] = titulo
        if descripcion is not None:
            data["descripcion"] = descripcion
        if tags is not None:
            data["tags"] = tags
        if es_confidencial is not None:
            data["es_confidencial"] = es_confidencial
        
        if data:
            logger.info(f"Actualizando metadatos de imagen {imagen_id}")
            return self.update(imagen_id, data)
        
        return self.get_by_id(imagen_id)
    
    @handle_supabase_error
    def deactivate_imagen(self, imagen_id: str, motivo: Optional[str] = None) -> Dict[str, Any]:
        """
        Desactiva una imagen (soft delete)
        
        Args:
            imagen_id: ID de la imagen
            motivo: Motivo de la desactivación
            
        Returns:
            Imagen desactivada
        """
        data = {"activo": False}
        
        if motivo:
            current_imagen = self.get_by_id(imagen_id)
            if current_imagen:
                descripcion_actual = current_imagen.get("descripcion", "")
                data["descripcion"] = f"{descripcion_actual}\n[DESACTIVADA: {motivo}]"
        
        logger.info(f"Desactivando imagen {imagen_id}")
        return self.update(imagen_id, data)
    
    def get_tipos_imagen(self) -> List[str]:
        """
        Obtiene la lista de tipos de imagen disponibles
        
        Returns:
            Lista de tipos de imagen
        """
        return [
            "radiografia_panoramica",
            "radiografia_periapical",
            "radiografia_bite_wing",
            "fotografia_intraoral",
            "fotografia_extraoral",
            "fotografia_oclusal",
            "tomografia",
            "escaner_3d",
            "otro"
        ]
    
    @handle_supabase_error
    def get_estadisticas_imagenes(self, paciente_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtiene estadísticas de imágenes
        
        Args:
            paciente_id: Filtrar por paciente (opcional)
            
        Returns:
            Estadísticas de imágenes
        """
        try:
            base_query = self.table.select("id", count="exact").eq("activo", True)
            
            if paciente_id:
                base_query = base_query.eq("paciente_id", paciente_id)
            
            # Total de imágenes
            total_response = base_query.execute()
            total = total_response.count or 0
            
            # Imágenes confidenciales
            conf_response = base_query.eq("es_confidencial", True).execute()
            confidenciales = conf_response.count or 0
            
            return {
                "total_imagenes": total,
                "imagenes_confidenciales": confidenciales,
                "imagenes_publicas": total - confidenciales
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de imágenes: {e}")
            return {
                "total_imagenes": 0,
                "imagenes_confidenciales": 0,
                "imagenes_publicas": 0
            }


# Instancia única para importar
imagenes_clinicas_table = ImagenesClinicasTable()