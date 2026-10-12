param(
    [Parameter(Mandatory=$true)][int]$Step,
    [string]$Python = '',
    [string]$Assembler = '',
    [string]$Vice = ''
)
# Dreadcastle, the chain of the book: build step $Step in its
# folder (chain/NN-name, its tools/run-game.ps1 -Mode Build) and verify
# it in VICE with tests/verify_game.py --step $Step (13: the complete
# game, from the project's folder). The report and the captures go to
# chain/evidence/NN-name/ (13: evidence/). 64tass, x64sc and python are
# looked for on the PATH; -Assembler, -Vice and -Python give their
# full paths instead.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$env:PYTHONDONTWRITEBYTECODE = '1'

function Find-Tool([string]$Given, [string[]]$Names, [string]$Switch) {
    if ($Given) {
        if (!(Test-Path -LiteralPath $Given)) { throw "Not found: $Given" }
        return $Given
    }
    foreach ($name in $Names) {
        $found = Get-Command $name -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($found) { return $found.Source }
    }
    throw "$($Names[0]) is not on the PATH: add its folder to the PATH, or give its full path with $Switch."
}

$Python = Find-Tool $Python @('python', 'python3', 'py') '-Python'
$Assembler = Find-Tool $Assembler @('64tass') '-Assembler'
$Vice = Find-Tool $Vice @('x64sc') '-Vice'
if ($Step -lt 1 -or $Step -gt 13) { throw 'Steps 1-13.' }
$complete = Join-Path $root 'game/build/dreadcastle.lbl'
if ($Step -ne 13 -and !(Test-Path -LiteralPath $complete)) {
    # Every test takes the numbers of the game from the labels of
    # the complete game: it is built first, at the root.
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'tools/run-game.ps1') `
        -Mode Build -Python $Python -Assembler $Assembler
    if ($LASTEXITCODE -ne 0) { throw 'The complete game could not be built.' }
}
if ($Step -eq 13) {
    $folder = Get-Item -LiteralPath $root
} else {
    $folder = Get-ChildItem -LiteralPath (Join-Path $root 'chain') -Directory -Filter ('{0:D2}-*' -f $Step) |
        Select-Object -First 1
    if (!$folder) { throw "Step $Step is not in chain/." }
}
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $folder.FullName 'tools/run-game.ps1') `
    -Mode Build -Python $Python -Assembler $Assembler
if ($LASTEXITCODE -ne 0) { throw "Step $Step could not be built." }
Push-Location $root
try {
    & $Python 'tests/verify_game.py' --step $Step --vice $Vice
    if ($LASTEXITCODE -ne 0) { throw "The test of step $Step failed." }
} finally {
    Pop-Location
}
