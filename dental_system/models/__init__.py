"""
Models package - REFACTORIZADO POR FUNCIONALIDAD
Organización modular de modelos por área funcional del sistema
"""

# ✅ MODELOS POR FUNCIONALIDAD (Nueva estructura)
from .pacientes_models import (
    PacienteModel,
    PacientesStatsModel,
    ContactoEmergenciaModel,
    AlergiaModel
)

from .consultas_models import (
    ConsultaModel,
    TurnoModel,
    ConsultasStatsModel,
    MotivosConsultaModel,
    HorarioAtencionModel
)

from .personal_models import (
    UsuarioModel,
    RolModel,
    PersonalModel,
    PersonalStatsModel,
    HorarioTrabajoModel,
    EspecialidadModel,
    PermisoModel
)

from .servicios_models import (
    ServicioModel,
    CategoriaServicioModel,
    ServicioStatsModel,
    IntervencionModel,
    MaterialModel
)

from .pagos_models import (
    PagoModel,
    PagosStatsModel,
    FacturaModel,
    ConceptoPagoModel,
    BalanceGeneralModel,
    CuentaPorCobrarModel
)

from .odontologia_models import (
    OdontogramaModel,
    DienteModel,
    CondicionDienteModel,
    HistorialClinicoModel,
    PlanTratamientoModel
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

# ✅ MODELOS DE FORMULARIOS (Reemplazar Dict[str,str])
from .form_models import (
    PacienteFormModel,
    ConsultaFormModel,
    PersonalFormModel,
    ServicioFormModel,
    PagoFormModel,
    PagoParcialFormModel,
    IntervencionFormModel
)

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
