"use client";
import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import useSWR from "swr";
import { Shell } from "@/components/Shell";
import { FyBars, HBars } from "@/components/Charts";
import { Empty, ErrorState, Kpi, Loading, Panel } from "@/components/ui";
import { AGENCIES, fetcher, int, pct, qs, usd, type Overview } from "@/lib/api";
import { useScope } from "@/lib/scope";

function OverviewPage() {
  const [scope, set] = useScope();
  const { data, error, isLoading, mutate } = useSWR<Overview>(`/v1/overview${qs(scope)}`, fetcher);
  const total = data?.by_fiscal_year.reduce((a, r) => a + Number(r.obligations), 0) ?? 0;
  const awards = data?.by_fiscal_year.reduce((a, r) => a + Number(r.awards), 0) ?? 0;
  const top = data?.top_recipients[0];
  const topShare = top && total ? Number(top.obligations) / total : null;
  const flagged = data ? Object.values(data.anomaly_counts).reduce((a, b) => a + b, 0) : 0;
  const yrs = data?.by_fiscal_year ?? [];
  const last = yrs.length >= 2 ? yrs[yrs.length - 1] : null; const prev = yrs.length >= 2 ? yrs[yrs.length - 2] : null;
  const yoy = last && prev && Number(prev.obligations) ? Number(last.obligations) / Number(prev.obligations) - 1 : null;
  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">Federal IT procurement, with the evidence attached</h1>
        <p className="text-mist-400 mt-1 max-w-3xl">Prime contract obligations for IT services and equipment (PSC D and 70) at six civilian agencies, built from USAspending transaction records through a Databricks Bronze → Silver → Gold pipeline. Every number below is reproducible from one published SQL query.</p>
      </div>
      <Explainer />
      {error && <ErrorState error={error} retry={() => mutate()} />}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <Kpi label="Obligations in scope" value={isLoading ? <span className="skeleton inline-block h-7 w-28" /> : usd(total)} sub={scope.fy ? `FY${scope.fy}` : "FY2022–FY2026 (2026 preliminary)"} />
        <Kpi label="Award-years" value={isLoading ? <span className="skeleton inline-block h-7 w-20" /> : int(awards)} sub="distinct award × fiscal year" />
        <Kpi label="Top recipient share" value={isLoading ? <span className="skeleton inline-block h-7 w-16" /> : pct(topShare)} sub={top ? top.recipient_name : "–"} />
        <Kpi label="Flagged anomalies" value={isLoading ? <span className="skeleton inline-block h-7 w-12" /> : int(flagged)} sub={data ? `${data.anomaly_counts.large_award} large award · ${data.anomaly_counts.concentration} concentration · ${data.anomaly_counts.recipient_growth} growth` : ""} />
      </div>
      <div className="grid lg:grid-cols-5 gap-4">
        <Panel title="Obligations by fiscal year" className="lg:col-span-3" action={yoy != null && <span className={`chip ${yoy >= 0 ? "chip-ok" : "chip-warn"}`}>{yoy >= 0 ? "+" : ""}{pct(yoy)} vs prior year{last?.fiscal_year === 2026 ? " (prelim.)" : ""}</span>}>
          {isLoading ? <Loading rows={6} /> : yrs.length ? <FyBars data={yrs.map((r) => ({ ...r, obligations: Number(r.obligations) }))} /> : <Empty>No rows in this scope.</Empty>}
        </Panel>
        <Panel title="By agency" className="lg:col-span-2">
          {isLoading ? <Loading rows={6} /> : data?.by_agency.length ? (
            <HBars data={data.by_agency.map((r) => ({ ...r, name: AGENCIES[r.awarding_agency_code] ?? r.awarding_agency_name, obligations: Number(r.obligations) }))} nameKey="name" valueKey="obligations" height={240}
              onClick={(row) => set({ agency: String(row.awarding_agency_code) })} />
          ) : <Empty>No rows.</Empty>}
        </Panel>
        <Panel title="Top recipients" className="lg:col-span-3" action={<Link className="link text-xs" href={`/agency${qs(scope)}`}>Explore →</Link>}>
          {isLoading ? <Loading rows={8} /> : data?.top_recipients.length ? (
            <table className="tbl"><thead><tr><th>Recipient</th><th className="num">Obligations</th><th className="num">Share</th><th className="num">Awards</th></tr></thead>
              <tbody>{data.top_recipients.map((r) => (
                <tr key={r.recipient_uei}><td><button className="link text-left" onClick={() => set({ recipient: r.recipient_uei })}>{r.recipient_name}</button></td>
                  <td className="num">{usd(r.obligations)}</td><td className="num">{pct(Number(r.obligations) / total)}</td><td className="num">{int(r.awards)}</td></tr>))}</tbody></table>
          ) : <Empty>No recipients in this scope.</Empty>}
        </Panel>
        <Panel title="Product/service classes" className="lg:col-span-2" action={<span className="text-xs text-mist-500">2-character PSC</span>}>
          {isLoading ? <Loading rows={8} /> : data?.psc_mix.length ? (
            <table className="tbl"><thead><tr><th>PSC</th><th className="num">Obligations</th><th className="num">Share</th></tr></thead>
              <tbody>{data.psc_mix.map((r) => (<tr key={r.psc_class2}><td><span className="font-mono text-mist-300">{r.psc_class2}</span> <span className="text-mist-400 text-xs">{r.description}</span></td><td className="num">{usd(r.obligations)}</td><td className="num">{pct(Number(r.obligations) / total)}</td></tr>))}</tbody></table>
          ) : <Empty>No rows.</Empty>}
        </Panel>
      </div>
      <div className="mt-6 grid md:grid-cols-3 gap-3 text-sm">
        <Link href={`/anomalies${qs(scope)}`} className="panel p-4 hover:border-signal/50"><div className="font-medium">Anomaly Lab →</div><div className="text-mist-400 mt-1">Statistically unusual awards, with the peer group, baseline and score behind every flag.</div></Link>
        <Link href={`/investigator${qs(scope)}`} className="panel p-4 hover:border-signal/50"><div className="font-medium">AI Investigator →</div><div className="text-mist-400 mt-1">Ask a question; get facts computed by SQL, cited award ids, and the model’s reading kept separate.</div></Link>
        <Link href="/methodology" className="panel p-4 hover:border-signal/50"><div className="font-medium">Methodology →</div><div className="text-mist-400 mt-1">Definitions, pipeline, reconciliation results, anomaly math, AI limits, and the SQL behind each figure.</div></Link>
      </div>
    </>
  );
}

