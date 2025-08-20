"""
📝 MODELOS DE FORMULARIOS - MIGRACIÓN Dict[str,str] → Typed Models
===============================================================

PROPÓSITO: Reemplazar Dict[str,str] form_data con modelos tipados
- Type safety para formularios
- Validación automática de campos
- IntelliSense para developers
- Consistencia entre servicios

USADO EN: Todos los servicios CRUD
"""

from typing import Optional, Dict, Any, List
import reflex as rx
from datetime import date, datetime
from decimal import Decimal


# ==========================================
# 👥 FORMULARIOS DE PACIENTES
# ==========================================

class PacienteFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE PACIENTES
    
    Reemplaza: form_data: Dict[str, str] en pacientes_service
    """
    
    # Datos personales básicos
    primer_nombre: str = ""
    segundo_nombre: str = ""
    primer_apellido: str = ""
    segundo_apellido: str = ""
    
    # Identificación y contacto
    numero_documento: str = ""
    numero_historia: str = ""
    tipo_documento: str = "cedula"  # cedula, pasaporte, etc.
    telefono_1: str = ""
    telefono_2: str = ""
    email: str = ""
    
    # Datos demográficos
    fecha_nacimiento: str = ""  # YYYY-MM-DD format
    edad: str = ""
    genero: str = ""  # masculino, femenino, otro
    direccion: str = ""
    ciudad: str = ""
    departamento: str = ""
    estado_civil: str = ""
    ocupacion: str = ""
    
    # Contacto de emergencia
    # contacto_emergencia_nombre: str = ""
    # contacto_emergencia_telefono: str = ""
    # contacto_emergencia_relacion: str = ""
    
    # Información médica
    alergias: str = ""
    medicamentos_actuales: str = ""
    condiciones_medicas: str = ""
    antecedentes_familiares: str = ""
    observaciones_medicas: str = ""
    
    # Estado
    activo: bool = True
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos y formato"""
        errors = {}
        
        if not self.primer_nombre.strip():
            errors.setdefault("primer_nombre", []).append("Primer nombre es requerido")
        
        if not self.primer_apellido.strip():
            errors.setdefault("primer_apellido", []).append("Primer apellido es requerido")
        
        if not self.numero_documento.strip():
            errors.setdefault("numero_documento", []).append("Número de documento es requerido")
        
        if self.email and "@" not in self.email:
            errors.setdefault("email", []).append("Email debe tener formato válido")
        
        return errors
    
    @property
    def nombre_completo(self) -> str:
        """Nombre completo formateado"""
        nombres = [self.primer_nombre, self.segundo_nombre]
        apellidos = [self.primer_apellido, self.segundo_apellido]
        
        nombres_str = " ".join(n for n in nombres if n.strip())
        apellidos_str = " ".join(a for a in apellidos if a.strip())
        
        return f"{nombres_str} {apellidos_str}".strip()
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad con servicios existentes"""
        return {
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "primer_apellido": self.primer_apellido,
            "segundo_apellido": self.segundo_apellido,
            "numero_documento": self.numero_documento,
            "numero_historia": self.numero_historia,
            "tipo_documento": self.tipo_documento,
            "telefono_1": self.telefono_1,
            "telefono_2": self.telefono_2,
            "email": self.email,
            "fecha_nacimiento": self.fecha_nacimiento,
            "edad": self.edad,
            "genero": self.genero,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "departamento": self.departamento,
            "estado_civil": self.estado_civil,
            "ocupacion": self.ocupacion,
            "alergias": self.alergias,
            "medicamentos_actuales": self.medicamentos_actuales,
            "condiciones_medicas": self.condiciones_medicas,
            "antecedentes_familiares": self.antecedentes_familiares,
            "observaciones_medicas": self.observaciones_medicas,
            "activo": str(self.activo)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PacienteFormModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            primer_nombre=str(data.get("primer_nombre", "")),
            segundo_nombre=str(data.get("segundo_nombre", "")),
            primer_apellido=str(data.get("primer_apellido", "")),
            segundo_apellido=str(data.get("segundo_apellido", "")),
            numero_documento=str(data.get("numero_documento", "")),
            numero_historia=str(data.get("numero_historia", "")),
            tipo_documento=str(data.get("tipo_documento", "cedula")),
            telefono_1=str(data.get("telefono_1", "")),
            telefono_2=str(data.get("telefono_2", "")),
            email=str(data.get("email", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "")),
            edad=str(data.get("edad", "")),
            genero=str(data.get("genero", "")),
            direccion=str(data.get("direccion", "")),
            ciudad=str(data.get("ciudad", "")),
            departamento=str(data.get("departamento", "")),
            estado_civil=str(data.get("estado_civil", "")),
            ocupacion=str(data.get("ocupacion", "")),
            alergias=str(data.get("alergias", "")),
            medicamentos_actuales=str(data.get("medicamentos_actuales", "")),
            condiciones_medicas=str(data.get("condiciones_medicas", "")),
            antecedentes_familiares=str(data.get("antecedentes_familiares", "")),
            observaciones_medicas=str(data.get("observaciones_medicas", "")),
            activo=data.get("activo", True) if isinstance(data.get("activo"), bool) else str(data.get("activo", "True")).lower() == "true"
        )


# ==========================================
# 📅 FORMULARIOS DE CONSULTAS
# ==========================================

class ConsultaFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE CONSULTAS
    
    Reemplaza: form_data: Dict[str, str] en consultas_service
    """
    
    # Referencias
    paciente_id: str = ""
    odontologo_id: str = ""
    
    # Detalles de la consulta
    tipo_consulta: str = "general"  # general, emergencia, control, primera_vez
    motivo_consulta: str = ""
    sintomas_principales: str = ""
    observaciones_cita: str = ""
    
    # Prioridad y estado
    prioridad: str = "normal"  # baja, normal, alta, urgente
    estado: str = "programada"  # programada, en_progreso, completada, cancelada
    
    # Información médica
    diagnostico_preliminar: str = ""
    diagnostico_final: str = ""
    tratamiento_realizado: str = ""
    receta_medicamentos: str = ""
    
    # Seguimiento
    proxima_consulta: str = ""  # Fecha sugerida
    requiere_seguimiento: bool = False
    notas_seguimiento: str = ""
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos"""
        errors = {}
        
        if not self.paciente_id.strip():
            errors.setdefault("paciente_id", []).append("Paciente es requerido")
        
        if not self.odontologo_id.strip():
            errors.setdefault("odontologo_id", []).append("Odontólogo es requerido")
        
        return errors
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad"""
        return {
            "paciente_id": self.paciente_id,
            "odontologo_id": self.odontologo_id,
            "tipo_consulta": self.tipo_consulta,
            "motivo_consulta": self.motivo_consulta,
            "sintomas_principales": self.sintomas_principales,
            "observaciones_cita": self.observaciones_cita,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "diagnostico_preliminar": self.diagnostico_preliminar,
            "diagnostico_final": self.diagnostico_final,
            "tratamiento_realizado": self.tratamiento_realizado,
            "receta_medicamentos": self.receta_medicamentos,
            "proxima_consulta": self.proxima_consulta,
            "requiere_seguimiento": str(self.requiere_seguimiento),
            "notas_seguimiento": self.notas_seguimiento,
        }


