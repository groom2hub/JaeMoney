# JaeMoney - Software Requirements Specification (SRS)

## 1. 프로젝트 개요

### 1.1 프로젝트 목표
이재명 대통령의 주식 거래(매매) 정보를 실시간으로 모니터링하고, 이메일 및 SMS/카톡 등의 채널을 통해 즉시 알림을 제공하는 웹 서비스 제공

### 1.2 프로젝트 범위
- 공시 정보 기반 주식 거래 데이터 수집
- 실시간 거래 모니터링 및 알림
- 거래 히스토리 조회 기능
- 통계/분석 대시보드
- 사용자 알림 구독 관리

---

## 2. 기능 요구사항 (FR: Functional Requirements)

### 2.1 데이터 수집 모듈 (Data Collection Module)

#### FR-2.1.1 공시 정보 수집
- **설명**: DART(공정거래위원회 전자공시), 금감원 등 공식 채널에서 주식 거래 정보 수집
- **입력**: 공시 API 또는 웹 크롤링
- **출력**: 구조화된 거래 정보 (종목, 매매 수량, 가격, 일시)
- **주기**: 하루 1-2회 또는 실시간 (가능한 경우)

#### FR-2.1.2 데이터 검증
- 중복 거래 필터링
- 거래 정보 유효성 검사
- 데이터 형식 표준화

### 2.2 알림 시스템 (Notification System)

#### FR-2.2.1 이메일 알림
- 새 거래 발생 시 즉시 이메일 발송
- 알림 내용: 종목명, 거래 유형(매수/매도), 수량, 예상 금액, 거래 일시
- 구독자 이메일 주소 관리

#### FR-2.2.2 SMS/카톡 알림
- 새 거래 발생 시 SMS 또는 카카오톡으로 즉시 푸시
- 간결한 메시지 형식 (예: "[JaeMoney] AAPL 1,000주 매도 $150K")
- 전화번호 또는 카톡 ID 관리

#### FR-2.2.3 알림 선호도 설정
- 사용자가 알림 채널 선택 가능 (이메일/SMS/카톡)
- 알림 수신 시간대 설정
- 특정 종목만 모니터링 옵션

### 2.3 웹 대시보드 (Web Dashboard)

#### FR-2.3.1 실시간 모니터링 페이지
- 현재 진행 중인 주식 거래 목록 표시
- 최근 거래 히스토리 (최근 1시간, 1일, 1주일 등)
- 거래 유형별 필터링 (매수/매도)
- 자동 새로고침 (매 30초 또는 5분)

#### FR-2.3.2 거래 히스토리 조회
- 전체 거래 내역 검색 및 조회
- 기간별 필터링 (시작일~종료일)
- 종목별 필터링
- CSV 다운로드 기능

#### FR-2.3.3 통계 및 분석 대시보드
- 누적 매수액 / 매도액
- 월별/분기별 거래 현황
- 거래 빈도 분석 (일 평균 거래 횟수, 총 거래액)
- 선호 종목 (가장 많이 거래하는 상위 N개)
- 매수/매도 비율 분석

#### FR-2.3.4 차트 및 시각화
- 거래액 추이 차트 (시계열)
- 종목별 거래량 파이 차트
- 월별 거래 현황 바 차트

### 2.4 사용자 관리 (User Management)

#### FR-2.4.1 회원가입
- 이메일 기반 회원가입
- 이메일 인증 프로세스
- 비밀번호 설정 (최소 8자, 대소문자 + 숫자 포함)

#### FR-2.4.2 로그인 및 세션 관리
- 이메일/비밀번호 로그인
- JWT 또는 세션 기반 인증
- "자동 로그인" 옵션

#### FR-2.4.3 프로필 관리
- 사용자 이메일, 전화번호 수정
- 비밀번호 변경
- 계정 삭제 기능

#### FR-2.4.4 알림 구독 관리
- 사용자별 구독 채널 선택 (이메일/SMS/카톡)
- 구독 활성화/비활성화 토글
- 수신 시간대 설정 (예: 09:00 ~ 21:00만 수신)
- 특정 종목 관심 설정 (옵션)

### 2.5 관리자 기능 (Admin Features)

#### FR-2.5.1 거래 정보 수동 입력
- 시스템에서 감지하지 못한 거래 수동 추가
- 거래 정보 수정/삭제

#### FR-2.5.2 시스템 로그 확인
- 알림 발송 히스토리
- 데이터 수집 로그
- 에러 로그

#### FR-2.5.3 사용자 관리
- 가입한 사용자 목록 조회
- 사용자별 구독 현황
- 사용자 강제 삭제

