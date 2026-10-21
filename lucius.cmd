@echo off
rem Lucius — zaganjalnik iz katerekoli lupine (repo root).
rem Uporaba:  lucius.cmd            (pogovor)
rem           lucius.cmd "Pozdrav"  (enkratno vprašanje)
rem           lucius.cmd --glas "Pozdrav"  (tudi izgovorjeno)
node "%~dp0lucius\lucius.mjs" %*
