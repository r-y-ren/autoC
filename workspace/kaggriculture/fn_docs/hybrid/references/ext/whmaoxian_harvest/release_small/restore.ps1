$ErrorActionPreference = 'Stop'
$backupBase = $PSScriptRoot
$backupInfo = Get-Content -LiteralPath (Join-Path $backupBase 'archive_info.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$backupOutput = Join-Path $backupBase $backupInfo.name
if ($backupInfo.assets.Count -gt 1) {
  if (Test-Path -LiteralPath $backupOutput) { throw 'Output ZIP already exists; verify it before replacing.' }
  foreach ($backupPart in $backupInfo.assets) {
    $backupPartPath = Join-Path $backupBase $backupPart.name
    $backupHash = (Get-FileHash -LiteralPath $backupPartPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($backupHash -ne $backupPart.sha256) { throw ('SHA256 mismatch: ' + $backupPart.name) }
  }
  $backupDestination = [IO.File]::Create($backupOutput)
  try { foreach ($backupPart in $backupInfo.assets) {
    $backupInput = [IO.File]::OpenRead((Join-Path $backupBase $backupPart.name))
    try { $backupInput.CopyTo($backupDestination) } finally { $backupInput.Dispose() }
  } } finally { $backupDestination.Dispose() }
}
$backupHash = (Get-FileHash -LiteralPath $backupOutput -Algorithm SHA256).Hash.ToLowerInvariant()
if ($backupHash -ne $backupInfo.sha256) { throw 'Complete ZIP SHA256 mismatch.' }
Write-Host ('Verified complete ZIP: ' + $backupOutput)
