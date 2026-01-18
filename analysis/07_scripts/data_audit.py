#!/usr/bin/env python3
"""
데이터 수집 현황 및 품질 감사 (Audit)
"""

import pandas as pd
import numpy as np
import os
from collections import defaultdict
import json

base_path = "/Users/yeong-gwang/Documents/배움 오전 1.38.42/외부/공모전/2026/링글/프로젝트/data"

companies = ['ringle', 'cake', 'hackers', 'malhae', 'maxai', 'pagoda', 'santa', 'uphone', 'yanadu', 'carrot']

# 결과 저장용
audit_results = {
    'data_collection': {},
    'column_schema': {},
    'missing_values': {},
    'distribution': {
        'by_company': {},
        'by_source': {},
        'by_platform': {}
    },
    'quality_issues': []
}

# 1. 전체 데이터 로드 및 분석
all_data = []
raw_files = []

for company in companies:
    # master_data 또는 filtered 파일 찾기
    master_path = f"{base_path}/{company}/{company}_master_data.csv"
    filtered_path = f"{base_path}/{company}/{company}_filtered.csv"

    if os.path.exists(filtered_path):
        df = pd.read_csv(filtered_path)
        raw_files.append({'company': company, 'file': 'filtered', 'rows': len(df)})
        all_data.append(df)
    elif os.path.exists(master_path):
        df = pd.read_csv(master_path)
        raw_files.append({'company': company, 'file': 'master', 'rows': len(df)})
        all_data.append(df)

# 전체 데이터 병합
df_all = pd.concat(all_data, ignore_index=True)

print("=" * 60)
print("1. 데이터 수집 현황 (Data Collection Summary)")
print("=" * 60)

# 회사별 데이터 수
print("\n[회사별 데이터 수]")
company_counts = df_all['company'].value_counts()
for company, count in company_counts.items():
    print(f"  {company.upper()}: {count:,}건")
    audit_results['distribution']['by_company'][company.upper()] = count

print(f"\n  총 데이터: {len(df_all):,}건")

# 소스 타입별 분포
print("\n[데이터 소스별 분포]")
if 'source_type' in df_all.columns:
    source_counts = df_all['source_type'].value_counts()
    for source, count in source_counts.items():
        pct = count / len(df_all) * 100
        print(f"  {source}: {count:,}건 ({pct:.1f}%)")
        audit_results['distribution']['by_source'][source] = count

# 플랫폼별 분포
print("\n[플랫폼별 분포]")
if 'source_platform' in df_all.columns:
    platform_counts = df_all['source_platform'].value_counts()
    for platform, count in platform_counts.items():
        pct = count / len(df_all) * 100
        print(f"  {platform}: {count:,}건 ({pct:.1f}%)")
        audit_results['distribution']['by_platform'][platform] = count

print("\n" + "=" * 60)
print("2. 컬럼 스키마 (Column Schema)")
print("=" * 60)

print(f"\n총 컬럼 수: {len(df_all.columns)}")
print("\n[컬럼 상세]")
for col in df_all.columns:
    dtype = str(df_all[col].dtype)
    non_null = df_all[col].notna().sum()
    null_pct = (1 - non_null / len(df_all)) * 100
    unique = df_all[col].nunique()

    print(f"  {col}")
    print(f"    - 타입: {dtype}")
    print(f"    - 유효값: {non_null:,}건 (결측: {null_pct:.1f}%)")
    print(f"    - 고유값: {unique:,}개")

    audit_results['column_schema'][col] = {
        'dtype': dtype,
        'non_null': int(non_null),
        'null_pct': round(null_pct, 2),
        'unique': int(unique)
    }

print("\n" + "=" * 60)
print("3. 결측치 분석 (Missing Values)")
print("=" * 60)

missing_summary = df_all.isnull().sum()
missing_pct = (df_all.isnull().sum() / len(df_all) * 100).round(2)

print("\n[결측치 현황]")
for col in df_all.columns:
    if missing_summary[col] > 0:
        print(f"  {col}: {missing_summary[col]:,}건 ({missing_pct[col]:.1f}%)")
        audit_results['missing_values'][col] = {
            'count': int(missing_summary[col]),
            'percentage': float(missing_pct[col])
        }

# rating 결측 분석
if 'rating' in df_all.columns:
    print("\n[rating 결측 상세 - 소스별]")
    for source in df_all['source_type'].unique():
        source_df = df_all[df_all['source_type'] == source]
        rating_null = source_df['rating'].isnull().sum()
        pct = rating_null / len(source_df) * 100 if len(source_df) > 0 else 0
        print(f"  {source}: {rating_null:,}건 결측 ({pct:.1f}%)")

print("\n" + "=" * 60)
print("4. 회사×소스 교차 분포")
print("=" * 60)

if 'source_type' in df_all.columns:
    cross_tab = pd.crosstab(df_all['company'], df_all['source_type'])
    print("\n" + cross_tab.to_string())

    # 저장
    audit_results['cross_distribution'] = cross_tab.to_dict()

print("\n" + "=" * 60)
print("5. 데이터 품질 이슈")
print("=" * 60)

# 중복 체크
if 'text' in df_all.columns:
    duplicates = df_all['text'].duplicated().sum()
    print(f"\n[텍스트 중복]: {duplicates:,}건 ({duplicates/len(df_all)*100:.1f}%)")
    if duplicates > 0:
        audit_results['quality_issues'].append({
            'issue': 'duplicate_text',
            'count': int(duplicates),
            'severity': 'medium'
        })

# 너무 짧은 텍스트
if 'text' in df_all.columns:
    short_text = (df_all['text'].str.len() < 10).sum()
    print(f"[짧은 텍스트 (<10자)]: {short_text:,}건")
    if short_text > 100:
        audit_results['quality_issues'].append({
            'issue': 'short_text',
            'count': int(short_text),
            'severity': 'low'
        })

# rating 범위 체크
if 'rating' in df_all.columns:
    invalid_rating = ((df_all['rating'] < 1) | (df_all['rating'] > 5)).sum()
    print(f"[비정상 rating (1-5 범위 외)]: {invalid_rating:,}건")

print("\n" + "=" * 60)
print("6. 통계 요약")
print("=" * 60)

if 'rating' in df_all.columns:
    print(f"\n[rating 통계]")
    print(f"  평균: {df_all['rating'].mean():.2f}")
    print(f"  중앙값: {df_all['rating'].median():.1f}")
    print(f"  표준편차: {df_all['rating'].std():.2f}")
    print(f"  최소: {df_all['rating'].min():.0f}")
    print(f"  최대: {df_all['rating'].max():.0f}")

if 'text' in df_all.columns:
    print(f"\n[text 길이 통계]")
    text_len = df_all['text'].str.len()
    print(f"  평균: {text_len.mean():.0f}자")
    print(f"  중앙값: {text_len.median():.0f}자")
    print(f"  최대: {text_len.max():.0f}자")

# JSON 저장
with open(f"{base_path}/phase/DATA_AUDIT_RESULTS.json", 'w', encoding='utf-8') as f:
    json.dump(audit_results, f, ensure_ascii=False, indent=2, default=str)

print(f"\n\n결과 저장: {base_path}/phase/DATA_AUDIT_RESULTS.json")
