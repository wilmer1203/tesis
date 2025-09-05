import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const AddPatientModal = ({ isOpen, onClose, onAddPatient }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    birthDate: '',
    gender: '',
    address: '',
    city: '',
    postalCode: '',
    province: '',
    insuranceCompany: '',
    policyNumber: '',
    emergencyContact: '',
    emergencyPhone: ''
  });

  const [errors, setErrors] = useState({});

  const genderOptions = [
    { value: 'male', label: 'Masculino' },
    { value: 'female', label: 'Femenino' },
    { value: 'other', label: 'Otro' }
  ];

  const insuranceOptions = [
    { value: 'sanitas', label: 'Sanitas' },
    { value: 'mapfre', label: 'MAPFRE' },
    { value: 'adeslas', label: 'Adeslas' },
    { value: 'dkv', label: 'DKV' },
    { value: 'asisa', label: 'ASISA' },
    { value: 'none', label: 'Sin seguro' }
  ];

  const validateForm = () => {
    const newErrors = {};

    if (!formData?.firstName?.trim()) {
      newErrors.firstName = 'El nombre es obligatorio';
    }

    if (!formData?.lastName?.trim()) {
      newErrors.lastName = 'Los apellidos son obligatorios';
    }

    if (!formData?.email?.trim()) {
      newErrors.email = 'El email es obligatorio';
    } else if (!/\S+@\S+\.\S+/?.test(formData?.email)) {
      newErrors.email = 'El email no es válido';
    }

    if (!formData?.phone?.trim()) {
      newErrors.phone = 'El teléfono es obligatorio';
    }

    if (!formData?.birthDate) {
      newErrors.birthDate = 'La fecha de nacimiento es obligatoria';
    }

    if (!formData?.gender) {
      newErrors.gender = 'El género es obligatorio';
    }

    setErrors(newErrors);
    return Object.keys(newErrors)?.length === 0;
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    
    if (validateForm()) {
      const newPatient = {
        id: `PAT-${Date.now()}`,
        ...formData,
        avatar: `https://randomuser.me/api/portraits/${formData?.gender === 'female' ? 'women' : 'men'}/${Math.floor(Math.random() * 50)}.jpg`,
        status: 'active',
        lastVisit: 'Nuevo paciente',
        assignedDentist: null,
        medicalConditions: [],
        medications: [],
        appointments: [],
        treatments: [],
        coverage: {
          consultations: '100%',
          cleanings: '80%',
          fillings: '70%',
          surgeries: '50%'
        },
        insuranceStatus: 'pending',
        createdAt: new Date()?.toISOString()
      };

      onAddPatient(newPatient);
      handleClose();
    }
  };

  const handleClose = () => {
    setFormData({
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      birthDate: '',
      gender: '',
      address: '',
      city: '',
      postalCode: '',
      province: '',
      insuranceCompany: '',
      policyNumber: '',
      emergencyContact: '',
      emergencyPhone: ''
    });
    setErrors({});
    onClose();
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors?.[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-1200 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity bg-background/80 backdrop-blur-sm" onClick={handleClose} />

        <div className="inline-block w-full max-w-2xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-card border border-border rounded-lg shadow-custom-xl">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <Icon name="UserPlus" size={20} color="var(--color-primary-foreground)" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-foreground">
                  Agregar Nuevo Paciente
                </h3>
                <p className="text-sm text-muted-foreground">
                  Complete la información básica del paciente
                </p>
              </div>
            </div>
            <Button variant="ghost" onClick={handleClose} className="p-2">
              <Icon name="X" size={20} />
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Personal Information */}
            <div className="space-y-4">
              <h4 className="text-sm font-semibold text-foreground border-b border-border pb-2">
                Información Personal
              </h4>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Nombre *"
                  value={formData?.firstName}
                  onChange={(e) => handleInputChange('firstName', e?.target?.value)}
                  error={errors?.firstName}
                  placeholder="Nombre del paciente"
                />
                <Input
                  label="Apellidos *"
                  value={formData?.lastName}
                  onChange={(e) => handleInputChange('lastName', e?.target?.value)}
                  error={errors?.lastName}
                  placeholder="Apellidos del paciente"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Email *"
                  type="email"
                  value={formData?.email}
                  onChange={(e) => handleInputChange('email', e?.target?.value)}
                  error={errors?.email}
                  placeholder="correo@ejemplo.com"
                />
                <Input
                  label="Teléfono *"
                  type="tel"
                  value={formData?.phone}
                  onChange={(e) => handleInputChange('phone', e?.target?.value)}
                  error={errors?.phone}
                  placeholder="+34 600 000 000"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Fecha de Nacimiento *"
                  type="date"
                  value={formData?.birthDate}
                  onChange={(e) => handleInputChange('birthDate', e?.target?.value)}
                  error={errors?.birthDate}
                />
                <Select
                  label="Género *"
                  options={genderOptions}
                  value={formData?.gender}
                  onChange={(value) => handleInputChange('gender', value)}
                  error={errors?.gender}
                  placeholder="Seleccionar género"
                />
              </div>
            </div>

            {/* Address Information */}
            <div className="space-y-4">
              <h4 className="text-sm font-semibold text-foreground border-b border-border pb-2">
                Dirección
              </h4>
              
              <Input
                label="Dirección"
                value={formData?.address}
                onChange={(e) => handleInputChange('address', e?.target?.value)}
                placeholder="Calle, número, piso"
              />

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Input
                  label="Ciudad"
                  value={formData?.city}
                  onChange={(e) => handleInputChange('city', e?.target?.value)}
                  placeholder="Madrid"
                />
                <Input
                  label="Código Postal"
                  value={formData?.postalCode}
                  onChange={(e) => handleInputChange('postalCode', e?.target?.value)}
                  placeholder="28001"
                />
                <Input
                  label="Provincia"
                  value={formData?.province}
                  onChange={(e) => handleInputChange('province', e?.target?.value)}
                  placeholder="Madrid"
                />
              </div>
            </div>

            {/* Insurance Information */}
            <div className="space-y-4">
              <h4 className="text-sm font-semibold text-foreground border-b border-border pb-2">
                Seguro Médico
              </h4>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Select
                  label="Compañía de Seguros"
                  options={insuranceOptions}
                  value={formData?.insuranceCompany}
                  onChange={(value) => handleInputChange('insuranceCompany', value)}
                  placeholder="Seleccionar seguro"
                />
                <Input
                  label="Número de Póliza"
                  value={formData?.policyNumber}
                  onChange={(e) => handleInputChange('policyNumber', e?.target?.value)}
                  placeholder="Número de póliza"
                />
              </div>
            </div>

            {/* Emergency Contact */}
            <div className="space-y-4">
              <h4 className="text-sm font-semibold text-foreground border-b border-border pb-2">
                Contacto de Emergencia
              </h4>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Nombre del Contacto"
                  value={formData?.emergencyContact}
                  onChange={(e) => handleInputChange('emergencyContact', e?.target?.value)}
                  placeholder="Nombre completo"
                />
                <Input
                  label="Teléfono de Emergencia"
                  type="tel"
                  value={formData?.emergencyPhone}
                  onChange={(e) => handleInputChange('emergencyPhone', e?.target?.value)}
                  placeholder="+34 600 000 000"
                />
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex items-center justify-end space-x-3 pt-6 border-t border-border">
              <Button variant="outline" onClick={handleClose}>
                Cancelar
              </Button>
              <Button type="submit" variant="default">
                Agregar Paciente
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AddPatientModal;