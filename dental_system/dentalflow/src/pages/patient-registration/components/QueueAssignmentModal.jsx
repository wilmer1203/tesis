import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Select from '../../../components/ui/Select';
import Input from '../../../components/ui/Input';

const QueueAssignmentModal = ({ 
  isOpen, 
  onClose, 
  patient, 
  onAssign 
}) => {
  const [selectedDentist, setSelectedDentist] = useState('');
  const [priority, setPriority] = useState('normal');
  const [notes, setNotes] = useState('');
  const [isAssigning, setIsAssigning] = useState(false);
  const [dentists, setDentists] = useState([]);

  // Mock dentists data
  const mockDentists = [
    {
      id: 'D001',
      name: 'Dr. María González',
      specialty: 'Odontología General',
      currentQueue: 3,
      estimatedWait: 45,
      status: 'available',
      avatar: '/assets/images/dentist-1.jpg'
    },
    {
      id: 'D002',
      name: 'Dr. Carlos Rodríguez',
      specialty: 'Endodoncia',
      currentQueue: 1,
      estimatedWait: 20,
      status: 'available',
      avatar: '/assets/images/dentist-2.jpg'
    },
    {
      id: 'D003',
      name: 'Dra. Ana Martínez',
      specialty: 'Ortodoncia',
      currentQueue: 5,
      estimatedWait: 75,
      status: 'busy',
      avatar: '/assets/images/dentist-3.jpg'
    },
    {
      id: 'D004',
      name: 'Dr. José Hernández',
      specialty: 'Cirugía Oral',
      currentQueue: 2,
      estimatedWait: 30,
      status: 'available',
      avatar: '/assets/images/dentist-4.jpg'
    }
  ];

  const priorityOptions = [
    { value: 'low', label: 'Baja - Consulta de rutina' },
    { value: 'normal', label: 'Normal - Consulta estándar' },
    { value: 'high', label: 'Alta - Dolor o molestia' },
    { value: 'urgent', label: 'Urgente - Emergencia dental' }
  ];

  useEffect(() => {
    if (isOpen) {
      setDentists(mockDentists);
      setSelectedDentist('');
      setPriority('normal');
      setNotes('');
    }
  }, [isOpen]);

  const handleAssign = async () => {
    if (!selectedDentist) return;

    setIsAssigning(true);
    
    try {
      const selectedDentistData = dentists?.find(d => d?.id === selectedDentist);
      const assignmentData = {
        patient,
        dentist: selectedDentistData,
        priority,
        notes,
        assignedAt: new Date(),
        estimatedPosition: selectedDentistData?.currentQueue + 1,
        estimatedWait: selectedDentistData?.estimatedWait + (selectedDentistData?.currentQueue * 15)
      };

      if (onAssign) {
        await onAssign(assignmentData);
      }
      
      onClose();
    } catch (error) {
      console.error('Error assigning to queue:', error);
    } finally {
      setIsAssigning(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'available':
        return 'text-success';
      case 'busy':
        return 'text-warning';
      case 'unavailable':
        return 'text-error';
      default:
        return 'text-muted-foreground';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent':
        return 'text-error';
      case 'high':
        return 'text-warning';
      case 'normal':
        return 'text-primary';
      case 'low':
        return 'text-muted-foreground';
      default:
        return 'text-muted-foreground';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      {/* Modal */}
      <div className="relative bg-card border border-border rounded-lg shadow-modal w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <div>
            <h2 className="text-xl font-semibold text-foreground">Asignar a Cola</h2>
            {patient && (
              <p className="text-sm text-muted-foreground mt-1">
                Paciente: {patient?.name} ({patient?.id})
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-muted rounded-md transition-smooth"
          >
            <Icon name="X" size={20} className="text-muted-foreground" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Patient Summary */}
          {patient && (
            <div className="bg-muted rounded-lg p-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                  <Icon name="User" size={24} className="text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="font-medium text-foreground">{patient?.name}</h3>
                  <div className="grid grid-cols-2 gap-2 text-sm text-muted-foreground mt-1">
                    <span>Edad: {patient?.age} años</span>
                    <span>Tel: {patient?.phone}</span>
                    <span>Seguro: {patient?.insurance}</span>
                    <span>Moneda: {patient?.preferredCurrency}</span>
                  </div>
                  {patient?.allergies && patient?.allergies?.length > 0 && (
                    <div className="flex items-center space-x-1 mt-2">
                      <Icon name="AlertTriangle" size={14} className="text-warning" />
                      <span className="text-xs text-warning">
                        Alergias: {patient?.allergies?.join(', ')}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Dentist Selection */}
          <div>
            <h3 className="text-lg font-medium text-foreground mb-4">Seleccionar Dentista</h3>
            <div className="grid gap-3">
              {dentists?.map((dentist) => (
                <div
                  key={dentist?.id}
                  className={`border border-border rounded-lg p-4 cursor-pointer transition-smooth hover:bg-muted ${
                    selectedDentist === dentist?.id ? 'bg-primary/5 border-primary' : ''
                  } ${dentist?.status === 'unavailable' ? 'opacity-50 cursor-not-allowed' : ''}`}
                  onClick={() => {
                    if (dentist?.status !== 'unavailable') {
                      setSelectedDentist(dentist?.id);
                    }
                  }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-secondary/10 rounded-full flex items-center justify-center">
                        <Icon name="UserCheck" size={20} className="text-secondary" />
                      </div>
                      <div>
                        <h4 className="font-medium text-foreground">{dentist?.name}</h4>
                        <p className="text-sm text-muted-foreground">{dentist?.specialty}</p>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className={`flex items-center space-x-1 ${getStatusColor(dentist?.status)}`}>
                        <div className={`w-2 h-2 rounded-full ${
                          dentist?.status === 'available' ? 'bg-success' : 
                          dentist?.status === 'busy' ? 'bg-warning' : 'bg-error'
                        }`}></div>
                        <span className="text-xs font-medium capitalize">{dentist?.status}</span>
                      </div>
                      <div className="text-sm text-muted-foreground mt-1">
                        Cola: {dentist?.currentQueue} • {dentist?.estimatedWait} min
                      </div>
                    </div>
                  </div>
                  
                  {selectedDentist === dentist?.id && (
                    <div className="mt-3 pt-3 border-t border-border">
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-muted-foreground">Posición estimada:</span>
                          <span className="ml-2 font-medium text-foreground">
                            #{dentist?.currentQueue + 1}
                          </span>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Tiempo estimado:</span>
                          <span className="ml-2 font-medium text-foreground">
                            {dentist?.estimatedWait + (dentist?.currentQueue * 15)} min
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Priority Selection */}
          <div>
            <Select
              label="Prioridad"
              options={priorityOptions}
              value={priority}
              onChange={setPriority}
              description="Seleccione la prioridad según la urgencia del caso"
            />
            
            {priority && (
              <div className={`mt-2 text-sm ${getPriorityColor(priority)}`}>
                <Icon name="Info" size={14} className="inline mr-1" />
                {priority === 'urgent' && 'El paciente será atendido con máxima prioridad'}
                {priority === 'high' && 'El paciente será atendido antes que los casos normales'}
                {priority === 'normal' && 'El paciente será atendido en orden de llegada'}
                {priority === 'low' && 'El paciente puede esperar más tiempo si hay casos urgentes'}
              </div>
            )}
          </div>

          {/* Notes */}
          <div>
            <Input
              label="Notas Adicionales"
              type="text"
              placeholder="Información adicional para el dentista..."
              value={notes}
              onChange={(e) => setNotes(e?.target?.value)}
              description="Opcional: Información relevante sobre el motivo de la consulta"
            />
          </div>

          {/* Queue Summary */}
          {selectedDentist && (
            <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
              <h4 className="font-medium text-foreground mb-2">Resumen de Asignación</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Dentista:</span>
                  <span className="ml-2 text-foreground">
                    {dentists?.find(d => d?.id === selectedDentist)?.name}
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Especialidad:</span>
                  <span className="ml-2 text-foreground">
                    {dentists?.find(d => d?.id === selectedDentist)?.specialty}
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Posición en cola:</span>
                  <span className="ml-2 font-medium text-foreground">
                    #{(dentists?.find(d => d?.id === selectedDentist)?.currentQueue || 0) + 1}
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Tiempo estimado:</span>
                  <span className="ml-2 font-medium text-foreground">
                    {((dentists?.find(d => d?.id === selectedDentist)?.estimatedWait || 0) + 
                      ((dentists?.find(d => d?.id === selectedDentist)?.currentQueue || 0) * 15))} min
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end space-x-4 p-6 border-t border-border">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={isAssigning}
          >
            Cancelar
          </Button>
          
          <Button
            variant="primary"
            onClick={handleAssign}
            loading={isAssigning}
            disabled={!selectedDentist}
            iconName="Clock"
            iconPosition="left"
          >
            Asignar a Cola
          </Button>
        </div>
      </div>
    </div>
  );
};

export default QueueAssignmentModal;