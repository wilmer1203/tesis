import React from 'react';
import Icon from '../../../components/AppIcon';
import PatientCard from './PatientCard';

const PatientList = ({ 
  patients, 
  selectedPatient, 
  onPatientSelect, 
  isLoading = false 
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2 text-muted-foreground">
          <Icon name="Loader2" size={20} className="animate-spin" />
          <span>Cargando pacientes...</span>
        </div>
      </div>
    );
  }

  if (patients?.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-center">
        <Icon name="Users" size={48} color="var(--color-muted-foreground)" />
        <h3 className="mt-4 text-lg font-semibold text-foreground">
          No se encontraron pacientes
        </h3>
        <p className="mt-2 text-sm text-muted-foreground max-w-sm">
          No hay pacientes que coincidan con los criterios de búsqueda actuales.
          Intenta ajustar los filtros o agregar un nuevo paciente.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-foreground">
          Pacientes ({patients?.length})
        </h3>
        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
          <Icon name="Users" size={14} />
          <span>Total encontrados</span>
        </div>
      </div>
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {patients?.map((patient) => (
          <PatientCard
            key={patient?.id}
            patient={patient}
            isSelected={selectedPatient?.id === patient?.id}
            onClick={onPatientSelect}
          />
        ))}
      </div>
    </div>
  );
};

export default PatientList;