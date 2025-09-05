import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';

const TreatmentDocumentation = ({ 
  treatmentData, 
  onUpdateTreatmentData, 
  onSaveTreatment, 
  onCompleteSession, 
  sessionActive,
  hasUnsavedChanges 
}) => {
  const [activeTab, setActiveTab] = useState('procedures');
  const [newProcedure, setNewProcedure] = useState({
    name: '',
    toothNumber: '',
    notes: '',
    billingCode: '',
    duration: ''
  });
  const [newMedication, setNewMedication] = useState({
    name: '',
    dosage: '',
    frequency: '',
    duration: '',
    instructions: ''
  });

  const commonProcedures = [
    { name: 'Limpieza dental', billingCode: 'D1110', duration: '45' },
    { name: 'Obturación composite', billingCode: 'D2140', duration: '60' },
    { name: 'Extracción simple', billingCode: 'D7140', duration: '30' },
    { name: 'Endodoncia', billingCode: 'D3310', duration: '90' },
    { name: 'Corona dental', billingCode: 'D2740', duration: '120' },
    { name: 'Radiografía panorámica', billingCode: 'D0330', duration: '15' },
    { name: 'Implante dental', billingCode: 'D6010', duration: '180' }
  ];

  const commonMedications = [
    { name: 'Ibuprofeno', dosage: '400mg', frequency: 'Cada 8 horas' },
    { name: 'Amoxicilina', dosage: '500mg', frequency: 'Cada 8 horas' },
    { name: 'Acetaminofén', dosage: '500mg', frequency: 'Cada 6 horas' },
    { name: 'Clindamicina', dosage: '300mg', frequency: 'Cada 6 horas' },
    { name: 'Enjuague bucal', dosage: '15ml', frequency: '2 veces al día' }
  ];

  const handleAddProcedure = () => {
    if (newProcedure?.name) {
      const procedure = {
        id: Date.now(),
        ...newProcedure,
        timestamp: new Date()?.toISOString()
      };
      
      onUpdateTreatmentData({
        procedures: [...(treatmentData?.procedures || []), procedure]
      });
      
      setNewProcedure({
        name: '',
        toothNumber: '',
        notes: '',
        billingCode: '',
        duration: ''
      });
    }
  };

  const handleAddMedication = () => {
    if (newMedication?.name) {
      const medication = {
        id: Date.now(),
        ...newMedication,
        timestamp: new Date()?.toISOString()
      };
      
      onUpdateTreatmentData({
        medications: [...(treatmentData?.medications || []), medication]
      });
      
      setNewMedication({
        name: '',
        dosage: '',
        frequency: '',
        duration: '',
        instructions: ''
      });
    }
  };

  const handleRemoveProcedure = (procedureId) => {
    onUpdateTreatmentData({
      procedures: treatmentData?.procedures?.filter(p => p?.id !== procedureId)
    });
  };

  const handleRemoveMedication = (medicationId) => {
    onUpdateTreatmentData({
      medications: treatmentData?.medications?.filter(m => m?.id !== medicationId)
    });
  };

  const handleNotesChange = (notes) => {
    onUpdateTreatmentData({ notes });
  };

  const handleFollowUpDateChange = (followUpDate) => {
    onUpdateTreatmentData({ followUpDate });
  };

  const handleQuickProcedure = (procedure) => {
    setNewProcedure({
      ...newProcedure,
      name: procedure?.name,
      billingCode: procedure?.billingCode,
      duration: procedure?.duration
    });
  };

  const handleQuickMedication = (medication) => {
    setNewMedication({
      ...newMedication,
      name: medication?.name,
      dosage: medication?.dosage,
      frequency: medication?.frequency
    });
  };

  const formatDate = (dateString) => {
    return new Date(dateString)?.toLocaleString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center space-x-3 mb-4">
          <Icon name="FileText" size={20} color="var(--color-primary)" />
          <div>
            <h3 className="text-lg font-semibold text-card-foreground">
              Documentación de Tratamiento
            </h3>
            <p className="text-sm text-muted-foreground">
              Registro de procedimientos y medicación
            </p>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1">
          <Button
            variant={activeTab === 'procedures' ? 'default' : 'ghost'}
            size="sm"
            iconName="Stethoscope"
            iconPosition="left"
            iconSize={14}
            onClick={() => setActiveTab('procedures')}
          >
            Procedimientos
          </Button>
          <Button
            variant={activeTab === 'medications' ? 'default' : 'ghost'}
            size="sm"
            iconName="Pill"
            iconPosition="left"
            iconSize={14}
            onClick={() => setActiveTab('medications')}
          >
            Medicación
          </Button>
          <Button
            variant={activeTab === 'notes' ? 'default' : 'ghost'}
            size="sm"
            iconName="StickyNote"
            iconPosition="left"
            iconSize={14}
            onClick={() => setActiveTab('notes')}
          >
            Notas
          </Button>
        </div>
      </div>
      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-4">
        {activeTab === 'procedures' && (
          <div className="space-y-4">
            {/* Quick Procedures */}
            <div>
              <h4 className="text-sm font-medium text-card-foreground mb-2">
                Procedimientos Comunes
              </h4>
              <div className="grid grid-cols-1 gap-1">
                {commonProcedures?.map((procedure, index) => (
                  <Button
                    key={index}
                    variant="ghost"
                    size="sm"
                    onClick={() => handleQuickProcedure(procedure)}
                    disabled={!sessionActive}
                    className="justify-start text-xs"
                  >
                    {procedure?.name} ({procedure?.billingCode})
                  </Button>
                ))}
              </div>
            </div>

            {/* Add New Procedure */}
            {sessionActive && (
              <div className="p-3 bg-muted/20 rounded-lg space-y-3">
                <h4 className="text-sm font-medium text-card-foreground">
                  Agregar Procedimiento
                </h4>
                
                <div className="space-y-2">
                  <Input
                    placeholder="Nombre del procedimiento"
                    value={newProcedure?.name}
                    onChange={(e) => setNewProcedure({...newProcedure, name: e?.target?.value})}
                    size="sm"
                  />
                  
                  <div className="grid grid-cols-2 gap-2">
                    <Input
                      placeholder="Diente #"
                      value={newProcedure?.toothNumber}
                      onChange={(e) => setNewProcedure({...newProcedure, toothNumber: e?.target?.value})}
                      size="sm"
                    />
                    <Input
                      placeholder="Código"
                      value={newProcedure?.billingCode}
                      onChange={(e) => setNewProcedure({...newProcedure, billingCode: e?.target?.value})}
                      size="sm"
                    />
                  </div>

                  <Input
                    placeholder="Duración (min)"
                    value={newProcedure?.duration}
                    onChange={(e) => setNewProcedure({...newProcedure, duration: e?.target?.value})}
                    size="sm"
                  />
                  
                  <textarea
                    className="w-full h-16 p-2 text-sm border border-border rounded-md bg-background resize-none"
                    placeholder="Notas del procedimiento..."
                    value={newProcedure?.notes}
                    onChange={(e) => setNewProcedure({...newProcedure, notes: e?.target?.value})}
                  />
                  
                  <Button
                    variant="default"
                    size="sm"
                    iconName="Plus"
                    iconPosition="left"
                    iconSize={14}
                    onClick={handleAddProcedure}
                    disabled={!newProcedure?.name}
                  >
                    Agregar Procedimiento
                  </Button>
                </div>
              </div>
            )}

            {/* Procedure List */}
            <div>
              <h4 className="text-sm font-medium text-card-foreground mb-2">
                Procedimientos de la Sesión ({treatmentData?.procedures?.length || 0})
              </h4>
              
              {treatmentData?.procedures?.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No se han registrado procedimientos
                </p>
              ) : (
                <div className="space-y-2">
                  {treatmentData?.procedures?.map((procedure) => (
                    <div key={procedure?.id} className="p-3 bg-card border border-border rounded-lg">
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex-1">
                          <h5 className="text-sm font-medium text-card-foreground">
                            {procedure?.name}
                            {procedure?.toothNumber && ` - Diente ${procedure?.toothNumber}`}
                          </h5>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground mt-1">
                            <span>{procedure?.billingCode}</span>
                            {procedure?.duration && <span>• {procedure?.duration} min</span>}
                            <span>• {formatDate(procedure?.timestamp)}</span>
                          </div>
                        </div>
                        
                        {sessionActive && (
                          <Button
                            variant="ghost"
                            size="xs"
                            iconName="Trash2"
                            onClick={() => handleRemoveProcedure(procedure?.id)}
                          />
                        )}
                      </div>
                      
                      {procedure?.notes && (
                        <p className="text-xs text-muted-foreground">
                          {procedure?.notes}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'medications' && (
          <div className="space-y-4">
            {/* Quick Medications */}
            <div>
              <h4 className="text-sm font-medium text-card-foreground mb-2">
                Medicamentos Comunes
              </h4>
              <div className="grid grid-cols-1 gap-1">
                {commonMedications?.map((medication, index) => (
                  <Button
                    key={index}
                    variant="ghost"
                    size="sm"
                    onClick={() => handleQuickMedication(medication)}
                    disabled={!sessionActive}
                    className="justify-start text-xs"
                  >
                    {medication?.name} {medication?.dosage}
                  </Button>
                ))}
              </div>
            </div>

            {/* Add New Medication */}
            {sessionActive && (
              <div className="p-3 bg-muted/20 rounded-lg space-y-3">
                <h4 className="text-sm font-medium text-card-foreground">
                  Recetar Medicamento
                </h4>
                
                <div className="space-y-2">
                  <Input
                    placeholder="Nombre del medicamento"
                    value={newMedication?.name}
                    onChange={(e) => setNewMedication({...newMedication, name: e?.target?.value})}
                    size="sm"
                  />
                  
                  <div className="grid grid-cols-2 gap-2">
                    <Input
                      placeholder="Dosis"
                      value={newMedication?.dosage}
                      onChange={(e) => setNewMedication({...newMedication, dosage: e?.target?.value})}
                      size="sm"
                    />
                    <Input
                      placeholder="Frecuencia"
                      value={newMedication?.frequency}
                      onChange={(e) => setNewMedication({...newMedication, frequency: e?.target?.value})}
                      size="sm"
                    />
                  </div>

                  <Input
                    placeholder="Duración del tratamiento"
                    value={newMedication?.duration}
                    onChange={(e) => setNewMedication({...newMedication, duration: e?.target?.value})}
                    size="sm"
                  />
                  
                  <textarea
                    className="w-full h-16 p-2 text-sm border border-border rounded-md bg-background resize-none"
                    placeholder="Instrucciones especiales..."
                    value={newMedication?.instructions}
                    onChange={(e) => setNewMedication({...newMedication, instructions: e?.target?.value})}
                  />
                  
                  <Button
                    variant="default"
                    size="sm"
                    iconName="Plus"
                    iconPosition="left"
                    iconSize={14}
                    onClick={handleAddMedication}
                    disabled={!newMedication?.name}
                  >
                    Recetar Medicamento
                  </Button>
                </div>
              </div>
            )}

            {/* Medication List */}
            <div>
              <h4 className="text-sm font-medium text-card-foreground mb-2">
                Medicamentos Recetados ({treatmentData?.medications?.length || 0})
              </h4>
              
              {treatmentData?.medications?.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No se han recetado medicamentos
                </p>
              ) : (
                <div className="space-y-2">
                  {treatmentData?.medications?.map((medication) => (
                    <div key={medication?.id} className="p-3 bg-card border border-border rounded-lg">
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex-1">
                          <h5 className="text-sm font-medium text-card-foreground">
                            {medication?.name} {medication?.dosage}
                          </h5>
                          <div className="text-xs text-muted-foreground mt-1">
                            {medication?.frequency}
                            {medication?.duration && ` • ${medication?.duration}`}
                            <span> • {formatDate(medication?.timestamp)}</span>
                          </div>
                        </div>
                        
                        {sessionActive && (
                          <Button
                            variant="ghost"
                            size="xs"
                            iconName="Trash2"
                            onClick={() => handleRemoveMedication(medication?.id)}
                          />
                        )}
                      </div>
                      
                      {medication?.instructions && (
                        <p className="text-xs text-muted-foreground">
                          {medication?.instructions}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'notes' && (
          <div className="space-y-4">
            {/* Session Notes */}
            <div>
              <h4 className="text-sm font-medium text-card-foreground mb-2">
                Notas de la Sesión
              </h4>
              <textarea
                className="w-full h-40 p-3 text-sm border border-border rounded-md bg-background resize-none"
                placeholder={sessionActive ? "Notas generales del tratamiento..." : "Sesión inactiva - no se pueden editar notas"}
                value={treatmentData?.notes || ''}
                onChange={(e) => handleNotesChange(e?.target?.value)}
                disabled={!sessionActive}
              />
            </div>

            {/* Follow-up */}
            <div>
              <h4 className="text-sm font-medium text-card-foreground mb-2">
                Programar Seguimiento
              </h4>
              <input
                type="datetime-local"
                className="w-full p-2 text-sm border border-border rounded-md bg-background"
                value={treatmentData?.followUpDate || ''}
                onChange={(e) => handleFollowUpDateChange(e?.target?.value)}
                disabled={!sessionActive}
              />
            </div>

            {/* Clinical Photography Upload */}
            <div>
              <h4 className="text-sm font-medium text-card-foreground mb-2">
                Fotografías Clínicas
              </h4>
              <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                <Icon name="Camera" size={32} color="var(--color-muted-foreground)" className="mx-auto mb-2" />
                <p className="text-sm text-muted-foreground mb-2">
                  Arrastra imágenes aquí o haz clic para seleccionar
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  iconName="Upload"
                  iconPosition="left"
                  iconSize={14}
                  disabled={!sessionActive}
                >
                  Subir Fotos
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
      {/* Action Buttons */}
      <div className="p-4 border-t border-border space-y-2">
        {sessionActive && (
          <>
            <Button
              variant="default"
              size="sm"
              iconName="Save"
              iconPosition="left"
              iconSize={16}
              onClick={onSaveTreatment}
              disabled={!hasUnsavedChanges}
              className="w-full"
            >
              Guardar Notas de Tratamiento
            </Button>
            
            <Button
              variant="success"
              size="sm"
              iconName="CheckCircle"
              iconPosition="left"
              iconSize={16}
              onClick={onCompleteSession}
              className="w-full"
            >
              Completar Sesión
            </Button>
          </>
        )}

        <div className="grid grid-cols-2 gap-2">
          <Button
            variant="outline"
            size="sm"
            iconName="Calendar"
            iconPosition="left"
            iconSize={14}
            disabled={!sessionActive}
          >
            Programar Cita
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            iconName="Printer"
            iconPosition="left"
            iconSize={14}
          >
            Imprimir
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TreatmentDocumentation;