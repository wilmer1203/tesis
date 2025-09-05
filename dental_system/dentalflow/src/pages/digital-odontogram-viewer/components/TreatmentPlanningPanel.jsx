import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';

const TreatmentPlanningPanel = ({ 
  selectedTooth, 
  onClose, 
  onSavePlan,
  className = '' 
}) => {
  const [planData, setPlanData] = useState({
    procedure: '',
    priority: 'media',
    estimatedCost: { bs: 0, usd: 0 },
    notes: '',
    scheduledDate: '',
    dentist: '',
    duration: 30
  });

  const [exchangeRate] = useState(36.45);

  // Mock procedures with estimated costs
  const procedures = [
    { 
      id: 'cleaning', 
      name: 'Limpieza Dental', 
      cost: { bs: 150000, usd: 4.11 },
      duration: 30,
      description: 'Limpieza profesional y eliminación de sarro'
    },
    { 
      id: 'filling', 
      name: 'Obturación con Resina', 
      cost: { bs: 250000, usd: 6.85 },
      duration: 45,
      description: 'Restauración con material composite'
    },
    { 
      id: 'crown', 
      name: 'Corona de Porcelana', 
      cost: { bs: 1200000, usd: 32.93 },
      duration: 90,
      description: 'Corona de porcelana sobre metal'
    },
    { 
      id: 'root-canal', 
      name: 'Endodoncia', 
      cost: { bs: 800000, usd: 21.95 },
      duration: 120,
      description: 'Tratamiento de conducto radicular'
    },
    { 
      id: 'extraction', 
      name: 'Extracción', 
      cost: { bs: 300000, usd: 8.22 },
      duration: 30,
      description: 'Extracción dental simple'
    },
    { 
      id: 'implant', 
      name: 'Implante Dental', 
      cost: { bs: 2500000, usd: 68.58 },
      duration: 180,
      description: 'Implante de titanio con corona'
    }
  ];

  const dentists = [
    'Dr. María González',
    'Dr. Carlos Mendoza',
    'Dr. Ana Rodríguez',
    'Dr. Luis Herrera'
  ];

  const handleProcedureChange = (procedureId) => {
    const procedure = procedures?.find(p => p?.id === procedureId);
    if (procedure) {
      setPlanData(prev => ({
        ...prev,
        procedure: procedure?.name,
        estimatedCost: procedure?.cost,
        duration: procedure?.duration
      }));
    }
  };

  const handleCostChange = (currency, value) => {
    const numValue = parseFloat(value) || 0;
    if (currency === 'bs') {
      setPlanData(prev => ({
        ...prev,
        estimatedCost: {
          bs: numValue,
          usd: numValue / exchangeRate
        }
      }));
    } else {
      setPlanData(prev => ({
        ...prev,
        estimatedCost: {
          bs: numValue * exchangeRate,
          usd: numValue
        }
      }));
    }
  };

  const handleSave = () => {
    if (!planData?.procedure || !planData?.dentist) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    const plan = {
      ...planData,
      tooth: selectedTooth,
      id: Date.now(),
      createdDate: new Date()?.toISOString(),
      status: 'planned'
    };

    onSavePlan(plan);
    onClose();
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'alta': return 'text-error';
      case 'media': return 'text-warning';
      case 'baja': return 'text-success';
      default: return 'text-muted-foreground';
    }
  };

  const formatCurrency = (amount, currency) => {
    if (currency === 'bs') {
      return `${amount?.toLocaleString('es-VE')} Bs`;
    }
    return `$${amount?.toFixed(2)}`;
  };

  if (!selectedTooth) return null;

  return (
    <div className={`bg-card border border-border rounded-lg shadow-soft ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div>
          <h3 className="text-lg font-semibold text-foreground">
            Planificar Tratamiento
          </h3>
          <p className="text-sm text-muted-foreground">Diente {selectedTooth}</p>
        </div>
        
        <Button variant="ghost" size="sm" onClick={onClose}>
          <Icon name="X" size={16} />
        </Button>
      </div>
      {/* Form */}
      <div className="p-4 space-y-6">
        {/* Procedure Selection */}
        <div>
          <label className="text-sm font-medium text-foreground mb-3 block">
            Procedimiento *
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {procedures?.map((procedure) => (
              <div
                key={procedure?.id}
                className={`p-3 border rounded-md cursor-pointer transition-smooth ${
                  planData?.procedure === procedure?.name
                    ? 'border-primary bg-primary/5' :'border-border hover:border-primary/50'
                }`}
                onClick={() => handleProcedureChange(procedure?.id)}
              >
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-medium text-foreground text-sm">
                    {procedure?.name}
                  </h4>
                  <div className="text-right">
                    <div className="text-xs font-medium text-foreground">
                      {formatCurrency(procedure?.cost?.bs, 'bs')}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {formatCurrency(procedure?.cost?.usd, 'usd')}
                    </div>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground">
                  {procedure?.description}
                </p>
                <div className="flex items-center space-x-2 mt-2 text-xs text-muted-foreground">
                  <Icon name="Clock" size={12} />
                  <span>{procedure?.duration} min</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Priority */}
        <div>
          <label className="text-sm font-medium text-foreground mb-2 block">
            Prioridad *
          </label>
          <div className="flex space-x-3">
            {['alta', 'media', 'baja']?.map((priority) => (
              <button
                key={priority}
                onClick={() => setPlanData(prev => ({ ...prev, priority }))}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-smooth ${
                  planData?.priority === priority
                    ? `${getPriorityColor(priority)} bg-current/10 border border-current`
                    : 'text-muted-foreground border border-border hover:border-primary/50'
                }`}
              >
                {priority?.charAt(0)?.toUpperCase() + priority?.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Cost Estimation */}
        <div>
          <label className="text-sm font-medium text-foreground mb-2 block">
            Costo Estimado
          </label>
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Bolívares"
              type="number"
              value={planData?.estimatedCost?.bs}
              onChange={(e) => handleCostChange('bs', e?.target?.value)}
              placeholder="0"
            />
            <Input
              label="Dólares USD"
              type="number"
              value={planData?.estimatedCost?.usd?.toFixed(2)}
              onChange={(e) => handleCostChange('usd', e?.target?.value)}
              placeholder="0.00"
            />
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Tasa de cambio: {exchangeRate?.toFixed(2)} Bs/USD
          </p>
        </div>

        {/* Dentist Assignment */}
        <div>
          <label className="text-sm font-medium text-foreground mb-2 block">
            Dentista Asignado *
          </label>
          <select
            value={planData?.dentist}
            onChange={(e) => setPlanData(prev => ({ ...prev, dentist: e?.target?.value }))}
            className="w-full px-3 py-2 border border-border rounded-md text-sm bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          >
            <option value="">Seleccionar dentista</option>
            {dentists?.map((dentist) => (
              <option key={dentist} value={dentist}>{dentist}</option>
            ))}
          </select>
        </div>

        {/* Scheduled Date */}
        <div>
          <Input
            label="Fecha Programada"
            type="date"
            value={planData?.scheduledDate}
            onChange={(e) => setPlanData(prev => ({ ...prev, scheduledDate: e?.target?.value }))}
            description="Opcional - Fecha tentativa para el tratamiento"
          />
        </div>

        {/* Duration */}
        <div>
          <Input
            label="Duración Estimada (minutos)"
            type="number"
            value={planData?.duration}
            onChange={(e) => setPlanData(prev => ({ ...prev, duration: parseInt(e?.target?.value) || 30 }))}
            min="15"
            max="300"
            step="15"
          />
        </div>

        {/* Notes */}
        <div>
          <label className="text-sm font-medium text-foreground mb-2 block">
            Notas Adicionales
          </label>
          <textarea
            value={planData?.notes}
            onChange={(e) => setPlanData(prev => ({ ...prev, notes: e?.target?.value }))}
            placeholder="Observaciones, consideraciones especiales, etc."
            rows={3}
            className="w-full px-3 py-2 border border-border rounded-md text-sm bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
          />
        </div>

        {/* Actions */}
        <div className="flex space-x-3 pt-4 border-t border-border">
          <Button variant="outline" onClick={onClose} className="flex-1">
            Cancelar
          </Button>
          <Button onClick={handleSave} className="flex-1">
            <Icon name="Save" size={16} className="mr-2" />
            Guardar Plan
          </Button>
        </div>
      </div>
      {/* Summary */}
      {planData?.procedure && (
        <div className="p-4 bg-muted/30 border-t border-border">
          <h4 className="text-sm font-medium text-foreground mb-2">Resumen del Plan</h4>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Procedimiento:</span>
              <span className="text-foreground">{planData?.procedure}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Prioridad:</span>
              <span className={getPriorityColor(planData?.priority)}>
                {planData?.priority?.charAt(0)?.toUpperCase() + planData?.priority?.slice(1)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Costo:</span>
              <span className="text-foreground">
                {formatCurrency(planData?.estimatedCost?.bs, 'bs')} / {formatCurrency(planData?.estimatedCost?.usd, 'usd')}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Duración:</span>
              <span className="text-foreground">{planData?.duration} minutos</span>
            </div>
            {planData?.dentist && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Dentista:</span>
                <span className="text-foreground">{planData?.dentist}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TreatmentPlanningPanel;