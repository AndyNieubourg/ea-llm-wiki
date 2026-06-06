<#
.SYNOPSIS
  Local setup for the EA LLM Wiki foundation (Windows / PowerShell).

.DESCRIPTION
  Installs the prerequisites the wiki needs but does NOT commit (third-party
  tools under their own licenses): the PlantUML JAR (GPLv3) and the
  obsidian-plantuml / Smart Connections community plugins. The repo ships only
  its own Obsidian config, so once these land the committed settings apply.

  Uses winget for prerequisites. Safe to re-run: every step checks before acting.

.PARAMETER Check
  Report what's present/missing and install nothing.
.PARAMETER SkipWinget
  Don't touch winget packages (you manage them).
.PARAMETER SkipPlugins
  Skip the two community-plugin downloads.
.PARAMETER SkipMermaid
  Skip mermaid-cli (only needed for headless diagram checks in Claude Code).

.EXAMPLE
  .\setup.ps1 --check
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\setup.ps1
#>
param(
  [switch]$Check,
  [switch]$SkipWinget,
  [switch]$SkipPlugins,
  [switch]$SkipMermaid,
  [switch]$Help
)

# Accept GNU-style flags too (--check etc.), so usage matches setup.sh
foreach ($a in $args) {
  switch ($a) {
    '--check'        { $Check = $true }
    '--skip-winget'  { $SkipWinget = $true }
    '--skip-plugins' { $SkipPlugins = $true }
    '--skip-mermaid' { $SkipMermaid = $true }
    '-h'             { $Help = $true }
    '--help'         { $Help = $true }
  }
}
if ($Help) { Get-Help $PSCommandPath -Detailed; exit 0 }

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# --- third-party sources (each under its own license; not redistributed) ---
$PlantumlRepo      = 'plantuml/plantuml'                       # GPLv3 distribution
$PluginPlantumlRepo = 'joethei/obsidian-plantuml'
$PluginSmartRepo    = 'brianpetro/obsidian-smart-connections'

# winget package IDs
$WingetPkgs = [ordered]@{
  'Git.Git'                       = 'git'
  'GitHub.cli'                    = 'gh'
  'EclipseAdoptium.Temurin.21.JDK' = 'OpenJDK (Temurin 21)'
  'Graphviz.Graphviz'             = 'graphviz'
  'OpenJS.NodeJS'                 = 'node'
  'Obsidian.Obsidian'            = 'obsidian'
}

