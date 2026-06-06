#!/usr/bin/env bash
#
# setup.sh — one-shot local setup for the EA LLM Wiki foundation.
#
# Installs the prerequisites the wiki needs but does NOT commit (third-party
# tools under their own licenses): the PlantUML JAR (GPLv3) and the
# obsidian-plantuml / Smart Connections community plugins. The repo ships only
# its own Obsidian config, so once these land the committed settings apply.
#
# Safe to re-run: every step checks before acting.
#
# Usage:
#   ./setup.sh              # full setup (macOS / Homebrew)
#   ./setup.sh --check      # report what's present/missing, install nothing
#   ./setup.sh --skip-brew  # don't touch Homebrew packages (you manage them)
#   ./setup.sh --skip-plugins   # skip the two community-plugin downloads
#   ./setup.sh --skip-mermaid   # skip mermaid-cli (only needed for headless
#                                 diagram checks in Claude Code worktrees)
#   ./setup.sh -h | --help
#
set -euo pipefail

# ---------------------------------------------------------------------------
# Config — third-party sources (each under its own license; not redistributed)
# ---------------------------------------------------------------------------
PLANTUML_REPO="plantuml/plantuml"                      # GPLv3 distribution
PLUGIN_PLANTUML_REPO="joethei/obsidian-plantuml"
PLUGIN_SMART_REPO="brianpetro/obsidian-smart-connections"

# ---------------------------------------------------------------------------
# Pretty logging
# ---------------------------------------------------------------------------
if [[ -t 1 ]]; then
  BOLD=$'\033[1m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; DIM=$'\033[2m'; RESET=$'\033[0m'
else
  BOLD=""; GREEN=""; YELLOW=""; RED=""; DIM=""; RESET=""
fi
info() { printf '%s\n' "${BOLD}==>${RESET} $*"; }
ok()   { printf '%s\n' "  ${GREEN}ok${RESET}   $*"; }
warn() { printf '%s\n' "  ${YELLOW}warn${RESET} $*"; }
miss() { printf '%s\n' "  ${RED}miss${RESET} $*"; }
skip() { printf '%s\n' "  ${DIM}skip${RESET} $*"; }
die()  { printf '%s\n' "${RED}error:${RESET} $*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
CHECK=0; SKIP_BREW=0; SKIP_PLUGINS=0; SKIP_MERMAID=0
for arg in "$@"; do
  case "$arg" in
    --check)        CHECK=1 ;;
    --skip-brew)    SKIP_BREW=1 ;;
    --skip-plugins) SKIP_PLUGINS=1 ;;
    --skip-mermaid) SKIP_MERMAID=1 ;;
    -h|--help)      grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)              die "unknown option: $arg (try --help)" ;;
  esac
done

# ---------------------------------------------------------------------------
# Locate repo root (this script lives at the repo root) and the vault config
# ---------------------------------------------------------------------------
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"
OBS="wiki/.obsidian"
[[ -d "$OBS" ]] || die "expected $OBS — run this from the repo root (where CLAUDE.md lives)."
JAR="$OBS/plantuml/plantuml.jar"
PLUGINS_DIR="$OBS/plugins"

IS_MAC=0; [[ "$(uname -s)" == "Darwin" ]] && IS_MAC=1

# ===========================================================================
# CHECK MODE — report status, change nothing
# ===========================================================================
if [[ "$CHECK" -eq 1 ]]; then
  info "Status check (no changes will be made)"
  for t in brew git gh java dot node mmdc; do
    if have "$t"; then ok "$t"; else miss "$t not on PATH"; fi
  done
  [[ -f "$JAR" ]] && ok "PlantUML JAR present ($(du -h "$JAR" | cut -f1))" || miss "PlantUML JAR missing ($JAR)"
  for id in obsidian-plantuml smart-connections; do
    if [[ -f "$PLUGINS_DIR/$id/main.js" && -f "$PLUGINS_DIR/$id/manifest.json" ]]; then
      ok "plugin $id installed"
    else
      miss "plugin $id not installed"
    fi
  done
  if [[ "$IS_MAC" -eq 1 ]]; then
    [[ -e /Library/Java/JavaVirtualMachines/openjdk.jdk ]] && ok "OpenJDK symlink present" || miss "OpenJDK symlink missing (GUI Java)"
  fi
  exit 0
fi

[[ "$IS_MAC" -eq 1 ]] || warn "Not macOS — brew/symlink steps assume macOS; adapt as needed."

# ===========================================================================
# 1. Homebrew prerequisites
# ===========================================================================
if [[ "$SKIP_BREW" -eq 1 ]]; then
  info "Homebrew packages — skipped (--skip-brew)"
elif ! have brew; then
  warn "Homebrew not found. Install it from https://brew.sh and re-run, or"
  warn "install git, gh, openjdk, graphviz, node manually then use --skip-brew."
else
  info "Homebrew packages"
  # CLI formulae
  for pkg in git gh openjdk graphviz node; do
    if brew list --formula "$pkg" >/dev/null 2>&1; then ok "$pkg"; else info "installing $pkg"; brew install "$pkg"; fi
  done
  # Obsidian (cask) — best effort
  if brew list --cask obsidian >/dev/null 2>&1; then ok "obsidian"; else
    info "installing obsidian (cask)"; brew install --cask obsidian || warn "could not install Obsidian cask — install it from https://obsidian.md"
  fi
fi

