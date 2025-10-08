# Fail fast
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Activeer venv als die bestaat (stil falen als niet)
$venv = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venv) { . $venv }

# Build naar 'site' (standaard van referflow)
python -m referflow.cli build

# Vervang /docs door nieuwe build
if (Test-Path .\docs) { Remove-Item -Recurse -Force .\docs }
Rename-Item -Path .\site -NewName docs

Write-Host "OK → Build staat in /docs. GitHub Pages pakt dit automatisch op."
