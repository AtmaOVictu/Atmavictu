@echo off
rem Izgradi Atma-debeli.exe (Node SEA, vse v enem) — debeli brat tankega.
rem Bundel (atma-bundle.mjs, zgrajen z esbuild) je vgrajen v exe kot sea asset:
rem ob zagonu ne bere nic z diska razen uporabniskih podatkov (projectRoot).
rem Rezultat: Atma-debeli.exe v korenu repa (v git ne sodi).
rem Tanka pot (Atma.exe + build\) ostane kot druga roka / varovalka.
setlocal
cd /d "%~dp0"

call node zgradi-bundel.cjs || goto :napaka
node --experimental-sea-config sea-debeli-config.json || goto :napaka

powershell -NoProfile -Command "Copy-Item (Get-Command node).Source '..\Atma-debeli.tmp' -Force" || goto :napaka

call npx --yes postject "..\Atma-debeli.tmp" NODE_SEA_BLOB "atma-debeli.blob" --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2 || goto :napaka

if exist "..\Atma-debeli.exe" del "..\Atma-debeli.exe"
move /y "..\Atma-debeli.tmp" "..\Atma-debeli.exe" >nul || goto :napaka

echo Atma-debeli.exe zgrajen v korenu repa. Nic zraven mu ni treba — vse nosi v sebi.
goto :konec

:napaka
echo Izgradnja debelega ni uspela.
exit /b 1

:konec
endlocal
