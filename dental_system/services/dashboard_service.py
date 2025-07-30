"""
Servicio centralizado para estadísticas del dashboard
Elimina duplicación entre boss_state y admin_state
"""

from typing import Dict, Any, Optional
from datetime import date, datetime
from .base_service import BaseService
from dental_system.models import DashboardStatsModel, AdminStatsModel, PacientesStatsModel
from ..supabase.tablas import pacientes_table
import logging

logger = logging.getLogger(__name__)

class DashboardService(BaseService):
    """
    Servicio que maneja todas las estadísticas del dashboard
    Usado tanto por Boss como Admin
    """
    
    def __init__(self):
        super().__init__()
    
    async def get_dashboard_stats(self, user_role: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas del dashboard según el rol del usuario
        
        Args:
            user_role: Rol del usuario (gerente, administrador)
            
        Returns:
            Diccionario con estadísticas apropiadas para el rol
        """
        try:
            logger.info(f"Obteniendo estadísticas del dashboard para rol: {user_role}")
            
            # Estadísticas base (común para todos)
            base_stats = await self._get_base_statistics()
            
            if user_role == "gerente":
                # Estadísticas completas para el jefe
                extended_stats = await self._get_manager_statistics()
                return {**base_stats, **extended_stats}
            
            elif user_role == "administrador":
                # Estadísticas específicas para admin
                admin_stats = await self._get_admin_statistics()
                return {**base_stats, **admin_stats}
            
            else:
                # Estadísticas básicas para otros roles
                return base_stats
                
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas del dashboard", e)
            return self._get_default_stats()
    
    async def _get_base_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas base comunes a todos los roles"""
        try:
            # Total pacientes activos
            pacientes_response = self.client.table('pacientes').select('id', count='exact').eq('activo', True).execute()
            total_pacientes = pacientes_response.count or 0
            
            # Consultas de hoy
            today = date.today().isoformat()
            consultas_response = self.client.table('consultas').select('id', count='exact').gte(
                'fecha_programada', today
            ).lt('fecha_programada', f"{today}T23:59:59").execute()
            consultas_hoy = consultas_response.count or 0
            
            # Personal activo
            personal_response = self.client.table('vista_personal_completo').select('id', count='exact').eq(
                'completamente_activo', True
            ).execute()
            personal_activo = personal_response.count or 0
            
            # Servicios activos
            servicios_response = self.client.table('servicios').select('id', count='exact').eq('activo', True).execute()
            servicios_activos = servicios_response.count or 0
            
            return {
                "total_pacientes": total_pacientes,
                "consultas_hoy": consultas_hoy,
                "personal_activo": personal_activo,
                "servicios_activos": servicios_activos
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas base: {e}")
            return {
                "total_pacientes": 0,
                "consultas_hoy": 0,
                "personal_activo": 0,
                "servicios_activos": 0
            }
    
    async def _get_manager_statistics(self) -> Dict[str, Any]:
        """Estadísticas adicionales para el gerente"""
        try:
            # Ingresos del mes
            current_month = datetime.now().strftime('%Y-%m')
            pagos_response = self.client.table('pagos').select('monto_pagado').gte(
                'fecha_pago', f"{current_month}-01"
            ).eq('estado_pago', 'completado').execute()
            
            ingresos_mes = sum([pago['monto_pagado'] for pago in pagos_response.data]) if pagos_response.data else 0
            
            # Pagos pendientes
            pagos_pendientes_response = self.client.table('pagos').select('id', count='exact').eq(
                'estado_pago', 'pendiente'
            ).execute()
            pagos_pendientes = pagos_pendientes_response.count or 0
            
            # Estadísticas de personal por tipo
            odontologos_response = self.client.table('vista_personal_completo').select('id', count='exact').eq(
                'tipo_personal', 'Odontólogo'
            ).eq('completamente_activo', True).execute()
            
            return {
                "ingresos_mes": ingresos_mes,
                "pagos_pendientes": pagos_pendientes,
                "total_odontologos": odontologos_response.count or 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas del gerente: {e}")
            return {
                "ingresos_mes": 0,
                "pagos_pendientes": 0,
                "total_odontologos": 0
            }
    
    async def _get_admin_statistics(self) -> Dict[str, Any]:
        """Estadísticas específicas para el administrador"""
        try:
            # Pacientes nuevos este mes
            current_month = datetime.now().strftime('%Y-%m')
            nuevos_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).gte('fecha_registro', f"{current_month}-01").execute()
            
            # Distribución por género
            hombres_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'masculino').execute()
            
            mujeres_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'femenino').execute()
            
            return {
                "nuevos_pacientes_mes": nuevos_response.count or 0,
                "pacientes_hombres": hombres_response.count or 0,
                "pacientes_mujeres": mujeres_response.count or 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas del admin: {e}")
            return {
                "nuevos_pacientes_mes": 0,
                "pacientes_hombres": 0,
                "pacientes_mujeres": 0
            }
    
    async def get_pacientes_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas específicas de pacientes
        Usado tanto por Boss como Admin
        """
        try:
            logger.info("Obteniendo estadísticas de pacientes")
            
            # Total y activos
            total_response = self.client.table('pacientes').select('id', count='exact').eq('activo', True).execute()
            total = total_response.count or 0
            
            # Nuevos este mes
            current_month = datetime.now().strftime('%Y-%m')
            nuevos_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).gte('fecha_registro', f"{current_month}-01").execute()
            
            # Por género
            hombres_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'masculino').execute()
            
            mujeres_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'femenino').execute()
            
            return {
                "total": total,
                "nuevos_mes": nuevos_response.count or 0,
                "activos": total,
                "hombres": hombres_response.count or 0,
                "mujeres": mujeres_response.count or 0
            }
            
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de pacientes", e)
            return {
                "total": 0,
                "nuevos_mes": 0,
                "activos": 0,
                "hombres": 0,
                "mujeres": 0
            }
    

    async def _load_pacientes_stats(self):
        """Cargar estadísticas de pacientes"""
        try:
            stats = pacientes_table.get_patient_stats()
            
            self.pacientes_stats = PacientesStatsModel(
                total=stats.get("total", 0),
                nuevos_mes=stats.get("nuevos_mes", 0),
                activos=stats.get("activos", 0),
                hombres=stats.get("hombres", 0),
                mujeres=stats.get("mujeres", 0),
                # Estadísticas adicionales (placeholder por ahora)
                edad_promedio=0.0,
                pacientes_con_email=0,
                pacientes_con_telefono=0,
                registros_ultima_semana=0
            )
            
            print(f"[DEBUG] Estadísticas de pacientes tipadas: {stats}")
        except Exception as e:
            print(f"[ERROR] Error cargando estadísticas de pacientes: {e}")
            self.pacientes_stats = PacientesStatsModel()


    async def get_pagos_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de pagos
        """
        try:
            logger.info("Obteniendo estadísticas de pagos")
            
            # Ingresos del mes
            current_month = datetime.now().strftime('%Y-%m')
            pagos_mes = self.client.table('pagos').select('monto_pagado').gte(
                'fecha_pago', f"{current_month}-01"
            ).eq('estado_pago', 'completado').execute()
            
            total_mes = sum([pago['monto_pagado'] for pago in pagos_mes.data]) if pagos_mes.data else 0
            
            # Pendientes
            pendientes = self.client.table('pagos').select('monto_total', 'monto_pagado').eq(
                'estado_pago', 'pendiente'
            ).execute()
            
            total_pendientes = sum([
                pago['monto_total'] - pago['monto_pagado'] 
                for pago in pendientes.data
            ]) if pendientes.data else 0
            
            return {
                "total_mes": total_mes,
                "pendientes": total_pendientes,
                "completados": total_mes
            }
            
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas de pagos", e)
            return {
                "total_mes": 0,
                "pendientes": 0,
                "completados": 0
            }
    
    def _get_default_stats(self) -> Dict[str, Any]:
        """Estadísticas por defecto en caso de error"""
        return {
            "total_pacientes": 0,
            "consultas_hoy": 0,
            "personal_activo": 0,
            "servicios_activos": 0,
            "ingresos_mes": 0,
            "pagos_pendientes": 0,
            "nuevos_pacientes_mes": 0,
            "pacientes_hombres": 0,
            "pacientes_mujeres": 0,
            "total_odontologos": 0
        }
    
    async def get_real_time_updates(self) -> Dict[str, Any]:
        """
        Obtiene actualizaciones en tiempo real para el dashboard
        (Para futuras implementaciones con websockets)
        """
        try:
            # Por ahora, obtener estadísticas básicas actualizadas
            base_stats = await self._get_base_statistics()
            
            # Agregar timestamp de actualización
            base_stats["last_updated"] = datetime.now().isoformat()
            
            return base_stats
            
        except Exception as e:
            self.handle_error("Error obteniendo actualizaciones en tiempo real", e)
            return {"last_updated": datetime.now().isoformat()}


# Instancia única para importar
dashboard_service = DashboardService()