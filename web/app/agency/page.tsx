"use client";
import { Suspense } from "react";
import useSWR from "swr";
import { Shell } from "@/components/Shell";
import { HBars, Lines } from "@/components/Charts";
import { Empty, ErrorState, Kpi, Loading, Panel } from "@/components/ui";
import { AGENCIES, fetcher, int, pct, qs, usd, type Agency } from "@/lib/api";
import { useScope } from "@/lib/scope";

function AgencyPage() {
  const [scope, set] = useScope();
  const { data, error, isLoading, mutate } = useSWR<Agency>(`/v1/agency${qs(scope)}`, fetcher);
  // pivot agency_fy -> per FY: services vs equipment
  const byFy = new Map<number, { fiscal_year: number; services: number; equipment: number; awards: number; recipients: number }>();
  for (const r of data?.agency_fy ?? []) {
    const row = byFy.get(r.fiscal_year) ?? { fiscal_year: r.fiscal_year, services: 0, equipment: 0, awards: 0, recipients: 0 };
    if (r.it_category === "IT services") row.services += Number(r.obligations); else row.equipment += Number(r.obligations);
    row.awards += Number(r.awards); row.recipients += Number(r.recipients); byFy.set(r.fiscal_year, row);
  }
  const trend = [...byFy.values()].sort((a, b) => a.fiscal_year - b.fiscal_year);
  const total = trend.reduce((a, r) => a + r.services + r.equipment, 0);
  const title = scope.agency ? AGENCIES[scope.agency] : "All six agencies";
  return (
    <>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div><h1 className="text-2xl font-semibold tracking-tight">{title}</h1><p className="text-mist-400 mt-1">IT services (PSC D) and IT equipment & software (PSC 70), prime contract obligations by fiscal year.</p></div>
        {!scope.agency && <span className="chip">Pick an agency in the scope bar for recipient drill-downs</span>}
      </div>
      {error && <ErrorState error={error} retry={() => mutate()} />}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <Kpi label="Obligations" value={isLoading ? "…" : usd(total)} sub={scope.fy ? `FY${scope.fy}` : "all years in scope"} />
        <Kpi label="Services share" value={isLoading ? "…" : pct(total ? trend.reduce((a, r) => a + r.services, 0) / total : null)} sub="PSC D of total" />
        <Kpi label="Award-years" value={isLoading ? "…" : int(trend.reduce((a, r) => a + r.awards, 0))} />
        <Kpi label="Recipient-years" value={isLoading ? "…" : int(trend.reduce((a, r) => a + r.recipients, 0))} sub="distinct recipient × FY" />
      </div>
      <div className="grid lg:grid-cols-2 gap-4">
        <Panel title="Services vs equipment by fiscal year">
          {isLoading ? <Loading rows={6} /> : trend.length ? <Lines data={trend} series={[{ key: "services", color: "#5aa9ff", name: "IT services (D)" }, { key: "equipment", color: "#f2b544", name: "IT equipment & software (70)" }]} /> : <Empty>No rows in this scope.</Empty>}
        </Panel>
        <Panel title="Top recipients">
          {isLoading ? <Loading rows={6} /> : data?.top_recipients.length ? <HBars data={data.top_recipients.slice(0, 12).map((r) => ({ ...r, obligations: Number(r.obligations) }))} nameKey="recipient_name" valueKey="obligations" height={300} onClick={(row) => set({ recipient: String(row.recipient_uei) })} /> : <Empty>No recipients.</Empty>}
        </Panel>
        <Panel title="Largest year-over-year increases by recipient" action={<span className="text-xs text-mist-500">same recipient, same agency, prior FY</span>}>
          {isLoading ? <Loading rows={6} /> : data?.yoy_recipients.length ? (
            <table className="tbl"><thead><tr><th>Recipient</th><th className="num">Prior FY</th><th className="num">This FY</th><th className="num">Change</th></tr></thead>
              <tbody>{data.yoy_recipients.map((r) => { const d = Number(r.obligations) - Number(r.prior_obligations); return (
                <tr key={r.recipient_uei}><td><button className="link text-left" onClick={() => set({ recipient: r.recipient_uei })}>{r.recipient_name}</button></td>
                  <td className="num">{usd(r.prior_obligations)}</td><td className="num">{usd(r.obligations)}</td><td className={`num ${d >= 0 ? "text-mint" : "text-rose"}`}>{d >= 0 ? "+" : ""}{usd(d)}</td></tr>); })}</tbody></table>
          ) : <Empty>Needs a single fiscal year in scope with a prior year.</Empty>}
        </Panel>
        <Panel title="PSC classes">
          {isLoading ? <Loading rows={6} /> : data?.psc_mix.length ? (
            <table className="tbl"><thead><tr><th>PSC</th><th>Example description</th><th className="num">Obligations</th><th className="num">Awards</th></tr></thead>
              <tbody>{data.psc_mix.map((r) => (<tr key={r.psc_class2}><td className="font-mono">{r.psc_class2}</td><td className="text-mist-400 text-xs">{r.description}</td><td className="num">{usd(r.obligations)}</td><td className="num">{int(r.awards)}</td></tr>))}</tbody></table>
          ) : <Empty>No rows.</Empty>}
        </Panel>
      </div>
    </>
  );
}
export default function Page() { return <Shell><Suspense fallback={<Loading rows={8} />}><AgencyPage /></Suspense></Shell>; }
