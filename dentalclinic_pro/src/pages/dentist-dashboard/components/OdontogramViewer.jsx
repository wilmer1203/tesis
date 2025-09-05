import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const OdontogramViewer = ({ patient, onUpdateOdontogram, onSaveChanges }) => {
  const [selectedTooth, setSelectedTooth] = useState(null);
  const [treatmentMode, setTreatmentMode] = useState('view');
  const [selectedTreatment, setSelectedTreatment] = useState('');
  const [hasChanges, setHasChanges] = useState(false);

  // Dental chart layout - Adult teeth (32 teeth)
  const upperTeeth = [
    { id: 18, number: '18', position: 'upper-right' },
    { id: 17, number: '17', position: 'upper-right' },
    { id: 16, number: '16', position: 'upper-right' },
    { id: 15, number: '15', position: 'upper-right' },
    { id: 14, number: '14', position: 'upper-right' },
    { id: 13, number: '13', position: 'upper-right' },
    { id: 12, number: '12', position: 'upper-right' },
    { id: 11, number: '11', position: 'upper-right' },
    { id: 21, number: '21', position: 'upper-left' },
    { id: 22, number: '22', position: 'upper-left' },
    { id: 23, number: '23', position: 'upper-left' },
    { id: 24, number: '24', position: 'upper-left' },
    { id: 25, number: '25', position: 'upper-left' },
    { id: 26, number: '26', position: 'upper-left' },
    { id: 27, number: '27', position: 'upper-left' },
    { id: 28, number: '28', position: 'upper-left' }
  ];

  const lowerTeeth = [
    { id: 48, number: '48', position: 'lower-right' },
    { id: 47, number: '47', position: 'lower-right' },
    { id: 46, number: '46', position: 'lower-right' },
    { id: 45, number: '45', position: 'lower-right' },
    { id: 44, number: '44', position: 'lower-right' },
    { id: 43, number: '43', position: 'lower-right' },
    { id: 42, number: '42', position: 'lower-right' },
    { id: 41, number: '41', position: 'lower-right' },
    { id: 31, number: '31', position: 'lower-left' },
    { id: 32, number: '32', position: 'lower-left' },
    { id: 33, number: '33', position: 'lower-left' },
    { id: 34, number: '34', position: 'lower-left' },
    { id: 35, number: '35', position: 'lower-left' },
    { id: 36, number: '36', position: 'lower-left' },
    { id: 37, number: '37', position: 'lower-left' },
    { id: 38, number: '38', position: 'lower-left' }
  ];

  const treatmentCodes = [
    { code: 'S', label: 'Sano', color: 'bg-success' },
    { code: 'C', label: 'Caries', color: 'bg-error' },
    { code: 'O', label: 'Obturación', color: 'bg-primary' },
    { code: 'E', label: 'Extracción', color: 'bg-destructive' },
    { code: 'I', label: 'Implante', color: 'bg-secondary' },
    { code: 'P', label: 'Prótesis', color: 'bg-warning' },
    { code: 'R', label: 'Endodoncia', color: 'bg-accent' },
    { code: 'F', label: 'Faltante', color: 'bg-muted' }
  ];

  const getToothCondition = (toothId) => {
    if (!patient?.odontograma) return 'S';
    return patient?.odontograma?.[toothId] || 'S';
  };

  const getToothColor = (condition) => {
    const treatment = treatmentCodes?.find(t => t?.code === condition);
    return treatment ? treatment?.color : 'bg-muted';
  };

  const handleToothClick = (tooth) => {
    if (treatmentMode === 'edit') {
      setSelectedTooth(tooth);
    }
  };

  const handleTreatmentApply = () => {
    if (selectedTooth && selectedTreatment) {
      onUpdateOdontogram(selectedTooth?.id, selectedTreatment);
      setHasChanges(true);
      setSelectedTooth(null);
      setSelectedTreatment('');
    }
  };

  const handleSave = () => {
    onSaveChanges();
    setHasChanges(false);
    setTreatmentMode('view');
  };

  const ToothComponent = ({ tooth, isUpper = true }) => {
    const condition = getToothCondition(tooth?.id);
    const isSelected = selectedTooth?.id === tooth?.id;
    
    return (
      <div className="flex flex-col items-center space-y-1">
        <span className="text-xs text-muted-foreground font-mono">
          {tooth?.number}
        </span>
        <div
          className={`w-8 h-8 rounded-md border-2 cursor-pointer transition-all duration-200 flex items-center justify-center ${
            getToothColor(condition)
          } ${
            isSelected 
              ? 'border-primary ring-2 ring-primary/30 scale-110' :'border-border hover:border-primary/50'
          } ${
            treatmentMode === 'edit' ? 'hover:scale-105' : ''
          }`}
          onClick={() => handleToothClick(tooth)}
          title={`Diente ${tooth?.number}: ${treatmentCodes?.find(t => t?.code === condition)?.label || 'Sano'}`}
        >
          <span className="text-xs font-bold text-white">
            {condition}
          </span>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Icon name="Stethoscope" size={20} color="var(--color-primary)" />
          <div>
            <h3 className="text-lg font-semibold text-card-foreground">
              Odontograma
            </h3>
            {patient && (
              <p className="text-sm text-muted-foreground">
                {patient?.nombre} {patient?.apellido}
              </p>
            )}
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {hasChanges && (
            <span className="text-xs text-warning bg-warning/10 px-2 py-1 rounded-md">
              Cambios sin guardar
            </span>
          )}
          
          <Button
            variant={treatmentMode === 'edit' ? 'default' : 'outline'}
            size="sm"
            iconName="Edit"
            iconPosition="left"
            iconSize={16}
            onClick={() => setTreatmentMode(treatmentMode === 'edit' ? 'view' : 'edit')}
          >
            {treatmentMode === 'edit' ? 'Modo Vista' : 'Editar'}
          </Button>

          {hasChanges && (
            <Button
              variant="success"
              size="sm"
              iconName="Save"
              iconPosition="left"
              iconSize={16}
              onClick={handleSave}
            >
              Guardar
            </Button>
          )}
        </div>
      </div>
      {/* Treatment Legend */}
      <div className="mb-6 p-4 bg-muted/30 rounded-lg">
        <h4 className="text-sm font-medium text-card-foreground mb-3">
          Códigos de Tratamiento
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
          {treatmentCodes?.map((treatment) => (
            <div key={treatment?.code} className="flex items-center space-x-2">
              <div className={`w-4 h-4 rounded ${treatment?.color} flex items-center justify-center`}>
                <span className="text-xs font-bold text-white">
                  {treatment?.code}
                </span>
              </div>
              <span className="text-xs text-card-foreground">
                {treatment?.label}
              </span>
            </div>
          ))}
        </div>
      </div>
      {/* Dental Chart */}
      <div className="space-y-8">
        {/* Upper Teeth */}
        <div className="flex flex-col items-center space-y-4">
          <h4 className="text-sm font-medium text-muted-foreground">
            Arcada Superior
          </h4>
          <div className="flex items-center space-x-2 md:space-x-3">
            {upperTeeth?.map((tooth) => (
              <ToothComponent key={tooth?.id} tooth={tooth} isUpper={true} />
            ))}
          </div>
        </div>

        {/* Lower Teeth */}
        <div className="flex flex-col items-center space-y-4">
          <div className="flex items-center space-x-2 md:space-x-3">
            {lowerTeeth?.map((tooth) => (
              <ToothComponent key={tooth?.id} tooth={tooth} isUpper={false} />
            ))}
          </div>
          <h4 className="text-sm font-medium text-muted-foreground">
            Arcada Inferior
          </h4>
        </div>
      </div>
      {/* Treatment Selection Panel */}
      {treatmentMode === 'edit' && selectedTooth && (
        <div className="mt-6 p-4 bg-primary/5 border border-primary/20 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-sm font-medium text-card-foreground">
              Aplicar Tratamiento - Diente {selectedTooth?.number}
            </h4>
            <Button
              variant="ghost"
              size="xs"
              iconName="X"
              onClick={() => setSelectedTooth(null)}
            />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-4">
            {treatmentCodes?.map((treatment) => (
              <Button
                key={treatment?.code}
                variant={selectedTreatment === treatment?.code ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedTreatment(treatment?.code)}
                className="justify-start"
              >
                <div className={`w-3 h-3 rounded mr-2 ${treatment?.color}`} />
                {treatment?.label}
              </Button>
            ))}
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="default"
              size="sm"
              iconName="Check"
              iconPosition="left"
              iconSize={16}
              onClick={handleTreatmentApply}
              disabled={!selectedTreatment}
            >
              Aplicar Tratamiento
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setSelectedTooth(null);
                setSelectedTreatment('');
              }}
            >
              Cancelar
            </Button>
          </div>
        </div>
      )}
      {/* Instructions */}
      {treatmentMode === 'edit' && !selectedTooth && (
        <div className="mt-6 p-4 bg-muted/20 rounded-lg">
          <div className="flex items-center space-x-2 mb-2">
            <Icon name="Info" size={16} color="var(--color-primary)" />
            <span className="text-sm font-medium text-card-foreground">
              Instrucciones
            </span>
          </div>
          <p className="text-sm text-muted-foreground">
            Haga clic en cualquier diente para seleccionarlo y aplicar un tratamiento. 
            Los cambios se guardarán automáticamente en el historial del paciente.
          </p>
        </div>
      )}
    </div>
  );
};

export default OdontogramViewer;