# JaeMoney - 최종 아키텍처 설계

## 📌 목표
- **GitHub Actions**: 30분마다 자동으로 DART 크롤링 + 알림 발송
- **웹 서버**: 필요할 때만 켜서 거래 기록 조회
- **비용**: 완전 무료
- **알림**: 두 명에게 이메일 + SMS 동시 발송

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Repository                      │
│                      (Public, 무료)                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📄 trades.json                                              │
│  └─ 거래 데이터만 (개인정보 없음)                            │
│     {                                                        │
│       "trades": [                                            │
│         {                                                    │
│           "id": 1,                                           │
│           "symbol": "AAPL",                                  │
│           "company": "Apple",                                │
│           "type": "BUY",                                     │
│           "quantity": 100,                                   │
│           "price": 150.5,                                    │
│           "timestamp": "2024-01-15T10:30:00"                │
│         }                                                    │
│       ]                                                      │
│     }                                                        │
│                                                              │
│  🔧 .github/workflows/crawl-notify.yml                       │
│  └─ 30분마다 자동 실행                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         ↑                                      ↑
         │                                      │
    [Read/Write]                          [Read Only]
         │                                      │
┌────────┴──────────────────┐    ┌─────────────┴────────┐
│  GitHub Actions           │    │  로컬 웹 서버         │
│  (24/7 자동)             │    │  (필요할 때만)        │
├──────────────────────────┤    ├───────────────────────┤
│                          │    │                       │
│ 1. DART 크롤링          │    │ 1. 시작 시           │
│ 2. 새 거래 감지         │    │    trades.json      │
│ 3. trades.json 저장     │    │    다운로드          │
│ 4. GitHub 커밋         │    │                       │
│ 5. 알림 발송 📧📱       │    │ 2. 웹에 표시        │
│    ├─ USER_1           │    │    (최신 데이터)      │
│    └─ USER_2           │    │                       │
│                          │    │ 3. React 대시보드    │
└──────────────────────────┘    └───────────────────────┘
         ↓
    Secrets (비공개)
    ├─ USER_1_EMAIL
    ├─ USER_1_PHONE
    ├─ USER_2_EMAIL
    ├─ USER_2_PHONE
    ├─ SENDGRID_API_KEY
    └─ TWILIO_API_KEY
```

---

## 🔄 30분 실행 사이클

```
시간: 10:00 AM
┌─────────────────────────────────────┐
│ 1️⃣ GitHub Actions 자동 실행 시작     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 2️⃣ DART API 크롤링                  │
│    - 이전 거래 이후 모든 거래 조회    │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │ 새 거래      │
        │ 있나?       │
        └──┬───────┬──┘
        YES│       │NO
           │       │
    ┌──────▼──┐  ┌─▼─────────┐
    │ 처리    │  │ 30분 후    │
    │ 계속    │  │ 다시 실행  │
    └──────┬──┘  └───────────┘
           │
┌──────────▼──────────────────────┐
│ 3️⃣ trades.json 업데이트         │
│    {                            │
│      "id": 1,                   │
│      "symbol": "AAPL",          │
│      "company": "Apple",        │
│      "type": "BUY",             │
│      "quantity": 100,           │
│      "price": 150.5,            │
│      "timestamp": "10:00:00"    │
│    }                            │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 4️⃣ GitHub에 자동 커밋              │
│    "New trade: AAPL BUY 100"       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 5️⃣ Secrets 읽기                     │
│    ├─ USER_1_EMAIL                 │
│    ├─ USER_1_PHONE                 │
│    ├─ USER_2_EMAIL                 │
│    ├─ USER_2_PHONE                 │
│    ├─ SENDGRID_API_KEY             │
│    └─ TWILIO_API_KEY               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 6️⃣ 알림 발송                        │
│    USER_1:                         │
│    ├─ 이메일 📧                     │
│    └─ SMS 📱                        │
│    USER_2:                         │
│    ├─ 이메일 📧                     │
│    └─ SMS 📱                        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 7️⃣ 완료! 다음 30분 대기             │
└──────────────────────────────────────┘
```

---

## 📁 파일 구조

```
JaeMoney/
├── .github/
│   └── workflows/
│       └── crawl-notify.yml          # ⭐ 핵심: 30분마다 실행
│
├── data/
│   └── trades.json                   # ⭐ GitHub이 자동 관리
│
├── scripts/                          # 실행 스크립트
│   ├── crawl_dart.py                # DART 크롤링
│   └── send_notifications.py         # 알림 발송
│
├── frontend/                         # React 웹
│   ├── src/
│   │   ├── pages/Dashboard.tsx      # trades.json 표시
│   │   └── services/api.ts          # GitHub Raw URL에서 JSON 다운로드
│   └── package.json
│
├── ARCHITECTURE_DESIGN.md            # 이 파일
├── SETUP.md                          # 설정 가이드
├── README.md
└── .gitignore
```

---

## 🔐 GitHub Secrets 설정

### 설정할 값 (GitHub 관리자만 볼 수 있음)

```
Repository Settings → Secrets and variables → Actions

