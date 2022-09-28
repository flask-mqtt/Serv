$VENV_PATH= $PSScriptRoot+'\_venv'
$TRUE_FALSE= (Test-Path $VENV_PATH)
$createvenv= $true
if($TRUE_FALSE -ne "True")
{
    python -m venv _venv
}
_venv/scripts/activate.ps1 
python main.py