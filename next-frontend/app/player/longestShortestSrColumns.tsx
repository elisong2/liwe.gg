"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Longestshortestsr = {
  champion: string;
  gameduration: string;
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
    header: "Duration",
    cell: ({ getValue }) => {
      const totalSeconds = getValue() as number;
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    },
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
