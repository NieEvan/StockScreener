# Stock Screener Application

A comprehensive stock screening and alerting system consisting of:

1. A backend service that monitors stocks and generates alerts
2. A web frontend that displays real-time alerts and interactive charts

## Project Structure

- `modules/` - Core backend modules for stock analysis and alert generation
- `strategies/` - Trading strategies that analyze market data and generate signals
- `web/` - Next.js web application for displaying alerts and charts

## Backend Service

The backend service monitors stocks using data from MetaTrader 5 and custom trading strategies. When a trading signal is detected, it sends alerts via WebSockets to the frontend application.

### Key Features

- Integration with MetaTrader 5
- Support for multiple timeframes (1M, 5M, 1H, 4H)
- MongoDB storage for historical data
- WebSocket server for real-time alerts
- Email notifications

## Web Frontend

The web frontend is built with Next.js, HeroUI (previously NextUI), and TradingView's Lightweight Charts. It provides a responsive dashboard for monitoring stocks and receiving real-time alerts.

### Key Features

- Real-time stock alerts via WebSocket
- Interactive candlestick charts
- Symbol selection and search
- Responsive design for desktop and mobile
- Dark/light theme support

## Getting Started

### Prerequisites

- Node.js 18+
- MongoDB
- MetaTrader 5 (for backend)

### Running the Backend

1. Install dependencies
2. Configure MongoDB connection in `config/settings.py`
3. Run `main.py` to start the backend service

### Running the Web Frontend

1. Navigate to the web directory: `cd web`
2. Install dependencies: `yarn install`
3. Start the development server: `yarn dev`
4. For testing without the backend, run the mock WebSocket server: `yarn mock-server`

## WebSocket Communication

The backend sends alerts with the following structure:

```json
{
  "market": "FOREX1MB",
  "symbol": "EURUSD",
  "direction": "买入",
  "conditions": "Breakout detected"
}
```

The web frontend connects to this WebSocket server to receive and display these alerts in real-time. 