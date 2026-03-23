"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Champs_Arena = {
  champion: string;
  wins: number;
  losses: number;
  q: number;
  w: number;
  e: number;
  r: number;
  kills: number;
  deaths: number;
  assists: number;
  largest_killing_spree: number;
  longesttimespentliving: number;
  gold_earned: number;
  total_damage_dealt_to_champions: number;
  total_damage_taken: number;
  total_damage_shielded_on_teammates: number;
  damage_self_mitigated: number;
  total_heals_on_teammates: number;
  timeccingothers: number;
  missing_pings: number;
};

export const champsArenaColumns: ColumnDef<Champs_Arena>[] = [
  {
    accessorKey: "champion",
    header: "Champion",
  },
  {
    accessorKey: "wins",
    header: "Wins",
  },
  {
    accessorKey: "losses",
    header: "Losses",
  },
  {
    accessorKey: "q",
    header: "Q",
  },
  {
    accessorKey: "w",
    header: "W",
  },
  {
    accessorKey: "e",
    header: "E",
  },
  {
    accessorKey: "r",
    header: "R",
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

  {
    accessorKey: "largest_killing_spree",
    header: "Largest Killing Spree",
  },
  {
    accessorKey: "longesttimespentliving",
    header: "Longest Time Spent Living",
  },

  {
    accessorKey: "gold_earned",
    header: "Gold Earned",
  },

  {
    accessorKey: "total_damage_dealt_to_champions",
    header: "Total Damage Dealt to Champions",
  },
  {
    accessorKey: "total_damage_taken",
    header: "Total Damage Taken",
  },
  {
    accessorKey: "total_damage_shielded_on_teammates",
    header: "Total Damage Shielded on Teammates",
  },
  {
    accessorKey: "damage_self_mitigated",
    header: "Damage Self Mitigated",
  },
  {
    accessorKey: "total_heals_on_teammates",
    header: "Total Heals on Teammates",
  },
  {
    accessorKey: "timeccingothers",
    header: "Time CCing Others",
  },

  {
    accessorKey: "missing_pings",
    header: "Missing Pings",
  },
];
