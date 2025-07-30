

"""
🔧 SUPABASE HELPERS OPTIMIZADO - Sistema Dental Odontomara
==========================================================
Utilidades avanzadas para validación, manejo de datos y optimización
de operaciones con Supabase. Incluye cache, validadores especializados
y funciones específicas para el dominio dental.

NUEVO: Funciones especializadas para el contexto odontológico
"""

from typing import Any, Dict, List, Optional, Union, TypeVar, Callable
from functools import lru_cache, wraps
import json
import re
from datetime import datetime, date
from decimal import Decimal
import logging

# ==========================================
# CONFIGURACIÓN Y LOGGING
# ==========================================

logger = logging.getLogger(__name__)

# TypeVars para tipado genérico
T = TypeVar('T')

# ==========================================
# 🔒 VALIDADORES DE DATOS SEGUROS
# ==========================================

def safe_get(data: Any, key: str, default: Any = "") -> Any:
    """
    Obtener valor de forma segura de un diccionario.
    
    Args:
        data: Diccionario o cualquier objeto
        key: Clave a buscar
        default: Valor por defecto
        
    Returns:
        Valor encontrado o default
    """
    if not data or not isinstance(data, dict):
        return default
    return data.get(key, default)


def safe_get_nested(data: Any, *keys: str, default: Any = "") -> Any:
    """
    Obtener valor anidado de forma segura.
    
    Args:
        data: Diccionario base
        *keys: Secuencia de claves anidadas
        default: Valor por defecto
        
    Returns:
        Valor encontrado o default
        
    Example:
        # En lugar de: data.get('usuarios', {}).get('nombre', '')
        # Usar: safe_get_nested(data, 'usuarios', 'nombre')
    """
    current = data
    
    for key in keys:
        if not current or not isinstance(current, dict):
            return default
        current = current.get(key)
        
    return current if current is not None else default


def validate_supabase_response(response: Any) -> List[Dict[str, Any]]:
    """
    Validar y limpiar respuesta de Supabase.
    
    Args:
        response: Respuesta de Supabase
        
    Returns:
        Lista limpia de diccionarios válidos
    """
    if not response or not hasattr(response, 'data'):
        return []
    
    data = response.data
    if not data or not isinstance(data, list):
        return []
    
    # Filtrar elementos None y no-diccionarios
    return [
        item for item in data
        if item is not None and isinstance(item, dict)
    ]


def safe_search_filter(
    items: List[Dict[str, Any]], 
    search_term: str, 
    fields: List[str]
) -> List[Dict[str, Any]]:
    """
    Filtrar lista de forma segura por término de búsqueda.
    
    Args:
        items: Lista de elementos a filtrar
        search_term: Término de búsqueda
        fields: Lista de campos donde buscar (soporta anidación con '.')
        
    Returns:
        Lista filtrada
        
    Example:
        safe_search_filter(
            personal_data, 
            "juan", 
            ["usuarios.nombre_completo", "usuarios.email", "numero_documento"]
        )
    """
    if not search_term or not fields:
        return items
    
    search_term = search_term.lower()
    filtered_items = []
    
    for item in items:
        if not item or not isinstance(item, dict):
            continue
            
        try:
            # Buscar en cada campo especificado
            for field in fields:
                if '.' in field:
                    # Campo anidado (ej: "usuarios.nombre")
                    keys = field.split('.')
                    value = safe_get_nested(item, *keys)
                else:
                    # Campo simple
                    value = safe_get(item, field)
                
                # Convertir a string y buscar
                value_str = str(value).lower() if value else ""
                if search_term in value_str:
                    filtered_items.append(item)
                    break  # Encontrado en este campo, no buscar en otros
                    
        except (AttributeError, TypeError, KeyError) as e:
            logger.warning(f"Error en búsqueda para item: {e}")
            continue
    
    return filtered_items


def safe_convert_type(value: Any, target_type: type, default: Any = None) -> Any:
    """
    Convertir valor a tipo específico de forma segura.
    
    Args:
        value: Valor a convertir
        target_type: Tipo objetivo (str, int, float, bool)
        default: Valor por defecto si conversión falla
        
    Returns:
        Valor convertido o default
    """
    if value is None:
        return default
    
    try:
        if target_type == str:
            return str(value)
        elif target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        elif target_type == bool:
            return bool(value)
        else:
            return target_type(value)
    except (ValueError, TypeError):
        return default

