import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ActivityFeed = () => {
  const [filter, setFilter] = useState('all');

  const activities = [
    {
      id: 1,
      type: "appointment",
      title: "Nueva cita programada",
      description: "María González - Limpieza dental con Dr. Carlos Ruiz",
      time: "Hace 5 minutos",
      icon: "Calendar",
      color: "blue",
      user: "Secretaria Ana"
    },
    {
      id: 2,
      type: "payment",
      title: "Pago recibido",
      description: "€85.00 - Tratamiento de endodoncia (Juan Martínez)",
      time: "Hace 12 minutos",
      icon: "CreditCard",
      color: "emerald",
      user: "Sistema"
    },
    {
      id: 3,
      type: "patient",
      title: "Nuevo paciente registrado",
      description: "Carmen Rodríguez - Registro completado",
      time: "Hace 25 minutos",
      icon: "UserPlus",
      color: "purple",
      user: "Secretaria Ana"
    },
    {
      id: 4,
      type: "treatment",
      title: "Tratamiento completado",
      description: "Extracción molar - Pedro Sánchez",
      time: "Hace 1 hora",
      icon: "CheckCircle",
      color: "emerald",
      user: "Dra. Ana López"
    },
    {
      id: 5,
      type: "system",
      title: "Respaldo automático",
      description: "Copia de seguridad completada exitosamente",
      time: "Hace 2 horas",
      icon: "Database",
      color: "gray",
      user: "Sistema"
    },
    {
      id: 6,
      type: "appointment",
      title: "Cita cancelada",
      description: "Isabel Fernández - Ortodoncia reprogramada",
      time: "Hace 3 horas",
      icon: "XCircle",
      color: "red",
      user: "Secretaria Ana"
    },
    {
      id: 7,
      type: "inventory",
      title: "Stock bajo",
      description: "Anestesia local - Solo quedan 5 unidades",
      time: "Hace 4 horas",
      icon: "AlertTriangle",
      color: "amber",
      user: "Sistema"
    }
  ];

  const getIconColor = (color) => {
    const colors = {
      blue: "var(--color-primary)",
      emerald: "var(--color-success)",
      purple: "var(--color-secondary)",
      red: "var(--color-error)",
      amber: "var(--color-warning)",
      gray: "var(--color-muted-foreground)"
    };
    return colors?.[color] || colors?.gray;
  };

  const getBgColor = (color) => {
    const colors = {
      blue: "bg-blue-500/10",
      emerald: "bg-emerald-500/10",
      purple: "bg-purple-500/10",
      red: "bg-red-500/10",
      amber: "bg-amber-500/10",
      gray: "bg-gray-500/10"
    };
    return colors?.[color] || colors?.gray;
  };

  const filterOptions = [
    { id: 'all', label: 'Todas', count: activities?.length },
    { id: 'appointment', label: 'Citas', count: activities?.filter(a => a?.type === 'appointment')?.length },
    { id: 'payment', label: 'Pagos', count: activities?.filter(a => a?.type === 'payment')?.length },
    { id: 'system', label: 'Sistema', count: activities?.filter(a => a?.type === 'system')?.length }
  ];

  const filteredActivities = filter === 'all' 
    ? activities 
    : activities?.filter(activity => activity?.type === filter);

  return (
    <div className="bg-surface border border-border rounded-lg shadow-custom-md">
      <div className="p-6 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-foreground">Actividad Reciente</h2>
          <Button 
            variant="outline" 
            iconName="RefreshCw" 
            iconSize={16}
            onClick={() => console.log("Actualizar actividad")}
          >
            Actualizar
          </Button>
        </div>
        
        <div className="flex space-x-2 overflow-x-auto">
          {filterOptions?.map((option) => (
            <Button
              key={option?.id}
              variant={filter === option?.id ? "default" : "ghost"}
              onClick={() => setFilter(option?.id)}
              className="text-sm whitespace-nowrap"
            >
              {option?.label} ({option?.count})
            </Button>
          ))}
        </div>
      </div>
      <div className="p-6">
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {filteredActivities?.map((activity, index) => (
            <div key={activity?.id} className="relative">
              {index !== filteredActivities?.length - 1 && (
                <div className="absolute left-6 top-12 w-px h-8 bg-border"></div>
              )}
              
              <div className="flex items-start space-x-4">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center ${getBgColor(activity?.color)}`}>
                  <Icon 
                    name={activity?.icon} 
                    size={18} 
                    color={getIconColor(activity?.color)} 
                  />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-medium text-foreground">
                      {activity?.title}
                    </h3>
                    <span className="text-xs text-muted-foreground">
                      {activity?.time}
                    </span>
                  </div>
                  
                  <p className="text-sm text-muted-foreground mt-1">
                    {activity?.description}
                  </p>
                  
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-xs text-muted-foreground">
                      Por: {activity?.user}
                    </span>
                    
                    <Button
                      variant="ghost"
                      iconName="MoreHorizontal"
                      iconSize={14}
                      className="p-1"
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-4 pt-4 border-t border-border">
          <Button 
            variant="outline" 
            fullWidth
            iconName="Eye"
            iconPosition="left"
            iconSize={16}
          >
            Ver Toda la Actividad
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ActivityFeed;