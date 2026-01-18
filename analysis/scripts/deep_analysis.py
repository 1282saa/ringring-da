#!/usr/bin/env python3
"""
영어 학습 서비스 심층 분석 - 파트별 통계 및 정성 분석
2026 Ringle Competition Analysis
"""

import pandas as pd
import numpy as np
import re
import json
from collections import Counter, defaultdict
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 데이터 로드
base_path = "/Users/yeong-gwang/Documents/배움 오전 1.38.42/외부/공모전/2026/링글/프로젝트/data"

companies = ['ringle', 'cake', 'hackers', 'malhae', 'maxai', 'pagoda', 'santa', 'uphone', 'yanadu', 'carrot']
all_data = []

for company in companies:
    try:
        df = pd.read_csv(f"{base_path}/{company}/{company}_filtered.csv")
        all_data.append(df)
    except:
        try:
            df = pd.read_csv(f"{base_path}/{company}/{company}_master_data.csv")
            all_data.append(df)
        except:
            print(f"Warning: {company} data not found")

df = pd.concat(all_data, ignore_index=True)
print(f"총 데이터: {len(df)}건")

# ============================================================
# PART 1: 서비스 유형별 분석
# ============================================================

# 서비스 유형 분류
SERVICE_TYPES = {
    'AI_BASED': ['cake', 'santa', 'maxai'],       # AI 기반 서비스
    'HUMAN_TUTOR': ['ringle', 'uphone', 'carrot', 'pagoda'],  # 휴먼 튜터 서비스
    'CONTENT_BASED': ['yanadu', 'hackers', 'malhae']  # 콘텐츠/강의 기반
}

# 가격대 분류 (추정)
PRICE_TIER = {
    'PREMIUM': ['ringle'],        # 고가 (40분 3-5만원)
    'MID': ['uphone', 'carrot', 'pagoda', 'yanadu', 'hackers'],  # 중가
    'LOW': ['cake', 'santa', 'maxai', 'malhae']  # 저가/무료+프리미엄
}

# 학습 방식 분류
LEARNING_MODE = {
    'SYNCHRONOUS': ['ringle', 'uphone', 'carrot', 'pagoda'],  # 실시간 대화
    'ASYNCHRONOUS': ['cake', 'santa', 'yanadu', 'hackers', 'malhae', 'maxai']  # 비실시간
}

def classify_service(company):
    """서비스 유형 분류"""
    result = {'company': company}
    for type_name, companies in SERVICE_TYPES.items():
        if company.lower() in companies:
            result['service_type'] = type_name
    for tier, companies in PRICE_TIER.items():
        if company.lower() in companies:
            result['price_tier'] = tier
    for mode, companies in LEARNING_MODE.items():
        if company.lower() in companies:
            result['learning_mode'] = mode
    return result

# 서비스 유형별 통계 분석
part1_results = {
    'service_classification': [classify_service(c) for c in companies],
    'type_comparison': {}
}

for type_name, type_companies in SERVICE_TYPES.items():
    type_df = df[df['company'].str.lower().isin(type_companies)]
    if 'rating' in type_df.columns:
        ratings = type_df['rating'].dropna()
        if len(ratings) > 0:
            part1_results['type_comparison'][type_name] = {
                'count': len(type_df),
                'avg_rating': round(ratings.mean(), 2),
                'std_rating': round(ratings.std(), 2),
                'companies': type_companies
            }

print("\n=== PART 1: 서비스 유형별 분석 ===")
print(json.dumps(part1_results, indent=2, ensure_ascii=False))

# ============================================================
# PART 2: 사용자 여정 분석 (User Journey)
# ============================================================