# --- logging ---
function Info($m) { Write-Host "==> $m" -ForegroundColor White }
function Ok($m)   { Write-Host "  ok   $m" -ForegroundColor Green }
function Warn($m) { Write-Host "  warn $m" -ForegroundColor Yellow }
function Miss($m) { Write-Host "  miss $m" -ForegroundColor Red }
function Skip($m) { Write-Host "  skip $m" -ForegroundColor DarkGray }
function Die($m)  { Write-Host "error: $m" -ForegroundColor Red; exit 1 }
function Have($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

function Refresh-Path {
  $machine = [Environment]::GetEnvironmentVariable('Path','Machine')
  $user    = [Environment]::GetEnvironmentVariable('Path','User')
  $env:Path = ($machine, $user | Where-Object { $_ }) -join ';'
}

# --- locate repo root (this script lives at the repo root) ---
$RepoRoot = $PSScriptRoot
Set-Location $RepoRoot
$Obs = Join-Path $RepoRoot 'wiki\.obsidian'
if (-not (Test-Path $Obs)) { Die "expected $Obs - run this from the repo root (where CLAUDE.md lives)." }
$Jar        = Join-Path $Obs 'plantuml\plantuml.jar'
$PluginsDir = Join-Path $Obs 'plugins'

# ===========================================================================
# CHECK MODE
# ===========================================================================
if ($Check) {
  Info 'Status check (no changes will be made)'
  foreach ($t in 'winget','git','gh','java','dot','node','mmdc') {
    if (Have $t) { Ok $t } else { Miss "$t not on PATH" }
  }
  if (Test-Path $Jar) { Ok ("PlantUML JAR present ({0:N0} MB)" -f ((Get-Item $Jar).Length/1MB)) }
  else { Miss "PlantUML JAR missing ($Jar)" }
  foreach ($id in 'obsidian-plantuml','smart-connections') {
    $d = Join-Path $PluginsDir $id
    if ((Test-Path "$d\main.js") -and (Test-Path "$d\manifest.json")) { Ok "plugin $id installed" }
    else { Miss "plugin $id not installed" }
  }
  exit 0
}

# ===========================================================================
# 1. winget prerequisites
# ===========================================================================
if ($SkipWinget) {
  Info 'winget packages - skipped (--skip-winget)'
} elseif (-not (Have 'winget')) {
  Warn 'winget not found. Install "App Installer" from the Microsoft Store, or'
  Warn 'install git, gh, a JDK, Graphviz and Node manually, then use --skip-winget.'
} else {
  Info 'winget packages'
  foreach ($id in $WingetPkgs.Keys) {
    $name = $WingetPkgs[$id]
    winget list --id $id -e --accept-source-agreements *> $null
    if ($LASTEXITCODE -eq 0) { Ok $name; continue }
    Info "installing $name"
    winget install --id $id -e --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { Warn "$name install returned $LASTEXITCODE (continuing)" }
  }
  Refresh-Path
}

# ===========================================================================
# 2. Ensure java + dot are on PATH (Graphviz silent installs often skip this)
# ===========================================================================
Info 'PATH check for java + dot'
if (-not (Have 'dot')) {
  $gvBin = 'C:\Program Files\Graphviz\bin'
  if (Test-Path "$gvBin\dot.exe") {
    $userPath = [Environment]::GetEnvironmentVariable('Path','User')
    if ($userPath -notlike "*$gvBin*") {
      [Environment]::SetEnvironmentVariable('Path', "$userPath;$gvBin", 'User')
      Info "added $gvBin to your user PATH (new terminals will see it)"
    }
    Refresh-Path
  }
}
if (Have 'java') { Ok 'java on PATH' } else { Warn 'java not on PATH yet - open a NEW terminal after install, or set JAVA_HOME/PATH' }
if (Have 'dot')  { Ok 'dot on PATH' }  else { Warn 'dot (Graphviz) not on PATH yet - open a NEW terminal, or add C:\Program Files\Graphviz\bin' }

# ===========================================================================
# 3. mermaid-cli (optional - only for headless diagram verification)
# ===========================================================================
if ($SkipMermaid) {
  Info 'mermaid-cli - skipped (--skip-mermaid)'
} elseif (Have 'mmdc') {
  Info 'mermaid-cli'; Ok 'mmdc present'
} elseif (Have 'npm') {
  Info 'mermaid-cli'; Info 'installing @mermaid-js/mermaid-cli (npm -g)'
  npm install -g '@mermaid-js/mermaid-cli'
  if ($LASTEXITCODE -eq 0) { Refresh-Path; Ok 'mmdc installed' } else { Warn 'mmdc install failed (non-fatal)' }
} else {
  Warn 'npm not found - skipping mermaid-cli (install Node to enable headless Mermaid checks)'
}

# ===========================================================================
# 4. PlantUML JAR (GPLv3) - download to the path data.json already points at
# ===========================================================================
Info 'PlantUML JAR'
if (Test-Path $Jar) {
  Ok ("already present ({0:N0} MB)" -f ((Get-Item $Jar).Length/1MB))
} else {
  New-Item -ItemType Directory -Force -Path (Split-Path $Jar) | Out-Null
  Info 'resolving latest PlantUML release'
  try {
    $rel = Invoke-RestMethod "https://api.github.com/repos/$PlantumlRepo/releases/latest" -UseBasicParsing -Headers @{ 'User-Agent' = 'ea-llm-wiki-setup' }
  } catch { Die "could not query GitHub API ($($_.Exception.Message)). Try again or download manually per wiki\.obsidian\plantuml\README.md" }
  $tag = $rel.tag_name
  if (-not $tag) { Die 'could not resolve latest PlantUML release tag' }
  $ver = $tag.TrimStart('v')
  $url = "https://github.com/$PlantumlRepo/releases/download/$tag/plantuml-$ver.jar"
  Info "downloading $url"
  try {
    Invoke-WebRequest $url -OutFile $Jar -UseBasicParsing
    Ok ("PlantUML $tag -> $Jar ({0:N0} MB)" -f ((Get-Item $Jar).Length/1MB))
  } catch { Die "JAR download failed ($($_.Exception.Message)) - see wiki\.obsidian\plantuml\README.md" }
}

# ===========================================================================
# 5. Community plugins - fetch release assets into the vault's plugins dir
# ===========================================================================
function Install-Plugin($id, $repo) {
  $dir = Join-Path $PluginsDir $id
  if ((Test-Path "$dir\main.js") -and (Test-Path "$dir\manifest.json")) { Ok "$id already installed"; return }
  Info "installing plugin $id (from $repo latest release)"
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $base = "https://github.com/$repo/releases/latest/download"
  try {
    Invoke-WebRequest "$base/manifest.json" -OutFile "$dir\manifest.json" -UseBasicParsing
    Invoke-WebRequest "$base/main.js"       -OutFile "$dir\main.js"       -UseBasicParsing
  } catch { Warn "$id: download failed ($($_.Exception.Message))"; return }
  try { Invoke-WebRequest "$base/styles.css" -OutFile "$dir\styles.css" -UseBasicParsing } catch { }  # optional
  Ok "$id installed"
}
if ($SkipPlugins) {
  Info 'Community plugins - skipped (--skip-plugins)'
} else {
  Info 'Community plugins'
  Install-Plugin 'obsidian-plantuml' $PluginPlantumlRepo
  Install-Plugin 'smart-connections' $PluginSmartRepo
}

# ===========================================================================
# 6. Verify + next steps
# ===========================================================================
Info 'Verification'
$rc = 0
foreach ($t in 'java','dot') { if (Have $t) { Ok $t } else { Miss "$t missing (new terminal may be needed)"; $rc = 1 } }
if (Have 'mmdc') { Ok 'mmdc' } else { Skip 'mmdc (optional)' }
if (Test-Path $Jar) { Ok 'PlantUML JAR' } else { Miss 'PlantUML JAR'; $rc = 1 }
foreach ($id in 'obsidian-plantuml','smart-connections') {
  if (Test-Path (Join-Path $PluginsDir "$id\main.js")) { Ok "plugin $id" } else { Miss "plugin $id"; $rc = 1 }
}

Write-Host ''
Write-Host 'Next steps (one-time, in the Obsidian GUI):' -ForegroundColor White
Write-Host '  1. Open the vault:  Obsidian -> Open folder as vault -> select the wiki\ folder (NOT the repo root).'
Write-Host '  2. Settings -> Community plugins -> turn OFF Restricted Mode (trust author).'
Write-Host '  3. Enable PlantUML and Smart Connections (already listed in community-plugins.json).'
Write-Host '  4. Fully quit and reopen Obsidian so the PlantUML plugin picks up the local JAR.'
Write-Host '  5. Open any page with a PlantUML ArchiMate block - it should render with no spinner.'
Write-Host ''
Write-Host 'If java/dot were just installed, open a NEW terminal so PATH refreshes before re-checking.' -ForegroundColor DarkGray
Write-Host 'Diagram troubleshooting: wiki\.obsidian\plantuml\README.md' -ForegroundColor DarkGray

if ($rc -eq 0) { Info 'Setup complete.' } else { Warn 'Setup finished with missing items above - see notes.' }
exit $rc
