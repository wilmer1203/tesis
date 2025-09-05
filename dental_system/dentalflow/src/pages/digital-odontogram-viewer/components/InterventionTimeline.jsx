import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const InterventionTimeline = ({ 
  selectedTooth, 
  onInterventionClick,
  className = '' 
}) => {
  const [filterDentist, setFilterDentist] = useState('all');
  const [filterProcedure, setFilterProcedure] = useState('all');
  const [dateRange, setDateRange] = useState('all');

  // Mock interventions data
  const allInterventions = [
    {
      id: 1,
      date: '2024-09-04',
      time: '10:30',
      tooth: 12,
      dentist: 'Dr. María González',
      procedure: 'Diagnóstico',
      cost: { bs: 80000, usd: 2.19 },
      status: 'completed',
      notes: 'Caries detectada en superficie oclusal',
      changes: ['Diagnóstico de caries']
    },
    {
      id: 2,
      date: '2024-09-03',
      time: '14:15',
      tooth: 16,
      dentist: 'Dr. Carlos Mendoza',
      procedure: 'Control Post-Endodoncia',
      cost: { bs: 120000, usd: 3.29 },
      status: 'completed',
      notes: 'Evolución favorable, sin dolor',
      changes: ['Actualización de estado']
    },
    {
      id: 3,
      date: '2024-09-02',
      time: '09:00',
      tooth: 23,
      dentist: 'Dr. Ana Rodríguez',
      procedure: 'Obturación con Resina',
      cost: { bs: 250000, usd: 6.85 },
      status: 'completed',
      notes: 'Obturación completada, oclusión ajustada',
      changes: ['Diente obturado', 'Estado cambiado a sano']
    },
    {
      id: 4,
      date: '2024-09-01',
      time: '16:45',
      tooth: 36,
      dentist: 'Dr. María González',
      procedure: 'Limpieza Dental',
      cost: { bs: 150000, usd: 4.11 },
      status: 'completed',
      notes: 'Limpieza profunda, eliminación de sarro',
      changes: ['Limpieza completada']
    },
    {
      id: 5,
      date: '2024-08-30',
      time: '11:20',
      tooth: 47,
      dentist: 'Dr. Carlos Mendoza',
      procedure: 'Extracción',
      cost: { bs: 300000, usd: 8.22 },
      status: 'completed',
      notes: 'Extracción simple, sin complicaciones',
      changes: ['Diente extraído', 'Estado cambiado a ausente']
    },
    {
      id: 6,
      date: '2024-08-28',
      time: '13:30',
      tooth: 14,
      dentist: 'Dr. Ana Rodríguez',
      procedure: 'Corona de Porcelana',
      cost: { bs: 1200000, usd: 32.93 },
      status: 'completed',
      notes: 'Corona cementada, ajuste oclusal perfecto',
      changes: ['Corona instalada', 'Tratamiento completado']
    }
  ];

  // Get unique dentists and procedures for filters
  const dentists = [...new Set(allInterventions.map(i => i.dentist))];
  const procedures = [...new Set(allInterventions.map(i => i.procedure))];

  // Filter interventions
  const filteredInterventions = allInterventions?.filter(intervention => {
    if (selectedTooth && intervention?.tooth !== selectedTooth) return false;
    if (filterDentist !== 'all' && intervention?.dentist !== filterDentist) return false;
    if (filterProcedure !== 'all' && intervention?.procedure !== filterProcedure) return false;
    
    if (dateRange !== 'all') {
      const interventionDate = new Date(intervention.date);
      const today = new Date();
      const daysAgo = Math.floor((today - interventionDate) / (1000 * 60 * 60 * 24));
      
      switch (dateRange) {
        case '7': return daysAgo <= 7;
        case '30': return daysAgo <= 30;
        case '90': return daysAgo <= 90;
        default: return true;
      }
    }
    
    return true;
  });

  const formatCurrency = (amount, currency) => {
    if (currency === 'bs') {
      return `${amount?.toLocaleString('es-VE')} Bs`;
    }
    return `$${amount?.toFixed(2)}`;
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return { icon: 'CheckCircle', color: 'text-success' };
      case 'in-progress': return { icon: 'Clock', color: 'text-warning' };
      case 'scheduled': return { icon: 'Calendar', color: 'text-primary' };
      default: return { icon: 'Circle', color: 'text-muted-foreground' };
    }
  };

  const getProcedureIcon = (procedure) => {
    switch (procedure?.toLowerCase()) {
      case 'limpieza dental': return 'Sparkles';
      case 'obturación con resina': return 'Wrench';
      case 'corona de porcelana': return 'Crown';
      case 'extracción': return 'Scissors';
      case 'endodoncia': return 'Zap';
      case 'diagnóstico': return 'Search';
      default: return 'Activity';
    }
  };

  return (
    <div className={`bg-card border border-border rounded-lg ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-foreground">
            {selectedTooth ? `Historial - Diente ${selectedTooth}` : 'Línea de Tiempo de Intervenciones'}
          </h3>
          <div className="text-sm text-muted-foreground">
            {filteredInterventions?.length} intervenciones
          </div>
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-medium text-muted-foreground mb-1 block">
              Dentista
            </label>
            <select
              value={filterDentist}
              onChange={(e) => setFilterDentist(e?.target?.value)}
              className="w-full px-3 py-2 border border-border rounded-md text-sm bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="all">Todos los dentistas</option>
              {dentists?.map(dentist => (
                <option key={dentist} value={dentist}>{dentist}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-muted-foreground mb-1 block">
              Procedimiento
            </label>
            <select
              value={filterProcedure}
              onChange={(e) => setFilterProcedure(e?.target?.value)}
              className="w-full px-3 py-2 border border-border rounded-md text-sm bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="all">Todos los procedimientos</option>
              {procedures?.map(procedure => (
                <option key={procedure} value={procedure}>{procedure}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-muted-foreground mb-1 block">
              Período
            </label>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e?.target?.value)}
              className="w-full px-3 py-2 border border-border rounded-md text-sm bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="all">Todo el historial</option>
              <option value="7">Últimos 7 días</option>
              <option value="30">Últimos 30 días</option>
              <option value="90">Últimos 90 días</option>
            </select>
          </div>
        </div>
      </div>
      {/* Timeline */}
      <div className="p-4 max-h-96 overflow-y-auto">
        {filteredInterventions?.length > 0 ? (
          <div className="space-y-4">
            {filteredInterventions?.map((intervention, index) => {
              const statusConfig = getStatusIcon(intervention?.status);
              const isLast = index === filteredInterventions?.length - 1;
              
              return (
                <div key={intervention?.id} className="relative">
                  {/* Timeline line */}
                  {!isLast && (
                    <div className="absolute left-6 top-12 w-0.5 h-full bg-border"></div>
                  )}
                  {/* Timeline item */}
                  <div 
                    className="flex items-start space-x-4 cursor-pointer hover:bg-muted/50 rounded-md p-2 transition-smooth"
                    onClick={() => onInterventionClick && onInterventionClick(intervention)}
                  >
                    {/* Status indicator */}
                    <div className="flex-shrink-0 w-12 h-12 bg-background border-2 border-border rounded-full flex items-center justify-center">
                      <Icon 
                        name={statusConfig?.icon} 
                        size={20} 
                        className={statusConfig?.color} 
                      />
                    </div>
                    
                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <Icon 
                              name={getProcedureIcon(intervention?.procedure)} 
                              size={16} 
                              className="text-primary" 
                            />
                            <h4 className="font-medium text-foreground">
                              {intervention?.procedure}
                            </h4>
                            {!selectedTooth && (
                              <span className="bg-primary/10 text-primary text-xs px-2 py-1 rounded">
                                Diente {intervention?.tooth}
                              </span>
                            )}
                          </div>
                          
                          <div className="text-sm text-muted-foreground mb-2">
                            {new Date(intervention.date)?.toLocaleDateString('es-VE')} • {intervention?.time} • {intervention?.dentist}
                          </div>
                          
                          {intervention?.notes && (
                            <p className="text-sm text-foreground mb-2">
                              {intervention?.notes}
                            </p>
                          )}
                          
                          {intervention?.changes?.length > 0 && (
                            <div className="flex flex-wrap gap-1 mb-2">
                              {intervention?.changes?.map((change, idx) => (
                                <span 
                                  key={idx}
                                  className="bg-success/10 text-success text-xs px-2 py-1 rounded"
                                >
                                  {change}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                        
                        {/* Cost */}
                        <div className="text-right ml-4">
                          <div className="text-sm font-medium text-foreground">
                            {formatCurrency(intervention?.cost?.bs, 'bs')}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {formatCurrency(intervention?.cost?.usd, 'usd')}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <Icon name="Clock" size={48} className="text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-foreground mb-2">
              No hay intervenciones
            </h3>
            <p className="text-muted-foreground">
              {selectedTooth 
                ? `No se encontraron intervenciones para el diente ${selectedTooth} con los filtros aplicados.`
                : 'No se encontraron intervenciones con los filtros aplicados.'
              }
            </p>
            <Button 
              variant="outline" 
              className="mt-4"
              onClick={() => {
                setFilterDentist('all');
                setFilterProcedure('all');
                setDateRange('all');
              }}
            >
              Limpiar Filtros
            </Button>
          </div>
        )}
      </div>
      {/* Summary */}
      {filteredInterventions?.length > 0 && (
        <div className="p-4 border-t border-border bg-muted/30">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-lg font-semibold text-foreground">
                {filteredInterventions?.length}
              </div>
              <div className="text-xs text-muted-foreground">Intervenciones</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-foreground">
                {formatCurrency(
                  filteredInterventions?.reduce((sum, i) => sum + i?.cost?.bs, 0), 
                  'bs'
                )}
              </div>
              <div className="text-xs text-muted-foreground">Total Bs</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-foreground">
                {formatCurrency(
                  filteredInterventions?.reduce((sum, i) => sum + i?.cost?.usd, 0), 
                  'usd'
                )}
              </div>
              <div className="text-xs text-muted-foreground">Total USD</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-foreground">
                {[...new Set(filteredInterventions.map(i => i.tooth))]?.length}
              </div>
              <div className="text-xs text-muted-foreground">Dientes Tratados</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InterventionTimeline;