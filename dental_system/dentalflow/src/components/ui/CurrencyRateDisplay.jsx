import React, { useState, useEffect } from 'react';
import Icon from '../AppIcon';

const CurrencyRateDisplay = ({ 
  compact = false, 
  showHistory = true,
  className = '' 
}) => {
  const [rateData, setRateData] = useState({
    usdToVes: 36.45,
    vesToUsd: 0.0274,
    lastUpdate: new Date(),
    trend: 'up', // up, down, stable
    change24h: 0.12,
    changePercent: 0.33
  });
  
  const [showDetails, setShowDetails] = useState(false);
  const [rateHistory, setRateHistory] = useState([
    { time: '09:00', rate: 36.33 },
    { time: '12:00', rate: 36.41 },
    { time: '15:00', rate: 36.45 },
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setRateData(prev => {
        const change = (Math.random() - 0.5) * 0.2;
        const newRate = Math.max(30, prev?.usdToVes + change);
        const trend = change > 0.05 ? 'up' : change < -0.05 ? 'down' : 'stable';
        
        return {
          ...prev,
          usdToVes: newRate,
          vesToUsd: 1 / newRate,
          lastUpdate: new Date(),
          trend,
          change24h: prev?.change24h + change,
          changePercent: ((prev?.change24h + change) / prev?.usdToVes) * 100
        };
      });

      // Update history every hour
      const now = new Date();
      if (now?.getMinutes() === 0) {
        setRateHistory(prev => [
          ...prev?.slice(-5),
          { 
            time: now?.toLocaleTimeString('es-VE', { hour: '2-digit', minute: '2-digit' }), 
            rate: rateData?.usdToVes 
          }
        ]);
      }
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, [rateData?.usdToVes]);

  const getTrendIcon = () => {
    switch (rateData?.trend) {
      case 'up':
        return { icon: 'TrendingUp', color: 'text-success' };
      case 'down':
        return { icon: 'TrendingDown', color: 'text-error' };
      default:
        return { icon: 'Minus', color: 'text-muted-foreground' };
    }
  };

  const trendConfig = getTrendIcon();

  if (compact) {
    return (
      <div className={`relative ${className}`}>
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="flex items-center space-x-2 px-3 py-2 text-sm text-muted-foreground hover:text-foreground transition-smooth"
          title="Tasa de cambio actual"
        >
          <Icon name="DollarSign" size={14} />
          <span className="font-mono">{rateData?.usdToVes?.toFixed(2)} Bs</span>
          <Icon name={trendConfig?.icon} size={12} className={trendConfig?.color} />
        </button>
        {showDetails && (
          <div className="absolute right-0 top-full mt-2 w-80 bg-popover border border-border rounded-md shadow-modal p-4 z-30">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-foreground">Tasa de Cambio</h3>
                <button
                  onClick={() => setShowDetails(false)}
                  className="p-1 hover:bg-muted rounded transition-smooth"
                >
                  <Icon name="X" size={14} className="text-muted-foreground" />
                </button>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-muted rounded-md p-3">
                  <div className="text-xs text-muted-foreground mb-1">USD → VES</div>
                  <div className="text-lg font-mono font-semibold text-foreground">
                    {rateData?.usdToVes?.toFixed(2)} Bs
                  </div>
                </div>
                <div className="bg-muted rounded-md p-3">
                  <div className="text-xs text-muted-foreground mb-1">VES → USD</div>
                  <div className="text-lg font-mono font-semibold text-foreground">
                    ${rateData?.vesToUsd?.toFixed(4)}
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <Icon name={trendConfig?.icon} size={16} className={trendConfig?.color} />
                  <span className={`font-medium ${trendConfig?.color}`}>
                    {rateData?.change24h >= 0 ? '+' : ''}{rateData?.change24h?.toFixed(2)} Bs
                  </span>
                  <span className={`text-xs ${trendConfig?.color}`}>
                    ({rateData?.changePercent >= 0 ? '+' : ''}{rateData?.changePercent?.toFixed(2)}%)
                  </span>
                </div>
                <span className="text-xs text-muted-foreground">24h</span>
              </div>

              {showHistory && rateHistory?.length > 0 && (
                <div className="border-t border-border pt-3">
                  <div className="text-xs text-muted-foreground mb-2">Historial Reciente</div>
                  <div className="space-y-1">
                    {rateHistory?.slice(-3)?.map((entry, index) => (
                      <div key={index} className="flex justify-between text-xs">
                        <span className="text-muted-foreground">{entry?.time}</span>
                        <span className="font-mono text-foreground">{entry?.rate?.toFixed(2)} Bs</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="text-xs text-muted-foreground">
                Actualizado: {rateData?.lastUpdate?.toLocaleTimeString('es-VE')}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={`bg-card border border-border rounded-md p-4 ${className}`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-foreground">Tasa de Cambio</h3>
        <div className="flex items-center space-x-1">
          <Icon name={trendConfig?.icon} size={16} className={trendConfig?.color} />
          <span className={`text-sm font-medium ${trendConfig?.color}`}>
            {rateData?.changePercent >= 0 ? '+' : ''}{rateData?.changePercent?.toFixed(2)}%
          </span>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="text-center">
          <div className="text-xs text-muted-foreground mb-1">USD → VES</div>
          <div className="text-2xl font-mono font-bold text-foreground">
            {rateData?.usdToVes?.toFixed(2)}
          </div>
          <div className="text-xs text-muted-foreground">Bolívares</div>
        </div>
        <div className="text-center">
          <div className="text-xs text-muted-foreground mb-1">VES → USD</div>
          <div className="text-2xl font-mono font-bold text-foreground">
            {rateData?.vesToUsd?.toFixed(4)}
          </div>
          <div className="text-xs text-muted-foreground">Dólares</div>
        </div>
      </div>
      <div className="flex items-center justify-between text-sm border-t border-border pt-3">
        <div className="flex items-center space-x-2">
          <span className="text-muted-foreground">Cambio 24h:</span>
          <span className={`font-medium ${trendConfig?.color}`}>
            {rateData?.change24h >= 0 ? '+' : ''}{rateData?.change24h?.toFixed(2)} Bs
          </span>
        </div>
        <span className="text-xs text-muted-foreground">
          {rateData?.lastUpdate?.toLocaleTimeString('es-VE')}
        </span>
      </div>
      {showHistory && rateHistory?.length > 0 && (
        <div className="mt-4 border-t border-border pt-3">
          <div className="text-xs text-muted-foreground mb-2">Historial del Día</div>
          <div className="space-y-1">
            {rateHistory?.map((entry, index) => (
              <div key={index} className="flex justify-between text-xs">
                <span className="text-muted-foreground">{entry?.time}</span>
                <span className="font-mono text-foreground">{entry?.rate?.toFixed(2)} Bs</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CurrencyRateDisplay;