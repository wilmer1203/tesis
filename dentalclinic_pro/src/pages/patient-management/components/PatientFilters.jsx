import React from 'react';
import Icon from '../../../components/AppIcon';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';

const PatientFilters = ({ 
  searchTerm, 
  onSearchChange, 
  filters, 
  onFilterChange, 
  onClearFilters 
}) => {
  const insuranceOptions = [
    { value: 'all', label: 'Todos los seguros' },
    { value: 'sanitas', label: 'Sanitas' },
    { value: 'mapfre', label: 'MAPFRE' },
    { value: 'adeslas', label: 'Adeslas' },
    { value: 'dkv', label: 'DKV' },
    { value: 'asisa', label: 'ASISA' },
    { value: 'none', label: 'Sin seguro' }
  ];

  const statusOptions = [
    { value: 'all', label: 'Todos los estados' },
    { value: 'active', label: 'Activo' },
    { value: 'scheduled', label: 'Programado' },
    { value: 'overdue', label: 'Vencido' },
    { value: 'inactive', label: 'Inactivo' }
  ];

  const dentistOptions = [
    { value: 'all', label: 'Todos los dentistas' },
    { value: 'dr-martinez', label: 'Dr. Martínez' },
    { value: 'dra-lopez', label: 'Dra. López' },
    { value: 'dr-garcia', label: 'Dr. García' },
    { value: 'dra-rodriguez', label: 'Dra. Rodríguez' },
    { value: 'unassigned', label: 'Sin asignar' }
  ];

  const visitDateOptions = [
    { value: 'all', label: 'Cualquier fecha' },
    { value: 'last-week', label: 'Última semana' },
    { value: 'last-month', label: 'Último mes' },
    { value: 'last-3-months', label: 'Últimos 3 meses' },
    { value: 'last-6-months', label: 'Últimos 6 meses' },
    { value: 'over-6-months', label: 'Más de 6 meses' }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-foreground flex items-center space-x-2">
          <Icon name="Filter" size={16} />
          <span>Filtros de Búsqueda</span>
        </h3>
        <Button
          variant="ghost"
          onClick={onClearFilters}
          className="text-xs px-2 py-1"
        >
          Limpiar
        </Button>
      </div>
      <div className="space-y-3">
        <Input
          type="search"
          placeholder="Buscar por nombre, teléfono o email..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e?.target?.value)}
          className="w-full"
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Select
            placeholder="Estado del paciente"
            options={statusOptions}
            value={filters?.status}
            onChange={(value) => onFilterChange('status', value)}
          />

          <Select
            placeholder="Seguro médico"
            options={insuranceOptions}
            value={filters?.insurance}
            onChange={(value) => onFilterChange('insurance', value)}
          />

          <Select
            placeholder="Dentista asignado"
            options={dentistOptions}
            value={filters?.dentist}
            onChange={(value) => onFilterChange('dentist', value)}
          />

          <Select
            placeholder="Última visita"
            options={visitDateOptions}
            value={filters?.lastVisit}
            onChange={(value) => onFilterChange('lastVisit', value)}
          />
        </div>
      </div>
    </div>
  );
};

export default PatientFilters;