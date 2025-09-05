import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import Header from '../../components/ui/Header';
import QueueControlBar from './components/QueueControlBar';
import QueueColumn from './components/QueueColumn';
import TransferModal from './components/TransferModal';
import QueueAnalytics from './components/QueueAnalytics';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const QueueManagementDashboard = () => {
  const navigate = useNavigate();
  const [currentView, setCurrentView] = useState('columns');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [transferModal, setTransferModal] = useState({
    isOpen: false,
    patient: null,
    currentDentistId: null
  });

  // Mock data for dentists and their queues
  const [dentists, setDentists] = useState([
    {
      id: 'D001',
      name: 'Dr. Carlos García',
      specialty: 'Odontología General',
      status: 'available',
      queueLength: 4,
      estimatedWaitTime: 25
    },
    {
      id: 'D002',
      name: 'Dra. María López',
      specialty: 'Endodoncia',
      status: 'busy',
      queueLength: 3,
      estimatedWaitTime: 35
    },
    {
      id: 'D003',
      name: 'Dr. José Martínez',
      specialty: 'Cirugía Oral',
      status: 'available',
      queueLength: 5,
      estimatedWaitTime: 20
    },
    {
      id: 'D004',
      name: 'Dra. Ana Rodríguez',
      specialty: 'Ortodoncia',
      status: 'break',
      queueLength: 2,
      estimatedWaitTime: 45
    }
  ]);

  // Mock patient queues
  const [patientQueues, setPatientQueues] = useState({
    'D001': [
      {
        id: 'P-2024-0892',
        name: 'Ana María Rodríguez',
        age: 34,
        phone: '+58 412-555-0123',
        service: 'Limpieza Dental',
        estimatedCost: '45.00 USD / 1,642 Bs',
        arrivalTime: '09:15',
        waitTime: 45,
        estimatedTime: 30,
        priority: 'normal',
        hasInsurance: true
      },
      {
        id: 'P-2024-0893',
        name: 'Carlos Mendoza',
        age: 28,
        phone: '+58 424-555-0124',
        service: 'Consulta General',
        estimatedCost: '25.00 USD / 912 Bs',
        arrivalTime: '09:30',
        waitTime: 30,
        estimatedTime: 20,
        priority: 'urgent',
        hasInsurance: false
      },
      {
        id: 'P-2024-0894',
        name: 'Luisa Fernández',
        age: 45,
        phone: '+58 414-555-0125',
        service: 'Extracción',
        estimatedCost: '80.00 USD / 2,916 Bs',
        arrivalTime: '09:45',
        waitTime: 15,
        estimatedTime: 45,
        priority: 'high',
        hasInsurance: true
      },
      {
        id: 'P-2024-0895',
        name: 'Pedro Jiménez',
        age: 52,
        phone: '+58 416-555-0126',
        service: 'Revisión',
        estimatedCost: '30.00 USD / 1,094 Bs',
        arrivalTime: '10:00',
        waitTime: 5,
        estimatedTime: 15,
        priority: 'normal',
        hasInsurance: false
      }
    ],
    'D002': [
      {
        id: 'P-2024-0896',
        name: 'Carmen Silva',
        age: 38,
        phone: '+58 412-555-0127',
        service: 'Endodoncia',
        estimatedCost: '150.00 USD / 5,468 Bs',
        arrivalTime: '08:45',
        waitTime: 75,
        estimatedTime: 90,
        priority: 'normal',
        hasInsurance: true
      },
      {
        id: 'P-2024-0897',
        name: 'Roberto Díaz',
        age: 41,
        phone: '+58 424-555-0128',
        service: 'Tratamiento de Conducto',
        estimatedCost: '120.00 USD / 4,374 Bs',
        arrivalTime: '09:00',
        waitTime: 60,
        estimatedTime: 75,
        priority: 'urgent',
        hasInsurance: false
      },
      {
        id: 'P-2024-0898',
        name: 'Elena Morales',
        age: 29,
        phone: '+58 414-555-0129',
        service: 'Consulta Especializada',
        estimatedCost: '40.00 USD / 1,458 Bs',
        arrivalTime: '09:20',
        waitTime: 40,
        estimatedTime: 30,
        priority: 'normal',
        hasInsurance: true
      }
    ],
    'D003': [
      {
        id: 'P-2024-0899',
        name: 'Miguel Torres',
        age: 35,
        phone: '+58 416-555-0130',
        service: 'Cirugía de Muelas del Juicio',
        estimatedCost: '200.00 USD / 7,290 Bs',
        arrivalTime: '08:30',
        waitTime: 90,
        estimatedTime: 120,
        priority: 'high',
        hasInsurance: true
      },
      {
        id: 'P-2024-0900',
        name: 'Sofía Herrera',
        age: 26,
        phone: '+58 412-555-0131',
        service: 'Extracción Simple',
        estimatedCost: '60.00 USD / 2,187 Bs',
        arrivalTime: '09:10',
        waitTime: 50,
        estimatedTime: 30,
        priority: 'normal',
        hasInsurance: false
      },
      {
        id: 'P-2024-0901',
        name: 'Andrés Vega',
        age: 43,
        phone: '+58 424-555-0132',
        service: 'Biopsia',
        estimatedCost: '180.00 USD / 6,561 Bs',
        arrivalTime: '09:25',
        waitTime: 35,
        estimatedTime: 60,
        priority: 'urgent',
        hasInsurance: true
      },
      {
        id: 'P-2024-0902',
        name: 'Gabriela Ruiz',
        age: 31,
        phone: '+58 414-555-0133',
        service: 'Consulta Pre-quirúrgica',
        estimatedCost: '35.00 USD / 1,276 Bs',
        arrivalTime: '09:40',
        waitTime: 20,
        estimatedTime: 25,
        priority: 'normal',
        hasInsurance: false
      },
      {
        id: 'P-2024-0903',
        name: 'Fernando Castro',
        age: 48,
        phone: '+58 416-555-0134',
        service: 'Implante Dental',
        estimatedCost: '300.00 USD / 10,935 Bs',
        arrivalTime: '09:55',
        waitTime: 5,
        estimatedTime: 150,
        priority: 'normal',
        hasInsurance: true
      }
    ],
    'D004': [
      {
        id: 'P-2024-0904',
        name: 'Valentina Moreno',
        age: 16,
        phone: '+58 412-555-0135',
        service: 'Consulta Ortodoncia',
        estimatedCost: '50.00 USD / 1,823 Bs',
        arrivalTime: '09:05',
        waitTime: 55,
        estimatedTime: 40,
        priority: 'normal',
        hasInsurance: true
      },
      {
        id: 'P-2024-0905',
        name: 'Diego Ramírez',
        age: 22,
        phone: '+58 424-555-0136',
        service: 'Ajuste de Brackets',
        estimatedCost: '30.00 USD / 1,094 Bs',
        arrivalTime: '09:35',
        waitTime: 25,
        estimatedTime: 20,
        priority: 'normal',
        hasInsurance: false
      }
    ]
  });

  // Calculate queue statistics
  const queueStats = {
    totalPatients: Object.values(patientQueues)?.flat()?.length,
    urgentPatients: Object.values(patientQueues)?.flat()?.filter(p => p?.priority === 'urgent')?.length,
    activeDentists: dentists?.filter(d => d?.status === 'available' || d?.status === 'busy')?.length,
    averageWaitTime: Math.round(
      Object.values(patientQueues)?.flat()?.reduce((sum, p) => sum + p?.waitTime, 0) / 
      Object.values(patientQueues)?.flat()?.length
    ),
    capacityUsed: Math.round((Object.values(patientQueues)?.flat()?.length / (dentists?.length * 8)) * 100),
    completedToday: 23
  };

  // Real-time updates simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setPatientQueues(prev => {
        const updated = { ...prev };
        Object.keys(updated)?.forEach(dentistId => {
          updated[dentistId] = updated?.[dentistId]?.map(patient => ({
            ...patient,
            waitTime: patient?.waitTime + 1
          }));
        });
        return updated;
      });
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  const handlePatientTransfer = (patientId, fromDentistId, toDentistId = null) => {
    if (toDentistId) {
      // Direct transfer (drag & drop)
      const patient = patientQueues?.[fromDentistId]?.find(p => p?.id === patientId);
      if (patient) {
        setPatientQueues(prev => ({
          ...prev,
          [fromDentistId]: prev?.[fromDentistId]?.filter(p => p?.id !== patientId),
          [toDentistId]: [...prev?.[toDentistId], patient]
        }));
      }
    } else {
      // Open transfer modal
      const patient = patientQueues?.[fromDentistId]?.find(p => p?.id === patientId);
      setTransferModal({
        isOpen: true,
        patient,
        currentDentistId: fromDentistId
      });
    }
  };

  const handleConfirmTransfer = async (transferData) => {
    const { patientId, fromDentistId, toDentistId, priority } = transferData;
    const patient = patientQueues?.[fromDentistId]?.find(p => p?.id === patientId);
    
    if (patient) {
      const updatedPatient = { ...patient, priority };
      setPatientQueues(prev => ({
        ...prev,
        [fromDentistId]: prev?.[fromDentistId]?.filter(p => p?.id !== patientId),
        [toDentistId]: [...prev?.[toDentistId], updatedPatient]
      }));
    }
  };

  const handlePatientPriority = (patientId, dentistId) => {
    setPatientQueues(prev => ({
      ...prev,
      [dentistId]: prev?.[dentistId]?.map(patient => 
        patient?.id === patientId 
          ? { 
              ...patient, 
              priority: patient?.priority === 'urgent' ? 'normal' : 
                       patient?.priority === 'high' ? 'urgent' : 'high'
            }
          : patient
      )
    }));
  };

  const handleStartConsultation = (patientId, dentistId) => {
    navigate(`/patient-consultation?patient=${patientId}&dentist=${dentistId}`);
  };

  const handleToggleAvailability = (dentistId) => {
    setDentists(prev => prev?.map(dentist => 
      dentist?.id === dentistId 
        ? { 
            ...dentist, 
            status: dentist?.status === 'available' ? 'break' : 'available'
          }
        : dentist
    ));
  };

  const handleEmergencyAdd = () => {
    navigate('/patient-registration?emergency=true');
  };

  const handleGlobalAction = (action) => {
    switch (action) {
      case 'addPatient': navigate('/patient-registration');
        break;
      case 'refresh':
        window.location?.reload();
        break;
      case 'settings': console.log('Open queue settings');
        break;
      case 'handleUrgent': console.log('Handle urgent patients');
        break;
      case 'redistribute': console.log('Redistribute patients');
        break;
      default:
        break;
    }
  };

  const handlePatientReorder = (dentistId, dragIndex, dropIndex) => {
    setPatientQueues(prev => {
      const updatedQueue = [...prev[dentistId]];
      const [removed] = updatedQueue.splice(dragIndex, 1);
      updatedQueue.splice(dropIndex, 0, removed);
      return {
        ...prev,
        [dentistId]: updatedQueue
      };
    });
  };

  const filteredQueues = () => {
    if (selectedFilter === 'all') return patientQueues;
    
    const filtered = {};
    Object.keys(patientQueues)?.forEach(dentistId => {
      filtered[dentistId] = patientQueues?.[dentistId]?.filter(patient => {
        switch (selectedFilter) {
          case 'urgent':
            return patient?.priority === 'urgent';
          case 'waiting':
            return patient?.waitTime > 0;
          case 'overdue':
            return patient?.waitTime > 60;
          default:
            return true;
        }
      });
    });
    return filtered;
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="min-h-screen bg-background">
        <Header />
        
        <main className="pt-16">
          <div className="max-w-7xl mx-auto p-6">
            {/* Page Header */}
            <div className="mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-foreground">Gestión de Colas</h1>
                  <p className="text-muted-foreground">
                    Monitoreo en tiempo real del flujo de pacientes
                  </p>
                </div>
                
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                    <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
                    <span>Actualización en vivo</span>
                  </div>
                  
                  <Button
                    variant="outline"
                    iconName="BarChart3"
                    onClick={() => setShowAnalytics(!showAnalytics)}
                  >
                    {showAnalytics ? 'Ocultar' : 'Mostrar'} Análisis
                  </Button>
                </div>
              </div>
            </div>

            {/* Control Bar */}
            <QueueControlBar
              queueStats={queueStats}
              onEmergencyAdd={handleEmergencyAdd}
              onGlobalAction={handleGlobalAction}
              onFilterChange={setSelectedFilter}
              onViewChange={setCurrentView}
            />

            {/* Analytics Panel */}
            {showAnalytics && (
              <div className="mb-6">
                <QueueAnalytics
                  isExpanded={showAnalytics}
                  onToggle={() => setShowAnalytics(!showAnalytics)}
                />
              </div>
            )}

            {/* Queue Columns */}
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-6">
              {dentists?.map(dentist => (
                <QueueColumn
                  key={dentist?.id}
                  dentist={dentist}
                  patients={filteredQueues()?.[dentist?.id] || []}
                  onPatientTransfer={handlePatientTransfer}
                  onPatientPriority={handlePatientPriority}
                  onStartConsultation={handleStartConsultation}
                  onToggleAvailability={handleToggleAvailability}
                  onPatientReorder={handlePatientReorder}
                />
              ))}
            </div>

            {/* Empty State */}
            {Object.values(filteredQueues())?.every(queue => queue?.length === 0) && (
              <div className="text-center py-12">
                <Icon name="Users" size={64} className="text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium text-foreground mb-2">
                  No hay pacientes en las colas
                </h3>
                <p className="text-muted-foreground mb-4">
                  {selectedFilter === 'all' ? 'Todas las colas están vacías en este momento' : 'No hay pacientes que coincidan con el filtro seleccionado'}
                </p>
                <Button
                  variant="outline"
                  iconName="UserPlus"
                  onClick={() => navigate('/patient-registration')}
                >
                  Registrar Nuevo Paciente
                </Button>
              </div>
            )}
          </div>
        </main>

        {/* Transfer Modal */}
        <TransferModal
          isOpen={transferModal?.isOpen}
          onClose={() => setTransferModal({ isOpen: false, patient: null, currentDentistId: null })}
          patient={transferModal?.patient}
          dentists={dentists}
          currentDentistId={transferModal?.currentDentistId}
          onConfirmTransfer={handleConfirmTransfer}
        />
      </div>
    </DndProvider>
  );
};

export default QueueManagementDashboard;