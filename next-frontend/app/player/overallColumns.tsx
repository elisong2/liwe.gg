"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Overall = {
  Stat: string;
  Value: number;
};

export const overallColumns: ColumnDef<Overall>[] = [
  {
    accessorKey: "stat",
    header: "Stat",
  },
  {
    accessorKey: "value",
    header: "Value",
  },
];
