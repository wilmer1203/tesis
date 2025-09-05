import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ConsultationHistoryPanel = ({ patientId }) => {
  const [selectedVisit, setSelectedVisit] = useState(null);
  const [showAllVisits, setShowAllVisits] = useState(false);

  const consultationHistory = [
    {
      id: 1,
      date: '2024-09-04',
      time: '10:30',
      dentists: ['Dr. María González', 'Dr. Carlos Mendoza'],
      procedures: [
        { name: 'Limpieza Dental', tooth: '11-18', cost: { bs: 1500, usd: 41.15 } },
        { name: 'Obturación', tooth: '16', cost: { bs: 2800, usd: 76.82 } }
      ],
      totalCost: { bs: 4300, usd: 117.97 },
      status: 'completed',
      notes: `Paciente presenta buena higiene oral. Se realizó limpieza completa y obturación en molar superior derecho.\nSe recomienda control en 6 meses.`,
      photos: [
        'https://images.pexels.com/photos/3845810/pexels-photo-3845810.jpeg?w=150&h=150&fit=crop',
        'https://images.pexels.com/photos/3845811/pexels-photo-3845811.jpeg?w=150&h=150&fit=crop'
      ]
    },
    {
      id: 2,
      date: '2024-08-15',
      time: '14:15',
      dentists: ['Dr. Ana Silva'],
      procedures: [
        { name: 'Consulta General', tooth: 'General', cost: { bs: 800, usd: 21.95 } },
        { name: 'Radiografía', tooth: 'General', cost: { bs: 1200, usd: 32.93 } }
      ],
      totalCost: { bs: 2000, usd: 54.88 },
      status: 'completed',
      notes: `Control de rutina. Paciente sin molestias. Se detectó inicio de caries en diente 24.\nSe programa tratamiento para próxima visita.`,
      photos: []
    },
    {
      id: 3,
      date: '2024-07-20',
      time: '09:45',
      dentists: ['Dr. María González'],
      procedures: [
        { name: 'Obturación', tooth: '14', cost: { bs: 2500, usd: 68.56 } }
      ],
      totalCost: { bs: 2500, usd: 68.56 },
      status: 'completed',
      notes: `Tratamiento de caries en premolar superior derecho. Procedimiento sin complicaciones.\nPaciente tolera bien el tratamiento.`,
      photos: [
        'https://images.pexels.com/photos/3845812/pexels-photo-3845812.jpeg?w=150&h=150&fit=crop'
      ]
    },
    {
      id: 4,
      date: '2024-06-10',
      time: '16:00',
      dentists: ['Dr. Luis Torres'],
      procedures: [
        { name: 'Extracción', tooth: '18', cost: { bs: 3500, usd: 96.04 } }
      ],
      totalCost: { bs: 3500, usd: 96.04 },
      status: 'completed',
      notes: `Extracción de muela del juicio superior derecha. Procedimiento quirúrgico sin complicaciones.\nSe prescribe antibiótico y analgésico.`,
      photos: []
    },
    {
      id: 5,
      date: '2024-05-15',
      time: '11:20',
      dentists: ['Dr. Carlos Mendoza'],
      procedures: [
        { name: 'Corona', tooth: '26', cost: { bs: 8000, usd: 219.45 } }
      ],
      totalCost: { bs: 8000, usd: 219.45 },
      status: 'completed',
      notes: `Colocación de corona en molar superior izquierdo. Excelente adaptación.\nPaciente satisfecho con el resultado estético.`,
      photos: [
        'https://images.pexels.com/photos/3845813/pexels-photo-3845813.jpeg?w=150&h=150&fit=crop',
        'https://images.pexels.com/photos/3845814/pexels-photo-3845814.jpeg?w=150&h=150&fit=crop'
      ]
    }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'text-success bg-success/10';
      case 'in-progress':
        return 'text-warning bg-warning/10';
      case 'cancelled':
        return 'text-error bg-error/10';
      default:
        return 'text-muted-foreground bg-muted';
    }
  };

  const visitsToShow = showAllVisits ? consultationHistory : consultationHistory?.slice(0, 3);
  const totalVisits = consultationHistory?.length;
  const totalSpent = consultationHistory?.reduce((sum, visit) => ({
    bs: sum?.bs + visit?.totalCost?.bs,
    usd: sum?.usd + visit?.totalCost?.usd
  }), { bs: 0, usd: 0 });

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="History" size={20} className="text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Historial de Consultas</h2>
        </div>
        <div className="flex items-center space-x-4 text-sm text-muted-foreground">
          <div className="flex items-center space-x-1">
            <Icon name="Calendar" size={14} />
            <span>{totalVisits} visitas</span>
          </div>
          <div className="flex items-center space-x-1">
            <Icon name="DollarSign" size={14} />
            <span>{totalSpent?.bs?.toLocaleString()} Bs</span>
          </div>
        </div>
      </div>
      <div className="p-4 space-y-4">
        {/* Summary Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-primary/5 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-primary">{totalVisits}</div>
            <div className="text-xs text-muted-foreground">Total Visitas</div>
          </div>
          <div className="bg-success/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-success">{totalSpent?.bs?.toLocaleString()}</div>
            <div className="text-xs text-muted-foreground">Total Bs</div>
          </div>
          <div className="bg-success/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-success">${totalSpent?.usd?.toFixed(2)}</div>
            <div className="text-xs text-muted-foreground">Total USD</div>
          </div>
        </div>

        {/* Visit History */}
        <div className="space-y-3">
          {visitsToShow?.map((visit) => (
            <div key={visit?.id} className="bg-muted/30 rounded-lg p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="text-sm font-medium text-foreground">
                    {new Date(visit.date)?.toLocaleDateString('es-VE', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </div>
                  <div className="text-sm text-muted-foreground">{visit?.time}</div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(visit?.status)}`}>
                    Completado
                  </span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedVisit(selectedVisit === visit?.id ? null : visit?.id)}
                >
                  <Icon 
                    name={selectedVisit === visit?.id ? "ChevronUp" : "ChevronDown"} 
                    size={16} 
                  />
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                <div>
                  <div className="text-xs text-muted-foreground mb-1">Dentistas</div>
                  <div className="text-sm text-foreground">
                    {visit?.dentists?.join(', ')}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground mb-1">Costo Total</div>
                  <div className="text-sm font-medium text-foreground">
                    {visit?.totalCost?.bs?.toLocaleString()} Bs / ${visit?.totalCost?.usd?.toFixed(2)}
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 mb-3">
                {visit?.procedures?.map((procedure, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full"
                  >
                    {procedure?.name} ({procedure?.tooth})
                  </span>
                ))}
              </div>

              {/* Expanded Details */}
              {selectedVisit === visit?.id && (
                <div className="border-t border-border pt-4 mt-4 space-y-4">
                  {/* Detailed Procedures */}
                  <div>
                    <h4 className="text-sm font-semibold text-foreground mb-2">Procedimientos Detallados</h4>
                    <div className="space-y-2">
                      {visit?.procedures?.map((procedure, index) => (
                        <div key={index} className="flex justify-between items-center bg-card rounded p-2">
                          <div>
                            <div className="text-sm font-medium text-foreground">{procedure?.name}</div>
                            <div className="text-xs text-muted-foreground">Diente: {procedure?.tooth}</div>
                          </div>
                          <div className="text-right">
                            <div className="text-sm font-medium text-foreground">
                              {procedure?.cost?.bs?.toLocaleString()} Bs
                            </div>
                            <div className="text-xs text-muted-foreground">
                              ${procedure?.cost?.usd?.toFixed(2)}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Clinical Notes */}
                  <div>
                    <h4 className="text-sm font-semibold text-foreground mb-2">Notas Clínicas</h4>
                    <div className="bg-card rounded p-3 text-sm text-foreground whitespace-pre-line">
                      {visit?.notes}
                    </div>
                  </div>

                  {/* Photos */}
                  {visit?.photos?.length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold text-foreground mb-2">Fotografías</h4>
                      <div className="flex space-x-2">
                        {visit?.photos?.map((photo, index) => (
                          <div key={index} className="w-16 h-16 rounded overflow-hidden bg-muted">
                            <img
                              src={photo}
                              alt={`Foto ${index + 1} de la visita`}
                              className="w-full h-full object-cover cursor-pointer hover:opacity-80 transition-smooth"
                              onClick={() => console.log('Open photo viewer')}
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex justify-end space-x-2">
                    <Button variant="outline" size="sm">
                      <Icon name="FileText" size={14} className="mr-1" />
                      Ver Recibo
                    </Button>
                    <Button variant="outline" size="sm">
                      <Icon name="Download" size={14} className="mr-1" />
                      Exportar
                    </Button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Show More/Less Button */}
        {consultationHistory?.length > 3 && (
          <div className="text-center pt-4">
            <Button
              variant="outline"
              onClick={() => setShowAllVisits(!showAllVisits)}
            >
              {showAllVisits ? (
                <>
                  <Icon name="ChevronUp" size={16} className="mr-2" />
                  Mostrar Menos
                </>
              ) : (
                <>
                  <Icon name="ChevronDown" size={16} className="mr-2" />
                  Mostrar Todas ({consultationHistory?.length - 3} más)
                </>
              )}
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConsultationHistoryPanel;