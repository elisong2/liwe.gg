"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Summs = {
  spell: string;
  casts: number;
};

export const summsColumns: ColumnDef<Summs>[] = [
  {
    accessorKey: "spell",
    header: "Spell",
  },
  {
    accessorKey: "casts",
    header: "Casts",
  },
];
