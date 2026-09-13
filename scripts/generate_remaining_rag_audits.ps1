$ErrorActionPreference = 'Stop'
python (Join-Path (Get-Location).Path 'scripts/generate_remaining_rag_audits.py')
if ($LASTEXITCODE -ne 0) { throw 'audit generator failed' }
