#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""Shared, read-only helper for the OQ openFDA test-cases (OQ-007..OQ-015, OQ-032).

The system under test is mcp-servers/openfda/server.py. That module does
`from mcp.server.fastmcp import FastMCP` at import time (server.py:21) and decorates
its tools with @mcp.tool(). The `mcp` package may not be installed in the OQ test
environment, so this helper injects a minimal, behaviour-preserving stub for
`mcp.server.fastmcp.FastMCP` into sys.modules BEFORE importing server. The stub's
.tool() decorator returns the wrapped function unchanged, so the REAL server logic
(_query, _trunc, search_enforcement, openfda_query) is exercised — not a re-implementation.

This is read-only and offline: it never performs a live network call. Tests that need
HTTP responses monkeypatch server's urllib.* with deterministic fakes.
"""
import os
import sys
import types
import importlib.util

REPO = os.environ.get("OQ_REPO") or os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
SERVER_PATH = os.path.join(REPO, "mcp-servers", "openfda", "server.py")


def _install_mcp_stub():
    """Inject a minimal mcp.server.fastmcp stub if mcp is not importable."""
    try:
        import mcp.server.fastmcp  # noqa: F401  (real package present — use it)
        return False
    except Exception:
        pass

    class _FastMCP:
        def __init__(self, *a, **k):
            pass

        def tool(self, *a, **k):
            def deco(fn):
                return fn  # leave the real function untouched
            return deco

        def run(self, *a, **k):
            raise RuntimeError("stub FastMCP.run() must not be called in OQ tests")

    mcp_mod = types.ModuleType("mcp")
    server_mod = types.ModuleType("mcp.server")
    fastmcp_mod = types.ModuleType("mcp.server.fastmcp")
    fastmcp_mod.FastMCP = _FastMCP
    server_mod.fastmcp = fastmcp_mod
    mcp_mod.server = server_mod
    sys.modules["mcp"] = mcp_mod
    sys.modules["mcp.server"] = server_mod
    sys.modules["mcp.server.fastmcp"] = fastmcp_mod
    return True


def load_server():
    """Import and return the real server module from the repo under test."""
    if not os.path.isfile(SERVER_PATH):
        sys.stderr.write(f"FAIL: server.py not found at {SERVER_PATH}\n")
        sys.exit(1)
    _install_mcp_stub()
    spec = importlib.util.spec_from_file_location("openfda_server_under_test", SERVER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
