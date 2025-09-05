import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const PaymentFilters = ({ onFiltersChange, activeFilters }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [filters, setFilters] = useState({
    dateRange: activeFilters?.dateRange || 'today',
    paymentMethod: activeFilters?.paymentMethod || 'all',
    status: activeFilters?.status || 'all',
    amountRange: activeFilters?.amountRange || 'all',
    insuranceType: activeFilters?.insuranceType || 'all',
    searchTerm: activeFilters?.searchTerm || ''
  });

  const dateRangeOptions = [
    { value: 'today', label: 'Hoy' },
    { value: 'week', label: 'Esta semana' },
    { value: 'month', label: 'Este mes' },
    { value: 'quarter', label: 'Este trimestre' },
    { value: 'year', label: 'Este año' },
    { value: 'custom', label: 'Rango personalizado' }
  ];

  const paymentMethodOptions = [
    { value: 'all', label: 'Todos los métodos' },
    { value: 'cash', label: 'Efectivo' },
    { value: 'card', label: 'Tarjeta' },
    { value: 'transfer', label: 'Transferencia' },
    { value: 'insurance', label: 'Seguro médico' },
    { value: 'plan', label: 'Plan de pagos' }
  ];

  const statusOptions = [
    { value: 'all', label: 'Todos los estados' },
    { value: 'pending', label: 'Pendiente' },
    { value: 'partial', label: 'Pago parcial' },
    { value: 'completed', label: 'Completado' },
    { value: 'overdue', label: 'Vencido' },
    { value: 'cancelled', label: 'Cancelado' }
  ];

  const amountRangeOptions = [
    { value: 'all', label: 'Todos los montos' },
    { value: '0-50', label: '0€ - 50€' },
    { value: '51-100', label: '51€ - 100€' },
    { value: '101-200', label: '101€ - 200€' },
    { value: '201-500', label: '201€ - 500€' },
    { value: '500+', label: 'Más de 500€' }
  ];

  const insuranceTypeOptions = [
    { value: 'all', label: 'Todos los seguros' },
    { value: 'public', label: 'Seguridad Social' },
    { value: 'private', label: 'Seguro privado' },
    { value: 'mutual', label: 'Mutua' },
    { value: 'none', label: 'Sin seguro' }
  ];

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const clearAllFilters = () => {
    const clearedFilters = {
      dateRange: 'today',
      paymentMethod: 'all',
      status: 'all',
      amountRange: 'all',
      insuranceType: 'all',
      searchTerm: ''
    };
    setFilters(clearedFilters);
    onFiltersChange(clearedFilters);
  };

  const getActiveFilterCount = () => {
    let count = 0;
    if (filters?.dateRange !== 'today') count++;
    if (filters?.paymentMethod !== 'all') count++;
    if (filters?.status !== 'all') count++;
    if (filters?.amountRange !== 'all') count++;
    if (filters?.insuranceType !== 'all') count++;
    if (filters?.searchTerm) count++;
    return count;
  };

  return (
    <div className="bg-surface border border-border rounded-lg p-4 mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <Icon name="Filter" size={20} color="var(--color-primary)" />
          <h3 className="text-lg font-semibold text-foreground">Filtros de Pagos</h3>
          {getActiveFilterCount() > 0 && (
            <span className="bg-primary text-primary-foreground px-2 py-1 rounded-full text-xs font-medium">
              {getActiveFilterCount()}
            </span>
          )}
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            onClick={clearAllFilters}
            iconName="X"
            iconPosition="left"
            iconSize={16}
            className="text-sm"
          >
            Limpiar
          </Button>
          <Button
            variant="ghost"
            onClick={() => setIsExpanded(!isExpanded)}
            iconName={isExpanded ? "ChevronUp" : "ChevronDown"}
            iconPosition="right"
            iconSize={16}
            className="text-sm"
          >
            {isExpanded ? 'Contraer' : 'Expandir'}
          </Button>
        </div>
      </div>
      {/* Quick Filters */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        <Input
          type="search"
          placeholder="Buscar paciente o servicio..."
          value={filters?.searchTerm}
          onChange={(e) => handleFilterChange('searchTerm', e?.target?.value)}
          className="w-full"
        />
        
        <Select
          options={dateRangeOptions}
          value={filters?.dateRange}
          onChange={(value) => handleFilterChange('dateRange', value)}
          placeholder="Rango de fechas"
        />

        <Select
          options={statusOptions}
          value={filters?.status}
          onChange={(value) => handleFilterChange('status', value)}
          placeholder="Estado del pago"
        />

        <Select
          options={paymentMethodOptions}
          value={filters?.paymentMethod}
          onChange={(value) => handleFilterChange('paymentMethod', value)}
          placeholder="Método de pago"
        />
      </div>
      {/* Advanced Filters */}
      {isExpanded && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-4 border-t border-border">
          <Select
            options={amountRangeOptions}
            value={filters?.amountRange}
            onChange={(value) => handleFilterChange('amountRange', value)}
            placeholder="Rango de monto"
          />

          <Select
            options={insuranceTypeOptions}
            value={filters?.insuranceType}
            onChange={(value) => handleFilterChange('insuranceType', value)}
            placeholder="Tipo de seguro"
          />

          {filters?.dateRange === 'custom' && (
            <div className="flex space-x-2">
              <Input
                type="date"
                placeholder="Fecha inicio"
                className="flex-1"
              />
              <Input
                type="date"
                placeholder="Fecha fin"
                className="flex-1"
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PaymentFilters;