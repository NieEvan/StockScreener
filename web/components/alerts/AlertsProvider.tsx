'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { Alert } from './AlertTypes';

interface AlertsContextType {
  alerts: Alert[];
  loading: boolean;
  error: string | null;
}

const AlertsContext = createContext<AlertsContextType | undefined>(undefined);

export function useAlerts() {
  const context = useContext(AlertsContext);
  if (context === undefined) {
    throw new Error('useAlerts must be used within an AlertsProvider');
  }
  return context;
}

interface AlertsProviderProps {
  children: ReactNode;
}

export function AlertsProvider({ children }: AlertsProviderProps) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Mock initial alerts for demo purposes
    const mockAlerts: Alert[] = Array.from({ length: 25 }).map((_, index) => {
      const symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'];
      const markets = ['FOREX1MB', 'FOREX5MB', 'FOREX1HS', 'FOREX4HS'];
      const directions = ['买入', '卖出'];
      const conditions = [
        'Breakout detected',
        'Support level reached',
        'Resistance broken',
        'Moving average crossover',
        'RSI oversold',
        'RSI overbought'
      ];
      
      return {
        id: (index + 1).toString(),
        market: markets[Math.floor(Math.random() * markets.length)],
        symbol: symbols[Math.floor(Math.random() * symbols.length)],
        direction: directions[Math.floor(Math.random() * directions.length)],
        conditions: conditions[Math.floor(Math.random() * conditions.length)],
        timestamp: new Date(Date.now() - Math.floor(Math.random() * 86400000)).toLocaleString(),
      };
    });
    
    setAlerts(mockAlerts);
    setLoading(false);
    
    // Setup WebSocket connection to receive alerts from backend
    const socket = new WebSocket('ws://localhost:8000/ws');
    
    socket.onopen = () => {
      console.log('Connected to alerts websocket');
    };
    
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data) {
          setAlerts(prev => [
            {
              id: Date.now().toString(),
              ...data,
              timestamp: new Date().toLocaleString()
            },
            ...prev
          ].slice(0, 100)); // Keep last 100 alerts
        }
      } catch (error) {
        console.error('Error parsing alert data:', error);
        setError('Failed to parse alert data');
      }
    };
    
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('WebSocket connection error');
    };
    
    return () => {
      socket.close();
    };
  }, []);

  const value = { alerts, loading, error };
  
  return (
    <AlertsContext.Provider value={value}>
      {children}
    </AlertsContext.Provider>
  );
} 