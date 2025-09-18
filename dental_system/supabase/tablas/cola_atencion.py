"""
Operaciones CRUD para la tabla cola_atencion - Sistema de colas por odontólogo
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from .base import BaseTable
from ..client import handle_supabase_error
import logging

logger = logging.getLogger(__name__)


class ColaAtencionTable(BaseTable):
    """
    Maneja operaciones para la tabla cola_atencion
    Sistema de colas independientes por odontólogo
    """

    def __init__(self):
        super().__init__('cola_atencion')

    @handle_supabase_error
    def agregar_a_cola(self,
                      consulta_id: str,
                      odontologo_id: str,
                      posicion_cola: int = None) -> Dict[str, Any]:
        """
        Agregar consulta a cola de odontólogo específico

        Args:
            consulta_id: ID de la consulta
            odontologo_id: ID del odontólogo
            posicion_cola: Posición en la cola (se calcula automáticamente si no se proporciona)

        Returns:
            Registro creado en cola_atencion
        """
        logger.info(f"Agregando consulta {consulta_id} a cola del odontólogo {odontologo_id}")

        # Si no se proporciona posición, calcular la siguiente disponible
        if posicion_cola is None:
            posicion_cola = self._calcular_siguiente_posicion(odontologo_id)

        data = {
            'consulta_id': consulta_id,
            'odontologo_id': odontologo_id,
            'posicion_cola': posicion_cola,
            'estado_cola': 'esperando'
        }

        result = self.client.table(self.table_name).insert(data).execute()
        return result.data[0] if result.data else None

    @handle_supabase_error
    def obtener_cola_odontologo(self, odontologo_id: str) -> List[Dict[str, Any]]:
        """
        Obtener cola completa de un odontólogo ordenada por posición

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Lista de consultas en la cola con información del paciente
        """
        logger.info(f"Obteniendo cola del odontólogo {odontologo_id}")

        result = self.client.table(self.table_name).select(
            """
            *,
            consultas!inner(
                id,
                numero_consulta,
                estado,
                prioridad,
                motivo_consulta,
                fecha_llegada,
                pacientes!inner(
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    numero_documento,
                    celular_1
                )
            )
            """
        ).eq(
            'odontologo_id', odontologo_id
        ).eq(
            'estado_cola', 'esperando'
        ).order('posicion_cola').execute()

        return result.data if result.data else []

    @handle_supabase_error
    def obtener_proximo_paciente(self, odontologo_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtener el próximo paciente en la cola del odontólogo

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Datos del próximo paciente o None si no hay cola
        """
        logger.info(f"Obteniendo próximo paciente para odontólogo {odontologo_id}")

        result = self.client.table(self.table_name).select(
            """
            *,
            consultas!inner(
                id,
                numero_consulta,
                estado,
                prioridad,
                motivo_consulta,
                fecha_llegada,
                pacientes!inner(
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    numero_documento,
                    celular_1
                )
            )
            """
        ).eq(
            'odontologo_id', odontologo_id
        ).eq(
            'estado_cola', 'esperando'
        ).order('posicion_cola').limit(1).execute()

        return result.data[0] if result.data else None

    @handle_supabase_error
    def cambiar_estado_cola(self,
                           consulta_id: str,
                           nuevo_estado: str) -> Dict[str, Any]:
        """
        Cambiar estado de una consulta en la cola

        Args:
            consulta_id: ID de la consulta
            nuevo_estado: Nuevo estado ('esperando', 'siendo_atendido', 'atendido', 'derivado', 'cancelado')

        Returns:
            Registro actualizado
        """
        logger.info(f"Cambiando estado de consulta {consulta_id} a {nuevo_estado}")

        data = {
            'estado_cola': nuevo_estado
        }

        result = self.client.table(self.table_name).update(data).eq(
            'consulta_id', consulta_id
        ).execute()

        return result.data[0] if result.data else None

    @handle_supabase_error
    def transferir_consulta(self,
                           consulta_id: str,
                           nuevo_odontologo_id: str,
                           motivo: str) -> Dict[str, Any]:
        """
        Transferir consulta de un odontólogo a otro

        Args:
            consulta_id: ID de la consulta a transferir
            nuevo_odontologo_id: ID del nuevo odontólogo
            motivo: Motivo de la transferencia (obligatorio)

        Returns:
            Nuevo registro en cola_atencion
        """
        if not motivo or motivo.strip() == "":
            raise ValueError("El motivo de transferencia es obligatorio")

        logger.info(f"Transfiriendo consulta {consulta_id} a odontólogo {nuevo_odontologo_id}")

        # Marcar registro actual como transferido
        self.cambiar_estado_cola(consulta_id, 'derivado')

        # Crear nuevo registro en la cola del nuevo odontólogo
        nueva_posicion = self._calcular_siguiente_posicion(nuevo_odontologo_id)

        data = {
            'consulta_id': consulta_id,
            'odontologo_id': nuevo_odontologo_id,
            'posicion_cola': nueva_posicion,
            'estado_cola': 'esperando'
        }

        result = self.client.table(self.table_name).insert(data).execute()
        return result.data[0] if result.data else None

    @handle_supabase_error
    def obtener_estadisticas_colas(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de todas las colas

        Returns:
            Diccionario con estadísticas por odontólogo
        """
        logger.info("Obteniendo estadísticas de colas")

        result = self.client.table(self.table_name).select(
            """
            odontologo_id,
            estado_cola,
            personal!inner(primer_nombre, primer_apellido, especialidad)
            """
        ).execute()

        estadisticas = {}
        for registro in result.data:
            odontologo_id = registro['odontologo_id']
            estado = registro['estado_cola']

            if odontologo_id not in estadisticas:
                personal_data = registro.get('personal', {})
                estadisticas[odontologo_id] = {
                    'nombre': f"{personal_data.get('primer_nombre', '')} {personal_data.get('primer_apellido', '')}".strip(),
                    'especialidad': personal_data.get('especialidad', ''),
                    'esperando': 0,
                    'atendiendo': 0,
                    'atendidos': 0,
                    'total': 0
                }

            if estado == 'esperando':
                estadisticas[odontologo_id]['esperando'] += 1
            elif estado == 'siendo_atendido':
                estadisticas[odontologo_id]['atendiendo'] += 1
            elif estado == 'atendido':
                estadisticas[odontologo_id]['atendidos'] += 1

            estadisticas[odontologo_id]['total'] += 1

        return estadisticas

    def _calcular_siguiente_posicion(self, odontologo_id: str) -> int:
        """
        Calcular la siguiente posición disponible en la cola del odontólogo

        Args:
            odontologo_id: ID del odontólogo

        Returns:
            Siguiente posición en la cola
        """
        result = self.client.table(self.table_name).select(
            'posicion_cola'
        ).eq(
            'odontologo_id', odontologo_id
        ).eq(
            'estado_cola', 'esperando'
        ).order('posicion_cola', desc=True).limit(1).execute()

        if result.data:
            return result.data[0]['posicion_cola'] + 1
        else:
            return 1


# Instancia global para importar
cola_atencion_table = ColaAtencionTable()