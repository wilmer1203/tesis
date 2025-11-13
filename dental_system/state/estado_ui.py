"""
📱 ESTADO DE INTERFAZ DE USUARIO - SUBSTATE SEPARADO
===================================================
"""

import reflex as rx
from datetime import datetime
from typing import Dict, Any, List, Union
from dental_system.models.ui_models import ToastModel

class EstadoUI(rx.State, mixin=True):

    
    # ==========================================
    # 📱 VARIABLES DE NAVEGACIÓN Y PÁGINAS
    # ==========================================
    
    # Control de navegación principal
    current_page: str = "dashboard"
    previous_page: str = ""
    titulo_pagina: str = "Dashboard"
    subtitulo_pagina: str = ""
    
    # Breadcrumbs y navegación
    ruta_navegacion: List[Dict[str, str]] = []
    puede_retroceder: bool = False
   
    # ==========================================
    # 📱 ESTADOS DE MODALES Y OVERLAYS
    # ==========================================
    
    # Modales principales del sistema

    modal_crear_consulta_abierto: bool = False
    modal_editar_consulta_abierto: bool = False
    modal_ver_consulta_abierto: bool = False

    modal_crear_pago_abierto: bool = False
    modal_ver_pago_abierto: bool = False
    
    # Modales de confirmación y alertas
    modal_confirmacion_abierto: bool = False
    
    # Contenido de modales dinámicos
    titulo_modal_confirmacion: str = ""
    mensaje_modal_confirmacion: str = ""
    accion_modal_confirmacion: str = ""
  
    # 🍞 SISTEMA DE TOASTS FLOTANTES
    active_toasts: List[ToastModel] = []
  
    # ==========================================
    # 📱 ESTADOS DE FORMULARIOS MULTI-PASO
    # ==========================================
    
    # Formulario de pacientes (3 pasos)
    paso_formulario_paciente: int = 0
    total_pasos_paciente: int = 3
    errores_formulario_paciente: Dict[str, str] = {}
    puede_continuar_form_paciente: bool = True
    datos_temporales_paciente: Dict[str, Any] = {}
    
    # Formulario de personal (3 pasos)
    paso_formulario_personal: int = 0
    total_pasos_personal: int = 3
    errores_formulario_personal: Dict[str, str] = {}
    puede_continuar_form_personal: bool = True
    datos_temporales_personal: Dict[str, Any] = {}
    
    datos_temporales_consulta: Dict[str, Any] = {}
    # ==========================================
    # 📱 NOTIFICACIONES Y FEEDBACK
    # ==========================================
    
    # Toast messages
    toast_visible: bool = False
    toast_mensaje: str = ""
    toast_tipo: str = "info"  # info, success, warning, error
    toast_duracion: int = 3000  # milisegundos

    cargando_dashboard: bool = False
    
    # ==========================================
    # 📱 MÉTODOS DE NAVEGACIÓN
    # ==========================================
    
    @rx.event
    def navigate_to(self, pagina: str, titulo: str = "", subtitulo: str = ""):
        """
        🧭 NAVEGACIÓN PRINCIPAL ENTRE PÁGINAS

        Args:
            pagina: Nombre de la página destino
            titulo: Título a mostrar en la página
            subtitulo: Subtítulo opcional
        """
        self.previous_page = self.current_page
        self.current_page = pagina
        self.titulo_pagina = titulo or pagina.title()
        self.subtitulo_pagina = subtitulo
        self.puede_retroceder = bool(self.previous_page)

        # Actualizar breadcrumbs
        self._actualizar_breadcrumbs(pagina, titulo)

        print(f"🧭 Navegación: {self.previous_page} → {self.current_page}")

    def _actualizar_breadcrumbs(self, pagina: str, titulo: str):
        """🔗 Actualizar breadcrumbs de navegación"""
        # Lógica para mantener breadcrumbs relevantes
        breadcrumb = {
            "pagina": pagina,
            "titulo": titulo or pagina.title(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Mantener máximo 5 breadcrumbs
        if len(self.ruta_navegacion) >= 5:
            self.ruta_navegacion = self.ruta_navegacion[-4:]
        
        self.ruta_navegacion.append(breadcrumb)
    
    # ==========================================
    # 📱 GESTIÓN DE MODALES
    # ==========================================

    @rx.event
    def abrir_modal_consulta(self, tipo: str, datos: Dict[str, Any] = None):
        """📅 Abrir modal de consultas"""
        self.cerrar_todos_los_modales()
        
        if tipo == "crear":
            self.modal_crear_consulta_abierto = True
            self.datos_temporales_consulta = {}
        elif tipo == "editar":
            self.modal_editar_consulta_abierto = True
            self.datos_temporales_consulta = datos or {}
        elif tipo == "ver":
            self.modal_ver_consulta_abierto = True
            self.datos_temporales_consulta = datos or {}
        
        print(f"📅 Modal consulta abierto: {tipo}")
    
    @rx.event
    def abrir_modal_confirmacion(self, titulo: str, mensaje: str, accion: str):
        """⚠️ Abrir modal de confirmación"""
        self.modal_confirmacion_abierto = True
        self.titulo_modal_confirmacion = titulo
        self.mensaje_modal_confirmacion = mensaje
        self.accion_modal_confirmacion = accion
        print(f"⚠️ Modal confirmación: {titulo}")

    @rx.event
    async def ejecutar_accion_confirmacion(self):
        """
        ✅ EJECUTAR ACCIÓN CONFIRMADA

        Ejecuta la acción almacenada en accion_modal_confirmacion
        basándose en el nombre del método.
        """
        try:
            accion = self.accion_modal_confirmacion
            print(f"🎯 Ejecutando acción confirmada: {accion}")

            # Router de acciones disponibles
            if accion == "activar_personal":
                await self.ejecutar_accion_personal()
            elif accion == "desactivar_personal":
                await self.ejecutar_accion_personal()
            elif accion == "activar_servicio":
                await self.ejecutar_accion_servicio()
            elif accion == "desactivar_servicio":
                await self.ejecutar_accion_servicio()
            else:
                print(f"⚠️ Acción no reconocida: {accion}")

            # Cerrar modal después de ejecutar la acción
            self.cerrar_todos_los_modales()

        except Exception as e:
            print(f"❌ Error ejecutando acción confirmada: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al ejecutar la acción")
            # Cerrar modal incluso si hay error
            self.cerrar_todos_los_modales()

    @rx.event
    def cerrar_todos_los_modales(self):
        """❌ Cerrar todos los modales abiertos"""
        # Modales de pacientes
        self.modal_crear_paciente_abierto = False
        self.modal_editar_paciente_abierto = False
        
        # Modales de consultas
        self.modal_crear_consulta_abierto = False
        self.modal_editar_consulta_abierto = False
        self.modal_ver_consulta_abierto = False
        
        # Modales de personal
        self.modal_crear_personal_abierto = False
        self.modal_editar_personal_abierto = False

        # Modales de pagos
        self.modal_crear_pago_abierto = False
        self.modal_ver_pago_abierto = False
        
        # Modales de confirmación/alerta
        self.modal_confirmacion_abierto = False
        self.datos_temporales_consulta = {}
     
        print("❌ Todos los modales cerrados")
    
    # ==========================================
    # 📱 SETTERS PARA MODALES (Requeridos por UI)
    # ==========================================
    
    @rx.event
    def set_modal_crear_consulta_abierto(self, abierto: bool):
        """📅 Setter para modal de crear consulta"""
        self.modal_crear_consulta_abierto = abierto
    
    @rx.event
    def set_modal_editar_consulta_abierto(self, abierto: bool):
        """📅 Setter para modal de editar consulta"""
        self.modal_editar_consulta_abierto = abierto
    
    # ==========================================
    # 📱 FORMULARIOS MULTI-PASO
    # ==========================================
    
    @rx.event
    def avanzar_paso_paciente(self):
        """➡️ Avanzar paso en formulario de paciente"""
        if self.puede_continuar_form_paciente and self.paso_formulario_paciente < self.total_pasos_paciente - 1:
            self.paso_formulario_paciente += 1
            print(f"📝 Formulario paciente: paso {self.paso_formulario_paciente + 1}/{self.total_pasos_paciente}")
    
    @rx.event
    def retroceder_paso_paciente(self):
        """⬅️ Retroceder paso en formulario de paciente"""
        if self.paso_formulario_paciente > 0:
            self.paso_formulario_paciente -= 1
            print(f"📝 Formulario paciente: paso {self.paso_formulario_paciente + 1}/{self.total_pasos_paciente}")
    
    @rx.event
    def avanzar_paso_personal(self):
        """➡️ Avanzar paso en formulario de personal"""
        if self.puede_continuar_form_personal and self.paso_formulario_personal < self.total_pasos_personal - 1:
            self.paso_formulario_personal += 1
            print(f"📝 Formulario personal: paso {self.paso_formulario_personal + 1}/{self.total_pasos_personal}")
    
    @rx.event
    def retroceder_paso_personal(self):
        """⬅️ Retroceder paso en formulario de personal"""
        if self.paso_formulario_personal > 0:
            self.paso_formulario_personal -= 1
            print(f"📝 Formulario personal: paso {self.paso_formulario_personal + 1}/{self.total_pasos_personal}")
    
    
    # ==========================================
    # 📱 SISTEMA DE NOTIFICACIONES
    # ==========================================
    
    @rx.event
    def mostrar_toast(self, mensaje: str, tipo: str = "info", duracion: int = 3000):
        """🍞 Mostrar toast message"""
        self.toast_mensaje = mensaje
        self.toast_tipo = tipo
        self.toast_duracion = duracion
        self.toast_visible = True
        print(f"Toast ({tipo}): {mensaje}")
    
    @rx.event
    def ocultar_toast(self):
        """🙈 Ocultar toast message"""
        self.toast_visible = False
        self.toast_mensaje = ""
        print("Toast ocultado")
    
    @rx.event
    def remove_toast(self, toast_id: str):
        """❌ Remover toast específico"""
        self.active_toasts = [t for t in self.active_toasts if t.id != toast_id]
        print(f"❌ Toast removido: {toast_id}")
    
    

    # ==========================================
    # 📊 GRÁFICOS Y ANALYTICS - PRODUCCIÓN
    # ==========================================
    area_toggle: bool = True
    selected_tab: str = "Pacientes"
    timeframe: str = "Mensual"

    # 📊 DATOS REALES DEL DASHBOARD (últimos 30 días)
    pacientes_data_real: List[Dict[str, Any]] = []
    ingresos_data_real: List[Dict[str, Any]] = []
    consultas_data_real: List[Dict[str, Any]] = []

    # 📈 ESTADÍSTICAS DEL GERENTE
    dashboard_stats: Dict[str, Any] = {}

    def toggle_areachart(self):
        """🔄 Alterna entre gráfico de área y barras"""
        self.area_toggle = not self.area_toggle

    def set_selected_tab(self, selected_tab: Union[str, List[str]]):
        """📑 Cambia la pestaña seleccionada del gráfico"""
        if isinstance(selected_tab, list):
            self.selected_tab = selected_tab[0]
        else:
            self.selected_tab = selected_tab

    @rx.var(cache=False)
    def get_current_data(self) -> List[Dict[str, Any]]:
        """📊 Obtener datos reales según tab seleccionado"""
        match self.selected_tab:
            case "Pacientes":
                return self.pacientes_data_real
            case "Ingresos":
                return self.ingresos_data_real
            case "Consultas":
                return self.consultas_data_real
        return []

    async def cargar_stats_gerente_dashboard(self):
        """📊 CARGAR ESTADÍSTICAS DEL GERENTE PARA DASHBOARD"""
        try:
            from dental_system.services.dashboard_service import dashboard_service

            print("📊 Cargando stats del gerente...")
            self.cargando_dashboard = True

            # Llamar al service
            stats = await dashboard_service.get_gerente_stats_simple()
            self.dashboard_stats = stats

            print(f"✅ Stats cargadas: {stats}")
            self.cargando_dashboard = False

        except Exception as e:
            print(f"❌ Error cargando stats del gerente: {e}")
            self.cargando_dashboard = False
            self.dashboard_stats = {
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

    async def cargar_datos_graficos_reales(self):
        """📈 CARGAR DATOS REALES PARA GRÁFICOS (últimos 30 días)"""
        try:
            from dental_system.services.dashboard_service import dashboard_service

            print("📈 Cargando datos reales para gráficos...")

            # Obtener datos de los últimos 30 días
            chart_data = await dashboard_service.get_chart_data_last_30_days("gerente")

            # Asignar a variables de estado
            self.pacientes_data_real = chart_data.get("pacientes_data", [])
            self.ingresos_data_real = chart_data.get("ingresos_data", [])
            self.consultas_data_real = chart_data.get("consultas_data", [])

            print(f"✅ Datos gráficos cargados: {len(self.pacientes_data_real)} días")

        except Exception as e:
            print(f"❌ Error cargando datos de gráficos: {e}")
            # Mantener arrays vacíos
            self.pacientes_data_real = []
            self.ingresos_data_real = []
            self.consultas_data_real = []

    async def cargar_dashboard_gerente_completo(self):
        """🚀 CARGAR TODO EL DASHBOARD DEL GERENTE (stats + gráficos)"""
        try:
            print("🚀 Iniciando carga completa del dashboard...")

            # Cargar stats y gráficos en secuencia
            await self.cargar_stats_gerente_dashboard()
            await self.cargar_datos_graficos_reales()

            print("✅ Dashboard del gerente cargado completamente")

        except Exception as e:
            print(f"❌ Error en carga completa del dashboard: {e}")
