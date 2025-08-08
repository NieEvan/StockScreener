// Mock data for development purposes
export interface CandleData {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
}

// Generate random candle data
export const generateMockCandleData = (symbol: string, count: number = 100): CandleData[] => {
  const data: CandleData[] = [];
  let basePrice = 0;
  
  // Set different base prices for different symbols
  switch(symbol) {
    case 'EURUSD':
      basePrice = 1.05;
      break;
    case 'GBPUSD':
      basePrice = 1.25;
      break;
    case 'USDJPY':
      basePrice = 150.0;
      break;
    case 'AUDUSD':
      basePrice = 0.65;
      break;
    case 'USDCAD':
      basePrice = 1.35;
      break;
    default:
      basePrice = 100;
  }
  
  // Start date 'count' days ago
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - count);
  
  let price = basePrice;
  for (let i = 0; i < count; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);
    
    // Generate random price movements
    const change = (Math.random() - 0.5) * 0.01 * basePrice; // Random price change
    const open = price;
    const close = price + change;
    const high = Math.max(open, close) + (Math.random() * 0.005 * basePrice);
    const low = Math.min(open, close) - (Math.random() * 0.005 * basePrice);
    
    // Format date as YYYY-MM-DD
    const formattedDate = date.toISOString().split('T')[0];
    
    data.push({
      time: formattedDate,
      open: Number(open.toFixed(5)),
      high: Number(high.toFixed(5)),
      low: Number(low.toFixed(5)),
      close: Number(close.toFixed(5))
    });
    
    // Update price for next candle
    price = close;
  }
  
  return data;
};

// Simulate fetching data from an API
export const fetchChartData = async (symbol: string): Promise<CandleData[]> => {
  // In a real application, this would be an API call
  // For now, we'll just use the mock data generator
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(generateMockCandleData(symbol));
    }, 500); // Simulate network delay
  });
}; 