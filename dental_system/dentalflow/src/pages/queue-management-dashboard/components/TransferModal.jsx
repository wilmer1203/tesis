import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Select from '../../../components/ui/Select';
import Input from '../../../components/ui/Input';

const TransferModal = ({ 
  isOpen, 
  onClose, 
  patient, 
  dentists, 
  currentDentistId, 
  onConfirmTransfer 
}) => {
  const [selectedDentist, setSelectedDentist] = useState('');
  const [justification, setJustification] = useState('');
  const [priority, setPriority] = useState('normal');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen || !patient) return null;

  const availableDentists = dentists?.filter(d => d?.id !== currentDentistId && d?.status !== 'unavailable')?.map(d => ({
      value: d?.id,
      label: `${d?.name} - ${d?.specialty}`,
      description: `${d?.queueLength} pacientes en cola • ~${d?.estimatedWaitTime}m espera`
    }));

  const priorityOptions = [
    { value: 'normal', label: 'Normal' },
    { value: 'high', label: 'Alta Prioridad' },
    { value: 'urgent', label: 'Urgente' }
  ];

  const handleSubmit = async (e) => {
    e?.preventDefault();
    if (!selectedDentist || !justification?.trim()) return;

    setIsSubmitting(true);
    try {
      await onConfirmTransfer({
        patientId: patient?.id,
        fromDentistId: currentDentistId,
        toDentistId: selectedDentist,
        justification: justification?.trim(),
        priority,
        timestamp: new Date()?.toISOString()
      });
      handleClose();
    } catch (error) {
      console.error('Transfer failed:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setSelectedDentist('');
    setJustification('');
    setPriority('normal');
    setIsSubmitting(false);
    onClose();
  };

  const selectedDentistInfo = dentists?.find(d => d?.id === selectedDentist);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-card border border-border rounded-lg shadow-modal w-full max-w-md max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <h2 className="text-lg font-semibold text-foreground">Transferir Paciente</h2>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-muted rounded-md transition-smooth"
            disabled={isSubmitting}
          >
            <Icon name="X" size={20} className="text-muted-foreground" />
          </button>
        </div>

        {/* Content */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Patient Info */}
          <div className="bg-muted rounded-md p-4">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                <Icon name="User" size={20} className="text-primary" />
              </div>
              <div>
                <div className="font-medium text-foreground">{patient?.name}</div>
                <div className="text-sm text-muted-foreground">
                  {patient?.id} • {patient?.service}
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-muted-foreground">Edad:</span>
                <span className="ml-1 text-foreground">{patient?.age} años</span>
              </div>
              <div>
                <span className="text-muted-foreground">Espera:</span>
                <span className="ml-1 text-foreground">{patient?.waitTime}m</span>
              </div>
            </div>
          </div>

          {/* Destination Dentist */}
          <div>
            <Select
              label="Dentista de Destino"
              description="Seleccione el dentista que recibirá al paciente"
              options={availableDentists}
              value={selectedDentist}
              onChange={setSelectedDentist}
              required
              searchable
            />
            
            {selectedDentistInfo && (
              <div className="mt-3 bg-muted rounded-md p-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Estado:</span>
                  <span className={`font-medium ${
                    selectedDentistInfo?.status === 'available' ? 'text-success' : 'text-warning'
                  }`}>
                    {selectedDentistInfo?.status === 'available' ? 'Disponible' : 'Ocupado'}
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm mt-1">
                  <span className="text-muted-foreground">Cola actual:</span>
                  <span className="text-foreground">{selectedDentistInfo?.queueLength} pacientes</span>
                </div>
                <div className="flex items-center justify-between text-sm mt-1">
                  <span className="text-muted-foreground">Tiempo estimado:</span>
                  <span className="text-foreground">~{selectedDentistInfo?.estimatedWaitTime}m</span>
                </div>
              </div>
            )}
          </div>

          {/* Priority */}
          <div>
            <Select
              label="Prioridad en Nueva Cola"
              options={priorityOptions}
              value={priority}
              onChange={setPriority}
            />
          </div>

          {/* Justification */}
          <div>
            <Input
              label="Justificación"
              description="Explique el motivo de la transferencia"
              type="text"
              value={justification}
              onChange={(e) => setJustification(e?.target?.value)}
              placeholder="Ej: Especialidad requerida, reducir tiempo de espera..."
              required
              minLength={10}
            />
          </div>

          {/* Actions */}
          <div className="flex space-x-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isSubmitting}
              className="flex-1"
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              loading={isSubmitting}
              disabled={!selectedDentist || !justification?.trim()}
              className="flex-1"
            >
              Confirmar Transferencia
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TransferModal;