import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Icon from '../AppIcon';

const QueueStatusIndicator = ({ className = '' }) => {
  const navigate = useNavigate();
  const [queueData, setQueueData] = useState({
    total: 12,
    waiting: 8,
    inProgress: 3,
    urgent: 2,
    estimated: 25
  });
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setQueueData(prev => ({
        ...prev,
        total: Math.max(0, prev?.total + Math.floor(Math.random() * 3) - 1),
        waiting: Math.max(0, prev?.waiting + Math.floor(Math.random() * 2) - 1),
        inProgress: Math.min(5, Math.max(0, prev?.inProgress + Math.floor(Math.random() * 2) - 1)),
        urgent: Math.max(0, prev?.urgent + Math.floor(Math.random() * 2) - 1),
        estimated: Math.max(10, prev?.estimated + Math.floor(Math.random() * 10) - 5)
      }));
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const handleClick = () => {
    navigate('/queue-management-dashboard');
  };

  const handleDetailsToggle = (e) => {
    e?.stopPropagation();
    setShowDetails(!showDetails);
  };

  return (
    <div className={`relative ${className}`}>
      {/* Desktop View */}
      <button
        onClick={handleClick}
        className="hidden sm:flex items-center space-x-3 px-4 py-2 bg-card border border-border rounded-md hover:bg-muted transition-smooth shadow-soft"
        title="Ver cola de pacientes"
      >
        <div className="flex items-center space-x-2">
          <Icon name="Users" size={16} className="text-primary" />
          <span className="text-sm font-medium text-foreground">{queueData?.total}</span>
        </div>
        
        {queueData?.urgent > 0 && (
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-error rounded-full animate-pulse"></div>
            <span className="text-xs text-error font-medium">{queueData?.urgent}</span>
          </div>
        )}

        <button
          onClick={handleDetailsToggle}
          className="p-1 hover:bg-muted rounded transition-smooth"
        >
          <Icon name="ChevronDown" size={14} className="text-muted-foreground" />
        </button>
      </button>
      {/* Mobile View */}
      <button
        onClick={handleClick}
        className="sm:hidden relative p-2 bg-card border border-border rounded-md hover:bg-muted transition-smooth"
        title="Cola de pacientes"
      >
        <Icon name="Users" size={20} className="text-primary" />
        <div className="absolute -top-1 -right-1 bg-primary text-primary-foreground text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
          {queueData?.total}
        </div>
        {queueData?.urgent > 0 && (
          <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-error rounded-full animate-pulse"></div>
        )}
      </button>
      {/* Details Dropdown */}
      {showDetails && (
        <div className="absolute top-full left-0 mt-2 w-72 bg-popover border border-border rounded-md shadow-modal p-4 z-20">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-foreground">Estado de la Cola</h3>
              <button
                onClick={() => setShowDetails(false)}
                className="p-1 hover:bg-muted rounded transition-smooth"
              >
                <Icon name="X" size={14} className="text-muted-foreground" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-muted rounded-md p-3">
                <div className="flex items-center space-x-2">
                  <Icon name="Clock" size={16} className="text-warning" />
                  <span className="text-xs text-muted-foreground">Esperando</span>
                </div>
                <div className="text-lg font-semibold text-foreground mt-1">{queueData?.waiting}</div>
              </div>

              <div className="bg-muted rounded-md p-3">
                <div className="flex items-center space-x-2">
                  <Icon name="Activity" size={16} className="text-success" />
                  <span className="text-xs text-muted-foreground">En Consulta</span>
                </div>
                <div className="text-lg font-semibold text-foreground mt-1">{queueData?.inProgress}</div>
              </div>

              {queueData?.urgent > 0 && (
                <div className="bg-error/10 rounded-md p-3 col-span-2">
                  <div className="flex items-center space-x-2">
                    <Icon name="AlertTriangle" size={16} className="text-error" />
                    <span className="text-xs text-error font-medium">Casos Urgentes</span>
                  </div>
                  <div className="text-lg font-semibold text-error mt-1">{queueData?.urgent}</div>
                </div>
              )}
            </div>

            <div className="border-t border-border pt-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Tiempo estimado:</span>
                <span className="font-medium text-foreground">{queueData?.estimated} min</span>
              </div>
            </div>

            <button
              onClick={handleClick}
              className="w-full bg-primary text-primary-foreground py-2 px-4 rounded-md text-sm font-medium hover:bg-primary/90 transition-smooth"
            >
              Gestionar Cola
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default QueueStatusIndicator;