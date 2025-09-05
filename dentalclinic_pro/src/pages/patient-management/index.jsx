import React, { useState, useEffect } from 'react';
import Header from '../../components/ui/Header';
import Sidebar from '../../components/ui/Sidebar';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';
import PatientFilters from './components/PatientFilters';
import PatientList from './components/PatientList';
import PatientProfile from './components/PatientProfile';
import AddPatientModal from './components/AddPatientModal';

const PatientManagement = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [filters, setFilters] = useState({
    status: 'all',
    insurance: 'all',
    dentist: 'all',
    lastVisit: 'all'
  });

  // Mock patient data
  const [patients, setPatients] = useState([
    {
      id: 'PAT-001',
      firstName: 'María',
      lastName: 'García López',
      email: 'maria.garcia@email.com',
      phone: '+34 612 345 678',
      birthDate: '1985-03-15',
      gender: 'female',
      address: 'Calle Mayor 123, 2º A',
      city: 'Madrid',
      postalCode: '28001',
      province: 'Madrid',
      avatar: 'https://randomuser.me/api/portraits/women/1.jpg',
      status: 'active',
      lastVisit: '15/11/2024',
      assignedDentist: 'Dr. Martínez',
      insuranceCompany: 'Sanitas',
      policyNumber: 'SAN-123456789',
      insuranceExpiry: '2025-12-31',
      insuranceStatus: 'verified',
      bloodType: 'A+',
      allergies: 'Penicilina',
      medicalConditions: [
        { name: 'Hipertensión', date: '2020-05-10' },
        { name: 'Diabetes Tipo 2', date: '2021-08-15' }
      ],
      medications: [
        { name: 'Enalapril', dosage: '10mg', frequency: '1 vez al día' },
        { name: 'Metformina', dosage: '500mg', frequency: '2 veces al día' }
      ],
      appointments: [
        {
          date: '15/11/2024',
          time: '10:00',
          type: 'Limpieza dental',
          dentist: 'Dr. Martínez',
          status: 'completed',
          notes: 'Limpieza rutinaria completada sin complicaciones'
        },
        {
          date: '20/12/2024',
          time: '15:30',
          type: 'Revisión',
          dentist: 'Dr. Martínez',
          status: 'scheduled',
          notes: 'Revisión semestral programada'
        }
      ],
      treatments: [
        {
          name: 'Empaste composite',
          tooth: '16',
          date: '10/10/2024',
          status: 'completed',
          notes: 'Empaste en molar superior derecho'
        },
        {
          name: 'Endodoncia',
          tooth: '26',
          date: '25/12/2024',
          status: 'planned',
          notes: 'Tratamiento de conducto programado'
        }
      ],
      coverage: {
        consultations: '100%',
        cleanings: '80%',
        fillings: '70%',
        surgeries: '50%'
      }
    },
    {
      id: 'PAT-002',
      firstName: 'Carlos',
      lastName: 'Rodríguez Sánchez',
      email: 'carlos.rodriguez@email.com',
      phone: '+34 623 456 789',
      birthDate: '1978-07-22',
      gender: 'male',
      address: 'Avenida de la Paz 45, 1º B',
      city: 'Barcelona',
      postalCode: '08001',
      province: 'Barcelona',
      avatar: 'https://randomuser.me/api/portraits/men/2.jpg',
      status: 'overdue',
      lastVisit: '20/08/2024',
      assignedDentist: 'Dra. López',
      insuranceCompany: 'MAPFRE',
      policyNumber: 'MAP-987654321',
      insuranceExpiry: '2025-06-30',
      insuranceStatus: 'verified',
      bloodType: 'O-',
      allergies: 'Látex',
      medicalConditions: [],
      medications: [],
      appointments: [
        {
          date: '20/08/2024',
          time: '09:00',
          type: 'Consulta general',
          dentist: 'Dra. López',
          status: 'completed',
          notes: 'Revisión general, se detectó caries en molar'
        }
      ],
      treatments: [
        {
          name: 'Tratamiento de caries',
          tooth: '36',
          date: '15/01/2025',
          status: 'planned',
          notes: 'Empaste necesario en molar inferior izquierdo'
        }
      ],
      coverage: {
        consultations: '100%',
        cleanings: '75%',
        fillings: '60%',
        surgeries: '40%'
      }
    },
    {
      id: 'PAT-003',
      firstName: 'Ana',
      lastName: 'Martín Fernández',
      email: 'ana.martin@email.com',
      phone: '+34 634 567 890',
      birthDate: '1992-12-08',
      gender: 'female',
      address: 'Plaza del Sol 12, 3º C',
      city: 'Valencia',
      postalCode: '46001',
      province: 'Valencia',
      avatar: 'https://randomuser.me/api/portraits/women/3.jpg',
      status: 'scheduled',
      lastVisit: '05/11/2024',
      assignedDentist: 'Dr. García',
      insuranceCompany: 'Adeslas',
      policyNumber: 'ADE-456789123',
      insuranceExpiry: '2025-03-31',
      insuranceStatus: 'pending',
      bloodType: 'B+',
      allergies: 'Ninguna conocida',
      medicalConditions: [
        { name: 'Bruxismo', date: '2023-02-14' }
      ],
      medications: [],
      appointments: [
        {
          date: '05/11/2024',
          time: '16:00',
          type: 'Ortodoncia - Revisión',
          dentist: 'Dr. García',
          status: 'completed',
          notes: 'Ajuste de brackets, evolución favorable'
        },
        {
          date: '18/12/2024',
          time: '11:00',
          type: 'Ortodoncia - Ajuste',
          dentist: 'Dr. García',
          status: 'scheduled',
          notes: 'Ajuste mensual programado'
        }
      ],
      treatments: [
        {
          name: 'Tratamiento de ortodoncia',
          tooth: 'Múltiples',
          date: '15/01/2024',
          status: 'in-progress',
          notes: 'Tratamiento de ortodoncia en curso, duración estimada 18 meses'
        }
      ],
      coverage: {
        consultations: '100%',
        cleanings: '85%',
        fillings: '75%',
        surgeries: '55%'
      }
    },
    {
      id: 'PAT-004',
      firstName: 'Luis',
      lastName: 'Jiménez Torres',
      email: 'luis.jimenez@email.com',
      phone: '+34 645 678 901',
      birthDate: '1965-04-30',
      gender: 'male',
      address: 'Calle de la Rosa 78, Bajo',
      city: 'Sevilla',
      postalCode: '41001',
      province: 'Sevilla',
      avatar: 'https://randomuser.me/api/portraits/men/4.jpg',
      status: 'active',
      lastVisit: '28/11/2024',
      assignedDentist: 'Dra. Rodríguez',
      insuranceCompany: 'DKV',
      policyNumber: 'DKV-789123456',
      insuranceExpiry: '2025-09-30',
      insuranceStatus: 'verified',
      bloodType: 'AB+',
      allergies: 'Aspirina',
      medicalConditions: [
        { name: 'Enfermedad periodontal', date: '2022-11-20' }
      ],
      medications: [
        { name: 'Clorhexidina', dosage: '0.12%', frequency: 'Enjuague 2 veces al día' }
      ],
      appointments: [
        {
          date: '28/11/2024',
          time: '14:00',
          type: 'Tratamiento periodontal',
          dentist: 'Dra. Rodríguez',
          status: 'completed',
          notes: 'Curetaje y alisado radicular sector superior'
        }
      ],
      treatments: [
        {
          name: 'Tratamiento periodontal',
          tooth: 'Múltiples',
          date: '15/09/2024',
          status: 'in-progress',
          notes: 'Tratamiento periodontal en múltiples sesiones'
        }
      ],
      coverage: {
        consultations: '100%',
        cleanings: '90%',
        fillings: '80%',
        surgeries: '60%'
      }
    }
  ]);

  const [filteredPatients, setFilteredPatients] = useState(patients);

  // Filter patients based on search term and filters
  useEffect(() => {
    let filtered = patients;

    // Search filter
    if (searchTerm) {
      filtered = filtered?.filter(patient =>
        `${patient?.firstName} ${patient?.lastName}`?.toLowerCase()?.includes(searchTerm?.toLowerCase()) ||
        patient?.email?.toLowerCase()?.includes(searchTerm?.toLowerCase()) ||
        patient?.phone?.includes(searchTerm)
      );
    }

    // Status filter
    if (filters?.status !== 'all') {
      filtered = filtered?.filter(patient => patient?.status === filters?.status);
    }

    // Insurance filter
    if (filters?.insurance !== 'all') {
      if (filters?.insurance === 'none') {
        filtered = filtered?.filter(patient => !patient?.insuranceCompany);
      } else {
        filtered = filtered?.filter(patient => 
          patient?.insuranceCompany?.toLowerCase()?.includes(filters?.insurance?.toLowerCase())
        );
      }
    }

    // Dentist filter
    if (filters?.dentist !== 'all') {
      if (filters?.dentist === 'unassigned') {
        filtered = filtered?.filter(patient => !patient?.assignedDentist);
      } else {
        filtered = filtered?.filter(patient => 
          patient?.assignedDentist?.toLowerCase()?.includes(filters?.dentist?.toLowerCase())
        );
      }
    }

    // Last visit filter
    if (filters?.lastVisit !== 'all') {
      const now = new Date();
      filtered = filtered?.filter(patient => {
        if (patient?.lastVisit === 'Nuevo paciente') return filters?.lastVisit === 'over-6-months';
        
        const visitDate = new Date(patient.lastVisit.split('/').reverse().join('-'));
        const daysDiff = Math.floor((now - visitDate) / (1000 * 60 * 60 * 24));
        
        switch (filters?.lastVisit) {
          case 'last-week':
            return daysDiff <= 7;
          case 'last-month':
            return daysDiff <= 30;
          case 'last-3-months':
            return daysDiff <= 90;
          case 'last-6-months':
            return daysDiff <= 180;
          case 'over-6-months':
            return daysDiff > 180;
          default:
            return true;
        }
      });
    }

    setFilteredPatients(filtered);
  }, [searchTerm, filters, patients]);

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    setFilters({
      status: 'all',
      insurance: 'all',
      dentist: 'all',
      lastVisit: 'all'
    });
  };

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
  };

  const handlePatientUpdate = (updatedPatient) => {
    setPatients(prev => 
      prev?.map(patient => 
        patient?.id === updatedPatient?.id ? updatedPatient : patient
      )
    );
    setSelectedPatient(updatedPatient);
  };

  const handleAddPatient = (newPatient) => {
    setPatients(prev => [newPatient, ...prev]);
  };

  const handleScheduleAppointment = (patient) => {
    // Navigate to appointment scheduling with patient pre-selected
    window.location.href = `/appointment-scheduling?patient=${patient?.id}`;
  };

  return (
    <div className="min-h-screen bg-background">
      <Header 
        userRole="manager" 
        userName="Dr. Smith"
        isCollapsed={isSidebarCollapsed}
      />
      
      <Sidebar 
        userRole="manager"
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
      />

      <main className={`transition-all duration-300 ${
        isSidebarCollapsed ? 'ml-16' : 'ml-64'
      } mt-16`}>
        <div className="p-6">
          {/* Breadcrumb */}
          <nav className="flex items-center space-x-2 text-sm text-muted-foreground mb-6">
            <span>Dashboard</span>
            <Icon name="ChevronRight" size={16} />
            <span>Pacientes</span>
            <Icon name="ChevronRight" size={16} />
            <span className="text-foreground font-medium">Gestión de Pacientes</span>
          </nav>

          {/* Page Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-foreground">
                Gestión de Pacientes
              </h1>
              <p className="text-muted-foreground">
                Administra la base de datos de pacientes, historiales médicos y citas
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                iconName="FileText"
                iconPosition="left"
              >
                Generar Reporte
              </Button>
              <Button
                variant="default"
                onClick={() => setIsAddModalOpen(true)}
                iconName="UserPlus"
                iconPosition="left"
              >
                Agregar Paciente
              </Button>
            </div>
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-12 gap-6">
            {/* Left Panel - Patient Directory */}
            <div className="col-span-12 lg:col-span-4 space-y-6">
              <PatientFilters
                searchTerm={searchTerm}
                onSearchChange={setSearchTerm}
                filters={filters}
                onFilterChange={handleFilterChange}
                onClearFilters={handleClearFilters}
              />
              
              <PatientList
                patients={filteredPatients}
                selectedPatient={selectedPatient}
                onPatientSelect={handlePatientSelect}
              />
            </div>

            {/* Right Panel - Patient Profile */}
            <div className="col-span-12 lg:col-span-8">
              <PatientProfile
                patient={selectedPatient}
                onUpdate={handlePatientUpdate}
                onScheduleAppointment={handleScheduleAppointment}
              />
            </div>
          </div>
        </div>
      </main>

      {/* Add Patient Modal */}
      <AddPatientModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onAddPatient={handleAddPatient}
      />
    </div>
  );
};

export default PatientManagement;