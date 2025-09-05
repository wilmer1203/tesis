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
    FacturaModel,
    ConceptoPagoModel,
    BalanceGeneralModel,
    CuentaPorCobrarModel,
    PagoFormModel,
    PagoParcialFormModel
)

from .odontologia_models import (
    OdontogramaModel,
    DienteModel,
    CondicionDienteModel,
    HistorialClinicoModel,
    PlanTratamientoModel,
    IntervencionFormModel
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
    "FacturaModel",
    "ConceptoPagoModel",
    "BalanceGeneralModel",
    "CuentaPorCobrarModel",
    
    # ✅ ODONTOLOGÍA ESPECIALIZADA
    "OdontogramaModel",
    "DienteModel",
    "CondicionDienteModel",
    "HistorialClinicoModel",
    "PlanTratamientoModel",
    
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
    "PagoParcialFormModel",
    "IntervencionFormModel",
    
    # ✅ AUTENTICACIÓN
    "AuthModel"
]

# ✅ BACKWARD COMPATIBILITY - Aliases para imports existentes
# Esto permite que el código existente siga funcionando
from .dashboard_models import DashboardStatsModel, AdminStatsModel
