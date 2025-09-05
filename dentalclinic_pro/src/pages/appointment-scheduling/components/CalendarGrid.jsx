import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';

const CalendarGrid = ({ 
  viewMode, 
  currentDate, 
  appointments, 
  dentists, 
  selectedDentist,
  onAppointmentClick,
  onTimeSlotClick 
}) => {
  const [draggedAppointment, setDraggedAppointment] = useState(null);

  const timeSlots = Array.from({ length: 12 }, (_, i) => {
    const hour = i + 8; // 8 AM to 7 PM
    return `${hour?.toString()?.padStart(2, '0')}:00`;
  });

  const getAppointmentTypeColor = (type) => {
    const colors = {
      consultation: 'bg-blue-600',
      treatment: 'bg-green-600',
      followup: 'bg-yellow-600',
      emergency: 'bg-red-600',
      cleaning: 'bg-purple-600'
    };
    return colors?.[type] || 'bg-gray-600';
  };

  const getFilteredDentists = () => {
    if (selectedDentist === 'all') return dentists;
    return dentists?.filter(d => d?.id === selectedDentist);
  };

  const getAppointmentsForSlot = (dentistId, timeSlot) => {
    return appointments?.filter(apt => 
      apt?.dentistId === dentistId && 
      apt?.time === timeSlot &&
      apt?.date === currentDate?.toDateString()
    );
  };

  const handleDragStart = (e, appointment) => {
    setDraggedAppointment(appointment);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e) => {
    e?.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e, dentistId, timeSlot) => {
    e?.preventDefault();
    if (draggedAppointment) {
      // Handle appointment move logic here
      console.log('Moving appointment:', draggedAppointment, 'to', dentistId, timeSlot);
      setDraggedAppointment(null);
    }
  };

  const renderDayView = () => {
    const filteredDentists = getFilteredDentists();
    
    return (
      <div className="flex-1 overflow-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 p-4">
          {filteredDentists?.map((dentist) => (
            <div key={dentist?.id} className="bg-card border border-border rounded-lg">
              <div className="p-4 border-b border-border">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
                    <Icon name="User" size={20} color="var(--color-primary-foreground)" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-card-foreground">{dentist?.name}</h3>
                    <p className="text-sm text-muted-foreground">{dentist?.specialty}</p>
                  </div>
                  <div className={`ml-auto w-3 h-3 rounded-full ${dentist?.available ? 'bg-green-500' : 'bg-red-500'}`} />
                </div>
              </div>
              
              <div className="p-2 max-h-96 overflow-y-auto">
                {timeSlots?.map((timeSlot) => {
                  const slotAppointments = getAppointmentsForSlot(dentist?.id, timeSlot);
                  
                  return (
                    <div
                      key={timeSlot}
                      className="flex items-center p-2 border-b border-border/50 hover:bg-muted/50 cursor-pointer"
                      onClick={() => onTimeSlotClick(dentist?.id, timeSlot)}
                      onDragOver={handleDragOver}
                      onDrop={(e) => handleDrop(e, dentist?.id, timeSlot)}
                    >
                      <div className="w-16 text-sm text-muted-foreground font-mono">
                        {timeSlot}
                      </div>
                      <div className="flex-1 ml-3">
                        {slotAppointments?.length > 0 ? (
                          slotAppointments?.map((appointment) => (
                            <div
                              key={appointment?.id}
                              draggable
                              onDragStart={(e) => handleDragStart(e, appointment)}
                              onClick={(e) => {
                                e?.stopPropagation();
                                onAppointmentClick(appointment);
                              }}
                              className={`p-2 rounded-md text-white text-sm cursor-move hover:opacity-80 ${getAppointmentTypeColor(appointment?.type)}`}
                            >
                              <div className="font-medium">{appointment?.patientName}</div>
                              <div className="text-xs opacity-90">{appointment?.service}</div>
                              <div className="text-xs opacity-75">{appointment?.duration} min</div>
                            </div>
                          ))
                        ) : (
                          <div className="text-sm text-muted-foreground italic">
                            Disponible
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderWeekView = () => {
    const filteredDentists = getFilteredDentists();
    const weekDays = Array.from({ length: 7 }, (_, i) => {
      const date = new Date(currentDate);
      const startOfWeek = date?.getDate() - date?.getDay();
      date?.setDate(startOfWeek + i);
      return date;
    });

    return (
      <div className="flex-1 overflow-auto">
        <div className="min-w-full">
          {/* Header */}
          <div className="grid grid-cols-8 border-b border-border bg-surface sticky top-0">
            <div className="p-3 text-sm font-medium text-muted-foreground">
              Horario
            </div>
            {weekDays?.map((day) => (
              <div key={day?.toDateString()} className="p-3 text-center border-l border-border">
                <div className="text-sm font-medium text-foreground">
                  {day?.toLocaleDateString('es-ES', { weekday: 'short' })}
                </div>
                <div className="text-xs text-muted-foreground">
                  {day?.getDate()}
                </div>
              </div>
            ))}
          </div>

          {/* Time slots */}
          {timeSlots?.map((timeSlot) => (
            <div key={timeSlot} className="grid grid-cols-8 border-b border-border/50">
              <div className="p-3 text-sm text-muted-foreground font-mono bg-surface">
                {timeSlot}
              </div>
              {weekDays?.map((day) => (
                <div
                  key={`${day?.toDateString()}-${timeSlot}`}
                  className="p-2 border-l border-border min-h-16 hover:bg-muted/30 cursor-pointer"
                  onClick={() => onTimeSlotClick('all', timeSlot)}
                >
                  {/* Appointments for this day/time would be rendered here */}
                  <div className="space-y-1">
                    {appointments?.filter(apt => apt?.date === day?.toDateString() && apt?.time === timeSlot)?.map((appointment) => (
                        <div
                          key={appointment?.id}
                          className={`p-1 rounded text-xs text-white ${getAppointmentTypeColor(appointment?.type)}`}
                          onClick={(e) => {
                            e?.stopPropagation();
                            onAppointmentClick(appointment);
                          }}
                        >
                          <div className="font-medium truncate">{appointment?.patientName}</div>
                          <div className="truncate opacity-90">{appointment?.service}</div>
                        </div>
                      ))}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderMonthView = () => {
    const year = currentDate?.getFullYear();
    const month = currentDate?.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate?.setDate(startDate?.getDate() - firstDay?.getDay());
    
    const days = [];
    const current = new Date(startDate);
    
    while (current <= lastDay || days?.length < 42) {
      days?.push(new Date(current));
      current?.setDate(current?.getDate() + 1);
    }

    return (
      <div className="flex-1 p-4">
        <div className="grid grid-cols-7 gap-1">
          {['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']?.map((day) => (
            <div key={day} className="p-3 text-center text-sm font-medium text-muted-foreground bg-surface border border-border">
              {day}
            </div>
          ))}
          
          {days?.map((day) => {
            const dayAppointments = appointments?.filter(apt => apt?.date === day?.toDateString());
            const isCurrentMonth = day?.getMonth() === month;
            const isToday = day?.toDateString() === new Date()?.toDateString();
            
            return (
              <div
                key={day?.toDateString()}
                className={`min-h-24 p-2 border border-border cursor-pointer hover:bg-muted/30 ${
                  isCurrentMonth ? 'bg-card' : 'bg-muted/20'
                } ${isToday ? 'ring-2 ring-primary' : ''}`}
                onClick={() => onTimeSlotClick('all', day?.toDateString())}
              >
                <div className={`text-sm font-medium mb-1 ${
                  isCurrentMonth ? 'text-card-foreground' : 'text-muted-foreground'
                }`}>
                  {day?.getDate()}
                </div>
                <div className="space-y-1">
                  {dayAppointments?.slice(0, 3)?.map((appointment) => (
                    <div
                      key={appointment?.id}
                      className={`p-1 rounded text-xs text-white truncate ${getAppointmentTypeColor(appointment?.type)}`}
                      onClick={(e) => {
                        e?.stopPropagation();
                        onAppointmentClick(appointment);
                      }}
                    >
                      {appointment?.patientName}
                    </div>
                  ))}
                  {dayAppointments?.length > 3 && (
                    <div className="text-xs text-muted-foreground">
                      +{dayAppointments?.length - 3} más
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="flex-1 bg-background">
      {viewMode === 'day' && renderDayView()}
      {viewMode === 'week' && renderWeekView()}
      {viewMode === 'month' && renderMonthView()}
    </div>
  );
};

export default CalendarGrid;