# 사용자 여정 단계 패턴
JOURNEY_PATTERNS = {
    'AWARENESS': {
        'keywords': [r'알게\s*됐', r'처음\s*알', r'광고', r'추천.*받', r'검색.*해서'],
        'description': '인지 단계'
    },
    'CONSIDERATION': {
        'keywords': [r'고민', r'비교', r'선택', r'결정', r'어떤.*좋', r'vs', r'고르'],
        'description': '고려 단계'
    },
    'TRIAL': {
        'keywords': [r'처음.*써', r'시작.*했', r'무료.*체험', r'첫.*수업', r'가입.*했'],
        'description': '시작 단계'
    },
    'ACTIVE_USE': {
        'keywords': [r'\d+개월', r'\d+년.*사용', r'계속.*하고', r'매일', r'꾸준히'],
        'description': '활성 사용'
    },
    'LOYALTY': {
        'keywords': [r'최고', r'추천.*합니다', r'강추', r'만족', r'좋아요'],
        'description': '충성 단계'
    },
    'CHURN_RISK': {
        'keywords': [r'그만.*두', r'취소', r'환불', r'후회', r'실망', r'안 쓸'],
        'description': '이탈 위험'
    }
}

def detect_journey_stage(text):
    """텍스트에서 사용자 여정 단계 감지"""
    if not isinstance(text, str):
        return []
    stages = []
    for stage, info in JOURNEY_PATTERNS.items():
        for pattern in info['keywords']:
            if re.search(pattern, text, re.IGNORECASE):
                stages.append(stage)
                break
    return stages

# 회사별 여정 단계 분포 분석
journey_by_company = defaultdict(lambda: defaultdict(int))
journey_examples = defaultdict(lambda: defaultdict(list))

for idx, row in df.iterrows():
    text = str(row.get('text', ''))
    company = str(row.get('company', '')).upper()
    stages = detect_journey_stage(text)
    for stage in stages:
        journey_by_company[company][stage] += 1
        if len(journey_examples[company][stage]) < 3:
            journey_examples[company][stage].append(text[:200])

part2_results = {
    'journey_distribution': dict(journey_by_company),
    'methodology': {
        'patterns_used': len(JOURNEY_PATTERNS),
        'stages': list(JOURNEY_PATTERNS.keys())
    }
}

print("\n=== PART 2: 사용자 여정 분석 ===")
for company in ['RINGLE', 'CAKE', 'YANADU', 'UPHONE']:
    if company in journey_by_company:
        print(f"\n{company}:")
        for stage, count in sorted(journey_by_company[company].items(), key=lambda x: -x[1]):
            print(f"  {stage}: {count}건")

# ============================================================
# PART 3: 심리적 동기 유형별 분석
# ============================================================

MOTIVATION_TYPES = {
    'CAREER_DRIVEN': {
        'patterns': [
            r'(승진|이직|취업|면접|이력서|resume|자소서).*영어',
            r'영어.*(승진|이직|취업|면접)',
            r'(회사|직장|업무|비즈니스).*영어',
            r'외국계.*회사',
            r'글로벌.*기업'
        ],
        'description': '커리어 동기 - 직업적 성장을 위한 영어'
    },
    'SHAME_AVOIDANCE': {
        'patterns': [
            r'(창피|부끄러|민망|쪽팔|당황)',
            r'(못.*말|말.*못|말문.*막)',
            r'외국인.*앞',
            r'(긴장|떨리|떨려)'
        ],
        'description': '수치심 회피 - 창피함을 피하고 싶은 동기'
    },
    'SELF_ACTUALIZATION': {
        'patterns': [
            r'(꿈|목표|버킷리스트)',
            r'외국.*살|이민|해외.*생활',
            r'(성장|발전|나아지)',
            r'자기.*개발'
        ],
        'description': '자아실현 - 더 나은 자신이 되고 싶은 동기'
    },
    'PARENTING': {
        'patterns': [
            r'(아이|자녀|애들|우리.*애)',
            r'(엄마|아빠|부모).*영어',
            r'같이.*공부',
            r'가르치.*영어'
        ],
        'description': '양육 동기 - 자녀 교육 관련'
    },
    'TRAVEL': {
        'patterns': [
            r'(여행|해외.*갈|외국.*갈)',
            r'(공항|호텔|식당).*영어',
            r'자유.*여행'
        ],
        'description': '여행 동기 - 해외 여행을 위한 영어'
    },
    'ACADEMIC': {
        'patterns': [
            r'(유학|MBA|대학원|석사|박사)',
            r'(토익|토플|아이엘츠|IELTS|TOEFL)',
            r'(학교|시험|점수)'
        ],
        'description': '학업 동기 - 시험/유학 준비'
    }
}

