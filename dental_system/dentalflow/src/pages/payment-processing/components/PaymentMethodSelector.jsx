import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Input from '../../../components/ui/Input';
import { Checkbox } from '../../../components/ui/Checkbox';

const PaymentMethodSelector = ({ 
  totalBs = 0, 
  totalUsd = 0, 
  exchangeRate = 36.45,
  onPaymentChange = () => {} 
}) => {
  const [paymentMethods, setPaymentMethods] = useState({
    cashBs: false,
    cashUsd: false,
    cardBs: false,
    cardUsd: false,
    transfer: false,
    zelle: false
  });

  const [amounts, setAmounts] = useState({
    cashBs: 0,
    cashUsd: 0,
    cardBs: 0,
    cardUsd: 0,
    transfer: 0,
    zelle: 0
  });

  const paymentOptions = [
    {
      id: 'cashBs',
      name: 'Efectivo Bolívares',
      icon: 'Banknote',
      currency: 'Bs',
      color: 'text-success'
    },
    {
      id: 'cashUsd',
      name: 'Efectivo USD',
      icon: 'DollarSign',
      currency: 'USD',
      color: 'text-success'
    },
    {
      id: 'cardBs',
      name: 'Tarjeta de Débito/Crédito',
      icon: 'CreditCard',
      currency: 'Bs',
      color: 'text-primary'
    },
    {
      id: 'cardUsd',
      name: 'Tarjeta Internacional',
      icon: 'CreditCard',
      currency: 'USD',
      color: 'text-primary'
    },
    {
      id: 'transfer',
      name: 'Transferencia Bancaria',
      icon: 'ArrowRightLeft',
      currency: 'Bs',
      color: 'text-accent'
    },
    {
      id: 'zelle',
      name: 'Zelle',
      icon: 'Smartphone',
      currency: 'USD',
      color: 'text-warning'
    }
  ];

  const handleMethodToggle = (methodId) => {
    const newMethods = {
      ...paymentMethods,
      [methodId]: !paymentMethods?.[methodId]
    };
    setPaymentMethods(newMethods);
    
    if (!newMethods?.[methodId]) {
      const newAmounts = { ...amounts, [methodId]: 0 };
      setAmounts(newAmounts);
      onPaymentChange(newMethods, newAmounts);
    } else {
      onPaymentChange(newMethods, amounts);
    }
  };

  const handleAmountChange = (methodId, value) => {
    const numValue = parseFloat(value) || 0;
    const newAmounts = { ...amounts, [methodId]: numValue };
    setAmounts(newAmounts);
    onPaymentChange(paymentMethods, newAmounts);
  };

  const calculateTotals = () => {
    const paidBs = amounts?.cashBs + amounts?.cardBs + amounts?.transfer + (amounts?.cashUsd * exchangeRate) + (amounts?.zelle * exchangeRate);
    const paidUsd = amounts?.cashUsd + amounts?.zelle + (amounts?.cashBs / exchangeRate) + (amounts?.cardBs / exchangeRate) + (amounts?.transfer / exchangeRate);
    
    return {
      paidBs,
      paidUsd,
      remainingBs: Math.max(0, totalBs - paidBs),
      remainingUsd: Math.max(0, totalUsd - paidUsd)
    };
  };

  const totals = calculateTotals();

  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
      <div className="flex items-center space-x-2 mb-6">
        <Icon name="CreditCard" size={24} className="text-primary" />
        <h2 className="text-xl font-semibold text-foreground">Métodos de Pago</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {paymentOptions?.map((option) => (
          <div key={option?.id} className="border border-border rounded-md p-4">
            <div className="flex items-center space-x-3 mb-3">
              <Checkbox
                checked={paymentMethods?.[option?.id]}
                onChange={() => handleMethodToggle(option?.id)}
              />
              <Icon name={option?.icon} size={20} className={option?.color} />
              <div className="flex-1">
                <span className="text-sm font-medium text-foreground">{option?.name}</span>
                <div className="text-xs text-muted-foreground">{option?.currency}</div>
              </div>
            </div>

            {paymentMethods?.[option?.id] && (
              <div className="mt-3">
                <Input
                  type="number"
                  placeholder={`Monto en ${option?.currency}`}
                  value={amounts?.[option?.id] || ''}
                  onChange={(e) => handleAmountChange(option?.id, e?.target?.value)}
                  className="w-full"
                  min="0"
                  step="0.01"
                />
                {option?.currency === 'USD' && amounts?.[option?.id] > 0 && (
                  <div className="text-xs text-muted-foreground mt-1">
                    Equivale a: {(amounts?.[option?.id] * exchangeRate)?.toLocaleString('es-VE')} Bs
                  </div>
                )}
                {option?.currency === 'Bs' && amounts?.[option?.id] > 0 && (
                  <div className="text-xs text-muted-foreground mt-1">
                    Equivale a: ${(amounts?.[option?.id] / exchangeRate)?.toFixed(2)} USD
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
      {/* Payment Summary */}
      <div className="bg-muted rounded-md p-4 space-y-3">
        <h3 className="text-sm font-semibold text-foreground">Resumen de Pago</h3>
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-muted-foreground">Total a Pagar:</div>
            <div className="font-medium text-foreground">
              {totalBs?.toLocaleString('es-VE')} Bs
            </div>
            <div className="font-medium text-foreground">
              ${totalUsd?.toFixed(2)} USD
            </div>
          </div>
          
          <div>
            <div className="text-muted-foreground">Pagado:</div>
            <div className="font-medium text-success">
              {totals?.paidBs?.toLocaleString('es-VE')} Bs
            </div>
            <div className="font-medium text-success">
              ${totals?.paidUsd?.toFixed(2)} USD
            </div>
          </div>
        </div>

        {(totals?.remainingBs > 0 || totals?.remainingUsd > 0) && (
          <div className="border-t border-border pt-3">
            <div className="text-muted-foreground text-sm">Pendiente:</div>
            <div className="font-medium text-warning">
              {totals?.remainingBs?.toLocaleString('es-VE')} Bs
            </div>
            <div className="font-medium text-warning">
              ${totals?.remainingUsd?.toFixed(2)} USD
            </div>
          </div>
        )}

        {totals?.remainingBs <= 0 && totals?.remainingUsd <= 0 && (
          <div className="flex items-center space-x-2 text-success">
            <Icon name="CheckCircle" size={16} />
            <span className="text-sm font-medium">Pago Completo</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default PaymentMethodSelector;