import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const InteractiveOdontogram = ({ 
  patient, 
  sessionActive, 
  onUpdateOdontogram, 
  onSaveChanges, 
  hasUnsavedChanges 
}) => {
  const [selectedTeeth, setSelectedTeeth] = useState([]);
  const [selectedTreatment, setSelectedTreatment] = useState('');
  const [treatmentNotes, setTreatmentNotes] = useState('');
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [batchMode, setBatchMode] = useState(false);
  const [treatmentHistory, setTreatmentHistory] = useState([]);

  // Enhanced dental chart layout
  const upperTeeth = [
    { id: 18, number: '18', position: 'upper-right', type: 'molar' },
    { id: 17, number: '17', position: 'upper-right', type: 'molar' },
    { id: 16, number: '16', position: 'upper-right', type: 'molar' },
    { id: 15, number: '15', position: 'upper-right', type: 'premolar' },
    { id: 14, number: '14', position: 'upper-right', type: 'premolar' },
    { id: 13, number: '13', position: 'upper-right', type: 'canine' },
    { id: 12, number: '12', position: 'upper-right', type: 'incisor' },
    { id: 11, number: '11', position: 'upper-right', type: 'incisor' },
    { id: 21, number: '21', position: 'upper-left', type: 'incisor' },
    { id: 22, number: '22', position: 'upper-left', type: 'incisor' },
    { id: 23, number: '23', position: 'upper-left', type: 'canine' },
    { id: 24, number: '24', position: 'upper-left', type: 'premolar' },
    { id: 25, number: '25', position: 'upper-left', type: 'premolar' },
    { id: 26, number: '26', position: 'upper-left', type: 'molar' },
    { id: 27, number: '27', position: 'upper-left', type: 'molar' },
    { id: 28, number: '28', position: 'upper-left', type: 'molar' }
  ];

  const lowerTeeth = [
    { id: 48, number: '48', position: 'lower-right', type: 'molar' },
    { id: 47, number: '47', position: 'lower-right', type: 'molar' },
    { id: 46, number: '46', position: 'lower-right', type: 'molar' },
    { id: 45, number: '45', position: 'lower-right', type: 'premolar' },
    { id: 44, number: '44', position: 'lower-right', type: 'premolar' },
    { id: 43, number: '43', position: 'lower-right', type: 'canine' },
    { id: 42, number: '42', position: 'lower-right', type: 'incisor' },
    { id: 41, number: '41', position: 'lower-right', type: 'incisor' },
    { id: 31, number: '31', position: 'lower-left', type: 'incisor' },
    { id: 32, number: '32', position: 'lower-left', type: 'incisor' },
    { id: 33, number: '33', position: 'lower-left', type: 'canine' },
    { id: 34, number: '34', position: 'lower-left', type: 'premolar' },
    { id: 35, number: '35', position: 'lower-left', type: 'premolar' },
    { id: 36, number: '36', position: 'lower-left', type: 'molar' },
    { id: 37, number: '37', position: 'lower-left', type: 'molar' },
    { id: 38, number: '38', position: 'lower-left', type: 'molar' }
  ];

  const treatmentCodes = [
    { code: 'S', label: 'Sano', color: 'bg-success', billingCode: 'D1110' },
    { code: 'C', label: 'Caries', color: 'bg-error', billingCode: 'D0150' },
    { code: 'O', label: 'Obturación', color: 'bg-primary', billingCode: 'D2140' },
    { code: 'E', label: 'Extracción', color: 'bg-destructive', billingCode: 'D7140' },
    { code: 'I', label: 'Implante', color: 'bg-secondary', billingCode: 'D6010' },
    { code: 'P', label: 'Prótesis', color: 'bg-warning', billingCode: 'D6240' },
    { code: 'R', label: 'Endodoncia', color: 'bg-accent', billingCode: 'D3310' },
    { code: 'F', label: 'Faltante', color: 'bg-muted', billingCode: 'D0120' },
    { code: 'L', label: 'Limpieza', color: 'bg-info', billingCode: 'D1110' },
    { code: 'CR', label: 'Corona', color: 'bg-violet-500', billingCode: 'D2740' }
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
    if (!sessionActive) return;
    
    if (batchMode) {
      setSelectedTeeth(prev => {
        const isSelected = prev?.some(t => t?.id === tooth?.id);
        if (isSelected) {
          return prev?.filter(t => t?.id !== tooth?.id);
        } else {
          return [...prev, tooth];
        }
      });
    } else {
      setSelectedTeeth([tooth]);
    }
  };

  const handleTreatmentApply = () => {
    if (selectedTeeth?.length === 0 || !selectedTreatment) return;

    selectedTeeth?.forEach(tooth => {
      onUpdateOdontogram(tooth?.id, selectedTreatment, treatmentNotes);
      
      // Add to treatment history
      const historyEntry = {
        id: Date.now() + tooth?.id,
        toothNumber: tooth?.number,
        toothId: tooth?.id,
        treatment: selectedTreatment,
        treatmentLabel: treatmentCodes?.find(t => t?.code === selectedTreatment)?.label,
        notes: treatmentNotes,
        timestamp: new Date(),
        billingCode: treatmentCodes?.find(t => t?.code === selectedTreatment)?.billingCode
      };
      
      setTreatmentHistory(prev => [historyEntry, ...prev]);
    });

    // Clear selections
    setSelectedTeeth([]);
    setSelectedTreatment('');
    setTreatmentNotes('');
  };

  const handleClearSelection = () => {
    setSelectedTeeth([]);
    setSelectedTreatment('');
    setTreatmentNotes('');
  };

  const toggleBatchMode = () => {
    setBatchMode(!batchMode);
    setSelectedTeeth([]);
  };

  const ToothComponent = ({ tooth, isUpper = true }) => {
    const condition = getToothCondition(tooth?.id);
    const isSelected = selectedTeeth?.some(t => t?.id === tooth?.id);
    const size = isFullScreen ? 'w-12 h-12 text-sm' : 'w-10 h-10 text-xs';
    
    return (
      <div className="flex flex-col items-center space-y-1">
        <span className={`text-xs text-muted-foreground font-mono ${isFullScreen ? 'text-sm' : ''}`}>
          {tooth?.number}
        </span>
        <div
          className={`${size} rounded-md border-2 cursor-pointer transition-all duration-200 flex items-center justify-center ${
            getToothColor(condition)
          } ${
            isSelected 
              ? 'border-primary ring-2 ring-primary/30 scale-110 shadow-lg' 
              : 'border-border hover:border-primary/50'
          } ${
            sessionActive ? 'hover:scale-105 hover:shadow-md' : 'cursor-not-allowed opacity-60'
          } ${
            !sessionActive ? 'pointer-events-none' : ''
          }`}
          onClick={() => handleToothClick(tooth)}
          title={`Diente ${tooth?.number} (${tooth?.type}): ${
            treatmentCodes?.find(t => t?.code === condition)?.label || 'Sano'
          }`}
        >
          <span className={`font-bold text-white ${isFullScreen ? 'text-sm' : 'text-xs'}`}>
            {condition}
          </span>
        </div>
        {/* Tooth type indicator */}
        <div className={`w-1 h-1 rounded-full ${
          tooth?.type === 'molar' ? 'bg-blue-500' :
          tooth?.type === 'premolar' ? 'bg-green-500' :
          tooth?.type === 'canine'? 'bg-yellow-500' : 'bg-gray-400'
        }`} />
      </div>
    );
  };

  return (
    <div className={`h-full ${isFullScreen ? 'fixed inset-0 z-50 bg-background' : ''}`}>
      <div className="h-full flex flex-col p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Icon name="Stethoscope" size={20} color="var(--color-primary)" />
            <div>
              <h3 className="text-lg font-semibold text-card-foreground">
                Odontograma Interactivo
              </h3>
              {patient && (
                <p className="text-sm text-muted-foreground">
                  {patient?.nombre} {patient?.apellido} • Sesión {sessionActive ? 'Activa' : 'Inactiva'}
                </p>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {hasUnsavedChanges && (
              <span className="text-xs text-warning bg-warning/10 px-2 py-1 rounded-md">
                Cambios sin guardar
              </span>
            )}
            
            <Button
              variant={batchMode ? 'default' : 'outline'}
              size="sm"
              iconName="MousePointer"
              iconPosition="left"
              iconSize={16}
              onClick={toggleBatchMode}
              disabled={!sessionActive}
            >
              {batchMode ? 'Selección Múltiple' : 'Selección Simple'}
            </Button>

            <Button
              variant="outline"
              size="sm"
              iconName={isFullScreen ? 'Minimize' : 'Maximize'}
              onClick={() => setIsFullScreen(!isFullScreen)}
            >
              {isFullScreen ? 'Salir' : 'Pantalla Completa'}
            </Button>

            {hasUnsavedChanges && (
              <Button
                variant="success"
                size="sm"
                iconName="Save"
                iconPosition="left"
                iconSize={16}
                onClick={onSaveChanges}
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
          <div className="grid grid-cols-2 md:grid-cols-5 lg:grid-cols-10 gap-2">
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
        <div className="flex-1 space-y-8 overflow-auto">
          {/* Upper Teeth */}
          <div className="flex flex-col items-center space-y-4">
            <h4 className={`font-medium text-muted-foreground ${isFullScreen ? 'text-base' : 'text-sm'}`}>
              Arcada Superior
            </h4>
            <div className={`flex items-center ${isFullScreen ? 'space-x-4' : 'space-x-2 md:space-x-3'}`}>
              {upperTeeth?.map((tooth) => (
                <ToothComponent key={tooth?.id} tooth={tooth} isUpper={true} />
              ))}
            </div>
          </div>

          {/* Lower Teeth */}
          <div className="flex flex-col items-center space-y-4">
            <div className={`flex items-center ${isFullScreen ? 'space-x-4' : 'space-x-2 md:space-x-3'}`}>
              {lowerTeeth?.map((tooth) => (
                <ToothComponent key={tooth?.id} tooth={tooth} isUpper={false} />
              ))}
            </div>
            <h4 className={`font-medium text-muted-foreground ${isFullScreen ? 'text-base' : 'text-sm'}`}>
              Arcada Inferior
            </h4>
          </div>
        </div>

        {/* Treatment Selection Panel */}
        {sessionActive && selectedTeeth?.length > 0 && (
          <div className="mt-6 p-4 bg-primary/5 border border-primary/20 rounded-lg">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-sm font-medium text-card-foreground">
                Aplicar Tratamiento - {selectedTeeth?.length === 1 
                  ? `Diente ${selectedTeeth?.[0]?.number}` 
                  : `${selectedTeeth?.length} dientes seleccionados`
                }
              </h4>
              <Button
                variant="ghost"
                size="xs"
                iconName="X"
                onClick={handleClearSelection}
              />
            </div>

            {selectedTeeth?.length > 1 && (
              <div className="mb-3 p-2 bg-info/10 rounded-md">
                <p className="text-xs text-info">
                  Dientes seleccionados: {selectedTeeth?.map(t => t?.number)?.join(', ')}
                </p>
              </div>
            )}

            <div className="grid grid-cols-2 md:grid-cols-5 gap-2 mb-4">
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

            <div className="mb-4">
              <textarea
                className="w-full h-20 p-2 text-sm border border-border rounded-md bg-background resize-none"
                placeholder="Notas del tratamiento (opcional)..."
                value={treatmentNotes}
                onChange={(e) => setTreatmentNotes(e?.target?.value)}
              />
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
                onClick={handleClearSelection}
              >
                Cancelar
              </Button>
            </div>
          </div>
        )}

        {/* Instructions for inactive session */}
        {!sessionActive && (
          <div className="mt-6 p-4 bg-muted/20 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <Icon name="Info" size={16} color="var(--color-primary)" />
              <span className="text-sm font-medium text-card-foreground">
                Sesión Inactiva
              </span>
            </div>
            <p className="text-sm text-muted-foreground">
              Inicie una sesión de tratamiento para poder editar el odontograma y documentar procedimientos.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default InteractiveOdontogram;