---

## 3. 비기능 요구사항 (NFR: Non-Functional Requirements)

### 3.1 성능 (Performance)
- **응답 속도**: 웹 페이지 로드 시간 3초 이내
- **데이터베이스 쿼리**: 일반적인 쿼리 응답 시간 500ms 이내
- **알림 발송 지연**: 거래 감지 후 5분 이내 알림 발송
- **동시 사용자**: 최대 1,000 동시 접속 지원

### 3.2 가용성 (Availability)
- **서비스 가용성**: 99.5% 이상
- **장애 대응**: 자동 백업 및 장애 조치(Failover)

### 3.3 보안 (Security)
- **데이터 암호화**: HTTPS/TLS 사용, 민감 데이터 암호화 저장
- **인증**: JWT 또는 OAuth 기반 인증
- **권한 관리**: 역할 기반 접근 제어 (RBAC)
- **개인정보보호**: 사용자 전화번호, 이메일 등 개인정보 암호화
- **OWASP 준수**: OWASP Top 10 취약점 제거

### 3.4 확장성 (Scalability)
- **데이터베이스**: 향후 대량 데이터 처리를 위한 샤딩 지원 설계
- **API**: RESTful API 또는 GraphQL로 향후 모바일 앱 확장 가능
- **마이크로서비스**: 알림 시스템, 데이터 수집 모듈 분리 가능

### 3.5 신뢰성 (Reliability)
- **데이터 무결성**: 거래 데이터 중복 없음 보장
- **재시도 로직**: 알림 발송 실패 시 자동 재시도 (최대 3회)
- **로깅**: 모든 중요 이벤트 로깅

### 3.6 유지보수성 (Maintainability)
- **코드 품질**: 일관된 코딩 스타일, 명확한 주석
- **문서화**: API 문서, 개발 가이드, 배포 문서
- **테스트**: 단위 테스트, 통합 테스트, E2E 테스트

---

## 4. 기술 스택 (Technology Stack)

### 4.1 Backend
- **언어**: Python 3.10+ 또는 Node.js 18+
- **프레임워크**: Django/Flask (Python) 또는 Express.js/NestJS (Node.js)
- **데이터베이스**: PostgreSQL 또는 MySQL
- **캐시**: Redis (세션, 임시 데이터)
- **작업 큐**: Celery (Python) 또는 Bull (Node.js) - 알림 발송, 데이터 수집

### 4.2 Frontend
- **프레임워크**: React 18+
- **상태 관리**: Redux 또는 Zustand
- **UI 라이브러리**: Material-UI, Tailwind CSS
- **차트 라이브러리**: Chart.js, Recharts

### 4.3 Infrastructure
- **호스팅**: AWS, GCP, 또는 Docker + 온프레미스
- **API 서버**: Docker + Kubernetes (선택사항)
- **CI/CD**: GitHub Actions, GitLab CI
- **모니터링**: Prometheus + Grafana, ELK Stack

### 4.4 외부 서비스
- **SMS/카톡**: Twilio, NAVER Cloud SMS API, 카카오 비즈메시지 API
- **이메일**: SendGrid, AWS SES
- **공시 정보**: DART API, 금감원 공시 API 또는 웹 크롤링 (Selenium, BeautifulSoup)

---

## 5. 데이터 모델 (Data Models)

### 5.1 User (사용자)
```
- id (PK)
- email (UK)
- password_hash
- phone_number
- created_at
- updated_at
- is_active
```

### 5.2 StockTrade (주식 거래)
```
- id (PK)
- symbol (종목 코드)
- company_name (회사명)
- trade_type (ENUM: BUY, SELL)
- quantity (수량)
- price (가격)
- total_amount (총액 = quantity * price)
- trade_date (거래 일자)
- disclosure_source (공시 출처: DART, 금감원 등)
- created_at
- updated_at
```

### 5.3 Subscription (알림 구독)
```
- id (PK)
- user_id (FK)
- channel (ENUM: EMAIL, SMS, KAKAO_TALK)
- is_active (구독 여부)
- start_time (수신 시작 시간, 예: 09:00)
- end_time (수신 종료 시간, 예: 21:00)
- created_at
- updated_at
```

### 5.4 Notification (발송된 알림)
```
- id (PK)
- user_id (FK)
- stock_trade_id (FK)
- channel (ENUM: EMAIL, SMS, KAKAO_TALK)
- status (ENUM: PENDING, SENT, FAILED)
- sent_at
- created_at
```

---

## 6. API 엔드포인트 (API Endpoints)

