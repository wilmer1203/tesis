import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const StaffUtilization = () => {
  const staffData = [
    {
      id: 1,
      name: "Dr. Carlos Ruiz",
      role: "Dentista Senior",
      avatar: "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=100&h=100&fit=crop&crop=face",
      status: "active",
      todayAppointments: 8,
      completedToday: 6,
      utilization: 85,
      nextAppointment: "14:30 - María González"
    },
    {
      id: 2,
      name: "Dra. Ana López",
      role: "Ortodoncista",
      avatar: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=100&h=100&fit=crop&crop=face",
      status: "active",
      todayAppointments: 6,
      completedToday: 4,
      utilization: 72,
      nextAppointment: "15:00 - Juan Martínez"
    },
    {
      id: 3,
      name: "Dr. Miguel Torres",
      role: "Endodoncista",
      avatar: "https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=100&h=100&fit=crop&crop=face",
      status: "busy",
      todayAppointments: 5,
      completedToday: 3,
      utilization: 90,
      nextAppointment: "En consulta - Carmen Rodríguez"
    },
    {
      id: 4,
      name: "Ana Secretaria",
      role: "Recepcionista",
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=100&h=100&fit=crop&crop=face",
      status: "active",
      todayAppointments: 0,
      completedToday: 12,
      utilization: 68,
      nextAppointment: "Gestión administrativa"
    }
  ];

  const getStatusColor = (status) => {
    const colors = {
      active: "bg-emerald-500",
      busy: "bg-amber-500",
      offline: "bg-gray-500",
      break: "bg-blue-500"
    };
    return colors?.[status] || colors?.offline;
  };

  const getStatusText = (status) => {
    const statusTexts = {
      active: "Disponible",
      busy: "Ocupado",
      offline: "Desconectado",
      break: "En Descanso"
    };
    return statusTexts?.[status] || status;
  };

  const getUtilizationColor = (utilization) => {
    if (utilization >= 80) return "text-emerald-400";
    if (utilization >= 60) return "text-amber-400";
    return "text-red-400";
  };

  return (
    <div className="bg-surface border border-border rounded-lg p-6 shadow-custom-md">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-foreground">Utilización del Personal</h2>
        <Button 
          variant="outline" 
          iconName="Users" 
          iconPosition="left"
          iconSize={16}
        >
          Gestionar Personal
        </Button>
      </div>
      <div className="space-y-4">
        {staffData?.map((staff) => (
          <div
            key={staff?.id}
            className="flex items-center justify-between p-4 bg-muted/30 rounded-lg hover:bg-muted/50 transition-colors duration-150"
          >
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center overflow-hidden">
                  <img
                    src={staff?.avatar}
                    alt={staff?.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                  <div className="w-full h-full bg-primary/10 rounded-full flex items-center justify-center" style={{display: 'none'}}>
                    <Icon name="User" size={20} color="var(--color-primary)" />
                  </div>
                </div>
                <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-surface ${getStatusColor(staff?.status)}`}></div>
              </div>
              
              <div className="space-y-1">
                <h3 className="text-sm font-medium text-foreground">{staff?.name}</h3>
                <p className="text-xs text-muted-foreground">{staff?.role}</p>
                <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                  <span className={`px-2 py-1 rounded-md ${getStatusColor(staff?.status)} text-white`}>
                    {getStatusText(staff?.status)}
                  </span>
                </div>
              </div>
            </div>

            <div className="text-right space-y-1">
              <div className="flex items-center space-x-4">
                <div className="text-center">
                  <p className="text-lg font-semibold text-foreground">
                    {staff?.completedToday}/{staff?.todayAppointments}
                  </p>
                  <p className="text-xs text-muted-foreground">Citas</p>
                </div>
                
                <div className="text-center">
                  <p className={`text-lg font-semibold ${getUtilizationColor(staff?.utilization)}`}>
                    {staff?.utilization}%
                  </p>
                  <p className="text-xs text-muted-foreground">Utilización</p>
                </div>
              </div>
              
              <p className="text-xs text-muted-foreground max-w-32 truncate">
                {staff?.nextAppointment}
              </p>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6 pt-4 border-t border-border">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-lg font-semibold text-foreground">78%</p>
            <p className="text-xs text-muted-foreground">Promedio Utilización</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-emerald-400">3</p>
            <p className="text-xs text-muted-foreground">Personal Activo</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-amber-400">19</p>
            <p className="text-xs text-muted-foreground">Citas Restantes</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StaffUtilization;