import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ReceiptGenerator = ({ 
  consultation, 
  paymentData, 
  exchangeRate = 36.45,
  onReceiptGenerated = () => {} 
}) => {
  const [showPreview, setShowPreview] = useState(false);
  const [receiptData, setReceiptData] = useState(null);

  const generateReceipt = () => {
    const receiptNumber = `REC-${new Date()?.getFullYear()}-${String(Math.floor(Math.random() * 9999))?.padStart(4, '0')}`;
    const currentDate = new Date();
    
    const receipt = {
      number: receiptNumber,
      date: currentDate?.toLocaleDateString('es-VE'),
      time: currentDate?.toLocaleTimeString('es-VE'),
      patient: consultation?.patient,
      services: consultation?.services,
      paymentMethods: paymentData?.methods || [],
      amounts: paymentData?.amounts || {},
      exchangeRate,
      totals: calculateTotals(),
      clinic: {
        name: 'DentalFlow Clínica Dental',
        address: 'Av. Principal, Centro Comercial Plaza, Piso 2, Local 15',
        city: 'Caracas, Venezuela',
        phone: '+58 212-555-0123',
        email: 'info@dentalflow.ve',
        rif: 'J-12345678-9'
      }
    };
    
    setReceiptData(receipt);
    setShowPreview(true);
    onReceiptGenerated(receipt);
  };

  const calculateTotals = () => {
    const subtotalBs = consultation?.services?.reduce((sum, service) => sum + service?.priceBs, 0);
    const subtotalUsd = consultation?.services?.reduce((sum, service) => sum + service?.priceUsd, 0);
    const taxBs = subtotalBs * 0.16;
    const taxUsd = subtotalUsd * 0.16;
    
    return {
      subtotalBs,
      subtotalUsd,
      taxBs,
      taxUsd,
      totalBs: subtotalBs + taxBs,
      totalUsd: subtotalUsd + taxUsd
    };
  };

  const handlePrint = () => {
    window.print();
  };

  const handleDownload = () => {
    // Mock PDF download
    const element = document.createElement('a');
    element.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(receiptData, null, 2));
    element.download = `${receiptData?.number}.txt`;
    element?.click();
  };

  const handleEmail = () => {
    const subject = `Recibo de Pago ${receiptData?.number} - DentalFlow`;
    const body = `Estimado/a ${consultation?.patient?.name},\n\nAdjunto encontrará su recibo de pago por los servicios dentales recibidos.\n\nGracias por confiar en DentalFlow.`;
    
    window.open(`mailto:${consultation?.patient?.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`);
  };

  if (!showPreview) {
    return (
      <div className="bg-card border border-border rounded-lg p-6 shadow-soft">
        <div className="flex items-center space-x-2 mb-6">
          <Icon name="Receipt" size={24} className="text-primary" />
          <h2 className="text-xl font-semibold text-foreground">Generar Recibo</h2>
        </div>

        <div className="text-center py-8">
          <Icon name="FileText" size={64} className="text-muted-foreground mx-auto mb-4" />
          <p className="text-muted-foreground mb-6">
            Genere el recibo oficial de pago para el paciente
          </p>
          
          <Button 
            onClick={generateReceipt}
            iconName="Plus"
            size="lg"
          >
            Generar Recibo
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg shadow-soft">
      {/* Header Actions */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center space-x-2">
          <Icon name="Receipt" size={24} className="text-primary" />
          <h2 className="text-xl font-semibold text-foreground">Recibo de Pago</h2>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={handlePrint} iconName="Printer">
            Imprimir
          </Button>
          <Button variant="outline" size="sm" onClick={handleDownload} iconName="Download">
            Descargar
          </Button>
          <Button variant="outline" size="sm" onClick={handleEmail} iconName="Mail">
            Enviar Email
          </Button>
          <button
            onClick={() => setShowPreview(false)}
            className="p-2 hover:bg-muted rounded-md transition-smooth"
          >
            <Icon name="X" size={16} className="text-muted-foreground" />
          </button>
        </div>
      </div>
      {/* Receipt Content */}
      <div className="p-6 max-h-96 overflow-y-auto" id="receipt-content">
        {/* Clinic Header */}
        <div className="text-center mb-6 border-b border-border pb-4">
          <div className="flex items-center justify-center space-x-2 mb-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Icon name="Tooth" size={20} color="white" />
            </div>
            <h1 className="text-2xl font-bold text-foreground">{receiptData?.clinic?.name}</h1>
          </div>
          <div className="text-sm text-muted-foreground space-y-1">
            <p>{receiptData?.clinic?.address}</p>
            <p>{receiptData?.clinic?.city}</p>
            <p>Tel: {receiptData?.clinic?.phone} • Email: {receiptData?.clinic?.email}</p>
            <p>RIF: {receiptData?.clinic?.rif}</p>
          </div>
        </div>

        {/* Receipt Info */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-2">Información del Recibo</h3>
            <div className="text-sm space-y-1">
              <p><span className="text-muted-foreground">Número:</span> <span className="font-mono">{receiptData?.number}</span></p>
              <p><span className="text-muted-foreground">Fecha:</span> {receiptData?.date}</p>
              <p><span className="text-muted-foreground">Hora:</span> {receiptData?.time}</p>
            </div>
          </div>
          
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-2">Información del Paciente</h3>
            <div className="text-sm space-y-1">
              <p><span className="text-muted-foreground">Nombre:</span> {receiptData?.patient?.name}</p>
              <p><span className="text-muted-foreground">ID:</span> <span className="font-mono">{receiptData?.patient?.id}</span></p>
              <p><span className="text-muted-foreground">Teléfono:</span> {receiptData?.patient?.phone}</p>
            </div>
          </div>
        </div>

        {/* Services Table */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-foreground mb-3">Servicios Realizados</h3>
          <div className="border border-border rounded-md overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-muted">
                <tr>
                  <th className="text-left p-3 text-foreground">Servicio</th>
                  <th className="text-left p-3 text-foreground">Dentista</th>
                  <th className="text-right p-3 text-foreground">Precio Bs</th>
                  <th className="text-right p-3 text-foreground">Precio USD</th>
                </tr>
              </thead>
              <tbody>
                {receiptData?.services?.map((service, index) => (
                  <tr key={index} className="border-t border-border">
                    <td className="p-3 text-foreground">{service?.name}</td>
                    <td className="p-3 text-muted-foreground">Dr. {service?.dentist}</td>
                    <td className="p-3 text-right font-mono text-foreground">
                      {service?.priceBs?.toLocaleString('es-VE')} Bs
                    </td>
                    <td className="p-3 text-right font-mono text-foreground">
                      ${service?.priceUsd?.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Payment Methods */}
        {receiptData?.paymentMethods?.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-foreground mb-3">Métodos de Pago</h3>
            <div className="bg-muted rounded-md p-3 space-y-2">
              {receiptData?.paymentMethods?.map((method, index) => (
                <div key={index} className="flex justify-between text-sm">
                  <span className="text-muted-foreground">{method?.name}:</span>
                  <span className="font-mono text-foreground">
                    {method?.currency === 'USD' ? '$' : ''}{method?.amount?.toLocaleString('es-VE')} {method?.currency}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Totals */}
        <div className="border-t border-border pt-4">
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Subtotal:</span>
              <div className="text-right">
                <div className="text-foreground">{receiptData?.totals?.subtotalBs?.toLocaleString('es-VE')} Bs</div>
                <div className="text-muted-foreground">${receiptData?.totals?.subtotalUsd?.toFixed(2)} USD</div>
              </div>
            </div>
            
            <div className="flex justify-between">
              <span className="text-muted-foreground">IVA (16%):</span>
              <div className="text-right">
                <div className="text-foreground">{receiptData?.totals?.taxBs?.toLocaleString('es-VE')} Bs</div>
                <div className="text-muted-foreground">${receiptData?.totals?.taxUsd?.toFixed(2)} USD</div>
              </div>
            </div>
            
            <div className="flex justify-between text-lg font-semibold border-t border-border pt-2">
              <span className="text-foreground">Total Pagado:</span>
              <div className="text-right">
                <div className="text-primary">{receiptData?.totals?.totalBs?.toLocaleString('es-VE')} Bs</div>
                <div className="text-primary">${receiptData?.totals?.totalUsd?.toFixed(2)} USD</div>
              </div>
            </div>
          </div>
        </div>

        {/* Exchange Rate */}
        <div className="mt-4 text-xs text-muted-foreground text-center">
          <p>Tasa de cambio utilizada: 1 USD = {receiptData?.exchangeRate?.toFixed(2)} Bs</p>
          <p>Fecha de generación: {new Date()?.toLocaleString('es-VE')}</p>
        </div>

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-border text-center text-xs text-muted-foreground">
          <p>Gracias por confiar en DentalFlow</p>
          <p>Este recibo es válido como comprobante de pago</p>
        </div>
      </div>
    </div>
  );
};

export default ReceiptGenerator;