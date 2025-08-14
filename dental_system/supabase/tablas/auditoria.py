"""
Operaciones CRUD para la tabla auditoria
Sistema de auditoría y trazabilidad completa
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class AuditoriaTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la auditoría del sistema
    """
    
    def __init__(self):
        super().__init__('auditoria')
    
    @handle_supabase_error
    def registrar_accion(self,
                        tabla_afectada: str,
                        registro_id: str,
                        accion: str,
                        usuario_id: Optional[str] = None,
                        datos_anteriores: Optional[Dict[str, Any]] = None,
                        datos_nuevos: Optional[Dict[str, Any]] = None,
                        campos_modificados: Optional[List[str]] = None,
                        motivo: Optional[str] = None,
                        modulo: Optional[str] = None,
                        accion_contexto: Optional[str] = None,
                        ip_address: Optional[str] = None,
                        user_agent: Optional[str] = None) -> Dict[str, Any]:
        """
        Registra una acción en la auditoría
        
        Args:
            tabla_afectada: Nombre de la tabla afectada
            registro_id: ID del registro afectado
            accion: Tipo de acción (INSERT, UPDATE, DELETE)
            usuario_id: ID del usuario que ejecuta la acción
            datos_anteriores: Datos antes de la modificación
            datos_nuevos: Datos después de la modificación
            campos_modificados: Lista de campos que cambiaron
            motivo: Motivo de la acción
            modulo: Módulo del sistema donde ocurrió
            accion_contexto: Contexto adicional de la acción
            ip_address: IP del usuario
            user_agent: User agent del navegador
            
        Returns:
            Registro de auditoría creado
        """
        data = {
            "tabla_afectada": tabla_afectada,
            "registro_id": registro_id,
            "accion": accion.upper(),
            "fecha_accion": datetime.now().isoformat()
        }
        
        # Agregar campos opcionales
        if usuario_id:
            data["usuario_id"] = usuario_id
        if datos_anteriores:
            data["datos_anteriores"] = datos_anteriores
        if datos_nuevos:
            data["datos_nuevos"] = datos_nuevos
        if campos_modificados:
            data["campos_modificados"] = campos_modificados
        if motivo:
            data["motivo"] = motivo
        if modulo:
            data["modulo"] = modulo
        if accion_contexto:
            data["accion_contexto"] = accion_contexto
        if ip_address:
            data["ip_address"] = ip_address
        if user_agent:
            data["user_agent"] = user_agent
        
        logger.info(f"Registrando auditoría: {accion} en {tabla_afectada} - {registro_id}")
        return self.create(data)
    
    @handle_supabase_error
    def get_by_tabla(self, 
                    tabla_afectada: str, 
                    registro_id: Optional[str] = None,
                    limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene registros de auditoría por tabla
        
        Args:
            tabla_afectada: Nombre de la tabla
            registro_id: ID específico del registro (opcional)
            limit: Límite de registros a obtener
            
        Returns:
            Lista de registros de auditoría
        """
        query = self.table.select("""
            *,
            usuarios(email)
        """).eq("tabla_afectada", tabla_afectada)
        
        if registro_id:
            query = query.eq("registro_id", registro_id)
        
        query = query.order("fecha_accion", desc=True).limit(limit)
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_usuario(self, usuario_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene registros de auditoría de un usuario específico
        
        Args:
            usuario_id: ID del usuario
            limit: Límite de registros
            
        Returns:
            Lista de acciones del usuario
        """
        logger.info(f"Obteniendo auditoría del usuario {usuario_id}")
        query = self.table.select("""
            *,
            usuarios(email)
        """).eq("usuario_id", usuario_id).order("fecha_accion", desc=True).limit(limit)
        
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_by_date_range(self,
                         fecha_inicio: date,
                         fecha_fin: date,
                         tabla_afectada: Optional[str] = None,
                         accion: Optional[str] = None,
                         limit: int = 500) -> List[Dict[str, Any]]:
        """
        Obtiene registros de auditoría en un rango de fechas
        
        Args:
            fecha_inicio: Fecha inicial
            fecha_fin: Fecha final
            tabla_afectada: Filtrar por tabla (opcional)
            accion: Filtrar por tipo de acción (opcional)
            limit: Límite de registros
            
        Returns:
            Lista de registros en el rango de fechas
        """
        query = self.table.select("""
            *,
            usuarios(email)
        """).gte("fecha_accion", fecha_inicio.isoformat()
        ).lte("fecha_accion", fecha_fin.isoformat())
        
        if tabla_afectada:
            query = query.eq("tabla_afectada", tabla_afectada)
        if accion:
            query = query.eq("accion", accion.upper())
        
        query = query.order("fecha_accion", desc=True).limit(limit)
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_registro_history(self, tabla: str, registro_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene el historial completo de un registro específico
        
        Args:
            tabla: Nombre de la tabla
            registro_id: ID del registro
            
        Returns:
            Historial cronológico del registro
        """
        logger.info(f"Obteniendo historial de {tabla}.{registro_id}")
        query = self.table.select("""
            *,
            usuarios(email)
        """).eq("tabla_afectada", tabla).eq("registro_id", registro_id).order("fecha_accion")
        
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_estadisticas_auditoria(self, 
                                  fecha_inicio: Optional[date] = None,
                                  fecha_fin: Optional[date] = None) -> Dict[str, Any]:
        """
        Obtiene estadísticas de auditoría
        
        Args:
            fecha_inicio: Fecha inicial (opcional, por defecto último mes)
            fecha_fin: Fecha final (opcional, por defecto hoy)
            
        Returns:
            Estadísticas de auditoría
        """
        if not fecha_inicio:
            fecha_inicio = date.today().replace(day=1)  # Primer día del mes
        if not fecha_fin:
            fecha_fin = date.today()
        
        try:
            # Total de acciones
            total_response = self.table.select("id", count="exact").gte(
                "fecha_accion", fecha_inicio.isoformat()
            ).lte("fecha_accion", fecha_fin.isoformat()).execute()
            
            total_acciones = total_response.count or 0
            
            # Acciones por tipo
            insert_response = self.table.select("id", count="exact").eq("accion", "INSERT").gte(
                "fecha_accion", fecha_inicio.isoformat()
            ).lte("fecha_accion", fecha_fin.isoformat()).execute()
            
            update_response = self.table.select("id", count="exact").eq("accion", "UPDATE").gte(
                "fecha_accion", fecha_inicio.isoformat()
            ).lte("fecha_accion", fecha_fin.isoformat()).execute()
            
            delete_response = self.table.select("id", count="exact").eq("accion", "DELETE").gte(
                "fecha_accion", fecha_inicio.isoformat()
            ).lte("fecha_accion", fecha_fin.isoformat()).execute()
            
            return {
                "total_acciones": total_acciones,
                "inserts": insert_response.count or 0,
                "updates": update_response.count or 0,
                "deletes": delete_response.count or 0,
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de auditoría: {e}")
            return {
                "total_acciones": 0,
                "inserts": 0,
                "updates": 0,
                "deletes": 0,
                "error": str(e)
            }
    
    @handle_supabase_error
    def cleanup_old_records(self, days_to_keep: int = 365) -> int:
        """
        Limpia registros de auditoría antiguos
        
        Args:
            days_to_keep: Días a mantener (por defecto 1 año)
            
        Returns:
            Número de registros eliminados
        """
        from datetime import timedelta
        
        fecha_limite = date.today() - timedelta(days=days_to_keep)
        
        logger.info(f"Limpiando registros de auditoría anteriores a {fecha_limite}")
        
        # Obtener registros a eliminar
        old_records = self.table.select("id").lt("fecha_accion", fecha_limite.isoformat()).execute()
        count_to_delete = len(old_records.data) if old_records.data else 0
        
        if count_to_delete > 0:
            # Eliminar registros antiguos
            delete_response = self.table.delete().lt("fecha_accion", fecha_limite.isoformat()).execute()
            logger.info(f"Eliminados {count_to_delete} registros de auditoría antiguos")
        
        return count_to_delete


# Instancia única para importar
auditoria_table = AuditoriaTable()