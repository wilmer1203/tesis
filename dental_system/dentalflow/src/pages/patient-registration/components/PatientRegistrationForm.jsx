import React, { useState } from 'react';

import Input from '../../../components/ui/Input';
import Button from '../../../components/ui/Button';
import Select from '../../../components/ui/Select';
import { Checkbox } from '../../../components/ui/Checkbox';

const PatientRegistrationForm = ({ onSubmit, onCancel, initialData = null }) => {
  const [formData, setFormData] = useState({
    // Personal Information
    firstName: initialData?.firstName || '',
    lastName: initialData?.lastName || '',
    cedula: initialData?.cedula || '',
    birthDate: initialData?.birthDate || '',
    gender: initialData?.gender || '',
    phone: initialData?.phone || '',
    email: initialData?.email || '',
    address: initialData?.address || '',
    city: initialData?.city || 'Caracas',
    state: initialData?.state || 'Distrito Capital',
    
    // Emergency Contact
    emergencyName: initialData?.emergencyName || '',
    emergencyPhone: initialData?.emergencyPhone || '',
    emergencyRelation: initialData?.emergencyRelation || '',
    
    // Insurance Information
    hasInsurance: initialData?.hasInsurance || false,
    insuranceProvider: initialData?.insuranceProvider || '',
    insuranceNumber: initialData?.insuranceNumber || '',
    
    // Payment Preferences
    preferredCurrency: initialData?.preferredCurrency || 'BS',
    
    // Medical History
    allergies: initialData?.allergies || [],
    medications: initialData?.medications || '',
    medicalConditions: initialData?.medicalConditions || [],
    previousTreatments: initialData?.previousTreatments || '',
    
    // Additional Information
    referredBy: initialData?.referredBy || '',
    notes: initialData?.notes || ''
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showMedicalHistory, setShowMedicalHistory] = useState(false);

  // Options for dropdowns
  const genderOptions = [
    { value: 'M', label: 'Masculino' },
    { value: 'F', label: 'Femenino' },
    { value: 'O', label: 'Otro' }
  ];

  const stateOptions = [
    { value: 'Distrito Capital', label: 'Distrito Capital' },
    { value: 'Miranda', label: 'Miranda' },
    { value: 'Vargas', label: 'Vargas' },
    { value: 'Aragua', label: 'Aragua' },
    { value: 'Carabobo', label: 'Carabobo' },
    { value: 'Zulia', label: 'Zulia' },
    { value: 'Lara', label: 'Lara' },
    { value: 'Táchira', label: 'Táchira' }
  ];

  const relationOptions = [
    { value: 'padre', label: 'Padre' },
    { value: 'madre', label: 'Madre' },
    { value: 'esposo', label: 'Esposo/a' },
    { value: 'hijo', label: 'Hijo/a' },
    { value: 'hermano', label: 'Hermano/a' },
    { value: 'amigo', label: 'Amigo/a' },
    { value: 'otro', label: 'Otro' }
  ];

  const insuranceOptions = [
    { value: 'Seguros Caracas', label: 'Seguros Caracas' },
    { value: 'Seguros Universales', label: 'Seguros Universales' },
    { value: 'Seguros Mercantil', label: 'Seguros Mercantil' },
    { value: 'Seguros La Previsora', label: 'Seguros La Previsora' },
    { value: 'Otro', label: 'Otro' }
  ];

  const currencyOptions = [
    { value: 'BS', label: 'Bolívares (BS)' },
    { value: 'USD', label: 'Dólares (USD)' },
    { value: 'MIXED', label: 'Mixto (BS + USD)' }
  ];

  const commonAllergies = [
    'Penicilina', 'Lidocaína', 'Látex', 'Aspirina', 'Ibuprofeno', 
    'Anestesia local', 'Metales', 'Acrílico', 'Ninguna'
  ];

  const commonConditions = [
    'Diabetes', 'Hipertensión', 'Problemas cardíacos', 'Asma', 
    'Epilepsia', 'Embarazo', 'Lactancia', 'Ninguna'
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear error when user starts typing
    if (errors?.[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  const handleAllergyChange = (allergy, checked) => {
    setFormData(prev => ({
      ...prev,
      allergies: checked 
        ? [...prev?.allergies, allergy]
        : prev?.allergies?.filter(a => a !== allergy)
    }));
  };

  const handleConditionChange = (condition, checked) => {
    setFormData(prev => ({
      ...prev,
      medicalConditions: checked 
        ? [...prev?.medicalConditions, condition]
        : prev?.medicalConditions?.filter(c => c !== condition)
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    // Required fields
    if (!formData?.firstName?.trim()) newErrors.firstName = 'El nombre es requerido';
    if (!formData?.lastName?.trim()) newErrors.lastName = 'El apellido es requerido';
    if (!formData?.cedula?.trim()) newErrors.cedula = 'La cédula es requerida';
    if (!formData?.birthDate) newErrors.birthDate = 'La fecha de nacimiento es requerida';
    if (!formData?.gender) newErrors.gender = 'El género es requerido';
    if (!formData?.phone?.trim()) newErrors.phone = 'El teléfono es requerido';

    // Cedula format validation (Venezuelan format)
    const cedulaRegex = /^[VEJ]-\d{7,8}$/;
    if (formData?.cedula && !cedulaRegex?.test(formData?.cedula)) {
      newErrors.cedula = 'Formato de cédula inválido (ej: V-12345678)';
    }

    // Phone format validation
    const phoneRegex = /^\+58\s\d{3}-\d{3}-\d{4}$/;
    if (formData?.phone && !phoneRegex?.test(formData?.phone)) {
      newErrors.phone = 'Formato de teléfono inválido (ej: +58 412-555-0123)';
    }

    // Email validation
    if (formData?.email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex?.test(formData?.email)) {
        newErrors.email = 'Formato de email inválido';
      }
    }

    // Emergency contact validation
    if (formData?.emergencyName && !formData?.emergencyPhone) {
      newErrors.emergencyPhone = 'Teléfono de emergencia requerido';
    }

    // Insurance validation
    if (formData?.hasInsurance && !formData?.insuranceProvider) {
      newErrors.insuranceProvider = 'Proveedor de seguro requerido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors)?.length === 0;
  };

  const handleSubmit = async (e) => {
    e?.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Calculate age from birth date
      const birthDate = new Date(formData.birthDate);
      const today = new Date();
      const age = today?.getFullYear() - birthDate?.getFullYear();
      
      const patientData = {
        ...formData,
        id: `P-${new Date()?.getFullYear()}-${String(Math.floor(Math.random() * 9999) + 1)?.padStart(4, '0')}`,
        age,
        registrationDate: new Date()?.toISOString(),
        status: 'active'
      };

      if (onSubmit) {
        await onSubmit(patientData);
      }
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      <div className="p-6 border-b border-border">
        <h2 className="text-xl font-semibold text-foreground">
          {initialData ? 'Editar Paciente' : 'Registro de Nuevo Paciente'}
        </h2>
        <p className="text-sm text-muted-foreground mt-1">
          Complete la información del paciente para el registro
        </p>
      </div>
      <form onSubmit={handleSubmit} className="p-6 space-y-8">
        {/* Personal Information */}
        <div>
          <h3 className="text-lg font-medium text-foreground mb-4">Información Personal</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Nombre"
              type="text"
              placeholder="Ingrese el nombre"
              value={formData?.firstName}
              onChange={(e) => handleInputChange('firstName', e?.target?.value)}
              error={errors?.firstName}
              required
            />
            
            <Input
              label="Apellido"
              type="text"
              placeholder="Ingrese el apellido"
              value={formData?.lastName}
              onChange={(e) => handleInputChange('lastName', e?.target?.value)}
              error={errors?.lastName}
              required
            />
            
            <Input
              label="Cédula de Identidad"
              type="text"
              placeholder="V-12345678"
              value={formData?.cedula}
              onChange={(e) => handleInputChange('cedula', e?.target?.value)}
              error={errors?.cedula}
              required
            />
            
            <Input
              label="Fecha de Nacimiento"
              type="date"
              value={formData?.birthDate}
              onChange={(e) => handleInputChange('birthDate', e?.target?.value)}
              error={errors?.birthDate}
              required
            />
            
            <Select
              label="Género"
              options={genderOptions}
              value={formData?.gender}
              onChange={(value) => handleInputChange('gender', value)}
              error={errors?.gender}
              required
            />
            
            <Input
              label="Teléfono"
              type="tel"
              placeholder="+58 412-555-0123"
              value={formData?.phone}
              onChange={(e) => handleInputChange('phone', e?.target?.value)}
              error={errors?.phone}
              required
            />
            
            <Input
              label="Email"
              type="email"
              placeholder="ejemplo@email.com"
              value={formData?.email}
              onChange={(e) => handleInputChange('email', e?.target?.value)}
              error={errors?.email}
              className="md:col-span-2"
            />
            
            <Input
              label="Dirección"
              type="text"
              placeholder="Dirección completa"
              value={formData?.address}
              onChange={(e) => handleInputChange('address', e?.target?.value)}
              className="md:col-span-2"
            />
            
            <Input
              label="Ciudad"
              type="text"
              placeholder="Ciudad"
              value={formData?.city}
              onChange={(e) => handleInputChange('city', e?.target?.value)}
            />
            
            <Select
              label="Estado"
              options={stateOptions}
              value={formData?.state}
              onChange={(value) => handleInputChange('state', value)}
            />
          </div>
        </div>

        {/* Emergency Contact */}
        <div>
          <h3 className="text-lg font-medium text-foreground mb-4">Contacto de Emergencia</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input
              label="Nombre Completo"
              type="text"
              placeholder="Nombre del contacto"
              value={formData?.emergencyName}
              onChange={(e) => handleInputChange('emergencyName', e?.target?.value)}
            />
            
            <Input
              label="Teléfono"
              type="tel"
              placeholder="+58 412-555-0123"
              value={formData?.emergencyPhone}
              onChange={(e) => handleInputChange('emergencyPhone', e?.target?.value)}
              error={errors?.emergencyPhone}
            />
            
            <Select
              label="Parentesco"
              options={relationOptions}
              value={formData?.emergencyRelation}
              onChange={(value) => handleInputChange('emergencyRelation', value)}
              placeholder="Seleccione parentesco"
            />
          </div>
        </div>

        {/* Insurance Information */}
        <div>
          <h3 className="text-lg font-medium text-foreground mb-4">Información de Seguro</h3>
          <div className="space-y-4">
            <Checkbox
              label="¿Tiene seguro médico?"
              checked={formData?.hasInsurance}
              onChange={(e) => handleInputChange('hasInsurance', e?.target?.checked)}
            />
            
            {formData?.hasInsurance && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Select
                  label="Proveedor de Seguro"
                  options={insuranceOptions}
                  value={formData?.insuranceProvider}
                  onChange={(value) => handleInputChange('insuranceProvider', value)}
                  error={errors?.insuranceProvider}
                  required
                />
                
                <Input
                  label="Número de Póliza"
                  type="text"
                  placeholder="Número de póliza"
                  value={formData?.insuranceNumber}
                  onChange={(e) => handleInputChange('insuranceNumber', e?.target?.value)}
                />
              </div>
            )}
          </div>
        </div>

        {/* Payment Preferences */}
        <div>
          <h3 className="text-lg font-medium text-foreground mb-4">Preferencias de Pago</h3>
          <Select
            label="Moneda Preferida"
            options={currencyOptions}
            value={formData?.preferredCurrency}
            onChange={(value) => handleInputChange('preferredCurrency', value)}
            description="Seleccione la moneda preferida para los pagos"
          />
        </div>

        {/* Medical History */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-foreground">Historia Médica</h3>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              iconName={showMedicalHistory ? "ChevronUp" : "ChevronDown"}
              iconPosition="right"
              onClick={() => setShowMedicalHistory(!showMedicalHistory)}
            >
              {showMedicalHistory ? 'Ocultar' : 'Mostrar'}
            </Button>
          </div>
          
          {showMedicalHistory && (
            <div className="space-y-6">
              {/* Allergies */}
              <div>
                <h4 className="text-sm font-medium text-foreground mb-3">Alergias</h4>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                  {commonAllergies?.map((allergy) => (
                    <Checkbox
                      key={allergy}
                      label={allergy}
                      checked={formData?.allergies?.includes(allergy)}
                      onChange={(e) => handleAllergyChange(allergy, e?.target?.checked)}
                    />
                  ))}
                </div>
              </div>

              {/* Medical Conditions */}
              <div>
                <h4 className="text-sm font-medium text-foreground mb-3">Condiciones Médicas</h4>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                  {commonConditions?.map((condition) => (
                    <Checkbox
                      key={condition}
                      label={condition}
                      checked={formData?.medicalConditions?.includes(condition)}
                      onChange={(e) => handleConditionChange(condition, e?.target?.checked)}
                    />
                  ))}
                </div>
              </div>

              {/* Medications */}
              <Input
                label="Medicamentos Actuales"
                type="text"
                placeholder="Liste los medicamentos que toma actualmente"
                value={formData?.medications}
                onChange={(e) => handleInputChange('medications', e?.target?.value)}
                description="Separe múltiples medicamentos con comas"
              />

              {/* Previous Treatments */}
              <Input
                label="Tratamientos Dentales Previos"
                type="text"
                placeholder="Describa tratamientos dentales anteriores"
                value={formData?.previousTreatments}
                onChange={(e) => handleInputChange('previousTreatments', e?.target?.value)}
              />
            </div>
          )}
        </div>

        {/* Additional Information */}
        <div>
          <h3 className="text-lg font-medium text-foreground mb-4">Información Adicional</h3>
          <div className="space-y-4">
            <Input
              label="Referido por"
              type="text"
              placeholder="¿Quién lo refirió a nuestra clínica?"
              value={formData?.referredBy}
              onChange={(e) => handleInputChange('referredBy', e?.target?.value)}
            />
            
            <Input
              label="Notas Adicionales"
              type="text"
              placeholder="Información adicional relevante"
              value={formData?.notes}
              onChange={(e) => handleInputChange('notes', e?.target?.value)}
            />
          </div>
        </div>

        {/* Form Actions */}
        <div className="flex items-center justify-end space-x-4 pt-6 border-t border-border">
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isSubmitting}
          >
            Cancelar
          </Button>
          
          <Button
            type="submit"
            variant="primary"
            loading={isSubmitting}
            iconName="Save"
            iconPosition="left"
          >
            {initialData ? 'Actualizar Paciente' : 'Registrar Paciente'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default PatientRegistrationForm;