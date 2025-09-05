import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const DateRangeSelector = ({ dateRange, onDateRangeChange, className = '' }) => {
  const [showCustomRange, setShowCustomRange] = useState(false);
  const [customStart, setCustomStart] = useState('');
  const [customEnd, setCustomEnd] = useState('');

  const presetRanges = [
    { id: 'today', label: 'Hoy', days: 0 },
    { id: 'yesterday', label: 'Ayer', days: 1 },
    { id: 'week', label: 'Esta Semana', days: 7 },
    { id: 'month', label: 'Este Mes', days: 30 },
    { id: 'quarter', label: 'Trimestre', days: 90 },
    { id: 'year', label: 'Este Año', days: 365 }
  ];

  const handlePresetSelect = (preset) => {
    const endDate = new Date();
    const startDate = new Date();
    
    if (preset?.id === 'today') {
      startDate?.setHours(0, 0, 0, 0);
      endDate?.setHours(23, 59, 59, 999);
    } else if (preset?.id === 'yesterday') {
      startDate?.setDate(startDate?.getDate() - 1);
      startDate?.setHours(0, 0, 0, 0);
      endDate?.setDate(endDate?.getDate() - 1);
      endDate?.setHours(23, 59, 59, 999);
    } else {
      startDate?.setDate(startDate?.getDate() - preset?.days);
      startDate?.setHours(0, 0, 0, 0);
      endDate?.setHours(23, 59, 59, 999);
    }

    onDateRangeChange({
      start: startDate,
      end: endDate,
      preset: preset?.id
    });
    setShowCustomRange(false);
  };

  const handleCustomRangeApply = () => {
    if (customStart && customEnd) {
      const startDate = new Date(customStart);
      const endDate = new Date(customEnd);
      endDate?.setHours(23, 59, 59, 999);
      
      onDateRangeChange({
        start: startDate,
        end: endDate,
        preset: 'custom'
      });
      setShowCustomRange(false);
    }
  };

  const formatDateRange = () => {
    if (!dateRange?.start || !dateRange?.end) return 'Seleccionar período';
    
    const start = dateRange?.start?.toLocaleDateString('es-VE', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric' 
    });
    const end = dateRange?.end?.toLocaleDateString('es-VE', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric' 
    });
    
    if (start === end) return start;
    return `${start} - ${end}`;
  };

  return (
    <div className={`relative ${className}`}>
      <div className="flex flex-wrap items-center gap-2">
        {/* Preset Buttons */}
        <div className="flex flex-wrap gap-1">
          {presetRanges?.map((preset) => (
            <button
              key={preset?.id}
              onClick={() => handlePresetSelect(preset)}
              className={`px-3 py-1.5 text-sm rounded-md transition-smooth ${
                dateRange?.preset === preset?.id
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted text-muted-foreground hover:text-foreground hover:bg-muted/80'
              }`}
            >
              {preset?.label}
            </button>
          ))}
        </div>

        {/* Custom Range Toggle */}
        <button
          onClick={() => setShowCustomRange(!showCustomRange)}
          className={`flex items-center space-x-2 px-3 py-1.5 text-sm rounded-md border transition-smooth ${
            showCustomRange || dateRange?.preset === 'custom' ?'bg-primary text-primary-foreground border-primary' :'bg-card text-foreground border-border hover:bg-muted'
          }`}
        >
          <Icon name="Calendar" size={16} />
          <span>{formatDateRange()}</span>
          <Icon name={showCustomRange ? "ChevronUp" : "ChevronDown"} size={14} />
        </button>
      </div>
      {/* Custom Range Picker */}
      {showCustomRange && (
        <div className="absolute top-full left-0 mt-2 bg-popover border border-border rounded-md shadow-modal p-4 z-20 min-w-80">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-foreground">Período Personalizado</h3>
              <button
                onClick={() => setShowCustomRange(false)}
                className="p-1 hover:bg-muted rounded transition-smooth"
              >
                <Icon name="X" size={16} className="text-muted-foreground" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">
                  Fecha Inicio
                </label>
                <input
                  type="date"
                  value={customStart}
                  onChange={(e) => setCustomStart(e?.target?.value)}
                  className="w-full px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">
                  Fecha Fin
                </label>
                <input
                  type="date"
                  value={customEnd}
                  onChange={(e) => setCustomEnd(e?.target?.value)}
                  className="w-full px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowCustomRange(false)}
              >
                Cancelar
              </Button>
              <Button
                variant="default"
                size="sm"
                onClick={handleCustomRangeApply}
                disabled={!customStart || !customEnd}
              >
                Aplicar
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DateRangeSelector;