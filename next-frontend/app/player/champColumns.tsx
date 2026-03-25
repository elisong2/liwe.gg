"use client";

import { ColumnDef } from "@tanstack/react-table";

export type Champs = {
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
  double_kills: number;
  triple_kills: number;
  quadra_kills: number;
  pentakills: number;
  largest_killing_spree: number;
  longesttimespentliving: string;
  firstbloodkill: number;
  firsttowerkill: number;
  gold_earned: number;
  cs: number;
  total_damage_dealt_to_champions: number;
  total_damage_taken: number;
  total_damage_shielded_on_teammates: number;
  damage_self_mitigated: number;
  total_heals_on_teammates: number;
  timeccingothers: number;
  damage_dealt_to_buildings: number;
  damagedealttoobjectives: number;
  damagedealttoturrets: number;
  missing_pings: number;
  visionscore: number;
  wardskilled: number;
  wardsplaced: number;
};

export const champsColumns: ColumnDef<Champs>[] = [
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
    accessorKey: "double_kills",
    header: "Double Kills",
  },
  {
    accessorKey: "triple_kills",
    header: "Triple Kills",
  },
  {
    accessorKey: "quadra_kills",
    header: "Quadra Kills",
  },
  {
    accessorKey: "pentakills",
    header: "Penta Kills",
  },
  {
    accessorKey: "largest_killing_spree",
    header: "Largest Killing Spree",
  },
  {
    accessorKey: "longesttimespentliving",
    header: "Longest Time Spent Living",
    cell: ({ getValue }) => {
      const totalSeconds = getValue() as number;
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    },
  },
  {
    accessorKey: "firstbloodkill",
    header: "First Blood Kills",
  },
  {
    accessorKey: "firsttowerkill",
    header: "First Tower Kills",
  },
  {
    accessorKey: "gold_earned",
    header: "Gold Earned",
  },
  {
    accessorKey: "cs",
    header: "CS",
  },
  {
    accessorKey: "total_damage_dealt_to_champs",
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
    accessorKey: "damage_dealt_to_buildings",
    header: "Damage Dealt to Buildings",
  },
  {
    accessorKey: "damagedealttoobjectives",
    header: "Damage Dealt to Objectives",
  },
  {
    accessorKey: "damagedealttoturrets",
    header: "Damage Dealt to Turrets",
  },
  {
    accessorKey: "missing_pings",
    header: "Missing Pings",
  },
  {
    accessorKey: "visionscore",
    header: "Vision Score",
  },
  {
    accessorKey: "wardskilled",
    header: "Wards Killed",
  },
  {
    accessorKey: "wardsplaced",
    header: "Wards Placed",
  },
];
