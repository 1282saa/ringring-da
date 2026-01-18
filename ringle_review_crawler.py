#!/usr/bin/env python3
"""
링글(Ringle) 사용자 후기 크롤러
- Google Play 스토어 리뷰
- 클리앙 게시글
- 블라인드 공개 게시글
- 브런치 블로그
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import json
import os

# User-Agent 설정
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

# 결과 저장 리스트
all_reviews = []


def crawl_google_play():
    """Google Play 스토어 리뷰 크롤링"""
    print("\n[1/4] Google Play 스토어 리뷰 크롤링 중...")

    try:
        from google_play_scraper import app, reviews_all, Sort

        # 앱 정보 가져오기
        app_info = app('com.ringle', lang='ko', country='kr')
        print(f"  - 앱: {app_info['title']}")
        print(f"  - 평점: {app_info['score']}")
        print(f"  - 리뷰 수: {app_info['reviews']}")

        # 리뷰 가져오기 (최대 500개)
        result = reviews_all(
            'com.ringle',
            sleep_milliseconds=100,
            lang='ko',
            country='kr',
            sort=Sort.NEWEST
        )

        print(f"  - 수집된 리뷰: {len(result)}개")

        for review in result:
            all_reviews.append({
                'platform': 'Google Play',
                'text': review['content'],
                'rating': review['score'],
                'date': review['at'].strftime('%Y-%m-%d') if review['at'] else '',
                'author': review['userName'] if review['userName'] else 'Anonymous',
                'url': f"https://play.google.com/store/apps/details?id=com.ringle&reviewId={review['reviewId']}"
            })

        print(f"  ✅ Google Play 크롤링 완료: {len(result)}개")
        return len(result)

    except Exception as e:
        print(f"  ❌ Google Play 크롤링 실패: {e}")
        return 0


def crawl_clien():
    """클리앙 게시글 크롤링"""
    print("\n[2/4] 클리앙 게시글 크롤링 중...")

    clien_urls = [
        'https://www.clien.net/service/board/use/9288297',  # 링글플러스 사용기
        'https://www.clien.net/service/board/park/17774660',  # 링글 수업 체험기
    ]

    count = 0
    for url in clien_urls:
        try:
            time.sleep(1)  # 요청 간격
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

                # 제목
                title_elem = soup.select_one('.post_subject span')
                title = title_elem.get_text(strip=True) if title_elem else ''

                # 본문
                content_elem = soup.select_one('.post_article')
                if content_elem:
                    # 불필요한 요소 제거
                    for elem in content_elem.select('.attached_source, .og_box, script, style'):
                        elem.decompose()
                    text = content_elem.get_text(separator='\n', strip=True)
                else:
                    text = ''

                # 작성일
                date_elem = soup.select_one('.post_author span')
                date_str = ''
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
                    if date_match:
                        date_str = date_match.group(1)

                # 작성자
                author_elem = soup.select_one('.post_info .nickname')
                author = author_elem.get_text(strip=True) if author_elem else 'Anonymous'

                if text:
                    all_reviews.append({
                        'platform': 'Clien',
                        'text': f"[{title}]\n{text}" if title else text,
                        'rating': '',
                        'date': date_str,
                        'author': author,
                        'url': url
                    })
                    count += 1
                    print(f"  - 수집: {title[:30]}...")

        except Exception as e:
            print(f"  ⚠️ 클리앙 크롤링 오류 ({url}): {e}")

    print(f"  ✅ 클리앙 크롤링 완료: {count}개")
    return count


def crawl_blind():
    """블라인드 공개 게시글 크롤링"""
    print("\n[3/4] 블라인드 게시글 크롤링 중...")

    # 블라인드 URL들 (검색에서 발견된 것들)
    blind_urls = [
        'https://www.teamblind.com/kr/post/링글-화상영어-CKO0jbHJ',
        'https://www.teamblind.com/kr/post/영어공부-링글-강추강추-gfSS0fuq',
        'https://www.teamblind.com/kr/post/링글-돈값해-1HEYBaFF',
        'https://www.teamblind.com/kr/post/링글-써보신-분-J0pgRbCC',
        'https://www.teamblind.com/kr/post/링글-캠블리-등-화상-영어-어때-j6QPfnxh',
        'https://www.teamblind.com/kr/post/링글-써본사람-ovgwdpfq',
        'https://www.teamblind.com/kr/post/링글-해-본-사람-YZFw0ue4',
        'https://www.teamblind.com/kr/post/링글-화상영어-강추-8eQePASa',
    ]

    count = 0
    for url in blind_urls:
        try:
            time.sleep(1.5)  # 요청 간격
            response = requests.get(url, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

                # 제목
                title_elem = soup.select_one('h1.title, .article-title, [class*="title"]')
                title = title_elem.get_text(strip=True) if title_elem else ''

                # 본문 (여러 셀렉터 시도)
                content_elem = soup.select_one('.article-content, .post-content, [class*="content"]')
                text = content_elem.get_text(separator='\n', strip=True) if content_elem else ''

                # JSON-LD에서 데이터 추출 시도
                script_tags = soup.find_all('script', type='application/ld+json')
                for script in script_tags:
                    try:
                        data = json.loads(script.string)
                        if isinstance(data, dict):
                            if 'articleBody' in data:
                                text = data['articleBody']
                            if 'headline' in data:
                                title = data['headline']
                    except:
                        pass

                if text and len(text) > 20:
                    all_reviews.append({
                        'platform': 'Blind',
                        'text': f"[{title}]\n{text}" if title else text,
                        'rating': '',
                        'date': '',
                        'author': 'Anonymous',
                        'url': url
                    })
                    count += 1
                    print(f"  - 수집: {title[:30] if title else url[-20:]}...")

        except Exception as e:
            print(f"  ⚠️ 블라인드 크롤링 오류: {e}")

    print(f"  ✅ 블라인드 크롤링 완료: {count}개")
    return count


def crawl_brunch():
    """브런치 블로그 크롤링"""
    print("\n[4/4] 브런치 블로그 크롤링 중...")

    brunch_urls = [
        'https://brunch.co.kr/@0simi/162',  # 2년간 링글 347회 수업후 깨달은 링글 200%활용법
        'https://brunch.co.kr/@sunjae/21',  # 요즘 푹 빠진 링글 Ringle 사용기
        'https://brunch.co.kr/@kongkong2222/114',  # 아이비리그 화상영어 링글 8개월 진행 후기
    ]

    count = 0
    for url in brunch_urls:
        try:
            time.sleep(1)
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

                # 제목
                title_elem = soup.select_one('.cover_title, h1.title')
                title = title_elem.get_text(strip=True) if title_elem else ''

                # 본문
                content_elem = soup.select_one('.wrap_body_frame')
                if content_elem:
                    for elem in content_elem.select('script, style, .wrap_btn'):
                        elem.decompose()
                    text = content_elem.get_text(separator='\n', strip=True)
                else:
                    text = ''

                # 작성일
                date_elem = soup.select_one('.date_item, time')
                date_str = date_elem.get_text(strip=True) if date_elem else ''

                # 작성자
                author_elem = soup.select_one('.txt_username, .author_name')
                author = author_elem.get_text(strip=True) if author_elem else 'Anonymous'

                if text:
                    all_reviews.append({
                        'platform': 'Brunch',
                        'text': f"[{title}]\n{text}" if title else text,
                        'rating': '',
                        'date': date_str,
                        'author': author,
                        'url': url
                    })
                    count += 1
                    print(f"  - 수집: {title[:30]}...")

        except Exception as e:
            print(f"  ⚠️ 브런치 크롤링 오류 ({url}): {e}")

    print(f"  ✅ 브런치 크롤링 완료: {count}개")
    return count


def crawl_blog_reviews():
    """개인 블로그 후기 크롤링 (추가)"""
    print("\n[추가] 개인 블로그 후기 크롤링 중...")

    blog_urls = [
        ('https://kindoflegacy.com/entry/내돈내산-링글-영어회화-7개월-리뷰-캠블리-스픽-비교', 'Tistory'),
        ('https://kindoflegacy.com/entry/내돈내산-링글-1년-6개월-솔직-후기-feat수업가격AI-튜터스터디-클럽', 'Tistory'),
    ]

    count = 0
    for url, platform in blog_urls:
        try:
            time.sleep(1)
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

                # 제목
                title_elem = soup.select_one('h1, .title, .entry-title')
                title = title_elem.get_text(strip=True) if title_elem else ''

                # 본문
                content_elem = soup.select_one('.entry-content, .post-content, article')
                if content_elem:
                    for elem in content_elem.select('script, style, nav, .widget'):
                        elem.decompose()
                    text = content_elem.get_text(separator='\n', strip=True)
                else:
                    text = ''

                if text and len(text) > 100:
                    # 텍스트가 너무 길면 앞부분만 저장
                    if len(text) > 10000:
                        text = text[:10000] + "...(truncated)"

                    all_reviews.append({
                        'platform': platform,
                        'text': f"[{title}]\n{text}" if title else text,
                        'rating': '',
                        'date': '',
                        'author': 'Anonymous',
                        'url': url
                    })
                    count += 1
                    print(f"  - 수집: {title[:30] if title else url[-30:]}...")

        except Exception as e:
            print(f"  ⚠️ 블로그 크롤링 오류: {e}")

    print(f"  ✅ 블로그 크롤링 완료: {count}개")
    return count


def save_to_csv(output_path):
    """결과를 CSV로 저장"""
    if not all_reviews:
        print("\n❌ 수집된 데이터가 없습니다.")
        return None

    df = pd.DataFrame(all_reviews)

    # 컬럼 순서 정리
    columns = ['platform', 'text', 'rating', 'date', 'author', 'url']
    df = df[columns]

    # 텍스트 정리 (줄바꿈을 공백으로)
    df['text'] = df['text'].apply(lambda x: ' '.join(str(x).split()) if pd.notna(x) else '')

    # CSV 저장
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"\n📊 데이터 저장 완료: {output_path}")
    print(f"   - 총 {len(df)}개 리뷰 수집")
    print(f"   - 플랫폼별 분포:")
    print(df['platform'].value_counts().to_string())

    return df


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🔍 링글(Ringle) 사용자 후기 크롤러")
    print("=" * 60)

    start_time = time.time()

    # 각 플랫폼 크롤링
    gp_count = crawl_google_play()
    clien_count = crawl_clien()
    blind_count = crawl_blind()
    brunch_count = crawl_brunch()
    blog_count = crawl_blog_reviews()

    # 결과 저장
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'ringle_reviews.csv')
    df = save_to_csv(output_path)

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 60)
    print(f"✅ 크롤링 완료! (소요 시간: {elapsed_time:.1f}초)")
    print("=" * 60)

    # 요약 통계
    print(f"\n📈 수집 요약:")
    print(f"   - Google Play: {gp_count}개")
    print(f"   - 클리앙: {clien_count}개")
    print(f"   - 블라인드: {blind_count}개")
    print(f"   - 브런치: {brunch_count}개")
    print(f"   - 블로그: {blog_count}개")
    print(f"   - 총합: {len(all_reviews)}개")

    return df


if __name__ == '__main__':
    main()
