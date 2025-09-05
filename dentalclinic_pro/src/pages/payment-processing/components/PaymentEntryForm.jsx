import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';

const PaymentEntryForm = ({ selectedPayment, onPaymentProcessed }) => {
  const [paymentData, setPaymentData] = useState({
    amount: selectedPayment?.amount || 0,
    paymentMethod: 'cash',
    cardType: '',
    cardNumber: '',
    installments: 1,
    notes: '',
    applyDiscount: false,
    discountAmount: 0,
    discountReason: '',
    generateReceipt: true,
    sendEmail: false,
    patientEmail: ''
  });

  const [isProcessing, setIsProcessing] = useState(false);
  const [showCardDetails, setShowCardDetails] = useState(false);
  const [showInstallments, setShowInstallments] = useState(false);

  const paymentMethodOptions = [
    { value: 'cash', label: 'Efectivo' },
    { value: 'card', label: 'Tarjeta de crédito/débito' },
    { value: 'transfer', label: 'Transferencia bancaria' },
    { value: 'insurance', label: 'Seguro médico' },
    { value: 'plan', label: 'Plan de pagos' }
  ];

  const cardTypeOptions = [
    { value: 'visa', label: 'Visa' },
    { value: 'mastercard', label: 'Mastercard' },
    { value: 'amex', label: 'American Express' },
    { value: 'other', label: 'Otra' }
  ];

  const installmentOptions = [
    { value: 1, label: '1 pago (sin intereses)' },
    { value: 3, label: '3 cuotas (+2% interés)' },
    { value: 6, label: '6 cuotas (+4% interés)' },
    { value: 12, label: '12 cuotas (+8% interés)' }
  ];

  const handleInputChange = (field, value) => {
    setPaymentData(prev => ({
      ...prev,
      [field]: value
    }));

    // Show/hide additional fields based on payment method
    if (field === 'paymentMethod') {
      setShowCardDetails(value === 'card');
      setShowInstallments(value === 'plan' || value === 'card');
    }
  };

  const calculateTotal = () => {
    let total = parseFloat(paymentData?.amount) || 0;
    
    if (paymentData?.applyDiscount) {
      total -= parseFloat(paymentData?.discountAmount) || 0;
    }

    if (paymentData?.installments > 1) {
      const interestRate = paymentData?.installments === 3 ? 0.02 : 
                          paymentData?.installments === 6 ? 0.04 : 
                          paymentData?.installments === 12 ? 0.08 : 0;
      total += total * interestRate;
    }

    return Math.max(0, total);
  };

  const calculateTax = () => {
    return calculateTotal() * 0.21; // IVA 21%
  };

  const handleProcessPayment = async () => {
    setIsProcessing(true);
    
    // Simulate payment processing
    setTimeout(() => {
      const processedPayment = {
        ...selectedPayment,
        ...paymentData,
        totalAmount: calculateTotal(),
        taxAmount: calculateTax(),
        processedAt: new Date()?.toISOString(),
        status: 'completed',
        transactionId: `TXN-${Date.now()}`
      };

      onPaymentProcessed(processedPayment);
      setIsProcessing(false);
      
      // Reset form
      setPaymentData({
        amount: 0,
        paymentMethod: 'cash',
        cardType: '',
        cardNumber: '',
        installments: 1,
        notes: '',
        applyDiscount: false,
        discountAmount: 0,
        discountReason: '',
        generateReceipt: true,
        sendEmail: false,
        patientEmail: ''
      });
    }, 2000);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    })?.format(amount);
  };

  if (!selectedPayment) {
    return (
      <div className="bg-surface border border-border rounded-lg h-full flex items-center justify-center">
        <div className="text-center">
          <Icon name="CreditCard" size={48} color="var(--color-muted-foreground)" className="mx-auto mb-4" />
          <h3 className="text-lg font-medium text-foreground mb-2">Seleccionar Pago</h3>
          <p className="text-muted-foreground">
            Selecciona un pago de la lista para procesar la transacción
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-surface border border-border rounded-lg h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-foreground">Procesar Pago</h2>
          <div className="flex items-center space-x-2">
            <Icon name="User" size={16} color="var(--color-primary)" />
            <span className="text-sm font-medium text-foreground">{selectedPayment?.patientName}</span>
          </div>
        </div>

        {/* Payment Summary */}
        <div className="bg-muted/30 rounded-lg p-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-muted-foreground">Servicio:</span>
              <div className="font-medium text-foreground">{selectedPayment?.serviceDescription}</div>
            </div>
            <div>
              <span className="text-muted-foreground">Monto original:</span>
              <div className="font-medium text-foreground">{formatCurrency(selectedPayment?.amount)}</div>
            </div>
            <div>
              <span className="text-muted-foreground">Estado:</span>
              <div className="font-medium text-warning">
                {selectedPayment?.status === 'pending' ? 'Pendiente' : 
                 selectedPayment?.status === 'partial' ? 'Pago parcial' : 'Vencido'}
              </div>
            </div>
            <div>
              <span className="text-muted-foreground">Fecha vencimiento:</span>
              <div className="font-medium text-foreground">
                {new Date(selectedPayment.dueDate)?.toLocaleDateString('es-ES')}
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Form Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Payment Amount */}
        <div className="space-y-4">
          <h3 className="text-md font-medium text-foreground">Detalles del Pago</h3>
          
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Monto a pagar"
              type="number"
              value={paymentData?.amount}
              onChange={(e) => handleInputChange('amount', e?.target?.value)}
              placeholder="0.00"
              step="0.01"
              min="0"
              required
            />

            <Select
              label="Método de pago"
              options={paymentMethodOptions}
              value={paymentData?.paymentMethod}
              onChange={(value) => handleInputChange('paymentMethod', value)}
              required
            />
          </div>
        </div>

        {/* Card Details */}
        {showCardDetails && (
          <div className="space-y-4">
            <h3 className="text-md font-medium text-foreground">Detalles de la Tarjeta</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <Select
                label="Tipo de tarjeta"
                options={cardTypeOptions}
                value={paymentData?.cardType}
                onChange={(value) => handleInputChange('cardType', value)}
                required
              />

              <Input
                label="Últimos 4 dígitos"
                type="text"
                value={paymentData?.cardNumber}
                onChange={(e) => handleInputChange('cardNumber', e?.target?.value)}
                placeholder="****"
                maxLength="4"
              />
            </div>
          </div>
        )}

        {/* Installments */}
        {showInstallments && (
          <div className="space-y-4">
            <h3 className="text-md font-medium text-foreground">Plan de Pagos</h3>
            
            <Select
              label="Número de cuotas"
              options={installmentOptions}
              value={paymentData?.installments}
              onChange={(value) => handleInputChange('installments', value)}
            />
          </div>
        )}

        {/* Discount Section */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="applyDiscount"
              checked={paymentData?.applyDiscount}
              onChange={(e) => handleInputChange('applyDiscount', e?.target?.checked)}
              className="rounded border-border"
            />
            <label htmlFor="applyDiscount" className="text-sm font-medium text-foreground">
              Aplicar descuento
            </label>
          </div>

          {paymentData?.applyDiscount && (
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Monto del descuento"
                type="number"
                value={paymentData?.discountAmount}
                onChange={(e) => handleInputChange('discountAmount', e?.target?.value)}
                placeholder="0.00"
                step="0.01"
                min="0"
              />

              <Input
                label="Motivo del descuento"
                type="text"
                value={paymentData?.discountReason}
                onChange={(e) => handleInputChange('discountReason', e?.target?.value)}
                placeholder="Ej: Descuento por fidelidad"
              />
            </div>
          )}
        </div>

        {/* Notes */}
        <div className="space-y-4">
          <Input
            label="Notas adicionales"
            type="text"
            value={paymentData?.notes}
            onChange={(e) => handleInputChange('notes', e?.target?.value)}
            placeholder="Comentarios sobre el pago..."
          />
        </div>

        {/* Receipt Options */}
        <div className="space-y-4">
          <h3 className="text-md font-medium text-foreground">Opciones de Recibo</h3>
          
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="generateReceipt"
                checked={paymentData?.generateReceipt}
                onChange={(e) => handleInputChange('generateReceipt', e?.target?.checked)}
                className="rounded border-border"
              />
              <label htmlFor="generateReceipt" className="text-sm font-medium text-foreground">
                Generar recibo impreso
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="sendEmail"
                checked={paymentData?.sendEmail}
                onChange={(e) => handleInputChange('sendEmail', e?.target?.checked)}
                className="rounded border-border"
              />
              <label htmlFor="sendEmail" className="text-sm font-medium text-foreground">
                Enviar recibo por email
              </label>
            </div>

            {paymentData?.sendEmail && (
              <Input
                label="Email del paciente"
                type="email"
                value={paymentData?.patientEmail}
                onChange={(e) => handleInputChange('patientEmail', e?.target?.value)}
                placeholder="paciente@email.com"
              />
            )}
          </div>
        </div>
      </div>
      {/* Payment Summary & Actions */}
      <div className="p-6 border-t border-border bg-muted/30">
        <div className="space-y-4">
          {/* Calculation Summary */}
          <div className="bg-surface rounded-lg p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Subtotal:</span>
              <span className="text-foreground">{formatCurrency(paymentData?.amount)}</span>
            </div>
            {paymentData?.applyDiscount && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Descuento:</span>
                <span className="text-success">-{formatCurrency(paymentData?.discountAmount)}</span>
              </div>
            )}
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">IVA (21%):</span>
              <span className="text-foreground">{formatCurrency(calculateTax())}</span>
            </div>
            <div className="border-t border-border pt-2">
              <div className="flex justify-between font-semibold">
                <span className="text-foreground">Total:</span>
                <span className="text-foreground text-lg">{formatCurrency(calculateTotal() + calculateTax())}</span>
              </div>
            </div>
            {paymentData?.installments > 1 && (
              <div className="text-xs text-muted-foreground">
                {paymentData?.installments} cuotas de {formatCurrency((calculateTotal() + calculateTax()) / paymentData?.installments)}
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <Button
              variant="default"
              onClick={handleProcessPayment}
              loading={isProcessing}
              iconName="CreditCard"
              iconPosition="left"
              fullWidth
              className="flex-1"
            >
              {isProcessing ? 'Procesando...' : 'Procesar Pago'}
            </Button>
            
            <Button
              variant="outline"
              iconName="FileText"
              iconPosition="left"
              className="px-6"
            >
              Vista Previa
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentEntryForm;