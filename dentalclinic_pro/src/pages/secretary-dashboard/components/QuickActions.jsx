import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const QuickActions = () => {
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  const [appointmentForm, setAppointmentForm] = useState({
    patient: '',
    dentist: '',
    date: '',
    time: '',
    treatment: '',
    duration: '30',
    notes: ''
  });

  const dentistOptions = [
    { value: '', label: 'Seleccionar dentista' },
    { value: 'dr-rodriguez', label: 'Dr. Rodríguez' },
    { value: 'dr-lopez', label: 'Dr. López' },
    { value: 'dr-martinez', label: 'Dr. Martínez' }
  ];

  const treatmentOptions = [
    { value: '', label: 'Seleccionar tratamiento' },
    { value: 'cleaning', label: 'Limpieza dental' },
    { value: 'filling', label: 'Empaste' },
    { value: 'extraction', label: 'Extracción' },
    { value: 'checkup', label: 'Revisión' },
    { value: 'orthodontics', label: 'Ortodoncia' },
    { value: 'implant', label: 'Implante' },
    { value: 'root-canal', label: 'Endodoncia' }
  ];

  const durationOptions = [
    { value: '15', label: '15 minutos' },
    { value: '30', label: '30 minutos' },
    { value: '45', label: '45 minutos' },
    { value: '60', label: '60 minutos' },
    { value: '90', label: '90 minutos' },
    { value: '120', label: '120 minutos' }
  ];

  const quickStats = [
    {
      label: 'Citas Hoy',
      value: '12',
      icon: 'Calendar',
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/20'
    },
    {
      label: 'Pacientes Nuevos',
      value: '3',
      icon: 'UserPlus',
      color: 'text-green-400',
      bgColor: 'bg-green-500/20'
    },
    {
      label: 'Pagos Pendientes',
      value: '€525',
      icon: 'CreditCard',
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/20'
    },
    {
      label: 'Sala de Espera',
      value: '2',
      icon: 'Users',
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/20'
    }
  ];

  const upcomingAppointments = [
    {
      time: '14:30',
      patient: 'Laura Sánchez',
      dentist: 'Dr. Rodríguez',
      treatment: 'Ortodoncia'
    },
    {
      time: '15:00',
      patient: 'Miguel Torres',
      dentist: 'Dr. López',
      treatment: 'Implante'
    },
    {
      time: '15:30',
      patient: 'Carmen Ruiz',
      dentist: 'Dr. Martínez',
      treatment: 'Limpieza'
    }
  ];

  const handleFormChange = (field, value) => {
    setAppointmentForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmitAppointment = (e) => {
    e?.preventDefault();
    console.log('Nueva cita:', appointmentForm);
    setShowAppointmentForm(false);
    setAppointmentForm({
      patient: '',
      dentist: '',
      date: '',
      time: '',
      treatment: '',
      duration: '30',
      notes: ''
    });
  };

  const navigateToPage = (path) => {
    window.location.href = path;
  };

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      <div className="bg-surface rounded-lg border border-border shadow-custom-md p-4">
        <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <Icon name="BarChart3" size={20} className="mr-2" />
          Resumen del Día
        </h2>
        <div className="grid grid-cols-2 gap-3">
          {quickStats?.map((stat, index) => (
            <div key={index} className="p-3 bg-card rounded-lg border border-border">
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 ${stat?.bgColor} rounded-lg flex items-center justify-center`}>
                  <Icon name={stat?.icon} size={18} color={`var(--color-${stat?.color?.split('-')?.[1]}-400)`} />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">{stat?.label}</p>
                  <p className="text-lg font-semibold text-foreground">{stat?.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      {/* Quick Actions */}
      <div className="bg-surface rounded-lg border border-border shadow-custom-md p-4">
        <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <Icon name="Zap" size={20} className="mr-2" />
          Acciones Rápidas
        </h2>
        <div className="space-y-3">
          <Button
            variant="default"
            fullWidth
            iconName="UserPlus"
            iconPosition="left"
            onClick={() => navigateToPage('/patient-management')}
            className="justify-start"
          >
            Registrar Nuevo Paciente
          </Button>
          <Button
            variant="outline"
            fullWidth
            iconName="Calendar"
            iconPosition="left"
            onClick={() => setShowAppointmentForm(!showAppointmentForm)}
            className="justify-start"
          >
            Programar Cita
          </Button>
          <Button
            variant="outline"
            fullWidth
            iconName="CreditCard"
            iconPosition="left"
            onClick={() => navigateToPage('/payment-processing')}
            className="justify-start"
          >
            Procesar Pago
          </Button>
          <Button
            variant="outline"
            fullWidth
            iconName="Search"
            iconPosition="left"
            onClick={() => navigateToPage('/patient-management')}
            className="justify-start"
          >
            Buscar Paciente
          </Button>
        </div>
      </div>
      {/* Quick Appointment Form */}
      {showAppointmentForm && (
        <div className="bg-surface rounded-lg border border-border shadow-custom-md p-4">
          <h3 className="text-md font-semibold text-foreground mb-4 flex items-center">
            <Icon name="Calendar" size={18} className="mr-2" />
            Nueva Cita Rápida
          </h3>
          <form onSubmit={handleSubmitAppointment} className="space-y-4">
            <Input
              label="Paciente"
              type="text"
              placeholder="Nombre del paciente"
              value={appointmentForm?.patient}
              onChange={(e) => handleFormChange('patient', e?.target?.value)}
              required
            />
            <Select
              label="Dentista"
              options={dentistOptions}
              value={appointmentForm?.dentist}
              onChange={(value) => handleFormChange('dentist', value)}
              required
            />
            <div className="grid grid-cols-2 gap-3">
              <Input
                label="Fecha"
                type="date"
                value={appointmentForm?.date}
                onChange={(e) => handleFormChange('date', e?.target?.value)}
                required
              />
              <Input
                label="Hora"
                type="time"
                value={appointmentForm?.time}
                onChange={(e) => handleFormChange('time', e?.target?.value)}
                required
              />
            </div>
            <Select
              label="Tratamiento"
              options={treatmentOptions}
              value={appointmentForm?.treatment}
              onChange={(value) => handleFormChange('treatment', value)}
              required
            />
            <Select
              label="Duración"
              options={durationOptions}
              value={appointmentForm?.duration}
              onChange={(value) => handleFormChange('duration', value)}
            />
            <Input
              label="Notas"
              type="text"
              placeholder="Notas adicionales (opcional)"
              value={appointmentForm?.notes}
              onChange={(e) => handleFormChange('notes', e?.target?.value)}
            />
            <div className="flex items-center space-x-3">
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowAppointmentForm(false)}
                fullWidth
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                iconName="Check"
                iconPosition="left"
                fullWidth
              >
                Programar
              </Button>
            </div>
          </form>
        </div>
      )}
      {/* Upcoming Appointments */}
      <div className="bg-surface rounded-lg border border-border shadow-custom-md p-4">
        <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <Icon name="Clock" size={20} className="mr-2" />
          Próximas Citas
        </h2>
        <div className="space-y-3">
          {upcomingAppointments?.map((appointment, index) => (
            <div key={index} className="p-3 bg-card rounded-lg border border-border">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center space-x-3">
                    <span className="text-sm font-mono text-primary font-medium">
                      {appointment?.time}
                    </span>
                    <span className="text-sm font-medium text-foreground">
                      {appointment?.patient}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    {appointment?.treatment} • {appointment?.dentist}
                  </p>
                </div>
                <Button variant="ghost" className="p-2">
                  <Icon name="MoreVertical" size={16} />
                </Button>
              </div>
            </div>
          ))}
          {upcomingAppointments?.length === 0 && (
            <p className="text-center text-muted-foreground py-4">
              No hay más citas programadas para hoy
            </p>
          )}
        </div>
        <div className="mt-4">
          <Button
            variant="outline"
            fullWidth
            iconName="Calendar"
            iconPosition="left"
            onClick={() => navigateToPage('/appointment-scheduling')}
          >
            Ver Agenda Completa
          </Button>
        </div>
      </div>
    </div>
  );
};

export default QuickActions;