# ==========================================
# 👨‍⚕️ FORMULARIOS DE PERSONAL
# ==========================================

class PersonalFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE PERSONAL
    
    Reemplaza: form_data: Dict[str, str] en personal_service
    """
    
    # Datos personales
    primer_nombre: str = ""
    segundo_nombre: str = ""
    primer_apellido: str = ""
    segundo_apellido: str = ""
    
    # Identificación
    numero_documento: str = ""
    telefono: str = ""
    email: str = ""
    direccion: str = ""
    
    # Datos profesionales
    tipo_personal: str = "asistente"  # odontologo, asistente, administrador
    especialidad: str = ""
    numero_colegiatura: str = ""
    fecha_ingreso: str = ""  # YYYY-MM-DD
    
    # Información laboral
    salario: str = "0"
    comision_servicios: str = "0"
    horario_trabajo: str = ""
    estado_laboral: str = "activo"  # activo, inactivo, vacaciones, licencia
    
    # Usuario del sistema
    crear_usuario: bool = True
    usuario_email: str = ""
    usuario_password: str = ""
    rol_sistema: str = "asistente"  # gerente, administrador, odontologo, asistente
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos"""
        errors = {}
        
        if not self.primer_nombre.strip():
            errors.setdefault("primer_nombre", []).append("Primer nombre es requerido")
        
        if not self.primer_apellido.strip():
            errors.setdefault("primer_apellido", []).append("Primer apellido es requerido")
        
        if not self.numero_documento.strip():
            errors.setdefault("numero_documento", []).append("Número de documento es requerido")
        
        if self.crear_usuario:
            if not self.usuario_email.strip():
                errors.setdefault("usuario_email", []).append("Email de usuario es requerido")
            
            if not self.usuario_password.strip():
                errors.setdefault("usuario_password", []).append("Password es requerida")
        
        return errors
    
    @property
    def nombre_completo(self) -> str:
        """Nombre completo formateado"""
        nombres = [self.primer_nombre, self.segundo_nombre]
        apellidos = [self.primer_apellido, self.segundo_apellido]
        
        nombres_str = " ".join(n for n in nombres if n.strip())
        apellidos_str = " ".join(a for a in apellidos if a.strip())
        
        return f"{nombres_str} {apellidos_str}".strip()
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad"""
        return {
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "primer_apellido": self.primer_apellido,
            "segundo_apellido": self.segundo_apellido,
            "numero_documento": self.numero_documento,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "tipo_personal": self.tipo_personal,
            "especialidad": self.especialidad,
            "numero_colegiatura": self.numero_colegiatura,
            "fecha_ingreso": self.fecha_ingreso,
            "salario": self.salario,
            "comision_servicios": self.comision_servicios,
            "horario_trabajo": self.horario_trabajo,
            "estado_laboral": self.estado_laboral,
            "crear_usuario": str(self.crear_usuario),
            "usuario_email": self.usuario_email,
            "usuario_password": self.usuario_password,
            "rol_sistema": self.rol_sistema,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalFormModel":
        """Crear instancia desde diccionario"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            primer_nombre=str(data.get("primer_nombre", "")),
            segundo_nombre=str(data.get("segundo_nombre", "")),
            primer_apellido=str(data.get("primer_apellido", "")),
            segundo_apellido=str(data.get("segundo_apellido", "")),
            numero_documento=str(data.get("numero_documento", "")),
            telefono=str(data.get("telefono", "")),
            email=str(data.get("email", "")),
            direccion=str(data.get("direccion", "")),
            tipo_personal=str(data.get("tipo_personal", "asistente")),
            especialidad=str(data.get("especialidad", "")),
            numero_colegiatura=str(data.get("numero_colegiatura", "")),
            fecha_ingreso=str(data.get("fecha_ingreso", "")),
            salario=str(data.get("salario", "0")),
            comision_servicios=str(data.get("comision_servicios", "0")),
            horario_trabajo=str(data.get("horario_trabajo", "")),
            estado_laboral=str(data.get("estado_laboral", "activo")),
            crear_usuario=data.get("crear_usuario", True) if isinstance(data.get("crear_usuario"), bool) else str(data.get("crear_usuario", "True")).lower() == "true",
            usuario_email=str(data.get("usuario_email", "")),
            usuario_password=str(data.get("usuario_password", "")),
            rol_sistema=str(data.get("rol_sistema", "asistente"))
        )


