"""
🎯 SERVICIO CENTRALIZADO DE REPORTES
Maneja todas las consultas y procesamiento de datos para reportes por rol

ESTRUCTURA:
- Métodos para Gerente (6 métodos)
- Métodos para Odontólogo (4 métodos)
- Métodos para Administrador (6 métodos)

OPTIMIZACIONES:
- Queries directas optimizadas
- Procesamiento en BD cuando es posible
- Cálculos de porcentajes en Python
- Manejo de errores robusto
"""

from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class ReportesService(BaseService):
    """
    Servicio que maneja todas las estadísticas y reportes diferenciados por rol
    """

    def __init__(self):
        super().__init__()

    # ====================================================================
    # 👔 MÉTODOS PARA GERENTE
    # ====================================================================

    async def get_distribucion_pagos_usd_bs(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, float]:
        """
        💵 Distribución de pagos USD vs BS para gráfico de torta

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            {
                "total_usd": 4357.75,
                "total_bs": 8092.25,
                "porcentaje_usd": 35.0,
                "porcentaje_bs": 65.0
            }
        """
        try:
            logger.info(f"📊 Obteniendo distribución pagos USD vs BS ({fecha_inicio} - {fecha_fin})")

            # Query optimizada
            response = self.client.table('pago').select(
                'monto_pagado_usd, monto_pagado_bs'
            ).eq('estado_pago', 'completado').gte(
                'fecha_pago', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_pago', f"{fecha_fin}T23:59:59"
            ).execute()

            # Calcular totales
            total_usd = 0.0
            total_bs = 0.0

            for pago in (response.data or []):
                total_usd += float(pago.get('monto_pagado_usd', 0) or 0)
                total_bs += float(pago.get('monto_pagado_bs', 0) or 0)

            # Calcular porcentajes
            total_general = total_usd + total_bs
            porcentaje_usd = (total_usd / total_general * 100) if total_general > 0 else 0
            porcentaje_bs = (total_bs / total_general * 100) if total_general > 0 else 0

            resultado = {
                "total_usd": round(total_usd, 2),
                "total_bs": round(total_bs, 2),
                "porcentaje_usd": round(porcentaje_usd, 1),
                "porcentaje_bs": round(porcentaje_bs, 1)
            }

            logger.info(f"✅ Distribución: USD ${total_usd:.2f} ({porcentaje_usd:.1f}%), BS ${total_bs:.2f} ({porcentaje_bs:.1f}%)")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo distribución pagos: {e}")
            return {
                "total_usd": 0.0,
                "total_bs": 0.0,
                "porcentaje_usd": 0.0,
                "porcentaje_bs": 0.0
            }

    async def get_ranking_servicios(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        🏆 Ranking de servicios más aplicados

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD
            limit: Número máximo de servicios a retornar

        Returns:
            [
                {
                    "servicio_nombre": "Limpieza Dental",
                    "categoria": "Preventiva",
                    "veces_aplicado": 156,
                    "ingresos_generados": 4680.00,
                    "porcentaje": 28.5
                },
                ...
            ]
        """
        try:
            logger.info(f"🏆 Obteniendo ranking servicios ({fecha_inicio} - {fecha_fin})")

            # Query con JOIN
            response = self.client.table('historia_medica').select(
                'servicio_id, precio_total_usd, precio_total_bs, servicio:servicio_id(nombre, categoria)'
            ).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            if not response.data:
                return []

            # Agrupar por servicio
            servicios_agrupados = {}
            for registro in response.data:
                servicio_id = registro.get('servicio_id')
                servicio_info = registro.get('servicio')

                if not servicio_info:
                    continue

                if servicio_id not in servicios_agrupados:
                    servicios_agrupados[servicio_id] = {
                        'servicio_nombre': servicio_info.get('nombre', 'Desconocido'),
                        'categoria': servicio_info.get('categoria', 'N/A'),
                        'veces_aplicado': 0,
                        'ingresos_generados': 0.0
                    }

                servicios_agrupados[servicio_id]['veces_aplicado'] += 1
                servicios_agrupados[servicio_id]['ingresos_generados'] += (
                    float(registro.get('precio_total_usd', 0) or 0) +
                    float(registro.get('precio_total_bs', 0) or 0)
                )

            # Convertir a lista y ordenar
            ranking = list(servicios_agrupados.values())
            ranking.sort(key=lambda x: x['veces_aplicado'], reverse=True)
            ranking = ranking[:limit]

            # Calcular porcentajes
            total_veces = sum(s['veces_aplicado'] for s in ranking)
            for servicio in ranking:
                servicio['porcentaje'] = round(
                    (servicio['veces_aplicado'] / total_veces * 100) if total_veces > 0 else 0,
                    1
                )
                servicio['ingresos_generados'] = round(servicio['ingresos_generados'], 2)

            logger.info(f"✅ Ranking obtenido: {len(ranking)} servicios")

            return ranking

        except Exception as e:
            logger.error(f"❌ Error obteniendo ranking servicios: {e}")
            return []

    async def get_ranking_odontologos(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        ordenar_por: str = 'intervenciones'  # 'intervenciones' o 'ingresos'
    ) -> List[Dict[str, Any]]:
        """
        👨‍⚕️ Ranking de odontólogos por intervenciones o ingresos

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD
            ordenar_por: 'intervenciones' o 'ingresos'

        Returns:
            [
                {
                    "nombre": "Dr. Juan Pérez",
                    "especialidad": "Endodoncia",
                    "total_intervenciones": 89,
                    "ingresos_totales": 8920.00
                },
                ...
            ]
        """
        try:
            logger.info(f"👨‍⚕️ Obteniendo ranking odontólogos ({fecha_inicio} - {fecha_fin})")

            # Query con JOIN
            response = self.client.table('intervencion').select(
                'id, total_usd, total_bs, odontologo_id, personal:odontologo_id(primer_nombre, primer_apellido, especialidad)'
            ).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            if not response.data:
                return []

            # Agrupar por odontólogo
            odontologos_agrupados = {}
            for intervencion in response.data:
                odontologo_id = intervencion.get('odontologo_id')
                odontologo_info = intervencion.get('personal')

                if not odontologo_info:
                    continue

                if odontologo_id not in odontologos_agrupados:
                    odontologos_agrupados[odontologo_id] = {
                        'nombre': f"{odontologo_info.get('primer_nombre', '')} {odontologo_info.get('primer_apellido', '')}".strip(),
                        'especialidad': odontologo_info.get('especialidad', 'General'),
                        'total_intervenciones': 0,
                        'ingresos_totales': 0.0
                    }

                odontologos_agrupados[odontologo_id]['total_intervenciones'] += 1
                odontologos_agrupados[odontologo_id]['ingresos_totales'] += (
                    float(intervencion.get('total_usd', 0) or 0) +
                    float(intervencion.get('total_bs', 0) or 0)
                )

            # Convertir a lista y ordenar
            ranking = list(odontologos_agrupados.values())

            if ordenar_por == 'ingresos':
                ranking.sort(key=lambda x: x['ingresos_totales'], reverse=True)
            else:
                ranking.sort(key=lambda x: x['total_intervenciones'], reverse=True)

            # Redondear ingresos
            for odontologo in ranking:
                odontologo['ingresos_totales'] = round(odontologo['ingresos_totales'], 2)

            logger.info(f"✅ Ranking odontólogos obtenido: {len(ranking)} odontólogos")

            return ranking

        except Exception as e:
            logger.error(f"❌ Error obteniendo ranking odontólogos: {e}")
            return []

    async def get_estadisticas_pacientes(self) -> Dict[str, Any]:
        """
        👥 Estadísticas generales de pacientes

        Returns:
            {
                "total_pacientes": 1247,
                "nuevos_mes": 87,
                "hombres": 598,
                "mujeres": 649,
                "edad_promedio": 35.5
            }
        """
        try:
            logger.info("👥 Obteniendo estadísticas de pacientes")

            # Total pacientes activos
            total_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).execute()

            total_pacientes = total_response.count or 0

            # Nuevos este mes
            current_month = datetime.now().strftime('%Y-%m')
            nuevos_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).gte(
                'fecha_registro', f"{current_month}-01"
            ).execute()

            nuevos_mes = nuevos_response.count or 0

            # Por género
            hombres_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).eq('genero', 'masculino').execute()

            mujeres_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).eq('genero', 'femenino').execute()

            hombres = hombres_response.count or 0
            mujeres = mujeres_response.count or 0

            # Edad promedio (calculado en cliente por simplicidad)
            # En producción, esto podría hacerse con una función SQL
            edad_promedio = 0.0  # Placeholder

            resultado = {
                "total_pacientes": total_pacientes,
                "nuevos_mes": nuevos_mes,
                "hombres": hombres,
                "mujeres": mujeres,
                "edad_promedio": edad_promedio
            }

            logger.info(f"✅ Stats pacientes: Total={total_pacientes}, Nuevos={nuevos_mes}")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas pacientes: {e}")
            return {
                "total_pacientes": 0,
                "nuevos_mes": 0,
                "hombres": 0,
                "mujeres": 0,
                "edad_promedio": 0.0
            }

    async def get_metodos_pago_populares(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        💳 Métodos de pago más usados

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            [
                {
                    "metodo": "Efectivo",
                    "veces_usado": 234,
                    "monto_total": 12450.00,
                    "porcentaje": 45.2
                },
                ...
            ]
        """
        try:
            logger.info(f"💳 Obteniendo métodos de pago populares ({fecha_inicio} - {fecha_fin})")

            # Query
            response = self.client.table('pago').select(
                'metodos_pago, monto_pagado_usd, monto_pagado_bs'
            ).eq('estado_pago', 'completado').gte(
                'fecha_pago', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_pago', f"{fecha_fin}T23:59:59"
            ).execute()

            if not response.data:
                return []

            # Agrupar por método (metodos_pago es JSONB array)
            metodos_agrupados = {}

            for pago in response.data:
                metodos = pago.get('metodos_pago', [])
                monto_total = (
                    float(pago.get('monto_pagado_usd', 0) or 0) +
                    float(pago.get('monto_pagado_bs', 0) or 0)
                )

                # Si metodos_pago está vacío, asumir "efectivo"
                if not metodos or not isinstance(metodos, list):
                    metodos = ["efectivo"]

                # Distribuir el monto entre los métodos usados
                monto_por_metodo = monto_total / len(metodos) if len(metodos) > 0 else monto_total

                for metodo in metodos:
                    # Normalizar nombre del método
                    metodo_nombre = str(metodo).lower().replace('_', ' ').title()

                    if metodo_nombre not in metodos_agrupados:
                        metodos_agrupados[metodo_nombre] = {
                            'metodo': metodo_nombre,
                            'veces_usado': 0,
                            'monto_total': 0.0
                        }

                    metodos_agrupados[metodo_nombre]['veces_usado'] += 1
                    metodos_agrupados[metodo_nombre]['monto_total'] += monto_por_metodo

            # Convertir a lista y ordenar
            ranking = list(metodos_agrupados.values())
            ranking.sort(key=lambda x: x['veces_usado'], reverse=True)

            # Calcular porcentajes
            total_veces = sum(m['veces_usado'] for m in ranking)
            for metodo in ranking:
                metodo['porcentaje'] = round(
                    (metodo['veces_usado'] / total_veces * 100) if total_veces > 0 else 0,
                    1
                )
                metodo['monto_total'] = round(metodo['monto_total'], 2)

            logger.info(f"✅ Métodos de pago: {len(ranking)} métodos identificados")

            return ranking

        except Exception as e:
            logger.error(f"❌ Error obteniendo métodos de pago: {e}")
            return []

    async def get_dashboard_cards_gerente(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, Any]:
        """
        📊 DATOS COMPLETOS PARA LOS 8 CARDS DEL DASHBOARD GERENTE

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            {
                "ingresos_mes": 45678.50,
                "consultas_mes": 156,
                "servicios_aplicados": 342,
                "pagos_pendientes_count": 12,
                "pagos_pendientes_monto": 5430.00,
                "total_pacientes": 1247,
                "pacientes_masculino": 598,
                "pacientes_femenino": 649,
                "consultas_canceladas": 8,
                "pacientes_nuevos_mes": 23
            }
        """
        try:
            logger.info(f"📊 Obteniendo datos completos para cards del gerente ({fecha_inicio} - {fecha_fin})")

            # 1. INGRESOS DEL MES (USD + BS convertido)
            ingresos_response = self.client.table('pago').select(
                'monto_pagado_usd, monto_pagado_bs'
            ).eq('estado_pago', 'completado').gte(
                'fecha_pago', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_pago', f"{fecha_fin}T23:59:59"
            ).execute()

            ingresos_mes = 0.0
            for pago in (ingresos_response.data or []):
                ingresos_mes += float(pago.get('monto_pagado_usd', 0) or 0)
                ingresos_mes += float(pago.get('monto_pagado_bs', 0) or 0)

            # 2. CONSULTAS DEL MES
            consultas_response = self.client.table('consulta').select(
                'id', count='exact'
            ).gte(
                'fecha_llegada', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_llegada', f"{fecha_fin}T23:59:59"
            ).execute()
            consultas_mes = consultas_response.count or 0

            # 3. SERVICIOS APLICADOS EN EL MES
            servicios_response = self.client.table('historia_medica').select(
                'id', count='exact'
            ).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()
            servicios_aplicados = servicios_response.count or 0

            # 4. PAGOS PENDIENTES (count + monto)
            pagos_pendientes_response = self.client.table('pago').select(
                'saldo_pendiente_usd, saldo_pendiente_bs'
            ).in_('estado_pago', ['pendiente', 'parcial']).execute()

            pagos_pendientes_count = len(pagos_pendientes_response.data or [])
            pagos_pendientes_monto = 0.0
            for pago in (pagos_pendientes_response.data or []):
                pagos_pendientes_monto += float(pago.get('saldo_pendiente_usd', 0) or 0)
                pagos_pendientes_monto += float(pago.get('saldo_pendiente_bs', 0) or 0)

            # 5. TOTAL PACIENTES (activos)
            total_pacientes_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).execute()
            total_pacientes = total_pacientes_response.count or 0

            # 6. PACIENTES POR GÉNERO
            masculino_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).eq('genero', 'masculino').execute()
            pacientes_masculino = masculino_response.count or 0

            femenino_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).eq('genero', 'femenino').execute()
            pacientes_femenino = femenino_response.count or 0

            # 7. CONSULTAS CANCELADAS DEL MES
            canceladas_response = self.client.table('consulta').select(
                'id', count='exact'
            ).eq('estado', 'cancelada').gte(
                'fecha_llegada', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_llegada', f"{fecha_fin}T23:59:59"
            ).execute()
            consultas_canceladas = canceladas_response.count or 0

            # 8. PACIENTES NUEVOS DEL MES
            nuevos_response = self.client.table('paciente').select(
                'id', count='exact'
            ).eq('activo', True).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()
            pacientes_nuevos_mes = nuevos_response.count or 0

            resultado = {
                'ingresos_mes': round(ingresos_mes, 2),
                'consultas_mes': consultas_mes,
                'servicios_aplicados': servicios_aplicados,
                'pagos_pendientes_count': pagos_pendientes_count,
                'pagos_pendientes_monto': round(pagos_pendientes_monto, 2),
                'total_pacientes': total_pacientes,
                'pacientes_masculino': pacientes_masculino,
                'pacientes_femenino': pacientes_femenino,
                'consultas_canceladas': consultas_canceladas,
                'pacientes_nuevos_mes': pacientes_nuevos_mes
            }

            logger.info(f"✅ Cards gerente obtenidos: Ingresos=${ingresos_mes:.2f}, Consultas={consultas_mes}")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo cards del gerente: {e}")
            return {
                'ingresos_mes': 0.0,
                'consultas_mes': 0,
                'servicios_aplicados': 0,
                'pagos_pendientes_count': 0,
                'pagos_pendientes_monto': 0.0,
                'total_pacientes': 0,
                'pacientes_masculino': 0,
                'pacientes_femenino': 0,
                'consultas_canceladas': 0,
                'pacientes_nuevos_mes': 0
            }

    async def get_evolucion_temporal(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        tipo: str
    ) -> List[Dict[str, Any]]:
        """
        📈 EVOLUCIÓN TEMPORAL PARA GRÁFICOS CON TABS

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD
            tipo: "pacientes_nuevos", "consultas", "ingresos"

        Returns:
            [
                {"fecha": "2025-01-01", "valor": 5},
                {"fecha": "2025-01-02", "valor": 8},
                ...
            ]
        """
        try:
            logger.info(f"📈 Obteniendo evolución temporal de {tipo} ({fecha_inicio} - {fecha_fin})")

            if tipo == "pacientes_nuevos":
                # Query de pacientes agrupados por fecha de registro
                response = self.client.table('paciente').select(
                    'fecha_registro'
                ).eq('activo', True).gte(
                    'fecha_registro', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_registro', f"{fecha_fin}T23:59:59"
                ).execute()

                # Agrupar por fecha
                datos_por_fecha = {}
                for paciente in (response.data or []):
                    fecha = paciente.get('fecha_registro', '')[:10]
                    datos_por_fecha[fecha] = datos_por_fecha.get(fecha, 0) + 1

            elif tipo == "consultas":
                # Query de consultas agrupadas por fecha de llegada
                response = self.client.table('consulta').select(
                    'fecha_llegada'
                ).gte(
                    'fecha_llegada', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_llegada', f"{fecha_fin}T23:59:59"
                ).execute()

                # Agrupar por fecha
                datos_por_fecha = {}
                for consulta in (response.data or []):
                    fecha = consulta.get('fecha_llegada', '')[:10]
                    datos_por_fecha[fecha] = datos_por_fecha.get(fecha, 0) + 1

            elif tipo == "ingresos":
                # Query de pagos agrupados por fecha de pago
                response = self.client.table('pago').select(
                    'fecha_pago, monto_pagado_usd, monto_pagado_bs'
                ).eq('estado_pago', 'completado').gte(
                    'fecha_pago', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_pago', f"{fecha_fin}T23:59:59"
                ).execute()

                # Agrupar por fecha y sumar montos
                datos_por_fecha = {}
                for pago in (response.data or []):
                    fecha = pago.get('fecha_pago', '')[:10]
                    monto = (
                        float(pago.get('monto_pagado_usd', 0) or 0) +
                        float(pago.get('monto_pagado_bs', 0) or 0)
                    )
                    datos_por_fecha[fecha] = datos_por_fecha.get(fecha, 0.0) + monto

            else:
                logger.warning(f"⚠️ Tipo de evolución no reconocido: {tipo}")
                return []

            # Convertir a lista ordenada
            resultado = [
                {'fecha': fecha, 'valor': round(valor, 2) if tipo == "ingresos" else int(valor)}
                for fecha, valor in sorted(datos_por_fecha.items())
            ]

            logger.info(f"✅ Evolución temporal obtenida: {len(resultado)} días con datos")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo evolución temporal: {e}")
            return []

    # ====================================================================
    # 🦷 MÉTODOS PARA ODONTÓLOGO
    # ====================================================================

    async def get_ingresos_odontologo_usd_bs(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, float]:
        """
        💵 Distribución de ingresos USD vs BS del odontólogo

        Args:
            odontologo_id: UUID del odontólogo
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            {
                "total_usd": 3568.00,
                "total_bs": 5352.00,
                "porcentaje_usd": 40.0,
                "porcentaje_bs": 60.0
            }
        """
        try:
            logger.info(f"💵 Obteniendo ingresos odontólogo {odontologo_id}")

            # Query de intervenciones del odontólogo
            response = self.client.table('intervencion').select(
                'total_usd, total_bs'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            # Calcular totales
            total_usd = 0.0
            total_bs = 0.0

            for intervencion in (response.data or []):
                total_usd += float(intervencion.get('total_usd', 0) or 0)
                total_bs += float(intervencion.get('total_bs', 0) or 0)

            # Calcular porcentajes
            total_general = total_usd + total_bs
            porcentaje_usd = (total_usd / total_general * 100) if total_general > 0 else 0
            porcentaje_bs = (total_bs / total_general * 100) if total_general > 0 else 0

            resultado = {
                "total_usd": round(total_usd, 2),
                "total_bs": round(total_bs, 2),
                "porcentaje_usd": round(porcentaje_usd, 1),
                "porcentaje_bs": round(porcentaje_bs, 1)
            }

            logger.info(f"✅ Ingresos odontólogo: USD ${total_usd:.2f}, BS ${total_bs:.2f}")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo ingresos odontólogo: {e}")
            return {
                "total_usd": 0.0,
                "total_bs": 0.0,
                "porcentaje_usd": 0.0,
                "porcentaje_bs": 0.0
            }

    async def get_ranking_servicios_odontologo(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        🏆 Ranking de servicios más aplicados por el odontólogo

        Args:
            odontologo_id: UUID del odontólogo
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD
            limit: Número máximo de servicios

        Returns:
            [
                {
                    "servicio_nombre": "Limpieza Dental",
                    "categoria": "Preventiva",
                    "veces_aplicado": 67,
                    "ingresos_generados": 2010.00,
                    "promedio_por_servicio": 30.00,
                    "porcentaje": 28.5
                },
                ...
            ]
        """
        try:
            logger.info(f"🏆 Obteniendo ranking servicios odontólogo {odontologo_id}")

            # Primero obtener IDs de intervenciones del odontólogo
            intervenciones_response = self.client.table('intervencion').select(
                'id'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            if not intervenciones_response.data:
                return []

            intervencion_ids = [i['id'] for i in intervenciones_response.data]

            # Query de servicios de esas intervenciones
            response = self.client.table('historia_medica').select(
                'servicio_id, precio_total_usd, precio_total_bs, servicio:servicio_id(nombre, categoria)'
            ).in_('intervencion_id', intervencion_ids).execute()

            if not response.data:
                return []

            # Agrupar por servicio
            servicios_agrupados = {}
            for registro in response.data:
                servicio_id = registro.get('servicio_id')
                servicio_info = registro.get('servicio')

                if not servicio_info:
                    continue

                if servicio_id not in servicios_agrupados:
                    servicios_agrupados[servicio_id] = {
                        'servicio_nombre': servicio_info.get('nombre', 'Desconocido'),
                        'categoria': servicio_info.get('categoria', 'N/A'),
                        'veces_aplicado': 0,
                        'ingresos_generados': 0.0
                    }

                servicios_agrupados[servicio_id]['veces_aplicado'] += 1
                servicios_agrupados[servicio_id]['ingresos_generados'] += (
                    float(registro.get('precio_total_usd', 0) or 0) +
                    float(registro.get('precio_total_bs', 0) or 0)
                )

            # Convertir a lista y ordenar
            ranking = list(servicios_agrupados.values())
            ranking.sort(key=lambda x: x['veces_aplicado'], reverse=True)
            ranking = ranking[:limit]

            # Calcular porcentajes y promedios
            total_veces = sum(s['veces_aplicado'] for s in ranking)
            for servicio in ranking:
                servicio['porcentaje'] = round(
                    (servicio['veces_aplicado'] / total_veces * 100) if total_veces > 0 else 0,
                    1
                )
                servicio['promedio_por_servicio'] = round(
                    servicio['ingresos_generados'] / servicio['veces_aplicado'],
                    2
                )
                servicio['ingresos_generados'] = round(servicio['ingresos_generados'], 2)

            logger.info(f"✅ Ranking servicios odontólogo: {len(ranking)} servicios")

            return ranking

        except Exception as e:
            logger.error(f"❌ Error obteniendo ranking servicios odontólogo: {e}")
            return []

    async def get_intervenciones_odontologo(
        self,
        odontologo_id: str,
        filtros: Dict[str, Any],
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        📋 Tabla completa de intervenciones del odontólogo con paginación

        Args:
            odontologo_id: UUID del odontólogo
            filtros: {
                "fecha_inicio": "2025-10-01",
                "fecha_fin": "2025-10-31",
                "busqueda": "texto",  # nombre paciente o número consulta
                "estado": "completada"
            }
            limit: Registros por página
            offset: Offset para paginación

        Returns:
            {
                "intervenciones": [...],
                "total": 145,
                "pagina_actual": 1,
                "total_paginas": 3
            }
        """
        try:
            logger.info(f"📋 Obteniendo intervenciones odontólogo {odontologo_id}")

            # Construir query base
            query = self.client.table('intervencion').select(
                '''
                id,
                fecha_registro,
                procedimiento_realizado,
                total_usd,
                total_bs,
                estado,
                consulta:consulta_id(numero_consulta, paciente:paciente_id(primer_nombre, primer_apellido))
                ''',
                count='exact'
            ).eq('odontologo_id', odontologo_id)

            # Aplicar filtros
            if filtros.get('fecha_inicio'):
                query = query.gte('fecha_registro', f"{filtros['fecha_inicio']}T00:00:00")

            if filtros.get('fecha_fin'):
                query = query.lte('fecha_registro', f"{filtros['fecha_fin']}T23:59:59")

            if filtros.get('estado'):
                query = query.eq('estado', filtros['estado'])

            # Ejecutar con paginación
            response = query.order(
                'fecha_registro', desc=True
            ).range(offset, offset + limit - 1).execute()

            # Procesar datos
            intervenciones = []
            for interv in (response.data or []):
                consulta_info = interv.get('consulta', {})
                paciente_info = consulta_info.get('paciente', {}) if consulta_info else {}

                intervenciones.append({
                    'id': interv.get('id'),
                    'fecha_registro': interv.get('fecha_registro', ''),
                    'numero_consulta': consulta_info.get('numero_consulta', 'N/A') if consulta_info else 'N/A',
                    'paciente_nombre': f"{paciente_info.get('primer_nombre', '')} {paciente_info.get('primer_apellido', '')}".strip() if paciente_info else 'N/A',
                    'procedimiento_realizado': interv.get('procedimiento_realizado', ''),
                    'total_usd': float(interv.get('total_usd', 0) or 0),
                    'total_bs': float(interv.get('total_bs', 0) or 0),
                    'estado': interv.get('estado', '')
                })

            # Calcular paginación
            total = response.count or 0
            pagina_actual = (offset // limit) + 1
            total_paginas = (total + limit - 1) // limit if total > 0 else 1

            resultado = {
                'intervenciones': intervenciones,
                'total': total,
                'pagina_actual': pagina_actual,
                'total_paginas': total_paginas
            }

            logger.info(f"✅ Intervenciones obtenidas: {len(intervenciones)} de {total}")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo intervenciones odontólogo: {e}")
            return {
                'intervenciones': [],
                'total': 0,
                'pagina_actual': 1,
                'total_paginas': 1
            }

    async def get_estadisticas_odontograma_odontologo(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, Any]:
        """
        🦷 Estadísticas del odontograma del odontólogo

        Args:
            odontologo_id: UUID del odontólogo
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            {
                "condiciones_mas_tratadas": [
                    {"tipo": "obturacion", "cantidad": 67, "porcentaje": 34.5},
                    ...
                ],
                "dientes_mas_intervenidos": [
                    {"diente_numero": 16, "intervenciones": 18},
                    ...
                ],
                "superficies_mas_tratadas": [
                    {"superficie": "oclusal", "cantidad": 45, "porcentaje": 38.2},
                    ...
                ]
            }
        """
        try:
            logger.info(f"🦷 Obteniendo estadísticas odontograma {odontologo_id}")

            # Primero obtener IDs de intervenciones del odontólogo
            intervenciones_response = self.client.table('intervencion').select(
                'id'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            if not intervenciones_response.data:
                return {
                    "condiciones_mas_tratadas": [],
                    "dientes_mas_intervenidos": [],
                    "superficies_mas_tratadas": []
                }

            intervencion_ids = [i['id'] for i in intervenciones_response.data]

            # Query de SERVICIOS aplicados (historia_medica) en lugar de condiciones
            response = self.client.table('historia_medica').select(
                'diente_numero, superficie, servicio:servicio_id(nombre, categoria)'
            ).in_('intervencion_id', intervencion_ids).execute()

            if not response.data:
                return {
                    "condiciones_mas_tratadas": [],
                    "dientes_mas_intervenidos": [],
                    "superficies_mas_tratadas": []
                }

            # Agrupar estadísticas
            servicios_count = {}  # Servicios aplicados
            dientes_servicios = {}  # Servicios únicos por diente
            superficies_count = {}  # Superficies tratadas

            for registro in response.data:
                diente_num = registro.get('diente_numero')
                superficie = registro.get('superficie')
                servicio_data = registro.get('servicio', {})
                servicio_nombre = servicio_data.get('nombre', 'N/A') if servicio_data else 'N/A'

                # Contar servicios aplicados
                servicios_count[servicio_nombre] = servicios_count.get(servicio_nombre, 0) + 1

                # Contar dientes intervenidos (solo si tiene diente_numero)
                if diente_num:
                    # Contar UNA VEZ por diente, sin importar si es superficie o completo
                    if diente_num not in dientes_servicios:
                        dientes_servicios[diente_num] = set()
                    dientes_servicios[diente_num].add(servicio_nombre)

                # Contar superficies (SOLO si superficie NO es NULL)
                if superficie and superficie.strip():
                    superficies_count[superficie] = superficies_count.get(superficie, 0) + 1

            # Convertir a listas y ordenar
            # 1. SERVICIOS MÁS APLICADOS
            total_servicios = sum(servicios_count.values())
            servicios_list = [
                {
                    'tipo': servicio_nombre,  # Ya viene con formato correcto
                    'cantidad': cantidad,
                    'porcentaje': round((cantidad / total_servicios * 100) if total_servicios > 0 else 0, 1)
                }
                for servicio_nombre, cantidad in servicios_count.items()
            ]
            servicios_list.sort(key=lambda x: x['cantidad'], reverse=True)
            servicios_list = servicios_list[:5]  # Top 5

            # 2. DIENTES MÁS INTERVENIDOS (contar servicios únicos por diente)
            dientes_list = [
                {
                    'diente_numero': num,
                    'intervenciones': len(servicios_set)  # Cantidad de servicios únicos
                }
                for num, servicios_set in dientes_servicios.items()
            ]
            dientes_list.sort(key=lambda x: x['intervenciones'], reverse=True)
            dientes_list = dientes_list[:5]  # Top 5

            # 3. SUPERFICIES MÁS TRATADAS (solo cuando superficie NO es NULL)
            total_superficies = sum(superficies_count.values())
            superficies_list = [
                {
                    'superficie': sup.title() if sup else 'N/A',
                    'cantidad': cantidad,
                    'porcentaje': round((cantidad / total_superficies * 100) if total_superficies > 0 else 0, 1)
                }
                for sup, cantidad in superficies_count.items()
            ]
            superficies_list.sort(key=lambda x: x['cantidad'], reverse=True)

            resultado = {
                'condiciones_mas_tratadas': servicios_list,  # Ahora son servicios aplicados
                'dientes_mas_intervenidos': dientes_list,
                'superficies_mas_tratadas': superficies_list
            }

            logger.info(f"✅ Estadísticas odontograma obtenidas")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas odontograma: {e}")
            return {
                "condiciones_mas_tratadas": [],
                "dientes_mas_intervenidos": [],
                "superficies_mas_tratadas": []
            }

    async def get_dashboard_cards_odontologo(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, Any]:
        """
        📊 DATOS COMPLETOS PARA LOS CARDS DEL DASHBOARD ODONTÓLOGO

        Args:
            odontologo_id: UUID del odontólogo
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            {
                "ingresos_total": 12450.50,
                "num_consultas": 45,
                "servicios_aplicados": 128,
                "consultas_canceladas": 3,
                "promedio_por_consulta": 276.68,
                "pacientes_unicos": 38,
                "dientes_tratados": 156
            }
        """
        try:
            logger.info(f"📊 Obteniendo dashboard cards odontólogo {odontologo_id} ({fecha_inicio} - {fecha_fin})")

            # 1. INGRESOS TOTALES (desde intervenciones)
            intervenciones_response = self.client.table('intervencion').select(
                'id, total_usd, total_bs, consulta_id'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            ingresos_total = 0.0
            consultas_ids = set()
            for interv in (intervenciones_response.data or []):
                ingresos_total += float(interv.get('total_usd', 0) or 0)
                ingresos_total += float(interv.get('total_bs', 0) or 0)
                if interv.get('consulta_id'):
                    consultas_ids.add(interv.get('consulta_id'))

            num_consultas = len(consultas_ids)

            # 2. SERVICIOS APLICADOS (desde historia_medica)
            intervencion_ids = [i['id'] for i in (intervenciones_response.data or [])]

            servicios_aplicados = 0
            if intervencion_ids:
                servicios_response = self.client.table('historia_medica').select(
                    'id', count='exact'
                ).in_('intervencion_id', intervencion_ids).execute()
                servicios_aplicados = servicios_response.count or 0

            # 3. CONSULTAS CANCELADAS
            # TODO: Redefinir qué significa "canceladas" para un odontólogo específico
            # Por ahora en 0 porque no tiene sentido contar por primer_odontologo_id
            # cuando el odontólogo puede trabajar en consultas de otros
            consultas_canceladas = 0

            # 4. PROMEDIO POR CONSULTA
            promedio_por_consulta = (ingresos_total / num_consultas) if num_consultas > 0 else 0.0

            # 5. PACIENTES ÚNICOS (desde consultas)
            pacientes_unicos = 0
            if consultas_ids:
                consultas_response = self.client.table('consulta').select(
                    'paciente_id'
                ).in_('id', list(consultas_ids)).execute()

                pacientes_set = set()
                for c in (consultas_response.data or []):
                    if c.get('paciente_id'):
                        pacientes_set.add(c.get('paciente_id'))
                pacientes_unicos = len(pacientes_set)

            # 6. DIENTES TRATADOS (desde diente)
            dientes_tratados = 0
            if intervencion_ids:
                dientes_response = self.client.table('diente').select(
                    'diente_numero'
                ).in_('intervencion_id', intervencion_ids).eq('activo', True).execute()

                dientes_set = set()
                for d in (dientes_response.data or []):
                    if d.get('diente_numero'):
                        dientes_set.add(d.get('diente_numero'))
                dientes_tratados = len(dientes_set)

            resultado = {
                'ingresos_total': round(ingresos_total, 2),
                'num_consultas': num_consultas,
                'servicios_aplicados': servicios_aplicados,
                'consultas_canceladas': consultas_canceladas,
                'promedio_por_consulta': round(promedio_por_consulta, 2),
                'pacientes_unicos': pacientes_unicos,
                'dientes_tratados': dientes_tratados
            }

            logger.info(f"✅ Cards odontólogo: Ingresos=${ingresos_total:.2f}, Consultas={num_consultas}")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo cards odontólogo: {e}")
            return {
                'ingresos_total': 0.0,
                'num_consultas': 0,
                'servicios_aplicados': 0,
                'consultas_canceladas': 0,
                'promedio_por_consulta': 0.0,
                'pacientes_unicos': 0,
                'dientes_tratados': 0
            }

    async def get_metodos_pago_odontologo(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        💳 Métodos de pago usados en servicios del odontólogo

        Args:
            odontologo_id: UUID del odontólogo
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            [
                {
                    "metodo": "Efectivo",
                    "veces_usado": 23,
                    "monto_total": 4580.00,
                    "porcentaje": 45.2
                },
                ...
            ]
        """
        try:
            logger.info(f"💳 Obteniendo métodos de pago odontólogo {odontologo_id}")

            # Obtener intervenciones del odontólogo
            intervenciones_response = self.client.table('intervencion').select(
                'consulta_id'
            ).eq('odontologo_id', odontologo_id).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            if not intervenciones_response.data:
                return []

            consultas_ids = list(set([i['consulta_id'] for i in intervenciones_response.data if i.get('consulta_id')]))

            if not consultas_ids:
                return []

            # Obtener pagos de esas consultas
            pagos_response = self.client.table('pago').select(
                'metodos_pago, monto_pagado_usd, monto_pagado_bs'
            ).in_('consulta_id', consultas_ids).eq('estado_pago', 'completado').execute()

            if not pagos_response.data:
                return []

            # Agrupar por método
            metodos_agrupados = {}

            for pago in pagos_response.data:
                metodos = pago.get('metodos_pago', [])
                monto_total = (
                    float(pago.get('monto_pagado_usd', 0) or 0) +
                    float(pago.get('monto_pagado_bs', 0) or 0)
                )

                if not metodos or not isinstance(metodos, list):
                    metodos = ["efectivo"]

                monto_por_metodo = monto_total / len(metodos) if len(metodos) > 0 else monto_total

                for metodo in metodos:
                    metodo_nombre = str(metodo).lower().replace('_', ' ').title()

                    if metodo_nombre not in metodos_agrupados:
                        metodos_agrupados[metodo_nombre] = {
                            'metodo': metodo_nombre,
                            'veces_usado': 0,
                            'monto_total': 0.0
                        }

                    metodos_agrupados[metodo_nombre]['veces_usado'] += 1
                    metodos_agrupados[metodo_nombre]['monto_total'] += monto_por_metodo

            # Convertir a lista y ordenar
            ranking = list(metodos_agrupados.values())
            ranking.sort(key=lambda x: x['veces_usado'], reverse=True)

            # Calcular porcentajes
            total_veces = sum(m['veces_usado'] for m in ranking)
            for metodo in ranking:
                metodo['porcentaje'] = round(
                    (metodo['veces_usado'] / total_veces * 100) if total_veces > 0 else 0,
                    1
                )
                metodo['monto_total'] = round(metodo['monto_total'], 2)

            logger.info(f"✅ Métodos de pago odontólogo: {len(ranking)} métodos")

            return ranking

        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo métodos de pago odontólogo (probablemente sin permisos): {e}")
            # Retornar lista vacía si no hay permisos (es esperado para odontólogos)
            return []

    async def get_evolucion_temporal_odontologo(
        self,
        odontologo_id: str,
        fecha_inicio: str,
        fecha_fin: str,
        tipo: str
    ) -> List[Dict[str, Any]]:
        """
        📈 EVOLUCIÓN TEMPORAL PARA GRÁFICOS DEL ODONTÓLOGO

        Args:
            odontologo_id: UUID del odontólogo
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD
            tipo: "ingresos", "intervenciones"

        Returns:
            [
                {"fecha": "2025-01-01", "valor": 450.00},
                {"fecha": "2025-01-02", "valor": 680.00},
                ...
            ]
        """
        try:
            logger.info(f"📈 Obteniendo evolución temporal odontólogo {tipo} ({fecha_inicio} - {fecha_fin})")

            if tipo == "ingresos":
                # Query de intervenciones agrupadas por fecha
                response = self.client.table('intervencion').select(
                    'fecha_registro, total_usd, total_bs'
                ).eq('odontologo_id', odontologo_id).gte(
                    'fecha_registro', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_registro', f"{fecha_fin}T23:59:59"
                ).execute()

                # Agrupar por fecha y sumar montos
                datos_por_fecha = {}
                for interv in (response.data or []):
                    fecha = interv.get('fecha_registro', '')[:10]
                    monto = (
                        float(interv.get('total_usd', 0) or 0) +
                        float(interv.get('total_bs', 0) or 0)
                    )
                    datos_por_fecha[fecha] = datos_por_fecha.get(fecha, 0.0) + monto

            elif tipo == "intervenciones":
                # Query de intervenciones agrupadas por fecha
                response = self.client.table('intervencion').select(
                    'fecha_registro'
                ).eq('odontologo_id', odontologo_id).gte(
                    'fecha_registro', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_registro', f"{fecha_fin}T23:59:59"
                ).execute()

                # Agrupar por fecha
                datos_por_fecha = {}
                for interv in (response.data or []):
                    fecha = interv.get('fecha_registro', '')[:10]
                    datos_por_fecha[fecha] = datos_por_fecha.get(fecha, 0) + 1

            else:
                logger.warning(f"⚠️ Tipo de evolución no reconocido: {tipo}")
                return []

            # Convertir a lista ordenada
            resultado = [
                {'fecha': fecha, 'valor': round(valor, 2) if tipo == "ingresos" else int(valor)}
                for fecha, valor in sorted(datos_por_fecha.items())
            ]

            logger.info(f"✅ Evolución temporal odontólogo obtenida: {len(resultado)} días")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo evolución temporal odontólogo: {e}")
            return []

    # ====================================================================
    # 👨‍💼 MÉTODOS PARA ADMINISTRADOR
    # ====================================================================

    async def get_consultas_por_estado(
        self,
        fecha: str  # "hoy", "semana", "mes", o fecha específica YYYY-MM-DD
    ) -> List[Dict[str, Any]]:
        """
        📊 Distribución de consultas por estado

        Args:
            fecha: "hoy", "semana", "mes", o fecha específica

        Returns:
            [
                {"estado": "en_espera", "cantidad": 8, "color": "#f59e0b"},
                {"estado": "en_atencion", "cantidad": 6, "color": "#3b82f6"},
                {"estado": "completada", "cantidad": 14, "color": "#10b981"},
                {"estado": "cancelada", "cantidad": 2, "color": "#ef4444"}
            ]
        """
        try:
            logger.info(f"📊 Obteniendo consultas por estado ({fecha})")

            # Determinar rango de fechas
            if fecha == "hoy":
                fecha_inicio = date.today().isoformat()
                fecha_fin = date.today().isoformat()
            elif fecha == "semana":
                hoy = date.today()
                fecha_inicio = (hoy - timedelta(days=hoy.weekday())).isoformat()
                fecha_fin = hoy.isoformat()
            elif fecha == "mes":
                fecha_inicio = date.today().replace(day=1).isoformat()
                fecha_fin = date.today().isoformat()
            else:
                # Fecha específica
                fecha_inicio = fecha
                fecha_fin = fecha

            # Query para cada estado
            estados = {
                'en_espera': '#f59e0b',
                'en_atencion': '#3b82f6',
                'completada': '#10b981',
                'cancelada': '#ef4444'
            }

            resultado = []

            for estado, color in estados.items():
                response = self.client.table('consulta').select(
                    'id', count='exact'
                ).eq('estado', estado).gte(
                    'fecha_llegada', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_llegada', f"{fecha_fin}T23:59:59"
                ).execute()

                resultado.append({
                    'estado': estado.replace('_', ' ').title(),
                    'cantidad': response.count or 0,
                    'color': color
                })

            logger.info(f"✅ Consultas por estado obtenidas")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo consultas por estado: {e}")
            return []

    async def get_consultas_tabla(
        self,
        filtros: Dict[str, Any],
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        📋 Tabla de consultas con filtros y paginación

        Args:
            filtros: {
                "fecha": "hoy" | "semana" | "mes",
                "odontologo_id": "uuid",
                "estado": "en_espera",
                "busqueda": "texto"
            }
            limit: Registros por página
            offset: Offset para paginación

        Returns:
            {
                "consultas": [...],
                "total": 24,
                "pagina_actual": 1,
                "total_paginas": 1
            }
        """
        try:
            logger.info(f"📋 Obteniendo tabla de consultas")

            # Determinar rango de fechas
            fecha = filtros.get('fecha', 'hoy')
            if fecha == "hoy":
                fecha_inicio = date.today().isoformat()
                fecha_fin = date.today().isoformat()
            elif fecha == "semana":
                hoy = date.today()
                fecha_inicio = (hoy - timedelta(days=hoy.weekday())).isoformat()
                fecha_fin = hoy.isoformat()
            elif fecha == "mes":
                fecha_inicio = date.today().replace(day=1).isoformat()
                fecha_fin = date.today().isoformat()
            else:
                fecha_inicio = filtros.get('fecha_inicio', date.today().isoformat())
                fecha_fin = filtros.get('fecha_fin', date.today().isoformat())

            # Construir query
            query = self.client.table('consulta').select(
                '''
                numero_consulta,
                fecha_llegada,
                estado,
                tipo_consulta,
                motivo_consulta,
                paciente:paciente_id(primer_nombre, primer_apellido, numero_historia),
                personal:primer_odontologo_id(primer_nombre, primer_apellido)
                ''',
                count='exact'
            ).gte(
                'fecha_llegada', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_llegada', f"{fecha_fin}T23:59:59"
            )

            # Aplicar filtros opcionales
            if filtros.get('odontologo_id'):
                query = query.eq('primer_odontologo_id', filtros['odontologo_id'])

            if filtros.get('estado'):
                query = query.eq('estado', filtros['estado'])

            # Ejecutar con paginación
            response = query.order(
                'fecha_llegada', desc=True
            ).range(offset, offset + limit - 1).execute()

            # Procesar datos
            consultas = []
            for consulta in (response.data or []):
                paciente_info = consulta.get('paciente', {})
                odontologo_info = consulta.get('personal', {})

                consultas.append({
                    'numero_consulta': consulta.get('numero_consulta', 'N/A'),
                    'fecha_llegada': consulta.get('fecha_llegada', ''),
                    'paciente_nombre': f"{paciente_info.get('primer_nombre', '')} {paciente_info.get('primer_apellido', '')}".strip() if paciente_info else 'N/A',
                    'paciente_hc': paciente_info.get('numero_historia', 'N/A') if paciente_info else 'N/A',
                    'odontologo_nombre': f"{odontologo_info.get('primer_nombre', '')} {odontologo_info.get('primer_apellido', '')}".strip() if odontologo_info else 'N/A',
                    'estado': consulta.get('estado', ''),
                    'tipo_consulta': consulta.get('tipo_consulta', ''),
                    'motivo_consulta': consulta.get('motivo_consulta', '')
                })

            # Calcular paginación
            total = response.count or 0
            pagina_actual = (offset // limit) + 1
            total_paginas = (total + limit - 1) // limit if total > 0 else 1

            resultado = {
                'consultas': consultas,
                'total': total,
                'pagina_actual': pagina_actual,
                'total_paginas': total_paginas
            }

            logger.info(f"✅ Tabla consultas: {len(consultas)} de {total}")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo tabla consultas: {e}")
            return {
                'consultas': [],
                'total': 0,
                'pagina_actual': 1,
                'total_paginas': 1
            }

    async def get_pagos_pendientes(self) -> List[Dict[str, Any]]:
        """
        💰 Lista de pagos pendientes con alertas por antigüedad

        Returns:
            [
                {
                    "recibo": "REC-001",
                    "paciente_nombre": "Ana García",
                    "paciente_hc": "0023",
                    "saldo_total": 450.00,
                    "fecha_pago": "2025-10-05",
                    "dias_pendientes": 33,
                    "alerta": "urgente"  # urgente (>30), pronto (15-30), normal (<15)
                },
                ...
            ]
        """
        try:
            logger.info("💰 Obteniendo pagos pendientes")

            # Query
            response = self.client.table('pago').select(
                '''
                numero_recibo,
                fecha_pago,
                saldo_pendiente_usd,
                saldo_pendiente_bs,
                paciente:paciente_id(primer_nombre, primer_apellido, numero_historia),
                consulta:consulta_id(numero_consulta)
                '''
            ).in_('estado_pago', ['pendiente', 'parcial']).order(
                'fecha_pago', desc=False
            ).execute()

            # Procesar datos
            pagos_pendientes = []
            hoy = date.today()

            for pago in (response.data or []):
                paciente_info = pago.get('paciente', {})
                saldo_total = (
                    float(pago.get('saldo_pendiente_usd', 0) or 0) +
                    float(pago.get('saldo_pendiente_bs', 0) or 0)
                )

                # Calcular días pendientes
                fecha_pago_str = pago.get('fecha_pago', '')
                if fecha_pago_str:
                    try:
                        fecha_pago = datetime.fromisoformat(fecha_pago_str.replace('Z', '+00:00')).date()
                        dias_pendientes = (hoy - fecha_pago).days
                    except:
                        dias_pendientes = 0
                else:
                    dias_pendientes = 0

                # Determinar nivel de alerta
                if dias_pendientes > 30:
                    alerta = "urgente"
                elif dias_pendientes >= 15:
                    alerta = "pronto"
                else:
                    alerta = "normal"

                pagos_pendientes.append({
                    'recibo': pago.get('numero_recibo', 'N/A'),
                    'paciente_nombre': f"{paciente_info.get('primer_nombre', '')} {paciente_info.get('primer_apellido', '')}".strip() if paciente_info else 'N/A',
                    'paciente_hc': paciente_info.get('numero_historia', 'N/A') if paciente_info else 'N/A',
                    'saldo_total': round(saldo_total, 2),
                    'fecha_pago': fecha_pago_str[:10] if fecha_pago_str else 'N/A',
                    'dias_pendientes': dias_pendientes,
                    'alerta': alerta
                })

            logger.info(f"✅ Pagos pendientes: {len(pagos_pendientes)}")

            return pagos_pendientes

        except Exception as e:
            logger.error(f"❌ Error obteniendo pagos pendientes: {e}")
            return []

    async def get_pacientes_nuevos_tiempo(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        📈 Pacientes nuevos por día en un rango de fechas

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            [
                {"fecha": "2025-11-01", "nuevos": 3},
                {"fecha": "2025-11-02", "nuevos": 5},
                ...
            ]
        """
        try:
            logger.info(f"📈 Obteniendo pacientes nuevos ({fecha_inicio} - {fecha_fin})")

            # Query
            response = self.client.table('paciente').select(
                'fecha_registro'
            ).eq('activo', True).gte(
                'fecha_registro', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_registro', f"{fecha_fin}T23:59:59"
            ).execute()

            # Agrupar por fecha
            pacientes_por_fecha = {}

            for paciente in (response.data or []):
                fecha_registro = paciente.get('fecha_registro', '')
                if fecha_registro:
                    # Extraer solo la fecha (YYYY-MM-DD)
                    fecha = fecha_registro[:10]
                    pacientes_por_fecha[fecha] = pacientes_por_fecha.get(fecha, 0) + 1

            # Convertir a lista y ordenar
            resultado = [
                {'fecha': fecha, 'nuevos': cantidad}
                for fecha, cantidad in pacientes_por_fecha.items()
            ]
            resultado.sort(key=lambda x: x['fecha'])

            logger.info(f"✅ Pacientes nuevos: {len(resultado)} días con registros")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo pacientes nuevos: {e}")
            return []

    async def get_distribucion_consultas_odontologo(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        📊 Distribución de consultas por odontólogo

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            [
                {
                    "odontologo": "Dr. García",
                    "total_consultas": 42,
                    "completadas": 38,
                    "pendientes": 4
                },
                ...
            ]
        """
        try:
            logger.info(f"📊 Obteniendo distribución consultas por odontólogo")

            # Query con JOIN
            response = self.client.table('consulta').select(
                'estado, personal:primer_odontologo_id(primer_nombre, primer_apellido)'
            ).gte(
                'fecha_llegada', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_llegada', f"{fecha_fin}T23:59:59"
            ).execute()

            # Agrupar por odontólogo
            odontologos = {}

            for consulta in (response.data or []):
                odontologo_info = consulta.get('personal', {})
                if not odontologo_info:
                    continue

                nombre = f"{odontologo_info.get('primer_nombre', '')} {odontologo_info.get('primer_apellido', '')}".strip()
                estado = consulta.get('estado', '')

                if nombre not in odontologos:
                    odontologos[nombre] = {
                        'odontologo': nombre,
                        'total_consultas': 0,
                        'completadas': 0,
                        'pendientes': 0
                    }

                odontologos[nombre]['total_consultas'] += 1

                if estado == 'completada':
                    odontologos[nombre]['completadas'] += 1
                elif estado in ['en_espera', 'en_atencion']:
                    odontologos[nombre]['pendientes'] += 1

            # Convertir a lista y ordenar
            resultado = list(odontologos.values())
            resultado.sort(key=lambda x: x['total_consultas'], reverse=True)

            logger.info(f"✅ Distribución consultas: {len(resultado)} odontólogos")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo distribución consultas: {e}")
            return []

    async def get_tipos_consulta_distribucion(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        🏷️ Distribución de tipos de consulta

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            [
                {"tipo": "General", "cantidad": 80, "porcentaje": 65.0},
                {"tipo": "Control", "cantidad": 25, "porcentaje": 20.3},
                {"tipo": "Urgencia", "cantidad": 12, "porcentaje": 9.8},
                {"tipo": "Emergencia", "cantidad": 6, "porcentaje": 4.9}
            ]
        """
        try:
            logger.info(f"🏷️ Obteniendo distribución tipos de consulta")

            # Query
            response = self.client.table('consulta').select(
                'tipo_consulta'
            ).gte(
                'fecha_llegada', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_llegada', f"{fecha_fin}T23:59:59"
            ).execute()

            # Agrupar por tipo
            tipos = {}
            for consulta in (response.data or []):
                tipo = consulta.get('tipo_consulta', 'general')
                tipos[tipo] = tipos.get(tipo, 0) + 1

            # Convertir a lista
            total = sum(tipos.values())
            resultado = [
                {
                    'tipo': tipo.title(),
                    'cantidad': cantidad,
                    'porcentaje': round((cantidad / total * 100) if total > 0 else 0, 1)
                }
                for tipo, cantidad in tipos.items()
            ]
            resultado.sort(key=lambda x: x['cantidad'], reverse=True)

            logger.info(f"✅ Distribución tipos consulta: {len(resultado)} tipos")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo distribución tipos consulta: {e}")
            return []

    # ====================================================================
    # 👨‍💼 MÉTODOS PARA ADMINISTRADOR - DATOS FINANCIEROS Y EVOLUTIVOS
    # ====================================================================

    async def get_dashboard_cards_admin(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, Any]:
        """
        💰 Cards financieros del dashboard del administrador (4 cards)

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            {
                "ingresos_periodo": 15450.75,
                "pagos_realizados": 23,
                "saldo_pendiente": 3200.50,
                "metodo_mas_usado": "Efectivo"
            }
        """
        try:
            logger.info(f"💰 Obteniendo cards dashboard admin ({fecha_inicio} - {fecha_fin})")

            # 1. Ingresos del período (solo USD)
            ingresos_response = self.client.table('pago').select(
                'monto_pagado_usd'
            ).eq('estado_pago', 'completado').gte(
                'fecha_pago', f"{fecha_inicio}T00:00:00"
            ).lte(
                'fecha_pago', f"{fecha_fin}T23:59:59"
            ).execute()

            ingresos_total = sum(
                float(p.get('monto_pagado_usd', 0) or 0)
                for p in ingresos_response.data
            ) if ingresos_response.data else 0

            # 2. Pagos realizados (cantidad)
            pagos_realizados = len(ingresos_response.data) if ingresos_response.data else 0

            # 3. Saldo pendiente (solo USD)
            pendientes_response = self.client.table('pago').select(
                'saldo_pendiente_usd'
            ).in_('estado_pago', ['pendiente', 'parcial']).execute()

            saldo_pendiente = sum(
                float(p.get('saldo_pendiente_usd', 0) or 0)
                for p in pendientes_response.data
            ) if pendientes_response.data else 0

            # 4. Método más usado
            metodos_count = {}
            for pago in ingresos_response.data if ingresos_response.data else []:
                metodos = pago.get('metodos_pago', [])
                if not metodos or not isinstance(metodos, list):
                    metodos = ["efectivo"]

                for metodo in metodos:
                    metodo_nombre = str(metodo).lower().replace('_', ' ').title()
                    metodos_count[metodo_nombre] = metodos_count.get(metodo_nombre, 0) + 1

            metodo_mas_usado = max(metodos_count.items(), key=lambda x: x[1])[0] if metodos_count else "Efectivo"

            resultado = {
                'ingresos_periodo': round(ingresos_total, 2),
                'pagos_realizados': pagos_realizados,
                'saldo_pendiente': round(saldo_pendiente, 2),
                'metodo_mas_usado': metodo_mas_usado
            }

            logger.info(f"✅ Cards admin: ${ingresos_total:.2f} ingresos, {pagos_realizados} pagos")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo cards admin: {e}")
            return {
                'ingresos_periodo': 0,
                'pagos_realizados': 0,
                'saldo_pendiente': 0,
                'metodo_mas_usado': "N/A"
            }

    async def get_metodos_pago_admin(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> List[Dict[str, Any]]:
        """
        💳 Métodos de pago más usados (ADMINISTRADOR)

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            [
                {
                    "metodo": "Efectivo",
                    "veces_usado": 234,
                    "monto_total": 12450.00,
                    "porcentaje": 45.2
                },
                ...
            ]
        """
        # Reutilizar la lógica del método existente
        return await self.get_metodos_pago_populares(fecha_inicio, fecha_fin)

    async def get_distribucion_pagos_admin(
        self,
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict[str, float]:
        """
        💵 Distribución de pagos USD vs BS (ADMINISTRADOR)

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD

        Returns:
            {
                "total_usd": 4357.75,
                "total_bs": 8092.25,
                "porcentaje_usd": 35.0,
                "porcentaje_bs": 65.0
            }
        """
        # Reutilizar la lógica del método existente
        return await self.get_distribucion_pagos_usd_bs(fecha_inicio, fecha_fin)

    async def get_evolucion_temporal_admin(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        tipo: str  # "consultas", "ingresos", "pacientes_nuevos"
    ) -> List[Dict[str, Any]]:
        """
        📈 Evolución temporal para gráficos con tabs (ADMINISTRADOR)

        Args:
            fecha_inicio: Fecha inicio formato YYYY-MM-DD
            fecha_fin: Fecha fin formato YYYY-MM-DD
            tipo: "consultas", "ingresos", "pacientes_nuevos"

        Returns:
            [
                {"fecha": "2024-01-01", "valor": 15, "label": "15 Consultas"},
                {"fecha": "2024-01-02", "valor": 22, "label": "22 Consultas"},
                ...
            ]
        """
        try:
            logger.info(f"📈 Obteniendo evolución temporal admin: {tipo} ({fecha_inicio} - {fecha_fin})")

            if tipo == "consultas":
                # Consultas por día
                response = self.client.table('consulta').select(
                    'fecha_llegada, estado'
                ).gte(
                    'fecha_llegada', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_llegada', f"{fecha_fin}T23:59:59"
                ).execute()

                # Agrupar por fecha
                consultas_por_fecha = {}
                for consulta in response.data if response.data else []:
                    fecha = consulta.get('fecha_llegada', '')[:10]  # YYYY-MM-DD
                    consultas_por_fecha[fecha] = consultas_por_fecha.get(fecha, 0) + 1

                resultado = [
                    {
                        'fecha': fecha,
                        'valor': cantidad,
                        'label': f"{cantidad} {'Consulta' if cantidad == 1 else 'Consultas'}"
                    }
                    for fecha, cantidad in sorted(consultas_por_fecha.items())
                ]

            elif tipo == "ingresos":
                # Ingresos por día (solo USD)
                response = self.client.table('pago').select(
                    'fecha_pago, monto_pagado_usd'
                ).eq('estado_pago', 'completado').gte(
                    'fecha_pago', f"{fecha_inicio}T00:00:00"
                ).lte(
                    'fecha_pago', f"{fecha_fin}T23:59:59"
                ).execute()

                # Agrupar por fecha
                ingresos_por_fecha = {}
                for pago in response.data if response.data else []:
                    fecha = pago.get('fecha_pago', '')[:10]  # YYYY-MM-DD
                    monto = float(pago.get('monto_pagado_usd', 0) or 0)
                    ingresos_por_fecha[fecha] = ingresos_por_fecha.get(fecha, 0) + monto

                resultado = [
                    {
                        'fecha': fecha,
                        'valor': round(monto, 2),
                        'label': f"${monto:,.2f}"
                    }
                    for fecha, monto in sorted(ingresos_por_fecha.items())
                ]

            elif tipo == "pacientes_nuevos":
                # Pacientes nuevos por día (usar fecha_registro, no created_at)
                response = self.client.table('paciente').select(
                    'fecha_registro'
                ).gte(
                    'fecha_registro', f"{fecha_inicio}"
                ).lte(
                    'fecha_registro', f"{fecha_fin}"
                ).execute()

                # Agrupar por fecha
                pacientes_por_fecha = {}
                for paciente in response.data if response.data else []:
                    fecha_str = paciente.get('fecha_registro', '')
                    # Manejar fecha_registro como DATE (YYYY-MM-DD), no TIMESTAMP
                    if fecha_str:
                        fecha = fecha_str if len(fecha_str) == 10 else fecha_str[:10]
                        pacientes_por_fecha[fecha] = pacientes_por_fecha.get(fecha, 0) + 1

                resultado = [
                    {
                        'fecha': fecha,
                        'valor': cantidad,
                        'label': f"{cantidad} {'Paciente' if cantidad == 1 else 'Pacientes'}"
                    }
                    for fecha, cantidad in sorted(pacientes_por_fecha.items())
                ]

            else:
                logger.warning(f"⚠️ Tipo de evolución no reconocido: {tipo}")
                return []

            logger.info(f"✅ Evolución {tipo}: {len(resultado)} puntos de datos")

            return resultado

        except Exception as e:
            logger.error(f"❌ Error obteniendo evolución temporal admin ({tipo}): {e}")
            return []


# Instancia única para importar
reportes_service = ReportesService()
