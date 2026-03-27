"use client";
import { useRef, useEffect, useState } from "react";
import Link from "next/link";
import { useTheme } from "next-themes";

export default function MusicPlayer() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const { theme, setTheme } = useTheme();

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

      <div className="fixed bottom-8 right-8 px-4 py-2 flex items-center gap-3 bg-foreground/5 border border-foreground/10 backdrop-blur-md rounded-md  text-foreground/30">
        <button
          onClick={togglePlay}
          className="cursor-pointer text-sm leading-none hover:text-foreground transition-colors"
          suppressHydrationWarning
        >
          {playing ? "pause" : "play"}
        </button>

        <div className="w-px h-3 bg-foreground/20" />

        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="cursor-pointer text-sm leading-none hover:text-foreground transition-colors"
          suppressHydrationWarning
        >
          {theme === "dark" ? "light" : "dark"}
        </button>

        <div className="w-px h-3 bg-foreground/20" />

        <Link
          href="/"
          className="text-sm leading-none hover:text-red-500 transition-colors "
        >
          home
        </Link>

        <div className="w-px h-3 bg-foreground/20" />

        <Link
          href="/legal"
          className="text-sm leading-none hover:text-foreground transition-colors "
        >
          legal
        </Link>
      </div>
    </>
  );
}
