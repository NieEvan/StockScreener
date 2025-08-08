# Stock Screener Web Application

A real-time stock screening and charting application built with Next.js and HeroUI (previously NextUI).

## Features

- Real-time stock alerts via WebSocket
- Interactive candlestick charts powered by TradingView's Lightweight Charts
- Multiple timeframe support (1M, 5M, 1H, 4H)
- Responsive design for desktop and mobile
- Dark/light theme support

## Tech Stack

- **Frontend**: Next.js, TypeScript, HeroUI
- **Charting**: TradingView's Lightweight Charts
- **Real-time Communication**: WebSockets
- **Styling**: Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18+
- Yarn or npm

### Installation

1. Clone the repository
2. Navigate to the web directory:
   ```bash
   cd web
   ```
3. Install dependencies:
   ```bash
   yarn install
   # or
   npm install
   ```
4. Run the development server:
   ```bash
   yarn dev
   # or
   npm run dev
   ```
5. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## WebSocket Integration

The application connects to a WebSocket server running at `ws://localhost:8000/ws` to receive real-time stock alerts. When an alert is received, it's displayed in the alerts panel.

## Backend Communication

The backend sends alerts with the following structure:

```json
{
  "market": "FOREX1MB",
  "symbol": "EURUSD",
  "direction": "买入",
  "conditions": "Breakout detected"
}
```

## Folder Structure

- `app/` - Next.js app directory
- `components/` - Reusable UI components
- `context/` - React context for state management
- `services/` - API and data services
- `styles/` - Global styles

## Customization

You can customize the application by modifying the following files:

- `config/site.ts` - Site configuration (name, navigation, etc.)
- `components/StockChart.tsx` - Chart appearance and behavior
- `components/AlertsPanel.tsx` - Alerts display and filtering
- `services/chartService.ts` - Chart data fetching and processing
