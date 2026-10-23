export const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Scope = { agency?: string; fy?: number; psc?: string; recipient?: string };

export function qs(scope: Scope, extra: Record<string, string | number | undefined> = {}): string {
  const p = new URLSearchParams();
  if (scope.agency) p.set("agency", scope.agency);
  if (scope.fy) p.set("fy", String(scope.fy));
  if (scope.psc) p.set("psc", scope.psc);
  if (scope.recipient) p.set("recipient", scope.recipient);
  for (const [k, v] of Object.entries(extra)) if (v !== undefined && v !== "") p.set(k, String(v));
  const s = p.toString();
  return s ? `?${s}` : "";
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) { super(message); this.status = status; }
}

export async function getJSON<T>(path: string): Promise<T> {
  const r = await fetch(`${API}${path}`, { headers: { Accept: "application/json" }, cache: "no-store" });
  if (!r.ok) {
    let detail = r.statusText;
    try { detail = (await r.json()).detail ?? detail; } catch { /* ignore */ }
    throw new ApiError(r.status, typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return r.json();
}

export async function postJSON<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(`${API}${path}`, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) {
    let detail = r.statusText;
    try { detail = (await r.json()).detail ?? detail; } catch { /* ignore */ }
    throw new ApiError(r.status, typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return r.json();
}

export const fetcher = <T,>(path: string) => getJSON<T>(path);

export const AGENCIES: Record<string, string> = {
  "036": "Veterans Affairs", "070": "Homeland Security", "075": "Health & Human Services",
  "020": "Treasury", "013": "Commerce", "028": "Social Security Administration",
};
export const FYS = [2022, 2023, 2024, 2025, 2026];
export const PRELIMINARY_FY = 2026;

export const usd = (n: number | string | null | undefined, compact = true) => {
  const v = Number(n ?? 0);
  if (!isFinite(v)) return "–";
  if (compact) {
    const a = Math.abs(v);
    if (a >= 1e9) return `${v < 0 ? "-" : ""}$${(a / 1e9).toFixed(2)}B`;
    if (a >= 1e6) return `${v < 0 ? "-" : ""}$${(a / 1e6).toFixed(1)}M`;
    if (a >= 1e3) return `${v < 0 ? "-" : ""}$${(a / 1e3).toFixed(0)}K`;
  }
  return v.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: compact ? 0 : 2 });
};
export const int = (n: number | string | null | undefined) => Number(n ?? 0).toLocaleString("en-US");
export const pct = (n: number | null | undefined, d = 1) => (n == null || !isFinite(n) ? "–" : `${(n * 100).toFixed(d)}%`);

// response types (subset)
export type Meta = { snapshot_version: string; built_utc: string; api_last_updated?: string[]; settled_fiscal_years: number[]; preliminary_fiscal_years: number[];
  tables: Record<string, number>; dq: Record<string, { pass?: boolean } & Record<string, unknown>> & { _all_pass: boolean }; anomaly_summary?: Record<string, { rows: number; flagged: number; scored: number; normal: number; not_scored: Record<string, number> }>; schema_version?: number };
export type Overview = { scope: Scope; by_fiscal_year: { fiscal_year: number; obligations: number; transactions: number; awards: number }[];
  by_agency: { awarding_agency_code: string; awarding_agency_name: string; obligations: number; awards: number }[];
  top_recipients: { recipient_uei: string; recipient_name: string; obligations: number; awards: number }[];
  psc_mix: { psc_class2: string; description: string; obligations: number; awards: number }[];
  anomaly_counts: Record<string, number> };
export type Agency = { agency_fy: { awarding_agency_code: string; awarding_agency_name: string; fiscal_year: number; it_category: string; obligations: number; transactions: number; awards: number; recipients: number }[];
  top_recipients: Overview["top_recipients"]; psc_mix: Overview["psc_mix"]; yoy_recipients: { recipient_uei: string; recipient_name: string; obligations: number; prior_obligations: number }[] };
export type Anomaly = { detector: string; award_key?: string; piid?: string; fiscal_year: number; awarding_agency_code: string; awarding_agency_name: string; recipient_uei?: string; recipient_name?: string;
  psc?: string; psc_class2?: string; value: number; unit: string; peer_n: number; baseline_median?: number; score: number; threshold: number; status: string; limits: string; usaspending_permalink?: string;
  top_recipient_name?: string; top_share?: number; prior_hhi?: number; hhi_change?: number; baseline?: number; delta?: number; awards?: number };
export type AnomalyDetail = Anomaly & { award_years: { fiscal_year: number; obligations: number; transactions: number; deobligations: number }[];
  transactions: { transaction_key: string; action_date: string; fiscal_year: number; modification_number: string; obligation: number; action_type: string; psc: string; awarding_sub_agency_name: string; usaspending_permalink: string }[];
  peer_group_sample: { award_key: string; piid: string; recipient_name: string; value: number; score: number | null; status: string }[] };
export type Investigation = { status: "ok" | "unavailable" | "limited"; reason?: string; cached?: boolean; mode?: string; model?: string; snapshot_version?: string;
  answer?: { facts: { claim: string; value: number | string; unit: string; tool_call_id: string; measure: string; entities: string[]; fiscal_years: number[] }[]; interpretation: string; citations: string[]; limits: string; insufficient_evidence: boolean };
  verification?: { verified_facts: unknown[]; unverified_facts: { claim: string; why: string }[]; bad_citations: string[]; ok: boolean };
  tool_log?: { id: string; name: string; args: Record<string, unknown> }[]; usage?: { input_tokens: number; output_tokens: number; usd: number; regenerated: boolean } };
