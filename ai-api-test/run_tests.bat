@echo off
chcp 65001 >nul
title AI Code Platform - API Test

echo ============================================
echo   AI Code Platform -  API Test
echo ============================================
echo.
echo Prerequisites:
echo   1. Make sure project is running (http://localhost:8123)
echo   2. Make sure MySQL and Redis are started
echo.
echo Press any key to start testing...
pause >nul

cd /d "%~dp0"

echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Running tests...
pytest testcases/ -v --html=reports/report.html --self-contained-html

echo.
if %errorlevel% equ 0 (
    echo ============================================
    echo   All tests passed!
    echo   Report: reports/report.html
    echo ============================================
    start reportseport.html
) else (
    echo ============================================
    echo   Tests completed (some failed)
    echo   Report: reports/report.html
    echo ============================================
    start reportseport.html
)

pause
