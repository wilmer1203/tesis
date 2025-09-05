import React from 'react';
import Icon from '../../../components/AppIcon';

const DashboardStats = ({ stats }) => {
  const defaultStats = {
    pacientes_asignados: 24,
    citas_hoy: 6,
    tratamientos_pendientes: 12,
    urgencias: 3
  };

  const currentStats = stats || defaultStats;

  const statCards = [
    {
      title: 'Pacientes Asignados',
      value: currentStats?.pacientes_asignados,
      icon: 'Users',
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      borderColor: 'border-primary/20'
    },
    {
      title: 'Citas Hoy',
      value: currentStats?.citas_hoy,
      icon: 'Calendar',
      color: 'text-success',
      bgColor: 'bg-success/10',
      borderColor: 'border-success/20'
    },
    {
      title: 'Tratamientos Pendientes',
      value: currentStats?.tratamientos_pendientes,
      icon: 'Clock',
      color: 'text-warning',
      bgColor: 'bg-warning/10',
      borderColor: 'border-warning/20'
    },
    {
      title: 'Urgencias',
      value: currentStats?.urgencias,
      icon: 'AlertTriangle',
      color: 'text-error',
      bgColor: 'bg-error/10',
      borderColor: 'border-error/20'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {statCards?.map((stat, index) => (
        <div
          key={index}
          className={`p-4 bg-card border rounded-lg ${stat?.borderColor} ${stat?.bgColor}/50`}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground mb-1">
                {stat?.title}
              </p>
              <p className="text-2xl font-bold text-card-foreground">
                {stat?.value}
              </p>
            </div>
            <div className={`p-3 rounded-lg ${stat?.bgColor}`}>
              <Icon 
                name={stat?.icon} 
                size={24} 
                className={stat?.color}
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DashboardStats;