"""
Estado Unificado del Sistema Dental - REEMPLAZO COMPLETO
Elimina herencia compleja (BossState, AdminState, SharedManagerState)
Centraliza toda la lógica en un solo estado claro y mantenible
"""

import reflex as rx
import datetime
from datetime import date, datetime as dt
from typing import List, Dict, Any, Optional, Union
import asyncio
# Servicios especializados (mantenidos separados según preferencia)
from dental_system.services.dashboard_service import dashboard_service
from dental_system.services.pacientes_service import pacientes_service
from dental_system.services.consultas_service import consultas_service
from dental_system.services.personal_service import personal_service

# Modelos tipados existentes
from dental_system.models import (
    PacienteModel,
    ConsultaModel,
    ServicioModel,
    PersonalModel,
    DashboardStatsModel,
    PacientesStatsModel,
    PagosStatsModel,
    AdminStatsModel
)

class AppState(rx.State):
    """
    🎯 ESTADO UNIFICADO - Reemplaza BossState, AdminState, SharedManagerState
    
    Características:
    ✅ Sin herencia múltiple
    ✅ Métodos con nombres claros
    ✅ Conexión real a Supabase
    ✅ Estructura preparada para intervenciones
    ✅ Permisos por rol integrados
    ✅ Servicios separados (dashboard_service, pacientes_service, etc.)
    """
    
    # ==========================================
    # 🔐 AUTENTICACIÓN Y SEGURIDAD
    # ==========================================
    is_authenticated: bool = False
    user_id: str = ""
    user_email: str = ""
    user_role: str = ""  # gerente, administrador, odontologo, asistente
    user_profile: Dict[str, Any] = {}
    
    # Control de sesión
    session_token: str = ""
    last_activity: str = ""
    login_error: str = ""
    is_loading_auth: bool = False
    
    # ==========================================
    # 📊 DATOS DEL DASHBOARD 
    # ==========================================
    dashboard_stats: DashboardStatsModel = DashboardStatsModel()
    pacientes_stats: PacientesStatsModel = PacientesStatsModel()
    pagos_stats: PagosStatsModel = PagosStatsModel()
    admin_stats: AdminStatsModel = AdminStatsModel()
    
    # Estado de carga del dashboard
    is_loading_dashboard: bool = False
    dashboard_error: str = ""
    
    # ==========================================
    # 👥 GESTIÓN DE PACIENTES (ADMIN + GERENTE)
    # ==========================================
    pacientes_list: List[Dict[str, Any]] = []
    selected_paciente: Dict[str, Any] = {}
    show_paciente_modal: bool = False
    is_loading_pacientes: bool = False
    pacientes_error: str = ""
    
    # Formulario de paciente con campos separados (estructura exacta mantenida)
    paciente_form: Dict[str, str] = {
        # Nombres separados
        "primer_nombre": "",
        "segundo_nombre": "",
        "primer_apellido": "",
        "segundo_apellido": "",
        
        # Documentación
        "numero_documento": "",
        "tipo_documento": "CC",
        "fecha_nacimiento": "",
        "genero": "",
        
        # Teléfonos separados
        "telefono_1": "",
        "telefono_2": "",
        
        # Contacto y ubicación
        "email": "",
        "direccion": "",
        "ciudad": "",
        "departamento": "",
        "ocupacion": "",
        "estado_civil": "",
        
        # Información médica
        "alergias": "",
        "medicamentos_actuales": "",
        "condiciones_medicas": "",
        "antecedentes_familiares": "",
        "observaciones": ""
    }
    
    # Confirmación de eliminación de pacientes
    show_delete_paciente_confirmation: bool = False
    paciente_to_delete: Dict[str, Any] = {}
    
    # Confirmación de reactivación de pacientes
    show_reactivate_paciente_confirmation: bool = False
    paciente_to_reactivate: Dict[str, Any] = {}

    
    # Filtros y búsqueda de pacientes
    pacientes_search: str = ""
    pacientes_filter_genero: str = ""
    pacientes_filter_activos: str = "activos"
    # ==========================================
    # 📅 GESTIÓN DE CONSULTAS (ADMIN + GERENTE)
    # ==========================================
    consultas_list: List[Dict[str, Any]] = []
    selected_consulta: Dict[str, Any] = {}
    show_consulta_modal: bool = False
    is_loading_consultas: bool = False
    consultas_error: str = ""
    
    # Formulario de consulta
    consulta_form: Dict[str, str] = {
        "paciente_id": "",
        "paciente_nombre": "",  # Para mostrar en el input
        "odontologo_id": "",
        "fecha_programada": "",
        "hora_programada": "",
        "tipo_consulta": "general",
        "motivo_consulta": "",
        "observaciones_cita": "",
        "prioridad": "normal",
        "estado": "programada" # Solo programada por defecto
    }
    
    # Confirmación de eliminación de consultas
    show_cancel_confirmation: bool = False
    consulta_to_cancel: Dict[str, Any] = {}
    motivo_cancelacion: str = ""
    
    # Filtros y búsqueda de consultas
    consultas_search: str = ""
    consultas_filter_estado: str = "Todos"  # Todos, Programada, En Progreso, Completada, Cancelada (SIN confirmada)
    consultas_filter_odontologo: str = "Todos"
    consultas_filter_tipo: str = "Todos"  # general, control, urgencia, cirugia, otro
    consultas_filter_fecha_inicio: str = ""  # YYYY-MM-DD
    consultas_filter_fecha_fin: str = ""    # YYYY-MM-DD""
    
    # ✅ BUSCADOR DE PACIENTES PARA MODAL
    pacientes_search_modal: str = ""
    pacientes_disponibles: List[Dict[str, Any]] = []
    show_pacientes_dropdown: bool = False
    selected_paciente_modal: Dict[str, Any] = {}
    
    # ✅ LISTA DE ODONTÓLOGOS PARA FILTROS
    odontologos_list: List[Dict[str, Any]] = []
    
    # ==========================================
    # 🦷 INTERVENCIONES (ESTRUCTURA BASE PREPARADA)
    # ==========================================
    intervenciones_list: List[Dict[str, Any]] = []
    selected_intervencion: Dict[str, Any] = {}
    show_intervencion_modal: bool = False
    is_loading_intervenciones: bool = False
    
    # Formulario de intervención (estructura base)
    intervencion_form: Dict[str, str] = {
        "consulta_id": "",
        "odontologo_id": "",  # Puede ser diferente por intervención
        "servicio_id": "",    # Puede ser diferente por intervención
        "diente_numero": "",
        "superficie": "",
        "descripcion": "",
        "costo_base": "",
        "descuento": "0",
        "costo_total": "",    # Para pago individual
        "estado": "planificada",  # planificada, en_proceso, completada
        "observaciones": ""
    }
    
    # ==========================================
    # 🏥 GESTIÓN DE SERVICIOS (SOLO GERENTE)
    # ==========================================
    servicios_list: List[Dict[str, Any]] = []
    selected_servicio: Dict[str, Any] = {}
    show_servicio_modal: bool = False
    is_loading_servicios: bool = False
    
    # Formulario de servicio
    servicio_form: Dict[str, str] = {
        "nombre": "",
        "descripcion": "",
        "precio_base": "",
        "duracion_estimada": "",
        "categoria": "",
        "requiere_anestesia": "false",
        "observaciones": ""
    }
    
    # Confirmación de eliminación de servicios
    show_delete_servicio_confirmation: bool = False
    servicio_to_delete: Dict[str, Any] = {}
    
    # ==========================================
    # 👨‍⚕️ GESTIÓN DE PERSONAL 
    # ==========================================
    personal_list: List[Dict[str, Any]] = []
    selected_personal: Dict[str, Any] = {}
    show_personal_modal: bool = False
    is_loading_personal: bool = False
    
    # Estados adicionales necesarios (agregar a la sección de estados)
    personal_search: str = ""
    personal_filter_tipo: str = "Todos"
    personal_filter_estado: str = "Todos"
    
    # Estados para estadísticas
    personal_activos: int = 0
    total_odontologos: int = 0
    otros_roles: int = 0
    
    # Formulario de personal con campos separados
    personal_form: Dict[str, str] = {
        "primer_nombre": "",
        "segundo_nombre": "",
        "primer_apellido": "",
        "segundo_apellido": "",
        "email": "",
        "telefono": "",
        "tipo_personal": "",  # odontologo, asistente, administrador
        "especialidad": "",
        "numero_licencia": "",
        "numero_documento": "",
        "celular": "",
        "direccion": "",
        "salario": "",
        "password": ""
    }
    
    # Confirmación de eliminación de personal
    show_delete_personal_confirmation: bool = False
    personal_to_delete: Dict[str, Any] = {}
    
    # Confirmación de reactivación de personal
    show_reactivate_personal_confirmation: bool = False
    personal_to_reactivate: Dict[str, Any] = {}

    
    # ==========================================
    # 🔐 AUTENTICACIÓN - TODO EN UN LUGAR
    # ==========================================
    
    # Estados de autenticación

    current_user: Dict[str, Any] = {}
    user_permissions: List[str] = []
    
    # ==========================================
    # 🧭 NAVEGACIÓN SIMPLE
    # ==========================================
    
    current_page: str = "dashboard"  # dashboard, pacientes, consultas, odontologia
    
    @rx.event
    async def navigate_to(self, page: str):
        """🧭 Navegar a una página - SIMPLE Y CLARO"""
        # Verificar permisos básicos
        if not self._can_access_page(page):
            self.show_error(f"No tienes permisos para acceder a {page}")
            return
        
        self.current_page = page
        await self._load_page_data(page)
        
    def _can_access_page(self, page: str) -> bool:
        """🔒 Verificar permisos - LÓGICA SIMPLE"""
        if not self.is_authenticated:
            return page == "login"
        
        # Permisos por rol - CLARO Y SIMPLE
        permissions = {
            "gerente": ["dashboard", "pacientes", "consultas", "personal", "reportes", "odontologia"],
            "administrador": ["dashboard", "pacientes", "consultas", "pagos"],
            "odontologo": ["dashboard", "pacientes", "consultas", "odontologia"],
            "asistente": ["dashboard", "consultas"]
        }
        
        allowed_pages = permissions.get(self.user_role, ["dashboard"])
        return page in allowed_pages
    
    async def _load_page_data(self, page: str):
        """📊 Cargar datos específicos de cada página"""
        if page == "pacientes":
            await self.load_pacientes_list()
        elif page == "consultas":
            await self.load_consultas_list()
        # elif page == "odontologia":
        # 
    # ==========================================
    # 🔑 MÉTODOS DE AUTENTICACIÓN
    # ==========================================

    @rx.event
    async def login(self, form_data: Dict[str, Any]) -> None:
        """🔐 Login corregido con redirección por rol"""
        print("=" * 60)
        print("🎯 LOGIN INICIADO - REDIRECCIÓN POR ROL")
        print(f"📝 Datos del formulario: {form_data}")
        print("=" * 60)
        
        self.is_loading_auth = True
        self.login_error = ""
        
        try:
            # Extraer credenciales
            email = form_data.get("email", "").strip().lower()
            password = form_data.get("password", "").strip()
            
            print(f"📧 Email: {email}")
            print(f"🔒 Password length: {len(password)}")
            
            if not email or not password:
                self.login_error = "Email y contraseña son requeridos"
                print("❌ Credenciales vacías")
                return
            
            # Importar y usar SupabaseAuth
            from dental_system.supabase.auth import SupabaseAuth
            auth_client = SupabaseAuth()
            
            print("🔄 Ejecutando sign_in...")
            session, user_info = auth_client.sign_in(email, password)

            if session and user_info:
                print("✅ Autenticación exitosa!")
                
                # Actualizar estado
                self.is_authenticated = True
                self.user_id = user_info["id"]
                self.user_email = user_info["email"]
                self.user_role = user_info["rol"]["nombre"]
                self.user_profile = user_info
                self.current_user = user_info  # ✅ NUEVO: Sincronizar current_user
                
                print(f"👤 Usuario: {self.user_email}")
                print(f"🎭 Rol: {self.user_role}")
                
                # 🎯 DETERMINAR RUTA SEGÚN ROL - AQUÍ ESTÁ LA CORRECCIÓN
                dashboard_route = self.get_dashboard_route()
                print(f"🚀 Redirigiendo a: {dashboard_route}")
                
                # ✅ INICIALIZAR current_page según el rol
                if self.user_role == "gerente":
                    self.current_page = "dashboard"  # Página inicial para gerente
                elif self.user_role == "administrador":
                    self.current_page = "dashboard"  # Página inicial para admin
                elif self.user_role == "odontologo":
                    self.current_page = "dashboard"  # Página inicial para odontólogo
                else:
                    self.current_page = "dashboard"  # Por defecto
                
                # 🔄 CARGAR DATOS INICIALES
                await self.load_initial_data()
                
                # 🚀 REDIRECCIÓN CORREGIDA - USA LA RUTA POR ROL
                return rx.redirect(dashboard_route)
                
            else:
                self.login_error = "Credenciales inválidas"
                print("❌ Credenciales inválidas")
                
        except Exception as e:
            error_msg = f"Error de autenticación: {str(e)}"
            self.login_error = error_msg
            print(f"💥 Error: {error_msg}")
            
        finally:
            self.is_loading_auth = False
            print("🔄 Login process finalizado")
        
    @rx.event
    async def logout_user(self):
        """Cerrar sesión y limpiar estado"""
        # Limpiar datos de autenticación
        self.is_authenticated = False
        self.user_id = ""
        self.user_email = ""
        self.user_role = ""
        self.user_profile = {}
        self.current_user = {}  
        self.session_token = ""
        self.current_page = "dashboard"  
        
        # Limpiar datos del dashboard
        self.dashboard_stats = DashboardStatsModel()
        self.pacientes_list = []
        self.consultas_list = []
        self.servicios_list = []
        self.personal_list = []
        
        print("✅ Sesión cerrada correctamente")
        return rx.redirect("/login")

    def get_dashboard_route(self) -> str:
    # 🎯 Determinar ruta del dashboard según el rol - MEJORADO
        route_map = {
            "gerente": "/boss",
            "administrador": "/admin", 
            "odontologo": "/dentist",
            "asistente": "/dentist"  # Asistentes también van a /dentist
        }
    
        route = route_map.get(self.user_role, "/")
        print(f"🎯 Rol '{self.user_role}' → Ruta '{route}'")
        return route
    
    @rx.event 
    async def sync_user_state(self):
        """🔄 Sincronizar estado del usuario después del login"""
        if self.is_authenticated and self.user_profile:
            # Asegurar que current_user esté sincronizado
            self.current_user = self.user_profile
            
            # Asegurar que current_page esté inicializada
            if not self.current_page or self.current_page == "":
                self.current_page = "dashboard"
            
            print(f"🔄 Estado sincronizado - Usuario: {self.user_email}, Rol: {self.user_role}, Página: {self.current_page}")

    # ==========================================
    # 📊 MÉTODOS DEL DASHBOARD
    # ==========================================
    
    @rx.event
    async def load_initial_data(self):
        """Cargar datos iniciales según el rol del usuario"""
        self.is_loading_dashboard = True
        
        try:
            # Cargar stats del dashboard
            await self.load_dashboard_stats()
            
            # Cargar datos específicos según permisos
            if self.user_role in ["gerente", "administrador"]:
                await self.load_pacientes_list()
                await self.load_consultas_list()
                
            if self.user_role == "gerente":
                await self.load_servicios_list()
                await self.load_personal_list()
                
        except Exception as e:
            self.dashboard_error = f"Error cargando datos: {str(e)}"
        finally:
            self.is_loading_dashboard = False
    
    @rx.event
    async def load_dashboard_stats(self):
        """Cargar estadísticas del dashboard usando servicios reales"""
        try:
            # Configurar servicios con contexto del usuario
            dashboard_service.set_user_context(self.user_id, self.user_profile)
            pacientes_service.set_user_context(self.user_id, self.user_profile)
            
            # Obtener estadísticas base
            base_stats = await dashboard_service._get_base_statistics()
            
            # Obtener estadísticas de pacientes
            pacientes_stats = await pacientes_service.get_patient_stats()
            
            # Obtener estadísticas de pagos si es gerente
            pagos_stats = {}
            if self.user_role == "gerente":
                pagos_stats = await dashboard_service.get_pagos_stats()
            
            # Actualizar modelos
            self.dashboard_stats = DashboardStatsModel(**base_stats)
            self.pacientes_stats = PacientesStatsModel(**pacientes_stats)
            if pagos_stats:
                self.pagos_stats = PagosStatsModel(**pagos_stats)
                
        except Exception as e:
            self.dashboard_error = f"Error cargando stats: {str(e)}"
    
    # ==========================================
    # 👥 MÉTODOS DE GESTIÓN DE PACIENTES
    # ==========================================
    
    @rx.event
    async def load_pacientes_list(self):
        """Cargar lista de pacientes usando servicio real"""
        if not self.has_pacientes_permission():
            return
            
        self.is_loading_pacientes = True
        try:
            # Configurar servicio con contexto del usuario
            pacientes_service.set_user_context(self.user_id, self.user_profile)
            
            activos_only = None  # Por defecto todos
            if self.pacientes_filter_activos == "Activos":
                activos_only = True  # Solo activos
            elif self.pacientes_filter_activos == "Inactivos":
                activos_only = False  # Solo inactivos
            # Si es "activos", mantener True
            
            # Usar método real que existe en pacientes_service
            pacientes = await pacientes_service.get_filtered_patients(
                search= self.pacientes_search,
                genero= self.pacientes_filter_genero,
                activos_only=activos_only
            )
            
            # Convertir modelos a diccionarios para el estado
            self.pacientes_list = [p.to_dict() if hasattr(p, 'to_dict') else p.__dict__ for p in pacientes]

        except Exception as e:
            self.pacientes_error = f"Error cargando pacientes: {str(e)}"
        finally:
            self.is_loading_pacientes = False
    
    @rx.event
    async def abrir_modal_paciente(self, paciente_id: str = ""):
        """Abrir modal para crear o editar paciente"""
        if not self.has_pacientes_permission():
            return
            
        if paciente_id:
            # Editar paciente existente
            paciente = next((p for p in self.pacientes_list if p["id"] == paciente_id), None)
            if paciente:
                self.selected_paciente = paciente
                # Cargar datos en el formulario
                for key, value in paciente.items():
                    if key in self.paciente_form:
                        self.paciente_form[key] = str(value) if value else ""
            else:
                self.show_error("Paciente no encontrado")
                return
        else:
            # Crear nuevo paciente
            self.selected_paciente = {}
            self.limpiar_formulario_paciente()
            
        self.show_paciente_modal = True
    
    @rx.event
    def cerrar_modal_paciente(self):
        """Cerrar modal de paciente"""
        self.show_paciente_modal = False
        self.selected_paciente = {}
        self.limpiar_formulario_paciente()
    
    @rx.event  
    def set_show_delete_paciente_confirmation(self, show: bool):
        """Controlar visibilidad del modal de confirmación"""
        self.show_delete_paciente_confirmation = show
    
    @rx.event
    async def guardar_paciente(self):
        """Guardar paciente usando servicio real"""
        if not self.has_pacientes_permission():
            return
            
        try:
            # Configurar servicio con contexto del usuario
            pacientes_service.set_user_context(self.user_id, self.user_profile)
            
            # Preparar datos del formulario
            paciente_data = {k: v for k, v in self.paciente_form.items() if v.strip()}
            
            if self.selected_paciente:
                # Actualizar paciente existente
                await pacientes_service.update_patient(
                    patient_id=self.selected_paciente["id"],
                    form_data=paciente_data
                )
            else:
                # Crear nuevo paciente
                await pacientes_service.create_patient(paciente_data,self.user_id)
            
            # Recargar lista y cerrar modal
            await self.load_pacientes_list()
            self.cerrar_modal_paciente()
                
        except Exception as e:
            self.pacientes_error = f"Error guardando paciente: {str(e)}"
        finally:
            self.loading = False
    
    @rx.event
    def confirmar_eliminar_paciente(self, paciente_id: str):
        """Mostrar confirmación para eliminar paciente"""
        paciente = next((p for p in self.pacientes_list if p["id"] == paciente_id), None)
        if paciente:
            self.paciente_to_delete = paciente
            self.show_delete_paciente_confirmation = True
    
    @rx.event
    async def eliminar_paciente(self):
        """Eliminar paciente usando servicio real"""
        if not self.has_pacientes_permission() or not self.paciente_to_delete:
            return
            
        try:
            # Configurar servicio con contexto del usuario
            pacientes_service.set_user_context(self.user_id, self.user_profile)
            
            # Usar método real que existe
            success = await pacientes_service.deactivate_patient(self.paciente_to_delete["id"])
           
            if success:
                nombre = f"{self.paciente_to_delete.get('primer_nombre', '')} {self.paciente_to_delete.get('primer_apellido', '')}"
                self.show_success(f"Paciente {nombre} eliminado exitosamente")
                await self.load_pacientes_list()
                self.show_delete_paciente_confirmation = False
                self.paciente_to_delete = {}
                
            # Recargar lista y cerrar confirmación
            else:
                self.show_error("Error eliminando paciente")
                
        except Exception as e:
            self.show_error(f"Error eliminando paciente: {str(e)}")
        finally:
            self.loading = False
        
        
    @rx.event
    def confirmar_reactivar_paciente(self, paciente_id: str):
        """Mostrar confirmación para reactivar paciente"""
        paciente = next((p for p in self.pacientes_list if p["id"] == paciente_id), None)
        if paciente:
            self.paciente_to_reactivate = paciente
            self.show_reactivate_paciente_confirmation = True

    @rx.event
    async def ejecutar_reactivar_paciente(self):
        """Ejecutar reactivación confirmada"""
        if not self.paciente_to_reactivate:
            return
        if not self.has_pacientes_permission():
            return
            
        try:
            print(f"🔄 Reactivando paciente: {self.paciente_to_reactivate["id"]}")
            
            # Configurar servicio con contexto del usuario
            pacientes_service.set_user_context(self.user_id, self.user_profile)
            
            # Reactivar usando el servicio
            success = await pacientes_service.reactivate_patient(self.paciente_to_reactivate["id"])
            
            if success:
                # Buscar el paciente en la lista para mostrar mensaje
                paciente = next((p for p in self.pacientes_list if p["id"] == self.paciente_to_reactivate["id"]), None)
                if paciente:
                    nombre = f"{paciente.get('primer_nombre', '')} {paciente.get('primer_apellido', '')}"
                    self.show_success(f"Paciente {nombre} reactivado exitosamente")
                else:
                    self.show_success("Paciente reactivado exitosamente")
                
                # Recargar lista para mostrar cambios
                await self.load_pacientes_list()
                 # Cerrar modal de confirmación
                self.show_reactivate_paciente_confirmation = False
                self.paciente_to_reactivate = {}
            else:
                self.show_error("Error reactivando paciente")
                
        except Exception as e:
            error_msg = f"Error reactivando paciente: {str(e)}"
            print(f"❌ {error_msg}")
            self.show_error(error_msg)
            

    @rx.event  
    def set_show_reactivate_paciente_confirmation(self, show: bool):
        """Controlar visibilidad del modal de confirmación de reactivación"""
        self.show_reactivate_paciente_confirmation = show
        
        
    def limpiar_formulario_paciente(self):
        """Limpiar formulario de paciente"""
        for key in self.paciente_form:
            self.paciente_form[key] = ""
    
    # ==========================================
    # 📅 MÉTODOS DE GESTIÓN DE CONSULTAS
    # ==========================================
    
    @rx.event
    async def load_consultas_list(self):
        """📅 MEJORADO: Cargar lista de consultas con mejor logging"""
        if not self.has_consultas_permission():
            return
            
        self.is_loading_consultas = True
        try:
            print("🔄 Cargando consultas...")
            consultas_service.set_user_context(self.user_id, self.user_profile)
            
            # Determinar fechas para filtro
            fecha_inicio = None
            fecha_fin = None
            
            if self.consultas_filter_fecha_inicio:
                from datetime import datetime
                fecha_inicio = datetime.strptime(self.consultas_filter_fecha_inicio, "%Y-%m-%d").date()
                
            if self.consultas_filter_fecha_fin:
                from datetime import datetime
                fecha_fin = datetime.strptime(self.consultas_filter_fecha_fin, "%Y-%m-%d").date()
            
            # Si no hay fechas específicas, usar consultas de hoy
            if not fecha_inicio and not fecha_fin:
                consultas = await consultas_service.get_today_consultations()
            else:
                # Usar filtros avanzados
                consultas = await consultas_service.get_filtered_consultations(
                    search=self.consultas_search if self.consultas_search else None,
                    estado=self.consultas_filter_estado.lower() if self.consultas_filter_estado != "Todos" else None,
                    odontologo_id=self.consultas_filter_odontologo if self.consultas_filter_odontologo != "Todos" else None,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
            
            # Convertir a diccionarios
            self.consultas_list = [c.to_dict() if hasattr(c, 'to_dict') else c.__dict__ for c in consultas]
            
            print(f"✅ Consultas cargadas: {len(self.consultas_list)} registros")
            self.odontologos_list = await self.get_support_data_for_consultas()
                   
        except Exception as e:
            error_msg = f"Error cargando consultas: {str(e)}"
            print(f"❌ {error_msg}")
            self.consultas_error = error_msg
            self.show_error(error_msg)
        finally:
            self.is_loading_consultas = False
    
    
    
    @rx.event
    async def abrir_modal_consulta(self, consulta_id: str = ""):
        """Abrir modal para crear o editar consulta"""
        if not self.has_consultas_permission():
            return
            
        if consulta_id:
            # Editar consulta existente
            consulta = next((c for c in self.consultas_list if c["id"] == consulta_id), None)
            if consulta:
                self.selected_consulta = consulta
                # Cargar datos en el formulario
                for key, value in consulta.items():
                    if key in self.consulta_form:
                        self.consulta_form[key] = str(value) if value else ""
        else:
            # Crear nueva consulta
            self.selected_consulta = {}
            self.limpiar_formulario_consulta()
            
        self.show_consulta_modal = True
    
    @rx.event
    async def guardar_consulta(self):
        """✅ CORREGIDO: Guardar consulta - Validación simplificada"""
        if not self.has_consultas_permission():
            return
            
        self.is_loading_consultas = True
        try:
            consultas_service.set_user_context(self.user_id, self.user_profile)
            
            # ✅ VALIDACIÓN BÁSICA CORREGIDA
            if not self.consulta_form.get("paciente_id"):
                self.show_error("Debe seleccionar un paciente")
                return
                
            if not self.consulta_form.get("motivo_consulta"):
                self.show_error("Debe especificar el motivo de consulta")
                return
            
            # ✅ VALIDACIÓN DE ODONTÓLOGO SIMPLIFICADA
            odontologo_id = self.consulta_form.get("odontologo_id", "")
            
            if not odontologo_id or odontologo_id.strip() == "":
                self.show_error("Debe seleccionar un odontólogo")
                return
            
            # ✅ VERIFICAR QUE EL ODONTÓLOGO EXISTE EN LA LISTA CARGADA
            odontologo_valido = False
            odontologo_nombre = "Desconocido"
            
            for odon in self.odontologos_list:
                if odon.get("id") == odontologo_id:
                    odontologo_valido = True
                    odontologo_nombre = odon.get("nombre_completo", "Sin nombre")
                    break
            
            if not odontologo_valido:
                self.show_error(f"Odontólogo no válido. ID: {odontologo_id}")
                print(f"🔍 DEBUG - Odontólogo ID: '{odontologo_id}'")
                print(f"🔍 DEBUG - Odontólogos disponibles:")
                for odon in self.odontologos_list:
                    print(f"  - ID: '{odon.get('id')}', Nombre: '{odon.get('nombre_completo')}'")
                return
            
            # ✅ PREPARAR DATOS CORRECTOS
            consulta_data = {
                "paciente_id": self.consulta_form["paciente_id"],
                "odontologo_id": odontologo_id,  # ✅ USAR EL ID DIRECTAMENTE
                "motivo_consulta": self.consulta_form["motivo_consulta"],
                "tipo_consulta": self.consulta_form.get("tipo_consulta", "general"),
                "prioridad": self.consulta_form.get("prioridad", "normal"),
                "observaciones_cita": self.consulta_form.get("observaciones_cita", "")
            }
            
            print(f"✅ Datos a enviar: {consulta_data}")
            
            if self.selected_consulta:
                # Actualizar
                result = await consultas_service.update_consultation(
                    self.selected_consulta["id"],
                    consulta_data
                )
            else:
                # Crear
                result = await consultas_service.create_consultation(
                    consulta_data,
                    self.user_id
                )
            
            if result:
                await self.load_consultas_list()
                self.cerrar_modal_consulta()
                
                action = "actualizada" if self.selected_consulta else "creada"
                self.show_success(f"Consulta {action} exitosamente para {odontologo_nombre}")
            else:
                self.show_error("Error guardando consulta")
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ Error guardando consulta: {error_msg}")
            self.show_error(error_msg)
        finally:
            self.is_loading_consultas = False
        
    @rx.event
    def cerrar_modal_consulta(self):
        """Cerrar modal de consulta"""
        self.show_consulta_modal = False
        self.selected_consulta = {}
        self.limpiar_formulario_consulta()
    
    @rx.event
    async def cambiar_estado_consulta(self, consulta_id: str, nuevo_estado: str):
        """🔄 Cambiar estado de consulta (sin 'confirmada')"""
        if not self.has_consultas_permission():
            return
            
        try:
            consultas_service.set_user_context(self.user_id, self.user_profile)
            
            success = await consultas_service.change_consultation_status(
                consulta_id, 
                nuevo_estado
            )
            
            if success:
                await self.load_consultas_list()
                
                # Mensaje específico según el estado
                estado_messages = {
                    "en_progreso": "Consulta iniciada",
                    "completada": "Consulta completada",
                    "cancelada": "Consulta cancelada"
                }
                
                self.show_success(estado_messages.get(nuevo_estado, f"Estado cambiado a {nuevo_estado}"))
            else:
                self.show_error("Error cambiando estado de consulta")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def limpiar_formulario_consulta(self):
        """Limpiar formulario de consulta"""
        for key in self.consulta_form:
            self.consulta_form[key] = ""
    
    @rx.event
    async def change_consulta_status(self, consulta_id: str, nuevo_estado: str):
        """Guardar consulta usando servicio real"""
        if not self.has_consultas_permission():
            return
        
        try:
            # Configurar servicio con contexto del usuario
            consultas_service.set_user_context(self.user_id, self.user_profile)
            
            success = await consultas_service.change_consultation_status(
                consulta_id, 
                nuevo_estado
            )
            
            if success:   
                await self.load_consultas_list()
            
        except Exception as e:
            self.handle_service_error(e, "cambiando estado de consulta")
        finally:
            self.set_loading(False)
    
    
        
    @rx.event
    async def ejecutar_cancelar_consulta(self):
        """Ejecutar la cancelación de consulta con motivo"""
        if not self.consulta_to_cancel or not self.has_consultas_permission():
            return
            
        try:
            consultas_service.set_user_context(self.user_id, self.user_profile)
            
            # Cancelar con motivo
            success = await consultas_service.cancel_consultation(
                self.consulta_to_cancel["id"], 
                self.motivo_cancelacion
            )
            
            if success:
                self.show_success("Consulta cancelada exitosamente")
                await self.load_consultas_list()
                self.set_show_cancel_confirmation(False)
            else:
                self.show_error("Error cancelando consulta")
                
        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    @rx.event
    def confirmar_cancelar_consulta(self, consulta_id: str):
        """Mostrar confirmación para cancelar consulta"""
        consulta = next((c for c in self.consultas_list if c["id"] == consulta_id), None)
        if consulta:
            self.consulta_to_cancel = consulta
            self.motivo_cancelacion = ""
            self.show_cancel_confirmation = True
        
    @rx.event
    def set_show_consulta_modal(self, show: bool):
        """Controlar visibilidad del modal de consulta"""
        self.show_consulta_modal = show
        if not show:
            self.cerrar_modal_consulta()

    @rx.event
    def set_show_cancel_confirmation(self, show: bool):
        """Controlar visibilidad del modal de confirmación de cancelación"""
        self.show_cancel_confirmation = show
        if not show:
            self.consulta_to_cancel = {}
            self.motivo_cancelacion = ""

    @rx.event
    def set_motivo_cancelacion(self, motivo: str):
        """Establecer motivo de cancelación"""
        self.motivo_cancelacion = motivo
    # ==========================================
    # 🔍 MÉTODOS DE BÚSQUEDA DE PACIENTES PARA MODAL
    # ==========================================
    
    @rx.event
    async def buscar_pacientes_modal(self, search_term: str):
        """🔍 Buscar pacientes simplificado"""
        self.pacientes_search_modal = search_term
        
        if len(search_term) >= 2:
            try:
                pacientes_service.set_user_context(self.user_id, self.user_profile)
                
                pacientes = await pacientes_service.get_filtered_patients(
                    search=search_term,
                    activos_only=True
                )
                
                # Convertir a formato simple
                self.pacientes_disponibles = []
                for p in pacientes[:10]:  # Solo 10 resultados
                    p_dict = p.to_dict() if hasattr(p, 'to_dict') else p.__dict__
                    self.pacientes_disponibles.append({
                        "id": p_dict.get("id"),
                        "primer_nombre": p_dict.get("primer_nombre", ""),
                        "primer_apellido": p_dict.get("primer_apellido", ""),
                        "numero_documento": p_dict.get("numero_documento", ""),
                        "display_text": f"{p_dict.get('primer_nombre', '')} {p_dict.get('primer_apellido', '')} - {p_dict.get('numero_documento', '')}"
                    })
                
                self.show_pacientes_dropdown = len(self.pacientes_disponibles) > 0
                
            except Exception as e:
                print(f"Error buscando: {e}")
                self.pacientes_disponibles = []
                self.show_pacientes_dropdown = False
        else:
            self.pacientes_disponibles = []
            self.show_pacientes_dropdown = False
    
    @rx.event
    def seleccionar_paciente_modal(self, paciente: Dict[str, Any]):
        """✅ Seleccionar paciente"""
        self.selected_paciente_modal = paciente
        self.consulta_form["paciente_id"] = paciente.get("id", "")
        self.pacientes_search_modal = paciente.get("display_text", "")
        self.show_pacientes_dropdown = False
    
    @rx.event
    def limpiar_seleccion_paciente(self):
        """🧹 Limpiar selección de paciente"""
        self.selected_paciente_modal = {}
        self.consulta_form["paciente_id"] = ""
        self.consulta_form["paciente_nombre"] = ""
        self.pacientes_search_modal = ""
        self.show_pacientes_dropdown = False    
        
    # ==========================================
    # 🏥 MÉTODOS DE GESTIÓN DE SERVICIOS (SOLO GERENTE)
    # ==========================================
    
    @rx.event
    async def load_servicios_list(self):
        """Cargar lista de servicios usando tablas directas"""
        if not self.has_servicios_permission():
            return
            
        self.is_loading_servicios = True
        try:
            # Usar tabla directa hasta que exista servicio específico
            from dental_system.supabase.tablas import services_table
            servicios_data = services_table.get_active_services()
            
            # Convertir a formato esperado
            self.servicios_list = []
            for servicio in servicios_data:
                self.servicios_list.append({
                    "id": servicio.get("id"),
                    "nombre": servicio.get("nombre", ""),
                    "descripcion": servicio.get("descripcion", ""),
                    "precio_base": servicio.get("precio_base", 0),
                    "categoria": servicio.get("categoria", ""),
                    "activo": servicio.get("activo", True)
                })
                
        except Exception as e:
            print(f"Error cargando servicios: {str(e)}")
            self.servicios_list = []
        finally:
            self.is_loading_servicios = False
    
    @rx.event
    async def load_personal_list(self):
        """Cargar lista de personal usando servicio real"""
        if not self.has_personal_permission():
            return
            
        self.is_loading_personal = True
        try:
            # Importar el servicio
            from dental_system.services.personal_service import personal_service
            
            # Configurar servicio con contexto del usuario
            personal_service.set_user_context(self.user_id, self.user_profile)
            
            # Convertir filtros
            activos_only = True
            if self.personal_filter_estado == "Todos":
                activos_only = None
            elif self.personal_filter_estado == "Inactivo":
                activos_only = False
            
            print(f"🔍 Cargando personal - Tipo: {self.personal_filter_tipo}, Estado: {self.personal_filter_estado}")
            
            # Obtener personal filtrado
            personal = await personal_service.get_filtered_personal(
                search=self.personal_search,
                tipo_personal=self.personal_filter_tipo if self.personal_filter_tipo != "Todos" else None,
                estado_laboral=self.personal_filter_estado.lower() if self.personal_filter_estado != "Todos" else None,
                activos_only=activos_only
            )
            
            # Convertir modelos a diccionarios para el estado
            self.personal_list = [p.to_dict() if hasattr(p, 'to_dict') else p.__dict__ for p in personal]
            
            # Actualizar estadísticas
            await self.update_personal_stats()
            
        except Exception as e:
            self.show_error(f"Error cargando personal: {str(e)}")
        finally:
            self.is_loading_personal = False
    
    @rx.event
    async def abrir_modal_personal(self, personal_id: str = ""):
        """Abrir modal para crear o editar personal"""
        if not self.has_personal_permission():
            return
            
        if personal_id:
            # Editar personal existente
            personal = next((p for p in self.personal_list if p["id"] == personal_id), None)
            if personal:
                self.selected_personal = personal
                # Cargar datos en el formulario
                for key, value in personal.items():
                    if key in self.personal_form:
                        self.personal_form[key] = str(value) if value else ""
                
                # Cargar datos del usuario relacionado si existe
                if "usuarios" in personal and personal["usuarios"]:
                    user_data = personal["usuarios"]
                    if isinstance(user_data, dict):
                        self.personal_form["email"] = user_data.get("email", "")
                        self.personal_form["telefono"] = user_data.get("telefono", "")
            else:
                self.show_error("Personal no encontrado")
                return
        else:
            # Crear nuevo personal
            self.selected_personal = {}
            self.limpiar_formulario_personal()
            
        self.show_personal_modal = True

    @rx.event
    def cerrar_modal_personal(self):
        """Cerrar modal de personal"""
        self.show_personal_modal = False
        self.selected_personal = {}
        self.limpiar_formulario_personal()

    @rx.event
    async def guardar_personal(self):
        """Guardar personal usando servicio real"""
        if not self.has_personal_permission():
            return
            
        try:
            # Importar el servicio
            from dental_system.services.personal_service import personal_service
            
            # Configurar servicio con contexto del usuario
            personal_service.set_user_context(self.user_id, self.user_profile)
            
            # Preparar datos del formulario
            personal_data = {k: v for k, v in self.personal_form.items() if v.strip()}
            
            if self.selected_personal:
                # Actualizar personal existente
                result = await personal_service.update_staff_member(
                    personal_id=self.selected_personal["id"],
                    form_data=personal_data
                )
            else:
                # Crear nuevo personal
                result = await personal_service.create_staff_member(
                    form_data=personal_data,
                    creator_user_id=self.user_id
                )
            
            if result:
                # Recargar lista y cerrar modal
                await self.load_personal_list()
                self.cerrar_modal_personal()
                
                action = "actualizado" if self.selected_personal else "creado"
                nombre = f"{personal_data.get('primer_nombre', '')} {personal_data.get('primer_apellido', '')}"
                self.show_success(f"Personal {nombre} {action} exitosamente")
            else:
                self.show_error("Error guardando personal")
                    
        except Exception as e:
            self.show_error(f"Error guardando personal: {str(e)}")

    @rx.event
    def confirmar_eliminar_personal(self, personal_id: str):
        """Mostrar confirmación para eliminar personal"""
        personal = next((p for p in self.personal_list if p["id"] == personal_id), None)
        if personal:
            self.personal_to_delete = personal
            self.show_delete_personal_confirmation = True

    @rx.event
    async def eliminar_personal(self):
        """Eliminar personal usando servicio real"""
        if not self.has_personal_permission() or not self.personal_to_delete:
            return
            
        try:     
            # Configurar servicio con contexto del usuario
            personal_service.set_user_context(self.user_id, self.user_profile)
            
            # Desactivar personal
            success = await personal_service.deactivate_staff_member(self.personal_to_delete["id"])
            
            if success:
                nombre = f"{self.personal_to_delete.get('primer_nombre', '')} {self.personal_to_delete.get('primer_apellido', '')}"
                self.show_success(f"Personal {nombre} desactivado exitosamente")
                await self.load_personal_list()
                self.show_delete_personal_confirmation = False
                self.personal_to_delete = {}
            else:
                self.show_error("Error desactivando personal")
                
        except Exception as e:
            self.show_error(f"Error desactivando personal: {str(e)}")

    @rx.event
    def confirmar_reactivar_personal(self, personal_id: str):
        """Mostrar confirmación para reactivar personal"""
        personal = next((p for p in self.personal_list if p["id"] == personal_id), None)
        if personal:
            self.personal_to_reactivate = personal
            self.show_reactivate_personal_confirmation = True

   
    @rx.event
    async def ejecutar_reactivar_personal(self):
        """Ejecutar reactivación confirmada"""
        if not self.personal_to_reactivate:
            return
        
        if not self.has_personal_permission():
            return
            
        try:
            # Configurar servicio con contexto del usuario
            personal_service.set_user_context(self.user_id, self.user_profile)
            
            # Reactivar personal
            success = await personal_service.reactivate_staff_member(self.personal_to_reactivate["id"])
            
            if success:
                # Buscar personal para mostrar mensaje
                personal = next((p for p in self.personal_list if p["id"] == self.personal_to_reactivate["id"]), None)
                if personal:
                    nombre = f"{personal.get('primer_nombre', '')} {personal.get('primer_apellido', '')}"
                    self.show_success(f"Personal {nombre} reactivado exitosamente")
                else:
                    self.show_success("Personal reactivado exitosamente")
                
                await self.load_personal_list()
                # Cerrar modal de confirmación
                self.show_reactivate_personal_confirmation = False
                self.personal_to_reactivate = {}
            else:
                self.show_error("Error reactivando personal")
                
        except Exception as e:
            self.show_error(f"Error reactivando personal: {str(e)}")
        
        

    def limpiar_formulario_personal(self):
        """Limpiar formulario de personal"""
        for key in self.personal_form:
            self.personal_form[key] = ""

    async def update_personal_stats(self):
        """Actualizar estadísticas de personal"""
        try:
            # Importar el servicio
            from dental_system.services.personal_service import personal_service
            
            # Configurar servicio
            personal_service.set_user_context(self.user_id, self.user_profile)
            
            # Obtener estadísticas
            stats = await personal_service.get_staff_stats()
            
            # Actualizar estado
            self.personal_activos = stats.get("activos", 0)
            self.total_odontologos = stats.get("odontologos", 0)
            self.otros_roles = stats.get("administradores", 0) + stats.get("asistentes", 0) + stats.get("gerentes", 0)
            
        except Exception as e:
            print(f"Error actualizando estadísticas de personal: {e}")
    
    # ==========================================
    # 🔐 MÉTODOS DE PERMISOS
    # ==========================================
    
    def has_pacientes_permission(self) -> bool:
        """Verificar si tiene permisos para gestionar pacientes"""
        return self.user_role in ["gerente", "administrador"]
    
    def has_consultas_permission(self) -> bool:
        """Verificar si tiene permisos para gestionar consultas"""
        return self.user_role in ["gerente", "administrador"]
    
    def has_servicios_permission(self) -> bool:
        """Verificar si tiene permisos para gestionar servicios"""
        return self.user_role == "gerente"
    
    def has_personal_permission(self) -> bool:
        """Verificar si tiene permisos para gestionar personal"""
        return self.user_role == "gerente"
    
    def has_intervenciones_permission(self) -> bool:
        """Verificar si tiene permisos para gestionar intervenciones"""
        return self.user_role in ["gerente", "odontologo"]
    
    # ==========================================
    # 🔧 MÉTODOS AUXILIARES
    # ==========================================
    
    @rx.event
    def update_paciente_form(self, field: str, value: str):
        """Actualizar campo del formulario de paciente"""
        self.paciente_form[field] = value
    
    @rx.event
    def update_consulta_form(self, field: str, value: str):
        """Actualizar campo del formulario de consulta"""
        self.consulta_form[field] = value
    
    @rx.event
    def update_servicio_form(self, field: str, value: str):
        """Actualizar campo del formulario de servicio"""
        self.servicio_form[field] = value
    
    @rx.event
    def update_personal_form(self, field: str, value: str):
        """Actualizar campo del formulario de personal"""
        self.personal_form[field] = value
    
    @rx.event
    def set_pacientes_search(self, search: str):
        """Actualizar búsqueda de pacientes"""
        self.pacientes_search = search
        
    @rx.event
    def set_pacientes_filter_activos(self, activos: str):
        """Establecer filtro por estado activo"""
        self.pacientes_filter_activos = activos
        
    @rx.event
    def set_consultas_search(self, search: str):
        """Actualizar búsqueda de consultas"""
        self.consultas_search = search
     
    @rx.event    
    def set_consultas_filter_estado(self, estado: str):
        """Establecer filtro por estado de consultas"""
        self.consultas_filter_estado = estado
    
    @rx.event
    def set_consultas_filter_odontologo(self, odontologo_id: str):
        """👩‍⚕️ Establecer filtro por odontólogo"""
        self.consultas_filter_odontologo = odontologo_id
        
    @rx.event
    def set_consultas_filter_tipo(self, tipo: str):
        """📋 Establecer filtro por tipo de consulta"""
        self.consultas_filter_tipo = tipo
        
    @rx.event
    def set_consultas_filter_fecha_inicio(self, fecha: str):
        """📅 Establecer fecha inicio para filtro"""
        self.consultas_filter_fecha_inicio = fecha
        
    @rx.event
    def set_consultas_filter_fecha_fin(self, fecha: str):
        """📅 Establecer fecha fin para filtro"""
        self.consultas_filter_fecha_fin = fecha
    
    @rx.event
    async def aplicar_filtros_consultas(self):
        """🔍 Aplicar todos los filtros de consultas"""
        await self.load_consultas_list()
    
    @rx.event
    async def limpiar_filtros_consultas(self):
        """🧹 Limpiar todos los filtros"""
        self.consultas_search = ""
        self.consultas_filter_estado = "Todos"
        self.consultas_filter_odontologo = "Todos"
        self.consultas_filter_tipo = "Todos"
        self.consultas_filter_fecha_inicio = ""
        self.consultas_filter_fecha_fin = ""
        await self.load_consultas_list()
    
    
    
    @rx.event
    def set_personal_search(self, search: str):
        """Actualizar búsqueda de personal"""
        self.personal_search = search

    @rx.event
    def set_personal_filter_tipo(self, tipo: str):
        """Establecer filtro por tipo de personal"""
        self.personal_filter_tipo = tipo

    @rx.event
    def set_personal_filter_estado(self, estado: str):
        """Establecer filtro por estado laboral"""
        self.personal_filter_estado = estado

    @rx.event
    def set_show_personal_modal(self, show: bool):
        """Controlar visibilidad del modal de personal"""
        self.show_personal_modal = show

    @rx.event
    def set_show_delete_personal_confirmation(self, show: bool):
        """Controlar visibilidad del modal de confirmación de eliminación"""
        self.show_delete_personal_confirmation = show

    @rx.event
    def set_show_reactivate_personal_confirmation(self, show: bool):
        """Controlar visibilidad del modal de confirmación de reactivación"""
        self.show_reactivate_personal_confirmation = show
        
        
        
    @rx.var
    def consultas_programadas(self) -> int:
        """Consultas en estado programada"""
        return len([c for c in self.consultas_list if c.get("estado") == "programada"])

    @rx.var
    def consultas_en_progreso(self) -> int:
        """Consultas en progreso"""
        return len([c for c in self.consultas_list if c.get("estado") == "en_progreso"])

    @rx.var
    def consultas_completadas(self) -> int:
        """Consultas completadas"""
        return len([c for c in self.consultas_list if c.get("estado") == "completada"])

    @rx.var
    def consultas_canceladas(self) -> int:
        """Consultas canceladas"""
        return len([c for c in self.consultas_list if c.get("estado") == "cancelada"])

# ==========================================
# 🔧 MÉTODO MEJORADO PARA CARGAR DATOS INICIALES
# ==========================================
    # ==========================================
    # 📱 MÉTODOS DE ESTADO DE LA UI
    # ==========================================
    
    def get_current_page_title(self) -> str:
        """Obtener título de la página actual"""
        if self.user_role == "gerente":
            return "Dashboard del Gerente"
        elif self.user_role == "administrador":
            return "Dashboard del Administrador"
        elif self.user_role == "odontologo":
            return "Dashboard del Odontólogo"
        else:
            return "Sistema Dental"
    
    def get_user_display_name(self) -> str:
        """Obtener nombre para mostrar del usuario"""
        if self.user_profile:
            nombre = self.user_profile.get("primer_nombre", "")
            apellido = self.user_profile.get("primer_apellido", "")
            return f"{nombre} {apellido}".strip() or self.user_email
        return self.user_email
    
    def get_total_pacientes(self) -> int:
        """Obtener total de pacientes"""
        return len(self.pacientes_list)
    
    def get_total_consultas(self) -> int:
        """Obtener total de consultas"""
        return len(self.consultas_list)
    
    def get_total_servicios(self) -> int:
        """Obtener total de servicios"""
        return len(self.servicios_list)
    
    def get_total_personal(self) -> int:
        """Obtener total de personal"""
        return len(self.personal_list)
    
    
    async def get_support_data_for_consultas(self):
        """Obtener datos de apoyo para consultas (odontólogos, servicios)"""
        try:
            return await consultas_service.get_support_data()
        except Exception as e:
            self.show_error(f"Error obteniendo datos de apoyo: {str(e)}")
            return []
    
    
    
     # ==========================================
    # 🎯 PROPIEDADES COMPUTADAS - FILTROS Y BÚSQUEDAS
    # ==========================================
    
    @rx.var  
    def pacientes_filtrados(self) -> List[Dict[str, Any]]:
        """🔍 Filtrar pacientes en tiempo real - MEJORADO"""
        if not self.pacientes_list:
            return []
            
        filtered = self.pacientes_list.copy()
        
        # Filtro por búsqueda (nombre, apellido, documento)
        if self.pacientes_search:
            search_lower = self.pacientes_search.lower()
            filtered = [
                p for p in filtered
                if (search_lower in (p.get("primer_nombre", "") + " " + p.get("primer_apellido", "")).lower()
                or search_lower in p.get("numero_documento", "").lower()
                or search_lower in p.get("email", "").lower()
                or search_lower in p.get("telefono_1", "").lower())
            ]
        
        # Filtro por estado
        if self.pacientes_filter_activos == "Activos":
            filtered = [p for p in filtered if p.get("activo", True)]
        elif self.pacientes_filter_activos == "Inactivos":
            filtered = [p for p in filtered if not p.get("activo", False)]
        # "Todos" no filtra nada
        
        return filtered
    
    @rx.var
    def consultas_filtradas(self) -> List[Dict[str, Any]]:
        """🔍 Filtrar consultas en tiempo real - MEJORADO"""
        if not self.consultas_list:
            return []
            
        filtered = self.consultas_list.copy()
        
        # Filtro por búsqueda (nombre paciente, motivo, número consulta)
        if self.consultas_search:
            search_lower = self.consultas_search.lower()
            filtered = [
                c for c in filtered
                if (search_lower in (c.get("paciente_nombre", "") or c.get("paciente_nombre_completo", "")).lower()
                    or search_lower in (c.get("motivo_consulta", "")).lower()
                    or search_lower in (c.get("numero_consulta", "")).lower()
                    or search_lower in (c.get("paciente_documento", "")).lower())
            ]
        
        # Filtro por estado (sin 'confirmada')
        if self.consultas_filter_estado != "Todos":
            estado_map = {
                "Programada": "programada",
                "En Progreso": "en_progreso", 
                "Completada": "completada",
                "Cancelada": "cancelada"
            }
            estado_filtro = estado_map.get(self.consultas_filter_estado, self.consultas_filter_estado.lower())
            filtered = [c for c in filtered if c.get("estado", "") == estado_filtro]
        
        # Filtro por odontólogo
        if self.consultas_filter_odontologo != "Todos":
            filtered = [c for c in filtered if c.get("odontologo_id", "") == self.consultas_filter_odontologo]
        
        # Filtro por tipo de consulta
        if self.consultas_filter_tipo != "Todos":
            filtered = [c for c in filtered if c.get("tipo_consulta", "") == self.consultas_filter_tipo]

        return filtered

    @rx.var
    def personal_filtrados(self) -> List[Dict[str, Any]]:
        """🔍 Filtrar personal en tiempo real"""
        if not self.personal_list:
            return []
            
        filtered = self.personal_list.copy()
        
        # Filtro por búsqueda
        if self.personal_search:
            search_lower = self.personal_search.lower()
            filtered = [
                p for p in filtered
                if (search_lower in (p.get("primer_nombre", "") + " " + p.get("primer_apellido", "")).lower()
                    or search_lower in p.get("numero_documento", "").lower()
                    or search_lower in p.get("email", "").lower()
                    or search_lower in (p.get("usuarios", {}).get("email", "") if isinstance(p.get("usuarios"), dict) else "").lower())
            ]
        
        # Filtro por tipo
        if self.personal_filter_tipo != "Todos":
            filtered = [p for p in filtered if p.get("tipo_personal", "") == self.personal_filter_tipo]
        
        # Filtro por estado
        if self.personal_filter_estado != "Todos":
            estado_map = {
                "Activo": "activo",
                "Inactivo": "inactivo", 
                "Vacaciones": "vacaciones"
            }
            estado_filtro = estado_map.get(self.personal_filter_estado, self.personal_filter_estado.lower())
            filtered = [p for p in filtered if p.get("estado_laboral", "") == estado_filtro]
        
        return filtered
    # ==========================================
    # 🚨 MANEJO DE MENSAJES - SIMPLIFICADO  
    # ==========================================
    
    # Estados de UI
    loading: bool = False
    error_message: str = ""
    success_message: str = ""
    info_message: str = ""
    
    def show_error(self, message: str):
        """❌ Mostrar mensaje de error - SIMPLE"""
        self.error_message = message
        self.success_message = ""
        self.info_message = ""
        # Auto-limpiar después de 5 segundos
        # TODO: Implementar timer
    
    def show_success(self, message: str):
        """✅ Mostrar mensaje de éxito - SIMPLE"""
        self.success_message = message
        self.error_message = ""
        self.info_message = ""
    
    def show_info(self, message: str):
        """ℹ️ Mostrar mensaje de información - SIMPLE"""
        self.info_message = message
        self.error_message = ""
        self.success_message = ""
    
    def clear_messages(self):
        """🧹 Limpiar todos los mensajes"""
        self.error_message = ""
        self.success_message = ""
        self.info_message = ""
        
    # ==========================================
    # GRÁFICOS Y ANALYTICS
    # ==========================================
    area_toggle: bool = True
    selected_tab: str = "Pacientes"
    
    def toggle_areachart(self):
        """Alterna entre gráfico de área y barras."""
        self.area_toggle = not self.area_toggle
    
    def set_selected_tab(self, selected_tab: Union[str, List[str]]):
        """Cambia la pestaña seleccionada."""
        if isinstance(selected_tab, list):
            self.selected_tab = selected_tab[0]
        else:
            self.selected_tab = selected_tab