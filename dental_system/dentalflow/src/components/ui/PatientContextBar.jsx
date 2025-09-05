import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Icon from '../AppIcon';
import Button from './Button';

const PatientContextBar = ({ 
  patient = null, 
  onDismiss = null, 
  showQueueStatus = true,
  className = '' 
}) => {
  const navigate = useNavigate();
  const [isExpanded, setIsExpanded] = useState(false);

  // Mock patient data when none provided
  const currentPatient = patient || {
    id: 'P-2024-0892',
    name: 'Ana María Rodríguez',
    age: 34,
    phone: '+58 412-555-0123',
    queuePosition: 3,
    estimatedTime: 15,
    status: 'waiting', // waiting, in-progress, completed
    lastVisit: '2024-08-15',
    allergies: ['Penicilina'],
    insurance: 'Seguros Caracas'
  };

  const getStatusConfig = (status) => {
    switch (status) {
      case 'waiting':
        return {
          color: 'text-warning',
          bg: 'bg-warning/10',
          icon: 'Clock',
          label: 'En Espera'
        };
      case 'in-progress':
        return {
          color: 'text-success',
          bg: 'bg-success/10',
          icon: 'Activity',
          label: 'En Consulta'
        };
      case 'completed':
        return {
          color: 'text-muted-foreground',
          bg: 'bg-muted',
          icon: 'CheckCircle',
          label: 'Completado'
        };
      default:
        return {
          color: 'text-muted-foreground',
          bg: 'bg-muted',
          icon: 'User',
          label: 'Desconocido'
        };
    }
  };

  const statusConfig = getStatusConfig(currentPatient?.status);

  const handleViewHistory = () => {
    navigate(`/patient-consultation?patient=${currentPatient?.id}`);
  };

  const handleViewOdontogram = () => {
    navigate(`/digital-odontogram-viewer?patient=${currentPatient?.id}`);
  };

  const handleDismiss = () => {
    if (onDismiss) {
      onDismiss();
    }
  };

  if (!patient && !currentPatient) return null;

  return (
    <div className={`sticky top-16 z-40 bg-card border-b border-border shadow-soft ${className}`}>
      <div className="px-6 py-3">
        {/* Mobile View */}
        <div className="sm:hidden">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                <Icon name="User" size={20} className="text-primary" />
              </div>
              <div>
                <div className="font-medium text-foreground text-sm">{currentPatient?.name}</div>
                <div className="text-xs text-muted-foreground">{currentPatient?.id}</div>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="p-2 hover:bg-muted rounded-md transition-smooth"
              >
                <Icon name={isExpanded ? "ChevronUp" : "ChevronDown"} size={16} className="text-muted-foreground" />
              </button>
              
              {onDismiss && (
                <button
                  onClick={handleDismiss}
                  className="p-2 hover:bg-muted rounded-md transition-smooth"
                >
                  <Icon name="X" size={16} className="text-muted-foreground" />
                </button>
              )}
            </div>
          </div>

          {isExpanded && (
            <div className="mt-3 pt-3 border-t border-border space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="text-xs">
                  <span className="text-muted-foreground">Edad:</span>
                  <span className="ml-1 text-foreground">{currentPatient?.age} años</span>
                </div>
                <div className="text-xs">
                  <span className="text-muted-foreground">Teléfono:</span>
                  <span className="ml-1 text-foreground">{currentPatient?.phone}</span>
                </div>
              </div>

              {showQueueStatus && (
                <div className={`flex items-center space-x-2 px-3 py-2 rounded-md ${statusConfig?.bg}`}>
                  <Icon name={statusConfig?.icon} size={16} className={statusConfig?.color} />
                  <span className={`text-sm font-medium ${statusConfig?.color}`}>{statusConfig?.label}</span>
                  {currentPatient?.status === 'waiting' && (
                    <span className="text-xs text-muted-foreground ml-auto">
                      Posición: {currentPatient?.queuePosition} • {currentPatient?.estimatedTime} min
                    </span>
                  )}
                </div>
              )}

              <div className="flex space-x-2">
                <Button variant="outline" size="sm" onClick={handleViewHistory} className="flex-1">
                  <Icon name="FileText" size={14} className="mr-1" />
                  Historial
                </Button>
                <Button variant="outline" size="sm" onClick={handleViewOdontogram} className="flex-1">
                  <Icon name="Tooth" size={14} className="mr-1" />
                  Odontograma
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Desktop View */}
        <div className="hidden sm:flex items-center justify-between">
          <div className="flex items-center space-x-6">
            {/* Patient Info */}
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                <Icon name="User" size={24} className="text-primary" />
              </div>
              <div>
                <div className="font-semibold text-foreground">{currentPatient?.name}</div>
                <div className="text-sm text-muted-foreground">
                  {currentPatient?.id} • {currentPatient?.age} años • {currentPatient?.phone}
                </div>
              </div>
            </div>

            {/* Status */}
            {showQueueStatus && (
              <div className={`flex items-center space-x-2 px-4 py-2 rounded-md ${statusConfig?.bg}`}>
                <Icon name={statusConfig?.icon} size={16} className={statusConfig?.color} />
                <span className={`text-sm font-medium ${statusConfig?.color}`}>{statusConfig?.label}</span>
                {currentPatient?.status === 'waiting' && (
                  <span className="text-sm text-muted-foreground ml-2">
                    Posición: {currentPatient?.queuePosition} • {currentPatient?.estimatedTime} min
                  </span>
                )}
              </div>
            )}

            {/* Additional Info */}
            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
              {currentPatient?.allergies?.length > 0 && (
                <div className="flex items-center space-x-1">
                  <Icon name="AlertTriangle" size={14} className="text-warning" />
                  <span>Alergias: {currentPatient?.allergies?.join(', ')}</span>
                </div>
              )}
              <div className="flex items-center space-x-1">
                <Icon name="Shield" size={14} />
                <span>{currentPatient?.insurance}</span>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-3">
            <Button variant="outline" size="sm" onClick={handleViewHistory}>
              <Icon name="FileText" size={16} className="mr-2" />
              Historial Médico
            </Button>
            
            <Button variant="outline" size="sm" onClick={handleViewOdontogram}>
              <Icon name="Tooth" size={16} className="mr-2" />
              Odontograma
            </Button>

            {onDismiss && (
              <button
                onClick={handleDismiss}
                className="p-2 hover:bg-muted rounded-md transition-smooth"
                title="Cerrar contexto del paciente"
              >
                <Icon name="X" size={16} className="text-muted-foreground" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientContextBar;