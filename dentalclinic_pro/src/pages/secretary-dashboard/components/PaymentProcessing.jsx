import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const PaymentProcessing = () => {
  const [selectedPayment, setSelectedPayment] = useState(null);
  const [paymentForm, setPaymentForm] = useState({
    amount: '',
    method: '',
    reference: '',
    notes: ''
  });

  const pendingPayments = [
    {
      id: 1,
      patient: "María González",
      treatment: "Limpieza dental",
      amount: 75.00,
      date: "2024-08-12",
      status: "pending",
      insurance: "Sanitas",
      copay: 15.00
    },
    {
      id: 2,
      patient: "Carlos Martín",
      treatment: "Empaste",
      amount: 120.00,
      date: "2024-08-12",
      status: "pending",
      insurance: "Particular",
      copay: 120.00
    },
    {
      id: 3,
      patient: "Ana Fernández",
      treatment: "Revisión",
      amount: 50.00,
      date: "2024-08-11",
      status: "overdue",
      insurance: "Adeslas",
      copay: 10.00
    },
    {
      id: 4,
      patient: "José Ruiz",
      treatment: "Extracción",
      amount: 180.00,
      date: "2024-08-10",
      status: "partial",
      insurance: "Particular",
      copay: 180.00,
      paid: 90.00
    }
  ];

  const recentPayments = [
    {
      id: 1,
      patient: "Laura Sánchez",
      amount: 95.00,
      method: "Tarjeta",
      timestamp: "2024-08-12 10:30",
      reference: "TXN-001234"
    },
    {
      id: 2,
      patient: "Miguel Torres",
      amount: 200.00,
      method: "Efectivo",
      timestamp: "2024-08-12 09:15",
      reference: "REC-001235"
    }
  ];

  const paymentMethods = [
    { value: '', label: 'Seleccionar método' },
    { value: 'cash', label: 'Efectivo' },
    { value: 'card', label: 'Tarjeta de Crédito/Débito' },
    { value: 'transfer', label: 'Transferencia Bancaria' },
    { value: 'insurance', label: 'Seguro Médico' }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'text-yellow-400 bg-yellow-500/20';
      case 'overdue':
        return 'text-red-400 bg-red-500/20';
      case 'partial':
        return 'text-orange-400 bg-orange-500/20';
      default:
        return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'pending':
        return 'Pendiente';
      case 'overdue':
        return 'Vencido';
      case 'partial':
        return 'Parcial';
      default:
        return 'Desconocido';
    }
  };

  const handlePaymentSelect = (payment) => {
    setSelectedPayment(payment);
    setPaymentForm({
      amount: payment?.status === 'partial' ? (payment?.copay - payment?.paid)?.toFixed(2) : payment?.copay?.toFixed(2),
      method: '',
      reference: '',
      notes: ''
    });
  };

  const handleFormChange = (field, value) => {
    setPaymentForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleProcessPayment = (e) => {
    e?.preventDefault();
    console.log('Procesando pago:', { selectedPayment, paymentForm });
    // Reset form
    setSelectedPayment(null);
    setPaymentForm({
      amount: '',
      method: '',
      reference: '',
      notes: ''
    });
  };

  const generateReceipt = (payment) => {
    console.log('Generando recibo para:', payment);
  };

  return (
    <div className="bg-surface rounded-lg border border-border shadow-custom-md h-full">
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Icon name="CreditCard" size={20} color="var(--color-primary)" />
            <h2 className="text-lg font-semibold text-foreground">
              Gestión de Pagos
            </h2>
          </div>
          <div className="flex items-center space-x-2">
            <Button variant="outline" className="text-sm">
              <Icon name="FileText" size={16} className="mr-2" />
              Reportes
            </Button>
            <Button variant="ghost" className="p-2">
              <Icon name="RefreshCw" size={16} />
            </Button>
          </div>
        </div>
      </div>
      <div className="p-4 h-full overflow-y-auto">
        {/* Pending Payments Section */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-foreground mb-3 flex items-center">
            <Icon name="Clock" size={16} className="mr-2" />
            Pagos Pendientes ({pendingPayments?.length})
          </h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {pendingPayments?.map((payment) => (
              <div
                key={payment?.id}
                className={`p-3 rounded-lg border cursor-pointer transition-all duration-200 hover:shadow-custom-sm ${
                  selectedPayment?.id === payment?.id
                    ? 'border-primary bg-primary/5' :'border-border bg-card hover:bg-muted/50'
                }`}
                onClick={() => handlePaymentSelect(payment)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-1">
                      <h4 className="font-medium text-foreground">{payment?.patient}</h4>
                      <span
                        className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                          payment?.status
                        )}`}
                      >
                        {getStatusText(payment?.status)}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground mb-1">
                      {payment?.treatment} • {payment?.insurance}
                    </p>
                    <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                      <span>Fecha: {new Date(payment.date)?.toLocaleDateString('es-ES')}</span>
                      <span>Total: €{payment?.amount?.toFixed(2)}</span>
                      <span>Copago: €{payment?.copay?.toFixed(2)}</span>
                      {payment?.paid && (
                        <span>Pagado: €{payment?.paid?.toFixed(2)}</span>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-semibold text-foreground">
                      €{payment?.status === 'partial' ? (payment?.copay - payment?.paid)?.toFixed(2) : payment?.copay?.toFixed(2)}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {payment?.status === 'partial' ? 'Restante' : 'A pagar'}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Payment Form */}
        {selectedPayment && (
          <div className="mb-6 p-4 bg-muted/30 rounded-lg border border-border">
            <h3 className="text-sm font-medium text-foreground mb-3 flex items-center">
              <Icon name="CreditCard" size={16} className="mr-2" />
              Procesar Pago - {selectedPayment?.patient}
            </h3>
            <form onSubmit={handleProcessPayment} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Importe"
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                  value={paymentForm?.amount}
                  onChange={(e) => handleFormChange('amount', e?.target?.value)}
                  required
                />
                <Select
                  label="Método de Pago"
                  options={paymentMethods}
                  value={paymentForm?.method}
                  onChange={(value) => handleFormChange('method', value)}
                  required
                />
              </div>
              <Input
                label="Referencia/Número de Transacción"
                type="text"
                placeholder="Opcional"
                value={paymentForm?.reference}
                onChange={(e) => handleFormChange('reference', e?.target?.value)}
              />
              <Input
                label="Notas"
                type="text"
                placeholder="Notas adicionales (opcional)"
                value={paymentForm?.notes}
                onChange={(e) => handleFormChange('notes', e?.target?.value)}
              />
              <div className="flex items-center justify-end space-x-3">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setSelectedPayment(null)}
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  iconName="Check"
                  iconPosition="left"
                >
                  Procesar Pago
                </Button>
              </div>
            </form>
          </div>
        )}

        {/* Recent Payments */}
        <div>
          <h3 className="text-sm font-medium text-foreground mb-3 flex items-center">
            <Icon name="CheckCircle" size={16} className="mr-2" />
            Pagos Recientes
          </h3>
          <div className="space-y-2">
            {recentPayments?.map((payment) => (
              <div
                key={payment?.id}
                className="p-3 rounded-lg border border-border bg-card"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-foreground">{payment?.patient}</h4>
                    <div className="flex items-center space-x-4 text-xs text-muted-foreground mt-1">
                      <span>{payment?.method}</span>
                      <span>{payment?.timestamp}</span>
                      <span>Ref: {payment?.reference}</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="text-right">
                      <p className="text-lg font-semibold text-success">
                        €{payment?.amount?.toFixed(2)}
                      </p>
                      <p className="text-xs text-muted-foreground">Completado</p>
                    </div>
                    <Button
                      variant="ghost"
                      onClick={() => generateReceipt(payment)}
                      className="p-2"
                    >
                      <Icon name="Printer" size={16} />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-card rounded-lg border border-border">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                <Icon name="Clock" size={20} color="var(--color-warning)" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Pendientes</p>
                <p className="text-xl font-semibold text-foreground">
                  €{pendingPayments?.reduce((sum, p) => sum + (p?.status === 'partial' ? p?.copay - p?.paid : p?.copay), 0)?.toFixed(2)}
                </p>
              </div>
            </div>
          </div>
          <div className="p-4 bg-card rounded-lg border border-border">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                <Icon name="CheckCircle" size={20} color="var(--color-success)" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Hoy</p>
                <p className="text-xl font-semibold text-foreground">
                  €{recentPayments?.reduce((sum, p) => sum + p?.amount, 0)?.toFixed(2)}
                </p>
              </div>
            </div>
          </div>
          <div className="p-4 bg-card rounded-lg border border-border">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                <Icon name="TrendingUp" size={20} color="var(--color-primary)" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Este Mes</p>
                <p className="text-xl font-semibold text-foreground">€2,450.00</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentProcessing;