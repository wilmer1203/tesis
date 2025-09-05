import React from 'react';
import Button from '../../../components/ui/Button';

const QuickActions = () => {
  const quickActions = [
    {
      id: 1,
      title: "Gestión de Personal",
      description: "Administrar empleados y roles",
      icon: "Users",
      variant: "default",
      action: () => console.log("Gestión de personal")
    },
    {
      id: 2,
      title: "Configuración del Sistema",
      description: "Ajustes y preferencias",
      icon: "Settings",
      variant: "outline",
      action: () => console.log("Configuración")
    },
    {
      id: 3,
      title: "Informes Financieros",
      description: "Reportes de ingresos y gastos",
      icon: "FileText",
      variant: "secondary",
      action: () => console.log("Informes financieros")
    },
    {
      id: 4,
      title: "Respaldo del Sistema",
      description: "Crear copia de seguridad",
      icon: "Database",
      variant: "outline",
      action: () => console.log("Respaldo")
    },
    {
      id: 5,
      title: "Análisis de Rendimiento",
      description: "Métricas y estadísticas",
      icon: "BarChart3",
      variant: "ghost",
      action: () => console.log("Análisis")
    },
    {
      id: 6,
      title: "Gestión de Inventario",
      description: "Control de suministros médicos",
      icon: "Package",
      variant: "outline",
      action: () => console.log("Inventario")
    }
  ];

  return (
    <div className="bg-surface border border-border rounded-lg p-6 shadow-custom-md">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-foreground">Acciones Rápidas</h2>
        <Button variant="ghost" iconName="MoreHorizontal" iconSize={16} />
      </div>
      <div className="space-y-3">
        {quickActions?.map((action) => (
          <div
            key={action?.id}
            className="flex items-center justify-between p-3 rounded-md hover:bg-muted transition-colors duration-150 cursor-pointer"
            onClick={action?.action}
          >
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                <Button
                  variant="ghost"
                  iconName={action?.icon}
                  iconSize={18}
                  className="p-0 h-auto w-auto hover:bg-transparent"
                />
              </div>
              <div>
                <h3 className="text-sm font-medium text-foreground">{action?.title}</h3>
                <p className="text-xs text-muted-foreground">{action?.description}</p>
              </div>
            </div>
            <Button
              variant={action?.variant}
              iconName="ChevronRight"
              iconSize={16}
              className="p-2"
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default QuickActions;