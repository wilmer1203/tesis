import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Select from '../../../components/ui/Select';

const QueueControlBar = ({ 
  queueStats, 
  onEmergencyAdd, 
  onGlobalAction, 
  onFilterChange,
  onViewChange 
}) => {
  const [currentView, setCurrentView] = useState('columns');
  const [selectedFilter, setSelectedFilter] = useState('all');

  const viewOptions = [
    { value: 'columns', label: 'Vista por Columnas' },
    { value: 'list', label: 'Vista de Lista' },
    { value: 'timeline', label: 'Vista Cronológica' }
  ];

  const filterOptions = [
    { value: 'all', label: 'Todos los Pacientes' },
    { value: 'urgent', label: 'Solo Urgentes' },
    { value: 'waiting', label: 'En Espera' },
    { value: 'overdue', label: 'Tiempo Excedido' }
  ];

  const handleViewChange = (value) => {
    setCurrentView(value);
    onViewChange(value);
  };

  const handleFilterChange = (value) => {
    setSelectedFilter(value);
    onFilterChange(value);
  };

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft p-4 mb-6">
      {/* Top Row - Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-4">
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-2xl font-bold text-foreground">{queueStats?.totalPatients}</div>
          <div className="text-xs text-muted-foreground">Total Pacientes</div>
        </div>
        
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-2xl font-bold text-warning">{queueStats?.urgentPatients}</div>
          <div className="text-xs text-muted-foreground">Urgentes</div>
        </div>
        
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-2xl font-bold text-success">{queueStats?.activeDentists}</div>
          <div className="text-xs text-muted-foreground">Dentistas Activos</div>
        </div>
        
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-2xl font-bold text-foreground">{queueStats?.averageWaitTime}m</div>
          <div className="text-xs text-muted-foreground">Espera Promedio</div>
        </div>
        
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-2xl font-bold text-primary">{queueStats?.capacityUsed}%</div>
          <div className="text-xs text-muted-foreground">Capacidad</div>
        </div>
        
        <div className="bg-muted rounded-md p-3 text-center">
          <div className="text-2xl font-bold text-foreground">{queueStats?.completedToday}</div>
          <div className="text-xs text-muted-foreground">Completados Hoy</div>
        </div>
      </div>
      {/* Bottom Row - Controls */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between space-y-4 lg:space-y-0 lg:space-x-4">
        {/* Left Side - Emergency and Actions */}
        <div className="flex flex-wrap items-center space-x-3">
          <Button
            variant="destructive"
            iconName="AlertTriangle"
            iconPosition="left"
            onClick={onEmergencyAdd}
          >
            Paciente Urgente
          </Button>
          
          <Button
            variant="outline"
            iconName="UserPlus"
            iconPosition="left"
            onClick={() => onGlobalAction('addPatient')}
          >
            Agregar Paciente
          </Button>
          
          <Button
            variant="ghost"
            iconName="RefreshCw"
            onClick={() => onGlobalAction('refresh')}
            className="px-3"
          />
        </div>

        {/* Right Side - View and Filter Controls */}
        <div className="flex flex-wrap items-center space-x-3">
          <div className="flex items-center space-x-2">
            <Icon name="Filter" size={16} className="text-muted-foreground" />
            <Select
              options={filterOptions}
              value={selectedFilter}
              onChange={handleFilterChange}
              className="w-48"
            />
          </div>
          
          <div className="flex items-center space-x-2">
            <Icon name="Layout" size={16} className="text-muted-foreground" />
            <Select
              options={viewOptions}
              value={currentView}
              onChange={handleViewChange}
              className="w-48"
            />
          </div>
          
          <Button
            variant="outline"
            iconName="Settings"
            onClick={() => onGlobalAction('settings')}
            className="px-3"
          />
        </div>
      </div>
      {/* Alert Bar for Critical Situations */}
      {queueStats?.urgentPatients > 5 && (
        <div className="mt-4 bg-error/10 border border-error/20 rounded-md p-3">
          <div className="flex items-center space-x-2">
            <Icon name="AlertTriangle" size={16} className="text-error" />
            <span className="text-sm font-medium text-error">
              Atención: {queueStats?.urgentPatients} pacientes urgentes en cola
            </span>
            <Button
              variant="destructive"
              size="sm"
              onClick={() => onGlobalAction('handleUrgent')}
              className="ml-auto"
            >
              Gestionar Urgencias
            </Button>
          </div>
        </div>
      )}
      {/* Capacity Warning */}
      {queueStats?.capacityUsed > 90 && (
        <div className="mt-2 bg-warning/10 border border-warning/20 rounded-md p-3">
          <div className="flex items-center space-x-2">
            <Icon name="AlertCircle" size={16} className="text-warning" />
            <span className="text-sm font-medium text-warning">
              Capacidad al {queueStats?.capacityUsed}% - Considere redistribuir pacientes
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onGlobalAction('redistribute')}
              className="ml-auto"
            >
              Redistribuir
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default QueueControlBar;