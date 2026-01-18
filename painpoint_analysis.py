#!/usr/bin/env python3
"""
링글(Ringle) 페인포인트 분석
- 수집된 리뷰에서 불만/개선사항 추출
- 카테고리별 분류
"""

import pandas as pd
import re
from collections import Counter
import os

# 페인포인트 키워드 사전
PAINPOINT_KEYWORDS = {
    '가격': [
        '비싸', '비쌈', '가격', '비용', '돈', '금액', '요금', '크레딧', '할인',
        '부담', '비싼', '저렴', '가성비', '결제', '환불', '구독', '싸', '값'
    ],
    '튜터 품질': [
        '튜터', '선생님', '강사', '원어민', '수준', '실력', '피드백', '교정',
        '발음', '악센트', '불친절', '친절', '태도', '준비', '전문', '경험',
        '답변', '설명', '이해', '무성의'
    ],
    '예약 시스템': [
        '예약', '스케줄', '시간', '일정', '취소', '변경', '오픈', '마감',
        '알림', '노쇼', '대기', '자리', '슬롯', '가능한', '못잡', '스케쥴'
    ],
    '앱 UX/버그': [
        '앱', '오류', '버그', '느리', '렉', '속도', '불편', '인터페이스',
        '화면', '접속', '로그인', '연결', '끊김', '터치', '안됨', '안됩',
        '업데이트', '설치', '오디오', '영상', '줌', '크래시', '튕김',
        '스크롤', '불안정', '안먹', '작동'
    ],
    '수업 효과': [
        '효과', '실력', '향상', '발전', '변화', '도움', '성장', '진전',
        '느낌', '체감', '결과', '학습', '공부', '연습', '복습', '예습'
    ],
    '콘텐츠/교재': [
        '교재', '콘텐츠', '자료', '주제', '토픽', '아티클', '웨비나',
        '수업자료', '내용', '질문', '대화', '토론'
    ],
    '고객지원': [
        '고객', '문의', '응대', '답변', '서비스', '지원', '센터', '이메일',
        '연락', '해결', '대응'
    ]
}

# 부정적 표현
NEGATIVE_INDICATORS = [
    '안', '못', '없', '불', '힘들', '어렵', '싫', '별로', '아쉽', '실망',
    '짜증', '답답', '불만', '화나', '최악', '나쁘', '개선', '문제', '오류',
    '버그', '안됨', '안됩', '안되', '느림', '느리', '불편', '아쉬움'
]


def clean_data(df):
    """데이터 정리 - 광고/무관한 데이터 제거"""
    # 블라인드 광고 데이터 제거
    df = df[~df['text'].str.contains('블라인드에 광고하세요', na=False)]

    # 너무 짧은 리뷰 제거 (10자 미만)
    df = df[df['text'].str.len() >= 10]

    # 중복 제거
    df = df.drop_duplicates(subset=['text'])

    return df.reset_index(drop=True)


def extract_painpoints(text):
    """텍스트에서 페인포인트 카테고리 추출"""
    text = str(text).lower()
    found_categories = []

    for category, keywords in PAINPOINT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                found_categories.append(category)
                break  # 카테고리당 하나만 카운트

    return found_categories


def is_negative_review(text, rating=None):
    """부정적 리뷰인지 판단"""
    text = str(text).lower()

    # 별점이 있으면 활용
    if rating is not None and rating != '':
        try:
            if float(rating) <= 2:
                return True
        except:
            pass

    # 부정적 표현 카운트
    negative_count = sum(1 for indicator in NEGATIVE_INDICATORS if indicator in text)

    return negative_count >= 2


def analyze_painpoints(df):
    """페인포인트 분석 수행"""
    results = {
        'category_counts': Counter(),
        'negative_reviews': [],
        'category_examples': {cat: [] for cat in PAINPOINT_KEYWORDS.keys()},
        'rating_distribution': {}
    }

    for idx, row in df.iterrows():
        text = row['text']
        rating = row.get('rating', '')

        # 카테고리 추출
        categories = extract_painpoints(text)

        # 부정적 리뷰 판별
        is_negative = is_negative_review(text, rating)

        if is_negative and categories:
            for cat in categories:
                results['category_counts'][cat] += 1

                # 예시 저장 (카테고리당 최대 5개)
                if len(results['category_examples'][cat]) < 5:
                    results['category_examples'][cat].append({
                        'text': text[:200] + '...' if len(text) > 200 else text,
                        'rating': rating,
                        'platform': row['platform']
                    })

            results['negative_reviews'].append({
                'text': text,
                'rating': rating,
                'categories': categories,
                'platform': row['platform']
            })

    # 별점 분포 (Google Play만)
    gp_df = df[df['platform'] == 'Google Play']
    if not gp_df.empty:
        gp_df['rating'] = pd.to_numeric(gp_df['rating'], errors='coerce')
        results['rating_distribution'] = gp_df['rating'].value_counts().sort_index().to_dict()

    return results


