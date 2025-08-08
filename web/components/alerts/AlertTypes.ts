export interface Alert {
  id: string;
  market: string;
  symbol: string;
  direction: string;
  conditions: string;
  timestamp: string;
}

export interface SortDescriptor {
  column?: string;
  direction?: 'ascending' | 'descending';
} 