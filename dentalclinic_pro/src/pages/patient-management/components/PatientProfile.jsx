import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Image from '../../../components/AppImage';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const PatientProfile = ({ patient, onUpdate, onScheduleAppointment }) => {
  const [activeTab, setActiveTab] = useState('personal');
  const [isEditing, setIsEditing] = useState(false);
  const [editedPatient, setEditedPatient] = useState(patient || {});

  const tabs = [
    { id: 'personal', label: 'Información Personal', icon: 'User' },
    { id: 'medical', label: 'Historia Médica', icon: 'FileText' },
    { id: 'insurance', label: 'Seguro', icon: 'Shield' },
    { id: 'appointments', label: 'Citas', icon: 'Calendar' },
    { id: 'treatments', label: 'Tratamientos', icon: 'Activity' }
  ];

  const genderOptions = [
    { value: 'male', label: 'Masculino' },
    { value: 'female', label: 'Femenino' },
    { value: 'other', label: 'Otro' }
  ];

  const bloodTypeOptions = [
    { value: 'A+', label: 'A+' },
    { value: 'A-', label: 'A-' },
    { value: 'B+', label: 'B+' },
    { value: 'B-', label: 'B-' },
    { value: 'AB+', label: 'AB+' },
    { value: 'AB-', label: 'AB-' },
    { value: 'O+', label: 'O+' },
    { value: 'O-', label: 'O-' }
  ];

  const handleSave = () => {
    onUpdate(editedPatient);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedPatient(patient);
    setIsEditing(false);
  };

  if (!patient) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center">
        <Icon name="UserPlus" size={64} color="var(--color-muted-foreground)" />
        <h3 className="mt-4 text-xl font-semibold text-foreground">
          Selecciona un Paciente
        </h3>
        <p className="mt-2 text-muted-foreground max-w-md">
          Elige un paciente de la lista para ver y editar su información detallada,
          historial médico y programar citas.
        </p>
      </div>
    );
  }

  const renderPersonalInfo = () => (
    <div className="space-y-6">
      <div className="flex items-start space-x-6">
        <div className="relative">
          <div className="w-24 h-24 rounded-full overflow-hidden bg-muted">
            <Image
              src={patient?.avatar}
              alt={`${patient?.firstName} ${patient?.lastName}`}
              className="w-full h-full object-cover"
            />
          </div>
          {isEditing && (
            <Button
              variant="outline"
              className="absolute -bottom-2 -right-2 w-8 h-8 p-0"
            >
              <Icon name="Camera" size={16} />
            </Button>
          )}
        </div>

        <div className="flex-1 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Nombre"
              value={isEditing ? editedPatient?.firstName : patient?.firstName}
              onChange={(e) => setEditedPatient({...editedPatient, firstName: e?.target?.value})}
              disabled={!isEditing}
            />
            <Input
              label="Apellidos"
              value={isEditing ? editedPatient?.lastName : patient?.lastName}
              onChange={(e) => setEditedPatient({...editedPatient, lastName: e?.target?.value})}
              disabled={!isEditing}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Fecha de Nacimiento"
              type="date"
              value={isEditing ? editedPatient?.birthDate : patient?.birthDate}
              onChange={(e) => setEditedPatient({...editedPatient, birthDate: e?.target?.value})}
              disabled={!isEditing}
            />
            <Select
              label="Género"
              options={genderOptions}
              value={isEditing ? editedPatient?.gender : patient?.gender}
              onChange={(value) => setEditedPatient({...editedPatient, gender: value})}
              disabled={!isEditing}
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Teléfono"
          type="tel"
          value={isEditing ? editedPatient?.phone : patient?.phone}
          onChange={(e) => setEditedPatient({...editedPatient, phone: e?.target?.value})}
          disabled={!isEditing}
        />
        <Input
          label="Email"
          type="email"
          value={isEditing ? editedPatient?.email : patient?.email}
          onChange={(e) => setEditedPatient({...editedPatient, email: e?.target?.value})}
          disabled={!isEditing}
        />
      </div>

      <Input
        label="Dirección"
        value={isEditing ? editedPatient?.address : patient?.address}
        onChange={(e) => setEditedPatient({...editedPatient, address: e?.target?.value})}
        disabled={!isEditing}
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          label="Ciudad"
          value={isEditing ? editedPatient?.city : patient?.city}
          onChange={(e) => setEditedPatient({...editedPatient, city: e?.target?.value})}
          disabled={!isEditing}
        />
        <Input
          label="Código Postal"
          value={isEditing ? editedPatient?.postalCode : patient?.postalCode}
          onChange={(e) => setEditedPatient({...editedPatient, postalCode: e?.target?.value})}
          disabled={!isEditing}
        />
        <Input
          label="Provincia"
          value={isEditing ? editedPatient?.province : patient?.province}
          onChange={(e) => setEditedPatient({...editedPatient, province: e?.target?.value})}
          disabled={!isEditing}
        />
      </div>
    </div>
  );

  const renderMedicalHistory = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label="Tipo de Sangre"
          options={bloodTypeOptions}
          value={isEditing ? editedPatient?.bloodType : patient?.bloodType}
          onChange={(value) => setEditedPatient({...editedPatient, bloodType: value})}
          disabled={!isEditing}
        />
        <Input
          label="Alergias"
          value={isEditing ? editedPatient?.allergies : patient?.allergies}
          onChange={(e) => setEditedPatient({...editedPatient, allergies: e?.target?.value})}
          disabled={!isEditing}
          placeholder="Ej: Penicilina, Látex"
        />
      </div>

      <div className="space-y-4">
        <h4 className="text-sm font-semibold text-foreground">Condiciones Médicas</h4>
        <div className="bg-muted/30 rounded-lg p-4">
          <div className="space-y-2">
            {patient?.medicalConditions?.map((condition, index) => (
              <div key={index} className="flex items-center justify-between p-2 bg-card rounded border border-border">
                <span className="text-sm text-foreground">{condition?.name}</span>
                <span className="text-xs text-muted-foreground">{condition?.date}</span>
              </div>
            )) || (
              <p className="text-sm text-muted-foreground">No hay condiciones médicas registradas</p>
            )}
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h4 className="text-sm font-semibold text-foreground">Medicamentos Actuales</h4>
        <div className="bg-muted/30 rounded-lg p-4">
          <div className="space-y-2">
            {patient?.medications?.map((medication, index) => (
              <div key={index} className="flex items-center justify-between p-2 bg-card rounded border border-border">
                <div>
                  <span className="text-sm font-medium text-foreground">{medication?.name}</span>
                  <p className="text-xs text-muted-foreground">{medication?.dosage}</p>
                </div>
                <span className="text-xs text-muted-foreground">{medication?.frequency}</span>
              </div>
            )) || (
              <p className="text-sm text-muted-foreground">No hay medicamentos registrados</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const renderInsuranceInfo = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Compañía de Seguros"
          value={isEditing ? editedPatient?.insuranceCompany : patient?.insuranceCompany}
          onChange={(e) => setEditedPatient({...editedPatient, insuranceCompany: e?.target?.value})}
          disabled={!isEditing}
        />
        <Input
          label="Número de Póliza"
          value={isEditing ? editedPatient?.policyNumber : patient?.policyNumber}
          onChange={(e) => setEditedPatient({...editedPatient, policyNumber: e?.target?.value})}
          disabled={!isEditing}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Fecha de Vencimiento"
          type="date"
          value={isEditing ? editedPatient?.insuranceExpiry : patient?.insuranceExpiry}
          onChange={(e) => setEditedPatient({...editedPatient, insuranceExpiry: e?.target?.value})}
          disabled={!isEditing}
        />
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${
            patient?.insuranceStatus === 'verified' ? 'bg-accent' : 
            patient?.insuranceStatus === 'pending' ? 'bg-warning' : 'bg-error'
          }`} />
          <span className="text-sm text-foreground">
            {patient?.insuranceStatus === 'verified' ? 'Verificado' :
             patient?.insuranceStatus === 'pending' ? 'Pendiente' : 'No verificado'}
          </span>
        </div>
      </div>

      <div className="bg-muted/30 rounded-lg p-4">
        <h4 className="text-sm font-semibold text-foreground mb-3">Cobertura</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Consultas:</span>
              <span className="text-sm text-foreground">{patient?.coverage?.consultations || '100%'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Limpiezas:</span>
              <span className="text-sm text-foreground">{patient?.coverage?.cleanings || '80%'}</span>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Empastes:</span>
              <span className="text-sm text-foreground">{patient?.coverage?.fillings || '70%'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Cirugías:</span>
              <span className="text-sm text-foreground">{patient?.coverage?.surgeries || '50%'}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAppointments = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-foreground">Historial de Citas</h4>
        <Button
          variant="default"
          onClick={() => onScheduleAppointment(patient)}
          iconName="Plus"
          iconPosition="left"
          className="text-sm"
        >
          Nueva Cita
        </Button>
      </div>

      <div className="space-y-3">
        {patient?.appointments?.map((appointment, index) => (
          <div key={index} className="p-4 bg-card border border-border rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${
                  appointment?.status === 'completed' ? 'bg-accent' :
                  appointment?.status === 'scheduled' ? 'bg-warning' :
                  appointment?.status === 'cancelled' ? 'bg-error' : 'bg-muted'
                }`} />
                <div>
                  <p className="text-sm font-medium text-foreground">{appointment?.type}</p>
                  <p className="text-xs text-muted-foreground">
                    {appointment?.date} - {appointment?.time}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-foreground">{appointment?.dentist}</p>
                <p className="text-xs text-muted-foreground">
                  {appointment?.status === 'completed' ? 'Completada' :
                   appointment?.status === 'scheduled' ? 'Programada' :
                   appointment?.status === 'cancelled' ? 'Cancelada' : 'Pendiente'}
                </p>
              </div>
            </div>
            {appointment?.notes && (
              <p className="mt-2 text-xs text-muted-foreground">{appointment?.notes}</p>
            )}
          </div>
        )) || (
          <p className="text-sm text-muted-foreground text-center py-8">
            No hay citas registradas para este paciente
          </p>
        )}
      </div>
    </div>
  );

  const renderTreatments = () => (
    <div className="space-y-6">
      <h4 className="text-sm font-semibold text-foreground">Plan de Tratamiento</h4>
      
      <div className="space-y-3">
        {patient?.treatments?.map((treatment, index) => (
          <div key={index} className="p-4 bg-card border border-border rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-foreground">{treatment?.name}</p>
                <p className="text-xs text-muted-foreground">
                  Diente: {treatment?.tooth} | Fecha: {treatment?.date}
                </p>
              </div>
              <div className="text-right">
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                  treatment?.status === 'completed' ? 'bg-accent/20 text-accent' :
                  treatment?.status === 'in-progress' ? 'bg-warning/20 text-warning' :
                  treatment?.status === 'planned' ? 'bg-primary/20 text-primary' : 'bg-muted/20 text-muted-foreground'
                }`}>
                  {treatment?.status === 'completed' ? 'Completado' :
                   treatment?.status === 'in-progress' ? 'En Progreso' :
                   treatment?.status === 'planned' ? 'Planificado' : 'Pendiente'}
                </span>
              </div>
            </div>
            {treatment?.notes && (
              <p className="mt-2 text-xs text-muted-foreground">{treatment?.notes}</p>
            )}
          </div>
        )) || (
          <p className="text-sm text-muted-foreground text-center py-8">
            No hay tratamientos registrados para este paciente
          </p>
        )}
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'personal':
        return renderPersonalInfo();
      case 'medical':
        return renderMedicalHistory();
      case 'insurance':
        return renderInsuranceInfo();
      case 'appointments':
        return renderAppointments();
      case 'treatments':
        return renderTreatments();
      default:
        return renderPersonalInfo();
    }
  };

  return (
    <div className="bg-card border border-border rounded-lg h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">
              {patient?.firstName} {patient?.lastName}
            </h2>
            <p className="text-sm text-muted-foreground">
              ID: {patient?.id} | Última visita: {patient?.lastVisit}
            </p>
          </div>
          <div className="flex items-center space-x-2">
            {isEditing ? (
              <>
                <Button variant="outline" onClick={handleCancel}>
                  Cancelar
                </Button>
                <Button variant="default" onClick={handleSave}>
                  Guardar
                </Button>
              </>
            ) : (
              <Button
                variant="outline"
                onClick={() => setIsEditing(true)}
                iconName="Edit"
                iconPosition="left"
              >
                Editar
              </Button>
            )}
          </div>
        </div>
      </div>
      {/* Tabs */}
      <div className="border-b border-border">
        <nav className="flex space-x-8 px-6">
          {tabs?.map((tab) => (
            <button
              key={tab?.id}
              onClick={() => setActiveTab(tab?.id)}
              className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-150 ${
                activeTab === tab?.id
                  ? 'border-primary text-primary' :'border-transparent text-muted-foreground hover:text-foreground hover:border-muted'
              }`}
            >
              <Icon name={tab?.icon} size={16} />
              <span>{tab?.label}</span>
            </button>
          ))}
        </nav>
      </div>
      {/* Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default PatientProfile;