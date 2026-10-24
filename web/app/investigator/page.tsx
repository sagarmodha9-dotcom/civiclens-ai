"use client";
import { Suspense, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import useSWR from "swr";
import { Shell } from "@/components/Shell";
import { Empty, ErrorState, Loading, Panel } from "@/components/ui";
import { AGENCIES, fetcher, postStream, usd, type Investigation, type Progress } from "@/lib/api";
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
  const [steps, setSteps] = useState<Progress[]>([]);
  const [elapsed, setElapsed] = useState(0);
  const t0 = useRef(0);
  useEffect(() => {
    if (!busy) return;
    t0.current = Date.now(); setElapsed(0);
    const id = setInterval(() => setElapsed(Math.round((Date.now() - t0.current) / 1000)), 1000);
    return () => clearInterval(id);
  }, [busy]);
  async function ask(question: string) {
    setBusy(true); setErr(null); setRes(null); setQ(question); setSteps([]);
    try {
      const r = await postStream<Investigation>("/v1/investigate/stream",
        { question, agency: scope.agency, fy: scope.fy, psc: scope.psc, recipient: scope.recipient, selected_award_key: selectedAward, selected_fy: selectedAward ? scope.fy : undefined },
        (p) => setSteps((prev) => [...prev, p]));
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
          {busy && <Panel title={<span>Working <span className="text-xs text-mist-500 font-normal ml-2">{elapsed}s · live answers usually take 10–40 s</span></span>}>
            <ProgressList steps={steps} />
          </Panel>}
          {err != null && <ErrorState error={err} />}
          {res && res.status !== "ok" && <Panel title={res.status === "limited" ? "Live questions paused" : res.status === "unavailable" ? "Live AI is off" : "Something went wrong"}>
            <p className="text-sm text-mist-300">{res.reason}</p>
            <p className="text-xs text-mist-500 mt-2">{res.status === "limited" ? "Rate limits protect a fixed monthly budget. Questions that have already been asked on this snapshot (including the sample questions) are served from cache and still work." : res.status === "unavailable" ? "Sample questions that were answered earlier are still served from cache." : "Please try again in a moment."}</p>
          </Panel>}
          {res?.status === "ok" && res.cached && (
            <div role="status" className="rounded-lg border border-amber/40 bg-amber/5 px-4 py-3 text-sm">
              <span className="font-medium text-amber">Cached answer.</span> <span className="text-mist-300">This exact question was asked before in this scope on snapshot {res.snapshot_version}; you are seeing that stored answer, not a newly generated one. The data has not changed, so the numbers are the same the model would compute now.</span>
            </div>
          )}
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
                <div className="mt-3 text-xs text-mist-500">Tools: {res.tool_log?.filter((t) => !t.id.startsWith("ctx_")).map((t) => `${t.name}(${Object.entries(t.args).map(([k, val]) => `${k}=${val}`).join(", ")})`).join(" → ") || "none"}{res.tool_log?.some((t) => t.id.startsWith("ctx_")) && " · context: active scope" }{res.tool_log?.some((t) => t.id === "ctx_selected_anomaly") && " + selected anomaly"}{res.usage && ` · ${res.usage.input_tokens + res.usage.output_tokens} tokens · $${res.usage.usd.toFixed(4)}`}{res.cached && " · cached"}{res.usage?.regenerated && " · regenerated once after verification"}</div>
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
const STAGE_LABEL: Record<Progress["stage"], string> = {
  queued: "Request received",
  model: "Model is planning which queries to run",
  tool: "Running query",
  verify: "Server is verifying every fact against the query results",
  regenerate: "Verification found a problem — asking the model to correct it",
};
const TOOL_LABEL: Record<string, string> = {
  aggregate_spend: "aggregate_spend (sum obligations in scope)", year_over_year_recipients: "year_over_year_recipients (this year vs prior year)",
  list_anomalies: "list_anomalies (flagged awards in scope)", anomaly_explanation: "anomaly_explanation (peer group and baseline)",
  award_detail: "award_detail (one award, all years)", search_awards: "search_awards (find an award)",
};
function ProgressList({ steps }: { steps: Progress[] }) {
  // Only steps the server has reported are shown; the last one is the step in progress. Nothing here is a timer or a guess.
  const shown = steps.length ? steps : [{ stage: "queued", t: 0 } as Progress];
  return (
    <ol className="text-sm space-y-1.5" aria-live="polite" aria-label="Progress">
      {shown.map((p, i) => {
        const last = i === shown.length - 1;
        const label = p.stage === "tool" ? `${STAGE_LABEL.tool}: ${TOOL_LABEL[p.tool ?? ""] ?? p.tool}` : p.stage === "model" && (p.attempt ?? 1) > 1 ? "Model is revising its answer" : STAGE_LABEL[p.stage] ?? p.stage;
        return (
          <li key={i} className={`flex items-start gap-2 ${last ? "text-mist-100" : "text-mist-500"}`}>
            <span aria-hidden="true" className={`mt-1 inline-block h-2 w-2 rounded-full ${last ? "bg-signal animate-pulse" : "bg-mint"}`} />
            <span>{label}{last ? "…" : ""}</span>
          </li>
        );
      })}
    </ol>
  );
}

export default function Page() { return <Shell><Suspense fallback={<Loading rows={8} />}><Investigator /></Suspense></Shell>; }
