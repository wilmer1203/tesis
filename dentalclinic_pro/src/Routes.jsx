import React from "react";
import { BrowserRouter, Routes as RouterRoutes, Route } from "react-router-dom";
import ScrollToTop from "components/ScrollToTop";
import ErrorBoundary from "components/ErrorBoundary";
import NotFound from "pages/NotFound";
import ManagerDashboard from './pages/manager-dashboard';
import PatientManagement from './pages/patient-management';
import SecretaryDashboard from './pages/secretary-dashboard';
import AppointmentScheduling from './pages/appointment-scheduling';
import DentistDashboard from './pages/dentist-dashboard';
import PaymentProcessing from './pages/payment-processing';
import PatientTreatmentInterface from './pages/patient-treatment-interface';

const Routes = () => {
  return (
    <BrowserRouter>
      <ErrorBoundary>
      <ScrollToTop />
      <RouterRoutes>
        {/* Define your route here */}
        <Route path="/" element={<AppointmentScheduling />} />
        <Route path="/manager-dashboard" element={<ManagerDashboard />} />
        <Route path="/patient-management" element={<PatientManagement />} />
        <Route path="/secretary-dashboard" element={<SecretaryDashboard />} />
        <Route path="/appointment-scheduling" element={<AppointmentScheduling />} />
        <Route path="/dentist-dashboard" element={<DentistDashboard />} />
        <Route path="/payment-processing" element={<PaymentProcessing />} />
        <Route path="/patient-treatment-interface" element={<PatientTreatmentInterface />} />
        <Route path="*" element={<NotFound />} />
      </RouterRoutes>
      </ErrorBoundary>
    </BrowserRouter>
  );
};

export default Routes;