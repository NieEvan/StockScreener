'use client';

import { useState, useEffect } from 'react';
import { Card, CardBody, CardHeader, Divider, Spinner } from '@nextui-org/react';

import StockChart from '@/components/StockChart';
import AlertsPanel from '@/components/AlertsPanel';
import SymbolSelector from '@/components/SymbolSelector';
import { fetchChartData, CandleData } from '@/services/chartService';
import { useAlerts } from '@/context/AlertContext';

export default function Dashboard() {
  const [selectedSymbol, setSelectedSymbol] = useState<string>('EURUSD');
  const [chartData, setChartData] = useState<CandleData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const { alerts } = useAlerts();
  
  useEffect(() => {
    loadChartData(selectedSymbol);
  }, [selectedSymbol]);
  
  const loadChartData = async (symbol: string) => {
    setLoading(true);
    try {
      const data = await fetchChartData(symbol);
      setChartData(data);
    } catch (error) {
      console.error('Error fetching chart data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSymbolSelect = (symbol: string) => {
    setSelectedSymbol(symbol);
  };
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Stock Screener Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-6 gap-4">
        <div className="lg:col-span-3">
          <AlertsPanel />
        </div>

        <div className="lg:col-span-3">
          <Card className="mb-6">
            <CardHeader className="bg-default-100">
              <h2 className="text-xl font-semibold">Chart</h2>
            </CardHeader>
            <CardBody>
              <SymbolSelector onSymbolSelect={handleSymbolSelect} />
              <Divider className="my-4" />
              {loading ? (
                <div className="flex justify-center items-center h-[300px]">
                  <Spinner size="lg" />
                </div>
              ) : chartData.length > 0 ? (
                <StockChart symbol={selectedSymbol} data={chartData} />
              ) : (
                <div className="text-center py-10">No chart data available</div>
              )}
            </CardBody>
          </Card>
          
          <Card className="mt-6">
            <CardHeader className="bg-default-100">
              <h2 className="text-xl font-semibold">Market Summary</h2>
            </CardHeader>
            <CardBody>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Active Alerts:</span>
                  <span className="font-semibold">{alerts.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Latest Symbol:</span>
                  <span className="font-semibold">
                    {alerts.length > 0 ? alerts[0].symbol : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Last Alert:</span>
                  <span className="font-semibold">
                    {alerts.length > 0 ? alerts[0].timestamp : 'N/A'}
                  </span>
                </div>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
} 