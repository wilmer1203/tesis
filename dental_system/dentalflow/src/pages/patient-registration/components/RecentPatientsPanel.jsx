import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const RecentPatientsPanel = ({ onAddToQueue, onViewPatient }) => {
  const [recentPatients, setRecentPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);

  // Mock recent patients data
  const mockRecentPatients = [
    {
      id: 'P-2024-0892',
      name: 'Ana María Rodríguez',
      age: 34,
      phone: '+58 412-555-0123',
      registrationTime: new Date(Date.now() - 300000), // 5 minutes ago
      status: 'registered',
      preferredCurrency: 'BS',
      insurance: 'Seguros Caracas',
      allergies: ['Penicilina']
    },
    {
      id: 'P-2024-0891',
      name: 'Carlos Eduardo Pérez',
      age: 28,
      phone: '+58 414-555-0456',
      registrationTime: new Date(Date.now() - 900000), // 15 minutes ago
      status: 'in-queue',
      preferredCurrency: 'USD',
      insurance: 'Sin Seguro',
      allergies: []
    },
    {
      id: 'P-2024-0890',
      name: 'María José González',
      age: 45,
      phone: '+58 416-555-0789',
      registrationTime: new Date(Date.now() - 1800000), // 30 minutes ago
      status: 'completed',
      preferredCurrency: 'MIXED',
      insurance: 'Seguros Universales',
      allergies: ['Látex', 'Lidocaína']
    },
    {
      id: 'P-2024-0889',
      name: 'José Luis Martínez',
      age: 52,
      phone: '+58 424-555-0321',
      registrationTime: new Date(Date.now() - 2700000), // 45 minutes ago
      status: 'registered',
      preferredCurrency: 'BS',
      insurance: 'Seguros Mercantil',
      allergies: []
    },
    {
      id: 'P-2024-0888',
      name: 'Carmen Elena Herrera',
      age: 38,
      phone: '+58 426-555-0654',
      registrationTime: new Date(Date.now() - 3600000), // 1 hour ago
      status: 'in-queue',
      preferredCurrency: 'USD',
      insurance: 'Sin Seguro',
      allergies: ['Aspirina']
    }
  ];

  useEffect(() => {
    setRecentPatients(mockRecentPatients);
  }, []);

  const getStatusConfig = (status) => {
    switch (status) {
      case 'registered':
        return {
          color: 'text-primary',
          bg: 'bg-primary/10',
          icon: 'UserCheck',
          label: 'Registrado'
        };
      case 'in-queue':
        return {
          color: 'text-warning',
          bg: 'bg-warning/10',
          icon: 'Clock',
          label: 'En Cola'
        };
      case 'completed':
        return {
          color: 'text-success',
          bg: 'bg-success/10',
          icon: 'CheckCircle',
          label: 'Completado'
        };
      default:
        return {
          color: 'text-muted-foreground',
          bg: 'bg-muted',
          icon: 'User',
          label: 'Desconocido'
        };
    }
  };

  const getCurrencyDisplay = (currency) => {
    switch (currency) {
      case 'BS':
        return { label: 'BS', color: 'text-success' };
      case 'USD':
        return { label: 'USD', color: 'text-primary' };
      case 'MIXED':
        return { label: 'Mixto', color: 'text-warning' };
      default:
        return { label: 'N/A', color: 'text-muted-foreground' };
    }
  };

  const formatTimeAgo = (date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Hace un momento';
    if (diffInMinutes < 60) return `Hace ${diffInMinutes} min`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `Hace ${diffInHours}h`;
    
    return date?.toLocaleDateString('es-VE');
  };

  const handleAddToQueue = (patient) => {
    if (onAddToQueue) {
      onAddToQueue(patient);
    }
  };

  const handleViewPatient = (patient) => {
    setSelectedPatient(patient);
    if (onViewPatient) {
      onViewPatient(patient);
    }
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-foreground">Pacientes Recientes</h2>
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            iconName="RefreshCw"
            onClick={() => {
              // Refresh recent patients
              setRecentPatients([...mockRecentPatients]);
            }}
          />
          <Button
            variant="outline"
            size="sm"
            iconName="Users"
            iconPosition="left"
            onClick={() => {
              // View all patients
            }}
          >
            Ver Todos
          </Button>
        </div>
      </div>
      {recentPatients?.length === 0 ? (
        <div className="text-center py-8">
          <Icon name="Users" size={48} className="text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-medium text-foreground mb-2">No hay pacientes recientes</h3>
          <p className="text-sm text-muted-foreground">
            Los pacientes registrados recientemente aparecerán aquí
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {recentPatients?.map((patient) => {
            const statusConfig = getStatusConfig(patient?.status);
            const currencyConfig = getCurrencyDisplay(patient?.preferredCurrency);
            
            return (
              <div
                key={patient?.id}
                className={`border border-border rounded-lg p-4 transition-smooth hover:bg-muted cursor-pointer ${
                  selectedPatient?.id === patient?.id ? 'bg-primary/5 border-primary' : ''
                }`}
                onClick={() => handleViewPatient(patient)}
              >
                <div className="flex items-start justify-between">
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
                    
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm mb-3">
                      <div className="flex items-center space-x-2">
                        <Icon name="Calendar" size={14} className="text-muted-foreground" />
                        <span className="text-muted-foreground">Edad:</span>
                        <span className="text-foreground">{patient?.age} años</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Icon name="Phone" size={14} className="text-muted-foreground" />
                        <span className="text-muted-foreground">Tel:</span>
                        <span className="text-foreground">{patient?.phone}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Icon name="DollarSign" size={14} className="text-muted-foreground" />
                        <span className="text-muted-foreground">Moneda:</span>
                        <span className={`font-medium ${currencyConfig?.color}`}>
                          {currencyConfig?.label}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Icon name="Shield" size={14} className="text-muted-foreground" />
                        <span className="text-muted-foreground">Seguro:</span>
                        <span className="text-foreground text-xs">{patient?.insurance}</span>
                      </div>
                    </div>

                    {patient?.allergies?.length > 0 && (
                      <div className="flex items-center space-x-2 mb-3">
                        <Icon name="AlertTriangle" size={14} className="text-warning" />
                        <span className="text-xs text-warning font-medium">
                          Alergias: {patient?.allergies?.join(', ')}
                        </span>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-col items-end space-y-2">
                    <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${statusConfig?.bg}`}>
                      <Icon name={statusConfig?.icon} size={14} className={statusConfig?.color} />
                      <span className={`text-xs font-medium ${statusConfig?.color}`}>
                        {statusConfig?.label}
                      </span>
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {formatTimeAgo(patient?.registrationTime)}
                    </span>
                  </div>
                </div>
                {/* Quick Actions */}
                <div className="flex items-center justify-between mt-4 pt-3 border-t border-border">
                  <div className="flex space-x-2">
                    {patient?.status === 'registered' && (
                      <Button
                        variant="primary"
                        size="sm"
                        iconName="Clock"
                        iconPosition="left"
                        onClick={(e) => {
                          e?.stopPropagation();
                          handleAddToQueue(patient);
                        }}
                      >
                        Agregar a Cola
                      </Button>
                    )}
                    
                    {patient?.status === 'in-queue' && (
                      <Button
                        variant="outline"
                        size="sm"
                        iconName="Eye"
                        iconPosition="left"
                        onClick={(e) => {
                          e?.stopPropagation();
                          // View queue status
                        }}
                      >
                        Ver en Cola
                      </Button>
                    )}
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      iconName="FileText"
                      iconPosition="left"
                      onClick={(e) => {
                        e?.stopPropagation();
                        // View patient history
                      }}
                    >
                      Historial
                    </Button>
                  </div>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    iconName="Edit"
                    onClick={(e) => {
                      e?.stopPropagation();
                      // Edit patient
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}
      {/* Summary Stats */}
      <div className="mt-6 pt-6 border-t border-border">
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary">
              {recentPatients?.filter(p => p?.status === 'registered')?.length}
            </div>
            <div className="text-xs text-muted-foreground">Registrados</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-warning">
              {recentPatients?.filter(p => p?.status === 'in-queue')?.length}
            </div>
            <div className="text-xs text-muted-foreground">En Cola</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-success">
              {recentPatients?.filter(p => p?.status === 'completed')?.length}
            </div>
            <div className="text-xs text-muted-foreground">Completados</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecentPatientsPanel;