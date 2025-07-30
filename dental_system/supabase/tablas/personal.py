"""
Operaciones CRUD para la tabla personal
"""
from typing import Dict, List, Optional, Any
from datetime import date, datetime
from decimal import Decimal
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class PersonalTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para la tabla personal
    """
    
    def __init__(self):
        super().__init__('personal')
    
    def create_staff_complete(self,
                            usuario_id: str,
                            primer_nombre: str,
                            primer_apellido: str,
                            numero_documento: str,
                            celular: str,
                            tipo_personal: str,
                            segundo_nombre: Optional[str] = None,
                            segundo_apellido: Optional[str] = None,
                            tipo_documento: str = 'CC',
                            fecha_nacimiento: Optional[date] = None,
                            direccion: Optional[str] = None,
                            especialidad: Optional[str] = None,
                            numero_licencia: Optional[str] = None,
                            fecha_contratacion: Optional[date] = None,
                            salario: Optional[Decimal] = None,
                            horario_trabajo: Optional[Dict[str, Any]] = None,
                            observaciones: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea un nuevo registro de personal con nombres separados - ACTUALIZADA
        """
        data = {
            "usuario_id": usuario_id,
            "primer_nombre": primer_nombre,
            "primer_apellido": primer_apellido,
            "numero_documento": numero_documento,
            "tipo_documento": tipo_documento,
            "celular": celular,
            "tipo_personal": tipo_personal,
            "estado_laboral": "activo"
        }
       
        # Agregar campos opcionales solo si no están vacíos
        if segundo_nombre and segundo_nombre.strip():
            data["segundo_nombre"] = segundo_nombre.strip()
        if segundo_apellido and segundo_apellido.strip():
            data["segundo_apellido"] = segundo_apellido.strip()
        if fecha_nacimiento:
            data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
        if direccion and direccion.strip():
            data["direccion"] = direccion.strip()
        if especialidad and especialidad.strip():
            data["especialidad"] = especialidad.strip()
        if numero_licencia and numero_licencia.strip():
            data["numero_licencia"] = numero_licencia.strip()
        if fecha_contratacion:
            data["fecha_contratacion"] = fecha_contratacion.isoformat()
        else:
            data["fecha_contratacion"] = date.today().isoformat()
        if salario:
            data["salario"] = float(salario)
        if horario_trabajo:
            data["horario_trabajo"] = horario_trabajo
        if observaciones and observaciones.strip():
            data["observaciones"] = observaciones.strip()
        
        print("------------------------------------------------------------------------------------")
       
        logger.info(f"Creando registro de personal para {primer_nombre} {primer_apellido}")
        return self.create(data)

    

    @handle_supabase_error
    def get_all_from_view(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todo el personal usando la vista vista_personal_completo
        
        Args:
            filters: Filtros opcionales
            
        Returns:
            Lista de personal con información completa
        """
        query = self.client.table('vista_personal_completo').select("*")
        
        # Aplicar filtros
        if filters:
            for field, value in filters.items():
                if value is not None:
                    query = query.eq(field, value)
        
        response = query.execute()
        return response.data


    @handle_supabase_error
    def get_filtered_personal(self, 
                            tipo_personal: Optional[str] = None,
                            estado_laboral: Optional[str] = None,
                            solo_activos: bool = True,
                            busqueda: Optional[str] = None) -> List[Dict[str, Any]]:

        """Obtener personal usando la vista (método preferido)"""
        query = self.client.table('vista_personal_completo').select("*")
        
        # Aplicar filtros básicos
        if solo_activos:
            query = query.eq('completamente_activo', True)
        
        if tipo_personal and tipo_personal != 'todos':
            query = query.eq('tipo_personal', tipo_personal)
            
        if estado_laboral and estado_laboral != 'todos':
            query = query.eq('estado_laboral', estado_laboral)
        
        # Ejecutar consulta
        response = query.execute()
        resultados = response.data or []
        
        # Aplicar filtro de búsqueda en memoria (más flexible)
        if busqueda and busqueda.strip():
            resultados = self._apply_search_filter(resultados, busqueda.strip())
        
        logger.info(f"✅ Personal obtenido desde vista: {len(resultados)} registros")
        return resultados

    def _get_personal_with_joins(self, tipo_personal: Optional[str], estado_laboral: Optional[str],
                                solo_activos: bool, busqueda: Optional[str]) -> List[Dict[str, Any]]:
        
        """Fallback: obtener personal usando JOINs directos"""
        query = self.table.select("""
            *,
            usuarios!inner(
                id, email, telefono, activo, ultimo_acceso, auth_user_id,
                roles!inner(nombre, descripcion, permisos)
            )
        """)
        
        # Aplicar filtros
        if solo_activos:
            query = query.eq('estado_laboral', 'activo')
            query = query.eq('usuarios.activo', True)
            
        if tipo_personal and tipo_personal != 'todos':
            query = query.eq('tipo_personal', tipo_personal)
            
        if estado_laboral and estado_laboral != 'todos':
            query = query.eq('estado_laboral', estado_laboral)
        
        # Ordenar
        query = query.order('primer_nombre, primer_apellido')
        
        response = query.execute()
        resultados = []
        
        # Transformar datos para compatibilidad con la vista
        for item in response.data or []:
            # Construir nombre completo
            nombres = []
            if item.get('primer_nombre'):
                nombres.append(item['primer_nombre'])
            if item.get('segundo_nombre'):
                nombres.append(item['segundo_nombre'])
            if item.get('primer_apellido'):
                nombres.append(item['primer_apellido'])
            if item.get('segundo_apellido'):
                nombres.append(item['segundo_apellido'])
            
            nombre_completo = ' '.join(nombres) if nombres else 'Sin nombre'
            
            # Reestructurar para compatibilidad
            usuarios_data = item.get('usuarios', {})
            if isinstance(usuarios_data, dict):
                usuarios_data['nombre_completo'] = nombre_completo
                item['nombre_completo'] = nombre_completo
                item['completamente_activo'] = (
                    item.get('estado_laboral') == 'activo' and 
                    usuarios_data.get('activo', False)
                )
            
            resultados.append(item)
        
        # Aplicar búsqueda
        if busqueda and busqueda.strip():
            resultados = self._apply_search_filter(resultados, busqueda.strip())
        
        logger.info(f"✅ Personal obtenido con JOINs (fallback): {len(resultados)} registros")
        return resultados


    def _apply_search_filter(self, items: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
        """Aplicar filtro de búsqueda en memoria"""
        search_lower = search_term.lower()
        filtered = []
        
        for item in items:
            # Campos donde buscar
            search_fields = [
                str(item.get('nombre_completo', '')).lower(),
                str(item.get('email', '')).lower(),
                str(item.get('numero_documento', '')).lower(),
                str(item.get('especialidad', '')).lower(),
                str(item.get('tipo_personal', '')).lower(),
                # Si usuarios es dict anidado
                str(item.get('usuarios', {}).get('email', '') if isinstance(item.get('usuarios'), dict) else '').lower()
            ]
            
            # Si algún campo contiene el término
            if any(search_lower in field for field in search_fields):
                filtered.append(item)
        
        return filtered

    @handle_supabase_error  
    def get_all_personal(self, solo_activos: bool = True) -> List[Dict[str, Any]]:
        """
        Obtiene todo el personal - SIMPLIFICADA
        """
        return self.get_filtered_personal(
            tipo_personal=None,
            estado_laboral=None,
            solo_activos=solo_activos,
            busqueda=None
        )

    # ==========================================
    # CONSULTAS ESPECÍFICAS 
    # ==========================================


    @handle_supabase_error
    def get_by_documento(self, numero_documento: str) -> Optional[Dict[str, Any]]:
        """Obtiene personal por número de documento"""
        response = self.table.select("*").eq("numero_documento", numero_documento).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_by_usuario_id(self, usuario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene personal por ID de usuario"""
        response = self.table.select("*").eq("usuario_id", usuario_id).execute()
        return response.data[0] if response.data else None
    
    
    @handle_supabase_error
    def get_by_type(self, tipo_personal: str, solo_activos: bool = True) -> List[Dict[str, Any]]:
        """Obtiene personal de un tipo específico"""
        return self.get_filtered_personal(
            tipo_personal=tipo_personal,
            estado_laboral=None,
            solo_activos=solo_activos,
            busqueda=None
        )
    
    @handle_supabase_error
    def get_dentists(self, incluir_inactivos: bool = False) -> List[Dict[str, Any]]:
        """Obtiene todos los odontólogos"""
        return self.get_by_type("Odontólogo", not incluir_inactivos)
    
   # ==========================================
    # ACTUALIZACIÓN DE ESTADO - SIMPLIFICADAS
    # ==========================================
    
    @handle_supabase_error
    def update_work_status(self, 
                          staff_id: str, 
                          nuevo_estado: str,
                          observaciones: Optional[str] = None) -> Dict[str, Any]:
        """
        Actualiza el estado laboral del personal
        
        Args:
            staff_id: ID del personal
            nuevo_estado: Nuevo estado (activo, vacaciones, licencia, inactivo)
            observaciones: Observaciones sobre el cambio
            
        Returns:
            Personal actualizado
        """
        data = {"estado_laboral": nuevo_estado}
        
        if observaciones:
            personal = self.get_by_id(staff_id)
            obs_actuales = personal.get("observaciones", "") if personal else ""
            data["observaciones"] = f"{obs_actuales}\n{date.today()}: {observaciones}"
        
        logger.info(f"Actualizando estado laboral de {staff_id} a {nuevo_estado}")
        return self.update(staff_id, data)
    
    @handle_supabase_error
    def update_schedule(self, staff_id: str, nuevo_horario: Dict[str, str]) -> Dict[str, Any]:
        """
        Actualiza el horario de trabajo
        
        Args:
            staff_id: ID del personal
            nuevo_horario: Nuevo horario {dia: "HH:MM-HH:MM"}
            
        Returns:
            Personal actualizado
        """
        return self.update(staff_id, {"horario_trabajo": nuevo_horario})
    
    @handle_supabase_error
    def update_salary(self, 
                     staff_id: str, 
                     nuevo_salario: Decimal,
                     fecha_efectiva: Optional[date] = None) -> Dict[str, Any]:
        """
        Actualiza el salario del personal
        
        Args:
            staff_id: ID del personal
            nuevo_salario: Nuevo salario
            fecha_efectiva: Fecha efectiva del cambio
            
        Returns:
            Personal actualizado
        """
        personal = self.get_by_id(staff_id)
        if not personal:
            raise ValueError(f"Personal {staff_id} no encontrado")
        
        # Registrar cambio en observaciones
        fecha = fecha_efectiva or date.today()
        salario_anterior = personal.get("salario", 0)
        observacion = f"\nCambio de salario {fecha}: ${salario_anterior} -> ${nuevo_salario}"
        
        obs_actuales = personal.get("observaciones", "")
        
        data = {
            "salario": float(nuevo_salario),
            "observaciones": obs_actuales + observacion
        }
        
        return self.update(staff_id, data)
    
    @handle_supabase_error
    def get_staff_performance(self, staff_id: str, mes: Optional[int] = None, año: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtiene métricas de desempeño del personal
        
        Args:
            staff_id: ID del personal
            mes: Mes a consultar (opcional)
            año: Año a consultar (opcional)
            
        Returns:
            Métricas de desempeño
        """
        from datetime import datetime
        
        # Si no se especifica mes/año, usar el actual
        if not mes or not año:
            ahora = datetime.now()
            mes = mes or ahora.month
            año = año or ahora.year
        
        # Obtener información del personal
        # personal = self.get_staff_details(staff_id)
        # if not personal:
        #     return None
        
        performance = {
            # "personal": personal,
            "periodo": f"{mes}/{año}",
            "metricas": {}
        }
        
        # Para odontólogos, obtener métricas de consultas e intervenciones
        if personal["tipo_personal"] == "Odontólogo":
            # Consultas atendidas
            consultas_response = self.client.table("consultas").select(
                "id, estado, costo_total"
            ).eq("odontologo_id", staff_id
            ).gte("fecha_programada", f"{año}-{mes:02d}-01"
            ).lt("fecha_programada", f"{año}-{mes+1:02d}-01" if mes < 12 else f"{año+1}-01-01"
            ).execute()
            
            consultas = consultas_response.data
            
            performance["metricas"]["consultas_programadas"] = len(consultas)
            performance["metricas"]["consultas_completadas"] = len([c for c in consultas if c["estado"] == "completada"])
            performance["metricas"]["consultas_canceladas"] = len([c for c in consultas if c["estado"] == "cancelada"])
            performance["metricas"]["no_asistencias"] = len([c for c in consultas if c["estado"] == "no_asistio"])
            performance["metricas"]["ingresos_generados"] = sum(c.get("costo_total", 0) for c in consultas if c["estado"] == "completada")
            
            # Intervenciones realizadas
            intervenciones_response = self.client.table("intervenciones").select(
                "id, estado, precio_final"
            ).eq("odontologo_id", staff_id
            ).gte("hora_inicio", f"{año}-{mes:02d}-01"
            ).lt("hora_inicio", f"{año}-{mes+1:02d}-01" if mes < 12 else f"{año+1}-01-01"
            ).execute()
            
            intervenciones = intervenciones_response.data
            
            performance["metricas"]["intervenciones_realizadas"] = len([i for i in intervenciones if i["estado"] == "completada"])
            performance["metricas"]["ingresos_intervenciones"] = sum(i["precio_final"] for i in intervenciones if i["estado"] == "completada")
        
        return performance
    

    # ==========================================
    # BÚSQUEDA Y ESTADÍSTICAS 
    # ==========================================


    @handle_supabase_error
    def search_staff(self, search_term: str) -> List[Dict[str, Any]]:
        """Busca personal por término general"""
        return self.get_filtered_personal(
            tipo_personal=None,
            estado_laboral=None,
            solo_activos=True,
            busqueda=search_term
        )
    
    @handle_supabase_error
    def get_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas básicas del personal"""
        try:
            # Usar vista para estadísticas
            all_personal = self.client.table('vista_personal_completo').select("tipo_personal, completamente_activo").execute()
            data = all_personal.data or []
            
            stats = {
                "total": len(data),
                "activos": len([p for p in data if p.get('completamente_activo')]),
                "odontologos": len([p for p in data if p.get('tipo_personal') == 'Odontólogo']),
                "administradores": len([p for p in data if p.get('tipo_personal') == 'Administrador']),
                "asistentes": len([p for p in data if p.get('tipo_personal') == 'Asistente']),
                "gerentes": len([p for p in data if p.get('tipo_personal') == 'Gerente'])
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            # Fallback simple
            return {
                "total": 0,
                "activos": 0, 
                "odontologos": 0,
                "administradores": 0,
                "asistentes": 0,
                "gerentes": 0
            }