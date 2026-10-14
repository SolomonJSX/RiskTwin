@echo off
chcp 65001 > nul
title RiskTwin Restart
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" restart
pause
