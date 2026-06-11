# 🔐 GitHub Secrets 설정 가이드

## 위치
```
GitHub 저장소
  ↓
Settings (설정 탭)
  ↓
Secrets and variables (왼쪽 메뉴)
  ↓
Actions
  ↓
New repository secret 버튼
```

**직접 URL:** https://github.com/groom2hub/JaeMoney/settings/secrets/actions

---

## 📝 7개 Secret 설정 방법

### Secret 1️⃣: USER_1_EMAIL
**설정 위치:**
```
Name: USER_1_EMAIL
Secret: (이메일 입력)
```

**어디서 얻는가?**
- 본인의 이메일 주소
- 예: `your-email@gmail.com`

---

### Secret 2️⃣: USER_1_PHONE
**설정 위치:**
```
Name: USER_1_PHONE
Secret: (전화번호 입력)
```

**어디서 얻는가?**
- 본인의 전화번호
- 형식: `+82-10-1234-5678` 또는 `010-1234-5678`
- 예: `+82-10-1111-1111`

---

### Secret 3️⃣: USER_2_EMAIL
**설정 위치:**
```
Name: USER_2_EMAIL
Secret: (이메일 입력)
```

**어디서 얻는가?**
- 친구/동료 이메일
- 예: `friend@naver.com`

---

### Secret 4️⃣: USER_2_PHONE
**설정 위치:**
```
Name: USER_2_PHONE
Secret: (전화번호 입력)
```

**어디서 얻는가?**
- 친구/동료 전화번호
- 형식: `+82-10-5678-9012` 또는 `010-5678-9012`
- 예: `+82-10-2222-2222`

---

### Secret 5️⃣: SENDGRID_API_KEY ⭐ 중요

#### Step 1: SendGrid 계정 생성
1. https://sendgrid.com 접속
2. **Sign Up** 클릭
3. 이메일, 비밀번호 입력
4. 계정 생성 완료

#### Step 2: API Key 생성
1. SendGrid 대시보드 로그인
2. **Settings** → **API Keys** 클릭
3. **Create API Key** 버튼
4. Name: `JaeMoney` 입력
5. Permission: **Full Access** 선택
6. **Create & Copy** 클릭
7. **복사된 키를 Secret에 붙여넣기**

**설정 위치:**
```
Name: SENDGRID_API_KEY
Secret: (SendGrid에서 복사한 API Key 전체)
```
참고: SendGrid API Key는 SG로 시작하는 긴 문자열

⚠️ **주의:** 키를 잃어버리면 다시 생성해야 함!

---

### Secret 6️⃣: TWILIO_ACCOUNT_SID ⭐ 중요

#### Step 1: Twilio 계정 생성
1. https://www.twilio.com 접속
2. **Sign Up** 클릭
3. 이메일, 비밀번호 입력
4. 전화번호 확인 (SMS 받음)
5. 계정 생성 완료

#### Step 2: Account SID 복사
1. Twilio 콘솔 로그인
2. https://www.twilio.com/console 접속
3. **Account SID** 찾기 (화면 우측 상단)
4. 복사 아이콘 클릭
5. Secret에 붙여넣기

**설정 위치:**
```
Name: TWILIO_ACCOUNT_SID
Secret: (Twilio에서 복사한 Account SID)
```

---

### Secret 7️⃣: TWILIO_AUTH_TOKEN ⭐ 중요

