@echo off
chcp 65001 >nul
echo ========================================================
echo RiskTwin • Word Documents Generator (АБРК & ГКБ 2026)
echo ========================================================
.\src\document-generator\.venv\Scripts\python.exe src\document-generator\main.py
echo.
pause
