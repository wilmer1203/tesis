import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';

const ReportCategoryTabs = ({ activeTab, onTabChange, className = '' }) => {
  const tabs = [
    {
      id: 'financial',
      label: 'Financiero',
      icon: 'DollarSign',
      description: 'Ingresos, pagos y análisis de rentabilidad'
    },
    {
      id: 'performance',
      label: 'Rendimiento',
      icon: 'TrendingUp',
      description: 'Métricas de dentistas y productividad'
    },
    {
      id: 'patients',
      label: 'Pacientes',
      icon: 'Users',
      description: 'Análisis de pacientes y satisfacción'
    },
    {
      id: 'operations',
      label: 'Operaciones',
      icon: 'Activity',
      description: 'Colas, tiempos de espera y eficiencia'
    }
  ];

  return (
    <div className={`bg-card border border-border rounded-lg p-1 ${className}`}>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-1">
        {tabs?.map((tab) => (
          <button
            key={tab?.id}
            onClick={() => onTabChange(tab?.id)}
            className={`flex flex-col items-center space-y-2 p-4 rounded-md transition-smooth text-center ${
              activeTab === tab?.id
                ? 'bg-primary text-primary-foreground shadow-soft'
                : 'text-muted-foreground hover:text-foreground hover:bg-muted'
            }`}
          >
            <Icon name={tab?.icon} size={24} />
            <div>
              <div className="font-medium text-sm">{tab?.label}</div>
              <div className={`text-xs mt-1 ${
                activeTab === tab?.id ? 'text-primary-foreground/80' : 'text-muted-foreground'
              }`}>
                {tab?.description}
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default ReportCategoryTabs;