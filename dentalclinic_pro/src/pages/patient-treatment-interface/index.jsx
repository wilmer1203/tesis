import React, { useState, useEffect } from 'react';
import Header from '../../components/ui/Header';
import PatientSummary from './components/PatientSummary';
import InteractiveOdontogram from './components/InteractiveOdontogram';
import TreatmentDocumentation from './components/TreatmentDocumentation';
import SessionTimer from './components/SessionTimer';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const PatientTreatmentInterface = () => {
  const [currentPatient, setCurrentPatient] = useState(null);
  const [sessionActive, setSessionActive] = useState(false);
  const [sessionStartTime, setSessionStartTime] = useState(null);
  const [treatmentData, setTreatmentData] = useState({
    procedures: [],
    medications: [],
    notes: '',
    followUpDate: '',
    billingCodes: []
  });
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  // Mock current patient data
  const mockCurrentPatient = {
    id: 'P001',
    nombre: 'María',
    apellido: 'González',
    edad: 34,
    telefono: '+34 612 345 678',
    email: 'maria.gonzalez@email.com',
    expediente: 'EXP-2024-001',
    alergias: ['Penicilina'],
    condiciones_medicas: ['Diabetes', 'Hipertensión'],
    medicamentos_actuales: ['Metformina 500mg', 'Enalapril 10mg'],
    ultima_visita: '2024-12-08',
    proxima_cita: {
      fecha: '2024-12-12',
      hora: '10:30:00',
      motivo: 'Revisión y tratamiento de caries'
    },
    historial_tratamientos: [
      { fecha: '2024-12-08', procedimiento: 'Limpieza dental', dentista: 'Dr. García' },
      { fecha: '2024-11-15', procedimiento: 'Obturación molar', dentista: 'Dr. García' },
      { fecha: '2024-10-20', procedimiento: 'Radiografía panorámica', dentista: 'Dr. García' }
    ],
    odontograma: {
      16: 'C',
      17: 'O',
      26: 'C',
      36: 'E',
      46: 'I'
    },
    alertas_medicas: [
      { tipo: 'alergia', mensaje: 'Alérgico a Penicilina' },
      { tipo: 'condicion', mensaje: 'Paciente diabético - controlar niveles de glucosa' }
    ]
  };

  useEffect(() => {
    // Simulate loading current patient for active session
    setCurrentPatient(mockCurrentPatient);
  }, []);

  const handleStartSession = () => {
    setSessionActive(true);
    setSessionStartTime(new Date());
  };

  const handleEndSession = () => {
    if (hasUnsavedChanges) {
      if (window.confirm('Tienes cambios sin guardar. ¿Estás seguro de terminar la sesión?')) {
        setSessionActive(false);
        setSessionStartTime(null);
        setHasUnsavedChanges(false);
      }
    } else {
      setSessionActive(false);
      setSessionStartTime(null);
    }
  };

  const handleOdontogramUpdate = (toothId, treatment, notes) => {
    if (currentPatient) {
      const updatedPatient = {
        ...currentPatient,
        odontograma: {
          ...currentPatient?.odontograma,
          [toothId]: treatment
        }
      };
      setCurrentPatient(updatedPatient);
      setHasUnsavedChanges(true);
      
      // Add procedure to treatment data
      const newProcedure = {
        id: Date.now(),
        toothId,
        treatment,
        notes,
        timestamp: new Date()?.toISOString()
      };
      
      setTreatmentData(prev => ({
        ...prev,
        procedures: [...prev?.procedures, newProcedure]
      }));
    }
  };

  const handleTreatmentDataUpdate = (newData) => {
    setTreatmentData(prev => ({ ...prev, ...newData }));
    setHasUnsavedChanges(true);
  };

  const handleSaveTreatment = async () => {
    try {
      // In a real app, this would save to backend
      console.log('Saving treatment data:', treatmentData);
      console.log('Updated patient:', currentPatient);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setHasUnsavedChanges(false);
      
      // Show success message
      alert('Tratamiento guardado exitosamente');
    } catch (error) {
      console.error('Error saving treatment:', error);
      alert('Error al guardar el tratamiento');
    }
  };

  const handleCompleteSession = async () => {
    if (hasUnsavedChanges) {
      await handleSaveTreatment();
    }
    
    // Generate session summary
    const sessionSummary = {
      patient: currentPatient,
      sessionDuration: sessionStartTime ? Date.now() - sessionStartTime?.getTime() : 0,
      treatmentData,
      completedAt: new Date()?.toISOString()
    };
    
    console.log('Session completed:', sessionSummary);
    alert('Sesión completada exitosamente');
    
    setSessionActive(false);
    setSessionStartTime(null);
    setTreatmentData({
      procedures: [],
      medications: [],
      notes: '',
      followUpDate: '',
      billingCodes: []
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Clinical Header */}
      <div className="bg-card border-b border-border">
        <Header 
          userRole="dentist" 
          userName="Dr. García"
          isCollapsed={false}
        />
        
        {/* Session Timer and Controls */}
        {currentPatient && (
          <div className="px-6 py-3 bg-primary/5">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Icon name="User" size={16} color="var(--color-primary)" />
                  <span className="text-sm font-medium text-card-foreground">
                    {currentPatient?.nombre} {currentPatient?.apellido}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    ({currentPatient?.expediente})
                  </span>
                </div>
                
                {sessionActive && (
                  <SessionTimer 
                    startTime={sessionStartTime}
                    isActive={sessionActive}
                  />
                )}
              </div>
              
              <div className="flex items-center space-x-3">
                {currentPatient?.alertas_medicas?.map((alerta, index) => (
                  <div 
                    key={index}
                    className="flex items-center space-x-1 bg-error/10 text-error px-2 py-1 rounded-md"
                  >
                    <Icon name="AlertTriangle" size={14} />
                    <span className="text-xs font-medium">
                      {alerta?.mensaje}
                    </span>
                  </div>
                ))}
                
                {hasUnsavedChanges && (
                  <span className="text-xs bg-warning/10 text-warning px-2 py-1 rounded-md">
                    Cambios sin guardar
                  </span>
                )}
                
                <Button
                  variant="outline"
                  size="sm"
                  iconName="Phone"
                  iconPosition="left"
                  iconSize={14}
                  className="text-xs"
                >
                  Emergencia
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main Interface */}
      <main className="pt-4">
        {currentPatient ? (
          <div className="h-[calc(100vh-140px)] flex">
            {/* Left Sidebar - Patient Summary */}
            <div className="w-80 border-r border-border bg-card">
              <PatientSummary 
                patient={currentPatient}
                sessionActive={sessionActive}
                onStartSession={handleStartSession}
                onEndSession={handleEndSession}
              />
            </div>
            
            {/* Center Panel - Interactive Odontogram */}
            <div className="flex-1 bg-background">
              <InteractiveOdontogram
                patient={currentPatient}
                sessionActive={sessionActive}
                onUpdateOdontogram={handleOdontogramUpdate}
                onSaveChanges={handleSaveTreatment}
                hasUnsavedChanges={hasUnsavedChanges}
              />
            </div>
            
            {/* Right Panel - Treatment Documentation */}
            <div className="w-96 border-l border-border bg-card">
              <TreatmentDocumentation
                treatmentData={treatmentData}
                onUpdateTreatmentData={handleTreatmentDataUpdate}
                onSaveTreatment={handleSaveTreatment}
                onCompleteSession={handleCompleteSession}
                sessionActive={sessionActive}
                hasUnsavedChanges={hasUnsavedChanges}
              />
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-[calc(100vh-140px)]">
            <div className="text-center">
              <Icon 
                name="UserX" 
                size={64} 
                color="var(--color-muted-foreground)" 
                className="mx-auto mb-4 opacity-50" 
              />
              <h3 className="text-lg font-medium text-card-foreground mb-2">
                No hay paciente activo
              </h3>
              <p className="text-sm text-muted-foreground mb-4">
                Seleccione un paciente desde el sistema de citas para comenzar una sesión de tratamiento
              </p>
              <Button
                variant="outline"
                size="sm"
                iconName="Calendar"
                iconPosition="left"
                iconSize={16}
              >
                Ver Agenda
              </Button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default PatientTreatmentInterface;