# ==========================================
# 🦷 FORMULARIOS DE SERVICIOS
# ==========================================

class ServicioFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE SERVICIOS
    
    Reemplaza: form_data: Dict[str, str] en servicios_service
    """
    
    # Información básica
    nombre: str = ""
    descripcion: str = ""
    categoria: str = "preventiva"  # preventiva, restaurativa, estetica, cirugia, etc.
    
    # Precios
    precio_base: str = "0"
    precio_minimo: str = "0"
    precio_maximo: str = "0"
    
    # Detalles del servicio
    duracion_estimada: str = "30"  # minutos
    requiere_consulta_previa: bool = False
    requiere_autorizacion: bool = False
    
    # Materiales e instrucciones
    material_incluido: str = ""
    instrucciones_pre: str = ""
    instrucciones_post: str = ""
    
    # Estado
    activo: bool = True
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos y formato"""
        errors = {}
        
        if not self.nombre.strip():
            errors.setdefault("nombre", []).append("Nombre del servicio es requerido")
        
        try:
            precio_base = float(self.precio_base)
            if precio_base < 0:
                errors.setdefault("precio_base", []).append("Precio base debe ser mayor a 0")
        except (ValueError, TypeError):
            errors.setdefault("precio_base", []).append("Precio base debe ser un número válido")
        
        return errors
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad"""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "precio_base": self.precio_base,
            "precio_minimo": self.precio_minimo,
            "precio_maximo": self.precio_maximo,
            "duracion_estimada": self.duracion_estimada,
            "requiere_consulta_previa": str(self.requiere_consulta_previa),
            "requiere_autorizacion": str(self.requiere_autorizacion),
            "material_incluido": self.material_incluido,
            "instrucciones_pre": self.instrucciones_pre,
            "instrucciones_post": self.instrucciones_post,
            "activo": str(self.activo),
        }


# ==========================================
# 💳 FORMULARIOS DE PAGOS
# ==========================================

class PagoFormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE PAGOS
    
    Reemplaza: form_data: Dict[str, str] en pagos_service
    """
    
    # Referencias
    paciente_id: str = ""
    consulta_id: str = ""  # Opcional
    
    # Montos
    monto_total: str = "0"
    monto_pagado: str = "0"
    descuento_aplicado: str = "0"
    impuestos: str = "0"
    
    # Método y detalles de pago
    metodo_pago: str = "efectivo"  # efectivo, tarjeta_credito, transferencia, etc.
    referencia_pago: str = ""
    concepto: str = ""
    
    # Estado y autorización
    estado_pago: str = "completado"  # pendiente, completado, anulado
    autorizado_por: str = ""
    motivo_descuento: str = ""
    
    # Observaciones
    observaciones: str = ""
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos y montos"""
        errors = {}
        
        if not self.paciente_id.strip():
            errors.setdefault("paciente_id", []).append("Paciente es requerido")
        
        try:
            monto_total = float(self.monto_total)
            if monto_total <= 0:
                errors.setdefault("monto_total", []).append("Monto total debe ser mayor a 0")
        except (ValueError, TypeError):
            errors.setdefault("monto_total", []).append("Monto total debe ser un número válido")
        
        try:
            monto_pagado = float(self.monto_pagado)
            if monto_pagado < 0:
                errors.setdefault("monto_pagado", []).append("Monto pagado no puede ser negativo")
        except (ValueError, TypeError):
            errors.setdefault("monto_pagado", []).append("Monto pagado debe ser un número válido")
        
        return errors
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad"""
        return {
            "paciente_id": self.paciente_id,
            "consulta_id": self.consulta_id,
            "monto_total": self.monto_total,
            "monto_pagado": self.monto_pagado,
            "descuento_aplicado": self.descuento_aplicado,
            "impuestos": self.impuestos,
            "metodo_pago": self.metodo_pago,
            "referencia_pago": self.referencia_pago,
            "concepto": self.concepto,
            "estado_pago": self.estado_pago,
            "autorizado_por": self.autorizado_por,
            "motivo_descuento": self.motivo_descuento,
            "observaciones": self.observaciones,
        }


