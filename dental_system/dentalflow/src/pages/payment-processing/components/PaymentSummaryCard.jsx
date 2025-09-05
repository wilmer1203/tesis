import React from 'react';
import Icon from '../../../components/AppIcon';

const PaymentSummaryCard = ({ 
  consultation, 
  exchangeRate = 36.45,
  onViewDetails = () => {} 
}) => {
  const calculateTotals = () => {
    const subtotalBs = consultation?.services?.reduce((sum, service) => sum + service?.priceBs, 0);
    const subtotalUsd = consultation?.services?.reduce((sum, service) => sum + service?.priceUsd, 0);
    const taxBs = subtotalBs * 0.16; // 16% IVA
    const taxUsd = subtotalUsd * 0.16;
    
    return {
      subtotalBs,
      subtotalUsd,
      taxBs,
      taxUsd,
      totalBs: subtotalBs + taxBs,
      totalUsd: subtotalUsd + taxUsd
    };
  };

  const totals = calculateTotals();

  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-foreground">Resumen de Consulta</h2>
          <p className="text-sm text-muted-foreground">
            Paciente: {consultation?.patient?.name} • {consultation?.patient?.id}
          </p>
        </div>
        <button
          onClick={onViewDetails}
          className="p-2 hover:bg-muted rounded-md transition-smooth"
          title="Ver detalles completos"
        >
          <Icon name="Eye" size={20} className="text-muted-foreground" />
        </button>
      </div>
      {/* Services List */}
      <div className="space-y-3 mb-6">
        <h3 className="text-sm font-medium text-foreground mb-3">Servicios Realizados</h3>
        {consultation?.services?.map((service, index) => (
          <div key={index} className="flex items-center justify-between py-2 border-b border-border last:border-b-0">
            <div className="flex-1">
              <div className="flex items-center space-x-2">
                <Icon name="Tooth" size={16} className="text-primary" />
                <span className="text-sm font-medium text-foreground">{service?.name}</span>
              </div>
              <div className="text-xs text-muted-foreground mt-1">
                Dr. {service?.dentist} • Pieza {service?.tooth}
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-medium text-foreground">
                {service?.priceBs?.toLocaleString('es-VE')} Bs
              </div>
              <div className="text-xs text-muted-foreground">
                ${service?.priceUsd?.toFixed(2)} USD
              </div>
            </div>
          </div>
        ))}
      </div>
      {/* Exchange Rate Display */}
      <div className="bg-muted rounded-md p-3 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Icon name="DollarSign" size={16} className="text-primary" />
            <span className="text-sm font-medium text-foreground">Tasa de Cambio</span>
          </div>
          <div className="text-right">
            <div className="text-sm font-mono font-semibold text-foreground">
              1 USD = {exchangeRate?.toFixed(2)} Bs
            </div>
            <div className="text-xs text-muted-foreground">
              Actualizado: {new Date()?.toLocaleTimeString('es-VE')}
            </div>
          </div>
        </div>
      </div>
      {/* Totals */}
      <div className="space-y-2 border-t border-border pt-4">
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Subtotal:</span>
          <div className="text-right">
            <div className="text-foreground">{totals?.subtotalBs?.toLocaleString('es-VE')} Bs</div>
            <div className="text-muted-foreground">${totals?.subtotalUsd?.toFixed(2)} USD</div>
          </div>
        </div>
        
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">IVA (16%):</span>
          <div className="text-right">
            <div className="text-foreground">{totals?.taxBs?.toLocaleString('es-VE')} Bs</div>
            <div className="text-muted-foreground">${totals?.taxUsd?.toFixed(2)} USD</div>
          </div>
        </div>
        
        <div className="flex justify-between text-lg font-semibold border-t border-border pt-2">
          <span className="text-foreground">Total a Pagar:</span>
          <div className="text-right">
            <div className="text-primary">{totals?.totalBs?.toLocaleString('es-VE')} Bs</div>
            <div className="text-primary">${totals?.totalUsd?.toFixed(2)} USD</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentSummaryCard;