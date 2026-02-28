"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Champs = {
  Assists: number;
  CS: number;
  Champion: string;
  Deaths: number;
  "Double Kills": number;
  E: number;
  "Gold Earned": number;
  Kills: number;
  "Largest Killing Spree": number;
  "Largest Multikill": number;
  Losses: number;
  Pentakills: number;
  Q: number;
  "Quadra Kills": number;
  R: number;
  "Total Damage Dealt to Champions": number;
  "Total Damage Shielded on Teammates": number;
  "Total Damage Taken": number;
  "Total Heals on Teammates": number;
  "Triple Kills": number;
  W: number;
  Wins: number;
};

export const champsColumns: ColumnDef<Champs>[] = [
  {
    accessorKey: "Champion",
    header: "Champion",
  },
  {
    accessorKey: "Q",
    header: "Q",
  },
  {
    accessorKey: "W",
    header: "W",
  },
  {
    accessorKey: "E",
    header: "E",
  },

  {
    accessorKey: "R",
    header: "R",
  },
  {
    accessorKey: "Wins",
    header: "Wins",
  },
  {
    accessorKey: "Losses",
    header: "Losses",
  },
  {
    accessorKey: "Kills",
    header: "Kills",
  },
  {
    accessorKey: "Deaths",
    header: "Deaths",
  },
  {
    accessorKey: "Assists",
    header: "Assists",
  },
  {
    accessorKey: "CS",
    header: "CS",
  },
  {
    accessorKey: "Gold Earned",
    header: "Gold Earned",
  },

  {
    accessorKey: "Largest Killing Spree",
    header: "Largest Killing Spree",
  },
  {
    accessorKey: "Largest Multikill",
    header: "Largest Multikill",
  },
  {
    accessorKey: "Double Kills",
    header: "Double Kills",
  },
  {
    accessorKey: "Triple Kills",
    header: "Triple Kills",
  },
  {
    accessorKey: "Quadra Kills",
    header: "Quadra Kills",
  },
  {
    accessorKey: "Pentakills",
    header: "Pentakills",
  },

  {
    accessorKey: "Total Damage Dealt to Champions",
    header: "Total Damage Dealt to Champions",
  },
  {
    accessorKey: "Total Damage Taken",
    header: "Total Damage Taken",
  },

  {
    accessorKey: "Total Damage Shielded on Teammates",
    header: "Total Damage Shielded on Teammates",
  },

  {
    accessorKey: "Total Heals on Teammates",
    header: "Total Heals on Teammates",
  },
];
