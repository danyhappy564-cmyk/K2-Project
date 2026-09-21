param([string]$Editor = 'D:\SPT Dev\02_Resources\Toolchain\Unity2022.3.43f1\Editor\Unity.exe')
$ErrorActionPreference = 'Stop'
if (!(Test-Path -LiteralPath $Editor)) { throw "Unity Editor가 없습니다: $Editor" }
$inputMesh = Join-Path $PSScriptRoot 'Assets-Local/UnityInput/k2c3-visual.json'
if (!(Test-Path -LiteralPath $inputMesh)) { throw 'Blender/export_visual.py를 먼저 실행하세요.' }
$artifacts = Join-Path $PSScriptRoot 'Artifacts'
New-Item -ItemType Directory -Path $artifacts -Force | Out-Null
$log = Join-Path $artifacts ('unity-build-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.log')
$project = Join-Path $PSScriptRoot 'Unity'
$build = Start-Process -FilePath $Editor -ArgumentList "-batchmode -nographics -quit -projectPath `"$project`" -executeMethod BuildK2Visual.Build -logFile `"$log`"" -WindowStyle Hidden -PassThru -Wait
if ($build.ExitCode -ne 0) { throw "Unity 빌드 실패. 로그: $log" }
if (!(Select-String -LiteralPath $log -SimpleMatch 'K2_VISUAL_BUILD_OK' -Quiet)) { throw "빌드 완료 표식이 없습니다: $log" }
$env:APPDATA = Join-Path (Split-Path $PSScriptRoot -Parent) '02_Resources/Toolchain/BuildAppData'
dotnet build (Join-Path $PSScriptRoot 'Client/K2.Visual.csproj') -c Release --configfile (Join-Path $PSScriptRoot 'NuGet.Config') -v minimal
if ($LASTEXITCODE -ne 0) { throw '클라이언트 빌드 실패' }
dotnet build (Join-Path $PSScriptRoot 'Server/K2.Server.csproj') -c Release --configfile (Join-Path $PSScriptRoot 'NuGet.Config') -v minimal
if ($LASTEXITCODE -ne 0) { throw '서버 빌드 실패' }
Write-Output '외형 번들과 클라이언트 DLL 생성 완료. 게임 검증은 별도입니다.'
