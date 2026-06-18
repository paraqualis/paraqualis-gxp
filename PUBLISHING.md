# Publishing paraqualis-skills to Claude Code Plugin Marketplace

This guide covers the authoritative steps to publish a Claude Code plugin with MCP servers, hooks, commands, sub-agents, and skills. All documentation references are current as of June 2026.

**Documentation sources:**
- https://code.claude.com/docs/en/plugins.md — Plugin creation and development
- https://code.claude.com/docs/en/plugins-reference.md — Complete technical schemas
- https://code.claude.com/docs/en/plugin-marketplaces.md — Marketplace distribution

---

## 1. Plugin MCP Servers

### How MCP Servers Are Bundled in Plugins

MCP servers are declared in **`.mcp.json`** at the plugin root, or inline in `plugin.json` under the `mcpServers` key. The plugin manifest does NOT require a special `mcpServers` field in `plugin.json`—it's either a reference to `.mcp.json` or inline configuration.

### Schema and Path Variables

**Location:**
- Default: `.mcp.json` in plugin root
- Or inline: `"mcpServers": { ... }` in `plugin.json`

**Example `.mcp.json` (Python stdio server):**

```json
{
  "openfda": {
    "command": "python3",
    "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-servers/openfda/server.py"]
  }
}
```

**Or inline in `plugin.json`:**

```json
{
  "name": "paraqualis-skills",
  "version": "1.0.0",
  "mcpServers": {
    "openfda": {
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-servers/openfda/server.py"]
    }
  }
}
```

### Path Variables for Plugins

- **`${CLAUDE_PLUGIN_ROOT}`** — Absolute path to the plugin's installation directory. Use this to reference all plugin files (scripts, binaries, config). Required for Python stdio servers.
- **`${CLAUDE_PLUGIN_DATA}`** — Persistent directory for plugin state (survives updates). Use for installed dependencies, generated code, caches.
- **`${CLAUDE_PROJECT_DIR}`** — The project root where Claude Code was launched.

### Python-based Stdio MCP Server Declaration

For a Python MCP server using the `mcp` package (requires Python ≥3.10):

**Option A (run the server script with python3 — what this plugin uses):**
```json
{
  "command": "python3",
  "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-servers/openfda/server.py"]
}
```

**Option B (invoke as a script if it has a shebang):**
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/openfda/server.py"
}
```

**Ensure the script is executable:**
```bash
chmod +x mcp-servers/openfda/server.py
```

**shebang line in the Python script:**
```python
#!/usr/bin/env python3
```

### MCP Server Integration

- Servers start automatically when the plugin is enabled
- Tools appear as standard MCP tools in Claude's toolkit
- Server declarations can include `env`, `args`, and `cwd` fields
- Multiple MCP servers are merged from `.mcp.json` and `plugin.json` inline config if both exist

---

## 2. Plugin Hooks

### How Hooks Are Bundled

Hooks are declared in **`hooks/hooks.json`** at the plugin root, or inline in `plugin.json` under the `hooks` key.

**Location:**
- Default: `hooks/hooks.json` in plugin root
- Or inline: `"hooks": { ... }` in `plugin.json`

### Hook Mechanism and Auto-Discovery

No special field in `plugin.json` is required to point at `hooks/hooks.json`—Claude Code auto-discovers it. If you use `.mcp.json`, hooks still auto-discover from the default location.

**Example `hooks/hooks.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/protect-approved-documents.py\""
          }
        ]
      }
    ]
  }
}
```

### Using `${CLAUDE_PLUGIN_ROOT}` in Hooks

Path must be wrapped in double quotes when used in shell-form hook commands:
```json
"command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/protect-approved-documents.py\""
```

Or use exec form with `args`:
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/protect-approved-documents.py",
  "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
}
```

### Hook Events Supported

PostToolUse, PreToolUse, SessionStart, UserPromptSubmit, PermissionRequest, and others. See [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md).

---

## 3. plugin.json Schema

### Required vs. Optional Fields

**Only `name` is required.** If you omit `plugin.json` entirely, Claude Code auto-discovers components in default locations (`skills/`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, etc.) and derives the name from the directory.

