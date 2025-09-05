import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/ui/Header';
import ReportCategoryTabs from './components/ReportCategoryTabs';
import DateRangeSelector from './components/DateRangeSelector';
import FinancialReports from './components/FinancialReports';
import PerformanceReports from './components/PerformanceReports';
import PatientAnalytics from './components/PatientAnalytics';
import OperationalMetrics from './components/OperationalMetrics';
import ReportExportPanel from './components/ReportExportPanel';
import CustomReportBuilder from './components/CustomReportBuilder';
import KPIDashboard from './components/KPIDashboard';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const ReportsDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('financial');
  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // Last 7 days
    end: new Date(),
    preset: 'week'
  });
  const [showExportPanel, setShowExportPanel] = useState(false);
  const [showCustomBuilder, setShowCustomBuilder] = useState(false);
  const [showKPIDashboard, setShowKPIDashboard] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Set page title
  useEffect(() => {
    document.title = 'Dashboard de Reportes - DentalFlow';
  }, []);

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
    setIsLoading(true);
    
    // Simulate loading
    setTimeout(() => {
      setIsLoading(false);
    }, 500);
  };

  const handleDateRangeChange = (newRange) => {
    setDateRange(newRange);
    setIsLoading(true);
    
    // Simulate data refresh
    setTimeout(() => {
      setIsLoading(false);
    }, 300);
  };

  const handleQuickNavigation = (path) => {
    navigate(path);
  };

  const renderReportContent = () => {
    if (isLoading) {
      return (
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Cargando datos del reporte...</p>
          </div>
        </div>
      );
    }

    switch (activeTab) {
      case 'financial':
        return <FinancialReports dateRange={dateRange} />;
      case 'performance':
        return <PerformanceReports dateRange={dateRange} />;
      case 'patients':
        return <PatientAnalytics dateRange={dateRange} />;
      case 'operations':
        return <OperationalMetrics dateRange={dateRange} />;
      default:
        return <FinancialReports dateRange={dateRange} />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="pt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Page Header */}
          <div className="mb-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold text-foreground">Dashboard de Reportes</h1>
                <p className="text-muted-foreground mt-1">
                  Análisis completo y métricas de rendimiento de la clínica
                </p>
              </div>
              
              <div className="flex items-center space-x-3">
                <Button
                  variant={showKPIDashboard ? 'default' : 'outline'}
                  onClick={() => setShowKPIDashboard(!showKPIDashboard)}
                  iconName="Activity"
                  iconPosition="left"
                >
                  KPI en Vivo
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => setShowCustomBuilder(!showCustomBuilder)}
                  iconName="Settings"
                  iconPosition="left"
                >
                  Reporte Personalizado
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => setShowExportPanel(!showExportPanel)}
                  iconName="Download"
                  iconPosition="left"
                >
                  Exportar
                </Button>
              </div>
            </div>
          </div>

          {/* Quick Navigation */}
          <div className="mb-6 p-4 bg-card border border-border rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <Icon name="Zap" size={16} className="text-primary" />
              <span className="text-sm font-medium text-foreground">Navegación Rápida</span>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => handleQuickNavigation('/patient-registration')}
                className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-muted hover:bg-muted/80 rounded-md transition-smooth"
              >
                <Icon name="UserPlus" size={14} />
                <span>Registrar Paciente</span>
              </button>
              <button
                onClick={() => handleQuickNavigation('/queue-management-dashboard')}
                className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-muted hover:bg-muted/80 rounded-md transition-smooth"
              >
                <Icon name="Users" size={14} />
                <span>Gestionar Cola</span>
              </button>
              <button
                onClick={() => handleQuickNavigation('/patient-consultation')}
                className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-muted hover:bg-muted/80 rounded-md transition-smooth"
              >
                <Icon name="Stethoscope" size={14} />
                <span>Nueva Consulta</span>
              </button>
              <button
                onClick={() => handleQuickNavigation('/payment-processing')}
                className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-muted hover:bg-muted/80 rounded-md transition-smooth"
              >
                <Icon name="CreditCard" size={14} />
                <span>Procesar Pago</span>
              </button>
            </div>
          </div>

          {/* KPI Dashboard */}
          {showKPIDashboard && (
            <div className="mb-8">
              <KPIDashboard />
            </div>
          )}

          {/* Custom Report Builder */}
          {showCustomBuilder && (
            <div className="mb-8">
              <div className="bg-card border border-border rounded-lg p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-foreground">Constructor de Reportes Personalizados</h2>
                  <button
                    onClick={() => setShowCustomBuilder(false)}
                    className="p-2 hover:bg-muted rounded-md transition-smooth"
                  >
                    <Icon name="X" size={16} className="text-muted-foreground" />
                  </button>
                </div>
                <CustomReportBuilder />
              </div>
            </div>
          )}

          {/* Export Panel */}
          {showExportPanel && (
            <div className="mb-8">
              <div className="bg-card border border-border rounded-lg p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-foreground">Panel de Exportación</h2>
                  <button
                    onClick={() => setShowExportPanel(false)}
                    className="p-2 hover:bg-muted rounded-md transition-smooth"
                  >
                    <Icon name="X" size={16} className="text-muted-foreground" />
                  </button>
                </div>
                <ReportExportPanel activeTab={activeTab} dateRange={dateRange} />
              </div>
            </div>
          )}

          {/* Report Category Tabs */}
          <div className="mb-6">
            <ReportCategoryTabs 
              activeTab={activeTab} 
              onTabChange={handleTabChange}
            />
          </div>

          {/* Date Range Selector */}
          <div className="mb-6">
            <DateRangeSelector 
              dateRange={dateRange}
              onDateRangeChange={handleDateRangeChange}
            />
          </div>

          {/* Report Content */}
          <div className="space-y-6">
            {renderReportContent()}
          </div>

          {/* Footer Actions */}
          <div className="mt-12 pt-8 border-t border-border">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="text-sm text-muted-foreground">
                Datos actualizados automáticamente cada 5 minutos • 
                Última actualización: {new Date()?.toLocaleTimeString('es-VE')}
              </div>
              
              <div className="flex items-center space-x-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.location?.reload()}
                  iconName="RefreshCw"
                  iconPosition="left"
                >
                  Actualizar Datos
                </Button>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowExportPanel(true)}
                  iconName="Share"
                  iconPosition="left"
                >
                  Compartir Reporte
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ReportsDashboard;