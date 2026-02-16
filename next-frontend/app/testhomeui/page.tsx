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

export default function Testui() {
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
    </>
  );
}
