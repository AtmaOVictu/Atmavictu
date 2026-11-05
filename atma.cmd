@echo off
rem Atma — zaganjalnik Book Workbench CLI iz katerekoli lupine (repo root).
rem Uporaba:  atma.cmd walk <projectRoot> <title> <body> <fragmentBody> <target>
rem           atma.cmd verify <projectRoot>
rem Zahteva zgrajen build\ (npm test ali npm run typecheck).
node "%~dp0build\src\atmaCli.js" %*
