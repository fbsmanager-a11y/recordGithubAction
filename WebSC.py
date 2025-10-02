import sys
import traceback
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

START_URL = (
    "https://search.naver.com/search.naver"
    "?where=nexearch&sm=top_hty&fbm=0&ie=utf8"
    "&query=%EA%B0%95%ED%98%95%EC%B2%A0&ackey=s5588o2j"
)

BASE_URL_FOR_JOIN = "https://search.naver.com/search.naver"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7",
}

TARGET_NAME = "강형철"
TARGET_SPANS = ["기업인", "1970"]

def normalize_text(s: str) -> str:
    return " ".join((s or "").split()).strip()

def match_title_box(box: BeautifulSoup) -> bool:
    """
    div.title_box 내부에서
    <strong class="name ..."><a>강형철</a></strong>
    그리고 순서 무관하게 sub_text 두 값(기업인, 1970)이 존재하는지 검사
    """
    a = box.select_one("strong.name a")
    if not a:
        return False
    name = normalize_text(a.get_text())
    if name != TARGET_NAME:
        return False

    spans = [normalize_text(s.get_text()) for s in box.select("span.sub_text")]
    # 두 값이 모두 포함되는지 확인 (순서 무관)
    return all(val in spans for val in TARGET_SPANS)

def find_target_url(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # 후보: div.title_box 블록들만 훑으며 정확 비교
    for box in soup.select("div.title_box"):
        if match_title_box(box):
            a = box.select_one("strong.name a[href]")
            if not a:
                continue
            href = a.get("href", "").strip()
            if not href:
                continue
            return urljoin(BASE_URL_FOR_JOIN, href)

    # 구조 변경 대비: fallback(전체 a태그를 검사) — name/스팬 매칭 통과하는 부모 div 탐색
    for a in soup.select("a[href]"):
        parent_box = a.find_parent("div", class_="title_box")
        if not parent_box:
            continue
        if match_title_box(parent_box):
            return urljoin(BASE_URL_FOR_JOIN, a["href"])

    raise RuntimeError("요청하신 이름/서브텍스트와 일치하는 블록을 찾지 못했습니다.")

def main():
    try:
        print(f"[1/3] GET {START_URL}")
        r = requests.get(START_URL, headers=HEADERS, timeout=10)
        r.raise_for_status()

        print("[2/3] HTML 분석 후 일치 블록 탐색…")
        target_url = find_target_url(r.text)
        print("  └ 이동할 URL:", target_url)

        print(f"[3/3] GET {target_url}")
        r2 = requests.get(target_url, headers=HEADERS, timeout=10)
        print("  └ 응답 코드:", r2.status_code)

        if r2.ok:
            soup2 = BeautifulSoup(r2.text, "html.parser")
            title = (soup2.title.string if soup2.title else "").strip()
            print("  └ 페이지 제목:", title[:160])

    except Exception as e:
        print("에러 발생:", e, file=sys.stderr)
        traceback.print_exc()

if __name__ == "__main__":
    main()
