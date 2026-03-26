"use client";

// working version

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { Searchbar } from "@/components/Search";
import { PlayerStats, StatsResponse } from "@/components/PlayerStats";
import { useRouter } from "next/navigation";

import Link from "next/dist/client/link";

import { Button } from "@/components/ui/button";

//
export default function PlayerPage() {
  const router = useRouter();
  const handleSearch = (query: string) => {
    // user enters `OPMAGEMASTER#NA1`
    const [ign, tag] = query.split("#");

    if (!tag) {
      alert("Please enter summoner as Name#Tag");
      return;
    }

    // convert to hyphen format `Eli-NA1`
    const encoded = `${encodeURIComponent(ign)}-${encodeURIComponent(tag)}`;

    // push dynamic route → /player/Eli-NA1
    router.push(`/player/${encoded}`);
  };

  const [loading, setLoading] = useState(false);
  const { ign_tag } = useParams<{ ign_tag: string }>();
  const [data, setData] = useState<any | null>(null);
  const [reshapeData, setReshapeData] = useState<any | null>(null);

  useEffect(() => {
    if (!ign_tag) return;

    // fetch(`http://127.0.0.1:8000/player/${ign_tag}`)
    // fetch(`https://liwegg-production.up.railway.app/player/${ign_tag}`)
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/player/${ign_tag}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Backend error: ${res.status}`);
        return res.json();
      })
      .then((json) => {
        console.log("Backend JSON:", json);
        // console.log("Summoners: ", json.summs);
        // console.log("sum 1: ", json.summs[0]);
        // console.log("overall: ", json.overall_agg);
        // console.log("ovearll: ", json.overall_agg[0]);
        // console.log("name: ", json.summs[0].Spell);

        // console.log("bruh ", data.summs);
        setData(json);
        const overallStats = json?.overall_agg?.[0];
        if (!overallStats) {
          setReshapeData([]);
          return;
        }
        const transformed = Object?.entries(json.overall_agg[0]).map(
          ([key, value]) => ({
            stat: key,
            value: value,
          }),
        );
        setReshapeData(transformed);
        // console.log("reshaped: ", transformed);
      })
      .catch((err) => console.error(err));
  }, [ign_tag]);

  const handleUpdate = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/player/${ign_tag}`,
        {
          method: "PATCH",
        },
      );
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const json = await res.json();
      setData(json); // update frontend state with fresh backend data
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
    window.location.reload();
  };
  // console.log("HI THERE bro");
  // console.log("Fetched player data:", data);
  // call hooks, even if data is not yet loaded

  // only conditional logic here — after hooks are declared
  if (!data)
    return (
      <div className="grid min-h-screen place-items-center">loading...</div>
    );
  // console.log("Fetched player data:", data);

  return (
    <>
      <h1 className="mt-25 mb-5 text-center text-6xl p-5">
        <Link href="/" target="_self" className="border-5 rounded-3xl p-4">
          liwe<span className="text-red-500">.</span>gg
        </Link>
      </h1>
      {/* <p className="text-center pt-5 font-italic">
        *currently does not track Mayhem
      </p> */}

      <div className="mt-15 justify-center items-center flex flex-col ">
        <Searchbar onSearch={handleSearch}></Searchbar>
      </div>

      <div className="flex justify-center items-center gap-3">
        <div className="pt-14">
          {/* Profile info */}
          {data.prof?.[0] && (
            <div className="mb-5 pb-4">
              <h2 className="text-xl font-bold">{data.prof[0].summoner}</h2>
              {/* <p>Games Played: {data.prof[0]["Games Played"]}</p> */}
            </div>
          )}
        </div>

        {/* <button
          onClick={handleUpdate}
          disabled={loading}
          className="px-2 py-2 mt-5 bg-blue-500 text-white rounded"
        >
          {loading ? "Updating..." : "Update"}
        </button> */}

        <Button
          variant="outline"
          onClick={handleUpdate}
          disabled={loading}
          className="px-2 py-2 mt-5 cursor-pointer"
        >
          {loading ? "Updating..." : "Update"}
        </Button>
      </div>

      {data.champs_overall?.length > 0 && <PlayerStats data={data} />}

      <div className="mt-24 pb-10">
        <p className="text-center text-sm font-italic">
          For first time/infrequent visitors, 'Update' may take some time
        </p>
        <p className="text-center text-sm pt-1 font-italic">
          Mayhem is currently untracked
        </p>
      </div>
    </>
  );
}
