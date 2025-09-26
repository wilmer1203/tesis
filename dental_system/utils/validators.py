"""
Sistema de Validaciones Robustas para Sistema Odontológico
Validaciones enterprise para prevenir errores de usuario y mantener integridad de datos
"""
import re
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, date
from decimal import Decimal

# Imports del sistema
from dental_system.models.pacientes_models import PacienteModel
from dental_system.models.consultas_models import ConsultaModel
from dental_system.models.form_models import (
    PacienteFormModel,
    ConsultaFormModel,
    PersonalFormModel,
    ServicioFormModel,
    PagoFormModel,
    IntervencionFormModel
)


class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""
    def __init__(self, errores: List[str]):
        self.errores = errores
        super().__init__(f"Errores de validación: {', '.join(errores)}")


class FormValidator:
    """
    Validador principal para todos los formularios del sistema odontológico

    Características:
    - Validaciones específicas por formulario
    - Validaciones de formato venezolano (CI, teléfonos)
    - Validaciones de negocio específicas
    - Validaciones de integridad de datos
    - Mensajes de error descriptivos en español
    """

    # Patrones de validación venezolanos
    PATRON_CEDULA_VENEZOLANA = r'^[VE]\d{7,8}$'
    PATRON_TELEFONO_MOVIL = r'^04\d{9}$'
    PATRON_TELEFONO_FIJO = r'^02\d{9}$'
    PATRON_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Listas de valores válidos
    GENEROS_VALIDOS = ["masculino", "femenino", "otro"]
    TIPOS_DOCUMENTO_VALIDOS = ["CI", "Pasaporte", "RIF"]
    ESTADOS_CONSULTA_VALIDOS = ["programada", "en_espera", "en_curso", "completada", "cancelada"]
    ESPECIALIDADES_VALIDAS = [
        "Odontología General", "Endodoncia", "Ortodoncia", "Periodoncia",
        "Cirugía Oral", "Odontopediatría", "Prostodoncia", "Implantología"
    ]

    @staticmethod
    def validar_paciente(data: Union[PacienteFormModel, Dict[str, Any]]) -> List[str]:
        """
        Validaciones específicas de pacientes

        Args:
            data: Datos del paciente (FormModel o diccionario)

        Returns:
            Lista de errores encontrados
        """
        errores = []

        # Convertir a diccionario si es FormModel
        if hasattr(data, '__dict__'):
            data_dict = data.__dict__
        else:
            data_dict = data

        # 1. Validaciones de campos obligatorios
        campos_obligatorios = {
            'primer_nombre': 'Primer nombre',
            'primer_apellido': 'Primer apellido',
            'numero_documento': 'Número de documento',
            'tipo_documento': 'Tipo de documento',
            'fecha_nacimiento': 'Fecha de nacimiento'
        }

        for campo, nombre_campo in campos_obligatorios.items():
            if not data_dict.get(campo) or data_dict[campo].strip() == "":
                errores.append(f"{nombre_campo} es obligatorio")

        # 2. Validar formato de cédula venezolana
        numero_documento = data_dict.get('numero_documento', '')
        tipo_documento = data_dict.get('tipo_documento', '')

        if tipo_documento == 'CI' and numero_documento:
            if not re.match(FormValidator.PATRON_CEDULA_VENEZOLANA, numero_documento):
                errores.append("Cédula debe tener formato V12345678 o E12345678")

        # 3. Validar teléfonos venezolanos
        celular_1 = data_dict.get('celular_1', '')
        if celular_1 and not re.match(FormValidator.PATRON_TELEFONO_MOVIL, celular_1):
            errores.append("Celular debe tener formato 04121234567 (11 dígitos)")

        celular_2 = data_dict.get('celular_2', '')
        if celular_2 and not re.match(FormValidator.PATRON_TELEFONO_MOVIL, celular_2):
            errores.append("Segundo celular debe tener formato 04121234567")

        # 4. Validar email
        email = data_dict.get('email', '')
        if email and not re.match(FormValidator.PATRON_EMAIL, email):
            errores.append("Email debe tener formato válido (usuario@dominio.com)")

        # 5. Validar fecha de nacimiento
        fecha_nacimiento = data_dict.get('fecha_nacimiento')
        if fecha_nacimiento:
            try:
                if isinstance(fecha_nacimiento, str):
                    fecha_obj = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
                else:
                    fecha_obj = fecha_nacimiento

                # No puede ser futuro
                if fecha_obj > date.today():
                    errores.append("Fecha de nacimiento no puede ser futura")

                # Edad mínima y máxima razonable
                edad = (date.today() - fecha_obj).days // 365
                if edad > 120:
                    errores.append("Edad no puede ser mayor a 120 años")
                if edad < 0:
                    errores.append("Fecha de nacimiento inválida")

            except (ValueError, TypeError):
                errores.append("Fecha de nacimiento debe tener formato válido (YYYY-MM-DD)")

        # 6. Validar género
        genero = data_dict.get('genero', '')
        if genero and genero not in FormValidator.GENEROS_VALIDOS:
            errores.append(f"Género debe ser uno de: {', '.join(FormValidator.GENEROS_VALIDOS)}")

        # 7. Validaciones de nombres (solo letras y espacios)
        nombres_campos = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']
        for campo in nombres_campos:
            valor = data_dict.get(campo, '')
            if valor and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', valor):
                nombre_campo = campo.replace('_', ' ').title()
                errores.append(f"{nombre_campo} debe contener solo letras y espacios")

        return errores

    @staticmethod
    def validar_intervencion(data: Union[IntervencionFormModel, Dict[str, Any]]) -> List[str]:
        """
        Validaciones de intervenciones odontológicas

        Args:
            data: Datos de la intervención

        Returns:
            Lista de errores encontrados
        """
        errores = []

        if hasattr(data, '__dict__'):
            data_dict = data.__dict__
        else:
            data_dict = data

        # 1. Validar que hay al menos un servicio
        servicios_ids = data_dict.get('servicios_ids', [])
        if not servicios_ids or len(servicios_ids) == 0:
            errores.append("Debe seleccionar al menos un servicio")

        # 2. Validar costos positivos
        costo_total_bs = data_dict.get('costo_total_bs', 0)
        costo_total_usd = data_dict.get('costo_total_usd', 0)

        try:
            costo_bs = float(costo_total_bs) if costo_total_bs else 0
            costo_usd = float(costo_total_usd) if costo_total_usd else 0

            if costo_bs <= 0 and costo_usd <= 0:
                errores.append("El costo total debe ser mayor a cero en al menos una moneda")

            if costo_bs < 0 or costo_usd < 0:
                errores.append("Los costos no pueden ser negativos")

            # Validar límites razonables
            if costo_bs > 10000000:  # 10 millones de BS
                errores.append("Costo en BS no puede exceder 10,000,000")

            if costo_usd > 10000:  # 10 mil USD
                errores.append("Costo en USD no puede exceder 10,000")

        except (ValueError, TypeError):
            errores.append("Los costos deben ser números válidos")

        # 3. Validar campos obligatorios
        if not data_dict.get('id_consulta'):
            errores.append("ID de consulta es obligatorio")

        if not data_dict.get('id_odontologo'):
            errores.append("ID de odontólogo es obligatorio")

        # 4. Validar observaciones (longitud)
        observaciones = data_dict.get('observaciones', '')
        if len(observaciones) > 2000:
            errores.append("Las observaciones no pueden exceder 2000 caracteres")

        # 5. Validar dientes seleccionados (si aplica)
        dientes_afectados = data_dict.get('dientes_afectados', [])
        if dientes_afectados:
            for diente in dientes_afectados:
                if not isinstance(diente, int) or diente < 11 or diente > 48:
                    errores.append(f"Número de diente inválido: {diente}")

        return errores

    @staticmethod
    def validar_consulta(data: Union[ConsultaFormModel, Dict[str, Any]]) -> List[str]:
        """
        Validaciones de consultas

        Args:
            data: Datos de la consulta

        Returns:
            Lista de errores encontrados
        """
        errores = []

        if hasattr(data, '__dict__'):
            data_dict = data.__dict__
        else:
            data_dict = data

        # 1. Campos obligatorios
        if not data_dict.get('numero_historia'):
            errores.append("Número de historia clínica es obligatorio")

        if not data_dict.get('primer_odontologo_id'):
            errores.append("Odontólogo principal es obligatorio")

        if not data_dict.get('motivo_consulta'):
            errores.append("Motivo de consulta es obligatorio")

        # 2. Validar estado de consulta
        estado = data_dict.get('estado_consulta', '')
        if estado and estado not in FormValidator.ESTADOS_CONSULTA_VALIDOS:
            errores.append(f"Estado de consulta debe ser uno de: {', '.join(FormValidator.ESTADOS_CONSULTA_VALIDOS)}")

        # 3. Validar fecha de consulta
        fecha_consulta = data_dict.get('fecha_consulta')
        if fecha_consulta:
            try:
                if isinstance(fecha_consulta, str):
                    fecha_obj = datetime.strptime(fecha_consulta, '%Y-%m-%d').date()
                else:
                    fecha_obj = fecha_consulta

                # No puede ser más de un año en el futuro
                if fecha_obj > date.today().replace(year=date.today().year + 1):
                    errores.append("Fecha de consulta no puede ser más de un año en el futuro")

                # No puede ser más de 5 años en el pasado
                if fecha_obj < date.today().replace(year=date.today().year - 5):
                    errores.append("Fecha de consulta no puede ser más de 5 años en el pasado")

            except (ValueError, TypeError):
                errores.append("Fecha de consulta debe tener formato válido")

        # 4. Validar motivo de consulta (longitud)
        motivo = data_dict.get('motivo_consulta', '')
        if len(motivo) > 500:
            errores.append("Motivo de consulta no puede exceder 500 caracteres")

        return errores

    @staticmethod
    def validar_personal(data: Union[PersonalFormModel, Dict[str, Any]]) -> List[str]:
        """
        Validaciones de personal

        Args:
            data: Datos del personal

        Returns:
            Lista de errores encontrados
        """
        errores = []

        if hasattr(data, '__dict__'):
            data_dict = data.__dict__
        else:
            data_dict = data

        # 1. Campos obligatorios
        campos_obligatorios = {
            'primer_nombre': 'Primer nombre',
            'primer_apellido': 'Primer apellido',
            'numero_documento': 'Número de documento',
            'especialidad': 'Especialidad'
        }

        for campo, nombre_campo in campos_obligatorios.items():
            if not data_dict.get(campo) or data_dict[campo].strip() == "":
                errores.append(f"{nombre_campo} es obligatorio")

        # 2. Validar especialidad
        especialidad = data_dict.get('especialidad', '')
        if especialidad and especialidad not in FormValidator.ESPECIALIDADES_VALIDAS:
            errores.append(f"Especialidad debe ser una de: {', '.join(FormValidator.ESPECIALIDADES_VALIDAS)}")

        # 3. Validar salario
        salario_base = data_dict.get('salario_base', 0)
        try:
            salario = float(salario_base) if salario_base else 0
            if salario < 0:
                errores.append("El salario no puede ser negativo")
            if salario > 100000:  # 100k USD máximo
                errores.append("El salario no puede exceder 100,000 USD")
        except (ValueError, TypeError):
            errores.append("El salario debe ser un número válido")

        # 4. Validar porcentaje de comisión
        porcentaje_comision = data_dict.get('porcentaje_comision', 0)
        try:
            comision = float(porcentaje_comision) if porcentaje_comision else 0
            if comision < 0 or comision > 100:
                errores.append("El porcentaje de comisión debe estar entre 0 y 100")
        except (ValueError, TypeError):
            errores.append("El porcentaje de comisión debe ser un número válido")

        return errores

    @staticmethod
    def validar_pago(data: Union[PagoFormModel, Dict[str, Any]]) -> List[str]:
        """
        Validaciones de pagos

        Args:
            data: Datos del pago

        Returns:
            Lista de errores encontrados
        """
        errores = []

        if hasattr(data, '__dict__'):
            data_dict = data.__dict__
        else:
            data_dict = data

        # 1. Validar montos
        monto_bs = data_dict.get('monto_pagado_bs', 0)
        monto_usd = data_dict.get('monto_pagado_usd', 0)

        try:
            bs = float(monto_bs) if monto_bs else 0
            usd = float(monto_usd) if monto_usd else 0

            if bs <= 0 and usd <= 0:
                errores.append("Debe registrar un monto mayor a cero en al menos una moneda")

            if bs < 0 or usd < 0:
                errores.append("Los montos no pueden ser negativos")

        except (ValueError, TypeError):
            errores.append("Los montos deben ser números válidos")

        # 2. Validar método de pago
        metodo_pago = data_dict.get('metodo_pago', '')
        metodos_validos = ['efectivo', 'transferencia', 'tarjeta_debito', 'tarjeta_credito', 'pago_movil']
        if metodo_pago and metodo_pago not in metodos_validos:
            errores.append(f"Método de pago debe ser uno de: {', '.join(metodos_validos)}")

        # 3. Validar tasa de cambio
        tasa_cambio = data_dict.get('tasa_cambio_bs_usd', 0)
        if monto_bs > 0 and monto_usd > 0:  # Pago mixto requiere tasa
            try:
                tasa = float(tasa_cambio) if tasa_cambio else 0
                if tasa <= 0:
                    errores.append("Tasa de cambio es obligatoria para pagos mixtos")
                if tasa > 100:  # Límite razonable
                    errores.append("Tasa de cambio parece incorrecta (mayor a 100)")
            except (ValueError, TypeError):
                errores.append("Tasa de cambio debe ser un número válido")

        return errores

    @staticmethod
    def validar_servicio(data: Union[ServicioFormModel, Dict[str, Any]]) -> List[str]:
        """
        Validaciones de servicios

        Args:
            data: Datos del servicio

        Returns:
            Lista de errores encontrados
        """
        errores = []

        if hasattr(data, '__dict__'):
            data_dict = data.__dict__
        else:
            data_dict = data

        # 1. Campos obligatorios
        if not data_dict.get('nombre') or data_dict['nombre'].strip() == "":
            errores.append("Nombre del servicio es obligatorio")

        if not data_dict.get('categoria'):
            errores.append("Categoría del servicio es obligatoria")

        # 2. Validar precios
        precio_base = data_dict.get('precio_base_usd', 0)
        precio_minimo = data_dict.get('precio_minimo_usd', 0)
        precio_maximo = data_dict.get('precio_maximo_usd', 0)

        try:
            base = float(precio_base) if precio_base else 0
            minimo = float(precio_minimo) if precio_minimo else 0
            maximo = float(precio_maximo) if precio_maximo else 0

            if base <= 0:
                errores.append("Precio base debe ser mayor a cero")

            if minimo > base:
                errores.append("Precio mínimo no puede ser mayor al precio base")

            if maximo < base:
                errores.append("Precio máximo no puede ser menor al precio base")

            if base > 10000:  # 10k USD máximo por servicio
                errores.append("Precio base no puede exceder 10,000 USD")

        except (ValueError, TypeError):
            errores.append("Los precios deben ser números válidos")

        # 3. Validar duración
        duracion = data_dict.get('duracion_minutos', 0)
        try:
            duracion_num = int(duracion) if duracion else 0
            if duracion_num <= 0:
                errores.append("Duración debe ser mayor a cero minutos")
            if duracion_num > 480:  # 8 horas máximo
                errores.append("Duración no puede exceder 480 minutos (8 horas)")
        except (ValueError, TypeError):
            errores.append("Duración debe ser un número entero válido")

        return errores


