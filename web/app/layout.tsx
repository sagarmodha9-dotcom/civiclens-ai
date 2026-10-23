import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "CivicLens AI — Federal IT Procurement Intelligence", template: "%s · CivicLens AI" },
  description: "Real USAspending contract data for six agencies, FY2022–FY2026: trends, vendor concentration, explainable anomalies and a grounded AI investigator.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}
