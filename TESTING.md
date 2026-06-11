# 🧪 전체 시스템 테스트 가이드

## 📋 테스트 체크리스트

### Step 1: GitHub Secrets 설정 (필수)

GitHub 저장소 → Settings → Secrets and variables → Actions

다음 6개 추가:

```
SECRET NAME          │ 설정값
─────────────────────┼─────────────────────────
USER_1_EMAIL         │ 첫 번째 수신자 이메일
USER_1_PHONE         │ 첫 번째 수신자 전화번호
USER_2_EMAIL         │ 두 번째 수신자 이메일
USER_2_PHONE         │ 두 번째 수신자 전화번호
SENDGRID_API_KEY     │ SendGrid API 키
TWILIO_ACCOUNT_SID   │ Twilio 계정 SID
TWILIO_AUTH_TOKEN    │ Twilio 인증 토큰
DART_API_KEY         │ DART API 키 (선택)
```

✅ **예시:**
```
USER_1_EMAIL = your-email@gmail.com
USER_1_PHONE = +82-10-1234-5678
USER_2_EMAIL = other-email@naver.com
USER_2_PHONE = +82-10-9876-5432
```

---

### Step 2: GitHub Actions 수동 실행 (테스트)

#### 2-1. 로컬에서 스크립트 테스트

```bash
cd /Users/choijunhyeok/Desktop/JaeMoney

# 환경 변수 설정 (.env 파일)
export DART_API_KEY="test-key"
export USER_1_EMAIL="test1@gmail.com"
export USER_1_PHONE="+82-10-1111-1111"
export USER_2_EMAIL="test2@gmail.com"
export USER_2_PHONE="+82-10-2222-2222"
export SENDGRID_API_KEY="test-sendgrid"
export TWILIO_ACCOUNT_SID="test-twilio-sid"
export TWILIO_AUTH_TOKEN="test-twilio-token"

# 스크립트 실행
python scripts/crawl_dart.py
python scripts/send_notifications.py
```

**예상 출력:**
```
==================================================
🤖 DART 크롤링 시작
⏰ 2024-01-15T10:30:00Z
==================================================
🔍 DART 크롤링 시작...
✅ DART 데이터 조회 완료
ℹ️  새로운 거래 정보 없음
==================================================
✅ 크롤링 완료! (추가: 0개)
==================================================
```

#### 2-2. GitHub에서 수동 실행

1. GitHub 저장소 페이지 열기
2. Actions 탭 클릭
3. "🤖 DART Crawling & Notifications" 선택
4. "Run workflow" 드롭다운 클릭
5. "Run workflow" 버튼 클릭

**로그 확인:**
- Actions 탭 → 최신 실행 클릭
- "crawl-and-notify" 작업 클릭
- 각 Step의 로그 확인

---

### Step 3: 테스트 거래 데이터 추가

#### 3-1. trades.json 수동 추가 (테스트용)

```bash
# trades.json에 테스트 거래 추가
cat > /Users/choijunhyeok/Desktop/JaeMoney/data/trades.json << 'EOF'
{
  "last_updated": "2024-01-15T10:30:00Z",
  "update_count": 1,
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
      "company_name": "Microsoft Corp.",
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
EOF
```

#### 3-2. GitHub에 커밋

```bash
cd /Users/choijunhyeok/Desktop/JaeMoney

git add data/trades.json
git commit -m "Add test trade data for testing"
git push origin main
```

---

### Step 4: 프론트엔드 테스트

#### 4-1. 프론트엔드 시작

```bash
cd /Users/choijunhyeok/Desktop/JaeMoney/frontend

# 처음 한 번
npm install

# 실행
npm start
```

브라우저가 자동으로 http://localhost:3000 열림

#### 4-2. 테스트할 것들

**대시보드 페이지 (http://localhost:3000)**

✅ 통계 카드 확인:
- [ ] 총 매수액: $15,050 (AAPL)
- [ ] 총 매도액: $19,010 (MSFT)
- [ ] 총 거래: 2건
- [ ] 순 자산: -$3,960 (음수)

✅ 파이 차트:
- [ ] 매수: 1개
- [ ] 매도: 1개

✅ 최근 거래 목록:
- [ ] MSFT 매도 표시
- [ ] AAPL 매수 표시

**거래 히스토리 페이지 (/trades)**

✅ 테이블 표시:
- [ ] 2개 거래 모두 보임
- [ ] 최신순 정렬 (MSFT → AAPL)

✅ 필터 테스트:
- [ ] 종목 검색 "AAPL" → AAPL만 보임
- [ ] 거래유형 "BUY" → AAPL만 보임
- [ ] 거래유형 "SELL" → MSFT만 보임

---

## 🔍 디버깅 팁

### 프론트엔드에서 JSON 안 보일 때

브라우저 개발자 도구 (F12) → Console 탭

**확인:**
```javascript
// 콘솔에서 실행
fetch('https://raw.githubusercontent.com/groom2hub/JaeMoney/main/data/trades.json')
  .then(r => r.json())
  .then(d => console.log(d))
```

GitHub Raw URL이 정상인지 확인

### GitHub Actions 로그 확인

Actions 탭 → "🤖 DART Crawling & Notifications" → 최신 실행 클릭

각 Step:
- ✅ Checkout repository
- ✅ Set up Python 3.11
- ✅ Install dependencies
- ✅ Run DART crawling
- ✅ Send notifications
- ✅ Commit and push changes
- ✅ Log execution

### 알림 테스트 (SendGrid/Twilio)

SendGrid:
1. https://app.sendgrid.com 로그인
2. Activity → Logs 확인
3. 이메일 발송 기록 보기

Twilio:
1. https://www.twilio.com/console 로그인
2. Messaging → Logs 확인
3. SMS 발송 기록 보기

---

## ✅ 테스트 완료 체크리스트

- [ ] GitHub Secrets 6개 설정됨
- [ ] 로컬에서 crawl_dart.py 실행됨
- [ ] 로컬에서 send_notifications.py 실행됨
- [ ] GitHub Actions 수동 실행됨
- [ ] trades.json 테스트 데이터 추가됨
- [ ] 프론트엔드 npm start 성공
- [ ] 대시보드 통계 카드 표시됨
- [ ] 파이 차트 표시됨
- [ ] 최근 거래 목록 표시됨
- [ ] 거래 히스토리 테이블 표시됨
- [ ] 필터 작동함

---

## 🎉 전체 테스트 성공!

모든 단계가 완료되면:

```
✅ GitHub Actions 자동 크롤링 설정 완료
✅ 30분마다 alarms 받도록 설정 완료
✅ 웹에서 최신 거래 기록 조회 가능
✅ 시스템 완전히 작동 중!
```

---

## 📌 주의사항

### 로컬 테스트 시
- 환경 변수 설정 필수 (SENDGRID_API_KEY 등)
- 실제 이메일/SMS 발송되지 않음 (API 키가 없으면)
- 다만 코드는 정상 실행됨 (에러 없음)

### GitHub Actions 실행 시
- 실제 이메일/SMS 발송됨 (Secrets 설정 시)
- 30분마다 자동 실행
- 수동 실행도 가능 (Run workflow 버튼)

### 비용 확인
- ✅ GitHub Actions: 무료 (월 2000분)
- ✅ SendGrid: 무료 (월 100개 이메일)
- ✅ Twilio: 무료 트라이얼 ($15 크레딧)

---

**테스트 시작!** 🚀
