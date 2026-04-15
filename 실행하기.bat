@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ================================
echo  BSN 홈페이지 리뉴얼 실행
echo ================================
echo.
python redesign.py
echo.
pause
