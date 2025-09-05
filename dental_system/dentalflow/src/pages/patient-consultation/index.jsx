import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import Header from '../../components/ui/Header';
import PatientContextBar from '../../components/ui/PatientContextBar';
import PatientInfoPanel from './components/PatientInfoPanel';
import TreatmentDocumentationPanel from './components/TreatmentDocumentationPanel';
import DigitalOdontogramViewer from './components/DigitalOdontogramViewer';
import ConsultationHistoryPanel from './components/ConsultationHistoryPanel';
import ParticipatingDentistsPanel from './components/ParticipatingDentistsPanel';
import PhotoUploadPanel from './components/PhotoUploadPanel';
import PaymentProcessingPanel from './components/PaymentProcessingPanel';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const PatientConsultation = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [currentPatient, setCurrentPatient] = useState(null);
  const [consultationData, setConsultationData] = useState({
    interventions: [],
    participatingDentists: [],
    totalCost: { bs: 0, usd: 0 },
    photos: [],
    paymentStatus: 'pending'
  });
  const [activeTab, setActiveTab] = useState('treatment');
  const [isConsultationActive, setIsConsultationActive] = useState(true);

  // Mock patient data
  const mockPatient = {
    id: 'P-2024-0892',
    name: 'Ana María Rodríguez',
    age: 34,
    gender: 'Femenino',
    phone: '+58 412-555-0123',
    email: 'ana.rodriguez@email.com',
    queuePosition: 0,
    status: 'in-consultation',
    allergies: ['Penicilina', 'Látex'],
    insurance: 'Seguros Caracas'
  };

  useEffect(() => {
    // Get patient from URL params or use mock data
    const patientId = searchParams?.get('patient');
    if (patientId) {
      // In a real app, fetch patient data from API
      setCurrentPatient(mockPatient);
    } else {
      setCurrentPatient(mockPatient);
    }
  }, [searchParams]);

  const handleInterventionAdd = (intervention) => {
    setConsultationData(prev => ({
      ...prev,
      interventions: [...prev?.interventions, intervention],
      totalCost: {
        bs: prev?.totalCost?.bs + (intervention?.costBs || 0),
        usd: prev?.totalCost?.usd + (intervention?.costUsd || 0)
      }
    }));
  };

  const handleDentistAdd = (dentist) => {
    setConsultationData(prev => ({
      ...prev,
      participatingDentists: [...prev?.participatingDentists, dentist]
    }));
  };

  const handleDentistRemove = (dentistId) => {
    setConsultationData(prev => ({
      ...prev,
      participatingDentists: prev?.participatingDentists?.filter(d => d?.id !== dentistId)
    }));
  };

  const handlePhotoUpload = (photo) => {
    setConsultationData(prev => ({
      ...prev,
      photos: [...prev?.photos, photo]
    }));
  };

  const handlePaymentProcess = (paymentData) => {
    setConsultationData(prev => ({
      ...prev,
      paymentStatus: 'completed'
    }));
  };

  const handleCompleteConsultation = () => {
    // In a real app, save consultation data to backend
    setIsConsultationActive(false);
    navigate('/queue-management-dashboard');
  };

  const handleToothClick = (toothNumber, toothData) => {
    console.log('Tooth clicked:', toothNumber, toothData);
    // Handle tooth selection for intervention
  };

  const tabs = [
    { id: 'treatment', label: 'Tratamiento', icon: 'Stethoscope' },
    { id: 'odontogram', label: 'Odontograma', icon: 'Tooth' },
    { id: 'history', label: 'Historial', icon: 'History' },
    { id: 'photos', label: 'Fotografías', icon: 'Camera' },
    { id: 'payment', label: 'Pagos', icon: 'CreditCard' }
  ];

  if (!currentPatient) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="pt-16 flex items-center justify-center h-screen">
          <div className="text-center">
            <Icon name="Loader2" size={48} className="mx-auto text-primary animate-spin mb-4" />
            <h2 className="text-xl font-semibold text-foreground mb-2">Cargando Consulta</h2>
            <p className="text-muted-foreground">Preparando la información del paciente...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      {/* Patient Context Bar */}
      <PatientContextBar 
        patient={currentPatient}
        showQueueStatus={false}
        onDismiss={() => navigate('/queue-management-dashboard')}
      />
      <div className="pt-32 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Consultation Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-foreground">Consulta del Paciente</h1>
              <p className="text-muted-foreground mt-1">
                Documentación completa del tratamiento y gestión de la consulta
              </p>
            </div>
            
            <div className="flex items-center space-x-3">
              {isConsultationActive && (
                <>
                  <div className="flex items-center space-x-2 px-3 py-2 bg-success/10 text-success rounded-md">
                    <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
                    <span className="text-sm font-medium">Consulta Activa</span>
                  </div>
                  
                  <Button
                    variant="outline"
                    onClick={() => navigate('/queue-management-dashboard')}
                  >
                    <Icon name="ArrowLeft" size={16} className="mr-2" />
                    Volver a Cola
                  </Button>
                  
                  <Button onClick={handleCompleteConsultation}>
                    <Icon name="CheckCircle" size={16} className="mr-2" />
                    Completar Consulta
                  </Button>
                </>
              )}
            </div>
          </div>

          {/* Main Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Left Sidebar - Patient Info */}
            <div className="lg:col-span-1 space-y-6">
              <PatientInfoPanel 
                patient={currentPatient}
                onPatientChange={setCurrentPatient}
              />
              
              <ParticipatingDentistsPanel
                onDentistAdd={handleDentistAdd}
                onDentistRemove={handleDentistRemove}
              />
            </div>

            {/* Main Content Area */}
            <div className="lg:col-span-3">
              {/* Tab Navigation */}
              <div className="bg-card border border-border rounded-lg shadow-soft mb-6">
                <div className="border-b border-border">
                  <nav className="flex space-x-1 p-1">
                    {tabs?.map((tab) => (
                      <button
                        key={tab?.id}
                        onClick={() => setActiveTab(tab?.id)}
                        className={`flex items-center space-x-2 px-4 py-3 rounded-md text-sm font-medium transition-smooth ${
                          activeTab === tab?.id
                            ? 'bg-primary text-primary-foreground'
                            : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                        }`}
                      >
                        <Icon name={tab?.icon} size={16} />
                        <span className="hidden sm:inline">{tab?.label}</span>
                      </button>
                    ))}
                  </nav>
                </div>

                {/* Tab Content */}
                <div className="p-6">
                  {activeTab === 'treatment' && (
                    <TreatmentDocumentationPanel
                      onInterventionAdd={handleInterventionAdd}
                      onSignatureCapture={() => console.log('Signature captured')}
                    />
                  )}

                  {activeTab === 'odontogram' && (
                    <DigitalOdontogramViewer
                      interventions={consultationData?.interventions}
                      onToothClick={handleToothClick}
                    />
                  )}

                  {activeTab === 'history' && (
                    <ConsultationHistoryPanel
                      patientId={currentPatient?.id}
                    />
                  )}

                  {activeTab === 'photos' && (
                    <PhotoUploadPanel
                      patientId={currentPatient?.id}
                      onPhotoUpload={handlePhotoUpload}
                    />
                  )}

                  {activeTab === 'payment' && (
                    <PaymentProcessingPanel
                      totalCost={consultationData?.totalCost}
                      participatingDentists={consultationData?.participatingDentists}
                      onPaymentProcess={handlePaymentProcess}
                    />
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions Bar */}
          {isConsultationActive && (
            <div className="fixed bottom-6 right-6 bg-card border border-border rounded-lg shadow-modal p-4">
              <div className="flex items-center space-x-3">
                <div className="text-sm text-muted-foreground">Acciones Rápidas:</div>
                <Button variant="outline" size="sm">
                  <Icon name="Camera" size={14} className="mr-1" />
                  Foto
                </Button>
                <Button variant="outline" size="sm">
                  <Icon name="FileText" size={14} className="mr-1" />
                  Nota
                </Button>
                <Button variant="outline" size="sm">
                  <Icon name="CreditCard" size={14} className="mr-1" />
                  Pago
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PatientConsultation;