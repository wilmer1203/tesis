"""
🏥 ESTADOS DE LA APLICACIÓN - SISTEMA ODONTOLÓGICO  
==================================================

ARQUITECTURA RECOMENDADA REFLEX.dev: AppState Monolítico Organizado
- AppState único bien estructurado por módulos
- Computed vars optimizados con @rx.var(cache=True)
- Servicios externos especializados
- Type safety con modelos Pydantic

VERSIÓN: 2.5 - AppState Optimizado (RECOMENDADO)
"""

# ==========================================
# 🏥 APPSTATE PRINCIPAL (RECOMENDADO)
# ==========================================

# ✅ SOLUCIÓN CORRECTA: AppState monolítico bien organizado
from .app_state import AppState
from .estado_auth import EstadoAuth
from .estado_odontograma_interactivo import EstadoOdontogramaInteractivo
# ==========================================
# 📤 EXPORTS PRINCIPALES  
# ==========================================

__all__ = [
    "AppState",
    "EstadoAuth",
    "EstadoOdontogramaInteractivo"
]

# ==========================================
# 📝 NOTAS DE ARQUITECTURA
# ==========================================

# ✅ BEST PRACTICES REFLEX.dev:
# 1. AppState monolítico organizado por módulos
# 2. @rx.var(cache=True) para computed vars  
# 3. Servicios externos para lógica de BD
# 4. Modelos tipados para type safety
# 5. Helper methods para operaciones complejas

# ❌ PATTERNS NO RECOMENDADOS:
# 1. Substates separados (MRO conflicts)
# 2. Herencia múltiple (complex resolution)
# 3. get_state() en computed vars (async issues)
# 4. Over-engineering para casos simples
