import type { Metadata } from "next";
import { Geist, Geist_Mono, DotGothic16 } from "next/font/google";
import "./globals.css";
import MusicPlayer from "@/components/MusicPlayer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const dotGothic16 = DotGothic16({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-dotgothic16",
});

export const metadata: Metadata = {
  title: "liwe.gg",
  description: "Learn more about your personal League stats!",
  openGraph: {
    title: "liwe.gg Home Page",
    description: "Your own League Stats!",
    url: "https://liwegg.vercel.app/",
    siteName: "liwe.gg",
    locale: "en-US",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        // className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        className={`${dotGothic16.variable} antialiased`}
      >
        {children}
        <MusicPlayer></MusicPlayer>
      </body>
    </html>
  );
}
