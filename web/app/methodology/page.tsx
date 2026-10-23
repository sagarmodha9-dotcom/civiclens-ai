"use client";
import useSWR from "swr";
import { Shell } from "@/components/Shell";
import { Loading, Panel } from "@/components/ui";
import { fetcher, int, type Meta } from "@/lib/api";

export default function Page() {
  const { data: meta } = useSWR<Meta>("/v1/meta", fetcher);
  const { data: sql } = useSWR<{ queries: Record<string, string>; row_cap: number }>("/v1/sql", fetcher);
  return (
    <Shell scoped={false}>
      <h1 className="text-2xl font-semibold tracking-tight mb-1">Methodology</h1>
      <p className="text-mist-400 mb-6 max-w-3xl">What the numbers are, where they come from, how they were checked, and what they cannot tell you.</p>
      <div className="grid lg:grid-cols-2 gap-4">
        <Panel title="Data source and scope">
          <ul className="text-sm space-y-1.5 text-mist-300">
            <li><b>Source:</b> USAspending.gov API v2, <code className="text-xs">POST /api/v2/download/transactions/</code>, prime contract transactions (award types A, B, C, D). Sub-award files are stored but never counted.</li>
            <li><b>IT procurement:</b> Product or Service Code starting with <code className="text-xs">D</code> (IT and telecom services) or <code className="text-xs">70</code> (IT equipment and software); the federal IT category definition. NAICS is kept as an attribute.</li>
            <li><b>Agencies:</b> awarding toptier VA (036), DHS (070), HHS (075), Treasury (020), Commerce (013), SSA (028).</li>
            <li><b>Fiscal year:</b> Oct 1 – Sep 30, from each transaction’s <code className="text-xs">action_date</code>, cross-checked against the file’s own <code className="text-xs">action_date_fiscal_year</code>. FY2026 ended Sep 30, 2026 and is shown as preliminary: reporting lag and revisions continue for months.</li>
            <li><b>Obligations, not ceilings:</b> figures are <code className="text-xs">federal_action_obligation</code> summed per fiscal year; de-obligations stay negative. Contract ceilings (<code className="text-xs">base_and_all_options_value</code>) are never summed.</li>
            <li><b>Grain:</b> transactions are deduplicated on <code className="text-xs">contract_transaction_unique_key</code> (newest ingest wins); awards are identified by <code className="text-xs">contract_award_unique_key</code>, which includes the agency and parent vehicle, because a PIID alone is not unique.</li>
          </ul>
        </Panel>
        <Panel title="Pipeline and checks">
          <ul className="text-sm space-y-1.5 text-mist-300">
            <li><b>Ingestion</b> on GitHub Actions: one download job per agency × fiscal year, each with a manifest (request body, extraction time, API <code className="text-xs">last_updated</code>, API row count, file hashes). Idempotent: unchanged cells are skipped.</li>
            <li><b>Bronze → Silver → Gold</b> on Databricks (Delta, Unity Catalog) and, with the same SQL files, in the published DuckDB snapshot. Gold tables are sums over Silver rows, so they reconcile to the cent by construction.</li>
            <li><b>Data-quality gate</b> before any publish: unique keys; Bronze = Silver + rejects + duplicates; Gold = Silver; fiscal year consistent; flag rate within design.</li>
            <li><b>Reconciliation at matching grain:</b> per-cell counts vs the API’s count for the identical filter; sampled awards’ window sums vs each award’s own transactions in the same window. Lifetime award totals are displayed, never compared with window sums.</li>
            <li><b>Snapshot:</b> immutable versioned file published as a release asset; the API is pinned to a version shown in the header; a failed pipeline never replaces the last good snapshot.</li>
          </ul>
          {meta && (
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
              <div className="chip">snapshot {meta.snapshot_version}</div><div className={`chip ${meta.dq._all_pass ? "chip-ok" : "chip-warn"}`}>DQ {meta.dq._all_pass ? "all pass" : "failing"}</div>
              {Object.entries(meta.tables).map(([t, n]) => <div key={t} className="flex justify-between border-b border-ink-800 py-0.5"><span className="text-mist-400">{t}</span><span className="num">{int(n)}</span></div>)}
            </div>
          )}
        </Panel>
        <Panel title="Anomaly detectors">
          <ul className="text-sm space-y-2 text-mist-300">
            <li><b>Unusually large award</b> — peer group: same awarding agency, same 2-character PSC class, same fiscal year. Statistic: robust z on log₁₀(obligations) = (x − median) / (1.4826 × MAD). Flag at z ≥ 3.5. Abstains below 30 peers or when MAD = 0. On log-normal peers the design flag rate is ≤ 2%; on a pure Pareto tail it can reach ~6%, which is the documented limit of a symmetric rule.</li>
            <li><b>Vendor concentration</b> — HHI of recipient shares within agency × PSC class × fiscal year (10,000 = one recipient). Flag when HHI ≥ 2,500 and top share ≥ 50%, or HHI rose ≥ 1,000 year over year; cells under $5M are not scored.</li>
            <li><b>Abrupt recipient growth</b> — same recipient, same agency, prior fiscal year. Flag when ratio ≥ 3 and increase ≥ $2M; prior year must be ≥ $500k.</li>
          </ul>
          <p className="text-xs text-mist-400 mt-3">A flag is a starting point for a question, not a conclusion. New vehicles, option exercises, consolidated buys and classification changes all produce legitimate outliers. The tables report rows, scored rows and flagged rows separately.</p>
          {meta?.anomaly_summary && (
            <table className="tbl mt-3 text-xs"><thead><tr><th>Detector</th><th className="num">Rows</th><th className="num">Scored</th><th className="num">Flagged</th><th>Not scored (reason: count)</th></tr></thead>
              <tbody>{Object.entries(meta.anomaly_summary).map(([k, v]) => <tr key={k}><td>{k}</td><td className="num">{int(v.rows)}</td><td className="num">{int(v.scored)}</td><td className="num">{int(v.flagged)}</td><td className="text-mist-400">{Object.entries(v.not_scored).map(([r, n]) => `${r.replace("not scored: ", "")}: ${int(n)}`).join("; ") || "–"}</td></tr>)}</tbody></table>
          )}
        </Panel>
        <Panel title="AI investigator: guarantees and limits">
          <ul className="text-sm space-y-1.5 text-mist-300">
            <li>Six read-only tools over the dashboard’s own queries; no free-text SQL; scope cannot be widened by the model.</li>
            <li>Structured output; every numeric fact is re-verified server-side against the tool call that produced it (value within 0.5%, matching entities and fiscal years); citations must exist in the snapshot. One regeneration on failure; remaining facts are shown as unverified.</li>
            <li>Misconduct vocabulary is blocked in output; the evaluation set includes injection, no-evidence and misconduct-baiting cases, and its results, including failures, are published in the repository.</li>
            <li>Limits: the model can still mis-state a trend in prose that a numeric check cannot catch (a judge pass measures this in evaluation); it cannot see anything outside the snapshot; it is rate-limited and budget-capped, and may be switched to cached answers.</li>
          </ul>
        </Panel>
      </div>
      <Panel title="The SQL behind each endpoint" className="mt-4">
        {!sql ? <Loading rows={6} /> : (
          <div className="space-y-3">{Object.entries(sql.queries).map(([k, s]) => (
            <details key={k} className="group"><summary className="cursor-pointer text-sm text-mist-200 font-mono">{k}</summary><pre className="mt-2 overflow-x-auto rounded-md bg-ink-950 p-3 text-xs text-mist-300 whitespace-pre-wrap">{s.trim()}</pre></details>))}
            <p className="text-xs text-mist-500">Parameters are bound, never interpolated; results are capped at {int(sql.row_cap)} rows.</p></div>
        )}
      </Panel>
    </Shell>
  );
}
