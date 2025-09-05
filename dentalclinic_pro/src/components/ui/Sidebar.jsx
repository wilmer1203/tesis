import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Icon from '../AppIcon';
import Button from './Button';

const Sidebar = ({ 
  userRole = 'manager', 
  isCollapsed = false, 
  onToggleCollapse = () => {},
  className = '' 
}) => {
  const [expandedSections, setExpandedSections] = useState({
    dashboard: true,
    clinical: true,
    administrative: true
  });
  const location = useLocation();

  const navigationSections = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: 'LayoutDashboard',
      items: [
        {
          label: 'Manager Overview',
          path: '/manager-dashboard',
          icon: 'BarChart3',
          roles: ['manager']
        },
        {
          label: 'Secretary Hub',
          path: '/secretary-dashboard',
          icon: 'Calendar',
          roles: ['secretary']
        },
        {
          label: 'Clinical Dashboard',
          path: '/dentist-dashboard',
          icon: 'Stethoscope',
          roles: ['dentist']
        }
      ]
    },
    {
      id: 'clinical',
      label: 'Clinical Operations',
      icon: 'Activity',
      items: [
        {
          label: 'Patient Management',
          path: '/patient-management',
          icon: 'Users',
          roles: ['manager', 'secretary', 'dentist'],
          description: 'Patient records and medical history'
        },
        {
          label: 'Appointment Scheduling',
          path: '/appointment-scheduling',
          icon: 'Calendar',
          roles: ['manager', 'secretary', 'dentist'],
          description: 'Schedule and manage appointments'
        }
      ]
    },
    {
      id: 'administrative',
      label: 'Administrative',
      icon: 'FileText',
      items: [
        {
          label: 'Payment Processing',
          path: '/payment-processing',
          icon: 'CreditCard',
          roles: ['manager', 'secretary'],
          description: 'Billing and payment management'
        }
      ]
    }
  ];

  const isActivePath = (path) => {
    return location?.pathname === path;
  };

  const toggleSection = (sectionId) => {
    if (!isCollapsed) {
      setExpandedSections(prev => ({
        ...prev,
        [sectionId]: !prev?.[sectionId]
      }));
    }
  };

  const handleNavigation = (path) => {
    window.location.href = path;
  };

  const getFilteredSections = () => {
    return navigationSections?.map(section => ({
      ...section,
      items: section?.items?.filter(item => item?.roles?.includes(userRole))
    }))?.filter(section => section?.items?.length > 0);
  };

  const filteredSections = getFilteredSections();

  return (
    <aside 
      className={`fixed left-0 top-16 bottom-0 z-1000 bg-surface border-r border-border transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-64'
      } ${className}`}
    >
      <div className="flex flex-col h-full">
        {/* Collapse Toggle */}
        <div className="flex items-center justify-between p-4 border-b border-border">
          {!isCollapsed && (
            <h2 className="text-sm font-semibold text-foreground font-heading">
              Navigation
            </h2>
          )}
          <Button
            variant="ghost"
            onClick={onToggleCollapse}
            className="p-2 hover:bg-muted"
          >
            <Icon 
              name={isCollapsed ? "ChevronRight" : "ChevronLeft"} 
              size={16} 
            />
          </Button>
        </div>

        {/* Navigation Content */}
        <nav className="flex-1 overflow-y-auto py-4">
          <div className="space-y-6">
            {filteredSections?.map((section) => (
              <div key={section?.id} className="px-3">
                {/* Section Header */}
                <button
                  onClick={() => toggleSection(section?.id)}
                  className={`w-full flex items-center justify-between p-2 rounded-md hover:bg-muted transition-colors duration-150 ${
                    isCollapsed ? 'justify-center' : ''
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon 
                      name={section?.icon} 
                      size={18} 
                      color="var(--color-muted-foreground)" 
                    />
                    {!isCollapsed && (
                      <span className="text-sm font-medium text-muted-foreground font-heading">
                        {section?.label}
                      </span>
                    )}
                  </div>
                  {!isCollapsed && (
                    <Icon 
                      name="ChevronDown" 
                      size={14} 
                      className={`transition-transform duration-150 ${
                        expandedSections?.[section?.id] ? 'rotate-180' : ''
                      }`}
                      color="var(--color-muted-foreground)"
                    />
                  )}
                </button>

                {/* Section Items */}
                {(expandedSections?.[section?.id] || isCollapsed) && (
                  <div className={`mt-2 space-y-1 ${isCollapsed ? '' : 'ml-4'}`}>
                    {section?.items?.map((item) => (
                      <div key={item?.path} className="relative group">
                        <Button
                          variant={isActivePath(item?.path) ? "default" : "ghost"}
                          onClick={() => handleNavigation(item?.path)}
                          className={`w-full justify-start p-3 text-sm font-medium transition-all duration-150 ${
                            isCollapsed ? 'px-2' : ''
                          }`}
                        >
                          <div className="flex items-center space-x-3">
                            <Icon 
                              name={item?.icon} 
                              size={16} 
                              color={isActivePath(item?.path) ? "var(--color-primary-foreground)" : "currentColor"}
                            />
                            {!isCollapsed && (
                              <span className="truncate">{item?.label}</span>
                            )}
                          </div>
                        </Button>

                        {/* Tooltip for collapsed state */}
                        {isCollapsed && (
                          <div className="absolute left-full top-0 ml-2 px-3 py-2 bg-popover border border-border rounded-md shadow-custom-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-150 z-1100 whitespace-nowrap">
                            <div className="text-sm font-medium text-popover-foreground">
                              {item?.label}
                            </div>
                            {item?.description && (
                              <div className="text-xs text-muted-foreground mt-1">
                                {item?.description}
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </nav>

        {/* User Role Indicator */}
        <div className="p-4 border-t border-border">
          <div className={`flex items-center space-x-3 p-3 bg-muted rounded-md ${
            isCollapsed ? 'justify-center' : ''
          }`}>
            <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
              <Icon name="Shield" size={16} color="var(--color-primary-foreground)" />
            </div>
            {!isCollapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground truncate">
                  {userRole === 'manager' ? 'Practice Manager' : 
                   userRole === 'secretary' ? 'Secretary' : 'Dentist'}
                </p>
                <p className="text-xs text-muted-foreground">
                  Active Role
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;