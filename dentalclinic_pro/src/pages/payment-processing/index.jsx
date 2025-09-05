import React, { useState, useEffect } from 'react';
import Header from '../../components/ui/Header';
import Sidebar from '../../components/ui/Sidebar';
import PaymentStats from './components/PaymentStats';
import PaymentFilters from './components/PaymentFilters';
import QuickActions from './components/QuickActions';
import PendingPaymentsList from './components/PendingPaymentsList';
import PaymentEntryForm from './components/PaymentEntryForm';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const PaymentProcessing = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [selectedPayment, setSelectedPayment] = useState(null);
  const [activeFilters, setActiveFilters] = useState({
    dateRange: 'today',
    paymentMethod: 'all',
    status: 'all',
    amountRange: 'all',
    insuranceType: 'all',
    searchTerm: ''
  });
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [lastProcessedPayment, setLastProcessedPayment] = useState(null);

  // Mock user data - in real app this would come from auth context
  const currentUser = {
    role: 'secretary',
    name: 'Carmen Martínez',
    email: 'carmen.martinez@dentalclinic.es'
  };

  useEffect(() => {
    // Auto-hide success message after 5 seconds
    if (showSuccessMessage) {
      const timer = setTimeout(() => {
        setShowSuccessMessage(false);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [showSuccessMessage]);

  const handleToggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const handleSelectPayment = (payment) => {
    setSelectedPayment(payment);
  };

  const handleFiltersChange = (newFilters) => {
    setActiveFilters(newFilters);
    // In real app, this would trigger API call to filter payments
    console.log('Filters updated:', newFilters);
  };

  const handleQuickAction = (actionId) => {
    switch (actionId) {
      case 'new_payment':
        setSelectedPayment({
          id: 'NEW',
          patientName: 'Nuevo Paciente',
          serviceDescription: 'Servicio personalizado',
          amount: 0,
          status: 'pending'
        });
        break;
      case 'scan_barcode':
        // Handle barcode scan result
        console.log('Barcode scanned');
        break;
      case 'insurance_claim':
        // Open insurance claim modal
        console.log('Insurance claim initiated');
        break;
      case 'payment_plan':
        // Open payment plan setup
        console.log('Payment plan setup');
        break;
      case 'generate_invoice':
        // Open invoice generator
        console.log('Invoice generator opened');
        break;
      case 'daily_report':
        // Generate daily report
        console.log('Daily report generated');
        break;
      default:
        console.log('Unknown action:', actionId);
    }
  };

  const handlePaymentProcessed = (processedPayment) => {
    setLastProcessedPayment(processedPayment);
    setShowSuccessMessage(true);
    setSelectedPayment(null);
    
    // In real app, this would update the payments list
    console.log('Payment processed:', processedPayment);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    })?.format(amount);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <Header 
        userRole={currentUser?.role}
        userName={currentUser?.name}
        isCollapsed={isSidebarCollapsed}
      />
      {/* Sidebar */}
      <Sidebar
        userRole={currentUser?.role}
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={handleToggleSidebar}
      />
      {/* Main Content */}
      <main 
        className={`transition-all duration-300 ${
          isSidebarCollapsed ? 'ml-16' : 'ml-64'
        } mt-16 min-h-screen`}
      >
        <div className="p-6">
          {/* Page Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-foreground mb-2">
                Procesamiento de Pagos
              </h1>
              <p className="text-muted-foreground">
                Gestiona facturación, pagos y reclamaciones de seguros médicos
              </p>
            </div>
            
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                iconName="Download"
                iconPosition="left"
                iconSize={16}
              >
                Exportar
              </Button>
              <Button
                variant="default"
                iconName="Plus"
                iconPosition="left"
                iconSize={16}
                onClick={() => handleQuickAction('new_payment')}
              >
                Nuevo Pago
              </Button>
            </div>
          </div>

          {/* Success Message */}
          {showSuccessMessage && lastProcessedPayment && (
            <div className="mb-6 p-4 bg-success/10 border border-success/20 rounded-lg">
              <div className="flex items-start space-x-3">
                <Icon name="CheckCircle" size={20} color="var(--color-success)" />
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-success mb-1">
                    Pago Procesado Exitosamente
                  </h3>
                  <p className="text-sm text-success/80">
                    Pago de {formatCurrency(lastProcessedPayment?.totalAmount)} para{' '}
                    {lastProcessedPayment?.patientName} ha sido procesado correctamente.
                  </p>
                  <p className="text-xs text-success/60 mt-1">
                    ID de transacción: {lastProcessedPayment?.transactionId}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  onClick={() => setShowSuccessMessage(false)}
                  iconName="X"
                  iconSize={16}
                  className="text-success hover:bg-success/10"
                />
              </div>
            </div>
          )}

          {/* Payment Statistics */}
          <PaymentStats />

          {/* Quick Actions */}
          <QuickActions onActionSelect={handleQuickAction} />

          {/* Filters */}
          <PaymentFilters 
            onFiltersChange={handleFiltersChange}
            activeFilters={activeFilters}
          />

          {/* Main Content Grid */}
          <div className="grid grid-cols-12 gap-6">
            {/* Pending Payments List - Left Panel (5 columns) */}
            <div className="col-span-12 lg:col-span-5">
              <PendingPaymentsList
                onSelectPayment={handleSelectPayment}
                selectedPaymentId={selectedPayment?.id}
              />
            </div>

            {/* Payment Entry Form - Right Panel (7 columns) */}
            <div className="col-span-12 lg:col-span-7">
              <PaymentEntryForm
                selectedPayment={selectedPayment}
                onPaymentProcessed={handlePaymentProcessed}
              />
            </div>
          </div>

          {/* Mobile View Helper */}
          <div className="lg:hidden mt-6 p-4 bg-warning/10 border border-warning/20 rounded-lg">
            <div className="flex items-start space-x-3">
              <Icon name="Smartphone" size={20} color="var(--color-warning)" />
              <div>
                <h3 className="text-sm font-medium text-warning mb-1">
                  Vista Móvil Limitada
                </h3>
                <p className="text-sm text-warning/80">
                  Para una experiencia completa de procesamiento de pagos, 
                  recomendamos usar un dispositivo de escritorio o tablet.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PaymentProcessing;