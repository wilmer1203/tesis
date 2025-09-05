import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';

const KPIDashboard = ({ className = '' }) => {
  const [kpiData, setKpiData] = useState({});
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Mock real-time KPI data
  const kpiMetrics = [
    {
      id: 'daily_revenue',
      title: 'Ingresos del Día',
      value: '2.850.000',
      unit: 'Bs',
      change: '+12.5%',
      trend: 'up',
      icon: 'DollarSign',
      color: 'text-success',
      bgColor: 'bg-success/10',
      target: '3.000.000',
      progress: 95
    },
    {
      id: 'daily_revenue_usd',
      title: 'Ingresos USD',
      value: '$780',
      unit: '',
      change: '+8.3%',
      trend: 'up',
      icon: 'DollarSign',
      color: 'text-success',
      bgColor: 'bg-success/10',
      target: '$850',
      progress: 92
    },
    {
      id: 'patients_today',
      title: 'Pacientes Hoy',
      value: '28',
      unit: '',
      change: '+4',
      trend: 'up',
      icon: 'Users',
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      target: '32',
      progress: 88
    },
    {
      id: 'avg_wait_time',
      title: 'Tiempo Espera Promedio',
      value: '18.5',
      unit: 'min',
      change: '-3.2',
      trend: 'down',
      icon: 'Clock',
      color: 'text-success',
      bgColor: 'bg-success/10',
      target: '15',
      progress: 82
    },
    {
      id: 'dentist_utilization',
      title: 'Utilización Dentistas',
      value: '88.7%',
      unit: '',
      change: '+2.1%',
      trend: 'up',
      icon: 'Activity',
      color: 'text-warning',
      bgColor: 'bg-warning/10',
      target: '90%',
      progress: 99
    },
    {
      id: 'satisfaction_score',
      title: 'Satisfacción Promedio',
      value: '4.65',
      unit: '/5.0',
      change: '+0.15',
      trend: 'up',
      icon: 'Star',
      color: 'text-success',
      bgColor: 'bg-success/10',
      target: '4.8',
      progress: 97
    },
    {
      id: 'queue_length',
      title: 'Cola Actual',
      value: '12',
      unit: 'pacientes',
      change: '-2',
      trend: 'down',
      icon: 'Users',
      color: 'text-warning',
      bgColor: 'bg-warning/10',
      target: '8',
      progress: 67
    },
    {
      id: 'completion_rate',
      title: 'Tasa de Completación',
      value: '96.5%',
      unit: '',
      change: '+1.2%',
      trend: 'up',
      icon: 'CheckCircle',
      color: 'text-success',
      bgColor: 'bg-success/10',
      target: '98%',
      progress: 98
    }
  ];

  const alertsAndNotifications = [
    {
      id: 1,
      type: 'warning',
      title: 'Cola Larga en Consultorio 2',
      message: 'Tiempo de espera superior a 30 minutos',
      time: '14:25',
      priority: 'high'
    },
    {
      id: 2,
      type: 'success',
      title: 'Meta de Ingresos Alcanzada',
      message: 'Ingresos diarios superaron el objetivo',
      time: '13:45',
      priority: 'medium'
    },
    {
      id: 3,
      type: 'info',
      title: 'Nuevo Paciente Registrado',
      message: 'Ana María Rodríguez - Primera visita',
      time: '13:20',
      priority: 'low'
    }
  ];

  const quickActions = [
    {
      id: 'view_queue',
      label: 'Ver Cola',
      icon: 'Users',
      action: () => console.log('Navigate to queue'),
      color: 'bg-primary'
    },
    {
      id: 'add_patient',
      label: 'Nuevo Paciente',
      icon: 'UserPlus',
      action: () => console.log('Add patient'),
      color: 'bg-success'
    },
    {
      id: 'process_payment',
      label: 'Procesar Pago',
      icon: 'CreditCard',
      action: () => console.log('Process payment'),
      color: 'bg-warning'
    },
    {
      id: 'generate_report',
      label: 'Generar Reporte',
      icon: 'FileText',
      action: () => console.log('Generate report'),
      color: 'bg-secondary'
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(new Date());
      // Simulate real-time updates
      setKpiData(prev => ({
        ...prev,
        lastUpdate: new Date()
      }));
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getAlertIcon = (type) => {
    switch (type) {
      case 'warning':
        return { icon: 'AlertTriangle', color: 'text-warning' };
      case 'success':
        return { icon: 'CheckCircle', color: 'text-success' };
      case 'error':
        return { icon: 'AlertCircle', color: 'text-error' };
      default:
        return { icon: 'Info', color: 'text-primary' };
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'border-l-error';
      case 'medium':
        return 'border-l-warning';
      default:
        return 'border-l-primary';
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Dashboard en Tiempo Real</h2>
          <p className="text-sm text-muted-foreground">
            Última actualización: {lastUpdate?.toLocaleTimeString('es-VE')}
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1 text-sm text-success">
            <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
            <span>En vivo</span>
          </div>
        </div>
      </div>
      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiMetrics?.map((kpi) => (
          <div key={kpi?.id} className="bg-card border border-border rounded-lg p-4 hover:shadow-soft transition-smooth">
            <div className="flex items-center justify-between mb-3">
              <div className={`p-2 rounded-lg ${kpi?.bgColor}`}>
                <Icon name={kpi?.icon} size={20} className={kpi?.color} />
              </div>
              <div className={`flex items-center space-x-1 text-xs ${kpi?.color}`}>
                <Icon name={kpi?.trend === 'up' ? 'ArrowUp' : 'ArrowDown'} size={12} />
                <span>{kpi?.change}</span>
              </div>
            </div>

            <div className="space-y-2">
              <div>
                <div className="text-2xl font-bold text-foreground">
                  {kpi?.value}
                  <span className="text-sm font-normal text-muted-foreground ml-1">{kpi?.unit}</span>
                </div>
                <div className="text-sm text-muted-foreground">{kpi?.title}</div>
              </div>

              {/* Progress Bar */}
              <div className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-muted-foreground">Objetivo: {kpi?.target}</span>
                  <span className="text-foreground">{kpi?.progress}%</span>
                </div>
                <div className="w-full bg-border rounded-full h-1.5">
                  <div 
                    className={`h-1.5 rounded-full transition-all duration-300 ${
                      kpi?.progress >= 90 ? 'bg-success' : 
                      kpi?.progress >= 70 ? 'bg-warning' : 'bg-error'
                    }`}
                    style={{ width: `${Math.min(kpi?.progress, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Acciones Rápidas</h3>
          <div className="grid grid-cols-2 gap-3">
            {quickActions?.map((action) => (
              <button
                key={action?.id}
                onClick={action?.action}
                className={`flex flex-col items-center space-y-2 p-4 rounded-lg text-white hover:opacity-90 transition-smooth ${action?.color}`}
              >
                <Icon name={action?.icon} size={24} />
                <span className="text-sm font-medium">{action?.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Alerts and Notifications */}
        <div className="lg:col-span-2 bg-card border border-border rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-foreground">Alertas y Notificaciones</h3>
            <button className="text-sm text-primary hover:text-primary/80 transition-smooth">
              Ver todas
            </button>
          </div>

          <div className="space-y-3">
            {alertsAndNotifications?.map((alert) => {
              const alertConfig = getAlertIcon(alert?.type);
              return (
                <div 
                  key={alert?.id} 
                  className={`flex items-start space-x-3 p-3 bg-muted rounded-lg border-l-4 ${getPriorityColor(alert?.priority)}`}
                >
                  <Icon name={alertConfig?.icon} size={16} className={alertConfig?.color} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-medium text-foreground truncate">{alert?.title}</h4>
                      <span className="text-xs text-muted-foreground ml-2">{alert?.time}</span>
                    </div>
                    <p className="text-sm text-muted-foreground mt-1">{alert?.message}</p>
                  </div>
                  <button className="p-1 hover:bg-background rounded transition-smooth">
                    <Icon name="X" size={14} className="text-muted-foreground" />
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      {/* System Status */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Estado del Sistema</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <div className="w-3 h-3 bg-success rounded-full"></div>
              <span className="text-sm font-medium text-foreground">Servidor Principal</span>
            </div>
            <div className="text-xs text-muted-foreground">Funcionando correctamente</div>
          </div>

          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <div className="w-3 h-3 bg-success rounded-full"></div>
              <span className="text-sm font-medium text-foreground">Base de Datos</span>
            </div>
            <div className="text-xs text-muted-foreground">Conexión estable</div>
          </div>

          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <div className="w-3 h-3 bg-warning rounded-full"></div>
              <span className="text-sm font-medium text-foreground">Respaldos</span>
            </div>
            <div className="text-xs text-muted-foreground">Último: hace 2 horas</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KPIDashboard;