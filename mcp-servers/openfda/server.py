#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""openFDA MCP server — exposes the FDA open data API (api.fda.gov) to Claude as tools.

Claude Code launches this as a stdio MCP server. One-time setup:
    pip install mcp          # the only dependency (HTTP uses the Python standard library)

Uses OPENFDA_API_KEY from the environment **if set** — it's optional and only raises the
rate limit (~1,000 → ~120,000 requests/day); every tool works without a key. Set one up
with the /openfda:setup command.
"""
import json
import logging
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

# Pre-flight: this server needs Python >= 3.10 (the `mcp` SDK does not support
# 3.9) and the `mcp` package itself. Check both up front and fail loud with
# guidance, rather than dying on an opaque ImportError or a syntax error raised
# by a newer dependency on an old interpreter.
_MIN_PY = (3, 10)
if sys.version_info < _MIN_PY:
    sys.exit(
        f"openfda MCP server requires Python >= {_MIN_PY[0]}.{_MIN_PY[1]}; "
        f"this interpreter is {sys.version.split()[0]}. "
        "Upgrade Python, then install dependencies:  pip install -r requirements.txt"
    )
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    sys.exit(
        "openfda MCP server requires the 'mcp' package (Python >=3.10). "
        "Install it:  pip install -r requirements.txt  (or: pip install mcp)"
    )

mcp = FastMCP("openfda")
BASE = "https://api.fda.gov"

# Server-side logging → stderr (NEVER stdout; stdout is the MCP stdio protocol channel).
# Gives failures an observable trail independent of what is returned to the caller
# (21 CFR Part 11 §11.10(e); EU GMP Annex 11 cl.9). Level via OPENFDA_LOG_LEVEL.
logging.basicConfig(
    stream=sys.stderr,
    level=getattr(logging, os.environ.get("OPENFDA_LOG_LEVEL", "WARNING").upper(), logging.WARNING),
    format="%(asctime)s openfda %(levelname)s %(message)s",
)
log = logging.getLogger("openfda")

# Surface the /openfda:setup nudge once per server-process lifetime when there's no key.
# We do this in two places: (1) on a 429 rate-limit error, because that's the moment the
# user actually feels the absent key bite; (2) on the FIRST successful no-key response, as
# a single tip so they know personal-key territory exists before they hit the wall.
_HINTED_NO_KEY = False


def _query(endpoint: str, search: str, limit: int) -> dict:
    """Call an openFDA endpoint; return {'total', 'results'} or {'error'} / no-match note."""
    global _HINTED_NO_KEY
    limit = max(1, min(int(limit), 50))
    params = {"search": search, "limit": limit}
    key = os.environ.get("OPENFDA_API_KEY")
    if key:
        params["api_key"] = key
    url = f"{BASE}/{endpoint}.json?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"total": 0, "results": [], "note": "No matching records."}
        if e.code == 429:
            # Rate-limited. The advice differs depending on whether they're on the shared
            # tier or have already burned through a personal-key quota.
            log.warning("openFDA 429 rate limit on %s (personal key set: %s)", endpoint, bool(key))
            if not key:
                msg = ("openFDA rate limit hit — you are on the shared (no-key) tier "
                       "(~1,000 requests/day). Run /openfda:setup to get a free personal "
                       "API key in under a minute (raises the limit to ~120,000/day).")
            else:
                msg = ("openFDA rate limit hit — your personal key has reached its "
                       "daily quota. It resets at midnight UTC.")
            return {"error": msg, "rate_limit": True}
        detail = e.read().decode("utf-8", "replace")[:300]
        log.error("openFDA HTTP %s on %s: %s", e.code, endpoint, detail)
        return {"error": f"openFDA HTTP {e.code}", "detail": detail}
    except Exception as e:                       # network/timeout/parse
        log.exception("openFDA request failed on %s: %s", endpoint, e)
        return {"error": str(e)}
    result = {"total": (data.get("meta", {}).get("results", {}) or {}).get("total"),
              "results": data.get("results", [])}
    # First successful call this session without a key → drop a single non-intrusive tip.
    if not key and not _HINTED_NO_KEY:
        _HINTED_NO_KEY = True
        result["tip"] = ("No OPENFDA_API_KEY set — using shared limits (~1,000/day). "
                         "Run /openfda:setup to get a free personal key "
                         "(raises to ~120,000/day). Shown once per session.")
    return result


def _pick(d: dict, keys) -> dict:
    return {k: d.get(k) for k in keys if d.get(k) is not None}


def _trunc(v, n=600) -> str:
    s = " ".join(v) if isinstance(v, list) else (v or "")
    return s[:n] + ("…" if len(s) > n else "")


@mcp.tool()
def search_enforcement(category: str, search: str, limit: int = 5) -> dict:
    """Search FDA recall / enforcement reports.

    category: 'drug', 'device', or 'food'.
    search:   an openFDA query — e.g. 'recalling_firm:"Acme Pharma"',
              'product_description:insulin', 'classification:"Class I"', or combine with
              '+AND+' (e.g. 'classification:"Class I"+AND+state:CA').
    Returns recalls trimmed to the key fields: status, classification (I/II/III),
    recalling firm, product, reason, initiation date, voluntary/mandated.
    """
    cat = category.lower().strip()
    if cat not in {"drug", "device", "food"}:
        return {"error": "category must be 'drug', 'device', or 'food'"}
    res = _query(f"{cat}/enforcement", search, limit)
    if "results" in res:
        res["results"] = [_pick(r, [
            "recall_number", "status", "classification", "recalling_firm",
            "product_description", "reason_for_recall", "recall_initiation_date",
            "voluntary_mandated", "distribution_pattern", "state", "country",
        ]) for r in res["results"]]
    return res


@mcp.tool()
def search_drug_labels(search: str, limit: int = 3) -> dict:
    """Search FDA structured drug labeling (SPL).

    search: e.g. 'openfda.brand_name:"Tylenol"', 'openfda.generic_name:metformin'.
    Returns brand/generic/manufacturer plus truncated indications, warnings and dosage.
    """
    res = _query("drug/label", search, limit)
    if "results" in res:
        out = []
        for r in res["results"]:
            o = r.get("openfda", {}) or {}
            out.append({
                "brand_name": o.get("brand_name"),
                "generic_name": o.get("generic_name"),
                "manufacturer_name": o.get("manufacturer_name"),
                "indications_and_usage": _trunc(r.get("indications_and_usage")),
                "warnings": _trunc(r.get("warnings")),
                "dosage_and_administration": _trunc(r.get("dosage_and_administration")),
            })
        res["results"] = out
    return res


@mcp.tool()
def search_drug_adverse_events(search: str, limit: int = 5) -> dict:
    """Search FDA drug adverse-event reports (FAERS).

    search: e.g. 'patient.drug.medicinalproduct:metformin',
            'patient.reaction.reactionmeddrapt:"NAUSEA"', or a date range
            'receivedate:[20240101+TO+20241231]'.
    Returns each report's id, seriousness, date, and its reactions + drugs (capped).
    """
    res = _query("drug/event", search, limit)
    if "results" in res:
        out = []
        for r in res["results"]:
            p = r.get("patient", {}) or {}
            out.append({
                "safetyreportid": r.get("safetyreportid"),
                "serious": r.get("serious"),
                "receivedate": r.get("receivedate"),
                "reactions": [rx.get("reactionmeddrapt") for rx in p.get("reaction", [])][:10],
                "drugs": [d.get("medicinalproduct") for d in p.get("drug", [])][:10],
            })
        res["results"] = out
    return res


@mcp.tool()
def openfda_query(endpoint: str, search: str, limit: int = 5) -> dict:
    """Generic openFDA query for any endpoint not covered by the specific tools.

    endpoint: an openFDA path WITHOUT '.json', e.g. 'device/510k', 'device/event',
              'drug/ndc', 'food/event', 'animalandveterinary/event'.
    search:   a raw openFDA query string.
    Returns the total count and up to `limit` raw result records (large objects are
    returned as-is — prefer the specific tools where they exist).
    """
    endpoint = endpoint.strip().strip("/").removesuffix(".json")
    return _query(endpoint, search, min(int(limit), 10))


@mcp.tool()
def server_version() -> dict:
    """Return the deployed paraqualis-skills version + the server's Python runtime.

    Lets a caller confirm at runtime which qualified build is in use, rather than
    trusting a static manifest (21 CFR Part 11 §11.10(k); GAMP 5 change control).
    """
    import platform
    from pathlib import Path
    name, version = "paraqualis-gxp", "unknown"
    manifest = Path(__file__).resolve().parents[2] / ".claude-plugin" / "plugin.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        name = data.get("name", name)
        version = data.get("version", version)
    except Exception as e:
        log.warning("could not read plugin.json: %s", e)
    return {"plugin": name, "version": version, "python": platform.python_version()}


if __name__ == "__main__":
    mcp.run()                                    # stdio transport (how Claude Code connects)
