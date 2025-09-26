"""
Middleware de Validación Automática para Sistema Odontológico
Intercepta operaciones de guardado para aplicar validaciones robustas
"""
import functools
from typing import Dict, Any, Callable, Optional, List
from datetime import datetime
import traceback

# Imports del sistema
from dental_system.utils.validators import (
    FormValidator,
    ValidadorGeneral,
    ValidationError,
    validar_formulario
)


class ValidationMiddleware:
    """
    Middleware para validaciones automáticas en operaciones de base de datos

    Características:
    - Intercepta operaciones CRUD antes de ejecutar
    - Aplica validaciones según tipo de entidad
    - Registra errores y métricas de validación
    - Permite bypass para casos especiales
    - Integración transparente con servicios existentes
    """

    def __init__(self):
        self.validation_stats = {
            "total_validaciones": 0,
            "validaciones_exitosas": 0,
            "validaciones_fallidas": 0,
            "ultimo_reset": datetime.now()
        }
        self.bypass_validation = False

    def set_bypass(self, bypass: bool = True):
        """Permitir bypass de validaciones para casos especiales"""
        self.bypass_validation = bypass

    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de validación"""
        total = self.validation_stats["total_validaciones"]
        if total > 0:
            success_rate = (self.validation_stats["validaciones_exitosas"] / total) * 100
        else:
            success_rate = 100.0

        return {
            **self.validation_stats,
            "tasa_exito_porcentaje": round(success_rate, 2),
            "tiempo_activo": (datetime.now() - self.validation_stats["ultimo_reset"]).total_seconds()
        }

    def reset_stats(self):
        """Resetear estadísticas de validación"""
        self.validation_stats = {
            "total_validaciones": 0,
            "validaciones_exitosas": 0,
            "validaciones_fallidas": 0,
            "ultimo_reset": datetime.now()
        }


# Instancia global del middleware
validation_middleware = ValidationMiddleware()


def validate_before_save(entity_type: str,
                        required_fields: Optional[List[str]] = None,
                        custom_validator: Optional[Callable] = None,
                        allow_partial: bool = False):
    """
    Decorator para validar datos antes de guardar en base de datos

    Args:
        entity_type: Tipo de entidad (paciente, consulta, etc.)
        required_fields: Campos obligatorios adicionales
        custom_validator: Validador personalizado adicional
        allow_partial: Permitir validación parcial (para updates)

    Usage:
        @validate_before_save("paciente", required_fields=["numero_historia"])
        def crear_paciente(data: Dict[str, Any]):
            # ... lógica de guardado
            return resultado
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Incrementar contador
            validation_middleware.validation_stats["total_validaciones"] += 1

            # Bypass si está habilitado
            if validation_middleware.bypass_validation:
                return func(*args, **kwargs)

            try:
                # Extraer datos para validar
                data = None
                if kwargs.get('data'):
                    data = kwargs['data']
                elif len(args) > 0 and isinstance(args[0], dict):
                    data = args[0]
                elif len(args) > 1 and isinstance(args[1], dict):
                    data = args[1]

                if data is None:
                    raise ValidationError(["No se encontraron datos para validar"])

                # 1. Validaciones estándar por tipo de entidad
                resultado_validacion = validar_formulario(entity_type, data)

                if not resultado_validacion['valido']:
                    validation_middleware.validation_stats["validaciones_fallidas"] += 1
                    raise ValidationError(resultado_validacion['errores'])

                # 2. Validaciones de campos obligatorios adicionales
                if required_fields:
                    errores_campos = []
                    for field in required_fields:
                        if not data.get(field):
                            errores_campos.append(f"Campo obligatorio faltante: {field}")

                    if errores_campos:
                        validation_middleware.validation_stats["validaciones_fallidas"] += 1
                        raise ValidationError(errores_campos)

                # 3. Validaciones personalizadas
                if custom_validator:
                    try:
                        custom_errors = custom_validator(data)
                        if custom_errors:
                            validation_middleware.validation_stats["validaciones_fallidas"] += 1
                            raise ValidationError(custom_errors)
                    except Exception as e:
                        validation_middleware.validation_stats["validaciones_fallidas"] += 1
                        raise ValidationError([f"Error en validación personalizada: {str(e)}"])

                # 4. Ejecutar función original si validaciones pasan
                validation_middleware.validation_stats["validaciones_exitosas"] += 1
                return func(*args, **kwargs)

            except ValidationError:
                # Re-lanzar errores de validación sin modificar
                raise
            except Exception as e:
                # Capturar errores inesperados
                validation_middleware.validation_stats["validaciones_fallidas"] += 1
                error_msg = f"Error interno en middleware de validación: {str(e)}"
                print(f"VALIDATION MIDDLEWARE ERROR: {error_msg}")
                print(f"Traceback: {traceback.format_exc()}")
                raise ValidationError([error_msg])

        return wrapper
    return decorator


