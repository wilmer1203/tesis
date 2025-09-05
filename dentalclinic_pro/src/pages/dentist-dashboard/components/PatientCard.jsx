import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const PatientCard = ({ patient, onSelectPatient, isSelected = false }) => {
  const getUrgencyColor = (urgency) => {
    switch (urgency) {
      case 'alta':
        return 'text-error bg-error/10 border-error/20';
      case 'media':
        return 'text-warning bg-warning/10 border-warning/20';
      case 'baja':
        return 'text-success bg-success/10 border-success/20';
      default:
        return 'text-muted-foreground bg-muted/10 border-border';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'en_tratamiento':
        return 'text-primary bg-primary/10 border-primary/20';
      case 'completado':
        return 'text-success bg-success/10 border-success/20';
      case 'pendiente':
        return 'text-warning bg-warning/10 border-warning/20';
      case 'cancelado':
        return 'text-error bg-error/10 border-error/20';
      default:
        return 'text-muted-foreground bg-muted/10 border-border';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString)?.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatTime = (timeString) => {
    return new Date(`2000-01-01T${timeString}`)?.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div 
      className={`p-4 bg-card border border-border rounded-lg cursor-pointer transition-all duration-200 hover:shadow-custom-md ${
        isSelected ? 'ring-2 ring-primary border-primary/50 bg-primary/5' : ''
      }`}
      onClick={() => onSelectPatient(patient)}
    >
      {/* Patient Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-base font-semibold text-card-foreground mb-1">
            {patient?.nombre} {patient?.apellido}
          </h3>
          <p className="text-sm text-muted-foreground">
            ID: {patient?.id} • {patient?.edad} años
          </p>
        </div>
        
        {/* Alert Indicators */}
        <div className="flex items-center space-x-2">
          {patient?.condiciones_medicas && patient?.condiciones_medicas?.length > 0 && (
            <div className="w-2 h-2 bg-warning rounded-full" title="Condiciones médicas especiales" />
          )}
          {patient?.alergias && patient?.alergias?.length > 0 && (
            <div className="w-2 h-2 bg-error rounded-full" title="Alergias conocidas" />
          )}
        </div>
      </div>
      {/* Urgency and Status */}
      <div className="flex items-center space-x-2 mb-3">
        <span className={`px-2 py-1 text-xs font-medium rounded-md border ${getUrgencyColor(patient?.urgencia)}`}>
          {patient?.urgencia === 'alta' ? 'Urgente' : 
           patient?.urgencia === 'media' ? 'Media' : 'Baja'}
        </span>
        <span className={`px-2 py-1 text-xs font-medium rounded-md border ${getStatusColor(patient?.estado_tratamiento)}`}>
          {patient?.estado_tratamiento === 'en_tratamiento' ? 'En Tratamiento' :
           patient?.estado_tratamiento === 'completado' ? 'Completado' :
           patient?.estado_tratamiento === 'pendiente' ? 'Pendiente' : 'Cancelado'}
        </span>
      </div>
      {/* Next Appointment */}
      {patient?.proxima_cita && (
        <div className="flex items-center space-x-2 mb-3 p-2 bg-muted/30 rounded-md">
          <Icon name="Calendar" size={14} color="var(--color-primary)" />
          <div className="flex-1">
            <p className="text-xs font-medium text-card-foreground">
              Próxima Cita
            </p>
            <p className="text-xs text-muted-foreground">
              {formatDate(patient?.proxima_cita?.fecha)} - {formatTime(patient?.proxima_cita?.hora)}
            </p>
          </div>
        </div>
      )}
      {/* Treatment Progress */}
      <div className="mb-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-medium text-card-foreground">
            Progreso del Tratamiento
          </span>
          <span className="text-xs text-muted-foreground">
            {patient?.progreso_tratamiento}%
          </span>
        </div>
        <div className="w-full bg-muted rounded-full h-1.5">
          <div 
            className="bg-primary h-1.5 rounded-full transition-all duration-300"
            style={{ width: `${patient?.progreso_tratamiento}%` }}
          />
        </div>
      </div>
      {/* Last Visit */}
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <span>Última visita:</span>
        <span>{formatDate(patient?.ultima_visita)}</span>
      </div>
      {/* Quick Actions */}
      <div className="flex items-center space-x-2 mt-3 pt-3 border-t border-border">
        <Button
          variant="ghost"
          size="xs"
          iconName="FileText"
          iconPosition="left"
          iconSize={12}
          className="flex-1 text-xs"
          onClick={(e) => {
            e?.stopPropagation();
            // Handle view history
          }}
        >
          Historial
        </Button>
        <Button
          variant="ghost"
          size="xs"
          iconName="Edit"
          iconPosition="left"
          iconSize={12}
          className="flex-1 text-xs"
          onClick={(e) => {
            e?.stopPropagation();
            // Handle edit notes
          }}
        >
          Notas
        </Button>
      </div>
    </div>
  );
};

export default PatientCard;