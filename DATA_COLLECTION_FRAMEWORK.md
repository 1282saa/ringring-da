# Data Collection Framework for English Learning Service Analysis

## Project Overview

**Objective**: Collect and analyze user-generated content across 10 English learning services in Korea for competitive analysis and AARRR framework evaluation.

**Target Services**:
| Service | Type | Target Audience |
|---------|------|-----------------|
| Ringle | 1:1 Video English | Business professionals |
| MaxAI | AI Speaking Coach | General learners |
| Santa (Riiid) | AI TOEIC Prep | Test takers |
| Malhae Voca | Vocabulary & Speaking | Beginners |
| Cake | Short-form Video Learning | Casual learners |
| Hackers | Test Prep (TOEIC/TOEFL) | Test takers |
| Yanadu | Online English Course | General learners |
| Carrot English | Phone/Video English | Business professionals |
| Pagoda | Language Academy | All levels |
| Uphone (Min Byeongcheol) | Phone English | Business professionals |

**Final Dataset**: 9,169 records across 10 services

---

## 1. Data Collection Architecture

### 1.1 Data Source Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA SOURCE TAXONOMY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  APP REVIEW  │  │    BLOG      │  │    NEWS      │          │
│  │  (60.8%)     │  │  (12.4%)     │  │  (5.9%)      │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │ • App Store  │  │ • Naver Blog │  │ • Daum News  │          │
│  │ • Play Store │  │ • Brunch     │  │ • Naver News │          │
│  │              │  │ • Tistory    │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │  COMMUNITY   │  │     SNS      │                            │
│  │  (9.6%)      │  │  (9.4%)      │                            │
│  ├──────────────┤  ├──────────────┤                            │
│  │ • Clien      │  │ • YouTube    │                            │
│  │ • Blind      │  │              │                            │
│  │ • DCinside   │  │              │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Unified Data Schema

All collected data follows a standardized 12-column schema:

```python
MASTER_SCHEMA = {
    'data_id': str,          # Unique identifier: {service}_{platform}_{uuid}
    'company': str,          # Service name (lowercase)
    'source_type': str,      # Category: app_review|blog|news|community|sns
    'source_platform': str,  # Specific platform: appstore|playstore|brunch|etc
    'search_keyword': str,   # Search query used for collection
    'title': str,            # Content title
    'text': str,             # Main content body (max 5000 chars)
    'rating': float,         # Rating score (1-5, nullable)
    'author': str,           # Author name
    'date': str,             # Publication date (YYYY-MM-DD)
    'url': str,              # Source URL
    'collected_at': str      # Collection timestamp (ISO format)
}
```

---

## 2. Collection Methodology by Source Type

### 2.1 App Store Reviews

#### 2.1.1 Google Play Store

**Tool**: `google-play-scraper` Python library

**Process**:
```python
from google_play_scraper import app, reviews, Sort

# Step 1: Get app metadata
app_info = app(app_id, lang='ko', country='kr')

# Step 2: Collect reviews with pagination
all_reviews = []
result, token = reviews(
    app_id,
    lang='ko',
    country='kr',
    sort=Sort.NEWEST,
    count=500
)
all_reviews.extend(result)

# Step 3: Continue with continuation token
while token:
    result, token = reviews(
        app_id,
        continuation_token=token,
        count=500
    )
    all_reviews.extend(result)
```

**App IDs Collected**:
| Service | Play Store App ID |
|---------|-------------------|
| Ringle | com.ringle.ringle_android |
| MaxAI | com.studymax.maxai_b2c |
| Santa | co.riiid.vida |
| Malhae | kr.epopsoft.word |
| Cake | me.mycake |
| Hackers | com.hackers.toeic |
| Yanadu | com.yanadu.android |
| Carrot | com.carrotenglish |
| Pagoda | com.pagoda.one.srunning |
| Uphone | com.bcm.uphone3.android |

#### 2.1.2 Apple App Store

**Tool**: iTunes RSS Feed API

