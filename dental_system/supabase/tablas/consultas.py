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
                          fecha_llegada: datetime = None,
                          fecha_programada: datetime = None,  # Compatibility parameter
                          orden_llegada_general: int = None,
                          orden_cola_odontologo: int = None,
                          estado: str = "en_espera",
                          tipo_consulta: str = 'general',
                          motivo_consulta: Optional[str] = None,
                          observaciones: str = None,
                          observaciones_cita: Optional[str] = None,  # Compatibility parameter
                          prioridad: str = 'normal',
                          creada_por: Optional[str] = None,
                          programada_por: Optional[str] = None) -> Dict[str, Any]:  # Compatibility parameter
        """
        Crea nueva consulta usando esquema v4.1 - ORDEN DE LLEGADA
        
        Args:
            paciente_id: ID del paciente
            primer_odontologo_id: ID del primer odontólogo asignado (esquema v4.1)
            odontologo_id: ID del odontólogo (backward compatibility)
            fecha_llegada: Momento real de llegada del paciente
            fecha_programada: Fecha programada (backward compatibility)
            orden_llegada_general: Orden general del día (calculado automáticamente si no se proporciona)
            orden_cola_odontologo: Posición en cola del odontólogo específico
            estado: Estado inicial (default: en_espera)
            tipo_consulta: Tipo (general, control, urgencia, cirugia, otro)
            motivo_consulta: Motivo de la consulta
            observaciones: Observaciones visibles (esquema v4.1)
            observaciones_cita: Observaciones (backward compatibility)
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
            "fecha_llegada": fecha_consulta.isoformat(),
            "orden_llegada_general": orden_llegada_general or 1,
            "orden_cola_odontologo": orden_cola_odontologo or 1,
            "estado": estado,
            "tipo_consulta": tipo_consulta,
            "motivo_consulta": motivo_consulta or "Consulta general",
            "observaciones": observaciones_finales,
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

            # Obtener nombre del odontólogo desde la vista (usar primer_odontologo_id)
            odontologo_id = consulta.get("primer_odontologo_id")
            if odontologo_id:  # Solo buscar si hay ID válido
                odontologo_data = self._get_odontologo_from_vista(odontologo_id)
                consulta["odontologo_nombre_completo"] = odontologo_data.get("nombre_completo", "Sin nombre") if odontologo_data else "Sin nombre"
            else:
                consulta["odontologo_nombre_completo"] = "Sin asignar"
            
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
        
        logger.info(f"Actualizando prioridad de consulta {consultation_id} a {nueva_prioridad}")
        return self.update(consultation_id, data)

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
            "estado": "en_espera"
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

    @handle_supabase_error
    def get_vista_consultas_dia(self, fecha: date = None) -> List[Dict[str, Any]]:
        """
        Obtener consultas del día usando vista optimizada

        Args:
            fecha: Fecha específica (por defecto hoy)

        Returns:
            Lista de consultas con información completa optimizada
        """
        if fecha is None:
            fecha = date.today()

        logger.info(f"Obteniendo consultas del día {fecha} usando vista optimizada")

        # Si existe la vista, usarla. Si no, usar query manual optimizada
        try:
            # Intentar usar la vista primero
            result = self.client.table('vista_consultas_dia').select('*').eq(
                'fecha', fecha.isoformat()
            ).execute()

            return result.data if result.data else []

        except Exception:
            # Fallback a query manual si la vista no existe
            logger.info("Vista no disponible, usando query optimizada manual")
            return self.get_today_consultations()

    @handle_supabase_error
    def get_vista_cola_odontologos(self) -> List[Dict[str, Any]]:
        """
        Obtener estado de colas por odontólogo usando vista optimizada

        Returns:
            Lista con estadísticas de cola por odontólogo
        """
        logger.info("Obteniendo estadísticas de colas usando vista optimizada")

        try:
            # Intentar usar la vista primero
            result = self.client.table('vista_cola_odontologos').select('*').execute()

            return result.data if result.data else []

        except Exception:
            # Fallback a query manual si la vista no existe
            logger.info("Vista no disponible, calculando estadísticas manualmente")
            return self._calcular_estadisticas_colas_manual()

    @handle_supabase_error
    def obtener_proximo_paciente_bd(self, odontologo_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtener próximo paciente usando función de BD

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Datos del próximo paciente o None
        """
        logger.info(f"Obteniendo próximo paciente para {odontologo_id} usando función BD")

        try:
            # Intentar usar la función de BD primero
            result = self.client.rpc('obtener_proximo_paciente', {
                'odontologo_id_param': odontologo_id
            }).execute()

            return result.data[0] if result.data else None

        except Exception:
            # Fallback a query manual
            logger.info("Función BD no disponible, usando query manual")
            return self._obtener_proximo_paciente_manual(odontologo_id)

    def _calcular_estadisticas_colas_manual(self) -> List[Dict[str, Any]]:
        """
        Calcular estadísticas de colas manualmente (fallback)

        Returns:
            Lista con estadísticas por odontólogo
        """
        # Query manual para obtener estadísticas
        result = self.client.table(self.table_name).select(
            """
            primer_odontologo_id,
            estado,
            personal!inner(primer_nombre, primer_apellido, especialidad)
            """
        ).eq('fecha_llegada::date', date.today().isoformat()).execute()

        estadisticas = {}
        for consulta in result.data:
            odontologo_id = consulta['primer_odontologo_id']
            estado = consulta['estado']

            if odontologo_id not in estadisticas:
                personal_data = consulta.get('personal', {})
                estadisticas[odontologo_id] = {
                    'odontologo_id': odontologo_id,
                    'odontologo_nombre': f"{personal_data.get('primer_nombre', '')} {personal_data.get('primer_apellido', '')}".strip(),
                    'especialidad': personal_data.get('especialidad', ''),
                    'pacientes_esperando': 0,
                    'pacientes_atendiendo': 0,
                    'pacientes_atendidos_hoy': 0,
                    'proximo_en_cola': None
                }

            # Contar por estado
            if estado == 'en_espera':
                estadisticas[odontologo_id]['pacientes_esperando'] += 1
            elif estado == 'en_atencion':
                estadisticas[odontologo_id]['pacientes_atendiendo'] += 1
            elif estado == 'completada':
                estadisticas[odontologo_id]['pacientes_atendidos_hoy'] += 1

        return list(estadisticas.values())

    def _obtener_proximo_paciente_manual(self, odontologo_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtener próximo paciente manualmente (fallback)

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Datos del próximo paciente
        """
        result = self.client.table(self.table_name).select(
            """
            *,
            pacientes!inner(primer_nombre, primer_apellido, numero_documento, celular_1)
            """
        ).eq(
            'primer_odontologo_id', odontologo_id
        ).eq(
            'estado', 'en_espera'
        ).order('orden_llegada_general').limit(1).execute()

        return result.data[0] if result.data else None


# ✅ NUEVA INSTANCIA PARA IMPORTAR - CORREGIDA
consultas_table = ConsultationsTable()