### Complete Schema for Publishable Plugin

```json
{
  "name": "paraqualis-skills",
  "displayName": "Paraqualis CSV & Regulatory Skills",
  "version": "1.0.0",
  "description": "Comprehensive toolkit for life-sciences computerized system validation (CSV), GxP regulatory guidance, and GAMP 5 assessment",
  "author": {
    "name": "Craig Wylie",
    "email": "craig.w.wylie@gmail.com",
    "url": "https://github.com/craigwylie"
  },
  "homepage": "https://github.com/craigwylie/paraqualis-skills",
  "repository": "https://github.com/craigwylie/paraqualis-skills",
  "license": "MIT",
  "keywords": ["csv", "gamp", "validation", "pharma", "regulatory", "part11"],
  
  "skills": "skills/",
  "commands": "commands/",
  "agents": "agents/",
  "hooks": "hooks/hooks.json",
  "mcpServers": ".mcp.json",
  
  "version": "1.0.0"
}
```

### Field Reference

| Field            | Type    | Required | Purpose                                                                                  |
| :--------------- | :------ | :------- | :--------------------------------------------------------------------------------------- |
| `name`           | string  | Yes      | Plugin identifier (kebab-case, no spaces). Namespaces all components.                   |
| `displayName`    | string  | No       | Human-readable name shown in UI (may contain spaces). Requires Claude Code v2.1.143+.   |
| `version`        | string  | No       | Semantic version (e.g., "1.0.0"). Sets update behavior; if omitted, git SHA is used.    |
| `description`    | string  | No       | Brief explanation of plugin purpose.                                                    |
| `author`         | object  | No       | `{name, email, url}` for attribution.                                                   |
| `homepage`       | string  | No       | Documentation URL.                                                                      |
| `repository`     | string  | No       | Source code URL.                                                                        |
| `license`        | string  | No       | SPDX license identifier (e.g., "MIT").                                                  |
| `keywords`       | array   | No       | Tags for discovery and categorization.                                                  |
| `skills`         | string  | No       | Custom skill directory path; adds to default `skills/` scan.                            |
| `commands`       | string  | No       | Custom commands/skills directory path; replaces default.                                |
| `agents`         | string  | No       | Custom agents directory path; replaces default.                                         |
| `hooks`          | string  | No       | Custom hooks config path (e.g., "hooks/hooks.json") or inline object.                   |
| `mcpServers`     | string  | No       | Custom MCP config path (e.g., ".mcp.json") or inline object.                            |
| `lspServers`     | string  | No       | Language Server Protocol config path or inline object.                                  |
| `defaultEnabled` | boolean | No       | If `false`, plugin installs disabled (user must enable). Requires v2.1.154+.             |

### Schema Validation

**Run validation before publishing:**

```bash
claude plugin validate .
```

or from inside a session:

```
/plugin validate .
```

### Auto-Discovery of Components

If you omit component fields, Claude Code looks in default locations:
- `skills/` — for skills (structure: `skills/<name>/SKILL.md`)
- `commands/` — for flat `.md` skill files
- `agents/` — for agent definitions
- `hooks/hooks.json` — for hook configuration
- `.mcp.json` — for MCP server config
- `.lsp.json` — for LSP server config

**You do NOT need to list these in `plugin.json` unless you want custom paths.**

---

## 4. marketplace.json Schema

### Required and Optional Fields

**Location:** `.claude-plugin/marketplace.json` at the repository root.

### Marketplace Manifest Structure

```json
{
  "name": "paraqualis-plugins",
  "owner": {
    "name": "Craig Wylie",
    "email": "craig.w.wylie@gmail.com"
  },
  "description": "Comprehensive plugin suite for life-sciences CSV validation, GAMP 5 assessment, and 21 CFR Part 11 compliance",
  "version": "1.0.0",
  
  "plugins": [
    {
      "name": "paraqualis-skills",
      "source": "./",
      "description": "Expert advisors and validation tools for pharma/medtech GxP systems",
      "version": "1.0.0",
      "author": {
        "name": "Craig Wylie",
        "email": "craig.w.wylie@gmail.com"
      },
      "homepage": "https://github.com/craigwylie/paraqualis-skills",
      "repository": "https://github.com/craigwylie/paraqualis-skills",
      "license": "MIT",
      "keywords": ["csv", "gamp", "validation", "pharma", "regulatory"]
    }
  ]
}
```

