import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Header from '../../components/ui/Header';
import PatientContextBar from '../../components/ui/PatientContextBar';
import PaymentSummaryCard from './components/PaymentSummaryCard';
import PaymentMethodSelector from './components/PaymentMethodSelector';
import DentistDistributionCard from './components/DentistDistributionCard';
import PaymentHistoryPanel from './components/PaymentHistoryPanel';
import ReceiptGenerator from './components/ReceiptGenerator';
import Button from '../../components/ui/Button';
import Icon from '../../components/AppIcon';

const PaymentProcessing = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [currentStep, setCurrentStep] = useState('payment');
  const [exchangeRate, setExchangeRate] = useState(36.45);
  const [paymentData, setPaymentData] = useState({
    methods: {},
    amounts: {},
    distribution: {}
  });
  const [showHistory, setShowHistory] = useState(false);

  // Mock consultation data
  const consultation = {
    id: 'CONS-2024-0892',
    date: '2024-01-04',
    time: '14:30',
    patient: {
      id: 'P-2024-0892',
      name: 'Ana María Rodríguez',
      age: 34,
      phone: '+58 412-555-0123',
      email: 'ana.rodriguez@email.com'
    },
    services: [
      {
        id: 'SRV-001',
        name: 'Limpieza Dental Profunda',
        dentist: 'María González',
        tooth: '16-26',
        priceBs: 1200000,
        priceUsd: 32.88,
        duration: 45
      },
      {
        id: 'SRV-002',
        name: 'Empaste Composite',
        dentist: 'Carlos Mendoza',
        tooth: '14',
        priceBs: 1650000,
        priceUsd: 45.27,
        duration: 60
      },
      {
        id: 'SRV-003',
        name: 'Radiografía Panorámica',
        dentist: 'María González',
        tooth: 'General',
        priceBs: 800000,
        priceUsd: 21.92,
        duration: 15
      }
    ],
    status: 'completed',
    notes: 'Consulta completada satisfactoriamente. Paciente sin complicaciones.'
  };

  useEffect(() => {
    // Update exchange rate periodically
    const interval = setInterval(() => {
      setExchangeRate(prev => prev + (Math.random() - 0.5) * 0.1);
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  const calculateTotals = () => {
    const subtotalBs = consultation?.services?.reduce((sum, service) => sum + service?.priceBs, 0);
    const subtotalUsd = consultation?.services?.reduce((sum, service) => sum + service?.priceUsd, 0);
    const taxBs = subtotalBs * 0.16;
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

  const handlePaymentChange = (methods, amounts) => {
    setPaymentData(prev => ({
      ...prev,
      methods,
      amounts
    }));
  };

  const handleDistributionChange = (distribution) => {
    setPaymentData(prev => ({
      ...prev,
      distribution
    }));
  };

  const handleProcessPayment = () => {
    // Mock payment processing
    console.log('Processing payment:', paymentData);
    setCurrentStep('receipt');
  };

  const handleReceiptGenerated = (receiptData) => {
    console.log('Receipt generated:', receiptData);
  };

  const handleNewPayment = () => {
    setCurrentStep('payment');
    setPaymentData({
      methods: {},
      amounts: {},
      distribution: {}
    });
  };

  const isPaymentComplete = () => {
    const paidBs = Object.values(paymentData?.amounts)?.reduce((sum, amount) => sum + (amount || 0), 0);
    return paidBs >= totals?.totalBs * 0.95; // Allow 5% tolerance
  };

  const steps = [
    { id: 'payment', label: 'Pago', icon: 'CreditCard' },
    { id: 'distribution', label: 'Distribución', icon: 'Users' },
    { id: 'receipt', label: 'Recibo', icon: 'Receipt' }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <PatientContextBar 
        patient={consultation?.patient}
        showQueueStatus={false}
        className="mt-16"
      />
      <div className="container mx-auto px-6 py-8">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Procesamiento de Pagos</h1>
            <p className="text-muted-foreground mt-2">
              Gestione el pago y distribución de honorarios para la consulta completada
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <Button
              variant="outline"
              onClick={() => setShowHistory(!showHistory)}
              iconName="History"
            >
              {showHistory ? 'Ocultar' : 'Ver'} Historial
            </Button>
            
            <Button
              variant="outline"
              onClick={() => navigate('/patient-consultation')}
              iconName="ArrowLeft"
            >
              Volver a Consulta
            </Button>
          </div>
        </div>

        {/* Progress Steps */}
        <div className="bg-card border border-border rounded-lg p-4 mb-8">
          <div className="flex items-center justify-between">
            {steps?.map((step, index) => (
              <div key={step?.id} className="flex items-center">
                <div className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-smooth ${
                  currentStep === step?.id 
                    ? 'bg-primary text-primary-foreground' 
                    : index < steps?.findIndex(s => s?.id === currentStep)
                      ? 'bg-success text-success-foreground'
                      : 'bg-muted text-muted-foreground'
                }`}>
                  <Icon name={step?.icon} size={16} />
                  <span className="font-medium">{step?.label}</span>
                </div>
                
                {index < steps?.length - 1 && (
                  <Icon 
                    name="ChevronRight" 
                    size={16} 
                    className="mx-4 text-muted-foreground" 
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="xl:col-span-2 space-y-8">
            {/* Payment Summary - Always visible */}
            <PaymentSummaryCard 
              consultation={consultation}
              exchangeRate={exchangeRate}
            />

            {/* Step Content */}
            {currentStep === 'payment' && (
              <PaymentMethodSelector
                totalBs={totals?.totalBs}
                totalUsd={totals?.totalUsd}
                exchangeRate={exchangeRate}
                onPaymentChange={handlePaymentChange}
              />
            )}

            {currentStep === 'distribution' && (
              <DentistDistributionCard
                consultation={consultation}
                onDistributionChange={handleDistributionChange}
              />
            )}

            {currentStep === 'receipt' && (
              <ReceiptGenerator
                consultation={consultation}
                paymentData={paymentData}
                exchangeRate={exchangeRate}
                onReceiptGenerated={handleReceiptGenerated}
              />
            )}

            {/* Action Buttons */}
            <div className="flex items-center justify-between bg-card border border-border rounded-lg p-6">
              <div className="flex items-center space-x-4">
                {currentStep !== 'payment' && (
                  <Button
                    variant="outline"
                    onClick={() => {
                      const currentIndex = steps?.findIndex(s => s?.id === currentStep);
                      if (currentIndex > 0) {
                        setCurrentStep(steps?.[currentIndex - 1]?.id);
                      }
                    }}
                    iconName="ArrowLeft"
                  >
                    Anterior
                  </Button>
                )}
              </div>

              <div className="flex items-center space-x-4">
                {currentStep === 'payment' && (
                  <Button
                    onClick={() => setCurrentStep('distribution')}
                    disabled={!isPaymentComplete()}
                    iconName="ArrowRight"
                    iconPosition="right"
                  >
                    Continuar a Distribución
                  </Button>
                )}

                {currentStep === 'distribution' && (
                  <Button
                    onClick={handleProcessPayment}
                    iconName="CreditCard"
                  >
                    Procesar Pago
                  </Button>
                )}

                {currentStep === 'receipt' && (
                  <Button
                    onClick={handleNewPayment}
                    iconName="Plus"
                  >
                    Nuevo Pago
                  </Button>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Payment History */}
            {showHistory && (
              <PaymentHistoryPanel patientId={consultation?.patient?.id} />
            )}

            {/* Quick Stats */}
            <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
              <h3 className="text-lg font-semibold text-foreground mb-4">Estadísticas Rápidas</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Icon name="DollarSign" size={16} className="text-primary" />
                    <span className="text-sm text-muted-foreground">Tasa Actual:</span>
                  </div>
                  <span className="font-mono text-sm font-medium text-foreground">
                    {exchangeRate?.toFixed(2)} Bs/USD
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Icon name="Users" size={16} className="text-accent" />
                    <span className="text-sm text-muted-foreground">Dentistas:</span>
                  </div>
                  <span className="text-sm font-medium text-foreground">
                    {new Set(consultation.services.map(s => s.dentist))?.size}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Icon name="Clock" size={16} className="text-warning" />
                    <span className="text-sm text-muted-foreground">Duración Total:</span>
                  </div>
                  <span className="text-sm font-medium text-foreground">
                    {consultation?.services?.reduce((sum, s) => sum + s?.duration, 0)} min
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Icon name="Tooth" size={16} className="text-success" />
                    <span className="text-sm text-muted-foreground">Servicios:</span>
                  </div>
                  <span className="text-sm font-medium text-foreground">
                    {consultation?.services?.length}
                  </span>
                </div>
              </div>
            </div>

            {/* Exchange Rate History */}
            <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
              <h3 className="text-lg font-semibold text-foreground mb-4">Tasa de Cambio</h3>
              
              <div className="space-y-3">
                <div className="text-center">
                  <div className="text-2xl font-mono font-bold text-primary">
                    {exchangeRate?.toFixed(2)}
                  </div>
                  <div className="text-sm text-muted-foreground">Bs por USD</div>
                </div>

                <div className="text-xs text-muted-foreground text-center">
                  Actualizado: {new Date()?.toLocaleTimeString('es-VE')}
                </div>

                <div className="bg-muted rounded p-3 text-xs space-y-1">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Apertura:</span>
                    <span className="text-foreground">36.33 Bs</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Máximo:</span>
                    <span className="text-foreground">36.52 Bs</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Mínimo:</span>
                    <span className="text-foreground">36.28 Bs</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentProcessing;