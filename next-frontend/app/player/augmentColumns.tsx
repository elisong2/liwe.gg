"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Augments = {
  augment: string;
  times_selected: number;
};

export const augmentsColumns: ColumnDef<Augments>[] = [
  {
    accessorKey: "augment",
    header: "Augment",
  },
  {
    accessorKey: "times_selected",
    header: "Times Selected",
  },
];
