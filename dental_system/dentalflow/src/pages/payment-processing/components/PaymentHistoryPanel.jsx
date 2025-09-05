import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Input from '../../../components/ui/Input';
import Button from '../../../components/ui/Button';

const PaymentHistoryPanel = ({ patientId }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPeriod, setFilterPeriod] = useState('all');
  const [showDetails, setShowDetails] = useState({});

  // Mock payment history data
  const paymentHistory = [
    {
      id: 'PAY-2024-0156',
      date: '2024-01-15',
      time: '14:30',
      totalBs: 2850000,
      totalUsd: 78.15,
      services: [
        { name: 'Limpieza Dental', dentist: 'María González', priceBs: 1200000, priceUsd: 32.88 },
        { name: 'Empaste Composite', dentist: 'Carlos Mendoza', priceBs: 1650000, priceUsd: 45.27 }
      ],
      paymentMethods: [
        { type: 'Efectivo USD', amount: 50, currency: 'USD' },
        { type: 'Transferencia', amount: 1027500, currency: 'Bs' }
      ],
      status: 'completed',
      receiptNumber: 'REC-2024-0156'
    },
    {
      id: 'PAY-2024-0089',
      date: '2023-12-08',
      time: '10:15',
      totalBs: 1800000,
      totalUsd: 49.32,
      services: [
        { name: 'Consulta General', dentist: 'Ana Rodríguez', priceBs: 800000, priceUsd: 21.92 },
        { name: 'Radiografía', dentist: 'Ana Rodríguez', priceBs: 1000000, priceUsd: 27.40 }
      ],
      paymentMethods: [
        { type: 'Tarjeta de Débito', amount: 1800000, currency: 'Bs' }
      ],
      status: 'completed',
      receiptNumber: 'REC-2024-0089'
    },
    {
      id: 'PAY-2024-0034',
      date: '2023-11-22',
      time: '16:45',
      totalBs: 3200000,
      totalUsd: 87.67,
      services: [
        { name: 'Extracción Dental', dentist: 'Luis Pérez', priceBs: 2200000, priceUsd: 60.27 },
        { name: 'Medicamentos', dentist: 'Luis Pérez', priceBs: 1000000, priceUsd: 27.40 }
      ],
      paymentMethods: [
        { type: 'Zelle', amount: 87.67, currency: 'USD' }
      ],
      status: 'completed',
      receiptNumber: 'REC-2024-0034'
    }
  ];

  const filteredHistory = paymentHistory?.filter(payment => {
    const matchesSearch = payment?.id?.toLowerCase()?.includes(searchTerm?.toLowerCase()) ||
                         payment?.services?.some(service => 
                           service?.name?.toLowerCase()?.includes(searchTerm?.toLowerCase()) ||
                           service?.dentist?.toLowerCase()?.includes(searchTerm?.toLowerCase())
                         );
    
    if (filterPeriod === 'all') return matchesSearch;
    
    const paymentDate = new Date(payment.date);
    const now = new Date();
    
    switch (filterPeriod) {
      case '30days':
        return matchesSearch && (now - paymentDate) <= (30 * 24 * 60 * 60 * 1000);
      case '90days':
        return matchesSearch && (now - paymentDate) <= (90 * 24 * 60 * 60 * 1000);
      case '1year':
        return matchesSearch && (now - paymentDate) <= (365 * 24 * 60 * 60 * 1000);
      default:
        return matchesSearch;
    }
  });

  const toggleDetails = (paymentId) => {
    setShowDetails(prev => ({
      ...prev,
      [paymentId]: !prev?.[paymentId]
    }));
  };

  const getStatusConfig = (status) => {
    switch (status) {
      case 'completed':
        return { color: 'text-success', bg: 'bg-success/10', icon: 'CheckCircle', label: 'Completado' };
      case 'pending':
        return { color: 'text-warning', bg: 'bg-warning/10', icon: 'Clock', label: 'Pendiente' };
      case 'cancelled':
        return { color: 'text-error', bg: 'bg-error/10', icon: 'XCircle', label: 'Cancelado' };
      default:
        return { color: 'text-muted-foreground', bg: 'bg-muted', icon: 'Circle', label: 'Desconocido' };
    }
  };

  const calculateTotal = () => {
    return filteredHistory?.reduce((sum, payment) => ({
      totalBs: sum?.totalBs + payment?.totalBs,
      totalUsd: sum?.totalUsd + payment?.totalUsd
    }), { totalBs: 0, totalUsd: 0 });
  };

  const totals = calculateTotal();

  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
      <div className="flex items-center space-x-2 mb-6">
        <Icon name="History" size={24} className="text-primary" />
        <h2 className="text-xl font-semibold text-foreground">Historial de Pagos</h2>
      </div>
      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="flex-1">
          <Input
            type="search"
            placeholder="Buscar por ID, servicio o dentista..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e?.target?.value)}
            className="w-full"
          />
        </div>
        
        <div className="sm:w-48">
          <select
            value={filterPeriod}
            onChange={(e) => setFilterPeriod(e?.target?.value)}
            className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
          >
            <option value="all">Todos los períodos</option>
            <option value="30days">Últimos 30 días</option>
            <option value="90days">Últimos 90 días</option>
            <option value="1year">Último año</option>
          </select>
        </div>
      </div>
      {/* Summary */}
      {filteredHistory?.length > 0 && (
        <div className="bg-muted rounded-md p-4 mb-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
            <div>
              <div className="text-muted-foreground">Total Pagos:</div>
              <div className="font-semibold text-foreground">{filteredHistory?.length}</div>
            </div>
            <div>
              <div className="text-muted-foreground">Total en Bolívares:</div>
              <div className="font-semibold text-foreground">{totals?.totalBs?.toLocaleString('es-VE')} Bs</div>
            </div>
            <div>
              <div className="text-muted-foreground">Total en USD:</div>
              <div className="font-semibold text-foreground">${totals?.totalUsd?.toFixed(2)} USD</div>
            </div>
          </div>
        </div>
      )}
      {/* Payment History List */}
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {filteredHistory?.length === 0 ? (
          <div className="text-center py-8">
            <Icon name="Search" size={48} className="text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">No se encontraron pagos</p>
          </div>
        ) : (
          filteredHistory?.map((payment) => {
            const statusConfig = getStatusConfig(payment?.status);
            
            return (
              <div key={payment?.id} className="border border-border rounded-md p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className={`px-2 py-1 rounded-full ${statusConfig?.bg}`}>
                      <Icon name={statusConfig?.icon} size={14} className={statusConfig?.color} />
                    </div>
                    <div>
                      <div className="font-medium text-foreground">{payment?.id}</div>
                      <div className="text-sm text-muted-foreground">
                        {new Date(payment.date)?.toLocaleDateString('es-VE')} • {payment?.time}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="text-right">
                      <div className="font-medium text-foreground">
                        {payment?.totalBs?.toLocaleString('es-VE')} Bs
                      </div>
                      <div className="text-sm text-muted-foreground">
                        ${payment?.totalUsd?.toFixed(2)} USD
                      </div>
                    </div>
                    
                    <button
                      onClick={() => toggleDetails(payment?.id)}
                      className="p-1 hover:bg-muted rounded transition-smooth"
                    >
                      <Icon 
                        name={showDetails?.[payment?.id] ? "ChevronUp" : "ChevronDown"} 
                        size={16} 
                        className="text-muted-foreground" 
                      />
                    </button>
                  </div>
                </div>
                {/* Quick Summary */}
                <div className="text-sm text-muted-foreground mb-2">
                  {payment?.services?.length} servicio{payment?.services?.length !== 1 ? 's' : ''} • 
                  {payment?.paymentMethods?.length} método{payment?.paymentMethods?.length !== 1 ? 's' : ''} de pago
                </div>
                {/* Expanded Details */}
                {showDetails?.[payment?.id] && (
                  <div className="border-t border-border pt-3 mt-3 space-y-3">
                    {/* Services */}
                    <div>
                      <h4 className="text-sm font-medium text-foreground mb-2">Servicios:</h4>
                      <div className="space-y-1">
                        {payment?.services?.map((service, index) => (
                          <div key={index} className="flex items-center justify-between text-sm bg-muted rounded p-2">
                            <div className="flex items-center space-x-2">
                              <Icon name="Tooth" size={14} className="text-primary" />
                              <span className="text-foreground">{service?.name}</span>
                              <span className="text-muted-foreground">• Dr. {service?.dentist}</span>
                            </div>
                            <div className="text-right">
                              <div className="text-foreground">{service?.priceBs?.toLocaleString('es-VE')} Bs</div>
                              <div className="text-muted-foreground">${service?.priceUsd?.toFixed(2)} USD</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Payment Methods */}
                    <div>
                      <h4 className="text-sm font-medium text-foreground mb-2">Métodos de Pago:</h4>
                      <div className="space-y-1">
                        {payment?.paymentMethods?.map((method, index) => (
                          <div key={index} className="flex items-center justify-between text-sm">
                            <span className="text-muted-foreground">{method?.type}:</span>
                            <span className="font-medium text-foreground">
                              {method?.currency === 'USD' ? '$' : ''}{method?.amount?.toLocaleString('es-VE')} {method?.currency}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex space-x-2 pt-2">
                      <Button variant="outline" size="sm" iconName="Download">
                        Descargar Recibo
                      </Button>
                      <Button variant="outline" size="sm" iconName="Printer">
                        Imprimir
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default PaymentHistoryPanel;