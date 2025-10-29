# 🦷 COMPONENTES ODONTOLÓGICOS - MÓDULO ESPECIALIZADO
# dental_system/components/odontologia/__init__.py

"""
Componentes especializados para el módulo odontológico:
- Sistema V2.0: Componentes legacy funcionales
- Sistema V3.0 Profesional: Componentes médicos optimizados (ISO/WHO/ADA)
"""

# ==========================================
# 🌟 SISTEMA V4.0 - COMPONENTES PROFESIONALES REFACTORIZADOS
# ==========================================
from .simple_tooth import (
    simple_tooth,
    tooth_with_tooltip,
    get_tooth_color,
    TOOTH_NAMES
)

from .professional_odontogram_grid import (
    professional_odontogram_grid,
    odontogram_legend
)



from .odontogram_controls_bar import (
    odontogram_controls_bar
)

# ==========================================
# 📚 SISTEMA V5.0 - HISTORIAL CLÍNICO DEL PACIENTE (2025-10-16)
# ==========================================
from .history_service_card import (
    history_service_card
)

from .patient_history_section import (
    patient_history_section
)

# ==========================================
# 📦 EXPORTS
# ==========================================
__all__ = [
    # V4.0 Componentes Profesionales Refactorizados
    "simple_tooth",
    "tooth_with_tooltip",
    "get_tooth_color",
    "TOOTH_NAMES",
    "professional_odontogram_grid",
    "odontogram_legend",
    "odontogram_controls_bar",

    # V5.0 Historial Clínico del Paciente
    "history_service_card",
    "patient_history_section"
]