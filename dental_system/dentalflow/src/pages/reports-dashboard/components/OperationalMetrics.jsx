import React, { useState } from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Line, AreaChart, Area } from 'recharts';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const OperationalMetrics = ({ dateRange, className = '' }) => {
  const [selectedView, setSelectedView] = useState('queue');
  const [selectedTimeframe, setSelectedTimeframe] = useState('daily');

  // Mock operational data
  const queueMetrics = [
    { time: '08:00', avg_wait: 12, queue_length: 3, efficiency: 85 },
    { time: '09:00', avg_wait: 18, queue_length: 5, efficiency: 78 },
    { time: '10:00', avg_wait: 25, queue_length: 8, efficiency: 72 },
    { time: '11:00', avg_wait: 22, queue_length: 6, efficiency: 75 },
    { time: '12:00', avg_wait: 15, queue_length: 4, efficiency: 82 },
    { time: '13:00', avg_wait: 8, queue_length: 2, efficiency: 90 },
    { time: '14:00', avg_wait: 20, queue_length: 7, efficiency: 76 },
    { time: '15:00', avg_wait: 28, queue_length: 9, efficiency: 68 },
    { time: '16:00', avg_wait: 24, queue_length: 7, efficiency: 73 },
    { time: '17:00', avg_wait: 16, queue_length: 4, efficiency: 80 }
  ];

  const utilizationData = [
    { dentist: 'Dr. María González', utilization: 92, appointments: 8, no_shows: 1, efficiency: 88 },
    { dentist: 'Dr. Carlos Mendoza', utilization: 88, appointments: 7, no_shows: 0, efficiency: 92 },
    { dentist: 'Dr. Ana Rodríguez', utilization: 85, appointments: 6, no_shows: 2, efficiency: 78 },
    { dentist: 'Dr. Luis Herrera', utilization: 90, appointments: 8, no_shows: 1, efficiency: 85 }
  ];

  const resourceEfficiency = [
    { resource: 'Consultorio 1', utilization: 95, downtime: 30, maintenance: 15 },
    { resource: 'Consultorio 2', utilization: 88, downtime: 45, maintenance: 20 },
    { resource: 'Consultorio 3', utilization: 92, downtime: 35, maintenance: 10 },
    { resource: 'Equipo Rayos X', utilization: 78, downtime: 60, maintenance: 45 },
    { resource: 'Autoclave', utilization: 85, downtime: 40, maintenance: 25 }
  ];

  const peakHoursAnalysis = [
    { hour: '08:00', patients: 12, wait_time: 8, satisfaction: 4.8 },
    { hour: '09:00', patients: 18, wait_time: 15, satisfaction: 4.6 },
    { hour: '10:00', patients: 25, wait_time: 22, satisfaction: 4.3 },
    { hour: '11:00', patients: 22, wait_time: 18, satisfaction: 4.5 },
    { hour: '12:00', patients: 8, wait_time: 5, satisfaction: 4.9 },
    { hour: '13:00', patients: 6, wait_time: 3, satisfaction: 5.0 },
    { hour: '14:00', patients: 20, wait_time: 20, satisfaction: 4.4 },
    { hour: '15:00', patients: 28, wait_time: 25, satisfaction: 4.2 },
    { hour: '16:00', patients: 24, wait_time: 22, satisfaction: 4.3 },
    { hour: '17:00', patients: 15, wait_time: 12, satisfaction: 4.7 }
  ];

  const bottleneckAnalysis = [
    { process: 'Registro de Paciente', avg_time: 8, target_time: 5, efficiency: 62 },
    { process: 'Preparación Consultorio', avg_time: 12, target_time: 10, efficiency: 83 },
    { process: 'Consulta Inicial', avg_time: 25, target_time: 20, efficiency: 80 },
    { process: 'Tratamiento', avg_time: 45, target_time: 40, efficiency: 89 },
    { process: 'Procesamiento de Pago', avg_time: 15, target_time: 8, efficiency: 53 },
    { process: 'Limpieza Consultorio', avg_time: 18, target_time: 15, efficiency: 83 }
  ];

  const operationalKPIs = [
    {
      title: 'Tiempo Espera Promedio',
      value: '18.5',
      unit: 'min',
      change: '-2.3',
      trend: 'down',
      icon: 'Clock',
      color: 'text-success'
    },
    {
      title: 'Utilización Promedio',
      value: '88.7%',
      unit: '',
      change: '+3.2%',
      trend: 'up',
      icon: 'Activity',
      color: 'text-success'
    },
    {
      title: 'Eficiencia Operacional',
      value: '85.8%',
      unit: '',
      change: '+1.5%',
      trend: 'up',
      icon: 'TrendingUp',
      color: 'text-success'
    },
    {
      title: 'Pacientes por Hora',
      value: '3.2',
      unit: '',
      change: '+0.4',
      trend: 'up',
      icon: 'Users',
      color: 'text-success'
    }
  ];

  const getEfficiencyColor = (value) => {
    if (value >= 85) return 'text-success';
    if (value >= 70) return 'text-warning';
    return 'text-error';
  };

  const getUtilizationColor = (value) => {
    if (value >= 90) return 'text-success';
    if (value >= 80) return 'text-warning';
    return 'text-error';
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload?.length) {
      return (
        <div className="bg-popover border border-border rounded-md shadow-modal p-3">
          <p className="text-sm font-medium text-foreground mb-2">{label}</p>
          {payload?.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry?.color }}>
              {entry?.name}: {entry?.value}
              {entry?.name?.includes('wait') || entry?.name?.includes('time') ? ' min' : ''}
              {entry?.name?.includes('efficiency') || entry?.name?.includes('utilization') ? '%' : ''}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {operationalKPIs?.map((kpi, index) => (
          <div key={index} className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Icon name={kpi?.icon} size={20} className="text-primary" />
              <div className={`flex items-center space-x-1 text-xs ${kpi?.color}`}>
                <Icon name={kpi?.trend === 'up' ? 'ArrowUp' : 'ArrowDown'} size={12} />
                <span>{kpi?.change}</span>
              </div>
            </div>
            <div className="text-2xl font-bold text-foreground mb-1">
              {kpi?.value}
              <span className="text-sm font-normal text-muted-foreground ml-1">{kpi?.unit}</span>
            </div>
            <div className="text-sm text-muted-foreground">{kpi?.title}</div>
          </div>
        ))}
      </div>
      {/* View Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex flex-wrap gap-2">
          <Button
            variant={selectedView === 'queue' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('queue')}
          >
            Análisis de Colas
          </Button>
          <Button
            variant={selectedView === 'utilization' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('utilization')}
          >
            Utilización
          </Button>
          <Button
            variant={selectedView === 'resources' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('resources')}
          >
            Recursos
          </Button>
          <Button
            variant={selectedView === 'bottlenecks' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('bottlenecks')}
          >
            Cuellos de Botella
          </Button>
        </div>

        <select
          value={selectedTimeframe}
          onChange={(e) => setSelectedTimeframe(e?.target?.value)}
          className="px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="hourly">Por Hora</option>
          <option value="daily">Diario</option>
          <option value="weekly">Semanal</option>
          <option value="monthly">Mensual</option>
        </select>
      </div>
      {/* Queue Analysis */}
      {selectedView === 'queue' && (
        <div className="space-y-6">
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Análisis de Colas por Hora</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={queueMetrics}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                  <XAxis 
                    dataKey="time" 
                    stroke="var(--color-muted-foreground)"
                    fontSize={12}
                  />
                  <YAxis 
                    stroke="var(--color-muted-foreground)"
                    fontSize={12}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Area 
                    type="monotone" 
                    dataKey="avg_wait" 
                    name="Tiempo Espera (min)"
                    stroke="var(--color-warning)" 
                    fill="var(--color-warning)"
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="queue_length" 
                    name="Longitud Cola"
                    stroke="var(--color-primary)" 
                    strokeWidth={3}
                    dot={{ fill: 'var(--color-primary)', strokeWidth: 2, r: 4 }}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Análisis de Horas Pico</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              {peakHoursAnalysis?.slice(0, 5)?.map((hour, index) => (
                <div key={index} className="bg-muted rounded-lg p-4 text-center">
                  <div className="text-lg font-semibold text-foreground mb-2">{hour?.hour}</div>
                  <div className="space-y-2">
                    <div>
                      <div className="text-2xl font-bold text-primary">{hour?.patients}</div>
                      <div className="text-xs text-muted-foreground">Pacientes</div>
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-warning">{hour?.wait_time} min</div>
                      <div className="text-xs text-muted-foreground">Espera</div>
                    </div>
                    <div className="flex items-center justify-center space-x-1">
                      <Icon name="Star" size={12} className="text-warning fill-current" />
                      <span className="text-sm font-medium text-foreground">{hour?.satisfaction}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      {/* Utilization Analysis */}
      {selectedView === 'utilization' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Utilización por Dentista</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Dentista</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Utilización</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Citas</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Ausencias</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Eficiencia</th>
                </tr>
              </thead>
              <tbody>
                {utilizationData?.map((dentist, index) => (
                  <tr key={index} className="border-b border-border last:border-b-0 hover:bg-muted/50">
                    <td className="py-3 px-4">
                      <div className="font-medium text-foreground">{dentist?.dentist}</div>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className={`font-semibold ${getUtilizationColor(dentist?.utilization)}`}>
                        {dentist?.utilization}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center text-foreground">{dentist?.appointments}</td>
                    <td className="py-3 px-4 text-center">
                      <span className={dentist?.no_shows > 0 ? 'text-error' : 'text-success'}>
                        {dentist?.no_shows}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className={`font-semibold ${getEfficiencyColor(dentist?.efficiency)}`}>
                        {dentist?.efficiency}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {/* Resource Efficiency */}
      {selectedView === 'resources' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Eficiencia de Recursos</h3>
          <div className="space-y-4">
            {resourceEfficiency?.map((resource, index) => (
              <div key={index} className="bg-muted rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-foreground">{resource?.resource}</h4>
                  <span className={`font-bold text-lg ${getUtilizationColor(resource?.utilization)}`}>
                    {resource?.utilization}%
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-muted-foreground">Tiempo Inactivo</div>
                    <div className="font-medium text-foreground">{resource?.downtime} min</div>
                  </div>
                  <div>
                    <div className="text-muted-foreground">Mantenimiento</div>
                    <div className="font-medium text-foreground">{resource?.maintenance} min</div>
                  </div>
                  <div>
                    <div className="text-muted-foreground">Tiempo Productivo</div>
                    <div className="font-medium text-success">
                      {480 - resource?.downtime - resource?.maintenance} min
                    </div>
                  </div>
                </div>
                <div className="mt-3">
                  <div className="w-full bg-border rounded-full h-2">
                    <div 
                      className="bg-success h-2 rounded-full transition-all duration-300"
                      style={{ width: `${resource?.utilization}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      {/* Bottleneck Analysis */}
      {selectedView === 'bottlenecks' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Análisis de Cuellos de Botella</h3>
          <div className="space-y-4">
            {bottleneckAnalysis?.map((process, index) => (
              <div key={index} className="border border-border rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-foreground">{process.process}</h4>
                  <div className="flex items-center space-x-4">
                    <span className={`font-semibold ${getEfficiencyColor(process.efficiency)}`}>
                      {process.efficiency}%
                    </span>
                    {process.efficiency < 80 && (
                      <Icon name="AlertTriangle" size={16} className="text-warning" />
                    )}
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-muted-foreground">Tiempo Actual</div>
                    <div className="font-medium text-foreground">{process.avg_time} min</div>
                  </div>
                  <div>
                    <div className="text-muted-foreground">Tiempo Objetivo</div>
                    <div className="font-medium text-success">{process.target_time} min</div>
                  </div>
                  <div>
                    <div className="text-muted-foreground">Diferencia</div>
                    <div className={`font-medium ${process.avg_time > process.target_time ? 'text-error' : 'text-success'}`}>
                      {process.avg_time > process.target_time ? '+' : ''}{process.avg_time - process.target_time} min
                    </div>
                  </div>
                </div>
                <div className="mt-3">
                  <div className="w-full bg-border rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all duration-300 ${
                        process.efficiency >= 85 ? 'bg-success' : 
                        process.efficiency >= 70 ? 'bg-warning' : 'bg-error'
                      }`}
                      style={{ width: `${process.efficiency}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default OperationalMetrics;