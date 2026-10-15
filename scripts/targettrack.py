#!/usr/bin/env python
"""Fetch and inventory the PSI TargetTrack archive (Zenodo DOI 10.5281/zenodo.821654).

The archive is untrusted third-party data. Keep it OUTSIDE the repo (it is ~833 MB,
and .gitignore excludes *.tar.gz / *.gz anyway), and always run this script with
`python -I` so the extraction directory cannot shadow stdlib imports.

Schema (formatVersion 1.4.1) relevant to expression-host mining
---------------------------------------------------------------
    <formatVersion>, <site>, <contactInfoList>, <protocolList>   (once, up front)
    <protocolList>/<protocol>  protocolId, protocolName, protocolDescription,
                               protocolType (ENUMERATED), protocolText (FREE TEXT)
    <target>  targetId, status (ENUMERATED), targetSequenceList/targetSequence/
              oneLetterCode, .../sourceOrganism/{scientificName,taxId},
              trialList/trial/{status, statusHistoryList/statusHistory/status,
              trialSequenceList/trialSequence/oneLetterCode,
              trialProtocolList/protocolRef/{protocolId, protocolType}}

There is NO expression-host element at any level. Host can only be recovered by
text-mining <protocolText> of protocols whose protocolType is "expression", then
propagating via trialProtocolList/protocolRef. This script quantifies exactly that.

Subcommands
-----------
  fetch      Resumable download + md5 verification of TargetTrack-1Jul2017.tar.gz.
  extract    Untar into a NEW EMPTY directory (refuses traversal/link members).
  schema     Dump every element path, attribute and value histogram in tt.xml.gz.
  protocols  Dump the protocol table (+ mined host label) as TSV, for eyeballing.
  inventory  Stream tt.xml.gz and emit host / outcome / sequence coverage counts.
  pairs      Verify the multi-host targets trial by trial and emit only the
             genuine paired observations (the artefact rate is ~43%).

Examples
--------
  python -I scripts/targettrack.py fetch   --dest D:/tt-work/download
  python -I scripts/targettrack.py extract --tarball D:/tt-work/download/TargetTrack-1Jul2017.tar.gz --dest D:/tt-work/extract
  python -I scripts/targettrack.py schema    --xml "<...>/tt.xml.gz" --limit 5000 > schema.txt
  python -I scripts/targettrack.py protocols --xml "<...>/tt.xml.gz" > protocols.tsv
  python -I scripts/targettrack.py inventory --xml "<...>/tt.xml.gz" --out-dir D:/tt-work/out
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import re
import sys
import tarfile
import urllib.request
from collections import Counter, defaultdict

ZENODO_RECORD = "821654"
ARCHIVE = "TargetTrack-1Jul2017.tar.gz"
ARCHIVE_URL = f"https://zenodo.org/api/records/{ZENODO_RECORD}/files/{ARCHIVE}/content"
ARCHIVE_SIZE = 832_912_731
ARCHIVE_MD5 = "200012a8a2a11ffd7e370ed142df36c3"
CHUNK = 1 << 20


# =============================================================== fetch / extract
def cmd_fetch(args: argparse.Namespace) -> int:
    os.makedirs(args.dest, exist_ok=True)
    path = os.path.join(args.dest, ARCHIVE)
    have = os.path.getsize(path) if os.path.exists(path) else 0

    while have < ARCHIVE_SIZE:
        req = urllib.request.Request(ARCHIVE_URL)
        if have:
            req.add_header("Range", f"bytes={have}-")
            print(f"resuming at {have:,} / {ARCHIVE_SIZE:,}", file=sys.stderr)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp, open(
                path, "ab" if have else "wb"
            ) as fh:
                while True:
                    buf = resp.read(CHUNK)
                    if not buf:
                        break
                    fh.write(buf)
                    have += len(buf)
        except Exception as exc:  # noqa: BLE001 - slow links truncate often
            print(f"interrupted ({exc}); resuming", file=sys.stderr)
        have = os.path.getsize(path)

    size = os.path.getsize(path)
    print(f"size {size:,} (expected {ARCHIVE_SIZE:,})")
    if size != ARCHIVE_SIZE:
        print("SIZE MISMATCH - re-run fetch to resume", file=sys.stderr)
        return 1
    h = hashlib.md5()  # noqa: S324 - integrity check against the published digest
    with open(path, "rb") as fh:
        for buf in iter(lambda: fh.read(CHUNK), b""):
            h.update(buf)
    ok = h.hexdigest() == ARCHIVE_MD5
    print(f"md5 {h.hexdigest()} ({'OK' if ok else 'MISMATCH, want ' + ARCHIVE_MD5})")
    return 0 if ok else 1


def _safe_members(tf, dest):
    dest = os.path.realpath(dest)
    for m in tf:
        target = os.path.realpath(os.path.join(dest, m.name))
        if target != dest and not target.startswith(dest + os.sep):
            raise RuntimeError(f"refusing path-traversal member: {m.name!r}")
        if m.issym() or m.islnk():
            raise RuntimeError(f"refusing link member: {m.name!r}")
        yield m


def cmd_extract(args: argparse.Namespace) -> int:
    os.makedirs(args.dest, exist_ok=True)
    if os.listdir(args.dest):
        print(f"{args.dest} is not empty - extract into a new empty dir", file=sys.stderr)
        return 1
    with tarfile.open(args.tarball, "r:gz") as tf:
        tf.extractall(args.dest, members=_safe_members(tf, args.dest))  # noqa: S202
    print(f"extracted to {args.dest}")
    return 0


# ======================================================================= parsing
def _open_xml(path: str):
    return gzip.open(path, "rb") if path.endswith(".gz") else open(path, "rb")


def _records(path: str, limit: int = 0):
    """Yield top-level record elements from tt.xml(.gz), freeing memory as we go."""
    from lxml import etree

    n = 0
    with _open_xml(path) as fh:
        ctx = etree.iterparse(fh, events=("end",), recover=True, huge_tree=True)
        for _, el in ctx:
            parent = el.getparent()
            if parent is None or parent.getparent() is not None:
                continue
            n += 1
            yield el
            el.clear()
            while el.getprevious() is not None:
                del parent[0]
            if limit and n >= limit:
                break


def _tag(el) -> str:
    return el.tag.rsplit("}", 1)[-1] if isinstance(el.tag, str) else "#non-element"


def _texts(el, path):
    return [(h.text or "").strip() for h in el.iterfind(path) if (h.text or "").strip()]


# ================================================= host mining from free protocol text
# Ordered rules. First match wins per category; a protocol may match several
# categories (e.g. a protocol that tried E. coli then switched to insect cells).
HOST_RULES: tuple[tuple[str, str], ...] = (
    # NB: bare "cell-free" is a false-positive magnet -- in these protocols it
    # almost always means "cell-free media" (the spun-off supernatant). Require an
    # expression-system context. Likewise "yeast" is usually "yeast extract" (media).
    (
        "cell-free",
        r"cell[\s-]?free\s+(?:protein\s+)?"
        r"(?:express\w*|synthes\w*|translat\w*|system|reaction|platform|pipeline|production)"
        r"|in\s?vitro\s+(?:transcription[/\s-]*translation|translation|protein\s+synthesis)"
        r"|wheat[\s-]?germ\s+(?:extract|lysate|system)|rapid\s+translation\s+system"
        r"|\bRTS[\s-]?500|PURE\s+system|S30\s+extract|reticulocyte\s+lysate",
    ),
    (
        "insect",
        r"\bSf-?9\b|\bSf-?21\b|\bHi-?5\b|High[\s-]Five|baculovir|Spodoptera"
        r"|Trichoplusia|\bS2\s+cells|Bac-to-Bac|Drosophila\s+S2",
    ),
    (
        "mammalian",
        r"HEK[\s-]?293|\b293[TFES]\b|\bCHO\b|COS-?[17]|\bHeLa\b|mammalian\s+(?:cell|express)"
        r"|FreeStyle|Expi293|\bNS0\b|BHK",
    ),
    (
        "yeast",
        r"Pichia|P\.\s?pastoris|\bpastoris\b|Saccharomyces|S\.\s?cerevisiae|\bcerevisiae\b"
        r"|Kluyveromyces|Schizosaccharomyces|S\.\s?pombe"
        r"|yeast\s+(?:cells?|strain|host|express\w*|culture|transformant)",
    ),
    (
        "e-coli",
        r"E\.\s?coli|Escherichia\s+coli|\bBL21\b|Rosetta|Origami|\bDE3\b|HMS\s?174"
        r"|B834|\bC41\b|\bC43\b|Tuner|NovaBlue|Arctic\s?Express|\bKRX\b"
        r"|Lemo21|SHuffle|T7\s+Express|\bK-?12\b|\bMG1655\b",
    ),
    (
        "other-bacteria",
        r"Bacillus\s+(?:subtilis|megaterium)|Lactococcus|Pseudomonas\s+(?:putida|fluorescens)"
        r"|Mycobacterium\s+smegmatis|Caulobacter|Rhodococcus|Streptomyces\s+lividans"
        r"|Corynebacterium\s+glutamicum",
    ),
    ("plant-or-other-eukaryote", r"Nicotiana|tobacco\s+leaf|Xenopus\s+oocyte|Leishmania\s+tarentolae|Dictyostelium"),
)
HOST_RX = tuple((name, re.compile(rx, re.I)) for name, rx in HOST_RULES)

# A few centers write loose key:value text into the per-trial <protocolDetails>
# deviation field, e.g.
#   "host: Escherichia coli  strain: BL21 DE3 gold magic  vector: pMCSG7
#    induction chemical: IPTG  expression temperature: 37  media: TB"
# This is free text, not an enumerated field, but it is the only per-trial
# host/strain/vector signal in TargetTrack.
KV_RX = re.compile(
    r"\b(host|strain|cloning vector|vector|media|expression temperature|"
    r"induction chemical)\s*:\s*([^:]{1,60}?)(?=\s+[A-Za-z ]{3,22}:|\Z)",
    re.I,
)

VECTOR_RX = re.compile(
    r"\b(p(?:ET|MCSG|SGX|GEX|BAD|TRC|QE|MAL|CR|ACYC|CDF|RSF|LIC|NIC|SpeedET|VP16|"
    r"Fastbac|FastBac|TriEx|Baculo|Opti|Destination|DEST|cDNA3|Tet|Pic|YES)[A-Za-z0-9._()-]*)",
)
STRAIN_RX = re.compile(
    r"\b(BL21(?:\s?\(DE3\))?(?:[\s-]?(?:pLysS|pLysE|Star|AI|Gold|CodonPlus))?"
    r"|Rosetta\s?2?(?:\s?\(DE3\))?(?:\s?pLysS)?|Origami\s?B?|B834(?:\(DE3\))?"
    r"|HMS\s?174(?:\(DE3\))?|C4[13](?:\(DE3\))?|Arctic\s?Express|Tuner(?:\(DE3\))?"
    r"|T7\s?Express|SHuffle|Lemo21|KRX|Sf-?9|Sf-?21|Hi-?5|HEK[\s-]?293[TFES]?|CHO)\b",
    re.I,
)


def classify_hosts(*texts: str) -> set[str]:
    blob = " ".join(t for t in texts if t)
    return {name for name, rx in HOST_RX if rx.search(blob)}


# ===================================================================== protocols
def _load_protocols(path: str):
    """Return {protocol@id: dict} for every <protocol> in <protocolList>.

    The join key is the @id attribute, which is "<CENTER>-<protocolId>".
    <protocolId> alone is center-local and collides across centers, so a
    <protocolRef> must be resolved with the owning target's center prefix.
    """
    protos: dict[str, dict] = {}
    for el in _records(path):
        if _tag(el) != "protocolList":
            continue
        for p in el.iterfind("protocol"):
            atid = (p.get("id") or "").strip()
            if not atid:
                continue
            name = (p.findtext("protocolName") or "").strip()
            desc = (p.findtext("protocolDescription") or "").strip()
            text = (p.findtext("protocolText") or "").strip()
            protos[atid] = {
                "protocol_id": (p.findtext("protocolId") or "").strip(),
                "type": (p.findtext("protocolType") or "").strip(),
                "name": name,
                "desc": desc,
                "text_len": len(text),
                "hosts": sorted(classify_hosts(name, desc, text)),
                "vectors": sorted({m.group(1) for m in VECTOR_RX.finditer(text)})[:20],
                "strains": sorted({m.group(1) for m in STRAIN_RX.finditer(text)})[:20],
            }
        break  # <protocolList> appears exactly once, ahead of the targets
    return protos


class ProtocolIndex:
    """Center-aware, truncation-tolerant resolution of <protocolRef> -> <protocol>."""

    def __init__(self, protos: dict[str, dict]):
        self.protos = protos
        self.by_center: dict[str, list[str]] = defaultdict(list)
        for atid in protos:
            self.by_center[atid.split("-", 1)[0]].append(atid)
        self._cache: dict[tuple[str, str], dict | None] = {}
        self.stats: Counter[str] = Counter()

    def resolve(self, center: str, pid: str):
        if not pid:
            self.stats["ref_blank_protocol_id"] += 1
            return None
        key = (center, pid)
        if key in self._cache:
            hit = self._cache[key]
            self.stats["ref_resolved" if hit else "ref_dangling"] += 1
            return hit
        atid = f"{center}-{pid}"
        hit = self.protos.get(atid)
        if hit is None:
            # Long protocol names are stored truncated in some centers' refs;
            # accept a UNIQUE prefix match within the same center.
            cands = [k for k in self.by_center.get(center, ()) if k.startswith(atid)]
            if len(cands) == 1:
                hit = self.protos[cands[0]]
                self.stats["ref_resolved_by_prefix"] += 1
        self._cache[key] = hit
        self.stats["ref_resolved" if hit else "ref_dangling"] += 1
        return hit


def cmd_protocols(args: argparse.Namespace) -> int:
    protos = _load_protocols(args.xml)
    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(["at_id", "protocol_id", "type", "text_chars", "hosts", "strains",
                "vectors", "name"])
    for atid, p in protos.items():
        w.writerow([
            atid, p["protocol_id"], p["type"], p["text_len"], "|".join(p["hosts"]),
            "|".join(p["strains"]), "|".join(p["vectors"]), p["name"][:80],
        ])
    print(f"# {len(protos)} protocols", file=sys.stderr)
    return 0


# ===================================================================== inventory
AA_RX = re.compile(r"^[ACDEFGHIKLMNPQRSTVWYXBZUO]+$", re.I)
# "selected" means the target was merely declared; "work stopped" and
# "test target" carry no experimental result. Everything else in the <status>
# enumeration is a real experimental outcome.
NON_OUTCOME = {"selected", "work stopped", "test target"}


def cmd_inventory(args: argparse.Namespace) -> int:
    os.makedirs(args.out_dir, exist_ok=True)
    protos = _load_protocols(args.xml)
    index = ProtocolIndex(protos)
    print(f"loaded {len(protos)} protocols", file=sys.stderr)

    proto_type = Counter(p["type"] for p in protos.values())
    expr_protos = {k: v for k, v in protos.items() if v["type"] == "expression"}
    expr_with_host = {k: v for k, v in expr_protos.items() if v["hosts"]}
    any_with_host = {k: v for k, v in protos.items() if v["hosts"]}

    s = Counter()
    center_counts: Counter[str] = Counter()
    host_per_target: Counter[str] = Counter()
    host_per_trial: Counter[str] = Counter()
    hosts_per_target_hist: Counter[int] = Counter()
    status_target: Counter[str] = Counter()
    status_trial: Counter[str] = Counter()
    reftype: Counter[str] = Counter()
    proto_ref_use: Counter[str] = Counter()
    expr_nohost_use: Counter[str] = Counter()
    strain_per_target: Counter[str] = Counter()
    vector_per_target: Counter[str] = Counter()
    kv_keys: Counter[str] = Counter()
    kv_host_values: Counter[str] = Counter()
    kv_strain_values: Counter[str] = Counter()
    kv_vector_values: Counter[str] = Counter()
    host_src: Counter[str] = Counter()
    host_per_target_by_src: dict[str, Counter] = defaultdict(Counter)
    seq_hosts: dict[bytes, set[str]] = defaultdict(set)
    multihost_rows: list[list[str]] = []
    lab_host_cov: dict[str, Counter] = defaultdict(Counter)

    for el in _records(args.xml, args.limit):
        tag = _tag(el)
        s[f"toplevel:{tag}"] += 1
        if tag != "target":
            continue
        s["targets"] += 1
        tid = (el.findtext("targetId") or "").strip()
        lab = (el.findtext("laboratoryList/lab") or "").strip() or "?"
        atid = (el.get("id") or "").strip()
        # target @id is "<CENTER>-<targetId>"; the center prefix is the protocol
        # namespace, and is NOT the same thing as <laboratoryList><lab>.
        center = atid[: -(len(tid) + 1)] if tid and atid.endswith("-" + tid) else "?"
        center_counts[center] += 1

        # ---- sequences
        seqs = [
            c for c in _texts(el, "targetSequenceList/targetSequence/oneLetterCode")
            if len(c) >= 20 and AA_RX.match(c)
        ]
        if seqs:
            s["targets_with_protein_sequence"] += 1
        if _texts(el, "trialList/trial/trialSequenceList/trialSequence/oneLetterCode"):
            s["targets_with_trial_sequence"] += 1

        # ---- outcome statuses
        tstat = (el.findtext("status") or "").strip()
        if tstat:
            status_target[tstat] += 1
        statuses = set(_texts(el, "trialList/trial/status"))
        statuses |= set(
            _texts(el, "trialList/trial/statusHistoryList/statusHistory/status")
        )
        if tstat:
            statuses.add(tstat)
        for st in statuses:
            status_trial[st] += 1
        real_outcome = bool(statuses - NON_OUTCOME)
        if statuses:
            s["targets_with_any_status"] += 1
        if real_outcome:
            s["targets_with_real_outcome"] += 1

        # ---- trials / protocol refs -> hosts
        target_hosts: set[str] = set()
        n_trials = 0
        has_expr_ref = False
        expr_protos_used: list[dict] = []
        hosts_from_text: set[str] = set()
        hosts_from_details: set[str] = set()
        details_strains: set[str] = set()
        details_vectors: set[str] = set()
        for tr in el.iterfind("trialList/trial"):
            n_trials += 1
            trial_hosts: set[str] = set()
            for ref in tr.iterfind("trialProtocolList/protocolRef"):
                pid = (ref.findtext("protocolId") or "").strip()
                rt = (ref.findtext("protocolType") or "").strip()
                reftype[rt] += 1
                if rt == "expression":
                    s["protocol_refs_declared_expression"] += 1

                # --- per-trial free-text deviation field
                det = " ".join((ref.findtext("protocolDetails") or "").split())
                if det:
                    s["protocol_details_blocks"] += 1
                    got_kv = False
                    for k, v in KV_RX.findall(det):
                        kl = k.lower()
                        kv_keys[kl] += 1
                        got_kv = True
                        vs = v.strip()
                        if kl == "host":
                            kv_host_values[vs.lower()] += 1
                        elif kl == "strain":
                            kv_strain_values[vs] += 1
                            details_strains.add(vs)
                        elif "vector" in kl:
                            kv_vector_values[vs] += 1
                            details_vectors.add(vs)
                    if got_kv:
                        s["protocol_details_with_key_value"] += 1
                    dh = classify_hosts(det)
                    if dh:
                        trial_hosts |= dh
                        hosts_from_details |= dh

                p = index.resolve(center, pid)
                if p is None:
                    continue
                proto_ref_use[f"{center}-{p['protocol_id']}"] += 1
                if p["type"] == "expression":
                    has_expr_ref = True
                    expr_protos_used.append(p)
                    trial_hosts |= set(p["hosts"])
                    hosts_from_text |= set(p["hosts"])
                    if not p["hosts"]:
                        s["expression_refs_resolved_but_no_host_in_text"] += 1
                        expr_nohost_use[
                            f"{center}-{p['protocol_id']} (text {p['text_len']} chars)"
                        ] += 1
            for h in trial_hosts:
                host_per_trial[h] += 1
            if trial_hosts:
                s["trials_with_host"] += 1
            s["trials"] += 1
            target_hosts |= trial_hosts

        if n_trials:
            s["targets_with_trial"] += 1
        if has_expr_ref:
            s["targets_with_expression_protocol_ref"] += 1

        if hosts_from_text:
            s["targets_with_host_from_protocol_text"] += 1
            host_src["protocol_text_only" if not hosts_from_details else "both"] += 1
            for h in hosts_from_text:
                host_per_target_by_src["protocol_text"][h] += 1
        if hosts_from_details:
            s["targets_with_host_from_protocol_details"] += 1
            if not hosts_from_text:
                host_src["protocol_details_only"] += 1
            for h in hosts_from_details:
                host_per_target_by_src["protocol_details"][h] += 1

        hosts_per_target_hist[len(target_hosts)] += 1
        lab_host_cov[lab]["targets"] += 1
        if target_hosts:
            s["targets_with_host"] += 1
            lab_host_cov[lab]["with_host"] += 1
            for h in target_hosts:
                host_per_target[h] += 1
            if real_outcome:
                s["targets_with_host_and_outcome"] += 1
            if seqs:
                s["targets_with_host_and_sequence"] += 1
            if seqs and real_outcome:
                s["targets_with_host_outcome_and_sequence"] += 1
        if len(target_hosts) >= 2:
            s["targets_multihost"] += 1
            multihost_rows.append([tid, lab, str(len(target_hosts)), "|".join(sorted(target_hosts)), "|".join(sorted(statuses))])

        # strain/vector granularity for this target's expression protocols
        if has_expr_ref or details_strains or details_vectors:
            strains, vectors = set(), set()
            for p in expr_protos_used:
                strains |= set(p["strains"])
                vectors |= set(p["vectors"])
            strains |= details_strains
            vectors |= details_vectors
            if strains:
                s["targets_with_strain"] += 1
                for x in strains:
                    strain_per_target[x] += 1
            if vectors:
                s["targets_with_vector"] += 1
                for x in vectors:
                    vector_per_target[x] += 1

        # ---- same protein, multiple hosts (exact sequence identity, cross-target)
        if seqs and target_hosts:
            for q in seqs:
                seq_hosts[hashlib.sha1(q.encode()).digest()] |= target_hosts  # noqa: S324

        if s["targets"] % 50_000 == 0:
            print(f"... {s['targets']:,} targets", file=sys.stderr, flush=True)

    seqlevel = Counter(len(v) for v in seq_hosts.values())
    out = {
        "protocols_total": len(protos),
        "protocols_by_type": proto_type.most_common(),
        "expression_protocols": len(expr_protos),
        "expression_protocols_with_minable_host": len(expr_with_host),
        "protocols_any_type_with_minable_host": len(any_with_host),
        "expression_protocol_host_labels": Counter(
            "|".join(v["hosts"]) for v in expr_protos.values()
        ).most_common(),
        "counts": dict(s),
        "protocol_ref_resolution": dict(index.stats),
        "targets_per_center": center_counts.most_common(),
        "hosts_per_target_histogram": dict(sorted(hosts_per_target_hist.items())),
        "host_per_target": host_per_target.most_common(),
        "host_per_trial": host_per_trial.most_common(),
        "protocol_ref_type_counts": reftype.most_common(),
        "distinct_protocols_referenced": len(proto_ref_use),
        "most_referenced_protocols": proto_ref_use.most_common(25),
        "most_referenced_expression_protocols_without_host": expr_nohost_use.most_common(25),
        "target_status_counts": status_target.most_common(),
        "any_status_counts": status_trial.most_common(),
        "strain_per_target": strain_per_target.most_common(40),
        "vector_per_target": vector_per_target.most_common(40),
        "strain_per_target_distinct": len(strain_per_target),
        "vector_per_target_distinct": len(vector_per_target),
        "host_source_breakdown": host_src.most_common(),
        "host_per_target_by_source": {
            k: v.most_common() for k, v in host_per_target_by_src.items()
        },
        "protocol_details_keys": kv_keys.most_common(),
        "protocol_details_host_values": kv_host_values.most_common(30),
        "protocol_details_host_values_distinct": len(kv_host_values),
        "protocol_details_strain_values": kv_strain_values.most_common(40),
        "protocol_details_strain_values_distinct": len(kv_strain_values),
        "protocol_details_vector_values": kv_vector_values.most_common(30),
        "protocol_details_vector_values_distinct": len(kv_vector_values),
        "distinct_sequences_with_host": len(seq_hosts),
        "distinct_sequences_by_n_hosts": dict(sorted(seqlevel.items())),
        "labs_by_host_coverage": sorted(
            ((k, v["targets"], v["with_host"]) for k, v in lab_host_cov.items()),
            key=lambda r: -r[1],
        )[:40],
    }
    with open(os.path.join(args.out_dir, "inventory.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    with open(os.path.join(args.out_dir, "multihost_targets.csv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["target_id", "lab", "n_distinct_hosts", "hosts", "statuses"])
        w.writerows(multihost_rows)
    print(json.dumps({k: out[k] for k in (
        "protocols_total", "protocols_by_type", "expression_protocols",
        "expression_protocols_with_minable_host",
        "expression_protocol_host_labels", "counts",
        "protocol_ref_resolution", "protocol_ref_type_counts",
        "hosts_per_target_histogram", "host_per_target", "host_per_trial",
        "host_source_breakdown", "host_per_target_by_source",
        "protocol_details_keys", "protocol_details_host_values",
        "protocol_details_strain_values_distinct",
        "protocol_details_vector_values_distinct",
        "target_status_counts", "distinct_sequences_with_host",
        "distinct_sequences_by_n_hosts", "strain_per_target_distinct",
        "vector_per_target_distinct")}, indent=2))
    print(f"wrote {args.out_dir}/inventory.json + multihost_targets.csv", file=sys.stderr)
    return 0


# ========================================================================= pairs
def cmd_pairs(args: argparse.Namespace) -> int:
    """Verify multi-host targets trial by trial.

    A target looks multi-host when the UNION of host labels over its trials has
    2+ members. That union is only a real paired observation if different
    *trials* carry different hosts. If one trial's protocol text merely mentions
    two hosts, it is an artefact -- which is exactly what CSGID's
    WU_PEI_transient_transfection protocol produces at scale, because its
    preamble mentions E. coli before describing a mammalian method.
    """
    protos = _load_protocols(args.xml)
    index = ProtocolIndex(protos)
    print(f"loaded {len(protos)} protocols", file=sys.stderr)

    verdict: Counter[str] = Counter()
    combos: dict[str, Counter] = defaultdict(Counter)
    status_by_host: dict[str, Counter] = defaultdict(Counter)
    blame: Counter[str] = Counter()
    rows: list[list[str]] = []
    n = 0

    for el in _records(args.xml, args.limit):
        if _tag(el) != "target":
            continue
        n += 1
        tid = (el.findtext("targetId") or "").strip()
        atid = (el.get("id") or "").strip()
        center = atid[: -(len(tid) + 1)] if tid and atid.endswith("-" + tid) else "?"

        per_trial: list[tuple[frozenset, str, tuple]] = []
        for tr in el.iterfind("trialList/trial"):
            th: set[str] = set()
            src: list[str] = []
            for ref in tr.iterfind("trialProtocolList/protocolRef"):
                det = " ".join((ref.findtext("protocolDetails") or "").split())
                if det:
                    dh = classify_hosts(det)
                    if dh:
                        th |= dh
                        src.append("protocolDetails")
                p = index.resolve(center, (ref.findtext("protocolId") or "").strip())
                if p and p["type"] == "expression" and p["hosts"]:
                    th |= set(p["hosts"])
                    src.append(f"{center}-{p['protocol_id']}")
            if th:
                per_trial.append(
                    (frozenset(th), (tr.findtext("status") or "").strip(), tuple(src))
                )

        allh: set[str] = set()
        for h, _, _ in per_trial:
            allh |= h
        if len(allh) < 2:
            continue

        multi = [t for t in per_trial if len(t[0]) >= 2]
        if len({h for h, _, _ in per_trial}) == 1:
            v = "ARTEFACT: all trials share one multi-host text"
        elif multi and len({h for h, _, _ in per_trial if len(h) == 1}) < 2:
            v = "ARTEFACT: one trial's text names two hosts"
        elif multi:
            v = "MIXED: mostly real, one trial's text names two hosts"
        else:
            v = "REAL: different trials, different single hosts"

        verdict[v] += 1
        combos[v]["|".join(sorted(allh))] += 1
        if v.startswith("ARTEFACT"):
            for _, _, src in multi:
                for sname in src:
                    blame[sname] += 1
        else:
            for h, st, _ in per_trial:
                if len(h) == 1 and st:
                    status_by_host[next(iter(h))][st] += 1
            rows.append([tid, center, str(len(allh)), "|".join(sorted(allh)),
                         ";".join(f"{'+'.join(sorted(h))}={st}" for h, st, _ in per_trial)])
        if n % 50_000 == 0:
            print(f"... {n:,} targets", file=sys.stderr, flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "verified_pairs.csv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["target_id", "center", "n_hosts", "hosts", "per_trial_host=status"])
        w.writerows(rows)

    out = {
        "targets_scanned": n,
        "multi_host_targets": sum(verdict.values()),
        "verdict": verdict.most_common(),
        "combos_by_verdict": {k: v.most_common() for k, v in combos.items()},
        "artefact_blamed_on_protocol": blame.most_common(15),
        "verified_pair_status_by_host": {
            k: v.most_common() for k, v in status_by_host.items()
        },
    }
    with open(os.path.join(args.out_dir, "pairs.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {args.out_dir}/pairs.json + verified_pairs.csv", file=sys.stderr)
    return 0


# ======================================================================== schema
def cmd_schema(args: argparse.Namespace) -> int:
    paths: Counter[str] = Counter()
    values: dict[str, Counter[str]] = defaultdict(Counter)
    CAP = 400

    def walk(el, prefix):
        p = f"{prefix}/{_tag(el)}"
        paths[p] += 1
        for k, v in el.attrib.items():
            key = f"{p}@{k}"
            paths[key] += 1
            if len(values[key]) < CAP:
                values[key][v[:100]] += 1
        text = (el.text or "").strip()
        if text and len(values[p]) < CAP:
            values[p][text[:100]] += 1
        for child in el:
            walk(child, p)

    n = 0
    for el in _records(args.xml, args.limit):
        n += 1
        walk(el, "")
    print(f"RECORDS_SCANNED\t{n}")
    print("\n=== ELEMENT / ATTRIBUTE PATHS ===")
    for p, c in paths.most_common():
        print(f"{c}\t{p}")
    print("\n=== VALUE HISTOGRAMS ===")
    for p in sorted(values):
        c = values[p]
        print(f"--- {p}  ({len(c)} distinct seen, cap {CAP})")
        for v, k in c.most_common(args.top):
            print(f"    {k}\t{v}")
    return 0


# ======================================================================== driver
def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch")
    f.add_argument("--dest", required=True, help="dir for the tarball (keep outside the repo)")
    f.set_defaults(fn=cmd_fetch)

    e = sub.add_parser("extract")
    e.add_argument("--tarball", required=True)
    e.add_argument("--dest", required=True, help="NEW EMPTY directory")
    e.set_defaults(fn=cmd_extract)

    for name, fn in (("schema", cmd_schema), ("protocols", cmd_protocols)):
        c = sub.add_parser(name)
        c.add_argument("--xml", required=True)
        c.add_argument("--limit", type=int, default=0, help="stop after N top-level records")
        if name == "schema":
            c.add_argument("--top", type=int, default=60)
        c.set_defaults(fn=fn)

    for name, fn in (("inventory", cmd_inventory), ("pairs", cmd_pairs)):
        c = sub.add_parser(name)
        c.add_argument("--xml", required=True)
        c.add_argument("--out-dir", required=True)
        c.add_argument("--limit", type=int, default=0)
        c.set_defaults(fn=fn)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
