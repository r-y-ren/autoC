$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
    & '.\.venv\Scripts\python.exe' league_round8.py `
        --candidate experiments/round8_top2_dsm_contract_entry.py `
        --opponents submissions/release_v6/main.py submissions/release_v7/main.py external/orderbook.py external/round8/master2965/main.py experiments/round8_top2_dsm_strict.py external/round8/fieldcraft/main.py `
        --split confirmation --workers 6 `
        --output results/round8_dsm_contract_entry_confirmation.json `
        >> results/round8_dsm_contract_entry_confirmation.log 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Confirmation runner exited with code $LASTEXITCODE; saved JSONL records remain reusable." }
    Write-Output 'Confirmation finished. Review the frozen protocol, then run assess_round8.py --phase confirmation. No source or release was promoted.'
}
finally {
    Pop-Location
}
