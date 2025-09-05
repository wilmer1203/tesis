import React from 'react';
import Icon from '../../../components/AppIcon';

const PaymentStats = () => {
  const stats = [
    {
      id: 'daily_revenue',
      title: 'Ingresos Hoy',
      value: '1.245,50',
      currency: '€',
      change: '+12.5%',
      changeType: 'positive',
      icon: 'TrendingUp',
      description: '8 pagos procesados'
    },
    {
      id: 'pending_payments',
      title: 'Pagos Pendientes',
      value: '3.890,00',
      currency: '€',
      change: '-5.2%',
      changeType: 'negative',
      icon: 'Clock',
      description: '15 pagos por cobrar'
    },
    {
      id: 'monthly_target',
      title: 'Meta Mensual',
      value: '78%',
      currency: '',
      change: '+3.1%',
      changeType: 'positive',
      icon: 'Target',
      description: '22.450€ de 28.750€'
    },
    {
      id: 'insurance_claims',
      title: 'Seguros Pendientes',
      value: '2.150,00',
      currency: '€',
      change: '0%',
      changeType: 'neutral',
      icon: 'Shield',
      description: '6 reclamaciones'
    }
  ];

  const getChangeColor = (type) => {
    switch (type) {
      case 'positive': return 'text-success';
      case 'negative': return 'text-error';
      case 'neutral': return 'text-muted-foreground';
      default: return 'text-muted-foreground';
    }
  };

  const getChangeIcon = (type) => {
    switch (type) {
      case 'positive': return 'ArrowUp';
      case 'negative': return 'ArrowDown';
      case 'neutral': return 'Minus';
      default: return 'Minus';
    }
  };

  const formatValue = (value, currency) => {
    if (currency === '€') {
      return `${value}${currency}`;
    } else if (currency === '') {
      return value;
    }
    return `${currency}${value}`;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      {stats?.map((stat) => (
        <div
          key={stat?.id}
          className="bg-surface border border-border rounded-lg p-6 hover:shadow-custom-md transition-shadow duration-150"
        >
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Icon 
                  name={stat?.icon} 
                  size={24} 
                  color="var(--color-primary)" 
                />
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  {stat?.title}
                </h3>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="text-2xl font-bold text-foreground">
              {formatValue(stat?.value, stat?.currency)}
            </div>

            <div className="flex items-center justify-between">
              <div className={`flex items-center space-x-1 text-sm ${getChangeColor(stat?.changeType)}`}>
                <Icon 
                  name={getChangeIcon(stat?.changeType)} 
                  size={14} 
                />
                <span className="font-medium">{stat?.change}</span>
              </div>
            </div>

            <p className="text-xs text-muted-foreground">
              {stat?.description}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PaymentStats;