**Process**:
```python
import requests

app_id = "1234567890"
all_reviews = []

for page in range(1, 11):
    url = f"https://itunes.apple.com/kr/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
    response = requests.get(url)
    data = response.json()

    entries = data.get('feed', {}).get('entry', [])
    for entry in entries:
        if 'im:rating' in entry:
            review = {
                'title': entry['title']['label'],
                'text': entry['content']['label'],
                'rating': int(entry['im:rating']['label']),
                'author': entry['author']['name']['label'],
                'date': entry['updated']['label'][:10]
            }
            all_reviews.append(review)
```

---

### 2.2 Blog Content

#### 2.2.1 Naver Blog

**Tool**: Selenium WebDriver

**Process**:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_naver_blog(keyword, max_results=30):
    encoded = urllib.parse.quote(keyword)
    url = f"https://search.naver.com/search.naver?where=blog&query={encoded}"

    driver.get(url)
    time.sleep(2)

    items = driver.find_elements(By.CSS_SELECTOR, '.total_wrap')
    results = []

    for item in items[:max_results]:
        title_elem = item.find_element(By.CSS_SELECTOR, '.title_link')
        results.append({
            'title': title_elem.text,
            'url': title_elem.get_attribute('href')
        })

    return results
```

#### 2.2.2 Brunch

**Tool**: Selenium WebDriver

**Selector**: `a[href*="@@"]` (Brunch article URL pattern)

**Process**:
```python
def scrape_brunch(keyword, max_results=30):
    encoded = urllib.parse.quote(keyword)
    url = f"https://brunch.co.kr/search?q={encoded}"

    driver.get(url)
    time.sleep(3)

    # Brunch articles have unique URL pattern with @@
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="@@"]')

    results = []
    for link in links[:max_results]:
        href = link.get_attribute('href')
        title = link.text
        if href and '@@' in href:
            results.append({'title': title, 'url': href})

    return results
```

#### 2.2.3 Tistory

**Tool**: Selenium via Naver Web Search

**Process**:
```python
def scrape_tistory(keyword, max_results=30):
    # Search Tistory via Naver
    encoded = urllib.parse.quote(f"site:tistory.com {keyword}")
    url = f"https://search.naver.com/search.naver?where=web&query={encoded}"

    driver.get(url)
    time.sleep(2)

    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="tistory.com"]')

    results = []
    for link in links[:max_results]:
        href = link.get_attribute('href')
        title = link.text
        if 'tistory.com' in href:
            results.append({'title': title, 'url': href, 'platform': 'tistory'})

    return results
```

---

### 2.3 News Articles

#### 2.3.1 Daum News

**Tool**: Selenium WebDriver

**Selector**: `a[href*="v.daum.net"]`

**Process**:
```python
def scrape_daum_news(keyword, max_results=50):
    encoded = urllib.parse.quote(keyword)
    url = f"https://search.daum.net/search?w=news&q={encoded}"

    driver.get(url)
    time.sleep(2)

    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="v.daum.net"]')

    results = []
    for link in links[:max_results]:
        href = link.get_attribute('href')
        title = link.text
        results.append({'title': title, 'url': href})

    return results
```

---

### 2.4 Community Forums

#### 2.4.1 Clien

**Tool**: Selenium WebDriver

**Process**:
```python
def scrape_clien(keyword, max_results=30):
    encoded = urllib.parse.quote(keyword)
    url = f"https://www.clien.net/service/search?q={encoded}&sort=recency"

    driver.get(url)
    time.sleep(2)

    items = driver.find_elements(By.CSS_SELECTOR, '.list_item')

    results = []
    for item in items[:max_results]:
        link = item.find_element(By.CSS_SELECTOR, 'a.subject_fixed')
        results.append({
            'title': link.text,
            'url': link.get_attribute('href')
        })

    return results
