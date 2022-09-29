
$JsonContent = Get-Content -Encoding "UTF8" -Path $PSScriptRoot"\config\config.json" -Raw | ConvertFrom-Json 
$APP_NAME = $JsonContent.APP_NAME

$VENV_PATH= $PSScriptRoot+"\_venv"
$TRUE_FALSE= (Test-Path $VENV_PATH)
$createvenv= $true
if($TRUE_FALSE -ne "True")
{
    python -m venv _venv
}

$VENV_PATH= $PSScriptRoot+"\_venv"
$TRUE_FALSE= (Test-Path $VENV_PATH)
$createvenv= $true
if($TRUE_FALSE -eq "True")
{
    Copy-Item -Path $VENV_PATH'\scripts\'python.exe -Destination $VENV_PATH'\scripts\'$APP_NAME""_python.exe
}
_venv/scripts/activate.ps1 
$s = $APP_NAME+"_python.exe main.py"
Invoke-Expression $s