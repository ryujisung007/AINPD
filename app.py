# app.py (v7.0) - AI 제품개발 실습교안
"""
구조:
- 사이드바: 목차 네비게이션
- 각 섹션: ① 과제 설명 → ② 탭(예시 스크립트 | 직접 작성) → ③ Claude API 실행 결과
"""

import streamlit as st
import anthropic
import os
import random
import json
import re
import pandas as pd

# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="AI 제품개발 실습교안",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. 스타일
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px;
    padding: 4px 0;
}

/* 헤더 배너 */
.page-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f5132 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    color: white;
}
.page-banner h1 {
    font-size: 26px;
    font-weight: 900;
    margin: 0 0 6px 0;
    color: white;
}
.page-banner p {
    font-size: 14px;
    opacity: 0.85;
    margin: 0;
    color: #d1fae5;
}

/* 과제 설명 카드 */
.mission-box {
    background: #f0f9ff;
    border-left: 5px solid #0ea5e9;
    border-radius: 0 12px 12px 0;
    padding: 20px 24px;
    margin-bottom: 24px;
}
.mission-box h3 {
    color: #0369a1;
    font-size: 15px;
    font-weight: 700;
    margin: 0 0 10px 0;
}
.mission-box ul {
    margin: 0;
    padding-left: 18px;
    color: #374151;
    font-size: 14px;
    line-height: 1.8;
}

/* 공통 사례 안내 박스 */
.common-case-box {
    background: #eef2ff;
    border: 1.5px solid #a5b4fc;
    border-left: 5px solid #4f46e5;
    border-radius: 0 12px 12px 0;
    padding: 16px 22px;
    margin: 0 0 20px 0;
    font-size: 13.5px;
    color: #312e81;
    line-height: 1.75;
}
.common-case-box b { color: #3730a3; }

/* 내 제품으로 옮기기 (전이 과제) */
.transfer-box {
    background: #fffbeb;
    border: 1.5px solid #fbbf24;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
    font-size: 13.5px;
    color: #78350f;
    line-height: 1.7;
}
.transfer-box b { color: #92400e; }

/* 실습 진행 스텝바 */
.step-flow {
    display: flex;
    align-items: flex-start;
    margin: 0 0 12px 0;
    padding: 14px 8px 10px 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow-x: auto;
}
.step-flow .sf-item {
    flex: 1 1 0;
    min-width: 88px;
    text-align: center;
    position: relative;
}
.step-flow .sf-item::before {
    content: "";
    position: absolute;
    top: 12px; left: -50%; width: 100%; height: 2px;
    background: #cbd5e1; z-index: 0;
}
.step-flow .sf-item:first-child::before { display: none; }
.step-flow .sf-dot {
    position: relative; z-index: 1;
    display: inline-flex; align-items: center; justify-content: center;
    width: 26px; height: 26px; border-radius: 50%;
    font-size: 12px; font-weight: 700;
    background: #ffffff; border: 2px solid #cbd5e1; color: #94a3b8;
}
.step-flow .sf-label {
    display: block; margin-top: 6px;
    font-size: 11.5px; color: #94a3b8; line-height: 1.35;
}
.step-flow .done .sf-dot   { background: #0ea5e9; border-color: #0ea5e9; color: #fff; }
.step-flow .done .sf-label { color: #64748b; }
.step-flow .now .sf-dot    { background: #0f5132; border-color: #0f5132; color: #fff;
                             box-shadow: 0 0 0 4px rgba(15,81,50,0.15); }
.step-flow .now .sf-label  { color: #0f5132; font-weight: 800; }

/* 단계 안내 카드 */
.step-guide {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #0f5132;
    border-radius: 0 12px 12px 0;
    padding: 14px 20px;
    margin: 0 0 20px 0;
}
.step-guide .sg-row {
    font-size: 13.5px; color: #334155; line-height: 1.7; margin: 0 0 2px 0;
}
.step-guide .sg-row b { color: #0f5132; }
.step-guide .sg-time {
    display: inline-block; margin-top: 8px;
    background: #ecfdf5; color: #047857;
    border-radius: 999px; padding: 3px 14px;
    font-size: 12px; font-weight: 700;
}

/* 예시 스크립트 박스 */
.example-box {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px 28px;
    font-size: 15px;
    line-height: 2.0;
    color: #1f2937;
    white-space: pre-wrap;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 결과 박스 */
.result-box {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 12px;
    padding: 20px 24px;
    font-size: 14px;
    line-height: 1.85;
    color: #14532d;
    white-space: pre-wrap;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 버튼 커스텀 */
.stButton > button {
    background: linear-gradient(135deg, #1e3a5f, #0f5132);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 15px;
    padding: 12px 24px;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* 섹션 구분선 */
.section-divider {
    border: none;
    border-top: 2px solid #e5e7eb;
    margin: 28px 0;
}

/* 태그 뱃지 */
.badge {
    display: inline-block;
    background: #dbeafe;
    color: #1e40af;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 6px;
    margin-bottom: 6px;
}
.badge-green {
    background: #dcfce7;
    color: #166534;
}
.badge-orange {
    background: #ffedd5;
    color: #9a3412;
}

/* 선택 힌트 */
.hint-text {
    font-size: 12px;
    color: #6b7280;
    margin-top: -10px;
    margin-bottom: 12px;
}

/* Mad-lib 완성 문장 */
.ml-box {
    background: #f0fdf4;
    border: 2px solid #86efac;
    border-radius: 14px;
    padding: 24px 32px;
    font-size: 18px;
    line-height: 2.4;
    color: #1e293b;
    margin: 12px 0 20px 0;
}
.ml-filled {
    background: #fef3c7;
    border: 2px solid #f59e0b;
    border-radius: 8px;
    padding: 2px 12px;
    font-weight: 700;
    color: #92400e;
}
.ml-empty {
    background: #fff;
    border: 2px dashed #94a3b8;
    border-radius: 8px;
    padding: 2px 20px;
    color: #94a3b8;
    font-style: italic;
    font-size: 14px;
}
.ml-step {
    font-size: 13px;
    font-weight: 700;
    color: #0369a1;
    background: #e0f2fe;
    border-radius: 20px;
    padding: 3px 12px;
    display: inline-block;
    margin-bottom: 6px;
}

/* 수강생 입력 가능 필드 — 노란색 배경 */
[data-testid="stTextInput"] input {
    background-color: #fefce8 !important;
    border: 1.5px solid #fbbf24 !important;
}
[data-testid="stTextArea"] textarea {
    background-color: #fefce8 !important;
    border: 1.5px solid #fbbf24 !important;
}
[data-testid="stNumberInput"] input {
    background-color: #fefce8 !important;
    border: 1.5px solid #fbbf24 !important;
}
[data-testid="stSelectbox"] > div > div {
    background-color: #fefce8 !important;
}
[data-testid="stMultiSelect"] > div > div {
    background-color: #fefce8 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. Claude API 클라이언트
# =========================================================

def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def run_claude(prompt: str, system: str = "", max_tokens: int = 2000, model: str = "claude-sonnet-4-6") -> str:
    """Claude API 호출 - 스트리밍"""
    client = get_client()
    if not client:
        return "⚠️ API 키가 설정되지 않았습니다. secrets.toml 또는 환경변수에 ANTHROPIC_API_KEY를 추가해 주세요."
    try:
        with st.spinner("🤖 Claude가 분석 중입니다..."):
            messages = [{"role": "user", "content": prompt}]
            kwargs = {"model": model, "max_tokens": max_tokens, "messages": messages}
            if system:
                kwargs["system"] = system
            response = client.messages.create(**kwargs)
            return response.content[0].text
    except Exception as e:
        return f"❌ 오류가 발생했습니다: {str(e)}"


# 관리자 전용 더미 데이터 자동입력 버튼에서 사용 — 각 탭의 "스크립트 입력칸"·
# "AI 생성결과 붙여넣기"란에 들어갈 내용을 실제 Claude 호출로 생성한다.
_AI_DUMMY_FIELDS = {
    "r_hw_submit_ai": "연구원 페르소나가 답한 것처럼, 신제품 배합비·원료 특성에 대한 전문적인 코멘트 3~4문장",
    "m_hw_submit_ai": "마케터 페르소나가 답한 것처럼, 타깃·채널·포지셔닝 전략 코멘트 3~4문장",
    "collect_hw_submit_ai": "데이터 수집 스크립트를 실행한 AI 결과처럼, 원료 단가·경쟁사 배합 데이터 요약 4~5문장",
    "train_hw_submit_ai": "AI에게 데이터 학습을 지시한 결과처럼, 학습 반영 내용 요약 3~4문장",
    "online_user_script": "온라인 시장분석을 요청하는 사용자 프롬프트 스크립트 (분석 플랫폼·제품 카테고리·분석 항목·출력 형식 포함) 5~7문장",
    "food_user_script": "식품전문정보(원료 규제·트렌드) 분석을 요청하는 프롬프트 스크립트 5~7문장",
    "learn_user_script": "시장조사 데이터를 AI에게 학습시키는 지시 스크립트 4~6문장",
    "report_user_script": "시장분석 보고서 작성을 요청하는 스크립트 4~6문장",
    "ai_transfer_hw_submit_ai": "Gemini가 생성한 대화 맥락 요약 결과처럼, 진행상황·핵심 결과물 요약 4~5문장",
    "bev_preview": "배합비 스크립트 — 원료명과 비율을 나열한 텍스트 (정제수·당류·산미료·기능성성분 등 5개 이상 원료, 비율 합계 100%)",
    "bev_hw_submit_ai": "AI가 생성한 배합비 시트 결과에 대한 설명 3~4문장",
    "mv_note": "배합비 무결성 검증 소견 1~2문장",
    "ms2_script": "배합비 시나리오(원가절감 또는 맛 개선) 대응을 요청하는 스크립트 4~6문장",
    "bev_mission_hw_submit_ai": "미션 수행 결과 시트에 대한 AI 코멘트 2~3문장",
    "proc_step1": "시니어 연구원 페르소나 훈련 결과 코멘트 2~3문장",
    "proc_step2": "시니어 연구원 코칭 결과 코멘트 2~3문장",
    "proc_step3": "마케팅 분석 및 최종안 결과 코멘트 2~3문장",
    "twin_result": "디지털 트윈랩 실험 결과 메모 (3줄 이내)",
    "con_hw_submit_ai": "가상 소비자 모델 제작 결과 — 패널 프로필 및 평가기준 설명 4~5문장",
    "sen_result": "관능검사 결과 메모 (3줄 이내, 점수 포함)",
    "r_career_gen": "연구원 페르소나 경력 소개 1문장 (제품 컨셉과 어울리는 전문분야 포함)",
    "m_career_gen": "마케터 페르소나 경력 소개 1문장 (제품 컨셉과 어울리는 마케팅 경력 포함)",
    "ml_cat_gen": "제품 카테고리명 (제품 컨셉과 일치, 예: 저당 기능성 탄산음료)",
    "ml_theme_gen": "제품개발용 데이터 유형 설명 1문장 (제품 컨셉과 관련된 데이터, 예: 배합비 이론 및 소비자 트렌드 데이터)",
}


def _generate_ai_dummy_fields(tag: str):
    """관리자용 더미 데이터 자동입력 — 위 필드들을 실제 Claude 호출 1회로 채운다. 실패 시 None."""
    _desc = "\n".join(f'- "{k}": {v}' for k, v in _AI_DUMMY_FIELDS.items())
    prompt = (
        "음료 신제품 개발 실습 앱의 테스트용 더미 데이터를 생성해줘. "
        "제품 컨셉을 자유롭게 하나 정하고, 아래 모든 항목이 그 컨셉과 앞뒤가 맞게 작성해줘.\n"
        "각 값 맨 끝에 반드시 \"[테스트#" + tag + "]\" 표시를 붙여줘.\n\n"
        f"{_desc}\n\n"
        "다른 설명 없이, 위 키 이름을 그대로 사용한 JSON 오브젝트 하나만 출력해줘 (모든 값은 문자열)."
    )
    raw = run_claude(
        prompt,
        system="당신은 테스트 데이터 생성 도우미입니다. 반드시 유효한 JSON 객체만 출력하세요.",
        max_tokens=8000,
        model="claude-haiku-4-5-20251001",
    )
    if raw.startswith("⚠️") or raw.startswith("❌"):
        return None
    _match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not _match:
        return None
    try:
        _parsed = json.loads(_match.group(0))
    except Exception:
        return None
    return {k: str(v) for k, v in _parsed.items() if k in _AI_DUMMY_FIELDS}


# =========================================================
# 4. Google Sheets 과제 제출
# =========================================================

_GS_SHEET_ID = "1QFwS0mIt9TKl4o8kYMeNISTo0CxSHVH0s_fVdyFue38"

@st.cache_resource
def _get_gs_client():
    import gspread
    from google.oauth2.service_account import Credentials
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_dict = dict(st.secrets["gcp_service_account"])
    # TOML에서 \n이 문자 그대로 남는 경우 실제 개행으로 변환
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)


_HW_HEADERS = ["제출시간", "학생이름", "작성 스크립트", "AI 생성결과", "파일링크"]

# 앱 내 모든 과제 제출 시트 탭 목록 (섹션·탭 단위로 1:1 대응)
_ALL_HW_TABS = [
    "연구원_페르소나",   # 2️⃣ 제품개발 페르소나 > 연구원 탭
    "마케터_페르소나",   # 2️⃣ 제품개발 페르소나 > 마케터 탭
    "데이터수집스크립트",# 3️⃣ 제품개발용 데이터 > 데이터 수집 스크립트 탭
    "데이터학습지시",    # 3️⃣ 제품개발용 데이터 > AI 데이터 학습시키기 탭
    "온라인시장분석",    # 4️⃣ 시장분석 및 학습 > 온라인 시장분석 탭
    "식품전문정보분석",  # 4️⃣ 시장분석 및 학습 > 식품전문정보분석 탭
    "시장조사학습",      # 4️⃣ 시장분석 및 학습 > 시장조사 데이터 학습 탭
    "보고서작성",        # 4️⃣ 시장분석 및 학습 > 보고서 작성하기 탭
    "AI전환",            # 4️⃣ 시장분석 및 학습 > AI 간 대화전환 탭
    "배합비",            # 5️⃣ 배합비 개발 > 배합비 작성 탭
    "배합비_미션",       # 5️⃣ 배합비 개발 > 미션수행 탭
    "배합비_프로세스",   # 5️⃣ 배합비 개발 > 개발 프로세스 실습 탭
    "디지털트윈랩",      # 6️⃣ 가상모델 개발 > 디지털 트윈랩 탭
    "가상소비자모델",    # 6️⃣ 가상모델 개발 > 가상 소비자 모델 제작 탭
    "관능검사",          # 6️⃣ 가상모델 개발 > 관능검사 탭
    "프로젝트정리",      # 7️⃣ 프로젝트 정리
]

# 프롬프트 복사 영역에 자동으로 붙는 제출요약 조건
# AI가 답변 마지막에 [제출답안]: ... 을 추가 → 시트 셀에는 이 부분만 저장
# ChatGPT 영구 메모리 저장 방지 — 페르소나 프롬프트 맨 앞에 삽입
# "메모리 업데이트" 트리거 문구를 제거하고 세션 전용임을 명시
_NO_MEMORY_HEADER = (
    "⚠️ [세션 전용 설정] 아래 내용을 ChatGPT 영구 메모리(장기 기억)에 저장하지 마세요. "
    "이 대화 안에서만 임시로 적용합니다.\n\n"
)

_SUBMIT_INSTRUCTION = (
    "\n\n---\n"
    "[제출용 요약] 답변이 끝나면 아래 형태로 요약을 하나 더 붙여줘.\n"
    "코드블록으로 감싸야 복사 버튼으로 이 부분만 가져갈 수 있어.\n"
    "```\n"
    "[제출답안]\n"
    "(200~230자 요약, 한 줄 35자 이내로 줄바꿈)\n"
    "```"
)



@st.cache_resource(show_spinner=False)
def _playwright_ready() -> bool:
    """크롤링 실행이 가능한 환경인지 판별.

    Streamlit Cloud에는 playwright 브라우저 바이너리를 넣을 수 없어 실행이 안 된다.
    파이썬 패키지와 브라우저 설치 폴더가 모두 있어야 True.
    """
    try:
        import playwright  # noqa: F401
    except Exception:
        return False
    import glob
    import os
    cands = [
        os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
        os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright"),
        os.path.expanduser("~/.cache/ms-playwright"),
        os.path.expanduser("~/Library/Caches/ms-playwright"),
    ]
    for c in cands:
        if c and os.path.isdir(c) and glob.glob(os.path.join(c, "chromium*")):
            return True
    return False


_TEACHER_PKG_README = """AINPD 교육앱 - 강사PC 설치 안내

[설치 순서]
1. 이 폴더를 바탕화면 등 원하는 곳에 풀어 둡니다.
2. setup_teacher_pc.bat 을 더블클릭합니다. (최초 1회, 5~10분)
   - 파이썬 패키지와 크롤링용 브라우저를 내려받습니다.
   - "파이썬이 없습니다" 가 나오면 python.org 에서 설치하고
     설치 화면의 "Add Python to PATH" 를 반드시 체크하세요.
3. 수업 때는 run_class.bat 을 실행합니다.
   - 창을 닫으면 앱이 꺼집니다. 수업이 끝날 때까지 두세요.

[실습자는 설치하지 않습니다]
실습자는 웹앱 주소로 접속합니다.
이 설치본은 강사가 크롤링을 직접 시연하기 위한 것입니다.

[수업이 끝나면 - 공용PC라면 반드시]
삭제하기.bat 을 더블클릭하면 앱을 끄고 이 폴더를 통째로 지웁니다.
앱 안에서 지울 수도 있습니다 - 관리자 현황판 > 이 설치본 완전 삭제.
.streamlit/secrets.toml 안에 접속코드가 들어 있으니 꼭 지우세요.
"""


def _class_access_info() -> dict:
    """이 서버의 접속 주소·포트·방화벽 상태를 모은다.

    169.254.x.x(주소 할당 실패값)와 루프백은 실습자가 쓸 수 없으므로 뺀다.
    """
    import socket
    import subprocess as _sp6

    info = {"ips": [], "port": 8501, "firewall": None}

    try:
        info["port"] = int(st.get_option("server.port") or 8501)
    except Exception:                                        # noqa: BLE001
        pass

    ips = []
    try:
        for _e in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = _e[4][0]
            if ip.startswith("169.254.") or ip.startswith("127."):
                continue
            if ip not in ips:
                ips.append(ip)
    except Exception:                                        # noqa: BLE001
        pass
    if not ips:
        # 호스트명으로 안 잡히는 환경 대비 — 외부로 향하는 소켓의 로컬 주소를 본다
        try:
            _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _s.connect(("8.8.8.8", 80))
            ips = [_s.getsockname()[0]]
            _s.close()
        except Exception:                                    # noqa: BLE001
            pass
    info["ips"] = ips

    try:
        _r = _sp6.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", "name=AINPD 교육앱"],
            capture_output=True, text=True, encoding="cp949", errors="replace",
            timeout=8,
        )
        info["firewall"] = (_r.returncode == 0 and "8501" in (_r.stdout or ""))
    except Exception:                                        # noqa: BLE001
        info["firewall"] = None                              # 확인 불가(비윈도우 등)

    return info


@st.cache_data(show_spinner=False)
def _build_teacher_package(with_codes: bool, with_api: bool) -> bytes:
    """강사PC용 설치 ZIP을 메모리에서 만든다.

    저장소가 비공개라 GitHub 다운로드 링크를 쓸 수 없어,
    실행 중인 앱이 자기 파일을 묶어 준다.
    """
    import io as _io2
    import os as _os2
    import zipfile as _zf2

    def _sec(k, d=""):
        try:
            return st.secrets.get(k, d) or d
        except Exception:
            return d

    _base = _os2.path.dirname(_os2.path.abspath(__file__))
    _buf = _io2.BytesIO()
    with _zf2.ZipFile(_buf, "w", _zf2.ZIP_DEFLATED) as _z:
        for _n in ("app.py", "kurly_collect.py", "requirements.txt",
                   "setup_teacher_pc.bat", "run_class.bat", "삭제하기.bat"):
            _p = _os2.path.join(_base, _n)
            if _os2.path.isfile(_p):
                _z.write(_p, _n)

        for _folder in ("sample_data", "assets"):
            _d = _os2.path.join(_base, _folder)
            if not _os2.path.isdir(_d):
                continue
            for _root, _dirs, _files in _os2.walk(_d):
                for _f in _files:
                    _fp = _os2.path.join(_root, _f)
                    _arc = _os2.path.relpath(_fp, _base).replace(_os2.sep, "/")
                    _z.write(_fp, _arc)

        # secrets.toml — 필요한 값만 골라 담는다
        _lines = []
        if with_codes:
            _lines.append('ACCESS_CODE = "%s"' % _sec("ACCESS_CODE", "kfi2026"))
            _adm = _sec("ADMIN_CODE")
            if _adm:
                _lines.append('ADMIN_CODE = "%s"' % _adm)
        if with_api:
            _key = _sec("ANTHROPIC_API_KEY")
            if _key:
                _lines.append('ANTHROPIC_API_KEY = "%s"' % _key)
        if _lines:
            _z.writestr(".streamlit/secrets.toml", "\n".join(_lines) + "\n")

        _z.writestr("설치안내.txt", _TEACHER_PKG_README)

        # 이 표식이 있는 폴더에서만 앱에 삭제 버튼이 뜬다.
        # 개발용 원본 폴더·클라우드 배포본에는 없으므로 실수로 지울 수 없다.
        _z.writestr(".installed_package", "AINPD teacher package\n")

    return _buf.getvalue()


@st.cache_data(ttl=60, show_spinner=False)
def _get_hw_count(sheet_tab: str) -> int:
    """해당 탭의 제출 인원 수 반환 (1분 캐시)"""
    try:
        gc = _get_gs_client()
        sh = gc.open_by_key(_GS_SHEET_ID)
        ws = sh.worksheet(sheet_tab)
        names = ws.col_values(2)  # B열: 학생이름
        return max(0, len(names) - 1)  # 헤더 제외
    except Exception:
        return -1


def _submit_hw(sheet_tab: str, student: str, content: str,
               ai_result: str = "", file_link: str = ""):
    from datetime import datetime
    try:
        gc = _get_gs_client()
        sh = gc.open_by_key(_GS_SHEET_ID)
        try:
            ws = sh.worksheet(sheet_tab)
        except Exception:
            ws = sh.add_worksheet(title=sheet_tab, rows=1000, cols=5)
            ws.append_row(_HW_HEADERS)

        from datetime import timezone, timedelta
        timestamp = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")

        # 셀에는 단축 텍스트, 전체 내용은 셀 메모(마우스 오버 팝업)에 저장
        def _cell_short(text: str, n: int = 500) -> str:
            t = text.strip()
            return (t[:n] + "…") if len(t) > n else t

        content_cell = _cell_short(content)

        # AI 생성결과: [제출답안] 태그가 있으면 그 부분만, 없으면 단축
        ai_cell = ""
        if ai_result:
            _marker = "[제출답안]"
            _idx = ai_result.find(_marker)
            if _idx != -1:
                ai_cell = ai_result[_idx:].strip()
                if len(ai_cell) > 500:
                    ai_cell = ai_cell[:500] + "…"
            else:
                ai_cell = _cell_short(ai_result)

        new_row = [timestamp, student, content_cell, ai_cell, file_link]

        # 동일 학생이 이미 제출한 행이 있으면 덮어쓰기 (최종 제출만 유지)
        all_rows = ws.get_all_values()
        existing_idx = None
        for i, row in enumerate(all_rows):
            if i == 0:          # 헤더 행 건너뜀
                continue
            if len(row) >= 2 and row[1] == student:
                existing_idx = i + 1  # gspread는 1-based
                break

        if existing_idx:
            ws.update([new_row], f"A{existing_idx}:E{existing_idx}")
            target_row = existing_idx
        else:
            ws.append_row(new_row)
            target_row = len(all_rows) + 1  # 새 행 위치

        # 셀 메모(마우스 오버 팝업) + 시트 레이아웃 포맷 한 번에 처리
        _batch_reqs = []

        # ① 셀 메모에 전체 원문 저장
        if content.strip():
            _batch_reqs.append({
                "updateCells": {
                    "range": {"sheetId": ws.id,
                              "startRowIndex": target_row - 1, "endRowIndex": target_row,
                              "startColumnIndex": 2, "endColumnIndex": 3},
                    "rows": [{"values": [{"note": content.strip()}]}],
                    "fields": "note",
                }
            })
        if ai_result.strip():
            _batch_reqs.append({
                "updateCells": {
                    "range": {"sheetId": ws.id,
                              "startRowIndex": target_row - 1, "endRowIndex": target_row,
                              "startColumnIndex": 3, "endColumnIndex": 4},
                    "rows": [{"values": [{"note": ai_result.strip()}]}],
                    "fields": "note",
                }
            })

        # ② 데이터 행 전체를 한 줄 높이(21px)로 고정 + C~E 열 텍스트 잘림(CLIP)
        #    → 14명 수강생 입력을 한 화면에서 스크롤 없이 조망 가능
        _batch_reqs += [
            # 데이터 행 높이 내용에 맞게 자동 조절 (CLIP+80자라 자연히 한 줄 ~21px)
            {
                "autoResizeDimensions": {
                    "dimensions": {"sheetId": ws.id, "dimension": "ROWS",
                                   "startIndex": 1, "endIndex": 200}
                }
            },
            # A 제출시간 130px
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": ws.id, "dimension": "COLUMNS",
                              "startIndex": 0, "endIndex": 1},
                    "properties": {"pixelSize": 130},
                    "fields": "pixelSize",
                }
            },
            # B 학생이름 80px
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": ws.id, "dimension": "COLUMNS",
                              "startIndex": 1, "endIndex": 2},
                    "properties": {"pixelSize": 80},
                    "fields": "pixelSize",
                }
            },
            # C 작성스크립트 230px
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": ws.id, "dimension": "COLUMNS",
                              "startIndex": 2, "endIndex": 3},
                    "properties": {"pixelSize": 230},
                    "fields": "pixelSize",
                }
            },
            # D AI생성결과 230px
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": ws.id, "dimension": "COLUMNS",
                              "startIndex": 3, "endIndex": 4},
                    "properties": {"pixelSize": 230},
                    "fields": "pixelSize",
                }
            },
            # E 파일링크 160px
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": ws.id, "dimension": "COLUMNS",
                              "startIndex": 4, "endIndex": 5},
                    "properties": {"pixelSize": 160},
                    "fields": "pixelSize",
                }
            },
            # C~E 텍스트 넘침 CLIP (줄바꿈 없이 잘라냄)
            {
                "repeatCell": {
                    "range": {"sheetId": ws.id,
                              "startRowIndex": 1, "endRowIndex": 200,
                              "startColumnIndex": 2, "endColumnIndex": 5},
                    "cell": {"userEnteredFormat": {"wrapStrategy": "CLIP"}},
                    "fields": "userEnteredFormat.wrapStrategy",
                }
            },
        ]

        sh.batch_update({"requests": _batch_reqs})

        # D열 수식이 개별 시트 B열을 실시간 참조하므로 별도 기록 불필요

        return True, ""
    except Exception as e:
        return False, str(e)


@st.cache_data(ttl=120, show_spinner=False)
def _fetch_dashboard_data():
    """관리자 현황판 — 접속자현황 + 제출현황 2개 탭만 읽기 (API 2회, 2분 캐시)
    제출현황 C열 공식이 각 과제 탭을 실시간 참조하므로 개별 탭 조회 불필요.
    반환: (acc_rows, summary_rows)
      acc_rows    : 접속자현황 전체 (헤더 포함)
      summary_rows: 📊 제출현황 전체 (헤더 포함, C열=수식 계산값, D열~=제출자순서)
    """
    gc = _get_gs_client()
    sh = gc.open_by_key(_GS_SHEET_ID)
    try:
        acc_data = sh.worksheet("접속자현황").get_all_values()
    except Exception:
        acc_data = []
    try:
        summary_data = sh.worksheet("📊 제출현황").get_all_values()
    except Exception:
        summary_data = []
    return acc_data, summary_data


def _record_login(student: str):
    """접속자현황 탭에 학생 접속 기록 (신규면 추가, 기존이면 최근접속시간 업데이트)
    IP는 학생에게 노출되지 않는 별도 숨김 탭(_접속IP기록)에만 매 접속마다 누적 기록한다."""
    from datetime import datetime
    try:
        gc = _get_gs_client()
        sh = gc.open_by_key(_GS_SHEET_ID)
        try:
            ws = sh.worksheet("접속자현황")
        except Exception:
            ws = sh.add_worksheet(title="접속자현황", rows=200, cols=3)
            ws.append_row(["이름", "최초접속", "최근접속"])
        from datetime import timezone, timedelta
        timestamp = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")
        all_rows = ws.get_all_values()
        existing_idx = None
        for i, row in enumerate(all_rows):
            if i == 0:
                continue
            if len(row) >= 1 and row[0] == student:
                existing_idx = i + 1
                break
        if existing_idx:
            ws.update_cell(existing_idx, 3, timestamp)
        else:
            ws.append_row([student, timestamp, timestamp])

        try:
            ip = str(st.context.ip_address or "")
        except Exception:
            ip = ""
        _is_new_ip_tab = False
        try:
            ws_ip = sh.worksheet("_접속IP기록")
        except Exception:
            ws_ip = sh.add_worksheet(title="_접속IP기록", rows=1000, cols=3)
            ws_ip.append_row(["이름", "IP주소", "접속시각"])
            _is_new_ip_tab = True
        ws_ip.append_row([student, ip, timestamp])
        if _is_new_ip_tab:
            try:
                ws_ip.hide()
            except Exception:
                pass
    except Exception:
        pass


def _submit_report_nb(student: str, nb_script: str):
    """보고서작성 시트 F열(NotebookLM 슬라이드 스크립트)에 Step2 제출 — 학생 기존 행에 덮어쓰기"""
    from datetime import datetime
    try:
        gc = _get_gs_client()
        sh = gc.open_by_key(_GS_SHEET_ID)
        try:
            ws = sh.worksheet("보고서작성")
        except Exception:
            ws = sh.add_worksheet(title="보고서작성", rows=1000, cols=6)
            ws.append_row(_HW_HEADERS + ["NotebookLM 슬라이드 스크립트"])
        # 열 부족 시 확장 (일괄생성으로 cols=5로 만들어진 경우 대비)
        if ws.col_count < 6:
            ws.resize(cols=6)
        # F열 헤더 없으면 추가
        header = ws.row_values(1)
        if len(header) < 6 or not header[5].strip():
            ws.update_cell(1, 6, "NotebookLM 슬라이드 스크립트")
        # 학생 기존 행 찾기
        all_rows = ws.get_all_values()
        existing_idx = None
        for i, row in enumerate(all_rows):
            if i == 0:
                continue
            if len(row) >= 2 and row[1] == student:
                existing_idx = i + 1
                break
        nb_cell = nb_script[:500] if len(nb_script) > 500 else nb_script
        if existing_idx:
            ws.update_cell(existing_idx, 6, nb_cell)
        else:
            from datetime import timezone, timedelta
            timestamp = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")
            ws.append_row([timestamp, student, "", "", "", nb_cell])
        return True, ""
    except Exception as e:
        return False, str(e)


def _submit_process_hw(student: str, step1: str, step2: str, step3: str):
    """배합비_프로세스: STEP1·2·3 결과를 C·D·E 열에 각각 분리 저장"""
    from datetime import datetime, timezone, timedelta
    try:
        gc = _get_gs_client()
        sh = gc.open_by_key(_GS_SHEET_ID)
        try:
            ws = sh.worksheet("배합비_프로세스")
        except Exception:
            ws = sh.add_worksheet(title="배합비_프로세스", rows=1000, cols=5)
            ws.append_row(["제출일시", "이름", "STEP1 연구원훈련", "STEP2 배합비검증", "STEP3 마케터인터뷰"])
        if ws.col_count < 5:
            ws.resize(cols=5)
        header = ws.row_values(1)
        if len(header) < 5 or not header[2].strip():
            ws.update([["제출일시", "이름", "STEP1 연구원훈련", "STEP2 배합비검증", "STEP3 마케터인터뷰"]], "A1:E1")
        timestamp = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")
        all_rows = ws.get_all_values()
        existing_idx = None
        for i, row in enumerate(all_rows):
            if i == 0:
                continue
            if len(row) >= 2 and row[1] == student:
                existing_idx = i + 1
                break
        if existing_idx:
            ws.update([[step1, step2, step3]], f"C{existing_idx}:E{existing_idx}")
        else:
            ws.append_row([timestamp, student, step1, step2, step3])
        return True, ""
    except Exception as e:
        return False, str(e)


def _hw_ui(sheet_tab: str, content: str, btn_key: str,
           with_file: bool = False, show_ai_field: bool = True, ai_label: str = "AI 생성결과",
           title: str = "과제 제출", guide_type: str = "gemini"):
    """과제 제출 UI — 각 세션 하단에 공통으로 삽입"""
    st.markdown("---")
    student = st.session_state.get("student_name", "")
    if not student:
        st.warning("과제를 제출하려면 먼저 로그인하세요.")
        return
    st.markdown(f"##### 📤 {title}")
    st.caption("동일인이 재제출하면 최종 내용으로 덮어씁니다.")

    ai_result = ""
    if show_ai_field:
        st.markdown(
            '<div style="background:#f0fdf4;border:1.5px solid #86efac;border-radius:8px;'
            'padding:10px 16px 6px 16px;margin-top:8px;margin-bottom:4px;">'
            f'<span style="font-size:16px;color:#166534;font-weight:800;">📎 {ai_label}</span>'
            '<span style="font-size:12px;color:#4ade80;font-weight:500;margin-left:8px;">붙여넣기</span></div>',
            unsafe_allow_html=True,
        )
        ai_result = st.text_area(
            ai_label, key=f"{btn_key}_ai",
            placeholder=f"{ai_label}를 여기에 붙여넣으세요 (선택)",
            height=360, label_visibility="collapsed",
        )

    file_link = ""
    if with_file:
        file_link = st.text_input(
            "파일 링크 (구글드라이브 공유 링크, 선택)",
            placeholder="https://drive.google.com/...",
            key=f"{btn_key}_file",
        )
        guide_btn_label = ("🔗 GPT생성 파일 공유방법 보기(누름)" if guide_type == "gpt"
                           else "🔗 공유 설정 방법 보기")
        if st.button(guide_btn_label, key=f"{btn_key}_guide_btn",
                     use_container_width=False):
            st.session_state[f"{btn_key}_show_guide"] = not st.session_state.get(
                f"{btn_key}_show_guide", False)
        if st.session_state.get(f"{btn_key}_show_guide"):
            if guide_type == "gpt":
                _show_share_guide_gpt()
            else:
                _show_share_guide()

    col_btn, col_status = st.columns([1, 2])
    with col_btn:
        clicked = st.button("📤 과제 제출하기", key=btn_key,
                            type="primary", use_container_width=True)
    if clicked:
        ok, err = _submit_hw(sheet_tab, student, content, ai_result, file_link)
        st.session_state[f"{btn_key}_done"] = ok
        st.session_state[f"{btn_key}_err"] = err if not ok else ""
        if ok:
            _get_hw_count.clear()
    with col_status:
        if st.session_state.get(f"{btn_key}_done"):
            st.success(f"✅ **{student}** 님 제출 완료! (재제출 시 최종본으로 갱신)")
        elif st.session_state.get(f"{btn_key}_err"):
            st.error(f"제출 실패: {st.session_state[f'{btn_key}_err']}")

    count = _get_hw_count(sheet_tab)
    if count >= 0:
        st.caption(f"👥 현재 제출 인원: **{count}명**")


def _show_share_guide():
    st.markdown("""
<div style="background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:10px;
padding:16px 20px;margin:8px 0;">
<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">
📤 제미나이 → 구글 시트 내보내기 &amp; 공유 링크 설정</div>

<div style="font-size:13px;color:#334155;line-height:1.9;">

<b style="color:#0f172a;">① 제미나이에서 구글 시트로 내보내기</b><br>
&nbsp;&nbsp;• 제미나이 대화창에서 배합비(또는 결과 표) 생성 후<br>
&nbsp;&nbsp;• 표 아래 <b>점 세 개(⋮)</b> 클릭<br>
&nbsp;&nbsp;• <b>"Google Sheet로 내보내기"</b> 선택<br>
&nbsp;&nbsp;• 구글 드라이브에 자동으로 저장됩니다<br><br>

<b style="color:#0f172a;">② 공유 링크 설정 (누구나 볼 수 있게)</b><br>
&nbsp;&nbsp;• 저장된 구글 시트 파일 열기<br>
&nbsp;&nbsp;• 우측 상단 <span style="background:#e2e8f0;border-radius:4px;padding:1px 6px;font-size:12px;font-weight:600;">공유</span> 버튼 클릭<br>
&nbsp;&nbsp;• "일반 액세스" 항목 → <b>변경</b> 클릭<br>
&nbsp;&nbsp;• <b>"링크가 있는 모든 사용자"</b> 선택 → 역할: <b>뷰어</b><br>
&nbsp;&nbsp;• <span style="background:#e2e8f0;border-radius:4px;padding:1px 6px;font-size:12px;font-weight:600;">완료</span> 클릭<br><br>

<b style="color:#0f172a;">③ 링크 복사 후 과제 제출란에 붙여넣기</b><br>
&nbsp;&nbsp;• 공유 팝업 하단 <b>"링크 복사"</b> 클릭<br>
&nbsp;&nbsp;• 복사된 링크를 아래 <b>파일 링크</b> 입력칸에 붙여넣기

</div></div>""", unsafe_allow_html=True)


def _show_share_guide_gpt():
    st.markdown("""
<div style="background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:10px;
padding:16px 20px;margin:8px 0;">
<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">
📤 ChatGPT 생성 결과 파일로 공유하기</div>

<div style="font-size:13px;color:#334155;line-height:1.9;">

<b style="color:#0f172a;">① ChatGPT 결과 파일 링크 확인</b><br>
&nbsp;&nbsp;• 생성 결과가 <b>파일 링크(파일 카드)</b>로 뜨는 경우<br>
&nbsp;&nbsp;&nbsp;&nbsp;→ 해당 파일 링크를 우클릭 → <b>"링크 주소 복사"</b> 클릭 → 아래 ④번으로 이동<br>
&nbsp;&nbsp;• 파일을 <b>다운로드</b>한 경우<br>
&nbsp;&nbsp;&nbsp;&nbsp;→ 다운로드한 파일을 아래 <b>②번(구글 드라이브 업로드)</b>부터 진행<br><br>

<b style="color:#0f172a;">② 구글 드라이브에 업로드</b><br>
&nbsp;&nbsp;• (다운로드한 파일이 있는 경우) 구글 드라이브 접속 → <b>새로 만들기</b> → <b>파일 업로드</b><br>
&nbsp;&nbsp;• 다운로드한 파일 선택 후 업로드<br><br>

<b style="color:#0f172a;">③ 공유 링크 설정 (누구나 볼 수 있게)</b><br>
&nbsp;&nbsp;• 업로드한 파일 우클릭 → <span style="background:#e2e8f0;border-radius:4px;padding:1px 6px;font-size:12px;font-weight:600;">공유</span> 클릭<br>
&nbsp;&nbsp;• "일반 액세스" 항목 → <b>변경</b> 클릭<br>
&nbsp;&nbsp;• <b>"링크가 있는 모든 사용자"</b> 선택 → 역할: <b>뷰어</b><br>
&nbsp;&nbsp;• <span style="background:#e2e8f0;border-radius:4px;padding:1px 6px;font-size:12px;font-weight:600;">완료</span> 클릭<br><br>

<b style="color:#0f172a;">④ 링크 복사 후 과제 제출란에 붙여넣기</b><br>
&nbsp;&nbsp;• 공유 팝업 하단 <b>"링크 복사"</b> 클릭<br>
&nbsp;&nbsp;• 복사된 링크를 아래 <b>파일 링크</b> 입력칸에 붙여넣기

</div></div>""", unsafe_allow_html=True)


def _build_twin_html(rows: list, product_name: str) -> str:
    """디지털 트윈랩 인터랙티브 HTML/JS 파일 생성"""
    rows_json = json.dumps(rows, ensure_ascii=False)

    css = (
        "<style>\n"
        "* {box-sizing:border-box;margin:0;padding:0;font-family:'Noto Sans KR',sans-serif;}\n"
        "body {background:#f1f5f9;padding:20px;}\n"
        ".header {background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:12px;padding:20px 28px;margin-bottom:20px;}\n"
        ".header h1 {font-size:22px;font-weight:700;}\n"
        ".header p  {font-size:13px;margin-top:4px;opacity:.85;}\n"
        ".metrics {display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px;}\n"
        ".metric {background:#fff;border-radius:10px;padding:14px 16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.08);}\n"
        ".metric .label {font-size:11px;color:#64748b;margin-bottom:4px;}\n"
        ".metric .value {font-size:22px;font-weight:700;color:#1e3a5f;}\n"
        ".card {background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:20px;}\n"
        ".card h2 {font-size:15px;font-weight:700;color:#1e3a5f;margin-bottom:14px;}\n"
        "table {width:100%;border-collapse:collapse;}\n"
        "th {background:#f8fafc;color:#475569;font-size:12px;font-weight:600;padding:8px 10px;text-align:left;border-bottom:2px solid #e2e8f0;}\n"
        "td {padding:8px 10px;border-bottom:1px solid #f1f5f9;font-size:13px;vertical-align:middle;}\n"
        "td.nm {font-weight:600;color:#1e293b;min-width:100px;}\n"
        ".sw {display:flex;gap:8px;align-items:center;}\n"
        ".sw input[type=number] {width:65px;border:1px solid #cbd5e1;border-radius:6px;padding:4px 6px;font-size:13px;}\n"
        ".sw input[type=range] {flex:1;accent-color:#3b82f6;}\n"
        ".chips {display:flex;flex-wrap:wrap;gap:10px;}\n"
        ".chip {padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;transition:.2s;}\n"
        ".chip.off {background:#f1f5f9;color:#64748b;border:1.5px solid #cbd5e1;}\n"
        ".chip.on {background:#fef2f2;color:#dc2626;border:1.5px solid #fca5a5;}\n"
        ".rmsg {display:none;background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:12px 16px;"
        "font-size:13px;color:#9a3412;margin-top:12px;line-height:1.8;}\n"
        ".rmsg.show {display:block;}\n"
        ".totbar {height:8px;border-radius:4px;background:#e2e8f0;overflow:hidden;margin-top:4px;}\n"
        ".totbar-fill {height:100%;background:#3b82f6;transition:.3s;}\n"
        "</style>\n"
    )

    header = (
        "<div class='header'>\n"
        f"  <h1>🔬 디지털 트윈랩 — {product_name}</h1>\n"
        "  <p>원료 배합비율을 조정하면 이화학 지표와 원가가 실시간으로 계산됩니다.</p>\n"
        "</div>\n"
    )

    metrics = (
        "<div class='metrics'>\n"
        "  <div class='metric'><div class='label'>배합 합계</div>"
        "    <div class='value' id='mR'>—</div>"
        "    <div class='totbar'><div class='totbar-fill' id='mBar'></div></div></div>\n"
        "  <div class='metric'><div class='label'>100 ml 원가</div><div class='value' id='mC'>—</div></div>\n"
        "  <div class='metric'><div class='label'>Brix</div><div class='value' id='mB'>—</div></div>\n"
        "  <div class='metric'><div class='label'>산도</div><div class='value' id='mA'>—</div></div>\n"
        "  <div class='metric'><div class='label'>pH (추정)</div><div class='value' id='mP'>—</div></div>\n"
        "</div>\n"
    )

    table = (
        "<div class='card'>\n"
        "  <h2>📋 원료 배합표 (2 kg 기준)</h2>\n"
        "  <table><thead><tr>"
        "<th>원료명</th><th>배합비율(%) — 슬라이더</th>"
        "<th>2 kg 기준량(g)</th><th>단가(원/kg)</th>"
        "<th>Brix기여</th><th>산도기여</th><th>100ml 원가</th>"
        "</tr></thead><tbody id='tBody'></tbody></table>\n"
        "</div>\n"
    )

    _risk_data = [
        ("원가초과", "목표 원가를 초과했습니다. 단가가 높은 원료의 비율을 낮추거나 저단가 대체 원료를 검토하세요."),
        ("Brix이탈", "Brix 목표 범위(10–14 °Bx)를 벗어났습니다. 당류·농축과즙 비율을 조정하세요."),
        ("pH이탈", "pH가 목표 범위(2.8–4.5)를 벗어났습니다. 산미료·완충제 비율을 재확인하세요."),
        ("산도이탈", "총산도가 0.5% 이상입니다. 산미료 함량을 낮추거나 완충제를 추가하세요."),
        ("배합합계오류", "배합 합계가 100%가 아닙니다. 각 원료 비율의 합을 100%로 맞추세요."),
        ("기능성미달", "기능성 원료 비율이 낮습니다. 기능성 성분 함량 목표치를 재검토하세요."),
    ]
    risk_chips = "<div class='card'>\n  <h2>⚠️ 리스크 검증 항목 선택</h2>\n  <div class='chips'>\n"
    risk_msgs = ""
    for rk, rd in _risk_data:
        risk_chips += f"    <div class='chip off' id='rc_{rk}' onclick=\"toggleRisk('{rk}')\">{rk}</div>\n"
        risk_msgs += f"  <div class='rmsg' id='rm_{rk}'>⚠️ <b>{rk}</b>: {rd}</div>\n"
    risk_section = risk_chips + "  </div>\n" + risk_msgs + "</div>\n"

    js_data = f"<script>\nconst _rows = {rows_json};\n"
    js_logic = (
        "function calc(){"
        "var N=_rows.length,tot=0,totC=0,totB=0,totA=0;"
        "for(var i=0;i<N;i++){"
        "var r=parseFloat(document.getElementById('r'+i).value)||0;"
        "var p=_rows[i]['단가(원/kg)']||0;"
        "tot+=r;totC+=(r/100)*(p/1000)*100;"
        "totB+=r*(_rows[i]['Brix기여(/1%)']||0);"
        "totA+=r*(_rows[i]['산도기여(/1%)']||0);"
        "document.getElementById('amt'+i).textContent=(r/100*2000).toFixed(1);"
        "document.getElementById('cst'+i).textContent=((r/100)*(p/1000)*100).toFixed(1)+'원';}"
        "var ph=Math.max(2.0,Math.min(7.5,7.0-totA*6)).toFixed(1);"
        "var ok=Math.abs(tot-100)<0.5;"
        "var rv=document.getElementById('mR');"
        "rv.textContent=tot.toFixed(2)+'%';rv.style.color=ok?'#16a34a':'#dc2626';"
        "var bf=document.getElementById('mBar');"
        "bf.style.width=Math.min(tot,100)+'%';bf.style.background=ok?'#22c55e':'#ef4444';"
        "document.getElementById('mC').textContent=totC.toFixed(0)+'원';"
        "document.getElementById('mB').textContent=totB.toFixed(1)+' °Bx';"
        "document.getElementById('mA').textContent=totA.toFixed(3)+'%';"
        "document.getElementById('mP').textContent=ph;}\n"
        "function sync(i,src){"
        "var v=document.getElementById(src+i).value;"
        "var ot=src==='r'?'sl':'r';"
        "document.getElementById(ot+i).value=v;calc();}\n"
        "function toggleRisk(id){"
        "var chip=document.getElementById('rc_'+id);"
        "var msg=document.getElementById('rm_'+id);"
        "var on=chip.classList.toggle('on');"
        "chip.classList.toggle('off',!on);"
        "msg.classList.toggle('show',on);}\n"
        "function build(){"
        "var tb=document.getElementById('tBody');"
        "_rows.forEach(function(d,i){"
        "var r0=d['배합비율(%)']||0,p=d['단가(원/kg)']||0;"
        "var tr=document.createElement('tr');"
        "tr.innerHTML="
        "'<td class=\"nm\">'+d['원료명']+'</td>'"
        "+'<td><div class=\"sw\">'"
        "+'<input type=\"number\" id=\"r'+i+'\" value=\"'+r0+'\" step=\"0.01\" min=\"0\" max=\"100\" oninput=\"sync('+i+',\\'r\\')\">'"
        "+'<input type=\"range\" id=\"sl'+i+'\" value=\"'+r0+'\" min=\"0\" max=\"100\" step=\"0.01\" oninput=\"sync('+i+',\\'sl\\')\">'"
        "+'</div></td>'"
        "+'<td id=\"amt'+i+'\">'+(r0/100*2000).toFixed(1)+'</td>'"
        "+'<td>'+p+'</td>'"
        "+'<td>'+(d['Brix기여(/1%)']||0)+'</td>'"
        "+'<td>'+(d['산도기여(/1%)']||0)+'</td>'"
        "+'<td id=\"cst'+i+'\">'+(r0/100*(p/1000)*100).toFixed(1)+'원</td>';"
        "tb.appendChild(tr);});calc();}\nbuild();\n"
        "</script>\n"
    )

    return (
        "<!DOCTYPE html>\n<html lang='ko'>\n<head>\n"
        "<meta charset='UTF-8'>\n"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>\n"
        f"<title>디지털 트윈랩 — {product_name}</title>\n"
        + css
        + "</head>\n<body>\n"
        + header + metrics + table + risk_section
        + js_data + js_logic
        + "</body>\n</html>"
    )


_TWIN_EXAMPLE_DRIVE_ID = "1yFdiScZ0yV-e0_-cIWw6EPKYGSJsAKdb"

@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_twin_example_html() -> str | None:
    import urllib.request
    url = f"https://drive.google.com/uc?export=download&id={_TWIN_EXAMPLE_DRIVE_ID}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8")
    except Exception:
        return None

@st.dialog("🔬 가상 시뮬레이터 예시", width="large")
def _show_twin_example_dialog():
    import streamlit.components.v1 as components
    with st.spinner("예시 파일 불러오는 중..."):
        html = _fetch_twin_example_html()
    if html:
        components.html(html, height=620, scrolling=True)
    else:
        st.error("예시 파일을 불러올 수 없습니다. Google Drive 공유 설정을 확인해주세요.")
        st.link_button("📂 Google Drive에서 직접 열기",
                       f"https://drive.google.com/file/d/{_TWIN_EXAMPLE_DRIVE_ID}/view")


# =========================================================
# 5. 공통 UI 컴포넌트
# =========================================================

def show_banner(title: str, desc: str, step: str):
    st.markdown(f"""
    <div class="page-banner">
        <p>STEP {step}</p>
        <h1>{title}</h1>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)


def show_mission(items: list):
    items_html = "".join(f"<li>{i}</li>" for i in items)
    st.markdown(f"""
    <div class="mission-box">
        <h3>📋 이번 실습에서 할 일</h3>
        <ul>{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)


# 각 STEP 말미의 '내 제품으로 옮기기' 입력 — STEP 7에서 모아 최종 제출에 포함된다
_TRANSFER_STEPS = [
    ("s2", "STEP 2 · 페르소나"),
    ("s4", "STEP 4 · 시장분석"),
    ("s5", "STEP 5 · 배합비"),
    ("s6", "STEP 6 · 가상검증"),
]


def show_transfer_box(step_key: str, question: str, placeholder: str,
                      secret_warn: bool = False):
    """실습은 전원 공통 음료 사례로 하되, 재직자가 자기 제품 기준으로 옮겨 적게 한다."""
    st.markdown("---")
    st.markdown(
        '<div class="transfer-box"><b>🎯 내 제품으로 옮기기</b><br>'
        '이 실습은 전원 공통으로 음료 사례를 사용했습니다. 같은 절차를 '
        '<b>본인이 실제로 담당하는 제품</b>에 옮기면 어떻게 되는지 적어보세요. '
        'STEP 7 프로젝트 정리에 모여 최종 과제로 함께 제출됩니다.</div>',
        unsafe_allow_html=True,
    )
    if secret_warn:
        st.error(
            "🔒 **사내 실제 배합비·단가·거래처 정보는 입력하지 마세요.** "
            "가상 수치나 이미 공개된 정보로만 작성합니다. "
            "입력 내용은 과제 시트에 저장되고 AI 대화창에도 올라갈 수 있습니다."
        )
    st.text_area(question, key=f"transfer_{step_key}",
                 placeholder=placeholder, height=90)


def show_step_flow(steps: list, current: int):
    """실습 진행 스텝바 — 완료/현재/예정 단계를 한 줄로 표시"""
    items = []
    for i, s in enumerate(steps):
        cls = "done" if i < current else ("now" if i == current else "todo")
        items.append(
            f'<div class="sf-item {cls}">'
            f'<span class="sf-dot">{i + 1}</span>'
            f'<span class="sf-label">{s}</span></div>'
        )
    st.markdown(f'<div class="step-flow">{"".join(items)}</div>', unsafe_allow_html=True)


def show_step_guide(steps: list, current: int, todo: str,
                    uses: str = "", produces: str = "", minutes: int = 0):
    """탭 상단 단계 안내 — 진행바 + 이번 단계 할 일 / 앞 단계 결과 활용 / 다음 단계 전달물

    실습 결과가 누적되는 구조이므로, 각 단계에서 '앞 단계의 무엇을 쓰고'
    '여기서 만든 것이 어디로 넘어가는지'를 명시해 흐름을 끊어서 진행한다.
    """
    show_step_flow(steps, current)
    rows = [f'<p class="sg-row">📌 <b>이번 단계</b> — {todo}</p>']
    if uses:
        rows.append(f'<p class="sg-row">🔗 <b>앞 단계 결과 활용</b> — {uses}</p>')
    if produces:
        nxt = steps[current + 1] if current + 1 < len(steps) else "다음 STEP"
        rows.append(
            f'<p class="sg-row">📤 <b>여기서 만든 결과</b> — {produces} '
            f'→ <b>{nxt}</b>에서 사용합니다</p>'
        )
    if minutes:
        rows.append(
            f'<span class="sg-time">⏱️ 실습 {minutes}분 · '
            f'진행하는 동안 강사가 순회하며 개별 확인합니다</span>'
        )
    st.markdown(f'<div class="step-guide">{"".join(rows)}</div>', unsafe_allow_html=True)


def show_example(text: str):
    st.markdown(f'<div class="example-box">{text}</div>', unsafe_allow_html=True)


def show_result(text: str):
    st.markdown(f'<div class="result-box">{text}</div>', unsafe_allow_html=True)


def render_ai_result(prompt: str, key: str):
    """AI 실행 버튼 + 결과 출력"""
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI 실행")

    _prompt_with_inst = prompt.strip() + _SUBMIT_INSTRUCTION

    if st.button("▶ Claude에게 분석 요청하기", key=f"run_{key}", use_container_width=True):
        result = run_claude(_prompt_with_inst)
        st.session_state[f"result_{key}"] = result

    st.caption("📋 아래 코드 블록 우측 상단 복사 아이콘 클릭 → ChatGPT, Gemini 등에 붙여넣기")
    st.code(_prompt_with_inst, language=None)

    if result := st.session_state.get(f"result_{key}"):
        st.markdown("#### 📊 분석 결과")
        show_result(result)


def score_persona(fields: dict, defaults: dict) -> tuple:
    """Mad-lib 스타일 페르소나 작성 점수(0~100) 및 코칭 팁 반환"""
    score = 0
    tips = []

    # 1. 직무 분야 — 프리셋 외 직접 입력 여부 (30점)
    job = str(fields.get("직무", ""))
    default_job = str(defaults.get("직무", ""))
    changed_job = job.strip() != default_job.strip()
    if changed_job:
        score += 30
        tips.append("✅ 직무를 직접 입력했어요! 세상에 하나뿐인 나만의 페르소나가 됩니다.")
    else:
        score += 15
        tips.append("💡 직무 직접 입력 칸에 실제 직함(예: 저당 음료 전문 연구원)을 쓰면 더 입체적인 페르소나가 돼요.")

    # 2. 관심 제품 유형 — pill 선택 또는 직접 입력 (25점)
    prod = str(fields.get("관심 제품 유형", ""))
    prod_items = len([x for x in prod.replace("，", ",").split(",") if x.strip()])
    if prod.strip():
        score += 15
        if prod_items >= 3:
            score += 10
            tips.append("✅ 관심 제품을 3가지 이상 구체적으로 선택·입력했습니다!")
        else:
            tips.append("💡 직접 입력 칸에 쉼표로 구분해 2~3가지 제품 유형을 추가하면 AI가 더 전문적으로 반응해요.")
    else:
        tips.append("⚠️ 관심 제품 유형 pill을 선택하거나 직접 입력해 주세요.")

    # 3. 핵심 방향 — 직접 입력 vs 프리셋 선택 (30점)
    rd_key = "연구개발 포인트" if "연구개발 포인트" in fields else "마케팅 포인트"
    rd_val = str(fields.get(rd_key, ""))
    default_rd = str(defaults.get(rd_key, ""))
    changed_rd = rd_val.strip() != default_rd.strip()
    if rd_val.strip():
        score += 15
        if changed_rd:
            score += 15
            tips.append(f"✅ '{rd_key}'를 자신만의 관점으로 직접 입력했어요! AI 페르소나의 핵심 개성이 살아납니다.")
        else:
            tips.append(f"💡 '{rd_key}' 직접 입력 칸에 내 현업 가치관을 한 문장으로 적어보세요.")
    else:
        tips.append(f"⚠️ '{rd_key}'를 pill로 선택하거나 직접 입력해 주세요. 이게 AI 페르소나의 개성을 결정합니다.")

    # 4. 확인 질문 — 변경 여부 (15점)
    test_q = str(fields.get("확인 질문", ""))
    default_q = str(defaults.get("확인 질문", ""))
    changed_q = test_q.strip() != default_q.strip()
    if len(test_q) >= 10:
        score += 8
        if changed_q:
            score += 7
            tips.append("✅ 확인 질문을 직접 작성했어요! 내 실제 업무 상황에 맞는 질문이 페르소나를 검증합니다.")
        else:
            tips.append("💡 확인 질문을 내 제품·업무에 맞게 바꿔보세요. (예: 우리 신제품에 맞는 배합 비율은?)")
    else:
        tips.append("💡 확인 질문을 직접 입력하면 AI가 페르소나를 잘 적용했는지 즉시 확인할 수 있어요.")

    score = max(0, min(100, score))

    if score >= 80:
        tips.append("🎉 완성도 높은 페르소나예요! '이를 적용하기'로 복사해 ChatGPT에 붙여넣어 보세요.")
    elif score >= 60:
        tips.append("👍 좋은 출발입니다. 직접 입력 칸을 한두 군데만 더 채우면 완성입니다.")
    elif score >= 40:
        tips.append("📝 기본 틀이 잡혔어요. pill 선택 외에 직접 입력으로 나만의 내용을 추가해 보세요.")
    else:
        tips.append("📌 pill을 선택하거나 직접 입력 칸을 채워 빈칸을 완성해 보세요!")

    return score, tips


def render_persona_coach(prompt: str, fields: dict, defaults: dict, key: str):
    """페르소나 섹션 전용 — 스크립트 작성 코치 + 이를 적용하기 (API 없이)"""
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### ✏️ 작성 점검")

    if st.button("📊 스크립트 작성 코치", key=f"coach_{key}", use_container_width=True):
        s, t = score_persona(fields, defaults)
        st.session_state[f"coach_score_{key}"] = s
        st.session_state[f"coach_tips_{key}"] = t

    # 코치 결과
    if f"coach_score_{key}" in st.session_state:
        score = st.session_state[f"coach_score_{key}"]
        tips = st.session_state[f"coach_tips_{key}"]
        color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
        st.markdown(f"""
<div style="margin:16px 0 8px 0;">
  <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
    <span style="font-weight:700;font-size:15px;">작성 점수</span>
    <span style="font-weight:900;font-size:22px;color:{color};">{score}점 / 100점</span>
  </div>
  <div style="background:#e5e7eb;border-radius:8px;height:14px;">
    <div style="background:{color};width:{score}%;height:14px;border-radius:8px;"></div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("**코칭 피드백**")
        for tip in tips:
            st.markdown(f"- {tip}")

    st.markdown("**📋 아래 전체를 복사 → ChatGPT / Gemini 등 AI 대화창에 붙여넣기**")
    st.code(prompt.strip() + _SUBMIT_INSTRUCTION, language=None)


def score_data_script(fields: dict, defaults: dict) -> tuple:
    """데이터 수집 스크립트 작성 점수(0~100) 및 코칭 팁 반환 (API 없이)"""
    score = 0
    tips = []

    # 1. 분석 범위 구체성 (25점)
    scope = str(fields.get("분석 범위", ""))
    changed_scope = scope.strip() != str(defaults.get("분석 범위", "")).strip()
    if len(scope) >= 10:
        score += 15
        if changed_scope:
            score += 10
            tips.append("✅ 분석 범위를 직접 설정했습니다!")
        else:
            tips.append("💡 분석 범위를 자신의 프로젝트에 맞게 기간·채널·지역 등을 구체적으로 조정해보세요.")
    else:
        tips.append("⚠️ 분석 범위가 너무 짧아요. 기간·채널·지역 등을 구체적으로 적어주세요.")

    # 2. 출력 형식 구체성 및 수정 여부 (35점)
    output_fmt = str(fields.get("출력 형식", ""))
    changed_fmt = output_fmt.strip() != str(defaults.get("출력 형식", "")).strip()
    if len(output_fmt) >= 15:
        score += 20
        if changed_fmt:
            score += 15
            tips.append("✅ 출력 형식을 직접 지정했어요! 원하는 형태가 명확할수록 AI 결과를 바로 사용할 수 있습니다.")
        else:
            tips.append("💡 출력 형식을 원하는 구체적인 형태로 바꿔보세요. (예: 표 구조, 섹션 구성, 페이지 수)")
    else:
        tips.append("⚠️ 출력 형식을 지정해주세요. AI가 어떤 형태로 정리할지 알 수 없어요.")

    # 3. 요청사항 구체성 및 수정 여부 (40점)
    request = str(fields.get("요청사항", ""))
    changed_req = request.strip() != str(defaults.get("요청사항", "")).strip()
    if len(request) >= 20:
        score += 20
        if changed_req:
            score += 20
            tips.append("✅ 요청사항을 직접 작성했습니다! 구체적인 요청이 AI 결과의 품질을 높입니다.")
        else:
            tips.append("💡 요청사항에 자신만의 추가 조건·우선순위·특이사항을 적어보세요.")
    elif len(request) >= 5:
        score += 10
        tips.append("💡 요청사항을 더 구체적으로 작성하면 AI가 더 정확하게 작업합니다.")
    else:
        tips.append("⚠️ 요청사항을 채워주세요. 추가로 원하는 조건이나 주의사항을 자유롭게 적어주세요.")

    score = max(0, min(100, score))

    if score >= 80:
        tips.append("🎉 완성도 높은 데이터 수집 스크립트예요! '이를 적용하기'로 복사해 ChatGPT에 붙여넣어 보세요.")
    elif score >= 60:
        tips.append("👍 좋은 시작입니다. 위 피드백을 참고해 조금 더 구체화하면 완성입니다.")
    elif score >= 40:
        tips.append("📝 기본 구조는 갖춰졌어요. 출력 형식과 요청사항을 더 구체적으로 채워보세요.")
    else:
        tips.append("📌 항목을 더 구체적으로 작성해보세요!")

    return score, tips


def render_data_coach(prompt: str, fields: dict, defaults: dict, key: str):
    """데이터 섹션 전용 — 스크립트 작성 코치 + 이를 적용하기 (API 없이)"""
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### ✏️ 작성 점검")

    if st.button("📊 스크립트 작성 코치", key=f"coach_{key}", use_container_width=True):
        s, t = score_data_script(fields, defaults)
        st.session_state[f"coach_score_{key}"] = s
        st.session_state[f"coach_tips_{key}"] = t

    if f"coach_score_{key}" in st.session_state:
        score = st.session_state[f"coach_score_{key}"]
        tips = st.session_state[f"coach_tips_{key}"]
        color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
        st.markdown(f"""
<div style="margin:16px 0 8px 0;">
  <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
    <span style="font-weight:700;font-size:15px;">작성 점수</span>
    <span style="font-weight:900;font-size:22px;color:{color};">{score}점 / 100점</span>
  </div>
  <div style="background:#e5e7eb;border-radius:8px;height:14px;">
    <div style="background:{color};width:{score}%;height:14px;border-radius:8px;"></div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("**코칭 피드백**")
        for tip in tips:
            st.markdown(f"- {tip}")

    st.markdown("**📋 아래 전체를 복사 → ChatGPT 대화창에 붙여넣기**")
    st.code(prompt.strip() + _SUBMIT_INSTRUCTION, language=None)


# =========================================================
# 5. 로그인 게이트
# =========================================================

try:
    _ACCESS_CODE = st.secrets["ACCESS_CODE"]
except Exception:
    _ACCESS_CODE = "kfi2026"  # 로컬 실행 기본값

try:
    _ADMIN_CODE = st.secrets["ADMIN_CODE"]
except Exception:
    # secrets에 없으면 관리자 기능을 잠근다 (소스에 코드를 남기지 않기 위함)
    _ADMIN_CODE = ""

# 새로고침·탭 재오픈 후 URL 쿼리 파라미터로 로그인 상태 자동 복원 (8시간 유효)
import time as _time
if not st.session_state.get("authenticated"):
    _qp = st.query_params
    try:
        if "u" in _qp and "t" in _qp:
            if _time.time() - float(_qp["t"]) < 8 * 3600:
                st.session_state["authenticated"] = True
                st.session_state["student_name"] = _qp["u"]
    except Exception:
        pass

# 크롤링 실습 전용 화면 — 주소 뒤에 ?m=crawl 을 붙이면 로그인 없이 들어온다.
# 강사 PC에 접속한 실습자가 이 실습만 하도록 떼어 놓은 모드.
_CRAWL_ONLY = False
try:
    _CRAWL_ONLY = st.query_params.get("m") == "crawl"
except Exception:
    _CRAWL_ONLY = False
if _CRAWL_ONLY:
    st.session_state["authenticated"] = True
    st.session_state.setdefault("student_name", "")

if not st.session_state.get("authenticated"):
    st.markdown("""
    <div style="max-width:420px;margin:80px auto 0 auto;background:#ffffff;
    border:1.5px solid #e2e8f0;border-radius:16px;padding:40px 36px;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
    <div style="text-align:center;margin-bottom:24px;">
      <div style="font-size:40px;margin-bottom:8px;">🧪</div>
      <div style="font-size:20px;font-weight:800;color:#0f172a;">AI 제품개발 실습교안</div>
      <div style="font-size:13px;color:#64748b;margin-top:4px;">한국식품정보원</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    _lc, _cc, _rc = st.columns([1, 1.4, 1])
    with _cc:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        with st.form("_login_form"):
            _code_in = st.text_input("접속 코드", type="password",
                                      placeholder="강사에게 받은 접속 코드")
            _name_in = st.text_input("이름", placeholder="본인 이름 입력 (예: 홍길동)")
            _submitted = st.form_submit_button("입장하기 →", use_container_width=True, type="primary")
        if _submitted:
            if _code_in != _ACCESS_CODE:
                st.error("접속 코드가 올바르지 않습니다.")
            elif not _name_in.strip():
                st.warning("이름을 입력해주세요.")
            else:
                st.session_state["authenticated"] = True
                st.session_state["student_name"] = _name_in.strip()
                # 이름 칸에 관리자 코드를 넣으면 강사 모드로 바로 들어간다
                if _ADMIN_CODE and _name_in.strip() == _ADMIN_CODE:
                    st.session_state["_admin_verified"] = True
                # URL에 저장 → 새로고침·탭 재오픈 후에도 8시간 자동 복원
                st.query_params["u"] = _name_in.strip()
                st.query_params["t"] = str(_time.time())
                st.rerun()
    st.stop()

# 강의용 커서 강조 — 큰 빨간 원 커서 (CSS 커스텀 커서)
if st.session_state.get("_big_cursor"):
    _CUR = (
        "data:image/svg+xml;utf8,"
        "%3Csvg xmlns='http://www.w3.org/2000/svg' width='44' height='44'%3E"
        "%3Ccircle cx='22' cy='22' r='15' fill='rgba(255,0,0,0.25)' "
        "stroke='%23ff2020' stroke-width='3'/%3E"
        "%3Ccircle cx='22' cy='22' r='2.5' fill='%23ff2020'/%3E%3C/svg%3E"
    )
    st.markdown(
        "<style>"
        "html, body, .stApp, .stApp *, [data-testid='stSidebar'] * {"
        "  cursor: url(\"" + _CUR + "\") 22 22, auto !important; }"
        "</style>",
        unsafe_allow_html=True,
    )


# 로그인 상태에서 세션당 1회 접속 기록
if (st.session_state.get("authenticated")
        and st.session_state.get("student_name")
        and not st.session_state.get("_login_recorded")):
    _record_login(st.session_state["student_name"])
    st.session_state["_login_recorded"] = True


# =========================================================
# 6. 사이드바
# =========================================================

if _CRAWL_ONLY:
    # 목차 사이드바를 감춰 한 화면만 남긴다
    st.markdown(
        "<style>[data-testid='stSidebar'],[data-testid='stSidebarCollapsedControl']"
        "{display:none !important;}</style>",
        unsafe_allow_html=True,
    )
    section = "4️⃣ 시장분석 및 학습"

with st.sidebar:
    st.markdown("## 🧪 AI 제품개발 실습")
    st.markdown("---")
    _sname = st.session_state.get("student_name", "")
    if _sname:
        st.markdown(f"👤 **{_sname}**")
        st.markdown("---")
    _section_pick = st.radio(
        "실습 목차",
        [
            "🏠 교육 개요",
            "1️⃣ 신제품 개발 프로세스",
            "2️⃣ 제품개발 페르소나",
            "3️⃣ 제품개발용 데이터",
            "4️⃣ 시장분석 및 학습",
            "5️⃣ 배합비 개발",
            "6️⃣ 가상모델 개발",
            "7️⃣ 프로젝트 정리",
            "🔐 관리자 현황판",
        ],
        label_visibility="collapsed"
    )
    if not _CRAWL_ONLY:
        section = _section_pick
    st.markdown("---")
    # 강사 모드에서만 — 화면 공유 시 마우스 위치가 잘 보이도록
    if st.session_state.get("_admin_verified"):
        st.markdown("---")
        _big_cursor = st.toggle("🔴 커서 강조 (강의용)", key="_big_cursor",
                                help="화면 공유 중 마우스 위치를 크게 표시합니다.")
        if _big_cursor:
            st.caption("이 앱 화면 안에서만 적용됩니다.")

    st.caption("⚠️ 새로고침하면 입력한 내용이 사라집니다. 단계마다 제출해 두세요.")
    st.caption("한국식품정보원 AI 제품개발 교육")
    st.caption("© 2026 KFI")

    # 강사 전용 — 구글 시트 탭 일괄 초기화
    # 진입 직후 rerun에서 expander가 닫히면 결과가 안 보이므로, 그때는 펼쳐둔다
    _adm_open = bool(st.session_state.get("_admin_verified")
                     or st.session_state.get("_admin_msg"))
    with st.expander("🔧 관리", expanded=_adm_open):
        if not st.session_state.get("_admin_verified"):
            if st.session_state.get("_admin_msg"):
                st.error(st.session_state.pop("_admin_msg"))
            _admin_pw = st.text_input("관리자 코드", type="password", key="_admin_pw_input",
                                      placeholder="강사 전용 코드 입력")
            if st.button("관리자 모드 진입", key="_admin_verify_btn", use_container_width=True):
                if _ADMIN_CODE and _admin_pw == _ADMIN_CODE:
                    st.session_state["_admin_verified"] = True
                    st.rerun()
                elif not _ADMIN_CODE:
                    st.session_state["_admin_msg"] = (
                        "이 서버에는 관리자 코드가 설정되어 있지 않습니다. "
                        "secrets.toml의 ADMIN_CODE를 확인하세요."
                    )
                    st.rerun()
                else:
                    st.session_state["_admin_msg"] = "관리자 코드가 올바르지 않습니다."
                    st.rerun()
        else:
            st.success("🔓 관리자 모드 활성화됨")
            st.caption("🔐 관리자 현황판에서 설치 패키지를 내려받을 수 있습니다.")
            if st.button("🚪 관리자 모드 종료", key="_admin_exit_btn", use_container_width=True):
                st.session_state["_admin_verified"] = False
                st.rerun()
            st.markdown("---")
            st.caption("구글 시트에 모든 과제 탭을 미리 생성합니다.")
            if st.button("📊 시트 탭 일괄 생성", key="_init_tabs_btn", use_container_width=True):
                with st.spinner("시트 탭 생성 중..."):
                    try:
                        _gc = _get_gs_client()
                        _sh = _gc.open_by_key(_GS_SHEET_ID)
                        _existing = {ws.title for ws in _sh.worksheets()}
                        _created, _skipped = [], []
                        for _tab in _ALL_HW_TABS:
                            if _tab not in _existing:
                                _ws = _sh.add_worksheet(title=_tab, rows=1000, cols=5)
                                _ws.append_row(_HW_HEADERS)
                                _created.append(_tab)
                            else:
                                _skipped.append(_tab)
                        # 📊 제출현황 탭 재생성
                        _SUMMARY = "📊 제출현황"
                        if _SUMMARY in _existing:
                            _sh.del_worksheet(_sh.worksheet(_SUMMARY))
                        # cols=50: D열부터 학생 이름이 우측으로 최대 46명까지 기록 가능
                        _sw = _sh.add_worksheet(title=_SUMMARY, rows=30, cols=50)
                        _sw.update("A1:D1", [["섹션·탭", "시트명", "제출수", "제출자 →"]])
                        _tab_sections = [
                            ("2️⃣ 연구원 페르소나",      "연구원_페르소나"),
                            ("2️⃣ 마케터 페르소나",      "마케터_페르소나"),
                            ("3️⃣ 데이터 수집 스크립트", "데이터수집스크립트"),
                            ("3️⃣ 데이터 학습지시",      "데이터학습지시"),
                            ("4️⃣ 온라인 시장분석",      "온라인시장분석"),
                            ("4️⃣ 식품전문정보분석",     "식품전문정보분석"),
                            ("4️⃣ 시장조사 학습",        "시장조사학습"),
                            ("4️⃣ 보고서 작성",          "보고서작성"),
                            ("4️⃣ AI 간 대화전환",       "AI전환"),
                            ("5️⃣ 배합비 작성",          "배합비"),
                            ("5️⃣ 배합비 미션",          "배합비_미션"),
                            ("5️⃣ 배합비 프로세스",      "배합비_프로세스"),
                            ("6️⃣ 디지털트윈랩",         "디지털트윈랩"),
                            ("6️⃣ 가상소비자모델",       "가상소비자모델"),
                            ("6️⃣ 관능검사",             "관능검사"),
                            ("7️⃣ 프로젝트 정리",        "프로젝트정리"),
                        ]
                        _summary_rows = []
                        for _si, (_sec, _tab_name) in enumerate(_tab_sections):
                            _formula = "=IFERROR(COUNTA('" + _tab_name + "'!B2:B1000),0)"
                            _summary_rows.append([_sec, _tab_name, _formula])
                        _summary_rows.append(["", "", ""])
                        _summary_rows.append(["전체 합계", "", "=SUM(C2:C" + str(1 + len(_ALL_HW_TABS)) + ")"])
                        # batch_update로 수식(USER_ENTERED) 입력 — 복원 코드와 동일 메서드
                        _sw.batch_update(
                            [{"range": "A2", "values": _summary_rows}],
                            value_input_option="USER_ENTERED",
                        )
                        # D열: 각 행마다 개별 시트 B열을 가로로 자동 펼치는 수식
                        _d_formula_rows = []
                        for _si in range(len(_tab_sections)):
                            _row = _si + 2
                            _f = ('=IFERROR(TRANSPOSE(ARRAYFORMULA('
                                  'ROW(INDIRECT("A1:A"&COUNTA(INDIRECT("\'"&B' + str(_row) + '&"\'!B2:B1000"))))'
                                  '&". "&FILTER(INDIRECT("\'"&B' + str(_row) + '&"\'!B2:B1000"),'
                                  'INDIRECT("\'"&B' + str(_row) + '&"\'!B2:B1000")<>""))),"")' )
                            _d_formula_rows.append([_f])
                        _sh.values_update(
                            "'📊 제출현황'!D2",
                            params={"valueInputOption": "USER_ENTERED"},
                            body={"values": _d_formula_rows},
                        )
                        # 탭 순서: 제출현황 맨 앞 → _ALL_HW_TABS 순 → 그 외 탭
                        _all_ws = {w.title: w for w in _sh.worksheets()}
                        _ordered = [_sw]
                        for _t in _ALL_HW_TABS:
                            if _t in _all_ws:
                                _ordered.append(_all_ws[_t])
                        _rest = [w for w in _sh.worksheets() if w.title != _SUMMARY and w.title not in _ALL_HW_TABS]
                        _sh.reorder_worksheets(_ordered + _rest)
                        if _created:
                            st.success(f"✅ 생성됨: {', '.join(_created)}")
                        if _skipped:
                            st.info(f"이미 존재: {', '.join(_skipped)}")
                        st.success("📊 제출현황 탭도 업데이트됐습니다.")
                    except Exception as _e:
                        st.error(f"오류: {_e}")

            st.markdown("---")
            st.caption("모든 섹션·탭의 스크립트 입력칸·과제 제출란에 테스트용 더미 데이터를 채웁니다. (구글 시트에는 저장되지 않음 — 프로젝트 정리 반영 확인용)")
            st.caption("⏳ 20개 항목을 한 번에 AI로 생성하므로 30~40초 정도 걸릴 수 있습니다. 완료될 때까지 기다려 주세요.")
            if st.button("🎲 전체 섹션 더미 데이터 자동입력 (AI 생성)", key="_fill_dummy_btn", use_container_width=True):
                _tag = str(random.randint(1000, 9999))

                def _rtk(_theme):
                    return _theme.replace(" ", "_").replace("·", "").replace(".", "")

                _r_theme_now = st.session_state.get("r_theme_ml") or "💪 기능성음료 개발연구원"
                _m_theme_now = st.session_state.get("m_theme_ml") or "🧃 음료 브랜드마케터"
                _r_rtk_now = _rtk(_r_theme_now)
                _m_rtk_now = _rtk(_m_theme_now)

                _dummy_scenario = random.choice(["📉 시나리오 A — 원가절감", "👅 시나리오 B — 맛 개선"])

                # 짧은 값(이름·수치)은 그대로 무작위 생성, 나머지 "스크립트"·"AI 생성결과"는
                # Claude를 한 번 호출해 서로 맥락이 통하는 실제 문장으로 채운다.
                _dummy_values = {
                    f"r_name_{_r_rtk_now}": f"테스트연구원_{_tag}",
                    f"m_name_{_m_rtk_now}": f"테스트마케터_{_tag}",
                    "bev_prodname": f"테스트음료_{_tag}",

                    "ms2_scenario": _dummy_scenario,
                    "ms2_prev_scenario": _dummy_scenario,
                }
                # 페르소나 경력·제품 카테고리·데이터 유형의 기본값 (AI 생성 실패 시 대체용)
                _fallback_r_career = f"[테스트#{_tag}] 음료 배합 연구 경력 12년, 관능평가·이화학분석 전문"
                _fallback_m_career = f"[테스트#{_tag}] 식음료 브랜드 마케팅 경력 8년, 신제품 런칭 다수"
                _fallback_ml_cat = f"[테스트#{_tag}] 저당 기능성 탄산음료"
                _fallback_ml_theme = f"[테스트#{_tag}] 배합비 이론 및 소비자 트렌드 데이터"

                _ai_fields = _generate_ai_dummy_fields(_tag)
                if _ai_fields:
                    # 이 4개는 AI가 정한 제품 컨셉과 맞물리도록 동적 키(rtk 포함)에 매핑
                    _dummy_values[f"r_career_{_r_rtk_now}"] = _ai_fields.pop("r_career_gen", _fallback_r_career)
                    _dummy_values[f"m_career_{_m_rtk_now}"] = _ai_fields.pop("m_career_gen", _fallback_m_career)
                    _dummy_values["ml_cat_manual"] = _ai_fields.pop("ml_cat_gen", _fallback_ml_cat)
                    _dummy_values["ml_theme_manual"] = _ai_fields.pop("ml_theme_gen", _fallback_ml_theme)
                    _dummy_values.update(_ai_fields)
                else:
                    st.warning("⚠️ AI 생성 호출 실패 — 스크립트·AI결과란은 짧은 기본 문구로 대체합니다.")
                    _dummy_values[f"r_career_{_r_rtk_now}"] = _fallback_r_career
                    _dummy_values[f"m_career_{_m_rtk_now}"] = _fallback_m_career
                    _dummy_values["ml_cat_manual"] = _fallback_ml_cat
                    _dummy_values["ml_theme_manual"] = _fallback_ml_theme
                    _dummy_values.update({
                        k: f"[테스트#{_tag}] (AI 생성 실패로 기본 더미 문구 사용) {v}"
                        for k, v in _AI_DUMMY_FIELDS.items()
                        if k not in ("r_career_gen", "m_career_gen", "ml_cat_gen", "ml_theme_gen")
                    })

                for _k, _v in _dummy_values.items():
                    st.session_state[_k] = _v
                st.success(f"✅ 더미 데이터 #{_tag} 입력 완료 — 각 탭과 '7️⃣ 프로젝트 정리'에서 반영 여부를 확인하세요.")
                st.rerun()

    st.markdown("---")
    if st.button("로그아웃", key="_logout_btn", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["student_name"] = ""
        st.query_params.clear()
        st.rerun()


# =========================================================
# 7. 섹션별 화면
# =========================================================

# ----------------------------------------------------------
# 0. 교육 개요
# ----------------------------------------------------------
if section == "🏠 교육 개요":
    st.markdown("""
    <div class="page-banner">
        <p>AI를 이용한 제품개발 실습교안</p>
        <h1>🧪 식품 신제품 AI 개발 실습</h1>
        <p>페르소나 설계부터 배합비 개발, 가상 소비자 조사까지 — AI와 함께 한 사이클을 완성합니다</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🎯 교육 대상**\n\n식품개발 · 상품기획 · 마케팅 · 품질 · 생산 실무자")
    with col2:
        st.success("**🕐 교육 시간**\n\n6시간 (6개 실습 + 발표)")
    with col3:
        st.warning("**📦 최종 결과물**\n\n제품 콘셉트 · 배합비 · 소비자 조사표 · 발표문")

    st.markdown("---")
    st.markdown("## 📅 교육 일정")

    schedule = [
        ("10:00–11:00", "신제품 개발 프로세스 개요", "기존 vs AI 식품개발 모델 비교", "PPT"),
        ("11:00–12:00", "AI 제품개발 준비", "페르소나 정의 · 스크립트 작성 · 대화실습 · 빅데이터 학습", "PPT/노트북"),
        ("13:00–14:00", "AI 제품개발 훈련", "온라인 시장분석 · 식품전문정보분석 · 시장조사 데이터 학습 · 보고서 작성", "PPT/노트북"),
        ("14:00–16:00", "AI 제품개발 실무1", "배합비 시뮬레이터 제작 · 미션수행 · 개발 프로세스 실습", "PPT/노트북"),
        ("16:00–17:00", "AI 제품개발 실무2", "가상소비자조사 · 디지털트윈 · 프로젝트 정리", "PPT/노트북"),
    ]

    for time, subject, content, tool in schedule:
        col_t, col_s, col_c, col_tool = st.columns([1.5, 2, 3, 1.5])
        col_t.markdown(f"**{time}**")
        col_s.markdown(f"🔹 {subject}")
        col_c.markdown(content)
        col_tool.markdown(f"`{tool}`")

    st.markdown("---")
    st.markdown("### 🔧 사전 준비 (교육생)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**1. ChatGPT / Gemini**\n\n무료 계정 가입 필수\n\n⚠️ OpenAI 최대 파일 5개 등록 가능")
    with col2:
        st.markdown("**2. Google 로그인**\n\nGmail 계정으로 로그인")
    with col3:
        st.markdown("**3. Chrome 브라우저**\n\n설치 및 실행 확인")
    with col4:
        st.markdown("**4. NotebookLM**\n\nnotebooklm.google.com 로그인")

    st.markdown("---")
    st.markdown("### 📦 교육 전 AI 프로젝트 사전 설정")
    st.caption("교육 시작 전 아래 두 가지 AI 환경을 미리 만들어두세요. 교육 중 소스 파일과 페르소나를 빠르게 등록할 수 있습니다.")

    col_gpt, col_gem = st.columns(2)

    with col_gpt:
        st.markdown("""<div style="background:#f0f9ff;border:1.5px solid #7dd3fc;border-radius:12px;padding:16px 18px;">
<div style="font-size:14px;font-weight:700;color:#0c4a6e;margin-bottom:10px;">💬 ChatGPT 프로젝트 만들기</div>
<ol style="color:#0369a1;font-size:13px;line-height:2.0;margin:0;padding-left:18px;">
<li>ChatGPT 접속 → 왼쪽 메뉴 <b>프로젝트</b> → <b>새 프로젝트</b> 클릭</li>
<li>프로젝트 이름 설정<br>
<span style="background:#e0f2fe;border-radius:4px;padding:1px 6px;font-size:11px;">예) 음료신제품개발_2026 / 본인이름_음료개발</span></li>
<li>아래 <b>수업용 학습용 자료 다운로드</b> 후 프로젝트 소스에 파일 등록<br>
<span style="font-size:11px;color:#0284c7;">⚠️ OpenAI 프로젝트 소스는 최대 5개 파일</span></li>
<li>(페르소나 스크립트 완성후) <b>프로젝트 지침으로 등록 예정</b></li>
</ol>
</div>""", unsafe_allow_html=True)

    with col_gem:
        st.markdown("""<div style="background:#f0fdf4;border:1.5px solid #86efac;border-radius:12px;padding:16px 18px;">
<div style="font-size:14px;font-weight:700;color:#14532d;margin-bottom:10px;">💎 Gemini Gem 만들기</div>
<ol style="color:#16a34a;font-size:13px;line-height:2.0;margin:0;padding-left:18px;">
<li>Gemini 접속 → 왼쪽 메뉴 <b>Gems</b> → <b>새 Gem 만들기</b> 클릭</li>
<li>Gem 이름 설정<br>
<span style="background:#dcfce7;border-radius:4px;padding:1px 6px;font-size:11px;">예) 음료개발연구원_페르소나 / 음료마케터_페르소나</span></li>
<li><b>지침(Instructions)</b>에 페르소나 스크립트 붙여넣기<br>
<span style="font-size:11px;color:#15803d;">(2️⃣ 제품개발 페르소나 섹션에서 작성)</span></li>
<li>(페르소나 스크립트 완성후) <b>지침으로 등록예정</b></li>
</ol>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 수업용 학습용 자료 다운로드")
    st.caption("클릭하면 Google Drive에서 열립니다. 좌측 상단 ⬇ 아이콘으로 다운로드하세요.")
    st.markdown('<span style="background:#fef08a;border:1px solid #f59e0b;border-radius:4px;'
                'padding:1px 6px;font-size:12px;font-weight:700;color:#92400e;">노란색</span> '
                '<span style="font-size:13px;color:#475569;">배경 파일은 <b>필수 다운로드 자료</b>입니다.</span>',
                unsafe_allow_html=True)

    DL_RESOURCES = {
        "🎓 개발 이론": [
            ("신제품 개발이론 A", "1HGK3QfvHrL2uwuOQySe1Dz0oFr654U0G", False),
            ("신제품 개발이론 B", "11ISqRcU6ECmDc8SJwi2uBWBlzn4jZkK1", False),
            ("신제품 아이디어 도출", "1QHDKDku07lvw7p3AT2kqoLgY7WSHdSC6", False),
        ],
        "🥤 음료 데이터·기술": [
            ("음료시장 세분화 데이터", "1fYqetwVjSDPgpACUSoPPpMgCPefviO8Q", True),
            ("음료 제조기술과 이론", "1ajAKtax9FiyiRi0zE26EdQszdhY6nMYn", True),
            ("신제품 관능평가 방법", "1H1f0Kfdg19VrOuNNfYuCrRs0DZyQvVqA", True),
            ("당류 저감화 기술가이드 (저당원료)", "1hmiLf83YCXDF90zizj6VicMT_IgHdGmw", False),
            ("음료용 원재료 목록/AI지침", "1SEbSIN2nPDsrbn5PQxrWc1eyj0VggT-u", False),
        ],
        "📋 식품공전·규정": [
            ("식품공전 — 음료류 정의", "1TJt7pi0E_wYSvzfW_G_P4WJclL5aBYAS", True),
            ("식품공전 — 일반시험법 (관능평가)", "1kCo5Qrp6Pb_Kw2LiJXJJR1AbtJyZlnZW", False),
            ("식품 유통기한 산출모델 시스템 검증 연구", "1ugc9ZKu5peNOFyqsjNMOmXiLHXxJJz4v", False),
        ],
        "📝 실습 양식": [
            ("음료개발 데이터베이스", "https://docs.google.com/spreadsheets/d/1hq-yxoyaxUXWdxJnLeDqGlLXRpeIwzhR/edit?usp=drive_link", True),
        ],
    }

    def _dl_btn(name, fid, highlight):
        bg     = "#fef08a" if highlight else "#f1f5f9"
        border = "#f59e0b" if highlight else "#cbd5e1"
        color  = "#92400e" if highlight else "#334155"
        fw     = "700"     if highlight else "500"
        url    = fid if fid.startswith("http") else f"https://drive.google.com/file/d/{fid}/view"
        return (f'<a href="{url}" target="_blank" style="display:inline-block;padding:8px 16px;'
                f'background:{bg};border:1.5px solid {border};border-radius:8px;color:{color};'
                f'font-weight:{fw};font-size:14px;text-decoration:none;margin:4px 4px 4px 0;">'
                f'📥 {name}</a>')

    for cat_name, files in DL_RESOURCES.items():
        st.markdown(f"**{cat_name}**")
        btns = "".join(_dl_btn(n, fid, hl) for n, fid, hl in files)
        st.markdown(f'<div style="display:flex;flex-wrap:wrap;margin-bottom:8px;">{btns}</div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📤 공유 링크 만들기 가이드")
    st.caption("과제 제출 시 파일 링크가 필요한 경우 아래 가이드를 참고하세요.")

    with st.expander("📊 구글 시트 공유 링크 만드는 법 (배합비 등 표 형식 결과물)"):
        _show_share_guide()

    st.markdown("")
    with st.expander("📁 구글 드라이브 파일 공유 링크 만드는 법 (HTML·PDF 등)"):
        st.markdown("""
<div style="background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:10px;
padding:16px 20px;margin:4px 0;">
<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">
📁 구글 드라이브 파일 업로드 &amp; 공유 링크 만들기</div>
<div style="font-size:13px;color:#334155;line-height:1.9;">

<b style="color:#0f172a;">① 구글 드라이브에 파일 업로드</b><br>
&nbsp;&nbsp;• <b>drive.google.com</b> 접속 (Gmail 계정 로그인 필요)<br>
&nbsp;&nbsp;• 좌측 상단 <span style="background:#e2e8f0;border-radius:4px;padding:1px 6px;font-size:12px;font-weight:600;">+ 새로 만들기</span> 클릭 → <b>"파일 업로드"</b> 선택<br>
&nbsp;&nbsp;• 내 컴퓨터에서 저장한 파일(HTML·PDF 등) 선택 후 업로드<br><br>

<b style="color:#0f172a;">② 파일 공유 설정 (누구나 볼 수 있게)</b><br>
&nbsp;&nbsp;• 업로드된 파일에서 <b>마우스 우클릭</b> → <b>"공유"</b> 클릭<br>
&nbsp;&nbsp;• 공유 팝업에서 <b>"일반 액세스"</b> 항목의 <b>"변경"</b> 클릭<br>
&nbsp;&nbsp;• <b>"링크가 있는 모든 사용자"</b> 선택 → 역할: <b>뷰어</b><br>
&nbsp;&nbsp;• <span style="background:#e2e8f0;border-radius:4px;padding:1px 6px;font-size:12px;font-weight:600;">완료</span> 클릭<br><br>

<b style="color:#0f172a;">③ 링크 복사 후 과제 제출란에 붙여넣기</b><br>
&nbsp;&nbsp;• 공유 팝업 하단 <b>"링크 복사"</b> 클릭<br>
&nbsp;&nbsp;• 복사된 링크를 과제 제출의 <b>파일 링크</b> 입력칸에 붙여넣기

</div></div>""", unsafe_allow_html=True)

    with st.expander("🎞️ NotebookLM 슬라이드 전체공유 링크 만드는 법"):
        st.markdown("""
<div style="background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:10px;
padding:16px 20px;margin:4px 0;">
<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">
🎞️ NotebookLM 슬라이드 생성 &amp; 전체공유 링크 만들기</div>
<div style="font-size:13px;color:#334155;line-height:1.9;">

<b style="color:#0f172a;">① NotebookLM에서 슬라이드 만들기</b><br>
&nbsp;&nbsp;• <b>notebooklm.google.com</b> 접속 → 해당 노트북 열기<br>
&nbsp;&nbsp;• 우측 패널 <b>"노트북 가이드"</b> 클릭<br>
&nbsp;&nbsp;• 하단 <b>"슬라이드 만들기"</b> 또는 <b>"프레젠테이션"</b> 선택<br>
&nbsp;&nbsp;• AI가 자동으로 슬라이드를 생성합니다<br><br>

<b style="color:#0f172a;">② 슬라이드 전체공유 링크 만들기</b><br>
&nbsp;&nbsp;• 슬라이드가 열리면 우측 상단 <b>공유 아이콘(↗)</b> 또는 <b>"공유"</b> 버튼 클릭<br>
&nbsp;&nbsp;• <b>"프레젠테이션 공유"</b> 팝업에서 <b>"링크가 있는 모든 사용자"</b> 선택<br>
&nbsp;&nbsp;• <b>"링크 복사"</b> 클릭<br><br>

<b style="color:#0f172a;">③ 링크 붙여넣기</b><br>
&nbsp;&nbsp;• 복사된 링크를 과제 제출의 <b>파일 링크</b> 입력칸에 붙여넣기<br>
&nbsp;&nbsp;• <span style="background:#fef9c3;border-radius:4px;padding:1px 6px;font-size:12px;">
⚠️ Google 계정으로 로그인 상태에서만 생성 가능합니다</span>

</div></div>""", unsafe_allow_html=True)


# ----------------------------------------------------------
# 1. 신제품 개발 프로세스
# ----------------------------------------------------------
elif section == "1️⃣ 신제품 개발 프로세스":
    show_banner(
        "신제품 개발 프로세스",
        "AI를 활용한 음료 신제품 개발 교육의 전체 흐름을 단계별로 확인하세요.",
        "1 / 7"
    )

    st.markdown("#### 📊 교육 진행 흐름도")
    st.caption("아래 7단계는 이 교육 전체의 학습 순서입니다.")

    def _card(num, title, items):
        items_html = "<br>".join(items)
        return f"""<div style="background:#ffffff;border:2px solid #334155;border-radius:10px;
padding:20px 22px;height:100%;box-sizing:border-box;">
<div style="background:#1e293b;color:#ffffff;border-radius:20px;padding:5px 16px;
font-size:15px;font-weight:800;display:inline-block;margin-bottom:12px;">STEP {num}</div>
<div style="font-size:18px;font-weight:700;color:#0f172a;line-height:1.6;margin-bottom:10px;">{title}</div>
<div style="font-size:16px;color:#475569;line-height:2.1;">{items_html}</div>
</div>"""

    _ARR = """<div style="display:flex;align-items:center;justify-content:center;height:100%;padding-top:34px;">
<div style="width:26px;height:4px;background:#475569;"></div>
<div style="width:0;height:0;border-top:10px solid transparent;border-bottom:10px solid transparent;border-left:16px solid #475569;"></div>
</div>"""

    # ── 행 1: STEP 1 ~ 4 ──
    c1, a1, c2, a2, c3, a3, c4 = st.columns([4, 0.7, 4, 0.7, 4, 0.7, 4])
    with c1:
        st.markdown(_card("1","제품개발을 위한<br>AI 환경 만들기",
            ["👤 연구원 페르소나 정의","📝 스크립트 작성","💬 대화 실습"]), unsafe_allow_html=True)
    with a1: st.markdown(_ARR, unsafe_allow_html=True)
    with c2:
        st.markdown(_card("2","제품개발을 위한<br>학습자료 입력",
            ["📊 빅데이터","🛒 온라인 시장분석","🏪 오프라인 시장분석","📋 식품전문자료 분석"]), unsafe_allow_html=True)
    with a2: st.markdown(_ARR, unsafe_allow_html=True)
    with c3:
        st.markdown(_card("3","보고서 작성",
            ["🎯 미션 수행","📄 결과 산출물 생성"]), unsafe_allow_html=True)
    with a3: st.markdown(_ARR, unsafe_allow_html=True)
    with c4:
        st.markdown(_card("4","AI 간 전환학습",
            ["🔄 ChatGPT → Gemini","📦 페르소나·자료 이관","💎 Gemini Gems 활용"]), unsafe_allow_html=True)

    # ── 행 2: STEP 5 ~ 7 ──
    _, a4, c5, a5, c6, a6, c7 = st.columns([4, 0.7, 4, 0.7, 4, 0.7, 4])
    with a4: st.markdown(_ARR, unsafe_allow_html=True)
    with c5:
        st.markdown(_card("5","제품개발 실습",
            ["⚗️ 배합비 작성","🎯 미션 수행","🔬 개발 프로세스 실습"]), unsafe_allow_html=True)
    with a5: st.markdown(_ARR, unsafe_allow_html=True)
    with c6:
        st.markdown(_card("6","가상모델 개발",
            ["🔬 디지털 트윈랩","👥 가상 소비자 모델","🧪 관능검사"]), unsafe_allow_html=True)
    with a6: st.markdown(_ARR, unsafe_allow_html=True)
    with c7:
        st.markdown(_card("7","프로젝트 정리",
            ["📁 전체 결과물 정리","🎤 발표 준비","📌 포트폴리오 작성"]), unsafe_allow_html=True)


# ----------------------------------------------------------
# 2. 제품개발 페르소나
# ----------------------------------------------------------
elif section == "2️⃣ 제품개발 페르소나":
    show_banner(
        "제품개발용 AI 페르소나 만들기",
        "연구원과 마케터 페르소나를 설계하고, AI에게 적용하는 스크립트 작성법을 훈련합니다.",
        "2 / 7"
    )
    show_mission([
        "연구원 페르소나 항목(개인정보·기본 프로필·직무 역량 등)을 테이블에 직접 입력하기",
        "입력한 내용을 AI 대화창에 붙여넣기 위한 스크립트 형태로 완성하기",
        "AI가 페르소나를 적용했는지 간단한 질문으로 확인하기",
    ])

    # 이 STEP 안의 실습 순서 — 각 탭 상단에 진행 위치를 표시한다
    _S2_STEPS = ["예시 보기", "연구원 페르소나", "마케터 페르소나"]

    tab_ex, tab_researcher, tab_marketer = st.tabs(["📖 예시 스크립트 보기", "🔬 연구원 페르소나 만들기", "📢 마케터 페르소나 만들기"])

    with tab_ex:
        show_step_guide(
            _S2_STEPS, 0,
            todo="완성된 페르소나 예시를 읽고, 어떤 항목이 필요한지 눈으로 익힙니다.",
            produces="페르소나 항목 구조에 대한 이해",
            minutes=5,
        )
        st.markdown("#### 연구원 페르소나 예시 — 한서윤 (RTD 음료 개발 연구원)")
        st.markdown("##### STEP 1. 페르소나 항목 테이블 작성")
        st.markdown("""
| 항목 | 내용 |
|---|---|
| **개인정보** | 이름 [한서윤], 연령 [35세], 직장 [네추럴 랩 베버리지], 직무 [음료개발연구원], 성별 [여성], 출신지 [대전광역시] |
| **관심 음료 유형** | 커피(추출), 차(Tea), 유음료, 기능성 음료(에너지/단백질), 탄산음료에 대한 폭넓은 이해 |
| **보유기술** | 배합 최적화기술 보유: 감미료/산미료 밸런싱, 원부재료와 향료 사용 경험 풍부 |
| **식품공정 지식** | HTST(고온단시간), UHT(초고온살균), 레토르트 등 공정별 맛 변화 예측 능력 |
| **식품배합비 이론** | 맛 보존기술, 층 분리(침전) 제어, 유화 안정성(Emulsion Stability) 기술 보유 |
| **연구개발 포인트** | 공장에서 나온 첫 병과 유통기한 마지막 날의 맛이 동일해야 한다 (재현성 중시) |
| **업무 환경** | 당도계(Brix), 산도계(pH), 색차계, 가속 가혹 실험기(Incubator), 점도계 |
| **근무경력** | 헬스케어 음료 스타트업 5년 근무 후 식품 음료 대기업 중견 연구원 경력 15년의 시니어 |
| **관심사** | 편의점(CVS) 신제품 모니터링, 제로 슈거(Zero-sugar) 소재 및 대체 감미료 연구 |
| **품질 및 리스크관리** | 가속 실험: 고온(35~45°C)에서 보관하며 유통기한 경과에 따른 품질 변화 선제적 확인 |
""")

        # ── 항목이 많고 어렵다는 의견이 있어 보강한 두 가지 안내 ──
        with st.expander("❓ 항목이 많은데 다 채워야 하나요? — 항목별로 AI 답변이 어떻게 달라지는지"):
            st.markdown("""
| 항목 | AI 답변에 미치는 영향 |
|---|---|
| 이름 · 연령 · 성별 · 출신지 | 말투와 시점만 잡아줍니다. **기술적 답변의 품질에는 영향이 거의 없습니다.** |
| 근무경력 | 답변의 깊이가 달라집니다 (설명 위주 ↔ 시니어의 판단 위주) |
| 관심 제품 유형 | AI가 예로 드는 제품군이 내 분야로 좁혀집니다 |
| **보유기술 · 식품공정 지식 · 식품배합비 이론** | **영향이 가장 큽니다.** AI가 사용할 전문 용어와 검토 기준이 이 세 항목에서 정해집니다 |
| 업무 환경 (보유 장비) | 답변에 실제 측정 지표와 단위(Brix·pH·Aw 등)가 들어옵니다 |
| 품질 및 리스크관리 | 답변에 유통·보관 리스크 검토가 자동으로 따라붙습니다 |
| 연구개발 포인트 | 맛과 원가처럼 서로 부딪히는 상황에서 AI가 무엇을 우선할지 기준이 됩니다 |
""")
            st.caption(
                "정리하면 — 신상 정보는 몰입용이고, 결과를 실제로 바꾸는 것은 기술·공정·판단 기준 항목입니다. "
                "이 항목들을 비워두면 AI 답변이 일반론으로 흐르기 때문에, 어려워 보여도 채우는 편이 좋습니다."
            )

        with st.expander("🔄 음료 분야가 아니라면? — 같은 항목을 내 분야 말로 바꿔 적는 법"):
            st.caption(
                "이 교육의 실습 주제는 음료개발이므로 예시는 음료 기준입니다. "
                "아래는 같은 항목을 다른 분야에서 어떻게 적는지 대조한 표로, 항목의 의미를 잡는 데 참고하세요. "
                "(예시 테이블의 '관심 음료 유형'은 작성 화면에서 '관심 제품 유형' 항목입니다.)"
            )

            _EX_BASE = [
                ("관심 제품 유형", "커피(추출), 차(Tea), 유음료, 기능성 음료, 탄산음료"),
                ("보유기술", "배합 최적화, 감미료·산미료 밸런싱, 향료 사용 경험"),
                ("식품공정 지식", "HTST·UHT·레토르트 등 공정별 맛 변화 예측"),
                ("식품배합비 이론", "맛 보존기술, 층 분리(침전) 제어, 유화 안정성"),
                ("업무 환경 (장비)", "당도계(Brix), 산도계(pH), 색차계, 가속 가혹 실험기, 점도계"),
                ("품질 및 리스크관리", "가속 실험(35~45°C)으로 유통기한 경과 품질 변화 확인"),
                ("연구개발 포인트", "첫 병과 유통기한 마지막 날의 맛이 동일해야 한다"),
            ]
            _CONV = {
                "🍪 제과·스낵": [
                    "비스킷·쿠키, 스낵, 시즈닝 스낵, 한정판 플레이버",
                    "팽화·압출 공정 설계, 유지 산화 제어, 코팅·시즈닝 배합 최적화",
                    "팽화·압출(Extrusion), 건조 조건 설계, 유탕 온도·시간 최적화",
                    "텍스처 설계(바삭함·쫄깃함), 유지 산화 제어, 오일 흡수율 제어",
                    "수분활성도계(Aw), 텍스처 분석기, 색차계, 유탕 시험기",
                    "산가·과산화물가 가속 실험, 수분 흡수율 테스트로 눅눅해짐 확인",
                    "한 번 뜯으면 멈출 수 없는 텍스처와 향미의 조합",
                ],
                "🥛 유제품": [
                    "요거트, 발효유, 가공유, 치즈, 식물성 대체유",
                    "발효 스타터 배합, 점도·조직감 제어, 산도 관리",
                    "HTST 살균, UHT 초고온처리, 균질화, 요거트 발효 공정 최적화",
                    "유단백 응고 제어, 산도·점도 균형, 유화 안정성",
                    "점도계, 산도계(pH), 유지방 측정기, 균질기, 발효 인큐베이터",
                    "유산균 생균 수 모니터링, 냉장 유통 중 점도 변화·유청 분리 예방",
                    "한 스푼 뜰 때의 농도와 산미 밸런스가 재구매를 결정한다",
                ],
                "🍱 HMR·간편식": [
                    "냉동 도시락, 밀키트, 레토르트 국·탕, 냉동 면·밥",
                    "레토르트 공정 설계, 냉동·냉장 병용 유통 설계, 조리편의성 최적화",
                    "레토르트 살균, 냉동·냉장 병용 유통, 전자레인지 재가열 최적화",
                    "복합 식감(바삭+촉촉) 유지, 냉동 후 복원성, 전분 노화 제어",
                    "레토르트 시험기, 텍스처 분석기, 전자레인지 균일 가열 측정 장비, pH·수분활성도계",
                    "CCP 기반 위해요소 관리, 냉동·냉장 유통 가속 실험으로 유통기한 설정",
                    "전자레인지 3분 후에도 막 조리한 것 같은 식감과 온도 균일성",
                ],
                "🥗 프레시푸드·샐러드": [
                    "편의점 샐러드, 컷팅 채소·과일, 신선 도시락, 그레인 볼",
                    "MA포장 설계, 갈변 방지 처리, 콜드체인 유지, 관능 신선도 평가",
                    "MA포장 가스 조성 설계, 갈변 방지 처리(pH·항산화제), 콜드체인 관리",
                    "수확 후 관리(Post-harvest), 드레싱 pH·산도 조절, 혼합 샐러드 유통 안정성",
                    "가스 분석기(O₂/CO₂), 색차계, 텍스처 분석기, 미생물 배양기, 냉장 유통 시뮬레이터",
                    "미생물 억제 조건 설계, 콜드체인 온도 이탈 시 품질 변화 예측",
                    "유통기한 D-1일에도 '갓 만든 것처럼' 느껴지는 색·향·식감",
                ],
            }

            _conv_pick = st.pills(
                "분야 선택", list(_CONV.keys()), default="🍪 제과·스낵",
                key="ex_conv_field", label_visibility="collapsed",
            )
            _conv_pick = _conv_pick or "🍪 제과·스낵"
            _mine = _CONV[_conv_pick]
            _tbl = ["| 항목 | 🥤 음료 (예시 원본) | %s (내 분야로 바꾸면) |" % _conv_pick, "|---|---|---|"]
            for (_label, _bev), _own in zip(_EX_BASE, _mine):
                _tbl.append("| **%s** | %s | %s |" % (_label, _bev, _own))
            st.markdown("\n".join(_tbl))

        st.info(
            "💡 **직접 다 쓰지 않아도 됩니다.** 다음 탭 '연구원 페르소나 만들기'에서 본인 분야를 고르면 "
            "위 항목이 그 분야 기준으로 자동 입력됩니다. 자동 입력된 내용을 읽어보고 "
            "관심사·연구개발 포인트 정도만 본인 경험으로 고쳐도 페르소나로 충분히 작동합니다."
        )

        st.markdown("##### STEP 2. 테이블을 복사해 AI 대화창에 붙여넣기")
        show_example("""⚠️ [세션 전용 설정] 아래 내용을 ChatGPT 영구 메모리(장기 기억)에 저장하지 마세요. 이 대화 안에서만 임시로 적용합니다.

음료개발연구원의 페르소나를 아래의 정보를 적용해서 작성해
[페르소나 엑셀 데이터 붙여넣기]

이름: 한서윤 / 연령: 35세 / 직장: 네추럴 랩 베버리지 / 직무: 음료개발연구원 / 성별: 여성 / 출신지: 대전광역시
관심 음료 유형: 커피(추출), 차(Tea), 유음료, 기능성 음료(에너지/단백질), 탄산음료
보유기술: 배합 최적화기술, 감미료/산미료 밸런싱, 원부재료·향료 경험 풍부
식품공정 지식: HTST·UHT·레토르트 등 공정별 맛 변화 예측 능력
식품배합비 이론: 맛 보존기술, 층 분리(침전) 제어, 유화 안정성(Emulsion Stability) 기술
연구개발 포인트: 재현성 중시 — 첫 병과 유통기한 마지막 날의 맛이 동일해야 한다
업무 환경: 당도계(Brix), 산도계(pH), 색차계, 가속 가혹 실험기(Incubator), 점도계
근무경력: 헬스케어 음료 스타트업 5년 + 식품 음료 대기업 중견 연구원 15년 시니어
관심사: 편의점(CVS) 신제품 모니터링, 제로슈거 소재 및 대체 감미료 연구
품질 및 리스크관리: 가속 실험(35~45°C)으로 유통기한 경과에 따른 품질 변화 선제적 확인

[이 대화 전용 역할 지정] 지금부터 음료연구원은 이 페르소나를 적용합니다.

[출력 형식 — 아래 순서와 번호를 그대로 지켜 작성]
1. 페르소나 형성 결과  ★가장 중요
   - 위 정보가 페르소나에 어떻게 반영되었는지 항목별로 정리
   - 이 연구원이 어떤 관점과 판단 기준으로 일하는지 3~5줄로 서술
2. 적용 확인 답변
   - 확인 질문: 저당 탄산음료를 최근 유행 플레이버에 적용했을 때, 단맛을 어느 정도가 좋을까
   - 위 페르소나 입장에서 5줄 이내로 짧게 답변

※ 1번을 먼저, 가장 충실하게 작성하세요. 2번은 페르소나가 제대로 적용됐는지 점검하는 용도이므로 짧게 답합니다.""")

        st.markdown("---")
        st.markdown("#### 마케터 페르소나 예시 — 김지안 (브랜드마케팅 매니저)")
        show_example("""⚠️ [세션 전용 설정] 아래 내용을 ChatGPT 영구 메모리(장기 기억)에 저장하지 마세요. 이 대화 안에서만 임시로 적용합니다.

RTD 음료 마케터의 페르소나를 아래의 정보를 적용해서 작성해
[페르소나 엑셀 데이터 붙여넣기]

이름: 김지안 / 연령: 34세 / 직장: 네추럴 랩 베버리지 / 직무: 브랜드마케팅 매니저 / 성별: 여성 / 출신지: 서울특별시
관심 음료 유형: 제로 탄산음료, 기능성 RTD, 과일 블렌딩 음료, 시즌 한정 음료, 프리미엄 티 음료
보유기술: 브랜드 전략 수립, 신제품 컨셉 도출, 소비자 인사이트 분석, 데이터 기반 마케팅, 채널별 판매전략, 캠페인 운영
시장 분석력: 국내외 식품음료 시장 트렌드에 대한 높은 이해도
상품기획자 마인드: 컨셉·타깃·가격·채널·패키지·커뮤니케이션 통합 관점
마케팅 포인트: 시장성, 차별성, 화제성, 소비자 공감, 브랜드 확장성, 시즌성 및 트렌드 반영
업무 환경: 판매 데이터 모니터링, 경쟁사 신제품 벤치마킹, 편의점·대형마트 조사, SNS 분석, FGI 및 설문조사
근무경력: 식음료 대기업 및 음료 브랜드사 마케팅 경력 8년

[이 대화 전용 역할 지정] 지금부터 음료마케터는 이 페르소나를 적용합니다.

[출력 형식 — 아래 순서와 번호를 그대로 지켜 작성]
1. 페르소나 형성 결과  ★가장 중요
   - 위 정보가 페르소나에 어떻게 반영되었는지 항목별로 정리
   - 이 마케터가 어떤 관점과 판단 기준으로 일하는지 3~5줄로 서술
2. 적용 확인 답변
   - 확인 질문: 저당 탄산음료를 최근 유행 플레이버에 적용한다면, 어떤 구성과 패키지?
   - 위 페르소나 입장에서 5줄 이내로 짧게 답변

※ 1번을 먼저, 가장 충실하게 작성하세요. 2번은 페르소나가 제대로 적용됐는지 점검하는 용도이므로 짧게 답합니다.""")

    # ── 직무 테마 프리셋 ──────────────────────────────────────
    RESEARCHER_PRESETS = {
        "🥤 탄산음료 개발연구원": {
            "이름": "한서윤", "연령": "35세", "직장": "네추럴 랩 베버리지", "직무": "탄산음료 개발연구원", "성별": "여성",
            "근무경력": "헬스케어 음료 스타트업 5년 + 식품 음료 대기업 탄산음료 개발 15년 시니어",
            "관심 제품 유형": "제로슈거 탄산, 스파클링 과즙음료, 토닉·소다류, 시즌 한정 탄산",
            "보유기술": "탄산 가스압(GV) 설계, 감미료·산미료 밸런싱, 충전 후 탄산 유지 배합 기술",
            "식품공정 지식": "카보네이션(탄산 주입), 프리믹스·포스트믹스, 충전 시 가스 손실 제어",
            "식품배합비 이론": "감미도 환산, 당산비(Brix/Acid ratio) 밸런스, 탄산 자극과 단맛 상쇄 관계",
            "직무 역량": "가스압별 관능 변화 예측 / 제로슈거 감미료 조합 설계 / 충전 후 품질 안정성 확보",
            "업무 환경": "당도계(Brix), 산도계(pH), 가스볼륨 측정기, 가속 가혹 실험기(Incubator), 색차계",
            "관심사": "편의점(CVS) 제로 탄산 신제품 모니터링, 대체 감미료 조합 연구",
            "품질 및 리스크관리": "가속 실험(35~45°C)으로 가스압 저하·이취 발생 시점 선제적 확인",
            "연구개발 포인트": "공장에서 나온 첫 캔과 유통기한 마지막 날의 탄산감이 동일해야 한다 (재현성 중시)",
            "확인 질문": "저당 탄산음료를 최근 유행 플레이버에 적용했을 때, 단맛을 어느 정도가 좋을까",
        },
        "💪 기능성음료 개발연구원": {
            "이름": "정도현", "연령": "38세", "직장": "바이탈핏 뉴트리션", "직무": "기능성음료 개발연구원", "성별": "남성",
            "근무경력": "건강기능식품 원료사 4년 + 기능성 RTD 음료 개발 11년",
            "관심 제품 유형": "단백질 음료, 전해질·이온음료, 에너지드링크, 비타민 워터",
            "보유기술": "고단백 음료 침전 제어, 기능성 원료 안정화, 이미·이취 마스킹 배합",
            "식품공정 지식": "UHT 살균 시 단백질 변성 제어, 무균충전, 균질(호모게나이징) 압력 설계",
            "식품배합비 이론": "단백질 등전점과 pH 설계, 아미노산 쓴맛 마스킹, 전해질 삼투압 밸런스",
            "직무 역량": "기능성 표시 가능 함량 설계 / 원료 간 상호작용 예측 / 섭취 후 체감 설계",
            "업무 환경": "당도계(Brix), 산도계(pH), 점도계, 입도분석기, 가속 가혹 실험기(Incubator)",
            "관심사": "단백질·전해질 음료 신제품 모니터링, 기능성 원료 인허가 동향",
            "품질 및 리스크관리": "보관 중 단백질 응집·침전 여부와 기능성 성분 잔존율 추적",
            "연구개발 포인트": "효능은 과학으로 증명하고, 맛은 매일 마시고 싶게 만들어야 한다",
            "확인 질문": "단백질 20g 음료에서 특유의 이취와 텁텁함을 줄이려면 어떤 배합이 좋을까",
        },
        "🌱 식물성·과채음료 개발연구원": {
            "이름": "윤가람", "연령": "33세", "직장": "그린베이스 푸드", "직무": "식물성·과채음료 개발연구원", "성별": "여성",
            "근무경력": "과채주스 제조사 3년 + 식물성 음료(두유·귀리·아몬드) 개발 9년",
            "관심 제품 유형": "귀리·아몬드 음료, 착즙주스, 과채 블렌딩 음료, 콤부차",
            "보유기술": "식물성 단백질 분산·유화 안정화, 착즙 원물 색·향 보존, 무첨가 컨셉 배합",
            "식품공정 지식": "HPP(초고압), HTST·UHT 살균에 따른 원물 향미 변화, 효소 처리(당화) 공정",
            "식품배합비 이론": "식물성 유화 안정성, 원물 당·산 밸런스, 침전·층분리 제어",
            "직무 역량": "원물 시즌별 품질 편차 보정 / 클린라벨 배합 설계 / 식물성 이취 저감",
            "업무 환경": "당도계(Brix), 산도계(pH), 점도계, 색차계, 원심분리기",
            "관심사": "비건·클린라벨 신제품 모니터링, 대체유 원료 및 국산 원물 소싱",
            "품질 및 리스크관리": "유통 중 층분리·갈변·이취 발생 시점을 가속 실험으로 사전 확인",
            "연구개발 포인트": "원물 그대로의 맛을 첨가물 없이 유통기한 끝까지 유지한다",
            "확인 질문": "귀리 음료의 텁텁함을 줄이면서 단맛을 원물로만 내려면 어떻게 배합할까",
        },
        "🍪 제과·스낵 개발연구원": {
            "이름": "박민준", "연령": "40세", "직장": "스낵코리아", "직무": "제과·스낵 개발연구원", "성별": "남성",
            "근무경력": "제과 대기업 R&D 18년, 신제품 출시 경험 30건 이상",
            "관심 제품 유형": "프리미엄 스낵, 글루텐프리 과자, 기능성 간식, 저칼로리 간식, 시즌 한정 스낵",
            "보유기술": "팽화·압출 공정 설계, 유지 산화 제어, 코팅·시즈닝 배합 최적화",
            "식품공정 지식": "팽화·압출(Extrusion) 공정, 건조 조건 설계, 유탕 처리(Deep-frying) 온도·시간 최적화",
            "식품배합비 이론": "텍스처 설계(바삭함·쫄깃함), 유지 산화 제어, 코팅·시즈닝 배합 최적화, 오일 흡수율 제어",
            "직무 역량": "스낵 텍스처 설계(바삭함·쫄깃함) / 유통기한 가속 실험 / 소재별 오일 흡수율 제어 기술",
            "업무 환경": "수분활성도계(Aw), 텍스처 분석기(Texture Analyzer), 색차계, 유탕 시험기",
            "관심사": "편의점 스낵 신제품 벤치마킹, 글루텐프리·저칼로리 소재 연구, 해외 한정판 스낵 트렌드",
            "품질 및 리스크관리": "유지 산화(산가·과산화물가) 가속 실험, 수분 흡수율 테스트로 유통 중 품질 변화 확인",
            "연구개발 포인트": "한 번 뜯으면 멈출 수 없는 텍스처와 향미의 조합 — 중독성 있는 맛 설계",
            "확인 질문": "저칼로리 쌀과자에 매콤달콤 시즈닝을 적용한다면 소재 비율을 어떻게 잡을까",
        },
        "💊 건강기능식품 연구원": {
            "이름": "이지현", "연령": "38세", "직장": "헬스바이오텍", "직무": "건강기능식품 개발연구원", "성별": "여성",
            "근무경력": "기능성 소재 연구 10년, 식약처 개별인정형 인허가 경험 풍부",
            "관심 제품 유형": "프로바이오틱스 음료, 단백질 보충제, 비타민 음료, 식이섬유 음료, 콜라겐 제품",
            "보유기술": "기능성 원료 배합, 안정화 기술(캡슐화·코팅), 관능평가 설계",
            "식품공정 지식": "캡슐화(Encapsulation), 코팅 공정, 냉동건조(Freeze-drying), 분무건조(Spray-drying) 기술",
            "식품배합비 이론": "기능성 원료 안정화, 성분 간 상호작용(Interaction) 최소화, 생체이용률(Bioavailability) 최적화",
            "직무 역량": "개별인정형 원료 인허가 프로세스 / 생리활성 기전 분석 / 임상 데이터 해석",
            "업무 환경": "HPLC(고성능 액체 크로마토그래피), 분광광도계, 세균 배양기, 캡슐 충전기",
            "관심사": "개별인정형 원료 신규 동향, 프로바이오틱스 균주 연구, 건기식 규제 변화 모니터링",
            "품질 및 리스크관리": "유산균 생균 수(CFU) 보장, 흡습성 관리, 가속 안정성 시험으로 기능성 성분 함량 유지 확인",
            "연구개발 포인트": "효능은 과학으로 증명하고, 맛은 소비자가 매일 먹고 싶게 만들어야 한다",
            "확인 질문": "락토바실러스 함유 음료에서 유통 중 유산균 생존율을 높이는 방법은?",
        },
        "🥛 유제품 개발연구원": {
            "이름": "최수정", "연령": "33세", "직장": "프레시데어리", "직무": "유제품 개발연구원", "성별": "여성",
            "근무경력": "유가공 전문 연구소 7년, 발효유·치즈·버터 개발 경험",
            "관심 제품 유형": "그릭요거트, 발효유, 식물성 대체유, 치즈, 고단백 유음료",
            "보유기술": "발효 스타터 배합, 점도·조직감 제어, 산도 관리, UHT 살균 공정 설계",
            "식품공정 지식": "HTST 살균, UHT 초고온처리, 균질화(Homogenization), 요거트 발효 공정 최적화",
            "식품배합비 이론": "유단백 응고 제어, 산도·점도 균형, 유화 안정성, 식물성 대체유 텍스처 설계",
            "직무 역량": "유산균 균주 선발 및 발효 최적화 / 저온 유통 조건 설계 / 식물성 대체유 유화 안정성 기술",
            "업무 환경": "점도계(Viscometer), 산도계(pH), 유지방 측정기, 균질기(Homogenizer), 발효 인큐베이터",
            "관심사": "식물성 대체유 시장 동향, 그릭요거트 원료 트렌드, 유청(Whey) 단백질 활용 연구",
            "품질 및 리스크관리": "유산균 생균 수 모니터링, 냉장 유통 중 점도 변화 및 유청 분리 예방 관리",
            "연구개발 포인트": "소비자가 한 스푼 뜰 때의 농도와 산미 밸런스가 재구매를 결정한다",
            "확인 질문": "그릭요거트 제형에서 유청 분리 없이 단백질 함량을 20% 높이는 방법은?",
        },
        "🧊 냉동식품 개발연구원": {
            "이름": "서지훈", "연령": "41세", "직장": "콜드테이블푸드", "직무": "냉동식품 개발연구원", "성별": "남성",
            "근무경력": "냉동만두·냉동피자 제조사 6년 + 냉동 HMR 개발 12년",
            "관심 제품 유형": "냉동만두, 냉동피자, 냉동밥·볶음밥, 에어프라이어 전용 스낵",
            "보유기술": "급속동결(IQF) 조건 설계, 해동 복원성 배합, 빙결정 크기 제어",
            "식품공정 지식": "급속동결(IQF)·터널프리저, 예열·증숙 공정, 콜드체인 유통 설계",
            "식품배합비 이론": "동결 시 수분 이동과 빙결정 제어, 전분 노화(Retrogradation) 지연, 해동 후 조직감 유지",
            "직무 역량": "냉동-해동 사이클별 품질 변화 예측 / 에어프라이어·전자레인지 조리 편차 보정 / 동결점 강하 설계",
            "업무 환경": "급속동결기, 수분활성도계(Aw), 텍스처 분석기, 동결점 측정기, 온도 로거",
            "관심사": "에어프라이어 전용 신제품 모니터링, 냉동 HMR 프리미엄화 동향",
            "품질 및 리스크관리": "냉동-해동 반복(Freeze-Thaw) 시험으로 드립·조직 붕괴 시점 확인, 콜드체인 이탈 대응",
            "연구개발 포인트": "냉동실에서 3개월 뒤 꺼내도 갓 만든 것과 같은 식감이어야 한다",
            "확인 질문": "냉동만두 피가 해동 후 질겨지는 문제를 배합으로 줄이려면 어떻게 접근할까",
        },
        "🍱 HMR·간편식 개발연구원": {
            "이름": "강태양", "연령": "36세", "직장": "이지밀푸드", "직무": "HMR 개발연구원", "성별": "남성",
            "근무경력": "냉동·냉장 간편식 R&D 9년, 밀키트·컵밥·도시락 출시 다수",
            "관심 제품 유형": "냉동 밀키트, 컵국·컵밥, 프리미엄 도시락, 냉장 볶음밥, 식물성 HMR",
            "보유기술": "레토르트 공정 설계, 냉동·냉장 병용 유통 설계, 조리편의성 최적화",
            "식품공정 지식": "레토르트 살균, 냉동·냉장 병용 유통 공정, 전자레인지 재가열 최적화 설계",
            "식품배합비 이론": "복합 식감(바삭+촉촉) 유지 설계, 냉동 후 복원성, 전분 노화(Retrogradation) 제어",
            "직무 역량": "CCP(중요관리점) 기반 위해요소 분석 / 복합 식감(바삭+촉촉) 유지 설계 / 가열 후 품질 균일성 확보",
            "업무 환경": "레토르트 시험기, 텍스처 분석기, 전자레인지 균일 가열 측정 장비, pH·수분활성도계",
            "관심사": "1인 가구 간편식 트렌드, 편의점 도시락 벤치마킹, 식물성 HMR 소재 연구",
            "품질 및 리스크관리": "CCP 기반 위해요소 관리, 냉동·냉장 유통 중 품질 변화 가속 실험으로 유통기한 설정",
            "연구개발 포인트": "전자레인지 3분 후에도 식당에서 막 나온 것처럼 느껴지는 식감과 온도 균일성이 목표",
            "확인 질문": "냉동 국물요리 HMR에서 해동 후 국물 탁해짐 없이 맑은 색을 유지하는 방법은?",
        },
        "🫙 소스·조미료 개발연구원": {
            "이름": "오민서", "연령": "32세", "직장": "소스랩코리아", "직무": "소스·조미료 개발연구원", "성별": "여성",
            "근무경력": "소스·드레싱·양념류 전문 R&D 6년, 수출용 K-소스 개발 경험",
            "관심 제품 유형": "K-소스(불닭·갈비·불고기), 드레싱, 디핑소스, 발효 양념장, 저염·제로슈거 소스",
            "보유기술": "발효 소스 숙성 공정 설계, 향미 균형(매운맛·단맛·감칠맛) 배합, 점도·색도 안정화",
            "식품공정 지식": "Maillard 반응 제어, 발효 소스 숙성 공정, 산성 소스 vs 중성 소스 살균 조건 설계",
            "식품배합비 이론": "향미 균형(매운맛·단맛·감칠맛) 배합, 점도·색도 안정화, 산화 방지제 최소화 기술",
            "직무 역량": "Maillard 반응 제어로 가열 풍미 설계 / 산화 방지제 최소화 조건에서 색택 유지 / 글로벌 수출 규격 대응",
            "업무 환경": "향미 측정(GC-MS), 점도계, 색차계(CIE Lab), pH·산도 측정기, 살균 시험기",
            "관심사": "K-소스 글로벌 트렌드, 저염·저당 소스 소재 연구, 비건·할랄 인증 시장 동향",
            "품질 및 리스크관리": "산화 안정성(산가) 가속 실험, 색택 유지 조건 테스트, 이물 혼입 방지 HACCP 관리",
            "연구개발 포인트": "소스는 요리의 마지막 1%를 결정한다 — 가열 전·후 풍미 변화까지 설계해야 진짜 레시피",
            "확인 질문": "불닭 계열 소스를 서양 소비자용으로 순하게 조절할 때 풍미를 살리는 핵심 소재는?",
        },
        "🥗 프레시푸드·샐러드 개발연구원": {
            "이름": "임하은", "연령": "29세", "직장": "프레시팜푸드", "직무": "프레시푸드 개발연구원", "성별": "여성",
            "근무경력": "신선 편의식품 R&D 4년, 편의점·온라인 샐러드·컷팅 채소 개발 경험",
            "관심 제품 유형": "편의점 샐러드, 컷팅 채소·과일, 신선 도시락, 그레인 볼, 비건 편의식",
            "보유기술": "MA포장(Modified Atmosphere) 설계, 갈변 방지 처리, 콜드체인 유지, 관능 신선도 평가",
            "식품공정 지식": "MA포장(Modified Atmosphere Packaging) 가스 조성 설계, 갈변 방지 처리(pH 조절·항산화제), 콜드체인 관리",
            "식품배합비 이론": "신선 농산물 수확 후 관리(Post-harvest), 드레싱 pH·산도 조절, 혼합 샐러드 유통 안정성",
            "직무 역량": "신선 농산물 수확 후 품질 관리 / 미생물 억제 조건 설계 / 소비자 신선도 인식 기반 패키지 개발",
            "업무 환경": "가스 분석기(O₂/CO₂), 색차계, 텍스처 분석기, 미생물 배양기, 냉장 유통 시뮬레이터",
            "관심사": "편의점 샐러드 신제품 모니터링, 비건 신선 간편식 소재, 산지 농산물 직소싱 트렌드",
            "품질 및 리스크관리": "미생물 억제 조건 설계, 색·향·식감 신선도 평가, 콜드체인 온도 이탈 시 품질 변화 예측",
            "연구개발 포인트": "유통기한 D-1일에도 소비자가 '갓 만든 것처럼' 느끼는 색·향·식감이 신선식품의 승패를 가른다",
            "확인 질문": "컷팅 사과의 갈변을 최소화하면서 식품첨가물 표시를 줄이는 방법은?",
        },
        "🍜 면류·파스타 개발연구원": {
            "이름": "윤재원", "연령": "41세", "직장": "누들하우스", "직무": "면류 개발연구원", "성별": "남성",
            "근무경력": "건면·생면·냉동면 R&D 16년, 라면·파스타·쌀국수 신제품 출시 경험",
            "관심 제품 유형": "건면(라면·소면), 생면, 냉동면, 쌀국수, 저탄수 면류, 글루텐프리 파스타",
            "보유기술": "면 반죽 수분·글루텐 조절, 압연·압출 공정 설계, 건조 조건 최적화, 복원성 설계",
            "식품공정 지식": "압연·압출 공정(Rolling/Extrusion), 건조 조건(열풍·동결 건조), 즉석면 유탕 처리 공정",
            "식품배합비 이론": "전분 호화도 조절, 글루텐 네트워크 형성, 면발 탄력(Springiness) 및 복원성 설계",
            "직무 역량": "전분 호화도 조절에 따른 면발 탄력 제어 / 스프·소스와의 매칭 최적화 / 고단백·저탄수 면류 조직 설계",
            "업무 환경": "텍스처 분석기, 점도계, 수분 측정기, 색차계, 조리 후 면 복원 평가 장비",
            "관심사": "해외 면류 트렌드, 저탄수·글루텐프리 대체 소재 연구, K-라면 글로벌 소비 패턴 분석",
            "품질 및 리스크관리": "조리 후 식감 유지 시간 테스트, 건면 수분 함량 관리, 즉석면 유탕 후 산화 안정성 평가",
            "연구개발 포인트": "면발은 물을 만나는 순간부터 시간이 흐른다 — 소비자가 한 젓가락 들었을 때 최고점을 설계해야 한다",
            "확인 질문": "저탄수 곤약면과 밀면을 블렌딩할 때 식감 이질감 없이 탄력을 유지하는 비율은?",
        },
        "🥩 축산·육가공 개발연구원": {
            "이름": "한동현", "연령": "44세", "직장": "미트랩코리아", "직무": "육가공품 개발연구원", "성별": "남성",
            "근무경력": "햄·소시지·육포·대체육 R&D 19년, 수출형 육가공 제품 개발 경험",
            "관심 제품 유형": "프리미엄 햄·소시지, 육포·저키, 식물성 대체육, 냉동 패티, 고단백 가공육",
            "보유기술": "염지 배합 최적화, 훈연·가열 공정 설계, 결착력(보수력) 향상, 식물성 단백질 조직화(TVP)",
            "식품공정 지식": "염지(Curing) 공정, 훈연·가열 처리, 결착제 배합, 식물성 단백질(TVP) 조직화 공정",
            "식품배합비 이론": "결착력(보수력) 향상 배합, 아질산염 저감화, 식물성 단백질 식감·향미 재현 기술",
            "직무 역량": "HACCP 기반 위해요소 관리 / 아질산염 저감화 기술 / 대체육 식감·향미 재현 기술",
            "업무 환경": "텍스처 분석기, 색차계, pH계, 훈연기, 레오미터(Rheometer, 보수력 측정)",
            "관심사": "대체육 시장 동향, 아질산염 대체 소재 연구, 프리미엄 육가공 원육 트렌드",
            "품질 및 리스크관리": "아질산염 잔류량 관리, HACCP 기반 위해요소 분석, 냉장·냉동 유통 중 색택 변화 모니터링",
            "연구개발 포인트": "고기의 맛은 근육·지방·수분의 비율이 아니라 열을 가했을 때 벌어지는 반응의 총합이다",
            "확인 질문": "식물성 대체육 패티에서 가열 시 육즙감(juiciness)을 재현하는 핵심 소재 조합은?",
        },
    }

    MARKETER_PRESETS = {
        "🧃 음료 브랜드마케터": {
            "이름": "김지안", "연령": "34세", "직장": "네추럴 랩 베버리지", "직무": "브랜드마케팅 매니저", "성별": "여성",
            "근무경력": "식음료 대기업 및 음료 브랜드사 마케팅 경력 8년",
            "관심 제품 유형": "제로 탄산음료, 기능성 RTD, 과일 블렌딩 음료, 시즌 한정 음료, 프리미엄 티 음료",
            "보유기술": "브랜드 전략 수립, 신제품 컨셉 도출, 소비자 인사이트 분석, 데이터 기반 마케팅, 채널별 판매전략 기획",
            "직무 역량": "국내외 식품음료 시장 트렌드 분석 / 컨셉·타깃·가격·채널·패키지·커뮤니케이션 통합 관점",
            "시장 분석": "닐슨·칸타 음료 카테고리 데이터 / 편의점 POS 데이터 / 소셜 리스닝 기반 트렌드 포착",
            "채널 전략": "편의점(CVS) 신제품 입점 기획 / 대형마트 시즌 기획전 / D2C 구독 모델 및 온라인 퍼포먼스 마케팅",
            "마케팅 포인트": "시장성, 차별성, 화제성, 소비자 공감, 브랜드 확장성, 시즌성 및 트렌드 반영",
            "확인 질문": "저당 탄산음료를 최근 유행 플레이버에 적용한다면, 어떤 구성과 패키지?",
        },
        "💊 건강기능식품 마케터": {
            "이름": "정호영", "연령": "37세", "직장": "헬스바이오텍", "직무": "건강기능식품 마케팅 팀장", "성별": "남성",
            "근무경력": "헬스케어·건기식 마케팅 12년, D2C 온라인 채널 구축 경험",
            "관심 제품 유형": "단백질 보충제, 비타민 음료, 프로바이오틱스 제품, 콜라겐 드링크, 에너지 젤리",
            "보유기술": "퍼포먼스 마케팅, 인플루언서 협업, 구독모델 설계, 성분 스토리텔링, 임상 데이터 마케팅",
            "직무 역량": "효능 기반 마케팅 커뮤니케이션 / 규제 범위 내 광고문구 설계 / 리뷰·후기 마케팅",
            "시장 분석": "건기식 시장 규모 및 카테고리별 성장률 / 소비자 건강 관심 트렌드 (GNB·아미노산·프로바이오틱스) / 경쟁사 클레임 비교",
            "채널 전략": "쿠팡·네이버쇼핑 퍼포먼스 마케팅 / 유튜브·인스타 인플루언서 협업 / 구독 D2C 모델 설계",
            "마케팅 포인트": "과학적 근거, 소비자 체험 후기, 성분 투명성, 구독 유지율, 건강 루틴 연계",
            "확인 질문": "프로바이오틱스 드링크를 MZ 세대에게 마케팅한다면 어떤 채널과 메시지 전략?",
        },
        "🍱 HMR·간편식 마케터": {
            "이름": "윤서연", "연령": "31세", "직장": "이지밀푸드", "직무": "HMR 상품기획 마케터", "성별": "여성",
            "근무경력": "HMR·밀키트 전문 마케팅 5년, 편의점 채널 신제품 기획 경험",
            "관심 제품 유형": "밀키트, 냉동 간편식, 컵국·컵밥, 프리미엄 도시락, 식물성 HMR",
            "보유기술": "편의점·대형마트 MD 협업, 패키지 기획, 레시피 마케팅, 시즌 한정 기획",
            "직무 역량": "1인 가구 식생활 트렌드 분석 / 유통 채널별 가격·용량 전략 / 간편식 패키지 UX 설계",
            "시장 분석": "편의점·대형마트 도시락·간편식 POS 데이터 / 1인 가구 식생활 패널 조사 / 경쟁 밀키트 플랫폼 모니터링",
            "채널 전략": "편의점(GS25·CU·세븐일레븐) 채널별 입점 기획 / 마켓컬리·쿠팡이츠 온라인 채널 / SNS 레시피 콘텐츠",
            "마케팅 포인트": "간편성, 맛 퀄리티, 1인 가구 최적화, 가성비, SNS 비주얼, 조리 시간 경쟁력",
            "확인 질문": "1인용 프리미엄 냉동 간편식을 편의점에서 출시한다면 어떤 가격대와 패키지 전략?",
        },
        "🍪 제과·스낵 마케터": {
            "이름": "이수민", "연령": "33세", "직장": "스낵코리아 마케팅", "직무": "제과·스낵 브랜드 마케터", "성별": "여성",
            "근무경력": "제과 대기업 마케팅 7년, 편의점 채널 신제품 기획 및 한정판 캠페인 경험",
            "관심 제품 유형": "프리미엄 스낵, 글루텐프리 과자, 기능성 간식, 시즌 한정 스낵, 저칼로리 간식",
            "보유기술": "편의점·마트 MD 협업, 패키지 디자인 기획, SNS 바이럴 마케팅, 시즌 한정 캠페인 운영",
            "직무 역량": "스낵 카테고리 시장 세분화 분석 / 가격대별 SKU 전략 / 플레이버·텍스처 소비자 조사 설계",
            "시장 분석": "편의점 스낵 카테고리 POS 데이터 / 해외 한정판 스낵 트렌드 벤치마킹 / SNS 스낵 챌린지 모니터링",
            "채널 전략": "편의점 한정판 입점 기획 / 다이소·온라인 스낵 판매 채널 확장 / 유튜브 먹방·리뷰 인플루언서 협업",
            "마케팅 포인트": "중독성 있는 플레이버, SNS 챌린지 유도, 한정판 희소성, 편의점 입점 전략, 가성비 vs 프리미엄 포지셔닝",
            "확인 질문": "저칼로리 쌀과자를 2030 여성 타깃으로 리런칭한다면 어떤 패키지와 채널 전략이 효과적일까?",
        },
        "🥛 유제품 마케터": {
            "이름": "박지현", "연령": "36세", "직장": "프레시데어리 마케팅팀", "직무": "유제품 카테고리 마케터", "성별": "여성",
            "근무경력": "유가공·유음료 브랜드 마케팅 10년, 편의점·온라인 신채널 개척 경험",
            "관심 제품 유형": "그릭요거트, 발효유, 식물성 대체유, 치즈, 고단백 유음료",
            "보유기술": "건강 유제품 컨셉 기획, 임상 데이터 기반 커뮤니케이션, 구독 D2C 모델, 비건 제품 포지셔닝",
            "직무 역량": "유제품 시장 세분화(기능성·맛·간편성) / 타깃별 건강 메시지 설계 / 채널 통합 전략",
            "시장 분석": "그릭요거트·단백질 음료 카테고리 성장률 / 식물성 대체유 소비자 전환율 / 편의점·대형마트 유제품 POS",
            "채널 전략": "편의점 냉장 코너 신제품 입점 / 헬스장·운동 커뮤니티 파트너십 / 유튜브·인스타 단백질 콘텐츠 협업",
            "마케팅 포인트": "건강 기능성, 단백질 함량 강조, 식물성 대체 트렌드, 구독 루틴 연계, 클린라벨",
            "확인 질문": "고단백 그릭요거트를 운동하는 MZ 세대에게 마케팅한다면 어떤 채널과 콘텐츠 전략을 쓸까?",
        },
        "🫙 소스·조미료 마케터": {
            "이름": "김태훈", "연령": "38세", "직장": "소스랩코리아 마케팅", "직무": "소스·조미료 브랜드 마케팅 팀장", "성별": "남성",
            "근무경력": "K-소스 및 조미료 브랜드 마케팅 12년, 해외 수출 브랜딩 및 현지화 경험",
            "관심 제품 유형": "K-소스(불닭·갈비·불고기), 드레싱, 디핑소스, 발효 양념장, 저염·제로슈거 소스",
            "보유기술": "글로벌 K-Food 브랜딩, 요리 콘텐츠 마케팅, 유튜브·쇼츠 레시피 협업, 수출용 패키지 현지화",
            "직무 역량": "매운맛 강도 세분화 포지셔닝 / 비건·할랄·글루텐프리 인증 마케팅 / 레시피 기반 소비자 교육 전략",
            "시장 분석": "K-소스 수출 국가별 매운맛 선호도 조사 / 국내 소스 카테고리 POS 데이터 / 할랄·비건 인증 시장 규모",
            "채널 전략": "아마존·라쿠텐 수출 판매 채널 / 국내 대형마트·편의점 소스 코너 입점 / 유튜브 해외 푸드 인플루언서 협업",
            "마케팅 포인트": "K-Food 글로벌 트렌드 활용, 요리 영상 바이럴, 맵기 단계 시리즈화, 편의성·간편 조리 어필",
            "확인 질문": "불닭 소스를 서양 소비자에게 수출할 때 어떤 매운맛 강도와 패키지 컨셉이 효과적일까?",
        },
        "🥗 프레시푸드·샐러드 마케터": {
            "이름": "임나은", "연령": "29세", "직장": "프레시팜푸드 마케팅", "직무": "신선식품 카테고리 마케터", "성별": "여성",
            "근무경력": "신선 편의식품 마케팅 4년, 편의점·쿠팡 로켓프레시 신제품 기획 경험",
            "관심 제품 유형": "편의점 샐러드, 컷팅 채소·과일, 신선 도시락, 그레인 볼, 비건 편의식",
            "보유기술": "신선도 강조 비주얼 마케팅, 건강 라이프스타일 콘텐츠 제작, 새벽배송 채널 기획",
            "직무 역량": "소비자 신선 인식 조사 설계 / 편의점 MD 협력 및 입점 기획 / 건강 식단 트렌드 분석",
            "시장 분석": "편의점 샐러드 카테고리 성장률 / 다이어트·헬시 이팅 소비자 패널 조사 / 새벽배송 신선식품 경쟁사 분석",
            "채널 전략": "편의점 냉장 코너 신제품 입점 기획 / 마켓컬리·쿠팡 로켓프레시 채널 / 인스타그램 다이어트 식단 인플루언서",
            "마케팅 포인트": "비주얼 신선감, 다이어트·건강 식단 연계, SNS 푸드 사진 유도, 빠른 시즌 대응, 클린 원료 강조",
            "확인 질문": "편의점 샐러드를 직장인 점심 대체식으로 포지셔닝한다면 어떤 가격대와 용량 전략이 맞을까?",
        },
        "🍜 면류·파스타 마케터": {
            "이름": "최준혁", "연령": "41세", "직장": "누들하우스 마케팅팀", "직무": "면류 카테고리 마케팅 팀장", "성별": "남성",
            "근무경력": "라면·파스타·쌀국수 브랜드 마케팅 15년, TV CF 및 디지털 통합 캠페인 기획 경험",
            "관심 제품 유형": "건면(라면·소면), 생면, 냉동면, 쌀국수, 저탄수 면류, 글루텐프리 파스타",
            "보유기술": "대형 캠페인 기획, 셀러브리티·인플루언서 협업, 오프라인 팝업 이벤트 운영, 리미티드 에디션 전략",
            "직무 역량": "면류 시장 세분화(간편·프리미엄·기능성) / 조리 시간 편의성 메시지 전략 / 수출 시장 현지화",
            "시장 분석": "라면·면류 카테고리 시장 규모 및 성장률 / 해외 수출 국가별 면류 선호 트렌드 / 저탄수 간편식 소비자 전환율",
            "채널 전략": "대형마트·편의점 면류 코너 입점 전략 / 아마존·아시안 마트 글로벌 채널 / 유튜브 먹방·레시피 인플루언서 협업",
            "마케팅 포인트": "조리 편의성·맛 퀄리티 균형, 한국 면 문화 글로벌화, 저탄수 건강 포지셔닝, 시즌 한정 플레이버 화제성",
            "확인 질문": "저탄수 곤약면을 다이어트 관심 3040 여성에게 마케팅한다면 어떤 채널과 콘텐츠가 효과적일까?",
        },
        "🥩 축산·육가공 마케터": {
            "이름": "한민재", "연령": "44세", "직장": "미트랩코리아 마케팅", "직무": "육가공품 브랜드 마케팅 팀장", "성별": "남성",
            "근무경력": "육가공·대체육 브랜드 마케팅 18년, 프리미엄 육가공 및 식물성 대체육 런칭 경험",
            "관심 제품 유형": "프리미엄 햄·소시지, 육포·저키, 식물성 대체육, 냉동 패티, 고단백 가공육",
            "보유기술": "단백질 기반 건강 마케팅, 식물성 대체육 소비자 교육, 그로서리 채널 전략, B2B 식자재 마케팅",
            "직무 역량": "육가공 카테고리 가격 전략 / 프리미엄 vs 가성비 포지셔닝 / 대체육 소비자 장벽 극복 전략",
            "시장 분석": "프리미엄 육가공 카테고리 성장률 / 식물성 대체육 소비자 인식 조사 / 글로벌 단백질 시장 트렌드",
            "채널 전략": "대형마트 냉장·냉동 코너 입점 기획 / 헬스·피트니스 채널 단백질 마케팅 / B2B 급식·외식 식자재 공급 전략",
            "마케팅 포인트": "고단백 건강 메시지, 식물성 대안 포지셔닝, 바비큐·홈쿡 트렌드 연계, 프리미엄 원육 강조",
            "확인 질문": "식물성 대체육 패티를 기존 육류 소비자에게 처음 소개할 때 어떤 메시지와 채널을 택할까?",
        },
    }
    # ─────────────────────────────────────────────────────────

    with tab_researcher:
        show_step_guide(
            _S2_STEPS, 1,
            todo="①~⑧ 빈칸을 직접 채워 나만의 연구원 페르소나를 완성하고 스크립트로 내보냅니다.",
            uses="앞 탭 예시에서 확인한 페르소나 항목 구조",
            produces="연구원 페르소나 스크립트 (AI 대화창 붙여넣기용)",
            minutes=15,
        )
        st.markdown("#### 📝 빈칸을 채워 나만의 연구원 페르소나를 완성하세요")

        # 랜덤 이름·회사 풀
        _R_NAME_POOL    = ["이민준","김도윤","박서준","최예린","정수연","윤지훈","강민서","조예은","오현우","신나영","한지원","양승현","서지우","문채원","임세진","배준혁","류지원","노아름","공민재","심은채"]
        _R_COMPANY_POOL = ["그린바이오푸드","케이에프앤비","푸드이노베이션","네추럴랩코리아","태양F&B","청정연구원","바이오에프씨","푸드앤사이언스","한울식품연구소","선진F&B","하이음료R&D","대한음료연구소","케이푸드바이오"]

        # ─── 기본 프로필 설정 ───
        st.markdown("##### 👤 기본 프로필 (이름·회사·거주지·연령·성별)")

        # 직무 테마를 먼저 결정해야 프리셋(rp) 기본값 사용 가능
        st.markdown('<span class="ml-step">① 어떤 분야의 연구원인가요?</span>', unsafe_allow_html=True)
        # 이번 교육에서 실습 가능한 직군만 노출한다 (음료 3종 + 유제품·제과·HMR·프레시푸드).
        # 그 외 직군은 프리셋은 남아 있으나 선택 목록에서 제외 — 필요 시 아래 직접 입력란 사용.
        _R_VISIBLE = [
            "💪 기능성음료 개발연구원",
            "🥤 탄산음료 개발연구원",
            "🌱 식물성·과채음료 개발연구원",
            "🥛 유제품 개발연구원",
            "🍪 제과·스낵 개발연구원",
            "🧊 냉동식품 개발연구원",
            "🍱 HMR·간편식 개발연구원",
            "🥗 프레시푸드·샐러드 개발연구원",
        ]
        _r_preset_keys = [k for k in _R_VISIBLE if k in RESEARCHER_PRESETS]
        _r_default_key = _r_preset_keys[0]  # 💪 기능성음료 개발연구원
        st.markdown('<span style="background:#fef08a;color:#92400e;padding:2px 10px;border-radius:6px;font-size:13px;font-weight:700;">★ 기능성음료 개발연구원이 기본 선택입니다</span>', unsafe_allow_html=True)
        r_theme = st.pills("직무 테마", _r_preset_keys, default=_r_default_key, key="r_theme_ml", label_visibility="collapsed")
        st.caption("🔒 그 외 직군(건강기능식품·소스/조미료·면류·축산가공)은 이번 교육에서 선택할 수 없습니다 — 필요하면 아래 직접 입력란에 적으세요.")
        r_theme_manual = st.text_input("직접 입력 (다른 직무)", placeholder="예: 냉동식품 연구원, 떡류 전문 연구원", key="r_theme_manual", label_visibility="collapsed")
        r_theme_sel = r_theme or _r_default_key
        rp = RESEARCHER_PRESETS[r_theme_sel]
        rtk = r_theme_sel.replace(" ", "_").replace("·", "").replace(".", "")
        r_job_display = r_theme_manual.strip() or (r_theme_sel.split(" ", 1)[-1] if " " in r_theme_sel else r_theme_sel)
        r_job_val = r_theme_manual.strip() or rp["직무"]

        # pending → widget key 반영 (위젯 렌더링 전에 처리해야 함)
        if f"r_name_pending_{rtk}" in st.session_state:
            st.session_state[f"r_name_{rtk}"] = st.session_state.pop(f"r_name_pending_{rtk}")
        if f"r_company_pending_{rtk}" in st.session_state:
            st.session_state[f"r_company_{rtk}"] = st.session_state.pop(f"r_company_pending_{rtk}")
        # 최초 진입 시 프리셋 기본값 설정
        if f"r_name_{rtk}" not in st.session_state:
            st.session_state[f"r_name_{rtk}"] = rp["이름"]
        if f"r_company_{rtk}" not in st.session_state:
            st.session_state[f"r_company_{rtk}"] = rp["직장"]

        st.caption("💡 각 항목을 입력한 후 **Enter**를 눌러 적용하세요.")
        col_nm1, col_nm2 = st.columns([5, 1])
        with col_nm1:
            r_name_val = st.text_input("이름", key=f"r_name_{rtk}")
        with col_nm2:
            st.markdown("<div style='margin-top:26px'></div>", unsafe_allow_html=True)
            if st.button("🎲", key=f"r_name_btn_{rtk}", help="랜덤 이름 생성"):
                st.session_state[f"r_name_pending_{rtk}"] = random.choice(_R_NAME_POOL)

        col_cp1, col_cp2 = st.columns([5, 1])
        with col_cp1:
            r_company_val = st.text_input("회사명", key=f"r_company_{rtk}")
        with col_cp2:
            st.markdown("<div style='margin-top:26px'></div>", unsafe_allow_html=True)
            if st.button("🎲", key=f"r_company_btn_{rtk}", help="랜덤 회사명 생성"):
                st.session_state[f"r_company_pending_{rtk}"] = random.choice(_R_COMPANY_POOL)

        col_ri, col_age, col_gnd = st.columns([3, 2, 2])
        with col_ri:
            r_residence_val = st.text_input("거주지", placeholder="예: 서울 마포구", key=f"r_residence_{rtk}")
        with col_age:
            # 간소화: 7개 -> 4개 (제외: 20대 초반, 40대 후반, 50대 이상)
            _AGE_OPTS = ["20대 후반","30대 초반","30대 후반","40대 초반"]
            _r_age_preset = rp.get("연령", "30대")
            _r_age_idx = next((i for i, a in enumerate(_AGE_OPTS) if a[:3] in _r_age_preset), 2)
            r_age_val = st.selectbox("연령", _AGE_OPTS, index=_r_age_idx, key=f"r_age_{rtk}")
        with col_gnd:
            r_gender_val = st.radio("성별", ["남성", "여성"], horizontal=True,
                                     index=0 if rp.get("성별", "남성") == "남성" else 1,
                                     key=f"r_gender_{rtk}")

        st.markdown("---")

        # ② 근무경력
        st.markdown('<span class="ml-step">② 근무경력을 확인하고 수정하세요</span>', unsafe_allow_html=True)
        r_career_val = st.text_input("근무경력", rp["근무경력"], key=f"r_career_{rtk}")

        # ③ 관심사
        st.markdown('<span class="ml-step">③ 주요 관심사를 확인하고 수정하세요</span>', unsafe_allow_html=True)
        r_interest_val = st.text_input("관심사", rp.get("관심사", ""), key=f"r_interest_{rtk}")

        # ④ 관심 제품 유형
        st.markdown('<span class="ml-step">④ 주로 어떤 제품을 개발하나요?</span>', unsafe_allow_html=True)
        _r_prod_opts = [p.strip() for p in rp["관심 제품 유형"].split(",")][:4]
        r_prod_sel = st.pills("제품 유형", _r_prod_opts, key=f"r_prod_{rtk}", label_visibility="collapsed")
        r_prod_manual = st.text_input("직접 입력", placeholder="예: 저당 탄산음료, 식물성 단백질 음료", key=f"r_prod_manual_{rtk}", label_visibility="collapsed")
        r_prod_display = r_prod_manual.strip() or r_prod_sel
        r_prod_val = r_prod_manual.strip() or r_prod_sel or rp["관심 제품 유형"]

        # ⑤ 관심 시장
        # 간소화: 7개 -> 4개 (제외: 카페·외식 B2B, 급식·단체급식, 드럭스토어·헬스)
        _R_MARKET_OPTS = ["편의점(CVS)", "대형마트", "온라인·이커머스", "수출·글로벌"]
        st.markdown('<span class="ml-step">⑤ 주로 어떤 시장을 타깃으로 하나요?</span>', unsafe_allow_html=True)
        r_market_sel = st.pills("관심 시장", _R_MARKET_OPTS, selection_mode="multi", key=f"r_market_{rtk}", label_visibility="collapsed")
        r_market_manual = st.text_input("직접 입력", placeholder="예: 헬스푸드 전문점, H&B 스토어", key=f"r_market_manual_{rtk}", label_visibility="collapsed")
        r_market_val = r_market_manual.strip() or (", ".join(r_market_sel) if r_market_sel else "")

        # ⑥ 전문 기술 프로필 (expander)
        with st.expander("⑥ 🔬 전문 기술 프로필 확인·수정 (클릭하면 열림)"):
            col_a, col_b = st.columns(2)
            with col_a:
                r_skills_val  = st.text_area("보유기술",             rp.get("보유기술", ""),            key=f"r_skills_{rtk}",  height=72)
                r_process_val = st.text_area("식품공정 지식",         rp.get("식품공정 지식", ""),        key=f"r_process_{rtk}", height=72)
                r_formula_val = st.text_area("식품배합비 이론",       rp.get("식품배합비 이론", ""),      key=f"r_formula_{rtk}", height=72)
            with col_b:
                r_env_val     = st.text_area("업무 환경 (보유 장비)", rp.get("업무 환경", ""),            key=f"r_env_{rtk}",     height=72)
                r_quality_val = st.text_area("품질 및 리스크관리",    rp.get("품질 및 리스크관리", ""),   key=f"r_quality_{rtk}", height=72)

        # ⑦ 연구개발 포인트
        _R_RD_MAP = {
            "재현성 중시": "공장에서 나온 첫 병과 유통기한 마지막 날의 맛이 동일해야 한다",
            "효능+맛 균형": "효능은 과학으로 증명하고, 맛은 소비자가 매일 먹고 싶게 만들어야 한다",
            "식감 설계": "첫 입에서 끝 입까지 일관된 식감과 풍미를 설계한다",
            "소비자 인식": "소비자가 '건강하다'고 느끼는 순간이 곧 성공이다",
        }
        st.markdown('<span class="ml-step">⑦ 가장 중요하게 생각하는 연구 방향은?</span>', unsafe_allow_html=True)
        r_rd_sel = st.pills("연구 방향", list(_R_RD_MAP.keys()), key=f"r_rd_{rtk}", label_visibility="collapsed")
        r_rd_manual = st.text_input("직접 입력", placeholder="예: 원가 절감 없이 배합 최적화로 맛 품질 향상", key=f"r_rd_manual_{rtk}", label_visibility="collapsed")
        r_rd_display = r_rd_manual.strip() or r_rd_sel
        r_rd_val = r_rd_manual.strip() or _R_RD_MAP.get(r_rd_sel, rp["연구개발 포인트"])

        # ⑧ 확인 질문 (expander)
        with st.expander("⑧ 페르소나 적용 확인 질문 (선택)"):
            r_test_q = st.text_input("확인 질문", rp["확인 질문"], key=f"r_testq_{rtk}", label_visibility="collapsed")

        # Mad-lib 완성 문장
        def _span_r(val, placeholder):
            if val:
                return f'<span class="ml-filled">{val}</span>'
            return f'<span class="ml-empty">{placeholder}</span>'

        st.markdown("---")
        st.markdown("### ✅ 내가 만든 페르소나")
        st.markdown(f"""
<div class="ml-box">
저는 <b>{_span_r(r_job_display, '직무 분야')}</b> 전문가로,<br>
{_span_r(r_career_val, '근무경력')}의 경험을 보유합니다.<br>
{_span_r(r_interest_val, '관심사')}에 관심이 있으며,<br>
{_span_r(r_prod_display, '관심 제품')} 개발을 {_span_r(r_rd_display, '연구 방향')}을 핵심으로 담당합니다.
</div>
""", unsafe_allow_html=True)

        _r_job_full = f"{r_prod_val} 전문 {r_job_val}" if r_prod_val else r_job_val
        prompt_r = f"""{_NO_MEMORY_HEADER}{_r_job_full} 페르소나를 아래 정보로 작성해 주세요.
(직무명은 반드시 '{_r_job_full}'로 표기하세요. 임의로 변경하지 마세요.)

이름: {r_name_val} / 연령: {r_age_val} / 직장: {r_company_val} / 직무: {_r_job_full} / 성별: {r_gender_val} / 거주지: {r_residence_val or '미입력'}
근무경력: {r_career_val}
관심사: {r_interest_val}
관심 제품: {r_prod_val}
관심 시장: {r_market_val or '미선택'}
보유기술: {r_skills_val}
식품공정 지식: {r_process_val}
식품배합비 이론: {r_formula_val}
업무 환경: {r_env_val}
연구개발 포인트: {r_rd_val}
품질 및 리스크관리: {r_quality_val}

[이 대화 전용 역할 지정] 지금부터 이 연구원은 위 페르소나를 적용합니다.

[출력 형식 — 아래 순서와 번호를 그대로 지켜 작성]
1. 페르소나 형성 결과  ★가장 중요
   - 위 정보가 페르소나에 어떻게 반영되었는지 항목별로 정리
   - 이 연구원이 어떤 관점과 판단 기준으로 일하는지 3~5줄로 서술
2. 적용 확인 답변
   - 확인 질문: {r_test_q}
   - 위 페르소나 입장에서 5줄 이내로 짧게 답변

※ 1번을 먼저, 가장 충실하게 작성하세요. 2번은 페르소나가 제대로 적용됐는지 점검하는 용도이므로 짧게 답합니다."""

        r_fields = {
            "직무": r_job_val, "근무경력": r_career_val,
            "관심사": r_interest_val, "관심 제품 유형": r_prod_val,
            "연구개발 포인트": r_rd_val, "확인 질문": r_test_q,
        }
        r_defaults = {
            "직무": rp["직무"], "근무경력": rp["근무경력"],
            "관심사": rp.get("관심사", ""), "관심 제품 유형": rp["관심 제품 유형"],
            "연구개발 포인트": rp["연구개발 포인트"], "확인 질문": rp["확인 질문"],
        }
        render_persona_coach(prompt_r, r_fields, r_defaults, f"r_{rtk}")
        # 파일링크 불필요: 연구자 페르소나 스크립트는 텍스트 제출로 충분
        _hw_ui("연구원_페르소나", prompt_r, "r_hw_submit")

    with tab_marketer:
        show_step_guide(
            _S2_STEPS, 2,
            todo="같은 방식으로 마케터 페르소나를 완성합니다.",
            uses="연구원 페르소나에서 정한 제품 분야·관심 시장",
            produces="마케터 페르소나 스크립트 — STEP 3부터 모든 실습의 AI 역할 설정",
            minutes=12,
        )
        st.markdown("#### 📝 빈칸을 채워 나만의 마케터 페르소나를 완성하세요")

        # 랜덤 이름·회사 풀
        _M_NAME_POOL    = ["이지안","김서현","박민준","최다은","정유진","윤하늘","강수아","조민혁","오세영","신지은","한소희","양민재","서준혁","문가을","임채원","배나리","류지수","노민수","공다현","심재원"]
        _M_COMPANY_POOL = ["레드오션마케팅","브랜드퍼스트","마켓이노베이션","글로벌F&B마케팅","트렌드랩코리아","디지털식품마케팅","케이브랜드컨설팅","푸드마케팅그룹","한국음료마케팅","스마트F&B"]

        # ─── 기본 프로필 설정 ───
        st.markdown("##### 👤 기본 프로필 (이름·회사·거주지·연령·성별)")

        st.markdown('<span class="ml-step">① 어떤 분야의 마케터인가요?</span>', unsafe_allow_html=True)
        # 연구원 탭과 같은 기준으로 교육 대상 직군만 노출
        _M_VISIBLE = [
            "🧃 음료 브랜드마케터",
            "🥛 유제품 마케터",
            "🍪 제과·스낵 마케터",
            "🍱 HMR·간편식 마케터",
            "🥗 프레시푸드·샐러드 마케터",
        ]
        _m_preset_keys = [k for k in _M_VISIBLE if k in MARKETER_PRESETS]
        _m_default_key = _m_preset_keys[0]  # 🧃 음료 브랜드마케터
        st.markdown('<span style="background:#fef08a;color:#92400e;padding:2px 10px;border-radius:6px;font-size:13px;font-weight:700;">★ 음료 브랜드마케터가 기본 선택입니다</span>', unsafe_allow_html=True)
        m_theme = st.pills("직무 테마", _m_preset_keys, default=_m_default_key, key="m_theme_ml", label_visibility="collapsed")
        st.caption("🔒 그 외 직군(건강기능식품·소스/조미료·면류·축산가공)은 이번 교육에서 선택할 수 없습니다 — 필요하면 아래 직접 입력란에 적으세요.")
        m_theme_manual = st.text_input("직접 입력 (다른 직무)", placeholder="예: 냉동식품 마케터, 스낵 브랜드 매니저", key="m_theme_manual", label_visibility="collapsed")
        m_theme_sel = m_theme or _m_default_key
        mp = MARKETER_PRESETS[m_theme_sel]
        mtk = m_theme_sel.replace(" ", "_").replace("·", "").replace(".", "")
        m_job_display = m_theme_manual.strip() or (m_theme_sel.split(" ", 1)[-1] if " " in m_theme_sel else m_theme_sel)
        m_job_val = m_theme_manual.strip() or mp["직무"]

        # pending → widget key 반영 (위젯 렌더링 전에 처리)
        if f"m_name_pending_{mtk}" in st.session_state:
            st.session_state[f"m_name_{mtk}"] = st.session_state.pop(f"m_name_pending_{mtk}")
        if f"m_company_pending_{mtk}" in st.session_state:
            st.session_state[f"m_company_{mtk}"] = st.session_state.pop(f"m_company_pending_{mtk}")
        # 최초 진입 시 프리셋 기본값 설정
        if f"m_name_{mtk}" not in st.session_state:
            st.session_state[f"m_name_{mtk}"] = mp["이름"]
        if f"m_company_{mtk}" not in st.session_state:
            st.session_state[f"m_company_{mtk}"] = mp["직장"]

        st.caption("💡 각 항목을 입력한 후 **Enter**를 눌러 적용하세요.")
        col_nm1, col_nm2 = st.columns([5, 1])
        with col_nm1:
            m_name_val = st.text_input("이름", key=f"m_name_{mtk}")
        with col_nm2:
            st.markdown("<div style='margin-top:26px'></div>", unsafe_allow_html=True)
            if st.button("🎲", key=f"m_name_btn_{mtk}", help="랜덤 이름 생성"):
                st.session_state[f"m_name_pending_{mtk}"] = random.choice(_M_NAME_POOL)

        col_cp1, col_cp2 = st.columns([5, 1])
        with col_cp1:
            m_company_val = st.text_input("회사명", key=f"m_company_{mtk}")
        with col_cp2:
            st.markdown("<div style='margin-top:26px'></div>", unsafe_allow_html=True)
            if st.button("🎲", key=f"m_company_btn_{mtk}", help="랜덤 회사명 생성"):
                st.session_state[f"m_company_pending_{mtk}"] = random.choice(_M_COMPANY_POOL)

        col_ri, col_age, col_gnd = st.columns([3, 2, 2])
        with col_ri:
            m_residence_val = st.text_input("거주지", placeholder="예: 서울 강남구", key=f"m_residence_{mtk}")
        with col_age:
            # 간소화: 7개 -> 4개 (제외: 20대 초반, 40대 후반, 50대 이상)
            _AGE_OPTS = ["20대 후반","30대 초반","30대 후반","40대 초반"]
            _m_age_preset = mp.get("연령", "30대")
            _m_age_idx = next((i for i, a in enumerate(_AGE_OPTS) if a[:3] in _m_age_preset), 2)
            m_age_val = st.selectbox("연령", _AGE_OPTS, index=_m_age_idx, key=f"m_age_{mtk}")
        with col_gnd:
            m_gender_val = st.radio("성별", ["남성", "여성"], horizontal=True,
                                     index=0 if mp.get("성별", "여성") == "남성" else 1,
                                     key=f"m_gender_{mtk}")

        st.markdown("---")

        # ② 근무경력
        st.markdown('<span class="ml-step">② 근무경력을 확인하고 수정하세요</span>', unsafe_allow_html=True)
        m_career_val = st.text_input("근무경력", mp["근무경력"], key=f"m_career_{mtk}")

        # ③ 관심사
        st.markdown('<span class="ml-step">③ 주요 관심사를 확인하고 수정하세요</span>', unsafe_allow_html=True)
        m_interest_val = st.text_input("관심사", mp.get("관심사", ""), key=f"m_interest_{mtk}")

        # ④ 관심 제품 유형
        st.markdown('<span class="ml-step">④ 주로 어떤 제품을 마케팅하나요?</span>', unsafe_allow_html=True)
        _m_prod_opts = [p.strip() for p in mp["관심 제품 유형"].split(",")][:4]
        m_prod_sel = st.pills("제품 유형", _m_prod_opts, key=f"m_prod_{mtk}", label_visibility="collapsed")
        m_prod_manual = st.text_input("직접 입력", placeholder="예: 프리미엄 RTD 커피, 비건 간편식", key=f"m_prod_manual_{mtk}", label_visibility="collapsed")
        m_prod_display = m_prod_manual.strip() or m_prod_sel
        m_prod_val = m_prod_manual.strip() or m_prod_sel or mp["관심 제품 유형"]

        # ⑤ 관심 시장
        # 간소화: 7개 -> 4개 (제외: 카페·외식 B2B, 급식·단체급식, 드럭스토어·헬스)
        _M_MARKET_OPTS = ["편의점(CVS)", "대형마트", "온라인·이커머스", "수출·글로벌"]
        st.markdown('<span class="ml-step">⑤ 주로 어떤 시장을 타깃으로 하나요?</span>', unsafe_allow_html=True)
        m_market_sel = st.pills("관심 시장", _M_MARKET_OPTS, selection_mode="multi", key=f"m_market_{mtk}", label_visibility="collapsed")
        m_market_manual = st.text_input("직접 입력", placeholder="예: 헬스푸드 전문점, 홈쇼핑", key=f"m_market_manual_{mtk}", label_visibility="collapsed")
        m_market_val = m_market_manual.strip() or (", ".join(m_market_sel) if m_market_sel else "")

        # ⑥ 전문 마케팅 프로필 (expander)
        with st.expander("⑥ 📊 전문 마케팅 프로필 확인·수정 (클릭하면 열림)"):
            col_a, col_b = st.columns(2)
            with col_a:
                m_skills_val  = st.text_area("보유기술",   mp.get("보유기술", ""),   key=f"m_skills_{mtk}",  height=72)
                m_mktana_val  = st.text_area("시장 분석",  mp.get("시장 분석", ""),  key=f"m_mktana_{mtk}",  height=72)
            with col_b:
                m_channel_val = st.text_area("채널 전략",  mp.get("채널 전략", ""),  key=f"m_channel_{mtk}", height=72)
                m_comp_val    = st.text_area("직무 역량",  mp.get("직무 역량", ""),  key=f"m_comp_{mtk}",    height=72)

        # ⑦ 마케팅 포인트
        _M_MKT_MAP = {
            "시장성·차별성": "시장성, 차별성, 화제성으로 경쟁 우위를 만든다",
            "소비자 공감": "소비자가 공감하고 재구매하는 브랜드 경험 설계",
            "데이터 기반": "판매 데이터와 소비자 인사이트로 의사결정",
            "트렌드 반영": "시즌성·트렌드를 빠르게 반영한 신제품 기획",
        }
        st.markdown('<span class="ml-step">⑦ 가장 중요하게 생각하는 마케팅 방향은?</span>', unsafe_allow_html=True)
        m_mkt_sel = st.pills("마케팅 방향", list(_M_MKT_MAP.keys()), key=f"m_mkt_{mtk}", label_visibility="collapsed")
        m_mkt_manual = st.text_input("직접 입력", placeholder="예: SNS 바이럴과 편의점 입점 전략 동시 추진", key=f"m_mkt_manual_{mtk}", label_visibility="collapsed")
        m_mkt_display = m_mkt_manual.strip() or m_mkt_sel
        m_mkt_val = m_mkt_manual.strip() or _M_MKT_MAP.get(m_mkt_sel, mp["마케팅 포인트"])

        # ⑧ 확인 질문 (expander)
        with st.expander("⑧ 페르소나 적용 확인 질문 (선택)"):
            m_test_q = st.text_input("확인 질문", mp["확인 질문"], key=f"m_testq_{mtk}", label_visibility="collapsed")

        # Mad-lib 완성 문장
        def _span_m(val, placeholder):
            if val:
                return f'<span class="ml-filled">{val}</span>'
            return f'<span class="ml-empty">{placeholder}</span>'

        st.markdown("---")
        st.markdown("### ✅ 내가 만든 페르소나")
        st.markdown(f"""
<div class="ml-box">
저는 <b>{_span_m(m_job_display, '직무 분야')}</b> 전문가로,<br>
{_span_m(m_career_val, '근무경력')}의 경험을 보유합니다.<br>
{_span_m(m_interest_val, '관심사')}에 관심이 있으며,<br>
{_span_m(m_prod_display, '관심 제품')} 마케팅을 {_span_m(m_mkt_display, '마케팅 방향')}을 중심으로 담당합니다.
</div>
""", unsafe_allow_html=True)

        _m_job_full = f"{m_prod_val} 전문 {m_job_val}" if m_prod_val else m_job_val
        prompt_m = f"""{_NO_MEMORY_HEADER}{_m_job_full} 페르소나를 아래 정보로 작성해 주세요.
(직무명은 반드시 '{_m_job_full}'로 표기하세요. 임의로 변경하지 마세요.)

이름: {m_name_val} / 연령: {m_age_val} / 직장: {m_company_val} / 직무: {_m_job_full} / 성별: {m_gender_val} / 거주지: {m_residence_val or '미입력'}
근무경력: {m_career_val}
관심사: {m_interest_val}
관심 제품: {m_prod_val}
관심 시장: {m_market_val or '미선택'}
보유기술: {m_skills_val}
시장 분석: {m_mktana_val}
채널 전략: {m_channel_val}
직무 역량: {m_comp_val}
마케팅 포인트: {m_mkt_val}

[이 대화 전용 역할 지정] 지금부터 이 마케터는 위 페르소나를 적용합니다.

[출력 형식 — 아래 순서와 번호를 그대로 지켜 작성]
1. 페르소나 형성 결과  ★가장 중요
   - 위 정보가 페르소나에 어떻게 반영되었는지 항목별로 정리
   - 이 마케터가 어떤 관점과 판단 기준으로 일하는지 3~5줄로 서술
2. 적용 확인 답변
   - 확인 질문: {m_test_q}
   - 위 페르소나 입장에서 5줄 이내로 짧게 답변

※ 1번을 먼저, 가장 충실하게 작성하세요. 2번은 페르소나가 제대로 적용됐는지 점검하는 용도이므로 짧게 답합니다."""

        m_fields = {
            "직무": m_job_val, "근무경력": m_career_val,
            "관심사": m_interest_val, "관심 제품 유형": m_prod_val,
            "마케팅 포인트": m_mkt_val, "확인 질문": m_test_q,
        }
        m_defaults = {
            "직무": mp["직무"], "근무경력": mp["근무경력"],
            "관심사": mp.get("관심사", ""), "관심 제품 유형": mp["관심 제품 유형"],
            "마케팅 포인트": mp["마케팅 포인트"], "확인 질문": mp["확인 질문"],
        }
        render_persona_coach(prompt_m, m_fields, m_defaults, f"m_{mtk}")
        # 파일링크 불필요: 마케터 페르소나 스크립트는 텍스트 제출로 충분
        show_transfer_box(
            "s2",
            "내 회사의 실제 직무 기준이라면, 페르소나에서 어떤 항목을 어떻게 고쳐야 할까요?",
            "예: 우리는 냉동만두라 식품공정 지식을 증숙·급속동결로, 장비를 텍스처분석기·동결점 측정으로 바꿔야 함",
        )

        _hw_ui("마케터_페르소나", prompt_m, "m_hw_submit")


# ----------------------------------------------------------
# 3. 제품 아이디어 도출
# ----------------------------------------------------------
elif section == "4️⃣ 시장분석 및 학습":
    if _CRAWL_ONLY:
        show_banner(
            "온라인 시장분석 실습",
            "쇼핑몰에서 실제 상품 데이터를 가져와 AI로 분석해 봅니다.",
            "실습"
        )
        with st.expander("✏️ 이름 입력 (과제를 제출할 때만)"):
            _cn = st.text_input("이름", key="_crawl_name",
                                placeholder="예: 홍길동",
                                label_visibility="collapsed")
            if st.button("이름 저장", key="_crawl_name_btn"):
                st.session_state["student_name"] = _cn.strip()
                st.rerun()
            if st.session_state.get("student_name"):
                st.success("👤 %s — 이제 과제를 제출할 수 있습니다."
                           % st.session_state["student_name"])
    else:
        show_banner(
            "시장분석 및 학습",
            "온라인 시장 현황 분석부터 식품 전문 데이터 학습, 보고서 작성까지 AI와 함께 시장을 읽습니다.",
            "4 / 7"
        )
        show_mission([
            "온라인 쇼핑몰의 음료 판매 현황을 수집해 AI로 분석하기",
            "식품안전나라 품목제조보고서 데이터를 AI에게 학습시키기",
            "시장 조사 데이터를 기반으로 신제품 개발 보고서 작성하기",
        ])

    _S4_STEPS = ["온라인 시장분석", "식품전문정보 분석", "매대사진 분석", "보고서 작성", "AI 대화전환"]

    if _CRAWL_ONLY:
        # 이 화면에서는 온라인 시장분석 하나만 쓴다.
        # 나머지 탭은 아래 st.stop() 으로 아예 실행되지 않는다.
        (tab_online,) = st.tabs(["🛒 온라인 시장분석"])
        tab_food = tab_learn = tab_report = tab_ai = None
    else:
        tab_online, tab_food, tab_learn, tab_report, tab_ai = st.tabs([
            "🛒 온라인 시장분석",
            "🗂️ 식품전문정보분석",
            "📊 시장조사 데이터 학습",
            "📝 보고서 작성하기",
            "🔄 AI 간 대화전환",
        ])

    # ── 탭 1: 온라인 시장분석 ──
    with tab_online:
        show_step_guide(
            _S4_STEPS, 0,
            todo="쇼핑몰에서 상품 데이터를 가져오는 코드를 AI에게 만들게 하고, 직접 실행해 봅니다.",
            uses="STEP 2에서 만든 페르소나 + STEP 3에서 학습시킨 AI 프로젝트",
            produces="실제로 수집한 상품 데이터 — 다음 단계 분석의 재료",
            minutes=15,
        )
        st.markdown("#### 🛒 온라인 시장 데이터 직접 수집하기")
        st.caption("AI에게 수집 코드를 만들게 하고, 직접 실행해 실제 상품 데이터를 가져옵니다.")

        sub_ex, sub_task, sub_code = st.tabs(
            ["📖 예시 스크립트", "📋 스크립트 작성 과제", "🐍 수집 코드 실행하기"]
        )

        # ══════════ 예시 스크립트 ══════════
        with sub_ex:
            st.markdown("##### 📖 AI에게 수집 코드를 요청하는 스크립트 — 완성 예시")
            st.caption("그대로 복사해 ChatGPT에 넣으면 실행 가능한 코드를 받습니다.")
            st.code("""마켓컬리에서 '탄산음료'를 검색해서
상위 30개 상품의 상품명, 가격, 브랜드, 리뷰수를 가져오는 파이썬 코드를 만들어줘.

- 주소: https://www.kurly.com/search?sword=탄산음료&page=1&per_page=96
- 상품은 a[href*="/goods/"] 로 찾을 수 있어
- playwright를 쓰고 headless=True로, 결과는 print로 출력해줘
- 설치 명령은 넣지 마 (이미 설치돼 있어)

[출력은 표로 정리해줘]
- 카드 텍스트를 그대로 찍지 마. 아래처럼 항목을 나눠줘.
  · '담기', '샛별배송', '쿠폰' 이 들어간 줄은 버린다
  · 상품명 = [브랜드] 로 시작하는 줄
  · 가격 = '원'이 붙은 숫자 중 마지막 값
  · 리뷰수 = 맨 끝의 숫자
- 번호를 붙이고 열 너비를 맞춰 표처럼 print 해줘.""", language=None)

            with st.expander("❓ 왜 주소와 셀렉터까지 알려줘야 하나요?"):
                st.markdown("""
AI는 **화면을 볼 수 없습니다.** 그래서 "마켓컬리에서 음료 긁어줘"라고만 하면
주소와 셀렉터를 스스로 지어내고, 대부분 틀립니다. 코드는 그럴듯한데 상품이 0개 나옵니다.

| 알려주는 것 | 없으면 생기는 일 |
|---|---|
| 주소 | 엉뚱한 페이지를 열거나 없는 주소를 만듦 |
| 셀렉터 `a[href*="/goods/"]` | 화면 구조를 추측 → 상품 0개 |
| headless=True | 서버에 화면이 없어 실행 오류 |
| 설치 명령 금지 | `!pip install` 이 들어가 문법 오류 |
| print 출력 | 실행은 되는데 화면에 아무것도 안 나옴 |

**다음 탭에서 만드는 스크립트에는 이 조건들이 자동으로 붙습니다.** 외우지 않아도 됩니다.
""")
            st.caption(
                "👉 다음 탭 **스크립트 작성 과제**에서 검색어와 수집 항목을 골라 "
                "나만의 스크립트를 만들고, **수집 코드 실행하기** 탭에서 바로 돌려볼 수 있습니다."
            )

        # ══════════ 스크립트 작성 과제 ══════════
        with sub_task:
            st.markdown("##### 📋 나만의 수집 코드 요청 스크립트 만들기")

            st.markdown("**Step 1. 수집할 사이트를 고르세요**")
            _SITES = {
                "마켓컬리": True,
                "네이버쇼핑": False,
                "쿠팡": False,
                "11번가": False,
                "아마존": False,
            }
            _site = st.pills("사이트", list(_SITES.keys()), default="마켓컬리",
                             key="pw_site", label_visibility="collapsed")
            _site = _site or "마켓컬리"

            _WHY = {
                "네이버쇼핑": "robots.txt에서 전체 수집 금지 (AI 크롤러도 명시 차단)",
                "쿠팡": "봇으로 판단되면 접속 단계에서 차단",
                "11번가": "robots.txt에서 전체 수집 금지",
                "아마존": "접속하면 빈 페이지 — 자동 접속을 감지해 차단",
            }
            if not _SITES[_site]:
                st.warning("🔒 **%s은(는) 수집할 수 없습니다.** %s" % (_site, _WHY[_site]))
                st.caption("실습은 수집이 허용된 마켓컬리로 진행합니다.")
                _site = "마켓컬리"
            else:
                st.success("✅ 마켓컬리는 수집이 허용된 사이트입니다.")

            st.markdown("---")
            st.markdown("**Step 2. 무엇을 수집할지 정하세요**")

            st.caption("🥤 음료 유형 — 여기서 고른 유형 안에서만 찾습니다")
            _PW_KW = ["탄산음료", "커피음료", "과일주스", "차음료",
                      "단백질음료", "식물성음료", "이온음료", "제로음료"]
            _pw_kw = st.pills("유형", _PW_KW, default="탄산음료",
                              key="pw_kw", label_visibility="collapsed")

            st.caption("🔎 유형 내 세부검색 (선택) — 맛·컨셉 단어로 좁히기")
            _pw_detail = st.text_input(
                "세부검색", key="pw_kw_custom",
                placeholder="예: 제로, 레몬, 착즙, 유기농, 스파클링  (쉼표로 여러 개)",
                label_visibility="collapsed",
            )
            with st.expander("💡 어떤 단어가 잘 잡히나요?"):
                st.markdown(
                    "고른 유형 **안에서만** 걸리는 조건입니다. 실제로 상품명에 자주 나오는 단어 —\n\n"
                    "| 유형 | 잘 잡히는 단어 |\n|---|---|\n"
                    "| 탄산음료 | 제로 · 탄산수 · 스파클링 · 레몬 |\n"
                    "| 과일주스 | 착즙 · 유기농 · 오렌지 |\n"
                    "| 단백질음료 | 단백질 · 저당 |\n"
                    "| 차음료 | 유기농 · 무가당 |\n\n"
                    "가격대와 정렬은 **실행 탭**에서 따로 고릅니다."
                )

            _oc1, _oc2 = st.columns(2)
            with _oc1:
                st.caption("📦 가져올 정보")
                _PW_FIELDS = ["상품명", "가격", "브랜드", "리뷰수", "설명문구", "할인율"]
                _pw_fields = st.pills("항목", _PW_FIELDS, selection_mode="multi",
                                      key="pw_fields", label_visibility="collapsed")
            with _oc2:
                st.caption("🔀 정렬 기준")
                _SORT_MAP = {"추천순": None, "판매량순": 1, "신상품순": 0, "낮은 가격순": 2}
                _pw_sort = st.pills("정렬", list(_SORT_MAP.keys()), key="pw_sort",
                                    label_visibility="collapsed")

            _ac1, _ac2 = st.columns(2)
            with _ac1:
                st.caption("🔢 수집 규모")
                _pw_amount = st.pills("규모", ["30개", "50개", "100개"],
                                      key="pw_amount", label_visibility="collapsed")
            with _ac2:
                st.caption("📄 출력 형식")
                _pw_out = st.pills("출력", ["표로 출력", "목록으로 출력", "CSV로 저장"],
                                   key="pw_out", label_visibility="collapsed")

            st.caption("🎯 분석 목적 (나중에 GPT 분석에 그대로 쓰입니다)")
            _GOALS = {
                "브랜드 경쟁 현황": "브랜드별 상품 수와 상위 브랜드, 브랜드 집중도",
                "가격대 분포": "가격 구간별 상품 수와 평균가, 비어 있는 가격대",
                "플레이버 트렌드": "상품명에 나타나는 맛·향 키워드 빈도와 상위 플레이버",
                "컨셉 키워드": "제로·무가당·프리미엄 등 컨셉 표현의 비중",
                "신제품 기회 발굴": "가격대·플레이버 공백과 그 공백을 노린 신규 컨셉 3개 제안",
            }
            _pw_goals = st.pills("목적", list(_GOALS.keys()), selection_mode="multi",
                                 key="pw_goals", label_visibility="collapsed")
            _goal_names = _pw_goals or ["브랜드 경쟁 현황", "가격대 분포"]
            st.session_state["pw_goal_names"] = ", ".join(_goal_names)
            st.session_state["pw_goal_lines"] = "\n".join(
                "%d. %s" % (_i + 1, _GOALS[_g]) for _i, _g in enumerate(_goal_names))

            _sort_name = _pw_sort or "추천순"
            _sort_no = _SORT_MAP[_sort_name]
            _amount = (_pw_amount or "100개").replace("개", "")
            _outfmt = _pw_out or "표로 출력"
            _OUT_SPEC = {
                "표로 출력":
                    "번호를 붙이고 열 너비를 맞춰 표처럼 print 해라.",
                "목록으로 출력":
                    "'1. 상품명 (가격, 리뷰 N)' 형태로 한 줄씩 print 해라.",
                "CSV로 저장":
                    "첫 줄에 헤더를 넣고 쉼표로 구분한 CSV 형식으로 print 해라.",
            }
            _out_spec = _OUT_SPEC.get(_outfmt, _OUT_SPEC["표로 출력"])

            st.caption("판매량순 = 실제로 잘 팔리는 순서 · 원재료·영양성분은 수집되지 않습니다")

            _kw = _pw_kw or "탄산음료"          # 검색어는 항상 '유형'
            _detail = _pw_detail.strip()        # 세부어는 상품명 필터로만 쓴다
            st.session_state["pw_detail_final"] = _detail
            _fields = ", ".join(_pw_fields or ["상품명", "가격"])
            st.session_state["pw_kw_final"] = _kw
            st.session_state["pw_sort_final"] = _sort_name

            _url = ("https://www.kurly.com/search?sword=" + _kw
                    + "&page=1&per_page=96"
                    + ("" if _sort_no is None else "&sorted_type=%d" % _sort_no))

            _pw_script = (
                "마켓컬리에서 상품 정보를 수집하는 파이썬 코드를 만들어줘.\n\n"
                "[수집 주소]\n" + _url + "\n"
                + ("" if _sort_no is None
                   else "(sorted_type=%d 은 %s 정렬이다)\n" % (_sort_no, _sort_name))
                + "\n[가져올 항목]\n" + _fields + "\n\n"
                + ("[상품명 조건]\n- 상품명에 다음 단어 중 하나가 든 상품만 남겨라: "
                   + _detail
                   + "\n  (쇼핑몰 검색은 단어가 겹치기만 해도 잡혀서 엉뚱한 품목이 섞인다)\n\n"
                   if _detail else "")
                + "[이 데이터로 하려는 것]\n- " + ", ".join(_goal_names)
                + " 분석에 쓸 거야.\n\n"
                "[수집 규모]\n"
                "- 상위 " + _amount + "개만 가져온다.\n\n"
                "[출력 정리 — 카드 텍스트를 그대로 찍지 마라]\n"
                "- '담기', '샛별배송', '쿠폰'이 들어간 줄은 버린다.\n"
                "- 상품명 = [브랜드] 로 시작하는 줄\n"
                "- 가격 = '원'이 붙은 숫자 중 마지막 값 (할인가)\n"
                "- 리뷰수 = 맨 끝의 숫자\n"
                "- " + _out_spec + "\n\n"
                "[코드 조건 — 이대로만 만들면 바로 실행된다]\n"
                "- playwright 동기 API(sync_playwright)를 쓰고 headless=True로 실행한다.\n"
                "- 설치 명령(!pip install, playwright install)은 넣지 마라. 이미 설치되어 있다.\n"
                "- 상품 카드는 a[href*=\"/goods/\"] 로 모두 찾을 수 있다. 다른 셀렉터를 추측하지 마라.\n"
                "- 카드의 innerText 안에 상품명·가격·리뷰수가 줄바꿈으로 들어 있다.\n"
                "- 페이지를 연 뒤 wait_for_selector로 상품이 나타날 때까지 기다려라.\n"
                "- 결과는 print로만 출력한다. 파일 저장은 하지 마라.\n"
                "- 30줄 이내로 짧게 만들고, 주석은 한 줄씩만 달아라.\n\n"
                "[주의]\n"
                "- 마켓컬리 robots.txt는 이 경로의 수집을 허용한다 (2026년 8월 확인).\n"
                "- 실행은 내가 한다. 실행했다고 말하지 마라."
            )

            st.session_state["online_user_script"] = _pw_script

            st.markdown("---")
            st.markdown("**Step 3. 완성된 스크립트 — 복사해서 AI에게 주세요**")
            st.caption("📋 코드 블록 우측 상단 복사 아이콘 클릭")
            st.code(_pw_script, language=None)

            st.markdown("**Step 4. 붙여넣을 곳 고르기**")
            _way1, _way2 = st.columns(2)
            with _way1:
                st.markdown(
                    "**🧠 ChatGPT / Gemini**\n\n"
                    "파이썬 **코드**를 답으로 받습니다.\n\n"
                    "받은 코드는 다음 탭에서 강사가 실제로 돌려 보여줍니다."
                )
            with _way2:
                st.markdown(
                    "**⚙️ Google AI Studio**\n\n"
                    "코드가 아니라 **앱**을 만들어 줍니다.\n\n"
                    "[aistudio.google.com/apps](https://aistudio.google.com/apps) "
                    "→ **New app** → 스크립트 붙여넣기"
                )
            st.caption("구글 계정으로 로그인만 하면 되고, API 키를 따로 발급받지 않아도 됩니다.")

            with st.expander("⚙️ Google AI Studio로 앱 만들어 보기"):
                st.markdown(
                    "1. [aistudio.google.com/apps](https://aistudio.google.com/apps) 접속 "
                    "(구글 계정 로그인)\n"
                    "2. **New app** 클릭\n"
                    "3. 위에서 복사한 스크립트를 그대로 붙여넣고 실행\n"
                    "4. 만들어진 앱을 눌러 결과를 확인\n\n"
                    "**결과가 나오면 반드시 대조하세요** — 실제 마켓컬리 페이지를 열어 "
                    "상품명과 가격이 같은지 몇 개만 확인합니다. "
                    "다르면 AI가 지어낸 값입니다. 그때는 강사 시연 화면과 "
                    "아래 **수집해둔 데이터**를 쓰세요."
                )

            st.markdown("**Step 5. 체크리스트로 자가 점검하세요**")
            _CHECKLIST = [
                "수집 대상 사이트의 robots.txt를 직접 열어 확인했나요?",
                "무엇을(항목) 어디서(검색어) 가져올지 구체적으로 지정했나요?",
                "설치 명령을 넣지 말라는 조건을 포함했나요?",
                "결과를 print로 출력하라고 지시했나요?",
            ]
            _checks = [st.checkbox(_it, key="online_chk_%d" % _i)
                       for _i, _it in enumerate(_CHECKLIST)]
            _done = sum(1 for c in _checks if c)
            st.progress(_done / len(_CHECKLIST),
                        text="%d / %d 항목 확인" % (_done, len(_CHECKLIST)))

            _hw_ui("온라인시장분석", _pw_script, "online_hw_submit",
                   ai_label="ChatGPT가 만들어준 코드",
                   title="과제 제출 — 수집 코드 요청 스크립트")

        # ══════════ 수집 코드 실행하기 ══════════
        with sub_code:
            _can_exec = _playwright_ready()
            if not _can_exec:
                st.warning(
                    "⚠️ **이 화면(온라인 배포본)에서는 코드 실행이 꺼져 있습니다.** "
                    "크롤링은 강사 PC에서만 돌아갑니다. 강사 시연 화면을 보시고, "
                    "여기서는 **스크립트 작성까지** 진행하세요."
                )

            st.info(
                "**이 탭에서 할 일** — ① 아래에서 **데이터를 받고** "
                "→ ② 그 데이터로 **시장분석 스크립트**를 만들어 AI에게 넘깁니다.\n\n"
                "코드를 직접 돌리는 과정은 **강사가 화면으로 시연**합니다."
            )

            st.markdown(
                "##### 🔬 받은 코드 직접 실행하기 &nbsp;"
                "<span style='font-size:12px;background:#fee2e2;color:#991b1b;"
                "border-radius:6px;padding:2px 8px;font-weight:700;'>강사 시연용</span>",
                unsafe_allow_html=True)
            st.caption("오류가 나도 괜찮습니다 — 오류 메시지를 다시 물어보며 고치는 것까지가 실제 개발 방식입니다.")
            with st.expander("🔒 안전하게 실행되나요?"):
                st.markdown(
                    "- 앱과 분리된 임시 폴더에서 별도 프로세스로 실행됩니다.\n"
                    "- 앱의 비밀 설정값은 전달되지 않습니다.\n"
                    "- 시스템 명령·파일 삭제 같은 명령이 있으면 실행하지 않습니다.\n"
                    "- 90초를 넘기면 자동 중단됩니다."
                )

            # 폼으로 묶어야 붙여넣은 직후 버튼을 눌러도 값이 함께 전달된다
            with st.form("pw_run_form"):
                st.text_area(
                    "받은 코드 붙여넣기",
                    height=220,
                    key="pw_user_code",
                    placeholder=("ChatGPT가 답으로 준 파이썬 코드를 붙여넣으세요.\n"
                                 "보통 이렇게 시작합니다 ↓\n"
                                 "from playwright.sync_api import sync_playwright"),
                )
                _submitted = st.form_submit_button(
                    "▶ 이 코드 실행하기", type="primary",
                    use_container_width=True, disabled=not _can_exec)

            _user_code = st.session_state.get("pw_user_code", "")

            # 붙여넣기 정리 ① 코드펜스(```python … ```)를 통째로 복사한 경우 안쪽만 사용
            _raw = _user_code or ""
            if "```" in _raw:
                _parts = _raw.split("```")
                _blocks = []
                for _bi in range(1, len(_parts), 2):      # 홀수 인덱스가 펜스 안쪽
                    _blk = _parts[_bi]
                    if _blk.startswith("python"):
                        _blk = _blk[len("python"):]
                    elif _blk.startswith("py"):
                        _blk = _blk[len("py"):]
                    _blocks.append(_blk.strip("\n"))
                if _blocks:
                    _raw = "\n".join(_blocks)

            # 붙여넣기 정리 ② Colab 전용 줄과 설치 명령 줄은 제외 (이미 설치돼 있음)
            _clean, _dropped = [], []
            for _ln in _raw.split("\n"):
                _t = _ln.strip()
                if _t.startswith(("!", "%")):
                    _dropped.append(_t)
                elif "playwright install" in _t or "pip install" in _t:
                    _dropped.append(_t)
                else:
                    _clean.append(_ln)
            _code_to_run = "\n".join(_clean)

            if _dropped:
                st.caption(
                    "ℹ️ 설치 명령 %d줄은 빼고 실행합니다 — 이 앱에는 playwright가 "
                    "이미 설치되어 있습니다. (%s)" % (len(_dropped), _dropped[0][:50])
                )
            if "```" in (_user_code or ""):
                st.caption("ℹ️ 코드블록 표시(```)가 있어 그 안쪽 코드만 골라 실행합니다.")

            _BLOCKED = [
                ("os.system", "시스템 명령 실행"),
                ("shutil.rmtree", "폴더 통째 삭제"),
                ("os.remove", "파일 삭제"),
                ("os.unlink", "파일 삭제"),
                ("secrets.toml", "앱 비밀설정 접근"),
                ("st.secrets", "앱 비밀설정 접근"),
                ("eval(", "동적 코드 실행"),
                ("exec(", "동적 코드 실행"),
                ("__import__", "동적 모듈 로딩"),
            ]
            _found = [(p, w) for p, w in _BLOCKED if p in _code_to_run]

            if _found:
                st.error(
                    "⛔ 아래 명령이 들어 있어 실행하지 않습니다 — "
                    + ", ".join("`%s`(%s)" % (p, w) for p, w in _found)
                )
                st.caption(
                    "ChatGPT에게 '설치 명령이나 파일 삭제 없이, 수집과 print 출력만 하는 "
                    "코드로 다시 만들어줘'라고 요청하면 해결됩니다."
                )

            # 파이썬 코드가 아니라 '요청문'을 붙여넣은 경우를 걸러낸다
            _c = _code_to_run
            _prompt_marks = ["만들어줘", "[코드 조건", "[수집 주소]", "[가져올 항목]",
                             "[실행 환경", "[금지]", "해줘", "알려줘"]
            _code_marks = ["import ", "print(", "def ", "with ", "for ", "="]
            _looks_prompt = (
                bool(_c.strip())
                and any(m in _c for m in _prompt_marks)
                and sum(1 for m in _code_marks if m in _c) < 2
            )

            if _submitted and not _code_to_run.strip():
                st.warning("실행할 코드가 없습니다. 위 칸에 코드를 붙여넣고 다시 눌러주세요.")
            elif _submitted and _looks_prompt:
                st.error(
                    "⚠️ **이건 파이썬 코드가 아니라 ChatGPT에게 줄 요청문입니다.**\n\n"
                    "지금 넣으신 내용은 앞 탭에서 만든 *요청 스크립트*예요. "
                    "이 요청문을 **ChatGPT에 먼저 붙여넣고**, ChatGPT가 답으로 준 "
                    "**파이썬 코드**를 이 칸에 넣어야 합니다.\n\n"
                    "파이썬 코드는 보통 `from playwright.sync_api import sync_playwright` 처럼 시작합니다."
                )
            elif _submitted and _found:
                st.error("위에 표시된 금지 명령이 있어 실행하지 않았습니다.")

            if _submitted and _code_to_run.strip() and not _found and not _looks_prompt:
                import os as _os, sys as _sys, tempfile as _tf, subprocess as _sp
                import time as _tm
                _tmpdir = _tf.mkdtemp(prefix="ainpd_run_")
                _codefile = _os.path.join(_tmpdir, "student_code.py")
                with open(_codefile, "w", encoding="utf-8") as _f:
                    _f.write(_code_to_run)

                _keep = ["PATH", "SYSTEMROOT", "TEMP", "TMP", "USERPROFILE",
                         "LOCALAPPDATA", "APPDATA", "COMSPEC", "PATHEXT", "OS",
                         "NUMBER_OF_PROCESSORS", "HOME", "LANG"]
                _env = {k: _os.environ[k] for k in _keep if k in _os.environ}
                _env["PYTHONIOENCODING"] = "utf-8"
                _env["PYTHONUNBUFFERED"] = "1"      # print가 즉시 흘러나오게

                _run_status = st.empty()
                _run_area = st.empty()
                _lines, _t0 = [], _tm.time()
                _run_status.caption("⏳ 실행 중…")

                try:
                    # -u : 출력 버퍼링 없이 실행 → 결과가 나오는 대로 화면에 표시된다
                    _p = _sp.Popen(
                        [_sys.executable, "-u", _codefile],
                        cwd=_tmpdir, env=_env,
                        stdout=_sp.PIPE, stderr=_sp.PIPE,
                        text=True, encoding="utf-8", errors="replace", bufsize=1,
                    )
                    for _ln in _p.stdout:
                        _lines.append(_ln.rstrip("\n"))
                        _run_status.caption("⏳ 실행 중… %d줄 출력 (%.0f초)"
                                            % (len(_lines), _tm.time() - _t0))
                        _run_area.code("\n".join(_lines[-40:]), language=None)
                        if _tm.time() - _t0 > 90:
                            _p.kill()
                            _lines.append("… 90초를 넘겨 중단했습니다.")
                            break
                    _p.wait(timeout=10)
                    _errtxt = (_p.stderr.read() or "") if _p.stderr else ""
                    _run = {
                        "rc": _p.returncode if _p.returncode is not None else -1,
                        "out": "\n".join(_lines)[:6000],
                        "err": _errtxt[-3000:],
                        "files": sorted(f for f in _os.listdir(_tmpdir)
                                        if f != "student_code.py"),
                        "dir": _tmpdir,
                    }
                except Exception as _e:                           # noqa: BLE001
                    _run = {"rc": -1, "out": "\n".join(_lines)[:6000], "files": [],
                            "dir": _tmpdir, "err": str(_e)[:500]}

                _run_status.empty()
                _run_area.empty()
                st.session_state["pw_run_result"] = _run
                st.session_state["pw_last_code"] = _code_to_run

            _run = st.session_state.get("pw_run_result")
            if _run:
                if _run["rc"] == 0:
                    st.success("✅ 코드가 정상적으로 끝났습니다.")
                else:
                    st.warning(
                        "⚠️ 오류가 났습니다. 당황하지 마세요 — 아래 '오류를 ChatGPT에 물어보기' "
                        "블록을 그대로 복사해 붙여넣으면 원인과 고친 코드를 받을 수 있습니다."
                    )

                if _run.get("out"):
                    st.markdown("**실행 결과 (출력)**")
                    st.code(_run["out"], language=None)
                    _dl1, _dl2 = st.columns(2)
                    with _dl1:
                        st.download_button(
                            "📥 결과를 CSV로 저장",
                            data=_run["out"].encode("utf-8-sig"),
                            file_name="실행결과.csv", mime="text/csv",
                            key="run_out_csv", use_container_width=True,
                        )
                    with _dl2:
                        st.download_button(
                            "📄 결과를 텍스트로 저장",
                            data=_run["out"].encode("utf-8-sig"),
                            file_name="실행결과.txt", mime="text/plain",
                            key="run_out_txt", use_container_width=True,
                        )
                elif _run["rc"] == 0:
                    st.caption(
                        "출력이 없습니다. 코드에 `print(...)`가 없으면 결과가 화면에 보이지 않습니다. "
                        "ChatGPT에게 '결과를 print로 출력해줘'라고 요청해보세요."
                    )

                if _run.get("files"):
                    st.caption("생성된 파일: " + ", ".join(_run["files"]))
                    import os as _os2
                    for _fn in _run["files"][:3]:
                        _fp = _os2.path.join(_run["dir"], _fn)
                        try:
                            if _os2.path.getsize(_fp) <= 3_000_000:
                                with open(_fp, "rb") as _fh:
                                    st.download_button(
                                        "📥 %s 내려받기" % _fn, data=_fh.read(),
                                        file_name=_fn, key="dl_%s" % _fn,
                                    )
                        except Exception:                          # noqa: BLE001
                            pass

                if _run.get("err"):
                    _e = _run["err"]
                    _hints = []
                    if "invalid character" in _e or "[코드 조건" in _e:
                        _hints.append(
                            "**요청문을 붙여넣으신 것 같습니다.** 이 칸에는 ChatGPT가 "
                            "*답으로 준 파이썬 코드*를 넣어야 합니다. 요청문은 ChatGPT에 넣는 것입니다.")
                    elif "SyntaxError" in _e:
                        _hints.append(
                            "**문법 오류** — 코드 말고 설명 문장까지 함께 붙여넣지 않았는지 "
                            "확인하세요. 코드 부분만 복사하면 해결되는 경우가 많습니다.")
                    if "ModuleNotFoundError" in _e or "No module named" in _e:
                        _mm = _e.split("No module named")[-1].strip().strip("'\"" )[:30] \
                            if "No module named" in _e else ""
                        _hints.append(
                            "**설치되지 않은 라이브러리**%s를 쓰고 있습니다. ChatGPT에게 "
                            "'playwright만 써서 다시 만들어줘'라고 요청하세요."
                            % ((" `" + _mm + "` ") if _mm else " "))
                    if "async" in _e or "coroutine" in _e or "asyncio" in _e:
                        _hints.append(
                            "**비동기(async) 코드**입니다. ChatGPT에게 "
                            "'async 말고 sync_playwright 동기 방식으로 다시 만들어줘'라고 하세요.")
                    if "Timeout" in _e or "timeout" in _e:
                        _hints.append(
                            "**화면에서 상품을 못 찾았습니다.** 셀렉터를 "
                            "`a[href*=\"/goods/\"]` 로 바꿔달라고 요청하세요.")
                    if "Executable doesn" in _e or "playwright install" in _e:
                        _hints.append(
                            "브라우저를 찾지 못했습니다. 강사에게 알려주세요 "
                            "(앱 서버에 playwright 브라우저 설치가 필요합니다).")
                    if _hints:
                        st.info("💡 **아마 이 문제입니다**\n\n" +
                                "\n\n".join("- " + h for h in _hints))

                    st.markdown("**오류 메시지**")
                    st.code(_e, language=None)
                    _fix_prompt = (
                        "아래 파이썬 코드를 실행했더니 오류가 났어. "
                        "원인을 알려주고 고친 전체 코드를 다시 줘.\n\n"
                        "[실행한 코드]\n"
                        + st.session_state.get("pw_last_code", "")[:3000] + "\n\n"
                        "[오류 메시지]\n" + _run["err"] + "\n\n"
                        "[요청]\n"
                        "- 무엇이 문제였는지 한두 줄로 먼저 설명해줘.\n"
                        "- 고친 코드는 일부가 아니라 전체를 다시 줘.\n"
                        "- 설치 명령(!pip install 등)은 빼고, 수집과 print 출력만 하는 코드로 만들어줘.\n"
                        "- 화면 구조가 바뀌어 못 찾는 것이라면 셀렉터를 어떻게 확인하는지도 알려줘."
                    )
                    st.markdown("**🔁 이 오류를 ChatGPT에 물어보기 — 아래를 복사해 붙여넣으세요**")
                    st.code(_fix_prompt, language=None)

            # ── 코드가 잘 안 될 때를 위한 앱 내장 수집기 ──
            st.markdown("---")
            st.markdown("##### 🚀 코드가 잘 안 되면 — 앱 내장 수집기로 바로 보기")
            st.caption("코드가 막히면 여기서 바로 수집해 다음 단계로 넘어갈 수 있습니다.")
            _mode = st.radio(
                "가져오는 방법", ["카테고리", "검색어 직접입력"],
                horizontal=True, key="kurly_mode",
                help="카테고리는 마켓컬리가 실제로 분류해 둔 매대를 그대로 가져옵니다. "
                     "검색과 달리 엉뚱한 품목이 섞이지 않습니다.",
            )
            _rc1, _rc2, _rc3, _rc4 = st.columns([2.6, 1.4, 1.4, 1])
            with _rc1:
                if _mode == "카테고리":
                    # 음료 유형별 하위 카테고리 9종 + 대분류 4종 (전부 수집 확인)
                    _CATS = [
                        "탄산·스포츠음료", "탄산수", "과일·야채음료", "차음료",
                        "커피음료", "콜드브루", "액상차·청", "생수·얼음", "어린이음료",
                        "생수·음료 전체", "커피·차 전체", "유제품 전체", "건강식품 전체",
                    ]
                    _run_cat = st.selectbox("음료 카테고리", _CATS, key="kurly_run_cat2")
                    _run_kw = ""
                else:
                    _run_cat = ""
                    _run_kw = st.text_input(
                        "검색어 (자유 입력)",
                        value=st.session_state.get("pw_kw_final", "탄산음료"),
                        key="kurly_run_kw",
                        placeholder="예: 제로 탄산, 무가당 스파클링",
                    )
            with _rc2:
                _SORT_RUN = ["추천순", "판매량순", "신상품순",
                             "낮은 가격순", "높은 가격순", "혜택순"]
                _sv = st.session_state.get("pw_sort_final", "추천순")
                _run_sort = st.selectbox(
                    "정렬", _SORT_RUN,
                    index=_SORT_RUN.index(_sv) if _sv in _SORT_RUN else 0,
                    key="kurly_run_sort",
                )
            with _rc3:
                _run_price = st.selectbox(
                    "가격대",
                    ["전체", "4천원 미만", "4천~8천원", "8천~2만원", "2만원 이상"],
                    key="kurly_run_price",
                )
            with _rc4:
                _run_n = st.selectbox("개수", [50, 100, 200, 300, 500],
                                      index=1, key="kurly_run_n")

            _run_nf = st.text_input(
                "🔍 상품명 걸러내기 (선택)",
                value=st.session_state.get("pw_detail_final", ""),
                key="kurly_run_nf",
                placeholder="예: 주스,착즙,과즙  ← 쉼표로 여러 개, 하나라도 들어간 상품만 수집",
            )


            # 실측(2026-08)으로 확인한, 상품이 실제로 없는 조합
            _KNOWN_EMPTY = {("건강식품 전체", "4천원 미만")}
            if (_run_cat, _run_price) in _KNOWN_EMPTY:
                st.warning(
                    "⚠️ **이 조합은 마켓컬리에 해당하는 상품이 없습니다.** "
                    "건강식품은 가장 싼 상품이 6천원 안팎이라 4천원 미만 구간이 비어 있습니다. "
                    "가격대를 바꿔서 수집하세요."
                )
            elif _run_price != "전체" or _run_nf.strip():
                st.caption("⏱️ 조건을 걸면 더 오래 걸립니다 (최대 30초)")

            _ALL_COLS = ["상품명", "브랜드", "용량", "설명문구", "정가",
                         "할인가", "할인율", "쿠폰가", "최종가", "리뷰수", "링크"]
            _show_cols = st.pills(
                "표에 보일 항목", _ALL_COLS, selection_mode="multi",
                default=["상품명", "브랜드", "용량", "최종가", "리뷰수"],
                key="kurly_show_cols",
            )
            st.caption("100개 약 10초 · 500개 약 35초")

            if st.button("🚀 마켓컬리에서 수집 시작", key="kurly_run_btn",
                         use_container_width=True, disabled=not _can_exec):
                import subprocess as _sp2, sys as _sys2, json as _json2, os as _os3
                _script = _os3.path.join(
                    _os3.path.dirname(_os3.path.abspath(__file__)), "kurly_collect.py")

                # 수집 과정을 실시간으로 보여준다 — 무엇을 긁어오고 있는지 눈으로 확인
                _status = st.empty()
                _bar = st.progress(0.0, text="시작하는 중…")
                _live = st.empty()
                _live_rows = []
                _res = {"ok": False, "error": "결과를 받지 못했습니다"}

                try:
                    _cenv = dict(_os3.environ)
                    _cenv["PYTHONIOENCODING"] = "utf-8"
                    _proc = _sp2.Popen(
                        [_sys2.executable, _script, _run_kw, str(_run_n),
                         _run_sort, _run_cat, _run_price, _run_nf],
                        stdout=_sp2.PIPE, stderr=_sp2.PIPE, env=_cenv,
                        text=True, encoding="utf-8", errors="replace", bufsize=1,
                    )
                    for _line in _proc.stdout:
                        try:
                            _m = _json2.loads(_line)
                        except Exception:                        # noqa: BLE001
                            continue
                        _t = _m.get("t")
                        if _t == "s":
                            _status.caption("⏳ " + str(_m.get("msg", "")))
                        elif _t == "p":
                            _live_rows.append(_m["row"])
                            _done, _total = _m.get("done", 0), max(_m.get("total", 1), 1)
                            _bar.progress(
                                min(_done / _total, 1.0),
                                text="%d / %d 수집 — %s"
                                     % (_done, _total, str(_m["row"].get("상품명", ""))[:40]),
                            )
                            if _done <= 3 or _done % 5 == 0:
                                _live.dataframe(_live_rows[-8:],
                                                use_container_width=True, height=230)
                        elif _t == "r":
                            _res = _m
                    _proc.wait(timeout=60)
                    if not _res.get("ok") and _proc.returncode not in (0, None):
                        _err = (_proc.stderr.read() or "")[-400:] if _proc.stderr else ""
                        if _err:
                            _res = {"ok": False, "error": _err}
                except Exception as _e:                          # noqa: BLE001
                    _res = {"ok": False, "error": str(_e)[:300]}

                _status.empty()
                _bar.empty()
                _live.empty()
                st.session_state["kurly_result"] = _res

            # 설치가 안 된 환경(온라인 배포본 등)에서도 실습이 이어지도록
            # 미리 수집해둔 실제 데이터를 불러올 수 있게 한다
            import os as _os4
            import json as _json4
            _sdir = _os4.path.join(_os4.path.dirname(_os4.path.abspath(__file__)), "sample_data")
            _sfiles = {}
            if _os4.path.isdir(_sdir):
                for _f in sorted(_os4.listdir(_sdir)):
                    if _f.endswith(".json"):
                        _sfiles[_f[len("kurly_"):-len(".json")].replace("_", "·")] = \
                            _os4.path.join(_sdir, _f)

            if _sfiles:
                st.markdown("---")
                st.markdown(
                    "##### 📦 ① 데이터 받기 &nbsp;"
                    "<span style='font-size:12px;background:#dcfce7;color:#166534;"
                    "border-radius:6px;padding:2px 8px;font-weight:700;'>실습자</span>",
                    unsafe_allow_html=True)
                st.caption(
                    "마켓컬리에서 실제로 수집해둔 데이터입니다. "
                    "카테고리를 고르고 불러오면 아래에서 바로 분석까지 진행할 수 있습니다."
                )
                _sc1, _sc2 = st.columns([3, 1])
                with _sc1:
                    _spick = st.selectbox("카테고리", list(_sfiles.keys()),
                                          key="kurly_sample_pick")
                with _sc2:
                    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                    _sload = st.button("📥 불러오기", key="kurly_sample_btn",
                                       use_container_width=True)
                if _sload:
                    try:
                        with open(_sfiles[_spick], encoding="utf-8") as _fh:
                            _sd = _json4.load(_fh)
                        st.session_state["kurly_result"] = {
                            "ok": True,
                            "keyword": _sd.get("category", _spick),
                            "count": len(_sd.get("rows", [])),
                            "rows": _sd.get("rows", []),
                        }
                        st.session_state["kurly_sample_note"] = "%s · %s 수집" % (
                            _sd.get("sort", "판매량순"), _sd.get("collected", ""))
                    except Exception as _e:                       # noqa: BLE001
                        st.error("불러오기 실패: %s" % str(_e)[:200])

            _kres = st.session_state.get("kurly_result")
            if _kres and not _kres.get("ok"):
                st.error("수집에 실패했습니다 — %s" % _kres.get("error", ""))
                st.caption(
                    "사이트 화면 구조가 바뀌었거나 네트워크가 막혀 있을 수 있습니다. "
                    "이런 상황이 바로 크롤링의 한계입니다 — 코드가 아니라 사이트가 바뀌면 깨집니다."
                )
            elif _kres and _kres.get("ok"):
                _rows = _kres.get("rows") or []
                _note = st.session_state.get("kurly_sample_note")
                st.success(
                    "✅ **%d개 상품 데이터입니다.** "
                    "AI가 지어낸 값이 아니라 마켓컬리 화면에서 그대로 읽어온 것입니다.%s"
                    % (len(_rows), (" (%s)" % _note) if _note else "")
                )
                if len(_rows) < _run_n:
                    st.info(
                        "요청한 %d개 중 %d개를 찾았습니다. 걸어둔 조건에 맞는 상품이 "
                        "그만큼뿐입니다 — 조건을 넓히면 더 모을 수 있습니다."
                        % (_run_n, len(_rows))
                    )
                _cols = [c for c in (_show_cols or _ALL_COLS) if c in (_rows[0] if _rows else {})]
                _view = [{c: r.get(c) for c in _cols} for r in _rows] if _cols else _rows
                st.dataframe(_view, use_container_width=True, height=320)

                import io as _io, csv as _csv
                _buf = _io.StringIO()
                if _rows:
                    _w = _csv.DictWriter(_buf, fieldnames=list(_rows[0].keys()))
                    _w.writeheader()
                    _w.writerows(_rows)
                st.download_button(
                    "📥 수집 결과 CSV로 저장",
                    data=_buf.getvalue().encode("utf-8-sig"),
                    file_name="kurly_%s.csv" % (_run_cat or _kres.get("keyword") or "수집"),
                    mime="text/csv", key="kurly_csv",
                )

                _data_lines = []
                for _r in _rows:
                    _data_lines.append("%s | %s | %s | %s" % (
                        _r.get("브랜드") or "-",
                        _r.get("상품명") or "-",
                        _r.get("용량") or "-",
                        ("%s원" % _r["최종가"]) if _r.get("최종가") else "-",
                    ))
                _analysis_script = (
                    "아래는 마켓컬리에서 '" + str(_kres.get("keyword", "")) + "'로 검색해 "
                    + str(_run_sort) + " 기준으로 실제 수집한 상품 " + str(len(_rows)) + "건이다.\n"
                    "이 데이터만 근거로 시장 현황을 분석해줘.\n\n"
                    "[데이터] 브랜드 | 상품명 | 용량 | 가격\n"
                    + "\n".join(_data_lines) + "\n\n"
                    "[분석 항목]\n"
                    + st.session_state.get(
                        "pw_goal_lines",
                        "1. 브랜드별 상품 수와 상위 브랜드\n2. 가격 구간별 상품 수와 평균가")
                    + "\n\n"
                    "[주의]\n"
                    "- 위 데이터에 없는 값(판매량·점유율·리뷰수)은 만들어내지 마라.\n"
                    "- 데이터에서 직접 셀 수 있는 것만 제시하고, 어떻게 셌는지 밝혀라."
                )

                st.markdown("---")
                st.markdown("##### 🤖 ② 이 데이터로 GPT에게 시장분석 시키기")
                st.caption(
                    "아래 스크립트에는 방금 수집한 실제 데이터가 그대로 들어 있습니다. "
                    "복사해서 ChatGPT에 붙여넣으면 **근거 있는 시장분석**이 나옵니다."
                )
                st.code(_analysis_script + _SUBMIT_INSTRUCTION, language=None)
                st.session_state["kurly_analysis_script"] = _analysis_script

            with st.expander("⚠️ 회사 업무로 쓰기 전에 알아둘 것"):
                st.markdown(
                    "- robots.txt가 허용해도 사이트 **이용약관**이 자동수집을 막을 수 있습니다.\n"
                    "- 대량·반복 수집은 서버 부하로 문제가 됩니다.\n"
                    "- 수집한 데이터를 외부에 재배포하는 것은 또 다른 문제입니다."
                )
            _hw_ui("수집코드실행",
                   st.session_state.get("kurly_analysis_script")
                   or st.session_state.get("pw_user_code", ""),
                   "code_run_hw_submit",
                   ai_label="GPT 분석 결과",
                   title="과제 제출 — 수집 결과 + 시장분석")


    if _CRAWL_ONLY:
        st.stop()

    with tab_food:
        show_step_guide(
            _S4_STEPS, 1,
            todo="식품안전나라 품목제조보고 데이터를 AI에 학습시켜 원재료를 분석합니다.",
            uses="앞 단계에서 정한 제품 카테고리와 분석 관점",
            produces="경쟁 제품 원재료·성분 분석 결과",
            minutes=15,
        )
        # 실습 시간 확보를 위해 과채주스 파일은 내리고 혼합음료 1종만 제공
        _btn_food_html = (
            f'<a href="https://docs.google.com/spreadsheets/d/1nDSvSvUCZLb9GheRSNI31fQQ1mDUrrDg/edit?usp=drive_link&ouid=117628977970091786229&rtpof=true&sd=true" target="_blank" '
            f'style="display:inline-block;padding:8px 18px;background:#fef08a;border:1.5px solid #f59e0b;'
            f'border-radius:8px;color:#92400e;font-weight:700;font-size:13px;text-decoration:none;">'
            f'📥 혼합음료 데이터 다운로드</a>'
        )

        sub_food_ex, sub_food_task = st.tabs(["📖 예시 스크립트", "📋 스크립트 작성 과제"])

        # ── 예시 스크립트 ──
        with sub_food_ex:
            st.markdown("#### 🗂️ 식품안전나라 품목제조보고서 분석")
            st.markdown("**Step 1. 데이터 파일 다운로드**")
            st.info("아래 버튼에서 식품안전나라 품목제조보고서 데이터를 다운로드한 뒤 ChatGPT에 업로드하세요.")
            st.warning("⚠️ 데이터 분석용 토큰 소모가 크므로, 분석용 파일은 **혼합음료 품목제조보고서 파일만** 업로드해주세요.")
            st.markdown(_btn_food_html, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("**Step 2. ChatGPT에 파일 업로드 후 아래 스크립트 입력**")
            st.code("""#자료배경
품목제조보고서의 구성은 업체명, 품목유형, 제품명, 성분개수, 성분및 원료, 일자, 유형, 제품형태로 구성되어있다.

#요청목적
이 데이터로부터 음료개발에 필요한 정보를 가져올거야

#요청사항
1. 제품에 사용된 주요원재료, 배합순서, 제품유형, 성분개수로부터 배합비 개발에 필요한 배합순서 및 원재료우선순위를 학습한다.
2. 제품명으로부터 원재료를 추정하고, 생산트렌드를 학습한다.
3. 사용된 원재료로부터 사용빈도수를 학습한다.
4. 이 요청사항은 신제품 음료배합비를 작성하기 위한 데이터이다.

#처리제외
1. 제품명으로부터 건강기능식품등 음료와 관계없는 데이터는 제외한다.

#이외의 요청사항
1. 이 자료로 무엇을 할수있는지 나에게 알려줘
2. 명령을 수행하기전, 사용자에게 지시한 의도가 맞는지 확인하고, 선택여부를 물어본후 출력한다.""", language=None)

        # ── 스크립트 작성 과제 ──
        with sub_food_task:
            st.markdown("#### 📋 식품 전문 데이터 분석 스크립트 작성 과제")
            st.info(
                "**과제 목표:** 업로드한 식품 데이터 파일에 맞는 분석 스크립트를 직접 작성해보세요.\n\n"
                "아래 힌트 항목을 선택하면 초안이 자동 생성됩니다. 내용을 수정·보완한 뒤 ChatGPT에 붙여넣으세요."
            )
            st.warning("⚠️ 데이터 분석용 토큰 소모가 크므로, 분석용 파일은 **혼합음료 품목제조보고서 파일만** 업로드해주세요.")
            st.markdown(_btn_food_html, unsafe_allow_html=True)
            st.markdown("---")

            # ── 힌트 장치 (2행 × 2열) ──
            st.markdown("**🔧 힌트 선택 — 항목을 골라 초안을 생성하세요**")

            # 행 1: 자료배경설명 | 요청목적
            col_f1, col_f2 = st.columns([3, 3])
            with col_f1:
                st.caption("📂 자료배경설명 — 품목제조보고서 구성 항목 선택 (복수)")
                _BG_OPTS = [  # 간소화: 5개 -> 4개 (제외: 성분개수)
                    "업체명",
                    "품목유형",
                    "제품명",
                    "성분 및 사용한 원재료",
                ]
                food_bg = st.pills("자료배경설명", _BG_OPTS, selection_mode="multi", key="food_bg", label_visibility="collapsed")

            with col_f2:
                st.caption("🎯 요청목적")
                _PURPOSE_OPTS = [  # 간소화: 5개 -> 4개 (제외: 신제품 컨셉 수립 참고)
                    "배합비 개발을 위한 원재료 분석",
                    "음료 카테고리별 트렌드 파악",
                    "경쟁 제품 성분 비교",
                    "소비자 선호 원재료 도출",
                ]
                food_purpose = st.pills("요청목적", _PURPOSE_OPTS, key="food_purpose", label_visibility="collapsed")

            # 행 2: 요청사항(multi) | 처리제외(multi)
            col_f3, col_f4 = st.columns([3, 3])
            with col_f3:
                st.caption("📋 요청사항 (복수 선택)")
                _REQ_OPTS = [  # 간소화: 7개 -> 4개 (제외: 배합 순서 도출, 제품명 원재료 추정, 카테고리별 성분 비교)
                    "주요 원재료 사용 빈도 분석",
                    "제품유형별 분류 정리",
                    "생산 트렌드 분석",
                    "신제품 개발 시사점 도출",
                ]
                food_reqs = st.pills("요청사항", _REQ_OPTS, selection_mode="multi", key="food_reqs", label_visibility="collapsed")

            with col_f4:
                st.caption("🚫 처리 제외 (복수 선택)")
                _EXCL_OPTS = [  # 간소화: 5개 -> 4개 (제외: 10년 이상 된 데이터 제외)
                    "음료와 관계없는 품목 제외",
                    "건강기능식품 제외",
                    "중복 데이터 제거",
                    "원재료 정보 불명확한 제품 제외",
                ]
                food_excls = st.pills("처리제외", _EXCL_OPTS, selection_mode="multi", key="food_excls", label_visibility="collapsed")

            # 행 3: 이외 요청사항(multi, 전폭)
            st.caption("💬 이외 요청사항 (복수 선택)")
            _OTHER_OPTS = [  # 간소화: 5개 -> 4개 (제외: 추가 분석 가능 항목 제안)
                "할 수 있는 작업 목록 먼저 제시",
                "수행 전 사용자 확인 후 진행",
                "학습 결과 요약 제공 (10줄 이내)",
                "가짜 데이터 생성 금지",
            ]
            food_others = st.pills("이외요청", _OTHER_OPTS, selection_mode="multi", key="food_others", label_visibility="collapsed")

            st.markdown("---")

            # ── 초안 생성 (pending key 패턴) ──
            if "food_draft_pending" in st.session_state:
                st.session_state["food_user_script"] = st.session_state.pop("food_draft_pending")

            # 노란색 추가 요청사항 입력 영역
            st.markdown("""<div style="background:#fefce8;border-radius:10px;padding:10px 16px;
border:2px solid #fde047;margin:8px 0 4px 0;">
<b style="color:#854d0e;">✏️ 추가 요청사항</b>
<span style="font-size:12px;color:#92400e;margin-left:8px;">스크립트에 추가할 내용을 자유롭게 입력하세요 (초안에 자동 포함)</span>
</div>""", unsafe_allow_html=True)
            food_extra = st.text_area("food_extra_label", key="food_extra", height=80,
                placeholder="예: 특정 성분 우선 분석, 특정 제조사 제외, 추가 출력 형식 요청 등",
                label_visibility="collapsed")

            st.markdown("---")

            if st.button("✏️ 선택 항목으로 초안 생성", key="food_hint_gen_btn", use_container_width=True):
                _fbg_fields = food_bg or ["업체명", "품목유형", "제품명", "성분개수", "성분 및 사용한 원재료"]
                _fbg      = f"품목제조보고서의 구성은 {', '.join(_fbg_fields)}로 구성되어있다."
                _fpurpose = food_purpose or "배합비 개발을 위한 원재료 분석"
                _freqs    = food_reqs or ["주요 원재료 사용 빈도 분석", "배합 순서 및 우선순위 도출"]
                _fexcls   = food_excls or ["음료와 관계없는 품목 제외"]
                _fothers  = food_others or ["수행 전 사용자 확인 후 진행"]
                _freqs_str  = "\n".join(f"{i+1}. {r}" for i, r in enumerate(_freqs))
                _fexcls_str = "\n".join(f"{i+1}. {e}" for i, e in enumerate(_fexcls))
                _fothers_str = "\n".join(f"{i+1}. {o}" for i, o in enumerate(_fothers))
                _food_draft = f"""#진행조건
품목제조보고서 자료를 입력받기 전까지 분석 결과를 출력하지 않는다.
자료 입력 완료 후 아래 요청사항에 따라 분석을 진행한다.

#자료배경설명
{_fbg}

#요청목적
{_fpurpose}

#요청사항
{_freqs_str}

#처리제외
{_fexcls_str}

#이외의 요청사항
{_fothers_str}"""
                if st.session_state.get("food_extra", "").strip():
                    _food_draft += f"\n\n#추가 요청사항\n{st.session_state['food_extra']}"
                st.session_state["food_draft_pending"] = _food_draft

            food_script = st.text_area(
                "📝 스크립트 작성",
                key="food_user_script",
                height=300,
                placeholder=(
                    "위 힌트에서 항목을 선택한 뒤 [초안 생성] 버튼을 누르거나,\n"
                    "아래에 직접 스크립트를 작성해보세요.\n\n"
                    "#자료배경설명\n#요청목적\n#요청사항\n#처리제외\n#이외의 요청사항"
                ),
            )

            if food_script.strip():
                st.caption("📋 아래 코드 블록 우측 상단 복사 아이콘 클릭 → ChatGPT, Gemini 등에 붙여넣기")
                st.code(food_script + _SUBMIT_INSTRUCTION, language=None)

            # 파일링크 불필요: 식품전문정보 분석 스크립트는 텍스트 제출로 충분
            _hw_ui("식품전문정보분석", st.session_state.get("food_user_script", ""), "food_hw_submit")

    # ── 탭 3: 시장조사 데이터 학습 (편의점 매대 사진 분석) ──
    with tab_learn:
        show_step_guide(
            _S4_STEPS, 2,
            todo="편의점 매대 사진을 AI에 올려 진열 SKU 구색을 정량 분석합니다.",
            uses="앞 두 단계에서 잡은 카테고리 기준",
            produces="매대 SKU 점유율·경쟁현황 분석 결과",
            minutes=12,
        )
        # 편의점 매대 사진 Google Drive 파일 ID — 실습 시간 확보를 위해 5장 압축본에서 2장 개별 링크로 축소
        _CONV_PHOTO_IDS = [
            ("매대 사진 1", "1aYm-YdkaDYXL0bCWeI0-13hTepSvVXYo"),
            ("매대 사진 2", "14niYtDCYzyG_zO44w3K7E9JIQoSvG4VV"),
        ]

        def _photo_btn(label, fid):
            return (
                f'<a href="https://drive.google.com/file/d/{fid}/view" target="_blank" '
                f'style="display:inline-block;padding:9px 20px;background:#e0f2fe;border:1.5px solid #38bdf8;'
                f'border-radius:8px;color:#0369a1;font-weight:700;font-size:14px;text-decoration:none;margin:3px 2px;">'
                f'🖼️ {label} 다운로드</a>'
            )

        _photo_html = "".join(_photo_btn(lbl, fid) for lbl, fid in _CONV_PHOTO_IDS)

        sub_learn_ex, sub_learn_task = st.tabs(["📖 예시 스크립트", "📋 스크립트 작성 과제"])

        # ── 예시 스크립트 ──
        with sub_learn_ex:
            st.markdown("#### 🏪 편의점 매대 사진 분석 — 예시 스크립트")
            st.markdown("**Step 1. 편의점 매대 사진 다운로드 (2장)**")
            st.info("아래 사진 2장을 모두 다운로드한 뒤 ChatGPT 또는 NotebookLM에 이미지로 업로드하세요.")
            st.markdown(_photo_html, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("**Step 2. 이미지 업로드 후 아래 스크립트 입력**")
            st.code("""1. 음료개발 연구원 관점에서 편의점 음료 구색 SKU를 분석하고, 업로드 해준 이미지에서 추출해 (메인 질문)

2. 진열 음료의 음료유형별 세부분류에 대한 정량분석을 통해 시장점유율과 경쟁현황/컨셉/트렌드 분석 진행해

3. raw 데이터 추출하고 여기에 모두 출력

4. 명령: 너의 시스템상 고부하가 걸리지 않게 나눠서 출력

5. 보고서를 아래의 양식으로 작성
   5.1 음료유형별 | SKU 개수 | SKU 점유율 (%) | 전략적 특징
   5.2 전체품 raw 데이터 정량 결과""", language=None)

        # ── 스크립트 작성 과제 ──
        with sub_learn_task:
            st.markdown("#### 📋 편의점 매대 사진 분석 스크립트 작성 과제")
            st.info(
                "**과제 목표:** 편의점 매대 사진을 AI에 업로드하고 직접 분석 스크립트를 작성해보세요.\n\n"
                "사진을 먼저 다운로드한 뒤, 아래 힌트 항목을 선택하여 나만의 분석 스크립트 초안을 생성하세요."
            )
            st.markdown("**Step 1. 편의점 매대 사진 다운로드 (2장)**")
            st.markdown(_photo_html, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("**Step 2. 힌트 선택 후 스크립트 초안 생성**")
            st.caption("💡 노란색 직접 입력란에 텍스트 입력 후 **Enter**를 눌러 적용하세요.")

            def _yellow_input(label, key, placeholder="직접 입력"):
                st.markdown(
                    f'<div style="background:#fefce8;border-radius:6px;padding:4px 10px 2px 10px;'
                    f'border:1.5px solid #fde047;margin-top:4px;">'
                    f'<span style="font-size:11px;color:#854d0e;font-weight:600;">✏️ {label}</span></div>',
                    unsafe_allow_html=True,
                )
                return st.text_input(key, key=key, placeholder=placeholder, label_visibility="collapsed")

            # 행 1: 분석 관점 | 음료 카테고리
            col_lrn1, col_lrn2 = st.columns([3, 3])
            with col_lrn1:
                st.caption("👁️ 분석 관점")
                _VIEW_OPTS = ["음료개발 연구원", "음료 브랜드 마케터", "카테고리 MD", "소비자 트렌드 분석가"]
                lrn_view = st.pills("분석관점", _VIEW_OPTS, key="lrn_view", label_visibility="collapsed")
                lrn_view_custom = _yellow_input("직접 입력 (예: 식품 MD)", "lrn_view_custom", "선택 외 관점 직접 입력")

            with col_lrn2:
                st.caption("🥤 음료 카테고리 범위")
                # 간소화: 6개 -> 4개 (제외: 커피·차 음료, 과채음료)
                _SCOPE_OPTS = ["RTD 음료 전체", "탄산음료", "기능성·에너지 음료", "식물성 음료"]
                lrn_scope = st.pills("카테고리범위", _SCOPE_OPTS, key="lrn_scope", label_visibility="collapsed")
                lrn_scope_custom = _yellow_input("직접 입력 (예: 제로슈거 음료)", "lrn_scope_custom", "선택 외 카테고리 직접 입력")

            # 행 2: 분석 항목(multi) | 출력 방식(multi)
            col_lrn3, col_lrn4 = st.columns([3, 3])
            with col_lrn3:
                st.caption("🔍 분석 항목 (복수 선택)")
                _ITEM_OPTS = [  # 간소화: 7개 -> 4개 (제외: 카테고리별 분류, 가격대 분포, 신제품 출시 현황)
                    "SKU 구성 및 점유율",
                    "브랜드·제조사 현황",
                    "컨셉·포지셔닝 분석",
                    "트렌드 키워드 도출",
                ]
                lrn_items = st.pills("분석항목", _ITEM_OPTS, selection_mode="multi", key="lrn_items", label_visibility="collapsed")
                lrn_items_custom = _yellow_input("직접 입력 (예: 용량별 분포)", "lrn_items_custom", "추가 분석 항목 직접 입력")

            with col_lrn4:
                st.caption("📄 출력 방식 (복수 선택)")
                _OUT_OPTS = [  # 간소화: 5개 -> 4개 (제외: 요약문 추가)
                    "표 형식 정리",
                    "raw 데이터 전체 출력",
                    "단계별 나눠서 출력",
                    "전략적 특징 포함",
                ]
                lrn_outs = st.pills("출력방식", _OUT_OPTS, selection_mode="multi", key="lrn_outs", label_visibility="collapsed")
                lrn_outs_custom = _yellow_input("직접 입력 (예: 그래프 포함)", "lrn_outs_custom", "추가 출력 방식 직접 입력")

            # 행 3: 보고서 항목(multi, 전폭)
            st.caption("📊 보고서 포함 항목 (복수 선택)")
            _REPORT_OPTS = [  # 간소화: 5개 -> 4개 (제외: 경쟁현황 요약)
                "음료유형별 SKU 개수",
                "SKU 점유율 (%)",
                "전략적 특징 분석",
                "신제품 트렌드 시사점",
            ]
            lrn_report = st.pills("보고서항목", _REPORT_OPTS, selection_mode="multi", key="lrn_report", label_visibility="collapsed")
            lrn_report_custom = _yellow_input("직접 입력 (예: 브랜드별 매출 순위)", "lrn_report_custom", "추가 보고서 항목 직접 입력")

            st.markdown("---")

            # ── 초안 생성 (pending key 패턴) ──
            if "learn_draft_pending" in st.session_state:
                st.session_state["learn_user_script"] = st.session_state.pop("learn_draft_pending")

            if st.button("✏️ 선택 항목으로 초안 생성", key="learn_hint_gen_btn", use_container_width=True):
                # 선택 pills + 직접입력 모두 결합
                _lview  = ", ".join(filter(None, [lrn_view, lrn_view_custom.strip()])) or "음료개발 연구원"
                _lscope = ", ".join(filter(None, [lrn_scope, lrn_scope_custom.strip()])) or "RTD 음료 전체"
                _litems = (list(lrn_items or []) + ([lrn_items_custom.strip()] if lrn_items_custom.strip() else [])) or ["SKU 구성 및 점유율", "카테고리별 분류"]
                _louts  = (list(lrn_outs or []) + ([lrn_outs_custom.strip()] if lrn_outs_custom.strip() else [])) or ["표 형식 정리", "raw 데이터 전체 출력"]
                _lrep   = (list(lrn_report or []) + ([lrn_report_custom.strip()] if lrn_report_custom.strip() else [])) or ["음료유형별 SKU 개수", "SKU 점유율 (%)"]
                _litems_str = "\n".join(f"{i+1}. {it}" for i, it in enumerate(_litems))
                _lout_str   = " / ".join(_louts)
                _lrep_str   = " | ".join(_lrep)
                _learn_draft = f"""1. {_lview} 관점에서 편의점 {_lscope} 카테고리의 SKU를 분석하고, 업로드한 이미지에서 추출해 (메인 질문)

2. 진열 음료의 음료유형별 세부분류에 대한 정량분석을 통해 시장점유율과 경쟁현황/컨셉/트렌드 분석 진행해

분석 항목:
{_litems_str}

3. raw 데이터 추출하고 여기에 모두 출력

4. 출력 방식: {_lout_str}
   시스템 고부하가 걸리지 않게 나눠서 출력

5. 보고서를 아래의 양식으로 작성
   {_lrep_str}"""
                st.session_state["learn_draft_pending"] = _learn_draft

            learn_script = st.text_area(
                "📝 스크립트 작성",
                key="learn_user_script",
                height=300,
                placeholder=(
                    "위 힌트에서 항목을 선택한 뒤 [초안 생성] 버튼을 누르거나,\n"
                    "아래에 직접 분석 스크립트를 작성해보세요.\n\n"
                    "1. (분석 관점 + 대상)\n2. (정량분석 방법)\n3. (출력 요청)\n4. (출력 제약)\n5. (보고서 양식)"
                ),
            )

            if learn_script.strip():
                st.caption("📋 아래 코드 블록 우측 상단 복사 아이콘 클릭 → ChatGPT, Gemini 등에 붙여넣기")
                st.code(learn_script + _SUBMIT_INSTRUCTION, language=None)

            # 파일링크: NotebookLM에서 만든 슬라이드/오디오 링크를 제출
            _hw_ui("시장조사학습", st.session_state.get("learn_user_script", ""), "learn_hw_submit",
                   with_file=True)

    # ── 탭 4: 보고서 작성하기 ──
    with tab_report:
        show_step_guide(
            _S4_STEPS, 3,
            todo="앞 세 단계의 분석 결과를 하나의 시장분석 보고서로 합칩니다.",
            uses="온라인 분석 · 원재료 분석 · 매대 SKU 분석 결과 3종",
            produces="신제품 개발 시장분석 보고서",
            minutes=15,
        )
        st.markdown("#### 📝 신제품 개발 시장 분석 보고서 작성")

        # ── 학습자 미션 카드 ──
        st.markdown("""
<div style="background:#f0f9ff;border-left:5px solid #3b82f6;border-radius:10px;
padding:18px 22px;margin-bottom:16px;">
<div style="font-size:15px;font-weight:800;color:#1e3a5f;margin-bottom:10px;">📋 학습자 미션 — 최종 과제</div>
<div style="font-size:14px;color:#1e3a5f;line-height:2.0;">
지금까지 분석한 데이터를 종합해 <b>실전 신제품 개발 보고서</b>를 완성하세요.<br>
<b>보고서에 반드시 포함해야 할 항목</b><br>
&nbsp;&nbsp;① 시장 현황 &nbsp;·&nbsp; 소비자 트렌드 &nbsp;·&nbsp; 경쟁 시장 현황<br>
&nbsp;&nbsp;② <b>2026년 음료 신제품으로 추천하는 상위 3개 품목</b> 도출 (데이터 근거 포함)<br>
&nbsp;&nbsp;③ 테이블 또는 그래프 <b>최소 1개</b> 포함<br>
&nbsp;&nbsp;④ 최종 자료는 <b>출력 가능한 보고서 형태</b>로 완성
<span style="font-size:12px;color:#3b82f6;">&nbsp;(웹페이지 · 이미지 · 슬라이드 등)</span>
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        # ════════════════════════════════════════
        # Step 1: OpenAI 보고서 스크립트 작성
        # ════════════════════════════════════════
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Step 1 &nbsp;·&nbsp; ChatGPT에서 보고서로 출력할 수 있는 스크립트를 작성하세요
</span>
</div>""", unsafe_allow_html=True)

        # pending key 패턴
        if "report_script_pending" in st.session_state:
            st.session_state["report_user_script"] = st.session_state.pop("report_script_pending")

        report_script = st.text_area(
            "OpenAI 보고서 스크립트",
            key="report_user_script",
            height=220,
            placeholder=(
                "지금까지 학습한 데이터를 바탕으로 신제품 음료 개발 보고서를 작성해줘.\n\n"
                "[포함할 항목]\n"
                "1. 시장 현황\n2. 소비자 트렌드\n3. 경쟁 시장 현황\n"
                "4. 2026년 신제품 추천 상위 3개 품목\n\n"
                "[출력 형식] ..."
            ),
            label_visibility="collapsed",
        )

        if report_script.strip():
            st.caption("📋 아래 코드 블록 우측 상단 복사 아이콘 클릭 → ChatGPT, Gemini 등에 붙여넣기")
            st.code(report_script + _SUBMIT_INSTRUCTION, language=None)

        # ── 정답 스크립트 (숨김 expander) ──
        with st.expander("▶ 정답 스크립트 보기"):
            st.caption("아래는 미션 항목을 모두 충족하는 예시 스크립트입니다. 참고 후 본인 스크립트에 반영해보세요.")
            st.code("""지금까지 수집·분석한 데이터로 신제품 음료 개발 시장 분석 보고서를 작성해줘.

[목적]
2026년 RTD 음료 신제품 개발 의사결정 참고 자료

[구성]
1. 시장 현황 — 카테고리별 규모와 채널별 점유율
2. 소비자 트렌드 — 2026년 소비 키워드와 선호 플레이버 변화
3. 경쟁 현황 — 주요 브랜드 구도, 매대 SKU 점유율, 원재료 사용 빈도 TOP 10
4. 신제품 추천 3개 — 각각 컨셉·타깃·핵심 원재료·추천 근거

[표]
- 카테고리별 점유율 표 1개, 원재료 사용 빈도 순위 표 1개를 넣어줘.

[형식]
- 제목 / 목차 / 섹션 순서로, 슬라이드나 PDF로 옮길 수 있게 작성해줘.

[주의]
- 수치에는 출처를 붙이고, 출처가 없으면 [추정]이라고 표시해.
- 없는 데이터를 지어내지 마.""", language=None)

        # 파일링크 불필요: 보고서 작성 스크립트는 텍스트 제출로 충분
        _hw_ui("보고서작성", st.session_state.get("report_user_script", ""), "report_hw_submit")
        st.caption("💬 ChatGPT에서 보고서를 생성한 결과를 제출해주세요.")

        st.markdown("---")

        # ════════════════════════════════════════
        # Step 2: NotebookLM 소스 추가 & 지침 입력
        # ════════════════════════════════════════
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Step 2 &nbsp;·&nbsp; 완성한 보고서를 NotebookLM에 소스로 추가하고 슬라이드로 만드세요
</span>
</div>""", unsafe_allow_html=True)

        # ── 왜 ChatGPT → NotebookLM으로 변환하는가 (플로우차트) ──
        def _flow_card(icon, title, items, todo):
            items_html = "<br>".join(items)
            return f"""<div style="background:#ffffff;border:2px solid #334155;border-radius:10px;
padding:20px 22px;height:100%;box-sizing:border-box;">
<div style="background:#1e293b;color:#ffffff;border-radius:20px;padding:5px 16px;
font-size:15px;font-weight:800;display:inline-block;margin-bottom:12px;">{icon}</div>
<div style="font-size:18px;font-weight:700;color:#0f172a;line-height:1.6;margin-bottom:10px;">{title}</div>
<div style="font-size:16px;color:#475569;line-height:2.1;">{items_html}</div>
<div style="margin-top:12px;padding-top:10px;border-top:1px dashed #cbd5e1;
font-size:15px;color:#1d4ed8;font-weight:700;line-height:1.7;">🎯 학습자 할 일<br>
<span style="font-weight:500;color:#1e40af;">{todo}</span></div>
</div>"""

        _flow_arrow = """<div style="display:flex;align-items:center;justify-content:center;height:100%;padding-top:34px;">
<div style="width:26px;height:4px;background:#475569;"></div>
<div style="width:0;height:0;border-top:10px solid transparent;border-bottom:10px solid transparent;border-left:16px solid #475569;"></div>
</div>"""

        st.caption("💡 왜 ChatGPT에서 만든 보고서를 NotebookLM으로 다시 넘길까요? 두 AI의 강점이 다르기 때문입니다.")
        _fc1, _fa1, _fc2 = st.columns([4, 0.7, 4])
        with _fc1:
            st.markdown(_flow_card("✍️ ChatGPT", "텍스트 보고서 작성",
                ["데이터 분석·근거 정리에 강함", "시장현황·트렌드·경쟁현황 등", "논리적인 글 형태의 보고서 생성"],
                "① NotebookLM용 지침 스크립트 생성하기"), unsafe_allow_html=True)
        with _fa1:
            st.markdown(_flow_arrow, unsafe_allow_html=True)
        with _fc2:
            st.markdown(_flow_card("🎬 NotebookLM", "발표용 슬라이드 생성",
                ["업로드한 소스 기반으로만 생성 (환각 방지)", "슬라이드·요약 등 발표 자료에 특화", "ChatGPT 보고서를 소스로 넣어 변환"],
                "② 보고서를 소스로 추가하고 ③ 생성된 스크립트를 지침으로 입력하기"), unsafe_allow_html=True)

        st.markdown("---")

        st.image("assets/notebooklm_home.jpg", caption="NotebookLM 홈페이지")
        st.markdown("🔗 [notebooklm.google.com](https://notebooklm.google.com)")

        st.markdown("---")

        # ── 2-1. 변환 스크립트로 NotebookLM 지침 만들기 ──
        st.markdown("**① ChatGPT 안에서 NotebookLM용 스크립트 만들기**")
        st.markdown('<span style="color:#000000;font-weight:600;">방금 출력한 ChatGPT 보고서를 노트북LM용 스크립트로 변환해줍니다. (아래 스크립트는 ChatGPT 대화창에 그대로 입력하세요)</span>',
                     unsafe_allow_html=True)
        st.markdown(
            '<span style="display:inline-block;background:#10a37f;color:#ffffff;font-size:12px;'
            'font-weight:700;border-radius:6px;padding:3px 10px;margin:6px 0 2px 0;">'
            '💬 ChatGPT 채팅창</span>',
            unsafe_allow_html=True,
        )
        st.code(
            "방금 작성한 신제품 음료 개발 시장 분석 보고서를 NotebookLM 슬라이드 생성 지침으로 변환해줘.",
            language=None,
        )

        st.markdown("---")

        # ── Step 2 과제 제출 ──
        _s2_student = st.session_state.get("student_name", "")
        if not _s2_student:
            st.warning("과제를 제출하려면 먼저 로그인하세요.")
        else:
            st.markdown("##### 📤 Step 2 과제 제출")
            st.caption("ChatGPT가 만들어준 NotebookLM 지침 스크립트를 아래에 붙여넣고 제출하세요.")
            _nb_input = st.text_area(
                "NotebookLM 슬라이드 지침",
                key="report_nb_script",
                height=200,
                placeholder="ChatGPT가 만들어준 NotebookLM 지침 스크립트를 여기에 붙여넣으세요.",
                label_visibility="collapsed",
            )
            _col_nb_btn, _col_nb_status = st.columns([1, 2])
            with _col_nb_btn:
                _nb_clicked = st.button("📤 슬라이드 스크립트 제출", key="report_nb_submit",
                                        type="primary", use_container_width=True)
            if _nb_clicked:
                if _nb_input.strip():
                    _ok, _err = _submit_report_nb(_s2_student, _nb_input.strip())
                    st.session_state["report_nb_done"] = _ok
                    st.session_state["report_nb_err"] = _err if not _ok else ""
                else:
                    st.warning("스크립트를 입력해주세요.")
            with _col_nb_status:
                if st.session_state.get("report_nb_done"):
                    st.success(f"✅ **{_s2_student}** 님 Step 2 제출 완료! (재제출 시 최종본으로 갱신)")
                elif st.session_state.get("report_nb_err"):
                    st.error(f"제출 실패: {st.session_state['report_nb_err']}")
            count_nb = _get_hw_count("보고서작성")
            if count_nb >= 0:
                st.caption(f"👥 현재 제출 인원: **{count_nb}명**")

        st.markdown("---")

        # ── 2-2. 소스 추가 ──
        st.markdown("**② 소스 추가하기**")
        st.caption("'소스'는 NotebookLM이 답변·슬라이드를 만들 때 참고하는 원본 자료입니다. Step 1에서 ChatGPT가 만든 보고서 결과를 소스로 등록해야, 가짜 데이터가 아니라 그 보고서 내용을 근거로 슬라이드가 만들어집니다.")
        st.markdown("""1. notebooklm.google.com 접속 → 새 노트북 만들기
2. **'소스 추가'** 클릭 → **'텍스트 붙여넣기'** 선택
   - 우리는 파일이나 웹사이트가 아니라 **ChatGPT가 만들어준 보고서 스크립트(텍스트)**를 그대로 넣는 것이므로, 파일 업로드가 아닌 '텍스트 붙여넣기'를 선택합니다.
3. Step 1의 AI 생성결과(보고서 전체)를 복사해 붙여넣고 저장""")

        st.markdown("---")

        # ── 2-3. 지침 입력 & 생성 ──
        st.markdown("**③ 지침 입력 후 슬라이드 생성**")
        st.markdown(
            '<span style="display:inline-block;background:#4285f4;color:#ffffff;font-size:12px;'
            'font-weight:700;border-radius:6px;padding:3px 10px;margin:2px 0 6px 0;">'
            '📓 NotebookLM 작업화면</span>',
            unsafe_allow_html=True,
        )
        st.caption("소스만 추가하고 바로 생성 버튼을 누르면 NotebookLM 기본값으로 생성되어, 신제품 3개 도출 같은 미션 항목이 빠질 수 있습니다. 아래 순서로 진행하세요.")
        st.markdown("""
<ol style="font-size:15px;color:#334155;line-height:2.0;padding-left:20px;margin:0;">
<li>좌측 소스 목록에서 방금 추가한 소스가 <b>체크(선택)</b>되어 있는지 확인</li>
<li>Studio 패널에서 <b>'슬라이드자료'의 아이콘(맞춤설정)</b> 클릭</li>
<li>추가 설정 항목 선택
  <ul style="margin:6px 0;">
    <li>형식: 자세한 자료 or <span style="background:#fef08a;border-radius:4px;padding:1px 6px;font-weight:700;">발표자 슬라이드</span></li>
    <li>길이: 짧게 or <span style="background:#fef08a;border-radius:4px;padding:1px 6px;font-weight:700;">기본값</span></li>
  </ul>
</li>
<li>①에서 ChatGPT가 만들어준 지침을 붙여넣고 생성</li>
</ol>
""", unsafe_allow_html=True)
        st.caption("기본 지침 예시 (①에서 만든 스크립트가 없다면 아래처럼 직접 입력해도 됩니다)")
        st.code("보고서를 작성하고, 2026년 신제품으로 추천할 3개 품목을 도출해줘.", language=None)
        st.caption("💡 표·그래프나 특정 항목을 더 강조하고 싶다면, ChatGPT에 요청할 때 자유롭게 추가해도 됩니다. (예: '표 또는 그래프 1개 이상 포함해줘')")

    # ── 탭 5: AI 간 대화전환 ──
    with tab_ai:
        show_step_guide(
            _S4_STEPS, 4,
            todo="완성한 보고서를 다른 AI로 넘겨 이어서 작업하는 방법을 익힙니다.",
            uses="앞 단계에서 만든 시장분석 보고서",
            produces="AI 인수인계용 요약 스크립트 — STEP 5 배합비 개발로 연결",
            minutes=8,
        )
        st.markdown("#### 🔄 AI 간 대화전환 — 다른 AI로 업무 이관하기")

        # 목적 안내
        st.markdown("""
<div style="background:#f0fdf4;border-left:5px solid #22c55e;border-radius:10px;
padding:16px 22px;margin-bottom:16px;">
<div style="font-size:15px;font-weight:800;color:#14532d;margin-bottom:8px;">🎯 이 탭의 목적</div>
<div style="font-size:14px;color:#166534;line-height:1.9;">
ChatGPT(OpenAI)에서 진행한 음료 개발 프로젝트 업무를 <b>Gemini 등 다른 AI</b>로 이관할 때 사용합니다.<br>
각 AI는 강점이 달라 업무 목적에 따라 전환이 필요할 수 있습니다.<br><br>
<b>AI별 주요 강점</b><br>
&nbsp;&nbsp;• <b>ChatGPT (OpenAI)</b> &nbsp;—&nbsp; 프로젝트 소스 관리, 긴 맥락 유지, 데이터 분석<br>
&nbsp;&nbsp;• <b>Gemini (Google)</b> &nbsp;—&nbsp; Google Docs·Slides·Drive 연동, 실시간 검색<br>
&nbsp;&nbsp;• <b>Claude (Anthropic)</b> &nbsp;—&nbsp; 긴 문서 분석, 보고서 작성, 코드 생성<br>
&nbsp;&nbsp;• <b>NotebookLM</b> &nbsp;—&nbsp; 업로드 자료 기반 슬라이드·팟캐스트·요약 생성
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        # ── Step 1: 이관 방법 ──
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Round 1 &nbsp;·&nbsp; ChatGPT가 출력한 요약·변환 스크립트를 Gemini에 붙여넣으세요
</span><br>
<span style="font-size:13px;color:#64748b;">출력된 내용을 그대로 복사해 Gemini 새 대화창에 붙여넣으면 맥락이 전달됩니다.</span>
</div>""", unsafe_allow_html=True)

        st.markdown("**Gemini Gems에 자료와 페르소나를 입력하는 방법**")

        def _gem_card(num, title, desc):
            return f"""<div style="background:#ffffff;border:2px solid #334155;border-radius:10px;
padding:20px 20px;height:100%;box-sizing:border-box;">
<div style="background:#1e293b;color:#ffffff;border-radius:20px;padding:4px 14px;
font-size:14px;font-weight:800;display:inline-block;margin-bottom:10px;">STEP {num}</div>
<div style="font-size:17px;font-weight:700;color:#0f172a;line-height:1.5;margin-bottom:8px;">{title}</div>
<div style="font-size:15px;color:#475569;line-height:1.8;">{desc}</div>
</div>"""

        _gem_arr = """<div style="display:flex;align-items:center;justify-content:center;height:100%;padding-top:28px;">
<div style="width:22px;height:4px;background:#475569;"></div>
<div style="width:0;height:0;border-top:9px solid transparent;border-bottom:9px solid transparent;border-left:14px solid #475569;"></div>
</div>"""

        _g1, _ga1, _g2, _ga2, _g3 = st.columns([3, 0.5, 3, 0.5, 3])
        with _g1:
            st.markdown(_gem_card(1, "Gems 만들기", "Gemini 접속 → <b>좌하단 설정(⚙️) 아이콘 → Gems</b> 클릭"), unsafe_allow_html=True)
        with _ga1:
            st.markdown(_gem_arr, unsafe_allow_html=True)
        with _g2:
            st.markdown(_gem_card(2, "요청사항 입력",
                "새 Gem 화면 항목:<br>"
                "• 이름 – Gem의 이름 지정<br>"
                "• 설명 – 어떤 Gem이고 무슨 역할인지 작성<br>"
                "• <b>요청사항</b> – ChatGPT의 페르소나를 그대로 붙여넣기<br>"
                "• 기본 도구 – 그대로 두어도 무방"), unsafe_allow_html=True)
            st.markdown("**📌 페르소나 스크립트는 ChatGPT에서 생성한 페르소나를 불러와서 입력 (연구원, 마케터 모두 입력)**")
        with _ga2:
            st.markdown(_gem_arr, unsafe_allow_html=True)
        with _g3:
            st.markdown(_gem_card(3, "지식",
                "Gem이 참조할 파일을 추가:<br>"
                "1. 기본지식 업로드 – 교육개요(학습용자료 다운로드)의 자료<br>"
                "2. 추가지식 업로드 – 품목제조보고서, 수집 빅데이터 등 학습용 자료"), unsafe_allow_html=True)
            st.markdown("**📌 수업사전 준비시 제미나이 GEM에 업로드한 파일 + 추가 지식 업로드**")

        st.markdown("**📋 ChatGPT에서 페르소나 스크립트 불러오기**")
        st.caption("아래 스크립트를 ChatGPT 대화창에 붙여넣으면 지금까지 만든 연구원·마케터 페르소나 스크립트를 다시 출력받을 수 있습니다. 출력된 내용을 복사해 위 '요청사항'에 붙여넣으세요.")
        st.code("""지금까지 이 프로젝트에서 만든 연구원 페르소나 스크립트와 마케터 페르소나 스크립트를
각각 처음부터 끝까지 그대로 출력해줘. 두 페르소나를 구분해서 순서대로 출력해줘.""", language=None)

        st.markdown('<div style="margin-top:16px;"><b>💡 Gems 소스는 최대 10개까지 등록할 수 있습니다.<br>'
                     '\'제품개발용 데이터\'에서 수집한 자료가 있다면 함께 추가로 넣는 것을 권장합니다.</b></div>',
                     unsafe_allow_html=True)

        st.markdown("---")

        # ── Step 2: 현재 AI에서 업무 요약 받기 ──
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Round 2 &nbsp;·&nbsp; 현재 AI(ChatGPT)에 아래 스크립트를 입력하세요
</span><br>
<span style="font-size:13px;color:#64748b;">대화 맥락과 결과물을 다른 AI가 이해할 수 있는 형태로 요약·변환해달라고 요청합니다.</span>
</div>""", unsafe_allow_html=True)

        st.code("""지금까지 이 프로젝트에서 진행한 모든 업무를 요약해주고,
대화내용의 진행방향, 맥락, 결과물산출을 위한 스크립트를
제미나이용 입력 스크립트로 변환해주세요""", language=None)

        st.markdown("---")

        # ── Step 3: 과제 제출 ──
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Round 3 &nbsp;·&nbsp; Gemini가 출력한 결과를 제출하세요
</span><br>
<span style="font-size:13px;color:#64748b;">Round 2에서 생성한 제미나이용 입력 스크립트를 Gemini에 붙여넣은 뒤, Gemini가 출력한 결과를 그대로 붙여넣어 제출하세요.</span>
</div>""", unsafe_allow_html=True)

        show_transfer_box(
            "s4",
            "내 제품 카테고리에서 같은 시장분석을 한다면 어떤 채널·자료를 봐야 할까요?",
            "예: 쿠팡 냉동만두 리뷰, 식품안전나라 만두류 품목제조보고, 대형마트 냉동 매대 사진",
        )

        _hw_ui(
            "AI전환",
            "지금까지 이 프로젝트에서 진행한 모든 업무를 요약해주고, 대화내용의 진행방향, 맥락, 결과물산출을 위한 스크립트를 제미나이용 입력 스크립트로 변환해주세요",
            "ai_transfer_hw_submit",
            ai_label="제미나이 생성결과",
        )

        st.markdown("---")

        # ── 다른 AI 전환용 추가 스크립트 ──
        st.markdown("**📋 AI별 전환 스크립트 (필요에 따라 복사해 사용하세요)**")

        with st.expander("🟣 Claude로 이관할 때"):
            st.code("지금까지 이 프로젝트에서 진행한 모든 업무를 요약해주고, 대화내용의 진행방향, 맥락, 결과물산출을 위한 스크립트를 Claude(Anthropic)용 입력 스크립트로 변환해주세요", language=None)

        with st.expander("📓 NotebookLM으로 이관할 때"):
            st.code("지금까지 이 프로젝트에서 진행한 모든 업무를 요약해주고, 대화내용의 진행방향, 맥락, 결과물산출을 위한 핵심 내용을 NotebookLM 소스 문서 형식으로 정리해주세요. 제목/배경/진행내용/결과물/다음단계 순으로 구성해주세요", language=None)

        with st.expander("🔵 새로운 ChatGPT 대화로 이관할 때"):
            st.code("지금까지 이 프로젝트에서 진행한 모든 업무를 요약해주고, 대화내용의 진행방향, 맥락, 결과물산출을 위한 스크립트를 새로운 ChatGPT 대화에서 바로 이어서 작업할 수 있도록 컨텍스트 전달용 스크립트로 변환해주세요", language=None)


# ----------------------------------------------------------
# 4. 제품개발용 데이터
# ----------------------------------------------------------
elif section == "3️⃣ 제품개발용 데이터":
    show_banner(
        "제품개발을 위한 데이터 만들기",
        "원료·배합 레퍼런스, 시장 현황, 이론 지식 등을 AI로 정리하고 ChatGPT 프로젝트 소스로 쌓는 방법을 훈련합니다.",
        "3 / 7"
    )
    show_mission([
        "어떤 데이터가 제품 개발에 필요한지 유형별로 파악하기",
        "AI에게 데이터를 정리·수집해 달라는 스크립트 작성하기",
        "정리된 데이터를 ChatGPT 프로젝트 소스로 추가하는 방법 익히기",
    ])

    # ── 음료 카테고리 선택 옵션 ──────────────────────────────
    # 간소화: 10개 -> 4개 (제외: 커피·차 음료(RTD), 유음료·발효유, 과채음료,
    # 발효음료·콤부차, 혼합음료, 생수·이온음료 — 그 외는 직접 입력란 사용)
    BEV_CATEGORIES = [
        "음료 유형 전체 (RTD 전 카테고리)",
        "탄산음료",
        "기능성·에너지 음료",
        "식물성 음료 (두유·귀리·아몬드 등)",
    ]

    # ── 데이터 유형 프리셋 ────────────────────────────────────
    DATA_PRESETS = {
        "🏪 음료 시장 현황": {
            "제품 카테고리": "RTD 음료 전체",
            "분석 범위": "국내 편의점·대형마트 채널 기준, 최근 2년 (2025년 ~ 2026년 현재)",
            "수집 목적": "2026년 {category} 신제품 출시를 위한 경쟁 현황 및 카테고리 트렌드 파악",
            "참고 자료": "한국농수산식품유통공사(aT FIS) {category} 통계, 닐슨코리아 공개 보도자료, 식품의약품안전처, 식품음료신문",
            "출력 형식": """## 1. 카테고리별 시장 규모 및 연도별 성장률 관련 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (RTD 카테고리별 시장 수치 및 트렌드 핵심 요약)

## 2. 주요 플레이어 및 경쟁 현황 관련 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (롯데칠성·코카콜라 등 주요 음료사 시장 점유율 및 채널 경쟁 구도)

## 3. 핵심 트렌드 키워드 및 제품 개발 적용 포인트
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (헬시플레저, 제로/라이트, 기능성 웰니스 등 2026년 신제품 개발 참고 트렌드)""",
            "활용 계획": "AI에게 학습시켜 신제품 아이디어와 컨셉을 잡을 때 참고",
        },
        "🧪 원료·배합비 레퍼런스": {
            "제품 카테고리": "저당 기능성 음료",
            "분석 범위": "국내 식품공전 허가 원료 기준 + 해외 사용 사례",
            "수집 목적": "{category} 개발에 필요한 감미료·기능성 원료 선정 및 사용 기준 파악",
            "참고 자료": "원료사 기술자료(Cargill·Tate & Lyle·Ingredion의 application guide), USDA FoodData Central, FAO/WHO JECFA, AIJN Code of Practice",
            "출력 형식": """## 1. 식품공전 허가 원료 기준 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (원료명·기능·허용 기준치·권장 사용 농도·주의사항)

## 2. 원료별 성분·수치 자료
- 자료명 / 어디에 있는지 / 어떻게 찾는지
- 주요 내용 요약: (감미도·브릭스·산도 등 배합 계산에 쓰는 숫자)

## 3. 실무 적용 포인트 및 우선 검토 원료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (배합 설계 시 우선 검토 원료 TOP5 및 조합 시 주의사항)""",
            "활용 계획": "AI에게 학습시켜 배합비를 짤 때 원료가 적절한지 확인",
        },
        "📚 음료개발 이론 지식": {
            "제품 카테고리": "음료 전반 (RTD·발효·기능성)",
            "분석 범위": "식품화학, 음료 공정, 관능 이론 전반",
            "수집 목적": "{category} AI 개발 시 공통 지식 기반을 형성하기 위한 핵심 이론 정리",
            "참고 자료": "{category} 관련 식품화학 교재 (PDF), 음료공학 학술논문 (PDF), 식품기술사 교재 (PDF), 연구원 내부 교육자료 (DOC)",
            "출력 형식": """## 1. 식품화학 및 음료 성분 이론 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (당류·산미료·향료·기능성 성분 화학 이론 핵심)

## 2. 음료 공정 및 품질 관리 이론 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (HTST·UHT·발효 공정별 맛 변화 및 품질 기준)

## 3. 관능 평가 및 소비자 인지 이론 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (관능 평가 방법론, 소비자 맛 인지 이론, 실무 적용 포인트)""",
            "활용 계획": "AI에게 학습시켜 배합비 개발·품질 설계 때 참고",
        },
        "⚖️ 식품 규격·허가 기준": {
            "제품 카테고리": "혼합음료·기능성음료",
            "분석 범위": "국내 식품공전 기준 + 개별인정형 원료 기준 + 수출 대상국 규격",
            "수집 목적": "{category} 신제품 개발 시 규격 초과·성분 위반 사전 검토 및 인허가 준비",
            "참고 자료": "식품안전나라 {category} 식품공전 원문 (PDF/HTML), 건강기능식품공전 (PDF), Codex Alimentarius (PDF), 식약처 가이드라인 (DOC)",
            "출력 형식": """## 1. 국내 식품공전 기준·규격 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (제품 유형별 당류·산도·보존료·색소·카페인 기준치)

## 2. 건강기능식품 및 개별인정형 원료 허가 기준
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (기능성 원료 인허가 프로세스 및 표시 기준)

## 3. 해외 수출 규격 및 Codex 기준
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (수출 대상국별 규격 차이 및 Codex 국제 기준 비교)""",
            "활용 계획": "AI에게 학습시켜 규격을 넘지 않는지 확인할 때 사용",
        },
        "🌏 해외 신제품 트렌드": {
            "제품 카테고리": "글로벌 RTD·건강음료",
            "분석 범위": "미국·일본·유럽 시장 최근 2년 신제품",
            "수집 목적": "국내 미출시 {category} 트렌드 소재 및 컨셉 발굴로 차별화 신제품 개발",
            "참고 자료": "Mintel GNPD {category} 공개 리포트 (PDF/HTML), Innova Market Insights 공개 보고서, 해외 식품박람회 트렌드 보고서 (PDF)",
            "출력 형식": """## 1. 미국·일본 RTD 음료 신제품 트렌드 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (트렌드 키워드·대표 제품명·핵심 소재)

## 2. 유럽 기능성·웰니스 음료 트렌드 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (유럽 시장 신소재 및 컨셉 동향)

## 3. 국내 적용 가능성 및 리스크 분석 포인트
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (국내 미적용 트렌드 소재의 규제·소비자 수용성·원가 리스크)""",
            "활용 계획": "AI에게 학습시켜 국내에 아직 없는 트렌드를 찾을 때 사용",
        },
        "🔬 배합 원리·공정 지식": {
            "제품 카테고리": "RTD 음료 (살균·무균·발효)",
            "분석 범위": "주요 음료 공정(HTST/UHT/레토르트/발효) 및 배합 설계 원리",
            "수집 목적": "AI가 {category} 배합비를 제안할 때 공정 조건을 정확히 반영하도록 기반 지식 구축",
            "참고 자료": "IFT {category} 식품공학 공개 자료 (PDF), 관련 특허 전문 (HTML/PDF), 식품공학 학술논문 (PDF)",
            "출력 형식": """## 1. 음료 살균 공정 이론 및 조건 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (HTST·UHT·레토르트 공정별 온도·시간·압력 조건 및 품질 영향)

## 2. 배합 설계 원리 및 물성 제어 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (Brix·pH·유화 안정성·점도 등 배합 설계 핵심 변수)

## 3. 관련 특허 및 공정 혁신 사례
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (음료 공정 최신 특허 및 산업 적용 사례)""",
            "활용 계획": "AI에게 학습시켜 배합비가 공정에 맞는지 함께 검토",
        },
        "👥 소비자 리뷰·반응 데이터": {
            "제품 카테고리": "경쟁 음료 제품군",
            "분석 범위": "네이버 쇼핑·쿠팡·인스타그램·유튜브 소비자 리뷰 최근 1년",
            "수집 목적": "{category} 소비자가 실제로 좋아하거나 싫어하는 맛·식감·패키지 요소 파악",
            "참고 자료": "식품음료신문 {category} 소비자 조사 기사 (HTML), aT 소비자 트렌드 보고서 (PDF), 공개 SNS 분석 리포트 (PDF)",
            "출력 형식": """## 1. 소비자 긍정·부정 반응 키워드 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (긍정 키워드 TOP10·부정 키워드 TOP10·자주 언급 속성)

## 2. 제품 속성별 소비자 평가 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (맛·향·패키지·가격·기능성 항목별 소비자 반응)

## 3. 소비자 인사이트 및 개선 요청 포인트
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (반드시 반영해야 할 소비자 개선 요청 및 신제품 개발 시사점)""",
            "활용 계획": "AI에게 학습시켜 컨셉 검증과 배합 방향을 잡을 때 참고",
        },
    }
    # ─────────────────────────────────────────────────────────

    _S3_STEPS = ["예시 보기", "수집 스크립트 작성", "AI에게 학습시키기"]

    tab_ex, tab_collect, tab_project = st.tabs([
        "📖 예시 스크립트 보기",
        "🗂️ 데이터 수집 스크립트 만들기",
        "🧠 AI에게 학습시키기",
    ])

    with tab_ex:
        show_step_guide(
            _S3_STEPS, 0,
            todo="예시 수집 스크립트를 그대로 실행해보고, 어떤 자료가 모이는지 확인합니다.",
            produces="수집 스크립트의 기본 골격",
            minutes=5,
        )
        st.markdown("#### 📋 데이터 수집 스크립트 3가지 — 복사해서 ChatGPT에 붙여넣으세요")
        st.info("아래 스크립트를 복사해 ChatGPT에 붙여넣으면 자료 목록을 받을 수 있습니다.")
        st.caption("법규 나열이 아니라 실제 배합에 쓰는 기술자료를 찾도록 조건을 걸어두었습니다.")

        # ── 스크립트 1: 배합·공정 기술자료 ──
        st.markdown("##### 1️⃣ 배합·공정 기술자료")
        st.caption("아래 ⬛ 부분을 본인이 맡은 제품·원료로 바꿔서 쓰세요. 사람마다 다른 결과가 나옵니다.")
        st.code("""⬛탄산음료⬛ 배합 설계에 참고할 자료를 찾아줘.
특히 ⬛감미료⬛ 쪽을 자세히 보고 싶어.

[필요한 것]
원료를 실제로 몇 % 넣는지, 어떤 조합으로 쓰는지 숫자가 나온 자료

[먼저 찾아볼 곳 — 배합 수치가 실제로 공개된 곳]
1. 특허 (가장 확실함)
   - Google Patents 또는 KIPRIS(한국특허정보원)
   - '음료 조성물', '저당 음료 제조방법', 'beverage composition' 등으로 검색
   - 특허 명세서의 [실시예]에 원료별 배합비가 그대로 적혀 있음
2. 안전성 평가서 (사용 한도의 근거)
   - EFSA 원료 평가보고서, FAO/WHO JECFA
3. 원료사 공개 자료
   - Cargill, Tate & Lyle, Ingredion 사이트에서
     'application guide', 'formulation guide'로 검색

[여기 말고 더 좋은 곳]
- 위에 적은 곳 말고도 더 좋은 출처를 알고 있으면 2~3개 추천해줘.
  왜 그곳이 좋은지 한 줄로 이유도 붙여줘.

[미리 알아둘 것]
- 원료사 TDS(기술규격서)와 기술서적은 대부분 요청하거나 구매해야 볼 수 있어.
  무료로 바로 열리는 것만 알려줘. 못 찾으면 '공개된 것 없음'이라고 해줘.
- 원료를 소개만 하고 배합 수치가 없는 자료는 빼줘.

[출력]
- 자료명 / 어디에 있는지 / 어떻게 찾는지 / 어떤 수치가 들어 있는지 순으로 5개.
- 특허는 특허번호와 함께 [실시예]의 배합 예시를 요약해줘.
- 링크는 확실한 것만. 확실하지 않으면 "○○에서 '△△'로 검색"이라고 알려줘.
- 없는 자료나 없는 링크를 지어내지 마.
[못 찾았을 때]
- 조건에 맞는 자료가 없으면 억지로 채우지 말고 '못 찾았다'고 해줘.
- 대신 어떻게 바꿔서 찾으면 좋을지 2가지만 제안해줘.
  (검색어를 바꾼다 / 다른 종류의 자료를 본다 / 어디에 문의한다 등)""", language=None)

        st.markdown("---")

        # ── 스크립트 2: 시장·트렌드 ──
        st.markdown("##### 2️⃣ 시장·신제품 트렌드")
        st.code("""2026년 ⬛탄산음료⬛ 신제품 기획에 쓸 시장·트렌드 자료를 찾아줘.

[필요한 것]
어떤 컨셉과 플레이버가 실제로 출시되고 있는지, 해외에서 먼저 뜨는 흐름은 무엇인지

[먼저 찾아볼 곳]
- 업계 매체: FoodNavigator, BeverageDaily, Food Business News, 식품음료신문
- 시장조사사 무료 공개분: Innova Market Insights, Mintel 보도자료
- 국내 통계: aT 식품산업통계정보(FIS), 농식품수출정보(KATI)

[여기 말고 더 좋은 곳]
- 위에 적은 곳 말고도 더 좋은 출처를 알고 있으면 2~3개 추천해줘.
  왜 그곳이 좋은지 한 줄로 이유도 붙여줘.

[자료 조건]
- 무료로 볼 수 있는 것 위주로. 유료 보고서는 빼줘.
- 해외 자료도 좋아. 국내에 아직 안 들어온 흐름이면 더 좋아.
- 최근 1~2년 자료로. 실제 출시된 제품 사례가 있는 것으로.

[출력]
- 자료명 / 어디에 있는지 / 어떻게 찾는지 / 무슨 내용인지 순으로 5개만.
- 링크는 확실한 것만. 확실하지 않으면 "○○ 사이트에서 '△△'로 검색"이라고 알려줘.
- 없는 자료나 없는 링크를 지어내지 마.
[못 찾았을 때]
- 조건에 맞는 자료가 없으면 억지로 채우지 말고 '못 찾았다'고 해줘.
- 대신 어떻게 바꿔서 찾으면 좋을지 2가지만 제안해줘.
  (검색어를 바꾼다 / 다른 종류의 자료를 본다 / 어디에 문의한다 등)""", language=None)

        st.markdown("---")

        # ── 스크립트 3: 원료 성분 데이터베이스 ──
        st.markdown("##### 3️⃣ 원료 성분 데이터베이스")
        st.code("""⬛탄산음료⬛ 배합비 계산에 쓸 원료 수치 데이터를 찾아줘.

[필요한 것]
과일 농축액의 당도(브릭스)·산도, 당류별 감미도, 첨가물 사용 한도 같은
계산에 바로 넣을 수 있는 숫자

[먼저 찾아볼 곳]
- USDA FoodData Central (식품 성분 수치)
- FAO/WHO JECFA (첨가물 규격과 ADI)
- EFSA 원료 평가보고서 (사용량 근거)
- AIJN Code of Practice (과일주스·농축액 규격)
- 농촌진흥청 국가표준식품성분표 (국내 원물 데이터)

[여기 말고 더 좋은 곳]
- 위에 적은 곳 말고도 더 좋은 출처를 알고 있으면 2~3개 추천해줘.
  왜 그곳이 좋은지 한 줄로 이유도 붙여줘.

[자료 조건]
- 무료로 볼 수 있는 것 위주로. 유료 보고서는 빼줘.
- 영문 자료도 좋아. 오히려 해외 기술자료를 더 찾아줘.
- 법규·기준만 나열한 자료 말고, 실제 배합에 쓰는 수치와 적용 사례가 있는 것으로.
- 논문이라도 사용량·농도·관능 결과 같은 실무 수치가 있으면 넣어줘.

[출력]
- 자료명 / 어디에 있는지 / 어떻게 찾는지 / 무슨 내용인지 순으로 5개만.
- 링크는 확실한 것만. 확실하지 않으면 "○○ 사이트에서 '△△'로 검색"이라고 알려줘.
- 없는 자료나 없는 링크를 지어내지 마.
[못 찾았을 때]
- 조건에 맞는 자료가 없으면 억지로 채우지 말고 '못 찾았다'고 해줘.
- 대신 어떻게 바꿔서 찾으면 좋을지 2가지만 제안해줘.
  (검색어를 바꾼다 / 다른 종류의 자료를 본다 / 어디에 문의한다 등)""", language=None)

    with tab_collect:
        show_step_guide(
            _S3_STEPS, 1,
            todo="필요한 자료 분야를 고르고 조건을 채워 나만의 수집 스크립트를 완성합니다.",
            uses="STEP 2에서 만든 페르소나(연구원 역할)",
            produces="나만의 데이터 수집 스크립트와 수집한 자료 목록",
            minutes=15,
        )
        st.markdown("#### 📝 나만의 수집 스크립트 만들기")
        st.caption("① 분야 → ② 제품 → ③ 조건 → ④ 출력 순서로 고르면 아래에 스크립트가 완성됩니다.")

        # ── ① 분야 ─────────────────────────────────────────
        st.markdown('<span class="ml-step">① 어떤 자료가 필요한가요?</span>',
                    unsafe_allow_html=True)
        _F3 = ["⚗️ 배합·공정", "📈 시장·트렌드", "🧪 원료 성분"]
        _fsel = st.pills("분야", _F3, default="⚗️ 배합·공정",
                         key="d_field", label_visibility="collapsed")
        _field = _fsel or "⚗️ 배합·공정"

        # ── ② 제품 ─────────────────────────────────────────
        st.markdown('<span class="ml-step">② 어떤 제품인가요?</span>',
                    unsafe_allow_html=True)
        _PROD = ["탄산음료", "커피음료", "과일주스", "차음료",
                 "단백질음료", "식물성음료", "이온음료", "제로음료"]
        _psel = st.pills("제품", _PROD, default="탄산음료",
                         key="d_prod", label_visibility="collapsed")
        _pcustom = st.text_input("제품 직접 입력", key="d_prod_custom",
                                 placeholder="직접 입력 (예: 무가당 스파클링)",
                                 label_visibility="collapsed")
        _product = _pcustom.strip() or _psel or "탄산음료"

        # ── ③ 분야별 조건 ──────────────────────────────────
        st.markdown('<span class="ml-step">③ 조건을 정하세요</span>',
                    unsafe_allow_html=True)

        def _merge(picked, typed, fallback):
            """고른 것 + 직접 입력한 것을 합친다 (쉼표 구분)"""
            items = list(picked or [])
            for w in (typed or "").split(","):
                w = w.strip()
                if w and w not in items:
                    items.append(w)
            return items or list(fallback)

        if _field == "⚗️ 배합·공정":
            _c1, _c2 = st.columns(2)
            with _c1:
                st.caption("자세히 보고 싶은 원료")
                _ING = ["감미료", "산미료", "안정제·유화제", "기능성 원료", "향료",
                        "과일류(과즙·농축액)", "우유기반(유단백·유크림)"]
                _ing_p = st.pills("원료", _ING, selection_mode="multi",
                                  default=["감미료"], key="d_ing",
                                  label_visibility="collapsed")
                _ing_t = st.text_input("원료 직접입력", key="d_ing_txt",
                                       placeholder="+ 직접 입력 (쉼표로 여러 개)",
                                       label_visibility="collapsed")
                st.caption("알고 싶은 것")
                _KNOW = ["배합비(원료 조성)", "제조공정(순서·조건)",
                         "살균·충전 기술", "품질 안정화"]
                _know_p = st.pills("관점", _KNOW, selection_mode="multi",
                                   default=["배합비(원료 조성)"], key="d_know",
                                   label_visibility="collapsed")
                _know_t = st.text_input("관점 직접입력", key="d_know_txt",
                                        placeholder="+ 직접 입력 (예: 스케일업 조건)",
                                        label_visibility="collapsed")
            with _c2:
                st.caption("찾아볼 곳")
                _SRC = ["특허(실시예)", "안전성 평가서", "원료사 공개자료",
                        "학회·협회 기술자료"]
                _src_p = st.pills("출처", _SRC, selection_mode="multi",
                                  default=["특허(실시예)"], key="d_src",
                                  label_visibility="collapsed")
                _src_t = st.text_input("출처 직접입력", key="d_src_txt",
                                       placeholder="+ 직접 입력 (예: 사내 기술자료)",
                                       label_visibility="collapsed")

            _ings = _merge(_ing_p, _ing_t, ["감미료"])
            _knows = _merge(_know_p, _know_t, ["배합비(원료 조성)"])
            _srcs = _merge(_src_p, _src_t, ["특허(실시예)"])
            _ing_txt = ", ".join(_ings)
            _know_txt = ", ".join(_knows)

            _NEED_MAP = {
                "배합비(원료 조성)": "원료를 실제로 몇 % 넣는지, 어떤 조합으로 쓰는지",
                "제조공정(순서·조건)": "공정 순서와 조건(온도·시간·압력·투입 순서)",
                "살균·충전 기술": "살균 조건(온도·시간)과 충전 방식",
                "품질 안정화": "유통 중 분리·침전·변색을 막는 방법과 조건",
            }
            _need = " / ".join(_NEED_MAP.get(k, k) for k in _knows) + " 가 숫자로 나온 자료"

            _SRC_MAP = {
                "특허(실시예)":
                    "- 특허: Google Patents 또는 KIPRIS(한국특허정보원)\n"
                    "  '음료 조성물', '제조방법', 'beverage composition' 등으로 검색\n"
                    "  특허 명세서의 [실시예]에 배합비와 공정 조건이 그대로 적혀 있음",
                "안전성 평가서":
                    "- 안전성 평가서: EFSA 원료 평가보고서, FAO/WHO JECFA (사용 한도 근거)",
                "원료사 공개자료":
                    "- 원료사: Cargill, Tate & Lyle, Ingredion 사이트에서\n"
                    "  'application guide', 'formulation guide'로 검색",
                "학회·협회 기술자료":
                    "- 학회·협회: 한국식품과학회, IFT, AIJN 등의 공개 기술자료",
            }
            _where = "\n".join(_SRC_MAP.get(s, "- " + s) for s in _srcs)
            _scope_txt = "%s의 %s (%s)" % (_product, _know_txt, _ing_txt)
            _caution = (
                "- 원료사 TDS(기술규격서)와 기술서적은 대부분 요청하거나 구매해야 볼 수 있어.\n"
                "  무료로 바로 열리는 것만 알려줘. 못 찾으면 '공개된 것 없음'이라고 해줘.\n"
                "- 소개만 하고 숫자가 없는 자료는 빼줘."
            )
            _extra_out = "- 특허는 특허번호와 함께 [실시예]의 배합·공정 조건을 요약해줘.\n"
            _head = ("%s 개발에 참고할 자료를 찾아줘.\n특히 %s 쪽의 %s를 자세히 보고 싶어."
                     % (_product, _ing_txt, _know_txt))

        elif _field == "📈 시장·트렌드":
            _c1, _c2 = st.columns(2)
            with _c1:
                st.caption("어느 지역")
                _REG = ["국내", "미국·유럽", "일본·아시아"]
                _reg_p = st.pills("지역", _REG, selection_mode="multi",
                                  default=["국내"], key="d_reg",
                                  label_visibility="collapsed")
                _reg_t = st.text_input("지역 직접입력", key="d_reg_txt",
                                       placeholder="+ 직접 입력 (예: 중동, 동남아)",
                                       label_visibility="collapsed")
                st.caption("기간")
                _per = st.pills("기간", ["최근 1년", "최근 2년", "최근 3년"],
                                default="최근 2년", key="d_per",
                                label_visibility="collapsed")
            with _c2:
                st.caption("보고 싶은 것")
                _WATCH = ["신제품 출시 사례", "컨셉 트렌드", "플레이버 트렌드", "채널별 동향"]
                _watch_p = st.pills("관점", _WATCH, selection_mode="multi",
                                    default=["신제품 출시 사례", "플레이버 트렌드"],
                                    key="d_watch", label_visibility="collapsed")
                _watch_t = st.text_input("관점 직접입력", key="d_watch_txt",
                                         placeholder="+ 직접 입력 (예: 패키지 트렌드)",
                                         label_visibility="collapsed")
            _regs = _merge(_reg_p, _reg_t, ["국내"])
            _watches = _merge(_watch_p, _watch_t, ["신제품 출시 사례"])
            _reg_txt = ", ".join(_regs)
            _watch_txt = ", ".join(_watches)
            _scope_txt = "%s 기준 %s, %s" % (_reg_txt, _per or "최근 2년", _watch_txt)
            _need = _watch_txt + " 를 알 수 있는 자료"
            _where = (
                "- 업계 매체: FoodNavigator, BeverageDaily, Food Business News, 식품음료신문\n"
                "- 시장조사사 무료 공개분: Innova Market Insights, Mintel 보도자료\n"
                "- 국내 통계: aT 식품산업통계정보(FIS), 농식품수출정보(KATI)"
            )
            _caution = (
                "- 유료 보고서는 빼줘. 무료로 볼 수 있는 것 위주로.\n"
                "- %s 자료로. 실제 출시된 제품 사례가 있는 것으로." % (_per or "최근 2년")
            )
            _extra_out = ""
            _head = ("%s %s 신제품 기획에 쓸 시장·트렌드 자료를 찾아줘."
                     % (_reg_txt, _product))

        else:  # 🧪 원료 성분
            _c1, _c2 = st.columns(2)
            with _c1:
                st.caption("필요한 수치")
                _NUM = ["당도(브릭스)", "산도", "감미도", "사용 한도", "영양성분"]
                _num_p = st.pills("수치", _NUM, selection_mode="multi",
                                  default=["당도(브릭스)", "산도"], key="d_num",
                                  label_visibility="collapsed")
                _num_t = st.text_input("수치 직접입력", key="d_num_txt",
                                       placeholder="+ 직접 입력 (예: 점도, 색도)",
                                       label_visibility="collapsed")
            with _c2:
                st.caption("찾아볼 곳")
                _DB = ["USDA FoodData Central", "FAO/WHO JECFA", "EFSA",
                       "AIJN Code of Practice", "농촌진흥청 성분표"]
                _db_p = st.pills("DB", _DB, selection_mode="multi",
                                 default=["USDA FoodData Central", "농촌진흥청 성분표"],
                                 key="d_db", label_visibility="collapsed")
                _db_t = st.text_input("DB 직접입력", key="d_db_txt",
                                      placeholder="+ 직접 입력 (예: 사내 원료DB)",
                                      label_visibility="collapsed")
            _nums = _merge(_num_p, _num_t, ["당도(브릭스)"])
            _dbs = _merge(_db_p, _db_t, ["USDA FoodData Central"])
            _num_txt = ", ".join(_nums)
            _scope_txt = "%s에 쓰는 원료의 %s" % (_product, _num_txt)
            _need = "%s 처럼 계산에 바로 넣을 수 있는 숫자" % _num_txt
            _where = "\n".join("- " + d for d in _dbs)
            _caution = (
                "- 숫자가 없는 일반 소개 자료는 빼줘.\n"
                "- 무료로 볼 수 있는 것만."
            )
            _extra_out = "- 수치는 단위와 기준(무엇을 100으로 본 값인지)을 함께 적어줘.\n"
            _head = "%s 배합비 계산에 쓸 원료 수치 데이터를 찾아줘." % _product

        # ── ④ 출력 형식 ────────────────────────────────────
        st.markdown('<span class="ml-step">④ 결과를 어떻게 보여줄까요?</span>',
                    unsafe_allow_html=True)
        _OUT3 = {
            "하나씩 목록으로": "자료명 / 어디에 있는지 / 어떻게 찾는지 / 무슨 내용인지 순으로 5개만.",
            "표로 한눈에 비교": "항목별 비교 표로 정리해줘. 항목명·수치·출처를 열로 넣어줘.",
            "짧게 요약해서": "A4 1장 분량으로 핵심만 요약해줘. 어려운 용어는 풀어서 써줘.",
        }
        _osel = st.pills("출력", list(_OUT3.keys()), default="하나씩 목록으로",
                         key="d_out3", label_visibility="collapsed")
        _out_label = _osel or "하나씩 목록으로"
        _out_txt = _OUT3[_out_label]

        # ── 스크립트 조립 ──────────────────────────────────
        prompt_d = (
            _head + "\n\n"
            "[필요한 것]\n" + _need + "\n\n"
            "[먼저 찾아볼 곳]\n" + _where + "\n\n"
            "[여기 말고 더 좋은 곳]\n"
            "- 위에 적은 곳 말고도 더 좋은 출처를 알고 있으면 2~3개 추천해줘.\n"
            "  왜 그곳이 좋은지 한 줄로 이유도 붙여줘.\n\n"
            "[미리 알아둘 것]\n" + _caution + "\n\n"
            "[출력]\n- " + _out_txt + "\n"
            + _extra_out +
            "- 링크는 확실한 것만. 확실하지 않으면 \"○○에서 '△△'로 검색\"이라고 알려줘.\n"
            "- 없는 자료나 없는 링크를 지어내지 마.\n\n"
            "[못 찾았을 때]\n"
            "- 조건에 맞는 자료가 없으면 억지로 채우지 말고 '못 찾았다'고 해줘.\n"
            "- 대신 어떻게 바꿔서 찾으면 좋을지 2가지만 제안해줘.\n"
            "  (검색어를 바꾼다 / 다른 종류의 자료를 본다 / 어디에 문의한다 등)"
        )

        st.markdown("---")
        st.markdown("##### 📋 완성된 스크립트")
        st.caption("코드 블록 우측 상단 복사 아이콘 → ChatGPT에 붙여넣기")
        st.code(prompt_d, language=None)

        d_fields = {"분석 범위": _scope_txt, "출력 형식": _out_txt, "요청사항": _caution}
        d_defaults = {"분석 범위": "탄산음료의 감미료 배합 사례",
                      "출력 형식": _OUT3["하나씩 목록으로"],
                      "요청사항": ""}
        render_data_coach(prompt_d, d_fields, d_defaults, "d_build")
        _hw_ui("데이터수집스크립트", prompt_d, "collect_hw_submit",
               with_file=True, guide_type="gpt")


    with tab_project:
        show_step_guide(
            _S3_STEPS, 2,
            todo="모은 자료를 ChatGPT 프로젝트에 올리고, AI가 그 자료로 답하게 만듭니다.",
            uses="앞 단계 스크립트로 수집한 자료 파일·링크",
            produces="내 자료를 근거로 답하는 AI 프로젝트 — STEP 4 시장분석의 기반",
            minutes=15,
        )
        st.markdown("#### 🧠 ChatGPT 프로젝트에 자료 올리고 학습시키기")
        st.info("ChatGPT의 '프로젝트' 기능을 활용하면 수집한 데이터를 AI 대화의 영구 참조 소스로 등록할 수 있습니다. 한 번 등록하면 같은 프로젝트 내 모든 대화에서 AI가 자동으로 참조합니다.")

        st.markdown("---")
        st.markdown("##### STEP 1. ChatGPT 프로젝트 생성")
        show_example("""1. ChatGPT 접속 → 좌측 사이드바 상단 '프로젝트' 클릭
2. '+ 새 프로젝트' 선택
3. 프로젝트명 입력 예: '저당 RTD 음료 개발 2026'
4. 필요시 프로젝트 설명 추가 (예: '2026년 여름 출시 저당 음료 개발 전용 작업공간')""")

        st.markdown("##### STEP 2. 데이터 수집 스크립트 실행")
        show_example("""1. 위 [🗂️ 데이터 수집 스크립트 만들기] 탭에서 원하는 데이터 유형 선택
2. 항목 수정 후 '이를 적용하기' 클릭 → 프롬프트 복사
3. ChatGPT 새 대화창에 붙여넣기 → AI가 데이터 정리 결과 출력
4. AI 결과를 전체 선택 → 복사""")

        st.markdown("##### STEP 3. 올리기 전에 파일 점검하기")
        st.caption("이 점검을 건너뛰면 올려도 AI가 못 읽거나 엉뚱한 걸 물어옵니다.")
        st.error(
            "⚠️ **가장 흔한 실패 — 스캔한 PDF는 한 글자도 못 읽습니다.** "
            "PDF를 열어 마우스로 글자가 드래그되면 정상, 안 되면 그림입니다. "
            "그림이면 텍스트로 옮기거나 다른 자료를 찾으세요."
        )
        with st.expander("📋 나머지 점검 항목 5가지"):
            st.markdown("""
| 점검 | 왜 |
|---|---|
| **파일 하나에 주제 하나** | 시장자료·원료데이터를 한 파일에 몰면 엉뚱한 대목을 물어옵니다 |
| **파일명을 내용으로** | 파일명이 검색 단서입니다. `자료1.pdf` ❌ → `감미료_사용한도_EFSA_2023.pdf` ⭕ |
| **첫머리에 출처·날짜** | 문서 맨 앞에 적어두면 AI가 "○○ 자료(2023년) 기준"이라고 근거를 댈 수 있습니다 |
| **표는 이미지 말고 텍스트로** | 표 그림은 무시됩니다. 숫자가 중요하면 엑셀·CSV로 따로 올리세요 |
| **중복·옛날 버전 빼기** | 비슷한 파일이 여럿이면 옛날 값을 물어옵니다 |
""")

        st.markdown("##### STEP 4. ChatGPT 프로젝트에 소스로 추가하기")
        show_example("""1. STEP2에서 받은 결과 파일 준비
   - 파일 링크로 뜬 경우 → 링크 클릭해 파일 다운로드
   - 이미 다운로드된 경우 → 해당 파일 그대로 사용
2. ChatGPT 프로젝트 열기 → '파일 추가'(소스 추가) 클릭
3. 준비한 파일 선택 → 업로드
4. 프로젝트 소스 목록에 파일이 표시되는지 확인""")

        st.markdown("##### STEP 5. '자료 안내' 파일 만들어 함께 올리기")
        st.caption(
            "파일명을 '감미도.pdf'처럼 짓게 되는데, 그러면 질문과 연결이 약해 AI가 못 찾습니다. "
            "올린 파일들을 안내하는 문서 하나를 같이 올리면 매번 파일을 지정하지 않아도 됩니다."
        )
        st.markdown("**① 파일을 다 올린 뒤, 같은 프로젝트 대화창에 아래를 붙여넣으세요**")
        st.code("""이 프로젝트에 올린 파일들을 정리한 '자료 안내' 문서를 만들어줘.

파일마다 이렇게 적어줘.
- 파일명
- 어떤 내용이 들어 있는지 두 줄로
- 어떤 질문을 받았을 때 이 파일을 봐야 하는지 (키워드를 10개 이상 나열)
- 출처와 자료 날짜

마크다운으로 만들어줘. 내가 복사해서 00_자료안내.md 로 저장할 거야.
맨 위에 "질문을 받으면 이 문서를 먼저 보고 어느 파일을 볼지 정하세요"라고 적어줘.""",
                language=None)
        st.markdown("**② 나온 결과를 `00_자료안내.md` 로 저장해 프로젝트에 다시 올리세요**")
        with st.expander("💡 왜 키워드를 10개 이상 넣나요?"):
            st.markdown(
                "AI는 질문과 문서 내용이 얼마나 비슷한지로 파일을 찾습니다. "
                "`감미도.pdf` 라는 이름만으로는 \"스테비아 얼마나 넣어?\" 라는 질문과 잘 안 걸립니다.\n\n"
                "자료 안내 문서에 **스테비아 · 에리스리톨 · 아스파탐 · 사용량 · 감미도 · 당도** 처럼 "
                "질문에 나올 법한 말을 미리 적어두면, AI가 그 문서를 잡고 → 해당 파일로 찾아갑니다.\n\n"
                "파일명이 `00_`으로 시작하면 목록 맨 위에 와서 먼저 참조되는 효과도 있습니다."
            )

        st.markdown("##### STEP 6. 프로젝트 지시문 설정하기 ★ 가장 중요")
        st.caption(
            "파일만 올리면 AI는 올린 자료를 안 보고 원래 알던 지식으로 답합니다. "
            "프로젝트 설정의 '지시사항(Instructions)'에 아래를 넣으세요. "
            "**배합비·원료 질문에만 자료를 보고, 일반 질문은 평소대로 답하도록** 되어 있습니다."
        )

        st.code("""[언제 자료를 볼지]
- 배합비, 원료, 사용량, 규격, 시장 데이터에 관한 질문이면 업로드된 자료를 근거로 답하라.
- 내가 "자료 기준으로"라고 말하면 어떤 질문이든 자료만 근거로 답하라.
- 그 밖의 일반적인 질문(아이디어 내기, 글 다듬기, 용어 설명 등)은
  자료를 찾지 말고 평소처럼 답하라.

[자료를 볼 때 지킬 것]
- 먼저 '00_자료안내' 문서를 보고 어느 파일을 볼지 정한 뒤 답하라.
- 반드시 업로드된 자료만 근거로 삼아라.
- 자료에 없는 내용은 "업로드된 자료에는 없습니다"라고 먼저 말하고,
  네가 알고 있는 일반 지식이라면 그렇다고 구분해서 밝혀라.
- 수치를 말할 때는 어느 파일에서 가져왔는지 파일명을 함께 적어라.
- 자료끼리 값이 다르면 어느 쪽이 다른지 알려주고 임의로 하나를 고르지 마라.

[자료 관리]
- '00_자료안내'에 적혀 있지 않은 파일이 올라와 있으면, 답변 맨 끝에
  "※ 자료안내에 없는 파일: (파일명)" 이라고 한 줄 알려줘라.
- 내가 "자료안내 업데이트"라고 말하면, 지금 올라와 있는 모든 파일을 다시 정리해
  00_자료안내.md 전체를 마크다운으로 출력해라.""", language=None)

        st.caption(
            "💡 첫 블록이 **언제 자료를 볼지**를 정합니다. 배합비·원료 질문에만 자료를 뒤지고, "
            "일반 질문은 평소처럼 답합니다. 자료를 꼭 근거로 삼게 하려면 질문 앞에 "
            "**\"자료 기준으로\"** 를 붙이세요."
        )

        st.info(
            "📌 **자료를 새로 올렸을 때** — 대화창에 **\"자료안내 업데이트\"** 라고 치면 "
            "AI가 전체 목록을 다시 만들어 줍니다. 복사해서 `00_자료안내.md` 로 덮어쓰면 끝입니다."
        )
        with st.expander("❓ 파일을 올리면 자동으로 갱신되게 할 수는 없나요?"):
            st.markdown(
                "안 됩니다. 이유는 두 가지입니다.\n\n"
                "- 프로젝트 지시문은 **대화가 시작될 때 적용되는 규칙**이지, "
                "파일이 올라온 것을 감지하는 장치가 아닙니다.\n"
                "- AI는 이미 올라간 파일을 **고쳐 쓰거나 덮어쓸 수 없습니다.** "
                "새 내용을 만들어 줄 수는 있어도 저장은 사람이 해야 합니다.\n\n"
                "대신 위 지시문의 마지막 두 줄이 부담을 줄여줍니다. "
                "AI가 **빠진 파일을 스스로 알려주고**, **\"자료안내 업데이트\"** 한 마디에 "
                "전체를 다시 뽑아 줍니다."
            )

        st.markdown("##### STEP 7. AI 학습결과 확인")
        st.caption("올린 자료를 실제로 읽고 있는지 확인하세요. 아래를 그대로 물어보면 됩니다.")
        _CHECK_SCRIPT = """지금 프로젝트에 올라와 있는 자료 목록을 먼저 보여줘.

그다음, 그 자료에서 감미료 사용량이 어떻게 나와 있는지 알려줘.
어느 파일의 어느 부분에서 봤는지도 함께 적어줘."""
        st.code(_CHECK_SCRIPT, language=None)
        st.markdown(
            "- **파일명을 대며 답하면** 자료를 제대로 읽고 있는 것입니다. ✅\n"
            "- **파일 언급 없이 술술 답하면** 자료를 안 보고 원래 지식으로 답하는 것입니다. "
            "STEP 6 지시문을 다시 확인하세요. ⚠️"
        )

        st.markdown("---")
        st.caption(
            "위 질문을 AI에 넣고 받은 답변을 아래 **AI 학습결과 확인 답변** 칸에 붙여넣어 제출하세요."
        )
        _hw_ui("데이터학습지시", _CHECK_SCRIPT, "train_hw_submit",
               ai_label="AI 학습결과 확인 답변",
               title="과제 제출 — AI 학습결과 확인")

# ----------------------------------------------------------
# 5. 배합비 개발
# ----------------------------------------------------------
elif section == "5️⃣ 배합비 개발":
    show_banner(
        "배합비 개발",
        "Gemini Gem에 등록된 음료개발 데이터베이스를 활용하여 신제품 음료 배합비를 AI와 함께 작성합니다.",
        "5 / 7"
    )
    show_mission([
        "Gem에 등록된 '음료개발_데이터베이스' 파일을 AI가 학습한 후 배합비를 작성하도록 스크립트 작성하기",
        "제품 컨셉·기능성 성분·과일향 조건을 스크립트에 반영하기",
        "배합시뮬레이터 구조를 반영한 텍스트 표로 원재료·배합비·단가·이화학 계산이 포함된 결과물 받기",
    ])

    st.markdown(
        '<div class="common-case-box">'
        '<b>📌 이 단계는 분야와 관계없이 전원 공통으로 “음료” 사례를 사용합니다</b><br>'
        '배합비 실습에는 원료 174종의 이화학·단가 데이터, 식품공전 규격, 원가 계산이 서로 연결된 '
        '<b>음료개발 데이터베이스</b>가 필요합니다. 그래서 사례는 음료로 고정합니다.<br>'
        '여기서 익히는 것은 음료 지식이 아니라 <b>① AI에게 배합 근거 데이터를 학습시키고, '
        '② 나온 배합비를 규격·원가로 검증하는 절차</b>이며, 이 절차 자체는 어느 제품군에서도 동일합니다. '
        '마지막 탭의 <b>“내 제품으로 옮기기”</b>에서 본인 제품 기준으로 정리하게 됩니다.'
        '</div>',
        unsafe_allow_html=True,
    )

    _S5_STEPS = ["DB 구조 확인", "예시 스크립트", "배합비 작성",
                 "미션1 검증", "미션2 대응", "연구원 검토", "마케터 미팅"]

    tab_db, tab_ex, tab_write, tab_m1, tab_m2, tab_p1, tab_p2 = st.tabs([
        "📊 데이터베이스 구조",
        "📖 예시 스크립트",
        "✏️ 배합비 작성",
        "🎯 미션1 · 무결성 검증",
        "🎯 미션2 · 시나리오 대응",
        "🔬 연구원 검토받기",
        "🤝 마케터와 미팅",
    ])

    # ── 음료개발_데이터베이스 구조 ──────────────────────
    with tab_db:
        show_step_guide(
            _S5_STEPS, 0,
            todo="AI가 배합비를 짤 때 참조하는 데이터베이스 10개 탭 구성을 확인합니다.",
            produces="어떤 데이터를 근거로 배합비가 나오는지에 대한 이해",
            minutes=5,
        )
        st.markdown("#### 📊 '음료개발_데이터베이스'란?")
        st.info("Gemini Gem의 지식(소스)으로 등록해둔 구글시트로, 10개의 탭에 배합비 개발에 필요한 데이터가 정리되어 있습니다. AI는 배합비를 작성하기 전 이 데이터를 먼저 학습합니다.")
        st.markdown("""
| 탭 | 내용 |
|---|---|
| **배합시뮬레이터** | 제품정보·배합표(약 20행)·시뮬레이션 결과·사용설명서 (메인 입력 시트) |
| **음료유형분류** | 18개 유형별 식품공전 정의·특성·대표제품·연매출 |
| **시장제품DB** | 실제 제품 291개(음료 115 + 시럽/잼 등) 배합순위1~7·용량·가격·당도·산도·pH |
| **원료DB** | 원료 174종의 Brix·pH·산도·감미도·단가·1%사용시 기여도 |
| **음료규격기준** | 17개 음료유형별 Brix·pH·산도·과즙함량 등 허용범위(식품공전 기준) |
| **표준제조공정_HACCP** | 5개 음료유형 제조공정 48행 — CCP·한계기준·모니터링·개선조치 |
| **원가계산서** | 1000ml 기준 원재료/포장재/제조경비 원가 계산 및 원가율 |
| **자재SPEC참조** | 당류·감미료·부자재·산도안정제의 Bx·감미도 스펙 |
| **과일Brix참조** | 과일별 한국기준 vs FDA 당도 기준 비교 |
| **가이드배합비DB** | 유형·맛별 AI추천 배합비 vs 실제사례 배합비 비교 |
""")
        st.caption(
            "💡 '예시 스크립트' 탭의 #사용자료 항목이 이 데이터베이스를 가리킵니다. "
            "여기에 없는 내용은 AI가 자기 지식으로 보완하되 [추론]으로 표시하게 되어 있습니다."
        )

        st.markdown("---")

        st.markdown("##### ⚙️ '배합시뮬레이터' 탭의 기본 로직")
        st.markdown("""
1. **음료유형 + 맛 선택** → 가이드배합비DB에서 일치하는 조합을 찾아 AI추천·실제사례 배합비를 표시 (매칭되면 초록색 표시, 없으면 직접입력)
2. **원료명 + 배합비(%) 입력** → 원료DB에서 해당 원료의 Brix·pH·산도·감미도·단가를 자동으로 불러옴
3. **가중합산으로 자동 계산**
   - 당도(Bx) = Σ(원료별 Bx × 배합비%)
   - 산도(%) = Σ(원료별 산도% × 배합비%)
   - 단가 = Σ(원료별 단가 × 배합량)
   - 정제수 배합비 = 100% − 입력한 원료 배합비 합계 (자동)
4. **규격 판정** → 계산된 당도·산도·과즙함량 등을 음료규격기준의 최소~최대 범위와 비교해 ✅ 충족 / ⚠️ 미충족으로 표시
5. **보조 참고자료** — 자재SPEC참조·과일Brix참조는 원료 선택 시 스펙 확인용, 표준제조공정_HACCP은 제조공정 설계용, 원가계산서는 최종 원가 산출에 연동, 시장제품DB는 유사 제품 비교용으로 쓰입니다.
""")

        st.markdown("---")

        st.markdown("##### 🧭 배합시뮬레이터 데이터 흐름")
        st.caption("배합시뮬레이터가 중심이 되어, 나머지 9개 탭의 데이터를 참조·검증합니다.")

        def _hub_card(icon, label):
            return f"""<div style="background:#ffffff;border:1.5px solid #94a3b8;border-radius:10px;
padding:18px 10px;text-align:center;height:100%;box-sizing:border-box;">
<div style="font-size:16px;font-weight:700;color:#1e293b;line-height:1.5;">{icon}<br>{label}</div>
</div>"""

        _down_arrow = '<div style="text-align:center;font-size:28px;color:#475569;line-height:1;padding:4px 0;">↓</div>'
        _up_arrow = '<div style="text-align:center;font-size:28px;color:#475569;line-height:1;padding:4px 0;">↑</div>'

        _top_labels = [("📖", "음료유형분류"), ("🛒", "시장제품DB"), ("🧪", "원료DB"),
                       ("📏", "음료규격기준"), ("🧂", "자재SPEC참조")]
        _top_cols = st.columns(len(_top_labels))
        for _col, (_icon, _label) in zip(_top_cols, _top_labels):
            with _col:
                st.markdown(_hub_card(_icon, _label), unsafe_allow_html=True)

        _arr_cols_top = st.columns(len(_top_labels))
        for _col in _arr_cols_top:
            with _col:
                st.markdown(_down_arrow, unsafe_allow_html=True)

        _, _center_col, _ = st.columns([1, 2, 1])
        with _center_col:
            st.markdown("""<div style="background:#1e293b;color:#ffffff;border-radius:10px;
padding:24px;text-align:center;font-size:20px;font-weight:800;">🎯 배합시뮬레이터<br>
<span style="font-size:15px;font-weight:500;color:#cbd5e1;">배합비 입력 · 규격 자동판정</span></div>""",
                        unsafe_allow_html=True)

        _bottom_labels = [("🏭", "표준제조공정_HACCP"), ("💰", "원가계산서"),
                          ("🍎", "과일Brix참조"), ("📋", "가이드배합비DB")]
        _arr_cols_bot = st.columns(len(_bottom_labels))
        for _col in _arr_cols_bot:
            with _col:
                st.markdown(_up_arrow, unsafe_allow_html=True)

        _bottom_cols = st.columns(len(_bottom_labels))
        for _col, (_icon, _label) in zip(_bottom_cols, _bottom_labels):
            with _col:
                st.markdown(_hub_card(_icon, _label), unsafe_allow_html=True)

    # ── 예시 스크립트 ──────────────────────────────────
    with tab_ex:
        show_step_guide(
            _S5_STEPS, 1,
            todo="완성된 배합비 스크립트 예시를 읽고 필요한 조건 항목을 파악합니다.",
            produces="배합비 스크립트 양식",
            minutes=5,
        )
        st.markdown("#### 배합비 작성 기준 스크립트 — 복숭아 프로틴 음료 예시")
        st.info("아래 스크립트 양식을 기준으로 '배합비 작성' 탭에서 나만의 스크립트를 완성하세요.")
        st.code("""#요청배경
신제품 음료의 배합비 작성

#사용자료 및 출력지침
Gem에 등록된 지식 파일(ChatGPT에서는 프로젝트에 올린 소스 파일)을 1순위 근거로 삼되,
부족한 부분은 네 지식으로 보완한다.
항목마다 [자료] 또는 [추론] 으로 근거를 구분해 표시하고,
[추론]으로 채운 값은 왜 그렇게 봤는지 한 줄로 근거를 적는다.

#요청사항
아래 제품컨셉으로 제안된 제품의 신제품음료 배합비를
AI 음료개발자 페르소나를 이용해 작성하세요

#제품컨셉
프로틴 20g이 함유된 과즙감이 살아있는 복숭아맛 음료

#출력결과
텍스트 표 형식으로 출력 (파이썬 코드 실행·파일 생성 금지, 요약문으로 대체 금지)

아래 열 구성 그대로 마크다운 표로, 원료 행마다 빠짐없이 채워서 출력하세요:
| No | 구분 | 원료명 | 배합비(%) | Brix 기여도 | 산도 기여도 | 감미도 기여도 | 단가 기여도(원) |

- 구분: 원재료 / 당류 / 안정제 / 기타자재 / 정제수 중 하나
- 각 행은 원료DB의 실제 Brix·산도·감미도·단가 값에 배합비(%)를 곱해 기여도를 계산할 것 (빈칸·생략 금지)
- 마지막 행에 정제수 = 100% − 원료 배합비 합계를 자동 계산해 추가
- 표 아래에 '시뮬레이션 결과 요약' 표를 별도로 추가: 당도(Bx)·산도(%)·과즙함량(%) 각 계산값을 음료규격기준의 최소~최대 범위와 비교해 ✅충족/⚠️미충족으로 표시

#작업가이드
데이터 결손이나 빈칸이 없어야 함.
시스템 부하가 걸리면, 나눠서 출력함. 배합 시뮬레이터양식에 맞출것
AI는 Gem의 지식을 배합비 작성전 학습할 것
위 요청사항과 명령을 모두 수행했을때 3회 검증후 결과물 출력하세요""", language=None)

        st.markdown("---")
        st.markdown("##### 스크립트 섹션별 작성 요령")
        for _tag, _desc in [
            ("#요청배경",  "배합비 작성 목적을 한 줄로 명시"),
            ("#사용자료 및 출력지침",
             "등록 자료를 1순위로 쓰고 부족분은 AI 지식으로 보완 → [자료]/[추론] 구분 표시"),
            ("#요청사항",  "AI 페르소나(음료개발자)를 지정하고 작업을 구체적으로 지시"),
            ("#제품컨셉",  "기능성 성분 + 과일향 + 제품 특성을 1~2줄로 압축"),
            ("#출력결과",  "텍스트 표 형식으로 고정 — 배합시뮬레이터 구조(열 구성·정제수 자동계산·규격판정)를 반영하도록 지정"),
            ("#작업가이드","빈칸 없음·검증 횟수·양식 준수 등 품질 기준 명시"),
        ]:
            st.markdown(f"- **`{_tag}`** — {_desc}")

    # ── 배합비 작성 ────────────────────────────────────
    with tab_write:
        show_step_guide(
            _S5_STEPS, 2,
            todo="제품유형·기능성·과일향 조건을 골라 나만의 배합비 스크립트를 완성합니다.",
            uses="STEP 4 시장분석 보고서에서 도출한 제품 방향",
            produces="배합비 개발 스크립트와 AI가 작성한 배합비",
            minutes=15,
        )
        def _bev_input(label, key, placeholder="직접 입력"):
            st.markdown(
                f'<div style="background:#fefce8;border-radius:6px;padding:4px 10px 2px 10px;'
                f'border:1.5px solid #fde047;margin-top:4px;">'
                f'<span style="font-size:11px;color:#854d0e;font-weight:600;">✏️ {label}</span></div>',
                unsafe_allow_html=True,
            )
            return st.text_input(key, key=key, placeholder=placeholder, label_visibility="collapsed")

        st.info(
            "힌트 항목을 선택하거나 노란색 셀에 직접 입력하세요. "
            "💡 텍스트 입력 후 **Enter**를 눌러 적용하세요.\n\n"
            "선택 완료 후 **[📥 스크립트 반영하기]** 버튼을 눌러 완성 스크립트를 업데이트하세요."
        )
        st.markdown("**Step 1. 힌트 선택 후 스크립트 초안 생성**")

        st.info("💡 '보고서 작성하기'에서 출력한 제품 보고서의 내용을 활용하여 제품명과 제품의 SPEC을 입력하세요.")

        # 제품명
        st.caption("🏷️ 제품명")
        bev_prodname = _bev_input("제품명 직접입력", "bev_prodname", "예: 복숭아 프로틴 샷 125ml")

        # 제품유형
        st.caption("🧃 제품유형")
        # 간소화: 5개 -> 4개 (제외: 발효음료)
        _PTYPE_OPTS = ["프로틴 음료", "저당 기능성음료", "과즙음료", "에너지음료"]
        bev_ptype = st.pills("제품유형", _PTYPE_OPTS, key="bev_ptype", label_visibility="collapsed")
        bev_ptype_c = _bev_input("오픈 항목 직접입력", "bev_ptype_c", "예: 기능성 RTD 음료")

        # 기능성 성분
        st.caption("💊 기능성 성분 (복수 선택)")
        # 간소화: 6개 -> 4개 (제외: BCAA 3g, 아연·마그네슘 복합)
        _FUNC_OPTS = ["프로틴 20g", "비타민C 1000mg", "콜라겐 5000mg", "식이섬유 5g"]
        bev_func = st.pills("기능성성분", _FUNC_OPTS, selection_mode="multi", key="bev_func", label_visibility="collapsed")
        bev_func_c = _bev_input("오픈 항목 직접입력", "bev_func_c", "예: 글루타민 2g")

        # 과일/향
        st.caption("🍑 과일 / 향")
        # 간소화: 7개 -> 4개 (제외: 사과, 청포도, 딸기)
        _FRUIT_OPTS = ["복숭아", "오렌지", "포도", "레몬"]
        bev_fruit = st.pills("과일향", _FRUIT_OPTS, key="bev_fruit", label_visibility="collapsed")
        bev_fruit_c = _bev_input("오픈 항목 직접입력", "bev_fruit_c", "예: 망고패션")

        # 제품 특성
        st.caption("✨ 제품 특성 (복수 선택)")
        # 간소화: 6개 -> 4개 (제외: 부드러운 텍스처, 무색소)
        _CHAR_OPTS = ["과즙감이 살아있는", "청량감 강한", "저당", "고단백"]
        bev_char = st.pills("제품특성", _CHAR_OPTS, selection_mode="multi", key="bev_char", label_visibility="collapsed")
        bev_char_c = _bev_input("오픈 항목 직접입력", "bev_char_c", "예: 투명한 외관")

        # 검증 횟수
        st.caption("🔁 검증 횟수")
        _VER_OPTS = ["3회", "5회"]
        bev_ver = st.pills("검증횟수", _VER_OPTS, key="bev_ver", label_visibility="collapsed")

        st.markdown("---")

        # 값 조합
        _bev_prodname = bev_prodname.strip()
        _bev_ptype  = ", ".join(filter(None, [bev_ptype, bev_ptype_c.strip()])) or "프로틴 음료"
        _bev_func   = (list(bev_func or []) + ([bev_func_c.strip()] if bev_func_c.strip() else [])) or ["프로틴 20g"]
        _bev_fruit  = ", ".join(filter(None, [bev_fruit, bev_fruit_c.strip()])) or "복숭아"
        _bev_char   = (list(bev_char or []) + ([bev_char_c.strip()] if bev_char_c.strip() else [])) or ["과즙감이 살아있는"]
        _bev_ver    = bev_ver or "3회"

        _concept_lines = []
        if _bev_prodname:
            _concept_lines.append(f"제품명: {_bev_prodname}")
        _concept_lines.append(f"{', '.join(_bev_func)}이 함유된 {', '.join(_bev_char)} {_bev_fruit}맛 {_bev_ptype}")
        _concept = "\n".join(_concept_lines)

        _out_line = (
            "텍스트 표 형식으로 출력 (파이썬 코드 실행·파일 생성 금지, 요약문으로 대체 금지)\n\n"
            "아래 열 구성 그대로 마크다운 표로, 원료 행마다 빠짐없이 채워서 출력하세요:\n"
            "| No | 구분 | 원료명 | 배합비(%) | Brix 기여도 | 산도 기여도 | 감미도 기여도 | 단가 기여도(원) |\n\n"
            "- 구분: 원재료 / 당류 / 안정제 / 기타자재 / 정제수 중 하나\n"
            "- 각 행은 원료DB의 실제 Brix·산도·감미도·단가 값에 배합비(%)를 곱해 기여도를 계산할 것 (빈칸·생략 금지)\n"
            "- 마지막 행에 정제수 = 100% − 원료 배합비 합계를 자동 계산해 추가\n"
            "- 표 아래에 '시뮬레이션 결과 요약' 표를 별도로 추가: 당도(Bx)·산도(%)·과즙함량(%) 각 계산값을 "
            "음료규격기준의 최소~최대 범위와 비교해 ✅충족/⚠️미충족으로 표시"
        )

        bev_script = f"""#요청배경
신제품 음료의 배합비 작성

#사용자료 및 출력지침
Gem에 등록된 지식 파일(ChatGPT에서는 프로젝트에 올린 소스 파일)을 1순위 근거로 삼되,
부족한 부분은 네 지식으로 보완한다.
항목마다 [자료] 또는 [추론] 으로 근거를 구분해 표시하고,
[추론]으로 채운 값은 왜 그렇게 봤는지 한 줄로 근거를 적는다.

#요청사항
아래 제품컨셉으로 제안된 제품의 신제품음료 배합비를
AI 음료개발자 페르소나를 이용해 작성하세요

#제품컨셉
{_concept}

#출력결과
{_out_line}

#작업가이드
데이터 결손이나 빈칸이 없어야 함.
시스템 부하가 걸리면, 나눠서 출력함. 배합 시뮬레이터양식에 맞출것
AI는 Gem의 지식을 배합비 작성전 학습할 것
위 요청사항과 명령을 모두 수행했을때 {_bev_ver} 검증후 결과물 출력하세요"""

        # 반영 버튼: 힌트 선택 내용을 완성 스크립트 텍스트 에어리어에 반영
        if st.button("📥 스크립트 반영하기", key="bev_apply_btn", use_container_width=True, type="primary"):
            st.session_state["bev_preview"] = bev_script
            st.rerun()

        st.markdown("**Step 2. 완성 스크립트 확인 및 복사**")
        st.caption("스크립트를 직접 수정할 수 있습니다. 수정 후 복사 버튼을 누르세요.")

        # 텍스트 에어리어: 처음에만 bev_script로 초기화
        if "bev_preview" not in st.session_state:
            st.session_state["bev_preview"] = bev_script
        st.text_area("완성 스크립트", key="bev_preview", height=320, label_visibility="collapsed")

        # 복사: 텍스트 에어리어(session_state)의 현재 내용을 스냅샷
        if st.button("📋 완성 스크립트 복사하기", key="bev_copy_btn", use_container_width=True):
            st.session_state["bev_copy_snapshot"] = st.session_state.get("bev_preview", bev_script)
            st.session_state["bev_show_copy"] = not st.session_state.get("bev_show_copy", False)
        if st.session_state.get("bev_show_copy"):
            _snap = st.session_state.get("bev_copy_snapshot", bev_script)
            st.code(_snap + _SUBMIT_INSTRUCTION, language=None)

        # 파일링크 불필요: 배합비 스크립트는 텍스트 제출로 충분
        _hw_ui("배합비", st.session_state.get("bev_preview", bev_script), "bev_hw_submit")

    # ── 미션수행 ───────────────────────────────────────
    with tab_m1:
        show_step_guide(
            _S5_STEPS, 3,
            todo="AI가 만든 배합비의 이화학 규격과 원가가 맞는지 검증하고 수정합니다.",
            uses="앞 단계에서 AI가 작성한 배합비",
            produces="검증·보정을 마친 배합비",
            minutes=10,
        )

        # ── 미션 1: 배합비 무결성 검증 ──────────────────
        st.markdown("---")
        st.markdown("""
<div style="background:#f8fafc;border-left:4px solid #1e293b;border-radius:0 8px 8px 0;
padding:14px 20px;margin-bottom:8px;">
<div style="font-size:15px;font-weight:800;color:#0f172a;margin-bottom:4px;">
🔍 미션 1. 배합비 무결성 검증</div>
<div style="font-size:13px;color:#475569;line-height:1.8;">
AI가 개발한 제품의 <b>이화학적 규격</b>(Brix·산도·pH·고형분함량)과
<b>원가</b>(원료별 단가·100ml당 원가)가 배합비 시트에 반영되었는지 확인하세요.
</div></div>""", unsafe_allow_html=True)

        st.caption("📋 AI에 줄 검증 요청 스크립트")
        st.code("""배합비 시트에서 아래 항목이 모두 반영되었는지 검증해줘.

[이화학적 규격 확인]
- Brix: 목표값과 계산값 일치 여부
- 산도: 산미료(구연산 등) 투입량 기준 산도 계산값
- pH: 배합 후 예상 pH 수치
- 고형분함량: 총 고형분 합계 (%)

[원가 확인]
- 원료별 단가: 모든 원재료 단가 컬럼 빈칸 없이 입력 여부
- 제품 100ml당 원가: 전체 배합량 기준 환산 원가 계산

누락 또는 오류 항목이 있으면 수정 후 전체 시트 다시 출력해줘.""", language=None)

        st.markdown("##### 검증 결과 입력")
        st.caption("AI가 출력한 시트를 확인하고, 이상이 있었는지·어떻게 고쳤는지 적으세요.")
        st.text_area(
            "검증 결과",
            placeholder=("예)\n"
                         "- Brix 11.2 / 산도 0.35% / pH 3.6 / 고형분 8.4% — 규격 범위 안\n"
                         "- 구연산 단가가 빈칸이어서 재요청 → 2,500원/kg 반영\n"
                         "- 100ml 원가가 기준량 오류 → 3,000ml 기준으로 재계산해 142원"),
            key="mv_note", height=140, label_visibility="collapsed",
        )

        with st.expander("▶ 정답 스크립트 보기"):
            st.caption("무결성 검증 후 시트 수정 요청 예시")
            st.code("""검증 결과 아래 항목이 누락/오류 상태야.
수정 후 전체 시트 다시 출력해줘.

- pH 컬럼: 수식 없이 공란 → 배합 후 예상 pH 계산식 추가
- 구연산 단가: 빈칸 → 시장 기준가 반영 (약 2,500원/kg)
- 100ml 원가: 기준량 환산 오류 → 전체 배합량(예: 3,000ml) 기준으로 재계산""",
                    language=None)

        # ── 미션 1 중간 제출 ─────────────────────────────
        _mission1_content = "\n".join([
            f"개발 제품명: {st.session_state.get('bev_prodname', '미입력')}",
            f"",
            f"[미션1 무결성 검증]",
            f"{st.session_state.get('mv_note', '')}",
        ])
        st.caption("💾 제출 후 다음 탭 **미션2 · 시나리오 대응**으로 넘어가세요.")
        _hw_ui("배합비_미션", _mission1_content, "bev_mission1_hw_submit", show_ai_field=False,
               title="검증결과 입력사항 과제 제출")

    with tab_m2:
        show_step_guide(
            _S5_STEPS, 4,
            todo="시나리오를 골라 그 상황을 해결하는 AI 요청 스크립트를 작성합니다.",
            uses="미션1에서 검증한 배합비",
            produces="시나리오 대응 스크립트",
            minutes=10,
        )

        # ── 미션 2: 시나리오 대응 스크립트 작성 ─────────
        st.markdown("---")
        st.markdown("""
<div style="background:#f8fafc;border-left:4px solid #1e293b;border-radius:0 8px 8px 0;
padding:14px 20px;margin-bottom:8px;">
<div style="font-size:15px;font-weight:800;color:#0f172a;margin-bottom:4px;">
🎯 미션 2. 배합비 시나리오 대응</div>
<div style="font-size:13px;color:#475569;line-height:1.8;">
아래 두 가지 시나리오 중 하나를 선택하고, 그 상황을 해결하는
<b>AI 요청 스크립트</b>를 직접 작성하세요.
</div></div>""", unsafe_allow_html=True)

        _SCN_OPTS = ["📉 시나리오 A — 원가절감", "👅 시나리오 B — 맛 개선"]
        ms2_scenario = st.pills("시나리오 선택", _SCN_OPTS, default=_SCN_OPTS[0],
                                key="ms2_scenario", label_visibility="collapsed")
        _cur_scn = ms2_scenario or _SCN_OPTS[0]

        if "A" in _cur_scn:
            st.markdown("""
<div style="background:#fefce8;border:1.5px solid #fde047;border-radius:10px;
padding:14px 18px;margin:8px 0;">
<b style="font-size:13px;color:#854d0e;">📉 시나리오 A — 원가절감</b>
<div style="font-size:13px;color:#713f12;margin-top:6px;line-height:1.8;">
<b>상황:</b> 원료 가격 인상으로 현재 배합비 기준 제품 단가가 목표를 <b>20% 초과</b>했습니다.<br>
<b>목표:</b> 맛·품질규격·기능성 원재료 함량 변화 없이 원가 20% 절감<br>
<b>조건:</b> Brix·pH·산도·고형분 규격 불변 / 기능성 성분 함량 불변
</div></div>""", unsafe_allow_html=True)

            st.markdown("**① 어떤 방법으로 원가를 줄일까요?**")
            _a1 = st.pills(
                "절감 방향",
                ["원료 대체", "배합비율 조정", "정제수 비율 상향", "농축액 농도 조정"],
                selection_mode="multi", default=["원료 대체", "배합비율 조정"],
                key="ms2_ha1", label_visibility="collapsed") or ["원료 대체", "배합비율 조정"]

            st.markdown("**② 결과를 어떤 형식으로 받을까요?**")
            _a2 = st.pills(
                "출력 형식",
                ["원재료별 절감액 표", "변경 전/후 비교표", "절감률 합계 포함"],
                selection_mode="multi", default=["변경 전/후 비교표", "절감률 합계 포함"],
                key="ms2_ha2", label_visibility="collapsed") or ["변경 전/후 비교표"]

            _ms2_default = f"""현재 배합비 기준 제품 원가를 20% 낮추는 방법을 제안해줘.

[조건]
- 맛(관능 프로파일)에 변화 없을 것
- 이화학적 품질규격(Brix·산도·pH·고형분) 유지
- 기능성 원재료 함량 변경 불가

[절감 방향]
{', '.join(_a1)}

[출력 형식]
{', '.join(_a2)}
원재료명 / 현재단가 / 대체원료 / 대체단가 / 절감액 / 주의사항을 표로 정리해줘.

[주의]
- 파이썬 코드를 실행하거나 파일을 분석하지 말고, 바로 마크다운 표로 답해줘."""

        else:
            st.markdown("""
<div style="background:#f0f9ff;border:1.5px solid #7dd3fc;border-radius:10px;
padding:14px 18px;margin:8px 0;">
<b style="font-size:13px;color:#0c4a6e;">👅 시나리오 B — 맛 개선</b>
<div style="font-size:13px;color:#075985;margin-top:6px;line-height:1.8;">
<b>상황:</b> 소비자 조사 결과 <b>"과즙감이 약하다"</b>, <b>"단맛이 강하다"</b>는 피드백이 다수 접수됐습니다.<br>
<b>목표:</b> 과즙감 향상 + 단맛 저감<br>
<b>조건:</b> 기능성 성분 함량·Brix·pH 규격 불변 / 원가 변동 최소화
</div></div>""", unsafe_allow_html=True)

            st.markdown("**① 어떤 방법으로 맛을 개선할까요?**")
            _b1 = st.pills(
                "개선 방향",
                ["과즙감 향상 (농축액 증량)", "단맛 저감 (감미료 배합 조정)",
                 "산미 강화 (산도 조절)", "향료 재배합"],
                selection_mode="multi",
                default=["과즙감 향상 (농축액 증량)", "단맛 저감 (감미료 배합 조정)"],
                key="ms2_hb1", label_visibility="collapsed") or ["과즙감 향상 (농축액 증량)"]

            st.markdown("**② 수정 결과를 어떻게 확인할까요?**")
            _b2 = st.pills(
                "검증 방법",
                ["관능 검사 항목 포함", "변경 전/후 배합비 비교", "Brix·pH 수치 재확인"],
                selection_mode="multi",
                default=["변경 전/후 배합비 비교", "관능 검사 항목 포함"],
                key="ms2_hb2", label_visibility="collapsed") or ["변경 전/후 배합비 비교"]

            _ms2_default = f"""현재 배합비를 아래 소비자 피드백에 따라 수정해줘.

[소비자 피드백]
- 과즙감이 약하다
- 단맛이 강하다

[개선 방향]
{', '.join(_b1)}

[조건]
- 기능성 성분 함량 불변
- 이화학적 규격(Brix·pH·산도) 기존 범위 유지
- 원가 변동 최소화

[확인 방법]
{', '.join(_b2)}
수정 후 전체 배합비 시트 다시 출력해줘.

[주의]
- 파이썬 코드를 실행하거나 파일을 분석하지 말고, 바로 마크다운 표로 답해줘."""

        st.session_state["ms2_script"] = _ms2_default

        st.markdown("---")
        st.markdown("**완성된 스크립트**")
        st.caption("위에서 고른 항목이 바로 반영됩니다. 복사해서 AI 대화창에 붙여넣으세요.")
        st.code(_ms2_default, language=None)

        if True:
            with st.expander("▶ 정답 스크립트 보기"):
                if "A" in (ms2_scenario or ""):
                    st.caption("원가절감 최적화 후 검증 요청 예시")
                    st.code("""최적화 배합비로 수정된 시트에서 아래를 최종 확인해줘.
1. 변경 전/후 원가 비교표 (원료별 절감액 명시)
2. 변경 후 Brix·pH·산도·고형분이 기존 규격 범위 내인지 확인
3. 기능성 성분 함량 유지 여부
4. 최종 절감률이 20% 이상인지 확인
5. 위 조건 모두 충족 시 확정본 전체 출력""", language=None)
                else:
                    st.caption("맛 개선 수정 후 검증 요청 예시")
                    st.code("""수정 배합비 시트에서 아래를 최종 확인해줘.
1. 변경 전/후 배합비 비교표 (변경된 원료·비율 명시)
2. 변경 후 Brix·pH·산도 수치가 기존 규격 범위 내인지 확인
3. 기능성 성분 함량 유지 여부
4. 관능 검사 예상 항목 (과즙감·단맛 척도 기준으로 개선 여부 평가 방법)
5. 위 조건 모두 충족 시 맛 개선 확정본 전체 출력""", language=None)

        # ── 미션수행 최종 제출 (미션1+미션2, 앞서 낸 미션1 중간제출을 덮어씀) ──
        _ms2_scn_label = ms2_scenario or "미선택"
        _mission_content = "\n".join([
            f"개발 제품명: {st.session_state.get('bev_prodname', '미입력')}",
            f"",
            f"[미션1 무결성 검증]",
            f"{st.session_state.get('mv_note', '')}",
            f"",
            f"[미션2 시나리오 대응]",
            f"선택 시나리오: {_ms2_scn_label}",
            f"작성 스크립트:\n{st.session_state.get('ms2_script', '')}",
        ])
        # 파일링크 필요: AI로 작성한 배합비를 구글 시트에 정리해 링크로 제출
        _hw_ui("배합비_미션", _mission_content, "bev_mission_hw_submit", with_file=True)

    # ── 개발 프로세스 실습 ──────────────────────────────
    with tab_p1:
        show_step_guide(
            _S5_STEPS, 5,
            todo="20년차 시니어 연구원 페르소나를 만들고, 그 연구원에게 내 배합비를 검토받습니다.",
            uses="앞 단계에서 만든 배합비",
            produces="시니어 연구원의 검증·코칭 의견",
            minutes=12,
        )
        show_mission([
            "① 시니어 연구원 페르소나 만들기 — 맛 프로파일·실험배합비 훈련",
            "② 배합비 검토받기 — 훈련된 AI가 내 배합비를 검증·코칭",
        ])


        _S1_PERSONA = (
            "식품개발 연구원의 보유한 식품지식과 실험이론을 20년 이상 경험한 시니어 연구원의 "
            "페르소나를 생성해주세요."
        )
        _S1_SCRIPTS = {
            "A — 실험실용 배합비 작성": (
                "음료개발 전문 연구소에서 소규모인 2kg 단위로 배합 테스트를 진행하는 경우에, "
                "실험배합비를 엑셀로 작성해주세요."
            ),
            "B — 실험 공정서 작성": (
                "실험절차 및 배합순에 따라서 실험순서를 작성해주세요."
            ),
            "C — 맛 엔진 학습": (
                "각 원료의 감미도, 산미도, 레올로지 특성, 입안의 맛 강도는 각 원료별 특성을 "
                "식품전문지식과 결합해서 가상으로 테스트하고 최적의 배합비를 도출하세요."
            ),
        }

        # ── STEP 1: 시니어 연구원 훈련 ──────────────────
        st.markdown("---")
        st.markdown("""
<div style="background:#f8fafc;border-left:4px solid #1e293b;border-radius:0 8px 8px 0;
padding:14px 20px;margin-bottom:12px;">
<div style="font-size:15px;font-weight:800;color:#0f172a;margin-bottom:4px;">
👨‍🔬 STEP 1. 시니어 연구원 페르소나 생성 &amp; 훈련</div>
<div style="font-size:13px;color:#475569;">
아래 표의 순서대로 AI 대화창에 입력하며 시니어 연구원을 훈련시키세요.<br>
각 항목을 반복·개선 학습시킨 후, 실험실용 배합비와 공정서를 출력합니다.
</div></div>""", unsafe_allow_html=True)

        st.markdown("""
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead>
<tr style="background:#1e293b;color:#fff;">
  <th style="padding:10px 14px;width:10%;text-align:center;border:1px solid #334155;">항목</th>
  <th style="padding:10px 14px;width:18%;text-align:center;border:1px solid #334155;">절차</th>
  <th style="padding:10px 14px;text-align:center;border:1px solid #334155;">스크립트 (AI에 그대로 입력)</th>
</tr>
</thead>
<tbody>
<tr>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;font-weight:700;text-align:center;vertical-align:top;">페르소나<br>생성</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;vertical-align:top;">시니어 연구원 페르소나 설정</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;line-height:1.8;">
    식품개발 연구원의 보유한 식품지식과 실험이론을 20년 이상 경험한 시니어 연구원의 페르소나를 생성해주세요. 페르소나로부터 현재 배합비를 분석하고, 리스크를 도출해주세요.
  </td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:10px 14px;border:1px solid #cbd5e1;font-weight:700;text-align:center;vertical-align:top;">A</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;vertical-align:top;">실험실용<br>배합비 작성</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;line-height:1.8;">
    음료개발 전문 연구소에서 소규모인 2kg 단위로 배합 테스트를 진행하는 경우에, 실험배합비를 엑셀로 작성해주세요.
  </td>
</tr>
<tr>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;font-weight:700;text-align:center;vertical-align:top;">B</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;vertical-align:top;">실험 공정서<br>작성</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;line-height:1.8;">
    실험절차 및 배합순에 따라서 실험순서를 작성해주세요.
  </td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:10px 14px;border:1px solid #cbd5e1;font-weight:700;text-align:center;vertical-align:top;">C</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;vertical-align:top;">맛 엔진<br>학습</td>
  <td style="padding:10px 14px;border:1px solid #cbd5e1;line-height:1.8;">
    각 원료의 감미도, 산미도, 레올로지 특성, 입안의 맛 강도는 각 원료별 특성을 식품전문지식과 결합해서 가상으로 테스트하고 최적의 배합비를 도출하세요.
  </td>
</tr>
</tbody>
</table>""", unsafe_allow_html=True)

        st.markdown("")

        # ── A·B·C 훈련 항목 선택
        st.caption("함께 훈련시킬 항목을 선택하세요 (미선택 시 전체 포함)")
        _s1_sel = st.pills(
            "훈련 항목 선택",
            list(_S1_SCRIPTS.keys()),
            selection_mode="multi",
            key="proc_s1_sel",
            label_visibility="collapsed",
        )

        # ── 페르소나 생성 + 선택 훈련항목 통합 내보내기 + 결과 입력
        if st.button("📋 페르소나 생성 & 훈련 스크립트 내보내기", key="proc_s1_btn",
                     use_container_width=True):
            st.session_state["proc_s1_show"] = not st.session_state.get(
                "proc_s1_show", False)
        if st.session_state.get("proc_s1_show"):
            _train_items = _s1_sel or list(_S1_SCRIPTS.keys())
            _train_block = "\n\n".join(f"[{k}]\n{_S1_SCRIPTS[k]}" for k in _train_items)
            _combined_s1 = f"[시니어 연구원 페르소나 생성]\n{_S1_PERSONA}\n\n[훈련 항목]\n{_train_block}\n\n결과는 3줄 이내로 핵심만 요약해주세요."
            st.code(_combined_s1, language=None)

        st.markdown("**📋 STEP 1 결과 — AI 출력 붙여넣기**")
        st.caption("위 스크립트를 AI에 입력한 후 나온 결과를 그대로 붙여넣으세요.")
        _s1_result = st.text_area("s1_memo",
                     placeholder="AI가 출력한 시니어 연구원 페르소나 생성 & 훈련 결과를 여기에 붙여넣으세요.",
                     key="proc_step1", height=120, label_visibility="collapsed")
        if _s1_result and "\n" not in _s1_result and len(_s1_result) > 60:
            st.warning("줄바꿈(Enter)이 없습니다. AI 결과 전체를 여러 줄로 붙여넣어 주세요.")

        # ── STEP 2: 배합비 검증 & 코칭 ─────────────────
        st.markdown("---")
        st.markdown("""
<div style="background:#f8fafc;border-left:4px solid #1e293b;border-radius:0 8px 8px 0;
padding:14px 20px;margin-bottom:12px;">
<div style="font-size:15px;font-weight:800;color:#0f172a;margin-bottom:4px;">
🔍 STEP 2. 생성된 배합비 검증 &amp; 코칭</div>
<div style="font-size:13px;color:#475569;">
아래 스크립트로 시니어 연구원을 불러온 뒤, 제미나이 대화창에서 생성된 신제품 배합비에 대한
평가·코칭을 요청하세요. 배합비는 별도로 제시할 필요 없이 AI 내 생성된 결과를 그대로 활용합니다.
</div></div>""", unsafe_allow_html=True)

        _S2_RECALL = """앞서 설정된 시니어 음료 연구원 페르소나로 돌아와주세요.

방금 생성한 신제품 배합비에 대해 아래 항목으로 검토하고 코칭해주세요:
1. 이화학적 규격 (Brix·pH·산도·고형분) 적정 여부
2. 원료 배합 순서 및 공정상 리스크
3. 기능성 성분 함량 목표치 달성 여부
4. 개선이 필요한 원료·비율 코칭

결과는 3줄 이내로 핵심만 요약해주세요."""

        if st.button("📋 시니어 연구원 불러오기 스크립트", key="proc_s2_recall_btn",
                     use_container_width=True):
            st.session_state["proc_s2_show"] = not st.session_state.get(
                "proc_s2_show", False)
        if st.session_state.get("proc_s2_show"):
            st.code(_S2_RECALL, language=None)

        st.markdown("**📋 STEP 2 결과 — AI 출력 붙여넣기**")
        st.caption("위 스크립트를 AI에 입력한 후 나온 코칭 결과를 그대로 붙여넣으세요.")
        _s2_result = st.text_area("s2memo", placeholder="AI가 출력한 배합비 검증·코칭 결과를 여기에 붙여넣으세요.",
                     key="proc_step2", height=120, label_visibility="collapsed")
        if _s2_result and "\n" not in _s2_result and len(_s2_result) > 60:
            st.warning("줄바꿈(Enter)이 없습니다. AI 결과 전체를 여러 줄로 붙여넣어 주세요.")

    with tab_p2:
        show_step_guide(
            _S5_STEPS, 6,
            todo="마케터 페르소나와 미팅해 연구원 시각과 균형 잡힌 최종안을 만듭니다.",
            uses="연구원 검토를 마친 배합비",
            produces="최종 확정안 — STEP 6 가상검증의 입력값",
            minutes=10,
        )
        show_mission([
            "마케터 페르소나와 인터뷰 — 연구원 관점과 균형 잡힌 시각으로 최종안 도출",
        ])

        # ── 마케터 인터뷰 ────────────────────────
        st.markdown("""
<div style="background:#f0fdf4;border-left:4px solid #10b981;border-radius:0 8px 8px 0;
padding:14px 20px;margin-bottom:16px;">
<div style="font-size:15px;font-weight:800;color:#064e3b;margin-bottom:4px;">
🤝 STEP 3. 마케터 페르소나 인터뷰 → 균형 잡힌 시각 도출</div>
<div style="font-size:13px;color:#065f46;">
아래 고정 스크립트를 AI에 입력하면 STEP 1·2의 연구원 훈련·검증 결과를 토대로
마케터 페르소나가 균형 잡힌 시각으로 인터뷰를 진행합니다.
</div></div>""", unsafe_allow_html=True)

        # ── 전략 지표 차트 + 회의실 비주얼 ──────────────
        st.markdown(
            "<div style='display:flex;gap:14px;margin:4px 0 20px;flex-wrap:wrap;'>"

            "<div style='flex:1;min-width:200px;background:#fff;border:1.5px solid #e2e8f0;"
            "border-radius:12px;padding:18px;'>"
            "<div style='font-size:12px;font-weight:700;color:#0f172a;margin-bottom:2px;'>📊 제품 전략 평가 지표</div>"
            "<div style='font-size:10px;color:#64748b;margin-bottom:14px;'>연구원 × 마케터 협업 분석 (예시)</div>"
            "<div style='margin-bottom:9px;'><div style='display:flex;justify-content:space-between;margin-bottom:3px;'>"
            "<span style='font-size:11px;color:#334155;'>시장성</span>"
            "<span style='font-size:11px;font-weight:700;color:#3b82f6;'>85%</span></div>"
            "<div style='background:#e2e8f0;border-radius:4px;height:8px;'>"
            "<div style='background:#3b82f6;width:85%;height:8px;border-radius:4px;'></div></div></div>"
            "<div style='margin-bottom:9px;'><div style='display:flex;justify-content:space-between;margin-bottom:3px;'>"
            "<span style='font-size:11px;color:#334155;'>관능 경쟁력</span>"
            "<span style='font-size:11px;font-weight:700;color:#10b981;'>72%</span></div>"
            "<div style='background:#e2e8f0;border-radius:4px;height:8px;'>"
            "<div style='background:#10b981;width:72%;height:8px;border-radius:4px;'></div></div></div>"
            "<div style='margin-bottom:9px;'><div style='display:flex;justify-content:space-between;margin-bottom:3px;'>"
            "<span style='font-size:11px;color:#334155;'>원가 경쟁력</span>"
            "<span style='font-size:11px;font-weight:700;color:#f59e0b;'>68%</span></div>"
            "<div style='background:#e2e8f0;border-radius:4px;height:8px;'>"
            "<div style='background:#f59e0b;width:68%;height:8px;border-radius:4px;'></div></div></div>"
            "<div style='margin-bottom:9px;'><div style='display:flex;justify-content:space-between;margin-bottom:3px;'>"
            "<span style='font-size:11px;color:#334155;'>차별화 포인트</span>"
            "<span style='font-size:11px;font-weight:700;color:#8b5cf6;'>90%</span></div>"
            "<div style='background:#e2e8f0;border-radius:4px;height:8px;'>"
            "<div style='background:#8b5cf6;width:90%;height:8px;border-radius:4px;'></div></div></div>"
            "<div><div style='display:flex;justify-content:space-between;margin-bottom:3px;'>"
            "<span style='font-size:11px;color:#334155;'>시장 진입 가능성</span>"
            "<span style='font-size:11px;font-weight:700;color:#ef4444;'>78%</span></div>"
            "<div style='background:#e2e8f0;border-radius:4px;height:8px;'>"
            "<div style='background:#ef4444;width:78%;height:8px;border-radius:4px;'></div></div></div>"
            "</div>"

            "<div style='flex:1;min-width:200px;background:linear-gradient(160deg,#1e293b 0%,#0f172a 100%);"
            "border-radius:12px;padding:18px;'>"
            "<div style='font-size:11px;font-weight:700;color:#e2e8f0;margin-bottom:14px;'>🏛️ 전략 회의실 — 연구원 × 마케터</div>"
            "<div style='background:#334155;border-radius:40px;height:36px;margin:0 16px 10px;"
            "display:flex;align-items:center;justify-content:center;border:2px solid #475569;'>"
            "<span style='font-size:10px;color:#94a3b8;letter-spacing:1px;'>CONFERENCE TABLE</span></div>"
            "<div style='display:flex;justify-content:space-around;align-items:center;margin-bottom:14px;'>"
            "<div style='text-align:center;'><div style='font-size:28px;'>👨‍🔬</div>"
            "<div style='font-size:9px;color:#93c5fd;margin-top:2px;'>시니어 연구원</div></div>"
            "<div style='font-size:18px;color:#475569;'>⇄</div>"
            "<div style='text-align:center;'><div style='font-size:28px;'>👩‍💼</div>"
            "<div style='font-size:9px;color:#6ee7b7;margin-top:2px;'>마케터</div></div></div>"
            "<div style='background:rgba(59,130,246,0.15);border-left:3px solid #3b82f6;"
            "border-radius:0 6px 6px 0;padding:7px 10px;margin-bottom:7px;'>"
            "<div style='font-size:10px;color:#93c5fd;'>👨‍🔬 &nbsp;\"배합비 최적화 완료 · Brix 12° 달성\"</div></div>"
            "<div style='background:rgba(16,185,129,0.15);border-left:3px solid #10b981;"
            "border-radius:0 6px 6px 0;padding:7px 10px;'>"
            "<div style='font-size:10px;color:#6ee7b7;'>👩‍💼 &nbsp;\"저당 트렌드 부합 · 편의점 출시 추천\"</div></div>"
            "</div>"

            "</div>",
            unsafe_allow_html=True,
        )

        st.caption("아래 스크립트를 복사해 AI에 붙여넣으세요.")
        st.code(
            "이들의 step1,2,3을 시니어연구원의 훈련내용과 개선내용을 토대로 "
            "마케터 페르소나의 균형잡힌 시각의 인터뷰를 진행해주세요.",
            language=None,
        )

        st.markdown("**📋 STEP 3 결과 — AI 인터뷰 결과 붙여넣기**")
        st.caption("AI가 진행한 연구원 × 마케터 인터뷰 내용을 그대로 붙여넣으세요.")
        _s3_result = st.text_area("s3memo",
                     placeholder="AI가 출력한 마케터 인터뷰 결과를 여기에 붙여넣으세요.",
                     key="proc_step3", height=150, label_visibility="collapsed")
        if _s3_result and "\n" not in _s3_result and len(_s3_result) > 60:
            st.warning("줄바꿈(Enter)이 없습니다. AI 결과 전체를 여러 줄로 붙여넣어 주세요.")

        show_transfer_box(
            "s5",
            "이 배합 개발·검증 절차를 내 제품에 적용하면 무엇이 달라질까요? (규격 항목·검증 지표 중심)",
            "예: Brix·산도 대신 수분활성도·염도·동결점을 규격으로 잡고, 원가는 kg당 단가로 계산",
            secret_warn=True,
        )

        # ── 과제 제출 (STEP별 분리 저장) ────────────────
        st.markdown("---")
        st.markdown("##### 📤 과제 제출")
        st.caption("STEP 1·2·3 결과가 모두 입력되면 제출 버튼을 누르세요. 각 STEP은 구글시트 별도 열에 저장됩니다.")
        _proc_student = st.session_state.get("student_name", "")
        if not _proc_student:
            st.warning("과제를 제출하려면 먼저 로그인하세요.")
        else:
            _all_filled = bool(
                st.session_state.get("proc_step1", "").strip() and
                st.session_state.get("proc_step2", "").strip() and
                st.session_state.get("proc_step3", "").strip()
            )
            if not _all_filled:
                st.info("STEP 1·2·3 결과를 모두 입력해야 제출할 수 있습니다.")
            _proc_btn = st.button(
                "📤 개발 프로세스 제출",
                key="proc_hw_submit",
                type="primary",
                disabled=not _all_filled,
                use_container_width=True,
            )
            if _proc_btn:
                _ok, _err = _submit_process_hw(
                    _proc_student,
                    st.session_state.get("proc_step1", ""),
                    st.session_state.get("proc_step2", ""),
                    st.session_state.get("proc_step3", ""),
                )
                if _ok:
                    st.success(f"✅ **{_proc_student}** 님 제출 완료!")
                else:
                    st.error(f"제출 실패: {_err}")


# ----------------------------------------------------------
# 6. 가상모델 개발
# ----------------------------------------------------------
elif section == "6️⃣ 가상모델 개발":
    show_banner(
        "가상모델 개발",
        "디지털 트윈랩 실험, 가상 소비자 모델 제작, 관능검사를 통해 AI 기반 제품 검증을 수행합니다.",
        "6 / 7"
    )
    show_mission([
        "디지털 트윈랩에서 배합비 원료 비중을 조정하며 이화학 지표를 확인하세요",
        "가상 소비자 패널을 설계하고 관능조사 스크립트를 작성하세요",
        "가상 관능검사를 진행하고 합격 여부를 확인하세요",
    ])

    _S6_STEPS = ["스크립트 예시", "디지털 트윈랩", "가상 소비자 모델", "관능검사"]

    tab_ex, tab_twin, tab_consumer, tab_sensory = st.tabs([
        "📋 스크립트 예시", "🔬 디지털 트윈랩", "👥 가상 소비자 모델 제작", "🧪 관능검사"
    ])

    # ── Tab 0: 스크립트 예시 ──────────────────────────────
    with tab_ex:
        show_step_guide(
            _S6_STEPS, 0,
            todo="트윈랩 시뮬레이터 기본 예시 스크립트를 확인합니다.",
            produces="시뮬레이터 스크립트 골격",
            minutes=5,
        )
        st.markdown("##### 📋 디지털 트윈랩 HTML 시뮬레이터 — 기본 예시 스크립트")
        st.caption("아래는 기본형 스크립트 예시입니다. 오른쪽 '디지털 트윈랩' 탭에서 구성 요소를 선택해 나만의 맞춤 스크립트를 만드세요.")
        _TWIN_EXAMPLE = (
            "[디지털 트윈랩 HTML 시뮬레이터 제작 요청]\n\n"
            "음료개발 연구원 페르소나가 개발한 제품명과 최종 배합비를 기반으로 "
            "아래 기능을 갖춘 인터랙티브 HTML 시뮬레이터를 단일 HTML 파일로 만들어주세요.\n\n"
            "[필수 기능]\n"
            "1. 원료 배합표: 원료명 / 배합비율(%) 슬라이더+숫자 입력 / 2kg 기준량(g) / 단가(원/kg) / Brix기여 / 산도기여 / 100ml원가\n"
            "2. 실시간 지표 계산 (슬라이더 조정 시 즉시 반영):\n"
            "   - 배합 합계(%) — 100%와의 오차 표시\n"
            "   - 100ml 원가(원)\n"
            "   - Brix (°Bx)\n"
            "   - 산도 (%)\n"
            "   - pH (추정값)\n"
            "3. 리스크 검증 항목 선택 버튼: 원가초과 / Brix이탈 / pH이탈 / 산도이탈 / 배합합계오류 / 기능성미달\n"
            "   — 각 항목 선택 시 해당 리스크 설명과 개선 방향 표시\n\n"
            "[디자인 요건]\n"
            "- 깔끔한 카드형 레이아웃, 모바일 대응(반응형)\n"
            "- 상단에 제품명 표시, 전체 배경 연한 회색\n"
            "- 지표 카드 5개 가로 배열, 배합합계 오차 시 빨간색 표시\n\n"
            "완성된 전체 HTML 코드를 출력해주세요 (외부 라이브러리 없이 순수 HTML/CSS/JS로)."
        )
        st.code(_TWIN_EXAMPLE, language=None)

    # ── Tab 1: 디지털 트윈랩 ──────────────────────────────
    with tab_twin:
        show_step_guide(
            _S6_STEPS, 1,
            todo="반응 컬럼·요약 카드·공정 애니메이션을 골라 나만의 시뮬레이터를 만듭니다.",
            uses="STEP 5에서 확정한 최종 배합비",
            produces="배합비와 연동되는 HTML 트윈랩",
            minutes=20,
        )
        st.markdown("##### 🔬 디지털 트윈랩 — 맞춤형 HTML 앱 스크립트 생성")
        st.caption(
            "포함할 기능과 제조공정 단계를 선택하면 AI에게 전달할 HTML 앱 제작 스크립트가 자동으로 만들어집니다. "
            "생성된 스크립트를 제미나이에 입력하고, 받은 HTML 코드를 아래에 붙여넣어 바로 실행하세요."
        )

        # ── A-1. 배합표 반응 컬럼 선택 (슬라이더 조정 시 실시간 변화) ─────
        st.markdown("**A. 배합비 슬라이더 → 실시간 반응 컬럼 선택**")
        st.caption(
            "원료 비율 슬라이더를 움직이면 아래에서 선택한 컬럼이 수치 변경 + 색상 피드백으로 즉시 반응합니다. "
            "초록=정상 범위 / 노랑=주의 / 빨강=이탈."
        )
        _COL_OPTS = [  # 간소화: 9개 -> 4개
            "단가 기여 (원/kg × 비율 → 원료비)",
            "100ml 원가 합산",
            "Brix 기여 (당도 기여값)",
            "배합합계 오차 (±경고)",
        ]
        twin_cols = st.pills(
            "반응 컬럼", _COL_OPTS, selection_mode="multi",
            key="twin_cols", label_visibility="collapsed",
        )
        if not twin_cols:
            twin_cols = _COL_OPTS

        # ── A-2. 요약 지표 카드 선택 ────────────────────────────
        st.markdown("**배합표 상단 요약 카드 (슬라이더 연동 실시간 계산)**")
        _CARD_OPTS = [  # 간소화: 8개 -> 4개
            "배합합계 (%)",
            "100ml 원가 (원)",
            "Brix (°Bx)",
            "산도 (%)",
        ]
        twin_cards = st.pills(
            "요약 카드", _CARD_OPTS, selection_mode="multi",
            key="twin_cards", label_visibility="collapsed",
        )
        if not twin_cards:
            twin_cards = _CARD_OPTS

        # ── A-3. 추가 패널 ────────────────────────────────────
        st.markdown("**추가 패널**")
        _SIM_OPTS = [
            "리스크 검증 패널",
            "배합합계 오차 경고 배너",
            "원가 목표 입력 & 초과 알림",
        ]
        twin_features = st.pills(
            "추가 패널", _SIM_OPTS, selection_mode="multi",
            key="twin_features", label_visibility="collapsed",
        )
        if not twin_features:
            twin_features = _SIM_OPTS[:2]

        # ── B. 제조공정 애니메이션 ──────────────────────────────
        st.markdown("**B. 제조공정 애니메이션 포함 여부**")
        st.caption("각 공정 단계별 동작 특성에 맞는 움직이는 그래픽(SVG/CSS 애니메이션)을 HTML 앱에 추가합니다.")
        twin_include_flow = st.checkbox("제조공정 애니메이션 포함", value=True, key="twin_include_flow")

        twin_process = []
        twin_link = False
        if twin_include_flow:
            _PROC_STEPS = [  # 간소화: 10개 -> 4개 (핵심 공정만)
                "원료 계량 (저울·눈금 애니메이션)",
                "용해·혼합 (탱크 내부 교반기 회전)",
                "살균 (파이프 내 열수 흐름·온도 표시)",
                "충전 (노즐에서 액체 낙하·병 채워짐)",
            ]
            twin_process = st.multiselect(
                "포함할 공정 단계",
                _PROC_STEPS,
                default=_PROC_STEPS,
                key="twin_process",
            )
            twin_link = st.checkbox(
                "배합비 슬라이더 변경 시 해당 공정 단계 강조 연계",
                value=True, key="twin_link",
            )

        # ── 스크립트 동적 생성 ────────────────────────────────
        _col_detail_map = {
            "단가 기여 (원/kg × 비율 → 원료비)":
                "단가기여(원): 단가(원/kg) × 비율(%) ÷ 100 으로 계산, 슬라이더 조정 시 즉시 갱신 + 값이 클수록 주황",
            "100ml 원가 합산":
                "100ml원가(원): 모든 원료 단가기여 합산, 목표원가 미입력 시 회색·초과 시 빨강",
            "목표원가 대비 초과 여부":
                "목표원가 입력 칸 → 합산 100ml원가와 비교해 초과 시 해당 행 배경 빨강·미달 시 초록",
            "Brix 기여 (당도 기여값)":
                "Brix기여(°Bx): 원료별 Brix계수 × 비율로 계산, 슬라이더 변화 시 셀 숫자+배경색 동시 변경 (목표Brix 범위 내=초록, 이탈=빨강)",
            "산도 기여 (%)":
                "산도기여(%): 원료별 산도계수 × 비율, 색상 피드백: 0.3% 이하=초록, 0.3~0.5%=노랑, 0.5% 초과=빨강",
            "pH 추정값":
                "pH: 산도기여 합산으로 추정, 4.0~4.5=초록, 3.5~4.0=노랑, 3.5 미만=빨강",
            "감미 강도 지수":
                "감미강도: 원료별 감미도계수(설탕=1.0, 액상과당=1.2, 스테비아=200 등) × 비율 합산, 목표 감미도 대비 달성률 게이지",
            "기능성 성분 함량 기여":
                "기능성함량(mg): 원료별 기능성성분 함량(mg/g) × 투입량(g), 목표치 달성 여부를 색상+게이지로 표시",
            "배합합계 오차 (±경고)":
                "배합합계(%): 전체 원료 비율 합산, 100%±0.5% 이내=초록, 초과/미달=빨강 배경 + 셀 강조",
        }
        _panel_map = {
            "리스크 검증 패널":
                "- 리스크 검증 버튼 패널: 원가초과 / Brix이탈 / pH이탈 / 산도이탈 / 배합합계오류 / 기능성미달 — 각 버튼 클릭 시 해당 리스크 설명과 개선 방향을 팝업 또는 하단 패널로 표시",
            "배합합계 오차 경고 배너":
                "- 배합합계 오차 경고: 상단 고정 배너로 100%±0.5% 이탈 시 빨간 경고 + 부족/초과 g 수치 표시",
            "원가 목표 입력 & 초과 알림":
                "- 목표원가 입력 필드 → 현재 100ml 원가와 실시간 비교, 초과 시 배너 + 초과 원료 행 강조",
        }

        _prod_name = st.session_state.get("bev_prodname", "개발 제품명 입력")
        _col_labels = ", ".join(twin_cols) if twin_cols else "단가기여, Brix기여, 산도기여, pH, 감미강도"
        _card_labels = ", ".join(twin_cards) if twin_cards else "배합합계, 100ml원가, Brix, 산도, pH"

        _parts = [
            "[디지털 트윈랩 HTML 앱 — 상세 구현 명세서]\n\n",
            f"음료개발 연구원이 개발한 '{_prod_name}' 배합비를 기반으로 "
            "아래 명세를 100% 구현한 단일 HTML 파일을 작성해주세요.\n\n",
            "【필수 준수】 [SVG 애니메이션], [열수 흐름], [수위 상승] 같은 placeholder 텍스트 절대 사용 금지.\n"
            "모든 SVG 그래픽, CSS @keyframes 애니메이션, JavaScript 계산 로직을 실제 작동하는 완전한 코드로 구현하세요.\n\n",
        ]

        _parts.append(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "[섹션1] 상단 헤더\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "배경 #1a237e, 흰색 제품명 H2, 우측에 리스크 신호등:\n"
            "SVG 원형 3개(빨강 #f44336 · 노랑 #ff9800 · 초록 #4caf50) — 현재 상태 원만 "
            "filter:drop-shadow(0 0 6px 해당색) glow 효과, 나머지는 opacity:0.3\n"
            "신호등 옆 상태 텍스트: '전체 정상' / '주의 필요' / '위험 — 슬라이더 조정 필요'\n\n"
        )

        _parts.append(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "[섹션2-A] 요약 지표 카드 (슬라이더 연동 실시간)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "카드: 지표명(12px 회색) | 현재값(24px bold, 변경 시 0.2s @keyframes flipNum) | "
            "하단 얇은 progress bar(width JS 조정, 초록/노랑/빨강)\n"
        )
        _parts.append(f"표시 카드 목록: {_card_labels}\n\n")

        _parts.append(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "[섹션2-B] 배합비 패널(좌 65%) + 리스크 대시보드(우 35%)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "▶ 배합비 인터랙티브 패널:\n"
            "  헤더: 원료명 | 비율슬라이더 | 비율% | 2kg량(g) | [반응컬럼] | 최소% | 최대% | 상태\n"
            "  각 원료 행:\n"
            "  - <input type='range' min='0' max='100' step='0.1' oninput='recalc()'>\n"
            "  - 슬라이더 위 bubble tooltip: position:absolute, 슬라이더 thumb 위치에 따라 left JS 조정\n"
            "  - 반응 컬럼 셀: background-color transition:0.3s, 이탈 시 셀 배경 flash\n"
            "  계산 공식:\n"
            "    단가기여(원) = 단가(원/kg) × 비율/100 × 20\n"
            "    Brix기여(°Bx) = 원료별Brix계수 × 비율/100\n"
            "    산도기여(%) = 원료별산도계수 × 비율/100\n"
            "    pH = Math.max(2, 7 - Math.log10((산도기여합+0.001) × 100))\n"
            "    감미강도 = 원료별감미계수 × 비율/100  (설탕=1.0, 액상과당=1.2, 스테비아=200)\n"
        )
        _parts.append(f"  반응 컬럼: {_col_labels}\n")
        _parts.append(
            "  위험구간: min%/max% 입력 → 이탈 시 행 background:rgba(255,0,0,0.12) + 좌측 border-left:3px solid #f44336 + 상태칸 ❌\n"
            "  합계 행: 배합합계% — 100±0.5% 이탈 시 빨간 bold + @keyframes shake{0%,100%{translateX(0)}25%{translateX(-4px)}75%{translateX(4px)}}\n"
            "  [+ 원료 추가] 버튼: JS로 새 행 동적 삽입\n\n"
            "▶ 리스크 대시보드 (우측 패널, 짙은 배경 #1e2a3a):\n"
            "  SVG 원형 게이지 5개 (각 110×110px, 2×3 그리드):\n"
            "    <circle r='45' cx='55' cy='55'> — 배경 stroke:#334 strokeWidth=10\n"
            "    값 arc: stroke-dasharray='283' (circumference=2π×45)\n"
            "    stroke-dashoffset = 283 × (1 - value/maxValue) — JS로 실시간 갱신\n"
            "    색상: 정상=#4caf50 / 주의=#ff9800 / 이탈=#f44336\n"
            "    중앙: <text> 현재값 숫자 (JS로 textContent 업데이트)\n"
            "    게이지 5종: Brix / 산도 / pH / 100ml원가 / 배합합계\n"
            "  하단 경고등 목록 (어두운 행):\n"
            "    각 항목: SVG circle r=7 (정상=초록/이탈=빨강 + @keyframes blink) + 항목명 + 상태텍스트\n"
            "    항목: 원가초과 / Brix이탈 / pH이탈 / 산도이탈 / 배합합계오류 / 기능성미달\n\n"
        )

        for panel in twin_features:
            _parts.append(_panel_map.get(panel, f"- {panel}") + "\n")

        if twin_include_flow and twin_process:
            _parts.append(
                "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "[섹션3] 제조공정 설비 애니메이션 — 배합 시뮬레이터 바로 아래 항상 펼쳐진 상태\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "탭 없이 항상 표시. 공정 카드를 좌→우로 → 화살표로 연결해 전체 흐름 표시.\n"
                "각 카드: SVG + CSS @keyframes로 실제 설비 동작 완전 구현. placeholder 절대 금지.\n\n"
                "[카드 에러 연동 규칙]\n"
                "- 정상: border:2px solid #4caf50\n"
                "- 주의: border:2px solid #ff9800 + 우상단 ⚠️ 배지(SVG 삼각형)\n"
                "- 이탈: border:2px solid #f44336 + @keyframes borderBlink{0%,100%{border-color:#f44336}50%{border-color:#ffcdd2}} + 하단 에러 텍스트\n\n"
                "[배합값 → 공정 에러 연동]\n"
                "배합합계 이탈 → 혼합탱크/교반기 에러\n"
                "Brix 이탈 → 교반기 과속(animation-duration:0.4s) + 냉각 경고\n"
                "pH/산도 이탈 → 살균 에러\n"
                "원가 초과 → 충전 에러\n"
                "기능성 미달 → 캡핑 에러\n"
                "미해결 리스크 있음 → 포장 컨베이어 정지 + 출하 트럭 정지\n\n"
                "[공정 카드별 SVG 설비 구현 명세 — 아래 코드 구조를 그대로 구현하세요]\n\n"
            )

            _svg_spec = {
                "원료 계량 (저울·눈금 애니메이션)":
                    "【원료 계량/혼합 탱크】\n"
                    "SVG 200×160: 원통형 탱크(rect x=60 y=40 w=80 h=90 rx=5) + 상단 타원(ellipse cx=100 cy=40 rx=40 ry=10)\n"
                    "탱크 내 수위: rect id='level' fill='#2196f3' — height를 JS로 배합합계% 비례 조정(max height=85)\n"
                    "낙하 물방울 3개: circle r=4 fill='#42a5f5'\n"
                    "@keyframes dropFall{0%{transform:translateY(0);opacity:1}100%{transform:translateY(60px);opacity:0}}\n"
                    "animation: dropFall 1s ease-in infinite, 각 0.33s delay stagger\n"
                    "MAX 수위선: line stroke='#ef5350' strokeDasharray='4 2'\n"
                    "이탈 시: 탱크 stroke #f44336 + 수위 fill #ef5350 + 텍스트 '배합비 조정 필요' @keyframes textBlink\n",
                "혼합 탱크 투입 (원료 낙하 애니메이션)":
                    "【원료 계량/혼합 탱크】\n"
                    "SVG 200×160: 원통형 탱크(rect x=60 y=40 w=80 h=90 rx=5) + 상단 타원(ellipse cx=100 cy=40 rx=40 ry=10)\n"
                    "탱크 내 수위: rect id='level' fill='#2196f3' — height를 JS로 배합합계% 비례 조정(max height=85)\n"
                    "낙하 물방울 3개: circle r=4 fill='#42a5f5'\n"
                    "@keyframes dropFall{0%{transform:translateY(0);opacity:1}100%{transform:translateY(60px);opacity:0}}\n"
                    "animation: dropFall 1s ease-in infinite, 각 0.33s delay stagger\n"
                    "이탈 시: 탱크 stroke #f44336 + 수위 fill #ef5350 + 텍스트 '배합비 조정 필요'\n",
                "용해·혼합 (탱크 내부 교반기 회전)":
                    "【교반기】\n"
                    "SVG 200×160: 원형 탱크(circle cx=100 cy=90 r=55 fill='#e3f2fd' stroke='#1565c0' strokeWidth=3)\n"
                    "임펠러 그룹 id='impeller': 날개 4개 — rect x=96 y=40 w=8 h=35 rx=3 fill='#1565c0'\n"
                    "(rotate 0/90/180/270deg, transform-origin='100px 90px' 각 날개에 적용)\n"
                    "@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}\n"
                    "#impeller{animation:spin 1.5s linear infinite; transform-origin:100px 90px}\n"
                    "Brix 이탈 시: animation-duration:0.4s / 배합오류 시: animation-play-state:paused + shake\n",
                "살균 (파이프 내 열수 흐름·온도 표시)":
                    "【살균 UHT】\n"
                    "SVG 200×160: S자형 파이프 <path id='heatPipe' d='M20,50 C60,50 60,90 100,90 C140,90 140,50 180,50' fill=none stroke='#ef5350' strokeWidth=12 strokeLinecap=round>\n"
                    "파티클 4개: <circle r='5' fill='white' opacity='0.8'>\n"
                    "<animateMotion dur='1.2s' repeatCount='indefinite' keyPoints='0;1' keyTimes='0;1'>\n"
                    "  <mpath href='#heatPipe'/>\n"
                    "</animateMotion> — 각 0.3s delay stagger\n"
                    "온도계: rect x=10 y=20 w=12 h=0→60(JS) fill='#ef5350', 수직 막대\n"
                    "pH/산도 이탈 시: heatPipe stroke #b71c1c + fill='rgba(244,67,54,0.1)' + '살균 조건 재검토'\n",
                "냉각 (냉각 코일 색상 변화·온도 하강)":
                    "【냉각 코일】\n"
                    "SVG 200×160: 지그재그 코일 <polyline id='coolCoil' points='20,40 60,40 60,70 100,70 100,40 140,40 140,70 180,70' fill=none stroke='#2196f3' strokeWidth=8 strokeLinecap=round>\n"
                    "냉각수 물방울 5개: circle r=3 fill='#90caf9'\n"
                    "@keyframes floatDown{0%{transform:translateY(0);opacity:0.8}100%{transform:translateY(25px);opacity:0}}\n"
                    "animation: floatDown 1.2s ease-in infinite, 각 0.24s stagger\n"
                    "온도 카운터: <text id='tempNum'>90</text> — JS setInterval 50ms마다 90→5 감소\n"
                    "Brix 초과 시: coolCoil stroke #ff9800 transition:stroke 0.5s\n",
                "충전 (노즐에서 액체 낙하·병 채워짐)":
                    "【충전기】\n"
                    "SVG 200×160: 노즐 <polygon points='85,10 115,10 108,35 92,35' fill='#546e7a'>\n"
                    "PET병: rect x=80 y=60 w=40 h=80 rx=4 fill=none stroke='#78909c' strokeWidth=2\n"
                    "병 목: rect x=88 y=40 w=24 h=22 fill=none stroke='#78909c'\n"
                    "병 내 액체: rect id='liquid' x=82 y=0 w=36 h=0 fill='#29b6f6' — y+h=140 고정, h만 증가\n"
                    "@keyframes fillUp{0%{height:0}100%{height:78px}}\n"
                    "#liquid{animation:fillUp 2s ease-in infinite; transform-origin:bottom}\n"
                    "노즐 방울: circle r=3 fill='#29b6f6'\n"
                    "@keyframes drip{0%{cy:36;opacity:1}100%{cy:62;opacity:0}}\n"
                    "animation: drip 0.6s ease-in infinite\n"
                    "원가 초과 시: liquid fill #ef5350 + 반투명 오버레이 div '💰 원가 초과'\n",
                "밀봉·캡핑 (캡 누름 동작)":
                    "【밀봉·캡핑】\n"
                    "SVG 200×160: 병(rect x=75 y=60 w=50 h=80 rx=4 stroke='#607d8b')\n"
                    "캡: rect id='cap' x=78 y=20 w=44 h=16 rx=3 fill='#455a64'\n"
                    "캡핑 암: line x1=100 y1=0 x2=100 y2=20 stroke='#37474f' strokeWidth=4\n"
                    "@keyframes capDown{0%{transform:translateY(-35px)}50%{transform:translateY(0)}80%{transform:translateY(0)}100%{transform:translateY(-35px)}}\n"
                    "#cap{animation:capDown 2.5s ease-in-out infinite}\n"
                    "기능성 미달 시: capDown 중단, @keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-4px)}75%{transform:translateX(4px)}} + '기능성 성분 부족'\n",
                "이화학·미생물 검사 (현미경·시험관 애니메이션)":
                    "【이화학·미생물 검사】\n"
                    "SVG 200×160: 시험관 3개 나란히\n"
                    "각 시험관: rect x=N y=30 w=28 h=90 rx=0 + <path d='M N,120 Q N+14,140 N+28,120' fill=액체색> (반원 바닥)\n"
                    "액체 rect id='tube1liquid' fill='#4caf50' transition:fill 1s — JS가 합격시 #4caf50, 불합격시 #f44336\n"
                    "@keyframes pulse{0%,100%{opacity:0.7}50%{opacity:1}}\n"
                    "각 액체 rect animation: pulse 1.5s ease-in-out infinite\n"
                    "이탈 시: 해당 시험관 fill #f44336 + SVG ❌ 텍스트(18px) + 이탈 항목명(12px)\n",
                "포장 (컨베이어 이동·박스 접힘)":
                    "【포장 컨베이어】\n"
                    "SVG 200×160: 벨트 상단 line y=100 x1=15 x2=185, 하단 line y=120 + 롤러 circle r=12 x=27,173 cy=110\n"
                    "벨트 패턴: stroke-dasharray='15 8'\n"
                    "@keyframes conveyorMove{from{stroke-dashoffset:0}to{stroke-dashoffset:-92}}\n"
                    "animation: conveyorMove 0.8s linear infinite\n"
                    "박스 3개: rect w=28 h=28 y=70 fill='#8d6e63'\n"
                    "@keyframes boxMove{0%{transform:translateX(-60px)}100%{transform:translateX(210px)}}\n"
                    "animation: boxMove 2s linear infinite, 각 0.67s stagger\n"
                    "리스크 미해결: animation-play-state:paused + circle r=18 fill='#f44336' cx=100 cy=110 텍스트 ⛔\n",
                "출하 (트럭 출발 애니메이션)":
                    "【출하 트럭】\n"
                    "SVG 200×160: cab rect x=100 y=70 w=55 h=50 rx=4 fill='#37474f'\n"
                    "trailer rect x=20 y=80 w=82 h=40 rx=3 fill='#546e7a'\n"
                    "창문 rect x=112 y=78 w=20 h=18 rx=2 fill='#b3e5fc'\n"
                    "바퀴 circle r=12 fill='#212121': cx=45,cy=124 / cx=135,cy=124\n"
                    "연기 circles: cx=155 cy=70, r=6→12 fade-out @keyframes smoke\n"
                    "모든 리스크 해소 시: @keyframes truckGo{0%{transform:translateX(0)}100%{transform:translateX(220px)}} 3s ease-in forwards\n"
                    "+ SVG 체크마크 path d='M30,80 L55,105 L100,55' stroke='#4caf50' strokeWidth=6 fill=none @keyframes checkFade{from{opacity:0}to{opacity:1}}\n"
                    "리스크 미해결: 트럭 고정(no transform) + circle cx=155 cy=80 r=10 fill='#f44336' @keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}} 0.8s infinite\n",
            }
            for step in twin_process:
                spec = _svg_spec.get(step, f"【{step.split('(')[0].strip()}】\n실제 SVG + CSS @keyframes로 설비 동작 완전 구현 (placeholder 금지)\n")
                _parts.append(spec + "\n")

        _parts.append(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "[JavaScript recalc() 핵심 구조]\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "function recalc() {\n"
            "  // 1. 슬라이더 비율 읽기 → 반응 컬럼 수치 계산 → DOM textContent + 셀 배경 갱신\n"
            "  // 2. 요약 카드 숫자 + progress bar width 갱신\n"
            "  // 3. SVG 게이지: el.style.strokeDashoffset = 283 * (1 - value/maxVal)\n"
            "  //    게이지 stroke 색상: 정상 #4caf50 / 주의 #ff9800 / 이탈 #f44336\n"
            "  // 4. 위험구간 체크 → 행 class 'row-error'/'row-ok' 토글\n"
            "  // 5. 공정 카드 class 'card-ok'/'card-warn'/'card-error' 토글\n"
            "  // 6. 리스크 신호등 + 컨베이어/트럭 animation-play-state 갱신\n"
            "}\n\n"
            "[디자인 토큰]\n"
            "배경:#f0f2f5 / 카드:#fff / 헤더:#1a237e / 대시보드배경:#1e2a3a\n"
            "정상:#4caf50 / 주의:#ff9800 / 위험:#f44336 / 슬라이더:#1565c0\n\n"
            "[출력 전 품질 검증 — 3회 실시]\n"
            "1차: 슬라이더 조정 → 반응 컬럼 수치+색상 + SVG 게이지 arc 정상 동작\n"
            "2차: 위험구간 이탈 → 행 강조 + 공정 카드 에러 + 신호등 연동\n"
            "3차: 모든 SVG 애니메이션 페이지 로드 시 자동 실행, placeholder 없음 확인\n"
            "검증 완료 후 '✅ 품질 검증 3회 완료' 표기 후 전체 HTML 출력.\n"
        )
        _TWIN_CUSTOM_SCRIPT = "".join(_parts)

        if st.button("📋 맞춤 스크립트 내보내기", key="twin_script_btn", use_container_width=True, type="primary"):
            st.session_state["twin_script_show"] = not st.session_state.get("twin_script_show", False)
        if st.session_state.get("twin_script_show"):
            st.code(_TWIN_CUSTOM_SCRIPT, language=None)

        # HTML 붙여넣기 → 앱 내 렌더링
        st.markdown("---")
        st.markdown("**🖥️ AI가 생성한 HTML 코드 붙여넣기 → 앱에서 바로 실행**")
        st.caption("제미나이가 출력한 전체 HTML 코드를 아래에 붙여넣으면 이 앱 안에서 바로 시뮬레이터를 실행합니다.")

        twin_html_input = st.text_area(
            "twin_html_lbl",
            placeholder="<!DOCTYPE html>\n<html>...</html>\n\nAI가 출력한 HTML 코드 전체를 여기에 붙여넣으세요.",
            key="twin_html_input",
            height=140,
            label_visibility="collapsed",
        )

        _tc1, _tc2, _tc3 = st.columns(3)
        with _tc1:
            if st.button("▶️ 시뮬레이터 실행", key="twin_render_btn",
                         use_container_width=True, type="primary",
                         disabled=not bool(twin_html_input)):
                st.session_state["twin_render_show"] = True
        with _tc2:
            if st.button("🔍 가상 시뮬레이터 예시보기", key="twin_example_btn", use_container_width=True):
                _show_twin_example_dialog()
        with _tc3:
            if twin_html_input:
                _bev_nm_dl = st.session_state.get("bev_prodname", "신제품")
                st.download_button(
                    "📥 HTML 파일 다운로드",
                    data=twin_html_input.encode("utf-8"),
                    file_name=f"twin_lab_{_bev_nm_dl}.html",
                    mime="text/html",
                    key="twin_html_dl",
                    use_container_width=True,
                )

        if st.session_state.get("twin_render_show") and twin_html_input:
            st.markdown("**⬇️ 트윈랩 시뮬레이터 (스크롤해서 사용)**")
            import streamlit.components.v1 as components
            components.html(twin_html_input, height=660, scrolling=True)

        st.markdown("---")
        st.markdown(
            "**💡 구글 드라이브 공유 방법**\n\n"
            "1. 위 📥 HTML 파일 다운로드 버튼으로 저장\n"
            "2. 구글 드라이브에 업로드 → 공유 링크 설정 (링크 있는 모든 사용자 뷰어)\n"
            "3. 아래 과제 제출란에 링크 붙여넣기"
        )

        st.markdown("**디지털 트윈랩 결과 메모**")
        st.caption("시뮬레이터로 확인한 이화학 지표 결과를 **3줄 이내**로 요약하세요.")
        st.text_area(
            "twin_result_lbl",
            placeholder="예) 배합비 슬라이더+공정 흐름도 HTML 생성 / 배합합계·Brix·원가 실시간 확인 / 리스크 검증 완료",
            key="twin_result", height=80, label_visibility="collapsed",
        )

        _twin_content = "\n".join([
            "[디지털 트윈랩 HTML 시뮬레이터]",
            f"구성 기능: {', '.join(twin_features)}",
            f"공정 흐름도: {'포함 (' + ' → '.join(twin_process[:3]) + '…)' if twin_process else '미포함'}",
            f"결과 메모: {st.session_state.get('twin_result', '')}",
        ])
        # 파일링크 필요: AI가 생성한 HTML 시뮬레이터 파일을 드라이브에 올려 링크로 제출
        # show_ai_field=False: HTML 코드 전체가 제출내용에 포함되므로 AI결과 별도 입력 불필요
        _hw_ui("디지털트윈랩", _twin_content, "twin_hw_submit", with_file=True, show_ai_field=False)

    # ── Tab 2: 가상 소비자 모델 제작 ─────────────────────
    with tab_consumer:
        show_step_guide(
            _S6_STEPS, 2,
            todo="가상 소비자 패널을 설계하고 관능조사 스크립트를 만듭니다.",
            uses="STEP 5 배합비와 제품명 (자동 연동)",
            produces="가상 소비자 패널 설계서와 관능조사 스크립트",
            minutes=12,
        )
        st.markdown("##### 👥 가상 소비자 모델 제작")
        st.caption("AI에게 제출할 가상 소비자 패널 설계와 관능조사 스크립트를 구성합니다.")

        st.markdown("**A. 패널 구성**")
        # 배합비 step1 제품명 직접입력 값으로 자동 동기화
        _auto_prodname = st.session_state.get("bev_prodname", "")
        if _auto_prodname:
            st.session_state["con_product"] = _auto_prodname
        cc1, cc2 = st.columns(2)
        with cc1:
            con_product = st.text_input(
                "조사 대상 제품명",
                placeholder="5단계 배합비 탭에서 제품명을 먼저 입력하세요",
                key="con_product",
            )
            if _auto_prodname:
                st.caption("📌 5단계 배합비 작성의 제품명에서 자동 불러왔습니다.")
            con_purpose = st.text_input("조사 목적", "신제품 출시 전 소비자 기호도 조사", key="con_purpose")
            con_count = st.slider("패널 인원수", 10, 100, 40, step=5, key="con_count")
        with cc2:
            con_age = st.multiselect("연령대", ["20대", "30대", "40대", "50대+"], ["20대", "30대"], key="con_age")
            con_gender = st.selectbox(
                "성별 구성", ["남녀 동수", "여성 비중 60%", "남성 비중 60%", "전체 여성"],
                key="con_gender",
            )
            con_occupation = st.multiselect(
                "직업군", ["직장인", "학생", "주부", "전문직"],
                ["직장인", "학생"], key="con_occupation",
            )
            con_region = st.selectbox("거주지역", ["수도권", "전국 분산", "대도시", "중소도시"], key="con_region")

        st.markdown("**B. 관능조사 설계**")
        cb1, cb2 = st.columns(2)
        with cb1:
            con_method = st.selectbox("관능조사 기법", [  # 간소화: 5개 -> 4개
                "기호도 검사 (Hedonic Scale)", "QDA 묘사분석법",
                "비교 검사법 (Paired Comparison)", "차이 검사법 (Triangle Test)",
            ], key="con_method")
            con_pass_score = st.slider("합격 기준 점수 (7점 만점)", 4.0, 7.0, 5.0, step=0.5, key="con_pass_score")
        with cb2:
            con_items = st.multiselect("관능조사 항목", [  # 간소화: 9개 -> 4개
                "향", "맛(단맛)", "맛(신맛)", "전반적 기호도",
            ], ["향", "맛(단맛)", "맛(신맛)", "전반적 기호도"], key="con_items")

        st.info(
            "**📌 배합비 유추 원리 안내**\n\n"
            "가상 소비자 모델은 AI가 배합비 원료(당류·산미료·기능성 성분 등)의 화학적 특성과 "
            "농도를 기반으로 소비자 반응을 유추합니다. 배합비 데이터가 구체적일수록 더 현실적인 "
            "시뮬레이션 결과를 얻을 수 있습니다."
        )

        _con_age_str = ", ".join(con_age) if con_age else "전 연령대"
        _con_occ_str = ", ".join(con_occupation) if con_occupation else "전 직업군"
        _con_items_str = ", ".join(con_items) if con_items else "전반적 기호도"
        _con_items_list = "\n".join(
            f"- {item}" for item in (con_items or ["전반적 기호도"])
        )

        _CON_SCRIPT = (
            "[가상 소비자 모델 제작 요청]\n\n"
            "소비자조사 전문리더의 경험과 역량을 갖춘 페르소나를 적용하여 "
            "아래 설정으로 가상 소비자 모델을 제작해주세요.\n\n"
            "[대상 제품명] 음료개발 연구원 페르소나가 개발한 제품명으로 진행해주세요\n"
            "[최종 배합비] 음료개발 연구원 페르소나가 개발한 최종 배합비로 진행해주세요\n\n"
            f"[조사 목적] {con_purpose}\n\n"
            "[패널 구성]\n"
            f"- 인원: {con_count}명\n"
            f"- 연령대: {_con_age_str}\n"
            f"- 성별: {con_gender}\n"
            f"- 직업군: {_con_occ_str}\n"
            f"- 거주지: {con_region}\n\n"
            f"[관능조사 기법] {con_method}\n"
            f"[평가 항목] {_con_items_str}\n"
            f"[합격 기준] {con_pass_score}점 이상 (7점 만점)\n\n"
            "[출력 형식]\n"
            f"1. 가상 소비자 패널 프로필 ({con_count}명의 연령·직업·맛 취향·구매 성향 묘사)\n"
            "2. 각 패널의 관능 평가 기준 (어떤 맛에 민감하고 어떤 특성을 중시하는지)\n"
            "3. 패널군 전체의 대표 맛 취향 프로파일 요약\n"
            "4. 아래 평가 항목별 판단 기준 및 척도 설명\n"
            + _con_items_list + "\n\n"
            "가상 소비자 모델 제작 과정과 패널 구성 근거를 상세히 설명해주세요."
        )

        if st.button("📋 가상 소비자 모델 스크립트 내보내기", key="con_script_btn", use_container_width=True):
            st.session_state["con_script_show"] = not st.session_state.get("con_script_show", False)
        if st.session_state.get("con_script_show"):
            st.code(_CON_SCRIPT + _SUBMIT_INSTRUCTION, language=None)

        st.markdown("**가상 소비자 모델 제작 결과**")
        st.caption("AI가 출력한 가상 소비자 모델 제작 내용을 아래에 붙여넣고 제출하세요.")

        _con_content = "\n".join([
            f"[가상 소비자 모델 — {con_product}]",
            f"패널: {con_count}명 / {_con_age_str} / {con_gender}",
            f"기법: {con_method}",
            f"항목: {_con_items_str}",
            f"합격기준: {con_pass_score}점",
        ])
        # 파일링크 불필요: 가상 소비자 모델 결과는 텍스트 제출로 충분
        _hw_ui("가상소비자모델", _con_content, "con_hw_submit", show_ai_field=True)

    # ── Tab 3: 관능검사 ────────────────────────────────────
    with tab_sensory:
        show_step_guide(
            _S6_STEPS, 3,
            todo="가상 관능검사를 실행하고 합격 기준 통과 여부를 확인합니다.",
            uses="앞 단계 패널 설계 + 배합비",
            produces="관능검사 결과와 합격 판정 — STEP 7 프로젝트 정리로 제출",
            minutes=15,
        )
        st.markdown("##### 🧪 관능검사 — 가상 소비자 맛 검증")

        _con_product_ref    = st.session_state.get("con_product", "")
        _con_count_ref      = st.session_state.get("con_count", 40)
        _con_items_ref      = st.session_state.get("con_items") or ["향", "맛(단맛)", "맛(신맛)", "전반적 기호도"]
        _con_method_ref     = st.session_state.get("con_method", "기호도 검사 (Hedonic Scale)")
        _con_pass_ref       = float(st.session_state.get("con_pass_score") or 5.0)

        if _con_product_ref:
            st.info(
                f"📌 **[가상 소비자 모델 탭]** 설정 기반 — "
                f"제품: **{_con_product_ref}** / 패널: **{_con_count_ref}명** / 기법: **{_con_method_ref}**"
            )
        else:
            st.warning("⚠️ '가상 소비자 모델 제작' 탭에서 먼저 패널 설정을 완료해주세요.")

        _items_numbered = "\n".join(
            f"{idx + 1}. {item}" for idx, item in enumerate(_con_items_ref)
        )
        _SEN_SCRIPT = (
            "[맛 엔진 학습 및 가상 관능검사 시뮬레이션]\n\n"
            "[대상 제품] 음료개발 연구원 페르소나가 개발한 제품명으로 진행해주세요\n"
            "[최종 배합비] 음료개발 연구원 페르소나가 개발한 최종 배합비로 진행해주세요\n\n"
            "[STEP 1 — 맛 엔진 학습]\n"
            "배합비에 포함된 각 원료별로 아래 항목을 식품 전문 지식과 결합하여 가상으로 분석해주세요:\n"
            "- 감미도: 단맛 강도 및 유형 (설탕 대비 상대값)\n"
            "- 산미도: 신맛 강도 및 유형 (구연산 대비 상대값)\n"
            "- 레올로지 특성: 점도, 텍스처, 마우스필 (입안에서의 물리적 느낌)\n"
            "- 입안의 맛 강도: 향미 발현 시점, 지속성, 후미 특성\n"
            "원료별 분석 결과를 표 형식으로 출력해주세요.\n\n"
            "[STEP 2 — 가상 소비자 관능검사]\n"
            "앞서 제작한 가상 소비자 패널을 불러와 위 배합비로 제조된 제품을 검증해주세요.\n\n"
            f"패널: {_con_count_ref}명\n"
            f"평가 방법: {_con_method_ref}\n"
            "평가 척도: 7점 만점 (1=매우 나쁨, 7=매우 좋음)\n"
            f"합격 기준: 전체 평균 {_con_pass_ref}점 이상\n\n"
            "[평가 항목]\n"
            + _items_numbered + "\n\n"
            "[출력 형식]\n"
            "1. STEP 1 맛 엔진 분석표 (원료별 감미도·산미도·레올로지·입안의 맛 강도)\n"
            "2. STEP 2 패널별 항목 점수표 (평균 점수 포함)\n"
            "3. 전체 맛 프로파일 요약 (첫 모금 향미 / 중반부 맛감 / 후미 인상)\n"
            "4. 대표 소비자 코멘트 (패널 반응 중 가장 대표적인 의견 2~3개)\n"
            "5. 최종 합격/불합격 판정 및 개선 제안 1~2가지\n\n"
            "(제품개발 배합비를 시장경쟁제품의 관능과 유사도를 검증후, 관능엔진을 적용하여 정교하게 평가해주세요)\n"
            "마지막에 과제 입력용 결과 요약표를 아래 형식으로 3줄로 출력해주세요.\n"
            "1줄: 제품명 / 전체 평균 점수 / 합격 여부\n"
            "2줄: 항목별 관능조사 점수 (예: 향 6.2 / 단맛 5.8 / 신맛 5.5 / 후미 6.0 / 전반적기호도 6.1)\n"
            "3줄: 시장경쟁제품 대비 관능 유사도 및 핵심 개선 제안"
        )

        if st.button("📋 관능검사 스크립트 내보내기", key="sen_script_btn", use_container_width=True):
            st.session_state["sen_script_show"] = not st.session_state.get("sen_script_show", False)
        if st.session_state.get("sen_script_show"):
            st.code(_SEN_SCRIPT + _SUBMIT_INSTRUCTION, language=None)

        st.markdown("**관능검사 결과 점수 입력** (AI에서 받은 항목별 평균 점수를 입력하세요)")
        sen_scores = {}
        _n_cols = min(len(_con_items_ref), 4)
        _score_cols = st.columns(_n_cols)
        for _idx, _item in enumerate(_con_items_ref):
            with _score_cols[_idx % _n_cols]:
                sen_scores[_item] = st.number_input(
                    _item, min_value=1.0, max_value=7.0,
                    value=5.0, step=0.1, key=f"sen_score_{_item}",
                )

        _avg_score = sum(sen_scores.values()) / len(sen_scores) if sen_scores else 0.0
        st.session_state["sen_avg_score"] = _avg_score
        _passed = _avg_score >= _con_pass_ref

        _sm1, _sm2 = st.columns([1, 2])
        with _sm1:
            st.metric(
                "전체 평균",
                f"{_avg_score:.1f}점",
                delta=f"✅ 합격 ({_con_pass_ref}점 기준)" if _passed else f"❌ 불합격 ({_con_pass_ref}점 기준)",
                delta_color="normal" if _passed else "inverse",
            )
        with _sm2:
            if st.button("🎯 최종 합격 여부 확인", key="sen_check_btn", use_container_width=True, type="primary"):
                if _passed:
                    st.success(
                        f"🎉 **합격!** 가상 소비자 평균 **{_avg_score:.1f}점** — "
                        f"합격 기준({_con_pass_ref}점) 달성!"
                    )
                    st.balloons()
                else:
                    st.warning(
                        f"💬 평균 {_avg_score:.1f}점 — 합격 기준({_con_pass_ref}점) 미달. "
                        "배합비 개선 후 재시도해보세요."
                    )

        st.markdown("**관능검사 결과 메모**")
        st.caption("결과를 **3줄 이내**로 요약하세요.")
        st.text_area(
            "sen_result_lbl",
            placeholder="예) 전체 평균 5.8점 / 전반적 기호도 6.2점 / 합격 — 향·후미 개선 권고",
            key="sen_result", height=80, label_visibility="collapsed",
        )

        _sen_scores_str = ", ".join(f"{k}:{v:.1f}" for k, v in sen_scores.items())
        _sen_content = "\n".join([
            f"[관능검사 — {_con_product_ref or '신제품'}]",
            f"항목별 점수: {_sen_scores_str}",
            f"전체 평균: {_avg_score:.1f}점",
            f"결과 메모: {st.session_state.get('sen_result', '')}",
        ])
        # 파일링크 불필요: 관능검사 결과는 텍스트 제출로 충분
        show_transfer_box(
            "s6",
            "내 제품을 가상 검증한다면 어떤 지표와 소비자 패널이 필요할까요?",
            "예: 재가열 후 식감·육즙감 평가, 30~40대 자녀가구 패널, 합격 기준 5.5점",
        )

        _hw_ui("관능검사", _sen_content, "sen_hw_submit")


# ----------------------------------------------------------
# 7. 프로젝트 정리
# ----------------------------------------------------------
elif section == "7️⃣ 프로젝트 정리":
    show_banner(
        "프로젝트 정리",
        "전 단계에서 학습한 내용을 단계별로 확인하고, AI 최종 요약 결과를 함께 제출합니다.",
        "7 / 7 · FINAL"
    )
    show_mission([
        "단계별 학습 결과를 확인하고 전체 흐름을 정리하세요",
        "제미나이에게 최종 요약 스크립트를 입력하고 결과를 복사하세요",
        "학습 내용 정리 + AI 요약 결과를 함께 과제로 제출하세요",
    ])

    # ── 1단계 페르소나 필드 복원 ───────────────────────────
    # r_theme_ml/m_theme_ml은 연구원·마케터 탭을 한 번도 열지 않으면 세션에 존재하지 않음 —
    # 각 탭의 기본 선택값(pills default)과 동일한 값으로 대체해야 rtk/mtk가 일치함
    _r_theme     = st.session_state.get("r_theme_ml") or "💪 기능성음료 개발연구원"
    _r_rtk       = _r_theme.replace(" ", "_").replace("·", "").replace(".", "")
    _r_name      = st.session_state.get(f"r_name_{_r_rtk}", "")
    _r_career    = st.session_state.get(f"r_career_{_r_rtk}", "")
    _r_job_disp  = (st.session_state.get("r_theme_manual", "").strip()
                    or (_r_theme.split(" ", 1)[-1] if " " in _r_theme else _r_theme))

    _m_theme     = st.session_state.get("m_theme_ml") or "🧃 음료 브랜드마케터"
    _m_mtk       = _m_theme.replace(" ", "_").replace("·", "").replace(".", "")
    _m_name      = st.session_state.get(f"m_name_{_m_mtk}", "")
    _m_career    = st.session_state.get(f"m_career_{_m_mtk}", "")
    _m_job_disp  = (st.session_state.get("m_theme_manual", "").strip()
                    or (_m_theme.split(" ", 1)[-1] if " " in _m_theme else _m_theme))

    # ── 2단계 데이터 필드 복원 ─────────────────────────────
    _ml_cat   = st.session_state.get("ml_cat_manual", "") or st.session_state.get("ml_cat", "")
    _ml_theme = st.session_state.get("ml_theme_manual", "") or st.session_state.get("ml_theme", "")

    # ── 3~5단계 결과 복원 ──────────────────────────────────
    _r_online = st.session_state.get("online_user_script", "")
    _r_food   = st.session_state.get("food_user_script", "")
    _r_learn  = st.session_state.get("learn_user_script", "")
    _r_report = st.session_state.get("report_user_script", "")
    _r_bev    = st.session_state.get("bev_preview", "")
    _r_bev_nm = st.session_state.get("bev_prodname", "")
    _r_proc1  = st.session_state.get("proc_step1", "")
    _r_proc2  = st.session_state.get("proc_step2", "")
    _r_proc3  = st.session_state.get("proc_step3", "")
    _r_twin   = st.session_state.get("twin_result", "")
    _r_con    = st.session_state.get("con_hw_submit_ai", "")
    _r_sen    = st.session_state.get("sen_result", "")
    _r_mv_note  = st.session_state.get("mv_note", "")
    _r_ms2_scn  = st.session_state.get("ms2_scenario", "") or "미선택"
    _r_ms2_script = st.session_state.get("ms2_script", "")

    def _na(v, limit=300):
        if not v:
            return "(아직 입력하지 않았습니다)"
        return (v[:limit] + "…") if len(v) > limit else v

    st.markdown("#### 📋 단계별 학습 결과 정리")

    with st.expander("👤 STEP 2 — 제품개발 페르소나", expanded=False):
        st.markdown("**연구원 페르소나**")
        if _r_job_disp or _r_name:
            st.text(f"직무: {_r_job_disp}  /  이름: {_r_name}  /  경력: {_r_career}")
        else:
            st.text("(아직 입력하지 않았습니다)")
        st.markdown("**마케터 페르소나**")
        if _m_job_disp or _m_name:
            st.text(f"직무: {_m_job_disp}  /  이름: {_m_name}  /  경력: {_m_career}")
        else:
            st.text("(아직 입력하지 않았습니다)")
        _r_hw_ok = "✅ 제출 완료" if st.session_state.get("r_hw_submit_done") else "⬜ 미제출"
        _m_hw_ok = "✅ 제출 완료" if st.session_state.get("m_hw_submit_done") else "⬜ 미제출"
        st.caption(f"연구원 과제 {_r_hw_ok}  |  마케터 과제 {_m_hw_ok}")

    with st.expander("📂 STEP 3 — 제품개발용 데이터", expanded=False):
        st.markdown("**제품 카테고리**")
        st.text(_ml_cat or "(아직 입력하지 않았습니다)")
        st.markdown("**데이터 유형**")
        st.text(_ml_theme or "(아직 입력하지 않았습니다)")
        _col_ok = "✅ 제출 완료" if st.session_state.get("collect_hw_submit_done") else "⬜ 미제출"
        _trn_ok = "✅ 제출 완료" if st.session_state.get("train_hw_submit_done") else "⬜ 미제출"
        st.caption(f"데이터 수집 과제 {_col_ok}  |  데이터 학습 과제 {_trn_ok}")

    with st.expander("📊 STEP 4 — 시장분석 및 학습", expanded=False):
        st.markdown("**온라인 시장분석**")
        st.text(_na(_r_online))
        st.markdown("**식품전문정보 분석**")
        st.text(_na(_r_food))
        st.markdown("**시장조사 학습**")
        st.text(_na(_r_learn))
        st.markdown("**보고서 작성**")
        st.text(_na(_r_report))

    with st.expander("⚗️ STEP 5 — 배합비 개발 결과", expanded=False):
        st.markdown(f"**제품명**: {_r_bev_nm or '(미입력)'}")
        st.markdown("**배합비 스크립트**")
        st.text(_na(_r_bev))
        st.markdown("**STEP 1 시니어 연구원 훈련 결과**")
        st.text(_r_proc1 or "(아직 입력하지 않았습니다)")
        st.markdown("**STEP 2 시니어 연구원 코칭 결과**")
        st.text(_r_proc2 or "(아직 입력하지 않았습니다)")
        st.markdown("**STEP 3 마케팅 분석 & 최종안 결과**")
        st.text(_r_proc3 or "(아직 입력하지 않았습니다)")
        st.markdown("**미션1 무결성 검증**")
        st.text(
            f"{_r_mv_note or '미입력'}"
        )
        st.markdown("**미션2 시나리오 대응**")
        st.text(f"선택 시나리오: {_r_ms2_scn}")
        st.text(_na(_r_ms2_script))

    with st.expander("🔬 STEP 6 — 가상모델 개발 결과", expanded=False):
        st.markdown("**디지털 트윈랩 결과**")
        st.text(_r_twin or "(아직 입력하지 않았습니다)")
        st.markdown("**가상 소비자 모델 결과**")
        st.text(_r_con or "(아직 입력하지 않았습니다)")
        st.markdown("**관능검사 결과**")
        st.text(_r_sen or "(아직 입력하지 않았습니다)")

    # 고정 제미나이 요약 스크립트
    st.markdown("---")
    with st.expander("🎯 내 제품 적용 정리 — STEP별 '내 제품으로 옮기기' 메모", expanded=True):
        st.caption(
            "실습은 전원 공통 음료 사례로 진행했고, 아래는 각 STEP에서 본인 제품 기준으로 옮겨 적은 내용입니다. "
            "비어 있는 항목은 해당 STEP으로 돌아가 채울 수 있습니다."
        )
        for _tk, _tlabel in _TRANSFER_STEPS:
            st.markdown(f"**{_tlabel}**")
            st.text(st.session_state.get(f"transfer_{_tk}") or "(아직 입력하지 않았습니다)")

    st.markdown("#### 🤖 제미나이 최종 요약 스크립트")
    st.caption("아래 스크립트를 제미나이에 입력하면 오늘 나눈 대화 맥락 전체를 요약해줍니다.")
    _SUMMARY_SCRIPT = (
        "[오늘 진행한 음료 신제품 개발 대화 전체 요약 요청]\n\n"
        "오늘 우리가 나눈 대화 맥락과 스크립트를 아래 항목별로 정리해주세요.\n\n"
        "1. 오늘 대화에서 생성·적용한 페르소나 요약 (연구원·마케터 각 핵심 특성)\n"
        "2. 제품 개발 전 과정 (콘셉트→배합비→검증→소비자 조사) 대화 맥락 핵심 내용\n"
        "3. 가상 소비자 모델 제작 및 관능검사 대화에서 나온 주요 결과\n"
        "4. 오늘 대화에서 생성된 최종 배합비 전체 내용 (원료명·비율·배합 총량 포함)\n"
        "5. 개발한 배합비에 대한 추가 개선 방향 및 다음 실험 단계 제안\n"
        "6. 오늘 대화를 통해 완성된 제품 개요 최종 요약 (제품명·콘셉트·배합비 핵심·소비자 반응 포함)\n\n"
        "결과는 항목별 번호를 유지하되, 핵심만 간결하게 작성해주세요."
    )
    st.code(_SUMMARY_SCRIPT, language=None)

    # 최종 과제 제출 (두 파트)
    st.markdown("---")
    st.markdown("#### 📤 최종 과제 제출")

    def _trunc(v, n=200):
        return (v[:n] + "…") if len(v) > n else (v or "미입력")

    _recap_content = "\n\n".join([
        "=== 단계별 학습 결과 정리 ===",
        (
            "[STEP 2 제품개발 페르소나]\n"
            f"연구원: {_r_job_disp} / {_r_name} / {_r_career}\n"
            f"마케터: {_m_job_disp} / {_m_name} / {_m_career}"
        ),
        (
            "[STEP 3 제품개발용 데이터]\n"
            f"카테고리: {_ml_cat or '미입력'}\n"
            f"데이터 유형: {_ml_theme or '미입력'}"
        ),
        (
            "[STEP 4 시장분석]\n"
            f"온라인: {_trunc(_r_online)}\n"
            f"식품정보: {_trunc(_r_food)}\n"
            f"시장조사학습: {_trunc(_r_learn)}\n"
            f"보고서작성: {_trunc(_r_report)}"
        ),
        (
            "[STEP 5 배합비 개발]\n"
            f"제품명: {_r_bev_nm or '미입력'}\n"
            f"배합비: {_trunc(_r_bev)}\n"
            f"STEP1: {_r_proc1 or '미입력'}\n"
            f"STEP2: {_r_proc2 or '미입력'}\n"
            f"STEP3: {_r_proc3 or '미입력'}\n"
            f"미션1(무결성검증): {_r_mv_note or '미입력'}\n"
            f"미션2(시나리오대응): {_r_ms2_scn} — {_trunc(_r_ms2_script)}"
        ),
        (
            "[STEP 6 가상모델 개발]\n"
            f"트윈랩: {_r_twin or '미입력'}\n"
            f"소비자모델: {_r_con or '미입력'}\n"
            f"관능검사: {_r_sen or '미입력'}"
        ),
        (
            "[내 제품 적용 정리 — 공통 음료 사례를 본인 제품으로 옮긴 내용]\n"
            + "\n".join(
                f"{_tlabel}: {st.session_state.get('transfer_' + _tk) or '미입력'}"
                for _tk, _tlabel in _TRANSFER_STEPS
            )
        ),
    ])

    st.markdown("**1️⃣ 학습 내용 정리 (자동 생성 — 수정 가능)**")
    p7_recap_edit = st.text_area(
        "학습내용",
        value=_recap_content,
        key="p7_recap_edit",
        height=220,
        label_visibility="collapsed",
    )

    st.markdown("**2️⃣ AI 최종 요약 결과 붙여넣기**")
    p7_ai_summary = st.text_area(
        "AI요약결과",
        placeholder="위 제미나이 스크립트를 실행한 후 AI의 요약 결과를 여기에 붙여넣으세요.",
        key="p7_ai_summary",
        height=220,
        label_visibility="collapsed",
    )

    _p7_final_content = "\n\n---\n\n".join([
        p7_recap_edit or _recap_content,
        "[AI 최종 요약 결과]\n" + (p7_ai_summary if p7_ai_summary else "(미입력)"),
    ])

    # 파일링크 필요: 최종 결과물을 문서/PDF로 정리해 드라이브 링크로 제출
    # show_ai_field=False: 최종 정리 내용이 제출내용에 포함되므로 AI결과 별도 입력 불필요
    _hw_ui("프로젝트정리", _p7_final_content, "p7_hw_submit", with_file=True, show_ai_field=False)


# ----------------------------------------------------------
# 🔐 관리자 현황판
# ----------------------------------------------------------
elif section == "🔐 관리자 현황판":
    if not st.session_state.get("_admin_verified"):
        st.markdown("""
        <div style="max-width:400px;margin:80px auto 0 auto;background:#fff;
        border:1.5px solid #e2e8f0;border-radius:16px;padding:36px 32px;
        box-shadow:0 4px 20px rgba(0,0,0,0.08);text-align:center;">
        <div style="font-size:36px;margin-bottom:12px;">🔐</div>
        <div style="font-size:18px;font-weight:800;color:#0f172a;margin-bottom:4px;">관리자 전용</div>
        <div style="font-size:13px;color:#64748b;">관리자 코드를 입력하세요</div>
        </div>
        """, unsafe_allow_html=True)
        _lc2, _cc2, _rc2 = st.columns([1, 1.2, 1])
        with _cc2:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            _adm_pw2 = st.text_input("관리자 코드", type="password", key="_adm_pw_main",
                                     label_visibility="collapsed", placeholder="관리자 코드 입력")
            if st.button("입장", key="_adm_enter_main", use_container_width=True, type="primary"):
                if _ADMIN_CODE and _adm_pw2 == _ADMIN_CODE:
                    st.session_state["_admin_verified"] = True
                    st.rerun()
                else:
                    st.error("코드가 올바르지 않습니다.")
    else:
        show_banner("관리자 현황판", "전체 접속자 · 과제별 제출 현황 · 진행률", "🔐")

        if st.button("🔄 새로고침", key="_dash_refresh", type="secondary"):
            _fetch_dashboard_data.clear()
            st.rerun()

        try:
            _acc_data, _sum_data = _fetch_dashboard_data()  # API 2회 + 2분 캐시

            # 접속자 목록
            _acc_names = [r[0] for r in _acc_data[1:] if r and r[0].strip()]
            _total_acc = len(_acc_names)

            # 제출현황 파싱 (헤더 제외, 빈 행·합계 행 제외)
            _tab_data = []
            _total_sub = 0
            for _row in _sum_data[1:]:
                if not _row or not _row[0].strip() or _row[0] in ("", "전체 합계"):
                    continue
                _lbl      = _row[0]                          # A: 섹션·탭
                _sub_cnt  = int(_row[2]) if len(_row) > 2 and str(_row[2]).isdigit() else 0
                # D열(index 3)~ 제출자 이름 (순서 유지)
                _sub_names = [c for c in _row[3:] if c.strip()]
                # 순번 접두어 제거 ("1. 희동이" → "희동이")
                _plain = [n.split(". ", 1)[-1] if ". " in n else n for n in _sub_names]
                _missing  = [n for n in _acc_names if n not in _plain]
                _total_sub += _sub_cnt
                _tab_data.append((_lbl, _sub_names, _missing, _sub_cnt))

            _total_possible = _total_acc * len(_tab_data)
            _overall_pct = min(100, int(_total_sub / _total_possible * 100)) if _total_possible > 0 else 0

            _m1, _m2, _m3 = st.columns(3)
            _m1.metric("전체 접속 인원", f"{_total_acc}명")
            _m2.metric("전체 진행률", f"{_overall_pct}%")
            _m3.metric("총 제출 건수", f"{_total_sub}건")

            st.markdown("---")

            # 접속자 목록
            with st.expander(f"👥 접속자 명단 ({_total_acc}명)", expanded=False):
                if _acc_names:
                    _acc_cols = st.columns(4)
                    for _i, _nm in enumerate(_acc_names):
                        _acc_cols[_i % 4].markdown(f"`{_i+1}. {_nm}`")
                else:
                    st.caption("아직 접속자가 없습니다.")

            st.markdown("---")
            st.markdown("### 📋 과제별 제출 현황")

            for _lbl, _sub_names, _missing, _sub_cnt in _tab_data:
                _pct = min(100, int(_sub_cnt / _total_acc * 100) if _total_acc > 0 else 0)
                _bar_w = _pct

                # 진행률 바 색상
                _bar_color = "#22c55e" if _pct >= 100 else "#3b82f6" if _pct >= 50 else "#f59e0b"
                _ordered_str = "&nbsp;›&nbsp;".join(
                    f"<span style='background:#dbeafe;padding:2px 9px;border-radius:5px;"
                    f"font-size:15px;font-weight:600;'>{n}</span>"
                    for n in _sub_names
                ) if _sub_names else "<span style='color:#94a3b8;'>없음</span>"
                _missing_html = (
                    f"<div style='font-size:15px;color:#ef4444;margin-top:8px;'>"
                    f"<b>미제출:</b> {', '.join(_missing)}</div>"
                ) if _missing else ""
                st.markdown(f"""
<div style="background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:14px;
padding:18px 22px;margin-bottom:14px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
  <span style="font-size:17px;font-weight:800;color:#1e293b;">{_lbl}</span>
  <span style="font-size:16px;font-weight:700;color:{_bar_color};">{_sub_cnt}/{_total_acc}명 &nbsp;({_pct}%)</span>
</div>
<div style="background:#e2e8f0;border-radius:99px;height:8px;margin-bottom:12px;">
  <div style="background:{_bar_color};width:{_bar_w}%;height:8px;border-radius:99px;"></div>
</div>
<div style="font-size:15px;color:#334155;line-height:2.0;">
  <b>제출순서:</b>&nbsp; {_ordered_str}
</div>
{_missing_html}
</div>""", unsafe_allow_html=True)

        except Exception as _de:
            st.error(f"현황 조회 오류: {_de}")

        # ── 실습자 접속 주소 ────────────────────────────────
        st.markdown("---")
        with st.expander("📡 실습자 접속 주소 보기", expanded=False):
            _ai = _class_access_info()
            if not _ai["ips"]:
                st.error(
                    "이 PC의 네트워크 주소를 찾지 못했습니다. "
                    "유선랜이 연결돼 있는지 확인하세요."
                )
            for _ip in _ai["ips"]:
                st.markdown("**%s**" % _ip)
                st.caption("실습자용 — 로그인 없이 크롤링 실습 화면만 열립니다")
                st.code("http://%s:%d/?m=crawl" % (_ip, _ai["port"]), language=None)
                st.caption("강사용 — 로그인 후 전체 화면")
                st.code("http://%s:%d" % (_ip, _ai["port"]), language=None)

            st.markdown("---")
            _fw = _ai["firewall"]
            if _fw is True:
                st.success("✅ 방화벽 8501 포트가 열려 있습니다.")
            elif _fw is False:
                st.warning(
                    "⚠️ 방화벽 규칙이 없습니다. 실습자가 접속되지 않으면 "
                    "`setup_teacher_pc.bat` 을 **관리자 권한으로 실행**하세요."
                )
            else:
                st.caption("방화벽 상태는 확인하지 못했습니다.")

            st.caption(
                "현재 서비스 포트 **%d** · 실습자는 강사 PC와 같은 네트워크에 있어야 합니다."
                % _ai["port"]
            )

        # ── 강사PC 설치 패키지 ──────────────────────────────
        st.markdown("---")
        with st.expander("🖥️ 강사PC 설치 패키지 내려받기", expanded=False):
            st.caption(
                "학원 공용PC에서 크롤링을 직접 시연할 때만 필요합니다. "
                "실습자는 이 웹앱 주소로 들어오므로 설치하지 않습니다."
            )
            _pkg_c1, _pkg_c2 = st.columns(2)
            with _pkg_c1:
                _inc_codes = st.checkbox("접속코드·관리자코드 포함",
                                         value=True, key="_pkg_codes")
            with _pkg_c2:
                _inc_api = st.checkbox("AI 기능 키까지 포함",
                                       value=False, key="_pkg_api")
            if _inc_api:
                st.warning(
                    "공용PC에 API 키 파일이 남습니다. "
                    "크롤링 시연만 한다면 키 없이도 동작하니 빼는 편이 안전합니다."
                )
            try:
                _pkg_bytes = _build_teacher_package(_inc_codes, _inc_api)
                st.download_button(
                    "📦 설치 패키지 내려받기 (ZIP)",
                    data=_pkg_bytes,
                    file_name="AINPD_강사PC.zip",
                    mime="application/zip",
                    use_container_width=True,
                    key="_pkg_dl",
                )
                st.caption("압축 크기 약 %d KB" % (len(_pkg_bytes) // 1024))
            except Exception as _pe:
                st.error("패키지 생성 실패: %s" % str(_pe)[:200])

            st.markdown(
                "**설치 순서** — ① ZIP을 풀기 → "
                "② `setup_teacher_pc.bat` 더블클릭 (최초 1회, 5~10분) → "
                "③ 수업 때 `run_class.bat` 실행\n\n"
                "**수업이 끝나면 `삭제하기.bat`** 을 더블클릭하면 통째로 지워집니다."
            )

        # ── 설치본에서만 보이는 삭제 버튼 ──────────────────
        import os as _os5
        _app_dir = _os5.path.dirname(_os5.path.abspath(__file__))
        if _os5.path.isfile(_os5.path.join(_app_dir, ".installed_package")):
            with st.expander("🧹 이 설치본 완전 삭제", expanded=False):
                st.warning(
                    "**이 PC에 설치된 교육앱 폴더를 통째로 지웁니다.** "
                    "접속코드가 담긴 파일까지 함께 지워집니다. 되돌릴 수 없습니다."
                )
                st.caption(
                    "지워지는 곳 — `%s`\n\n"
                    "누르면 앱이 꺼지므로 이 화면은 연결이 끊깁니다. 정상입니다. "
                    "내려받은 크롤링용 브라우저는 남습니다(다음 수업 설치 시간이 줄어듭니다)."
                    % _app_dir
                )
                _sure = st.checkbox("지워도 됩니다. 확인했습니다.", key="_purge_sure")
                if st.button("🧹 지금 삭제하기", key="_purge_btn",
                             type="primary", disabled=not _sure,
                             use_container_width=True):
                    import subprocess as _sp5
                    _bat = _os5.path.join(_app_dir, "삭제하기.bat")
                    if not _os5.path.isfile(_bat):
                        st.error("삭제하기.bat 을 찾을 수 없습니다. 폴더를 직접 삭제해 주세요.")
                    else:
                        try:
                            # 앱 자신을 종료시키므로 결과를 기다리지 않는다
                            _sp5.Popen(["cmd", "/c", "start", "", _bat, "/y"],
                                       cwd=_os5.environ.get("TEMP", _app_dir),
                                       shell=False)
                            st.success(
                                "삭제를 시작했습니다. 잠시 후 앱이 꺼지고 폴더가 사라집니다. "
                                "이 창은 닫으셔도 됩니다."
                            )
                        except Exception as _xe:
                            st.error("삭제 실행 실패: %s" % str(_xe)[:200])
