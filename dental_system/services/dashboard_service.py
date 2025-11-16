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

from typing import Dict, Any, Optional, List
from datetime import date, datetime, timedelta
from .base_service import BaseService
from dental_system.models import DashboardStatsModel, AdminStatsModel, PacientesStatsModel
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
            # base_stats = await self._get_optimized_base_statistics()
            
            if user_role == "gerente":
                base_stats = await self.get_gerente_stats_simple()

            return base_stats
            
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
            pagos_response = self.client.table('pago').select('monto_pagado_usd, monto_pagado_bs').gte(
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
            nuevos_response = self.client.table('paciente').select('id', count='exact').eq(
                'activo', True
            ).gte('fecha_registro', f"{current_month}-01").execute()
            
            # 🚻 DISTRIBUCIÓN POR GÉNERO (cache 30 min - cambia poco)
            hombres_response = self.client.table('paciente').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'masculino').execute()
            
            mujeres_response = self.client.table('paciente').select('id', count='exact').eq(
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
            total_response = self.client.table('paciente').select('id', count='exact').eq('activo', True).execute()
            total = total_response.count or 0
            
            # Nuevos este mes
            current_month = datetime.now().strftime('%Y-%m')
            nuevos_response = self.client.table('paciente').select('id', count='exact').eq(
                'activo', True
            ).gte('fecha_registro', f"{current_month}-01").execute()
            
            # Por género
            hombres_response = self.client.table('paciente').select('id', count='exact').eq(
                'activo', True
            ).eq('genero', 'masculino').execute()
            
            mujeres_response = self.client.table('paciente').select('id', count='exact').eq(
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
            # Importar pacientes_service para evitar circular imports
            from .pacientes_service import pacientes_service

            # Usar el servicio de pacientes que ya tiene queries directas
            stats = await pacientes_service.get_patient_stats()

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

            logger.info(f"✅ Estadísticas de pacientes cargadas: {stats}")
        except Exception as e:
            logger.error(f"❌ Error cargando estadísticas de pacientes: {e}")
            self.pacientes_stats = PacientesStatsModel()


    async def get_pagos_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de pagos
        """
        try:
            logger.info("Obteniendo estadísticas de pagos")
            
            # Ingresos del mes
            current_month = datetime.now().strftime('%Y-%m')
            pagos_mes = self.client.table('pago').select('monto_pagado_usd, monto_pagado_bs').gte(
                'fecha_pago', f"{current_month}-01"
            ).eq('estado_pago', 'completado').execute()

            total_mes = sum([(pago.get('monto_pagado_usd', 0) or 0) + (pago.get('monto_pagado_bs', 0) or 0) for pago in pagos_mes.data]) if pagos_mes.data else 0
            
            # Pendientes (saldos pendientes en USD + BS)
            pendientes = self.client.table('pago').select(
                'saldo_pendiente_usd, saldo_pendiente_bs'
            ).eq('estado_pago', 'pendiente').execute()

            total_pendientes = sum([
                (p.get('saldo_pendiente_usd', 0) or 0) + (p.get('saldo_pendiente_bs', 0) or 0)
                for p in pendientes.data
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
                consultas_response = self.client.table('consulta').select(
                    'id', count='exact'
                ).gte(
                    'fecha_llegada', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_llegada', f"{date_info['date_sql']}T23:59:59"
                ).execute()
                
                consultas_count = consultas_response.count or 0
                
                # 👥 PACIENTES NUEVOS DEL DÍA
                pacientes_response = self.client.table('paciente').select(
                    'id', count='exact'
                ).gte(
                    'fecha_registro', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_registro', f"{date_info['date_sql']}T23:59:59"
                ).eq('activo', True).execute()
                
                pacientes_count = pacientes_response.count or 0
                
                # 💰 INGRESOS DEL DÍA (USD + BS)
                pagos_response = self.client.table('pago').select(
                    'monto_pagado_usd, monto_pagado_bs'
                ).gte(
                    'fecha_pago', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_pago', f"{date_info['date_sql']}T23:59:59"
                ).eq('estado_pago', 'completado').execute()

                ingresos_total = sum([
                    (p.get('monto_pagado_usd', 0) or 0) + (p.get('monto_pagado_bs', 0) or 0)
                    for p in pagos_response.data
                ]) if pagos_response.data else 0
                
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
                consultas_response = self.client.table('consulta').select(
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
            pagos_response = self.client.table('pago').select(
                'monto_pagado_usd, monto_pagado_bs, metodos_pago, fecha_pago'
            ).gte('fecha_pago', fecha_30_dias).eq(
                'estado_pago', 'completado'
            ).execute()

            # Filtrar pagos del odontólogo (esto requiere JOIN, simplificado por ahora)
            # TODO: Mejorar esta consulta con JOIN

            # Agrupar por método de pago (nota: metodos_pago es JSONB array)
            ingresos_por_metodo = {}
            for pago in pagos_response.data if pagos_response.data else []:
                # metodos_pago es un array JSONB, por ahora simplificamos
                metodo = "mixto"  # Por ahora agrupar todo como mixto
                monto = (pago.get('monto_pagado_usd', 0) or 0) + (pago.get('monto_pagado_bs', 0) or 0)

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
            consultas_response = self.client.table('consulta').select(
                'id', count='exact'
            ).gte('fecha_llegada', fecha_30_dias).execute()
            
            # Total pacientes nuevos últimos 30 días
            pacientes_response = self.client.table('paciente').select(
                'id', count='exact'
            ).gte('fecha_registro', fecha_30_dias).eq('activo', True).execute()
            
            # Total ingresos últimos 30 días
            pagos_response = self.client.table('pago').select(
                'monto_total_usd'
            ).gte('fecha_pago', fecha_30_dias).eq('estado_pago', 'completado').execute()
            
            total_ingresos = sum([p['monto_total_usd'] for p in pagos_response.data]) if pagos_response.data else 0
            
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

    async def get_gerente_stats_simple(self) -> Dict[str, Any]:
                """
                📊 ESTADÍSTICAS SIMPLIFICADAS PARA GERENTE

                Stats para los 5 cards principales:
                1. Ingresos del Mes
                2. Ingresos Hoy (USD + BS)
                3. Consultas Hoy
                4. Servicios Aplicados Hoy
                5. Tiempo Promedio Atención
                """
                try:
                    logger.info("📊 Obteniendo stats simplificadas para gerente")

                    today = date.today().isoformat()
                    current_month = datetime.now().strftime('%Y-%m')

                    # 1️⃣ INGRESOS DEL MES
                    pagos_mes = self.client.table('pago').select(
                        'monto_pagado_usd, monto_pagado_bs'
                    ).gte(
                        'fecha_pago', f"{current_month}-01"
                    ).eq('estado_pago', 'completado').execute()

                    ingresos_mes_total = sum([
                        (p.get('monto_pagado_usd', 0) or 0) + (p.get('monto_pagado_bs', 0) or 0)
                        for p in (pagos_mes.data or [])
                    ])

                    # 2️⃣ INGRESOS HOY (USD + BS desglosado)
                    pagos_hoy = self.client.table('pago').select(
                        'monto_pagado_usd, monto_pagado_bs, tasa_cambio_bs_usd'
                    ).gte(
                        'fecha_pago', f"{today}T00:00:00"
                    ).lt(
                        'fecha_pago', f"{today}T23:59:59"
                    ).eq('estado_pago', 'completado').execute()

                    ingresos_hoy_usd = 0
                    ingresos_hoy_bs = 0
                    for pago in (pagos_hoy.data or []):
                        ingresos_hoy_usd += pago.get('monto_pagado_usd', 0) or 0
                        ingresos_hoy_bs += pago.get('monto_pagado_bs', 0) or 0

                    ingresos_hoy_total = ingresos_hoy_usd + ingresos_hoy_bs

                    # 3️⃣ CONSULTAS HOY (totales y por estado)
                    consultas_hoy_total_resp = self.client.table('consulta').select(
                        'id', count='exact'
                    ).gte(
                        'fecha_llegada', f"{today}T00:00:00"
                    ).lt(
                        'fecha_llegada', f"{today}T23:59:59"
                    ).execute()

                    consultas_hoy_total = consultas_hoy_total_resp.count or 0

                    completadas_resp = self.client.table('consulta').select(
                        'id', count='exact'
                    ).gte(
                        'fecha_llegada', f"{today}T00:00:00"
                    ).lt(
                        'fecha_llegada', f"{today}T23:59:59"
                    ).eq('estado', 'completada').execute()

                    en_espera_resp = self.client.table('consulta').select(
                        'id', count='exact'
                    ).gte(
                        'fecha_llegada', f"{today}T00:00:00"
                    ).lt(
                        'fecha_llegada', f"{today}T23:59:59"
                    ).eq('estado', 'en_espera').execute()

                    consultas_completadas = completadas_resp.count or 0
                    consultas_en_espera = en_espera_resp.count or 0

                    # 4️⃣ SERVICIOS APLICADOS HOY
                    servicios_hoy_response = self.client.table('historia_medica').select(
                        'id', count='exact'
                    ).gte(
                        'fecha_registro', f"{today}T00:00:00"
                    ).lt(
                        'fecha_registro', f"{today}T23:59:59"
                    ).execute()

                    servicios_aplicados = servicios_hoy_response.count or 0
                    promedio_servicios = (servicios_aplicados / consultas_hoy_total) if consultas_hoy_total > 0 else 0

                    # 5️⃣ TIEMPO PROMEDIO ATENCIÓN (fecha_creacion → fecha_actualizacion cuando completada)
                    consultas_completadas_hoy = self.client.table('consulta').select(
                        'fecha_creacion, fecha_actualizacion'
                    ).eq('estado', 'completada').gte(
                        'fecha_actualizacion', f"{today}T00:00:00"
                    ).lt(
                        'fecha_actualizacion', f"{today}T23:59:59"
                    ).execute()

                    tiempos = []
                    for consulta in (consultas_completadas_hoy.data or []):
                        if consulta.get('fecha_creacion') and consulta.get('fecha_actualizacion'):
                            try:
                                inicio = datetime.fromisoformat(consulta['fecha_creacion'].replace('Z', '+00:00'))
                                fin = datetime.fromisoformat(consulta['fecha_actualizacion'].replace('Z', '+00:00'))
                                diferencia_minutos = (fin - inicio).total_seconds() / 60
                                if diferencia_minutos > 0:
                                    tiempos.append(diferencia_minutos)
                            except Exception:
                                continue

                    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0

                    logger.info(f"✅ Stats gerente: Ingresos mes=${ingresos_mes_total:.2f}, Hoy=${ingresos_hoy_total:.2f}, Consultas={consultas_hoy_total}")

                    return {
                        # Card 1: Ingresos del Mes
                        "ingresos_mes": round(ingresos_mes_total, 2),

                        # Card 2: Ingresos Hoy (con desglose)
                        "ingresos_hoy_total": round(ingresos_hoy_total, 2),
                        "ingresos_hoy_usd": round(ingresos_hoy_usd, 2),
                        "ingresos_hoy_bs": round(ingresos_hoy_bs, 2),

                        # Card 3: Consultas Hoy
                        "consultas_hoy_total": consultas_hoy_total,
                        "consultas_completadas": consultas_completadas,
                        "consultas_en_espera": consultas_en_espera,

                        # Card 4: Servicios Aplicados Hoy
                        "servicios_aplicados": servicios_aplicados,
                        "promedio_servicios_consulta": round(promedio_servicios, 1),

                        # Card 5: Tiempo Promedio Atención
                        "tiempo_promedio_minutos": round(tiempo_promedio, 0),
                    }

                except Exception as e:
                    logger.error(f"❌ Error obteniendo stats del gerente: {e}")
                    return {
                        "ingresos_mes": 0,
                        "ingresos_hoy_total": 0,
                        "ingresos_hoy_usd": 0,
                        "ingresos_hoy_bs": 0,
                        "consultas_hoy_total": 0,
                        "consultas_completadas": 0,
                        "consultas_en_espera": 0,
                        "servicios_aplicados": 0,
                        "promedio_servicios_consulta": 0,
                        "tiempo_promedio_minutos": 0,
                    }

    # ==========================================
    # 🦷 MÉTODOS PARA DASHBOARD DEL ODONTÓLOGO
    # ==========================================

    async def get_odontologo_stats_simple(self, odontologo_id: str) -> Dict[str, Any]:
        """
        🦷 ESTADÍSTICAS SIMPLIFICADAS PARA ODONTÓLOGO

        Stats para los 5 cards principales:
        1. Ingresos del Mes (USD total generado por este odontólogo)
        2. Ingresos Hoy (USD total de hoy)
        3. Consultas Hoy (intervenciones realizadas por este odontólogo)
        4. Servicios Aplicados (count de servicios únicos aplicados hoy)
        5. Tiempo Promedio Atención (minutos por consulta completada)

        Args:
            odontologo_id: UUID del odontólogo (id de personal)

        Returns:
            Dict con estadísticas para los 5 cards
        """
        try:
            logger.info(f"🦷 Obteniendo stats para odontólogo: {odontologo_id}")

            today = date.today().isoformat()
            current_month = datetime.now().strftime('%Y-%m')

            # 1️⃣ INGRESOS DEL MES (solo del odontólogo)
            # Necesitamos obtener intervenciones del odontólogo y sumar sus ingresos
            intervenciones_mes = self.client.table('intervencion').select(
                'id'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{current_month}-01"
            ).execute()

            intervenciones_ids = [i['id'] for i in (intervenciones_mes.data or [])]

            ingresos_mes_total = 0
            if intervenciones_ids:
                # Obtener servicios de esas intervenciones
                servicios_mes = self.client.table('historia_medica').select(
                    'precio_total_usd, precio_total_bs'
                ).in_('intervencion_id', intervenciones_ids).execute()

                # ingresos_mes_total = sum([
                #     (s.get('precio_total_usd', 0) or 0) + (s.get('precio_total_bs', 0) or 0)
                #     for s in (servicios_mes.data or [])
                # ])
                ingresos_mes_total = sum([
                    (s.get('precio_total_usd', 0))
                    for s in (servicios_mes.data or [])
                ])

            # 2️⃣ INGRESOS HOY (solo del odontólogo)
            intervenciones_hoy = self.client.table('intervencion').select(
                'id'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{today}T00:00:00"
            ).lt(
                'fecha_registro', f"{today}T23:59:59"
            ).execute()

            intervenciones_hoy_ids = [i['id'] for i in (intervenciones_hoy.data or [])]

            ingresos_hoy_total = 0
            if intervenciones_hoy_ids:
                servicios_hoy = self.client.table('historia_medica').select(
                    'precio_total_usd, precio_total_bs'
                ).in_('intervencion_id', intervenciones_hoy_ids).execute()

                # ingresos_hoy_total = sum([
                #     (s.get('precio_total_usd', 0) or 0) + (s.get('precio_total_bs', 0) or 0)
                #     for s in (servicios_hoy.data or [])
                # ])
                ingresos_hoy_total = sum([
                    (s.get('precio_total_usd', 0))
                    for s in (servicios_hoy.data or [])
                ])

            # 3️⃣ CONSULTAS HOY (intervenciones del odontólogo, no consultas)
            consultas_hoy_count = len(intervenciones_hoy_ids)

            # 4️⃣ SERVICIOS APLICADOS HOY (count de servicios)
            servicios_aplicados = 0
            if intervenciones_hoy_ids:
                servicios_aplicados_resp = self.client.table('historia_medica').select(
                    'id', count='exact'
                ).in_('intervencion_id', intervenciones_hoy_ids).execute()

                servicios_aplicados = servicios_aplicados_resp.count or 0

            # 5️⃣ TIEMPO PROMEDIO ATENCIÓN
            # Calcular desde hora_inicio hasta hora_fin de intervenciones completadas hoy
            # intervenciones_completadas_hoy = self.client.table('intervencion').select(
            #     'hora_inicio'
            # ).eq('odontologo_id', odontologo_id).eq('estado', 'completada').gte(
            #     'fecha_registro', f"{today}T00:00:00"
            # ).lt(
            #     'fecha_registro', f"{today}T23:59:59"
            # ).execute()

            # tiempos = []
            # for interv in (intervenciones_completadas_hoy.data or []):
            #     # Priorizar duracion_real si existe
            #     if interv.get('duracion_real'):
            #         tiempos.append(interv['duracion_real'])
            #     elif interv.get('hora_inicio') and interv.get('hora_fin'):
            #         try:
            #             # Parsear tiempos
            #             inicio = datetime.fromisoformat(interv['hora_inicio'].replace('Z', '+00:00'))
            #             fin = datetime.fromisoformat(interv['hora_fin'].replace('Z', '+00:00'))
            #             diferencia_minutos = (fin - inicio).total_seconds() / 60
            #             if diferencia_minutos > 0:
            #                 tiempos.append(diferencia_minutos)
            #         except Exception:
            #             continue

            # tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0

            logger.info(f"✅ Stats odontólogo: Ingresos mes=${ingresos_mes_total:.2f}, Hoy=${ingresos_hoy_total:.2f}, Consultas={consultas_hoy_count}")

            return {
                # Card 1: Ingresos del Mes
                "ingresos_mes": round(ingresos_mes_total, 2),

                # Card 2: Ingresos Hoy
                "ingresos_hoy": round(ingresos_hoy_total, 2),

                # Card 3: Consultas Hoy (intervenciones)
                "consultas_hoy": consultas_hoy_count,

                # Card 4: Servicios Aplicados
                "servicios_aplicados": servicios_aplicados,

                # Card 5: Tiempo Promedio
                # "tiempo_promedio_minutos": round(tiempo_promedio, 0),
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo stats del odontólogo: {e}")
            return {
                "ingresos_mes": 0,
                "ingresos_hoy": 0,
                "consultas_hoy": 0,
                "servicios_aplicados": 0,
                "tiempo_promedio_minutos": 0,
            }

    async def get_odontologo_chart_data(self, odontologo_id: str) -> Dict[str, list[Dict[str, Any]]]:
        """
        📈 DATOS PARA GRÁFICOS DEL ODONTÓLOGO (últimos 30 días)

        Genera 2 arrays de datos:
        1. Consultas por día (intervenciones realizadas)
        2. Ingresos por día (en USD)

        Args:
            odontologo_id: UUID del odontólogo

        Returns:
            Dict con arrays: consultas_data, ingresos_data
        """
        try:
            logger.info(f"📈 Obteniendo datos de gráficos para odontólogo: {odontologo_id}")

            # Preparar fechas (últimos 30 días)
            dates = []
            for i in range(30, -1, -1):
                date_obj = datetime.now() - timedelta(days=i)
                dates.append({
                    'date_obj': date_obj.date(),
                    'date_str': date_obj.strftime("%d-%m"),
                    'date_sql': date_obj.strftime("%Y-%m-%d")
                })

            consultas_data = []
            ingresos_data = []

            # Obtener datos para cada día
            for date_info in dates:
                # 📅 INTERVENCIONES DEL DÍA
                intervenciones_dia = self.client.table('intervencion').select(
                    'id'
                ).eq('odontologo_id', odontologo_id).gte(
                    'fecha_registro', f"{date_info['date_sql']}T00:00:00"
                ).lt(
                    'fecha_registro', f"{date_info['date_sql']}T23:59:59"
                ).execute()

                intervenciones_count = len(intervenciones_dia.data or [])
                intervenciones_ids = [i['id'] for i in (intervenciones_dia.data or [])]

                # 💰 INGRESOS DEL DÍA
                ingresos_dia = 0
                if intervenciones_ids:
                    servicios_dia = self.client.table('historia_medica').select(
                        'precio_total_usd, precio_total_bs'
                    ).in_('intervencion_id', intervenciones_ids).execute()

                    ingresos_dia = sum([
                        (s.get('precio_total_usd', 0) or 0) + (s.get('precio_total_bs', 0) or 0)
                        for s in (servicios_dia.data or [])
                    ])

                # Agregar a los arrays
                consultas_data.append({
                    "name": date_info['date_str'],
                    "Consultas": intervenciones_count
                })

                ingresos_data.append({
                    "name": date_info['date_str'],
                    "Ingresos": float(ingresos_dia)
                })

            return {
                "consultas_data": consultas_data,
                "ingresos_data": ingresos_data
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo datos de gráficos del odontólogo: {e}")
            return self._get_empty_chart_data_odontologo()

    async def get_odontologo_top_servicios(self, odontologo_id: str, limit: int = 5) -> list[Dict[str, Any]]:
        """
        📊 TOP SERVICIOS MÁS APLICADOS POR EL ODONTÓLOGO (hoy)

        Agrupa los servicios aplicados hoy y retorna los top N con:
        - Nombre del servicio
        - Cantidad de veces aplicado
        - Total de ingresos generados

        Args:
            odontologo_id: UUID del odontólogo
            limit: Número máximo de servicios a retornar (default: 5)

        Returns:
            List de dicts con: servicio_nombre, count, total_ingresos
        """
        try:
            logger.info(f"📊 Obteniendo top {limit} servicios para odontólogo: {odontologo_id}")

            today = date.today().isoformat()

            # 1. Obtener intervenciones del día
            intervenciones_hoy = self.client.table('intervencion').select(
                'id'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{today}T00:00:00"
            ).lt(
                'fecha_registro', f"{today}T23:59:59"
            ).execute()

            intervenciones_ids = [i['id'] for i in (intervenciones_hoy.data or [])]

            if not intervenciones_ids:
                return []

            # 2. Obtener servicios aplicados en esas intervenciones
            servicios_aplicados = self.client.table('historia_medica').select(
                'servicio_id, precio_total_usd, precio_total_bs, cantidad'
            ).in_('intervencion_id', intervenciones_ids).execute()

            if not servicios_aplicados.data:
                return []

            # 3. Agrupar por servicio_id
            servicios_agrupados = {}
            for servicio in servicios_aplicados.data:
                servicio_id = servicio.get('servicio_id')
                if not servicio_id:
                    continue

                if servicio_id not in servicios_agrupados:
                    servicios_agrupados[servicio_id] = {
                        'servicio_id': servicio_id,
                        'count': 0,
                        'total_ingresos': 0
                    }

                servicios_agrupados[servicio_id]['count'] += servicio.get('cantidad', 1)
                servicios_agrupados[servicio_id]['total_ingresos'] += (
                    (servicio.get('precio_total_usd', 0) or 0) +
                    (servicio.get('precio_total_bs', 0) or 0)
                )

            # 4. Obtener nombres de los servicios
            servicio_ids = list(servicios_agrupados.keys())
            servicios_info = self.client.table('servicios').select(
                'id, nombre'
            ).in_('id', servicio_ids).execute()

            # Crear diccionario id -> nombre
            nombres_servicios = {
                s['id']: s['nombre']
                for s in (servicios_info.data or [])
            }

            # 5. Construir resultado final
            resultado = []
            for servicio_id, datos in servicios_agrupados.items():
                resultado.append({
                    'servicio_nombre': nombres_servicios.get(servicio_id, 'Servicio Desconocido'),
                    'count': datos['count'],
                    'total_ingresos': round(datos['total_ingresos'], 2)
                })

            # 6. Ordenar por count (descendente) y limitar
            resultado_ordenado = sorted(resultado, key=lambda x: x['count'], reverse=True)[:limit]

            logger.info(f"✅ Top {len(resultado_ordenado)} servicios obtenidos")

            return resultado_ordenado

        except Exception as e:
            logger.error(f"❌ Error obteniendo top servicios del odontólogo: {e}")
            return []

    def _get_empty_chart_data_odontologo(self) -> Dict[str, list]:
        """📊 DATOS VACÍOS PARA GRÁFICOS DEL ODONTÓLOGO"""
        empty_data_consultas = []
        empty_data_ingresos = []

        for i in range(30, -1, -1):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%d-%m")
            empty_data_consultas.append({
                "name": date_str,
                "Consultas": 0
            })
            empty_data_ingresos.append({
                "name": date_str,
                "Ingresos": 0
            })

        return {
            "consultas_data": empty_data_consultas,
            "ingresos_data": empty_data_ingresos
        }

    # ====================================================================
    # 👨‍💼 MÉTODOS PARA DASHBOARD ADMINISTRADOR (VISTA "HOY")
    # ====================================================================

    async def get_dashboard_stats_admin(self) -> Dict[str, Any]:
        """
        📊 Estadísticas del dashboard del ADMINISTRADOR (solo del día actual)

        Returns:
            {
                "consultas_hoy_completadas": 5,
                "consultas_hoy_total": 12,
                "ingresos_hoy": 850.50,
                "pagos_realizados_hoy": 8,
                "servicios_aplicados_hoy": 15,
                "intervenciones_hoy": 18,
                "pacientes_nuevos_hoy": 2
            }
        """
        try:
            from datetime import date
            hoy = date.today().isoformat()

            logger.info(f"📊 Obteniendo estadísticas dashboard admin para {hoy}")

            # 1. Consultas de hoy
            consultas_response = self.client.table('consulta').select(
                'id, estado'
            ).gte('fecha_llegada', f"{hoy}T00:00:00").lte(
                'fecha_llegada', f"{hoy}T23:59:59"
            ).execute()

            consultas_hoy_total = len(consultas_response.data) if consultas_response.data else 0
            consultas_hoy_completadas = sum(
                1 for c in (consultas_response.data or []) if c.get('estado') == 'completada'
            )

            # 2. Ingresos de hoy (solo USD)
            ingresos_response = self.client.table('pago').select(
                'monto_pagado_usd'
            ).eq('estado_pago', 'completado').gte(
                'fecha_pago', f"{hoy}T00:00:00"
            ).lte(
                'fecha_pago', f"{hoy}T23:59:59"
            ).execute()

            ingresos_hoy = sum(
                float(p.get('monto_pagado_usd', 0) or 0)
                for p in (ingresos_response.data or [])
            )

            # 3. Pagos realizados hoy (cantidad)
            pagos_realizados_hoy = len(ingresos_response.data) if ingresos_response.data else 0

            # 4. Servicios aplicados hoy
            servicios_response = self.client.table('historia_medica').select(
                'id'
            ).gte('fecha_registro', f"{hoy}T00:00:00").lte(
                'fecha_registro', f"{hoy}T23:59:59"
            ).execute()

            servicios_aplicados_hoy = len(servicios_response.data) if servicios_response.data else 0

            # 5. Intervenciones de hoy
            intervenciones_response = self.client.table('intervencion').select(
                'id'
            ).gte('fecha_registro', f"{hoy}T00:00:00").lte(
                'fecha_registro', f"{hoy}T23:59:59"
            ).execute()

            intervenciones_hoy = len(intervenciones_response.data) if intervenciones_response.data else 0

            # 6. Pacientes nuevos hoy
            pacientes_response = self.client.table('paciente').select(
                'id'
            ).eq('fecha_registro', hoy).execute()

            pacientes_nuevos_hoy = len(pacientes_response.data) if pacientes_response.data else 0

            resultado = {
                'consultas_hoy_completadas': consultas_hoy_completadas,
                'consultas_hoy_total': consultas_hoy_total,
                'ingresos_hoy': round(ingresos_hoy, 2),
                'pagos_realizados_hoy': pagos_realizados_hoy,
                'servicios_aplicados_hoy': servicios_aplicados_hoy,
                'intervenciones_hoy': intervenciones_hoy,
                'pacientes_nuevos_hoy': pacientes_nuevos_hoy
            }

            logger.info(f"✅ Dashboard admin: {consultas_hoy_total} consultas, ${ingresos_hoy:.2f} ingresos")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo stats admin: {e}")
            return {
                'consultas_hoy_completadas': 0,
                'consultas_hoy_total': 0,
                'ingresos_hoy': 0,
                'pagos_realizados_hoy': 0,
                'servicios_aplicados_hoy': 0,
                'intervenciones_hoy': 0,
                'pacientes_nuevos_hoy': 0
            }

    async def get_consultas_hoy_por_estado_admin(self) -> List[Dict[str, Any]]:
        """
        📊 Consultas de hoy agrupadas por estado (ADMINISTRADOR)

        Returns:
            [
                {"estado": "En Espera", "cantidad": 5, "color": "yellow"},
                {"estado": "En Atención", "cantidad": 3, "color": "blue"},
                ...
            ]
        """
        try:
            from datetime import date
            hoy = date.today().isoformat()

            response = self.client.table('consulta').select(
                'estado'
            ).gte('fecha_llegada', f"{hoy}T00:00:00").lte(
                'fecha_llegada', f"{hoy}T23:59:59"
            ).execute()

            # Agrupar por estado
            estados_count = {}
            for consulta in (response.data or []):
                estado = consulta.get('estado', 'desconocido')
                estados_count[estado] = estados_count.get(estado, 0) + 1

            # Mapear estados a nombres legibles y colores
            mapeo_estados = {
                'programada': {'nombre': 'En Espera', 'color': 'yellow'},
                'en_progreso': {'nombre': 'En Atención', 'color': 'blue'},
                'completada': {'nombre': 'Completada', 'color': 'green'},
                'cancelada': {'nombre': 'Cancelada', 'color': 'red'}
            }

            resultado = [
                {
                    'estado': mapeo_estados.get(estado, {'nombre': estado.title(), 'color': 'gray'})['nombre'],
                    'cantidad': cantidad,
                    'color': mapeo_estados.get(estado, {'nombre': estado.title(), 'color': 'gray'})['color']
                }
                for estado, cantidad in estados_count.items()
            ]

            # Ordenar: en_espera, en_progreso, completada, cancelada
            orden = {'En Espera': 0, 'En Atención': 1, 'Completada': 2, 'Cancelada': 3}
            resultado.sort(key=lambda x: orden.get(x['estado'], 99))

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo consultas por estado admin: {e}")
            return []

    async def get_consultas_hoy_por_odontologo_admin(self) -> List[Dict[str, Any]]:
        """
        📊 Consultas de hoy agrupadas por odontólogo (ADMINISTRADOR)

        Returns:
            [
                {"nombre": "Dr. García", "cantidad": 8},
                {"nombre": "Dra. Martínez", "cantidad": 5},
                ...
            ]
        """
        try:
            from datetime import date
            hoy = date.today().isoformat()

            # Obtener intervenciones de hoy con información del odontólogo
            response = self.client.table('intervencion').select(
                'odontologo_id, personal:odontologo_id(primer_nombre, primer_apellido)'
            ).gte('fecha_registro', f"{hoy}T00:00:00").lte(
                'fecha_registro', f"{hoy}T23:59:59"
            ).execute()

            # Agrupar por odontólogo
            odontologos_count = {}
            for intervencion in (response.data or []):
                personal_data = intervencion.get('personal', {})
                if personal_data:
                    nombre = f"{personal_data.get('primer_nombre', '')} {personal_data.get('primer_apellido', '')}".strip()
                    odontologos_count[nombre] = odontologos_count.get(nombre, 0) + 1

            # Convertir a lista y ordenar por cantidad
            resultado = [
                {'nombre': nombre, 'cantidad': cantidad}
                for nombre, cantidad in odontologos_count.items()
            ]
            resultado.sort(key=lambda x: x['cantidad'], reverse=True)

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo consultas por odontólogo admin: {e}")
            return []

    async def get_dashboard_stats_asistente(self) -> Dict[str, Any]:
        """
        👩‍⚕️ Estadísticas básicas del dashboard del ASISTENTE (solo lectura - HOY)

        Returns:
            {
                "consultas_hoy_total": 12,
                "consultas_completadas": 5,
                "consultas_en_espera": 4,
                "pacientes_atendidos_hoy": 8
            }
        """
        try:
            from datetime import date
            hoy = date.today().isoformat()

            logger.info(f"👩‍⚕️ Obteniendo estadísticas dashboard asistente para {hoy}")

            # 1. Consultas de hoy (total, completadas, en espera)
            consultas_response = self.client.table('consulta').select(
                'id, estado'
            ).gte('fecha_llegada', f"{hoy}T00:00:00").lte(
                'fecha_llegada', f"{hoy}T23:59:59"
            ).execute()

            consultas_hoy_total = len(consultas_response.data) if consultas_response.data else 0

            consultas_completadas = sum(
                1 for c in (consultas_response.data or []) if c.get('estado') == 'completada'
            )

            consultas_en_espera = sum(
                1 for c in (consultas_response.data or [])
                if c.get('estado') in ['programada', 'en_progreso']
            )

            # 2. Pacientes únicos atendidos hoy (completados)
            consultas_completadas_ids = [
                c.get('id') for c in (consultas_response.data or [])
                if c.get('estado') == 'completada'
            ]

            if consultas_completadas_ids:
                # Obtener pacientes únicos de intervenciones completadas
                intervenciones_response = self.client.table('intervencion').select(
                    'consulta_id, numero_historia'
                ).in_('consulta_id', consultas_completadas_ids).execute()

                pacientes_unicos = set(
                    i.get('numero_historia') for i in (intervenciones_response.data or [])
                    if i.get('numero_historia')
                )
                pacientes_atendidos_hoy = len(pacientes_unicos)
            else:
                pacientes_atendidos_hoy = 0

            resultado = {
                'consultas_hoy_total': consultas_hoy_total,
                'consultas_completadas': consultas_completadas,
                'consultas_en_espera': consultas_en_espera,
                'pacientes_atendidos_hoy': pacientes_atendidos_hoy
            }

            logger.info(f"✅ Dashboard asistente: {consultas_hoy_total} consultas, {pacientes_atendidos_hoy} pacientes")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo stats asistente: {e}")
            return {
                'consultas_hoy_total': 0,
                'consultas_completadas': 0,
                'consultas_en_espera': 0,
                'pacientes_atendidos_hoy': 0
            }

# Instancia única para importar
dashboard_service = DashboardService()