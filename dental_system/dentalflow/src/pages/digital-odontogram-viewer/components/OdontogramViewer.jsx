import React, { useState, useRef, useEffect } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const OdontogramViewer = ({ 
  selectedVersion, 
  comparisonVersion, 
  showComparison, 
  onToothClick,
  selectedTooth,
  zoomLevel,
  onZoomChange 
}) => {
  const svgRef = useRef(null);
  const [hoveredTooth, setHoveredTooth] = useState(null);

  // FDI tooth numbering system
  const adultTeeth = {
    // Upper jaw (maxilla)
    upperRight: [18, 17, 16, 15, 14, 13, 12, 11],
    upperLeft: [21, 22, 23, 24, 25, 26, 27, 28],
    // Lower jaw (mandible)
    lowerLeft: [31, 32, 33, 34, 35, 36, 37, 38],
    lowerRight: [48, 47, 46, 45, 44, 43, 42, 41]
  };

  // Mock tooth data with conditions and treatments
  const toothData = {
    11: { status: 'healthy', conditions: [], treatments: [] },
    12: { status: 'caries', conditions: ['Caries'], treatments: [] },
    13: { status: 'filled', conditions: [], treatments: ['Composite Filling'] },
    14: { status: 'crown', conditions: [], treatments: ['Porcelain Crown'] },
    15: { status: 'healthy', conditions: [], treatments: [] },
    16: { status: 'root-canal', conditions: ['Pulpitis'], treatments: ['Root Canal', 'Crown'] },
    17: { status: 'missing', conditions: ['Extracted'], treatments: ['Extraction'] },
    18: { status: 'impacted', conditions: ['Impacted'], treatments: [] },
    21: { status: 'healthy', conditions: [], treatments: [] },
    22: { status: 'healthy', conditions: [], treatments: [] },
    23: { status: 'caries', conditions: ['Caries'], treatments: [] },
    24: { status: 'filled', conditions: [], treatments: ['Amalgam Filling'] },
    25: { status: 'healthy', conditions: [], treatments: [] },
    26: { status: 'crown', conditions: [], treatments: ['Metal Crown'] },
    27: { status: 'healthy', conditions: [], treatments: [] },
    28: { status: 'missing', conditions: ['Extracted'], treatments: ['Extraction'] },
    31: { status: 'healthy', conditions: [], treatments: [] },
    32: { status: 'healthy', conditions: [], treatments: [] },
    33: { status: 'healthy', conditions: [], treatments: [] },
    34: { status: 'caries', conditions: ['Caries'], treatments: [] },
    35: { status: 'filled', conditions: [], treatments: ['Composite Filling'] },
    36: { status: 'root-canal', conditions: ['Necrosis'], treatments: ['Root Canal'] },
    37: { status: 'healthy', conditions: [], treatments: [] },
    38: { status: 'impacted', conditions: ['Impacted'], treatments: [] },
    41: { status: 'healthy', conditions: [], treatments: [] },
    42: { status: 'healthy', conditions: [], treatments: [] },
    43: { status: 'healthy', conditions: [], treatments: [] },
    44: { status: 'filled', conditions: [], treatments: ['Composite Filling'] },
    45: { status: 'healthy', conditions: [], treatments: [] },
    46: { status: 'crown', conditions: [], treatments: ['Porcelain Crown'] },
    47: { status: 'caries', conditions: ['Caries'], treatments: [] },
    48: { status: 'missing', conditions: ['Extracted'], treatments: ['Extraction'] }
  };

  const getToothColor = (toothNumber) => {
    const tooth = toothData?.[toothNumber];
    if (!tooth) return '#E2E8F0'; // Default gray

    switch (tooth?.status) {
      case 'healthy': return '#10B981'; // Green
      case 'caries': return '#EF4444'; // Red
      case 'filled': return '#3B82F6'; // Blue
      case 'crown': return '#8B5CF6'; // Purple
      case 'root-canal': return '#F59E0B'; // Amber
      case 'missing': return '#6B7280'; // Gray
      case 'impacted': return '#EC4899'; // Pink
      default: return '#E2E8F0';
    }
  };

  const getToothStroke = (toothNumber) => {
    if (selectedTooth === toothNumber) return '#1E293B';
    if (hoveredTooth === toothNumber) return '#475569';
    return '#CBD5E1';
  };

  const handleToothClick = (toothNumber) => {
    onToothClick(toothNumber);
  };

  const renderTooth = (toothNumber, x, y, isUpper = true) => {
    const toothWidth = 24;
    const toothHeight = 32;
    
    return (
      <g key={toothNumber}>
        {/* Tooth shape */}
        <rect
          x={x - toothWidth/2}
          y={y - (isUpper ? toothHeight : 0)}
          width={toothWidth}
          height={toothHeight}
          rx={4}
          fill={getToothColor(toothNumber)}
          stroke={getToothStroke(toothNumber)}
          strokeWidth={selectedTooth === toothNumber ? 3 : 2}
          className="cursor-pointer transition-all duration-200"
          onClick={() => handleToothClick(toothNumber)}
          onMouseEnter={() => setHoveredTooth(toothNumber)}
          onMouseLeave={() => setHoveredTooth(null)}
        />
        {/* Tooth number */}
        <text
          x={x}
          y={y + (isUpper ? -toothHeight/2 + 5 : toothHeight/2 + 5)}
          textAnchor="middle"
          className="text-xs font-medium fill-white pointer-events-none"
        >
          {toothNumber}
        </text>
        {/* Status indicator */}
        {toothData?.[toothNumber]?.conditions?.length > 0 && (
          <circle
            cx={x + toothWidth/2 - 4}
            cy={y - (isUpper ? toothHeight - 4 : -4)}
            r={3}
            fill="#DC2626"
            className="pointer-events-none"
          />
        )}
      </g>
    );
  };

  const renderOdontogram = () => {
    const centerX = 400;
    const centerY = 200;
    const toothSpacing = 32;
    
    return (
      <svg
        ref={svgRef}
        width="800"
        height="400"
        viewBox="0 0 800 400"
        className="w-full h-full border border-border rounded-md bg-white"
        style={{ transform: `scale(${zoomLevel})` }}
      >
        {/* Upper jaw */}
        <g>
          {/* Upper right quadrant */}
          {adultTeeth?.upperRight?.map((tooth, index) => 
            renderTooth(tooth, centerX - (index + 1) * toothSpacing, centerY - 60, true)
          )}
          
          {/* Upper left quadrant */}
          {adultTeeth?.upperLeft?.map((tooth, index) => 
            renderTooth(tooth, centerX + (index + 1) * toothSpacing, centerY - 60, true)
          )}
        </g>
        {/* Lower jaw */}
        <g>
          {/* Lower left quadrant */}
          {adultTeeth?.lowerLeft?.map((tooth, index) => 
            renderTooth(tooth, centerX + (index + 1) * toothSpacing, centerY + 60, false)
          )}
          
          {/* Lower right quadrant */}
          {adultTeeth?.lowerRight?.map((tooth, index) => 
            renderTooth(tooth, centerX - (index + 1) * toothSpacing, centerY + 60, false)
          )}
        </g>
        {/* Jaw outline */}
        <path
          d={`M ${centerX - 280} ${centerY - 80} 
              Q ${centerX} ${centerY - 100} ${centerX + 280} ${centerY - 80}
              L ${centerX + 260} ${centerY - 40}
              Q ${centerX} ${centerY - 20} ${centerX - 260} ${centerY - 40} Z`}
          fill="none"
          stroke="#94A3B8"
          strokeWidth="2"
          strokeDasharray="5,5"
        />
        <path
          d={`M ${centerX - 260} ${centerY + 40} 
              Q ${centerX} ${centerY + 20} ${centerX + 260} ${centerY + 40}
              L ${centerX + 280} ${centerY + 80}
              Q ${centerX} ${centerY + 100} ${centerX - 280} ${centerY + 80} Z`}
          fill="none"
          stroke="#94A3B8"
          strokeWidth="2"
          strokeDasharray="5,5"
        />
        {/* Center line */}
        <line
          x1={centerX}
          y1={centerY - 120}
          x2={centerX}
          y2={centerY + 120}
          stroke="#CBD5E1"
          strokeWidth="1"
          strokeDasharray="3,3"
        />
      </svg>
    );
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-foreground">
            {showComparison ? 'Comparación de Odontogramas' : 'Odontograma Digital'}
          </h3>
          <p className="text-sm text-muted-foreground">
            {showComparison 
              ? `Versión ${selectedVersion} vs Versión ${comparisonVersion}`
              : `Versión ${selectedVersion} - Actualizado el 04/09/2024`
            }
          </p>
        </div>
        
        {/* Zoom controls */}
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onZoomChange(Math.max(0.5, zoomLevel - 0.1))}
            disabled={zoomLevel <= 0.5}
          >
            <Icon name="ZoomOut" size={16} />
          </Button>
          
          <span className="text-sm text-muted-foreground px-2">
            {Math.round(zoomLevel * 100)}%
          </span>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => onZoomChange(Math.min(2.0, zoomLevel + 0.1))}
            disabled={zoomLevel >= 2.0}
          >
            <Icon name="ZoomIn" size={16} />
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => onZoomChange(1.0)}
          >
            <Icon name="RotateCcw" size={16} />
          </Button>
        </div>
      </div>
      
      {/* Odontogram display */}
      <div className="relative overflow-auto bg-muted rounded-md p-4" style={{ height: '500px' }}>
        {showComparison ? (
          <div className="grid grid-cols-2 gap-6 h-full">
            <div className="bg-white rounded border border-border p-4">
              <h4 className="text-sm font-medium text-foreground mb-2">
                Versión {selectedVersion}
              </h4>
              {renderOdontogram()}
            </div>
            <div className="bg-white rounded border border-border p-4">
              <h4 className="text-sm font-medium text-foreground mb-2">
                Versión {comparisonVersion}
              </h4>
              {renderOdontogram()}
            </div>
          </div>
        ) : (
          <div className="flex justify-center items-center h-full">
            {renderOdontogram()}
          </div>
        )}
      </div>
      
      {/* Legend */}
      <div className="mt-6 p-4 bg-muted rounded-md">
        <h4 className="text-sm font-medium text-foreground mb-3">Leyenda</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-success rounded"></div>
            <span className="text-xs text-muted-foreground">Sano</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-error rounded"></div>
            <span className="text-xs text-muted-foreground">Caries</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-primary rounded"></div>
            <span className="text-xs text-muted-foreground">Obturado</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-purple-500 rounded"></div>
            <span className="text-xs text-muted-foreground">Corona</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-warning rounded"></div>
            <span className="text-xs text-muted-foreground">Endodoncia</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-muted-foreground rounded"></div>
            <span className="text-xs text-muted-foreground">Ausente</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-pink-500 rounded"></div>
            <span className="text-xs text-muted-foreground">Impactado</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-error rounded-full"></div>
            <span className="text-xs text-muted-foreground">Condición</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OdontogramViewer;