import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const TodaySchedule = () => {
  const [selectedAppointment, setSelectedAppointment] = useState(null);

  const todayAppointments = [
    {
      id: 1,
      time: "09:00",
      patient: "María González",
      phone: "+34 612 345 678",
      treatment: "Limpieza dental",
      dentist: "Dr. Rodríguez",
      status: "confirmed",
      duration: 30,
      notes: "Primera visita"
    },
    {
      id: 2,
      time: "09:30",
      patient: "Carlos Martín",
      phone: "+34 623 456 789",
      treatment: "Empaste",
      dentist: "Dr. López",
      status: "waiting",
      duration: 45,
      notes: "Dolor en muela superior derecha"
    },
    {
      id: 3,
      time: "10:15",
      patient: "Ana Fernández",
      phone: "+34 634 567 890",
      treatment: "Revisión",
      dentist: "Dr. Rodríguez",
      status: "in-progress",
      duration: 30,
      notes: "Control post-tratamiento"
    },
    {
      id: 4,
      time: "11:00",
      patient: "José Ruiz",
      phone: "+34 645 678 901",
      treatment: "Extracción",
      dentist: "Dr. López",
      status: "completed",
      duration: 60,
      notes: "Muela del juicio"
    },
    {
      id: 5,
      time: "12:00",
      patient: "Laura Sánchez",
      phone: "+34 656 789 012",
      treatment: "Ortodoncia",
      dentist: "Dr. Rodríguez",
      status: "confirmed",
      duration: 45,
      notes: "Ajuste de brackets"
    },
    {
      id: 6,
      time: "14:30",
      patient: "Miguel Torres",
      phone: "+34 667 890 123",
      treatment: "Implante",
      dentist: "Dr. López",
      status: "confirmed",
      duration: 90,
      notes: "Colocación de implante"
    }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return 'text-blue-400 bg-blue-500/20';
      case 'waiting':
        return 'text-yellow-400 bg-yellow-500/20';
      case 'in-progress':
        return 'text-green-400 bg-green-500/20';
      case 'completed':
        return 'text-gray-400 bg-gray-500/20';
      default:
        return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'confirmed':
        return 'Confirmada';
      case 'waiting':
        return 'Esperando';
      case 'in-progress':
        return 'En curso';
      case 'completed':
        return 'Completada';
      default:
        return 'Desconocido';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'confirmed':
        return 'CheckCircle';
      case 'waiting':
        return 'Clock';
      case 'in-progress':
        return 'Activity';
      case 'completed':
        return 'CheckCircle2';
      default:
        return 'Circle';
    }
  };

  const handleStatusChange = (appointmentId, newStatus) => {
    console.log(`Cambiando estado de cita ${appointmentId} a ${newStatus}`);
  };

  return (
    <div className="bg-surface rounded-lg border border-border shadow-custom-md h-full">
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Icon name="Calendar" size={20} color="var(--color-primary)" />
            <h2 className="text-lg font-semibold text-foreground">
              Agenda de Hoy
            </h2>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-muted-foreground">
              {new Date()?.toLocaleDateString('es-ES', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </span>
            <Button variant="ghost" className="p-2">
              <Icon name="RefreshCw" size={16} />
            </Button>
          </div>
        </div>
      </div>
      <div className="p-4">
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {todayAppointments?.map((appointment) => (
            <div
              key={appointment?.id}
              className={`p-3 rounded-lg border transition-all duration-200 cursor-pointer hover:shadow-custom-sm ${
                selectedAppointment?.id === appointment?.id
                  ? 'border-primary bg-primary/5' :'border-border bg-card hover:bg-muted/50'
              }`}
              onClick={() => setSelectedAppointment(appointment)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-sm font-mono text-primary font-medium">
                      {appointment?.time}
                    </span>
                    <span
                      className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                        appointment?.status
                      )}`}
                    >
                      <Icon 
                        name={getStatusIcon(appointment?.status)} 
                        size={12} 
                        className="mr-1" 
                      />
                      {getStatusText(appointment?.status)}
                    </span>
                  </div>

                  <div className="space-y-1">
                    <h3 className="font-medium text-foreground">
                      {appointment?.patient}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {appointment?.treatment} • {appointment?.dentist}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {appointment?.phone} • {appointment?.duration} min
                    </p>
                    {appointment?.notes && (
                      <p className="text-xs text-muted-foreground italic">
                        {appointment?.notes}
                      </p>
                    )}
                  </div>
                </div>

                <div className="flex flex-col space-y-1 ml-3">
                  {appointment?.status === 'confirmed' && (
                    <Button
                      variant="ghost"
                      onClick={(e) => {
                        e?.stopPropagation();
                        handleStatusChange(appointment?.id, 'waiting');
                      }}
                      className="p-1 h-auto"
                    >
                      <Icon name="Clock" size={14} color="var(--color-warning)" />
                    </Button>
                  )}
                  {appointment?.status === 'waiting' && (
                    <Button
                      variant="ghost"
                      onClick={(e) => {
                        e?.stopPropagation();
                        handleStatusChange(appointment?.id, 'in-progress');
                      }}
                      className="p-1 h-auto"
                    >
                      <Icon name="Play" size={14} color="var(--color-success)" />
                    </Button>
                  )}
                  {appointment?.status === 'in-progress' && (
                    <Button
                      variant="ghost"
                      onClick={(e) => {
                        e?.stopPropagation();
                        handleStatusChange(appointment?.id, 'completed');
                      }}
                      className="p-1 h-auto"
                    >
                      <Icon name="Check" size={14} color="var(--color-success)" />
                    </Button>
                  )}
                  <Button
                    variant="ghost"
                    className="p-1 h-auto"
                  >
                    <Icon name="MoreVertical" size={14} />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {todayAppointments?.length === 0 && (
          <div className="text-center py-8">
            <Icon name="Calendar" size={48} color="var(--color-muted-foreground)" className="mx-auto mb-3" />
            <p className="text-muted-foreground">No hay citas programadas para hoy</p>
          </div>
        )}
      </div>
      <div className="p-4 border-t border-border">
        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">
            Total: {todayAppointments?.length} citas
          </span>
          <div className="flex items-center space-x-4">
            <span className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="text-muted-foreground">Confirmadas</span>
            </span>
            <span className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <span className="text-muted-foreground">Esperando</span>
            </span>
            <span className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-muted-foreground">En curso</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TodaySchedule;