'use client';

import { Selection } from '@nextui-org/react';
import { 
  Input,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Button
} from '@nextui-org/react';
import { 
  MagnifyingGlassIcon, 
  ChevronDownIcon
} from '@heroicons/react/24/outline';

interface AlertsFiltersProps {
  uniqueSymbols: string[];
  uniqueMarkets: string[];
  uniqueConditions: string[];
  selectedSymbols: string[];
  selectedMarkets: string[];
  selectedConditions: string[];
  searchQuery: string;
  onSearchChange: (value: string) => void;
  onSymbolSelectionChange: (keys: Selection) => void;
  onMarketSelectionChange: (keys: Selection) => void;
  onConditionsSelectionChange: (keys: Selection) => void;
}

export default function AlertsFilters({
  uniqueSymbols,
  uniqueMarkets,
  uniqueConditions,
  selectedSymbols,
  selectedMarkets,
  selectedConditions,
  searchQuery,
  onSearchChange,
  onSymbolSelectionChange,
  onMarketSelectionChange,
  onConditionsSelectionChange
}: AlertsFiltersProps) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center p-4">
      <Input
        isClearable
        className="w-full md:max-w-[240px]"
        placeholder="Search..."
        value={searchQuery}
        onValueChange={onSearchChange}
        startContent={
          <MagnifyingGlassIcon className="h-4 w-4 text-default-400" />
        }
      />
      <div className="flex flex-row gap-2">
        <Dropdown>
          <DropdownTrigger>
            <Button 
              variant="flat"
              endContent={<ChevronDownIcon className="h-4 w-4" />}
            >
              Symbol {selectedSymbols.length > 0 && `(${selectedSymbols.length})`}
            </Button>
          </DropdownTrigger>
          <DropdownMenu
            aria-label="Symbol filter"
            closeOnSelect={false}
            selectionMode="multiple"
            onSelectionChange={onSymbolSelectionChange}
          >
            {uniqueSymbols.map((symbol) => (
              <DropdownItem key={symbol}>{symbol}</DropdownItem>
            ))}
          </DropdownMenu>
        </Dropdown>
        
        <Dropdown>
          <DropdownTrigger>
            <Button 
              variant="flat"
              endContent={<ChevronDownIcon className="h-4 w-4" />}
            >
              Market {selectedMarkets.length > 0 && `(${selectedMarkets.length})`}
            </Button>
          </DropdownTrigger>
          <DropdownMenu
            aria-label="Market filter"
            closeOnSelect={false}
            selectionMode="multiple"
            onSelectionChange={onMarketSelectionChange}
          >
            {uniqueMarkets.map((market) => (
              <DropdownItem key={market}>{market}</DropdownItem>
            ))}
          </DropdownMenu>
        </Dropdown>
        
        <Dropdown>
          <DropdownTrigger>
            <Button 
              variant="flat"
              endContent={<ChevronDownIcon className="h-4 w-4" />}
            >
              Conditions {selectedConditions.length > 0 && `(${selectedConditions.length})`}
            </Button>
          </DropdownTrigger>
          <DropdownMenu
            aria-label="Conditions filter"
            closeOnSelect={false}
            selectionMode="multiple"
            onSelectionChange={onConditionsSelectionChange}
          >
            {uniqueConditions.map((condition) => (
              <DropdownItem key={condition}>{condition}</DropdownItem>
            ))}
          </DropdownMenu>
        </Dropdown>
      </div>
    </div>
  );
} 