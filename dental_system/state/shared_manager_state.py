"""
Estado base compartido entre Boss y Admin
Centraliza funcionalidad común y elimina duplicación
SOLUCIÓN DEFINITIVA - Estructura de datos corregida
"""

import reflex as rx
from typing import Dict, List, Any, Optional
from .base import BaseState

# Importar servicios centralizados
from dental_system.services.dashboard_service import dashboard_service
from dental_system.services.pacientes_service import pacientes_service
from dental_system.services.consultas_service import consultas_service
from ..models import PacienteModel, ConsultaModel, ServicioModel, PersonalModel

class SharedManagerState(BaseState):
    """
    Estado base compartido entre BossState y AdminState
    Contiene toda la funcionalidad común eliminando duplicación
    """
    
    # ==========================================
    # VARIABLES DE ESTADO
    # ==========================================
    
    # Variable para controlar si ya se configuraron los servicios
    _services_configured: bool = False
    _last_configured_user_id: str = ""
    
    # ==========================================
    # CONFIGURACIÓN DE SERVICIOS 
    # ==========================================
    
    # En shared_manager_state.py - AGREGAR DEBUG TEMPORAL

    def _configure_services(self):
        """Configura los servicios con el contexto del usuario actual"""
        # Verificaciones existentes...
        if not self.is_authenticated:
            print("[DEBUG] ⚠️ Usuario no autenticado, saltando configuración de servicios")
            return False
        
        if not self.user_role:
            print(f"[DEBUG] ⚠️ user_role vacío: '{self.user_role}', saltando configuración de servicios")
            return False
        
        if not self.user_profile or not isinstance(self.user_profile, dict):
            print("[DEBUG] ⚠️ user_profile no disponible, saltando configuración de servicios")
            return False
            
        if self._services_configured:
            current_user_id = self._get_current_user_id()
            if self._last_configured_user_id == current_user_id:
                return True
        
        user_id = self._get_current_user_id()
        user_profile = self.user_profile
        
        try:
            print(f"[DEBUG] 🔧 Configurando servicios para usuario: {user_id} (rol: {self.user_role})")
            
            # ===== SIMPLIFICADO: Ya no necesita normalización =====
            # Convertir MutableProxy a dict normal si es necesario
            if hasattr(user_profile, '__dict__'):
                user_profile = dict(user_profile)
            
            print(f"[DEBUG] 📦 Enviando user_profile directo a servicios")
            
            # Configurar servicios directamente
            dashboard_service.set_user_context(user_id, user_profile)
            pacientes_service.set_user_context(user_id, user_profile)
            consultas_service.set_user_context(user_id, user_profile)
            
            self._services_configured = True
            self._last_configured_user_id = user_id
            
            print(f"[DEBUG] ✅ Servicios configurados exitosamente para: {self.user_role}")
            return True
            
        except Exception as e:
            print(f"[ERROR] ❌ Error configurando servicios: {e}")
            return False

    def _ensure_services_configured(self):
        """Asegura que los servicios estén configurados antes de usarlos"""
        success = self._configure_services()
        
        if not success:
            print("[DEBUG] ⚠️ No se pudieron configurar servicios - usuario no listo")
            # Intentar una vez más en caso de timing
            if self.is_authenticated and self.user_role and self.user_profile:
                print("[DEBUG] 🔄 Reintentando configuración de servicios...")
                return self._configure_services()
        
        return success

    # NUEVO: Método para forzar reconfiguración cuando cambie el usuario
    def _reset_services_configuration(self):
        """Resetea la configuración de servicios (útil cuando cambia el usuario)"""
        self._services_configured = False
        self._last_configured_user_id = ""
        print("[DEBUG] 🔄 Configuración de servicios reseteada")
    
    # ==========================================
    # MÉTODOS AUXILIARES COMUNES 
    # ==========================================
    
    def _get_current_user_id(self) -> str:
        """Obtener ID del usuario actual de forma segura"""
        # OPCIÓN 1: Intentar desde user_profile primero
        if self.user_profile and isinstance(self.user_profile, dict):
            # Probar diferentes estructuras posibles
            user_id = (
                self.user_profile.get("id") or 
                self.user_profile.get("user_id") or
                self.user_profile.get("usuario_id") or
                ""
            )
            if user_id:
                return str(user_id)
        
        # OPCIÓN 2: Fallback a current_user si existe
        if hasattr(self, 'current_user') and self.current_user:
            return str(self.current_user.get("id", ""))
        
        print("[DEBUG] ⚠️ No se pudo extraer user_id")
        return ""
    
    def _get_current_user_name(self) -> str:
        """Obtener nombre del usuario actual de forma segura - CORREGIDO"""
        # OPCIÓN 1: Usar user_display_name si existe (desde AuthState)
        if hasattr(self, 'user_display_name'):
            return self.user_display_name
        
        # OPCIÓN 2: Extraer desde user_profile
        if self.user_profile and isinstance(self.user_profile, dict):
            # Probar diferentes claves posibles
            name = (
                self.user_profile.get("nombre_completo") or
                self.user_profile.get("name") or
                self.user_profile.get("full_name") or
                ""
            )
            if name:
                return name
        
        # OPCIÓN 3: Extraer desde current_user
        if hasattr(self, 'current_user') and self.current_user:
            email = self.current_user.get("email", "")
            if email:
                return email.split("@")[0].title()
        
        return "Usuario"
    
    def _get_current_user_role(self) -> str:
        """Obtener rol del usuario actual"""
        # OPCIÓN 1: Usar user_role directamente desde AuthState (MÁS CONFIABLE)
        if hasattr(self, 'user_role') and self.user_role:
            print(f"[DEBUG] 🎯 Rol extraído desde user_role: '{self.user_role}'")
            return self.user_role
        
        # OPCIÓN 2: Extraer desde user_profile (FALLBACK)
        if self.user_profile and isinstance(self.user_profile, dict):
            # Probar diferentes estructuras posibles
            rol = (
                self.user_profile.get("rol_nombre") or  # Estructura plana
                self.user_profile.get("rol", {}).get("nombre") or  # Estructura anidada
                self.user_profile.get("role") or  # En inglés
                ""
            )
            if rol:
                print(f"[DEBUG] 🎯 Rol extraído desde user_profile: '{rol}'")
                return rol
        
        # OPCIÓN 3: Extraer desde current_user (ÚLTIMO RECURSO)
        if hasattr(self, 'current_user') and self.current_user:
            rol = self.current_user.get("rol", {}).get("nombre", "")
            if rol:
                print(f"[DEBUG] 🎯 Rol extraído desde current_user: '{rol}'")
                return rol
        
        print("[DEBUG] ⚠️ No se pudo extraer rol del usuario")
        return ""
    
    # ==========================================
    # NAVEGACIÓN COMÚN
    # ==========================================
    
    current_page: str = "dashboard"
    sidebar_collapsed: bool = False
    
    def toggle_sidebar(self):
        """Alternar el estado del sidebar"""
        self.sidebar_collapsed = not self.sidebar_collapsed
    
    # ==========================================
    # CARGA DE DASHBOARD (MÉTODO COMÚN CORREGIDO)
    # ==========================================
    
    async def load_dashboard_data(self):
        """
        Cargar datos del dashboard usando servicio centralizado
        CORREGIDO: Mejor verificación de usuario
        """
        # CORREGIDO: Usar método mejorado para obtener rol
        user_role = self._get_current_user_role()
        print(f"[DEBUG] Cargando dashboard para rol: '{user_role}'")
        
        # NUEVO: Verificación más robusta
        if not self.is_authenticated:
            self.show_error("Debe iniciar sesión para acceder al dashboard")
            return
        
        if not user_role:
            print("[WARNING] ⚠️ Rol de usuario vacío, intentando debug...")
            self._debug_user_state()
            self.show_error("Error: No se pudo determinar el rol del usuario")
            return
        
        self.set_loading(True)
        
        try:
            # Asegurar que servicios estén configurados CON verificación
            if not self._ensure_services_configured():
                self.show_error("Error: No se pudieron configurar los servicios correctamente")
                return
            
            # Obtener estadísticas usando servicio centralizado
            stats = await dashboard_service.get_dashboard_stats(user_role)
            
            # Aplicar estadísticas al estado específico (implementado por subclases)
            await self._apply_dashboard_stats(stats)
            
            print(f"[DEBUG] ✅ Dashboard cargado exitosamente para {user_role}: {stats}")
            
        except Exception as e:
            print(f"[ERROR] ❌ Error cargando dashboard: {e}")
            self.show_error(f"Error cargando datos del dashboard: {str(e)}")
        finally:
            self.set_loading(False)

    def _debug_user_state(self):
        """Debug del estado del usuario para diagnóstico"""
        print("[DEBUG] 🔍 ===== DEBUG DEL ESTADO DEL USUARIO =====")
        print(f"[DEBUG] - is_authenticated: {getattr(self, 'is_authenticated', 'NO_EXISTE')}")
        print(f"[DEBUG] - user_role: '{getattr(self, 'user_role', 'NO_EXISTE')}'")
        print(f"[DEBUG] - user_profile type: {type(getattr(self, 'user_profile', None))}")
        
        if hasattr(self, 'user_profile') and self.user_profile:
            print(f"[DEBUG] - user_profile keys: {list(self.user_profile.keys()) if isinstance(self.user_profile, dict) else 'NO_ES_DICT'}")
            if isinstance(self.user_profile, dict):
                # Buscar claves que contengan 'rol'
                rol_keys = [k for k in self.user_profile.keys() if 'rol' in k.lower()]
                print(f"[DEBUG] - claves con 'rol': {rol_keys}")
                for key in rol_keys:
                    print(f"[DEBUG] - {key}: {self.user_profile[key]}")
        
        print(f"[DEBUG] - current_user: {getattr(self, 'current_user', 'NO_EXISTE')}")
        print("[DEBUG] =============================================")

    async def _apply_dashboard_stats(self, stats: Dict[str, Any]):
        """
        Método abstracto que debe implementar cada subclase
        para aplicar las estadísticas a sus modelos específicos
        """
        pass  # Implementado por BossState y AdminState
    
    # ==========================================
    # GESTIÓN DE PACIENTES COMÚN (CORREGIDA)
    # ==========================================
    
    # Variables de estado comunes
    pacientes_search: str = ""
    pacientes_filter_genero: str = ""
    pacientes_filter_activos: str = "activos"
    pacientes_list: List[PacienteModel] = []
    
    async def load_pacientes_data(self):
        """
        Cargar datos de pacientes usando servicio centralizado
        CORREGIDO: Mejor verificación de permisos y usuario
        """
        user_role = self._get_current_user_role()
        print(f"[DEBUG] Cargando pacientes, rol: '{user_role}'")
        
        # NUEVO: Verificación más robusta
        if not self.is_authenticated:
            self.show_error("Debe iniciar sesión para acceder a pacientes")
            return
        
        if not user_role:
            print("[WARNING] ⚠️ Rol vacío al cargar pacientes, ejecutando debug...")
            self._debug_user_state()
            self.show_error("Error: No se pudo determinar el rol del usuario")
            return
        
        # Verificar permisos específicos
        if not self.check_permission("pacientes", "leer"):
            self.show_error(f"El rol '{user_role}' no tiene permisos para ver pacientes")
            return
        
        self.set_loading(True)
        
        try:
            # Asegurar que servicios estén configurados
            if not self._ensure_services_configured():
                self.show_error("Error: No se pudieron configurar los servicios correctamente")
                return
            
            # Usar servicio centralizado
            pacientes = await pacientes_service.get_filtered_patients(
                search=self.pacientes_search if self.pacientes_search else None,
                genero=self.pacientes_filter_genero if self.pacientes_filter_genero != "todos" else None,
                activos_only=self.pacientes_filter_activos == "activos"
            )
            
            # Aplicar a estado específico
            self.pacientes_list = pacientes
            print(f"[DEBUG] ✅ Pacientes cargados exitosamente: {len(pacientes)} registros")

        except Exception as e:
            print(f"[ERROR] ❌ Error cargando pacientes: {e}")
            self.show_error(f"Error cargando pacientes: {str(e)}")
        finally:
            self.set_loading(False)
    
    async def _apply_pacientes_data(self, pacientes: List ):
        """Método que implementan las subclases para aplicar datos de pacientes"""
        print("---------------------------------------")
        print(pacientes)
        pass
    
    # Métodos de filtros comunes
    def set_pacientes_search(self, search_term: str):
        """Establecer término de búsqueda"""
        self.pacientes_search = search_term
    
    def set_pacientes_filter_genero(self, genero: str):
        """Establecer filtro por género"""
        self.pacientes_filter_genero = genero
    
    def set_pacientes_filter_activos(self, activos: str):
        """Establecer filtro por estado activo"""
        self.pacientes_filter_activos = activos
    
    @rx.event
    async def apply_pacientes_filters(self):
        """Aplicar filtros y recargar datos"""
        await self.load_pacientes_data()
    
    # ==========================================
    # GESTIÓN DE CONSULTAS COMÚN (CORREGIDA)
    # ==========================================
    
    # Variables de estado comunes
    consultas_search: str = ""
    consultas_filter_estado: str = "todos"
    consultas_filter_odontologo: str = "todos"
    consultas_list: List[ConsultaModel] = []
    odontologos_list:  List[PersonalModel] = []
    servicios_list:  List[ServicioModel] = []
                
    async def load_consultas_data(self):
        """
        Cargar datos de consultas usando servicio centralizado
        CORREGIDO: Mejor verificación de usuario
        """
        user_role = self._get_current_user_role()
        print(f"[DEBUG] Cargando consultas rol: '{user_role}'")
        
        if not self.is_authenticated or not user_role:
            self.show_error("Error: Usuario no válido para cargar consultas")
            return
        
        self.set_loading(True)
        
        try:
            # Asegurar que servicios estén configurados
            if not self._ensure_services_configured():
                self.show_error("Error: No se pudieron configurar los servicios correctamente")
                return
            
            # Usar servicio centralizado
            consultas = await consultas_service.get_today_consultations(
                odontologo_id=self.consultas_filter_odontologo if self.consultas_filter_odontologo != "todos" else None)
            
            # Aplicar filtros adicionales en memoria si es necesario
            if self.consultas_filter_estado != "todos":
                consultas = [c for c in consultas if c.estado == self.consultas_filter_estado]
            
            # Aplicar a estado específico
            self.consultas_list = consultas
            print(f"[DEBUG] ✅ Consultas cargadas exitosamente: {len(consultas)} registros")     
            
            try:
                support_data = await self.get_support_data_for_consultas()
                self.odontologos_list = [PersonalModel.from_dict(item) for item in  support_data.get("odontologos", [])]
                print("=========================================================")
                print(self.odontologos_list)
                self.servicios_list = [ServicioModel.from_dict(item) for item in support_data.get("servicios", [])]
                print(f"[DEBUG] ✅ Datos de apoyo cargados: {len(self.odontologos_list)} odontólogos, {len(self.servicios_list)} servicios")
            except Exception as e:
                print(f"[ERROR] Error cargando datos de apoyo: {e}")
            
        except Exception as e:
            print(f"[ERROR] ❌ Error cargando consultas: {e}")
            self.show_error(f"Error cargando consultas: {str(e)}")
        finally:
            self.set_loading(False)
    
    
    # Métodos de filtros comunes
    def set_consultas_search(self, search_term: str):
        """Establecer término de búsqueda de consultas"""
        self.consultas_search = search_term
    
    def set_consultas_filter_estado(self, estado: str):
        """Establecer filtro por estado de consultas"""
        self.consultas_filter_estado = estado
    
    def set_consultas_filter_odontologo(self, odontologo_id: str):
        """Establecer filtro por odontólogo"""
        self.consultas_filter_odontologo = odontologo_id
    
    @rx.event
    async def apply_consultas_filters(self):
        """Aplicar filtros y recargar datos"""
        await self.load_consultas_data()
    
    # ==========================================
    # MANEJO DE MODALES COMÚN
    # ==========================================
    
    def clear_global_message(self):
        """Limpiar mensajes globales - común a todos los modales"""
        super().clear_global_message()
    
    # ==========================================
    # MÉTODOS DE NAVEGACIÓN COMUNES
    # ==========================================
    
    async def navigate_to_dashboard(self):
        """Navegar al dashboard"""
        self.current_page = "dashboard"
        self.clear_global_message()
        await self.load_dashboard_data()
    
    async def navigate_to_pacientes(self):
        """Navegar a pacientes"""
        self.current_page = "pacientes"
        self.clear_global_message()
        await self.load_pacientes_data()
    
    async def navigate_to_consultas(self):
        """Navegar a consultas"""
        self.current_page = "consultas"
        self.clear_global_message()
        await self.load_consultas_data()
    
    # ==========================================
    # OPERACIONES DE SERVICIOS EXPUESTAS
    # ==========================================
    
    async def get_support_data_for_consultas(self):
        """Obtener datos de apoyo para consultas (odontólogos, servicios)"""
        try:
            self._ensure_services_configured()
            return await consultas_service.get_support_data()
        except Exception as e:
            self.show_error(f"Error obteniendo datos de apoyo: {str(e)}")
            return {"odontologos": [], "servicios": []}
    
    # ==========================================
    # VALIDACIONES COMUNES
    # ==========================================
    
    def validate_form_data(self, form_data: Dict[str, str], required_fields: List[str]) -> List[str]:
        """Valida datos de formulario"""
        missing_fields = []
        
        for field in required_fields:
            if field not in form_data or not form_data[field] or (isinstance(form_data[field], str) and not form_data[field].strip()):
                missing_fields.append(field)
        
        return missing_fields
    
    def format_validation_error(self, base_message: str, missing_fields: List[str]) -> str:
        """Formatea errores de validación"""
        if missing_fields:
            return f"{base_message}. Campos requeridos: {', '.join(missing_fields)}"
        return base_message
    
    # ==========================================
    # GESTIÓN DE ESTADO DE CARGA Y MENSAJES
    # ==========================================
    
    def show_success_and_reload(self, message: str, reload_method):
        """Muestra mensaje de éxito y recarga datos"""
        self.show_success(message)
    
    def handle_service_error(self, error: Exception, context: str = ""):
        """Maneja errores de servicios de forma consistente"""
        error_msg = str(error)
        
        if "PermissionError" in error_msg or "sin permisos" in error_msg.lower():
            self.show_error("No tiene permisos para realizar esta acción")
        elif "ValueError" in error_msg:
            clean_msg = error_msg.replace("ValueError: ", "").replace("Error inesperado: ", "")
            self.show_error(clean_msg)
        else:
            context_msg = f" en {context}" if context else ""
            self.show_error(f"Error{context_msg}: {error_msg}")
    
    # ==========================================
    # PROPIEDADES COMPUTADAS COMUNES (CORREGIDAS)
    # ==========================================
    
    @rx.var
    def user_can_create_patients(self) -> bool:
        """Verifica si el usuario puede crear pacientes"""
        return self.check_permission("pacientes", "crear")
    
    @rx.var
    def user_can_create_consultations(self) -> bool:
        """Verifica si el usuario puede crear consultas"""
        return self.check_permission("consultas", "crear")
    
    @rx.var
    def user_can_manage_payments(self) -> bool:
        """Verifica si el usuario puede gestionar pagos"""
        return self.check_permission("pagos", "crear")
    
    @rx.var
    def current_user_display_name(self) -> str:
        """Nombre para mostrar del usuario actual"""
        return self._get_current_user_name()
    
    @rx.var
    def current_user_role_display(self) -> str:
        """Rol para mostrar del usuario actual"""
        role_map = {
            "gerente": "Gerente",
            "administrador": "Administrador",
            "odontologo": "Odontólogo", 
            "asistente": "Asistente"
        }
        return role_map.get(self._get_current_user_role(), "Usuario")
    
    # ==========================================
    # MÉTODOS DE INICIALIZACIÓN
    # ==========================================
    
    async def on_load_shared(self):
        """Inicialización común que pueden llamar las subclases"""
        print("[DEBUG] 🚀 Inicializando SharedManagerState...")
        
        # Resetear configuración de servicios para asegurar reconfiguración
        self._reset_services_configuration()
        
        # Debug del estado inicial
        user_role = self._get_current_user_role()
        print(f"[DEBUG] - Rol detectado en inicialización: '{user_role}'")
        
        # Cargar dashboard
        return self.load_dashboard_data()