```

#### 2.4.2 Blind

**Tool**: Selenium WebDriver

**Note**: Blind requires login for full content access. Collection limited to public search results.

---

### 2.5 YouTube

**Tool**: Selenium WebDriver

**Process**:
```python
def search_youtube(keyword, max_results=30):
    encoded = urllib.parse.quote(keyword)
    url = f"https://www.youtube.com/results?search_query={encoded}"

    driver.get(url)
    time.sleep(3)

    videos = driver.find_elements(By.CSS_SELECTOR, 'ytd-video-renderer')

    results = []
    for video in videos[:max_results]:
        title_elem = video.find_element(By.CSS_SELECTOR, '#video-title')
        results.append({
            'title': title_elem.text,
            'url': title_elem.get_attribute('href')
        })

    return results
```

---

## 3. Content Extraction Pipeline

### 3.1 Universal Content Scraper

```python
def scrape_content(url):
    """Extract main content from any URL"""

    driver.get(url)
    time.sleep(2)

    # Priority-ordered CSS selectors for content extraction
    CONTENT_SELECTORS = [
        '.wrap_body',              # Brunch
        '.tt_article_useless_p_margin',  # Tistory
        '.article_view',           # News sites
        '.entry-content',          # WordPress
        '.post-content',           # Generic blog
        '#content',                # Generic
        'article',                 # HTML5 semantic
        '.contents_style',         # Korean blogs
        '.se-main-container'       # Naver Blog
    ]

    for selector in CONTENT_SELECTORS:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            text = element.text.strip()
            if len(text) > 100:  # Minimum content threshold
                return text[:5000]  # Max 5000 characters
        except:
            continue

    return ""
```

### 3.2 Content Quality Thresholds

| Metric | Threshold | Purpose |
|--------|-----------|---------|
| Minimum Length | 100 chars | Filter empty/error pages |
| Maximum Length | 5000 chars | Storage optimization |
| Encoding | UTF-8 | Korean language support |

---

## 4. Data Quality Assurance

### 4.1 Validation Checks

```python
def validate_data_quality(df, service_name):
    issues = []

    # Check 1: Company field consistency
    wrong_company = df[df['company'] != service_name]
    if len(wrong_company) > 0:
        issues.append(f"Company mismatch: {len(wrong_company)} records")

    # Check 2: Cross-contamination detection
    competitor_keywords = get_competitor_keywords(service_name)
    contaminated = 0
    for _, row in df.iterrows():
        text = str(row['text']).lower() + str(row['title']).lower()
        if any(kw in text for kw in competitor_keywords):
            contaminated += 1

    if contaminated / len(df) > 0.10:  # >10% threshold
        issues.append(f"Cross-contamination: {contaminated} records")

    # Check 3: Text presence rate
    text_rate = df['text'].notna().sum() / len(df)
    if text_rate < 0.80:  # <80% threshold
        issues.append(f"Low text rate: {text_rate:.1%}")

    return issues
```

### 4.2 Decontamination Process

```python
def remove_competitor_data(df, service_name):
    """Remove records that belong to competitor services"""

    own_keywords = SERVICE_KEYWORDS[service_name]
    competitor_keywords = COMPETITOR_KEYWORDS[service_name]

    def is_valid_record(row):
        text = str(row['text']).lower() + str(row['title']).lower()

        has_own = any(kw in text for kw in own_keywords)
        has_competitor = any(kw in text for kw in competitor_keywords)

        # Keep if: has own keyword OR doesn't have competitor keyword
        return has_own or not has_competitor

    return df[df.apply(is_valid_record, axis=1)]
