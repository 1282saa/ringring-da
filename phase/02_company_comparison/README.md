# Level 2: 회사별 특성 비교

> "각 회사는 어떻게 다른가? 어떤 특색이 있는가?"

---

## 분석 목록

| # | 분석 | 파일 | 상태 |
|---|------|------|------|
| 1 | TF-IDF 고유 키워드 | [01_tfidf_unique_keywords.md](./01_tfidf_unique_keywords.md) | ✅ |
| 2 | 감정 분포 비교 | [02_sentiment_distribution.md](./02_sentiment_distribution.md) | ✅ |
| 3 | 포지셔닝 맵 | - | ⏳ |

---

## 핵심 발견

### 회사별 고유 키워드
| 회사 | 고유 키워드 | 포지션 |
|------|------------|--------|
| **Ringle** | 명문대, 튜터, 커리어 | 프리미엄 커리어 영어 |
| **Cake** | 영상, 표현, 유튜브 | 콘텐츠 기반 표현 학습 |
| **Hackers** | 토익, 시험, 파트 | 토익 시험 전문 |
| **MaxAI** | 대화, 영어회화, 원어민 | AI 대화 영어회화 |

### 감정 분포 랭킹
| 순위 | 회사 | 긍정률 | 건강도 |
|------|------|--------|--------|
| 1 | Carrot | 87.6% | 🟢 매우 건강 |
| 6 | **Ringle** | 66.6% | 🟡 주의 필요 |
| 10 | Pagoda | 40.3% | 🔴 위험 |

---

## 시각화

| 시각화 | 파일 |
|--------|------|
| 감정 분포 차트 | [visualizations/03_sentiment_distribution.png](./visualizations/03_sentiment_distribution.png) |

---

## 데이터 파일

| 파일 | 설명 |
|------|------|
| `data/tfidf_unique_keywords.csv` | 회사별 TF-IDF 점수 |
| `data/sentiment_distribution.csv` | 회사별 감정 분포 |

---

[← Level 1](../01_market_overview/README.md) | [상위 폴더](../README.md) | [다음: Level 3 →](../03_deep_insights/README.md)
