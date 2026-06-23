# app.py (v6.0) - AI 제품개발 실습교안 웹앱
"""
DEFAULT CODING RULES
- Role: 20년 경력 시니어 풀스택 개발자
- Constraints: 외부 라이브러리 최소, 오류 처리 포함, 가독성 최우선
- Purpose: AI 제품개발 실습교안 기반 Streamlit 교육용 웹페이지
"""

import streamlit as st
import importlib
from typing import Dict


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
# 2. 스타일 설정
# =========================================================

def apply_custom_style():
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 34px;
            font-weight: 800;
            color: #1f2937;
            margin-bottom: 8px;
        }
        .sub-title {
            font-size: 18px;
            color: #4b5563;
            margin-bottom: 24px;
        }
        .section-card {
            padding: 18px;
            border-radius: 14px;
            background-color: #f9fafb;
            border: 1px solid #e5e7eb;
            margin-bottom: 16px;
        }
        .script-box {
            padding: 16px;
            border-radius: 12px;
            background-color: #f3f4f6;
            border-left: 5px solid #6366f1;
            white-space: pre-wrap;
            font-family: "Noto Sans KR", sans-serif;
            font-size: 15px;
            line-height: 1.7;
        }
        .small-caption {
            color: #6b7280;
            font-size: 13px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


apply_custom_style()


# =========================================================
# 3. 기존 외부 앱 설정
# =========================================================

EXTERNAL_APPS: Dict[str, str] = {
    "🔁 가상 페르소나 개발모드": "abc_persona_main",
    "🥣 FoodTech 대시보드": "pages.foodtech.01_dashboard",
    "🔍 FoodTech 기술/제품 추천": "pages.foodtech.02_recommendation",
    "📊 FoodTech 요약 리포트": "pages.foodtech.03_summary",
}


# =========================================================
# 4. 공통 유틸 함수
# =========================================================

def safe_text(value: str, default: str = "") -> str:
    """입력값 공백 방지"""
    if value is None:
        return default
    value = str(value).strip()
    return value if value else default


def render_prompt_result(prompt: str):
    """생성된 프롬프트 출력"""
    st.markdown("### 생성된 AI 스크립트")
    st.text_area(
        label="복사해서 ChatGPT, Gemini, Claude 등에 입력하세요.",
        value=prompt.strip(),
        height=420
    )


def run_selected_external_app(module_path: str):
    """기존 외부 앱 실행"""
    try:
        module = importlib.import_module(module_path)

        if hasattr(module, "main"):
            module.main()
        else:
            st.error(f"❌ '{module_path}' 모듈에는 main() 함수가 없습니다.")

    except ModuleNotFoundError:
        st.error(
            f"""
            ❌ 모듈을 찾을 수 없습니다.

            실행하려는 모듈:
            `{module_path}`

            확인할 사항:
            1. 파일 경로가 실제로 존재하는지 확인
            2. 폴더에 `__init__.py`가 필요한 구조인지 확인
            3. 파일명이 숫자로 시작하거나 특수문자가 포함되어 있지 않은지 확인
            """
        )

    except Exception as e:
        st.error(f"❌ 앱 실행 중 오류가 발생했습니다: {e}")


# =========================================================
# 5. 메인 교육 앱
# =========================================================

def render_home():
    st.markdown('<div class="main-title">🧪 AI 제품개발 실습교안 작성 도우미</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">식품 신제품 개발 교육에서 사용할 AI 스크립트, 페르소나, 데이터, 배합비, 소비자 조사 프롬프트를 단계별로 작성합니다.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**대상**\n\n식품개발, 상품기획, 마케팅, 품질, 생산 실무자")

    with col2:
        st.success("**목적**\n\nAI를 활용한 제품개발 실습 스크립트 작성")

    with col3:
        st.warning("**결과물**\n\n제품 콘셉트, 페르소나, 배합비, 조사표, 발표 요약")

    st.markdown("## 교육 흐름")

    st.markdown(
        """
        | 단계 | 실습 내용 | 산출물 |
        |---|---|---|
        | 1 | 신제품 개발 프로세스 이해 | 기존 개발 vs AI 개발 비교 |
        | 2 | 제품개발 페르소나 만들기 | 기획자, 마케터, 연구원, 생산, 품질 페르소나 |
        | 3 | 제품 아이디어 도출 | 푸드테크 기반 제품 아이디어 |
        | 4 | 제품개발용 데이터 만들기 | 데이터 수집 계획, API 활용 방향 |
        | 5 | 배합비 개발 | 원료, Brix, pH, 공정 고려 배합비 |
        | 6 | 가상 소비자 조사 | 소비자 페르소나, 설문지, 응답 요약 |
        | 7 | 프로젝트 정리 | 발표용 요약문 |
        """
    )


def render_process_page():
    st.header("1. 신제품 개발 프로세스")

    st.markdown(
        """
        <div class="section-card">
        기존 식품개발 방식과 AI를 활용한 제품개발 방식을 비교하는 섹션입니다.
        교육 초반에 제품개발 흐름을 이해시키는 용도로 사용합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        product_category = st.text_input("제품 카테고리", "저당 과채음료")
        target_consumer = st.text_input("타깃 소비자", "2030 직장인")
        product_goal = st.text_input("개발 목적", "피로회복과 건강한 수분 보충")

    with col2:
        season = st.text_input("출시 시즌", "여름")
        sales_channel = st.text_input("판매 채널", "편의점, 온라인몰")
        ai_tool = st.text_input("활용 AI 도구", "ChatGPT, Gemini, Streamlit")

    if st.button("신제품 개발 프로세스 스크립트 생성", use_container_width=True):
        prompt = f"""
당신은 식품 신제품 개발 컨설턴트입니다.

다음 조건을 바탕으로 기존 식품개발 프로세스와 AI 활용 제품개발 프로세스를 비교해 주세요.

[제품 조건]
- 제품 카테고리: {safe_text(product_category)}
- 타깃 소비자: {safe_text(target_consumer)}
- 개발 목적: {safe_text(product_goal)}
- 출시 시즌: {safe_text(season)}
- 판매 채널: {safe_text(sales_channel)}
- 활용 AI 도구: {safe_text(ai_tool)}

[출력 형식]
1. 기존 식품개발 프로세스
2. AI 활용 식품개발 프로세스
3. 단계별 필요한 데이터
4. AI 활용 시 장점
5. 예상 리스크
6. 실무 적용 방안
7. 교육생 토론 질문 3개
"""
        render_prompt_result(prompt)


def render_persona_page():
    st.header("2. 제품개발 페르소나 만들기")

    st.markdown(
        """
        <div class="section-card">
        기획자, 마케터, 연구원, 생산팀, 품질팀 등 역할별 가상 페르소나를 만들고,
        제품개발 회의처럼 대화시키기 위한 스크립트를 작성합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("제품명", "오렌지 비트 에너지 샷")
        product_type = st.text_input("제품유형", "저당 기능성 음료")
        main_ingredients = st.text_area("주요 원료", "오렌지농축액, 비트농축액, 비타민B군, 타우린")

    with col2:
        target = st.text_input("타깃", "2030 직장인")
        package = st.text_input("포장 형태", "250mL 파우치팩")
        selected_roles = st.multiselect(
            "생성할 페르소나 역할",
            ["기획자", "마케터", "연구원", "생산팀", "품질팀", "구매팀", "영업팀"],
            ["기획자", "마케터", "연구원", "생산팀", "품질팀"]
        )

    if st.button("페르소나 스크립트 생성", use_container_width=True):
        roles_text = ", ".join(selected_roles)

        prompt = f"""
당신은 식품회사 신제품 개발 프로젝트 매니저입니다.

다음 제품을 개발하기 위해 역할별 가상 페르소나를 만들어 주세요.

[제품 정보]
- 제품명: {safe_text(product_name)}
- 제품유형: {safe_text(product_type)}
- 주요 원료: {safe_text(main_ingredients)}
- 타깃 소비자: {safe_text(target)}
- 포장 형태: {safe_text(package)}

[생성할 페르소나 역할]
{roles_text}

[출력 형식]
각 페르소나별로 아래 항목을 작성해 주세요.

1. 이름
2. 부서와 직무
3. 경력
4. 제품개발에서 중요하게 보는 기준
5. 우려하는 리스크
6. 제품에 대한 1차 의견
7. 회의에서 할 법한 발언 예시

마지막에는 위 페르소나들이 신제품 개발 회의를 하는 대화 예시를 작성해 주세요.
"""
        render_prompt_result(prompt)


def render_idea_page():
    st.header("3. 제품 아이디어 도출")

    st.markdown(
        """
        <div class="section-card">
        푸드테크 기술, 소비자 트렌드, 판매 채널을 입력하면 신제품 아이디어를 생성하는 스크립트를 작성합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        tech_keywords = st.text_area("푸드테크 기술 키워드", "저당화 기술, 천연 감미료, 기능성 원료, 발효 기술")
        product_group = st.text_input("제품군", "RTD 음료")
        consumer_trend = st.text_area("소비자 트렌드", "헬시플레저, 제로슈거, 피로회복, 간편 섭취")

    with col2:
        channel = st.text_input("출시 채널", "편의점")
        price_range = st.text_input("희망 가격대", "2,000원~3,000원")
        idea_count = st.number_input("아이디어 개수", min_value=1, max_value=20, value=5)

    if st.button("제품 아이디어 스크립트 생성", use_container_width=True):
        prompt = f"""
당신은 푸드테크 기반 식품 신제품 기획자입니다.

다음 기술과 시장 트렌드를 바탕으로 신제품 아이디어 {idea_count}개를 제안해 주세요.

[입력 조건]
- 푸드테크 기술 키워드: {safe_text(tech_keywords)}
- 제품군: {safe_text(product_group)}
- 소비자 트렌드: {safe_text(consumer_trend)}
- 출시 채널: {safe_text(channel)}
- 희망 가격대: {safe_text(price_range)}

[출력 형식]
표 형식으로 작성해 주세요.

항목:
1. 제품명
2. 핵심 콘셉트
3. 주요 원료
4. 타깃 소비자
5. 차별화 포인트
6. 예상 제조 리스크
7. 마케팅 문구
8. 제품화 우선순위 점수

마지막에는 가장 추천하는 제품 1개와 그 이유를 작성해 주세요.
"""
        render_prompt_result(prompt)


def render_data_page():
    st.header("4. 제품개발용 데이터 만들기")

    st.markdown(
        """
        <div class="section-card">
        식품안전나라, 품목제조보고, 시장 트렌드, 소비자 리뷰 등 제품개발에 필요한 데이터를 정리하는 스크립트를 작성합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        product_category = st.text_input("분석 제품군", "저당 음료")
        period = st.text_input("분석 기간", "최근 3년")
        purpose = st.text_area("분석 목적", "2026년 여름 출시용 저당 기능성 음료 개발")

    with col2:
        data_sources = st.multiselect(
            "활용 데이터 소스",
            [
                "식품안전나라",
                "품목제조보고",
                "네이버 블로그",
                "네이버 쇼핑",
                "해외 신제품 데이터",
                "소비자 리뷰",
                "논문",
                "특허"
            ],
            ["식품안전나라", "품목제조보고", "네이버 블로그", "네이버 쇼핑"]
        )

        output_type = st.selectbox(
            "원하는 결과 형태",
            ["데이터 수집 계획", "분석 항목표", "API 활용 계획", "Streamlit 화면 설계안"]
        )

    if st.button("데이터 활용 스크립트 생성", use_container_width=True):
        prompt = f"""
당신은 식품 신제품 개발용 데이터 분석가입니다.

다음 조건을 바탕으로 제품개발용 데이터 수집 및 분석 계획을 작성해 주세요.

[분석 조건]
- 분석 제품군: {safe_text(product_category)}
- 분석 기간: {safe_text(period)}
- 분석 목적: {safe_text(purpose)}
- 활용 데이터 소스: {", ".join(data_sources)}
- 원하는 결과 형태: {safe_text(output_type)}

[출력 형식]
1. 수집해야 할 데이터 항목
2. 데이터 출처별 활용 목적
3. 데이터 정제 방법
4. 제품개발에 연결하는 방법
5. Streamlit 화면 구성안
6. 분석 결과 예시
7. 교육생 실습 과제
"""
        render_prompt_result(prompt)


def render_formula_page():
    st.header("5. 배합비 개발")

    st.markdown(
        """
        <div class="section-card">
        제품명, 목표 Brix, 목표 pH, 원료 조건을 입력하여 배합비 개발용 AI 스크립트를 작성합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("제품명", "오렌지 비트 에너지 샷")
        product_type = st.text_input("제품유형", "저당 기능성 음료")
        base_weight = st.number_input("기준 배합량 kg", min_value=1.0, value=100.0)
        target_brix = st.number_input("목표 Brix", min_value=0.0, value=10.0)

    with col2:
        target_ph = st.number_input("목표 pH", min_value=0.0, value=3.5)
        main_ingredients = st.text_area("주요 원료", "오렌지농축액, 비트농축액, 비타민B군, 타우린")
        sweetener = st.text_input("감미료", "설탕, 알룰로스")
        acidulant = st.text_input("산미료", "구연산")

    if st.button("배합비 개발 스크립트 생성", use_container_width=True):
        prompt = f"""
당신은 음료 배합비 개발 전문가입니다.

다음 조건으로 {base_weight}kg 기준 음료 배합비 초안을 작성해 주세요.

[제품 조건]
- 제품명: {safe_text(product_name)}
- 제품유형: {safe_text(product_type)}
- 기준 배합량: {base_weight}kg
- 목표 Brix: {target_brix}
- 목표 pH: {target_ph}
- 주요 원료: {safe_text(main_ingredients)}
- 감미료: {safe_text(sweetener)}
- 산미료: {safe_text(acidulant)}

[출력 형식]
표 형식으로 작성해 주세요.

원료명 / 배합량 kg / 배합비율 % / 기여 Brix / 기능 / 주의사항

[추가 설명]
1. 배합 설계 의도
2. 목표 Brix 달성 방법
3. pH 조정 방법
4. 살균 공정 고려사항
5. 향미 개선 포인트
6. 품질 안정성 리스크
7. 추가 실험이 필요한 항목
"""
        render_prompt_result(prompt)


def render_consumer_page():
    st.header("6. 가상 소비자 조사")

    st.markdown(
        """
        <div class="section-card">
        제품 콘셉트를 바탕으로 소비자 페르소나, 설문 문항, 가상 응답, 구매의향 분석 스크립트를 작성합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("제품명", "오렌지 비트 에너지 샷")
        concept = st.text_area("제품 콘셉트", "저당, 피로회복, 여름 시즌 한정 기능성 음료")
        target = st.text_input("타깃 소비자", "2030 직장인")

    with col2:
        sample_size = st.number_input("가상 소비자 수", min_value=5, max_value=500, value=30)
        price = st.text_input("예상 판매가", "2,500원")
        channel = st.text_input("판매 채널", "편의점")

    if st.button("가상 소비자 조사 스크립트 생성", use_container_width=True):
        prompt = f"""
당신은 식품 소비자 조사 전문가입니다.

다음 제품에 대해 {target} 소비자 {sample_size}명을 대상으로 한 가상 소비자 조사를 설계해 주세요.

[제품 정보]
- 제품명: {safe_text(product_name)}
- 제품 콘셉트: {safe_text(concept)}
- 타깃 소비자: {safe_text(target)}
- 예상 판매가: {safe_text(price)}
- 판매 채널: {safe_text(channel)}

[출력 형식]
1. 소비자 페르소나 5종
2. 설문 문항 10개
3. 응답 척도 설계
4. 가상 응답 요약표
5. 구매의향 분석
6. 맛, 가격, 패키지, 콘셉트별 평가
7. 제품 개선 제안
8. 최종 출시 가능성 평가
"""
        render_prompt_result(prompt)


def render_project_page():
    st.header("7. 프로젝트 정리")

    st.markdown(
        """
        <div class="section-card">
        교육생이 만든 제품개발 결과를 발표자료 형태로 정리하는 최종 스크립트를 작성합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("최종 제품명", "오렌지 비트 에너지 샷")
        category = st.text_input("제품 카테고리", "저당 기능성 음료")
        target = st.text_input("타깃 소비자", "2030 직장인")

    with col2:
        core_concept = st.text_area("핵심 콘셉트", "저당, 피로회복, 여름 한정, 간편 섭취")
        key_result = st.text_area("주요 실습 결과", "페르소나 개발, 제품 아이디어 도출, 배합비 초안, 가상 소비자 조사")

    if st.button("최종 발표 스크립트 생성", use_container_width=True):
        prompt = f"""
다음 AI 제품개발 실습 결과를 발표자료 형식으로 정리해 주세요.

[프로젝트 정보]
- 최종 제품명: {safe_text(product_name)}
- 제품 카테고리: {safe_text(category)}
- 타깃 소비자: {safe_text(target)}
- 핵심 콘셉트: {safe_text(core_concept)}
- 주요 실습 결과: {safe_text(key_result)}

[출력 형식]
1. 프로젝트 개요
2. 제품개발 배경
3. 타깃 소비자 정의
4. 제품 콘셉트
5. AI를 활용한 개발 과정
6. 페르소나 회의 결과
7. 데이터 분석 방향
8. 배합비 개발 방향
9. 가상 소비자 조사 결과
10. 최종 개선 방향
11. 발표용 1분 요약문
12. 질의응답 예상 질문 5개와 답변
"""
        render_prompt_result(prompt)


def render_training_app():
    section = st.sidebar.radio(
        "📘 실습교안 목차",
        [
            "0. 교육 개요",
            "1. 신제품 개발 프로세스",
            "2. 제품개발 페르소나",
            "3. 제품 아이디어 도출",
            "4. 제품개발용 데이터",
            "5. 배합비 개발",
            "6. 가상 소비자 조사",
            "7. 프로젝트 정리",
        ],
        key="training_section"
    )

    if section == "0. 교육 개요":
        render_home()
    elif section == "1. 신제품 개발 프로세스":
        render_process_page()
    elif section == "2. 제품개발 페르소나":
        render_persona_page()
    elif section == "3. 제품 아이디어 도출":
        render_idea_page()
    elif section == "4. 제품개발용 데이터":
        render_data_page()
    elif section == "5. 배합비 개발":
        render_formula_page()
    elif section == "6. 가상 소비자 조사":
        render_consumer_page()
    elif section == "7. 프로젝트 정리":
        render_project_page()


# =========================================================
# 6. 최상위 앱 라우터
# =========================================================

def main():
    st.sidebar.title("🧪 식품개발 멀티앱 플랫폼")

    app_options = {
        "📘 AI 제품개발 실습교안": "internal_training_app",
        **EXTERNAL_APPS
    }

    selected_app = st.sidebar.selectbox(
        "📂 실행할 앱 선택",
        list(app_options.keys()),
        key="app_selector"
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("v6.0 | AI 제품개발 교육용 Streamlit 앱")

    selected_value = app_options[selected_app]

    if selected_value == "internal_training_app":
        render_training_app()
    else:
        run_selected_external_app(selected_value)


if __name__ == "__main__":
    main()
