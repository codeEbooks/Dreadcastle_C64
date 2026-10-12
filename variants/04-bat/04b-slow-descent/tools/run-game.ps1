param(
    [ValidateSet('Build','Play','Verify','Record','Disk')][string]$Mode = 'Play',
    [ValidateSet('6581','8580')][string]$Model = '6581',
    [string]$Python = '',
    [string]$Assembler = '',
    [string]$Vice = ''
)
# Dreadcastle: build the program and run it in VICE. The same script
# is in every folder of the book's package that holds a program: the
# complete game (the root), each step of chain/ and each variant of
# variants/. Run it from anywhere:
#   Build   write the data (game/assets/build_assets.py), check that
#           no line of the sources is longer than 60 characters
#           (tools/check_lines.py) and assemble with 64tass into
#           game/build: dreadcastle.prg, .lst and .lbl;
#   Play    build, then start the program in VICE (x64sc): a PAL C64
#           with the SID chosen by -Model, joystick 2 on the keypad
#           (4 left, 6 right, 8 jump, 0 fire);
#   Disk    build, make the disk game/build/dreadcastle.d64
#           (tools/make_disk.py, with VICE's c1541), then start VICE
#           with it on a 1541 (true drive emulation, at the real
#           speed: about two minutes of loading), LOAD"*",8,1 and RUN
#           typed by VICE's autostart, as on a C64; in the complete
#           game and in chain/13-complete;
#   Verify  build, then run the test (tests/verify_game.py), the
#           check that every level can be finished (tests/levels.py,
#           about twenty-five minutes) and the disk: its loading from
#           a 1541, measured, then RUN (tools/load_time.py); in the
#           complete game only;
#   Record  build, then record from the SID of VICE, 6581 and 8580,
#           in real time (tools/record_music.py): the theme, Tom's
#           theme (dreadcastle-boss.prg, assembled with
#           -D RECORD_SONG=1), the three jingles (RECORD_SONG=2, 3, 4)
#           and the sound effects (RECORD_SFX=1); about six minutes;
#           WAV files and reports in evidence/; in the complete game
#           only.
# A mode that needs a file this folder has not says so and stops.
# 64tass, x64sc and python are looked for on the PATH; -Assembler,
# -Vice and -Python give their full paths instead.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$env:PYTHONDONTWRITEBYTECODE = '1'      # no __pycache__ folders

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

$needs = @{
    'Disk' = @('tools/make_disk.py');
    'Verify' = @('tests/verify_game.py', 'tests/levels.py', 'tools/load_time.py');
    'Record' = @('tools/record_music.py')
}
if ($needs.ContainsKey($Mode)) {
    foreach ($file in $needs[$Mode]) {
        if (!(Test-Path -LiteralPath (Join-Path $root $file))) {
            $where = 'the complete game, at the root of the package'
            if ($Mode -eq 'Disk') { $where += ', and in chain/13-complete' }
            throw "-Mode $Mode needs $file, which is not in this folder: it works in $where."
        }
    }
}

$Python = Find-Tool $Python @('python', 'python3', 'py') '-Python'
$Assembler = Find-Tool $Assembler @('64tass') '-Assembler'
if ($Mode -ne 'Build') { $Vice = Find-Tool $Vice @('x64sc') '-Vice' }
Push-Location $root
try {
    New-Item -ItemType Directory -Force -Path 'game/build' | Out-Null
    if ($Mode -eq 'Verify' -or $Mode -eq 'Record') {
        New-Item -ItemType Directory -Force -Path 'evidence' | Out-Null
    }
    & $Python 'game/assets/build_assets.py'
    if ($LASTEXITCODE -ne 0) { throw 'The data of game/assets could not be built: see the message above.' }
    & $Python 'tools/check_lines.py'
    if ($LASTEXITCODE -ne 0) { throw 'A line of the sources is longer than 60 characters.' }
    & $Assembler --cbm-prg -Wall -Werror --vice-labels-numeric -l game/build/dreadcastle.lbl -L game/build/dreadcastle.lst -o game/build/dreadcastle.prg game/src/main.asm
    if ($LASTEXITCODE -ne 0) { throw '64tass stopped: its message names the file and the line.' }
    if ($Mode -eq 'Play') {
        $engine = @{ '6581' = '256'; '8580' = '257' }[$Model]
        $arguments = @('-default','-pal','-sound','-sidenginemodel',$engine,'+VICIIvcache',
            '-autostartprgmode','1','-joydev2','1','-autostart','game/build/dreadcastle.prg')
        Start-Process -FilePath $Vice -ArgumentList $arguments -WorkingDirectory $root
    } elseif ($Mode -eq 'Verify') {
        & $Python 'tests/verify_game.py' --vice $Vice
        if ($LASTEXITCODE -ne 0) { throw 'The test failed: see evidence/game-test.json.' }
        & $Python 'tests/levels.py'
        if ($LASTEXITCODE -ne 0) { throw 'The level check failed: see evidence/levels-check.json.' }
        & $Python 'tools/load_time.py' --vice $Vice
        if ($LASTEXITCODE -ne 0) { throw 'The disk did not load or start: see evidence/load-time.json.' }
    } elseif ($Mode -eq 'Disk') {
        & $Python 'tools/make_disk.py' --vice $Vice
        if ($LASTEXITCODE -ne 0) { throw 'The disk could not be made: see the message above.' }
        $engine = @{ '6581' = '256'; '8580' = '257' }[$Model]
        $arguments = @('-default','-pal','-sound','-sidenginemodel',$engine,'+VICIIvcache',
            '-drive8type','1541','-drive8truedrive','+autostart-warp',
            '-joydev2','1','-autostart','game/build/dreadcastle.d64')
        Start-Process -FilePath $Vice -ArgumentList $arguments -WorkingDirectory $root
    } elseif ($Mode -eq 'Record') {
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_SONG=1 -o game/build/dreadcastle-boss.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of Tom''s theme.' }
        # the three jingles (songs 2-4) and the sound effects
        $number = 2
        foreach ($jingle in 'clear', 'won', 'dawn') {
            & $Assembler --cbm-prg -Wall -Werror -D RECORD_SONG=$number -o "game/build/dreadcastle-$jingle.prg" game/src/main.asm
            if ($LASTEXITCODE -ne 0) { throw "64tass stopped on the program for the recording of the jingle $jingle." }
            $number += 1
        }
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_SFX=1 -o game/build/dreadcastle-sfx.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the sound effects.' }
        foreach ($song in 'theme', 'boss', 'clear', 'won', 'dawn', 'sfx') {
            foreach ($chip in '6581', '8580') {
                & $Python 'tools/record_music.py' --vice $Vice --model $chip --song $song
                if ($LASTEXITCODE -ne 0) { throw "The recording failed ($song, $chip): see evidence/." }
            }
        }
    }
} finally {
    Pop-Location
}