# ==========================================
# 🦷 VALIDADORES ESPECÍFICOS DENTALES
# ==========================================

def validate_numero_diente(numero: int) -> bool:
    """
    Validar número de diente según notación FDI.
    
    Args:
        numero: Número del diente (ej: 11, 21, 47)
        
    Returns:
        True si es válido según FDI
    """
    if not isinstance(numero, int):
        return False
    
    # Dientes permanentes: 11-18, 21-28, 31-38, 41-48
    permanent_ranges = [
        range(11, 19),  # Cuadrante 1
        range(21, 29),  # Cuadrante 2
        range(31, 39),  # Cuadrante 3
        range(41, 49),  # Cuadrante 4
    ]
    
    # Dientes temporales: 51-55, 61-65, 71-75, 81-85
    temporal_ranges = [
        range(51, 56),  # Cuadrante 5
        range(61, 66),  # Cuadrante 6
        range(71, 76),  # Cuadrante 7
        range(81, 86),  # Cuadrante 8
    ]
    
    all_ranges = permanent_ranges + temporal_ranges
    return any(numero in rango for rango in all_ranges)


def validate_documento_identidad(documento: str, tipo: str = "CC") -> bool:
    """
    Validar documento de identidad venezolano.
    
    Args:
        documento: Número de documento
        tipo: Tipo de documento (CC, Pasaporte, etc.)
        
    Returns:
        True si es válido
    """
    if not documento or not isinstance(documento, str):
        return False
    
    documento = documento.strip()
    
    if tipo == "CC":
        # Cédula venezolana: entre 6 y 10 dígitos
        return documento.isdigit() and 6 <= len(documento) <= 10
    elif tipo == "Pasaporte":
        # Pasaporte: formato más flexible
        return len(documento) >= 6 and len(documento) <= 15
    else:
        # Otros tipos: validación básica
        return len(documento) >= 6


def validate_telefono_venezolano(telefono: str) -> bool:
    """
    Validar número de teléfono venezolano.
    
    Args:
        telefono: Número de teléfono
        
    Returns:
        True si es válido
    """
    if not telefono or not isinstance(telefono, str):
        return False
    
    # Limpiar el número
    clean_phone = re.sub(r'[^\d+]', '', telefono)
    
    # Patrones válidos para Venezuela
    patterns = [
        r'^\+584\d{8}$',    # +584xxxxxxxx (móvil)
        r'^584\d{8}$',      # 584xxxxxxxx (móvil sin +)
        r'^04\d{8}$',       # 04xxxxxxxx (móvil nacional)
        r'^\+5821\d{7}$',   # +5821xxxxxxx (fijo)
        r'^5821\d{7}$',     # 5821xxxxxxx (fijo sin +)
        r'^021\d{7}$',      # 021xxxxxxx (fijo nacional)
    ]
    
    return any(re.match(pattern, clean_phone) for pattern in patterns)


def validate_email_domain(email: str, allowed_domains: List[str] = None) -> bool:
    """
    Validar email con dominios permitidos opcionales.
    
    Args:
        email: Dirección de email
        allowed_domains: Lista de dominios permitidos (opcional)
        
    Returns:
        True si es válido
    """
    if not email or not isinstance(email, str):
        return False
    
    # Patrón básico de email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False
    
    # Verificar dominios permitidos si se especifican
    if allowed_domains:
        domain = email.split('@')[1].lower()
        return domain in [d.lower() for d in allowed_domains]
    
    return True

# ==========================================
# 💰 VALIDADORES FINANCIEROS
# ==========================================

def validate_monto_monetary(monto: Union[str, int, float, Decimal]) -> bool:
    """
    Validar monto monetario (positivo, máximo 2 decimales).
    
    Args:
        monto: Monto a validar
        
    Returns:
        True si es válido
    """
    try:
        if isinstance(monto, str):
            # Limpiar string de caracteres no numéricos excepto punto y coma
            clean_monto = re.sub(r'[^\d.,]', '', monto)
            clean_monto = clean_monto.replace(',', '.')
            monto = float(clean_monto)
        
        # Debe ser positivo
        if float(monto) < 0:
            return False
        
        # Máximo 2 decimales
        decimal_places = len(str(float(monto)).split('.')[1]) if '.' in str(float(monto)) else 0
        return decimal_places <= 2
        
    except (ValueError, TypeError, IndexError):
        return False


