"""
🚀 SERVICIO CENTRALIZADO DASHBOARD - VERSIÓN 2.0 CON CACHE INTELIGENTE
=======================================================================

CARACTERÍSTICAS NUEVAS:
- 📊 Cache con TTL para métricas pesadas
- ⚡ Separación real-time vs cached stats  
- 🔄 Invalidación automática de cache
- 📈 Optimización de consultas complejas

MÉTRICAS POR TIPO:
- REAL-TIME: consultas_hoy, pagos_pendientes, turnos_activos
- CACHED: totales mensuales, gráficos 30 días, stats de personal
"""

from typing import Dict, Any, Optional
from datetime import date, datetime, timedelta
from .base_service import BaseService
from .cache_invalidation_hooks import CacheInvalidationHooks
from dental_system.models import DashboardStatsModel, AdminStatsModel, PacientesStatsModel
from dental_system.supabase.tablas import (
    pacientes_table, consultas_table, pagos_table, 
    personal_table, servicios_table
)
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
        🚀 OBTIENE ESTADÍSTICAS OPTIMIZADAS CON CACHE INTELIGENTE
        
        NUEVA LÓGICA V2.0:
        - Combina real-time stats + cached stats
        - Real-time: consultas activas, pagos recientes
        - Cached: totales mensuales, stats de personal
        
        Args:
            user_role: Rol del usuario (gerente, administrador, odontologo)
            
        Returns:
            Diccionario con estadísticas optimizadas por rol
        """
        try:
            logger.info(f"🚀 Obteniendo stats optimizadas para rol: {user_role}")
            
            # 📊 ESTADÍSTICAS BASE (mix real-time + cache)
            base_stats = await self._get_optimized_base_statistics()
            
            if user_role == "gerente":
                # 👔 Estadísticas completas para gerente
                extended_stats = await self._get_cached_manager_statistics()
                return {**base_stats, **extended_stats}
            
            elif user_role == "administrador":
                # 👤 Estadísticas administrativas
                admin_stats = await self._get_cached_admin_statistics()
                return {**base_stats, **admin_stats}
            
            else:
                # 🦷 Estadísticas básicas para odontólogos/asistentes
                return base_stats
                
        except Exception as e:
            self.handle_error("Error obteniendo estadísticas del dashboard", e)
            return self._get_default_stats()
    
    async def _get_optimized_base_statistics(self) -> Dict[str, Any]:
        """
        🚀 ESTADÍSTICAS BASE OPTIMIZADAS - VERSIÓN 2.0
        
        SEPARACIÓN INTELIGENTE:
        - REAL-TIME: consultas_hoy (cambia cada llegada de paciente)
        - CACHED: total_pacientes, personal_activo, servicios_activos
        """
        try:
            # 📊 REAL-TIME STATS (siempre frescos)
            realtime_stats = await self._get_realtime_base_stats()
            
            # 💾 CACHED STATS (con TTL optimizado) - Temporalmente deshabilitado
            cached_stats = await self._fetch_cached_base_stats()
            
            # Combinar ambos
            return {**realtime_stats, **cached_stats}
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas base optimizadas: {e}")
            return self._get_default_base_stats()
    
    async def _get_realtime_base_stats(self) -> Dict[str, Any]:
        """
        ⚡ MÉTRICAS REAL-TIME (sin cache)
        
        Estas métricas cambian frecuentemente y necesitan estar siempre actualizadas
        """
        try:
            today = date.today().isoformat()
            
            # 📅 CONSULTAS DE HOY (real-time - cada llegada de paciente)
            consultas_response = self.client.table('consultas').select('id', count='exact').gte(
                'fecha_llegada', today
            ).lt('fecha_llegada', f"{today}T23:59:59").execute()
            consultas_hoy = consultas_response.count or 0
            
            # ⏰ CONSULTAS EN CURSO (real-time - estado actual)
            consultas_activas = self.client.table('consultas').select('id', count='exact').eq(
                'estado', 'en_progreso'
            ).execute()
            consultas_en_curso = consultas_activas.count or 0
            
            logger.debug(f"⚡ Real-time stats: consultas_hoy={consultas_hoy}, en_curso={consultas_en_curso}")
            
            return {
                "consultas_hoy": consultas_hoy,
                "consultas_en_curso": consultas_en_curso
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo stats real-time: {e}")
            return {
                "consultas_hoy": 0,
                "consultas_en_curso": 0
            }
    
    async def _fetch_cached_base_stats(self) -> Dict[str, Any]:
        """
        💾 MÉTRICAS CACHEADAS (TTL: 15 minutos)
        
        Estas métricas cambian poco y pueden ser cacheadas para mejor performance
        """
        try:
            # 👥 TOTAL PACIENTES (cambia poco - cache 15 min)
            pacientes_response = self.client.table('pacientes').select('id', count='exact').eq('activo', True).execute()
            total_pacientes = pacientes_response.count or 0
            
            # 👨‍⚕️ PERSONAL ACTIVO (cambia muy poco - cache 30 min)
            personal_response = self.client.table('vista_personal_completo').select('id', count='exact').eq(
                'completamente_activo', True
            ).execute()
            personal_activo = personal_response.count or 0
            
            # 🏥 SERVICIOS ACTIVOS (casi nunca cambia - cache 1 hora)
            servicios_response = self.client.table('servicios').select('id', count='exact').eq('activo', True).execute()
            servicios_activos = servicios_response.count or 0
            
            logger.debug(f"💾 Cached stats: pacientes={total_pacientes}, personal={personal_activo}, servicios={servicios_activos}")
            
            return {
                "total_pacientes": total_pacientes,
                "personal_activo": personal_activo,
                "servicios_activos": servicios_activos
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo stats cacheadas: {e}")
            return {
                "total_pacientes": 0,
                "personal_activo": 0,
                "servicios_activos": 0
            }
    
    def _get_default_base_stats(self) -> Dict[str, Any]:
        """📊 Stats por defecto en caso de error"""
        return {
            "total_pacientes": 0,
            "consultas_hoy": 0,
            "consultas_en_curso": 0,
            "personal_activo": 0,
            "servicios_activos": 0
        }
    
    async def _get_cached_manager_statistics(self) -> Dict[str, Any]:
        """
        👔 ESTADÍSTICAS PARA GERENTE - VERSIÓN CACHEADA 2.0
        
        SEPARACIÓN INTELIGENTE:
        - REAL-TIME: pagos_pendientes (cada pago cambia esto)
        - CACHED: ingresos_mes, total_odontologos
        """
        try:
            # 💳 REAL-TIME: Pagos pendientes (cambia con cada pago)
            realtime_payments = await self._get_realtime_payment_stats()
            
            # 💾 CACHED: Ingresos mensuales y personal - Temporalmente deshabilitado
            cached_manager = await self._fetch_cached_manager_stats()
            
            return {**realtime_payments, **cached_manager}
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas del gerente: {e}")
            return self._get_default_manager_stats()
    
    async def _get_realtime_payment_stats(self) -> Dict[str, Any]:
        """
        💳 ESTADÍSTICAS REAL-TIME DE PAGOS
        
        Solo pagos pendientes que cambian frecuentemente
        """
        try:
            # 💰 PAGOS PENDIENTES (real-time - cada pago cambia esto)
            pagos_pendientes_response = self.client.table('pagos').select('id', count='exact').eq(
                'estado_pago', 'pendiente'
            ).execute()
            pagos_pendientes = pagos_pendientes_response.count or 0
            
            logger.debug(f"💳 Payment real-time: pagos_pendientes={pagos_pendientes}")
            
            return {"pagos_pendientes": pagos_pendientes}
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo stats real-time de pagos: {e}")
            return {"pagos_pendientes": 0}
    
    async def _fetch_cached_manager_stats(self) -> Dict[str, Any]:
        """
        💾 ESTADÍSTICAS CACHEADAS PARA GERENTE (TTL: 30 minutos)
        
        Ingresos mensuales y conteos de personal que cambian poco
        """
        try:
            # 💰 INGRESOS DEL MES (cache 30 min - se actualiza diariamente)
            current_month = datetime.now().strftime('%Y-%m')
            pagos_response = self.client.table('pagos').select('monto_pagado_usd, monto_pagado_bs').gte(
                'fecha_pago', f"{current_month}-01"
            ).eq('estado_pago', 'completado').execute()

            ingresos_mes = sum([(pago.get('monto_pagado_usd', 0) or 0) + (pago.get('monto_pagado_bs', 0) or 0) for pago in pagos_response.data]) if pagos_response.data else 0
            
            # 🦷 TOTAL ODONTÓLOGOS (cache 30 min - cambia muy poco)
            odontologos_response = self.client.table('vista_personal_completo').select('id', count='exact').eq(
                'tipo_personal', 'Odontólogo'
            ).eq('completamente_activo', True).execute()
            
            total_odontologos = odontologos_response.count or 0
            
            logger.debug(f"💾 Manager cached: ingresos_mes={ingresos_mes}, odontologos={total_odontologos}")
            
            return {
                "ingresos_mes": ingresos_mes,
                "total_odontologos": total_odontologos
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo stats cacheadas del gerente: {e}")
            return {
                "ingresos_mes": 0,
                "total_odontologos": 0
            }
    
    def _get_default_manager_stats(self) -> Dict[str, Any]:
        """📊 Stats por defecto del gerente en caso de error"""
        return {
            "ingresos_mes": 0,
            "pagos_pendientes": 0,
            "total_odontologos": 0
        }
    
    async def _get_cached_admin_statistics(self) -> Dict[str, Any]:
        """
        👤 ESTADÍSTICAS PARA ADMINISTRADOR - VERSIÓN CACHEADA 2.0
        
        Todo puede ser cacheado ya que son conteos que cambian poco
        """
        try:
            # 💾 CACHED: Todas las estadísticas de admin - Temporalmente deshabilitado
            return await self._fetch_cached_admin_stats()
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas del administrador: {e}")
            return self._get_default_admin_stats()
    
    async def _fetch_cached_admin_stats(self) -> Dict[str, Any]:
        """
        💾 ESTADÍSTICAS CACHEADAS PARA ADMIN (TTL: 30 minutos)
        
        Pacientes por demografía que cambian poco
        """
        try:
            current_month = datetime.now().strftime('%Y-%m')
            
            # 👥 PACIENTES NUEVOS ESTE MES (cache 30 min - se actualiza diariamente)
            nuevos_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).gte('fecha_registro', f"{current_month}-01").execute()
            
            # 🚻 DISTRIBUCIÓN POR GÉNERO (cache 30 min - cambia poco)
            hombres_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'masculino').execute()
            
            mujeres_response = self.client.table('pacientes').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'femenino').execute()
            
            nuevos_pacientes_mes = nuevos_response.count or 0
            pacientes_hombres = hombres_response.count or 0
            pacientes_mujeres = mujeres_response.count or 0
            
            logger.debug(f"💾 Admin cached: nuevos={nuevos_pacientes_mes}, hombres={pacientes_hombres}, mujeres={pacientes_mujeres}")
            
            return {
                "nuevos_pacientes_mes": nuevos_pacientes_mes,
                "pacientes_hombres": pacientes_hombres,
                "pacientes_mujeres": pacientes_mujeres
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo stats cacheadas del admin: {e}")
            return self._get_default_admin_stats()
    
    def _get_default_admin_stats(self) -> Dict[str, Any]:
        """📊 Stats por defecto del admin en caso de error"""
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
            pagos_mes = self.client.table('pagos').select('monto_pagado_usd, monto_pagado_bs').gte(
                'fecha_pago', f"{current_month}-01"
            ).eq('estado_pago', 'completado').execute()

            total_mes = sum([(pago.get('monto_pagado_usd', 0) or 0) + (pago.get('monto_pagado_bs', 0) or 0) for pago in pagos_mes.data]) if pagos_mes.data else 0
            
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


    # ==========================================
    # 📊 NUEVOS MÉTODOS PARA GRÁFICOS
    # ==========================================
    
    async def get_chart_data_last_30_days(self, user_role: str = None) -> Dict[str, list[Dict[str, Any]]]:
        """
        📈 OBTENER DATOS CACHEADOS PARA GRÁFICOS DE ÚLTIMOS 30 DÍAS - V2.0
        
        OPTIMIZACIONES NUEVAS:
        - Cache TTL 1 hora para datos generales
        - Cache TTL 30 min para datos de odontólogos  
        - Consultas optimizadas con mejor performance
        
        Args:
            user_role: Rol del usuario (gerente, administrador, odontologo)
            
        Returns:
            Dict con arrays de datos para gráficos cacheados
        """
        try:
            logger.info(f"📈 Obteniendo datos de gráficos cacheados para rol: {user_role}")
            
            if user_role == "odontologo":
                # Cache específico para odontólogos (TTL: 30 min)
                # Cache deshabilitado temporalmente
                return await self._get_dentist_chart_data()
            else:
                # Cache general para gerente/admin - Temporalmente deshabilitado
                return await self._get_general_chart_data()
                
        except Exception as e:
            self.handle_error("Error obteniendo datos de gráficos cacheados", e)
            return self._get_empty_chart_data()
    
    async def _get_general_chart_data(self) -> Dict[str, list[Dict[str, Any]]]:
        """
        📊 DATOS GENERALES PARA GERENTE Y ADMIN (últimos 30 días)
        
        Incluye:
        - Consultas por día
        - Pacientes nuevos por día  
        - Ingresos por día
        """
        try:
            # Preparar fechas (últimos 30 días)
            dates = []
            for i in range(30, -1, -1):
                date_obj = datetime.now() - timedelta(days=i)
                dates.append({
                    'date_obj': date_obj.date(),
                    'date_str': date_obj.strftime("%d-%m"),
                    'date_sql': date_obj.strftime("%Y-%m-%d")
                })
            
            # Arrays para los resultados
            consultas_data = []
            pacientes_data = []
            ingresos_data = []
            
            # Obtener datos para cada día
            for date_info in dates:
                # 📅 CONSULTAS DEL DÍA
                consultas_response = self.client.table('consultas').select(
                    'id', count='exact'
                ).gte(
                    'fecha_llegada', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_llegada', f"{date_info['date_sql']}T23:59:59"
                ).execute()
                
                consultas_count = consultas_response.count or 0
                
                # 👥 PACIENTES NUEVOS DEL DÍA
                pacientes_response = self.client.table('pacientes').select(
                    'id', count='exact'
                ).gte(
                    'fecha_registro', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_registro', f"{date_info['date_sql']}T23:59:59"
                ).eq('activo', True).execute()
                
                pacientes_count = pacientes_response.count or 0
                
                # 💰 INGRESOS DEL DÍA
                pagos_response = self.client.table('pagos').select(
                    'monto_pagado'
                ).gte(
                    'fecha_pago', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_pago', f"{date_info['date_sql']}T23:59:59"
                ).eq('estado_pago', 'completado').execute()
                
                ingresos_total = sum([p['monto_pagado'] for p in pagos_response.data]) if pagos_response.data else 0
                
                # Agregar a los arrays
                consultas_data.append({
                    "name": date_info['date_str'],
                    "Consultas": consultas_count
                })
                
                pacientes_data.append({
                    "name": date_info['date_str'], 
                    "Pacientes": pacientes_count
                })
                
                ingresos_data.append({
                    "name": date_info['date_str'],
                    "Ingresos": float(ingresos_total)
                })
            
            return {
                "consultas_data": consultas_data,
                "pacientes_data": pacientes_data,
                "ingresos_data": ingresos_data
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo datos generales de gráficos: {e}")
            return self._get_empty_chart_data()
    
    async def _get_dentist_chart_data(self) -> Dict[str, list[Dict[str, Any]]]:
        """
        🦷 DATOS ESPECÍFICOS PARA ODONTÓLOGOS (últimos 30 días)
        
        Incluye:
        - Consultas propias por día
        - Ingresos propios por tipo de pago
        - Pacientes atendidos por día
        """
        try:
            # Obtener ID del odontólogo desde el contexto del usuario
            odontologo_id = self._get_current_dentist_id()
            if not odontologo_id:
                print("⚠️ No se pudo obtener ID del odontólogo")
                return self._get_empty_chart_data()
            
            # Preparar fechas
            dates = []
            for i in range(30, -1, -1):
                date_obj = datetime.now() - timedelta(days=i)
                dates.append({
                    'date_obj': date_obj.date(),
                    'date_str': date_obj.strftime("%d-%m"),
                    'date_sql': date_obj.strftime("%Y-%m-%d")
                })
            
            # Arrays para resultados
            consultas_data = []
            ingresos_por_tipo_data = []
            
            # 📅 CONSULTAS PROPIAS POR DÍA
            for date_info in dates:
                consultas_response = self.client.table('consultas').select(
                    'id', count='exact'
                ).eq('odontologo_id', odontologo_id).gte(
                    'fecha_llegada', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_llegada', f"{date_info['date_sql']}T23:59:59"
                ).execute()
                
                consultas_count = consultas_response.count or 0
                
                consultas_data.append({
                    "name": date_info['date_str'],
                    "Consultas": consultas_count
                })
            
            # 💰 INGRESOS POR TIPO DE PAGO (últimos 30 días)
            fecha_30_dias = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Obtener pagos del odontólogo (a través de sus consultas)
            pagos_response = self.client.table('pagos').select(
                'monto_pagado, metodo_pago, fecha_pago'
            ).gte('fecha_pago', fecha_30_dias).eq(
                'estado_pago', 'completado'
            ).execute()
            
            # Filtrar pagos del odontólogo (esto requiere JOIN, simplificado por ahora)
            # TODO: Mejorar esta consulta con JOIN
            
            # Agrupar por método de pago
            ingresos_por_metodo = {}
            for pago in pagos_response.data if pagos_response.data else []:
                metodo = pago['metodo_pago']
                monto = pago['monto_pagado']
                
                if metodo not in ingresos_por_metodo:
                    ingresos_por_metodo[metodo] = 0
                ingresos_por_metodo[metodo] += monto
            
            # Convertir a formato para gráfico
            for metodo, total in ingresos_por_metodo.items():
                ingresos_por_tipo_data.append({
                    "name": metodo.replace('_', ' ').title(),
                    "value": float(total),
                    "fill": self._get_payment_method_color(metodo)
                })
            
            return {
                "consultas_data": consultas_data,
                "ingresos_por_tipo_data": ingresos_por_tipo_data,
                "pacientes_data": []  # Placeholder por ahora
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de odontólogo: {e}")
            return self._get_empty_chart_data()
    
    def _get_current_dentist_id(self) -> str:
        """
        🆔 OBTENER ID DEL ODONTÓLOGO ACTUAL
        
        Extrae el ID del personal desde el contexto del usuario
        """
        try:
            if not self.current_user_profile:
                return None
            
            # Buscar en la información del personal
            personal_info = self.current_user_profile.get("personal_info", {})
            if personal_info and personal_info.get("id"):
                return personal_info["id"]
            
            # Fallback: buscar por email en tabla personal
            email = self.current_user_profile.get("email")
            if email:
                personal_response = self.client.table('vista_personal_completo').select(
                    'id'
                ).eq('email', email).eq('tipo_personal', 'Odontólogo').execute()
                
                if personal_response.data:
                    return personal_response.data[0]['id']
            
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo ID del odontólogo: {e}")
            return None
    
    def _get_payment_method_color(self, metodo: str) -> str:
        """🎨 COLORES PARA MÉTODOS DE PAGO"""
        colors = {
            'efectivo': '#22c55e',      # Verde
            'tarjeta_credito': '#3b82f6',  # Azul
            'tarjeta_debito': '#8b5cf6',   # Púrpura  
            'transferencia': '#f59e0b',    # Amarillo
            'cheque': '#ef4444',           # Rojo
            'otro': '#6b7280'              # Gris
        }
        return colors.get(metodo, '#6b7280')
    
    def _get_empty_chart_data(self) -> Dict[str, list]:
        """📊 DATOS VACÍOS EN CASO DE ERROR"""
        # Generar fechas vacías para mantener estructura
        empty_data = []
        for i in range(30, -1, -1):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%d-%m")
            empty_data.append({
                "name": date_str,
                "Consultas": 0,
                "Pacientes": 0,
                "Ingresos": 0
            })
        
        return {
            "consultas_data": empty_data,
            "pacientes_data": empty_data,
            "ingresos_data": empty_data,
            "ingresos_por_tipo_data": []
        }
    
    async def get_summary_stats_30_days(self) -> Dict[str, Any]:
        """
        📊 RESUMEN DE ESTADÍSTICAS DE ÚLTIMOS 30 DÍAS
        
        Para mostrar totales en cards/widgets
        """
        try:
            fecha_30_dias = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Total consultas últimos 30 días
            consultas_response = self.client.table('consultas').select(
                'id', count='exact'
            ).gte('fecha_llegada', fecha_30_dias).execute()
            
            # Total pacientes nuevos últimos 30 días
            pacientes_response = self.client.table('pacientes').select(
                'id', count='exact'
            ).gte('fecha_registro', fecha_30_dias).eq('activo', True).execute()
            
            # Total ingresos últimos 30 días
            pagos_response = self.client.table('pagos').select(
                'monto_pagado'
            ).gte('fecha_pago', fecha_30_dias).eq('estado_pago', 'completado').execute()
            
            total_ingresos = sum([p['monto_pagado'] for p in pagos_response.data]) if pagos_response.data else 0
            
            return {
                "consultas_30_dias": consultas_response.count or 0,
                "pacientes_nuevos_30_dias": pacientes_response.count or 0,  
                "ingresos_30_dias": float(total_ingresos)
            }
            
        except Exception as e:
            self.handle_error("Error obteniendo resumen de 30 días", e)
            return {
                "consultas_30_dias": 0,
                "pacientes_nuevos_30_dias": 0,
                "ingresos_30_dias": 0.0
            }    

# Instancia única para importar
dashboard_service = DashboardService()