### Field Reference

**Marketplace-level fields:**

| Field          | Type   | Required | Purpose                                                                                 |
| :------------- | :----- | :------- | :-------------------------------------------------------------------------------------- |
| `name`         | string | Yes      | Marketplace identifier (kebab-case, no spaces). Users install with `@marketplace-name`. |
| `owner`        | object | Yes      | Maintainer info: `{ name (required), email (optional) }`.                               |
| `description`  | string | No       | Brief marketplace description.                                                          |
| `version`      | string | No       | Marketplace manifest version.                                                           |
| `plugins`      | array  | Yes      | List of plugin entries.                                                                 |

**Plugin entry fields (in `plugins[]`):**

| Field           | Type           | Required | Purpose                                                           |
| :-------------- | :------------- | :------- | :---------------------------------------------------------------- |
| `name`          | string         | Yes      | Plugin identifier. Users install with `plugin-name@marketplace`.  |
| `source`        | string\|object | Yes      | Where to fetch the plugin (see "Plugin sources" below).           |
| `description`   | string         | No       | Brief plugin description.                                         |
| `version`       | string         | No       | Plugin version. If set, users only update when this changes.      |
| `author`        | object         | No       | Plugin author `{name, email, url}`.                               |
| `homepage`      | string         | No       | Documentation URL.                                                |
| `repository`    | string         | No       | Source code URL.                                                  |
| `license`       | string         | No       | SPDX license identifier.                                          |
| `keywords`      | array          | No       | Tags for discovery.                                               |
| `category`      | string         | No       | Plugin category for organization.                                 |
| `strict`        | boolean        | No       | If `false`, marketplace entry fully defines components (v2.1.158+).|
| `defaultEnabled`| boolean        | No       | If `false`, plugin installs disabled (v2.1.154+).                 |

### Plugin Sources

**Relative path (same repository):**
```json
"source": "./"
```
Resolves relative to marketplace root (where `.claude-plugin/marketplace.json` lives).

**GitHub repository:**
```json
"source": {
  "source": "github",
  "repo": "owner/repo",
  "ref": "v1.0.0",
  "sha": "a1b2c3d4..."
}
```

**Git repository (any host):**
```json
"source": {
  "source": "url",
  "url": "https://gitlab.com/team/plugin.git",
  "ref": "main"
}
```

**Git subdirectory:**
```json
"source": {
  "source": "git-subdir",
  "url": "https://github.com/acme/monorepo.git",
  "path": "tools/claude-plugin"
}
```

**npm package:**
```json
"source": {
  "source": "npm",
  "package": "@org/plugin",
  "version": "2.1.0"
}
```

---

## 5. Publication Process End-to-End

### Step-by-Step Publication

#### 1. Prepare Your Repository

Your public GitHub repository must contain:

```
paraqualis-skills/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest (required)
│   └── marketplace.json     # Marketplace catalog (if creating a marketplace)
├── skills/                  # Skill definitions
├── commands/                # Flat skill commands
├── agents/                  # Agent definitions
├── hooks/
│   └── hooks.json          # Hook configuration
├── mcp-servers/
│   └── openfda/
│       └── server.py       # MCP server (Python stdio)
├── .mcp.json               # MCP server declarations
├── README.md               # Installation and usage instructions
├── CHANGELOG.md            # Version history
└── LICENSE                 # License file
```

#### 2. Validate Your Plugin Locally

```bash
claude plugin validate .
```

Check for:
- Valid JSON syntax in `plugin.json`, `marketplace.json`, `.mcp.json`, and `hooks/hooks.json`
- Correct frontmatter in skills, agents, and commands
- No path traversal issues (`../` paths)
- Kebab-case naming for plugin and marketplace names

#### 3. Test Locally Before Publishing

```bash
# Test with --plugin-dir
claude --plugin-dir ./

# Inside a session, verify your skills and MCP server work
/paraqualis-skills:gamp-advisor

# Check MCP server is available
/mcp
```

