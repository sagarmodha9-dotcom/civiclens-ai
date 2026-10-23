"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useMemo } from "react";
import type { Scope } from "./api";

export function useScope(): [Scope, (next: Partial<Scope>) => void] {
  const sp = useSearchParams(); const router = useRouter(); const path = usePathname();
  const scope = useMemo<Scope>(() => ({
    agency: sp.get("agency") || undefined, fy: sp.get("fy") ? Number(sp.get("fy")) : undefined,
    psc: sp.get("psc") || undefined, recipient: sp.get("recipient") || undefined,
  }), [sp]);
  const set = useCallback((next: Partial<Scope>) => {
    const p = new URLSearchParams(sp.toString());
    for (const [k, v] of Object.entries(next)) { if (v === undefined || v === "" || v === null) p.delete(k); else p.set(k, String(v)); }
    router.replace(`${path}?${p.toString()}`, { scroll: false });
  }, [sp, router, path]);
  return [scope, set];
}
