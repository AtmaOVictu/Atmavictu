@echo off
rem Atma besede — zelene besede, kjer so zelene in potrebne.
rem Uporaba: atma\besede.cmd seznam
rem          atma\besede.cmd dodaj <kje> <kaj> [zakaj]
node "%~dp0besede.cjs" %*
