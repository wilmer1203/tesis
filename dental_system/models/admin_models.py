"""
Modelos de datos tipados específicos para el Administrador - CORREGIDO PARA CONSULTAS
Actualizado para usar nombres completos desde vista y campos separados
"""

import reflex as rx
from typing import Optional, Dict, Any, List
from datetime import datetime


class PacienteModel(rx.Base):
    """Modelo para datos de pacientes - CORREGIDO para nombres y teléfonos separados"""
    id: Optional[str] = ""
    numero_historia: str = ""
    
    # ✅ NOMBRES SEPARADOS (según nueva estructura DB)
    primer_nombre: str = ""
    segundo_nombre: Optional[str] = ""
    primer_apellido: str = ""
    segundo_apellido: Optional[str] = ""
    
    # Documentación
    numero_documento: str = ""
    tipo_documento: str = "CC"
    fecha_nacimiento: Optional[str] = ""
    edad: Optional[int] = None
    genero: Optional[str] = ""
    
    # ✅ TELÉFONOS SEPARADOS (según nueva estructura DB)
    telefono_1: Optional[str] = ""
    telefono_2: Optional[str] = ""
    
    email: Optional[str] = ""
    direccion: Optional[str] = ""
    ciudad: Optional[str] = ""
    departamento: Optional[str] = ""
    ocupacion: Optional[str] = ""
    estado_civil: Optional[str] = ""
    
    # Información médica
    alergias: List[str] = []
    medicamentos_actuales: List[str] = []
    condiciones_medicas: List[str] = []
    antecedentes_familiares: List[str] = []
    observaciones: Optional[str] = ""
    
    # Control del sistema
    fecha_registro: str = ""
    fecha_actualizacion: str = ""
    registrado_por: Optional[str] = ""
    activo: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PacienteModel":
        """Crear instancia desde diccionario de Supabase - ACTUALIZADO"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            numero_historia=str(data.get("numero_historia", "")),
            
            # ✅ NOMBRES SEPARADOS
            primer_nombre=str(data.get("primer_nombre", "")),
            segundo_nombre=str(data.get("segundo_nombre", "") if data.get("segundo_nombre") else ""),
            primer_apellido=str(data.get("primer_apellido", "")),
            segundo_apellido=str(data.get("segundo_apellido", "") if data.get("segundo_apellido") else ""),
            
            numero_documento=str(data.get("numero_documento", "")),
            tipo_documento=str(data.get("tipo_documento", "CC")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "") if data.get("fecha_nacimiento") else ""),
            edad=data.get("edad") if isinstance(data.get("edad"), int) else None,
            genero=str(data.get("genero", "") if data.get("genero") else ""),
            
            # ✅ TELÉFONOS SEPARADOS
            telefono_1=str(data.get("telefono_1", "") if data.get("telefono_1") else ""),
            telefono_2=str(data.get("telefono_2", "") if data.get("telefono_2") else ""),
            
            email=str(data.get("email", "") if data.get("email") else ""),
            direccion=str(data.get("direccion", "") if data.get("direccion") else ""),
            ciudad=str(data.get("ciudad", "") if data.get("ciudad") else ""),
            departamento=str(data.get("departamento", "") if data.get("departamento") else ""),
            ocupacion=str(data.get("ocupacion", "") if data.get("ocupacion") else ""),
            estado_civil=str(data.get("estado_civil", "") if data.get("estado_civil") else ""),
            
            # Información médica (arrays)
            alergias=data.get("alergias", []) if isinstance(data.get("alergias"), list) else [],
            medicamentos_actuales=data.get("medicamentos_actuales", []) if isinstance(data.get("medicamentos_actuales"), list) else [],
            condiciones_medicas=data.get("condiciones_medicas", []) if isinstance(data.get("condiciones_medicas"), list) else [],
            antecedentes_familiares=data.get("antecedentes_familiares", []) if isinstance(data.get("antecedentes_familiares"), list) else [],
            observaciones=str(data.get("observaciones", "") if data.get("observaciones") else ""),
            
            # Control del sistema
            fecha_registro=str(data.get("fecha_registro", "")),
            fecha_actualizacion=str(data.get("fecha_actualizacion", "")),
            registrado_por=str(data.get("registrado_por", "") if data.get("registrado_por") else ""),
            activo=bool(data.get("activo", True))
        )
    
    @property
    def nombre_completo(self) -> str:
        """Construir nombre completo desde campos separados"""
        nombres = []
        if self.primer_nombre:
            nombres.append(self.primer_nombre)
        if self.segundo_nombre:
            nombres.append(self.segundo_nombre)
        if self.primer_apellido:
            nombres.append(self.primer_apellido)
        if self.segundo_apellido:
            nombres.append(self.segundo_apellido)
        
        return " ".join(nombres) if nombres else "Sin nombre"

    @property
    def edad_display(self) -> str:
        """Propiedad para mostrar la edad"""
        return f"{self.edad} años" if self.edad else "N/A"
    
    @property
    def telefono_display(self) -> str:
        """✅ ACTUALIZADO: Propiedad para mostrar el teléfono principal"""
        if self.telefono_1:
            return self.telefono_1
        elif self.telefono_2:
            return self.telefono_2
        else:
            return "Sin teléfono"
    
    @property
    def fecha_registro_display(self) -> str:
        """Propiedad para mostrar la fecha de registro formateada"""
        try:
            if self.fecha_registro:
                fecha_obj = datetime.fromisoformat(self.fecha_registro.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y")
            return "Sin fecha"
        except:
            return str(self.fecha_registro)
    
    @property
    def contacto_display(self) -> str:
        """✅ ACTUALIZADO: Propiedad para mostrar información de contacto resumida"""
        contactos = []
        if self.telefono_1:
            contactos.append(f"Tel1: {self.telefono_1}")
        if self.telefono_2:
            contactos.append(f"Tel2: {self.telefono_2}")
        if self.email:
            contactos.append(f"Email: {self.email}")
        
        return " | ".join(contactos) if contactos else "Sin contacto"
    
    @property
    def alergias_display(self) -> str:
        """Propiedad para mostrar alergias como string"""
        return ", ".join(self.alergias) if self.alergias else "Sin alergias conocidas"
    
    @property
    def medicamentos_display(self) -> str:
        """Propiedad para mostrar medicamentos como string"""
        return ", ".join(self.medicamentos_actuales) if self.medicamentos_actuales else "Sin medicamentos"
    
    @property
    def condiciones_display(self) -> str:
        """Propiedad para mostrar condiciones médicas como string"""
        return ", ".join(self.condiciones_medicas) if self.condiciones_medicas else "Sin condiciones reportadas"

    def matches_search(self, search_term: str) -> bool:
        """✅ ACTUALIZADO: Verificar si el paciente coincide con el término de búsqueda"""
        if not search_term:
            return True
        
        search_lower = search_term.lower()
        fields_to_search = [
            self.primer_nombre.lower(),
            self.segundo_nombre.lower() if self.segundo_nombre else "",
            self.primer_apellido.lower(),
            self.segundo_apellido.lower() if self.segundo_apellido else "",
            self.numero_documento.lower(),
            self.email.lower() if self.email else "",
            self.telefono_1.lower() if self.telefono_1 else "",
            self.telefono_2.lower() if self.telefono_2 else "",
            self.numero_historia.lower()
        ]
        
        return any(search_lower in field for field in fields_to_search)


class AdminStatsModel(rx.Base):
    """Modelo para estadísticas específicas del administrador"""
    total_pacientes: int = 0
    nuevos_pacientes_mes: int = 0
    consultas_hoy: int = 0
    pagos_pendientes: int = 0
    
    # Estadísticas adicionales de pacientes
    pacientes_activos: int = 0
    pacientes_hombres: int = 0
    pacientes_mujeres: int = 0
    
    # Estadísticas de actividad
    pacientes_registrados_semana: int = 0
    consultas_semana: int = 0
    ingresos_mes: float = 0.0


class ConsultaModel(rx.Base):
    """✅ CORREGIDO: Modelo para datos de consultas/citas"""
    id: Optional[str] = ""
    numero_consulta: str = ""
    paciente_id: str = ""
    odontologo_id: str = ""
    fecha_programada: str = ""
    fecha_inicio_real: Optional[str] = ""
    fecha_fin_real: Optional[str] = ""
    estado: str = "programada"
    tipo_consulta: str = "general"
    prioridad: str = "normal"
    motivo_consulta: Optional[str] = ""
    observaciones_cita: Optional[str] = ""
    costo_total: float = 0.0
    
    # ✅ INFORMACIÓN RELACIONADA - CORREGIDA PARA NUEVOS CAMPOS
    paciente_nombre: str = ""          # Ahora viene como paciente_nombre_completo
    odontologo_nombre: str = ""        # Ahora viene como odontologo_nombre_completo
    paciente_telefono: str = ""        # Nuevo campo
    paciente_documento: str = ""       # Nuevo campo
    odontologo_especialidad: str = "" # Nuevo campo
    
    orden_llegada: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConsultaModel":
        """✅ CORREGIDO: Crear instancia desde diccionario de Supabase - ACTUALIZADO PARA NUEVOS CAMPOS"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            id=str(data.get("id", "")),
            numero_consulta=str(data.get("numero_consulta", "")),
            paciente_id=str(data.get("paciente_id", "")),
            odontologo_id=str(data.get("odontologo_id", "")),
            fecha_programada=str(data.get("fecha_programada", "")),
            fecha_inicio_real=str(data.get("fecha_inicio_real", "") if data.get("fecha_inicio_real") else ""),
            fecha_fin_real=str(data.get("fecha_fin_real", "") if data.get("fecha_fin_real") else ""),
            estado=str(data.get("estado", "programada")),
            tipo_consulta=str(data.get("tipo_consulta", "general")),
            prioridad=str(data.get("prioridad", "normal")),
            motivo_consulta=str(data.get("motivo_consulta", "") if data.get("motivo_consulta") else ""),
            observaciones_cita=str(data.get("observaciones_cita", "") if data.get("observaciones_cita") else ""),
            costo_total=float(data.get("costo_total", 0)),
            
            # Orden de llegada
            orden_llegada=data.get("orden_llegada"),
            
            # ✅ INFORMACIÓN RELACIONADA - CORREGIDA PARA USAR NUEVOS CAMPOS PROCESADOS
            paciente_nombre=str(data.get("paciente_nombre_completo", "") or data.get("paciente_nombre", "")),
            odontologo_nombre=str(data.get("odontologo_nombre_completo", "") or data.get("odontologo_nombre", "")),
            paciente_telefono=str(data.get("paciente_telefono", "") if data.get("paciente_telefono") else ""),
            paciente_documento=str(data.get("paciente_documento", "") if data.get("paciente_documento") else ""),
            odontologo_especialidad=str(data.get("odontologo_especialidad", "") if data.get("odontologo_especialidad") else "")
        )
    
    @property
    def estado_display(self) -> str:
        """Propiedad para mostrar el estado formateado"""
        estados_map = {
            "programada": "Programada",
            "confirmada": "Confirmada", 
            "en_progreso": "En Progreso",
            "completada": "Completada",
            "cancelada": "Cancelada",
            "no_asistio": "No Asistió"
        }
        return estados_map.get(self.estado, self.estado.capitalize())
    
    @property
    def fecha_display(self) -> str:
        """Propiedad para mostrar la fecha formateada"""
        try:
            if self.fecha_programada:
                fecha_obj = datetime.fromisoformat(self.fecha_programada.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y %H:%M")
            return "Sin fecha"
        except:
            return str(self.fecha_programada)
    
    @property
    def paciente_info_display(self) -> str:
        """✅ NUEVO: Información completa del paciente para mostrar"""
        info_parts = [self.paciente_nombre]
        if self.paciente_documento:
            info_parts.append(f"CC: {self.paciente_documento}")
        if self.paciente_telefono:
            info_parts.append(f"Tel: {self.paciente_telefono}")
        return " | ".join(info_parts)
    
    @property
    def odontologo_info_display(self) -> str:
        """✅ NUEVO: Información completa del odontólogo para mostrar"""
        info_parts = [self.odontologo_nombre]
        if self.odontologo_especialidad:
            info_parts.append(f"({self.odontologo_especialidad})")
        return " ".join(info_parts)


class PagoModel(rx.Base):
    """Modelo para datos de pagos"""
    id: Optional[str] = ""
    numero_recibo: str = ""
    consulta_id: Optional[str] = ""
    paciente_id: str = ""
    fecha_pago: str = ""
    monto_total: float = 0.0
    monto_pagado: float = 0.0
    saldo_pendiente: float = 0.0
    metodo_pago: str = ""
    referencia_pago: Optional[str] = ""
    concepto: str = ""
    estado_pago: str = "completado"
    
    # Información relacionada
    paciente_nombre: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PagoModel":
        """Crear instancia desde diccionario de Supabase"""
        if not data or not isinstance(data, dict):
            return cls()
        
        # Manejar datos relacionados
        paciente_data = data.get("pacientes", {})
        
        return cls(
            id=str(data.get("id", "")),
            numero_recibo=str(data.get("numero_recibo", "")),
            consulta_id=str(data.get("consulta_id", "")),
            paciente_id=str(data.get("paciente_id", "")),
            fecha_pago=str(data.get("fecha_pago", "")),
            monto_total=float(data.get("monto_total", 0)),
            monto_pagado=float(data.get("monto_pagado", 0)),
            saldo_pendiente=float(data.get("saldo_pendiente", 0)),
            metodo_pago=str(data.get("metodo_pago", "")),
            referencia_pago=str(data.get("referencia_pago", "")),
            concepto=str(data.get("concepto", "")),
            estado_pago=str(data.get("estado_pago", "completado")),
            
            # Información relacionada
            paciente_nombre=str(paciente_data.get("nombre_completo", "") if paciente_data else "")
        )
    
    @property
    def estado_display(self) -> str:
        """Propiedad para mostrar el estado del pago"""
        estados_map = {
            "pendiente": "Pendiente",
            "completado": "Completado",
            "anulado": "Anulado",
            "reembolsado": "Reembolsado"
        }
        return estados_map.get(self.estado_pago, self.estado_pago.capitalize())
    
    @property
    def monto_display(self) -> str:
        """Propiedad para mostrar el monto formateado"""
        return f"${self.monto_total:,.2f}"
    
    @property
    def fecha_display(self) -> str:
        """Propiedad para mostrar la fecha formateada"""
        try:
            if self.fecha_pago:
                fecha_obj = datetime.fromisoformat(self.fecha_pago.replace('Z', '+00:00'))
                return fecha_obj.strftime("%d/%m/%Y")
            return "Sin fecha"
        except:
            return str(self.fecha_pago)


class PacientesStatsModel(rx.Base):
    """Modelo extendido para estadísticas de pacientes del admin"""
    total: int = 0
    nuevos_mes: int = 0
    activos: int = 0
    hombres: int = 0
    mujeres: int = 0
    
    # Estadísticas adicionales
    edad_promedio: float = 0.0
    pacientes_con_email: int = 0
    pacientes_con_telefono: int = 0
    registros_ultima_semana: int = 0