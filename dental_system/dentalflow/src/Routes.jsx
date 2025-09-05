import React from "react";
import { BrowserRouter, Routes as RouterRoutes, Route } from "react-router-dom";
import ScrollToTop from "components/ScrollToTop";
import ErrorBoundary from "components/ErrorBoundary";
import NotFound from "pages/NotFound";
import PatientRegistration from './pages/patient-registration';
import QueueManagementDashboard from './pages/queue-management-dashboard';
import PatientConsultation from './pages/patient-consultation';
import DigitalOdontogramViewer from './pages/digital-odontogram-viewer';
import ReportsDashboard from './pages/reports-dashboard';
import PaymentProcessing from './pages/payment-processing';

const Routes = () => {
  return (
    <BrowserRouter>
      <ErrorBoundary>
      <ScrollToTop />
      <RouterRoutes>
        {/* Define your route here */}
        <Route path="/" element={<DigitalOdontogramViewer />} />
        <Route path="/patient-registration" element={<PatientRegistration />} />
        <Route path="/queue-management-dashboard" element={<QueueManagementDashboard />} />
        <Route path="/patient-consultation" element={<PatientConsultation />} />
        <Route path="/digital-odontogram-viewer" element={<DigitalOdontogramViewer />} />
        <Route path="/reports-dashboard" element={<ReportsDashboard />} />
        <Route path="/payment-processing" element={<PaymentProcessing />} />
        <Route path="*" element={<NotFound />} />
      </RouterRoutes>
      </ErrorBoundary>
    </BrowserRouter>
  );
};

export default Routes;
