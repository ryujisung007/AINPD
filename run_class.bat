@echo off
title AINPD 교육앱 - 수업 실행
setlocal EnableDelayedExpansion

echo ============================================================
echo   AINPD 교육앱 실행 준비
echo ============================================================
echo.
echo   [실습자에게 알려줄 주소]
echo.

set "FOUND="
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set "IP=%%b"
        rem 169.254 는 주소 할당 실패값이라 접속에 쓸 수 없다
        echo !IP! | findstr /b "169.254." > nul
        if errorlevel 1 (
            set "FOUND=1"
            echo     [실습자 - 크롤링 실습만]  http://!IP!:8501/?m=crawl
            echo     [강사  - 전체 화면    ]  http://!IP!:8501
            echo.
        )
    )
)

if not defined FOUND (
    echo     [!] 사용할 수 있는 IP 주소를 찾지 못했습니다.
    echo         유선랜이 연결돼 있는지 확인하세요.
    echo.
)

echo   실습자는 위 crawl 주소로 들어가면 로그인 없이
echo   온라인 시장분석 실습 화면만 바로 열립니다.
echo.
echo ------------------------------------------------------------
echo   창을 닫으면 수업이 끊깁니다. 수업이 끝날 때까지 두세요.
echo ------------------------------------------------------------
echo.

python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

pause
