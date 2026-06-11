# JaeMoney 🚀

> 이재명 대통령 주식 거래 모니터링 서비스

실시간으로 주식 거래 정보를 감지하고, 이메일/SMS/카톡으로 즉시 알림을 받을 수 있는 웹 서비스입니다.

## 🎯 핵심 기능

- **실시간 모니터링**: DART/금감원 공시 정보 자동 감지
- **멀티채널 알림**: 이메일, SMS, 카톡으로 즉시 통보
- **거래 히스토리**: 과거 거래 기록 검색 및 조회
- **분석 대시보드**: 통계, 차트, 거래 패턴 분석
- **사용자 커스터마이징**: 알림 채널, 시간대, 종목 선택

## 📋 요구사항

자세한 요구사항은 [SRS.md](./SRS.md) 참고

### 기술 스택
- **Backend**: Python 3.10+, FastAPI/Flask
- **Frontend**: React 18+, Tailwind CSS
- **Database**: PostgreSQL
- **Cache**: Redis
- **Job Queue**: Celery
- **Deployment**: Docker, Docker Compose

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/groom2hub/JaeMoney.git
cd JaeMoney
```

### 2. 환경 설정
```bash
cp .env.example .env
# .env 파일 수정 (API 키 등)
```

### 3. 백엔드 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 4. 프론트엔드 설정
```bash
cd frontend
npm install
npm start
```

## 📁 프로젝트 구조

```
JaeMoney/
├── SRS.md                      # 상세 요구사항
├── CLAUDE.md                   # 프로젝트 개요
├── README.md                   # 이 파일
├── backend/                    # 백엔드 (Python)
├── frontend/                   # 프론트엔드 (React)
├── docs/                       # 문서
├── docker-compose.yml          # Docker 구성
└── .env.example               # 환경 변수 템플릿
```

## 📖 문서

- [SRS (Software Requirements Specification)](./SRS.md) - 전체 요구사항
- [개발 가이드](./docs/개발가이드.md) - 개발 환경 설정 및 코드 컨벤션
- [API 문서](./docs/API.md) - REST API 엔드포인트
- [배포 가이드](./docs/배포가이드.md) - 프로덕션 배포

## 🔄 개발 단계

- [ ] **Phase 1** (1-2주): 프로젝트 구조 + 인증
- [ ] **Phase 2** (2-3주): 데이터 수집 + 알림
- [ ] **Phase 3** (2-3주): 대시보드 + UI
- [ ] **Phase 4** (1-2주): 관리자 기능 + 최적화
- [ ] **Phase 5** (1주): 배포 + 운영

## 🔐 보안

- JWT 기반 인증
- 개인정보 암호화 저장
- HTTPS/TLS 통신
- OWASP 취약점 대응

⚠️ **법적 고지**: 이 프로젝트는 교육/엔터테인먼트 목적이며, 공시 정보의 사용은 관련 법규를 준수해야 합니다.

## 📝 라이선스

MIT License

## 👤 기여

이슈 및 풀 리퀘스트는 언제든 환영합니다!

## 📧 문의

문제가 있으면 [GitHub Issues](https://github.com/groom2hub/JaeMoney/issues)를 통해 보고해주세요.
