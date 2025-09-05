import React from 'react';
import Icon from '../../../components/AppIcon';
import Image from '../../../components/AppImage';

const PatientCard = ({ patient, isSelected, onClick }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'text-accent';
      case 'overdue':
        return 'text-error';
      case 'scheduled':
        return 'text-warning';
      default:
        return 'text-muted-foreground';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return 'CheckCircle';
      case 'overdue':
        return 'AlertCircle';
      case 'scheduled':
        return 'Clock';
      default:
        return 'User';
    }
  };

  return (
    <div
      onClick={() => onClick(patient)}
      className={`p-4 border border-border rounded-lg cursor-pointer transition-all duration-200 hover:bg-muted/50 ${
        isSelected ? 'bg-primary/10 border-primary' : 'bg-card'
      }`}
    >
      <div className="flex items-start space-x-3">
        <div className="relative">
          <div className="w-12 h-12 rounded-full overflow-hidden bg-muted">
            <Image
              src={patient?.avatar}
              alt={`${patient?.firstName} ${patient?.lastName}`}
              className="w-full h-full object-cover"
            />
          </div>
          <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-card flex items-center justify-center ${
            patient?.status === 'active' ? 'bg-accent' : 
            patient?.status === 'overdue' ? 'bg-error' : 
            patient?.status === 'scheduled' ? 'bg-warning' : 'bg-muted'
          }`}>
            <Icon 
              name={getStatusIcon(patient?.status)} 
              size={8} 
              color="white" 
            />
          </div>
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-foreground truncate">
              {patient?.firstName} {patient?.lastName}
            </h3>
            <span className={`text-xs font-medium ${getStatusColor(patient?.status)}`}>
              {patient?.status === 'active' ? 'Activo' :
               patient?.status === 'overdue' ? 'Vencido' :
               patient?.status === 'scheduled' ? 'Programado' : 'Inactivo'}
            </span>
          </div>

          <div className="mt-1 space-y-1">
            <div className="flex items-center space-x-2 text-xs text-muted-foreground">
              <Icon name="Phone" size={12} />
              <span className="truncate">{patient?.phone}</span>
            </div>
            <div className="flex items-center space-x-2 text-xs text-muted-foreground">
              <Icon name="Mail" size={12} />
              <span className="truncate">{patient?.email}</span>
            </div>
          </div>

          <div className="mt-2 flex items-center justify-between">
            <div className="flex items-center space-x-1 text-xs text-muted-foreground">
              <Icon name="Calendar" size={12} />
              <span>Última visita: {patient?.lastVisit}</span>
            </div>
            {patient?.assignedDentist && (
              <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                <Icon name="UserCheck" size={12} />
                <span className="truncate max-w-20">{patient?.assignedDentist}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientCard;