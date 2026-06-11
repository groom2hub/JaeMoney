# JaeMoney 로컬 실행 가이드

## 필수 설치

- Docker & Docker Compose
- Node.js 18+ (프론트엔드용)

## 1️⃣ Backend + Database 실행

### 터미널 1: Docker 실행
```bash
cd /Users/choijunhyeok/Desktop/JaeMoney
docker-compose up
```

출력 예시:
```
postgres_1  | database system is ready to accept connections
redis_1     | Ready to accept connections
backend_1   | INFO:     Application startup complete
```

✅ 완료 신호: `Application startup complete`

### API 테스트
```bash
curl http://localhost:8000/health
# 응답: {"status":"healthy"}
```

## 2️⃣ Frontend 실행

### 터미널 2: Node 모듈 설치
```bash
cd /Users/choijunhyeok/Desktop/JaeMoney/frontend
npm install
```

완료 시간: ~2분

### 터미널 2: 프론트엔드 시작
```bash
npm start
```

자동으로 브라우저 열림: http://localhost:3000

## 3️⃣ 사용해보기

### 회원가입
1. http://localhost:3000 접속
2. "회원가입" 클릭
3. 이메일/비밀번호 입력 (예: `test@example.com` / `password123`)
4. 회원가입 완료

### 거래 정보 입력 (API로)
```bash
# 토큰 얻기
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"

# 거래 추가
curl -X POST http://localhost:8000/api/trades \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "company_name": "Apple Inc.",
    "trade_type": "BUY",
    "quantity": 100,
    "price": 150.50,
    "trade_date": "2024-01-15T10:30:00",
    "disclosure_source": "DART"
  }'
```

## 4️⃣ API 문서 확인

Swagger UI: http://localhost:8000/docs

모든 엔드포인트 테스트 가능

## 🛑 중지하기

### Ctrl + C로 각 터미널 중지

```bash
# Docker 완전 중지
docker-compose down
```

## 📝 기본 테스트 계정

이미 만든 계정으로 로그인 가능:
- 이메일: `test@example.com`
- 비밀번호: `password123`

## ❓ 문제 해결

### Port 이미 사용 중
```bash
# 8000 포트 사용 프로세스 확인
lsof -i :8000
```

### DB 연결 실패
```bash
# Docker 로그 확인
docker-compose logs postgres
```

### Node modules 문제
```bash
# 재설치
rm -rf frontend/node_modules frontend/package-lock.json
npm install
```

---

이제 모두 실행됩니다! 🚀