class ValidadorGeneral:
    """
    Validador general para casos especiales y validaciones cruzadas
    """

    @staticmethod
    def validar_unicidad_documento(numero_documento: str,
                                  tipo_documento: str,
                                  excluir_id: str = None) -> bool:
        """
        Validar que el documento no esté duplicado en el sistema

        Args:
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
            excluir_id: ID a excluir de la validación (para ediciones)

        Returns:
            True si es único, False si está duplicado
        """
        # En implementación real, consultaría la base de datos
        # Por ahora retorna True para no bloquear el desarrollo
        return True

    @staticmethod
    def validar_disponibilidad_odontologo(odontologo_id: str,
                                        fecha_consulta: date,
                                        hora_inicio: str) -> bool:
        """
        Validar que el odontólogo esté disponible en la fecha/hora

        Args:
            odontologo_id: ID del odontólogo
            fecha_consulta: Fecha de la consulta
            hora_inicio: Hora de inicio

        Returns:
            True si está disponible, False si no
        """
        # En implementación real, consultaría la agenda
        return True

    @staticmethod
    def validar_integridad_pago(id_consulta: str,
                               monto_total: float,
                               pagos_anteriores: List[Dict]) -> List[str]:
        """
        Validar integridad de pagos vs costo total de consulta

        Args:
            id_consulta: ID de la consulta
            monto_total: Monto total de la consulta
            pagos_anteriores: Lista de pagos anteriores

        Returns:
            Lista de errores de integridad
        """
        errores = []

        # Calcular total pagado anteriormente
        total_pagado = sum(pago.get('monto_usd', 0) for pago in pagos_anteriores)

        if total_pagado > monto_total:
            errores.append("El total pagado excede el costo de la consulta")

        return errores


