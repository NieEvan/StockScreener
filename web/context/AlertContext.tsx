'use client';

import { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { Alert } from '../components/AlertsPanel';

interface AlertContextType {
  alerts: Alert[];
  addAlert: (alert: Omit<Alert, 'id' | 'timestamp'>) => void;
  clearAlerts: () => void;
}

const AlertContext = createContext<AlertContextType | undefined>(undefined);

export function AlertProvider({ children }: { children: ReactNode }) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  
  useEffect(() => {
    // Setup WebSocket connection to receive alerts from backend
    const socket = new WebSocket('ws://localhost:8000/ws');
    
    socket.onopen = () => {
      console.log('Connected to alerts websocket');
    };
    
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data) {
          addAlert({
            market: data.market,
            symbol: data.symbol,
            direction: data.direction,
            conditions: data.conditions,
          });
        }
      } catch (error) {
        console.error('Error parsing alert data:', error);
      }
    };
    
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    return () => {
      socket.close();
    };
  }, []);
  
  // Add a new alert to the list
  const addAlert = (alertData: Omit<Alert, 'id' | 'timestamp'>) => {
    const newAlert: Alert = {
      id: Date.now().toString(),
      ...alertData,
      timestamp: new Date().toLocaleString(),
    };
    
    setAlerts(prevAlerts => [newAlert, ...prevAlerts].slice(0, 100)); // Keep last 100 alerts
  };
  
  // Clear all alerts
  const clearAlerts = () => {
    setAlerts([]);
  };
  
  return (
    <AlertContext.Provider value={{ alerts, addAlert, clearAlerts }}>
      {children}
    </AlertContext.Provider>
  );
}

export function useAlerts() {
  const context = useContext(AlertContext);
  if (context === undefined) {
    throw new Error('useAlerts must be used within an AlertProvider');
  }
  return context;
} 