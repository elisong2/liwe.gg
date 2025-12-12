"use client";

// working version

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import { Searchbar } from "@/components/Search";
import { useRouter } from "next/navigation";

function usePaginatedData<T>(data: T[], pageSize: number) {
  const [page, setPage] = useState(1);

  const paginated = data.slice(0, page * pageSize);
  const loadMore = () => setPage((p) => p + 1);
  const hasMore = data.length > paginated.length;

  return { paginated, loadMore, hasMore };
}

export default function PlayerPage() {
  const router = useRouter();
  const handleSearch = (query: string) => {
    // 🟢 Step 1: User enters `Eli#NA1`
    const [ign, tag] = query.split("#");

    if (!tag) {
      alert("Please enter summoner as Name#Tag");
      return;
    }

    // 🟢 Step 2: Convert to hyphen format `Eli-NA1`
    const encoded = `${encodeURIComponent(ign)}-${encodeURIComponent(tag)}`;

    // 🟢 Step 3: Push dynamic route → /player/Eli-NA1
    router.push(`/player/${encoded}`);
  };

  const [loading, setLoading] = useState(false);
  const { ign_tag } = useParams<{ ign_tag: string }>();
  const [data, setData] = useState<any | null>(null);

  useEffect(() => {
    if (!ign_tag) return;

    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/player/${ign_tag}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Backend error: ${res.status}`);
        return res.json();
      })
      .then((json) => setData(json))
      .catch((err) => console.error(err));
  }, [ign_tag]);

  const handleUpdate = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/player/${ign_tag}`,
        {
          method: "PATCH",
        }
      );
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const json = await res.json();
      setData(json); // update frontend state with fresh backend data
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // ✅ Always call hooks, even if data is not yet loaded
  const {
    paginated: paginatedMatches,
    loadMore: loadMoreMatches,
    hasMore: hasMoreMatches,
  } = usePaginatedData(data?.match_history ?? [], 5);

  const {
    paginated: paginatedChamps,
    loadMore: loadMoreChamps,
    hasMore: hasMoreChamps,
  } = usePaginatedData(data?.champ_agg ?? [], 5);

  const {
    paginated: paginatedSumms,
    loadMore: loadMoreSumms,
    hasMore: hasMoreSumms,
  } = usePaginatedData(data?.summs ?? [], 20);

  const {
    paginated: paginatedOverall,
    loadMore: loadMoreOverall,
    hasMore: hasMoreOverall,
  } = usePaginatedData(data?.overall_agg ?? [], 1);

  // ✅ Only conditional logic here — after hooks are declared
  if (!data) return <div>Loading...</div>;

  return (
    <>
      <Navbar></Navbar>
      <Searchbar onSearch={handleSearch}></Searchbar>

      <button
        onClick={handleUpdate}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        {loading ? "Updating..." : "Update"}
      </button>
      <div className="p-6">
        {/* Profile info */}
        {data.prof?.[0] && (
          <div className="mb-6 border-b pb-4">
            <h2 className="text-xl font-bold">{data.prof[0].Summoner}</h2>
            <p>Games Played: {data.prof[0]["Games Played"]}</p>
          </div>
        )}

        {/* Summs */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-2">Summoner Spells</h3>
          {paginatedSumms.map((summs: any, idx: number) => (
            <div key={idx} className="border p-2 mb-2 rounded">
              {Object.entries(summs).map(([key, value]) => (
                <p key={key}>
                  <strong>{key}:</strong> {String(value)}
                </p>
              ))}
            </div>
          ))}
        </div>

        {/* Overall */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-2">Total</h3>
          {paginatedOverall.map((overall: any, idx: number) => (
            <div key={idx} className="border p-2 mb-2 rounded">
              {Object.entries(overall).map(([key, value]) => (
                <p key={key}>
                  <strong>{key}:</strong> {String(value)}
                </p>
              ))}
            </div>
          ))}
        </div>

        {/* Champ Aggregates */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-2">Champion Stats</h3>
          {paginatedChamps.map((champ: any, idx: number) => (
            <div key={idx} className="border p-2 mb-2 rounded">
              {Object.entries(champ).map(([key, value]) => (
                <p key={key}>
                  <strong>{key}:</strong> {String(value)}
                </p>
              ))}
            </div>
          ))}
          {hasMoreChamps && (
            <button
              onClick={loadMoreChamps}
              className="bg-blue-500 text-white px-3 py-1 rounded mt-2"
            >
              Load more champs
            </button>
          )}
        </div>

        {/* Match History */}
        <div>
          <h3 className="text-lg font-semibold mb-2">Match History</h3>
          {paginatedMatches.map((match: any, idx: number) => (
            <div key={idx} className="border p-2 mb-2 rounded">
              {Object.entries(match).map(([key, value]) => (
                <p key={key}>
                  <strong>{key}:</strong> {String(value)}
                </p>
              ))}
            </div>
          ))}
          {hasMoreMatches && (
            <button
              onClick={loadMoreMatches}
              className="bg-blue-500 text-white px-3 py-1 rounded mt-2"
            >
              Load more matches
            </button>
          )}
        </div>
      </div>
    </>
  );
}
