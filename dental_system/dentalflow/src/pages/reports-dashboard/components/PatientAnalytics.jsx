import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const PatientAnalytics = ({ dateRange, className = '' }) => {
  const [selectedMetric, setSelectedMetric] = useState('demographics');
  const [showDetails, setShowDetails] = useState(false);

  // Mock patient analytics data
  const demographicsData = [
    { age_group: '18-25', count: 45, percentage: 15 },
    { age_group: '26-35', count: 78, percentage: 26 },
    { age_group: '36-45', count: 92, percentage: 31 },
    { age_group: '46-55', count: 56, percentage: 19 },
    { age_group: '56+', count: 29, percentage: 9 }
  ];

  const satisfactionTrends = [
    { date: '01/09', satisfaction: 4.2, responses: 28 },
    { date: '02/09', satisfaction: 4.5, responses: 32 },
    { date: '03/09', satisfaction: 4.3, responses: 29 },
    { date: '04/09', satisfaction: 4.7, responses: 35 }
  ];

  const treatmentPreferences = [
    { treatment: 'Limpieza', count: 156, percentage: 35, color: '#2563EB' },
    { treatment: 'Empastes', count: 89, percentage: 20, color: '#059669' },
    { treatment: 'Blanqueamiento', count: 67, percentage: 15, color: '#F59E0B' },
    { treatment: 'Ortodoncia', count: 45, percentage: 10, color: '#EF4444' },
    { treatment: 'Endodoncia', count: 34, percentage: 8, color: '#8B5CF6' },
    { treatment: 'Otros', count: 54, percentage: 12, color: '#6B7280' }
  ];

  const retentionData = [
    { month: 'Ene', new_patients: 45, returning: 78, retention_rate: 63 },
    { month: 'Feb', new_patients: 52, returning: 85, retention_rate: 62 },
    { month: 'Mar', new_patients: 48, returning: 92, retention_rate: 66 },
    { month: 'Abr', new_patients: 56, returning: 89, retention_rate: 61 }
  ];

  const patientJourney = [
    { stage: 'Primera Visita', count: 234, conversion: 100 },
    { stage: 'Segunda Visita', count: 189, conversion: 81 },
    { stage: 'Tratamiento Completo', count: 156, conversion: 67 },
    { stage: 'Seguimiento', count: 134, conversion: 57 },
    { stage: 'Paciente Fiel', count: 98, conversion: 42 }
  ];

  const waitTimeAnalysis = [
    { time_range: '0-15 min', count: 145, satisfaction: 4.8 },
    { time_range: '16-30 min', count: 89, satisfaction: 4.5 },
    { time_range: '31-45 min', count: 34, satisfaction: 4.1 },
    { time_range: '46+ min', count: 12, satisfaction: 3.6 }
  ];

  const summaryCards = [
    {
      title: 'Pacientes Totales',
      value: '1,247',
      change: '+12.3%',
      trend: 'up',
      icon: 'Users',
      color: 'text-success'
    },
    {
      title: 'Satisfacción Promedio',
      value: '4.43',
      change: '+0.23',
      trend: 'up',
      icon: 'Star',
      color: 'text-success'
    },
    {
      title: 'Tasa de Retención',
      value: '63.2%',
      change: '+2.1%',
      trend: 'up',
      icon: 'RefreshCw',
      color: 'text-success'
    },
    {
      title: 'Tiempo Espera Promedio',
      value: '18.5',
      change: '-3.2',
      trend: 'down',
      icon: 'Clock',
      color: 'text-success'
    }
  ];

  const getSatisfactionColor = (rating) => {
    if (rating >= 4.5) return 'text-success';
    if (rating >= 4.0) return 'text-warning';
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
              {entry?.name === 'satisfaction' && ' ⭐'}
              {entry?.name === 'retention_rate' && '%'}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryCards?.map((card, index) => (
          <div key={index} className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Icon name={card?.icon} size={20} className="text-primary" />
              <div className={`flex items-center space-x-1 text-xs ${card?.color}`}>
                <Icon name={card?.trend === 'up' ? 'ArrowUp' : 'ArrowDown'} size={12} />
                <span>{card?.change}</span>
              </div>
            </div>
            <div className="text-2xl font-bold text-foreground mb-1">{card?.value}</div>
            <div className="text-sm text-muted-foreground">{card?.title}</div>
          </div>
        ))}
      </div>
      {/* Metric Selection */}
      <div className="flex flex-wrap gap-2">
        <Button
          variant={selectedMetric === 'demographics' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setSelectedMetric('demographics')}
        >
          Demografía
        </Button>
        <Button
          variant={selectedMetric === 'satisfaction' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setSelectedMetric('satisfaction')}
        >
          Satisfacción
        </Button>
        <Button
          variant={selectedMetric === 'treatments' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setSelectedMetric('treatments')}
        >
          Tratamientos
        </Button>
        <Button
          variant={selectedMetric === 'retention' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setSelectedMetric('retention')}
        >
          Retención
        </Button>
        <Button
          variant={selectedMetric === 'journey' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setSelectedMetric('journey')}
        >
          Recorrido
        </Button>
      </div>
      {/* Demographics Analysis */}
      {selectedMetric === 'demographics' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Distribución por Edad</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={demographicsData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                  <XAxis 
                    dataKey="age_group" 
                    stroke="var(--color-muted-foreground)"
                    fontSize={12}
                  />
                  <YAxis 
                    stroke="var(--color-muted-foreground)"
                    fontSize={12}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar 
                    dataKey="count" 
                    name="Pacientes" 
                    fill="var(--color-primary)" 
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Análisis de Tiempo de Espera</h3>
            <div className="space-y-4">
              {waitTimeAnalysis?.map((item, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                  <div>
                    <div className="font-medium text-foreground">{item?.time_range}</div>
                    <div className="text-sm text-muted-foreground">{item?.count} pacientes</div>
                  </div>
                  <div className="text-right">
                    <div className={`flex items-center space-x-1 ${getSatisfactionColor(item?.satisfaction)}`}>
                      <Icon name="Star" size={14} className="fill-current" />
                      <span className="font-medium">{item?.satisfaction}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      {/* Satisfaction Trends */}
      {selectedMetric === 'satisfaction' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Tendencias de Satisfacción</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={satisfactionTrends}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis 
                  dataKey="date" 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                  domain={[3.5, 5]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area 
                  type="monotone" 
                  dataKey="satisfaction" 
                  name="Satisfacción"
                  stroke="var(--color-success)" 
                  fill="var(--color-success)"
                  fillOpacity={0.2}
                  strokeWidth={3}
                />
                <Line 
                  type="monotone" 
                  dataKey="responses" 
                  name="Respuestas"
                  stroke="var(--color-primary)" 
                  strokeWidth={2}
                  dot={{ fill: 'var(--color-primary)', strokeWidth: 2, r: 4 }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
      {/* Treatment Preferences */}
      {selectedMetric === 'treatments' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Preferencias de Tratamiento</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={treatmentPreferences}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={2}
                    dataKey="count"
                  >
                    {treatmentPreferences?.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry?.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value, name) => [`${value} pacientes`, 'Cantidad']}
                    labelFormatter={(label) => `Tratamiento: ${label}`}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Desglose de Tratamientos</h3>
            <div className="space-y-3">
              {treatmentPreferences?.map((treatment, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div 
                      className="w-4 h-4 rounded-full" 
                      style={{ backgroundColor: treatment?.color }}
                    ></div>
                    <span className="text-sm font-medium text-foreground">{treatment?.treatment}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium text-foreground">{treatment?.count}</div>
                    <div className="text-xs text-muted-foreground">{treatment?.percentage}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      {/* Retention Analysis */}
      {selectedMetric === 'retention' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Análisis de Retención de Pacientes</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={retentionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis 
                  dataKey="month" 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Bar 
                  dataKey="new_patients" 
                  name="Pacientes Nuevos" 
                  fill="var(--color-primary)" 
                  radius={[2, 2, 0, 0]}
                />
                <Bar 
                  dataKey="returning" 
                  name="Pacientes Recurrentes" 
                  fill="var(--color-success)" 
                  radius={[2, 2, 0, 0]}
                />
                <Line 
                  type="monotone" 
                  dataKey="retention_rate" 
                  name="Tasa de Retención (%)"
                  stroke="var(--color-warning)" 
                  strokeWidth={3}
                  dot={{ fill: 'var(--color-warning)', strokeWidth: 2, r: 5 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
      {/* Patient Journey */}
      {selectedMetric === 'journey' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Recorrido del Paciente</h3>
          <div className="space-y-4">
            {patientJourney?.map((stage, index) => (
              <div key={index} className="relative">
                <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold text-sm">
                      {index + 1}
                    </div>
                    <div>
                      <div className="font-medium text-foreground">{stage?.stage}</div>
                      <div className="text-sm text-muted-foreground">{stage?.count} pacientes</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-foreground">{stage?.conversion}%</div>
                    <div className="text-xs text-muted-foreground">Conversión</div>
                  </div>
                </div>
                
                {index < patientJourney?.length - 1 && (
                  <div className="flex justify-center py-2">
                    <Icon name="ChevronDown" size={20} className="text-muted-foreground" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientAnalytics;