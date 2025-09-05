import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const PatientRegistration = () => {
  const [isNewPatient, setIsNewPatient] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    dni: '',
    phone: '',
    email: '',
    birthDate: '',
    address: '',
    city: '',
    postalCode: '',
    insuranceProvider: '',
    insuranceNumber: '',
    emergencyContact: '',
    emergencyPhone: '',
    allergies: '',
    medications: '',
    medicalHistory: ''
  });

  const [searchResults] = useState([
    {
      id: 1,
      name: "María González Pérez",
      dni: "12345678A",
      phone: "+34 612 345 678",
      email: "maria.gonzalez@email.com",
      lastVisit: "2024-07-15"
    },
    {
      id: 2,
      name: "Carlos Martín López",
      dni: "87654321B",
      phone: "+34 623 456 789",
      email: "carlos.martin@email.com",
      lastVisit: "2024-06-20"
    }
  ]);

  const insuranceOptions = [
    { value: '', label: 'Seleccionar seguro' },
    { value: 'sanitas', label: 'Sanitas' },
    { value: 'adeslas', label: 'Adeslas' },
    { value: 'mapfre', label: 'Mapfre Salud' },
    { value: 'dkv', label: 'DKV Seguros' },
    { value: 'asisa', label: 'Asisa' },
    { value: 'particular', label: 'Particular (sin seguro)' }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    console.log('Registrando paciente:', formData);
  };

  const handlePatientSelect = (patient) => {
    setFormData({
      firstName: patient?.name?.split(' ')?.[0],
      lastName: patient?.name?.split(' ')?.slice(1)?.join(' '),
      dni: patient?.dni,
      phone: patient?.phone,
      email: patient?.email,
      birthDate: '',
      address: '',
      city: '',
      postalCode: '',
      insuranceProvider: '',
      insuranceNumber: '',
      emergencyContact: '',
      emergencyPhone: '',
      allergies: '',
      medications: '',
      medicalHistory: ''
    });
    setIsNewPatient(false);
  };

  const filteredResults = searchResults?.filter(patient =>
    patient?.name?.toLowerCase()?.includes(searchQuery?.toLowerCase()) ||
    patient?.dni?.toLowerCase()?.includes(searchQuery?.toLowerCase()) ||
    patient?.phone?.includes(searchQuery)
  );

  return (
    <div className="bg-surface rounded-lg border border-border shadow-custom-md h-full">
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Icon name="UserPlus" size={20} color="var(--color-primary)" />
            <h2 className="text-lg font-semibold text-foreground">
              Gestión de Pacientes
            </h2>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant={isNewPatient ? "default" : "outline"}
              onClick={() => setIsNewPatient(true)}
              className="text-sm"
            >
              Nuevo
            </Button>
            <Button
              variant={!isNewPatient ? "default" : "outline"}
              onClick={() => setIsNewPatient(false)}
              className="text-sm"
            >
              Buscar
            </Button>
          </div>
        </div>
      </div>
      <div className="p-4 h-full overflow-y-auto">
        {!isNewPatient && (
          <div className="mb-6">
            <Input
              type="search"
              placeholder="Buscar por nombre, DNI o teléfono..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e?.target?.value)}
              className="mb-4"
            />

            {searchQuery && (
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {filteredResults?.map((patient) => (
                  <div
                    key={patient?.id}
                    className="p-3 border border-border rounded-lg hover:bg-muted/50 cursor-pointer transition-colors duration-200"
                    onClick={() => handlePatientSelect(patient)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-foreground">{patient?.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {patient?.dni} • {patient?.phone}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-muted-foreground">
                          Última visita: {new Date(patient.lastVisit)?.toLocaleDateString('es-ES')}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
                {filteredResults?.length === 0 && searchQuery && (
                  <p className="text-center text-muted-foreground py-4">
                    No se encontraron pacientes
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Nombre"
              type="text"
              placeholder="Nombre del paciente"
              value={formData?.firstName}
              onChange={(e) => handleInputChange('firstName', e?.target?.value)}
              required
            />
            <Input
              label="Apellidos"
              type="text"
              placeholder="Apellidos del paciente"
              value={formData?.lastName}
              onChange={(e) => handleInputChange('lastName', e?.target?.value)}
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="DNI/NIE"
              type="text"
              placeholder="12345678A"
              value={formData?.dni}
              onChange={(e) => handleInputChange('dni', e?.target?.value)}
              required
            />
            <Input
              label="Fecha de Nacimiento"
              type="date"
              value={formData?.birthDate}
              onChange={(e) => handleInputChange('birthDate', e?.target?.value)}
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Teléfono"
              type="tel"
              placeholder="+34 612 345 678"
              value={formData?.phone}
              onChange={(e) => handleInputChange('phone', e?.target?.value)}
              required
            />
            <Input
              label="Email"
              type="email"
              placeholder="paciente@email.com"
              value={formData?.email}
              onChange={(e) => handleInputChange('email', e?.target?.value)}
            />
          </div>

          <Input
            label="Dirección"
            type="text"
            placeholder="Calle, número, piso"
            value={formData?.address}
            onChange={(e) => handleInputChange('address', e?.target?.value)}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Ciudad"
              type="text"
              placeholder="Madrid"
              value={formData?.city}
              onChange={(e) => handleInputChange('city', e?.target?.value)}
            />
            <Input
              label="Código Postal"
              type="text"
              placeholder="28001"
              value={formData?.postalCode}
              onChange={(e) => handleInputChange('postalCode', e?.target?.value)}
            />
          </div>

          <div className="border-t border-border pt-4">
            <h3 className="text-sm font-medium text-foreground mb-3">Información del Seguro</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Select
                label="Proveedor de Seguro"
                options={insuranceOptions}
                value={formData?.insuranceProvider}
                onChange={(value) => handleInputChange('insuranceProvider', value)}
              />
              <Input
                label="Número de Póliza"
                type="text"
                placeholder="Número de póliza"
                value={formData?.insuranceNumber}
                onChange={(e) => handleInputChange('insuranceNumber', e?.target?.value)}
              />
            </div>
          </div>

          <div className="border-t border-border pt-4">
            <h3 className="text-sm font-medium text-foreground mb-3">Contacto de Emergencia</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Nombre del Contacto"
                type="text"
                placeholder="Nombre completo"
                value={formData?.emergencyContact}
                onChange={(e) => handleInputChange('emergencyContact', e?.target?.value)}
              />
              <Input
                label="Teléfono de Emergencia"
                type="tel"
                placeholder="+34 612 345 678"
                value={formData?.emergencyPhone}
                onChange={(e) => handleInputChange('emergencyPhone', e?.target?.value)}
              />
            </div>
          </div>

          <div className="border-t border-border pt-4">
            <h3 className="text-sm font-medium text-foreground mb-3">Información Médica</h3>
            <div className="space-y-4">
              <Input
                label="Alergias"
                type="text"
                placeholder="Alergias conocidas"
                value={formData?.allergies}
                onChange={(e) => handleInputChange('allergies', e?.target?.value)}
              />
              <Input
                label="Medicamentos Actuales"
                type="text"
                placeholder="Medicamentos que toma actualmente"
                value={formData?.medications}
                onChange={(e) => handleInputChange('medications', e?.target?.value)}
              />
              <Input
                label="Historial Médico"
                type="text"
                placeholder="Condiciones médicas relevantes"
                value={formData?.medicalHistory}
                onChange={(e) => handleInputChange('medicalHistory', e?.target?.value)}
              />
            </div>
          </div>

          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-border">
            <Button
              type="button"
              variant="outline"
              onClick={() => {
                setFormData({
                  firstName: '',
                  lastName: '',
                  dni: '',
                  phone: '',
                  email: '',
                  birthDate: '',
                  address: '',
                  city: '',
                  postalCode: '',
                  insuranceProvider: '',
                  insuranceNumber: '',
                  emergencyContact: '',
                  emergencyPhone: '',
                  allergies: '',
                  medications: '',
                  medicalHistory: ''
                });
              }}
            >
              Limpiar
            </Button>
            <Button
              type="submit"
              iconName="Save"
              iconPosition="left"
            >
              {isNewPatient ? 'Registrar Paciente' : 'Actualizar Paciente'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PatientRegistration;