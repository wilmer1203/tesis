import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const FinancialReports = ({ dateRange, className = '' }) => {
  const [selectedMetric, setSelectedMetric] = useState('revenue');
  const [showExchangeHistory, setShowExchangeHistory] = useState(false);

  // Mock financial data
  const revenueData = [
    { date: '01/09', bs: 2850000, usd: 780, total_bs: 3135000 },
    { date: '02/09', bs: 3200000, usd: 920, total_bs: 3535200 },
    { date: '03/09', bs: 2950000, usd: 850, total_bs: 3259500 },
    { date: '04/09', bs: 3450000, usd: 1100, total_bs: 3851000 }
  ];

  const paymentMethodData = [
    { method: 'Efectivo BS', amount: 8450000, percentage: 45, color: '#2563EB' },
    { method: 'Transferencia BS', amount: 5200000, percentage: 28, color: '#059669' },
    { method: 'Efectivo USD', amount: 3650, percentage: 20, color: '#F59E0B' },
    { method: 'Tarjeta USD', amount: 1200, percentage: 7, color: '#EF4444' }
  ];

  const dentistPerformance = [
    { name: 'Dr. María González', revenue_bs: 4200000, revenue_usd: 1150, patients: 28, avg_treatment: 150000 },
    { name: 'Dr. Carlos Mendoza', revenue_bs: 3800000, revenue_usd: 980, patients: 24, avg_treatment: 158333 },
    { name: 'Dr. Ana Rodríguez', revenue_bs: 3200000, revenue_usd: 850, patients: 22, avg_treatment: 145454 },
    { name: 'Dr. Luis Herrera', revenue_bs: 2950000, revenue_usd: 720, patients: 19, avg_treatment: 155263 }
  ];

  const exchangeRateHistory = [
    { date: '01/09', rate: 36.20 },
    { date: '02/09', rate: 36.45 },
    { date: '03/09', rate: 36.38 },
    { date: '04/09', rate: 36.52 }
  ];

  const summaryCards = [
    {
      title: 'Ingresos Totales (BS)',
      value: '18.650.000',
      change: '+12.5%',
      trend: 'up',
      icon: 'TrendingUp',
      color: 'text-success'
    },
    {
      title: 'Ingresos Totales (USD)',
      value: '$4.850',
      change: '+8.3%',
      trend: 'up',
      icon: 'DollarSign',
      color: 'text-success'
    },
    {
      title: 'Margen de Ganancia',
      value: '68.5%',
      change: '+2.1%',
      trend: 'up',
      icon: 'Percent',
      color: 'text-success'
    },
    {
      title: 'Tasa Promedio',
      value: '36.39 Bs',
      change: '+0.32',
      trend: 'up',
      icon: 'ArrowUpDown',
      color: 'text-warning'
    }
  ];

  const formatCurrency = (value, currency = 'BS') => {
    if (currency === 'USD') {
      return `$${value?.toLocaleString('es-VE', { minimumFractionDigits: 2 })}`;
    }
    return `${value?.toLocaleString('es-VE')} Bs`;
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload?.length) {
      return (
        <div className="bg-popover border border-border rounded-md shadow-modal p-3">
          <p className="text-sm font-medium text-foreground mb-2">{label}</p>
          {payload?.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry?.color }}>
              {entry?.name}: {entry?.name?.includes('USD') ? formatCurrency(entry?.value, 'USD') : formatCurrency(entry?.value)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryCards?.map((card, index) => (
          <div key={index} className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Icon name={card?.icon} size={20} className="text-primary" />
              <div className={`flex items-center space-x-1 text-xs ${card?.color}`}>
                <Icon name={card?.trend === 'up' ? 'ArrowUp' : 'ArrowDown'} size={12} />
                <span>{card?.change}</span>
              </div>
            </div>
            <div className="text-2xl font-bold text-foreground mb-1">{card?.value}</div>
            <div className="text-sm text-muted-foreground">{card?.title}</div>
          </div>
        ))}
      </div>
      {/* Revenue Chart */}
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <h3 className="text-lg font-semibold text-foreground">Ingresos por Día</h3>
          <div className="flex items-center space-x-2 mt-2 sm:mt-0">
            <Button
              variant={selectedMetric === 'revenue' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedMetric('revenue')}
            >
              Ingresos
            </Button>
            <Button
              variant={selectedMetric === 'comparison' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedMetric('comparison')}
            >
              Comparación
            </Button>
          </div>
        </div>

        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis 
                dataKey="date" 
                stroke="var(--color-muted-foreground)"
                fontSize={12}
              />
              <YAxis 
                stroke="var(--color-muted-foreground)"
                fontSize={12}
                tickFormatter={(value) => `${(value / 1000000)?.toFixed(1)}M`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Bar 
                dataKey="bs" 
                name="Bolívares" 
                fill="var(--color-primary)" 
                radius={[2, 2, 0, 0]}
              />
              <Bar 
                dataKey="total_bs" 
                name="Total (BS equivalente)" 
                fill="var(--color-accent)" 
                radius={[2, 2, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Payment Methods */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-6">Métodos de Pago</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={paymentMethodData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="percentage"
                >
                  {paymentMethodData?.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry?.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value) => [`${value}%`, 'Porcentaje']}
                  labelFormatter={(label) => `Método: ${label}`}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-4">
            {paymentMethodData?.map((method, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div 
                  className="w-3 h-3 rounded-full" 
                  style={{ backgroundColor: method?.color }}
                ></div>
                <span className="text-sm text-muted-foreground">{method?.method}</span>
                <span className="text-sm font-medium text-foreground ml-auto">
                  {method?.percentage}%
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Exchange Rate History */}
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-foreground">Historial de Tasa</h3>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowExchangeHistory(!showExchangeHistory)}
              iconName={showExchangeHistory ? "ChevronUp" : "ChevronDown"}
            >
              {showExchangeHistory ? 'Ocultar' : 'Ver Detalles'}
            </Button>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={exchangeRateHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis 
                  dataKey="date" 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="var(--color-muted-foreground)"
                  fontSize={12}
                  domain={['dataMin - 0.1', 'dataMax + 0.1']}
                />
                <Tooltip 
                  formatter={(value) => [`${value?.toFixed(2)} Bs`, 'Tasa']}
                  labelFormatter={(label) => `Fecha: ${label}`}
                />
                <Line 
                  type="monotone" 
                  dataKey="rate" 
                  stroke="var(--color-warning)" 
                  strokeWidth={3}
                  dot={{ fill: 'var(--color-warning)', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {showExchangeHistory && (
            <div className="mt-4 space-y-2">
              {exchangeRateHistory?.map((entry, index) => (
                <div key={index} className="flex justify-between items-center py-2 border-b border-border last:border-b-0">
                  <span className="text-sm text-muted-foreground">{entry?.date}</span>
                  <span className="text-sm font-medium text-foreground">{entry?.rate?.toFixed(2)} Bs</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      {/* Dentist Performance Table */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-6">Rendimiento por Dentista</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Dentista</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Ingresos (BS)</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Ingresos (USD)</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Pacientes</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Promedio/Tratamiento</th>
              </tr>
            </thead>
            <tbody>
              {dentistPerformance?.map((dentist, index) => (
                <tr key={index} className="border-b border-border last:border-b-0 hover:bg-muted/50">
                  <td className="py-3 px-4">
                    <div className="font-medium text-foreground">{dentist?.name}</div>
                  </td>
                  <td className="py-3 px-4 text-right font-medium text-foreground">
                    {formatCurrency(dentist?.revenue_bs)}
                  </td>
                  <td className="py-3 px-4 text-right font-medium text-foreground">
                    {formatCurrency(dentist?.revenue_usd, 'USD')}
                  </td>
                  <td className="py-3 px-4 text-right text-foreground">{dentist?.patients}</td>
                  <td className="py-3 px-4 text-right text-foreground">
                    {formatCurrency(dentist?.avg_treatment)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default FinancialReports;