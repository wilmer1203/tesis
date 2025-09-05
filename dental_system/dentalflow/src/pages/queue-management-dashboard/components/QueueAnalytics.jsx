import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const QueueAnalytics = ({ isExpanded, onToggle }) => {
  const [activeTab, setActiveTab] = useState('waitTimes');

  // Mock analytics data
  const waitTimeData = [
    { time: '09:00', promedio: 15, maximo: 25 },
    { time: '10:00', promedio: 22, maximo: 35 },
    { time: '11:00', promedio: 18, maximo: 30 },
    { time: '12:00', promedio: 28, maximo: 45 },
    { time: '13:00', promedio: 12, maximo: 20 },
    { time: '14:00', promedio: 25, maximo: 40 },
    { time: '15:00', promedio: 20, maximo: 32 }
  ];

  const dentistWorkloadData = [
    { name: 'Dr. García', pacientes: 12, tiempoPromedio: 25, eficiencia: 85 },
    { name: 'Dra. López', pacientes: 8, tiempoPromedio: 30, eficiencia: 78 },
    { name: 'Dr. Martínez', pacientes: 15, tiempoPromedio: 20, eficiencia: 92 },
    { name: 'Dra. Rodríguez', pacientes: 10, tiempoPromedio: 28, eficiencia: 80 }
  ];

  const serviceDistributionData = [
    { name: 'Limpieza', value: 35, color: '#2563EB' },
    { name: 'Consulta', value: 25, color: '#059669' },
    { name: 'Tratamiento', value: 20, color: '#F59E0B' },
    { name: 'Emergencia', value: 15, color: '#EF4444' },
    { name: 'Otros', value: 5, color: '#64748B' }
  ];

  const tabs = [
    { id: 'waitTimes', label: 'Tiempos de Espera', icon: 'Clock' },
    { id: 'workload', label: 'Carga de Trabajo', icon: 'BarChart3' },
    { id: 'services', label: 'Distribución de Servicios', icon: 'PieChart' }
  ];

  const renderWaitTimesChart = () => (
    <div className="space-y-4">
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={waitTimeData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="time" stroke="#64748B" fontSize={12} />
            <YAxis stroke="#64748B" fontSize={12} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#FFFFFF', 
                border: '1px solid #E2E8F0',
                borderRadius: '6px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="promedio" 
              stroke="#2563EB" 
              strokeWidth={2}
              name="Promedio (min)"
            />
            <Line 
              type="monotone" 
              dataKey="maximo" 
              stroke="#EF4444" 
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Máximo (min)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-lg font-semibold text-foreground">22m</div>
          <div className="text-xs text-muted-foreground">Promedio Hoy</div>
        </div>
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-lg font-semibold text-warning">45m</div>
          <div className="text-xs text-muted-foreground">Máximo Hoy</div>
        </div>
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-lg font-semibold text-success">15m</div>
          <div className="text-xs text-muted-foreground">Mínimo Hoy</div>
        </div>
      </div>
    </div>
  );

  const renderWorkloadChart = () => (
    <div className="space-y-4">
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={dentistWorkloadData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="name" stroke="#64748B" fontSize={12} />
            <YAxis stroke="#64748B" fontSize={12} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#FFFFFF', 
                border: '1px solid #E2E8F0',
                borderRadius: '6px'
              }}
            />
            <Bar dataKey="pacientes" fill="#2563EB" name="Pacientes" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="space-y-2">
        {dentistWorkloadData?.map((dentist, index) => (
          <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-md">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                <Icon name="User" size={16} className="text-primary" />
              </div>
              <span className="font-medium text-foreground">{dentist?.name}</span>
            </div>
            <div className="flex items-center space-x-4 text-sm">
              <span className="text-muted-foreground">{dentist?.pacientes} pacientes</span>
              <span className="text-muted-foreground">{dentist?.tiempoPromedio}m promedio</span>
              <span className={`font-medium ${
                dentist?.eficiencia >= 85 ? 'text-success' : 
                dentist?.eficiencia >= 75 ? 'text-warning' : 'text-error'
              }`}>
                {dentist?.eficiencia}% eficiencia
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderServicesChart = () => (
    <div className="space-y-4">
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={serviceDistributionData}
              cx="50%"
              cy="50%"
              outerRadius={80}
              dataKey="value"
              label={({ name, value }) => `${name}: ${value}%`}
            >
              {serviceDistributionData?.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry?.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      
      <div className="grid grid-cols-2 gap-2">
        {serviceDistributionData?.map((service, index) => (
          <div key={index} className="flex items-center space-x-2 p-2 bg-muted rounded-md">
            <div 
              className="w-3 h-3 rounded-full" 
              style={{ backgroundColor: service?.color }}
            ></div>
            <span className="text-sm text-foreground">{service?.name}</span>
            <span className="text-sm font-medium text-foreground ml-auto">{service?.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );

  if (!isExpanded) {
    return (
      <div className="bg-card border border-border rounded-lg shadow-soft p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Icon name="BarChart3" size={20} className="text-primary" />
            <span className="font-medium text-foreground">Análisis de Cola</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            iconName="ChevronDown"
            onClick={onToggle}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="BarChart3" size={20} className="text-primary" />
          <span className="font-medium text-foreground">Análisis de Cola</span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          iconName="ChevronUp"
          onClick={onToggle}
        />
      </div>
      {/* Tabs */}
      <div className="border-b border-border">
        <div className="flex space-x-1 p-4">
          {tabs?.map((tab) => (
            <button
              key={tab?.id}
              onClick={() => setActiveTab(tab?.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-smooth ${
                activeTab === tab?.id
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              }`}
            >
              <Icon name={tab?.icon} size={16} />
              <span>{tab?.label}</span>
            </button>
          ))}
        </div>
      </div>
      {/* Content */}
      <div className="p-4">
        {activeTab === 'waitTimes' && renderWaitTimesChart()}
        {activeTab === 'workload' && renderWorkloadChart()}
        {activeTab === 'services' && renderServicesChart()}
      </div>
    </div>
  );
};

export default QueueAnalytics;