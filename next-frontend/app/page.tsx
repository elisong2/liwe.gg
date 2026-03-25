"use client";

// import Image from "next/image";
import { useRouter } from "next/navigation";
import { Searchbar } from "@/components/Search";
import Link from "next/dist/client/link";

export default function Home() {
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
      <h1 className="mt-25 mb-5 text-center text-6xl p-5">
        <Link href="/" target="_self" className="border-5 rounded-3xl p-4">
          liwe.gg
        </Link>
      </h1>
      <p className="text-center pt-5 font-italic">
        League stats you didn't know about yourself!
      </p>
      <br />

      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="pointer-events-auto">
          <Searchbar onSearch={handleSearch}></Searchbar>
        </div>
      </div>

      <p className="text-center text-sm bottom-10 absolute w-full">
        made with FastAPI + Next.js
      </p>
    </>
  );
}
