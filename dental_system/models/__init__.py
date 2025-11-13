"""
Models package - REFACTORIZADO POR FUNCIONALIDAD
Organización modular de modelos por área funcional del sistema
"""

# ✅ MODELOS POR FUNCIONALIDAD (Nueva estructura)
from .pacientes_models import (
    PacienteModel,
    PacientesStatsModel,
    PacienteFormModel,
    # Modelos para historial completo
    ServicioHistorial,
    IntervencionHistorial,
    ConsultaHistorial,
    HistorialCompletoPaciente
)

from .consultas_models import (
    ConsultaModel,
    TurnoModel,
    ConsultaFormModel
)

from .personal_models import (
    UsuarioModel,
    RolModel,
    PersonalModel,
    PersonalStatsModel,
    PersonalFormModel
)

from .servicios_models import (
    ServicioModel,
    ServicioStatsModel,
    EstadisticaCategoriaModel,
    ServicioFormModel
)

from .pagos_models import (
    PagoModel,
    PagosStatsModel,
    ConsultaPendientePago,
    CuentaPorCobrarModel,
    PagoFormModel,
    ServicioFormateado
    
)

from .ui_models import (
    ToastModel,
    NotificationModel
)

from .odontologia_models import (
    OdontogramaModel,
    ActualizacionOdontogramaResult,
    IntervencionModel,
    IntervencionFormModel,
    HistorialMedicoModel,
    HistorialServicioModel
)

from .dashboard_models import (
    DashboardStatsModel,
    AdminStatsModel,
    GerenteStatsModel,
    OdontologoStatsModel,
    AsistenteStatsModel,
    MetricaTemporalModel,
    ComparativaModel,
    AlertaModel,
    ReporteModel,
    KPIModel
)

# ✅ FORMULARIOS AHORA INTEGRADOS EN SUS MÓDULOS RESPECTIVOS

# ✅ MODELOS DE AUTENTICACIÓN (Mantener separado)
# from .auth import AuthSession as AuthModel

__all__ = [
    # ✅ PACIENTES
    "PacienteModel",
    "PacientesStatsModel",
    "ServicioHistorial",
    "IntervencionHistorial",
    "ConsultaHistorial",
    "HistorialCompletoPaciente",
    
    # ✅ CONSULTAS
    "ConsultaModel",
    "TurnoModel",
    
    # ✅ PERSONAL Y USUARIOS
    "UsuarioModel",
    "RolModel",
    "PersonalModel",
    "PersonalStatsModel",
    
    # ✅ SERVICIOS
    "ServicioModel",
    "ServicioStatsModel",
    "EstadisticaCategoriaModel",

    # ✅ PAGOS Y FACTURACIÓN
    "PagoModel",
    "PagosStatsModel", 
    "ConsultaPendientePago",
    "ServicioFormateado",
    "CuentaPorCobrarModel",
    
    # ✅ ODONTOLOGÍA ESPECIALIZADA
    "OdontogramaModel",
    "ActualizacionOdontogramaResult",  # ✨ V3.0
    "IntervencionModel",
    "HistorialMedicoModel",
    "HistorialServicioModel",
    
    # ✅ DASHBOARD Y ESTADÍSTICAS
    "DashboardStatsModel",
    "AdminStatsModel",
    "GerenteStatsModel", 
    "OdontologoStatsModel",
    "AsistenteStatsModel",
    "MetricaTemporalModel",
    "ComparativaModel",
    "AlertaModel",
    "ReporteModel",
    "KPIModel",
    
    # ✅ MODELOS DE FORMULARIOS
    "PacienteFormModel",
    "ConsultaFormModel", 
    "PersonalFormModel",
    "ServicioFormModel",
    "PagoFormModel",
    "IntervencionFormModel",
    
    # ✅ AUTENTICACIÓN
    # "AuthModel"
]

# ✅ BACKWARD COMPATIBILITY - Aliases para imports existentes
# Esto permite que el código existente siga funcionando
from .dashboard_models import DashboardStatsModel, AdminStatsModel
