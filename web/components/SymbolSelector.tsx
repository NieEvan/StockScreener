'use client';

import { useState, useEffect } from 'react';
import { Select, SelectItem, Input, Button } from '@nextui-org/react';

interface SymbolSelectorProps {
  onSymbolSelect: (symbol: string) => void;
}

export default function SymbolSelector({ onSymbolSelect }: SymbolSelectorProps) {
  const [selectedSymbol, setSelectedSymbol] = useState<string>('EURUSD');
  const [search, setSearch] = useState<string>('');
  const [symbols, setSymbols] = useState<string[]>(['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']);
  const [filteredSymbols, setFilteredSymbols] = useState<string[]>(symbols);
  
  useEffect(() => {
    // Here you would typically fetch available symbols from your backend API
    // For demo purposes, we're using a static list
    setFilteredSymbols(
      symbols.filter(symbol => 
        symbol.toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [search, symbols]);
  
  const handleSelectSymbol = (value: string) => {
    setSelectedSymbol(value);
    onSymbolSelect(value);
  };
  
  return (
    <div className="flex flex-col gap-2 md:flex-row md:items-end">
      <div className="flex-1">
        <Input
          label="Search Symbol"
          placeholder="Type to search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          isClearable
          className="max-w-xs"
        />
      </div>
      
      <div className="flex-1">
        <Select
          label="Select Symbol"
          placeholder="Select a symbol"
          selectedKeys={[selectedSymbol]}
          onChange={(e) => handleSelectSymbol(e.target.value)}
          className="max-w-xs"
        >
          {filteredSymbols.map((symbol) => (
            <SelectItem key={symbol} value={symbol}>
              {symbol}
            </SelectItem>
          ))}
        </Select>
      </div>
      
      <Button 
        color="primary" 
        onClick={() => onSymbolSelect(selectedSymbol)}
      >
        Load Chart
      </Button>
    </div>
  );
} 