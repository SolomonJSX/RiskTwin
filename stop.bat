@echo off
chcp 65001 > nul
title RiskTwin Stop
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" stop
pause
