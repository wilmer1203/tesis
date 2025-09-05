import React, { useState } from 'react';
import { useDrag } from 'react-dnd';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const PatientCard = ({ 
  patient, 
  position, 
  dentistId, 
  onTransfer, 
  onPriority, 
  onStartConsultation,
  onReorder 
}) => {
  const [showActions, setShowActions] = useState(false);

  const [{ isDragging }, drag] = useDrag({
    type: 'patient',
    item: { patientId: patient?.id, currentDentistId: dentistId },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  const getPriorityConfig = (priority) => {
    switch (priority) {
      case 'urgent':
        return {
          color: 'text-error',
          bg: 'bg-error/10',
          icon: 'AlertTriangle',
          label: 'Urgente'
        };
      case 'high':
        return {
          color: 'text-warning',
          bg: 'bg-warning/10',
          icon: 'ArrowUp',
          label: 'Alta'
        };
      case 'normal':
        return {
          color: 'text-muted-foreground',
          bg: 'bg-muted',
          icon: 'Minus',
          label: 'Normal'
        };
      default:
        return {
          color: 'text-muted-foreground',
          bg: 'bg-muted',
          icon: 'Minus',
          label: 'Normal'
        };
    }
  };

  const priorityConfig = getPriorityConfig(patient?.priority);

  const formatWaitTime = (minutes) => {
    if (minutes < 60) {
      return `${minutes}m`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const getWaitTimeColor = (minutes) => {
    if (minutes > 60) return 'text-error';
    if (minutes > 30) return 'text-warning';
    return 'text-muted-foreground';
  };

  return (
    <div
      ref={drag}
      className={`bg-background border border-border rounded-md p-3 transition-all duration-200 cursor-move relative group ${
        isDragging ? 'opacity-50 scale-95' : 'hover:shadow-soft'
      }`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      {/* Patient Info */}
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-sm font-medium text-foreground">{patient?.name}</span>
            {patient?.priority !== 'normal' && (
              <div className={`flex items-center space-x-1 px-2 py-0.5 rounded-full ${priorityConfig?.bg}`}>
                <Icon name={priorityConfig?.icon} size={12} className={priorityConfig?.color} />
                <span className={`text-xs font-medium ${priorityConfig?.color}`}>
                  {priorityConfig?.label}
                </span>
              </div>
            )}
          </div>
          
          <div className="text-xs text-muted-foreground space-y-1">
            <div>ID: {patient?.id}</div>
            <div>Llegada: {patient?.arrivalTime}</div>
            <div className={getWaitTimeColor(patient?.waitTime)}>
              Esperando: {formatWaitTime(patient?.waitTime)}
            </div>
          </div>
        </div>

        <div className="text-right">
          <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center mb-1">
            <span className="text-sm font-bold text-primary">{position}</span>
          </div>
          <div className="text-xs text-muted-foreground">
            ~{patient?.estimatedTime}m
          </div>
        </div>
      </div>
      {/* Patient Details */}
      <div className="flex items-center space-x-4 text-xs text-muted-foreground mb-3">
        <div className="flex items-center space-x-1">
          <Icon name="Calendar" size={12} />
          <span>{patient?.age} años</span>
        </div>
        <div className="flex items-center space-x-1">
          <Icon name="Phone" size={12} />
          <span>{patient?.phone}</span>
        </div>
        {patient?.hasInsurance && (
          <div className="flex items-center space-x-1">
            <Icon name="Shield" size={12} />
            <span>Seguro</span>
          </div>
        )}
      </div>
      {/* Service Info */}
      <div className="bg-muted rounded-md p-2 mb-3">
        <div className="text-xs font-medium text-foreground mb-1">{patient?.service}</div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground">Estimado:</span>
          <span className="font-medium text-foreground">{patient?.estimatedCost}</span>
        </div>
      </div>
      {/* Action Buttons */}
      <div className={`flex space-x-2 transition-all duration-200 ${
        showActions ? 'opacity-100 max-h-10' : 'opacity-0 max-h-0 overflow-hidden'
      }`}>
        <Button
          variant="outline"
          size="sm"
          iconName="ArrowRight"
          onClick={() => onStartConsultation(patient?.id, dentistId)}
          className="flex-1 text-xs"
        >
          Iniciar
        </Button>
        
        <Button
          variant="ghost"
          size="sm"
          iconName="ArrowUpDown"
          onClick={() => onPriority(patient?.id, dentistId)}
          className="px-2"
        />
        
        <Button
          variant="ghost"
          size="sm"
          iconName="ArrowRightLeft"
          onClick={() => onTransfer(patient?.id, dentistId)}
          className="px-2"
        />
      </div>
      {/* Drag Handle */}
      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <Icon name="GripVertical" size={14} className="text-muted-foreground" />
      </div>
    </div>
  );
};

export default PatientCard;