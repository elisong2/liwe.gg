"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Longestshortestsr = {
  champion: string;
  gameduration: number;
  kills: number;
  deaths: number;
  assists: number;
};

export const longestShortestSrColumns: ColumnDef<Longestshortestsr>[] = [
  {
    accessorKey: "champion",
    header: "Champion",
  },
  {
    accessorKey: "gameduration",
    header: "Game Duration",
  },
  {
    accessorKey: "kills",
    header: "Kills",
  },
  {
    accessorKey: "deaths",
    header: "Deaths",
  },
  {
    accessorKey: "assists",
    header: "Assists",
  },
];
