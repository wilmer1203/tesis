import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Image from '../../../components/AppImage';

const ParticipatingDentistsPanel = ({ onDentistAdd, onDentistRemove }) => {
  const [showAddDentist, setShowAddDentist] = useState(false);
  const [participatingDentists, setParticipatingDentists] = useState([
    {
      id: 'dr-gonzalez',
      name: 'Dr. María González',
      specialty: 'Odontología General',
      role: 'primary',
      joinTime: new Date(Date.now() - 7200000),
      interventions: 2,
      totalCost: { bs: 4300, usd: 117.97 },
      status: 'active',
      avatar: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&h=150&fit=crop&crop=face'
    },
    {
      id: 'dr-mendoza',
      name: 'Dr. Carlos Mendoza',
      specialty: 'Endodoncia',
      role: 'consultant',
      joinTime: new Date(Date.now() - 3600000),
      interventions: 1,
      totalCost: { bs: 2800, usd: 76.82 },
      status: 'active',
      avatar: 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=150&h=150&fit=crop&crop=face'
    }
  ]);

  const availableDentists = [
    {
      id: 'dr-silva',
      name: 'Dr. Ana Silva',
      specialty: 'Ortodoncia',
      status: 'available',
      avatar: 'https://images.unsplash.com/photo-1594824388853-e0e5e5e7b9b7?w=150&h=150&fit=crop&crop=face'
    },
    {
      id: 'dr-torres',
      name: 'Dr. Luis Torres',
      specialty: 'Cirugía Oral',
      status: 'busy',
      avatar: 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150&h=150&fit=crop&crop=face'
    },
    {
      id: 'dr-ramirez',
      name: 'Dr. Carmen Ramírez',
      specialty: 'Periodoncia',
      status: 'available',
      avatar: 'https://images.unsplash.com/photo-1607990281513-2c110a25bd8c?w=150&h=150&fit=crop&crop=face'
    }
  ];

  const handleAddDentist = (dentist) => {
    const newParticipant = {
      ...dentist,
      role: 'consultant',
      joinTime: new Date(),
      interventions: 0,
      totalCost: { bs: 0, usd: 0 },
      status: 'active'
    };

    setParticipatingDentists(prev => [...prev, newParticipant]);
    setShowAddDentist(false);

    if (onDentistAdd) {
      onDentistAdd(newParticipant);
    }
  };

  const handleRemoveDentist = (dentistId) => {
    setParticipatingDentists(prev => prev?.filter(d => d?.id !== dentistId));
    
    if (onDentistRemove) {
      onDentistRemove(dentistId);
    }
  };

  const getRoleLabel = (role) => {
    switch (role) {
      case 'primary':
        return 'Principal';
      case 'consultant':
        return 'Consultor';
      case 'assistant':
        return 'Asistente';
      default:
        return role;
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'primary':
        return 'text-primary bg-primary/10';
      case 'consultant':
        return 'text-success bg-success/10';
      case 'assistant':
        return 'text-warning bg-warning/10';
      default:
        return 'text-muted-foreground bg-muted';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'available':
        return 'text-success';
      case 'busy':
        return 'text-warning';
      case 'offline':
        return 'text-error';
      default:
        return 'text-muted-foreground';
    }
  };

  const totalCost = participatingDentists?.reduce((sum, dentist) => ({
    bs: sum?.bs + dentist?.totalCost?.bs,
    usd: sum?.usd + dentist?.totalCost?.usd
  }), { bs: 0, usd: 0 });

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="Users" size={20} className="text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Dentistas Participantes</h2>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowAddDentist(!showAddDentist)}
        >
          <Icon name="Plus" size={16} className="mr-2" />
          Agregar
        </Button>
      </div>
      <div className="p-4 space-y-4">
        {/* Summary */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-primary/5 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-primary">{participatingDentists?.length}</div>
            <div className="text-xs text-muted-foreground">Dentistas</div>
          </div>
          <div className="bg-success/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-success">{totalCost?.bs?.toLocaleString()}</div>
            <div className="text-xs text-muted-foreground">Total Bs</div>
          </div>
          <div className="bg-success/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-success">${totalCost?.usd?.toFixed(2)}</div>
            <div className="text-xs text-muted-foreground">Total USD</div>
          </div>
        </div>

        {/* Participating Dentists List */}
        <div className="space-y-3">
          {participatingDentists?.map((dentist) => (
            <div key={dentist?.id} className="bg-muted/30 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 rounded-full overflow-hidden bg-muted flex-shrink-0">
                    <Image
                      src={dentist?.avatar}
                      alt={`Foto de ${dentist?.name}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h3 className="font-medium text-foreground">{dentist?.name}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRoleColor(dentist?.role)}`}>
                        {getRoleLabel(dentist?.role)}
                      </span>
                      <div className={`w-2 h-2 rounded-full ${dentist?.status === 'active' ? 'bg-success' : 'bg-muted-foreground'}`}></div>
                    </div>
                    <div className="text-sm text-muted-foreground mb-2">{dentist?.specialty}</div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <span className="text-muted-foreground">Ingresó:</span>
                        <span className="ml-1 text-foreground">
                          {dentist?.joinTime?.toLocaleTimeString('es-VE', { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Intervenciones:</span>
                        <span className="ml-1 font-medium text-foreground">{dentist?.interventions}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="text-right">
                    <div className="text-sm font-medium text-foreground">
                      {dentist?.totalCost?.bs?.toLocaleString()} Bs
                    </div>
                    <div className="text-xs text-muted-foreground">
                      ${dentist?.totalCost?.usd?.toFixed(2)}
                    </div>
                  </div>
                  
                  {dentist?.role !== 'primary' && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveDentist(dentist?.id)}
                    >
                      <Icon name="X" size={14} className="text-error" />
                    </Button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Add Dentist Panel */}
        {showAddDentist && (
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
            <h3 className="text-md font-semibold text-foreground mb-3 flex items-center">
              <Icon name="UserPlus" size={16} className="mr-2 text-primary" />
              Agregar Dentista a la Consulta
            </h3>
            
            <div className="space-y-3">
              {availableDentists?.filter(dentist => !participatingDentists?.find(p => p?.id === dentist?.id))?.map((dentist) => (
                  <div key={dentist?.id} className="flex items-center justify-between bg-card rounded-lg p-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-full overflow-hidden bg-muted">
                        <Image
                          src={dentist?.avatar}
                          alt={`Foto de ${dentist?.name}`}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div>
                        <div className="font-medium text-foreground">{dentist?.name}</div>
                        <div className="text-sm text-muted-foreground">{dentist?.specialty}</div>
                      </div>
                      <div className="flex items-center space-x-1">
                        <div className={`w-2 h-2 rounded-full ${dentist?.status === 'available' ? 'bg-success' : 'bg-warning'}`}></div>
                        <span className={`text-xs font-medium ${getStatusColor(dentist?.status)}`}>
                          {dentist?.status === 'available' ? 'Disponible' : 'Ocupado'}
                        </span>
                      </div>
                    </div>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleAddDentist(dentist)}
                      disabled={dentist?.status !== 'available'}
                    >
                      <Icon name="Plus" size={14} className="mr-1" />
                      Agregar
                    </Button>
                  </div>
                ))}
            </div>

            <div className="flex justify-end mt-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowAddDentist(false)}
              >
                Cancelar
              </Button>
            </div>
          </div>
        )}

        {/* Distribution Preview */}
        <div className="bg-muted/30 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center">
            <Icon name="PieChart" size={16} className="mr-2 text-primary" />
            Distribución de Ingresos
          </h3>
          
          <div className="space-y-2">
            {participatingDentists?.map((dentist) => {
              const percentage = totalCost?.bs > 0 ? (dentist?.totalCost?.bs / totalCost?.bs * 100) : 0;
              return (
                <div key={dentist?.id} className="flex items-center justify-between text-sm">
                  <span className="text-foreground">{dentist?.name}</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-20 bg-muted rounded-full h-2">
                      <div
                        className="bg-primary h-2 rounded-full"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-muted-foreground w-12 text-right">
                      {percentage?.toFixed(1)}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParticipatingDentistsPanel;