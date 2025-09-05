import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';
import Input from '../../../components/ui/Input';
import Button from '../../../components/ui/Button';

const PatientSearchPanel = ({ onPatientSelect, onNewRegistration }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);

  // Mock patient data
  const mockPatients = [
    {
      id: 'P-2024-0001',
      name: 'María Elena González',
      phone: '+58 412-555-0123',
      email: 'maria.gonzalez@email.com',
      cedula: 'V-12345678',
      age: 34,
      lastVisit: '2024-08-15',
      status: 'active',
      insurance: 'Seguros Caracas'
    },
    {
      id: 'P-2024-0002',
      name: 'Carlos Alberto Rodríguez',
      phone: '+58 414-555-0456',
      email: 'carlos.rodriguez@email.com',
      cedula: 'V-23456789',
      age: 28,
      lastVisit: '2024-07-22',
      status: 'active',
      insurance: 'Seguros Universales'
    },
    {
      id: 'P-2024-0003',
      name: 'Ana Beatriz Martínez',
      phone: '+58 416-555-0789',
      email: 'ana.martinez@email.com',
      cedula: 'V-34567890',
      age: 45,
      lastVisit: '2024-06-10',
      status: 'inactive',
      insurance: 'Sin Seguro'
    },
    {
      id: 'P-2024-0004',
      name: 'José Luis Hernández',
      phone: '+58 424-555-0321',
      email: 'jose.hernandez@email.com',
      cedula: 'V-45678901',
      age: 52,
      lastVisit: '2024-09-01',
      status: 'active',
      insurance: 'Seguros Mercantil'
    }
  ];

  useEffect(() => {
    if (searchQuery?.trim()?.length >= 2) {
      setIsSearching(true);
      
      // Simulate API call delay
      const timer = setTimeout(() => {
        const filtered = mockPatients?.filter(patient =>
          patient?.name?.toLowerCase()?.includes(searchQuery?.toLowerCase()) ||
          patient?.phone?.includes(searchQuery) ||
          patient?.cedula?.includes(searchQuery) ||
          patient?.id?.toLowerCase()?.includes(searchQuery?.toLowerCase())
        );
        setSearchResults(filtered);
        setIsSearching(false);
      }, 300);

      return () => clearTimeout(timer);
    } else {
      setSearchResults([]);
      setIsSearching(false);
    }
  }, [searchQuery]);

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
    if (onPatientSelect) {
      onPatientSelect(patient);
    }
  };

  const handleNewRegistration = () => {
    setSelectedPatient(null);
    setSearchQuery('');
    setSearchResults([]);
    if (onNewRegistration) {
      onNewRegistration();
    }
  };

  const getStatusColor = (status) => {
    return status === 'active' ? 'text-success' : 'text-muted-foreground';
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-foreground">Búsqueda de Pacientes</h2>
        <Button
          variant="outline"
          size="sm"
          iconName="UserPlus"
          iconPosition="left"
          onClick={handleNewRegistration}
        >
          Nuevo Paciente
        </Button>
      </div>
      {/* Search Input */}
      <div className="mb-6">
        <Input
          type="search"
          placeholder="Buscar por nombre, cédula, teléfono o ID..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e?.target?.value)}
          className="w-full"
        />
        <p className="text-sm text-muted-foreground mt-2">
          Ingrese al menos 2 caracteres para buscar
        </p>
      </div>
      {/* Search Results */}
      {isSearching && (
        <div className="flex items-center justify-center py-8">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm text-muted-foreground">Buscando pacientes...</span>
          </div>
        </div>
      )}
      {!isSearching && searchQuery?.trim()?.length >= 2 && searchResults?.length === 0 && (
        <div className="text-center py-8">
          <Icon name="Search" size={48} className="text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-medium text-foreground mb-2">No se encontraron pacientes</h3>
          <p className="text-sm text-muted-foreground mb-4">
            No hay pacientes que coincidan con "{searchQuery}"
          </p>
          <Button
            variant="primary"
            iconName="UserPlus"
            iconPosition="left"
            onClick={handleNewRegistration}
          >
            Registrar Nuevo Paciente
          </Button>
        </div>
      )}
      {!isSearching && searchResults?.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-foreground mb-3">
            Resultados ({searchResults?.length})
          </h3>
          
          {searchResults?.map((patient) => (
            <div
              key={patient?.id}
              className={`border border-border rounded-lg p-4 cursor-pointer transition-smooth hover:bg-muted ${
                selectedPatient?.id === patient?.id ? 'bg-primary/5 border-primary' : ''
              }`}
              onClick={() => handlePatientSelect(patient)}
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                      <Icon name="User" size={20} className="text-primary" />
                    </div>
                    <div>
                      <h4 className="font-medium text-foreground">{patient?.name}</h4>
                      <p className="text-sm text-muted-foreground">{patient?.id}</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                    <div className="flex items-center space-x-2">
                      <Icon name="CreditCard" size={14} className="text-muted-foreground" />
                      <span className="text-muted-foreground">Cédula:</span>
                      <span className="text-foreground">{patient?.cedula}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Icon name="Phone" size={14} className="text-muted-foreground" />
                      <span className="text-muted-foreground">Teléfono:</span>
                      <span className="text-foreground">{patient?.phone}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Icon name="Calendar" size={14} className="text-muted-foreground" />
                      <span className="text-muted-foreground">Última visita:</span>
                      <span className="text-foreground">{patient?.lastVisit}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Icon name="Shield" size={14} className="text-muted-foreground" />
                      <span className="text-muted-foreground">Seguro:</span>
                      <span className="text-foreground">{patient?.insurance}</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex flex-col items-end space-y-2">
                  <div className={`flex items-center space-x-1 ${getStatusColor(patient?.status)}`}>
                    <div className={`w-2 h-2 rounded-full ${patient?.status === 'active' ? 'bg-success' : 'bg-muted-foreground'}`}></div>
                    <span className="text-xs font-medium capitalize">{patient?.status}</span>
                  </div>
                  <span className="text-xs text-muted-foreground">{patient?.age} años</span>
                </div>
              </div>
              
              {selectedPatient?.id === patient?.id && (
                <div className="mt-4 pt-4 border-t border-border">
                  <div className="flex space-x-3">
                    <Button
                      variant="primary"
                      size="sm"
                      iconName="Clock"
                      iconPosition="left"
                      onClick={(e) => {
                        e?.stopPropagation();
                        // Handle add to queue
                      }}
                    >
                      Agregar a Cola
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      iconName="FileText"
                      iconPosition="left"
                      onClick={(e) => {
                        e?.stopPropagation();
                        // Handle view history
                      }}
                    >
                      Ver Historial
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      iconName="Edit"
                      iconPosition="left"
                      onClick={(e) => {
                        e?.stopPropagation();
                        // Handle edit patient
                      }}
                    >
                      Editar
                    </Button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
      {/* Quick Actions */}
      {!searchQuery && (
        <div className="mt-6 pt-6 border-t border-border">
          <h3 className="text-sm font-medium text-foreground mb-3">Acciones Rápidas</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <Button
              variant="outline"
              iconName="Users"
              iconPosition="left"
              onClick={() => {
                // Handle view all patients
              }}
            >
              Ver Todos los Pacientes
            </Button>
            <Button
              variant="outline"
              iconName="Download"
              iconPosition="left"
              onClick={() => {
                // Handle export patients
              }}
            >
              Exportar Lista
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientSearchPanel;