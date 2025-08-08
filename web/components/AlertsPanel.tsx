'use client';

import { AlertsProvider } from './alerts/AlertsProvider';
import AlertsPanel from './alerts/AlertsPanel';

export default function AlertsPanelWrapper() {
  return (
    <AlertsProvider>
      <AlertsPanel />
    </AlertsProvider>
  );
} 