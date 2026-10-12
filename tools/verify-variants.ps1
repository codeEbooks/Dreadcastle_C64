param(
    [string]$Python = '',
    [string]$Assembler = '',
    [string]$Vice = ''
)
# Dreadcastle, the chain of the book: build every guided
# variant and every "where it breaks" of variants/ from chain/
# (tools/variants.py) and prove them in VICE (tools/make_variants.py
# --test): a variant must pass the test of its step with the model
# changed in the same way, a break must be stopped by the test of its
# step and is photographed. 64tass, x64sc and python are looked for on
# the PATH; -Assembler, -Vice and -Python give their full paths.
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
$complete = Join-Path $root 'game/build/dreadcastle.lbl'
if (!(Test-Path -LiteralPath $complete)) {
    # Every test takes the numbers of the game from the labels of
    # the complete game: it is built first, at the root.
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'tools/run-game.ps1') `
        -Mode Build -Python $Python -Assembler $Assembler
    if ($LASTEXITCODE -ne 0) { throw 'The complete game could not be built.' }
}
Push-Location $root
try {
    & $Python 'tools/make_variants.py' --test --assembler $Assembler --vice $Vice
    if ($LASTEXITCODE -ne 0) { throw 'A variant or a break is not proved: see variants/variants.json.' }
} finally {
    Pop-Location
}
