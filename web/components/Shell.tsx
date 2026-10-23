"use client";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import useSWR from "swr";
import { Suspense } from "react";
import { fetcher, type Meta } from "@/lib/api";
import { ScopeBar } from "./ScopeBar";

const NAV = [["/", "Overview"], ["/agency", "Agency Explorer"], ["/anomalies", "Anomaly Lab"], ["/investigator", "AI Investigator"], ["/methodology", "Methodology"]] as const;

function NavLinks({ path, mobile = false }: { path: string; mobile?: boolean }) {
  const sp = useSearchParams(); const q = sp.toString() ? `?${sp.toString()}` : "";
  return <>{NAV.map(([href, label]) => (
    <Link key={href} href={href === "/methodology" ? href : `${href}${q}`} aria-current={path === href ? "page" : undefined}
      className={mobile ? `whitespace-nowrap px-3 py-1 rounded-md ${path === href ? "bg-ink-800 text-mist-50" : "text-mist-400"}`
        : `px-3 py-1.5 rounded-md ${path === href ? "bg-ink-800 text-mist-50" : "text-mist-400 hover:text-mist-100 hover:bg-ink-850"}`}>{label}</Link>
  ))}</>;
}

export function Shell({ children, scoped = true }: { children: React.ReactNode; scoped?: boolean }) {
  const path = usePathname();
  const { data: meta, error } = useSWR<Meta>("/v1/meta", fetcher, { revalidateOnFocus: false });
  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-20 border-b border-ink-700/70 bg-ink-950/90 backdrop-blur">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 flex items-center gap-4 h-14">
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <span className="inline-grid h-7 w-7 place-items-center rounded-md bg-signal/15 text-signal font-bold">C</span>
            <span className="font-semibold tracking-tight">CivicLens <span className="text-mist-400 font-normal">AI</span></span>
          </Link>
          <nav aria-label="Primary" className="ml-2 hidden md:flex items-center gap-1 text-sm"><Suspense fallback={null}><NavLinks path={path} /></Suspense></nav>
          <div className="ml-auto flex items-center gap-2 text-xs text-mist-400">
            {meta ? (
              <span className="chip" title={`Built ${meta.built_utc}`}>snapshot {meta.snapshot_version}{meta.api_last_updated?.length ? ` · USAspending as of ${meta.api_last_updated.join("/")}` : ""}</span>
            ) : error ? <span className="chip chip-warn">API unreachable</span> : <span className="skeleton h-5 w-40" />}
          </div>
        </div>
        <nav aria-label="Primary mobile" className="md:hidden flex overflow-x-auto gap-1 px-3 pb-2 text-sm"><Suspense fallback={null}><NavLinks path={path} mobile /></Suspense></nav>
      </header>
      {scoped && <Suspense fallback={null}><ScopeBar /></Suspense>}
      <main className="mx-auto w-full max-w-7xl px-4 sm:px-6 py-6 flex-1">{children}</main>
      <footer className="border-t border-ink-700/70 text-xs text-mist-500">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 py-4 flex flex-wrap gap-x-6 gap-y-1">
          <span>Source: USAspending.gov (prime contract transactions, PSC D/70, awarding agencies VA, DHS, HHS, Treasury, Commerce, SSA).</span>
          <span>FY2026 is preliminary.</span>
          <span>Anomalies are statistical comparisons, not findings of wrongdoing.</span>
          <a className="link" href="https://github.com/sagarmodha9-dotcom/civiclens-ai" target="_blank" rel="noreferrer">Source code</a>
          {meta && <span>schema v{meta.schema_version ?? 1}</span>}
        </div>
      </footer>
    </div>
  );
}
