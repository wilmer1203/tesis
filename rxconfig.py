import reflex as rx

config = rx.Config(
    app_name="dental_system",
    tailwind=None,  # No estamos usando Tailwind
    db_url="",
    env=rx.Env.DEV,
)

# """
# Configuración optimizada de Reflex para Sistema Dental Odontomara
# Incluye configuraciones de producción, desarrollo y optimizaciones
# """

# import reflex as rx
# import os
# from pathlib import Path

# # ==========================================
# # CONFIGURACIÓN DE ENTORNO
# # ==========================================

# # Detectar entorno automáticamente
# def get_environment() -> rx.Env:
#     """Detectar entorno basado en variables de entorno"""
#     env_var = os.getenv("ENVIRONMENT", "dev").lower()
#     if env_var in ["prod", "production"]:
#         return rx.Env.PROD
#     elif env_var in ["staging", "stage"]:
#         return rx.Env.PROD  # Usar PROD para staging
#     else:
#         return rx.Env.DEV

# # ==========================================
# # CONFIGURACIONES POR ENTORNO
# # ==========================================

# ENVIRONMENT = get_environment()

# # Configuración base
# BASE_CONFIG = {
#     "app_name": "dental_system",
#     "env": ENVIRONMENT,
    
#     # Configuración de base de datos (no usamos por Supabase)
#     "db_url": "",
    
#     # Optimizaciones de Reflex
#     "compile": True,  # Compilar para mejor rendimiento
#     "hot_reload": ENVIRONMENT == rx.Env.DEV,  # Solo en desarrollo
    
#     # Configuración de frontend
#     "frontend_packages": [
#         # Paquetes adicionales si son necesarios
#     ],
    
#     # Configuración de backend
#     "backend_port": int(os.getenv("BACKEND_PORT", "8000")),
#     "frontend_port": int(os.getenv("FRONTEND_PORT", "3000")),
    
#     # Timeouts y límites
#     "timeout": 300,  # 5 minutos
#     "api_url": f"http://localhost:{int(os.getenv('BACKEND_PORT', '8000'))}",
# }

# # Configuración específica para desarrollo
# DEV_CONFIG = {
#     **BASE_CONFIG,
#     "debug": True,
#     "hot_reload": True,
#     "compile": False,  # No compilar en dev para velocidad
# }

# # Configuración específica para producción
# PROD_CONFIG = {
#     **BASE_CONFIG,
#     "debug": False,
#     "hot_reload": False,
#     "compile": True,
#     "backend_port": int(os.getenv("PORT", "8000")),  # Para Heroku/Railway
#     "api_url": os.getenv("API_URL", f"http://localhost:{int(os.getenv('PORT', '8000'))}"),
# }

# # ==========================================
# # CONFIGURACIÓN FINAL
# # ==========================================

# # Seleccionar configuración según entorno
# if ENVIRONMENT == rx.Env.DEV:
#     final_config = DEV_CONFIG
#     print("[CONFIG] 🔧 Modo DESARROLLO activado")
#     print(f"[CONFIG] 🌐 Frontend: http://localhost:{final_config['frontend_port']}")
#     print(f"[CONFIG] ⚙️ Backend: http://localhost:{final_config['backend_port']}")
# else:
#     final_config = PROD_CONFIG
#     print("[CONFIG] 🚀 Modo PRODUCCIÓN activado")
#     print(f"[CONFIG] 🌐 API URL: {final_config['api_url']}")

# # Crear configuración de Reflex
# config = rx.Config(**final_config)

# # ==========================================
# # VALIDACIONES DE CONFIGURACIÓN
# # ==========================================

# def validate_config():
#     """Validar que la configuración esté correcta"""
#     required_env_vars = [
#         "SUPABASE_URL",
#         "SUPABASE_ANON_KEY",
#         "SUPABASE_SERVICE_ROLE_KEY"
#     ]
    
#     missing_vars = []
#     for var in required_env_vars:
#         if not os.getenv(var):
#             missing_vars.append(var)
    
#     if missing_vars:
#         print(f"[CONFIG] ❌ Variables de entorno faltantes: {missing_vars}")
#         return False
#     else:
#         print("[CONFIG] ✅ Todas las variables de entorno están configuradas")
#         return True

# # ==========================================
# # CONFIGURACIONES ADICIONALES
# # ==========================================

# # Configuración de logging
# LOGGING_CONFIG = {
#     "level": "DEBUG" if ENVIRONMENT == rx.Env.DEV else "INFO",
#     "format": "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
#     "file_enabled": ENVIRONMENT == rx.Env.PROD
# }

# # Configuración de la aplicación dental específica
# DENTAL_APP_CONFIG = {
#     "app_title": "Sistema Dental Odontomara",
#     "app_description": "Sistema integral para gestión odontológica",
#     "app_version": "1.0.0",
#     "clinic_name": "Clínica Dental Odontomara",
#     "clinic_location": "Puerto La Cruz, Anzoátegui",
#     "max_upload_size": 10 * 1024 * 1024,  # 10MB
#     "allowed_file_types": [".jpg", ".jpeg", ".png", ".pdf"],
#     "session_timeout": 24 * 60 * 60,  # 24 horas en segundos
# }

# # ==========================================
# # FUNCIÓN DE INICIALIZACIÓN
# # ==========================================

# def initialize_app():
#     """Inicializar la aplicación con validaciones"""
#     print(f"[CONFIG] 🦷 Inicializando {DENTAL_APP_CONFIG['app_title']} v{DENTAL_APP_CONFIG['app_version']}")
#     print(f"[CONFIG] 🏥 Clínica: {DENTAL_APP_CONFIG['clinic_name']}")
#     print(f"[CONFIG] 📍 Ubicación: {DENTAL_APP_CONFIG['clinic_location']}")
    
#     # Validar configuración
#     if not validate_config():
#         print("[CONFIG] ⚠️ Configuración incompleta, la aplicación puede no funcionar correctamente")
    
#     return config

# # Ejecutar inicialización
# if __name__ == "__main__":
#     initialize_app()

# # ==========================================
# # EXPORTAR CONFIGURACIONES
# # ==========================================

# __all__ = [
#     "config",
#     "ENVIRONMENT", 
#     "DENTAL_APP_CONFIG",
#     "LOGGING_CONFIG",
#     "initialize_app",
#     "validate_config"
# ]