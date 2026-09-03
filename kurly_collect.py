# -*- coding: utf-8 -*-
"""마켓컬리 검색·카테고리 수집기 (교육 실습용)

수집 근거
    kurly.com의 robots.txt는 `User-agent: *` 에 대해 `Allow: /` 이며,
    금지 경로는 /mypage/, /order/, /popup/, /games/, /shop/goods/goods_qna.php 뿐이다.
    검색(/search)과 카테고리(/categories) 경로는 금지 대상이 아니다. (2026-08 확인)

실행 방식
    Streamlit은 자체 이벤트 루프를 돌리므로 앱 프로세스 안에서 Playwright sync API를
    쓰면 충돌한다. 앱에서는 이 파일을 subprocess로 실행하고 표준출력의 JSON을 읽는다.
    진행 상황을 한 줄씩 흘려보내 앱이 실시간으로 표시할 수 있게 한다.

        python kurly_collect.py "제로 탄산" 100 판매량순 "" 전체
        python kurly_collect.py "" 200 판매량순 "생수·음료" 4천~8천원

예의
    - 페이지 사이에 1초 이상 쉰다.
    - 필요한 만큼만 가져오고 멈춘다.
    - 로그인이 필요한 영역에는 접근하지 않는다.
"""
import json
import re
import sys
import time
from urllib.parse import quote

# 윈도우 기본 인코딩(cp949)으로는 한글 대시 등을 못 써서 출력이 깨진다 → UTF-8 고정
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 카드 안에 섞여 나오는 버튼·배지 텍스트 (상품명이 아님)
_NOISE = {
    "담기", "샛별배송", "택배배송", "판매자배송", "일시품절", "품절",
    "Kurly Only", "한정수량", "새벽배송",
}

_JS = "els => els.map(e => ({href: e.getAttribute('href'), text: e.innerText}))"

# 정렬 (sorted_type) — 6종 모두 실측 확인
SORTS = {
    "추천순": None,
    "신상품순": 0,
    "판매량순": 1,
    "낮은 가격순": 2,
    "높은 가격순": 3,
    "혜택순": 5,
}

# 카테고리 (2026-08 확인)
CATEGORIES = {
    # 대분류
    "생수·음료 전체": "914",
    "커피·차 전체": "383",
    "유제품 전체": "018",
    "건강식품 전체": "032",
    # 음료 유형별 (하위 카테고리)
    "탄산수": "914002",
    "탄산·스포츠음료": "914003",
    "과일·야채음료": "914004",
    "차음료": "914005",
    "생수·얼음": "914001",
    "어린이음료": "914006",
    "커피음료": "383005",
    "콜드브루": "383004",
    "액상차·청": "383011",
}

# 가격대 — URL 필터(filters=price:)는 카테고리마다 ID가 달라 다른 카테고리에서는
# 0건이 되고 응답도 느려진다(실측). 그래서 수집한 뒤 최종가로 직접 거른다.
PRICE_RANGES = {
    "전체": (0, 10 ** 9),
    "4천원 미만": (0, 3999),
    "4천~8천원": (4000, 8000),
    "8천~2만원": (8000, 20000),
    "2만원 이상": (20000, 10 ** 9),
}
PRICE_FILTERS = PRICE_RANGES      # 앱에서 목록으로 쓰던 이름 유지


def _emit(obj):
    """진행 상황을 한 줄 JSON으로 즉시 흘려보낸다 (앱이 실시간으로 읽는다)."""
    print(json.dumps(obj, ensure_ascii=False), flush=True)


def _parse_card(href, text):
    """상품 카드의 innerText에서 항목을 뽑아낸다."""
    if not text:
        return None

    segs = [s.strip() for s in text.split("\n") if s.strip()]
    segs = [s for s in segs if s not in _NOISE]
    if not segs:
        return None

    # '쿠폰혜택가 6,286원'은 별도 값 — 정가로 잘못 잡히지 않게 먼저 분리한다
    coupon = ""
    rest = []
    for s in segs:
        if s.startswith("쿠폰혜택가"):
            m = re.search(r"([\d,]+)\s*원", s)
            if m:
                coupon = m.group(1)
            continue
        rest.append(s)
    segs = rest or segs

    # 상품명: 대괄호 브랜드가 붙은 세그먼트를 우선, 없으면 가장 긴 세그먼트
    name = ""
    for s in segs:
        if s.startswith("[") and "]" in s:
            name = s
            break
    if not name:
        cands = [s for s in segs if "원" not in s and len(s) >= 8]
        name = max(cands, key=len) if cands else segs[0]

    # 브랜드: 상품명 앞머리의 [브랜드]
    m = re.match(r"\[([^\]]+)\]", name)
    brand = m.group(1).strip() if m else ""

    # 설명문구: 상품명 바로 뒤의 짧은 홍보 문구
    desc = ""
    if name in segs:
        for s in segs[segs.index(name) + 1:]:
            if "원" in s or re.fullmatch(r"[\d,]+\+?", s):
                break
            if len(s) >= 4:
                desc = s
                break

    joined = " ".join(segs)

    # 할인율: '30%3,200원' 형태
    dm = re.search(r"(\d{1,2})\s*%\s*[\d,]+\s*원", joined)
    discount = (dm.group(1) + "%") if dm else ""

    # 가격: '12,345원' 패턴 (정가 → 할인가 순)
    prices = [int(x.replace(",", "")) for x in re.findall(r"([\d,]{3,})\s*원", joined)]
    list_price = prices[0] if prices else None
    sale_price = prices[1] if len(prices) > 1 else None

    # 용량 표기 (400mL, 1.5L, 200g 등)
    vm = re.search(r"(\d+(?:\.\d+)?\s*(?:mL|ml|ML|L|g|G|kg|KG))", name)
    volume = vm.group(1).replace(" ", "") if vm else ""

    # 리뷰수: 카드 맨 끝의 순수 숫자 (예: 488, 9,999+)
    review = ""
    if segs and re.fullmatch(r"[\d,]+\+?", segs[-1]):
        review = segs[-1]

    return {
        "상품명": name,
        "브랜드": brand,
        "용량": volume,
        "설명문구": desc,
        "정가": list_price,
        "할인가": sale_price,
        "할인율": discount,
        "쿠폰가": coupon,
        "최종가": sale_price if sale_price else list_price,
        "리뷰수": review,
        "링크": ("https://www.kurly.com" + href) if href.startswith("/") else href,
    }


