"""
📱 ESTADO DE INTERFAZ DE USUARIO - SUBSTATE SEPARADO
===================================================

PROPÓSITO: Manejo centralizado y especializado de UI y navegación
- Control de páginas activas y navegación
- Estados de modales y notificaciones
- Barras laterales y estados de pantalla
- Formularios multi-paso y validaciones UI
- Loading states y feedback de usuario

USADO POR: AppState como coordinador principal
PATRÓN: Substate con get_estado_ui() en AppState
"""

import reflex as rx
from datetime import datetime,timedelta
from typing import Dict, Any, List, Optional, Union
import logging
from dental_system.models.ui_models import ToastModel, NotificationModel
logger = logging.getLogger(__name__)

class EstadoUI(rx.State, mixin=True):
    """
    📱 ESTADO ESPECIALIZADO EN INTERFAZ DE USUARIO Y NAVEGACIÓN
    
    RESPONSABILIDADES:
    - Control de navegación y páginas activas
    - Gestión de modales y overlays
    - Estados de formularios multi-paso
    - Notificaciones y alertas de usuario
    - Loading states y feedback visual
    - Sidebar y componentes de layout
    """
    
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
    
    # Estados de sidebar y layout
    sidebar_abierto: bool = True
    sidebar_colapsado: bool = False
    modo_mobile: bool = False
    ancho_pantalla: str = "desktop"  # desktop, tablet, mobile
    
    # ==========================================
    # 📱 ESTADOS DE MODALES Y OVERLAYS
    # ==========================================
    
    # Modales principales del sistema
    modal_crear_paciente_abierto: bool = False
    modal_editar_paciente_abierto: bool = False
    modal_ver_paciente_abierto: bool = False
    
    modal_crear_consulta_abierto: bool = False
    modal_editar_consulta_abierto: bool = False
    modal_ver_consulta_abierto: bool = False
    
    modal_crear_personal_abierto: bool = False
    modal_editar_personal_abierto: bool = False
    modal_ver_personal_abierto: bool = False
    
    modal_crear_servicio_abierto: bool = False
    modal_editar_servicio_abierto: bool = False
    
    modal_crear_pago_abierto: bool = False
    modal_ver_pago_abierto: bool = False
    
    # Modales de confirmación y alertas
    modal_confirmacion_abierto: bool = False
    modal_alerta_abierto: bool = False
    modal_info_abierto: bool = False
    modal_cambio_odontologo_abierto: bool = False
    
    # Contenido de modales dinámicos
    titulo_modal_confirmacion: str = ""
    mensaje_modal_confirmacion: str = ""
    accion_modal_confirmacion: str = ""
    
    titulo_modal_alerta: str = ""
    mensaje_modal_alerta: str = ""
    tipo_alerta: str = "info"  # info, warning, error, success
    
    # 🍞 SISTEMA DE TOASTS FLOTANTES
    active_toasts: List[ToastModel] = []
    active_notifications: List[NotificationModel] = []
    
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
    
    # Formulario de consultas (2 pasos)
    paso_formulario_consulta: int = 0
    total_pasos_consulta: int = 2
    errores_formulario_consulta: Dict[str, str] = {}
    puede_continuar_form_consulta: bool = True
    datos_temporales_consulta: Dict[str, Any] = {}
    datos_temporales_servicio: Dict[str, Any] = {}

    # ==========================================
    # 📱 NOTIFICACIONES Y FEEDBACK
    # ==========================================
    
    # Sistema de notificaciones
    notificaciones_activas: List[Dict[str, Any]] = []
    mostrar_notificaciones: bool = False
    total_notificaciones_no_leidas: int = 0
    
    # Toast messages
    toast_visible: bool = False
    toast_mensaje: str = ""
    toast_tipo: str = "info"  # info, success, warning, error
    toast_duracion: int = 3000  # milisegundos
    
    # Loading states globales
    cargando_global: bool = False
    mensaje_cargando: str = "Cargando..."
    progreso_carga: int = 0  # 0-100
    
    # Estados de operaciones específicas
    cargando_pacientes: bool = False
    cargando_consultas: bool = False
    cargando_personal: bool = False
    cargando_servicios: bool = False
    cargando_pagos: bool = False
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

    
    @rx.event
    def retroceder_pagina(self):
        """⬅️ Retroceder a la página anterior"""
        if self.puede_retroceder and self.previous_page:
            pagina_temp = self.current_page
            self.current_page = self.previous_page
            self.previous_page = pagina_temp
            self.titulo_pagina = self.current_page.title()
            print(f"⬅️ Retroceso: {pagina_temp} → {self.current_page}")
    
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
    def abrir_modal_paciente(self, tipo: str, datos: Dict[str, Any] = None):
        """👥 Abrir modal de pacientes"""
        self.cerrar_todos_los_modales()
        
        if tipo == "crear":
            self.modal_crear_paciente_abierto = True
            self.datos_temporales_paciente = {}
        elif tipo == "editar":
            self.modal_editar_paciente_abierto = True
            self.datos_temporales_paciente = datos or {}
        elif tipo == "ver":
            self.modal_ver_paciente_abierto = True
            self.datos_temporales_paciente = datos or {}
        
        print(f"👥 Modal paciente abierto: {tipo}")
    
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
    def abrir_modal_personal(self, tipo: str, datos: Dict[str, Any] = None):
        """👨‍⚕️ Abrir modal de personal"""
        self.cerrar_todos_los_modales()
        print("estamos en abrir modal")
        if tipo == "crear":
            self.modal_crear_personal_abierto = True
            print("se cambio a TRUE  del modal crear personal")
            self.datos_temporales_personal = {}
        elif tipo == "editar":
            self.modal_editar_personal_abierto = True
            self.datos_temporales_personal = datos or {}
        elif tipo == "ver":
            self.modal_ver_personal_abierto = True
            self.datos_temporales_personal = datos or {}
        
        print(f"👨‍⚕️ Modal personal abierto: {tipo}")

    @rx.event
    def abrir_modal_servicio(self, tipo: str, datos: Dict[str, Any] = None):
        """🏥 Abrir modal de servicio"""
        self.cerrar_todos_los_modales()
        if tipo == "crear":
            self.modal_crear_servicio_abierto = True
            self.datos_temporales_servicio = {}
        elif tipo == "editar":
            self.modal_editar_servicio_abierto = True
            self.datos_temporales_servicio = datos or {}

        print(f"🏥 Modal servicio abierto: {tipo}")

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
            elif accion == "eliminar_paciente":
                # Aquí iría la lógica para eliminar paciente
                pass
            elif accion == "reactivar_paciente":
                # Aquí iría la lógica para reactivar paciente
                pass
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
    def abrir_modal_alerta(self, titulo: str, mensaje: str, tipo: str = "info"):
        """🔔 Abrir modal de alerta"""
        self.modal_alerta_abierto = True
        self.titulo_modal_alerta = titulo
        self.mensaje_modal_alerta = mensaje
        self.tipo_alerta = tipo
    
    @rx.event
    def abrir_modal_cambio_odontologo(self):
        """🔄 Abrir modal de cambio de odontólogo"""
        self.modal_cambio_odontologo_abierto = True
        print("🔄 Modal cambio odontólogo abierto")
    

    @rx.event
    def cerrar_todos_los_modales(self):
        """❌ Cerrar todos los modales abiertos"""
        # Modales de pacientes
        self.modal_crear_paciente_abierto = False
        self.modal_editar_paciente_abierto = False
        self.modal_ver_paciente_abierto = False
        
        # Modales de consultas
        self.modal_crear_consulta_abierto = False
        self.modal_editar_consulta_abierto = False
        self.modal_ver_consulta_abierto = False
        
        # Modales de personal
        self.modal_crear_personal_abierto = False
        self.modal_editar_personal_abierto = False
        self.modal_ver_personal_abierto = False
        
        # Modales de servicios
        self.modal_crear_servicio_abierto = False
        self.modal_editar_servicio_abierto = False
        
        # Modales de pagos
        self.modal_crear_pago_abierto = False
        self.modal_ver_pago_abierto = False
        
        # Modales de confirmación/alerta
        self.modal_confirmacion_abierto = False
        self.modal_alerta_abierto = False
        self.modal_info_abierto = False
        self.modal_cambio_odontologo_abierto = False
        
        # Limpiar datos temporales
        self.datos_temporales_paciente = {}
        self.datos_temporales_consulta = {}
        self.datos_temporales_personal = {}
        
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
    def resetear_formulario_paciente(self):
        """🔄 Resetear formulario de paciente"""
        self.paso_formulario_paciente = 0
        self.errores_formulario_paciente = {}
        self.puede_continuar_form_paciente = True
        self.datos_temporales_paciente = {}
        print("🔄 Formulario paciente reseteado")
    
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
    
    @rx.event
    def resetear_formulario_personal(self):
        """🔄 Resetear formulario de personal"""
        self.paso_formulario_personal = 0
        self.errores_formulario_personal = {}
        self.puede_continuar_form_personal = True
        self.datos_temporales_personal = {}
        print("🔄 Formulario personal reseteado")
    
    @rx.event
    def avanzar_paso_consulta(self):
        """➡️ Avanzar paso en formulario de consulta"""
        if self.puede_continuar_form_consulta and self.paso_formulario_consulta < self.total_pasos_consulta - 1:
            self.paso_formulario_consulta += 1
            print(f"📝 Formulario consulta: paso {self.paso_formulario_consulta + 1}/{self.total_pasos_consulta}")
    
    @rx.event
    def retroceder_paso_consulta(self):
        """⬅️ Retroceder paso en formulario de consulta"""
        if self.paso_formulario_consulta > 0:
            self.paso_formulario_consulta -= 1
            print(f"📝 Formulario consulta: paso {self.paso_formulario_consulta + 1}/{self.total_pasos_consulta}")
    
    @rx.event
    def resetear_formulario_consulta(self):
        """🔄 Resetear formulario de consulta"""
        self.paso_formulario_consulta = 0
        self.errores_formulario_consulta = {}
        self.puede_continuar_form_consulta = True
        self.datos_temporales_consulta = {}
        print("🔄 Formulario consulta reseteado")
    
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
        print(f"🍞 Toast ({tipo}): {mensaje}")
    
    @rx.event
    def ocultar_toast(self):
        """🙈 Ocultar toast message"""
        self.toast_visible = False
        self.toast_mensaje = ""
        print("🙈 Toast ocultado")
    
    # ==========================================
    # 🍞 SISTEMA DE TOASTS FLOTANTES MODERNO
    # ==========================================
    
    @rx.event
    def add_toast(self, message: str, toast_type: str = "info", duration: int = 4000):
        """🍞 Agregar toast flotante"""
        if toast_type == "success":
            toast = ToastModel.success(message, duration)
        elif toast_type == "error":
            toast = ToastModel.error(message, duration)
        elif toast_type == "warning":
            toast = ToastModel.warning(message, duration)
        else:
            toast = ToastModel.info(message, duration)
            
        # Agregar al inicio de la lista
        self.active_toasts = [toast] + self.active_toasts
        
        # Limitar a máximo 3 toasts simultáneos
        if len(self.active_toasts) > 3:
            self.active_toasts = self.active_toasts[:3]
            
        print(f"🍞 Toast agregado ({toast_type}): {message}")
    
    @rx.event
    def remove_toast(self, toast_id: str):
        """❌ Remover toast específico"""
        self.active_toasts = [t for t in self.active_toasts if t.id != toast_id]
        print(f"❌ Toast removido: {toast_id}")
    
    @rx.event
    def clear_all_toasts(self):
        """🧹 Limpiar todos los toasts"""
        self.active_toasts = []
        print("🧹 Todos los toasts limpiados")
    
    @rx.event
    def add_notification(self, title: str, message: str, notification_type: str = "info", action_url: str = "", action_text: str = ""):
        """📢 Agregar notificación persistente"""
        notification = NotificationModel(
            id=f"notif_{datetime.now().timestamp()}",
            title=title,
            message=message,
            notification_type=notification_type,
            timestamp=datetime.now().isoformat(),
            is_read=False,
            action_url=action_url,
            action_text=action_text
        )
        
        # Agregar al inicio
        self.active_notifications = [notification] + self.active_notifications
        
        # Limitar a máximo 10 notificaciones
        if len(self.active_notifications) > 10:
            self.active_notifications = self.active_notifications[:10]
            
        print(f"📢 Notificación agregada: {title}")
    
    @rx.event
    def mark_notification_read(self, notification_id: str):
        """✅ Marcar notificación como leída"""
        for notif in self.active_notifications:
            if notif.id == notification_id:
                notif.is_read = True
                break
        print(f"✅ Notificación marcada como leída: {notification_id}")
    
    @rx.event
    def remove_notification(self, notification_id: str):
        """🗑️ Remover notificación"""
        self.active_notifications = [n for n in self.active_notifications if n.id != notification_id]
        print(f"🗑️ Notificación removida: {notification_id}")
    
    @rx.event
    def agregar_notificacion(self, titulo: str, mensaje: str, tipo: str = "info"):
        """🔔 Agregar nueva notificación"""
        notificacion = {
            "id": f"notif_{len(self.notificaciones_activas)}_{int(datetime.now().timestamp())}",
            "titulo": titulo,
            "mensaje": mensaje,
            "tipo": tipo,
            "timestamp": datetime.now().isoformat(),
            "leida": False
        }
        
        self.notificaciones_activas.append(notificacion)
        self.total_notificaciones_no_leidas += 1
        print(f"🔔 Nueva notificación: {titulo}")
    
    @rx.event
    def marcar_notificacion_leida(self, notificacion_id: str):
        """📖 Marcar notificación como leída"""
        for notif in self.notificaciones_activas:
            if notif["id"] == notificacion_id and not notif["leida"]:
                notif["leida"] = True
                self.total_notificaciones_no_leidas = max(0, self.total_notificaciones_no_leidas - 1)
                break
    
    @rx.event
    def limpiar_notificaciones(self):
        """🗑️ Limpiar todas las notificaciones"""
        self.notificaciones_activas = []
        self.total_notificaciones_no_leidas = 0
        self.mostrar_notificaciones = False
        print("🗑️ Notificaciones limpiadas")
    
    # ==========================================
    # 📱 LOADING STATES
    # ==========================================
    
    @rx.event
    def iniciar_carga_global(self, mensaje: str = "Cargando..."):
        """⏳ Iniciar loading global"""
        self.cargando_global = True
        self.mensaje_cargando = mensaje
        self.progreso_carga = 0
        print(f"⏳ Carga global iniciada: {mensaje}")
    
    @rx.event
    def actualizar_progreso_carga(self, progreso: int):
        """📊 Actualizar progreso de carga"""
        self.progreso_carga = max(0, min(100, progreso))
    
    @rx.event
    def finalizar_carga_global(self):
        """✅ Finalizar loading global"""
        self.cargando_global = False
        self.mensaje_cargando = "Cargando..."
        self.progreso_carga = 100
        print("✅ Carga global finalizada")
    
    @rx.event
    def set_cargando_modulo(self, modulo: str, cargando: bool):
        """🔄 Cambiar estado de carga de módulo específico"""
        if modulo == "pacientes":
            self.cargando_pacientes = cargando
        elif modulo == "consultas":
            self.cargando_consultas = cargando
        elif modulo == "personal":
            self.cargando_personal = cargando
        elif modulo == "servicios":
            self.cargando_servicios = cargando
        elif modulo == "pagos":
            self.cargando_pagos = cargando
        elif modulo == "dashboard":
            self.cargando_dashboard = cargando
        
        print(f"🔄 Loading {modulo}: {cargando}")
    
    # ==========================================
    # 📱 LAYOUT Y RESPONSIVE
    # ==========================================
    
    @rx.event
    def toggle_sidebar(self):
        """📂 Alternar sidebar"""
        self.sidebar_abierto = not self.sidebar_abierto
        print(f"📂 Sidebar: {'abierto' if self.sidebar_abierto else 'cerrado'}")
    
    @rx.event
    def colapsar_sidebar(self, colapsado: bool):
        """📁 Colapsar/expandir sidebar"""
        self.sidebar_colapsado = colapsado
        print(f"📁 Sidebar colapsado: {colapsado}")
    
    @rx.event
    def detectar_ancho_pantalla(self, ancho: str):
        """📱 Detectar cambio de ancho de pantalla"""
        self.ancho_pantalla = ancho
        self.modo_mobile = ancho == "mobile"
        
        # Auto-colapsar sidebar en móvil
        if self.modo_mobile:
            self.sidebar_abierto = False
        
        print(f"📱 Ancho de pantalla: {ancho}")
    
    # ==========================================
    # 📱 COMPUTED VARS PARA UI
    # ==========================================
    
    @rx.var(cache=True)
    def hay_modales_abiertos(self) -> bool:
        """🪟 Verificar si hay algún modal abierto"""
        return (
            self.modal_crear_paciente_abierto or
            self.modal_editar_paciente_abierto or
            self.modal_ver_paciente_abierto or
            self.modal_crear_consulta_abierto or
            self.modal_editar_consulta_abierto or
            self.modal_ver_consulta_abierto or
            self.modal_crear_personal_abierto or
            self.modal_editar_personal_abierto or
            self.modal_ver_personal_abierto or
            self.modal_crear_servicio_abierto or
            self.modal_editar_servicio_abierto or
            self.modal_crear_pago_abierto or
            self.modal_ver_pago_abierto or
            self.modal_confirmacion_abierto or
            self.modal_alerta_abierto or
            self.modal_info_abierto
        )
    
    @rx.var(cache=True)
    def progreso_formulario_paciente(self) -> float:
        """📊 Progreso del formulario de paciente (0-100)"""
        if self.total_pasos_paciente == 0:
            return 0
        return (self.paso_formulario_paciente / (self.total_pasos_paciente - 1)) * 100
    
    @rx.var(cache=True)
    def progreso_formulario_personal(self) -> float:
        """📊 Progreso del formulario de personal (0-100)"""
        if self.total_pasos_personal == 0:
            return 0
        return (self.paso_formulario_personal / (self.total_pasos_personal - 1)) * 100
    
    @rx.var(cache=True)
    def progreso_formulario_consulta(self) -> float:
        """📊 Progreso del formulario de consulta (0-100)"""
        if self.total_pasos_consulta == 0:
            return 0
        return (self.paso_formulario_consulta / (self.total_pasos_consulta - 1)) * 100
    
    @rx.var(cache=True)
    def hay_notificaciones_pendientes(self) -> bool:
        """🔔 Verificar si hay notificaciones no leídas"""
        return self.total_notificaciones_no_leidas > 0
    
    @rx.var(cache=True)
    def hay_carga_activa(self) -> bool:
        """⏳ Verificar si hay algún proceso de carga activo"""
        return (
            self.cargando_global or
            self.cargando_pacientes or
            self.cargando_consultas or
            self.cargando_personal or
            self.cargando_servicios or
            self.cargando_pagos or
            self.cargando_dashboard
        )
    
    @rx.var(cache=True)
    def titulo_breadcrumb_actual(self) -> str:
        """📍 Título actual para breadcrumbs"""
        if self.ruta_navegacion:
            return self.ruta_navegacion[-1]["titulo"]
        return self.titulo_pagina
    
    @rx.var(cache=True)
    def clase_css_sidebar(self) -> str:
        """🎨 Clase CSS para el sidebar según estado"""
        clases = ["sidebar"]
        
        if not self.sidebar_abierto:
            clases.append("sidebar-closed")
        
        if self.sidebar_colapsado:
            clases.append("sidebar-collapsed")
        
        if self.modo_mobile:
            clases.append("sidebar-mobile")
        
        return " ".join(clases)
    
    # ==========================================
    # 📱 UTILIDADES DE UI
    # ==========================================
    
    def obtener_icono_notificacion(self, tipo: str) -> str:
        """🎨 Obtener icono para tipo de notificación"""
        iconos = {
            "info": "📘",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        return iconos.get(tipo, "📘")
    
    def obtener_color_toast(self, tipo: str) -> str:
        """🎨 Obtener color para toast según tipo"""
        colores = {
            "info": "blue",
            "success": "green",
            "warning": "yellow", 
            "error": "red"
        }
        return colores.get(tipo, "blue")
    
    def formatear_timestamp_notificacion(self, timestamp: str) -> str:
        """🕐 Formatear timestamp de notificación"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            ahora = datetime.now()
            diferencia = ahora - dt
            
            if diferencia.seconds < 60:
                return "Hace un momento"
            elif diferencia.seconds < 3600:
                minutos = diferencia.seconds // 60
                return f"Hace {minutos} min"
            elif diferencia.days == 0:
                horas = diferencia.seconds // 3600
                return f"Hace {horas} h"
            else:
                return dt.strftime("%d/%m %H:%M")
        except:
            return "Recientemente"
    
    def limpiar_datos_temporales_completo(self):
        """🧹 Limpiar todos los datos temporales"""
        self.datos_temporales_paciente = {}
        self.datos_temporales_consulta = {}
        self.datos_temporales_personal = {}
        self.datos_temporales_servicio = {}
        
        # Resetear formularios
        self.resetear_formulario_paciente()
        self.resetear_formulario_personal()
        self.resetear_formulario_consulta()
        
        print("🧹 Datos temporales limpiados completamente")
        
        
        
           
        
    # ==========================================
    # GRÁFICOS Y ANALYTICS
    # ==========================================
    area_toggle: bool = True
    selected_tab: str = "Pacientes"
    timeframe: str = "Mensual"
    pacientes_data = []
    ingresos_data = []
    consultas_data = []
    
    
    def toggle_areachart(self):
        """Alterna entre gráfico de área y barras."""
        self.area_toggle = not self.area_toggle
    
    def set_selected_tab(self, selected_tab: Union[str, List[str]]):
        """Cambia la pestaña seleccionada."""
        if isinstance(selected_tab, list):
            self.selected_tab = selected_tab[0]
        else:
            self.selected_tab = selected_tab
    
    @rx.var(cache=False)
    def get_current_data(self) -> list:
        match self.selected_tab:
            case "Pacientes":
                return self.pacientes_data
            case "Ingresos":
                return self.ingresos_data
            case "Consultas":
                return self.consultas_data
        return []
    
    def randomize_data(self):
        import random
        """Genera datos de ejemplo para gráficos"""
        if self.pacientes_data:
            return
        
        for i in range(30, -1, -1):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%d-%m")
            
            self.ingresos_data.append({
                "name": date_str,
                "Ingresos": random.randint(1000, 5000)
            })
            
            self.consultas_data.append({
                "name": date_str,
                "Consultas": random.randint(10, 50)
            })
            
            self.pacientes_data.append({
                "name": date_str,
                "Pacientes": random.randint(5, 20)
            })
            
            
    