# 🦷 COMPONENTES ODONTOLÓGICOS - MÓDULO ESPECIALIZADO
# dental_system/components/odontologia/__init__.py

"""
Componentes especializados para el módulo odontológico:
- Sistema V2.0: Componentes legacy funcionales
- Sistema V3.0 Profesional: Componentes médicos optimizados (ISO/WHO/ADA)
"""

# ==========================================
# 🔄 SISTEMA V2.0 - COMPONENTES LEGACY
# ==========================================
from .intervention_tabs_v2 import (
    intervention_tabs_integrated,
    tabs_navigation
)

# ==========================================
# 🏥 SISTEMA V3.0 PROFESIONAL - COMPONENTES MÉDICOS
# ==========================================
from .professional_tooth import (
    professional_tooth,
    professional_tooth_with_tooltip,
    medical_conditions_legend
)

from .medical_condition_modal import (
    medical_condition_modal,
    medical_condition_button,
    medical_conditions_grid
)

from .medical_odontogram_grid import (
    medical_odontogram_grid,
    medical_odontogram_page,
    medical_status_bar,
    medical_controls_panel
)

from .panel_intervenciones_previas import (
    panel_intervenciones_previas,
    intervencion_previa_card
)

from .odontograma_status_bar_v3 import (
    odontograma_status_bar_v3,
    odontograma_cache_indicator,
    odontograma_changes_counter,
    odontograma_stats_panel,
    odontograma_action_buttons
)

from .timeline_odontograma import (
    timeline_odontograma_versiones,
    version_card,
    cambio_item,
    modal_historial_odontograma,
    boton_ver_historial
)

from .modal_validacion import (
    modal_validacion_odontograma,
    error_item,
    warning_item,
    boton_validar_manual
)

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

from .tooth_detail_sidebar import (
    tooth_detail_sidebar,
    empty_sidebar_placeholder,
    intervention_card,
    condition_badge
)

from .intervention_timeline import (
    intervention_timeline,
    intervention_timeline_card
)

from .odontogram_controls_bar import (
    odontogram_controls_bar
)

# ==========================================
# 📦 EXPORTS
# ==========================================
__all__ = [
    # V2.0 Legacy
    "intervention_tabs_integrated",
    "tabs_navigation",

    # V3.0 Professional Tooth Components
    "professional_tooth",
    "professional_tooth_with_tooltip",
    "medical_conditions_legend",

    # V3.0 Professional Modal
    "medical_condition_modal",
    "medical_condition_button",
    "medical_conditions_grid",

    # V3.0 Professional Grid
    "medical_odontogram_grid",
    "medical_odontogram_page",
    "medical_status_bar",
    "medical_controls_panel",

    # Panel Intervenciones Previas
    "panel_intervenciones_previas",
    "intervencion_previa_card",

    # V3.0 Status Bar & Controls
    "odontograma_status_bar_v3",
    "odontograma_cache_indicator",
    "odontograma_changes_counter",
    "odontograma_stats_panel",
    "odontograma_action_buttons",

    # V3.0 Timeline & History
    "timeline_odontograma_versiones",
    "version_card",
    "cambio_item",
    "modal_historial_odontograma",
    "boton_ver_historial",

    # V3.0 Validaciones
    "modal_validacion_odontograma",
    "error_item",
    "warning_item",
    "boton_validar_manual",

    # V4.0 Componentes Profesionales Refactorizados
    "simple_tooth",
    "tooth_with_tooltip",
    "get_tooth_color",
    "TOOTH_NAMES",
    "professional_odontogram_grid",
    "odontogram_legend",
    "tooth_detail_sidebar",
    "empty_sidebar_placeholder",
    "intervention_card",
    "condition_badge",
    "intervention_timeline",
    "intervention_timeline_card",
    "odontogram_controls_bar"
]