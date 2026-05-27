# AEGIS Runbook

## Start The Monitor

From this repository folder:

`python aegis_monitor.py --host 127.0.0.1 --port 8765`

Open:

`http://127.0.0.1:8765`

## Start The Terminal Simulation

`python aegis_os.py`

Reviewer mode:

`python aegis_os.py --reviewer-mode`

## Expected Outputs

The monitor creates JSON artifacts in:

`monitor_snapshots/`

The terminal runner writes report files in the repository folder unless a different output path is passed.

## Useful Checks

Health endpoint:

`http://127.0.0.1:8765/api/health`

Current data endpoint:

`http://127.0.0.1:8765/api/data?cycles=1000&seed=2026`

Live tick endpoint:

`http://127.0.0.1:8765/api/live?seed=2026`

