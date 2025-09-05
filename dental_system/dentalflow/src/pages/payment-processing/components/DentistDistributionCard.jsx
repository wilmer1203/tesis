import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const DentistDistributionCard = ({ 
  consultation, 
  onDistributionChange = () => {} 
}) => {
  const [customDistribution, setCustomDistribution] = useState(false);
  const [distributions, setDistributions] = useState({});

  const calculateAutoDistribution = () => {
    const dentistServices = {};
    
    consultation?.services?.forEach(service => {
      if (!dentistServices?.[service?.dentist]) {
        dentistServices[service.dentist] = {
          services: [],
          totalBs: 0,
          totalUsd: 0
        };
      }
      
      dentistServices?.[service?.dentist]?.services?.push(service);
      dentistServices[service.dentist].totalBs += service?.priceBs;
      dentistServices[service.dentist].totalUsd += service?.priceUsd;
    });

    return dentistServices;
  };

  const autoDistribution = calculateAutoDistribution();
  const totalBs = Object.values(autoDistribution)?.reduce((sum, dentist) => sum + dentist?.totalBs, 0);
  const totalUsd = Object.values(autoDistribution)?.reduce((sum, dentist) => sum + dentist?.totalUsd, 0);

  const handleCustomDistributionToggle = () => {
    setCustomDistribution(!customDistribution);
    if (!customDistribution) {
      // Initialize custom distribution with auto values
      const initialDistribution = {};
      Object.keys(autoDistribution)?.forEach(dentist => {
        initialDistribution[dentist] = {
          percentageBs: (autoDistribution?.[dentist]?.totalBs / totalBs) * 100,
          percentageUsd: (autoDistribution?.[dentist]?.totalUsd / totalUsd) * 100,
          amountBs: autoDistribution?.[dentist]?.totalBs,
          amountUsd: autoDistribution?.[dentist]?.totalUsd
        };
      });
      setDistributions(initialDistribution);
    }
  };

  const handlePercentageChange = (dentist, currency, percentage) => {
    const newDistributions = { ...distributions };
    const total = currency === 'Bs' ? totalBs : totalUsd;
    
    newDistributions[dentist] = {
      ...newDistributions?.[dentist],
      [`percentage${currency}`]: percentage,
      [`amount${currency}`]: (total * percentage) / 100
    };
    
    setDistributions(newDistributions);
    onDistributionChange(newDistributions);
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <Icon name="Users" size={24} className="text-primary" />
          <h2 className="text-xl font-semibold text-foreground">Distribución por Dentista</h2>
        </div>
        
        <Button
          variant={customDistribution ? "default" : "outline"}
          size="sm"
          onClick={handleCustomDistributionToggle}
          iconName={customDistribution ? "Calculator" : "Edit"}
        >
          {customDistribution ? "Automática" : "Personalizar"}
        </Button>
      </div>
      <div className="space-y-4">
        {Object.entries(autoDistribution)?.map(([dentist, data]) => (
          <div key={dentist} className="border border-border rounded-md p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                  <Icon name="UserCheck" size={20} className="text-primary" />
                </div>
                <div>
                  <div className="font-medium text-foreground">Dr. {dentist}</div>
                  <div className="text-sm text-muted-foreground">
                    {data?.services?.length} servicio{data?.services?.length !== 1 ? 's' : ''}
                  </div>
                </div>
              </div>
              
              {!customDistribution && (
                <div className="text-right">
                  <div className="text-sm font-medium text-foreground">
                    {data?.totalBs?.toLocaleString('es-VE')} Bs
                  </div>
                  <div className="text-sm text-muted-foreground">
                    ${data?.totalUsd?.toFixed(2)} USD
                  </div>
                </div>
              )}
            </div>

            {/* Services List */}
            <div className="space-y-2 mb-4">
              {data?.services?.map((service, index) => (
                <div key={index} className="flex items-center justify-between text-sm bg-muted rounded p-2">
                  <div className="flex items-center space-x-2">
                    <Icon name="Tooth" size={14} className="text-primary" />
                    <span className="text-foreground">{service?.name}</span>
                    <span className="text-muted-foreground">• Pieza {service?.tooth}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-foreground">{service?.priceBs?.toLocaleString('es-VE')} Bs</div>
                    <div className="text-muted-foreground">${service?.priceUsd?.toFixed(2)} USD</div>
                  </div>
                </div>
              ))}
            </div>

            {customDistribution && (
              <div className="grid grid-cols-2 gap-4 border-t border-border pt-3">
                <div>
                  <label className="text-xs text-muted-foreground">Porcentaje Bolívares</label>
                  <div className="flex items-center space-x-2 mt-1">
                    <input
                      type="number"
                      min="0"
                      max="100"
                      step="0.1"
                      value={distributions?.[dentist]?.percentageBs || 0}
                      onChange={(e) => handlePercentageChange(dentist, 'Bs', parseFloat(e?.target?.value) || 0)}
                      className="w-20 px-2 py-1 text-sm border border-border rounded"
                    />
                    <span className="text-sm text-muted-foreground">%</span>
                    <span className="text-sm font-medium text-foreground">
                      {(distributions?.[dentist]?.amountBs || 0)?.toLocaleString('es-VE')} Bs
                    </span>
                  </div>
                </div>
                
                <div>
                  <label className="text-xs text-muted-foreground">Porcentaje USD</label>
                  <div className="flex items-center space-x-2 mt-1">
                    <input
                      type="number"
                      min="0"
                      max="100"
                      step="0.1"
                      value={distributions?.[dentist]?.percentageUsd || 0}
                      onChange={(e) => handlePercentageChange(dentist, 'Usd', parseFloat(e?.target?.value) || 0)}
                      className="w-20 px-2 py-1 text-sm border border-border rounded"
                    />
                    <span className="text-sm text-muted-foreground">%</span>
                    <span className="text-sm font-medium text-foreground">
                      ${(distributions?.[dentist]?.amountUsd || 0)?.toFixed(2)} USD
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Commission Info */}
            <div className="bg-muted/50 rounded p-2 mt-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-muted-foreground">Comisión Clínica (15%):</span>
                <div className="text-right">
                  <div className="text-muted-foreground">
                    {(data?.totalBs * 0.15)?.toLocaleString('es-VE')} Bs
                  </div>
                  <div className="text-muted-foreground">
                    ${(data?.totalUsd * 0.15)?.toFixed(2)} USD
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between text-xs mt-1">
                <span className="text-foreground font-medium">Neto para Dentista:</span>
                <div className="text-right">
                  <div className="text-success font-medium">
                    {(data?.totalBs * 0.85)?.toLocaleString('es-VE')} Bs
                  </div>
                  <div className="text-success font-medium">
                    ${(data?.totalUsd * 0.85)?.toFixed(2)} USD
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      {/* Total Summary */}
      <div className="border-t border-border pt-4 mt-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-foreground">Total Distribución:</span>
          <div className="text-right">
            <div className="text-lg font-semibold text-primary">
              {totalBs?.toLocaleString('es-VE')} Bs
            </div>
            <div className="text-lg font-semibold text-primary">
              ${totalUsd?.toFixed(2)} USD
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DentistDistributionCard;