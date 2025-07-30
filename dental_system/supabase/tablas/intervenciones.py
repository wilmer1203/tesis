"""
Operaciones CRUD para la tabla intervenciones - AGREGAR INSTANCIA FALTANTE
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta, date
from decimal import Decimal
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class InterventionsTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla intervenciones
    """
    
    def __init__(self):
        super().__init__('intervenciones')
    
    @handle_supabase_error
    def create_intervention(self,
                          consulta_id: str,
                          servicio_id: str,
                          odontologo_id: str,
                          hora_inicio: datetime,
                          procedimiento_realizado: str,
                          precio_acordado: Decimal,
                          precio_final: Decimal,
                          asistente_id: Optional[str] = None,
                          hora_fin: Optional[datetime] = None,
                          dientes_afectados: Optional[List[int]] = None,
                          diagnostico_inicial: Optional[str] = None,
                          materiales_utilizados: Optional[List[str]] = None,
                          anestesia_utilizada: Optional[str] = None,
                          complicaciones: Optional[str] = None,
                          descuento: Decimal = Decimal('0'),
                          requiere_control: bool = False,
                          fecha_control_sugerida: Optional[date] = None,
                          instrucciones_paciente: Optional[str] = None,
                          estado: str = 'completada') -> Dict[str, Any]:
        """
        Crea una nueva intervención/procedimiento
        """
        # Calcular duración si se proporciona hora_fin
        duracion_real = None
        if hora_fin:
            duracion = hora_fin - hora_inicio
            duracion_real = str(duracion)
        
        data = {
            "consulta_id": consulta_id,
            "servicio_id": servicio_id,
            "odontologo_id": odontologo_id,
            "hora_inicio": hora_inicio.isoformat(),
            "procedimiento_realizado": procedimiento_realizado,
            "precio_acordado": float(precio_acordado),
            "descuento": float(descuento),
            "precio_final": float(precio_final),
            "estado": estado,
            "requiere_control": requiere_control
        }
        
        # Agregar campos opcionales
        if asistente_id:
            data["asistente_id"] = asistente_id
        if hora_fin:
            data["hora_fin"] = hora_fin.isoformat()
            data["duracion_real"] = duracion_real
        if dientes_afectados:
            data["dientes_afectados"] = dientes_afectados
        if diagnostico_inicial:
            data["diagnostico_inicial"] = diagnostico_inicial
        if materiales_utilizados:
            data["materiales_utilizados"] = materiales_utilizados
        if anestesia_utilizada:
            data["anestesia_utilizada"] = anestesia_utilizada
        if complicaciones:
            data["complicaciones"] = complicaciones
        if fecha_control_sugerida:
            data["fecha_control_sugerida"] = fecha_control_sugerida.isoformat()
        if instrucciones_paciente:
            data["instrucciones_paciente"] = instrucciones_paciente
        
        logger.info(f"Creando intervención para consulta {consulta_id}")
        return self.create(data)
    
    @handle_supabase_error
    def get_intervention_details(self, intervention_id: str) -> Optional[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtiene una intervención con información completa usando vista
        """
        response = self.table.select("""
            *,
            consultas!inner(
                numero_consulta, fecha_programada,
                pacientes!inner(
                    id, numero_historia,
                    primer_nombre, segundo_nombre, primer_apellido, segundo_apellido
                )
            ),
            servicios!inner(
                codigo, nombre, categoria
            )
        """).eq("id", intervention_id).execute()
        
        if response.data:
            intervencion = response.data[0]
            
            # Construir nombre completo del paciente
            paciente_data = intervencion.get("consultas", {}).get("pacientes", {})
            nombres_paciente = []
            if paciente_data.get("primer_nombre"):
                nombres_paciente.append(paciente_data["primer_nombre"])
            if paciente_data.get("segundo_nombre"):
                nombres_paciente.append(paciente_data["segundo_nombre"])
            if paciente_data.get("primer_apellido"):
                nombres_paciente.append(paciente_data["primer_apellido"])
            if paciente_data.get("segundo_apellido"):
                nombres_paciente.append(paciente_data["segundo_apellido"])
            
            intervencion["paciente_nombre_completo"] = " ".join(nombres_paciente) if nombres_paciente else "Sin nombre"
            
            # Obtener nombres del personal desde vista
            if intervencion.get("odontologo_id"):
                odontologo_data = self._get_personal_from_vista(intervencion["odontologo_id"])
                intervencion["odontologo_nombre_completo"] = odontologo_data.get("nombre_completo", "Sin nombre") if odontologo_data else "Sin nombre"
            
            if intervencion.get("asistente_id"):
                asistente_data = self._get_personal_from_vista(intervencion["asistente_id"])
                intervencion["asistente_nombre_completo"] = asistente_data.get("nombre_completo", "Sin nombre") if asistente_data else "Sin nombre"
            
            return intervencion
        
        return None
    
    def _get_personal_from_vista(self, personal_id: str) -> Optional[Dict[str, Any]]:
        """
        ✅ NUEVO: Obtiene información del personal desde la vista
        """
        try:
            response = self.client.table('vista_personal_completo').select(
                "id, nombre_completo, especialidad, tipo_personal"
            ).eq("id", personal_id).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            logger.warning(f"Error obteniendo personal desde vista: {e}")
            return None
    
    @handle_supabase_error
    def get_by_consultation(self, consulta_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las intervenciones de una consulta
        """
        response = self.table.select("""
            *,
            servicios(codigo, nombre, categoria)
        """).eq("consulta_id", consulta_id).order("hora_inicio").execute()
        
        return response.data
    
    @handle_supabase_error
    def get_by_patient(self, paciente_id: str) -> List[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtiene todas las intervenciones de un paciente
        """
        # Primero obtener consultas del paciente
        consultas_response = self.client.table("consultas").select("id").eq(
            "paciente_id", paciente_id
        ).execute()
        
        consulta_ids = [c["id"] for c in consultas_response.data]
        
        if not consulta_ids:
            return []
        
        # Obtener intervenciones de esas consultas
        response = self.table.select("""
            *,
            consultas!inner(
                numero_consulta, fecha_programada
            ),
            servicios(codigo, nombre, categoria)
        """).in_("consulta_id", consulta_ids).order("hora_inicio", desc=True).execute()
        
        # Procesar para agregar nombres desde vista
        processed_data = []
        for intervencion in response.data:
            if intervencion.get("odontologo_id"):
                odontologo_data = self._get_personal_from_vista(intervencion["odontologo_id"])
                intervencion["odontologo_nombre_completo"] = odontologo_data.get("nombre_completo", "Sin nombre") if odontologo_data else "Sin nombre"
            
            processed_data.append(intervencion)
        
        return processed_data
    
    @handle_supabase_error
    def get_by_tooth(self, paciente_id: str, numero_diente: int) -> List[Dict[str, Any]]:
        """
        Obtiene todas las intervenciones realizadas en un diente específico
        """
        intervenciones_paciente = self.get_by_patient(paciente_id)
        
        # Filtrar por diente
        intervenciones_diente = []
        for intervencion in intervenciones_paciente:
            if intervencion.get("dientes_afectados") and numero_diente in intervencion["dientes_afectados"]:
                intervenciones_diente.append(intervencion)
        
        return intervenciones_diente
    
    @handle_supabase_error
    def get_pending_controls(self, 
                           odontologo_id: Optional[str] = None,
                           dias_adelante: int = 30) -> List[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtiene intervenciones que requieren control
        """
        fecha_limite = (datetime.now() + timedelta(days=dias_adelante)).date()
        
        query = self.table.select("""
            *,
            consultas!inner(
                pacientes!inner(
                    primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                    numero_historia, telefono_1, telefono_2
                )
            ),
            servicios(nombre)
        """).eq("requiere_control", True
        ).lte("fecha_control_sugerida", fecha_limite.isoformat())
        
        if odontologo_id:
            query = query.eq("odontologo_id", odontologo_id)
        
        query = query.order("fecha_control_sugerida")
        response = query.execute()
        
        # Procesar nombres de pacientes
        processed_data = []
        for intervencion in response.data:
            paciente_data = intervencion.get("consultas", {}).get("pacientes", {})
            nombres_paciente = []
            if paciente_data.get("primer_nombre"):
                nombres_paciente.append(paciente_data["primer_nombre"])
            if paciente_data.get("segundo_nombre"):
                nombres_paciente.append(paciente_data["segundo_nombre"])
            if paciente_data.get("primer_apellido"):
                nombres_paciente.append(paciente_data["primer_apellido"])
            if paciente_data.get("segundo_apellido"):
                nombres_paciente.append(paciente_data["segundo_apellido"])
            
            intervencion["paciente_nombre_completo"] = " ".join(nombres_paciente) if nombres_paciente else "Sin nombre"
            
            # Obtener nombre del odontólogo
            if intervencion.get("odontologo_id"):
                odontologo_data = self._get_personal_from_vista(intervencion["odontologo_id"])
                intervencion["odontologo_nombre_completo"] = odontologo_data.get("nombre_completo", "Sin nombre") if odontologo_data else "Sin nombre"
            
            processed_data.append(intervencion)
        
        # Filtrar solo los que no tienen una consulta de control programada
        intervenciones_pendientes = []
        for intervencion in processed_data:
            # Verificar si ya hay una consulta de control
            paciente_id = intervencion["consultas"]["pacientes"]["id"]
            fecha_control = intervencion["fecha_control_sugerida"]
            
            # Buscar consultas futuras del paciente
            consultas_futuras = self.client.table("consultas").select("id").eq(
                "paciente_id", paciente_id
            ).gte("fecha_programada", fecha_control
            ).in_("estado", ["programada", "confirmada"]).execute()
            
            if not consultas_futuras.data:
                intervenciones_pendientes.append(intervencion)
        
        return intervenciones_pendientes
    
    @handle_supabase_error
    def update_status(self, 
                     intervention_id: str, 
                     nuevo_estado: str,
                     hora_fin: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Actualiza el estado de una intervención
        """
        data = {"estado": nuevo_estado}
        
        if nuevo_estado == "completada" and hora_fin:
            # Obtener intervención para calcular duración
            intervencion = self.get_by_id(intervention_id)
            if intervencion:
                hora_inicio = datetime.fromisoformat(intervencion["hora_inicio"].replace('Z', '+00:00'))
                duracion = hora_fin - hora_inicio
                
                data["hora_fin"] = hora_fin.isoformat()
                data["duracion_real"] = str(duracion)
        
        logger.info(f"Actualizando estado de intervención {intervention_id} a {nuevo_estado}")
        return self.update(intervention_id, data)
    
    @handle_supabase_error
    def add_complication(self, intervention_id: str, complicacion: str) -> Dict[str, Any]:
        """
        Agrega una complicación a la intervención
        """
        intervencion = self.get_by_id(intervention_id)
        if not intervencion:
            raise ValueError(f"Intervención {intervention_id} no encontrada")
        
        complicaciones_actuales = intervencion.get("complicaciones", "")
        nueva_complicacion = f"{complicaciones_actuales}\n{datetime.now()}: {complicacion}".strip()
        
        return self.update(intervention_id, {"complicaciones": nueva_complicacion})
    
    @handle_supabase_error
    def get_statistics_by_service(self, 
                                 servicio_id: str,
                                 fecha_inicio: Optional[date] = None,
                                 fecha_fin: Optional[date] = None) -> Dict[str, Any]:
        """
        Obtiene estadísticas de intervenciones por servicio
        """
        query = self.table.select("""
            id, estado, precio_final, descuento, 
            hora_inicio, duracion_real, complicaciones
        """).eq("servicio_id", servicio_id)
        
        if fecha_inicio:
            query = query.gte("hora_inicio", fecha_inicio.isoformat())
        if fecha_fin:
            fecha_fin_dt = datetime.combine(fecha_fin, datetime.max.time())
            query = query.lte("hora_inicio", fecha_fin_dt.isoformat())
        
        response = query.execute()
        intervenciones = response.data
        
        # Calcular estadísticas
        stats = {
            "servicio_id": servicio_id,
            "total_realizadas": len(intervenciones),
            "completadas": len([i for i in intervenciones if i["estado"] == "completada"]),
            "suspendidas": len([i for i in intervenciones if i["estado"] == "suspendida"]),
            "en_progreso": len([i for i in intervenciones if i["estado"] == "en_progreso"]),
            "ingresos_totales": sum(i["precio_final"] for i in intervenciones if i["estado"] == "completada"),
            "descuentos_totales": sum(i["descuento"] for i in intervenciones),
            "precio_promedio": 0,
            "con_complicaciones": len([i for i in intervenciones if i.get("complicaciones")]),
            "duracion_promedio": None
        }
        
        # Calcular promedios
        if stats["completadas"] > 0:
            stats["precio_promedio"] = stats["ingresos_totales"] / stats["completadas"]
            
            # Calcular duración promedio
            duraciones = []
            for i in intervenciones:
                if i["estado"] == "completada" and i.get("duracion_real"):
                    # Parsear duración (formato: "HH:MM:SS")
                    try:
                        partes = i["duracion_real"].split(":")
                        if len(partes) >= 2:
                            minutos = int(partes[0]) * 60 + int(partes[1])
                            duraciones.append(minutos)
                    except:
                        pass
            
            if duraciones:
                stats["duracion_promedio"] = sum(duraciones) / len(duraciones)
        
        return stats
    
    @handle_supabase_error
    def get_dentist_productivity(self, 
                                odontologo_id: str,
                                fecha_inicio: date,
                                fecha_fin: date) -> Dict[str, Any]:
        """
        ✅ CORREGIDO: Obtiene productividad de un odontólogo
        """
        query = self.table.select("""
            *,
            servicios(nombre, categoria, precio_base)
        """).eq("odontologo_id", odontologo_id
        ).gte("hora_inicio", fecha_inicio.isoformat()
        ).lte("hora_inicio", datetime.combine(fecha_fin, datetime.max.time()).isoformat())
        
        response = query.execute()
        intervenciones = response.data
        
        # Agrupar por categoría de servicio
        por_categoria = {}
        
        for intervencion in intervenciones:
            if intervencion["estado"] == "completada":
                categoria = intervencion["servicios"]["categoria"]
                
                if categoria not in por_categoria:
                    por_categoria[categoria] = {
                        "cantidad": 0,
                        "ingresos": 0
                    }
                
                por_categoria[categoria]["cantidad"] += 1
                por_categoria[categoria]["ingresos"] += intervencion["precio_final"]
        
        # Obtener nombre del odontólogo desde vista
        odontologo_data = self._get_personal_from_vista(odontologo_id)
        odontologo_nombre = odontologo_data.get("nombre_completo", "Sin nombre") if odontologo_data else "Sin nombre"
        
        return {
            "odontologo_id": odontologo_id,
            "odontologo_nombre": odontologo_nombre,
            "periodo": f"{fecha_inicio} - {fecha_fin}",
            "total_intervenciones": len([i for i in intervenciones if i["estado"] == "completada"]),
            "ingresos_totales": sum(i["precio_final"] for i in intervenciones if i["estado"] == "completada"),
            "por_categoria": por_categoria,
            "intervenciones_suspendidas": len([i for i in intervenciones if i["estado"] == "suspendida"])
        }


# ✅ CREAR INSTANCIA PARA IMPORTAR
interventions_table = InterventionsTable()