# Phase 1: 영어학습 서비스 리뷰 데이터 분석

> 2026 링글 공모전 | 데이터 기반 인사이트 도출
> 분석 기간: 2026-01-18

---

## 폴더 구조

```
phase/
│
├── README.md                    ← 현재 문서 (네비게이션)
├── ANALYSIS_FRAMEWORK.md        ← 분석 프레임워크 & 진행 상황
├── FINAL_INSIGHTS.md            ← ⭐ 최종 인사이트 리포트
│
├── 01_market_overview/          ← Level 1: 시장 전체 조감
│   ├── 01_keyword_frequency.md  ← 키워드 빈도 분석
│   └── data/
│       ├── keyword_frequency_cleaned.csv
│       └── category_frequency_detailed.csv
│
├── 02_company_comparison/       ← Level 2: 회사별 특성 비교
│   ├── 01_tfidf_unique_keywords.md  ← TF-IDF 고유 키워드
│   ├── 02_sentiment_distribution.md ← 감정 분포 비교
│   └── data/
│       ├── tfidf_unique_keywords.csv
│       └── sentiment_distribution.csv
│
├── 03_deep_insights/            ← Level 3: 심층 인사이트
│   ├── 01_cooccurrence_network.md   ← 키워드 동시출현 네트워크
│   ├── 02_churn_pattern.md          ← 이탈/전환 패턴
│   ├── 03_hidden_needs.md           ← 숨겨진 니즈
│   └── data/
│       ├── cooccurrence_network.csv
│       ├── competitor_mentions.csv
│       └── hidden_needs.csv
│
└── visualizations/              ← 시각화 자료
    ├── 01_wordcloud.png             ← 워드클라우드
    ├── 02_keyword_frequency.png     ← 키워드 빈도 차트
    ├── 03_sentiment_distribution.png← 감정 분포 차트
    ├── 04_keyword_network.png       ← 동시출현 네트워크
    ├── 05_competitor_heatmap.png    ← 경쟁사 언급 히트맵
    └── 06_hidden_needs.png          ← 숨겨진 니즈 차트
```

---

## 빠른 네비게이션

### 핵심 문서
| 문서 | 설명 | 바로가기 |
|------|------|----------|
| 최종 인사이트 | 전체 분석 결과 요약 | [FINAL_INSIGHTS.md](./FINAL_INSIGHTS.md) |
| 분석 프레임워크 | 방법론 및 진행 상황 | [ANALYSIS_FRAMEWORK.md](./ANALYSIS_FRAMEWORK.md) |

### Level별 분석
| Level | 주제 | 핵심 질문 | 문서 |
|-------|------|-----------|------|
| **L1** | 시장 전체 조감 | 시장에서 뭘 이야기하나? | [01_keyword_frequency.md](./01_market_overview/01_keyword_frequency.md) |
| **L2-1** | 회사별 고유 키워드 | 각 회사 특색은? | [01_tfidf_unique_keywords.md](./02_company_comparison/01_tfidf_unique_keywords.md) |
| **L2-2** | 감정 분포 비교 | 어디가 잘하고 못하나? | [02_sentiment_distribution.md](./02_company_comparison/02_sentiment_distribution.md) |
| **L3-1** | 키워드 네트워크 | 무엇이 연관되어 있나? | [01_cooccurrence_network.md](./03_deep_insights/01_cooccurrence_network.md) |
| **L3-2** | 이탈/전환 패턴 | 어디서 어디로 가나? | [02_churn_pattern.md](./03_deep_insights/02_churn_pattern.md) |
| **L3-3** | 숨겨진 니즈 | 사용자가 원하는 것은? | [03_hidden_needs.md](./03_deep_insights/03_hidden_needs.md) |

### 시각화
| # | 시각화 | 파일 |
|---|--------|------|
| 1 | 워드클라우드 | [01_wordcloud.png](./visualizations/01_wordcloud.png) |
| 2 | 키워드 빈도 | [02_keyword_frequency.png](./visualizations/02_keyword_frequency.png) |
| 3 | 감정 분포 | [03_sentiment_distribution.png](./visualizations/03_sentiment_distribution.png) |
| 4 | 키워드 네트워크 | [04_keyword_network.png](./visualizations/04_keyword_network.png) |
| 5 | 경쟁사 히트맵 | [05_competitor_heatmap.png](./visualizations/05_competitor_heatmap.png) |
| 6 | 숨겨진 니즈 | [06_hidden_needs.png](./visualizations/06_hidden_needs.png) |

---

## 데이터 파일 목록

| 파일 | 위치 | 설명 |
|------|------|------|
| `keyword_frequency_cleaned.csv` | L1/data | 정제된 키워드 빈도 |
| `category_frequency_detailed.csv` | L1/data | 카테고리별 상세 빈도 |
| `tfidf_unique_keywords.csv` | L2/data | 회사별 TF-IDF 점수 |
| `sentiment_distribution.csv` | L2/data | 회사별 감정 분포 |
| `cooccurrence_network.csv` | L3/data | 키워드 동시출현 데이터 |
| `competitor_mentions.csv` | L3/data | 경쟁사 언급 데이터 |
| `hidden_needs.csv` | L3/data | 숨겨진 니즈 빈도 |

---

## 분석 완료 현황

| 단계 | 상태 | 완료일 |
|------|------|--------|
| 데이터 수집 (10개 서비스) | ✅ | 2026-01-18 |
| 데이터 정제 (허수 필터링) | ✅ | 2026-01-18 |
| Level 1: 키워드 빈도 | ✅ | 2026-01-18 |
| Level 2-1: TF-IDF 분석 | ✅ | 2026-01-18 |
| Level 2-2: 감정 분포 | ✅ | 2026-01-18 |
| Level 3-1: 동시출현 네트워크 | ✅ | 2026-01-18 |
| Level 3-2: 이탈/전환 패턴 | ✅ | 2026-01-18 |
| Level 3-3: 숨겨진 니즈 | ✅ | 2026-01-18 |
| 시각화 | ✅ | 2026-01-18 |
| 최종 리포트 | ✅ | 2026-01-18 |

---

## 핵심 인사이트 요약

### 링글 현황
- 긍정률 66.6% (10개 서비스 중 6위)
- 앱 리뷰 부정률 38% → **앱 품질 개선 시급**

### 시장 기회
- 시험 준비 시장(토익) 대규모 → **AI 모의고사**
- 비즈니스 영어 니즈 높음 → **발표/회의/면접 AI**

### 경쟁 위협
- 스픽: AI 무제한 + 저가로 가격 민감 사용자 흡수
- 캠블리: 즉시 연결 + 유연성으로 캐주얼 사용자 흡수

---

*Phase 1 분석 완료 | Claude Code*