class PagoParcialFormModel(rx.Base):
    """
    📝 FORMULARIO PARA PAGOS PARCIALES
    
    Usado en: process_partial_payment
    """
    
    monto_adicional: str = "0"
    metodo_pago: str = "efectivo"
    referencia_pago: str = ""
    observaciones: str = ""
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar monto adicional"""
        errors = {}
        
        try:
            monto = float(self.monto_adicional)
            if monto <= 0:
                errors.setdefault("monto_adicional", []).append("Monto debe ser mayor a 0")
        except (ValueError, TypeError):
            errors.setdefault("monto_adicional", []).append("Monto debe ser un número válido")
        
        return errors
    
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad"""
        return {
            "monto_adicional": self.monto_adicional,
            "metodo_pago": self.metodo_pago,
            "referencia_pago": self.referencia_pago,
            "observaciones": self.observaciones,
        }


# ==========================================
# 🦷 FORMULARIOS DE ODONTOLOGÍA
# ==========================================

class IntervencionFormModel(rx.Base):
    """
    📝 FORMULARIO DE INTERVENCIÓN ODONTOLÓGICA
    
    Usado en: odontologia_service para intervenciones
    """
    
    # Referencias
    consulta_id: str = ""
    servicio_id: str = ""
    odontologo_id: str = ""
    asistente_id: str = ""
    
    # Detalles clínicos
    diagnostico_inicial: str = ""
    procedimiento_realizado: str = ""
    dientes_afectados: str = ""  # Lista separada por comas
    
    # Materiales y anestesia
    materiales_utilizados: str = ""
    anestesia_utilizada: str = ""
    
    # Precio y seguimiento
    precio_acordado: str = "0"
    descuento: str = "0"
    precio_final: str = "0"
    
    # Control
    requiere_control: bool = False
    fecha_control_sugerida: str = ""
    instrucciones_paciente: str = ""
    
    # Observaciones
    complicaciones: str = ""
    observaciones: str = ""
    
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos de intervención"""
        errors = {}
        
        if not self.consulta_id.strip():
            errors.setdefault("consulta_id", []).append("Consulta es requerida")
        
        if not self.servicio_id.strip():
            errors.setdefault("servicio_id", []).append("Servicio es requerido")
        
        if not self.procedimiento_realizado.strip():
            errors.setdefault("procedimiento_realizado", []).append("Procedimiento realizado es requerido")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a dict - Any porque puede contener listas"""
        return {
            "consulta_id": self.consulta_id,
            "servicio_id": self.servicio_id,
            "odontologo_id": self.odontologo_id,
            "asistente_id": self.asistente_id,
            "diagnostico_inicial": self.diagnostico_inicial,
            "procedimiento_realizado": self.procedimiento_realizado,
            "dientes_afectados": self.dientes_afectados,
            "materiales_utilizados": self.materiales_utilizados,
            "anestesia_utilizada": self.anestesia_utilizada,
            "precio_acordado": self.precio_acordado,
            "descuento": self.descuento,
            "precio_final": self.precio_final,
            "requiere_control": self.requiere_control,
            "fecha_control_sugerida": self.fecha_control_sugerida,
            "instrucciones_paciente": self.instrucciones_paciente,
            "complicaciones": self.complicaciones,
            "observaciones": self.observaciones,
        }