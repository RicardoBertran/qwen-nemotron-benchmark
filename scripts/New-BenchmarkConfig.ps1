param(
    [Parameter(Mandatory)][string]$QwenModel,
    [Parameter(Mandatory)][string]$QwenDraft,
    [Parameter(Mandatory)][string]$NemotronModel,
    [Parameter(Mandatory)][string]$NemotronDraft,
    [string]$OutputPath = './results/local/models.ini'
)
$ErrorActionPreference = 'Stop'
$templatePath = Join-Path $PSScriptRoot '../configs/models.template.ini'
$content = Get-Content -LiteralPath $templatePath -Raw
$replacements = @{
    'PEGA_AQUI_LA_RUTA_QWEN_MTP' = $QwenDraft
    'PEGA_AQUI_LA_RUTA_NEMOTRON_MTP' = $NemotronDraft
    'PEGA_AQUI_LA_RUTA_QWEN' = $QwenModel
    'PEGA_AQUI_LA_RUTA_NEMOTRON' = $NemotronModel
}
foreach ($key in ($replacements.Keys | Sort-Object Length -Descending)) {
    $resolved = (Resolve-Path -LiteralPath $replacements[$key]).Path
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) { throw 'Se requiere un archivo GGUF.' }
    $content = $content.Replace($key, $resolved.Replace('\','/'))
}
$destination = [IO.Path]::GetFullPath($OutputPath)
New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
[IO.File]::WriteAllText($destination, $content, [Text.UTF8Encoding]::new($false))
Write-Output "Configuración creada: $destination"
