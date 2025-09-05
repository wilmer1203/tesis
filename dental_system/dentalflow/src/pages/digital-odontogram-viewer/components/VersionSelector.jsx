import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const VersionSelector = ({ 
  versions, 
  selectedVersion, 
  comparisonVersion, 
  showComparison, 
  onVersionChange, 
  onComparisonVersionChange, 
  onToggleComparison,
  onExport,
  onPrint 
}) => {
  const formatVersionDate = (dateString) => {
    return new Date(dateString)?.toLocaleDateString('es-VE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const getVersionChanges = (version) => {
    // Mock changes data
    const changes = {
      'v1.0': { added: 0, modified: 0, total: 32 },
      'v1.1': { added: 2, modified: 1, total: 32 },
      'v1.2': { added: 0, modified: 3, total: 32 },
      'v1.3': { added: 1, modified: 2, total: 32 }
    };
    return changes?.[version] || { added: 0, modified: 0, total: 32 };
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
        {/* Version Selection */}
        <div className="flex flex-col sm:flex-row sm:items-center space-y-3 sm:space-y-0 sm:space-x-6">
          {/* Primary Version */}
          <div className="flex items-center space-x-3">
            <label className="text-sm font-medium text-foreground">Versión:</label>
            <select
              value={selectedVersion}
              onChange={(e) => onVersionChange(e?.target?.value)}
              className="px-3 py-2 border border-border rounded-md text-sm bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              {versions?.map((version) => (
                <option key={version?.id} value={version?.id}>
                  {version?.name} - {formatVersionDate(version?.date)}
                </option>
              ))}
            </select>
          </div>

          {/* Comparison Toggle */}
          <div className="flex items-center space-x-3">
            <Button
              variant={showComparison ? "default" : "outline"}
              size="sm"
              onClick={onToggleComparison}
            >
              <Icon name="GitCompare" size={16} className="mr-2" />
              {showComparison ? 'Ocultar Comparación' : 'Comparar Versiones'}
            </Button>
          </div>

          {/* Comparison Version (when comparison is enabled) */}
          {showComparison && (
            <div className="flex items-center space-x-3">
              <label className="text-sm font-medium text-foreground">vs:</label>
              <select
                value={comparisonVersion}
                onChange={(e) => onComparisonVersionChange(e?.target?.value)}
                className="px-3 py-2 border border-border rounded-md text-sm bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                {versions?.filter(v => v?.id !== selectedVersion)?.map((version) => (
                    <option key={version?.id} value={version?.id}>
                      {version?.name} - {formatVersionDate(version?.date)}
                    </option>
                  ))}
              </select>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={onPrint}>
            <Icon name="Printer" size={16} className="mr-2" />
            Imprimir
          </Button>
          
          <Button variant="outline" size="sm" onClick={onExport}>
            <Icon name="Download" size={16} className="mr-2" />
            Exportar
          </Button>
        </div>
      </div>
      {/* Version Information */}
      <div className="mt-4 pt-4 border-t border-border">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Selected Version Info */}
          <div className="bg-muted rounded-md p-3">
            <h4 className="text-sm font-medium text-foreground mb-2">
              Versión Actual: {versions?.find(v => v?.id === selectedVersion)?.name}
            </h4>
            <div className="space-y-1 text-xs text-muted-foreground">
              <div>Fecha: {formatVersionDate(versions?.find(v => v?.id === selectedVersion)?.date)}</div>
              <div>Dentista: {versions?.find(v => v?.id === selectedVersion)?.dentist}</div>
              <div className="flex items-center space-x-4 mt-2">
                {(() => {
                  const changes = getVersionChanges(selectedVersion);
                  return (
                    <>
                      <span className="text-success">+{changes?.added}</span>
                      <span className="text-warning">~{changes?.modified}</span>
                      <span className="text-muted-foreground">Total: {changes?.total}</span>
                    </>
                  );
                })()}
              </div>
            </div>
          </div>

          {/* Comparison Version Info (when comparison is enabled) */}
          {showComparison && comparisonVersion && (
            <div className="bg-muted rounded-md p-3">
              <h4 className="text-sm font-medium text-foreground mb-2">
                Comparando con: {versions?.find(v => v?.id === comparisonVersion)?.name}
              </h4>
              <div className="space-y-1 text-xs text-muted-foreground">
                <div>Fecha: {formatVersionDate(versions?.find(v => v?.id === comparisonVersion)?.date)}</div>
                <div>Dentista: {versions?.find(v => v?.id === comparisonVersion)?.dentist}</div>
                <div className="flex items-center space-x-4 mt-2">
                  {(() => {
                    const changes = getVersionChanges(comparisonVersion);
                    return (
                      <>
                        <span className="text-success">+{changes?.added}</span>
                        <span className="text-warning">~{changes?.modified}</span>
                        <span className="text-muted-foreground">Total: {changes?.total}</span>
                      </>
                    );
                  })()}
                </div>
              </div>
            </div>
          )}

          {/* Change Summary */}
          <div className="bg-primary/10 rounded-md p-3">
            <h4 className="text-sm font-medium text-foreground mb-2">
              {showComparison ? 'Diferencias Detectadas' : 'Resumen de Cambios'}
            </h4>
            <div className="space-y-1 text-xs">
              {showComparison ? (
                <>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Nuevos tratamientos:</span>
                    <span className="text-success font-medium">3</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Modificaciones:</span>
                    <span className="text-warning font-medium">2</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Sin cambios:</span>
                    <span className="text-muted-foreground font-medium">27</span>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Última actualización:</span>
                    <span className="text-foreground font-medium">04/09/2024</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Cambios pendientes:</span>
                    <span className="text-warning font-medium">2</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Estado:</span>
                    <span className="text-success font-medium">Actualizado</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
      {/* Legend for changes */}
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex items-center justify-between">
          <h5 className="text-sm font-medium text-foreground">Leyenda de Cambios:</h5>
          <div className="flex items-center space-x-4 text-xs">
            <div className="flex items-center space-x-1">
              <span className="text-success">+</span>
              <span className="text-muted-foreground">Agregado</span>
            </div>
            <div className="flex items-center space-x-1">
              <span className="text-warning">~</span>
              <span className="text-muted-foreground">Modificado</span>
            </div>
            <div className="flex items-center space-x-1">
              <span className="text-error">-</span>
              <span className="text-muted-foreground">Eliminado</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VersionSelector;