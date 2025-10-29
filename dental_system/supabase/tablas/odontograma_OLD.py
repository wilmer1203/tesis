"""
Operaciones CRUD para las tablas odontograma y condiciones_diente
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class OdontogramsTable(BaseTable):
    """
    Maneja todas las operaciones CRUD para odontogramas y condiciones de dientes
    """
    
    def __init__(self):
        super().__init__('odontograma')
        # También necesitamos acceso a la tabla condiciones_diente
        self.conditions_table = 'condiciones_diente'
        self.teeth_table = 'dientes'
    
    @handle_supabase_error
    def create_odontogram(self,
                         paciente_id: str,
                         odontologo_id: str,
                         tipo_odontograma: str = 'adulto',
                         notas_generales: Optional[str] = None,
                         observaciones_clinicas: Optional[str] = None,
                         template_usado: str = 'universal') -> Dict[str, Any]:
        """
        Crea un nuevo odontograma para un paciente
        
        Args:
            paciente_id: ID del paciente
            odontologo_id: ID del odontólogo
            tipo_odontograma: Tipo (adulto, pediatrico, mixto)
            notas_generales: Notas generales del odontograma
            observaciones_clinicas: Observaciones clínicas
            template_usado: Template usado para el odontograma
            
        Returns:
            Odontograma creado
        """
        # Verificar si el paciente ya tiene un odontograma activo
        odontograma_activo = self.get_active_odontogram(paciente_id)
        if odontograma_activo:
            # Desactivar el anterior
            self.update(odontograma_activo["id"], {"activo": False})
            nueva_version = odontograma_activo.get("version", 1) + 1
        else:
            nueva_version = 1
        
        data = {
            "paciente_id": paciente_id,
            "odontologo_id": odontologo_id,
            "tipo_odontograma": tipo_odontograma,
            "version": nueva_version,
            "activo": True,
            "template_usado": template_usado
        }
        
        if notas_generales:
            data["notas_generales"] = notas_generales
        if observaciones_clinicas:
            data["observaciones_clinicas"] = observaciones_clinicas
        
        logger.info(f"Creando odontograma v{nueva_version} para paciente {paciente_id}")
        return self.create(data)
    
    @handle_supabase_error
    def get_active_odontogram(self, paciente_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el odontograma activo de un paciente
        
        Args:
            paciente_id: ID del paciente
            
        Returns:
            Odontograma activo o None
        """
        response = self.table.select("*").eq(
            "paciente_id", paciente_id
        ).eq("es_version_actual", True).execute()
        
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_odontogram_with_conditions(self, odontogram_id: str) -> Dict[str, Any]:
        """
        Obtiene un odontograma completo con todas las condiciones de dientes
        
        Args:
            odontogram_id: ID del odontograma
            
        Returns:
            Odontograma con condiciones de todos los dientes
        """
        # Obtener odontograma
        odontograma = self.get_by_id(odontogram_id)
        if not odontograma:
            return None
        
        # Obtener todas las condiciones de este odontograma
        conditions_response = self.client.table(self.conditions_table).select("""
            *,
            dientes!inner(
                numero_diente, nombre, tipo_diente, 
                ubicacion, cuadrante, es_temporal
            )
        """).eq("odontograma_id", odontogram_id).execute()
        
        # Organizar condiciones por diente
        condiciones_por_diente = {}
        for condicion in conditions_response.data:
            numero_diente = condicion["dientes"]["numero_diente"]
            if numero_diente not in condiciones_por_diente:
                condiciones_por_diente[numero_diente] = []
            condiciones_por_diente[numero_diente].append(condicion)
        
        odontograma["condiciones_por_diente"] = condiciones_por_diente
        return odontograma
    
    @handle_supabase_error
    def add_tooth_condition(self,
                          odontograma_id: str,
                          diente_id: str,
                          tipo_condicion: str,
                          caras_afectadas: Optional[List[str]] = None,
                          severidad: str = 'leve',
                          descripcion: Optional[str] = None,
                          observaciones: Optional[str] = None,
                          material_utilizado: Optional[str] = None,
                          color_material: Optional[str] = None,
                          fecha_tratamiento: Optional[date] = None,
                          estado: str = 'actual',
                          requiere_seguimiento: bool = False,
                          registrado_por: Optional[str] = None,
                          color_hex: str = '#FFFFFF') -> Dict[str, Any]:
        """
        Agrega o actualiza una condición a un diente
        
        Args:
            odontograma_id: ID del odontograma
            diente_id: ID del diente
            tipo_condicion: Tipo de condición (sano, caries, obturacion, etc.)
            caras_afectadas: Caras del diente afectadas
            severidad: Severidad (leve, moderada, severa)
            descripcion: Descripción de la condición
            observaciones: Observaciones adicionales
            material_utilizado: Material usado en tratamiento
            color_material: Color del material
            fecha_tratamiento: Fecha del tratamiento
            estado: Estado (planificado, en_tratamiento, actual, historico)
            requiere_seguimiento: Si requiere seguimiento
            registrado_por: ID del usuario que registra
            color_hex: Color para renderizado
            
        Returns:
            Condición creada
        """
        data = {
            "odontograma_id": odontograma_id,
            "diente_id": diente_id,
            "tipo_condicion": tipo_condicion,
            "severidad": severidad,
            "estado": estado,
            "requiere_seguimiento": requiere_seguimiento,
            "color_hex": color_hex
        }
        
        # Agregar campos opcionales
        if caras_afectadas:
            data["caras_afectadas"] = caras_afectadas
        if descripcion:
            data["descripcion"] = descripcion
        if observaciones:
            data["observaciones"] = observaciones
        if material_utilizado:
            data["material_utilizado"] = material_utilizado
        if color_material:
            data["color_material"] = color_material
        if fecha_tratamiento:
            data["fecha_tratamiento"] = fecha_tratamiento.isoformat()
        if registrado_por:
            data["registrado_por"] = registrado_por
        
        logger.info(f"Agregando condición {tipo_condicion} al diente {diente_id}")
        
        response = self.client.table(self.conditions_table).insert(data).execute()
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def update_tooth_condition(self,
                             condition_id: str,
                             updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una condición existente
        
        Args:
            condition_id: ID de la condición
            updates: Diccionario con actualizaciones
            
        Returns:
            Condición actualizada
        """
        response = self.client.table(self.conditions_table).update(
            updates
        ).eq("id", condition_id).execute()
        
        return response.data[0] if response.data else None
    
    @handle_supabase_error
    def get_tooth_history(self, paciente_id: str, numero_diente: int) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de un diente específico del paciente
        
        Args:
            paciente_id: ID del paciente
            numero_diente: Número del diente
            
        Returns:
            Lista de condiciones históricas del diente
        """
        # Primero obtener el diente_id
        diente_response = self.client.table(self.teeth_table).select("id").eq(
            "numero_diente", numero_diente
        ).execute()
        
        if not diente_response.data:
            return []
        
        diente_id = diente_response.data[0]["id"]
        
        # Obtener todos los odontogramas del paciente
        odontogramas_response = self.table.select("id, version, fecha_creacion").eq(
            "paciente_id", paciente_id
        ).order("version", desc=True).execute()
        
        # Obtener condiciones de ese diente en todos los odontogramas
        condiciones = []
        for odontograma in odontogramas_response.data:
            conditions_response = self.client.table(self.conditions_table).select("""
                *,
                odontograma!inner(version, fecha_creacion),
                registrador:usuarios!registrado_por(nombre_completo)
            """).eq("odontograma_id", odontograma["id"]
            ).eq("diente_id", diente_id).execute()
            
            condiciones.extend(conditions_response.data)
        
        # Ordenar por fecha
        condiciones.sort(key=lambda x: x["fecha_registro"], reverse=True)
        
        return condiciones
    
    @handle_supabase_error
    def get_teeth_by_condition(self, 
                             odontograma_id: str,
                             tipo_condicion: Optional[str] = None,
                             estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtiene dientes filtrados por condición
        
        Args:
            odontograma_id: ID del odontograma
            tipo_condicion: Filtrar por tipo de condición
            estado: Filtrar por estado
            
        Returns:
            Lista de dientes con sus condiciones
        """
        query = self.client.table(self.conditions_table).select("""
            *,
            dientes!inner(*)
        """).eq("odontograma_id", odontograma_id)
        
        if tipo_condicion:
            query = query.eq("tipo_condicion", tipo_condicion)
        if estado:
            query = query.eq("estado", estado)
        
        response = query.execute()
        return response.data
    
    @handle_supabase_error
    def get_treatment_plan(self, odontograma_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene el plan de tratamiento (condiciones planificadas)
        
        Args:
            odontograma_id: ID del odontograma
            
        Returns:
            Lista de tratamientos planificados
        """
        return self.get_teeth_by_condition(odontograma_id, estado='planificado')
    
    @handle_supabase_error
    def mark_treatment_completed(self,
                               condition_id: str,
                               fecha_tratamiento: date,
                               material_utilizado: Optional[str] = None,
                               observaciones: Optional[str] = None) -> Dict[str, Any]:
        """
        Marca un tratamiento planificado como completado
        
        Args:
            condition_id: ID de la condición
            fecha_tratamiento: Fecha en que se completó
            material_utilizado: Material usado
            observaciones: Observaciones del tratamiento
            
        Returns:
            Condición actualizada
        """
        updates = {
            "estado": "actual",
            "fecha_tratamiento": fecha_tratamiento.isoformat()
        }
        
        if material_utilizado:
            updates["material_utilizado"] = material_utilizado
        if observaciones:
            updates["observaciones"] = observaciones
        
        return self.update_tooth_condition(condition_id, updates)
    
    @handle_supabase_error
    def get_odontogram_summary(self, odontograma_id: str) -> Dict[str, Any]:
        """
        Obtiene un resumen del estado del odontograma
        
        Args:
            odontograma_id: ID del odontograma
            
        Returns:
            Resumen con estadísticas
        """
        # Obtener todas las condiciones
        conditions_response = self.client.table(self.conditions_table).select(
            "tipo_condicion, estado, severidad, requiere_seguimiento"
        ).eq("odontograma_id", odontograma_id).execute()
        
        condiciones = conditions_response.data
        
        # Calcular estadísticas
        resumen = {
            "total_dientes_afectados": len(set(c["diente_id"] for c in condiciones)),
            "por_tipo_condicion": {},
            "por_estado": {},
            "por_severidad": {},
            "requieren_seguimiento": 0,
            "dientes_sanos": 0,
            "dientes_con_caries": 0,
            "dientes_obturados": 0,
            "dientes_ausentes": 0
        }
        
        # Contar por categorías
        for condicion in condiciones:
            # Por tipo
            tipo = condicion["tipo_condicion"]
            resumen["por_tipo_condicion"][tipo] = resumen["por_tipo_condicion"].get(tipo, 0) + 1
            
            # Por estado
            estado = condicion["estado"]
            resumen["por_estado"][estado] = resumen["por_estado"].get(estado, 0) + 1
            
            # Por severidad
            severidad = condicion["severidad"]
            resumen["por_severidad"][severidad] = resumen["por_severidad"].get(severidad, 0) + 1
            
            # Requieren seguimiento
            if condicion["requiere_seguimiento"]:
                resumen["requieren_seguimiento"] += 1
            
            # Contadores específicos
            if tipo == "sano":
                resumen["dientes_sanos"] += 1
            elif tipo == "caries":
                resumen["dientes_con_caries"] += 1
            elif tipo == "obturacion":
                resumen["dientes_obturados"] += 1
            elif tipo == "ausente":
                resumen["dientes_ausentes"] += 1
        
        return resumen
    
    @handle_supabase_error
    def clone_odontogram(self,
                        odontograma_origen_id: str,
                        odontologo_id: str,
                        notas: Optional[str] = None) -> Dict[str, Any]:
        """
        Clona un odontograma existente creando una nueva versión
        
        Args:
            odontograma_origen_id: ID del odontograma a clonar
            odontologo_id: ID del odontólogo que crea la nueva versión
            notas: Notas sobre la nueva versión
            
        Returns:
            Nuevo odontograma creado
        """
        # Obtener odontograma origen
        origen = self.get_by_id(odontograma_origen_id)
        if not origen:
            raise ValueError(f"Odontograma {odontograma_origen_id} no encontrado")
        
        # Crear nuevo odontograma
        nuevo_odontograma = self.create_odontogram(
            paciente_id=origen["paciente_id"],
            odontologo_id=odontologo_id,
            tipo_odontograma=origen["tipo_odontograma"],
            notas_generales=notas or f"Clonado de versión {origen['version']}",
            template_usado=origen["template_usado"]
        )
        
        # Copiar todas las condiciones actuales
        conditions_response = self.client.table(self.conditions_table).select("*").eq(
            "odontograma_id", odontograma_origen_id
        ).eq("estado", "actual").execute()
        
        for condicion in conditions_response.data:
            # Crear copia de la condición
            nueva_condicion = condicion.copy()
            del nueva_condicion["id"]
            del nueva_condicion["fecha_registro"]
            nueva_condicion["odontograma_id"] = nuevo_odontograma["id"]
            nueva_condicion["registrado_por"] = odontologo_id
            
            self.client.table(self.conditions_table).insert(nueva_condicion).execute()
        
        return nuevo_odontograma
    
    @handle_supabase_error
    def get_all_teeth(self, tipo_odontograma: str = 'adulto') -> List[Dict[str, Any]]:
        """
        Obtiene todos los dientes según el tipo de odontograma
        
        Args:
            tipo_odontograma: Tipo (adulto, pediatrico, mixto)
            
        Returns:
            Lista de dientes disponibles
        """
        query = self.client.table(self.teeth_table).select("*")
        
        if tipo_odontograma == 'adulto':
            query = query.eq("es_temporal", False)
        elif tipo_odontograma == 'pediatrico':
            query = query.eq("es_temporal", True)
        # Si es 'mixto', no filtrar
        
        query = query.order("numero_diente")
        response = query.execute()
        
        return response.data
    
    @handle_supabase_error
    def get_teeth_by_quadrant(self, cuadrante: int) -> List[Dict[str, Any]]:
        """
        Obtiene todos los dientes de un cuadrante
        
        Args:
            cuadrante: Número del cuadrante (1-8)
            
        Returns:
            Lista de dientes del cuadrante
        """
        response = self.client.table(self.teeth_table).select("*").eq(
            "cuadrante", cuadrante
        ).order("posicion_en_cuadrante").execute()
        
        return response.data


# Instancia única para importar
odontograms_table = OdontogramsTable()