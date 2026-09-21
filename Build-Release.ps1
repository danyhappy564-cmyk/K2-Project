$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'Build-Visual.ps1')
& (Join-Path $PSScriptRoot 'Package-Visual.ps1')
