$repoRoot = Split-Path -Path $PSScriptRoot -Parent
Set-Location -Path $repoRoot
. "$repoRoot\pytorch_env\Scripts\Activate.ps1"
Set-Location -Path (Join-Path -Path $repoRoot -ChildPath '2D_optical_vision_mapping')
jupyter notebook