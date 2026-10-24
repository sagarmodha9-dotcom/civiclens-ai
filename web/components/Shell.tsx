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
            <a className="chip hover:text-mist-100" href="https://github.com/sagarmodha9-dotcom/civiclens-ai" target="_blank" rel="noreferrer" aria-label="Source code on GitHub">
              <svg aria-hidden="true" viewBox="0 0 16 16" width="14" height="14" fill="currentColor" className="inline -mt-0.5 mr-1"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>GitHub
            </a>
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
          <span>Built by <a className="link" href="https://www.linkedin.com/in/sagarmodha/" target="_blank" rel="noreferrer">Sagar Modha</a></span>
          {meta && <span>schema v{meta.schema_version ?? 1}</span>}
        </div>
      </footer>
    </div>
  );
}