def generate_report(df, results, output_path):
    """분석 보고서 생성"""
    report_lines = []

    report_lines.append("=" * 70)
    report_lines.append("링글(Ringle) 사용자 후기 페인포인트 분석 보고서")
    report_lines.append("=" * 70)
    report_lines.append("")

    # 1. 데이터 개요
    report_lines.append("## 1. 데이터 개요")
    report_lines.append(f"   - 총 리뷰 수: {len(df)}개")
    report_lines.append(f"   - 부정적 리뷰 수: {len(results['negative_reviews'])}개")
    report_lines.append(f"   - 부정적 리뷰 비율: {len(results['negative_reviews'])/len(df)*100:.1f}%")
    report_lines.append("")

    # 플랫폼별 분포
    report_lines.append("   플랫폼별 분포:")
    for platform, count in df['platform'].value_counts().items():
        report_lines.append(f"     - {platform}: {count}개")
    report_lines.append("")

    # 2. 별점 분포 (Google Play)
    if results['rating_distribution']:
        report_lines.append("## 2. Google Play 별점 분포")
        for rating, count in sorted(results['rating_distribution'].items()):
            bar = '█' * int(count / 5)
            report_lines.append(f"   {int(rating)}점: {bar} ({count}개)")
        report_lines.append("")

    # 3. 페인포인트 카테고리 순위
    report_lines.append("## 3. 페인포인트 카테고리 순위")
    report_lines.append("")

    total_painpoints = sum(results['category_counts'].values())
    for i, (category, count) in enumerate(results['category_counts'].most_common(), 1):
        pct = count / total_painpoints * 100 if total_painpoints > 0 else 0
        bar = '█' * int(pct / 2)
        report_lines.append(f"   {i}. {category}: {count}건 ({pct:.1f}%)")
        report_lines.append(f"      {bar}")
        report_lines.append("")

    # 4. 카테고리별 대표 불만 사례
    report_lines.append("## 4. 카테고리별 대표 불만 사례")
    report_lines.append("")

    for category in results['category_counts'].most_common():
        cat_name = category[0]
        examples = results['category_examples'][cat_name]

        if examples:
            report_lines.append(f"### [{cat_name}]")
            for i, ex in enumerate(examples[:3], 1):
                rating_str = f" (★{ex['rating']})" if ex['rating'] else ""
                report_lines.append(f"   {i}. [{ex['platform']}{rating_str}]")
                report_lines.append(f"      \"{ex['text']}\"")
                report_lines.append("")

    # 5. 주요 인사이트
    report_lines.append("## 5. 주요 인사이트 및 시사점")
    report_lines.append("")

    top_categories = results['category_counts'].most_common(3)
    if top_categories:
        report_lines.append("   가장 많이 언급된 페인포인트:")
        for i, (cat, count) in enumerate(top_categories, 1):
            report_lines.append(f"   {i}. {cat} ({count}건)")

            # 카테고리별 구체적 시사점
            if cat == '앱 UX/버그':
                report_lines.append("      → 앱 안정성/속도 개선 필요, 터치 반응 문제 해결 시급")
            elif cat == '가격':
                report_lines.append("      → 가격 대비 가치 인식 개선 필요, 할인/프로모션 전략 검토")
            elif cat == '예약 시스템':
                report_lines.append("      → 예약 경쟁 완화, 스케줄 알림 개선 필요")
            elif cat == '튜터 품질':
                report_lines.append("      → 튜터 품질 관리 강화, 매칭 알고리즘 개선")
            elif cat == '수업 효과':
                report_lines.append("      → 학습 효과 가시화, 진도 관리 기능 강화")

        report_lines.append("")

    # AI 전화영어 서비스 기획 시사점
    report_lines.append("## 6. AI 전화영어 서비스 기획 시사점")
    report_lines.append("")
    report_lines.append("   기존 링글 사용자 페인포인트 기반 AI 서비스 차별화 포인트:")
    report_lines.append("")
    report_lines.append("   1. [앱 안정성] AI 기반 서비스는 서버 안정성과 빠른 응답속도 필수")
    report_lines.append("   2. [가격 접근성] 휴먼 튜터 대비 합리적 가격 책정으로 진입장벽 낮추기")
    report_lines.append("   3. [즉시 예약] AI는 24/7 이용 가능 → 예약 경쟁 문제 해결")
    report_lines.append("   4. [일관된 품질] AI 튜터의 일관된 피드백 품질 보장")
    report_lines.append("   5. [연습 부담 감소] 사람 대면 부담 없이 편하게 연습 가능")
    report_lines.append("")

    report_lines.append("=" * 70)
    report_lines.append("분석 완료")
    report_lines.append("=" * 70)

    # 보고서 저장
    report_text = '\n'.join(report_lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    return report_text


def save_negative_reviews(results, output_path):
    """부정적 리뷰만 별도 CSV로 저장"""
    if results['negative_reviews']:
        neg_df = pd.DataFrame(results['negative_reviews'])
        neg_df['categories'] = neg_df['categories'].apply(lambda x: ', '.join(x))
        neg_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"   부정적 리뷰 저장: {output_path}")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🔍 링글(Ringle) 페인포인트 분석")
    print("=" * 60)

    # 데이터 로드
    data_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(data_dir, 'ringle_reviews.csv')

    if not os.path.exists(input_path):
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {input_path}")
        return

    df = pd.read_csv(input_path)
    print(f"\n📂 원본 데이터 로드: {len(df)}개 리뷰")

    # 데이터 정리
    df = clean_data(df)
    print(f"📂 정리 후 데이터: {len(df)}개 리뷰")

    # 정리된 데이터 저장
    cleaned_path = os.path.join(data_dir, 'ringle_reviews_cleaned.csv')
    df.to_csv(cleaned_path, index=False, encoding='utf-8-sig')
    print(f"   정리된 데이터 저장: {cleaned_path}")

    # 페인포인트 분석
    print("\n🔬 페인포인트 분석 중...")
    results = analyze_painpoints(df)

    # 보고서 생성
    report_path = os.path.join(data_dir, 'painpoint_report.txt')
    report = generate_report(df, results, report_path)
    print(f"\n📊 분석 보고서 저장: {report_path}")

    # 부정적 리뷰 저장
    negative_path = os.path.join(data_dir, 'negative_reviews.csv')
    save_negative_reviews(results, negative_path)

    # 보고서 출력
    print("\n" + report)

    return df, results


if __name__ == '__main__':
    main()
