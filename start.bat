@echo off
chcp 65001 > nul
title RiskTwin Launcher
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" start
pause