function Explainer() {
  // Plain-language orientation for non-technical visitors. Open on a first visit; the choice is remembered per browser only.
  const [open, setOpen] = useState(true);
  useEffect(() => { try { if (localStorage.getItem("civiclens.explainer") === "closed") setOpen(false); } catch { /* storage unavailable */ } }, []);
  const toggle = () => { setOpen((o) => { try { localStorage.setItem("civiclens.explainer", o ? "closed" : "open"); } catch { /* ignore */ } return !o; }); };
  return (
    <section className="panel p-4 mb-6" aria-labelledby="explainer-h">
      <div className="flex items-center justify-between gap-3">
        <h2 id="explainer-h" className="text-sm font-semibold text-mist-100">What am I looking at?</h2>
        <button className="ghost text-xs" onClick={toggle} aria-expanded={open} aria-controls="explainer-body">{open ? "Hide" : "Show"}</button>
      </div>
      {open && (
        <div id="explainer-body" className="mt-3 grid md:grid-cols-4 gap-4 text-sm text-mist-300">
          <div><div className="font-medium text-mist-100 mb-1">The data</div>Every IT contract transaction the federal government reported to USAspending.gov for six civilian agencies, fiscal years 2022–2026 (Oct–Sep). About 110,000 records, pulled directly from the source and re-counted against it.</div>
          <div><div className="font-medium text-mist-100 mb-1">The numbers</div>“Obligations” are dollars the government committed on contracts, not dollars paid out. An award is one contract; an award-year is that contract’s activity in one fiscal year. Use the filters above to narrow to an agency, a year, or a product class.</div>
          <div><div className="font-medium text-mist-100 mb-1">The flags</div>“Flagged anomalies” are awards, recipients or categories that are statistically unusual next to comparable ones — an award far larger than its peers, one vendor holding most of a category, a vendor growing several-fold in a year. A flag is a comparison, not an accusation; click “Why?” in the Anomaly Lab to see exactly what it was compared with.</div>
          <div><div className="font-medium text-mist-100 mb-1">The AI Investigator</div>Ask a question in plain English. The AI decides which of the dashboard’s own queries to run; the server then re-checks every number it states against those query results and removes anything it cannot trace. It will not guess, go outside the data, or call spending wasteful or fraudulent.</div>
        </div>
      )}
    </section>
  );
}

export default function Page() {
  return <Shell><Suspense fallback={<Loading rows={8} />}><OverviewPage /></Suspense></Shell>;
}
