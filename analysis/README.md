# 📊 영어학습 서비스 VOC 분석 결과

> 2026 링글 공모전 | 10개 서비스 7,604건 분석

---

## 🎯 핵심 발견

| # | 발견 | 근거 |
|---|------|------|
| 1 | **앱이 발목을 잡고 있다** | 앱 리뷰 부정률 38% vs 블로그 긍정률 80% |
| 2 | **스픽이 최대 경쟁자** | 스픽 99회 언급 (경쟁사 1위) |
| 3 | **비즈니스 영어가 기회** | 발표+면접+회의 = 976건 |

---

## 📁 폴더 구조

```
analysis/
│
├── 📄 01_final_reports/         ★ 최종 보고서 (여기부터 보세요!)
│   ├── 고객문제_분석보고서.docx       → 고객 문제 중심 분석
│   ├── VOC_분석_보고서_논문형식.docx  → 논문 형식 전체 분석
│   ├── VOC_분석_보고서_전체.docx     → 전체 요약
│   └── REPORT_FINAL.pdf             → PDF 버전
│
├── 🖥️ 02_dashboards/            대시보드 (웹 브라우저로 열기)
│   ├── DASHBOARD.html               → 요약 대시보드
│   ├── DASHBOARD_DETAIL.html        → 상세 대시보드
│   └── FULL_REPORT.html             → 8페이지 풀 리포트
│
├── 💡 03_insights/              인사이트 문서
│   ├── FINAL_INSIGHTS.md            → 최종 인사이트
│   ├── DEEP_ANALYSIS_REPORT.md      → 심층 분석
│   ├── QUALITATIVE_INSIGHTS.md      → 정성 분석
│   ├── INSIGHT_SUMMARY.md           → 인사이트 요약
│   └── REPORT_FINAL.md              → 마크다운 보고서
│
├── 🔬 04_detailed_analysis/     상세 분석 (주제별)
│   ├── market_overview/             → 시장 개요
│   │   └── 01_keyword_frequency.md
│   ├── company_comparison/          → 서비스 비교
│   │   ├── 01_tfidf_unique_keywords.md
│   │   └── 02_sentiment_distribution.md
│   └── deep_insights/               → 심층 인사이트
│       ├── 01_cooccurrence_network.md
│       ├── 02_churn_pattern.md
│       └── 03_hidden_needs.md
│
├── 📈 05_data/                  분석 데이터 (CSV)
│   ├── sentiment_distribution.csv   → 감성 분석 결과
│   ├── competitor_mentions.csv      → 경쟁사 언급
│   ├── hidden_needs.csv             → 숨겨진 니즈
│   ├── painpoint_structured.csv     → 페인포인트
│   ├── user_segments.csv            → 유저 세그먼트
│   ├── tfidf_unique_keywords.csv    → TF-IDF 키워드
│   ├── keyword_frequency_*.csv      → 키워드 빈도
│   └── ...
│
├── 📊 06_visualizations/        시각화 차트 (PNG)
│   ├── 01_wordcloud.png             → 워드클라우드
│   ├── 02_keyword_frequency.png     → 키워드 빈도
│   ├── 03_sentiment_distribution.png → 감성 분포
│   ├── 04_keyword_network.png       → 키워드 네트워크
│   ├── 05_positioning_map.png       → 포지셔닝 맵
│   └── ...
│
├── 🛠️ 07_scripts/               분석 스크립트 (Python)
│   ├── create_customer_problem_report.py
│   ├── create_academic_report.py
│   └── ...
│
└── 📚 08_methodology/           방법론 문서
    ├── ANALYSIS_FRAMEWORK.md        → 분석 프레임워크
    ├── DATA_COLLECTION_FRAMEWORK.md → 데이터 수집 가이드
    ├── REVIEW_ANALYSIS_BEST_PRACTICES.md → 분석 방법론
    └── VOC_ANALYSIS_REPORT.md       → VOC 분석 가이드
```

---

## 🚀 Quick Start

### 1. 최종 보고서 열기 (추천)
```bash
open 01_final_reports/고객문제_분석보고서.docx
```

### 2. 대시보드 열기
```bash
open 02_dashboards/DASHBOARD.html
```

### 3. 인사이트 확인
```bash
cat 03_insights/FINAL_INSIGHTS.md
```

---

## 📋 보고서 선택 가이드

| 목적 | 파일 | 경로 |
|------|------|------|
| **고객 문제 파악** | 고객문제 분석보고서 | `01_final_reports/` |
| **전체 분석 확인** | 논문형식 보고서 | `01_final_reports/` |
| **빠른 확인** | 대시보드 | `02_dashboards/DASHBOARD.html` |
| **데이터 확인** | CSV 파일들 | `05_data/` |
| **방법론 이해** | 프레임워크 문서 | `08_methodology/` |

---

## 📊 주요 데이터 설명

| 파일 | 내용 | 주요 컬럼 |
|------|------|----------|
| `sentiment_distribution.csv` | 서비스별 감성 분석 | company, positive_pct, negative_pct |
| `competitor_mentions.csv` | 경쟁사 언급 빈도 | service, competitor, mentions |
| `hidden_needs.csv` | 숨겨진 니즈 | need_type, count |
| `painpoint_structured.csv` | 페인포인트 구조화 | category, keyword, count |
| `user_segments.csv` | 유저 세그먼트 | segment, keywords, count |

---

## 📈 시각화 목록

| 파일 | 설명 |
|------|------|
| `01_wordcloud.png` | 전체 키워드 워드클라우드 |
| `02_keyword_frequency.png` | TOP 키워드 빈도 차트 |
| `03_sentiment_distribution.png` | 서비스별 감성 분포 |
| `04_keyword_network.png` | 키워드 동시출현 네트워크 |
| `05_positioning_map.png` | 경쟁 포지셔닝 맵 |
| `06_hidden_needs.png` | 숨겨진 니즈 차트 |

---

*Last Updated: 2026-01-18*
