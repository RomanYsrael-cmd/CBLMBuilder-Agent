$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$fillScript = Join-Path $scriptDir "fill_cblm.py"

if (Test-Path $venvPython) {
    $pythonCmd = $venvPython
} else {
    $pythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
}

if (-not $pythonCmd) {
    Write-Error "No Python interpreter found. Expected $venvPython or a working 'python' on PATH."
}

& $pythonCmd $fillScript @args
exit $LASTEXITCODE