### 6.1 인증 (Auth)
- `POST /api/auth/signup` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/logout` - 로그아웃
- `POST /api/auth/refresh` - 토큰 갱신

### 6.2 사용자 (User)
- `GET /api/users/profile` - 프로필 조회
- `PUT /api/users/profile` - 프로필 수정
- `POST /api/users/change-password` - 비밀번호 변경
- `DELETE /api/users/account` - 계정 삭제

### 6.3 알림 구독 (Subscription)
- `GET /api/subscriptions` - 구독 정보 조회
- `PUT /api/subscriptions` - 구독 정보 수정
- `POST /api/subscriptions/toggle` - 구독 활성화/비활성화

### 6.4 거래 정보 (Stock Trade)
- `GET /api/trades` - 거래 목록 조회 (필터링, 페이지네이션)
- `GET /api/trades/:id` - 거래 상세 정보
- `GET /api/trades/export/csv` - CSV 다운로드

### 6.5 대시보드 (Dashboard)
- `GET /api/dashboard/stats` - 통계 데이터 (누적 매수액, 매도액 등)
- `GET /api/dashboard/chart-data` - 차트 데이터 (월별 거래액 등)
- `GET /api/dashboard/recent-trades` - 최근 거래 (실시간)

### 6.6 관리자 (Admin)
- `POST /api/admin/trades/manual` - 거래 수동 입력
- `PUT /api/admin/trades/:id` - 거래 정보 수정
- `DELETE /api/admin/trades/:id` - 거래 삭제
- `GET /api/admin/logs` - 시스템 로그 조회
- `GET /api/admin/users` - 사용자 목록 조회

---

## 7. 구현 계획 (Implementation Roadmap)

### Phase 1: 기초 구축 (1-2주)
- [ ] 프로젝트 구조 설정 (Backend + Frontend)
- [ ] 데이터베이스 스키마 설계 및 생성
- [ ] 사용자 인증 시스템 구현
- [ ] 기본 API 엔드포인트 구현

### Phase 2: 데이터 수집 및 알림 (2-3주)
- [ ] DART API 또는 웹 크롤링 구현
- [ ] 데이터 검증 로직 구현
- [ ] 이메일 알림 발송 시스템 구현
- [ ] SMS/카톡 알림 발송 시스템 구현
- [ ] 배경 작업 큐 (Celery/Bull) 설정

### Phase 3: 대시보드 및 UI (2-3주)
- [ ] 실시간 모니터링 페이지 개발
- [ ] 거래 히스토리 조회 페이지 개발
- [ ] 통계/분석 대시보드 개발
- [ ] 차트 및 시각화 구현

### Phase 4: 관리자 기능 및 최적화 (1-2주)
- [ ] 관리자 패널 개발
- [ ] 로그 시스템 구현
- [ ] 성능 최적화 (캐싱, 인덱싱)
- [ ] 보안 감사

### Phase 5: 배포 및 운영 (1주)
- [ ] Docker 이미지 생성
- [ ] 배포 스크립트 작성
- [ ] 모니터링 및 로깅 설정
- [ ] 운영 문서 작성

---

## 8. 성공 기준 (Success Criteria)

- [x] 모든 핵심 기능 (FR) 구현 완료
- [x] 비기능 요구사항 (NFR) 충족 (성능, 보안, 가용성)
- [x] 단위 테스트 커버리지 80% 이상
- [x] 통합 테스트 완료
- [x] 배포 및 운영 환경 구성 완료
- [x] 사용자 가이드 및 문서 작성 완료

---

## 9. 위험 및 완화 계획 (Risks & Mitigation)

| 위험 | 영향 | 확률 | 완화 계획 |
|------|------|------|----------|
| 공시 정보 API 변경 | 데이터 수집 실패 | 중 | 웹 크롤링 백업 방안 준비, 정기 모니터링 |
| 외부 SMS API 장애 | 알림 발송 실패 | 중 | 다중 SMS 제공자 사용, 재시도 로직 |
| 데이터베이스 성능 저하 | 서비스 지연 | 낮 | 인덱싱, 캐싱, 샤딩 전략 사전 설계 |
| 보안 취약점 | 데이터 유출 | 낮 | 정기 보안 감사, OWASP 준수, 침투 테스트 |

---

## 10. 참고 자료 (References)

- DART API 문서: https://dart.fsc.go.kr/
- 금감원 공시 정보: https://www.fss.or.kr/
- Twilio SMS API: https://www.twilio.com/
- SendGrid 이메일 API: https://sendgrid.com/
