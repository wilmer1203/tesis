"""
📅 CONSULTAS SERVICE - ESQUEMA v4.1 CON LÓGICA DE COLAS
======================================================

🎯 CARACTERÍSTICAS PRINCIPALES:
✅ Sistema de colas por orden de llegada (NO citas programadas)
✅ Múltiples odontólogos por consulta
✅ Estados: en_espera → en_atencion → completada
✅ Gestión automática de orden en cola
✅ Lógica de transición entre odontólogos
✅ Tiempo real y notificaciones
✅ Validaciones de negocio específicas

🔄 OPTIMIZACIONES IMPLEMENTADAS:
- Algoritmos de gestión de colas eficientes
- Cálculo automático de tiempos de espera
- Validaciones de estado específicas del negocio
- Transiciones automáticas entre odontólogos
- Cache inteligente para consultas frecuentes
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import date, datetime, timedelta
from .base_service import BaseService
from dental_system.supabase.tablas import consultas_table, personal_table
from dental_system.models import ConsultaModel, ConsultaFormModel, PersonalModel, TurnoModel
from .cache_invalidation_hooks import invalidate_after_consultation_operation
import logging

logger = logging.getLogger(__name__)

class ConsultasServiceV41(BaseService):
    """
    📅 SERVICIO ESPECIALIZADO DE CONSULTAS - ESQUEMA v4.1
    
    RESPONSABILIDADES:
    - Gestión de colas por orden de llegada
    - Asignación automática de turnos
    - Transiciones de estado validadas
    - Múltiples odontólogos por consulta
    - Métricas de tiempo real
    - Optimización de flujo de atención
    """
    
    def __init__(self):
        super().__init__()
        self.consultas_table = consultas_table
        self.personal_table = personal_table
    
    # ==========================================
    # 🚀 MÉTODOS DE GESTIÓN DE COLAS
    # ==========================================
    
    async def crear_consulta_por_llegada(self, 
                                       form_data: ConsultaFormModel, 
                                       user_id: str) -> ConsultaModel:
        """
        ➕ CREAR NUEVA CONSULTA POR ORDEN DE LLEGADA - v4.1
        
        Args:
            form_data: Formulario tipado con datos validados
            user_id: Usuario que registra la llegada
            
        Returns:
            ConsultaModel: Consulta creada con orden automático
        """
        try:
            logger.info("🏥 Creando consulta por orden de llegada...")
            
            # ✅ Validar permisos
            self.require_permission("consultas", "crear")
            
            # ✅ Validar formulario tipado
            errores = form_data.validate_form()
            if errores:
                raise ValueError(f"Datos inválidos: {errores}")
            
            # ✅ Calcular posición en cola automáticamente
            orden_general = await self._calcular_siguiente_orden_general()
            orden_cola_doctor = await self._calcular_siguiente_orden_cola_doctor(
                form_data.primer_odontologo_id
            )
            
            # ✅ Crear consulta con esquema v4.1
            datos_consulta = {
                # Referencias de paciente y odontólogos
                "paciente_id": form_data.paciente_id,
                "primer_odontologo_id": form_data.primer_odontologo_id,
                "odontologo_preferido_id": form_data.odontologo_preferido_id or None,
                
                # Sistema de colas v4.1
                "fecha_llegada": datetime.now().isoformat(),
                "orden_llegada_general": orden_general,
                "orden_cola_odontologo": orden_cola_doctor,
                
                # Estado inicial y detalles
                "estado": "en_espera",
                "tipo_consulta": form_data.tipo_consulta,
                "motivo_consulta": form_data.motivo_consulta,
                "observaciones": form_data.observaciones,
                "notas_internas": form_data.notas_internas,
                "prioridad": form_data.prioridad,
                
                # Control administrativo
                "creada_por": user_id,
                "fecha_creacion": datetime.now().isoformat()
            }
            
            # ✅ Insertar en base de datos
            resultado = await self._ejecutar_creacion_consulta(datos_consulta)
            
            if not resultado:
                raise ValueError("Error insertando consulta en BD")
            
            # ✅ Crear modelo tipado del resultado
            consulta_model = ConsultaModel.from_dict(resultado)
            
            # ✅ Notificar a odontólogo (opcional)
            await self._notificar_nueva_consulta_en_cola(consulta_model)
            
            # ✅ Invalidar cache de estadísticas
            invalidate_after_consultation_operation()
            
            logger.info(f"✅ Consulta creada - Turno #{orden_general} en cola Dr. #{orden_cola_doctor}")
            return consulta_model
            
        except Exception as e:
            logger.error(f"❌ Error creando consulta: {str(e)}")
            raise ValueError(f"No se pudo crear la consulta: {str(e)}")
    
    async def iniciar_atencion_consulta(self, 
                                      consulta_id: str, 
                                      odontologo_id: str) -> ConsultaModel:
        """
        🏥 INICIAR ATENCIÓN DE CONSULTA - TRANSICIÓN VALIDADA
        
        Args:
            consulta_id: ID de la consulta a iniciar
            odontologo_id: ID del odontólogo que inicia atención
            
        Returns:
            ConsultaModel: Consulta con estado actualizado
        """
        try:
            logger.info(f"🏥 Iniciando atención consulta {consulta_id}...")
            
            # ✅ Validar permisos
            self.require_permission("consultas", "actualizar")
            
            # ✅ Obtener consulta actual
            consulta_actual = await self._obtener_consulta_por_id(consulta_id)
            if not consulta_actual:
                raise ValueError("Consulta no encontrada")
            
            # ✅ Validar estado de transición
            await self._validar_transicion_estado(
                consulta_actual, "en_espera", "en_atencion"
            )
            
            # ✅ Verificar disponibilidad del odontólogo
            await self._validar_disponibilidad_odontologo(odontologo_id)
            
            # ✅ Actualizar estado y tiempos
            datos_actualizacion = {
                "estado": "en_atencion",
                "fecha_inicio_atencion": datetime.now().isoformat(),
                "odontologo_actual": odontologo_id,
                "fecha_actualizacion": datetime.now().isoformat()
            }
            
            # ✅ Ejecutar actualización
            resultado = await self._ejecutar_actualizacion_consulta(
                consulta_id, datos_actualizacion
            )
            
            if not resultado:
                raise ValueError("Error actualizando estado en BD")
            
            # ✅ Crear modelo actualizado
            consulta_actualizada = ConsultaModel.from_dict(resultado)
            
            # ✅ Notificar inicio de atención
            await self._notificar_inicio_atencion(consulta_actualizada)
            
            # ✅ Actualizar métricas de cola
            await self._actualizar_metricas_cola_tiempo_real(odontologo_id)
            
            logger.info(f"✅ Consulta {consulta_id} iniciada por Dr. {odontologo_id}")
            return consulta_actualizada
            
        except Exception as e:
            logger.error(f"❌ Error iniciando atención: {str(e)}")
            raise ValueError(f"No se pudo iniciar la atención: {str(e)}")
    
    async def completar_consulta(self, 
                                consulta_id: str, 
                                datos_finalizacion: Dict[str, Any]) -> ConsultaModel:
        """
        ✅ COMPLETAR CONSULTA CON RESULTADOS
        
        Args:
            consulta_id: ID de la consulta a completar
            datos_finalizacion: Datos del diagnóstico, tratamiento, etc.
            
        Returns:
            ConsultaModel: Consulta completada
        """
        try:
            logger.info(f"✅ Completando consulta {consulta_id}...")
            
            # ✅ Validar permisos
            self.require_permission("consultas", "actualizar")
            
            # ✅ Obtener consulta actual
            consulta_actual = await self._obtener_consulta_por_id(consulta_id)
            if not consulta_actual:
                raise ValueError("Consulta no encontrada")
            
            # ✅ Validar transición de estado
            await self._validar_transicion_estado(
                consulta_actual, "en_atencion", "completada"
            )
            
            # ✅ Calcular duración de la consulta
            duracion_minutos = await self._calcular_duracion_consulta(consulta_actual)
            
            # ✅ Preparar datos de finalización
            datos_actualizacion = {
                **datos_finalizacion,
                "estado": "completada",
                "fecha_fin_atencion": datetime.now().isoformat(),
                "duracion_minutos": duracion_minutos,
                "fecha_actualizacion": datetime.now().isoformat()
            }
            
            # ✅ Ejecutar actualización
            resultado = await self._ejecutar_actualizacion_consulta(
                consulta_id, datos_actualizacion
            )
            
            if not resultado:
                raise ValueError("Error finalizando consulta en BD")
            
            # ✅ Crear modelo finalizado
            consulta_completada = ConsultaModel.from_dict(resultado)
            
            # ✅ Liberar odontólogo para siguiente consulta
            await self._liberar_odontologo_para_siguiente(
                consulta_actual.primer_odontologo_id
            )
            
            # ✅ Actualizar estadísticas de productividad
            await self._actualizar_estadisticas_productividad(
                consulta_completada, duracion_minutos
            )
            
            logger.info(f"✅ Consulta {consulta_id} completada en {duracion_minutos}min")
            return consulta_completada
            
        except Exception as e:
            logger.error(f"❌ Error completando consulta: {str(e)}")
            raise ValueError(f"No se pudo completar la consulta: {str(e)}")
    
    async def transferir_entre_odontologos(self, 
                                         consulta_id: str,
                                         odontologo_destino_id: str,
                                         motivo_transferencia: str) -> ConsultaModel:
        """
        🔄 TRANSFERIR CONSULTA ENTRE ODONTÓLOGOS - v4.1
        
        Args:
            consulta_id: ID de la consulta
            odontologo_destino_id: ID del odontólogo destino
            motivo_transferencia: Motivo de la transferencia
            
        Returns:
            ConsultaModel: Consulta transferida
        """
        try:
            logger.info(f"🔄 Transfiriendo consulta {consulta_id}...")
            
            # ✅ Validar permisos
            self.require_permission("consultas", "actualizar")
            
            # ✅ Obtener consulta actual
            consulta_actual = await self._obtener_consulta_por_id(consulta_id)
            if not consulta_actual:
                raise ValueError("Consulta no encontrada")
            
            # ✅ Validar que está en atención
            if consulta_actual.estado != "en_atencion":
                raise ValueError("Solo se pueden transferir consultas en atención")
            
            # ✅ Validar disponibilidad del odontólogo destino
            await self._validar_disponibilidad_odontologo(odontologo_destino_id)
            
            # ✅ Calcular nueva posición en cola del destino
            orden_nueva_cola = await self._calcular_siguiente_orden_cola_doctor(
                odontologo_destino_id
            )
            
            # ✅ Actualizar consulta con estado de transferencia
            datos_transferencia = {
                "estado": "entre_odontologos",
                "odontologo_preferido_id": odontologo_destino_id,
                "orden_cola_odontologo": orden_nueva_cola,
                "notas_internas": f"{consulta_actual.notas_internas}\n\nTRANSFERENCIA: {motivo_transferencia}",
                "fecha_actualizacion": datetime.now().isoformat()
            }
            
            # ✅ Ejecutar transferencia
            resultado = await self._ejecutar_actualizacion_consulta(
                consulta_id, datos_transferencia
            )
            
            if not resultado:
                raise ValueError("Error ejecutando transferencia en BD")
            
            # ✅ Crear modelo transferido
            consulta_transferida = ConsultaModel.from_dict(resultado)
            
            # ✅ Notificar a ambos odontólogos
            await self._notificar_transferencia_consulta(
                consulta_transferida, 
                consulta_actual.primer_odontologo_id,
                odontologo_destino_id,
                motivo_transferencia
            )
            
            logger.info(f"✅ Consulta {consulta_id} transferida a Dr. {odontologo_destino_id}")
            return consulta_transferida
            
        except Exception as e:
            logger.error(f"❌ Error transfiriendo consulta: {str(e)}")
            raise ValueError(f"No se pudo transferir la consulta: {str(e)}")
    
    # ==========================================
    # 📊 MÉTODOS DE CONSULTA DE COLAS
    # ==========================================
    
    async def obtener_cola_odontologo(self, odontologo_id: str) -> List[ConsultaModel]:
        """
        👨‍⚕️ OBTENER COLA DE UN ODONTÓLOGO ESPECÍFICO
        
        Args:
            odontologo_id: ID del odontólogo
            
        Returns:
            List[ConsultaModel]: Consultas ordenadas por llegada
        """
        try:
            logger.info(f"📋 Obteniendo cola del Dr. {odontologo_id}...")
            
            # ✅ Validar permisos
            self.require_permission("consultas", "leer")
            
            # ✅ Query optimizado para cola específica
            consultas_data = await self._query_cola_odontologo(odontologo_id)
            
            # ✅ Convertir a modelos tipados
            consultas_cola = []
            for item in consultas_data:
                try:
                    modelo = ConsultaModel.from_dict(item)
                    consultas_cola.append(modelo)
                except Exception as e:
                    logger.warning(f"Error procesando consulta en cola: {e}")
                    continue
            
            # ✅ Ordenar por posición en cola
            consultas_cola.sort(key=lambda c: c.orden_cola_odontologo or 0)
            
            logger.info(f"✅ Cola Dr. {odontologo_id}: {len(consultas_cola)} consultas")
            return consultas_cola
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo cola: {str(e)}")
            return []
    
    async def obtener_dashboard_colas_tiempo_real(self) -> Dict[str, Any]:
        """
        📊 DASHBOARD COMPLETO DE COLAS EN TIEMPO REAL
        
        Returns:
            Dict con métricas completas del sistema de colas
        """
        try:
            logger.info("📊 Generando dashboard de colas en tiempo real...")
            
            # ✅ Validar permisos
            self.require_permission("consultas", "leer")
            
            # ✅ Obtener odontólogos activos
            odontologos_activos = await self._obtener_odontologos_activos()
            
            # ✅ Construir dashboard por odontólogo
            dashboard = {
                "fecha": date.today().isoformat(),
                "timestamp": datetime.now().isoformat(),
                "total_odontologos": len(odontologos_activos),
                "colas_por_odontologo": {},
                "metricas_globales": {}
            }
            
            # ✅ Procesar cada odontólogo
            for odontologo in odontologos_activos:
                cola_doctor = await self.obtener_cola_odontologo(odontologo.id)
                
                # Calcular métricas de la cola
                en_espera = len([c for c in cola_doctor if c.estado == "en_espera"])
                en_atencion = len([c for c in cola_doctor if c.estado == "en_atencion"])
                
                # Tiempo promedio estimado
                tiempo_espera_promedio = await self._calcular_tiempo_espera_promedio(cola_doctor)
                
                dashboard["colas_por_odontologo"][odontologo.id] = {
                    "nombre": odontologo.nombre_completo_display,
                    "especialidad": odontologo.especialidad,
                    "total_consultas": len(cola_doctor),
                    "en_espera": en_espera,
                    "en_atencion": en_atencion,
                    "tiempo_espera_promedio": tiempo_espera_promedio,
                    "disponible": en_atencion == 0,
                    "consultas": [
                        {
                            "id": c.id,
                            "paciente": c.paciente_nombre,
                            "estado": c.estado,
                            "orden": c.orden_cola_odontologo,
                            "tiempo_espera": c.tiempo_espera_estimado,
                            "es_urgente": c.es_urgente
                        }
                        for c in cola_doctor[:5]  # Solo primeras 5 para el dashboard
                    ]
                }
            
            # ✅ Métricas globales
            todas_consultas = []
            for cola in dashboard["colas_por_odontologo"].values():
                todas_consultas.extend(cola["consultas"])
            
            dashboard["metricas_globales"] = {
                "total_consultas_hoy": len(todas_consultas),
                "total_en_espera": sum(cola["en_espera"] for cola in dashboard["colas_por_odontologo"].values()),
                "total_en_atencion": sum(cola["en_atencion"] for cola in dashboard["colas_por_odontologo"].values()),
                "odontologos_disponibles": len([cola for cola in dashboard["colas_por_odontologo"].values() if cola["disponible"]]),
                "tiempo_espera_global": sum(cola["tiempo_espera_promedio"] for cola in dashboard["colas_por_odontologo"].values()) / len(odontologos_activos) if odontologos_activos else 0
            }
            
            logger.info("✅ Dashboard de colas generado exitosamente")
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Error generando dashboard: {str(e)}")
            return {}
    
    # ==========================================
    # 🔧 MÉTODOS INTERNOS DE GESTIÓN DE COLAS  
    # ==========================================
    
    async def _calcular_siguiente_orden_general(self) -> int:
        """📊 Calcular siguiente orden de llegada general del día"""
        try:
            hoy = date.today()
            max_orden = await self._query_max_orden_llegada_dia(hoy)
            return (max_orden or 0) + 1
        except Exception as e:
            logger.warning(f"Error calculando orden general: {e}")
            return 1
    
    async def _calcular_siguiente_orden_cola_doctor(self, odontologo_id: str) -> int:
        """👨‍⚕️ Calcular siguiente posición en cola específica del doctor"""
        try:
            max_orden_cola = await self._query_max_orden_cola_doctor(odontologo_id)
            return (max_orden_cola or 0) + 1
        except Exception as e:
            logger.warning(f"Error calculando orden cola doctor: {e}")
            return 1
    
    async def _validar_transicion_estado(self, 
                                       consulta: ConsultaModel,
                                       estado_actual_esperado: str,
                                       estado_destino: str) -> None:
        """✅ Validar que la transición de estado es válida"""
        if consulta.estado != estado_actual_esperado:
            raise ValueError(
                f"Estado inválido para transición. "
                f"Esperado: {estado_actual_esperado}, "
                f"Actual: {consulta.estado}"
            )
        
        # Validaciones específicas del negocio v4.1
        transiciones_validas = {
            ("en_espera", "en_atencion"),
            ("en_atencion", "completada"),
            ("en_atencion", "entre_odontologos"),
            ("entre_odontologos", "en_atencion"),
            ("en_espera", "cancelada"),
            ("en_atencion", "cancelada")
        }
        
        if (estado_actual_esperado, estado_destino) not in transiciones_validas:
            raise ValueError(
                f"Transición no válida: {estado_actual_esperado} → {estado_destino}"
            )
    
    async def _validar_disponibilidad_odontologo(self, odontologo_id: str) -> None:
        """👨‍⚕️ Validar que el odontólogo está disponible"""
        consultas_en_atencion = await self._query_consultas_en_atencion_doctor(odontologo_id)
        
        if len(consultas_en_atencion) > 0:
            raise ValueError(
                f"Odontólogo ya tiene consulta en atención. "
                f"Debe completar la consulta actual primero."
            )
    
    async def _calcular_duracion_consulta(self, consulta: ConsultaModel) -> int:
        """⏱️ Calcular duración de la consulta en minutos"""
        try:
            if not consulta.fecha_inicio_atencion:
                return 0
            
            inicio = datetime.fromisoformat(consulta.fecha_inicio_atencion.replace('Z', '+00:00'))
            ahora = datetime.now()
            duracion = ahora - inicio
            
            return int(duracion.total_seconds() / 60)
        except Exception as e:
            logger.warning(f"Error calculando duración: {e}")
            return 0
    
    async def _calcular_tiempo_espera_promedio(self, cola: List[ConsultaModel]) -> float:
        """⏰ Calcular tiempo de espera promedio en la cola"""
        if not cola:
            return 0.0
        
        consultas_espera = [c for c in cola if c.estado == "en_espera"]
        if not consultas_espera:
            return 0.0
        
        tiempos = []
        for consulta in consultas_espera:
            try:
                if consulta.fecha_llegada:
                    llegada = datetime.fromisoformat(consulta.fecha_llegada.replace('Z', '+00:00'))
                    espera_minutos = (datetime.now() - llegada).total_seconds() / 60
                    tiempos.append(max(0, espera_minutos))
            except Exception as e:
                logger.warning(f"Error calculando tiempo espera individual: {e}")
                continue
        
        return sum(tiempos) / len(tiempos) if tiempos else 0.0
    
    # ==========================================
    # 🔔 MÉTODOS DE NOTIFICACIONES
    # ==========================================
    
    async def _notificar_nueva_consulta_en_cola(self, consulta: ConsultaModel) -> None:
        """🔔 Notificar nueva consulta en cola (implementación básica)"""
        logger.info(f"🔔 Nueva consulta en cola Dr. {consulta.primer_odontologo_id}: {consulta.paciente_nombre}")
        # TODO: Implementar notificaciones reales (WebSocket, push notifications, etc.)
    
    async def _notificar_inicio_atencion(self, consulta: ConsultaModel) -> None:
        """🏥 Notificar inicio de atención"""
        logger.info(f"🏥 Iniciada atención consulta {consulta.id}: {consulta.paciente_nombre}")
        # TODO: Implementar notificaciones específicas
    
    async def _notificar_transferencia_consulta(self, 
                                              consulta: ConsultaModel,
                                              odontologo_origen: str,
                                              odontologo_destino: str,
                                              motivo: str) -> None:
        """🔄 Notificar transferencia entre odontólogos"""
        logger.info(f"🔄 Transferencia: Dr. {odontologo_origen} → Dr. {odontologo_destino}: {motivo}")
        # TODO: Implementar notificaciones específicas
    
    # ==========================================
    # 🗄️ MÉTODOS DE QUERY OPTIMIZADOS
    # ==========================================
    
    async def _query_cola_odontologo(self, odontologo_id: str) -> List[Dict[str, Any]]:
        """🗄️ Query optimizado para cola específica"""
        # TODO: Implementar query real a BD
        # return self.consultas_table.get_cola_odontologo(odontologo_id)
        return []
    
    async def _query_max_orden_llegada_dia(self, fecha: date) -> Optional[int]:
        """🗄️ Query para máximo orden de llegada del día"""
        # TODO: Implementar query real a BD
        # return self.consultas_table.get_max_orden_llegada(fecha)
        return 0
    
    async def _query_max_orden_cola_doctor(self, odontologo_id: str) -> Optional[int]:
        """🗄️ Query para máximo orden en cola del doctor"""
        # TODO: Implementar query real a BD
        # return self.consultas_table.get_max_orden_cola_doctor(odontologo_id)
        return 0
    
    async def _obtener_consulta_por_id(self, consulta_id: str) -> Optional[ConsultaModel]:
        """🗄️ Obtener consulta por ID"""
        # TODO: Implementar query real a BD
        # data = self.consultas_table.get_by_id(consulta_id)
        # return ConsultaModel.from_dict(data) if data else None
        return None
    
    async def _obtener_odontologos_activos(self) -> List[PersonalModel]:
        """👨‍⚕️ Obtener lista de odontólogos activos"""
        # TODO: Implementar query real a BD
        # data = self.personal_table.get_odontologos_activos()
        # return [PersonalModel.from_dict(item) for item in data]
        return []
    
    async def _ejecutar_creacion_consulta(self, datos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """💾 Ejecutar creación de consulta en BD"""
        # TODO: Implementar insert real a BD
        # return self.consultas_table.create_with_queue_management(datos)
        return datos  # Placeholder
    
    async def _ejecutar_actualizacion_consulta(self, 
                                             consulta_id: str,
                                             datos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """📝 Ejecutar actualización de consulta en BD"""
        # TODO: Implementar update real a BD
        # return self.consultas_table.update_with_queue_validation(consulta_id, datos)
        return datos  # Placeholder
    
    # ==========================================
    # 📊 MÉTODOS DE MÉTRICAS Y ESTADÍSTICAS
    # ==========================================
    
    async def _actualizar_metricas_cola_tiempo_real(self, odontologo_id: str) -> None:
        """📊 Actualizar métricas de cola en tiempo real"""
        logger.info(f"📊 Actualizando métricas cola Dr. {odontologo_id}")
        # TODO: Implementar actualización de métricas
    
    async def _actualizar_estadisticas_productividad(self, 
                                                   consulta: ConsultaModel,
                                                   duracion_minutos: int) -> None:
        """📈 Actualizar estadísticas de productividad"""
        logger.info(f"📈 Actualizando stats productividad: {duracion_minutos}min")
        # TODO: Implementar actualización de estadísticas
    
    async def _liberar_odontologo_para_siguiente(self, odontologo_id: str) -> None:
        """🔄 Liberar odontólogo para siguiente consulta en cola"""
        logger.info(f"🔄 Liberando Dr. {odontologo_id} para siguiente consulta")
        # TODO: Implementar lógica de liberación automática


# ==========================================
# 🏭 INSTANCIA SINGLETON DEL SERVICIO
# ==========================================

consultas_service_v41 = ConsultasServiceV41()