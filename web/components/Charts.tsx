"use client";
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { usd } from "@/lib/api";

const axis = { stroke: "#34435c", tick: { fill: "#8f9bb0", fontSize: 12 } } as const;
const tip = { contentStyle: { background: "#131924", border: "1px solid #243044", borderRadius: 8, fontSize: 12 }, labelStyle: { color: "#b8c2d1" }, itemStyle: { color: "#e6eaf0" } } as const;

export function FyBars({ data, prelimFy = 2026 }: { data: { fiscal_year: number; obligations: number }[]; prelimFy?: number }) {
  return (
    <div className="h-64" role="img" aria-label="Obligations by fiscal year">
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
          <CartesianGrid vertical={false} stroke="#1c2535" />
          <XAxis dataKey="fiscal_year" tickFormatter={(v) => `FY${String(v).slice(2)}`} {...axis} />
          <YAxis tickFormatter={(v) => usd(v)} width={64} {...axis} />
          <Tooltip {...tip} formatter={(v) => [usd(Number(v), false), "Obligations"]} labelFormatter={(l) => `FY${l}${Number(l) === prelimFy ? " (preliminary)" : ""}`} />
          <Bar dataKey="obligations" radius={[6, 6, 0, 0]}>
            {data.map((d) => <Cell key={d.fiscal_year} fill={d.fiscal_year === prelimFy ? "#f2b544" : "#5aa9ff"} fillOpacity={d.fiscal_year === prelimFy ? 0.7 : 0.9} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function HBars({ data, nameKey, valueKey, onClick, height = 280 }: { data: Record<string, unknown>[]; nameKey: string; valueKey: string; onClick?: (row: Record<string, unknown>) => void; height?: number }) {
  return (
    <div style={{ height }} role="img" aria-label={`${valueKey} by ${nameKey}`}>
      <ResponsiveContainer>
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 16, left: 8, bottom: 0 }}>
          <CartesianGrid horizontal={false} stroke="#1c2535" />
          <XAxis type="number" tickFormatter={(v) => usd(v)} {...axis} />
          <YAxis type="category" dataKey={nameKey} width={170} tickFormatter={(v) => String(v).length > 24 ? `${String(v).slice(0, 23)}…` : String(v)} {...axis} />
          <Tooltip {...tip} formatter={(v) => [usd(Number(v), false), "Obligations"]} />
          <Bar dataKey={valueKey} fill="#5aa9ff" radius={[0, 6, 6, 0]} onClick={(d) => onClick?.(d as unknown as Record<string, unknown>)} cursor={onClick ? "pointer" : undefined} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function Lines({ data, series, xKey = "fiscal_year" }: { data: Record<string, unknown>[]; series: { key: string; color: string; name: string }[]; xKey?: string }) {
  return (
    <div className="h-64" role="img" aria-label="Trend lines">
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
          <CartesianGrid vertical={false} stroke="#1c2535" />
          <XAxis dataKey={xKey} tickFormatter={(v) => `FY${String(v).slice(2)}`} {...axis} />
          <YAxis tickFormatter={(v) => usd(v)} width={64} {...axis} />
          <Tooltip {...tip} formatter={(v, n) => [usd(Number(v), false), String(n)]} />
          {series.map((s) => <Line key={s.key} type="monotone" dataKey={s.key} name={s.name} stroke={s.color} strokeWidth={2} dot={{ r: 3 }} />)}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
