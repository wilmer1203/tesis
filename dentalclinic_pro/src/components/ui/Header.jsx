import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Icon from '../AppIcon';
import Button from './Button';

const Header = ({ userRole = 'manager', userName = 'Dr. Smith', isCollapsed = false }) => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navigationItems = [
    {
      label: 'Dashboard',
      path: `/${userRole}-dashboard`,
      icon: 'LayoutDashboard',
      roles: ['manager', 'secretary', 'dentist']
    },
    {
      label: 'Patients',
      path: '/patient-management',
      icon: 'Users',
      roles: ['manager', 'secretary', 'dentist']
    },
    {
      label: 'Appointments',
      path: '/appointment-scheduling',
      icon: 'Calendar',
      roles: ['manager', 'secretary', 'dentist']
    },
    {
      label: 'Payments',
      path: '/payment-processing',
      icon: 'CreditCard',
      roles: ['manager', 'secretary']
    }
  ];

  const filteredNavItems = navigationItems?.filter(item => 
    item?.roles?.includes(userRole)
  );

  const isActivePath = (path) => {
    return location?.pathname === path;
  };

  const getRoleDisplayName = (role) => {
    const roleNames = {
      manager: 'Practice Manager',
      secretary: 'Secretary',
      dentist: 'Dentist'
    };
    return roleNames?.[role] || role;
  };

  const handleNavigation = (path) => {
    window.location.href = path;
    setIsMobileMenuOpen(false);
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-1000 bg-surface border-b border-border shadow-custom-md">
      <div className="flex items-center justify-between h-16 px-6">
        {/* Logo Section */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Icon name="Stethoscope" size={20} color="var(--color-primary-foreground)" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-heading font-semibold text-foreground">
                DentalClinic Pro
              </span>
              <span className="text-xs text-muted-foreground font-caption">
                Healthcare Management
              </span>
            </div>
          </div>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center space-x-1">
          {filteredNavItems?.map((item) => (
            <Button
              key={item?.path}
              variant={isActivePath(item?.path) ? "default" : "ghost"}
              onClick={() => handleNavigation(item?.path)}
              iconName={item?.icon}
              iconPosition="left"
              iconSize={18}
              className="px-4 py-2 text-sm font-medium transition-all duration-150"
            >
              {item?.label}
            </Button>
          ))}
        </nav>

        {/* User Profile Section */}
        <div className="flex items-center space-x-4">
          {/* Role Indicator */}
          <div className="hidden md:flex items-center space-x-2 px-3 py-1 bg-muted rounded-md">
            <Icon name="Shield" size={16} color="var(--color-accent)" />
            <span className="text-sm font-medium text-muted-foreground">
              {getRoleDisplayName(userRole)}
            </span>
          </div>

          {/* Profile Dropdown */}
          <div className="relative">
            <Button
              variant="ghost"
              onClick={() => setIsProfileOpen(!isProfileOpen)}
              className="flex items-center space-x-2 px-3 py-2"
            >
              <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <Icon name="User" size={16} color="var(--color-primary-foreground)" />
              </div>
              <span className="hidden md:block text-sm font-medium text-foreground">
                {userName}
              </span>
              <Icon 
                name="ChevronDown" 
                size={16} 
                className={`transition-transform duration-150 ${isProfileOpen ? 'rotate-180' : ''}`}
              />
            </Button>

            {/* Profile Dropdown Menu */}
            {isProfileOpen && (
              <div className="absolute right-0 top-full mt-2 w-56 bg-popover border border-border rounded-md shadow-custom-lg z-1100">
                <div className="p-3 border-b border-border">
                  <p className="text-sm font-medium text-popover-foreground">{userName}</p>
                  <p className="text-xs text-muted-foreground">{getRoleDisplayName(userRole)}</p>
                </div>
                <div className="py-2">
                  <button className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-popover-foreground hover:bg-muted transition-colors duration-150">
                    <Icon name="User" size={16} />
                    <span>Profile</span>
                  </button>
                  <button className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-popover-foreground hover:bg-muted transition-colors duration-150">
                    <Icon name="Settings" size={16} />
                    <span>Settings</span>
                  </button>
                  <button className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-popover-foreground hover:bg-muted transition-colors duration-150">
                    <Icon name="HelpCircle" size={16} />
                    <span>Help</span>
                  </button>
                  <div className="border-t border-border mt-2 pt-2">
                    <button className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-error hover:bg-muted transition-colors duration-150">
                      <Icon name="LogOut" size={16} />
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="lg:hidden p-2"
          >
            <Icon name={isMobileMenuOpen ? "X" : "Menu"} size={20} />
          </Button>
        </div>
      </div>
      {/* Mobile Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-surface border-t border-border shadow-custom-md">
          <nav className="px-4 py-4 space-y-2">
            {filteredNavItems?.map((item) => (
              <Button
                key={item?.path}
                variant={isActivePath(item?.path) ? "default" : "ghost"}
                onClick={() => handleNavigation(item?.path)}
                iconName={item?.icon}
                iconPosition="left"
                iconSize={18}
                fullWidth
                className="justify-start px-4 py-3 text-sm font-medium"
              >
                {item?.label}
              </Button>
            ))}
            
            {/* Mobile Role Indicator */}
            <div className="flex items-center space-x-2 px-4 py-2 mt-4 bg-muted rounded-md">
              <Icon name="Shield" size={16} color="var(--color-accent)" />
              <span className="text-sm font-medium text-muted-foreground">
                {getRoleDisplayName(userRole)}
              </span>
            </div>
          </nav>
        </div>
      )}
      {/* Overlay for mobile menu */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </header>
  );
};

export default Header;