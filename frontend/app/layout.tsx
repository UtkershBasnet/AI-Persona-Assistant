import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Utkersh Basnet — AI Persona",
  description:
    "Chat with Utkersh Basnet's AI persona. Ask about his projects, skills, experience, and book an interview.",
  keywords: [
    "Utkersh Basnet",
    "AI Persona",
    "Software Engineer",
    "Full Stack Developer",
    "Interview",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
