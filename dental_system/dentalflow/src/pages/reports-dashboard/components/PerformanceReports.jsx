import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const PerformanceReports = ({ dateRange, className = '' }) => {
  const [selectedView, setSelectedView] = useState('productivity');
  const [selectedDentist, setSelectedDentist] = useState('all');

  // Mock performance data
  const productivityData = [
    { date: '01/09', maria: 8, carlos: 7, ana: 6, luis: 5 },
    { date: '02/09', maria: 9, carlos: 8, ana: 7, luis: 6 },
    { date: '03/09', maria: 7, carlos: 9, ana: 8, luis: 7 },
    { date: '04/09', maria: 10, carlos: 8, ana: 6, luis: 8 }
  ];

  const efficiencyData = [
    { dentist: 'Dr. María González', avg_time: 45, satisfaction: 4.8, completion_rate: 98, revenue_per_hour: 285000 },
    { dentist: 'Dr. Carlos Mendoza', avg_time: 52, satisfaction: 4.6, completion_rate: 95, revenue_per_hour: 265000 },
    { dentist: 'Dr. Ana Rodríguez', avg_time: 48, satisfaction: 4.7, completion_rate: 97, revenue_per_hour: 275000 },
    { dentist: 'Dr. Luis Herrera', avg_time: 55, satisfaction: 4.5, completion_rate: 93, revenue_per_hour: 245000 }
  ];

  const skillsRadarData = [
    { skill: 'Endodoncia', maria: 95, carlos: 88, ana: 92, luis: 85 },
    { skill: 'Ortodoncia', maria: 85, carlos: 92, ana: 88, luis: 90 },
    { skill: 'Cirugía', maria: 90, carlos: 95, ana: 85, luis: 88 },
    { skill: 'Estética', maria: 92, carlos: 85, ana: 95, luis: 82 },
    { skill: 'Periodoncia', maria: 88, carlos: 90, ana: 92, luis: 95 },
    { skill: 'Implantes', maria: 87, carlos: 93, ana: 85, luis: 90 }
  ];

  const treatmentSuccessData = [
    { treatment: 'Limpieza', success_rate: 99, avg_time: 30, patient_satisfaction: 4.9 },
    { treatment: 'Empaste', success_rate: 97, avg_time: 45, patient_satisfaction: 4.7 },
    { treatment: 'Endodoncia', success_rate: 94, avg_time: 90, patient_satisfaction: 4.5 },
    { treatment: 'Extracción', success_rate: 98, avg_time: 25, patient_satisfaction: 4.3 },
    { treatment: 'Corona', success_rate: 96, avg_time: 120, patient_satisfaction: 4.8 },
    { treatment: 'Implante', success_rate: 95, avg_time: 150, patient_satisfaction: 4.6 }
  ];

  const kpiCards = [
    {
      title: 'Productividad Promedio',
      value: '7.5',
      unit: 'pacientes/día',
      change: '+8.2%',
      trend: 'up',
      icon: 'Users',
      color: 'text-success'
    },
    {
      title: 'Tiempo Promedio',
      value: '50',
      unit: 'minutos',
      change: '-5.1%',
      trend: 'down',
      icon: 'Clock',
      color: 'text-success'
    },
    {
      title: 'Satisfacción',
      value: '4.65',
      unit: '/5.0',
      change: '+0.15',
      trend: 'up',
      icon: 'Star',
      color: 'text-success'
    },
    {
      title: 'Tasa de Éxito',
      value: '96.5%',
      unit: '',
      change: '+1.2%',
      trend: 'up',
      icon: 'CheckCircle',
      color: 'text-success'
    }
  ];

  const dentistOptions = [
    { value: 'all', label: 'Todos los Dentistas' },
    { value: 'maria', label: 'Dr. María González' },
    { value: 'carlos', label: 'Dr. Carlos Mendoza' },
    { value: 'ana', label: 'Dr. Ana Rodríguez' },
    { value: 'luis', label: 'Dr. Luis Herrera' }
  ];

  const getPerformanceColor = (value, type) => {
    switch (type) {
      case 'satisfaction':
        return value >= 4.5 ? 'text-success' : value >= 4.0 ? 'text-warning' : 'text-error';
      case 'completion':
        return value >= 95 ? 'text-success' : value >= 90 ? 'text-warning' : 'text-error';
      case 'time':
        return value <= 45 ? 'text-success' : value <= 60 ? 'text-warning' : 'text-error';
      default:
        return 'text-foreground';
    }
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload?.length) {
      return (
        <div className="bg-popover border border-border rounded-md shadow-modal p-3">
          <p className="text-sm font-medium text-foreground mb-2">{label}</p>
          {payload?.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry?.color }}>
              {entry?.name}: {entry?.value}
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
        {kpiCards?.map((card, index) => (
          <div key={index} className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Icon name={card?.icon} size={20} className="text-primary" />
              <div className={`flex items-center space-x-1 text-xs ${card?.color}`}>
                <Icon name={card?.trend === 'up' ? 'ArrowUp' : 'ArrowDown'} size={12} />
                <span>{card?.change}</span>
              </div>
            </div>
            <div className="text-2xl font-bold text-foreground mb-1">
              {card?.value}
              <span className="text-sm font-normal text-muted-foreground ml-1">{card?.unit}</span>
            </div>
            <div className="text-sm text-muted-foreground">{card?.title}</div>
          </div>
        ))}
      </div>
      {/* View Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex flex-wrap gap-2">
          <Button
            variant={selectedView === 'productivity' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('productivity')}
          >
            Productividad
          </Button>
          <Button
            variant={selectedView === 'efficiency' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('efficiency')}
          >
            Eficiencia
          </Button>
          <Button
            variant={selectedView === 'skills' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('skills')}
          >
            Habilidades
          </Button>
          <Button
            variant={selectedView === 'treatments' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedView('treatments')}
          >
            Tratamientos
          </Button>
        </div>

        <select
          value={selectedDentist}
          onChange={(e) => setSelectedDentist(e?.target?.value)}
          className="px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        >
          {dentistOptions?.map((option) => (
            <option key={option?.value} value={option?.value}>
              {option?.label}
            </option>
          ))}
        </select>
      </div>
      {/* Productivity Chart */}
      {selectedView === 'productivity' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Productividad Diaria (Pacientes Atendidos)</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={productivityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis 
                  dataKey="date" 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Bar dataKey="maria" name="Dr. María" fill="#2563EB" radius={[2, 2, 0, 0]} />
                <Bar dataKey="carlos" name="Dr. Carlos" fill="#059669" radius={[2, 2, 0, 0]} />
                <Bar dataKey="ana" name="Dr. Ana" fill="#F59E0B" radius={[2, 2, 0, 0]} />
                <Bar dataKey="luis" name="Dr. Luis" fill="#EF4444" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
      {/* Efficiency Table */}
      {selectedView === 'efficiency' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Métricas de Eficiencia</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Dentista</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Tiempo Promedio</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Satisfacción</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Tasa Completación</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Ingresos/Hora</th>
                </tr>
              </thead>
              <tbody>
                {efficiencyData?.map((dentist, index) => (
                  <tr key={index} className="border-b border-border last:border-b-0 hover:bg-muted/50">
                    <td className="py-3 px-4">
                      <div className="font-medium text-foreground">{dentist?.dentist}</div>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className={`font-medium ${getPerformanceColor(dentist?.avg_time, 'time')}`}>
                        {dentist?.avg_time} min
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <div className="flex items-center justify-center space-x-1">
                        <Icon name="Star" size={14} className="text-warning fill-current" />
                        <span className={`font-medium ${getPerformanceColor(dentist?.satisfaction, 'satisfaction')}`}>
                          {dentist?.satisfaction}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className={`font-medium ${getPerformanceColor(dentist?.completion_rate, 'completion')}`}>
                        {dentist?.completion_rate}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right font-medium text-foreground">
                      {dentist?.revenue_per_hour?.toLocaleString('es-VE')} Bs
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {/* Skills Radar Chart */}
      {selectedView === 'skills' && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Análisis de Habilidades por Especialidad</h3>
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={skillsRadarData}>
                <PolarGrid stroke="var(--color-border)" />
                <PolarAngleAxis 
                  dataKey="skill" 
                  tick={{ fontSize: 12, fill: 'var(--color-muted-foreground)' }}
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 100]}
                  tick={{ fontSize: 10, fill: 'var(--color-muted-foreground)' }}
                />
                <Radar name="Dr. María" dataKey="maria" stroke="#2563EB" fill="#2563EB" fillOpacity={0.1} strokeWidth={2} />
                <Radar name="Dr. Carlos" dataKey="carlos" stroke="#059669" fill="#059669" fillOpacity={0.1} strokeWidth={2} />
                <Radar name="Dr. Ana" dataKey="ana" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.1} strokeWidth={2} />
                <Radar name="Dr. Luis" dataKey="luis" stroke="#EF4444" fill="#EF4444" fillOpacity={0.1} strokeWidth={2} />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
      {/* Treatment Success Analysis */}
      {selectedView === 'treatments' && (
        <div className="space-y-6">
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Análisis de Tratamientos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {treatmentSuccessData?.map((treatment, index) => (
                <div key={index} className="bg-muted rounded-lg p-4">
                  <div className="text-lg font-semibold text-foreground mb-2">{treatment?.treatment}</div>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Tasa de Éxito:</span>
                      <span className={`text-sm font-medium ${getPerformanceColor(treatment?.success_rate, 'completion')}`}>
                        {treatment?.success_rate}%
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Tiempo Promedio:</span>
                      <span className="text-sm font-medium text-foreground">{treatment?.avg_time} min</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Satisfacción:</span>
                      <div className="flex items-center space-x-1">
                        <Icon name="Star" size={12} className="text-warning fill-current" />
                        <span className={`text-sm font-medium ${getPerformanceColor(treatment?.patient_satisfaction, 'satisfaction')}`}>
                          {treatment?.patient_satisfaction}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PerformanceReports;