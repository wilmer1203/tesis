import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Icon from '../AppIcon';
import Button from './Button';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [queueCount, setQueueCount] = useState(12);
  const [urgentAlerts, setUrgentAlerts] = useState(2);
  const [exchangeRate, setExchangeRate] = useState(36.45);
  const [lastRateUpdate, setLastRateUpdate] = useState(new Date());
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showMoreMenu, setShowMoreMenu] = useState(false);
  const [showRateDetails, setShowRateDetails] = useState(false);

  const navigationItems = [
    { 
      label: 'Pacientes', 
      path: '/patient-registration', 
      icon: 'Users',
      tooltip: 'Registro y búsqueda de pacientes'
    },
    { 
      label: 'Colas', 
      path: '/queue-management-dashboard', 
      icon: 'Clock',
      tooltip: 'Gestión de colas y turnos'
    },
    { 
      label: 'Consultas', 
      path: '/patient-consultation', 
      icon: 'Stethoscope',
      tooltip: 'Consultas y tratamientos'
    },
    { 
      label: 'Pagos', 
      path: '/payment-processing', 
      icon: 'CreditCard',
      tooltip: 'Procesamiento de pagos'
    },
    { 
      label: 'Reportes', 
      path: '/reports-dashboard', 
      icon: 'BarChart3',
      tooltip: 'Reportes y análisis'
    }
  ];

  const moreMenuItems = [
    { label: 'Configuración', icon: 'Settings', action: () => console.log('Settings') },
    { label: 'Ayuda', icon: 'HelpCircle', action: () => console.log('Help') },
    { label: 'Administración', icon: 'Shield', action: () => console.log('Admin') }
  ];

  const currentUser = {
    name: 'Dr. María González',
    role: 'Dentista',
    avatar: '/assets/images/avatar-placeholder.png'
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setQueueCount(prev => Math.max(0, prev + Math.floor(Math.random() * 3) - 1));
      setExchangeRate(prev => prev + (Math.random() - 0.5) * 0.1);
      setLastRateUpdate(new Date());
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const handleNavigation = (path) => {
    navigate(path);
  };

  const handleQueueClick = () => {
    navigate('/queue-management-dashboard');
  };

  const handleLogout = () => {
    console.log('Logout');
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-card border-b border-border shadow-soft">
      <div className="flex items-center justify-between h-16 px-6">
        {/* Logo */}
        <div className="flex items-center">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Icon name="Tooth" size={20} color="white" />
            </div>
            <span className="text-xl font-semibold text-foreground">DentalFlow</span>
          </div>
        </div>

        {/* Primary Navigation */}
        <nav className="hidden md:flex items-center space-x-1">
          {navigationItems?.map((item) => (
            <button
              key={item?.path}
              onClick={() => handleNavigation(item?.path)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-smooth ${
                location?.pathname === item?.path
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              }`}
              title={item?.tooltip}
            >
              <Icon name={item?.icon} size={16} />
              <span>{item?.label}</span>
            </button>
          ))}
        </nav>

        {/* Right Section */}
        <div className="flex items-center space-x-4">
          {/* Queue Status */}
          <button
            onClick={handleQueueClick}
            className="hidden sm:flex items-center space-x-2 px-3 py-2 bg-muted rounded-md hover:bg-muted/80 transition-smooth"
            title="Ver cola de pacientes"
          >
            <Icon name="Users" size={16} className="text-muted-foreground" />
            <span className="text-sm font-medium text-foreground">{queueCount}</span>
            {urgentAlerts > 0 && (
              <div className="w-2 h-2 bg-error rounded-full"></div>
            )}
          </button>

          {/* Exchange Rate */}
          <div className="relative">
            <button
              onClick={() => setShowRateDetails(!showRateDetails)}
              className="hidden lg:flex items-center space-x-2 px-3 py-2 text-sm text-muted-foreground hover:text-foreground transition-smooth"
              title="Tasa de cambio actual"
            >
              <Icon name="DollarSign" size={14} />
              <span className="font-mono">{exchangeRate?.toFixed(2)} Bs</span>
            </button>

            {showRateDetails && (
              <div className="absolute right-0 top-full mt-2 w-64 bg-popover border border-border rounded-md shadow-modal p-4 z-10">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">USD/VES</span>
                    <span className="font-mono text-lg">{exchangeRate?.toFixed(2)}</span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Actualizado: {lastRateUpdate?.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* More Menu */}
          <div className="relative">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowMoreMenu(!showMoreMenu)}
              iconName="MoreHorizontal"
              className="hidden md:flex"
            >
            </Button>

            {showMoreMenu && (
              <div className="absolute right-0 top-full mt-2 w-48 bg-popover border border-border rounded-md shadow-modal py-2 z-10">
                {moreMenuItems?.map((item, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      item?.action();
                      setShowMoreMenu(false);
                    }}
                    className="w-full flex items-center space-x-3 px-4 py-2 text-sm text-foreground hover:bg-muted transition-smooth"
                  >
                    <Icon name={item?.icon} size={16} />
                    <span>{item?.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-3 p-2 rounded-md hover:bg-muted transition-smooth"
            >
              <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
                <Icon name="User" size={16} color="white" />
              </div>
              <div className="hidden sm:block text-left">
                <div className="text-sm font-medium text-foreground">{currentUser?.name}</div>
                <div className="text-xs text-muted-foreground">{currentUser?.role}</div>
              </div>
              <Icon name="ChevronDown" size={16} className="text-muted-foreground" />
            </button>

            {showUserMenu && (
              <div className="absolute right-0 top-full mt-2 w-56 bg-popover border border-border rounded-md shadow-modal py-2 z-10">
                <div className="px-4 py-2 border-b border-border">
                  <div className="text-sm font-medium text-foreground">{currentUser?.name}</div>
                  <div className="text-xs text-muted-foreground">{currentUser?.role}</div>
                </div>
                <button
                  onClick={() => {
                    console.log('Profile');
                    setShowUserMenu(false);
                  }}
                  className="w-full flex items-center space-x-3 px-4 py-2 text-sm text-foreground hover:bg-muted transition-smooth"
                >
                  <Icon name="User" size={16} />
                  <span>Mi Perfil</span>
                </button>
                <button
                  onClick={() => {
                    console.log('Preferences');
                    setShowUserMenu(false);
                  }}
                  className="w-full flex items-center space-x-3 px-4 py-2 text-sm text-foreground hover:bg-muted transition-smooth"
                >
                  <Icon name="Settings" size={16} />
                  <span>Preferencias</span>
                </button>
                <div className="border-t border-border mt-2 pt-2">
                  <button
                    onClick={() => {
                      handleLogout();
                      setShowUserMenu(false);
                    }}
                    className="w-full flex items-center space-x-3 px-4 py-2 text-sm text-error hover:bg-muted transition-smooth"
                  >
                    <Icon name="LogOut" size={16} />
                    <span>Cerrar Sesión</span>
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="sm"
            iconName="Menu"
            className="md:hidden"
            onClick={() => console.log('Mobile menu')}
          >
          </Button>
        </div>
      </div>
      {/* Mobile Navigation */}
      <div className="md:hidden border-t border-border bg-card">
        <nav className="flex overflow-x-auto py-2 px-4 space-x-1">
          {navigationItems?.map((item) => (
            <button
              key={item?.path}
              onClick={() => handleNavigation(item?.path)}
              className={`flex flex-col items-center space-y-1 px-3 py-2 rounded-md text-xs font-medium whitespace-nowrap transition-smooth ${
                location?.pathname === item?.path
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              }`}
            >
              <Icon name={item?.icon} size={16} />
              <span>{item?.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};

export default Header;