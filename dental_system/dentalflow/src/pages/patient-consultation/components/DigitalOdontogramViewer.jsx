import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const DigitalOdontogramViewer = ({ interventions = [], onToothClick }) => {
  const [selectedTooth, setSelectedTooth] = useState(null);
  const [odontogramData, setOdontogramData] = useState({});
  const [viewMode, setViewMode] = useState('current'); // current, history, comparison
  const [hoveredTooth, setHoveredTooth] = useState(null);

  // FDI tooth numbering system
  const adultTeeth = {
    upperRight: [18, 17, 16, 15, 14, 13, 12, 11],
    upperLeft: [21, 22, 23, 24, 25, 26, 27, 28],
    lowerLeft: [31, 32, 33, 34, 35, 36, 37, 38],
    lowerRight: [48, 47, 46, 45, 44, 43, 42, 41]
  };

  // Mock odontogram data with conditions
  const mockOdontogramData = {
    11: { condition: 'healthy', treatments: ['cleaning'], lastUpdate: '2024-09-04' },
    12: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    13: { condition: 'cavity', treatments: [], lastUpdate: '2024-09-04' },
    14: { condition: 'filled', treatments: ['filling'], lastUpdate: '2024-07-20' },
    15: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    16: { condition: 'filled', treatments: ['filling', 'cleaning'], lastUpdate: '2024-09-04' },
    17: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    18: { condition: 'missing', treatments: ['extraction'], lastUpdate: '2024-06-10' },
    21: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    22: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    23: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    24: { condition: 'cavity', treatments: [], lastUpdate: '2024-09-04' },
    25: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    26: { condition: 'crown', treatments: ['crown'], lastUpdate: '2024-05-15' },
    27: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    28: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    31: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    32: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    33: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    34: { condition: 'filled', treatments: ['filling'], lastUpdate: '2024-03-20' },
    35: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    36: { condition: 'root_canal', treatments: ['root_canal'], lastUpdate: '2024-04-10' },
    37: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    38: { condition: 'impacted', treatments: [], lastUpdate: '2024-08-15' },
    41: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    42: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    43: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    44: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    45: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    46: { condition: 'filled', treatments: ['filling'], lastUpdate: '2024-02-28' },
    47: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' },
    48: { condition: 'healthy', treatments: [], lastUpdate: '2024-08-15' }
  };

  useEffect(() => {
    setOdontogramData(mockOdontogramData);
  }, []);

  const getToothColor = (toothNumber) => {
    const tooth = odontogramData?.[toothNumber];
    if (!tooth) return '#E2E8F0'; // Default gray

    switch (tooth?.condition) {
      case 'healthy':
        return '#10B981'; // Green
      case 'cavity':
        return '#EF4444'; // Red
      case 'filled':
        return '#3B82F6'; // Blue
      case 'crown':
        return '#8B5CF6'; // Purple
      case 'root_canal':
        return '#F59E0B'; // Amber
      case 'missing':
        return '#6B7280'; // Gray
      case 'impacted':
        return '#EC4899'; // Pink
      default:
        return '#E2E8F0';
    }
  };

  const getConditionLabel = (condition) => {
    const labels = {
      healthy: 'Sano',
      cavity: 'Caries',
      filled: 'Obturado',
      crown: 'Corona',
      root_canal: 'Endodoncia',
      missing: 'Ausente',
      impacted: 'Impactado'
    };
    return labels?.[condition] || condition;
  };

  const handleToothClick = (toothNumber) => {
    setSelectedTooth(toothNumber);
    if (onToothClick) {
      onToothClick(toothNumber, odontogramData?.[toothNumber]);
    }
  };

  const ToothSVG = ({ number, position, onClick }) => {
    const color = getToothColor(number);
    const isSelected = selectedTooth === number;
    const isHovered = hoveredTooth === number;
    
    return (
      <g
        onClick={() => onClick(number)}
        onMouseEnter={() => setHoveredTooth(number)}
        onMouseLeave={() => setHoveredTooth(null)}
        className="cursor-pointer"
        transform={`translate(${position?.x}, ${position?.y})`}
      >
        {/* Tooth shape */}
        <rect
          x="0"
          y="0"
          width="24"
          height="32"
          rx="4"
          fill={color}
          stroke={isSelected ? "#2563EB" : isHovered ? "#64748B" : "transparent"}
          strokeWidth={isSelected ? "3" : "2"}
          opacity={isHovered ? 0.8 : 1}
        />
        {/* Tooth number */}
        <text
          x="12"
          y="20"
          textAnchor="middle"
          fontSize="10"
          fill="white"
          fontWeight="bold"
        >
          {number}
        </text>
        {/* Condition indicator */}
        {odontogramData?.[number]?.treatments?.length > 0 && (
          <circle
            cx="20"
            cy="4"
            r="3"
            fill="#FFFFFF"
            stroke={color}
            strokeWidth="1"
          />
        )}
      </g>
    );
  };

  const renderQuadrant = (teeth, startX, startY, direction = 'horizontal') => {
    return teeth?.map((toothNumber, index) => {
      const position = direction === 'horizontal' 
        ? { x: startX + (index * 30), y: startY }
        : { x: startX, y: startY + (index * 38) };
      
      return (
        <ToothSVG
          key={toothNumber}
          number={toothNumber}
          position={position}
          onClick={handleToothClick}
        />
      );
    });
  };

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="Tooth" size={20} className="text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Odontograma Digital</h2>
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant={viewMode === 'current' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('current')}
          >
            Actual
          </Button>
          <Button
            variant={viewMode === 'history' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('history')}
          >
            Historial
          </Button>
        </div>
      </div>
      <div className="p-4">
        {/* Odontogram SVG */}
        <div className="bg-muted/30 rounded-lg p-6 mb-4">
          <svg width="100%" height="400" viewBox="0 0 600 400" className="mx-auto">
            {/* Upper jaw */}
            <g>
              {/* Upper right quadrant */}
              {renderQuadrant(adultTeeth?.upperRight, 50, 50)}
              
              {/* Upper left quadrant */}
              {renderQuadrant(adultTeeth?.upperLeft, 290, 50)}
            </g>
            
            {/* Jaw separation line */}
            <line x1="50" y1="200" x2="550" y2="200" stroke="#CBD5E1" strokeWidth="2" strokeDasharray="5,5" />
            
            {/* Lower jaw */}
            <g>
              {/* Lower left quadrant */}
              {renderQuadrant(adultTeeth?.lowerLeft, 290, 220)}
              
              {/* Lower right quadrant */}
              {renderQuadrant(adultTeeth?.lowerRight, 50, 220)}
            </g>
            
            {/* Quadrant labels */}
            <text x="150" y="30" textAnchor="middle" fontSize="12" fill="#64748B" fontWeight="bold">
              Cuadrante 1 (Superior Derecho)
            </text>
            <text x="390" y="30" textAnchor="middle" fontSize="12" fill="#64748B" fontWeight="bold">
              Cuadrante 2 (Superior Izquierdo)
            </text>
            <text x="390" y="380" textAnchor="middle" fontSize="12" fill="#64748B" fontWeight="bold">
              Cuadrante 3 (Inferior Izquierdo)
            </text>
            <text x="150" y="380" textAnchor="middle" fontSize="12" fill="#64748B" fontWeight="bold">
              Cuadrante 4 (Inferior Derecho)
            </text>
          </svg>
        </div>

        {/* Legend */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-4">
          {[
            { condition: 'healthy', label: 'Sano', color: '#10B981' },
            { condition: 'cavity', label: 'Caries', color: '#EF4444' },
            { condition: 'filled', label: 'Obturado', color: '#3B82F6' },
            { condition: 'crown', label: 'Corona', color: '#8B5CF6' },
            { condition: 'root_canal', label: 'Endodoncia', color: '#F59E0B' },
            { condition: 'missing', label: 'Ausente', color: '#6B7280' },
            { condition: 'impacted', label: 'Impactado', color: '#EC4899' }
          ]?.map((item) => (
            <div key={item?.condition} className="flex items-center space-x-2">
              <div
                className="w-4 h-4 rounded"
                style={{ backgroundColor: item?.color }}
              ></div>
              <span className="text-sm text-foreground">{item?.label}</span>
            </div>
          ))}
        </div>

        {/* Selected Tooth Details */}
        {selectedTooth && odontogramData?.[selectedTooth] && (
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
            <h3 className="text-md font-semibold text-foreground mb-3 flex items-center">
              <Icon name="Info" size={16} className="mr-2 text-primary" />
              Diente {selectedTooth} - Detalles
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-muted-foreground">Estado</div>
                <div className="font-medium text-foreground">
                  {getConditionLabel(odontogramData?.[selectedTooth]?.condition)}
                </div>
              </div>
              
              <div>
                <div className="text-sm text-muted-foreground">Tratamientos</div>
                <div className="font-medium text-foreground">
                  {odontogramData?.[selectedTooth]?.treatments?.length > 0 
                    ? odontogramData?.[selectedTooth]?.treatments?.join(', ')
                    : 'Ninguno'
                  }
                </div>
              </div>
              
              <div>
                <div className="text-sm text-muted-foreground">Última Actualización</div>
                <div className="font-medium text-foreground">
                  {new Date(odontogramData[selectedTooth].lastUpdate)?.toLocaleDateString('es-VE')}
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-2 mt-4">
              <Button variant="outline" size="sm">
                <Icon name="History" size={14} className="mr-1" />
                Ver Historial
              </Button>
              <Button variant="outline" size="sm">
                <Icon name="Edit" size={14} className="mr-1" />
                Editar Estado
              </Button>
            </div>
          </div>
        )}

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
          <div className="bg-success/10 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-success">
              {Object.values(odontogramData)?.filter(t => t?.condition === 'healthy')?.length}
            </div>
            <div className="text-xs text-muted-foreground">Dientes Sanos</div>
          </div>
          
          <div className="bg-error/10 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-error">
              {Object.values(odontogramData)?.filter(t => t?.condition === 'cavity')?.length}
            </div>
            <div className="text-xs text-muted-foreground">Con Caries</div>
          </div>
          
          <div className="bg-primary/10 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-primary">
              {Object.values(odontogramData)?.filter(t => t?.condition === 'filled')?.length}
            </div>
            <div className="text-xs text-muted-foreground">Obturados</div>
          </div>
          
          <div className="bg-muted rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-foreground">
              {Object.values(odontogramData)?.filter(t => t?.condition === 'missing')?.length}
            </div>
            <div className="text-xs text-muted-foreground">Ausentes</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DigitalOdontogramViewer;