"use client";
import { useRef, useEffect, useState } from "react";
import Link from "next/link";

export default function MusicPlayer() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.volume = 0.125;

    const handlePlay = () => setPlaying(true);
    const handlePause = () => setPlaying(false);

    audio.addEventListener("play", handlePlay);
    audio.addEventListener("pause", handlePause);

    const unlock = () => {
      audio.play();
      window.removeEventListener("click", unlock);
    };
    window.addEventListener("click", unlock);

    return () => {
      window.removeEventListener("click", unlock);
      audio.removeEventListener("play", handlePlay);
      audio.removeEventListener("pause", handlePause);
    };
  }, []);

  const togglePlay = () => {
    if (!audioRef.current) return;
    audioRef.current.paused
      ? audioRef.current.play()
      : audioRef.current.pause();
  };

  return (
    <>
      <audio ref={audioRef} src="/music/lightsout.mp3" loop />

      <div className="fixed bottom-8 right-8 px-4 py-2 flex items-center gap-3 bg-white/5 border border-white/10 backdrop-blur-md rounded-md  text-white/30">
        <button
          onClick={togglePlay}
          className="cursor-pointer text-sm leading-none hover:text-white transition-colors"
          suppressHydrationWarning
        >
          {playing ? "pause" : "play"}
        </button>

        <div className="w-px h-3 bg-white/20" />

        <Link
          href="/"
          className="text-sm leading-none hover:text-white transition-colors "
        >
          home
        </Link>

        <div className="w-px h-3 bg-white/20" />

        <Link
          href="/legal"
          className="text-sm leading-none hover:text-white transition-colors "
        >
          legal
        </Link>
      </div>
    </>
  );
}
