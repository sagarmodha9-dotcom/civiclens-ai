"use client";
import type { ReactNode } from "react";

export function Kpi({ label, value, sub }: { label: string; value: ReactNode; sub?: ReactNode }) {
  return <div className="kpi"><span className="label">{label}</span><span className="value">{value}</span>{sub && <span className="sub">{sub}</span>}</div>;
}
export function Panel({ title, children, action, className = "" }: { title?: ReactNode; children: ReactNode; action?: ReactNode; className?: string }) {
  return (
    <section className={`panel p-5 ${className}`}>
      {(title || action) && <div className="mb-3 flex items-center justify-between gap-3"><h2 className="text-sm font-semibold text-mist-100">{title}</h2>{action}</div>}
      {children}
    </section>
  );
}
export function Loading({ rows = 4 }: { rows?: number }) {
  return <div className="space-y-2" role="status" aria-live="polite" aria-label="Loading">{Array.from({ length: rows }).map((_, i) => <div key={i} className="skeleton h-4" style={{ width: `${90 - i * 12}%` }} />)}</div>;
}
export function ErrorState({ error, retry }: { error: unknown; retry?: () => void }) {
  const msg = error instanceof Error ? error.message : String(error);
  return (
    <div role="alert" className="rounded-lg border border-rose/30 bg-rose/5 p-4 text-sm">
      <div className="font-medium text-rose">Couldn’t load this section</div>
      <div className="text-mist-400 mt-1">{msg}</div>
      {retry && <button className="ghost mt-3" onClick={retry}>Try again</button>}
    </div>
  );
}
export function Empty({ children }: { children: ReactNode }) {
  return <div className="rounded-lg border border-dashed border-ink-700 p-6 text-center text-sm text-mist-400">{children}</div>;
}
export function Status({ s }: { s: string }) {
  const cls = s === "flagged" ? "chip chip-flag" : s === "normal" ? "chip chip-ok" : "chip";
  return <span className={cls}>{s}</span>;
}