# ===========================================================================
# 2. OpenJDK symlink (macOS) — the load-bearing step that makes the GUI app
#    find Java. Needs sudo. See wiki/.obsidian/plantuml/README.md.
# ===========================================================================
if [[ "$IS_MAC" -eq 1 ]]; then
  info "OpenJDK symlink (so the Obsidian GUI can find Java)"
  if [[ -e /Library/Java/JavaVirtualMachines/openjdk.jdk ]]; then
    ok "symlink already present"
  elif have brew && [[ -d "$(brew --prefix)/opt/openjdk/libexec/openjdk.jdk" ]]; then
    info "creating symlink (sudo)"
    sudo ln -sfn "$(brew --prefix)/opt/openjdk/libexec/openjdk.jdk" /Library/Java/JavaVirtualMachines/openjdk.jdk \
      && ok "symlink created" || warn "symlink failed — see wiki/.obsidian/plantuml/README.md"
  else
    warn "OpenJDK not found via brew — skipping symlink. Install OpenJDK first."
  fi
fi

# ===========================================================================
# 3. mermaid-cli (optional — only for headless diagram verification)
# ===========================================================================
if [[ "$SKIP_MERMAID" -eq 1 ]]; then
  info "mermaid-cli — skipped (--skip-mermaid)"
elif have mmdc; then
  info "mermaid-cli"; ok "mmdc present"
elif have npm; then
  info "mermaid-cli"; info "installing @mermaid-js/mermaid-cli (npm -g)"
  npm install -g @mermaid-js/mermaid-cli && ok "mmdc installed" || warn "mmdc install failed (non-fatal)"
else
  warn "npm not found — skipping mermaid-cli (install Node to enable headless Mermaid checks)"
fi

# ===========================================================================
# 4. PlantUML JAR (GPLv3) — download to the path data.json already points at
# ===========================================================================
info "PlantUML JAR"
if [[ -f "$JAR" ]]; then
  ok "already present ($(du -h "$JAR" | cut -f1))"
else
  mkdir -p "$(dirname "$JAR")"
  have curl || die "curl is required to download the PlantUML JAR"
  info "resolving latest PlantUML release"
  LATEST="$(curl -fsSL "https://api.github.com/repos/${PLANTUML_REPO}/releases/latest" \
            | grep -m1 '"tag_name"' | sed -E 's/.*"tag_name": *"([^"]+)".*/\1/')"
  [[ -n "$LATEST" ]] || die "could not resolve latest PlantUML release (GitHub API rate limit? try again, or download manually per wiki/.obsidian/plantuml/README.md)"
  URL="https://github.com/${PLANTUML_REPO}/releases/download/${LATEST}/plantuml-${LATEST#v}.jar"
  info "downloading $URL"
  curl -fSL --progress-bar -o "$JAR" "$URL" \
    && ok "PlantUML $LATEST -> $JAR ($(du -h "$JAR" | cut -f1))" \
    || die "JAR download failed — see wiki/.obsidian/plantuml/README.md"
fi

# ===========================================================================
# 5. Community plugins — fetch release assets into the vault's plugins dir.
#    (Obsidian's own "manual install" method: drop main.js/manifest.json/
#    styles.css into <vault>/.obsidian/plugins/<id>/.)
# ===========================================================================
install_plugin() {
  local id="$1" repo="$2" dir="$PLUGINS_DIR/$1"
  if [[ -f "$dir/main.js" && -f "$dir/manifest.json" ]]; then ok "$id already installed"; return; fi
  info "installing plugin $id (from $repo latest release)"
  mkdir -p "$dir"
  local base="https://github.com/${repo}/releases/latest/download"
  curl -fSL -o "$dir/manifest.json" "$base/manifest.json" || { warn "$id: manifest.json download failed"; return; }
  curl -fSL -o "$dir/main.js"       "$base/main.js"       || { warn "$id: main.js download failed"; return; }
  # styles.css is optional — not every plugin ships one
  curl -fsSL -o "$dir/styles.css"   "$base/styles.css" 2>/dev/null && : || true
  ok "$id installed"
}
if [[ "$SKIP_PLUGINS" -eq 1 ]]; then
  info "Community plugins — skipped (--skip-plugins)"
else
  info "Community plugins"
  have curl || die "curl is required to download plugins"
  install_plugin "obsidian-plantuml" "$PLUGIN_PLANTUML_REPO"
  install_plugin "smart-connections" "$PLUGIN_SMART_REPO"
fi

# ===========================================================================
# 6. Verify + next steps
# ===========================================================================
info "Verification"
rc=0
for t in java dot; do have "$t" && ok "$t" || { miss "$t missing"; rc=1; }; done
have mmdc && ok "mmdc" || skip "mmdc (optional)"
[[ -f "$JAR" ]] && ok "PlantUML JAR" || { miss "PlantUML JAR"; rc=1; }
for id in obsidian-plantuml smart-connections; do
  [[ -f "$PLUGINS_DIR/$id/main.js" ]] && ok "plugin $id" || { miss "plugin $id"; rc=1; }
done

cat <<EOF

${BOLD}Next steps (one-time, in the Obsidian GUI):${RESET}
  1. Open the vault:        ${DIM}open -a Obsidian wiki/${RESET}   (vault root is wiki/, NOT the repo root)
  2. Settings -> Community plugins -> turn OFF Restricted Mode (trust author).
  3. Enable ${BOLD}PlantUML${RESET} and ${BOLD}Smart Connections${RESET} (already listed in community-plugins.json).
  4. Fully quit and reopen Obsidian so the PlantUML plugin picks up the local JAR.
  5. Open any page with a PlantUML ArchiMate block — it should render with no spinner.

If diagrams don't render, see ${DIM}wiki/.obsidian/plantuml/README.md${RESET} (Java symlink / troubleshooting).
EOF

[[ "$rc" -eq 0 ]] && info "${GREEN}Setup complete.${RESET}" || warn "Setup finished with missing items above — see notes."
exit "$rc"