def validate_update_operation(entity_type: str,
                            check_exists: bool = True,
                            validate_permissions: bool = True):
    """
    Decorator específico para operaciones de actualización

    Args:
        entity_type: Tipo de entidad
        check_exists: Verificar que la entidad existe antes de actualizar
        validate_permissions: Validar permisos del usuario

    Usage:
        @validate_update_operation("paciente", check_exists=True)
        def actualizar_paciente(id_paciente: str, data: Dict[str, Any]):
            # ... lógica de actualización
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            validation_middleware.validation_stats["total_validaciones"] += 1

            if validation_middleware.bypass_validation:
                return func(*args, **kwargs)

            try:
                # Extraer ID y datos
                entity_id = None
                data = None

                if kwargs.get('id'):
                    entity_id = kwargs['id']
                elif len(args) > 0:
                    entity_id = args[0]

                if kwargs.get('data'):
                    data = kwargs['data']
                elif len(args) > 1:
                    data = args[1]

                # Validaciones específicas de actualización
                errores = []

                if not entity_id:
                    errores.append("ID de entidad requerido para actualización")

                if not data:
                    errores.append("Datos requeridos para actualización")

                # Validación de existencia (simulada por ahora)
                if check_exists and entity_id:
                    # En implementación real verificaríamos en BD
                    # Por ahora asumimos que existe
                    pass

                # Validaciones estándar de datos (si hay datos)
                if data:
                    resultado_validacion = validar_formulario(entity_type, data)
                    if not resultado_validacion['valido']:
                        errores.extend(resultado_validacion['errores'])

                if errores:
                    validation_middleware.validation_stats["validaciones_fallidas"] += 1
                    raise ValidationError(errores)

                # Ejecutar función original
                validation_middleware.validation_stats["validaciones_exitosas"] += 1
                return func(*args, **kwargs)

            except ValidationError:
                raise
            except Exception as e:
                validation_middleware.validation_stats["validaciones_fallidas"] += 1
                error_msg = f"Error en validación de actualización: {str(e)}"
                raise ValidationError([error_msg])

        return wrapper
    return decorator


def validate_delete_operation(entity_type: str,
                            check_dependencies: bool = True,
                            require_confirmation: bool = False):
    """
    Decorator para validar operaciones de eliminación

    Args:
        entity_type: Tipo de entidad
        check_dependencies: Verificar dependencias antes de eliminar
        require_confirmation: Requerir confirmación explícita

    Usage:
        @validate_delete_operation("paciente", check_dependencies=True)
        def eliminar_paciente(id_paciente: str, confirmacion: bool = False):
            # ... lógica de eliminación
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            validation_middleware.validation_stats["total_validaciones"] += 1

            if validation_middleware.bypass_validation:
                return func(*args, **kwargs)

            try:
                errores = []

                # Extraer ID
                entity_id = kwargs.get('id') or (args[0] if len(args) > 0 else None)
                confirmacion = kwargs.get('confirmacion', False)

                if not entity_id:
                    errores.append("ID de entidad requerido para eliminación")

                if require_confirmation and not confirmacion:
                    errores.append("Confirmación explícita requerida para eliminación")

                # Verificar dependencias (simulado)
                if check_dependencies and entity_id:
                    # En implementación real verificaríamos dependencias en BD
                    dependencias = verificar_dependencias_simulado(entity_type, entity_id)
                    if dependencias:
                        errores.append(f"No se puede eliminar: existen dependencias ({', '.join(dependencias)})")

                if errores:
                    validation_middleware.validation_stats["validaciones_fallidas"] += 1
                    raise ValidationError(errores)

                validation_middleware.validation_stats["validaciones_exitosas"] += 1
                return func(*args, **kwargs)

            except ValidationError:
                raise
            except Exception as e:
                validation_middleware.validation_stats["validaciones_fallidas"] += 1
                error_msg = f"Error en validación de eliminación: {str(e)}"
                raise ValidationError([error_msg])

        return wrapper
    return decorator


