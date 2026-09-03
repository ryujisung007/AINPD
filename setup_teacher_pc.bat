@echo off
chcp 65001 > nul
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
echo [1/3] Python 확인 완료
python --version
echo.

echo [2/3] 필요한 패키지를 설치합니다. (2~3분)
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [X] 패키지 설치 실패. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
)
echo     완료
echo.

echo [3/3] 크롤링용 브라우저를 내려받습니다. (5~10분, 약 200MB)
python -m playwright install chromium
if errorlevel 1 (
    echo [!] 브라우저 설치에 실패했습니다.
    echo     크롤링 실행 기능만 꺼지고 나머지 수업은 정상 진행됩니다.
) else (
    echo     완료
)
echo.

if not exist ".streamlit\secrets.toml" (
    echo ============================================================
    echo [!] .streamlit\secrets.toml 파일이 없습니다.
    echo     이 파일에는 접속코드와 API 키가 들어 있어 GitHub에 올라가지 않습니다.
    echo     USB 등으로 가져와 .streamlit 폴더에 넣어주세요.
    echo ============================================================
) else (
    echo [OK] secrets.toml 확인됨
)
echo.
echo 준비가 끝났습니다. 수업 때는 run_class.bat 을 실행하세요.
pause