def format_currency_venezuelan(amount: Union[int, float, Decimal], currency: str = "Bs") -> str:
    """
    Formatear cantidad como moneda venezolana.
    
    Args:
        amount: Cantidad numérica
        currency: Símbolo de moneda
        
    Returns:
        String formateado (ej: "Bs 1.234,56")
    """
    try:
        # Convertir a float si es necesario
        if isinstance(amount, (str, Decimal)):
            amount = float(amount)
        
        # Formatear con separadores de miles y 2 decimales
        formatted = f"{amount:,.2f}"
        
        # Cambiar punto por coma para decimales (estilo venezolano)
        formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
        
        return f"{currency} {formatted}"
    
    except (ValueError, TypeError):
        return f"{currency} 0,00"

# ==========================================
# 📊 FUNCIONES DE AGREGACIÓN Y ESTADÍSTICAS
# ==========================================

@lru_cache(maxsize=128)
def calculate_age_from_birthdate(birthdate_str: str) -> Optional[int]:
    """
    Calcular edad desde fecha de nacimiento (con cache).
    
    Args:
        birthdate_str: Fecha en formato ISO (YYYY-MM-DD)
        
    Returns:
        Edad en años o None si es inválida
    """
    try:
        birthdate = datetime.fromisoformat(birthdate_str).date()
        today = date.today()
        
        age = today.year - birthdate.year
        
        # Ajustar si el cumpleaños no ha pasado este año
        if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
            age -= 1
            
        return age if age >= 0 else None
        
    except (ValueError, TypeError):
        return None


