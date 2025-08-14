"""
🔐 ESTADO DE AUTENTICACIÓN - SUBSTATE SEPARADO
===============================================

PROPÓSITO: Manejo centralizado y especializado de autenticación
- Login, logout, gestión de sesiones
- Control de permisos por rol
- Validación de tokens y contexto de usuario
- Integración con servicios de autenticación

USADO POR: AppState como coordinador principal
PATRÓN: Substate con get_estado_auth() en AppState
"""

import reflex as rx
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import logging

# Servicios relacionados con autenticación
from dental_system.supabase.auth import auth
from dental_system.services.cache_invalidation_hooks import CacheInvalidationHooks

logger = logging.getLogger(__name__)

class EstadoAuth(rx.State, mixin=True):
    """
    🔐 ESTADO ESPECIALIZADO EN AUTENTICACIÓN Y SEGURIDAD
    
    RESPONSABILIDADES:
    - Gestión completa de login/logout
    - Control de permisos granulares por rol
    - Validación de sesiones y tokens
    - Context de usuario para servicios
    - Rutas de navegación según roles
    """
    
    # ==========================================
    # 🔐 VARIABLES DE AUTENTICACIÓN BÁSICA
    # ==========================================
    
    # Estados principales de autenticación
    esta_autenticado: bool = False
    id_usuario: str = ""                    # ID en tabla usuarios
    id_personal: str = ""                   # ID en tabla personal (para odontólogos/personal)
    email_usuario: str = ""
    rol_usuario: str = ""                   # gerente, administrador, odontologo, asistente
    perfil_usuario: Dict[str, Any] = {}
    usuario_actual: Dict[str, Any] = {}
    permisos_usuario: List[str] = []
    
    # Control de sesión y seguridad
    token_sesion: str = ""
    ultima_actividad: str = ""
    error_login: str = ""
    esta_cargando_auth: bool = False
    
    # Estados de formularios multi-paso
    paso_formulario_paciente: int = 0
    errores_formulario_paciente: Dict[str, str] = {}
    puede_continuar_form_paciente: bool = True
    
    paso_formulario_personal: int = 0
    errores_formulario_personal: Dict[str, str] = {}
    puede_continuar_form_personal: bool = True
    
    # ==========================================
    # 🔐 MÉTODOS PRINCIPALES DE AUTENTICACIÓN
    # ==========================================
    
    @rx.event
    async def iniciar_sesion(self, datos_formulario: Dict[str, str]):
        """
        🔐 MÉTODO PRINCIPAL DE LOGIN CON NOMBRES EN ESPAÑOL
        
        QUÉ HACE:
        1. Valida email y contraseña
        2. Autentica con Supabase
        3. Obtiene rol y permisos del usuario
        4. Redirige al dashboard apropiado según el rol
        
        PARÁMETROS:
        - datos_formulario: {"email": "...", "password": "..."}
        
        IMPORTANTE: Este método maneja la redirección automática
        """
        print("🎯 LOGIN INICIADO - REDIRECCIÓN POR ROL")
        
        self.esta_cargando_auth = True
        self.error_login = ""
        
        try:
            # Extraer y validar credenciales
            email = datos_formulario.get("email", "").strip().lower()
            contraseña = datos_formulario.get("password", "").strip()
            
            if not email or not contraseña:
                self.error_login = "Email y contraseña son requeridos"
                return
            
            # Autenticar con Supabase
            sesion, info_usuario = auth.sign_in(email, contraseña)

            if sesion and info_usuario:
                # Actualizar estado de autenticación
                self.esta_autenticado = True
                self.id_usuario = info_usuario["id"]
                self.email_usuario = info_usuario["email"]
                self.rol_usuario = info_usuario["rol"]["nombre"]
                self.perfil_usuario = info_usuario
                self.usuario_actual = info_usuario
                
                # 🔄 OBTENER PERSONAL_ID si es odontólogo o personal usando el servicio
                self.id_personal = ""
                if self.rol_usuario in ["odontologo", "asistente"]:
                    try:
                        from dental_system.supabase.tablas.personal import personal_table
                        datos_personal = personal_table.get_by_usuario_id(self.id_usuario)
                        if datos_personal:
                            self.id_personal = datos_personal["id"]
                            print(f"🔄 Personal ID obtenido: usuario {self.id_usuario} → personal {self.id_personal}")
                        else:
                            print(f"⚠️ No se encontró personal para usuario {self.id_usuario}")
                    except Exception as e:
                        print(f"❌ Error obteniendo id_personal: {e}")
                
                print(f"✅ Usuario autenticado: {self.email_usuario} - Rol: {self.rol_usuario} - Personal ID: {self.id_personal}")
                
                # 🚀 INICIALIZAR DATOS POST-LOGIN
                await self.post_login_inicializacion()
                
                # Determinar ruta según rol y redirigir
                ruta_dashboard = self.obtener_ruta_dashboard()
                
                # # Invalidar cache al cambiar usuario
                # CacheInvalidationHooks.force_refresh_all_dashboard_cache()
                
                return rx.redirect(ruta_dashboard)
                
            else:
                self.error_login = "Credenciales inválidas"
                
        except Exception as e:
            self.error_login = f"Error de autenticación: {str(e)}"
            print(f"❌ Error en login: {e}")
            
        finally:
            self.esta_cargando_auth = False
    
    @rx.event
    async def cerrar_sesion(self):
        """
        🚪 CERRAR SESIÓN CON NOMBRES EN ESPAÑOL
        
        QUÉ HACE:
        1. Limpia todos los datos del usuario
        2. Resetea el estado de autenticación
        3. Invalida cache del dashboard
        4. Redirige al login
        """
        print("🚪 Cerrando sesión...")
        
        # Limpiar autenticación
        self.esta_autenticado = False
        self.id_usuario = ""
        self.id_personal = ""
        self.email_usuario = ""
        self.rol_usuario = ""
        self.perfil_usuario = {}
        self.usuario_actual = {}
        self.permisos_usuario = []
        
        # Limpiar estados de formulario
        self.paso_formulario_paciente = 0
        self.errores_formulario_paciente = {}
        self.puede_continuar_form_paciente = True
        
        self.paso_formulario_personal = 0
        self.errores_formulario_personal = {}
        self.puede_continuar_form_personal = True
        
        # Control de sesión
        self.token_sesion = ""
        self.ultima_actividad = ""
        self.error_login = ""
        
        # Invalidar cache completo al logout
        try:
            CacheInvalidationHooks.force_refresh_all_dashboard_cache()
            print("🗑️ Cache invalidado al cerrar sesión")
        except Exception as e:
            print(f"⚠️ Error invalidando cache al logout: {e}")
        
        print("✅ Sesión cerrada correctamente")
        return rx.redirect("/login")
    
    def obtener_ruta_dashboard(self) -> str:
        """
        🎯 DETERMINAR RUTA DEL DASHBOARD SEGÚN ROL - NOMBRES EN ESPAÑOL
        
        MAPEO DE ROLES:
        - gerente → /boss
        - administrador → /admin
        - odontologo → /dentist
        - asistente → /dentist
        """
        mapa_rutas = {
            "gerente": "/boss",
            "administrador": "/admin", 
            "odontologo": "/dentist",
            "asistente": "/dentist"
        }
        
        ruta = mapa_rutas.get(self.rol_usuario, "/")
        print(f"🎯 Rol '{self.rol_usuario}' → Ruta '{ruta}'")
        return ruta
    
    # ==========================================
    # 🔐 COMPUTED VARS PARA PERMISOS Y VALIDACIONES
    # ==========================================
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache validación de permisos
    def tiene_permiso_pacientes(self) -> bool:
        """👥 Verifica si puede gestionar pacientes"""
        return self.rol_usuario in ["gerente", "administrador"]
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache validación de permisos
    def tiene_permiso_consultas(self) -> bool:
        """📅 Verifica si puede gestionar consultas"""
        return self.rol_usuario in ["gerente", "administrador", "odontologo"]
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache validación de permisos
    def tiene_permiso_personal(self) -> bool:
        """👨‍⚕️ Verifica si puede gestionar personal"""
        return self.rol_usuario == "gerente"
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache validación de permisos
    def tiene_permiso_servicios(self) -> bool:
        """🏥 Verifica si puede gestionar servicios"""
        return self.rol_usuario == "gerente"
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache validación de permisos
    def tiene_permiso_pagos(self) -> bool:
        """💳 Verifica si puede gestionar pagos"""
        return self.rol_usuario in ["gerente", "administrador"]
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache validación de permisos
    def tiene_permiso_odontologia(self) -> bool:
        """🦷 Verifica si puede usar módulo odontológico"""
        return self.rol_usuario in ["gerente", "odontologo"]
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache display de usuario
    def nombre_usuario_display(self) -> str:
        """👤 Nombre para mostrar en UI"""
        if not self.perfil_usuario:
            return "Usuario"
        
        # Intentar obtener nombre desde perfil
        nombre = self.perfil_usuario.get("nombre", "")
        if nombre and nombre != "None":
            return nombre
        
        # Fallback al email
        return self.email_usuario.split("@")[0] if self.email_usuario else "Usuario"
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache rol display
    def rol_usuario_display(self) -> str:
        """👔 Rol formateado para mostrar"""
        roles_display = {
            "gerente": "Gerente",
            "administrador": "Administrador",
            "odontologo": "Odontólogo",
            "asistente": "Asistente"
        }
        return roles_display.get(self.rol_usuario, self.rol_usuario.title())
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache validación de sesión
    def sesion_valida(self) -> bool:
        """✅ Verifica si la sesión es válida"""
        return (
            self.esta_autenticado and 
            bool(self.id_usuario) and 
            bool(self.rol_usuario) and
            bool(self.email_usuario)
        )
    
    @rx.var(cache=True)  # ✅ OPTIMIZACIÓN: Cache tipo de dashboard
    def tipo_dashboard(self) -> str:
        """📊 Tipo de dashboard según rol"""
        if self.rol_usuario == "gerente":
            return "completo"
        elif self.rol_usuario == "administrador":
            return "administrativo"
        elif self.rol_usuario == "odontologo":
            return "clinico"
        else:
            return "basico"
    
    # ==========================================
    # 🔐 MÉTODOS DE UTILIDAD PARA SERVICIOS
    # ==========================================
    
    def obtener_contexto_usuario(self) -> Dict[str, Any]:
        """
        📋 CONTEXTO COMPLETO DEL USUARIO PARA SERVICIOS
        
        Returns:
            Dict con toda la información necesaria para servicios
        """
        return {
            "id_usuario": self.id_usuario,
            "id_personal": self.id_personal,
            "email": self.email_usuario,
            "rol": self.rol_usuario,
            "perfil_completo": self.perfil_usuario,
            "permisos": self.permisos_usuario,
            "sesion_valida": self.sesion_valida
        }
    
    def validar_permiso_para_operacion(self, modulo: str, operacion: str) -> bool:
        """
        🔒 VALIDAR PERMISO GRANULAR PARA OPERACIÓN
        
        Args:
            modulo: Módulo del sistema (pacientes, consultas, etc.)
            operacion: Tipo de operación (crear, leer, actualizar, eliminar)
            
        Returns:
            True si tiene permiso, False si no
        """
        # Mapeo de permisos por rol y módulo
        matriz_permisos = {
            "gerente": {
                "pacientes": ["crear", "leer", "actualizar", "eliminar"],
                "consultas": ["crear", "leer", "actualizar", "eliminar"],
                "personal": ["crear", "leer", "actualizar", "eliminar"],
                "servicios": ["crear", "leer", "actualizar", "eliminar"],
                "pagos": ["crear", "leer", "actualizar", "eliminar"],
                "odontologia": ["crear", "leer", "actualizar", "supervisar"]
            },
            "administrador": {
                "pacientes": ["crear", "leer", "actualizar", "eliminar"],
                "consultas": ["crear", "leer", "actualizar", "eliminar"],
                "personal": [],
                "servicios": ["leer"],
                "pagos": ["crear", "leer", "actualizar"],
                "odontologia": []
            },
            "odontologo": {
                "pacientes": ["leer"],  # Solo sus pacientes asignados
                "consultas": ["crear", "leer", "actualizar"],  # Solo sus consultas
                "personal": [],
                "servicios": ["leer"],
                "pagos": [],
                "odontologia": ["crear", "leer", "actualizar"]
            },
            "asistente": {
                "pacientes": [],
                "consultas": ["leer"],  # Solo lectura básica
                "personal": [],
                "servicios": [],
                "pagos": [],
                "odontologia": ["leer"]
            }
        }
        
        permisos_rol = matriz_permisos.get(self.rol_usuario, {})
        permisos_modulo = permisos_rol.get(modulo, [])
        
        return operacion in permisos_modulo
    
    # ==========================================
    # 🔐 MÉTODOS PARA FORMULARIOS MULTI-PASO
    # ==========================================
    
    @rx.event
    def avanzar_paso_formulario_paciente(self):
        """➡️ Avanzar paso en formulario de paciente"""
        if self.puede_continuar_form_paciente and self.paso_formulario_paciente < 3:
            self.paso_formulario_paciente += 1
            print(f"📝 Formulario paciente: paso {self.paso_formulario_paciente}")
    
    @rx.event
    def retroceder_paso_formulario_paciente(self):
        """⬅️ Retroceder paso en formulario de paciente"""
        if self.paso_formulario_paciente > 0:
            self.paso_formulario_paciente -= 1
            print(f"📝 Formulario paciente: paso {self.paso_formulario_paciente}")
    
    @rx.event
    def resetear_formulario_paciente(self):
        """🔄 Resetear formulario de paciente"""
        self.paso_formulario_paciente = 0
        self.errores_formulario_paciente = {}
        self.puede_continuar_form_paciente = True
        print("🔄 Formulario paciente reseteado")
    
    @rx.event
    def avanzar_paso_formulario_personal(self):
        """➡️ Avanzar paso en formulario de personal"""
        if self.puede_continuar_form_personal and self.paso_formulario_personal < 3:
            self.paso_formulario_personal += 1
            print(f"📝 Formulario personal: paso {self.paso_formulario_personal}")
    
    @rx.event
    def retroceder_paso_formulario_personal(self):
        """⬅️ Retroceder paso en formulario de personal"""
        if self.paso_formulario_personal > 0:
            self.paso_formulario_personal -= 1
            print(f"📝 Formulario personal: paso {self.paso_formulario_personal}")
    
    @rx.event 
    def resetear_formulario_personal(self):
        """🔄 Resetear formulario de personal"""
        self.paso_formulario_personal = 0
        self.errores_formulario_personal = {}
        self.puede_continuar_form_personal = True
        print("🔄 Formulario personal reseteado")
    
    # ==========================================
    # 🔐 VALIDACIONES DE SEGURIDAD
    # ==========================================
    
    def requiere_autenticacion(self) -> bool:
        """🔒 Verificar que el usuario esté autenticado"""
        if not self.sesion_valida:
            print("⚠️ Operación requiere autenticación")
            return False
        return True
    
    def requiere_rol(self, roles_permitidos: Union[str, List[str]]) -> bool:
        """🔒 Verificar que el usuario tenga uno de los roles permitidos"""
        if not self.requiere_autenticacion():
            return False
        
        if isinstance(roles_permitidos, str):
            roles_permitidos = [roles_permitidos]
        
        if self.rol_usuario not in roles_permitidos:
            print(f"⚠️ Operación requiere roles: {roles_permitidos}, usuario tiene: {self.rol_usuario}")
            return False
        
        return True
    
    def verificar_acceso_a_modulo(self, modulo: str) -> bool:
        """🔒 Verificar acceso general a un módulo"""
        accesos_modulo = {
            "dashboard": ["gerente", "administrador", "odontologo", "asistente"],
            "pacientes": ["gerente", "administrador"],
            "consultas": ["gerente", "administrador", "odontologo"],
            "personal": ["gerente"],
            "servicios": ["gerente"],
            "pagos": ["gerente", "administrador"],
            "odontologia": ["gerente", "odontologo"]
        }
        
        roles_permitidos = accesos_modulo.get(modulo, [])
        return self.requiere_rol(roles_permitidos)
    