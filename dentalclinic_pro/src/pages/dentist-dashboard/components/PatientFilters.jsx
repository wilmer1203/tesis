import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const PatientFilters = ({ 
  filters, 
  onFiltersChange, 
  onClearFilters,
  totalPatients = 0,
  filteredCount = 0 
}) => {
  const urgencyOptions = [
    { value: '', label: 'Todas las urgencias' },
    { value: 'alta', label: 'Urgente' },
    { value: 'media', label: 'Media' },
    { value: 'baja', label: 'Baja' }
  ];

  const statusOptions = [
    { value: '', label: 'Todos los estados' },
    { value: 'en_tratamiento', label: 'En Tratamiento' },
    { value: 'pendiente', label: 'Pendiente' },
    { value: 'completado', label: 'Completado' },
    { value: 'cancelado', label: 'Cancelado' }
  ];

  const dateRangeOptions = [
    { value: '', label: 'Todas las fechas' },
    { value: 'today', label: 'Hoy' },
    { value: 'tomorrow', label: 'Mañana' },
    { value: 'this_week', label: 'Esta semana' },
    { value: 'next_week', label: 'Próxima semana' },
    { value: 'this_month', label: 'Este mes' }
  ];

  const handleFilterChange = (key, value) => {
    onFiltersChange({
      ...filters,
      [key]: value
    });
  };

  const hasActiveFilters = Object.values(filters)?.some(value => value !== '');

  return (
    <div className="bg-card border border-border rounded-lg p-4 mb-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <Icon name="Filter" size={18} color="var(--color-primary)" />
          <h3 className="text-sm font-semibold text-card-foreground">
            Filtros de Pacientes
          </h3>
        </div>
        
        <div className="flex items-center space-x-3">
          <span className="text-xs text-muted-foreground">
            {filteredCount} de {totalPatients} pacientes
          </span>
          {hasActiveFilters && (
            <Button
              variant="ghost"
              size="xs"
              iconName="X"
              iconPosition="left"
              iconSize={12}
              onClick={onClearFilters}
            >
              Limpiar
            </Button>
          )}
        </div>
      </div>
      {/* Search Input */}
      <div className="mb-4">
        <Input
          type="search"
          placeholder="Buscar por nombre, ID o teléfono..."
          value={filters?.search || ''}
          onChange={(e) => handleFilterChange('search', e?.target?.value)}
          className="w-full"
        />
      </div>
      {/* Filter Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Date Range Filter */}
        <div>
          <Select
            label="Próxima Cita"
            options={dateRangeOptions}
            value={filters?.dateRange || ''}
            onChange={(value) => handleFilterChange('dateRange', value)}
            placeholder="Seleccionar rango"
          />
        </div>

        {/* Urgency Filter */}
        <div>
          <Select
            label="Nivel de Urgencia"
            options={urgencyOptions}
            value={filters?.urgency || ''}
            onChange={(value) => handleFilterChange('urgency', value)}
            placeholder="Seleccionar urgencia"
          />
        </div>

        {/* Status Filter */}
        <div>
          <Select
            label="Estado del Tratamiento"
            options={statusOptions}
            value={filters?.status || ''}
            onChange={(value) => handleFilterChange('status', value)}
            placeholder="Seleccionar estado"
          />
        </div>
      </div>
      {/* Quick Filter Buttons */}
      <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-border">
        <Button
          variant={filters?.quickFilter === 'urgent' ? 'default' : 'outline'}
          size="xs"
          iconName="AlertTriangle"
          iconPosition="left"
          iconSize={12}
          onClick={() => handleFilterChange('quickFilter', 
            filters?.quickFilter === 'urgent' ? '' : 'urgent')}
        >
          Urgentes
        </Button>
        
        <Button
          variant={filters?.quickFilter === 'today' ? 'default' : 'outline'}
          size="xs"
          iconName="Calendar"
          iconPosition="left"
          iconSize={12}
          onClick={() => handleFilterChange('quickFilter', 
            filters?.quickFilter === 'today' ? '' : 'today')}
        >
          Citas Hoy
        </Button>
        
        <Button
          variant={filters?.quickFilter === 'medical_conditions' ? 'default' : 'outline'}
          size="xs"
          iconName="Heart"
          iconPosition="left"
          iconSize={12}
          onClick={() => handleFilterChange('quickFilter', 
            filters?.quickFilter === 'medical_conditions' ? '' : 'medical_conditions')}
        >
          Condiciones Médicas
        </Button>
        
        <Button
          variant={filters?.quickFilter === 'allergies' ? 'default' : 'outline'}
          size="xs"
          iconName="Shield"
          iconPosition="left"
          iconSize={12}
          onClick={() => handleFilterChange('quickFilter', 
            filters?.quickFilter === 'allergies' ? '' : 'allergies')}
        >
          Alergias
        </Button>
      </div>
    </div>
  );
};

export default PatientFilters;