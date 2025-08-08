// Mock WebSocket server for local development testing
const WebSocket = require('ws');
const http = require('http');

const PORT = 8000;

// Create HTTP server
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('WebSocket server is running');
});

// Create WebSocket server
const wss = new WebSocket.Server({ server });

// Sample stock symbols
const symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'];
const markets = ['FOREX1MB', 'FOREX5MB', 'FOREX1HS', 'FOREX4HS'];
const directions = ['买入', '卖出'];
const conditions = [
  'Breakout detected',
  'Support level reached',
  'Resistance broken',
  'Moving average crossover',
  'RSI oversold',
  'RSI overbought',
  'MACD signal'
];

// Function to generate random alerts
function generateRandomAlert() {
  const symbol = symbols[Math.floor(Math.random() * symbols.length)];
  const market = markets[Math.floor(Math.random() * markets.length)];
  const direction = directions[Math.floor(Math.random() * directions.length)];
  const condition = conditions[Math.floor(Math.random() * conditions.length)];
  
  return {
    market,
    symbol,
    direction,
    conditions: condition
  };
}

// Handle WebSocket connections
wss.on('connection', (ws) => {
  console.log('Client connected');
  
  // Send initial alert
  const initialAlert = generateRandomAlert();
  ws.send(JSON.stringify(initialAlert));
  
  // Generate random alerts every 30 seconds
  const interval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      const alert = generateRandomAlert();
      ws.send(JSON.stringify(alert));
      console.log('Alert sent:', alert);
    }
  }, 30000);
  
  // Handle client disconnect
  ws.on('close', () => {
    console.log('Client disconnected');
    clearInterval(interval);
  });
  
  // Handle errors
  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
    clearInterval(interval);
  });
});

// Start server
server.listen(PORT, () => {
  console.log(`Mock WebSocket server running at http://localhost:${PORT}`);
}); 