#### Step 1: Auth Token 복사
1. Twilio 콘솔 (https://www.twilio.com/console)
2. **Auth Token** 찾기 (Account SID 아래)
3. 복사 아이콘 클릭
4. Secret에 붙여넣기

**설정 위치:**
```
Name: TWILIO_AUTH_TOKEN
Secret: (Twilio에서 복사한 Auth Token)
```

---

## 🎯 최종 체크리스트

### SendGrid
- [ ] 계정 생성됨
- [ ] API Key 생성됨
- [ ] API Key 복사됨

### Twilio
- [ ] 계정 생성됨
- [ ] Account SID 찾음
- [ ] Auth Token 찾음

### GitHub Secrets (총 7개)
- [ ] USER_1_EMAIL
- [ ] USER_1_PHONE
- [ ] USER_2_EMAIL
- [ ] USER_2_PHONE
- [ ] SENDGRID_API_KEY
- [ ] TWILIO_ACCOUNT_SID
- [ ] TWILIO_AUTH_TOKEN

---

## 📸 GitHub Secrets 설정 예시

### 화면 구성
```
┌─ Settings ─────────────────────────────────────┐
│                                                │
│ Code security and analysis                    │
│ ├─ Secrets and variables ← 여기 클릭          │
│ │  ├─ Actions                                 │
│ │  ├─ Dependabot                              │
│ │  └─ Codespaces                              │
│ │                                              │
│ └─ Actions                                    │
│    └─ General                                 │
│                                                │
└────────────────────────────────────────────────┘
```

### Actions 탭 열면
```
┌─ Actions ────────────────────────────────────┐
│                                              │
│ Repository secrets                          │
│ ┌──────────────────────────────────────┐    │
│ │ Name           │ Updated   │ Action │    │
│ ├──────────────────────────────────────┤    │
│ │ USER_1_EMAIL   │ 1 min ago │  ✎  🗑  │    │
│ │ USER_1_PHONE   │ 1 min ago │  ✎  🗑  │    │
│ │ USER_2_EMAIL   │ 1 min ago │  ✎  🗑  │    │
│ │ USER_2_PHONE   │ 1 min ago │  ✎  🗑  │    │
│ │ SENDGRID_...   │ 1 min ago │  ✎  🗑  │    │
│ │ TWILIO_ACCOUNT │ 1 min ago │  ✎  🗑  │    │
│ │ TWILIO_AUTH... │ 1 min ago │  ✎  🗑  │    │
│ └──────────────────────────────────────┘    │
│                                              │
│ 🟢 New repository secret 버튼                │
│                                              │
└──────────────────────────────────────────────┘
```

---

## ⚠️ 주의사항

### 보안
- ❌ 절대 Secret 값을 코드에 저장하지 마세요
- ❌ 절대 누구에게도 API 키를 공유하지 마세요
- ✅ GitHub Secrets에만 저장하세요

### API 키 재생성
- SendGrid: Settings → API Keys → Delete → Create New
- Twilio: Auth Token을 잘못 저장하면 다시 생성

### 테스트
- Secret 설정 후 GitHub Actions 수동 실행
- Actions 탭 → "Run workflow"

---

## 🔍 각 서비스별 상세 가이드

### SendGrid 계정에서 API Key 찾기

1. SendGrid 대시보드 접속
2. 좌측 메뉴 → **Settings**
3. **API Keys** 클릭
4. **Create API Key** 버튼
   ```
   Name: JaeMoney
   API Key Type: Full Access (추천)
   ```
5. **Create & Copy** 클릭
6. 검은색 키가 나타남:
   ```
   SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   → 이걸 복사해서 GitHub Secret에 붙여넣기

### Twilio 계정에서 SID/Token 찾기

1. Twilio 콘솔 접속 (https://www.twilio.com/console)
2. Dashboard 화면에서 Account SID와 Auth Token을 볼 수 있음
3. 각각을 복사해서 GitHub Secret에 붙여넣기
   - Account SID: AC로 시작하는 긴 문자열
   - Auth Token: 하이픈으로 구분된 복잡한 문자열

---

## 🎉 완료!

모든 Secret이 설정되면:
- ✅ GitHub Actions 30분마다 자동 실행 가능
- ✅ 두 명에게 이메일/SMS 발송 가능
- ✅ trades.json 자동 업데이트

**다음 단계:** GitHub Actions 수동 실행으로 테스트! 🚀
