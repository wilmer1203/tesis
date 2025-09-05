import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Image from '../../../components/AppImage';

const PatientInfoPanel = ({ patient, onPatientChange }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const patientData = patient || {
    id: 'P-2024-0892',
    name: 'Ana María Rodríguez',
    age: 34,
    gender: 'Femenino',
    phone: '+58 412-555-0123',
    email: 'ana.rodriguez@email.com',
    address: 'Av. Francisco de Miranda, Caracas',
    bloodType: 'O+',
    allergies: ['Penicilina', 'Látex'],
    insurance: 'Seguros Caracas',
    emergencyContact: {
      name: 'Carlos Rodríguez',
      relationship: 'Esposo',
      phone: '+58 414-555-0456'
    },
    medicalHistory: [
      'Hipertensión controlada',
      'Diabetes tipo 2'
    ],
    lastVisit: '2024-08-15',
    totalVisits: 12,
    photo: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face'
  };

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="User" size={20} className="text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Información del Paciente</h2>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-2 hover:bg-muted rounded-md transition-smooth"
        >
          <Icon 
            name={isExpanded ? "ChevronUp" : "ChevronDown"} 
            size={16} 
            className="text-muted-foreground" 
          />
        </button>
      </div>
      {/* Content */}
      {isExpanded && (
        <div className="p-4 space-y-4">
          {/* Patient Photo and Basic Info */}
          <div className="flex items-start space-x-4">
            <div className="w-20 h-20 rounded-full overflow-hidden bg-muted flex-shrink-0">
              <Image
                src={patientData?.photo}
                alt={`Foto de ${patientData?.name}`}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-xl font-semibold text-foreground mb-1">
                {patientData?.name}
              </h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="text-muted-foreground">ID:</span>
                  <span className="ml-2 font-medium text-foreground">{patientData?.id}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Edad:</span>
                  <span className="ml-2 font-medium text-foreground">{patientData?.age} años</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Género:</span>
                  <span className="ml-2 font-medium text-foreground">{patientData?.gender}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Tipo Sangre:</span>
                  <span className="ml-2 font-medium text-foreground">{patientData?.bloodType}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div className="bg-muted rounded-md p-3">
            <h4 className="text-sm font-semibold text-foreground mb-2 flex items-center">
              <Icon name="Phone" size={16} className="mr-2 text-primary" />
              Información de Contacto
            </h4>
            <div className="space-y-1 text-sm">
              <div className="flex items-center">
                <Icon name="Phone" size={14} className="mr-2 text-muted-foreground" />
                <span className="text-foreground">{patientData?.phone}</span>
              </div>
              <div className="flex items-center">
                <Icon name="Mail" size={14} className="mr-2 text-muted-foreground" />
                <span className="text-foreground">{patientData?.email}</span>
              </div>
              <div className="flex items-start">
                <Icon name="MapPin" size={14} className="mr-2 mt-0.5 text-muted-foreground" />
                <span className="text-foreground">{patientData?.address}</span>
              </div>
            </div>
          </div>

          {/* Medical Alerts */}
          {patientData?.allergies?.length > 0 && (
            <div className="bg-warning/10 border border-warning/20 rounded-md p-3">
              <h4 className="text-sm font-semibold text-warning mb-2 flex items-center">
                <Icon name="AlertTriangle" size={16} className="mr-2" />
                Alergias
              </h4>
              <div className="flex flex-wrap gap-2">
                {patientData?.allergies?.map((allergy, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-warning/20 text-warning text-xs font-medium rounded-full"
                  >
                    {allergy}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Medical History */}
          {patientData?.medicalHistory?.length > 0 && (
            <div className="bg-muted rounded-md p-3">
              <h4 className="text-sm font-semibold text-foreground mb-2 flex items-center">
                <Icon name="FileText" size={16} className="mr-2 text-primary" />
                Historial Médico
              </h4>
              <ul className="space-y-1">
                {patientData?.medicalHistory?.map((condition, index) => (
                  <li key={index} className="text-sm text-foreground flex items-center">
                    <Icon name="Dot" size={12} className="mr-1 text-muted-foreground" />
                    {condition}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Insurance and Emergency Contact */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="bg-muted rounded-md p-3">
              <h4 className="text-sm font-semibold text-foreground mb-2 flex items-center">
                <Icon name="Shield" size={16} className="mr-2 text-primary" />
                Seguro
              </h4>
              <p className="text-sm text-foreground">{patientData?.insurance}</p>
            </div>

            <div className="bg-muted rounded-md p-3">
              <h4 className="text-sm font-semibold text-foreground mb-2 flex items-center">
                <Icon name="UserCheck" size={16} className="mr-2 text-primary" />
                Contacto de Emergencia
              </h4>
              <div className="text-sm">
                <p className="text-foreground font-medium">{patientData?.emergencyContact?.name}</p>
                <p className="text-muted-foreground">{patientData?.emergencyContact?.relationship}</p>
                <p className="text-foreground">{patientData?.emergencyContact?.phone}</p>
              </div>
            </div>
          </div>

          {/* Visit Statistics */}
          <div className="bg-primary/5 border border-primary/20 rounded-md p-3">
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-primary">{patientData?.totalVisits}</div>
                <div className="text-xs text-muted-foreground">Visitas Totales</div>
              </div>
              <div>
                <div className="text-sm font-medium text-foreground">
                  {new Date(patientData.lastVisit)?.toLocaleDateString('es-VE')}
                </div>
                <div className="text-xs text-muted-foreground">Última Visita</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientInfoPanel;