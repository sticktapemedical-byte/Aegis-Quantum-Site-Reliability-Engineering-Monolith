$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
python .\aegis_monitor.py --host 127.0.0.1 --port 8765