def aggregate_patient_stats(patients_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Agregar estadísticas de pacientes de forma eficiente.
    
    Args:
        patients_data: Lista de datos de pacientes
        
    Returns:
        Diccionario con estadísticas agregadas
    """
    if not patients_data:
        return {
            "total": 0,
            "por_genero": {},
            "por_rango_edad": {},
            "promedio_edad": 0.0,
            "con_email": 0,
            "con_telefono": 0
        }
    
    stats = {
        "total": len(patients_data),
        "por_genero": {},
        "por_rango_edad": {"0-17": 0, "18-35": 0, "36-55": 0, "56+": 0},
        "edades": [],
        "con_email": 0,
        "con_telefono": 0
    }
    
    for patient in patients_data:
        # Género
        genero = safe_get(patient, "genero", "no_especificado")
        stats["por_genero"][genero] = stats["por_genero"].get(genero, 0) + 1
        
        # Edad
        edad = safe_get(patient, "edad")
        if edad and isinstance(edad, int):
            stats["edades"].append(edad)
            
            # Rangos de edad
            if edad < 18:
                stats["por_rango_edad"]["0-17"] += 1
            elif edad < 36:
                stats["por_rango_edad"]["18-35"] += 1
            elif edad < 56:
                stats["por_rango_edad"]["36-55"] += 1
            else:
                stats["por_rango_edad"]["56+"] += 1
        
        # Email
        if safe_get(patient, "email"):
            stats["con_email"] += 1
        
        # Teléfono
        if safe_get(patient, "telefono_1") or safe_get(patient, "telefono_2"):
            stats["con_telefono"] += 1
    
    # Calcular promedio de edad
    if stats["edades"]:
        stats["promedio_edad"] = sum(stats["edades"]) / len(stats["edades"])
    else:
        stats["promedio_edad"] = 0.0
    
    # Limpiar lista de edades (no necesaria en resultado final)
    del stats["edades"]
    
    return stats

# ==========================================
# 🔄 DECORADORES Y MANEJO DE ERRORES
# ==========================================

def handle_supabase_errors(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorador para manejar errores comunes de Supabase.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                logger.error(f"Datos nulos en {func.__name__}: {e}")
                return [] if 'list' in str(func.__annotations__.get('return', '')) else None
            raise
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}")
            raise
    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorador para reintentar operaciones fallidas.
    
    Args:
        max_retries: Número máximo de reintentos
        delay: Retraso entre reintentos en segundos
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Intento {attempt + 1} falló en {func.__name__}: {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"Todos los intentos fallaron en {func.__name__}: {e}")
            
            raise last_exception
        return wrapper
    return decorator

# ==========================================
# 🔍 FUNCIONES DE BÚSQUEDA AVANZADA
# ==========================================

def fuzzy_search_patients(
    patients: List[Dict[str, Any]], 
    search_term: str,
    threshold: float = 0.6
) -> List[Dict[str, Any]]:
    """
    Búsqueda difusa de pacientes (por si hay errores de escritura).
    
    Args:
        patients: Lista de pacientes
        search_term: Término de búsqueda
        threshold: Umbral de similitud (0.0 - 1.0)
        
    Returns:
        Lista de pacientes que coinciden difusamente
    """
    try:
        from difflib import SequenceMatcher
    except ImportError:
        # Fallback a búsqueda normal si no está disponible difflib
        return safe_search_filter(
            patients, 
            search_term,
            ["primer_nombre", "primer_apellido", "numero_documento", "email"]
        )
    
    def similarity(a: str, b: str) -> float:
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    search_term = search_term.lower()
    results = []
    
    for patient in patients:
        # Campos a buscar
        searchable_fields = [
            f"{safe_get(patient, 'primer_nombre', '')} {safe_get(patient, 'primer_apellido', '')}",
            safe_get(patient, "numero_documento", ""),
            safe_get(patient, "email", ""),
            safe_get(patient, "telefono_1", ""),
        ]
        
        # Verificar similitud en cualquier campo
        max_similarity = 0.0
        for field_value in searchable_fields:
            if field_value:
                sim = similarity(search_term, str(field_value))
                max_similarity = max(max_similarity, sim)
        
        if max_similarity >= threshold:
            results.append(patient)
    
    # Ordenar por similitud descendente
    results.sort(key=lambda p: max(
        similarity(search_term, f"{safe_get(p, 'primer_nombre', '')} {safe_get(p, 'primer_apellido', '')}")
        for _ in [None]  # Placeholder para generar solo una vez
    ), reverse=True)
    
    return results

# ==========================================
# 📋 FUNCIONES DE EXPORTACIÓN
# ==========================================

def export_to_json_safe(data: Any, filename: str = None) -> str:
    """
    Exportar datos a JSON de forma segura.
    
    Args:
        data: Datos a exportar
        filename: Nombre del archivo (opcional)
        
    Returns:
        JSON string o ruta del archivo
    """
    def json_serializer(obj):
        """Serializar objetos no serializables por defecto"""
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Objeto de tipo {type(obj)} no es serializable")
    
    json_str = json.dumps(data, default=json_serializer, indent=2, ensure_ascii=False)
    
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_str)
            return filename
        except Exception as e:
            logger.error(f"Error escribiendo archivo {filename}: {e}")
            return json_str
    
    return json_str

# ==========================================
# 🧪 FUNCIONES DE TESTING Y VALIDACIÓN
# ==========================================

def validate_data_integrity(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validar integridad de datos contra un esquema.
    
    Args:
        data: Datos a validar
        schema: Esquema de validación
        
    Returns:
        Diccionario con errores encontrados
    """
    errors = {"missing": [], "invalid": [], "warnings": []}
    
    # Verificar campos requeridos
    required_fields = schema.get("required", [])
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            errors["missing"].append(f"Campo requerido '{field}' está vacío")
    
    # Verificar tipos de datos
    field_types = schema.get("types", {})
    for field, expected_type in field_types.items():
        if field in data and data[field] is not None:
            if not isinstance(data[field], expected_type):
                errors["invalid"].append(f"Campo '{field}' debe ser de tipo {expected_type.__name__}")
    
    # Validaciones personalizadas
    validators = schema.get("validators", {})
    for field, validator_func in validators.items():
        if field in data and data[field] is not None:
            try:
                if not validator_func(data[field]):
                    errors["invalid"].append(f"Campo '{field}' no pasa la validación")
            except Exception as e:
                errors["warnings"].append(f"Error validando '{field}': {e}")
    
    return errors

# ==========================================
# 📤 EXPORTS
# ==========================================

__all__ = [
    # Validadores básicos
    "safe_get",
    "safe_get_nested", 
    "validate_supabase_response",
    "safe_search_filter",
    "safe_convert_type",
    
    # Validadores dentales
    "validate_numero_diente",
    "validate_documento_identidad",
    "validate_telefono_venezolano",
    "validate_email_domain",
    
    # Validadores financieros
    "validate_monto_monetary",
    "format_currency_venezuelan",
    
    # Estadísticas y agregación
    "calculate_age_from_birthdate",
    "aggregate_patient_stats",
    
    # Decoradores
    "handle_supabase_errors",
    "retry_on_failure",
    
    # Búsqueda avanzada
    "fuzzy_search_patients",
    
    # Exportación
    "export_to_json_safe",
    
    # Validación de integridad
    "validate_data_integrity",
]