import React, { useState } from 'react';
import Header from '../../components/ui/Header';
import Sidebar from '../../components/ui/Sidebar';
import TodaySchedule from './components/TodaySchedule';
import PatientRegistration from './components/PatientRegistration';
import PaymentProcessing from './components/PaymentProcessing';
import QuickActions from './components/QuickActions';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';

const SecretaryDashboard = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [activePanel, setActivePanel] = useState('schedule');

  const currentUser = {
    name: "Carmen López",
    role: "secretary"
  };

  const panelOptions = [
    {
      id: 'schedule',
      label: 'Agenda del Día',
      icon: 'Calendar',
      component: TodaySchedule
    },
    {
      id: 'patients',
      label: 'Gestión de Pacientes',
      icon: 'Users',
      component: PatientRegistration
    },
    {
      id: 'payments',
      label: 'Procesamiento de Pagos',
      icon: 'CreditCard',
      component: PaymentProcessing
    }
  ];

  const handleSidebarToggle = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const ActivePanelComponent = panelOptions?.find(panel => panel?.id === activePanel)?.component || TodaySchedule;

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
        onToggleCollapse={handleSidebarToggle}
      />
      {/* Main Content */}
      <main 
        className={`transition-all duration-300 pt-16 ${
          isSidebarCollapsed ? 'ml-16' : 'ml-64'
        }`}
      >
        <div className="p-6">
          {/* Dashboard Header */}
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-foreground mb-2">
                  Panel de Secretaría
                </h1>
                <p className="text-muted-foreground">
                  Gestiona las operaciones diarias de la clínica dental
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="text-sm font-medium text-foreground">
                    {currentUser?.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Secretaria
                  </p>
                </div>
                <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
                  <Icon name="User" size={20} color="var(--color-primary-foreground)" />
                </div>
              </div>
            </div>
          </div>

          {/* Panel Navigation */}
          <div className="mb-6">
            <div className="flex items-center space-x-1 bg-surface rounded-lg p-1 border border-border">
              {panelOptions?.map((panel) => (
                <Button
                  key={panel?.id}
                  variant={activePanel === panel?.id ? "default" : "ghost"}
                  onClick={() => setActivePanel(panel?.id)}
                  iconName={panel?.icon}
                  iconPosition="left"
                  iconSize={16}
                  className="flex-1 text-sm font-medium"
                >
                  {panel?.label}
                </Button>
              ))}
            </div>
          </div>

          {/* Dashboard Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-200px)]">
            {/* Left Panel - Today's Schedule (3 columns) */}
            <div className="lg:col-span-3">
              {activePanel === 'schedule' ? (
                <TodaySchedule />
              ) : (
                <div className="bg-surface rounded-lg border border-border shadow-custom-md p-4">
                  <h3 className="text-sm font-medium text-foreground mb-3 flex items-center">
                    <Icon name="Calendar" size={16} className="mr-2" />
                    Agenda Rápida
                  </h3>
                  <div className="space-y-2">
                    <div className="p-2 bg-card rounded border border-border">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono text-primary">14:30</span>
                        <span className="text-xs text-muted-foreground">Laura S.</span>
                      </div>
                    </div>
                    <div className="p-2 bg-card rounded border border-border">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono text-primary">15:00</span>
                        <span className="text-xs text-muted-foreground">Miguel T.</span>
                      </div>
                    </div>
                    <div className="p-2 bg-card rounded border border-border">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono text-primary">15:30</span>
                        <span className="text-xs text-muted-foreground">Carmen R.</span>
                      </div>
                    </div>
                  </div>
                  <Button
                    variant="outline"
                    fullWidth
                    onClick={() => setActivePanel('schedule')}
                    className="mt-3 text-xs"
                  >
                    Ver Agenda Completa
                  </Button>
                </div>
              )}
            </div>

            {/* Center Panel - Main Content (6 columns) */}
            <div className="lg:col-span-6">
              <ActivePanelComponent />
            </div>

            {/* Right Panel - Quick Actions & Payment Tools (3 columns) */}
            <div className="lg:col-span-3">
              {activePanel === 'payments' ? (
                <div className="bg-surface rounded-lg border border-border shadow-custom-md p-4">
                  <h3 className="text-sm font-medium text-foreground mb-3 flex items-center">
                    <Icon name="TrendingUp" size={16} className="mr-2" />
                    Resumen Financiero
                  </h3>
                  <div className="space-y-3">
                    <div className="p-3 bg-card rounded border border-border">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">Ingresos Hoy</span>
                        <span className="text-sm font-semibold text-success">€295.00</span>
                      </div>
                    </div>
                    <div className="p-3 bg-card rounded border border-border">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">Pendientes</span>
                        <span className="text-sm font-semibold text-warning">€525.00</span>
                      </div>
                    </div>
                    <div className="p-3 bg-card rounded border border-border">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">Este Mes</span>
                        <span className="text-sm font-semibold text-primary">€2,450.00</span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <QuickActions />
              )}
            </div>
          </div>

          {/* Mobile View - Stacked Layout */}
          <div className="lg:hidden mt-6">
            <div className="space-y-6">
              {activePanel === 'schedule' && <TodaySchedule />}
              {activePanel === 'patients' && <PatientRegistration />}
              {activePanel === 'payments' && <PaymentProcessing />}
            </div>
          </div>
        </div>
      </main>
      {/* Footer */}
      <footer className={`bg-surface border-t border-border py-4 transition-all duration-300 ${
        isSidebarCollapsed ? 'ml-16' : 'ml-64'
      }`}>
        <div className="px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-6 h-6 bg-primary rounded flex items-center justify-center">
                  <Icon name="Stethoscope" size={14} color="var(--color-primary-foreground)" />
                </div>
                <span className="text-sm font-medium text-foreground">DentalClinic Pro</span>
              </div>
              <span className="text-xs text-muted-foreground">
                Sistema de Gestión Dental
              </span>
            </div>
            <div className="flex items-center space-x-4 text-xs text-muted-foreground">
              <span>Versión 2.1.0</span>
              <span>© {new Date()?.getFullYear()} DentalClinic Pro</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default SecretaryDashboard;