#### 4. Publish to GitHub

Push your repository to public GitHub:

```bash
git remote add origin https://github.com/yourusername/paraqualis-skills.git
git push -u origin main
```

#### 5. Add Your Plugin to Community Marketplace (Optional)

Users can install your plugin by:
1. Adding your GitHub repository as a marketplace
2. Installing the plugin from it

**Distribution options (in order of certainty):**

1. **Your own GitHub marketplace (recommended; works today).** This repo already contains
   `.claude-plugin/marketplace.json`, so anyone can install straight from GitHub — no
   third-party listing needed:
   ```
   /plugin marketplace add <owner>/paraqualis-skills
   /plugin install paraqualis-skills@paraqualis
   ```
2. **An official / community marketplace listing.** Any curated submission process is
   evolving — **verify the current method in the official docs before relying on a specific
   URL**: https://code.claude.com/docs/en/plugin-marketplaces . Do not assume a submission
   URL that is not confirmed there; option 1 works regardless of any listing.

#### 6. Version Management and Updates

**Option A: Explicit versioning (stable releases)**
- Set `"version": "1.0.0"` in `plugin.json`
- Bump this field on every release
- Commit and tag with a git tag: `v1.0.0`
- Users only receive updates when you change this field

**Option B: Commit-SHA versioning (active development)**
- Omit `version` from `plugin.json`
- Every new commit is treated as a new version
- Simplest for internal/team plugins

**Create a release tag:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 6. User Installation Workflow

### For Users Installing from Your Repository

**Add your marketplace:**
```
/plugin marketplace add yourusername/paraqualis-skills
```

**Install the plugin:**
```
/plugin install paraqualis-skills@paraqualis-plugins
```

Or install directly from GitHub:
```
/plugin install paraqualis-skills@anthropics/claude-plugins-community
```
(if approved for official community marketplace)

**Update:**
```
/plugin update paraqualis-skills
```

---

## 7. Common Gotchas and Troubleshooting

### Plugin Won't Load

**Symptoms:** `claude --plugin-dir ./` starts but plugin is not available

**Causes and fixes:**

1. **Invalid `plugin.json` JSON syntax**
   - Run `claude plugin validate .`
   - Check for missing commas, unquoted strings, trailing commas

2. **Components in wrong directory**
   - ❌ `my-plugin/.claude-plugin/skills/` — WRONG
   - ✅ `my-plugin/skills/` — CORRECT
   - Only `plugin.json` goes in `.claude-plugin/`

3. **Missing executable bit on scripts**
   ```bash
   chmod +x hooks/protect-approved-documents.py
   chmod +x mcp-servers/openfda/server.py
   ```

4. **Hooks path incorrect**
   - Default: `hooks/hooks.json` (auto-discovered, no need to specify in `plugin.json`)
   - If custom path: `"hooks": "config/my-hooks.json"` in `plugin.json`

### MCP Server Not Starting

**Symptoms:** MCP server declared but doesn't connect; `claude --debug` shows errors

**Causes and fixes:**

1. **Python interpreter not found**
   - Verify: `python3 --version` (requires Python ≥3.10)
   - Use full path in command: `"command": "python3"` or `/usr/bin/python3`

2. **Server script not executable**
   ```bash
   chmod +x mcp-servers/openfda/server.py
   ```

3. **Shebang missing**
   - Script needs: `#!/usr/bin/env python3` as first line

