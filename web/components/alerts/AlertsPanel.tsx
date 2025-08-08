'use client';

import { useState, useMemo } from 'react';
import { 
  Card, 
  CardBody, 
  CardHeader, 
  Chip,
  Selection
} from '@nextui-org/react';
import { useAlerts } from './AlertsProvider';
import AlertsFilters from './AlertsFilters';
import AlertsTable from './AlertsTable';
import { SortDescriptor } from './AlertTypes';

export default function AlertsPanel() {
  const { alerts } = useAlerts();
  const [page, setPage] = useState(1);
  const [rowsPerPage] = useState(10);
  const [selectedSymbols, setSelectedSymbols] = useState<string[]>([]);
  const [selectedMarkets, setSelectedMarkets] = useState<string[]>([]);
  const [selectedConditions, setSelectedConditions] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortDescriptor, setSortDescriptor] = useState<SortDescriptor>({
    column: 'timestamp',
    direction: 'descending',
  });

  // Extract unique values for filters
  const uniqueSymbols = useMemo(() => {
    return Array.from(new Set(alerts.map(alert => alert.symbol)));
  }, [alerts]);
  
  const uniqueMarkets = useMemo(() => {
    return Array.from(new Set(alerts.map(alert => alert.market)));
  }, [alerts]);
  
  const uniqueConditions = useMemo(() => {
    return Array.from(new Set(alerts.map(alert => alert.conditions)));
  }, [alerts]);
  
  // Filtering and sorting logic
  const filteredAlerts = useMemo(() => {
    let filtered = [...alerts];
    
    // Apply symbol filter
    if (selectedSymbols.length > 0) {
      filtered = filtered.filter(alert => 
        selectedSymbols.includes(alert.symbol)
      );
    }
    
    // Apply market filter
    if (selectedMarkets.length > 0) {
      filtered = filtered.filter(alert => 
        selectedMarkets.includes(alert.market)
      );
    }
    
    // Apply conditions filter
    if (selectedConditions.length > 0) {
      filtered = filtered.filter(alert => 
        selectedConditions.includes(alert.conditions)
      );
    }
    
    // Apply search query
    if (searchQuery.trim() !== "") {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        alert => 
          alert.symbol.toLowerCase().includes(query) ||
          alert.market.toLowerCase().includes(query) ||
          alert.conditions.toLowerCase().includes(query)
      );
    }
    
    // Apply sorting
    if (sortDescriptor.column) {
      filtered.sort((a, b) => {
        const first = a[sortDescriptor.column as keyof typeof a];
        const second = b[sortDescriptor.column as keyof typeof b];
        const cmp = first < second ? -1 : first > second ? 1 : 0;
        
        return sortDescriptor.direction === "descending" ? -cmp : cmp;
      });
    }
    
    return filtered;
  }, [alerts, selectedSymbols, selectedMarkets, selectedConditions, searchQuery, sortDescriptor]);
  
  // Handle dropdown selection changes
  const handleSymbolSelectionChange = (keys: Selection) => {
    if (typeof keys === 'string' && keys === "all") {
      setSelectedSymbols([]);
    } else if (keys instanceof Set) {
      setSelectedSymbols(Array.from(keys) as string[]);
    }
  };

  const handleMarketSelectionChange = (keys: Selection) => {
    if (typeof keys === 'string' && keys === "all") {
      setSelectedMarkets([]);
    } else if (keys instanceof Set) {
      setSelectedMarkets(Array.from(keys) as string[]);
    }
  };

  const handleConditionsSelectionChange = (keys: Selection) => {
    if (typeof keys === 'string' && keys === "all") {
      setSelectedConditions([]);
    } else if (keys instanceof Set) {
      setSelectedConditions(Array.from(keys) as string[]);
    }
  };
  
  return (
    <Card className="w-full">
      <CardHeader className="bg-default-100 flex justify-between">
        <h3 className="text-xl font-semibold">Stock Alerts</h3>
        {alerts.length > 0 && (
          <Chip color="danger" variant="flat">
            {filteredAlerts.length} Alerts
          </Chip>
        )}
      </CardHeader>
      <CardBody className="p-0">
        <AlertsFilters
          uniqueSymbols={uniqueSymbols}
          uniqueMarkets={uniqueMarkets}
          uniqueConditions={uniqueConditions}
          selectedSymbols={selectedSymbols}
          selectedMarkets={selectedMarkets}
          selectedConditions={selectedConditions}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          onSymbolSelectionChange={handleSymbolSelectionChange}
          onMarketSelectionChange={handleMarketSelectionChange}
          onConditionsSelectionChange={handleConditionsSelectionChange}
        />
        <AlertsTable
          alerts={filteredAlerts}
          page={page}
          rowsPerPage={rowsPerPage}
          sortDescriptor={sortDescriptor}
          onSortChange={setSortDescriptor}
          onPageChange={setPage}
        />
      </CardBody>
    </Card>
  );
} 