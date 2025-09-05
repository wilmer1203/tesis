import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const AppointmentModal = ({ 
  isOpen, 
  onClose, 
  appointment = null, 
  dentists, 
  patients,
  onSave 
}) => {
  const [formData, setFormData] = useState({
    patientId: appointment?.patientId || '',
    dentistId: appointment?.dentistId || '',
    date: appointment?.date || new Date()?.toISOString()?.split('T')?.[0],
    time: appointment?.time || '09:00',
    duration: appointment?.duration || 30,
    service: appointment?.service || '',
    type: appointment?.type || 'consultation',
    notes: appointment?.notes || '',
    status: appointment?.status || 'pending'
  });

  const serviceOptions = [
    { value: 'consultation', label: 'Consulta General' },
    { value: 'cleaning', label: 'Limpieza Dental' },
    { value: 'filling', label: 'Empaste' },
    { value: 'extraction', label: 'Extracción' },
    { value: 'root_canal', label: 'Endodoncia' },
    { value: 'crown', label: 'Corona' },
    { value: 'orthodontics', label: 'Ortodoncia' },
    { value: 'whitening', label: 'Blanqueamiento' },
    { value: 'implant', label: 'Implante' },
    { value: 'emergency', label: 'Emergencia' }
  ];

  const typeOptions = [
    { value: 'consultation', label: 'Consulta' },
    { value: 'treatment', label: 'Tratamiento' },
    { value: 'followup', label: 'Seguimiento' },
    { value: 'emergency', label: 'Emergencia' },
    { value: 'cleaning', label: 'Limpieza' }
  ];

  const statusOptions = [
    { value: 'pending', label: 'Pendiente' },
    { value: 'confirmed', label: 'Confirmada' },
    { value: 'completed', label: 'Completada' },
    { value: 'cancelled', label: 'Cancelada' }
  ];

  const durationOptions = [
    { value: 15, label: '15 minutos' },
    { value: 30, label: '30 minutos' },
    { value: 45, label: '45 minutos' },
    { value: 60, label: '1 hora' },
    { value: 90, label: '1.5 horas' },
    { value: 120, label: '2 horas' }
  ];

  const patientOptions = patients?.map(patient => ({
    value: patient?.id,
    label: `${patient?.name} - ${patient?.phone}`
  }));

  const dentistOptions = dentists?.map(dentist => ({
    value: dentist?.id,
    label: `${dentist?.name} - ${dentist?.specialty}`
  }));

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    onSave(formData);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-surface border border-border rounded-lg shadow-custom-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
              <Icon name="Calendar" size={20} color="var(--color-primary-foreground)" />
            </div>
            <div>
              <h2 className="text-xl font-heading font-semibold text-foreground">
                {appointment ? 'Editar Cita' : 'Nueva Cita'}
              </h2>
              <p className="text-sm text-muted-foreground">
                {appointment ? 'Modificar los detalles de la cita' : 'Programar una nueva cita médica'}
              </p>
            </div>
          </div>
          
          <Button
            variant="ghost"
            onClick={onClose}
            iconName="X"
            iconSize={20}
            className="p-2"
          />
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Patient and Dentist Selection */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label="Paciente"
              required
              searchable
              options={patientOptions}
              value={formData?.patientId}
              onChange={(value) => handleInputChange('patientId', value)}
              placeholder="Seleccionar paciente"
            />
            
            <Select
              label="Dentista"
              required
              options={dentistOptions}
              value={formData?.dentistId}
              onChange={(value) => handleInputChange('dentistId', value)}
              placeholder="Seleccionar dentista"
            />
          </div>

          {/* Date and Time */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input
              label="Fecha"
              type="date"
              required
              value={formData?.date}
              onChange={(e) => handleInputChange('date', e?.target?.value)}
            />
            
            <Input
              label="Hora"
              type="time"
              required
              value={formData?.time}
              onChange={(e) => handleInputChange('time', e?.target?.value)}
            />
            
            <Select
              label="Duración"
              required
              options={durationOptions}
              value={formData?.duration}
              onChange={(value) => handleInputChange('duration', value)}
            />
          </div>

          {/* Service and Type */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label="Servicio"
              required
              searchable
              options={serviceOptions}
              value={formData?.service}
              onChange={(value) => handleInputChange('service', value)}
              placeholder="Seleccionar servicio"
            />
            
            <Select
              label="Tipo de Cita"
              required
              options={typeOptions}
              value={formData?.type}
              onChange={(value) => handleInputChange('type', value)}
            />
          </div>

          {/* Status */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label="Estado"
              required
              options={statusOptions}
              value={formData?.status}
              onChange={(value) => handleInputChange('status', value)}
            />
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Notas Adicionales
            </label>
            <textarea
              value={formData?.notes}
              onChange={(e) => handleInputChange('notes', e?.target?.value)}
              placeholder="Agregar notas sobre la cita, instrucciones especiales, etc."
              rows={4}
              className="w-full px-3 py-2 bg-input border border-border rounded-md text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-none"
            />
          </div>

          {/* Patient Info Preview */}
          {formData?.patientId && (
            <div className="bg-card p-4 rounded-lg border border-border">
              <h4 className="font-medium text-card-foreground mb-2">Información del Paciente</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Teléfono:</span>
                  <span className="ml-2 text-card-foreground">+34 612 345 678</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Email:</span>
                  <span className="ml-2 text-card-foreground">paciente@email.com</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Última visita:</span>
                  <span className="ml-2 text-card-foreground">15/07/2024</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Alergias:</span>
                  <span className="ml-2 text-card-foreground">Penicilina</span>
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-border">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
            >
              Cancelar
            </Button>
            
            {appointment && (
              <Button
                type="button"
                variant="destructive"
                iconName="Trash2"
                iconPosition="left"
                iconSize={16}
              >
                Eliminar
              </Button>
            )}
            
            <Button
              type="submit"
              variant="default"
              iconName="Save"
              iconPosition="left"
              iconSize={16}
            >
              {appointment ? 'Actualizar Cita' : 'Crear Cita'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AppointmentModal;