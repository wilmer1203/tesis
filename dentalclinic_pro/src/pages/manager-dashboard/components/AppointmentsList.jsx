import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const AppointmentsList = () => {
  const [selectedFilter, setSelectedFilter] = useState('today');

  const appointments = [
    {
      id: 1,
      patientName: "María González",
      dentist: "Dr. Carlos Ruiz",
      time: "09:00",
      treatment: "Limpieza dental",
      status: "confirmed",
      duration: "30 min",
      phone: "+34 612 345 678"
    },
    {
      id: 2,
      patientName: "Juan Martínez",
      dentist: "Dra. Ana López",
      time: "10:30",
      treatment: "Extracción molar",
      status: "pending",
      duration: "45 min",
      phone: "+34 623 456 789"
    },
    {
      id: 3,
      patientName: "Carmen Rodríguez",
      dentist: "Dr. Miguel Torres",
      time: "11:15",
      treatment: "Endodoncia",
      status: "in-progress",
      duration: "90 min",
      phone: "+34 634 567 890"
    },
    {
      id: 4,
      patientName: "Pedro Sánchez",
      dentist: "Dr. Carlos Ruiz",
      time: "14:00",
      treatment: "Revisión general",
      status: "confirmed",
      duration: "20 min",
      phone: "+34 645 678 901"
    },
    {
      id: 5,
      patientName: "Isabel Fernández",
      dentist: "Dra. Ana López",
      time: "15:30",
      treatment: "Ortodoncia",
      status: "confirmed",
      duration: "60 min",
      phone: "+34 656 789 012"
    }
  ];

  const getStatusColor = (status) => {
    const colors = {
      confirmed: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
      pending: "bg-amber-500/10 text-amber-400 border-amber-500/20",
      "in-progress": "bg-blue-500/10 text-blue-400 border-blue-500/20",
      completed: "bg-green-500/10 text-green-400 border-green-500/20",
      cancelled: "bg-red-500/10 text-red-400 border-red-500/20"
    };
    return colors?.[status] || colors?.pending;
  };

  const getStatusText = (status) => {
    const statusTexts = {
      confirmed: "Confirmada",
      pending: "Pendiente",
      "in-progress": "En Progreso",
      completed: "Completada",
      cancelled: "Cancelada"
    };
    return statusTexts?.[status] || status;
  };

  const filters = [
    { id: 'today', label: 'Hoy', count: 5 },
    { id: 'tomorrow', label: 'Mañana', count: 8 },
    { id: 'week', label: 'Esta Semana', count: 23 }
  ];

  return (
    <div className="bg-surface border border-border rounded-lg shadow-custom-md">
      <div className="p-6 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-foreground">Citas Programadas</h2>
          <Button 
            variant="outline" 
            iconName="Calendar" 
            iconPosition="left"
            iconSize={16}
          >
            Ver Calendario
          </Button>
        </div>
        
        <div className="flex space-x-2">
          {filters?.map((filter) => (
            <Button
              key={filter?.id}
              variant={selectedFilter === filter?.id ? "default" : "ghost"}
              onClick={() => setSelectedFilter(filter?.id)}
              className="text-sm"
            >
              {filter?.label} ({filter?.count})
            </Button>
          ))}
        </div>
      </div>
      <div className="p-6">
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {appointments?.map((appointment) => (
            <div
              key={appointment?.id}
              className="flex items-center justify-between p-4 bg-muted/30 rounded-lg hover:bg-muted/50 transition-colors duration-150"
            >
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                  <Icon name="User" size={20} color="var(--color-primary)" />
                </div>
                
                <div className="space-y-1">
                  <h3 className="text-sm font-medium text-foreground">
                    {appointment?.patientName}
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    {appointment?.dentist} • {appointment?.treatment}
                  </p>
                  <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                    <Icon name="Clock" size={12} />
                    <span>{appointment?.time} ({appointment?.duration})</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className={`px-2 py-1 rounded-md text-xs font-medium border ${getStatusColor(appointment?.status)}`}>
                  {getStatusText(appointment?.status)}
                </div>
                
                <div className="flex space-x-1">
                  <Button
                    variant="ghost"
                    iconName="Phone"
                    iconSize={14}
                    className="p-2"
                    onClick={() => console.log(`Llamar a ${appointment?.phone}`)}
                  />
                  <Button
                    variant="ghost"
                    iconName="Edit"
                    iconSize={14}
                    className="p-2"
                    onClick={() => console.log(`Editar cita ${appointment?.id}`)}
                  />
                  <Button
                    variant="ghost"
                    iconName="MoreVertical"
                    iconSize={14}
                    className="p-2"
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AppointmentsList;