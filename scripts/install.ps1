[CmdletBinding()]
param(
    [string]$DshHome = (Join-Path ([Environment]::GetFolderPath('UserProfile')) '.dsh'),
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$skillsRoot = Join-Path $DshHome 'skills'
$target = Join-Path $skillsRoot 'xhs-chaijie-dsh'
$targetFull = [System.IO.Path]::GetFullPath($target)
$sourcePrefix = $source.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

if ($targetFull.StartsWith($sourcePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Install target cannot be inside the source repository: $targetFull"
}

if (Test-Path -LiteralPath $target) {
    if (-not $Force) {
        throw "Target already exists: $target. Re-run with -Force only after reviewing the existing directory."
    }
    $backup = "$target.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Move-Item -LiteralPath $target -Destination $backup
    Write-Host "Existing installation moved to: $backup"
}

New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Recurse
Write-Host "Installed xhs-chaijie-dsh to: $target"
Write-Host "Restart DSH or start a new session so it rescans skills."
