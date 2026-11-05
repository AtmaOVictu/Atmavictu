@echo off
rem Izgradi Atma.exe (Node SEA) — samostojni Book Workbench CLI, brez nameščenega Node.
rem Rezultat: Atma.exe v korenu repa (v git ne sodi).
rem Atma.exe je tanki exe po kroju Lucius.exe: Node runtime nosi v sebi,
rem ukazno logiko pa bere iz build\src\atmaCli.js zraven sebe —
rem zato build\ potuje zraven exeta (kakor lucius\ potuje z Lucius.exe).
setlocal
cd /d "%~dp0"

node --experimental-sea-config sea-config.json || goto :napaka

powershell -NoProfile -Command "Copy-Item (Get-Command node).Source '..\Atma.tmp' -Force" || goto :napaka

call npx --yes postject "..\Atma.tmp" NODE_SEA_BLOB "atma.blob" --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2 || goto :napaka

if exist "..\Atma.exe" del "..\Atma.exe"
move /y "..\Atma.tmp" "..\Atma.exe" >nul || goto :napaka

echo Atma.exe zgrajen v korenu repa. Zraven mora stati build\ (npm run typecheck ali npm test ga zgradita).
goto :konec

:napaka
echo Izgradnja ni uspela.
exit /b 1

:konec
endlocal
