"""
📊 ESTADO DE REPORTES
Maneja el estado de los reportes diferenciados por rol

CARACTERÍSTICAS:
- Estados separados por rol (Gerente, Odontólogo, Administrador)
- Filtros de fecha con presets
- Paginación para tablas
- Carga asíncrona de datos
- Actualización manual con botón refresh
"""

import reflex as rx
from typing import Dict, Any, List, Optional, Union
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class EstadoReportes(rx.State,mixin=True):
    """
    Estado que maneja todos los reportes del sistema
    """

    # ====================================================================
    # 🔄 ESTADOS COMUNES
    # ====================================================================

    cargando_reportes: bool = False
    filtro_fecha: str = "mes"  # "hoy", "semana", "mes", "30_dias", "3_meses", "año", "custom"
    fecha_inicio_custom: str = ""
    fecha_fin_custom: str = ""

    # ====================================================================
    # 👔 ESTADOS PARA GERENTE
    # ====================================================================

    # Distribución pagos USD vs BS
    distribucion_pagos: Dict[str, float] = {}

    # Ranking de servicios
    ranking_servicios: List[Dict[str, Any]] = []

    # Ranking de odontólogos
    ranking_odontologos: List[Dict[str, Any]] = []
    ordenar_odontologos_por: str = "intervenciones"  # "intervenciones" o "ingresos"

    # Estadísticas de pacientes
    estadisticas_pacientes: Dict[str, Any] = {}

    # Métodos de pago
    metodos_pago_populares: List[Dict[str, Any]] = []

    # 📊 NUEVOS: Cards del dashboard completo
    dashboard_cards_gerente: Dict[str, Any] = {}

    # 📈 NUEVOS: Evolución temporal para gráficos con tabs
    evolucion_temporal_pacientes: List[Dict[str, Any]] = []
    evolucion_temporal_consultas: List[Dict[str, Any]] = []
    evolucion_temporal_ingresos: List[Dict[str, Any]] = []
    tab_grafico_activo: str = "pacientes_nuevos"  # "pacientes_nuevos", "consultas", "ingresos"

    # ====================================================================
    # 🦷 ESTADOS PARA ODONTÓLOGO
    # ====================================================================

    # 📊 NUEVOS: Cards del dashboard completo (7 cards)
    dashboard_cards_odontologo: Dict[str, Any] = {}

    # 📈 NUEVOS: Evolución temporal para gráficos con tabs
    evolucion_temporal_ingresos_odontologo: List[Dict[str, Any]] = []
    evolucion_temporal_intervenciones_odontologo: List[Dict[str, Any]] = []
    tab_grafico_odontologo: str = "ingresos"  # "ingresos", "intervenciones"

    # 💳 NUEVO: Métodos de pago del odontólogo
    metodos_pago_odontologo: List[Dict[str, Any]] = []

    # Distribución ingresos propios USD vs BS
    distribucion_ingresos_odontologo: Dict[str, float] = {}

    # Ranking servicios propios
    ranking_servicios_odontologo: List[Dict[str, Any]] = []

    # Tabla de intervenciones
    intervenciones_odontologo: List[Dict[str, Any]] = []
    total_intervenciones: int = 0
    pagina_actual_intervenciones: int = 1
    total_paginas_intervenciones: int = 1
    busqueda_intervenciones_odontologo: str = ""  # Búsqueda en tabla intervenciones

    # Estadísticas odontograma
    estadisticas_odontograma: Dict[str, Any] = {}

    # ====================================================================
    # 👨‍💼 ESTADOS PARA ADMINISTRADOR
    # ====================================================================

    # Consultas por estado
    consultas_por_estado_dash: List[Dict[str, Any]] = []

    # Tabla de consultas
    consultas_tabla: List[Dict[str, Any]] = []
    total_consultas: int = 0
    pagina_actual_consultas: int = 1
    total_paginas_consultas: int = 1
    busqueda_consultas_admin: str = ""  # Búsqueda en tabla consultas
    filtro_consulta_estado: str = ""  # Filtro opcional
    filtro_consulta_odontologo: str = ""  # Filtro opcional

    # Pagos pendientes
    pagos_pendientes: List[Dict[str, Any]] = []

    # Pacientes nuevos en el tiempo
    pacientes_nuevos_tiempo: List[Dict[str, Any]] = []

    # Distribución consultas por odontólogo
    distribucion_consultas_odontologo: List[Dict[str, Any]] = []

    # Tipos de consulta
    tipos_consulta_distribucion: List[Dict[str, Any]] = []

    # 💰 NUEVOS: Datos financieros para administrador
    dashboard_cards_admin: Dict[str, Any] = {}
    metodos_pago_admin: List[Dict[str, Any]] = []
    distribucion_pagos_admin: Dict[str, float] = {}

    # 📈 NUEVOS: Evolución temporal para gráficos con tabs (administrador)
    evolucion_temporal_consultas_admin: List[Dict[str, Any]] = []
    evolucion_temporal_ingresos_admin: List[Dict[str, Any]] = []
    evolucion_temporal_pacientes_admin: List[Dict[str, Any]] = []
    tab_grafico_admin: str = "consultas"  # "consultas", "ingresos", "pacientes_nuevos"

    # 📊 DASHBOARD HOY - Métricas en tiempo real (administrador)
    dashboard_stats_admin: Dict[str, Any] = {}
    consultas_hoy_por_estado_admin: List[Dict[str, Any]] = []
    consultas_hoy_por_odontologo_admin: List[Dict[str, Any]] = []
    cargando_dashboard_admin: bool = False

    # 📊 DASHBOARD HOY - Métricas básicas para asistente (solo lectura)
    dashboard_stats_asistente: Dict[str, Any] = {}
    cargando_dashboard_asistente: bool = False

    # ====================================================================
    # 🔧 MÉTODOS AUXILIARES
    # ====================================================================

    def _get_rango_fechas(self) -> tuple[str, str]:
        """
        Obtiene el rango de fechas según el filtro seleccionado

        Returns:
            (fecha_inicio, fecha_fin) en formato YYYY-MM-DD
        """
        hoy = date.today()

        if self.filtro_fecha == "hoy":
            return (hoy.isoformat(), hoy.isoformat())

        elif self.filtro_fecha == "semana":
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            return (inicio_semana.isoformat(), hoy.isoformat())

        elif self.filtro_fecha == "mes":
            inicio_mes = hoy.replace(day=1)
            return (inicio_mes.isoformat(), hoy.isoformat())

        elif self.filtro_fecha == "30_dias":
            hace_30_dias = hoy - timedelta(days=30)
            return (hace_30_dias.isoformat(), hoy.isoformat())

        elif self.filtro_fecha == "3_meses":
            hace_3_meses = hoy - timedelta(days=90)
            return (hace_3_meses.isoformat(), hoy.isoformat())

        elif self.filtro_fecha == "año":
            inicio_año = hoy.replace(month=1, day=1)
            return (inicio_año.isoformat(), hoy.isoformat())

        elif self.filtro_fecha == "custom":
            if self.fecha_inicio_custom and self.fecha_fin_custom:
                return (self.fecha_inicio_custom, self.fecha_fin_custom)
            else:
                # Fallback a mes actual
                inicio_mes = hoy.replace(day=1)
                return (inicio_mes.isoformat(), hoy.isoformat())

        else:
            # Fallback a mes actual
            inicio_mes = hoy.replace(day=1)
            return (inicio_mes.isoformat(), hoy.isoformat())

    async def set_filtro_fecha(self, nuevo_filtro: str):
        """
        Cambia el filtro de fecha y recarga los reportes

        Args:
            nuevo_filtro: "hoy", "semana", "mes", "30_dias", "3_meses", "año", "custom"
        """
        logger.info(f"📅 Cambiando filtro de fecha a: {nuevo_filtro}")
        self.filtro_fecha = nuevo_filtro

        # Recargar reportes según el rol
        await self.cargar_reportes_por_rol()

    async def set_fecha_custom(self, fecha_inicio: str, fecha_fin: str):
        """
        Establece rango de fechas personalizado

        Args:
            fecha_inicio: Fecha inicio YYYY-MM-DD
            fecha_fin: Fecha fin YYYY-MM-DD
        """
        self.fecha_inicio_custom = fecha_inicio
        self.fecha_fin_custom = fecha_fin
        self.filtro_fecha = "custom"

        # Recargar reportes
        await self.cargar_reportes_por_rol()

    # ====================================================================
    # 👔 MÉTODOS PARA CARGAR DATOS - GERENTE
    # ====================================================================

    async def cargar_reportes_gerente(self):
        """
        Carga todos los reportes para el rol Gerente
        """
        try:
            logger.info("👔 Cargando reportes para Gerente")
            self.cargando_reportes = True

            from dental_system.services.reportes_service import reportes_service

            # Obtener rango de fechas
            fecha_inicio, fecha_fin = self._get_rango_fechas()

            # Cargar datos en paralelo (simulado con await secuencial por ahora)
            # En producción, podrías usar asyncio.gather para cargar en paralelo

            # 📊 NUEVO: Cards del dashboard completo (8 cards en uno)
            self.dashboard_cards_gerente = await reportes_service.get_dashboard_cards_gerente(
                fecha_inicio, fecha_fin
            )

            # 1. Distribución pagos USD vs BS
            self.distribucion_pagos = await reportes_service.get_distribucion_pagos_usd_bs(
                fecha_inicio, fecha_fin
            )

            # 2. Ranking de servicios
            self.ranking_servicios = await reportes_service.get_ranking_servicios(
                fecha_inicio, fecha_fin, limit=10
            )

            # 3. Ranking de odontólogos
            self.ranking_odontologos = await reportes_service.get_ranking_odontologos(
                fecha_inicio, fecha_fin, ordenar_por=self.ordenar_odontologos_por
            )

            # 4. Estadísticas de pacientes
            self.estadisticas_pacientes = await reportes_service.get_estadisticas_pacientes()

            # 5. Métodos de pago
            self.metodos_pago_populares = await reportes_service.get_metodos_pago_populares(
                fecha_inicio, fecha_fin
            )

            # 📈 NUEVO: Evolución temporal para gráficos con tabs
            self.evolucion_temporal_pacientes = await reportes_service.get_evolucion_temporal(
                fecha_inicio, fecha_fin, "pacientes_nuevos"
            )
            self.evolucion_temporal_consultas = await reportes_service.get_evolucion_temporal(
                fecha_inicio, fecha_fin, "consultas"
            )
            self.evolucion_temporal_ingresos = await reportes_service.get_evolucion_temporal(
                fecha_inicio, fecha_fin, "ingresos"
            )

            logger.info("✅ Reportes de Gerente cargados exitosamente")

        except Exception as e:
            logger.error(f"❌ Error cargando reportes de Gerente: {e}")
        finally:
            self.cargando_reportes = False

    async def cambiar_ordenamiento_odontologos(self, nuevo_orden: str):
        """
        Cambia el ordenamiento del ranking de odontólogos

        Args:
            nuevo_orden: "intervenciones" o "ingresos"
        """
        logger.info(f"📊 Cambiando ordenamiento odontólogos a: {nuevo_orden}")
        self.ordenar_odontologos_por = nuevo_orden

        # Recargar solo el ranking de odontólogos
        from dental_system.services.reportes_service import reportes_service
        fecha_inicio, fecha_fin = self._get_rango_fechas()

        self.ranking_odontologos = await reportes_service.get_ranking_odontologos(
            fecha_inicio, fecha_fin, ordenar_por=nuevo_orden
        )

    # ====================================================================
    # 🦷 MÉTODOS PARA CARGAR DATOS - ODONTÓLOGO
    # ====================================================================

    async def cargar_reportes_odontologo(self):
        """
        Carga todos los reportes para el rol Odontólogo
        """
        try:
            logger.info("🦷 Cargando reportes para Odontólogo")
            self.cargando_reportes = True

            from dental_system.services.reportes_service import reportes_service

            # Obtener ID del odontólogo desde el estado de auth
            odontologo_id = self.get_personal_id_from_auth()
            if not odontologo_id:
                logger.warning("⚠️ No se pudo obtener ID del odontólogo")
                return

            # Obtener rango de fechas
            fecha_inicio, fecha_fin = self._get_rango_fechas()

            # 📊 NUEVO: Cards del dashboard completo (7 cards en uno)
            self.dashboard_cards_odontologo = await reportes_service.get_dashboard_cards_odontologo(
                odontologo_id, fecha_inicio, fecha_fin
            )

            # 1. Distribución ingresos USD vs BS
            self.distribucion_ingresos_odontologo = await reportes_service.get_ingresos_odontologo_usd_bs(
                odontologo_id, fecha_inicio, fecha_fin
            )

            # 2. Ranking servicios propios
            self.ranking_servicios_odontologo = await reportes_service.get_ranking_servicios_odontologo(
                odontologo_id, fecha_inicio, fecha_fin, limit=10
            )

            # 💳 NUEVO: Métodos de pago del odontólogo
            self.metodos_pago_odontologo = await reportes_service.get_metodos_pago_odontologo(
                odontologo_id, fecha_inicio, fecha_fin
            )

            # 3. Tabla de intervenciones (primera página)
            resultado_intervenciones = await reportes_service.get_intervenciones_odontologo(
                odontologo_id,
                filtros={"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin},
                limit=50,
                offset=0
            )
            self.intervenciones_odontologo = resultado_intervenciones.get('intervenciones', [])
            self.total_intervenciones = resultado_intervenciones.get('total', 0)
            self.pagina_actual_intervenciones = resultado_intervenciones.get('pagina_actual', 1)
            self.total_paginas_intervenciones = resultado_intervenciones.get('total_paginas', 1)

            # 4. Estadísticas del odontograma
            self.estadisticas_odontograma = await reportes_service.get_estadisticas_odontograma_odontologo(
                odontologo_id, fecha_inicio, fecha_fin
            )

            # 📈 NUEVO: Evolución temporal para gráficos con tabs
            self.evolucion_temporal_ingresos_odontologo = await reportes_service.get_evolucion_temporal_odontologo(
                odontologo_id, fecha_inicio, fecha_fin, "ingresos"
            )
            self.evolucion_temporal_intervenciones_odontologo = await reportes_service.get_evolucion_temporal_odontologo(
                odontologo_id, fecha_inicio, fecha_fin, "intervenciones"
            )

            logger.info("✅ Reportes de Odontólogo cargados exitosamente")

        except Exception as e:
            logger.error(f"❌ Error cargando reportes de Odontólogo: {e}")
        finally:
            self.cargando_reportes = False

    async def cargar_pagina_intervenciones(self, pagina: int):
        """
        Carga una página específica de intervenciones

        Args:
            pagina: Número de página (1-indexed)
        """
        try:
            from dental_system.services.reportes_service import reportes_service

            odontologo_id = self.get_personal_id_from_auth()
            if not odontologo_id:
                return

            fecha_inicio, fecha_fin = self._get_rango_fechas()

            # Calcular offset
            limit = 50
            offset = (pagina - 1) * limit

            resultado = await reportes_service.get_intervenciones_odontologo(
                odontologo_id,
                filtros={"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin},
                limit=limit,
                offset=offset
            )

            self.intervenciones_odontologo = resultado.get('intervenciones', [])
            self.pagina_actual_intervenciones = resultado.get('pagina_actual', 1)

        except Exception as e:
            logger.error(f"❌ Error cargando página de intervenciones: {e}")

    def get_personal_id_from_auth(self) -> Optional[str]:
        """
        Obtiene el ID del personal desde el estado de autenticación

        Returns:
            UUID del personal o None
        """
        try:
            # EstadoReportes hereda de AppState que incluye EstadoAuth
            # Por lo tanto, tenemos acceso directo a id_personal
            return self.id_personal if hasattr(self, 'id_personal') else None

        except Exception as e:
            logger.error(f"❌ Error obteniendo personal_id: {e}")
            return None

    # ====================================================================
    # 👨‍💼 MÉTODOS PARA CARGAR DATOS - ADMINISTRADOR
    # ====================================================================

    async def cargar_reportes_administrador(self):
        """
        Carga todos los reportes para el rol Administrador
        """
        try:
            logger.info("👨‍💼 Cargando reportes para Administrador")
            self.cargando_reportes = True

            from dental_system.services.reportes_service import reportes_service

            # Obtener rango de fechas
            fecha_inicio, fecha_fin = self._get_rango_fechas()

            # 1. Consultas por estado (hoy por defecto)
            self.consultas_por_estado_dash = await reportes_service.get_consultas_por_estado("hoy")

            # 2. Tabla de consultas (primera página)
            resultado_consultas = await reportes_service.get_consultas_tabla(
                filtros={
                    "fecha": self.filtro_fecha,
                    "estado": self.filtro_consulta_estado,
                    "odontologo_id": self.filtro_consulta_odontologo
                },
                limit=50,
                offset=0
            )
            self.consultas_tabla = resultado_consultas.get('consultas', [])
            self.total_consultas = resultado_consultas.get('total', 0)
            self.pagina_actual_consultas = resultado_consultas.get('pagina_actual', 1)
            self.total_paginas_consultas = resultado_consultas.get('total_paginas', 1)

            # 3. Pagos pendientes
            self.pagos_pendientes = await reportes_service.get_pagos_pendientes()

            # 4. Pacientes nuevos en el tiempo
            self.pacientes_nuevos_tiempo = await reportes_service.get_pacientes_nuevos_tiempo(
                fecha_inicio, fecha_fin
            )

            # 5. Distribución consultas por odontólogo
            self.distribucion_consultas_odontologo = await reportes_service.get_distribucion_consultas_odontologo(
                fecha_inicio, fecha_fin
            )

            # 6. Tipos de consulta
            self.tipos_consulta_distribucion = await reportes_service.get_tipos_consulta_distribucion(
                fecha_inicio, fecha_fin
            )

            # 💰 NUEVOS: Datos financieros
            # 7. Cards del dashboard completo (4 cards financieros)
            self.dashboard_cards_admin = await reportes_service.get_dashboard_cards_admin(
                fecha_inicio, fecha_fin
            )

            # 8. Métodos de pago
            self.metodos_pago_admin = await reportes_service.get_metodos_pago_admin(
                fecha_inicio, fecha_fin
            )

            # 9. Distribución pagos USD vs BS
            self.distribucion_pagos_admin = await reportes_service.get_distribucion_pagos_admin(
                fecha_inicio, fecha_fin
            )

            # 📈 NUEVOS: Evolución temporal para gráficos con tabs
            # 10. Evolución de consultas
            self.evolucion_temporal_consultas_admin = await reportes_service.get_evolucion_temporal_admin(
                fecha_inicio, fecha_fin, "consultas"
            )

            # 11. Evolución de ingresos
            self.evolucion_temporal_ingresos_admin = await reportes_service.get_evolucion_temporal_admin(
                fecha_inicio, fecha_fin, "ingresos"
            )

            # 12. Evolución de pacientes nuevos
            self.evolucion_temporal_pacientes_admin = await reportes_service.get_evolucion_temporal_admin(
                fecha_inicio, fecha_fin, "pacientes_nuevos"
            )

            logger.info("✅ Reportes de Administrador cargados exitosamente")

        except Exception as e:
            logger.error(f"❌ Error cargando reportes de Administrador: {e}")
        finally:
            self.cargando_reportes = False

    async def cargar_pagina_consultas(self, pagina: int):
        """
        Carga una página específica de consultas

        Args:
            pagina: Número de página (1-indexed)
        """
        try:
            from dental_system.services.reportes_service import reportes_service

            # Calcular offset
            limit = 50
            offset = (pagina - 1) * limit

            resultado = await reportes_service.get_consultas_tabla(
                filtros={
                    "fecha": self.filtro_fecha,
                    "estado": self.filtro_consulta_estado,
                    "odontologo_id": self.filtro_consulta_odontologo
                },
                limit=limit,
                offset=offset
            )

            self.consultas_tabla = resultado.get('consultas', [])
            self.pagina_actual_consultas = resultado.get('pagina_actual', 1)

        except Exception as e:
            logger.error(f"❌ Error cargando página de consultas: {e}")

    async def aplicar_filtro_consultas(self, estado: str = "", odontologo_id: str = ""):
        """
        Aplica filtros a la tabla de consultas y recarga

        Args:
            estado: Estado de consulta (vacío = todos)
            odontologo_id: ID del odontólogo (vacío = todos)
        """
        self.filtro_consulta_estado = estado
        self.filtro_consulta_odontologo = odontologo_id

        # Recargar primera página con filtros
        await self.cargar_pagina_consultas(1)

    # ====================================================================
    # 🔄 MÉTODOS PRINCIPALES
    # ====================================================================

    async def cargar_reportes_por_rol(self):
        """
        Carga los reportes según el rol del usuario actual

        Este método se llama desde la página de reportes al montar
        y cuando se cambia el filtro de fecha
        """
        try:
            # Obtener rol del usuario desde el estado de auth
            # Placeholder - ajustar según estructura real
            rol_usuario = self.get_rol_usuario()

            if rol_usuario == "gerente":
                await self.cargar_reportes_gerente()
            elif rol_usuario == "odontologo":
                await self.cargar_reportes_odontologo()
            elif rol_usuario == "administrador":
                await self.cargar_reportes_administrador()
            else:
                logger.warning(f"⚠️ Rol no reconocido para reportes: {rol_usuario}")

        except Exception as e:
            logger.error(f"❌ Error cargando reportes por rol: {e}")

    def get_rol_usuario(self) -> str:
        """
        Obtiene el rol del usuario actual desde el estado de auth

        Returns:
            "gerente", "odontologo", "administrador", o ""
        """
        try:
            # EstadoReportes hereda de AppState que incluye EstadoAuth
            # Por lo tanto, tenemos acceso directo a rol_usuario
            return self.rol_usuario if hasattr(self, 'rol_usuario') else ""

        except Exception as e:
            logger.error(f"❌ Error obteniendo rol de usuario: {e}")
            return ""

    async def actualizar_reportes(self):
        """
        Actualiza los reportes manualmente (botón de refresh)
        """
        logger.info("🔄 Actualizando reportes manualmente")
        await self.cargar_reportes_por_rol()

    # ====================================================================
    # 📄 MÉTODOS DE PAGINACIÓN Y BÚSQUEDA
    # ====================================================================

    async def pagina_siguiente_intervenciones(self):
        """
        Navega a la siguiente página de intervenciones del odontólogo
        """
        if self.pagina_actual_intervenciones < self.total_paginas_intervenciones:
            await self.cargar_pagina_intervenciones(self.pagina_actual_intervenciones + 1)

    async def pagina_anterior_intervenciones(self):
        """
        Navega a la página anterior de intervenciones del odontólogo
        """
        if self.pagina_actual_intervenciones > 1:
            await self.cargar_pagina_intervenciones(self.pagina_actual_intervenciones - 1)

    async def pagina_siguiente_consultas(self):
        """
        Navega a la siguiente página de consultas del administrador
        """
        if self.pagina_actual_consultas < self.total_paginas_consultas:
            await self.cargar_pagina_consultas(self.pagina_actual_consultas + 1)

    async def pagina_anterior_consultas(self):
        """
        Navega a la página anterior de consultas del administrador
        """
        if self.pagina_actual_consultas > 1:
            await self.cargar_pagina_consultas(self.pagina_actual_consultas - 1)

    async def cambiar_orden_ranking_odontologos(self, nuevo_orden: Union[str, List[str]]):
        """
        Alias para cambiar_ordenamiento_odontologos (compatibilidad)

        Args:
            nuevo_orden: "intervenciones" o "ingresos" (puede ser str o List[str])
        """
        # Normalizar: si es lista, tomar primer elemento
        orden = nuevo_orden[0] if isinstance(nuevo_orden, list) else nuevo_orden
        await self.cambiar_ordenamiento_odontologos(orden)

    def cambiar_tab_grafico(self, nuevo_tab: Union[str, List[str]]):
        """
        Cambia el tab activo del gráfico de evolución temporal (GERENTE)

        Args:
            nuevo_tab: "pacientes_nuevos", "consultas", o "ingresos" (puede ser str o List[str])
        """
        # Normalizar: si es lista, tomar primer elemento
        tab = nuevo_tab[0] if isinstance(nuevo_tab, list) else nuevo_tab
        logger.info(f"📊 Cambiando tab de gráfico gerente a: {tab}")
        self.tab_grafico_activo = tab

    def cambiar_tab_grafico_odontologo(self, nuevo_tab: Union[str, List[str]]):
        """
        Cambia el tab activo del gráfico de evolución temporal (ODONTÓLOGO)

        Args:
            nuevo_tab: "ingresos", "intervenciones" (puede ser str o List[str])
        """
        # Normalizar: si es lista, tomar primer elemento
        tab = nuevo_tab[0] if isinstance(nuevo_tab, list) else nuevo_tab
        logger.info(f"📊 Cambiando tab de gráfico odontólogo a: {tab}")
        self.tab_grafico_odontologo = tab

    def cambiar_tab_grafico_admin(self, nuevo_tab: Union[str, List[str]]):
        """
        Cambia el tab activo del gráfico de evolución temporal (ADMINISTRADOR)

        Args:
            nuevo_tab: "consultas", "ingresos", "pacientes_nuevos" (puede ser str o List[str])
        """
        # Normalizar: si es lista, tomar primer elemento
        tab = nuevo_tab[0] if isinstance(nuevo_tab, list) else nuevo_tab
        logger.info(f"📊 Cambiando tab de gráfico administrador a: {tab}")
        self.tab_grafico_admin = tab

    # ====================================================================
    # 📊 COMPUTED VARS (Propiedades calculadas)
    # ====================================================================

    @rx.var
    def estadisticas_pacientes_gerente(self) -> Dict[str, Any]:
        """
        Alias para estadisticas_pacientes (compatibilidad con la página)
        """
        return self.estadisticas_pacientes

    @rx.var
    def estadisticas_odontograma_odontologo(self) -> Dict[str, Any]:
        """
        Alias para estadisticas_odontograma (compatibilidad con la página)
        """
        return self.estadisticas_odontograma

    async def cargar_reportes_completos(self):
        """
        Alias para cargar_reportes_por_rol (compatibilidad con la página)
        """
        await self.cargar_reportes_por_rol()

    @rx.var
    def tiene_datos_gerente(self) -> bool:
        """Indica si hay datos cargados para el reporte de gerente"""
        return bool(self.distribucion_pagos or self.ranking_servicios)

    @rx.var
    def tiene_datos_odontologo(self) -> bool:
        """Indica si hay datos cargados para el reporte de odontólogo"""
        return bool(self.distribucion_ingresos_odontologo or self.ranking_servicios_odontologo)

    @rx.var
    def tiene_datos_administrador(self) -> bool:
        """Indica si hay datos cargados para el reporte de administrador"""
        return bool(self.consultas_por_estado_dash or self.consultas_tabla)

    @rx.var
    def total_pagos_pendientes_monto(self) -> float:
        """Suma total de pagos pendientes"""
        return sum(p.get('saldo_total', 0) for p in self.pagos_pendientes)

    @rx.var
    def total_pagos_urgentes(self) -> int:
        """Cantidad de pagos con alerta urgente (>30 días)"""
        return sum(1 for p in self.pagos_pendientes if p.get('alerta') == 'urgente')

    @rx.var
    def nombre_filtro_fecha_actual(self) -> str:
        """Nombre legible del filtro de fecha actual"""
        nombres = {
            "hoy": "Hoy",
            "semana": "Esta Semana",
            "mes": "Este Mes",
            "30_dias": "Últimos 30 Días",
            "3_meses": "Últimos 3 Meses",
            "año": "Este Año",
            "custom": "Rango Personalizado"
        }
        return nombres.get(self.filtro_fecha, "Este Mes")

    @rx.var
    def datos_grafico_distribucion_pagos(self) -> List[Dict[str, Any]]:
        """
        Datos formateados para el gráfico de torta de distribución de pagos

        Returns:
            [
                {"name": "USD", "value": 4357.75, "fill": "#10b981"},
                {"name": "BS", "value": 8092.25, "fill": "#3b82f6"}
            ]
        """
        if not self.distribucion_pagos:
            return []

        return [
            {
                "name": "USD",
                "value": self.distribucion_pagos.get('total_usd', 0),
                "fill": "#10b981"
            },
            {
                "name": "BS",
                "value": self.distribucion_pagos.get('total_bs', 0),
                "fill": "#3b82f6"
            }
        ]

    @rx.var
    def datos_grafico_ingresos_odontologo(self) -> List[Dict[str, Any]]:
        """
        Datos formateados para el gráfico de torta de ingresos del odontólogo

        Returns:
            [
                {"name": "USD", "value": 3568.00, "fill": "#10b981"},
                {"name": "BS", "value": 5352.00, "fill": "#3b82f6"}
            ]
        """
        if not self.distribucion_ingresos_odontologo:
            return []

        return [
            {
                "name": "USD",
                "value": self.distribucion_ingresos_odontologo.get('total_usd', 0),
                "fill": "#10b981"
            },
            {
                "name": "BS",
                "value": self.distribucion_ingresos_odontologo.get('total_bs', 0),
                "fill": "#3b82f6"
            }
        ]

    @rx.var
    def datos_grafico_tipos_consulta(self) -> List[Dict[str, Any]]:
        """
        Datos formateados para el gráfico de torta de tipos de consulta

        Returns:
            Lista con colores asignados por tipo
        """
        if not self.tipos_consulta_distribucion:
            return []

        colores = {
            'General': '#3b82f6',
            'Control': '#10b981',
            'Urgencia': '#f59e0b',
            'Emergencia': '#ef4444'
        }

        return [
            {
                **tipo,
                "fill": colores.get(tipo.get('tipo', ''), '#6b7280')
            }
            for tipo in self.tipos_consulta_distribucion
        ]

    @rx.var
    def datos_evolucion_activa(self) -> List[Dict[str, Any]]:
        """
        Retorna los datos de evolución temporal según el tab activo

        Returns:
            Lista de datos para el gráfico según tab seleccionado
        """
        if self.tab_grafico_activo == "pacientes_nuevos":
            return self.evolucion_temporal_pacientes
        elif self.tab_grafico_activo == "consultas":
            return self.evolucion_temporal_consultas
        elif self.tab_grafico_activo == "ingresos":
            return self.evolucion_temporal_ingresos
        return []

    @rx.var
    def titulo_grafico_activo(self) -> str:
        """
        Retorna el título según el tab activo (GERENTE)

        Returns:
            Título descriptivo del gráfico
        """
        titulos = {
            "pacientes_nuevos": "Pacientes Nuevos en el Tiempo",
            "consultas": "Consultas Realizadas",
            "ingresos": "Ingresos Mensuales"
        }
        return titulos.get(self.tab_grafico_activo, "Evolución Temporal")

    @rx.var
    def datos_evolucion_odontologo_activa(self) -> List[Dict[str, Any]]:
        """
        Retorna los datos de evolución temporal según el tab activo (ODONTÓLOGO)

        Returns:
            Lista de datos para el gráfico según tab seleccionado
        """
        if self.tab_grafico_odontologo == "ingresos":
            return self.evolucion_temporal_ingresos_odontologo
        elif self.tab_grafico_odontologo == "intervenciones":
            return self.evolucion_temporal_intervenciones_odontologo
        return []

    @rx.var
    def titulo_grafico_odontologo_activo(self) -> str:
        """
        Retorna el título según el tab activo (ODONTÓLOGO)

        Returns:
            Título descriptivo del gráfico
        """
        titulos = {
            "ingresos": "Ingresos Generados",
            "intervenciones": "Intervenciones Realizadas"
        }
        return titulos.get(self.tab_grafico_odontologo, "Evolución Temporal")

    @rx.var
    def condiciones_mas_tratadas_top5(self) -> List[Dict[str, Any]]:
        """
        Retorna las top 5 condiciones más tratadas en formato para mini_stat_card

        Returns:
            Lista de dicts con label, value, color
        """
        from dental_system.styles.themes import COLORS

        if not self.estadisticas_odontograma:
            return []

        condiciones = self.estadisticas_odontograma.get("condiciones_mas_tratadas", [])
        if not condiciones:
            return []

        return [
            {
                "label": cond.get("tipo", "N/A"),
                "value": cond.get("cantidad", 0),
                "color": COLORS["primary"]["500"]
            }
            for cond in condiciones[:5]
        ]

    @rx.var
    def dientes_mas_intervenidos_top5(self) -> List[Dict[str, Any]]:
        """
        Retorna los top 5 dientes más intervenidos en formato para mini_stat_card

        Returns:
            Lista de dicts con label, value, color
        """
        from dental_system.styles.themes import COLORS

        if not self.estadisticas_odontograma:
            return []

        dientes = self.estadisticas_odontograma.get("dientes_mas_intervenidos", [])
        if not dientes:
            return []

        return [
            {
                "label": f"Diente {diente.get('diente_numero', 0)}",
                "value": diente.get("intervenciones", 0),
                "color": COLORS["blue"]["500"]
            }
            for diente in dientes[:5]
        ]

    @rx.var
    def superficies_mas_tratadas_top5(self) -> List[Dict[str, Any]]:
        """
        Retorna las top 5 superficies más tratadas en formato para mini_stat_card

        Returns:
            Lista de dicts con label, value, color
        """
        from dental_system.styles.themes import COLORS

        if not self.estadisticas_odontograma:
            return []

        superficies = self.estadisticas_odontograma.get("superficies_mas_tratadas", [])
        if not superficies:
            return []

        return [
            {
                "label": sup.get("superficie", "N/A").capitalize(),
                "value": sup.get("cantidad", 0),
                "color": COLORS["secondary"]["500"]
            }
            for sup in superficies[:5]
        ]

    # ====================================================================
    # 📊 COMPUTED VARS PARA ADMINISTRADOR
    # ====================================================================

    @rx.var
    def datos_grafico_distribucion_pagos_admin(self) -> List[Dict[str, Any]]:
        """
        Datos formateados para el gráfico de torta de distribución de pagos (ADMIN)

        Returns:
            [
                {"name": "USD", "value": 4357.75, "fill": "#10b981"},
                {"name": "BS", "value": 8092.25, "fill": "#3b82f6"}
            ]
        """
        if not self.distribucion_pagos_admin:
            return []

        return [
            {
                "name": "USD",
                "value": self.distribucion_pagos_admin.get('total_usd', 0),
                "fill": "#10b981"
            },
            {
                "name": "BS",
                "value": self.distribucion_pagos_admin.get('total_bs', 0),
                "fill": "#3b82f6"
            }
        ]

    @rx.var
    def datos_evolucion_admin_activa(self) -> List[Dict[str, Any]]:
        """
        Retorna los datos de evolución temporal según el tab activo (ADMIN)

        Returns:
            Lista de datos para el gráfico según tab seleccionado
        """
        if self.tab_grafico_admin == "consultas":
            return self.evolucion_temporal_consultas_admin
        elif self.tab_grafico_admin == "ingresos":
            return self.evolucion_temporal_ingresos_admin
        elif self.tab_grafico_admin == "pacientes_nuevos":
            return self.evolucion_temporal_pacientes_admin
        return []

    @rx.var
    def titulo_grafico_admin_activo(self) -> str:
        """
        Retorna el título según el tab activo (ADMINISTRADOR)

        Returns:
            Título descriptivo del gráfico
        """
        titulos = {
            "consultas": "Consultas Realizadas",
            "ingresos": "Ingresos Generados",
            "pacientes_nuevos": "Pacientes Nuevos Registrados"
        }
        return titulos.get(self.tab_grafico_admin, "Evolución Temporal")

    # ====================================================================
    # 📊 MÉTODOS DE DASHBOARD - ADMINISTRADOR (HOY)
    # ====================================================================

    @rx.event
    async def cargar_dashboard_admin(self):
        """
        🚀 CARGAR DASHBOARD COMPLETO DEL ADMINISTRADOR (TIEMPO REAL - HOY)

        Carga todas las métricas del día actual:
        - 7 cards principales (consultas, ingresos, pagos, servicios, intervenciones, pacientes nuevos)
        - Gráfico consultas por estado (en espera, en atención, completada, cancelada)
        - Gráfico consultas por odontólogo

        Diferencia con reportes:
        - Dashboard: Solo datos de HOY (tiempo real)
        - Reportes: Datos históricos con filtros de fecha
        """
        try:
            from dental_system.services.dashboard_service import dashboard_service

            print("🚀 Cargando dashboard del administrador (HOY)...")
            self.cargando_dashboard_admin = True

            # Llamar a los 3 métodos del service en paralelo
            import asyncio
            resultados = await asyncio.gather(
                dashboard_service.get_dashboard_stats_admin(),
                dashboard_service.get_consultas_hoy_por_estado_admin(),
                dashboard_service.get_consultas_hoy_por_odontologo_admin(),
                return_exceptions=True
            )

            # Asignar resultados
            self.dashboard_stats_admin = resultados[0] if not isinstance(resultados[0], Exception) else {}
            self.consultas_hoy_por_estado_admin = resultados[1] if not isinstance(resultados[1], Exception) else []
            self.consultas_hoy_por_odontologo_admin = resultados[2] if not isinstance(resultados[2], Exception) else []

            print(f"✅ Dashboard admin cargado - Stats: {self.dashboard_stats_admin}")
            print(f"✅ Consultas por estado: {len(self.consultas_hoy_por_estado_admin)} estados")
            print(f"✅ Consultas por odontólogo: {len(self.consultas_hoy_por_odontologo_admin)} odontólogos")

            self.cargando_dashboard_admin = False

        except Exception as e:
            print(f"❌ Error cargando dashboard admin: {e}")
            import traceback
            traceback.print_exc()
            self.cargando_dashboard_admin = False

            # Valores por defecto en caso de error
            self.dashboard_stats_admin = {
                "consultas_hoy_completadas": 0,
                "consultas_hoy_total": 0,
                "ingresos_hoy": 0.0,
                "pagos_realizados_hoy": 0,
                "servicios_aplicados_hoy": 0,
                "intervenciones_hoy": 0,
                "pacientes_nuevos_hoy": 0
            }
            self.consultas_hoy_por_estado_admin = []
            self.consultas_hoy_por_odontologo_admin = []

    @rx.event
    async def cargar_dashboard_asistente(self):
        """
        👩‍⚕️ CARGAR DASHBOARD BÁSICO DEL ASISTENTE (SOLO LECTURA - HOY)

        Carga solo métricas básicas del día actual:
        - Consultas hoy (total, completadas, en espera)
        - Pacientes atendidos hoy

        Diferencias con dashboard admin:
        - Asistente: Solo 4 métricas básicas (consultas y pacientes)
        - Admin: 7 métricas completas (incluye ingresos, pagos, servicios, intervenciones)
        """
        try:
            from dental_system.services.dashboard_service import dashboard_service

            print("👩‍⚕️ Cargando dashboard del asistente (solo lectura - HOY)...")
            self.cargando_dashboard_asistente = True

            # Llamar al método específico del service
            stats = await dashboard_service.get_dashboard_stats_asistente()

            # Asignar resultado
            self.dashboard_stats_asistente = stats if not isinstance(stats, Exception) else {}

            print(f"✅ Dashboard asistente cargado - Stats: {self.dashboard_stats_asistente}")

            self.cargando_dashboard_asistente = False

        except Exception as e:
            print(f"❌ Error cargando dashboard asistente: {e}")
            import traceback
            traceback.print_exc()
            self.cargando_dashboard_asistente = False

            # Valores por defecto en caso de error
            self.dashboard_stats_asistente = {
                "consultas_hoy_total": 0,
                "consultas_completadas": 0,
                "consultas_en_espera": 0,
                "pacientes_atendidos_hoy": 0
            }
