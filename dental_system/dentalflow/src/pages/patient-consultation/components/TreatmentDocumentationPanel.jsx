import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const TreatmentDocumentationPanel = ({ onInterventionAdd, onSignatureCapture }) => {
  const [currentIntervention, setCurrentIntervention] = useState({
    procedure: '',
    tooth: '',
    notes: '',
    costBs: '',
    costUsd: '',
    dentist: '',
    duration: '',
    materials: []
  });

  const [exchangeRate] = useState(36.45);
  const [showSignaturePad, setShowSignaturePad] = useState(false);
  const [interventions, setInterventions] = useState([
    {
      id: 1,
      procedure: 'Limpieza Dental',
      tooth: '11',
      dentist: 'Dr. María González',
      costBs: 1500,
      costUsd: 41.15,
      timestamp: new Date(Date.now() - 3600000),
      status: 'completed'
    },
    {
      id: 2,
      procedure: 'Obturación',
      tooth: '16',
      dentist: 'Dr. Carlos Mendoza',
      costBs: 2800,
      costUsd: 76.82,
      timestamp: new Date(Date.now() - 1800000),
      status: 'in-progress'
    }
  ]);

  const procedureOptions = [
    { value: 'limpieza', label: 'Limpieza Dental' },
    { value: 'obturacion', label: 'Obturación' },
    { value: 'extraccion', label: 'Extracción' },
    { value: 'endodoncia', label: 'Endodoncia' },
    { value: 'corona', label: 'Corona' },
    { value: 'implante', label: 'Implante' },
    { value: 'blanqueamiento', label: 'Blanqueamiento' },
    { value: 'ortodoncia', label: 'Ortodoncia' },
    { value: 'cirugia', label: 'Cirugía Oral' },
    { value: 'protesis', label: 'Prótesis' }
  ];

  const toothOptions = Array.from({ length: 32 }, (_, i) => {
    const toothNumber = i + 11 <= 18 ? i + 11 : i + 11 <= 28 ? i + 13 : i + 11 <= 38 ? i + 15 : i + 17;
    return { value: toothNumber?.toString(), label: `Diente ${toothNumber}` };
  });

  const dentistOptions = [
    { value: 'dr-gonzalez', label: 'Dr. María González' },
    { value: 'dr-mendoza', label: 'Dr. Carlos Mendoza' },
    { value: 'dr-silva', label: 'Dr. Ana Silva' },
    { value: 'dr-torres', label: 'Dr. Luis Torres' }
  ];

  const materialOptions = [
    { value: 'amalgama', label: 'Amalgama' },
    { value: 'resina', label: 'Resina Compuesta' },
    { value: 'ceramica', label: 'Cerámica' },
    { value: 'oro', label: 'Oro' },
    { value: 'titanio', label: 'Titanio' }
  ];

  const handleInputChange = (field, value) => {
    setCurrentIntervention(prev => ({
      ...prev,
      [field]: value
    }));

    // Auto-calculate currency conversion
    if (field === 'costBs' && value) {
      const usdValue = (parseFloat(value) / exchangeRate)?.toFixed(2);
      setCurrentIntervention(prev => ({
        ...prev,
        costUsd: usdValue
      }));
    } else if (field === 'costUsd' && value) {
      const bsValue = (parseFloat(value) * exchangeRate)?.toFixed(2);
      setCurrentIntervention(prev => ({
        ...prev,
        costBs: bsValue
      }));
    }
  };

  const handleAddIntervention = () => {
    if (!currentIntervention?.procedure || !currentIntervention?.tooth) {
      return;
    }

    const newIntervention = {
      id: Date.now(),
      ...currentIntervention,
      timestamp: new Date(),
      status: 'completed'
    };

    setInterventions(prev => [...prev, newIntervention]);
    
    if (onInterventionAdd) {
      onInterventionAdd(newIntervention);
    }

    // Reset form
    setCurrentIntervention({
      procedure: '',
      tooth: '',
      notes: '',
      costBs: '',
      costUsd: '',
      dentist: '',
      duration: '',
      materials: []
    });
  };

  const handleSignature = () => {
    setShowSignaturePad(true);
    if (onSignatureCapture) {
      onSignatureCapture();
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'text-success bg-success/10';
      case 'in-progress':
        return 'text-warning bg-warning/10';
      case 'pending':
        return 'text-muted-foreground bg-muted';
      default:
        return 'text-muted-foreground bg-muted';
    }
  };

  const totalCostBs = interventions?.reduce((sum, intervention) => sum + (intervention?.costBs || 0), 0);
  const totalCostUsd = interventions?.reduce((sum, intervention) => sum + (intervention?.costUsd || 0), 0);

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="Stethoscope" size={20} className="text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Documentación de Tratamiento</h2>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-sm text-muted-foreground">
            Tasa: {exchangeRate?.toFixed(2)} Bs/USD
          </div>
        </div>
      </div>
      <div className="p-4 space-y-6">
        {/* New Intervention Form */}
        <div className="bg-muted/50 rounded-lg p-4">
          <h3 className="text-md font-semibold text-foreground mb-4 flex items-center">
            <Icon name="Plus" size={16} className="mr-2 text-primary" />
            Nueva Intervención
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Select
              label="Procedimiento"
              options={procedureOptions}
              value={currentIntervention?.procedure}
              onChange={(value) => handleInputChange('procedure', value)}
              required
            />

            <Select
              label="Diente"
              options={toothOptions}
              value={currentIntervention?.tooth}
              onChange={(value) => handleInputChange('tooth', value)}
              searchable
              required
            />

            <Select
              label="Dentista"
              options={dentistOptions}
              value={currentIntervention?.dentist}
              onChange={(value) => handleInputChange('dentist', value)}
              required
            />

            <Input
              label="Costo (Bs)"
              type="number"
              value={currentIntervention?.costBs}
              onChange={(e) => handleInputChange('costBs', e?.target?.value)}
              placeholder="0.00"
            />

            <Input
              label="Costo (USD)"
              type="number"
              value={currentIntervention?.costUsd}
              onChange={(e) => handleInputChange('costUsd', e?.target?.value)}
              placeholder="0.00"
            />

            <Input
              label="Duración (min)"
              type="number"
              value={currentIntervention?.duration}
              onChange={(e) => handleInputChange('duration', e?.target?.value)}
              placeholder="30"
            />
          </div>

          <div className="mt-4">
            <Input
              label="Notas del Procedimiento"
              type="text"
              value={currentIntervention?.notes}
              onChange={(e) => handleInputChange('notes', e?.target?.value)}
              placeholder="Detalles adicionales del tratamiento..."
            />
          </div>

          <div className="mt-4">
            <Select
              label="Materiales Utilizados"
              options={materialOptions}
              value={currentIntervention?.materials}
              onChange={(value) => handleInputChange('materials', value)}
              multiple
              searchable
            />
          </div>

          <div className="flex justify-end space-x-3 mt-6">
            <Button variant="outline" onClick={handleSignature}>
              <Icon name="PenTool" size={16} className="mr-2" />
              Capturar Firma
            </Button>
            <Button onClick={handleAddIntervention}>
              <Icon name="Plus" size={16} className="mr-2" />
              Agregar Intervención
            </Button>
          </div>
        </div>

        {/* Current Session Interventions */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-md font-semibold text-foreground flex items-center">
              <Icon name="List" size={16} className="mr-2 text-primary" />
              Intervenciones de la Sesión
            </h3>
            <div className="text-sm text-muted-foreground">
              {interventions?.length} intervención{interventions?.length !== 1 ? 'es' : ''}
            </div>
          </div>

          <div className="space-y-3">
            {interventions?.map((intervention) => (
              <div key={intervention?.id} className="bg-card border border-border rounded-md p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="font-medium text-foreground">
                        {procedureOptions?.find(p => p?.value === intervention?.procedure)?.label || intervention?.procedure}
                      </h4>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(intervention?.status)}`}>
                        {intervention?.status === 'completed' ? 'Completado' : 
                         intervention?.status === 'in-progress' ? 'En Progreso' : 'Pendiente'}
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm text-muted-foreground">
                      <div>
                        <span className="font-medium">Diente:</span> {intervention?.tooth}
                      </div>
                      <div>
                        <span className="font-medium">Dentista:</span> {intervention?.dentist}
                      </div>
                      <div>
                        <span className="font-medium">Costo:</span> {intervention?.costBs} Bs
                      </div>
                      <div>
                        <span className="font-medium">USD:</span> ${intervention?.costUsd}
                      </div>
                    </div>

                    <div className="text-xs text-muted-foreground mt-2">
                      {intervention?.timestamp?.toLocaleString('es-VE')}
                    </div>
                  </div>

                  <div className="flex space-x-2">
                    <Button variant="ghost" size="sm">
                      <Icon name="Edit" size={14} />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Icon name="Trash2" size={14} className="text-error" />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Session Summary */}
        <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
          <h3 className="text-md font-semibold text-foreground mb-3 flex items-center">
            <Icon name="Calculator" size={16} className="mr-2 text-primary" />
            Resumen de la Sesión
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{interventions?.length}</div>
              <div className="text-xs text-muted-foreground">Intervenciones</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-foreground">{totalCostBs?.toLocaleString()} Bs</div>
              <div className="text-xs text-muted-foreground">Total Bolívares</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-foreground">${totalCostUsd?.toFixed(2)}</div>
              <div className="text-xs text-muted-foreground">Total USD</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-success">
                {interventions?.filter(i => i?.status === 'completed')?.length}/{interventions?.length}
              </div>
              <div className="text-xs text-muted-foreground">Completadas</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TreatmentDocumentationPanel;