import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const AppointmentSidebar = ({ 
  currentDate, 
  appointments, 
  waitList, 
  cancellations,
  onPatientClick 
}) => {
  const todayAppointments = appointments?.filter(apt => 
    apt?.date === currentDate?.toDateString()
  );

  const upcomingAppointments = todayAppointments?.filter(apt => new Date(`${apt.date} ${apt.time}`) > new Date())?.sort((a, b) => a?.time?.localeCompare(b?.time));

  const getStatusColor = (status) => {
    const colors = {
      confirmed: 'text-green-400',
      pending: 'text-yellow-400',
      cancelled: 'text-red-400',
      completed: 'text-blue-400'
    };
    return colors?.[status] || 'text-muted-foreground';
  };

  const getAppointmentTypeIcon = (type) => {
    const icons = {
      consultation: 'MessageCircle',
      treatment: 'Wrench',
      followup: 'RotateCcw',
      emergency: 'AlertTriangle',
      cleaning: 'Sparkles'
    };
    return icons?.[type] || 'Calendar';
  };

  return (
    <div className="w-80 bg-surface border-l border-border flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <h2 className="text-lg font-heading font-semibold text-foreground">
          Resumen del Día
        </h2>
        <p className="text-sm text-muted-foreground">
          {currentDate?.toLocaleDateString('es-ES', { 
            weekday: 'long', 
            month: 'long', 
            day: 'numeric' 
          })}
        </p>
      </div>
      <div className="flex-1 overflow-y-auto">
        {/* Statistics */}
        <div className="p-4 border-b border-border">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-card p-3 rounded-lg border border-border">
              <div className="flex items-center space-x-2">
                <Icon name="Calendar" size={16} color="var(--color-primary)" />
                <span className="text-sm text-muted-foreground">Total Citas</span>
              </div>
              <div className="text-2xl font-bold text-card-foreground mt-1">
                {todayAppointments?.length}
              </div>
            </div>
            
            <div className="bg-card p-3 rounded-lg border border-border">
              <div className="flex items-center space-x-2">
                <Icon name="Clock" size={16} color="var(--color-warning)" />
                <span className="text-sm text-muted-foreground">Pendientes</span>
              </div>
              <div className="text-2xl font-bold text-card-foreground mt-1">
                {upcomingAppointments?.length}
              </div>
            </div>
          </div>
        </div>

        {/* Upcoming Appointments */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-foreground">Próximas Citas</h3>
            <Icon name="ChevronRight" size={16} color="var(--color-muted-foreground)" />
          </div>
          
          <div className="space-y-3">
            {upcomingAppointments?.slice(0, 5)?.map((appointment) => (
              <div
                key={appointment?.id}
                className="p-3 bg-card rounded-lg border border-border hover:bg-muted/50 cursor-pointer transition-colors"
                onClick={() => onPatientClick(appointment)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <Icon 
                        name={getAppointmentTypeIcon(appointment?.type)} 
                        size={14} 
                        color="var(--color-primary)" 
                      />
                      <span className="font-medium text-card-foreground text-sm">
                        {appointment?.patientName}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground mb-1">
                      {appointment?.service}
                    </p>
                    <div className="flex items-center space-x-3 text-xs">
                      <span className="text-muted-foreground">
                        {appointment?.time}
                      </span>
                      <span className="text-muted-foreground">
                        {appointment?.duration} min
                      </span>
                      <span className={getStatusColor(appointment?.status)}>
                        {appointment?.status === 'confirmed' ? 'Confirmada' :
                         appointment?.status === 'pending' ? 'Pendiente' :
                         appointment?.status === 'cancelled' ? 'Cancelada' : 'Completada'}
                      </span>
                    </div>
                  </div>
                  
                  <div className="ml-2">
                    <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                      <span className="text-xs font-medium text-primary">
                        {appointment?.patientName?.charAt(0)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {upcomingAppointments?.length === 0 && (
              <div className="text-center py-6">
                <Icon name="Calendar" size={32} color="var(--color-muted-foreground)" className="mx-auto mb-2" />
                <p className="text-sm text-muted-foreground">
                  No hay citas pendientes para hoy
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Wait List */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-foreground">Lista de Espera</h3>
            <div className="flex items-center space-x-1">
              <span className="text-xs bg-warning/20 text-warning px-2 py-1 rounded-full">
                {waitList?.length}
              </span>
            </div>
          </div>
          
          <div className="space-y-2">
            {waitList?.slice(0, 3)?.map((patient) => (
              <div
                key={patient?.id}
                className="p-2 bg-card rounded border border-border hover:bg-muted/50 cursor-pointer"
                onClick={() => onPatientClick(patient)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-card-foreground">
                      {patient?.name}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {patient?.requestedService}
                    </p>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {patient?.waitTime}
                  </div>
                </div>
              </div>
            ))}
            
            {waitList?.length === 0 && (
              <p className="text-sm text-muted-foreground text-center py-3">
                No hay pacientes en lista de espera
              </p>
            )}
          </div>
        </div>

        {/* Cancellations */}
        <div className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-foreground">Cancelaciones</h3>
            <div className="flex items-center space-x-1">
              <Icon name="AlertTriangle" size={14} color="var(--color-error)" />
              <span className="text-xs bg-error/20 text-error px-2 py-1 rounded-full">
                {cancellations?.length}
              </span>
            </div>
          </div>
          
          <div className="space-y-2">
            {cancellations?.slice(0, 3)?.map((cancellation) => (
              <div
                key={cancellation?.id}
                className="p-2 bg-card rounded border border-border"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-card-foreground">
                      {cancellation?.patientName}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {cancellation?.originalTime} - {cancellation?.service}
                    </p>
                  </div>
                  <div className="text-xs text-error">
                    {cancellation?.reason}
                  </div>
                </div>
              </div>
            ))}
            
            {cancellations?.length === 0 && (
              <p className="text-sm text-muted-foreground text-center py-3">
                No hay cancelaciones hoy
              </p>
            )}
          </div>
        </div>
      </div>
      {/* Quick Actions */}
      <div className="p-4 border-t border-border">
        <div className="space-y-2">
          <Button
            variant="outline"
            fullWidth
            iconName="UserPlus"
            iconPosition="left"
            iconSize={16}
            className="text-sm"
          >
            Agregar a Lista de Espera
          </Button>
          
          <Button
            variant="outline"
            fullWidth
            iconName="MessageSquare"
            iconPosition="left"
            iconSize={16}
            className="text-sm"
          >
            Enviar Recordatorios
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AppointmentSidebar;