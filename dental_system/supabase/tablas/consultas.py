"""
Operaciones CRUD para la tabla consultas (citas) 
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, date, timedelta
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class ConsultationsTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla consultas
    """
    
    def __init__(self):
        super().__init__('consultas')
    
    @handle_supabase_error
    def create_consultation(self,
                          paciente_id: str,
                          primer_odontologo_id: str = None,
                          odontologo_id: str = None,  # Compatibility parameter
                          odontologo_preferido_id: str = None,
                          fecha_llegada: datetime = None,
                          fecha_programada: datetime = None,  # Compatibility parameter
                          orden_llegada_general: int = None,
                          orden_cola_odontologo: int = None,
                          estado: str = "en_espera",
                          tipo_consulta: str = 'general',
                          motivo_consulta: Optional[str] = None,
                          observaciones: str = None,
                          observaciones_cita: Optional[str] = None,  # Compatibility parameter
                          notas_internas: str = None,
                          prioridad: str = 'normal',
                          creada_por: Optional[str] = None,
                          programada_por: Optional[str] = None) -> Dict[str, Any]:  # Compatibility parameter
        """
        Crea nueva consulta usando esquema v4.1 - ORDEN DE LLEGADA
        
        Args:
            paciente_id: ID del paciente
            primer_odontologo_id: ID del primer odontólogo asignado (esquema v4.1)
            odontologo_id: ID del odontólogo (backward compatibility)
            odontologo_preferido_id: Odontólogo preferido (opcional)
            fecha_llegada: Momento real de llegada del paciente
            fecha_programada: Fecha programada (backward compatibility)
            orden_llegada_general: Orden general del día (calculado automáticamente si no se proporciona)
            orden_cola_odontologo: Posición en cola del odontólogo específico
            estado: Estado inicial (default: en_espera)
            tipo_consulta: Tipo (general, control, urgencia, cirugia, otro)
            motivo_consulta: Motivo de la consulta
            observaciones: Observaciones visibles (esquema v4.1)
            observaciones_cita: Observaciones (backward compatibility)
            notas_internas: Notas internas del personal
            prioridad: Prioridad (normal, alta, urgente)
            creada_por: ID del usuario que crea la consulta
            programada_por: Usuario que programa (backward compatibility)
            
        Returns:
            Consulta creada con datos completos v4.1
        """
        # Resolver campos con backward compatibility
        doctor_id = primer_odontologo_id or odontologo_id
        fecha_consulta = fecha_llegada or fecha_programada or datetime.now()
        usuario_creador = creada_por or programada_por
        observaciones_finales = observaciones or observaciones_cita or ""
        
        if not doctor_id:
            raise ValueError("Se requiere primer_odontologo_id o odontologo_id")
        
        # Datos principales con esquema v4.1
        data = {
            "paciente_id": paciente_id,
            "primer_odontologo_id": doctor_id,
            "odontologo_preferido_id": odontologo_preferido_id if odontologo_preferido_id else None,
            "fecha_llegada": fecha_consulta.isoformat(),
            "orden_llegada_general": orden_llegada_general or 1,
            "orden_cola_odontologo": orden_cola_odontologo or 1,
            "estado": estado,
            "tipo_consulta": tipo_consulta,
            "motivo_consulta": motivo_consulta or "Consulta general",
            "observaciones": observaciones_finales,
            "notas_internas": notas_internas or "",
            "prioridad": prioridad,
            "creada_por": usuario_creador if usuario_creador else None,
            
            # Campos omitidos: odontologo_id no existe en esquema v4.1
        }
        
        logger.info(f"Creando consulta v4.1 para paciente {paciente_id} con Dr. {doctor_id}")
        return self.create(data)
    
    @handle_supabase_error
    def get_by_numero(self, numero_consulta: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una consulta por su número
        
        Args:
            numero_consulta: Número de la consulta (formato YYYYMMDD###)
            
        Returns:
            Consulta encontrada o None
        """
        response = self.table.select("*").eq("numero_consulta", numero_consulta).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_consultation_details(self, consultation_id: str) -> Optional[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtiene una consulta con información completa usando vista
        
        Args:
            consultation_id: ID de la consulta
            
        Returns:
            Consulta con información expandida
        """
        response = self.table.select("""
            *,
            pacientes!inner(
                id, numero_historia, 
                primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                celular_1, celular_2, email
            )
        """).eq("id", consultation_id).execute()
        
        if response.data:
            consulta = response.data[0]
            
            # Construir nombre completo del paciente
            paciente_data = consulta.get("pacientes", {})
            nombres_paciente = []
            if paciente_data.get("primer_nombre"):
                nombres_paciente.append(paciente_data["primer_nombre"])
            if paciente_data.get("segundo_nombre"):
                nombres_paciente.append(paciente_data["segundo_nombre"])
            if paciente_data.get("primer_apellido"):
                nombres_paciente.append(paciente_data["primer_apellido"])
            if paciente_data.get("segundo_apellido"):
                nombres_paciente.append(paciente_data["segundo_apellido"])
            
            consulta["paciente_nombre_completo"] = " ".join(nombres_paciente) if nombres_paciente else "Sin nombre"
            
            # Obtener nombre del odontólogo desde la vista
            odontologo_data = self._get_odontologo_from_vista(consulta.get("odontologo_id"))
            consulta["odontologo_nombre_completo"] = odontologo_data.get("nombre_completo", "Sin nombre") if odontologo_data else "Sin nombre"
            
            return consulta
        
        return None
    
    def _get_odontologo_from_vista(self, odontologo_id: str) -> Optional[Dict[str, Any]]:
        """
        ✅ NUEVO: Obtiene información del odontólogo desde la vista
        """
        try:
            response = self.client.table('vista_personal_completo').select(
                "id, nombre_completo, especialidad"
            ).eq("id", odontologo_id).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            logger.warning(f"Error obteniendo odontólogo desde vista: {e}")
            return None
    
    @handle_supabase_error
    def get_by_date_range(self,
                         fecha_inicio: date,
                         fecha_fin: date,
                         odontologo_id: Optional[str] = None,
                         estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtiene consultas en un rango de fechas
        
        Args:
            fecha_inicio: Fecha inicial
            fecha_fin: Fecha final
            odontologo_id: Filtrar por odontólogo (opcional)
            estado: Filtrar por estado (opcional)
            
        Returns:
            Lista de consultas en el rango
        """
        query = self.table.select("""
            *,
            pacientes(
                id, numero_historia,
                primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                celular_1, celular_2
            )
        """).gte("fecha_llegada", fecha_inicio.isoformat()).lte("fecha_llegada", fecha_fin.isoformat())
        
        if odontologo_id:
            query = query.eq("primer_odontologo_id", odontologo_id)
        if estado:
            query = query.eq("estado", estado)
        
        query = query.order("fecha_llegada")
        response = query.execute()
        
        # Procesar resultados para agregar nombres completos
        processed_data = []
        for consulta in response.data:
            consulta_procesada = self._process_consulta_names(consulta)
            processed_data.append(consulta_procesada)
        
        return processed_data
    
    @handle_supabase_error
    def get_today_consultations(self, odontologo_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtiene las consultas del día usando vista para odontólogos
        
        Args:
            odontologo_id: Filtrar por odontólogo (opcional)
            
        Returns:
            Lista de consultas de hoy con nombres completos
        """
        from datetime import date
        today = date.today()
        fecha_inicio = today.isoformat()
        fecha_fin = f"{today.isoformat()}T23:59:59"
        
        print(f"[DEBUG] 📅 get_today_consultations - Hoy: {today}")
        print(f"[DEBUG] 🔍 Rango de búsqueda: {fecha_inicio} a {fecha_fin}")
        print(f"[DEBUG] 👨‍⚕️ Odontólogo ID: {odontologo_id}")
        
        # Query para consultas con información básica
        query = self.table.select("""
            *,
            pacientes!inner(
                id, numero_historia,
                primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                numero_documento, celular_1, celular_2, email
            )
        """).gte("fecha_llegada", fecha_inicio
        ).lt("fecha_llegada", fecha_fin
        ).order("fecha_llegada")
        
        if odontologo_id:
            query = query.eq("primer_odontologo_id", odontologo_id)
        
        response = query.execute()
        print(f"[DEBUG] 🏥 Consultas encontradas en BD: {len(response.data) if response.data else 0}")
        
        if response.data:
            for i, consulta in enumerate(response.data):
                print(f"[DEBUG] 📋 Consulta {i+1}: {consulta.get('id')} - {consulta.get('fecha_llegada')} - Estado: {consulta.get('estado')}")
        
        if response.data:
            # Procesar datos para construir nombres completos
            processed_data = []
            
            for i, consulta in enumerate(response.data, 1):
                consulta_procesada = self._process_consulta_names(consulta)
                consulta_procesada["orden_llegada"] = i
                processed_data.append(consulta_procesada)
            
            return processed_data
        
        return []
    
    def _process_consulta_names(self, consulta: Dict[str, Any]) -> Dict[str, Any]:
        """
        ✅ NUEVO: Procesa una consulta para agregar nombres completos
        """
        consulta_procesada = consulta.copy()
        
        # Construir nombre del paciente desde campos separados
        paciente_data = consulta.get("pacientes", {})
        nombres_paciente = []
        
        if paciente_data.get("primer_nombre"):
            nombres_paciente.append(paciente_data["primer_nombre"])
        if paciente_data.get("segundo_nombre"):
            nombres_paciente.append(paciente_data["segundo_nombre"])
        if paciente_data.get("primer_apellido"):
            nombres_paciente.append(paciente_data["primer_apellido"])
        if paciente_data.get("segundo_apellido"):
            nombres_paciente.append(paciente_data["segundo_apellido"])
        
        consulta_procesada["paciente_nombre_completo"] = " ".join(nombres_paciente) if nombres_paciente else "Sin nombre"
        
        # Obtener nombre del odontólogo desde la vista
        odontologo_id = consulta.get("odontologo_id")
        if odontologo_id:
            odontologo_data = self._get_odontologo_from_vista(odontologo_id)
            consulta_procesada["odontologo_nombre_completo"] = odontologo_data.get("nombre_completo", "Sin nombre") if odontologo_data else "Sin nombre"
            consulta_procesada["odontologo_especialidad"] = odontologo_data.get("especialidad", "") if odontologo_data else ""
        else:
            consulta_procesada["odontologo_nombre_completo"] = "Sin asignar"
            consulta_procesada["odontologo_especialidad"] = ""
        
        # Agregar información adicional del paciente
        consulta_procesada["paciente_telefono"] = (
            paciente_data.get("celular_1") or 
            paciente_data.get("celular_2") or 
            ""
        )
        consulta_procesada["paciente_documento"] = paciente_data.get("numero_documento", "")
        
        return consulta_procesada
    
    @handle_supabase_error
    def get_upcoming_consultations(self, 
                                 paciente_id: Optional[str] = None,
                                 odontologo_id: Optional[str] = None,
                                 days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtiene las próximas consultas
        
        Args:
            paciente_id: Filtrar por paciente (opcional)
            odontologo_id: Filtrar por odontólogo (opcional)
            days_ahead: Días hacia adelante para buscar
            
        Returns:
            Lista de próximas consultas
        """
        fecha_inicio = datetime.now()
        fecha_fin = fecha_inicio + timedelta(days=days_ahead)
        
        query = self.table.select("""
            *,
            pacientes(
                numero_historia,
                primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                celular_1, celular_2
            )
        """).gte("fecha_llegada", fecha_inicio.isoformat()
        ).lte("fecha_llegada", fecha_fin.isoformat()
        ).in_("estado", ["programada", "confirmada"])
        
        if paciente_id:
            query = query.eq("paciente_id", paciente_id)
        if odontologo_id:
            query = query.eq("primer_odontologo_id", odontologo_id)
        
        query = query.order("fecha_llegada")
        response = query.execute()
        
        # Procesar resultados
        processed_data = []
        for consulta in response.data:
            consulta_procesada = self._process_consulta_names(consulta)
            processed_data.append(consulta_procesada)
        
        return processed_data
    
    @handle_supabase_error
    def update_status(self, consultation_id: str, nuevo_estado: str, notas: Optional[str] = None) -> Dict[str, Any]:
        """
        Actualiza el estado de una consulta
        
        Args:
            consultation_id: ID de la consulta
            nuevo_estado: Nuevo estado (en_espera, en_atencion, entre_odontologos, completada, cancelada)
            notas: Notas adicionales sobre el cambio
            
        Returns:
            Consulta actualizada
        """
        data = {"estado": nuevo_estado}
        
        # Agregar timestamps según el estado (usando nombres correctos del esquema)
        if nuevo_estado == "en_atencion":
            data["fecha_inicio_atencion"] = datetime.now().isoformat()
        elif nuevo_estado in ["completada", "cancelada"]:
            data["fecha_fin_atencion"] = datetime.now().isoformat()
        
        if notas:
            data["notas_internas"] = notas
        
        logger.info(f"Actualizando estado de consulta {consultation_id} a {nuevo_estado}")
        return self.update(consultation_id, data)
    
    @handle_supabase_error
    def update_priority(self, consultation_id: str, nueva_prioridad: str, notas: Optional[str] = None) -> Dict[str, Any]:
        """
        Actualiza la prioridad de una consulta
        
        Args:
            consultation_id: ID de la consulta
            nueva_prioridad: Nueva prioridad (baja, normal, alta, urgente)
            notas: Notas adicionales sobre el cambio
            
        Returns:
            Consulta actualizada
        """
        data = {"prioridad": nueva_prioridad}
        
        if notas:
            data["notas_internas"] = notas
        
        logger.info(f"Actualizando prioridad de consulta {consultation_id} a {nueva_prioridad}")
        return self.update(consultation_id, data)
    
    @handle_supabase_error
    def confirm_consultation(self, consultation_id: str) -> Dict[str, Any]:
        """
        Confirma una consulta programada
        
        Args:
            consultation_id: ID de la consulta
            
        Returns:
            Consulta confirmada
        """
        return self.update_status(consultation_id, "confirmada")
    
    @handle_supabase_error
    def cancel_consultation(self, consultation_id: str, motivo: str) -> Dict[str, Any]:
        """
        Cancela una consulta
        
        Args:
            consultation_id: ID de la consulta
            motivo: Motivo de cancelación
            
        Returns:
            Consulta cancelada
        """
        return self.update_status(consultation_id, "cancelada", motivo)
    
    @handle_supabase_error
    def mark_no_show(self, consultation_id: str) -> Dict[str, Any]:
        """
        Marca una consulta como no asistida
        
        Args:
            consultation_id: ID de la consulta
            
        Returns:
            Consulta actualizada
        """
        return self.update_status(consultation_id, "no_asistio")
    
    @handle_supabase_error
    def reschedule_consultation(self, 
                              consultation_id: str,
                              nueva_fecha: datetime,
                              motivo: str) -> Dict[str, Any]:
        """
        Reprograma una consulta
        
        Args:
            consultation_id: ID de la consulta
            nueva_fecha: Nueva fecha y hora
            motivo: Motivo de reprogramación
            
        Returns:
            Consulta reprogramada
        """
        data = {
            "fecha_llegada": nueva_fecha.isoformat(),
            "estado": "en_espera",
            "notas_internas": f"Reprogramada: {motivo}"
        }
        
        logger.info(f"Reprogramando consulta {consultation_id}")
        return self.update(consultation_id, data)
    
    @handle_supabase_error
    def get_availability_slots(self,
                             odontologo_id: str,
                             fecha: date,
                             duracion_minutos: int = 30) -> List[Dict[str, Any]]:
        """
        Obtiene los espacios disponibles de un odontólogo en una fecha
        
        Args:
            odontologo_id: ID del odontólogo
            fecha: Fecha a consultar
            duracion_minutos: Duración de la cita en minutos
            
        Returns:
            Lista de horarios disponibles
        """
        # Obtener todas las consultas del odontólogo ese día
        consultas_dia = self.get_by_date_range(fecha, fecha, odontologo_id)
        
        # Definir horario de trabajo (esto podría venir de configuración)
        hora_inicio = 8  # 8:00 AM
        hora_fin = 17    # 5:00 PM
        
        # Crear lista de todos los slots posibles
        slots_disponibles = []
        hora_actual = hora_inicio
        
        while hora_actual < hora_fin:
            slot_inicio = datetime.combine(fecha, datetime.min.time().replace(hour=hora_actual))
            slot_fin = slot_inicio + timedelta(minutes=duracion_minutos)
            
            # Verificar si el slot está ocupado
            ocupado = False
            for consulta in consultas_dia:
                if consulta["estado"] not in ["cancelada", "no_asistio"]:
                    consulta_inicio = datetime.fromisoformat(consulta["fecha_llegada"].replace('Z', '+00:00'))
                    consulta_fin = consulta_inicio + timedelta(minutes=30)  # Duración por defecto
                
                # Verificar si hay solapamiento
                if not (slot_fin <= consulta_inicio or slot_inicio >= consulta_fin):
                    ocupado = True
                    break
            
            if not ocupado:
                slots_disponibles.append({
                    "hora_inicio": slot_inicio.strftime("%H:%M"),
                    "hora_fin": slot_fin.strftime("%H:%M"),
                    "disponible": True
                })
            
            # Avanzar al siguiente slot
            hora_actual += duracion_minutos / 60
        
        return slots_disponibles


# ✅ NUEVA INSTANCIA PARA IMPORTAR - CORREGIDA
consultas_table = ConsultationsTable()