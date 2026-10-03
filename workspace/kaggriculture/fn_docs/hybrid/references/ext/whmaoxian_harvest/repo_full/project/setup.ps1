$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
uv venv --python 3.12 .venv
if ($LASTEXITCODE -ne 0) { throw 'Could not create environment' }
# Kaggriculture requires only the core dependencies; other bundled games have
# large ML dependencies that are intentionally not installed on this machine.
uv pip install --python .venv/Scripts/python.exe --no-deps -r requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw 'Could not install dependencies' }
.venv/Scripts/python.exe -m unittest -v test_agent
if ($LASTEXITCODE -ne 0) { throw 'Agent checks failed' }
