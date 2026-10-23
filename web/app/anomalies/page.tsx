"use client";
import { Suspense, useState } from "react";
import Link from "next/link";
import useSWR from "swr";
import { Shell } from "@/components/Shell";
import { Empty, ErrorState, Loading, Panel, Status } from "@/components/ui";
import { AGENCIES, fetcher, int, pct, qs, usd, type Anomaly, type AnomalyDetail, type Meta } from "@/lib/api";
import { useScope } from "@/lib/scope";

const DETECTORS = [["large_award", "Unusually large award"], ["concentration", "Vendor concentration"], ["recipient_growth", "Abrupt recipient growth"]] as const;

function Detail({ awardKey, fy, onClose }: { awardKey: string; fy: number; onClose: () => void }) {
  const { data, error, isLoading } = useSWR<AnomalyDetail>(`/v1/anomalies/${encodeURIComponent(awardKey)}/${fy}`, fetcher);
  return (
    <Panel title={<span>Why this award-year was scored <span className="font-mono text-mist-400 text-xs ml-2">{awardKey} · FY{fy}</span></span>} action={<button className="ghost" onClick={onClose}>Close</button>}>
      {isLoading && <Loading rows={8} />}{error && <ErrorState error={error} />}
      {data && (
        <div className="grid lg:grid-cols-3 gap-5 text-sm">
          <div className="space-y-2">
            <div className="text-xs uppercase tracking-wider text-mist-500">Comparison</div>
            <dl className="grid grid-cols-2 gap-y-1">
              <dt className="text-mist-400">Value</dt><dd className="num">{usd(data.value, false)}</dd>
              <dt className="text-mist-400">Unit</dt><dd>{data.unit}</dd>
              <dt className="text-mist-400">Peer group</dt><dd>{AGENCIES[data.awarding_agency_code] ?? data.awarding_agency_name} · PSC {data.psc_class2} · FY{data.fiscal_year}</dd>
              <dt className="text-mist-400">Peer size</dt><dd className="num">{int(data.peer_n)}</dd>
              <dt className="text-mist-400">Baseline median</dt><dd className="num">{usd(data.baseline_median ?? 0, false)}</dd>
              <dt className="text-mist-400">Robust z (log10)</dt><dd className="num">{Number(data.score).toFixed(2)} vs {data.threshold}</dd>
              <dt className="text-mist-400">Status</dt><dd><Status s={data.status} /></dd>
            </dl>
            <p className="text-xs text-mist-400 pt-2 border-t border-ink-800">{data.limits}</p>
            <div className="flex gap-2 pt-1">
              {data.usaspending_permalink && <a className="link text-xs" href={data.usaspending_permalink} target="_blank" rel="noreferrer">Open on USAspending ↗</a>}
              <Link className="link text-xs" href={`/investigator?agency=${data.awarding_agency_code}&fy=${fy}&award=${encodeURIComponent(awardKey)}`}>Ask the investigator →</Link>
            </div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-mist-500 mb-2">Transactions in the snapshot ({data.transactions.length})</div>
            <div className="max-h-72 overflow-auto"><table className="tbl"><thead><tr><th>Date</th><th>Mod</th><th className="num">Obligation</th><th>Type</th></tr></thead>
              <tbody>{data.transactions.map((t) => (<tr key={t.transaction_key}><td className="font-mono text-xs">{t.action_date}</td><td className="font-mono text-xs">{t.modification_number}</td><td className={`num ${Number(t.obligation) < 0 ? "text-rose" : ""}`}>{usd(t.obligation, false)}</td><td className="text-xs text-mist-400">{t.action_type}</td></tr>))}</tbody></table></div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-mist-500 mb-2">Peer group sample (largest first)</div>
            <div className="max-h-72 overflow-auto"><table className="tbl"><thead><tr><th>Recipient</th><th className="num">Value</th><th className="num">z</th></tr></thead>
              <tbody>{data.peer_group_sample.map((p) => (<tr key={p.award_key} className={p.award_key === awardKey ? "bg-signal/10" : ""}><td className="text-xs">{p.recipient_name}</td><td className="num">{usd(p.value)}</td><td className="num">{p.score == null ? "–" : Number(p.score).toFixed(2)}</td></tr>))}</tbody></table></div>
          </div>
        </div>
      )}
    </Panel>
  );
}

