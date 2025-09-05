import React, { useState, useEffect } from 'react';
import Header from '../../components/ui/Header';
import Sidebar from '../../components/ui/Sidebar';
import DashboardStats from './components/DashboardStats';
import PatientFilters from './components/PatientFilters';
import PatientCard from './components/PatientCard';
import OdontogramViewer from './components/OdontogramViewer';
import PatientNotes from './components/PatientNotes';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const DentistDashboard = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [activeTab, setActiveTab] = useState('odontogram');
  const [filters, setFilters] = useState({
    search: '',
    dateRange: '',
    urgency: '',
    status: '',
    quickFilter: ''
  });

  // Mock data for assigned patients
  const mockPatients = [
    {
      id: 'P001',
      nombre: 'María',
      apellido: 'González',
      edad: 34,
      telefono: '+34 612 345 678',
      email: 'maria.gonzalez@email.com',
      urgencia: 'alta',
      estado_tratamiento: 'en_tratamiento',
      progreso_tratamiento: 65,
      proxima_cita: {
        fecha: '2024-12-12',
        hora: '10:30:00'
      },
      ultima_visita: '2024-12-08',
      condiciones_medicas: ['Diabetes', 'Hipertensión'],
      alergias: ['Penicilina'],
      odontograma: {
        16: 'C',
        17: 'O',
        26: 'C',
        36: 'E',
        46: 'I'
      },
      notas_clinicas: []
    },
    {
      id: 'P002',
      nombre: 'Carlos',
      apellido: 'Rodríguez',
      edad: 28,
      telefono: '+34 623 456 789',
      email: 'carlos.rodriguez@email.com',
      urgencia: 'media',
      estado_tratamiento: 'pendiente',
      progreso_tratamiento: 25,
      proxima_cita: {
        fecha: '2024-12-12',
        hora: '14:00:00'
      },
      ultima_visita: '2024-12-05',
      condiciones_medicas: [],
      alergias: [],
      odontograma: {
        11: 'C',
        21: 'C',
        31: 'O'
      },
      notas_clinicas: []
    },
    {
      id: 'P003',
      nombre: 'Ana',
      apellido: 'Martínez',
      edad: 45,
      telefono: '+34 634 567 890',
      email: 'ana.martinez@email.com',
      urgencia: 'baja',
      estado_tratamiento: 'completado',
      progreso_tratamiento: 100,
      proxima_cita: {
        fecha: '2024-12-15',
        hora: '09:00:00'
      },
      ultima_visita: '2024-12-10',
      condiciones_medicas: ['Osteoporosis'],
      alergias: [],
      odontograma: {
        14: 'O',
        15: 'O',
        24: 'O',
        25: 'O'
      },
      notas_clinicas: []
    },
    {
      id: 'P004',
      nombre: 'Luis',
      apellido: 'Fernández',
      edad: 52,
      telefono: '+34 645 678 901',
      email: 'luis.fernandez@email.com',
      urgencia: 'alta',
      estado_tratamiento: 'en_tratamiento',
      progreso_tratamiento: 40,
      proxima_cita: {
        fecha: '2024-12-12',
        hora: '16:30:00'
      },
      ultima_visita: '2024-12-09',
      condiciones_medicas: ['Cardiopatía'],
      alergias: ['Látex', 'Ibuprofeno'],
      odontograma: {
        18: 'E',
        28: 'E',
        38: 'E',
        48: 'E',
        16: 'R',
        26: 'R'
      },
      notas_clinicas: []
    },
    {
      id: 'P005',
      nombre: 'Elena',
      apellido: 'López',
      edad: 29,
      telefono: '+34 656 789 012',
      email: 'elena.lopez@email.com',
      urgencia: 'media',
      estado_tratamiento: 'en_tratamiento',
      progreso_tratamiento: 80,
      proxima_cita: {
        fecha: '2024-12-13',
        hora: '11:15:00'
      },
      ultima_visita: '2024-12-07',
      condiciones_medicas: [],
      alergias: [],
      odontograma: {
        12: 'O',
        22: 'O',
        32: 'C',
        42: 'C'
      },
      notas_clinicas: []
    },
    {
      id: 'P006',
      nombre: 'Roberto',
      apellido: 'Sánchez',
      edad: 38,
      telefono: '+34 667 890 123',
      email: 'roberto.sanchez@email.com',
      urgencia: 'baja',
      estado_tratamiento: 'pendiente',
      progreso_tratamiento: 10,
      proxima_cita: {
        fecha: '2024-12-14',
        hora: '15:45:00'
      },
      ultima_visita: '2024-12-06',
      condiciones_medicas: [],
      alergias: [],
      odontograma: {
        13: 'C',
        23: 'C'
      },
      notas_clinicas: []
    }
  ];

  const [patients, setPatients] = useState(mockPatients);

  // Filter patients based on current filters
  const filteredPatients = patients?.filter(patient => {
    // Search filter
    if (filters?.search) {
      const searchTerm = filters?.search?.toLowerCase();
      const matchesSearch = 
        patient?.nombre?.toLowerCase()?.includes(searchTerm) ||
        patient?.apellido?.toLowerCase()?.includes(searchTerm) ||
        patient?.id?.toLowerCase()?.includes(searchTerm) ||
        patient?.telefono?.includes(searchTerm);
      
      if (!matchesSearch) return false;
    }

    // Urgency filter
    if (filters?.urgency && patient?.urgencia !== filters?.urgency) {
      return false;
    }

    // Status filter
    if (filters?.status && patient?.estado_tratamiento !== filters?.status) {
      return false;
    }

    // Quick filters
    if (filters?.quickFilter) {
      switch (filters?.quickFilter) {
        case 'urgent':
          return patient?.urgencia === 'alta';
        case 'today':
          const today = new Date()?.toISOString()?.split('T')?.[0];
          return patient?.proxima_cita?.fecha === today;
        case 'medical_conditions':
          return patient?.condiciones_medicas && patient?.condiciones_medicas?.length > 0;
        case 'allergies':
          return patient?.alergias && patient?.alergias?.length > 0;
        default:
          return true;
      }
    }

    return true;
  });

  // Dashboard statistics
  const dashboardStats = {
    pacientes_asignados: patients?.length,
    citas_hoy: patients?.filter(p => {
      const today = new Date()?.toISOString()?.split('T')?.[0];
      return p?.proxima_cita?.fecha === today;
    })?.length,
    tratamientos_pendientes: patients?.filter(p => 
      p?.estado_tratamiento === 'pendiente' || p?.estado_tratamiento === 'en_tratamiento'
    )?.length,
    urgencias: patients?.filter(p => p?.urgencia === 'alta')?.length
  };

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
  };

  const handleFiltersChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleClearFilters = () => {
    setFilters({
      search: '',
      dateRange: '',
      urgency: '',
      status: '',
      quickFilter: ''
    });
  };

  const handleUpdateOdontogram = (toothId, treatment) => {
    if (selectedPatient) {
      const updatedPatient = {
        ...selectedPatient,
        odontograma: {
          ...selectedPatient?.odontograma,
          [toothId]: treatment
        }
      };
      
      setSelectedPatient(updatedPatient);
      
      // Update in patients array
      setPatients(prev => prev?.map(p => 
        p?.id === selectedPatient?.id ? updatedPatient : p
      ));
    }
  };

  const handleSaveOdontogramChanges = () => {
    // In a real app, this would save to backend
    console.log('Odontogram changes saved for patient:', selectedPatient?.id);
  };

  const handleAddNote = (note) => {
    if (selectedPatient) {
      const updatedPatient = {
        ...selectedPatient,
        notas_clinicas: [note, ...(selectedPatient?.notas_clinicas || [])]
      };
      
      setSelectedPatient(updatedPatient);
      
      // Update in patients array
      setPatients(prev => prev?.map(p => 
        p?.id === selectedPatient?.id ? updatedPatient : p
      ));
    }
  };

  const handleUpdateNote = (updatedNote) => {
    if (selectedPatient) {
      const updatedPatient = {
        ...selectedPatient,
        notas_clinicas: selectedPatient?.notas_clinicas?.map(note =>
          note?.id === updatedNote?.id ? updatedNote : note
        )
      };
      
      setSelectedPatient(updatedPatient);
      
      // Update in patients array
      setPatients(prev => prev?.map(p => 
        p?.id === selectedPatient?.id ? updatedPatient : p
      ));
    }
  };

  // Auto-select first patient on load
  useEffect(() => {
    if (filteredPatients?.length > 0 && !selectedPatient) {
      setSelectedPatient(filteredPatients?.[0]);
    }
  }, [filteredPatients, selectedPatient]);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <Header 
        userRole="dentist" 
        userName="Dr. García"
        isCollapsed={sidebarCollapsed}
      />
      {/* Sidebar */}
      <Sidebar
        userRole="dentist"
        isCollapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      {/* Main Content */}
      <main className={`pt-16 transition-all duration-300 ${
        sidebarCollapsed ? 'ml-16' : 'ml-64'
      }`}>
        <div className="p-6">
          {/* Page Header */}
          <div className="mb-6">
            <div className="flex items-center space-x-3 mb-2">
              <Icon name="Stethoscope" size={24} color="var(--color-primary)" />
              <h1 className="text-2xl font-bold text-foreground">
                Panel del Dentista
              </h1>
            </div>
            <p className="text-muted-foreground">
              Gestión clínica y documentación de pacientes asignados
            </p>
          </div>

          {/* Dashboard Statistics */}
          <DashboardStats stats={dashboardStats} />

          {/* Main Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Panel - Patient List */}
            <div className="lg:col-span-5">
              <div className="space-y-6">
                {/* Patient Filters */}
                <PatientFilters
                  filters={filters}
                  onFiltersChange={handleFiltersChange}
                  onClearFilters={handleClearFilters}
                  totalPatients={patients?.length}
                  filteredCount={filteredPatients?.length}
                />

                {/* Patient List */}
                <div className="bg-card border border-border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-card-foreground">
                      Pacientes Asignados
                    </h3>
                    <span className="text-sm text-muted-foreground">
                      {filteredPatients?.length} pacientes
                    </span>
                  </div>

                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {filteredPatients?.length === 0 ? (
                      <div className="text-center py-8">
                        <Icon 
                          name="Users" 
                          size={48} 
                          color="var(--color-muted-foreground)" 
                          className="mx-auto mb-3 opacity-50" 
                        />
                        <p className="text-sm text-muted-foreground">
                          No se encontraron pacientes con los filtros aplicados
                        </p>
                      </div>
                    ) : (
                      filteredPatients?.map((patient) => (
                        <PatientCard
                          key={patient?.id}
                          patient={patient}
                          onSelectPatient={handlePatientSelect}
                          isSelected={selectedPatient?.id === patient?.id}
                        />
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Right Panel - Clinical Workspace */}
            <div className="lg:col-span-7">
              {selectedPatient ? (
                <div className="space-y-6">
                  {/* Patient Info Header */}
                  <div className="bg-card border border-border rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h2 className="text-xl font-semibold text-card-foreground">
                          {selectedPatient?.nombre} {selectedPatient?.apellido}
                        </h2>
                        <p className="text-sm text-muted-foreground">
                          ID: {selectedPatient?.id} • {selectedPatient?.edad} años • 
                          Progreso: {selectedPatient?.progreso_tratamiento}%
                        </p>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Button
                          variant={activeTab === 'odontogram' ? 'default' : 'outline'}
                          size="sm"
                          iconName="Stethoscope"
                          iconPosition="left"
                          iconSize={16}
                          onClick={() => setActiveTab('odontogram')}
                        >
                          Odontograma
                        </Button>
                        <Button
                          variant={activeTab === 'notes' ? 'default' : 'outline'}
                          size="sm"
                          iconName="FileText"
                          iconPosition="left"
                          iconSize={16}
                          onClick={() => setActiveTab('notes')}
                        >
                          Notas
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Clinical Workspace */}
                  {activeTab === 'odontogram' ? (
                    <OdontogramViewer
                      patient={selectedPatient}
                      onUpdateOdontogram={handleUpdateOdontogram}
                      onSaveChanges={handleSaveOdontogramChanges}
                    />
                  ) : (
                    <PatientNotes
                      patient={selectedPatient}
                      onAddNote={handleAddNote}
                      onUpdateNote={handleUpdateNote}
                    />
                  )}
                </div>
              ) : (
                <div className="bg-card border border-border rounded-lg p-8 text-center">
                  <Icon 
                    name="UserCheck" 
                    size={64} 
                    color="var(--color-muted-foreground)" 
                    className="mx-auto mb-4 opacity-50" 
                  />
                  <h3 className="text-lg font-medium text-card-foreground mb-2">
                    Seleccione un Paciente
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Elija un paciente de la lista para ver su odontograma y notas clínicas
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DentistDashboard;