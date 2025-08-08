'use client';

import { useMemo } from 'react';
import { 
  Table, 
  TableHeader, 
  TableColumn, 
  TableBody, 
  TableRow, 
  TableCell,
  Chip,
  Pagination
} from '@nextui-org/react';
import { Alert, SortDescriptor } from './AlertTypes';

interface AlertsTableProps {
  alerts: Alert[];
  page: number;
  rowsPerPage: number;
  sortDescriptor: SortDescriptor;
  onSortChange: (descriptor: SortDescriptor) => void;
  onPageChange: (page: number) => void;
}

export default function AlertsTable({
  alerts,
  page,
  rowsPerPage,
  sortDescriptor,
  onSortChange,
  onPageChange
}: AlertsTableProps) {
  // Pagination
  const pages = Math.ceil(alerts.length / rowsPerPage);
  const paginatedAlerts = useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    
    return alerts.slice(start, end);
  }, [alerts, page, rowsPerPage]);
  
  if (alerts.length === 0) {
    return (
      <div className="flex justify-center items-center min-h-[400px] w-full">
        <p className="text-default-500">No alerts found</p>
      </div>
    );
  }
  
  return (
    <Table
      aria-label="Stock alerts table"
      bottomContent={
        <div className="flex w-full justify-center">
          <Pagination
            isCompact
            showControls
            showShadow
            color="primary"
            page={page}
            total={pages}
            onChange={onPageChange}
          />
        </div>
      }
      sortDescriptor={sortDescriptor}
      onSortChange={onSortChange}
    >
      <TableHeader>
        <TableColumn allowsSorting key="timestamp">TIMESTAMP</TableColumn>
        <TableColumn allowsSorting key="symbol">SYMBOL</TableColumn>
        <TableColumn allowsSorting key="market">MARKET</TableColumn>
        <TableColumn allowsSorting key="direction">DIRECTION</TableColumn>
        <TableColumn allowsSorting key="conditions">CONDITIONS</TableColumn>
      </TableHeader>
      <TableBody emptyContent="No alerts found">
        {paginatedAlerts.map((alert) => (
          <TableRow key={alert.id} className={alert.direction === '买入' ? 'bg-success-50' : 'bg-danger-50'}>
            <TableCell>{alert.timestamp}</TableCell>
            <TableCell>{alert.symbol}</TableCell>
            <TableCell>{alert.market}</TableCell>
            <TableCell>
              <Chip 
                color={alert.direction === '买入' ? 'success' : 'danger'} 
                variant="flat"
              >
                {alert.direction}
              </Chip>
            </TableCell>
            <TableCell>{alert.conditions}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
} 