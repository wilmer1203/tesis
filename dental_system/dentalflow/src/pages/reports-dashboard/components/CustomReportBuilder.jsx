import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const CustomReportBuilder = ({ className = '' }) => {
  const [selectedFields, setSelectedFields] = useState([]);
  const [groupBy, setGroupBy] = useState('');
  const [sortBy, setSortBy] = useState('');
  const [filters, setFilters] = useState([]);
  const [reportName, setReportName] = useState('');
  const [showPreview, setShowPreview] = useState(false);

  const availableFields = [
    { id: 'patient_name', label: 'Nombre del Paciente', category: 'Paciente', type: 'text' },
    { id: 'patient_age', label: 'Edad del Paciente', category: 'Paciente', type: 'number' },
    { id: 'patient_phone', label: 'Teléfono', category: 'Paciente', type: 'text' },
    { id: 'dentist_name', label: 'Dentista', category: 'Personal', type: 'text' },
    { id: 'treatment_type', label: 'Tipo de Tratamiento', category: 'Tratamiento', type: 'text' },
    { id: 'treatment_date', label: 'Fecha de Tratamiento', category: 'Tratamiento', type: 'date' },
    { id: 'treatment_cost_bs', label: 'Costo (BS)', category: 'Financiero', type: 'currency' },
    { id: 'treatment_cost_usd', label: 'Costo (USD)', category: 'Financiero', type: 'currency' },
    { id: 'payment_method', label: 'Método de Pago', category: 'Financiero', type: 'text' },
    { id: 'wait_time', label: 'Tiempo de Espera', category: 'Operacional', type: 'number' },
    { id: 'satisfaction_rating', label: 'Calificación', category: 'Calidad', type: 'number' },
    { id: 'appointment_status', label: 'Estado de Cita', category: 'Operacional', type: 'text' }
  ];

  const groupByOptions = [
    { id: 'dentist_name', label: 'Por Dentista' },
    { id: 'treatment_type', label: 'Por Tipo de Tratamiento' },
    { id: 'payment_method', label: 'Por Método de Pago' },
    { id: 'date', label: 'Por Fecha' },
    { id: 'month', label: 'Por Mes' },
    { id: 'patient_age_group', label: 'Por Grupo de Edad' }
  ];

  const sortOptions = [
    { id: 'treatment_date_desc', label: 'Fecha (Más Reciente)' },
    { id: 'treatment_date_asc', label: 'Fecha (Más Antigua)' },
    { id: 'treatment_cost_desc', label: 'Costo (Mayor a Menor)' },
    { id: 'treatment_cost_asc', label: 'Costo (Menor a Mayor)' },
    { id: 'patient_name_asc', label: 'Nombre Paciente (A-Z)' },
    { id: 'dentist_name_asc', label: 'Nombre Dentista (A-Z)' }
  ];

  const filterOperators = [
    { id: 'equals', label: 'Igual a', types: ['text', 'number', 'date'] },
    { id: 'contains', label: 'Contiene', types: ['text'] },
    { id: 'greater_than', label: 'Mayor que', types: ['number', 'currency', 'date'] },
    { id: 'less_than', label: 'Menor que', types: ['number', 'currency', 'date'] },
    { id: 'between', label: 'Entre', types: ['number', 'currency', 'date'] },
    { id: 'in_list', label: 'En lista', types: ['text'] }
  ];

  const savedReports = [
    { id: 1, name: 'Ingresos Mensuales por Dentista', fields: 5, lastRun: '2024-09-03' },
    { id: 2, name: 'Pacientes por Tratamiento', fields: 4, lastRun: '2024-09-02' },
    { id: 3, name: 'Análisis de Satisfacción', fields: 6, lastRun: '2024-09-01' }
  ];

  const handleFieldToggle = (field) => {
    setSelectedFields(prev => 
      prev?.find(f => f?.id === field?.id)
        ? prev?.filter(f => f?.id !== field?.id)
        : [...prev, field]
    );
  };

  const handleAddFilter = () => {
    setFilters(prev => [...prev, {
      id: Date.now(),
      field: '',
      operator: '',
      value: ''
    }]);
  };

  const handleRemoveFilter = (filterId) => {
    setFilters(prev => prev?.filter(f => f?.id !== filterId));
  };

  const handleFilterChange = (filterId, property, value) => {
    setFilters(prev => prev?.map(f => 
      f?.id === filterId ? { ...f, [property]: value } : f
    ));
  };

  const handleGenerateReport = () => {
    if (selectedFields?.length === 0) {
      alert('Por favor seleccione al menos un campo');
      return;
    }

    const reportConfig = {
      name: reportName || 'Reporte Personalizado',
      fields: selectedFields,
      groupBy,
      sortBy,
      filters,
      timestamp: new Date()?.toISOString()
    };

    console.log('Generando reporte personalizado:', reportConfig);
    setShowPreview(true);
  };

  const handleSaveReport = () => {
    if (!reportName?.trim()) {
      alert('Por favor ingrese un nombre para el reporte');
      return;
    }

    console.log('Guardando reporte:', reportName);
    alert(`Reporte "${reportName}" guardado exitosamente`);
  };

  const getFieldsByCategory = (category) => {
    return availableFields?.filter(field => field?.category === category);
  };

  const categories = [...new Set(availableFields.map(field => field.category))];

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Report Name */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Configuración del Reporte</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Nombre del Reporte
            </label>
            <input
              type="text"
              value={reportName}
              onChange={(e) => setReportName(e?.target?.value)}
              placeholder="Mi Reporte Personalizado"
              className="w-full px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          <div className="flex items-end">
            <Button
              variant="outline"
              onClick={handleSaveReport}
              iconName="Save"
              iconPosition="left"
              className="w-full"
            >
              Guardar Configuración
            </Button>
          </div>
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Field Selection */}
        <div className="lg:col-span-2 bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Seleccionar Campos</h3>
          
          <div className="space-y-4">
            {categories?.map(category => (
              <div key={category}>
                <h4 className="text-sm font-medium text-muted-foreground mb-2">{category}</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {getFieldsByCategory(category)?.map(field => (
                    <label key={field?.id} className="flex items-center space-x-3 p-2 hover:bg-muted rounded-md cursor-pointer">
                      <input
                        type="checkbox"
                        checked={selectedFields?.some(f => f?.id === field?.id)}
                        onChange={() => handleFieldToggle(field)}
                        className="w-4 h-4 text-primary border-border rounded focus:ring-ring"
                      />
                      <span className="text-sm text-foreground">{field?.label}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {selectedFields?.length > 0 && (
            <div className="mt-6 p-4 bg-muted rounded-lg">
              <h4 className="text-sm font-medium text-foreground mb-2">Campos Seleccionados ({selectedFields?.length})</h4>
              <div className="flex flex-wrap gap-2">
                {selectedFields?.map(field => (
                  <span key={field?.id} className="inline-flex items-center space-x-1 px-2 py-1 bg-primary/10 text-primary text-xs rounded-md">
                    <span>{field?.label}</span>
                    <button
                      onClick={() => handleFieldToggle(field)}
                      className="hover:bg-primary/20 rounded-full p-0.5"
                    >
                      <Icon name="X" size={12} />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Configuration Panel */}
        <div className="space-y-6">
          {/* Grouping */}
          <div className="bg-card border border-border rounded-lg p-4">
            <h4 className="text-sm font-semibold text-foreground mb-3">Agrupar Por</h4>
            <select
              value={groupBy}
              onChange={(e) => setGroupBy(e?.target?.value)}
              className="w-full px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="">Sin agrupar</option>
              {groupByOptions?.map(option => (
                <option key={option?.id} value={option?.id}>{option?.label}</option>
              ))}
            </select>
          </div>

          {/* Sorting */}
          <div className="bg-card border border-border rounded-lg p-4">
            <h4 className="text-sm font-semibold text-foreground mb-3">Ordenar Por</h4>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e?.target?.value)}
              className="w-full px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="">Sin ordenar</option>
              {sortOptions?.map(option => (
                <option key={option?.id} value={option?.id}>{option?.label}</option>
              ))}
            </select>
          </div>

          {/* Filters */}
          <div className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-foreground">Filtros</h4>
              <Button
                variant="outline"
                size="sm"
                onClick={handleAddFilter}
                iconName="Plus"
              >
                Agregar
              </Button>
            </div>

            <div className="space-y-3">
              {filters?.map(filter => (
                <div key={filter?.id} className="p-3 bg-muted rounded-md">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-muted-foreground">Filtro</span>
                    <button
                      onClick={() => handleRemoveFilter(filter?.id)}
                      className="p-1 hover:bg-background rounded transition-smooth"
                    >
                      <Icon name="X" size={12} className="text-muted-foreground" />
                    </button>
                  </div>
                  
                  <div className="space-y-2">
                    <select
                      value={filter?.field}
                      onChange={(e) => handleFilterChange(filter?.id, 'field', e?.target?.value)}
                      className="w-full px-2 py-1 text-xs border border-border rounded bg-input text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                    >
                      <option value="">Seleccionar campo</option>
                      {availableFields?.map(field => (
                        <option key={field?.id} value={field?.id}>{field?.label}</option>
                      ))}
                    </select>
                    
                    <select
                      value={filter?.operator}
                      onChange={(e) => handleFilterChange(filter?.id, 'operator', e?.target?.value)}
                      className="w-full px-2 py-1 text-xs border border-border rounded bg-input text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                    >
                      <option value="">Operador</option>
                      {filterOperators?.map(op => (
                        <option key={op?.id} value={op?.id}>{op?.label}</option>
                      ))}
                    </select>
                    
                    <input
                      type="text"
                      value={filter?.value}
                      onChange={(e) => handleFilterChange(filter?.id, 'value', e?.target?.value)}
                      placeholder="Valor"
                      className="w-full px-2 py-1 text-xs border border-border rounded bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                    />
                  </div>
                </div>
              ))}
              
              {filters?.length === 0 && (
                <div className="text-center py-4 text-sm text-muted-foreground">
                  No hay filtros configurados
                </div>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="space-y-3">
            <Button
              variant="default"
              fullWidth
              onClick={handleGenerateReport}
              iconName="Play"
              iconPosition="left"
            >
              Generar Reporte
            </Button>
            <Button
              variant="outline"
              fullWidth
              onClick={() => setShowPreview(true)}
              iconName="Eye"
              iconPosition="left"
            >
              Vista Previa
            </Button>
          </div>
        </div>
      </div>
      {/* Saved Reports */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Reportes Guardados</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {savedReports?.map(report => (
            <div key={report?.id} className="p-4 bg-muted rounded-lg">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-medium text-foreground text-sm">{report?.name}</h4>
                <button className="p-1 hover:bg-background rounded transition-smooth">
                  <Icon name="MoreHorizontal" size={14} className="text-muted-foreground" />
                </button>
              </div>
              <div className="text-xs text-muted-foreground mb-3">
                {report?.fields} campos • Última ejecución: {report?.lastRun}
              </div>
              <div className="flex space-x-2">
                <Button variant="outline" size="sm" className="flex-1">
                  Cargar
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  Ejecutar
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
      {/* Preview Modal */}
      {showPreview && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-popover border border-border rounded-lg p-6 w-full max-w-4xl mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-foreground">Vista Previa del Reporte</h3>
              <button
                onClick={() => setShowPreview(false)}
                className="p-1 hover:bg-muted rounded transition-smooth"
              >
                <Icon name="X" size={16} className="text-muted-foreground" />
              </button>
            </div>

            <div className="space-y-4">
              <div className="text-sm text-muted-foreground">
                Mostrando vista previa con datos de muestra
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border">
                      {selectedFields?.map(field => (
                        <th key={field?.id} className="text-left py-2 px-3 font-medium text-muted-foreground">
                          {field?.label}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {[1, 2, 3, 4, 5]?.map(row => (
                      <tr key={row} className="border-b border-border">
                        {selectedFields?.map(field => (
                          <td key={field?.id} className="py-2 px-3 text-foreground">
                            {field?.type === 'currency' ? '$150.00' : 
                             field?.type === 'date' ? '04/09/2024' :
                             field?.type === 'number' ? '25' :
                             `Dato ${row}`}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <Button
                variant="outline"
                onClick={() => setShowPreview(false)}
              >
                Cerrar
              </Button>
              <Button
                variant="default"
                onClick={handleGenerateReport}
              >
                Generar Reporte Final
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomReportBuilder;