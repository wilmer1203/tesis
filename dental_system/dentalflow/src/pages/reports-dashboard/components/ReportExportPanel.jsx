import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ReportExportPanel = ({ activeTab, dateRange, className = '' }) => {
  const [exportFormat, setExportFormat] = useState('pdf');
  const [includeCharts, setIncludeCharts] = useState(true);
  const [includeRawData, setIncludeRawData] = useState(false);
  const [emailRecipients, setEmailRecipients] = useState('');
  const [isExporting, setIsExporting] = useState(false);
  const [showScheduler, setShowScheduler] = useState(false);

  const exportFormats = [
    { id: 'pdf', label: 'PDF', icon: 'FileText', description: 'Documento con formato' },
    { id: 'excel', label: 'Excel', icon: 'FileSpreadsheet', description: 'Hoja de cálculo' },
    { id: 'csv', label: 'CSV', icon: 'Database', description: 'Datos separados por comas' },
    { id: 'json', label: 'JSON', icon: 'Code', description: 'Formato de datos estructurado' }
  ];

  const scheduleOptions = [
    { id: 'daily', label: 'Diario', description: 'Todos los días a las 8:00 AM' },
    { id: 'weekly', label: 'Semanal', description: 'Lunes a las 8:00 AM' },
    { id: 'monthly', label: 'Mensual', description: 'Primer día del mes a las 8:00 AM' },
    { id: 'quarterly', label: 'Trimestral', description: 'Primer día del trimestre' }
  ];

  const handleExport = async () => {
    setIsExporting(true);
    
    // Simulate export process
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock export logic
    const exportData = {
      format: exportFormat,
      tab: activeTab,
      dateRange: dateRange,
      includeCharts,
      includeRawData,
      timestamp: new Date()?.toISOString()
    };

    console.log('Exporting report:', exportData);
    
    // Simulate file download
    const fileName = `reporte-${activeTab}-${new Date()?.toISOString()?.split('T')?.[0]}.${exportFormat}`;
    console.log(`Descargando: ${fileName}`);
    
    setIsExporting(false);
    
    // Show success message
    alert(`Reporte exportado exitosamente como ${fileName}`);
  };

  const handleScheduleReport = () => {
    console.log('Programando reporte automático');
    setShowScheduler(false);
    alert('Reporte programado exitosamente');
  };

  const handleEmailReport = () => {
    if (!emailRecipients?.trim()) {
      alert('Por favor ingrese al menos un destinatario');
      return;
    }
    
    console.log('Enviando reporte por email a:', emailRecipients);
    alert(`Reporte enviado por email a: ${emailRecipients}`);
    setEmailRecipients('');
  };

  return (
    <div className={`bg-card border border-border rounded-lg p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-foreground">Exportar Reporte</h3>
        <Icon name="Download" size={20} className="text-primary" />
      </div>
      <div className="space-y-6">
        {/* Export Format Selection */}
        <div>
          <label className="block text-sm font-medium text-foreground mb-3">
            Formato de Exportación
          </label>
          <div className="grid grid-cols-2 gap-3">
            {exportFormats?.map((format) => (
              <button
                key={format?.id}
                onClick={() => setExportFormat(format?.id)}
                className={`flex items-center space-x-3 p-3 rounded-lg border transition-smooth ${
                  exportFormat === format?.id
                    ? 'border-primary bg-primary/10 text-primary' :'border-border bg-muted text-muted-foreground hover:text-foreground hover:border-border'
                }`}
              >
                <Icon name={format?.icon} size={20} />
                <div className="text-left">
                  <div className="font-medium">{format?.label}</div>
                  <div className="text-xs opacity-80">{format?.description}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Export Options */}
        <div>
          <label className="block text-sm font-medium text-foreground mb-3">
            Opciones de Contenido
          </label>
          <div className="space-y-3">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={includeCharts}
                onChange={(e) => setIncludeCharts(e?.target?.checked)}
                className="w-4 h-4 text-primary border-border rounded focus:ring-ring"
              />
              <span className="text-sm text-foreground">Incluir gráficos y visualizaciones</span>
            </label>
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={includeRawData}
                onChange={(e) => setIncludeRawData(e?.target?.checked)}
                className="w-4 h-4 text-primary border-border rounded focus:ring-ring"
              />
              <span className="text-sm text-foreground">Incluir datos sin procesar</span>
            </label>
          </div>
        </div>

        {/* Date Range Display */}
        <div className="bg-muted rounded-lg p-3">
          <div className="flex items-center space-x-2 text-sm">
            <Icon name="Calendar" size={16} className="text-muted-foreground" />
            <span className="text-muted-foreground">Período:</span>
            <span className="font-medium text-foreground">
              {dateRange?.start && dateRange?.end
                ? `${dateRange?.start?.toLocaleDateString('es-VE')} - ${dateRange?.end?.toLocaleDateString('es-VE')}`
                : 'Período no seleccionado'
              }
            </span>
          </div>
        </div>

        {/* Export Actions */}
        <div className="space-y-3">
          <Button
            variant="default"
            fullWidth
            onClick={handleExport}
            loading={isExporting}
            iconName="Download"
            iconPosition="left"
          >
            {isExporting ? 'Exportando...' : 'Descargar Reporte'}
          </Button>

          <div className="grid grid-cols-2 gap-3">
            <Button
              variant="outline"
              onClick={() => setShowScheduler(true)}
              iconName="Clock"
              iconPosition="left"
            >
              Programar
            </Button>
            <Button
              variant="outline"
              onClick={handleEmailReport}
              iconName="Mail"
              iconPosition="left"
            >
              Enviar Email
            </Button>
          </div>
        </div>

        {/* Email Recipients */}
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            Destinatarios de Email (opcional)
          </label>
          <textarea
            value={emailRecipients}
            onChange={(e) => setEmailRecipients(e?.target?.value)}
            placeholder="admin@clinica.com, doctor@clinica.com"
            className="w-full px-3 py-2 text-sm border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-none"
            rows={3}
          />
          <div className="text-xs text-muted-foreground mt-1">
            Separar múltiples emails con comas
          </div>
        </div>

        {/* Recent Exports */}
        <div>
          <h4 className="text-sm font-medium text-foreground mb-3">Exportaciones Recientes</h4>
          <div className="space-y-2">
            {[
              { name: 'reporte-financiero-2024-09-03.pdf', date: '03/09/2024', size: '2.4 MB' },
              { name: 'reporte-pacientes-2024-09-02.xlsx', date: '02/09/2024', size: '1.8 MB' },
              { name: 'reporte-operaciones-2024-09-01.csv', date: '01/09/2024', size: '856 KB' }
            ]?.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-2 bg-muted rounded-md">
                <div className="flex items-center space-x-2">
                  <Icon name="FileText" size={14} className="text-muted-foreground" />
                  <div>
                    <div className="text-xs font-medium text-foreground">{file?.name}</div>
                    <div className="text-xs text-muted-foreground">{file?.date} • {file?.size}</div>
                  </div>
                </div>
                <button className="p-1 hover:bg-background rounded transition-smooth">
                  <Icon name="Download" size={14} className="text-muted-foreground" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
      {/* Schedule Modal */}
      {showScheduler && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-popover border border-border rounded-lg p-6 w-full max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-foreground">Programar Reporte</h3>
              <button
                onClick={() => setShowScheduler(false)}
                className="p-1 hover:bg-muted rounded transition-smooth"
              >
                <Icon name="X" size={16} className="text-muted-foreground" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Frecuencia
                </label>
                <div className="space-y-2">
                  {scheduleOptions?.map((option) => (
                    <label key={option?.id} className="flex items-start space-x-3">
                      <input
                        type="radio"
                        name="schedule"
                        value={option?.id}
                        className="mt-1 w-4 h-4 text-primary border-border focus:ring-ring"
                      />
                      <div>
                        <div className="text-sm font-medium text-foreground">{option?.label}</div>
                        <div className="text-xs text-muted-foreground">{option?.description}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <Button
                  variant="outline"
                  onClick={() => setShowScheduler(false)}
                >
                  Cancelar
                </Button>
                <Button
                  variant="default"
                  onClick={handleScheduleReport}
                >
                  Programar
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportExportPanel;