#!/usr/bin/env python3
"""
링글(Ringle) 네이버 블로그 전수조사 크롤러
- 다양한 키워드 조합으로 검색
- 페이지네이션 처리
- 본문 내용 추출
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime
from urllib.parse import quote, urljoin
import json
import os

# 설정
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://search.naver.com/',
}

# 키워드 전략
KEYWORDS = {
    'brand': [
        '링글',
        'Ringle',
        '링글플러스',
        '링글틴즈',
    ],
    'experience': [
        '링글 후기',
        '링글 리뷰',
        '링글 사용후기',
        '링글 솔직후기',
        '링글 내돈내산',
        '링글 체험',
        '링글 수업 후기',
        '링글 3개월',
        '링글 6개월',
        '링글 1년',
    ],
    'comparison': [
        '링글 vs 캠블리',
        '링글 캠블리 비교',
        '링글 스픽 비교',
        '링글 vs 스픽',
        '링글 화상영어 비교',
        '화상영어 추천 링글',
    ],
    'feature': [
        '링글 AI튜터',
        '링글 튜터',
        '링글 원어민',
        '링글 수업',
        '링글 교재',
        '링글 피드백',
    ],
    'price': [
        '링글 가격',
        '링글 수업료',
        '링글 할인',
        '링글 무료체험',
        '링글 쿠폰',
    ],
    'painpoint': [
        '링글 단점',
        '링글 환불',
        '링글 해지',
        '링글 불만',
    ],
}

def get_all_keywords():
    """모든 키워드 리스트 반환"""
    all_kw = []
    for category, keywords in KEYWORDS.items():
        all_kw.extend(keywords)
    return all_kw

def search_naver_blog(keyword, start=1, display=30):
    """네이버 블로그 검색 결과 가져오기"""

    # 네이버 통합검색 블로그 탭 URL
    url = f"https://search.naver.com/search.naver"
    params = {
        'where': 'blog',
        'query': keyword,
        'start': start,
        'display': display,
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"      ❌ 검색 오류: {e}")
        return None

def parse_search_results(html):
    """검색 결과 페이지 파싱"""
    results = []

    if not html:
        return results

    soup = BeautifulSoup(html, 'html.parser')

    # 블로그 검색 결과 항목들
    items = soup.select('.view_wrap, .api_txt_lines.total_tit, li.bx')

    # 다른 셀렉터도 시도
    if not items:
        items = soup.select('.total_wrap .total_group')

    if not items:
        # 개별 블로그 포스트 링크 추출
        links = soup.select('a.api_txt_lines.total_tit')
        for link in links:
            href = link.get('href', '')
            title = link.get_text(strip=True)
            if href and 'blog.naver.com' in href:
                results.append({
                    'title': title,
                    'url': href,
                    'snippet': '',
                    'author': '',
                    'date': '',
                })

    # 상세 정보 추출 시도
    for item in soup.select('.view_wrap'):
        try:
            # 제목
            title_elem = item.select_one('.api_txt_lines.total_tit')
            title = title_elem.get_text(strip=True) if title_elem else ''

            # URL
            url = title_elem.get('href', '') if title_elem else ''

            # 요약
            snippet_elem = item.select_one('.api_txt_lines.dsc_txt')
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''

            # 작성자
            author_elem = item.select_one('.sub_txt.sub_name')
            author = author_elem.get_text(strip=True) if author_elem else ''

            # 날짜
            date_elem = item.select_one('.sub_txt.sub_time')
            date = date_elem.get_text(strip=True) if date_elem else ''

            if url and 'blog.naver.com' in url:
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet,
                    'author': author,
                    'date': date,
                })
        except Exception as e:
            continue

    return results

def get_blog_content(url):
    """개별 블로그 포스트 본문 추출"""
    try:
        # 모바일 URL로 변환 (더 쉬운 파싱)
        if 'blog.naver.com' in url:
            # iframe 내부 URL 추출
            response = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # iframe src 찾기
            iframe = soup.select_one('iframe#mainFrame')
            if iframe:
                iframe_src = iframe.get('src', '')
                if iframe_src:
                    if iframe_src.startswith('/'):
                        iframe_url = f"https://blog.naver.com{iframe_src}"
                    else:
                        iframe_url = iframe_src

                    response = requests.get(iframe_url, headers=HEADERS, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')

            # 본문 추출
            content_selectors = [
                '.se-main-container',
                '.post-view',
                '#postViewArea',
                '.se_component_wrap',
                '#post-area',
                '.post_ct',
            ]

            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # 불필요한 요소 제거
                    for tag in content_elem.select('script, style, .se_oglink, .og_box'):
                        tag.decompose()

                    text = content_elem.get_text(separator=' ', strip=True)
                    if len(text) > 50:
                        return text[:8000]  # 최대 8000자

            # 전체 body에서 추출 시도
            body = soup.select_one('body')
            if body:
                text = body.get_text(separator=' ', strip=True)
                if len(text) > 100:
                    return text[:8000]

        return ''

    except Exception as e:
        return ''

def crawl_keyword(keyword, max_pages=10):
    """특정 키워드로 네이버 블로그 크롤링"""
    all_results = []
    seen_urls = set()

    print(f"   🔍 키워드: '{keyword}'")

    for page in range(1, max_pages + 1):
        start = (page - 1) * 30 + 1

        html = search_naver_blog(keyword, start=start)
        if not html:
            break

        results = parse_search_results(html)

        if not results:
            print(f"      페이지 {page}: 결과 없음, 종료")
            break

        new_count = 0
        for r in results:
            if r['url'] and r['url'] not in seen_urls:
                seen_urls.add(r['url'])
                r['search_keyword'] = keyword
                all_results.append(r)
                new_count += 1

        print(f"      페이지 {page}: {new_count}개 신규 (누적: {len(all_results)}개)")

        if new_count == 0:
            break

        time.sleep(1)  # 요청 간격

    return all_results

def enrich_with_content(results, sample_size=None):
    """검색 결과에 본문 내용 추가"""
    print(f"\n📄 본문 수집 중... (총 {len(results)}개)")

    if sample_size:
        results = results[:sample_size]

    for i, r in enumerate(results):
        if (i + 1) % 10 == 0:
            print(f"   진행: {i+1}/{len(results)}")

        content = get_blog_content(r['url'])
        r['content'] = content
        time.sleep(0.5)

    return results

def main():
    """메인 실행"""
    print("=" * 60)
    print("🔍 링글 네이버 블로그 전수조사 크롤러")
    print("=" * 60)

    start_time = time.time()
    all_results = []
    seen_urls = set()

    keywords = get_all_keywords()
    print(f"\n📋 총 {len(keywords)}개 키워드로 검색")
    print("-" * 60)

    for i, keyword in enumerate(keywords):
        print(f"\n[{i+1}/{len(keywords)}] 검색 중...")
        results = crawl_keyword(keyword, max_pages=5)  # 키워드당 최대 5페이지

        # 중복 제거하며 추가
        for r in results:
            if r['url'] not in seen_urls:
                seen_urls.add(r['url'])
                all_results.append(r)

        print(f"   ✅ 완료: {len(results)}개 수집 (전체 누적: {len(all_results)}개)")
        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"📊 검색 완료: 총 {len(all_results)}개 고유 포스트")

    # 본문 수집 (전체)
    print("\n📄 본문 내용 수집 시작...")
    all_results = enrich_with_content(all_results)

    # DataFrame 생성
    df = pd.DataFrame(all_results)
    df['company'] = 'Ringle'
    df['source_type'] = 'blog'
    df['source_platform'] = 'Naver Blog'
    df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 저장
    output_path = 'naver/ringle_naver_blog.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print(f"✅ 크롤링 완료!")
    print(f"   - 총 포스트: {len(df)}개")
    print(f"   - 본문 수집: {len(df[df['content'].notna() & (df['content'] != '')])}개")
    print(f"   - 소요 시간: {elapsed/60:.1f}분")
    print(f"   - 저장 위치: {output_path}")
    print("=" * 60)

    # 키워드별 통계
    print("\n📈 키워드별 수집 현황:")
    print(df['search_keyword'].value_counts().head(15).to_string())

    return df

if __name__ == '__main__':
    main()
