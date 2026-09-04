@echo off
title AINPD 교육앱 - 설치본 완전 삭제

set "TGT=%~dp0"
if "%TGT:~-1%"=="\" set "TGT=%TGT:~0,-1%"

echo ============================================================
echo   AINPD 교육앱 설치본을 완전히 삭제합니다
echo ============================================================
echo.
echo   삭제할 폴더
echo     %TGT%
echo.
echo   접속 코드가 들어 있는 설정 파일까지 전부 지워집니다.
echo   내려받은 크롤링용 브라우저는 지워지지 않습니다.
echo   남겨두면 다음 수업에서 설치 시간이 줄어듭니다.
echo.

if /i "%~1"=="/y" goto confirmed

set "OK="
set /p OK=삭제하려면 Y 를 누르고 엔터:
if /i not "%OK%"=="Y" (
    echo.
    echo   취소했습니다.
    ping -n 3 127.0.0.1 > nul
    exit /b
)

:confirmed
echo.
echo [1/2] 실행 중인 교육앱을 종료합니다...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*streamlit*' -and $_.CommandLine -like '*app.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" > nul 2>&1

echo [2/2] 폴더를 삭제합니다...
echo.
echo   이 창은 곧 닫힙니다. 잠시 후 폴더가 사라집니다.

start "" /d "%TEMP%" /min powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 4; Remove-Item -LiteralPath '%TGT%' -Recurse -Force -ErrorAction SilentlyContinue"

ping -n 3 127.0.0.1 > nul
exit