# 심리적 장벽 유형
BARRIER_TYPES = {
    'COST_BARRIER': {
        'patterns': [r'(비싸|가격|돈|부담|비용|환불|가성비)'],
        'description': '비용 장벽'
    },
    'TIME_BARRIER': {
        'patterns': [r'(시간.*없|바빠|시간.*부족|짬짬이)'],
        'description': '시간 장벽'
    },
    'CONFIDENCE_BARRIER': {
        'patterns': [r'(자신.*없|두려|겁이|못할 것|무서)'],
        'description': '자신감 장벽'
    },
    'CONTINUITY_BARRIER': {
        'patterns': [r'(작심삼일|꾸준.*못|포기|중도|그만)'],
        'description': '지속성 장벽'
    },
    'EFFECTIVENESS_DOUBT': {
        'patterns': [r'(효과.*없|실력.*안|도움.*안|의미.*없)'],
        'description': '효과 의심'
    }
}

def analyze_motivation(text):
    """텍스트에서 동기 유형 분석"""
    if not isinstance(text, str):
        return []
    found = []
    for mtype, info in MOTIVATION_TYPES.items():
        for pattern in info['patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                found.append(mtype)
                break
    return found

def analyze_barrier(text):
    """텍스트에서 장벽 유형 분석"""
    if not isinstance(text, str):
        return []
    found = []
    for btype, info in BARRIER_TYPES.items():
        for pattern in info['patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                found.append(btype)
                break
    return found

# 회사별 동기/장벽 분석
motivation_by_company = defaultdict(lambda: defaultdict(int))
barrier_by_company = defaultdict(lambda: defaultdict(int))
motivation_quotes = defaultdict(lambda: defaultdict(list))
barrier_quotes = defaultdict(lambda: defaultdict(list))

for idx, row in df.iterrows():
    text = str(row.get('text', ''))
    company = str(row.get('company', '')).upper()

    motivations = analyze_motivation(text)
    barriers = analyze_barrier(text)

    for m in motivations:
        motivation_by_company[company][m] += 1
        if len(motivation_quotes[company][m]) < 3:
            motivation_quotes[company][m].append(text[:300])

    for b in barriers:
        barrier_by_company[company][b] += 1
        if len(barrier_quotes[company][b]) < 3:
            barrier_quotes[company][b].append(text[:300])

part3_results = {
    'motivation_distribution': dict(motivation_by_company),
    'barrier_distribution': dict(barrier_by_company),
    'motivation_types': {k: v['description'] for k, v in MOTIVATION_TYPES.items()},
    'barrier_types': {k: v['description'] for k, v in BARRIER_TYPES.items()}
}

print("\n=== PART 3: 심리적 동기 분석 ===")
for company in ['RINGLE', 'CAKE', 'YANADU', 'UPHONE']:
    if company in motivation_by_company:
        print(f"\n{company} 동기 분포:")
        for mtype, count in sorted(motivation_by_company[company].items(), key=lambda x: -x[1]):
            print(f"  {MOTIVATION_TYPES[mtype]['description']}: {count}건")

# ============================================================
# PART 4: 통계적 검증 및 방법론
# ============================================================

print("\n=== PART 4: 통계적 검증 ===")

# 4.1 회사별 평점 차이 통계 검정 (ANOVA)
company_ratings = {}
for company in companies:
    company_df = df[df['company'].str.lower() == company]
    if 'rating' in company_df.columns:
        ratings = company_df['rating'].dropna()
        if len(ratings) > 0:
            company_ratings[company.upper()] = ratings.values

# ANOVA 검정
if len(company_ratings) >= 2:
    rating_groups = list(company_ratings.values())
    f_stat, p_value = stats.f_oneway(*rating_groups)
    print(f"\n1. 회사간 평점 차이 (One-way ANOVA)")
    print(f"   F-statistic: {f_stat:.4f}")
    print(f"   p-value: {p_value:.6f}")
    print(f"   결론: {'통계적으로 유의미한 차이 존재 (p<0.05)' if p_value < 0.05 else '유의미한 차이 없음'}")

# 4.2 서비스 유형별 평점 차이 (t-test)
ai_ratings = []
human_ratings = []

for company, ratings in company_ratings.items():
    if company.lower() in SERVICE_TYPES['AI_BASED']:
        ai_ratings.extend(ratings)
    elif company.lower() in SERVICE_TYPES['HUMAN_TUTOR']:
        human_ratings.extend(ratings)

if len(ai_ratings) > 0 and len(human_ratings) > 0:
    t_stat, p_value = stats.ttest_ind(ai_ratings, human_ratings)
    print(f"\n2. AI vs 휴먼튜터 평점 비교 (Independent t-test)")
    print(f"   AI 기반 평균: {np.mean(ai_ratings):.2f} (n={len(ai_ratings)})")
    print(f"   휴먼 튜터 평균: {np.mean(human_ratings):.2f} (n={len(human_ratings)})")
    print(f"   t-statistic: {t_stat:.4f}")
    print(f"   p-value: {p_value:.6f}")
    print(f"   Cohen's d (효과크기): {abs(np.mean(ai_ratings) - np.mean(human_ratings)) / np.sqrt((np.std(ai_ratings)**2 + np.std(human_ratings)**2)/2):.3f}")

# 4.3 긍정/부정 비율 카이제곱 검정
print(f"\n3. 긍정률 차이 검정 (Chi-square test)")
contingency_data = []
for company, ratings in company_ratings.items():
    positive = sum(1 for r in ratings if r >= 4)
    negative = sum(1 for r in ratings if r <= 2)
    contingency_data.append([positive, negative])

if len(contingency_data) >= 2:
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_data)
    print(f"   Chi-square: {chi2:.4f}")
    print(f"   p-value: {p_value:.6f}")
    print(f"   자유도: {dof}")

# 4.4 신뢰구간 계산
print(f"\n4. 회사별 평점 95% 신뢰구간")
for company, ratings in sorted(company_ratings.items()):
    mean = np.mean(ratings)
    sem = stats.sem(ratings)
    ci = stats.t.interval(0.95, len(ratings)-1, loc=mean, scale=sem)
    print(f"   {company}: {mean:.2f} [{ci[0]:.2f}, {ci[1]:.2f}]")

# ============================================================
# 최종 결과 저장
# ============================================================

final_report = {
    'part1_service_types': part1_results,
    'part2_user_journey': part2_results,
    'part3_psychology': part3_results,
    'part4_statistics': {
        'methodology': {
            'anova': 'One-way ANOVA for comparing means across companies',
            'ttest': 'Independent t-test for AI vs Human tutor comparison',
            'chi_square': 'Chi-square test for proportion comparison',
            'confidence_interval': '95% CI using t-distribution'
        },
        'sample_sizes': {company: len(ratings) for company, ratings in company_ratings.items()}
    },
    'motivation_quotes': dict(motivation_quotes),
    'barrier_quotes': dict(barrier_quotes),
    'journey_examples': dict(journey_examples)
}

# JSON 저장
with open(f"{base_path}/phase/DEEP_ANALYSIS_RESULTS.json", 'w', encoding='utf-8') as f:
    json.dump(final_report, f, ensure_ascii=False, indent=2, default=str)

print(f"\n\n=== 분석 완료 ===")
print(f"결과 저장: {base_path}/phase/DEEP_ANALYSIS_RESULTS.json")
