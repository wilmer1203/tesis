"""
Validaciones específicas para el módulo de servicios
"""
import re
from decimal import Decimal
from typing import Dict, Any, Optional

def validar_codigo_servicio(codigo: str) -> Optional[str]:
    """
    Valida el código del servicio según la restricción:
    chk_servicios_codigo check (codigo ~ '^[A-Z0-9]+$')
    
    Args:
        codigo: Código a validar
        
    Returns:
        Mensaje de error o None si es válido
    """
    if not codigo:
        return "El código es requerido"
        
    if not re.match(r'^[A-Z0-9]+$', codigo):
        return "El código debe contener solo letras mayúsculas y números"
        
    if len(codigo) > 20:
        return "El código no puede exceder 20 caracteres"
    
    return None

def validar_nombre_servicio(nombre: str) -> Optional[str]:
    """
    Valida el nombre del servicio
    
    Args:
        nombre: Nombre a validar
        
    Returns:
        Mensaje de error o None si es válido
    """
    if not nombre:
        return "El nombre es requerido"
        
    if len(nombre) > 100:
        return "El nombre no puede exceder 100 caracteres"
    
    return None

def validar_precio(precio: Any, campo: str) -> Optional[str]:
    """
    Valida el precio según las restricciones:
    chk_servicios_precio_bs/usd check (precio > 0)
    
    Args:
        precio: Precio a validar
        campo: Nombre del campo (bs/usd) para el mensaje
        
    Returns:
        Mensaje de error o None si es válido
    """
    try:
        precio_decimal = Decimal(str(precio))
        if precio_decimal <= 0:
            return f"El precio en {campo} debe ser mayor a 0"
            
        # Validar que no exceda 10 dígitos con 2 decimales
        if len(str(precio_decimal)) > 13:  # 10 dígitos + punto + 2 decimales
            return f"El precio en {campo} excede el máximo permitido"
            
    except (ValueError, TypeError, decimal.InvalidOperation):
        return f"El precio en {campo} debe ser un número válido"
    
    return None

def validar_duracion(duracion: str) -> Optional[str]:
    """
    Valida la duración estimada (interval en PostgreSQL)
    
    Args:
        duracion: Duración en formato HH:MM:SS o número de minutos
        
    Returns:
        Mensaje de error o None si es válido
    """
    # Si es un número, asumimos que son minutos
    if str(duracion).isdigit():
        minutos = int(duracion)
        if minutos <= 0:
            return "La duración debe ser mayor a 0 minutos"
        if minutos > 480:  # 8 horas máximo
            return "La duración no puede exceder 8 horas"
        return None
        
    # Si es formato interval HH:MM:SS
    try:
        if not re.match(r'^\d{2}:\d{2}:\d{2}$', duracion):
            return "Formato de duración inválido. Use HH:MM:SS"
            
        horas, minutos, segundos = map(int, duracion.split(':'))
        total_minutos = horas * 60 + minutos + segundos/60
        
        if total_minutos <= 0:
            return "La duración debe ser mayor a 0"
        if total_minutos > 480:
            return "La duración no puede exceder 8 horas"
            
    except ValueError:
        return "Formato de duración inválido"
    
    return None

def validar_categoria(categoria: str) -> Optional[str]:
    """
    Valida la categoría del servicio
    
    Args:
        categoria: Categoría a validar
        
    Returns:
        Mensaje de error o None si es válido
    """
    CATEGORIAS_VALIDAS = {
        'preventiva', 'restaurativa', 'estetica', 'cirugia',
        'endodoncia', 'protesis', 'ortodoncia', 'implantes',
        'pediatrica', 'diagnostico', 'emergencia', 'otro'
    }
    
    if not categoria:
        return "La categoría es requerida"
        
    if len(categoria) > 50:
        return "La categoría no puede exceder 50 caracteres"
        
    if categoria.lower() not in CATEGORIAS_VALIDAS:
        return "Categoría inválida"
    
    return None