# Installer Windows (TIDAK DIUJI di Windows dari sesi ini). Memanggil scripts/install_skills.py.
# Dry-run default. Tambahkan -Apply untuk menyalin.
# Contoh: powershell -ExecutionPolicy Bypass -File scripts\install_windows.ps1 -Target "$env:USERPROFILE\.claude\skills" -Apply
param(
  [string]$Target = "$env:USERPROFILE\.claude\skills",
  [switch]$Apply,
  [switch]$Force
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { Write-Error "Python 3.9+ tidak ditemukan di PATH"; exit 2 }
$args = @("$here\install_skills.py", "--target", $Target)
if ($Apply) { $args += "--apply" }
if ($Force) { $args += "--force" }
& $py.Source @args
exit $LASTEXITCODE