4. **Missing `${CLAUDE_PLUGIN_ROOT}` in path**
   - Use: `"args": ["${CLAUDE_PLUGIN_ROOT}/mcp-servers/openfda/server.py"]`
   - NOT: `"args": ["./mcp-servers/openfda/server.py"]` (won't work after installation)

5. **Environment variables missing**
   - If server needs `PYTHONPATH`: `"env": { "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/openfda" }`

### Hooks Not Firing

**Symptoms:** Hook declared but doesn't execute

**Causes and fixes:**

1. **Event name misspelled (case-sensitive)**
   - ❌ `"postToolUse"` — WRONG (camelCase)
   - ✅ `"PostToolUse"` — CORRECT (PascalCase)

2. **Matcher doesn't match your tools**
   - Edit matcher: `"matcher": "Write|Edit"` for file operations
   - Leave empty to match all tools

3. **Script not executable**
   ```bash
   chmod +x hooks/protect-approved-documents.py
   ```

4. **Path uses wrong quoting in shell form**
   - ❌ `"command": "${CLAUDE_PLUGIN_ROOT}/hook.sh"` — Missing quotes
   - ✅ `"command": "\"${CLAUDE_PLUGIN_ROOT}/hook.sh\""` — Wrapped in double quotes

### Marketplace Installation Fails

**Symptoms:** Users can add your marketplace but plugin install fails

**Causes and fixes:**

1. **`marketplace.json` not at `.claude-plugin/marketplace.json`**
   - Ensure path is exactly `.claude-plugin/marketplace.json` at repo root

2. **Plugin source path doesn't exist**
   - If `"source": "./"`, your `plugin.json` must be at the repo root
   - If `"source": "./plugins/my-plugin"`, `plugin.json` must be at `plugins/my-plugin/.claude-plugin/plugin.json`

3. **Duplicate plugin names in marketplace**
   - Each plugin in `plugins[]` must have a unique `name`

4. **`${CLAUDE_PLUGIN_ROOT}` not used in hooks/MCP configs**
   - After installation, plugins are copied to cache
   - Relative paths like `./` or `../` won't work
   - Always use `${CLAUDE_PLUGIN_ROOT}` for bundled files

### Plugins with Both Hooks and MCP Servers

**Common issues:**

1. **Both `.mcp.json` and `"mcpServers"` in `plugin.json`** — They merge, so duplication is fine but confusing. Choose one approach.

2. **Hook tries to call MCP server that hasn't started yet** — Use `SessionStart` event to initialize state before other hooks fire.

3. **Hook and MCP server fight over `${CLAUDE_PLUGIN_DATA}`** — Different servers/hooks writing to same directory can race. Use subdirectories per component.

---

## Validation Commands

### Before Publishing

```bash
# Validate manifest and syntax
claude plugin validate .

# Run in strict mode to catch misspellings
claude plugin validate . --strict

# List components
claude plugin list --json

# Test locally
claude --plugin-dir ./

# Inside session
/plugin validate .
/plugin list
```

---

## Example: paraqualis-skills Publishing Checklist

- [ ] `.claude-plugin/plugin.json` has valid JSON and all required metadata
- [ ] `.claude-plugin/marketplace.json` defined (if creating a marketplace)
- [ ] `skills/` contains valid `SKILL.md` files
- [ ] `agents/` contains valid agent definitions with frontmatter
- [ ] `commands/` contains flat `.md` files or empty (if using `skills/`)
- [ ] `hooks/hooks.json` has valid JSON and uses `${CLAUDE_PLUGIN_ROOT}` for paths
- [ ] `mcp-servers/openfda/server.py` is executable (`chmod +x`)
- [ ] `.mcp.json` declares the server with `${CLAUDE_PLUGIN_ROOT}` and Python interpreter
- [ ] All scripts have shebang (`#!/usr/bin/env python3` or `#!/bin/bash`)
- [ ] `README.md` includes installation instructions
- [ ] `CHANGELOG.md` documents version changes
- [ ] `LICENSE` file present (MIT, Apache, etc.)
- [ ] Tested locally with `claude --plugin-dir ./`
- [ ] Validated with `claude plugin validate .`
- [ ] Pushed to public GitHub
- [ ] Ready to submit to community marketplace (optional)

---

## Links and References

**Official Claude Code Documentation:**
- [Plugins](https://code.claude.com/docs/en/plugins.md)
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)
- [Discover & Install Plugins](https://code.claude.com/docs/en/discover-plugins.md)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)
- [MCP Documentation](https://code.claude.com/docs/en/mcp.md)
- [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

**Community Resources:**
- [Community Plugin Marketplace](https://github.com/anthropics/claude-plugins-community)
- [Official Plugin Marketplace](https://github.com/anthropics/claude-plugins-official)

