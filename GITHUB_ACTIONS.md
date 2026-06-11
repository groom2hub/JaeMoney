# GitHub Actions로 30분마다 알림 보내기

## 📋 개요

GitHub Actions의 `schedule` 트리거를 사용하여 30분마다 자동으로:
1. DART에서 거래 정보 크롤링
2. 새 거래 발견 시 이메일/SMS 알림 발송

## 🔧 설정 단계

### 1️⃣ 서버 배포 (필수)

먼저 API 서버를 항상 실행 중이어야 함:

**Heroku 배포 예시:**
```bash
heroku create jaemoney-api
git push heroku main
```

또는 Railway, Render 등 사용

### 2️⃣ GitHub Secrets 설정

레포지토리 Settings → Secrets and variables → Actions

다음 값 추가:
```
API_URL=https://your-deployed-api.herokuapp.com/api
API_TOKEN=your-jwt-token
DART_API_KEY=your-dart-api-key
SENDGRID_API_KEY=your-sendgrid-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### 3️⃣ Workflow 확인

`.github/workflows/crawl-schedule.yml`가 있으면 완료!

## ⏰ 스케줄 옵션

```yaml
# 30분마다
- cron: '*/30 * * * *'

# 1시간마다
- cron: '0 * * * *'

# 매일 09:00 (UTC)
- cron: '0 9 * * *'

# 매일 09:00, 12:00, 15:00 (UTC)
- cron: '0 9,12,15 * * *'

# 평일만 (월-금)
- cron: '0 9 * * 1-5'
```

## 🚀 수동 실행

GitHub 페이지에서 "Run workflow" 클릭하면 바로 실행

## 📊 실행 로그 확인

레포지토리 → Actions 탭 → 실행 기록 확인

## ⚠️ 주의사항

1. **무료 용량**: GitHub Actions 월 2000분 제공
   - 30분마다 = 하루 48회 = 월 ~1440분 (충분함)

2. **정확도**: ±5분 오차 가능
   - 매우 정확한 시간이 필요하면 외부 스케줄러 사용

3. **서버 응답**: API 서버가 다운되면 크롤링 실패
   - 모니터링 설정 권장

## 🔄 다른 방법들

### 옵션 1: Celery Beat (현재 코드)
```python
# backend/celery_config.py에서 스케줄 설정
app.conf.beat_schedule = {
    'crawl-dart-every-30-min': {
        'task': 'workers.tasks.crawl_dart_task',
        'schedule': 30 * 60,  # 30분
    },
}
```

### 옵션 2: APScheduler
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(crawl_dart, 'interval', minutes=30)
scheduler.start()
```

### 옵션 3: 외부 서비스
- EasyCron
- cron-job.org
- AWS EventBridge

## 📧 실제 이메일 발송 연동

SendGrid 사용 예시:

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email, trade):
    message = Mail(
        from_email='noreply@jaemoney.com',
        to_emails=to_email,
        subject=f'[JaeMoney] {trade["company_name"]} {trade["trade_type"]}',
        plain_text_content=f'거래 발생: {trade["quantity"]}주 @ {trade["price"]}원'
    )
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    sg.send(message)
```

## 📱 실제 SMS 발송 연동

Twilio 사용 예시:

```python
from twilio.rest import Client

def send_sms(phone_number, trade):
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    client.messages.create(
        body=f'[JaeMoney] {trade["company_name"]} {trade["trade_type"]} {trade["quantity"]}주',
        from_='+1234567890',
        to=phone_number
    )
```

---

모두 설정 완료! 이제 자동으로 30분마다 알림이 옵니다 🎉
