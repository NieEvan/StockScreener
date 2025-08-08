'use client';

import { useEffect, useRef, useState } from 'react';
import { createChart, ColorType, CrosshairMode } from 'lightweight-charts';

interface ChartProps {
  symbol: string;
  data: {
    time: string;
    open: number;
    high: number;
    low: number;
    close: number;
  }[];
}

const StockChart = ({ symbol, data }: ChartProps) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [chartInstance, setChartInstance] = useState<any>(null);

  useEffect(() => {
    if (chartContainerRef.current && data.length > 0) {
      const handleResize = () => {
        if (chartInstance) {
          chartInstance.applyOptions({ 
            width: chartContainerRef.current?.clientWidth || 600 
          });
        }
      };

      const chart = createChart(chartContainerRef.current, {
        layout: {
          background: { type: ColorType.Solid, color: 'transparent' },
          textColor: 'rgba(255, 255, 255, 0.9)',
        },
        width: chartContainerRef.current.clientWidth,
        height: 300,
        grid: {
          vertLines: {
            color: 'rgba(42, 46, 57, 0.5)',
          },
          horzLines: {
            color: 'rgba(42, 46, 57, 0.5)',
          },
        },
        crosshair: {
          mode: CrosshairMode.Normal,
        },
        timeScale: {
          borderColor: 'rgba(197, 203, 206, 0.8)',
          timeVisible: true,
        },
        rightPriceScale: {
          borderColor: 'rgba(197, 203, 206, 0.8)',
        },
      });

      const candleSeries = chart.addCandlestickSeries({
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350',
      });

      candleSeries.setData(data);
      
      setChartInstance(chart);

      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        chart.remove();
      };
    }
  }, [data]);

  return (
    <div className="w-full">
      <div className="text-lg font-semibold mb-2">{symbol}</div>
      <div ref={chartContainerRef} className="w-full" />
    </div>
  );
};

export default StockChart; 