import React, { useState, useEffect } from 'react';
import Header from '../../components/ui/Header';
import Sidebar from '../../components/ui/Sidebar';
import CalendarHeader from './components/CalendarHeader';
import CalendarGrid from './components/CalendarGrid';
import AppointmentSidebar from './components/AppointmentSidebar';
import AppointmentModal from './components/AppointmentModal';

const AppointmentScheduling = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [viewMode, setViewMode] = useState('day');
  const [selectedDentist, setSelectedDentist] = useState('all');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [userRole] = useState('secretary'); // This would come from auth context

  // Mock data
  const dentists = [
    {
      id: 'dent1',
      name: 'Dr. María González',
      specialty: 'Odontología General',
      available: true,
      color: '#3B82F6'
    },
    {
      id: 'dent2',
      name: 'Dr. Carlos Rodríguez',
      specialty: 'Endodoncia',
      available: true,
      color: '#10B981'
    },
    {
      id: 'dent3',
      name: 'Dra. Ana Martínez',
      specialty: 'Ortodoncia',
      available: false,
      color: '#8B5CF6'
    },
    {
      id: 'dent4',
      name: 'Dr. Luis Fernández',
      specialty: 'Cirugía Oral',
      available: true,
      color: '#F59E0B'
    }
  ];

  const patients = [
    {
      id: 'pat1',
      name: 'Carmen López',
      phone: '+34 612 345 678',
      email: 'carmen.lopez@email.com',
      lastVisit: '2024-07-15',
      allergies: 'Penicilina'
    },
    {
      id: 'pat2',
      name: 'Miguel Sánchez',
      phone: '+34 623 456 789',
      email: 'miguel.sanchez@email.com',
      lastVisit: '2024-07-20',
      allergies: 'Ninguna'
    },
    {
      id: 'pat3',
      name: 'Isabel Ruiz',
      phone: '+34 634 567 890',
      email: 'isabel.ruiz@email.com',
      lastVisit: '2024-07-25',
      allergies: 'Látex'
    },
    {
      id: 'pat4',
      name: 'Antonio García',
      phone: '+34 645 678 901',
      email: 'antonio.garcia@email.com',
      lastVisit: '2024-08-01',
      allergies: 'Ninguna'
    },
    {
      id: 'pat5',
      name: 'Rosa Jiménez',
      phone: '+34 656 789 012',
      email: 'rosa.jimenez@email.com',
      lastVisit: '2024-08-05',
      allergies: 'Anestesia local'
    }
  ];

  const appointments = [
    {
      id: 'apt1',
      patientId: 'pat1',
      patientName: 'Carmen López',
      dentistId: 'dent1',
      dentistName: 'Dr. María González',
      date: new Date()?.toDateString(),
      time: '09:00',
      duration: 30,
      service: 'Consulta General',
      type: 'consultation',
      status: 'confirmed',
      notes: 'Primera consulta, revisar historial médico'
    },
    {
      id: 'apt2',
      patientId: 'pat2',
      patientName: 'Miguel Sánchez',
      dentistId: 'dent2',
      dentistName: 'Dr. Carlos Rodríguez',
      date: new Date()?.toDateString(),
      time: '10:30',
      duration: 60,
      service: 'Endodoncia',
      type: 'treatment',
      status: 'confirmed',
      notes: 'Tratamiento de conducto en molar superior'
    },
    {
      id: 'apt3',
      patientId: 'pat3',
      patientName: 'Isabel Ruiz',
      dentistId: 'dent1',
      dentistName: 'Dr. María González',
      date: new Date()?.toDateString(),
      time: '12:00',
      duration: 45,
      service: 'Limpieza Dental',
      type: 'cleaning',
      status: 'pending',
      notes: 'Limpieza profunda y revisión general'
    },
    {
      id: 'apt4',
      patientId: 'pat4',
      patientName: 'Antonio García',
      dentistId: 'dent3',
      dentistName: 'Dra. Ana Martínez',
      date: new Date()?.toDateString(),
      time: '14:00',
      duration: 30,
      service: 'Consulta Ortodoncia',
      type: 'consultation',
      status: 'confirmed',
      notes: 'Evaluación para brackets'
    },
    {
      id: 'apt5',
      patientId: 'pat5',
      patientName: 'Rosa Jiménez',
      dentistId: 'dent4',
      dentistName: 'Dr. Luis Fernández',
      date: new Date()?.toDateString(),
      time: '16:30',
      duration: 90,
      service: 'Extracción',
      type: 'treatment',
      status: 'confirmed',
      notes: 'Extracción de muela del juicio'
    }
  ];

  const waitList = [
    {
      id: 'wait1',
      name: 'Pedro Morales',
      phone: '+34 667 890 123',
      requestedService: 'Consulta de Emergencia',
      waitTime: '45 min',
      priority: 'high'
    },
    {
      id: 'wait2',
      name: 'Lucía Herrera',
      phone: '+34 678 901 234',
      requestedService: 'Limpieza Dental',
      waitTime: '2 horas',
      priority: 'normal'
    },
    {
      id: 'wait3',
      name: 'Javier Castillo',
      phone: '+34 689 012 345',
      requestedService: 'Consulta General',
      waitTime: '1 hora',
      priority: 'normal'
    }
  ];

  const cancellations = [
    {
      id: 'canc1',
      patientName: 'Elena Vázquez',
      originalTime: '11:00',
      service: 'Empaste',
      reason: 'Enfermedad',
      cancelledAt: '08:30'
    },
    {
      id: 'canc2',
      patientName: 'Roberto Silva',
      originalTime: '15:30',
      service: 'Consulta',
      reason: 'Emergencia familiar',
      cancelledAt: '14:00'
    }
  ];

  const handleAppointmentClick = (appointment) => {
    setSelectedAppointment(appointment);
    setIsModalOpen(true);
  };

  const handleTimeSlotClick = (dentistId, timeSlot) => {
    setSelectedAppointment(null);
    setIsModalOpen(true);
  };

  const handlePatientClick = (patient) => {
    console.log('Patient clicked:', patient);
  };

  const handleSaveAppointment = (appointmentData) => {
    console.log('Saving appointment:', appointmentData);
    // Here you would typically save to your backend
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedAppointment(null);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header userRole={userRole} userName="María Secretaria" />
      
      <div className="flex">
        <Sidebar 
          userRole={userRole}
          isCollapsed={isSidebarCollapsed}
          onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        />
        
        <main className={`flex-1 transition-all duration-300 ${
          isSidebarCollapsed ? 'ml-16' : 'ml-64'
        } mt-16`}>
          <div className="flex h-[calc(100vh-4rem)]">
            {/* Main Calendar Area */}
            <div className="flex-1 flex flex-col">
              <CalendarHeader
                currentDate={currentDate}
                onDateChange={setCurrentDate}
                viewMode={viewMode}
                onViewModeChange={setViewMode}
                selectedDentist={selectedDentist}
                onDentistChange={setSelectedDentist}
                dentists={dentists}
              />
              
              <CalendarGrid
                viewMode={viewMode}
                currentDate={currentDate}
                appointments={appointments}
                dentists={dentists}
                selectedDentist={selectedDentist}
                onAppointmentClick={handleAppointmentClick}
                onTimeSlotClick={handleTimeSlotClick}
              />
            </div>
            
            {/* Right Sidebar */}
            <AppointmentSidebar
              currentDate={currentDate}
              appointments={appointments}
              waitList={waitList}
              cancellations={cancellations}
              onPatientClick={handlePatientClick}
            />
          </div>
        </main>
      </div>

      {/* Appointment Modal */}
      <AppointmentModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        appointment={selectedAppointment}
        dentists={dentists}
        patients={patients}
        onSave={handleSaveAppointment}
      />
    </div>
  );
};

export default AppointmentScheduling;