# PlantUML local rendering

This folder ships the PlantUML JAR used by the `obsidian-plantuml` plugin to render diagrams locally (no public-server round-trip).

## Contents

- `plantuml.jar` — PlantUML **v1.2026.5** (full GPL distribution; ~28 MB). Source: [plantuml/plantuml@v1.2026.5](https://github.com/plantuml/plantuml/releases/tag/v1.2026.5).

The plugin's `data.json` points `localJar` at `.obsidian/plantuml/plantuml.jar` (relative to the vault root).

## System prerequisites

There are **two consumers** of this toolchain, and they need slightly different things:

1. **The Obsidian GUI plugin** — renders PlantUML locally inside the running app.
2. **Headless CLI verification** — how a `claude/*` worktree session checks a diagram renders (Method A in the root `CLAUDE.md` "Visual verification" section). This also covers **Mermaid**, which the GUI renders natively but the CLI does not.

### Who needs what

| Tool | Install | GUI plugin (PlantUML) | Headless PlantUML | Headless Mermaid |
|---|---|:---:|:---:|:---:|
| **Java (OpenJDK)** | `brew install openjdk` **+ JDK symlink** | required | required | — |
| **GraphViz** (`dot`) | `brew install graphviz` | required¹ | required¹ | — |
| **mermaid-cli** (`mmdc`) | `npm install -g @mermaid-js/mermaid-cli` (needs Node/npm) | — | — | required |
| **PlantUML JAR** | bundled in this folder — no install | required | required | — |

¹ GraphViz renders most diagram types (ArchiMate, class, ER, etc.). Only plain sequence diagrams skip it. Obsidian renders Mermaid natively, so the **GUI needs nothing** for Mermaid.

### Install (macOS, one shot)

```bash
brew install openjdk graphviz
npm install -g @mermaid-js/mermaid-cli
# OpenJDK is keg-only; this symlink makes the system Java picker (/usr/bin/java)
# find it — which fixes BOTH the GUI app AND the shell in one step:
sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
```

> [!important] The JDK symlink is the load-bearing step
> The Obsidian GUI app does **not** inherit your shell `PATH`, so a `~/.zshrc` PATH export (`export PATH="$(brew --prefix)/opt/openjdk/bin:$PATH"`) makes `java` work in the *shell* only — not in the plugin. The `sudo ln -sfn …` symlink above is what makes the GUI find Java, and because `/usr/bin/java` then resolves too, it also covers the shell. **Do the symlink.** The PATH export is an optional shell-only alternative, redundant once the symlink is in place.

### Verify

```bash
java -version    # OpenJDK version (works in shell once the symlink or PATH export is set)
dot -V           # GraphViz version
mmdc --version   # mermaid-cli version
```

If all three print a version, restart Obsidian — the plugin picks up the local JAR automatically. If `data.json` still shows `"localJar": ""` after restart, see **Troubleshooting** below.

## Fallback

The plugin keeps `server_url` set to `https://www.plantuml.com/plantuml`. When `localJar` is configured *and* Java/GraphViz are available, local rendering is used. If anything in the local chain fails, the plugin falls back to the public server.

## Troubleshooting — plugin blanked `localJar`

If `data.json` shows `"localJar": ""` (the committed value is `.obsidian/plantuml/plantuml.jar`), the plugin cleared it because it could not execute Java at load time — typically because OpenJDK is installed keg-only and the JDK symlink (above) was missing, so the GUI app's Java picker found nothing. Fix Java first (the `sudo ln -sfn …` symlink, then `java -version` must work), restore the setting, and restart Obsidian:

```bash
git -C "<main checkout>" restore wiki/.obsidian/plugins/obsidian-plantuml/data.json
```

Note the GUI app does **not** inherit your shell `PATH`, so a `~/.zshrc` PATH export alone is not enough for the plugin — the system-wide `/Library/Java/JavaVirtualMachines/openjdk.jdk` symlink is what makes the GUI find Java.

## Headless rendering (CLI) — for diagram verification

Independent of the Obsidian GUI plugin, the same JAR renders from the command line, which is how a `claude/*` worktree session verifies a diagram renders (Method A in the root `CLAUDE.md` "Visual verification" section — concurrency-safe, no live vault):

```bash
java -jar wiki/.obsidian/plantuml/plantuml.jar -tpng /tmp/diagram.puml   # PlantUML
mmdc -i /tmp/diagram.mmd -o /tmp/diagram-check.png                       # Mermaid (mermaid-cli)
```

Both tools (`mmdc`, and `java` + `dot` for the JAR) come from the **System prerequisites** above.

## Updating

When a new PlantUML release lands:

```bash
LATEST=$(gh api repos/plantuml/plantuml/releases/latest -q '.tag_name')
curl -sSL -o wiki/.obsidian/plantuml/plantuml.jar \
  "https://github.com/plantuml/plantuml/releases/download/${LATEST}/plantuml-${LATEST#v}.jar"
```

Then update this README's version line and commit both.
