import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const PatientSummary = ({ patient, sessionActive, onStartSession, onEndSession }) => {
  if (!patient) return null;

  const formatDate = (dateString) => {
    return new Date(dateString)?.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const getUrgencyColor = (urgencia) => {
    switch (urgencia) {
      case 'alta': return 'text-error';
      case 'media': return 'text-warning';
      case 'baja': return 'text-success';
      default: return 'text-muted-foreground';
    }
  };

  return (
    <div className="h-full p-4 overflow-y-auto">
      {/* Session Control */}
      <div className="mb-6">
        {!sessionActive ? (
          <Button
            variant="default"
            size="sm"
            iconName="Play"
            iconPosition="left"
            iconSize={16}
            onClick={onStartSession}
            className="w-full"
          >
            Iniciar Sesión
          </Button>
        ) : (
          <Button
            variant="destructive"
            size="sm"
            iconName="Square"
            iconPosition="left"
            iconSize={16}
            onClick={onEndSession}
            className="w-full"
          >
            Terminar Sesión
          </Button>
        )}
      </div>

      {/* Patient Basic Info */}
      <div className="mb-6 p-4 bg-muted/20 rounded-lg">
        <div className="flex items-center space-x-3 mb-3">
          <Icon name="User" size={20} color="var(--color-primary)" />
          <div>
            <h3 className="font-semibold text-card-foreground">
              {patient?.nombre} {patient?.apellido}
            </h3>
            <p className="text-sm text-muted-foreground">
              {patient?.edad} años • {patient?.expediente}
            </p>
          </div>
        </div>
        
        <div className="space-y-2 text-sm">
          <div className="flex items-center space-x-2">
            <Icon name="Phone" size={14} color="var(--color-muted-foreground)" />
            <span className="text-muted-foreground">{patient?.telefono}</span>
          </div>
          <div className="flex items-center space-x-2">
            <Icon name="Mail" size={14} color="var(--color-muted-foreground)" />
            <span className="text-muted-foreground">{patient?.email}</span>
          </div>
        </div>
      </div>

      {/* Medical Alerts */}
      {patient?.alertas_medicas?.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center space-x-2 mb-3">
            <Icon name="AlertTriangle" size={16} color="var(--color-error)" />
            <h4 className="text-sm font-medium text-card-foreground">
              Alertas Médicas
            </h4>
          </div>
          <div className="space-y-2">
            {patient?.alertas_medicas?.map((alerta, index) => (
              <div 
                key={index}
                className="p-2 bg-error/10 border border-error/20 rounded-md"
              >
                <p className="text-xs text-error font-medium">
                  {alerta?.mensaje}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Allergies */}
      {patient?.alergias?.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center space-x-2 mb-3">
            <Icon name="Shield" size={16} color="var(--color-warning)" />
            <h4 className="text-sm font-medium text-card-foreground">
              Alergias
            </h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {patient?.alergias?.map((alergia, index) => (
              <span 
                key={index}
                className="px-2 py-1 bg-warning/10 text-warning text-xs rounded-md"
              >
                {alergia}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Medical Conditions */}
      {patient?.condiciones_medicas?.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center space-x-2 mb-3">
            <Icon name="Heart" size={16} color="var(--color-primary)" />
            <h4 className="text-sm font-medium text-card-foreground">
              Condiciones Médicas
            </h4>
          </div>
          <div className="space-y-1">
            {patient?.condiciones_medicas?.map((condicion, index) => (
              <div key={index} className="text-sm text-muted-foreground">
                • {condicion}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Current Medications */}
      {patient?.medicamentos_actuales?.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center space-x-2 mb-3">
            <Icon name="Pill" size={16} color="var(--color-secondary)" />
            <h4 className="text-sm font-medium text-card-foreground">
              Medicamentos Actuales
            </h4>
          </div>
          <div className="space-y-1">
            {patient?.medicamentos_actuales?.map((medicamento, index) => (
              <div key={index} className="text-sm text-muted-foreground">
                • {medicamento}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Treatment History */}
      <div className="mb-6">
        <div className="flex items-center space-x-2 mb-3">
          <Icon name="History" size={16} color="var(--color-accent)" />
          <h4 className="text-sm font-medium text-card-foreground">
            Historial de Tratamientos
          </h4>
        </div>
        <div className="space-y-2">
          {patient?.historial_tratamientos?.slice(0, 3)?.map((tratamiento, index) => (
            <div key={index} className="p-2 bg-muted/10 rounded-md">
              <div className="flex justify-between items-start mb-1">
                <span className="text-xs font-medium text-card-foreground">
                  {tratamiento?.procedimiento}
                </span>
                <span className="text-xs text-muted-foreground">
                  {formatDate(tratamiento?.fecha)}
                </span>
              </div>
              <p className="text-xs text-muted-foreground">
                {tratamiento?.dentista}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Next Appointment */}
      {patient?.proxima_cita && (
        <div className="mb-6">
          <div className="flex items-center space-x-2 mb-3">
            <Icon name="Calendar" size={16} color="var(--color-success)" />
            <h4 className="text-sm font-medium text-card-foreground">
              Próxima Cita
            </h4>
          </div>
          <div className="p-2 bg-success/10 border border-success/20 rounded-md">
            <div className="flex justify-between items-center mb-1">
              <span className="text-xs font-medium text-success">
                {formatDate(patient?.proxima_cita?.fecha)}
              </span>
              <span className="text-xs text-success">
                {patient?.proxima_cita?.hora}
              </span>
            </div>
            <p className="text-xs text-muted-foreground">
              {patient?.proxima_cita?.motivo}
            </p>
          </div>
        </div>
      )}

      {/* Session Notes (Auto-save area) */}
      <div className="mb-6">
        <div className="flex items-center space-x-2 mb-3">
          <Icon name="FileText" size={16} color="var(--color-primary)" />
          <h4 className="text-sm font-medium text-card-foreground">
            Notas de Sesión
          </h4>
          {sessionActive && (
            <span className="text-xs text-success">Auto-guardado</span>
          )}
        </div>
        <textarea
          className="w-full h-20 p-2 text-xs border border-border rounded-md bg-background resize-none"
          placeholder="Notas rápidas durante la sesión..."
          disabled={!sessionActive}
        />
      </div>
    </div>
  );
};

export default PatientSummary;