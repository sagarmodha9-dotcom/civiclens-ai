"use client";
import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import useSWR from "swr";
import { Shell } from "@/components/Shell";
import { Empty, ErrorState, Loading, Panel } from "@/components/ui";
import { AGENCIES, fetcher, postJSON, usd, type Investigation } from "@/lib/api";
import { useScope } from "@/lib/scope";

function Investigator() {
  const [scope] = useScope();
  const sp = useSearchParams();
  const selectedAward = sp.get("award") || undefined;
  const { data: samples } = useSWR<{ questions: string[]; live: boolean; model: string; limits: { per_ip_per_hour: number; global_per_day: number } }>("/v1/investigate/samples", fetcher);
  const [q, setQ] = useState(selectedAward ? "Why was this award flagged, and what was it compared against?" : "");
  const [busy, setBusy] = useState(false);
  const [res, setRes] = useState<Investigation | null>(null);
  const [err, setErr] = useState<unknown>(null);
  async function ask(question: string) {
    setBusy(true); setErr(null); setRes(null); setQ(question);
    try {
      const r = await postJSON<Investigation>("/v1/investigate", { question, agency: scope.agency, fy: scope.fy, psc: scope.psc, recipient: scope.recipient, selected_award_key: selectedAward, selected_fy: selectedAward ? scope.fy : undefined });
      setRes(r);
    } catch (e) { setErr(e); } finally { setBusy(false); }
  }
  const a = res?.answer; const v = res?.verification;
  return (
    <>
      <div className="mb-5">
        <h1 className="text-2xl font-semibold tracking-tight">AI Investigator</h1>
        <p className="text-mist-400 mt-1 max-w-3xl">Ask about the data in the current scope. The model plans; SQL computes; every number is checked server-side against the exact tool call that produced it. Facts, interpretation and limits are kept apart, and award ids are cited so you can open the source record.</p>
      </div>
      <div className="grid lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          <Panel title={<span>Question <span className="text-xs text-mist-500 font-normal ml-2">scope: {scope.agency ? AGENCIES[scope.agency] : "all agencies"}{scope.fy ? ` · FY${scope.fy}` : ""}{scope.psc ? ` · PSC ${scope.psc}` : ""}{selectedAward ? ` · award ${selectedAward}` : ""}</span></span>}>
            <form onSubmit={(e) => { e.preventDefault(); if (q.trim().length >= 5) ask(q.trim()); }} className="flex flex-col gap-2">
              <textarea aria-label="Your question" value={q} onChange={(e) => setQ(e.target.value)} rows={3} maxLength={600} className="rounded-md border border-ink-700 bg-ink-850 px-3 py-2 text-sm outline-none focus:border-signal" placeholder="e.g. Which recipients grew fastest versus the prior fiscal year, and by how much?" />
              <div className="flex items-center gap-2">
                <button type="submit" className="primary" disabled={busy || q.trim().length < 5}>{busy ? "Investigating…" : "Ask"}</button>
                {samples && <span className="text-xs text-mist-500">{samples.live ? `live · ${samples.model} · ${samples.limits.per_ip_per_hour}/hour per visitor` : "live AI is off on this deployment; cached sample answers only"}</span>}
              </div>
            </form>
            <div className="mt-3 flex flex-wrap gap-2">{(samples?.questions ?? []).map((s) => <button key={s} className="chip hover:border-signal/60" onClick={() => ask(s)} disabled={busy}>{s}</button>)}</div>
          </Panel>
          {busy && <Panel><Loading rows={6} /><p className="text-xs text-mist-500 mt-2">Running tools against the snapshot, then verifying the answer…</p></Panel>}
          {err != null && <ErrorState error={err} />}
          {res && res.status !== "ok" && <Panel><Empty>{res.reason}</Empty></Panel>}
          {res?.status === "ok" && a && (
            <>
              <Panel title="Facts (computed by SQL, verified)" action={v && <span className={`chip ${v.ok ? "chip-ok" : "chip-warn"}`}>{v.ok ? "all facts verified" : `${v.unverified_facts.length} unverified`}</span>}>
                {a.facts.length ? (
                  <table className="tbl"><thead><tr><th>Claim</th><th className="num">Value</th><th>Measure · entities · FY</th><th>From</th></tr></thead>
                    <tbody>{a.facts.map((f, i) => { const bad = v?.unverified_facts.find((u) => u.claim === f.claim); return (
                      <tr key={i} className={bad ? "opacity-60" : ""}><td>{f.claim}{bad && <span className="chip chip-warn ml-2" title={bad.why}>unverified</span>}</td>
                        <td className="num">{typeof f.value === "number" ? (f.unit.toLowerCase().includes("usd") || f.measure.includes("oblig") ? usd(f.value, false) : f.value.toLocaleString()) : f.value}{f.unit && typeof f.value === "number" && !f.unit.toLowerCase().includes("usd") ? ` ${f.unit}` : ""}</td>
                        <td className="text-xs text-mist-400">{f.measure}{f.entities.length ? ` · ${f.entities.join(", ")}` : ""}{f.fiscal_years.length ? ` · FY${f.fiscal_years.join(", FY")}` : ""}</td>
                        <td className="font-mono text-xs text-mist-500">{res.tool_log?.find((t) => t.id === f.tool_call_id)?.name ?? f.tool_call_id}</td></tr>); })}</tbody></table>
                ) : <Empty>{a.insufficient_evidence ? "The investigator found no evidence in scope for this question." : "No numeric facts were needed."}</Empty>}
              </Panel>
              <Panel title="Interpretation (model’s reading of the facts)" action={a.insufficient_evidence && <span className="chip chip-warn">insufficient evidence</span>}>
                <p className="text-sm leading-relaxed whitespace-pre-line">{a.interpretation}</p>
                {a.limits && <p className="mt-3 text-xs text-mist-400 border-t border-ink-800 pt-3"><span className="uppercase tracking-wider text-mist-500 mr-2">Limits</span>{a.limits}</p>}
              </Panel>
              <Panel title="Citations and tools">
                <div className="flex flex-wrap gap-2 text-xs">
                  {a.citations.map((c) => <a key={c} className={`chip ${v?.bad_citations.includes(c) ? "chip-warn" : ""}`} href={`https://www.usaspending.gov/award/${encodeURIComponent(c)}/`} target="_blank" rel="noreferrer">{c} ↗</a>)}
                  {!a.citations.length && <span className="text-mist-500">No award-level citations in this answer.</span>}
                </div>
                <div className="mt-3 text-xs text-mist-500">Tools: {res.tool_log?.map((t) => `${t.name}(${Object.entries(t.args).map(([k, val]) => `${k}=${val}`).join(", ")})`).join(" → ") || "none"}{res.usage && ` · ${res.usage.input_tokens + res.usage.output_tokens} tokens · $${res.usage.usd.toFixed(4)}`}{res.cached && " · cached"}{res.usage?.regenerated && " · regenerated once after verification"}</div>
              </Panel>
            </>
          )}
        </div>
        <div className="space-y-4">
          <Panel title="How an answer is produced">
            <ol className="text-sm space-y-2 text-mist-300 list-decimal pl-4">
              <li>Your question and the active scope go to the model with six read-only tools.</li>
              <li>Each tool runs one of the dashboard’s own SQL queries, inside the scope.</li>
              <li>The model returns structured output: facts with tool ids, interpretation, citations, limits.</li>
              <li>The server re-checks every fact against the matching tool rows (value, entities, fiscal years) and every citation against the snapshot.</li>
              <li>Misconduct vocabulary is never produced; anomalies are described as unusual relative to a comparison group.</li>
            </ol>
          </Panel>
          <Panel title="What it will not do"><ul className="text-sm space-y-1 text-mist-300 list-disc pl-4"><li>Run arbitrary SQL or leave the active scope</li><li>Invent numbers, award ids or causes</li><li>Characterise spending as fraud, waste or abuse</li><li>Answer about agencies or years outside the snapshot</li></ul></Panel>
        </div>
      </div>
    </>
  );
}
export default function Page() { return <Shell><Suspense fallback={<Loading rows={8} />}><Investigator /></Suspense></Shell>; }
