"""
Operaciones CRUD para la tabla configuracion_sistema
Maneja configuraciones globales del sistema
"""
from typing import Dict, List, Optional, Any, Union
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class ConfiguracionSistemaTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para configuración del sistema
    """
    
    def __init__(self):
        super().__init__('configuracion_sistema')
    
    @handle_supabase_error
    def get_config_by_key(self, clave: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una configuración por su clave
        
        Args:
            clave: Clave de la configuración
            
        Returns:
            Configuración encontrada o None
        """
        logger.info(f"Obteniendo configuración: {clave}")
        response = self.table.select("*").eq("clave", clave).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_config_value(self, clave: str, default_value: Any = None) -> Any:
        """
        Obtiene solo el valor de una configuración
        
        Args:
            clave: Clave de la configuración
            default_value: Valor por defecto si no existe
            
        Returns:
            Valor de la configuración o valor por defecto
        """
        config = self.get_config_by_key(clave)
        if config and "valor" in config:
            return config["valor"]
        return default_value
    
    @handle_supabase_error
    def get_by_category(self, categoria: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las configuraciones de una categoría
        
        Args:
            categoria: Categoría de configuraciones
            
        Returns:
            Lista de configuraciones de la categoría
        """
        logger.info(f"Obteniendo configuraciones de categoría: {categoria}")
        query = self.table.select("*").eq("categoria", categoria).order("clave")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def get_public_configs(self) -> List[Dict[str, Any]]:
        """
        Obtiene solo las configuraciones públicas
        
        Returns:
            Lista de configuraciones públicas
        """
        logger.info("Obteniendo configuraciones públicas")
        query = self.table.select("*").eq("es_publica", True).order("categoria, clave")
        response = query.execute()
        return response.data or []
    
    @handle_supabase_error
    def set_config(self,
                  clave: str,
                  valor: Any,
                  descripcion: str,
                  categoria: str,
                  tipo_dato: str = "string",
                  es_publica: bool = False,
                  modificado_por: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea o actualiza una configuración
        
        Args:
            clave: Clave única de la configuración
            valor: Valor de la configuración
            descripcion: Descripción de qué hace la configuración
            categoria: Categoría de la configuración
            tipo_dato: Tipo de dato (string, number, boolean, json, array)
            es_publica: Si la configuración es pública
            modificado_por: Usuario que modifica la configuración
            
        Returns:
            Configuración creada o actualizada
        """
        # Verificar si la configuración ya existe
        existing = self.get_config_by_key(clave)
        
        data = {
            "clave": clave,
            "valor": valor,
            "descripcion": descripcion,
            "categoria": categoria,
            "tipo_dato": tipo_dato,
            "es_publica": es_publica
        }
        
        if modificado_por:
            data["modificado_por"] = modificado_por
        
        if existing:
            # Actualizar existente
            logger.info(f"Actualizando configuración existente: {clave}")
            return self.update(existing["id"], data)
        else:
            # Crear nueva
            logger.info(f"Creando nueva configuración: {clave}")
            return self.create(data)
    
    @handle_supabase_error
    def update_config_value(self, clave: str, nuevo_valor: Any, modificado_por: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Actualiza solo el valor de una configuración existente
        
        Args:
            clave: Clave de la configuración
            nuevo_valor: Nuevo valor
            modificado_por: Usuario que modifica
            
        Returns:
            Configuración actualizada o None si no existe
        """
        config = self.get_config_by_key(clave)
        if not config:
            logger.warning(f"Configuración no encontrada: {clave}")
            return None
        
        data = {"valor": nuevo_valor}
        if modificado_por:
            data["modificado_por"] = modificado_por
        
        logger.info(f"Actualizando valor de configuración: {clave}")
        return self.update(config["id"], data)
    
    @handle_supabase_error
    def delete_config(self, clave: str) -> bool:
        """
        Elimina una configuración
        
        Args:
            clave: Clave de la configuración a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        config = self.get_config_by_key(clave)
        if not config:
            logger.warning(f"Configuración no encontrada para eliminar: {clave}")
            return False
        
        logger.info(f"Eliminando configuración: {clave}")
        return self.delete(config["id"])
    
    def get_default_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtiene las configuraciones por defecto del sistema
        
        Returns:
            Diccionario con configuraciones por defecto organizadas por categoría
        """
        return {
            "clinica": {
                "nombre_clinica": {
                    "valor": "Clínica Odontológica",
                    "descripcion": "Nombre de la clínica",
                    "tipo_dato": "string",
                    "es_publica": True
                },
                "direccion_clinica": {
                    "valor": "",
                    "descripcion": "Dirección de la clínica",
                    "tipo_dato": "string",
                    "es_publica": True
                },
                "telefono_clinica": {
                    "valor": "",
                    "descripcion": "Teléfono principal de la clínica",
                    "tipo_dato": "string",
                    "es_publica": True
                }
            },
            "consultas": {
                "duracion_consulta_default": {
                    "valor": 30,
                    "descripcion": "Duración por defecto de las consultas en minutos",
                    "tipo_dato": "number",
                    "es_publica": False
                },
                "hora_inicio_atencion": {
                    "valor": "08:00",
                    "descripcion": "Hora de inicio de atención",
                    "tipo_dato": "string",
                    "es_publica": False
                },
                "hora_fin_atencion": {
                    "valor": "17:00",
                    "descripcion": "Hora de fin de atención",
                    "tipo_dato": "string",
                    "es_publica": False
                }
            },
            "pagos": {
                "metodos_pago_habilitados": {
                    "valor": ["efectivo", "tarjeta_credito", "tarjeta_debito", "transferencia"],
                    "descripcion": "Métodos de pago habilitados en el sistema",
                    "tipo_dato": "array",
                    "es_publica": False
                },
                "moneda_default": {
                    "valor": "COP",
                    "descripcion": "Moneda por defecto del sistema",
                    "tipo_dato": "string",
                    "es_publica": True
                }
            },
            "sistema": {
                "version_sistema": {
                    "valor": "1.0.0",
                    "descripcion": "Versión actual del sistema",
                    "tipo_dato": "string",
                    "es_publica": True
                },
                "mantenimiento_programado": {
                    "valor": False,
                    "descripcion": "Indica si hay mantenimiento programado",
                    "tipo_dato": "boolean",
                    "es_publica": True
                }
            }
        }


# Instancia única para importar
configuracion_sistema_table = ConfiguracionSistemaTable()