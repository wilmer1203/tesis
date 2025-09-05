import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';


const PatientNotes = ({ patient, onAddNote, onUpdateNote }) => {
  const [newNote, setNewNote] = useState('');
  const [editingNote, setEditingNote] = useState(null);
  const [noteType, setNoteType] = useState('general');

  const noteTypes = [
    { value: 'general', label: 'General', icon: 'FileText', color: 'text-primary' },
    { value: 'tratamiento', label: 'Tratamiento', icon: 'Stethoscope', color: 'text-success' },
    { value: 'diagnostico', label: 'Diagnóstico', icon: 'Search', color: 'text-warning' },
    { value: 'seguimiento', label: 'Seguimiento', icon: 'Clock', color: 'text-secondary' }
  ];

  const formatDate = (dateString) => {
    return new Date(dateString)?.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleAddNote = () => {
    if (newNote?.trim()) {
      const note = {
        id: Date.now(),
        tipo: noteType,
        contenido: newNote?.trim(),
        fecha: new Date()?.toISOString(),
        dentista: 'Dr. García'
      };
      
      onAddNote(note);
      setNewNote('');
      setNoteType('general');
    }
  };

  const handleEditNote = (note) => {
    setEditingNote({ ...note });
  };

  const handleUpdateNote = () => {
    if (editingNote && editingNote?.contenido?.trim()) {
      onUpdateNote(editingNote);
      setEditingNote(null);
    }
  };

  const handleCancelEdit = () => {
    setEditingNote(null);
  };

  const getNoteTypeInfo = (type) => {
    return noteTypes?.find(t => t?.value === type) || noteTypes?.[0];
  };

  const mockNotes = patient?.notas_clinicas || [
    {
      id: 1,
      tipo: 'diagnostico',
      contenido: `Paciente presenta caries en diente 16 (molar superior derecho). Se observa cavidad de tamaño medio en superficie oclusal.\n\nRecomendación: Obturación con resina compuesta. Programar cita para tratamiento.`,
      fecha: '2024-12-10T10:30:00.000Z',
      dentista: 'Dr. García'
    },
    {
      id: 2,
      tipo: 'tratamiento',
      contenido: `Realizada obturación en diente 16 con resina compuesta A2.\n\nProcedimiento sin complicaciones. Paciente tolera bien el tratamiento.\n\nIndicaciones post-operatorias entregadas.`,
      fecha: '2024-12-08T14:15:00.000Z',
      dentista: 'Dr. García'
    },
    {
      id: 3,
      tipo: 'seguimiento',
      contenido: `Control post-operatorio diente 16. Obturación en buen estado, sin sensibilidad.\n\nPaciente refiere comodidad al masticar. Próximo control en 6 meses.`,
      fecha: '2024-12-05T09:45:00.000Z',
      dentista: 'Dr. García'
    }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Icon name="FileText" size={20} color="var(--color-primary)" />
          <div>
            <h3 className="text-lg font-semibold text-card-foreground">
              Notas Clínicas
            </h3>
            {patient && (
              <p className="text-sm text-muted-foreground">
                {patient?.nombre} {patient?.apellido}
              </p>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className="text-xs text-muted-foreground">
            {mockNotes?.length} notas registradas
          </span>
        </div>
      </div>
      {/* Add New Note */}
      <div className="mb-6 p-4 bg-muted/20 rounded-lg">
        <h4 className="text-sm font-medium text-card-foreground mb-3">
          Agregar Nueva Nota
        </h4>
        
        {/* Note Type Selection */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-4">
          {noteTypes?.map((type) => (
            <Button
              key={type?.value}
              variant={noteType === type?.value ? 'default' : 'outline'}
              size="sm"
              iconName={type?.icon}
              iconPosition="left"
              iconSize={14}
              onClick={() => setNoteType(type?.value)}
              className="justify-start"
            >
              {type?.label}
            </Button>
          ))}
        </div>

        {/* Note Content */}
        <div className="space-y-3">
          <textarea
            value={newNote}
            onChange={(e) => setNewNote(e?.target?.value)}
            placeholder="Escriba su nota clínica aquí..."
            className="w-full h-24 px-3 py-2 bg-input border border-border rounded-md text-sm text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
          />
          
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">
              {newNote?.length}/500 caracteres
            </span>
            <Button
              variant="default"
              size="sm"
              iconName="Plus"
              iconPosition="left"
              iconSize={14}
              onClick={handleAddNote}
              disabled={!newNote?.trim()}
            >
              Agregar Nota
            </Button>
          </div>
        </div>
      </div>
      {/* Notes List */}
      <div className="space-y-4">
        <h4 className="text-sm font-medium text-card-foreground">
          Historial de Notas
        </h4>
        
        {mockNotes?.length === 0 ? (
          <div className="text-center py-8">
            <Icon name="FileText" size={48} color="var(--color-muted-foreground)" className="mx-auto mb-3 opacity-50" />
            <p className="text-sm text-muted-foreground">
              No hay notas clínicas registradas
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {mockNotes?.map((note) => {
              const typeInfo = getNoteTypeInfo(note?.tipo);
              const isEditing = editingNote?.id === note?.id;
              
              return (
                <div key={note?.id} className="p-4 bg-muted/10 border border-border rounded-lg">
                  {/* Note Header */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <Icon 
                        name={typeInfo?.icon} 
                        size={16} 
                        className={typeInfo?.color}
                      />
                      <span className={`text-sm font-medium ${typeInfo?.color}`}>
                        {typeInfo?.label}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        • {formatDate(note?.fecha)}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-muted-foreground">
                        {note?.dentista}
                      </span>
                      {!isEditing && (
                        <Button
                          variant="ghost"
                          size="xs"
                          iconName="Edit"
                          onClick={() => handleEditNote(note)}
                        />
                      )}
                    </div>
                  </div>
                  {/* Note Content */}
                  {isEditing ? (
                    <div className="space-y-3">
                      <textarea
                        value={editingNote?.contenido}
                        onChange={(e) => setEditingNote({
                          ...editingNote,
                          contenido: e?.target?.value
                        })}
                        className="w-full h-24 px-3 py-2 bg-input border border-border rounded-md text-sm text-foreground resize-none focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
                      />
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="default"
                          size="xs"
                          iconName="Check"
                          iconPosition="left"
                          iconSize={12}
                          onClick={handleUpdateNote}
                        >
                          Guardar
                        </Button>
                        <Button
                          variant="ghost"
                          size="xs"
                          onClick={handleCancelEdit}
                        >
                          Cancelar
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="text-sm text-card-foreground whitespace-pre-line">
                      {note?.contenido}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientNotes;