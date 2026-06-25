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


def run_claude(prompt: str, system: str = "") -> str:
    """Claude API 호출 - 스트리밍"""
    client = get_client()
    if not client:
        return "⚠️ API 키가 설정되지 않았습니다. secrets.toml 또는 환경변수에 ANTHROPIC_API_KEY를 추가해 주세요."
    try:
        with st.spinner("🤖 Claude가 분석 중입니다..."):
            messages = [{"role": "user", "content": prompt}]
            kwargs = {"model": "claude-sonnet-4-6", "max_tokens": 2000, "messages": messages}
            if system:
                kwargs["system"] = system
            response = client.messages.create(**kwargs)
            return response.content[0].text
    except Exception as e:
        return f"❌ 오류가 발생했습니다: {str(e)}"


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
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]), scopes=scopes
    )
    return gspread.authorize(creds)


_HW_HEADERS = ["제출시간", "학생이름", "작성 스크립트", "AI 생성결과", "파일링크"]


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

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_row = [timestamp, student, content, ai_result, file_link]

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
            ws.update(f"A{existing_idx}:E{existing_idx}", [new_row])
        else:
            ws.append_row(new_row)

        return True, ""
    except Exception as e:
        return False, str(e)


def _hw_ui(sheet_tab: str, content: str, btn_key: str,
           with_file: bool = False, show_ai_field: bool = True):
    """과제 제출 UI — 각 세션 하단에 공통으로 삽입"""
    st.markdown("---")
    student = st.session_state.get("student_name", "")
    if not student:
        st.warning("과제를 제출하려면 먼저 로그인하세요.")
        return
    st.markdown("##### 📤 과제 제출")
    st.caption("동일인이 재제출하면 최종 내용으로 덮어씁니다.")

    ai_result = ""
    if show_ai_field:
        st.markdown(
            '<div style="background:#f0fdf4;border:1.5px solid #86efac;border-radius:6px;'
            'padding:4px 10px 2px 10px;margin-top:4px;">'
            '<span style="font-size:11px;color:#166534;font-weight:600;">📎 AI 생성결과 붙여넣기</span></div>',
            unsafe_allow_html=True,
        )
        ai_result = st.text_area(
            "AI 생성결과", key=f"{btn_key}_ai",
            placeholder="AI 대화창의 결과를 여기에 붙여넣으세요 (선택)",
            height=120, label_visibility="collapsed",
        )

    file_link = ""
    if with_file:
        file_link = st.text_input(
            "파일 링크 (구글드라이브 공유 링크, 선택)",
            placeholder="https://drive.google.com/...",
            key=f"{btn_key}_file",
        )
        if st.button("🔗 공유 설정 방법 보기", key=f"{btn_key}_guide_btn",
                     use_container_width=False):
            st.session_state[f"{btn_key}_show_guide"] = not st.session_state.get(
                f"{btn_key}_show_guide", False)
        if st.session_state.get(f"{btn_key}_show_guide"):
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


def show_example(text: str):
    st.markdown(f'<div class="example-box">{text}</div>', unsafe_allow_html=True)


def show_result(text: str):
    st.markdown(f'<div class="result-box">{text}</div>', unsafe_allow_html=True)


def render_ai_result(prompt: str, key: str):
    """AI 실행 버튼 + 결과 출력"""
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI 실행")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("▶ Claude에게 분석 요청하기", key=f"run_{key}"):
            result = run_claude(prompt)
            st.session_state[f"result_{key}"] = result

    with col2:
        if st.button("📋 프롬프트 복사용 보기", key=f"copy_{key}"):
            st.session_state[f"show_prompt_{key}"] = not st.session_state.get(f"show_prompt_{key}", False)

    if st.session_state.get(f"show_prompt_{key}"):
        st.text_area("복사해서 ChatGPT, Gemini 등에 붙여넣기", value=prompt.strip(), height=300, key=f"ta_{key}")

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 스크립트 작성 코치", key=f"coach_{key}"):
            s, t = score_persona(fields, defaults)
            st.session_state[f"coach_score_{key}"] = s
            st.session_state[f"coach_tips_{key}"] = t
    with col2:
        if st.button("📋 이를 적용하기", key=f"apply_{key}"):
            st.session_state[f"show_prompt_{key}"] = not st.session_state.get(f"show_prompt_{key}", False)

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

    # 프롬프트 복사용 출력
    if st.session_state.get(f"show_prompt_{key}"):
        st.markdown("**아래 전체를 복사 → ChatGPT / Gemini 등 AI 대화창에 붙여넣기**")
        st.code(prompt.strip(), language=None)


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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 스크립트 작성 코치", key=f"coach_{key}"):
            s, t = score_data_script(fields, defaults)
            st.session_state[f"coach_score_{key}"] = s
            st.session_state[f"coach_tips_{key}"] = t
    with col2:
        if st.button("📋 이를 적용하기", key=f"apply_{key}"):
            st.session_state[f"show_prompt_{key}"] = not st.session_state.get(f"show_prompt_{key}", False)

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

    if st.session_state.get(f"show_prompt_{key}"):
        st.markdown("**아래 전체를 복사 → ChatGPT 대화창에 붙여넣기**")
        st.code(prompt.strip(), language=None)


# =========================================================
# 5. 로그인 게이트
# =========================================================

try:
    _ACCESS_CODE = st.secrets["ACCESS_CODE"]
except Exception:
    _ACCESS_CODE = "kfi2026"  # 로컬 실행 기본값

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
                st.rerun()
    st.stop()


# =========================================================
# 6. 사이드바
# =========================================================