```

---

## 5. Final Data Distribution

### 5.1 By Service

| Service | Total | App Review | Blog | News | Community | YouTube |
|---------|-------|------------|------|------|-----------|---------|
| Ringle | 1,782 | 309 | 452 | 385 | 494 | 142 |
| MaxAI | 594 | 330 | 105 | 14 | 56 | 89 |
| Santa | 925 | 700 | 79 | 14 | 35 | 97 |
| Malhae | 860 | 700 | 59 | 9 | 21 | 71 |
| Cake | 936 | 697 | 86 | 1 | 67 | 85 |
| Hackers | 991 | 700 | 97 | 21 | 55 | 118 |
| Yanadu | 864 | 606 | 97 | 21 | 53 | 87 |
| Carrot | 654 | 486 | 48 | 11 | 39 | 70 |
| Pagoda | 256 | 73 | 64 | 36 | 40 | 43 |
| Uphone | 1,307 | 1,155 | 53 | 26 | 17 | 56 |
| **Total** | **9,169** | **5,756** | **1,140** | **538** | **877** | **858** |

### 5.2 By Platform

| Platform | Records | Percentage |
|----------|---------|------------|
| App Store | 3,187 | 34.8% |
| Play Store | 2,569 | 28.0% |
| YouTube | 858 | 9.4% |
| Clien | 496 | 5.4% |
| Brunch | 493 | 5.4% |
| Naver Blog | 330 | 3.6% |
| Tistory | 323 | 3.5% |
| Daum News | 336 | 3.7% |
| Blind | 353 | 3.8% |
| Others | 224 | 2.4% |

---

## 6. Technical Stack

### 6.1 Core Dependencies

```
python >= 3.8
pandas >= 1.3.0
selenium >= 4.0.0
google-play-scraper >= 1.2.0
requests >= 2.28.0
```

### 6.2 Selenium Configuration

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)

    return driver
```

---

## 7. File Structure

```
data/
├── DATA_COLLECTION_FRAMEWORK.md    # This document
├── {service}/
│   ├── {service}_master_data.csv   # Unified master data
│   ├── review/
│   │   ├── playstore/
│   │   │   └── {service}_playstore.csv
│   │   └── appstore/
│   │       └── {service}_appstore.csv
│   ├── blog/
│   │   ├── {service}_naver_blog.csv
│   │   ├── {service}_brunch.csv
│   │   └── {service}_tistory.csv
│   ├── news/
│   │   └── {service}_daum_news.csv
│   └── community/
│       └── {service}_clien.csv
```

---

## 8. Usage Guidelines

### 8.1 Running Full Collection Pipeline

```python
# 1. Initialize services
services = ['ringle', 'maxai', 'santa', 'malhae', 'cake',
            'hackers', 'yanadu', 'carrot', 'pagoda', 'uphone']

# 2. For each service
for service in services:
    # Collect app reviews
    collect_playstore_reviews(service)
    collect_appstore_reviews(service)

    # Collect blog content
    collect_naver_blog(service)
    collect_brunch(service)
    collect_tistory(service)

    # Collect news
    collect_daum_news(service)

    # Collect community
    collect_clien(service)

    # Collect YouTube
    collect_youtube(service)

    # Merge to master data
    create_master_data(service)

    # Quality assurance
    validate_and_clean(service)
```

### 8.2 Incremental Updates

```python
# For periodic updates, only collect new content
def incremental_update(service, days=7):
    existing_df = pd.read_csv(f'{service}/{service}_master_data.csv')
    existing_urls = set(existing_df['url'].dropna())

    # Collect new data
    new_data = collect_all_sources(service)

    # Filter to only new URLs
    new_data = new_data[~new_data['url'].isin(existing_urls)]

    # Append to master
    updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    updated_df.to_csv(f'{service}/{service}_master_data.csv', index=False)
```

---

## 9. Limitations & Considerations

### 9.1 Known Limitations

1. **Rate Limiting**: App store APIs have rate limits; implement delays between requests
2. **Dynamic Content**: Some sites require JavaScript rendering (handled by Selenium)
3. **Login Walls**: Blind and some communities require authentication for full access
4. **Content Changes**: URLs may become invalid over time

### 9.2 Ethical Considerations

- Respect robots.txt directives
- Implement reasonable request delays (2-3 seconds)
- Do not collect personal identifiable information beyond public usernames
- Use data only for research/analysis purposes

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-18 | Initial data collection (8 services) |
| 1.1 | 2026-01-18 | Added Pagoda, Uphone services |
| 1.2 | 2026-01-18 | Data quality validation and cleaning |

---

**Document Author**: Data Collection Pipeline
**Last Updated**: 2026-01-18
**Total Records**: 9,169
**Services Covered**: 10
