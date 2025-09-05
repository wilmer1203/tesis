import React, { useState, useRef } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Image from '../../../components/AppImage';

const PhotoUploadPanel = ({ patientId, onPhotoUpload }) => {
  const [photos, setPhotos] = useState([
    {
      id: 1,
      type: 'before',
      url: 'https://images.pexels.com/photos/3845810/pexels-photo-3845810.jpeg?w=300&h=300&fit=crop',
      timestamp: new Date(Date.now() - 3600000),
      procedure: 'Limpieza Dental',
      tooth: '11-18',
      notes: 'Estado inicial antes de la limpieza'
    },
    {
      id: 2,
      type: 'after',
      url: 'https://images.pexels.com/photos/3845811/pexels-photo-3845811.jpeg?w=300&h=300&fit=crop',
      timestamp: new Date(Date.now() - 1800000),
      procedure: 'Limpieza Dental',
      tooth: '11-18',
      notes: 'Resultado después de la limpieza completa'
    },
    {
      id: 3,
      type: 'during',
      url: 'https://images.pexels.com/photos/3845812/pexels-photo-3845812.jpeg?w=300&h=300&fit=crop',
      timestamp: new Date(Date.now() - 900000),
      procedure: 'Obturación',
      tooth: '16',
      notes: 'Proceso de obturación en molar superior'
    }
  ]);

  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [uploadMode, setUploadMode] = useState(false);
  const [newPhotoData, setNewPhotoData] = useState({
    type: 'before',
    procedure: '',
    tooth: '',
    notes: ''
  });

  const fileInputRef = useRef(null);

  const photoTypes = [
    { value: 'before', label: 'Antes', color: 'text-warning bg-warning/10' },
    { value: 'during', label: 'Durante', color: 'text-primary bg-primary/10' },
    { value: 'after', label: 'Después', color: 'text-success bg-success/10' },
    { value: 'xray', label: 'Radiografía', color: 'text-secondary bg-secondary/10' },
    { value: 'clinical', label: 'Clínica', color: 'text-accent bg-accent/10' }
  ];

  const procedures = [
    'Limpieza Dental',
    'Obturación',
    'Extracción',
    'Endodoncia',
    'Corona',
    'Implante',
    'Blanqueamiento',
    'Ortodoncia',
    'Cirugía Oral',
    'Prótesis'
  ];

  const handleFileSelect = (event) => {
    const file = event?.target?.files?.[0];
    if (file) {
      // In a real app, you would upload to a server
      const mockUrl = URL.createObjectURL(file);
      const newPhoto = {
        id: Date.now(),
        type: newPhotoData?.type,
        url: mockUrl,
        timestamp: new Date(),
        procedure: newPhotoData?.procedure,
        tooth: newPhotoData?.tooth,
        notes: newPhotoData?.notes,
        file: file
      };

      setPhotos(prev => [...prev, newPhoto]);
      setUploadMode(false);
      setNewPhotoData({
        type: 'before',
        procedure: '',
        tooth: '',
        notes: ''
      });

      if (onPhotoUpload) {
        onPhotoUpload(newPhoto);
      }
    }
  };

  const handleDeletePhoto = (photoId) => {
    setPhotos(prev => prev?.filter(p => p?.id !== photoId));
    if (selectedPhoto === photoId) {
      setSelectedPhoto(null);
    }
  };

  const getTypeConfig = (type) => {
    return photoTypes?.find(t => t?.value === type) || photoTypes?.[0];
  };

  const groupedPhotos = photos?.reduce((groups, photo) => {
    const key = photo?.procedure || 'General';
    if (!groups?.[key]) {
      groups[key] = [];
    }
    groups?.[key]?.push(photo);
    return groups;
  }, {});

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-3">
          <Icon name="Camera" size={20} className="text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Fotografías del Tratamiento</h2>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-sm text-muted-foreground">
            {photos?.length} foto{photos?.length !== 1 ? 's' : ''}
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setUploadMode(!uploadMode)}
          >
            <Icon name="Plus" size={16} className="mr-2" />
            Agregar Foto
          </Button>
        </div>
      </div>
      <div className="p-4 space-y-4">
        {/* Upload Panel */}
        {uploadMode && (
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
            <h3 className="text-md font-semibold text-foreground mb-4 flex items-center">
              <Icon name="Upload" size={16} className="mr-2 text-primary" />
              Subir Nueva Fotografía
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Tipo de Fotografía
                </label>
                <select
                  value={newPhotoData?.type}
                  onChange={(e) => setNewPhotoData(prev => ({ ...prev, type: e?.target?.value }))}
                  className="w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:ring-2 focus:ring-ring focus:border-transparent"
                >
                  {photoTypes?.map(type => (
                    <option key={type?.value} value={type?.value}>
                      {type?.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Procedimiento
                </label>
                <select
                  value={newPhotoData?.procedure}
                  onChange={(e) => setNewPhotoData(prev => ({ ...prev, procedure: e?.target?.value }))}
                  className="w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:ring-2 focus:ring-ring focus:border-transparent"
                >
                  <option value="">Seleccionar procedimiento</option>
                  {procedures?.map(procedure => (
                    <option key={procedure} value={procedure}>
                      {procedure}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Diente/Área
                </label>
                <input
                  type="text"
                  value={newPhotoData?.tooth}
                  onChange={(e) => setNewPhotoData(prev => ({ ...prev, tooth: e?.target?.value }))}
                  placeholder="Ej: 16, 11-18, General"
                  className="w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:ring-2 focus:ring-ring focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Notas
                </label>
                <input
                  type="text"
                  value={newPhotoData?.notes}
                  onChange={(e) => setNewPhotoData(prev => ({ ...prev, notes: e?.target?.value }))}
                  placeholder="Descripción de la fotografía"
                  className="w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:ring-2 focus:ring-ring focus:border-transparent"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />
              <Button
                onClick={() => fileInputRef?.current?.click()}
                className="flex-1 mr-2"
              >
                <Icon name="Upload" size={16} className="mr-2" />
                Seleccionar Archivo
              </Button>
              <Button
                variant="ghost"
                onClick={() => setUploadMode(false)}
              >
                Cancelar
              </Button>
            </div>
          </div>
        )}

        {/* Photos by Procedure */}
        <div className="space-y-6">
          {Object.entries(groupedPhotos)?.map(([procedure, procedurePhotos]) => (
            <div key={procedure}>
              <h3 className="text-md font-semibold text-foreground mb-3 flex items-center">
                <Icon name="Folder" size={16} className="mr-2 text-primary" />
                {procedure}
                <span className="ml-2 text-sm text-muted-foreground">
                  ({procedurePhotos?.length} foto{procedurePhotos?.length !== 1 ? 's' : ''})
                </span>
              </h3>

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {procedurePhotos?.map((photo) => {
                  const typeConfig = getTypeConfig(photo?.type);
                  return (
                    <div key={photo?.id} className="relative group">
                      <div className="aspect-square rounded-lg overflow-hidden bg-muted cursor-pointer">
                        <Image
                          src={photo?.url}
                          alt={`${photo?.type} - ${photo?.procedure}`}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                          onClick={() => setSelectedPhoto(selectedPhoto === photo?.id ? null : photo?.id)}
                        />
                      </div>
                      {/* Photo Info Overlay */}
                      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg flex flex-col justify-between p-2">
                        <div className="flex justify-between items-start">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${typeConfig?.color}`}>
                            {typeConfig?.label}
                          </span>
                          <button
                            onClick={() => handleDeletePhoto(photo?.id)}
                            className="p-1 bg-error/80 text-white rounded-full hover:bg-error transition-colors"
                          >
                            <Icon name="Trash2" size={12} />
                          </button>
                        </div>

                        <div className="text-white text-xs">
                          <div className="font-medium">{photo?.tooth}</div>
                          <div className="opacity-80">
                            {photo?.timestamp?.toLocaleTimeString('es-VE', { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </div>
                        </div>
                      </div>
                      {/* Selection Indicator */}
                      {selectedPhoto === photo?.id && (
                        <div className="absolute inset-0 border-4 border-primary rounded-lg pointer-events-none"></div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Selected Photo Details */}
        {selectedPhoto && (
          <div className="bg-muted/30 rounded-lg p-4">
            {(() => {
              const photo = photos?.find(p => p?.id === selectedPhoto);
              if (!photo) return null;
              
              const typeConfig = getTypeConfig(photo?.type);
              return (
                <div>
                  <h3 className="text-md font-semibold text-foreground mb-3 flex items-center">
                    <Icon name="Info" size={16} className="mr-2 text-primary" />
                    Detalles de la Fotografía
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <div>
                        <span className="text-sm text-muted-foreground">Tipo:</span>
                        <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${typeConfig?.color}`}>
                          {typeConfig?.label}
                        </span>
                      </div>
                      <div>
                        <span className="text-sm text-muted-foreground">Procedimiento:</span>
                        <span className="ml-2 text-sm font-medium text-foreground">{photo?.procedure}</span>
                      </div>
                      <div>
                        <span className="text-sm text-muted-foreground">Diente/Área:</span>
                        <span className="ml-2 text-sm font-medium text-foreground">{photo?.tooth}</span>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div>
                        <span className="text-sm text-muted-foreground">Fecha:</span>
                        <span className="ml-2 text-sm font-medium text-foreground">
                          {photo?.timestamp?.toLocaleDateString('es-VE')}
                        </span>
                      </div>
                      <div>
                        <span className="text-sm text-muted-foreground">Hora:</span>
                        <span className="ml-2 text-sm font-medium text-foreground">
                          {photo?.timestamp?.toLocaleTimeString('es-VE')}
                        </span>
                      </div>
                    </div>
                  </div>
                  {photo?.notes && (
                    <div className="mt-3">
                      <span className="text-sm text-muted-foreground">Notas:</span>
                      <p className="mt-1 text-sm text-foreground bg-card rounded p-2">
                        {photo?.notes}
                      </p>
                    </div>
                  )}
                  <div className="flex justify-end space-x-2 mt-4">
                    <Button variant="outline" size="sm">
                      <Icon name="Download" size={14} className="mr-1" />
                      Descargar
                    </Button>
                    <Button variant="outline" size="sm">
                      <Icon name="Share" size={14} className="mr-1" />
                      Compartir
                    </Button>
                  </div>
                </div>
              );
            })()}
          </div>
        )}

        {/* Empty State */}
        {photos?.length === 0 && (
          <div className="text-center py-12">
            <Icon name="Camera" size={48} className="mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium text-foreground mb-2">No hay fotografías</h3>
            <p className="text-muted-foreground mb-4">
              Agrega fotografías del tratamiento para documentar el progreso
            </p>
            <Button onClick={() => setUploadMode(true)}>
              <Icon name="Plus" size={16} className="mr-2" />
              Agregar Primera Foto
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PhotoUploadPanel;