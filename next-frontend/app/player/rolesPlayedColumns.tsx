"use client";

import { ColumnDef } from "@tanstack/react-table";

export type RolesPlayed = {
  role: string;
  wins: number;
  losses: number;
};

export const rolesPlayedColumns: ColumnDef<RolesPlayed>[] = [
  {
    accessorKey: "role",
    header: "Role",
  },
  {
    accessorKey: "wins",
    header: "Wins",
  },
  {
    accessorKey: "losses",
    header: "Losses",
  },
];
