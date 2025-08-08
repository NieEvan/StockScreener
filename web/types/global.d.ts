declare module 'lightweight-charts';
declare module '@nextui-org/react' {
  // Add Selection type
  export type Selection = "all" | Set<string> | string;
  
  // Import components from HeroUI
  export const Card: any;
  export const CardBody: any;
  export const CardHeader: any;
  export const Chip: any;
  export const Table: any;
  export const TableHeader: any;
  export const TableColumn: any;
  export const TableBody: any;
  export const TableRow: any;
  export const TableCell: any;
  export const Dropdown: any;
  export const DropdownTrigger: any;
  export const DropdownMenu: any;
  export const DropdownItem: any;
  export const Button: any;
  export const Pagination: any;
  export const Input: any;
  export const Divider: any;
  export const Spinner: any;
}
declare module '@heroui/system';
declare module '@heroui/link';
declare module '@heroui/button';
declare module '@heroui/navbar';
declare module '@heroui/theme';
declare module '@heroui/kbd';
declare module '@heroui/input';
declare module 'next-themes';
declare module '@heroicons/react/24/outline';

// Extend the React module for JSX elements
declare namespace React {
  interface ReactElement {
    props: any;
    type: any;
  }
}

// Define type for JSX elements
declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: any;
  }
} 