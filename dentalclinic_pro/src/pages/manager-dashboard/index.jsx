import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import Header from '../../components/ui/Header';
import Sidebar from '../../components/ui/Sidebar';
import MetricsCard from './components/MetricsCard';
import QuickActions from './components/QuickActions';
import AppointmentsList from './components/AppointmentsList';
import ActivityFeed from './components/ActivityFeed';
import StaffUtilization from './components/StaffUtilization';
import Button from '../../components/ui/Button';
import Icon from '../../components/AppIcon';

const ManagerDashboard = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000); // Update every minute

    return () => clearInterval(timer);
  }, []);

  const metricsData = [
    {
      title: "Citas de Hoy",
      value: "24",
      change: "+12%",
      changeType: "increase",
      icon: "Calendar",
      color: "primary"
    },
    {
      title: "Ingresos Diarios",
      value: "€2,450",
      change: "+8.5%",
      changeType: "increase",
      icon: "Euro",
      color: "success"
    },
    {
      title: "Pacientes Activos",
      value: "1,247",
      change: "+5.2%",
      changeType: "increase",
      icon: "Users",
      color: "warning"
    },
    {
      title: "Utilización Personal",
      value: "78%",
      change: "-2.1%",
      changeType: "decrease",
      icon: "TrendingUp",
      color: "error"
    }
  ];

  const formatDate = (date) => {
    return date?.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (date) => {
    return date?.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <Helmet>
        <title>Panel de Gestión - DentalClinic Pro</title>
        <meta name="description" content="Panel de control administrativo para la gestión integral de la clínica dental" />
      </Helmet>
      <Header 
        userRole="manager" 
        userName="Dr. García" 
        isCollapsed={sidebarCollapsed}
      />
      <Sidebar 
        userRole="manager"
        isCollapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      <main className={`pt-16 transition-all duration-300 ${
        sidebarCollapsed ? 'ml-16' : 'ml-64'
      }`}>
        <div className="p-6 space-y-6">
          {/* Header Section */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground mb-2">
                Panel de Gestión
              </h1>
              <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <Icon name="Calendar" size={16} />
                  <span>{formatDate(currentTime)}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Icon name="Clock" size={16} />
                  <span>{formatTime(currentTime)}</span>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                iconName="Download"
                iconPosition="left"
                iconSize={16}
              >
                Exportar Datos
              </Button>
              <Button
                variant="default"
                iconName="Plus"
                iconPosition="left"
                iconSize={16}
              >
                Agregar Personal
              </Button>
            </div>
          </div>

          {/* Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {metricsData?.map((metric, index) => (
              <MetricsCard
                key={index}
                title={metric?.title}
                value={metric?.value}
                change={metric?.change}
                changeType={metric?.changeType}
                icon={metric?.icon}
                color={metric?.color}
              />
            ))}
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Panel - Quick Actions */}
            <div className="lg:col-span-4 space-y-6">
              <QuickActions />
              <StaffUtilization />
            </div>

            {/* Center Panel - Appointments and Activity */}
            <div className="lg:col-span-8 space-y-6">
              <AppointmentsList />
              <ActivityFeed />
            </div>
          </div>

          {/* Additional Analytics Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="bg-surface border border-border rounded-lg p-6 shadow-custom-md">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-foreground">Rendimiento Mensual</h3>
                <Icon name="TrendingUp" size={20} color="var(--color-success)" />
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Citas Completadas</span>
                  <span className="text-sm font-medium text-foreground">847</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Ingresos Totales</span>
                  <span className="text-sm font-medium text-success">€45,230</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Nuevos Pacientes</span>
                  <span className="text-sm font-medium text-foreground">127</span>
                </div>
              </div>
            </div>

            <div className="bg-surface border border-border rounded-lg p-6 shadow-custom-md">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-foreground">Alertas del Sistema</h3>
                <Icon name="AlertTriangle" size={20} color="var(--color-warning)" />
              </div>
              <div className="space-y-3">
                <div className="flex items-center space-x-3 p-2 bg-amber-500/10 rounded-md">
                  <Icon name="Package" size={16} color="var(--color-warning)" />
                  <span className="text-sm text-foreground">Stock bajo: Anestesia</span>
                </div>
                <div className="flex items-center space-x-3 p-2 bg-blue-500/10 rounded-md">
                  <Icon name="Calendar" size={16} color="var(--color-primary)" />
                  <span className="text-sm text-foreground">Mantenimiento programado</span>
                </div>
              </div>
            </div>

            <div className="bg-surface border border-border rounded-lg p-6 shadow-custom-md">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-foreground">Acceso Rápido</h3>
                <Icon name="Zap" size={20} color="var(--color-primary)" />
              </div>
              <div className="space-y-2">
                <Button
                  variant="ghost"
                  fullWidth
                  iconName="FileText"
                  iconPosition="left"
                  iconSize={16}
                  className="justify-start"
                >
                  Generar Informe Diario
                </Button>
                <Button
                  variant="ghost"
                  fullWidth
                  iconName="Settings"
                  iconPosition="left"
                  iconSize={16}
                  className="justify-start"
                >
                  Configuración Avanzada
                </Button>
                <Button
                  variant="ghost"
                  fullWidth
                  iconName="HelpCircle"
                  iconPosition="left"
                  iconSize={16}
                  className="justify-start"
                >
                  Centro de Ayuda
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ManagerDashboard;