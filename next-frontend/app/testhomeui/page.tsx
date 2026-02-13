"use client";
import React from "react";
import { Searchbar } from "@/components/Search";
import Link from "next/dist/client/link";
import { useRouter } from "next/navigation";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function testui() {
  const router = useRouter();

  const handleSearch = (query: string) => {
    const [ign, tag] = query.split("#");

    if (!tag) {
      alert("Please enter summoner as Name#Tag");
      return;
    }

    const encoded = `${encodeURIComponent(ign)}-${encodeURIComponent(tag)}`;

    router.push(`/player/${encoded}`);
  };
  return (
    <>
      <h1 className="mt-25 mb-5 text-center text-6xl font-bold p-5">
        <Link href="/" target="_self" className="border-5 rounded-3xl p-4">
          liwe.gg
        </Link>
      </h1>
      <p className="text-center pt-5 font-italic">
        League stats you didn't know about yourself!
      </p>

      <div className="mt-15 justify-center items-center flex flex-col ">
        <Searchbar onSearch={handleSearch}></Searchbar>
      </div>

      <div className="justify-center items-center flex mt-10">
        <Tabs defaultValue="overview" className="w-[400px]">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="matches">Match History</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>
          <TabsContent value="overview">
            <Card>
              <CardHeader>
                <CardTitle>Overview</CardTitle>
                <CardDescription>
                  View your key metrics and recent project activity. Track
                  progress across all your active projects.
                </CardDescription>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm">
                You have 12 active projects and 3 pending tasks.
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="matches">
            <Card>
              <CardHeader>
                <CardTitle>Match History</CardTitle>
                <CardDescription></CardDescription>
              </CardHeader>
              <CardContent className="text-muted-foreground text-sm"></CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      <p className="text-center text-sm bottom-10 absolute w-full">
        made with FastAPI + Next.js
      </p>
    </>
  );
}
