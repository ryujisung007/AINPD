@echo off
title AINPD 교육앱 - 강사PC 준비
echo ============================================================
echo   AINPD 교육앱 - 강사 PC 준비 (최초 1회만)
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python이 없습니다.
    echo     https://www.python.org/downloads/ 에서 설치하세요.
    echo     설치 화면에서 "Add Python to PATH" 를 반드시 체크하세요.
    pause
    exit /b 1
)
echo [1/4] Python 확인 완료
python --version
echo.

echo [2/4] 필요한 패키지를 설치합니다. (2~3분)
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [X] 패키지 설치 실패. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
)
echo     완료
echo.

echo [3/4] 크롤링용 브라우저를 내려받습니다. (5~10분, 약 200MB)
python -m playwright install chromium
if errorlevel 1 (
    echo [!] 브라우저 설치에 실패했습니다.
    echo     크롤링 실행 기능만 꺼지고 나머지 수업은 정상 진행됩니다.
) else (
    echo     완료
)
echo.

echo [4/4] 실습자가 접속할 수 있도록 방화벽을 엽니다. (8501 포트)
netsh advfirewall firewall delete rule name="AINPD 교육앱" > nul 2>&1
netsh advfirewall firewall add rule name="AINPD 교육앱" dir=in action=allow protocol=TCP localport=8501 > nul 2>&1
if errorlevel 1 (
    echo [!] 방화벽 규칙을 넣지 못했습니다. 관리자 권한이 없는 PC입니다.
    echo     실습자가 접속되지 않으면 이 파일을 마우스 오른쪽 클릭 후
    echo     "관리자 권한으로 실행" 으로 다시 한 번 돌려주세요.
) else (
    echo     완료
)
echo.

if not exist ".streamlit\secrets.toml" (
    echo ============================================================
    echo [!] .streamlit\secrets.toml 파일이 없습니다.
    echo     접속 코드 기본값 kfi2026 으로 로그인됩니다.
    echo     ^(웹앱 관리자 현황판에서 받은 설치 패키지에는 들어 있습니다^)
    echo ============================================================
) else (
    echo [OK] secrets.toml 확인됨
)
echo.
echo ------------------------------------------------------------
echo   준비 완료. 수업 때는 run_class.bat 을 실행하세요.
echo   수업이 끝나고 이 PC에서 지울 때는 삭제하기.bat 을 실행하세요.
echo ------------------------------------------------------------
pause
