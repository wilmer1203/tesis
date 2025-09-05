import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Header from '../../components/ui/Header';
import PatientContextBar from '../../components/ui/PatientContextBar';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';
import OdontogramViewer from './components/OdontogramViewer';
import ToothDetailPanel from './components/ToothDetailPanel';
import VersionSelector from './components/VersionSelector';
import InterventionTimeline from './components/InterventionTimeline';
import TreatmentPlanningPanel from './components/TreatmentPlanningPanel';

const DigitalOdontogramViewer = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const patientId = searchParams?.get('patient');

  // State management
  const [selectedTooth, setSelectedTooth] = useState(null);
  const [selectedVersion, setSelectedVersion] = useState('v1.3');
  const [comparisonVersion, setComparisonVersion] = useState('v1.2');
  const [showComparison, setShowComparison] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(1.0);
  const [activePanel, setActivePanel] = useState('timeline'); // timeline, planning, none
  const [showPatientContext, setShowPatientContext] = useState(!!patientId);

  // Mock patient data
  const currentPatient = patientId ? {
    id: patientId,
    name: 'Ana María Rodríguez',
    age: 34,
    phone: '+58 412-555-0123',
    queuePosition: null,
    status: 'completed',
    lastVisit: '2024-09-04',
    allergies: ['Penicilina'],
    insurance: 'Seguros Caracas'
  } : null;

  // Mock odontogram versions
  const odontogramVersions = [
    {
      id: 'v1.3',
      name: 'v1.3',
      date: '2024-09-04',
      dentist: 'Dr. María González',
      changes: 3,
      description: 'Diagnóstico de caries en diente 12'
    },
    {
      id: 'v1.2',
      name: 'v1.2',
      date: '2024-09-01',
      dentist: 'Dr. Carlos Mendoza',
      changes: 2,
      description: 'Control post-endodoncia diente 16'
    },
    {
      id: 'v1.1',
      name: 'v1.1',
      date: '2024-08-28',
      dentist: 'Dr. Ana Rodríguez',
      changes: 4,
      description: 'Instalación corona diente 14'
    },
    {
      id: 'v1.0',
      name: 'v1.0',
      date: '2024-08-15',
      dentist: 'Dr. María González',
      changes: 0,
      description: 'Odontograma inicial'
    }
  ];

  // Handle tooth selection
  const handleToothClick = (toothNumber) => {
    setSelectedTooth(selectedTooth === toothNumber ? null : toothNumber);
  };

  // Handle version changes
  const handleVersionChange = (version) => {
    setSelectedVersion(version);
  };

  const handleComparisonVersionChange = (version) => {
    setComparisonVersion(version);
  };

  const handleToggleComparison = () => {
    setShowComparison(!showComparison);
    if (!showComparison && comparisonVersion === selectedVersion) {
      // Auto-select a different version for comparison
      const otherVersions = odontogramVersions?.filter(v => v?.id !== selectedVersion);
      if (otherVersions?.length > 0) {
        setComparisonVersion(otherVersions?.[0]?.id);
      }
    }
  };

  // Handle export and print
  const handleExport = () => {
    console.log('Exporting odontogram...');
    // Mock export functionality
    alert('Odontograma exportado exitosamente');
  };

  const handlePrint = () => {
    console.log('Printing odontogram...');
    window.print();
  };

  // Handle intervention actions
  const handleAddIntervention = (toothNumber) => {
    navigate(`/patient-consultation?patient=${patientId}&tooth=${toothNumber}&action=add-intervention`);
  };

  const handleInterventionClick = (intervention) => {
    console.log('Intervention clicked:', intervention);
    setSelectedTooth(intervention?.tooth);
  };

  // Handle treatment planning
  const handleSaveTreatmentPlan = (plan) => {
    console.log('Treatment plan saved:', plan);
    alert('Plan de tratamiento guardado exitosamente');
  };

  // Navigation handlers
  const handleNavigateToConsultation = () => {
    navigate(`/patient-consultation${patientId ? `?patient=${patientId}` : ''}`);
  };

  const handleNavigateToReports = () => {
    navigate('/reports-dashboard');
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e?.ctrlKey || e?.metaKey) {
        switch (e?.key) {
          case 'p':
            e?.preventDefault();
            handlePrint();
            break;
          case 'e':
            e?.preventDefault();
            handleExport();
            break;
          case 'c':
            e?.preventDefault();
            handleToggleComparison();
            break;
          default:
            break;
        }
      }
      
      if (e?.key === 'Escape') {
        setSelectedTooth(null);
        setActivePanel('timeline');
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <Header />
      {/* Patient Context Bar */}
      {showPatientContext && currentPatient && (
        <PatientContextBar
          patient={currentPatient}
          onDismiss={() => setShowPatientContext(false)}
          showQueueStatus={false}
        />
      )}
      {/* Main Content */}
      <div className={`${showPatientContext ? 'pt-32' : 'pt-16'}`}>
        <div className="max-w-7xl mx-auto p-6">
          {/* Page Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-foreground">
                Visor de Odontograma Digital
              </h1>
              <p className="text-muted-foreground">
                {currentPatient 
                  ? `Historial dental de ${currentPatient?.name}`
                  : 'Visualización y análisis de registros dentales'
                }
              </p>
            </div>

            {/* Quick Actions */}
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={handleNavigateToReports}>
                <Icon name="BarChart3" size={16} className="mr-2" />
                Reportes
              </Button>
              
              {currentPatient && (
                <Button onClick={handleNavigateToConsultation}>
                  <Icon name="Stethoscope" size={16} className="mr-2" />
                  Ir a Consulta
                </Button>
              )}
            </div>
          </div>

          {/* Version Selector */}
          <div className="mb-6">
            <VersionSelector
              versions={odontogramVersions}
              selectedVersion={selectedVersion}
              comparisonVersion={comparisonVersion}
              showComparison={showComparison}
              onVersionChange={handleVersionChange}
              onComparisonVersionChange={handleComparisonVersionChange}
              onToggleComparison={handleToggleComparison}
              onExport={handleExport}
              onPrint={handlePrint}
            />
          </div>

          {/* Main Layout */}
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
            {/* Odontogram Viewer - Main Content */}
            <div className="xl:col-span-3">
              <OdontogramViewer
                selectedVersion={selectedVersion}
                comparisonVersion={comparisonVersion}
                showComparison={showComparison}
                onToothClick={handleToothClick}
                selectedTooth={selectedTooth}
                zoomLevel={zoomLevel}
                onZoomChange={setZoomLevel}
              />

              {/* Panel Toggle Buttons */}
              <div className="mt-4 flex justify-center space-x-2">
                <Button
                  variant={activePanel === 'timeline' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setActivePanel(activePanel === 'timeline' ? 'none' : 'timeline')}
                >
                  <Icon name="Clock" size={16} className="mr-2" />
                  Línea de Tiempo
                </Button>
                
                {selectedTooth && (
                  <Button
                    variant={activePanel === 'planning' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setActivePanel(activePanel === 'planning' ? 'none' : 'planning')}
                  >
                    <Icon name="Calendar" size={16} className="mr-2" />
                    Planificar Tratamiento
                  </Button>
                )}
              </div>

              {/* Timeline Panel */}
              {activePanel === 'timeline' && (
                <div className="mt-6">
                  <InterventionTimeline
                    selectedTooth={selectedTooth}
                    onInterventionClick={handleInterventionClick}
                  />
                </div>
              )}

              {/* Treatment Planning Panel */}
              {activePanel === 'planning' && selectedTooth && (
                <div className="mt-6">
                  <TreatmentPlanningPanel
                    selectedTooth={selectedTooth}
                    onClose={() => setActivePanel('none')}
                    onSavePlan={handleSaveTreatmentPlan}
                  />
                </div>
              )}
            </div>

            {/* Tooth Detail Panel - Sidebar */}
            <div className="xl:col-span-1">
              {selectedTooth ? (
                <ToothDetailPanel
                  selectedTooth={selectedTooth}
                  onClose={() => setSelectedTooth(null)}
                  onAddIntervention={handleAddIntervention}
                />
              ) : (
                <div className="bg-card border border-border rounded-lg p-6 text-center">
                  <Icon name="MousePointer" size={48} className="text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-foreground mb-2">
                    Selecciona un Diente
                  </h3>
                  <p className="text-muted-foreground text-sm mb-4">
                    Haz clic en cualquier diente del odontograma para ver su historial detallado y planificar tratamientos.
                  </p>
                  
                  {/* Quick Stats */}
                  <div className="space-y-3 mt-6">
                    <div className="bg-muted rounded-md p-3">
                      <div className="text-sm font-medium text-foreground">Dientes Sanos</div>
                      <div className="text-2xl font-bold text-success">24</div>
                    </div>
                    <div className="bg-muted rounded-md p-3">
                      <div className="text-sm font-medium text-foreground">Requieren Atención</div>
                      <div className="text-2xl font-bold text-warning">6</div>
                    </div>
                    <div className="bg-muted rounded-md p-3">
                      <div className="text-sm font-medium text-foreground">Tratamientos Pendientes</div>
                      <div className="text-2xl font-bold text-error">2</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Help Section */}
          <div className="mt-8 bg-muted/30 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Icon name="HelpCircle" size={20} className="text-primary mt-0.5" />
              <div>
                <h4 className="font-medium text-foreground mb-1">Atajos de Teclado</h4>
                <div className="text-sm text-muted-foreground space-y-1">
                  <div><kbd className="bg-muted px-2 py-1 rounded text-xs">Ctrl+P</kbd> Imprimir odontograma</div>
                  <div><kbd className="bg-muted px-2 py-1 rounded text-xs">Ctrl+E</kbd> Exportar odontograma</div>
                  <div><kbd className="bg-muted px-2 py-1 rounded text-xs">Ctrl+C</kbd> Alternar comparación</div>
                  <div><kbd className="bg-muted px-2 py-1 rounded text-xs">Esc</kbd> Deseleccionar diente</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DigitalOdontogramViewer;