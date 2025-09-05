import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Header from '../../components/ui/Header';
import PatientContextBar from '../../components/ui/PatientContextBar';
import PatientSearchPanel from './components/PatientSearchPanel';
import PatientRegistrationForm from './components/PatientRegistrationForm';
import RecentPatientsPanel from './components/RecentPatientsPanel';
import QueueAssignmentModal from './components/QueueAssignmentModal';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const PatientRegistration = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  const [currentView, setCurrentView] = useState('search'); // search, register, edit
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [showQueueModal, setShowQueueModal] = useState(false);
  const [patientForQueue, setPatientForQueue] = useState(null);
  const [showPatientContext, setShowPatientContext] = useState(false);
  const [registrationSuccess, setRegistrationSuccess] = useState(false);

  // Check for URL parameters on mount
  useEffect(() => {
    const action = searchParams?.get('action');
    const patientId = searchParams?.get('patient');
    
    if (action === 'register') {
      setCurrentView('register');
    } else if (action === 'edit' && patientId) {
      // Load patient data for editing
      setCurrentView('edit');
    }
  }, [searchParams]);

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
    setShowPatientContext(true);
  };

  const handleNewRegistration = () => {
    setCurrentView('register');
    setSelectedPatient(null);
    setShowPatientContext(false);
    setRegistrationSuccess(false);
  };

  const handleRegistrationSubmit = async (patientData) => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      console.log('Patient registered:', patientData);
      setRegistrationSuccess(true);
      setSelectedPatient(patientData);
      
      // Show success message and option to add to queue
      setTimeout(() => {
        setCurrentView('search');
        setShowPatientContext(true);
      }, 2000);
      
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  const handleRegistrationCancel = () => {
    setCurrentView('search');
    setSelectedPatient(null);
    setShowPatientContext(false);
    setRegistrationSuccess(false);
  };

  const handleAddToQueue = (patient) => {
    setPatientForQueue(patient);
    setShowQueueModal(true);
  };

  const handleQueueAssignment = async (assignmentData) => {
    try {
      console.log('Queue assignment:', assignmentData);
      
      // Navigate to queue management dashboard
      navigate('/queue-management-dashboard', {
        state: { 
          newAssignment: assignmentData,
          highlightPatient: assignmentData?.patient?.id 
        }
      });
      
    } catch (error) {
      console.error('Queue assignment error:', error);
    }
  };

  const handleViewPatient = (patient) => {
    navigate('/patient-consultation', {
      state: { patient }
    });
  };

  const renderMainContent = () => {
    switch (currentView) {
      case 'register': case'edit':
        return (
          <div className="space-y-6">
            {registrationSuccess && (
              <div className="bg-success/10 border border-success/20 rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <Icon name="CheckCircle" size={24} className="text-success" />
                  <div>
                    <h3 className="font-medium text-success">¡Paciente registrado exitosamente!</h3>
                    <p className="text-sm text-success/80 mt-1">
                      El paciente ha sido registrado y puede ser agregado a la cola de atención.
                    </p>
                  </div>
                </div>
              </div>
            )}
            
            <PatientRegistrationForm
              onSubmit={handleRegistrationSubmit}
              onCancel={handleRegistrationCancel}
              initialData={currentView === 'edit' ? selectedPatient : null}
            />
          </div>
        );
      
      default:
        return (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Search Panel */}
            <div className="lg:col-span-2">
              <PatientSearchPanel
                onPatientSelect={handlePatientSelect}
                onNewRegistration={handleNewRegistration}
              />
            </div>
            
            {/* Recent Patients Panel */}
            <div className="lg:col-span-1">
              <RecentPatientsPanel
                onAddToQueue={handleAddToQueue}
                onViewPatient={handleViewPatient}
              />
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Patient Context Bar */}
      {showPatientContext && selectedPatient && (
        <PatientContextBar
          patient={selectedPatient}
          onDismiss={() => {
            setShowPatientContext(false);
            setSelectedPatient(null);
          }}
          showQueueStatus={false}
        />
      )}

      {/* Main Content */}
      <main className={`${showPatientContext ? 'pt-32' : 'pt-16'} pb-8`}>
        <div className="max-w-7xl mx-auto px-6">
          {/* Page Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-foreground">Registro de Pacientes</h1>
                <p className="text-muted-foreground mt-2">
                  {currentView === 'register' ?'Complete el formulario para registrar un nuevo paciente'
                    : currentView === 'edit' ?'Edite la información del paciente seleccionado' :'Busque pacientes existentes o registre nuevos pacientes para la atención'
                  }
                </p>
              </div>
              
              {/* Quick Actions */}
              <div className="flex items-center space-x-3">
                {currentView === 'search' && (
                  <>
                    <Button
                      variant="outline"
                      iconName="Users"
                      iconPosition="left"
                      onClick={() => navigate('/queue-management-dashboard')}
                    >
                      Ver Colas
                    </Button>
                    <Button
                      variant="primary"
                      iconName="UserPlus"
                      iconPosition="left"
                      onClick={handleNewRegistration}
                    >
                      Nuevo Paciente
                    </Button>
                  </>
                )}
                
                {(currentView === 'register' || currentView === 'edit') && (
                  <Button
                    variant="outline"
                    iconName="ArrowLeft"
                    iconPosition="left"
                    onClick={handleRegistrationCancel}
                  >
                    Volver a Búsqueda
                  </Button>
                )}
              </div>
            </div>
          </div>

          {/* Breadcrumb */}
          <nav className="flex items-center space-x-2 text-sm text-muted-foreground mb-6">
            <button
              onClick={() => navigate('/')}
              className="hover:text-foreground transition-smooth"
            >
              Inicio
            </button>
            <Icon name="ChevronRight" size={16} />
            <span className="text-foreground">Registro de Pacientes</span>
            {(currentView === 'register' || currentView === 'edit') && (
              <>
                <Icon name="ChevronRight" size={16} />
                <span className="text-foreground">
                  {currentView === 'register' ? 'Nuevo Paciente' : 'Editar Paciente'}
                </span>
              </>
            )}
          </nav>

          {/* Main Content */}
          {renderMainContent()}

          {/* Quick Stats */}
          {currentView === 'search' && (
            <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-card border border-border rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <Icon name="Users" size={20} className="text-primary" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-foreground">1,247</div>
                    <div className="text-sm text-muted-foreground">Total Pacientes</div>
                  </div>
                </div>
              </div>
              
              <div className="bg-card border border-border rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-success/10 rounded-full flex items-center justify-center">
                    <Icon name="UserPlus" size={20} className="text-success" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-foreground">23</div>
                    <div className="text-sm text-muted-foreground">Nuevos Hoy</div>
                  </div>
                </div>
              </div>
              
              <div className="bg-card border border-border rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-warning/10 rounded-full flex items-center justify-center">
                    <Icon name="Clock" size={20} className="text-warning" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-foreground">12</div>
                    <div className="text-sm text-muted-foreground">En Cola</div>
                  </div>
                </div>
              </div>
              
              <div className="bg-card border border-border rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-accent/10 rounded-full flex items-center justify-center">
                    <Icon name="Activity" size={20} className="text-accent" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-foreground">8</div>
                    <div className="text-sm text-muted-foreground">En Consulta</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Queue Assignment Modal */}
      <QueueAssignmentModal
        isOpen={showQueueModal}
        onClose={() => {
          setShowQueueModal(false);
          setPatientForQueue(null);
        }}
        patient={patientForQueue}
        onAssign={handleQueueAssignment}
      />
    </div>
  );
};

export default PatientRegistration;