import React, { useState } from 'react';
import { useDrop } from 'react-dnd';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import PatientCard from './PatientCard';

const QueueColumn = ({ 
  dentist, 
  patients, 
  onPatientTransfer, 
  onPatientPriority, 
  onStartConsultation,
  onToggleAvailability,
  onPatientReorder 
}) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const [{ isOver }, drop] = useDrop({
    accept: 'patient',
    drop: (item) => {
      if (item?.currentDentistId !== dentist?.id) {
        onPatientTransfer(item?.patientId, item?.currentDentistId, dentist?.id);
      }
    },
    collect: (monitor) => ({
      isOver: monitor?.isOver(),
    }),
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'available':
        return 'text-success bg-success/10';
      case 'busy':
        return 'text-warning bg-warning/10';
      case 'break':
        return 'text-muted-foreground bg-muted';
      case 'unavailable':
        return 'text-error bg-error/10';
      default:
        return 'text-muted-foreground bg-muted';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'available':
        return 'CheckCircle';
      case 'busy':
        return 'Clock';
      case 'break':
        return 'Coffee';
      case 'unavailable':
        return 'XCircle';
      default:
        return 'User';
    }
  };

  const statusConfig = {
    color: getStatusColor(dentist?.status),
    icon: getStatusIcon(dentist?.status)
  };

  return (
    <div
      ref={drop}
      className={`bg-card border border-border rounded-lg shadow-soft transition-all duration-200 ${
        isOver ? 'border-primary bg-primary/5' : ''
      }`}
      style={{ position: 'relative' }}
    >
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
              <Icon name="User" size={20} className="text-primary" />
            </div>
            <div>
              <h3 className="font-semibold text-foreground">{dentist?.name}</h3>
              <p className="text-sm text-muted-foreground">{dentist?.specialty}</p>
            </div>
          </div>
          
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 hover:bg-muted rounded-md transition-smooth lg:hidden"
          >
            <Icon name={isExpanded ? "ChevronUp" : "ChevronDown"} size={16} className="text-muted-foreground" />
          </button>
        </div>

        {/* Status and Controls */}
        <div className="flex items-center justify-between">
          <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${statusConfig?.color}`}>
            <Icon name={statusConfig?.icon} size={14} />
            <span className="text-sm font-medium capitalize">{dentist?.status}</span>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className="text-sm text-muted-foreground">
              {patients?.length} pacientes
            </span>
            <Button
              variant="ghost"
              size="sm"
              iconName="Settings"
              onClick={() => onToggleAvailability(dentist?.id)}
              className="p-2"
            />
          </div>
        </div>

        {/* Queue Stats */}
        <div className="grid grid-cols-3 gap-2 mt-3 text-center">
          <div className="bg-muted rounded-md p-2">
            <div className="text-lg font-semibold text-foreground">{patients?.length}</div>
            <div className="text-xs text-muted-foreground">Total</div>
          </div>
          <div className="bg-muted rounded-md p-2">
            <div className="text-lg font-semibold text-foreground">
              {patients?.filter(p => p?.priority === 'urgent')?.length}
            </div>
            <div className="text-xs text-muted-foreground">Urgentes</div>
          </div>
          <div className="bg-muted rounded-md p-2">
            <div className="text-lg font-semibold text-foreground">
              {dentist?.estimatedWaitTime}m
            </div>
            <div className="text-xs text-muted-foreground">Espera</div>
          </div>
        </div>
      </div>
      {/* Patient List */}
      <div className={`transition-all duration-200 ${isExpanded ? 'block' : 'hidden lg:block'}`}>
        <div className="p-4 space-y-3 max-h-96 overflow-y-auto">
          {patients?.length === 0 ? (
            <div className="text-center py-8">
              <Icon name="Users" size={48} className="text-muted-foreground mx-auto mb-3" />
              <p className="text-muted-foreground">No hay pacientes en cola</p>
            </div>
          ) : (
            patients?.map((patient, index) => (
              <PatientCard
                key={patient?.id}
                patient={patient}
                position={index + 1}
                dentistId={dentist?.id}
                onTransfer={onPatientTransfer}
                onPriority={onPatientPriority}
                onStartConsultation={onStartConsultation}
                onReorder={onPatientReorder}
              />
            ))
          )}
        </div>
      </div>
      {/* Drop Zone Indicator */}
      {isOver && (
        <div className="absolute inset-0 bg-primary/10 border-2 border-dashed border-primary rounded-lg flex items-center justify-center">
          <div className="text-center">
            <Icon name="UserPlus" size={32} className="text-primary mx-auto mb-2" />
            <p className="text-primary font-medium">Transferir paciente aquí</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default QueueColumn;