# Funciones de utilidad para integración fácil
def validar_formulario(tipo_formulario: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validar formulario según su tipo

    Args:
        tipo_formulario: Tipo de formulario (paciente, consulta, etc.)
        data: Datos a validar

    Returns:
        Diccionario con resultado de validación
    """
    validadores = {
        'paciente': FormValidator.validar_paciente,
        'consulta': FormValidator.validar_consulta,
        'personal': FormValidator.validar_personal,
        'servicio': FormValidator.validar_servicio,
        'pago': FormValidator.validar_pago,
        'intervencion': FormValidator.validar_intervencion
    }

    if tipo_formulario not in validadores:
        return {
            'valido': False,
            'errores': [f"Tipo de formulario no reconocido: {tipo_formulario}"]
        }

    try:
        errores = validadores[tipo_formulario](data)
        return {
            'valido': len(errores) == 0,
            'errores': errores,
            'total_errores': len(errores)
        }
    except Exception as e:
        return {
            'valido': False,
            'errores': [f"Error interno de validación: {str(e)}"]
        }


def validar_multiple(validaciones: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validar múltiples formularios en lote

    Args:
        validaciones: Lista de diccionarios con 'tipo' y 'data'

    Returns:
        Resumen de todas las validaciones
    """
    resultados = {}
    total_errores = 0

    for i, validacion in enumerate(validaciones):
        tipo = validacion.get('tipo')
        data = validacion.get('data')
        clave = validacion.get('clave', f'validacion_{i}')

        resultado = validar_formulario(tipo, data)
        resultados[clave] = resultado
        total_errores += resultado.get('total_errores', 0)

    return {
        'resultados': resultados,
        'total_errores': total_errores,
        'todas_validas': total_errores == 0
    }