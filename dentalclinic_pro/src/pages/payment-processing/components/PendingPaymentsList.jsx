import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const PendingPaymentsList = ({ onSelectPayment, selectedPaymentId }) => {
  const [sortBy, setSortBy] = useState('date');
  const [sortOrder, setSortOrder] = useState('desc');

  const pendingPayments = [
    {
      id: 'PAY-001',
      patientName: 'María García López',
      patientId: 'P-2024-001',
      serviceDescription: 'Limpieza dental + Fluorización',
      amount: 85.00,
      dueDate: '2024-08-12',
      status: 'pending',
      insuranceCoverage: 60,
      paymentMethod: 'insurance',
      priority: 'normal',
      lastContact: '2024-08-10'
    },
    {
      id: 'PAY-002',
      patientName: 'Carlos Rodríguez Martín',
      patientId: 'P-2024-002',
      serviceDescription: 'Empaste composite posterior',
      amount: 120.00,
      dueDate: '2024-08-15',
      status: 'partial',
      insuranceCoverage: 0,
      paymentMethod: 'card',
      priority: 'high',
      paidAmount: 50.00,
      lastContact: '2024-08-11'
    },
    {
      id: 'PAY-003',
      patientName: 'Ana Fernández Silva',
      patientId: 'P-2024-003',
      serviceDescription: 'Ortodoncia - Cuota mensual',
      amount: 180.00,
      dueDate: '2024-08-08',
      status: 'overdue',
      insuranceCoverage: 0,
      paymentMethod: 'plan',
      priority: 'urgent',
      lastContact: '2024-08-05'
    },
    {
      id: 'PAY-004',
      patientName: 'José Luis Moreno',
      patientId: 'P-2024-004',
      serviceDescription: 'Extracción muela del juicio',
      amount: 95.00,
      dueDate: '2024-08-14',
      status: 'pending',
      insuranceCoverage: 80,
      paymentMethod: 'insurance',
      priority: 'normal',
      lastContact: '2024-08-12'
    },
    {
      id: 'PAY-005',
      patientName: 'Laura Jiménez Ruiz',
      patientId: 'P-2024-005',
      serviceDescription: 'Corona dental cerámica',
      amount: 450.00,
      dueDate: '2024-08-16',
      status: 'pending',
      insuranceCoverage: 40,
      paymentMethod: 'plan',
      priority: 'normal',
      lastContact: '2024-08-11'
    },
    {
      id: 'PAY-006',
      patientName: 'Miguel Ángel Torres',
      patientId: 'P-2024-006',
      serviceDescription: 'Revisión + Radiografía',
      amount: 65.00,
      dueDate: '2024-08-13',
      status: 'completed',
      insuranceCoverage: 100,
      paymentMethod: 'insurance',
      priority: 'normal',
      paidAmount: 65.00,
      lastContact: '2024-08-12'
    }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'text-warning';
      case 'partial': return 'text-accent';
      case 'overdue': return 'text-error';
      case 'completed': return 'text-success';
      default: return 'text-muted-foreground';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'pending': return 'Pendiente';
      case 'partial': return 'Parcial';
      case 'overdue': return 'Vencido';
      case 'completed': return 'Completado';
      default: return status;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-error';
      case 'high': return 'bg-warning';
      case 'normal': return 'bg-muted';
      default: return 'bg-muted';
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    })?.format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString)?.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const sortedPayments = [...pendingPayments]?.sort((a, b) => {
    let aValue, bValue;
    
    switch (sortBy) {
      case 'date':
        aValue = new Date(a.dueDate);
        bValue = new Date(b.dueDate);
        break;
      case 'amount':
        aValue = a?.amount;
        bValue = b?.amount;
        break;
      case 'patient':
        aValue = a?.patientName?.toLowerCase();
        bValue = b?.patientName?.toLowerCase();
        break;
      case 'status':
        aValue = a?.status;
        bValue = b?.status;
        break;
      default:
        return 0;
    }

    if (sortOrder === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  return (
    <div className="bg-surface border border-border rounded-lg h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-foreground">Pagos Pendientes</h2>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-muted-foreground">
              {pendingPayments?.filter(p => p?.status !== 'completed')?.length} pendientes
            </span>
            <Button variant="ghost" iconName="RefreshCw" iconSize={16} />
          </div>
        </div>

        {/* Sort Controls */}
        <div className="flex items-center space-x-2">
          <span className="text-sm text-muted-foreground">Ordenar por:</span>
          <Button
            variant={sortBy === 'date' ? 'default' : 'ghost'}
            onClick={() => handleSort('date')}
            iconName={sortBy === 'date' ? (sortOrder === 'asc' ? 'ArrowUp' : 'ArrowDown') : 'Calendar'}
            iconPosition="left"
            iconSize={14}
            className="text-xs px-2 py-1"
          >
            Fecha
          </Button>
          <Button
            variant={sortBy === 'amount' ? 'default' : 'ghost'}
            onClick={() => handleSort('amount')}
            iconName={sortBy === 'amount' ? (sortOrder === 'asc' ? 'ArrowUp' : 'ArrowDown') : 'Euro'}
            iconPosition="left"
            iconSize={14}
            className="text-xs px-2 py-1"
          >
            Monto
          </Button>
          <Button
            variant={sortBy === 'patient' ? 'default' : 'ghost'}
            onClick={() => handleSort('patient')}
            iconName={sortBy === 'patient' ? (sortOrder === 'asc' ? 'ArrowUp' : 'ArrowDown') : 'User'}
            iconPosition="left"
            iconSize={14}
            className="text-xs px-2 py-1"
          >
            Paciente
          </Button>
        </div>
      </div>
      {/* Payments List */}
      <div className="flex-1 overflow-y-auto">
        <div className="space-y-2 p-4">
          {sortedPayments?.map((payment) => (
            <div
              key={payment?.id}
              onClick={() => onSelectPayment(payment)}
              className={`p-4 border border-border rounded-lg cursor-pointer transition-all duration-150 hover:bg-muted/50 ${
                selectedPaymentId === payment?.id ? 'bg-primary/10 border-primary' : ''
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <h3 className="font-medium text-foreground">{payment?.patientName}</h3>
                    <div className={`w-2 h-2 rounded-full ${getPriorityColor(payment?.priority)}`} />
                  </div>
                  <p className="text-sm text-muted-foreground mb-1">{payment?.patientId}</p>
                  <p className="text-sm text-foreground">{payment?.serviceDescription}</p>
                </div>
                <div className="text-right">
                  <div className="text-lg font-semibold text-foreground">
                    {formatCurrency(payment?.amount)}
                  </div>
                  {payment?.paidAmount && (
                    <div className="text-sm text-success">
                      Pagado: {formatCurrency(payment?.paidAmount)}
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <span className={`text-sm font-medium ${getStatusColor(payment?.status)}`}>
                    {getStatusText(payment?.status)}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    Vence: {formatDate(payment?.dueDate)}
                  </span>
                  {payment?.insuranceCoverage > 0 && (
                    <div className="flex items-center space-x-1">
                      <Icon name="Shield" size={14} color="var(--color-accent)" />
                      <span className="text-sm text-accent">{payment?.insuranceCoverage}%</span>
                    </div>
                  )}
                </div>
                <div className="flex items-center space-x-2">
                  {payment?.paymentMethod === 'plan' && (
                    <Icon name="Calendar" size={14} color="var(--color-secondary)" />
                  )}
                  {payment?.paymentMethod === 'insurance' && (
                    <Icon name="Shield" size={14} color="var(--color-accent)" />
                  )}
                  {payment?.paymentMethod === 'card' && (
                    <Icon name="CreditCard" size={14} color="var(--color-primary)" />
                  )}
                  <Icon name="ChevronRight" size={14} color="var(--color-muted-foreground)" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      {/* Summary Footer */}
      <div className="p-4 border-t border-border bg-muted/30">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Total pendiente:</span>
            <div className="font-semibold text-foreground">
              {formatCurrency(
                pendingPayments?.filter(p => p?.status !== 'completed')?.reduce((sum, p) => sum + (p?.amount - (p?.paidAmount || 0)), 0)
              )}
            </div>
          </div>
          <div>
            <span className="text-muted-foreground">Vencidos:</span>
            <div className="font-semibold text-error">
              {pendingPayments?.filter(p => p?.status === 'overdue')?.length}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PendingPaymentsList;