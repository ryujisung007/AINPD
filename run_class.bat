@echo off
chcp 65001 > nul
title AINPD 교육앱 - 수업 실행
echo ============================================================
echo   AINPD 교육앱 실행 중...
echo ============================================================
echo.
echo [수강생에게 알려줄 주소]
echo.
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do echo     http://%%b:8501
)
echo.
echo   (여러 개가 보이면 192.168 로 시작하는 주소를 알려주세요)
echo   접속코드는 secrets.toml 의 ACCESS_CODE 값입니다.
echo.
echo ------------------------------------------------------------
echo   창을 닫으면 수업이 끊깁니다. 수업 끝날 때까지 두세요.
echo ------------------------------------------------------------
echo.

python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

pause
