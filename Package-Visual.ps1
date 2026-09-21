$ErrorActionPreference = 'Stop'
$workspace = Split-Path $PSScriptRoot -Parent
$bundle = Join-Path $PSScriptRoot 'Artifacts/VisualBundle/k2c3_visual.bundle'
$client = Join-Path $PSScriptRoot 'Client/bin/Release/netstandard2.1/K2.Visual.dll'
$server = Join-Path $PSScriptRoot 'Server/bin/Release/net10.0/K2.Server.dll'
foreach ($file in @($bundle,$client,$server)) {
    if (!(Test-Path -LiteralPath $file)) { throw "필수 파일 없음: $file" }
}
if ((Get-Item -LiteralPath $bundle).Length -lt 1000000) { throw '외형 번들 크기가 비정상입니다.' }
$name = 'K2C3-Visual-Test-0.2.0-SPT-4.1.6'
$releaseRoot = Join-Path $workspace '03_Releases'
$release = Join-Path $releaseRoot $name
$zip = "$release.zip"
if ((Test-Path -LiteralPath $release) -or (Test-Path -LiteralPath $zip)) {
    $backup = Join-Path $workspace ('02_Resources/Backups/K2C3-Visual-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
    New-Item -ItemType Directory -Path $backup | Out-Null
    foreach ($path in @($release,$zip)) {
        if (Test-Path -LiteralPath $path) {
            $resolved = (Resolve-Path -LiteralPath $path).Path
            if (!$resolved.StartsWith($releaseRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw '백업 경로 오류' }
            Move-Item -LiteralPath $resolved -Destination $backup
        }
    }
}
$pluginDir = Join-Path $release 'BepInEx/plugins/K2-Project'
$serverDir = Join-Path $release 'SPT_Runtime/user/mods/K2-Project'
New-Item -ItemType Directory -Path $pluginDir,$serverDir -Force | Out-Null
Copy-Item -LiteralPath $bundle,$client -Destination $pluginDir
Copy-Item -LiteralPath $server -Destination $serverDir
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Server/data') -Destination $serverDir -Recurse
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'VISUAL_TEST_KO.md') -Destination (Join-Path $release '읽어주세요.md')
Compress-Archive -LiteralPath (Join-Path $release 'BepInEx'),(Join-Path $release 'SPT_Runtime'),(Join-Path $release '읽어주세요.md') -DestinationPath $zip
Write-Output $zip
