param(
    [Parameter(Mandatory)][string]$ServerExe,
    [Parameter(Mandatory)][string]$ConfigPath,
    [ValidateRange(1,65535)][int]$Port = 8080
)
$ErrorActionPreference = 'Stop'
$server = (Resolve-Path -LiteralPath $ServerExe).Path
$config = (Resolve-Path -LiteralPath $ConfigPath).Path
if (-not (Test-Path -LiteralPath $server -PathType Leaf)) { throw 'No se encuentra llama-server.' }
if (-not (Test-Path -LiteralPath $config -PathType Leaf)) { throw 'No se encuentra el INI.' }
& $server --models-preset $config --models-max 1 --host 127.0.0.1 --port $Port
if ($LASTEXITCODE -ne 0) { throw "llama-server terminó con código $LASTEXITCODE." }
