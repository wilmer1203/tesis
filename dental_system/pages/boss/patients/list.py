"""
Página de gestión de pacientes para gerentes
Importa la funcionalidad completa de admin/patients pero accesible para gerentes
"""

# Importar la funcionalidad completa de pacientes
from dental_system.pages.admin.patients.list import patients_management

# Exportar directamente la funcionalidad
__all__ = ["patients_management"]