Secret Name          │ 예시 값
─────────────────────┼──────────────────────────
USER_1_EMAIL         │ user1@gmail.com
USER_1_PHONE         │ +82-10-1234-5678
USER_2_EMAIL         │ user2@naver.com
USER_2_PHONE         │ +82-10-9876-5432
SENDGRID_API_KEY     │ SG.xxx...
TWILIO_ACCOUNT_SID   │ ACxxx...
TWILIO_AUTH_TOKEN    │ authxxx...
DART_API_KEY         │ (선택사항)
```

---

## 📊 trades.json 스키마

### 전체 구조

```json
{
  "last_updated": "2024-01-15T10:30:00Z",
  "update_count": 5,
  "trades": [
    {
      "id": 1,
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "trade_type": "BUY",
      "quantity": 100,
      "price": 150.5,
      "total_amount": 15050,
      "trade_date": "2024-01-15T10:30:00Z",
      "disclosure_source": "DART",
      "discovered_at": "2024-01-15T10:35:00Z"
    },
    {
      "id": 2,
      "symbol": "MSFT",
      "company_name": "Microsoft",
      "trade_type": "SELL",
      "quantity": 50,
      "price": 380.2,
      "total_amount": 19010,
      "trade_date": "2024-01-15T14:20:00Z",
      "disclosure_source": "DART",
      "discovered_at": "2024-01-15T14:25:00Z"
    }
  ]
}
```

### 각 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | number | 거래 고유 ID |
| `symbol` | string | 종목 코드 (예: AAPL) |
| `company_name` | string | 회사명 |
| `trade_type` | string | "BUY" 또는 "SELL" |
| `quantity` | number | 거래 수량 |
| `price` | number | 주가 |
| `total_amount` | number | 총액 (quantity × price) |
| `trade_date` | string | 거래 일시 (ISO 8601) |
| `disclosure_source` | string | 공시 출처 ("DART", "금감원" 등) |
| `discovered_at` | string | 감지된 시간 |

---

## 🤖 GitHub Actions 워크플로우 상세

### 실행 조건
- **스케줄**: 매일 자동 (UTC 기준)
  ```
  0 * * * *    → 매시간 정각 (00분)
  */30 * * * * → 매 30분마다
  0 9 * * *    → 매일 09:00 UTC
  ```

### 실행 단계

```
1. Environment Setup
   └─ Python 3.11 설치
   └─ 의존성 설치 (requests, BeautifulSoup4)

2. DART Crawling
   └─ DART API 호출
   └─ 새 거래 조회
   └─ JSON으로 파싱

3. Check for New Trades
   └─ trades.json과 비교
   └─ 중복 필터링
   └─ 새 거래만 선택

4. Update trades.json
   └─ 새 거래 추가
   └─ last_updated 업데이트
   └─ JSON 포맷팅

5. Commit & Push
   └─ git add data/trades.json
   └─ git commit "New trade: AAPL BUY 100"
   └─ git push origin main

6. Send Notifications
   ├─ USER_1
   │  ├─ SendGrid로 이메일 발송
   │  │  "From: noreply@jaemoney.com"
   │  │  "To: USER_1_EMAIL"
   │  │  "Subject: [JaeMoney] Apple 매수 100주"
   │  │  "Body: [거래 상세정보]"
   │  │
   │  └─ Twilio로 SMS 발송
   │     "To: USER_1_PHONE"
   │     "[JaeMoney] AAPL 매수 100주 $15,050"
   │
   └─ USER_2
      ├─ SendGrid로 이메일 발송
      └─ Twilio로 SMS 발송