with st.sidebar:
    st.markdown("## 🧪 AI 제품개발 실습")
    st.markdown("---")
    _sname = st.session_state.get("student_name", "")
    if _sname:
        st.markdown(f"👤 **{_sname}**")
        st.markdown("---")
    section = st.radio(
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
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("한국식품정보원 AI 제품개발 교육")
    st.caption("© 2026 KFI")
    st.markdown("---")
    if st.button("로그아웃", key="_logout_btn", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["student_name"] = ""
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
        ("11:00–12:00", "실무 AI 활용 실습 1", "페르소나 정의 · 스크립트 작성 · 대화실습", "PPT/노트북"),
        ("13:00–14:00", "제품개발용 데이터", "빅데이터 · API 활용 · 사례 발표", "PPT/노트북"),
        ("14:00–15:00", "실무 AI 활용 실습 2", "배합비 개발 프로그램 작성", "PPT/노트북"),
        ("15:00–16:00", "실무 AI 활용 실습 3", "가상 소비자 조사 · 페르소나 · 조사표 출력", "PPT/노트북"),
        ("16:00–17:00", "프로젝트 정리 및 발표", "스크립트 디자인 · AI 모델 실습 · 개별 발표", "PPT/노트북"),
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
<li>아래 <b>예시 자료 다운로드</b> 후 프로젝트 소스에 파일 등록<br>
<span style="font-size:11px;color:#0284c7;">⚠️ OpenAI 프로젝트 소스는 최대 5개 파일</span></li>
<li>교육 중 연구원 페르소나 스크립트 완성 후 <b>추가 등록</b></li>
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
<li>아래 예시 자료를 <b>소스 파일로 첨부</b> 후 저장</li>
</ol>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 예시 자료 다운로드")
    st.caption("클릭하면 Google Drive에서 열립니다. 우측 상단 ⬇ 아이콘으로 다운로드하세요.")

    DL_RESOURCES = {
        "🎓 개발 이론": [
            ("신제품 개발이론 A", "1HGK3QfvHrL2uwuOQySe1Dz0oFr654U0G", False),
            ("신제품 개발이론 B", "11ISqRcU6ECmDc8SJwi2uBWBlzn4jZkK1", False),
            ("신제품 아이디어 도출", "1QHDKDku07lvw7p3AT2kqoLgY7WSHdSC6", False),
        ],
        "🥤 음료 데이터·기술": [
            ("(1) 음료시장 세분화 데이터", "1fYqetwVjSDPgpACUSoPPpMgCPefviO8Q", True),
            ("(3) 음료 제조기술과 이론", "1ajAKtax9FiyiRi0zE26EdQszdhY6nMYn", True),
            ("(4) 신제품 관능평가 방법", "1H1f0Kfdg19VrOuNNfYuCrRs0DZyQvVqA", True),
            ("당류 저감화 기술가이드 (저당원료)", "1hmiLf83YCXDF90zizj6VicMT_IgHdGmw", False),
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
    st.markdown("### 📤 구글 시트 공유 링크 만들기")
    st.caption("제미나이에서 생성한 배합비·결과표를 구글 시트로 내보낸 뒤, 과제 제출용 공유 링크를 만드는 방법입니다.")
    _show_share_guide()


# ----------------------------------------------------------
# 1. 신제품 개발 프로세스
# ----------------------------------------------------------
elif section == "1️⃣ 신제품 개발 프로세스":
    show_banner(
        "신제품 개발 프로세스",
        "AI를 활용한 음료 신제품 개발 교육의 전체 흐름을 단계별로 확인하세요.",
        "1 / 6"
    )

    st.markdown("#### 📊 교육 진행 흐름도")
    st.caption("아래 7단계는 이 교육 전체의 학습 순서입니다. 각 단계를 클릭해 해당 섹션으로 이동하세요.")

    def _card(num, title, items):
        items_html = "<br>".join(items)
        return f"""<div style="background:#ffffff;border:2px solid #334155;border-radius:10px;
padding:20px 22px;height:100%;box-sizing:border-box;">
<div style="background:#1e293b;color:#ffffff;border-radius:20px;padding:4px 14px;
font-size:13px;font-weight:800;display:inline-block;margin-bottom:12px;">STEP {num}</div>
<div style="font-size:16px;font-weight:700;color:#0f172a;line-height:1.6;margin-bottom:10px;">{title}</div>
<div style="font-size:14px;color:#475569;line-height:2.1;">{items_html}</div>
</div>"""

    _ARR = """<div style="display:flex;align-items:center;justify-content:center;height:100%;padding-top:34px;">
<div style="width:22px;height:3px;background:#475569;"></div>
<div style="width:0;height:0;border-top:8px solid transparent;border-bottom:8px solid transparent;border-left:13px solid #475569;"></div>
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

    # ── 행 연결 화살표 (STEP 4 아래 → STEP 5 위) ──
    _, _, _, _, _, _, turn_col = st.columns([4, 0.7, 4, 0.7, 4, 0.7, 4])
    with turn_col:
        st.markdown("""<div style="display:flex;justify-content:center;padding:6px 0;">
<div style="display:flex;flex-direction:column;align-items:center;">
<div style="width:3px;height:22px;background:#475569;"></div>
<div style="width:0;height:0;border-left:8px solid transparent;border-right:8px solid transparent;border-top:13px solid #475569;"></div>
</div></div>""", unsafe_allow_html=True)

    # ── 행 2: STEP 5 ~ 7 (오른쪽부터 채워 STEP 4 아래에 5가 오도록) ──
    _, empty2, c5, a5, c6, a6, c7 = st.columns([4, 0.7, 4, 0.7, 4, 0.7, 4])
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
        "1 / 6"
    )
    show_mission([
        "연구원 페르소나 항목(개인정보·기본 프로필·직무 역량 등)을 테이블에 직접 입력하기",
        "입력한 내용을 AI 대화창에 붙여넣기 위한 스크립트 형태로 완성하기",
        "AI가 페르소나를 적용했는지 간단한 질문으로 확인하기",
    ])

    tab_ex, tab_researcher, tab_marketer = st.tabs(["📖 예시 스크립트 보기", "🔬 연구원 페르소나 만들기", "📢 마케터 페르소나 만들기"])

    with tab_ex:
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
        st.markdown("##### STEP 2. 테이블을 복사해 AI 대화창에 붙여넣기")
        show_example("""음료개발연구원의 페르소나를 아래의 정보를 적용해서 작성해
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

메모리 업데이트! 지금부터 음료연구원은 이 페르소나를 적용
[페르소나 출력 후 간단한 질문으로 적용확인]
저당 탄산음료를 최근 유행 플레이버에 적용했을 때, 단맛을 어느 정도가 좋을까""")

        st.markdown("---")
        st.markdown("#### 마케터 페르소나 예시 — 김지안 (브랜드마케팅 매니저)")
        show_example("""RTD 음료 마케터의 페르소나를 아래의 정보를 적용해서 작성해
[페르소나 엑셀 데이터 붙여넣기]

이름: 김지안 / 연령: 34세 / 직장: 네추럴 랩 베버리지 / 직무: 브랜드마케팅 매니저 / 성별: 여성 / 출신지: 서울특별시
관심 음료 유형: 제로 탄산음료, 기능성 RTD, 과일 블렌딩 음료, 시즌 한정 음료, 프리미엄 티 음료
보유기술: 브랜드 전략 수립, 신제품 컨셉 도출, 소비자 인사이트 분석, 데이터 기반 마케팅, 채널별 판매전략, 캠페인 운영
시장 분석력: 국내외 식품음료 시장 트렌드에 대한 높은 이해도
상품기획자 마인드: 컨셉·타깃·가격·채널·패키지·커뮤니케이션 통합 관점
마케팅 포인트: 시장성, 차별성, 화제성, 소비자 공감, 브랜드 확장성, 시즌성 및 트렌드 반영
업무 환경: 판매 데이터 모니터링, 경쟁사 신제품 벤치마킹, 편의점·대형마트 조사, SNS 분석, FGI 및 설문조사
근무경력: 식음료 대기업 및 음료 브랜드사 마케팅 경력 8년

메모리 업데이트! 지금부터 음료마케터는 이 페르소나를 적용
[페르소나 출력 후 간단한 질문으로 적용확인]
저당 탄산음료를 최근 유행 플레이버에 적용한다면, 어떤 구성과 패키지?""")

    # ── 직무 테마 프리셋 ──────────────────────────────────────
    RESEARCHER_PRESETS = {
        "🧃 음료개발연구원": {
            "이름": "한서윤", "연령": "35세", "직장": "네추럴 랩 베버리지", "직무": "음료개발연구원", "성별": "여성",
            "근무경력": "헬스케어 음료 스타트업 5년 + 식품 음료 대기업 중견 연구원 15년 시니어",
            "관심 제품 유형": "커피(추출), 차(Tea), 유음료, 기능성 음료(에너지/단백질), 탄산음료",
            "보유기술": "배합 최적화기술: 감미료·산미료 밸런싱, 원부재료·향료 사용 경험 풍부",
            "식품공정 지식": "HTST(고온단시간), UHT(초고온살균), 레토르트 등 공정별 맛 변화 예측 능력",
            "식품배합비 이론": "맛 보존기술, 층 분리(침전) 제어, 유화 안정성(Emulsion Stability) 기술",
            "직무 역량": "HTST·UHT·레토르트 공정별 맛 변화 예측 / 맛 보존기술, 층 분리 제어, 유화 안정성(Emulsion Stability) 기술",
            "업무 환경": "당도계(Brix), 산도계(pH), 색차계, 가속 가혹 실험기(Incubator), 점도계",
            "관심사": "편의점(CVS) 신제품 모니터링, 제로슈거 소재 및 대체 감미료 연구",
            "품질 및 리스크관리": "가속 실험(35~45°C)으로 유통기한 경과에 따른 품질 변화 선제적 확인",
            "연구개발 포인트": "공장에서 나온 첫 병과 유통기한 마지막 날의 맛이 동일해야 한다 (재현성 중시)",
            "확인 질문": "저당 탄산음료를 최근 유행 플레이버에 적용했을 때, 단맛을 어느 정도가 좋을까",
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
        st.markdown("#### 📝 빈칸을 채워 나만의 연구원 페르소나를 완성하세요")

        # 랜덤 이름·회사 풀
        _R_NAME_POOL    = ["이민준","김도윤","박서준","최예린","정수연","윤지훈","강민서","조예은","오현우","신나영","한지원","양승현","서지우","문채원","임세진","배준혁","류지원","노아름","공민재","심은채"]
        _R_COMPANY_POOL = ["그린바이오푸드","케이에프앤비","푸드이노베이션","네추럴랩코리아","태양F&B","청정연구원","바이오에프씨","푸드앤사이언스","한울식품연구소","선진F&B","하이음료R&D","대한음료연구소","케이푸드바이오"]

        # ─── 기본 프로필 설정 ───
        st.markdown("##### 👤 기본 프로필 (이름·회사·거주지·연령·성별)")

        # 직무 테마를 먼저 결정해야 프리셋(rp) 기본값 사용 가능
        st.markdown('<span class="ml-step">① 어떤 분야의 연구원인가요?</span>', unsafe_allow_html=True)
        _r_preset_keys = list(RESEARCHER_PRESETS.keys())
        _r_default_key = _r_preset_keys[0]  # 🧃 음료개발연구원
        st.markdown('<span style="background:#fef08a;color:#92400e;padding:2px 10px;border-radius:6px;font-size:13px;font-weight:700;">★ 음료개발연구원이 기본 선택입니다</span>', unsafe_allow_html=True)
        r_theme = st.pills("직무 테마", _r_preset_keys, default=_r_default_key, key="r_theme_ml", label_visibility="collapsed")
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
            _AGE_OPTS = ["20대 초반","20대 후반","30대 초반","30대 후반","40대 초반","40대 후반","50대 이상"]
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
        _R_MARKET_OPTS = ["편의점(CVS)", "대형마트", "온라인·이커머스", "카페·외식 B2B", "수출·글로벌", "급식·단체급식", "드럭스토어·헬스"]
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

        prompt_r = f"""{r_job_val} 페르소나를 아래 정보로 작성해 주세요.

이름: {r_name_val} / 연령: {r_age_val} / 직장: {r_company_val} / 직무: {r_job_val} / 성별: {r_gender_val} / 거주지: {r_residence_val or '미입력'}
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

메모리 업데이트! 지금부터 이 연구원은 위 페르소나를 적용
[적용 확인] {r_test_q}"""

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
        _hw_ui("페르소나", prompt_r, "r_hw_submit")

    with tab_marketer:
        st.markdown("#### 📝 빈칸을 채워 나만의 마케터 페르소나를 완성하세요")

        # 랜덤 이름·회사 풀
        _M_NAME_POOL    = ["이지안","김서현","박민준","최다은","정유진","윤하늘","강수아","조민혁","오세영","신지은","한소희","양민재","서준혁","문가을","임채원","배나리","류지수","노민수","공다현","심재원"]
        _M_COMPANY_POOL = ["레드오션마케팅","브랜드퍼스트","마켓이노베이션","글로벌F&B마케팅","트렌드랩코리아","디지털식품마케팅","케이브랜드컨설팅","푸드마케팅그룹","한국음료마케팅","스마트F&B"]

        # ─── 기본 프로필 설정 ───
        st.markdown("##### 👤 기본 프로필 (이름·회사·거주지·연령·성별)")

        st.markdown('<span class="ml-step">① 어떤 분야의 마케터인가요?</span>', unsafe_allow_html=True)
        _m_preset_keys = list(MARKETER_PRESETS.keys())
        _m_default_key = _m_preset_keys[0]  # 🧃 음료 브랜드마케터
        st.markdown('<span style="background:#fef08a;color:#92400e;padding:2px 10px;border-radius:6px;font-size:13px;font-weight:700;">★ 음료 브랜드마케터가 기본 선택입니다</span>', unsafe_allow_html=True)
        m_theme = st.pills("직무 테마", _m_preset_keys, default=_m_default_key, key="m_theme_ml", label_visibility="collapsed")
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
            _AGE_OPTS = ["20대 초반","20대 후반","30대 초반","30대 후반","40대 초반","40대 후반","50대 이상"]
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
        _M_MARKET_OPTS = ["편의점(CVS)", "대형마트", "온라인·이커머스", "카페·외식 B2B", "수출·글로벌", "급식·단체급식", "드럭스토어·헬스"]
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

        prompt_m = f"""{m_job_val} 페르소나를 아래 정보로 작성해 주세요.

이름: {m_name_val} / 연령: {m_age_val} / 직장: {m_company_val} / 직무: {m_job_val} / 성별: {m_gender_val} / 거주지: {m_residence_val or '미입력'}
근무경력: {m_career_val}
관심사: {m_interest_val}
관심 제품: {m_prod_val}
관심 시장: {m_market_val or '미선택'}
보유기술: {m_skills_val}
시장 분석: {m_mktana_val}
채널 전략: {m_channel_val}
직무 역량: {m_comp_val}
마케팅 포인트: {m_mkt_val}

메모리 업데이트! 지금부터 이 마케터는 위 페르소나를 적용
[적용 확인] {m_test_q}"""

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
        _hw_ui("페르소나", prompt_m, "m_hw_submit")


# ----------------------------------------------------------
# 3. 제품 아이디어 도출
# ----------------------------------------------------------
elif section == "4️⃣ 시장분석 및 학습":
    show_banner(
        "시장분석 및 학습",
        "온라인 시장 현황 분석부터 식품 전문 데이터 학습, 보고서 작성까지 AI와 함께 시장을 읽습니다.",
        "4 / 6"
    )
    show_mission([
        "네이버 쇼핑 음료 판매 현황을 AI로 분석하기",
        "식품안전나라 품목제조보고서 데이터를 AI에게 학습시키기",
        "시장 조사 데이터를 기반으로 신제품 개발 보고서 작성하기",
    ])

    tab_online, tab_food, tab_learn, tab_report, tab_ai = st.tabs([
        "🛒 온라인 시장분석",
        "🗂️ 식품전문정보분석",
        "📊 시장조사 데이터 학습",
        "📝 보고서 작성하기",
        "🔄 AI 간 대화전환",
    ])

    # ── 탭 1: 온라인 시장분석 ──
    with tab_online:
        st.markdown("#### 🛒 네이버 쇼핑 음료 판매 현황 분석")

        sub_ex, sub_task = st.tabs(["📖 예시 스크립트", "📋 스크립트 작성 과제"])

        with sub_ex:
            st.info("아래 예시 스크립트를 참고해 ChatGPT 또는 Gemini에서 음료 판매 현황을 분석할 수 있습니다.")
            st.code("""네이버 쇼핑에서 RTD 음료 카테고리의 최신 판매 및 추천 현황을 분석해줘.

[분석 대상]
- 카테고리: RTD 음료 전체 (탄산·커피·주스·기능성·차·식물성 음료)
- 기준: 최신 판매량 순위 + 리뷰수 + 별점 기준 상위 제품 (최근 6개월)

[분석 항목]
1. 플레이버별 현황
   - 가장 많이 팔리는 맛/향 TOP 10
   - 신규 등장 플레이버 트렌드

2. 제조사별 현황
   - 카테고리별 상위 브랜드 점유율
   - 신규 진입 브랜드 동향

3. 원재료별 현황
   - 제품명·성분표에서 자주 등장하는 원재료 TOP 10
   - 기능성 원료 사용 트렌드 (콜라겐·GABA·L-테아닌 등)

4. 컨셉별 현황
   - 제로슈거 / 기능성 / 프리미엄 / 로컬 / 식물성 컨셉 비중
   - 최근 6개월 신제품 컨셉 변화 방향

[출력 형식]
각 항목을 표로 정리하고, 신제품 개발 시사점 3가지를 마지막에 요약해줘.
데이터 출처가 있으면 함께 명시해줘. 가짜 데이터나 추정값은 '추정' 표시 필수.""", language=None)

        with sub_task:
            # ── 시나리오 카드 ──
            _SCENARIOS = {
                "🥤 쿠팡 — 기능성 음료 트렌드": {
                    "상황": "당신은 기능성 RTD 음료(에너지 드링크·전해질 음료·단백질 음료) 신제품 담당자입니다.",
                    "과제": "쿠팡에서 기능성 음료 카테고리의 최신 판매 현황과 소비자 반응을 분석하는 스크립트를 작성하세요.",
                    "힌트": "플랫폼(쿠팡), 제품 카테고리(기능성 음료), 분석 기준(리뷰수·별점·판매량), 원하는 출력 형식을 모두 포함하세요.",
                },
                "☕ 마켓컬리 — 프리미엄 커피 음료": {
                    "상황": "당신은 프리미엄 RTD 커피 브랜드의 마케터입니다.",
                    "과제": "마켓컬리에서 프리미엄 콜드브루·라떼 음료의 판매 트렌드와 소비자 선호 원재료를 파악하는 스크립트를 작성하세요.",
                    "힌트": "프리미엄 채널(마켓컬리), 제품 세부 유형(콜드브루·라떼), 원재료·컨셉 분석 항목을 명확히 지정하세요.",
                },
                "🫧 편의점 앱 — 제로슈거 탄산음료": {
                    "상황": "당신은 제로슈거 탄산음료 신제품을 편의점 출시 전 경쟁 분석 중인 연구원입니다.",
                    "과제": "GS25·CU 편의점 앱 기반 제로슈거 탄산음료의 경쟁 현황과 플레이버 공백 영역을 찾는 스크립트를 작성하세요.",
                    "힌트": "채널(편의점), 제품군(제로슈거 탄산), 경쟁 공백 발굴 목적을 스크립트에 담으세요.",
                },
                "🌿 SNS — 식물성 음료 컨셉 트렌드": {
                    "상황": "당신은 귀리·아몬드 기반 식물성 음료의 신규 컨셉을 기획 중인 제품 개발팀장입니다.",
                    "과제": "인스타그램·유튜브 쇼츠에서 식물성 음료 관련 최신 트렌드 키워드와 소비자 반응을 수집하는 스크립트를 작성하세요.",
                    "힌트": "SNS 플랫폼, 해시태그·키워드 분석 방향, 컨셉별 소비자 반응 항목을 명확히 지정하세요.",
                },
            }

            st.markdown("##### 1️⃣ 시나리오를 선택하세요")
            chosen = st.pills(
                "시나리오", list(_SCENARIOS.keys()),
                key="online_scenario", label_visibility="collapsed"
            )
            sc = _SCENARIOS.get(chosen, list(_SCENARIOS.values())[0])

            st.markdown(
                f'<div style="background:#f0f9ff;border-left:4px solid #3b82f6;border-radius:8px;'
                f'padding:16px 20px;margin:8px 0 16px 0;">'
                f'<b>📌 상황</b><br>{sc["상황"]}<br><br>'
                f'<b>📝 과제</b><br>{sc["과제"]}<br><br>'
                f'<span style="color:#6b7280;font-size:13px;">💡 힌트: {sc["힌트"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown("##### 2️⃣ 분석 항목을 선택해 초안을 만들어보세요")

            col_hint1, col_hint2 = st.columns([2, 3])
            with col_hint1:
                st.caption("🖥️ 플랫폼 선택")
                _PLATFORM_OPTS = ["네이버 쇼핑", "쿠팡", "마켓컬리", "편의점 앱(CU·GS)", "인스타그램", "유튜브 쇼츠"]
                hint_platform = st.pills("플랫폼", _PLATFORM_OPTS, key="hint_platform", label_visibility="collapsed")

            with col_hint2:
                st.caption("🥤 음료 제품 카테고리 선택")
                _CATEGORY_OPTS = ["RTD 음료 전체", "탄산음료", "커피·차 음료", "기능성·에너지 음료", "과채음료", "유음료·발효유", "식물성 음료", "발효음료·콤부차", "혼합음료"]
                hint_category = st.pills("카테고리", _CATEGORY_OPTS, key="hint_category", label_visibility="collapsed")

            col_hint3, col_hint4 = st.columns([3, 2])
            with col_hint3:
                st.caption("🔍 분석 항목 (복수 선택)")
                _ANALYSIS_OPTS = ["플레이버 트렌드", "제조사·브랜드 현황", "원재료 사용 빈도", "컨셉·포지셔닝", "가격대 분포", "소비자 리뷰 감성", "신제품 출시 현황"]
                hint_items = st.pills("분석 항목", _ANALYSIS_OPTS, selection_mode="multi", key="hint_items", label_visibility="collapsed")

            with col_hint4:
                st.caption("📄 출력 형식")
                _FORMAT_OPTS = ["표 형식", "요약문", "키워드 목록", "TOP 10 순위"]
                hint_fmt = st.pills("출력 형식", _FORMAT_OPTS, key="hint_fmt", label_visibility="collapsed")

            # 노란색 추가 요청사항 입력 영역
            st.markdown("""<div style="background:#fefce8;border-radius:10px;padding:10px 16px;
border:2px solid #fde047;margin:8px 0 4px 0;">
<b style="color:#854d0e;">✏️ 추가 요청사항</b>
<span style="font-size:12px;color:#92400e;margin-left:8px;">스크립트에 추가할 내용을 자유롭게 입력하세요 (초안에 자동 포함)</span>
</div>""", unsafe_allow_html=True)
            online_extra = st.text_area("online_extra_label", key="online_extra", height=75,
                placeholder="예: 특정 브랜드 분석 제외, 신제품 위주, 추가 분석 항목 등",
                label_visibility="collapsed")

            st.markdown("---")

            # 초안 생성 버튼 (pending key 패턴)
            if "online_draft_pending" in st.session_state:
                st.session_state["online_user_script"] = st.session_state.pop("online_draft_pending")

            if st.button("✏️ 선택 항목으로 초안 생성", key="hint_gen_btn", use_container_width=True):
                _plat  = hint_platform or "네이버 쇼핑"
                _cat   = hint_category or "RTD 음료 전체"
                _items = hint_items or ["플레이버 트렌드", "원재료 사용 빈도"]
                _fmt   = hint_fmt or "표 형식"
                _items_str = "\n".join(f"{i+1}. {item}" for i, item in enumerate(_items))
                _draft = f"""{_plat}에서 {_cat} 카테고리의 최신 판매 현황을 분석해줘.

[분석 대상]
- 플랫폼: {_plat}
- 카테고리: {_cat}
- 기준: 최신 판매량 + 리뷰수 + 별점 기준 상위 제품 (최근 6개월)

[분석 항목]
{_items_str}

[출력 형식]
{_fmt}으로 정리하고, 신제품 개발 시사점 3가지를 마지막에 요약해줘.
데이터 출처가 있으면 함께 명시해줘.
※ 가짜 데이터 금지. 추정값은 '추정' 표시 필수."""
                if st.session_state.get("online_extra", "").strip():
                    _draft += f"\n\n[추가 요청사항]\n{st.session_state['online_extra']}"
                st.session_state["online_draft_pending"] = _draft

            st.markdown("##### 3️⃣ 초안을 내 상황에 맞게 수정하세요")
            user_script = st.text_area(
                "스크립트 작성",
                placeholder="위에서 항목을 선택한 뒤 '초안 생성' 버튼을 누르거나, 예시를 참고해 직접 작성하세요.",
                height=260,
                key="online_user_script",
                label_visibility="collapsed",
            )

            if user_script.strip():
                if st.button("📋 완성 스크립트 복사하기", key="online_copy_btn", use_container_width=True):
                    st.session_state["online_copy_snapshot"] = user_script
                    st.session_state["online_show_copy"] = not st.session_state.get("online_show_copy", False)
                if st.session_state.get("online_show_copy"):
                    st.markdown("**아래 스크립트를 복사해 ChatGPT에 붙여넣으세요**")
                    st.code(st.session_state.get("online_copy_snapshot", user_script), language=None)

            st.markdown("##### 4️⃣ 체크리스트로 자가 점검하세요")
            _CHECKLIST = [
                "분석 대상 플랫폼·채널을 명시했나요?",
                "제품 카테고리를 구체적으로 지정했나요?",
                "분석 항목(플레이버·제조사·원재료·컨셉 중 2개 이상)을 포함했나요?",
                "원하는 출력 형식(표·요약 등)을 지정했나요?",
                "가짜 데이터 방지 주의사항을 포함했나요?",
            ]
            checks = []
            for i, item in enumerate(_CHECKLIST):
                checks.append(st.checkbox(item, key=f"online_chk_{i}"))

            passed = sum(checks)
            if passed == 5:
                st.success("✅ 완벽합니다! 5개 항목을 모두 충족하는 좋은 스크립트입니다.")
            elif passed >= 3:
                st.warning(f"🔶 {passed}/5 충족 — 미체크 항목을 스크립트에 추가하면 더 좋은 결과를 얻을 수 있어요.")
            elif user_script.strip():
                st.error(f"⚠️ {passed}/5 충족 — 예시 스크립트를 다시 참고해 부족한 항목을 보완하세요.")
            else:
                st.caption("스크립트를 작성한 뒤 체크리스트를 체크해보세요.")

        # 파일링크 불필요: 온라인 시장분석 스크립트는 텍스트 제출로 충분
        _hw_ui("온라인시장분석", st.session_state.get("online_user_script", ""), "online_hw_submit")

    # ── 탭 2: 식품전문정보분석 ──
    with tab_food:
        _fid_foodsafety = "1T3xNARxfKrgLKTiyhNPJWYYE5s_MoTSy"
        _btn_food_html = (
            f'<a href="https://drive.google.com/file/d/{_fid_foodsafety}/view" target="_blank" '
            f'style="display:inline-block;padding:8px 18px;background:#fef08a;border:1.5px solid #f59e0b;'
            f'border-radius:8px;color:#92400e;font-weight:700;font-size:13px;text-decoration:none;">'
            f'📥 식품안전나라 품목제조보고서 데이터 다운로드</a>'
        )

        sub_food_ex, sub_food_task = st.tabs(["📖 예시 스크립트", "📋 스크립트 작성 과제"])

        # ── 예시 스크립트 ──
        with sub_food_ex:
            st.markdown("#### 🗂️ 식품안전나라 품목제조보고서 분석")
            st.markdown("**Step 1. 데이터 파일 다운로드**")
            st.info("아래 버튼에서 식품안전나라 품목제조보고서 데이터를 다운로드한 뒤 ChatGPT에 업로드하세요.")
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
            st.markdown(_btn_food_html, unsafe_allow_html=True)
            st.markdown("---")

            # ── 힌트 장치 (2행 × 2열) ──
            st.markdown("**🔧 힌트 선택 — 항목을 골라 초안을 생성하세요**")

            # 행 1: 자료배경서명 | 요청목적
            col_f1, col_f2 = st.columns([3, 3])
            with col_f1:
                st.caption("📂 자료배경서명 — 품목제조보고서 구성 항목 선택 (복수)")
                _BG_OPTS = [
                    "업체명",
                    "품목유형",
                    "제품명",
                    "성분개수",
                    "성분 및 사용한 원재료",
                ]
                food_bg = st.pills("자료배경서명", _BG_OPTS, selection_mode="multi", key="food_bg", label_visibility="collapsed")

            with col_f2:
                st.caption("🎯 요청목적")
                _PURPOSE_OPTS = [
                    "배합비 개발을 위한 원재료 분석",
                    "음료 카테고리별 트렌드 파악",
                    "경쟁 제품 성분 비교",
                    "소비자 선호 원재료 도출",
                    "신제품 컨셉 수립 참고",
                ]
                food_purpose = st.pills("요청목적", _PURPOSE_OPTS, key="food_purpose", label_visibility="collapsed")

            # 행 2: 요청사항(multi) | 처리제외(multi)
            col_f3, col_f4 = st.columns([3, 3])
            with col_f3:
                st.caption("📋 요청사항 (복수 선택)")
                _REQ_OPTS = [
                    "주요 원재료 사용 빈도 분석",
                    "배합 순서 및 우선순위 도출",
                    "제품유형별 분류 정리",
                    "생산 트렌드 분석",
                    "제품명으로부터 원재료 추정",
                    "신제품 개발 시사점 도출",
                    "카테고리별 성분 비교",
                ]
                food_reqs = st.pills("요청사항", _REQ_OPTS, selection_mode="multi", key="food_reqs", label_visibility="collapsed")

            with col_f4:
                st.caption("🚫 처리 제외 (복수 선택)")
                _EXCL_OPTS = [
                    "음료와 관계없는 품목 제외",
                    "건강기능식품 제외",
                    "중복 데이터 제거",
                    "10년 이상 된 데이터 제외",
                    "원재료 정보 불명확한 제품 제외",
                ]
                food_excls = st.pills("처리제외", _EXCL_OPTS, selection_mode="multi", key="food_excls", label_visibility="collapsed")

            # 행 3: 이외 요청사항(multi, 전폭)
            st.caption("💬 이외 요청사항 (복수 선택)")
            _OTHER_OPTS = [
                "할 수 있는 작업 목록 먼저 제시",
                "수행 전 사용자 확인 후 진행",
                "학습 결과 요약 제공 (10줄 이내)",
                "추가 분석 가능 항목 제안",
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
                _food_draft = f"""#자료배경서명
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
                    "#자료배경서명\n#요청목적\n#요청사항\n#처리제외\n#이외의 요청사항"
                ),
            )

            if food_script.strip():
                if st.button("📋 완성 스크립트 복사하기", key="food_copy_btn", use_container_width=True):
                    st.session_state["food_copy_snapshot"] = food_script
                    st.session_state["food_show_copy"] = not st.session_state.get("food_show_copy", False)
                if st.session_state.get("food_show_copy"):
                    st.code(st.session_state.get("food_copy_snapshot", food_script), language=None)

            # 파일링크 불필요: 식품전문정보 분석 스크립트는 텍스트 제출로 충분
            _hw_ui("식품전문정보분석", st.session_state.get("food_user_script", ""), "food_hw_submit")

    # ── 탭 3: 시장조사 데이터 학습 (편의점 매대 사진 분석) ──
    with tab_learn:
        # 편의점 매대 사진 Google Drive 파일 ID (5장) — 실제 ID로 교체 필요
        _CONV_ZIP_ID = "14gA_A7Lw3Q1J8qbmWK46go7PQJcMSPH1"

        def _photo_btn(label, fid):
            return (
                f'<a href="https://drive.google.com/file/d/{fid}/view" target="_blank" '
                f'style="display:inline-block;padding:9px 20px;background:#e0f2fe;border:1.5px solid #38bdf8;'
                f'border-radius:8px;color:#0369a1;font-weight:700;font-size:14px;text-decoration:none;margin:3px 2px;">'
                f'📦 {label}</a>'
            )

        sub_learn_ex, sub_learn_task = st.tabs(["📖 예시 스크립트", "📋 스크립트 작성 과제"])

        # ── 예시 스크립트 ──
        with sub_learn_ex:
            st.markdown("#### 🏪 편의점 매대 사진 분석 — 예시 스크립트")
            st.markdown("**Step 1. 편의점 매대 사진 다운로드 (5장)**")
            st.info("아래 사진 5장을 다운로드한 뒤 ChatGPT 또는 NotebookLM에 이미지로 업로드하세요.")
            _photo_html = _photo_btn("판매시장 분석용 자료 다운로드 (사진 5장 압축)", _CONV_ZIP_ID)
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
            st.markdown("**Step 1. 편의점 매대 사진 다운로드 (5장)**")
            st.markdown(_photo_html, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("**Step 2. 힌트 선택 후 스크립트 초안 생성**")

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
                _SCOPE_OPTS = ["RTD 음료 전체", "탄산음료", "커피·차 음료", "기능성·에너지 음료", "과채음료", "식물성 음료"]
                lrn_scope = st.pills("카테고리범위", _SCOPE_OPTS, key="lrn_scope", label_visibility="collapsed")
                lrn_scope_custom = _yellow_input("직접 입력 (예: 제로슈거 음료)", "lrn_scope_custom", "선택 외 카테고리 직접 입력")

            # 행 2: 분석 항목(multi) | 출력 방식(multi)
            col_lrn3, col_lrn4 = st.columns([3, 3])
            with col_lrn3:
                st.caption("🔍 분석 항목 (복수 선택)")
                _ITEM_OPTS = [
                    "SKU 구성 및 점유율",
                    "카테고리별 분류",
                    "브랜드·제조사 현황",
                    "컨셉·포지셔닝 분석",
                    "트렌드 키워드 도출",
                    "가격대 분포",
                    "신제품 출시 현황",
                ]
                lrn_items = st.pills("분석항목", _ITEM_OPTS, selection_mode="multi", key="lrn_items", label_visibility="collapsed")
                lrn_items_custom = _yellow_input("직접 입력 (예: 용량별 분포)", "lrn_items_custom", "추가 분석 항목 직접 입력")

            with col_lrn4:
                st.caption("📄 출력 방식 (복수 선택)")
                _OUT_OPTS = [
                    "표 형식 정리",
                    "raw 데이터 전체 출력",
                    "단계별 나눠서 출력",
                    "요약문 추가",
                    "전략적 특징 포함",
                ]
                lrn_outs = st.pills("출력방식", _OUT_OPTS, selection_mode="multi", key="lrn_outs", label_visibility="collapsed")
                lrn_outs_custom = _yellow_input("직접 입력 (예: 그래프 포함)", "lrn_outs_custom", "추가 출력 방식 직접 입력")

            # 행 3: 보고서 항목(multi, 전폭)
            st.caption("📊 보고서 포함 항목 (복수 선택)")
            _REPORT_OPTS = [
                "음료유형별 SKU 개수",
                "SKU 점유율 (%)",
                "전략적 특징 분석",
                "경쟁현황 요약",
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
                if st.button("📋 완성 스크립트 복사하기", key="learn_copy_btn", use_container_width=True):
                    # 클릭 시점 내용을 스냅샷으로 저장 (리런 후에도 원본 유지)
                    st.session_state["learn_copy_snapshot"] = learn_script
                    st.session_state["learn_show_copy"] = not st.session_state.get("learn_show_copy", False)
                if st.session_state.get("learn_show_copy"):
                    _snap = st.session_state.get("learn_copy_snapshot", learn_script)
                    st.code(_snap, language=None)

            # 파일링크: NotebookLM에서 만든 슬라이드/오디오 링크를 제출
            _hw_ui("시장조사학습", st.session_state.get("learn_user_script", ""), "learn_hw_submit",
                   with_file=True)

    # ── 탭 4: 보고서 작성하기 ──
    with tab_report:
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
Step 1 &nbsp;·&nbsp; OpenAI에서 보고서로 출력할 수 있는 스크립트를 작성하세요
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
            if st.button("📋 스크립트 복사하기", key="report_copy_btn", use_container_width=True):
                st.session_state["report_show_copy"] = not st.session_state.get("report_show_copy", False)
            if st.session_state.get("report_show_copy"):
                st.code(report_script, language=None)

        # 파일링크 불필요: 보고서 작성 스크립트는 텍스트 제출로 충분
        _hw_ui("보고서작성", st.session_state.get("report_user_script", ""), "report_hw_submit")

        # ── 정답 스크립트 (숨김 expander) ──
        with st.expander("▶ 정답 스크립트 보기"):
            st.caption("아래는 미션 항목을 모두 충족하는 예시 스크립트입니다. 참고 후 본인 스크립트에 반영해보세요.")
            st.code("""지금까지 학습하고 분석한 모든 데이터를 바탕으로 신제품 음료 개발 시장 분석 보고서를 작성해줘.

[보고서 목적]
2026년 출시 예정인 RTD 음료 신제품 개발을 위한 의사결정 참고 자료

[필수 포함 항목]

1. 시장 현황
   - 국내 RTD 음료 시장 규모 및 카테고리별 성장률 (최근 3년 추이)
   - 채널별(편의점·온라인·마트·B2B) 판매 현황 및 점유율

2. 소비자 트렌드
   - 2026년 주요 소비 키워드 (헬시플레저·제로·기능성·프리미엄 등)
   - 연령대별·채널별 구매 패턴 및 선호 플레이버 변화

3. 경쟁 시장 현황
   - 주요 브랜드(롯데칠성·코카콜라·웅진·동아오츠카 등) 경쟁 구도
   - 편의점 매대 SKU 분석 기반 카테고리 점유율
   - 품목제조보고서 기반 원재료 사용 빈도 TOP 10

4. 2026년 음료 신제품 추천 상위 3개 품목 도출
   - 추천 품목 ①: 제품 컨셉 · 타깃 소비자 · 핵심 원재료 · 추천 근거
   - 추천 품목 ②: 제품 컨셉 · 타깃 소비자 · 핵심 원재료 · 추천 근거
   - 추천 품목 ③: 제품 컨셉 · 타깃 소비자 · 핵심 원재료 · 추천 근거

[시각화 조건]
- 카테고리별 시장 점유율 테이블 또는 차트 1개 이상 필수 포함
- 원재료 사용 빈도 순위 테이블 포함

[출력 형식]
- 보고서 제목 / 목차 / 섹션별 내용 순서로 구성
- 슬라이드·PDF·웹페이지로 출력 가능한 형식으로 작성
- 수치 데이터는 반드시 출처 명시, 없으면 '추정' 표시
- 가짜 데이터 생성 금지""", language=None)

        st.markdown("---")

        # ════════════════════════════════════════
        # Step 2: NotebookLM 변환 스크립트
        # ════════════════════════════════════════
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Step 2 &nbsp;·&nbsp; OpenAI에서 작성한 스크립트를 NotebookLM용 슬라이드 스크립트로 변환하세요
</span>
</div>""", unsafe_allow_html=True)

        # ── 변환 명령 스크립트 (고정, 복사 가능) ──
        st.caption("아래 스크립트를 복사해 OpenAI에 붙여넣으면 NotebookLM용 스크립트로 변환해줍니다.")
        st.code("출력한 보고서를 노트북 lm용 보고서 작성 스크립트로 변환해주세요.", language=None)

        st.markdown("---")

        # ── NotebookLM 예시 스크립트 ──
        st.markdown("**📋 NotebookLM 슬라이드 보고서 스크립트 예시**")
        st.caption("변환 후 생성될 NotebookLM용 스크립트 예시입니다. 참고하여 완성도를 확인하세요.")
        st.code("""OpenAI에서 작성한 신제품 음료 개발 시장 분석 보고서를 NotebookLM 슬라이드 형식으로 변환해줘.

[슬라이드 구성]
- Slide 1: 표지 (보고서 제목 · 작성자 · 날짜)
- Slide 2: 목차
- Slide 3~4: 시장 현황 (테이블 또는 차트 포함)
- Slide 5~6: 소비자 트렌드 (키워드 시각화 포함)
- Slide 7~8: 경쟁 시장 현황 (SKU 점유율 테이블 포함)
- Slide 9~10: 2026년 신제품 추천 상위 3개 품목
- Slide 11: 결론 및 신제품 개발 방향 제언

[슬라이드 작성 조건]
- 각 슬라이드: 제목 1줄 + 핵심 내용 불릿 3~5개 + 시각화 자료 (가능한 경우)
- 발표 시간: 10분 내외 분량으로 구성
- 데이터 시각화: 테이블 또는 그래프 최소 1개 이상 포함 필수
- 가짜 데이터 생성 금지 — 업로드된 자료 기반으로만 작성

[최종 제출]
NotebookLM 슬라이드로 완성하여 발표 자료로 제출""", language=None)

    # ── 탭 5: AI 간 대화전환 ──
    with tab_ai:
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

        # ── Step 1: 현재 AI에서 업무 요약 받기 ──
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Step 1 &nbsp;·&nbsp; 현재 AI(ChatGPT)에 아래 스크립트를 입력하세요
</span><br>
<span style="font-size:13px;color:#64748b;">대화 맥락과 결과물을 다른 AI가 이해할 수 있는 형태로 요약·변환해달라고 요청합니다.</span>
</div>""", unsafe_allow_html=True)

        st.code("""지금까지 이 프로젝트에서 진행한 모든 업무를 요약해주고,
대화내용의 진행방향, 맥락, 결과물산출을 위한 스크립트를
제미나이용 입력 스크립트로 변환해주세요""", language=None)

        st.markdown("---")

        # ── Step 2: 이관 방법 ──
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 18px;
border:1.5px solid #cbd5e1;margin-bottom:12px;">
<span style="font-size:15px;font-weight:700;color:#1e293b;">
Step 2 &nbsp;·&nbsp; ChatGPT가 출력한 요약·변환 스크립트를 Gemini에 붙여넣으세요
</span><br>
<span style="font-size:13px;color:#64748b;">출력된 내용을 그대로 복사해 Gemini 새 대화창에 붙여넣으면 맥락이 전달됩니다.</span>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div style="background:#f1f5f9;border-radius:10px;padding:16px 20px;margin-bottom:12px;border:1.5px solid #cbd5e1;">
<b style="color:#1e293b;font-size:14px;">Gemini Gems에 자료와 페르소나를 입력하는 방법</b>
<ol style="color:#334155;font-size:13px;line-height:2.2;margin-top:10px;padding-left:18px;">
<li><b>Gemini 접속 후 왼쪽 메뉴에서 [Gems 만들기]</b>를 클릭합니다.</li>
<li><b>이름과 지침(Instructions) 입력</b> — 이 교육에서 작성한 연구원/마케터 <b>페르소나 스크립트를 그대로 붙여넣습니다.</b></li>
<li><b>파일 업로드</b> — 품목제조보고서, 편의점 매대 사진, 시장조사 자료 등 수집한 데이터를 <b>Gem의 소스 파일로 첨부</b>합니다.</li>
<li><b>저장 후 대화 시작</b> — Step 1에서 ChatGPT가 출력한 <b>요약·변환 스크립트를 첫 메시지로 붙여넣으면</b> 맥락이 전달되며 이어서 작업할 수 있습니다.</li>
<li>이후 대화에서는 <b>"위 내용을 바탕으로 [다음 작업]을 진행해줘"</b> 형태로 명령합니다.</li>
</ol>
</div>
""", unsafe_allow_html=True)

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
        "3 / 6"
    )
    show_mission([
        "어떤 데이터가 제품 개발에 필요한지 유형별로 파악하기",
        "AI에게 데이터를 정리·수집해 달라는 스크립트 작성하기",
        "정리된 데이터를 ChatGPT 프로젝트 소스로 추가하는 방법 익히기",
    ])

    # ── 음료 카테고리 선택 옵션 ──────────────────────────────
    BEV_CATEGORIES = [
        "음료 유형 전체 (RTD 전 카테고리)",
        "탄산음료",
        "커피·차 음료 (RTD)",
        "기능성·에너지 음료",
        "유음료·발효유",
        "과채음료",
        "식물성 음료 (두유·귀리·아몬드 등)",
        "발효음료·콤부차",
        "혼합음료",
        "생수·이온음료",
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
            "활용 계획": "RAG 검색 소스로 추가해 신제품 아이디어 도출 및 컨셉 개발 시 참조",
        },
        "🧪 원료·배합비 레퍼런스": {
            "제품 카테고리": "저당 기능성 음료",
            "분석 범위": "국내 식품공전 허가 원료 기준 + 해외 사용 사례",
            "수집 목적": "{category} 개발에 필요한 감미료·기능성 원료 선정 및 사용 기준 파악",
            "참고 자료": "식품안전나라 {category} 관련 원료 DB (HTML), 원료사 TDS·스펙시트 (PDF), PubMed 논문 (PDF), JECFA 모노그래프 (PDF)",
            "출력 형식": """## 1. 식품공전 허가 원료 기준 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (원료명·기능·허용 기준치·권장 사용 농도·주의사항)

## 2. 원료사 TDS·연구 논문 자료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (감미료·기능성 원료별 스펙 및 배합 적용 사례)

## 3. 실무 적용 포인트 및 우선 검토 원료
- [자료명](URL)
- 파일 형태: PDF / HTML / DOC
- 주요 내용 요약: (배합 설계 시 우선 검토 원료 TOP5 및 조합 시 주의사항)""",
            "활용 계획": "배합비 설계 단계에서 RAG 소스로 참조해 원료 적정성 자동 점검",
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
            "활용 계획": "RAG 기본 소스로 등록해 배합비 개발·품질 설계 전 단계에서 참조",
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
            "활용 계획": "개발 단계에서 RAG에 규격 초과 여부를 묻는 소스로 활용",
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
            "활용 계획": "RAG 소스에 추가 후 아이디어 도출 시 '국내 미적용 트렌드' 필터링 용도",
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
            "활용 계획": "RAG 공정 지식 소스로 추가해 배합비 제안 시 공정 적합성 자동 검토",
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
            "활용 계획": "신제품 컨셉 검증 및 배합 방향 설정 시 RAG 소스로 활용",
        },
    }
    # ─────────────────────────────────────────────────────────

    tab_ex, tab_collect, tab_project, tab_train = st.tabs([
        "📖 예시 스크립트 보기",
        "🗂️ 데이터 수집 스크립트 만들기",
        "📁 ChatGPT 프로젝트에 넣기",
        "🧠 AI 데이터 학습시키기",
    ])

    with tab_ex:
        st.markdown("#### 📋 데이터 수집 스크립트 3가지 — 복사해서 ChatGPT에 붙여넣으세요")
        st.info("아래 스크립트를 그대로 복사해 ChatGPT 또는 Gemini에 입력하면 해당 분야의 자료 목록을 받을 수 있습니다.")

        # ── 스크립트 1: 음료 제조기술 ──
        st.markdown("##### 1️⃣ 음료 제조기술 수집 스크립트")
        st.code("""음료 유형 전체 (RTD 전 카테고리) 제품 개발을 위한 [배합원리 및 공정지식] 자료를 찾아 주세요.

- 범위: 국내 및 농식품 데이터 베이스 참고할것
- 목적: 음료 유형 전체 (RTD 전 카테고리) 개발에 필요한 감미료·기능성 원료 선정 및 사용 기준 파악
- 출처 우선: 식품안전나라 음료 유형 전체 (RTD 전 카테고리) 관련 원료 DB (HTML), 원료사 TDS·스펙시트 (PDF), PubMed 논문 (PDF), JECFA 모노그래프 (PDF)
- 형태: PDF·HTML·DOC 공개 자료, 10MB 이하

출력: 자료명·URL·파일형태·내용요약을 ## 섹션 3개로 구분해 출력 (실제 접속 가능한 URL만)
인용횟수다수순 및 다운가능확인 검증할것
※ 가짜 URL 생성 금지. 링크 없으면 '공개 링크 없음' 명시.""", language=None)

        st.markdown("---")

        # ── 스크립트 2: 음료 시장정보 ──
        st.markdown("##### 2️⃣ 음료 시장정보 수집 스크립트")
        st.code("""음료 유형 전체 (RTD 전 카테고리) 제품 개발을 위한 [신제품 개발을 위한 26년 성수기 음료시장 자료데이터가 필요해] 자료를 찾아 주세요.

- 범위: 미국, 유럽 시장 및 국내 음료 RTD 제품 현황 통계정보 및 시장정보
- 목적: 2026년 음료 유형 전체 (RTD 전 카테고리) 신제품 출시를 위한 경쟁 현황 및 카테고리 트렌드 파악
- 출처 우선: 한국농수산식품유통공사(aT FIS) 음료 유형 전체 (RTD 전 카테고리) 통계, 닐슨코리아 공개 보도자료, 식품의약품안전처, 식품음료신문
- 형태: PDF·HTML·DOC 공개 자료, 10MB 이하

출력: 자료명·URL·파일형태·내용요약을 ## 섹션 3개로 구분해 출력 (실제 접속 가능한 URL만)
각 섹션을 ## 헤더로 구분하고 RAG 검색에 최적화된 구조화 문서로 작성해 주세요. 항목마다 독립적으로 검색·참조할 수 있도록 충분한 맥락을 포함하세요. 가짜 URL은 절대 생성하지 마세요.
※ 가짜 URL 생성 금지. 링크 없으면 '공개 링크 없음' 명시.""", language=None)

        st.markdown("---")

        # ── 스크립트 3: 원재료/성분 DB ──
        st.markdown("##### 3️⃣ 원재료/성분 데이터베이스 수집 스크립트")
        st.code("""음료 유형 전체 (RTD 전 카테고리) 제품 개발을 위한 [원료와 배합비 작성을 위한 원재료의 성분, 과일농축, 원물의 당, 산 데이터, 주요 당류의 감미도, 브릭스, 산미료 데이터] 자료를 찾아 주세요.

- 범위: 국내 기관 자료 및 관련분석 논문, 기술서 위주 검토
- 목적: 음료 유형 전체 (RTD 전 카테고리) 개발에 필요한 감미료·기능성 원료 선정 및 사용 기준 파악
- 출처 우선: 식품안전나라 음료 유형 전체 (RTD 전 카테고리) 관련 원료 DB (HTML), 원료사 TDS·스펙시트 (PDF), PubMed 논문 (PDF), JECFA 모노그래프 (PDF)
- 형태: PDF·HTML·DOC 공개 자료, 10MB 이하

출력: 자료명·URL·파일형태·내용요약을 ## 섹션 3개로 구분해 출력 (실제 접속 가능한 URL만)
각 섹션을 ## 헤더로 구분하고 RAG 검색에 최적화된 구조화 문서로 작성해 주세요. 항목마다 독립적으로 검색·참조할 수 있도록 충분한 맥락을 포함하세요. 가짜 URL은 절대 생성하지 마세요.
※ 가짜 URL 생성 금지. 링크 없으면 '공개 링크 없음' 명시.""", language=None)

    with tab_collect:
        st.markdown("#### 📝 빈칸을 채워 나만의 스크립트를 완성하세요")
        st.markdown('<p class="hint-text">① ~ ④ 순서대로 클릭하면 아래 문장이 완성됩니다</p>', unsafe_allow_html=True)

        SCOPE_OPTIONS = {
            "🏪 음료 시장 현황": {
                "국내 편의점·대형마트, 최근 2년": "국내 편의점·대형마트 채널 기준, 최근 2년 (2025~2026년 현재)",
                "국내 전 채널, 최근 3년": "국내 전 채널 기준, 최근 3년 (2024~2026년)",
                "온라인 채널 중심, 최근 1년": "온라인 채널(쿠팡·네이버쇼핑) 기준, 최근 1년 (2026년)",
                "편의점 채널 집중, 최근 1년": "편의점 채널 기준, 최근 1년 (2026년 현재)",
            },
            "🧪 원료·배합비 레퍼런스": {
                "국내 식품공전 + 해외 사례": "국내 식품공전 허가 원료 기준 + 해외 사용 사례",
                "국내 기준 집중 (식품공전)": "국내 식품공전 허가 원료 기준 (최신 개정판)",
                "해외 기준 비교": "미국 FDA·EU EFSA·일본 후생성 허가 기준 비교",
                "감미료·산미료 집중": "감미료·산미료·기능성 원료군 집중 분석",
            },
            "📚 음료개발 이론 지식": {
                "식품화학·공정·관능 전반": "식품화학, 음료 공정, 관능 이론 전반",
                "살균 공정 집중": "살균 공정 집중 (HTST·UHT·레토르트)",
                "배합 설계 이론 집중": "배합 설계 원리 집중 (Brix·pH·유화·점도)",
                "관능 평가 이론 집중": "관능 평가 방법론 및 소비자 맛 인지 이론 집중",
            },
            "⚖️ 식품 규격·허가 기준": {
                "국내 식품공전 + 개별인정 + 수출": "국내 식품공전 기준 + 개별인정형 원료 기준 + 수출 대상국 규격",
                "국내 식품공전 기준만": "국내 식품공전 기준 (최신 개정판)",
                "건강기능식품 인허가": "건강기능식품 인허가 기준 및 개별인정형 원료 절차",
                "수출 대상국 규격 비교": "미국·일본·EU 수출 대상국 규격 비교",
            },
            "🌏 해외 신제품 트렌드": {
                "미국·일본·유럽, 최근 2년": "미국·일본·유럽 주요 시장 기준, 최근 2년 (2025~2026년)",
                "미국 시장 집중": "미국 시장 집중 (Mintel·GNPD 기준, 최근 2년)",
                "일본·동아시아 시장 집중": "일본·동아시아 시장 기준, 최근 2년",
                "유럽 기능성·웰니스 집중": "유럽 기능성·웰니스 음료 시장 집중, 최근 2년",
            },
            "🔬 배합 원리·공정 지식": {
                "음료 공정 전반": "주요 음료 공정(HTST/UHT/레토르트/발효) 및 배합 설계 원리",
                "살균·무균 공정 집중": "살균·무균 충전 공정 집중 (HTST·UHT)",
                "발효 공정 집중": "발효 음료 공정 집중 (발효 스타터·산도·균주 설계)",
                "배합 설계 원리 집중": "배합 설계 원리 집중 (물성·안정성·원가 최적화)",
            },
            "👥 소비자 리뷰·반응 데이터": {
                "네이버·쿠팡·SNS, 최근 1년": "네이버 쇼핑·쿠팡·인스타그램·유튜브 소비자 리뷰 최근 1년",
                "네이버·쿠팡 리뷰 집중": "네이버 쇼핑·쿠팡 구매 리뷰 집중, 최근 1년",
                "SNS 중심, 최근 6개월": "인스타그램·유튜브·틱톡 SNS 반응 중심, 최근 6개월",
                "FGI·소비자 조사 중심": "FGI 결과 및 정량 소비자 조사 보고서 중심",
            },
        }
        OUTPUT_LABELS = {
            "RAG 링크형 📎": "RAG 링크형",
            "비교 표형 📊": "비교 표형",
            "교육 요약형 📄": "교육 요약형",
        }
        _REQ_DEFAULT = "각 섹션을 ## 헤더로 구분하고 RAG 검색에 최적화된 구조화 문서로 작성해 주세요. 항목마다 독립적으로 검색·참조할 수 있도록 충분한 맥락을 포함하세요. 가짜 URL은 절대 생성하지 마세요."
        REQUEST_MAP = {
            "RAG 최적화": _REQ_DEFAULT,
            "ChatGPT 프로젝트용": "ChatGPT 프로젝트 소스 파일로 저장 가능한 형태로 출력해 주세요. 내용을 복사해 txt 파일로 저장 후 바로 업로드할 수 있도록 구성해 주세요.",
            "발표 요약형": "발표용 A4 2페이지 이내 핵심 요약 형식으로 작성해 주세요. 핵심 수치·트렌드·시사점 위주로 구성하고, 교육생이 발표 자료로 바로 활용할 수 있도록 해 주세요.",
            "실제 URL 수집형": "반드시 실제로 접속 가능한 URL 링크만 제공해 주세요. 가짜 링크나 플레이스홀더는 절대 생성하지 말고, 링크가 없는 경우 '공개 링크 없음'으로 명시해 주세요.",
        }
        OUTPUT_CONTENT = {
            "RAG 링크형": None,  # dp["출력 형식"] 사용 (테마별 동적)
            "비교 표형": "원료명 / 기능 / 허용 기준치 / 권장 사용 농도 / 주의사항을 비교 표 형식으로 작성해 주세요.\n카테고리별·유형별로 구분된 표를 포함하고, 각 항목의 출처를 명기해 주세요.",
            "교육 요약형": "A4 2페이지 이내 핵심 요약 형식으로 작성해 주세요.\n주요 수치와 인사이트 위주로 정리하고, 교육생이 쉽게 이해할 수 있도록 용어 설명을 포함해 주세요.",
        }

        # ── ① 제품 ────────────────────────────────────────────
        st.markdown('<span class="ml-step">① 어떤 제품을 개발하나요?</span>', unsafe_allow_html=True)
        cat_sel = st.pills("제품", BEV_CATEGORIES, key="ml_cat", label_visibility="collapsed")
        cat_manual = st.text_input("직접 입력", placeholder="예: 저당 탄산음료, 기능성 에너지 음료", key="ml_cat_manual", label_visibility="collapsed")
        d_category = cat_manual.strip() or cat_sel or "음료 유형 전체 (RTD 전 카테고리)"
        cat_display = cat_manual.strip() or cat_sel

        # ── ② 데이터 유형 ─────────────────────────────────────
        st.markdown('<span class="ml-step">② 어떤 데이터가 필요한가요?</span>', unsafe_allow_html=True)
        theme_sel = st.pills("데이터 유형", list(DATA_PRESETS.keys()), key="ml_theme", label_visibility="collapsed")
        theme_manual = st.text_input("직접 입력", placeholder="예: 신제품 개발 연구원을 위한 배합비 이론 자료", key="ml_theme_manual", label_visibility="collapsed")
        d_theme = theme_sel or list(DATA_PRESETS.keys())[0]
        theme_display = theme_manual.strip() or theme_sel

        dp = DATA_PRESETS[d_theme]
        dtk = d_theme.replace(" ", "_").replace("·", "").replace(".", "")
        theme_label = theme_manual.strip() or (d_theme.split(" ", 1)[-1] if " " in d_theme else d_theme)
        dp_purpose = dp["수집 목적"].format(category=d_category)
        dp_sources = dp["참고 자료"].format(category=d_category)

        # ── ③ 분석 범위 ───────────────────────────────────────
        _scope_opts = SCOPE_OPTIONS.get(d_theme, {})
        st.markdown('<span class="ml-step">③ 어느 범위에서 찾을까요?</span>', unsafe_allow_html=True)
        scope_sel = st.pills("범위", list(_scope_opts.keys()), key=f"ml_scope_{dtk}", label_visibility="collapsed")
        scope_manual = st.text_input("직접 입력", placeholder="예: 국내 편의점 기준 최근 3년, 미국·일본 시장 비교", key=f"ml_scope_manual_{dtk}", label_visibility="collapsed")
        d_scope = scope_manual.strip() or _scope_opts.get(scope_sel, dp["분석 범위"])
        scope_display = scope_manual.strip() or scope_sel

        # ── ④ 출력 형식 ───────────────────────────────────────
        st.markdown('<span class="ml-step">④ 어떤 형태로 받을까요?</span>', unsafe_allow_html=True)
        out_sel = st.pills("출력", list(OUTPUT_LABELS.keys()), key=f"ml_out_{dtk}", label_visibility="collapsed")
        out_manual = st.text_input("직접 입력", placeholder="예: 핵심만 bullet point로, 표+요약 혼합형", key=f"ml_out_manual_{dtk}", label_visibility="collapsed")
        out_label = OUTPUT_LABELS.get(out_sel, "RAG 링크형")
        d_output = out_manual.strip() or OUTPUT_CONTENT.get(out_label) or dp["출력 형식"]
        out_display = out_manual.strip() or out_sel

        # ── ⑤ 추가 요청 (선택, expander) ──────────────────────
        with st.expander("⑤ 추가 요청사항 선택 (선택)"):
            req_sel = st.pills("요청사항", list(REQUEST_MAP.keys()), key=f"ml_req_{dtk}", label_visibility="collapsed")
            req_manual = st.text_area("직접 입력", placeholder="예: 인용 횟수 높은 순, 20페이지 이상 PDF 우선", key=f"ml_req_manual_{dtk}", label_visibility="collapsed", height=80)
        d_request = req_manual.strip() or REQUEST_MAP.get(req_sel, _REQ_DEFAULT)

        # ── Mad-lib 완성 문장 ─────────────────────────────────
        def _span(val, placeholder):
            if val:
                return f'<span class="ml-filled">{val}</span>'
            return f'<span class="ml-empty">{placeholder}</span>'

        st.markdown("---")
        st.markdown("### ✅ 내가 만든 스크립트")
        st.markdown(f"""
<div class="ml-box">
저는 {_span(cat_display, '제품 카테고리')}를 개발하기 위해,<br>
{_span(theme_display, '데이터 유형')} 데이터를 {_span(scope_display, '분석 범위')} 기준으로 수집하여<br>
{_span(out_display, '출력 형식')} 형태로 정리해 주세요.
</div>
""", unsafe_allow_html=True)

        # 수집 목적·참고 자료 (접이식)
        with st.expander("📌 수집 목적 · 참고 자료 확인"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**수집 목적**")
                st.info(dp_purpose)
            with col2:
                st.markdown("**참고 자료**")
                st.info(dp_sources)

        # ── 프롬프트 생성 & 작성 점검 ────────────────────────
        OUTPUT_SHORT = {
            "RAG 링크형": "자료명·URL·파일형태·내용요약을 ## 섹션 3개로 구분해 출력 (실제 접속 가능한 URL만)",
            "비교 표형": "항목별 비교 표로 출력 (항목명·기준치·출처 포함)",
            "교육 요약형": "A4 2페이지 이내 핵심 요약, 용어 설명 포함",
        }
        d_output_short = OUTPUT_SHORT.get(out_label, OUTPUT_SHORT["RAG 링크형"])

        prompt_d = f"""{d_category} 제품 개발을 위한 [{theme_label}] 자료를 찾아 주세요.

- 범위: {d_scope}
- 목적: {dp_purpose}
- 출처 우선: {dp_sources}
- 형태: PDF·HTML·DOC 공개 자료, 10MB 이하

출력: {d_output_short}
{d_request}
※ 가짜 URL 생성 금지. 링크 없으면 '공개 링크 없음' 명시."""

        d_fields = {"분석 범위": d_scope, "출력 형식": d_output, "요청사항": d_request}
        d_defaults = {"분석 범위": dp["분석 범위"], "출력 형식": dp["출력 형식"], "요청사항": _REQ_DEFAULT}
        render_data_coach(prompt_d, d_fields, d_defaults, f"d_{dtk}")
        # 파일링크 불필요: 데이터 수집 스크립트는 텍스트 제출로 충분
        _hw_ui("데이터수집스크립트", prompt_d, "collect_hw_submit")

    with tab_project:
        st.markdown("#### ChatGPT 프로젝트에 데이터 소스 추가하기")
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

        st.markdown("##### STEP 3. 프로젝트 소스 파일로 저장·추가")
        show_example("""방법 A — 파일 업로드 방식 (권장)
  1. AI 결과를 메모장(Notepad)에 붙여넣기
  2. '원료레퍼런스_저당음료.txt' 등 파일명으로 저장
  3. ChatGPT 프로젝트 → '파일 추가' → 저장한 파일 업로드

방법 B — 대화 내에서 직접 저장
  1. AI 결과 대화 화면에서 '프로젝트에 추가' 클릭 (ChatGPT Plus 기능)
  2. 저장할 프로젝트 선택 → 완료""")

        st.markdown("##### STEP 4. 프로젝트 내에서 AI에게 참조 요청")
        show_example("""같은 프로젝트에서 새 대화 시작 후:

"업로드한 원료 레퍼런스 데이터를 기반으로, 저당 탄산음료 배합 시
에리스리톨과 스테비아를 조합할 때 최적 비율과 주의사항을 알려줘"

→ AI가 업로드된 소스 파일을 참조해 답변합니다.""")

        st.markdown("---")
        st.markdown("##### 데이터 유형별 추천 파일 구성")
        st.markdown("""
| 파일명 | 내용 | 활용 시점 |
|---|---|---|
| `시장현황_RTD음료.txt` | 카테고리별 시장규모·트렌드 | 아이디어 도출 단계 |
| `원료레퍼런스_저당.txt` | 감미료·기능성 원료 기준표 | 배합비 설계 단계 |
| `음료이론_기초.txt` | 공정·화학 핵심 개념 요약 | 전 개발 단계 공통 |
| `식품규격_혼합음료.txt` | 식품공전 기준·규격 | 품질·인허가 단계 |
| `소비자인사이트.txt` | 리뷰 키워드·개선 요청 | 컨셉·배합 방향 설정 |
| `해외트렌드_2025.txt` | 글로벌 신제품 트렌드 | 아이디어 도출 단계 |
""")
        st.success("💡 TIP: 데이터 유형별로 파일을 나눠두면 배합비 설계 대화에서는 원료 파일만, 아이디어 도출 대화에서는 시장현황·트렌드 파일만 참조하도록 조절할 수 있어요.")

    with tab_train:
        st.markdown("#### 🧠 AI에게 빅데이터 학습시키기")
        st.info("ChatGPT 프로젝트에 데이터 소스를 등록한 뒤, 아래 스크립트를 전체 복사하여 ChatGPT 프로젝트 대화창에 붙여넣으세요.")

        st.markdown("##### 📋 학습 지시 스크립트")
        st.markdown("아래 스크립트를 그대로 복사해 ChatGPT에 입력하면 됩니다.")

        _TRAIN_SCRIPT = """음료개발 연구원 페르소나에게 음료개발용 데이터를 학습시켜주세요

#자료 구성
1. 데이터는 프로젝트에 소스로 입력되어있습니다.

#학습방법 요청
2. 학습은 입력한 연구원 페르소나 스크립트내에서 작업해주세요

#학습 및 작업우선순위
3. 학습할 목적에 따라 데이터를 학습하고, 앞으로는 이 절차와 내용에 따라서 음료개발에 1순위로 적용해주세요
4. 이외의 내용은 AI 가 페르소나의 가이드원칙에 따라서 학습하고 생성합니다.

#사전 확인사항
5. chatGPT의 프로젝트 소스에 등록한 리스트를 출력해주세요
6. 사용자에게 리스트가 맞는지 확인후 학습을 진행해주세요
7. 학습후 학습한 결과에 대해 10줄 이내로 피드백해주세요"""

        st.code(_TRAIN_SCRIPT, language=None)
        # 파일링크 불필요: 데이터 학습 지시 스크립트는 텍스트 제출로 충분
        _hw_ui("데이터학습지시", _TRAIN_SCRIPT, "train_hw_submit")


# ----------------------------------------------------------
# 5. 배합비 개발
# ----------------------------------------------------------
elif section == "5️⃣ 배합비 개발":
    show_banner(
        "배합비 개발",
        "Gemini Gem에 등록된 음료개발 데이터베이스를 활용하여 신제품 음료 배합비를 AI와 함께 작성합니다.",
        "5 / 6"
    )
    show_mission([
        "Gem에 등록된 '음료개발_데이터베이스' 파일을 AI가 학습한 후 배합비를 작성하도록 스크립트 작성하기",
        "제품 컨셉·기능성 성분·과일향 조건을 스크립트에 반영하기",
        "구글시트 수식 형식으로 원재료·배합비·단가·이화학 계산이 포함된 결과물 받기",
    ])

    tab_ex, tab_write, tab_mission, tab_process = st.tabs([
        "📖 예시 스크립트",
        "✏️ 배합비 작성",
        "🎯 미션수행",
        "🔬 개발 프로세스 실습",
    ])

    # ── 예시 스크립트 ──────────────────────────────────
    with tab_ex:
        st.markdown("#### 배합비 작성 기준 스크립트 — 복숭아 프로틴 음료 예시")
        st.info("아래 스크립트 양식을 기준으로 '배합비 작성' 탭에서 나만의 스크립트를 완성하세요.")
        st.code("""#요청배경
신제품 음료의 배합비 작성

#사용자료
Gem에 등록된 지식의 '음료개발_데이터베이스' 파일

#요청사항
아래 제품컨셉으로 제안된 제품의 신제품음료 배합비를
AI 음료개발자 페르소나를 이용해 작성하세요

#제품컨셉
프로틴 20g이 함유된 과즙감이 살아있는 복숭아맛 음료

#출력결과
구글시트로 각 원재료와 배합비, 단가, 이화학적 계산을 수식화

#작업가이드
데이터 결손이나 빈칸이 없어야 함.
시스템 부하가 걸리면, 나눠서 출력함. 배합 시뮬레이터양식에 맞출것
AI는 Gem의 지식을 배합비 작성전 학습할 것
위 요청사항과 명령을 모두 수행했을때 3회 검증후 결과물 출력하세요""", language=None)

        st.markdown("---")
        st.markdown("##### 스크립트 섹션별 작성 요령")
        for _tag, _desc in [
            ("#요청배경",  "배합비 작성 목적을 한 줄로 명시"),
            ("#사용자료",  "Gem에 등록한 파일명을 정확히 지정 → AI가 해당 지식을 우선 참조"),
            ("#요청사항",  "AI 페르소나(음료개발자)를 지정하고 작업을 구체적으로 지시"),
            ("#제품컨셉",  "기능성 성분 + 과일향 + 제품 특성을 1~2줄로 압축"),
            ("#출력결과",  "결과물 형식 지정 (구글시트 수식화 → AI가 시트 구조로 출력)"),
            ("#작업가이드","빈칸 없음·검증 횟수·양식 준수 등 품질 기준 명시"),
        ]:
            st.markdown(f"- **`{_tag}`** — {_desc}")

    # ── 배합비 작성 ────────────────────────────────────
    with tab_write:
        def _bev_input(label, key, placeholder="직접 입력"):
            st.markdown(
                f'<div style="background:#fefce8;border-radius:6px;padding:4px 10px 2px 10px;'
                f'border:1.5px solid #fde047;margin-top:4px;">'
                f'<span style="font-size:11px;color:#854d0e;font-weight:600;">✏️ {label}</span></div>',
                unsafe_allow_html=True,
            )
            return st.text_input(key, key=key, placeholder=placeholder, label_visibility="collapsed")

        st.info(
            "힌트 항목을 선택하거나 노란색 셀에 직접 입력하세요.\n\n"
            "선택 완료 후 **[📥 스크립트 반영하기]** 버튼을 눌러 완성 스크립트를 업데이트하세요."
        )
        st.markdown("**Step 1. 힌트 선택 후 스크립트 초안 생성**")

        # 제품명
        st.caption("🏷️ 제품명")
        bev_prodname = _bev_input("제품명 직접입력", "bev_prodname", "예: 복숭아 프로틴 샷 125ml")

        # 제품유형
        st.caption("🧃 제품유형")
        _PTYPE_OPTS = ["프로틴 음료", "저당 기능성음료", "과즙음료", "발효음료", "에너지음료"]
        bev_ptype = st.pills("제품유형", _PTYPE_OPTS, key="bev_ptype", label_visibility="collapsed")
        bev_ptype_c = _bev_input("오픈 항목 직접입력", "bev_ptype_c", "예: 기능성 RTD 음료")

        # 기능성 성분
        st.caption("💊 기능성 성분 (복수 선택)")
        _FUNC_OPTS = ["프로틴 20g", "비타민C 1000mg", "콜라겐 5000mg", "식이섬유 5g", "BCAA 3g", "아연·마그네슘 복합"]
        bev_func = st.pills("기능성성분", _FUNC_OPTS, selection_mode="multi", key="bev_func", label_visibility="collapsed")
        bev_func_c = _bev_input("오픈 항목 직접입력", "bev_func_c", "예: 글루타민 2g")

        # 과일/향
        st.caption("🍑 과일 / 향")
        _FRUIT_OPTS = ["복숭아", "오렌지", "사과", "포도", "레몬", "청포도", "딸기"]
        bev_fruit = st.pills("과일향", _FRUIT_OPTS, key="bev_fruit", label_visibility="collapsed")
        bev_fruit_c = _bev_input("오픈 항목 직접입력", "bev_fruit_c", "예: 망고패션")

        # 제품 특성
        st.caption("✨ 제품 특성 (복수 선택)")
        _CHAR_OPTS = ["과즙감이 살아있는", "청량감 강한", "부드러운 텍스처", "저당", "무색소", "고단백"]
        bev_char = st.pills("제품특성", _CHAR_OPTS, selection_mode="multi", key="bev_char", label_visibility="collapsed")
        bev_char_c = _bev_input("오픈 항목 직접입력", "bev_char_c", "예: 투명한 외관")

        # 출력 결과 형식
        st.caption("📊 출력 결과 형식")
        _OUT_OPTS = ["구글시트로 수식화", "엑셀 표로 정리", "텍스트 표 형식"]
        bev_out = st.pills("출력형식", _OUT_OPTS, key="bev_out", label_visibility="collapsed")
        bev_out_c = _bev_input("오픈 항목 직접입력", "bev_out_c", "예: 마크다운 표")

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
        _bev_out    = ", ".join(filter(None, [bev_out, bev_out_c.strip()])) or "구글시트로 수식화"
        _bev_ver    = bev_ver or "3회"

        _concept_lines = []
        if _bev_prodname:
            _concept_lines.append(f"제품명: {_bev_prodname}")
        _concept_lines.append(f"{', '.join(_bev_func)}이 함유된 {', '.join(_bev_char)} {_bev_fruit}맛 {_bev_ptype}")
        _concept = "\n".join(_concept_lines)

        if "구글시트" in _bev_out:
            _out_line = "구글시트로 각 원재료와 배합비, 단가, 이화학적 계산을 수식화"
        elif "엑셀" in _bev_out:
            _out_line = "엑셀 표로 원재료명·배합비율(%)·배합량(kg)·단가·이화학 계산 정리"
        else:
            _out_line = f"{_bev_out} — 원재료명, 배합비율(%), 배합량(kg), 단가, 이화학 계산 포함"

        bev_script = f"""#요청배경
신제품 음료의 배합비 작성

#사용자료
Gem에 등록된 지식의 '음료개발_데이터베이스' 파일

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
            st.code(_snap, language=None)

        # 파일링크 불필요: 배합비 스크립트는 텍스트 제출로 충분
        _hw_ui("배합비", st.session_state.get("bev_preview", bev_script), "bev_hw_submit")

    # ── 미션수행 ───────────────────────────────────────
    with tab_mission:
        show_mission([
            "미션 1 — AI가 개발한 배합비의 이화학적 규격과 원가가 정확히 반영되었는지 검증하기",
            "미션 2 — 시나리오를 선택하고, 그 상황을 해결하는 AI 요청 스크립트 작성하기",
        ])

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
        st.caption("AI가 출력한 시트에서 아래 값을 확인하여 입력하세요.")

        _mc1, _mc2 = st.columns(2)
        with _mc1:
            st.markdown("**이화학적 규격**")
            st.text_input("Brix (계산값)", placeholder="예: 11.2 °Bx", key="mv_brix")
            st.text_input("산도 (계산값)", placeholder="예: 0.35%", key="mv_acid")
            st.text_input("pH (계산값)", placeholder="예: 3.6", key="mv_ph")
            st.text_input("고형분함량 (계산값)", placeholder="예: 8.4%", key="mv_solid")
        with _mc2:
            st.markdown("**원가**")
            st.text_input("원료별 단가 누락 항목", placeholder="없으면 '없음' 입력", key="mv_cost_missing")
            st.text_input("제품 100ml당 원가", placeholder="예: 142원", key="mv_cost_100ml")
            st.text_input("전체 배합 기준 원가 합계", placeholder="예: 4,260원/3L", key="mv_cost_total")

        st.markdown("**검증 소견** (이상 항목 또는 수정 내용 메모)")
        st.text_area("검증소견", placeholder="예: pH 컬럼 수식 오류 → AI 재요청 후 3.6으로 수정됨",
                     key="mv_note", height=80, label_visibility="collapsed")

        with st.expander("▶ 정답 스크립트 보기"):
            st.caption("무결성 검증 후 시트 수정 요청 예시")
            st.code("""검증 결과 아래 항목이 누락/오류 상태야.
수정 후 전체 시트 다시 출력해줘.

- pH 컬럼: 수식 없이 공란 → 배합 후 예상 pH 계산식 추가
- 구연산 단가: 빈칸 → 시장 기준가 반영 (약 2,500원/kg)
- 100ml 원가: 기준량 환산 오류 → 전체 배합량(예: 3,000ml) 기준으로 재계산""",
                    language=None)

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
        ms2_scenario = st.pills("시나리오 선택", _SCN_OPTS, key="ms2_scenario",
                                label_visibility="collapsed")

        # 시나리오 설명 카드
        if ms2_scenario and "A" in ms2_scenario:
            st.markdown("""
<div style="background:#fefce8;border:1.5px solid #fde047;border-radius:10px;
padding:14px 18px;margin:8px 0;">
<b style="font-size:13px;color:#854d0e;">📉 시나리오 A — 원가절감</b>
<div style="font-size:13px;color:#713f12;margin-top:6px;line-height:1.8;">
<b>상황:</b> 원료 가격 인상으로 현재 배합비 기준 제품 단가가 목표를 <b>20% 초과</b>했습니다.<br>
<b>목표:</b> 맛·품질규격·기능성 원재료 함량 변화 없이 원가 20% 절감<br>
<b>조건:</b> Brix·pH·산도·고형분 규격 불변 / 기능성 성분 함량 불변
</div></div>""", unsafe_allow_html=True)
            _show_a = st.session_state.get("ms2_show_hints_a", False)
            if st.button("💡 힌트 닫기" if _show_a else "💡 힌트 보기", key="ms2_hint_toggle_a", use_container_width=True):
                st.session_state["ms2_show_hints_a"] = not _show_a
                st.rerun()
            if st.session_state.get("ms2_show_hints_a", False):
                st.markdown(
                    '<div style="background:#fef9c3;border:1.5px solid #facc15;'
                    'border-radius:8px;padding:12px 16px;margin:6px 0;">'
                    '<b style="color:#713f12;font-size:13px;">💡 힌트 — 선택 후 스크립트에 반영됩니다</b>',
                    unsafe_allow_html=True,
                )
                st.pills("절감 방향",
                    ["원료 대체", "배합비율 조정", "정제수 비율 상향", "농축액 농도 조정"],
                    selection_mode="multi", key="ms2_ha1", label_visibility="collapsed")
                st.pills("출력 형식",
                    ["원재료별 절감액 표", "변경 전/후 비교표", "절감률 합계 포함"],
                    selection_mode="multi", key="ms2_ha2", label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)
            _a1 = st.session_state.get("ms2_ha1") or []
            _a2 = st.session_state.get("ms2_ha2") or []
            _ms2_default = f"""현재 배합비 기준 제품 원가를 20% 낮추는 방법을 제안해줘.

[조건]
- 맛(관능 프로파일)에 변화 없을 것
- 이화학적 품질규격(Brix·산도·pH·고형분) 유지
- 기능성 원재료 함량 변경 불가

[절감 방향]
{', '.join(_a1) if _a1 else '원료 대체 / 배합비율 조정'}

[출력 형식]
{', '.join(_a2) if _a2 else '원재료명 / 현재단가 / 대체원료 / 대체단가 / 절감액 / 주의사항 표 형식'}
전체 절감률 합계 포함"""

        elif ms2_scenario and "B" in ms2_scenario:
            st.markdown("""
<div style="background:#f0f9ff;border:1.5px solid #7dd3fc;border-radius:10px;
padding:14px 18px;margin:8px 0;">
<b style="font-size:13px;color:#0c4a6e;">👅 시나리오 B — 맛 개선</b>
<div style="font-size:13px;color:#075985;margin-top:6px;line-height:1.8;">
<b>상황:</b> 소비자 조사 결과 <b>"과즙감이 약하다"</b>, <b>"단맛이 강하다"</b>는 피드백이 다수 접수됐습니다.<br>
<b>목표:</b> 과즙감 향상 + 단맛 저감<br>
<b>조건:</b> 기능성 성분 함량·Brix·pH 규격 불변 / 원가 변동 최소화
</div></div>""", unsafe_allow_html=True)
            _show_b = st.session_state.get("ms2_show_hints_b", False)
            if st.button("💡 힌트 닫기" if _show_b else "💡 힌트 보기", key="ms2_hint_toggle_b", use_container_width=True):
                st.session_state["ms2_show_hints_b"] = not _show_b
                st.rerun()
            if st.session_state.get("ms2_show_hints_b", False):
                st.markdown(
                    '<div style="background:#fef9c3;border:1.5px solid #facc15;'
                    'border-radius:8px;padding:12px 16px;margin:6px 0;">'
                    '<b style="color:#713f12;font-size:13px;">💡 힌트 — 선택 후 스크립트에 반영됩니다</b>',
                    unsafe_allow_html=True,
                )
                st.pills("개선 방향",
                    ["과즙감 향상 (농축액 증량)", "단맛 저감 (감미료 배합 조정)", "산미 강화 (산도 조절)", "향료 재배합"],
                    selection_mode="multi", key="ms2_hb1", label_visibility="collapsed")
                st.pills("검증 방법",
                    ["관능 검사 항목 포함", "변경 전/후 배합비 비교", "Brix·pH 수치 재확인"],
                    selection_mode="multi", key="ms2_hb2", label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)
            _b1 = st.session_state.get("ms2_hb1") or []
            _b2 = st.session_state.get("ms2_hb2") or []
            _ms2_default = f"""현재 배합비를 아래 소비자 피드백에 따라 수정해줘.

[소비자 피드백]
- 과즙감이 약하다
- 단맛이 강하다

[개선 방향]
{', '.join(_b1) if _b1 else '과즙감 향상 / 단맛 저감'}

[조건]
- 기능성 성분 함량 불변
- 이화학적 규격(Brix·pH·산도) 기존 범위 유지
- 원가 변동 최소화

[검증]
{', '.join(_b2) if _b2 else '변경 전/후 배합비 비교표 및 관능 검사 항목 포함'}
수정 후 전체 배합비 시트 다시 출력해줘."""
        else:
            _ms2_default = ""
            st.info("위에서 시나리오를 선택하면 힌트와 스크립트 작성란이 나타납니다.")

        if ms2_scenario:
            st.markdown("---")
            st.markdown("**스크립트 작성 → 수정 후 복사하세요**")

            if "ms2_script" not in st.session_state:
                st.session_state["ms2_script"] = _ms2_default

            st.text_area("미션2 스크립트", key="ms2_script",
                         height=260, label_visibility="collapsed")

            if st.button("📋 스크립트 복사하기", key="ms2_copy_btn", use_container_width=True):
                st.session_state["ms2_copy_snap"] = st.session_state.get("ms2_script", _ms2_default)
                st.session_state["ms2_show_copy"] = not st.session_state.get("ms2_show_copy", False)
            if st.session_state.get("ms2_show_copy"):
                st.code(st.session_state.get("ms2_copy_snap", _ms2_default), language=None)

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

        # ── 미션수행 결과 제출 ─────────────────────────
        _ms2_scn_label = ms2_scenario or "미선택"
        _mission_content = "\n".join([
            f"개발 제품명: {st.session_state.get('bev_prodname', '미입력')}",
            f"",
            f"[미션1 무결성 검증]",
            f"Brix: {st.session_state.get('mv_brix', '')}",
            f"산도: {st.session_state.get('mv_acid', '')}",
            f"pH: {st.session_state.get('mv_ph', '')}",
            f"고형분함량: {st.session_state.get('mv_solid', '')}",
            f"단가 누락항목: {st.session_state.get('mv_cost_missing', '')}",
            f"100ml 원가: {st.session_state.get('mv_cost_100ml', '')}",
            f"전체 원가: {st.session_state.get('mv_cost_total', '')}",
            f"검증소견: {st.session_state.get('mv_note', '')}",
            f"",
            f"[미션2 시나리오 대응]",
            f"선택 시나리오: {_ms2_scn_label}",
            f"작성 스크립트:\n{st.session_state.get('ms2_script', '')}",
        ])
        # 파일링크 필요: AI로 작성한 배합비를 구글 시트에 정리해 링크로 제출
        _hw_ui("배합비_미션", _mission_content, "bev_mission_hw_submit", with_file=True)

    # ── 개발 프로세스 실습 ──────────────────────────────
    with tab_process:
        show_mission([
            "STEP 1 — 시니어 연구원 페르소나 생성 후 맛 프로파일 & 실험배합비 훈련",
            "STEP 2 — 훈련된 AI가 내 배합비를 검증·코칭",
            "STEP 3 — 마케터 페르소나와 협의하여 최적안 도출",
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

        st.markdown("**STEP 1 결과 메모**")
        st.caption("AI에게 스크립트를 입력한 후 결과를 **3줄 이내**로 요약해 입력하세요.")
        st.text_area("s1_memo",
                     placeholder="예) 시니어 연구원 생성 완료 / A 실험배합비 2kg 완성 / C 맛 엔진: 감미료 비율 재조정 권고",
                     key="proc_step1", height=80, label_visibility="collapsed")

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

        st.markdown("**STEP 2 결과 메모**")
        st.caption("AI 코칭 결과를 **3줄 이내**로 요약해 입력하세요.")
        st.text_area("s2memo", placeholder="예) pH 3.8→3.6 조정 권고 / 구연산 투입 최종 단계로 변경 / 비타민C 0.05% 보강",
                     key="proc_step2", height=80, label_visibility="collapsed")

        # ── STEP 3: 마케터 페르소나와 협의 ──────────────
        st.markdown("---")
        st.markdown("""
<div style="background:#f8fafc;border-left:4px solid #1e293b;border-radius:0 8px 8px 0;
padding:14px 20px;margin-bottom:12px;">
<div style="font-size:15px;font-weight:800;color:#0f172a;margin-bottom:4px;">
🤝 STEP 3. 마케팅 페르소나 분석 → 최적안 도출</div>
<div style="font-size:13px;color:#475569;">
아래 스크립트로 기 설정된 마케팅 페르소나를 불러온 뒤, 확정 배합비에 대한
시장성·관능·원가·차별화·시장 진입 관점의 항목별 분석을 요청하세요.
</div></div>""", unsafe_allow_html=True)

        _S3_RECALL = """앞서 설정된 마케팅 페르소나를 불러와주세요.

방금 확정된 신제품 배합비를 아래 항목별로 마케팅 관점에서 분석해주세요:
1. 시장성 — 현재 시장 트렌드와의 부합도
2. 관능 경쟁력 — 소비자 맛·향미 선호 관점 평가
3. 원가 경쟁력 — 목표 판매가 대비 원가율 적정성
4. 차별화 포인트 — 기존 경쟁 제품 대비 강점
5. 시장 진입 가능성 — 출시 타이밍·채널 적합성

결과는 3줄 이내로 핵심만 요약해주세요."""

        if st.button("📋 마케팅 페르소나 불러오기 스크립트", key="proc_s3_recall_btn",
                     use_container_width=True):
            st.session_state["proc_s3_show"] = not st.session_state.get(
                "proc_s3_show", False)
        if st.session_state.get("proc_s3_show"):
            st.code(_S3_RECALL, language=None)

        st.markdown("**STEP 3 결과 메모**")
        st.caption("AI 분석 결과를 **3줄 이내**로 요약해 입력하세요.")
        st.text_area("s3memo", placeholder="예) 저당 트렌드 부합·시장성 우수 / 감귤 향미 차별화 강점 / 편의점 채널 단가 맞춤 조정 필요",
                     key="proc_step3", height=80, label_visibility="collapsed")

        # ── 과제 제출 ───────────────────────────────────
        _proc_content = "\n".join([
            f"개발 제품명: {st.session_state.get('bev_prodname', '미입력')}",
            f"",
            f"[STEP1 페르소나 생성 & 훈련 결과]",
            f"{st.session_state.get('proc_step1', '')}",
            f"",
            f"[STEP2 배합비 검증·코칭 내용]",
            f"{st.session_state.get('proc_step2', '')}",
            f"",
            f"[STEP3 마케팅 분석 결과 & 최종안]",
            f"{st.session_state.get('proc_step3', '')}",
        ])
        # 파일링크 불필요: 공정 설계 스크립트는 텍스트 제출로 충분
        _hw_ui("배합비_프로세스", _proc_content, "proc_hw_submit")


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

    tab_ex, tab_twin, tab_consumer, tab_sensory = st.tabs([
        "📋 스크립트 예시", "🔬 디지털 트윈랩", "👥 가상 소비자 모델 제작", "🧪 관능검사"
    ])

    # ── Tab 0: 스크립트 예시 ──────────────────────────────
    with tab_ex:
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
        _COL_OPTS = [
            "단가 기여 (원/kg × 비율 → 원료비)",
            "100ml 원가 합산",
            "목표원가 대비 초과 여부",
            "Brix 기여 (당도 기여값)",
            "산도 기여 (%)",
            "pH 추정값",
            "감미 강도 지수",
            "기능성 성분 함량 기여",
            "배합합계 오차 (±경고)",
        ]
        twin_cols = st.pills(
            "반응 컬럼", _COL_OPTS, selection_mode="multi",
            key="twin_cols", label_visibility="collapsed",
        )
        if not twin_cols:
            twin_cols = _COL_OPTS[:5]

        # ── A-2. 요약 지표 카드 선택 ────────────────────────────
        st.markdown("**배합표 상단 요약 카드 (슬라이더 연동 실시간 계산)**")
        _CARD_OPTS = [
            "배합합계 (%)",
            "100ml 원가 (원)",
            "Brix (°Bx)",
            "산도 (%)",
            "pH 추정값",
            "감미 강도 지수",
            "기능성 성분 총함량",
            "목표원가 달성률 (%)",
        ]
        twin_cards = st.pills(
            "요약 카드", _CARD_OPTS, selection_mode="multi",
            key="twin_cards", label_visibility="collapsed",
        )
        if not twin_cards:
            twin_cards = _CARD_OPTS[:5]

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
            _PROC_STEPS = [
                "원료 계량 (저울·눈금 애니메이션)",
                "혼합 탱크 투입 (원료 낙하 애니메이션)",
                "용해·혼합 (탱크 내부 교반기 회전)",
                "살균 (파이프 내 열수 흐름·온도 표시)",
                "냉각 (냉각 코일 색상 변화·온도 하강)",
                "충전 (노즐에서 액체 낙하·병 채워짐)",
                "밀봉·캡핑 (캡 누름 동작)",
                "이화학·미생물 검사 (현미경·시험관 애니메이션)",
                "포장 (컨베이어 이동·박스 접힘)",
                "출하 (트럭 출발 애니메이션)",
            ]
            twin_process = st.multiselect(
                "포함할 공정 단계",
                _PROC_STEPS,
                default=_PROC_STEPS[:6],
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
            con_age = st.multiselect("연령대", ["10대", "20대", "30대", "40대", "50대+"], ["20대", "30대"], key="con_age")
            con_gender = st.selectbox(
                "성별 구성", ["남녀 동수", "여성 비중 60%", "남성 비중 60%", "전체 여성", "전체 남성"],
                key="con_gender",
            )
            con_occupation = st.multiselect(
                "직업군", ["직장인", "학생", "주부", "자영업자", "전문직"],
                ["직장인", "학생"], key="con_occupation",
            )
            con_region = st.selectbox("거주지역", ["수도권", "전국 분산", "대도시", "중소도시"], key="con_region")

        st.markdown("**B. 관능조사 설계**")
        cb1, cb2 = st.columns(2)
        with cb1:
            con_method = st.selectbox("관능조사 기법", [
                "기호도 검사 (Hedonic Scale)", "QDA 묘사분석법",
                "비교 검사법 (Paired Comparison)", "순위 검사법 (Ranking Test)",
                "차이 검사법 (Triangle Test)",
            ], key="con_method")
            con_pass_score = st.slider("합격 기준 점수 (7점 만점)", 4.0, 7.0, 5.0, step=0.5, key="con_pass_score")
        with cb2:
            con_items = st.multiselect("관능조사 항목", [
                "색", "향", "맛(단맛)", "맛(신맛)", "맛(쓴맛)",
                "점도/텍스처", "후미", "전반적 기호도", "구매의향",
            ], ["향", "맛(단맛)", "맛(신맛)", "후미", "전반적 기호도", "구매의향"], key="con_items")

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
            st.code(_CON_SCRIPT, language=None)

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
        st.markdown("##### 🧪 관능검사 — 가상 소비자 맛 검증")

        _con_product_ref    = st.session_state.get("con_product", "")
        _con_count_ref      = st.session_state.get("con_count", 40)
        _con_items_ref      = st.session_state.get("con_items") or ["향", "맛(단맛)", "맛(신맛)", "후미", "전반적 기호도", "구매의향"]
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
            st.code(_SEN_SCRIPT, language=None)

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
        _hw_ui("관능검사", _sen_content, "sen_hw_submit")


# ----------------------------------------------------------
# 7. 프로젝트 정리
# ----------------------------------------------------------
elif section == "7️⃣ 프로젝트 정리":
    show_banner(
        "프로젝트 정리",
        "전 단계에서 학습한 내용을 단계별로 확인하고, AI 최종 요약 결과를 함께 제출합니다.",
        "FINAL"
    )
    show_mission([
        "단계별 학습 결과를 확인하고 전체 흐름을 정리하세요",
        "제미나이에게 최종 요약 스크립트를 입력하고 결과를 복사하세요",
        "학습 내용 정리 + AI 요약 결과를 함께 과제로 제출하세요",
    ])

    # ── 1단계 페르소나 필드 복원 ───────────────────────────
    _r_theme     = st.session_state.get("r_theme_ml") or ""
    _r_rtk       = _r_theme.replace(" ", "_").replace("·", "").replace(".", "")
    _r_name      = st.session_state.get(f"r_name_{_r_rtk}", "")
    _r_career    = st.session_state.get(f"r_career_{_r_rtk}", "")
    _r_job_disp  = (st.session_state.get("r_theme_manual", "").strip()
                    or (_r_theme.split(" ", 1)[-1] if " " in _r_theme else _r_theme))

    _m_theme     = st.session_state.get("m_theme_ml") or ""
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
    _r_con    = st.session_state.get("con_memo", "")
    _r_sen    = st.session_state.get("sen_result", "")

    def _na(v, limit=300):
        if not v:
            return "(아직 입력하지 않았습니다)"
        return (v[:limit] + "…") if len(v) > limit else v

    st.markdown("#### 📋 단계별 학습 결과 정리")

    with st.expander("👤 1단계 — 제품개발 페르소나", expanded=False):
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

    with st.expander("📂 2단계 — 제품개발용 데이터", expanded=False):
        st.markdown("**제품 카테고리**")
        st.text(_ml_cat or "(아직 입력하지 않았습니다)")
        st.markdown("**데이터 유형**")
        st.text(_ml_theme or "(아직 입력하지 않았습니다)")
        _col_ok = "✅ 제출 완료" if st.session_state.get("collect_hw_submit_done") else "⬜ 미제출"
        _trn_ok = "✅ 제출 완료" if st.session_state.get("train_hw_submit_done") else "⬜ 미제출"
        st.caption(f"데이터 수집 과제 {_col_ok}  |  데이터 학습 과제 {_trn_ok}")

    with st.expander("📊 3단계 — 시장분석 및 학습", expanded=False):
        st.markdown("**온라인 시장분석**")
        st.text(_na(_r_online))
        st.markdown("**식품전문정보 분석**")
        st.text(_na(_r_food))
        st.markdown("**시장조사 학습**")
        st.text(_na(_r_learn))
        st.markdown("**보고서 작성**")
        st.text(_na(_r_report))

    with st.expander("⚗️ 3단계 — 배합비 개발 결과", expanded=False):
        st.markdown(f"**제품명**: {_r_bev_nm or '(미입력)'}")
        st.markdown("**배합비 스크립트**")
        st.text(_na(_r_bev))
        st.markdown("**STEP 1 시니어 연구원 훈련 결과**")
        st.text(_r_proc1 or "(아직 입력하지 않았습니다)")
        st.markdown("**STEP 2 시니어 연구원 코칭 결과**")
        st.text(_r_proc2 or "(아직 입력하지 않았습니다)")
        st.markdown("**STEP 3 마케팅 분석 & 최종안 결과**")
        st.text(_r_proc3 or "(아직 입력하지 않았습니다)")

    with st.expander("🔬 3단계 — 가상모델 개발 결과", expanded=False):
        st.markdown("**디지털 트윈랩 결과**")
        st.text(_r_twin or "(아직 입력하지 않았습니다)")
        st.markdown("**가상 소비자 모델 결과**")
        st.text(_r_con or "(아직 입력하지 않았습니다)")
        st.markdown("**관능검사 결과**")
        st.text(_r_sen or "(아직 입력하지 않았습니다)")

    # 고정 제미나이 요약 스크립트
    st.markdown("---")
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
            "[1단계 제품개발 페르소나]\n"
            f"연구원: {_r_job_disp} / {_r_name} / {_r_career}\n"
            f"마케터: {_m_job_disp} / {_m_name} / {_m_career}"
        ),
        (
            "[2단계 제품개발용 데이터]\n"
            f"카테고리: {_ml_cat or '미입력'}\n"
            f"데이터 유형: {_ml_theme or '미입력'}"
        ),
        (
            "[3단계 시장분석]\n"
            f"온라인: {_trunc(_r_online)}\n"
            f"식품정보: {_trunc(_r_food)}"
        ),
        (
            "[3단계 배합비 개발]\n"
            f"제품명: {_r_bev_nm or '미입력'}\n"
            f"배합비: {_trunc(_r_bev)}\n"
            f"STEP1: {_r_proc1 or '미입력'}\n"
            f"STEP2: {_r_proc2 or '미입력'}\n"
            f"STEP3: {_r_proc3 or '미입력'}"
        ),
        (
            "[3단계 가상모델 개발]\n"
            f"트윈랩: {_r_twin or '미입력'}\n"
            f"소비자모델: {_r_con or '미입력'}\n"
            f"관능검사: {_r_sen or '미입력'}"
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
