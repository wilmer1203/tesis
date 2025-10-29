"""
Models package - REFACTORIZADO POR FUNCIONALIDAD
Organización modular de modelos por área funcional del sistema
"""

# ✅ MODELOS POR FUNCIONALIDAD (Nueva estructura)
from .pacientes_models import (
    PacienteModel,
    PacientesStatsModel,
    ContactoEmergenciaModel,
    AlergiaModel,
    PacienteFormModel
)

from .consultas_models import (
    ConsultaModel,
    TurnoModel,
    ConsultasStatsModel,
    MotivosConsultaModel,
    HorarioAtencionModel,
    ConsultaConOrdenModel,
    ConsultaFormModel,
    ConsultaFinalizacionModel,
    ConsultaResumenModel
)

from .personal_models import (
    UsuarioModel,
    RolModel,
    PersonalModel,
    PersonalStatsModel,
    HorarioTrabajoModel,
    EspecialidadModel,
    PermisoModel,
    PersonalFormModel
)

from .servicios_models import (
    ServicioModel,
    CategoriaServicioModel,
    ServicioStatsModel,
    EstadisticaCategoriaModel,
    IntervencionModel,
    MaterialModel,
    ServicioFormModel
)

from .pagos_models import (
    PagoModel,
    PagosStatsModel,
    ConsultaPendientePago,
    BalanceGeneralModel,
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
    DienteModel,
    CondicionDienteModel,
    CondicionCatalogoModel,  # ✨ V3.0: Catálogo de condiciones
    ActualizacionOdontogramaResult,  # ✨ V3.0: Resultado batch
    HistorialClinicoModel,
    PlanTratamientoModel,
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
from .auth import AuthSession as AuthModel

__all__ = [
    # ✅ PACIENTES
    "PacienteModel",
    "PacientesStatsModel", 
    "ContactoEmergenciaModel",
    "AlergiaModel",
    
    # ✅ CONSULTAS
    "ConsultaModel",
    "TurnoModel",
    "ConsultasStatsModel",
    "MotivosConsultaModel", 
    "HorarioAtencionModel",
    "ConsultaConOrdenModel",
    
    # ✅ PERSONAL Y USUARIOS
    "UsuarioModel",
    "RolModel",
    "PersonalModel",
    "PersonalStatsModel",
    "HorarioTrabajoModel",
    "EspecialidadModel",
    "PermisoModel",
    
    # ✅ SERVICIOS E INTERVENCIONES  
    "ServicioModel",
    "CategoriaServicioModel",
    "ServicioStatsModel",
    "EstadisticaCategoriaModel",
    "IntervencionModel",
    "MaterialModel",
    
    # ✅ PAGOS Y FACTURACIÓN
    "PagoModel",
    "PagosStatsModel", 
    "ConsultaPendientePago",
    "ServicioFormateado",
    "BalanceGeneralModel",
    "CuentaPorCobrarModel",
    
    # ✅ ODONTOLOGÍA ESPECIALIZADA
    "OdontogramaModel",
    "DienteModel",
    "CondicionDienteModel",
    "CondicionCatalogoModel",  # ✨ V3.0
    "ActualizacionOdontogramaResult",  # ✨ V3.0
    "HistorialClinicoModel",
    "PlanTratamientoModel",
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
    "ConsultaFinalizacionModel",
    "ConsultaResumenModel",
    "PersonalFormModel",
    "ServicioFormModel",
    "PagoFormModel",
    "IntervencionFormModel",
    
    # ✅ AUTENTICACIÓN
    "AuthModel"
]

# ✅ BACKWARD COMPATIBILITY - Aliases para imports existentes
# Esto permite que el código existente siga funcionando
from .dashboard_models import DashboardStatsModel, AdminStatsModel