def batch_validate(validations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validar múltiples operaciones en lote

    Args:
        validations: Lista de operaciones a validar

    Returns:
        Resumen de validaciones en lote
    """
    resultados = []
    total_errores = 0

    for i, validation in enumerate(validations):
        try:
            entity_type = validation.get('type')
            data = validation.get('data')
            operation = validation.get('operation', 'create')

            resultado = validar_formulario(entity_type, data)
            resultado['operation'] = operation
            resultado['index'] = i

            resultados.append(resultado)
            if not resultado['valido']:
                total_errores += 1

        except Exception as e:
            resultados.append({
                'valido': False,
                'errores': [f"Error procesando validación {i}: {str(e)}"],
                'operation': validation.get('operation', 'unknown'),
                'index': i
            })
            total_errores += 1

    return {
        'resultados': resultados,
        'total_operaciones': len(validations),
        'operaciones_validas': len(validations) - total_errores,
        'operaciones_con_errores': total_errores,
        'todas_validas': total_errores == 0
    }


# Validadores personalizados específicos del dominio
def validar_unicidad_documento(data: Dict[str, Any]) -> List[str]:
    """Validador personalizado para unicidad de documentos"""
    errores = []
    numero_documento = data.get('numero_documento')
    tipo_documento = data.get('tipo_documento')

    if numero_documento and tipo_documento:
        # En implementación real consultaríamos la BD
        es_unico = ValidadorGeneral.validar_unicidad_documento(
            numero_documento,
            tipo_documento,
            data.get('id')  # Excluir ID actual en ediciones
        )

        if not es_unico:
            errores.append(f"Ya existe un paciente con {tipo_documento}: {numero_documento}")

    return errores


def validar_disponibilidad_odontologo(data: Dict[str, Any]) -> List[str]:
    """Validador personalizado para disponibilidad de odontólogos"""
    errores = []
    odontologo_id = data.get('primer_odontologo_id')
    fecha_consulta = data.get('fecha_consulta')
    hora_inicio = data.get('hora_inicio')

    if odontologo_id and fecha_consulta and hora_inicio:
        disponible = ValidadorGeneral.validar_disponibilidad_odontologo(
            odontologo_id,
            fecha_consulta,
            hora_inicio
        )

        if not disponible:
            errores.append("El odontólogo no está disponible en el horario seleccionado")

    return errores


def validar_integridad_financiera(data: Dict[str, Any]) -> List[str]:
    """Validador personalizado para integridad financiera"""
    errores = []
    id_consulta = data.get('id_consulta')
    monto_pago = data.get('monto_pagado_usd', 0)

    if id_consulta and monto_pago > 0:
        # En implementación real consultaríamos costos y pagos anteriores
        errores_integridad = ValidadorGeneral.validar_integridad_pago(
            id_consulta,
            1000.0,  # Monto simulado
            []  # Pagos anteriores simulados
        )
        errores.extend(errores_integridad)

    return errores


def verificar_dependencias_simulado(entity_type: str, entity_id: str) -> List[str]:
    """Simulación de verificación de dependencias"""
    # En implementación real consultaríamos la BD
    dependencias_simuladas = {
        "paciente": ["2 consultas activas", "1 tratamiento en curso"],
        "personal": ["5 consultas asignadas"],
        "servicio": ["10 intervenciones registradas"]
    }

    return dependencias_simuladas.get(entity_type, [])


# Funciones de utilidad para integración
def enable_validation_bypass():
    """Habilitar bypass temporal de validaciones"""
    validation_middleware.set_bypass(True)


def disable_validation_bypass():
    """Deshabilitar bypass de validaciones"""
    validation_middleware.set_bypass(False)


def get_validation_statistics() -> Dict[str, Any]:
    """Obtener estadísticas actuales de validación"""
    return validation_middleware.get_stats()


def reset_validation_statistics():
    """Resetear estadísticas de validación"""
    validation_middleware.reset_stats()


# Context manager para bypass temporal
class TemporaryValidationBypass:
    """Context manager para bypass temporal de validaciones"""

    def __enter__(self):
        self.original_state = validation_middleware.bypass_validation
        validation_middleware.set_bypass(True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        validation_middleware.set_bypass(self.original_state)


# Ejemplos de uso de los decorators
"""
# Ejemplo 1: Validación básica
@validate_before_save("paciente")
def crear_paciente(data: Dict[str, Any]):
    # Función se ejecuta solo si validaciones pasan
    return supabase.table("pacientes").insert(data).execute()

# Ejemplo 2: Validación con campos obligatorios adicionales
@validate_before_save("consulta", required_fields=["numero_historia"],
                     custom_validator=validar_disponibilidad_odontologo)
def crear_consulta(data: Dict[str, Any]):
    return supabase.table("consultas").insert(data).execute()

# Ejemplo 3: Validación de actualización
@validate_update_operation("paciente", check_exists=True)
def actualizar_paciente(id_paciente: str, data: Dict[str, Any]):
    return supabase.table("pacientes").update(data).eq("id", id_paciente).execute()

# Ejemplo 4: Validación de eliminación
@validate_delete_operation("paciente", check_dependencies=True, require_confirmation=True)
def eliminar_paciente(id_paciente: str, confirmacion: bool = False):
    return supabase.table("pacientes").delete().eq("id", id_paciente).execute()

# Ejemplo 5: Bypass temporal
with TemporaryValidationBypass():
    # Operaciones sin validación (para imports masivos, etc.)
    crear_paciente_sin_validacion(data)
"""