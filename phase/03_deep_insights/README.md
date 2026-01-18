# Level 3: 심층 인사이트

> "왜 그런가? 링글에게 어떤 의미인가?"

---

## 분석 목록

| # | 분석 | 파일 | 상태 |
|---|------|------|------|
| 1 | 키워드 동시출현 네트워크 | [01_cooccurrence_network.md](./01_cooccurrence_network.md) | ✅ |
| 2 | 이탈/전환 패턴 | [02_churn_pattern.md](./02_churn_pattern.md) | ✅ |
| 3 | 숨겨진 니즈 | [03_hidden_needs.md](./03_hidden_needs.md) | ✅ |

---

## 핵심 발견

### 1. 키워드 네트워크
- "영어"가 중심 허브
- "시간"이 거의 모든 키워드와 연결 → **시간 효율성이 핵심 가치**
- "가격-시간-효과" 삼각 구조

### 2. 이탈/전환 패턴
| 링글에서 가장 많이 언급되는 경쟁사 |
|----------------------------------|
| 스픽 (99회) - AI 무제한 vs 튜터 품질 |
| 말해보카 (99회) - 어휘 학습 비교 |
| 캠블리 (90회) - 화상영어 직접 경쟁 |

### 3. 숨겨진 니즈 Top 5
| 니즈 | 빈도 | AI 기회 |
|------|------|---------|
| 목표 설정 | 893건 | AI 맞춤 플랜 |
| 업종별 영어 | 804건 | 산업별 시나리오 |
| 발표 연습 | 452건 | AI 발표 코치 |
| 면접 영어 | 288건 | AI 면접관 |
| 회의 영어 | 236건 | AI 회의 롤플레이 |

---

## 시각화

| 시각화 | 파일 |
|--------|------|
| 키워드 네트워크 | [visualizations/04_keyword_network.png](./visualizations/04_keyword_network.png) |
| 경쟁사 히트맵 | [visualizations/05_competitor_heatmap.png](./visualizations/05_competitor_heatmap.png) |
| 숨겨진 니즈 차트 | [visualizations/06_hidden_needs.png](./visualizations/06_hidden_needs.png) |

---

## 데이터 파일

| 파일 | 설명 |
|------|------|
| `data/cooccurrence_network.csv` | 키워드 동시출현 데이터 |
| `data/competitor_mentions.csv` | 경쟁사 언급 데이터 |
| `data/hidden_needs.csv` | 숨겨진 니즈 빈도 |

---

[← Level 2](../02_company_comparison/README.md) | [상위 폴더](../README.md) | [최종 리포트 →](../FINAL_INSIGHTS.md)