function AnomalyLab() {
  const [scope] = useScope();
  const [detector, setDetector] = useState<(typeof DETECTORS)[number][0]>("large_award");
  const [sel, setSel] = useState<{ key: string; fy: number } | null>(null);
  const { data, error, isLoading, mutate } = useSWR<{ items: Anomaly[] }>(`/v1/anomalies${qs(scope, { detector, limit: 100 })}`, fetcher);
  const { data: meta } = useSWR<Meta>("/v1/meta", fetcher);
  const summ = meta?.anomaly_summary?.[detector];
  return (
    <>
      <div className="mb-5">
        <h1 className="text-2xl font-semibold tracking-tight">Anomaly Lab</h1>
        <p className="text-mist-400 mt-1 max-w-3xl">Each flag is a statistical comparison with its peer group, baseline, score and threshold shown. “Flagged” means unusual relative to that comparison group; it is not a finding of wrongdoing, and small groups abstain rather than score.</p>
      </div>
      <div className="flex flex-wrap items-center gap-2 mb-4" role="tablist" aria-label="Detector">
        {DETECTORS.map(([k, l]) => <button key={k} role="tab" aria-selected={detector === k} className={detector === k ? "primary" : "ghost"} onClick={() => { setDetector(k); setSel(null); }}>{l}</button>)}
        {summ && <span className="chip ml-auto" title="Counts across the whole snapshot, before scope filters">{int(summ.flagged)} flagged · {int(summ.scored)} scored · {int(summ.rows)} rows{Object.keys(summ.not_scored).length ? ` · ${int(summ.rows - summ.scored)} not scored` : ""}</span>}
      </div>
      {sel && <div className="mb-4"><Detail awardKey={sel.key} fy={sel.fy} onClose={() => setSel(null)} /></div>}
      <Panel title={`Flagged in scope: ${data ? int(data.items.length) : "…"}`} action={error ? <button className="ghost" onClick={() => mutate()}>Retry</button> : undefined}>
        {error && <ErrorState error={error} retry={() => mutate()} />}
        {isLoading ? <Loading rows={10} /> : !data?.items.length ? <Empty>No flagged items in this scope for this detector. {summ && summ.flagged === 0 ? "Nothing in the whole snapshot met the threshold with a large enough peer group." : "Widen the scope."}</Empty> : (
          <div className="overflow-x-auto"><table className="tbl">
            <thead>{detector === "large_award" ? <tr><th>Award</th><th>Agency</th><th>FY</th><th>Recipient</th><th>PSC</th><th className="num">Value</th><th className="num">Peers</th><th className="num">Median</th><th className="num">z</th><th></th></tr>
              : detector === "concentration" ? <tr><th>Agency</th><th>PSC class</th><th>FY</th><th className="num">Cell spend</th><th className="num">Recipients</th><th className="num">HHI</th><th className="num">Top share</th><th>Top recipient</th><th className="num">Δ HHI</th></tr>
              : <tr><th>Recipient</th><th>Agency</th><th>FY</th><th className="num">Prior FY</th><th className="num">This FY</th><th className="num">Ratio</th><th className="num">Awards</th></tr>}</thead>
            <tbody>{data.items.map((a, i) => detector === "large_award" ? (
              <tr key={`${a.award_key}-${a.fiscal_year}`}><td className="font-mono text-xs">{a.piid}</td><td className="text-xs">{AGENCIES[a.awarding_agency_code]}</td><td>{a.fiscal_year}</td><td className="text-xs">{a.recipient_name}</td><td className="font-mono text-xs">{a.psc}</td>
                <td className="num">{usd(a.value)}</td><td className="num">{int(a.peer_n)}</td><td className="num">{usd(a.baseline_median ?? 0)}</td><td className="num font-medium text-rose">{Number(a.score).toFixed(2)}</td>
                <td><button className="link text-xs" onClick={() => setSel({ key: a.award_key!, fy: a.fiscal_year })}>Why?</button></td></tr>
            ) : detector === "concentration" ? (
              <tr key={i}><td className="text-xs">{AGENCIES[a.awarding_agency_code]}</td><td className="font-mono">{a.psc_class2}</td><td>{a.fiscal_year}</td><td className="num">{usd(a.value)}</td><td className="num">{int(a.peer_n)}</td><td className="num font-medium text-rose">{Math.round(Number(a.score)).toLocaleString()}</td><td className="num">{pct(Number(a.top_share) / 100)}</td><td className="text-xs">{a.top_recipient_name}</td><td className="num">{a.hhi_change == null ? "–" : Math.round(Number(a.hhi_change)).toLocaleString()}</td></tr>
            ) : (
              <tr key={i}><td className="text-xs">{a.recipient_name}</td><td className="text-xs">{AGENCIES[a.awarding_agency_code]}</td><td>{a.fiscal_year}</td><td className="num">{usd(a.baseline ?? 0)}</td><td className="num">{usd(a.value)}</td><td className="num font-medium text-rose">{Number(a.score).toFixed(1)}×</td><td className="num">{int(a.awards ?? 0)}</td></tr>
            ))}</tbody></table></div>
        )}
        {data?.items[0] && <p className="mt-3 text-xs text-mist-500">{data.items[0].limits}</p>}
      </Panel>
    </>
  );
}
export default function Page() { return <Shell><Suspense fallback={<Loading rows={8} />}><AnomalyLab /></Suspense></Shell>; }
