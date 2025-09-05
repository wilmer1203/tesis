import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const QuickActions = ({ onActionSelect }) => {
  const [isScanning, setIsScanning] = useState(false);

  const quickActions = [
    {
      id: 'new_payment',
      title: 'Nuevo Pago',
      description: 'Registrar pago manual',
      icon: 'Plus',
      color: 'primary',
      action: () => onActionSelect('new_payment')
    },
    {
      id: 'scan_barcode',
      title: 'Escanear Código',
      description: 'Código de servicio',
      icon: 'Scan',
      color: 'secondary',
      action: () => handleBarcodeScan()
    },
    {
      id: 'insurance_claim',
      title: 'Reclamación Seguro',
      description: 'Procesar seguro médico',
      icon: 'Shield',
      color: 'accent',
      action: () => onActionSelect('insurance_claim')
    },
    {
      id: 'payment_plan',
      title: 'Plan de Pagos',
      description: 'Configurar cuotas',
      icon: 'Calendar',
      color: 'warning',
      action: () => onActionSelect('payment_plan')
    },
    {
      id: 'generate_invoice',
      title: 'Generar Factura',
      description: 'Crear nueva factura',
      icon: 'FileText',
      color: 'success',
      action: () => onActionSelect('generate_invoice')
    },
    {
      id: 'daily_report',
      title: 'Reporte Diario',
      description: 'Resumen de ingresos',
      icon: 'BarChart3',
      color: 'muted',
      action: () => onActionSelect('daily_report')
    }
  ];

  const handleBarcodeScan = () => {
    setIsScanning(true);
    // Simulate barcode scanning
    setTimeout(() => {
      setIsScanning(false);
      onActionSelect('scan_barcode');
    }, 2000);
  };

  const getColorClasses = (color) => {
    switch (color) {
      case 'primary':
        return 'bg-primary/10 text-primary border-primary/20 hover:bg-primary/20';
      case 'secondary':
        return 'bg-secondary/10 text-secondary border-secondary/20 hover:bg-secondary/20';
      case 'accent':
        return 'bg-accent/10 text-accent border-accent/20 hover:bg-accent/20';
      case 'warning':
        return 'bg-warning/10 text-warning border-warning/20 hover:bg-warning/20';
      case 'success':
        return 'bg-success/10 text-success border-success/20 hover:bg-success/20';
      case 'muted':
        return 'bg-muted/50 text-muted-foreground border-muted hover:bg-muted';
      default:
        return 'bg-surface text-foreground border-border hover:bg-muted/50';
    }
  };

  return (
    <div className="bg-surface border border-border rounded-lg p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-foreground">Acciones Rápidas</h2>
        <Button variant="ghost" iconName="Settings" iconSize={16} />
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {quickActions?.map((action) => (
          <button
            key={action?.id}
            onClick={action?.action}
            disabled={action?.id === 'scan_barcode' && isScanning}
            className={`p-4 border rounded-lg transition-all duration-150 text-left ${getColorClasses(action?.color)}`}
          >
            <div className="flex flex-col items-center space-y-3">
              <div className="w-12 h-12 rounded-lg flex items-center justify-center bg-current/10">
                {action?.id === 'scan_barcode' && isScanning ? (
                  <div className="animate-spin">
                    <Icon name="Loader2" size={24} />
                  </div>
                ) : (
                  <Icon name={action?.icon} size={24} />
                )}
              </div>
              
              <div className="text-center">
                <h3 className="text-sm font-medium mb-1">
                  {action?.title}
                </h3>
                <p className="text-xs opacity-80">
                  {action?.description}
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>
      {/* Recent Actions */}
      <div className="mt-6 pt-6 border-t border-border">
        <h3 className="text-sm font-medium text-foreground mb-3">Acciones Recientes</h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center space-x-2">
              <Icon name="CreditCard" size={14} color="var(--color-success)" />
              <span className="text-foreground">Pago procesado - María García</span>
            </div>
            <span className="text-muted-foreground">Hace 5 min</span>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center space-x-2">
              <Icon name="FileText" size={14} color="var(--color-primary)" />
              <span className="text-foreground">Factura generada - Carlos Rodríguez</span>
            </div>
            <span className="text-muted-foreground">Hace 12 min</span>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center space-x-2">
              <Icon name="Shield" size={14} color="var(--color-accent)" />
              <span className="text-foreground">Reclamación enviada - Ana Fernández</span>
            </div>
            <span className="text-muted-foreground">Hace 25 min</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuickActions;