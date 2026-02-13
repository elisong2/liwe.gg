"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Summs = {
  Spell: string;
  Count: number;
};

export const columns: ColumnDef<Summs>[] = [
  {
    accessorKey: "Spell",
    header: "Spell",
  },
  {
    accessorKey: "Uses",
    header: "Count",
  },
];
