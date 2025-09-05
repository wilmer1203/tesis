import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ToothDetailPanel = ({ 
  selectedTooth, 
  onClose, 
  onAddIntervention,
  className = '' 
}) => {
  const [activeTab, setActiveTab] = useState('history');

  if (!selectedTooth) return null;

  // Mock tooth data with detailed information
  const toothData = {
    11: {
      number: 11,
      name: 'Incisivo Central Superior Derecho',
      status: 'Sano',
      conditions: [],
      interventions: [
        {
          id: 1,
          date: '2024-08-15',
          dentist: 'Dr. María González',
          procedure: 'Limpieza Dental',
          cost: { bs: 150000, usd: 4.11 },
          notes: 'Limpieza rutinaria, sin complicaciones'
        }
      ],
      plannedTreatments: []
    },
    12: {
      number: 12,
      name: 'Incisivo Lateral Superior Derecho',
      status: 'Caries',
      conditions: ['Caries Oclusal', 'Sensibilidad'],
      interventions: [
        {
          id: 2,
          date: '2024-09-01',
          dentist: 'Dr. Carlos Mendoza',
          procedure: 'Diagnóstico',
          cost: { bs: 80000, usd: 2.19 },
          notes: 'Caries detectada en superficie oclusal'
        }
      ],
      plannedTreatments: [
        {
          id: 1,
          procedure: 'Obturación con Resina',
          estimatedCost: { bs: 250000, usd: 6.85 },
          priority: 'Alta',
          notes: 'Requiere tratamiento inmediato'
        }
      ]
    },
    16: {
      number: 16,
      name: 'Primer Molar Superior Derecho',
      status: 'Endodoncia + Corona',
      conditions: ['Pulpitis Irreversible'],
      interventions: [
        {
          id: 3,
          date: '2024-07-20',
          dentist: 'Dr. Ana Rodríguez',
          procedure: 'Endodoncia',
          cost: { bs: 800000, usd: 21.95 },
          notes: 'Tratamiento de conducto completado en 3 sesiones'
        },
        {
          id: 4,
          date: '2024-08-10',
          dentist: 'Dr. Ana Rodríguez',
          procedure: 'Corona de Porcelana',
          cost: { bs: 1200000, usd: 32.93 },
          notes: 'Corona cementada, oclusión ajustada'
        }
      ],
      plannedTreatments: []
    }
  };

  const currentTooth = toothData?.[selectedTooth] || {
    number: selectedTooth,
    name: `Diente ${selectedTooth}`,
    status: 'Sin información',
    conditions: [],
    interventions: [],
    plannedTreatments: []
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'sano': return 'text-success';
      case 'caries': return 'text-error';
      case 'obturado': return 'text-primary';
      case 'endodoncia + corona': return 'text-warning';
      default: return 'text-muted-foreground';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
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

  const tabs = [
    { id: 'history', label: 'Historial', icon: 'History' },
    { id: 'conditions', label: 'Condiciones', icon: 'AlertTriangle' },
    { id: 'planned', label: 'Planificado', icon: 'Calendar' }
  ];

  return (
    <div className={`bg-card border border-border rounded-lg shadow-soft ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div>
          <h3 className="text-lg font-semibold text-foreground">
            Diente {currentTooth?.number}
          </h3>
          <p className="text-sm text-muted-foreground">{currentTooth?.name}</p>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(currentTooth?.status)} bg-muted`}>
            {currentTooth?.status}
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <Icon name="X" size={16} />
          </Button>
        </div>
      </div>
      {/* Tabs */}
      <div className="flex border-b border-border">
        {tabs?.map((tab) => (
          <button
            key={tab?.id}
            onClick={() => setActiveTab(tab?.id)}
            className={`flex items-center space-x-2 px-4 py-3 text-sm font-medium transition-smooth ${
              activeTab === tab?.id
                ? 'text-primary border-b-2 border-primary bg-primary/5' :'text-muted-foreground hover:text-foreground hover:bg-muted'
            }`}
          >
            <Icon name={tab?.icon} size={16} />
            <span>{tab?.label}</span>
            {tab?.id === 'conditions' && currentTooth?.conditions?.length > 0 && (
              <span className="bg-error text-error-foreground text-xs rounded-full px-2 py-0.5">
                {currentTooth?.conditions?.length}
              </span>
            )}
            {tab?.id === 'planned' && currentTooth?.plannedTreatments?.length > 0 && (
              <span className="bg-warning text-warning-foreground text-xs rounded-full px-2 py-0.5">
                {currentTooth?.plannedTreatments?.length}
              </span>
            )}
          </button>
        ))}
      </div>
      {/* Content */}
      <div className="p-4 max-h-96 overflow-y-auto">
        {activeTab === 'history' && (
          <div className="space-y-4">
            {currentTooth?.interventions?.length > 0 ? (
              currentTooth?.interventions?.map((intervention) => (
                <div key={intervention?.id} className="bg-muted rounded-md p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-medium text-foreground">{intervention?.procedure}</h4>
                      <p className="text-sm text-muted-foreground">
                        {new Date(intervention.date)?.toLocaleDateString('es-VE')} • {intervention?.dentist}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-foreground">
                        {formatCurrency(intervention?.cost?.bs, 'bs')}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {formatCurrency(intervention?.cost?.usd, 'usd')}
                      </div>
                    </div>
                  </div>
                  {intervention?.notes && (
                    <p className="text-sm text-muted-foreground mt-2">
                      {intervention?.notes}
                    </p>
                  )}
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <Icon name="FileText" size={48} className="text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">No hay intervenciones registradas</p>
              </div>
            )}
            
            <Button 
              variant="outline" 
              className="w-full"
              onClick={() => onAddIntervention(selectedTooth)}
            >
              <Icon name="Plus" size={16} className="mr-2" />
              Agregar Intervención
            </Button>
          </div>
        )}

        {activeTab === 'conditions' && (
          <div className="space-y-4">
            {currentTooth?.conditions?.length > 0 ? (
              currentTooth?.conditions?.map((condition, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-error/10 rounded-md">
                  <Icon name="AlertTriangle" size={20} className="text-error" />
                  <div>
                    <p className="font-medium text-foreground">{condition}</p>
                    <p className="text-sm text-muted-foreground">
                      Detectado el {new Date()?.toLocaleDateString('es-VE')}
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <Icon name="CheckCircle" size={48} className="text-success mx-auto mb-4" />
                <p className="text-success font-medium">Sin condiciones detectadas</p>
                <p className="text-muted-foreground text-sm">Este diente está en buen estado</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'planned' && (
          <div className="space-y-4">
            {currentTooth?.plannedTreatments?.length > 0 ? (
              currentTooth?.plannedTreatments?.map((treatment) => (
                <div key={treatment?.id} className="bg-warning/10 rounded-md p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-medium text-foreground">{treatment?.procedure}</h4>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className="text-xs text-muted-foreground">Prioridad:</span>
                        <span className={`text-xs font-medium ${getPriorityColor(treatment?.priority)}`}>
                          {treatment?.priority}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-foreground">
                        {formatCurrency(treatment?.estimatedCost?.bs, 'bs')}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {formatCurrency(treatment?.estimatedCost?.usd, 'usd')}
                      </div>
                    </div>
                  </div>
                  {treatment?.notes && (
                    <p className="text-sm text-muted-foreground mt-2">
                      {treatment?.notes}
                    </p>
                  )}
                  <div className="flex space-x-2 mt-3">
                    <Button variant="outline" size="sm" className="flex-1">
                      <Icon name="Calendar" size={14} className="mr-1" />
                      Programar
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1">
                      <Icon name="Edit" size={14} className="mr-1" />
                      Editar
                    </Button>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <Icon name="Calendar" size={48} className="text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">No hay tratamientos planificados</p>
              </div>
            )}
            
            <Button 
              variant="outline" 
              className="w-full"
              onClick={() => console.log('Add planned treatment')}
            >
              <Icon name="Plus" size={16} className="mr-2" />
              Planificar Tratamiento
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ToothDetailPanel;