7. Logging
   └─ 성공 또는 실패 기록
   └─ GitHub Actions 로그에 저장
```

---

## 💻 로컬 웹 서버 동작

### 시작 시 (npm start)

```
1. 앱 시작
   └─ React 앱 로드

2. GitHub에서 trades.json 다운로드
   └─ URL: https://raw.githubusercontent.com/groom2hub/JaeMoney/main/data/trades.json
   └─ 메모리에 로드

3. 웹에 표시
   ├─ Dashboard: 통계 + 차트
   ├─ Trade History: 테이블
   └─ (모두 최신 데이터)

4. 필요 시 새로고침
   └─ 우클릭 → 새로고침
   └─ 또는 대시보드의 "데이터 새로고침" 버튼
```

### 데이터 흐름

```
GitHub Repository
└─ trades.json (원본 데이터)
   ↓
GitHub Raw URL
└─ https://raw.githubusercontent.com/...
   ↓
브라우저 (JavaScript)
└─ fetch() API로 다운로드
   ↓
React State (메모리)
└─ useTradesStore
   ↓
웹에 표시
└─ Dashboard, History, Charts
```

---

## 📧 알림 형식

### 이메일

**발신자:** noreply@jaemoney.com  
**제목:** `[JaeMoney] [회사명] [거래유형] [수량]주`  
**본문:**

```
새로운 주식 거래가 감지되었습니다.

회사명: Apple Inc.
종목: AAPL
거래 유형: 매수
수량: 100주
주가: $150.50
총액: $15,050
거래 일시: 2024-01-15 10:30:00

자세한 정보는 다음 링크에서 확인하세요:
https://jaemoney.example.com (배포 후)

---
JaeMoney - 주식 거래 모니터링 서비스
```

### SMS

**메시지:**

```
[JaeMoney] AAPL 매수 100주 $15,050
```

또는

```
[JaeMoney] Apple 매수 100주
총액: $15,050
거래일시: 2024-01-15 10:30
```

---

## 🔄 데이터 갱신 흐름

```
GitHub Actions 실행            로컬 웹 서버
    (자동)                     (필요할 때)
       │
       │ 30분마다
       ├─ DART 크롤링
       │
       ├─ 새 거래?
       │  YES ↓
       │
       ├─ trades.json 업데이트
       │
       ├─ GitHub 커밋
       │
       ├─ 알림 발송 📧📱
       │
       └─ 대기 30분
                                   │
                                   │ npm start
                                   ↓
                            GitHub에서 JSON 다운로드
                                   ↓
                            웹에 즉시 표시 (최신)
```

---

## ✅ 체크리스트

### 사전 준비
- [ ] GitHub 저장소 생성
- [ ] SendGrid 계정 (무료)
- [ ] Twilio 계정 (무료 트라이얼)
- [ ] DART API 키 (선택사항)

### GitHub 설정
- [ ] Secrets 6개 입력
- [ ] workflows 디렉토리 생성
- [ ] crawl-notify.yml 생성

### 로컬 설정
- [ ] Node.js 설치
- [ ] npm install
- [ ] .env 설정 (로컬용)

### 테스트
- [ ] GitHub Actions 수동 실행 (Run workflow)
- [ ] 알림 받았나 확인
- [ ] trades.json 업데이트 확인
- [ ] npm start → 웹에서 확인

---

## 🎯 최종 결과

✅ **GitHub Actions**: 24/7 자동 크롤링 + 알림  
✅ **웹 서버**: 필요할 때만 (1분 이내 시작)  
✅ **비용**: 완전 무료 (GitHub + SendGrid + Twilio 무료 티어)  
✅ **보안**: 개인정보는 Secrets (비공개)  
✅ **투명성**: 거래정보는 공개 (trades.json)  
✅ **두 명 알림**: 이메일 + SMS 동시 발송  

---

**다음 단계**: 코드 구현 시작! 🚀
