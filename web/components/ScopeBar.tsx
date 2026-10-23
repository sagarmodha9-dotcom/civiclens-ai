"use client";
import { AGENCIES, FYS, PRELIMINARY_FY } from "@/lib/api";
import { useScope } from "@/lib/scope";

const PSC = [["", "All IT"], ["D3", "D3 · IT & telecom services"], ["70", "70 · IT equipment & software"]];

export function ScopeBar() {
  const [scope, set] = useScope();
  return (
    <div className="border-b border-ink-700/70 bg-ink-900/60">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-2 flex flex-wrap items-center gap-2 text-sm" role="group" aria-label="Dashboard scope">
        <span className="text-xs uppercase tracking-wider text-mist-500 mr-1">Scope</span>
        <select aria-label="Agency" value={scope.agency ?? ""} onChange={(e) => set({ agency: e.target.value || undefined })}>
          <option value="">All six agencies</option>
          {Object.entries(AGENCIES).map(([c, n]) => <option key={c} value={c}>{n}</option>)}
        </select>
        <select aria-label="Fiscal year" value={scope.fy ?? ""} onChange={(e) => set({ fy: e.target.value ? Number(e.target.value) : undefined })}>
          <option value="">FY2022–FY2026</option>
          {FYS.map((y) => <option key={y} value={y}>FY{y}{y === PRELIMINARY_FY ? " (preliminary)" : ""}</option>)}
        </select>
        <select aria-label="PSC class" value={scope.psc ?? ""} onChange={(e) => set({ psc: e.target.value || undefined })}>
          {PSC.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
        </select>
        {scope.recipient && <button className="chip" onClick={() => set({ recipient: undefined })} aria-label="Clear recipient filter">recipient {scope.recipient} ✕</button>}
        {(scope.agency || scope.fy || scope.psc || scope.recipient) && (
          <button className="ghost ml-auto" onClick={() => set({ agency: undefined, fy: undefined, psc: undefined, recipient: undefined })}>Reset</button>
        )}
        {scope.fy === PRELIMINARY_FY && <span className="chip chip-warn">FY2026 ended Sep 30, 2026 · subject to reporting lag and revision</span>}
      </div>
    </div>
  );
}