def _build_url(page_no, keyword, category, sort, price):
    if category and category in CATEGORIES:
        url = ("https://www.kurly.com/categories/%s?page=%d&per_page=96"
               % (CATEGORIES[category], page_no))
    else:
        url = ("https://www.kurly.com/search?sword=%s&page=%d&per_page=96"
               % (quote(keyword), page_no))
    st = SORTS.get(sort)
    if st is not None:
        url += "&sorted_type=%d" % st
    return url


def collect(keyword, limit=100, max_pages=8, sort="추천순", category="", price="전체",
            name_filter=""):
    from playwright.sync_api import sync_playwright

    rows, seen = [], set()
    _emit({"t": "s", "msg": "브라우저를 준비하는 중"})

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox"])
        page = browser.new_page(user_agent=UA, locale="ko-KR")

        # 상품 정보는 텍스트에만 있으므로 이미지·폰트·미디어는 받지 않는다 (로딩 시간 단축)
        page.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in ("image", "media", "font")
            else route.continue_(),
        )

        try:
            for page_no in range(1, max_pages + 1):
                url = _build_url(page_no, keyword, category, sort, price)
                _emit({"t": "s", "msg": "%d페이지를 여는 중" % page_no})
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                try:
                    page.wait_for_selector('a[href*="/goods/"]', timeout=15000)
                except Exception:
                    pass
                page.wait_for_timeout(600)

                cards = page.eval_on_selector_all('a[href*="/goods/"]', _JS)
                if not cards:
                    _emit({"t": "s", "msg": "%d페이지에서 상품을 찾지 못했습니다" % page_no})
                    break
                _emit({"t": "s", "msg": "%d페이지에서 상품 %d개 발견 — 정리하는 중"
                                        % (page_no, len(cards))})

                added = 0
                for c in cards:
                    href = c.get("href") or ""
                    if not href or href in seen:
                        continue
                    seen.add(href)
                    row = _parse_card(href, c.get("text") or "")
                    # 가격대 걸러내기 (URL 필터가 카테고리마다 달라 여기서 직접 판정)
                    if row and price and price != "전체":
                        _lo, _hi = PRICE_RANGES.get(price, (0, 10 ** 9))
                        _fp = row.get("최종가")
                        if _fp is None or not (_lo <= _fp <= _hi):
                            continue
                    # 상품명 걸러내기 — 검색은 키워드 매칭이라 엉뚱한 품목이 섞인다
                    # (예: '과일주스' 검색 → 생과일까지 나옴)
                    if row and name_filter:
                        _words = [w.strip() for w in name_filter.split(",") if w.strip()]
                        if _words and not any(w in row["상품명"] for w in _words):
                            continue
                    if row and row["상품명"]:
                        rows.append(row)
                        added += 1
                        _emit({"t": "p", "done": len(rows), "total": limit, "row": row})
                    if len(rows) >= limit:
                        break

                if len(rows) >= limit or added == 0:
                    break
                time.sleep(1.0)          # 서버 부담을 주지 않기 위한 간격
        finally:
            browser.close()

    return rows[:limit]


if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else "음료"
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    srt = sys.argv[3] if len(sys.argv) > 3 else "추천순"
    cat = sys.argv[4] if len(sys.argv) > 4 else ""
    prc = sys.argv[5] if len(sys.argv) > 5 else "전체"
    nfl = sys.argv[6] if len(sys.argv) > 6 else ""
    try:
        data = collect(kw, lim, sort=srt, category=cat, price=prc, name_filter=nfl)
        _emit({"t": "r", "ok": True, "keyword": (cat or kw),
               "count": len(data), "rows": data})
    except Exception as e:                                  # noqa: BLE001
        _emit({"t": "r", "ok": False, "error": str(e)[:300]})
