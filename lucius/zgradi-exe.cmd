@echo off
rem Izgradi Lucius.exe (Node SEA) — brezplačno, povsem lokalno.
rem Rezultat: Lucius.exe v korenu repa (v git ne sodi).
setlocal
cd /d "%~dp0"

node --experimental-sea-config sea-config.json || goto :napaka

powershell -NoProfile -Command "Copy-Item (Get-Command node).Source '..\Lucius.tmp' -Force" || goto :napaka

call npx --yes postject "..\Lucius.tmp" NODE_SEA_BLOB "lucius.blob" --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2 || goto :napaka

if exist "..\Lucius.exe" del "..\Lucius.exe"
move /y "..\Lucius.tmp" "..\Lucius.exe" >nul || goto :napaka

echo Lucius.exe zgrajen v korenu repa.
goto :konec

:napaka
echo Izgradnja ni uspela.
exit /b 1

:konec
endlocal
