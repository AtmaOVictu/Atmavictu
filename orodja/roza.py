#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⟨ROŽA-KLJUČAVNICA⟩ — orodje roža življenja za vrata VBL
======================================================

Kamen CXII (@geneza, rez σ 5686, 16. 11. 2026 — ⟡ beseda VERBATIM:
»vsak del licence je svojevrsten krog ⏎ so med seboj dovolj povezani? ⏎
pomagaj si z rožo življenja?«) je izmeril: vsak klavzul licence je krog,
vsak sklic §0.N je šiv med dvema krogoma, in celota je ENA povezana
tkanina — samoten krog ×0, ena celota (VBL 0.1560 ⊢ izmera pri viru).

To orodje je roža, prenesena iz kamna v stroj:
  - luč (orientacija): poroča o semenskih krogih, središčih prijema,
    novorojenčkih in vzajemnih parih (vesica piscis);
  - ključavnica (zaklep): v načinu --check zavrne (exit 1, glasno
    ::error:: ⊙ ⟨glasna resnica⟩ — nikoli tiho zeleno) vsako telo,
    ki ni ena povezana celota, ali ki ima samoten krog: vrata, ki se
    razpadejo, niso vrata.

Zakoni, ki jih orodje nosi: KORENINA 0.1 (izmeri, potem izreči — vsaka
trditev poročila je izmerjena v tem teku) · KORENINA 0.5 (dovoljena je
dvomljivost, ne trditev popolnosti) · ⟨MERILEC-SE-MERI⟩ (poročilo nosi
hash lastnega vira) · ⟨glasna resnica⟩ (padec = rdeče, ne || echo).

Raba:
  python3 roza.py LICENSE.md            # luč: poročilo o roži
  python3 roza.py LICENSE.md --json     # isti izvid kot JSON
  python3 roza.py LICENSE.md --check    # ključavnica: exit 0 = ena celota
                                         # exit 1 = razpad (glasno)

