$ErrorActionPreference = 'Stop'
$workspace = Split-Path $PSScriptRoot -Parent
$env:APPDATA = Join-Path $workspace '02_Resources/Toolchain/BuildAppData'
dotnet restore (Join-Path $PSScriptRoot 'Server/K2.Server.csproj') --configfile (Join-Path $PSScriptRoot 'NuGet.Config') -v minimal
if ($LASTEXITCODE -ne 0) { throw '복원 실패' }
dotnet build (Join-Path $PSScriptRoot 'Server/K2.Server.csproj') -c Release --no-restore -v minimal
if ($LASTEXITCODE -ne 0) { throw '빌드 실패' }
$name = 'K2-Prototype-0.1.0-SPT-4.1.5'
$release = Join-Path $workspace "03_Releases/$name"
$zip = "$release.zip"
if ((Test-Path $release) -or (Test-Path $zip)) {
    $backup = Join-Path $workspace ('02_Resources/Backups/K2-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
    New-Item -ItemType Directory -Path $backup | Out-Null
    foreach ($target in @($release, $zip)) {
        if (Test-Path -LiteralPath $target) {
            $resolved = (Resolve-Path -LiteralPath $target).Path
            if (!$resolved.StartsWith((Join-Path $workspace '03_Releases') + '\', [StringComparison]::OrdinalIgnoreCase)) { throw '백업 경로 오류' }
            Move-Item -LiteralPath $resolved -Destination $backup
        }
    }
}
$mod = Join-Path $release 'SPT_Runtime/user/mods/K2-Project'
New-Item -ItemType Directory -Path $mod -Force | Out-Null
Copy-Item (Join-Path $PSScriptRoot 'Server/bin/Release/net10.0/K2.Server.dll') $mod
Copy-Item (Join-Path $PSScriptRoot 'Server/data') $mod -Recurse
Copy-Item (Join-Path $PSScriptRoot 'INSTALL_KO.md') $mod
Compress-Archive -LiteralPath (Join-Path $release 'SPT_Runtime') -DestinationPath $zip
Write-Output $zip
