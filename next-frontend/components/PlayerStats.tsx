"use client";
import React from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { DataTable } from "@/components/data-table";
import { summsColumns, Summs } from "../app/player/summsColumns";
import { augmentsColumns, Augments } from "../app/player/augmentColumns";
import {
  rolesPlayedColumns,
  RolesPlayed,
} from "../app/player/rolesPlayedColumns";
import { champsColumns, Champs } from "../app/player/champColumns";
import {
  champsArenaColumns,
  Champs_Arena,
} from "../app/player/champArenaColumns";
import {
  longestShortestSrColumns,
  Longestshortestsr,
} from "@/app/player/longestShortestSrColumns";

export interface StatsResponse {
  prof: Record<string, any>[];
  champs_overall: Record<string, any>[];
  champs_sr: Record<string, any>[];
  champs_urf: Record<string, any>[];
  champs_arena: Record<string, any>[];
  arena_augments: Record<string, any>[];
  roles_played: Record<string, any>[];
  longest_sr: Record<string, any>[];
  shortest_sr: Record<string, any>[];
  summs: Record<string, any>[];
}

interface Props {
  data: StatsResponse;
}

export function PlayerStats({ data }: Props) {
  return (
    <div className="max-w-[1400px] mx-auto px-6 mt-5">
      <div className="grid grid-cols-3 gap-4">
        {/* Panel 1: Champion Stats */}

        {/* Panel 2: Summoner Spells + Augments */}
        <Tabs defaultValue="summs">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="summs">Summoners</TabsTrigger>
            <TabsTrigger value="augments">Augments</TabsTrigger>
          </TabsList>
          <TabsContent value="summs">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">Summoner Spells</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <DataTable
                  columns={summsColumns}
                  data={data.summs as Summs[]}
                />
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="augments">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">Augments Selected</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <DataTable
                  columns={augmentsColumns}
                  data={data.arena_augments as Augments[]}
                />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <Tabs defaultValue="champs_overall">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="champs_overall">Champs Overall</TabsTrigger>
            <TabsTrigger value="champs_sr">Champs SR</TabsTrigger>
            <TabsTrigger value="champs_arena">Champs Arena</TabsTrigger>
          </TabsList>
          <TabsContent value="champs_overall">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">Champions Overall</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <DataTable
                  columns={champsColumns}
                  data={data.champs_overall as Champs[]}
                />
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="champs_sr">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">
                  Champions Summoner's Rift
                </CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <DataTable
                  columns={champsColumns}
                  data={data.champs_sr as Champs[]}
                />
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="champs_arena">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">Champions Arena</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <DataTable
                  columns={champsArenaColumns}
                  data={data.champs_arena as Champs_Arena[]}
                />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Panel 3: Records + Roles */}
        <Tabs defaultValue="roles">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="roles">Roles</TabsTrigger>
            <TabsTrigger value="longest_shortest">
              Shortest + Longest
            </TabsTrigger>
            {/* <TabsTrigger value="shortest">Shortest SR</TabsTrigger> */}
          </TabsList>
          <TabsContent value="roles">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">Roles Played</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <DataTable
                  columns={rolesPlayedColumns}
                  data={data.roles_played as RolesPlayed[]}
                />
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="longest_shortest">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">
                  Shortest + Longest SR Game
                </CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <div className="mt-12">
                  <DataTable
                    columns={longestShortestSrColumns}
                    data={data.shortest_sr as Longestshortestsr[]}
                  />
                </div>

                <div className="mt-20">
                  <DataTable
                    columns={longestShortestSrColumns}
                    data={data.longest_sr as Longestshortestsr[]}
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="shortest">
            <Card className="h-[500px] flex flex-col">
              <CardHeader>
                <CardTitle className="text-center">Shortest SR Games</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm flex-1 overflow-y-auto">
                <DataTable
                  columns={longestShortestSrColumns}
                  data={data.shortest_sr as Longestshortestsr[]}
                />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
