# 🦷 COMPONENTES ODONTOLÓGICOS - MÓDULO ESPECIALIZADO
# dental_system/components/odontologia/__init__.py

"""
Componentes especializados para el módulo odontológico:
- Navegación por tabs profesional
- Odontograma interactivo
- Historia clínica visual
- Formularios de intervención especializados
"""


from .intervention_tabs_v2 import (
    intervention_tabs_integrated,
    tabs_navigation
)

__all__ = [
    "intervention_tabs_integrated",
    "tabs_navigation"
]