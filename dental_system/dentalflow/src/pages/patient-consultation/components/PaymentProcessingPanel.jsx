import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';

const PaymentProcessingPanel = ({ totalCost, participatingDentists, onPaymentProcess }) => {
  const navigate = useNavigate();
  const [exchangeRate] = useState(36.45);
  const [paymentData, setPaymentData] = useState({
    totalBs: totalCost?.bs || 7100,
    totalUsd: totalCost?.usd || 194.79,
    paidBs: 0,
    paidUsd: 0,
    paymentMethods: [],
    patientPaid: false,
    distributionApproved: false
  });

  const [paymentMethods, setPaymentMethods] = useState([]);
  const [showAddPayment, setShowAddPayment] = useState(false);
  const [newPayment, setNewPayment] = useState({
    method: 'cash',
    currency: 'bs',
    amount: '',
    reference: '',
    notes: ''
  });

  const availablePaymentMethods = [
    { value: 'cash', label: 'Efectivo', icon: 'Banknote' },
    { value: 'card', label: 'Tarjeta de Débito/Crédito', icon: 'CreditCard' },
    { value: 'transfer', label: 'Transferencia Bancaria', icon: 'ArrowRightLeft' },
    { value: 'mobile', label: 'Pago Móvil', icon: 'Smartphone' },
    { value: 'zelle', label: 'Zelle', icon: 'DollarSign' },
    { value: 'paypal', label: 'PayPal', icon: 'Globe' }
  ];

  const mockDentistDistribution = [
    {
      id: 'dr-gonzalez',
      name: 'Dr. María González',
      percentage: 60,
      amountBs: 4260,
      amountUsd: 116.87,
      role: 'primary'
    },
    {
      id: 'dr-mendoza',
      name: 'Dr. Carlos Mendoza',
      percentage: 40,
      amountBs: 2840,
      amountUsd: 77.92,
      role: 'consultant'
    }
  ];

  const handleAddPayment = () => {
    if (!newPayment?.amount || parseFloat(newPayment?.amount) <= 0) {
      return;
    }

    const amount = parseFloat(newPayment?.amount);
    const payment = {
      id: Date.now(),
      ...newPayment,
      amount,
      timestamp: new Date(),
      status: 'completed'
    };

    setPaymentMethods(prev => [...prev, payment]);

    // Update totals
    if (newPayment?.currency === 'bs') {
      setPaymentData(prev => ({
        ...prev,
        paidBs: prev?.paidBs + amount
      }));
    } else {
      setPaymentData(prev => ({
        ...prev,
        paidUsd: prev?.paidUsd + amount
      }));
    }

    // Reset form
    setNewPayment({
      method: 'cash',
      currency: 'bs',
      amount: '',
      reference: '',
      notes: ''
    });
    setShowAddPayment(false);
  };

  const handleProcessPayment = () => {
    const isFullyPaid = (paymentData?.paidBs >= paymentData?.totalBs * 0.95) || 
                       (paymentData?.paidUsd >= paymentData?.totalUsd * 0.95);
    
    if (isFullyPaid) {
      setPaymentData(prev => ({ ...prev, patientPaid: true }));
      if (onPaymentProcess) {
        onPaymentProcess({
          ...paymentData,
          paymentMethods,
          distribution: mockDentistDistribution
        });
      }
    }
  };

  const handleNavigateToPayments = () => {
    navigate('/payment-processing');
  };

  const remainingBs = Math.max(0, paymentData?.totalBs - paymentData?.paidBs);
  const remainingUsd = Math.max(0, paymentData?.totalUsd - paymentData?.paidUsd);
  const isFullyPaid = remainingBs <= paymentData?.totalBs * 0.05 && remainingUsd <= paymentData?.totalUsd * 0.05;

  const getMethodIcon = (method) => {
    const methodConfig = availablePaymentMethods?.find(m => m?.value === method);
    return methodConfig?.icon || 'CreditCard';
  };

  const getMethodLabel = (method) => {
    const methodConfig = availablePaymentMethods?.find(m => m?.value === method);
    return methodConfig?.label || method;
  };

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="CreditCard" size={20} className="text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Procesamiento de Pagos</h2>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-sm text-muted-foreground">
            Tasa: {exchangeRate?.toFixed(2)} Bs/USD
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleNavigateToPayments}
          >
            <Icon name="ExternalLink" size={16} className="mr-2" />
            Ver Módulo Completo
          </Button>
        </div>
      </div>
      <div className="p-4 space-y-6">
        {/* Payment Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-primary/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-primary">{paymentData?.totalBs?.toLocaleString()}</div>
            <div className="text-xs text-muted-foreground">Total Bs</div>
          </div>
          <div className="bg-primary/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-primary">${paymentData?.totalUsd?.toFixed(2)}</div>
            <div className="text-xs text-muted-foreground">Total USD</div>
          </div>
          <div className="bg-success/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-success">{paymentData?.paidBs?.toLocaleString()}</div>
            <div className="text-xs text-muted-foreground">Pagado Bs</div>
          </div>
          <div className="bg-success/5 rounded-lg p-3 text-center">
            <div className="text-lg font-bold text-success">${paymentData?.paidUsd?.toFixed(2)}</div>
            <div className="text-xs text-muted-foreground">Pagado USD</div>
          </div>
        </div>

        {/* Payment Status */}
        <div className={`rounded-lg p-4 ${isFullyPaid ? 'bg-success/10 border border-success/20' : 'bg-warning/10 border border-warning/20'}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Icon 
                name={isFullyPaid ? "CheckCircle" : "Clock"} 
                size={20} 
                className={isFullyPaid ? "text-success" : "text-warning"} 
              />
              <div>
                <div className={`font-semibold ${isFullyPaid ? "text-success" : "text-warning"}`}>
                  {isFullyPaid ? "Pago Completado" : "Pago Pendiente"}
                </div>
                {!isFullyPaid && (
                  <div className="text-sm text-muted-foreground">
                    Restante: {remainingBs?.toLocaleString()} Bs / ${remainingUsd?.toFixed(2)}
                  </div>
                )}
              </div>
            </div>
            
            {!isFullyPaid && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowAddPayment(!showAddPayment)}
              >
                <Icon name="Plus" size={16} className="mr-2" />
                Agregar Pago
              </Button>
            )}
          </div>
        </div>

        {/* Add Payment Form */}
        {showAddPayment && (
          <div className="bg-muted/30 rounded-lg p-4">
            <h3 className="text-md font-semibold text-foreground mb-4 flex items-center">
              <Icon name="Plus" size={16} className="mr-2 text-primary" />
              Registrar Nuevo Pago
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Método de Pago
                </label>
                <select
                  value={newPayment?.method}
                  onChange={(e) => setNewPayment(prev => ({ ...prev, method: e?.target?.value }))}
                  className="w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:ring-2 focus:ring-ring focus:border-transparent"
                >
                  {availablePaymentMethods?.map(method => (
                    <option key={method?.value} value={method?.value}>
                      {method?.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Moneda
                </label>
                <select
                  value={newPayment?.currency}
                  onChange={(e) => setNewPayment(prev => ({ ...prev, currency: e?.target?.value }))}
                  className="w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:ring-2 focus:ring-ring focus:border-transparent"
                >
                  <option value="bs">Bolívares (Bs)</option>
                  <option value="usd">Dólares (USD)</option>
                </select>
              </div>

              <Input
                label="Monto"
                type="number"
                value={newPayment?.amount}
                onChange={(e) => setNewPayment(prev => ({ ...prev, amount: e?.target?.value }))}
                placeholder="0.00"
                required
              />

              <Input
                label="Referencia"
                type="text"
                value={newPayment?.reference}
                onChange={(e) => setNewPayment(prev => ({ ...prev, reference: e?.target?.value }))}
                placeholder="Número de referencia"
              />
            </div>

            <div className="mt-4">
              <Input
                label="Notas"
                type="text"
                value={newPayment?.notes}
                onChange={(e) => setNewPayment(prev => ({ ...prev, notes: e?.target?.value }))}
                placeholder="Notas adicionales del pago"
              />
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <Button
                variant="ghost"
                onClick={() => setShowAddPayment(false)}
              >
                Cancelar
              </Button>
              <Button onClick={handleAddPayment}>
                <Icon name="Plus" size={16} className="mr-2" />
                Registrar Pago
              </Button>
            </div>
          </div>
        )}

        {/* Payment Methods List */}
        {paymentMethods?.length > 0 && (
          <div>
            <h3 className="text-md font-semibold text-foreground mb-3 flex items-center">
              <Icon name="List" size={16} className="mr-2 text-primary" />
              Pagos Registrados
            </h3>
            
            <div className="space-y-2">
              {paymentMethods?.map((payment) => (
                <div key={payment?.id} className="bg-card border border-border rounded-md p-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Icon name={getMethodIcon(payment?.method)} size={16} className="text-primary" />
                      <div>
                        <div className="font-medium text-foreground">
                          {getMethodLabel(payment?.method)}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {payment?.timestamp?.toLocaleTimeString('es-VE')}
                          {payment?.reference && ` • Ref: ${payment?.reference}`}
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="font-semibold text-foreground">
                        {payment?.currency === 'bs' 
                          ? `${payment?.amount?.toLocaleString()} Bs`
                          : `$${payment?.amount?.toFixed(2)}`
                        }
                      </div>
                      <div className="text-xs text-success">Completado</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Dentist Distribution */}
        <div className="bg-muted/30 rounded-lg p-4">
          <h3 className="text-md font-semibold text-foreground mb-3 flex items-center">
            <Icon name="PieChart" size={16} className="mr-2 text-primary" />
            Distribución entre Dentistas
          </h3>
          
          <div className="space-y-3">
            {mockDentistDistribution?.map((dentist) => (
              <div key={dentist?.id} className="flex items-center justify-between bg-card rounded p-3">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <Icon name="User" size={16} className="text-primary" />
                  </div>
                  <div>
                    <div className="font-medium text-foreground">{dentist?.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {dentist?.role === 'primary' ? 'Dentista Principal' : 'Consultor'} • {dentist?.percentage}%
                    </div>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="font-semibold text-foreground">
                    {dentist?.amountBs?.toLocaleString()} Bs
                  </div>
                  <div className="text-sm text-muted-foreground">
                    ${dentist?.amountUsd?.toFixed(2)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-3">
          <Button variant="outline">
            <Icon name="FileText" size={16} className="mr-2" />
            Generar Recibo
          </Button>
          
          {isFullyPaid ? (
            <Button variant="success">
              <Icon name="CheckCircle" size={16} className="mr-2" />
              Pago Completado
            </Button>
          ) : (
            <Button onClick={handleProcessPayment} disabled={paymentMethods?.length === 0}>
              <Icon name="CreditCard" size={16} className="mr-2" />
              Procesar Pago
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PaymentProcessingPanel;