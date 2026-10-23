"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef } from "react";
import type { Scope } from "./api";

export function useScope(): [Scope, (next: Partial<Scope>) => void] {
  const sp = useSearchParams(); const router = useRouter(); const path = usePathname();
  const scope = useMemo<Scope>(() => ({
    agency: sp.get("agency") || undefined, fy: sp.get("fy") ? Number(sp.get("fy")) : undefined,
    psc: sp.get("psc") || undefined, recipient: sp.get("recipient") || undefined,
  }), [sp]);
  // Two quick changes (agency, then fiscal year) must both survive: the router updates `sp` asynchronously, so a second
  // `set` built from the stale `sp` would drop the first change (live e2e run 40015888921). Merge onto the params we last
  // asked for until the router catches up.
  const pending = useRef<URLSearchParams | null>(null);
  useEffect(() => { pending.current = null; }, [sp]);
  const set = useCallback((next: Partial<Scope>) => {
    const p = new URLSearchParams((pending.current ?? sp).toString());
    for (const [k, v] of Object.entries(next)) { if (v === undefined || v === "" || v === null) p.delete(k); else p.set(k, String(v)); }
    pending.current = p;
    router.replace(`${path}?${p.toString()}`, { scroll: false });
  }, [sp, router, path]);
  return [scope, set];
}
