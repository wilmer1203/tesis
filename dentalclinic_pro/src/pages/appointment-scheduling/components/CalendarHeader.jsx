import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const CalendarHeader = ({ 
  currentDate, 
  onDateChange, 
  viewMode, 
  onViewModeChange, 
  selectedDentist, 
  onDentistChange,
  dentists 
}) => {
  const formatDate = (date) => {
    return date?.toLocaleDateString('es-ES', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const navigateDate = (direction) => {
    const newDate = new Date(currentDate);
    if (viewMode === 'day') {
      newDate?.setDate(newDate?.getDate() + direction);
    } else if (viewMode === 'week') {
      newDate?.setDate(newDate?.getDate() + (direction * 7));
    } else {
      newDate?.setMonth(newDate?.getMonth() + direction);
    }
    onDateChange(newDate);
  };

  const goToToday = () => {
    onDateChange(new Date());
  };

  return (
    <div className="bg-surface border-b border-border p-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-heading font-bold text-foreground">
            Programación de Citas
          </h1>
          <div className="flex items-center space-x-2 px-3 py-1 bg-muted rounded-md">
            <Icon name="Calendar" size={16} color="var(--color-accent)" />
            <span className="text-sm font-medium text-muted-foreground">
              {formatDate(currentDate)}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            onClick={goToToday}
            iconName="Home"
            iconPosition="left"
            iconSize={16}
            className="text-sm"
          >
            Hoy
          </Button>
          
          <Button
            variant="default"
            iconName="Plus"
            iconPosition="left"
            iconSize={16}
            className="text-sm"
          >
            Nueva Cita
          </Button>
        </div>
      </div>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {/* Date Navigation */}
          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              onClick={() => navigateDate(-1)}
              iconName="ChevronLeft"
              iconSize={16}
              className="p-2"
            />
            <Button
              variant="ghost"
              onClick={() => navigateDate(1)}
              iconName="ChevronRight"
              iconSize={16}
              className="p-2"
            />
          </div>

          {/* View Mode Toggle */}
          <div className="flex items-center bg-muted rounded-md p-1">
            {['day', 'week', 'month']?.map((mode) => (
              <Button
                key={mode}
                variant={viewMode === mode ? "default" : "ghost"}
                onClick={() => onViewModeChange(mode)}
                className="px-3 py-1 text-sm capitalize"
              >
                {mode === 'day' ? 'Día' : mode === 'week' ? 'Semana' : 'Mes'}
              </Button>
            ))}
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Dentist Filter */}
          <div className="flex items-center space-x-2">
            <Icon name="UserCheck" size={16} color="var(--color-muted-foreground)" />
            <select
              value={selectedDentist}
              onChange={(e) => onDentistChange(e?.target?.value)}
              className="bg-input border border-border rounded-md px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="all">Todos los Dentistas</option>
              {dentists?.map((dentist) => (
                <option key={dentist?.id} value={dentist?.id}>
                  {dentist?.name}
                </option>
              ))}
            </select>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              iconName="Clock"
              iconPosition="left"
              iconSize={16}
              className="text-sm"
            >
              Bloquear Horario
            </Button>
            
            <Button
              variant="outline"
              iconName="Bell"
              iconPosition="left"
              iconSize={16}
              className="text-sm"
            >
              Recordatorios
            </Button>
            
            <Button
              variant="outline"
              iconName="Printer"
              iconPosition="left"
              iconSize={16}
              className="text-sm"
            >
              Imprimir
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CalendarHeader;