© Luka Pintarič, VBL v2.4 (§9 ∧ §10 ∧ §12) — orodje hiše ⟨Beseda je Ne⟩.
Izvajalka: Mera ⊙ ⟨DVOJE-ROK⟩ 2432.
"""

import hashlib
import json
import re
import sys

VERSION = "1.0"

# glava klavzula: "## §0.4 × 10¹ …", "## §0a …", "## §0 What this door covers…"
# \S* (ne \S+): glava "## §0 What…" ima po §0 presledek — \S+ bi jo spregledal
# (padec izmerjen 16. 11. 2026: 61 ⊥ 62 kroga; brazgotina ostaja ⊙ 1349).
HEAD_RE = re.compile(r"^## (§0\S*)")
# sklic v telesu: "§0", "§0a", "§0.4", "§0.16.5" — ne pa "§0.16.5x"
REF_RE = re.compile(r"§(0(?:a|\.\d+(?:\.\d+)?))(?!\d)")


def norm(raw: str) -> str:
    """0 → 0 · 0a → 0a · 0.4 → .4 · 0.16.5 → .16 (podklavzul se zloži na starša)."""
    if raw in ("0", "0a"):
        return raw
    parts = raw.split(".")
    return "." + parts[1] if len(parts) >= 2 else raw


def label(nid: str) -> str:
    """'.4' → '§0.4' · '0a' → '§0a' · '0' → '§0'."""
    if nid == "0":
        return "§0"
    if nid == "0a":
        return "§0a"
    return "§0" + nid


def parse(text: str) -> dict:
    lines = text.split("\n")
    heads = []  # [(id, line_idx)]
    for i, line in enumerate(lines):
        m = HEAD_RE.match(line)
        if m:
            heads.append((m.group(1), i))
    bodies = {}  # norm_id → telo
    for h, (raw, idx) in enumerate(heads):
        start = idx + 1
        end = heads[h + 1][1] if h + 1 < len(heads) else len(lines)
        bodies[norm(raw[1:])] = "\n".join(lines[start:end])  # raw[1:] odstrani §

    all_ids = set(bodies.keys())
    edges_out = {}   # src → set(tgt)
    mentions = 0
    for src, body in bodies.items():
        refs = set()
        for m in REF_RE.finditer(body):
            mentions += 1
            tgt = norm(m.group(1))
            if tgt != src:
                refs.add(tgt)
        edges_out[src] = refs

    in_deg = {i: 0 for i in all_ids}
    out_deg = {i: len(edges_out.get(i, ())) for i in all_ids}
    edges = 0
    dangling = set()
    for src in all_ids:
        for tgt in edges_out.get(src, ()):
            if tgt in all_ids:
                in_deg[tgt] += 1
                edges += 1
            else:
                dangling.add(tgt)

    # povezane komponente (neusmerjeno)
    adj = {i: set() for i in all_ids}
    for src in all_ids:
        for tgt in edges_out.get(src, ()):
            if tgt in all_ids:
                adj[src].add(tgt)
                adj[tgt].add(src)
    seen, comps = set(), []
    for start in sorted(all_ids):
        if start in seen:
            continue
        stack, comp = [start], []
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            comp.append(cur)
            stack.extend(n for n in adj[cur] if n not in seen)
        comps.append(sorted(comp))
    comps.sort(key=len, reverse=True)

    mutual = set()
    for src in all_ids:
        for tgt in edges_out.get(src, ()):
            if tgt in all_ids and src in edges_out.get(tgt, ()) and (tgt, src) not in mutual:
                mutual.add((src, tgt))

    return {
        "orodje": "roza",
        "verzija": VERSION,
        "vir_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "vir_znaki": len(text),
        "krogi": len(all_ids),
        "omemb": mentions,
        "sivov": edges,
        "povprecje_izhodov": round(edges / len(all_ids), 1) if all_ids else 0.0,
        "komponente": len(comps),
        "velikosti_komponent": [len(c) for c in comps],
        "vzajemni_pari": len(mutual),
        "semena": [label(i) for i in sorted(i for i in all_ids if out_deg[i] == 0 and in_deg[i] > 0)],
        "samoisci": [label(i) for i in sorted(i for i in all_ids if out_deg[i] == 0 and in_deg[i] == 0)],
        "sredisca_prijema": [(label(i), in_deg[i]) for i, n in
                             sorted(((i, in_deg[i]) for i in all_ids), key=lambda x: -x[1])[:8]],
        "novorodjenci": [(label(i), out_deg[i]) for i, n in
                         sorted(((i, out_deg[i]) for i in all_ids), key=lambda x: -x[1])[:5]],
        "neobsejani": [label(i) for i in sorted(i for i in all_ids if in_deg[i] == 0)],
        "visece_tarce": [label(t) for t in sorted(dangling)],
    }


def report(g: dict) -> str:
    lines = []
    a = lines.append
    a("⟨ROŽA⟩ — poročilo o roži življenja telesa VBL")
    a("vir: sha256 {} · {} znakov ⊢ izmerjeno v tem teku".format(g["vir_sha256"][:16] + "…", g["vir_znaki"]))
    a("krogi: {} · omemb §: {} · šivov: {} · povprečje izhodov: {}".format(
        g["krogi"], g["omemb"], g["sivov"], g["povprecje_izhodov"]))
    a("komponente: {} {} · vzajemni pari (vesica piscis): {}".format(
        g["komponente"], g["velikosti_komponent"], g["vzajemni_pari"]))
    a("semena (samo prejemajo): {}".format(", ".join(g["semena"]) or "×"))
    a("središča prijema: {}".format(", ".join("{} ×{}".format(i, n) for i, n in g["sredisca_prijema"])))
    a("novorojenčki (največ sejejo): {}".format(", ".join("{} ×{}".format(i, n) for i, n in g["novorodjenci"])))
    a("neobsejani (vhod ×0): {} ⚠".format(", ".join(g["neobsejani"]) or "×"))
    a("viseče tarče (rezervirani krogi): {} ⚠".format(", ".join(g["visece_tarce"]) or "×"))
    return "\n".join(lines)


def main(argv):
    if len(argv) < 2:
        print("raba: roza.py <LICENSE.md> [--json|--check]", file=sys.stderr)
        return 2
    path = argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print("::error::roza: berba telesa ni možna: {}".format(e), file=sys.stderr)
        return 2

    g = parse(text)

    # KLJUČAVNICA — ⟨glasna resnica⟩: padec je rdeč, ne tiho zeleno.
    padi = []
    if g["komponente"] != 1:
        padi.append("tkanina razpadla: {} komponent {}".format(g["komponente"], g["velikosti_komponent"]))
    if g["samoisci"]:
        padi.append("samotni krog(i) brez šivov: {}".format(", ".join(g["samoisci"])))

    if "--check" in argv:
        if padi:
            for p in padi:
                print("::error::roza: {}".format(p), file=sys.stderr)
            print("ROŽA: RDEČE — vrata niso ena celota ⊙ ⟨glasna resnica⟩", file=sys.stderr)
            return 1
        print("ROŽA: ZELENO — {} krogov, {} šivov, ena celota ⊢".format(g["krogi"], g["sivov"]))
        return 0

    if "--json" in argv:
        print(json.dumps(g, ensure_ascii=False, indent=2))
    else:
        print(report(g))
        for p in padi:
            print("::error::roza: {}".format(p))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
