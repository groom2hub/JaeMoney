# JaeMoney - 프로젝트 개요

## 프로젝트 설명
이재명 대통령의 주식 거래 정보를 실시간으로 모니터링하고, 이메일 및 SMS/카톡으로 즉시 알림을 제공하는 웹 서비스

## 핵심 기능
1. **실시간 모니터링**: 공시 정보 기반 주식 거래 자동 감지
2. **멀티채널 알림**: 이메일, SMS, 카톡으로 즉시 통보
3. **거래 히스토리**: 과거 거래 기록 조회 및 검색
4. **분석 대시보드**: 통계, 차트, 거래 패턴 분석
5. **사용자 관리**: 회원가입, 로그인, 알림 구독 설정

## 프로젝트 구조
```
JaeMoney/
├── SRS.md                      # 상세 요구사항 명세서
├── CLAUDE.md                   # 이 파일
├── backend/
│   ├── app.py                  # FastAPI/Flask 애플리케이션
│   ├── requirements.txt         # Python 의존성
│   ├── models/                 # 데이터 모델
│   ├── routes/                 # API 엔드포인트
│   ├── services/               # 비즈니스 로직
│   │   ├── auth_service.py
│   │   ├── stock_service.py
│   │   ├── notification_service.py
│   │   └── crawl_service.py    # DART 크롤링
│   └── workers/                # 백그라운드 작업
│       └── celery_tasks.py
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/           # API 호출
│   │   └── App.tsx
│   └── public/
├── docker-compose.yml
├── .env.example
└── docs/
    ├── API.md
    ├── 개발가이드.md
    └── 배포가이드.md
```

## 기술 스택
- **Backend**: Python + FastAPI/Flask, PostgreSQL, Redis, Celery
- **Frontend**: React 18+, Tailwind CSS, Chart.js
- **Infrastructure**: Docker, GitHub Actions
- **외부 서비스**: DART API, SMS API (Twilio), 이메일 (SendGrid)

## 구현 단계
1. **Phase 1 (1-2주)**: 프로젝트 구조 + 인증 시스템
2. **Phase 2 (2-3주)**: 데이터 수집 + 알림 시스템
3. **Phase 3 (2-3주)**: 대시보드 + UI
4. **Phase 4 (1-2주)**: 관리자 기능 + 최적화
5. **Phase 5 (1주)**: 배포 + 운영 문서

## 주의사항
- 공시 정보의 법적 문제 검토 필요
- DART API 이용약관 확인 필요
- 개인정보(전화번호, 이메일) 암호화 필수

## 다음 단계
1. 기술 스택 확정 (Python/Node.js, 프레임워크 선택)
2. GitHub 레포지토리 연결
3. 개발 환경 구성 (로컬 DB, 가상 환경)
4. Phase 1 시작: 프로젝트 구조 + API 스켈레톤
